# QCE — Inventory and Lineage

**Status:** inventory and lineage complete. **No falsifier written yet. No
manuscript text edited. No number corrected.**
**Branch:** `fix/qce-audit-sweep`, created before the first commit. **Baseline:**
`97ed1cb`.
**Subject:** `FernandoMay/qce-ieee-package`.

This document establishes **implementation facts only**. Every entry is a statement
about what the code does, measured here, with no scientific interpretation and no
manuscript disposition. Per the standing rule, the chain runs
implementation fact → experimental implication → claim correspondence →
disposition, and this document is only the first link.

---

## 1. Reproduction

| artifact | result |
|---|---|
| `qce_simulator.py` → exit code | **0** |
| `figures/metrics.json` | **byte-identical** to the committed artifact (md5 `19e8419c9824a66ee4395281980969a7`) |
| `figures/*.png` (5 files) | **NOT byte-identical** |

The prior sweep recorded only the JSON. The figures were checked now.

**The figure difference is a rendering-environment difference, not a data
difference.** The regenerated `fig_comparison.png` has an IHDR width of 1483 px
against the committed 1484 px, and the maximum absolute pixel difference over the
overlapping region is 1.0 — a one-pixel canvas extent with the content shifted
accordingly. The underlying data is byte-identical, so no result changed; the
committed figures were produced under a different matplotlib/font environment than
the one that would regenerate them.

Recorded as a property of the reproducibility package: **the data artifact
reproduces byte-for-byte; the figures do not, and the paper does not say so.**

---

## 2. Lineage of the published numbers

`np.random.seed(SEED)` at `qce_simulator.py:32`, `SEED = 42`.
`N_SENSORS = 4`, `N_MITIGATIONS = 5`, so the configuration space is 2⁵ = 32.

| quantity | paper | artifact | status |
|---|---|---|---|
| QCE reliability | 0.924 | 0.9237 | exact |
| full-mitigation reliability | 0.912 | 0.9117 | exact |
| QCE errors | 0 | 0 | exact |
| full-mitigation errors | 0 | 0 | exact |
| power reduction vs full | 13.8% | **13.740%** | **does not round correctly** |

**Correction to DEFECT-003 §1.** The prior report recorded the power reduction as
"13.8% vs 13.75%, rounding". Recomputed from the artifact:

    (727.2826656034424 − 627.345737700338) / 727.2826656034424 = 13.7404%

13.740 rounds to **13.7**, not 13.8. The discrepancy is 0.06 percentage points —
small, and not a rounding. This is the only published number that does not trace.

**The predictor is on the dependency path.** This is not the `leo-routing` shape: the
mechanism is connected to the published number, and the numbers are real.

---

## 3. Implementation inventory

Answers to the six pre-registered hypotheses. These are hypotheses under test, not
findings; each is recorded as what the code does.

### H1 — Predictor: does the code implement the algorithm the paper names?

`ErrorPredictor` at `qce_simulator.py:157-187`. The update rule (lines 179-187):

```python
raw_pred = self.predict(observation, raw_only=True)
error    = actual_error - raw_pred
self.W  += self.lr * error * observation * raw_pred * (1 - raw_pred)
self.b  += self.lr * error * raw_pred * (1 - raw_pred)
```

This is the cross-entropy gradient of a logistic regression with respect to its
logits. `actual_error` is an observed binary label, not a reward signal.
The class docstring at line 158 reads `"""Lightweight RL-based error prediction
model."""` — the RL label is present **inside the code**, not only in the manuscript.

### H2 — `gamma`: does it participate causally in the result?

Occurrences of `\bgamma\b` in the entire simulator: **1**.

    166:  self.gamma = 0.9

Assigned once, never read. No return is ever computed, so there is nothing for a
discount factor to discount.

### H3 — "RL": is there a reward/state/action/update loop?

