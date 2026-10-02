# Instrument Finding — Control Vacuity by Nominal Execution

**Class**: `CONTROL-NOT-DELIVERED` — a distinct instance of the falsifier family, adjacent to but not identical with `NON-DISCRIMINATING-FALSIFIER` (`1752c30`)
**Evidence**: `f41f8a7` and `3f684c2`, two independent occurrences
**Status**: FROZEN. Separate from D1b; the D1b adjudication does not absorb it.

---

## 1. The defect

> **A control that is not delivered an instance of the behaviour it claims to falsify can report PASS, because it simply executes the nominal path.**

The discriminator is not whether a test is weak. It is whether the test was ever **put in the situation it names**.

## 2. The frozen rule

```text
CONTROL_VALID
    =
    target behavior is actually presented
    AND
    target path is observably distinguishable from the control path
```

**A PASS without both conditions is not evidence.** Not weak evidence — not evidence.

## 3. Two occurrences, which is what makes this a finding rather than an anomaly

### Occurrence 1 — `f41f8a7`

Four of six properties reported PASS under both the strict and the deliberately vulnerable derivation:

```
registry_integrity     PASS / PASS     NO - vacuous
identity_binding       PASS / PASS     NO - vacuous
fail_closed_invariant  PASS / PASS     NO - vacuous
effect_provenance      PASS / PASS     NO - vacuous
```

Cause: those three tests passed **no agent surface** to either mode, so both modes resolved from the registry by the same route. Four clean PASSes that carried no information.

### Occurrence 2 — `3f684c2`

`VULNERABLE` passed all three of `I−`, `I+`, `I0`. Had this gone unreported, the result would have read that `VULNERABLE` behaves equivalently to `STRICT` on the controls — which is false and would have materially changed the reading of the run.

Cause, identical: `VULNERABLE` was handed `surface=None` and fell through to the registry, so its distinctive behaviour was never exercised.

## 4. Why two occurrences matter

A single occurrence is a plausible harness bug, repairable in place. **A repeat of the same cause, in a different suite written afterwards, is evidence about method.**

The second occurrence happened *after* the first was diagnosed and recorded. The same gap reappeared because nothing structural prevented it: the mode list was implicit in each test's construction rather than an explicit parameter.

The corrective in `3f684c2` is the durable part — every mode now receives the agent's volunteered declaration, and the mode list is explicit per control. The occurrence is retained because the fact that it recurred is the finding.

## 5. Distinction from `NON-DISCRIMINATING-FALSIFIER`

| | `NON-DISCRIMINATING-FALSIFIER` (`1752c30`) | `CONTROL-NOT-DELIVERED` (this) |
|---|---|---|
| Nature | the property **cannot** take its failing value | the failing condition **was never presented** |
| Example | `PASS(p) == "hash changed"` over SHA-256 | variant under test never received the surface that triggers it |
| Direction | the assertion is tautological | the test is misconfigured |
| Fix | design a different property | pass the control what it names |

An R2 defect may still fail sometimes. A non-discriminating falsifier cannot fail at all. This defect is a third thing: the test is capable of failing, and was never given the chance.

## 6. Standing consequence

Any future control must satisfy both conditions of §2 before its result is reported, and the satisfying condition must be recorded in the ledger — not merely asserted. Where a property holds under every variant, it is reported as `invariant-by-construction` with its rationale, rather than counted as a passing test or as a weak one. `effect_provenance` is the worked example: it holds for `VULNERABLE` because that variant labels itself `DECLARED` truthfully, which makes it a labelling property rather than a security property. Conflating the two would be wrong in the opposite direction.

## 7. Scope

This finding is about test construction. It makes no claim about the policy under test, the derivation, or the risk function, and it is recorded separately from the D1b adjudication so that neither absorbs the other.