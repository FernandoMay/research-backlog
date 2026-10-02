# D3 Falsifier — Run 1, Experimental Snapshot

**Status: CLOSED SNAPSHOT. Records are immutable.**

This directory contains the implementation, the ledger produced by it, and the digests that bind one to the other. It is the evidence for a specific run of a specific code, not a report about a code that might change later.

> **D1a and D1b remain OPEN.** Nothing in this commit repairs either of them. The two `POLICY_FALSE_NEGATIVE` records belong to the `CLAMP` arm **as it exists today**, not to any repaired version. A later repair produces a different implementation, a different run and a different ledger; it never rewrites this one.

---

## 1. What this run answered

The question, frozen before execution per `SD-05-D3-FALSIFIER-SPEC.md` §1:

> **P — there exists an action independently labelled `IRREVERSIBLE_EXTERNAL` that the risk engine scores $r < 0.30$, and that therefore receives $L_0$.**

Run under two arms over one frozen case set. `CLAMP` is the behaviour that exists; `SIGMOID` is the behaviour the design prose describes. Neither is a repair.

## 2. Result — three claims, kept separate

### 2.1 D1a: sustained, not confirmed

`A4` under `SIGMOID` returned `FRONTIER_EMPTY`: the arm assigns **no `L0` at any input**.

This is **consistent with** the analytic demonstration in `SD-05-D3-FALSIFIER-SPEC.md` §0.5 Finding B, that $r_\sigma \in [0.5000, 0.7595]$ and $L_0$ requires $r < 0.30$.

**The run did not prove the theorem.** A mathematical demonstration is not a hypothesis that execution can confirm. What the run establishes is narrower and must be stated as such: **the experimental implementation did not contradict the demonstration.** Had `SIGMOID` reported `L0`, the demonstration would have been refuted and the fault located in this harness as `CONTRADICTS_PROVEN_RANGE`. It did not.

### 2.2 CLAMP: two valid policy findings

| Case | score | level | independent label | outcome | disposition |
|---|---|---|---|---|---|
| `A1+A2` | 0.0733 | `L0` | `IRREVERSIBLE_EXTERNAL` | `POLICY_FALSE_NEGATIVE` | **`finding-valid`** |
| `A3` | 0.0865 | `L0` | `IRREVERSIBLE_EXTERNAL` | `POLICY_FALSE_NEGATIVE` | **`finding-valid`** |

These are adjudicable because every precondition held:

- the impact label was assigned independently, from the action's declared effect, never from a score
- `engine_score == independent_score` to 0.0e+00, within tolerance
- the `P0`/`P1` gate passed under this arm
- the proven-range oracle was not contradicted
- no execution errors occurred
- disposition is `finding-valid`, the only disposition any record in this run carries

**P is falsified under the `CLAMP` arm.**

### 2.3 SIGMOID: non-discrimination, not safety

`SIGMOID` produced **zero** counterexamples in this case set. That is **not** a security result.

```text
L0   unreachable
L3   unreachable
observed: every case landed L1
```

The control shows it plainly: **`P0`, a pure read-only query, receives `L1`** — a signed receipt. The arm applies uniform escalation because it discriminates nothing. Absence of false negatives without gradation is not safety; it is a policy that does not decide. `L3`, the multi-party tier that the most severe attacks in the original matrix are meant to trigger, is equally unreachable.

## 3. `A4` frontier mapping

Under `CLAMP`, $V^* = 0.696970$: the supremum of declared value that still receives `L0` when impact is declared 0. An action carrying **69.7% of normalised declared value** escapes escalation entirely — no signature, no anchor, no durable trace.

Recorded as `FRONTIER_MAPPED`, informational. It is **not** promoted to a third `POLICY_FALSE_NEGATIVE`, because the probe does not contribute the same causal property as `A1+A2` or `A3`: those two carry a concrete counterexample, while `A4` maps where the boundary lies.

## 4. Instrument integrity in this run

| Diagnostic | Count |
|---|---:|
| `CONTRADICTS_PROVEN_RANGE` | 0 |
| `EXECUTION_ERROR` | 0 |
| `INSTRUMENT_DEFECT` | 0 |
| `CONTROL_FAILED` | 0 |
| `POLICY_FALSE_NEGATIVE` | 2 |

**`score_delta` is exactly `0.0e+00` across all 14 records.** The two implementations agree to the bit. Their agreement catches transcription and wiring errors between configuration and code. It does **not** establish that either function is the intended one — that is the oracle's role, and the oracle shares no code with either path.

**Zero diagnostics is not the same as a proven-capable instrument.** Oracle and adjudicator capability were verified separately by injecting all seven outcome classes, including `SIGMOID → r=0.12` (outside the proven range) and `SIGMOID → r=0.90`. Both correctly classified `CONTRADICTS_PROVEN_RANGE` rather than reading as policy findings.

## 5. Implementation defect found and fixed during this run

The first harness run crashed with `TypeError` in `adjudicate`. Cause: `probe_a4_boundary` returns `None` when an arm assigns no `L0` at all, and the `A4` record passed `None` into the score fields.

This is an implementation result, not a licence to adapt the specification. Fixed by classifying the empty frontier as `FRONTIER_EMPTY` — an observation that the arm's `L0` region is empty — rather than crashing or coercing a value. Recorded rather than cleaned silently.

## 6. Provenance — this ledger belongs to this code

| File | sha256 |
|---|---|
| `frozen.py` | `5b8ceb43e36e689c3f686d4eafc630217bb7bb35b09dec9d535119b0f364c380` |
| `engine.py` | `05f959dafcde1837345eefba9f16d4331bca058bae012b2428e7231c998e5aa0` |
| `instruments.py` | `7572e535591d6748f575d7197fdf166c760fe7e4681fda14fed004975e71f385` |
| `run.py` | `e239c0307a10f05b4f461005bc7ddaa9c293edb0f35841ac9b6dd58844dc49da` |
| `result.json` | `46523a143aefb9ccf293335c2abff94310e5b0a256ddf4a774c21baa0670e9c6` |

Frozen configuration, with provenance rather than assertion:

| Constant | Value | Origin |
|---|---|---|
| weights | `[0.2, 0.3, 0.3, 0.1, 0.1]` | submitted prototype `AdaptiveRiskEngine` default — **not a design choice** |
| γ | `0.15` | submitted prototype, hardcoded; the prose carries γ as a free parameter |
| thresholds | `[0.30, 0.65, 0.85]` | design prose §3 |

## 7. Reproduce

```bash
cd proposals/SD-05-D3-IMPLEMENTATION
python3 run.py > result.json
shasum -a 256 result.json   # must equal the digest above
```

## 8. What this run does not establish

- **Not** that the scheme is unsafe. It falsifies P **for this adversary set under the CLAMP arm**.
- **Not** that SIGMOID is safe. It is non-discriminating.
- **Not** that the policy holds generally. Two counterexamples exist; they do not bound the rest.
- **Not** anything about `D1a`/`D1b` being repaired. Both remain open.
- **Not** a success rate, a detection rate, or a security score. `2` findings across 14 records is a count, not a proportion with meaning.