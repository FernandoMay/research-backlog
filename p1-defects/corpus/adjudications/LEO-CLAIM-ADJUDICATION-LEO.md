# LEO claim adjudication — disposition and required action

**Date:** 2026-09-30
**Frozen evidence state:** sweep commit `3fd1fa6`, integrity row `5c98fef`, docs `8a7c420`. Working tree clean, eight falsifiers green.
**Precondition:** the manuscript has not been edited. This document adjudicates; it does not rewrite.
**Companion:** `CLAIM-INTEGRITY-LEO.md` established which values changed. This one decides what happens to each claim.

---

## Disposition vocabulary

Scientific disposition and editorial action are **separate fields**. A claim can be scientifically unanswerable while remaining textually worth keeping in a reformulated form, so the two must not be collapsed into one choice.

| disposition | meaning |
|---|---|
| **RETAIN** | directly supported by the final evidence, as worded |
| **REWRITE** | evidence exists, but the current wording overreads what it measures |
| **REMOVE** | no defensible proposition remains on the available evidence |
| **NEW EXPERIMENT REQUIRED** | the question is scientifically sound; this sweep cannot identify it |
| **NOT VERIFIED** | insufficient evidence to adjudicate; must not become "contradicted" |
| **NON-DISCRIMINATING** | the number is correct, but the instrument cannot attribute it to the mechanism the claim evaluates |

**REMOVE ≠ NEW EXPERIMENT REQUIRED.** REMOVE means no defensible proposition remains. NEW EXPERIMENT REQUIRED means the proposition may well be true and the experiment cannot currently identify it. Collapsing them would discard real questions.

**Historical state** is recorded per claim as `SUPERSEDED BY REPAIRED EVIDENCE` or `unchanged`. It is not a disposition. It exists because the distinction below is the central result of this program and should not be lost in a table of verdicts:

> Correspondence failure ≠ reproduction failure. The paper corresponded to its artifact. The artifact measured something else.

---

## The matrix

