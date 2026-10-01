property: candidates are updated from objective feedback, or the
         search is random and the objective only ranks
==============================================================================
  [INFO] the optimiser's source mentions a gradient-style rule: False
  [INFO] Q2-F1 dependency between successive candidates:
         40 candidate pairs captured by instrumenting numpy (40 iterations)
         mean corr(candidate_t, candidate_t+1)      +0.1399
         objective range over the search           0.3629 to 1.3344
  [FAIL] Q2-F1 successive candidates are independent of both the incumbent and the objective.
         Each draw is fresh from the RNG, so there is no update rule: the objective is
         computed and then used only to pick a winner.
  [INFO] Q2-F2 alter ONLY the objective used for selection:
         candidate sequences identical under the altered objective: True
         selected winner changed: False
         plain winner energy 0.446488   reversed 0.446488
         the objective was REVERSED, which changes the ranking by construction
  [FAIL] Q2-F2 the objective changed neither the sequence nor the winner; the
         optimiser did not use it at all
  [INFO] positive control — a deliberately simple objective-directed optimiser:
         control trajectory length                  25
         mean cos(candidate_t, candidate_t+1)      +0.9793
         control objective 1.183214 -> 0.318479 (-0.864735)
  [PASS] positive control: an objective-directed optimiser reaches +0.98 consecutive
           similarity and lowers the energy, so this falsifier can detect an update rule
           when one exists. F1 and F2 are therefore informative.
==============================================================================
FAILED: Q2F1-no-update-rule, Q2F2-objective-unused

Implementation fact: candidate generation is independent of the objective.
Scientific interpretation: random search is a legitimate algorithm.
Claim correspondence: unresolved until Q6 maps what the manuscript calls this.
No disposition is assigned here.

## Falsifier defects found while building Q2 (all retained, none cleaned)

1. **Contract violation in the intervention wrapper.** The first `biased_qaoa`
   returned a three-tuple to carry the objective bias, but `optimize_qaoa`
   unpacks two values from `qaoa_run`. The test raised before measuring anything.
2. **Candidate list iterated as pairs.** The recorder appends every draw in call
   order, producing a flat list (gamma_0, beta_0, gamma_1, ...). Iterating it as
   `(g, b)` unpacked each two-element draw into two scalars and failed on
   zero-dimensional arrays.
3. **F1 measured an undefined quantity.** It correlated a length-4 candidate
   vector against a scalar energy. `corrcoef` rejected it, correctly. A
   correlation between a candidate and the objective was never the right
   instrument; whether the objective steers is an intervention question, which is
   why F2 exists.
4. **F2's intervention could not have failed.** The original bias added a large
   constant to the cost Hamiltonian. That shifts every candidate energy by the
   same amount, so the ranking — and the winner — are unchanged by construction.
   A test that passes for a reason that has nothing to do with the hypothesis is
   not evidence. The intervention now REVERSES the objective, which changes the
   ranking by construction. F2's RED result below is only meaningful because of
   this change.
5. **The positive control could not pass.** `directional()` built a perturbed copy
   named `probe` and then evaluated the unperturbed `th` twice, so every gradient
   entry was exactly zero and the optimiser could not move. A control that cannot
   pass is indistinguishable from one that cannot fail. The results in this log
   were rejected until the control was repaired, per the standing rule that a
   falsifier whose own control fails proves nothing.

## Why F1 is not the load-bearing test

F1 shows candidates are mutually uncorrelated. That is *consistent* with
independent sampling but does not prove it: a deterministic gradient step with a
large step size can also decorrelate successors. F2 is load-bearing because it
intervenes on the selection signal alone. Under a reversed objective the candidate
sequence stays bit-identical AND the winner is unchanged, which is only possible
if the objective is consulted after generation has already finished.

## Disposition boundaries

- Implementation fact: candidate generation is independent of the objective;
  the objective only ranks already-generated candidates.
- Scientific interpretation: random search is a legitimate algorithm. Nothing
  here is a defect on its own.
- Claim correspondence: NOT ADJUDICATED. What the manuscript calls this is the
  subject of Q6. No label is promoted to a disposition on the strength of this
  falsifier.
