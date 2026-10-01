# LEO claim-integrity reconciliation

**Date:** 2026-09-30
**Frozen state:** `3fd1fa654fd68f23a69f96a4c85bb9e3712a1e2b`, working tree clean,
seven falsifiers green.
**Scope:** what in `paper/main.tex` is still true under the evidence regenerated
after R1, L1c, R2, M1-R2, M1-B, L1p, M1-B2 and M1-C.
**Not done here:** no manuscript claim was edited. This document is the audit
record, not the correction.

---

## 0. The finding that reframes everything else

**Every number in the paper's Table 1 matched the pre-repair artifact exactly.**

| metric | paper | pre-repair artifact |
|---|---|---|
| Avg Latency (Dijkstra / NSGA-II / NSGA-II+QL) | 24.35 / 24.17 / 25.10 | 24.35 / 24.17 / 25.10 |
| Delivery Rate | 80.00 / 74.50 / 78.00 | 80.00 / 74.50 / 78.00 |
| Resilience | 77.83 / 77.83 / 77.83 | 77.83 / 77.83 / 77.83 |

Not approximately. Exactly, all nine. The paper was a faithful report of an
experiment that the sweep then showed was not measuring what it claimed. This is
the `i01` pattern again — a real simulation with a faithful description of the
wrong pipeline — and it is why "the paper matches the artifact" was never
evidence of validity.

---

## 1. Claim → evidence matrix

| # | claim | artifact | published | pre-repair | **final** | status |
|---|---|---|---|---|---|---|
| C1 | Dijkstra avg latency 24.35 ms | `metrics.json` | 24.35 | 24.35 | **15.03** | contradicted |
| C2 | NSGA-II avg latency 24.17 ms | `metrics.json` | 24.17 | 24.17 | **14.88** | contradicted |
| C3 | NSGA-II+QL avg latency 25.10 ms | `metrics.json` | 25.10 | 25.10 | **15.65** | contradicted |
| C4 | Dijkstra delivery 80.00% | `metrics.json` | 80.00 | 80.00 | **91.50** | contradicted |
| C5 | NSGA-II delivery 74.50% | `metrics.json` | 74.50 | 74.50 | **92.50** | contradicted |
| C6 | NSGA-II+QL delivery 78.00% | `metrics.json` | 78.00 | 78.00 | **89.50** | contradicted |
| C7 | Resilience 77.83% for all three | `metrics.json` | 77.83 ×3 | 77.83 ×3 | **100.00 / 100.00 / 94.52** | contradicted |
| C8 | Coverage 100.0% for all three | `metrics.json` | 100.0 ×3 | 100.0 ×3 | **100.0 / 100.0 / 100.0** | survives — but see §3 |
| C9 | NSGA-II improves latency by 0.18 ms | derived from C1−C2 | +0.18 | +0.18 | **+0.15** | contradicted; see §4 |
| C10 | Ablation: QL alone lowest at 15.06 ms | `metrics_extended.json` | 15.06 | 15.06 | **15.15** | contradicted |
| C11 | Ablation: NSGA-II alone worst at 21.43 ms | `metrics_extended.json` | 21.43 | 21.43 | **15.13** | contradicted |
| C12 | Ablation: hybrid 21.11 ms | `metrics_extended.json` | 21.11 | 21.11 | **15.23** | contradicted |
| C13 | Ablation: hybrid delivery 99.7% | `metrics_extended.json` | 99.7 | 99.7 | **99.7** | survives |
| C14 | DQN delivery 97.7% at 8% failure | `metrics_extended.json` | 97.7 | 97.67 | **98.67** | contradicted |
| C15 | Dijkstra delivery 98.2% at 8% failure | `metrics_extended.json` | 98.2 | 98.17 | **98.67** | contradicted |
| C16 | Hybrid delivery 99.0% at 8% failure | `metrics_extended.json` | 99.0 | 99.0 | **98.83** | contradicted |
| C17 | "NSGA-II-guided mode" 99.5% at 8% failure | `metrics_extended.json` | 99.5 | 99.5 | **98.50** | contradicted + mislabelled |
| C18 | Hybrid >62% resilience at 10% failure vs 40/42% | none | 62/40/42 | — | — | **not verifiable** |
| C19 | Hybrid sustains 99.0% where DQN falls to 97.7% | `metrics_extended.json` | 99.0 / 97.7 | 99.0 / 97.67 | **98.83 / 98.67** | contradicted |
| C20 | Hybrid is "most robust under stress" | `metrics_extended.json` | ordering | DQN < Dijk < ga < hybrid | **dijkstra = hybrid = 98.67 > ga 98.50** | contradicted |

**Survives: C8 and C13.** Everything else is contradicted or not verifiable.

---

## 2. The four layers, separated

| layer | question | state |
|---|---|---|
| **R1** | does `weights → routing → objective`? | ✅ established. Falsifier 6/6, 18 negative-control round-trip cases in SGN's counterpart |
| **R2** | does the experiment identify its comparisons? | ✅ established. Arms carry the treatment their names advertise; same-admission arms are *required* to agree |
| **M1** | are latency and resilience measurements sensitive to the mechanism? | ✅ established. Routing reaches latency (5.13 ms separation) and resilience (100/100/79.69%) |
| **L1** | does the artifact identify its run? | ✅ established for both artifacts; shared `environment` block, byte-identical A/B |

