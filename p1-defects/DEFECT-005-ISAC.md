# P1 Defect Report 005 — ISAC, range-Doppler joint sensing and communication

**Date:** 2026-09-30
**Package:** `FernandoMay/isac-jasc-ieee`
**Corpus:** P1 research-hardening sweep. **Separate from the E1 dataset**, frozen at v1.0.
**Status:** Frozen. No number corrected, no file modified, no figure regenerated, no claim rewritten, no repair started.
**Method:** claim → artifact → input → transformation → metric → published number, with the circularity question asked explicitly rather than assumed.

---

## 1. Reproduction passes, and it is the most faithful in the sweep

`isac_simulator.py` run to completion in a clean venv: **exit 0, `isac_experiment_results.csv` byte-identical, 2550 rows.**

Four earlier attempts failed on environment issues rather than package issues: a missing temp directory after macOS rotated `/var/folders`, a full disk (1.2 GiB free on a 100%-used volume), and missing `numpy`, `pandas` and `jinja2`. Two comparisons reported "identical" while the simulator had never run and the CSV had not been regenerated. **Both were void and neither was treated as a match.** This is the fourth time in this sweep that a failed run nearly produced a false reproduction claim, which is itself an argument for the standing rule that a failed run is a result.

The successful run's own summary table, which the paper's headline claim is measured against:

| SNR dB | sensing PE | comm. BER | SE [bps/Hz] | crlb_R [m] | crlb_v [m/s] |
|---|---|---|---|---|---|
| −15 | 0.1190 | 3.511e−01 | 0.02 | 5.9645 | 4.0132 |
| 0 | 0.0115 | 2.397e−01 | 0.56 | 1.0607 | 218.4964 |
| +15 | 0.0031 | 4.340e−03 | 2.65 | 0.1886 | 0.3333 |

## 2. Finding — the validation is circular by construction

`isac_simulator.py:147-148`:

```python
R_est = R_true + np.random.randn() * crlb_range(params, snr_meas)
v_est = v_true + np.random.randn() * crlb_velocity(params, snr_meas)
```

The "estimator" is the true value plus Gaussian noise whose **standard deviation is the Cramér-Rao bound it is being compared against.** There is no estimator. No likelihood is evaluated, no Fisher information is formed from data, no observation is inverted. The bound generates the observation that is then checked against the bound.

The question this audit was opened to ask — *can the independent evidence falsify the result, or is the instrument built from the same quantity it claims to validate?* — resolves in the second direction.

Consequence: the CRLB comparison in this package is **not evidence of anything.** The agreement between simulated accuracy and the bound is arithmetic, not physics. No improvement to the sensing model, and no replacement of the CRLB derivation, could change the outcome, because the outcome is an input.

This also explains the otherwise notable property of this package: its artifact is the most bit-faithful in the sweep while carrying the most consequential defect. Faithful reproduction of a circular construction reproduces the circularity exactly.

## 3. Finding — the paper's headline quantitative claim is not supported

`main.tex:70`, abstract:

> "ISAC achieves reliable sensing accuracy (prediction error < 0.05) and communication throughput (**spectral efficiency > 4 bps/Hz**) at SNR above −5 dB"

The regenerated sweep reaches a maximum spectral efficiency of **2.65 bps/Hz**, at +15 dB. No SNR in the artifact produces a value above 4. The claim is false against the repository's own committed data.

## 4. Finding — the README table contradicts the artifact in all nine cells

`README.md:44-48` against the regenerated CSV:

| metric | README −15 | artifact | README 0 | artifact | README +15 | artifact |
|---|---|---|---|---|---|---|
| sensing PE | 0.350 | **0.1190** | 0.045 | **0.0115** | 0.008 | **0.0031** |
| comm. BER | 0.45 | **3.511e−01** | 0.008 | **2.397e−01** | 3e−4 | **4.340e−03** |
| SE [bps/Hz] | 0.80 | **0.02** | 3.50 | **0.56** | 5.50 | **2.65** |

Every cell differs, by factors from 1.6× to 40×. The direction is consistent — the README reports higher PE, lower BER and higher SE than the artifact produces.

## 5. Finding — the "inverse Fisher matrix" derivation is never performed

`main.tex:188` states the CRLB "are the diagonal elements of the inverse Fisher matrix", and the paper presents a joint parameter vector `θ = [R, v]ᵀ`.

