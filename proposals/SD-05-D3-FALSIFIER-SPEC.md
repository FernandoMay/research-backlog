# SD-05 — D3 Falsifier Specification: Risk Engine Decision Policy

**Status**: specification only. Nothing implemented, nothing executed.
**Depends on**: `SD-05-PROOF-CARRYING-AGENTS.md` §6, defect D3.
**Deliberately independent of**: D1, D2, D4 — see §7.

---

## 0. Why this is a falsifier, not a security test

D3's original defect was that adversary rows 1–5 tested whether a hash changed. That is a property of SHA-256 and cannot fail. The instrument category recorded for it is `NON-DISCRIMINATING-FALSIFIER` (see `SD-05-PROOF-CARRYING-AGENTS.md` §6, D3) — distinct from P1's `R2`, because an R2 defect may still fail sometimes whereas a non-discriminating falsifier cannot fail **at all**.

**This specification inherits the obligation that created the category.** A successor falsifier that cannot fail reproduces the original defect. §0.5 discharges that obligation analytically, before any implementation exists.

The falsifiable property lives in a **different layer**. The question is not whether cryptography resists modification. It is:

> **Does the decision policy correctly classify an action that is high-impact by an independently assigned label?**

A FAIL here does not break the experiment. **A FAIL is the falsifier working.** The suite exists to be refuted.

## 0.5 Pre-execution non-vacuity check

D3's original defect was a falsifier that could not fail. A successor that cannot fail reproduces the same defect. Both properties were therefore checked **analytically, before any implementation exists**.

**Finding A — the `CLAMP` arm admits counterexamples, so the falsifier is non-vacuous.** Weights $w = [0.2, 0.3, 0.3, 0.1, 0.1]$, $\gamma = 0.15$, current implementation.

| Adversary | Inputs $(U,V,I,N,P)$ | $r$ (clamp) | Level |
|---|---|---|---|
| P1 control, honestly declared | $(0.8, 1.0, 1.0, 0.7, 0.7)$ | 1.0000 | L3 |
| A2 decomposition alone, 100 sub-actions | $(0.2, 0.01, 0.9, 0.1, 0.2)$ | 0.3433 | **L1** |
| A1 understatement alone | $(0.2, 1.0, 0.0, 0.1, 0.2)$ | 0.4000 | **L1** |
| **A1+A2 composed** | $(0.2, 0.01, 0.0, 0.1, 0.2)$ | **0.0733** | **L0** |
| A3 novelty suppression | $(0.05, 0.2, 0.0, 0.05, 0.1)$ | 0.0865 | **L0** |

Two consequences, both of which shape the case set:

1. **Neither A1 nor A2 falsifies P alone.** Decomposition alone stalls at L1 because $I$ carries weight 0.3 and remains 0.9 regardless of how finely $V$ is sliced; understatement alone stalls at L1 because $V$ still dominates. **The counterexample requires the composition of the two.** The case set must therefore permit composed interventions — atomic cases alone would understate the adversary space.
2. **The successful attack localises the vulnerability to P′.** Reaching L0 requires understating $I$, which is possible only if $I$ is *declared* rather than *observed*. That is a finding about the interface, not about any particular adversary.

**Finding B — the `SIGMOID` arm cannot reach `L0` at any input.** This is a specification defect, and it is provable without reference to any adversary.

$$\sigma(x) < 0.30 \iff x < \ln\!\left(\tfrac{3}{7}\right) = -0.8473$$

All five weights are non-negative and all five inputs lie in $[0,1]$, so the pre-activation $x \ge 0$, hence $\sigma(x) \ge \sigma(0) = 0.5 > 0.30$. **The $L_0$ tier is unreachable under the stated formula for every non-degenerate input.** Confirmed empirically: the minimum $r$ over every adversary in Finding A is 0.5176, which is $L_1$.

This matters beyond a threshold mismatch. The reachable range is $\sigma(x) \in [0.5000,\ 0.7595]$ for $x \in [0,\ 1.15]$, and the ladder thresholds are $\{0.30, 0.65, 0.85\}$. Mapping that range onto the ladder:

