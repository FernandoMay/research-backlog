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
| **B2** | Input artifact | **Not a blocker — a flag.** Data present, or an acquisition path: `data/`, `dataset/`, `datasets/`, files with extensions `.csv .tsv .npy .npz .mat .pkl .h5 .hdf5 .parquet .arrow .jsonl`, or an acquisition script (`download*.{py,sh}`, `fetch*.{py,sh}`, `get_data*.py`). When absent on a claim-bearing repository, the classification carries `INPUT_ARTIFACT_ABSENT` into execution rather than being downgraded. See §9.1. |
| **B3** | Execution instruction | Any of: (a) README contains a run/usage/install section heading; (b) a **dedicated instruction document** exists — `REPRODUCE.md`, `REPRODUCE.txt`, `RUN.md`, `USAGE.md`, `INSTRUCTIONS.md`, `HOWTO.md`, `QUICKSTART.md`, `GETTING_STARTED.md`; (c) a probable entrypoint script exists (`main.py`, `run.py`, `train.py`, `evaluate.py`, `experiment.py`) |

B3(b) was **added after validation found it missing**. See §6.1.

**A `REPRODUCE.md` is candidate documentation, not evidence of reproducibility.** Its presence makes the execution chain *discoverable*, which supports eligibility for an attempt. It does not establish that the repository is reproducible, that its instructions are correct, or that its published results can be regenerated. A repository may ship a `REPRODUCE.md` and still fail to execute; that failure is `EXECUTION_FAILURE`, never `NUMERIC_MISMATCH`.

### 3.3 Classification

```text
A false                      -> NO_PUBLISHED_CLAIM
A true, B1 and B3 present    -> REPRODUCE_ELIGIBLE  (+ INPUT_ARTIFACT_ABSENT flag if B2 absent)
A true, B1 or B3 absent      -> REPRODUCE_NOT_YET_ELIGIBLE  (+ the missing element named)
```

### 3.4 What `REPRODUCE_NOT_YET_ELIGIBLE` means, and what it does not

It means, narrowly:

> **The available inventory does not yet contain sufficient evidence to justify a reproduction attempt under the current protocol.**

It does **not** mean:

- that the repository cannot be reproduced
- that "we do not know how to reproduce it"
- that no reproduction is possible in principle
- anything about whether the published result is correct

The distinction is load-bearing. `NOT_YET_ELIGIBLE` is a statement about **the inventory**, not about the science. Eligibility is re-evaluated whenever new evidence appears.

`NO_PUBLISHED_CLAIM` means no published quantitative claim was found at the inspected depth. It is **not** a reproducibility verdict and **not** a judgement of the repository's value.

## 4. Execution ladder

Once a repository is `REPRODUCE_ELIGIBLE`, execution resolves to exactly one of:

```text
REPRODUCE_ELIGIBLE
   ↓
execution
   ├── REPRODUCED           published figure regenerated within tolerance
   ├── NUMERIC_MISMATCH     genuine numerical divergence
   └── EXECUTION_FAILURE    environment, dependency, dataset, credential, timeout, crash
```

**`EXECUTION_FAILURE` is independent of `NUMERIC_MISMATCH` and must never be collapsed into it.** A repository that fails because a dataset is unavailable has produced no information about whether its published result is correct. The order is fixed:

1. Classify the execution failure.
2. Only genuine numerical divergence is a mismatch.
3. Everything else is `EXECUTION_FAILURE`, a statement about the attempt and never about the result.

This exists so that "I could not reproduce it" cannot silently become "the result is false."

## 5. What this predicate deliberately does not do

- It does not judge whether a claim is **correct**. That is `CLAIM_CORRESPONDS`, a separate layer.
- It does not attempt regeneration. Eligibility means *an attempt is warranted*, nothing more.
- It does not rank. No score, no ordering by merit.

## 6. Known limits of this predicate — stated before the run, amended by what the run found

Stated in advance so a later reader does not have to reverse-engineer them from a failure. §6.1 was confirmed and extended by validation; §9 records what validation then found that was not anticipated here.

### 6.1 `INCOMPLETE-MARKER-VOCABULARY` — third occurrence, found by validation

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
---

## 9. Defects found by the self-contained ground truth

