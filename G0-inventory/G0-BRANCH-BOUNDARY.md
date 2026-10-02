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

## 4. Push state at the time of recording

| Ref | Commit |
|---|---|
| `origin/main` | `9d61c09` |
| `main` (local) | `34e63eb` |
| `audit/g0-estate` | `34e63eb` |

**`34e63eb` was never pushed.** The published remote history ends at `9d61c09` (G0-3 wave 1). No audit commit was ever published to `origin/main` beyond that point, so no remote history requires unwinding and no force-push is possible or needed.

## 5. Standing constraints, unchanged

- `p1-defects/` remains frozen at `c8c5226` and is not touched by G0.
- `G0-estate-audit.md` remains frozen at `b0a2773` and is not touched by G0.
- The G0-1 snapshot and its recorded digest remain immutable historical evidence.
- `main` is not deleted, reset, or rewritten for the duration of G0.
- G0 never modifies the repositories it audits. Inspection is read-only by API.