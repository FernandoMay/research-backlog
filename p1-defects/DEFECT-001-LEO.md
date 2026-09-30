# P1 Defect Report 001 — LEO routing and LEO edge orchestration

**Date:** 2026-09-30
**Corpus:** P1 research-hardening sweep. **Separate from the E1 dataset**, which is frozen at v1.0 and is not re-adjudicated on the basis of findings in this document.
**Status:** Both packages frozen. No number corrected, no file modified, no claim rewritten.
**Method:** code first, then artifact, then paper. README was not used as a source for any finding below.

---

## 1. The contrast this pair establishes

| Package | Reproduces | Mechanism ↔ declared claim | Failure |
|---|---|---|---|
| `leo-routing-itft2026-package` | Yes, bit-exact | **No** | Deterministically decoupled optimisation |
| `i01-leo-edge-orchestration` | Yes, to the decimal | **Yes**, for the mechanism | Internal document and provenance failure |

**Both packages reproduce.** A single reproducibility verdict cannot separate them, because on that criterion they are identical. They differ in what the reproduction licenses a reader to conclude.

This is an empirical demonstration that reproduction and correspondence are orthogonal dimensions. It is the clearest case available so far for why the frozen rubric keeps L2 (reproduction) and U3 (relation) as independent layers rather than collapsing them into one quality score.

## 2. What may and may not be concluded

Not:

> these packages are not reproducible.

Yes:

> Both packages are reproducible. Reproducibility alone determines neither whether a result corresponds to the mechanism declared to produce it, nor whether the document represents the result obtained. In `leo-routing` the numbers are faithful to code that computes an unrelated function. In `i01` the numbers are faithful to a real simulation, and the description around them is what fails.

## 3. Package A — `leo-routing-itft2026-package`

### 3.1 Mechanism

`simulator/leo_routing_simulator.py:158-200`, inside `nsga2_optimize()`:

```python
for chrom in chromosomes:
    latency    = np.random.uniform(20, 50)
    resilience = np.random.uniform(60, 95)
    coverage   = np.random.uniform(60, 95)
    w = chrom['weights']
    score = -(w[0] * latency - w[1] * resilience - w[2] * coverage)
```

Formally the evaluator computes `f(x) = R`, with `R` independent of `x`. The chromosome's weight vector multiplies three quantities that were already drawn. Consequences, in order of severity:

1. The objective does not depend on the solution, so changing the solution cannot change the evaluation.
2. The Pareto front is structure in noise, not a latency–resilience–coverage trade-off.
3. Crossover is decorative: averaging weights of two chromosomes scored independently of those weights produces no gradient toward anything.

`np.random.seed(42)` at line 36 makes the defect **exactly reproducible**. Reproducible noise is more damaging than nondeterminism, because a re-run confirms it and lends false confidence.

### 3.2 Reproduction

First two attempts failed — missing `matplotlib`, then `matplotlib.pyplot` not stubbable as a submodule. The artifact comparison was reported as **void** at that point rather than as a false match. With dependencies in a venv:

- exit 0
- **0 of 12** result fields differ
- `optimal_weights {0.651, 0.106, 0.243}` bit-identical

### 3.3 Second, independent defect

`avg_resilience_pct = 77.83` and `avg_coverage_pct = 100.0` are **identical across all three variants** — `dijkstra`, `nsgaii_offline`, `nsgaii_plus_qlearning`. Computed per routing strategy they would differ. They are not being computed per-algorithm.

### 3.4 Reach into the paper

| Location | Claim |
|---|---|
| `paper/main.tex:33` abstract | "NSGA-II for offline Pareto-optimal routing policy generation"; "simultaneously optimizes three conflicting objectives"; ablation attributes performance to "the NSGA-II offline Pareto prior" |
| `paper/main.tex:57` | contribution 1: "generates a Pareto-optimal library of routing policies offline" |
| `paper/main.tex:121` | "Each chromosome encodes a weight vector that parameterizes the routing objective function" — states the exact mechanism the code does not implement |
| `paper/main.tex:184` | `w*` seeds the Q-table and defines the balanced routing mode |
| `paper/main.tex:240` | "NSGA-II optimization provides marginal latency improvement (24.17 ms) … due to its weight-optimized path selection" |

Numbers reaching the paper: `24.35`, `24.17`, `25.1`, `80.0`, `74.5`, `78.0`, `77.83`. **`0.651` does not appear.** The optimised weight vector is never published as a number, but the claim that it was *obtained by optimisation* is falsifiable and false — the concrete value need not appear for a claim about its provenance to be checkable.

### 3.5 Salvage path

The repository is not uniformly invalid. `compute_latency_ms(snr_matrix, active_mask, route_type)` at line 259 **takes the actual routing action**. `leo_routing_extended.py` imports it and calls it as `compute_latency_ms(env.snr_matrix, active_mask, act)` at lines 286, 300, 322 and 341, inside `evaluate_strategy(env_factory, router_mode)`. The Q-learning training loop rewards on the resulting latency. The decoupled draw does not appear in the extended simulator at all.

