property: every entry point completes, and no published figure
         predates the artifact it depicts
==============================================================================
  fig5_scenario_scale.png
  fig6_failure_sweep.png
  [FAIL] F1 generate_extended_figures raised NameError: name 'abl_order' is not defined
         The extended experiment writes its artifact before it draws
         its figures, so a run that crashes here still leaves a fresh,
         correct artifact behind it. That is why row R2's check -- the
         artifact regenerated and no number moved -- could not see this.
  [FAIL] F1 figures not produced: fig7_ablation.png
  [INFO] F2 committed lineage:
         fig5_scenario_scale.png  37aa3f2  (OLDER than artifact)
         fig6_failure_sweep.png  37aa3f2  (OLDER than artifact)
         fig7_ablation.png  f81f097  (OLDER than artifact)
  [FAIL] F2 3 committed figure(s) are not derived from the same
         execution as data/metrics_extended.json: fig5_scenario_scale, fig6_failure_sweep, fig7_ablation
         These were drawn by an earlier run and committed alongside newer
         numbers, so the figure and the artifact beside it disagree about
         which execution produced them. Neither is wrong on its own; the
         pairing is.
==============================================================================
FAILED: F1-figure-generation-crashes, F1-missing-figures, F2-figure-predates-artifact

Seven green falsifiers and a crashing pipeline were both true at the same
time, because the suite measures and never renders. This row closes that
seam. It makes no scientific claim.
