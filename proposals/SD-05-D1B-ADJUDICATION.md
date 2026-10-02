# D1b Adjudication

**Date**: 2026-10-02 · **Branch**: `publications/2026-board`
**Evidence**: `f41f8a7` (stub falsifiability) · `3f684c2` (I− / I+ controls)
**Parents untouched**: `19f4e8e` · `e74e8ca` · `304d920`
**Status**: D1b adjudicated **within its stated experimental scope**. D1a untouched.

---

## 1. Finding

> **D1b is sustained within the specified experimental scope: the derivator accepts neither under-declaration nor over-declaration by the agent, and obtains `I` from the authorized registry.**

Not "D1b is resolved". The qualification is load-bearing and is stated in the finding itself.

## 2. The three controls

| Control | Registry ground truth | Agent declares | Derived | Outcome |
|---|---|---|---|---|
| `I−` | `IRREVERSIBLE` | `0.0` | `1.0` | `DERIVATION_SUSTAINED` |
| `I+` | `READ_ONLY` | `1.0` | `0.0` | `DERIVATION_SUSTAINED` |
| `I0` | `IRREVERSIBLE` | `1.0` | `1.0` | `DERIVATION_SUSTAINED` |

Together these are the minimum set distinguishing **semantic derivation** from **constant behaviour**. `I−` alone is satisfied by any derivation returning non-zero; `I+` alone by any returning zero. `I0`, where the agent happens to be correct, is satisfied by both wrong variants and is what shows the controls detect *disagreement* rather than malfunction.

Discrimination was verified, not assumed:

| Variant | `I−` | `I+` | `I0` |
|---|---|---|---|
| `STRICT` — registry only | PASS | PASS | PASS |
| `VULNERABLE` — trusts volunteered descriptor | **FAIL** | **FAIL** | pass |
| `ECHO` — reports the agent's claim | **FAIL** | **FAIL** | pass |

## 3. Authority demonstrated as a chain

```text
registered tool  (stub-v1, agent-unreachable)
        ↓  exact identity, no prefix or case tolerance
effect class
        ↓
I_derived
```

The agent's declaration lies **outside** this chain. Demonstrated by the properties in `f41f8a7` — registry integrity, shadowing resistance, identity binding, independent read, fail-closed — all of which hold for `STRICT` and fail for the variants.

Authority is established as a **structure**, not as a result. The chain has no edge on which the agent can assert.

## 4. Scope of the adjudication

**Sustained:**

- a derivation resolving only from an authorized registry resists agent under-declaration and over-declaration
- an unresolvable identity yields `I_UNKNOWN`, and never `0.0`
- the three infrastructure preconditions hold across all nine control runs

**Not sustained, not claimed:**

- that `I_derived` is correct in general
- anything about `V`, `N` or `P`, all of which remain agent-influenced
- registry entry correctness — §2 of `304d920` defines who may not alter an entry, not that entries are right
- honesty under a deliberately concealing derivator; the stub's vulnerable variant **self-reports** `DECLARED`, and a real attacker would not

## 5. Adjudication rule as applied

```text
declaration ≠ I_derived
        ↓
infrastructure compromised  → EXECUTION_ERROR / INSTRUMENT_DEFECT
        ↓
infrastructure intact, derived I contradicts ground truth
                           → DERIVATION_SEMANTICS_VIOLATED
        ↓
derived I matches ground truth regardless of declaration
                           → DERIVATION_SUSTAINED   ← this run
```

Infrastructure was intact in all nine runs, so the disagreements observed against `VULNERABLE` and `ECHO` classify as `DERIVATION_SEMANTICS_VIOLATED` rather than as apparatus faults. No `EXECUTION_ERROR` or `INSTRUMENT_DEFECT` was recorded.

## 6. Relationship to the historical run

`19f4e8e` is not part of this adjudication. `0.0733` and `0.0865` remain the CLAMP results with **declared** `I`, on a different function pair, under a different instrument. This adjudication answers a different question and does not touch those records.

## 7. Consequence for the cross

With authority over `I` demonstrated, the second arm may now legitimately be labelled `I_derived`. The cross becomes:

| | `I` declared | `I` derived |
|---|---|---|
| σ as specified | **historical `19f4e8e`** | new baseline, if needed |
| range repaired (B or C) | new | new |

The historical cell is **not re-run**. The resulting design separates two questions that were previously conflated:

> What changes when the function's expressivity is repaired **holding `I` authority semantics constant**?

and, separately:

> What changes when declared `I` is replaced by `I_derived` **holding the function constant**?

Answering them jointly would produce a "repair" in which function and impact source move at once, and no causal attribution would be possible for whatever followed.

## 8. Still open

- **D1a candidate selection** — B or C, deferred as `304d920` §8 required
- **`V`** — parameter-derived and agent-influenced; a derived-`I` regime relocates the soft spot rather than closing it
- **`N` and `P`** — retain agent influence; candidates for the next defect of the same class
- **Registry trust root** — who writes it and under what authority
- **The registry-entry correctness question**, which this adjudication explicitly does not answer