# G0 — GitHub Estate Audit Evidence Model

Status: **FROZEN (read-only inventory model)**
Scope: all owned repositories observable to the linked GitHub account.
Purpose: establish an evidence-backed estate inventory before any P1/P2/P3 work is reclassified.

## Identity and state

Each repository record keeps these fields separate:
- **IDENTITY** — name, visibility, default branch, observed directly.
- **STATE** — active / dormant / archived / ambiguous. `pushed_at` and `updated_at` are recorded separately; `pushed_at` is the primary write-activity signal.
- **EVIDENCE** — implementation, tests, CI, artifacts; observed per repository.
- **CLAIMS** — README, paper, metadata; record whether each source was actually read.
- **PROVENANCE** — commits, releases, deployments.
- **RELATION** — canonical / duplicate / family, only when supported by repository evidence. Name similarity alone is insufficient.
- **ACTION** — KEEP / CURATE / ARCHIVE / INVESTIGATE. This is a work-queue action, not a quality score.

## Scope correction

- **Owned total observed:** 534
- **Public:** 222
- **Private:** 312
- **Archived:** 0
- **Forks:** 8

Public GitHub search visibility and account-owned inventory are separate populations. A public search under `FernandoMay` cannot establish the full 534-repository owned estate.

## Activity correction

Current observed bucket counts:

| Age bucket | updated_at | pushed_at |
|---|---:|---:|
| 0–90d | 59 | 55 |
| 91–180d | 471 | 356 |
| 181–270d | 0 | 9 |
| 451–540d | 0 | 15 |
| >630d | 0 | 46 |

This evidence includes **113 repositories with `pushed_at` older than 180 days**, including **46 older than 630 days**, despite `updated_at` placing the observed estate within 180 days.

## Anti-contamination rules

- name similarity ≠ duplicate
- small repo ≠ worthless
- old repo ≠ obsolete
- many commits ≠ maturity
- README quality ≠ implementation quality
- stars ≠ technical validity
- `updated_at` ≠ activity
- high visibility count ≠ public portfolio
- an audit narrative ≠ repository evidence
- **an inherited finding ≠ an inherited mechanism** — a mechanism explanation transfers only if it is independently traceable to the source adjudication

## P1 inheritance rule

Existing P1 adjudications are inherited evidence, not new work items. A repository already adjudicated by the P1 research-hardening process must not be re-audited merely because a generic estate audit raises a superficially similar concern.

Current inherited adjudications:
- **SGN** — near-chance measurements are disclosed; material finding is that 2/4 arms lack verifiable ground truth, not that 0.50/0.51 is inherently anomalous.
- **CRL** — mechanism/access/activation are supported and exposure is equalized; current metric cannot resolve benefit. Claims are appropriately limited where the manuscript does so.
- **QCE** — byte-identical artifact evidence reproduces 0.924/0.912/13.74%; defects are attribution at `:484`, two arms without code paths, and kernel-C divergence (1.0000 vs 0.9237).
- **ISAC** — material defect is the 621× self-discrepancy between the paper's two CRLB equations; synthetic-data labeling is not itself the finding.
- **LEO NSGA-II** — the published latency was a base value transformed by `bl_lat × (0.7 + 0.3·w)` combined with asymmetric 60.0 ms baseline / 55.0 ms non-baseline stand-ins, rather than the arm's own measurement. Separately, the resilience **metric** is decoupled from the mechanism (`M1-control-resilience-decoupled`). `DEFECT-001-LEO.md` §3.7's "genetic load balancer" description is **wrong for this package**: the implementation is `GAWeightedRouter` consuming the NSGA-II prior as a fixed routing mode. *Mechanism traceability corrected 2026-10-01 — see `INHERITED-MECHANISM-DRIFT` below.*
- **LEO extended/ablation** — experimental design and labeling require correction.
- **I01 / LEO edge orchestration** — comparison objectives are not currently matched.

These entries are portfolio evidence with provenance to the P1 process. They are not automatically reopened by G0.

## Unadjudicated candidates

Legitimate concerns not yet adjudicated by P1 must be marked **INVESTIGATE**, not silently converted into P1 findings.
- **XING** — verify headline recovery/cost claims against direct artifacts.
- **SentinelX** — verify whether “AI-powered” claims correspond to an implemented/evaluated model or heuristic/rule system.
- **BioHealy** — verify engineering-vs-medical-device claims, validation boundaries, and safety/clinical language.

