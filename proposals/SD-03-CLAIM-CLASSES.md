# SD-03 — Claim Classes and Reporting

**Date**: 2026-10-02 · **Branch**: `publications/2026-board`
**Reproduction verdict**: `REPRODUCED_WITH_ENVIRONMENT_DEPENDENT_FIELDS` (ladder v2, `ab03961`)
**Prior**: `3e4a2ef` (reproduction), `1f8f9c2`-era wave-1 correspondence finding

---

## 1. The three claim classes

`accuracy` is reproducible under the released protocol. `latency_ms` is a measurement in a concrete environment. `itr_bits_min` inherits that dependence because its formula consumes latency.

| Class | Fields | Status |
|---|---|---|
| **Reproducible result** | `accuracy` (per subject), `mean_accuracy` | reproduced exactly |
| **Environment-conditioned measurement** | `latency_ms` (per subject), `mean_latency_ms` | environment-dependent |
| **Derived metric** | `itr_bits_min` (per subject), `mean_itr_bits_min` | derived from an environment-dependent quantity |

## 2. Manuscript language

To be used in the results section. Not a draft to be softened:

> **Accuracy results are reproducible under the released experimental protocol.** Runtime measurements (`latency_ms`) are environment-dependent and therefore are reported together with the execution environment rather than treated as invariant algorithmic results. **ITR is derived from accuracy and measured latency and consequently inherits this environmental dependence.**

The nuance that must survive editing: `latency_ms` and `itr_bits_min` are **not** "non-reproducible" in an absolute sense. They are **reproducible as measurements under a fixed environment and protocol**, but not as constants independent of hardware and software.

## 3. Artifact annotation

Original values are **retained, not substituted**. A second machine producing a different clock is not a correction, and replacing the published numbers would destroy their provenance.

| Field | Committed value | Regenerated value | Class |
|---|---|---|---|
| `accuracy` subj 0–3 | 0.25 / 0.375 / 0.30 / 0.375 | **identical** | reproducible |
| `mean_accuracy` | 0.325 | **identical** | reproducible |
| `latency_ms` subj 0–3 | 6.5196 / 6.4413 / 6.5030 / 6.6045 | 3.2614 / 3.2722 / 3.1763 / 3.1883 | environment-dependent |
| `itr_bits_min` subj 0–3 | 0.0 / 3.2768 / 0.5505 / 3.2762 | 0.0 / 3.2871 / 0.5524 / 3.2874 | derived |
| `mean_latency_ms` | **6.517107290710555** | 3.2245635624875035 | environment-dependent |
| `mean_itr_bits_min` | **1.7758821146395407** | 1.7817153481297185 | derived |

The two bolded published values remain the ones in the manuscript, now annotated with the environment that produced them.

### Environment annotation to accompany them

| | |
|---|---|
| Device | CPU |
| Python | 3.13.13 |
| torch | 2.14.1 |
| numpy | 2.5.3 |
| Platform | macOS, Apple silicon |
| Date | 2026-10-02 |

## 4. Why the ITR difference is fully accounted for

`src/pipeline_loso_itr.py:126` computes

```python
calculate_itr(4, accuracy, 1.0 + latency / 1000)
```

Recomputing ITR from the regenerated accuracy and regenerated latency reproduces every regenerated ITR to within **1e-12**. Nothing diverges about the method; the difference is a faster clock raising bits-per-minute.

This is why ITR is classified `DERIVED_FROM_ENVIRONMENT_DEPENDENT` rather than `ENVIRONMENT_DEPENDENT`: it is not independently measured, and it will move whenever latency moves.

## 5. What is deliberately not done

- **`latency_ms` and `itr_bits_min` are not removed.** Deleting them so the package reads `REPRODUCED` would be manufacturing a clean verdict.
- **The published values are not replaced.** They keep their provenance.
- **The verdict is not upgraded.** `REPRODUCED_WITH_ENVIRONMENT_DEPENDENT_FIELDS` is not `REPRODUCED`, and the submission must say which part of the result regenerated.
- **No claim is made about the proxy being valid.** SD-03 uses a synthetic subject-structured BCI proxy and states in its own `REPRODUCE.md` that it *"is not a human-EEG result"*. That disclosure is correct and is not weakened here.
- The field classification used at `3e4a2ef` was formed **after** its diff was observed and does not satisfy the ladder's pre-registration rule. The ladder applies prospectively.

## 6. Consequence for the submission

The package can state exactly which part of its result was regenerated and which part is conditioned on the machine, without inflating the result and without concealing divergence. That is strictly more informative than the two alternatives it replaces:

| Alternative | Why not |
|---|---|
| publish accuracy only | discards a measurement the paper already reports, without saying why |
| publish everything unexplained | leaves a reviewer to discover that the runtime figures are machine-dependent |
| **separate the claim classes** | states what reproduced, what is conditioned, and why |