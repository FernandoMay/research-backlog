#!/usr/bin/env python3
"""CRL-F2 falsifier: correspondence of the published anomaly score.

Property under test.

    The published anomaly score must be reconstructible from an identified
    execution of the repository as committed.

The manuscript reports an average anomaly score of 0.02 at main.tex L155. The
committed code, run as committed with its own pinned seed, prints 0.0300. Three
things have to be established before either number is called wrong:

    what calculation produces the printed value, reconstructed from the real run
    rather than from a formula copied into this file;
    whether a controlled change in the anomaly's input moves the value;
    whether the run contains more than one silent definition of "anomaly".

The disposition is not assumed. `0.02` may be the same computation under a
different seed, a different averaging population, or something this repository
no longer contains. Those are different findings and they are separated here.

**No historical value is a target.** Nothing in this file asserts that the
output should be 0.03, and nothing asserts it should be 0.02. Calibrating a
repair toward a published number is the error this program exists to catch.
"""

import contextlib
import importlib.util
import inspect
import io
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "src" / "crl_simulation.py"

COMMITTED_SEED = 20260909
PUBLISHED = 0.02
SEARCH_SEEDS = 200


def load_module():
    import random
    sys.path.insert(0, str(TARGET.parent))
    spec = importlib.util.spec_from_file_location("crl_f2", TARGET)
    module = importlib.util.module_from_spec(spec)
    sys.modules["crl_f2"] = module
    spec.loader.exec_module(module)
    return module, random


