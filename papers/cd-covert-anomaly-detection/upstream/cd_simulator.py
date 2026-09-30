#!/usr/bin/env python3
"""
Covert Activity Detection via Anomaly Analysis in Distributed
Spectral Signal Processing
==============================================================
Models a distributed spectrum sensor network detecting covert
(LPI/LPD) signals embedded in background noise + primary users.
Multiple anomaly detection algorithms are compared:
  - Energy detection (baseline)
  - Autoencoder reconstruction
  - One-Class SVM
  - Isolation Forest
  - Cyclostationary detection

Distributed fusion combines local decisions across sensors.
ROC curves, SNR operating range, and scalability are evaluated.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.signal import spectrogram, welch, correlate, butter, filtfilt
from scipy.stats import skew, kurtosis
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
import os, json, itertools, copy, warnings
warnings.filterwarnings('ignore')

matplotlib.rcParams.update({
    'font.family': 'serif', 'font.size': 10,
    'axes.labelsize': 11, 'legend.fontsize': 8,
    'figure.dpi': 150,
})

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)
SEED = 42
rng = np.random.default_rng(SEED)

# ====================================================================
#  CONSTANTS
# ====================================================================
FS = 20e6             # Sampling rate (20 MHz)
T_OBS = 1024e-6       # Observation window (1024 us)
N_SAMPS = int(FS * T_OBS)  # ~20480 samples per observation

N_SENSORS = 4
N_FREQ_BINS = 256     # FFT size
N_TIME_BINS = 80      # Time bins in spectrogram

# Frequency plan (MHz)
F_PRIMARY = [2.4, 2.6, 5.2, 5.8]  # Primary user center freqs (MHz)
F_COVERT_RANGE = (2.3, 5.9)        # Covert signal frequency range

# Detection methods
METHODS = ['Energy', 'Autoencoder', 'OC-SVM', 'IForest', 'Cyclostationary']

# ====================================================================
#  SPECTRUM ENVIRONMENT
# ====================================================================

class SpectrumEnvironment:
    """Generates synthetic RF spectrum with background, primary, and covert signals."""
    def __init__(self, seed=SEED):
        self.rng = np.random.default_rng(seed)
        self.noise_floor_db = -100  # dBm/Hz

    def generate_observation(self, covert_power_db=-115, covert_active=False,
                             n_primary=2, snr_primary_db=15):
        """Generate one observation: time-domain I/Q samples.

        Returns: (samples, label) where label=1 if covert active
        """
        n = N_SAMPS
        t = np.arange(n) / FS
        signal = np.zeros(n, dtype=complex)

        # --- Background noise ---
        noise_power = 10**(self.noise_floor_db / 10) * FS
        noise = (self.rng.normal(size=n) + 1j*self.rng.normal(size=n)) / np.sqrt(2)
        noise *= np.sqrt(noise_power)
        signal += noise

        # --- Primary users (OFDM-like) ---
        active_pri = self.rng.choice(F_PRIMARY, n_primary, replace=False)
        for fp in active_pri:
            pw = 10**((self.noise_floor_db + snr_primary_db) / 10) * FS
            phases = self.rng.uniform(0, 2*np.pi, n)
            pri_sig = np.sqrt(pw) * np.exp(1j * (2*np.pi*fp*1e6*t + phases))
            signal += pri_sig

        # --- Covert signal (narrowband BPSK, frequency-hopped) ---
        label = 1 if covert_active else 0
        if covert_active:
            fc = self.rng.uniform(F_COVERT_RANGE[0], F_COVERT_RANGE[1]) * 1e6
            pw = 10**(covert_power_db / 10) * FS

            # BPSK modulation at symbol rate = 500 kHz
            sym_rate = 500e3
            sym_len = max(1, int(FS / sym_rate))
            n_syms = n // sym_len
            bits = self.rng.choice([-1, 1], n_syms)
            bpsk = np.repeat(bits, sym_len)[:n_syms * sym_len]
            if len(bpsk) < n:
                bpsk = np.pad(bpsk, (0, n - len(bpsk)))
            else:
                bpsk = bpsk[:n]

            covert_sig = np.sqrt(pw) * bpsk * np.exp(1j * 2*np.pi*fc*t)
            signal += covert_sig

        # --- Impulsive noise (optional) ---
        if self.rng.random() < 0.1:
            n_imp = self.rng.integers(1, 5)
            for _ in range(n_imp):
                pos = self.rng.integers(0, n)
                amp = np.sqrt(noise_power * 100) * self.rng.exponential()
                sig_len = self.rng.integers(10, 100)
                end = min(pos + sig_len, n)
                signal[pos:end] += amp * (self.rng.normal(size=end-pos) +
                                          1j*self.rng.normal(size=end-pos))/np.sqrt(2)

        return signal, label

    def generate_dataset(self, n_normal=500, n_anomaly=200, covert_power_db=-85):
        """Generate training + test datasets."""
        X_train, y_train = [], []
        X_test, y_test = [], []

        print(f"  Generating dataset ({n_normal} normal, {n_anomaly} covert)...")
        for i in range(n_normal):
            sig, lab = self.generate_observation(covert_power_db, False)
            feats = extract_features(sig)
            if i < n_normal // 2:
                X_train.append(feats); y_train.append(lab)
            else:
                X_test.append(feats); y_test.append(lab)

        for i in range(n_anomaly):
            sig, lab = self.generate_observation(covert_power_db, True)
            feats = extract_features(sig)
            X_test.append(feats); y_test.append(lab)

        return np.array(X_train), np.array(y_train), \
               np.array(X_test), np.array(y_test)

# ====================================================================
#  FEATURE EXTRACTION
# ====================================================================

def extract_features(signal):
    """Extract statistical and spectral features from I/Q samples.

    Returns a feature vector with:
      - PSD statistics (mean, var, peak, edge energy)
      - Subband energy ratios
      - Higher-order statistics
      - Spectrogram texture features
    """
    n = len(signal)
    feats = []

    # 1. PSD via periodogram (single FFT)
    X = np.fft.fft(signal, n=512)
    psd = np.abs(X[:256])**2 / (512 * FS)
    psd_db = 10 * np.log10(psd + 1e-30)
    feats.extend([np.mean(psd_db), np.std(psd_db), np.max(psd_db),
                  np.percentile(psd_db, 95), np.percentile(psd_db, 5)])

    # 2. Subband energy ratios (divide spectrum into 8 bands)
    n_bands = 8
    band_edges = np.linspace(0, len(psd), n_bands+1).astype(int)
    energies = []
    for i in range(n_bands):
        e = np.sum(psd[band_edges[i]:band_edges[i+1]]) + 1e-30
        energies.append(e)
    total_e = np.sum(energies)
    ratios = [e / total_e for e in energies]
    feats.extend(ratios)
    feats.append(np.std(ratios))  # spectral flatness indicator
    # Peak-to-average ratio (sensitive to narrowband signals)
    feats.append(np.max(psd_db) - np.mean(psd_db))

    # 3. Higher-order statistics (time domain)
    sig_real = np.real(signal)
    sig_imag = np.imag(signal)
    for s in [sig_real, sig_imag]:
        feats.extend([np.mean(s), np.std(s), skew(s), kurtosis(s),
                      np.max(np.abs(s))])

    # 4. Simple autocorrelation at selected lags (used FFT for speed)
    x = sig_real - np.mean(sig_real)
    n_x = len(x)
    # FFT-based autocorrelation
    n_fft = 1 << (n_x - 1).bit_length()  # next power of 2
    Xf = np.fft.rfft(x, n=n_fft)
    ac_fft = np.fft.irfft(Xf * np.conj(Xf), n=n_fft)[:n_x]
    denom = ac_fft[0] + 1e-30
    ac_lags = [0, 1, 2, 5, 10, 20, 50, 100]
    vals = [ac_fft[lag] / denom for lag in ac_lags if lag < n_x]
    feats.extend(vals[:5])
    feats.append(np.max(np.abs(vals)))

    # 5. Spectrogram (fewer windows, faster)
    nperseg = 256
    noverlap = 128
    nhop = nperseg - noverlap
    nw = max(1, (n - nperseg) // nhop + 1)
    Sxx = np.zeros((nperseg//2+1, min(20, nw)))
    window = np.hanning(nperseg)
    for i in range(min(20, nw)):
        seg = signal[i*nhop:i*nhop+nperseg]
        if len(seg) < nperseg:
            seg = np.pad(seg, (0, nperseg - len(seg)))
        # Use magnitude of complex spectrum
        sp = np.fft.fft(seg * window.astype(complex))
        Sxx[:, i] = np.abs(sp[:nperseg//2+1]) ** 2
    Sxx_db = 10 * np.log10(Sxx + 1e-30)
    feats.extend([np.mean(Sxx_db), np.std(Sxx_db), np.max(Sxx_db),
                  np.mean(np.std(Sxx_db, axis=1))])

    # 6. Edge/transient energy (downsampled envelope)
    envelope = np.abs(signal[::10])
    smooth = np.convolve(envelope, np.ones(10)/10, mode='same')
    edges = np.diff(smooth)
    feats.extend([np.max(np.abs(edges)), np.mean(np.abs(edges)),
                  np.std(edges)])

    # 7. Crest factor and signal envelope statistics
    sig_abs = np.abs(signal)
    feats.append(np.max(sig_abs) / (np.mean(sig_abs) + 1e-30))
    feats.append(np.percentile(sig_abs, 99) - np.percentile(sig_abs, 50))
    # Phase variation (differential phase std)
    phase = np.angle(signal)
    diff_phase = np.diff(np.unwrap(phase))
    feats.append(np.std(diff_phase))

    return np.array(feats)

def extract_feature_names():
    return (['psd_mean', 'psd_std', 'psd_max', 'psd_p95', 'psd_p5'] +
            [f'band_{i}' for i in range(8)] + ['band_std', 'psd_par'] +
            ['re_mean', 're_std', 're_skew', 're_kurt', 're_maxabs'] +
            ['im_mean', 'im_std', 'im_skew', 'im_kurt', 'im_maxabs'] +
            ['ac_0', 'ac_1', 'ac_2', 'ac_5', 'ac_10', 'ac_max'] +
            ['sg_mean', 'sg_std', 'sg_max', 'sg_fvar'] +
            ['edge_max', 'edge_mean', 'edge_std'] +
            ['crest', 'env_range', 'phase_jitter'])

# ====================================================================
#  ANOMALY DETECTION MODELS
# ====================================================================

class EnergyDetector:
    """Baseline: threshold on total received power."""
    def __init__(self, threshold=None):
        self.threshold = threshold
        self.name = 'Energy'

    def fit(self, X_train):
        # Compute power feature distribution
        powers = X_train[:, 0]  # psd_mean
        self.threshold = np.percentile(powers, 95)
        return self

    def predict(self, X_test):
        powers = X_test[:, 0]
        scores = powers - self.threshold
        return scores  # positive = anomaly

    def predict_binary(self, X_test):
        return (self.predict(X_test) > 0).astype(int)


class AutoencoderDetector:
    """Simple autoencoder reconstructs features; anomaly = reconstruction error."""
    def __init__(self, hidden_dim=8):
        self.hidden_dim = hidden_dim
        self.name = 'Autoencoder'
        self.W1 = self.W2 = self.b1 = self.b2 = None

    def fit(self, X_train):
        # Simple 2-layer autoencoder via SVD (PCA-like)
        X_centered = X_train - np.mean(X_train, axis=0)
        U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
        n_feat = X_train.shape[1]
        # Encoder: project to top-k components
        k = min(self.hidden_dim, n_feat)
        self.W1 = Vt[:k, :].T          # n_feat x k
        self.W2 = Vt[:k, :]             # k x n_feat
        self.mean = np.mean(X_train, axis=0)
        return self

    def predict(self, X_test):
        Xc = X_test - self.mean
        latent = Xc @ self.W1
        recon = latent @ self.W2 + self.mean
        errors = np.mean((X_test - recon)**2, axis=1)
        return errors  # higher = more anomalous

    def predict_binary(self, X_test):
        scores = self.predict(X_test)
        thresh = np.percentile(scores, 90)
        return (scores > thresh).astype(int)


class OCSVMDetector:
    """One-Class SVM on feature space."""
    def __init__(self, nu=0.05):
        self.nu = nu
        self.name = 'OC-SVM'
        self.model = OneClassSVM(nu=nu, kernel='rbf', gamma='scale')

    def fit(self, X_train):
        self.model.fit(X_train)
        return self

    def predict(self, X_test):
        # Negative decision_function = anomaly
        return -self.model.score_samples(X_test)

    def predict_binary(self, X_test):
        return (self.model.predict(X_test) == -1).astype(int)


class IForestDetector:
    """Isolation Forest for anomaly detection."""
    def __init__(self, contamination=0.05):
        self.contamination = contamination
        self.name = 'IForest'
        self.model = IsolationForest(contamination=contamination,
                                     random_state=SEED)

    def fit(self, X_train):
        self.model.fit(X_train)
        return self

    def predict(self, X_test):
        return -self.model.score_samples(X_test)

    def predict_binary(self, X_test):
        return (self.model.predict(X_test) == -1).astype(int)


class CyclostationaryDetector:
    """Detects covert signals via cyclostationary peaks (alpha-domain)."""
    def __init__(self, threshold=None):
        self.threshold = threshold
        self.name = 'Cyclostationary'

    def _cyclic_profile(self, signal):
        """Compute simplified cyclic autocorrelation peak."""
        n = len(signal)
        x = np.real(signal)
        # Multiple cycle frequencies
        alphas = np.linspace(0.01, 0.5, 20)
        peaks = []
        for a in alphas:
            shifted = x * np.exp(-1j * 2 * np.pi * a * np.arange(n))
            ac = np.abs(np.mean(shifted))
            peaks.append(ac)
        return np.max(peaks)

    def fit(self, X_train, signals_train=None):
        if signals_train is not None:
            profiles = [self._cyclic_profile(s) for s in signals_train]
            self.threshold = np.percentile(profiles, 95)
        else:
            self.threshold = 0.01
        return self

    def predict(self, X_test, signals_test=None):
        if signals_test is not None:
            return np.array([self._cyclic_profile(s) - self.threshold
                           for s in signals_test])
        # Fallback: use last 3 features (AC stats)
        ac_feats = X_test[:, -7:-4]  # ac_max, ac_mean, ac_std
        scores = np.mean(ac_feats, axis=1) * 10
        return scores

    def predict_binary(self, X_test, signals_test=None):
        return (self.predict(X_test, signals_test) > 0).astype(int)


# ====================================================================
#  DISTRIBUTED FUSION
# ====================================================================

class DistributedFusion:
    """Fuses decisions from multiple distributed sensors."""
    def __init__(self, n_sensors=N_SENSORS, fusion_rule='soft'):
        self.n = n_sensors
        self.rule = fusion_rule  # 'soft', 'hard_and', 'hard_or', 'hard_k'

    def fuse(self, local_scores):
        """Fuse local anomaly scores into global decision.

        local_scores: (n_sensors, n_samples) array
        Returns: global_score per sample
        """
        if self.rule == 'soft':
            return np.mean(local_scores, axis=0)
        elif self.rule == 'hard_and':
            decisions = (local_scores > 0).astype(int)
            return np.all(decisions, axis=0).astype(float)
        elif self.rule == 'hard_or':
            decisions = (local_scores > 0).astype(int)
            return np.any(decisions, axis=0).astype(float)
        elif self.rule.startswith('hard_k'):
            k = int(self.rule.split('_k')[1])
            decisions = (local_scores > 0).astype(int)
            return (np.sum(decisions, axis=0) >= k).astype(float)
        return np.mean(local_scores, axis=0)

# ====================================================================
#  SIMULATION
# ====================================================================

def _make_detector(method):
    if method == 'Energy': return EnergyDetector()
    if method == 'Autoencoder': return AutoencoderDetector(hidden_dim=8)
    if method == 'OC-SVM': return OCSVMDetector(nu=0.05)
    if method == 'IForest': return IForestDetector(contamination=0.05)
    if method == 'Cyclostationary': return CyclostationaryDetector()
    raise ValueError(f"Unknown method: {method}")

def _evaluate_roc(scores, y_true):
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, th = roc_curve(y_true, scores)
    roc_auc = auc(fpr, tpr)
    dist = np.sqrt((1 - tpr)**2 + fpr**2)
    bi = np.argmin(dist)
    return {'auc': roc_auc, 'best_pd': tpr[bi], 'best_pfa': fpr[bi],
            'fpr': fpr.tolist(), 'tpr': tpr.tolist(), 'thresholds': th.tolist()}

def run_all_methods(env, n_train=250, n_test_normal=250, n_test_covert=200,
                     covert_power_db=-85, n_sensors=N_SENSORS):
    """Generate data once per sensor, run all methods, return dict of results."""
    n_test = n_test_normal + n_test_covert

    # Generate training data (from sensor 0 only)
    X_train = np.array([extract_features(env.generate_observation(covert_power_db, False)[0])
                        for _ in range(n_train)])

    # Generate test data for all sensors independently (shared noise floor)
    sensor_data = []
    for si in range(n_sensors):
        nf_offset_db = 0.0  # identical noise floor; diversity from independent noise realizations
        cp = covert_power_db + nf_offset_db
        feats, labels = [], []
        for _ in range(n_test):
            is_covert = len(feats) >= n_test_normal
            sig, lab = env.generate_observation(cp, is_covert)
            feats.append(extract_features(sig))
            labels.append(lab)
        sensor_data.append((np.array(feats), np.array(labels)))

    X_test_ref, y_test = sensor_data[0]

    # Train all detectors on the same training data
    detectors = {m: _make_detector(m).fit(X_train) for m in METHODS}

    # Evaluate each method
    results = {}
    for method in METHODS:
        det = detectors[method]
        local_scores = np.array([det.predict(feats) for feats, _ in sensor_data])
        fusion = DistributedFusion(n_sensors, 'soft')
        global_scores = fusion.fuse(local_scores)
        res = _evaluate_roc(global_scores, y_test)
        res.update({'method': method, 'n_sensors': n_sensors,
                     'covert_power_db': covert_power_db})
        results[method] = res
    return results

def monte_carlo_evaluation(n_trials=20, **kwargs):
    """Run multiple trials and aggregate."""
    results = {m: {'aucs': [], 'pds': [], 'pfas': []} for m in METHODS}
    for t in range(n_trials):
        env = SpectrumEnvironment(seed=SEED + t * 1000)
        trial_results = run_all_methods(env, **kwargs)
        for method in METHODS:
            results[method]['aucs'].append(trial_results[method]['auc'])
            results[method]['pds'].append(trial_results[method]['best_pd'])
            results[method]['pfas'].append(trial_results[method]['best_pfa'])
        print(f"  Trial {t+1}/{n_trials}")
    return results

def snr_sweep(covert_powers=None, **kwargs):
    """Sweep covert signal power and evaluate detection performance."""
    if covert_powers is None:
        covert_powers = np.arange(-130, -100, 3)
    sweep = {m: {'powers': [], 'aucs': [], 'pds': []} for m in METHODS}

    for cp in covert_powers:
        env = SpectrumEnvironment(seed=SEED)
        trial_results = run_all_methods(env, covert_power_db=cp, **kwargs)
        for method in METHODS:
            sweep[method]['powers'].append(cp)
            sweep[method]['aucs'].append(trial_results[method]['auc'])
            sweep[method]['pds'].append(trial_results[method]['best_pd'])
        print(f"  Power {cp:.0f} dBm")
    return sweep

# ====================================================================
#  PLOTS
# ====================================================================

def plot_roc_curves(results, title='ROC Curves'):
    """Plot ROC curves for all methods."""
    fig, ax = plt.subplots(figsize=(7, 6))
    colors = {'Energy': 'gray', 'Autoencoder': 'steelblue',
              'OC-SVM': 'coral', 'IForest': 'seagreen',
              'Cyclostationary': 'purple'}
    markers = {'Energy': 'o', 'Autoencoder': 's',
               'OC-SVM': '^', 'IForest': 'D', 'Cyclostationary': 'v'}

    for method in METHODS:
        if method in results and 'fpr' in results[method]:
            fpr = np.array(results[method]['fpr'])
            tpr = np.array(results[method]['tpr'])
            auc_val = results[method]['auc']
            ax.plot(fpr, tpr, color=colors.get(method, 'blue'),
                    marker=markers.get(method, 'o'),
                    markevery=max(1, len(fpr)//8),
                    label=f'{method} (AUC={auc_val:.3f})', alpha=0.8)

    ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, label='Random')
    ax.set_xlabel('False Positive Rate (Pfa)')
    ax.set_ylabel('True Positive Rate (Pd)')
    ax.set_title(title)
    ax.legend(fontsize=8, loc='lower right')
    ax.grid(alpha=0.2); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_roc_curves.pdf'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_roc_curves.png'), dpi=150)
    plt.close()
    print("  [ROC] saved.")

def plot_auc_comparison(mc_results):
    """Bar chart comparing AUC across methods."""
    fig, ax = plt.subplots(figsize=(8, 5))
    methods = []
    means = []; stds = []
    for m in METHODS:
        if m in mc_results:
            methods.append(m)
            means.append(np.mean(mc_results[m]['aucs']))
            stds.append(np.std(mc_results[m]['aucs']))

    colors = ['gray', 'steelblue', 'coral', 'seagreen', 'purple'][:len(methods)]
    ax.bar(methods, means, yerr=stds, color=colors, alpha=0.8, capsize=5,
           edgecolor='k', linewidth=0.5)
    ax.set_ylabel('AUC')
    ax.set_title('Detection Performance Comparison (20 MC Trials)')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_auc_comparison.pdf'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_auc_comparison.png'), dpi=150)
    plt.close()
    print("  [AUC] saved.")

def plot_snr_sweep(sweep):
    """Plot detection performance vs covert signal power."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    colors = {'Energy': 'gray', 'Autoencoder': 'steelblue',
              'OC-SVM': 'coral', 'IForest': 'seagreen',
              'Cyclostationary': 'purple'}

    for metric, ax, ylabel in [('aucs', axes[0], 'AUC'),
                                ('pds', axes[1], 'Pd (best Pfa)')]:
        for method in METHODS:
            if method in sweep:
                p = sweep[method]['powers']
                v = sweep[method][metric]
                ax.plot(p, v, 'o-', color=colors.get(method, 'blue'),
                        label=method, alpha=0.8, markersize=5)
        ax.set_xlabel('Covert Signal Power (dBm)')
        ax.set_ylabel(ylabel)
        ax.set_title(f'{ylabel} vs Covert Power')
        ax.legend(fontsize=7); ax.grid(alpha=0.3)
        ax.axvline(-100, color='red', ls='--', alpha=0.3, label='Noise floor')
        ax.axhline(0.9, color='green', ls=':', alpha=0.3, label='Pd=0.9')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_snr_sweep.pdf'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_snr_sweep.png'), dpi=150)
    plt.close()
    print("  [SNR sweep] saved.")

