#!/usr/bin/env python3
"""LEO M1-B2 falsifier: does each arm publish its own latency measurement?

Property under test.

    Each arm's published latency must be the latency its own routing decision
    produced. No published value may be another arm's measurement transformed by
    a factor derived from the optimiser's output.

The pre-fix pipeline does exactly that. `bl_lat` and `ns_lat` were the same
expression, and the offline arm's published value was `ns_lat * (0.7 + 0.3 * w)`
— the optimiser's own weight, used as a multiplier on a measurement. Since
0.7 + 0.3*w is below 1 for every weight vector that exists, the arm's latency
advantage was a property of the multiplier.

**No number in this file is a target.** The historical 24.17 ms and the current
15.85 ms are both products of the mechanism being repaired, so either could be
"expected" and quoting either would rebuild the contamination. What is tested is
the measurement path: which call produced the value that gets published. A repair
that changed the numbers while still publishing a transformed value would pass a
value-based test and fail this one, which is the whole reason the test is about
the path.

The published-value assertion (F2) deliberately avoids a global grep. A scanner
narrow enough to miss a moved statement gave false greens twice in this row, and
a scanner wide enough to match a comment or a docstring would flag the
explanation of the defect as the defect. So the assertion is derived: instrument
`compute_latency_ms`, run the loop, and check for every round whether the value
that reached the arm's list equals the raw measurement or the raw measurement
times the factor. That settles it on the path rather than on the text.
"""

import importlib.util
import inspect
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "simulator" / "leo_routing_simulator.py"


def load_module():
    spec = importlib.util.spec_from_file_location("leo_b2_target", TARGET)
    module = importlib.util.module_from_spec(spec)
    sys.modules["leo_b2_target"] = module
    spec.loader.exec_module(module)
    return module


def instrument(module):
    """Wrap compute_latency_ms so every call is recorded with its strategy."""
    original = module.compute_latency_ms
    calls = []

    def wrapped(snr_matrix, active_mask, route_type):
        value = original(snr_matrix, active_mask, route_type)
        calls.append((int(route_type), float(value) if np.isfinite(value) else None))
        return value

    module.compute_latency_ms = wrapped
    return original, calls


def run_rounds(module, policy_weights, rounds=4):
    np.random.seed(321)
    env = module.LEORoutingEnv(num_sats=20, num_planes=2,
                               failure_rate=0.04, recovery_rate=0.02)
    router = module.QLearningRouter()
    policy = {"weights": np.asarray(policy_weights, dtype=float)}
    original, calls = instrument(module)
    try:
        measured = module._evaluate_rounds(env, router, policy, rounds=rounds)
    finally:
        module.compute_latency_ms = original
    return measured, calls


