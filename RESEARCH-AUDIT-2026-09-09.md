# Research Package Audit

## Author Metadata

- **Author:** Fernando May Fuentes
- **Affiliation:** Instituto Politecnico Nacional
- **Email:** fmayf1500@alumno.ipn.mx
- **ORCID:** https://orcid.org/0009-0002-3953-5224

## Scope

Six conference packages were reviewed against the implementation, test suite, compiled manuscript, and the reference package conventions in `amso-ieee-package` and `h266-drl-iccpr2026-package`.

## Corrections Applied

- Replaced stale or unsupported numerical claims with values from seeded executions.
- Added seed `20260909` to executable entry points.
- Removed ground-truth covert labels from the I-02 detector feature vector.
- Corrected I-02 terminology from an unsupported full diffusion claim to an explicit reconstruction-based baseline.
- Added experimental protocols, limitations, threats to validity, and reproducibility notes.
- Added ORCID metadata to every manuscript and `CITATION.cff` to every package.
- Added compiled PDFs after the revision.
- Documented negative and inconclusive results instead of presenting them as advantages.

## Verification

| Package | Tests | PDF |
|---|---:|---|
| I-01 LEO orchestration | 19 passed | compiled |
| I-02 covert detection | 21 passed | compiled |
| S-01 CRL | 15 passed | compiled |
| S-02 semantic THz | 8 passed | compiled |
| V-01 quantum-inspired routing | 8 passed | compiled |
| R-01 covert sub-THz | 8 passed | compiled |

## Interpretation Rule

The current papers are reproducible simulation baselines, not validated field experiments. Claims involving hardware, operational 6G deployment, quantum advantage, real LEO performance, or security guarantees remain future work until supported by calibrated data and controlled baselines.
