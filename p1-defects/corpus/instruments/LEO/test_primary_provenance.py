#!/usr/bin/env python3
"""LEO L1p falsifier: execution provenance of the PRIMARY artifact.

Property under test.

    Every quantitative artifact must identify the source revision and execution
    environment sufficient to distinguish the run from another implementation or
    dependency state.

This is the same contract as row L1c on the extended artifact, and it now
matters for a reason L1c did not. M1-B regenerated `data/metrics.json`, produced
new resilience values that discriminate between arms for the first time, and the
artifact recording them cannot say which commit, which dependencies, or whether
the tree was clean produced them. Deterministic and traceable are different
properties, and the two have now been separated by accident rather than by
design.

The primary artifact also stopped being a trivial derivative of the extended
one. It carries the three principal arms, the resilience reconciliation and the
numbers the paper's table quotes. It is primary evidence now, and it needs an
identity of its own.

Two design points that were decided rather than discovered, both recorded here
because they are load-bearing:

    Determinism. No wall-clock field may appear in metrics.json. Two runs of the
    same commit must stay byte-identical, and check A is the only thing standing
    between "deterministic" and "assumed deterministic". A timestamp inside the
    artifact would end reproducibility checking in exchange for a fact the run
    log already records. F3 asserts its absence.

    Cross-artifact coupling. The user required metrics.json and
    metrics_extended.json to share source_commit, dependency_versions, seed and
    configuration. Three of those are implemented literally. `configuration` is
    not, and deliberately so: the extended artifact's configuration names the
    scales 30/60/90 and failure rates 2/4/8% that its own experiment sweeps, and
    the primary artifact runs neither. Forcing the two to declare an identical
    configuration would record something false in one of them. What is shared is
    an `environment` block -- the fields that identify the run rather than the
    experiment. F4 checks the coupling on that block and reports value agreement
    separately, because the two artifacts come from separate script invocations
    and are entitled to record different revisions.
"""

import copy
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRIMARY = ROOT / "data" / "metrics.json"
EXTENDED = ROOT / "data" / "metrics_extended.json"

REQUIRED = {
    "source_commit",
    "source_dirty",
    "python_version",
    "dependency_versions",
    "seed",
    "configuration",
    "generator",
}

SHARED = ("source_commit", "dependency_versions", "seed", "python_version",
          "platform", "architecture")

SHA1 = re.compile(r"^[0-9a-f]{40}$")
PYVER = re.compile(r"^3\.\d+\.\d+")
# Anything that would make two runs of one commit differ.
NONDETERMINISTIC = ("timestamp", "generated_at", "run_at", "date", "time",
                    "elapsed", "duration", "hostname", "wall")


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
    if set(a) != set(b):
        return False
    return all(a[k] == b[k] for k in a)


