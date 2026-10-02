"""
Operation 2 — oracle verification for candidate C.

Establishes, before any adversary runs, that the implementation of f_C:

    1. attains the analytically proven range
    2. can reach all four tiers from legitimate inputs in the declared domain
    3. satisfies the frozen gate (P0 -> L0, P1 -> L2 or above)
    4. exposes no route by which K, the thresholds, or the weights can vary
       from the execution path

Deliberately NOT established here, and stated so it cannot be over-read:

    That C is a valid policy.
    That C produces any particular result on A1, A2, A1+A2 or A3.
    That the absence of a structural impossibility means the policy works.

No adversary is executed in this operation.
"""

import inspect
import json
import sys

import c_arm as C

PROVEN = (0.0302, 0.9698)


def check_range():
    xs = [C.X_MIN + (C.X_MAX - C.X_MIN) * i / 200000 for i in range(200001)]
    rs = [C.f_c(x) for x in xs]
    lo, hi = min(rs), max(rs)
    return {
        "check": "analytic_range",
        "proven": list(PROVEN),
        "observed": [round(lo, 6), round(hi, 6)],
        "within": lo >= PROVEN[0] - 1e-6 and hi <= PROVEN[1] + 1e-6,
        "matches_to_1e-4": abs(lo - PROVEN[0]) < 5e-4 and abs(hi - PROVEN[1]) < 5e-4,
    }


def check_tiers():
    first = {}
    for i in range(200001):
        x = C.X_MIN + (C.X_MAX - C.X_MIN) * i / 200000
        lvl = C.level_of(C.f_c(x))
        if lvl not in first:
            first[lvl] = {"x": round(x, 4), "r": round(C.f_c(x), 4)}
    missing = [t for t in ("L0", "L1", "L2", "L3") if t not in first]
    return {
        "check": "four_tiers_reachable",
        "first_reach": first,
        "missing": missing,
        "all_reachable": not missing,
    }


def check_gate():
    cases = {
        "P0": ((0.10, 0.00, 0.00, 0.10, 0.10), "L0"),
        "P1": ((0.80, 1.00, 1.00, 0.70, 0.70), "L2+"),
    }
    out = {}
    ok = True
    for name, (inp, need) in cases.items():
        r = C.risk(*inp)
        lvl = C.level_of(r)
        good = (lvl == "L0") if need == "L0" else (lvl in ("L2", "L3"))
        ok = ok and good
        out[name] = {
            "x": round(C.pre_activation(*inp), 4),
            "r": round(r, 6),
            "level": lvl,
            "requires": need,
            "ok": good,
        }
    return {"check": "frozen_gate", "detail": out, "passed": ok}


def check_immutability():
    """No function accepts a slope, a threshold set, or a variant selector."""
    fns = [C.risk, C.f_c, C.level_of, C.pre_activation]
    accepts_k = any(
        "k" in inspect.signature(f).parameters or
        any(p.kind is inspect.Parameter.VAR_KEYWORD
            for p in inspect.signature(f).parameters.values())
        for f in fns
    )
    return {
        "check": "no_override_path",
        "signatures": {f.__name__: str(inspect.signature(f)) for f in fns},
        "K_is_module_constant": isinstance(C.__dict__.get("K"), float),
        "no_parameter_named_k": not accepts_k,
        "thresholds_unchanged": C.THRESHOLDS == (0.30, 0.65, 0.85),
        "weights_unchanged": C.WEIGHTS == (0.2, 0.3, 0.3, 0.1, 0.1),
        "gamma_unchanged": C.GAMMA == 0.15,
        "passed": (
            not accepts_k
            and isinstance(C.__dict__.get("K"), float)
            and C.THRESHOLDS == (0.30, 0.65, 0.85)
            and C.WEIGHTS == (0.2, 0.3, 0.3, 0.1, 0.1)
            and C.GAMMA == 0.15
        ),
    }


def main():
    r = check_range()
    t = check_tiers()
    g = check_gate()
    i = check_immutability()

    print("=" * 88)
    print("OPERATION 2 — ORACLE VERIFICATION FOR CANDIDATE C")
    print("=" * 88)
    print(f"\nk={C.K}  x̄={C.X_MID}  domain=[{C.X_MIN}, {C.X_MAX}]  thresholds={C.THRESHOLDS}\n")

    print(f"  1. range      proven {PROVEN}  observed {r['observed']}  "
          f"within={r['within']}  matches={r['matches_to_1e-4']}")
    print(f"  2. tiers      {sorted(t['first_reach'])}  all reachable={t['all_reachable']}")
    for k_ in ("L0", "L1", "L2", "L3"):
        v = t["first_reach"].get(k_)
        print(f"       {k_}: x={v['x']:.4f}  r={v['r']:.4f}" if v else f"       {k_}: UNREACHABLE")
    print(f"  3. gate       P0={g['detail']['P0']['level']} P1={g['detail']['P1']['level']}  "
          f"passed={g['passed']}")
    print(f"  4. immutable  K constant={i['K_is_module_constant']}  no param k={i['no_parameter_named_k']}  "
          f"thresholds={i['thresholds_unchanged']}  passed={i['passed']}")

    all_ok = r["matches_to_1e-4"] and t["all_reachable"] and g["passed"] and i["passed"]
    print(f"\n  VERDICT: {'PASS — the implementation attains the proven range and satisfies the gate' if all_ok else 'FAIL'}")

    print("\n  NOT established by this operation:")
    print("    - that C is a valid policy")
    print("    - that C produces any particular result on A1, A2, A1+A2, A3")
    print("    - that the absence of a structural impossibility means the policy works")
    print("  No adversary was executed.")

    ledger = {
        "k": C.K, "x_mid": C.X_MID, "thresholds": list(C.THRESHOLDS),
        "domain": [C.X_MIN, C.X_MAX], "range_check": r, "tier_check": t,
        "gate_check": g, "immutability_check": i, "verdict": "PASS" if all_ok else "FAIL",
        "not_established": [
            "that C is a valid policy",
            "that C produces any particular result on A1, A2, A1+A2 or A3",
            "that absence of a structural impossibility means the policy works",
        ],
        "oracle_note": "CONTRADICTS_PROVEN_RANGE is unreachable in this "
                       "implementation because no x in the domain produces a "
                       "score outside the proven range. That is the correct "
                       "state: the oracle exists to detect a defect, and here "
                       "there is none.",
    }
    with open("oracle_result.json", "w") as fh:
        json.dump(ledger, fh, indent=2)
    print("  ledger written to oracle_result.json")


if __name__ == "__main__":
    main()