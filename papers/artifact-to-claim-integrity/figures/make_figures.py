#!/usr/bin/env python3
"""Generate the two figures for the artifact-to-claim-integrity paper.

Dependency-free: it emits vector PDF using only the Python standard library,
so both figures regenerate on any machine with a Python 3 interpreter and no
network access.

Every geometric quantity in the output is derived from the committed data
files. Nothing is hand-placed: bar extents, axis ticks, segment widths,
column widths, annotation strings and row labels are all computed from the
CSVs, and column widths are measured from the text they must hold.

The script recomputes every derived value the manuscript quotes and aborts
(exit 1, nothing written) if any recomputed value disagrees with the frozen
dataset. It also reports the arithmetic errors the dataset's own aggregate
layer has made and had corrected, because the manuscript is obliged to
disclose them; they are printed here and embedded in the figure.

Usage
-----
    python3 make_figures.py             # write both PDFs, run all checks
    python3 make_figures.py --verify    # print derived values, write nothing

Provenance of the data
----------------------
``data/e1_rows.csv`` is a verbatim transcription of the thirteen-row table in
``research-audit/E1-DATASET-v1.0.md`` (the frozen dataset of record, frozen
2026-09-29). ``data/failure_classes.csv`` transcribes the taxonomy section of
the same file together with the cross-package findings in
``research-audit/E1-AGGREGATE.md``. No value in either CSV originates in this
script.
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import sys

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

HERE = pathlib.Path(__file__).resolve().parent
DATA_ROWS = HERE / "data" / "e1_rows.csv"
DATA_CLASSES = HERE / "data" / "failure_classes.csv"
OUT_GRADIENT = HERE / "fig_layer_gradient.pdf"
OUT_CLASSES = HERE / "fig_failure_classes.pdf"

# --------------------------------------------------------------------------
# Values as recorded in the frozen dataset's derived-metrics block.
#
# These are transcribed from E1-DATASET-v1.0.md and are the targets the
# recomputation is checked against. The block carried two figures that did not
# survive being summed back out of the row table; both were corrected in the
# dataset on 2026-09-30 and logged in its correction log, and the constants
# below now match the corrected block. The pre-correction values are kept in
# SUPERSEDED_* below so the figure can state what was wrong, not only what is
# right; see corrections().
# --------------------------------------------------------------------------

DATASET = "E1-DATASET-v1.0.md (frozen 2026-09-29, corrected 2026-09-30)"

RECORDED_CLAIM_TOTAL = 375
RECORDED_CLAIM_CORRECT = 263
RECORDED_CLAIM_CONTRADICTED = 95
RECORDED_CLAIM_UNSUPPORTED = 17

RECORDED_U2_EXISTS = 13
RECORDED_U2_REPRODUCES = 10
RECORDED_U3_BROKEN = 13
RECORDED_U3_ABSENT = 8
RECORDED_INTERNAL_CONSISTENCY = 1
RECORDED_SUPPORTED = 0
RECORDED_PARTIALLY = 8
RECORDED_CONTRADICTED = 5

RECORDED_GRADIENT = (13, 10, 1, 0)
RECORDED_PKG_GE1_CONTRADICTED = 13
RECORDED_PKG_GE1_UNSUPPORTED = 8

# What the derived-metrics block recorded before the 2026-09-30 correction.
SUPERSEDED_INTERNAL_CONSISTENCY = 2
SUPERSEDED_PARTIALLY = 7
SUPERSEDED_CONTRADICTED = 6

# Cross-batch granularity record, E1-DATASET-v1.0.md section
# "Cross-batch comparability -- recorded limitation".
RECORDED_BATCH12_CLAIMS = 270
RECORDED_BATCH12_CORRECT = 213
RECORDED_BATCH3_CLAIMS = 81
RECORDED_BATCH3_CORRECT = 28
RECORDED_BATCH3_CLAIMS_WITH_AUDIT_ROW = 105
RECORDED_BATCH3_CORRECT_WITH_AUDIT_ROW = 50

N_ROWS = 13

# Rows 1..8 are batches 1 and 2. Row 13 is the audit-manuscript layer of the
# cd programme, which batch 3 scores as a fifth row. The dataset's own
# cross-batch comparability note quotes 34.6%, which is batch 3 over four
# packages (rows 9..12), excluding the audit row.
BATCH12_ROWS = range(1, 9)
BATCH3_ROWS = range(9, 13)
BATCH3_WITH_AUDIT_ROW = range(9, 14)


# --------------------------------------------------------------------------
# Minimal PDF writer (base-14 fonts, no external dependency)
# --------------------------------------------------------------------------

class PDF:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self.ops: list[str] = []

    # -- graphics state ---------------------------------------------------
    def fill(self, rgb) -> None:
        self.ops.append(f"{rgb[0]:.4f} {rgb[1]:.4f} {rgb[2]:.4f} rg")

    def stroke(self, rgb) -> None:
        self.ops.append(f"{rgb[0]:.4f} {rgb[1]:.4f} {rgb[2]:.4f} RG")

    def line_width(self, width: float) -> None:
        self.ops.append(f"{width:.2f} w")

    def rect(self, x: float, y: float, w: float, h: float) -> None:
        self.ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re")

    def line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        self.ops.append(f"{x1:.2f} {y1:.2f} {x2:.2f} {y2:.2f} m "
                        f"{x2:.2f} {y2:.2f} l S")

    def fill_rect(self, x: float, y: float, w: float, h: float, rgb) -> None:
        self.fill(rgb)
        self.rect(x, y, w, h)
        self.ops.append("f")

    def stroke_rect(self, x: float, y: float, w: float, h: float, rgb,
                    width: float = 0.6) -> None:
        self.stroke(rgb)
        self.line_width(width)
        self.rect(x, y, w, h)
        self.ops.append("S")

    def translate_all(self, dy: float) -> None:
        """Shift every drawing operation vertically, once, at the end."""
        if dy:
            self.ops.insert(0, "q")
            self.ops.insert(1, f"1 0 0 1 0 {dy:.2f} cm")
            self.ops.append("Q")

    # -- text -------------------------------------------------------------
    @staticmethod
    def _escape(text: str) -> str:
        return (text.replace("\\", r"\\")
                    .replace("(", r"\(")
                    .replace(")", r"\)"))

    def text(self, x: float, y: float, size: float, text: str,
             bold: bool = False, rgb=(0.0, 0.0, 0.0)) -> None:
        self.fill(rgb)
        self.ops.append("BT")
        self.ops.append(f"/{'F2' if bold else 'F1'} {size:.2f} Tf")
        self.ops.append(f"{x:.2f} {y:.2f} Td")
        self.ops.append(f"({self._escape(text)}) Tj")
        self.ops.append("ET")

    def text_right(self, x: float, y: float, size: float, text: str,
                   bold: bool = False, rgb=(0.0, 0.0, 0.0)) -> None:
        self.text(x - text_width(text, size, bold), y, size, text, bold, rgb)

    def text_center(self, x: float, y: float, size: float, text: str,
                    bold: bool = False, rgb=(0.0, 0.0, 0.0)) -> None:
        self.text(x - text_width(text, size, bold) / 2.0, y, size, text,
                  bold, rgb)

    # -- output -----------------------------------------------------------
    def build(self) -> bytes:
        content = "\n".join(self.ops).encode("latin-1", errors="replace")
        objects = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            (b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 "
             + f"{self.width:.0f} {self.height:.0f}".encode("ascii")
             + b"] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> "
               b"/ProcSet [/PDF /Text] >> /Contents 6 0 R >>"),
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
            b"/Encoding /WinAnsiEncoding >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold "
            b"/Encoding /WinAnsiEncoding >>",
            b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n"
            + content + b"\nendstream",
        ]

        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for index, body in enumerate(objects, start=1):
            offsets.append(len(out))
            out += f"{index} 0 obj\n".encode("ascii") + body + b"\nendobj\n"

        xref_at = len(out)
        out += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
        out += b"0000000000 65535 f \n"
        for offset in offsets[1:]:
            out += f"{offset:010d} 00000 n \n".encode("ascii")
        out += (b"trailer\n<< /Size " + str(len(objects) + 1).encode("ascii")
                + b" /Root 1 0 R >>\nstartxref\n"
                + str(xref_at).encode("ascii") + b"\n%%EOF\n")
        return bytes(out)


# Helvetica advance widths for the printable ASCII range 32..126, in 1/1000 em.
# A per-string sum is materially more accurate than a flat 0.5 em estimate and
# keeps centred, right-aligned and wrapped text visually correct. The tuples are
# padded with 32 leading zeros so an advance is table[ord(char)].
_W = (
    278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333,
    278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278,
    584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278,
    500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944,
    667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
    278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500,
    278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584,
)
_BOLD_W = (
    278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333,
    278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333,
    584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278,
    556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944,
    667, 667, 611, 333, 278, 333, 584, 556, 333, 556, 611, 556, 556, 500,
    556, 556, 278, 556, 556, 222, 222, 556, 222, 833, 611, 556, 556, 556,
    333, 556, 556, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584,
)
# Printable ASCII must be fully covered or centred labels will drift.
assert len(_W) >= 95 and len(_BOLD_W) >= 95, "width tables too short"
_W = (0,) * 32 + _W
_BOLD_W = (0,) * 32 + _BOLD_W


def text_width(text: str, size: float, bold: bool = False) -> float:
    table = _BOLD_W if bold else _W
    total = 0
    for char in text:
        code = ord(char)
        total += table[code] if code < len(table) else 556
    return total * size / 1000.0


def wrap(text: str, size: float, max_w: float, bold: bool = False) -> list[str]:
    """Greedy word wrap against the measured advance width.

    A single word longer than ``max_w`` is hard-split on character boundaries
    rather than allowed to overflow the figure.
    """
    lines: list[str] = []
    current = ""
    for word in text.split():
        while text_width(word, size, bold) > max_w:
            cut = len(word)
            while cut > 1 and text_width(word[:cut], size, bold) > max_w:
                cut -= 1
            if current:
                lines.append(current)
                current = ""
            lines.append(word[:cut])
            word = word[cut:]
        candidate = f"{current} {word}".strip()
        if current and text_width(candidate, size, bold) > max_w:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------

BLACK = (0.08, 0.08, 0.08)
GREY_TEXT = (0.38, 0.38, 0.38)
GRID = (0.88, 0.88, 0.88)
RULE = (0.62, 0.62, 0.62)
EXISTS = (0.20, 0.40, 0.62)
REPRO = (0.36, 0.58, 0.78)
INTERNAL = (0.74, 0.62, 0.28)
VERDICT = (0.74, 0.24, 0.18)
CORRECT = (0.30, 0.52, 0.38)
CONTRADICTED = (0.74, 0.36, 0.20)
UNSUPPORTED = (0.60, 0.58, 0.56)
ACCENT = (0.62, 0.20, 0.16)
WHITE = (1.0, 1.0, 1.0)


# --------------------------------------------------------------------------
# Data loading and derivation
# --------------------------------------------------------------------------

class Correction:
    """A recorded arithmetic error in the frozen dataset's aggregate layer.

    The layer that fails is the summary block, never the row table. Each entry
    is printed by the script, embedded in the figure, and written up in the
    manuscript's correction log. The corrected value is recomputed from the rows
    here rather than hard-coded, so a figure that stops matching the corrected
    block cannot render. None of them changes the paper's central result.
    """

    def __init__(self, label: str, recorded: str, corrected: str,
                 note: str) -> None:
        self.label = label
        self.recorded = recorded
        self.corrected = corrected
        self.note = note

    def __str__(self) -> str:
        return (f"{self.label}: derived-metrics block recorded "
                f"{self.recorded}, corrected to {self.corrected}")


def read_csv(path: pathlib.Path) -> list[dict]:
    """Read a CSV, skipping ``#`` provenance comments above the header."""
    with path.open(newline="", encoding="utf-8") as handle:
        lines = [ln for ln in handle if not ln.lstrip().startswith("#")]
    return list(csv.DictReader(lines))


