#!/usr/bin/env python3
"""LEO L1c falsifier: execution provenance of the extended artifact.

Property under test.

    Every quantitative artifact must identify the source revision and execution
    environment sufficient to distinguish the run from another implementation or
    dependency state -- and, where an artifact aggregates several experiments,
    must record the effective configuration *per scenario* rather than one
    ambiguous global block.

The second clause is the reason this is not just a copy of the SGN row 6c
falsifier. `run_extended` does not run one experiment. It runs a constellation
scale sweep, a failure-rate sweep and an ablation, and it calls
`nsga2_optimize` once per scenario -- seven separate optimizations, each with its
own weight vector. A single global `configuration` block would record the seed
and the NSGA-II parameters but would not record *which* weight vector fed *which*
scenario, and that mapping is precisely what row R1 changed. Recording a global
block here would satisfy a token field list while losing the only thing worth
recording.

As in SGN 6c, the property is that the origin is distinguishable, not that every
change moves a number. The mutation test asserts that altering a recorded commit,
a dependency version, the seed, or a per-scenario configuration breaks
provenance equivalence. It does not require each mutation to move a metric.
"""

import copy
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
METRICS = ROOT / "data" / "metrics_extended.json"

REQUIRED = {
    "source_commit",
    "python_version",
    "dependency_versions",
    "seed",
    "configuration",
    "generator",
}

PREFERRED = {"source_dirty", "platform", "architecture", "nsga2"}

SCENARIO_KEYS = ("scenario_scale", "scenario_failure", "ablation")

SCENARIO_FIELDS = {
    "num_sats",
    "failure_rate",
    "recovery_rate",
    "algorithms",
    "optimized_weights",
}

SHA1 = re.compile(r"^[0-9a-f]{40}$")
PYVER = re.compile(r"^3\.\d+\.\d+")


def git(*args):
    try:
        out = subprocess.run(["git", "-C", str(ROOT), *args],
                             capture_output=True, text=True)
    except OSError:
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def reachable(revision):
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", revision, "HEAD"],
            capture_output=True, text=True)
    except OSError:
        return False
    return out.returncode == 0


def same_run(a, b):
    """True when two provenance blocks describe the same run."""
    if set(a) != set(b):
        return False
    for key in a:
        if a[key] != b[key]:
            return False
    return True


