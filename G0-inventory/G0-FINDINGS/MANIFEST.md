# G0 Findings Manifest

Ledger of audit artifacts, their freeze state, and their defect classifications. Every commit hash below was verified to exist and to touch the artifact it is paired with.

**Branch**: `audit/g0-estate` from `main` tip `34e63eb`. See `G0-BRANCH-BOUNDARY.md`.

---

## 1. Commit ledger

| Artifact | State | Commit | Verified |
|---|---|---|---|
| P1 | **FROZEN** | `c8c5226` | touches `p1-defects/` |
| G0 estate model | **FROZEN** | `b0a2773` | touches `G0-estate-audit.md` |
| G0-2 identity resolution | CLOSED | `4a75f37` | touches `G0-2-IDENTITY.md` |
| G0-3 wave 1 (3 promoted repos) | CLOSED | `9d61c09` | touches `G0-3-WAVE1-RESEARCH.md` |
| G0-3 wave 2 (121 repos) | CLOSED | `34e63eb` | touches `G0-3-WAVE2-AMBIGUOUS.md` |

`main` is frozen at `34e63eb`. `origin/main` is at `9d61c09`; `34e63eb` was never pushed, so no remote audit history requires unwinding.

## 2. Defect and finding ledger

| Subject | Classification | Record |
|---|---|---|
| `biohealy-ipn` | **DOCUMENTATION FINDING** | `G0-FINDINGS/FINDING-001-biohealy-current-unmeasured.md` |
| Scaffold detector (0 found, actual 16) | **INSTRUMENT DEFECT** | `G0-3-WAVE2-AMBIGUOUS.md` §5 |
| Relation detector (44 → 2) | **INSTRUMENT DEFECT** | `G0-3-WAVE2-AMBIGUOUS.md` §5 |
| `sentinelx/.env` | **FALSE POSITIVE AVOIDED** | `G0-3-WAVE2-AMBIGUOUS.md` §3 |
| `G0-inventory/.gitignore` | **AUDIT INSTRUMENT DEFECT** | `G0-3-WAVE2-AMBIGUOUS.md`, commit `34e63eb` |
| Branch boundary | **G0 PROCESS/INSTRUMENT DEFECT** | `G0-BRANCH-BOUNDARY.md` |

## 3. Standing rules established

**Name similarity and directory-layout similarity may surface candidates. Neither establishes identity or relation. Only content or artifact evidence can.**

This is what makes the 332-pair result interpretable. The ledger must retain the exact criterion, because `2` relations against `288` with no observed overlap must not be restated as "families" — the 21 template pairs and 21 layout-only pairs are the special cases that a bare count would erase.

**Exposure is determined by destination class, not by whether a value is a placeholder.**

Scheme, authority presence, credential semantics, and embedded-secret evidence decide it. A non-placeholder value resolving to a local path is not a credential. No credential value was ever read into output at any point.

**A hand-maintained marker vocabulary can return a confident negative.**

Before trusting a "none found", ask whether the marker list could see the thing at all. The same silence appears in a stale `.gitignore` rule: nothing errors, and the result looks correct.

## 4. Findings index

| ID | Object | Class | Status |
|---|---|---|---|
| G0-FINDING-001 | `FernandoMay/biohealy-ipn` | Documentation / correspondence | FROZEN, no repair proposed |

## 5. Untouched, by standing constraint

- `p1-defects/` — frozen at `c8c5226`
- `G0-estate-audit.md` — frozen at `b0a2773`
- G0-1 snapshot and its recorded digest — immutable historical evidence
- The 534 audited repositories — read-only via API, never cloned, never modified