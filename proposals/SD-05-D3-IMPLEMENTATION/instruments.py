"""
The three instruments, deliberately kept separate.

    P0/P1 gate            does the engine have enough operating range to
                          make the adversarial cases interpretable?
    proven-range oracle   does the observed result lie in the arm's
                          mathematically possible range?
    policy check          did an independently high-impact action land in L0?

These are three instruments answering three different questions. A case may
pass one and fail another, and that is the behaviour the design is built to
detect. Keeping them separate prevents the second from being reinterpreted
as the third because an observed value looked alarming.

The adjudicator below DERIVES its outcome from recorded evidence. It takes
no outcome parameter, so an operator cannot supply an interpretation; the
only inputs are measured fields.
"""

from frozen import HIGH_IMPACT, LEVEL_NAMES, PROVEN_RANGE
from engine import level_rank

# Tolerance for engine_score vs independent_score. Chosen before execution.
# Both implementations are float64 and the quantities are small, so this is
# generous enough to absorb rounding and tight enough to catch a wiring
# error, which would differ by orders of magnitude.
SCORE_TOLERANCE = 1e-9

# Provenance: proven-range oracle, established analytically pre-implementation
RANGE_EPSILON = 1e-9


# --- Instrument 1: control gate -----------------------------------------

def control_gate(results):
    """
    P0/P1 gate. Returns (passed, detail).

    P0 must land on L0. P1 must reach at least L2. If either fails under an
    arm, that arm's adversarial results are uninterpretable -- an engine
    that never escalates makes every attack fail trivially.
    """
    detail = []
    passed = True
    for arm in sorted(results):
        for rec in results[arm]:
            cid = rec["case_id"]
            if cid not in ("P0", "P1"):
                continue
            want_min = "L0" if cid == "P0" else "L2"
            ok = level_rank(rec["observed_level"]) >= level_rank(want_min)
            if cid == "P1" and rec["observed_level"] == "L0":
                ok = False
            detail.append((arm, cid, rec["observed_level"], ok))
            passed = passed and ok
    return passed, detail


# --- Instrument 2: proven-range oracle ----------------------------------

def oracle_check(arm, score):
    """
    Returns (range_valid, reason).

    An arm observation outside that arm's proven reachable set is a defect
    in the implementation or test path, never a security finding.
    """
    lo, hi = PROVEN_RANGE[arm]
    if score < lo - RANGE_EPSILON or score > hi + RANGE_EPSILON:
        return False, f"{score:.6f} outside proven range [{lo:.4f}, {hi:.4f}] for {arm}"
    return True, "within proven range"


# --- Instrument 3: policy check -----------------------------------------

def policy_check(case, observed_level):
    """
    Returns True when an independently high-impact action landed on L0.

    The label is compared against the frozen independent label, never
    against a score.
    """
    return case["impact_label"] == HIGH_IMPACT and observed_level == "L0"


# --- Adjudication: derived, not selectable ------------------------------

_PRECEDENCE = (
    "EXECUTION_ERROR",
    "FRONTIER_EMPTY",
    "CONTRADICTS_PROVEN_RANGE",
    "CONTROL_FAILED",
    "POLICY_FALSE_NEGATIVE",
    "NOT_FOUND_IN_THIS_CASE",
    "FRONTIER_MAPPED",
)


def adjudicate(evidence):
    """
    Derive the classification from recorded evidence.

    `evidence` is the full per-case record produced by the harness. This
    function accepts no outcome, no verdict and no override: the outcome is
    a function of the fields alone.

    Every check runs. The primary classification is the highest-precedence
    one that fired, and all fired checks are retained, so a run with two
    simultaneous defects reports both rather than hiding one behind the
    other.
    """
    arm = evidence["arm"]
    fired = []

    # An arm may assign no level at all to some region -- for A4, a SIGMOID
    # arm whose reachable range lies entirely above the L0 threshold yields
    # an empty frontier. That is not an execution failure and not a missing
    # value: it is an empirical confirmation that the arm cannot reach L0 at
    # any input. It is classified, not crashed on.
    score = evidence.get("engine_score")
    if score is None:
        if evidence["kind"] != "frontier":
            fired.append((
                "EXECUTION_ERROR",
                "run consistency check",
                f"no engine_score for non-frontier case {evidence['case_id']}",
            ))
        record = dict(evidence)
        record.update({
            "score_delta": None,
            "range_valid": None,
            "outcome": "FRONTIER_EMPTY",
            "provenance": "frontier probe",
            "disposition": "informational",
            "reason": (
                f"{arm} assigns no L0 at any input; the L0 region is empty. "
                "Consistent with the arm's proven range."
            ),
            "all_checks_fired": ["FRONTIER_EMPTY"],
        })
        return record

    # consistency of the run itself
    delta = abs(evidence["engine_score"] - evidence["independent_score"])
    if delta > SCORE_TOLERANCE:
        fired.append((
            "EXECUTION_ERROR",
            "run consistency check",
            f"score_delta {delta:.3e} exceeds tolerance {SCORE_TOLERANCE:.0e}",
        ))

    # mathematical possibility of the observation
    ok_range, reason = oracle_check(arm, evidence["engine_score"])
    if not ok_range:
        fired.append(("CONTRADICTS_PROVEN_RANGE", "proven-range oracle", reason))

    kind = evidence["kind"]

    # control behaviour
    if kind == "control":
        cid = evidence["case_id"]
        want_min = "L0" if cid == "P0" else "L2"
        ok = level_rank(evidence["observed_level"]) >= level_rank(want_min)
        if cid == "P1" and evidence["observed_level"] == "L0":
            ok = False
        if not ok:
            fired.append((
                "CONTROL_FAILED",
                "control gate",
                f"{cid} reached {evidence['observed_level']}, required {want_min} or above",
            ))

    # the security property
    if kind == "adversarial" and policy_check(evidence, evidence["observed_level"]):
        fired.append((
            "POLICY_FALSE_NEGATIVE",
            "policy check",
            f"{evidence['case_id']} is {evidence['impact_label']} but received L0",
        ))

    if not fired:
        fired.append((
            "FRONTIER_MAPPED" if kind == "frontier" else "NOT_FOUND_IN_THIS_CASE",
            "policy check",
            "no policy false negative in this case",
        ))

    primary = min((f[0] for f in fired), key=_PRECEDENCE.index)
    provenance = next(f[1] for f in fired if f[0] == primary)
    reason = next(f[2] for f in fired if f[0] == primary)

    # Only one disposition may ever be finding-valid.
    disposition = (
        "finding-valid" if primary == "POLICY_FALSE_NEGATIVE" else "experiment-invalid"
    ) if primary != "FRONTIER_MAPPED" and primary != "NOT_FOUND_IN_THIS_CASE" else "informational"

    record = dict(evidence)
    record.update({
        "score_delta": delta,
        "range_valid": ok_range,
        "outcome": primary,
        "provenance": provenance,
        "disposition": disposition,
        "reason": reason,
        "all_checks_fired": [f[0] for f in fired],
    })
    return record