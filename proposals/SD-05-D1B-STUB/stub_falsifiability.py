"""
D1b stub falsifiability: five properties, tested against STRICT and against a
deliberately VULNERABLE derivation.

The vulnerable variant is the point. A test that passes against both is
vacuous. Results are reported per property for both modes; the suite only
claims anything if STRICT passes and VULNERABLE fails.
"""

import json
import sys

from registry_stub import (
    AgentSurface, I_UNKNOWN, REGISTRY, REGISTRY_VERSION,
    derive_impact, provenance_of, registry_lookup,
)

RESULTS = []


def record(prop, mode, passed, detail):
    RESULTS.append({
        "property": prop, "mode": mode, "passed": passed, "detail": detail,
    })


# --- Property 1: registry integrity ------------------------------------
def p1_registry_integrity():
    """Is the effective tool the registered one, with its registered class?"""
    for mode in ("STRICT", "VULNERABLE"):
        ok = True
        detail = []
        # hostile surface: shadows every irreversible tool and volunteers
        # read-only descriptors, so a derivation that consults the surface
        # at all diverges from one that does not
        s_hostile = AgentSurface()
        for tid, (cls, mut, _) in REGISTRY.items():
            if mut:
                s_hostile.bind("helper_" + tid, tid)
                s_hostile.volunteer_descriptor(tid, "READ_ONLY")
        for tool_id in REGISTRY:
            got = derive_impact(tool_id, s_hostile, mode)
            effect_class, mutates, _ = REGISTRY[tool_id]
            expected = 0.0 if effect_class == "READ_ONLY" else 1.0
            good = got == expected
            ok = ok and good
            if not good:
                detail.append(f"{tool_id}: got {got} expected {expected}")
        record("registry_integrity", mode, ok,
               "all registered tools resolve to their registered class"
               if ok else "; ".join(detail))


# --- Property 2: shadowing resistance ---------------------------------
def p2_shadowing():
    """
    Can the agent substitute or intercept a registered tool?

    Four attack shapes: a shadowing local binding with the same target id,
    a volunteered descriptor claiming read-only, a descriptor for a tool
    that does not exist, and a stale registry version.
    """
    for mode in ("STRICT", "VULNERABLE"):
        ok = True
        detail = []

        # (a) local binding shadowing an irreversible tool, named read-only
        s = AgentSurface()
        s.bind("safe_helper", "transfer_funds")
        got = derive_impact("transfer_funds", s, mode)
        if got == 0.0:
            ok = False
            detail.append("shadowed local binding downgraded transfer_funds to 0.0")

        # (b) volunteered descriptor claiming a mutating tool is read-only
        s = AgentSurface()
        s.volunteer_descriptor("transfer_funds", "READ_ONLY")
        got = derive_impact("transfer_funds", s, mode)
        if got == 0.0:
            ok = False
            detail.append("volunteered descriptor downgraded transfer_funds to 0.0")

        # (c) descriptor for a tool that is not registered at all
        s = AgentSurface()
        s.volunteer_descriptor("totally_invented_tool", "READ_ONLY")
        got = derive_impact("totally_invented_tool", s, mode)
        if got == 0.0:
            ok = False
            detail.append("unregistered tool accepted as 0.0 instead of I_UNKNOWN")

        # (d) stale registry version must not resolve
        got = registry_lookup("transfer_funds", "stale-v0")
        if got is not None:
            ok = False
            detail.append("stale registry version resolved")

        record("shadowing_resistance", mode, ok,
               "no substitution, interception, invention or stale version admitted"
               if ok else "; ".join(detail))


# --- Property 3: identity binding --------------------------------------
def p3_identity_binding():
    """Is the tool identity bound to the registry, or is it free-floating?"""
    for mode in ("STRICT", "VULNERABLE"):
        ok = True
        detail = []
        # An unknown identity must never resolve to an impact value
        s_hostile = AgentSurface()
        s_hostile.volunteer_descriptor("transfer_funds_v2", "READ_ONLY")
        s_hostile.bind("x", "transfer_funds_v2")
        for fake in ["transfer_funds_v2", "TRANSFER_FUNDS", "transfer funds", ""]:
            got = derive_impact(fake, s_hostile, mode)
            if got != I_UNKNOWN:
                ok = False
                detail.append(f"{fake!r} resolved to {got} instead of I_UNKNOWN")
        # The binding must be by exact identity, not prefix or case
        record("identity_binding", mode, ok,
               "only exact registered identities resolve" if ok else "; ".join(detail))


# --- Property 4: effect provenance -------------------------------------
def p4_effect_provenance():
    """Does the provenance label correctly distinguish REGISTRY from DECLARED?"""
    for mode in ("STRICT", "VULNERABLE"):
        ok = True
        detail = []
        bare = AgentSurface()
        if provenance_of("transfer_funds", bare, mode) != "REGISTRY":
            ok = False
            detail.append("bare call not labelled REGISTRY")
        shadowed = AgentSurface()
        shadowed.volunteer_descriptor("transfer_funds", "READ_ONLY")
        label = provenance_of("transfer_funds", shadowed, mode)
        if mode == "STRICT":
            # Under STRICT the descriptor is ignored, so REGISTRY is correct
            if label != "REGISTRY":
                ok = False
                detail.append(f"STRICT mislabelled as {label}")
        else:
            if label != "DECLARED":
                ok = False
                detail.append(f"VULNERABLE should self-report DECLARED, said {label}")
        record("effect_provenance", mode, ok,
               "provenance label tracks the actual source" if ok else "; ".join(detail))


