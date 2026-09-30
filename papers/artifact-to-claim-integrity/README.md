# Artifact-to-Claim Integrity: A Layered Method for Detecting Reproducibility, Correspondence, and Package-Level Failures in Computational Research

ACM `sigconf` manuscript reporting a methodology paper built on a **frozen
primary dataset**. This is a report of completed work, not a proposal. Every
quantitative claim in the manuscript traces to a file on disk, and the figure
script **parses the frozen dataset at build time**, re-derives every value it
draws from it, and aborts without writing anything if any of them disagrees.

**Status: compiled and verified.** 21 pages, three `pdflatex` passes, zero
errors, zero undefined references, zero undefined citations, zero overfull
boxes, zero LaTeX and package warnings. Both figures are embedded as vector PDF
Form XObjects (2 Form XObjects, 0 Image XObjects, 0 JPEG/DCTDecode streams).

---

## Quick path

Two layouts exist and both are supported. In a **public clone** of the corpus
repository the paper is at `papers/artifact-to-claim-integrity/` and the audit
corpus at `audit/`. In the **author's working tree** it is at
`research-papers/artifact-to-claim-integrity/` and the corpus at
`research-audit/`. Every script discovers which one it is in by walking up from
its own location; there is no absolute path and no home-directory path
anywhere in this directory.

```bash
# Step 0. Get to the paper directory. Use whichever line matches your checkout.
cd papers/artifact-to-claim-integrity          # public clone
# cd research-papers/artifact-to-claim-integrity   # author's tree

# 0a. Confirm there is nothing to install. Standard library only.
python3 -c "import sys; print('python', sys.version.split()[0])"

# 1. Verify the figures agree with the frozen dataset (read-only, exits 0).
#    Parses audit/E1-DATASET-v1.0.md, so it fails if the CSVs or the dataset
#    disagree, and prints where it found the dataset.
python3 figures/make_figures.py --verify

# 1b. Prove the guarantee is real: corrupt the dataset five ways in memory and
#     require the checks to fail every time. Writes nothing, touches nothing.
python3 figures/make_figures.py --self-test

# 2. Verify the corpus: aggregates against the rows, the rows against the three
#    primary batch reports, cross-batch spans, layer labels, byte-identity,
#    stale figures derived from the correction log. Read-only, exits 0.
python3 verify_dataset.py

# 3. Regenerate both figures. Byte-identical on every run.
python3 figures/make_figures.py

# 4. Compile the manuscript. Finds pdflatex itself, runs three passes, and
#    fails on any LaTeX error, undefined reference, undefined citation or
#    overfull box. Says which platforms to install TeX on if it cannot.
./build.sh --check
```

`requirements.txt` exists and lists nothing, because there is nothing to
install: `make_figures.py` is standard-library only and emits vector PDF with a
built-in base-14 font writer rather than a plotting library. `verify_dataset.py`
is standard-library only too. `build.sh` is `/bin/sh`. The only external
toolchain is a LaTeX installation, needed **only** to rebuild the PDF; the
committed `main.pdf` is there to be read.

The previous version of this README began with `cd
research-papers/artifact-to-claim-integrity`, a path that exists in no published
layout, and its step 4 hard-coded `/Library/TeX/texbin/pdflatex`, a
macOS-specific absolute path, in the same block of instructions that asserted
both scripts were runnable by someone who is not the author. A cold-start
reproduction failed at step zero. Both are fixed: the layout is discovered, and
the toolchain is discovered.

---

## What the paper claims

Four claims, in descending order of how much I would defend them.

**C1 --- Correct numerical output is not sufficient evidence of
artifact-to-claim integrity.** In a frozen corpus of 13 scored rows over 12
distinct packages: all 13 contain at least one claim contradicted by their own
artifacts; 10 of 13 artifacts reproduce under auditor execution; 0 of 13
packages achieve a `SUPPORTED` verdict. No reproducing row is `SUPPORTED`, and
the **joint distribution** — 0/7/3 among reproducing rows, 0/1/2 among the rest
— is recomputed by the figure script on every run and fails the build if either
block contains a `SUPPORTED` verdict. An earlier version of this file called the
*disjointness* of the two sets "machine-checked". It was not, and the paper now
says so: the sets are disjoint because the `SUPPORTED` column is empty, which
makes the disjointness assertion subsumed by an assertion already made. The
joint distribution is the part that carries content and can fail.

**C2 --- The gap decomposes into three failure classes, and two of them are
invisible to a reproduction check.** Circular validation (the artifact
reproduces a property derived from the assumption it purports to validate);
self-contradicting verification (a supplied verifier compiles, runs, exits 0, and
disagrees with the claim it is bundled with); semantic relation failure
(the artifact exists, runs, and implements a different mechanism from the one
it names). These are the frozen dataset's own class names, unmodified; an
earlier version of this paper and of the figure CSV published two of the three
under different names, and the figure script now parses the names out of the
dataset and fails the build if either side renames one.

**C3 --- The relation between an artifact and a claim is a distinct unit of
analysis, and it is where the consequential failures live.** Two artifacts can
both exist and both run while the relation between one of them and its claim
is entirely absent. In 8 of 13 rows the relation is absent for at least one
claim. Relation failures survive reproduction and survive a number check, and
they occur at every level of reproduction fidelity in the corpus: two of the
four correspondence-failure packages are the best reproduction results in their
own batches.

