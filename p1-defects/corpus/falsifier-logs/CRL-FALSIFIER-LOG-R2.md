property: the published configuration exercises the mechanism, with
         matched doses and a reproducible artifact
==============================================================================
  [INFO] RF1 is there an entry point that delivers targeted stress?
  [FAIL] RF1 no stressed experiment exists. The package offers run_experiment (p=0.05)
         and run_comparison (p=0.20), both injecting uniformly at random over active
         agents, and neither targets an agent holding a ready node. The manuscript at L151
         states the repository includes a stressed mode; it does not, which was recorded
         as claim C5 in the inventory.
  [INFO] RF2 are the doses matched between the two arms?
         not evaluable without RF1
  [INFO] RF3 does the control arm ever run the recovery path?
         not evaluable without RF1
  [INFO] RF4 does a provenance-carrying artifact exist?
  [FAIL] RF4 no artifact exists at data/resilience_experiment.json. Row F2 established
         that the published 0.02 is reachable from this code under 5 of 200 seeds while the
         repository pins 20260909 giving 0.0300, and that nothing connects the
         publication to either execution. Results go to stdout, so no number is lineaged.
  [INFO] RF5 does the published entry point put the stressor in the window?
  [WARN] RF5 the published run_experiment does not report how many cycles in which the
         guard withheld a completion. Without that, a reader cannot tell whether the
         mechanism was exercised at all.
==============================================================================
FAILED: RF1-no-stressed-entry-point, RF2-not-evaluable, RF3-not-evaluable, RF4-no-artifact, RF5-published-entry-not-instrumented

R2 repairs activation only. It does not re-demonstrate causality -- row
F1 established that -- and it does not manufacture an effect: no
magnitude is required, only that the stressor reaches the guard with
matched doses in a single differing condition, and that the result lands
in an artifact rather than on stdout.
