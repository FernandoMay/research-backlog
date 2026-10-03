# V — Architectural Closure and Open Fork

**Date**: 2026-10-02 · **Branch**: `publications/2026-board`
**Evidence**: `098bdf8` (the specification that produced the finding)
**Predecessors unmodified**: `84a5fd1` · `a1c2f66` · `19f4e8e`

---

## 1. What is closed

> **D1b cannot be extended to `V` as an independent pre-authorisation authority under the current semantics.**

This is a valid architectural result, produced by the enumeration in `098bdf8` §3: no observable is simultaneously agent-independent, available before authorisation, and equal to the committed value. The committed value is observable only as a post-action ledger delta; everything available pre-action is a bound or a threshold.

That closure is about **extensibility of the D1b method to `V`**. It is not a finding that `V` is unprotectable, and not a recommendation about what to do next.

## 2. What is not closed

**Whether `V` should keep its meaning or be redefined.** The evidence cannot decide that. It is a normative question about what the policy is *for*, not an empirical one, and no experiment adjudicates it.

No selection is made here, and neither option is labelled correct.

## 3. The fork

```text
                                  V
                                  │
                  ┌───────────────┴───────────────┐
                  │                               │
        committed value                       bound
                  │                               │
        preserves the semantics              changes what V is
        recovered at 3ea1927                and therefore the policy
                  │                               │
      post-action role only              pre-authorisation gate
      audit and adjudication             possible
```

### Option 1 — preserve `V` as the committed value

- The independent source exists and is authoritative: the ledger delta.
- It is available **only after** the action.
- `V` therefore **cannot** be an independent pre-authorisation gate in the current scope. That becomes an **explicit architectural limitation**, not a solved problem.
- The controls `V−`, `V+`, `VΔ`, `Vid` keep their value but **change function**: they would demonstrate that the post-hoc measurement corresponds to the real action and cannot be falsified by agent declaration. They would **not** demonstrate that `V` gates a pre-authorisation decision.
- Consequent next work: design, explicitly and on its own terms, **what the pre-authorisation decision uses instead of `V`** — and without pretending that substitute is `V`.

### Option 2 — redefine `V` as a bound

```text
balance / policy limit / tool maximum
        ↓
      V_bound
        ↓
  authorisation
```

- An independent pre-authorisation authority becomes available.
- But this changes **"V = committed value"** into **"V = independently authorised maximum"**. That alters the policy's semantics.
- Under the standard applied at `41fdc4b`, a change to a normative element is a **redesign of SD-05**, not a repair of `V`'s authority. It requires its own specification and its own controls, and must not be adjudicated as a `D1b` repair.

## 4. Why the choice is not made here

`098bdf8` produced a finding about what is *possible* under each design. It cannot produce a judgment about which design is *intended*, and the recovered source is a **non-primary transcription** that explicitly does not establish design intent with certainty.

Selecting one would convert an evidentiary result into a normative decision without evidence for it — the same inversion that `41fdc4b` was careful to avoid when it framed C as *selected by a stated criterion*, not as *the correct repair*.

## 5. What remains exactly where it was

- **`N` and `P`** — agent-influenced, **not exercised** by any run so far. They are surfaces, not grounds to extend this conclusion beyond `V`.
- **`I`** — unmodified. The `84a5fd1` adjudication stands: derived `I` removed one counterexample and three persist.
- **`19f4e8e`** — untouched, not re-run, not reinterpreted by any result above.
- **`k`, thresholds, `V`'s scale, case composition** — unmodified throughout.

## 6. What is deliberately absent

No implementation, no controls, no threshold change, and no recommendation. The specification at `098bdf8` already contains everything the evidence supports; what it does not contain is a choice, and that choice is not the auditor's to make.