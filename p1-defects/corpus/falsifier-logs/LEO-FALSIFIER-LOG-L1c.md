property: an artifact identifies the code, the environment, and the
         effective per-scenario configuration that produced it
==============================================================================
  [FAIL] F1 the artifact carries no provenance block
         It records scenario results only. Nothing in it identifies
         which code, which dependency state, or which weight vector
         produced each scenario, so two different runs of this
         experiment are indistinguishable after the fact.
         Present top-level keys: ['ablation', 'revision_note', 'scenario_failure', 'scenario_scale']
==============================================================================
FAILED: F1-no-provenance
