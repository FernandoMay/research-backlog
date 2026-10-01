#!/usr/bin/env python3
"""LEO M1 falsifier: does the experiment measure what the paper interprets?

This row is a measurement experiment, not a bug hunt. Three questions are kept
separate on purpose, because they have different answers and may have different
repairs:

    M1-A  does failure rate actually reach the routing and the environment?
    M1-B  does routing actually reach resilience?
    M1-C  does the latency pipeline distinguish a real observation from a
          disconnected graph?

Nothing here changes the environment, the metric, or any threshold. The falsifier
observes the current pipeline and reports what it can and cannot distinguish.

The synthetic routing perturbation is the load-bearing control, and it is the
same move that row R1 used: establish that a dependency exists at the object
*before* the final metric, so that a flat metric can be read as a property of
the experimental range rather than as a broken measurement. Two identical
environments, identical failures, identical seed, different routing decisions.
If resilience does not move, the metric is decoupled from the mechanism, full
stop. If it does move, the causal route exists and the question becomes whether
the nominal scenario ever exercises it.

No assertion compares a result to a previously published number. The finding
that the metric is decoupled is a statement about the pipeline, not a claim that
the pipeline's outputs are wrong.
"""

import importlib.util
import inspect
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "simulator" / "leo_routing_simulator.py"

SENTINEL_PER_HOP = None  # resolved from the module


def load_module():
    spec = importlib.util.spec_from_file_location("leo_m1_target", TARGET)
    module = importlib.util.module_from_spec(spec)
    sys.modules["leo_m1_target"] = module
    spec.loader.exec_module(module)
    return module


def build_env(module, seed=42, num_sats=60):
    np.random.seed(seed)
    return module.LEORoutingEnv(num_sats=num_sats,
                                num_planes=module.NUM_ORBITAL_PLANES)