Establishing all four is not evidence for any particular claim. It establishes
that the instrument now works. **What the instrument says is §1.**

---

## 3. C8 survives, and it is not evidence

Coverage is 100.0% for all three arms, before and after. It "survives" the
comparison and it is worthless, because coverage is computed from the active
satellite count and the coverage footprint **before the link-admission rule and
without ever reading the route**:

```
coverage by strategy 0, 1, 2:  [100, 100, 100]   identical
```

Coverage has no causal path to routing. It cannot discriminate arms, before or
after. A claim resting on it would be resting on a number that is constant
because the metric is constant, not because the methods agree.

This is the distinction the whole program turns on: **a number that survives a
comparison is not the same as a claim that survives.**

---

## 4. C9: the `+0.18` / `+0.15` proximity is not survival

```
Published advantage: +0.18 ms — not supported by the repaired measurement pipeline.
Final measured advantage: +0.15 ms — newly generated result after M1-C.
Numerical proximity does not establish claim survival.
```

They are 0.03 ms apart and come from unrelated mechanisms.

- The published `+0.18` was produced by `ns_lat × (0.7 + 0.3·w_latency)` — the
  optimiser's own weight used as a multiplier — combined with **asymmetric
  stand-ins** (60.0 ms for the baseline, 55.0 ms for the others) averaged in over
  disconnections.
- The final `+0.15` is the difference of two per-arm means over 183 and 185
  observations, with 17 and 15 disconnections excluded rather than averaged in.

Selecting this proximity as evidence that the paper was approximately right is
choosing a preferred explanation among unverified causes, which is the defect
the audit exists to detect. It is recorded as a coincidence.

---

## 5. C10–C12: the ablation's central attribution has lost its evidence

The paper's prose states the mechanism explicitly: *"Q-learning alone achieves
the lowest latency (15.06 ms) but, without the NSGA-II prior, its delivery rate
under stress is lower... NSGA-II alone... incurs higher latency (21.43 ms)."*

| arm | paper | pre-repair | final |
|---|---|---|---|
| QL only | 15.06 | 15.06 | **15.15** |
| NSGA-II only | 21.43 | 21.43 | **15.13** |
| Hybrid | 21.11 | 21.11 | **15.23** |

Claimed spread across arms: **6.37 ms**. Final spread: **0.10 ms**.

The specific evidence for the attribution — that the offline prior costs latency
and Q-learning's switching recovers it — is gone. The arms are now
indistinguishable on latency within a tenth of a millisecond.

That is not automatically bad news for the method; it may mean the offline prior
costs nothing. But the paper does not claim that, and the experiment as repaired
cannot distinguish "the prior is free" from "the metric cannot see the
difference". Distinguishing those is new evidence, not a re-reading.

---

## 6. C17: a label defect that outlived its number

The paper's *"NSGA-II-guided mode 99.5%"* was always the `ga` arm, which
`DEFECT-001-LEO.md` §3.7 described as a genetic load balancer. That description
is wrong for this package — the arm is `GAWeightedRouter`, which selects a fixed
routing mode from the optimiser's weights, so "NSGA-II only" names the treatment
accurately (row R2). The number is now 98.50, and the label is now correct.

---

## 7. C18: not verifiable, and deliberately not called contradicted

The resilience claim of 62% versus 40%/42% at **10%** failure has no supporting
measurement. `metrics_extended.json` sweeps 2%, 4% and 8%; 10% is not in it.
"Searched and not found" is not "does not exist", and neither is it
"contradicted".

---

## 8. Four findings, kept separate

```
100.00 / 100.00 / 94.52      resilience, now per-arm and route-dependent
15.03 / 14.88 / 15.65 ms     latency, each arm's own measurement
183/185/179 obs, 17/15/21    disconnections, named rather than averaged in
62 vs 40/42 at 10%           not measured by this artifact
```

And one that is not a number:

```
240 ms                       disconnected-graph sentinel in the optimiser's
                             evaluator, a different path from the evaluation
                             loop, deliberately not unified with inf
```

---

## 9. What would need new evidence, not re-reading

1. **The attribution claim.** Establishing whether the offline prior costs
   anything requires a scenario where route choice changes latency. The sweep
   shows 98.3% of ISL pairs at positive SNR and dijkstra returning 1 hop on
   200/200 draws, so the metric cannot respond to failures across a wide range.
2. **The robustness claim.** "Most robust under stress" needs a scenario that
   actually separates the arms at high failure. At 8% the final delivery spread
   is 0.33 percentage points.
3. **The resilience claim.** Needs a failure rate in the swept set and a metric
   with a route-dependent path, both now available, neither yet run together.
4. **A clean latency statistic.** The final latencies exclude disconnections, so
   they are observations over 179–185 of 200 rounds. Any claim should state that
   coverage.

---

## 10. Ruling

Under the evidence regenerated after the sweep, **2 of 20 quantitative claims
survive** (C8 and C13), and one of those survives without being capable of
supporting a claim about method differences.

The manuscript's Table 1 was a faithful report of a pipeline that did not measure
what the paper says it measures. That is a provenance finding, not a collection
of stale numbers: the values were never wrong as *reports*; they were wrong as
*evidence*.

No manuscript claim is edited by this document.
