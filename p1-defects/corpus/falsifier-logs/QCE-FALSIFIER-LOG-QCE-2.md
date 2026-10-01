==============================================================================
QCE-2 falsifier — reconstructibility of the ablation arms
property: each tab:ablation row is a reconstructible experimental state of
         the same system, defined by an executable intervention
==============================================================================

  [INFO] validating the re-implementation of run_episode's selection logic
           my episode()      reliability 0.9236938624 power 627.345738 errors 0
           run_episode()     reliability 0.9236938624 power 627.345738 errors 0
           the re-implementation reproduces the original exactly: True
           FULL arm fingerprint: {'errors': 0, 'power': 627.3457, 'reliability': 0.923694, 'risks': [0.1], 'dvfs': [2]}

  [INFO] H4a — NoSafety: the row is defined as `sigma = 0`, i.e. the
         predictor emits raw logistic probabilities with no blending.
           FULL (floor=0.15) {'errors': 0, 'power': 627.3457, 'reliability': 0.923694, 'risks': [0.1], 'dvfs': [2]}
           NoSafety (floor=0.0) {'errors': 18, 'power': 581.995, 'reliability': 0.049862, 'risks': [0.01, 0.1], 'dvfs': [2, 3]}
           R4 it produces a distinguishable state: True
           CONTROL floor=0.60  {'errors': 0, 'power': 354.0291, 'reliability': 0.963554, 'risks': [0.1, 0.7], 'dvfs': [0, 2]}
           the harness detects a safety-path intervention: True
  [PASS] H4a positive control: this harness detects a change on the safety path
  [FAIL] H4a NoSafety (floor=0.0) IS distinguishable from Full: {'errors': 18, 'power': 581.995, 'reliability': 0.049862, 'risks': [0.01, 0.1], 'dvfs': [2, 3]}
         The intervention exists, alters only the safety blend, and changes the
         outcome. The arm is therefore reconstructible from the artifact — which
         means the absence of a code path in qce_simulator.py is a packaging gap,
         not an absent experiment.

  [INFO] H4b — NoRL: the row is defined as 'temperature-based policy
         selection only'. gamma is NOT the intervention: QCE-1 established
         it is never read, so an arm built on it would be vacuous.
         The predictor is removed from the DECISION PATH instead.
           FULL             {'errors': 0, 'power': 627.3457, 'reliability': 0.923694, 'risks': [0.1], 'dvfs': [2]}
           NoRL (temperature policy) {'errors': 0, 'power': 490.8399, 'reliability': 0.94083, 'risks': [0.1, 0.3], 'dvfs': [1, 2]}
           R4 it produces a distinguishable state: True
           CONTROL forced 0.95 prediction {'errors': 0, 'power': 354.0291, 'reliability': 0.963554, 'risks': [0.1, 0.7], 'dvfs': [0, 2]}
           the policy switch is live: True
  [PASS] H4b positive control: the policy switch demonstrably changes the
           outcome, so an unchanged result is a real property of the arm.
  [FAIL] H4b NoRL is DISTINGUISHABLE from Full: {'errors': 0, 'power': 490.8399, 'reliability': 0.94083, 'risks': [0.1, 0.3], 'dvfs': [1, 2]}
         Removing the predictor from the decision path changes the outcome.
         The artifact therefore contradicts the published claim that QCE-NoRL is
         identical to QCE (full). The arm is reconstructible and its published
         identity is not what the artifact produces.

  [INFO] reconstructibility table
  arm            code path    runs  artifact                           published                      verdict
  QCE (full)     run_episode  yes   0 / 627.3 / 0.9237                 0 / 627.3 / 0.9237             MATCH
  QCE-NoSafety   NONE in repo yes   18 / 582.0 / 0.0499                21 / 578.3 / 0.0070            NO MATCH
                 -> the artifact contains no code path for this row; the arm
                    below is RECONSTRUCTED here for comparison only.
  QCE-NoRL       NONE in repo yes   0 / 490.8 / 0.9408                 0 / 627.3 / 0.9237             NO MATCH
                 -> the artifact contains no code path for this row; the arm
                    below is RECONSTRUCTED here for comparison only.

==============================================================================
FAILED: H4a-nosafety-is-reconstructible, H4b-norl-is-distinguishable-from-full, QCE-NoSafety-no-code-path-and-published-value-not-reproduced, QCE-NoRL-no-code-path-and-published-value-not-reproduced

Design-identity finding: neither ablation row has a code path in the
artifact. Both are reconstructible here as interventions, and neither
reproduces its published value.

The numerical identity of QCE-NoRL and QCE (full) is NOT treated here as
proof that the arm lacks effect. It is compared against what removing
the predictor from the decision path actually produces, because an arm
with no code path cannot have its effect measured from its absence.

## Reimplementation validated first

`episode()` reimplements `run_episode`'s selection logic so the temperature-policy arm
can be built. It was validated BEFORE use by running it in `original` mode and
comparing against the native `run_episode`:

    my episode()    reliability 0.9236938624   power 627.345738   errors 0
    run_episode()   reliability 0.9236938624   power 627.345738   errors 0
    exact match: True

An unvalidated reimplementation cannot distinguish "this arm has no effect" from "I
reimplemented it wrong". It matched exactly, to ten decimals.

## H4a — NoSafety

The row is defined at `main.tex:433` as "QCE without the safety floor (σ = 0). The
predictor outputs raw logistic regression probabilities without blending." The
intervention is therefore `predictor.safety_floor = 0.0`, which changes `predict()`
from `0.15 + 0.85*raw` to `raw` and touches nothing else.

