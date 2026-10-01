# QCE-3 — Claim-Chain Adjudication

**Status:** adjudication complete and frozen. **No manuscript text has been edited.
No number corrected. No repair started.**
**Branch:** `fix/qce-audit-sweep`. **Baseline:** `97ed1cb`.
**Evidence:** `FALSIFIER-LOG-QCE-1.md` (causal participation),
`FALSIFIER-LOG-QCE-2.md` (ablation reconstructibility), `CLAIM-INVENTORY-QCE.md`.

Each claim is adjudicated along one chain, and the links are **not** summed:

```
claim  →  mechanism  →  experiment  →  artifact  →  provenance
```

---

## 0. Three rules this adjudication follows, and why

**Two prohibitions are stated here and bind any future repair.**

1. **`gamma = 0` is not the NoRL intervention.** QCE-1 established that `gamma` occurs
   once and is never read. Building an ablation arm on it would be intervening on a
   dead parameter, and the arm would be vacuous — it would report "no effect" for a
   reason that has nothing to do with the mechanism under test. NoRL is defined by
   removing the predictor from the **decision path**, which is the causal route it
   actually takes.
2. **A numeric discrepancy is not a repair target.** No historical published number
   anywhere in this package — 21 errors, 578.3 mW, 0.0070, 0.9237, 627.3, 13.8% — is a
   target a repair may be tuned toward. A repair is validated by restoring a
   pre-specified property, never by producing a number that matches a published one.

**Failures are not summed.** `gamma` being unread and the predictor emitting a
constant are causally related — the second partly explains why the first cannot be
observed — but they are different claims with different evidence and different
dispositions. C4 (adapts) and C13 (`gamma` inert) are recorded separately.

**A numeric discrepancy is not automatically an implementation fault.** Each published
number is put through:

```
published number
  → can I identify its population?
  → can I identify its execution?
  → can I regenerate it?
  → is the discrepancy documented?
```

Only when all four fail does a number become an R1 candidate. Missing experimental
identity is **R3/provenance**, not incorrect implementation.

**Mechanism correspondence and quantitative reproduction are different axes.**
`QCE-NoSafety` is the cleanest case in the whole sweep: the *direction* of the causal
chain is exactly what the paper says, and the *magnitude* is not. Reducing that to
"contradicted" destroys information.

---

## 1. Adjudication matrix

