# P1 Defects

Defect reports from the P1 research-hardening sweep: audit of research packages against the bar the rest of the estate is held to.

**This is a different corpus from `../audit/`.** The E1 dataset in `../audit/E1-DATASET-v1.0.md` is frozen at v1.0, covers 13 rows, and is not re-adjudicated on the basis of anything in this directory. The rubric's own assignment rule keeps these as separate records.

## Reports

| ID | Packages | Finding class | Status |
|---|---|---|---|
| [001](DEFECT-001-LEO.md) | `leo-routing-itft2026-package`, `i01-leo-edge-orchestration` | U3 correspondence failure; problem-definition, within-document contradiction, temporal provenance | Open, nothing corrected |

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
