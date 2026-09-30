# E1 Batch 1 Audit Report

**Rubric:** `ARTIFACT-TO-CLAIM-RUBRIC.md` v1.0
**Date:** 2026-09-29
**Auditor:** delegated agent, read-only
**Note:** reconstructed from the agent's completed return after the scratch directory was rotated. Findings are verbatim; only the file was lost.

## Machine-readable results

| package | repo | L1 | L2 | L3 total | L3 supported | L3 contradicted | L3 unsupported | L4 | L5 | L6 | L7 | L8 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| adan-ieee-package | FernandoMay/adan-ieee-package | SUPPORTED | SUPPORTED | 24 | 17 | 3 | 4 | CONTRADICTED | SUPPORTED | SUPPORTED | CONTRADICTED | PARTIALLY SUPPORTED |
| camae-paper | FernandoMay/camae-paper | SUPPORTED | SUPPORTED | 52 | 47 | 5 | 0 | SUPPORTED | SUPPORTED | SUPPORTED | CONTRADICTED | PARTIALLY SUPPORTED |
| isac-jasc-ieee | FernandoMay/isac-jasc-ieee | SUPPORTED | SUPPORTED | 81 | 70 | 11 | 0 | SUPPORTED | CONTRADICTED | SUPPORTED | CONTRADICTED | CONTRADICTED |
| sc-ieee-package | FernandoMay/sc-ieee-package | SUPPORTED | CONTRADICTED | 38 | 34 | 4 | 0 | SUPPORTED | CONTRADICTED | SUPPORTED | SUPPORTED | PARTIALLY SUPPORTED |

## L8 verdicts

- **adan — PARTIALLY SUPPORTED.** Artifacts reproduce to 2.2e-16, but 4 ablation numbers exist in no code and no artifact, and 3 overhead/percent claims are wrong, one of them arithmetically impossible.
- **camae — PARTIALLY SUPPORTED.** All 36 table cells and 45/45 summary cells exact, but all 4 comparative claims favouring CAMAE are contradicted, including the abstract's headline 82.3%.
- **isac — CONTRADICTED.** The abstract's only headline number is refuted by the paper's own table, and the CRLB "validation" is circular by construction.
- **sc — PARTIALLY SUPPORTED.** 24/24 table cells and the adaptive-selection result hold, but the headline level does not reproduce and the C kernel does not compile.

## L3 discrepancies — 23 contradicted, 4 unsupported

| package | claimed | actual | artifact |
|---|---|---|---|
| adan | 237% improvement over NoRes | **238.13%** | `figures/metrics.json` |
| adan | 4.3 invocations/step | **2.608** (measured 1304/500) | same |
| adan | weighted cost 1.86 | **5.272** (2636/500) | same |
| adan | ADAN₋H / −AR / −AP / −RP = .621/.658/.697/.718 | **no code, no artifact exists** | *none* |
| camae | 82.3% turbulence reduction | **CWF ESI = 0.0000000000 identically**; CAMAE 0.01658912, so the metric is undefined and the direction reverses | `results/Cognitive_Radar_Jamming_CWF.csv` |
| camae | 1.5% over CWF | **1.0930%** | `results/Cognitive_Radar_Jamming_{CAMAE,CWF}.csv` |
| camae | "tighter distribution" | sd **60.2155** vs 6.6821 / 9.8575 — **9× wider** | same |
| camae | "significantly outperform" | **z = 0.3** | `results/Satcom_LEO_Doppler_*.csv` |
| camae | CAMAE "lower ESI" | **higher in all 3 scenarios** | all 9 CSVs |
| isac | SE > 4 bps/Hz | sweep max **2.64451** at +15 dB | `isac_experiment_results.csv` (type=sweep) |
| isac | σ_v < 5 m/s across the range | **104.01 m/s at −15 dB**; violated in 9 of 11 points | same |
| isac | README table, 9 cells | −15 dB PE **0.0472** not 0.350; 0 dB SE **0.5381** not 3.50; +15 dB BER **5.077e-3** not 3e-4 — up to **33× off** | same |
| sc | 0.69 on LEO | **0.684983** → 0.68 | `figures/metrics.json` |
| sc | degradation 2–10% | LEO L2 **−15.45%**; L1 −25.18% ≈ L0 −25.34% | same |
| sc | 10–15% L0→L2 loss | **16.34 / 16.16 / 16.15%** | same |

## What survived as SUPPORTED

R7 requires this recorded, not omitted.

- **isac: 55/55 cells** of `results_summary.tex` agree with the artifact across PE / BER / SE / CRLB_R / SINR × 11 SNR. Also correct: `N_MC`, target distributions, sub-metre σ_R, and regime bands. The cleanest table in the batch.
- **camae: all 36 table cells.** `paper_table_results.csv` is the exact mean of the 9 per-run CSVs (45/45). The "recovery within 1–2 timesteps" claim is **correct**.
- **sc: all 24 table cells**, the adaptive selection result (L2 chosen on all paths, scores 0.8407 / 0.7113 / 0.7956, `selected_level==2` in all 90 records) — **and this one reproduces**. Plus an exact 8× bandwidth saving and genuine Pareto optimality.
- **adan: all 4 table rows** — 96.3%, 52.7%, 47.3%, +0.523, +0.259, and the exact Full-Resilience "4.0 / 10.0" overhead.

## Duplication check

No byte-identical artifact exists across the four packages. All 86 files over 2 KB were hashed; nothing is scored twice. The only duplication is within `isac`, which ships each figure twice (root and `figures/`) with differing bytes.

## The finding that qualifies the hypothesis

The original hypothesis — artifact reproducibility is better than artifact-to-claim correspondence — **survives, but needs a qualifier: reproducibility is selectively good, and it fails exactly where the conclusion depends on it.**

- `sc` reproduces 540 of 720 records bit-exactly and fails on precisely the 180 carrying its recommended operating point.
- `isac` has the batch's most reproducible artifact (agreement to 1.8e-12) and the batch's worst defect: the estimator error is **drawn from the CRLB it is being tested against** (line 147). That is circular by construction.

**Good simulation hygiene buys nothing when the defect lives in what the simulation measures.**

## Auditor self-corrections

Recorded because R7 applies to the auditor too. Two of the auditor's own errors were caught before reporting:

1. A `camae` "capacity drop" that was actually an upward spike.
2. A broken scenario-name join that made 45/45 cells falsely mismatch.

Correcting the first is what turned a would-be false contradiction into a SUPPORTED finding.
