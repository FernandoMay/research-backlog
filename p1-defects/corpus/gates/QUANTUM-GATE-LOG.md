==============================================================================
Quantum audit release gate
asserts: every falsifier is RED and every falsifier's positive control still PASSES
==============================================================================
  [OK     ] Q1 test_measurement_oracle.py
            exit=1  FAIL=2  PASS=1

  [OK     ] Q2 test_optimizer_semantics.py
            exit=1  FAIL=2  PASS=1

  [OK     ] Q3 test_noise_channel.py
            exit=1  FAIL=4  PASS=1

  [OK     ] Q4 test_experimental_controls.py
            exit=1  FAIL=4  PASS=2

  [OK     ] Q5 test_gap_semantics.py
            exit=1  FAIL=1  PASS=1

  [OK     ] Q6 test_claim_correspondence.py
            exit=1  FAIL=1  PASS=1

==============================================================================
GATE PASSED — 6 falsifiers, all RED, all with a working positive control

This is not a statement about the package's scientific merit, and not a
statement about whether the manuscript is publishable. It says the audit
instruments are intact and the recorded defects are still present.