## Freeze boundary

G0 freezes the **inventory model and evidence semantics**, not the repositories themselves. No repository code, README, branch, release, deployment, visibility, or archival state is changed by G0.

## Required per-repository record

```text
IDENTITY      name · visibility · default branch [observed]
STATE         active / dormant / archived / ambiguous [pushed_at, updated_at, SEPARATELY]
EVIDENCE      code · tests · CI · artifacts [observed per repo]
CLAIMS        README / paper / metadata [read status explicit]
PROVENANCE    commits · releases · deployments [observed]
RELATION      canonical / duplicate / family [evidence-backed]
ACTION        KEEP / CURATE / ARCHIVE / INVESTIGATE [work queue, not a score]
```

Definition of done for G0: the estate can be reasoned about from observed evidence without collapsing visibility, activity, implementation quality, or prior adjudications into a single narrative score.

---

# G0 instrument finding — inheritance defect

## Class

**INHERITED-MECHANISM-DRIFT**

This is a **G0 instrument defect**, not a P1 defect class. P1 is frozen at `c8c5226`
and its defect vocabulary is not reopened. The defect occurred in the transfer of
knowledge **from** P1 **into** this audit, which is G0's instrument surface.

## Observed

The G0 inheritance layer correctly transferred package-level adjudications for **SGN,
CRL, QCE and ISAC**. Each was cross-checked against the frozen corpus and each matched
its source.

For **LEO**, however, it inherited an explanatory mechanism that the frozen P1 corpus
does not support.

**Incorrect inherited description:**

> objective function is partly decoupled from the network realization because
> evaluation samples random metrics.

**Corpus-supported LEO finding:**

> The published latency was a base value transformed by `bl_lat × (0.7 + 0.3·w)`,
> combined with asymmetric 60.0 ms baseline / 55.0 ms non-baseline stand-ins, rather
> than the arm's own measurement.

**Separately:**

> `M1-control-resilience-decoupled` establishes that the **resilience metric** is
> decoupled from the mechanism. That is a different claim, about a different
> component, established by a different falsifier.

**Also:**

> `DEFECT-001-LEO.md` §3.7 explicitly records that describing the arm as a "genetic
> load balancer" is wrong for this package; the implementation is `GAWeightedRouter`
> consuming the NSGA-II prior as a fixed routing mode.

The G0 entry had conflated a resilience-metric finding with an NSGA-II objective claim,
and had imported a mechanism attribution from the same report lineage that P1
explicitly corrected.

## Disposition

**G0 INSTRUMENT DEFECT — NOT A NEW P1 FINDING**

No P1 artifact is modified by this correction. The corpus at `c8c5226` remains the
authority; this document is the mutable audit artifact, and it was the artifact at
fault.

## Rule added

> **Inheritance may transfer an adjudicated finding only with its corpus-supported
> mechanism. A mechanism explanation must be independently traceable to the source
> adjudication; it must not be reconstructed from secondary audit summaries.**

## Required future behaviour

For every inherited entry, distinguish three things:

| | |
|---|---|
| **WHAT** | was adjudicated |
| **WHY** | it was adjudicated |
| **HOW** | the mechanism was established |

**Do not inherit the second or the third merely because the first is correct.**

## Preservation check

```
Source corpus:  frozen P1 c8c5226   (immutable)
G0 summary:    mutable audit artifact (correctable)

Any inherited mechanism not traceable to the source adjudication
must FAIL the inheritance check.

LEO:
  finding transfer         PASS
  mechanism traceability    FAIL   <- corrected in this commit
  corrected disposition    PASS
```

This check runs against the frozen corpus, never against another audit's summary.
**An audit narrative is itself an artifact with provenance and correspondence**, and it
is not a sufficient source of truth for a second audit — which is the tenth
anti-contamination axis.

## Why this is recorded rather than quietly fixed

The inheritance rule was correct in five of six entries on its first use. A rule that
works five times out of six is not a rule that can be applied to the remaining 528
repositories without the failure being written down. The failure mode is silent
multiplication: one wrong mechanism, carried forward, becomes the mental model of a
defect and then the premise of a repair.

**A finding may be inherited. Its causal explanation may only be inherited if its
traceability to the source record is preserved as well.**
