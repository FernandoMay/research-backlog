# Artifact-to-Claim Integrity: A Layered Method for Detecting Reproducibility, Correspondence, and Package-Level Failures in Computational Research

ACM `sigconf` manuscript reporting a methodology paper built on a **frozen
primary dataset**. This is a report of completed work, not a proposal. Every
quantitative claim in the manuscript traces to a file on disk, and the figure
script re-derives the aggregates from the frozen row table and aborts if any
value disagrees.

**Status: compiled and verified.** 17 pages, three `pdflatex` passes, zero
errors, zero undefined references, zero undefined citations, zero overfull
boxes. Six `Underfull \vbox` page-fill warnings and no `Underfull \hbox`: ACM
`sigconf` runs `\flushbottom`, so these appear wherever a page break leaves
slack, and none is a line overflowing or a figure mis-sized. Both figures are
embedded as vector PDF Form XObjects (2 Form XObjects, 0 Image XObjects,
0 JPEG/DCTDecode streams).

---

## Quick path

```bash
# 1. Verify the figures reproduce from the committed data (read-only, exits 0)
python3 figures/make_figures.py --verify

# 2. Verify the corpus: aggregates, layer labels, byte-identity, stale strings
#    (read-only, exits 0; use --root to point at a throwaway tree)
python3 verify_dataset.py

# 3. Regenerate both figures (rewrites the two PDFs, byte-stable in content)
python3 figures/make_figures.py

# 4. Compile the manuscript
cd /Users/fmf/Documents/research-papers/artifact-to-claim-integrity
/Library/TeX/texbin/pdflatex -interaction=nonstopmode main.tex   # x3
```

No third-party Python packages are required. `make_figures.py` is
standard-library only and emits vector PDF with a built-in base-14 font
writer, so it runs on any machine with a Python 3 interpreter.

---

## What the paper claims

Four claims, in descending order of how much I would defend them.

**C1 --- Correct numerical output is not sufficient evidence of
artifact-to-claim integrity.** In a frozen corpus of 13 scored rows over 12
distinct packages: all 13 contain at least one claim contradicted by their own
artifacts; 10 of 13 artifacts reproduce under auditor execution; 0 of 13
packages achieve a `SUPPORTED` verdict. The reproduced group and the supported
group are **disjoint**, and that disjointness is machine-checked on every run
of the figure script.

**C2 --- The gap decomposes into three failure classes, and two of them are
invisible to a reproduction check.** Circular validation (the artifact
reproduces a property derived from the assumption it purports to validate);
contradictory verification (a supplied verifier compiles, runs, exits 0, and
disagrees with the claim it is bundled with); semantic correspondence failure
(the artifact exists, runs, and implements a different mechanism from the one
it names).

**C3 --- The relation between an artifact and a claim is a distinct unit of
analysis, and it is where the consequential failures live.** Two artifacts can
both exist and both run while the relation between one of them and its claim
is entirely absent. In 8 of 13 rows the relation is absent for at least one
claim. Relation failures survive reproduction and survive a number check.

**C4 --- The aggregation layer requires the same audit as the artifacts.**
The dataset's own aggregation layer failed its consistency check four times,
in three entries of the dataset's correction log. Three failures were
arithmetic: one before the freeze on the claim-level totals, two after it on
the verdict distribution and the internal-consistency count, all caught by
row-level reconciliation. The fourth was not arithmetic and is the strongest
instance: the aggregate's headline table carried its layer labels shifted by
one from L3 upward, so every count was correct and only the names were wrong.
That one could not have been caught by reconciliation, because reconciliation
compares sums against sums; it was caught by asserting the label sequence
against the frozen rubric, and that assertion now runs in the verification
script. All four are logged rather than quietly amended. Eight evaluator
self-corrections are in the record, three of them methodologically material.

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

---

## The three headline numbers, and why the third is not the headline

| Quantity | Value | Why it is or is not the lead |
|---|---|---|
| Packages containing at least one contradicted claim | **13/13** | Lead. Categorical, denominator fixed at 13, comparable across batches, not confusable with a verdict count. |
| Artifacts reproducing under auditor execution | **10/13** | Lead. Same denominator, same comparability. |
| Packages achieving full package-level support | **0/13** | Lead. The negative of the same question. |
| Claims correct | 263/375 (70.1%) | **Not the lead.** Conditioned by two claim granularities; reported as descriptive in the same sentence that gives the conditioning. |

