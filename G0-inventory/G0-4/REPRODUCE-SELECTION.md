# G0-4 — Population Definition for `METRICS_REPRODUCE`

**Date**: 2026-10-02, branch `audit/g0-estate`
**Phase**: population definition. This document defines the selection predicate **before** it is applied to any repository.
**Status**: G0 remains OPEN. Nothing here is a reproducibility conclusion.

---

## 1. Population

Verified against `snapshot.json` (G0-1, `16c6aca`). The three buckets are **disjoint** — zero intersection in every pairwise check.

| Bucket | Count | Basis |
|---|---|---|
| Exact identity (P1 inheritances) | **7** | `RESOLVED_EXACT` |
| Content-inspected | **121** | 119 `AMBIGUOUS` + 2 explicit targets (`sentinelx`, `biohealy-ipn`, both `NO_CANDIDATE_SURFACED`) |
| Remaining | **406** | `NO_CANDIDATE_SURFACED` minus the 2 explicit targets |
| **Total** | **534** | |

## 2. The selection question

> Does there exist a **published quantitative metric or computational result whose regeneration can be checked from the artifacts currently available**?

This is a conjunction, and it separates into two independently testable conditions:

- **A — a published claim exists**
- **B — regeneration is checkable from artifacts currently available**

Explicitly **not** selection criteria: apparent importance, size, star count, visibility, public/private status, whether it "looks scientific", or whether a number looks suspicious.

## 3. Predicate — mechanical definition

### 3.1 Condition A — `PUBLISHED_CLAIM`

Satisfied if **either**:

- **A1 (tree evidence).** The file tree contains a claim-bearing path matching
  `(result|metric|benchmark|eval|experiment|performance|report|ablation|accuracy|figure)` with a data/document extension
  (`.json .csv .tsv .md .txt .log .yaml .yml .npy .npz .mat .pkl .tex .pdf`),
  **or** a manuscript path (`*.tex`, `*.pdf`).
- **A2 (document evidence).** The README contains a quantitative claim: a number
  co-occurring with a metric token or a unit
  (metric vocabulary: `accuracy|auc|auroc|precision|recall|f1|latency|ms|throughput|error|rmse|mse|mae|bleu|rouge|perplexity|baseline|benchmark|score|rate|ratio|loss|reward|iter|itr|wps|power|mw|w/|db|snr|psnr|ssim|iou|fid|map`)
  (unit vocabulary: `%|\bms\b|\bmw\b|\bwatt|\bdb\b|\bmbps\b|\bdpi\b|\bhz\b|\bkhz\b|\bgb\b|\bmb\b|\bfps\b`).

### 3.2 Condition B — `REGENERATION_CHECKABLE`

Three objective elements, checked in this order. The **first** absent element is the one reported.

| ID | Element | Test |
|---|---|---|
| **B1** | Execution chain | Dependency or build manifest present: `requirements*.txt`, `pyproject.toml`, `setup.py`, `environment.yml`, `package.json`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Makefile`, `CMakeLists.txt`, `Dockerfile`, `*.cabal`, `Gemfile` |
| **B2** | Input artifact | Data present, or an acquisition path: `data/`, `dataset/`, `datasets/`, files with extensions `.csv .tsv .npy .npz .mat .pkl .h5 .hdf5 .parquet .arrow .jsonl`, or an acquisition script (`download*.{py,sh}`, `fetch*.{py,sh}`, `get_data*.py`) |
| **B3** | Execution instruction | Any of: (a) README contains a run/usage/install section heading; (b) a **dedicated instruction document** exists — `REPRODUCE.md`, `REPRODUCE.txt`, `RUN.md`, `USAGE.md`, `INSTRUCTIONS.md`, `HOWTO.md`, `QUICKSTART.md`, `GETTING_STARTED.md`; (c) a probable entrypoint script exists (`main.py`, `run.py`, `train.py`, `evaluate.py`, `experiment.py`) |

B3(b) was **added after validation found it missing**. See §5.1.

### 3.3 Classification

```text
A false                    -> NO_PUBLISHED_CLAIM
A true, B1/B2/B3 present   -> REPRODUCE_ELIGIBLE
A true, some element absent -> REPRODUCE_NOT_YET_ELIGIBLE
                               + the single missing element named