def load_rows(path: pathlib.Path) -> list[dict]:
    rows = read_csv(path)
    if not rows:
        raise SystemExit(f"no rows in {path}")
    for row in rows:
        row["row"] = int(row["row"])
        for key in ("u1_total", "u1_correct", "u1_contradicted",
                    "u1_unsupported"):
            row[key] = int(row[key])
    return sorted(rows, key=lambda r: r["row"])


def load_classes(path: pathlib.Path) -> list[dict]:
    rows = read_csv(path)
    if len(rows) != 3:
        raise SystemExit(f"expected 3 failure classes in {path}, got {len(rows)}")
    return sorted(rows, key=lambda r: int(r["class_id"]))


def tally(rows: list[dict], key: str) -> int:
    return sum(1 for r in rows if r[key] == "Y")


def verdict_counts(rows: list[dict]) -> dict[str, int]:
    out = {"SUPPORTED": 0, "PARTIALLY": 0, "CONTRADICTED": 0}
    for row in rows:
        out[row["u4_verdict"]] += 1
    return out


def derived(rows: list[dict]) -> dict:
    d: dict = {}
    d["n_rows"] = len(rows)
    d["claims_total"] = sum(r["u1_total"] for r in rows)
    d["claims_correct"] = sum(r["u1_correct"] for r in rows)
    d["claims_contradicted"] = sum(r["u1_contradicted"] for r in rows)
    d["claims_unsupported"] = sum(r["u1_unsupported"] for r in rows)
    d["u2_exists"] = tally(rows, "u2_exists")
    d["u2_reproduces"] = tally(rows, "u2_reproduces")
    d["u3_broken"] = tally(rows, "u3_broken")
    d["u3_absent"] = tally(rows, "u3_absent")
    d["internal_consistency"] = tally(rows, "l7_internal_supported")
    d["l7_strict_supported"] = sum(1 for r in rows
                                   if r["l7_internal"] == "SUPPORTED")
    d["verdicts"] = verdict_counts(rows)
    d["pkg_ge1_contradicted"] = sum(1 for r in rows if r["u1_contradicted"] > 0)
    d["pkg_ge1_unsupported"] = sum(1 for r in rows if r["u1_unsupported"] > 0)
    d["gradient"] = (d["u2_exists"], d["u2_reproduces"],
                     d["internal_consistency"], d["verdicts"]["SUPPORTED"])
    d["pct_correct"] = 100.0 * d["claims_correct"] / d["claims_total"]
    d["pct_contradicted"] = 100.0 * d["claims_contradicted"] / d["claims_total"]
    d["pct_unsupported"] = 100.0 * d["claims_unsupported"] / d["claims_total"]

    def subset(span) -> tuple[int, int]:
        picked = [r for r in rows if r["row"] in span]
        return (sum(r["u1_total"] for r in picked),
                sum(r["u1_correct"] for r in picked))

    d["batch12_claims"], d["batch12_correct"] = subset(BATCH12_ROWS)
    d["batch3_claims"], d["batch3_correct"] = subset(BATCH3_ROWS)
    (d["batch3w_claims"],
     d["batch3w_correct"]) = subset(BATCH3_WITH_AUDIT_ROW)
    d["pct_batch12"] = 100.0 * d["batch12_correct"] / d["batch12_claims"]
    d["pct_batch3"] = 100.0 * d["batch3_correct"] / d["batch3_claims"]
    d["pct_batch3w"] = 100.0 * d["batch3w_correct"] / d["batch3w_claims"]

    # Cross-layer disagreement: the joint distribution of U2 reproduction and
    # U4 verdict. If reproduction were a usable proxy for package integrity,
    # the reproduced block would be dominated by SUPPORTED verdicts.
    d["repro_verdicts"] = {"SUPPORTED": 0, "PARTIALLY": 0, "CONTRADICTED": 0}
    d["norepro_verdicts"] = {"SUPPORTED": 0, "PARTIALLY": 0, "CONTRADICTED": 0}
    for row in rows:
        bucket = ("repro_verdicts" if row["u2_reproduces"] == "Y"
                  else "norepro_verdicts")
        d[bucket][row["u4_verdict"]] += 1
    d["repro_n"] = d["u2_reproduces"]
    d["norepro_n"] = N_ROWS - d["u2_reproduces"]
    d["repro_and_supported"] = d["repro_verdicts"]["SUPPORTED"]
    return d


