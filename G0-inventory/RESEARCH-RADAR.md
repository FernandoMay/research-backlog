# G0 — Research Radar

**Status:** live. **No repository was modified.**
**Purpose:** track repositories the owner has explicitly designated as research
targets, with their verification state held layered and visible.

---

## 1. What the radar is and is not

The radar is **not** a queue of results and **not** a positive-evaluation list. It
holds repositories whose *content* is unverified, alongside exactly what *was*
verified about them.

Promotion basis: **owner-declared research target.** That is explicit provenance from
the owner. It is not an inference from name, description, size or activity, and it is
not inherited from a secondary narrative. Name-inference remains barred — that is what
`name similarity ≠ duplicate` and the G0-2 instrument finding are for.

---

## 2. Layered state — per repository

```
EXISTENCE      VERIFIED | NOT FOUND
VISIBILITY     VERIFIED
CONTENT        NOT VERIFIED      <- no repository has been inspected
NUMERIC CLAIMS NOT VERIFIED
EXTERNAL TEXT  SECONDARY_SOURCE
```

### SD-01 · `iscmi-01-fuzzy-conformal`

| layer | state | evidence |
|---|---|---|
| existence | **VERIFIED** | GitHub API, public, last push 2026-09-24 |
| visibility | **VERIFIED** | `public` |
| identity | `NO_CANDIDATE_SURFACED` | unique name; no cluster |
| G0-3 state | `NOT_INSPECTED` | 0/1 content inspections |
| dominant language | TeX | observable — paper-dominant |
| description | *(empty)* | observable |
| content | **NOT VERIFIED** | — |
| numeric claims | **NOT VERIFIED** | Brier 0.0210 · ECE 0.0226 · coverage 93.86% · interval width 0.1759 · `breast_cancer` proxy |
| package readiness | **NOT VERIFIED** | "Package Ready", "congelado" |
| external narrative | **SECONDARY_SOURCE** | `SECONDARY-SOURCE-gemini-conversation.md` @ `df53d43` |

### SD-02 · `incc-2026-semantic-jscc`

| layer | state | evidence |
|---|---|---|
| existence | **VERIFIED** | GitHub API, public, last push 2026-09-24 |
| visibility | **VERIFIED** | `public` |
| identity | `NO_CANDIDATE_SURFACED` | unique name; no cluster |
| G0-3 state | `NOT_INSPECTED` | 0/1 content inspections |
| dominant language | TeX | observable — paper-dominant |
| description | *(empty)* | observable |
| content | **NOT VERIFIED** | — |
| numeric claims | **NOT VERIFIED** | 83.89% at 0 dB · 97.78% at 10 dB · 12.5% payload |
| package readiness | **NOT VERIFIED** | "Package Ready" |
| external narrative | **SECONDARY_SOURCE** | as above |

### SD-03 · `iccit-2026-bci-transformer-swarm`

| layer | state | evidence |
|---|---|---|
| existence | **VERIFIED** | GitHub API, public, last push 2026-09-24 |
| visibility | **VERIFIED** | `public` |
| identity | `NO_CANDIDATE_SURFACED` | unique name; no cluster |
| G0-3 state | `NOT_INSPECTED` | 0/1 content inspections |
| dominant language | Python | observable |
| description | *(empty)* | observable |
| content | **NOT VERIFIED** | — |
| numeric claims | **NOT VERIFIED** | LOSO 32.5% vs 25% chance · 6.52 ms · 1.78 bits/min |
| package readiness | **NOT VERIFIED** | "Pipeline Ready" |
| external narrative | **SECONDARY_SOURCE** | as above |

---

## 3. Promotion changed their G0 bucket, and only that

All three move from the **408 `NO_CANDIDATE_SURFACED`** census group to an explicit
radar designation, on owner declaration.

The census group is unchanged at **408**. A repository does not leave the censored
state because someone named it; it gains a second, explicit label. Both remain true.

This is the distinction the G0-2 instrument finding requires: the census records what
a defective instrument surfaced, and it must not be rewritten when better information
arrives from a different direction.

---

## 4. G0-3 eligibility

| repository | eligible for G0-3? |
|---|---|
| SD-01, SD-02, SD-03 | **yes** — identity is not ambiguous, so no selection problem exists |
| any `AMBIGUOUS` repository | no — blocked until identity resolves |

The three packages carry **no identity ambiguity**, so they can be inspected without
first choosing among candidates. That is the condition G0-2 established and it is
satisfied here.

---

## 5. What inspection would settle, and what it would not

Inspecting them would establish: whether the code runs, whether the artifact
regenerates, whether the reported metrics reproduce, and whether the README's claims
correspond to the implementation.

It would **not** establish that the numbers are correct in an absolute sense, that the
comparison is fair, or that the venue is appropriate. Those are separate questions and
`METRICS_REPRODUCE` is not `CLAIM_CORRESPONDS`.

---

## 6. Boundary

No README, branch, artifact, release or publication has been modified by anything in
this document. The radar is a record. Acting on it is a separate, authorised operation.