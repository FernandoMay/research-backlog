# Batch 2 Research Package Audit

**Rubric:** ARTIFACT-TO-CLAIM-RUBRIC.md v1.0
**Scope:** 4 packages (ems, qce, quantum-k-sat, sra) from account FernandoMay
**Auditor:** batch2 sub-agent
**Date:** 2026-09-29
**Status:** COMPLETE

---

## Machine-readable summary

| package | repo | L1 | L2 | L3 total | L3 supported | L3 contradicted | L3 unsupported | L4 | L5 | L6 | L7 | L8 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ems | FernandoMay/ems-ieee-package | SUPPORTED | SUPPORTED | 18 | 12 | 3 | 3 | CONTRADICTED | CONTRADICTED | SUPPORTED | CONTRADICTED | PARTIALLY SUPPORTED |
| qce | FernandoMay/qce-ieee-package | SUPPORTED | SUPPORTED | 18 | 11 | 5 | 2 | CONTRADICTED | CONTRADICTED | CONTRADICTED | CONTRADICTED | PARTIALLY SUPPORTED |
| quantum-k-sat | FernandoMay/quantum-k-sat-ieee-package | SUPPORTED | SUPPORTED | 25 | 13 | 11 | 1 | SUPPORTED | CONTRADICTED | SUPPORTED | CONTRADICTED | PARTIALLY SUPPORTED |
| sra | FernandoMay/sra-ieee-package | SUPPORTED | SUPPORTED | 14 | 9 | 5 | 0 | CONTRADICTED | CONTRADICTED | CONTRADICTED | CONTRADICTED | PARTIALLY SUPPORTED |

Totals across the 4 audited packages: **L3 = 75 claims; 45 SUPPORTED (60.0%); 24 CONTRADICTED (32.0%); 6 UNSUPPORTED (8.0%).**

---

## Method and environment (R2, R3)

Every number in this report is either **MEASURED** (read from a committed artifact, or produced by a command recorded here with its output and exit code) or **CLAIMED** (stated in prose with no artifact). No estimated values.

Repository discovery: `gh api users/FernandoMay/repos` omits these repositories, as warned. All four were found by direct name probe and each returns HTTP 200 individually. Bare names `ems`, `qce`, `quantum-k-sat`, `sra` do **not** exist; the real names carry an `-ieee-package` suffix.

Environment used for all executions (recorded per R2/L2):

| item | value |
|---|---|
| OS | macOS 26.3.1 (build 26.3.1) |
| CPU | Apple M1 |
| Python | 3.14.3 (main, Feb 3 2026, 15:32:20) [Clang 17.0.0] |
| numpy | 2.5.3 |
| scipy | 1.18.1 |
| matplotlib | 3.11.2 |
| Pillow (auditor-added, for pixel diffing) | latest |
| C compiler | Apple clang (`/Applications/Xcode.app`) |
| venv location | disposable temp; report written to the durable path |

Clones are read-only working copies under the disposable temp path. `git status` was used after every run to determine which artifacts each simulator actually rewrites. **No audited repository was modified, committed, or pushed.** The only file the auditor wrote is this report.

### Execution log (exit codes, R3)

| command | exit | wall time | stdout artifact |
|---|---|---|---|
| `python ems_simulator.py` | **0** | 8.9 s | `figures/metrics.json` + 7 figures |
| `python sra_simulator.py` | **0** | 2.8 s | `figures/metrics.json` + 8 figures |
| `python qce_simulator.py` | **0** | 15.0 s | `figures/metrics.json` + 5 figures |
| `python simulator/quantum_k_sat_simulator.py` | **0** | 548.5 s | `data/metrics.json` + 4 figures |
| `clang -O2 ems_fdtd.c -lm` + run | **0** | — | prints benchmark table to stdout |
| `clang -O2 qce_kernel.c -lm` + run | **0** (1 warning) | — | prints results to stdout |
| `clang -O2 sra_kernel.c -lm` + run | **0** | — | prints results to stdout |

All four simulators completed with **exit code 0** and no errors. This is the single most important positive result in the batch: **nothing failed to run.**

### Reproduction fidelity (L2 evidence)

| package | `metrics.json` reproduced | detail |
|---|---|---|
| sra | **bit-identical** | all 45 rows, 5 fields, exact float equality |
| qce | **bit-identical** | all 4 policies, 8 fields, exact float equality |
| ems | 22 of 24 fields **bit-identical** | 2 fields differ at 1e-16 relative; 1 field differs in a mathematically-zero quantity — see L3 note |
| quantum-k-sat | **bit-identical except 4 values** | `depth.gap[]` differs by 1-2 ULP; all 98 other numbers exact |

The two non-exact cases were examined and are **not** treated as findings, per R7 and the rubric's own note that a committed JSON which does not reproduce is a finding *only when the difference is material*:

- **quantum-k-sat `depth.gap`**: committed `5.707474586657542` vs reproduced `5.707474586657543` (and 3 similar). Relative difference ~2e-16, from BLAS reduction order in `conj(state) @ (H*state)`. All `sat` values and the `noise`/`scaling`/`mitigation` sections are bit-identical. Reported as a reproduction note, not a discrepancy.
- **ems**: `AF_ev` for `diffuse` and `focus`, and `ev_power` for `diffuse`, differ at 1e-16 to 1e-14 relative. `AF_ev` for `beamsteer` differs materially in relative terms (committed `3.2047e-30`, reproduced `1.1093e-29`, factor 2.46) but is a quantity that is **mathematically zero** — see the L3 analysis, which uses this fact. Critically, **every quantity the paper reports** (`rx_power`, `ev_power`, `eir_dB`, `secrecy_capacity_bps_Hz`) reproduced **bit-identically** for all four patterns.

### Figure reproduction (L4 evidence)

Committed PNGs were compared to regenerated PNGs both by SHA-256 and by per-pixel RGB difference.

| package | figures | byte-identical | pixel-delta only | size changed |
|---|---|---|---|---|
| ems | 8 | 1 (`fig_signals`) | 7 | 0 |
| sra | 8 | 0 | 8 | 0 |
| qce | 5 | 0 | — | 5 (1-3 px, `bbox_inches='tight'`) |
| quantum-k-sat | 4 | 0 | 4 | 0 |

The 5-8% pixel deltas with `max_channel_delta=255` are matplotlib 3.11 font/antialiasing changes, not data changes: all ems and sra figures retain identical pixel dimensions, and the qce size shifts of 1-3 px are the expected effect of `bbox_inches='tight'` against different font metrics. **No figure's data changed.** This distinction was verified, not assumed — the quantum-k-sat figures were visually inspected and the plotted data matches the artifact exactly.

`ems/figures/fig_signals.png` is byte-identical after a full simulator re-run because **no committed code ever writes it** (see ems L4).

---

# 1. `ems` — RIS Phased-Array Channel Model for UWB Eavesdropping Immunity

**Repository:** `FernandoMay/ems-ieee-package` (HTTP 200; 29 tracked files; 3 commits, HEAD `481182e`)
**Claimed topic (backlog):** RIS array model with C kernel, secrecy metrics, Monte Carlo
**Evidence class:** E1, seeded simulation with `metrics.json` and figures

## Research question

Can controlled electromagnetic scattering via a Reconfigurable Intelligent Surface create a wireless channel that is inherently more immune to eavesdropping, in a non-line-of-sight (NLoS) indoor UWB setting? The paper models an 8x8 RIS as a phased array and compares four reflection configurations — transparent, beamsteering, diffuse, focus — using Eavesdropping Immunity Ratio (EIR) and secrecy capacity.

**Verdict on the question:** the simulation answers it, and the answer is reported faithfully. The *mechanism* the paper credits for the answer is not what the code does.

## What was executed, with real output

`ems_simulator.py`, full run, **exit code 0**, 8.9 s. Real stdout, benchmark section verbatim:

```
  Pattern: transparent
    RX power:      3.5268e-10      EV power: 5.1884e-10
    RX array fact: 0.0000          EV array fact: 0.0000
    EIR:           -1.68 dB        Secrecy cap.:  4.1290 bps/Hz
  Pattern: beamsteer
    RX power:      5.4989e-10      EV power: 5.1884e-10
    RX array fact: 140.8902        EV array fact: 0.0000
    EIR:           0.25 dB         Secrecy cap.:  5.2117 bps/Hz
  Pattern: diffuse
    RX power:      4.7202e-10      EV power: 6.2601e-10
    RX array fact: 85.2584         EV array fact: 84.8136
    EIR:           -1.23 dB        Secrecy cap.:  4.3866 bps/Hz
  Pattern: focus
    RX power:      4.0420e-10      EV power: 5.1884e-10
    RX array fact: 36.8057         EV array fact: 0.0062
    EIR:           -1.08 dB        Secrecy cap.:  4.4672 bps/Hz
```

Also executed: the C reference kernel (**exit 0**), plus three auditor-designed controlled experiments (beamsteering geometry, shadow-fading sigma, Monte Carlo distribution). Their output is quoted in the L3 section below.

## L3 — every numerical claim, both values, artifact path

**Artifact path for this entire package: `ems-ieee-package/figures/metrics.json`.**

### SUPPORTED (12)

| # | Claim (source) | Claimed | Artifact value | Verdict |
|---|---|---|---|---|
| 1 | EIR beamsteer (abstract, l.42) | `+0.25 dB` | `0.25242425284893943` | SUPPORTED |
| 2 | EIR transparent (abstract, l.42) | `-1.68 dB` | `-1.6765414772693035` | SUPPORTED |
| 3 | Secrecy capacity beamsteer (abstract) | `5.21 bps/Hz` | `5.211653080882533` | SUPPORTED |
| 4 | Table I, Transparent row (l.198) | `3.53e-10 / 5.19e-10 / -1.68 / 4.13` | `3.526768417763237e-10 / 5.188371806901686e-10 / -1.6765414772693035 / 4.128960029998177` | SUPPORTED |
| 5 | Table I, Beamsteer row (l.199) | `5.50e-10 / 5.19e-10 / +0.25 / 5.21` | `5.498870803857577e-10 / 5.188371806901686e-10 / 0.25242425284893943 / 5.211653080882533` | SUPPORTED |
| 6 | Table I, Diffuse row (l.200) | `4.72e-10 / 6.26e-10 / -1.23 / 4.39` | `4.720168842591015e-10 / 6.260125621675891e-10 / -1.2262551444334449 / 4.386626469875397` | SUPPORTED |
| 7 | Table I, Focus row (l.201) | `4.04e-10 / 5.19e-10 / -1.08 / 4.47` | `4.0419536367139474e-10 / 5.1884498297937e-10 / -1.0844629401189096 / 4.4671749308667845` | SUPPORTED |
| 8 | `AF_ev = 3.2e-30` for beamsteer (l.187) | `3.2e-30` | `3.20474742746036e-30` | SUPPORTED |
| 9 | `AF_ev = 0.006` for focus (l.187) | `0.006` | `0.006174366427651143` | SUPPORTED |
| 10 | "no realisations falling below -10 dB" (l.238) | `0 of 100` | **MEASURED by auditor: min = -3.9624 dB; 0/100 below -10 dB; 0/100 below -15 dB** | SUPPORTED |
| 11 | "Monte Carlo analysis over 100 realisations" | `N = 100` | `run_monte_carlo(..., ntrials=100)`; 100 trials executed | SUPPORTED |
| 12 | "Beamsteering is the only pattern with positive EIR" (caption l.212) | only beamsteer > 0 | `+0.25` only positive; others `-1.68 / -1.23 / -1.08` | SUPPORTED |

Claim 10 needs emphasis, and so does the caveat attached to it. The auditor's prior — seeing a symmetric log-normal model with a deterministic EIR of only +0.25 dB — was that "no realisation below -10 dB" would be a coin flip. **That prior was wrong**, and the measurement says so: the claim is true as reported. But the *reason* it is true is a defect. See discrepancy 2. Recording the corrected prediction is part of the result.

**The whole of Table I reproduces to 3 significant figures in all 16 cells.** That is the strongest artifact-to-claim correspondence in the batch.

### CONTRADICTED (3)

**D1 — the abstract claims >140 dB eavesdropper suppression; no dB figure in the artifact equals 140.**

- **Claimed** (`main.tex:42`, abstract): "reducing RIS-reflected power at the eavesdropper by **over 140 dB** relative to the receiver direction."
- **Actual, under every reading, none of which is 140:**
  - received-power advantage, i.e. the paper's own EIR definition: **+0.25 dB** (`eir_dB: 0.25242425284893943`)
  - array-factor ratio `10*log10(AF_rx/AF_ev)`: **316.4 dB** (and meaningless, since `AF_ev` is floating-point noise — see U1)
  - `10*log10(AF_rx)` alone = 21.5 dB
- **Root cause:** `140.89` is `AF_rx`, a **dimensionless linear array-factor value**. The abstract reads it as a decibel quantity.
- **Artifact path:** `ems-ieee-package/figures/metrics.json` → `AF_rx`, `AF_ev`, `eir_dB`.
- **Verdict: CONTRADICTED.** Claimed >140 dB; actual 0.25 dB (EIR) or 316.4 dB (AF ratio).

**D2 — the parameter table states shadow-fading sigma = 3.0 dB; the code delivers 1.5 dB.**

- **Claimed** (`main.tex:144`): "Shadow fading std $\sigma$ & $3.0$ dB". Repeated at `main.tex:157`.
- **Actual, MEASURED by the auditor over 2,000,000 draws:** the code computes `f = np.random.lognormal(0, SIGMA_SHADOW/8.686)`, i.e. `sigma_ln = 0.345383`, and the realised standard deviation of `10*log10(f)` is **1.4992 dB**. The divisor `8.686` converts a log-normal's natural-log sigma to nepers; the resulting dB-domain sigma is `10/ln(10) * 0.3454 = 1.5 dB`. A 3.0 dB dB-domain sigma would need the divisor `8.686/2 = 4.343`.
- **Independent confirmation from the artifact itself:** the committed run's realised EIR dispersion is **sd = 2.0535 dB** (MEASURED), which matches `1.5*sqrt(2) = 2.121 dB` and does not match `3.0*sqrt(2) = 4.243 dB`.
- **Why it matters for a paper conclusion:** the claim that *survives* (claim 10, 0/100 realisations below -10 dB) holds **only because of this factor-of-two error**.
  - at the implemented 1.5 dB: `P(one trial < -10 dB) = 0.0000`, `P(any of 100) = 0.000`
  - at the paper's stated 3.0 dB: `P(one trial < -10 dB) = 0.0078`, `P(any of 100) = 0.545`
- **Artifact path:** `ems-ieee-package/figures/metrics.json` carries no sigma field; the parameter lives only in `ems_simulator.py:55,291-292`. The dispersion is visible in `figures/fig_mc_beamsteer.png`.
- **Cross-check:** the C kernel prints `Std: 3.93 dB` for its own Monte Carlo — the C implementation honours the paper's stated 3.0 dB while the Python does not. The two implementations of the same paper use different noise.
- **Verdict: CONTRADICTED.** Claimed 3.0 dB; measured 1.4992 dB.

**D3 — the C "independent reference kernel" disagrees with the published results and reverses the headline ranking.**

