# P1 Defect Report 006 — Quantum-K-SAT, QAOA simulation

**Date:** 2026-09-30
**Package:** `FernandoMay/quantum-k-sat-ieee-package`
**Corpus:** P1 research-hardening sweep. **Separate from the E1 dataset**, frozen at v1.0.
**Status:** Frozen. No number corrected, no file modified, no claim rewritten, no repair started.
**Method:** quantum claim → artifact → state/Hamiltonian/mixer/parameters → evolution or search → measurement/sampling → published metric → paper and README, with the four-way classification applied to each named mechanism separately.

---

## 1. What the package does get right

The top-level framing is honest and should be recorded before anything else.

`paper/main.tex:22`: *"Through **exact state-vector simulation** of up to 14 qubits and 63 clauses"*. The paper says plainly that this is a classical simulation. `H_B = \sum_j X_j` is the standard QAOA mixing Hamiltonian, the initial state is written as $\ket{+}$, and the framework description at lines 53-58 matches the actual layer structure in `qaoa_run`: `cost_op` then `mixer`, repeated `p` times. The cost Hamiltonian `make_H` is a correct diagonal of unsatisfied-clause counts, and `cost_op` and `mixer` each preserve the norm exactly (verified: 1.000000 after each).

**This is not a package claiming quantum hardware it does not have.** The framing is category 2 — a classical simulation of a quantum algorithm, honestly labelled.

The findings below are therefore all narrower than "it is not quantum". They concern three specific mechanism names.

## 2. Finding — "measurement" is a top-10 exact-amplitude oracle

`best_sat_from_state`, line 69:

```python
probs = np.abs(state)**2
probs /= probs.sum()
top = np.argsort(probs)[-10:]
for idx in top:
    bits = [int(x) for x in format(idx, f'0{n}b')]
    best = max(best, sat_ratio(bits, clauses))
```

This reads the **complete** probability distribution — available only because the simulator keeps the full state vector — selects the ten most probable computational basis states, evaluates the satisfaction ratio of each, and returns the **maximum**.

A measurement performs one Born-rule draw and returns one bitstring. It cannot see the full distribution, and it cannot return the best of ten. This function is an oracle over exact amplitudes, and it is the sole path from the simulated state to every published satisfaction ratio, including the "measurement errors dominate" conclusion at line 190 and the readout-calibration result.

**Magnitude not established.** On a 6-qubit, 12-clause instance both the oracle and a single Born draw returned 1.0, so the divergence was not demonstrated numerically here. The structural difference is established by reading the code; the size of the effect is **not** claimed.

## 3. Finding — "variational" parameters are optimised by random search

`optimize_qaoa`, line 98:

```python
for _ in range(iters):
    g = np.random.uniform(0, np.pi, p)
    b = np.random.uniform(0, np.pi, p)
    state, _ = qaoa_run(clauses, n, p, g, b, noise)
    e = np.real(np.conj(state) @ (H * state))
    if e < best_e: best_e, best_p = e, (g.copy(), b.copy())
```

$\boldsymbol{\gamma}$ and $\boldsymbol{\beta}$ are drawn uniformly at random and the best of 40 draws is kept. There is no gradient, no parameter-shift rule, no classical optimiser of any kind. QAOA is by construction a *variational* algorithm whose defining feature is that a classical optimiser tunes those parameters; a random search over the same space is not variational optimisation, and the paper's own framework section calls them "variational parameters".

## 4. Finding — the "depolarizing channel" is not a channel

`qaoa_run`, line 57:

```python
state = (1-noise)*state + noise*np.ones(N,complex)/N
```

The second term is **not** a normalised state. `np.ones(N)/N` has squared norm $N\cdot(1/N)^2 = 1/N$, which for the paper's 12-qubit setting is $1/4096$. Measured on the state itself:

| | ‖ψ‖² |
|---|---|
| unitary path, no noise | 1.000000 |
| after noise = 0.1 | 0.821289 |
| after noise = 0.2 | 0.660156 |
| after noise = 0.3 | 0.516602 |
| after noise = 0.5 | 0.282227 |

A physical channel is trace-preserving and cannot reduce the norm. This is a coherent superposition admixture whose magnitude shrinks, and the shrinkage grows with the qubit count. The correct $\ket{+}$ would be `np.ones(N)/np.sqrt(N)`, whose squared norm is 1.000000.

Consequence: the noise axis in the paper's Figure 1 and in the `noise` experiment does not correspond to depolarising error, and the readout-versus-gate-noise conclusion drawn at line 190 rests on it.

## 5. Finding — the baseline comparison uses different instances

`exp_noise`, line 117:

```python
for t in range(6):
    cl = gen_3sat(n, m)          # QAOA: six fresh instances
    ...
for _ in range(6):
    cl = gen_3sat(n, m)          # WalkSAT: six DIFFERENT fresh instances
    ws.append(walk_sat(cl, n, 2000))
rs = np.mean([sat_ratio(np.random.randint(0,2,n), cl) for _ in range(100)])
```

QAOA and WalkSAT are evaluated on **two disjoint sets of six instances**. The comparison in the paper — *"outperforming WalkSAT (0.967)"* — is between methods run on different problems. The random-sampling baseline additionally reuses the last WalkSAT instance via the leaked loop variable `cl`, so it is evaluated on one arbitrary instance while the other two get six each.

The same defect appears at line 895 of the batch report, which records the two methods as tested with a paired t-test across "identical instances". They are not identical, and the test is not paired.

## 6. Finding — the chosen operating point is not the best one

`data/metrics.json`, `depth` section, regenerated 2026-09-30:

```
p    = [1, 2, 3, 4]
sat  = [0.98333, 0.96667, 0.96667, 0.96667]
gap  = [5.70747, 6.68037, 6.24094, 5.96937]
```

`p=1` is the best point on **both** metrics. `p=2` is the worst on the gap and tied-worst on satisfaction. And `p=2`, `p=3` and `p=4` return **bit-identical** satisfaction ratios, which is consistent with §3: with random search, additional layers do not change which states the oracle selects.

Against this:

- `paper/main.tex:22` — *"shallow-depth QAOA (**p=2**) achieves a mean satisfaction ratio of 0.986"*. The depth experiment gives 0.96667 at p=2 and 0.98333 at p=1.
- `paper/main.tex:251` — *"The marginal benefit of deeper circuits (p > 2)"*. There is no benefit to measure: satisfaction is constant from p=2 onward, and p=1 is strictly better than all of them.

The paper selected a strictly dominated operating point and characterised the reason as diminishing returns.

## 7. Finding — the artifact is not bit-reproducible

`data/metrics.json` regenerated and compared against the committed file: identical except `depth.gap`, which differs in the final one or two units in the last place.

```
5.707474586657542  ->  5.707474586657543
6.680373038766503  ->  6.680373038766502
6.240937119889088  ->  6.2409371198890895
5.96937077649221   ->  5.969370776492196
```

The effect is at the 1e-15 level and does not affect any claim. It is recorded because it is the opposite of the `isac-jasc-ieee` result, and the difference is informative: both packages draw an expectation value as `state.conj() @ (H * state)`, but only one is reproducible. The cause is not established and is not asserted.

## 8. Classification

Reproduces: **yes, to within floating-point non-determinism.** Framing honest: **yes.** Circuit structure correct: **yes.** Norm preservation on the unitary path: **exact.**

| mechanism named | what the code does | category |
|---|---|---|
| "exact state-vector simulation" | exactly that | accurate |
| `$H_B = \sum X_j$, $\ket{+}$ initial, p alternating layers | exactly that | accurate |
| "variational parameters" | uniform random search, best of 40 | category 3 — quantum-named, classical, and the mechanism is absent from the result |
| "measurement" | top-10 exact-amplitude oracle | category 4 — labelled as an operation that does not occur |
| "depolarizing channel" | norm-shrinking coherent admixture | category 4 |
| comparison against WalkSAT | different instances per method | not a quantum defect; a design defect |

**This is a seventh profile, and the most nuanced in the sweep.** Unlike QCE, the top-level framing is not overstated — the paper says "exact state-vector simulation" in its abstract. The failures are confined to three mechanism *names* inside an otherwise correctly implemented circuit, and the package's central result depends on all three.

Note the contrast with QCE: there, a correct classical method carried a wrong label. Here, a correct circuit structure carries wrong labels for the three operations that produce the result.

## 9. Auditor note — a reading error, recorded

While measuring the norm, the first pass summed the second element of `qaoa_run`'s return value, which is the cost Hamiltonian `H`, not the state. That produced a squared norm of 244 on the noise-free path and briefly looked like a second normalisation defect. It was an indexing error on the auditor's side. `qaoa_run` returns `(state, H)`; the unitary path is 1.000000 and the noise path does shrink. Recorded because a report on a code-reading defect should record its own.

## 10. Not verified

- The magnitude of the oracle's advantage over Born sampling. Both saturated at 1.0 on the instance tested; the effect was not measured on harder instances and is not claimed.
- Whether readout calibration and ZNE are implemented as described at line 190. The mitigation experiment was not traced to the metric path.
- Whether the four figures regenerate byte-identically. Not compared.
- The Chinese-language paper and the presentation decks were not read.
- Whether the float non-determinism in §7 is environment-specific. One machine, two runs.