Dijkstra, ACO, DQN, Q-learning and the failure sweeps are causally connected. Exactly one function is broken, and it is the function the paper's central contribution rests on. The repair is to make the chromosome actually parameterise an evaluation that traverses the environment — using machinery that already exists in the same file. **Not started, by design** (see §6).

**A correct implementation elsewhere in the same repository does not rescue the incorrect implementation that produced the published numbers.** Provenance of the number governs, not the presence of a working alternative.

## 4. Package B — `i01-leo-edge-orchestration`

### 4.1 Reproduction passes

`src/simulation.py:492-493` sets `np.random.seed(20260909)` and `random.seed(20260909)`. Three consecutive runs, identical every time:

| | avg latency | deadline met | tasks | exec time |
|---|---|---|---|---|
| XING | 28.0745 s | 39.53% | 941 | 0.0627 s |
| PSO | 0.4024 s | 98.72% | 941 | 0.3779 s |
| GA | 0.4025 s | 98.72% | 941 | 1.8636 s |
| `latex/paper.tex:170-172` | 28.07 / 0.40 / 0.40 | 39.5 / 98.7 / 98.7 | — | 0.047 / 0.415 / 1.815 |

The table reproduces the code. There are **no committed data artifacts** — no JSON, no CSV — so the table exists only in the paper. Because it reproduces, that is a provenance gap rather than a correctness gap. `requirements.txt` supports a clean-venv run, which is better discipline than Package A.

### 4.2 Defect 1 — the comparison is ill-posed

`XINGOrchestrator._calculate_reward` (line 185) optimises four criteria:

```
compute_score * 0.5 + energy_score * 0.3 - queue_penalty + priority_bonus
```

`PSOOptimizer._evaluate` (line 304) and `GAOptimizer._fitness` (line 383) have **byte-identical bodies** and optimise one:

```
load_factor = sat_loads[sat_id] / 10.0
total_cost += load_factor
```

The baselines never read `energy_level`, `queue_length`, `task.priority` or `task.computational_load`. XING is a multi-criteria greedy assignment; PSO and GA are load balancers. The ~70× latency gap is not evidence that load balancing outperforms multi-criteria assignment. It is evidence that the two were never solving the same problem.

This is a **problem-definition failure**, kept distinct from U3: the artifact executes, and its semantics match its own code. What does not match is the framing that presents the result as a comparison.

### 4.3 Defect 2 — the conclusion contradicts the results

`latex/paper.tex:193`:

> "Our experimental results demonstrate **significant improvements over classical optimization methods** in latency, deadline compliance, and execution efficiency."

The paper's own table shows the opposite on the first two: 28.07 s against 0.40 s, and 39.5% against 98.7%. XING wins only on assignment runtime.

`latex/paper.tex:177`, the discussion, states it correctly:

> "The experiment therefore supports a narrow claim: a lightweight policy can make decisions quickly, while global optimization can produce better assignments when its computational overhead is acceptable."

The results section is honest and the conclusion contradicts it. This is a **within-document contradiction**, not an artifact-to-claim failure.

### 4.4 Defect 3 — the abstract is from a superseded run

| quantity | abstract, `paper.tex:24` | table, `paper.tex:170-172` | this run |
|---|---|---|---|
| tasks | 955 | — | 941 |
| assignment phase | 0.037 s | 0.047 s | 0.0627 s |
| XING latency | 31.24 s | 28.07 s | 28.0745 s |
| XING deadline | 37.2% | 39.5% | 39.53% |
| PSO/GA latency | 0.41–0.42 s | 0.40 s | 0.4024 / 0.4025 s |
| PSO/GA deadline | ~98.1–98.2% | 98.7% | 98.72% |

The table matches the code. The abstract matches nothing in the repository. It is the most-read part of the paper and the part that does not reproduce. This is a **temporal provenance failure**: a superseded run persisted in the section readers encounter first.

## 5. A finding about the audit process itself

While auditing Package B, an initial search for `seed` returned no match, and the near-conclusion was that the source was unseeded. The seeds are at lines 492 and 493. The search output had been truncated by a `head` limit before reaching them.

Recorded because it is a property of the method, not an anecdote:

> **"I did not find X" is not "X does not exist."** A truncated search is indistinguishable from an absent one unless the output is checked for completeness.

Any audit instrument that reports absence must distinguish *searched and not found* from *not searched*. Package A's reproduction was likewise reported as void after two failed runs, rather than as a match, and that discipline is the reason the void was caught.

## 6. Status and sequencing

- No number was changed. No file in either repository was modified.
- `25add0a` (E1 frozen dataset and methodology paper) is untouched.
- **`nsga2_optimize` repair is deliberately not started.** It will be designed against the completed P1 sweep rather than against the first finding, so the repaired objective preserves the properties the paper actually needs.
- These packages are **not** added to the E1 dataset. E1 is frozen at v1.0; a single new instance does not license re-adjudication, and the rubric's own assignment rule keeps these as separate records.

## 7. Not verified

- Whether the extended simulator in Package A reproduces. It does not complete within 120 s; its reproducibility is unverified and open.
- Whether Package B's test suite and Dockerfile run. Installed and executed from `requirements.txt`; the tests were not executed.
- The provenance of Package B's abstract numbers. The code cannot produce them, but which earlier run or configuration did is not recorded anywhere in the repository.
