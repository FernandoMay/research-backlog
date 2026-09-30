#!/usr/bin/env python3
"""Mechanical verification of the E1 audit corpus and the paper built on it.

This is a check, not a report generator. Every assertion below is capable of
failing, and several exist because a defect in this corpus was found by hand
first and must never be found by hand again.

Checks
------
A0  Read the canonical L1-L8 layer table out of the rubric. Every other layer
    assertion is relative to this, so it is the source of truth and the reason
    a missing rubric is a hard failure rather than a skipped check.
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
    byte-identical to their local originals, by cmp and by SHA-256. Skipped,
    loudly, in a public clone that has no pushed tree.
A6  Audit the in-scope files for stale figure strings and shifted layer labels.
    The stale patterns are PARSED OUT OF THE DATASET'S CORRECTION LOG, not
    transcribed into this file. See "What this can and cannot detect".
A7  Print the final gradient.
A8  Join the frozen row table to the three batch reports on the repository name
    and diff every U1/U2/L7/U4 cell against the primary records. This is the
    check that does not exist anywhere else in the pipeline: the row table's
    own author never ran it.
A9  Re-derive the cross-batch claim-pool split from the row table and compare
    it against the dataset's cross-batch block, per span and per report. This is
    the check that would have caught the 2026-09-30 rate/span mispairing.

Exit status is 0 only when every assertion passes and no stale string is found
outside a recognised correction record.

What this can and cannot detect
-------------------------------
Stated at the top rather than in a limitations section, because an integrity
instrument that overstates its coverage is the failure class this study is
about, and this file is inside the study.

CAN
  * Detect any disagreement between the frozen row table and the three batch
    reports' own per-row L3/L7/L8 columns (A8). The batch reports are primary
    evidence and are never transcribed by this author, so this comparison has
    two independent origins.
  * Detect a rate paired with the wrong row span (A9). The defect this check
    exists for was invisible to the earlier instrument set: reconciliation
    compares sums against sums and a mispaired rate is not a wrong sum.
  * Detect any pre-correction figure anywhere in the corpus that the dataset's
    correction log records as corrected (A6). The list of such figures is
    derived from the log at run time, so logging a new correction automatically
    arms a new guard instead of requiring this file to be edited.
  * Detect a layer label whose L-number disagrees with the rubric (A0, A3, A6).

CANNOT
  * Detect a defect nobody has written down anywhere. This was the central
    criticism of the earlier revision of A6, which was a literal blocklist of
    known-bad strings: an instrument that only finds defects someone already
    wrote down is not an instrument. A6 is now derived, which widens it to
    every correction the log records, but the residual limitation is the same
    one and is stated here rather than papered over.
  * Cover figures/make_figures.py's figure output, or any PDF. It checks the
    manuscript's numbers, not the rendered figure's geometry.
  * Substitute for an independent re-derivation. Every check in this file was
    written by the same author as the corpus it checks. The defects this file
    could not find in itself were found by an outside auditor who wrote their
    own derivation code and imported no module of ours.

Usage
-----
    python3 verify_dataset.py
    python3 verify_dataset.py --root /path/to/corpus/tree   # throwaway trees

The corpus root is discovered from this script's own location, so no absolute
path is baked in and the script runs from any checkout at any depth, in either
the author's tree (``research-audit/`` + ``security/``) or a public clone
(``audit/``). Pass --root only to point at a throwaway copy of the tree.
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

HERE = pathlib.Path(__file__).resolve().parent

EMDASH = "\u2014"
ENDASH = "\u2013"

# Two layouts. The author's working tree keeps the rubric under security/ and
# the audit corpus under research-audit/; the public repository flattens the
# audit corpus to audit/ and versions the rubric file. An earlier revision
# hard-coded the author's paths, so this script exited 1 in a fresh clone and
# the typeset table had no covering instrument at all for a third party.
RUBRIC_RELPATHS = (
    "security/ARTIFACT-TO-CLAIM-RUBRIC.md",
    "audit/ARTIFACT-TO-CLAIM-RUBRIC-v1.0.md",
)
DATASET_RELPATHS = (
    "research-audit/E1-DATASET-v1.0.md",
    "audit/E1-DATASET-v1.0.md",
)
AGGREGATE_RELPATHS = (
    "research-audit/E1-AGGREGATE.md",
    "audit/E1-AGGREGATE.md",
)
BATCH1_RELPATHS = ("research-audit/E1-BATCH-1.md", "audit/E1-BATCH-1.md")
BATCH2_RELPATHS = ("research-audit/batch2/REPORT.md", "audit/batch2/REPORT.md")
BATCH3_RELPATHS = ("research-audit/batch3/REPORT.md", "audit/batch3/REPORT.md")
PUSH_ROOT_RELPATHS = ("research-backlog-repo",)
PAPER_RELPATHS = (
    "research-papers/artifact-to-claim-integrity",
    "papers/artifact-to-claim-integrity",
)

# Populated by resolve_layout(); kept as module-level names so the reporting
# helpers and the checks can refer to a single resolved layout.
LAYOUT: dict[str, str] = {}


def resolve_layout(root: pathlib.Path) -> dict[str, str]:
    """Choose the first candidate path that exists for each file."""
    def pick(candidates: tuple[str, ...], what: str) -> str:
        for relpath in candidates:
            if (root / relpath).is_file():
                return relpath
        raise SystemExit(
            f"verify_dataset.py: cannot locate the {what}.\n"
            f"Looked under {root} for any of:\n"
            + "\n".join(f"  {c}" for c in candidates)
        )

    layout = {
        "rubric": pick(RUBRIC_RELPATHS, "rubric"),
        "dataset": pick(DATASET_RELPATHS, "frozen dataset"),
        "aggregate": pick(AGGREGATE_RELPATHS, "aggregate report"),
        "batch1": pick(BATCH1_RELPATHS, "batch 1 report"),
        "batch2": pick(BATCH2_RELPATHS, "batch 2 report"),
        "batch3": pick(BATCH3_RELPATHS, "batch 3 report"),
        "paper": pick(tuple(f"{p}/main.tex" for p in PAPER_RELPATHS),
                      "manuscript"),
    }
    paper_dir = layout["paper"].rsplit("/", 1)[0]
    layout["paper_dir"] = paper_dir
    layout["paper_readme"] = f"{paper_dir}/README.md"
    layout["make_figures"] = f"{paper_dir}/figures/make_figures.py"
    layout["rows_csv"] = f"{paper_dir}/figures/data/e1_rows.csv"
    layout["classes_csv"] = f"{paper_dir}/figures/data/failure_classes.csv"
    return layout


def discover_root() -> pathlib.Path:
    """Locate the corpus root by walking up from this script.

    This script ships inside the tree it verifies, so its own position is the
    only anchor it needs. Nothing here depends on the tree being called
    ``Documents`` or on living at any particular depth. Both the author's layout
    and a public clone are accepted; the marker for each is the frozen dataset
    plus a rubric.
    """
    for parent in HERE.parents:
        has_dataset = any((parent / p).is_file() for p in DATASET_RELPATHS)
        has_rubric = any((parent / p).is_file() for p in RUBRIC_RELPATHS)
        if has_dataset and has_rubric:
            return parent
    searched = "\n  ".join(str(p) for p in HERE.parents) or str(HERE)
    raise SystemExit(
        "verify_dataset.py: cannot locate the corpus root.\n"
        f"Looked for the frozen dataset ({DATASET_RELPATHS[0]} or "
        f"{DATASET_RELPATHS[1]}) together with a rubric, in:\n  {searched}\n"
        "Run this script from a checkout that contains the audit corpus, or "
        "pass --root /path/to/corpus/tree."
    )


DEFAULT_ROOT = discover_root()

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

def compare_copies(local: pathlib.Path, pushed: pathlib.Path, label: str,
                   root: pathlib.Path) -> None:
    for path in (local, pushed):
        if not path.exists():
            fail("A5", f"{label}: {rel(root, path)} does not exist")
            return
    lb, pb = local.read_bytes(), pushed.read_bytes()
    lsha, psha = hashlib.sha256(lb).hexdigest(), hashlib.sha256(pb).hexdigest()

    proc = subprocess.run(["cmp", str(local), str(pushed)],
                          capture_output=True, text=True)
    cmp_ok = proc.returncode == 0
    sha_ok = lsha == psha

    print(f"  {label}")
    print(f"    cmp      : {'identical' if cmp_ok else 'DIFFER -> ' + proc.stdout.strip()}")
    print(f"    local    : {lsha}  {rel(root, local)}")
    print(f"    pushed   : {psha}  {rel(root, pushed)}")
    print(f"    sha-256  : {'match' if sha_ok else 'MISMATCH'}")

    if not cmp_ok:
        fail("A5", f"{label}: cmp reports the pushed copy differs from the local original")
    if not sha_ok:
        fail("A5", f"{label}: SHA-256 differs between local and pushed copies")


# --------------------------------------------------------------------------
# A6 -- stale-string and stale-label audit
# --------------------------------------------------------------------------

# The earlier revision of this check held a literal list of the pre-correction
# figures the author already knew about. That is a blocklist: it re-finds the
# defects that were written down and cannot find any other, which is the only
# kind that matters. The 2026-09-30 rate/span mispairing was invisible to it,
# because `34.6` appeared nowhere in this file.
#
# The patterns are now DERIVED from the dataset's own correction log at run
# time. Two kinds are emitted per logged correction:
#
#   * the log's own sentence, whitespace-normalised, as a literal pattern.
#     This is precise and applies to every correction without exception.
#   * a bare word-boundary pattern for each integer the log records as
#     superseded, but ONLY for values of 20 or more. A corpus of denominators
#     contains small integers everywhere -- "L2", "10/13", "7/13" -- and a bare
#     `7` or `2` pattern fires on correct text dozens of times per file. This
#     limitation is stated rather than tuned away.
#
# A new logged correction therefore arms a new guard without this file being
# edited, which is the difference between an instrument and a list.
STALE_PATTERNS = [
    # Structural framings with no distinctive number attached, which a
    # value-derived scan cannot produce. These four are the residue that would
    # otherwise have to be hand-maintained, and they are all superseded
    # *framings* rather than superseded values.
    (r"\b13\s*,\s*10\s*,\s*2\s*,\s*0\b", "gradient tuple (13, 10, 2, 0)"),
    (r"\b10/13\s*->\s*2/13\b", "gradient step 2/13"),
    (r"\b2\s+of\s+13\b", "internal consistency 2 of 13 (pre-correction)"),
    (r"\b2\s*/\s*13\b", "internal consistency 2/13 (pre-correction)"),
    (r"0\s*/\s*7\s*/\s*6", "pre-correction verdict roll-up 0/7/6"),
    (r"[Dd]elta\s*2\b", "the superseded 'Delta 2' framing"),
]

# ``label`` -> the log sentence shape, plus the rubric layer name to pair with a
# logged L-number so the shifted form can be derived too.
LOG_CORRECTIONS = [
    (r"stated\s+`(\d+)`\s+claims adjudicated,\s+`(\d+)`\s+contradicted",
     "pre-freeze claim-level summary", ()),
    (r"recorded\s+`0`\s+SUPPORTED,\s+`(\d+)`\s+PARTIALLY SUPPORTED,\s+"
     r"`(\d+)`\s+CONTRADICTED", "post-freeze verdict roll-up", ()),
    (r"recorded\s+`(\d+)`\s+of\s+`13`", "post-freeze internal consistency", ()),
    (r"labelled its rows\s+`L(\d)\b", "post-publication layer-label shift",
     ("Figure", "Method", "Selection", "Internal consistency", "Verdict")),
]

# Values below this are too common in a corpus of denominators to match bare.
BARE_VALUE_FLOOR = 20


def prose_pattern(sentence: str) -> str:
    """A literal pattern that tolerates re-typesetting of a logged sentence.

    The same sentence appears across the corpus inside backticks, inside
    ``$...$``, inside ``\\texttt{}``, and rewrapped across lines. Matching the
    log's wording verbatim would therefore fire only on the log's own wording,
    so the formatting delimiters are made optional and internal whitespace is
    matched loosely.
    """
    text = re.sub(r"\s+", " ", sentence).strip()
    parts: list[str] = []
    for token in re.split(r"([`$])", text):
        if token in ("`", "$"):
            parts.append("[`$]?")
        else:
            parts.append(re.escape(token).replace("\\ ", r"\s+"))
    return "".join(parts)


def derive_stale_patterns(dataset_text: str,
                          rubric: dict[str, int]) -> list[tuple[str, str]]:
    """Build the stale-figure patterns from the correction log's own text."""
    found: list[tuple[str, str]] = []
    for pattern, label, layer_names in LOG_CORRECTIONS:
        for match in re.finditer(pattern, dataset_text):
            sentence = re.sub(r"\s+", " ", match.group(0)).strip()
            found.append((prose_pattern(sentence), f"{label}, log wording"))
            for group in match.groups():
                value = int(group)
                if value >= BARE_VALUE_FLOOR:
                    # Guard against LaTeX column widths such as
                    # p{0.315\columnwidth} and against hash-like digit runs.
                    found.append((rf"(?<![\d.]){value}(?![\d.])",
                                  f"{label}: superseded value {value}"))
            if layer_names:
                first = int(match.group(1))
                for offset, name in enumerate(layer_names):
                    stated = first + offset
                    expected = rubric.get(name)
                    if expected is None or expected == stated:
                        continue
                    name_rx = re.escape(name).replace("\\ ", r"\s+")
                    found.append(
                        (rf"\bL{stated}\s*[{EMDASH}{ENDASH}-]+\s*{name_rx}",
                         f"{label}: {name} stated as L{stated}, rubric says "
                         f"L{expected}"))
    return found