def corrections(d: dict) -> list[Correction]:
    """The arithmetic errors the manuscript is obliged to disclose."""
    v = d["verdicts"]
    return [
        Correction(
            "U4 verdict distribution",
            f"{RECORDED_SUPPORTED} / {SUPERSEDED_PARTIALLY} / "
            f"{SUPERSEDED_CONTRADICTED}",
            f"{v['SUPPORTED']} / {v['PARTIALLY']} / {v['CONTRADICTED']}",
            "an arithmetic slip in the block's hand-written roll-up: three "
            "PARTIALLY and one CONTRADICTED in batch 1, four PARTIALLY in "
            "batch 2, one PARTIALLY and four CONTRADICTED in batch 3 gives "
            "8 and 5, not 7 and 6. All three batch reports agree with the "
            "rows",
        ),
        Correction(
            "internal consistency",
            f"{SUPERSEDED_INTERNAL_CONSISTENCY} of 13",
            f"{d['internal_consistency']} of 13",
            "a miscount, not a summation error, which is why the first round "
            "of reconciliation missed it. The earlier draft counted the two "
            "rows whose layer stack places internal consistency at SUPPORTED, "
            "sc-ieee-package and cd-covert-anomaly-detection; the recorded "
            "internal-consistency column marks only the first, because the "
            "second is CONTRADICTED at that layer on a ddof disclosure alone",
        ),
    ]


