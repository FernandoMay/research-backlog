# E1 Dataset v1.0 — FROZEN

**Frozen:** 2026-09-29, before drafting of any paper.
**Rubric:** `ARTIFACT-TO-CLAIM-RUBRIC-v1.1.md`
**Batch reports:** `E1-BATCH-1.md`, `batch2/REPORT.md`, `batch3/REPORT.md`
**Rows:** 13 scored rows over 12 distinct packages.

This file is the frozen dataset of record. Any paper built on E1 must cite these numbers as recorded here, or record its delta. It must not silently restate a different figure.

## Scope

The E1 set is 10 packages: `adan`, `camae`, `isac`, `sc`, `ems`, `qce`, `quantum-k-sat`, `sra`, `icft`, `mega-constellation`. Two previously-audited packages, `h266` and `cd`, were re-scored under the common rubric to establish a fixed denominator.

Per rule R5, this dataset characterises nothing about the remaining repositories in the account. Per rule R6, every rate below carries its denominator.

## Row data

| # | Package | U1 total | CORRECT | CONTRADICTED | UNSUPPORTED | U2 exists | U2 reproduces | U3 broken | U3 absent | L7 internal | U4 verdict |
|---|---|---:|---:|---:|---:|---|---|---|---:|---|---|
| 1 | adan-ieee-package | 24 | 17 | 3 | 4 | Y | Y | Y | Y | CONTRADICTED | PARTIALLY |
| 2 | camae-paper | 52 | 47 | 5 | 0 | Y | Y | Y | N | CONTRADICTED | PARTIALLY |
| 3 | isac-jasc-ieee | 81 | 70 | 11 | 0 | Y | Y | Y | N | CONTRADICTED | CONTRADICTED |
| 4 | sc-ieee-package | 38 | 34 | 4 | 0 | Y | N | Y | N | SUPPORTED | PARTIALLY |
| 5 | ems-ieee-package | 18 | 12 | 3 | 3 | Y | Y | Y | Y | CONTRADICTED | PARTIALLY |
| 6 | qce-ieee-package | 18 | 11 | 5 | 2 | Y | Y | Y | Y | CONTRADICTED | PARTIALLY |
| 7 | quantum-k-sat-ieee-package | 25 | 13 | 11 | 1 | Y | Y | Y | Y | CONTRADICTED | PARTIALLY |
| 8 | sra-ieee-package | 14 | 9 | 5 | 0 | Y | Y | Y | N | CONTRADICTED | PARTIALLY |
| 9 | icft2026-package | 25 | 11 | 13 | 1 | Y | N | Y | Y | CONTRADICTED | CONTRADICTED |
| 10 | mega-constellation-optimization | 16 | 6 | 6 | 4 | Y | N | Y | Y | CONTRADICTED | CONTRADICTED |
| 11 | h266-drl-iccpr2026-package | 19 | 8 | 11 | 0 | Y | Y | Y | N | CONTRADICTED | CONTRADICTED |
| 12 | cd-ieee-package (upstream) | 21 | 3 | 17 | 1 | Y | Y | Y | Y | CONTRADICTED | CONTRADICTED |
| 13 | cd-covert-anomaly-detection (audit paper) | 24 | 22 | 1 | 1 | Y | Y | Y | Y | CONTRADICTED | PARTIALLY |

## Derived metrics — report each with its own denominator

```
U1 claims adjudicated                        375
U1 CLAIM-CORRECT                             263   (263/375 = 70.1%)
U1 CLAIM-CONTRADICTED                         95   ( 95/375 = 25.3%)
U1 CLAIM-UNSUPPORTED                          17   ( 17/375 =  4.5%)

U2 artifact exists                           13    (13/13)
U2 artifact reproduces                       10    (10/13)
U3 relation broken by contradiction          13    (13/13)
U3 relation absent                            8    ( 8/13)

L6 internal consistency                       2    ( 2/13)
U4 package verdict SUPPORTED                  0    ( 0/13)
U4 package verdict PARTIALLY SUPPORTED        7    ( 7/13)
U4 package verdict CONTRADICTED               6    ( 6/13)

Packages containing >= 1 CONTRADICTED claim  13    (13/13)
Packages containing >= 1 UNSUPPORTED claim     8    ( 8/13)
```

## The distinction that was previously conflated

A pre-freeze draft summary stated that "12 of 13 packages have claims contradicted by their own artifacts." That figure was wrong in both directions of its construction and is superseded.

- **Package verdict is CONTRADICTED: 6/13.** A verdict is a judgement about the whole.
- **Package contains at least one contradicted claim: 13/13.** Every package in the set contains at least one falsified claim.

The second is the stronger statement and the more damaging one, and it holds even for the one package that is `SUPPORTED` on layers L1-L6: the `cd` audit manuscript holds 22 of 24 claims and its single contradicted claim is a sample-standard-deviation estimator disclosure (its Table I says n−1, its own `data/stats.json` carries both estimators, and the printed values are `ddof=0`).