The two quantities a reader is most likely to conflate --- `13/13` containment
and the `0/8/5` verdict distribution --- are reported separately and with a
figure panel that places them side by side. Conflating them was the specific
error that rubric v1.1 was written to correct.

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
| Batches 1-2 claim pool / correct / rate | 270 / 213 / 78.9% | same block, "Cross-batch comparability" section |
| Batch 3, 4 packages | 81 / 28 / 34.6% | same section (the 34.6% figure is over 4 packages) |
| Batch 3, 5 scored rows | 105 / 50 / 47.6% | `batch3/REPORT.md`, Denominator A |
| Reproduced rows by verdict: 0 / 7 / 3 | n=10 | roll-up of the frozen row table; machine-checked by the figure script |
| Non-reproduced rows by verdict: 0 / 1 / 2 | n=3 | same |

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

Entry 3 is the one that constrains the method, and the reason it is worth
recording separately: **row-level reconciliation cannot find it.** That check
compares sums against sums, so a summary whose counts are all correct
reconciles perfectly while naming the wrong layer. Finding it required parsing
the label sequence and asserting it against the rubric's names in order, which
is why `verify_dataset.py` asserts exactly that.

No correction changes the central result. Before, during and after: 0 of 13
`SUPPORTED`, 10 of 13 reproduce, 13 of 13 contain a contradicted claim, and the
gradient is `13/13 -> 10/13 -> 1/13 -> 0/13`.

---

## TODO markers

Four literal `TODO(...)` markers remain in `main.tex`. None is estimated or
filled with a placeholder number.

**1. `TODO(per-row U3 reason code)`** --- Section 5.3, line 779.
*Wants:* a frozen assignment of each relation-absent row to a specific absence
mechanism (constructed-and-discarded / replaced / never-built).
*Blocked because:* the frozen U3 column is binary. The batch reports
establish the three mechanisms but do not record which rows they were observed
in. Resolving it is re-adjudication of 8 rows after the fact, which would
break the freeze this paper reports against.

**2. `TODO(single-granularity re-adjudication)`** --- Section 8.3, line 1208.
*Wants:* the total claim count and the correct rate at one fixed claim
granularity across all 13 rows.
*Blocked because:* requires re-adjudicating all 13 rows under the rubric's U1
definition and re-freezing the dataset. That is a new corpus version, not a
correction to this one. It is the single change that would most improve the
paper's quantitative claims.

**3. `TODO(inter-rater reliability)`** --- Section 8.6, line 1264.
*Wants:* an agreement coefficient over the four-unit scheme.
*Blocked because:* each batch had a single evaluator (batch 1 a delegated
agent, batches 2 and 3 separate agents) and no row was double-coded. A second
adjudicator would have to re-score a sample from the artifacts without access
to the first adjudicator's findings. The statistic does not exist in the frozen
record and cannot be reconstructed from it.

**4. `TODO(novelty assessment)`** --- Section 8.7, line 1286.
*Wants:* a positioning review against published work on artifact evaluation
and reproducibility measurement, with a comparison table against prior
taxonomies of artifact-to-claim failure.
*Blocked because:* requires a literature search, an inclusion criterion, and
verification of the subject packages' own references. None exists in the
available material, and inventing citations was prohibited for this series.
This is the gap a reviewer will press hardest.

---

## Files

| Path | Lines | What it is |
|---|---:|---|
| `main.tex` | 1602 | The manuscript. ACM `sigconf`, `review` option, single-column 506.3 pt text block. |
| `main.pdf` | --- | Compiled output, 17 pages. |
| `README.md` | --- | This file. |
| `verify_dataset.py` | 762 | Cross-file verification. Recomputes the dataset's aggregates from its rows, asserts the aggregate's layer labels against the rubric, re-rolls the layer counts from the batch reports, and proves the two pushed copies are byte-identical. Exits 1 on any mismatch. |
| `figures/make_figures.py` | 1007 | Stdlib-only figure generator. Recomputes every derived value and aborts on mismatch. |
| `figures/data/e1_rows.csv` | 14 | Verbatim transcription of the frozen 13-row table. |
| `figures/data/failure_classes.csv` | 22 | Transcription of the taxonomy section plus the cross-package findings. |
| `figures/fig_layer_gradient.pdf` | --- | 520 x 396 pt, vector. |
| `figures/fig_failure_classes.pdf` | --- | 520 x 304 pt, vector. |

