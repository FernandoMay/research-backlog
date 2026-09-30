# Artifact-to-Claim Integrity Audit

A reproducible evaluation of 13 research packages against a frozen rubric, measuring the gap between what computational artifacts produce and what manuscripts claim.

This directory is separate from `BACKLOG.md`, which remains the single source of truth for the research pipeline itself. This directory records the **integrity evaluation** of that pipeline's artifacts.

## Read in this order

| File | What it is |
|---|---|
| [`ARTIFACT-TO-CLAIM-RUBRIC-v1.1.md`](ARTIFACT-TO-CLAIM-RUBRIC-v1.1.md) | The current rubric. Defines the four units of analysis: Claim, Artifact, Relation, Package |
| [`ARTIFACT-TO-CLAIM-RUBRIC-v1.0.md`](ARTIFACT-TO-CLAIM-RUBRIC-v1.0.md) | The first version, retained for audit trail. v1.1 supersedes it |
| [`E1-DATASET-v1.0.md`](E1-DATASET-v1.0.md) | **The frozen dataset.** Every number any paper may cite comes from here |
| [`E1-AGGREGATE.md`](E1-AGGREGATE.md) | Cross-batch aggregate and the central result |
| [`E1-BATCH-1.md`](E1-BATCH-1.md), [`batch2/`](batch2/REPORT.md), [`batch3/`](batch3/REPORT.md) | Per-package audit reports with full discrepancy tables |

## The central result

```
artifact exists                13/13   100%
artifact reproduces            10/13    77%
internal consistency            1/13     8%
package survives whole          0/13     0%
```

**All 13 evaluated packages contained at least one claim contradicted by their own artifacts.** Ten artifacts reproduced under auditor execution, and no package achieved full package-level support under the frozen rubric.

Correct numerical outputs are not sufficient evidence of artifact-to-claim integrity.

## Three failure classes

1. **Circular validation** — the artifact reproduces the property it is meant to validate. `isac` draws its estimator error from the very Cramér-Rao bound it is tested against, and has the most reproducible artifact in the set.
2. **Self-contradicting verification** — the artifact is executable and reproducible, and disagrees with the claim it purposes to verify. `ems`, `qce` and `sra` ship C kernels that compile, exit 0, and contradict their papers, with READMEs instructing readers to run them as verification.
3. **Semantic relation failure** — the artifact exists and runs, but does not implement the mechanism it names. `quantum-k-sat` is a classical search presenting a top-10 exact-amplitude oracle as "measurement".

These are the class names `E1-DATASET-v1.0.md` records. Earlier revisions of this
README and of the methodology paper published two of the three under different
names, and the paper's figure pipeline now parses the names out of that file and
fails its build if either side renames one.

## Known limitations, stated in the dataset

- The corpus was authored primarily by the evaluator's own account, who therefore had direct knowledge of implementation history and publication context. Rules, verdict vocabulary, and package-level criteria were fixed before adjudication to reduce confirmation bias. Negative findings were retained.
- The corpus is small (13 rows) and deliberately heterogeneous in domain.
- Per-claim rates come from two different claim granularities and must be read as indicative. Layer and package verdicts are categorical and are the defensible result.
- The frozen dataset's own aggregation layer failed its consistency check four times, recorded in four entries of the dataset's correction log. Three were arithmetic: before publication on the claim-level totals, and after the freeze on the package verdict distribution and the internal-consistency count, both caught by row-level reconciliation. The fourth was not arithmetic and could not have been caught by reconciliation, because every count was correct: the aggregate's headline table carried its layer labels shifted by one from L3 upward, so 6/13 was labelled L3 Figure when the rubric calls it L4. It was caught by parsing the labels and asserting the sequence against the rubric, and the aggregate file was already public when it was found, so that correction is post-publication. A fifth, also post-publication, attached batch 3's four-package rate of 34.6% to its five scored rows, where 47.6% is correct; reconciliation passes on that one, because a mispaired rate is not a wrong sum. In every instance the thirteen per-package rows were correct and the summary was not, and every correction is retained in the correction log rather than quietly amended, because the aggregation layer requires the same audit as the artifacts.
- Two further defects are in the **verification apparatus** rather than in the dataset, recorded as the correction log's fifth entry. The methodology paper's figure pipeline published a provenance guarantee it did not implement — it compared a transcription against constants in its own source and never opened the dataset, so corrupting the dataset left it exiting 0 and writing byte-identical figures — and a figure caption described a panel the generator does not draw, which is the third failure class occurring inside the evaluation apparatus itself. Both were found by an independent falsification attempt, not by any instrument in this series. The pipeline has since been rebuilt to parse the dataset at build time, so the claim is now true; the structural limitation it exposed is that an apparatus whose checked source is a constant transcribed by its own author cannot be shown to detect a correspondence failure in itself.
- Bit-for-bit artifact reproduction is **not** a column of the row table. It was measured per package by each batch's evaluator and had no recorded field until the correction pass added a block for it: **5 of 13 scored rows** reproduce byte-identically, and `icft` does so on every scientific field with one wall-clock field differing. Do not read that count as a column of the frozen table.

## Papers

Two papers in [`../papers/`](../papers) were produced from this work:

- `soroban-escrow-cost-asymmetry` — lifecycle cost asymmetry and one-sided dispute resolution in a Soroban token-escrow contract family
- `cd-covert-anomaly-detection` — what a twenty-seed anomaly-detection benchmark actually establishes, a benchmark-integrity audit

A methodology paper on artifact-to-claim integrity is in preparation at
`papers/artifact-to-claim-integrity/` and cites `E1-DATASET-v1.0.md` as its
primary dataset. Its build path, from a fresh clone:

```bash
cd papers/artifact-to-claim-integrity
python3 figures/make_figures.py --verify   # parses E1-DATASET-v1.0.md, exits 0
python3 figures/make_figures.py --self-test # proves 5 corruptions abort the build
python3 verify_dataset.py                  # joins the rows against the batch reports
python3 figures/make_figures.py            # regenerates both figures
./build.sh --check                         # finds pdflatex, 3 passes, error gate
```

No third-party Python packages are required; `requirements.txt` exists to say so.
