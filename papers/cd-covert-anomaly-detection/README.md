# Auditing a Covert-Detection Simulation

**What this is.** An evidence audit of `FernandoMay/cd-ieee-package`, followed by a paper written
only from what the audit left standing. The audit found that the upstream package is exactly
reproducible but that 14 of its 20 quantitative claims are contradicted by its own committed
artifacts. The honest result is a *negative* one, and that is what this manuscript reports.

**What it claims.** At the operating point the upstream package reports (−85 dBm covert power,
four fused sensors), the detection benchmark is **saturated**: Isolation Forest attains AUC 1.0000
with zero dispersion in twenty of twenty seeds, and four of five detectors exceed 0.977. Paired
per-seed differences between the leading detectors are exactly zero in most trials, so the ranking
is not statistically recoverable. The saturation is caused by a modelling defect — simulated primary
users are generated with a per-sample random phase and are therefore spectrally flat, so the covert
band is distinguished only by aggregate power. In the only region where the problem is non-trivial,
the machine-learning detectors do not beat the energy baseline consistently, and distributed fusion
produces no measurable gain.

**What it does NOT claim.** No detection superiority, no robustness, no scalability, no novelty.
This manuscript cites **no prior work**, which it states as a novelty risk rather than papering over.
The underlying evidence has **no prior-work baseline at all**, which is a workshop-paper limitation
and is stated prominently in the Limitations section.

---

## Verdict on the audited package

| Question | Answer |
|---|---|
| Does the upstream code run? | Yes, unmodified, 4 min 43 s |
| Is the 20-seed artifact reproducible? | **Yes — byte-identical** |
| Does the upstream results table reproduce? | **Yes — to 4 decimal places, all 5 detectors** |
| Are the upstream paper's other claims true? | **14 of 20 contradicted by committed artifacts** |
| Is the 20-seed run statistically sound? | Honest, but the metric is saturated — it cannot rank detectors |
| Does the sensor-scalability figure have an artifact? | **No. Its claims are also false.** |
| Is the C reference kernel usable? | **No — memory-unsafe, aborts on every run** |

Full detail, with both values for every disagreement: **[EVIDENCE.md](EVIDENCE.md)**.

---

## Quick path

1. Read `EVIDENCE.md` — the complete audit, the claim table, and the six fatal findings.
2. Read `main.tex` — the manuscript (6 pages, IEEE conference format).
3. Reproduce the numbers:

   ```bash
   python scripts/stats.py        # derives every table number from data/metrics.json. No simulation.
   python scripts/make_figures.py # reads only data/, writes all five figures
   pdflatex main.tex              # 3 passes
   ```

4. To regenerate the two series the upstream code computes but never saves (optional, ~2 min):

   ```bash
   python scripts/recover.py
   ```

---

## How every number is traced

```
FernandoMay/cd-ieee-package  (commit 3bf8a4d)
        |
        |  re-executed unmodified, byte-identical output
        v
data/metrics.json              sha256 4242d117...   5 detectors x 20 seeds
        |
        |  scripts/stats.py  (no simulation)
        v
data/stats.json                every value in Table I, Table II and the inline text
        |
        +--> data/recovered_roc.json          scripts/recover.py
        +--> data/recovered_scalability.json  scripts/recover.py
                |
                |  scripts/make_figures.py
                v
        figures/*.pdf
```

No number in this paper was entered by hand. `upstream/cd_simulator.py` is a verbatim copy of the
committed simulator; `data/metrics.json` is byte-identical to the committed `figures/metrics.json`.

---

## Layout

| Path | Contents |
|---|---|
| `main.tex` | The manuscript. 6 pages, IEEEtran, 0 errors, 0 undefined refs, 0 overfull boxes. |
| `EVIDENCE.md` | The audit: claim-versus-artifact table, fatal findings, statistical assessment, minimum experiment set. |
| `data/metrics.json` | Byte-identical copy of the committed upstream artifact. |
| `data/stats.json` | Derived table values, CIs, paired differences, signal-model arithmetic. |
| `data/recovered_roc.json` | ROC point arrays, regenerated (upstream never persisted these). |
| `data/recovered_scalability.json` | AUC vs K, regenerated (upstream never persisted these). |
| `upstream/cd_simulator.py` | Verbatim copy of the committed simulator. |
| `scripts/recover.py` | Regenerates the two discarded series. |
| `scripts/stats.py` | Derives all table numbers from the committed artifact. |
| `scripts/make_figures.py` | Reads only `data/`; writes all five figures. |
| `figures/` | Five figures, each `.pdf` (vector, for LaTeX) and `.png`. |

## Figures

| Figure | Data file | Note |
|---|---|---|
| `fig_provenance` | `data/*.json` (sha256 read at build time) | The chain above |
| `fig_auc_distribution` | `data/metrics.json` | 20 seeds, mean ± 1 SD, two panels |
| `fig_auc_vs_power` | `data/metrics.json` | Sweep; n=1 per point, **paired** |
| `fig_roc_curves` | `data/recovered_roc.json` | Single 250/250/200 trial |
| `fig_auc_vs_sensors` | `data/recovered_scalability.json` | n=1 per cell, **unpaired** |

**Deliberately excluded:** the upstream feature-importance figure. Its labels are pseudo-labels that
split all-normal training data by index, and its two top-ranked features are identically 1.0
constants that `f_classif` scores as `NaN` and a descending sort therefore places first. There is no
correct version of it to report. The C kernel is excluded entirely — see EVIDENCE.md §F4.

---

## What was corrected, and why

The upstream abstract states an Isolation Forest AUC of 0.999; its body states 1.000. The artifact
records exactly 1.0000 in all twenty seeds, so the **abstract is wrong and the body is right**. This
manuscript reports the artifact value and carries a correction notice.

The upstream "AUC 0.600" for the cyclic detector is **not** an error: it is reproducible from
committed code at a different sample size (250/250/200), and it matches the legend of the upstream
figure. The 20-seed mean is 0.6367 and the paired sweep point is 0.6266. The real defect is that the
same upstream section reports three other detectors from a *different* run than the figure it cites —
so the section's text contradicts that figure's own legend on four of five detectors.

---

## Next step

If a positive paper is wanted, the minimum experiment set is in
[EVIDENCE.md](EVIDENCE.md#minimum-experiment-set-to-support-a-positive-paper). The two blocking
items are a prior-work baseline set on identical seeds, and a spectrally valid primary-user model
without which the problem stays a total-power test.
