# G0-3 Wave 2 — Ambiguous-Cluster Content Inspection

**Object**: the 119 `AMBIGUOUS` repositories from G0-2, plus `sentinelx` and `biohealy-ipn` as explicit targets. 121 repositories.
**Method**: read-only inspection via GitHub API (`gh api`). No repository cloned, no file written, no repository modified.
**Date**: 2026-10-02
**Parent**: `G0-estate-audit.md`

Wave 1 (`G0-3-WAVE1-RESEARCH.md`) covered three owner-promoted repositories. Its targets are excluded here.

### Provenance

Raw payloads are gitignored and regenerate byte-identically from `collect.py` against the recorded endpoint. Digests retained:

| File | sha256 |
|---|---|
| `raw/wave2-observed.json` | `23cccf6ad7fd7a3c1532226e3b434ba0815062f8d5d86f930fe41a3cf9ec9036` |
| `raw/wave2-targets.json` | `7711b69d31eca41aacbd27fcc654c21e5c484bdf1cf592c8ad7fa7cf415c9429` |
| `raw/wave2-pairs.json` | `a528d7da8665c0825b38dfbfe347dfeff3975ee87ad347a3758011831c4140de` |
| `raw/wave2-relation-corrected.json` | `d1cf8f21e668b7bb9dcc55088ea71804e7d6a9c74fdd35cd2cf661eee171455f` |

---

## 1. Pair assessment scope

G0-2 produced 34 name clusters covering 119 `AMBIGUOUS` members. Relation was assessed over **all unordered pairs inside each cluster** — no fixed base member, no self-comparison.

| Quantity | Value |
|---|---|
| Clusters | 34 |
| Members in scope | 119 |
| Unordered pairs assessed | 332 |
| Members in more than one cluster | 0 |

`332` was cross-checked against the expected total `Σ C(n,2)` over in-scope cluster members: **exact match**. Coverage is complete.

### 1.1 A cluster contains already-adjudicated packages

The 9-member cluster `q` contains two `RESOLVED_EXACT` P1 packages: `qce-ieee-package` and `quantum-k-sat-ieee-package`. They are **excluded** from wave 2 — re-inspecting an adjudicated package would reopen a closed adjudication. The exclusion is the scope guard holding, not a coverage gap.

This is direct evidence for the structural fact that name clustering may **surface** candidates and may never resolve identity: a clustering rule placed two packages resolved by exact identifier match into the same candidate cluster as seven unrelated ambiguous repositories. Had identity been inherited from the cluster instead of from exact identifier matching, both would have been mis-adjudicated.

---

## 2. Relation results — observed evidence only

| Outcome | Pairs | Meaning |
|---|---|---|
| **RELATED** (project-specific identical README text) | **2** | Same project text, not template boilerplate |
| Identical README text, but generic scaffold | 21 | Same template — not evidence of a shared project |
| Top-level layout match only | 21 | Candidate surfaced — **not** a relation verdict |
| **NO RELATION observed** | **288** | No observed overlap |

### 2.1 The two RELATED pairs

- `empleados` == `empleadosapi` — README is a Micronaut 3.7.2 generated documentation index.
- `mirailand` == `miraiweblight` — README is project-specific ("MIRAI Platform … empowering adolescents").

### 2.2 Two classes of pair explicitly NOT counted as relation

**Generic scaffold (21 pairs, 7 repositories).** Seven `workspace-*` repositories share a byte-identical README reading `# Welcome to Z.ai Code Scaffold`. They are instances of one template, not seven related projects.

**Layout-only match (21 pairs).** Repositories sharing an identical set of top-level directory names. Top-level layout has near-zero discriminative power — `src/`, `README.md`, `package.json` is what most web projects contain. These pairs are recorded as **surfaced candidates**, never as relation.

### 2.3 Repository structure findings

| Finding | Count | Names |
|---|---|---|
| No blobs at all (empty) | 5 | `teocom`, `versus7`, `vibrani0m`, `vibrani0m0`, `workspace-8a6684d2-…` |
| No README or `.md` file | 7 | above five plus `goginbooks` (6 files), `gotennisson` (3 files) |
| Generic scaffold README | 16 | 10 Z.ai Code Scaffold (`chainguardai`, `spaceverses`, `travelai`, 7 `workspace-*`), 4 Vercel/Next.js (`aegis-otc`, `nexus`, `niko-sun-frontend`, `workspace-66b9d710-…`), 2 StackBlitz (`miraiapp`, `miraiweb`) |

`vibrani0m` and `vibrani0m0` are near-identical names with **zero content in both**. Name similarity produced a pair with nothing to relate.

---

## 3. `sentinelx` — committed `.env` is NOT a credential exposure

`sentinelx` (521 files) has a committed top-level `.env`, sha256 `be8e1a92feff8f6cb699a9a70cc7d76a183538ab8c68a45e7d40f0d32bf20b94`, 50 bytes, one key.

| Property | Value |
|---|---|
| Key | `DATABASE_URL` |
| Scheme | `file` |
| Host class | unparseable (local path, no authority) |
| Credentials embedded in URL | no |
| sha256 | `be8e1a92feff8f6cb699a9a70cc7d76a183538ab8c68a45e7d40f0d32bf20b94` |