| ID | Claim | Source | Mechanism | Experiment | Artifact | Provenance | Verdict | Class |
|---|---|---|---|---|---|---|---|---|
| C1 | "quantum-inspired variational optimizer", "based on a simplified QAOA ansatz" | `:26`, `:489` | none executed; `self.params` ×1 at `:201` | exhaustive scan of 32 basis states | `optimize()` `:249-277` | **disclosed** at `:226` "we perform basis-state enumeration" | **SUPPORTED BY DISCLOSURE** | R3 |
| C2 | "pre-computes **Pareto-optimal** configurations" | `:26`, `:489` | no dominance test exists | `optimize()` returns one point | `pareto`/`front`/`dominance` = 0 occurrences | — | **CONTRADICTED** | R2/R3 |
| C3 | "an online **reinforcement learning** predictor" | `:26`, `:266` heading | logistic regression + online SGD | — | `reward`/`action`/`policy`/`Q_value`/`discount` = 0 | body discloses "logistic regression" `:268` | **R3 — label only** | R3 |
| C4 | "**continuously adapts** to system conditions from streaming sensor data" | `:489`, `:482` | predictor is causal (QCE-1 control) | episode | `pred_prob` constant **0.150039**, all 200 decision steps | — | **CONTRADICTED** | R1/R2 |
| C5 | "the RL predictor **enables anticipatory mitigation** … detecting early signs of thermal stress before errors occur" | `:482` | — | one risk level (0.1) for all 200 steps | constant output carries no per-step information | — | **CONTRADICTED** | R1/R2 |
| C6 | "the safety-bounded prediction prevents the system from overconfidently boosting performance" | `:482` | floor pins `pred_prob ≥ 0.15` | NoSafety arm reaches risk 0.01, DVFS 3, 18 errors | floor = 0.15 at `:168` | — | **SUPPORTED** | — |
| C7 | "the 13.8% reduction arises **primarily from the quantum optimizer's decision** to use DVFS 2 instead of DVFS 3" | `:484` | DVFS 2 is *selected* because risk = 0.1 | risk = 0.1 because `pred_prob` = 0.150039 ∈ (0.05, 0.2] | floor = 0.60 → power 354 mW; floor = 0.0 → DVFS 3 appears | — | **ATTRIBUTION CONTRADICTED** | R2/R3 |
| C8 | "we perform basis-state enumeration … 32 computational basis states" | `:226` | argmin of `diag(H_c)` | — | exactly what `optimize()` does | — | **SUPPORTED** | — |
| C9 | `eq:predictor`, `eq:update`, `eq:bias_update` | `:271`, `:280`, `:285` | matches `predict()`/`update()` verbatim incl. the raw-gradient bias note | — | `qce_simulator.py:170-187` | — | **SUPPORTED** | — |
| C10 | weight sign analysis (all negative at r=0.01, positive at r≥0.1) | `:230-240` | — | — | control: rel×0.05 → mask `[False]*5`; rel×1.0 → `[True]*5` | — | **SUPPORTED** | — |
| C11 | `tab:precomputed` (4 risk levels → DVFS + mask) | `:256-259` | — | — | matches `run_episode`'s table exactly | **identical to the C kernel's output** | **SUPPORTED** | — |
| C12 | offline cost ≈ 3200 ops, negligible vs T=200 | `:244` | — | — | consistent | — | **SUPPORTED** | — |
| C13 | `gamma` is a discount factor of the predictor | `:266` heading | **unread**; 1 occurrence, `:166` | 0.0 / 0.9 / 0.999 identical | — | — | **NO PARTICIPATION** | R1 |
| C14 | "warmup (first 10 steps): temperature-based selection" | `:297` | — | — | `t < 10` branch at `:356` | — | **SUPPORTED** | — |
| C15 | QCE zero errors; reliability 0.924 vs 0.912 | `:491`, `:26` | — | main run | 0.9236939 / 0.9116773, both byte-traced | `SEED=42`, reproduces exactly | **SUPPORTED** | — |
| C16 | power reduction **13.8%** | `:26`, `:484`, `:491` | — | main run | **13.7404%** | — | **NUMERIC DISCREPANCY** — 13.740 rounds to 13.7 | R3 |
| C17 | `tab:ablation` row **QCE-NoSafety** = 21 / 578.3 / 0.0070 | `:447` | **corresponds**: floor=0 makes risk 0.01 reachable | σ=0 reproduces risk 0.01, DVFS 3, errors | 18 / 582.0 / 0.0499 | no code path in repo | **MECHANISM SUPPORTED · QUANTITATIVE REPRODUCTION FAILS** | R2/R3 |
| C18 | `tab:ablation` row **QCE-NoRL** = 0 / 627.3 / 0.9237, "identical to full QCE" | `:448`, `:456` | paper defines it as temperature-policy-only | temperature policy selects risk {0.1, 0.3, 0.7} | **0 / 490.84 / 0.94083** | no code path; identity not produced by the paper's own definition | **IDENTITY / PROVENANCE FAILURE** | R2/R3 |
| C19 | "includes a **reference** C kernel for embedded deployment" | `:26`, `README:10` | `expf()` reliability form, 4 precomputed configs, `RAND_MAX` float warning | compiled and executed | **1.0000** vs 0.9237; 619.0 mW vs 627.3 | divergence never stated | **CORRESPONDENCE GAP** | R3 |
| C20 | "the predictor requires only four multiplications per step" | `:491` | — | — | `np.dot(W, obs)` with `n_sensors=4` | — | **SUPPORTED** | — |
| C21 | figures reproduce | implied by "fully implemented in NumPy for reproducibility" `:26` | — | regenerated all 5 | IHDR 1483 vs 1484 px, max pixel diff 1.0 | data byte-identical | **ENVIRONMENTAL — not a data contradiction** | — |
| C22 | "direct **Pareto** optimization" is future work | `:493` | — | — | — | — | **INTERNAL TENSION with `:26`/`:489`** | R3 |
| C23 | Chinese paper carries the strong labels | `paper/zh` | — | — | 帕累托 5, 逻辑回归 4, 随机梯度下降 2 | — | **NON-FINDING — disclosure present** | — |

**Counts:** SUPPORTED 9 · SUPPORTED BY DISCLOSURE 1 · CONTRADICTED 3 ·
ATTRIBUTION CONTRADICTED 1 · NO PARTICIPATION 1 · NUMERIC DISCREPANCY 1 ·
MECHANISM-SUPPORTED/QUANTITATIVE-FAIL 1 · IDENTITY/PROVENANCE FAILURE 1 ·
CORRESPONDENCE GAP 1 · INTERNAL TENSION 1 · ENVIRONMENTAL 1 · NON-FINDING 1.

---

## 2. C17 — the finest distinction in the sweep

`QCE-NoSafety` is the case that justifies separating the two axes.

**Mechanism correspondence: SURVIVES.** The paper at `:454` predicts that removing
the floor lets the predictor drift low, makes risk level 0.01 reachable, selects
DVFS 3, and causes thermal runaway. Every link of that chain occurs:

