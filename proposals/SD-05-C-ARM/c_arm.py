"""
Candidate C transfer function — operation 1: mechanical implementation.

Scope, strictly:
    Introduces the frozen slope k. Nothing else.

Not touched: thresholds, weights, gamma, and the semantics of U, V, I, N, P.
No condition derived from A1, A2, A1+A2 or A3 appears anywhere in this file.

Provenance of every constant is given below. All are frozen at selection
commit 41fdc4b and none is a parameter of any function here.
"""

import math

# --- Frozen from the submitted prototype, unchanged ---------------------
WEIGHTS = (0.2, 0.3, 0.3, 0.1, 0.1)
GAMMA = 0.15
# Provenance: AdaptiveRiskEngine.__init__ default and the hardcoded 0.15 in
# compute_risk. Not design choices; these are what the submission contained.

# --- Frozen domain -------------------------------------------------------
X_MIN = 0.0
X_MAX = sum(WEIGHTS) + GAMMA        # 1.15
# Provenance: all weights non-negative and all inputs in [0,1], so the
# pre-activation cannot leave [0, 1.15].

# --- The only thing this operation introduces ---------------------------
K = 6.0334
X_MID = (X_MIN + X_MAX) / 2.0       # 0.575
# Provenance: 41fdc4b. K = 2 * k_min where k_min = 3.0167 is the smallest
# slope making L3 reachable over the declared domain. The factor of two is a
# declared margin chosen at specification time.

# --- Normative, unchanged -----------------------------------------------
THRESHOLDS = (0.30, 0.65, 0.85)
# Provenance: recovered design intent, normative. NOT remapped. Candidate B
# would have moved these; candidate C does not.


def pre_activation(u, v, i, n, p):
    """Unchanged from the submitted formula. No case-dependent term added."""
    linear = (WEIGHTS[0] * u + WEIGHTS[1] * v + WEIGHTS[2] * i
              + WEIGHTS[3] * n + WEIGHTS[4] * p)
    return linear + GAMMA * u * v


def f_c(x):
    """The repaired transfer function: sigmoid with the frozen slope."""
    return 1.0 / (1.0 + math.exp(-K * (x - X_MID)))


def risk(u, v, i, n, p):
    """C's risk score. The only public entry point."""
    return f_c(pre_activation(u, v, i, n, p))


def level_of(r):
    t0, t1, t2 = THRESHOLDS
    if r < t0:
        return "L0"
    if r < t1:
        return "L1"
    if r < t2:
        return "L2"
    return "L3"


# The frozen parameters are module-level constants with no override path.
# `risk` and `f_c` accept only the five declared inputs and never a slope, a
# threshold set, or a variant selector. There is no code path from an
# execution to the value of K. Operation 2 tests that property; this module
# is written so the property can hold.