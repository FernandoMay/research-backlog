CRL publication gate
==============================================================================
  PASS  1a gate runs on the audit branch, not the forbidden one
  PASS  1b remote main untouched at the pre-audit baseline
  PASS  1c working tree clean
  PASS  2 every audit commit exists in the history
  PASS  2b every audit commit is an ancestor of HEAD
  PASS  3 RF1-RF5 falsifiers green from a clean state
  PASS  3b F2 remains red as a retained finding
  PASS  3c F2's falsifier log is committed, not overwritten
  PASS  4a artifact carries full provenance
  PASS  4b no wall-clock field in the artifact
  PASS  4c artifact digest recorded for the record
  PASS  5a no manuscript modified
  PASS  5b E1 corpus untouched
  PASS  5c the published 0.02 was not turned into a target
  PASS  6a every disposition survives in the adjudication document
  PASS  6b completion=100% appears in no assertion as a resilience benefit
  PASS  6c the adjudication states the repaired 100% is not positive evidence
  PASS  6d the metric-semantics defect is retained as NEW EXPERIMENT REQUIRED
  PASS  6e the manuscript's accurate self-limitations are recorded
==============================================================================
19/19 gate checks passed

CRL is closed. Recorded as a positive result rather than another defective
package: the mechanism has causal access and the configuration can activate
it, but the published outcome has insufficient resolution to demonstrate
the benefit one might want to infer from it. The manuscript already states
several of these limitations correctly.
