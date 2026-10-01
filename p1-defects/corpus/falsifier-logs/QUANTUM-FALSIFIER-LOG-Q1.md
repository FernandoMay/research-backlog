property: the readout is a measurement or it is a labelled oracle
==============================================================================
  [INFO] published readout: best_sat_from_state(state, H, n, clauses)
         it accepts no shot count at all, so a shot count cannot influence it by construction
  [INFO] positive control — a Born sampler over the SAME distribution:
         S=1     max-probability across 40 repeats: 1.0000 to 1.0000   (spread 0.0000)
         S=10    max-probability across 40 repeats: 0.2000 to 0.7000   (spread 0.5000)
         S=100   max-probability across 40 repeats: 0.2100 to 0.3500   (spread 0.1400)
         S=1000  max-probability across 40 repeats: 0.2250 to 0.2880   (spread 0.0630)
  [PASS] positive control: a genuine measurement varies across repeats, so the
           property is detectable in this state
  [INFO] Q1-F1 repeated invocation of the published readout:
         40 invocations -> 1 distinct value(s): [1.0]
  [FAIL] Q1-F1 the readout returned an identical value on all 40 invocations.
         A Born measurement with any finite shot count varies with the draws it makes;
         this cannot, because no sampling occurs in the path. The value is derived
         from the exact probability distribution instead.
  [INFO] Q1-F2 perturb only the requested shot count:
         S=1     oracle -> 1.0000   a real measurement returned 14 distinct argmax outcome(s)
         S=10    oracle -> 1.0000   a real measurement returned 10 distinct argmax outcome(s)
         S=100   oracle -> 1.0000   a real measurement returned 2 distinct argmax outcome(s)
         S=1000  oracle -> 1.0000   a real measurement returned 1 distinct argmax outcome(s)
  [FAIL] Q1-F2 the shot count has no behavioural effect on the readout: identical for
         S = 1, 10, 100, 1000. Over the same distribution a genuine
         measurement returns different outcomes at every S, so the difference is the
         readout's, not the distribution's.
         The readout is an exact oracle. That is a legitimate simulator choice; it is
         a defect only if the manuscript presents it as measurement behaviour, which is Q6.
==============================================================================
FAILED: Q1F1-no-sampling-variability, Q1F2-shots-have-no-effect

Implementation fact: the readout is an exact probability oracle.
Scientific interpretation: that may be a legitimate simulator design.
Claim correspondence: unresolved until Q6 maps what the manuscript says
it measures. No disposition is assigned here.

Audit correction, recorded so it cannot reappear as a defect:
qaoa_run returns (state, H). An earlier audit read the cost Hamiltonian
as the state and reported a second normalisation defect that does not
exist. That was the auditor's error.
