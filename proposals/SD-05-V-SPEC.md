# V Specification — Authority and Provenance of Value

**Status**: specification only. No implementation chosen. D1b adjudication stands at `84a5fd1`.
**Branch**: `publications/2026-board`
**Predecessor discipline**: the same sequence that governed `I` — semantics, then controls, then implementation, then cross.

---

## 1. Semantics — what `V` is, and what it must not be

| | `I` | `V` |
|---|---|---|
| Question answered | **what kind** of external change | **how much** is at stake |
| Source of truth in the recovered text | *"Severidad del impacto (0 = read-only; 1 = mutación o DB / transferencia de activos)"* | *"Escalar normalizado del valor monetario/recursos comprometidos en la acción"* |
| Natural authority | tool effect class, static, system-assigned | **none for the value itself** — see §3 |

**Constraint.** The `I` repair must not reappear indirectly inside `V`. If `V` is defined so that recovering it re-derives impact — for example by making `V` a function of the tool class — then the two variables are not independent and the cross loses its second dimension. `V` must carry magnitude only.

## 2. Authority analysis — the `I` rule applied unchanged

For any candidate implementation:

| Question | Required answer |
|---|---|
| Who can write the datum? | a component outside the agent's surface |
| Who can modify it? | no one reachable from the agent |
| What observable is it derived from? | named, and agent-independent |
| Is there an authority independent of the agent? | yes, or the derivation is `DECLARED` |

> **A derivation whose inputs the agent can manufacture remains `DECLARED`, however many intermediate operations it performs.**

This is the rule that governed `I` and it is not relaxed for `V`. Arithmetic performed on an agent-authored amount produces a **more confidently wrong** number, not a derived one.

## 3. Finding — `V` has no independent pre-authorisation observable

This is an **architecture finding**, surfaced during specification, not an invitation to invent an authority source.

| Observable | Authority | Available | Is it the value? |
|---|---|---|---|
| account balance | independent | **pre** | a ceiling, not the value |
| ledger delta after execution | independent | **post** | **yes — but only after the action** |
| requested amount | **agent** | pre | no — agent-authored |
| per-action cap | independent | pre | a cap, not the value |
| maximum the tool accepts | independent | pre | a cap, not the value |
| signature threshold by amount | independent | pre | a threshold, not the value |

**No observable is simultaneously agent-independent, available before authorisation, and equal to the committed value.**

Two quantities are available, and they are not the same thing:

- **the value** — independent, but only *post*-authorisation
- **the bound** — independent and *pre*-authorisation, but an upper bound

The design requires all three properties of `V` at once and no observable supplies them together. This is a specification defect in the current design, at the same structural level as D1a.

## 4. Identity binding — a new property `V` needs and `I` did not

`I` binds to a tool by exact registry identity, and a mismatch fails closed. `V` binds to an **action instance**, which is strictly harder.

Without it, the following is constructible and technically independent:

```text
action A
   ↓
V observable belonging to B
   ↓
V attached to the classification of A
```

The derivation would read an independent source and still be **semantically wrong**. Identity binding for `V` therefore requires:

| Sub-property | Requirement |
|---|---|
| action identity | the value is bound to the specific action being classified, not to any value in the same account |
| binding token | the binding is unforgeable by the agent |
| staleness | a value from a prior action cannot attach to a later one |
| cross-action rejection | reading B's value while classifying A must fail closed, not silently substitute |

## 5. Required controls

None may be implemented before §1–§4 are settled.

| Control | Setup | Required outcome | Tests |
|---|---|---|---|
| **`V−`** | ground truth genuinely low; agent declares high | derived `V` cannot exceed the observable | the derived path cannot inflate |
| **`V+`** | ground truth genuinely high | high value reaches the policy | the derived path has **no artificial ceiling** |
| **`VΔ`** | agent declares $V_1$, observable authority contains $V_2 \ne V_1$ | $V_2$ prevails | the authority is not advisory |
| **`Vid`** | value belongs to a different action | binding rejected, fail closed | identity binding, per §4 |

**`VΔ` is the load-bearing one.** `V_declared = V_derived` by itself demonstrates nothing — it is equally consistent with a derivation that simply inherited the agent's claim. That is precisely the false positive recorded for `I` at `df8875c`, and it must not recur.

**`V+` is not optional.** A derivation that always returns low would pass `V−` while providing no protection at all.

## 6. Unknown and fail-closed

Following `304d920` §6, stated as a pipeline invariant rather than a threshold choice:

> If `V` cannot be determined from its authority, it is `V_UNKNOWN`, and **`V_UNKNOWN` shall not yield a risk score below the `L0` threshold.**

The invariant holds regardless of which candidate below is chosen, and must be re-proven per arm rather than assumed from the current one.

## 7. Three candidates — no choice made

| | `V` is the **value** | `V` is a **bound** | `V` stays **declared** |
|---|---|---|---|
| Independent authority | yes, post-hoc | yes, pre-authorisation | **no** |
| Available pre-decision | **no** | yes | yes |
| Uses declared amount | no | no | yes |
| `V−` passable | yes | yes | **no** |
| Prevents the `A2` decomposition attack | post-hoc only | yes, if the bound is tight | **no** |
| Changes the meaning of `V` from the recovered text | no | **yes** | no |
| Honest reading | it is a verification, not a gate | it is worst-case exposure, not magnitude | the surface stays open |

The middle column is architecturally coherent and is **not** what the recovered text says `V` is. Adopting it would be a redesign of the variable, not a repair of its authority — and by the standard applied at `41fdc4b`, that must be declared rather than smuggled in as a repair.

## 8. What is not decided here

- **No candidate selected.** §3 is a finding about the current design, not a recommendation to adopt the bound.
- **No implementation.** Not before §1–§6 are audited.
- **No threshold changes.** The `V` scale and its normalisation are unspecified in the recovered text and are not invented here.
- **`N` and `P`** are untouched and remain agent-influenced. `V` is the next surface, not the last.
- `I` is not modified, and the `84a5fd1` adjudication is not amended.

## 9. The rule inherited from `I`

> If a variable cannot be obtained from an agent-independent observable within the declared scope, that is an **architecture or specification finding** — not an invitation to invent a source of authority.

Applied here, it produces §3 rather than a solution. §3 is the deliverable of this specification, and the specification stops there.