def check(rows: list[dict], d: dict) -> tuple[list[str], list[Delta]]:
    """Recompute every derived value the manuscript quotes. Abort on mismatch."""
    problems: list[str] = []

    def expect(label: str, actual, required) -> None:
        if actual != required:
            problems.append(f"{label}: recomputed {actual!r} != "
                            f"{DATASET} {required!r}")

    expect("row count", d["n_rows"], N_ROWS)
    expect("row indices", [r["row"] for r in rows], list(range(1, N_ROWS + 1)))

    # Each row must be internally additive before any column is summed.
    for row in rows:
        split = row["u1_correct"] + row["u1_contradicted"] + row["u1_unsupported"]
        if split != row["u1_total"]:
            problems.append(
                f"row {row['row']} ({row['package']}): "
                f"{row['u1_correct']}+{row['u1_contradicted']}+"
                f"{row['u1_unsupported']} = {split} != total {row['u1_total']}")

    expect("U1 claims adjudicated", d["claims_total"], RECORDED_CLAIM_TOTAL)
    expect("U1 CLAIM-CORRECT", d["claims_correct"], RECORDED_CLAIM_CORRECT)
    expect("U1 CLAIM-CONTRADICTED", d["claims_contradicted"],
           RECORDED_CLAIM_CONTRADICTED)
    expect("U1 CLAIM-UNSUPPORTED", d["claims_unsupported"],
           RECORDED_CLAIM_UNSUPPORTED)
    expect("U2 artifact exists", d["u2_exists"], RECORDED_U2_EXISTS)
    expect("U2 artifact reproduces", d["u2_reproduces"], RECORDED_U2_REPRODUCES)
    expect("U3 broken by contradiction", d["u3_broken"], RECORDED_U3_BROKEN)
    expect("U3 relation absent", d["u3_absent"], RECORDED_U3_ABSENT)
    expect("internal consistency", d["internal_consistency"],
           RECORDED_INTERNAL_CONSISTENCY)
    expect("gradient", list(d["gradient"]), list(RECORDED_GRADIENT))
    expect("packages with >=1 contradicted claim", d["pkg_ge1_contradicted"],
           RECORDED_PKG_GE1_CONTRADICTED)
    expect("packages with >=1 unsupported claim", d["pkg_ge1_unsupported"],
           RECORDED_PKG_GE1_UNSUPPORTED)
    expect("U4 SUPPORTED", d["verdicts"]["SUPPORTED"], RECORDED_SUPPORTED)
    expect("U4 PARTIALLY SUPPORTED", d["verdicts"]["PARTIALLY"],
           RECORDED_PARTIALLY)
    expect("U4 CONTRADICTED", d["verdicts"]["CONTRADICTED"],
           RECORDED_CONTRADICTED)
    expect("verdict counts sum to the row count",
           sum(d["verdicts"].values()), N_ROWS)

    # The two internal-consistency encodings are redundant on purpose. If they
    # ever disagree, one of them is a miscount of the recorded column rather
    # than a roll-up of it, and that is exactly the error of 2026-09-30.
    expect("internal-consistency flag agrees with the recorded column",
           d["internal_consistency"], d["l7_strict_supported"])

    # The recorded percentages must round-trip from the recomputed counts.
    for label, actual, required in (
        ("CLAIM-CORRECT", d["pct_correct"], 70.1),
        ("CLAIM-CONTRADICTED", d["pct_contradicted"], 25.3),
        ("CLAIM-UNSUPPORTED", d["pct_unsupported"], 4.5),
    ):
        if round(actual, 1) != required:
            problems.append(f"{label}: recomputed {actual:.4f}% does not round "
                            f"to the recorded {required}%")

    # Cross-batch granularity record.
    expect("batches 1-2 claim pool", d["batch12_claims"],
           RECORDED_BATCH12_CLAIMS)
    expect("batches 1-2 correct", d["batch12_correct"], RECORDED_BATCH12_CORRECT)
    expect("batch 3 claim pool (4 packages)", d["batch3_claims"],
           RECORDED_BATCH3_CLAIMS)
    expect("batch 3 correct (4 packages)", d["batch3_correct"],
           RECORDED_BATCH3_CORRECT)
    expect("batch 3 claim pool (5 rows)", d["batch3w_claims"],
           RECORDED_BATCH3_CLAIMS_WITH_AUDIT_ROW)
    expect("batch 3 correct (5 rows)", d["batch3w_correct"],
           RECORDED_BATCH3_CORRECT_WITH_AUDIT_ROW)
    if round(d["pct_batch12"], 1) != 78.9:
        problems.append(f"batches 1-2 rate {d['pct_batch12']:.4f}% does not "
                        f"round to the recorded 78.9%")
    if round(d["pct_batch3"], 1) != 34.6:
        problems.append(f"batch 3 rate {d['pct_batch3']:.4f}% does not round "
                        f"to the recorded 34.6%")
    if round(d["pct_batch3w"], 1) != 47.6:
        problems.append(f"batch 3 five-row rate {d['pct_batch3w']:.4f}% does "
                        f"not round to the recorded 47.6%")

    # Cross-layer disagreement. The reproduced block must not contain a single
    # SUPPORTED verdict, or the manuscript's central claim would be false.
    expect("rows with a reproduced artifact AND a SUPPORTED verdict",
           d["repro_and_supported"], 0)
    expect("reproduced-row verdict block size", sum(d["repro_verdicts"].values()),
           RECORDED_U2_REPRODUCES)
    expect("non-reproduced-row verdict block size",
           sum(d["norepro_verdicts"].values()), N_ROWS - RECORDED_U2_REPRODUCES)

    return problems, corrections(d)


