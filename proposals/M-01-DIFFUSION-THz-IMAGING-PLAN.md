# Paper M-01 — ISCMI 2026 (Deadline: Sep 30)

## Paper
**Diffusion-Guided Image Reconstruction and Anomaly Detection over Severely Attenuated Terahertz Imaging Channels**

## Conference
- **Venue:** ISCMI 2026 — Soft Computing & Machine Intelligence
- **Dates:** Nov 18–20, 2026 | Vienna, Austria
- **Publication:** (Ei Compendex & Scopus)
- **Deadline:** September 30, 2026

## Research Questions
1. Can score-based diffusion models recover THz images from severely attenuated signals?
2. How can diffusion-guided reconstruction distinguish natural attenuation from malicious interference?
3. What is the reconstruction quality vs SNR tradeoff in THz imaging channels?

## Methodology
- **Model:** Score-based diffusion model adapted to THz scattering matrices
- **Reconstruction:** Guide denoising process with channel prior information
- **Anomaly Detection:** Distinguish natural attenuation from adversarial perturbation
- **Evaluation:** Synthetic THz imaging dataset with controlled attenuation levels
- **Metrics:** PSNR, SSIM, perceptual quality, detection accuracy, reconstruction time

## Key Components
```
THz Imaging Signal (attenuated)
       │
       ▼
Score-Based Diffusion Model
       │
       ▼
Channel Prior Integration
       │
       ▼
Denoising / Reconstruction
       │
       ▼
Anomaly Detection (natural vs adversarial)
```

## Expected Contributions
1. Novel diffusion-based approach for THz image reconstruction
2. Channel-prior-guided denoising for THz imaging
3. Dual-purpose reconstruction + anomaly detection framework
4. Benchmark on synthetic THz imaging dataset

## Timeline (Sep 22 – Sep 30)
- **Sep 22-24:** Diffusion model architecture + THz channel modeling
- **Sep 25-27:** Training pipeline + synthetic dataset generation
- **Sep 28-29:** Experiments + analysis
- **Sep 30:** Write paper + submit

## References
- Score-based diffusion models (2024-2026)
- THz imaging systems
- Anomaly detection in imaging
- Channel-aware reconstruction

## Status
📋 Proposed → ⏳ In Progress
