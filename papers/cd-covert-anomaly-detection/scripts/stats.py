#!/usr/bin/env python3
"""Derive every table number in the manuscript from the committed artifact.

Reads ONLY `data/metrics.json` (byte-identical to `figures/metrics.json` in
FernandoMay/cd-ieee-package, sha256 4242d117...) and writes `data/stats.json`.
No simulation is run here. The manuscript's tables and inline numbers are
transcribed from `data/stats.json`, so each one is traceable to a committed
file without re-running anything.

Run:  python scripts/stats.py
"""

import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

T_CRIT_DF19 = 2.093024054  # two-sided 95% Student-t quantile, df = 19


def main():
    with open(os.path.join(DATA, "metrics.json")) as fh:
        raw = json.load(fh)
    mc, sweep = raw["mc"], raw["sweep"]

    out = {
        "source": "data/metrics.json (upstream figures/metrics.json, verbatim)",
        "monte_carlo": {},
        "sweep": {},
        "derived": {},
    }

    # ---- Monte Carlo table: mean, population std (upstream convention), CIs ----
    for m, v in mc.items():
        a = np.asarray(v["aucs"], dtype=float)
        n = len(a)
        sd_pop = float(np.std(a))           # ddof=0, what upstream prints
        sd_samp = float(np.std(a, ddof=1))  # ddof=1, sample std
        se = sd_samp / math.sqrt(n)
        out["monte_carlo"][m] = {
            "n_trials": n,
            "mean_auc": float(a.mean()),
            "std_auc_ddof0": sd_pop,
            "std_auc_ddof1": sd_samp,
            "min_auc": float(a.min()),
            "max_auc": float(a.max()),
            "mean_pd": float(np.mean(v["pds"])),
            "mean_pfa": float(np.mean(v["pfas"])),
            "ci95_low": float(a.mean() - T_CRIT_DF19 * se),
            "ci95_high": float(a.mean() + T_CRIT_DF19 * se),
            "n_trials_at_ceiling": int((a >= 0.9999).sum()),
        }

    # ---- Paired per-seed differences between the strong detectors ----
    ref = "IForest"
    for other in ("OC-SVM", "Energy", "Autoencoder"):
        d = np.asarray(mc[ref]["aucs"]) - np.asarray(mc[other]["aucs"])
        out["derived"][f"paired_{ref}_minus_{other}"] = {
            "per_trial": [float(x) for x in d],
            "mean_diff": float(d.mean()),
            "std_diff_ddof1": float(np.std(d, ddof=1)),
            "n_tied_exactly_zero": int((d == 0.0).sum()),
        }

    # ---- Power sweep: one realisation per point ----
    for m, v in sweep.items():
        p = np.asarray(v["powers"], dtype=float)
        a = np.asarray(v["aucs"], dtype=float)
        g95 = p[a >= 0.95]
        g99 = p[a >= 0.99]
        out["sweep"][m] = {
            "powers": [float(x) for x in p],
            "aucs": [float(x) for x in a],
            "pds": [float(x) for x in v["pds"]],
            "max_auc": float(a.max()),
            "argmax_power": float(p[int(np.argmax(a))]),
            "first_power_auc_ge_0p90": float(p[a >= 0.90][0]) if (a >= 0.90).any() else None,
            "first_power_auc_ge_0p95": float(g95[0]) if len(g95) else None,
            "first_power_auc_ge_0p99": float(g99[0]) if len(g99) else None,
            "ever_reaches_0p99": bool((a >= 0.99).any()),
        }

    # ---- Transition width: chance -> AUC >= 0.99 ----
    widths = {}
    for m, v in out["sweep"].items():
        p = np.asarray(v["powers"], dtype=float)
        a = np.asarray(v["aucs"], dtype=float)
        chance = p[int(np.argmax(a >= 0.5))]
        widths[m] = {
            "chance_from_dBm": float(chance),
            "transition_width_dB": (float(v["first_power_auc_ge_0p99"]) - float(chance))
                                  if v["first_power_auc_ge_0p99"] is not None else None,
        }
    out["derived"]["transition_width"] = widths

    # ---- Head-to-head vs the Energy baseline across the sweep ----
    h2h = {}
    p_ref = out["sweep"]["Energy"]["powers"]
    for m in ("Autoencoder", "OC-SVM", "IForest", "Cyclostationary"):
        a_ref = np.asarray(out["sweep"]["Energy"]["aucs"], dtype=float)
        a_m = np.asarray(out["sweep"][m]["aucs"], dtype=float)
        p_m = np.asarray(out["sweep"][m]["powers"], dtype=float)
        # x = the candidate method, y = the Energy baseline.
        # "Below Energy" means the candidate's AUC is strictly smaller.
        worse = [float(p) for p, x, y in zip(p_m, a_m, a_ref) if x < y]
        h2h[m] = {
            "n_powers_where_below_Energy": len(worse),
            "n_powers_total": len(p_m),
            "powers_below_Energy": worse,
            "max_auc_advantage": float(np.max(a_m - a_ref)),
            "min_auc_advantage": float(np.min(a_m - a_ref)),
        }
    out["derived"]["head_to_head_vs_Energy"] = h2h

    # ---- Signal-model arithmetic used in the System Model section ----
    fs, noise_floor_dbm_per_hz = 20e6, -100.0
    noise_total_dbm = 10.0 * math.log10(10 ** (noise_floor_dbm_per_hz / 10.0) * fs)
    out["derived"]["signal_model"] = {
        "fs_hz": fs,
        "noise_floor_dbm_per_hz": noise_floor_dbm_per_hz,
        "noise_total_dbm": noise_total_dbm,
        "snr_offset_dB": -noise_total_dbm,   # SNR_dB = P_c + offset
        "periodogram_fft_size": 512,
        "samples_used_for_psd": 512,
        "samples_per_observation": 20480,
        "fraction_of_observation_used_for_psd": 512.0 / 20480.0,
        "frequency_resolution_hz": fs / 512.0,
        "n_features_total": 41,
        "n_constant_features": 2,
        "constant_feature_names": ["ac_0", "ac_max"],
    }

    with open(os.path.join(DATA, "stats.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    # ---- console report, so the numbers can be eyeballed against the paper ----
    print("Monte Carlo (20 trials, -85 dBm, K=4), from data/metrics.json")
    hdr = f"  {'method':<15}{'mean':>8}{'sd(ddof0)':>11}{'sd(ddof1)':>11}{'min':>8}{'95% CI':>20}{'>=0.9999':>9}"
    print(hdr)
    for m, v in out["monte_carlo"].items():
        ci = f"[{v['ci95_low']:.4f}, {v['ci95_high']:.4f}]"
        print(f"  {m:<15}{v['mean_auc']:>8.4f}{v['std_auc_ddof0']:>11.4f}"
              f"{v['std_auc_ddof1']:>11.4f}{v['min_auc']:>8.4f}{ci:>20}"
              f"{v['n_trials_at_ceiling']:>9}")
    print("\nTransition width (chance performance -> AUC >= 0.99)")
    for m, v in widths.items():
        w = "never reaches 0.99" if v["transition_width_dB"] is None else f"{v['transition_width_dB']:.0f} dB"
        print(f"  {m:<15} chance from {v['chance_from_dBm']:>7.0f} dBm   width {w}")
    print("\nHead-to-head vs Energy across the 9 sweep powers")
    for m, v in h2h.items():
        print(f"  {m:<15} below Energy at {v['n_powers_where_below_Energy']}/{v['n_powers_total']} powers"
              f"  AUC advantage range [{v['min_auc_advantage']:+.4f}, {v['max_auc_advantage']:+.4f}]")
    print("\nPaired per-seed differences")
    for k, v in out["derived"].items():
        if k.startswith("paired_"):
            print(f"  {k:<34} mean {v['mean_diff']:+.5f}  sd {v['std_diff_ddof1']:.5f}"
                  f"  exact ties {v['n_tied_exactly_zero']}/20")
    print("\nSignal-model arithmetic")
    sm = out["derived"]["signal_model"]
    print(f"  noise total in {sm['fs_hz']/1e6:.0f} MHz = {sm['noise_total_dbm']:.2f} dBm"
          f"  ->  SNR_dB = P_c + {sm['snr_offset_dB']:.2f} dB")
    print(f"  periodogram uses {sm['samples_used_for_psd']}/{sm['samples_per_observation']} samples"
          f" ({100*sm['fraction_of_observation_used_for_psd']:.1f}%),"
          f" resolution {sm['frequency_resolution_hz']/1e3:.2f} kHz")
    print("\nwrote data/stats.json")


if __name__ == "__main__":
    main()