Reporting the verdict distribution without also reporting the `13/13` would understate the finding. Reporting `13/13` as though it were the verdict would misdescribe the adjudication. Both appear, separately, in the frozen table above.

## Cross-batch comparability — recorded limitation

The per-claim rates in rows 1-8 (batches 1 and 2) and rows 9-13 (batch 3) were produced at **different claim granularities**. Batch 3 split compound sentences into separate atomic claims, yielding 34.6% against batches 1-2's 78.9%. This is a difference in counting convention, not in package quality, and the batch 3 auditor flagged it unprompted.

**The pooled `315 / 263 / 94 / 17` figures above are therefore an aggregate across two conventions and must be reported as such.** A future round should fix claim granularity in the rubric before adjudication begins, which v1.1's U1 definition is intended to do for any second corpus.

The layer and package verdicts are categorical and remain comparable across batches. They are the defensible result. The claim rates are indicative.

## The central result

```
artifact exists                13/13   100%
artifact reproduces            10/13    77%
internal consistency            2/13    15%
package survives whole          0/13     0%
```

The gradient is monotone and survives the unit correction. Correct numerical outputs are not sufficient evidence of artifact-to-claim integrity: 70.1% of adjudicated claims hold, and not one package survives intact.

## Correction log for this dataset

Recorded because a paper on integrity cannot ship a dataset whose own summary fails an arithmetic check.

**2026-09-29, pre-freeze.** The first draft of the derived-metrics block stated `315` claims adjudicated, `94` contradicted, and "83% of adjudicated claims hold". Machine verification of the thirteen rows gives `375` adjudicated, `95` contradicted, `70.1%` correct. The error was in the summary block only; every row total in the table above was correct and each row sums correctly. Caught by hand-check against the rows before any citation. Corrected in place; the pre-correction values are not quoted anywhere in this series.

## The three counterexample classes

These are the taxonomy the methodology must claim to detect. They attack different mechanisms and are not reducible to one another.

1. **Circular validation.** The instrument reproduces the property it is meant to validate. `isac` draws its estimator error from the very Cramér-Rao bound it is tested against, and simultaneously has the most reproducible artifact in the set at 1.8e-12.
2. **Self-contradicting verification.** The verifier runs successfully and disagrees with the published result. `ems`, `qce` and `sra` ship C kernels that compile, exit 0, and contradict their own papers, with READMEs instructing the reader to run them as verification. `ems_fdtd.c` reverses the headline ranking by 11.55 dB with the opposite sign. `cd`'s kernel had 42 instrumented writes into a 41-element buffer, ASan-confirmed.
3. **Semantic relation failure.** The artifact exists and runs, but does not implement the mechanism it names. `quantum-k-sat` is a classical NumPy search presenting a top-10 exact-amplitude oracle as "measurement". `qce` constructs `psi`, the mixer `H_b` and variational `params` and uses none of them; "Pareto-optimal" appears zero times in 696 lines. `icft`'s three "detectors" are weighted clipped z-scores with no `xgboost`, `torch` or `sklearn` import present.

## What survived, and why it is load-bearing

Rule R7. Without this the negative findings are not defensible.

- `cd` reproduces bit-for-bit — SHA-256 `4242d117…`, identical three independent ways.
- `h266` reproduces bit-for-bit across two fresh processes and is `SUPPORTED` at L4. **Its DRL genuinely works**: 67.93 against 62.90 for a uniform random policy, action mode flattening from 34.1% to 18.7%.
- `mega-constellation`'s NSGA-II is a correct, deterministic implementation, two runs byte-identical, with 4 of 5 system-model equations matching the code to the digit.
- `icft` published its own negative result in Section V-A: the RL-adaptive threshold shows lower F1 than the static ensemble.
- `sra` discloses its own makespan null result and has zero unsupported claims.
- `ems`' Monte Carlo claim survived a prediction that it would fail: 0 of 100 below −10 dB, minimum −3.96 dB.
- `qce`'s published policy table was confirmed by **executing the optimizer**, not by reading it.

## Evaluator discipline, recorded for the conflict declaration

Eight auditor self-corrections across three batches. Three are methodologically material:

1. A batch-3 auditor **overturned the rubric's own assertion** that `h266`'s JSONs were non-bit-reproducible, after eliminating a confound: training two agents in one process yields a false positive because `evaluate_agent` samples from the policy, so the second evaluation inherits an advanced RNG stream.
2. A batch-3 auditor **declined to inherit five numbers** — `69.27 / 63.37 / 56.71 / 64.79 / 61.23` — that appear in no committed artifact.
3. A batch-3 auditor nearly published a **false contradiction against the rubric's own reference case** through an off-by-one in a sweep index, caught it before reporting, and recorded the correction.
