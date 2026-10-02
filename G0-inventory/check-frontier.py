#!/usr/bin/env python3
"""
G0 frontier invariant check.

Read-only. Makes the three audit frontiers a machine-checkable property
instead of prose, and detects the one silent failure mode that matters here.

THE FAILURE THIS EXISTS TO CATCH
--------------------------------
Local `main` sits one commit ahead of `origin/main`. That is deliberate.
Someone who later runs `git push origin main` "to catch up" publishes G0-3
wave 2 to the default branch, collapses the boundary established in
G0-BRANCH-BOUNDARY.md, and does it with a clean exit status and no error.

That is why this checks OBSERVED REF STATE and not whether commands
succeeded. A push reports; refs prove.

GitHub branch protection is deliberately NOT applied yet. Enabling it is an
infrastructure decision that should be made once and verified to actually
reject a direct push, not toggled in reaction. Until then, this script is
the compensating control.

Usage:  python3 check-frontier.py     (exit 0 = intact, 1 = violated)
"""

import subprocess
import sys

# Pinned states. Each is a decision, not a snapshot of whatever is current.
PINNED = {
    "origin/main": "9d61c09a8ddba82561b5fd84317671f582a4b6a4",
    "local main": "34e63eb96f211616a2a645b2022aa6984a0bb84e",
}
# Frozen trees: content identity, not commit identity.
FROZEN_TREES = {
    "p1-defects": ("c8c5226", "ce6852428edf6397b70bf762ff6b432dec85ba85"),
    "G0-estate-audit.md": ("b0a2773", "24477a2bcccbe4d535b6e9fc8930d1f5b293091a"),
}


def git(*args):
    p = subprocess.run(["git", *args], capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def lsremote(ref):
    rc, out = git("ls-remote", "origin", f"refs/heads/{ref}")
    if rc != 0 or not out:
        return None
    return out.split()[0]


violations = []
notes = []

# --- Frontier 1: origin/main must not advance ---------------------------
actual = lsremote("main")
if actual is None:
    violations.append("origin/main unreachable — cannot verify the frontier")
elif actual != PINNED["origin/main"]:
    violations.append(
        f"origin/main MOVED: expected {PINNED['origin/main'][:7]}, found {actual[:7]}. "
        "A direct push to the default branch may have published audit state. "
        "STOP and inspect before any further action."
    )
else:
    notes.append(f"origin/main {actual[:7]} unchanged (public frontier)")

# --- Frontier 2: local main stays deliberately ahead -------------------
rc, out = git("rev-parse", "main")
if rc == 0 and out == PINNED["local main"]:
    notes.append(f"local main {out[:7]} frozen ahead of origin — NOT awaiting a push")
elif rc == 0:
    notes.append(f"local main {out[:7]} differs from pinned {PINNED['local main'][:7]} — intentional change?")

# --- Frontier 3: audit branch local == remote --------------------------
remote_audit = lsremote("audit/g0-estate")
rc, local_audit = git("rev-parse", "audit/g0-estate")
if rc != 0:
    violations.append("local audit/g0-estate missing")
elif remote_audit is None:
    violations.append("origin/audit/g0-estate absent — the isolated audit trail has no remote representation")
elif remote_audit != local_audit:
    violations.append(f"audit trail diverged: remote {remote_audit[:7]} vs local {local_audit[:7]}")
else:
    notes.append(f"audit/g0-estate {local_audit[:7]} verified on remote (ls-remote)")

# --- Frozen content: trees must be byte-identical ----------------------
for path, (commit, tree) in FROZEN_TREES.items():
    rc, out = git("rev-parse", f"HEAD:{path}")
    if rc != 0:
        violations.append(f"frozen path missing at HEAD: {path}")
    elif out != tree:
        violations.append(f"FROZEN PATH MODIFIED: {path} is {out[:7]}, expected {tree[:7]} from {commit}")

if not any(v.startswith("FROZEN PATH") for v in violations):
    notes.append(f"frozen content intact: {len(FROZEN_TREES)} trees byte-identical to their pins")

# --- Report ------------------------------------------------------------
for n in notes:
    print(f"  ok    {n}")
for v in violations:
    print(f"  VIOLATION  {v}")

if violations:
    print(f"\nFRONTIER VIOLATED ({len(violations)}). Do not proceed on assumption.")
    sys.exit(1)

print("\nAll three frontiers intact.")
sys.exit(0)