**C4 --- The aggregation layer requires the same audit as the artifacts, and
an apparatus that checks itself is the weakest kind of audit there is.**
The dataset's own aggregation layer failed its consistency check four times,
across four entries of the dataset's correction log. Three failures were
arithmetic: one before the freeze on the claim-level totals, two after it on
the verdict distribution and the internal-consistency count, all caught by
row-level reconciliation. The fourth was not arithmetic: the aggregate's
headline table carried its layer labels shifted by one from L3 upward, so every
count was correct and only the names were wrong. A fifth, also in the summary
layer, attached batch 3's four-package rate to its five scored rows and so
reported 34.6% where 47.6% was correct; reconciliation passes on that one, because
a mispaired rate is not a wrong sum. Both of those are now caught by a check
that joins the frozen row table against the per-row claim columns of the three
batch reports — primary records written by three separate evaluators, never
transcribed by us.

Two further defects are in the **verification apparatus**, and they are the
reason the paper now states a limitation of its own method. The figure pipeline
published a guarantee it did not implement: it read two CSVs and compared them
against constants in its own source, never opening the dataset, so corrupting
the dataset left it exiting 0 and writing byte-identical figures. And a figure
caption described a panel the generator does not draw — this paper's own third
failure class, inside its own apparatus. Both were found by an independent
falsification attempt that wrote its own derivation code, imported no module of
ours, and never opened our working tree. The pipeline has since been rebuilt so
the claim is true: `make_figures.py` now parses the dataset, diffs the CSVs
against it cell by cell, and `--self-test` proves five corruptions each abort
the build. Seven defects in total are logged rather than quietly amended. Eight
evaluator self-corrections are in the record, three of them methodologically
material.

---

## What the paper does not claim

Stated plainly, because these are the claims a reviewer will test first.

- **No prevalence claim.** Nothing here describes packages outside the 13
  audited rows. Per rubric rules R5 and R6, every rate carries its denominator
  and none is extrapolated.
- **No defect rate.** `70.1% of claims correct` is **not** presented as a
  defect-complement rate. The 375-claim pool mixes two claim granularities, so
  the figure is descriptive only. See `TODO(single-granularity
  re-adjudication)`.
- **No novelty claim.** No assessment against prior work in
  reproducibility methodology or artifact evaluation has been performed. This
  manuscript has **no reference list**, by the same deliberate choice made in
  the two earlier papers of this series: inventing references would be a worse
  defect than the absence. See `TODO(novelty assessment)`.
- **No inter-rater reliability.** Each batch was adjudicated by a single
  evaluator and no row was independently double-coded. See
  `TODO(inter-rater reliability)`.
- **No blind audit.** The corpus was authored primarily by the first author.
  First-author authorship is treated as an experimental property of the
  dataset, not an editorial confession: an author-controlled corpus is the only
  way to distinguish a badly designed artifact from one designed to mislead.
  The weakness for generalisation and the strength for mechanism attribution
  are the same fact.
- **No mechanistic binding to the artifacts themselves.** This paper reports
  the method and its results. It does not report the individual packages' full
  evidence, which lives in the three batch reports.
- **No claim that a self-check verifies itself.** The pipeline's guarantee runs
  from the frozen dataset to the figures. It does not cover `main.tex`, which is
  typeset by hand; the guard over the typeset table is derived from the
  correction log rather than a diff, and cannot find a defect nobody recorded.
  Section 6.4 of the manuscript states this as a limitation of the method after
  an independent falsification attempt found a caption describing a panel the
  generator does not draw --- uncatchable by every instrument in this directory.
- **No claim that bit-for-bit reproduction is a corpus statistic.** It is a
  strictly stronger statement than `reproduces`, it was measured per package
  rather than adjudicated as a layer, and it had no recorded field until the
  correction pass added one. The corrected figure is **5 of 13 scored rows**,
  with a sixth (`icft`) matching on every scientific field but one wall-clock
  field. An earlier version of this file quoted three, and the manuscript quoted
  three in one place and four in another; neither number was traceable to
  anything in the corpus.

---

## The three headline numbers, and why the third is not the headline

| Quantity | Value | Why it is or is not the lead |
|---|---|---|
| Packages containing at least one contradicted claim | **13/13** | Lead. Categorical, denominator fixed at 13, comparable across batches, not confusable with a verdict count. |
| Artifacts reproducing under auditor execution | **10/13** | Lead. Same denominator, same comparability. |
| Packages achieving full package-level support | **0/13** | Lead. The negative of the same question. |
| Claims correct | 263/375 (70.1%) | **Not the lead.** Conditioned by two claim granularities; reported as descriptive in the same sentence that gives the conditioning. |

The two quantities a reader is most likely to conflate --- `13/13` containment
and the `0/8/5` verdict distribution --- are reported separately, and a note
column of the gradient figure places them side by side under the heading
"Verdict vs. containment". An earlier caption described this as a third panel,
which the figure does not contain. Conflating the two quantities was the
specific error that rubric v1.1 was written to correct.

---

