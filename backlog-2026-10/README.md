# Research Backlog Index

Fourteen investigations (A-01 to A-14), plus two invitation inboxes: 15 items received 2026-09-26 and 12 items received 2026-10-09..2026-10-14.

**The highest-leverage item in this backlog is not an inbox invitation.** `FernandoMay/dsl-bank` holds a finished, committed, tested durability study — including a blind adversarial audit that falsified its own core property and produced seven defects. As of 2026-10-14 that study is written up and in submission at AIBT 2026 as paper `SH-2025` (see [Inbox 2026-10](#inbox-2026-10)); the remaining action is to resend it with an abstract and keywords, not to start writing. Everything else on either inbox is either blocked on work that does not exist or routed to venues that do not deserve it.

All external facts below were retrieved on **2026-09-27**, except the [Inbox 2026-10](#inbox-2026-10) section and the A-04 update, retrieved on **2026-10-14**. Every cell that could not be verified is `TBD` and names what was searched.

## Priority roadmap

Ordered by expected value per unit of effort, **not** by deadline date.

### Tier 0 — damage control, this week, no writing

| Item | Action | Cost | Risk if skipped |
|---|---|---|---|
| **A-02** CINC #10432 | Ask the managing editor to confirm the revision landed | One email | An accepted paper dies silently. Revision was due 2026-09-19; eight days with no receipt |
| **A-01** AI4Science | Recover the original submission order number from your own email records | One search | A finished revision sits unused. The venue site is unreachable, so this is blocked on the number, not on the work |

### Tier 1 — a real manuscript and a real venue

| Item | Target | Window | Why this tier |
|---|---|---|---|
| **A-03** CPU/GPU + TornadoVM | **ICCD 2027**. Track 1 names "hardware acceleration for computing-intensive/data-intensive applications". Fallbacks: IPDPS 2027, CCGrid 2027, ISC HP 2027 | IPDPS 2027 `2026-10-08`, CCGrid 2027 `2026-12-01`, ISC HP 2027 `2026-12-21`. ICCD 2027 CFP not published | The only item with a finished manuscript, real measurements and an established venue. ICCD 2026 closed 2026-06-10 |
| **A-02** CINC | Springer LNCS published version, once Tier 0 confirms the revision landed | Editor-dependent | Highest single value here: already at provisional acceptance |

### Tier 2 — real code, unwritten

| Item | Asset that already exists | Venue fit |
|---|---|---|
| **DSLBank paper** | `FernandoMay/dsl-bank`: 287 tests, 9 packages, real PostgreSQL, a generated 243-cell crash-and-concurrency matrix, a blind audit that falsified its own ownership property and produced 7 defects with failing tests, then remediation | AIBT `Track 2: Blockchain Technology and Systems`, ICICM `Track-4: Cybersecurity and Privacy Protection`, CAIT `Multiagent systems` |
| Almond | Workforce-optimization solver, first vertical slice | Not yet a paper. A vertical slice is not a contribution |
| **A-04 / A-05 / A-06** | Drafts with every number blocked by the audit | Not a writing problem. Each needs a real run before any venue is relevant |

### Tier 3 — the inbox

One venue in eleven is genuinely established, and its window closed in June. See [Inbox 2026-09](#inbox-2026-09).

## Inbox 2026-09

Fifteen invitations received 2026-09-26. Per-venue evidence: [conferences/inbox-2026-09/inbox-index.md](conferences/inbox-2026-09/inbox-index.md).

| Venue | Official deadline | Classification | Finding |
|---|---|---|---|
| ICCD 2026 | **closed 2026-06-10** | `Verified established` | The only solid IEEE conference in the batch. Window shut 109 days before the email arrived |
| AICM 2026 | **2026-09-30** | `Contradicted` | Email said 2026-10-30 — that is the *notification* date. Closes in 3 days |
| ICAIT 2026 | 2026-09-30 | `Verified established` | Telecom and optical only. No fit with any research line |
| MLPR 2026 | 2026-09-30 | `Verified thin` | Calls its recommended journal `SCI`; the journal's own pages say `ESCI` |
| AIAT 2026 | 2026-10-01 | `Verified thin` | No fit |
| **CAIT 2026** | **2026-10-05** | `Contradicted` | Email said 2026-10-20 — that is the *registration* deadline. A 15-day miss |
| **ICICM 2026** | 2026-10-05 | `Verified established` | Real fit: `Track-4: Cybersecurity and Privacy Protection`, `Special Track 4: Applied Operations Research and Optimization` |
| **AIBT 2026** | 2026-10-10 | `Verified thin` | No past-edition archive. Real fit: `Track 2: Blockchain Technology and Systems`, `Track 5` FinTech |
| ICCIP 2026 | 2026-10-05 | `Verified thin` | Claims IEEE Record #70931; the site shows ACM for all ten archived editions |
| ICMSR 2026 | 2026-10-05 | `Verified thin` | Claims a 12th edition, 8 are archived. Special-issue journals unverified |
| BioMRH 2026 | 2026-10-09 | `Verified thin` | Springer LNNS is intent, not confirmed indexing |
| AISC journal | 2026-12-31, no-APC claim | `Unverified` | Zero articles published, no APC figure published, no Scopus / DOAJ / WoS |
| IntechOpen book | proposals `2026-10-14`, chapters `2026-12-16` | `Verified established` | Live page, ISBN assigned. Open-access chapter fee applies |
| NanoX 2026 | n/a | `Verified thin` | "Global Nanotechnology Network" and the named program director exist nowhere |
| DSC Next 2027 | not published | `Verified thin` | Rome venue with a Mississauga address; the site lists Greenbelt MD and Noida India |

**Tooling gap affecting the whole inbox:** `dl.acm.org` returned HTTP 403 and `conferences.ieee.org` returned 404/418 on every request, so no "indexed in ACM DL" and no IEEE conference-record number in this batch could be independently confirmed.

## Inbox 2026-10

Twelve items received 2026-10-09..2026-10-14. Per-venue evidence: [conferences/inbox-2026-10/inbox-index.md](conferences/inbox-2026-10/inbox-index.md).

Seven are new venues; five are repeats of a September record that carry a status delta. In four of the repeats the email deadline is wrong — see the index's contradictions table. This section is the assignment layer: it says what, if anything, each item changes for the investigations above. The paragraph previously claiming "**No new investigation is opened for the seven new venues**" is now false. The seven new venues (and the IntechOpen book item) have been assigned to new investigations: 01 ECCS → `A-13`; 02 ICACS → `A-07`; 03 RAAI → `A-09`; 04 ICCC → `A-08`; 05 ICETC → `A-12`; 06 ICICSE → `A-11`; 07 CSAI → `A-10`; 12 IntechOpen → `A-14`. Rows 08/09/10/11 keep their existing A-04/A-01/AIBT/ICCPR references.

| # | Item | Classification | What it changes for this backlog |
|---|---|---|---|
| 01 | ECCS 2027 | `Verified established` | Vienna, Jun 2027; `Terahertz Communications` is Track 3 and maps to A-01/A-03. Assigned to investigation **`A-13`**. |
| 02 | ICACS 2026 | `Verified established` | Phuket, Dec 2026. Assigned to investigation **`A-07`** (verifiable execution and durability metrics for autonomous multi-agent economies on distributed ledgers; re-anchored off the DSL Bank study). **Deadline 2026-10-15 — not submittable in 2026.** |
| 03 | RAAI 2026 | `Verified established` | Singapore, Dec 2026. Assigned to investigation **`A-09`** (fuzzy-calibrated conformal prediction for safe action selection in autonomous agents). |
| 04 | ICCC 2026 | `Contradicted` | Chengdu, Dec 2026; team must note the deadline is **2026-10-20**, not the email's Nov 20. Assigned to investigation **`A-08`** (adaptive edge-cloud orchestration for distributed multi-agent cognitive runtimes). |
| 05 | ICETC 2026 | `Contradicted` | Porto, Dec 2026; deadline 2026-10-30 (news 2026-10-10), not the email's Nov 10. Assigned to investigation **`A-12`** (brainwave-driven adaptive cognitive offloading for assistive learning). |
| 06 | ICICSE 2026 | `Contradicted` | Chongqing, Dec 2026; deadline 2026-11-15, not the email's Nov 10. Assigned to investigation **`A-11`** (reproducible conformance harness for reinforcement-learned multi-agent scheduling). |
| 07 | CSAI 2026 | `Verified established` | Beijing, Dec 2026; deadline 2026-11-05. Assigned to investigation **`A-10`** (semantic context compression and vector orchestration for distributed multi-agent memory). |
| 08 | ISCMI 2026 | `Verified established` | **A-04 delta.** The submission deadline A-04 logged as unverifiable is now published (2026-09-30). Registration due **2026-10-25**. The reported abstract approval (`VA263-A`) is `User-asserted`, not `Accepted` |
| 09 | AI4Science 2026 | `Verified thin` | **A-01 delta.** The official site is reachable again. The email asserts submission closed 2026-10-13; that date is not published. Item remains **not submitted** |
| 10 | AIBT 2026 | `Verified thin` | **New in-submission item.** The DSL Bank manuscript is reported submitted as paper `SH-2025`; the venue asks for abstract and keywords. Notification 2026-11-10 |
| 11 | ICCPR 2026 | `Verified established` | Registration due 2026-10-15. A decision item (attend / not attend), not an investigation |
| 12 | IntechOpen book | `Verified established` | Chapter proposal due 2026-10-14; EUR 1,650 only if the chapter is accepted. Assigned to investigation **`A-14`** (cognitive offloading, autonomy, and human-AI trust in agentic systems). |

### The one new item with a real receipt: DSL Bank / AIBT

Reported to the backlog on the venue's own email: paper **`SH-2025`**, *"The DSL Bank Durability Study: A Blind Adversarial Audit of a Solana Payment-Rails Platform"*, status `In submission workflow` (venue email is the handle; portal URL `zmeeting.org/submission/aibt2026` + manuscript number `SH-2025`). The repository [dsl-bank](https://github.com/FernandoMay/dsl-bank) is the backing asset. **Open action: resend the corrected article with an abstract and keywords before the venue's review window; notification 2026-11-10.**

## Backlog

| ID | Investigation | Venue | Submission date | Repo | Submission link | Status |
|---|---|---|---|---|---|---|
| A-01 | Quantum-informed stochastic models for THz urban propagation, reframed as CEG (compositional / agentic evidence-grounded) | AI4Science 2026 (official name verified) | `TBD — never submitted` | [ai4science-2026-agentic-science](https://github.com/FernandoMay/ai4science-2026-agentic-science) | `TBD — no recorded portal handle; submission order number never recorded` | `Proposed` — user-confirmed NOT submitted 2026-09-27. Pending: upload `paper/main.pdf` under the original order. |
| A-02 | COGN-NDAN: semantic-aware cross-layer protocol with neural feedback for neuro-symbiotic 6G networks | `CINC` (acronym expansion unverified) manuscript #10432 | `TBD — original submission date not found` | [cogn-ndan](https://github.com/FernandoMay/cogn-ndan) | `TBD — submission system URL unknown; manuscript #10432 is the only handle on record` | `User-asserted` — revision package reported sent 2026-09-27, **no receipt evidence**. Not editorially accepted. |
| A-03 | History-based adaptive CPU/GPU selection, Java 21 + TornadoVM, third-version IEEE-format LaTeX manuscript | **Not chosen.** 4 candidate IEEE venues researched, all marked `candidate — not chosen` | `TBD — none` | `TBD — none` | `TBD — none` | `Proposed` — venue undecided, user does not know the conference. |
| A-04 | Fuzzy-calibrated conformal uncertainty for tabular medical data (MIMIC-III / UCI) | **Ambiguous acronym, 1 official match verified** — ISCMI = International Conference on Soft Computing & Machine Intelligence | `TBD — none` | `TBD — none` | `TBD — none` | `Proposed` — draft only; all numeric claims blocked. |
| A-05 | Semantic joint source-channel coding over a Rayleigh fading channel, reusing `sem-01-adversarial-semantic` | **Ambiguous acronym, 2 official matches verified** — INCC = Information Network and Computer Communications; INCC = International Neuromorphic Computing Conference | `TBD — none` | `TBD — none` | `TBD — none` | `Proposed` — draft only; all numeric claims blocked. |
| A-06 | Spatial-temporal Transformer swarm for BCI decoding | **Ambiguous acronym, 3 official matches verified** — ICCIT = Computer and Information Technology / Cognitive and Intelligent Technology / Creative Communication and Innovative Technology | `TBD — none` | `TBD — none` | `TBD — none` | `Proposed` — draft only; all numeric claims blocked. |
| A-07 | Verifiable Execution and Durability Metrics for Autonomous Multi-Agent Economies on Distributed Ledgers | ICACS 2026 (Phuket, Dec 18–20) | `TBD — none` | [xing-core](https://github.com/FernandoMay/xing-core) | `TBD — none` | `Proposed — proposal only; no manuscript, no run; all numeric claims blocked`. |
| A-08 | Adaptive Edge-Cloud Orchestration for Distributed Multi-Agent Cognitive Runtimes | ICCC 2026 (Chengdu, Dec 11–14) | `TBD — none` | [xing-core](https://github.com/FernandoMay/xing-core) | `TBD — none` | `Proposed — proposal only; no manuscript, no run; all numeric claims blocked`. |
| A-09 | Fuzzy-Calibrated Conformal Prediction for Safe Action Selection in Autonomous Agents | RAAI 2026 (Singapore, Dec 18–20) | `TBD — none` | [iscmi-01-fuzzy-conformal](https://github.com/FernandoMay/iscmi-01-fuzzy-conformal) | `TBD — none` | `Proposed — proposal only; no manuscript, no run; all numeric claims blocked`. |
| A-10 | Semantic Context Compression and Vector Orchestration for Distributed Multi-Agent Memory | CSAI 2026 (Beijing, Dec 18–21) | `TBD — none` | [xing-core](https://github.com/FernandoMay/xing-core) | `TBD — none` | `Proposed — proposal only; no manuscript, no run; all numeric claims blocked`. |
| A-11 | A Reproducible Conformance Harness for Reinforcement-Learned Multi-Agent Scheduling | ICICSE 2026 (Chongqing, Dec 27–29) | `TBD — none` | [xing-core](https://github.com/FernandoMay/xing-core) | `TBD — none` | `Proposed — proposal only; no manuscript, no run; all numeric claims blocked`. |
| A-12 | Brainwave-Driven Adaptive Cognitive Offloading for Assistive Learning | ICETC 2026 (Porto, Dec 14–17) | `TBD — none` | [fcstn](https://github.com/FernandoMay/fcstn) | `TBD — none` | `Proposed — proposal only; no manuscript, no run; all numeric claims blocked`. |
| A-13 | Decentralized Cognitive Routing for Resilient THz-Enabled Multi-Agent Wireless Networks | ECCS 2027 (Vienna, Jun 2–4 2027) | `TBD — none` | [leo-routing-itft2026-package](https://github.com/FernandoMay/leo-routing-itft2026-package) | `TBD — none` | `Proposed — proposal only; no manuscript, no run; all numeric claims blocked`. |
| A-14 | Cognitive Offloading, Autonomy, and Human-AI Trust in Agentic Systems | IntechOpen book "AI and Psychology - Influence of AI on Human Mind" | `TBD — none` | `TBD — none` | `TBD — none` | `Proposed — proposal only; no manuscript, no run; all numeric claims blocked`. |

### ID provenance

`A-01` is the only **carried-over** ID; it was already `A-01` in the previous backlog. `A-02` through `A-06` were assigned on **2026-09-27** in the order the items are listed above. `A-07`..`A-14` were assigned on **2026-10-14**.

## Status legend

These five values are the only permitted statuses. Definitions are binding and live in [rules.md](rules.md).

| Status | Meaning |
|---|---|
| `Proposed` | Draft only. Never submitted anywhere. |
| `In submission workflow` | Submitted, awaiting a decision. Requires a real submission link. |
| `Revision in progress` | A decision was received and a revision is being written. |
| `User-asserted` | The user stated this happened, but no receipt evidence exists on file. |
| `Accepted` | Accepted, with a recorded decision artifact. |

## Where to look

| Record | Covers |
|---|---|
| [conferences/ai4science-2026/README.md](conferences/ai4science-2026/README.md) | A-01 |
| [conferences/cinc-10432/README.md](conferences/cinc-10432/README.md) | A-02 |
| [conferences/adaptive-cpu-gpu-ieee/README.md](conferences/adaptive-cpu-gpu-ieee/README.md) | A-03, candidate IEEE venue table |
| [conferences/iscmi-fuzzy-conformal/README.md](conferences/iscmi-fuzzy-conformal/README.md) | A-04 |
| [conferences/incc-semantic-jscc/README.md](conferences/incc-semantic-jscc/README.md) | A-05 |
| [conferences/iccit-bci-transformer/README.md](conferences/iccit-bci-transformer/README.md) | A-06 |
| [conferences/icacs-2026/README.md](conferences/icacs-2026/README.md) | A-07 |
| [conferences/iccc-2026/README.md](conferences/iccc-2026/README.md) | A-08 |
| [conferences/raai-2026/README.md](conferences/raai-2026/README.md) | A-09 |
| [conferences/csai-2026/README.md](conferences/csai-2026/README.md) | A-10 |
| [conferences/icicse-2026/README.md](conferences/icicse-2026/README.md) | A-11 |
| [conferences/icetc-2026/README.md](conferences/icetc-2026/README.md) | A-12 |
| [conferences/eccs-2027/README.md](conferences/eccs-2027/README.md) | A-13 |
| [conferences/intechopen-book/README.md](conferences/intechopen-book/README.md) | A-14 |
| [conferences/inbox-2026-09/inbox-index.md](conferences/inbox-2026-09/inbox-index.md) | The 15 invitations of 2026-09-26, with verification evidence |
| [conferences/inbox-2026-10/inbox-index.md](conferences/inbox-2026-10/inbox-index.md) | The 12 items of 2026-10-09..2026-10-14, with verification evidence and the assignment layer |
| [STRATEGIC-DRAFTS-AUDIT-2026-09-15.md](STRATEGIC-DRAFTS-AUDIT-2026-09-15.md) | Surviving audit; source of the blocked-claims tables |
| [rules.md](rules.md) | Backlog rules |

## Recommended work order

Carried forward verbatim from the surviving audit, [STRATEGIC-DRAFTS-AUDIT-2026-09-15.md](STRATEGIC-DRAFTS-AUDIT-2026-09-15.md):

1. **ISCMI** (A-04): fuzzy-calibrated conformal uncertainty; fastest to validate with public tabular data.
2. **INCC** (A-05): semantic JSCC over Rayleigh fading; reuse `sem-01-adversarial-semantic` after adding a real channel/noise pipeline.
3. **ICCIT** (A-06): spatial-temporal Transformer swarm for BCI; highest risk because it requires subject-wise public EEG evaluation and real latency measurement.

This order covers A-04 to A-06 only. A-01 and A-02 are already past the draft stage and sit outside it.

## TBD register

Every unresolved cell, and why. Rule 5 of [rules.md](rules.md) requires each TBD to name what was searched.

| Record | Field | Why unresolved | What was searched |
|---|---|---|---|
| A-01 | Submission order number | Never recorded in any artifact or memory before the storage cleanup | Backlog index, Engram project history, surviving audit file |
| A-01 | Submission link | No portal handle exists because the upload never happened | User confirmation 2026-09-27 |
| A-01 | Submission date | The paper was never submitted | User confirmation 2026-09-27 |
| A-01 | Official site re-verification | `ic-ai4science.org` did not respond to any fetch attempt on 2026-09-27 (DNS resolves to `43.98.198.75` via `w.web725.com`; HTTPS and HTTP both return no response) | `webfetch` on `www.ic-ai4science.org/`, `/EditorialPolicy`; `curl` over HTTPS and HTTP; DNS lookup |
| A-02 | CINC expansion | No official 2026 source confirms which venue manuscript #10432 belongs to | `websearch` for CINC expansions; no official conference site reachable |
| A-02 | Submission system URL | Not on file | Backlog index, Engram project history |
| A-02 | Original submission date | Not on file | Backlog index, Engram project history |
| A-02 | Revision receipt | User-asserted only | No editorial email, no manuscript status page, no acknowledgement on file |
| A-03 | Venue | User does not know which conference | Stated by user 2026-09-27 |
| A-03 | Repo / submission link / submission date | Nothing was ever created for this item | `TBD — none` |
| A-03 | CLUSTER 2027 deadline | 2027 CFP not published | `clustercomp.org/2027/` returns HTTP 404 on 2026-09-27 |
| A-03 | SC27 deadline | No SC27 site reachable | `sc27.supercomputing.org` transport error; only SC26 published, deadline 2026-04-08 already closed |
| A-04 | ISCMI submission deadline | Official site publishes no deadline at all | `iscmi.us`, `/cfp.html`, `/submission.html`, `/registration.html` |
| A-04 | Repo / submission link / submission date | Nothing was ever created for this item | `TBD — none` |
| A-05 | Repo / submission link / submission date | Nothing was ever created for this item | `TBD — none` |
| A-06 | Repo / submission link / submission date | Nothing was ever created for this item | `TBD — none` |
| A-06 | "IEEE ICCIT = International Conference on Computing, Information and Technology" | This specific expansion was **not** confirmed as a distinct 2026 venue | `conferences.ieee.org` search; three official ICCIT 2026 sites checked, none use that expansion |

## Blocked claims

The surviving audit blocks these. They are reproduced per record and must not be restated as results. See the audit file and the individual records.

| Draft | Claim | Current evidence status | Required evidence |
|---|---|---|---|
| ISCMI | MIMIC-III/UCI evaluation and ECE/Brier/latency table | No current repository run linked | Dataset license, preprocessing, code, seeds, repeated trials |
| INCC | 72% bandwidth reduction and 95.4% task accuracy | No current Deep-JSCC experiment linked | Dataset, channel model, trained weights, raw metrics, baselines |
| ICCIT | 86.9% BCI accuracy, kappa 0.82, 8.7 ms execution | No current transformer-swarm run linked | Public BCI dataset, subject-wise split, model code, hardware benchmark |