def main():
    print("property: the primary artifact identifies the code and environment")
    print("         that produced it, and is coupled to the extended one")
    print("=" * 78)

    if not PRIMARY.exists():
        print(f"  [FAIL] artifact absent: {PRIMARY.relative_to(ROOT)}")
        return 1

    with open(PRIMARY) as handle:
        primary = json.load(handle)

    failures = []
    provenance = primary.get("provenance")

    if not isinstance(provenance, dict):
        print("  [FAIL] F1 the primary artifact carries no provenance block")
        print("         Its top-level keys are:", sorted(primary))
        print("         It records arm results, the constellation and the optimiser's")
        print("         weights, and nothing about which commit, which dependency state,")
        print("         or whether the tree was clean produced them. Check A shows the run")
        print("         is reproducible; it does not show which run this is.")
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

    # --- F1b: populated ------------------------------------------------------
    unpopulated = []
    if provenance.get("source_commit") is not None and not SHA1.match(
            str(provenance["source_commit"])):
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

    # --- F2: the shared environment block exists on both sides --------------
    env = provenance.get("environment")
    if not isinstance(env, dict) or not env:
        print("  [FAIL] F2 no shared `environment` block on the primary artifact.")
        print("         Without it the two artifacts cannot be compared field by field,")
        print("         and the coupling the row exists to create is absent.")
        failures.append("F2-no-environment-block")
    else:
        print(f"  [PASS] F2 shared environment block present with "
              f"{len(env)} field(s): {', '.join(sorted(env))}")

    # --- F3: nothing that breaks reproducibility ----------------------------
    offenders = sorted({tok for tok in NONDETERMINISTIC
                        if any(tok in str(k).lower() for k in provenance)})
    if offenders:
        print(f"  [FAIL] F3 the provenance carries wall-clock state: "
              f"{', '.join(offenders)}")
        print("         Two runs of one commit would stop being byte-identical, which")
        print("         ends check A. The run time belongs in the run log.")
        failures.append("F3-nondeterministic-field")
    else:
        print("  [PASS] F3 no wall-clock field in the artifact; reproducibility is testable")

    # --- F4: cross-artifact coupling ----------------------------------------
    if not EXTENDED.exists():
        print("  [WARN] F4 extended artifact absent; coupling not checked")
    elif not isinstance(env, dict):
        print("  [FAIL] F4 coupling cannot be checked without the environment block")
        failures.append("F4-no-env-for-coupling")
    else:
        with open(EXTENDED) as handle:
            extended = json.load(handle)
        ext_prov = extended.get("provenance", {})
        ext_env = ext_prov.get("environment")

        if not isinstance(ext_env, dict) or not ext_env:
            print("  [FAIL] F4 the extended artifact has no matching `environment` "
                  "block, so the two")
            print("         cannot be compared. L1c predates this coupling; the extended")
            print("         side has to be brought to the same shape.")
            failures.append("F4-extended-no-environment")
        else:
            only_primary = sorted(set(env) - set(ext_env))
            only_extended = sorted(set(ext_env) - set(env))
            if only_primary or only_extended:
                print(f"  [FAIL] F4 the environment blocks disagree in shape. "
                      f"primary only: {only_primary}; extended only: {only_extended}")
                failures.append("F4-environment-shape-mismatch")
            else:
                print(f"  [PASS] F4 both artifacts expose the same "
                      f"{len(env)} environment field(s)")

            for field in SHARED:
                if field not in env:
                    continue
                a, b = env[field], ext_env.get(field)
                if a == b:
                    print(f"  [INFO] F4 {field:<20} agrees across both artifacts")
                else:
                    print(f"  [INFO] F4 {field:<20} differs -- primary "
                          f"{str(a)[:24]} vs extended {str(b)[:24]}")
            print("         The two artifacts come from separate script invocations, so")
            print("         differing revisions are correct. What matters is that the")
            print("         fields are comparable and populated on both sides.")

    # --- F5: distinguishability ---------------------------------------------
    mutations = []
    if provenance.get("source_commit") and SHA1.match(str(provenance["source_commit"])):
        mutations.append(("source_commit", provenance["source_commit"],
                          "0" * 40 if provenance["source_commit"] != "0" * 40 else "1" * 40))
    deps = provenance.get("dependency_versions")
    if isinstance(deps, dict) and deps:
        name = sorted(deps)[0]
        mutations.append((f"dependency_versions[{name}]", deps[name], "99.99.99"))
    if provenance.get("seed") is not None:
        mutations.append(("seed", provenance["seed"], 4242))
    cfg = provenance.get("configuration")
    if isinstance(cfg, dict) and cfg:
        key = sorted(cfg)[0]
        mutations.append((f"configuration[{key}]", cfg[key], "perturbed"))

    if not mutations:
        print("  [FAIL] F5 nothing to mutate; the provenance is too thin to "
              "distinguish runs")
        failures.append("F5-no-mutation-surface")
    else:
        indistinguishable = []
        for label, _before, after in mutations:
            mutant = copy.deepcopy(provenance)
            if label.startswith("dependency_versions["):
                mutant["dependency_versions"][sorted(mutant["dependency_versions"])[0]] = after
            elif label.startswith("configuration["):
                mutant["configuration"][sorted(mutant["configuration"])[0]] = after
            elif label == "seed":
                mutant["seed"] = after
            else:
                mutant["source_commit"] = after
            if same_run(provenance, mutant):
                indistinguishable.append(label)

        if indistinguishable:
            print(f"  [FAIL] F5 mutation went unnoticed, artifact still reads as the "
                  f"same run: {', '.join(indistinguishable)}")
            failures.append("F5-indistinguishable")
        else:
            print(f"  [PASS] F5 all {len(mutations)} mutations break provenance "
                  f"equivalence:")
            for label, _b, _a in mutations:
                print(f"           {label}")

    # --- F6: the recorded revision is reachable ----------------------------
    recorded = provenance.get("source_commit")
    head = git("rev-parse", "HEAD")
    if not recorded:
        print("  [FAIL] F6 no source_commit recorded; the artifact is untraceable")
        failures.append("F6-untraceable")
    elif reachable(recorded):
        print(f"  [PASS] F6 recorded source_commit {recorded[:12]} is reachable in "
              f"this history (HEAD {str(head)[:12]})")
        if provenance.get("source_dirty"):
            print("  [WARN] F6 the tree was dirty at generation time; source_commit "
                  "records HEAD, not the exact bytes")
    else:
        print(f"  [FAIL] F6 recorded source_commit {recorded[:12]} is not reachable "
              f"from HEAD {str(head)[:12]}")
        failures.append("F6-unreachable")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        return 1
    print("PASSED: the primary artifact identifies its own origin")
    return 0


if __name__ == "__main__":
    sys.exit(main())
