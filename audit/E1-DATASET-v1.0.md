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

Naming in this block is mixed by construction, and the mixing is recorded here rather than
silently normalised. `U1`-`U4` are the units of rubric **v1.1**. The line
`L7 internal consistency` is named by its rubric **v1.0 layer** because the row table's column
is `L7 internal` and all three batch reports score that layer under the v1.0 name; v1.1 places
the same measurement under U4. The gradient block below uses the v1.1 unit names, so a reader
comparing the two blocks must not assume one naming system.

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

The per-claim rates in rows 1-8 (batches 1 and 2) and rows 9-13 (batch 3) were produced at **different claim granularities**. Batch 3 split compound sentences into separate atomic claims, yielding 50/105 (47.6%) over its five scored rows against batches 1-2's 213/270 (78.9%) over rows 1-8. This is a difference in counting convention, not in package quality, and the batch 3 auditor flagged it unprompted.

Claim-pool split, machine-readable and re-derivable from the row table above:

```
batches 1-2   rows 1-8    213/270   78.9%
batch 3       rows 9-13    50/105   47.6%
batch 3, four packages, cd counted once as its upstream manuscript   rows 9-12   28/81   34.6%
```

The batch-3 report carries a **four-package** denominator as well, 81/28 (34.6%), in which `cd` is counted once as its upstream manuscript rather than as two scored rows. That is a different denominator, not an alternative value for this one, and the two are not interchangeable. Correction-log entry four records a defect in which the two were conflated.

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

**2026-09-29, pre-freeze.** The first draft of the derived-metrics block stated `315` claims adjudicated, `94` contradicted, and "83% of adjudicated claims hold". Machine verification of the thirteen rows gives `375` adjudicated, `95` contradicted, `70.1%` correct. The error was in the summary block only; every row total in the table above was correct and each row sums correctly. Caught by hand-check against the rows before any citation. Corrected in place; the pre-correction values are used nowhere in this series as results and are quoted only inside correction records, this one included.

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

**2026-09-30, post-publication, found by an independent falsification attempt.** A fourth defect, of the same species as the first three and in the same layer, was found by an auditor who did not use any instrument in this series. It is recorded here with that provenance because the provenance is the finding.

1. **This file, cross-batch comparability section — a rate paired with the wrong denominator span.** The section attributed `34.6%` to batch 3 while naming rows 9-13 as batch 3's rows. Batch 3 contributes **five** rows, not four, because the `cd` programme contributes both its upstream row (12) and its audit-manuscript row (13); the four-package figure of `34.6%` counts `cd` once. Rows 9-13 give `50/105 = 47.6%`. Rows 9-12 give `28/81 = 34.6%`. The corrected rate for the span the section names is **47.6%**, and the section now states both denominators and says which is which. **Every one of the thirteen rows was correct before this correction and is correct after it**, and no row, count or per-package figure moved; the failure was entirely in a sentence in the summary layer, which is the same layer that failed three times already. `E1-AGGREGATE.md` carried the same mispairing and is corrected with it.

The origin is traceable and the loss is not the batch-3 auditor's. `batch3/REPORT.md` reports both denominators and states them explicitly — "L3 across the five rows: 105 claims, 50 supported (47.6%)" and "L3 across four packages: 81 claims, 28 supported (34.6%)" — and its comparability caveat names both again: "This batch is at 28/81 (34.6%) on the same denominator definition, or 50/105 (47.6%) including the audit-paper row." The primary record was right on both counts and said so twice. The error entered the dataset on the way in.

**How it was caught, and what that implies.** Not by row-level reconciliation, which passes: the rows sum correctly and the block agrees with them. Not by the reconciliation of the arithmetic three, which compares sums against sums and cannot see a rate attached to the wrong span. It was caught by an auditor who re-derived the cross-batch split from the row table and compared the re-derived rate against the rate the section attached to the span. The row-level reconciliation this file relies on was never applied to this sentence, and the correction log's third entry had claimed this section was repaired. A log entry that says "corrected in place" about a section that still contains a wrong figure transfers more assurance than a log with no entry at all.

The error was not neutral in direction: pairing the four-package rate with the five-row span inflated the apparent granularity gap from 31.3 points to 44.3 points. The granularity caveat below is unchanged by this correction — 47.6% is still a rate conditioned by a different claim convention and is still not a defect rate — but it is now the right number under the right caveat.

**2026-09-30, post-publication, same falsification attempt.** A fifth entry, recording defects in the **evaluation apparatus** rather than in this file's numbers. The thirteen rows, the derived-metrics block and the gradient block are untouched by every item below; the rows were correct before this entry and are correct after it.

