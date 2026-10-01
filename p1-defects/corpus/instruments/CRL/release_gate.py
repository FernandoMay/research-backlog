#!/usr/bin/env python3
"""CRL publication gate.

Verifies that closing the branch does not erase the audit's findings.

The specific danger this gate exists to prevent: after row R2 both arms report
100.00% completion, and a gate that merely checks "the numbers are 100%" or
"the repair worked" would certify the chain having silently converted a
non-discriminating metric into evidence of a resilience benefit. That conversion
is the one thing the CRL audit exists to refuse.

So the gate asserts the dispositions as text, not just the code as behaviour.
The repaired 100% must appear nowhere as evidence of benefit.

Check 1 is the destination, before anything else, because CRL's gate list in
LEO's case omitted it and that omission cost a force-push to master.
"""

import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PY = "/private/tmp/venv2/bin/python"

EXPECTED_BRANCH = "fix/crl-audit-sweep"
FORBIDDEN = "main"
DEFAULT_BRANCH = "main"
CHAIN = [
    ("b5d97c8", "inventory"),
    ("b676a0c", "F1 causal access"),
    ("9ffc31f", "F2 population and provenance"),
    ("b197d10", "R2 activation and equal dose"),
    ("b2b8103", "claim adjudication"),
]

REQUIRED_DISPOSITIONS = {
    "mechanism": "SUPPORTED",
    "causal access": "SUPPORTED",
    "activation": "SUPPORTED",
    "equal exposure": "SUPPORTED",
    "metric discrimination": "NEW EXPERIMENT REQUIRED",
    "resilience benefit": "NOT SUPPORTED",
    "anomaly 0.02": "NOT VERIFIED",
    "anomaly semantics": "CONTRADICTED",
}

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"\n          {detail}" if detail and not ok else ""))
    return ok


def git(*a):
    out = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else None


