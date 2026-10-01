# CRL — claim adjudication

**Date:** 2026-09-30
**Evidence state:** inventory `b5d97c8`, CRL-F1 `b676a0c`, CRL-F2 `9ffc31f`, R2 `b197d10`.
**Branch:** `fix/crl-audit-sweep`.
**Manuscript:** not edited.
**Artifact:** `data/resilience_experiment.json`, byte-identical across two runs.

---

## 0. Why adjudication precedes the gate

R2 changed what this package means. Before R2 the primary experiment never
exercised the mechanism, so nothing in it could be attributed to the control
plane. After R2 the causal pathway is active and equalised — and the two arms
still report the same completion. Freezing branch integrity now would certify a
chain whose central number cannot distinguish the arms.

The temptation is to read the repaired 100% as positive evidence of resilience.
It is not. See §3.

---

## 1. Claim matrix

| class | claim | disposition | basis |
|---|---|---|---|
| **Mechanism** | the CRL retains completions and recovers agents | **SUPPORTED** | the guard withheld 3 completions and the arm performed 3 control-plane modifications, ending with 0 failed agents |
| **Causal access** | the guard can change the reported outcome at a matched dose | **SUPPORTED** | row F1: dose 3, guarded 55.00% vs unguarded 100.00% |
| **Activation** | a configuration exists that places the stressor inside the causal window | **SUPPORTED** | row R2: targeted injection, dose calibrated and capped at 2 in both arms; the published entry point now exercises the guard in 6 cycles |
| **Equal exposure** | the arms differ in one condition | **SUPPORTED** | both received dose 2; the control recorded 0 modifications, so it is genuinely unguarded |
| **Metric** | completion rate distinguishes resilient operation from unverified operation | **NOT VERIFIED** | both arms report 100.00%. In the control arm **2 of the 20 completions were written while the assigned agent was FAILED**; in the CRL arm 0 were. The metric cannot tell the two situations apart |
| **Resilience benefit** | the CRL improves completion under stress | **NOT SUPPORTED** | difference is 0.00% on the primary metric. Not contradicted either — the metric cannot register a benefit even if one exists, which is precisely the defect |
| **Anomaly score 0.02** | published anomaly corresponds to the repository as committed | **NOT VERIFIED / PROVENANCE GAP** | 0.02 is reachable from this code under 5 of 200 seeds; the repository pins 20260909, which gives 0.0300; no artifact, seed or configuration is recorded for the published value |
| **Anomaly semantics** | "anomaly" carries one definition | **CONTRADICTED** | one run carries two silent averaging populations: per-cycle values `[0.0000, 0.0600]` averaging 0.0300, and `observer.anomaly_scores` `[0.0600]` averaging 0.0600. `detect_anomaly` returns 0.0 before two states exist and never appends it |
| **Experimental activation (as published)** | the published configuration exercises the mechanism | **NOT VERIFIED as published; SUPPORTED after R2** | the committed `run_experiment` withheld 0 completions across its 2-cycle window. R2 adds the entry point the manuscript says exists and instruments the published one |
| **Repository contents** | "the repository includes a stressed mode with earlier failure injection" | **CONTRADICTED (pre-R2); SUPPORTED (post-R2)** | no occurrence of `stress`, `earlier`, `severe` or `--stress` existed in `src/`, `tests/` or `README.md`. R2 adds `run_stressed_experiment`. The manuscript's claim was falsifiable and was false |

---

## 2. What the paper says, and what survives of it

The manuscript is not an overclaiming document here. Four of seven inventoried
claims are it limiting itself, and every one of those limitations is accurate:

| paper | status |
|---|---|
| "This ceiling effect means that the benign experiment cannot measure resilience benefit" (L150) | **correct, and confirmed** — row F1a reproduced the ceiling at every failure rate |
| "The anomaly score is a descriptive artifact metric, not evidence of detection accuracy" (L155) | **correct** |
| "a software-architecture prototype and not a validated production resilience guarantee" (L158) | **correct** |
| "must be interpreted as" limitations on synthetic models, partitions, recovery deadlines | **correct** |

The paper's self-limitations are stronger than its own evidence requires. That
is the opposite of the pattern found in LEO and ISAC, and it is worth recording
as such rather than being averaged away.

The one paper claim that was false is about the repository's own contents, and
R2 makes it true.

---

## 3. The metric-semantics defect, left open

This is a **finding**, not a failure of R2, and it is not repaired here.

```
with CRL     completion 20/20 = 100.00%   falsely marked: 0   agents FAILED at end: 0
without CRL  completion 20/20 = 100.00%   falsely marked: 2   agents FAILED at end: 2
```

Both arms report 100%. In one arm every completion reflects delivery after
recovery. In the other, **two completions were written while the assigned agent
was FAILED** — the arm reports success for work it never verified.

The completion metric counts task completions without distinguishing *delivered*
from *falsely marked*. It therefore scores the arm that checks nothing
identically to the arm that recovers. R2 activated the mechanism and equalised
the dose; it did not change what "completed" means, and repairing that would
mean redefining the experimental outcome rather than the configuration.

**Disposition: NEW EXPERIMENT REQUIRED.** Any claim that the CRL improves
completion under stress is unaddressable with this metric, in either direction.

---

## 4. Superseded states

| claim | before R2 | after R2 | state |
|---|---|---|---|
| mechanism active | 0 guard opportunities in the published run | 3 withholds, 3 modifications | SUPERSEDED BY REPAIRED EVIDENCE |
| arms comparable | doses differed by construction | both dose 2, control clean | SUPERSEDED BY REPAIRED EVIDENCE |
| results lineaged | stdout only | artifact with commit, seed, config, dependencies | SUPERSEDED BY REPAIRED EVIDENCE |
| anomaly 0.02 | unreachable lineage | **unchanged** — R2 does not repair it | **still a provenance gap** |
| metric semantics | conflated | **unchanged** | **still conflated, now quantified** |

The repaired 100% is **not** positive evidence of resilience. It is the same
number the unverified arm produces for a different reason, and the artifact now
records why.

---

## 5. Frozen

CRL claims are adjudicated. No manuscript claim is edited.

```
Mechanism            SUPPORTED
Causal access        SUPPORTED
Activation (R2)      SUPPORTED
Equal exposure       SUPPORTED
Metric discrimination NOT VERIFIED
Resilience benefit   NOT SUPPORTED
Anomaly 0.02         NOT VERIFIED / PROVENANCE GAP
Anomaly semantics    CONTRADICTED — two silent populations
Stressed mode claim  was false, now true
```

Three items remain open and are recorded rather than repaired: the metric's
semantics, the anomaly provenance gap, and the absence of any claim-level
justification for the published 0.02.

The publication gate follows and must verify that this distinction survives it.