# A-07 — ICACS 2026, Formal Auditing and Durability Metrics for High-Throughput Layer-1 Payment Rails

**Status: `Proposed` — proposal only; no manuscript, no run; all numeric claims blocked.**

## At a glance

| Field | Value |
|---|---|
| Backlog ID | `A-07` (assigned 2026-10-14) |
| Venue | ICACS 2026 (Phuket, Thailand, December 18–20, 2026) |
| Track | Track 4: Systems and Networks / Track 3: AI and Machine Learning |
| Working title | Formal Auditing and Durability Metrics for High-Throughput Layer-1 Payment Rails |
| Enfoque (rendered in ENGLISH) | Adversarial-audit methodology and resilience metrics for high-throughput payment protocols (Solana/Soroban), focused on smart-contract scalability and durability under extreme load |
| Repo | [dsl-bank](https://github.com/FernandoMay/dsl-bank) |
| Submission link | `TBD — none` |
| Submission date | `TBD — none` |
| Official deadline | **2026-10-15** (from Inbox 2026-10; source: [inbox-2026-10/02-icacs-2026/README.md](../inbox-2026-10/02-icacs-2026/README.md)) |
| Inbox classification | `Verified established` |
| Retrieved | 2026-10-14 |

## Evidence gate (rules.md §3)

No number may appear until a linked, reproducible run exists. Current state: **no run** — all numeric claims blocked.

| Field | Status | Required evidence |
|---|---|---|
| Reproducible run | No run linked | Linked, current run (code + seeds + configuration) with reproducible instructions |
| Durability metrics | Blocked | Defined metrics, measurement harness, baseline runs, repeated trials across load profiles |
| Adversarial audit artifacts | Blocked | Audit log, failure catalog, test corpus, defect IDs linked to failing tests and remediation commits |
| Dataset/platform traces | Blocked | Network/transaction traces, version pins (protocol, runtime), environment manifest |
| Baselines | Blocked | Published baselines with citations and reproduction steps |

## References to establish

Canonical search terms (3–6). **do NOT invent citations.** Only record verified sources if/when found.

- "formal verification" + "adversarial audit" + "layer-1" + "payment rails"
- "durability metrics" + "resilience" + "high-throughput" + "blockchain" + "load testing"
- "Solana" + "Soroban" + "smart contract" + "scalability" + "extreme load"
- "fault injection" + "blast radius" + "liveness/safety" + "durability"
- "blind adversarial audit" + "DSL bank" + "reproducible run"

## Next real action

Link the existing [dsl-bank](https://github.com/FernandoMay/dsl-bank) blind adversarial audit artifacts to a concrete measurement harness (load profiles, durability metrics definitions, failure taxonomy) that can produce reproducible runs with pinned versions and seeds; no numbers to be published until that linked run exists.

(End of file)
