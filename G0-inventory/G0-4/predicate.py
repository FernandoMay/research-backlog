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
A1_NAME = re.compile(
    r"(result|metric|benchmark|eval|experiment|performance|report|ablation|accuracy|figure)",
    re.I,
)
A1_EXT = re.compile(r"\.(json|csv|tsv|md|txt|log|yaml|yml|npy|npz|mat|pkl|tex|pdf)$", re.I)

# --- A2: quantitative claim in the README -------------------------------
METRIC_VOCAB = re.compile(
    r"\b(accuracy|auc|auroc|precision|recall|f1|latency|ms|throughput|error|rmse|mse|mae"
    r"|bleu|rouge|perplexity|baseline|benchmark|score|rate|ratio|loss|reward|iter|itr|wps"
    r"|power|mw|w/|db|snr|psnr|ssim|iou|fid|map)\b",
    re.I,
)
UNIT_VOCAB = re.compile(r"(%|\bms\b|\bmw\b|\bwatt|\bdb\b|\bmbps\b|\bdpi\b|\bhz\b|\bkhz\b|\bgb\b|\bmb\b|\bfps\b)", re.I)
NUMBER = re.compile(r"\d+(?:\.\d+)?")

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
    a1 = [f for f in low if A1_EXT.search(f) and (A1_NAME.search(f) or f.endswith((".tex", ".pdf")))]
    a2 = bool(METRIC_VOCAB.search(readme) and (UNIT_VOCAB.search(readme) or NUMBER.search(readme)))
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
    if not b2:
        missing.append("INPUT_ARTIFACT")
    if not b3:
        missing.append("EXECUTION_INSTRUCTION")

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
        "B2_input_artifact": bool(b2),
        "B3_execution_instruction": bool(b3),
        "missing": missing,
        "files_n": len(files),
        "readme_n": len(readme),
    }


# The observation schema, fixed so a caller cannot smuggle extra evidence in.
SCHEMA_KEYS = {"files", "readme"}