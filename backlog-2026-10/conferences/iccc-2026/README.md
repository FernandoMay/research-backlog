# A-08 — ICCC 2026, Adaptive Edge-Cloud Orchestration for Distributed Multi-Agent Cognitive Runtimes

**Status: `Proposed` — proposal only; no manuscript, no run; all numeric claims blocked.**

## At a glance

| Field | Value |
|---|---|
| Backlog ID | `A-08` (assigned 2026-10-14) |
| Venue | ICCC 2026 (Chengdu, China, December 11–14, 2026) |
| Track | Computer Architecture, Systems, and Networking |
| Working title | Adaptive Edge-Cloud Orchestration for Distributed Multi-Agent Cognitive Runtimes |
| Enfoque (rendered in ENGLISH) | Framework for distributed orchestration of AI agents across edge devices and the cloud, minimising latency and guaranteeing fault tolerance over heterogeneous networks |
| Repo | `TBD — none` |
| Submission link | `TBD — none` |
| Submission date | `TBD — none` |
| Official deadline | **2026-10-20** (email said Nov 20) (from Inbox 2026-10; source: [inbox-2026-10/04-iccc-2026/README.md](../inbox-2026-10/04-iccc-2026/README.md)) |
| Inbox classification | `Contradicted` |
| Retrieved | 2026-10-14 |

## Evidence gate (rules.md §3)

No number may appear until a linked, reproducible run exists. Current state: **no run** — all numeric claims blocked.

| Field | Status | Required evidence |
|---|---|---|
| Reproducible run | No run linked | Linked, current run (code + seeds + configuration) with reproducible instructions |
| Orchestration metrics | Blocked | End-to-end latency, p95/p99, throughput, tail latency; measurement methodology and repeated trials |
| Fault tolerance | Blocked | Failure injection (node/link churn), recovery time, availability, rollback/consistency guarantees |
| Heterogeneous network model | Blocked | Topology, bandwidth/latency profiles, jitter, packet loss; trace-based or reproducible synthetic traces |
| Baselines | Blocked | Baseline schedulers/orchestrators with citations and reproduction steps |

## References to establish

Canonical search terms (3–6). **do NOT invent citations.** Only record verified sources if/when found.

- "edge-cloud orchestration" + "multi-agent systems" + "distributed runtime" + "latency minimization"
- "agent orchestration" + "fault tolerance" + "heterogeneous networks" + "edge computing"
- "cognitive runtime" + "distributed AI agents" + "resource allocation" + "scheduling"
- "resilience" + "partition tolerance" + "graceful degradation" + "reproducible experiments"

## Next real action

Define a minimal synthetic benchmark (heterogeneous network traces + agent workload) and a test harness to measure latency and fault-tolerance; create a reproducible environment manifest (versions, seeds, hardware profile) before any numeric claims; no numbers to be published until linked run exists.

(End of file)