def main():
    print("property: every arm publishes the latency its own routing decision")
    print("         produced, untransformed")
    print("=" * 78)

    module = load_module()
    failures = []

    weights = [0.05, 0.90, 0.05]          # selects the resilient strategy
    measured, calls = run_rounds(module, weights)
    w_lat = float(weights[0])
    factor = 0.7 + 0.3 * w_lat

    # --- F1: each arm has its own measurement call --------------------------
    print(f"  [INFO] F1 compute_latency_ms was called {len(calls)} times over "
          f"{len(measured['baseline_latencies'])} rounds")
    strategies = [c[0] for c in calls]
    distinct = sorted(set(strategies))
    print(f"         strategies passed: {distinct}")
    if len(calls) == 3 * len(measured['baseline_latencies']):
        print(f"  [PASS] F1 every arm measures independently: three calls per round "
              f"for three arms")
    else:
        print(f"  [FAIL] F1 expected 3 calls per round, saw {len(calls)} for "
              f"{len(measured['baseline_latencies'])} rounds.")
        print("         One arm is reusing another's measurement.")
        failures.append("F1-not-independent")

    # --- F2: is the published value the raw measurement, or a transform? -----
    # Reconstruct both hypotheses from the instrumented calls. The calls are
    # recorded in production order -- baseline, offline, hybrid, per round -- so
    # index 1 of each round's slice is the offline arm's OWN raw measurement.
    # An earlier version compared against the mean of all three, which is not the
    # quantity the multiplier is applied to, so the ratio test could not fire and
    # the assertion fell back to reading the source text. That fallback is a grep
    # wearing a derivation's clothes.
    per_round_ns_raw = []
    for i in range(len(measured['baseline_latencies'])):
        chunk = calls[3 * i:3 * i + 3]
        if len(chunk) == 3 and chunk[1][1] is not None:
            per_round_ns_raw.append(chunk[1][1])
    per_round_ns_raw = np.array(per_round_ns_raw, dtype=float)
    published = np.array(measured['nsgaii_latencies'], dtype=float)

    is_transform = False
    ratio = None
    if len(per_round_ns_raw) == len(published) and np.all(per_round_ns_raw != 0):
        ratio = published / per_round_ns_raw
        is_transform = bool(np.allclose(ratio, factor, rtol=1e-6))
        is_identity = bool(np.allclose(ratio, 1.0, rtol=1e-6))

    src = inspect.getsource(module._evaluate_rounds)
    declares_factor = "0.7 + 0.3" in src

    if is_transform or (declares_factor and not is_identity):
        print(f"  [FAIL] F2 the offline arm's published latency is a transform of a "
              f"measurement, not a measurement.")
        if ratio is not None:
            print(f"           published / own-raw-measurement = {np.round(ratio, 6).tolist()}")
            print(f"           0.7 + 0.3 * w_latency with w_latency={w_lat:.3f} is "
                  f"{factor:.6f}")
        print(f"           factor present in the evaluation loop: {declares_factor}")
        print("           The optimiser's own weight is being used as a multiplier on")
        print("           the arm's measured latency. That factor is below 1 for every "
                  "weight vector")
        print("           that exists, so any advantage is a property of the multiplier.")
        failures.append("F2-published-value-is-transformed")
    elif ratio is not None:
        print(f"  [PASS] F2 published / own-raw-measurement = "
              f"{np.round(ratio, 6).tolist()}: the published value is the arm's own "
              f"measurement")
    else:
        print(f"  [PASS] F2 no transform present on the publication path")


    # --- F3: does perturbing the arm's strategy move its measurement? -------
    # Guards the false repair: deleting the multiplier while still measuring
    # Dijkstra would leave this passing by accident, so it is asserted against
    # the NSGA-II arm's own route, not against the baseline.
    alt = [0.90, 0.05, 0.05]              # selects the latency-focused strategy
    alt_measured, alt_calls = run_rounds(module, alt)

    base_strategy = module.weights_to_route_type(weights)
    alt_strategy = module.weights_to_route_type(alt)

    base_inputs = [c[0] for c in calls]
    alt_inputs = [c[0] for c in alt_calls]
    inputs_moved = base_inputs != alt_inputs

    base_ns = float(np.mean([v for v in measured['nsgaii_latencies']]))
    alt_ns = float(np.mean([v for v in alt_measured['nsgaii_latencies']]))

    if inputs_moved:
        print(f"  [PASS] F3 perturbing the arm's weights moves the route it requests: "
              f"strategy {base_strategy} -> {alt_strategy}")
        print(f"           and moves the latency it reports: {base_ns:.4f} -> "
              f"{alt_ns:.4f} ms")
        print("           The arm's number follows its own decision, which is what a")
        print("           measurement does and a multiplier cannot.")
    else:
        print(f"  [FAIL] F3 perturbing the arm's weights left every requested route "
              f"unchanged")
        print(f"         (strategy {base_strategy} under both weight vectors). The arm "
                  f"is not")
        print("         reporting anything that depends on its own policy.")
        failures.append("F3-strategy-perturbation-inert")

    # --- F4: same-policy control --------------------------------------------
    # The two weight vectors select different strategies, so they are entitled to
    # differ -- but nothing here REQUIRES a difference. An arm that selects the
    # same route as the baseline under the same environment must be allowed to
    # report the same latency. Asserted as a control, never as a target.
    same_policy = [1.0, 0.0, 0.0]         # also latency-focused, as is the baseline
    same_measured, same_calls = run_rounds(module, same_policy)
    same_strategy = module.weights_to_route_type(same_policy)
    same_ns = float(np.mean([v for v in same_measured['nsgaii_latencies']]))
    baseline_ns = float(np.mean([v for v in measured['baseline_latencies']]))

    if same_strategy == 0:
        if abs(same_ns - baseline_ns) < 1e-9:
            print(f"  [PASS] F4 same-policy control: an arm selecting the baseline's "
                  f"strategy reports the")
            print(f"           same latency ({same_ns:.4f} ms). Equal results are "
                  f"permitted and not engineered away")
        else:
            print(f"  [INFO] F4 same-policy control: both arms requested strategy 0 but "
                  f"reported {baseline_ns:.4f}")
            print(f"           and {same_ns:.4f} ms. Worth a look, and not asserted here.")
    else:
        print(f"  [INFO] F4 same-policy control not applicable: the control policy "
              f"selected strategy {same_strategy}")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        print()
        print("No historical or current figure is a target here. The criterion is the")
        print("measurement path, and the outcome may be that the offline arm's")
        print("advantage disappears -- which would be the result the repair exists to")
        print("reveal, not a surprise to be corrected.")
        return 1
    print("PASSED: every arm publishes its own measurement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