| predicted at `:454` | observed under σ = 0 |
|---|---|
| predictions drift very low | `pred_prob` falls below 0.05 |
| selects risk level 0.01 | risk levels become `[0.01, 0.1]` — 0.01 appears for the first time |
| DVFS 3, no mitigations | DVFS levels become `[2, 3]` — 3 appears for the first time |
| thermal runaway, errors | **18 errors** |

**Quantitative reproduction: FAILS.**

| | errors | power (mW) | reliability |
|---|---|---|---|
| published | 21 | 578.3 | 0.0070 |
| reconstructed | 18 | 582.0 | 0.0499 |

The power agrees to 0.6%. The error count is within 14%. The **reliability differs by
a factor of seven** (0.0499 against 0.0070).

So the disposition is **not** "contradicted". It is: the mechanism the row describes
is real and behaves as described; the magnitude it is reported with is not
reproducible from the committed artifact. A repair that "fixed" this by tuning numbers
toward 21 / 578.3 / 0.0070 would be repairing a *target*, not a *property*.

---

## 3. C18 — stated as an identity failure, not a reproduction failure

"NoRL does not reproduce" is too weak. The chain is:

```
published QCE-NoRL  =  0 errors / 627.3 mW / 0.9237      (identical to Full)
        ↓  what does the paper define NoRL to be?  :434
"temperature-based policy selection only"
        ↓  reconstruct that policy on the committed artifact
risk levels {0.1, 0.3, 0.7}, DVFS {1, 2}
        ↓
0 errors / 490.84 mW / 0.94083
```

**while the mechanism the repository actually preserves:**

```
predictor  →  constant 0.150039  →  risk 0.1  →  Full-like behaviour
```

The two policies are not the same policy. Junction temperature ranges 45.00 to 74.65
over the episode and crosses two thresholds; the predictor's constant never crosses
one. That is why removing the predictor changes the outcome on **both** axes, in the
direction of better reliability *and* lower power.

**Deliberately not concluded:** that the NoRL arm had no effect. The published identity
is not treated as proof of that. A third possibility stays open — the row may have been
produced by an implementation differing from `:434` — and this repository preserves
nothing against which to test it. That absence *is* the finding.

---

## 4. C7 — attribution

The paper attributes the power saving to the **optimizer's decision** to use DVFS 2.
The measurements place it elsewhere in the chain:

```
floor = 0.15 (default)  → pred_prob 0.150039 → risk 0.1 → DVFS 2 → 627.3 mW
floor = 0.60 (control)  → risk {0.1, 0.7}    → DVFS {0, 2} → 354.0 mW
floor = 0.00 (NoSafety) → risk {0.01, 0.1}   → DVFS {2, 3}  → 582.0 mW
```

DVFS 2 is reached because the safety floor pins `pred_prob` above the 0.05 threshold
into the 0.1 bucket. The optimizer's table *maps* risk 0.1 to DVFS 2, but nothing in
the optimizer chooses to be at risk 0.1. The saving is attributable to the floor's
consequence, not to an optimizer preference between frequency levels.

Recorded as an attribution contradiction, not a numerical one: 13.7404% is the
measured reduction (C16 handles its rounding).

---

## 5. Numeric discrepancies — the four-step chain

| published | population identifiable? | execution identifiable? | regenerable? | discrepancy documented? | disposition |
|---|---|---|---|---|---|
| QCE 0.924 | yes, one run | yes, `SEED=42` | **yes**, 0.9236939 | n/a | **traces** |
| full 0.912 | yes | yes | **yes**, 0.9116773 | n/a | **traces** |
| 0 / 0 errors | yes | yes | **yes** | n/a | **traces** |
| **13.8%** | yes | yes | **yes, 13.7404%** | **no** | **R3 numeric discrepancy** — 13.740 rounds to 13.7 |
| **NoSafety 21 / 578.3 / 0.0070** | yes (σ=0) | **no code path** | **partially** — mechanism yes, magnitude no | **no** | **R2/R3** |
| **NoRL 0 / 627.3 / 0.9237** | yes (temperature policy) | **no code path** | **no** — reconstruction differs | **no** | **R2/R3 identity** |
| **kernel 1.0000** | yes | yes (compiled) | **yes** — and it differs | **no** | **R3 correspondence gap** |

Only the `13.8%` row is a case where everything is identifiable and the artifact
simply disagrees. It is therefore the only published number in the package that is a
**numeric discrepancy** rather than a **provenance gap**, and it is the smallest one.

---

## 6. Repair classes

| Class | Meaning | Items |
|---|---|---|
| **R1** | Mechanism not implemented as named | C4, C5, C13 |
| **R2** | Sound mechanism, unidentifiable experiment | C2, C17, C18 |
| **R3** | Valid artifact, invalid document / provenance | C1, C3, C7, C16, C19, C22 |
| **—** | No repair needed | C6, C8, C9, C10, C11, C12, C14, C15, C20, C21 |

