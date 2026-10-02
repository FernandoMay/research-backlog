# D1a — Recovery of Documented Normative Intent

**Date**: 2026-10-02 · **Branch**: `publications/2026-board`
**Purpose**: determine whether B or C is the honest repair, by recovering what the design *said*, not by preference.
**Status**: intent substantially recovered. One interpretive step identified and stated.

---

## 1. Source limitation, stated before the citation

> **There is no versioned SD-05 design artifact in this repository.** The only `SD-05-*` files are those produced by this audit. The normative text exists solely as a transcription in conversation, with no digest and no version history.

This is a real limitation and it is not worked around. Two consequences:

- The intent recovered below is attributable to **a transcribed text**, not to a version-controlled specification.
- No future reader can verify these quotes against an artifact, because there is no artifact. They can verify them only against the conversation.

A design decision that commits to normative intent should ideally rest on something versioned. This one does not, and that is a finding about the project's documentation state, not about the candidates.

## 2. The normative text, quoted

**Codomain — explicit:**

> definimos la función de escalado de riesgo no lineal $r_i \in [0, 1]$

**Thresholds, with enforcement mechanisms and costs attached:**

> | **$L_0$: Low Risk** | $r_i < 0.30$ | **Local Receipt:** Log local con hash en cadena local. | $< 1\text{ ms}$ | $\$0.00$
> | **$L_1$: Medium Risk** | $0.30 \le r_i < 0.65$ | **Signed Receipt:** Recibo con firma Ed25519 ... | $2-5\text{ ms}$ | $\$0.00$
> | **$L_2$: High Risk** | $0.65 \le r_i < 0.85$ | **On-Chain Anchoring** ... | $200-800\text{ ms}$ | Gas estándar
> | **$L_3$: Critical** | $r_i \ge 0.85$ | **Multi-Party Attestation** ... | $1000-2500\text{ ms}$ | Multi-sig gas

**Transfer function — bare σ, no slope parameter:**

> $$r_i = \sigma \left( w_1 U_i + w_2 V_i + w_3 I_i + w_4 N_i + w_5 P_i + \gamma (U_i \cdot V_i) \right)$$

The only named tuning constant is $\gamma$, and the prose carries it as a **free parameter with no stated value**; the code hardcodes `0.15`.

## 3. The four questions

### Q1 — What did `0.30 / 0.65 / 0.85` mean?

**Normative boundaries tied to enforcement mechanisms.** Each threshold selects a specific attestation mechanism with stated latency and cost, and the design's stated thesis is that attestation cost should scale with risk. These are not arbitrary cut-points on an arbitrary scale — they *are* the policy.

### Q2 — Calibrated probability/risk, or a score?

**A score, never claimed to be calibrated.** The prose calls it a *"función de escalado de riesgo"* and contains no calibration, reliability, or probability language. The design's risk semantics come entirely from the thresholds, not from the score's distribution.

### Q3 — Was σ's slope normatively fixed?

**No.** The prose writes bare `σ` with no steepness parameter. Unlike $\gamma$, which is at least named, the slope is not addressed at all. It is **incidental to the implementation**, not part of the specification.

### Q4 — What did the scale's definition state?

**$r_i \in [0,1]$, explicitly.** The design declares the codomain in the same sentence that introduces the function.

## 4. Consequence

The design normatively fixes **two** things and leaves **one** unspecified:

| Element | Status | Source |
|---|---|---|
| codomain $[0,1]$ | **normative** | "$r_i \in [0,1]$" |
| boundaries $\{0.30, 0.65, 0.85\}$ | **normative** | threshold table with mechanisms and costs |
| σ's slope | **unspecified** | bare `σ`, never addressed |

Applied to the candidates:

| | codomain honoured | boundaries honoured | touches a normative element? |
|---|---|---|---|
| **B** | yes | **no** — moved to $\{0.578, 0.669, 0.721\}$ | **yes** — redefines the policy |
| **C** | yes — range $[0.0302, 0.9698] \subset [0,1]$ | yes — kept at $\{0.30, 0.65, 0.85\}$ | **no** — specifies an unspecified parameter |

**C is the repair that satisfies both normative constraints and changes only what the design left unspecified.** B preserves the specified function and redefines the policy boundaries, which is the reverse of what the documented intent supports.

## 5. The interpretive step, stated rather than hidden

The conclusion depends on reading **"$r_i \in [0,1]$" as normative about the function's output**, rather than as a loose label on the quantity $r_i$.

The text supports this reading: it declares the range in the same sentence that introduces the function, and the thresholds immediately after are absolute numbers in that range. But the text does not use the word "calibrated", and it never says the output is a probability.

**An alternative reading exists** — that $\sigma$'s output was always understood as an uncalibrated score and `0.30` was meant as "30% of the achievable range". Under that reading B would be faithful and C would be the redesign. **The text does not state this.** Adopting it would be inventing a retrospective intent, which is exactly what must not happen.

So: the documented intent points to C, subject to one interpretive step that is recorded rather than concealed.

## 6. Corrected contamination formulation

`f85333f` stated the disclosure in a form that over-claimed. The accurate formulation, per the correction:

> The per-case predictions for B and C **cannot be treated as results independent of the historical observation**. Candidate selection must rest exclusively on pre-defined semantic rules and analytic properties.

This is **not** the claim that B and C were tuned to the cases. The parameters do come from rules that contain no case, and the rules are published, so that claim remains checkable. The two statements are different, and the second is the accurate one.

## 7. What this document does not do

- It does not select the candidate. `f85333f` deliberately left that open; this document supplies the evidence for the choice and stops there.
- It does not repair the missing versioned artifact. That remains a documentation defect, recorded in §1.
- It does not reach `V`, `N` or `P`.
- It does not modify `19f4e8e`, `e74e8ca`, `304d920`, `f41f8a7`, `3f684c2` or `df8875c`.