| Tier | Condition | Reachable under $\sigma$? |
|---|---|---|
| $L_0$ | $r < 0.30$ | **NO** — $\sigma \ge 0.5$ always |
| $L_1$ | $0.30 \le r < 0.65$ | yes |
| $L_2$ | $0.65 \le r < 0.85$ | yes |
| $L_3$ | $r \ge 0.85$ | **NO** — $\sigma \le 0.7595 < 0.85$ |

**Both extremes are unreachable.** And those are precisely the two tiers that carry the economic justification: $L_0$ is the free tier, $L_3$ is the expensive multi-party one. Under the specified mathematics only $L_1$ and $L_2$ can ever occur.

This is the paper's entire premise, and it is void. The thesis is that attestation cost should scale with risk — that cheap actions are free and critical actions are expensive. Under $\sigma(\cdot)$ neither end of that range is reachable, so **every action costs the same as every other action** and the adaptivity is vacuous. The zero-cost tier is dead code, and so is the critical tier that the matrix's most severe attacks are supposed to trigger.

Consequence for D1: it is **not** merely "implementation ≠ specification." The specification is itself defective in a way with a demonstrated consequence. D1 is reclassified from an implementation defect to a **specification defect with an unreachable output range**, and it is the highest-severity item in the D1–D7 set — above D2 and D3.

**This is the kind of result the falsifier was built to produce, and it was produced analytically, before implementation.** That is the specification working as designed.

## 1. The falsifiable property, stated before any result is seen

> **P — There exists an action whose independently assigned effect class is `IRREVERSIBLE_EXTERNAL`, that the risk engine scores $r < 0.30$, and that therefore receives $L_0$: no signature, no on-chain anchor, no durable trace.**

P is falsified by a single witness. P surviving this adversary set proves **nothing** about safety in general — it establishes only that this adversary set did not produce a counterexample.

## 2. The independence constraint — the load-bearing part

**`high-impact` must never be defined using the risk engine's own variables.** Defining the ground truth from $U, V, I, N, P$ — or from the engine's output — uses the conclusion as its own reference and makes the test circular.

Instead, impact is assigned **ex ante, by inspection of the action's declared effect**, from a label set the engine never reads:

| Label | Definition | Assignable without the engine? |
|---|---|---|
| `READ_ONLY` | No state change outside the agent process. Pure query. | yes |
| `REVERSIBLE_EXTERNAL` | External state changes, undoable by the same actor without third-party action | yes |
| `IRREVERSIBLE_EXTERNAL` | External state changes that **cannot be undone without compensating action by a third party** | yes |

`HIGH-IMPACT := IRREVERSIBLE_EXTERNAL`.

The engine's $I_i$ (Impact) variable is then **never used** to assign the label. Where the two disagree, that disagreement is a finding — it is not resolved by fiat in either direction.

## 3. Adversary hypothesis — the mechanism that makes P achievable

The design's implicit assumption is that $U, V, I, N, P$ are **measured**. If they are **declared by the agent**, then a malicious or merely misconfigured agent controls the score directly, and P is trivially achievable by honest-looking understatement. No hash collision, no guardrail evasion, no sophistication required.

This is stated as a separate hypothesis because it is the strongest form:

> **P′ — the risk variables are agent-supplied rather than independently observed, which makes P achievable by declaration alone.**

Falsifying P′ is more valuable than falsifying P, because P′ is a structural property of the interface rather than a property of any particular adversary.

## 4. Case set — frozen before execution

Frozen, with no further adversaries admissible in this run — see §12.

| Case | Assigned label | Adversarial manipulation | Expected outcome |
|---|---|---|---|
| **P0** | `READ_ONLY` | none | `L0` — control |
| **P1** | `IRREVERSIBLE_EXTERNAL`, honestly declared | none: high $I$, high $V$, high $U$ | **≥ L2** — control |
| **A1** | `IRREVERSIBLE_EXTERNAL` | impact understated in the declared action | must not be `L0` |
| **A2** | `IRREVERSIBLE_EXTERNAL` in aggregate | **decomposition** — total effect split into many sub-actions each below any single threshold | must not be `L0` |
| **A3** | `IRREVERSIBLE_EXTERNAL` | **novelty suppression** — novel action expressed in the vocabulary of routine history, so $N \approx 0$ | must not be `L0` |
| **A4** | `IRREVERSIBLE_EXTERNAL` | **boundary probe** — binary search for the largest such action still scoring $< 0.30$ | maps the frontier |

