# A-09 — RAAI 2026, Fuzzy-Calibrated Conformal Prediction for Safe Action Selection in Autonomous Agents

**Status: `Proposed` — not submitted anywhere. First reproducible run and recorded metrics are linked (asset PR #1). Real-time/latency and multi-seed evidence remain blocked.**

## Update 2026-10-14 — first reproducible run delivered

The asset [iscmi-01-fuzzy-conformal](https://github.com/FernandoMay/iscmi-01-fuzzy-conformal)
now carries a closed-loop **safe action selection** extension that the previous
"Next real action" asked for: the fuzzy-scaled conformal construction is
generalised from binary coverage to a finite action set, with an
abstain/reject decision rule before action execution.

Delivered on branch `a09-selective-action-selection`, commit `4905230`,
pull request [#1](https://github.com/FernandoMay/iscmi-01-fuzzy-conformal/pull/1).

**Verified figures** (reproducible: `pytest tests/ -q` → 10 passed;
`python src/agent_selection.py` → `data/agent_selection_metrics.json`):

| proxy | actions | coverage (base) | coverage (fuzzy) | selective risk (base) | selective risk (fuzzy) | AURC |
|---|---|---|---|---|---|---|
| digits | 10 | 0.867 | 0.897 | 0.006 | 0.018 | 0.003 |
| wine | 3 | 0.944 | 1.000 | 0.000 | 0.000 | 0.000 |
| iris | 3 | 0.867 | 0.967 | 0.071 | 0.038 | 0.014 |

Provenance: seed `20260915`, ensemble size `7`, `alpha = 0.10`, `beta = 0.50`,
scikit-learn `1.6.1`. Datasets are public scikit-learn proxies (`digits`, `wine`,
`iris`) used as a finite action set — **methodological stand-ins, not deployment
or safety validation**. Full detail and honest limitations live in the asset's
`RESULTS.md`.

## At a glance

| Field | Value |
|---|---|
| Backlog ID | `A-09` (assigned 2026-10-14) |
| Venue | RAAI 2026 (Singapore, December 18–20, 2026) |
| Track | Artificial Intelligence, Machine Learning and Deep Learning |
| Working title | Fuzzy-Calibrated Conformal Prediction for Safe Action Selection in Autonomous Agents |
| Enfoque (rendered in ENGLISH) | Fuzzy-calibrated (adaptive) conformal prediction that bounds uncertainty before an autonomous agent executes an action; abstain / reject / defer decision rules for critical environments |
| Repo | [iscmi-01-fuzzy-conformal](https://github.com/FernandoMay/iscmi-01-fuzzy-conformal) |
| Submission link | `TBD — none` |
| Submission date | `TBD — none` |
| Official deadline | **2026-11-01** (from Inbox 2026-10; source: [inbox-2026-10/03-raai-2026/README.md](../inbox-2026-10/03-raai-2026/README.md)) |
| Inbox classification | `Verified established` |
| Retrieved | 2026-10-14 |

**Topic decision (2026-10-14):** Sharpened from a generic calibration topic to a **fuzzy-calibrated conformal** topic, merging the A-04 fuzzy-conformal asset with agentic action selection. Momentum: `iscmi-01-fuzzy-conformal` already packaged (SD-01); deadline 2026-11-01 gives room for a real run. Fits the venue's AI/ML track.

## Evidence gate (rules.md §3)

| Field | Status | Evidence / remaining requirement |
|---|---|---|
| Reproducible run | **Satisfied** (2026-10-14) | [iscmi-01-fuzzy-conformal](https://github.com/FernandoMay/iscmi-01-fuzzy-conformal) commit `4905230` / PR [#1](https://github.com/FernandoMay/iscmi-01-fuzzy-conformal/pull/1); seed `20260915`; `pytest tests/ -q`; `python src/agent_selection.py` |
| Uncertainty calibration | **Partial** | Marginal coverage, mean set size and miscoverage across a calibration/test split are recorded; **repeated trials / multi-seed confidence intervals still missing** |
| Decision-making loop | **Satisfied** (2026-10-14) | Closed-loop policy with abstain/reject (execute iff the prediction set is a singleton); action-level metrics: coverage, abstention rate, selective risk, risk-coverage curve, AURC — on proxy action sets, not real consequences |
| Real-time constraints | Blocked | Latency/compute budget, timing measurements, worst-case latency under load |
| Baselines | **Partial** | Non-conformal confidence ranking (AURC) and the non-fuzzy conformal variant; **missing** MC-dropout, temperature scaling, and Bayesian baselines with citations |

## References to establish

Canonical search terms (3–6). **do NOT invent citations.** Only record verified sources if/when found.

- "conformal prediction" + "uncertainty calibration" + "autonomous agents" + "decision-making"
- "adaptive conformal prediction" + "online conformal" + "non-exchangeable" + "distribution shift"
- "safe autonomous systems" + "abstention" + "human-in-the-loop" + "risk control"
- "coverage" + "prediction sets" + "calibration" + "reproducible evaluation"
- "real-time agents" + "critical environments" + "conformal risk control"

## Next real action

1. Add multi-seed runs with confidence intervals and a distribution-shift split (closes the "Uncertainty calibration" gap).
2. Add stronger selective-prediction baselines (MC-dropout, temperature scaling) and citations (closes the "Baselines" gap).
3. Add latency/timing measurements for the abstention policy (closes the "Real-time constraints" gap).
4. Draft the manuscript against the RAAI 2026 template (deadline 2026-11-01).