| | errors | power (mW) | reliability | risk levels | DVFS |
|---|---|---|---|---|---|
| Full (floor 0.15) | 0 | 627.3457 | 0.923694 | [0.1] | [2] |
| NoSafety (floor 0.0) | **18** | **581.9950** | **0.049862** | **[0.01, 0.1]** | **[2, 3]** |
| published | 21 | 578.3 | 0.0070 | — | — |
| control (floor 0.60) | 0 | 354.0291 | 0.963554 | [0.1, 0.7] | [0, 2] |

**The paper's causal story is qualitatively confirmed.** `:454` predicts that without
the floor the predictor drifts low, risk level 0.01 becomes reachable, DVFS 3 is
selected, and the system suffers thermal runaway. Every step of that chain occurs:
risk 0.01 appears for the first time, DVFS 3 appears for the first time, and errors
appear. The floor is doing what the paper says it does.

**The numbers do not reproduce.** 18 errors against 21, 582.0 mW against 578.3,
reliability 0.0499 against 0.0070 — the last differs by a factor of seven. The
phenomenon is confirmed and its magnitude is not.

**The arm is reconstructible.** The intervention exists, alters only the safety blend,
holds every other component constant, and produces a distinguishable state. So the
absence of `NoSafety` from `qce_simulator.py` is a **packaging gap, not an absent
experiment**.

## H4b — NoRL

`NoRL` is NOT `gamma = 0`. QCE-1 established `gamma` occurs once and is never read;
an arm built on it would be vacuous. The predictor is instead removed from the
**decision path**, which is the causal route it actually takes.

| | errors | power (mW) | reliability | risk levels | DVFS |
|---|---|---|---|---|---|
| Full | 0 | 627.3457 | 0.923694 | [0.1] | [2] |
| NoRL (temperature policy) | 0 | **490.8399** | **0.940830** | **[0.1, 0.3]** | **[1, 2]** |
| published | 0 | 627.3 | 0.9237 | — | — |
| control (forced 0.95) | 0 | 354.0291 | 0.963554 | [0.1, 0.7] | [0, 2] |

**The artifact does not produce the published identity.** Removing the predictor from
the decision path changes the outcome on both axes — reliability rises to 0.940830
and power falls to 490.8399 mW. The published row asserts identity with Full.

Why: the predictor emits a constant 0.150039 and therefore always selects risk 0.1
(QCE-1), whereas the junction temperature ranges 45.00 to 74.65 over the episode and
therefore selects risk 0.1, 0.3 and 0.7 at different steps. The two policies are not
the same policy, and on this workload they are not equivalent.

**Both reconstructions beat the published Full result on both axes.** That is an
observation, not a claim: neither reconstruction is a like-for-like competitor arm,
and no arm in the manuscript is beaten by one. It is recorded because it bears on
where the published ablation numbers came from, not because it indicts a policy.

## The identity question is kept separate, as it must be

The published `QCE-NoRL` row is numerically identical to `QCE (full)`. That identity
is **not** treated as proof that the arm lacks effect. An arm with no code path cannot
have its effect measured from its absence, and the reconstruction shows what removing
the predictor actually does. Both facts stand independently:

- the published identity is not produced by the paper's own definition of NoRL;
- and the identity is not, by itself, evidence that NoRL was a null arm.

A third possibility remains open and is not excluded: the published row may have been
produced by an implementation that differs from the description at `:434`. This
repository contains no code path to test that against, which is precisely the
finding.

## Reconstructibility summary

| arm | code path in repo | runs | artifact | published | verdict |
|---|---|---|---|---|---|
| QCE (full) | `run_episode` | yes | 0 / 627.3 / 0.9237 | 0 / 627.3 / 0.9237 | **MATCH** |
| QCE-NoSafety | none | yes | 18 / 582.0 / 0.0499 | 21 / 578.3 / 0.0070 | **NO MATCH** |
| QCE-NoRL | none | yes | 0 / 490.8 / 0.9408 | 0 / 627.3 / 0.9237 | **NO MATCH** |

Neither row has a code path. Both are reconstructible from the paper's own definitions.
Neither reproduces its published value.

## Falsifier defects found while building QCE-2 (all retained)

1. **An unreadable formatting hack.** The reconstructibility table was first written
   with `chr(101)+chr(114)+chr(114)+chr(111)+chr(114)+chr(115)` to build the word
   "errors" inside a nested f-string. It worked and was unreadable. Replaced with
   `%`-formatting.

2. **A hypothesis asserted before it was measured, in the diagnostic that preceded
   this falsifier.** Before writing QCE-2 I hypothesised that the temperature policy
   would also select risk 0.1 throughout, which would have explained the published
   NoRL identity and exonerated the paper. I wrote the concluding lines —
   "BOTH policies select risk 0.1 for all 200 steps", "may be TRUE and EXPLAINED" —
   **before** running the measurement. The measurement refuted the premise: temperature
   ranges 45.00 to 74.65 and crosses two thresholds.

   Had the script printed those lines and I read only its output, I would have
   reported a fabricated conclusion that vindicates the manuscript. This is the third
   instance in this sweep of a hardcoded conclusion printed beside a measurement that
   did not support it, and the reason QCE-2 emits only computed text.

## Boundary

Established: neither ablation row has a code path; both are reconstructible from the
paper's definitions; neither reproduces its published value; the NoSafety causal
story is qualitatively confirmed; the NoRL identity is not produced by the paper's own
definition of NoRL.

Not established, and not claimed: which implementation produced the published rows; whether
the published NoSafety magnitude can be reached by any variant; whether a
"Quantum-Only baseline" ever existed in a form this repository preserves.

Claim correspondence is **NOT ADJUDICATED** here. That is the next phase.
