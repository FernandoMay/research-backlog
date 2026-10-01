property: a latency statistic is computed over observations, and a
         disconnection is named rather than substituted
==============================================================================
  [PASS] C1 classifier present: 17.5 -> 'OBSERVATION', inf -> 'DISCONNECTED'
  [PASS] C1 unexpected outcome nan raises rather than being classified
  [PASS] C1 unexpected outcome negative raises rather than being classified
  [PASS] C1 unexpected outcome a string raises rather than being classified
  [PASS] C1 unexpected outcome a dict raises rather than being classified
  [PASS] C2 [15.0, 17.0, disconnected] aggregates to 16.0000 ms, the mean of the two observations
  [PASS] C2 2 disconnected round(s) exercised, none carrying a number
  [PASS] C2 the disconnection marker contributes to n_disconnected and to nothing else
  [PASS] C3 all-disconnected reports an explicit non-result: LatencySummary(mean_ms=None, n_observations=0, n_disconnected=3)
           observations=0, disconnected=3
  [PASS] C3 disconnections however expressed -- None or inf -- yield no statistic
  [INFO] C4 baseline  6 observations, 0 disconnections over 6 rounds
  [INFO] C4 nsgaii    6 observations, 0 disconnections over 6 rounds
  [INFO] C4 hybrid    6 observations, 0 disconnections over 6 rounds
  [PASS] C4 preservation: baseline publishes 15.4313 ms, identical to the mean of its observations
  [PASS] C4 preservation: nsgaii publishes 15.9775 ms, identical to the mean of its observations
  [PASS] C4 preservation: hybrid publishes 14.5324 ms, identical to the mean of its observations
  [INFO] C5 the _evaluate_chromosome sentinel is 240.0 ms and is still present
         It belongs to the optimiser's evaluator, a different path from the
         evaluation loop, and this row does not unify them. Not asserted:
         proving they mean the same thing would be a claim this row cannot
         support, and the two are kept distinguishable.
==============================================================================
PASSED: disconnections are named, not averaged in
