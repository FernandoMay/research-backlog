# G0-3 — Content Inspection, Wave 1

**Scope:** the 3 owner-promoted research repositories.
**No repository was modified.** Inspection was read-only via the GitHub API; nothing
was cloned and no branch, README, artifact or release was touched.

---

## 1. Method

Inspected via `git/trees?recursive=1` for structure and `contents/` for file content.
No clone, no execution. **Reproduction is therefore NOT established by this document.**

Established per repository: file inventory, dominant language, artifact contents,
document claims, and whether artifact ↔ document correspond.

---

## 2. Observed inventory

| repository | files | largest | language | description |
|---|---:|---|---|---|
| `iscmi-01-fuzzy-conformal` | 15 | `paper/main.pdf` 78 807 B | TeX | *(empty)* |
| `incc-2026-semantic-jscc` | 15 | `paper/main.pdf` 76 597 B | TeX | *(empty)* |
| `iccit-2026-bci-transformer-swarm` | 18 | `paper/main.pdf` 74 772 B | Python | *(empty)* |

All three: `REPRODUCE.md`, `CITATION.cff`, `Dockerfile`, `requirements.txt`,
`data/metrics.json`, `tests/`, `src/`, `paper/`, `pres/`. All seeded
`20260915`. All three have **empty GitHub descriptions**.

---

## 3. Correspondence: artifact ↔ document

Every numeric claim in the README and the paper abstract traces to
`data/metrics.json` exactly.

| repository | claim | artifact key | value | match |
|---|---|---|---|---|
| SD-01 | Brier 0.0210 | `baseline_brier` | 0.0209722 | ✅ |
| SD-01 | ECE 0.0226 | `baseline_ece` | 0.0226496 | ✅ |
| SD-01 | coverage 93.86% | `fuzzy_coverage` | 0.9385965 | ✅ |
| SD-01 | width 0.1759 | `fuzzy_mean_interval_width` | 0.1758595 | ✅ |
| SD-02 | 83.89% @ 0 dB | `snr.0.semantic_accuracy` | 0.8388889 | ✅ |
| SD-02 | 90.83% @ 2 dB | `snr.2.semantic_accuracy` | 0.9083333 | ✅ |
| SD-02 | 97.78% @ 10 dB | `snr.10.semantic_accuracy` | 0.9777778 | ✅ |
| SD-02 | 12.5% dimensions | `bandwidth_ratio` | 0.125 | ✅ |
| SD-03 | LOSO 32.5% | `mean_accuracy` | 0.325 | ✅ |
| SD-03 | 6.52 ms | `mean_latency_ms` | 6.5171073 | ✅ |
| SD-03 | 1.78 bits/min | `mean_itr_bits_min` | 1.7758821 | ✅ |

**The artifact ↔ document correspondence chain is intact in all three.** This is the
opposite of several P1 packages.

---

## 4. Finding — the documents are more conservative than the external narrative

The drift is **not** inside the repositories. It is entirely in the
`SECONDARY_SOURCE` archived at `df53d43`.

| | README says | paper says | secondary source says |
|---|---|---|---|
| SD-01 | "transparent **methodological baseline**" | "These results are **not clinical validation**; they demonstrate the **executable protocol**" | "**Package Ready**", "**congelado para submission**" |
| SD-02 | "transparent semantic latent **baseline** … clearly separates the prototype from **future** Deep JSCC training" | "raw baseline achieves **100%** … a measurable bandwidth–accuracy trade-off, **not a universal advantage**" | "**Package Ready**" |
| SD-03 | "synthetic proxy is **only a software validation harness**" | "a **pipeline validation, not a human-EEG result** … establishes the protocol **required before** a public EEG dataset can be used" | "**Package Ready**", "primera fase **100% completada**" |

Two specific overstatements in the source, neither present in any repository document:

1. **SD-01 — the reported metrics belong to the baseline, not the method.** The source
   presented Brier 0.0210 and ECE 0.0226 as the fuzzy method's results. The artifact
   labels them `baseline_brier` / `baseline_ece`. The artifact also contains
   **`fuzzy_ece = 0.0297`, which is worse than `baseline_ece = 0.0226`** — and the
   source never mentions it. The paper attributes the numbers to "the baseline
   classifier" in the same sentence. Correct in the repository; misattributed in the
   narrative.

2. **SD-02 — the raw baseline scores 100%.** `raw_accuracy` is `1.0` at every SNR.
   The paper says so explicitly: *"the raw baseline achieves 100%."* The source
   omitted this while praising the 83.89% figure as an achievement. The paper frames it
   as a loss against a perfect baseline; the narrative framed it as a result.

---

## 5. What the documents themselves disclose

Recorded because these are the self-limiting statements that P1 consistently found to
be the most accurate content in a package.

- SD-01 artifact: `"sklearn breast_cancer proxy; not clinical validation"`.
- SD-02 artifact: raw baseline at `1.0`; `latent_dim` 8 against `features` 64.
- SD-03 artifact: `"synthetic BCI proxy; not human EEG validation"`, and
  **subject 0 scores exactly chance — `accuracy 0.25`, `itr_bits_min 0.0`** — while
  subjects 1–3 score 0.375 / 0.30 / 0.375.

The per-subject spread in SD-03 is disclosed in the artifact and not smoothed in the
paper.

---

## 6. Layered state after inspection

| layer | SD-01 | SD-02 | SD-03 |
|---|---|---|---|
| EXISTENCE | **VERIFIED** | **VERIFIED** | **VERIFIED** |
| VISIBILITY | **VERIFIED** | **VERIFIED** | **VERIFIED** |
| CONTENT | **VERIFIED** | **VERIFIED** | **VERIFIED** |
| METRICS_REPRODUCE | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** |
| NUMERIC CLAIMS | **VERIFIED — traced to artifact** | **VERIFIED — traced to artifact** | **VERIFIED — traced to artifact** |
| CORRESPONDENCE | **CONSISTENT** | **CONSISTENT** | **CONSISTENT** |
| EXTERNAL TEXT | **DRIFTED** | **DRIFTED** | **DRIFTED** |
| SCIENTIFIC VALIDITY | not assessed | not assessed | not assessed |

**`METRICS_REPRODUCE` remains `NOT VERIFIED` for all three.** Tracing a number to an
artifact establishes that the document describes the artifact. It does not establish
that the code regenerates it. That requires execution, which was not performed.

---

## 7. Bearing on the materialization question

The question at the end of the radar — *does a new research repository need to
exist?* — is now answerable for SD-03.

**No.** SD-03 already contains the LOSO pipeline, the spatial attention encoder, the
Transformer swarm, the Wolpaw ITR, measured latency, **and** both PhysioNet scripts
(`scripts/download_physionet.py`, `scripts/preprocess_physionet.py`). The paper states
it "establishes the leakage-safe evaluation protocol required before a public EEG
dataset can be used".

Creating a repository for this research would be duplication, not progress. This is
the concrete case the user anticipated.

---

## 8. Remaining G0-3 scope

| group | count | status |
|---|---:|---|
| promoted research repositories | 3 | **done, this document** |
| `AMBIGUOUS` repositories | 119 | not started |
| `SentinelX` | 1 | not started |
| `BioHealy` | 1 | not started |

**124 repositories remain.** None has been inspected. The protocol is now established
and tested; scaling it to the `AMBIGUOUS` set is mechanical but must preserve the two
safeguards — per-member evidence, and the ability to conclude **no relation**.