# A line inside one of these is quoting a caught error as history. That is
# required by the dataset's own instruction to record corrections, so it is not
# a stale value.
CORRECTION_CONTEXT = re.compile(
    r"correction|corrected|correct |miscount|supersed|pre-freeze|post-freeze|"
    r"post-publication|delta|recorded as|block recorded|block stated|"
    r"block gave|recorded \d|shift|wrong summary|wrong verdict|wrong internal|"
    r"before this correction|was wrong|mispairing|was never wrong",
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


def audit_stale_figures(root: pathlib.Path, relpaths: list[str],
                        patterns: list[tuple[str, str]]) -> int:
    flagged = 0
    print()
    print(f"  stale figure strings, {len(patterns)} pattern(s): the "
          "dataset's correction log parsed at run time, plus 6 structural "
          "framings (matches are shown with context; occurrences inside a "
          "correction record are expected)")
    for relpath in relpaths:
        path = root / relpath
        if not path.exists():
            fail("A6", f"{relpath} does not exist")
            continue
        lines = read_lines(path)
        for pattern, why in patterns:
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
                       rubric: dict[str, int], in_scope_paths: list[str]
                       ) -> tuple[int, int]:
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
                in_scope = relpath in in_scope_paths
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
# A8 -- the frozen row table against the primary batch records
#
# This is the check that did not exist anywhere in the pipeline. The frozen row
# table was transcribed by the same author who wrote this script, so every
# comparison made against it so far has been a transcription against itself.
# The three batch reports are primary evidence, were written by three
# different evaluators, and carry their own per-row L3/L7/L8 columns. Joining
# on the repository name gives two genuinely independent origins for every U1,
# U2, L7 and U4 cell.
# --------------------------------------------------------------------------