```

`NO_PUBLISHED_CLAIM` means there is nothing to reproduce. It is **not** a reproducibility verdict and **not** a judgement of the repository's value.

## 4. What this predicate deliberately does not do

- It does not judge whether a claim is **correct**. That is `CLAIM_CORRESPONDS`, a separate layer.
- It does not attempt regeneration. Eligibility means *an attempt is warranted*, nothing more.
- It does not rank. No score, no ordering by merit.

## 5. Known limits of this predicate, recorded before the run

These are properties of the instrument, stated in advance so a later reader does not have to reverse-engineer them from a failure.

### 5.1 `INCOMPLETE-MARKER-VOCABULARY` — third occurrence, found by validation

The first implementation of B3 tested only README section headings and a closed basename whitelist for entrypoints. Applied to the three wave-1 repositories — the one set where independent inspection had already verified that **every published figure traces exactly** — it misclassified **2 of 3** as `REPRODUCE_NOT_YET_ELIGIBLE`, missing element `EXECUTION_INSTRUCTION`.

Two independent causes:

1. **A dedicated reproduction-instruction document was not recognised at all.** All three repositories contain `REPRODUCE.md` — the most explicit execution instruction a repository can carry, named for the purpose. The predicate had no term for it.
2. **The entrypoint test was a closed basename whitelist.** `main.py`, `run.py`, `train.py`, `evaluate.py`, `experiment.py` matched. `src/simulator.py` and `src/pipeline_loso_itr.py` are equally real entrypoints and did not.

This is the **third recorded instance of the same defect class** in this audit, after the scaffold detector (`INCOMPLETE-MARKER-VOCABULARY`, 0 found against an actual 16). The consistent finding across all three is that **the vocabulary is the defect, not the code**. Every marker list in this audit is now published in the specification above so that it can be checked rather than trusted.

Had the predicate been applied to the 406 remaining repositories before validation, the error would have been systematic and would have looked like a result.

**Scope of the fix.** B3(b) adds dedicated instruction documents. It was **not** fixed by broadening to "any executable file exists", which would make B3 nearly vacuous and destroy its ability to distinguish a repository whose execution chain is discoverable from one where it is not.

**Validation remains partial.** The three wave-1 repositories all contain `data/metrics.json`, so they exercise B2 only through its data-file branch. **The self-contained case — a regeneration requiring no external data — has no representation in the available ground truth.** B2 will classify such a repository `REPRODUCE_NOT_YET_ELIGIBLE` on a missing `INPUT_ARTIFACT` that is in fact not needed. That is an over-classification of unknown size, resolvable only at execution, and it is recorded rather than guessed away.

**L1 — Structural absence is not claim absence.** A repository can publish a benchmark table in its README with no results file in the tree. A1 and A2 exist to catch this, but A2 is a regex over one document. Absence of A1 **and** A2 at README depth is **not** proof that no claim exists. Such repositories are recorded as `NO_PUBLISHED_CLAIM` **at this inspection depth**, and the phrase is not allowed to harden into "publishes nothing."

**L2 — Only the README and the tree are inspected.** Claims in issues, wikis, releases, notebooks, or external papers are invisible to this predicate.

**L3 — Credential and configuration blockers are not mechanized.** A repository requiring an API key, a dataset licence, paid access, or proprietary hardware cannot be detected by any of B1–B3. Such repositories may be classified `REPRODUCE_ELIGIBLE` and then fail at execution. **That failure is a `NOT_ATTEMPTED` execution outcome, never a mismatch.**

**L4 — Vocabulary is hand-maintained.** This is the `INCOMPLETE-MARKER-VOCABULARY` defect class, already recorded twice in this audit. A metric vocabulary that does not contain a term produces a confident negative. The vocabulary is published above so it can be checked, and the count of `NO_PUBLISHED_CLAIM` is expected to be an over-count by an unknown amount.

**L5 — Scaffold and empty repositories.** Generic scaffolds and empty repositories are objects in their own right. A scaffold is not a reproduction candidate; an empty repository has no artifact to reproduce. Both must be classified by inspection, not by the predicate.

## 6. Execution rule, fixed in advance

> **A failed execution never counts as a mismatch automatically.**

The order is fixed:

1. Classify the execution failure (environment, missing dependency, missing dataset, missing credential, timeout, crash, or genuine numerical divergence).
2. Only if the classification is genuine numerical divergence does a mismatch exist.
3. Anything else yields `NOT_ATTEMPTED` or `EXECUTION_BLOCKED`, which is a statement about the attempt, never about the published result.

This exists so that "I could not reproduce it" cannot silently become "the result is false."

## 7. Records to produce

- This document, unchanged, as the predicate of record.
- `predicate.py` — the implementation, containing the vocabulary above and no others.
- `G0-4-REPRODUCE-POPULATION.md` — the classified population, with per-repository missing element named.
- The raw observation payload, gitignored, with digests retained.

## 8. Provenance

### 8.1 Wave-1 payload recovered — `UNRETAINED-OBSERVATION-PAYLOAD` closed

G0-3 wave 1 retained **no raw payload and no digests**. Its observation could not be re-derived from retained evidence, so every figure in `G0-3-WAVE1-RESEARCH.md` was unre-verifiable. Wave 2 retained digests; wave 1 did not.

The three wave-1 repositories were re-collected on 2026-10-02 to serve as the predicate's validation set. The re-collection **regenerated the wave-1 inventory identically** — 15, 15 and 18 files — so the wave-1 observation is now confirmed reproducible rather than merely asserted to have been.

| File | sha256 |
|---|---|
| `raw/wave1.json` | `fec615e98b76a2f0586c47123126ef717ddfa81e4037c304def6befa11127176` |

This is the audit's own version of the failure it detects elsewhere: an artifact whose evidence was not retained could not be checked by anyone, including by the auditor.