| ID | exact claim (abridged) | loc | type | published | final evidence | disposition | action | reason |
|---|---|---|---|---|---|---|---|---|
| **C1** | Dijkstra avg latency 24.35 ms | L232, L240 | measurement | 24.35 | **15.03** (183 obs / 17 disc) | REMOVE | REWRITE with 15.03 and observation coverage | published value reproduced by the pre-repair artifact; measurement was semantically contaminated by averaged disconnections |
| **C2** | NSGA-II avg latency 24.17 ms | L232, L240 | measurement | 24.17 | **14.88** (185 obs / 15 disc) | REMOVE | REWRITE with 14.88 | published value was `bl_lat × (0.7+0.3·w)`; the arm now measures its own route |
| **C3** | NSGA-II+QL avg latency 25.10 ms | L232, L240 | measurement | 25.10 | **15.65** (179 obs / 21 disc) | REMOVE | REWRITE with 15.65 | unchanged by any repair and still moved, because the aggregated set changed |
| **C4** | Dijkstra delivery 80.00% | L232, L240 | measurement | 80.00 | **91.50** | REMOVE | REWRITE with 91.50 | the 55/60 stand-ins were counted as failed deliveries and as latencies |
| **C5** | NSGA-II delivery 74.50% | L232, L233 | measurement | 74.50 | **92.50** | REMOVE | REWRITE with 92.50 | as C4 |
| **C6** | NSGA-II+QL delivery 78.00% | L232, L240 | measurement | 78.00 | **89.50** | REMOVE | REWRITE with 89.50 | as C4 |
| **C7** | Resilience 77.83% for all three | L234 | measurement | 77.83 ×3 | **100.00 / 100.00 / 94.52** | REMOVE | REWRITE | the three values were one measurement appended to three lists; identical by construction |
| **C8** | "near-100% coverage"; "The 100% coverage fraction **confirms** the viability of global satellite connectivity" | L33, L235, L315 | measurement **used as evidence** | 100.0 ×3 | **100.0 ×3** — and `compute_resilience(env, route_type)` returns identical coverage for strategies 0, 1, 2 | **NON-DISCRIMINATING** | REWRITE | the value is correct and unchanged, but coverage is computed before the link-admission rule and never reads the route, so it cannot support a statement about method behaviour or mechanism. "Confirms viability" is a causal use of a non-discriminating instrument |
| **C9** | "NSGA-II optimization provides marginal latency improvement (24.17 ms)" | L240 | causal inference from C1−C2 | +0.18 | +0.15 measured, from an unrelated mechanism | **REMOVE** | REMOVE the historical figure; retain +0.15 **only** as a new result | published advantage came from the `0.7+0.3·w` multiplier plus asymmetric 55/60 stand-ins. Numerical proximity does not establish survival |
| **C10** | "Q-learning alone achieves the lowest latency (15.06 ms)" | L276 | comparative ordering | 15.06 | **15.15** | REMOVE | REMOVE | ordering claim; see C21 |
| **C11** | "NSGA-II alone ... incurs higher latency (21.43 ms)" | L276 | comparative ordering | 21.43 | **15.13** | REMOVE | REMOVE | ordering claim; see C21 |
| **C12** | "The hybrid ... attains 21.11 ms latency" | L276 | measurement | 21.11 | **15.23** | REMOVE | REWRITE with 15.23 | unchanged by M1-B and M1-B2; moved when M1-C stopped averaging disconnections |
| **C13a** | hybrid delivery "99.7%" | L276 | measurement | 99.7 | **99.7** | **RETAIN** | RETAIN | survives literally; the extended artifact's ablation block was regenerated after M1-B and reports the same value |
| **C13b** | "it inherits the adaptive switching of Q-learning while using the NSGA-II-derived policy library to cover the resilient regime that a single fixed mode cannot" | L276 | causal attribution | — | not identified | **NEW EXPERIMENT REQUIRED** | REWRITE to report non-identification | see C21 |
| **C14** | "the DQN baseline falls to 97.7%" | L33, L264, L325 | measurement | 97.7 | **98.67** | REMOVE | REWRITE with 98.67 | |
| **C15** | "Dijkstra's to 98.2%" | L264 | measurement | 98.2 | **98.67** | REMOVE | REWRITE with 98.67 | |
| **C16** | "the hybrid sustains 99.0% delivery at 8% failure" | L33, L264, L325 | measurement | 99.0 | **98.83** | REMOVE | REWRITE with 98.83 | |
| **C17** | "the NSGA-II-guided mode [sustains] 99.5%" | L264 | measurement **+ label** | 99.5 | **98.50**, label now correct | REMOVE | REWRITE value; RETAIN the corrected label | row R2 established the arm is `GAWeightedRouter` consuming the NSGA-II prior as a fixed mode, so "NSGA-II only" names the treatment accurately. `DEFECT-001-LEO.md` §3.7's description of it as a genetic load balancer is wrong for this package |
| **C18** | hybrid "maintain[s] over 62% resilience at 10% failure ... compared to 40% for Dijkstra and 42% for NSGA-II alone" | L298 | measurement at an unswept condition | 62/40/42 | **no measurement** | **NEW EXPERIMENT REQUIRED** | REWRITE to state it is unreported | `metrics_extended.json` sweeps 2/4/8%. "Searched and not found" is neither "contradicted" nor "does not exist" |
| **C19** | "the hybrid is the most robust under stress" | L33, L264, L325 | comparative ordering | ordering | dijkstra = hybrid = 98.67 > ga 98.50 | REMOVE | REMOVE | the published ordering does not reproduce at any swept point; the arms are within 0.33 pp at 8% |
| **C20** | "An ablation study attributes this to the synergy between the NSGA-II offline Pareto prior and the Q-learning agent's state-conditioned mode switching" | L33, L326 | attribution | — | not identified | **NEW EXPERIMENT REQUIRED** | REWRITE to report non-identification | the attribution rests on C10–C12, whose spread collapsed from 6.37 ms to 0.10 ms |
| **C21** | **latency cost of the offline prior** (implicit premise of C10, C11, C13b, C20) | L184, L276 | causal premise | 6.37 ms spread | **0.10 ms spread** | **NEW EXPERIMENT REQUIRED — NOT IDENTIFIED** | REWRITE; reserve the original assertion for a future experiment | see the dedicated finding below |

