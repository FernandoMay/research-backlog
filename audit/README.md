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
internal consistency            2/13    15%
package survives whole          0/13     0%
```

**All 13 evaluated packages contained at least one claim contradicted by their own artifacts.** Ten artifacts reproduced under auditor execution, and no package achieved full package-level support under the frozen rubric.

Correct numerical outputs are not sufficient evidence of artifact-to-claim integrity.

## Three failure classes

1. **Circular validation** — the artifact reproduces the property it is meant to validate. `isac` draws its estimator error from the very Cramér-Rao bound it is tested against, and has the most reproducible artifact in the set.
2. **Contradictory verification** — the artifact is executable and reproducible, and disagrees with the claim it purports to verify. `ems`, `qce` and `sra` ship C kernels that compile, exit 0, and contradict their papers, with READMEs instructing readers to run them as verification.
3. **Semantic correspondence failure** — the artifact exists and runs, but does not implement the mechanism it names. `quantum-k-sat` is a classical search presenting a top-10 exact-amplitude oracle as "measurement".

## Known limitations, stated in the dataset

- The corpus was authored primarily by the evaluator's own account, who therefore had direct knowledge of implementation history and publication context. Rules, verdict vocabulary, and package-level criteria were fixed before adjudication to reduce confirmation bias. Negative findings were retained.
- The corpus is small (13 rows) and deliberately heterogeneous in domain.
- Per-claim rates come from two different claim granularities and must be read as indicative. Layer and package verdicts are categorical and are the defensible result.
- The frozen dataset's own summary block initially contained inconsistent aggregate counts, detected by row-level reconciliation before publication and corrected. The correction is retained in the dataset's correction log, because the aggregation layer requires the same audit as the artifacts.

## Papers

Two papers in [`../papers/`](../papers) were produced from this work:

- `soroban-escrow-cost-asymmetry` — lifecycle cost asymmetry and one-sided dispute resolution in a Soroban token-escrow contract family
- `cd-covert-anomaly-detection` — what a twenty-seed anomaly-detection benchmark actually establishes, a benchmark-integrity audit

A methodology paper on artifact-to-claim integrity is in preparation and will cite `E1-DATASET-v1.0.md` as its primary dataset.
