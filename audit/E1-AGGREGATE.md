# E1 Aggregate Results

**Rubric:** `ARTIFACT-TO-CLAIM-RUBRIC.md` v1.0
**Date:** 2026-09-29
**Batches:** 1, 2, 3 — all complete
**Rows:** 13 (12 distinct packages; `cd` scored twice, once per paper layer)

## Scope statement

This covers **only the 12 packages audited below**. Per rubric rules R5 and R6, it characterises nothing about the remaining repositories in the account. Every rate below carries its denominator.

The E1 set was 10 packages: `adan`, `camae`, `isac`, `sc`, `ems`, `qce`, `quantum-k-sat`, `sra`, `icft`, `mega-constellation`. Two previously-audited packages, `h266` and `cd`, were re-scored under this rubric to fix the denominator.

## The headline table

| Layer | SUPPORTED | CONTRADICTED | Rate |
|---|---:|---:|---|
| L1 — Artifact exists | 13 | 0 | **13/13** |
| L2 — Reproduction | 10 | 3 | **10/13** |
| L3 — Figure | 6 | 7 | 6/13 |
| L4 — Method | 3 | 10 | **3/13** |
| L5 — Selection | 7 | 6 | 7/13 |
| L6 — Internal consistency | 2 | 11 | **2/13** |
| L7 — Verdict: SUPPORTED | **0** | — | **0/13** |

Verdict distribution: **0 SUPPORTED · 7 PARTIALLY SUPPORTED · 6 CONTRADICTED.**

## The gradient

The hypothesis under test was: *artifact reproducibility is materially better than artifact-to-claim correspondence.*

With N=13 and a fixed rubric, it holds, and the gradient is monotone:

```
artifacts exist              13/13  100%
artifacts reproduce          10/13   77%
internal consistency          2/13   15%
package survives whole        0/13    0%
```

**The fracture is not arithmetic.** Individual numbers are mostly right — batch 1 and 2 put L3 at 213/270 claims supported, 78.9%. What fails is the layer above: selection, framing, and whether the abstract, the body, the table and the figure describe the same run.

## What the L3 claim rate is NOT

**The per-claim L3 rate is not aggregatable across batches, and must not be quoted as a single figure.**

Batch 3's auditor used a different claim granularity than batches 1 and 2, yielding 34.6% against their 78.9% — a difference in how finely a "claim" was counted, not a difference in the packages. The auditor flagged this unprompted. The **layer verdicts are comparable; the claim rates are not.**

## The three findings that carry the most weight

### 1. Validation that is circular by construction

`isac` drew its estimator error from the very Cramér–Rao bound it was being tested against. Its artifact is also the most reproducible in the entire set, agreeing to 1.8e-12. Good simulation hygiene buys nothing when the defect is in what the simulation measures.

### 2. Code that verifies nothing, and says it does

`ems`, `qce` and `sra` all ship C kernels that **compile, run, exit 0, and contradict their own papers** — with READMEs instructing the reader to run them as verification. `ems_fdtd.c` reverses the headline ranking, disagreeing by 11.55 dB with the opposite sign. `sc`'s kernel does not compile. In `cd`, ASan confirmed 42 instrumented writes into a 41-element buffer, aborting every run.

A verifier that runs and disagrees is worse than no verifier, because it transfers false confidence.

### 3. Naming that outruns the mechanism

- `quantum-k-sat` — a classical NumPy simulation. Random search presented as variational optimisation. A non-norm-preserving "depolarising" admixture of |11…1> with ‖ψ‖² = 0.39. A **top-10 exact-amplitude oracle** presented as "measurement". A paired t-test run across two separate instance generators.
- `qce` — 32-state exhaustive classical enumeration. `psi`, the mixer `H_b` and the variational `params` are each constructed and **never used**. "Pareto-optimal" appears zero times in 696 lines.
- `mega-constellation` — the constellation is not a Walker-Delta. Twenty satellites per plane span 21.375° of arc at 1.125° spacing. SBX never clips bounds: 110 of 20000 offspring fall outside the declared range.
- `icft` — three "detectors" are weighted clipped z-scores, with no `xgboost`, `torch` or `sklearn` import anywhere. The HMM "identifies 3 of 4 events" while assigning one state to 4986 of 5000 steps at precision equal to the base rate.

## What survived, and why it matters that it did

R7 requires this. Without it the negative findings are not defensible.

- `cd` **reproduces bit-for-bit** — SHA-256 `4242d117…`, identical three independent ways.
- `h266` **reproduces bit-for-bit** across two fresh processes, and is SUPPORTED at L4: four published figures with committed generators, all faithful to the data. **Its DRL genuinely works** — it beats a uniform random policy 67.93 vs 62.90, and the action distribution flattens from a 34.1% mode to 18.7%.
- `mega-constellation`'s NSGA-II is a **correct implementation**, deterministic across runs, and 4 of 5 system-model equations match the code to the digit.
- `icft` **published its own negative result** in Section V-A: "The RL-adaptive threshold shows lower F1 than the static ensemble."
- `sra` **discloses its own null result** on makespan. Zero unsupported claims.
- `ems`' Monte Carlo claim survived a prediction that it would fail: 0 of 100 below −10 dB, minimum −3.96 dB.
- `qce`'s published policy table was confirmed **by executing the optimizer**, not by reading it.

## Auditor discipline

Eight self-corrections were recorded across three batches. Three matter methodologically:

1. Batch 3's auditor **overturned the rubric's own assertion** that `h266`'s JSONs are non-bit-reproducible. It could not reproduce that, and eliminated a confound first: its initial test trained two agents in one process and got a false positive, because `evaluate_agent` samples from the policy, so the second evaluation inherited an advanced RNG stream.
2. Batch 3's auditor **declined to inherit five numbers** — "69.27 / 63.37 / 56.71 / 64.79 / 61.23" appear in no committed artifact.
3. Batch 3's auditor nearly published a **false contradiction against the rubric's own reference case** through an off-by-one in a sweep index, caught it, and recorded it.

The rubric is also due a correction: it treats `cd` as one package scored PARTIALLY SUPPORTED. The upstream package is CONTRADICTED — both of its stated conclusions are contradicted by its own artifacts. The PARTIALLY SUPPORTED verdict belongs to the audit manuscript written about it. Those are two different objects and the rubric should score them separately, as batch 3 did.

## Recommended next step

The E1 set is complete and the separation is confirmed on 13 rows with a fixed rubric. Continuing to audit further packages of the same kind has diminishing returns and no clear endpoint. The aggregate is now a dataset in its own right, and the next artifact is a methodology paper on **artifact-to-claim integrity in computational research**, using this as its primary dataset.