**Survive as written: C13a only.** One claim out of twenty-one.

---

## C21: the premise underneath four claims

This is the block that most needs care, because it is where an audit can flip into an overclaim in the opposite direction.

```
OLD                      FINAL
QL        15.06          15.15
GA        21.43          15.13
Hybrid    21.11          15.23
spread     6.37 ms        0.10 ms
```

The claim that the offline prior **costs** latency, and that Q-learning's switching recovers it, has lost its evidence. The paper does not claim the opposite, and neither does this audit:

> **The repaired experiment cannot distinguish "the prior is free" from "the metric cannot see the difference".**

It is genuinely possible that a zero-cost prior is the correct finding. The sweep cannot establish that, because 98.3% of ISL pairs sit at positive SNR and `dijkstra_shortest_path` returns 1 hop on 200 of 200 draws, so latency has no dynamic range across the swept failure range. A flat result under an insensitive instrument is not evidence of absence.

Disposition: **NEW EXPERIMENT REQUIRED / NOT IDENTIFIED.** Not REMOVE: the proposition may be true.

---

## Superseded states, recorded

| ID | paper value | pre-repair artifact | final artifact | historical state |
|---|---|---|---|---|
| C1 | 24.35 | 24.35 | 15.03 | SUPERSEDED BY REPAIRED EVIDENCE |
| C2 | 24.17 | 24.17 | 14.88 | SUPERSEDED BY REPAIRED EVIDENCE |
| C3 | 25.10 | 25.10 | 15.65 | SUPERSEDED BY REPAIRED EVIDENCE |
| C4–C6 | 80.00/74.50/78.00 | identical | 91.50/92.50/89.50 | SUPERSEDED BY REPAIRED EVIDENCE |
| C7 | 77.83 ×3 | identical (one measurement, three lists) | 100.00/100.00/94.52 | SUPERSEDED BY REPAIRED EVIDENCE |
| C8 | 100.0 ×3 | identical | identical | unchanged, and non-discriminating throughout |
| C13a | 99.7 | 99.7 | 99.7 | unchanged |
| C18 | 62/40/42 | — | — | never measured |

All nine Table I values are traceable to the pre-repair artifact. **The paper corresponded to its artifact; the artifact measured something else.** That is the distinction the E1 rubric keeps as L2 and U3, and this package is now the clearest demonstration of it: perfect reproduction, and a failure of correspondence that no reproducibility verdict could reach.

---

## What each disposition requires, in aggregate

| disposition | claims |
|---|---|
| RETAIN | C13a |
| NON-DISCRIMINATING | C8 |
| NEW EXPERIMENT REQUIRED | C13b, C18, C20, C21 |
| REMOVE | C9, C10, C11, C19 |
| REMOVE + REWRITE with new value | C1–C7, C12, C14–C17 |

**No manuscript line is edited by this document.** The editorial column records what a future edit would have to do and what evidence it would have to cite; it is not an instruction already carried out.

---

## One thing this matrix cannot deliver

Ten of the twenty-one claims reduce to nine numbers plus an ordering. Rewriting them with the new values is mechanical and safe **provided** each rewritten sentence states its observation coverage — 183/185/179 observations with 17/15/21 disconnections excluded — because a latency mean over 183 of 200 rounds is not the same kind of object as one over 200.

The other group cannot be rewritten at all. C13b, C20 and C21 are not stale numbers; they are unanswered questions. The honest text for them is a statement that the experiment as designed does not identify the effect, and that is a weaker result than the paper currently claims.