The first ground truth (wave 1, 3 repositories, all data-backed) could only exercise the data-backed branch of B2. A second ground truth was built specifically to cover classes that could break the predicate. It found **three further defects**, two of them in the permissive direction — the direction that manufactures findings.

### 9.1 B2 — self-contained regeneration was a false negative

`fcstn`: 172 files, **zero data files**, and `RUN_RESULTS.md` publishing `22 passed in 458.39s` plus metric-tensor curvature results. `mandelbrot.py` computes from hardcoded parameters (`center=(-0.5, 0.0)`) against numpy/cupy alone.

Ground truth: **`REPRODUCE_ELIGIBLE`**. Predicate: `REPRODUCE_NOT_YET_ELIGIBLE` on a missing `INPUT_ARTIFACT` that was never needed.

**Cause.** B2 tested "is a data file present" and read absence as "data is required." Absence of a data file does not establish that external data is required — that is an *execution* question.

**Fix.** B2 became a **flag, not a blocker**. A claim-bearing repository with B1 and B3 present is `REPRODUCE_ELIGIBLE` and carries `INPUT_ARTIFACT_ABSENT` into execution, where a genuinely missing dataset becomes `EXECUTION_FAILURE`.

Before this fix, `INPUT_ARTIFACT` was absent on **116 of 121** inspected repositories — 96%. That was never a finding. It was a prediction that B2 was wrong.

### 9.2 A2 — mass false positives on web and mobile repositories

The first metric vocabulary matched:

| Repository | Matched | What it actually was |
|---|---|---|
| `rescueM` | `Map` | a navigation screen (`map` was meant for mAP) |
| `fg-supply` | `AppColors.error` | a Dart colour constant |
| `travelai` | `Ratio` | the CSS property "Aspect Ratio" |
| `spaceverses` | `Ratio` | identical |

A bare `\d+` additionally matched hex colours and version numbers anywhere in a 10 KB README. The predicate was not selecting repositories with published claims; it was selecting **web and mobile templates**.

**Fix.** Vocabulary restricted to terms unambiguous in a README; `mAP`, `F1`, `PSNR`, `SSIM`, `BLEU`, `IoU` matched **case-sensitively**; a metric term now counts only when a number appears **within 40 characters** and a result-like unit appears nearby. A bare number is not a result.

Effect on the inspected population: `REPRODUCE_ELIGIBLE` fell from **24 to 8**. All 24 had been A2 false positives.

### 9.3 A1 — assets, foreign uploads, and issue templates counted as claims

| Repository | Path that fired | What it actually was |
|---|---|---|
| `workspace-63c46920-…` | `upload/FG Supply.pdf` | a document belonging to a **different project** |
| `dsltech` | `assets/images/doc.pdf` | a UI image asset |
| `smart-contract-auditor` | `.github/issue_template/bug_report.md` | a GitHub issue template |

**Cause.** Any `.tex`/`.pdf` anywhere counted as a manuscript, and the token `report` matched a GitHub issue template.

**Fix.** Vendored, template and asset locations are excluded outright (`.github/`, `node_modules/`, `assets/`, `upload/`, `ios/`, `android/`, `build/`, `dist/`, …), and a manuscript must sit at a paper-like path (`paper/`, `latex/`, `manuscript/`, `main.tex`, `*paper.*`).

Effect on the inspected population: `REPRODUCE_ELIGIBLE` fell from **8 to 3**.

### 9.4 B3 — residual, and deliberately not fixed

A repository whose only entrypoint has a non-standard name and which ships no instruction document is classified `REPRODUCE_NOT_YET_ELIGIBLE`. Example: `requirements.txt` + `mandelbrot.py` + a README with no usage section.

**Not fixed**, because the alternative — treating any executable file as an instruction — makes B3 vacuous and destroys its ability to distinguish a discoverable execution chain from an undiscoverable one. This is the same vocabulary defect a fifth time, and it is left standing with its exact trigger recorded rather than papered over.

### 9.5 `SEARCH-API-UNUSABLE` — code search returns confident zeros

GitHub code search returned **0** for `filename:REPRODUCE.md+owner:FernandoMay` and **0** for `repo:FernandoMay/xing-adan-resilience`, which the tree API shows has **18 blobs**. The token carries `repo` scope; the tree API works on the same repository.

