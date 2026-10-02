# G0 Frontier — Invariant, Verification, and Status

**Date**: 2026-10-02, branch `audit/g0-estate`
**Purpose**: make the three audit frontiers a machine-checkable property rather than prose, and hold the one silent failure mode that prose cannot catch.
**Check**: `python3 G0-inventory/check-frontier.py` — read-only, exit 0 intact / 1 violated.

---

## 1. The three frontiers

| Frontier | Ref | Commit | State |
|---|---|---|---|
| **P1** | `c8c5226` | — | **FROZEN**, historical corpus, not touched by G0 |
| **G0 historical, in `main`** | `origin/main` | `9d61c09` | **FROZEN** — deliberately held here |
| **G0 future** | `audit/g0-estate` | `0c16218` | **isolated**, published and remotely verified |

`local main` is `34e63eb`: one commit ahead of `origin/main`. This is a **deliberately unpublishable state**, not technical debt. It is not awaiting a push.

## 2. The operational property

The risk is specific and silent:

> Local `main` is one commit ahead of `origin/main`. Someone running `git push origin main` "to catch up" publishes G0-3 wave 2 to the default branch, collapses the boundary, and gets a clean exit status and no error.

Documentation does not stop that. A paragraph in a record cannot be enforced by anything. So the property is enforced by `check-frontier.py`, which reads **observed ref state** and fails loudly when `origin/main` moves.

This is why the checker inspects `git ls-remote` output rather than whether commands succeeded. **A push reports; refs prove.**

## 3. Verification evidence

A checker that passes on the healthy state and has never been observed to fail is an untested instrument. Both directions were exercised.

### 3.1 Positive — current state

```
ok    origin/main 9d61c09 unchanged (public frontier)
ok    local main 34e63eb frozen ahead of origin — NOT awaiting a push
ok    audit/g0-estate 0c16218 verified on remote (ls-remote)
ok    frozen content intact: 2 trees byte-identical to their pins
All three frontiers intact.                                                exit 0
```

### 3.2 Negative — three failure modes, all detected

Each simulated with a `git` shim on `PATH`. **The real remote was not modified by any of them**, confirmed by re-reading `ls-remote` afterwards.

| Injected condition | Detected | Exit |
|---|---|---|
| `origin/main` advanced to `deadbee…` | `VIOLATION origin/main MOVED … STOP and inspect before any further action.` | 1 |
| `origin/audit/g0-estate` absent | `VIOLATION … the isolated audit trail has no remote representation` | 1 |
| `p1-defects` tree altered | `VIOLATION FROZEN PATH MODIFIED: p1-defects is 0000000, expected ce68524 from c8c5226` | 1 |

Frozen content is checked as **tree identity**, not commit identity: `p1-defects` is `ce6852428edf6397b70bf762ff6b432dec85ba85` and `G0-estate-audit.md` is `24477a2bcccbe4d535b6e9fc8930d1f5b293091a`. Comparing trees means a commit that touched a frozen path is caught regardless of which commit carried it.

### 3.3 Branch protection is deliberately not applied

GitHub branch protection on `main` is **not** enabled. It is an infrastructure decision that should be made once and verified to actually reject a direct push — not toggled in reaction to an observation. Enabling it without testing that it rejects is the same class of error as trusting a checkbox.

Until that decision is made, `check-frontier.py` is the compensating control. If it is ever decided upon, the enablement must be followed by a verified rejection test and that result recorded here as configuration evidence.

## 4. Status summary

Stated to keep P1 and G0 as separate records. P1 is the historical record; G0 is the estate audit.

```text
P1                        frozen historical corpus; package adjudications preserved.
G0 inspection             121/534 repositories inspected through current waves.
G0 reproducibility        not yet established (METRICS_REPRODUCE undecided).
G0 identity resolution    partial.
G0                        OPEN.
```

### 4.1 A conflation that was corrected

An earlier status line in conversation read *"P1 has 0 of 13 packages surviving whole."* That was wrong in three separate ways, and all three are recorded here rather than quietly dropped:

1. **`0/13` is an E1 figure, not a P1 figure.** It belongs to the E1 dataset (`audit/E1-DATASET-v1.0.md`, `audit/E1-AGGREGATE.md`) — gradient `13/13 → 10/13 → 1/13 → 0/13`, where the final label is *"package survives whole"*.
2. **P1 adjudicated 7 packages, not 13.** `P1-CLOSING-SYNTHESIS.md:3` states *"COMPLETE — 7 packages adjudicated, 0 open items"*, and the corpus holds exactly 7 distinct adjudications.
3. **"Adjudicated" is not "survived."** P1's status is a statement of adjudication coverage. Its per-package verdicts are largely negative, but coverage and outcome are different claims and were merged.

The repository already carried the guardrail against this: `p1-defects/README.md:5` states the E1 dataset *"is a different corpus from `../audit/`… and is not re-adjudicated on the basis of anything in this directory."* The warning existed in writing and was still crossed.

The generic lesson, now permanent: **a figure carries its corpus, its label, and its claim type. Moving any one of them into a different corpus silently changes what is being asserted.** An E1 survival count used as a P1 outcome and a G0 completion indicator is a number that has lost all three.

## 5. Standing constraints

- `p1-defects/` frozen at `c8c5226`; `G0-estate-audit.md` frozen at `b0a2773`. Neither is touched by G0.
- `origin/main` does not advance without a separate, explicit decision.
- `main` is not deleted, reset, or rewritten.
- G0 never modifies the repositories it audits; inspection is read-only via API.