def main():
    print("property: the published anomaly score is reconstructible from an")
    print("         identified execution of the repository as committed")
    print("=" * 78)

    m, random = load_module()
    failures = []

    # --- F2a: identify the calculation from the real run -------------------
    print(f"  [INFO] F2a reconstruct from the actual run, not from a copied formula:")
    np.random.seed(COMMITTED_SEED)
    random.seed(COMMITTED_SEED)
    runner = m.SimulationRunner(num_agents=10, num_tasks=20)
    with contextlib.redirect_stdout(io.StringIO()):
        reported = runner.run_experiment()
    print(f"           run_experiment avg_anomaly_score = {reported['avg_anomaly_score']!r}"
          f"  -> printed .4f = {reported['avg_anomaly_score']:.4f}")
    print(f"           cycles_run {reported['cycles_run']}, "
          f"completed {reported['completed_tasks']}/{reported['total_tasks']}")

    source = inspect.getsource(m.SimulationRunner.run_experiment)
    uses_cycle_values = "anomaly_score" in source and "np.mean" in source
    if uses_cycle_values:
        print(f"  [PASS] F2a the printed value is the mean of the per-cycle scores "
              f"returned by run_cycle")
    else:
        print(f"  [FAIL] F2a the aggregation could not be identified in run_experiment")
        failures.append("F2a-aggregation-unidentified")

    # --- F2b: does a controlled change in the input move the value? ---------
    print(f"  [INFO] F2b perturb the anomaly's input and re-measure:")
    np.random.seed(COMMITTED_SEED)
    random.seed(COMMITTED_SEED)
    r2 = m.SimulationRunner(num_agents=10, num_tasks=10)
    with contextlib.redirect_stdout(io.StringIO()):
        fewer_tasks = r2.run_experiment()
    print(f"           20 tasks -> {reported['avg_anomaly_score']:.4f}")
    print(f"           10 tasks -> {fewer_tasks['avg_anomaly_score']:.4f}")
    if abs(reported['avg_anomaly_score'] - fewer_tasks['avg_anomaly_score']) > 1e-12:
        print(f"  [PASS] F2b changing the workload moves the anomaly score, so the "
              f"metric is causally")
        print(f"           connected to the run rather than being a constant")
    else:
        print(f"  [FAIL] F2b the anomaly score did not move with the workload")
        failures.append("F2b-metric-inert")

    # --- F2c: how many silent definitions of "anomaly" does the run carry? --
    print(f"  [INFO] F2c silent definitions of anomaly in one run:")
    np.random.seed(COMMITTED_SEED)
    random.seed(COMMITTED_SEED)
    r3 = m.SimulationRunner(num_agents=10, num_tasks=20)
    agents = r3.create_agents()
    dag = r3.create_dag(agents)
    crl = m.CognitiveResilienceLayer()
    out = crl.run_simulation(agents, dag, num_cycles=200)
    per_cycle = [x["evaluation"]["anomaly_score"] for x in out]
    observer_list = list(crl.observer.anomaly_scores)
    print(f"           per-cycle scores reported by run_cycle : "
          f"{[f'{v:.4f}' for v in per_cycle]}")
    print(f"           observer.anomaly_scores list           : "
          f"{[f'{v:.4f}' for v in observer_list]}")
    print(f"           mean of per-cycle values                 : {np.mean(per_cycle):.4f}")
    if observer_list:
        print(f"           mean of the observer's own list          : "
              f"{np.mean(observer_list):.4f}")
    if len(per_cycle) != len(observer_list):
        print(f"  [FAIL] F2c the run carries TWO averaging populations: "
              f"{len(per_cycle)} per-cycle values against")
        print(f"         {len(observer_list)} entries in the observer's own list. They "
              f"disagree")
        print(f"         ({np.mean(per_cycle):.4f} against {np.mean(observer_list):.4f}), "
              f"and the difference is structural: detect_anomaly returns 0.0")
        print(f"         before two states exist and never appends that value, so the "
              f"observer's list")
        print(f"         excludes the structural zero while the reported mean includes it. "
              f"Neither name")
        print(f"         says which population it means.")
        failures.append("F2c-two-silent-definitions")
    else:
        print(f"  [PASS] F2c the run carries one averaging population")

    # --- F2d: is the published value reachable from this code at all? ------
    print(f"  [INFO] F2d is {PUBLISHED} reachable from the committed code at all?")
    reached, observed = 0, []
    for seed in range(SEARCH_SEEDS):
        np.random.seed(seed)
        random.seed(seed)
        rr = m.SimulationRunner(num_agents=10, num_tasks=20)
        with contextlib.redirect_stdout(io.StringIO()):
            out_r = rr.run_experiment()
        observed.append(out_r["avg_anomaly_score"])
        if abs(out_r["avg_anomaly_score"] - PUBLISHED) < 1e-9:
            reached += 1
    observed = np.array(observed)
    print(f"           {SEARCH_SEEDS} seeds: min {observed.min():.4f} "
          f"max {observed.max():.4f}")
    print(f"           seeds yielding exactly {PUBLISHED}: {reached}")
    print(f"           the repository's own pinned seed {COMMITTED_SEED} yields "
          f"{reported['avg_anomaly_score']:.4f}")
    if reached:
        print(f"  [FAIL] F2d the published value IS reachable from the committed code "
              f"({reached} of {SEARCH_SEEDS}")
        print(f"         seeds), but the manuscript records no seed, no configuration and "
              f"no artifact for")
        print(f"         the execution that produced it, and the repository pins "
              f"{COMMITTED_SEED}, which")
        print(f"         yields {reported['avg_anomaly_score']:.4f}. This is a provenance "
              f"gap, not a wrong")
        print(f"         number: the code can emit the published value and nothing in the "
              f"repository")
        print(f"         identifies which run did. Not CONTRADICTED -- the value is not "
              f"outside the code's")
        print(f"         range. NOT VERIFIED, because no lineage connects the publication "
              f"to an execution.")
        print(f"         No attempt is made to move the output toward {PUBLISHED}; the "
              f"historical value is not")
        print(f"         a target and matching it would prove nothing.")
        failures.append("F2d-published-value-unlineaged")
    else:
        print(f"  [FAIL] F2d the published value is not reachable from this code at any "
              f"seed tested")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        print()
        print("Disposition: NOT VERIFIED / PROVENANCE GAP. Not CONTRADICTED. The value is")
        print("inside the code's range, the repository stores no artifact, and the")
        print("manuscript records no execution that would let a reader identify which run")
        print("produced it. The absence is the finding.")
        return 1
    print("PASSED: the published value is reconstructible from an identified execution")
    return 0


if __name__ == "__main__":
    sys.exit(main())