## Number provenance

Every number in `main.tex`, and where it comes from. `E1-DATASET-v1.0.md` is
the frozen dataset of record (frozen 2026-09-29); the three batch reports are
the evidence base it names, and carry the per-package mechanism detail.

### Aggregates and derived metrics

| Quantity | Value | Source |
|---|---|---|
| Rows / distinct packages | 13 / 12 | `E1-DATASET-v1.0.md` header |
| Claims adjudicated / correct / contradicted / unsupported | 375 / 263 / 95 / 17 | `E1-DATASET-v1.0.md`, derived-metrics block |
| Same, as percentages | 70.1% / 25.3% / 4.5% | same block |
| Artifact exists / reproduces | 13/13, 10/13 | same block |
| Relation broken by contradiction / absent | 13/13, 8/13 | same block |
| Internal consistency (L7) | 1/13 | same block; corrected, see "Resolved corrections" below |
| Verdict distribution (row roll-up) | 0 SUPPORTED, 8 PARTIALLY, 5 CONTRADICTED | roll-up of the frozen row table, confirmed by all three batch reports |
| Packages with >= 1 contradicted claim | 13/13 | derived-metrics block |
| Packages with >= 1 unsupported claim | 8/13 | derived-metrics block |
| Gradient 13/13 -> 10/13 -> 1/13 -> 0/13 | as stated | `E1-DATASET-v1.0.md`, "The central result" block |
| Batches 1-2 claim pool / correct / rate, rows 1-8 | 270 / 213 / 78.9% | same file, "Cross-batch comparability" fenced block; span and rate parsed at build time |
| Batch 3, 5 scored rows, rows 9-13 | 105 / 50 / **47.6%** | same block; this is the rate the paper quotes |
| Batch 3, 4 packages, rows 9-12 | 81 / 28 / 34.6% | same block, and `batch3/REPORT.md` "Denominator B". A **different** denominator, not an alternative value |
| Reproduced rows by verdict: 0 / 7 / 3 | n=10 | roll-up of the frozen row table; recomputed and checked by the figure script |
| Non-reproduced rows by verdict: 0 / 1 / 2 | n=3 | same |
| Rows reproducing bit-for-bit | 5 / 13 | dataset's "Bit-for-bit artifact reproduction" block; every named repository asserted to be a scored row |
| Rows reproducing bit-for-bit except one wall-clock field | 1 / 13 (`icft`) | same block, scope `exact-scientific-fields-only` |
| `cd` three-way SHA-256 | `4242d117dff67c716523e694704ca918f2537d4756cf1d4161938a629c237675` | `batch3/REPORT.md:565-567`, three lines, one hash |

### Correction log and evaluator discipline

| Quantity | Value | Source |
|---|---|---|
| Pre-freeze wrong summary | 315 adjudicated, 94 contradicted, 83% correct | `E1-DATASET-v1.0.md`, correction log, entry 1 |
| Corrected values | 375, 95, 70.1% | same |
| Derived errors from those | 1.19x on the denominator, 12.9 points on the rate | arithmetic on the two rows above, shown inline in the manuscript |
| Post-freeze wrong verdict roll-up | 0 / 7 / 6 | same, entry 2 |
| Post-freeze corrected roll-up | 0 / 8 / 5 | same |
| Post-freeze wrong internal consistency | 2/13 | same, entry 2 |
| Post-freeze corrected internal consistency | 1/13 | same |
| Post-publication layer-label shift | L3..L7 shifted to L4..L8 in the aggregate headline table; counts unaffected | same, entry 3 |
| Post-publication batch-3 rate/span mispairing | 34.6% attached to rows 9-13; the five rows give 47.6% | `batch3/REPORT.md` "Denominator A"; re-derivation of the row table | entry 4 |
| Post-publication figure pipeline never opened the dataset | exit 0 and byte-identical PDFs on a corrupted dataset | throwaway-copy corruption test | entry 5 |
| Declined inherited numbers | 69.27, 63.37, 56.71, 64.79, 61.23 | `E1-DATASET-v1.0.md`, evaluator discipline item 2 |
| Total evaluator self-corrections | 8 across 3 batches | `E1-DATASET-v1.0.md` |

### Per-package mechanism evidence

