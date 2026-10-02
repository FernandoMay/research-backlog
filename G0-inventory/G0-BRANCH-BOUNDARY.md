# G0 Branch Boundary — Defect Record and Transition

**Type**: G0 process/instrument defect. Not a P1 defect class.
**Recorded**: 2026-10-02, on `audit/g0-estate`, which is the first commit after the boundary was established.
**Standing rule**: branch destination is a gate property, recorded before the first commit.

---

## 1. The defect

> **G0 branch-boundary defect:** G0-0 through G0-3 wave 2 were committed directly to `main`. No product repositories were modified, but the audit instrument itself was not branch-isolated. Starting with the next G0 commit, audit work is isolated on a dedicated branch. Historical commits are preserved unchanged.

## 2. Why it was not repaired retrospectively

The purpose of the branch rule was never to police where commits live. It was to prevent **audit state being conflated with product state**, so that a reader of any single branch could tell which is which.

That conflation already occurred: commits `16c6aca → 4a75f37 → 9d61c09 → 34e63eb` sit directly on `main`. That is a historical fact.

Moving them retrospectively would have produced a **second history** and made traceability strictly worse — the exact outcome the rule exists to prevent. A repaired past here is a less auditable past.

So the deviation is **recorded as a defect** rather than erased. The defect is the finding; the fix is forward-only.

## 3. The boundary

```
historical G0 work, unchanged:
    main:  ... → 16c6aca → 4a75f37 → 9d61c09 → 34e63eb   [FROZEN, no rewrite]

from this commit forward:
    audit/g0-estate: 34e63eb → <new G0 work>            [isolated]
```

`audit/g0-estate` was created **from `main`'s tip at `34e63eb`**. It is not a rebase, a cherry-pick, or a graft. There is one history; `main` simply stops receiving audit commits.

## 4. Push state — verified by observed remote state

The branch was published. Verification is by **`git ls-remote`**, not by the exit status or message of `git push`. A push that reports success while changing nothing is a known failure mode, and its report is not evidence.

`git ls-remote origin refs/heads/audit/g0-estate` returned:

```
9c0511d2c00f639ad5c193aaba7a7e93382f1358	refs/heads/audit/g0-estate
```

### 4.1 Observed remote state, before and after

| Ref | Before | After | Result |
|---|---|---|---|
| `origin/audit/g0-estate` | *(absent)* | `9c0511d` | created |
| `origin/main` | `9d61c09` | `9d61c09` | **unchanged** |

`origin/main` was captured **before** the push as well as after, so "unchanged" is a comparison between two observations rather than an assertion.

### 4.2 State verification

| Check | Result |
|---|---|
| `origin/audit/g0-estate` == local `HEAD` (`9c0511d`) | **equal** |
| `origin/main` == pre-push value (`9d61c09`) | **equal** |
| The three boundary/finding records exist in the remote commit | **confirmed** |
| `p1-defects/` file count in `origin/main` vs `origin/audit/g0-estate` | **91 vs 91**, identical |

### 4.3 Resulting provenance

```
origin/main                 9d61c09   [frozen; wave 1, untouched]
        │
        └── audit/g0-estate 9c0511d   [boundary + three frozen records]

local main                  34e63eb   [frozen; wave 2, never pushed]
local audit/g0-estate       9c0511d
```

`origin/main` carries the audit trail through G0-3 wave 1 and stops there. `origin/audit/g0-estate` carries the isolated trail from wave 2 onward. The two are now separately addressable, which is the property the branch rule existed to create.

### 4.4 What publication does and does not mean

Publishing the branch establishes that **the isolated audit trail has a verifiable remote representation**. It does not mean G0 is complete, and `9c0511d` is not a release. Wave 2 closed 121 repositories; the estate is 534; `METRICS_REPRODUCE` remains undecided.

Local `main` remains at `34e63eb`, one commit ahead of `origin/main`. That commit is frozen and unpushed by design — it is not awaiting a push, and it should not be pushed without a separate decision.

## 5. Standing constraints, unchanged

- `p1-defects/` remains frozen at `c8c5226` and is not touched by G0.
- `G0-estate-audit.md` remains frozen at `b0a2773` and is not touched by G0.
- The G0-1 snapshot and its recorded digest remain immutable historical evidence.
- `main` is not deleted, reset, or rewritten for the duration of G0.
- G0 never modifies the repositories it audits. Inspection is read-only by API.