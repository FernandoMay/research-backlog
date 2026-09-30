# Artifact-to-Claim Integrity Rubric v1.1

**Supersedes:** v1.0 (2026-09-29). Retained alongside for audit trail.
**Change:** defines the four units of analysis. v1.0 defined layers but did not fix what a "claim" is counted against, which made cross-batch claim rates non-aggregable. See §Correction.

## Why v1.1 exists

v1.0 scored eight layers and produced a correct gradient, but it left the unit of analysis implicit. That produced a real error: a draft summary conflated *"the package verdict is CONTRADICTED"* (6/13) with *"the package contains at least one claim contradicted by its own artifacts"* (13/13). Both are true. They are different metrics with different denominators, and conflating them in the first paper on artifact-to-claim integrity would have been a defect in the paper's own integrity metric.

The unit of analysis is part of the result, not an editorial detail.

## The four units

### U1 — Claim

**Question:** what does the manuscript assert?

A claim is a proposition in the manuscript that is falsifiable against some artifact. It has exactly one of three statuses, and the three are not interchangeable:

| Status | Meaning |
|---|---|
| `CLAIM-CORRECT` | An artifact contains the asserted value. |
| `CLAIM-CONTRADICTED` | An artifact contains a *different* value. The falsification is measurable. |
| `CLAIM-UNSUPPORTED` | No artifact bears on the claim. The claim is neither confirmed nor refuted. |

`CLAIM-UNSUPPORTED` is the distinct unit. A claim with no artifact and a claim with a contradicting artifact are in different epistemic positions, and merging them inflates the appearance of evidence. v1.0 recorded both in a single L3 column, which is the root of the aggregation defect.

### U2 — Artifact

**Question:** what does the code produce or implement?

Exists if a committed file contains the result. Reproduces if an auditor regenerated it and recorded the output. A verifier that runs and disagrees is neither absent nor correct — it is an artifact that actively misinforms, and is scored as `CONTRADICTED`, not as partial support.

### U3 — Relation

**Question:** does the artifact actually evidence that claim?

This is the unit v1.0 lacked, and it is where the interesting failures live. Two artifacts can both exist and both run, yet the relation between an artifact and a claim can be entirely absent.

- `QCE` asserts Pareto optimality. A 32-state exhaustive enumeration exists and runs. No Pareto computation exists anywhere in 696 lines. The artifact is present; the relation is absent.
- `quantum-k-sat` asserts variational optimisation. A classical search that runs exists. The mechanism does not correspond to the name.
- `SRA`'s makespan is claimed to improve with gate error. The artifact proves the quantity is invariant. The relation is present and negates the claim.

Relation failures are not arithmetic errors. They survive a clean reproduction and a careful number check, and they are the failure mode a conventional reproducibility benchmark cannot detect.

### U4 — Package

**Question:** do manuscript, code, data and figures survive together?

Scored on the layer stack of v1.0 (L1-L8). A package is `SUPPORTED` only if every layer holds. Any contradicted claim moves a package off `SUPPORTED`; the package verdict also accounts for whether the *central* claim is contradicted, not merely whether some peripheral number is wrong.

## Metrics to report, each with its denominator

These are distinct quantities. Never merge them, never quote one as another.

```
Claim-level:      CLAIM-CORRECT / CLAIM-CONTRADICTED / CLAIM-UNSUPPORTED
Artifact:         exists / reproduces
Relation:         broken-by-contradiction / absent
Package:          verdict distribution over the audited set
Package contains ≥ 1 CLAIM-CONTRADICTED
Package contains ≥ 1 CLAIM-UNSUPPORTED
```

## Correction to v1.0, recorded deliberately

v1.0 scored `cd` as a single package with verdict `PARTIALLY SUPPORTED`. The batch 3 auditor established that this conflates two different objects:

- **`cd-ieee-package`** (upstream repository) — artifacts reproduce bit-for-bit, but *both* of its stated conclusions are contradicted by its own artifacts. Verdict: `CONTRADICTED`.
- **The audit manuscript written about it** — `SUPPORTED` on layers L1-L6, holding 22 of 24 claims. Verdict: `PARTIALLY SUPPORTED`, its one contradicted claim being a sample-SD estimator disclosure.

Same research programme, two artifacts, two verdicts. v1.1 scores them separately. The dataset contains 13 scored rows over 12 distinct packages.

## Unchanged from v1.0

Rules R1-R8 all stand, including R5 (no extrapolation beyond the audited set), R6 (never a percentage without its denominator), and R7 (absence of contradiction is not evidence of presence — what survives must be recorded as carefully as what fails).
