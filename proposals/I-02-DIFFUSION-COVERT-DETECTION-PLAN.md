# Paper I-02 — CCIOT 2026 (Deadline: Sep 1)

## Paper
**Diffusion Models for Covert Communication Detection in Distributed Systems**

## Conference
- **Venue:** CCIOT 2026 — Cloud Computing and Internet of Things
- **Dates:** Oct 24–26, 2026 | Okinawa, Japan
- **Publisher:** ACM (Ei Compendex & Scopus)
- **Deadline:** September 1, 2026

## Research Questions
1. Can conditional diffusion models effectively learn the distribution of normal network traffic?
2. How accurately can deviation from the learned distribution detect covert communication channels?
3. What is the false positive/negative tradeoff compared to traditional anomaly detection?

## Methodology
- **Architecture:** Conditional diffusion model trained on normal traffic profiles
- **Detection:** Anomaly scoring via reconstruction probability / divergence from generated distribution
- **Refinement:** Reinforcement learning loop to tune detection thresholds
- **Evaluation:** Standard IDS datasets (CICIDS, UNSW-NB15) + custom covert channel simulations
- **Metrics:** AUC-ROC, F1-score, detection latency, false positive rate

## Key Components
```
Normal Traffic Data
       │
       ▼
Conditional Diffusion Model
       │
       ▼
Generated Traffic Distribution
       │
       ▼
Comparison Engine ← Observed Traffic
       │
       ▼
Anomaly Score → Classification
       │
       ▼
RL Threshold Optimizer
```

## Expected Contributions
1. Novel application of diffusion models to covert communication detection
2. Adaptive threshold optimization via RL
3. Benchmark comparison with AE, GAN, and statistical methods
4. Open-source detection framework

## Timeline (Aug 28 – Sep 1)
- **Aug 28:** Dataset preparation + diffusion model architecture
- **Aug 29:** Training pipeline + baseline implementation
- **Aug 30:** Experiments + ablation study
- **Aug 31:** Write paper draft
- **Sep 1:** Finalize + submit

## References
- Diffusion models for anomaly detection (2024-2026)
- Covert channel detection literature
- CICIDS / UNSW-NB15 datasets
- XING security agent concepts

## Status
📋 Proposed → ⏳ In Progress
