# Quantum — claim inventory and lineage reconstruction

**Date:** 2026-09-30
**Baseline:** `dc1e43c` ("Initial commit: QAOA for K-SAT on NISQ devices"), tree clean at clone.
**Branch:** `fix/quantum-audit-sweep`, created **before the first commit**.
**Status:** no code modified, no artifact regenerated, no manuscript edited. Reconstruction only.
**Code:** `simulator/quantum_k_sat_simulator.py` (one module, 18 functions).

---

## 0. Destination gate

```
branch at clone   master
branch created    fix/quantum-audit-sweep   ← before any commit
```

---

## 1. Q1 — the "measurement" is an exact oracle, not a Born sample

```python
def best_sat_from_state(state, H, n, clauses):
    probs = np.abs(state)**2
    probs /= probs.sum()
    top = np.argsort(probs)[-10:]
    best = 0
    for idx in top:
        bits = [int(x) for x in format(idx, f'0{n}b')]
        best = max(best, sat_ratio(bits, clauses))
    return best
```

It reads the exact probability of every one of the 16 basis states, renormalises,
takes the ten most probable, and evaluates each exactly.

```
exact distinct probabilities available: 16 of 16
10 repeats of the scorer -> 1 distinct value: [1.0 × 10]
```

**A Born measurement with S shots varies with S. This cannot, by construction.**
There is no shot count, no sampling, no stochasticity anywhere in the path.

This is not automatically wrong. Reading exact amplitudes is a perfectly
legitimate *simulation oracle*. It becomes a defect only when the readout is
presented as evidence about measurement behaviour — which is what Q6 must
adjudicate.

---

## 2. Q2 — the "variational optimizer" is a random search with elitism

```python
def optimize_qaoa(clauses, n, p, noise=0.0, iters=40):
    best_e = 1e9
    best_p = None
    for _ in range(iters):
        g = np.random.uniform(0, np.pi, p)
        b = np.random.uniform(0, np.pi, p)
        state, _ = qaoa_run(clauses, n, p, g, b, noise)
        e = np.real(np.conj(state) @ (H * state))
        if e < best_e:
            best_e = e
            best_p = (g.copy(), b.copy())
    return best_p, best_e
```

Forty candidates drawn uniformly at random, each evaluated once, the best kept.
**There is no update rule.** No gradient, no parameter-shift, no SPSA, no
COBYLA, no population, no reuse of the incumbent as a starting point. The
objective is used only to select, never to steer.

This is a legitimate algorithm. It is not a variational optimizer, and if any
claim depends on variational optimisation having occurred, that claim has no
support from this code.

---

## 3. Q3 — the declared depolarizing channel does not preserve the trace

```python
if noise > 0:
    state = (1-noise)*state + noise*np.ones(N,complex)/N
```

The maximally mixed state `I/2^n` is the ket `ones(N)/sqrt(N)`, whose squared
norm is 1. **The code uses `ones(N)/N`, whose squared norm is `1/N = 0.0625`
at n = 4** — an unnormalised vector. So the mixture does not interpolate toward
the maximally mixed state; it shrinks toward zero.

| noise | trace after mixing | preserved |
|---|---|---|
| 0.00 | 1.00000000 | yes |
| 0.05 | 0.92640625 | **no** |
| 0.10 | 0.85562500 | **no** |
| 0.20 | 0.72250000 | **no** |
| 0.30 | 0.60062500 | **no** |
| 0.50 | 0.39062500 | **no** |

The correct mixture `(1-p)ρ + p·I/2^n` has trace 1 at every p. This one loses
`(1-noise)² + noise²/N` of trace, so **every amplitude, and therefore every
probability the Q1 oracle reads, is computed from a non-normalised state at any
non-zero noise setting.**

Two defects compound here: the channel is not trace-preserving, and the scorer
normalises the resulting distribution rather than rejecting it.

---

## 4. Q4/Q5/Q6 — not yet adjudicated

Recorded as open rather than resolved:

- **Q4** whether QAOA and WalkSAT share an instance and an evaluation budget
- **Q5** whether the reported p-depth ordering survives
- **Q6** whether "measurement", "optimizer", "depolarizing" and "QAOA" describe
  what the code performs

Per the standing rule, the labels above are **not** adjudication dispositions.
Falsifiers come next; the terminology is not a verdict.

---

## 5. A fact preserved from the earlier audit, stated so it is not repeated

`qaoa_run` returns `(state, H)`. An earlier audit briefly read the cost
Hamiltonian as the state and reported a second normalisation defect. That was an
auditor error, not a package defect, and the tuple is read correctly here.

---

## 6. Frozen

Inventory and lineage only. No repair is designed and no falsifier has been
written. The order is: Q1 falsifier, then Q2, then Q3, then experimental
controls, then the claim matrix, then the gate.

No scientific claim is adjudicated by this document.