def repo_key(record: dict) -> str:
    """Last path segment of a batch report's repo column."""
    return record["repo"].rsplit("/", 1)[-1].strip()


def dataset_key(name: str) -> str:
    """The dataset writes the layer as a parenthetical; drop it."""
    return re.sub(r"\s*\([^)]*\)\s*$", "", name.strip())


L8_NORMALISE = {"PARTIALLY SUPPORTED": "PARTIALLY", "SUPPORTED": "SUPPORTED",
                "CONTRADICTED": "CONTRADICTED", "UNVERIFIABLE": "UNVERIFIABLE"}


def check_rows_against_batch_reports(
        dataset_rows: list[dict], dataset: pathlib.Path,
        batch_paths: list[pathlib.Path]) -> int:
    """Diff every transcribed cell against the batch reports' own columns."""
    primary: dict[str, dict] = {}
    for path in batch_paths:
        for rec in parse_batch_layers(path):
            key = repo_key(rec)
            if key in primary:
                fail("A8", f"repository {key!r} appears in more than one batch "
                           "report; the join is ambiguous")
            primary[key] = rec

    cells = 0
    unmatched: list[str] = []
    for row in dataset_rows:
        key = dataset_key(row["package"])
        rec = primary.get(key)
        if rec is None:
            unmatched.append(key)
            continue
        # L3 is the batch rubric's numerical-claim layer and maps cell for cell
        # onto the dataset's U1 columns.
        expectations = (
            ("U1 total", row["total"], rec["L3 total"]),
            ("U1 correct", row["correct"], rec["L3 supported"]),
            ("U1 contradicted", row["contradicted"], rec["L3 contradicted"]),
            ("U1 unsupported", row["unsupported"], rec["L3 unsupported"]),
            ("L7 internal", row["internal"], rec["L7"]),
            ("U4 verdict", row["verdict"],
             L8_NORMALISE.get(rec["L8"], rec["L8"])),
            ("U2 exists", "Y" if rec["L1"] == "SUPPORTED" else "N",
             "Y" if row["exists"] else "N"),
            ("U2 reproduces", "Y" if rec["L2"] == "SUPPORTED" else "N",
             "Y" if row["reproduces"] else "N"),
        )
        for name, want, got in expectations:
            cells += 1
            if str(want) != str(got):
                fail("A8", f"row {row['n']} ({key}) {name}: frozen table "
                           f"{want!r} != {rec['_file'].rsplit('/', 1)[-1]} "
                           f"{got!r}")
        print(f"  ok  row {row['n']:2d} {key:<32} 8/8 cells agree with "
              f"{rec['_file'].rsplit('/', 1)[-1]}")

    for key in unmatched:
        fail("A8", f"frozen row {key!r} has no counterpart in any batch "
                   "report; the row cannot be traced to primary evidence")

    print(f"  {cells} cells compared across {len(dataset_rows)} rows against "
          "three independent primary records")

    # Bit-for-bit reproduction is not a column of the row table, so nothing
    # above constrains it. This checks the one thing that can be checked from
    # inside the corpus: every repository the dataset lists as reproducing
    # byte-identically is a scored row. A count quoted for a package outside
    # the corpus is worse than no count.
    block = parse_bitforbit(dataset)
    scored = {dataset_key(r["package"]) for r in dataset_rows}
    exact = [b for b in block if b["scope"] == "exact"]
    print()
    print(f"  bit-for-bit block: {len(exact)} exact, "
          f"{len(block) - len(exact)} qualified, from "
          f"{len(dataset_rows)} scored rows")
    seen: set[str] = set()
    for entry in block:
        key = dataset_key(entry["package"])
        if key not in scored:
            fail("A8", f"bit-for-bit block names {entry['package']!r}, which "
                       "is not a scored row of the frozen table")
        if key in seen:
            fail("A8", f"bit-for-bit block lists {entry['package']!r} twice")
        seen.add(key)
        print(f"    ok  {entry['scope']:<30} {entry['package']}")
    if not block:
        fail("A8", "no bit-for-bit block found; any count of bit-for-bit "
                   "reproduction in the paper would be an assertion")
    return cells


