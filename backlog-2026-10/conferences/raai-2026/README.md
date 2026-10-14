# A-09 — RAAI 2026, Fuzzy-Calibrated Conformal Prediction for Safe Action Selection in Autonomous Agents

**Status: `Proposed` — proposal only; no manuscript, no run; all numeric claims blocked.**

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

No number may appear until a linked, reproducible run exists. Current state: **no run** — all numeric claims blocked.

| Field | Status | Required evidence |
|---|---|---|
| Reproducible run | No run linked | Linked, current run (code + seeds + configuration) with reproducible instructions |
| Uncertainty calibration | Blocked | Conformal prediction coverage, set size, miscoverage rate, calibration error across splits; repeated trials |
| Decision-making loop | Blocked | Closed-loop evaluation (policy with reject/abstain/defer), safety constraints, action-level metrics |
| Real-time constraints | Blocked | Latency/compute budget, timing measurements, worst-case latency under load |
| Baselines | Blocked | Baselines (probabilistic, ensemble, temperature scaling) with citations and reproduction steps |

## References to establish

Canonical search terms (3–6). **do NOT invent citations.** Only record verified sources if/when found.

- "conformal prediction" + "uncertainty calibration" + "autonomous agents" + "decision-making"
- "adaptive conformal prediction" + "online conformal" + "non-exchangeable" + "distribution shift"
- "safe autonomous systems" + "abstention" + "human-in-the-loop" + "risk control"
- "coverage" + "prediction sets" + "calibration" + "reproducible evaluation"
- "real-time agents" + "critical environments" + "conformal risk control"

## Next real action

Extend the [iscmi-01-fuzzy-conformal](https://github.com/FernandoMay/iscmi-01-fuzzy-conformal) package to closed-loop agent evaluation (decision rules before action execution, abstention/reject policies), define safety metrics, and produce a linked reproducible run with pinned datasets, seeds, and timing measurements; no numbers to be published until that run exists.

(End of file)