def main():
    print("property: an artifact identifies the code, the environment, and the")
    print("         effective per-scenario configuration that produced it")
    print("=" * 78)

    if not METRICS.exists():
        print(f"  [FAIL] artifact absent: {METRICS.relative_to(ROOT)}")
        return 1

    with open(METRICS) as handle:
        artifact = json.load(handle)

    failures = []
    provenance = artifact.get("provenance")

    if not isinstance(provenance, dict):
        print("  [FAIL] F1 the artifact carries no provenance block")
        print("         It records scenario results only. Nothing in it identifies")
        print("         which code, which dependency state, or which weight vector")
        print("         produced each scenario, so two different runs of this")
        print("         experiment are indistinguishable after the fact.")
        print(f"         Present top-level keys: {sorted(artifact)}")
        print("=" * 78)
        print("FAILED: F1-no-provenance")
        return 1

    present = set(provenance)
    missing = sorted(REQUIRED - present)
    if missing:
        print(f"  [FAIL] F1 provenance identifies {len(present)} field(s), "
              f"missing {len(missing)}: {', '.join(missing)}")
        failures.append("F1-missing-fields")
    else:
        print(f"  [PASS] F1 all {len(REQUIRED)} required provenance fields present")

    # --- F1b: populated, not placeholder -------------------------------------
    unpopulated = []
    commit = provenance.get("source_commit")
    if commit is not None and not SHA1.match(str(commit)):
        unpopulated.append("source_commit")
    pyver = provenance.get("python_version")
    if pyver is not None and not PYVER.match(str(pyver)):
        unpopulated.append("python_version")
    if not (isinstance(provenance.get("dependency_versions"), dict)
            and provenance["dependency_versions"]):
        unpopulated.append("dependency_versions")
    if provenance.get("seed") is None:
        unpopulated.append("seed")
    if not (isinstance(provenance.get("configuration"), dict)
            and provenance["configuration"]):
        unpopulated.append("configuration")
    if not str(provenance.get("generator") or "").strip():
        unpopulated.append("generator")

    if unpopulated:
        print(f"  [FAIL] F1b present but unpopulated: {', '.join(unpopulated)}")
        failures.append("F1b-unpopulated")
    else:
        print("  [PASS] F1b populated and well-formed")

    absent = sorted(PREFERRED - present)
    if absent:
        print(f"  [WARN] F1c preferred fields absent: {', '.join(absent)}")
    else:
        print(f"  [PASS] F1c preferred fields present: {', '.join(sorted(PREFERRED))}")

    # --- F2: per-scenario effective configuration -----------------------------
    scenarios = provenance.get("scenarios")
    if not isinstance(scenarios, dict) or not scenarios:
        print("  [FAIL] F2 no per-scenario configuration recorded.")
        print(f"         run_extended calls nsga2_optimize once per scenario -- "
              f"{len(SCENARIO_KEYS)} scenario families, seven")
        print("         optimizations in total -- so a single global configuration "
              "cannot say which weight")
        print("         vector fed which scenario. That mapping is what row R1 "
              "changed.")
        failures.append("F2-no-scenarios")
    else:
        expected_scenarios = set()
        for family in SCENARIO_KEYS:
            block = artifact.get(family)
            if isinstance(block, dict):
                for scenario_id in block:
                    expected_scenarios.add(f"{family}/{scenario_id}")

        recorded = set(scenarios)
        if recorded == expected_scenarios:
            print(f"  [PASS] F2 provenance covers exactly the {len(recorded)} "
                  f"scenario(s) present in the artifact")
        else:
            extra = sorted(recorded - expected_scenarios)
            gaps = sorted(expected_scenarios - recorded)
            print(f"  [FAIL] F2 scenario coverage mismatch. "
                  f"unrecorded: {gaps if gaps else 'none'}; "
                  f"recorded but absent from the artifact: {extra if extra else 'none'}")
            failures.append("F2-coverage-mismatch")

        incomplete = []
        for name, cfg in sorted(scenarios.items()):
            if not isinstance(cfg, dict):
                incomplete.append(f"{name}:not-a-mapping")
                continue
            gaps = sorted(SCENARIO_FIELDS - set(cfg))
            if gaps:
                incomplete.append(f"{name}:missing {','.join(gaps)}")
                continue
            weights = cfg.get("optimized_weights")
            if not (isinstance(weights, list) and len(weights) == 3):
                incomplete.append(f"{name}:optimized_weights malformed")
            else:
                total = sum(float(w) for w in weights)
                if abs(total - 1.0) > 1e-6:
                    incomplete.append(f"{name}:weights sum to {total:.6f}")
            if not cfg.get("algorithms"):
                incomplete.append(f"{name}:no algorithms recorded")

        if incomplete:
            print(f"  [FAIL] F2b per-scenario configuration incomplete for "
                  f"{len(incomplete)} scenario(s):")
            for item in incomplete[:8]:
                print(f"           {item}")
            failures.append("F2b-incomplete")
        else:
            print(f"  [PASS] F2b all {len(scenarios)} scenario(s) record "
                  f"{len(SCENARIO_FIELDS)} effective-configuration fields, "
                  f"weights normalised")

        # --- F2c: the recorded algorithms match the artifact's own rows -----
        # The three families do not share a shape. scenario_scale and
        # scenario_failure are keyed by algorithm name, so the recorded set must
        # equal the block's keys. The ablation is keyed by arm, and each arm's
        # block holds metric names, so the recorded set for ablation/<arm> must
        # be exactly that one arm. Comparing an ablation arm against its metric
        # names would be a shape error, not a provenance error.
        METRIC_NAMES = {"latency_ms", "delivery_pct"}
        mismatch = []
        for name, cfg in sorted(scenarios.items()):
            family, _, scenario_id = name.partition("/")
            block = artifact.get(family, {}).get(scenario_id)
            if not isinstance(block, dict) or not isinstance(cfg, dict):
                continue
            recorded_algos = set(cfg.get("algorithms") or [])
            block_keys = set(block)
            if block_keys & METRIC_NAMES:
                expected_algos = {scenario_id}
            else:
                expected_algos = block_keys
            if recorded_algos != expected_algos:
                mismatch.append(f"{name}: recorded {sorted(recorded_algos)} "
                                f"vs expected {sorted(expected_algos)}")
        if mismatch:
            print(f"  [FAIL] F2c recorded algorithms disagree with the artifact rows:")
            for item in mismatch[:4]:
                print(f"           {item}")
            failures.append("F2c-algorithm-mismatch")
        else:
            print(f"  [PASS] F2c recorded algorithms match the artifact's own rows "
                  f"(scale and failure families keyed by algorithm; ablation keyed by arm)")

    # --- F3: distinguishability ---------------------------------------------
    mutations = []
    if "source_commit" in provenance and SHA1.match(str(provenance["source_commit"])):
        other = "0" * 40 if provenance["source_commit"] != "0" * 40 else "1" * 40
        mutations.append(("source_commit", provenance["source_commit"], other, None))

    deps = provenance.get("dependency_versions")
    if isinstance(deps, dict) and deps:
        name = sorted(deps)[0]
        mutations.append((f"dependency_versions[{name}]", deps[name], "99.99.99", None))

    if "seed" in provenance:
        mutations.append(("seed", provenance["seed"], 4242, None))

    if isinstance(provenance["configuration"], dict) and provenance["configuration"]:
        key = sorted(provenance["configuration"])[0]
        mutations.append((f"configuration[{key}]", provenance["configuration"][key],
                          "perturbed", None))

    if isinstance(provenance.get("scenarios"), dict) and provenance["scenarios"]:
        name = sorted(provenance["scenarios"])[0]
        mutations.append(("scenarios[{}].optimized_weights".format(name),
                          provenance["scenarios"][name].get("optimized_weights"),
                          [0.5, 0.3, 0.2],
                          name))

    if not mutations:
        print("  [FAIL] F3 nothing to mutate; the provenance is too thin to "
              "distinguish runs")
        failures.append("F3-no-mutation-surface")
    else:
        indistinguishable = []
        for label, _before, after, scenario in mutations:
            mutant = copy.deepcopy(provenance)
            if label.startswith("dependency_versions["):
                mutant["dependency_versions"][sorted(mutant["dependency_versions"])[0]] = after
            elif label.startswith("scenarios["):
                mutant["scenarios"][scenario]["optimized_weights"] = after
            elif label.startswith("configuration["):
                mutant["configuration"][sorted(mutant["configuration"])[0]] = after
            elif label == "seed":
                mutant["seed"] = after
            else:
                mutant["source_commit"] = after
            if same_run(provenance, mutant):
                indistinguishable.append(label)

        if indistinguishable:
            print(f"  [FAIL] F3 mutation went unnoticed, artifact still reads as the "
                  f"same run: {', '.join(indistinguishable)}")
            failures.append("F3-indistinguishable")
        else:
            print(f"  [PASS] F3 all {len(mutations)} mutations break provenance "
                  f"equivalence:")
            for label, _b, _a, _s in mutations:
                print(f"           {label}")

    # --- F4: the recorded revision is reachable in this history --------------
    recorded_commit = provenance.get("source_commit")
    head = git("rev-parse", "HEAD")
    if not recorded_commit:
        print("  [FAIL] F4 no source_commit recorded; the artifact is untraceable")
        failures.append("F4-untraceable")
    elif reachable(recorded_commit):
        print(f"  [PASS] F4 recorded source_commit {recorded_commit[:12]} is reachable "
              f"in this history (HEAD {str(head)[:12]})")
        if provenance.get("source_dirty"):
            print("  [WARN] F4 the tree was dirty at generation time; source_commit "
                  "records HEAD, not the exact bytes")
    else:
        print(f"  [FAIL] F4 recorded source_commit {recorded_commit[:12]} is not "
              f"reachable from HEAD {str(head)[:12]}")
        failures.append("F4-unreachable")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        return 1
    print("PASSED: the artifact identifies its own origin, per scenario")
    return 0


if __name__ == "__main__":
    sys.exit(main())