| Quantity | Value | Source |
|---|---|---|
| isac: most exact reproduction in corpus | 1.8e-12 | `E1-DATASET-v1.0.md`, counterexample class 1 |
| isac: summary table agreement | 55 of 55 cells | `E1-BATCH-1.md`, "What survived" |
| isac: sweep max standard error | 2.64451 (claim: > 4) | `E1-BATCH-1.md`, L3 table |
| isac: velocity spread at lowest level | 104.01 m/s (claim: < 5) | same |
| isac: README table worst error | 33x | same |
| ems: C kernel EIR disagreement | 11.55 dB, opposite sign | `E1-DATASET-v1.0.md`, class 2 |
| ems: C kernel size | 245 lines | `batch2/REPORT.md` |
| ems: main table agreement | 16 of 16 cells, 3 s.f. | same |
| ems: Monte Carlo survival | 0 of 100 below -10 dB, min -3.96 dB | same |
| ems: mis-steering / forfeited gain | 22.87 deg / 14.63 dB | same |
| ems: eavesdropper null magnitude | 3.2e-30, below the 1.42e-14 float64 floor | same |
| ems: stated vs implemented fading sd | 3.0 dB vs 1.4992 dB | same |
| qce: Pareto occurrences | 0 in 696 lines | `E1-DATASET-v1.0.md`, class 3 |
| qce: state space | 32 states enumerated | `batch2/REPORT.md` |
| qce: executed policy | 1 mask, 1 DVFS level, 200 steps | same |
| qce: predictor output range | 0.1500 to 0.5750, safety floor 0.15 | same |
| qce: C kernel reliability | 1.0000 vs paper 0.924 | same |
| qce: policy table agreement | 4 policies, 8 fields, bit-identical | same |
| quantum-k-sat: state vector size | 16,384 complex amplitudes at n=14 | `batch2/REPORT.md` |
| quantum-k-sat: readout | top-10 exact amplitudes vs 2000 WalkSAT flips | same |
| quantum-k-sat: baseline pooled mean | 0.9556 (paper: 0.964 and 0.967) | same |
| quantum-k-sat: effect size | d = 1.558 (paper: 1.14) | same |
| quantum-k-sat: gap trend | 5.7075 -> 5.9694, described as a decrease | same |
| quantum-k-sat: figure agreement | 13 of 14 claims, 4 of 4 figures sound | same |
| mega-constellation: arc / spacing | 21.375 deg at 1.125 deg | `E1-AGGREGATE.md`, finding 3 |
| mega-constellation: out-of-bounds offspring | 110 of 20000 (0.55%) | same |
| mega-constellation: latitude band | 20 latitudes, 0 to 12.25 deg | `batch3/REPORT.md` |
| mega-constellation: max coverage in artifact | 0.5933 | same |
| mega-constellation: correct implementation | 4 of 5 system-model equations; two runs byte-identical | `E1-DATASET-v1.0.md` + `batch3/REPORT.md` |
| icft: detector imports present | none of xgboost, torch, sklearn | `E1-DATASET-v1.0.md`, class 3 |
| icft: HMM state-2 assignment | 4986 of 5000 steps (99.72%) | `batch3/REPORT.md` |
| icft: action counts | 0.75 -> 1597; lowest 0.25 -> 61; two lowest = 128 of 5000 | same |
| icft: table agreement | 20 of 20 cells | same |
| sra: headline effect under a controlled draw | 6.47% vs the claimed 14.9% | `batch2/REPORT.md` |
| sra: metrics artifact | 45 of 45 rows, 5 fields, bit-identical | same |
| sra: unsupported claims | 0 | same |
| h266: reproduction | byte-for-byte, two fresh processes; 1 wall-clock field differs | `batch3/REPORT.md` + `E1-DATASET-v1.0.md` |
| h266: policy genuinely works | 67.93 vs 62.90 uniform random | `E1-DATASET-v1.0.md`, "What survived" |
| h266: action mode flattening | 34.1% -> 18.7% | same |
| h266: own multi-seed file | -10.26% vs fixed, p(vs fixed) = 1.0 | `batch3/REPORT.md` |
| h266: training loop | 1 update call, 120 full-batch steps, buffer 60,000 | same |
| h266: mechanism identities correct | 15 | same |
| cd: three-way hash | `4242d117dff67c716523e694704ca918f2537d4756cf1d4161938a629c237675` | `E1-DATASET-v1.0.md` + `batch3/REPORT.md` |
| cd audit manuscript: claims | 22 of 24 correct, 1 contradicted, 1 unsupported | `E1-DATASET-v1.0.md` |
| cd audit manuscript: SD contradiction | printed values are ddof=0, table declares n-1 | `E1-DATASET-v1.0.md` + `batch3/REPORT.md` |
| cd upstream: claims | 3 correct, 17 contradicted, 1 unsupported of 21 | `E1-DATASET-v1.0.md` |
| cd: kernel buffer overflow | 42 writes into 41 elements, ASan-confirmed | `E1-AGGREGATE.md` |

### Numbers deliberately **not** quoted

- The `78%` action-concentration figure in `batch3/REPORT.md` is not
  reconcilable with the per-action counts given in the same paragraph of that
  report (the top two actions sum to 2865 of 5000 = 57.3%; the top three to
  78.6%). The manuscript quotes the raw counts instead, which are
  unambiguous. Flagged rather than propagated.
- The dataset's pre-correction values (`315`, `94`, `83%`) are quoted **only**
  in the correction-log discussion of Section 4.4 and in the paper's
  conclusion, as the record of a caught error. They are never used as results,
  consistent with the dataset's own instruction that the pre-correction values
  are not quoted in this series. One place in the dataset violated that
  instruction and has been corrected: its cross-batch comparability section
  still described the pooled figures as `315 / 263 / 94 / 17`.

---

## Resolved corrections to the frozen dataset

