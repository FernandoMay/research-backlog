"""
Reproduction ladder v2 — four outcomes, with pre-registered field classes.

Origin: the gap discovered at 3e4a2ef. SD-03's execution succeeded, its
deterministic metrics reproduced exactly, and three fields differed because
they consume measured wall-clock latency. None of the original three
outcomes fitted, and the honest response was to record the gap rather than
force a wrong bucket.

FOUR OUTCOMES
    REPRODUCED
    REPRODUCED_WITH_ENVIRONMENT_DEPENDENT_FIELDS
    NUMERIC_MISMATCH
    EXECUTION_FAILURE

THE PRE-REGISTRATION RULE, which is what makes the fourth outcome honest
--------------------------------------------------------------------------------
Every numeric field must be classified BEFORE execution as one of

    DETERMINISTIC
    ENVIRONMENT_DEPENDENT
    DERIVED_FROM_ENVIRONMENT_DEPENDENT

without looking at any regenerated value. This is load-bearing. If the class
were chosen after seeing the diff, a mismatch could always be excused by
relabelling the field, and the ladder would have no failure mode at all —
which is exactly NON-DISCRIMINATING-FALSIFIER, the defect class already
recorded twice in this chain.

A field declared DETERMINISTIC that differs is a NUMERIC_MISMATCH and
cannot be reclassified afterwards. That is the property the controls test.

`3e4a2ef` is retained as the evidence of the defect discovery. The fourth
outcome was NOT present when that adjudication was written, and this module
does not retroactively pretend otherwise.
"""

import hashlib
import json

DETERMINISTIC = "DETERMINISTIC"
ENVIRONMENT_DEPENDENT = "ENVIRONMENT_DEPENDENT"
DERIVED_FROM_ENVIRONMENT_DEPENDENT = "DERIVED_FROM_ENVIRONMENT_DEPENDENT"

REPRODUCED = "REPRODUCED"
REPRODUCED_ENV = "REPRODUCED_WITH_ENVIRONMENT_DEPENDENT_FIELDS"
NUMERIC_MISMATCH = "NUMERIC_MISMATCH"
EXECUTION_FAILURE = "EXECUTION_FAILURE"

# Precedence. A deterministic divergence outranks an environment-dependent
# one: if a deterministic field disagrees, the environment cannot explain it
# and the run is a mismatch regardless of what else moved.
_PRECEDENCE = (
    EXECUTION_FAILURE,
    NUMERIC_MISMATCH,
    REPRODUCED_ENV,
    REPRODUCED,
)


def seal(registry):
    """
    Freeze a field registry. Returns its digest.

    The digest is what makes pre-registration checkable: a registry sealed
    before execution has a different digest from any registry edited after,
    provided the content differs.
    """
    payload = json.dumps(registry, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def compare(registry, committed, regenerated, execution_completed=True,
            sealed_digest=None, current_digest=None):
    """
    Adjudicate one reproduction.

    registry      field path -> declared class, sealed before execution
    committed     field path -> published value
    regenerated   field path -> regenerated value

    If sealed_digest is supplied it is checked against current_digest. A
    mismatch means the registry was edited after execution, which is reported
    rather than silently honoured.
    """
    if not execution_completed:
        return {
            "outcome": EXECUTION_FAILURE,
            "reason": "execution did not complete",
            "fields": [],
            "disposition": "experiment-invalid",
        }

    tampered = (sealed_digest is not None and current_digest is not None
                and sealed_digest != current_digest)

    fields = []
    worst = REPRODUCED
    for path in sorted(set(committed) | set(regenerated)):
        declared = registry.get(path)
        c = committed.get(path)
        r = regenerated.get(path)
        if c is None or r is None:
            fields.append({"field": path, "declared": declared,
                           "status": "ABSENT", "note": "missing on one side"})
            worst = _bump(worst, NUMERIC_MISMATCH)
            continue
        equal = _close(c, r)
        if declared is None:
            status = "UNCLASSIFIED"
            verdict = NUMERIC_MISMATCH
        elif equal:
            status = "MATCH"
            verdict = REPRODUCED
        elif declared == DETERMINISTIC:
            status = "DIVERGES"
            verdict = NUMERIC_MISMATCH
        else:
            status = "ENV_DIVERGES"
            verdict = REPRODUCED_ENV
        worst = _bump(worst, verdict)
        fields.append({
            "field": path, "declared": declared,
            "committed": c, "regenerated": r,
            "status": status, "contributes": verdict,
        })

    out = {
        "outcome": worst,
        "fields": fields,
        "registry_sealed_digest": sealed_digest,
        "registry_current_digest": current_digest,
        "registry_tampered_after_sealing": tampered,
        "disposition": "finding-valid" if worst in (REPRODUCED, REPRODUCED_ENV)
        else "experiment-invalid",
    }
    if tampered:
        out["reason"] = ("field registry changed after sealing; the "
                         "classification cannot be honoured post hoc")
        out["disposition"] = "experiment-invalid"
    return out


def _bump(current, candidate):
    return candidate if _PRECEDENCE.index(candidate) < _PRECEDENCE.index(current) else current


def _close(a, b, rel=1e-9, abs_=1e-12):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= max(abs_, rel * max(abs(a), abs(b)))
    return a == b


def classify_fields(sample_fields, declared_notes):
    """
    Helper producing a registry from a flat field list plus a notes mapping.
    Intended to be called BEFORE execution and sealed immediately.
    """
    return {f: declared_notes.get(f, DETERMINISTIC) for f in sample_fields}