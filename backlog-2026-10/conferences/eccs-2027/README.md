# A-13 — ECCS 2027, Decentralized Cognitive Routing for Resilient THz-Enabled Multi-Agent Wireless Networks

**Status: `Proposed` — proposal only; no manuscript, no run; all numeric claims blocked.**

## At a glance

| Field | Value |
|---|---|
| Backlog ID | `A-13` (assigned 2026-10-14) |
| Venue | ECCS 2027 (Vienna, Austria, June 2–4, 2027) |
| Track | Track 3: Terahertz Communications |
| Working title | Decentralized Cognitive Routing for Resilient THz-Enabled Multi-Agent Wireless Networks |
| Enfoque (rendered in ENGLISH) | Distributed AI agents for dynamic, decentralised route selection in THz-enabled next-generation (6G) networks, with resilience under churn and link/node failure |
| Repo | [leo-routing-itft2026-package](https://github.com/FernandoMay/leo-routing-itft2026-package) |
| Submission link | `TBD — none` |
| Submission date | `TBD — none` |
| Official deadline | **2027-01-05** (from Inbox 2026-10; source: [inbox-2026-10/01-eccs-2027/README.md](../inbox-2026-10/01-eccs-2027/README.md)) |
| Inbox classification | `Verified established` |
| Retrieved | 2026-10-14 |

**Topic decision (2026-10-14):** Anchored to ECCS's verbatim `Track 3: Terahertz Communications` (which maps to backlog A-01 / A-03), fusing the **THz/6G** line with cognitive multi-agent routing. Momentum: `leo-routing-itft2026-package` (NSGA-II + Q-learning simulator, JSON metrics) is a ready baseline; deadline 2027-01-05 gives the most room of this batch — **the item with the best chance of producing a real, reproducible run**.

## Evidence gate (rules.md §3)

No number may appear until a linked, reproducible run exists. Current state: **no run** — all numeric claims blocked.

| Field | Status | Required evidence |
|---|---|---|
| Reproducible run | No run linked | Linked, current run (code + seeds + configuration) with reproducible instructions |
| Routing performance | Blocked | Packet delivery ratio, end-to-end delay, throughput, path stretch, routing overhead; repeated trials |
| Resilience | Blocked | Link/node failures, churn, adversarial or stochastic disruptions; recovery time, convergence, availability |
| Decentralized cognitive routing | Blocked | Agent coordination model, convergence guarantees (if claimed), exploration/exploitation, overhead |
| Network simulation | Blocked | Simulator version, topology, mobility, radio model, traffic model, reproducible traces/config |
| Baselines | Blocked | Baseline protocols (e.g., established routing) with citations and reproduction steps |

## References to establish

Canonical search terms (3–6). **do NOT invent citations.** Only record verified sources if/when found.

- "decentralized routing" + "cognitive routing" + "multi-agent routing" + "6G" + "edge networks"
- "AI-driven networks" + "distributed intelligence" + "reinforcement learning routing" + "resilience"
- "network simulation" + "ns-3" + "OMNeT++" + "reproducible network experiments"
- "fault tolerance" + "routing convergence" + "mobility" + "traffic engineering"
- "decentralized control" + "autonomous agents" + "wireless networks" + "performance evaluation"

## Next real action

Define a reproducible simulation scenario (6G/edge, mobility, failure models), specify resilience metrics, implement decentralized cognitive routing agents in a pinned simulator (version + config), and produce a linked run with seeds; no numbers to be published until that run exists. Note: LEO routing direction may be considered, but no repo verified.

(End of file)
