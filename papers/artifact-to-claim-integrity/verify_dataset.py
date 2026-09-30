#!/usr/bin/env python3
"""Mechanical verification of the E1 audit corpus and the paper built on it.

This is a check, not a report generator. Every assertion below is capable of
failing, and several exist because a defect in this corpus was found by hand
first and must never be found by hand again.

Checks
------
A1  Recompute the verdict distribution and the internal-consistency count from
    the thirteen-row table in E1-DATASET-v1.0.md and assert they equal the
    derived-metrics block.
A2  Recompute the gradient block from the same rows and assert it agrees.
A3  Parse the layer labels in E1-AGGREGATE.md's headline table and assert the
    L-number of every row equals the rubric's index for that layer's name.
    This is the assertion that catches the 2026-09-30 label shift. It reads the
    canonical layer names out of the rubric rather than hard-coding them, so it
    fails both on a shifted number and on a renamed layer.
A4  Re-roll every layer count in E1-AGGREGATE.md from the three batch reports'
    own machine-readable layer columns and assert the counts are unchanged.
A5  Assert the two pushed copies under research-backlog-repo/audit/ are
    byte-identical to their local originals, by cmp and by SHA-256.
A6  Audit the seven in-scope files for stale figure strings and shifted layer
    labels, and report every occurrence with context.
A7  Print the final gradient.

Exit status is 0 only when every assertion passes and no stale string is found
outside a recognised correction record.

Usage
-----
    python3 verify_dataset.py
    python3 verify_dataset.py --root /path/to/Documents   # for throwaway trees
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

# --------------------------------------------------------------------------
# Locations
# --------------------------------------------------------------------------

DEFAULT_ROOT = pathlib.Path("/Users/fmf/Documents")

EMDASH = "\u2014"
ENDASH = "\u2013"

RUBRIC_RELPATH = "security/ARTIFACT-TO-CLAIM-RUBRIC.md"
DATASET_RELPATH = "research-audit/E1-DATASET-v1.0.md"
AGGREGATE_RELPATH = "research-audit/E1-AGGREGATE.md"
BATCH1_RELPATH = "research-audit/E1-BATCH-1.md"
BATCH2_RELPATH = "research-audit/batch2/REPORT.md"
BATCH3_RELPATH = "research-audit/batch3/REPORT.md"
PUSH_AGG_RELPATH = "research-backlog-repo/audit/E1-AGGREGATE.md"
PUSH_DAT_RELPATH = "research-backlog-repo/audit/E1-DATASET-v1.0.md"
PUSH_README_RELPATH = "research-backlog-repo/audit/README.md"
TEX_RELPATH = "research-papers/artifact-to-claim-integrity/main.tex"
PAPER_README_RELPATH = "research-papers/artifact-to-claim-integrity/README.md"

# The seven files this change is permitted to touch, in report order.
SEVEN_RELPATHS = [
    AGGREGATE_RELPATH,
    DATASET_RELPATH,
    PUSH_AGG_RELPATH,
    PUSH_DAT_RELPATH,
    PUSH_README_RELPATH,
    TEX_RELPATH,
    PAPER_README_RELPATH,
]

# Out-of-scope files that are scanned for the same defects and reported, never
# edited. These carry the same class of defect and must be visible in the run.
READ_ONLY_EXTRA_RELPATHS = [
    "research-papers/artifact-to-claim-integrity/figures/make_figures.py",
    "research-papers/artifact-to-claim-integrity/figures/data/e1_rows.csv",
]

N_ROWS = 13

# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

FAILURES: list[str] = []
NOTES: list[str] = []


def fail(check: str, message: str) -> None:
    FAILURES.append(f"[{check}] {message}")


def note(message: str) -> None:
    NOTES.append(message)


def section(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(root: pathlib.Path, path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_lines(path: pathlib.Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def cells(line: str) -> list[str]:
    """Split a markdown table row into stripped, non-empty-pipe cells."""
    parts = line.strip()
    if parts.startswith("|"):
        parts = parts[1:]
    if parts.endswith("|"):
        parts = parts[:-1]
    return [c.strip() for c in parts.split("|")]


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|") and len(cells(s)) >= 2


# --------------------------------------------------------------------------
# A0 -- the canonical layer table, read from the rubric
# --------------------------------------------------------------------------

LAYER_HEADING = re.compile(
    r"^#{2,4}\s*L(\d)\s*[" + EMDASH + ENDASH + r"-]+\s*(.+?)\s*$"
)

# Surface forms used across the corpus that name a rubric layer but are not the
# rubric's literal wording. Mapping them keeps the check from being defeated by
# a cosmetic rewording while still failing on a real shift.
LAYER_ALIASES = {
    "artifact exists": "Artifact",
    "reproduction": "Reproduction",
    "numerical claim": "Numerical claim",
    "figure": "Figure",
    "method": "Method",
    "selection": "Selection",
    "internal consistency": "Internal consistency",
    "consistent": "Internal consistency",
    "consistency": "Internal consistency",
    "verdict": "Verdict",
    "verdict: supported": "Verdict",
    "package verdict": "Verdict",
}


def load_rubric_layers(path: pathlib.Path) -> dict[str, int]:
    """Return {canonical layer name: L-number} straight from the rubric."""
    layers: dict[str, int] = {}
    for line in read_lines(path):
        m = LAYER_HEADING.match(line)
        if not m:
            continue
        number, name = int(m.group(1)), m.group(2).strip()
        # Strip any trailing parenthetical gloss the rubric may carry.
        name = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
        key = name.lower()
        if key in LAYER_ALIASES:
            name = LAYER_ALIASES[key]
        if name in layers:
            fail("A0", f"rubric defines {name!r} twice at L{layers[name]} and L{number}")
        layers[name] = number
    if not layers:
        fail("A0", f"no layer headings parsed from {path}")
    return layers


def canonical_layer_name(raw: str) -> str | None:
    """Map a label's trailing name onto a rubric layer name, or None."""
    text = raw.strip().lower()
    text = re.sub(r"[^a-z0-9: ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if text in LAYER_ALIASES:
        return LAYER_ALIASES[text]
    # Longest-suffix match, so "verdict supported" resolves before "verdict".
    for alias in sorted(LAYER_ALIASES, key=len, reverse=True):
        if text == alias or text.endswith(" " + alias):
            return LAYER_ALIASES[alias]
    return None


LABEL_RE = re.compile(
    r"\bL(\d)\s*[" + EMDASH + ENDASH + r"-]+\s*([A-Za-z][A-Za-z ]{2,})"
)
LABEL_SHORT_RE = re.compile(r"\bL(\d)\s+(consistent|consistency)\b", re.I)


# --------------------------------------------------------------------------
# A1/A2 -- recompute the dataset's aggregates from its own rows
# --------------------------------------------------------------------------

ROW_HEADER_TAIL = ["L7 internal", "U4 verdict"]


def parse_dataset_rows(path: pathlib.Path) -> list[dict]:
    rows: list[dict] = []
    header: list[str] | None = None
    for line in read_lines(path):
        if not is_table_row(line):
            continue
        c = cells(line)
        if header is None:
            if c[0] == "#" and c[-2:] == ROW_HEADER_TAIL:
                header = c
            continue
        if re.fullmatch(r"\d+", c[0]) and len(c) == len(header):
            rows.append({
                "n": int(c[0]),
                "package": c[1],
                "total": int(c[2]),
                "correct": int(c[3]),
                "contradicted": int(c[4]),
                "unsupported": int(c[5]),
                "exists": c[6] == "Y",
                "reproduces": c[7] == "Y",
                "u3_broken": c[8] == "Y",
                "u3_absent": c[9] == "Y",
                "internal": c[10],
                "verdict": c[11],
            })
    if not rows:
        fail("A1", f"no thirteen-row table parsed from {path}")
    return rows


DERIVED_LINE = re.compile(
    r"^(\S.*?)\s{2,}(\d+)(?:\s+\(\s*(\d+)\s*/\s*(\d+)\s*\))?"
)
GRADIENT_LINE = re.compile(
    r"^(artifact exists|artifact reproduces|internal consistency|"
    r"package survives whole)\s+(\d+)\s*/\s*(\d+)\s+(\d+)%",
    re.I,
)


def parse_derived_block(path: pathlib.Path) -> dict[str, int]:
    """Label -> value, from the derived-metrics fenced block."""
    out: dict[str, int] = {}
    for line in read_lines(path):
        m = DERIVED_LINE.match(line)
        if m:
            label = re.sub(r"\s+", " ", m.group(1)).strip()
            out[label] = int(m.group(2))
            if m.group(3) is not None and int(m.group(3)) != int(m.group(2)):
                fail("A1", f"derived block {label!r}: count {m.group(2)} does not "
                           f"match its own fraction {m.group(3)}/{m.group(4)}")
    return out


def parse_gradient_block(path: pathlib.Path) -> list[tuple[str, int, int, int]]:
    out: list[tuple[str, int, int, int]] = []
    for line in read_lines(path):
        m = GRADIENT_LINE.match(line)
        if m:
            out.append((m.group(1).lower(), int(m.group(2)), int(m.group(3)),
                        int(m.group(4))))
    return out


# --------------------------------------------------------------------------
# A3 -- the assertion that must catch the label shift
# --------------------------------------------------------------------------

def parse_aggregate_headline(path: pathlib.Path) -> list[dict]:
    """One dict per row of the headline table: stated L-number, label, counts."""
    rows: list[dict] = []
    in_table = False
    for lineno, line in enumerate(read_lines(path), start=1):
        if not is_table_row(line):
            in_table = False
            continue
        c = cells(line)
        if c[0] == "Layer" and c[-1] == "Rate":
            in_table = True
            continue
        if not in_table:
            continue
        m = re.match(r"^L(\d)\s*[" + EMDASH + ENDASH + r"-]+", c[0])
        if m:
            rows.append({"stated": int(m.group(1)), "label": c[0],
                         "supported": c[1], "contradicted": c[2],
                         "rate": c[3], "lineno": lineno})
    if not rows:
        fail("A3", f"headline table not found in {path}")
    return rows


def strip_md(value: str) -> str:
    return re.sub(r"[*`_]", "", value).strip()


def check_aggregate_labels(path: pathlib.Path, rubric: dict[str, int]) -> None:
    """Every stated L-number must equal the rubric's index for that layer name.

    This is the check that would have caught the shift. The rubric is the only
    source of truth for the mapping; nothing here trusts the file under test.
    """
    rows = parse_aggregate_headline(path)
    print(f"  {len(rows)} layer rows parsed from the headline table")

    numbers: list[int] = []
    for row in rows:
        stated, raw, lineno = row["stated"], row["label"], row["lineno"]
        name_part = re.sub(r"^L\d\s*[" + EMDASH + ENDASH + r"-]+\s*", "", raw)
        canonical = canonical_layer_name(name_part)
        if canonical is None:
            fail("A3", f"{path.name}:{lineno}: label {raw!r} names no layer in "
                       f"the rubric; cannot be checked")
            continue
        expected = rubric.get(canonical)
        if expected is None:
            fail("A3", f"{raw!r} resolves to {canonical!r}, which the rubric "
                       f"does not define")
            continue
        numbers.append(stated)
        mark = "ok " if expected == stated else "BAD"
        print(f"  [{mark}] L{stated} {name_part.strip()!r} -> rubric L{expected} "
              f"({canonical})")
        if expected != stated:
            fail("A3", f"{path.name}:{lineno}: label {raw!r} is shifted; the "
                       f"rubric places {canonical} at L{expected}, not L{stated}. "
                       f"This is the 2026-09-30 layer-label shift.")

    if numbers != sorted(numbers):
        fail("A3", f"headline table L-numbers are not ascending: {numbers}")
    if len(set(numbers)) != len(numbers):
        fail("A3", f"headline table repeats an L-number: {numbers}")
    ordered = sorted(n for n in numbers)
    if ordered != numbers:
        fail("A3", f"headline table layers appear out of rubric order: {ordered}")


# --------------------------------------------------------------------------
# A4 -- re-roll the layer counts from the primary batch records
# --------------------------------------------------------------------------

BATCH_HEADER_TAIL = ["L4", "L5", "L6", "L7", "L8"]

# The batch reports carry four L3 columns (total/supported/contradicted/
# unsupported), so a bare "L3" verdict column does not exist and is not tallied
# here. The aggregate's headline table reports no L3 row for the same reason:
# the per-claim L3 rate is not aggregable across batches.
TALLIED_LAYERS = ["L1", "L2", "L4", "L5", "L6", "L7", "L8"]


def is_separator(line: str) -> bool:
    """True for a markdown table alignment row such as |---|---|.

    The interior pipes must be removed, not just the leading and trailing ones,
    or every separator row is mistaken for a data row.
    """
    s = line.strip().replace("|", "")
    return bool(s) and set(s) <= set("-: ")


def parse_batch_layers(path: pathlib.Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in read_lines(path):
        if not is_table_row(line) or is_separator(line):
            continue
        c = cells(line)
        if header is None:
            if c[0] == "package" and c[1] == "repo" and c[-5:] == BATCH_HEADER_TAIL:
                header = c
            continue
        if len(c) == len(header) and re.match(r"^\S", c[0]):
            rec = {header[i]: c[i] for i in range(len(header))}
            rec["_file"] = str(path)
            rows.append(rec)
    return rows


def re_roll_layers(paths: list[pathlib.Path]) -> tuple[dict[str, int], dict[str, int]]:
    """{layer: supported count}, {layer: row count} from the batch reports."""
    supported: dict[str, int] = {layer: 0 for layer in TALLIED_LAYERS}
    total: dict[str, int] = {layer: 0 for layer in TALLIED_LAYERS}
    seen: set[str] = set()
    for path in paths:
        for rec in parse_batch_layers(path):
            key = rec["package"]
            if key in seen:
                fail("A4", f"row {key!r} appears in more than one batch report")
            seen.add(key)
            for layer in TALLIED_LAYERS:
                total[layer] += 1
                if rec[layer] == "SUPPORTED":
                    supported[layer] += 1
    return supported, total


def parse_aggregate_counts(path: pathlib.Path) -> dict[int, int]:
    """{L-number: SUPPORTED count} from the aggregate headline table."""
    out: dict[int, int] = {}
    for row in parse_aggregate_headline(path):
        value = strip_md(row["supported"])
        if value.isdigit():
            out[row["stated"]] = int(value)
        else:
            fail("A4", f"{path.name}:{row['lineno']}: SUPPORTED cell {row['supported']!r} "
                       f"is not a bare integer")
    return out


# --------------------------------------------------------------------------
# A5 -- pushed copies
# --------------------------------------------------------------------------

def compare_copies(local: pathlib.Path, pushed: pathlib.Path, label: str) -> None:
    for path in (local, pushed):
        if not path.exists():
            fail("A5", f"{label}: {rel(DEFAULT_ROOT, path)} does not exist")
            return
    lb, pb = local.read_bytes(), pushed.read_bytes()
    lsha, psha = hashlib.sha256(lb).hexdigest(), hashlib.sha256(pb).hexdigest()

    proc = subprocess.run(["cmp", str(local), str(pushed)],
                          capture_output=True, text=True)
    cmp_ok = proc.returncode == 0
    sha_ok = lsha == psha

    print(f"  {label}")
    print(f"    cmp      : {'identical' if cmp_ok else 'DIFFER -> ' + proc.stdout.strip()}")
    print(f"    local    : {lsha}  {rel(DEFAULT_ROOT, local)}")
    print(f"    pushed   : {psha}  {rel(DEFAULT_ROOT, pushed)}")
    print(f"    sha-256  : {'match' if sha_ok else 'MISMATCH'}")

    if not cmp_ok:
        fail("A5", f"{label}: cmp reports the pushed copy differs from the local original")
    if not sha_ok:
        fail("A5", f"{label}: SHA-256 differs between local and pushed copies")


# --------------------------------------------------------------------------
# A6 -- stale-string and stale-label audit
# --------------------------------------------------------------------------

STALE_FIGURES = [
    (r"\b2\s*/\s*13\b", "internal consistency 2/13 (pre-correction)"),
    (r"\b2 of 13\b", "internal consistency 2 of 13 (pre-correction)"),
    (r"\b13\s*,\s*10\s*,\s*2\s*,\s*0\b", "gradient tuple (13, 10, 2, 0)"),
    (r"\b10/13 -> 2/13\b", "gradient step 2/13"),
    # Guarded against LaTeX column widths such as p{0.315\columnwidth} and
    # against version-like or hash-like digit runs.
    (r"(?<![\d.])315(?![\d.])", "pre-correction claim total 315"),
    (r"(?<![\d.])94(?![\d.])", "pre-correction contradicted count 94"),
    (r"(?<![\d.])83\s*%", "pre-correction correct rate 83%"),
    (r"0\s*/\s*7\s*/\s*6", "pre-correction verdict roll-up 0/7/6"),
    (r"[Dd]elta\s*2\b", "the superseded 'Delta 2' framing"),
]

# A line inside one of these is quoting a caught error as history. That is
# required by the dataset's own instruction to record corrections, so it is not
# a stale value.
CORRECTION_CONTEXT = re.compile(
    r"correction|corrected|correct |miscount|supersed|pre-freeze|post-freeze|"
    r"post-publication|delta|recorded as|block recorded|block stated|"
    r"block gave|recorded \d|shift|wrong summary|wrong verdict|wrong internal|"
    r"before this correction|was wrong",
    re.I,
)
CONTEXT_WINDOW = 4


def in_code_span(line: str, start: int, end: int) -> bool:
    """True when line[start:end] sits inside backticks or a \\texttt{...}.

    A layer label written in code formatting is a quotation of a label, either
    the pre-correction one inside a correction record or the current one being
    cited. A live table row or heading is never code-formatted, so this rule
    classifies quotations without weakening the check on live labels.

    Quotation marks and whitespace between the label and the delimiting
    backtick are tolerated, because `` `"L6 consistent"` `` puts the closing
    backtick after the closing quote.
    """
    before, after = line[:start], line[end:]
    if before.count("`") % 2 == 1 and after.lstrip(" \t\"'").startswith("`"):
        return True
    return before.rstrip().endswith("\\texttt{") and after.lstrip().startswith("}")


def audit_stale_figures(root: pathlib.Path, relpaths: list[str]) -> int:
    flagged = 0
    print()
    print("  stale figure strings (matches are shown with context; occurrences "
          "inside a correction record are expected)")
    for relpath in relpaths:
        path = root / relpath
        if not path.exists():
            fail("A6", f"{relpath} does not exist")
            continue
        lines = read_lines(path)
        for pattern, why in STALE_FIGURES:
            rx = re.compile(pattern)
            for i, line in enumerate(lines):
                if not rx.search(line):
                    continue
                lo, hi = max(0, i - CONTEXT_WINDOW), min(len(lines), i + CONTEXT_WINDOW + 1)
                window = lines[lo:hi]
                historical = any(CORRECTION_CONTEXT.search(w) for w in window)
                tag = "HISTORICAL" if historical else "STALE"
                if not historical:
                    flagged += 1
                    fail("A6", f"{relpath}:{i + 1}: {why} -> {line.strip()!r}")
                print(f"    [{tag}] {relpath}:{i + 1}: {why}")
                print(f"             {line.strip()[:96]}")
    return flagged


def audit_stale_labels(root: pathlib.Path, relpaths: list[str],
                       rubric: dict[str, int]) -> tuple[int, int]:
    """Flag any L-label whose number disagrees with the rubric's index.

    An occurrence inside a correction record is history, not a live defect: the
    dataset requires its caught errors to be quoted as history. Such occurrences
    are printed and classified HISTORICAL, and do not fail the run.
    """
    in_scope_bad = 0
    read_only_bad = 0
    print()
    print("  layer labels across the corpus (L-number vs the rubric's index)")
    for relpath in relpaths:
        path = root / relpath
        if not path.exists():
            continue
        lines = read_lines(path)
        for i, line in enumerate(lines, start=1):
            hits: list[tuple[int, str, str, int, int]] = []
            for m in LABEL_RE.finditer(line):
                hits.append((int(m.group(1)), m.group(2).strip(), m.group(0),
                             m.start(), m.end()))
            for m in LABEL_SHORT_RE.finditer(line):
                hits.append((int(m.group(1)), m.group(2), m.group(0),
                             m.start(), m.end()))
            for stated, name, raw, ms, me in hits:
                canonical = canonical_layer_name(name)
                if canonical is None or canonical not in rubric:
                    continue
                expected = rubric[canonical]
                if expected == stated:
                    continue
                lo = max(0, i - 1 - CONTEXT_WINDOW)
                hi = min(len(lines), i + CONTEXT_WINDOW)
                historical = (in_code_span(line, ms, me) or
                              any(CORRECTION_CONTEXT.search(w) for w in lines[lo:hi]))
                in_scope = relpath in SEVEN_RELPATHS
                if historical:
                    tag = "HISTORICAL"
                elif in_scope:
                    tag = "STALE"
                    in_scope_bad += 1
                else:
                    tag = "STALE, READ-ONLY"
                    read_only_bad += 1
                print(f"    [{tag}] {relpath}:{i}: {raw!r} names {canonical}, "
                      f"which the rubric places at L{expected}")
                print(f"             {line.strip()[:96]}")
                if not historical and in_scope:
                    fail("A6", f"{relpath}:{i}: shifted layer label {raw!r} "
                               f"({canonical} is L{expected} in the rubric)")
    return in_scope_bad, read_only_bad


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT,
                    help="Documents root (default: %s)" % DEFAULT_ROOT)
    args = ap.parse_args()
    root: pathlib.Path = args.root.resolve()

    print("E1 dataset verification")
    print("root: %s" % root)

    # ---- A0 -------------------------------------------------------------
    section("A0  canonical layer table, read from the rubric")
    rubric = load_rubric_layers(root / RUBRIC_RELPATH)
    for name in sorted(rubric, key=lambda n: rubric[n]):
        print(f"  L{rubric[name]} {name}")
    if len(rubric) != 8:
        fail("A0", f"expected 8 rubric layers, parsed {len(rubric)}")

    # ---- A1 -------------------------------------------------------------
    section("A1  recompute dataset aggregates from the thirteen rows")
    dataset = root / DATASET_RELPATH
    rows = parse_dataset_rows(dataset)
    derived = parse_derived_block(dataset)

    if len(rows) != N_ROWS:
        fail("A1", f"row table has {len(rows)} rows, expected {N_ROWS}")
    if [r["n"] for r in rows] != list(range(1, N_ROWS + 1)):
        fail("A1", f"row indices are not 1..{N_ROWS}: "
                   f"{[r['n'] for r in rows]}")

    for r in rows:
        split = r["correct"] + r["contradicted"] + r["unsupported"]
        if split != r["total"]:
            fail("A1", f"row {r['n']} ({r['package']}) does not sum: "
                       f"{r['correct']}+{r['contradicted']}+{r['unsupported']} "
                       f"= {split} != {r['total']}")

    verdicts = {"SUPPORTED": 0, "PARTIALLY": 0, "CONTRADICTED": 0}
    for r in rows:
        if r["verdict"] not in verdicts:
            fail("A1", f"row {r['n']} carries unrecognised verdict "
                       f"{r['verdict']!r}")
            continue
        verdicts[r["verdict"]] += 1
    internal = sum(1 for r in rows if r["internal"] == "SUPPORTED")
    exists = sum(1 for r in rows if r["exists"])
    reproduces = sum(1 for r in rows if r["reproduces"])
    u3_absent = sum(1 for r in rows if r["u3_absent"])
    total_claims = sum(r["total"] for r in rows)
    correct_claims = sum(r["correct"] for r in rows)
    contra_claims = sum(r["contradicted"] for r in rows)
    unsup_claims = sum(r["unsupported"] for r in rows)

    expect_derived = {
        "U1 claims adjudicated": total_claims,
        "U1 CLAIM-CORRECT": correct_claims,
        "U1 CLAIM-CONTRADICTED": contra_claims,
        "U1 CLAIM-UNSUPPORTED": unsup_claims,
        "U2 artifact exists": exists,
        "U2 artifact reproduces": reproduces,
        "U3 relation absent": u3_absent,
        "L7 internal consistency": internal,
        "U4 package verdict SUPPORTED": verdicts["SUPPORTED"],
        "U4 package verdict PARTIALLY SUPPORTED": verdicts["PARTIALLY"],
        "U4 package verdict CONTRADICTED": verdicts["CONTRADICTED"],
    }

    print(f"  rows parsed: {len(rows)}")
    print(f"  recomputed  : verdicts {verdicts['SUPPORTED']} / "
          f"{verdicts['PARTIALLY']} / {verdicts['CONTRADICTED']}, "
          f"internal consistency {internal} of {len(rows)}")
    print(f"  derived block:")
    for label, computed in expect_derived.items():
        recorded = derived.get(label)
        if recorded is None:
            fail("A1", f"derived-metrics block has no line for {label!r}")
            print(f"    MISSING  {label}")
            continue
        mark = "ok " if recorded == computed else "BAD"
        if recorded != computed:
            fail("A1", f"{label}: derived block records {recorded}, rows give "
                       f"{computed}")
        print(f"    [{mark}] {label}: block {recorded}, rows {computed}")

    # ---- A2 -------------------------------------------------------------
    section("A2  gradient block against the recomputed rows")
    gradient = parse_gradient_block(dataset)
    expect_gradient = [
        ("artifact exists", exists),
        ("artifact reproduces", reproduces),
        ("internal consistency", internal),
        ("package survives whole", verdicts["SUPPORTED"]),
    ]
    if len(gradient) != len(expect_gradient):
        fail("A2", f"gradient block has {len(gradient)} lines, expected "
                   f"{len(expect_gradient)}")
    for (label, computed), (g_label, num, den, pct) in zip(expect_gradient, gradient):
        if g_label != label:
            fail("A2", f"gradient line {g_label!r} is out of order, expected {label!r}")
        if num != computed:
            fail("A2", f"gradient {label}: block records {num}, rows give {computed}")
        if den != len(rows):
            fail("A2", f"gradient {label}: denominator {den} != {len(rows)}")
        want_pct = round(100.0 * num / den)
        if abs(pct - want_pct) >= 1:
            fail("A2", f"gradient {label}: {num}/{den} recorded as {pct}%, "
                       f"which is {want_pct}%")
        print(f"  {'ok ' if num == computed else 'BAD'} {label}: "
              f"{num}/{den} ({pct}%), rows give {computed}")

    # ---- A3 -------------------------------------------------------------
    section("A3  aggregate headline labels against the rubric")
    aggregate = root / AGGREGATE_RELPATH
    check_aggregate_labels(aggregate, rubric)

    # ---- A4 -------------------------------------------------------------
    section("A4  aggregate counts re-rolled from the three batch reports")
    batch_paths = [root / BATCH1_RELPATH, root / BATCH2_RELPATH,
                   root / BATCH3_RELPATH]
    batch_rows = {rel(root, p): parse_batch_layers(p) for p in batch_paths}
    n_batch_rows = sum(len(v) for v in batch_rows.values())
    print(f"  batch reports supply {n_batch_rows} rows: " +
          ", ".join(f"{name}={len(v)}" for name, v in batch_rows.items()))
    if n_batch_rows != N_ROWS:
        fail("A4", f"the three batch reports jointly supply {n_batch_rows} rows, "
                   f"expected {N_ROWS}")
    supported, total_rows = re_roll_layers(batch_paths)
    headline = {r["stated"]: r for r in parse_aggregate_headline(aggregate)}
    counts = parse_aggregate_counts(aggregate)

    print(f"  {'layer':<34} {'batches':>8} {'aggregate':>10}  status")
    for stated in sorted(counts):
        raw = headline[stated]["label"]
        name_part = re.sub(r"^L\d\s*[" + EMDASH + ENDASH + r"-]+\s*", "", raw)
        name = canonical_layer_name(name_part) or "?"
        key = f"L{stated}"
        from_batches = supported.get(key)
        agg = counts[stated]
        ok = from_batches == agg
        if not ok:
            fail("A4", f"{key} ({name}): batch reports give {from_batches} "
                       f"SUPPORTED for {name}, aggregate records {agg} under that "
                       f"label. The counts disagree.")
        shown = "?" if from_batches is None else str(from_batches)
        print(f"  {key + ' ' + name:<34} {shown:>8} {agg:>10}  "
              f"{'ok' if ok else 'MISMATCH'}")

    # ---- A5 -------------------------------------------------------------
    section("A5  pushed copies byte-identical to local originals")
    compare_copies(dataset, root / PUSH_DAT_RELPATH, "E1-DATASET-v1.0.md")
    compare_copies(aggregate, root / PUSH_AGG_RELPATH, "E1-AGGREGATE.md")

    # ---- A6 -------------------------------------------------------------
    section("A6  stale-string and stale-label audit")
    scan = SEVEN_RELPATHS + READ_ONLY_EXTRA_RELPATHS
    in_scope_bad, read_only_bad = audit_stale_labels(root, scan, rubric)
    audit_stale_figures(root, scan)
    if read_only_bad:
        print()
        print(f"  {read_only_bad} shifted layer label(s) remain in files outside the")
        print("  seven this change may edit. They are reported, not fixed here:")
        print("  see the report for the paths and the reason they are out of scope.")

    # ---- A7 -------------------------------------------------------------
    section("A7  final gradient")
    print(f"  artifact exists                {exists}/{len(rows)}   "
          f"{round(100 * exists / len(rows))}%")
    print(f"  artifact reproduces            {reproduces}/{len(rows)}   "
          f"{round(100 * reproduces / len(rows))}%")
    print(f"  internal consistency           {internal}/{len(rows)}   "
          f"{round(100 * internal / len(rows))}%")
    print(f"  package survives whole         {verdicts['SUPPORTED']}/{len(rows)}   "
          f"{round(100 * verdicts['SUPPORTED'] / len(rows))}%")
    print()
    print(f"  verdict distribution           "
          f"{verdicts['SUPPORTED']} SUPPORTED / {verdicts['PARTIALLY']} "
          f"PARTIALLY / {verdicts['CONTRADICTED']} CONTRADICTED")
    print(f"  claim pool                     {correct_claims}/{total_claims} "
          f"correct ({round(100 * correct_claims / total_claims, 1)}%), "
          f"{contra_claims} contradicted, {unsup_claims} unsupported")

    # ---- result ---------------------------------------------------------
    section("RESULT")
    for n in NOTES:
        print(f"  note: {n}")
    if FAILURES:
        print(f"  {len(FAILURES)} FAILURE(S):")
        for f in FAILURES:
            print(f"    {f}")
        return 1
    print("  all assertions passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
