"""
Ladder v2 falsification — the instrument must distinguish four cases.

    deterministic identical      -> REPRODUCED
    deterministic different      -> NUMERIC_MISMATCH
    runtime different            -> REPRODUCED_WITH_ENVIRONMENT_DEPENDENT_FIELDS
    execution failed             -> EXECUTION_FAILURE

Plus the property that makes the fourth outcome honest: a registry edited
after sealing is refused, and a field pre-declared DETERMINISTIC that
diverges cannot be excused by relabelling it.

An ECHO variant is included — an adjudicator that excuses every divergence —
so the suite can be shown to fail against it. Controls that pass against
both prove nothing.
"""

import json

from repro_ladder import (
    DETERMINISTIC, ENVIRONMENT_DEPENDENT, DERIVED_FROM_ENVIRONMENT_DEPENDENT,
    REPRODUCED, REPRODUCED_ENV, NUMERIC_MISMATCH, EXECUTION_FAILURE,
    seal, compare,
)

RESULTS = []


def reg():
    return {
        "accuracy": DETERMINISTIC,
        "latency_ms": ENVIRONMENT_DEPENDENT,
        "itr_bits_min": DERIVED_FROM_ENVIRONMENT_DEPENDENT,
        "mean_accuracy": DETERMINISTIC,
        "mean_latency_ms": ENVIRONMENT_DEPENDENT,
        "mean_itr_bits_min": DERIVED_FROM_ENVIRONMENT_DEPENDENT,
    }


SD03_COMMITTED = {
    "accuracy": 0.25, "latency_ms": 6.519649928668514, "itr_bits_min": 0.0,
    "mean_accuracy": 0.325, "mean_latency_ms": 6.517107290710555,
    "mean_itr_bits_min": 1.7758821146395407,
}
SD03_REGENERATED = {
    "accuracy": 0.25, "latency_ms": 3.2614384749990677, "itr_bits_min": 0.0,
    "mean_accuracy": 0.325, "mean_latency_ms": 3.2245635624875035,
    "mean_itr_bits_min": 1.7817153481297185,
}


def echo_adjudicate(registry, committed, regenerated, **kw):
    """Deliberately wrong: excuses every divergence."""
    return {"outcome": REPRODUCED, "fields": [], "disposition": "finding-valid",
            "reason": "echo variant"}


def case(name, want, runner, registry=None, committed=None, regen=None,
         sealed=None, current=None, completed=True):
    out = runner(registry or reg(), committed or SD03_COMMITTED, regen,
                 execution_completed=completed,
                 sealed_digest=sealed, current_digest=current)
    got = out["outcome"]
    ok = got == want
    RESULTS.append((name, ok, got, want))
    print(f"  {'OK  ' if ok else 'FAIL'} {name:52s} -> {got}")
    return out


def main():
    print("=" * 96)
    print("LADDER v2 FALSIFICATION")
    print("=" * 96)
    r = reg()

    print("\n--- 1. los cuatro casos que el ladder debe distinguir ---")
    case("deterministic identical, nothing moved",
         REPRODUCED, compare, regen=dict(SD03_COMMITTED))

    d = dict(SD03_REGENERATED)
    d["accuracy"] = 0.375           # a DETERMINISTIC field diverges
    o = case("deterministic different", NUMERIC_MISMATCH, compare, regen=d)
    div = [f["field"] for f in o["fields"] if f["contributes"] == NUMERIC_MISMATCH]
    print(f"        campos que aportan el mismatch: {div}")

    o = case("runtime different, deterministic identical",
             REPRODUCED_ENV, compare, regen=dict(SD03_REGENERATED))
    envf = [f["field"] for f in o["fields"] if f["status"] == "ENV_DIVERGES"]
    print(f"        campos dependientes de entorno que difieren: {envf}")

    case("execution failed", EXECUTION_FAILURE, compare,
         regen={}, completed=False)

    print("\n--- 2. la pre-registro no se puede editar despues ---")
    sealed = seal(r)
    edited = dict(r)
    edited["accuracy"] = ENVIRONMENT_DEPENDENT      # reetiquetar el campo que divergio
    o = case("registry edited after sealing is refused", NUMERIC_MISMATCH,
             compare, regen=d, sealed=sealed, current=seal(edited))
    print(f"        detectado como alterado: {o['registry_tampered_after_sealing']}")

    print("\n--- 3. no-discriminating: ECHO debe fallar ---")
    echo_fails = 0
    for name, want in [("deterministic different", NUMERIC_MISMATCH),
                       ("runtime different", REPRODUCED_ENV),
                       ("execution failed", EXECUTION_FAILURE)]:
        regen = d if name == "deterministic different" else (
            dict(SD03_REGENERATED) if name == "runtime different" else {})
        completed = name != "execution failed"
        got = echo_adjudicate(r, SD03_COMMITTED, regen,
                              execution_completed=completed)["outcome"]
        ok = got != want
        echo_fails += ok
        print(f"  {'OK  ' if ok else 'FAIL'} ECHO falla en: {name:32s} (devuelve {got})")

    passed = all(ok for _, ok, _, _ in RESULTS)
    discriminating = echo_fails == 3
    print()
    print(f"  los cuatro casos diferenciados correctamente: {passed}")
    print(f"  el suite discrimina contra ECHO              : {discriminating}")
    print(f"\n  VERDICT: {'PASS' if passed and discriminating else 'FAIL'}")

    with open("ladder_controls.json", "w") as fh:
        json.dump({
            "checks": [{"case": n, "ok": ok, "got": g, "want": w}
                       for n, ok, g, w in RESULTS],
            "echo_fails": echo_fails,
            "suite_discriminates": discriminating,
            "verdict": "PASS" if passed and discriminating else "FAIL",
            "origin": "gap discovered at 3e4a2ef; this outcome did not exist then",
            "note": "The fourth outcome requires pre-registered field classes. "
                    "Without sealing, a mismatch could always be excused by "
                    "relabelling the field, which would make the ladder "
                    "non-discriminating.",
        }, fh, indent=2)
    print("  ledger written to ladder_controls.json")


if __name__ == "__main__":
    main()