# --------------------------------------------------------------------------
# Shared page scaffolding
# --------------------------------------------------------------------------

class Page:
    """Full-width single-page figure with a downward cursor and auto-height.

    The page is laid out from a virtual top, then the whole drawing is
    translated so the MediaBox is exactly the extent of the content. This
    keeps the figure from overflowing or leaving a dead band at the bottom.
    """

    WIDTH = 520.0
    LEFT = 44.0
    MARGIN = 28.0
    HEADROOM = 13.0

    def __init__(self, title: str, subtitle: str) -> None:
        self.pdf = PDF(self.WIDTH, 1000.0)
        self.content_w = self.WIDTH - 2 * self.LEFT
        self.top = self.pdf.height - self.MARGIN - self.HEADROOM
        self.y = self.top
        self.pdf.text(self.LEFT, self.y, 12.0, title, bold=True)
        self.y -= 15.0
        for line in wrap(subtitle, 8.0, self.content_w):
            self.pdf.text(self.LEFT, self.y, 8.0, line, rgb=GREY_TEXT)
            self.y -= 10.5

    def heading(self, text: str) -> None:
        self.y -= 8.0
        self.pdf.text(self.LEFT, self.y, 9.5, text, bold=True, rgb=BLACK)
        self.y -= 15.0

    def paragraph(self, text: str, size: float = 7.5, rgb=BLACK,
                  bold: bool = False, lead: float = 9.8,
                  width: float | None = None, x: float | None = None) -> None:
        w = self.content_w if width is None else width
        ox = self.LEFT if x is None else x
        for line in wrap(text, size, w, bold):
            self.pdf.text(ox, self.y, size, line, rgb=rgb, bold=bold)
            self.y -= lead

    def label_at(self, text: str, x: float, width: float,
                 size: float = 8.5) -> None:
        """Draw a heading at an explicit x without moving the cursor.

        Used for side-by-side headings, where a cursor-advancing helper would
        push each successive heading onto a different line. The width is
        checked because a heading that overruns its column is invisible in the
        log and only shows up as clipped text.
        """
        w = text_width(text, size, True)
        if w > width:
            raise SystemExit(
                f'heading "{text}" is {w:.1f}pt wide, column is {width:.1f}pt')
        self.pdf.text(x, self.y, size, text, bold=True, rgb=BLACK)

    def column(self, text: str, x: float, width: float, size: float = 7.0,
               rgb=BLACK, bold: bool = False, lead: float = 9.0) -> None:
        """Draw a wrapped block at an explicit x. Returns the y reached."""
        y = self.y
        for line in wrap(text, size, width, bold):
            self.pdf.text(x, y, size, line, rgb=rgb, bold=bold)
            y -= lead
        return y

    def gap(self, amount: float) -> None:
        self.y -= amount

    def rule(self, colour=RULE, width: float = 0.6) -> None:
        self.pdf.stroke(colour)
        self.pdf.line_width(width)
        self.pdf.line(self.LEFT, self.y + 8.0, self.LEFT + self.content_w,
                      self.y + 8.0)

    def finish(self, out_path: pathlib.Path) -> None:
        bottom = self.y
        self.pdf.translate_all(self.MARGIN - bottom)
        self.pdf.height = (self.top - bottom) + 2 * self.MARGIN + self.HEADROOM
        out_path.write_bytes(self.pdf.build())


# --------------------------------------------------------------------------
# Figure 1: the four-layer gradient
#
# Layout is a wide two-panel row over a three-column note row. The earlier
# portrait layout of this figure was 520 x 561 pt, which exceeds
# \topfraction in ACM sigconf and therefore could never be placed as a
# full-width top float. The target here is roughly 520 x 300 pt.
# --------------------------------------------------------------------------

GRADIENT_LABELS = ("U2 exists", "U2 reproduces", "L7 consistent",
                   "U4 SUPPORTED")