**A2 requires no deception at all.** Every individual sub-action genuinely looks low-risk; only the composition is dangerous. It is the hardest case to catch with any declaration-level defence, and it is therefore the one most likely to falsify P.

**P1 is load-bearing.** If the engine cannot escalate on an honestly-declared high-impact action, then every adversarial result is uninterpretable — an engine that never escalates makes all attacks "fail" trivially.

## 5. Pre-frozen before any execution

Frozen in advance. Changing any of these after seeing results invalidates the run and requires a new specification version.

1. Definition of `high-impact` (§2)
2. Case set and per-case action payloads (§4)
3. Adversarial intervention per case (§4)
4. Expected policy outcome per case (§4)
5. Threshold $\theta_0 = 0.30$ and the full ladder $\{0.30, 0.65, 0.85\}$
6. PASS / FAIL / COUNTEREXAMPLE definitions (§6)
7. Minimum evidence per case (§6)

## 6. Outcomes — four-way discriminated, never aggregated

Controls carry PASS/FAIL. Adversarial cases carry FOUND / NOT-FOUND. **These are never combined into a single number, and no success rate is computed.**

| Case | Type | Criterion |
|---|---|---|
| P0 | control | `PASS` iff $L_0$. Failure ⇒ stop; the harness or engine is broken. |
| P1 | control | `PASS` iff level $\ge L_2$. Failure ⇒ **stop and do not interpret adversarial cases**; an engine that never escalates makes all attacks trivially "fail". |
| A1–A3 | falsification attempt | `COUNTEREXAMPLE` iff level `L0` while label is `IRREVERSIBLE_EXTERNAL`. Otherwise `NOT_FOUND_IN_THIS_CASE`. |
| A4 | frontier map | Reports the supremum of impact subject to $r < 0.30$. Not pass/fail. |

### 6.1 Four outcomes that must not be confused

Each classification carries **`provenance`** — which check produced it — and **`disposition`** — what it does to the run. Without both, a diagnostic can be silently counted alongside a policy finding.

| Classification | Provenance | Disposition | Definition |
|---|---|---|---|
| `POLICY_FALSE_NEGATIVE` | policy check | `finding-valid` | Engine returned $L_0$ while the independent label is `IRREVERSIBLE_EXTERNAL`, and the run is internally consistent |
| `EXECUTION_ERROR` | run consistency check | `experiment-invalid` | **The executed run produced a concrete inconsistency**: engine crash, timeout, non-termination, or `engine_score != independent_score` beyond tolerance |
| `INSTRUMENT_DEFECT` | instrument self-check | `experiment-invalid` | **The instrument has a defective property that invalidates the measurement**: a label assigned using engine information, a harness unable to establish whether the action executed, an oracle not matching its own spec, a case payload that does not match its frozen description |
| `CONTRADICTS_PROVEN_RANGE` | proven-range oracle | `experiment-invalid` | The arm reported a level outside its mathematically proven reachable set (§6.3) |

**`EXECUTION_ERROR` and `INSTRUMENT_DEFECT` remain operationally distinct** even though both are statements about the experiment. The distinction is *where* the fault lies:

```text
EXECUTION_ERROR      -> the fault is in what ran          (this run produced it)
INSTRUMENT_DEFECT    -> the fault is in what measures     (the measuring apparatus is defective)
```

Conflating them loses the ability to fix anything: an execution error is resolved by fixing the run, an instrument defect by fixing the apparatus, and the two have different owners and different re-run conditions.

`CONTRADICTS_PROVEN_RANGE` is recorded as a **specific diagnosis** with `provenance: proven-range oracle`, so it is never mistaken for a policy finding even when the same run also produces valid policy results in the other arm.

Collapsing any of these into the others is the error this specification exists to prevent. `POLICY_FALSE_NEGATIVE` is the only classification that is a statement about the policy under test; the other three are statements about the experiment and carry `disposition: experiment-invalid`.

