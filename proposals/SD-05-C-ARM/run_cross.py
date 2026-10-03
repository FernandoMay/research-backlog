"""
THE CROSS — candidate C against declared and derived impact.

Frozen and not to be touched during the run:
    k = 6.0334, thresholds {0.30, 0.65, 0.85}, V, the case composition,
    the impact classification, the I_derived rule, 19f4e8e, and the
    prediction frozen at 7e22541.

The case definitions are imported from the run-1 snapshot rather than
retyped, so composition cannot drift. The historical cell is NOT re-run.

If execution differs from the frozen prediction, the adjudication order is:
does it contradict the proven range -> CONTRADICTS_PROVEN_RANGE; then is it
an execution or instrument fault; only if it survives both is it a policy
finding. A discrepancy with the prediction is never itself a finding.
"""

import json
import sys

sys.path.insert(0, "../SD-05-D3-IMPLEMENTATION")
sys.path.insert(0, "../SD-05-D1B-STUB")
sys.path.insert(0, ".")

import frozen                      # run-1 case definitions, imported not retyped
import c_arm as C
from registry_stub import REGISTRY, derive_impact, provenance_of
from c_adjudicate import adjudicate

# Frozen mapping from case to registry tool, as used in the prediction at
# 7e22541. Both tools are IRREVERSIBLE in stub-v1.
TOOL_FOR = {
    "A1": "transfer_funds",
    "A2": "transfer_funds",
    "A1+A2": "transfer_funds",
    "A3": "grant_access",
}


def record_for(case, arm, impact_value, impact_source):
    """Build the evidence record through the same path the injection tested."""
    u, v, i_decl, n, p = case["inputs"]
    i_used = i_decl if arm == "declared" else impact_value
    x = C.pre_activation(u, v, i_used, n, p)
    r = C.risk(u, v, i_used, n, p)
    return {
        "case_id": case["case_id"],
        "arm": "C",
        "impact_authority": arm,
        "kind": "adversarial",
        "inputs": [u, v, i_used, n, p],
        "inputs_declared": [u, v, i_decl, n, p],
        "inputs_source": impact_source,
        "impact_label": case["impact_label"],
        "adversarial_intervention": case["intervention"],
        "expected_policy": case["expected"],
        "x": x,
        "engine_score": r,
        "independent_score": C.risk(u, v, i_used, n, p),
        "observed_level": C.level_of(r),
        "signature_required": C.level_of(r) != "L0",
        "anchor_required": C.level_of(r) in ("L2", "L3"),
        "trace_required": C.level_of(r) in ("L2", "L3"),
    }


def main():
    prediction = json.load(open("cross_prediction.json"))
    results = {"frozen_prediction": "7e22541", "records": [], "gate": {}}

    # --- gate, same frozen requirement, same arm configuration ----------
    gate_ok = True
    gate_detail = {}
    for c in frozen.CASES:
        if c["kind"] != "control":
            continue
        rec = record_for(c, "declared", 0.0, "MEASURED")
        ok = rec["observed_level"] == "L0" if c["case_id"] == "P0" \
            else C.level_of(rec["engine_score"]) in ("L2", "L3")
        gate_ok = gate_ok and ok
        gate_detail[c["case_id"]] = {"level": rec["observed_level"], "ok": ok}
    results["gate"] = {"passed": gate_ok, "detail": gate_detail}

    adversarial = [c for c in frozen.CASES if c["kind"] == "adversarial"]

    # --- the cross -------------------------------------------------------
    for case in adversarial:
        cid = case["case_id"]
        tool = TOOL_FOR[cid]
        impact_value = derive_impact(tool, None, "STRICT")
        source = provenance_of(tool, None, "STRICT")

        for arm in ("declared", "derived"):
            rec = record_for(case, arm, impact_value, source)
            adj = adjudicate(rec)
            results["records"].append({
                "case_id": cid,
                "impact_authority": arm,
                "registry_tool": tool,
                "registry_impact": impact_value,
                "impact_source": source,
                "declared_inputs": rec["inputs_declared"],
                "used_inputs": rec["inputs"],
                "x": round(rec["x"], 6),
                "r": round(rec["engine_score"], 6),
                "level": rec["observed_level"],
                "outcome": adj["outcome"],
                "provenance": adj["provenance"],
                "disposition": adj["disposition"],
                "score_delta": adj["score_delta"],
                "range_valid": adj["range_valid"],
                "all_checks_fired": adj["all_checks_fired"],
            })

    # --- mechanical comparison against the frozen prediction ------------
    # Recorded as consistency or divergence. Never as confirmation.
    comparison = []
    for row in results["records"]:
        pc = prediction["cases"][row["case_id"]]
        key = "predicted_level_declared" if row["impact_authority"] == "declared" \
            else "predicted_level_derived"
        expected = pc[key] if key in pc else (
            pc["level_declared"] if row["impact_authority"] == "declared" else pc["level_derived"])
        comparison.append({
            "case_id": row["case_id"],
            "impact_authority": row["impact_authority"],
            "predicted_level": expected,
            "observed_level": row["level"],
            "consistent": expected == row["level"],
        })
    results["prediction_comparison"] = comparison
    results["prediction_consistent"] = all(c["consistent"] for c in comparison)

    # --- report ----------------------------------------------------------
    print("=" * 100)
    print("THE CROSS — candidate C x impact authority")
    print("=" * 100)
    print(f"\nk={C.K}  x̄={C.X_MID}  thresholds={C.THRESHOLDS}  "
          f"gate={'PASS' if gate_ok else 'FAIL'}")

    print("\n--- REGISTRO ---")
    print(f"  {'caso':7s} {'autoridad':11s} {'x':>8s} {'r':>8s} {'lvl':>4s} "
          f"{'outcome':26s} {'disp':18s}")
    print("  " + "-" * 88)
    for r in results["records"]:
        print(f"  {r['case_id']:7s} {r['impact_authority']:11s} {r['x']:8.4f} {r['r']:8.4f} "
              f"{r['level']:>4s} {r['outcome']:26s} {r['disposition']:18s}")

    print("\n--- CONTRAEJEMPLOS (finding-valid) ---")
    for auth in ("declared", "derived"):
        hits = [r["case_id"] for r in results["records"]
                if r["impact_authority"] == auth and r["disposition"] == "finding-valid"]
        print(f"  I {auth:9s} : {len(hits)}/4  {hits}")

    print("\n--- COMPARACIÓN CON LA PREDICCIÓN CONGELADA (7e22541) ---")
    print(f"  {'caso':7s} {'autoridad':11s} {'predicho':>9s} {'observado':>10s}  consistente")
    for c in comparison:
        print(f"  {c['case_id']:7s} {c['impact_authority']:11s} {c['predicted_level']:>9s} "
              f"{c['observed_level']:>10s}  {c['consistent']}")
    print(f"\n  predicción consistente en su conjunto: {results['prediction_consistent']}")
    print("  (consistente NO es 'confirmada'. la predicción es una hipótesis congelada,")
    print("   y la coincidencia no prueba que la regla causal sea correcta en general.)")

    results["verdict"] = ("CONSISTENT_WITH_FROZEN_PREDICTION"
                          if results["prediction_consistent"] else "DIVERGES_FROM_FROZEN_PREDICTION")
    print(f"\n  VERDICT: {results['verdict']}")
    if not results["prediction_consistent"]:
        print("  → adjudicar contra el oráculo primero; NO ajustar k, thresholds, V ni la predicción.")

    with open("cross_result.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print("  ledger written to cross_result.json")


if __name__ == "__main__":
    main()