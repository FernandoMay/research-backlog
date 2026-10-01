property: each ablation arm receives exactly the treatment its name
         declares, and the optimiser's causal route is observable
==============================================================================
  [PASS] F1 ql completes with nsga2_optimize replaced by a raiser;
           the Q-learning-only arm does not consume the offline prior
  [PASS] F2 ga completes without re-running nsga2_optimize; it is a
           fixed-mode selector, not a second evolutionary search
  [PASS] F3 hybrid consumes the prior through its argument rather than
           by calling the optimiser itself; the route is the weights
           kwarg that run_extended supplies from get_weights()
  [PASS] F4 perturbing the prior moves the hybrid: [.90,.05,.05] -> 17.86 ms / 93.3%, [.05,.05,.90] -> 21.02 ms / 100.0%
           causal route from the optimiser's output to the arm's
           result is observable
  [PASS] F5 one label source, consistent across figures; tick labels derived
           rather than hardcoded. ga is published as a treatment name, which
           F4 confirms it earns: it consumes the prior and applies a fixed mode.
  [PASS] F6 the ql arm's result is invariant to whether the optimiser
           ran first; no accidental coupling through the RNG stream
  [INFO] F7 declared effective inputs per arm: {'ga': 'optimizer-derived', 'ql': 'not consumed', 'hybrid': 'optimizer-derived'}
         F1, F2 and F6 above establish these empirically rather than by
         reading the call sites. No arm's result is compared to a
         previously published number anywhere in this file.
==============================================================================
PASSED: the ablation is identifiable