| element | occurrences |
|---|---|
| `reward` | 0 |
| `action` | 0 |
| `policy` | 0 |
| `Q_value` / `q_value` | 0 |
| `explore` | 0 |
| `epsilon` | 0 |
| `discount` | 0 |
| `gamma` | 1 (assignment only) |

There is no reward, no action space and no return. What exists is a supervised
logistic regression trained online by SGD on observed labels.

### H4 — QAOA: variational circuit or exhaustive enumeration?

`QuantumInspiredOptimizer.optimize` at lines 249-277:

```python
H_c = self._cost_hamiltonian(reliability_vals, energy_vals, latency_vals)
H_b = self._mixer_hamiltonian()                    # constructed
psi = np.ones(n_states) / np.sqrt(n_states)        # constructed
...
for state_idx in range(n_states):                  # 32 basis states
    state = np.zeros(n_states); state[state_idx] = 1.0
    exp_val = state.conj().T @ H_c @ state
    if exp_val < best_energy: ...
```

An exhaustive scan of all 32 computational basis states, returning the argmin of the
diagonal of `H_c`. No mixer is applied, no superposition is propagated, no
parameter vector is used, no evolution operator exists, no sampling occurs.

**Correction to DEFECT-003 §4: there are THREE dead quantum ingredients, not two.**
The report identified `H_b` and `psi`. Occurrence counts:

| symbol | occurrences | line |
|---|---|---|
| `self.params` | **1** | 201 |
| `H_b` | **1** | 253 |
| `psi` | **1** | 256 |
| `self.n_layers` | **1** | 200 |

`self.params = np.random.randn(n_layers * 2) * 0.1` is the parameter vector a
variational circuit would optimise. It is constructed and never read, which is the
single most direct piece of evidence that no variational optimisation takes place.
`self.n_layers` is likewise never used to build anything.

### H5 — Pareto: is there a population, frontier or artifact to support the term?

Occurrences in `qce_simulator.py`: `pareto` 0, `Pareto` 0, `hypervolume` 0,
`front` 0, `non-dominated` 0, `non_dominated` 0, `dominance` 0.

`optimize()` returns a **single** mask from a single argmin. No candidate set, no
front, no trade-off surface, no dominance test exists.

### H6 — Results: do the numbers reproduce independently of the narrative?

Yes. §1 and §2 above. Reproduction is exact and the published numbers trace.

---

## 4. Two items DEFECT-003 listed as "not verified" — now resolved

### 4.1 The C kernel diverges materially. **CONFIRMED.**

Compiled with `cc -O2` and executed:

| quantity | C kernel | NumPy / paper |
|---|---|---|
| Avg Reliability | **1.0000** | 0.9237 / 0.924 |
| Avg Power | 619.0 mW | 627.3 mW |
| Total Errors | 0 | 0 |
| workload | Tasks=8, Cores=4, Steps=200 | see §2 |
| precomputed configurations | 4 | 2⁵ = 32 scanned |

The kernel computes `total_reliability += expf(-es.health_metrics[t][3] / 1e6f)` —
an exponential form, not the simulator's reliability computation. It also carries a
compiler warning: `randf()` does `(float)rand() / RAND_MAX` with
`RAND_MAX = 0x7fffffff`, which as a float is 2147483648.

The paper (`:26`) says the framework "includes a reference C kernel for embedded
deployment", and the README (`:10`) calls it a "Reference C implementation". The
paper presents 0.924 as *the* result and never states that the C implementation of
the same framework yields 1.0000.

### 4.2 The ablation table has no code path. **CONFIRMED.**

Occurrences in `qce_simulator.py`: `NoSafety` 0, `NoRL` 0, `ablation` 0,
`Ablation` 0, `no_safety` 0, `no_rl` 0.

`paper/en/main.tex:447-449` reports three rows:

| Variant | Errors | Power | Reliability |
|---|---|---|---|
| QCE-NoSafety | 21 | 578.3 | 0.0070 |
| QCE-NoRL | 0 | 627.3 | 0.9237 |
| QCE (full) | 0 | 627.3 | 0.9237 |

