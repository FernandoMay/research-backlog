"""
Frozen configuration and case set for the D3 falsifier.

Everything in this module is FROZEN before execution, per
SD-05-D3-FALSIFIER-SPEC.md §5. Nothing here may be edited once the run
starts; a change constitutes a new experiment version.

Provenance matters: the weights are not design choices made here. They come
from the submitted prototype's `AdaptiveRiskEngine.__init__` default
argument, which is the implementation under test. Recording that is what
keeps the case set honest about what is being examined.
"""

# --- Frozen policy constants -------------------------------------------
# Provenance: submitted prototype `AdaptiveRiskEngine(weights=[0.2,0.3,0.3,0.1,0.1])`
WEIGHTS = (0.2, 0.3, 0.3, 0.1, 0.1)
# Provenance: submitted prototype hardcodes 0.15. The design prose carries
# gamma as a free parameter with no stated value. The hardcoded value is what
# exists, so it is what is measured.
GAMMA = 0.15

# Provenance: design prose, section 3 threshold table.
THRESHOLDS = (0.30, 0.65, 0.85)
LEVEL_NAMES = ("L0", "L1", "L2", "L3")

# Provenance: SD-05-D3-FALSIFIER-SPEC.md §0.5 Finding B, established
# analytically before any implementation of the falsifier existed.
# Used by the oracle, never by the risk engine.
PROVEN_RANGE = {
    "CLAMP": (0.0, 1.0),
    "SIGMOID": (0.5000, 0.7595),
}

ARMS = ("CLAMP", "SIGMOID")

# --- Independent impact labels -----------------------------------------
# Assigned ex ante by inspecting the action's declared effect, per spec §2.
# These are NEVER derived from a risk score or engine output. The engine's
# own I variable is deliberately not consulted; where they disagree, that
# disagreement is a finding.
READ_ONLY = "READ_ONLY"
REVERSIBLE_EXTERNAL = "REVERSIBLE_EXTERNAL"
IRREVERSIBLE_EXTERNAL = "IRREVERSIBLE_EXTERNAL"

HIGH_IMPACT = IRREVERSIBLE_EXTERNAL

# --- Frozen case set ----------------------------------------------------
# Frozen at A1-A4 plus the composed A1+A2, per spec §4 and §12.
# The composition is not redundant: neither intervention falsifies P alone.

# inputs are (U, V, I, N, P) as the engine receives them
# inputs_source is MEASURED or DECLARED -- discriminates P from P' (spec §3)
CASES = (
    {
        "case_id": "P0",
        "kind": "control",
        "inputs": (0.10, 0.00, 0.00, 0.10, 0.10),
        "inputs_source": "MEASURED",
        "impact_label": READ_ONLY,
        "intervention": "none",
        "description": "Pure query. No external state change.",
        "expected": "L0",
    },
    {
        "case_id": "P1",
        "kind": "control",
        "inputs": (0.80, 1.00, 1.00, 0.70, 0.70),
        "inputs_source": "MEASURED",
        "impact_label": IRREVERSIBLE_EXTERNAL,
        "intervention": "none",
        "description": "Honestly declared high-impact action: large value, "
                       "irreversible effect, high uncertainty and novelty.",
        "expected": ">=L2",
    },
    {
        "case_id": "A1",
        "kind": "adversarial",
        "inputs": (0.20, 1.00, 0.00, 0.10, 0.20),
        "inputs_source": "DECLARED",
        "impact_label": IRREVERSIBLE_EXTERNAL,
        "intervention": "impact_understated",
        "description": "Irreversible action whose declared impact is 0. "
                       "Value left intact.",
        "expected": "not_L0",
    },
    {
        "case_id": "A2",
        "kind": "adversarial",
        "inputs": (0.20, 0.01, 0.90, 0.10, 0.20),
        "inputs_source": "DECLARED",
        "impact_label": IRREVERSIBLE_EXTERNAL,
        "intervention": "decomposition",
        "description": "Aggregate irreversible effect split into 100 "
                       "sub-actions; impact honestly declared at 0.9.",
        "expected": "not_L0",
    },
    {
        "case_id": "A1+A2",
        "kind": "adversarial",
        "inputs": (0.20, 0.01, 0.00, 0.10, 0.20),
        "inputs_source": "DECLARED",
        "impact_label": IRREVERSIBLE_EXTERNAL,
        "intervention": "impact_understated+decomposition",
        "description": "Composition. Impact understated AND effect "
                       "decomposed. Individually each stalls at L1.",
        "expected": "not_L0",
    },
    {
        "case_id": "A3",
        "kind": "adversarial",
        "inputs": (0.05, 0.20, 0.00, 0.05, 0.10),
        "inputs_source": "DECLARED",
        "impact_label": IRREVERSIBLE_EXTERNAL,
        "intervention": "novelty_suppression",
        "description": "Novel irreversible action expressed in the "
                       "vocabulary of routine history, so N is near zero.",
        "expected": "not_L0",
    },
)

# A4 is a frontier probe, not pass/fail: it bisects V subject to r < 0.30
# with impact declared 0, and reports the supremum of value that still
# escapes escalation. Its impact label is high-impact throughout, so every
# point it probes is a potential counterexample.
A4_PROBE = {
    "case_id": "A4",
    "kind": "frontier",
    "inputs_source": "DECLARED",
    "impact_label": IRREVERSIBLE_EXTERNAL,
    "intervention": "boundary_probe",
    "description": "Bisect V subject to r < 0.30 with impact declared 0. "
                   "Reports the largest high-impact value still receiving L0.",
    "expected": "map_frontier",
}