# Claim Adjudication — Quantum K-SAT Package

**Status:** adjudication complete. **No manuscript text has been edited.**
**Branch:** `fix/quantum-audit-sweep`. **Baseline:** `dc1e43c`.
**Evidence:** `FALSIFIER-LOG-Q1.md` … `FALSIFIER-LOG-Q6.md`.
**Claim IDs below are the IDs emitted by `tests/test_claim_correspondence.py`.**

---

## 0. Scope and what this document is not

This assigns a disposition to each claim examined in Q6 and states the manuscript
action each disposition requires. It does **not** judge whether QAOA on 3-SAT is a
good idea, whether the measurements are scientifically interesting, or whether the
package should be published. It answers one question: *does the sentence describe
the thing it is attributed to?*

Three boundaries are held throughout:

1. **Implementation fact / scientific interpretation / claim correspondence** are
   never merged. Q2 established that the optimiser is random search; that random
   search is a legitimate algorithm; and that what the manuscript calls it is a
   separate question answered by Q6.
2. **A contradicted claim is not a worthless claim.** A SAT ratio near 0.98 may be
   a correct measurement of a quantity that is not the one the sentence names.
3. **A green repair is not a true claim.** Nothing here upgrades a claim's status.

---

## 1. Disposition vocabulary

| Disposition | Meaning |
|---|---|
| **RETAIN** | Accurate as written. No action. |
| **REWRITE** | The underlying measurement may be sound; the sentence does not describe it. Fix the text. |
| **REMOVE** | Contradicted by a measured value or by the code, and no text edit makes the sentence true as written. |
| **NON-DISCRIMINATING** | Numerically supported but scientifically unable to separate the alternatives it is offered to separate. |
| **NEW EXPERIMENT REQUIRED** | Not contradicted; simply not decidable from this artifact. |

---

## 2. Adjudication

### C1 — Algorithm 1 swaps the mixing and cost Hamiltonians · **REWRITE**
`main.tex:101-102` applies $\beta$ to $H_B$ (mixing) and $\gamma$ to $H_C$ (cost).
`qaoa_run` applies `cost_op(state, beta[l], H)` then `mixer(state, gamma[l], n)`.
**The code is correct and the published pseudocode is backwards.**
Action: correct the pseudocode. Repair class **R3** — document only, no code change.

### C2 — three different noise operators · **REWRITE**
`eq (1)` (`:116`) gives a density-matrix channel $(1-\lambda)\rho + \lambda I/2^n$.
Algorithm 1 (`:104`) gives an amplitude blend with $\lambda/\sqrt{2^n}$. The code
(`:57`) blends with $\lambda/N$. Three different objects, three different
amplitudes, and only the first is the channel the prose describes.
Action: choose one operator, implement it, and make the equation, the pseudocode and
the code agree. Repair class **R1** if the density-matrix channel is adopted.
Highest-value repair in the package: it changes what the noise axis *means*, so every
number on it must be regenerated.

### C4 — measurement described as sampling · **REWRITE**
`main.tex:86` claims sampling from the output distribution. `best_sat_from_state`
reads exact $|\psi|^2$, takes the top 10 basis states, and evaluates all of them.
Zero shots are drawn (Q1).
Action: describe the exact top-10 readout. Repair class **R3**.

### C5 — WalkSAT restart probability 0.3 · **REMOVE or IMPLEMENT**
`main.tex:123` specifies a restart probability. `walk_sat` is a single 2000-flip run
returning on satisfaction; the string `restart` does not appear in the simulator.
Action: either implement the restart (**R1**) or drop the parameter (**R3**). As
written the sentence describes an algorithm the artifact does not contain.

### C6 — "on identical instances" · **REMOVE the sentence; repair the experiment**
`main.tex:150` claims WalkSAT was evaluated on identical instances. Q4 F1 measured
**zero** shared instances between the arms.
This is not a text fix. Every QAOA-versus-WalkSAT comparison in the package rests on
unpaired averages over disjoint instance sets. Repair class **R2**.

### C7 — three values for the same WalkSAT baseline · **REMOVE the inconsistent ones**
0.954 (`:200`), 0.964 (`:150`) and 0.967 (`:22`, `:235`, `:262`) are all given for the
same overall baseline, plus per-`n` values 0.972 and 0.959 (`:160`) that agree with
none of them. The artifact's mean over the 11 noise levels is **0.9556 ± 0.0214**.
No stated value matches the artifact to three decimals; these are not rounding
differences.
Action: reconcile to the artifact. Repair class **R3**.

