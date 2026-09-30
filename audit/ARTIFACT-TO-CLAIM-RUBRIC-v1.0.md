# Artifact-to-Claim Integrity Rubric v1.0

**Created:** 2026-09-29
**Status:** canonical. Every audit in this series is scored against this file, and this file is versioned.

## Why this exists

Three audits of this account (nine orphan packages, four Stellar repositories, `h266-drl-iccpr2026-package`, `cd-ieee-package`) found the same fracture repeatedly: **the simulation infrastructure is sound and the paper written on top of it is not.** Clean, seeded simulators whose baselines reproduce exactly, under papers containing numbers absent from their own artifacts.

Those audits used different rubrics, so their counts are not comparable. This file fixes that. It is the denominator.

## Reference case

`cd-ieee-package` is the reference exemplar. It scored 3 SUPPORTED / 14 CONTRADICTED / 1 UNSUPPORTED across 20 claims, while its `data/metrics.json` was byte-identical to the upstream artifact and 33/33 cited values verified mechanically. The split is the phenomenon, and this rubric exists to measure it consistently.

A CONTRADICTED verdict on a well-built package is a **positive finding about the audit**, not a failure of the package. Record what holds as carefully as what fails — see rule R7.

## Rules

- **R1 — Artifact before claim.** Never read the paper's number first. Read the artifact, record the value, then find the claim. Inheriting a prior agent's finding without checking is the failure mode this process exists to prevent.
- **R2 — MEASURED vs CLAIMED.** Every value is one or the other. `MEASURED` means read from an artifact or produced by a command you ran. `CLAIMED` means stated in prose with no artifact. No third category, no estimated values.
- **R3 — A run you did not execute is not a result.** Record the exit code and the output. If it cannot be run, say why.
- **R4 — Version scope.** A number is only valid for the artifact version, seed, and configuration that produced it. Flag explicitly when a paper reports a figure from a different run than the one it cites. `cd` did this on 4 of 5 detectors in one section.
- **R5 — No extrapolation.** From `N` audited packages, the report covers exactly those `N`. Do not characterise the other 200+ repositories.
- **R6 — Preserve the denominator.** Report `N audited` alongside every rate. A percentage without its denominator is not a result.
- **R7 — Absence of contradiction is not evidence of presence.** When a claim survives, record it as SUPPORTED. An audit that only finds faults is not a balanced audit, and the confirmed result is what makes a negative finding defensible.
- **R8 — Disclose method failure.** If a tool, endpoint, or environment blocked verification, record it. An unverifiable layer is a result, not a silent omission.

## The eight layers

Score every layer. A layer may be SUPPORTED, CONTRADICTED, UNVERIFIABLE, or NOT APPLICABLE.

### L1 — Artifact

Does the cited result exist as a committed file?

- SUPPORTED: a committed artifact contains the value.
- CONTRADICTED: the artifact exists but disagrees with the claim.
- UNVERIFIABLE: no artifact, and the code does not write one.
- NOT APPLICABLE: the package makes no quantitative claim.

### L2 — Reproduction

Can the result be regenerated from committed code with a stated seed and configuration?

- SUPPORTED: executed by the auditor, output recorded.
- UNVERIFIABLE: could not execute; record the exact blocker.
- CONTRADICTED: executed, and the output disagrees with the committed artifact.

Record the seed, the trial count, and the environment. A committed JSON that does not reproduce across toolchain versions is a finding, not a nitpick — `h266` had weight-init RNG making its JSONs non-bit-reproducible.

### L3 — Numerical claim

Does the number in the paper correspond to the artifact?

Report `claims_total / claims_supported / claims_contradicted / claims_unsupported`. Every CONTRADICTED entry records **both values** — claimed and actual — and the artifact path.

### L4 — Figure

Does each figure have a generator that is committed and reproducible, and does it match the data?

- SUPPORTED: generator committed, runs, output matches.
- CONTRADICTED: figure exists with no generator, or a generator whose output differs from the published figure.
- Flag fabricated interpretation separately from a missing generator. `cd`'s feature-importance figure had a generator — the generator was the defect, sorting `NaN` `f_classify` scores to the top over identically-1.0 constant features.

### L5 — Method

Did the described method actually run?

- SUPPORTED: code implementing the method exists and was exercised.
- CONTRADICTED: the method is described but the code does not implement it, or implements it inertly. `h266` described 120 minibatch iterations and executed 1 `agent.update()` call.

Distinguish a method that was not run from one that was run and produced nothing.

### L6 — Selection

Is there undeclared selection of seed, trial, or best case?

- SUPPORTED: no selection, or selection is declared and the full distribution is reported.
- CONTRADICTED: best-case reported without disclosure. `h266` reported seed 42 at 69.27 VMAF while a uniformly random policy scored 63.37 and the other three seeds scored 56.71 / 64.79 / 61.23.

Also check the inverse: a zero-variance result across many trials (`cd` Isolation Forest, sd 0.0000 over 20 seeds) makes a significance test meaningless. That is a selection-and-statistics finding, not a positive result.

### L7 — Internal consistency

Do tables, figures, and prose describe the same run?

- SUPPORTED: all three agree.
- CONTRADICTED: a section reports values from a different trial than the figure it cites, or the abstract, body, and artifact disagree on the headline number. `cd` had Isolation Forest stated as 0.999 in the abstract, 1.000 in the body, and 1.0000 in all 20 trials of the artifact.

### L8 — Verdict

One of:

| Verdict | Meaning |
|---|---|
| **SUPPORTED** | Artifacts exist, reproduce, and match every claim. |
| **PARTIALLY SUPPORTED** | Real reproducible artifacts, with a bounded set of contradicted claims. The honest case, and the one `cd` occupies. |
| **CONTRADICTED** | The paper's central claim is contradicted by its own artifacts. |
| **UNVERIFIABLE** | The audit could not establish enough to judge. |

## Aggregate

Once every package is scored, compute and report:

```
N audited
N with reproducible artifacts (L1+L2 SUPPORTED)
N with internally consistent papers (L7 SUPPORTED)
N with unsupported claims (L3 unsupported > 0)
N with contradicted claims (L3 contradicted > 0)
N with figure/data mismatch (L4 CONTRADICTED)
N with methodological non-execution (L5 CONTRADICTED)
```

Always with `N audited` attached. R5 and R6 forbid extending these figures beyond the audited set.

The hypothesis under test, stated so it can fail: **artifact reproducibility is materially better than artifact-to-claim correspondence.** If the aggregate does not support that, report that instead.
