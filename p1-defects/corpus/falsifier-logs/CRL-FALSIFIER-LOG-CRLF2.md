property: the published anomaly score is reconstructible from an
         identified execution of the repository as committed
==============================================================================
  [INFO] F2a reconstruct from the actual run, not from a copied formula:
           run_experiment avg_anomaly_score = np.float64(0.03)  -> printed .4f = 0.0300
           cycles_run 2, completed 20/20
  [PASS] F2a the printed value is the mean of the per-cycle scores returned by run_cycle
  [INFO] F2b perturb the anomaly's input and re-measure:
           20 tasks -> 0.0300
           10 tasks -> 0.0150
  [PASS] F2b changing the workload moves the anomaly score, so the metric is causally
           connected to the run rather than being a constant
  [INFO] F2c silent definitions of anomaly in one run:
           per-cycle scores reported by run_cycle : ['0.0000', '0.0600']
           observer.anomaly_scores list           : ['0.0600']
           mean of per-cycle values                 : 0.0300
           mean of the observer's own list          : 0.0600
  [FAIL] F2c the run carries TWO averaging populations: 2 per-cycle values against
         1 entries in the observer's own list. They disagree
         (0.0300 against 0.0600), and the difference is structural: detect_anomaly returns 0.0
         before two states exist and never appends that value, so the observer's list
         excludes the structural zero while the reported mean includes it. Neither name
         says which population it means.
  [INFO] F2d is 0.02 reachable from the committed code at all?
           200 seeds: min 0.0187 max 0.5399
           seeds yielding exactly 0.02: 5
           the repository's own pinned seed 20260909 yields 0.0300
  [FAIL] F2d the published value IS reachable from the committed code (5 of 200
         seeds), but the manuscript records no seed, no configuration and no artifact for
         the execution that produced it, and the repository pins 20260909, which
         yields 0.0300. This is a provenance gap, not a wrong
         number: the code can emit the published value and nothing in the repository
         identifies which run did. Not CONTRADICTED -- the value is not outside the code's
         range. NOT VERIFIED, because no lineage connects the publication to an execution.
         No attempt is made to move the output toward 0.02; the historical value is not
         a target and matching it would prove nothing.
==============================================================================
FAILED: F2c-two-silent-definitions, F2d-published-value-unlineaged

Disposition: NOT VERIFIED / PROVENANCE GAP. Not CONTRADICTED. The value is
inside the code's range, the repository stores no artifact, and the
manuscript records no execution that would let a reader identify which run
produced it. The absence is the finding.