**Consequence.** The conclusion "the estate contains no notebooks" is **not obtainable** by this route and was not drawn. Candidate discovery for the notebook class was done from `language == "Jupyter Notebook"` in the snapshot instead, which located 5 repositories.

A search endpoint returning 0 for content that demonstrably exists is the same species as a detector returning 0 for a scaffold: a confident negative from an unvalidated instrument.

## 10. Precision, recall, and the direction of error

The predicate is deliberately **biased toward the restrictive direction**, and the asymmetry is the justification:

| Error | Consequence |
|---|---|
| False `REPRODUCE_ELIGIBLE` | manufactures an execution attempt; can manufacture a finding about a result that was never testable |
| False `REPRODUCE_NOT_YET_ELIGIBLE` | defers work; the repository can be re-evaluated when evidence appears |

A known probable false negative is recorded rather than fixed: **`mirailand`** ships `docs/6im1_mirai_final.pdf` and `docs/mirai onepager.pdf`, which look like a manuscript and a one-pager. Under §9.3 neither fires, because a manuscript must now sit at a paper-like path. `mirailand` is a candidate for manual review.

## 11. Cross-repository artifact duplication

Two Z.ai scaffold workspaces contain artifacts belonging to **`fg-supply`**:

- `workspace-63c46920-…` — `upload/FG Supply.pdf`, plus four UI screenshots (`Calculadora.jpg`, `Dashboard.jpg`, `Login.jpg`, `Menú expandido.jpg`)
- `workspace-81c65fbf-…` — `upload/FG Supply.pdf`

The `fg-supply` artifacts therefore exist in at least three repositories. Excluding `upload/` from A1 is correct — files fed into an AI coding session are not claims *of that repository* — but the duplication is a structural fact about the estate: **a claim-bearing artifact is not necessarily owned by one repository**, and identity resolution over artifacts must not assume otherwise.

---

## 12. Operational invariants for the 406-repository run

`9db4494` is the **frozen selection instrument**. It is not a reproducibility test, and running it produces no reproducibility result.

### 12.1 Four invariants

1. **The predicate does not modify repositories.** Read-only via API. Nothing cloned, nothing written, no repository altered.
2. **The 406 are classified, not executed.** No reproduction attempt occurs in this phase. Classification is an inventory judgement, never an execution outcome.
3. **`REPRODUCE_ELIGIBLE` means only *eligible for a reproduction attempt*.** It asserts that the available inventory contains sufficient evidence to justify an attempt. It asserts nothing about whether the attempt will succeed.
4. **The result of the 406 is not a reproducibility rate.** No proportion of any classification state may be reported as a rate of reproducibility, non-reproducibility, or scientific validity.

### 12.2 Semantic non-implications

These hold for every repository, without exception, and may not be collapsed:

```text
ELIGIBLE  ≠  REPRODUCED
NOT_YET   ≠  NOT_REPRODUCIBLE
NO_CLAIM  ≠  NO_RESEARCH
```

`NOT_YET_ELIGIBLE` is a statement about the inventory, not about the science, and is re-evaluated whenever new evidence appears. `NO_PUBLISHED_CLAIM` records that no claim was found **at the inspected depth** and is explicitly not a judgement of value.

### 12.3 B3 is deliberately not relaxed

`mirailand` stays `REPRODUCE_NOT_YET_ELIGIBLE` and goes to manual review. Treating any executable file as a presumed reproduction entrypoint would manufacture eligibility. Losing candidates is preferable to fabricating them; the asymmetry in §10 governs.

## 13. Artifact ↔ repository is not 1:1

G0 must not build the implicit ontology:

```text
repo → artifacts          (owned, 1:1)
```

The `upload/FG Supply.pdf` finding shows the relation is not ownership. The permitted form is:

```text
repo  ←→  artifact          (with membership evidence)
```

**The same artifact appearing in three repositories does not establish that the three are the same project, and does not make a claim attributable to each of them.** Membership is a claim requiring evidence, in the same way identity is: name similarity and co-location are candidates, never resolutions.

Consequences for this phase:

- An artifact found in several repositories is recorded once per repository **with its path**, and the membership relation is marked unestablished.
- Classification is per repository and uses only that repository's own paths. No repository inherits another's artifacts.
- Any future identity resolution over artifacts must treat cross-repository appearance as a **candidate signal only** — the same rule already applied to repository names in G0-2.
