"""
Oracle capability injection for candidate C.

CONTRADICTS_PROVEN_RANGE is unreachable from a correct f_C, which is the
right state and also the reason this injection exists. An oracle nobody has
seen fire is an untested instrument, and NON-DISCRIMINATING-FALSIFIER has
already occurred twice in this chain.

The injection enters at the MEASUREMENT CHANNEL, not by handing a fabricated
result straight to the adjudicator. Handing a value directly demonstrates
classification. It does not demonstrate that the apparatus can detect an
invalid observation at its real integration point, which is the property
being claimed here.

f_C is not modified. No parameter is added to it. The injected value travels
the same record-building path a legitimate observation travels.

The real adjudicator from the run-1 snapshot is imported rather than copied,
so what is verified is the instrument that will actually be used.
"""

import json
import sys

sys.path.insert(0, "../SD-05-D3-IMPLEMENTATION")

import c_arm as C
from c_adjudicate import adjudicate   # run-1 instrument, with C's range registered

PROVEN_LO, PROVEN_HI = 0.0302, 0.9698   # the analytic bound, not the sampled one

# Inputs that span the declared domain. Legitimate cases.
LEGIT = {
    "read_only":      (0.10, 0.00, 0.00, 0.10, 0.10),
    "high_impact":    (0.80, 1.00, 1.00, 0.70, 0.70),
    "mid":            (0.50, 0.50, 0.50, 0.50, 0.50),
    "all_zero":       (0.00, 0.00, 0.00, 0.00, 0.00),
    "all_one":        (1.00, 1.00, 1.00, 1.00, 1.00),
}


def build_record(name, u, v, i, n, p, measure_r, recompute_r):
    """
    The integration point. A legitimate record and an injected record are
    built by exactly this function; they differ only in the values the two
    measurement channels report.
    """
    x = C.pre_activation(u, v, i, n, p)
    r = measure_r(x)
    rec_r = recompute_r(x)
    return {
        "case_id": name, "arm": "C", "kind": "adversarial",
        "inputs": [u, v, i, n, p],
        "inputs_source": "DECLARED",
        "impact_label": "IRREVERSIBLE_EXTERNAL",
        "adversarial_intervention": "none",
        "expected_policy": "not_L0",
        "x": x,
        "engine_score": r,
        "independent_score": rec_r,
        "observed_level": C.level_of(r),
        "signature_required": False,
        "anchor_required": False,
        "trace_required": False,
    }


# --- channel A: a wrong arm or a mislabelled variant --------------------
# Both paths compute the same wrong thing, so score_delta stays 0 and the
# oracle is the only instrument that can fire.
def wrong_arm_below(x):
    return 0.01

def wrong_arm_above(x):
    return 0.99

# --- channel B: a single-channel arithmetic or wiring fault -------------
def untouched(x):
    return C.f_c(x)


