#!/usr/bin/env python3
"""
G0-4 reproduction-selection predicate.

Implements REPRODUCE-SELECTION.md exactly. The vocabularies below are
copied from that document and are the ONLY terms used. Adding a term
without amending the specification would make the two disagree, which is
the L4 defect class recorded in that file.

Read-only. Takes an observation record, returns a classification.

Design note: every predicate here is a NEGATIVE-capable check over
observable structure. That is deliberate. It is also the weakness: see L1
in the specification. A structural check cannot prove that a published
claim does not exist, only that no evidence of one was found at the
inspected depth.
"""

import re

# --- A1: claim-bearing tree paths ---------------------------------------
# REWRITTEN after ground-truth validation. The first rule treated any .tex
# or .pdf anywhere as claim-bearing, which matched UI assets
# (assets/images/doc.pdf), an uploaded PDF belonging to a DIFFERENT project
# (upload/fg supply.pdf inside an unrelated scaffold), and a GitHub issue
# template (.github/issue_template/bug_report.md).
#
# Two changes: vendored/template/asset locations are excluded outright, and a
# manuscript must sit at a paper-like path rather than anywhere.

A1_NAME = re.compile(
    r"(result|metric|benchmark|eval|experiment|performance|report|ablation|accuracy|figure)",
    re.I,
)
A1_EXT = re.compile(r"\.(json|csv|tsv|md|txt|log|yaml|yml|npy|npz|mat|pkl|tex|pdf)$", re.I)

# Locations that never contain the repository's own claims.
# Matched as PATH COMPONENTS, not as a string prefix. The prefix form only
# excluded vendor directories at the top level and let nested ones through:
# newslttr matched inside bakendo/env/lib/python3.10/site-packages/, and
# socketlab matched inside javascript_implementation/node_modules/.
A1_EXCLUDE_COMPONENT = {
    ".github", "node_modules", ".venv", "venv", "env", "virtualenv",
    "site-packages", "vendor", "third_party", "assets", "static", "public",
    "upload", "uploads", "ios", "android", ".dart_tool", "build", "dist",
    "migrations", "__macosx", ".git", "__pycache__", "dist-info", "eggs",
}
# A manuscript must be at a paper-like path.
A1_PAPER = re.compile(
    r"(^|/)(paper|papers|latex|manuscript|manuscripts)/|(^|/)main\.(tex|pdf)$|"
    r"(paper|manuscript|article)\.(tex|pdf|md)$",
    re.I,
)


def a1_excluded(low):
    return any(part in A1_EXCLUDE_COMPONENT for part in low.split("/")[:-1])


def a1_claim(files):
    hits = []
    for f in files:
        low = f.lower()
        if a1_excluded(low):
            continue
        if A1_EXT.search(low) and A1_NAME.search(low):
            hits.append(f)
        elif low.endswith((".tex", ".pdf")) and A1_PAPER.search(low):
            hits.append(f)
    return hits

# --- A2: quantitative claim in the README -------------------------------
# REWRITTEN after ground-truth validation. The first vocabulary produced
# mass false positives on web and mobile repositories: it matched the
# navigation screen "Map" (intended for mAP), the Dart colour constant
# "AppColors.error", and the CSS property "Aspect Ratio". A bare \d+ also
# matched hex colours and version numbers.
#
# Two changes: the vocabulary is restricted to terms that are unambiguous in
# a README, and a metric term only counts when a number appears WITHIN
# A2_WINDOW characters of it. A metric published in prose puts the number
# next to the name; a UI string does not.
#
# mAP is matched case-sensitively on purpose. See A2_CASE_SENSITIVE.

A2_METRIC_LOWER = re.compile(
    r"\b(accuracy|precision|recall|auroc|auc-?roc|rmse|mse|mae|brier|ece"
    r"|bleu|rouge|perplexity|latency|throughput|snr|psnr|ssim|iou|fid"
    r"|wer|cer|word error rate|bit error rate|ber|itr|words per minute|wpm)\b",
    re.I,
)
# Ambiguous in a README, therefore matched case-sensitively only.
A2_METRIC_CASE = re.compile(r"\bmAP\b|\bF1[- ]score\b|\bF1\b|\bPSNR\b|\bSSIM\b|\bBLEU\b|\bIoU\b")
# Result-like unit must also be adjacent. A bare number is not a result.
A2_UNIT = re.compile(r"(%|\bms\b|\bmilliseconds?\b|\bdB\b|\bSNR\b|\bMW\b|\bmW\b|\bwatt"
                     r"|\bdpi\b|\bHz\b|\bMHz\b|\bGB/s\b|\bMbps\b|\bfps\b|\btokens?/s\b)", re.I)
A2_WINDOW = 40