def draw_gradient_bars(page: Page, d: dict, x: float, width: float) -> float:
    """Panel (a): the four categorical layer verdicts. Returns the y reached."""
    stages = [
        (GRADIENT_LABELS[i], value, colour) for i, (value, colour) in enumerate(
            ((d["u2_exists"], EXISTS),
             (d["u2_reproduces"], REPRO),
             (d["internal_consistency"], INTERNAL),
             (d["verdicts"]["SUPPORTED"], VERDICT)))
    ]
    label_size, value_size, tick_size = 7.0, 6.5, 6.5
    label_w = max(text_width(s[0], label_size) for s in stages) + 8.0
    value_w = max(text_width(f"{s[1]}/13", value_size, True) for s in stages) + 8.0
    plot_w = width - label_w - value_w
    if plot_w < 50.0:
        raise SystemExit(f"figure 1 panel (a) plot area too narrow: {plot_w:.1f}")
    axis_max, ticks = 14.0, [0, 2, 4, 6, 8, 10, 12, 14]
    bar_h, bar_gap = 13.0, 5.0
    block_h = len(stages) * (bar_h + bar_gap) - bar_gap
    bar_top = page.y

    axis_y = bar_top - block_h - 4.0
    for tick in ticks:
        tx = x + label_w + (tick / axis_max) * plot_w
        page.pdf.stroke(GRID)
        page.pdf.line_width(0.5)
        page.pdf.line(tx, axis_y, tx, bar_top)
        page.pdf.text_center(tx, axis_y - 9.5, tick_size, str(tick),
                             rgb=GREY_TEXT)
    page.pdf.stroke(RULE)
    page.pdf.line_width(0.8)
    page.pdf.line(x + label_w, axis_y, x + label_w + plot_w, axis_y)

    for index, (label, value, colour) in enumerate(stages):
        bar_y = bar_top - (index + 1) * (bar_h + bar_gap) + bar_gap
        bar_w = (value / axis_max) * plot_w
        page.pdf.text(x, bar_y + 3.6, label_size, label, rgb=BLACK)
        page.pdf.fill_rect(x + label_w, bar_y, bar_w, bar_h, colour)
        page.pdf.text(x + label_w + bar_w + 4.0, bar_y + 3.6, value_size,
                      f"{value}/13", bold=True, rgb=BLACK if value else ACCENT)
        if not value:
            # A zero bar must read as a measured zero, not an omission.
            page.pdf.stroke(ACCENT)
            page.pdf.line_width(1.3)
            page.pdf.line(x + label_w, bar_y + 0.5, x + label_w,
                          bar_y + bar_h - 0.5)

    y = axis_y - 19.0
    page.pdf.text(x + label_w, y, tick_size, "packages, n = 13", rgb=GREY_TEXT)
    return y - 10.0


def draw_claim_pool(page: Page, d: dict, x: float, width: float) -> float:
    """Panel (b): the adjudicated claim pool. Returns the y reached."""
    segs = [
        ("CLAIM-CORRECT", d["claims_correct"], CORRECT, "pct_correct"),
        ("CLAIM-CONTRADICTED", d["claims_contradicted"], CONTRADICTED,
         "pct_contradicted"),
        ("CLAIM-UNSUPPORTED", d["claims_unsupported"], UNSUPPORTED,
         "pct_unsupported"),
    ]
    label_size, bar_h = 7.0, 18.0
    label = f"{d['claims_total']} claims"
    label_w = text_width(label, label_size) + 8.0
    axis_max, ticks = 400.0, [0, 100, 200, 300, 400]
    plot_w = width - label_w
    if plot_w < 60.0:
        raise SystemExit(f"figure 1 panel (b) plot area too narrow: {plot_w:.1f}")
    bar_top = page.y

    axis_y = bar_top - bar_h - 4.0
    for tick in ticks:
        tx = x + label_w + (tick / axis_max) * plot_w
        page.pdf.stroke(GRID)
        page.pdf.line_width(0.5)
        page.pdf.line(tx, axis_y, tx, bar_top)
        page.pdf.text_center(tx, axis_y - 9.5, 6.5, str(tick), rgb=GREY_TEXT)
    page.pdf.stroke(RULE)
    page.pdf.line_width(0.8)
    page.pdf.line(x + label_w, axis_y, x + label_w + plot_w, axis_y)

    page.pdf.text(x, bar_top - bar_h + 5.6, label_size, label, rgb=BLACK)
    cursor = x + label_w
    for _, value, colour, _ in segs:
        seg_w = (value / axis_max) * plot_w
        page.pdf.fill_rect(cursor, bar_top - bar_h, seg_w, bar_h, colour)
        # Per-segment values are carried by the legend. Two of the three
        # segments are narrower than their own labels, so an in-bar value
        # label would collide with the axis.
        cursor += seg_w

    y = axis_y - 19.0
    # Legend, flowed onto new lines rather than allowed to overrun.
    swatch, gap_after, line_gap = 7.0, 12.0, 9.5
    lx, ly = x, y
    for name, value, colour, key in segs:
        text = f"{name} {value} ({d[key]:.1f}%)"
        item_w = swatch + 3.0 + text_width(text, 6.5)
        if lx > x and lx + item_w > x + width:
            lx, ly = x, ly - line_gap
        page.pdf.fill_rect(lx, ly - 0.8, swatch, 6.0, colour)
        page.pdf.text(lx + swatch + 3.0, ly, 6.5, text, rgb=BLACK)
        lx += item_w + gap_after
    if lx - gap_after > x + width:
        raise SystemExit("figure 1 legend item overruns the panel width")
    return ly - 11.0