BITFORBIT_LINE = re.compile(
    r"^(?P<package>[A-Za-z0-9][\w.-]*)\s+"
    r"(?P<scope>exact|exact-scientific-fields-only)(?:\s\s+(?P<note>.*))?$")


def parse_bitforbit(dataset: pathlib.Path) -> list[dict]:
    lines = read_lines(dataset)
    try:
        start = next(i for i, ln in enumerate(lines)
                     if ln.startswith("### Bit-for-bit artifact reproduction"))
    except StopIteration:
        return []
    out: list[dict] = []
    in_block = False
    for line in lines[start + 1:]:
        if line.strip().startswith("```"):
            in_block = not in_block
            continue
        if not in_block:
            continue
        m = BITFORBIT_LINE.match(line.strip())
        if m:
            out.append({"package": m.group("package"),
                        "scope": m.group("scope"),
                        "note": (m.group("note") or "").strip()})
    return out


# --------------------------------------------------------------------------
# A9 -- the cross-batch claim-pool split, re-derived
#
# The 2026-09-30 defect was a correct rate attached to the wrong row span.
# Row-level reconciliation cannot see it: it compares sums against sums, and a
# mispaired rate is not a wrong sum. What sees it is re-deriving each span from
# the row table and comparing against the figure the dataset pairs with that
# span. The spans themselves are then checked against the per-report totals in
# the batch reports, so the partition is verified and not assumed.
# --------------------------------------------------------------------------