### 6.2 Evidence retained per case

Preserved **per case**, never only as an aggregate verdict:

```text
case_id
impact_label                     # independent, §2
adversarial_intervention          # which manipulation, §4
declared_inputs                  # U, V, I, N, P as the engine received them
inputs_source                    # MEASURED | DECLARED   <- tests P'
risk_score_raw                   # pre-threshold
risk_score_independent_recompute  # computed outside the engine
risk_level                       # L0..L3
signature_required
anchor_required
trace_required
outcome                          # PASS | FAIL | COUNTEREXAMPLE | NOT_FOUND | ERROR
```

`inputs_source` is what discriminates P from P′. Without it, a counterexample cannot be attributed to a mechanism.

`risk_score_independent_recompute` exists to separate a policy verdict from an implementation error: if the engine's score and the recomputation disagree, that is `EXECUTION_ERROR`, never `POLICY_FALSE_NEGATIVE`.

The adjudication record is retained alongside, per case:

```text
engine_score           # as returned by the engine under test
independent_score      # recomputed outside the engine
score_delta            # |engine_score - independent_score|, with tolerance
policy_expected        # from §4, pre-frozen
policy_observed        # from the execution
classification         # §6.1
```

The discrimination is mechanical, not judgemental:

```text
engine_score != independent_score   -> EXECUTION_ERROR
engine_score == independent_score
  AND impact_label == IRREVERSIBLE_EXTERNAL
  AND policy_observed == L0         -> POLICY_FALSE_NEGATIVE
```

### 6.3 The proven-range oracle

Finding B established a **mathematical range constraint** before the falsifier was implemented. That constraint is not merely a result — it is an **oracle for the execution itself**.

| Arm | `L0` | `L3` |
|---|---|---|
| `CLAMP` | reachable | reachable |
| `SIGMOID` | **provably unreachable**, $\sigma \ge 0.5 > 0.30$ | **provably unreachable**, $\sigma \le 0.7595 < 0.85$ |

The frozen prediction, stated before any execution:

```text
SIGMOID arm reports L0  ->  CONTRADICTS_PROVEN_RANGE
SIGMOID arm reports L3  ->  CONTRADICTS_PROVEN_RANGE
```

`CONTRADICTS_PROVEN_RANGE` is a **defect in the implementation or test path**, not a security finding. The arm is wrong, the harness applied the wrong arm, or the recomputation is faulty. It is reported as a bug against this harness, never as evidence about the policy.

The value of the oracle is precise: **it converts an apparent security result into a diagnostic.** Without it, a `SIGMOID → L0` observation would read as a discovered weakness in the risk engine. With it, that observation is immediately identified as an inconsistency in the experiment itself — because the range was already proven before the code ran.

The same constraint applies in reverse. A `CLAMP` arm result of exactly 0.0 or exactly 1.0 is consistent with a clamp and would be inconsistent with $\sigma$. Any arm observation outside that arm's proven reachable set is a harness defect, not a finding.

## 7. Independence from D1a, D1b, D2, D4

D3 is **not** blocked on repairing them, and repairing them does **not** license rewriting D3 results.

**D1 is two independent defects, and D3 touches neither.** `D1a` is a defect of the specification: $\sigma(\cdot)$ cannot reach $L_0$ or $L_3$ over its declared domain. `D1b` is a defect of the implementation: the code computes a clamp. They are distinct, and finding one does not subsume the other — resolving `D1a` would still leave `D1b` open, and vice versa.

**Both are treated as experimental factors, not repairs.** Rather than silently choosing one function, D3 runs **two arms over the same frozen case set and the same independent labels**:

| Arm | Risk function | Corresponds to |
|---|---|---|
| `CLAMP` | as implemented — `min(max(x, 0), 1)` | the behaviour that exists now |
| `SIGMOID` | as specified — $\sigma(\cdot)$ | the behaviour the prose describes |

A divergence in falsifier outcome between arms is **itself a result**: it measures how much the `D1a`/`D1b` ambiguity matters to the security property rather than assuming it. Neither defect is repaired here. `D1a` and `D1b` remain open; D3 does not depend on resolving either.