**C13 is R1 but trivial and not worth a repair.** `gamma` is unread. The disposition is
to delete an unused attribute, not to implement Q-learning. Recording it as an R1
mechanism gap would overstate it: nothing is claimed to depend on `gamma` except the
heading at `:266`, which C3 already handles as a label issue.

**C4/C5 are the substantive R1 candidates**, and they are about the predictor's
*behaviour*, not its algorithm. A logistic regression trained online on observed labels
is a legitimate online classifier. What fails is the claim that it **detects early
signs** and **continuously adapts** — it emits a constant. That is a real mechanism
gap between the claim and the behaviour, and it is the one finding here that a
different implementation could actually fix.

---

## 7. Non-findings — explicitly protected

| ID | Non-finding | Why it must not be promoted |
|---|---|---|
| N1 | The Chinese paper discloses the mechanism (帕累托 5, 逻辑回归 4, 随机梯度下降 2) | The contrary finding came from searching the **wrong corpus** — English tokens (`pareto`, `logistic`) in a document written in Chinese. A wrong-corpus search returns a clean zero indistinguishable from a real absence. That is a defect of this audit, not of the package. |
| N2 | `gamma` unread does **not** mean the predictor is disconnected | QCE-1's forced-0.95 control moved reliability, power and risk level. The predictor is causal; its *trained state* is non-discriminating. |
| N3 | The optimizer **does** minimise its cost Hamiltonian | H3c's control proved it responds to its inputs. A single-point argmin is not Pareto; it is not "nothing". |
| N4 | PNG byte mismatch is **not** a data contradiction | `metrics.json` is byte-identical; the 1-px difference is rendering environment. |
| N5 | The 0.963554 / 354.0291 observation is **not** a result | An exploratory intervention outside the comparison set. No like-for-like arm is beaten. It belongs in no results table. |
| N6 | The 25/60-sample containment result from i01 is **not** applicable here | QCE has no unseeded revision; its artifact is seeded and reproduces exactly. |

---

## 8. Auditor audit — three records

**A1 — H3b's positive control produced a false negative.** The control intervened on
`predictor.lr`, which is causal in general, and moved nothing. The block correctly
declared its own results void. Investigating produced the deeper finding that the
predictor emits a constant. **Methodological consequence now adopted:** an intervention
producing an ambiguous negative requires an emission/intermediate-state diagnostic,
because *no-effect* and *dead* are different states.

**A2 — a hypothesis was written before its measurement, and would have exonerated the
package.** Before QCE-2 I hypothesised the temperature policy would also always select
risk 0.1, which would have explained the published NoRL identity and vindicated the
paper — and I wrote the concluding lines before running the measurement. Temperature
ranges 45.00 to 74.65 and crosses two thresholds; the premise was false. Third instance
in this sweep of a hardcoded conclusion printed beside a measurement that did not
support it. QCE-2 emits computed text only.

**A3 — a Git error did not become a change to the audited object.** `git push` returned
`cannot lock ref … is at 67cccd9 but expected ca410b4`. Verified with `git ls-remote`
that the remote was already at `67cccd9` — the push had applied server-side and the
error was a stale lock race. **No force-push, no history rewrite, no reset.** The
verified action was to do nothing further.

---

## 9. Summary

| | |
|---|---|
| Claims adjudicated | 23 |
| SUPPORTED | 9 |
| SUPPORTED BY DISCLOSURE | 1 |
| CONTRADICTED | 3 |
| ATTRIBUTION CONTRADICTED | 1 |
| NO PARTICIPATION | 1 |
| NUMERIC DISCREPANCY | 1 |
| MECHANISM SURVIVES / QUANTITATIVE FAILS | 1 |
| IDENTITY / PROVENANCE FAILURE | 1 |
| CORRESPONDENCE GAP | 1 |
| INTERNAL TENSION | 1 |
| ENVIRONMENTAL | 1 |
| **NON-FINDING** | 1 |
| **R1 candidates** | 2 substantive + 1 trivial |
| **R2** | 3 |
| **R3** | 6 |
| Non-findings protected | 6 |
| Auditor records | 3 |
| Falsifier defects retained | 5 |

**This is not the LEO or the Quantum profile.** The artifact is sound, the predictor is
on the dependency path, the numbers trace, and QCE discloses its actual mechanisms
adjacent to every strong label — in both languages. The defects are concentrated in
what the mechanisms *do* relative to what the surrounding sentences say they do, plus
two arms and a reference kernel whose experimental identity the repository does not
preserve.

**No repair is authorised.** No manuscript text has been edited.