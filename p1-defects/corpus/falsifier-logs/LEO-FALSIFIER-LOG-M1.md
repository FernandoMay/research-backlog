property: the experiment's parameters reach the mechanisms, and the
         metrics distinguish the phenomena the paper interprets
==============================================================================
  [FAIL] M1-B resilience is one measurement appended to three lists.
           compute_resilience is called once per round (1 call site in the evaluation loop) and its
           single result is appended to baseline_resilience, nsgaii_resilience and hybrid_resilience
           alike. The three arms cannot differ in resilience, so an identical
           avg_resilience_pct is structural, not an empirical finding about the methods.
           signature: compute_resilience(env) -- it never receives a router,
           so no causal path from routing to resilience exists to be tested.
  [FAIL] M1-B2 the baseline and the NSGA-II arm are the same measurement.
           bl_lat = compute_latency_ms(env2.snr_matrix, active_mask, 0)
           ns_lat = compute_latency_ms(env2.snr_matrix, active_mask, 0)
           Both call compute_latency_ms with route_type 0, so the two values are
           identical in every round before anything else happens.
           The arm's published latency is then rescaled:
           nsgaii_latencies.append(ns_lat * (0.7 + 0.3 * best_policy['weights'][0]) if np.isfinite(ns_lat) else 55.0)
           so the NSGA-II latency is the Dijkstra latency multiplied by a factor
           derived from the optimiser's own weight. That factor is below 1 for
           every weight vector that exists, so the arm's latency advantage is a
           property of the multiplier, not of any routing decision.
  [INFO] M1-A failure-rate sweep, latency classified per point:
           0% failures (60 active) -> latency   15.5665 ms [ observation]  resilience  79.69%
           5% failures (57 active) -> latency   15.5665 ms [ observation]  resilience  82.81%
          10% failures (54 active) -> latency   15.5665 ms [ observation]  resilience  82.81%
          20% failures (48 active) -> latency   15.5665 ms [ observation]  resilience  79.69%
          30% failures (42 active) -> latency       inf ms [disconnected]  resilience  79.69%
          40% failures (36 active) -> latency       inf ms [disconnected]  resilience  85.94%
          50% failures (30 active) -> latency   15.5665 ms [ observation]  resilience  78.12%
          60% failures (24 active) -> latency       inf ms [disconnected]  resilience  75.00%
          70% failures (18 active) -> latency       inf ms [disconnected]  resilience  89.06%
          80% failures (12 active) -> latency       inf ms [disconnected]  resilience  85.00%
  [PASS] M1-A failure rate reaches resilience: 14.0625 points of movement across the sweep
  [INFO] M1-A latency span across observations: 0.0000 ms (5 observations, 5 disconnections)
         Latency is flat over this range. That is a statement about the experimental
         range and the graph density, not yet about the metric: see M1-B2.
  [INFO] M1-C sentinel check:
  [FAIL] M1-C the evaluation loop substitutes a constant for a disconnected graph,
         so a disconnection is averaged into the latency statistic as if it were an
         observed latency. There is no category separating the two:
           baseline_latencies.append(bl_lat if np.isfinite(bl_lat) else 60.0)
           nsgaii_latencies.append(ns_lat * (0.7 + 0.3 * best_policy['weights'][0]) if np.isfinite(ns_lat) else 55.0)
           hybrid_latencies.append(hy_lat if np.isfinite(hy_lat) else 55.0)
         The constants are 60.0 and 55.0 ms, not the 240.0 ms sentinel, so they
         are ad hoc rather than traceable to anything measured.
  [INFO] M1-control synthetic routing perturbation:
         route 0: latency  11.0334 ms  resilience  79.69%
         route 1: latency  16.1626 ms  resilience  79.69%
         route 2: latency  15.8255 ms  resilience  79.69%
  [PASS] M1-control routing reaches latency: 5.1291 ms of separation across strategies
  [FAIL] M1-control routing does NOT reach resilience. Three different strategies,
         same environment and seed, all yield 79.6875%. This is the decoupling
         itself: the metric cannot see routing, so a flat avg_resilience_pct
         across methods is guaranteed regardless of what the methods do.
==============================================================================
FAILED: M1-B-resilience-broadcast, M1-B2-baseline-is-nsgaii, M1-C-sentinel-not-categorised, M1-control-resilience-decoupled

No environment, metric or threshold is changed by this file. M1 is left
RED so that the repair can be chosen among M1-R1 (change the environment),
M1-R2 (change the metric) and M1-R3 (change the experimental scenario),
rather than assumed.