def plot_sensor_scalability():
    """Evaluate AUC vs number of sensors."""
    n_list = [1, 2, 4, 8]
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {'Energy': 'gray', 'Autoencoder': 'steelblue',
              'OC-SVM': 'coral', 'IForest': 'seagreen',
              'Cyclostationary': 'purple'}

    env_base = SpectrumEnvironment(seed=SEED)
    for method in METHODS:
        aucs = []
        for n in n_list:
            n_save = N_SENSORS
            res = run_all_methods(env_base, n_train=80, n_test_normal=80,
                                   n_test_covert=60, covert_power_db=-85,
                                   n_sensors=n)
            aucs.append(res[method]['auc'])
        ax.plot(n_list, aucs, 'o-', color=colors.get(method, 'blue'),
                label=method, alpha=0.8)
        print(f"  Scalability: {method} done")

    ax.set_xlabel('Number of Sensors')
    ax.set_ylabel('AUC')
    ax.set_title('Detection Scalability with Distributed Sensors')
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    ax.set_xticks(n_list)
    ax.set_xticklabels(n_list)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_sensor_scalability.pdf'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_sensor_scalability.png'), dpi=150)
    plt.close()
    print("  [scalability] saved.")

def plot_feature_importance(X_train, y_train):
    """Rank features by ANOVA F-score."""
    from sklearn.feature_selection import f_classif
    names = extract_feature_names()
    nf = len(names)
    # Create pseudo-labels: last half are anomalies
    pseudo_y = np.zeros(len(X_train))
    pseudo_y[len(X_train)//2:] = 1
    f_scores, p_vals = f_classif(X_train[:len(pseudo_y)], pseudo_y)
    top_idx = np.argsort(f_scores)[::-1][:10]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(range(10), f_scores[top_idx], color='steelblue', alpha=0.8)
    ax.set_yticks(range(10))
    ax.set_yticklabels([names[i] for i in top_idx])
    ax.set_xlabel('ANOVA F-Score')
    ax.set_title('Top-10 Discriminative Features')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_feature_importance.pdf'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_feature_importance.png'), dpi=150)
    plt.close()
    print("  [features] saved.")
    return top_idx

