#!/usr/bin/env python3
"""Generate the lifecycle fee figure for the Soroban escrow cost-asymmetry paper.

The script is dependency-free: it emits vector PDF using only the Python
standard library, so the figure can be regenerated on any machine with a
Python 3 interpreter and no network access.

Geometry is computed from ``figures/data/lifecycle_fees.csv``. Nothing in the
output is hand-placed: bar extents, axis ticks and annotation strings are all
derived from the CSV values.

Usage
-----
    python3 make_figures.py             # write lifecycle_fees.pdf + report
    python3 make_figures.py --verify    # print derived values only, no output

Provenance of the CSV: every row is a per-transaction fee recorded in
``E2E-PROOF.md`` (lines 70-95) of the audited repository, measured on Stellar
testnet against contract
``CB7I2GURQDV4Q7YAT2PZAG3ZNFQJ37GI6MWZ4P3W7SUCJZPSHP2G6L6J``.
One observation per step. There is no replication, so every quantity derived
here is a description of a single lifecycle, not a distribution.
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import sys

# --------------------------------------------------------------------------
# Fixed data, transcribed from the primary artifact. Kept in one place so the
# derivation checks below can prove the CSV and the manuscript agree.
# --------------------------------------------------------------------------

CONTRACT_ID = "CB7I2GURQDV4Q7YAT2PZAG3ZNFQJ37GI6MWZ4P3W7SUCJZPSHP2G6L6J"
PROVENANCE = "E2E-PROOF.md:70-95, Stellar testnet, single observed lifecycle (n=1)"

# Fee constants transcribed from the contract source.
MAX_FEE_BPS = 1000        # lib.rs:11
DEFAULT_FEE_BPS = 80      # tests.rs:12

HERE = pathlib.Path(__file__).resolve().parent
DATA_CSV = HERE / "data" / "lifecycle_fees.csv"
OUTPUT_PDF = HERE / "lifecycle_fees.pdf"


# --------------------------------------------------------------------------
# Derivation helpers
# --------------------------------------------------------------------------

def load_rows(csv_path: pathlib.Path) -> list[dict]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"no rows in {csv_path}")
    for row in rows:
        row["fee_stroops"] = int(row["fee_stroops"])
        row["ledger"] = int(row["ledger"])
        row["contract_op"] = row["contract_op"].strip().lower() == "true"
    return rows


def by_step(rows: list[dict], step: str) -> dict:
    for row in rows:
        if row["step"] == step:
            return row
    raise KeyError(step)


def truncating_fee(amount: int, fee_bps: int) -> int:
    """Fee arithmetic as implemented: (amount * fee_bps) // 10_000, truncating.

    Mirrors lib.rs:199 and lib.rs:226.
    """
    return (amount * fee_bps) // 10_000


def zero_fee_threshold(fee_bps: int) -> int:
    """Largest amount whose fee truncates to zero.

    Solves amount * fee_bps < 10_000, i.e. amount <= (10_000 - 1) // fee_bps.
    """
    return (10_000 - 1) // fee_bps


def derived(rows: list[dict]) -> dict:
    fund = by_step(rows, "S6")["fee_stroops"]
    release = by_step(rows, "S7")["fee_stroops"]
    create = by_step(rows, "S5")["fee_stroops"]
    fees = [row["fee_stroops"] for row in rows]
    return {
        "n_steps": len(rows),
        "fund": fund,
        "release": release,
        "create": create,
        "ratio_fund_over_release": fund / release,
        "delta_fund_minus_release": fund - release,
        "ratio_fund_over_create": fund / create,
        "lifecycle_fee_sum": sum(fees),
        "fund_share_of_sum": fund / sum(fees),
        "span_max_over_min": max(fees) / min(fees),
        "max_step": max(rows, key=lambda r: r["fee_stroops"])["step"],
        "min_step": min(rows, key=lambda r: r["fee_stroops"])["step"],
        "zero_fee_threshold_default_bps": zero_fee_threshold(DEFAULT_FEE_BPS),
        "fee_at_1000_units": truncating_fee(1000, DEFAULT_FEE_BPS),
        "fee_at_3000_units": truncating_fee(3000, DEFAULT_FEE_BPS),
        "fee_at_1_unit": truncating_fee(1, DEFAULT_FEE_BPS),
        "ledger_first": min(row["ledger"] for row in rows),
        "ledger_last": max(row["ledger"] for row in rows),
    }


def check(rows: list[dict], d: dict) -> list[str]:
    """Assert the derived values against the primary artifacts. Failures abort."""
    problems: list[str] = []

    def expect(label: str, actual, required) -> None:
        if actual != required:
            problems.append(f"{label}: derived {actual!r} != artifact {required!r}")

    expect("fund_escrow fee", d["fund"], 366938)
    expect("release_funds fee", d["release"], 17791)
    expect("create_escrow fee", d["create"], 164691)
    expect("lifecycle fee sum", d["lifecycle_fee_sum"], 770179)
    expect("n steps", d["n_steps"], 7)
    expect("max step", d["max_step"], "S6")
    expect("min step", d["min_step"], "S4")
    expect("ledger first", d["ledger_first"], 4869181)
    expect("ledger last", d["ledger_last"], 4869223)
    expect("fee at 1000 units", d["fee_at_1000_units"], 8)
    expect("fee at 3000 units", d["fee_at_3000_units"], 24)
    expect("fee at 1 unit", d["fee_at_1_unit"], 0)
    expect("zero-fee threshold at 80 bps", d["zero_fee_threshold_default_bps"], 124)
    expect("escrow op count", sum(1 for r in rows if r["contract_op"]), 3)

    # Rounding the two headline ratios must reproduce the manuscript values.
    if round(d["ratio_fund_over_release"], 1) != 20.6:
        problems.append("fund/release ratio does not round to 20.6")
    if round(d["span_max_over_min"], 1) != 40.1:
        problems.append("max/min spread does not round to 40.1")
    if round(100 * d["fund_share_of_sum"], 1) != 47.6:
        problems.append("fund share does not round to 47.6 percent")

    # The 10% cap boundary stated in the manuscript: at the cap rate the fee on
    # 1000 base units is 100 (10% of the amount), and the cap has no minimum.
    if truncating_fee(1000, MAX_FEE_BPS) != 100:
        problems.append("1000 bps cap arithmetic unexpected")
    if truncating_fee(1, MAX_FEE_BPS) != 0:
        problems.append("no minimum fee expected at 1000 bps on 1 base unit")

    return problems


# --------------------------------------------------------------------------
# Minimal PDF writer (base-14 fonts, no external dependency)
# --------------------------------------------------------------------------

class PDF:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self.ops: list[str] = []

    # -- graphics state ---------------------------------------------------
    def fill(self, rgb: tuple[float, float, float]) -> None:
        self.ops.append(f"{rgb[0]:.4f} {rgb[1]:.4f} {rgb[2]:.4f} rg")

    def stroke(self, rgb: tuple[float, float, float]) -> None:
        self.ops.append(f"{rgb[0]:.4f} {rgb[1]:.4f} {rgb[2]:.4f} RG")

    def line_width(self, width: float) -> None:
        self.ops.append(f"{width:.2f} w")

    def rect(self, x: float, y: float, w: float, h: float) -> None:
        self.ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re")

    def line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        self.ops.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def fill_rect(self, x: float, y: float, w: float, h: float,
                  rgb: tuple[float, float, float]) -> None:
        self.fill(rgb)
        self.rect(x, y, w, h)
        self.ops.append("f")

    def translate_all(self, dy: float) -> None:
        """Shift every drawing operation vertically, once, at the end."""
        if dy:
            self.ops.insert(0, "q")
            self.ops.insert(1, f"1 0 0 1 0 {dy:.2f} cm")
            self.ops.append("Q")

    def stroke_rect(self, x: float, y: float, w: float, h: float,
                    rgb: tuple[float, float, float], width: float = 0.6) -> None:
        self.stroke(rgb)
        self.line_width(width)
        self.rect(x, y, w, h)
        self.ops.append("S")

    # -- text -------------------------------------------------------------
    @staticmethod
    def _escape(text: str) -> str:
        return (text.replace("\\", r"\\")
                    .replace("(", r"\(")
                    .replace(")", r"\)"))

    def text(self, x: float, y: float, size: float, text: str,
             bold: bool = False,
             rgb: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:
        self.fill(rgb)
        self.ops.append("BT")
        self.ops.append(f"/{'F2' if bold else 'F1'} {size:.2f} Tf")
        self.ops.append(f"{x:.2f} {y:.2f} Td")
        self.ops.append(f"({self._escape(text)}) Tj")
        self.ops.append("ET")

    def text_right(self, x: float, y: float, size: float, text: str,
                   bold: bool = False,
                   rgb: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:
        """Approximate right alignment using a 0.5 em width estimate."""
        width = len(text) * size * 0.5
        self.text(x - width, y, size, text, bold=bold, rgb=rgb)

    def text_center(self, x: float, y: float, size: float, text: str,
                    bold: bool = False,
                    rgb: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:
        """Approximate centering using a 0.5 em width estimate."""
        width = len(text) * size * 0.5
        self.text(x - width / 2.0, y, size, text, bold=bold, rgb=rgb)

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


# --------------------------------------------------------------------------
# Figure layout
# --------------------------------------------------------------------------

BLACK = (0.08, 0.08, 0.08)
GREY_TEXT = (0.35, 0.35, 0.35)
GRID = (0.87, 0.87, 0.87)
ESCROW_FILL = (0.16, 0.36, 0.60)
SETUP_FILL = (0.62, 0.68, 0.74)
HILITE = (0.72, 0.24, 0.18)
BAR_H = 15.0
BAR_GAP = 9.0
AXIS_MAX = 400_000.0
TICKS = [0, 100_000, 200_000, 300_000, 400_000]


def nice_num(value: int) -> str:
    return f"{value:,}"


def draw_bar_panel(pdf: PDF, rows: list[dict], x0: float, y_top: float,
                   width: float, title: str) -> float:
    """Draw one horizontal bar panel. Returns the y of its axis label baseline."""
    plot_w = width - 108.0

    pdf.text(x0, y_top + 24.0, 10.0, title, bold=True, rgb=BLACK)

    n = len(rows)
    block_h = n * (BAR_H + BAR_GAP)

    # Grid and x tick labels, drawn under the bars.
    axis_y = y_top - block_h - 6.0
    for tick in TICKS:
        tx = x0 + 108.0 + (tick / AXIS_MAX) * plot_w
        pdf.stroke(GRID)
        pdf.line_width(0.5)
        pdf.line(tx, axis_y, tx, y_top - 2.0)
        pdf.text_center(tx, axis_y - 13.0, 7.5, nice_num(tick), rgb=GREY_TEXT)
    pdf.stroke(GREY_TEXT)
    pdf.line_width(0.7)
    pdf.line(x0 + 108.0, axis_y, x0 + 108.0 + plot_w, axis_y)

    for index, row in enumerate(rows):
        bar_y = y_top - (index + 1) * (BAR_H + BAR_GAP) + BAR_GAP
        fee = row["fee_stroops"]
        bar_w = (fee / AXIS_MAX) * plot_w
        colour = ESCROW_FILL if row["contract_op"] else SETUP_FILL

        label = f"{row['step']}  {row['operation']}"
        pdf.text(x0, bar_y + 4.6, 8.0, label,
                 bold=row["contract_op"], rgb=BLACK if row["contract_op"] else GREY_TEXT)
        pdf.fill_rect(x0 + 108.0, bar_y, bar_w, BAR_H, colour)
        pdf.text(x0 + 108.0 + bar_w + 5.0, bar_y + 4.6, 8.0,
                 f"{nice_num(fee)}", bold=row["contract_op"], rgb=BLACK)

    label_y = axis_y - 25.0
    pdf.text(x0 + 108.0, label_y, 7.5,
             "network fee (stroops, 1e-8 XLM units)", rgb=GREY_TEXT)
    return label_y


def render(rows: list[dict], d: dict, out_path: pathlib.Path) -> None:
    # Page width is fixed. Content is laid out downwards from a virtual top,
    # then the whole drawing is translated so the MediaBox is exactly the size
    # of the content. This keeps the layout from overflowing or leaving a dead
    # band at the bottom, and it is why the origin is not simply 0.
    width = 700.0
    left = 40.0
    margin = 28.0
    headroom = 12.0  # room above the 12pt title for its ascender
    content_w = width - 2 * left
    pdf = PDF(width, 800.0)  # virtual canvas; real height computed below

    top_used = pdf.height - margin - headroom
    cursor = top_used
    pdf.text(left, cursor, 12.0,
             "Soroban escrow lifecycle fees on Stellar testnet", bold=True)
    cursor -= 16.0

    subtitle = (
        f"Contract {CONTRACT_ID}",
        f"Single observed lifecycle, n=1 per step. Source: {PROVENANCE}.",
        "Ledger sequence numbers are ordinal, not timestamps. These data "
        "contain no wall-clock timing, so no duration is claimed here.",
    )
    for index, line in enumerate(subtitle):
        pdf.text(left, cursor, 8.0, line,
                 rgb=BLACK if index < len(subtitle) - 1 else GREY_TEXT)
        cursor -= 11.0

    cursor -= 12.0
    cursor = draw_bar_panel(pdf, rows, left, cursor, content_w,
                            "(a) All seven recorded lifecycle steps")
    cursor -= 40.0
    cursor = draw_bar_panel(pdf, [r for r in rows if r["contract_op"]],
                            left, cursor, content_w,
                            "(b) Escrow operations only (setup steps excluded)")
    cursor -= 24.0

    pdf.stroke(GRID)
    pdf.line_width(0.6)
    pdf.line(left, cursor + 8.0, left + content_w, cursor + 8.0)
    cursor -= 4.0

    pdf.text(left, cursor, 8.5,
             f"fund_escrow / release_funds = {nice_num(d['fund'])} / "
             f"{nice_num(d['release'])} = {d['ratio_fund_over_release']:.1f}x",
             bold=True, rgb=HILITE)
    cursor -= 11.0
    pdf.text(left, cursor, 7.5,
             f"Escrow operations account for {100 * d['fund_share_of_sum']:.1f}% "
             f"of the {nice_num(d['lifecycle_fee_sum'])} stroop total of this "
             "lifecycle; fund_escrow alone is the largest single item.", rgb=BLACK)
    cursor -= 15.0

    # Legend, drawn from the same colours used above.
    lx = left
    for colour, text in ((ESCROW_FILL, "escrow contract operation"),
                         (SETUP_FILL, "bootstrap / onboarding step")):
        pdf.fill_rect(lx, cursor - 1.0, 9.0, 7.0, colour)
        pdf.text(lx + 14.0, cursor, 7.5, text, rgb=GREY_TEXT)
        lx += 26.0 + len(text) * 3.6
    cursor -= 4.0

    # Size the page to the content: measure the span actually drawn from the
    # virtual top, then shift the drawing down so it starts at the bottom
    # margin. The offset is negative because layout ran downward from the top.
    bottom_used = cursor
    pdf.translate_all(margin - bottom_used)
    pdf.height = (top_used - bottom_used) + 2 * margin + headroom
    out_path.write_bytes(pdf.build())


# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true",
                        help="print derived values and exit without writing a PDF")
    args = parser.parse_args(argv)

    rows = load_rows(DATA_CSV)
    d = derived(rows)
    problems = check(rows, d)

    print("Derived from figures/data/lifecycle_fees.csv")
    print(f"  steps                          : {d['n_steps']}")
    print(f"  create_escrow                  : {nice_num(d['create'])} stroops")
    print(f"  fund_escrow                    : {nice_num(d['fund'])} stroops")
    print(f"  release_funds                  : {nice_num(d['release'])} stroops")
    print(f"  fund / release                 : {d['ratio_fund_over_release']:.4f} "
          f"-> {round(d['ratio_fund_over_release'], 1)}x")
    print(f"  fund - release                 : {nice_num(d['delta_fund_minus_release'])} stroops")
    print(f"  fund / create                  : {d['ratio_fund_over_create']:.4f}")
    print(f"  lifecycle fee sum (n=1)        : {nice_num(d['lifecycle_fee_sum'])} stroops")
    print(f"  fund share of that sum         : {100 * d['fund_share_of_sum']:.4f}%")
    print(f"  max / min across steps         : {d['span_max_over_min']:.4f} "
          f"({d['max_step']} / {d['min_step']})")
    print(f"  ledger span (ordinal)          : {d['ledger_first']} -> {d['ledger_last']}")
    print(f"  fee(1000, 80bps)               : {d['fee_at_1000_units']}")
    print(f"  fee(3000, 80bps)               : {d['fee_at_3000_units']}")
    print(f"  fee(1, 80bps)                  : {d['fee_at_1_unit']}")
    print(f"  largest zero-fee amount, 80bps : {d['zero_fee_threshold_default_bps']} base units")

    if problems:
        print("\nCHECK FAILURES:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print("\nAll derivation checks passed.")

    if args.verify:
        return 0

    render(rows, d, OUTPUT_PDF)
    print(f"Wrote {OUTPUT_PDF} ({OUTPUT_PDF.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
