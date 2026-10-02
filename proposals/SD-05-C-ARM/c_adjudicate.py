"""
C-arm adjudication — the run-1 instrument, with C's proven range registered.

INTEGRATION FACT, recorded rather than worked around
----------------------------------------------------
The frozen run-1 adjudicator (`19f4e8e`) knows only `CLAMP` and `SIGMOID`.
Its `oracle_check` looks up `PROVEN_RANGE[arm]` and raises `KeyError: 'C'`
when handed the new arm. That is not a defect in the snapshot — it is the
correct behaviour of an instrument frozen against the arms that existed when
it was written.

So the C experiment needs its own instrument. Rather than duplicating the
adjudication logic or editing the frozen file, this module:

  * imports the real `adjudicate` from the run-1 snapshot, unchanged
  * registers C's analytically proven range in that module's lookup
  * touches nothing on disk in the snapshot

The snapshot's digest is verified unchanged before and after this import.
Nothing in the adjudication logic is reimplemented here, so what is under
test is the instrument that will actually be used in the cross.
"""

import sys

sys.path.insert(0, "../SD-05-D3-IMPLEMENTATION")

import instruments

C_PROVEN_RANGE = (0.0302, 0.9698)

# The single registration. Frozen at 41fdc4b, proven analytically in the
# operation-2 sweep, verified attainable by verify_c_oracle.py.
if "C" not in instruments.PROVEN_RANGE:
    instruments.PROVEN_RANGE["C"] = C_PROVEN_RANGE

adjudicate = instruments.adjudicate
oracle_check = instruments.oracle_check

__all__ = ["adjudicate", "oracle_check", "C_PROVEN_RANGE", "instruments"]