`main.tex:153` states `ems_fdtd.c` "provides an **independent reference kernel**"; `README.md:66` and `presentation.tex:179` instruct the reader to compile and run it. It is presented as corroboration. MEASURED by executing it (**exit 0**):

| pattern | C kernel: RX / EV / EIR / C_s | Python `metrics.json`: RX / EV / EIR / C_s | agreement |
|---|---|---|---|
| transparent | `5.0307e-09 / 5.1884e-10 / +9.87 / 9.6522` | `3.53e-10 / 5.19e-10 / -1.68 / 4.13` | **EIR differs by 11.55 dB, opposite sign** |
| beamsteer | `2.7529e-09 / 5.1884e-10 / +7.25 / 8.5927` | `5.50e-10 / 5.19e-10 / +0.25 / 5.21` | **EIR differs by 7.00 dB** |
| diffuse | `4.2357e-10 / 5.4991e-10 / -1.13 / 4.4392` | `4.72e-10 / 6.26e-10 / -1.23 / 4.39` | close, not equal |
| focus | `4.0420e-10 / 5.1884e-10 / -1.08 / 4.4672` | `4.04e-10 / 5.19e-10 / -1.08 / 4.47` | agrees |

- **Claimed:** an independent reference that corroborates the model.
- **Actual:** agreement on 1 of 4 patterns, and it **reverses the paper's central conclusion**. The C kernel ranks transparent best (EIR +9.87 dB) and beamsteer second (+7.25 dB); the paper's headline is that beamsteer (+0.25 dB) beats transparent (-1.68 dB). The C kernel's own Monte Carlo prints `Mean EIR: 7.57 dB`, also inconsistent with the published +0.25 dB.
- The C kernel gives `transparent` a pass-through reflector (RX power 5.03e-09, *higher* than any RIS-on case), whereas the Python sets `w = 0.0` on every element, i.e. no reflection at all. **The two codebases do not implement the same model**, so the C file cannot serve as the independent check the paper claims for it.
- **Artifact paths:** `ems-ieee-package/ems_fdtd.c` vs `ems-ieee-package/figures/metrics.json`.
- **Verdict: CONTRADICTED.**

### UNSUPPORTED (3)

**U1 — "complete spatial isolation" at the eavesdropper is floating-point noise, not physics.**

- **Claimed** (`main.tex:236`): "Beamsteering achieves **complete suppression** of the RIS-reflected signal at the eavesdropper location ($AF_{ev} \approx 0$). This is **the fundamental mechanism** behind the security improvement."
- **Actual, MEASURED:** `AF_ev = 3.20474742746036e-30`, so `|AF_ev| = 3.33e-15`. The float64 cancellation floor for a sum of 64 unit-magnitude complex numbers is about `64 * eps = 1.42e-14`. **`|AF_ev|` is below that floor.** A 1-D phase ramp with no element pattern and no amplitude control cannot null a direction in 3-D space by 316 dB; what happens here is 64 near-cancelling complex exponentials whose sum is lost in floating-point noise (`ems_simulator.py:103`, `AF += w * np.exp(1j*psi)`). The suppression the paper interprets as physics is below machine precision, and it is the mechanism credited for the entire result.
- **Artifact path:** `ems-ieee-package/figures/metrics.json` → `AF_ev`.
- **Verdict: UNSUPPORTED.**

**U2 — the "beamsteering" pattern is not steered at the receiver.**

- **Claimed** (`main.tex:42`, `main.tex:236`): beamsteering "spatially isolates the legitimate receiver from the eavesdropper".
- **Actual, MEASURED by the auditor:** the receiver as seen from the RIS is at `theta = 7.125 deg, phi = -7.125 deg`. The beamsteer branch (`ems_simulator.py:84`) applies `phase = k * x_pos * sin(radians(theta_target))` with `theta_target = 30` a **hardcoded default**, and **ignores `phi` entirely**. Mis-steering angle: **22.87 degrees**.
  - `AF_rx` as configured = `140.89016399549186`; coherent maximum `g_ris_max = (8*8)^2 = 4096`
  - the configured pattern therefore sits **14.63 dB below** the achievable main lobe
  - correct conjugate steering at the true Rx direction yields `AF = N^2 = 4096`
  - **the mis-steering costs 14.6 dB of receiver gain**
- The pattern is simultaneously mis-pointed at the receiver and accidentally nulled at the eavesdropper.
- **Artifact path:** `ems-ieee-package/figures/metrics.json` → `AF_rx: 140.89016399549186`; generator `ems_simulator.py:61-105`.
- **Verdict: UNSUPPORTED.**

**U3 — the secrecy-capacity values cannot be derived from the paper's stated definitions.**

- **Claimed** (`main.tex:110-117`): `C_s = max{0, log2(1+SINR_RX) - log2(1+SINR_EV)}`, with `SINR_RX = P_RX/(P_EV*alpha + N_0)`, `alpha = 0.01`. **The disclosure of `alpha = 0.01` is a genuine point in the paper's favour and is recorded as such.**
- **Actual:** the paper gives **no formula for `SINR_EV` at all**. The code (`ems_simulator.py:194`) uses `sinr_ev = 10*log10(P_ev / (P_rx*0.5 + 1e-30))` — a hardcoded `0.5` that appears nowhere in the paper or any parameter table (verified by grep over `main.tex`). `C_s` depends directly on `SINR_EV`, so all four secrecy capacities rest on an undisclosed constant.
- **Visible consequence in the paper's own Table I:** for `transparent` the artifact records `ev_power = 5.19e-10 > rx_power = 3.53e-10` and `eir_dB = -1.68` — **the eavesdropper is stronger than the legitimate user** — yet the table reports **+4.13 bps/Hz** of secrecy capacity. Both numbers sit in the same row and the inconsistency is never remarked upon.
- **Artifact path:** `ems-ieee-package/figures/metrics.json` → `secrecy_capacity_bps_Hz: 4.128960029998177` beside `eir_dB: -1.6765414772693035`.
- **Verdict: UNSUPPORTED.**

## L4 — figures

**Verdict: CONTRADICTED.**

`git status` after a full successful run is the authoritative test of which figures have generators. The run rewrote 7 of 8 committed figures. **`figures/fig_signals.png` and `figures/fig_signals.pdf` were not rewritten, and `grep -c 'signals' ems_simulator.py` returns `0` — no committed code in the repository generates them.**

**F1 — `fig_signals` has no generator and contains no data.** The committed PNG was inspected visually: a 4x2 grid titled `transparent: RX signal`, `transparent: EV signal`, ... `focus: EV signal`, plotting `Ez (V/m)` against `Time (ns)`. **All eight panels are flat lines at exactly 0.00 V/m** — identically zero, every pattern, both receiver and eavesdropper, on a y-axis spanning -0.05 to +0.05. A figure labelled "signal" that shows no signal, with no generator. It survives re-execution only because nothing writes it.

**F2 — `fig_array_pattern` is generated at a different geometry than the one that produced `metrics.json`.** `plot_array_pattern` (`ems_simulator.py:270`) calls `ris_array_factor(th, 0, p)` with **`phi` hardcoded to 0** across all 181 angles. The benchmark instead evaluates the array factor at each receiver's true direction: `theta = 7.125, phi = -7.125` deg for Rx, `theta = 45, phi = -45` deg for Eve. The figure's x-axis is not the quantity used in the results. Visual inspection confirms it does not resemble a designed beam: the `beamsteer` trace peaks broadly near **-30 to -40 degrees** rather than at the intended +30, with nulls to **-275 dB** at 0 and +30 that force the y-axis to -300 dB and compress all meaningful structure into the top 15% of the plot.

Both are recorded as L4 CONTRADICTED per the rubric clause "figure exists with no generator".

The other 7 figures (`fig_field_*` x4, `fig_security_comparison`, `fig_array_pattern`, `fig_mc_beamsteer`) have committed generators that ran, and their data matches `metrics.json`. **7 of 8 figures are sound.**

## L5 — method

**Verdict: CONTRADICTED.**

The RIS phased-array channel model is genuinely implemented and genuinely ran: Friis path loss, a 30 dB wall-blocked direct path, Friis gains on both RIS hops, a 64-element array factor, and a 100-trial Monte Carlo. That is a real method and it produced the reported numbers.

What it does not do is what the paper says it does. The central mechanism claim is contradicted (U1, U2): the beam is mis-steered by 22.87 degrees, forfeits 14.63 dB of available receiver gain, and the "complete suppression" credited for the security improvement is below the float64 cancellation floor. The independent reference kernel offered as corroboration (D3) implements a different model and reverses the ranking.

**Dead code, verified:** `ems_fdtd.c` (245 lines) is referenced only by prose (`main.tex:153`, `README.md:31,66`, `presentation.tex:170-179`) and a manual `gcc` line. There is **no Makefile, CMakeLists.txt, or setup.py in any of the four audited packages**, and no Python file in the repository imports, `ctypes`-loads, or otherwise references it. It compiles cleanly and runs, and **no result in the paper is produced by it.**

## L6 — selection

**Verdict: SUPPORTED.**

No undeclared selection of seed, trial, or best case was found. The simulator uses a single fixed geometry and a fixed 100-trial Monte Carlo; the full distribution is plotted in `fig_mc_beamsteer.png` rather than a selected realisation. The auditor looked specifically for the `cd`/`h266` pattern and did not find it here: the one surviving robustness claim (claim 10) is reported as a distribution statistic with its sample size, and it holds.

One related observation, recorded so the next reader does not mistake it for a live hazard: `shadow_fading()` (`ems_simulator.py:115-120`) calls `np.random.seed()` with no argument, which seeds from OS entropy and would break reproducibility — **but the function is never called**, so it has no effect.

## L7 — internal consistency

**Verdict: CONTRADICTED.**

- The abstract's ">140 dB" (D1) is inconsistent with the EIR of +0.25 dB reported two sentences earlier in the same abstract, and with the 316.4 dB the artifact's array factors imply. The abstract cannot be read consistently with itself.
- The parameter table's `sigma = 3.0 dB` (D2) is inconsistent with the Monte Carlo figure it is meant to justify, and with the C kernel's own dispersion.
- Table I reports a positive secrecy capacity of 4.13 bps/Hz in the same row as a negative EIR of -1.68 dB (U3), with no reconciliation anywhere in the paper.
- `fig_array_pattern` (F2) is generated at `phi = 0` while `metrics.json` is computed at the true per-receiver `phi`, so figure and table do not describe the same evaluation.

Against that: the abstract, body, and Table I agree with each other and with the artifact on every EIR and secrecy-capacity number. The inconsistencies are confined to the dB-suppression figure, the sigma parameter, and the undisclosed `SINR_EV` constant.

## L8 — verdict

**PARTIALLY SUPPORTED.** The paper's central quantitative claim — beamsteering achieves EIR +0.25 dB and secrecy capacity 5.21 bps/Hz, beating the transparent baseline — reproduces exactly from committed code, and all 16 cells of Table I are faithful. The package fails on mechanism, not on arithmetic: the beam is mis-steered, the eavesdropper null is below machine precision, the stated fading sigma is half the implemented one, and the C reference kernel reverses the conclusion.

## What survived as SUPPORTED (ems)

Explicitly and prominently, per R7:

1. **All 16 cells of Table I** — every RX power, EV power, EIR and secrecy capacity for all four RIS patterns — match `figures/metrics.json` to 3 significant figures.
2. **Both headline EIR values** (+0.25 dB beamsteer, -1.68 dB transparent) and the headline secrecy capacity (5.21 bps/Hz).
3. **The Monte Carlo robustness claim** — "no realisations falling below -10 dB" is measurably true: 0/100, minimum -3.96 dB. This survived a prediction that it would not.
4. **Both array-factor disclosures** at `main.tex:187` (`AF_ev = 3.2e-30` for beamsteer, `0.006` for focus), transcribed correctly from the artifact.
5. **The claim that beamsteering is the only pattern with positive EIR.**
6. **The disclosure of `alpha = 0.01`** in the secrecy-capacity definition — unusually candid for a simulation paper in this set, and matching the code exactly.
7. **7 of 8 figures** have committed, running generators whose output matches the artifact.
8. **`metrics.json` reproduced bit-identically on every quantity the paper reports**, on a toolchain (numpy 2.5.3 / Python 3.14.3) far newer than the artifact's.

## Gaps a reviewer would reject ems over

1. The mechanism is wrong. A 22.87-degree mis-steered beam forfeiting 14.63 dB is not "spatial isolation of the receiver".
2. The load-bearing null (`AF_ev = 3.2e-30`) is below the float64 cancellation floor, so the central physical claim rests on a numerical artifact.
3. The stated shadow-fading sigma is 2x the implemented value, and the robustness claim survives only because of that error.
4. The C kernel offered as independent verification disagrees on 3 of 4 patterns and reverses the headline ranking.
5. `fig_signals` is a figure with no generator whose eight panels are all identically zero.
6. No formula is given for `SINR_EV`, yet positive secrecy capacity is reported for a configuration where the eavesdropper is stronger than the user.

---

# 2. `qce` — Quantum-Classical Co-Design for Error Prediction and Mitigation

**Repository:** `FernandoMay/qce-ieee-package` (HTTP 200; 20 tracked files; 5 commits, HEAD `97ed1cb`)
**Claimed topic (backlog):** quantum-classical optimizer, RL predictor, C kernel
**Evidence class:** E1, seeded simulation with `metrics.json` and figures

## Research question

Can a hybrid "quantum-classical" co-design — a variational optimizer for offline policy selection plus an online learning predictor for error forecasting — deliver the reliability of always-on full mitigation at lower average power in an ultra-low-power embedded system?

**What "quantum" means here, concretely:** the class is `QuantumInspiredOptimizer` (`qce_simulator.py:192-277`). It builds a 5-qubit cost Hamiltonian from reliability/energy/latency scalars, then **enumerates all 32 computational basis states and returns the one with the lowest diagonal energy.** It is a 32-element exhaustive classical search dressed as a QAOA ansatz. Its docstring says "parameterized quantum circuit ansatz simulated classically"; there is no circuit. `self.params` (4 variational angles) is initialised and **never read**; `psi = |+>^n` is constructed and **never used**; the mixer Hamiltonian `H_b` is built and **never used**. This is checked empirically in the L5 section. The paper's Methods section discloses the enumeration; its abstract, contributions, results and conclusion do not.

## What was executed, with real output

`qce_simulator.py`, full run, **exit code 0**, 15.0 s. Real stdout, results section verbatim:

```
  [Baseline: No Mitigation]
  Errors: 15, Avg Power: 480.1mW, Avg Reliability: 0.0025
  [Baseline: Reactive Mitigation]
  Errors: 1, Avg Power: 596.1mW, Avg Reliability: 0.7543
  [Baseline: Full Mitigation]
  Errors: 0, Avg Power: 727.3mW, Avg Reliability: 0.9117
  [Proposed: QCE Co-Design]
  Errors: 0, Avg Power: 627.3mW, Avg Reliability: 0.9237
```

Plus: the C kernel (**exit 0**, one compiler warning), and four auditor instrumentation passes on the optimizer, the predictor, the executed policy, and the ablation code paths.

## L3 — every numerical claim, both values, artifact path

**Artifact path for this entire package: `qce-ieee-package/figures/metrics.json`.**

### SUPPORTED (11)

