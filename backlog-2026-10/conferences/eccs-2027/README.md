# A-13 — ECCS 2027, Decentralized Cognitive Routing for Resilient THz-Enabled Multi-Agent Wireless Networks

**Status: `Proposed` — proposal only; no manuscript, no submission.**
A reproducible routing run now exists (2026-10-14), but it covers **LEO inter-satellite routing**, not the THz / decentralized-cognitive aspects of this topic. See *Progress* below.

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

**Topic decision (2026-10-14):** Anchored to ECCS's verbatim `Track 3: Terahertz Communications` (which maps to backlog A-01 / A-03), fusing the **THz/6G** line with cognitive multi-agent routing. Momentum: `leo-routing-itft2026-package` (NSGA-II + Q-learning simulator, JSON metrics) is a ready baseline; deadline 2027-01-05 gives the most room of this batch.

## Progress (2026-10-14)

**Asset integrity finding.** The linked repo's simulator is *reproducible* but does not measure what it claims: `nsga2_optimize` scored chromosomes with `np.random.uniform` (lines 169–174), Figure 4 was hard-coded (line 625), the Dijkstra and NSGA-II columns called the same function with the same `route_type` (lines 446–447), and resilience/coverage were computed once and copied into every method column (lines 461–467). Consequently the committed `data/metrics.json` and the ITFT 2026 paper (Paper ID 90) numbers are **not measurements**. Full audit: `docs/SIMULATOR-NOTES.md` in the asset repo.

**Honest replacement built and run.** A ground-up simulator in which every objective is obtained by routing demands through a Walker constellation under failures (real link budget, real NSGA-II over evaluated objectives, real Q-learning over measured rewards; no sampled or hard-coded results). PR: [leo-routing-itft2026-package#1](https://github.com/FernandoMay/leo-routing-itft2026-package/pull/1). Reproduce with `python simulator/leo_routing_real.py --seeds 8`.

Measured results (192 satellites, 30 episodes × 40 demands × 8 seeds, 95% CI over seeds; artifact `data/real_metrics.json`):

| Metric | Dijkstra | NSGA-II | NSGA-II + Q-learning |
|---|---|---|---|
| Latency (ms) | 71.06 ± 0.53 | 69.86 ± 0.50 | 70.80 ± 0.58 |
| Delivery | 1.000 | 1.000 | 1.000 |
| Resilience | 0.954 ± 0.004 | 0.960 ± 0.004 | 0.957 ± 0.003 |

Honest reading: the offline NSGA-II policy Pareto-dominates Dijkstra, but by a small margin; the online Q-learner does **not** beat the offline policy in a stationary environment; delivery saturates because the mesh stays connected.

**Open decision — THz vs LEO.** The track is Terahertz Communications, but the asset is LEO inter-satellite routing at Ka-band (30 GHz). THz carriers (0.1–10 THz) are not physically usable for LEO inter-satellite links at ~10³ km ranges due to molecular absorption. Either the topic drops "THz", or the venue/track is reconsidered. **Not yet decided.**

## Evidence gate (rules.md §3)

No number may appear until a linked, reproducible run exists. State as of 2026-10-14: a linked run now exists for the **LEO routing and resilience** sub-claims only.

| Field | Status | Required evidence |
|---|---|---|
| Reproducible run | Partial | Linked run exists for LEO multi-objective resilient routing (asset PR #1, seed 20261014, config pinned). No run yet for the THz or decentralized-cognitive aspects. |
| Routing performance | Partial | End-to-end latency and delivery measured. Still blocked: throughput, path stretch, routing overhead. |
| Resilience | Partial | Link/node failures (uniform + load-weighted disruption) with a disjoint-backup metric measured. Still blocked: churn, adversarial disruption, recovery time, convergence. |
| Decentralized cognitive routing | Blocked | Current run is centralized offline NSGA-II + a single-agent Q-learner, not decentralized cognitive agents; no coordination model or convergence guarantees. |
| Network simulation | Partial | Simulator is self-contained and version-independent (numpy only); geometry, link budget, and traffic model pinned. Still blocked: mobility traces, external radio-model validation. |
| Baselines | Partial | A Dijkstra shortest-path baseline is implemented and measured. Still blocked: external routing protocols with citations and reproduction steps. |

## References to establish

Canonical search terms (3–6). **do NOT invent citations.** Only record verified sources if/when found.

- "decentralized routing" + "cognitive routing" + "multi-agent routing" + "6G" + "edge networks"
- "AI-driven networks" + "distributed intelligence" + "reinforcement learning routing" + "resilience"
- "network simulation" + "ns-3" + "OMNeT++" + "reproducible network experiments"
- "fault tolerance" + "routing convergence" + "mobility" + "traffic engineering"
- "decentralized control" + "autonomous agents" + "wireless networks" + "performance evaluation"

## Next real action

Resolve the THz vs LEO decision first (it determines the venue and the whole evidence plan). Then, for whichever direction is chosen: extend the honest simulator to the missing claims — a genuine decentralized/cognitive agent model with an explicit coordination model, plus throughput/path-stretch/overhead metrics — in a pinned configuration, and produce a linked run with seeds. No new number is to be published until that run exists. `TBD` fields above name searches not yet completed.
