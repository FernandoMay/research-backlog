#!/bin/sh
# Build main.pdf. Discoverable toolchain, three passes, error gate.
#
# The previous README hard-coded /Library/TeX/texbin/pdflatex, a macOS-specific
# absolute path that exists on no other machine, in the same instruction block
# that claimed the scripts were runnable by someone who is not the author. This
# script looks for pdflatex on PATH first, then in the usual TeX Live and
# MacTeX install locations, and if it finds none it says so and names what to
# install instead of failing with "command not found" three lines later.
#
# Usage:
#     ./build.sh          # three passes, abort on any error
#     ./build.sh --check  # same, and also print the page count and box census
#
# Exit status is 0 only when all three passes succeed and no pass reports an
# undefined reference or an overfull box.

set -e

cd "$(dirname "$0")"

PASSES=3

find_pdflatex() {
    # 1. On PATH. This is the case on every correctly configured TeX install,
    #    Linux, macOS with TeX Live's bin symlinked, CI, containers.
    if command -v pdflatex >/dev/null 2>&1; then
        command -v pdflatex
        return 0
    fi
    # 2. Conventional install locations, most specific first.
    for candidate in \
        /Library/TeX/texbin/pdflatex \
        /usr/local/texlive/*/bin/*/pdflatex \
        /opt/homebrew/bin/pdflatex \
        /usr/local/bin/pdflatex \
        /usr/bin/pdflatex
    do
        if [ -x "$candidate" ]; then
            echo "$candidate"
            return 0
        fi
    done
    return 1
}

PDFLATEX=$(find_pdflatex) || {
    cat >&2 <<'EOF'
build.sh: cannot find pdflatex.

Looked on PATH, then in:
  /Library/TeX/texbin/pdflatex
  /usr/local/texlive/*/bin/*/pdflatex
  /opt/homebrew/bin/pdflatex
  /usr/local/bin/pdflatex
  /usr/bin/pdflatex

Install one of:
  Debian/Ubuntu   apt-get install texlive-latex-recommended texlive-fonts-recommended
  Fedora/RHEL     dnf install texlive-scheme-medium
  macOS           install MacTeX from https://www.tug.org/mactex/, or the
                  smaller BasicTeX plus the packages listed in README.md
  any platform    a TeX Live or MiKTeX installation, then put its bin
                  directory on PATH

Everything else in this paper's build path is standard-library Python 3 with
nothing to install. Only the manuscript build needs a LaTeX toolchain, and only
if you want to rebuild the PDF rather than read the committed one.
EOF
    exit 127
}

echo "pdflatex: $PDFLATEX"
"$PDFLATEX" --version | head -1

# Three passes are needed for \ref and \cite to settle. Each pass's log is kept
# so a failure can be read rather than guessed at.
i=1
while [ "$i" -le "$PASSES" ]; do
    echo "--- pass $i of $PASSES ---"
    if ! "$PDFLATEX" -interaction=nonstopmode -halt-on-error main.tex \
        >"build-pass${i}.log" 2>&1; then
        echo "build.sh: pass $i failed. Tail of build-pass${i}.log:" >&2
        tail -30 "build-pass${i}.log" >&2
        exit 1
    fi
    i=$((i + 1))
done

# Error gate. The three passes are not enough on their own: a LaTeX run can
# complete with a non-zero-worthy condition logged rather than raised, which is
# how an undefined reference or a figure that never got placed gets through.
LAST="build-pass${PASSES}.log"

if grep -q '^!' "$LAST"; then
    echo "build.sh: LaTeX errors in $LAST:" >&2
    grep -A3 '^!' "$LAST" >&2
    exit 1
fi
if grep -q 'LaTeX Warning: Reference' "$LAST"; then
    echo "build.sh: undefined references in $LAST:" >&2
    grep 'LaTeX Warning: Reference' "$LAST" >&2
    exit 1
fi
if grep -q 'LaTeX Warning: Citation' "$LAST"; then
    echo "build.sh: undefined citations in $LAST:" >&2
    grep 'LaTeX Warning: Citation' "$LAST" >&2
    exit 1
fi
if grep -q 'Overfull \\hbox' "$LAST"; then
    echo "build.sh: overfull boxes in $LAST:" >&2
    grep 'Overfull \\hbox' "$LAST" >&2
    exit 1
fi

PAGES=$(sed -n 's/.*Output written on main.pdf (\([0-9]*\) pages.*/\1/p' "$LAST")
echo "build.sh: 3 passes, 0 errors, 0 undefined references,"
echo "           0 undefined citations, 0 overfull boxes, ${PAGES:-?} pages."

if [ "$1" = "--check" ]; then
    echo "--- vector figures ---"
    python3 - <<'PY'
import re, pathlib
data = pathlib.Path("main.pdf").read_bytes()
forms = len(re.findall(rb"/Subtype\s*/Form", data))
images = len(re.findall(rb"/Subtype\s*/Image", data))
dct = len(re.findall(rb"/DCTDecode", data))
print(f"  Form XObjects (vector): {forms}")
print(f"  Image XObjects:         {images}")
print(f"  DCTDecode streams:      {dct}")
if images or dct:
    raise SystemExit("build.sh: a figure was rasterised; both should be vector.")
PY
    echo "  both figures are vector PDF Form XObjects"
fi