CROSS_BATCH_LINE = re.compile(
    r"^(?P<label>.+?)\s+rows\s+(?P<lo>\d+)\s*-\s*(?P<hi>\d+)\s+"
    r"(?P<correct>\d+)\s*/\s*(?P<claims>\d+)\s+(?P<rate>[\d.]+)%")


def parse_cross_batch(path: pathlib.Path) -> list[dict]:
    lines = read_lines(path)
    try:
        start = next(i for i, ln in enumerate(lines)
                     if ln.strip().startswith("## Cross-batch comparability"))
    except StopIteration:
        fail("A9", f"{path.name} has no '## Cross-batch comparability' section")
        return []
    block: list[str] = []
    in_block = False
    for line in lines[start + 1:]:
        if line.strip().startswith("```"):
            in_block = not in_block
            continue
        if in_block:
            block.append(line.strip())
    spans = []
    for line in block:
        m = CROSS_BATCH_LINE.match(line)
        if m:
            spans.append({"label": m.group("label").strip(),
                          "lo": int(m.group("lo")), "hi": int(m.group("hi")),
                          "correct": int(m.group("correct")),
                          "claims": int(m.group("claims")),
                          "rate": float(m.group("rate"))})
    return spans


def report_totals(paths: list[pathlib.Path]) -> list[tuple[str, int, int, int]]:
    """(label, rows, claims, correct) re-rolled from one batch report."""
    out = []
    for path in paths:
        recs = parse_batch_layers(path)
        out.append((path.stem, len(recs),
                    sum(int(r["L3 total"]) for r in recs),
                    sum(int(r["L3 supported"]) for r in recs)))
    return out