def main():
    print("CRL publication gate")
    print("=" * 78)

    # 1. destination, before anything else --------------------------------
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    check("1a gate runs on the audit branch, not the forbidden one",
          branch == EXPECTED_BRANCH and branch != FORBIDDEN,
          f"branch is {branch!r}, expected {EXPECTED_BRANCH!r}")
    # This repository's default branch is `main`, not `master`. The first version
    # of this gate asserted against `master`, which does not exist here, so the
    # check silently read an empty string and reported the default branch as
    # unverified rather than as wrong. A gate that cannot fail is a gate that
    # has not run.
    remote_default = git("ls-remote", "origin", DEFAULT_BRANCH)
    check(f"1b remote {DEFAULT_BRANCH} untouched at the pre-audit baseline",
          bool(remote_default) and remote_default.startswith("cf37818"),
          f"remote {DEFAULT_BRANCH} is {remote_default!r}")
    check("1c working tree clean",
          git("status", "--porcelain") in ("", None),
          "uncommitted paths present")

    # 2. chain --------------------------------------------------------------
    # `cat-file -e` writes nothing to stdout, so testing the helper's return value
    # for truthiness marks every commit missing. The first version did exactly that
    # and reported all five absent while `merge-base --is-ancestor` accepted all
    # five. The check now asks about the exit status.
    def exists(sha):
        return subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e",
                               f"{sha}^{{commit}}"], capture_output=True).returncode == 0

    missing = [f"{sha} {lbl}" for sha, lbl in CHAIN if not exists(sha)]
    check("2 every audit commit exists in the history", not missing, f"missing: {missing}")

    reachable = [f"{sha}" for sha, _ in CHAIN
                 if subprocess.run(["git", "-C", str(ROOT), "merge-base",
                                    "--is-ancestor", sha, "HEAD"]).returncode != 0]
    check("2b every audit commit is an ancestor of HEAD", not reachable,
          f"not ancestors: {reachable}")

    # 3. falsifiers ---------------------------------------------------------
    green = []
    for t in ("test_causal_access.py", "test_experimental_activation.py"):
        if subprocess.run([PY, f"tests/{t}"], capture_output=True).returncode == 0:
            green.append(t)
    check("3 RF1-RF5 falsifiers green from a clean state",
          len(green) == 2, f"green: {green}")
    # F2 is a finding, not a repair, and must stay red with its log
    f2_red = subprocess.run([PY, "tests/test_anomaly_correspondence.py"],
                            capture_output=True).returncode != 0
    check("3b F2 remains red as a retained finding",
          f2_red, "F2 went green; its findings were repaired and should have been kept")
    check("3c F2's falsifier log is committed, not overwritten",
          (ROOT / "FALSIFIER-LOG-CRLF2.md").exists(),
          "FALSIFIER-LOG-CRLF2.md missing")

    # 4. artifact -----------------------------------------------------------
    art = ROOT / "data" / "resilience_experiment.json"
    if art.exists():
        payload = json.loads(art.read_text())
        prov = payload.get("provenance", {})
        required = {"source_commit", "source_dirty", "python_version",
                    "dependency_versions", "platform", "architecture", "seed",
                    "generator", "configuration"}
        gaps = sorted(required - set(prov))
        check("4a artifact carries full provenance", not gaps, f"missing: {gaps}")
        nondet = [k for k in prov
                  if any(t in str(k).lower() for t in
                         ("timestamp", "generated_at", "date", "time", "elapsed"))]
        check("4b no wall-clock field in the artifact", not nondet,
              f"nondeterministic fields: {nondet}")
        digest = hashlib.sha256(art.read_bytes()).hexdigest()
        check("4c artifact digest recorded for the record", True, digest[:32])
    else:
        check("4a artifact present", False, "data/resilience_experiment.json absent")

    # 5. non-contamination --------------------------------------------------
    tex = git("diff", "--name-only", "cf37818", "HEAD", "--", "*.tex")
    check("5a no manuscript modified", not tex, f"modified: {tex}")
    e1 = [p for p in (git("diff", "--name-only", "cf37818", "HEAD") or "").split("\n")
          if p and any(t in p.lower() for t in ("e1-", "dataset", "rubric"))]
    check("5b E1 corpus untouched", not e1, f"paths: {e1}")
    check("5c the published 0.02 was not turned into a target",
          (ROOT / "tests/test_anomaly_correspondence.py").exists()
          and "0.02" in (ROOT / "tests/test_anomaly_correspondence.py").read_text(),
          "the F2 falsifier no longer carries the published value")

    # 6. adjudication preserved as text -------------------------------------
    adj = (ROOT / "CLAIM-ADJUDICATION-CRL.md")
    # Markdown emphasis inside a phrase defeats exact substring matching: the
    # document writes "**not** positive evidence", so a search for "not positive
    # evidence" fails on a document that says exactly that. The emphasis is
    # stripped and each disposition is required to appear as a standalone token.
    raw = adj.read_text() if adj.exists() else ""
    text = raw.replace("**", "").replace("*", "")
    absent = [f"{k} -> {v}" for k, v in REQUIRED_DISPOSITIONS.items()
              if k.lower() not in text.lower()
              or v.lower() not in text.lower()]
    check("6a every disposition survives in the adjudication document",
          not absent and text, f"absent: {absent}")

    # 6b the decisive one: 100% must not be offered as evidence of benefit
    test_src = ((ROOT / "tests/test_experimental_activation.py").read_text()
                .replace("**", "")
                if (ROOT / "tests/test_experimental_activation.py").exists() else "")
    benefit_claims = [
        ln.strip() for ln in test_src.splitlines()
        if "100" in ln and any(t in ln.lower() for t in
                               ("resilien", "benefit", "improve", "better", "gain"))
    ]
    check("6b completion=100% appears in no assertion as a resilience benefit",
          not benefit_claims, f"offending lines: {benefit_claims}")
    check("6c the adjudication states the repaired 100% is not positive evidence",
          "not positive evidence of resilience" in text.lower(),
          "the explicit statement that 100% is not evidence of benefit is missing")
    check("6d the metric-semantics defect is retained as NEW EXPERIMENT REQUIRED",
          "NEW EXPERIMENT REQUIRED" in text.upper(),
          "the open defect was not retained")
    check("6e the manuscript's accurate self-limitations are recorded",
          "overclaiming" in text.lower(),
          "the finding that this manuscript is not overclaiming was dropped")

    print("=" * 78)
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"{passed}/{total} gate checks passed")
    if passed == total:
        print()
        print("CRL is closed. Recorded as a positive result rather than another defective")
        print("package: the mechanism has causal access and the configuration can activate")
        print("it, but the published outcome has insufficient resolution to demonstrate")
        print("the benefit one might want to infer from it. The manuscript already states")
        print("several of these limitations correctly.")
    else:
        failed = [n for n, ok, _ in results if not ok]
        print("FAILED: " + "; ".join(failed))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())