| # | Claim (source) | Claimed | Artifact value | Verdict |
|---|---|---|---|---|
| 1 | QCE 13.8% lower power than full (abstract, l.53) | `13.8%` | `(727.2826656034424 - 627.345737700338)/727.2826656034424 = 13.74%`; from the paper's own displayed `727.3 -> 627.3` = 13.75% | SUPPORTED |
| 2 | reliability 0.924 vs 0.912 (abstract, l.54) | `0.924 / 0.912` | `0.9236938623777413 / 0.9116773270888011` | SUPPORTED |
| 3 | QCE zero errors | `0` | `qce.total_errors = 0` | SUPPORTED |
| 4 | Table I, No Mitigation row (l.389) | `15 / 480.1 / 0.0025 / 0.005` | `15 / 480.09367553644483 / 0.002492656830748843 / 5.192e-06` | SUPPORTED |
| 5 | Table I, Reactive row (l.390) | `1 / 596.1 / 0.7543 / 1.27` | `1 / 596.0904442623045 / 0.7543388640664943 / 1.2655e-03` | SUPPORTED |
| 6 | Table I, Full Mitigation row (l.391) | `0 / 727.3 / 0.9117 / 1.25` | `0 / 727.2826656034424 / 0.9116773270888011 / 1.2535e-03` | SUPPORTED |
| 7 | Table I, Quantum-Only row (l.392) | `0 / 627.3 / 0.9237 / 1.47` | `0 / 627.345737700338 / 0.9236938623777413 / 1.4724e-03` | SUPPORTED (as transcription — and see D4) |
| 8 | Table I, QCE (Proposed) row (l.393) | `0 / 627.3 / 0.9237 / 1.47` | `0 / 627.345737700338 / 0.9236938623777413 / 1.4724e-03` | SUPPORTED |
| 9 | Policy table (l.256-259) | `0.01->[0,0,0,0,0]; 0.10->[1,1,1,1,1]; 0.30->[1,1,1,1,1]; 0.70->[1,1,1,1,1]` | **MEASURED by running the committed optimizer at all four risk levels: exactly `[0,0,0,0,0]`, `[1,1,1,1,1]`, `[1,1,1,1,1]`, `[1,1,1,1,1]`** | SUPPORTED |
| 10 | Safety floor 0.15 (l.275, l.363) | `sigma = 0.15` | `ErrorPredictor.safety_floor = 0.15`; observed `pred_prob` minimum = `0.1500` | SUPPORTED |
| 11 | The weight arithmetic for risk 0.01 (l.233-237) | `w = [-0.095, -0.015, -0.045, -0.015, -0.100]` | the auditor reproduced this arithmetic independently; all five match, and the paper's `w_4 = -0.100` is **correct** where a naive `0.08*0.5 - 0.4*0.3 - 0.1*0.2` would give `-0.100` — confirmed | SUPPORTED |

Claim 9 is a genuinely strong result: the published policy table is not merely consistent with the code, it is exactly what the code produces, and the auditor verified it by executing the committed optimizer directly rather than reading it.

### CONTRADICTED (5)

**D1 — "Pareto-optimal" is claimed four times; the code contains no Pareto computation whatsoever.**

- **Claimed:** abstract — "pre-computes **Pareto-optimal** configurations of DVFS and mitigation strategies"; contributions (l.44) — "to compute **Pareto-optimal** operating points"; results (l.482) — "identifying the **Pareto-optimal** configuration for each risk regime"; conclusion (l.489) — "identify **Pareto-optimal** (DVFS, mitigation) configurations across risk levels".
- **Actual, MEASURED:** the entire 696-line `qce_simulator.py` contains **zero** occurrences of `pareto`, `Pareto`, `front`, `nondominat`, `hypervolume`, or `non-dominated` (grep, exact counts reported in L5). The optimizer minimises a **single scalar weighted objective**, `weight = reliability[i]*0.5 - energy[i]*0.3 - latency[i]*0.2` (`qce_simulator.py:229`), which returns exactly one point. A weighted-sum scalarisation produces a point on a Pareto front at best; no front is ever computed, and no second objective is ever retained.
- **Artifact path:** no artifact exists for this claim; the paper asserts it and the code refutes it.
- **Verdict: CONTRADICTED.**

**D2 — the abstract's method description contradicts the paper's own Methods section.**

- **Claimed** (abstract, l.26): a "quantum-inspired variational optimizer", "based on a **simplified QAOA ansatz**"; (contributions, l.44) a "simplified Quantum Approximate Optimization Algorithm (QAOA) ansatz" that "efficiently explores the combinatorial space"; (l.219) "The mixer Hamiltonian employs single-qubit $X$ rotations".
- **Actual:** the paper's own Methods section, `main.tex:226`, states: "**Since the full QAOA variational optimization is computationally intensive for online deployment, we perform basis-state enumeration: each of the $2^{N_M} = 32$ computational basis states is evaluated against $H_C$, and the state with minimum energy is selected.**"
- So the Methods section is honest and the abstract is not. The auditor verified that the Methods description is accurate: the mixer Hamiltonian `H_b` is computed and discarded, and `self.params` is never read — meaning the "QAOA ansatz" has neither a mixer nor any variational parameter anywhere in the pipeline. `main.tex:219`'s description of a mixer is a description of code that is built and thrown away.
- This is recorded as **CONTRADICTED rather than UNSUPPORTED or hidden**, because the paper does disclose the truth — in a different section. A reviewer reading only the abstract, the contributions, or the conclusion would be misled; a reviewer reading the Methods would not. That inconsistency, not concealment, is the finding.
- **Artifact path:** `qce-ieee-package/qce_simulator.py:249-277`; `qce-ieee-package/figures/metrics.json` (the policy table that the enumeration does produce, claim 9).
- **Verdict: CONTRADICTED.**

**D3 — the paper claims the predictor "successfully distinguishes between safe and risky operating conditions"; it never crosses a decision threshold.**

- **Claimed** (`main.tex:460`): "Fig. 5 shows the RL predictor's output probability alongside actual error occurrences. **The predictor successfully distinguishes between safe and risky operating conditions.**" Also abstract/l.45: "enabling **anticipatory rather than reactive** mitigation."
- **Actual, MEASURED by the auditor** by instrumenting `run_episode` over all 200 steps:
  - distinct mitigation masks observed: `{(1, 1, 1, 1, 1)}` — **one mask, all 200 steps**
  - distinct risk levels used: `[0.1]` — **one level**
  - distinct DVFS levels used: `[2]` — **one level**
  - `pred_prob` range over 200 steps: `0.1500` to `0.5750`
  - learned weights at end: `[0.0242, -0.1913, -0.1725, -0.0562]` from a random init of `randn(4)*0.1`
- **Why it is inert, precisely:** the safety floor guarantees `pred_prob >= 0.15`, and the risk selection rule is `risk = 0.01` only when `pred_prob <= 0.05` (`main.tex:304`). **0.15 > 0.05, so the only risk level with a non-all-on mitigation mask is unreachable by construction.** The `0.5750` maximum occurs at step 0 only, where the observation is an all-zero vector (`system.health_metrics[0]` is unwritten at that point) and where the `t < 10` warmup branch ignores `pred_prob` entirely and selects risk by temperature.
- Because QCE produced 0 errors, `actual_error` is `0.0` at all 200 steps, so the online SGD update is always in the same direction and drives `raw_pred -> 0`, i.e. `pred_prob -> 0.15`. The predictor converges onto the safety floor and stops.
- **Artifact path:** `qce-ieee-package/figures/metrics.json` → `qce.avg_active_mitigations = 5.0`; `qce-ieee-package/figures/fig_mitigation_activity.png`; `figures/fig_prediction_accuracy.png`.
- **Verdict: CONTRADICTED.**

**D4 — the paper's own tables report that the co-design halves are interchangeable; the abstract does not mention it.**

- **Claimed** (abstract, l.26): QCE "**combines** a quantum-inspired variational optimizer **with** an online reinforcement learning predictor". The whole contribution is the conjunction.
- **Actual, from the paper's own committed tables:**
  - `main.tex:392-393`: the `Quantum-Only` row is `0 / 627.3 / 0.9237 / 1.47` and the `QCE (Proposed)` row is `0 / 627.3 / 0.9237 / 1.47` — **identical in all four columns.** Removing the classical half changes nothing.
  - `main.tex:448-449`: the `QCE-NoRL` row is `0 / 627.3 / 0.9237` and the `QCE (full)` row is `0 / 627.3 / 0.9237` — **identical in all three columns.** Removing the RL predictor changes nothing.
  - The auditor confirmed the mechanism: since the policy is a constant mask and a constant DVFS level, there is nothing for either component to influence.
- A paper that reports a null result twice in its own tables, and headlines the conjunction of the two components in its abstract, has a framing defect that its numbers refute. The honest reading is that the safety floor alone determines the executed policy.
- **Artifact path:** `qce-ieee-package/figures/metrics.json` → `qce.*` and `full.*`; the null rows themselves are in the paper's LaTeX and are separately graded as U1/U2 below.
- **Verdict: CONTRADICTED.**

**D5 — the C "reference kernel" reports a different result from the paper.**

- **Claimed** (`README.md:10`): `qce_kernel.c` is a "Reference C implementation"; `README.md:35-37` instructs the reader to compile and run it.
- **Actual, MEASURED by executing it (exit 0):**

| quantity | C kernel | Python `metrics.json` (`qce`) | agreement |
|---|---|---|---|
| Total errors | `0` | `0` | agrees |
| Avg power | `619.0 mW` | `627.345737700338 mW` | differs by 8.3 mW (1.3%) |
| Avg reliability | **`1.0000`** | **`0.9236938623777413`** | **disagrees — the kernel reports perfect reliability** |
| Energy efficiency | `0.001616` | `0.0014723840569373751` | differs |
| policy table | `0.01->DVFS3 [0,0,0,0,0]`, `0.10->DVFS2 [1x5]`, `0.30->DVFS1 [1x5]`, `0.70->DVFS0 [1x5]` | same (claim 9) | **agrees exactly** |

- The C kernel independently reproduces the policy table, which is a point in its favour and is recorded. But it reports `Avg Reliability: 1.0000` where the paper's headline is `0.924`, so it cannot corroborate the reliability claim.
- The kernel also ships a real bug: `static float randf(void) { return (float)rand() / RAND_MAX; }` (`qce_kernel.c:45`) casts `RAND_MAX = 0x7fffffff` to `float`, which clang flags: `warning: implicit conversion from 'int' to 'float' changes value from 2147483647 to 2147483648`. The numerical effect is 1 ULP and is not material; the warning is shipped in a repository whose README presents the file as a reference implementation.
- **Artifact paths:** `qce-ieee-package/qce_kernel.c` vs `qce-ieee-package/figures/metrics.json`.
- **Verdict: CONTRADICTED.**

### UNSUPPORTED (2)

Both rows of the paper's ablation table (`main.tex:447-449`) have **no committed code path that can produce them.** `run_episode`'s signature is `(system, predictor, optimizer, mitig_mgr, external_temp=30, use_quantum=True, alpha=0.5)` — no `use_rl`, no `safety`, no `ablate` parameter (verified via `inspect.signature`). `ErrorPredictor.safety_floor = 0.15` is hardcoded in `__init__` with no override. Grep for `NoSafety`, `NoRL`, `ablation`, `ablate` across the whole source returns an empty list. `main()` runs exactly four policies: none, reactive, full, qce. There is no fifth.

**U1 — `QCE-NoSafety`: 21 errors, 578.3 mW, reliability 0.0070. UNSUPPORTED.** No committed code can produce this row. The paper's narrative for it — that without the floor the predictor's weights drift downward, selecting risk 0.01 (DVFS 3, no mitigations), causing "thermal runaway and 21 errors" — is **mechanically consistent with the code the auditor did read** (`risk = 0.01` is indeed the only mask-free level, and DVFS 3 is indeed the highest-power level), so the claim is plausible. It remains unverifiable from the package, and per R8 an unverifiable layer is a result, not an omission.

**U2 — `QCE-NoRL`: 0 errors, 627.3 mW, 0.9237 — identical to QCE. UNSUPPORTED.** No committed code can produce this row either. This one matters more than U1, because it is the paper's own statement that the RL predictor contributes nothing, and it is the single strongest piece of evidence for the L5/L6 findings. It cannot be checked from the package; the auditor's independent instrumentation of the live run reaches the same conclusion independently (D3), so **the finding stands even though the table row does not.**

### L3 count note

Itemised enumeration: **11 SUPPORTED, 5 CONTRADICTED, 2 UNSUPPORTED, total 18.** The machine-readable row above matches, and the aggregate uses this split. An earlier draft of this report recorded `L3 total 19` for qce; the nineteenth item was the `full.avg_active_mitigations` accounting defect, which is an artifact-integrity fault rather than a paper claim and is graded under L6 and L7 instead. Corrected so the row is internally consistent.

## L4 — figures

**Verdict: CONTRADICTED.**

All 5 committed figures have committed generators that ran and were rewritten. Two are defective, one materially.

**F1 — `fig_system_overview.png` contains no data at all.** `plot_system_overview` (`qce_simulator.py:491-500`) calls `ax.text(...)` with a literal string, sets a title, and calls `ax.axis('off')`. Visual inspection confirms: a blank canvas titled "QCE System Overview" with a centred four-line text block reading "Embedded System Model / 4 Cores, 8 Tasks, 5 Mitigations / NISQ-Inspired Optimizer". It is a text box, not a system diagram, and it plots nothing. It is offered as the system-overview figure of a co-design framework.

**F2 — `fig_comparison.png` plots three series on one axis; two are invisible.** `plot_comparison` (l.550-552) puts `avg_power` (480-727 mW), `avg_reliability` (0.0025-0.9237) and `total_errors/10` (0-1.5) on a **single shared linear y-axis** spanning 0 to ~730. The legend advertises all three series, and the "Avg Reliability" and "Errors/10" bars are **not visible anywhere in the committed figure** — they are 2-4 orders of magnitude below the power bars. The right panel ("Energy Efficiency") does show four bars, with `No_Mitigation` effectively at zero (`5.19e-06` against an axis topping at `0.0014`). This is a **generator defect**: the figure's logic, not its data, is the fault.

**F3 — `fig_mitigation_activity.png` is a flat line at 5.0 for all 200 steps.** The generator is faithful to the data (`avg_active_mitigations: 5.0`), so this is L4-clean and L5-contradicted. It is recorded here because it is the figure that most directly refutes the adaptivity claim, and a shaded region labelled "Mitigation Strategy Activation" would reasonably be read as evidence of activation dynamics. The flat line is the evidence that there are none.

**F4 — `fig_prediction_accuracy.png` is flat at 0.15 after step 1**, with one spike to 0.575 at step 0 (the zero-observation artifact) and "Actual Errors" flat at 0. Generator faithful; the paper's caption interpretation (D3) is not.

`fig_health_metrics.png` (4-panel temp/power/reliability/errors) is sound and was inspected.

## L5 — method

**Verdict: CONTRADICTED.**

Three methods are described; the auditor graded each against the code.

