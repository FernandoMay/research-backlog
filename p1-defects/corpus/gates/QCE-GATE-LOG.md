==============================================================================
QCE audit release gate
  DESTINATION -> COMMIT/LINEAGE -> REPRODUCTION -> H3 controls ->
  H4 controls -> ADJUDICATION -> NON-FINDING NEGATIONS -> PROHIBITIONS
  -> CLEAN TREE
==============================================================================

  --- DESTINATION ---
  [OK     ] audit branch, not the default: fix/qce-audit-sweep
  [OK     ] baseline 97ed1cb is an ancestor: True
  [OK     ] remote master untouched (still 97ed1cb): True  97ed1cb

  --- COMMIT / LINEAGE ---
  [OK     ] commits on the audit branch: 5
             618f9f5 test(qce): gate pattern alignment and clean-tree scope
             3f24250 docs(qce): frozen claim-chain adjudication and release gate
             67cccd9 test(qce): ablation reconstructibility falsifier — neither row has a code path
             ca410b4 test(qce): causal participation falsifier — the named mechanisms do not participate
             7ef2c66 docs(qce): inventory and lineage — implementation facts only

  --- REPRODUCTION ---
  [OK     ] figures/metrics.json identical to the committed artifact: True

  --- QCE-1 CONTROLS ---
  [OK     ] QCE-1 test_causal_participation.py  exit=1 FAIL=3 PASS=2 control-mentions=3

  --- QCE-2 CONTROLS ---
  [OK     ] QCE-2 test_ablation_reconstructibility.py  exit=1 FAIL=2 PASS=2 control-mentions=2

  --- CLAIM-CHAIN ADJUDICATION ---
  [OK     ] mechanism/magnitude split preserved for NoSafety
  [OK     ] reliability differs by a factor of seven is stated
  [OK     ] NoRL stated as identity failure, not reproduction failure
  [OK     ] attribution of the 13.8% separated from its rounding
  [OK     ] failures are not summed
  [OK     ] auditor records present
  [OK     ] git race recorded without force-push

  --- NON-FINDING NEGATIONS ---
  [OK     ] N1 the Chinese paper DOES disclose the mechanism
  [OK     ] N2 gamma unread does NOT mean the predictor is disconnected
  [OK     ] N3 the optimizer DOES minimise its cost Hamiltonian
  [OK     ] N4 a PNG byte mismatch is NOT a data contradiction
  [OK     ] N5 the 0.963554 / 354.0291 observation is NOT a result
  [OK     ] N6 the i01 25/60-sample result is NOT applicable to QCE

  --- PROHIBITIONS (each verified by REJECTING its violation) ---
  [OK     ] P2 the exploratory observation (0.963554 / 354.0291 mW) must NOT appear in the claims matrix; the reconstructed NoRL values legitimately may
  [OK     ] P3 gamma=0 must not be used as the NoRL intervention
             (claims matrix extracted: 5341 chars; the reconstructed NoRL values are permitted there and were checked not to be the exploratory ones)
  [OK     ] P1 a printed phrase must not be accepted as evidence
  [OK     ] P2 a historical published number must not be a repair target
  [OK     ] P3 gamma=0 must not substitute for NoRL
  [OK     ] P4 absence in the current repo must not prove historical absence
  [OK     ] P5 the 0.9636 / 354 mW observation must not be a paper result
  [OK     ] P6 the Chinese non-finding must not rest on English searches
  [OK     ] P8 a wrong-corpus search is not evidence of absence
  [OK     ] P7 a PNG mismatch must not be a data contradiction when the JSON is identical

  --- CLEAN TREE ---
  [OK     ] working tree clean: True

==============================================================================
GATE PASSED
  destination, lineage, reproduction, falsifier controls, adjudication,
  non-finding negations, prohibitions and a clean tree all verified.

This asserts nothing about scientific merit or publishability. It says the
audit instruments are intact, the findings have not been dropped, the
non-findings have not been promoted, and the prohibitions still bind.
An audit that cannot do all four is a second source of unverified claims.

NO MANUSCRIPT TEXT HAS BEEN EDITED. NO NUMBER HAS BEEN CORRECTED.
NO REPAIR HAS BEEN STARTED.
