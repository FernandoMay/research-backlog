# P1 Defect Report 002 — CRL, cognitive resilience layer

**Date:** 2026-09-30
**Package:** `FernandoMay/s01-crl-metacognitive`
**Corpus:** P1 research-hardening sweep. **Separate from the E1 dataset**, which is frozen at v1.0.
**Status:** Frozen. No number corrected, no file modified, no claim rewritten, no repair started.
**Method:** claim → metric definition → generating script → inputs → mechanism → causal reachability → re-run. README used only to locate the claim; the paper was read independently and, as it turns out, is more careful than the README.

---

## 1. The claim, in both places it appears

`README.md:39-40`:

| Configuration | Completion Rate |
|---|---|
| With CRL, benign baseline | 100.0% ± 0.0% |
| Without CRL, benign baseline | 100.0% ± 0.0% |

`latex/paper.tex:144-145`, identical figures.

Re-run reproduces exactly: `With CRL: 100.00% ± 0.00%`, `Without CRL: 100.00% ± 0.00%`, `Improvement: 0.0%`, `Total Modifications: 0`, `Avg Anomaly Score: 0.0300`. Seed is fixed at `20260909` for both `numpy` and `random`. No committed metrics artifact exists; the README table matches the run.

## 2. Finding — the invariance is introduced by the measurement, not by the phenomenon

This is the question the audit was ordered to ask: is `100% ± 0%` real invariance of the phenomenon, or invariance manufactured by the function that measures it?

**It is manufactured by the measurement.** The two arms differ in exactly one guard.

With CRL, `src/crl_simulation.py:269-274`:

```python
for node in ready_nodes:
    agent = next((a for a in agents if a.agent_id == node.agent_id), None)
    if agent and agent.state in (AgentState.IDLE, AgentState.EXECUTING):
        node.status = "completed"
```

Without CRL, `src/crl_simulation.py` in `run_comparison()`:

```python
for node in ready_nodes:
    node.status = "completed"
```

**The baseline never inspects the agent's state.** It marks every ready node completed unconditionally. Failure injection is present in both arms at `p = 0.20` per cycle, but in the baseline it has **no causal path to the completion metric**: an agent can be `FAILED` and its node is completed anyway.

The consequence is that the baseline would report 100% completion against a system where every agent is permanently failed. "Without CRL = 100%" is therefore not a measurement of the absence of resilience. It is a measurement of a baseline that ignores the stressor it is being compared against.

The experiment as constructed cannot exhibit a CRL benefit, and no improvement to the CRL itself would change that. This is an **instrument failure**, which is more fundamental than a correspondence failure between artifact and claim.

## 3. Finding — the CRL performs no control action in the reported experiment

`Total Modifications: 0`. The observe → evaluate → modify cycle never fires an intervention.

The DAG drains in the first few cycles, and `if dag.is_complete(): break` exits the 200-cycle budget before injected failures can accumulate enough to require a repair. The stressor rate and the completion criterion are mismatched to the workload size: 20 tasks over 10 agents is too easy for `p = 0.20` per cycle to bite.

So the reported experiment does not exercise the mechanism the paper specifies. The control plane is inert in the one configuration that is published.

## 4. Finding — the paper routes its primary claim to an experiment that does not exist

`latex/paper.tex:24`, abstract:

> "A separate stressed comparison with injected failures is included in the code and must be reported only after a fixed-seed repeated experiment."

`latex/paper.tex:150`:

> "The repository therefore includes a stressed mode with earlier failure injection and must be used for the primary resilience claim."

**There is no stressed mode.** `grep` for `argparse`, `sys.argv`, `add_argument`, `mode =` and `stress` across `src/crl_simulation.py` returns nothing. The module has exactly two entry points, `run_experiment()` and `run_comparison()`, both hardcoded to 10 agents, 20 tasks, and `failure_probability=0.20`. The stressor rate is not parameterised and cannot be changed without editing source.

The paper is correct that the benign experiment cannot support a resilience claim, and correct that the next step is a fixed-seed repeated experiment under stress. **The experiment it specifies as the primary route is absent from the repository**, so the required next step cannot be executed as described. The claim about the repository's contents is falsifiable and false.

## 5. What the paper gets right, and why that matters

The paper is more careful than the README at every point where they differ. It states, correctly:

- "no improvement is claimed for that benign condition"
- "This ceiling effect means that the benign experiment cannot measure resilience benefit"
- "The contribution is therefore the formal control-plane design and reproducible evaluation protocol, **not an unsupported resilience percentage**"
- the anomaly score is "a descriptive artifact metric, not evidence of detection accuracy" (run: 0.0300)
- the seed is fixed, and repeated trials are required before any claim

The README carries the bare `100% ± 0%` table with none of this framing. The scientific error is therefore **not** in the paper's interpretation — it is that the remedy the paper prescribes is unimplemented, and the README presents the uninterpretable version.

## 6. Classification

Three distinct defects, none of them a reproduction failure:

1. **Instrument failure.** The baseline has no causal path from the stressor to the metric. The experiment cannot exhibit the effect it is designed to test.
2. **Dormant mechanism.** The CRL records zero modifications; the reported configuration never exercises it.
3. **Absent artifact.** The stressed mode the paper names as the primary route does not exist in the repository.

Against the DEFECT-001 contrast, this is a **third** failure profile: `leo-routing`'s NSGA-II path produces meaningless numbers, `i01` produces real numbers that are misdescribed, and CRL produces a real number that the paper correctly refuses to interpret — while the experiment needed to interpret it is absent.

## 7. Not verified

- Whether the CRL's `run_cycle` can modify anything in any configuration. `Total Modifications: 0` is established for the published configuration only; the modifier's reachability under a harder workload is untested because no such configuration is exposed.
- Whether the tests in `tests/test_crl.py` pass. The package was installed and executed via `requirements.txt`; the test suite was not run.
- Whether a stressed mode existed in an earlier commit and was removed. The repository was cloned at depth 1; history was not examined, and no provenance is asserted either way.

## 8. Status

Frozen. No repair started. The required next step is a design decision, not a code edit: the baseline must be made to model failure before any stressed comparison can be meaningful, and the stressed configuration must be exposed as a parameter rather than a source edit. Both are recorded, neither is begun, per the standing rule that repairs are designed against the completed P1 sweep.
