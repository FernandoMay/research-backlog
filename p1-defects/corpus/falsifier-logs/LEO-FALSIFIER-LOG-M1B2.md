property: every arm publishes the latency its own routing decision
         produced, untransformed
==============================================================================
  [INFO] F1 compute_latency_ms was called 12 times over 4 rounds
         strategies passed: [0, 2]
  [PASS] F1 every arm measures independently: three calls per round for three arms
  [FAIL] F2 the offline arm's published latency is a transform of a measurement, not a measurement.
           factor source in the evaluation loop: present
           The optimiser's own weight is being used as a multiplier on
           somebody's latency. That factor is below 1 for every weight vector that
           exists, so the arm's advantage is a property of the multiplier.
  [PASS] F3 perturbing the arm's weights moves the route it requests: strategy 2 -> 0
           and moves the latency it reports: 11.4744 -> 15.1864 ms
           The arm's number follows its own decision, which is what a
           measurement does and a multiplier cannot.
  [INFO] F4 same-policy control: both arms requested strategy 0 but reported 13.6269
           and 15.6561 ms. Worth a look, and not asserted here.
==============================================================================
FAILED: F2-published-value-is-transformed

No historical or current figure is a target here. The criterion is the
measurement path, and the outcome may be that the offline arm's
advantage disappears -- which would be the result the repair exists to
reveal, not a surprise to be corrected.
