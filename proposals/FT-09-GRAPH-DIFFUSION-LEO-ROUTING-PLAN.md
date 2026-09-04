# Paper FT-09 — Frontier Telematics (2027+)

## Paper
**Predictive Topological Routing and Dynamic Inter-Satellite Link Allocation in Mega-Constellations via Graph Neural Diffusion**

## Target Venue
- **Primary:** IEEE Journal on Selected Areas in Communications (JSAC)
- **Level:** Frontier Telematics / IEEE Transactions

## Research Questions
1. How can graph neural diffusion predict future link availability in LEO mega-constellations?
2. What routing strategy achieves zero packet loss during ISL handovers?
3. How does GND compare to classical link-state routing in NTN?

## Novelty (Level 4)
Current LEO routing (OSPF-style) collapses under signaling overhead in mega-constellations.
Graph Neural Diffusion predicts topological evolution and proactively routes before breaks.

## Architecture
```
[TLE Orbital Data] → [Continuous GND Engine]
                              ↓
                    [Manifold Prediction G(t)]
                              ↓
[Optimal ISL Routing] ← [Predictive Transition Matrix P*]
```

## Methodology
- **Graph Model:** Dynamic stochastic graph G(t) = (V, E(t), W(t))
- **Diffusion:** ODE-based graph diffusion with GCN layers
- **Data:** Real Starlink orbital TLE data, 1000+ satellites
- **Comparison:** GND vs OSPF vs Dijkstra vs reinforcement learning

## Mathematical Formulation
```
∂H(t)/∂t = -L(t)H(t) + F(H(t), X(t); Θ)

P* = argmin ∫ Σ (d_uv(t) + λ·P[LinkBreak]) dt
```

## Expected Contributions
1. Graph Neural Diffusion framework for satellite routing
2. Zero-packet-loss handover guarantee
3. 68% reduction in control overhead
4. Scalable to 1000+ node constellations

## Timeline
- **Q4 2026:** GND framework design + orbital data
- **Q1-Q2 2027:** Implementation + simulation
- **Q3 2027:** Paper writing + submission

## Status
📋 Proposed → ⏳ Planning
