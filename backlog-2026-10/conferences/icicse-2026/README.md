# A-11 — ICICSE 2026, Cross-Platform Desktop Shell Architecture with Liquid Glass Rendering and Native IPC Integration

**Status: `Proposed` — proposal only; no manuscript, no run; all numeric claims blocked.**

## At a glance

| Field | Value |
|---|---|
| Backlog ID | `A-11` (assigned 2026-10-14) |
| Venue | ICICSE 2026 (Chongqing, China, December 27–29, 2026) |
| Track | Computer Information Science & Software Engineering |
| Working title | Cross-Platform Desktop Shell Architecture with Liquid Glass Rendering and Native IPC Integration |
| Enfoque (rendered in ENGLISH) | Software architecture patterns for advanced, distributed user interfaces (Flutter/Linux/GLSL) with high-performance inter-process communication (IPC) channels |
| Repo | `TBD — none` |
| Submission link | `TBD — none` |
| Submission date | `TBD — none` |
| Official deadline | **2026-11-15** (email said Nov 10) (from Inbox 2026-10; source: [inbox-2026-10/06-icicse-2026/README.md](../inbox-2026-10/06-icicse-2026/README.md)) |
| Inbox classification | `Contradicted` |
| Retrieved | 2026-10-14 |

## Evidence gate (rules.md §3)

No number may appear until a linked, reproducible run exists. Current state: **no run** — all numeric claims blocked.

| Field | Status | Required evidence |
|---|---|---|
| Reproducible run | No run linked | Linked, current run (code + seeds + configuration) with reproducible instructions |
| Rendering performance | Blocked | Frame rate, GPU utilization, frame times (p95/p99), thermal/CPU overhead; controlled benchmarks on specified targets |
| IPC performance | Blocked | Latency (round-trip), throughput (msg/sec/bytes), jitter, zero-copy effectiveness; synthetic microbenchmarks with methodology |
| Architecture validity | Blocked | Architecture tradeoffs, conformance to platform constraints, portability matrix with test coverage |
| Baselines | Blocked | Baseline shells/frameworks with citations, fair comparison methodology, reproduction steps |

## References to establish

Canonical search terms (3–6). **do NOT invent citations.** Only record verified sources if/when found.

- "desktop shell architecture" + "cross-platform UI" + "Flutter" + "Linux" + "GLSL"
- "liquid glass" + "compositing" + "GPU rendering" + "rendering performance" + "benchmarking"
- "inter-process communication" + "IPC" + "high-performance IPC" + "zero-copy" + "D-Bus" + "Unix domain sockets"
- "distributed user interfaces" + "software architecture patterns" + "portability" + "reproducibility"
- "microbenchmarks" + "performance measurement" + "methodology" + "reproducible experiments"

## Next real action

Define reproducible microbenchmarks for GPU rendering (frame times) and IPC channels (latency/throughput/jitter) on a documented target matrix (Flutter/Linux/GLSL), create an architecture specification with measurable quality attributes, and produce a linked run with pinned toolchains and environment manifest; no numbers to be published until that run exists.

(End of file)