There is **no live disagreement** between this paper and the dataset. Every
figure quoted above is the corrected one, and the corrections below are all
made and all logged in `E1-DATASET-v1.0.md`'s `## Correction log for this
dataset` section. Nothing here is a choice between two readings; each entry is
a defect that was found, fixed, and recorded.

| Entry | Date | What the summary said | What it is | Status |
|---|---|---|---|---|
| 1 | 2026-09-29, pre-freeze | `315` adjudicated, `94` contradicted, 83% correct | wrong summation in the derived-metrics block | corrected to `375 / 263 / 95 / 17`, 70.1% |
| 2 | 2026-09-30, post-freeze | verdicts `0 / 7 / 6`; internal consistency `2/13` | wrong roll-up, then a miscount of a column | corrected to `0 / 8 / 5` and `1/13` |
| 3 | 2026-09-30, post-publication | aggregate headline table labelled `L3`..`L7` | **layer-label shift; no count was wrong** | corrected to `L4`..`L8` |
| 4 | 2026-09-30, post-publication | batch 3's rate `34.6%` attached to rows 9-13 | **rate paired with the wrong denominator span** | corrected to `50/105 = 47.6%`; the four-package figure is now labelled as a different denominator |
| 5 | 2026-09-30, post-publication | the figure pipeline claimed to abort on dataset divergence | **a provenance guarantee that was not implemented**, plus a caption naming a panel that is not drawn | pipeline rebuilt to parse the dataset; caption corrected; both logged |

- **Entry 2, verdicts.** The row table gives 8 `PARTIALLY` and 5
  `CONTRADICTED`; the block gave 7 and 6. Batch 1 is 3 P / 1 C, batch 2 is 4 P,
  batch 3 is 1 P / 4 C. All three batch reports agree with the row table.
- **Entry 2, internal consistency.** The block recorded `2/13`, counting the two
  rows whose recorded layer stack places internal consistency at `SUPPORTED`:
  `sc-ieee-package` and the `cd` audit manuscript. The recorded
  internal-consistency column marks only the first, because the second is
  `CONTRADICTED` at that layer on the `ddof` disclosure alone. Corrected to
  `1/13`. Note the label: internal consistency is **L7**, which the row table
  already had right and the block did not.
- **Entry 3, the layer-label shift.** `E1-AGGREGATE.md`'s headline table
  labelled its rows `L3 — Figure`, `L4 — Method`, `L5 — Selection`,
  `L6 — Internal consistency`, `L7 — Verdict: SUPPORTED`. Rubric v1.0 fixes
  those as `L4` through `L8`, and all three batch reports score under that
  mapping. Every count was correct — 13/13, 10/13, 6/13 figure, 3/13 method,
  7/13 selection, 1/13 internal consistency, 0/13 verdict — and only the names
  moved. Two related naming errors in the dataset itself were fixed in the
  same pass: the derived-metrics block labelled the internal-consistency line
  `L6`, and the cross-batch section still quoted the pre-correction pooled
  figures `315 / 263 / 94 / 17`.

- **Entry 4, the rate/span mispairing.** The cross-batch section attributed
  `34.6%` to batch 3 while naming rows 9-13 as batch 3's rows. Batch 3
  contributes **five** rows, not four, because the `cd` programme contributes
  both its upstream row (12) and its audit-manuscript row (13). Rows 9-13 give
  `50/105 = 47.6%`; the `34.6%` belongs to rows 9-12, which count `cd` once.
  **Row-level reconciliation passes on this defect**: the rows sum correctly and
  the rate is arithmetically right for the count beside it. What is wrong is the
  pairing of a rate with a span, and reconciliation compares sums against sums.
  The origin is traceable and the loss is not the batch-3 evaluator's — that
  report states both denominators explicitly, twice, as "Denominator A" and
  "Denominator B". The error direction was not neutral: pairing the four-package
  rate with the five-row span inflated the apparent granularity gap from 31.3 to
  44.3 points. Every one of the thirteen rows was correct before this correction
  and is correct after it.
- **Entry 5, the apparatus.** `make_figures.py` compared a CSV against a block
  of `RECORDED_*` constants in its own source, all transcribed by the same
  author from the same markdown, and never opened the dataset at all. Corrupting
  the dataset in a throwaway copy (`375`→`999`, batch-3 rate→`99.9%`) left the
  script exiting 0 and writing **byte-identical** PDFs. The same pass found a
  caption describing a panel the generator does not draw, a derived CSV column
  cross-checked against another column of the same file, a disjointness
  assertion that cannot fail, two of three taxonomy names renamed relative to
  the dataset, and a dead rubric citation. Entry 5 is a package: the machine has
  been rebuilt rather than the claim weakened.

Entries 3 and 4 are the ones that constrain the method, and for different
reasons. **Entry 3 could not have been found by reconciliation at all:** that
check compares sums against sums, so a summary whose counts are all correct
reconciles perfectly while naming the wrong layer. **Entry 4 could not have been
found by it either,** because a mispaired rate is not a wrong sum. Both needed a
different kind of check --- one that parses names, one that parses spans --- and
both of those now run on every invocation of `verify_dataset.py`, against the
per-row claim columns of the three batch reports, which are primary records
written by three separate evaluators.

**Entry 5 is the one that constrains the method most.** A block of constants
transcribed from a markdown table, checked against a CSV transcribed from the
same markdown table by the transcriber, verifies that the transcriber was
consistent with himself. Every defect in entries 4 and 5 was invisible to the
instruments this series had, and all were found by an outside party who wrote
their own derivation code and imported no module of ours. That fact is now a
stated limitation of the method (manuscript §6.4): **an apparatus whose checked
source is a constant transcribed by its own author cannot be shown to detect a
correspondence failure in itself.** The fix is not a longer list of known-bad
strings. It is a dependency graph in which the checked source is a committed
input, which is what the pipeline now is.

No correction changes the central result. Before, during and after: 0 of 13
`SUPPORTED`, 10 of 13 reproduce, 13 of 13 contain a contradicted claim, and the
gradient is `13/13 -> 10/13 -> 1/13 -> 0/13`.

---

## TODO markers

Four literal `TODO(...)` markers remain in `main.tex`. None is estimated or
filled with a placeholder number. Each is a marker for work that is
outstanding; the limitation it stands for is also stated in prose, so no reader
has to infer it from a marker alone.

**1. `TODO(per-row U3 reason code)`** --- Section 5.3.
*Wants:* a frozen assignment of each relation-absent row to a specific absence
mechanism (constructed-and-discarded / replaced / never-built).
*Blocked because:* the frozen U3 column is binary. The batch reports
establish the three mechanisms but do not record which rows they were observed
in. Resolving it is re-adjudication of 8 rows after the fact, which would
break the freeze this paper reports against. The prose states the count and
the three mechanisms and explicitly declines the row-by-row mapping.

**2. `TODO(single-granularity re-adjudication)`** --- Section 8.3.
*Wants:* the total claim count and the correct rate at one fixed claim
granularity across all 13 rows.
*Blocked because:* requires re-adjudicating all 13 rows under the rubric's U1
definition and re-freezing the dataset. That is a new corpus version, not a
correction to this one. It is the single change that would most improve the
paper's quantitative claims.

**3. `TODO(inter-rater reliability)`** --- Section 8.6.
*Wants:* an agreement coefficient over the four-unit scheme.
*Blocked because:* each batch had a single evaluator (batch 1 a delegated
agent, batches 2 and 3 separate agents) and no row was double-coded. A second
adjudicator would have to re-score a sample from the artifacts without access
to the first adjudicator's findings. The statistic does not exist in the frozen
record and cannot be reconstructed from it.

**4. `TODO(novelty assessment)`** --- Section 8.7, and stated first-class in
Section 1.5.
*Wants:* a positioning review against published work on artifact evaluation
and reproducibility measurement, with a comparison table against prior
taxonomies of artifact-to-claim failure.
*Blocked because:* requires a literature search, an inclusion criterion, and
verification of the subject packages' own references. None exists in the
available material, and inventing citations was prohibited for this series.
This is the gap a reviewer will press hardest, which is why Section 1.5 now
states in the introduction that the contribution is a reproducible evaluation
instrument and a primary dataset rather than a demonstrated advance.

---

## Files

| Path | Lines | What it is |
|---|---:|---|
| `main.tex` | 2101 | The manuscript. ACM `sigconf`, `review` option, single-column 506.3 pt text block. |
| `main.pdf` | --- | Compiled output, 21 pages. |
| `README.md` | --- | This file. |
| `requirements.txt` | 18 | Lists nothing, and says so, so nobody has to guess whether a step was missed. |
| `build.sh` | 134 | Finds `pdflatex`, runs three passes, and gates on LaTeX errors, undefined references, undefined citations and overfull boxes. Explains how to install TeX per platform if it cannot find one. |
| `verify_dataset.py` | 1276 | Cross-file verification, checks A0-A9. See below. |
| `figures/make_figures.py` | 1637 | Stdlib-only figure generator. **Parses the frozen dataset** and derives every expected value from it. `--self-test`, `--dataset`, `--print-capabilities`. |
| `figures/data/e1_rows.csv` | 21 | Verbatim transcription of the frozen 13-row table, one column per dataset column, no derived columns. |
| `figures/data/failure_classes.csv` | 28 | The dataset's own class names, plus the cross-package findings. Names are checked against the dataset at build time. |
| `figures/fig_layer_gradient.pdf` | --- | vector. Two panels and a three-column note row. |
| `figures/fig_failure_classes.pdf` | --- | vector. |

`verify_dataset.py` runs nine checks: **A0** reads the canonical L1-L8 layer
table out of the rubric, which every other layer assertion is relative to;
**A1** recomputes the dataset's aggregates from its own rows; **A2** does the
same for the gradient block; **A3** asserts the aggregate's layer labels against
the rubric; **A4** re-rolls every aggregate layer count from the batch reports;
**A5** proves the pushed copies under `research-backlog-repo/audit/` are
byte-identical, and skips *loudly* where that tree does not exist; **A6** scans
for stale figures and shifted layer labels; **A7** prints the gradient;
**A8** joins every cell of the frozen row table against the per-row L3/L7/L8
columns of the three batch reports and checks the bit-for-bit block against the
scored rows; **A9** re-derives the cross-batch split per span and joins it
against per-report totals.

Two of these are new and are the ones that matter. **A8** compares the frozen
row table against primary evidence written by three separate evaluators, so for
the first time the transcription is checked against something this author did
not write: 104 cells across 13 rows. **A9** is the check that would have caught
the rate/span mispairing. **A6** no longer holds a hand-written list of
known-bad strings; its patterns are **parsed out of the dataset's correction log
at run time**, so logging a new correction arms a new guard without editing the
script. Its docstring states plainly what it still cannot do.

## The figure script's guarantees

`figures/make_figures.py` is not a plotting convenience. It is a check that
happens to draw. The first thing to understand about it is **where its
expected values come from**, because that is what determines whether the
guarantee means anything.

### Where every checked value comes from

`E1-DATASET-v1.0.md` is located at run time and **parsed**. Every quantity the
checks compare against is read out of it:

| Checked quantity | Parsed from |
|---|---|
| 13 row records and every cell | the `## Row data` table |
| 375 / 263 / 95 / 17 and the rest of the aggregates | the `## Derived metrics` fenced block |
| 70.1 / 25.3 / 4.5 percent | the fractions written in that block |
| gradient `(13, 10, 1, 0)` | the `## The central result` block |
| row count and distinct-package count | the `**Rows:**` header line |
| batch spans and batch rates | the `## Cross-batch comparability` fenced block |
| the gradient axis's third label | the row table's column header |
| the three failure-class names | `## The three counterexample classes` |
| the pre-correction figures the figure discloses | the `## Correction log` entries |
| the bit-for-bit reproduction count | the `### Bit-for-bit artifact reproduction` block |
| distinct packages (derived from the table's layer qualifiers) | the `## Row data` table |

**There is no `RECORDED_*` constant in the script.** An earlier revision had one,
and the guarantee the manuscript advertised was therefore vacuous.

### The checks

1. **The transcription is diffed, not trusted.** `data/e1_rows.csv` is compared
   cell by cell against the dataset's own row table, and the class names in
   `data/failure_classes.csv` against the dataset's taxonomy list. This
   replaces a check that compared a derived CSV column against another column of
   the same CSV, which could not fail: a transcriber who miscounted produced a
   self-consistent error across both columns.
2. **Row-additivity.** Every row's `correct + contradicted + unsupported` must
   equal its own total, before any column is summed.
3. **Aggregate agreement.** Column totals must equal every figure in the
   derived-metrics block, and the gradient block must equal the recomputed
   gradient with a matching denominator and percentage.
4. **Percentage round-trip.** Each recorded percentage must round-trip from the
   recomputed count, and each cross-batch rate must round-trip from the count
   *paired with the span the dataset names*. A rate attached to the wrong span
   fails, which is the check that did not exist when `34.6%` was published over
   the five-row span.
5. **The central claim.** The joint distribution of reproduction against verdict
   is recomputed, and either block containing a `SUPPORTED` verdict fails the
   build. The disjointness of the two sets is *implied* — the `SUPPORTED` column
   is empty — and the script labels it as implied rather than as a check, because
   an earlier version of this file called it machine-checked and it was a
   tautology.
6. **Bit-for-bit entries are scored rows.** Every repository the dataset lists as
   reproducing byte-identically must be one of the thirteen, or the count the
   manuscript quotes is a count of something outside the corpus.
7. **Layout guards.** Column widths are measured from the text they must hold; a
   heading or legend that would overrun its column raises rather than clipping
   silently.

On any failure it prints `CHECK FAILURES:` to stderr, lists each mismatch against
the frozen record, and exits 1 **without writing either PDF**.

### The guarantee is self-tested

```
$ python3 figures/make_figures.py --self-test
self-test: does corrupting the dataset actually abort this build?
  [ok  ] claim total 375 -> 999: 1 failure(s), first is U1 claims adjudicated: ...
  [ok  ] batch-3 five-row rate 47.6% -> 99.9%: 1 failure(s), first is cross-batch ...
  [ok  ] batch-3 span rows 9-13 -> rows 9-12: 3 failure(s), first is cross-batch ...
  [ok  ] a failure-class name: 1 failure(s), first is failure_classes.csv class names ...
  [ok  ] row 3 correct count 70 -> 71: 1 failure(s), first is e1_rows.csv row 3 ...
  self-test passed: all 5 mutations caught
```

It mutates the real dataset text in memory, in a temporary directory, and
requires the real `check()` to return failures. It writes nothing outside that
directory and touches nothing on disk. A check that cannot fail is not a check,
so this one is required to fail.

### What those guarantees do not prove

Stated because the README would otherwise let a reader over-read them. The
script establishes that the **presentation layer cannot silently diverge from
the frozen dataset**. It does not establish that the frozen dataset is
scientifically correct, that the underlying simulations are valid models of what
their manuscripts claim, or that the claims it adjudicates were the claims a
reader would most want adjudicated. The chain from the frozen dataset to the
figure is verified; the chain from figure to scientific truth is not, and is not
claimed.

The boundary is narrower than the word *generated* suggests, in two places. The
script does not read `main.tex`. `Table I` is typeset by hand from the same
transcription, so the script's guarantee runs from the frozen dataset to the
figures and does not cover the typeset table. What covers the typeset table is
weaker and is now named as such: `verify_dataset.py` reads `main.tex` on every
run and rejects it if it carries a figure the correction log records as
superseded or a layer label that disagrees with the rubric. **That is a guard
derived from the correction log, not a cell-by-cell diff**, and it cannot detect
a defect nobody has written down anywhere. Section 6.4 of the manuscript states
what that limit cost: a caption describing a panel the generator does not draw
was in the manuscript, uncatchable by every instrument in this directory.

---

## The corrections are printed, not asserted

`figures/make_figures.py` prints the two arithmetic corrections as *reporting*
output rather than failing on them, because they are properties of the frozen
record that the manuscript must disclose rather than defects the script can fix.
The pre-correction figures are read out of the dataset's correction log rather
than hard-coded, so the disclosure cannot drift from the record it discloses. The
corrections are also embedded in the reconciliation note of
`fig_layer_gradient.pdf`, so a reader of the figure alone sees them.

The layer-label shift and the rate/span mispairing are not printed there,
because the figure has no panel for them. They are enforced in
`verify_dataset.py` instead: the aggregate's layer-label sequence is asserted
against the rubric, and the cross-batch spans are re-derived from the row table
and joined against the batch reports. That separation is deliberate and is the
point: the figure script reconciles counts, and these two defects were in the
names and in the spans.

## Build notes for the next person

Toolchain facts that cost time to rediscover:

- **`pdflatex` does not need a path.** `build.sh` looks on `PATH` first, then in
  `/Library/TeX/texbin`, `/usr/local/texlive/*/bin/*`, `/opt/homebrew/bin`,
  `/usr/local/bin` and `/usr/bin`, and prints per-platform install instructions
  if it finds none. The previous README hard-coded
  `/Library/TeX/texbin/pdflatex`, which exists on no other machine.
- **`build-pass{1,2,3}.log` are generated** by `build.sh` and are not part of the
  artifact. `main.log`, `main.aux` and `main.out` are the usual `pdflatex`
  by-products.
- **`seqsplit.sty` is not installed.** Long alphanumeric tokens are broken with
  `\allowbreak` inserted manually. `\path` from the `url` package cannot break
  a pure alphanumeric string because it only breaks at punctuation.
- **`enumitem.sty` is not installed.** List spacing is set with the standard
  `\topsep` / `\itemsep` / `\parsep` length assignments.
- **`array` cannot tolerate a line break inside a column preamble.** A `>{...}`
  column spec split across source lines raises
  `Illegal pream-token ... 'c' used`. Every preamble here is one unbroken
  line. (A minimal reproduction was checked in isolation before concluding
  this.)
- **An `l` column never wraps.** Every `tabular` here uses
  `p{}` with `>{\raggedright\arraybackslash}`.
- **A full-width float taller than `\topfraction` can never be placed** and
  gets deferred to the end of the document. An earlier layout of
  `fig_layer_gradient.pdf` was 520 x 561 pt and both figures were silently
  pushed to the last two pages despite zero log errors. Check the page a figure
  lands on, not just the compile status, if you resize one.
- The 64-character SHA-256 needs manual splitting; it is split at the
  `4242d117...f2537d47` / `56cf1d4161938a629c237675` boundary in Section 5.2.

## Known defects

**None outstanding in this directory.** The note is kept because a README that
still claimed a fixed defect was wrong would be its own failure class, and
because the honest list of what was found and fixed is more useful than a
silent repair.

Verified current state:

- `make_figures.py` takes its gradient-axis label for the third rung from the
  dataset's own column header, so `fig_layer_gradient.pdf` prints `L7 internal`
  — the dataset's name, not a synonym. Confirmed by decompressing the figure's
  content streams.
- `e1_rows.csv` has **no derived column**. The previous
  `l7_internal_supported` flag, which was cross-checked against another column of
  the same file and could therefore not fail, has been removed; internal
  consistency is computed from the transcribed `l7_internal` column and diffed
  against the dataset's own table.
- `verify_dataset.py` reports `[STALE]` for any layer label that disagrees with
  the rubric and for any superseded figure outside a correction record. It
  currently reports none.
- `fig_layer_gradient.pdf` contains two labelled panels, (a) and (b), and a
  three-column note row. It does **not** contain a panel (c), and no caption in
  this repository claims it does. Extract the text runs to confirm:

```
python3 - <<'EOF'
import re, zlib, pathlib
d = pathlib.Path("figures/fig_layer_gradient.pdf").read_bytes()
out = []
for m in re.finditer(rb"stream\r?\n(.*?)endstream", d, re.S):
    raw = m.group(1)
    try: raw = zlib.decompress(raw)
    except Exception: pass
    out.append(raw)
print("\n".join(s.decode("latin-1") for s in out))
EOF
```

- The reproduction instructions above work from a fresh public clone. The two
  steps that did not work before — step zero's `cd` to a path that exists in no
  published layout, and step four's hard-coded `/Library/TeX/texbin/pdflatex` —
  are fixed, and `verify_dataset.py` no longer requires the author's
  `security/` directory, so it runs in a clone that has only `audit/`.

## Publication state

**Not submitted, not committed, not pushed.** No `git init`, no commit, no
push was performed on this directory or on any audited repository. The three
batch reports were read only and are unmodified: they are primary evidence and
they were right. Publication is a separate decision by the author, and it should
be taken after the `TODO(novelty assessment)` is resolved, since that is the one
gap a reviewer is certain to press.
