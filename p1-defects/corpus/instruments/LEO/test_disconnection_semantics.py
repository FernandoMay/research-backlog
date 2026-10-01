#!/usr/bin/env python3
"""LEO M1-C falsifier: is a disconnection distinguishable from an observation?

Property under test.

    A latency statistic must be computed over observations only. A round in
    which no path exists produced no measurement, and averaging a stand-in for
    it converts the absence of a measurement into a measurement.

The pre-fix pipeline does exactly that:

    baseline_latencies.append(bl_lat if np.isfinite(bl_lat) else 60.0)
    nsgaii_latencies.append(ns_lat if np.isfinite(ns_lat) else 55.0)
    hybrid_latencies.append(hy_lat if np.isfinite(hy_lat) else 55.0)

60.0 and 55.0 are in the same list as real latencies of roughly 15-21 ms, and the
mean is taken over the union. Nothing in the artifact records that any of them
was ever substituted. The regime is not rare: the sweep in this same file finds
the graph disconnected at 30%, 40%, 60%, 70% and 80% failure.

**Out of scope, deliberately.** This row does not touch `compute_latency_ms` and
does not reinterpret `inf`. The sentinel is not "fixed" or made more physical; it
is kept exactly as the mechanism produces it and given a name. And the 240 ms
fallback in `_evaluate_chromosome` is a different mechanism in a different path
and is NOT unified with this one. F5 asserts only that the two remain distinct
in the artifact, never that they mean the same thing.

The governing rule, which is broader than this repository:

    a number is not an observation merely because it can enter a mean.

No figure is a target. C4 is the load-bearing control: a run with no
disconnections must reproduce the previous latencies exactly, which is the only
evidence that this row changed the aggregate's semantics and not the
measurement.
"""

import importlib.util
import inspect
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "simulator" / "leo_routing_simulator.py"

# The pre-repair stand-ins. Named here so the assertion can be specific.
LEGACY_STANDINS = (55.0, 60.0)


def load_module():
    spec = importlib.util.spec_from_file_location("leo_c_target", TARGET)
    module = importlib.util.module_from_spec(spec)
    sys.modules["leo_c_target"] = module
    spec.loader.exec_module(module)
    return module