def check_cross_batch(dataset_rows: list[dict], dataset: pathlib.Path,
                      batch_paths: list[pathlib.Path]) -> None:
    spans = parse_cross_batch(dataset)
    if len(spans) < 2:
        fail("A9", f"cross-batch block parsed {len(spans)} span(s), expected "
                   "at least the two batch rates")
        return

    by_index = {r["n"]: r for r in dataset_rows}
    print()
    print(f"  {'span':<40} {'dataset':>17}  {'row table':>17}  status")
    for span in spans:
        picked = [by_index[i] for i in range(span["lo"], span["hi"] + 1)
                  if i in by_index]
        if len(picked) != span["hi"] - span["lo"] + 1:
            fail("A9", f"cross-batch span {span['label']!r} names rows "
                       f"{span['lo']}-{span['hi']}, which the row table does "
                       "not contain")
            continue
        claims = sum(r["total"] for r in picked)
        correct = sum(r["correct"] for r in picked)
        rate = 100.0 * correct / claims if claims else 0.0
        label = span["label"]
        if len(label) > 40:
            label = label[:37] + "..."
        stated = f"{span['correct']}/{span['claims']} = {span['rate']}%"
        recomputed = f"{correct}/{claims} = {rate:.1f}%"
        ok = (claims == span["claims"] and correct == span["correct"]
              and round(rate, 1) == span["rate"])
        if not ok:
            fail("A9", f"cross-batch span {span['label']!r} (rows "
                       f"{span['lo']}-{span['hi']}): dataset records {stated}, "
                       f"the row table gives {correct}/{claims} = "
                       f"{rate:.4f}%")
        print(f"  rows {span['lo']}-{span['hi']} {label:<33} {stated:>17}  "
              f"{recomputed:>17}  {'ok' if ok else 'MISMATCH'}")

    # The partition itself, against the primary records. Batches 1 and 2 must
    # sum to rows 1-8 and batch 3 to rows 9-13 for the comparison above to mean
    # anything at all. A span that is not one of those two partitions -- the
    # four-package denominator, which counts cd once -- is checked against the
    # row table above and is deliberately not held to a report total.
    print()
    print("  per-report claim-pool totals, re-rolled from the batch reports")
    totals = report_totals(batch_paths)
    # (rows, claims, correct) for each partition.
    b12 = (sum(t[1] for t in totals[:2]), sum(t[2] for t in totals[:2]),
           sum(t[3] for t in totals[:2]))
    b3 = (totals[2][1], totals[2][2], totals[2][3])
    partitions = {"batches 1-2 (reports 1+2)": (1, b12),
                  "batch 3 (report 3, five rows)": (9, b3)}
    for label, (first, got) in partitions.items():
        print(f"    {label:<36} rows {first}-{first + got[0] - 1}: "
              f"{got[2]}/{got[1]} = {100.0 * got[2] / got[1]:.4f}%")
    if b12[0] != 8 or b3[0] != 5:
        fail("A9", f"the batch reports supply {b12[0]}+{b3[0]} rows; the "
                   f"dataset's cross-batch block assumes 8+5")
    else:
        print("    ok  the reports supply 8 rows to batches 1-2 and 5 to "
              "batch 3, which is the partition the dataset's spans assume")
    for span in spans:
        for first, got in partitions.values():
            if span["lo"] == first and span["hi"] == first + got[0] - 1:
                if span["claims"] != got[1] or span["correct"] != got[2]:
                    fail("A9", f"cross-batch span {span['label']!r}: the batch "
                               f"reports give {got[2]}/{got[1]}, the dataset "
                               f"records {span['correct']}/{span['claims']}")


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT,
                    help="corpus root (default: discovered from this "
                         "script's location, %s)" % DEFAULT_ROOT)
    args = ap.parse_args()
    root: pathlib.Path = args.root.resolve()

    print("E1 dataset verification")
    print("script: %s" % HERE)
    print("root: %s" % root)

    LAYOUT.update(resolve_layout(root))
    print("layout:")
    for key in sorted(LAYOUT):
        print(f"  {key:<14} {LAYOUT[key]}")

    rubric_path = root / LAYOUT["rubric"]

    # ---- A0 -------------------------------------------------------------
    section("A0  canonical layer table, read from the rubric")
    rubric = load_rubric_layers(rubric_path)
    for name in sorted(rubric, key=lambda n: rubric[n]):
        print(f"  L{rubric[name]} {name}")
    if len(rubric) != 8:
        fail("A0", f"expected 8 rubric layers, parsed {len(rubric)}")

    # ---- A1 -------------------------------------------------------------
    section("A1  recompute dataset aggregates from the thirteen rows")
    dataset = root / LAYOUT["dataset"]
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
    aggregate = root / LAYOUT["aggregate"]
    check_aggregate_labels(aggregate, rubric)

    # ---- A4 -------------------------------------------------------------
    section("A4  aggregate counts re-rolled from the three batch reports")
    batch_paths = [root / LAYOUT["batch1"], root / LAYOUT["batch2"],
                   root / LAYOUT["batch3"]]
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
    push_root = next((root / p for p in PUSH_ROOT_RELPATHS
                      if (root / p).is_dir()), None)
    if push_root is None:
        note("A5 skipped: no research-backlog-repo/ under this root. That tree "
             "exists only in the author's working copy, so a public clone has "
             "nothing to compare against. Skipped loudly rather than silently, "
             "because in a public clone the pushed copies are the ONLY copy and "
             "the check has nothing to prove.")
    else:
        compare_copies(dataset, push_root / "audit" / dataset.name,
                       dataset.name, root)
        compare_copies(aggregate, push_root / "audit" / aggregate.name,
                       aggregate.name, root)

    # ---- A6 -------------------------------------------------------------
    section("A6  stale-string and stale-label audit")
    dataset_text = dataset.read_text(encoding="utf-8")
    patterns = STALE_PATTERNS + derive_stale_patterns(dataset_text, rubric)
    in_scope_paths = [LAYOUT["aggregate"], LAYOUT["dataset"],
                      LAYOUT["paper"], LAYOUT["paper_readme"],
                      LAYOUT["make_figures"], LAYOUT["rows_csv"],
                      LAYOUT["classes_csv"]]
    if push_root is not None:
        in_scope_paths += [rel(root, push_root / "audit" / dataset.name),
                           rel(root, push_root / "audit" / aggregate.name),
                           rel(root, push_root / "audit" / "README.md")]
    in_scope_paths = [p for p in in_scope_paths if (root / p).is_file()]
    in_scope_bad, read_only_bad = audit_stale_labels(root, in_scope_paths,
                                                     rubric, in_scope_paths)
    audit_stale_figures(root, in_scope_paths, patterns)
    if read_only_bad:
        print()
        print(f"  {read_only_bad} shifted layer label(s) remain in files outside "
              "the in-scope set. They are reported, not fixed here.")

    # ---- A8 -------------------------------------------------------------
    section("A8  frozen row table against the three primary batch records")
    check_rows_against_batch_reports(rows, dataset, batch_paths)

    # ---- A9 -------------------------------------------------------------
    section("A9  cross-batch claim-pool split, re-derived from the rows")
    check_cross_batch(rows, dataset, batch_paths)

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