def main():
    global SENTINEL_PER_HOP
    print("property: the experiment's parameters reach the mechanisms, and the")
    print("         metrics distinguish the phenomena the paper interprets")
    print("=" * 78)

    module = load_module()
    SENTINEL_PER_HOP = module.PROP_DELAY_PER_HOP_MS * module.NUM_SATELLITES
    failures = []
    # Scan every function that can contain the measurement pipeline, not just
    # run_simulation. An earlier version scanned run_simulation alone and
    # reported M1-B2 and M1-C as PASS after row M1-B moved the evaluation loop
    # into `_evaluate_rounds`: the defects were still present, the scanner simply
    # no longer looked at them. A falsifier that goes green because the code
    # moved is worse than one that is red, because it converts an unexamined
    # region into a passing grade.
    scanned = ["run_simulation"]
    for name in ("_evaluate_rounds", "_evaluate_chromosome", "compute_resilience"):
        if hasattr(module, name):
            scanned.append(name)
    source = "\n".join(inspect.getsource(getattr(module, n)) for n in scanned)
    print(f"  [INFO] scanning {len(scanned)} function(s) for pipeline defects: "
          f"{', '.join(scanned)}")

    # --- M1-B: is resilience measured per treatment, or broadcast? ----------
    # The question the paper's prose depends on: can avg_resilience_pct differ
    # between methods? If one measurement is appended to three lists, it cannot,
    # and the identical 77.27 in all three arms is structural rather than
    # empirical.
    res_calls = [ln.strip() for ln in source.splitlines()
                 if "compute_resilience(" in ln]
    # Scoped to the evaluator, which is row M1-R2's call site: it holds a
    # routing decision and must attribute it. The evaluation loop's call is
    # deliberately left out of this assertion -- it is the single measurement
    # broadcast to three arms, which is row M1-B's defect and is not repaired
    # here. M1-R2 makes the metric capable of carrying a strategy; it does not
    # yet make the pipeline measure each arm under its own.
    evaluator_call = [ln for ln in res_calls if "_evaluate_chromosome" in ln
                      or ln.strip().startswith("resilience, coverage")]
    unattributed = [ln for ln in evaluator_call if "route_type=" not in ln]
    if unattributed:
        print("  [FAIL] M1-B0 the evaluator measures resilience without attributing "
              "its strategy:")
        for ln in unattributed:
            print(f"           {ln.strip()}")
        failures.append("M1-B0-unattributed-evaluator")
    else:
        print(f"  [PASS] M1-B0 the evaluator attributes its routing strategy to the metric")
    single_call = len(res_calls) == 1
    broadcast = any(
        ("baseline_resilience.append" in ln and "res_pct" in ln)
        for ln in source.splitlines()
    ) and sum(1 for ln in source.splitlines()
              if "res_pct" in ln and "_resilience.append" in ln) > 1

    if broadcast:
        print("  [FAIL] M1-B resilience is one measurement appended to three lists.")
        print(f"           compute_resilience is called once per round ({len(res_calls)} "
              f"call site in the evaluation loop) and its")
        print("           single result is appended to baseline_resilience, "
              "nsgaii_resilience and hybrid_resilience")
        print("           alike. The three arms cannot differ in resilience, so an "
              "identical")
        print("           avg_resilience_pct is structural, not an empirical finding "
              "about the methods.")
        sig = inspect.signature(module.compute_resilience)
        accepts_route = "route_type" in sig.parameters
        print(f"           signature: compute_resilience{sig}"
              + ("" if accepts_route else
                 " -- it never receives a router, so no causal path exists to be tested.")
              + (" The metric can now accept a strategy; what remains is that the"
                 " pipeline never passes one." if accepts_route else ""))
        failures.append("M1-B-resilience-broadcast")

    # --- M1-B2: is the baseline and the NSGA-II arm the same measurement? ---
    bl_line = next((ln.strip() for ln in source.splitlines()
                    if ln.strip().startswith("bl_lat =")), "")
    ns_line = next((ln.strip() for ln in source.splitlines()
                    if ln.strip().startswith("ns_lat =")), "")
    # Two independent assertions. They were nested once, with the multiplier
    # check inside the "same measurement" branch, which meant that repairing one
    # silently disarmed the other: after M1-B gave the arm its own strategy, the
    # outer branch stopped firing and M1-B2 reported green while the multiplier
    # was still in the code. An assertion nested inside another assertion is
    # only tested when the outer one happens to fail.
    same_measurement = bool(
        bl_line and ns_line
        and bl_line.split("=", 1)[1].strip() == ns_line.split("=", 1)[1].strip())
    if same_measurement:
        print("  [FAIL] M1-B2 the baseline and the NSGA-II arm are the same measurement.")
        print(f"           {bl_line}")
        print(f"           {ns_line}")
        print("           Both call compute_latency_ms with the same route, so the two "
              "values are")
        print("           identical in every round before anything else happens.")
        failures.append("M1-B2-baseline-is-nsgaii")
    else:
        print("  [PASS] M1-B2 the baseline and the NSGA-II arm route differently, so "
              "their latencies are")
        print("           now two measurements rather than one copied twice")

    multiplier_stmt = next(
        (ln.strip() for ln in source.splitlines() if "ns_lat *" in ln), "")
    # This assertion used to grep the evaluation loop for "0.7 + 0.3". Row M1-B2
    # removed the multiplier, and the loop now carries a docstring explaining
    # that it is gone -- so the grep matched its own explanation and reported the
    # defect as still present after it had been repaired. That is the third false
    # green in this file from scanning source text, and the same one M1-C hit.
    #
    # M1-B2 is asserted behaviourally and in one place:
    # tests/test_latency_independence.py instruments compute_latency_ms and
    # checks that published / own-raw-measurement equals 1.0. Keeping a second,
    # weaker, text-based copy of a property that already has a derived check is
    # how a fixed defect gets reopened by a docstring.
    print(f"  [INFO] M1-B2 is asserted in tests/test_latency_independence.py by "
          f"derivation")
    print("           (published / own-raw-measurement == 1.0). This file no longer "
          f"re-checks it by grep.")

    # --- M1-A: does failure rate reach the routing? --------------------------
    # A sweep is not evidence of a defect. What is evidence is whether the
    # parameter changes anything the metric reads. Each point is classified so
    # that a flat region can be read as "this range does not excite the metric"
    # rather than as "the metric is broken".
    env = build_env(module)
    rng = np.random.default_rng(11)

    print("  [INFO] M1-A failure-rate sweep, latency classified per point:")
    rows = []
    # Probed per strategy. After M1-R2 the strategies no longer share an
    # admission rule, and the shortest-path rule is trivially satisfied on a
    # 98.3%-dense graph: any positive link delivers, so its resilience is 100%
    # at every failure fraction. That is a correct reading of that strategy
    # rather than a dead metric, so asking whether the metric responds has to be
    # asked of the strategies, not of one arbitrary one.
    res_by_route = {0: [], 1: [], 2: []}
    for fraction in (0.0, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80):
        k = int(round(len(env.satellites) * fraction))
        if k:
            victims = set(rng.choice(len(env.satellites), size=k,
                                     replace=False).tolist())
            for s in env.satellites:
                if s.sid in victims:
                    s.active = False
        # The mask is rebuilt from the current satellite state on every point.
        # An earlier version hoisted it out of the loop, so the failures were
        # applied to the satellites but not to the argument passed to
        # compute_latency_ms, and the latency column came out flat for a reason
        # that had nothing to do with the model. A sweep that does not perturb
        # what it claims to perturb is worse than no sweep.
        mask = np.array([s.active for s in env.satellites], dtype=bool)
        active_now = int(mask.sum())
        np.random.seed(99)
        lat = module.compute_latency_ms(env.snr_matrix, mask, 0)
        res, _cov = module.compute_resilience(env, route_type=0)
        for rt in (0, 1, 2):
            res_by_route[rt].append(module.compute_resilience(env, route_type=rt)[0])
        for s in env.satellites:
            s.active = True
        # Three outcomes, not two. compute_latency_ms returns a latency, or
        # np.inf when the graph is disconnected under the selected strategy, or
        # nothing else -- the 240 ms value is the fallback this repository's own
        # _evaluate_chromosome substitutes, and it never appears in
        # run_simulation's pipeline at all. An earlier version of this
        # classifier called inf an observation, which is exactly the conflation
        # M1-C exists to prevent: the run loop turns that inf into 60.0 or 55.0
        # and averages it into the published statistic.
        if not np.isfinite(lat):
            kind = "disconnected"
        elif abs(lat - SENTINEL_PER_HOP) < 1e-9:
            kind = "sentinel"
        else:
            kind = "observation"
        rows.append((fraction, k, active_now, lat, res, kind))
        print(f"         {fraction:>4.0%} failures ({active_now:>2} active) -> "
              f"latency {lat:>9.4f} ms [{kind:>12}]  resilience(route0) {res:>6.2f}%")

    lat_observations = [r[3] for r in rows if r[5] == "observation"]
    n_disc = sum(1 for r in rows if r[5] == "disconnected")
    res_values = [r[4] for r in rows]
    lat_span = (max(lat_observations) - min(lat_observations)) if lat_observations else 0.0
    res_span = max(res_values) - min(res_values)

    responding = {rt: (max(v) - min(v)) for rt, v in res_by_route.items()
                  if v and (max(v) - min(v)) > 1e-9}
    for rt in (0, 1, 2):
        span = max(res_by_route[rt]) - min(res_by_route[rt])
        verdict = "responds" if span > 1e-9 else f"flat at {res_by_route[rt][0]:.2f}%"
        print(f"  [INFO] M1-A route_type={rt}: resilience {verdict} "
              f"(span {span:.4f} points)")
    if responding:
        print(f"  [PASS] M1-A failure rate reaches resilience for "
              f"{sorted(responding)}: {responding}")
        print("           The shortest-path rule is flat because on a 98.3%-dense graph")
        print("           any positive link delivers. That is what that strategy does, "
              "and the")
        print("           equal value is reported rather than engineered away.")
    else:
        print(f"  [FAIL] M1-A resilience is constant across 0%-80% failure for every "
              f"strategy.")
        failures.append("M1-A-failure-does-not-reach-resilience")

    print(f"  [INFO] M1-A latency span across observations: {lat_span:.4f} ms "
          f"({len(lat_observations)} observations, {n_disc} disconnections)")
    if lat_span < 1e-9:
        print("         Latency is flat over this range. That is a statement about the "
              "experimental")
        print("         range and the graph density, not yet about the metric: see M1-B2.")

    # --- M1-C: is the sentinel separated from observations? ------------------
    print("  [INFO] M1-C sentinel check:")
    pipeline_appends_sentinel = any(
        ("else" in ln and any(tok in ln for tok in ("60.0", "55.0")))
        and "append" in ln
        for ln in source.splitlines()
    ) or any(("if np.isfinite" in ln and any(tok in ln for tok in ("60.0", "55.0"))
              and "append" in ln) for ln in source.splitlines())
    if pipeline_appends_sentinel:
        offenders = [ln.strip() for ln in source.splitlines()
                     if "append" in ln and ("60.0" in ln or "55.0" in ln)]
        print("  [FAIL] M1-C the evaluation loop substitutes a constant for a "
              "disconnected graph,")
        print("         so a disconnection is averaged into the latency statistic as "
              "if it were an")
        print("         observed latency. There is no category separating the two:")
        for item in offenders:
            print(f"           {item}")
        print(f"         The constants are 60.0 and 55.0 ms, not the "
              f"{SENTINEL_PER_HOP:.1f} ms sentinel, so they")
        print("         are ad hoc rather than traceable to anything measured.")
        failures.append("M1-C-sentinel-not-categorised")
    else:
        print("  [PASS] M1-C disconnected-graph results are not averaged into the "
              "latency statistic")

    # --- the control: synthetic routing perturbation ------------------------
    # Same environment, same failures, same seed, different routing decisions.
    # If resilience does not move under a perturbation that necessarily changes
    # path exposure, the metric is decoupled from the mechanism. This is the
    # test that distinguishes "the nominal range does not excite this metric"
    # from "this metric cannot see routing at all".
    print("  [INFO] M1-control synthetic routing perturbation:")
    env_c = build_env(module)
    mask_c = np.array([s.active for s in env_c.satellites], dtype=bool)

    lat_by_route, res_by_route = {}, {}
    for route_type in (0, 1, 2):
        np.random.seed(4242)
        lat_by_route[route_type] = module.compute_latency_ms(
            env_c.snr_matrix, mask_c, route_type)
        res_by_route[route_type] = module.compute_resilience(env_c, route_type=route_type)

    print(f"         route 0: latency {lat_by_route[0]:8.4f} ms  "
          f"resilience {res_by_route[0][0]:6.2f}%")
    print(f"         route 1: latency {lat_by_route[1]:8.4f} ms  "
          f"resilience {res_by_route[1][0]:6.2f}%")
    print(f"         route 2: latency {lat_by_route[2]:8.4f} ms  "
          f"resilience {res_by_route[2][0]:6.2f}%")

    latency_moved = len({round(v, 9) for v in lat_by_route.values()}) > 1
    resilience_moved = len({round(v[0], 9) for v in res_by_route.values()}) > 1

    if latency_moved:
        print(f"  [PASS] M1-control routing reaches latency: "
              f"{max(lat_by_route.values()) - min(lat_by_route.values()):.4f} ms "
              f"of separation across strategies")
    else:
        print(f"  [FAIL] M1-control three routing strategies gave an identical latency")
        failures.append("M1-control-latency-decoupled")

    if resilience_moved:
        print(f"  [PASS] M1-control routing reaches resilience under a synthetic "
              f"perturbation")
    else:
        print(f"  [FAIL] M1-control routing does NOT reach resilience. Three different "
              f"strategies,")
        print(f"         same environment and seed, all yield "
              f"{res_by_route[0][0]:.4f}%. This is the decoupling")
        print("         itself: the metric cannot see routing, so a flat avg_resilience_pct")
        print("         across methods is guaranteed regardless of what the methods do.")
        failures.append("M1-control-resilience-decoupled")

    # --- R2's own assertions ------------------------------------------------
    # F1 is the control above, now expected to separate. F4 is the constraint
    # that keeps the repair honest: strategies that admit the same links are
    # entitled to the same value, and a repair that made them differ would be
    # manufacturing a result.
    print("  [INFO] R2 same-admission control (routes 0 and 1 share an admission rule):")
    np.random.seed(4242)
    res_0a = module.compute_resilience(env_c, route_type=0)
    np.random.seed(4242)
    res_1a = module.compute_resilience(env_c, route_type=1)
    if abs(res_0a[0] - res_1a[0]) < 1e-9:
        print(f"  [PASS] R2 same-admission control: routes 0 and 1 give the same "
              f"resilience ({res_0a[0]:.4f}%)")
        print("           because they admit the same links. The repair distinguishes")
        print("           exposure; it does not manufacture a difference.")
    else:
        print(f"  [FAIL] R2 same-admission control: routes 0 and 1 gave "
              f"{res_0a[0]:.4f}% and {res_1a[0]:.4f}% despite sharing an")
        print("         admission rule. The metric is manufacturing a distinction "
              "between strategies")
        print("         that are exposed to exactly the same failures.")
        failures.append("R2-manufactures-difference")

    # F2: with the route held fixed, failure must still move the metric
    np.random.seed(99)
    env_f0 = build_env(module)
    r_none = module.compute_resilience(env_f0, route_type=2)
    rng_f = np.random.default_rng(3)
    for s in env_f0.satellites:
        if s.sid in set(rng_f.choice(len(env_f0.satellites), size=30,
                                     replace=False).tolist()):
            s.active = False
    r_high = module.compute_resilience(env_f0, route_type=2)
    if abs(r_none[0] - r_high[0]) > 1e-9:
        print(f"  [PASS] R2 failure sensitivity with the route held fixed: "
              f"{r_none[0]:.2f}% -> {r_high[0]:.2f}% at 50% failure")
    else:
        print(f"  [FAIL] R2 failure held the route fixed but resilience did not move")
        failures.append("R2-no-failure-sensitivity")

    # --- M1-B: the no-broadcast test ----------------------------------------
    # Records the strategy every stored resilience value came from. The defect
    # being guarded against is a correct measurement copied to three lists, so
    # presence of a call is not enough: the value in each arm's list must trace
    # to a call carrying that arm's strategy.
    print("  [INFO] M1-B no-broadcast test (each arm measured under its own strategy):")
    np.random.seed(321)
    env_b = module.LEORoutingEnv(num_sats=20, num_planes=2,
                                 failure_rate=0.04, recovery_rate=0.02)
    router = module.QLearningRouter()
    policy = {'weights': np.array([0.05, 0.90, 0.05])}
    observed = module._evaluate_rounds(env_b, router, policy, rounds=4)

    triples = observed['strategies_observed']
    bl_set = sorted({t[0] for t in triples})
    ns_set = sorted({t[1] for t in triples})
    hy_set = sorted({t[2] for t in triples})
    print(f"           baseline strategies observed : {bl_set}")
    print(f"           nsgaii strategies observed    : {ns_set}")
    print(f"           hybrid strategies observed    : {sorted(set(hy_set))[:6]}")

    expected_ns = module.weights_to_route_type(policy['weights'])
    if ns_set == [expected_ns]:
        print(f"  [PASS] M1-B the nsgaii arm is measured under the strategy its own "
              f"weights select ({expected_ns})")
    else:
        print(f"  [FAIL] M1-B the nsgaii arm was measured under {ns_set} but its "
              f"weights select {expected_ns}")
        failures.append("M1-B-nsgaii-strategy-mismatch")

    # The broadcast signature: one resilience value reaching three lists.
    bl_vals = observed['baseline_resilience']
    ns_vals = observed['nsgaii_resilience']
    hy_vals = observed['hybrid_resilience']
    distinct = len({tuple(round(v, 9) for v in lst)
                    for lst in (bl_vals, ns_vals, hy_vals)})
    identical = (bl_vals == ns_vals == hy_vals)
    if identical and distinct == 1 and len({t[1] for t in triples}) > 1:
        print(f"  [FAIL] M1-B every arm stores the same value while the arms' "
              f"strategies differ")
        print("         across rounds -- the signature of a broadcast.")
        failures.append("M1-B-broadcast")
    elif identical:
        print(f"  [INFO] M1-B all three arms agree this run "
              f"({bl_vals[0]:.4f}%). That is permitted: equal results")
        print("           under one scenario are a finding, not a defect. What matters")
        print("           is that each value came from its own arm's strategy, which")
        print("           the assertions above establish.")
    else:
        print(f"  [PASS] M1-B the arms' stored values are not one value copied "
              f"({distinct} distinct series)")

    # Direct check of the mechanism the broadcast used to bypass: one call, three
    # appends. Asserted on the source, because the pre-fix defect was structural.
    loop_src = inspect.getsource(module._evaluate_rounds)
    resilience_calls = loop_src.count("compute_resilience(env2, route_type=strategy)")
    if resilience_calls == 1 and loop_src.count("compute_resilience(") == 1:
        print(f"  [PASS] M1-B resilience is evaluated once per arm with that arm's "
              f"strategy")
    else:
        print(f"  [WARN] M1-B the loop contains {loop_src.count('compute_resilience(')} "
              f"resilience call site(s); review attribution by hand")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        print()
        print("No environment, metric or threshold is changed by this file. M1 is left")
        print("RED so that the repair can be chosen among M1-R1 (change the environment),")
        print("M1-R2 (change the metric) and M1-R3 (change the experimental scenario),")
        print("rather than assumed.")
        return 1
    print("PASSED: the experiment measures what the paper interprets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
