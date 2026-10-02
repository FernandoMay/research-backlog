# G0-1 — Inventory Snapshot (metadata-only first pass)

**Status:** first pass complete. **No repository was modified.**
**Scope:** all 534 owned repositories. Metadata only. **No content was inspected.**

---

## 1. Provenance

| | |
|---|---|
| Source of truth | GitHub REST API, owner affiliation, all visibilities |
| Endpoint | `/user/repos?affiliation=owner&visibility=all&per_page=100&sort=full_name` |
| Retrieval | `gh api --paginate --slurp` |
| Extracted at (UTC) | `2026-10-02T15:43:07+00:00` |
| Raw response | `raw/g0-repos-raw.json` — 2 857 536 bytes |
| Raw sha256 | `8c882a4eae288072f59a3a2fb82f27303245735d14188ddde0685667b99c697a` |
| Normalized snapshot | `snapshot.json` |

The raw response is retained so the hash is **evidence** rather than an assertion, and
so the normalization can be re-derived and compared.

---

## 2. Verification — set-wise, not a count

Per `A4b`: a count proves something happened; a set comparison proves nothing was left
behind.

| check | result |
|---|---|
| records | **534** |
| distinct names | **534** |
| duplicate names in the response | **0** |
| records with a non-empty `INSPECTED` layer | **0** — required for this pass |
| `STATUS` values present | `NOT_INSPECTED: 534` |
| fields absent from the API response | `network_count` absent from **all 534** |

`network_count` is recorded as an **API absence**, not a normalization failure. It is
present in the schema and simply not returned for this endpoint.

---

## 3. Rules carried into the record

```
Absence of inspection  ≠ absence of evidence
Metadata               cannot produce a content claim
INSPECTED              empty by construction in this pass; not omitted
pushed_at              ≠ activity
updated_at             ≠ activity
repository count       ≠ public portfolio count
```

Observed consequences:

```
534 owned  =  222 public + 312 private        a public search sees at most 222
updated_at:  59 in 0–90d, 471 in 91–180d, ZERO older
pushed_at:   55 / 356 / 9 / 14 / 23 / 15 / 6 / 46   (113 older than 180d, 46 older than 630d)
```

Reading `updated_at` alone would conclude that all 534 are active. It would never
surface the 46 genuinely dormant by write activity.

---

## 4. Record schema

```json
{
  "OBSERVED":     { 22 metadata fields, as returned },
  "INSPECTED":    {},                       // empty in this pass
  "STATUS":       "NOT_INSPECTED",
  "INHERITED_P1": null                      // filled only with traceability
}
```

---

## 5. Finding — the P1 inheritance layer is grounded for all seven

Resolved by **exact identifier match** against the known upstream repository name.
Exact match is traceability; substring similarity is the inference the G0 rules
forbid. These are different operations and only one was used here.

| package | repository | present | visibility |
|---|---|---|---|
| LEO | `leo-routing-itft2026-package` | yes | private |
| ISAC | `isac-jasc-ieee` | yes | public |
| CRL | `s01-crl-metacognitive` | yes | public |
| QUANTUM | `quantum-k-sat-ieee-package` | yes | private |
| i01 | `i01-leo-edge-orchestration` | yes | public |
| QCE | `qce-ieee-package` | yes | private |
| SGN | `sgn-ieee-package` | yes | public |

**7 of 7.** Each carries `INHERITED_P1` as a citation, not as pending work. None of
these seven enters content re-inspection.

Four of the seven are **private** — they are invisible to any external reader of the
estate, which matters when the question is portfolio coherence rather than estate
hygiene.

---

## 6. Finding — `XING` is not yet a well-defined inspection target

`G0-estate-audit.md` lists **XING** as an `INVESTIGATE` candidate for content
inspection. Four repositories in the estate have `xing` in the name:

| repository | visibility | created | pushed | size (KB) | description |
|---|---|---|---|---|---|
| `xing` | private | 2026-06-13 | 2026-06-13 | 38 | yes |
| `xing-iccia2026` | public | 2026-06-13 | 2026-07-12 | 924 | yes |
| `xing-core` | public | 2026-07-13 | 2026-07-13 | 33 | no |
| `xing-adan-resilience` | public | 2026-09-10 | 2026-09-10 | 115 | no |

**No metadata field says which one the audit meant.** Three are public and one is
private. Resolving it by name similarity — picking the largest, or the newest, or the
one whose description looks most like the paper — is precisely what
`name similarity ≠ duplicate` and `RELATION: evidence-backed` forbid.

`xing-iccia2026` is the most plausible candidate on observable grounds (it is the only
public one with both a description and a size consistent with a paper package), but
"most plausible" is not a selection predicate, and adopting one silently would repeat
the `INHERITED-MECHANISM-DRIFT` failure mode at the target-selection step.

**Consequence:** `XING` stays `INVESTIGATE` but is **not yet a target**. It needs an
explicit selection criterion, stated before inspection, not one chosen during it.

---

## 7. Measured yields for the level-2 selection predicate

Computed, not estimated. No predicate has been adopted.

| candidate predicate | yield | share of the 222 public |
|---|---:|---:|
| A — all public | 222 | 100.0% |
| B — public **and** has description | 183 | 82.4% |
| C — public **and** has homepage | 3 | 1.4% |
| D — public **and** (description or homepage) | 185 | 83.3% |
| E — public **and** stars > 0 | 8 | 3.6% |
| F — any visibility, has description | 484 | — |
| G — any visibility, has homepage | 9 | — |
| H — all 534 | 534 | — |

**B and D are barely filters.** At 82–83% they exclude 37–39 of 222 repositories, so
adopting them would create the appearance of selection while doing almost nothing.

The selective predicates (C, E, G) are selective on metadata that the G0 rules
explicitly disqualify as evidence of anything: a homepage is not a claim, and a star is
not technical validity. A predicate built on them would be precise and meaningless.

The only defensible predicates today are **A** (inspect all public) and **H** (inspect
everything), and the difference between them is 312 private repositories.

---

## 8. What this pass does not establish

- No content claim is verified, refuted or even read.
- No repository is classified as canonical, duplicate, or family member. `RELATION` is
  untouched except for the seven exact-identifier P1 citations.
- No `ACTION` is assigned. `KEEP / CURATE / ARCHIVE / INVESTIGATE` remains a work queue
  and is empty.
- No judgment of quality, maturity, or value is implied by any field above. Size,
  language, topics, license and stars are recorded so a later classification can be
  *checked* against observables — not because they are evidence of anything.

**Nothing in this document is a claim about a repository's content.**