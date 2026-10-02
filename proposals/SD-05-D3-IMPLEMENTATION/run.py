"""
D3 falsifier harness.

Order is fixed by specification §8:

    controls (P0, P1)
        -> gate -- abort adversarial cases if the gate fails
        -> frozen adversarial set, both arms
        -> oracle
        -> mechanical adjudication

Nothing here repairs D1a, D1b, D2 or D4. Nothing adds an adversary. Nothing
changes a threshold. Nothing redefines high-impact. If an assumption cannot
be materialised exactly as specified, that is an implementation result, not
a licence to adapt the specification until it runs.
"""

import json
import sys

import frozen
from engine import engine_score, independent_score, level_of, probe_a4_boundary
from instruments import adjudicate, control_gate


def _observe(case, arm):
    """Produce the evidence record for one case under one arm."""
    score = engine_score(arm, case["inputs"])
    recomputed = independent_score(arm, case["inputs"])
    level = level_of(score)
    return {
        "case_id": case["case_id"],
        "arm": arm,
        "kind": case["kind"],
        "inputs": list(case["inputs"]),
        "inputs_source": case["inputs_source"],
        "impact_label": case["impact_label"],
        "adversarial_intervention": case["intervention"],
        "expected_policy": case["expected"],
        "engine_score": score,
        "independent_score": recomputed,
        "observed_level": level,
        "signature_required": level != "L0",
        "anchor_required": level_rank_at_least(level, "L2"),
        "trace_required": level_rank_at_least(level, "L2"),
    }


def level_rank_at_least(level, minimum):
    return ("L0", "L1", "L2", "L3").index(level) >= ("L0", "L1", "L2", "L3").index(minimum)


def main():
    out = {"provenance": {
        "spec": "SD-05-D3-FALSIFIER-SPEC.md",
        "weights": list(frozen.WEIGHTS),
        "gamma": frozen.GAMMA,
        "thresholds": list(frozen.THRESHOLDS),
        "arms": list(frozen.ARMS),
        "case_set": [c["case_id"] for c in frozen.CASES] + [frozen.A4_PROBE["case_id"]],
        "weights_provenance": "submitted prototype AdaptiveRiskEngine default; not a design choice",
    }, "records": []}

    # --- controls first, both arms ---
    controls = {arm: [_observe(c, arm) for c in frozen.CASES if c["kind"] == "control"]
                for arm in frozen.ARMS}

    gate_passed, gate_detail = control_gate(controls)
    for arm in frozen.ARMS:
        for rec in controls[arm]:
            out["records"].append(adjudicate(rec))

    out["gate"] = {"passed": gate_passed, "detail": [
        {"arm": a, "case_id": c, "observed": o, "ok": ok} for a, c, o, ok in gate_detail
    ]}

    if not gate_passed:
        out["adversarial_ran"] = False
        out["adversarial_note"] = (
            "Adversarial cases not executed. The control gate failed, so the "
            "engine lacks sufficient operating range to make them interpretable."
        )
        return out

    # --- adversarial, only if the gate held ---
    out["adversarial_ran"] = True
    for arm in frozen.ARMS:
        for case in frozen.CASES:
            if case["kind"] != "adversarial":
                continue
            out["records"].append(adjudicate(_observe(case, arm)))

    # --- A4 frontier probe ---
    frontier = {}
    for arm in frozen.ARMS:
        sup = probe_a4_boundary(arm, engine_score)
        frontier[arm] = sup
        rec = {
            "case_id": frozen.A4_PROBE["case_id"],
            "arm": arm,
            "kind": "frontier",
            "inputs": None,
            "inputs_source": frozen.A4_PROBE["inputs_source"],
            "impact_label": frozen.A4_PROBE["impact_label"],
            "adversarial_intervention": frozen.A4_PROBE["intervention"],
            "expected_policy": frozen.A4_PROBE["expected"],
            "engine_score": sup,
            "independent_score": sup,
            "observed_level": "L0" if sup is not None else "none",
            "frontier_empty": sup is None,
            "signature_required": False,
            "anchor_required": False,
            "trace_required": False,
            "frontier_supremum": sup,
        }
        out["records"].append(adjudicate(rec))
    out["frontier_supremum_of_V_under_L0"] = frontier
    return out


if __name__ == "__main__":
    result = main()
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")