def main():
    results = []

    print("=" * 92)
    print("ORACLE CAPABILITY INJECTION — candidate C")
    print("=" * 92)
    print(f"\nproven range [{PROVEN_LO}, {PROVEN_HI}]   f_C untouched\n")

    # --- 1. every legitimate measurement must stay inside ---------------
    print("--- 1. medición legítima: nunca debe disparar el oráculo ---")
    for name, inp in LEGIT.items():
        rec = build_record(name, *inp, C.f_c, C.f_c)
        r = rec["engine_score"]
        inside = PROVEN_LO <= r <= PROVEN_HI
        rec2 = adjudicate(rec)
        fires = "CONTRADICTS_PROVEN_RANGE" in rec2["all_checks_fired"]
        ok = inside and not fires
        results.append(("legitimate_stays_inside", name, ok))
        print(f"  {name:14s} x={rec['x']:.4f}  r={r:.6f}  inside={inside}  "
              f"oracle_fired={fires}  {'OK' if ok else 'FAIL'}")

    # --- 2. injection through the measurement channel --------------------
    print("\n--- 2. inyección por el canal de medición (ambos canales, delta=0) ---")
    for label, chan, want_range in (
        ("below lower bound", wrong_arm_below, True),
        ("above upper bound", wrong_arm_above, True),
    ):
        rec = build_record("injected", *LEGIT["high_impact"], chan, chan)
        res = adjudicate(rec)
        fired = "CONTRADICTS_PROVEN_RANGE" in res["all_checks_fired"]
        ok = fired and res["outcome"] == "CONTRADICTS_PROVEN_RANGE"
        results.append(("both_channels_corrupted", label, ok))
        print(f"  {label:20s} r={rec['engine_score']:.4f}  delta={res['score_delta']:.1e}  "
              f"fired={fired}  outcome={res['outcome']:26s} disp={res['disposition']}  "
              f"{'OK' if ok else 'FAIL'}")

    # --- 3. boundary values are valid, not violations -------------------
    print("\n--- 3. valores en la frontera: válidos, no violaciones ---")
    for label, val in (("at lower bound", PROVEN_LO), ("at upper bound", PROVEN_HI)):
        rec = build_record("boundary", *LEGIT["high_impact"],
                           lambda x, v=val: v, lambda x, v=val: v)
        res = adjudicate(rec)
        fired = "CONTRADICTS_PROVEN_RANGE" in res["all_checks_fired"]
        ok = not fired
        results.append(("boundary_valid", label, ok))
        print(f"  {label:20s} r={val:.4f}  fired={fired}  outcome={res['outcome']:26s}  "
              f"{'OK' if ok else 'FAIL'}")

    # --- 4. interior value is not a violation ----------------------------
    rec = build_record("interior", *LEGIT["high_impact"],
                       lambda x: 0.5, lambda x: 0.5)
    res = adjudicate(rec)
    fired = "CONTRADICTS_PROVEN_RANGE" in res["all_checks_fired"]
    results.append(("interior_valid", "r=0.5", not fired))
    print(f"\n--- 4. valor interior válido ---\n  r=0.5000  fired={fired}  "
          f"{'OK' if not fired else 'FAIL'}")

    # --- 5. the two corruption modes are distinguishable -----------------
    print("\n--- 5. los dos modos de corrupción se distinguen ---")
    only_one = build_record("single", *LEGIT["high_impact"], C.f_c, wrong_arm_above)
    res_one = adjudicate(only_one)
    both = build_record("both", *LEGIT["high_impact"], wrong_arm_above, wrong_arm_above)
    res_both = adjudicate(both)
    distinct = res_one["outcome"] != res_both["outcome"]
    results.append(("modes_distinguishable", "single vs both", distinct))
    print(f"  un solo canal corrupto   delta={res_one['score_delta']:.3e} -> {res_one['outcome']}")
    print(f"  ambos canales corruptos  delta={res_both['score_delta']:.3e} -> {res_both['outcome']}")
    print(f"  distinguibles: {distinct}   {'OK' if distinct else 'FAIL'}")

    passed = all(ok for _, _, ok in results)
    print(f"\n  VERDICT: {'PASS — the oracle detects the violation it exists to detect' if passed else 'FAIL'}")

    ledger = {
        "proven_range": [PROVEN_LO, PROVEN_HI],
        "f_c_unmodified": True,
        "adjudicator_source": "SD-05-D3-IMPLEMENTATION/instruments.py (imported, not copied)",
        "injection_point": "measurement channel, after f_C and before the adjudicator",
        "checks": [{"group": g, "case": c, "ok": ok} for g, c, ok in results],
        "verdict": "PASS" if passed else "FAIL",
        "demonstrates": [
            "every legitimate f_C measurement stays inside the proven range",
            "an out-of-range measurement travelling the real record path is caught",
            "boundary values are valid rather than violations",
            "an interior value is not a violation",
            "single-channel and both-channel corruption are distinguishable",
        ],
        "not_established": [
            "that C is a valid policy",
            "that C produces any particular result on A1, A2, A1+A2 or A3",
            "that the range is a security property",
            "any result about the cross",
        ],
    }
    with open("oracle_injection_result.json", "w") as fh:
        json.dump(ledger, fh, indent=2)
    print("  ledger written to oracle_injection_result.json")


if __name__ == "__main__":
    main()