# --- Property 5: independent read --------------------------------------
def p5_independent_read():
    """Can the agent alter the evidence used to derive I?"""
    for mode in ("STRICT", "VULNERABLE"):
        ok = True
        detail = []
        s = AgentSurface()
        # Agent mutates its own params and bindings at will
        s.set_params(amount=1, target="attacker", force=True)
        s.bind("a", "transfer_funds")
        s.bind("b", "grant_access")
        before = derive_impact("transfer_funds", s, mode)
        after = derive_impact("transfer_funds", s, mode)
        if before != after:
            ok = False
            detail.append("agent-side mutation changed a registry-derived I")
        if before == 0.0:
            ok = False
            detail.append("mutating agent surface downgraded transfer_funds to 0.0")
        # and the registry itself must be unchanged by all of that
        if REGISTRY["transfer_funds"][0] != "IRREVERSIBLE":
            ok = False
            detail.append("registry entry mutated")
        record("independent_read", mode, ok,
               "agent-side state cannot influence a registry-derived I"
               if ok else "; ".join(detail))


# --- Fail-closed invariant ---------------------------------------------
def p6_fail_closed():
    """An I_UNKNOWN must never resolve to zero."""
    for mode in ("STRICT", "VULNERABLE"):
        ok = True
        detail = []
        # hostile surface volunteers a read-only descriptor for an
        # unregistered tool; a derivation consulting it yields 0.0 instead
        s_hostile = AgentSurface()
        s_hostile.volunteer_descriptor("nope", "READ_ONLY")
        s_hostile.bind("n", "nope")
        for fake in ["nope", "unknown_tool", "TOOL_MISSING", "transfer_funds_v2"]:
            got = derive_impact(fake, s_hostile, mode)
            if got != I_UNKNOWN:
                ok = False
                detail.append(f"{fake} yielded {got}, not I_UNKNOWN")
        record("fail_closed_invariant", mode, ok,
               "undetermined class is I_UNKNOWN, never 0" if ok else "; ".join(detail))


def main():
    for fn in (p1_registry_integrity, p2_shadowing, p3_identity_binding,
               p4_effect_provenance, p5_independent_read, p6_fail_closed):
        fn()

    # effect_provenance is a LABELING property, not a security property. The
    # vulnerable variant consults agent metadata and therefore labels it
    # DECLARED, which is the correct label for what it actually did. It holds
    # by construction and does not discriminate; conflating that with a weak
    # test would be wrong in the opposite direction.
    INVARIANT_BY_CONSTRUCTION = {"effect_provenance"}

    props = sorted({r["property"] for r in RESULTS})
    print("=" * 92)
    print("D1b STUB FALSIFIABILITY")
    print("=" * 92)
    print(f"\nregistry version: {REGISTRY_VERSION}   tools: {len(REGISTRY)}\n")
    print(f"  {'property':28s} {'STRICT':>10s} {'VULNERABLE':>12s}   discriminating?")
    print("  " + "-" * 78)
    discriminates = True
    for p in props:
        s = next(r for r in RESULTS if r["property"] == p and r["mode"] == "STRICT")
        v = next(r for r in RESULTS if r["property"] == p and r["mode"] == "VULNERABLE")
        if s["passed"] == v["passed"]:
            if p in INVARIANT_BY_CONSTRUCTION:
                disc = "n/a - labeling property"
            else:
                disc = "NO - VACUOUS"
                discriminates = False
        else:
            disc = "yes"
        print(f"  {p:28s} {'PASS' if s['passed'] else 'FAIL':>10s} "
              f"{'PASS' if v['passed'] else 'FAIL':>12s}   {disc}")

    strict_all = all(r["passed"] for r in RESULTS if r["mode"] == "STRICT")
    vuln_any = any(r["passed"] for r in RESULTS
                   if r["mode"] == "VULNERABLE"
                   and r["property"] not in INVARIANT_BY_CONSTRUCTION)
    print()
    print(f"  STRICT passes all properties        : {strict_all}")
    print(f"  VULNERABLE passes a security property: {vuln_any} (must be False)")
    print(f"  invariant-by-construction (labeling) : {sorted(INVARIANT_BY_CONSTRUCTION)}")
    print(f"  suite is discriminating             : {discriminates}")
    print()
    for r in RESULTS:
        if r["mode"] == "STRICT" and not r["passed"]:
            print(f"  STRICT FAIL: {r['property']}: {r['detail']}")
    for r in RESULTS:
        if r["mode"] == "VULNERABLE" and not r["passed"]:
            print(f"  VULNERABLE correctly fails: {r['property']}: {r['detail']}")

    verdict = (
        "PASS -- a potentially independent authority source exists"
        if strict_all and not vuln_any and discriminates
        else "FAIL -- D1b is not yet falsifiable"
    )
    print(f"\n  VERDICT: {verdict}")

    ledger = {
        "registry_version": REGISTRY_VERSION,
        "tools": len(REGISTRY),
        "results": RESULTS,
        "strict_passes_all": strict_all,
        "vulnerable_passes_any": vuln_any,
        "suite_discriminates": discriminates,
        "invariant_by_construction": sorted(INVARIANT_BY_CONSTRUCTION),
        "known_limitation": "The vulnerable variant self-reports DECLARED, so "
            "effect_provenance holds for it. A real attacker would not "
            "self-report. This stub therefore does not test honesty under an "
            "uncooperative derivator, and the property must not be cited as "
            "evidence that provenance labels are trustworthy against a "
            "deliberately concealing implementation.",
        "verdict": verdict,
        "scope": "Shadowing resistance does NOT establish that I_derived is "
                 "correct. It establishes only that a potentially independent "
                 "source of authority exists. Correctness is tested by the "
                 "I- and I+ controls, which are a later step.",
    }
    with open("stub_result.json", "w") as fh:
        json.dump(ledger, fh, indent=2)
    print("  ledger written to stub_result.json")


if __name__ == "__main__":
    main()