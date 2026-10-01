==============================================================================
QCE-1 falsifier — causal participation of the named mechanisms
property: a component implementing the named algorithm participates causally
         in the reported result
==============================================================================

  [INFO] H3a does `self.params` participate? (variational circuit)
         constructed params: [-0.10128311  0.03142473 -0.09080241 -0.14123037]
         optimize() -> mask [True, True, True, True, True]  score 0.033750
         params set to zeros    -> mask [True, True, True, True, True]  score 0.033750   identical to baseline: True
         params set to +1000    -> mask [True, True, True, True, True]  score 0.033750   identical to baseline: True
         params set to -1000    -> mask [True, True, True, True, True]  score 0.033750   identical to baseline: True
         CONTROL reliability scaled by 0.05 -> mask [False, False, False, False, False]  score 0.010781
         the control moved the output: True
  [PASS] H3a positive control: this harness DOES detect a change when the
           optimizer's inputs change. The invariance below is a property of
           self.params, not of the instrument.
  [FAIL] H3a self.params set to zeros, +1000 and -1000 all left optimize()
         byte-identical. The parameter vector a variational circuit would
         optimise does not enter the computation at any magnitude.

  [INFO] H3b does `gamma` participate? (RL discounting)
         first: what does the predictor actually emit during decisions?
         pred_prob over t>=10 (the decision window): 0.150039 .. 0.150039
         pred_prob over the WHOLE episode (incl. warmup): max 0.575000
         distinct risk levels selected in the decision window: [0.1]
         the predictor's output is CONSTANT during the decision window: True
         predict() returns safety_floor + (1-safety_floor)*raw. With
         safety_floor = 0.15 and a raw value indistinguishable from 0, the
         output sits at 0.150039, which is above the 0.05
         threshold and below 0.2. One risk level is therefore selected
         for all 200 steps, and no predictor parameter can move it.

         POSITIVE CONTROL — a predictor forced to emit 0.95:
           risk levels [0.1] -> [0.7]
           reliability 0.923694 -> 0.963554
           power       627.3457 -> 354.0291
           the predictor IS on the decision path: True
         gamma = 0.9    -> avg_reliability 0.9236938624  avg_power 627.345738  errors 0
         gamma = 0.0    -> avg_reliability 0.9236938624  avg_power 627.345738  errors 0
         gamma = 0.999  -> avg_reliability 0.9236938624  avg_power 627.345738  errors 0
  [PASS] H3b positive control: this harness detects a change in the predictor's
           influence when one exists. Forcing 0.95 moves reliability, power and the
           selected risk level. The invariance below is a property of the trained
           predictor, not of the instrument.
  [FAIL] H3b gamma = 0.0, 0.9 and 0.999 produced IDENTICAL reliability, power
         and error counts across a full episode.

         The cause is now established rather than assumed. The predictor emits a
         constant 0.150039 throughout the decision window, so it always selects
         risk 0.1. A parameter that can only reshape a constant cannot
         move any reported quantity. `gamma` is doubly inert: it is never read
         (one occurrence in the file), and the quantity it would have discounted
         is itself constant.

  [INFO] H3c does `optimize()` ever return a SET? (Pareto)
         distinct return shapes across 6 different cost scalings: 1
           mask is a 5-element list, score is a float
         CONTROL a real Pareto routine over 5 points returns 4 points: [(1, 5), (2, 3), (3, 2), (5, 1)]
         this check can distinguish a single point from a front: True
  [FAIL] H3c optimize() returns exactly one mask of 5 booleans and one
         scalar, for every cost scaling tried. No front, no candidate
         set, no trade-off surface is ever returned. The optimizer DOES
         minimise its cost Hamiltonian — the control above proves it is
         causal — but a single-point argmin is not a Pareto computation.
==============================================================================
FAILED: H3a-params-not-causal, H3b-gamma-not-causal, H3c-no-front-ever-returned

Implementation facts, adjudicated separately:
  H3a  self.params does not enter optimize() at any magnitude.
  H3b  gamma does not change reliability, power or error count across a
       full episode.
  H3c  optimize() returns one point, never a front, while still being
       causal on its inputs.

