# SECONDARY_SOURCE — Gemini research conversation

**Category:** `SECONDARY_SOURCE`. **Not evidence. Not inherited.**
**Added:** 2026-10-02 · requested by the owner · source could not be fetched
programmatically (`share.gemini.google` requires authentication); content supplied
as pasted text.

---

## 1. Why this document exists and what it is not

This is an external AI assistant's conversation about conference research plans and
three research packages. It is archived so the material is on the record.

It is **not** an audit artifact. It is a secondary narrative, and P1's
`INHERITED-MECHANISM-DRIFT` finding is precisely what happens when a secondary
narrative is treated as a source of explanation:

> Inheritance may transfer an adjudicated finding only with its corpus-supported
> mechanism. A mechanism explanation must be independently traceable to the source
> adjudication; it must not be reconstructed from secondary audit summaries.

**No claim below has been verified.** Each is recorded with its verification status
explicitly `UNVERIFIED`. Any future use requires the same traceability treatment as
the P1 corpus.

---

## 2. What WAS independently verified

The three repositories the conversation names **do exist** and are public:

| repository | exists | visibility | last push |
|---|---|---|---|
| `iscmi-01-fuzzy-conformal` | yes | public | 2026-09-24 |
| `incc-2026-semantic-jscc` | yes | public | 2026-09-24 |
| `iccit-2026-bci-transformer-swarm` | yes | public | 2026-09-24 |

That the artifacts are real does **not** validate any claim about their contents.

---

## 3. Claim inventory — all UNVERIFIED

### SD-01 → `iscmi-01-fuzzy-conformal` (ISCMI 2026)
| claim | value | status |
|---|---|---|
| method | Fuzzy-Calibrated Conformal Prediction | UNVERIFIED |
| Brier score | 0.0210 | UNVERIFIED |
| Expected Calibration Error | 0.0226 | UNVERIFIED |
| fuzzy coverage | 93.86% | UNVERIFIED |
| interval width | 0.1759 | UNVERIFIED |
| dataset | `breast_cancer` as a methodological proxy | UNVERIFIED |
| repository contents | `CITATION.cff`, `REPRODUCE.md`, `Dockerfile` | UNVERIFIED |

### SD-02 → `incc-2026-semantic-jscc` (INCC 2026)
| claim | value | status |
|---|---|---|
| method | Semantic-Aware JSCC over Rayleigh fading | UNVERIFIED |
| accuracy at 0 dB | 83.89% | UNVERIFIED |
| accuracy at 10 dB | 97.78% | UNVERIFIED |
| payload transmitted | 12.5% of data | UNVERIFIED |

### SD-03 → `iccit-2026-bci-transformer-swarm` (ICCIT 2026)
| claim | value | status |
|---|---|---|
| method | Spatial-Temporal Transformer Swarms | UNVERIFIED |
| LOSO accuracy, 4 classes | 32.5% | UNVERIFIED |
| chance baseline | 25% | UNVERIFIED |
| inference latency | 6.52 ms | UNVERIFIED |
| ITR | 1.78 bits/min | UNVERIFIED |
| current dataset | synthetic proxy | UNVERIFIED |
| validation split | Leave-One-Subject-Out | UNVERIFIED |
| next dataset | PhysioNet / BCI Competition IV 2a | not started |

### Portfolio status claims
| claim | status |
|---|---|
| SD-01 "Package Ready", "congelado para submission" | UNVERIFIED |
| SD-02 "Package Ready" | UNVERIFIED |
| SD-03 "Pipeline Ready" | UNVERIFIED |
| "primera fase de construcción 100% completada" | UNVERIFIED |

### Behavioural claims about reviewers and venues
The conversation asserts, with no supporting evidence, that IEEE and INCC reviewers
"valoran infinitamente más" transparency over numerical inflation, and that a given
methodology is "inexpugnable". These are claims about third parties with no cited
evidence. **UNVERIFIED and unsupportable from within this repository.**

---

## 4. Internal contradictions found in the source

Recorded because a source that contradicts itself cannot be inherited even loosely.

1. **AIBT 2026 is simultaneously rejected and recommended.** The conversation contains a
   detailed assessment calling AIBT a mass-mailing call for papers from a predatory or
   vanity venue, advising not to click links or reply. Later in the same conversation
   it states the research question "encaja perfectamente con las exigencias
   metodológicas y los temas prioritarios de AIBT 2026" and maps a full methodology onto
   it. Both positions cannot be held.

2. **Venue quality is asserted in both directions.** ISCMI / INCC / ICCIT are described
   as venues where rigor is valued, in the same conversation that treats AIBT as spam,
   without distinguishing them on any stated criterion.

3. **A large block of the conversation is repeated verbatim**, including the entire
   SD-03 section. The repetition is not an error that changes a claim, but it is a
   quality signal for a source being treated as a reference.

---

## 5. What this conversation is plausibly good for

Stated so the archive is not read as uniformly dismissive.

- It names three real, public repositories and a plausible next dataset.
- Its methodological warnings about BCI evaluation — random splits and k-fold
  mixing epochs of the same subject across train and test inflate results through
  intra-subject correlation — are **substantively correct as general practice**, and
  match what P1 found independently in six other packages about population design.
- It flags the honest-reporting pattern (reporting the real trade-off rather than the
  flattering number) as the differentiator. That matches the P1 evidence, where CRL's
  and i01's most accurate sections were precisely the self-limiting ones.

Those are **general methodological positions**, not claims about this estate, and they
are checkable against P1's corpus rather than against this document.

---

## 6. Handling rule

```
This document may be CITED as a secondary source.
It may NOT be inherited as evidence.
It may NOT be used to establish any claim about a repository.
A claim from it enters the record only with its own independent verification.
```

Recorded in the G0 evidence model as the eleventh axis:

> **a secondary narrative is not evidence** — and is not evidence *about* the
> conversation's own subject either.