def render_gradient(d: dict, corrections_found: list[Correction],
                    out_path: pathlib.Path) -> None:
    page = Page(
        "The artifact-to-claim gradient, and the denominators it depends on",
        f"13 scored rows over 12 distinct packages. Source: {DATASET}. Every "
        "quantity below is recomputed from the frozen row table by "
        "figures/make_figures.py, which aborts if any value disagrees.")

    gutter = 20.0
    half = (page.content_w - gutter) / 2.0
    right_x = page.LEFT + half + gutter

    page.label_at("(a)  Categorical layer verdicts, n = 13", page.LEFT, half)
    page.label_at("(b)  Adjudicated claim pool, 375 claims", right_x, half)
    page.y -= 13.0

    top = page.y
    y_a = draw_gradient_bars(page, d, page.LEFT, half)
    y_b = draw_claim_pool(page, d, right_x, half)
    page.y = min(y_a, y_b) - 8.0

    # Note row: three columns under a single rule.
    col_w = (page.content_w - 2 * 16.0) / 3.0
    page.rule()
    page.gap(6.0)
    page.label_at("Granularity conditioning", page.LEFT, col_w)
    page.label_at("Verdict vs. containment", page.LEFT + col_w + 16.0, col_w)
    page.label_at("Aggregate reconciliation", page.LEFT + 2 * (col_w + 16.0),
                  col_w)
    page.y -= 12.0

    v = d["verdicts"]
    y1 = page.column(
        f"The {d['pct_correct']:.1f}% correct rate is computed over a pool of "
        f"{d['claims_total']} claims that mixes two counting conventions. "
        f"Batches 1-2: {d['batch12_correct']}/{d['batch12_claims']} = "
        f"{d['pct_batch12']:.1f}%. Batch 3: {d['batch3_correct']}/"
        f"{d['batch3_claims']} = {d['pct_batch3']:.1f}% over four packages, "
        f"{d['batch3w_correct']}/{d['batch3w_claims']} = {d['pct_batch3w']:.1f}% "
        f"over five rows. The split is a property of the splitter, so the "
        f"pooled rate is descriptive and is not a defect rate for this corpus. "
        f"Only panel (a) is comparable across batches.",
        page.LEFT, col_w, rgb=GREY_TEXT)

    y2 = page.column(
        f"Package-level verdict: {v['SUPPORTED']} SUPPORTED, "
        f"{v['PARTIALLY']} PARTIALLY, {v['CONTRADICTED']} CONTRADICTED, of 13. "
        f"Packages containing at least one CLAIM-CONTRADICTED claim: "
        f"{d['pkg_ge1_contradicted']} of 13. The second is the stronger "
        f"statement and the more damaging one, and it holds for the package "
        f"that is SUPPORTED on every layer below its verdict. Reporting only "
        f"the first understates the finding; reporting the second as the "
        f"verdict misdescribes the adjudication.",
        page.LEFT + col_w + 16.0, col_w)

    recon = ("Two arithmetic errors in the frozen dataset's derived-metrics "
             "block, found by row-level reconciliation against the thirteen "
             "per-package rows and corrected with the rows left untouched. ")
    recon += " ".join(f"{c.label}: block recorded {c.recorded}, corrected to "
                      f"{c.corrected}." for c in corrections_found)
    recon += (f" The correction makes the gradient steeper, not flatter: "
              f"{d['internal_consistency']} of 13 rows are internally "
              f"consistent. Neither correction changes the central result: "
              f"{d['verdicts']['SUPPORTED']} of 13 packages are SUPPORTED and "
              f"{d['pkg_ge1_contradicted']} of 13 contain a contradicted "
              f"claim before and after. Section 4.4 gives both rounds.")
    y3 = page.column(recon, page.LEFT + 2 * (col_w + 16.0), col_w, rgb=BLACK)

    page.y = min(y1, y2, y3) - 6.0
    page.finish(out_path)




# --------------------------------------------------------------------------
# Figure 2: the three failure classes
# --------------------------------------------------------------------------

def render_classes(classes: list[dict], out_path: pathlib.Path) -> None:
    page = Page(
        "Three failure classes, read across the four units of analysis",
        f"Classification and exemplars transcribed from {DATASET}, section "
        "'The three counterexample classes', and from the cross-package "
        "findings in E1-AGGREGATE.md. A cell is a structural property of the "
        "class definition, not a count: it records whether the class is "
        "detectable at that unit at all.")

    # Column widths are measured from the text each column must hold.
    name_size, mech_size, tag_size = 8.5, 7.5, 7.5
    name_w = max(text_width(c["class_name"], name_size, True) for c in classes)
    name_w += 14.0
    unit_w = max(text_width(t, tag_size, True) for t in
                 ("U1", "U2", "U3", "U4")) + 18.0
    cell_gap = 18.0
    mech_x = page.LEFT + name_w + 4 * unit_w + cell_gap
    mech_w = page.LEFT + page.content_w - mech_x
    if mech_w < 60.0:
        raise SystemExit(f"figure 2 mechanism column too narrow: {mech_w:.1f}")

    head_y = page.y - 6.0
    page.pdf.text(page.LEFT, head_y, tag_size, "failure class and corpus "
                  "exemplar", bold=True, rgb=BLACK)
    keys = ["u1_contradiction", "u2_reproduction", "u3_relation_failure",
            "u4_package_failure"]
    for index, key in enumerate(keys):
        cx = page.LEFT + name_w + index * unit_w + unit_w / 2.0
        page.pdf.text_center(cx, head_y, tag_size, key[:2].upper(), bold=True,
                             rgb=BLACK)
    page.pdf.text(mech_x, head_y, tag_size,
                  "mechanism the method must be able to falsify", bold=True,
                  rgb=BLACK)
    page.y = head_y - 6.0
    page.rule(colour=RULE, width=0.7)
    page.gap(8.0)

    for row in classes:
        top = page.y
        page.pdf.text(page.LEFT, top, name_size, row["class_name"], bold=True,
                      rgb=BLACK)
        y = top - 11.0
        for line in wrap(row["exemplar"], 7.0, name_w - 4.0):
            page.pdf.text(page.LEFT, y, 7.0, line, rgb=GREY_TEXT)
            y -= 9.0

        for index, key in enumerate(keys):
            cx = page.LEFT + name_w + index * unit_w + unit_w / 2.0
            value = row[key]
            if value == "YES":
                page.pdf.fill_rect(cx - unit_w / 2.0 + 2.0, top - 3.0,
                                   unit_w - 4.0, 11.0, ACCENT)
                page.pdf.text_center(cx, top, tag_size, "YES", bold=True,
                                     rgb=WHITE)
            else:
                page.pdf.stroke_rect(cx - unit_w / 2.0 + 2.0, top - 3.0,
                                     unit_w - 4.0, 11.0, GRID, 0.8)
                page.pdf.text_center(cx, top, tag_size, "NO", rgb=GREY_TEXT)

        lines = wrap(row["mechanism"], mech_size, mech_w)
        block_bottom = top
        for offset, line in enumerate(lines):
            ly = top - offset * 9.5
            page.pdf.text(mech_x, ly, mech_size, line, rgb=BLACK)
            block_bottom = ly
        page.y = min(y, block_bottom) - 14.0
        page.pdf.stroke(GRID)
        page.pdf.line_width(0.5)
        page.pdf.line(page.LEFT, page.y + 8.0,
                      page.LEFT + page.content_w, page.y + 8.0)

    page.gap(6.0)
    page.paragraph(
        "Read the four cell columns down the three rows. Class 1 is invisible "
        "at U1, U2 and U3 at once: its artifact reproduces to 1.8e-12, the "
        "most reproducible artifact in the set, and no artifact contains a "
        "different value for the asserted proposition. It is detectable only "
        "at U4, and only because the assertion's own construction is the "
        "defect.", rgb=ACCENT, bold=True)
    page.gap(2.0)
    page.paragraph(
        "Classes 2 and 3 are both invisible at U2, because reproduction is "
        "not what is wrong with them: a verifier that runs and disagrees, and "
        "an artifact that runs and implements something else, both "
        "reproduce perfectly. The two failure classes a reproduction check "
        "cannot see are precisely the two the earlier unit set did not have.")

    page.finish(out_path)


# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true",
                        help="print derived values and exit without writing "
                             "any PDF")
    args = parser.parse_args(argv)

    rows = load_rows(DATA_ROWS)
    classes = load_classes(DATA_CLASSES)
    d = derived(rows)
    problems, corrections_found = check(rows, d)

    print(f"Derived from {DATA_ROWS.name} and {DATA_CLASSES.name}")
    print(f"  source of record                 : {DATASET}")
    print(f"  rows / distinct packages        : {d['n_rows']} / 12")
    print()
    print("  U1 claim pool")
    print(f"    adjudicated                    : {d['claims_total']}")
    print(f"    CLAIM-CORRECT                  : {d['claims_correct']} "
          f"({d['pct_correct']:.1f}%)")
    print(f"    CLAIM-CONTRADICTED             : {d['claims_contradicted']} "
          f"({d['pct_contradicted']:.1f}%)")
    print(f"    CLAIM-UNSUPPORTED              : {d['claims_unsupported']} "
          f"({d['pct_unsupported']:.1f}%)")
    print()
    print("  U2 artifact")
    print(f"    exists                         : {d['u2_exists']}/13")
    print(f"    reproduces                     : {d['u2_reproduces']}/13")
    print()
    print("  U3 relation")
    print(f"    broken by contradiction        : {d['u3_broken']}/13")
    print(f"    absent                         : {d['u3_absent']}/13")
    print()
    print("  U4 package")
    print(f"    internal consistency           : {d['internal_consistency']}/13")
    print(f"    verdict SUPPORTED              : {d['verdicts']['SUPPORTED']}/13")
    print(f"    verdict PARTIALLY              : "
          f"{d['verdicts']['PARTIALLY']}/13")
    print(f"    verdict CONTRADICTED           : "
          f"{d['verdicts']['CONTRADICTED']}/13")
    print(f"    contains >=1 contradicted claim: {d['pkg_ge1_contradicted']}/13")
    print(f"    contains >=1 unsupported claim : {d['pkg_ge1_unsupported']}/13")
    print()
    print(f"  gradient (exists, reproduces, internal, SUPPORTED): "
          f"{d['gradient'][0]}/13 -> {d['gradient'][1]}/13 -> "
          f"{d['gradient'][2]}/13 -> {d['gradient'][3]}/13")
    print()
    print("  cross-layer disagreement: U2 reproduction against U4 verdict")
    print(f"    reproduced     (n={d['repro_n']:2d})                 : "
          f"{d['repro_verdicts']['SUPPORTED']} SUPPORTED, "
          f"{d['repro_verdicts']['PARTIALLY']} PARTIALLY, "
          f"{d['repro_verdicts']['CONTRADICTED']} CONTRADICTED")
    print(f"    not reproduced (n={d['norepro_n']:2d})                 : "
          f"{d['norepro_verdicts']['SUPPORTED']} SUPPORTED, "
          f"{d['norepro_verdicts']['PARTIALLY']} PARTIALLY, "
          f"{d['norepro_verdicts']['CONTRADICTED']} CONTRADICTED")
    print(f"    rows that both reproduce and are SUPPORTED: "
          f"{d['repro_and_supported']}")
    print()
    print("  cross-batch granularity record")
    print(f"    batches 1-2 (8 rows)           : {d['batch12_correct']}/"
          f"{d['batch12_claims']} = {d['pct_batch12']:.1f}%")
    print(f"    batch 3 (4 packages)           : {d['batch3_correct']}/"
          f"{d['batch3_claims']} = {d['pct_batch3']:.1f}%")
    print(f"    batch 3 (5 scored rows)        : {d['batch3w_correct']}/"
          f"{d['batch3w_claims']} = {d['pct_batch3w']:.1f}%")
    print()
    print("  failure classes")
    for row in classes:
        print(f"    {row['class_id']}. {row['class_name']} "
              f"-> {row['exemplar']}")

    print("\n  arithmetic errors in the frozen dataset's aggregate layer "
          "(logged, not quietly amended)")
    for correction in corrections_found:
        print(f"    - {correction}")
        print(f"      {correction.note}")

    if problems:
        print("\nCHECK FAILURES:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print("\nAll derivation checks passed.")

    if args.verify:
        return 0

    render_gradient(d, corrections_found, OUT_GRADIENT)
    render_classes(classes, OUT_CLASSES)
    print(f"\nWrote {OUT_GRADIENT.name} ({OUT_GRADIENT.stat().st_size} bytes)")
    print(f"Wrote {OUT_CLASSES.name} ({OUT_CLASSES.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
