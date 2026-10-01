property: an objective value must depend on the chromosome it
         purports to evaluate
==============================================================================
  [PASS] T1 a chromosome can be evaluated on the environment
  [PASS] T2 negative control: the same chromosome reseeded gives identical objectives (13.9611 ms)
  [PASS] T3 different chromosomes give different measured objectives under the same seed
           A (np.float64(0.7), np.float64(0.2), np.float64(0.1)) route=0 -> latency 13.9611 ms
           B (np.float64(0.1), np.float64(0.2), np.float64(0.7)) route=2 -> latency 15.0000 ms
  [PASS] T4 the difference is in a raw measured objective, not only in the score
  [PASS] T5 the dependence is routed: the chromosome selects strategy 0 vs 2, and compute_latency_ms
           measures that strategy against the environment
  [INFO] T6 failures   0% ( 0 sats) -> latency   13.9611 ms  [finite]
  [INFO] T6 failures   5% ( 3 sats) -> latency   13.9611 ms  [finite]
  [INFO] T6 failures  10% ( 6 sats) -> latency   13.9611 ms  [finite]
  [INFO] T6 failures  20% (12 sats) -> latency   13.9611 ms  [finite]
  [INFO] T6 failures  30% (18 sats) -> latency  240.0000 ms  [sentinel]
  [INFO] T6 failures  40% (24 sats) -> latency   13.9611 ms  [finite]
  [INFO] T6 failures  50% (30 sats) -> latency   13.9611 ms  [finite]
  [PASS] T6 the measured latency is not invariant across environments (2 distinct outcomes over the sweep)
  [NOTE] T6 latency never moved at any finite failure fraction: the shortest-path metric has no dynamic range in
         this environment. Recorded as a separate finding, outside row R1's scope.
==============================================================================
PASSED: the objective depends causally on the chromosome