def a2_claim(readme):
    """True only if a metric term sits next to a number (and ideally a unit)."""
    for m in list(A2_METRIC_LOWER.finditer(readme)) + list(A2_METRIC_CASE.finditer(readme)):
        lo, hi = m.start(), m.end()
        window = readme[max(0, lo - A2_WINDOW): hi + A2_WINDOW]
        if not re.search(r"\d+(?:\.\d+)?", window):
            continue          # a metric named but never quantified
        if not A2_UNIT.search(window):
            continue          # quantified, but no result-like unit nearby
        return True
    return False

# --- B1: execution chain -------------------------------------------------
B1_MANIFEST = (
    "requirements.txt", "requirements-dev.txt", "requirements_dev.txt", "pyproject.toml",
    "setup.py", "environment.yml", "environment.yaml", "package.json", "cargo.toml",
    "go.mod", "pom.xml", "build.gradle", "makefile", "cmakelists.txt", "dockerfile",
    "gemfile", "build.sbt",
)

# --- B2: input artifact --------------------------------------------------
B2_DIR = ("data/", "dataset/", "datasets/")
B2_EXT = (".csv", ".tsv", ".npy", ".npz", ".mat", ".pkl", ".h5", ".hdf5", ".parquet", ".arrow", ".jsonl")
B2_SCRIPT = re.compile(r"^(download|fetch|get_data|obtain|prepare_data)[^/]*\.(py|sh)$", re.I)

# --- B3: execution instruction ------------------------------------------
B3_SECTION = re.compile(
    r"^#{1,4}\s*(installation|install|usage|quick\s*start|getting\s*started|running|how\s*to\s*(run|use)|setup|build|reproduce|usage\s*examples?)\b",
    re.I | re.M,
)
# Dedicated instruction documents. Added after validation misclassified 2 of 3
# known-good repositories: all three carry REPRODUCE.md and the predicate had
# no term for it. Third INCOMPLETE-MARKER-VOCABULARY occurrence in this audit.
B3_INSTRUCTION_DOC = (
    "reproduce.md", "reproduce.txt", "run.md", "usage.md", "instructions.md",
    "howto.md", "how_to.md", "quickstart.md", "quick_start.md",
    "getting_started.md", "getting-started.md",
)
B3_ENTRYPOINT = ("main.py", "run.py", "train.py", "evaluate.py", "experiment.py")


def classify(rec):
    """rec: {files: [...], readme: str|None}. Returns a verdict dict."""
    files = rec.get("files") or []
    readme = rec.get("readme") or ""
    low = [f.lower() for f in files]
    bases = {f.rsplit("/", 1)[-1] for f in low}

    # ---- Condition A: does a published claim exist? ----
    a1 = a1_claim(files)
    a2 = a2_claim(readme)
    a_evidence = []
    if a1:
        a_evidence.append(f"A1:{len(a1)} claim-bearing path(s)")
    if a2:
        a_evidence.append("A2:quantitative claim in README")
    a = bool(a1 or a2)

    # ---- Condition B: is regeneration checkable? ----
    b1 = [m for m in B1_MANIFEST if m in bases]
    b2 = (
        [d for d in B2_DIR if any(f.startswith(d) for f in low)]
        or [f for f in low if f.endswith(B2_EXT)]
        or [f for f in low if B2_SCRIPT.match(f)]
    )
    b3_doc = [d for d in B3_INSTRUCTION_DOC if d in bases]
    b3_entry = [
        b for b in B3_ENTRYPOINT
        if b in bases or any(f.endswith("/" + b) for f in low)
    ]
    b3 = bool(B3_SECTION.search(readme)) or bool(b3_doc) or bool(b3_entry)

    missing = []
    if not b1:
        missing.append("EXECUTION_CHAIN")
    if not b3:
        missing.append("EXECUTION_INSTRUCTION")

    # B2 is a FLAG, not a blocker. Ground-truth validation found the blocker
    # form wrong: absence of a data file does not establish that external data
    # is required. Whether a missing dataset blocks execution is an execution
    # question, answerable only by attempting and classifying the failure.
    flags = []
    if a and not b2:
        flags.append("INPUT_ARTIFACT_ABSENT")

    if not a:
        state = "NO_PUBLISHED_CLAIM"
    elif not missing:
        state = "REPRODUCE_ELIGIBLE"
    else:
        state = "REPRODUCE_NOT_YET_ELIGIBLE"

    return {
        "state": state,
        "A": a, "A_evidence": a_evidence,
        "B1_execution_chain": bool(b1),
        "B2_input_artifact_present": bool(b2),
        "B3_execution_instruction": bool(b3),
        "missing": missing,
        "flags": flags,
        "files_n": len(files),
        "readme_n": len(readme),
    }


# The observation schema, fixed so a caller cannot smuggle extra evidence in.
SCHEMA_KEYS = {"files", "readme"}