**This is not an exposure.** The value is a local filesystem database path. `sentinelx` is **not** added to the credential blast radius.

**Instrument lesson.** A first-pass heuristic classified this value as "non-placeholder" and would have created a false `INC` entry. The determining property is the **destination class**, not placeholder-ness: a non-placeholder value that resolves to a local path is not a credential. Any future exposure scan must classify the destination before reporting.

This also demonstrates why no value was ever printed. Every finding above is derived from structural properties — scheme, authority presence, credential presence, digest — never from the secret.

---

## 4. `biohealy-ipn` — the delivered quantity is never measured

`biohealy-ipn` is the estate's highest-safety-requirement target: a bioelectric stimulation device that drives **current through human tissue**. 19 files. Every file and the complete 659-line paper were read, so the absence below is **verified absence across the whole repository**, not an unsuccessful search.

### 4.1 What the paper documents

- `docs/biohealy_paper.tex:102` — describes a "balanced Howland current pump with **hardware safety limits**".
- `docs/biohealy_paper.tex:249-251` — derives the ceiling arithmetically from circuit topology:
  `I_max = V_sat / R_lim = 12 / 10000 = 1.2 mA`, from op-amp saturation at the 12 V supply and the 10 kΩ limiting resistor.
- `docs/biohealy_paper.tex:532` — "The AD9833 output was measured with a digital oscilloscope."
- `docs/biohealy_paper.tex:538` — "Using a calibrated Hall-effect probe, the magnetic field at 1 cm …"

### 4.2 What is absent from every file

| Term class | Hits |
|---|---|
| The word "safe" | **0** |
| Electrical safety, galvanic isolation, IEC 60601, UL 60601 | **0** |
| Medical disclaimer, contraindications, "consult a physician" | **0** |
| IRB, ethics committee, informed consent, human subject | **0** |
| Warning, danger, hazard, "do not use" | **0** |

### 4.3 The finding

The paper claims hardware safety limits and derives a 1.2 mA ceiling — but that figure is **calculated from component topology, never measured**. The two verification procedures the paper does report measure **frequency** (oscilloscope) and **magnetic field** (Hall probe).

**The quantity the device exists to deliver — current through tissue — is the one quantity never measured anywhere in the repository.** No documented electrical safety envelope, no medical disclaimer, no contraindications, no human-subject or ethics status accompanies a device presented as a `"fully open-source" bioelectric stimulation device` for human use (`README.md`).

Scope statement, stated precisely: this is a **documentation** finding. It establishes that the repository does not document a safety envelope and does not report a measurement of delivered current. It does not establish that the device is unsafe, and no such conclusion is drawn.

### 4.4 Secondary artifact defect

`README.md` contains uncompiled LaTeX source — `\SIrange{10}{1000}{\micro\ampere}` — in the rendered Markdown. The README was pasted from the paper's LaTeX source without compilation. This is an artifact-correspondence defect (R3 class: a document that does not correspond to its source) and it independently confirms README and paper share one origin.

---

## 5. Instrument defects in this wave

Four defects. All recorded, none cleaned silently.

### `INCOMPLETE-MARKER-VOCABULARY`
The scaffold detector returned **0** on a repository whose README literally reads `# Welcome to Z.ai Code Scaffold`. A marker list missing that template produced a clean zero that read as a finding. Actual count: **16**. A detector whose vocabulary is a hand-maintained list can return a confident negative; the vocabulary, not the code, is the defect.

### `LAYOUT-AS-RELATION`
Top-level layout equality was initially treated as relation evidence. 21 pairs were over-claimed as RELATED. Top-level layout has near-zero discriminative power. Same rule as name similarity: **structure may surface candidates; it may never resolve relation.** Corrected tally: 44 → **2** RELATED.

### `FIXED-BASE-CLUSTERING`
The first implementation fixed one base member per cluster and compared the rest against it, which the no-first-member rule forbids. It also compared each member against itself, producing `rel == self` as evidence. Corrected to all unordered pairs.

### `OUT-OF-SCOPE-MEMBER-IN-CLUSTER`
The `q` cluster contains two already-adjudicated P1 packages. The derivation crashed on their absence from the observed set. **The crash was the scope guard working.** Recorded as a composition fact about the clustering, not repaired by re-inspection.

---

## 6. What wave 2 does and does not establish

**Establishes.** Across 121 repositories and 332 in-cluster pairs: 2 pairs relate by project-specific text; 288 show no observed overlap; 21 share a template; 21 share only layout. 16 repositories are generic scaffolds, 5 are empty, 7 have no documentation. `sentinelx`'s committed `.env` is a local path, not a credential. `biohealy-ipn` documents no safety envelope and never measures delivered current.

**Does not establish.** That the 288 NO-RELATION pairs are unrelated in fact — only that no overlap was observed in structure and README text at this inspection depth. That any scaffold repository is worthless. That the 5 empty repositories represent abandoned rather than in-progress work. Any statement about `sentinelx`'s remaining 520 files, which were enumerated but not read.

**Next.** Deep inspection or execution remains undecided for `METRICS_REPRODUCE`. The 16 scaffolds and 5 empty repositories do not require content adjudication: a scaffold is a known object, and an empty repository has no artifact to correspond to anything.