# P1 Defect Report 003 — QCE, quantum-classical co-design

**Date:** 2026-09-30
**Package:** `FernandoMay/qce-ieee-package`
**Corpus:** P1 research-hardening sweep. **Separate from the E1 dataset**, frozen at v1.0.
**Status:** Frozen. No number corrected, no file modified, no claim rewritten, no repair started.
**Method:** claim → implementation → dependency path to the published number, with `artifact → result`, `artifact → README claim` and `artifact → paper claim` kept separate, per the CRL precedent that a paper can be more rigorous than its own README.

---

## 1. Reproduction passes, and the published numbers trace

`qce_simulator.py` run to completion in a clean venv: **exit 0, `figures/metrics.json` byte-identical to the committed artifact.**

| quantity | paper | artifact | |
|---|---|---|---|
| QCE reliability | 0.924 | 0.9237 | exact |
| full-mitigation reliability | 0.912 | 0.9117 | exact |
| power reduction vs full | 13.8% | 13.75% | rounding |
| QCE / full errors | zero | 0 / 0 | exact |

The predictor **is** on the dependency path to the published number. This is not the `leo-routing` shape: the mechanism is connected, and the results are real and correctly reported.

One note on method: an earlier comparison reported the artifact as identical while the simulator had crashed on a missing `scipy` import and never regenerated the file. That comparison was void and was not treated as a match. Reproduction was re-established only after a clean run.

## 2. Finding — the "RL predictor" is supervised logistic regression

`ErrorPredictor` at `qce_simulator.py:157`. The update rule:

```python
error = actual_error - raw_pred
self.W += self.lr * error * observation * raw_pred * (1 - raw_pred)
self.b += self.lr * error * raw_pred * (1 - raw_pred)
```

This is exactly the cross-entropy gradient of a logistic regression. `actual_error` is an observed label, not a reward.

RL machinery census across the whole simulator:

| element | occurrences |
|---|---|
| `reward` | 0 |
| `action` | 0 |
| `policy` | 0 |
| `Q_value` | 0 |
| `explore` | 0 |
| `epsilon` | 0 |
| `discount` | 0 |

**`self.gamma = 0.9` is assigned at line 166 and never read again.** No return is ever computed, so there is nothing for a discount factor to discount. It is a vestige of a Q-learning design that was not completed, and it is the clearest single piece of evidence about what the component was intended to be.

## 3. Finding — "Pareto-optimal configurations" has no corresponding computation

`grep -ciE "pareto|hypervolume|front|non-dominated|non_dominated" qce_simulator.py` returns **0**.

The abstract states the optimizer "pre-computes **Pareto-optimal** configurations". `optimize()` at line 249 returns a **single** mask from a single argmin. There is no set of candidates returned, no front, no trade-off surface, no dominance test. A single-point argmin is not a Pareto computation, and the property is not merely unimplemented — it has no referent in the artifact.

## 4. Finding — the "simplified QAOA ansatz" is exhaustive enumeration of 32 basis states

`optimize()` at lines 249-277:

```python
H_c = self._cost_hamiltonian(...)
H_b = self._mixer_hamiltonian()          # constructed
psi = np.ones(n_states) / np.sqrt(n_states)   # constructed
...
for state_idx in range(n_states):        # n_states = 2^n_qubits = 32
    state = np.zeros(n_states)
    state[state_idx] = 1.0               # computational basis state
    exp_val = state.conj().T @ H_c @ state
    if exp_val < best_energy: ...
```

`H_b` and `psi` each occur **once** in the entire file — at construction. There is no mixer applied, no superposition propagated, no parameter vector, no evolution operator, no sampling, no expectation over bitstrings. The routine is an exhaustive scan of all 32 computational basis states returning the argmin of the diagonal of `H_c`.

For five binary mitigations this is a perfectly reasonable algorithm, and exhaustive search may well be the right choice. The defect is the description, not the method.

## 5. What the paper discloses, and where

This is the decisive part of the classification, and it separates QCE from every other package in the sweep.

Every place the paper uses the stronger label, it states the actual mechanism adjacent to it:

| location | text |
|---|---|
| `paper/en/main.tex:26` abstract | "an online reinforcement learning predictor … The online RL predictor, **implemented as lightweight logistic regression** with safety-bounded predictions" |
| `paper/en/main.tex:45` | "Online RL-based error prediction **using lightweight logistic regression** with online stochastic gradient descent" |
| `paper/en/main.tex:268` | "**We employ a logistic regression model**" |
| `paper/en/main.tex:244` | "The offline optimization evaluates $2^{N_M} = 32$ configurations per risk level" — an honest statement of exhaustive enumeration, in the same paper whose abstract calls it a variational QAOA ansatz |
| `README.md:64` | "Online RL predictor (logistic regression, online SGD, safety-bounded)" |

So a reader is never left believing an RL update is happening, and never left believing a variational circuit is running. The README is the tersest of the three and still names the mechanism in the same line.

**The paper's contribution framing is what is at issue, not a concealed mechanism.** The headline is "Quantum-Classical Co-Design … combining a quantum-inspired variational optimizer with an online reinforcement learning predictor". Removing the labels the artifact supports, the contribution is: an exhaustive offline search over 32 mitigation configurations, plus a supervised online logistic-regression risk classifier, plus a lookup that maps a predicted risk level to a precomputed configuration. That is a coherent and potentially useful design. It is not quantum-classical co-design with a variational optimizer and an RL predictor.

## 6. Classification

Reproduces: **yes**. Mechanism connected to the published result: **yes**. Numbers real and correctly traced: **yes**.

Three findings, all in the same class, and none of them concealed:

1. **Category misattribution.** A supervised logistic regression is labelled reinforcement learning throughout the framing, and the dead `gamma` shows the label was not incidental.
2. **Property with no referent.** "Pareto-optimal" is asserted in the abstract for a routine that returns one point from an argmin.
3. **Method misdescription.** A variational QAOA ansatz is claimed for an exhaustive basis-state scan whose two quantum ingredients are constructed and discarded.

This is a **fourth failure profile** in the sweep, and the cleanest one: the artifact is sound, the numbers are right, and the defect is entirely in the vocabulary attached to them — disclosed rather than hidden.

| Package | Reproduces | Numbers real | Defect location |
|---|---|---|---|
| `leo-routing` NSGA-II | yes | **no** | the function that computes them |
| `leo-routing` extended | yes | yes | experiment design, and one label |
| `i01` | yes | yes | document framing and provenance |
| `CRL` | yes | yes | the instrument, and an absent experiment |
| `QCE` | yes | yes | the vocabulary |

## 7. Not verified

- Whether the C reference kernel's output matches the NumPy results. A prior sweep reported the kernel returning reliability `1.0000` against the paper's `0.924`; that was not re-checked here and is inherited as unverified.
- Whether the ablation table in the paper has a committed code path. A prior sweep reported the `NoSafety` and `NoRL` rows having none; not re-checked here.
- The Chinese-language paper and the presentation decks were not read. If they carry the same framing, the classification extends to them, but that is not established.
