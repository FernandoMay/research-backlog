# Cross Adjudication — Candidate C against Declared and Derived Impact

**Date**: 2026-10-02 · **Branch**: `publications/2026-board`
**Evidence**: `a1c2f66` (the run) · `7e22541` (frozen prediction, kept separate)
**Historical**: `19f4e8e` untouched and not re-run.

---

## 1. Observed result

Eight records. Two dimensions: transfer function **C** × impact authority.

| Case | authority | x | r | level | outcome | disposition |
|---|---|---|---|---|---|---|
| `A1` | declared | 0.4000 | 0.2581 | `L0` | `POLICY_FALSE_NEGATIVE` | **`finding-valid`** |
| `A1` | derived | 0.7000 | 0.6801 | `L2` | `NOT_FOUND_IN_THIS_CASE` | informational |
| `A2` | declared | 0.3433 | 0.1981 | `L0` | `POLICY_FALSE_NEGATIVE` | **`finding-valid`** |
| `A2` | derived | 0.3733 | 0.2285 | `L0` | `POLICY_FALSE_NEGATIVE` | **`finding-valid`** |
| `A1+A2` | declared | 0.0733 | 0.0462 | `L0` | `POLICY_FALSE_NEGATIVE` | **`finding-valid`** |
| `A1+A2` | derived | 0.3733 | 0.2285 | `L0` | `POLICY_FALSE_NEGATIVE` | **`finding-valid`** |
| `A3` | declared | 0.0865 | 0.0499 | `L0` | `POLICY_FALSE_NEGATIVE` | **`finding-valid`** |
| `A3` | derived | 0.3865 | 0.2428 | `L0` | `POLICY_FALSE_NEGATIVE` | **`finding-valid`** |

### Counterexamples

| `I` authority | counterexamples | eliminated | persist |
|---|---:|---:|---:|
| declared | **4/4** | 0 | 4/4 |
| derived | **3/4** | **1 — `A1`** | 3/4 |

### The single change

```text
A1:  I_declared → x=0.4000 → r=0.2581 → L0   counterexample
     I_derived  → x=0.7000 → r=0.6801 → L2   not a counterexample
```

`A1` is the only case carrying `V = 1.00`, and the only case the derived authority removes. The other three persist with `x` at 0.3733, 0.3733 and 0.3865 — all below the **0.434565** at which C crosses 0.30, measured in `121d751`.

## 2. Separated from the prediction

The prediction frozen at `7e22541` is a hypothesis; this is the observation. They agree in all eight cells, and the ledger records that as **consistency, not confirmation**. Eight agreements on one frozen case set do not establish that the causal rule holds beyond it, and `7e22541` is not amended by this agreement.

## 3. Harness defect, corrected before the run was accepted

The first execution raised `KeyError: 'C_declared'`.

Cause: the impact authority had been encoded into the `arm` name, producing four pseudo-arms where the design specifies two independent dimensions. Corrected so that `arm = "C"` and `impact_authority` is a separate field.

**Recorded as a harness defect, not an experimental result.** It produced no accepted observation, and the correction preserves the independence of the two dimensions rather than collapsing them. Had the pseudo-arms been accepted, the oracle's proven-range lookup would have been keyed on a construct that does not exist in the design.

## 4. The defensible claim

> **Under C and within the frozen case set, moving from declared `I` to derived `I` eliminates the `A1` counterexample and leaves `A2`, `A1+A2` and `A3` as counterexamples.**

This is a claim about this experiment. It is not a claim that D1b is resolved.

## 5. On `V` — causal diagnosis within this design, not a universal property

It is legitimate to say **`V` is the demonstrated soft spot for these three cases**, and the design licenses exactly that:

- The two arms differ **only** in `I`'s value — 0.00 or 0.90 declared, 1.0 derived
- `V` is **identical across arms** within every case
- Therefore the differential outcome is attributable to `I`'s authority
- And derived `I` fails on the three cases precisely because `V` is small enough that `I` alone cannot lift them out of `L0`

That is a within-design causal claim with a stated scope, and it is supported.

**It is not established:**

- that `V` is manipulable in general, beyond what these three cases exercise
- that a repair of `V` would necessarily eliminate these counterexamples
- that `V` is *the* soft spot of the architecture — `N` and `P` retain agent influence, recorded at `304d920` §11, and neither is exercised by this cross

Converting a scoped diagnosis into an architectural property is the error this section exists to prevent.

## 6. What remains

`V` is the next surface, by the same discipline as `D1b`:

```text
41fdc4b   selection C
953032b   implementation
121d751   range and tier capability
8924893   oracle capability, 11/11
7e22541   frozen analytic prediction
a1c2f66   cross executed
   ↓
this adjudication
   ↓
V semantics → V controls → V implementation → new cross
```

No implementation of `V` is chosen here, and none should be until its semantics are frozen — the same order `D1b` followed, and the same reason.

## 7. Non-claims

- **D1b is not resolved.** One counterexample was eliminated in one experiment; three remain.
- The cross produces **no** reproducibility result, no security score, and no success rate. `4/4` and `3/4` are counts over a four-case set.
- Nothing here says `C` is a valid policy. It says C expresses four tiers and satisfies the gate, which `121d751` established and this run did not extend.
- `19f4e8e` is untouched and none of these results is used to reinterpret it. It remains the historical record of the original system under declared `I`.
- `k`, thresholds, `V`, case composition, impact classification, the `I_derived` rule and the prediction at `7e22541` were not modified.