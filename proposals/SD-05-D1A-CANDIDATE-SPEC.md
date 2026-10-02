# D1a Candidate Specification and Selection

**Date**: 2026-10-02 · **Branch**: `publications/2026-board`
**Parents untouched**: `19f4e8e` · `e74e8ca` · `304d920` · `f41f8a7` · `3f684c2` · `df8875c`
**Status**: B and C survive. Selection between them is **semantic**, and is **not made here**.

---

## 1. Honest disclosure about contamination risk

The diagnostic table in `e74e8ca` §4 — showing which level each case lands on under each candidate — **has already been seen**. It is on file.

The derivations below were produced by rules stated here that do not reference any case outcome. That is the strongest available guarantee, not a proof of independence: the outcomes are known and cannot be unknowable. What is enforced is that **no threshold or exponent was tuned against a case**, and the derivation rule for each candidate is published so the claim is checkable.

## 2. Eligibility criteria, applied analytically

A candidate must satisfy both, before any implementation:

1. **Expressivity** — all four tiers reachable over the declared domain
2. **The frozen gate** — `P0 → L0` and `P1 → L2 or above`

Domain is fixed: $x \in [0,\ 1.15]$, from non-negative weights over inputs in $[0,1]$.

### Tier reachability, computed correctly

Three thresholds define **four** tiers. An earlier scratch check indexed tiers by threshold position and mislabelled the top one.

$$L_0: r < t_0 \qquad L_1: t_0 \le r < t_1 \qquad L_2: t_1 \le r < t_2 \qquad L_3: r \ge t_2$$

| Candidate | range | thresholds | L0 | L1 | L2 | L3 | all four |
|---|---|---|---|---|---|---|---|
| `SIGMOID` | $[0.5000,\ 0.7595]$ | $\{0.30, 0.65, 0.85\}$ | **N** | Y | Y | **N** | no |
| `A` recentre | $[0.0000,\ 0.5190]$ | $\{0.30, 0.65, 0.85\}$ | Y | Y | **N** | **N** | no |
| `B` | $[0.5000,\ 0.7595]$ | $\{0.5779, 0.6687, 0.7206\}$ | Y | Y | Y | Y | **yes** |
| `C` | $[0.0302,\ 0.9698]$ | $\{0.30, 0.65, 0.85\}$ | Y | Y | Y | Y | **yes** |

### Gate, applied arithmetically

| Candidate | `P0` | `P1` | gate |
|---|---|---|---|
| `SIGMOID` | L1 | L2 | **FAIL** — `P0` cannot reach `L0` |
| `A` | L0 | **L1** | **FAIL** — `P1` cannot reach `L2` |
| `B` | L0 | L3 | PASS |
| `C` | L0 | L3 | PASS |

### Elimination

- **`A` is eliminated twice over.** It fails expressivity **and** the gate. Earlier wording in `e74e8ca` said "L3 unreachable"; it is **two** tiers unreachable, `L2` and `L3`, because its maximum of $0.5190$ falls below the `L2` boundary of $0.65$. The corrected figure is here.
- **`SIGMOID` fails the `P0` half of the gate.** It was already eliminated at `e74e8ca`; it is the historical state, not a candidate.

**Survivors: B and C.**

## 3. Candidate B — recalibrated thresholds

**Rule, stated independently of any case.** Map each threshold proportionally onto $\sigma$'s actual range:

$$t'_k = \sigma(0) + t_k \cdot \bigl(\sigma(1.15) - \sigma(0)\bigr)$$

This **preserves the relative spacing the design intended** — $L_0$ occupies 30% of the codomain, $L_1$ 35%, $L_2$ 20%, $L_3$ 15%. Equal spacing across the real range was considered and rejected: it discards that intent.

Result: $\{0.57785,\ 0.66868,\ 0.72058\}$.

**Preserves**: the specified transfer function, unmodified. The prose's formula survives intact.
**Changes**: what each level *means*, and where the boundaries fall.
**Thesis it would be testing**: *the function is right; the levels were defined against the wrong range.*

**Cost, stated plainly.** With boundaries at $0.578$ and $0.669$, risk scores compress into a narrow band. Distinguishing `L1` from `L2` becomes a difference of $0.09$ on a scale whose full reachable span is $0.26$. The policy is expressive, but the resolution at which it discriminates is materially poorer than the design assumed.

## 4. Candidate C — sigmoid with a slope derived from expressivity

**Rule, stated independently of any case.** Keep the sigmoid form; choose the smallest slope making all four tiers reachable, with declared margin.

$$f_C(x) = \sigma\bigl(k(x - \bar{x})\bigr),\qquad \bar{x} = 0.575$$

Derivation, from the requirement rather than from any case:

| Requirement | Inequality | Minimum $k$ |
|---|---|---|
| `L0` reachable | $\sigma_k(0) < 0.30$ | $1.4736$ |
| `L3` reachable | $\sigma_k(1.15) \ge 0.85$ | $3.0167$ |

$$k_{\min} = 3.0167 \qquad \Longrightarrow\qquad \textbf{chosen } k = 2k_{\min} = 6.0334$$

Proven range: $[0.0302,\ 0.9698]$.

**Preserves**: sigmoid shape, with its flat extremes and steep middle.
**Changes**: the transfer function's steepness. Thresholds stay at the design's $\{0.30, 0.65, 0.85\}$.
**Thesis it would be testing**: *the design's thresholds were right; the sigmoid as specified was too flat to express them.*

**Cost, stated plainly.** The steepened sigmoid makes the score **more sensitive near the middle** and **less sensitive at the extremes**: an action whose inputs change only slightly near $x = 0$ moves the score very little, and the same near $x = 1.15$. A risk engine should be most sensitive where decisions actually flip — which the steepened form does provide — but it is less linear in effect than the design's plain reading of "sigmoid".

## 5. The choice between B and C is semantic

Both pass. Both are proved. Neither is selected here, because the choice commits to a claim about what the design *meant*, and that is not settled by arithmetic.

| | B | C |
|---|---|---|
| The sigmoid is | correct as written | correct in form, wrong in slope |
| The thresholds $\{0.30, 0.65, 0.85\}$ | wrong | correct |
| Design intent recovered | level semantics | level boundaries |
| Discrimination resolution | poor — $0.09$ spans `L1`→`L2` | good — slope concentrated mid-range |
| Thesis being tested | mis-specified levels | under-powered function |

The distinction matters because **they predict different behaviour**, and that divergence is what the cross would then measure. If the true intent was always a sigmoid over $[0,1]$, C is the honest repair and B papers over a range error. If the σ output was always understood as an uncalibrated score, B is honest and C changes the design.

**This is not resolvable from `19f4e8e`, and no execution of the frozen case set will resolve it** — both leave the `A1+A2` and `A3` counterexamples standing, per `e74e8ca` §4.

## 6. Frozen for whichever is selected

1. The transfer function and thresholds, as derived above, unchanged after selection
2. The proven range, which becomes the **new oracle**: an observation outside it is `CONTRADICTS_PROVEN_RANGE`, `disposition: experiment-invalid`
3. The case set `A1`, `A2`, `A1+A2`, `A3` plus controls `P0`, `P1` — **unchanged**, no adversary added to test a repair
4. The frozen gate `P0 → L0`, `P1 → L2` or above
5. Oracle capability verified by injection before the run
6. Adjudication classifications and precedence unchanged from `1752c30`
7. `19f4e8e` as the historical cell — **not re-run**

## 7. Not in scope

- `V`, `N`, `P` remain agent-influenced. A D1a repair does not reach them.
- Cross construction, once selection is made
- Anything that would rewrite `19f4e8e`