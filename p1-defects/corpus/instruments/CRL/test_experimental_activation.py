#!/usr/bin/env python3
"""CRL R2 falsifiers: experimental activation.

Property under test.

    The published experimental configuration must place the stressor inside the
    causal window in which the guard can act, with matched doses and a single
    differing condition, and must leave a reproducible artifact.

Row R1 does not exist. Row F1 established that the guard has causal access to
the reported metric: at a matched dose of 3, guarded completes 55.00% and
unguarded 100.00%. So R2 does not re-demonstrate causality. R2 repairs the
*activation*, which the temporal inventory localised precisely:

    mean cycles before the DAG drains      3.30
    injections landing on a ready-node holder   42.8%
    injections invisible to the guard           57.2%

Two independent reasons the reported experiment never exercises the mechanism:
the window is short, and a uniformly random injection usually targets an agent
holding no currently-ready node, so the guard's decision is never reached. The
minimal intervention is therefore not "inject more failures" — it is to make the
stressor's unit "an agent currently holding a ready node", and to deliver a
matched dose before the window closes.

Criterion 6 is new and is the one the package fails hardest: **there is no
artifact at all.** Results go to stdout, so nothing identifies the execution that
produced any published number. Row F2 established that 0.02 is reachable from
this code under 5 of 200 seeds while the repository pins a seed giving 0.0300,
and nothing connects the publication to either. R2 writes the artifact that
closes that gap.

RF5 is the reversion guard. A repair that reports a difference but leaves the
published configuration untouched would satisfy RF1 through RF4 while the
manuscript's own entry point still fails to exercise the mechanism, so RF5
requires the published entry point itself to place the stressor in the window.
"""

import contextlib
import importlib.util
import io
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "src" / "crl_simulation.py"

COMMITTED_SEED = 20260909
ARTIFACT = ROOT / "data" / "resilience_experiment.json"


def load_module():
    import random
    sys.path.insert(0, str(TARGET.parent))
    spec = importlib.util.spec_from_file_location("crl_r2", TARGET)
    module = importlib.util.module_from_spec(spec)
    sys.modules["crl_r2"] = module
    spec.loader.exec_module(module)
    return module, random