Neither variant exists in the artifact. QCE-NoRL is numerically **identical** to the
full system to four significant figures, and `:456` explains this after the fact:
"Removing the RL predictor entirely (QCE-NoRL) produces identical results to full
QCE". The variant it is defined as — "identical to the Quantum-Only baseline" —
names a baseline that does not exist either: the simulator implements
`run_baseline_no_mitigation`, `run_baseline_reactive`,
`run_baseline_full_mitigation` and `run_baseline_energy_aware`.

---

## 5. Correction to this audit's own instruments — a fabricated finding, caught

I first measured the Chinese paper by grepping for `pareto` and `logistic`, and
recorded that the Chinese paper carried the strong labels with **zero** mechanism
disclosure. **That finding was false and does not exist.**

I searched English tokens in a Chinese document. `qce_simulator.py` and
`paper/en/main.tex` are English; `paper/zh/main.tex` is not. Re-measured with the
correct tokens:

| term | English token | Chinese token | count in zh paper |
|---|---|---|---|
| Pareto | `pareto` → 0 | 帕累托 | **5** |
| logistic regression | `logistic` → 0 | 逻辑回归 | **4** |
| SGD | `SGD` → 0 | 随机梯度下降 | **2** |
| reinforcement learning | → 10 | 强化学习 | 10 |
| QAOA | → 5 | QAOA | 5 |
| ansatz | → 0 | 拟设 | 3 |

`paper/zh/main.tex:28` reads, in full: "基于简化QAOA拟设的量子启发式优化器预先计算…
**帕累托最优**配置。在线强化学习预测器采用轻量级**逻辑回归**模型". The Chinese
paper discloses the mechanism **adjacent to the strong label**, exactly as the
English paper does at `:26`, `:45` and `:268`.

This is the `DEFECT-001 §5` failure — "I did not find X" is not "X does not exist" —
in a new form: **I did not search X** in the only place X appears. A search of the
wrong corpus reports a clean zero, which is indistinguishable from a genuine
absence, and reads as a finding rather than as a mistake. Recorded because a reader
of an earlier draft of this work would have seen the false claim.

**Presentation decks** (measured with the correct token for each language):

| deck | Pareto | logistic | RL abbreviation | QAOA |
|---|---|---|---|---|
| `pres/en` | 1 | 2 | `RL` ×5 | 1 |
| `pres/zh` | 0 | 1 | `RL` ×9 | 1 |

Both decks name the mechanism, and both carry the label predominantly as the
two-letter abbreviation `RL` — 5 and 9 occurrences respectively, against 2 and 1
mentions of logistic regression. The abbreviation is the highest-risk form of the
label: on a slide, the disclosure is the only mitigation and it is adjacent rather
than intrinsic.

---

## 6. Boundary

Nothing above is a finding about the manuscript. Established here:

- the simulator is seeded and reproduces its data artifact byte-for-byte;
- the published numbers trace to the artifact, one excepted;
- the predictor is a logistic regression with an unused `gamma`;
- the optimizer is an exhaustive 32-state scan with three dead quantum ingredients;
- no Pareto computation exists in the artifact;
- the ablation table has no code path;
- the C kernel diverges from the simulator by a material margin;
- the Chinese paper discloses the mechanism, contrary to what a wrong-token search
  suggested.

Not established, and not claimed:

- whether the framing is acceptable — that is claim correspondence;
- whether "RL predictor" is a fair label for supervised online logistic regression
  used as a risk classifier. **That is a scientific judgement about nomenclature, and
  it belongs to the disposition phase, not here.**
- whether exhaustive enumeration is the wrong algorithm for five binary mitigations.
  It is a reasonable choice. Only the description is in question.
- whether the ablation numbers were computed by some script outside the repository.

The next falsifier tests H3 and H5 behaviourally rather than by census, because a
token count is a textual check and H2 taught this sweep what that is worth.