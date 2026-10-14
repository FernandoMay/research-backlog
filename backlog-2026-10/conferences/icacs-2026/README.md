# A-07 — ICACS 2026, Verifiable Execution and Durability Metrics for Autonomous Multi-Agent Economies on Distributed Ledgers

**Status: `Proposed` — proposal only; no manuscript, no run; all numeric claims blocked.**

## At a glance

| Field | Value |
|---|---|
| Backlog ID | `A-07` (assigned 2026-10-14) |
| Venue | ICACS 2026 (Phuket, Thailand, December 18–20, 2026) |
| Track | Tracks 2 / 4 / 5 — blockchain and distributed-ledger sub-topics |
| Working title | Verifiable Execution and Durability Metrics for Autonomous Multi-Agent Economies on Distributed Ledgers |
| Enfoque (rendered in ENGLISH) | Verifiable execution and durability metrics for autonomous multi-agent economies running on a distributed ledger (agent swarms, auditable settlement), grounded in a reproducible conformance harness |
| Repo | [xing-core](https://github.com/FernandoMay/xing-core) |
| Submission link | `TBD — none` |
| Submission date | `TBD — none` |
| Official deadline | **2026-10-15** (from Inbox 2026-10; source: [inbox-2026-10/02-icacs-2026/README.md](../inbox-2026-10/02-icacs-2026/README.md)) |
| Inbox classification | `Verified established` |
| Retrieved | 2026-10-14 |

**Topic decision (2026-10-14):** Re-anchored from the DSL Bank payment-rails study (excluded per user direction) to the **ledger + multi-agent** line, backed by `xing-core` (agent swarms, WASM sandbox, conformance tests). **Deadline reality:** ICACS 2026 closes 2026-10-15, one day after this decision, with no manuscript and no linked run — **not submittable in 2026**. Keep as a parked proposal pending a retarget.

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

Extend the [xing-core](https://github.com/FernandoMay/xing-core) conformance harness into a concrete measurement harness for agent-economy execution (durability metric definitions, failure taxonomy, auditable settlement traces) that can produce reproducible runs with pinned versions and seeds; no numbers to be published until that linked run exists.