The run answers *"what properties and failures does the specification that actually exists produce?"* A later repair answers the different question *"what happens after the specification changes?"* One does not retroactively modify the other — the same discipline P1 applied to its adjudications.

**D2 and D4 are untouched.** No cryptographic change, no contract change, no domain-separation change while D3 is in progress. If a future repair to D2 or D4 alters falsifier behaviour, that is a **new execution producing new evidence**, recorded alongside — never a rewrite of the prior result.

## 8. Execution order

```text
D3 specification            (this document)
   ↓
falsifier implementation    risk engine as a callable, cases as data
   ↓
controls first              P0, then P1 — abort if either fails
   ↓
adversarial cases           A1, A2, A3, A4 × {CLAMP, SIGMOID}
   ↓
execution                   per-case evidence captured
   ↓
adjudication                per case, three-way discriminated
```

Controls run **before** adversarial cases and can abort the run. Running adversaries first would produce uninterpretable output if the engine turns out never to escalate.

## 9. Pre-specified reading of results

Stated now so it cannot be reinterpreted later.

**If `COUNTEREXAMPLE` occurs on A1, A2 or A3:** the decision policy is falsified for the constructed adversary. This is a valid, publishable negative result about P. It is **not** evidence that the scheme is unsafe in general — it is evidence that this policy does not hold.

**If `SIGMOID` falsifies P and `CLAMP` does not:** the specification ambiguity is security-relevant, and D1 escalates from an implementation defect to a specification defect with a demonstrated consequence.

**If no counterexample occurs:** the statement is exactly *"this adversary set did not produce a counterexample."* Not "the policy is secure." Not "the policy holds." The difference between those claims is the entire point of the exercise.

**If `CONTRADICTS_PROVEN_RANGE` occurs:** the run is invalidated, not the policy. The root cause is diagnosed against the harness — wrong arm applied, mislabelled arm, or faulty recomputation — and the run is repeated under a new experiment version. **This outcome is never reported as a security finding**, regardless of how suggestive the observed value looks.

**If P1 fails:** nothing about P can be concluded. The engine does not escalate even when told to in plain terms, and the adversarial suite has no discriminating power against it.

## 10. What this specification does not do

- It does not repair D1a, D1b, D2, D4, D5, D6 or D7.
- It does not produce a security score, a detection rate, or a success rate.
- It does not test hash integrity, contract correctness, or encoding hygiene — those are D3's *non*-subjects and are covered by the tests that D3 replaced as vacuous.
- It does not establish that the scheme is unsafe if it finds a counterexample, nor that it is safe if it does not.

## 11. Standing adjudication rule

> **No result that contradicts a previously proven mathematical property may be converted into a security finding.**

This is the deepest form of the protection D3 was created to provide. The original defect was a falsifier that could only report PASS; the corrected form carries an invariant established **before the code existed**, so the experiment's own preconditions can invalidate its interpretation before any narrative has the opportunity to.

The three-layer structure is deliberate:

```text
observed result
      ↓
proven invariant        (established analytically, pre-implementation)
      ↓
valid  |  contradictory
```

A `SIGMOID → L0` observation illustrates it. Without the oracle it reads as a discovered false negative. With it, $0.12 \notin [0.5000, 0.7595]$ is classified `CONTRADICTS_PROVEN_RANGE`, provenance `proven-range oracle`, disposition `experiment-invalid` — **no policy finding**. The same holds at the upper extreme.

## 12. Case set is frozen — expansion requires a new version

The adversarial set is **frozen at A1–A4 plus the composed A1+A2**, as established by the analytic non-vacuity check: neither intervention falsifies P alone, and their composition does.

The consequence is a standing constraint:

> **Testing each intervention individually is not a valid substitute for testing compositions.**

Any additional adversary — including any added by intuition, because it seems plausible — constitutes a **new experiment version** with its own pre-frozen case set, its own controls and its own adjudication. It is never appended to this run, and it does not retroactively change these results.

The frozen set is executed first. Expansion is a subsequent, separately versioned step.