# ====================================================================
#  MAIN
# ====================================================================
def main():
    print("="*65)
    print("  Covert Activity Detection via Anomaly Analysis")
    print("  in Distributed Spectral Signal Processing")
    print("="*65)

    print(f"\n  Sensors: {N_SENSORS}, FFT bins: {N_FREQ_BINS}")
    print(f"  Features: {len(extract_feature_names())}")
    print(f"  Methods: {', '.join(METHODS)}")

    # Feature analysis
    print("\n[Feature Analysis]")
    env = SpectrumEnvironment(seed=SEED)
    X, y, _, _ = env.generate_dataset(100, 100, -85)
    plot_feature_importance(X, y)

    # Single-trial ROC
    print("\n[Single Trial ROC]")
    env = SpectrumEnvironment(seed=SEED)
    trial_results = run_all_methods(env, n_train=250, n_test_normal=250,
                                     n_test_covert=200, covert_power_db=-85)
    for method in METHODS:
        r = trial_results[method]
        print(f"  {method:<15} AUC={r['auc']:.4f}  "
              f"Pd={r['best_pd']:.3f}  Pfa={r['best_pfa']:.3f}")
    plot_roc_curves(trial_results, 'ROC Curves (Covert Power = -85 dBm)')

    # Monte Carlo
    print("\n[Monte Carlo]")
    mc = monte_carlo_evaluation(n_trials=20, n_train=100, n_test_normal=100,
                                 n_test_covert=80, covert_power_db=-85)
    plot_auc_comparison(mc)

    # SNR sweep
    print("\n[SNR Sweep]")
    sweep = snr_sweep(covert_powers=np.arange(-120, -75, 5),
                      n_train=100, n_test_normal=100, n_test_covert=80)
    plot_snr_sweep(sweep)

    # Scalability
    print("\n[Scalability]")
    plot_sensor_scalability()

    # Summary
    print(f"\n{'='*65}")
    print("  RESULTS SUMMARY")
    print(f"{'='*65}")
    print(f"  {'Method':<18} {'AUC Mean':<10} {'AUC Std':<10} {'Pd@best':<10} {'Pfa@best':<10}")
    print("  " + "-"*58)
    for m in METHODS:
        if m in mc:
            mu = np.mean(mc[m]['aucs']); sd = np.std(mc[m]['aucs'])
            pd = np.mean(mc[m]['pds']); pf = np.mean(mc[m]['pfas'])
            print(f"  {m:<18} {mu:<10.4f} {sd:<10.4f} {pd:<10.3f} {pf:<10.4f}")

    # Save all results
    all_data = {'mc': {m: {'aucs': mc[m]['aucs'], 'pds': mc[m]['pds'],
                           'pfas': mc[m]['pfas']} for m in METHODS},
                'sweep': sweep}
    json.dump(all_data, open(os.path.join(OUTPUT_DIR, 'metrics.json'), 'w'),
              indent=2, cls=Encoder)
    print(f"\n  Figures saved to {OUTPUT_DIR}/")
    print("  Done.")

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super().default(obj)

if __name__ == '__main__':
    main()