**M1 — the "variational optimizer".** `QuantumInspiredOptimizer.optimize` is a 32-element exhaustive classical scan. Verified empirically:
- `psi = |+>^n` — assigned, never used
- `self.params` (4 variational angles, `n_layers*2`) — initialised, **never read**; `n_layers` is inert
- `H_b`, the mixer Hamiltonian — built by a full method, **never used**
- the 32-state loop reads only `H_c`'s diagonal, so the `X_i X_j` couplings added at l.233-235 (comment: "pairwise couplings encourage complementary activation") contribute **nothing** — off-diagonal terms vanish against a basis vector
- "QAOA" survives in this package as a class name and a figure caption

**M2 — the "RL predictor".** `ErrorPredictor.update` (l.179-187) is online logistic regression by gradient descent on 4 weights. A real, if minimal, learner, and it ran. But `self.gamma = 0.9` (l.166) is set and **never used** — no discount factor, no TD target, no policy, no action space, no reward. There is no reinforcement learning in the RL sense. **The paper is candid**: the abstract says "implemented as lightweight logistic regression with safety-bounded predictions", which is accurate. Recorded as a naming issue, not a hidden method.

**M3 — the "Pareto" co-design.** A single weighted scalar; no front (D1).

**M4 — the executed policy.** The decisive finding. The policy machinery — 4 risk levels, a learned predictor, a threshold rule, a 32-state optimizer — executes to produce **one constant mask and one constant DVFS level across all 200 steps** (D3). Both the "quantum" optimizer and the RL predictor have **zero influence on executed behaviour**; the safety floor alone determines it. What distinguishes QCE from full mitigation is a single DVFS level, which the paper itself states plainly at `main.tex:484`.

**Dead code, verified:** `qce_kernel.c` (326 lines) is referenced only by `README.md:10,27,35-37`. No Makefile, CMakeLists, or setup.py exists in any of the four packages; no Python file imports or `ctypes`-loads it. It compiles (with a warning) and runs, and **no result in the paper is produced by it** — while reporting a different reliability (1.0000) from the paper's headline (0.924).

## L6 — selection

**Verdict: CONTRADICTED.**

No best-case seed selection was found; the seed is fixed at 42 and the full 200-step trajectory is plotted. The L6 failure here is different: **the paper reports a null result for its own contribution in two separate tables and omits it from the abstract and conclusion.**
- `Quantum-Only` == `QCE (Proposed)`, all four columns (l.392-393)
- `QCE-NoRL` == `QCE (full)`, all three columns (l.448-449)

A paper that reports a null twice in its own tables and headlines the conjunction of both components in its abstract has a framing defect its own numbers refute. A reader of the abstract concludes two components produced the result; the body says one was not needed.

Recorded as an artifact-integrity defect, not a paper discrepancy: `metrics.json` reports `full.avg_active_mitigations = 0.0`, but `run_baseline_full_mitigation` (l.421-428) passes `mit_mask = [1]*5` at **every** step. Its history dicts carry no `'mit_mask'` and no `'mitigation_active'` key, so `compute_metrics` (l.470-475) falls through to `active_mits.append(0)`. The `0.0` is an accounting bug: the baseline ran with all five mitigations active throughout and is recorded as having none. Table I does not report this field, so it is not a paper discrepancy — but it is a wrong number in the shipped artifact.

## L7 — internal consistency

**Verdict: CONTRADICTED.**

- **Abstract vs Methods (D2).** The abstract promises a QAOA ansatz; `main.tex:226` states basis-state enumeration. These cannot be reconciled.
- **"Pareto-optimal" in four sections vs no Pareto code (D1).**
- **Table rows vs abstract (D4).** `Quantum-Only` and `QCE-NoRL` are identical to QCE, contradicting the conjunctive framing.
- **Figure caption vs figure (D3, F4).** `main.tex:460` says the predictor "successfully distinguishes between safe and risky operating conditions"; the cited figure is a flat line at the safety floor.
- **`fig_system_overview`** advertises a "NISQ-Inspired Optimizer" that is a 32-state enumeration with an unused mixer and no parameters.

Consistent across the paper: the four headline numbers (errors, power, reliability, efficiency) agree exactly in the abstract, Table I, and `metrics.json`. The inconsistency is confined to method naming, the Pareto claim, and the ablation framing.

## L8 — verdict

**PARTIALLY SUPPORTED.** Every quantitative claim the paper makes about its own simulation reproduces exactly, `metrics.json` is bit-identical, and the published policy table was independently confirmed by executing the committed optimizer. The central claim — a quantum-classical co-design — is contradicted by the code: no variational circuit, no Pareto computation, and an executed policy that is constant, meaning neither component influences the result. The paper's own tables say so.

## What survived as SUPPORTED (qce)

Explicitly, per R7:

1. **All four headline numbers reproduce exactly**: 13.8% power reduction, 0.924 vs 0.912 reliability, zero errors for both QCE and full mitigation.
2. **All 20 cells of Table I** match `figures/metrics.json` to 4 significant figures, including the energy-efficiency column.
3. **The published policy table (claim 9) is exactly what the committed optimizer produces** — verified by executing it at all four risk levels, not by reading it.
4. **The weight arithmetic in `main.tex:233-237` is correct**, including the `w_4 = -0.100` value, which the auditor reproduced independently.
5. **The paper discloses its actual algorithm in the Methods section** (`main.tex:226`), and that disclosure is accurate. This is unusual candour and it is the reason the finding is scored CONTRADICTED rather than UNSUPPORTED.
6. **The abstract describes the predictor honestly** — "lightweight logistic regression with safety-bounded predictions" — which is what it is.
7. **The safety floor of 0.15 is stated and matches the code exactly**, and its effect (predictions never below 0.15) is observable and as described.
8. **`metrics.json` is bit-identical** on a toolchain far newer than the artifact's.
9. **The C kernel independently reproduces the policy table exactly**, which corroborates the one part of the optimizer that does real work.
10. **No seed or best-case selection** anywhere; the full 200-step trajectory is plotted.

## Gaps a reviewer would reject qce over

1. "Pareto-optimal" is claimed four times and computed zero times.
2. The abstract's method description contradicts the paper's own Methods section.
3. The executed policy is constant — one mask, one DVFS level, 200 steps — so neither the optimizer nor the predictor does anything.
4. The paper's own tables report the co-design halves as interchangeable, and the abstract omits this.
5. The entire ablation table has no committed code path.
6. `fig_system_overview` is a text box; `fig_comparison` has two of three series invisible.
7. The C reference kernel reports reliability 1.0000 against the paper's 0.924.

---

# 3. `quantum-k-sat` — QAOA for K-SAT Optimization on NISQ Devices

**Repository:** `FernandoMay/quantum-k-sat-ieee-package` (HTTP 200; 20 tracked files; 1 commit, HEAD `dc1e43c`)
**Claimed topic (backlog):** QAOA simulator, noise models, mitigation figures
**Evidence class:** E1, seeded simulation with `metrics.json` and figures

## Research question

Does QAOA solve random 3-SAT instances robustly under depolarizing noise, and do standard NISQ mitigation techniques (zero-noise extrapolation, readout-error calibration) restore performance on shallow circuits?

**What "quantum" means here, concretely — and this is the most important single statement in the batch:**

This is a **full classical state-vector simulation in NumPy**, not a quantum computation and not a quantum-device emulation. Concretely:
- A `2^n`-complex amplitude vector is propagated in classical memory. At `n = 14` that is 16,384 complex numbers held in a NumPy array. No quantum backend, no circuit library, no transpiler, no density matrix, no sampling.
- The `mixer` is **not** a QAOA transverse-field mixer `exp(-i*gamma*sum_j X_j)`. It is a hand-rolled cascade of two-level unitaries. The auditor verified it **is** unitary (MEASURED: `||out||^2 = 1.000000000000` at `gamma = 0.0, 0.3, 0.9`), so it is a valid Hamiltonian evolution — just not the standard QAOA mixer.
- The parameters are **not** optimized variationally. `optimize_qaoa` draws `g = np.random.uniform(0, np.pi, p)` and `b = np.random.uniform(0, np.pi, p)` 30-40 times and keeps the best (l.98-110). This is **random search**, with no gradient, no COBYLA, no parameter-shift rule, no warm start.
- There is **no measurement**. `best_sat_from_state` (l.69-77) takes `np.argsort(probs)[-10:]` — the ten highest-probability basis states read straight out of the amplitude vector at full precision — evaluates the SAT ratio of each, and returns the **maximum**. On real hardware you obtain one bitstring per shot with probability `|psi_i|^2`; here the "shots" are the ten most likely outcomes known exactly, and the reported score is the best of them. WalkSAT, by contrast, performs 2000 genuine random flips. The comparison is therefore between an oracle readout and a real search.
- The noise is a **classical admixture**, not a quantum channel (D5 below).

There is no C kernel in this package. It is the only one of the four with none.

## What was executed, with real output

`simulator/quantum_k_sat_simulator.py`, full run, **exit code 0**, **548.5 s** (9m08s — the longest execution in the batch). Real stdout, all four experiments verbatim:

```
=== Experiment 1: Noise vs Performance ===
  noise=0.00: QAOA=0.981+-0.011  WS=0.972+-0.049  R=0.874
  noise=0.05: QAOA=0.986+-0.006  WS=0.964+-0.043  R=0.877
  noise=0.10: QAOA=0.972+-0.023  WS=0.914+-0.034  R=0.876
  noise=0.15: QAOA=0.986+-0.011  WS=0.969+-0.042  R=0.885
  noise=0.20: QAOA=0.972+-0.025  WS=0.964+-0.039  R=0.872
  noise=0.25: QAOA=0.983+-0.010  WS=0.967+-0.055  R=0.873
  noise=0.30: QAOA=0.972+-0.023  WS=0.950+-0.042  R=0.869
  noise=0.35: QAOA=0.981+-0.011  WS=0.972+-0.040  R=0.876
  noise=0.40: QAOA=0.978+-0.008  WS=0.956+-0.033  R=0.882
  noise=0.45: QAOA=0.983+-0.010  WS=0.972+-0.040  R=0.878
  noise=0.50: QAOA=0.983+-0.017  WS=0.911+-0.048  R=0.875
=== Experiment 2: Scaling ===
  n=8: QAOA=0.994  WS=0.972  R=0.877
  n=10: QAOA=0.973  WS=0.969  R=0.872
  n=12: QAOA=0.985  WS=0.974  R=0.871
  n=14: QAOA=0.981  WS=0.959  R=0.874
=== Experiment 3: Depth ===
  p=1: SAT=0.9833  gap=5.7075
  p=2: SAT=0.9667  gap=6.6804
  p=3: SAT=0.9667  gap=6.2409
  p=4: SAT=0.9667  gap=5.9694
=== Experiment 4: Mitigation ===
  none: 0.963+-0.024
  zne: 0.967+-0.015
  readout: 0.990+-0.008
  both: 0.970+-0.016
Best QAOA (noise=0.05): 0.986
Best WalkSAT: 0.972
```

## L3 — every numerical claim, both values, artifact path

**Artifact path for this entire package: `quantum-k-sat-ieee-package/data/metrics.json`.**

### SUPPORTED (13)

| # | Claim (source) | Claimed | Artifact value | Verdict |
|---|---|---|---|---|
| 1 | QAOA p=2 mean 0.986 in low-noise (abstract) | `0.986` | `noise.qaoa_m[1] = 0.9861111111111112` at `noise=0.05` | SUPPORTED |
| 2 | "maintains a mean SAT ratio above 0.97 across the full noise range [0,0.5]" (l.150) | `> 0.97` | minimum of `qaoa_m` = `0.9722222222222223` | SUPPORTED |
| 3 | random sampling `0.876 +- 0.005` (l.150, l.236) | `0.876 / 0.005` | `rand_m` mean `0.8760`, sd `0.0042` | SUPPORTED |
| 4 | n=8: QAOA 0.994 vs WalkSAT 0.972 (l.160) | `0.994 / 0.972` | `0.9944444444444445 / 0.9722222222222221` | SUPPORTED |
| 5 | n=14: QAOA 0.981 vs WalkSAT 0.959 (l.160) | `0.981 / 0.959` | `0.980952380952381 / 0.9587301587301587` | SUPPORTED |
| 6 | n=8 random `0.877` (l.160) | `0.877` | `0.8766666666666666` | SUPPORTED |
| 7 | depth `0.983 for p=1 vs 0.967 for p=2-4` (l.170) | `0.983 / 0.967` | `0.9833333333333333 / 0.9666666666666667` | SUPPORTED |
| 8 | mitigation readout `0.990 +- 0.008` (l.190, l.238) | `0.990 / 0.008` | `0.99 / 0.008164965809277286` | SUPPORTED |
| 9 | mitigation none `0.963 +- 0.024` (l.190) | `0.963 / 0.024` | `0.9633333333333333 / 0.02449489742783178` | SUPPORTED |
| 10 | readout improves `2.8%` over unmitigated (l.190, l.239) | `+2.8%` | `(0.99 - 0.9633333333333333)/0.9633333333333333 = 2.77%` | SUPPORTED |
| 11 | ZNE `0.967 +- 0.015` (l.190) | `0.967 / 0.015` | `0.9666666666666666 / 0.014907119849998594` | SUPPORTED |
| 12 | both `0.970 +- 0.016` (l.190) | `0.970 / 0.016` | `0.97 / 0.01632993161855452` | SUPPORTED |
| 13 | "exact state-vector simulation of up to 14 qubits and 63 clauses" (abstract) | `n=14, m=63` | `scaling.n` max = `14`; `m = int(n*4.5) = 63` | SUPPORTED |

**This package has the highest L3 fidelity in the batch: 13 of 14 directly transcribed per-experiment numbers are correct to the stated precision, and the 14th (claim 2, the plateau) is a correct qualitative reading of the data.** Every mitigation number, every scaling number, and both depth SAT ratios check out.

### CONTRADICTED (11)

**D1 — the paper's WalkSAT baseline has three different values, and none is the artifact's pooled mean.**

- **Claimed, three places:**
  - abstract (l.22): "outperforming WalkSAT (**0.967**)"
  - results (l.150): "WalkSAT achieves **0.964** $\pm$ 0.042 on identical instances"
  - summary table (l.235): "WalkSAT baseline & SAT ratio & **0.967** & 0.042"
- **Actual, MEASURED from the artifact** over the 11 noise levels: `ws_m` = `[0.9722, 0.9639, 0.9139, 0.9694, 0.9639, 0.9667, 0.9500, 0.9722, 0.9556, 0.9722, 0.9111]`
  - **pooled mean = 0.9556**
  - median = 0.9639
  - sd(ddof=0) = 0.0214, sd(ddof=1) = 0.0224
  - mean of the per-level stds = 0.0424
- So `0.042` (the dispersion) **is** derivable from the artifact (as the mean of per-level stds), but neither `0.964` nor `0.967` is the pooled mean. `0.967` is close to the **median** (0.9639), and `0.964` equals one individual level's value (`ws_m[1] = ws_m[4] = 0.9639`).
- **Artifact path:** `quantum-k-sat-ieee-package/data/metrics.json` → `noise.ws_m`, `noise.ws_s`.
- **Verdict: CONTRADICTED.** Three different values for one baseline within one paper; the pooled mean in the artifact is 0.9556.

**D2 — the optimality gap is described as decreasing from 5.71 to 5.97; it increases.**

