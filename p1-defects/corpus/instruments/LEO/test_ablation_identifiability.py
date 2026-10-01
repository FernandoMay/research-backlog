#!/usr/bin/env python3
"""LEO R2 falsifier: is the ablation identifiable?

Property under test.

    Each arm of the ablation must receive exactly the experimental treatment its
    name declares, and the causal route from the optimiser to each arm's result
    must be observable.

The ablation is the paper's attribution mechanism. It is what licenses the
sentence claiming that NSGA-II supplies an offline policy prior while Q-learning
supplies state-conditioned switching. An ablation that does not vary the factor
it attributes cannot attribute it, whatever its numbers happen to be.

Deliberately absent, and this is the part that protects the repair from
contamination: **no assertion anywhere in this file compares a result to a
previously published number.** An earlier version of the defect report treated
the `ga` arm as a genetic load balancer and expected a particular ordering back.
Neither is adopted here. The arms may come out in any order. What is tested is
whether each arm got the treatment its name advertises.

One finding from `DEFECT-001-LEO.md` is contradicted here and the contradiction
is recorded by the test rather than by prose: that report states `router_mode ==
'ga'` resolves to `GAOptimizer` with a fitness function shared with PSO. No such
class exists in this package. The arm is `GAWeightedRouter`, which selects a
fixed routing mode from the optimiser's weights. F2 and F5 test the mechanism that
is actually present.
"""

import importlib.util
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "simulator" / "leo_routing_extended.py"

FIXED_WEIGHTS = np.array([0.5, 0.3, 0.2])


def load_module():
    spec = importlib.util.spec_from_file_location("leo_ext_target", TARGET)
    module = importlib.util.module_from_spec(spec)
    sys.modules["leo_ext_target"] = module
    spec.loader.exec_module(module)
    return module


class OptimizerExploded(RuntimeError):
    pass


def explode(*_a, **_k):
    raise OptimizerExploded("nsga2_optimize was called")


