# G0-4 — Classification Ledger, 534 Repositories

**Branch**: `audit/g0-estate` · **Date**: 2026-10-02
**Instrument**: `predicate.py` at `9db4494` plus the nested-exclusion fix recorded in §2 below
**Predicate of record**: `REPRODUCE-SELECTION.md`
**Validation**: 7/7 against a deliberately diverse ground truth

> This ledger is an **inventory classification**. It is not a reproducibility result, and no proportion in it may be read as a rate.

---

## 1. Ledger

| Bucket | Repositories |
|---|---:|
| Adjudicated under P1 (different instrument) | 7 |
| Classified by this predicate | 527 |
| **Total coverage** | **534 / 534** |

| State | Count |
|---|---:|
| `NO_PUBLISHED_CLAIM` | 472 |
| `REPRODUCE_NOT_YET_ELIGIBLE` | 31 |
| `REPRODUCE_ELIGIBLE` | 24 |

### By bucket

| Bucket | `NO_PUBLISHED_CLAIM` | `NOT_YET_ELIGIBLE` | `ELIGIBLE` |
|---|---:|---:|---:|
| 121 content-inspected | 113 | 5 | 3 |
| 406 remaining | 359 | 26 | 21 |

### Missing elements, across the 31 `NOT_YET_ELIGIBLE`

| Element | Count |
|---|---:|
| `EXECUTION_CHAIN` | 24 |
| `EXECUTION_INSTRUCTION` | 14 |

41 repositories carry the non-blocking `INPUT_ARTIFACT_ABSENT` flag.

### 24 `REPRODUCE_ELIGIBLE`

`Almond` · `ai4science-2026-agentic-science` · `camae-paper` · `chp` · `dijkstralab` · `fcstn` · `i02-diffusion-covert-detection` · `iccit-2026-bci-transformer-swarm` · `icmv-ss2-quantum-cognitive-ai` · `incc-2026-semantic-jscc` · `iscmi-01-fuzzy-conformal` · `leo-01-predictive-routing` · `mirror` · `n01-diffusion-thz-edge` · `r01-physical-covert-thz` · `research-backlog` · `s02-semantic-thz` · `sem-01-adversarial-semantic` · `socketlab` · `v01-quantum-cognitive-networking` · `w3v-ieee-package` · `sentinelx` · `xing` · `xing-adan-resilience`

None has been executed. `ELIGIBLE` asserts only that an attempt is justified.

## 2. Instrument errors found during this run

### 2.1 `NESTED-VENDOR-ESCAPE` — found by spot check, not by the predicate

The vendor exclusion used `startswith`, so it excluded vendor directories **only at the top level**. Nested ones passed through:

| Repository | Path that fired | What it was |
|---|---|---|
| `newslttr` | `bakendo/env/lib/python3.10/site-packages/botocore/data/lookoutmetrics/…/service-2.json` | a committed virtualenv's third-party packages |
| `socketlab` | `javascript_implementation/node_modules/@tailwindcss/…/1.bug_report.yml` | `node_modules`, which the exclusion list already named |

**Fix.** Exclusion now matches **path components**, not a string prefix, and `env`, `site-packages`, `virtualenv`, `.git`, `__pycache__`, `eggs`, `dist-info` were added.

**Effect.** `newslttr` reclassified `REPRODUCE_ELIGIBLE → NO_PUBLISHED_CLAIM`. `socketlab` remained eligible on its own evidence (`latex_report/final_report.tex`, `latex_report/README.md`), which the fix correctly preserved. Ground truth held at 7/7.

This defect was found by **reading the evidence paths of the eligible set**, not by the predicate failing. A predicate does not audit itself; the spot check is the compensating control, and here it was load-bearing.

### 2.2 Empty repositories are not fetch failures

Seven repositories (`alpha`, `ctd`, `enhealthment`, `graphicsql`, `hanzi`, `vibraniohm`, `walllet`) returned `HTTP 409 — Git Repository is empty` on the tree endpoint. This was initially recorded as a fetch error.

It is not. A 409 with that message is the API stating the repository has no commits. All seven are recorded as `tree_status: empty_409_verified` — an observed fact with its evidence, not an assumption that they are empty. Had the failure been treated as an empty file list and classified without this check, seven repositories would have been classified on the strength of an error.

## 3. Falsos positivos y negativos

| Type | Found | How |
|---|---|---|
| False positive, A2 | 16 | ground truth; matched `Map`, `AppColors.error`, `Aspect Ratio` |
| False positive, A1 | 3 | ground truth; UI assets, a foreign upload, an issue template |
| False positive, A1 nested | 2 | spot check; committed virtualenv and `node_modules` |
| False negative, B2 | 1 confirmed (`fcstn`) | ground truth; self-contained regeneration |
| False negative, A1 | 1 probable (`mirailand`) | accepted deliberately; §12.3 |

`REPRODUCE_ELIGIBLE` on the inspected population moved 24 → 8 → 3 across the 121 as defects were removed. Every one of the first 24 was a false positive.

## 4. Manual review queue

| Repository | Reason |
|---|---|
| `Almond` | eligibility rests on a single path, `docs/ALMOND_TECHNICAL_REPORT.tex` |
| `mirailand` | probable false negative; ships `6im1_mirai_final.pdf` and `mirai onepager.pdf` |
| `research-backlog` | **the audit's own repository** qualifies, via `audit/batch*/REPORT.md` and `papers/…/e1_rows.csv` |

`research-backlog` is a structural note, not a conflict: G0 is read-only and never adjudicates P1, so the repository cannot certify its own findings. It is recorded so that no later reader mistakes it for an independent observation.

## 5. Artifact ↔ repository is not 1:1

The `upload/FG Supply.pdf` finding means membership cannot be modelled as ownership. `repo → artifacts` is wrong; `repo ←→ artifact`, with evidence, is permitted. The same artifact in three repositories does not make the three the same project, and does not make a claim attributable to each. Classification here is per repository and uses only that repository's own paths — no repository inherits another's artifacts. Cross-repository appearance is a candidate signal only, the same rule applied to repository names in G0-2.

## 6. Provenance

| File | sha256 |
|---|---|
| `raw/t406-targets.json` | `fa7bbdaa79721d2d5b81c4045664f4470193c42ec47b874f161b9328c44795b1` |
| `raw/t406-observed.json` | `9b52ccafbc69bd6e6172b8370a17216ec9c561fd9da130d3e10365b34ba84317` |
| `raw/t406-classified.json` | `82e697202b3506c87d74481efd89108ba8d4ba264e5ce74542b3caaa3ffd3382` |
| `raw/estate-classified.json` | `452a4f2ae7daadb6d242da2675bbbf9cb00230758dacc143b249f421993a661b` |
| `raw/wave1.json` | `fec615e98b76a2f0586c47123126ef717ddfa81e4037c304def6befa11127176` |

All payloads are gitignored and regenerate from the recorded endpoints. Collection was read-only via API: no repository was cloned, modified, or written to.

## 7. What this ledger does not establish

- **No reproducibility rate.** 24 of 534 are eligible for an attempt. None has been attempted. `24/534` is not a reproducibility figure and must never be reported as one.
- **`NO_PUBLISHED_CLAIM` is depth-limited.** 472 repositories had no claim found in the file tree or README at the inspected depth. That is not "no research," and not "no claim exists."
- **B3 under-detects.** A repository whose only entrypoint has a non-standard name and ships no instruction document is `NOT_YET` when it may well be executable.
- **`NOT_YET_ELIGIBLE` is about the inventory**, not the science, and is re-evaluated when new evidence appears.
- **No repository was executed**, so nothing here speaks to whether any published result is correct.