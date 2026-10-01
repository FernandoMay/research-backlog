# CRL — claim inventory and lineage reconstruction

**Date:** 2026-09-30
**Baseline:** `cf37818` ("refactor: strengthen manuscript and reproducibility package"), tree clean at clone.
**Branch:** `fix/crl-audit-sweep`, created **before the first commit**.
**Status:** no code modified, no artifact regenerated, no manuscript edited. Reconstruction only.
**Code:** `src/crl_simulation.py` (one module), `tests/test_crl.py`, `latex/paper.tex`, `README.md`.
**No committed artifact.** Results are printed to stdout; the repository stores no JSON or CSV.

---

## 0. Destination gate

```
branch at clone   main
branch created    fix/crl-audit-sweep   ← before any commit
```

---

## 1. Observed output

```
--- Single Experiment ---
Completion Rate: 100.00%
Total Modifications: 0
Avg Anomaly Score: 0.0300
DAG Complete: True

--- Comparison: With vs Without CRL ---
With CRL:    100.00% ± 0.00%
Without CRL: 100.00% ± 0.00%
Improvement: 0.0%
```

Runtime 0.2 s. The paper reports an average anomaly of 0.02; the committed code
prints 0.0300 — a difference to reconcile, recorded in §6 rather than resolved here.

---

## 2. Claim inventory

| # | claim | loc | type | published | evidence |
|---|---|---|---|---|---|
| **C1** | "With CRL 100.0% ± 0.0%" | L144, README L39 | measurement | 100.0 ± 0.0 | reproduced |
| **C2** | "Without CRL 100.0% ± 0.0%" | L145, README L40 | measurement | 100.0 ± 0.0 | reproduced |
| **C3** | the comparison attributes a resilience difference | L146–151 | causal inference | "Improvement: 0.0%" | **no arm's completion rate responds to the stressor — see §3** |
| **C4** | "This ceiling effect means that the benign experiment cannot measure resilience benefit" | L150 | self-limitation | — | **correct, and confirmed** |
| **C5** | "The repository therefore includes a **stressed mode with earlier failure injection** and must be used for the primary resilience claim" | L151 | falsifiable claim about the repository | — | **FALSE — no stressed mode exists** |
| **C6** | anomaly score 0.02 is "a descriptive artifact metric, not evidence of detection accuracy" | L155 | self-limitation | 0.02 | **correct, and confirmed** |
| **C7** | results are "a software-architecture prototype and not a validated production resilience guarantee" | L158 | limitation | — | **correct, and confirmed** |

**Four of seven claims are the manuscript limiting itself, and every one of those limitations is accurate.** This package is not a case of overclaiming. Its defect is narrower: a falsifiable statement about the repository's own contents is false, and the primary experiment has no causal path to the property it is set up to measure.

---

## 3. The causal chain the paper needs, and where it breaks

The comparison is meant to vary one factor — the presence of the control plane — and observe completion under injected failures. Tracing both arms as written:

```
with CRL      crl.run_simulation(...)        failure_probability = 0.20
  for node in ready_nodes:
      if agent and agent.state in (IDLE, EXECUTING):  node.status = "completed"   ← guarded

without CRL   inline loop in run_comparison  failure_probability = 0.20
  for node in ready_nodes:
      node.status = "completed"                                              ← UNGUARDED
```

The baseline marks a node completed **regardless of the assigned agent's state**. The failures are still injected; they simply do not reach the outcome.

Faithful replication of each arm, varying only the failure probability:

| p_fail | cycles | CRL completion | CRL failed agents | CRL mods | baseline completion | baseline failed agents |
|---|---|---|---|---|---|---|
| 0.05 | 4 | 100.00% | 0 | 0 | 100.00% | 0 |
| 0.20 | 4 | 100.00% | 0 | 0 | 100.00% | 0 |
| 0.50 | 4 | 100.00% | 0 | 0 | 100.00% | 0 |
| 0.90 | 4 | 100.00% | 0 | 6 | 100.00% | **3** |
| 1.00 | 6 | 100.00% | 0 | 11 | 100.00% | **4** |

**At p = 1.00 the baseline has four permanently failed agents and still reports 100% task completion.** That is the defect in one line, and it is not a subtle one.

Two further facts, both behavioural:

- **The CRL arm ends with zero failed agents at every p.** The control plane restores them; that is what its 6→11 modifications do. So the arms differ in agent survival and are identical in the reported metric.
- **The DAG drains in 2–6 cycles regardless of p.** The failure mechanism has at most a handful of draws in which to fire. At the default `failure_probability = 0.05` used by `run_experiment`, the expected number of failures across a four-cycle run is 0.2.

So the stressor is applied and then ignored, on one arm, and applied and repaired on the other, while both report the same ceiling. **Neither arm's completion rate is a function of the failure rate.**

---

## 4. C5: the repository does not contain a stressed mode

The claim is specific: a stressed mode, with *earlier* failure injection.

```
grep -rniE "stress|earlier|severe|hard_mode|--stress"  src/  tests/  README.md
  → no occurrence
```

The only knob is `failure_probability`, a parameter of `run_simulation`. It
changes the *rate* of injection, not the *timing*. Nothing injects earlier than
the top of the first cycle, and nothing prevents the DAG from draining first.
There is no CLI: `__main__` hard-codes `SimulationRunner(num_agents=10,
num_tasks=20)` and calls two methods with no arguments.

The paper's instruction — "must be used for the primary resilience claim" — is
therefore unexecutable as described. Not because the required experiment is
conceptually impossible, but because the mode the paper names is not in the
repository. That is a falsifiable claim, and it is false.

---

## 5. Layered reading

| layer | question | state |
|---|---|---|
| **R1** | does the mechanism work — does the control plane change anything? | the control plane *does* restore failed agents (6→11 modifications as p rises). But the reported metric cannot register it, so R1 is untestable **through the artifact**, not through the code |
| **R2** | is the stressor actually applied as an experimental condition? | **no** — applied and ignored in the baseline; applied and drained-over in the CRL arm |
| **R3** | nomenclature and provenance | **no committed artifact exists**; the paper's stressed-mode claim is false; the README reproduces the two ceiling numbers without the paper's caveats |

The separation matters. R1 and R2 are different defects with different repairs,
and R3 is a documentation defect that should not be repaired by changing a
number.

---

## 6. Open, not resolved here

- The anomaly score differs: paper 0.02, code 0.0300. Not reconciled in this document.
- The hard-coded `10 agents / 20 tasks / failure 0.05 and 0.20` are recorded as
  configuration the artifact does not expose, per the inventory discipline.
- `tests/test_crl.py` was not executed. This document makes no claim about it.

No repair is designed. The falsifiers come next, beginning with the control this
package needs and LEO did not:

> **The experiment must have causal access to the property it claims to measure.**
> An arm whose metric ignores the stressor cannot report the effect of removing
> a mechanism, at any failure rate.