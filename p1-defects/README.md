# P1 Defects

Defect reports from the P1 research-hardening sweep: audit of research packages against the bar the rest of the estate is held to.

**This is a different corpus from `../audit/`.** The E1 dataset in `../audit/E1-DATASET-v1.0.md` is frozen at v1.0, covers 13 rows, and is not re-adjudicated on the basis of anything in this directory. The rubric's own assignment rule keeps these as separate records.

## Reports

| ID | Packages | Finding class | Status |
|---|---|---|---|
| [001](DEFECT-001-LEO.md) | `leo-routing-itft2026-package`, `i01-leo-edge-orchestration` | U3 correspondence failure; problem-definition, within-document contradiction, temporal provenance; ablation design not identifiable | Open, nothing corrected |
| [002](DEFECT-002-CRL.md) | `s01-crl-metacognitive` | Instrument failure — baseline has no causal path from stressor to metric; dormant mechanism; absent stressed mode | Open, nothing corrected |
| [003](DEFECT-003-QCE.md) | `qce-ieee-package` | Category misattribution — supervised logistic regression labelled RL; "Pareto-optimal" with no referent; QAOA ansatz that is exhaustive enumeration | Open, nothing corrected |
| [004](DEFECT-004-SGN.md) | `sgn-ieee-package` | Decoder indexing error — `np.unpackbits` dilutes 1 bit/pixel to 8, publishing chance as a result; artifact holds no numbers | Open, nothing corrected |
| [005](DEFECT-005-ISAC.md) | `isac-jasc-ieee` | Circular validation — estimation error drawn from the CRLB it validates; Fisher derivation absent; σ² consumed as σ; range-Doppler figure is noise | Open, nothing corrected |
| [006](DEFECT-006-QUANTUM.md) | `quantum-k-sat-ieee-package` | "Measurement" is a top-10 exact-amplitude oracle; "variational parameters" are random search; the depolarising channel shrinks the norm | Open, nothing corrected |
| [**SWEEP**](SWEEP-CONSOLIDATION.md) | all 7 rows | Cross-report synthesis; where the defect was located each time | **Sweep closed, no repairs started** |

## Method

Code first, then artifact, then paper. No finding in these reports originates from a README, and no README is cited as evidence for any claim.

A report is written before any repair. Repairs are designed against the completed sweep, not against the first finding, so that a fix preserves what the paper actually needs rather than what happens to produce different numbers.

## Standing rules

- **No number changes until the experiment is rerun.** A corrected result is not a reworded one.
- **"I did not find X" is not "X does not exist."** Any reported absence distinguishes *searched and not found* from *not searched*, and records what was searched.
- **A failed run is a result.** A comparison that could not be executed is reported as void, never as a match.
- **A correct implementation elsewhere in the same repository does not rescue the incorrect implementation that produced the published numbers.** Provenance of the number governs.
- **A value need not appear in a paper for a claim about it to be falsifiable.** A claim that a quantity was obtained by some process is checkable against the process, whether or not the quantity is printed.

## What these reports are for

DEFECT-001 established a controlled contrast: two packages, both reproducible, with opposite failure modes. That is an empirical argument for keeping reproduction and correspondence as independent layers rather than one quality score, and it connects directly to the layered method in `../papers/artifact-to-claim-integrity/`.

DEFECT-002 adds a third profile, and it is the one that a reproducibility check cannot see at all: a package that reproduces perfectly, whose paper correctly refuses to interpret its own result, and whose prescribed next experiment does not exist. Nothing about that is detectable by re-running anything.

DEFECT-003 adds a fourth: an artifact that is sound, numbers that are real and correctly traced, and a defect located entirely in the vocabulary attached to them — and disclosed rather than concealed. Across four reports the defect has appeared in the function that computes the number, in the instrument that measures it, in the document that describes it, and in the words that name it. Only one of those four is reachable by re-running the code.

**The sweep's own standing conclusion:** reproducibility is not a scientific verdict. Every package in this corpus reproduces, and the reports locate the defect in six different places: the function that computes the number, the instrument that measures it, the document that describes it, the words that name it, and the decoder that reads it back.

Only the first of those is reachable by re-running the code. A package can be fully reproducible and still have no result worth trusting.

`isac-jasc-ieee` is the sharpest case in the set. Its artifact is the most bit-faithful in the sweep, and its central claim is a validation that cannot in principle fail: the estimation error is drawn from the Cramér-Rao bound it is compared against. Reproducing that package exactly reproduces the circularity exactly. It also conceals a second defect — a variance consumed as a standard deviation — because against a real estimator that confusion would have surfaced as an estimator beating the bound.

**A validation that cannot fail also cannot report the failures it would otherwise expose.**