The simulator contains **no matrix construction, no `linalg`, no `inv`, no `pinv`, and no occurrence of the string "Fisher"** — a count of zero for all five. What the code implements is the pair of closed-form scalar expressions the paper prints as equation (8):

```python
def crlb_range(params, snr_lin):   return C / (2 * params.B * np.sqrt(2 * snr_lin))
def crlb_velocity(params, snr_lin): return C / (2 * params.fc * T_frame * np.sqrt(2 * snr_lin))
```

with `C = 3e8`. The formulas match the paper's equation; the derivation the paper names as their source is not performed anywhere in the repository. Whether those closed forms are in fact the diagonal of the inverse Fisher matrix for this signal model is **not demonstrated here and not asserted against** — only that the derivation is absent and the derivation's result is what is used.

## 6. Finding — the bound is a variance and is consumed as a standard deviation

`main.tex:189` writes the bounds as `σ_R² ≥ c / (2B√(2·SNR))` and `σ_v² ≥ c / (2 f_c T_frame √(2·SNR))` — variances.

`crlb_range` and `crlb_velocity` return those expressions unchanged, and line 147 uses the return value directly as the multiplier of `np.random.randn()`, which has unit variance. The quantity therefore acts as a standard deviation in the code and as a variance in the paper.

**This defect is invisible in the results, and finding 2 is why.** Against a real estimator, feeding σ² where σ belongs would surface as an estimator appearing to beat the Cramér-Rao bound, which is impossible for an unbiased one and would have been caught. Because the errors are drawn from the bound rather than estimated, the confusion is self-consistent and produces no visible anomaly. The circularity conceals the units error.

That is worth recording as a general point: a validation that cannot fail also cannot report the failures it would otherwise expose.

## 7. Finding — Figure 5 is not computed from the simulation

`isac_simulator.py:310-320`, the figure titled **"Range-Doppler Map (OFDM-ISAC)"**:

```python
rd = np.random.randn(50, 50)
rd[25, 15] = 100
im = ax.imshow(rd, aspect='auto', cmap='viridis', extent=[-30, 30, 0, 500])
ax.set_xlabel('Velocity [m/s]')
ax.set_ylabel('Range [m]')
ax.set_title('Range-Doppler Map (OFDM-ISAC)')
```

The map is a 50×50 array of standard Gaussian noise with a single element overwritten to 100, presented on physical axes with a "Power [dB]" colorbar. It is not derived from the OFDM model, from any waveform, or from any simulation result. It is the shape an ideal range-Doppler resolution cell would have, drawn directly.

The figure is the package's principal visual evidence of sensing capability and it is hand-drawn noise. The axis extents are cosmetic: nothing maps array index to velocity or range.

## 8. Classification

Reproduces: **yes, exactly.** Numbers real: **yes.** Artifact traceable: **yes, faithfully.** Circularity: **yes, by construction.** Derivation performed: **no.** Units consistent: **no.** Principal figure computed: **no.**

| # | defect | location |
|---|---|---|
| 1 | Estimation error drawn from the bound it validates | `isac_simulator.py:147-148` |
| 2 | Headline SE > 4 bps/Hz unsupported; artifact max 2.65 | `main.tex:70` |
| 3 | All nine README cells contradict the artifact | `README.md:44-48` |
| 4 | Inverse Fisher matrix derivation absent; closed forms used instead | `main.tex:188` vs simulator |
| 5 | Variance consumed as standard deviation | `lib` lines 85-93 used at 147-148 |
| 6 | Range-Doppler figure is noise with one imposed pixel | `isac_simulator.py:310-320` |

This is a **sixth profile**, and the most severe in the sweep: the CRLB comparison — the package's named contribution, contribution 3 of the paper — cannot in principle fail, and the figure offered as its visual evidence contains no simulation output.

## 9. Not verified

- Whether Figures 1 through 4 regenerate byte-identically. Not checked; the run completed and produced them, but no byte comparison was performed.
- The provenance of the README table. The repository records nothing identifying what produced those nine values, and no earlier commit, configuration or manual run is asserted as the source.
- Whether the paper's agricultural and GreenRemit scenarios map to distinct simulation configurations. The run produces a `sinr_db` column and a `type` column; the correspondence between the named application scenarios and specific parameter sets was not traced.
- The Chinese-language materials and `presentation.pdf` were not read.
