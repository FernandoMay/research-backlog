==============================================================================
Q4 falsifier — experimental controls: pairing, dispersion, mitigation
property: each experiment compares algorithms on equal footing, and every
         strategy and baseline is named for what it actually does
==============================================================================

  [INFO] positive control — a properly paired harness built here:
         QAOA and WalkSAT receive the same instance in every trial: True
         so F1 is measuring something real.

  [INFO] F1 pairing — same instances for QAOA and WalkSAT?
         exp_noise hard-codes n=12, m=60 and runs 6+6 trials at up to noise 0.50
         a full faithful replay of all four experiments is out of scope for one falsifier,
         so F1 is evaluated by intercepting gen_3sat during a bounded replay of the
         instance-allocation logic only.
         QAOA instances   : 4 distinct
         WalkSAT instances: 3 distinct
         shared between arms: 0
  [FAIL] F1 the arms are NOT paired. exp_noise draws a fresh instance for the QAOA
         loop and then a different fresh instance for the WalkSAT loop, so the two
         curves are averages over disjoint instance sets. Any gap between them
         mixes the algorithm difference with instance difficulty.

  [INFO] F2 the Random baseline's evidence base:
         `rand_m` is computed as sat_ratio(random_bits, cl) over 100 draws,
         where `cl` is whatever instance the loop variable last held.
         instances reaching that expression with no arm attribution: 1
  [FAIL] F2 the Random baseline is computed from a single instance. All 100 draws
         share one clause set, so the reported baseline has an effective sample
         size of 1 instance x 100 assignments, not 100 independent problems.

  [INFO] F3 exp_depth dispersion:
         repeats the instance inside the depth loop: False
         reports any dispersion for the sat column: False
  [FAIL] F3 each depth level is a single instance with a single run. The reported
         SAT value per p carries no dispersion estimate, so the depth curve in fig3
         cannot distinguish a real p-dependence from one instance's draw.

  [INFO] F4 does 'zne' mitigate, or rename a smaller noise rate?
         factors = {'none':base_noise, 'zne':base_noise*0.3, 'readout':base_noise*0.5, 'both':base_noise*0.15}
=== Experiment 4: Mitigation ===
  none: 0.948+-0.044
  zne: 0.956+-0.054
  readout: 0.904+-0.076
  both: 0.978+-0.018
         every line in exp_mitigation that mentions the strategy name:
           strategies = ['none', 'zne', 'readout', 'both']
           for strat in strategies:
           ef = factors[strat]
           res['s'].append(strat)
           print(f"  {strat}: {np.mean(qs):.3f}+-{np.std(qs):.3f}")
         strategies the function iterates: ['none', 'zne', 'readout', 'both']
         distinct noise values that reached the circuit: [0.0225, 0.045, 0.075, 0.15]
         distinct values of factors[...]:                 [0.0225, 0.045, 0.075, 0.15]
         the two sets are identical: True
         any extrapolation, scale sweep or fit performed: False
         the strategy name reaches the simulator only as a noise rate: True
         control: plain noise 0.1500 -> SAT 0.9815; a genuine readout correction -> SAT 0.9877
         the genuine correction differs from plain noise scaling: True
  [FAIL] F4 the strategy name is inert. The only strategy-dependent quantity that
         reaches the simulator is a noise rate, so the four bars in fig4 are one
         sweep relabelled. ZNE is zero noise EXTRAPOLATION by definition; here it
         is 'assume less noise', which cannot remove bias — it only lowers the
         noise the simulator was told to apply. 'readout' halves the same parameter
         with no measurement model, so the two 'independent' techniques are one
         parameter sweep, and 'both' is their product.

  [INFO] search budget per arm, as configured:
         QAOA    : ['30'] circuit evaluations per instance (p=2, 40 random candidates per call in optimize_qaoa)
         WalkSAT : ['2000'] local flips per instance
         these budgets differ by roughly two orders of magnitude; recorded as a
         confound of the comparison, not adjudicated as a defect here.
==============================================================================
FAILED: F1-arms-not-paired, F2-baseline-single-instance, F3-depth-no-dispersion, F4-mitigation-is-a-relabelled-noise-sweep

Implementation fact: arms are unpaired in exp_noise, the Random baseline rests on a
single instance, exp_depth reports one run per depth with no dispersion, and the
mitigation strategies are a relabelled noise sweep.
Claim correspondence: NOT ADJUDICATED. What the manuscript concludes from these
experiments is Q6.

## Falsifier defects found while building Q4 (all retained)

1. **The positive control compared the wrong two things.** The harness that
   pairs arms correctly reported `False`. The tuple was built as
   `(key, qaoa_score, walk_score)` and unpacked as if the second element were a
   key, so an instance key was compared against a SAT ratio. A control that
   fails for the wrong reason is as useless as one that fails for the right one.
2. **F4's first behavioural test was vacuous.** Both arms were seeded with
   `1000 + len(vals)`, identical in each branch, so both executed the same
   computation and trivially agreed. The result `0.9815 ± 0.0185` on both sides
   was an artefact of the seeding, not evidence of equivalence.
3. **Runtime attribution put all four strategies on one label.** `cur` was
   assigned before calling `exp_mitigation` and retained the last loop value, so
   all four observed noise values were attributed to `both`. Replaced with an
   exhaustive source check — every occurrence of the loop variable — plus the
   set of noise values that actually reached the circuit. A sample attributed by
   guessing is weaker than an exhaustive check over the source.
4. **The strategy list was parsed from the loop header.** The function assigns
   `strategies = [...]` and then runs `for strat in strategies:`. Parsing the
   loop header recovered the single token `'strategies:'`, making every
   per-strategy assertion vacuous.
5. **Bookkeeping was counted as computation.** The filter missed
   `res['s'].append(strat)`, so a name that is only recorded and printed
   appeared computationally active. Recording a label is not using it.

## Numbers in this log must not be compared to any published figure

The `=== Experiment 4: Mitigation ===` block inside F4 is the package's own
`exp_mitigation` running under a patched `gen_3sat` that ignores the requested
size and returns a 6-variable, 27-clause instance. The values
0.948 / 0.956 / 0.904 / 0.978 are therefore outputs of a *different experiment*
on *smaller instances*. They exist here only to confirm that the function
executes and that exactly four distinct noise rates reach the circuit. They are
not a reproduction of the package's fig4 and must never be presented as one.

## Disposition boundaries

- Implementation fact: unpaired arms in exp_noise; Random baseline on one
  instance; exp_depth with one run per depth and no dispersion; strategy names
  inert.
- Scientific interpretation: NOT adjudicated. A budget asymmetry between QAOA and
  WalkSAT is a legitimate design question, not a defect; it is recorded as a
  confound only.
- Claim correspondence: NOT ADJUDICATED. fig4's four bars being labelled
  'none / zne / readout / both' is exactly the kind of vocabulary claim that Q6
  must examine.