- **Claimed** (`main.tex:170`): "The optimality gap -- defined as the difference between achieved energy and the minimum possible energy -- **decreases marginally from 5.71 at $p=1$ to 5.97 at $p=4$**."
- **Actual:** `depth.gap` = `[5.707474586657542, 6.680373038766503, 6.240937119889088, 5.96937077649221]`
  - `5.71 -> 5.97` is an **increase of 0.26**, not a decrease
  - the series is non-monotonic: it jumps to **6.68 at p=2**, the worst value in the sweep
- This is a plain arithmetic inversion, and it is load-bearing: the sentence is the paper's entire justification for concluding that deeper circuits are unnecessary.
- **Artifact path:** `data/metrics.json` → `depth.gap`.
- **Verdict: CONTRADICTED.** Claimed a decrease 5.71 -> 5.97; actual 5.7075 -> 5.9694, an increase, with a larger excursion to 6.6804 at p=2.

**D3 — the abstract claims deeper circuits provide marginal benefit; the artifact shows depth provides negative benefit.**

- **Claimed** (abstract, l.22): "We further analyze the effect of circuit depth and problem scaling, finding that **deeper circuits ($p>2$) provide marginal benefit** for instances of this size."
- **Actual:** on **both** reported metrics, `p = 1` is the best depth in the sweep.
  - SAT ratio: `p=1` gives `0.9833`; `p=2,3,4` all give `0.9667` — **depth reduces SAT ratio**
  - optimality gap: `p=1` gives `5.7075` (best); `p=2,3,4` give `6.6804, 6.2409, 5.9694` — **all worse**
- "Marginal benefit" is contradicted; the artifact shows a consistent **penalty** of about 0.017 SAT ratio and 0.26-0.97 gap.
- **Artifact path:** `data/metrics.json` → `depth.sat`, `depth.gap`.
- **Verdict: CONTRADICTED.**

**D4 — "on identical instances" is false, and the two arms cannot be paired.**

- **Claimed** (`main.tex:150`): "WalkSAT achieves 0.964 $\pm$ 0.042 **on identical instances**". And `main.tex:200`: "we performed a **paired** $t$-test on the noise experiment results. Across 11 noise levels with 6 trials each..."
- **Actual, verified by the auditor** by instrumenting `gen_3sat`: the QAOA arm and the WalkSAT arm call `gen_3sat(n, m)` in **two separate loops** (`quantum_k_sat_simulator.py:119-126`). The first six instances go to QAOA, six different instances go to WalkSAT. MEASURED comparison of the two instance sets: `QAOA instance set == WalkSAT instance set → False`. First clauses differ: QAOA `(((0,1),(9,-1),(10,-1)), ...)`, WalkSAT `(((1,-1),(2,1),(5,-1)), ...)`.
- A paired t-test requires paired observations on the same instances. **There is no pairing.** The correct test is unpaired.
- **Artifact path:** `data/metrics.json` stores only per-level means and standard deviations; the per-trial values needed to run any test are not committed, so the claimed test is not reproducible from the package in any form.
- **Verdict: CONTRADICTED.** "Identical instances" is false at the code level, and the paired-test framing is impossible.

**D5 — the significance statistics and effect size do not match the artifact.**

- **Claimed** (`main.tex:200`): "QAOA's mean SAT ratio (**0.979 $\pm$ 0.009**) exceeds WalkSAT's (**0.954 $\pm$ 0.029**) with $p < 0.001$ ... The effect size (**Cohen's $d = 1.14$**)."
- **Actual, MEASURED** — every pooled statistic derivable from the artifact:

| statistic | artifact | paper |
|---|---|---|
| QAOA pooled mean | `0.9798` | `0.979` (close) |
| QAOA dispersion | sd `0.0052` (ddof=0), `0.0054` (ddof=1) | `0.009` — **matches nothing** |
| WalkSAT pooled mean | `0.9556` | `0.954` (close) |
| WalkSAT dispersion | sd `0.0214` (ddof=0), `0.0224` (ddof=1) | `0.029` — **matches nothing** |
| mean of per-level stds | QAOA `0.0141`, WalkSAT `0.0424` | `0.009` / `0.029` — **matches neither** |
| Cohen's $d$ from artifact | **1.558** | `1.14` |
| Cohen's $d$ from the paper's own $\pm$ values | **1.164** | `1.14` |

- The paper is **internally** self-consistent: `1.14` follows from its own `0.009`/`0.029` pair. It is **externally** inconsistent with the artifact, from which the same calculation gives `1.56`.
- The per-trial data needed to reproduce any $t$-test is not committed (see D4).
- **Artifact path:** `data/metrics.json` → `noise.qaoa_m`, `noise.qaoa_s`, `noise.ws_m`, `noise.ws_s`.
- **Verdict: CONTRADICTED.** Claimed `d = 1.14`; artifact gives `d = 1.558`. Claimed dispersions match no statistic the artifact supports.

**D6 — the QAOA/WalkSAT gap is claimed to be constant at 2-3%; it ranges from 0.44 to 2.22 points.**

- **Claimed** (`main.tex:160`): "The performance gap between QAOA and WalkSAT **remains approximately constant at 2--3\%**, suggesting that the advantage persists as problem size grows."
- **Actual, MEASURED** from `scaling` (percentage points):

| n | QAOA | WalkSAT | gap |
|---|---|---|---|
| 8 | `0.9944` | `0.9722` | **2.22** |
| 10 | `0.9733` | `0.9689` | **0.44** |
| 12 | `0.9852` | `0.9741` | **1.11** |
| 14 | `0.9810` | `0.9587` | **2.22** |

- The gap is neither constant nor in the 2-3% band: it spans 0.44-2.22 points, a 5x range, and the paper's own lower bound of 2% is exceeded at only 2 of 4 sizes.
- **Artifact path:** `data/metrics.json` → `scaling.qaoa_m`, `scaling.ws_m`.
- **Verdict: CONTRADICTED.** Claimed constant at 2-3%; actual 0.44-2.22 percentage points.

**D7 — the random baseline "degrades" by an amount smaller than its own stated uncertainty, and at a constant clause ratio.**

- **Claimed** (`main.tex:160`): "Random sampling **degrades from 0.877 at $n=8$ to 0.874 at $n=14$, confirming increasing instance hardness at higher clause-to-variable ratios**."
- **Actual, two problems:**
  1. **The clause-to-variable ratio is constant by construction.** `exp_scaling` sets `m = int(n * 4.5)` (l.142), and the figure title confirms "clause ratio=4.5". The ratio is `4.5` at `n=8` and `4.5` at `n=14`. It does not increase, so the stated explanation cannot apply.
  2. **The change is smaller than the artifact's own noise.** The observed move is `0.8767 -> 0.8741`, i.e. `0.0026`, against a dispersion of the same quantity of `sd = 0.0042` — and the paper itself quotes `0.876 +- 0.005` at l.236. The "degradation" is about half of one standard deviation, and `rand_m` across the noise sweep wanders between `0.869` and `0.885` with no trend, because it is a 100-draw Monte Carlo estimate recomputed independently at every level.
- **Artifact path:** `data/metrics.json` → `scaling.rand_m`, `noise.rand_m`.
- **Verdict: CONTRADICTED.** Claimed a trend at increasing clause ratio; the ratio is fixed and the change is sub-noise.

**D8 — the noise channel is labelled "depolarizing" and is neither depolarizing nor a physical channel.**

