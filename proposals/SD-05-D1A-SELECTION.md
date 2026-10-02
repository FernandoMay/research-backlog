# D1a — Selection Record

**Date**: 2026-10-02 · **Branch**: `publications/2026-board`
**Decision**: candidate **C** selected.
**Scope of this commit**: closes the selection only. **No execution.**

---

## 1. The classification of the selection

> **C = repair selected by preservation of documented normative properties, under an incomplete primary source.**

The label is deliberate and both halves are load-bearing. C is not "the correct repair"; it is the repair selected by a stated criterion, applied to a source that cannot be verified against an artifact.

## 2. The narrower claim that is defensible

> **Given the recovered normative text and its documentation limits, C is the repair that modifies only the degree of freedom the text left unspecified.**

Not: that C is the historically intended function. Not: that B is wrong. Not: that C is better.

## 3. Basis

| Element | Status in the source | C's treatment |
|---|---|---|
| codomain $[0,1]$ | normative | preserved — range $[0.0302,\ 0.9698] \subset [0,1]$ |
| boundaries $\{0.30,\ 0.65,\ 0.85\}$ | normative | preserved unchanged |
| slope of $\sigma$ | **unspecified** | **specified** — the only thing changed |

B was eliminated by this criterion: it moves the normative boundaries to $\{0.57785,\ 0.66868,\ 0.72058\}$ and preserves the unspecified function unchanged, which inverts the preservation.

## 4. Frozen parameters

Frozen at selection. No adjustment after any execution.

| Parameter | Value | Provenance |
|---|---|---|
| $k_{\min}$ | $3.0167$ | derived from `L3` reachability: $\sigma_k(1.15) \ge 0.85$ |
| margin | $\times 2$ | declared, chosen at specification time |
| $k$ | **$6.0334$** | $2k_{\min}$ |
| midpoint $\bar{x}$ | $0.575$ | $(0 + 1.15)/2$ |
| thresholds | **$\{0.30,\ 0.65,\ 0.85\}$** | normative, unchanged |
| proven range | **$[0.0302,\ 0.9698]$** | analytic, pre-implementation |
| domain $x$ | $[0,\ 1.15]$ | from non-negative weights, inputs in $[0,1]$ |

$$f_C(x) = \sigma\bigl(6.0334\,(x - 0.575)\bigr)$$

## 5. Regenerated oracle

The proven range becomes the constraint on execution:

```text
any C observation outside [0.0302, 0.9698]
      -> CONTRADICTS_PROVEN_RANGE
      -> provenance: proven-range oracle (regenerated for C)
      -> disposition: experiment-invalid
```

Pre-known before any adversary runs:

| Property | Status |
|---|---|
| `L0` reachable | yes |
| `L1` reachable | yes |
| `L2` reachable | yes |
| `L3` reachable | yes |
| `P0 → L0` | required by the frozen gate |
| `P1 → L2` or above | required by the frozen gate |

Oracle capability must be verified by injection before the run, as at `f41f8a7`.

## 6. Discipline for the implementation that follows

> If the implementation produces unexpected values, **adjudicate against C's analytic range first.** Do not readjust $k$ while looking at cases.

$k$ is frozen by §4. An observation that appears anomalous is a candidate `CONTRADICTS_PROVEN_RANGE` until proven otherwise, not grounds to move the parameter.

## 7. Not done in this commit

- **No execution.** `A1`, `A2`, `A1+A2`, `A3` are not run.
- No implementation of $f_C$ yet.
- No cross construction.
- No modification of `19f4e8e`, `e74e8ca`, `304d920`, `f41f8a7`, `3f684c2`, `df8875c`, `f85333f` or `8af0be7`.

## 8. Carried forward, unchanged

- `19f4e8e` remains frozen. `0.0733` and `0.0865` remain the historical evidence of the original system under declared `I` — **not targets the new implementation must make disappear.**
- The historical cell is **not re-run** to complete a matrix.
- `V`, `N`, `P` remain agent-influenced and outside D1a.
- The missing versioned design artifact (§1 of `8af0be7`) remains an open documentation defect.