## The figure script's guarantees

`figures/make_figures.py` is not a plotting convenience. It is a check that
happens to draw:

1. **Row-additivity.** Every row's `correct + contradicted + unsupported`
   must equal its own total, before any column is summed.
2. **Aggregate agreement.** Column totals must equal every figure the
   manuscript quotes: 375 / 263 / 95 / 17, 13, 10, 13, 8, 1, and the gradient
   tuple `(13, 10, 1, 0)`.
3. **Percentage round-trip.** `round(263/375 * 100, 1)` must equal `70.1`, and
   likewise for 25.3, 4.5, 78.9, 34.6 and 47.6. A percentage that no longer
   follows from its count fails the build.
4. **The central claim.** Zero rows may both reproduce and be `SUPPORTED`. If
   one did, the manuscript's headline would be false and the script exits 1.
5. **Cross-batch pools.** The 270/213, 81/28 and 105/50 subsets must sum
   correctly from the row table.
6. **Layout guards.** Column widths are measured from the text they must
   hold; a heading or legend that would overrun its column raises rather than
   clipping silently.

On any failure it prints `CHECK FAILURES:` to stderr, lists each mismatch
against the frozen record, and exits 1 **without writing either PDF**.

## The two arithmetic corrections are printed, not asserted

`figures/make_figures.py` prints the two arithmetic corrections as *reporting*
output rather than failing on them, because they are properties of the frozen
record that the manuscript must disclose rather than defects that script can
fix. They are also embedded in the reconciliation panel of
`fig_layer_gradient.pdf`, so a reader of the figure alone sees them.

The third correction --- the layer-label shift --- is not printed there,
because the figure predates it and `make_figures.py` is outside the scope of
this fix. It is recorded in `verify_dataset.py` instead, which asserts the
aggregate's layer-label sequence against the rubric and fails if the shift is
reintroduced. That separation is deliberate and is the point: the figure script
reconciles counts, and this defect was in the names.

---

## Build notes for the next person

Toolchain facts that cost time to rediscover:

- `pdflatex` is at `/Library/TeX/texbin/pdflatex` (TeX Live 2026, macOS
  arm64).
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
   pushed to the last two pages despite zero log errors. The figure is now
   520 x 396 pt. If a figure is resized upward, check the page it lands on, not
   just the compile status.
- The 64-character SHA-256 needs manual splitting; it is split at the
  `4242d117...f2537d47` / `56cf1d4161938a629c237675` boundary in Section 5.2.

## Known defect outside this change's edit scope

`figures/make_figures.py` and `figures/data/e1_rows.csv` still carry the same
class of label error that this change fixed across the seven files it was
permitted to edit:

- `make_figures.py` line 629 sets `GRADIENT_LABELS` to include
  `"L6 consistent"`. Internal consistency is **L7**, so the axis label printed
  into `fig_layer_gradient.pdf` names the wrong layer.
- `e1_rows.csv` names its boolean column `l6_internal_supported` and carries a
  second, correctly named `l7_internal` column holding the recorded verdicts.
  `derived()` computes `internal_consistency` from the misnamed one. The value
  is correct; only the name is shifted, which is why no count moves.

Neither was changed here, because both sit outside the seven files this change
was allowed to touch. `verify_dataset.py` scans both and reports the first on
every run as `[STALE, READ-ONLY]` rather than passing over it silently. The fix
renames a column and a label constant and regenerates the figure, which is a
separate change with its own compile and its own page-count check.

## Publication state

**Not submitted, not committed, not pushed.** No `git init`, no commit, no
push was performed on this directory or on any audited repository. The audit
sources under `research-audit/` and `security/` were read only. Publication is
a separate decision by the author, and it should be taken after the
`TODO(novelty assessment)` is resolved, since that is the one gap a reviewer
is certain to press.
