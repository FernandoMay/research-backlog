property: the primary artifact identifies the code and environment
         that produced it, and is coupled to the extended one
==============================================================================
  [PASS] F1 all 7 required provenance fields present
  [PASS] F1b populated and well-formed
  [PASS] F2 shared environment block present with 8 field(s): architecture, dependency_versions, platform, python_implementation, python_version, seed, source_commit, source_dirty
  [PASS] F3 no wall-clock field in the artifact; reproducibility is testable
  [FAIL] F4 the extended artifact has no matching `environment` block, so the two
         cannot be compared. L1c predates this coupling; the extended
         side has to be brought to the same shape.
  [PASS] F5 all 4 mutations break provenance equivalence:
           source_commit
           dependency_versions[matplotlib]
           seed
           configuration[altitude_km]
  [PASS] F6 recorded source_commit c12dbf58c9f9 is reachable in this history (HEAD c12dbf58c9f9)
  [WARN] F6 the tree was dirty at generation time; source_commit records HEAD, not the exact bytes
==============================================================================
FAILED: F4-extended-no-environment