def main():
    print("property: the published configuration exercises the mechanism, with")
    print("         matched doses and a reproducible artifact")
    print("=" * 78)

    m, random = load_module()
    failures = []

    # --- RF1: a stressed experiment exists as a named entry point -----------
    print(f"  [INFO] RF1 is there an entry point that delivers targeted stress?")
    stressed = getattr(m, "run_stressed_experiment", None)
    if stressed is None:
        print(f"  [FAIL] RF1 no stressed experiment exists. The package offers "
              f"run_experiment (p=0.05)")
        print(f"         and run_comparison (p=0.20), both injecting uniformly at "
              f"random over active")
        print(f"         agents, and neither targets an agent holding a ready node. The "
              f"manuscript at L151")
        print(f"         states the repository includes a stressed mode; it does not, "
              f"which was recorded")
        print(f"         as claim C5 in the inventory.")
        failures.append("RF1-no-stressed-entry-point")
    else:
        print(f"  [PASS] RF1 run_stressed_experiment is defined")

    # --- RF2: doses matched across arms ------------------------------------
    print(f"  [INFO] RF2 are the doses matched between the two arms?")
    if stressed is None:
        print(f"         not evaluable without RF1")
        failures.append("RF2-not-evaluable")
    else:
        np.random.seed(COMMITTED_SEED)
        random.seed(COMMITTED_SEED)
        runner = m.SimulationRunner(num_agents=10, num_tasks=20)
        with contextlib.redirect_stdout(io.StringIO()):
            out = stressed(runner)
        crl_arm = out["with_crl"]
        base_arm = out["without_crl"]
        print(f"           with CRL    dose {crl_arm['failures_injected']}  "
              f"completion {crl_arm['completion']:.2%}  cycles {crl_arm['cycles']}")
        print(f"           without CRL dose {base_arm['failures_injected']}  "
              f"completion {base_arm['completion']:.2%}  cycles {base_arm['cycles']}")
        if crl_arm["failures_injected"] != base_arm["failures_injected"]:
            print(f"  [FAIL] RF2 the arms received different doses; a completion "
                  f"difference would")
            print(f"         measure exposure rather than the guard")
            failures.append("RF2-dose-mismatch")
        elif crl_arm["failures_injected"] > 0:
            print(f"  [PASS] RF2 both arms received {crl_arm['failures_injected']} "
                  f"injection(s), so the only")
            print(f"           differing condition is the guard")
        else:
            print(f"  [FAIL] RF2 no stress was delivered at all")
            failures.append("RF2-no-stress")

    # --- RF3: the control arm never executes the protected path ------------
    print(f"  [INFO] RF3 does the control arm ever run the recovery path?")
    if stressed is None:
        print(f"         not evaluable without RF1")
        failures.append("RF3-not-evaluable")
    else:
        np.random.seed(COMMITTED_SEED)
        random.seed(COMMITTED_SEED)
        runner = m.SimulationRunner(num_agents=10, num_tasks=20)
        with contextlib.redirect_stdout(io.StringIO()):
            out = stressed(runner)
        base = out["without_crl"]
        if base["modifications"] == 0:
            print(f"  [PASS] RF3 the control arm recorded {base['modifications']} "
                  f"control-plane modifications, so it is")
            print(f"           genuinely unguarded rather than accidentally running the "
                  f"protected path")
        else:
            print(f"  [FAIL] RF3 the control arm recorded {base['modifications']} "
                  f"modifications; the arms are not")
            print(f"         differing in the guard alone")
            failures.append("RF3-control-not-clean")

    # --- RF4: a reproducible artifact with provenance exists ----------------
    print(f"  [INFO] RF4 does a provenance-carrying artifact exist?")
    if not ARTIFACT.exists():
        print(f"  [FAIL] RF4 no artifact exists at {ARTIFACT.relative_to(ROOT)}. "
              f"Row F2 established")
        print(f"         that the published 0.02 is reachable from this code under 5 of "
              f"200 seeds while the")
        print(f"         repository pins {COMMITTED_SEED} giving 0.0300, and that nothing "
              f"connects the")
        print(f"         publication to either execution. Results go to stdout, so no "
              f"number is lineaged.")
        failures.append("RF4-no-artifact")
    else:
        artifact = json.loads(ARTIFACT.read_text())
        prov = artifact.get("provenance", {})
        required = {"source_commit", "seed", "configuration", "generator",
                    "python_version", "dependency_versions"}
        missing = sorted(required - set(prov))
        if missing:
            print(f"  [FAIL] RF4 artifact provenance missing: {missing}")
            failures.append("RF4-provenance-incomplete")
        else:
            print(f"  [PASS] RF4 artifact carries provenance: "
                  f"{', '.join(sorted(prov))}")

    # --- RF5: the PUBLISHED entry point exercises the mechanism -----------
    print(f"  [INFO] RF5 does the published entry point put the stressor in the window?")
    np.random.seed(COMMITTED_SEED)
    random.seed(COMMITTED_SEED)
    runner = m.SimulationRunner(num_agents=10, num_tasks=20)
    with contextlib.redirect_stdout(io.StringIO()):
        legacy = runner.run_experiment()
    guarded_opportunities = getattr(m, "GUARD_OPPORTUNITIES", None)
    if guarded_opportunities is None:
        print(f"  [WARN] RF5 the published run_experiment does not report how many "
              f"cycles in which the")
        print(f"         guard withheld a completion. Without that, a reader cannot tell "
              f"whether the")
        print(f"         mechanism was exercised at all.")
        failures.append("RF5-published-entry-not-instrumented")
    elif guarded_opportunities == 0:
        print(f"  [FAIL] RF5 the published run_experiment exercised the guard in 0 "
              f"cycles: completion "
              f"{legacy['completion_rate']:.2%}")
        print(f"         A repaired stressed experiment alongside it does not make the "
              f"published entry")
        print(f"         point informative.")
        failures.append("RF5-published-entry-still-inert")
    else:
        print(f"  [PASS] RF5 the published entry point exercised the guard in "
              f"{guarded_opportunities} cycle(s)")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        print()
        print("R2 repairs activation only. It does not re-demonstrate causality -- row")
        print("F1 established that -- and it does not manufacture an effect: no")
        print("magnitude is required, only that the stressor reaches the guard with")
        print("matched doses in a single differing condition, and that the result lands")
        print("in an artifact rather than on stdout.")
        return 1
    print("PASSED: the published configuration exercises the mechanism and is lineaged")
    return 0


if __name__ == "__main__":
    sys.exit(main())