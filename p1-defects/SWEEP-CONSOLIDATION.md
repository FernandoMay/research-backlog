# P1 Sweep — Consolidated

**Date:** 2026-09-30
**Packages audited:** 7 rows across 6 repositories
**Repairs started:** none, by standing rule
**E1 dataset:** untouched, frozen at v1.0, not re-adjudicated

## Reports

| ID | Package | Reports |
|---|---|---|
| 001 | `leo-routing-itft2026-package`, `i01-leo-edge-orchestration` | [DEFECT-001-LEO.md](DEFECT-001-LEO.md) |
| 002 | `s01-crl-metacognitive` | [DEFECT-002-CRL.md](DEFECT-002-CRL.md) |
| 003 | `qce-ieee-package` | [DEFECT-003-QCE.md](DEFECT-003-QCE.md) |
| 004 | `sgn-ieee-package` | [DEFECT-004-SGN.md](DEFECT-004-SGN.md) |
| 005 | `isac-jasc-ieee` | [DEFECT-005-ISAC.md](DEFECT-005-ISAC.md) |
| 006 | `quantum-k-sat-ieee-package` | [DEFECT-006-QUANTUM.md](DEFECT-006-QUANTUM.md) |

## The contrast table

| Package | Reproduces | Numbers real | Where the defect is |
|---|---|---|---|
| `leo-routing` NSGA-II | yes, bit-exact | **no** | the function that computes them |
| `leo-routing` extended | yes, byte-identical | yes | experiment design; one label |
| `i01-leo-edge-orchestration` | yes, to the decimal | yes | the document that describes them |
| `s01-crl-metacognitive` | yes | yes | the instrument that measures them |
| `qce-ieee-package` | yes | yes | the words that name them |
| `sgn-ieee-package` | partially | yes | the decoder that reads them back |
| `isac-jasc-ieee` | yes, bit-exact | yes | the validation itself, and the figure |
| `quantum-k-sat-ieee-package` | yes, to 1e-15 | yes | three mechanism names inside a correct circuit |

**Every package reproduces.** Not one of the eight rows would be caught by a reproducibility check.

## The finding this sweep supports

> Across seven packages, all of which reproduce their artifacts, the defect was located in eight different places: the function that computes the number, the instrument that measures it, the document that describes it, the words that name it, the decoder that reads it back, the validation that checks it, the design of the experiment, and the labels on the operations inside a correct circuit.
>
> **Only the first is reachable by re-running the code.**

That is a stronger claim than "reproducibility does not imply correctness", because it names the mechanisms rather than asserting the conclusion. It is also the empirical argument for the layered method in `../papers/artifact-to-claim-integrity/`: the layer that separates these eight cases from each other is not the reproduction layer, and no single verdict collapses them.

## The three sharpest cases

**`isac-jasc-ieee` — reproduction of a circular instrument.** The estimation error is drawn from the Cramér-Rao bound it is compared against (`R_est = R_true + randn() * crlb_range(...)`). The validation cannot fail. It also conceals a second defect, a variance consumed as a standard deviation, because against a real estimator that confusion would have surfaced as an estimator beating the bound. Its Figure 5, the range-Doppler map offered as sensing evidence, is `np.random.randn(50,50)` with one element set to 100. Its artifact is simultaneously the most bit-faithful in the sweep and its central claim is unfalsifiable.

**`s01-crl-metacognitive` — a baseline with no causal path.** The without-CRL arm marks every ready DAG node completed without inspecting agent state, so injected failures cannot reach the completion metric. The baseline would report 100% against a system where every agent is permanently failed. The paper correctly refuses to interpret its own 100%, and the stressed experiment it prescribes as the primary route does not exist in the repository.

**`quantum-k-sat-ieee-package` — a correct circuit with three wrong operation names.** The paper says "exact state-vector simulation" and the layer structure is correct. But "measurement" is a top-10 exact-amplitude oracle, "variational parameters" are uniform random draws, and the "depolarizing channel" reduces the state norm from 1.000 to 0.253 at noise 0.3. The chosen operating point p=2 is strictly dominated by p=1 on both metrics.

## What the sweep did not establish

- **No repair.** `nsga2_optimize` remains broken, the CRL baseline still cannot model failure, the LSB decoder still dilutes, the QCE labels are unchanged, and the ISAC estimator is still drawn from its own bound.
- **The cause of GAN_Enc and Adaptive_JND's chance-level bit accuracy in `sgn`** was not established; neither uses the mechanism proven for LSB.
- **Magnitudes** were not established for the SGN oracle-equivalent or the Quantum oracle, only structures. Both saturated on the instances tested.
- **Nothing here touches the E1 dataset.** These packages are a different corpus. The two may be related but they are not the same record.
- **C's kernel and ablation gaps in QCE**, recorded as unverified in DEFECT-003, were not revisited.

## The rule for what comes next

Repairs are designed against this complete set rather than against the first finding, and each one must state which paper properties it is intended to preserve before any code changes. A fix that makes a number differ is not evidence of a fix. The completion criterion is the standing one from the E1 rubric: every quantity in a revised manuscript must trace to an artifact regenerated by the revised code, and the artifact must be regenerated rather than hand-edited.

Two methodological facts from this sweep should carry into that work:

1. **A failed run is a result.** Four reproduction claims in this sweep were nearly reported as passing while the simulator had not run. Each was caught by checking whether the artifact had actually been rewritten.
2. **A reader's own error is part of the record.** DEFECT-006 records an auditor indexing error that briefly looked like a second normalisation defect. A report about code-reading defects should carry its own.
