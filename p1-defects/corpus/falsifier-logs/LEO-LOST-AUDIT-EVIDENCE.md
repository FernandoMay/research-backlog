# LEO — lost audit evidence

**Date:** 2026-09-30
**Status:** permanent record. These items are **not** reconstructed.

## Lost: pre-fix (RED) falsifier transcripts

Three rows had their RED transcript overwritten. The cause was mechanical and
identical in all three cases: the pre-fix run and the post-fix run were both
piped through `tee` to the same filename, so the second write replaced the
first.

| row | RED transcript | what survives |
|---|---|---|
| **R1** (`395ea46`) | lost | commit message body states "Red before the change, with the reseeded draw shown to be the objective itself"; the numbers quoted there (47.8885 / 71.0731 / 66.4372) came from the observed RED run |
| **R2** (`37aa3f2`) | lost | commit message describes the refuted premise and the repair's effect |
| **M1-C** (`3fd1fa6`) | lost | commit message records the pre-fix substitution and the observed coverage counts |

Rows whose RED transcript **is** preserved in `FALSIFIER-LOG-*.md`: **L1c,
L1p, M1, M1-B2**.

## What this means for the chain

The RED-before-GREEN sequence is **not** independently verifiable from the
repository for those three rows. What remains verifiable is:

- the commit messages, which describe the RED state;
- the code at each parent commit, from which the RED behaviour can be
  re-derived by checkout and execution;
- the replay, which reconstructs the current-state GREEN from history alone.

The RED transcripts for R1, R2 and M1-C are therefore **lost audit evidence**,
recorded as lost rather than reconstructed. A reconstruction produced after the
fact would not be the original observation, and presenting one as such would be
the same defect this program audits: a transcription presented as a measurement.

## Correct practice going forward

Falsifier logs are append-only. A row should write its pre-fix run to
`FALSIFIER-LOG-<row>-RED.md` and its post-fix run to
`FALSIFIER-LOG-<row>-GREEN.md`, and both should be committed with the repair.
Overwriting a log with a later run destroys the only artifact that records what
the instrument said before the repair, which is the half of the evidence that
distinguishes a falsifier from a test.

## Related: retained on purpose

The false-green discoveries in rows R2, M1-B, M1-C and P1 are **retained** in
comments inside the falsifier files. They are not cleaned up, because they are
the evidence for the methodology this package contributed:

> Textual presence is not behavioral verification.

Four false greens came from scanning source text instead of behaviour, and one
vacuous pass came from a probe that never forced the condition it claimed to
observe. Both classes are recorded in place.
