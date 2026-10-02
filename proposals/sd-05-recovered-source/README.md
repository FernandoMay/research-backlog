# Recovered Design Intent — SD-05

**Status**: **RECOVERED / NON-PRIMARY ARTIFACT**
**This is not a contemporaneous normative specification.**
**Recovery date**: 2026-10-02 · **Branch**: `publications/2026-board`

---

## 1. What this file is, and what it is not

| | |
|---|---|
| **Source** | conversation transcription supplied by the author during the 2026-10-02 audit session |
| **Nature** | recovered evidence of design intent |
| **Status** | **recovered / non-primary** |
| **NOT** | a specification that existed alongside the implementation |
| **NOT** | contemporaneous with the code it describes |

The original SD-05 design text was **never versioned as an artifact in this repository**. It reached this audit only as a transcription in conversation. This file preserves that transcription **as recovered** — not cleaned, not normalised, not corrected, not reordered — so that the chain can distinguish unambiguously between:

- what was documented **at the time of design**, and
- what was **recovered afterwards as evidence of intent**.

## 2. Preservation

| | |
|---|---|
| File | `RECOVERED-TRANSCRIPT.md` |
| sha256 | `c66f7fdb73b262110cef31e668223321c6df8f559cb714fc9d32be4f49410fec` |
| Lines | 66 |
| Sections preserved | risk engine and threshold table; the submitted `AdaptiveRiskEngine`; the adversary matrix; the receipt JSON's risk fields |

Sections not bearing on the risk function were omitted. **What was omitted is recorded as omitted** — this file is a partial recovery of a partial source, not a complete design document.

## 3. What the recovered text establishes

Recovered verbatim in `RECOVERED-TRANSCRIPT.md`:

1. **Codomain** — *"definimos la función de escalado de riesgo no lineal $r_i \in [0,1]$"*
2. **Normative thresholds** — a table mapping `{0.30, 0.65, 0.85}` to named enforcement mechanisms with stated latency and on-chain cost
3. **No calibration claim** — the text says *"función de escalado de riesgo"* and contains no calibration, reliability or probability language
4. **Slope unspecified** — the formula writes bare $\sigma$ with no steepness parameter; only $\gamma$ is named, and as a free parameter with no stated value
5. **Submitted code** — `compute_risk` returns `min(max(raw_score, 0.0), 1.0)`, a clamp, with weights `[0.2, 0.3, 0.3, 0.1, 0.1]` and `gamma = 0.15` hardcoded

These are the five facts on which the selection at `41fdc4b` rests.

## 4. Limits of this recovery

- **No digest existed at design time.** There is no contemporaneous hash to compare against. This file's digest proves *what was recovered and when*, not that it is faithful to an original.
- **Single source, no corroboration.** No second copy of the design text exists in the repository, in issues, or in releases. A transcription is evidence of what was said, not of what was specified.
- **Partial.** Only the sections bearing on the risk function were preserved.
- **The selection it supports is therefore qualified**, and carries the qualification in its own label: *"a repair selected by preservation of documented normative properties, under an incomplete primary source."*

## 5. Effect on `41fdc4b`

This file **strengthens** that selection's provenance without altering it. The chain can now name, separately and unambiguously:

| | |
|---|---|
| **Documented at design time** | codomain $[0,1]$; thresholds $\{0.30, 0.65, 0.85\}$; slope unspecified |
| **Recovered afterwards as evidence of intent** | the transcription in `RECOVERED-TRANSCRIPT.md`, sha256 `c66f7fdb…`, recovered 2026-10-02 |
| **Explicitly not established** | that $f_C$ is the historically intended function; that B is wrong; that $f_C$ is better |

## 6. Outstanding

The underlying defect is **not** closed by this file. The correct repair is to produce a genuine versioned specification going forward, authored as a specification rather than reconstructed as evidence. That is a separate act and is not begun.

Until then, the documentary chain carries this label wherever it is cited:

```text
RECOVERED DESIGN INTENT
SOURCE: conversation transcription
STATUS: recovered / non-primary artifact
NOT: contemporaneous normative specification
```