# SD-01 / SD-02 / SD-03 — Reproduction Adjudication

**Date**: 2026-10-02 · **Branch**: `publications/2026-board`
**Protocol**: `REPRODUCE.md` executed literally, per package — `venv`, `pip install -r requirements.txt`, `pytest tests/ -q`, `python src/<entry>.py`
**Result**: two `REPRODUCED`, one that **does not fit the frozen ladder**

---

## 1. Verdicts

| Package | commit | tests | `metrics.json` | Verdict |
|---|---|---|---|---|
| **SD-01** ISCMI | `78a646b` | 3 passed | **byte-identical** | `REPRODUCED` |
| **SD-02** INCC | `1879f91` | 2 passed | **byte-identical** | `REPRODUCED` |
| **SD-03** ICCIT | `ab4b445` | 2 passed | differs in 3 fields | **see §3** |

## 2. What `REPRODUCED` means here, and what it does not

For SD-01 and SD-02 the regenerated artifact is byte-identical to the committed one. That is the strongest form of the verdict: the numbers published in `paper/main.tex` are the numbers the committed code produces.

It does **not** establish that the packages are clinically valid, scientifically adequate, or ready to submit. Both packages say so themselves in `REPRODUCE.md` — a breast-cancer dataset used as a *methodological proxy*, and a PCA prototype that *must not be reported as* trained Deep JSCC. That self-disclosure is correct and is preserved.

## 3. SD-03 — the frozen ladder has no outcome for this case

### 3.1 What happened

The execution **succeeded**. No crash, no missing dependency, no timeout. The artifact differs in three fields and matches in every other.

| Field | Committed | Regenerated | Depends on wall clock? |
|---|---|---|---|
| `accuracy` per subject | 0.25 / 0.375 / 0.30 / 0.375 | **identical** | no |
| `mean_accuracy` | 0.325 | **identical** | no |
| `latency_ms` per subject | ~6.44 – 6.60 | ~3.18 – 3.27 | **yes** |
| `itr_bits_min` per subject | 3.2768 / 0.5505 / 3.2762 | 3.2871 / 0.5524 / 3.2874 | **yes, indirectly** |
| `mean_latency_ms` | 6.517107290710555 | 3.2245635624875035 | **yes** |
| `mean_itr_bits_min` | 1.7758821146395407 | 1.7817153481297185 | **yes, indirectly** |

### 3.2 The mechanism, proved rather than inferred

`src/pipeline_loso_itr.py:18-24,126`:

```python
def calculate_itr(num_classes, accuracy, trial_seconds):
    bits = math.log2(num_classes) + accuracy*math.log2(accuracy) \
         + (1-accuracy)*math.log2((1-accuracy)/(num_classes-1))
    return bits * 60.0 / trial_seconds

results.append({..., "itr_bits_min": calculate_itr(4, accuracy, 1.0 + latency/1000)})
```

`itr_bits_min` is a direct function of measured latency. Recomputing ITR from the regenerated accuracy and regenerated latency reproduces every regenerated ITR **to within 1e-12**. The difference is fully explained by a machine roughly twice as fast on the latency measurement, with the ITR moving slightly *up* because faster trials yield more bits per minute.

Nothing here diverges about the method.

### 3.3 Why none of the three frozen outcomes fits

| Outcome | Why it does not apply |
|---|---|
| `REPRODUCED` | two published numbers did not regenerate |
| `NUMERIC_MISMATCH` | there is no divergence about the result; the difference is a property of the hardware |
| `EXECUTION_FAILURE` | the execution succeeded |

**The ladder is missing an outcome for: execution succeeded, deterministic metrics reproduced exactly, environment-dependent metrics differ.**

That gap is recorded rather than closed by force-fitting a wrong bucket. Choosing `NUMERIC_MISMATCH` would assert a result divergence that does not exist; choosing `REPRODUCED` would hide that published numbers did not regenerate; choosing `EXECUTION_FAILURE` would misdescribe a successful run.

**Working label, explicitly not part of the frozen ladder:** `REPRODUCED_WITH_ENVIRONMENT_DEPENDENT_FIELDS`.

## 4. The submission-relevant finding

`data/metrics.json` places deterministic results and machine-dependent measurements **in one artifact under one reproduction claim**. From the published figures, `mean_latency_ms 6.5171073` and `mean_itr_bits_min 1.7758821` appear in the manuscript as results.

**Those two numbers are properties of the machine that produced them.** A reviewer on different hardware regenerates different published values, with no defect in the method and no error in the code.

Three options, none selected here:

1. **Report the deterministic metrics only**, and state latency as environment-characterised rather than as a result.
2. **Publish the measurement environment** alongside any wall-clock figure, so the number is interpretable.
3. **Keep both**, with the clock-dependent fields explicitly marked non-reproducible.

Option 1 is the one the package's own `REPRODUCE.md` already gestures at — *"benchmark GPU/CPU latency after warm-up"* — but it stops at measurement and does not address reproducibility of the figure.

## 5. Environment, recorded for provenance

| | |
|---|---|
| Python | 3.13.13 |
| Why not 3.14 | `scikit-learn` and `torch` publish **no `cp314` macOS wheels**; 3.13 resolves to wheels |
| numpy | 2.5.3 |
| scikit-learn | 1.9.1 (SD-01, SD-02) |
| torch | 2.14.1 (SD-03) |
| SD-01 / SD-02 venv | **shared** — their dependency sets are identical, so the comparison across the two uses one environment |
| SD-03 venv | separate, because of `torch` |

Digests for the committed and regenerated artifacts are in `reproduction_ledger.json`.

## 6. Non-claims

- Two `REPRODUCED` verdicts say nothing about clinical validity, scientific adequacy, or venue readiness.
- The SD-03 environment finding is **not** a defect in the method and **not** an instrument defect in this audit. It is a claim-structure issue in the artifact.
- No package was executed against its published PDF in this pass; the comparison is artifact-to-artifact.
- No package was modified. All three clones were read-only runs in a scratch directory.
- `SD-05` was not touched, and `0693f3f` remains frozen.