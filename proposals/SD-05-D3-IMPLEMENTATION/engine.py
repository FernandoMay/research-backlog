"""
Risk engine under test, plus an independent reimplementation.

Two functions compute the same quantity by deliberately different routes:

    engine_score(arm, inputs)        the engine under test
    independent_score(arm, inputs)   the adjudicator's own recomputation

They are written separately on purpose. If the adjudicator reused the
engine's code, `score_delta` would be identically zero by construction and
the EXECUTION_ERROR check in the specification would be a tautology --
reproducing exactly the NON-DISCRIMINATING-FALSIFIER defect that D3 exists
to eliminate.

Scope, stated honestly: for a formula this small, two independent
implementations will agree. What that agreement is worth is catching
transcription and wiring errors between configuration and code. It does
NOT establish that either function is the intended one -- that is what the
proven-range oracle is for, and it does not share code with either path.
"""

import math
from functools import reduce

from frozen import GAMMA, WEIGHTS, THRESHOLDS


def _raw_engine(inputs):
    """Weighted sum plus the interaction term. Comprehension form."""
    u, v, i, n, p = inputs
    linear = reduce(lambda acc, k: acc + k[0] * k[1], zip(WEIGHTS, (u, v, i, n, p)), 0.0)
    return linear + GAMMA * u * v


def _raw_independent(inputs):
    """Same quantity, expanded form. Written out rather than folded."""
    u, v, i, n, p = inputs
    return (
        0.2 * u
        + 0.3 * v
        + 0.3 * i
        + 0.1 * n
        + 0.1 * p
        + 0.15 * u * v
    )


def _apply_clamp(x):
    """As implemented in the submitted prototype."""
    return min(max(x, 0.0), 1.0)


def _apply_sigmoid(x):
    """As specified in the design prose."""
    return 1.0 / (1.0 + math.exp(-x))


_ARMS = {"CLAMP": _apply_clamp, "SIGMOID": _apply_sigmoid}


def engine_score(arm, inputs):
    """Score as returned by the engine under test."""
    if arm not in _ARMS:
        raise ValueError(f"unknown arm: {arm}")
    return _ARMS[arm](_raw_engine(inputs))


def independent_score(arm, inputs):
    """Recomputation performed outside the engine."""
    if arm not in _ARMS:
        raise ValueError(f"unknown arm: {arm}")
    return _ARMS[arm](_raw_independent(inputs))


def level_of(score):
    """Map a score to its tier using the frozen thresholds."""
    t0, t1, t2 = THRESHOLDS
    if score < t0:
        return "L0"
    if score < t1:
        return "L1"
    if score < t2:
        return "L2"
    return "L3"


def level_rank(level):
    return ("L0", "L1", "L2", "L3").index(level)


def probe_a4_boundary(arm, scorer):
    """
    A4 frontier probe.

    Bisects declared value V subject to the arm assigning L0, with impact
    declared 0 and the remaining variables held at the A1 profile. Returns
    the largest high-impact value that still escapes escalation.

    This is a frontier map, not pass/fail. It is not a counterexample on its
    own -- the adjudication of every probed point still runs through the
    policy check.
    """
    u, _, _, n, p = 0.20, None, None, 0.10, 0.20

    def l0(value):
        return level_of(scorer(arm, (u, value, 0.0, n, p))) == "L0"

    if not l0(0.0):
        return None  # the arm assigns no L0 at all -- the frontier is empty

    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if l0(mid):
            lo = mid
        else:
            hi = mid
    return lo