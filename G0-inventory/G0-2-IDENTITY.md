# G0-2 — Identity Resolution

**Status:** complete. **No repository was modified. No content was inspected.**
**Builds on:** G0-1 metadata snapshot (`G0-inventory/snapshot.json`).

---

## 1. The rule this phase exists to enforce

> **Before inheriting an adjudication, the identity of the object it applies to must
> be resolved first.**

And its corollary, which is the one that does the work:

> **Content inspection may discover which repository is the package. It must not be
> used retrospectively to convert an ambiguous selection into a selection that was
> always correct.**

That is the `INHERITED-MECHANISM-DRIFT` failure mode one step earlier: there, a wrong
explanation was inherited; here, a wrong *target* would be locked in by inspecting the
thing that was guessed.

---

## 2. Two-state record

```text
IDENTITY
  RESOLVED_EXACT          exact identifier match against a known upstream name
  AMBIGUOUS               >1 family candidate surfaced
  NO_CANDIDATE_SURFACED   no candidate surfaced — NOT a uniqueness claim

INSPECTION
  NOT_INSPECTED
  INSPECTED
```

---

## 3. Ledger

| state | count |
|---|---:|
| `RESOLVED_EXACT` | **7** |
| `AMBIGUOUS` | **119** |
| `NO_CANDIDATE_SURFACED` | **408** |
| total | **534** |

`NO_CANDIDATE_SURFACED` is named that way on purpose. Calling it `SINGLETON` or
`UNIQUE` would assert something the instrument cannot establish.

---

## 4. P1 inheritance — 7 of 7 resolved, cluster ambiguity does not block them

| package | repository | in a name cluster? | reinspection |
|---|---|---|---|
| LEO | `leo-routing-itft2026-package` | no | not required |
| ISAC | `isac-jasc-ieee` | no | not required |
| CRL | `s01-crl-metacognitive` | no | not required |
| QUANTUM | `quantum-k-sat-ieee-package` | **yes** | not required |
| i01 | `i01-leo-edge-orchestration` | no | not required |
| QCE | `qce-ieee-package` | **yes** | not required |
| SGN | `sgn-ieee-package` | no | not required |

**QUANTUM and QCE sit inside name clusters** (`q…` and `q…` respectively, alongside
unrelated repositories) and it does not matter: exact identifier match is a stronger
signal than any name-cluster inference, and it is the one the G0 rules permit.

All seven enter as **citations**. None enters content re-inspection.

---

## 5. The `XING` target is AMBIGUOUS — inspection BLOCKED

| repository | visibility | in the candidate set |
|---|---|---|
| `xin` | — | yes (spuriously) |
| `xing` | private | yes |
| `xing-adan-resilience` | public | yes |
| `xing-core` | public | yes |
| `xing-iccia2026` | public | yes |

`xing-iccia2026` is the most plausible on observable grounds. **It is still not
selected**, because plausibility is not a predicate and choosing it before inspection
is exactly the step this phase exists to prevent.

`SentinelX` and `BioHealy` surfaced no candidates and are eligible for level 3.

---

## 6. Defects of the name-cluster instrument — both directions

This instrument produced two wrong answers before it produced a usable one, and both
are recorded rather than tuned away.

**False negative.** The first rule (normalized-name prefix, length 6) returned
`SINGLETON` for `xing` — because `xing` is **three characters long** and the rule
required six, so the four `xing*` repositories landed in four different buckets. The
single most ambiguous target in the estate came out **resolved**, which is the most
dangerous failure mode an instrument can have.

**False positive.** The replacement extension rule merged `xin` into the `xing` cluster,
because `'xing'.startswith('xin')` is true.

**Therefore:** name clustering **cannot resolve identity**. It surfaces candidates,
with a known error rate in both directions. Every surfaced member is `AMBIGUOUS` by
construction, and no completeness claim is made — a repository sharing no prefix or
token with its family would not appear at all.

Candidate set: 34 clusters, 121 repositories (**22.7%**). Persisted at
`raw/cluster-candidates.json`.

---

## 7. Clusters surfaced, largest first

| n | members |
|---:|---|
| 19 | `mirai`, `mirai-career-pathfinder-ai`, `miraiapp`, `miraid`, `miragaming`, `mirailand`, … |
| 10 | `workspace-*` (UUID-named) |
| 9 | `q`, `qbook`, `qce-ieee-package`, `qgmt`, `qpos`, `qtp-ieee-package`, … |
| 7 | `go`, `goecommerce`, `goempleados`, `goginbooks`, `gotcp`, `gotennisson`, … |
| 6 | `savia`, `savia-flutter`, `savia-stellar-*`, `saviaapp`, `saviapp` |
| 5 | `xin`, `xing`, `xing-adan-resilience`, `xing-core`, `xing-iccia2026` |
| 4 | `dsl`, `dsl-bank`, `dslpos`, `dsltech` |
| 4 | `nexus`, `nexus-path`, `nexus-research-nexus`, `nexuspay` |
| 4 | `vibraniom`, `vibraniom-soundscape-studio`, `vibraniomapp`, `vibraniomx` |
| 3 | `RescueMe`, `rescue`, `rescueM` · `empleados`, `empleadosapi`, `empleadosapp` · `travel`, `travelai`, `travelmate` |
| 2 | 20 further pairs incl. `aegis`/`aegis-otc`, `breadline-protocol`/`breadline_flutter` |

**Note on `q` and `go`.** Both clusters are dominated by short names that prefix-match
many unrelated repositories. They are the clearest evidence that the extension rule
over-merges, and they should not be read as families.

---

## 8. What this phase does not establish

- No repository is classified as canonical, duplicate or family member. A cluster is a
  **candidate set**, not a family.
- No `ACTION` is assigned.
- No content claim is verified, refuted or read.
- No `AMBIGUOUS` repository has been resolved, including `xing-iccia2026`.

**Level 3 cannot begin for any target whose identity is `AMBIGUOUS`.**