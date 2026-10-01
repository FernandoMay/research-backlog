property: the experiment has causal access to the property it claims
         to measure
==============================================================================
  [INFO] F1a the package's two arms exactly as written, across p_fail:
             p | CRL arm (guarded+cycle)    | baseline (unguarded, no cycle)
          0.05 | 100.00% cyc4   fail0 mods0   | 100.00% cyc4   fail0
          0.20 | 100.00% cyc4   fail0 mods0   | 100.00% cyc4   fail0
          0.50 | 100.00% cyc4   fail0 mods0   | 100.00% cyc4   fail0
          0.90 | 100.00% cyc4   fail3 mods6   | 100.00% cyc4   fail3
          1.00 | 100.00% cyc6   fail6 mods11  | 100.00% cyc4   fail4
  [PASS] F1a the ceiling is reproduced: both arms report an identical completion at every
           failure rate, including p=1.00. This is the effect the manuscript itself names at
           L150, so the defect is real but the paper is not unaware of it.
  [INFO] F1b fail the agent assigned to a ready node immediately before the marking loop,
         so the guard's decision decides that node's outcome:
         guarded   completion  55.00%  failures injected 200  cycles 200
         unguarded completion 100.00%  failures injected 3  cycles 4
  [PASS] F1b the guard has causal access to the reported metric: an intervention that
           reaches the guard changes the outcome by 45.00%.
           The mechanism the paper credits with resilience is connected to the number it
           reports. The ceiling in F1a is therefore a property of the stressor never
           arriving during the window in which the guard acts -- not evidence that the
           mechanism is inert.
  [INFO] F1c negative control: two arms identical by construction must agree:
  [PASS] F1c identical arms agree exactly (100.00% guarded, 100.00% unguarded)
           The instrument therefore reports a difference only when one exists, and the F1b
           result is about the guard rather than about the harness.
==============================================================================
PASSED: the experiment has causal access to what it reports
