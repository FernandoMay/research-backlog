#!/usr/bin/env python3
"""LEO P1 falsifier: is the pipeline actually runnable end to end?

Property under test.

    Every entry point completes, and every artifact a run publishes is derived
    from the same execution as the artifacts beside it.

This row exists because the branch-integrity replay found a defect that seven
green falsifiers could not see. Commit 37aa3f2 deleted `abl_order` while four
lines of `generate_extended_figures` still referenced it. Since then every run of
the extended experiment has written `metrics_extended.json`, generated fig5 and
fig6, and then raised NameError while drawing fig7.

Two things went undetected, and both are about the same seam:

    The artifact is written before the figures. A run that crashes afterwards
    still leaves a correct, freshly-stamped artifact behind. So "the artifact
    regenerated and no number moved" was true and meant nothing about whether the
    pipeline ran. The check I used for row R2 was exactly this check.

    The falsifiers exercise measurement, never rendering. Seven green falsifiers
    and a crashing pipeline were both true at the same time, because nothing in
    the test suite drew a figure.

F1 calls the figure generator directly with synthetic scenario data. It is fast,
it targets the exact seam, and it cannot pass while any name in that function is
undefined. F2 checks the repository rather than the code: no committed figure may
predate the committed artifact it depicts, because that state means the figure
was produced by a different execution than the numbers beside it.

No scientific claim is involved. This is the row that separates "the repair
works" from "the thing that produces the repair's evidence runs".
"""

import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "simulator" / "leo_routing_extended.py"

FIG_DIR = "paper/figures"
EXTENDED_FIGURES = ("fig5_scenario_scale", "fig6_failure_sweep", "fig7_ablation")
ARTIFACT = "data/metrics_extended.json"


def load_module():
    spec = importlib.util.spec_from_file_location("leo_p1_target", TARGET)
    module = importlib.util.module_from_spec(spec)
    sys.modules["leo_p1_target"] = module
    spec.loader.exec_module(module)
    return module


def synthetic(module):
    """Minimal but structurally faithful scenario data."""
    algorithms = ['dijkstra', 'aco', 'dqn', 'ga', 'ql', 'hybrid']
    row = lambda seed: {a: {'latency_ms': 15.0 + seed, 'delivery_pct': 99.0 + seed * 0.01}
                        for a in algorithms}
    scale = {str(n): row(i) for i, n in enumerate((30, 60, 90))}
    failure = {str(f): row(i + 3) for i, f in enumerate((0.02, 0.04, 0.08))}
    ablation = {a: {'latency_ms': 15.0 + i, 'delivery_pct': 99.0 + i * 0.01}
                for i, a in enumerate(module.ABLATION_ARMS)}
    return scale, failure, ablation


def git_last_change(path):
    out = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%h", "--", path],
                         capture_output=True, text=True)
    return out.stdout.strip() or None


def git_ancestor(older, newer):
    if not older or not newer:
        return False
    out = subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor",
                          older, newer], capture_output=True, text=True)
    return out.returncode == 0


def main():
    print("property: every entry point completes, and no published figure")
    print("         predates the artifact it depicts")
    print("=" * 78)

    module = load_module()
    failures = []

    # --- F1: the figure generator runs to completion -------------------------
    scale, failure, ablation = synthetic(module)
    with tempfile.TemporaryDirectory() as tmp:
        try:
            module.generate_extended_figures(tmp, scale, failure, ablation)
            print(f"  [PASS] F1 generate_extended_figures completed without error")
        except Exception as exc:  # noqa: BLE001 - the failure is the finding
            print(f"  [FAIL] F1 generate_extended_figures raised "
                  f"{type(exc).__name__}: {exc}")
            print("         The extended experiment writes its artifact before it draws")
            print("         its figures, so a run that crashes here still leaves a fresh,")
            print("         correct artifact behind it. That is why row R2's check -- the")
            print("         artifact regenerated and no number moved -- could not see this.")
            failures.append("F1-figure-generation-crashes")

        produced = sorted(p.name for p in pathlib.Path(tmp).glob("*.png"))
        expected = {f"{name}.png" for name in EXTENDED_FIGURES}
        missing = sorted(expected - set(produced))
        if missing:
            print(f"  [FAIL] F1 figures not produced: {', '.join(missing)}")
            failures.append("F1-missing-figures")
        else:
            print(f"  [PASS] F1 all {len(expected)} extended figures written: "
                  f"{', '.join(sorted(produced))}")

    # --- F2: the committed figures are what the committed artifact produces ---
    # The first version of this assertion compared git commit ordering -- a figure
    # must not predate the artifact. It failed, and it was the assertion's fault.
    # A figure regenerated to byte-identical content is current even though git
    # records no new commit for it, so commit ordering reports staleness that does
    # not exist. fig5 and fig6 came out byte-identical from the run that fixed
    # fig7, and an ordering test still called them stale.
    #
    # The property is about content, so the check is about content: read the
    # committed artifact, regenerate the figures from it, and compare bytes. This
    # needs no experiment re-run, because the figures are drawn from the scenario
    # data the artifact already holds.
    print(f"  [INFO] F2 regenerating figures from the committed artifact and")
    print(f"         comparing bytes (no experiment re-run):")
    try:
        with open(ROOT / ARTIFACT) as handle:
            artifact = json.load(handle)
        scale = artifact["scenario_scale"]
        failure = artifact["scenario_failure"]
        ablation = artifact["ablation"]
    except (OSError, KeyError) as exc:
        print(f"  [FAIL] F2 could not read the committed artifact: {exc}")
        failures.append("F2-artifact-unreadable")
        scale = failure = ablation = None

    if scale is not None:
        with tempfile.TemporaryDirectory() as tmp:
            try:
                module.generate_extended_figures(tmp, scale, failure, ablation)
            except Exception as exc:  # noqa: BLE001
                print(f"  [FAIL] F2 regeneration from the artifact raised "
                      f"{type(exc).__name__}: {exc}")
                failures.append("F2-regeneration-crashes")

            divergent, verified = [], []
            for name in EXTENDED_FIGURES:
                committed = ROOT / FIG_DIR / f"{name}.png"
                regenerated = pathlib.Path(tmp) / f"{name}.png"
                if not committed.exists() or not regenerated.exists():
                    divergent.append(f"{name} (missing)")
                    continue
                same = committed.read_bytes() == regenerated.read_bytes()
                if same:
                    verified.append(name)
                else:
                    divergent.append(name)

            for name in verified:
                print(f"         {name}.png  byte-identical to the committed figure")
            for name in divergent:
                print(f"         {name}.png  DIFFERS from the committed figure")

        if divergent:
            print(f"  [FAIL] F2 {len(divergent)} committed figure(s) are not what the "
                  f"committed artifact produces:")
            print(f"         {', '.join(divergent)}")
            print("         The artifact and the figure beside it were drawn by different")
            print("         executions, so the pairing misreports which run produced what.")
            print("         Neither is wrong alone; the pairing is.")
            failures.append("F2-figure-diverges-from-artifact")
        else:
            print(f"  [PASS] F2 all {len(verified)} committed figures are exactly what "
                  f"the committed artifact produces")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        print()
        print("Seven green falsifiers and a crashing pipeline were both true at the same")
        print("time, because the suite measures and never renders. This row closes that")
        print("seam. It makes no scientific claim.")
        return 1
    print("PASSED: the pipeline runs and its outputs agree on their origin")
    return 0


if __name__ == "__main__":
    sys.exit(main())
