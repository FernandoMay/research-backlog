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

L7 internal consistency                       1    ( 1/13)
U4 package verdict SUPPORTED                  0    ( 0/13)
U4 package verdict PARTIALLY SUPPORTED        8    ( 8/13)
U4 package verdict CONTRADICTED               5    ( 5/13)

Packages containing >= 1 CONTRADICTED claim  13    (13/13)
Packages containing >= 1 UNSUPPORTED claim     8    ( 8/13)
```

## The distinction that was previously conflated

A pre-freeze draft summary stated that "12 of 13 packages have claims contradicted by their own artifacts." That figure was wrong in both directions of its construction and is superseded.

- **Package verdict is CONTRADICTED: 5/13.** A verdict is a judgement about the whole.
- **Package contains at least one contradicted claim: 13/13.** Every package in the set contains at least one falsified claim.

The second is the stronger statement and the more damaging one, and it holds even for the one package that is `SUPPORTED` on layers L1-L6: the `cd` audit manuscript holds 22 of 24 claims and its single contradicted claim is a sample-standard-deviation estimator disclosure (its Table I says n−1, its own `data/stats.json` carries both estimators, and the printed values are `ddof=0`).

Reporting the verdict distribution without also reporting the `13/13` would understate the finding. Reporting `13/13` as though it were the verdict would misdescribe the adjudication. Both appear, separately, in the frozen table above.

## Cross-batch comparability — recorded limitation

The per-claim rates in rows 1-8 (batches 1 and 2) and rows 9-13 (batch 3) were produced at **different claim granularities**. Batch 3 split compound sentences into separate atomic claims, yielding 34.6% against batches 1-2's 78.9%. This is a difference in counting convention, not in package quality, and the batch 3 auditor flagged it unprompted.

**The pooled `375 / 263 / 95 / 17` figures above are therefore an aggregate across two conventions and must be reported as such.** A future round should fix claim granularity in the rubric before adjudication begins, which v1.1's U1 definition is intended to do for any second corpus.

The layer and package verdicts are categorical and remain comparable across batches. They are the defensible result. The claim rates are indicative.

## The central result

```
artifact exists                13/13   100%
artifact reproduces            10/13    77%
internal consistency            1/13     8%
package survives whole          0/13     0%
```

The gradient is monotone and survives the unit correction. Correct numerical outputs are not sufficient evidence of artifact-to-claim integrity: 70.1% of adjudicated claims hold, and not one package survives intact.

## Correction log for this dataset

Recorded because a paper on integrity cannot ship a dataset whose own summary fails an arithmetic check.

**2026-09-29, pre-freeze.** The first draft of the derived-metrics block stated `315` claims adjudicated, `94` contradicted, and "83% of adjudicated claims hold". Machine verification of the thirteen rows gives `375` adjudicated, `95` contradicted, `70.1%` correct. The error was in the summary block only; every row total in the table above was correct and each row sums correctly. Caught by hand-check against the rows before any citation. Corrected in place; the pre-correction values are not quoted anywhere in this series.

**2026-09-30, post-freeze.** Two further figures in the same derived-metrics block were wrong, and both were caught by the same procedure: a row-level reconciliation that sums the thirteen per-package rows and compares the sum against the summary block. Neither touched a row. The row table, every per-package row total and every per-claim figure were correct before this correction and are correct after it; the failures were entirely in the aggregation layer, which is the layer this dataset exists to audit in the artifacts.

1. **Verdict distribution.** The block recorded `0` SUPPORTED, `7` PARTIALLY SUPPORTED, `6` CONTRADICTED. The roll-up is `0 / 8 / 5`. The error is an arithmetic slip in the hand-written roll-up: batch 1 gives three `PARTIALLY` and one `CONTRADICTED`, batch 2 gives four `PARTIALLY`, batch 3 gives one `PARTIALLY` and four `CONTRADICTED`, which is eight and five, not seven and six. All three batch reports agree with the rows on this point. Corrected to `0 / 8 / 5`.
2. **Internal consistency (L7).** The block recorded `2` of `13`. The roll-up of the recorded internal-consistency column is `1` of `13`: only `sc-ieee-package` (row 4) carries `SUPPORTED` in it. This is a miscount, not a summation error, and the draft's own working is visible in the paper that reported it: `cd`'s audit manuscript (row 13) was counted on the basis of its layer stack placing L1-L6 at `SUPPORTED`, but its recorded verdict in this column is `CONTRADICTED`, and that is the column in question. The contradiction is a sample-standard-deviation disclosure: Table I states n−1, the package's own `data/stats.json` carries both estimators, and the printed values are `ddof=0`. Corrected to `1` of `13`.

Neither correction changes the central result; both make it steeper, because a lower internal-consistency rate is a stronger claim about the corpus than a higher one. The gradient now reads `13/13` exists, `10/13` reproduces, `1/13` internally consistent, `0/13` surviving whole. The central claim, the three failure classes and all mechanism evidence in the batch reports are unaffected, and no batch report is amended: the reports were right and the summary was wrong.

**2026-09-30, post-publication.** A third defect was found in the aggregation layer after the two above, and it is of a different kind from both: **the counts were never wrong.** It is a layer-*label* shift, and it is recorded here because a count that reconciles perfectly can still be attached to the wrong layer.

1. **`E1-AGGREGATE.md`, headline table.** The table labelled its rows `L3 — Figure`, `L4 — Method`, `L5 — Selection`, `L6 — Internal consistency`, `L7 — Verdict: SUPPORTED`. `ARTIFACT-TO-CLAIM-RUBRIC.md` v1.0 fixes those names as `L4 — Figure`, `L5 — Method`, `L6 — Selection`, `L7 — Internal consistency`, `L8 — Verdict`, and all three batch reports score their rows under exactly that mapping, using the table header `L1 | L2 | L3 total | L3 supported | L3 contradicted | L3 unsupported | L4 | L5 | L6 | L7 | L8`. Every label from L3 upward in the aggregate was therefore off by one, and every count was correct: 13/13, 10/13, 6/13 figure, 3/13 method, 7/13 selection, 1/13 internal consistency, 0/13 verdict. Re-rolling the thirteen rows against the batch reports' layer columns reproduces all seven counts exactly, so the numbers were sound and only the labels moved. The same file's own prose contradicted its own table: it states elsewhere that `h266` is `SUPPORTED` at L4 on four figures with committed generators, which is L4 = Figure under the rubric and not what the table's L4 row said. Corrected in place; no count was altered.
2. **This file, derived-metrics block.** The block labelled the internal-consistency line `L6 internal consistency` and the second correction above was headed `Internal consistency (L6)`. Internal consistency is L7. The row table in this file already used `L7 internal`, so the block and the table disagreed about the name of the same column while agreeing about its value. Corrected in place.
3. **This file, cross-batch comparability section.** That section described the pooled figures as `315 / 263 / 94 / 17`. The pooled figures above it are `375 / 263 / 95 / 17`; `315` and `94` are the pre-correction values that the first entry above states are not quoted in this series. The section was describing a pool that no longer exists in the file. Corrected in place.

The third and fourth of these could not have been caught by the row-level reconciliation that caught the first two, because reconciliation compares sums against sums and these are naming errors. They were caught by a different check: parse the aggregate's layer labels and assert that the sequence matches the rubric's names in order. That check is now part of the manuscript's verification script, and it is the assertion that fails if the shift is reintroduced.

Because `E1-AGGREGATE.md` was already public when this was found, the correction is post-publication and cannot be made silently: the file is corrected, and this entry is the record. Nothing in the central result moves. The gradient still reads `13/13`, `10/13`, `1/13`, `0/13`, and the three failure classes and all mechanism evidence are unaffected. No batch report and no rubric file is amended: the reports were right and the summary was wrong, which is now the third recorded instance of the same fact.

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