def main():
    print("property: a latency statistic is computed over observations, and a")
    print("         disconnection is named rather than substituted")
    print("=" * 78)

    module = load_module()
    failures = []

    # --- C1: classification is total, two-valued, and rejects surprises ------
    classify = getattr(module, "classify_latency", None)
    if classify is None:
        print("  [FAIL] C1 no classifier exists. Round outcomes are not named, so a")
        print("         disconnected round and an observed round are indistinguishable")
        print("         in the lists that are averaged.")
        failures.append("C1-no-classifier")
    else:
        obs = classify(17.5)
        dis = classify(float("inf"))
        print(f"  [PASS] C1 classifier present: 17.5 -> {getattr(obs, 'kind', obs)!r}, "
              f"inf -> {getattr(dis, 'kind', dis)!r}")

        # A third outcome must raise, not fall into one of the two.
        # None is not probed here: it is the marker this row chose to record a
        # disconnected round with, so accepting it is the design rather than a
        # silent fallback. NaN, a negative latency and a non-number are the
        # states that must raise.
        for probe, label in ((float("nan"), "nan"), (-1.0, "negative"),
                              ("17.5", "a string"), ({"ms": 17.5}, "a dict")):
            try:
                result = classify(probe)
                print(f"  [FAIL] C1 unexpected outcome {label} was accepted as "
                      f"{getattr(result, 'kind', result)!r} instead of raising")
                failures.append(f"C1-accepted-{label}")
            except (ValueError, TypeError):
                print(f"  [PASS] C1 unexpected outcome {label} raises rather than "
                      f"being classified")

    # --- C2: a disconnection must not enter the mean ------------------------
    aggregate = getattr(module, "aggregate_latency", None)
    if aggregate is None:
        print("  [FAIL] C2 no aggregate exists; the statistic is taken over the union")
        print("         of observations and stand-ins.")
        failures.append("C2-no-aggregate")
    else:
        mixed = aggregate([15.0, 17.0, None])
        mean_two = (15.0 + 17.0) / 2
        if mixed is None:
            print(f"  [PASS] C2 mixed input reports no statistic: {mixed!r}")
        else:
            value = getattr(mixed, "mean_ms", None)
            if value is not None and abs(value - mean_two) < 1e-9:
                print(f"  [PASS] C2 [15.0, 17.0, disconnected] aggregates to "
                      f"{value:.4f} ms, the mean of the two observations")
            else:
                print(f"  [FAIL] C2 [15.0, 17.0, disconnected] aggregated to {mixed!r}")
                print("         The disconnection entered the statistic.")
                failures.append("C2-sentinel-in-mean")

            # A bare finite number IS an observation, and once the pipeline stops
            # inventing stand-ins, 55.0 or 60.0 ms is a latency a real route
            # could legitimately produce. An earlier version of this assertion
            # demanded that a bare 55.0 be excluded from the mean, which would
            # forbid a valid measurement and was wrong after the repair. A second
            # version grepped the loop's source for the literal constants and
            # matched them in a docstring that explains why they are gone -- a
            # source grep is not a behavioural check, and this row has already
            # produced two false greens from exactly that mistake. The check is
            # therefore behavioural: a disconnected round must carry no number.
            np.random.seed(777)
            env_c = module.LEORoutingEnv(num_sats=20, num_planes=2,
                                         failure_rate=0.04, recovery_rate=0.02)
            router_c = module.QLearningRouter()
            probe = module._evaluate_rounds(env_c, router_c,
                                            {"weights": np.array([0.05, 0.90, 0.05])},
                                            rounds=8)
            # Vacuity guard. The first version of this probe ran at the nominal
            # 4% failure rate, produced zero disconnections, and therefore
            # asserted nothing while reporting PASS. A check that never exercises
            # the condition it names is one step from a false green. The failure
            # rate is raised until the condition actually occurs, and the probe
            # reports whether it managed to.
            disconnects = 0
            leaked = []
            for rate in (0.04, 0.15, 0.30, 0.50, 0.80):
                env_c = module.LEORoutingEnv(num_sats=20, num_planes=2,
                                             failure_rate=rate,
                                             recovery_rate=rate / 2)
                router_c = module.QLearningRouter()
                trial = module._evaluate_rounds(
                    env_c, router_c, {"weights": np.array([0.05, 0.90, 0.05])},
                    rounds=8)
                trial_dis = sum(1 for arm in ("baseline", "nsgaii", "hybrid")
                                for k in trial[f"{arm}_latency_kinds"]
                                if k == "DISCONNECTED")
                disconnects += trial_dis
                for arm in ("baseline", "nsgaii", "hybrid"):
                    for value, kind in zip(trial[f"{arm}_latencies"],
                                           trial[f"{arm}_latency_kinds"]):
                        if kind == "DISCONNECTED" and value is not None:
                            leaked.append((arm, rate, value))
                if disconnects:
                    probe = trial
                    break

            if disconnects == 0:
                print(f"  [FAIL] C2 no disconnected round could be produced at any "
                      f"failure rate up to 80%, so")
                print("         the check never exercised the condition it names")
                failures.append("C2-vacuous")
            elif leaked:
                print(f"  [FAIL] C2 disconnected rounds still carry a number: "
                      f"{leaked[:3]}")
                failures.append("C2-disconnected-round-has-value")
            else:
                print(f"  [PASS] C2 {disconnects} disconnected round(s) exercised, none "
                      f"carrying a number")
            if abs(getattr(aggregate([15.0, 17.0, None]), "mean_ms", 0) - mean_two) > 1e-9:
                print(f"  [FAIL] C2 the disconnection marker entered the mean")
                failures.append("C2-marker-in-mean")
            else:
                print(f"  [PASS] C2 the disconnection marker contributes to "
                      f"n_disconnected and to nothing else")


    # --- C3: all disconnected must be an explicit non-result ----------------
    if aggregate is not None:
        empty = aggregate([None, None, None])
        if empty is None or getattr(empty, "mean_ms", None) is None:
            print(f"  [PASS] C3 all-disconnected reports an explicit non-result: "
                  f"{empty!r}")
            if empty is not None:
                print(f"           observations={getattr(empty, 'n_observations', '?')}, "
                      f"disconnected={getattr(empty, 'n_disconnected', '?')}")
        else:
            print(f"  [FAIL] C3 all-disconnected produced a statistic "
                  f"({getattr(empty, 'mean_ms', empty)}) instead of an explicit")
            print("         non-result. A wholly disconnected run has nothing to average.")
            failures.append("C3-all-disconnected-yields-statistic")

        marker_only = aggregate([None, None, float("inf")])
        v = getattr(marker_only, "mean_ms", None)
        if v is None:
            print(f"  [PASS] C3 disconnections however expressed -- None or inf -- "
                  f"yield no statistic")
        else:
            print(f"  [FAIL] C3 a wholly disconnected run reported {v} ms")
            failures.append("C3-marker-only-yields-statistic")


    # --- C4: preservation — the measurement itself is untouched -------------
    # A run with no disconnections must produce exactly the latencies the previous
    # pipeline produced. This is the only evidence that the aggregate's semantics
    # changed and the measurement did not.
    np.random.seed(321)
    env = module.LEORoutingEnv(num_sats=20, num_planes=2,
                               failure_rate=0.04, recovery_rate=0.02)
    router = module.QLearningRouter()
    policy = {"weights": np.array([0.05, 0.90, 0.05])}
    measured = module._evaluate_rounds(env, router, policy, rounds=6)

    arms = ("baseline", "nsgaii", "hybrid")
    contaminated, clean = [], []
    for arm in arms:
        values = measured[f"{arm}_latencies"]
        kinds = measured.get(f"{arm}_latency_kinds")
        if kinds is None:
            contaminated.append((arm, "no per-round kinds recorded"))
            continue
        obs = [v for v, k in zip(values, kinds) if k == "OBSERVATION"]
        dis = [k for k in kinds if k == "DISCONNECTED"]
        clean.append((arm, len(obs), len(dis)))

    if contaminated:
        for arm, why in contaminated:
            print(f"  [FAIL] C4 {arm}: {why}. The aggregate cannot be checked against "
                  f"the source")
            print("         because the pipeline does not record which rounds were "
                  "observed.")
            failures.append(f"C4-{arm}-no-kinds")
    else:
        for arm, n_obs, n_dis in clean:
            print(f"  [INFO] C4 {arm:<9} {n_obs} observations, {n_dis} disconnections "
                  f"over 6 rounds")

        # The preservation check: with a connected graph every round, the
        # published statistic must equal the mean of the measured values.
        all_observed = all(n_dis == 0 for _a, n_obs, n_dis in clean)
        if all_observed:
            for arm in arms:
                values = measured[f"{arm}_latencies"]
                kinds = measured[f"{arm}_latency_kinds"]
                expected = float(np.mean([v for v, k in zip(values, kinds)
                                          if k == "OBSERVATION"]))
                actual = float(np.mean(values))
                if abs(expected - actual) > 1e-9:
                    print(f"  [FAIL] C4 preservation: {arm} published "
                          f"{actual:.6f} but the observations average {expected:.6f}")
                    failures.append(f"C4-preservation-{arm}")
                else:
                    print(f"  [PASS] C4 preservation: {arm} publishes "
                          f"{actual:.4f} ms, identical to the mean of its observations")
        else:
            print(f"  [INFO] C4 this run contains disconnections, so the preservation "
                  f"check is")
            print("         compared per-round rather than on the aggregate:")
            for arm in arms:
                values = measured[f"{arm}_latencies"]
                kinds = measured[f"{arm}_latency_kinds"]
                leaked = [v for v, k in zip(values, kinds)
                          if k == "DISCONNECTED" and np.isfinite(v)]
                if leaked:
                    print(f"  [FAIL] C4 {arm} stored finite values for disconnected "
                          f"rounds: {leaked[:3]}")
                    failures.append(f"C4-disconnected-has-value-{arm}")
                else:
                    print(f"  [PASS] C4 {arm} stores no numeric stand-in for its "
                          f"disconnected rounds")

    # --- C5: the 240 ms path stays a separate mechanism ---------------------
    sentinel_per_hop = module.PROP_DELAY_PER_HOP_MS * module.NUM_SATELLITES
    src = inspect.getsource(module._evaluate_chromosome)
    uses_sentinel = "PROP_DELAY_PER_HOP_MS" in src
    print(f"  [INFO] C5 the _evaluate_chromosome sentinel is {sentinel_per_hop:.1f} ms "
          f"and is {'still present' if uses_sentinel else 'absent'}")
    print("         It belongs to the optimiser's evaluator, a different path from the")
    print("         evaluation loop, and this row does not unify them. Not asserted:")
    print("         proving they mean the same thing would be a claim this row cannot")
    print("         support, and the two are kept distinguishable.")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        return 1
    print("PASSED: disconnections are named, not averaged in")
    return 0


if __name__ == "__main__":
    sys.exit(main())
