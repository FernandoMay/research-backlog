# SD-05 — Package Manifest

**Branch**: `publications/2026-board` · **Date**: 2026-10-02
**Purpose**: index the chain and record the interpretive limit that governs how any of it may be cited.

---

## 1. The boundary phrase

> **The evidence determines which architecture is possible under each semantics; it does not determine which semantics the policy should have had.**

Every claim in this package is subject to it. It is the reason `74af5fa` closes an architectural finding without making a normative choice, and the reason no result here may be restated as a repair that was discovered experimentally.

## 2. The chain

| Commit | Artifact | State |
|---|---|---|
| `f74963e` | SD-05 design recorded, 7 defects (D1–D7) | historical |
| `2485544` | venues verified at source | historical |
| `1752c30` | D1 split into D1a/D1b; proven-range oracle | frozen |
| `d31ab45` | D3 falsifier spec; spec found void | frozen |
| `4c774dd` | execution error vs instrument defect separated | frozen |
| `304d920` | D1a repair spec, candidates A/B/C | frozen |
| `f41f8a7` | D1b stub falsifiability — independent authority exists | frozen |
| `3f684c2` | D1b `I−`/`I+` controls — derivation implements the semantics | frozen |
| `8af0be7` | normative intent recovered | frozen |
| `41fdc4b` | **C selected**, parameters frozen | frozen |
| `3ea1927` | recovered intent versioned as provenance | frozen |
| `953032b` | operation 1 — `f_C` implemented | frozen |
| `121d751` | operation 2 — range and tier capability | frozen |
| `8924893` | oracle capability injection, 11/11 | frozen |
| `7e22541` | analytic prediction frozen before execution | frozen |
| **`19f4e8e`** | **run 1 snapshot — historical, never rewritten** | **immutable** |
| `a1c2f66` | the cross executed | frozen |
| `84a5fd1` | cross adjudication | frozen |
| `098bdf8` | `V` specification — architecture finding | frozen |
| `74af5fa` | `V` closure, fork open | **current** |

Also produced and separately frozen: `SD-05-INSTRUMENT-CONTROL-VACUITY.md` (`CONTROL-NOT-DELIVERED`), and `SD-05-INSTRUMENT-*.md` records of the instrument defects found along the way.

## 3. What each result establishes, and what it does not

| Result | Establishes | Does **not** establish |
|---|---|---|
| `f41f8a7` | a potentially independent authority source exists | that `I_derived` is correct |
| `3f684c2` | the derivation resists under- and over-declaration | that `V`, `N` or `P` are anything |
| `121d751` | `f_C` attains the analytic range; all four tiers reachable | that `f_C` is a valid policy |
| `8924893` | the oracle can detect a range violation | anything about the cross |
| `a1c2f66` | derived `I` removes `A1`; `A2`, `A1+A2`, `A3` persist | that D1b is resolved |
| `098bdf8` | `V` has no independent pre-authorisation observable | which design `V` should adopt |
| `74af5fa` | D1b cannot be extended to `V` as a pre-authorisation gate | that `V` is unprotectable |

## 4. Standing non-claims

```text
ELIGIBLE   ≠  REPRODUCED
NOT_YET    ≠  NOT_REPRODUCIBLE
NO_CLAIM   ≠  NO_RESEARCH
consistent ≠  confirmed
counterexample eliminated  ≠  security result
```

## 5. Out of scope and untouched

- **`N` and `P`** — agent-influenced, **not exercised** by any run. Surfaces, not grounds to extend any conclusion.
- **`19f4e8e`** — immutable, never re-run, never reinterpreted by any later result.
- **`k = 6.0334`, thresholds `{0.30, 0.65, 0.85}`, `V`'s scale, case composition** — unmodified throughout.
- **The `V` fork** — open, and a design decision. No further work on `V` should begin before it is settled; building controls or an implementation now would select semantics by technical convenience.
- **Venues** — AIBT Oct 10 and ICCBN Oct 5 verified at source; portal, template and page limits remain unverified.