These three adjudicate three mechanisms. None transfers to the others.
Claim correspondence is NOT ADJUDICATED here.

## Falsifier defects found while building QCE-1 (all retained)

1. **The positive control for H3b was causal in principle and still moved nothing.**
   The original control intervened on `predictor.lr`, which sits directly on the SGD
   update path and is unambiguously causal *in general*. It produced identical
   reliability, power and error counts, and the block correctly declared its own
   results void.

   Investigating that failure produced a finding deeper than the one the block was
   built for: the trained predictor emits a **constant 0.150039** for every step in
   the decision window, so it selects risk level 0.1 for all 200 steps and no
   predictor parameter can move the outcome.

   This is a genuine subtlety about causal-intervention methodology and is recorded
   as such: **a variable can sit on the causal path and still have no effect on a
   given outcome.** An intervention test that only asks "does intervening change the
   result?" cannot, by itself, distinguish "this variable is dead" from "this
   variable cannot matter given the state the system is in." The second question
   needs the diagnostic that was added — what does the predictor actually emit.

   The control was replaced with a forced-predictor subclass, which does move
   reliability (0.923694 → 0.963554), power (627.3457 → 354.0291) and the selected
   risk level ([0.1] → [0.7]).

2. **Dead code in the control block.** `m_forced, h_forced = run_pipeline(None)`
   merely re-ran the baseline and was immediately overwritten. It read as though it
   were part of the positive control. Removed.

3. **A module reload crash in the ad-hoc diagnostic.** `sys.modules.pop` followed by
   `importlib.reload` raised `ImportError: module qce_simulator not in sys.modules`,
   and it destroyed the diagnostic mid-run — including the run that produced the
   decisive `pred_prob` constant. The diagnostic had to be rebuilt. A diagnostic
   that crashes after printing its most important number is still a failed
   diagnostic.

## What this falsifier establishes, mechanism by mechanism

**H3a — QAOA / variational circuit. FAILS.**
`self.params` set to zeros, +1000 and −1000 all leave `optimize()` byte-identical:
same mask, same score to six decimals. The positive control — scaling the reliability
inputs by 0.05 — moves the mask from `[True]*5` to `[False]*5` and the score from
0.033750 to 0.010781, so the harness detects participation when it exists.

**H3b — RL discounting. FAILS.**
`gamma` ∈ {0.0, 0.9, 0.999} produce identical reliability (0.9236938624), power
(627.345738) and error counts (0) across a full episode. `gamma` is doubly inert: it
occurs once in the file and is never read, **and** the quantity it would have
discounted is itself constant.

**H3c — Pareto. FAILS.**
`optimize()` returns one 5-element boolean list and one float, for all six cost
scalings tried. A deliberately genuine Pareto routine over 5 points returns 4
points, so the check distinguishes a single point from a front.

**Crucially: H3c's control also proves the optimizer IS causal on its inputs.** The
finding is not "the optimizer does nothing" — it minimises its cost Hamiltonian
correctly. The finding is that a single-point argmin is not a Pareto computation.

## The three mechanisms are adjudicated separately

None of these results transfers to the others. H3a says the parameter vector is dead;
it does not say the optimizer fails to minimise. H3b says the trained predictor is
non-discriminating; it does not say the predictor is disconnected — the forced-
predictor control proves it is connected. H3c says no front is ever returned; it does
not say the cost function is wrong.

## An observation recorded outside the paper's comparison set

The forced 0.95 predictor selects risk 0.7 and yields reliability **0.963554** at
**354.0291 mW** — better than the reported QCE result on *both* axes
(0.923694 at 627.3457 mW).

This is **not** a defect claim. It compares a hand-forced constant against a trained
model, and it falls outside the paper's comparison set (none / reactive / full /
QCE), so no arm in the manuscript is beaten by a like-for-like competitor. It is
recorded because it bears on the safety-floor argument at `main.tex:454` — the paper
attributes the predictor's conservatism to the floor, and this shows the operating
point the floor produces is not forced by the floor alone.

Any claim that "a better policy was available" would require adding that arm to the
experiment. It has not been added, and this observation asserts nothing.