1. **The paper's figure pipeline never opened this file.** `figures/make_figures.py` read only two CSVs, both transcribed from this dataset, and compared them against a block of `RECORDED_*` constants transcribed from this dataset by the same author in the same script. Corrupting this file in a throwaway copy — the claim total and the batch-3 rate — left the script exiting 0 and writing byte-identical figures. The dataset was not in the dependency graph, so divergence between transcription and source was unobservable. **The pipeline has been changed rather than the claim weakened**: the script now locates and parses this file, derives every expected value from it, diffs the CSVs against it cell by cell, and aborts without writing when the three disagree. Corrupting this file now aborts the build.
2. **The script asserted the defect in item one of the previous entry.** It hard-coded `BATCH3_ROWS = range(9, 13)`, a four-row span, against a `34.6%` pass condition, while its own comment named the exclusion. A correct dataset edit would have failed the build. Removed with the constants.
3. **The figure caption described a panel the generator does not draw.** The caption for the gradient figure described panels (a), (b) and (c); the generated PDF contains (a) and (b) only. This is a relation failure of the third counterexample class inside the evaluation apparatus, and it was uncatchable by the instruments in this series because no instrument read the manuscript. The caption has been corrected to describe what the artifact contains.
4. **A derived column was cross-checked against itself.** The committed CSV carried an `l7_internal_supported` flag with no counterpart in this file's row table, and the script's "redundant encoding" check compared it to another column of the same CSV. The column has been removed; internal consistency is now computed from the transcribed `L7 internal` column and diffed against this file's table.
5. **Two of the three class names below had been renamed in the published artifact.** They now read exactly as this section records them.
6. **Two instrument-level defects: a disjointness assertion that cannot fail, and a known-defect detector that is a blocklist.** Both are described in the paper, which states plainly what each check can and cannot detect. Neither changes a number.
7. **A dead citation.** `E1-AGGREGATE.md` cited `ARTIFACT-TO-CLAIM-RUBRIC.md` v1.0, a filename that does not exist in any published layout. Corrected to `ARTIFACT-TO-CLAIM-RUBRIC-v1.0.md`, and the v1.0-layer / v1.1-unit relationship is now stated rather than left to be inferred.

The pattern across entries four and five is the one worth recording. Every item was invisible to this study's own instruments, and the reason is structural rather than incidental: the self-check and the thing it checks share an author and a timestamp. A block of constants transcribed from a markdown table, checked against a CSV transcribed from the same markdown table by the transcriber, verifies that the transcriber was consistent with himself. Entries one through three were found because a human re-derived the numbers by hand. Entries four and five were found by a party who wrote their own derivation code, imported no module of ours, and never opened our working tree. That is the methodological result this series now carries, and it is a limitation of the method rather than a defect in one number: **a self-verification apparatus cannot be relied on to detect a correspondence failure in itself.** The fix is not a better blocklist. It is a dependency graph in which the checked source is a committed input rather than a constant, plus a verifying instrument authored independently of the artifact it checks. Both are now in place for the pipeline; neither is in place for the manuscript, and we do not claim otherwise.

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

### Bit-for-bit artifact reproduction, by scored row

This is **not** a column of the row table and must not be read as one: the rubric records
reproduction as a layer verdict, and `U2 reproduces` is `Y` for any regeneration under auditor
execution, including one that differs in the last place of a float. Bit-for-bit is a strictly
stronger statement, it was measured per package by each batch's evaluator, and it had no recorded
field anywhere in this series until this block was added. Papers built on this dataset quoted a
count of it --- three, in one place and four in another, neither traceable --- which is correction
log entry five. The block is here so that a count is derivable rather than asserted. Sources are
the three batch reports named in this file's header; `exact` means the regenerated artifact is
byte-identical to the committed one over every field.

```
cd-ieee-package          exact   SHA-256 4242d117, identical three independent ways
cd-covert-anomaly-detection  exact   its data/metrics.json is byte-identical to the upstream artifact
h266-drl-iccpr2026-package   exact   two full process runs, every scientific field byte-identical
qce-ieee-package         exact   all 4 policies, 8 fields, exact float equality
sra-ieee-package         exact   all 45 rows, 5 fields, exact float equality
icft2026-package         exact-scientific-fields-only   one wall-clock field differs
```

So **5 of 13 scored rows reproduce bit-for-bit, and a sixth (`icft`) does so on every scientific
field with one wall-clock field differing.** Batch 1 contributes none: `adan` reproduces to
2.2e-16, `isac` to 1.8e-12, and `sc` reproduces 540 of 720 records bit-exactly while failing on
precisely the 180 carrying its recommended operating point. Note that neither `adan` nor `isac`
nor `sc` is thereby excluded from the ten reproducing rows; bit-for-bit and reproduces are
different claims with different evidence, and only the second is a column of the row table.

## Evaluator discipline, recorded for the conflict declaration

Eight auditor self-corrections across three batches. Three are methodologically material:

1. A batch-3 auditor **overturned the rubric's own assertion** that `h266`'s JSONs were non-bit-reproducible, after eliminating a confound: training two agents in one process yields a false positive because `evaluate_agent` samples from the policy, so the second evaluation inherits an advanced RNG stream.
2. A batch-3 auditor **declined to inherit five numbers** — `69.27 / 63.37 / 56.71 / 64.79 / 61.23` — that appear in no committed artifact.
3. A batch-3 auditor nearly published a **false contradiction against the rubric's own reference case** through an off-by-one in a sweep index, caught it before reporting, and recorded the correction.