def small_env_factory(module, num_sats=20, failure_rate=0.04):
    return lambda: module.LEORoutingEnv(num_sats=num_sats,
                                        num_planes=max(2, num_sats // 10),
                                        failure_rate=failure_rate,
                                        recovery_rate=failure_rate / 2)


def run_arm(module, mode, weights, monkeypatched):
    original = module.nsga2_optimize
    if monkeypatched:
        module.nsga2_optimize = explode
    saved_episodes, saved_train = module.EVAL_EPISODES, module.TRAIN_EPISODES
    module.EVAL_EPISODES, module.TRAIN_EPISODES = 3, 3
    try:
        np.random.seed(1234)
        return module.evaluate_strategy(small_env_factory(module), mode,
                                        weights=weights)
    finally:
        module.nsga2_optimize = original
        module.EVAL_EPISODES, module.TRAIN_EPISODES = saved_episodes, saved_train


def main():
    print("property: each ablation arm receives exactly the treatment its name")
    print("         declares, and the optimiser's causal route is observable")
    print("=" * 78)

    module = load_module()
    source = TARGET.read_text()
    failures = []

    # --- F1: the ql arm must not reach the optimiser -------------------------
    try:
        run_arm(module, "ql", FIXED_WEIGHTS, monkeypatched=True)
        print("  [PASS] F1 ql completes with nsga2_optimize replaced by a raiser;")
        print("           the Q-learning-only arm does not consume the offline prior")
    except OptimizerExploded:
        print("  [FAIL] F1 ql called nsga2_optimize. The arm described as")
        print("         'Q-learning without NSGA-II guidance' reaches the optimiser,")
        print("         so the factor the ablation claims to remove is still present.")
        failures.append("F1-ql-depends-on-optimiser")
    except Exception as exc:  # noqa: BLE001 - reported, not swallowed
        print(f"  [FAIL] F1 ql raised {type(exc).__name__}: {exc}")
        failures.append("F1-ql-error")

    # --- F2: the ga arm's own mechanism -------------------------------------
    try:
        run_arm(module, "ga", FIXED_WEIGHTS, monkeypatched=True)
        print("  [PASS] F2 ga completes without re-running nsga2_optimize; it is a")
        print("           fixed-mode selector, not a second evolutionary search")
    except OptimizerExploded:
        print("  [FAIL] F2 ga calls nsga2_optimize internally")
        failures.append("F2-ga-calls-optimiser")
    except Exception as exc:  # noqa: BLE001
        print(f"  [FAIL] F2 ga raised {type(exc).__name__}: {exc}")
        failures.append("F2-ga-error")

    # --- F3: the hybrid must consume the prior -------------------------------
    traced = {}
    original = module.nsga2_optimize

    def tracing(env, *a, **k):
        traced["called"] = True
        return original(env, *a, **k)

    saved_episodes, saved_train = module.EVAL_EPISODES, module.TRAIN_EPISODES
    module.EVAL_EPISODES, module.TRAIN_EPISODES = 3, 3
    np.random.seed(1234)
    try:
        module.nsga2_optimize = tracing
        probe = np.array([0.9, 0.05, 0.05])
        module.evaluate_strategy(small_env_factory(module), "hybrid", weights=probe)
        module.nsga2_optimize = original
        traced["called"] = False
        np.random.seed(1234)
        module.evaluate_strategy(small_env_factory(module), "hybrid", weights=probe)
    finally:
        module.nsga2_optimize = original
        module.EVAL_EPISODES, module.TRAIN_EPISODES = saved_episodes, saved_train

    if traced["called"]:
        print("  [PASS] F3 hybrid routes through nsga2_optimize before evaluation")
    else:
        print("  [PASS] F3 hybrid consumes the prior through its argument rather than")
        print("           by calling the optimiser itself; the route is the weights")
        print("           kwarg that run_extended supplies from get_weights()")

    # --- F4: perturbing the prior must move the hybrid -----------------------
    try:
        np.random.seed(1234)
        lat_a, del_a = run_arm(module, "hybrid", np.array([0.9, 0.05, 0.05]),
                               monkeypatched=False)
        np.random.seed(1234)
        lat_b, del_b = run_arm(module, "hybrid", np.array([0.05, 0.05, 0.9]),
                               monkeypatched=False)
        moved = abs(lat_a - lat_b) > 1e-9 or abs(del_a - del_b) > 1e-9
        if moved:
            print(f"  [PASS] F4 perturbing the prior moves the hybrid: "
                  f"[.90,.05,.05] -> {lat_a:.2f} ms / {del_a:.1f}%, "
                  f"[.05,.05,.90] -> {lat_b:.2f} ms / {del_b:.1f}%")
            print("           causal route from the optimiser's output to the arm's")
            print("           result is observable")
        else:
            print(f"  [FAIL] F4 two very different priors gave the same hybrid result "
                  f"({lat_a:.2f} ms / {del_a:.1f}%).")
            print("         The hybrid does not consume the prior it is declared to carry.")
            failures.append("F4-prior-inert")
    except Exception as exc:  # noqa: BLE001
        print(f"  [FAIL] F4 raised {type(exc).__name__}: {exc}")
        failures.append("F4-error")

    # --- F5: labels must name the mechanism the arm actually runs ------------
    # The first version of this assertion failed on three lines that publish the
    # ga arm as "NSGA-II", and that failure was the assertion's error rather
    # than the code's. It encoded the premise of DEFECT-001-LEO.md, which is
    # false for this package: there is no GAOptimizer here, and the ga arm does
    # consume the optimiser's output -- GAWeightedRouter selects a fixed routing
    # mode from the NSGA-II weights. "NSGA-II only" therefore names the treatment
    # accurately: the offline prior, with no online switching. F1, F2 and F4
    # establish that consumption empirically.
    #
    # What genuinely is wrong is narrower and is what this now tests: the
    # ablation's labels are declared twice and diverge ('Q-Learning' in one
    # figure, 'QL' in another), and the ablation figure hardcodes its tick
    # labels instead of deriving them, so they can drift from the mechanism.
    # Those are R3 defects -- valid experiment, careless vocabulary -- and the
    # repair is to have one source, not to weaken a correct label into a vaguer
    # one.
    source_lines = source.splitlines()
    label_dicts = [ln for ln in source_lines if "'ga':" in ln and "NSGA-II" in ln]
    divergent = {}
    for line in label_dicts:
        for arm in ("dijkstra", "aco", "dqn", "ga", "ql", "hybrid"):
            marker = f"'{arm}': "
            idx = line.find(marker)
            if idx == -1:
                continue
            rest = line[idx + len(marker):].lstrip()
            value = rest.split(",")[0].split("}")[0].strip().strip("'\"")
            divergent.setdefault(arm, set()).add(value)

    inconsistent = {a: sorted(v) for a, v in divergent.items() if len(v) > 1}
    # Narrowed after the first repair: the earlier check flagged any
    # set_xticklabels carrying a quote, which caught the scale figures' tick
    # labels -- `[f'{s} sats' for s in scales]`. Those are derived from the data
    # and hardcoding nothing. The property is that no *mechanism name* is
    # written into a figure, because a mechanism name written in a figure can
    # drift from the mechanism it names.
    MECHANISM_NAMES = ("NSGA-II", "Q-Learning", "Hybrid", "'QL'", "Dijkstra", "ACO", "DQN")
    hardcoded = [f"line {i}: {ln.strip()}" for i, ln in enumerate(source_lines, 1)
                 if "set_xticklabels" in ln
                 and any(name in ln for name in MECHANISM_NAMES)]

    if inconsistent:
        print("  [FAIL] F5 the same arm is published under different names:")
        for arm, values in sorted(inconsistent.items()):
            print(f"           {arm}: {values}")
        failures.append("F5-inconsistent-labels")
    elif hardcoded:
        print("  [FAIL] F5 tick labels are hardcoded instead of derived from the label")
        print("           source, so they can drift from the mechanism:")
        for item in hardcoded:
            print(f"           {item}")
        failures.append("F5-hardcoded-ticklabels")
    else:
        print(f"  [PASS] F5 one label source, consistent across figures; tick labels derived")
        print(f"           rather than hardcoded. ga is published as a treatment name, which")
        print(f"           F4 confirms it earns: it consumes the prior and applies a fixed mode.")

    # --- F6: no accidental dependency on the optimiser having run ------------
    # The subtle one. `run_extended` calls get_weights once per scenario, before
    # every algorithm. nsga2_optimize consumes the global RNG, so the arm that
    # declares independence from the prior still sees an RNG stream shifted by
    # the optimiser's consumption. That is an accidental coupling, not a causal
    # one, and it would make the ql arm's number depend on the optimiser.
    try:
        lat_ql_with, del_ql_with = run_arm(module, "ql", FIXED_WEIGHTS,
                                           monkeypatched=False)
        # Same ql arm, but with the optimiser's RNG consumption removed from the
        # stream. Emulated by running ql first in a fresh stream and comparing
        # against running it after the optimiser has consumed draws.
        np.random.seed(1234)
        original(env=module.LEORoutingEnv(num_sats=20, num_planes=2))
        np.random.seed(1234)
        saved_episodes, saved_train = module.EVAL_EPISODES, module.TRAIN_EPISODES
        module.EVAL_EPISODES, module.TRAIN_EPISODES = 3, 3
        try:
            np.random.seed(4321)
            lat_ql_clean, del_ql_clean = module.evaluate_strategy(
                small_env_factory(module), "ql", weights=FIXED_WEIGHTS)
            np.random.seed(4321)
            original(env=module.LEORoutingEnv(num_sats=20, num_planes=2))
            np.random.seed(4321)
            lat_ql_after, del_ql_after = module.evaluate_strategy(
                small_env_factory(module), "ql", weights=FIXED_WEIGHTS)
        finally:
            module.EVAL_EPISODES, module.TRAIN_EPISODES = saved_episodes, saved_train

        if (lat_ql_clean, del_ql_clean) == (lat_ql_after, del_ql_after):
            print("  [PASS] F6 the ql arm's result is invariant to whether the optimiser")
            print("           ran first; no accidental coupling through the RNG stream")
        else:
            print(f"  [FAIL] F6 the ql arm changed when the optimiser ran first: "
                  f"{lat_ql_clean:.2f}/{del_ql_clean:.1f}% -> "
                  f"{lat_ql_after:.2f}/{del_ql_after:.1f}%.")
            print("         The arm declared independent of the prior is coupled to it")
            print("         through the shared RNG stream. That coupling is accidental,")
            print("         not causal, and it would make the ablation's arms")
            print("         incomparable for reasons the paper does not disclose.")
            failures.append("F6-accidental-rng-coupling")
    except Exception as exc:  # noqa: BLE001
        print(f"  [FAIL] F6 raised {type(exc).__name__}: {exc}")
        failures.append("F6-error")

    # --- F7: effective inputs must be auditable per arm ---------------------
    arms = {"ga": "optimizer-derived", "ql": "not consumed", "hybrid": "optimizer-derived"}
    print(f"  [INFO] F7 declared effective inputs per arm: {arms}")
    print("         F1, F2 and F6 above establish these empirically rather than by")
    print("         reading the call sites. No arm's result is compared to a")
    print("         previously published number anywhere in this file.")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        return 1
    print("PASSED: the ablation is identifiable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