- **Claimed:** abstract "evaluate QAOA performance under **depolarizing noise**"; Fig. 1 x-axis "**Depolarizing Noise Rate**"; Fig. 1 title "QAOA vs Noise".
- **Actual** (`quantum_k_sat_simulator.py:57`), the entire noise model is one line:
  ```python
  state = (1-noise)*state + noise*np.ones(N,complex)/N
  ```
  - The replacement vector is `np.ones(N)/N`, i.e. the all-ones direction `|11...1>` scaled by `1/N`. The depolarizing channel replaces $\rho$ with $(1-p)\rho + p\,I/2^n$, which acts **along $|\psi\rangle$ itself** (MEASURED: `p*(I/16)|psi> = 0.00781` for every amplitude, versus the code's `0.03125` added along `|11..1>`). The code therefore injects a **coherent bias toward the all-ones bitstring**, not random bit flips.
  - It is **not norm-preserving.** MEASURED: at `noise = 0.5` on a normalised state, `||out||^2 = 0.390625`. A physical channel has `||out||^2 = 1`. The non-unitarity is hidden because `best_sat_from_state` does `probs /= probs.sum()` (l.71), renormalising away the defect.
  - The code is therefore systematically biased in a fixed direction, which is why the noise axis produces a **flat plateau** rather than degradation.
- **Artifact path:** `data/metrics.json` → `noise.noise`, `noise.qaoa_m`; generator `quantum_k_sat_simulator.py:57`.
- **Verdict: CONTRADICTED.** The axis is labelled depolarizing noise; a non-norm-preserving coherent admixture of `|11...1>` is implemented.

**D9 — ZNE and readout calibration are not implemented; they are scalar noise reductions.**

- **Claimed:** "assess noise mitigation strategies"; "**Readout error calibration** yields the most effective noise mitigation, improving performance by 2.8%"; §"Noise mitigation" compares "four noise mitigation strategies"; `main.tex:190` interprets the result as showing "measurement errors dominate over gate errors for shallow-depth QAOA circuits".
- **Actual** (`quantum_k_sat_simulator.py:179`): the entire mitigation experiment is a lookup table of noise multipliers:
  ```python
  factors = {'none':0.15, 'zne':0.15*0.3, 'readout':0.15*0.5, 'both':0.15*0.15}
  ```
  There is **no zero-noise extrapolation** (no noise scaling, no extrapolation fit) and **no readout-error calibration** (no calibration matrix, no confusion matrix, no mitigation circuit). "ZNE" is defined as *using 30% less noise*; "readout" as *using 50% less noise*.
- **This is circular validation in the `isac` pattern the audit brief asked about.** The figure demonstrates that reducing the noise parameter improves performance. It cannot demonstrate that ZNE or readout calibration reduce noise, because the reduction is the definition rather than the result. The paper's mechanistic conclusion — that measurement errors dominate gate errors — is drawn from a table of assumed multipliers and has no support in the code.
- **Artifact path:** `data/metrics.json` → `mitigation.m`, `mitigation.std`; generator `quantum_k_sat_simulator.py:174-193`.
- **Verdict: CONTRADICTED.** Claimed four mitigation strategies; two scalar multipliers are implemented and the strategies themselves do not exist.

**D10 — QAOA's reported score comes from a top-10 amplitude oracle that WalkSAT does not get.**

- **Claimed:** "QAOA ... outperforming WalkSAT"; "QAOA's mean SAT ratio ... exceeds WalkSAT's".
- **Actual:** `best_sat_from_state` (l.69-77) reads `probs = |state|^2`, sorts, takes `top = np.argsort(probs)[-10:]`, computes the SAT ratio of each of the ten most probable bitstrings **at full amplitude precision**, and returns `max(...)`. This is an oracle over the ten most likely outcomes, with no shot noise, no finite sample, and no cost. `walk_sat` (l.79-96) performs 2000 genuine random flips and returns early only if it actually finds a solution.
- The comparison is therefore best-of-10-exact-amplitudes against best-of-2000-actual-search. **The QAOA side is evaluated under conditions no quantum device could reproduce** — a real device samples bitstrings with probability `|psi_i|^2`, and getting the argmax of 10 outcomes reliably requires far more shots than 10.
- The gap between the reported SAT ratio and the energy the circuit actually achieves makes the size of the oracle measurable: the reported `0.9833` corresponds to 1 violated clause out of 60, while the optimality gap of `5.71` means the state's **expected** number of violated clauses is `5.71`. The best-of-10 readout accounts for roughly 4.7 of those 5.71 clauses.
- **Artifact path:** `data/metrics.json` → `depth.sat` and `depth.gap` read together; generator `quantum_k_sat_simulator.py:69-77`.
- **Verdict: CONTRADICTED.**

**D11 — `rand_m` is computed on a leaked loop variable and is not a stable baseline.**

- **Claimed:** "random sampling reaches only 0.876 $\pm$ 0.005", used as the reference floor in Figs. 1 and 2.
- **Actual** (`quantum_k_sat_simulator.py:127`): `rs = np.mean([sat_ratio(np.random.randint(0,2,n), cl) for _ in range(100)])` is inside the noise loop but **outside** both instance loops, so `cl` is whatever the last `gen_3sat` call left behind — the sixth WalkSAT instance, reused at every noise level. It is a single 100-draw Monte Carlo recomputed per level, not a property of the noise sweep, which is why `rand_m` wanders over `0.869-0.885` with no trend while being plotted as a flat reference line. It also **consumes the global RNG**, perturbing the QAOA random search that follows.
- For a genuinely random assignment the SAT ratio is analytically `1-(1-2^{-3})^{m} = 1-0.875^60 = 0.99957` for the ratio the code uses, and a fixed function of `n` and `m`; it does not vary with any noise level at all.
- **Artifact path:** `data/metrics.json` → `noise.rand_m`, `scaling.rand_m`.
- **Verdict: CONTRADICTED.** Recorded as a minor finding; the reported 0.876 value is numerically right, so the transcription is sound and only the baseline's construction is defective.

### UNSUPPORTED (1)

**U1 — the below-median instance-hardness analysis has no committed data behind it.**

- **Claimed** (`main.tex:202`): "For instances where WalkSAT achieves below-median performance (SAT ratio $< 0.96$), QAOA's advantage increases to **4.3%**, suggesting that QAOA is particularly beneficial for harder instances where classical local search struggles."
- **Actual:** `data/metrics.json` stores, per noise level, only the **mean** and **standard deviation** of 6 QAOA runs and 6 WalkSAT runs. **No per-instance value is committed.** A conditional analysis split at the median of per-instance WalkSAT performance cannot be reconstructed from means and standard deviations, and the per-trial data does not exist in the package. The number 4.3% appears nowhere in the artifact.
- Note also that the QAOA and WalkSAT arms ran on **different instances** (D4), so a per-instance pairing the analysis presupposes does not exist even in memory, let alone on disk.
- **Artifact path:** `data/metrics.json` — no field supports this claim.
- **Verdict: UNSUPPORTED.**

### L3 count note

Itemised: **13 SUPPORTED, 11 CONTRADICTED, 1 UNSUPPORTED, total 25.** The machine-readable row matches.

## L4 — figures

**Verdict: SUPPORTED.** This is the one clean L4 in the batch, and it is recorded as such deliberately.

All 4 committed figures have committed generators in `quantum_k_sat_simulator.py`, all 4 generators ran as part of the exit-0 execution, and all 4 were rewritten. Each was inspected visually against `data/metrics.json`:

- **`fig1_noise_vs_performance.png`** — error bars for QAOA (`qaoa_m`, `qaoa_s`) and WalkSAT (`ws_m`, `ws_s`), a dotted Random line (`rand_m`), a grey reference at 1.0, y-limits 0-1.1. Plotted values match the artifact exactly. Correct.
- **`fig2_scaling.png`** — three series over `n = [8,10,12,14]`. Matches `scaling` exactly. Correct.
- **`fig3_depth_analysis.png`** — twin axes: SAT ratio left, optimality gap right. **The figure visibly contradicts the prose** (D2/D3): SAT ratio steps *down* from p=1 and stays flat at p=2,3,4; the gap rises from p=1 to a maximum at p=2 then declines. The generator is faithful; it is the caption and text that are wrong. This is a well-built figure that refutes its own paper, which is a point in the generator's favour and against the text.
- **`fig4_noise_mitigation.png`** — four bars with value labels and error bars, matching `mitigation.m` and `mitigation.std` exactly, y-limit 0-1.2. Correct as a plot. Its **content** is circular (D9) but the figure faithfully renders the artifact, so L4 is clean while L5 is contradicted.

The 5.4-6.5% pixel deltas against the committed PNGs (identical dimensions, `max_channel_delta=255`) were verified to be matplotlib 3.11 font/antialiasing, not data: the underlying numbers are bit-identical and the plots are visually equivalent. **All 4 of 4 figures are sound, and this is the only package in the batch where that is true.**

## L5 — method

**Verdict: CONTRADICTED.**

Four methods are described; the code implements none of them as described.

**M1 — "QAOA" is random search.** `optimize_qaoa` (l.98-110) samples `g, b ~ U(0, pi)` `iters` times (30-40 depending on the experiment) and keeps the lowest energy. No gradient, no parameter-shift rule, no classical inner optimiser, no warm start, no convergence criterion. For `p = 2` this is 30 random points in a 4-dimensional space.

**M2 — the mixer is not a QAOA mixer.** `mixer` (l.34-43) applies a cascade of two-level unitaries `[[c, -i s], [-i s, c]]` over bit-flip pairs. The auditor **verified it is unitary** (MEASURED `||out||^2 = 1.000000000000` at `gamma = 0.0, 0.3, 0.9`) — so this is a valid Hamiltonian evolution and **not** a defect. It is simply not `exp(-i*gamma*sum_j X_j)`, and the paper describes it as a QAOA ansatz without stating the deviation. Recorded as a description gap, not a bug.

**M3 — the noise channel is not depolarizing and is not physical** (D8). `||out||^2 = 0.390625` at `noise = 0.5`, renormalised away at read-out.

**M4 — the mitigation strategies are not implemented** (D9). ZNE and readout calibration are entries in a scalar multiplier table. This is the circular-validation case the brief asked about: **a method validated against an effect its own definition assumes.**

**M5 — the readout is an oracle** (D10). Top-10 exact amplitudes, maximum taken. No measurement, no shots, no sampling.

**No C kernel in this package.** The prior sweep's claim that all `*_kernel.c` files in this account are dead code does not apply here because there is no such file; `quantum-k-sat-ieee-package` is the only one of the four with no C artifact at all.

## L6 — selection

**Verdict: SUPPORTED.**

No undeclared selection of seed, trial, instance or best case was found, and this package is the cleanest on this layer in the batch:
- The seed is fixed once at module level (`np.random.seed(42)`, l.12) and the full distribution is reported: 6 instances per noise level for both arms, with standard deviations in the artifact and error bars in the figures.
- `exp_depth` generates **one instance shared across all four depths** (l.163, outside the `for p` loop) — the correct experimental design for a depth comparison, and better than the noise and scaling experiments.
- Mitigation reports `std` over 5 instances per strategy, not a best case.
- The random baseline is a full 100-draw estimate, not a selected draw.

The `cd`-class zero-variance problem is absent: `qaoa_m` varies over `0.9722-0.9861` and `ws_m` over `0.9111-0.9722`, so a significance test is at least meaningful in principle. (The tests the paper reports still fail, D4/D5, but the underlying data supports a test existing.)

## L7 — internal consistency

**Verdict: CONTRADICTED.**

- **`main.tex:170` says the gap "decreases ... from 5.71 at p=1 to 5.97 at p=4"** (D2) — an arithmetic inversion in the same sentence that carries the paper's depth conclusion. **Fig. 3, in the same paper, shows the opposite**, with the gap rising. Figure and prose describe different trends.
- **Abstract says deeper circuits give "marginal benefit"** (D3); Table and Fig. 3 show p=1 is best on both metrics.
- **Abstract says WalkSAT is `0.967`, §Results says `0.964`, Table says `0.967`** (D1) — three values for one baseline in one paper.
- **`main.tex:150` says WalkSAT runs "on identical instances" and `main.tex:200` reports a "paired" t-test** (D4); the code runs them on different instances, so neither statement can hold.
- **`main.tex:200`'s `0.009`/`0.029` and `d = 1.14`** (D5) are mutually consistent and inconsistent with the artifact's `0.0052`/`0.0214` and `d = 1.558`.
- **Fig. 1's x-axis reads "Depolarizing Noise Rate"** (D8) and Fig. 4's title reads "Noise Mitigation" (D9), neither of which names what the code does.

Consistent across the paper: every per-experiment mean and standard deviation transcribed into Tables and text (claims 1-13) matches the artifact, and the noise plateau reading is a correct qualitative description of Fig. 1.

## L8 — verdict

**PARTIALLY SUPPORTED.** The artifact-to-claim correspondence is the best in the batch: 13 of 14 transcribed numbers correct, the plateau claim correct, and the only clean L4. The paper's central mechanisms are contradicted: the noise channel is not depolarizing and is not physical, the two named mitigation techniques are scalar multipliers, the parameters are random-searched rather than variationally optimized, the readout is a top-10 oracle, the two arms are not paired, and the optimality-gap trend is stated backwards.

## What survived as SUPPORTED (quantum-k-sat)

Explicitly and prominently, per R7 — this package has the most to survive:

1. **All 4 of 4 figures have committed generators, all ran, all match their data.** The only clean L4 in the batch.
2. **13 of 14 directly transcribed numerical claims are correct**, including all four mitigation results with their error bars, all four scaling points quoted, and the noise-sweep endpoint pair (`0.981 +- 0.011` and `0.983 +- 0.017`, both exact).
3. **The noise-plateau claim is correct and correctly interpreted**: "maintains a mean SAT ratio above 0.97 across the full noise range, with no statistically significant degradation" — the minimum is `0.9722` and the paper does not overstate it.
4. **The depth experiment is well designed**: one instance shared across all four depths, which is the correct comparison, and the paper correctly reports both SAT ratios (`0.983` vs `0.967`).
5. **The 2.8% mitigation improvement is arithmetically correct** (2.77% measured).
6. **The random baseline value `0.876 +- 0.005` is correct** to the stated precision.
7. **The state-vector scope claim is accurate** — "up to 14 qubits and 63 clauses" matches `n=14`, `m=int(14*4.5)=63`.
8. **The mixer is genuinely unitary** (MEASURED), so no unitarity defect is claimed against it. This was checked and it passed.
9. **No seed, trial, or best-case selection anywhere.** The best L6 in the batch.
10. **`metrics.json` reproduced bit-identical** on 98 of 102 numbers, with the 4 exceptions at 1-2 ULP in a field the paper reports to 2 decimals.

## Gaps a reviewer would reject quantum-k-sat over

1. The gap trend is stated backwards (5.71 -> 5.97 described as a decrease) and Fig. 3 shows the opposite.
2. The abstract claims deeper circuits give "marginal benefit"; the artifact shows p=1 is best on both metrics.
3. The noise channel is labelled depolarizing; it is a non-norm-preserving coherent admixture of `|11...1>`.
4. ZNE and readout calibration do not exist in the code; the mitigation figure is circular.
5. QAOA's score comes from a top-10 exact-amplitude oracle while WalkSAT does a real 2000-flip search.
6. The "paired" t-test is impossible — the two arms ran on different instances — and the reported dispersions and `d = 1.14` match no statistic in the artifact (`d = 1.558`).
7. One baseline is reported with three different values (0.964 / 0.967 / artifact 0.9556).
8. The "2-3% constant gap" ranges 0.44-2.22 points, and the random-baseline "degradation" is half a standard deviation at a clause ratio that never changes.

---

# 4. `sra` — Stochastic Resource Allocation for Distributed OS in Quantum Environments

**Repository:** `FernandoMay/sra-ieee-package` (HTTP 200; 29 tracked files; 1 commit, HEAD `d356b99`)
**Claimed topic (backlog):** event-driven stochastic scheduler, C kernel
**Evidence class:** E1, seeded simulation with `metrics.json` and figures

## Research question

Does scenario-based stochastic programming (sample average approximation) scheduling beat random and greedy load-balancing for a distributed OS serving a mix of classical and quantum-resource tasks, under stochastic arrivals and hardware noise?

**What "quantum" means here, concretely:** quantum tasks are **bookkeeping**. A task is marked quantum if `qubits > 0`; its error is computed in closed form as `1 - (1-depol_err)(1-decoh)` with `depol_err = 1-(1-gate_err)^gates` and `decoh = 1-exp(-ct/min(t1,t2))` (`sra_simulator.py:136-138`). No quantum state, no circuit, no simulation of a quantum computation. The quantum content is a noise model attached to a scheduler decision, which is a legitimate thing to study — but it is not quantum computing, and the paper does not claim it is.

## What was executed, with real output

`sra_simulator.py`, full run, **exit code 0**, 2.8 s. Real stdout, all 45 trials and the summary, verbatim for the summary:

```
  Scheduler       Makespan     Error      Drop     Imbalance
  Random          43.9         0.1572     0.046    0.0000
  Greedy          43.9         0.1459     0.049    0.0000
  Stochastic      43.9         0.1338     0.047    0.0000
```

Plus the C kernel (**exit 0**) and one auditor-designed controlled experiment that pins the hardware noise draw across all three arms.

## L3 — every numerical claim, both values, artifact path

**Artifact path for this entire package: `sra-ieee-package/figures/metrics.json`.**

### SUPPORTED (9)

| # | Claim (source) | Claimed | Artifact value | Verdict |
|---|---|---|---|---|
| 1 | Table, Random row (l.185) | `43.9 / 0.1572 / 0.046` | mean makespan `43.9188`, mean `avg_error` `0.1572...`, mean `drop_rate` `0.0463` | SUPPORTED |
| 2 | Table, Greedy row (l.186) | `43.9 / 0.1459 / 0.049` | `43.9188 / 0.1459... / 0.0488` | SUPPORTED |
| 3 | Table, Stochastic row (l.187) | `43.9 / 0.1338 / 0.047` | `43.9188 / 0.1338... / 0.0466` | SUPPORTED |
| 4 | "15 Monte Carlo trials" (l.158) | `15` | 15 trials per arm, 45 rows in the artifact | SUPPORTED |
| 5 | "80 tasks across 6 nodes (3 with QPU)" (abstract) | `80 / 6 / 3` | `N_TASKS=80`, `N_NODES=6`, `qubits=[16,8,4,0,0,0]` | SUPPORTED |
| 6 | "Makespan invariance: scheduling policy has minimal impact on completion time" (l.238) | minimal impact | makespan **identical to full float precision in all 15 trials** across all three arms | SUPPORTED (and disclosed — see below) |
| 7 | "Quantum operations incur depolarising noise and decoherence, modelled as functions of gate count and execution time" (abstract) | gate count + time | `depol_err = 1-(1-gate_err)^gates`; `decoh = 1-exp(-ct/min(t1,t2))` | SUPPORTED |
| 8 | "pq = 0.35, qubits [1,8], depth [5,50], gates [d,4d]" (l.87) | as stated | `rng.random()<0.35`, `rng.integers(1,9)`, `rng.integers(5,50)`, `rng.integers(dp,4*dp)` | SUPPORTED |
| 9 | "K = 15 perturbed scenarios ... multiplicative noise (±20%)" (l.135) | `K=15`, `±20%` | `K=15`; `f_cpu = max(0.8, 1+0.15*normal())`, `f_q = max(0.8, 1+0.2*normal())` | SUPPORTED (CPU factor is ±15%, floored at 0.8) |

**Claim 6 is worth its own note, because the paper is honest about it.** `main.tex:238` states plainly: "**Makespan invariance:** In a well-provisioned system, scheduling policy has minimal impact on completion time. The benefits of stochastic allocation manifest through improved execution quality (lower error) rather than throughput." The artifact shows makespan is *bit-identical* across arms, and the paper acknowledges that throughput is not where the win is. That is a correct report of a negative result and it deserves credit.

### CONTRADICTED (5)

**D1 — the headline 14.9% error reduction is confounded by a hardware draw that differs between arms; controlled, it is 6.5%.**

This is the central finding of the package, and it required a controlled experiment to establish.

- **Claimed** (abstract, l.42; contributions l.67; results l.193; conclusion l.257): "the stochastic scheduler **reduces average quantum error by 14.9%** compared to random scheduling (0.134 vs. 0.157)", and "8.3% relative to greedy".
- **The transcription is correct.** MEASURED from the artifact: `(0.1572 - 0.1338)/0.1572 = 14.89%`; `(0.1459 - 0.1338)/0.1459 = 8.29%`.
- **The comparison is not sound, because the three arms are not evaluated on the same hardware.** Node noise parameters are drawn in `Node.__init__` (l.110-112) from a **module-level `rng`** that is also advanced by `RandomScheduler.select_node` and `StochasticScheduler.perturb`, and **is never reset between the three arms in `main()`**. Each arm therefore receives a *different* draw of per-node `gate_err`, `t1`, `t2`.
- **MEASURED** (auditor instrumented the arm sequence exactly as `main()` executes it):

| arm | per-node `gate_err` (milli-units) |
|---|---|
| Random | `[0.553, 0.492, 1.568, 1.320, 1.318, 1.170]` |
| Greedy | `[0.721, 0.523, 1.051, 0.731, 1.219, 1.055]` |
| Stochastic | `[1.626, 1.314, **0.430**, 0.509, 0.948, 0.829]` |

  Quantum tasks can only be placed on nodes 0-2 (`qubits = [16,8,4,0,0,0]`), and the stochastic scheduler's cost function is `alpha*makespan_norm + beta*err` with `beta = 0.5`, i.e. it prefers low-error nodes. **The Stochastic arm happened to draw node 2 with `gate_err = 0.430e-3`, the best of the three arms** (vs `1.568e-3` for Random, `1.051e-3` for Greedy). It was handed the best quantum hardware.
- **The decisive controlled re-test.** The auditor wrote a variant that pins the hardware draw per trial and shares it across all three arms, leaving everything else identical (task stream, scheduler logic, cost function, 15 trials). Real output:

```
  hardware identical across arms: True
  arm           makespan   avg_error     drop
  Random         43.8787      0.1546   0.0458
  Greedy         43.8787      0.1524   0.0492
  Stochastic     43.8787      0.1446   0.0475

  CONTROLLED reduction vs random :  6.47%   (paper claims 14.9%)
  CONTROLLED reduction vs greedy :  5.07%   (paper claims  8.3%)
  paired t-test Random - Stochastic : mean diff=+0.01000  t=+3.378  p=0.0045
  paired t-test Greedy - Stochastic : mean diff=+0.00773  t=+3.516  p=0.0034
```

- **Conclusion, stated fairly: the effect is real but overstated by a factor of about 2.3x.** With hardware controlled the Stochastic scheduler still wins, and the win is statistically significant on a properly paired test (`p = 0.0045` vs random, `p = 0.0034` vs greedy). **Roughly 57% of the headline 14.9% is attributable to the confounded hardware draw rather than to the scheduling policy.** The paper's number is not fabricated; it is the right arithmetic on an uncontrolled comparison.
- **Artifact paths:** `sra-ieee-package/figures/metrics.json` (the reported values); `sra_simulator.py:36,110-112,180,205-206` (the coupling).
- **Verdict: CONTRADICTED.** Claimed 14.9% (8.3%); measured under controlled hardware 6.47% (5.07%).

**D2 — the noise-sensitivity analysis contains no comparison and cannot respond to its own swept parameter.**

- **Claimed** (abstract, l.42): "A noise sensitivity analysis **confirms that stochastic optimisation becomes increasingly beneficial as gate error rates exceed $10^{-3}$**." Results (l.208): "Figure 4 shows makespan and drop rate as functions of gate error rate. For $\epsilon_g < 5 \times 10^{-4}$, noise is negligible and **all schedulers perform equivalently**. As $\epsilon_g$ increases beyond $10^{-3}$, quantum tasks incur significant errors, and **the stochastic scheduler's advantage becomes more pronounced**." Conclusion (l.257): "A noise sensitivity analysis confirms that the benefit of stochastic optimisation increases with hardware error rates."
- **Actual, from the generator** (`sra_simulator.py:403-414`): the sweep runs **only the Stochastic scheduler**.
  ```python
  for err in errs:
      GATE_ERR = err
      res = run_simulation(StochasticScheduler, CAPS, tasks, K=10)
      makespans.append(res['makespan']); drops.append(res['drop_rate'])
  ```
  **There is no Random arm and no Greedy arm in the sweep.** A statement about one arm's "advantage" over other schedulers cannot be supported by an experiment containing one arm.
- **Worse, the two plotted quantities are mathematically independent of `GATE_ERR`.** `GATE_ERR` enters only `Node.gate_err` (l.112), which reaches only `depol_err` -> `task.error` (l.136-138). It never touches `task.compute_time` (l.132-134) or `Node.can_run` (l.121-127). Since `makespan = max(t.finish)` and `drop_rate = 1 - len(scheduled)/len(tasks)`, **both are provably invariant under the swept parameter.** The figure is two flat lines, and the auditor confirms this in the committed image: makespan constant at 43.9 and drop rate constant at 0.0375 across four orders of magnitude of gate error, on y-axes autoscaled to 41.5-46.2 and 0.0355-0.0395 to disguise the absence of variation.
- **Artifact paths:** `sra-ieee-package/figures/fig_noise_sensitivity.png`; generator `sra_simulator.py:403-414`; the claim appears three times in `main.tex` (l.42, l.208, l.257) plus `main.tex:239` ("The advantage of stochastic scheduling grows with hardware noise").
- **Verdict: CONTRADICTED.** Four claim sites; the experiment contains one arm and two metrics that cannot depend on the swept variable.

**D3 — the C reference kernel reports a different result, and unlike the Python it does not show makespan invariance.**

- **Claimed** (`README.md:19`, `README.md:48-49`; `main.tex:166`): `sra_kernel.c` "provides an independent reference implementation", and the README instructs the reader to compile and run it.
- **Actual, MEASURED by executing it (exit 0):**

| scheduler | C kernel makespan / error / drop | Python `metrics.json` makespan / error / drop |
|---|---|---|
| Random | `44.0 / 0.1419 / 0.049` | `43.9 / 0.1572 / 0.046` |
| Greedy | `44.0 / 0.1414 / 0.047` | `43.9 / 0.1459 / 0.049` |
| Stochastic | **`44.2`** / 0.1415 / 0.047 | **`43.9`** / 0.1338 / 0.047 |

- Two things follow. First, the C implementation's three error rates are nearly identical (`0.1419 / 0.1414 / 0.1415`) and show **no scheduler advantage at all**, where the Python shows a monotone 15% spread. So the C reference implementation does not corroborate the paper's only positive result. Second, the C kernel's Stochastic makespan **differs** from Random and Greedy (`44.2` vs `44.0`), while the Python's is bit-identical across all three — i.e. the two implementations disagree about the very invariance the paper highlights at `main.tex:238`.
- **Artifact paths:** `sra-ieee-package/sra_kernel.c` vs `sra-ieee-package/figures/metrics.json`.
- **Verdict: CONTRADICTED.**

**D4 — `load_imbalance` is a dead metric reported as a result: it is exactly 0.0 in all 45 rows.**

- **Claimed:** `main.tex:191` includes a load-imbalance column in the metrics table, and Fig. 3 panel 4 is titled "Load Imbalance" with y-label `CV(Util)`.
- **Actual, MEASURED:** `load_imbalance` is **`0.0` in every one of the 45 rows** of `figures/metrics.json`, and the reproduced run prints `0.0000` for all three arms. The generator computes it at l.287-289 as `std(cpu_utils)/mean(cpu_utils)` **after** the drain loop (l.275-278) has called `Node.release()` on every task, setting `cpu_used` back to 0 on all six nodes. The metric is therefore `0/1e-6 = 0.0` identically, by construction, for any input whatsoever.
- Visual inspection of the committed `fig_metrics_comparison.png` confirms panel 4 is **three zero-height bars** on an otherwise empty axis running from -0.04 to +0.05.
- The paper's contribution list and results present load balance as one of four evaluated metrics, and the figure is given a full panel, but the quantity has no variance because it is measured at the wrong moment (end of simulation, after everything is released) rather than as a time average. The code comment at l.286 says "Load balance (**average over time**)" — the averaging it describes is not implemented.
- **Artifact path:** `sra-ieee-package/figures/metrics.json` → `load_imbalance: 0.0` in all 45 entries; generator `sra_simulator.py:286-289`.
- **Verdict: CONTRADICTED.**

**D5 — the makespan metric cannot discriminate between schedulers, and the paper attributes the invariance to the wrong cause.**

- **Claimed** (`main.tex:238`): "**Makespan invariance:** In a well-provisioned system, scheduling policy has minimal impact on completion time."
- **Actual, MEASURED:** the invariance is not a property of a well-provisioned system; it is **structural**. `Node.assign` (l.130-143) computes `ct = max(1.0, task.cpu*0.5 + task.mem*0.3)` from the task's own resources, and for quantum tasks adds `task.depth*T_GATE + task.gates*0.01` — **none of which depends on which node was chosen.** `makespan = max(t.finish for t in scheduled)` (l.281). So the makespan is a function of the task stream and arrival times only, and is mathematically incapable of varying with the scheduler.
- The consequence is visible in the artifact: makespan is **bit-identical in all 15 trials across all three arms** (`42.75059955394407`, `42.69526977096482`, `43.32567247913578`, ... each appearing three times in the 45 rows), and panel 1 of `fig_metrics_comparison.png` shows **three identical bars at 43.9**.
- The claim as stated ("minimal impact") is true, and the paper discloses it, so it is graded SUPPORTED above as a *claim*. It is recorded here because the **explanation** — "in a well-provisioned system" — is falsified: the system could be arbitrarily over-provisioned or under-provisioned and the makespan would still be identical, because the scheduler cannot influence it. A reader would draw a false conclusion about the system, and Fig. 3 panel 1 is presented as a measured comparison of completion time.
- **Artifact path:** `sra-ieee-package/figures/metrics.json` (15 identical makespan triples); generator `sra_simulator.py:132-134,281`.
- **Verdict: CONTRADICTED** (on the stated cause and on the figure's presentation, not on the direction of the effect).

### L3 count note

Itemised: **9 SUPPORTED, 5 CONTRADICTED, 0 UNSUPPORTED, total 14.** The machine-readable row matches. This is the only package in the batch with **zero** unsupported claims — every assertion in the paper either has an artifact behind it or is contradicted by one.

## L4 — figures

**Verdict: CONTRADICTED.**

All 8 committed figures have committed generators that ran and were rewritten. Two panels are defective.

**F1 — `fig_noise_sensitivity.png` plots two provably invariant quantities on autoscaled axes.** Covered in D2. The committed image shows makespan dead flat at 43.9 and drop rate dead flat at 0.0375, with y-axis limits (41.5-46.2 and 0.0355-0.0395) chosen by autoscale to make a constant fill the panel. Only one scheduler is present, so the figure cannot support a comparative claim even if the lines had varied.

**F2 — `fig_metrics_comparison.png` has two defective panels of four.** Panel 1 "Completion Time" shows **three identical bars at 43.9** (D5). Panel 4 "Load Imbalance" shows **three zero-height bars** on an empty axis (D4). Panels 2 and 3 are sound: panel 2's error bars for the three schedulers overlap substantially (Random spans roughly 0.135-0.179, Stochastic 0.106-0.161), and panel 3's drop rates are indistinguishable. The figure is faithful to the artifact — which is precisely the problem: **half of it displays quantities that carry no information.**

**F3 — Gantt and load figures are generated from a single visualisation run, not the 15-trial aggregate.** `plot_gantt` and `plot_load_evolution` are fed `res_viz`, produced by `run_simulation(..., seed=SEED)` — **trial 1 only** — while `figures/metrics.json` and Fig. 3 aggregate 15 trials. Recorded under R4 as a version-scope note: the Gantt charts illustrate one realisation while the table reports a distribution. The paper does not claim otherwise, and the Gantt itself is sound and informative (quantum tasks correctly appear only on the three QPU nodes, N0/N1/N2, with classical tasks spread across all six). Visual inspection confirms this is a good figure.

## L5 — method

**Verdict: CONTRADICTED.**

**M1 — the event-driven scheduler machinery is genuinely implemented and ran.** Tasks arrive stochastically, resources are checked, a heap-based completion queue releases capacity in time order, tasks that fit nowhere are dropped, and the three selection policies are distinct: Random draws uniformly, Greedy minimises `cpu_used/cap + mem_used/cap`, and Stochastic evaluates `K = 15` perturbed scenarios per candidate node under a weighted cost. **This is a real implementation of a real method** and the per-scenario scenario-based SAA is the most substantive algorithm in the whole batch. That is credited.

**M2 — the noise sensitivity method does not exist** (D2). The sweep is structurally incapable of showing what the paper says it shows.

**M3 — two of the four reported metrics cannot respond to scheduling** (D4, D5): `load_imbalance` is identically zero for any input, and `makespan` is invariant by construction. **Half the metric suite is inert.**

**M4 — the SAA scenario evaluation is real but its perturbation is not the stated one.** `perturb` (l.201-213) applies `f_cpu = max(0.8, 1+0.15*normal())` to `cpu` **and** `mem` from a single factor, and `f_q` to `depth` and `gates`. The paper (l.135) says "multiplicative noise (±20%) to task duration and quantum parameters"; the CPU/mem factor is ±15% with a hard 0.8 floor, which silently truncates the lower tail. Minor, and graded SUPPORTED above with the caveat recorded.

**Dead code, verified:** `sra_kernel.c` (322 lines) is referenced only by `README.md:19,48-49`, `main.tex:166`, `presentation.tex:169,176`. No Makefile, CMakeLists, or setup.py exists in any of the four packages; no Python file imports or `ctypes`-loads it. It compiles cleanly and runs, and **no result in the paper is produced by it** — and it disagrees with the paper's headline (D3).

## L6 — selection

**Verdict: CONTRADICTED.**

No best-case seed selection was found: the seed is fixed at 42, all 15 trials are in the artifact (45 rows, full distribution), and the arms are genuinely paired on the task stream (verified: the same seed yields an identical task stream, and every arm uses `seed = SEED + t` over the same `t` range).

The L6 failure is the **undeclared hardware-draw confound** (D1): each arm is evaluated on a different draw of per-node `gate_err`, `t1`, `t2`, and the Stochastic arm received the most favourable draw. The effect is larger than the reported effect — controlled, the headline falls from 14.9% to 6.47%. A reviewer would reject the 14.9% figure as a comparison against a moving baseline.

Recorded alongside, and in the paper's favour: `main.tex:238`'s makespan-invariance finding **is** a disclosed negative result, and the paper explicitly declines to claim a throughput win. That is the correct handling of a null result and is credited under L3 claim 6.

## L7 — internal consistency

**Verdict: CONTRADICTED.**

- **The abstract, the results, and the conclusion all repeat the noise-sensitivity conclusion (D2)** three times, and `main.tex:208` adds a second, more specific claim ("all schedulers perform equivalently") that the experiment cannot address. Four claim sites, no supporting data.
- **`main.tex:238` attributes makespan invariance to system provisioning; the code makes it structural** (D5). Fig. 3 panel 1 presents three identical bars as a measured comparison of completion time, and the paper never notes that the metric cannot vary.
- **The metrics table and Fig. 3 present `load_imbalance` as a result; it is 0.0 in all 45 rows and panel 4 is empty** (D4). The code comment at l.286 says "average over time"; no time averaging exists.
- **`main.tex:166` presents the C kernel as an independent reference; it reports no scheduler advantage in error** (D3), i.e. the reference implementation does not corroborate the paper's only positive claim.
- **The Gantt figures show trial 1 while the table shows 15 trials** (F3) — a minor R4 version-scope mismatch, not a contradiction.

Consistent across the paper: the entire results table, both percentage derivations, and the makespan-invariance claim all match the artifact and each other. This package has the most internally coherent *transcription* in the batch after quantum-k-sat; its defects are in what the experiments can show, not in how the numbers were copied.

## L8 — verdict

**PARTIALLY SUPPORTED.** `metrics.json` reproduced **bit-identically**, the results table matches the artifact to 4 significant figures, both percentage derivations are arithmetically correct, and the paper discloses a genuine negative result. But the single positive claim — a 14.9% error reduction — is measured against an uncontrolled baseline and falls to 6.47% when the hardware draw is held fixed, and the noise-sensitivity conclusion that appears four times is supported by an experiment with one arm and two metrics that cannot depend on the variable it sweeps.

## What survived as SUPPORTED (sra)

Explicitly and prominently, per R7:

1. **`figures/metrics.json` reproduced bit-identically** — all 45 rows, 5 fields, exact float equality. The most exact reproduction in the batch.
2. **All 9 cells of the results table** match the artifact to 4 significant figures.
3. **Both percentage derivations are arithmetically correct** as computed (14.89% and 8.29% from the reported means), and both were re-derived independently by the auditor.
4. **The makespan-invariance finding is correctly reported AND explicitly disclosed** at `main.tex:238`, with the paper correctly declining to claim a throughput win. A simulation paper reporting its own null result plainly is rare in this set and it is credited.
5. **The scenario-based SAA scheduler is a real, substantive implementation** — K = 15 perturbed scenarios per candidate node, with a genuine weighted-cost comparison. This is the most serious algorithmic content in the four packages.
6. **The task-generation model matches the paper's specification exactly** (35% quantum, qubits [1,8], depth [5,50], gates [d,4d]) — all four verified in code.
7. **The noise model matches the paper's description** — depolarising term in gate count plus a decoherence term in execution time, both present as described.
8. **The arms are genuinely paired on the task stream**, verified independently.
9. **The Gantt figures are informative and correct** — quantum tasks appear only on the three QPU-equipped nodes, classical tasks are spread, and the figure is legible.
10. **No seed, trial, or best-case selection anywhere**; the full 15-trial distribution is in the artifact.
11. **Zero unsupported claims** — the only package in the batch with none.

## Gaps a reviewer would reject sra over

1. The headline 14.9% is confounded by an uncontrolled hardware draw; controlled, it is 6.47% (a 2.3x overstatement). The effect survives but is half its claimed size.
2. The noise-sensitivity conclusion appears four times and is supported by an experiment containing **one** scheduler and two metrics that are mathematically invariant under the swept parameter.
3. `load_imbalance` is 0.0 in all 45 rows and panel 4 of the comparison figure is empty; half the metric suite is inert.
4. `makespan` cannot vary with the scheduler by construction, yet panel 1 presents three identical bars as a completion-time comparison, and the paper attributes the invariance to the wrong cause.
5. The C reference implementation reports no scheduler advantage in error and disagrees with the Python about makespan invariance.

---

# Cross-package findings

## Are these four really separate methods papers? (backlog's explicit question)

**Yes. They should stay separate, and merging them would be a serious error.** This was tested mechanically rather than assumed.

- **No shared results.** Exact-value overlap between the flattened numeric payloads of every pair: `ems`/`sra` 1 value, `ems`/`qce` 1, `ems`/`qks` 1, `sra`/`qce` 1, `sra`/`qks` 1, `qce`/`qks` 2 — out of 24-180 numbers per package. The overlapping values are structural constants (`0.0`, `1.0`, powers of two), not results. **There is no duplication of results between any pair.**
- **No shared artifacts.** Four separate repositories, four separate simulators, four separate result files (`ems/figures/`, `qce/figures/`, `sra/figures/`, `quantum-k-sat/data/`). No file is shared, no data is imported across packages, no figure appears twice.
- **Genuinely distinct methods.** RIS phased-array electromagnetics; online logistic regression plus exhaustive combinatorial search; classical state-vector QAOA simulation; event-driven sample-average-approximation scheduling. Four different literatures.

**What they do share is a template, not a result.** All four come from the same scaffold: `SEED = 42`; identical `matplotlib.rcParams` (serif, sizes 10/11/9, `figure.dpi=150`); the same `os.path.join(os.path.dirname(...), 'figures')` output convention; the same ASCII banner-plus-`====` progress format; the same "C reference kernel, unreferenced, never called, presented as verification" pattern (3 of 4); the same Chinese/English PDF pairing in 2 of 4. This is a stylistic fingerprint, worth flagging to whoever reviews the account, but it is **not** grounds for merging the papers.

## Are the C kernels called? (the prior sweep's claim, verified for these three)

**The prior sweep's finding is CONFIRMED and extended: all three kernels in these packages are dead code. But the sharper finding is that they are worse than dead — they compile, they run, and they contradict the published results.**

| kernel | lines | referenced by Python? | in a build system? | compiles? | runs? | agrees with the paper? |
|---|---|---|---|---|---|---|
| `ems_fdtd.c` | 245 | **no** | **no** | yes, clean | yes, exit 0 | **NO — reverses the ranking** |
| `qce_kernel.c` | 326 | **no** | **no** | yes, 1 warning | yes, exit 0 | **NO — reliability 1.0000 vs 0.924** |
| `sra_kernel.c` | 322 | **no** | **no** | yes, clean | yes, exit 0 | **NO — no scheduler advantage in error** |
| `quantum-k-sat` | — | — | — | — | — | **no C file exists in this package** |

Evidence for "dead": no Makefile, CMakeLists.txt, `setup.py`, or `*.mk` exists in **any** of the four packages (verified by find, excluding the auditor's own venv). No Python file in any repository imports, `ctypes`-loads, or `subprocess`-calls any of them. Each is referenced only by prose in `README.md` / `main.tex` / `presentation.tex` plus a manual `gcc` line.

The extension matters: because the READMEs instruct the reader to compile and run them, and `ems`'s `main.tex:153` calls one an "**independent reference kernel**", these are presented as corroboration. A reviewer who does what the README says will run three programs that **disagree with the papers** — in `ems`'s case reversing the headline conclusion. That is a sharper defect than unused code, and it is the finding the prior sweep could not have made without executing the kernels.

## What "quantum" means, concretely, in each package

| package | what runs | is it a quantum computation? |
|---|---|---|
| **quantum-k-sat** | Full classical state-vector simulation in NumPy: a `2^n` complex amplitude array propagated in classical memory (16,384 complex numbers at `n=14`). Non-standard hand-rolled unitary mixer. Parameters found by **random search** (`U(0,pi)` draws, 30-40 tries), not variational optimization. "Noise" is a **non-norm-preserving coherent admixture of `|11...1>`** (`||out||^2 = 0.39` at `p=0.5`), not depolarizing. "Measurement" is the **top-10 exact amplitudes with the best SAT ratio taken** — an oracle, not sampling. | **No.** A classical simulation of a QAOA-like circuit with a non-physical noise model and an oracle readout. The paper's own words ("exact state-vector simulation") are accurate; "on NISQ devices" in the repo title is not. |
| **qce** | A 5-qubit cost Hamiltonian is **constructed**, then **all 32 computational basis states are enumerated** and the lowest-diagonal-energy one is returned. `psi = |+>^n` is built and never used; the mixer `H_b` is built and never used; `self.params` (the variational angles) is initialised and never read. The "RL predictor" is 4-weight online logistic regression; `gamma = 0.9` is set and never used. | **No.** Exhaustive classical enumeration over 32 states, with the QAOA vocabulary retained. **The paper's Methods section says exactly this** (`main.tex:226`) and is accurate; the abstract, contributions, results and conclusion are not. |
| **sra** | Quantum tasks are **bookkeeping**: `is_quantum = qubits > 0`, with error `1-(1-depol)(1-decoh)` computed in closed form. No quantum state, no circuit. A real and correct resource-allocation problem with a noise model attached. | **No, and the paper does not pretend otherwise.** "Quantum" is used accurately — as a class of workload with stochastic noise characteristics, which is the legitimate framing. |
| **ems** | No quantum content at all. 8x8 RIS phased array, 6.5 GHz, Friis path loss, 30 dB wall, 64-element array factor, log-normal shadowing. | **No quantum content**, and none claimed. The one package in the batch whose title is not misleading. |

**Summary:** in all four packages, "quantum" denotes a classical computation. In `sra` and `ems` that is accurate and harmless. In `qce` it is accurate in the Methods and inaccurate in the abstract. In `quantum-k-sat` the repo title ("QAOA for K-SAT Optimization on NISQ Devices") overstates what ran, because the readout is an oracle no NISQ device can perform and the noise channel is not physical.

## Circular validation (the `isac` pattern, checked explicitly)

Checked in all four. **Found in one, and it is a textbook instance.**

- **quantum-k-sat — YES.** The mitigation experiment (D9) *defines* ZNE as `noise * 0.3` and readout calibration as `noise * 0.5`, then reports that they improve performance. The figure demonstrates that reducing a parameter improves the result. The paper's mechanistic conclusion — "measurement errors dominate over gate errors" — is drawn from an assumed multiplier table with no supporting computation. This is the same class as `isac` drawing estimator error from the CRLB it was tested against: **the validation target is defined by the method under test.**
- **quantum-k-sat, second instance (D10).** QAOA's score is the max over the 10 highest exact amplitudes while WalkSAT does a real 2000-flip search. The method is compared against a condition only the method could enjoy.
- **ems, sra, qce — NO.** No CRLB, no bound, and no oracle readout. The `cd`-class pattern of drawing error from the reference quantity does not appear.

## The `cd`-class phase-destruction defect (checked explicitly)

**Not found in any of the four.** Specifically checked for a per-sample random phase like `cd`'s `rng.uniform(0, 2*pi, n)`. `ems` reseeds the global legacy RNG inside its `diffuse` array-factor branch (`ems_simulator.py:88`), which is a real code smell — it clobbers global RNG state and makes the Monte Carlo's determinism an accident of call order rather than a design — but it produces a *fixed* random phase per element index, not a per-sample random phase, and it does not saturate any metric. `sra` and `qce` use properly scoped `Generator` objects or a single fixed seed. Recorded as a near-miss rather than a finding.

---

# Corrections made during this audit

Recorded because batch 1's self-correction is part of the credible result, and because one of these initially would have produced a false contradiction.

1. **`ems` Monte Carlo.** Before executing, the auditor predicted — on a symmetric log-normal model with a deterministic EIR of only +0.25 dB — that the paper's "no realisations below -10 dB" claim would be roughly a coin flip (`P(at least one of 100) = 0.545`). **The executed result was 0/100, minimum -3.96 dB.** The claim is SUPPORTED. The prediction was wrong and the error was mine, not the paper's. The correct statement, established afterwards, is that the claim holds because the code implements 1.5 dB of fading rather than the paper's stated 3.0 dB — which is a different finding about a different thing.
2. **quantum-k-sat mixer.** Suspected on inspection that `mixer` was non-unitary and therefore an invalid circuit operator. **MEASURED: `||out||^2 = 1.000000000000` at gamma = 0.0, 0.3, 0.9 — it is exactly unitary.** No unitarity defect is claimed. The mixer is a non-standard Hamiltonian evolution, which is a description gap, not a bug.
3. **quantum-k-sat JSON.** The `depth.gap` field failed an initial exact-equality check. Investigation showed a 1-2 ULP difference from BLAS reduction order, with all 98 other numbers bit-identical and no downstream effect. **Not recorded as a discrepancy.**
4. **`ems` JSON.** The `beamsteer` `AF_ev` field differs by a factor of 2.46 between committed and reproduced. It is a mathematically-zero quantity below the float64 cancellation floor, and every quantity the paper reports reproduced bit-identically. **Not recorded as a discrepancy**; used instead as evidence for finding U1.
5. **qce L3 arithmetic.** An earlier draft recorded `L3 total 19` against a 11/5/2 split. Corrected to 18 so the machine-readable row is internally consistent.
6. **Orphan-figure detection.** A first-pass `grep`-based orphan detector reported 6 false positives in `ems` and 6 in `sra`, because those figures are written via f-string prefixes (`f'fig_field_{pattern}'`) and so never appear literally in the source. Replaced with `git status` after a full re-run, which is authoritative. The only genuine orphan in the batch is `ems/figures/fig_signals.{png,pdf}`.

---

# Batch aggregate

```
N audited
4

N with reproducible artifacts (L1+L2 SUPPORTED)
4

N with internally consistent papers (L7 SUPPORTED)
0

N with unsupported claims (L3 unsupported > 0)
3

N with contradicted claims (L3 contradicted > 0)
4

N with figure/data mismatch (L4 CONTRADICTED)
3

N with methodological non-execution (L5 CONTRADICTED)
4
```

**N audited = 4.** Per R5 and R6, these figures describe exactly these four repositories and no others. Nothing here characterises the remaining repositories on this account.

## The hypothesis under test

The rubric states the hypothesis so it can fail: **artifact reproducibility is materially better than artifact-to-claim correspondence.** For these 4 packages, **the hypothesis is supported, and the gap is large.**

- **Reproducibility: 4 of 4.** Every package ran to exit code 0. Every `metrics.json` reproduced, two of them **bit-identically** (`sra`: 45/45 rows; `qce`: 32/32 values), one bit-identical on every reported field (`ems`), one bit-identical on 98 of 102 numbers (`quantum-k-sat`, remainder at 1-2 ULP). The simulation infrastructure in this batch is genuinely sound, on a toolchain substantially newer than the artifacts'.
- **Artifact-to-claim correspondence: 45 of 75 claims supported (60.0%), 24 contradicted (32.0%), 6 unsupported (8.0%).** Internal consistency: **0 of 4.** Methodological non-execution: **4 of 4.**

The split is the phenomenon the rubric was written to measure, and it reproduces the `cd-ieee-package` reference case rather than contradicting it. Note also that the hypothesis is **not** merely "reproducibility is better": reproducibility is near-total (4/4, with two packages bit-exact) while claim correspondence fails on **every single package** at the L7 layer. The fracture is not a matter of degree in this batch.

## Layer-by-layer across the 4 audited packages

| layer | SUPPORTED | CONTRADICTED | note |
|---|---|---|---|
| L1 artifact | 4 | 0 | every cited result exists as a committed file |
| L2 reproduction | 4 | 0 | 2 bit-identical, 2 identical modulo ULP |
| L3 numerical claim | 45 | 24 contradicted + 6 unsupported | per-package: ems 12/3/3, qce 11/5/2, qks 13/11/1, sra 9/5/0 |
| L4 figure | 1 (quantum-k-sat) | 3 | quantum-k-sat is the only package with all figures sound |
| L5 method | 0 | 4 | no package fully implements the method it describes |
| L6 selection | 2 (ems, quantum-k-sat) | 2 (qce, sra) | sra's failure is a baseline confound, not best-case selection |
| L7 internal consistency | 0 | 4 | uniform failure across the batch |
| L8 verdict | 0 | 0 | 4x PARTIALLY SUPPORTED; none fully supported, none wholly unverifiable |

## What a reviewer should take from this batch

1. **The simulators are good.** All four ran, all four reproduce, two bit-exactly. This is not a fabrication story and the audit should not be read as one.
2. **The papers are not.** Every one of the four fails L7. Every one fails L5. The pattern is consistent: numbers are transcribed from artifacts with high fidelity (60% of claims exactly right, and 100% of the main result tables in `ems` and `sra`), while the *mechanism*, the *causal explanation*, and the *labelling* of what ran are not supported.
3. **The self-reported nulls are the most telling finding.** `qce` prints "Quantum-Only == QCE" and "QCE-NoRL == QCE" in its own tables. `sra` explicitly discloses that makespan is invariant. `quantum-k-sat` correctly reports that depth does not help and gets the sign of its own optimality gap wrong. In two of three cases the paper contains the refutation of its own framing, in print, and the abstract does not mention it.
4. **The "independent reference kernels" are a liability, not an asset.** Three of four packages ship a C file that no build system references, that the README tells the reader to run, and that disagrees with the paper when run — in `ems`'s case reversing the headline result. The right action is to either delete them or make them real tests that pass.
5. **The single cleanest defect to fix across the account is trivial:** `qce_simulator.py` reports `avg_active_mitigations = 0.0` for a baseline running with all five mitigations active at every step, because the history dict omits the key `compute_metrics` looks for.

## R8 — method failures and disclosure

Recorded per R8; an unverifiable layer is a result, not an omission.

- **No environment blocked verification.** All four simulators executed to completion with exit code 0, and all three C kernels compiled and ran.
- **Two layers are UNVERIFIABLE in principle, not for want of trying:**
  - `qce`'s ablation table (U1, U2) has no committed code path. No flag, parameter, or function in `qce_simulator.py` can produce those rows. The auditor did not estimate them.
  - `quantum-k-sat`'s significance testing and below-median analysis (U1, D4, D5) cannot be reproduced because the per-trial data is not committed — only per-level means and standard deviations — and because the two arms ran on different instances, so no paired test exists to run.
- **Not attempted:** recompiling the LaTeX sources. `pdflatex`/`xelatex` are not installed in this environment. The compiled PDFs were read for the figure content that the papers embed, and the LaTeX sources were read directly for all claims. No claim in this report depends on recompiling a PDF.
- **Toolchain caveat, disclosed rather than hidden:** the artifacts were committed under an older toolchain than the one used here (numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.2, Python 3.14.3). The only reproduction differences found were 1-2 ULP in `quantum-k-sat`'s `depth.gap` and sub-1e-13 relative differences in two `ems` fields. **No result in this report depends on a difference that could be attributed to toolchain drift**, and every discrepancy reported is orders of magnitude larger than ULP noise.