### C8 — "gap decreases from 5.71 to 5.97" · **REMOVE the sentence; NEW EXPERIMENT**
The quoted endpoints are accurate. The direction word is not: the artifact's series
is 5.7075 / 6.6804 / 6.2409 / 5.9694, so p=4 is **higher** than p=1, and the series
rises before falling.
Independently, Q5 F2 established the reported gap is not a proper expectation value:
$|\psi|^2$ falls monotonically with depth (0.960179 → 0.850435), so the bias is
depth-coupled and no rescaling removes it.
Action: no depth claim is supportable from this artifact. **NEW EXPERIMENT REQUIRED.**

### C9 — "gap remains constant at 2–3%" · **REMOVE**
Artifact gaps per `n`: 0.0222, 0.0044, 0.0111, 0.0222. Only 2 of 4 lie in the stated
band, and at n=10 the gap is 0.0044.
Action: remove. The claim is contradicted by the figure it cites. Repair class **R3**.

### C10 — random baseline as evidence of instance hardness · **REMOVE**
A uniformly random assignment satisfies a random 3-clause with probability
7/8 = 0.8750, independently of $n$ and of the instance. The artifact's `rand_m`
spread across `n` is 0.0057. A mathematically invariant quantity cannot be evidence
of increasing hardness.
Action: remove the inference. The baseline is legitimate as a reference point; the
reading of it is not. Repair class **R3**.

### C11 — mitigation ordering and "measurement errors dominate" · **REMOVE**
The package maps readout → noise 0.075 and zne → 0.045. Less noise must score
higher. The artifact's ranking by score is `readout, both, zne, none`; the ranking
by applied noise is `both, zne, readout, none`. The ordering is **not monotone in
noise**.
The sentence at `:190` also contradicts the descriptions at `:185-186`: ZNE is
described as amplifying noise 2× and extrapolating to the zero-noise limit, and
readout as a confusion matrix estimated from calibration circuits. Neither exists.
`factors[strat]` is the only strategy-dependent quantity in the function.
Action: remove all four strategy descriptions and the ordering claim. Repair classes
**R1** (mechanisms unimplemented) and **R2** (the ordering is not identifiable).

### C12 — paired t-test · **REMOVE**
`main.tex:200` reports a **paired** $t$-test. Q4 F1 measured zero shared instances,
so the data cannot be paired.
Action: remove, or recompute from an experiment that records per-trial data and pairs
the arms. Repair class **R2**.

### C13 — p < 0.001 and Cohen's d = 1.14 · **UNSUPPORTED, not thereby false**
`metrics.json` contains only per-level means and standard deviations — **no per-trial
values exist**. The statistic cannot be recomputed even in principle.
Action: this is marked UNSUPPORTED rather than CONTRADICTED. The evidence does not
show the test was computed wrongly; it shows the test cannot be checked. If the
authors hold the per-trial data outside the artifact, **NEW EXPERIMENT REQUIRED** to
admit it; otherwise remove.

### C14 — hardware resource plan · **REMOVE the dependent figures**
`main.tex:209-210` budgets `N_shots ≈ 2048` per iteration and ≈60,000 total shots,
assuming a measurement process that does not occur (Q1). Every downstream planning
figure — including the comparison to a 127-qubit processor (`:212`) — inherits that.
Action: remove, or re-derive under a genuine shot budget. Repair class **R3**.

### C15 — "repeated 5–6 times" · **REMOVE or REPAIR**
`exp_depth` draws one instance and one run per depth, and reports no dispersion for
the `sat` or `gap` columns (Q4 F3).
Action: `exp_depth` needs replication. Repair class **R2**.

### C16 / C17 — ordering and spectral explanations · **REMOVE**
The plateau is explained at `:150` and `:248` by the channel preserving the relative
ranking of assignments and the spectral ordering of the cost Hamiltonian's
eigenstates. Q3 established the operation is an affine amplitude blend toward a
vector of norm $1/\sqrt{2^n}$ — not a channel on the density matrix — so it has no
established action on eigenstates or on orderings.
Action: remove both explanations. The plateau needs an explanation that is true; §3
proposes the likely one. Repair class **R3**.

### C18 — random initialisation disclosure · **RETAIN**
`main.tex:257` discloses that the classical optimisation uses random initialisation
rather than gradient or Bayesian methods. Q2 established this behaviourally and
independently: candidate generation is independent of the objective and the objective
only ranks.
**This limitation is accurate as written.** It is recorded prominently so it is not
averaged away by the fifteen contradictions around it — the same pattern observed in
CRL, and the opposite of LEO and ISAC, where nothing in the manuscript constrained
itself.

---

## 3. The plateau is NON-DISCRIMINATING, and probably not what the sentence means

The headline claim — QAOA maintains a SAT ratio above 0.97 across the full noise
range with no statistically significant degradation, therefore shallow QAOA is robust
to depolarizing noise — survives its numbers and fails as evidence.

Three independent measurement facts converge:

1. **The readout is exact and top-10.** Q1: zero shots, top-10 of $2^n$ basis states,
   all ten evaluated. At m/n = 5.0 the instance is unsatisfiable but densely
   populated with assignments violating only one or two clauses, so the best of ten
   candidates sits near 1.0 largely regardless of the circuit.
2. **The readout renormalises.** `best_sat_from_state` divides by the probability
   sum, which absorbs Q3's normalisation defect completely. The SAT ratio column
   therefore cannot exhibit the noise's effect on total probability.
3. **The reported dispersion is 6 trials over distinct instances**, unpaired (C6).

The plateau is therefore **NON-DISCRIMINATING**: the measurement as designed cannot
separate "QAOA is robust to noise" from "the top-10 readout saturates". Those are very
different claims and the artifact does not choose between them.
A discriminating experiment would hold the instance fixed, use a genuine shot budget,
and report the probability mass on satisfying assignments rather than a best-of-ten
maximum.

Note the honest counterweight: C2's repair will change this column, because a real
depolarizing channel distributes probability where the current map concentrates it.

---

## 4. Repair classes

| Class | Meaning | Items |
|---|---|---|
| **R1** | Mechanism not implemented | C2 *(if the density channel is adopted)*, C5 *(if restart is implemented)*, C11 *(ZNE extrapolation, readout calibration)* |
| **R2** | Sound code, unidentifiable experiment | C6, C11, C12, C15 |
| **R3** | Valid numbers, invalid document — **no code change** | C1, C4, C7, C9, C10, C14, C16, C17 |

**Eight of seventeen claims are R3.** The measurements largely stand; the sentences do
not describe them. That is a different problem from LEO's and ISAC's, where the
measurements themselves did not support the comparison being made.

**No repair is authorised yet.** Every R1 and R2 repair changes a number, and no
historical published number is ever a repair target. A repair is validated by
restoring a pre-specified property, not by producing different numbers.

---

## 5. Order of work if repairs are authorised

1. **C2 first.** It changes what the noise axis means, so every number on it must be
   regenerated afterwards. Doing anything else first wastes the work.
2. **C6 pairing.** All QAOA-versus-WalkSAT comparisons are unidentifiable without it.
3. **C15 replication.** The depth experiment cannot support a dispersion claim with
   one run per point.
4. **C11 mechanisms.** Only after the parameters being mitigated are real.
5. **R3 document corrections last**, against regenerated artifacts.

---

## 6. Cross-falsifier dependencies recorded

- **Q1 → C4, C14.** Zero shots makes the sampling claim false and the shot budget
  unfounded.
- **Q2 → C18.** The random-initialisation disclosure is *confirmed* by Q2, not merely
  unrefuted.
- **Q3 → C2, C16, C17.** The noise-operator finding propagates into the equation, the
  pseudocode and both ordering explanations.
- **Q4 → C6, C12, C15.** Unpaired arms invalidate the pairing claim and the paired
  test, and force the depth replication.
- **Q5 → C8.** The gap is not a proper expectation value and its bias is
  depth-coupled, so no depth claim is supportable.

---

## 7. Summary

| Outcome | Count |
|---|---|
| Claims examined | 17 |
| CONTRADICTED | 15 |
| UNSUPPORTED — not thereby false | 1 |
| SUPPORTED as written | 1 |

| Disposition | Count |
|---|---|
| REWRITE | 3 |
| REMOVE | 12 |
| RETAIN | 1 |
| NEW EXPERIMENT REQUIRED | 1 |

Additionally **NON-DISCRIMINATING** rather than wrong: the noise-plateau reading and
the "measurement errors dominate" reading. Both are recorded as unable to
discriminate rather than as failures, because the underlying measurements may be
sound and the instruments too blunt to resolve them.

Six falsifiers were built for this package. **Thirteen falsifier defects** were found
in them and all thirteen are retained in the logs. Three deserve emphasis:

- Q2's positive control evaluated the unperturbed vector twice, so every gradient was
  zero. The whole falsifier was **rejected and rebuilt** until the control passed.
- Q3's positive control used `sqrt(1-lam)*psi + sqrt(lam)*|+..+>`, which reported
  $\|\cdot\|^2 = 1.25$. The arithmetic was correct and the formula was wrong — that
  expression does not describe a channel.
- `np.diag(H)` on the 1-D diagonal returned by `make_H` **fabricates** an identity
  matrix and reported a ground energy of 0 where the true value is 1, reversing a
  conclusion about instance satisfiability.

One false green in the claim checker itself: C4's marker pattern never matched, so the
sampling claim was silently omitted from the first report. It is now asserted present,
and the claim count moved from 16 to 17. A test that cannot fail because it never ran
is the same defect class this programme exists to detect.