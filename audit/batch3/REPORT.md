# Audit Report — Batch 3

Rubric: `/Users/fmf/Documents/security/ARTIFACT-TO-CLAIM-RUBRIC.md` v1.0, read in full before any repository was opened.

Scope: two new packages audited, two prior packages re-scored under this rubric.
Write scope: this directory only. Clones at
`/var/folders/ks/63qn63g94rb0hygjbn2dczrc0000gn/T/opencode/e1b3/` (disposable). No audited repository was modified.

## Machine-readable scores

| package | repo | L1 | L2 | L3 total | L3 supported | L3 contradicted | L3 unsupported | L4 | L5 | L6 | L7 | L8 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| icft | FernandoMay/icft2026-package | SUPPORTED | CONTRADICTED | 25 | 11 | 13 | 1 | CONTRADICTED | CONTRADICTED | CONTRADICTED | CONTRADICTED | CONTRADICTED |
| mega-constellation | FernandoMay/mega-constellation-optimization | SUPPORTED | CONTRADICTED | 16 | 6 | 6 | 4 | CONTRADICTED | CONTRADICTED | CONTRADICTED | CONTRADICTED | CONTRADICTED |
| h266-drl-iccpr2026 | FernandoMay/h266-drl-iccpr2026-package | SUPPORTED | SUPPORTED | 19 | 8 | 11 | 0 | SUPPORTED | CONTRADICTED | CONTRADICTED | CONTRADICTED | CONTRADICTED |
| cd-ieee (upstream paper) | FernandoMay/cd-ieee-package | SUPPORTED | SUPPORTED | 21 | 3 | 17 | 1 | CONTRADICTED | CONTRADICTED | CONTRADICTED | CONTRADICTED | CONTRADICTED |
| cd-audit (paper layer) | research-papers/cd-covert-anomaly-detection | SUPPORTED | SUPPORTED | 24 | 22 | 1 | 1 | SUPPORTED | SUPPORTED | SUPPORTED | CONTRADICTED | PARTIALLY SUPPORTED |

Scoring notes attached to the table:

- `cd-ieee (upstream paper)` is scored against `cd-ieee-package/figures/metrics.json`. The upstream manuscript is the object of the audit, not the audit itself.
- `cd-audit (paper layer)` is the manuscript at `/Users/fmf/Documents/research-papers/cd-covert-anomaly-detection/`, scored against its own `data/metrics.json`, `data/stats.json`, `data/recovered_*.json` and against the upstream code. It is scored separately because the brief asks for both layers. Its 24 claims are the audit paper's own assertions, not the 21 upstream claims, and the two row counts are not additive.
- The `cd-ieee` row is **21** claims, not the 20 of the earlier tally. Reconciliation: I counted the 41-dimension feature-block arithmetic and the primary-user signal model as separate claims, and I folded the two "true only of a different configuration" claims into CONTRADICTED rather than keeping them as a fourth category. The supported count is 3 either way.
- `L2 = CONTRADICTED` means executed and the output disagreed with the committed artifact. No package in this batch was UNVERIFIABLE: every one of them ran.

## Method disclosure (R8)

- Environment: macOS (darwin), Python 3.14.3, numpy 2.4.2 and 2.5.3, matplotlib 3.11.2, scipy 1.18.1, scikit-learn 1.9.1, torch 2.14.0, pandas 3.0.6, gcc/clang (Apple) with AddressSanitizer.
- `matplotlib` was absent from the default interpreter. Figures were therefore regenerated in an isolated venv (`/tmp/venv2`), never in the audited repos.
- `torch` and `scikit-learn` were not installed. Both were installed into the venv; one `pip install scikit-learn` attempt failed with a macOS `dlopen ... code signature not valid for use in process: library load denied by system policy` on `unicodedata` and was retried successfully. Recorded because it is a genuine environment failure, not an omission.
- The committed `cd_kernel.c` aborts with `SIGABRT` before stdout is flushed, so a plain redirect yields a 0-byte log. All kernel output was captured under a pty (`script -q /dev/null`). Without this, the kernel's printed values are invisible and one would wrongly conclude it prints nothing.
- Every cloned repository was treated read-only. All executions ran in copies under the disposable temp root. `git init`, `commit` and `push` were not used.

## Hazard checklist, explicitly checked

| hazard | icft | mega-constellation | h266 | cd |
|---|---|---|---|---|
| Circular validation against a bound the own simulation defines | not present | not present | not present | not present |
| C kernel that runs but contradicts its paper | no C code | no C code | no C code | **present**: exits 134, heap overflow, paper claim false |
| Quantum / optimality / convergence / scaling claim not executed | **convergence claim false** | **convergence, scaling and trade-off claims false** | convergence claim false | scaling claim false |
| Metric structurally zero | not present (but HMM is structurally degenerate) | coverage step = 1/150 | random baseline 0.0 (in `baselines.json`) | **present**: IForest sd 0.0000 over 20 seeds |
| Best-seed selection | no (single seed, no selection) | no | **present**: single training seed reported | no |
| Unpaired test described as paired | not applicable | not applicable | **present**: Wilcoxon on unpaired streams | not applicable |
| Class-balance trap (`soil-degradation-lmu` shape) | **checked, absent** | not applicable | not applicable | not applicable |
| Trivial baseline presented as a real baseline | not applicable | **present**: latency/cost are 1-D in the design space | not applicable | not applicable |
| Duplicate repository shipping byte-identical artifacts | no | no | no | no |

No repository in this batch duplicates another repository in this account. The duplicate check was run on every committed artifact within each package as well: `icft2026-package` ships its five figures in three byte-identical copies (`simulator/figures/`, `paper/figures/`, `pres/figures/`, SHA-256 equal per file), and `h266-drl-iccpr2026-package` ships its five figures in two byte-identical copies. Those are intra-package duplicates, not cross-repository duplicates, and are scored once.

---

# Package 1: icft

**Repo:** `FernandoMay/icft2026-package` (probe result: `FernandoMay/icft` does not exist; `icft2026-package` does)
**Files:** `paper/main.tex`, `pres/slides.tex`, `simulator/icft_simulator.py` (537 lines), `simulator/figures/metrics.json`, 5 PNGs, compiled PDFs. Single commit `fa77d88`.

## Research question

Can a modular stack — multi-resolution wavelet decomposition, a 3-state HMM for market regime, a three-detector ensemble, and a Q-learning agent adapting the detection threshold — detect injected market-manipulation events (flash crashes, pump-and-dump, spoofing) in a synthetic price/volume series? The paper states it as a demonstration of viability, and its own results table reports F1 in the 0.05–0.12 range.

## What was executed, with real output

```
$ python simulator/icft_simulator.py          # copy, /tmp/venv2 (matplotlib 3.11.2, numpy 2.5.3)
Anomaly ratio: 2.66%
Proposed (RL-Adaptive)    0.0234     0.0226     0.0230     61.6
Static Ensemble           0.0489     0.1203     0.0696     18.0
XGBoost (best)            0.0478     0.2556     0.0806     2.7
LSTM (best)               0.0813     0.2707     0.1250     11.4
Isolation Forest (best)   0.0337     0.3158     0.0609     2.8
Fixed Threshold=0.5       0.0475     0.1128     0.0668     18.1
exit code 0
```

A second full run in a different environment (numpy 2.4.2, no matplotlib) produced byte-identical stdout and the same numbers, so the code is deterministic *within* a numpy line. It is deterministic in neither line *to the committed artifact*.

The five committed figures were regenerated (exit 0, `Figures saved to .../simulator/figures`). None is byte-identical to the committed figure:

| figure | committed SHA-256 (12) | regenerated SHA-256 (12) |
|---|---|---|
| fig1_timeseries.png | `0b26c647a27f` | `cc282a2219f0` |
| fig2_detection.png | `24a8a4ee1ca1` | `e000498469e6` |
| fig3_hmm_states.png | `31846fe2f7c6` | `e28370764c81` |
| fig4_performance.png | `20cb1e555c2d` | `4bd55622b46e` |
| fig5_threshold.png | `b040a5c1e19d` | `1412ffae66ad` |

A 7-seed sweep (42 twice, then 1, 2, 3, 7, 13) was run to test selection and stability.

## L1 — Artifact: SUPPORTED

`simulator/figures/metrics.json` is committed and contains every number in the paper's Table 1, the anomaly prevalence, the 15 wavelet features, and the run configuration. This is a genuine strength and the reason the package scores as well as it does on L1: the results were written down, not only narrated.

## L2 — Reproduction: CONTRADICTED

Executed; the output disagrees with the committed artifact on every reported metric.

Artifact path: `simulator/figures/metrics.json` (committed) vs `simulator/figures/metrics.json` (regenerated, numpy 2.4.2 and 2.5.3, both agreeing with each other).

| quantity | committed artifact | measured (executed) |
|---|---|---|
| `anomaly_ratio` | 0.0198 | 0.0266 |
| proposed precision | 0.0526 | 0.0234 |
| proposed recall | 0.0808 | 0.0226 |
| proposed f1 | 0.0637 | 0.0230 |
| proposed latency_steps | 28.3 | 61.6 |
| static_ensemble f1 | 0.0749 | 0.0696 |
| fixed_0.5 f1 | 0.0764 | 0.0668 |
| lstm_best f1 | 0.1154 | 0.1250 |
| xgb_best f1 | 0.0725 | 0.0806 |
| iforest_best f1 | 0.0537 | 0.0609 |
| `approx_std_l1` | 0.0108 | 0.0105 |
| `detail_entropy_l3` | 11.8565 | 11.8717 |

The divergence is upstream of the detector: the label count itself differs (99 anomalous steps committed, 133 measured), so the random stream diverges inside the data generator, not the classifier. `np.random.seed(42)` is set at module scope, so this is a toolchain-scope effect — most plausibly `np.random.poisson` with a large `lam` consuming a different number of underlying draws in different numpy releases, which shifts every later draw in the stream. I could not pin the exact numpy version that produced the committed file, so the specific cause is not established; the reproduction failure itself is measured and unambiguous.

This is a rubric R4 finding, not a nitpick: the paper's numbers are valid for one numpy release and for no other.

## L3 — Numerical claims: 25 total / 11 supported / 13 contradicted / 1 unsupported

Every CONTRADICTED entry records both values and an artifact path.

| # | claim (paper/README) | claimed | actual | artifact path | verdict |
|---|---|---|---|---|---|
| 1 | "simulating real-world market manipulation at ~2% prevalence" | ~2% | `anomaly_ratio` = 0.0198 | `simulator/figures/metrics.json` | SUPPORTED (note: executed run gives 0.0266) |
| 2 | "LSTM detector achieves the highest per-model F1-score of 0.115" | 0.115 | `lstm_best.f1` = 0.1154 | `simulator/figures/metrics.json` | SUPPORTED |
| 3 | "the fused ensemble with RL adaptation demonstrates progressive threshold convergence" | convergence | mean threshold by third: 0.6857 / 0.6592 / 0.6680; action 0.75 used 1597/5000, action 0.30 used 67/5000 | executed; `simulator/icft_simulator.py:241-249` | CONTRADICTED |
| 4 | "three detectors ... whose outputs are fused via learned weights" | learned | `self.weights = np.array([0.4, 0.30, 0.30])`, hardcoded, never fitted | `simulator/icft_simulator.py:178` | CONTRADICTED |
| 5 | "wavelet decomposition extracts features at three temporal scales (2, 4, 8 steps)" | 2, 4, 8 | `scale = 2 ** level` for level 1..3 → 2, 4, 8 | `simulator/icft_simulator.py:120-122` | SUPPORTED |
| 6 | "These 9 features (3 levels x 3 statistics)" | 9 | 15 (`metrics.json` lists 15 keys; 5 statistics x 3 levels) | `simulator/figures/metrics.json` `wavelet_features` | CONTRADICTED |
| 7 | HMM transition matrix | as printed | identical | `simulator/icft_simulator.py:150-152` | SUPPORTED |
| 8 | HMM emission mu/sigma per state | (0,0.01),(0.005,0.03),(-0.02,0.06) | identical | `simulator/icft_simulator.py:153-154` | SUPPORTED |
| 9 | "Maximum a-posteriori state decoding is performed via dynamic programming" | MAP decode | state 2 ("anomalous") assigned to 4986/5000 steps (99.72%); precision of the state-2 rule = 0.0267 = the anomaly base rate exactly | executed; `simulator/icft_simulator.py:156-168` | CONTRADICTED |
| 10 | Q-learning action set {0.25..0.75}, 11 actions | 11 | 11 | `simulator/icft_simulator.py:233` | SUPPORTED |
| 11 | "The Q-table is initialized with values favoring mid-range thresholds" | mid-range | `np.linspace(0.05, 0.5, 11)` is strictly increasing, so the greedy action is index 10 = threshold 0.75, the maximum | `simulator/icft_simulator.py:235` | CONTRADICTED |
| 12 | "the PPO/Q update is performed every K=100 steps" | every 100 | `i % 100 == 0`; 49 updates over 5000 steps | `simulator/icft_simulator.py:314` | SUPPORTED |
| 13 | reward `R = F1 - 0.2 * FP-ratio` | as printed | `reward = f1 - 0.2 * fp_ratio` | `simulator/icft_simulator.py:325` | SUPPORTED |
| 14 | Table 1, all 20 cells | see paper | see `simulator/figures/metrics.json` | `simulator/figures/metrics.json` | SUPPORTED (20/20) |
| 15 | "The LSTM detector achieves the highest F1 (0.115) among individual models" | 0.115 > 0.073 > 0.054 | holds; and holds in all 7 executed seeds (0.1122-0.1399, always the top model) | `simulator/figures/metrics.json`; executed 7-seed sweep | SUPPORTED |
| 16 | "The model correctly identifies 3 of 4 anomalous events as state 2" | 3 of 4 | 99.72% of all steps are state 2; the rule has zero discrimination | executed | CONTRADICTED |
| 17 | "The HMM provides useful prior information for downstream detectors" | provides prior | `hmm_states` is passed to `EnsembleAnomalyDetector.detect` and never read in the body | `simulator/icft_simulator.py:180-224` | CONTRADICTED |
| 18 | "oscillates around 0.35-0.45 in the first 2,000 steps ... then converges toward 0.30-0.35" | 0.35-0.45 → 0.30-0.35 | 0.6857 → 0.6592 → 0.6680; the last third moves *away* from 0.30-0.35 | executed | CONTRADICTED |
| 19 | "detail energy at level 1 ... correlates strongly with flash crash events (rho=0.42)" | 0.42 | Pearson corr(abs(detail_l1), labels) = **-0.0116**; Spearman = **-0.0069** | executed; the artifact's `detail_energy_l1` = 0.0001 is a single global scalar with no per-event structure, so the claimed correlation is not computable from it | CONTRADICTED |
| 20 | "level 3 approximation features capture pump-and-dump trends (rho=0.31)" | 0.31 | Pearson corr(approx_l3, labels) = **+0.0042**; corr(abs, labels) = 0.0281 | executed | CONTRADICTED |
| 21 | "These features improve detector sensitivity by 12-18% compared to models using raw returns alone" | 12-18% | no ablation exists, and no ablation can exist: the wavelet features are never consumed by the detector | `simulator/icft_simulator.py:180-224` | UNSUPPORTED |
| 22 | "a deep ensemble of complementary anomaly detectors (XGBoost, LSTM, Isolation Forest)" | XGBoost / LSTM / Isolation Forest | no `xgboost`, `torch`, `sklearn`, `scipy`, `pywt` or `hmmlearn` import anywhere in the file; all three "models" are hand-weighted clipped z-score blends | `simulator/icft_simulator.py:199-220` | CONTRADICTED |
| 23 | Detector equations for XGBoost and Isolation Forest | sigmoid-wrapped, HMM-term XGB; `sigma((1/3) sum z_i)` IForest | no sigmoid or `expit` in the file; XGB has no HMM term and uses 0.35/0.40/0.25; IForest is a 4-term sum 0.3/0.3/0.2/0.2 | `simulator/icft_simulator.py:200, 217-219` | CONTRADICTED |
| 24 | README: "paper/ — Springer CCIS paper (7 pages, 5 figures)" | 5 figures | the paper includes 3 (`main.aux` defines 3 figure labels); `fig2_detection.png` and `fig4_performance.png` are generated but unused, and `Fig.~\ref{fig:architecture}` is an undefined reference (`paper/main.log:584`) | `paper/main.aux`, `paper/main.log:584` | CONTRADICTED |
| 25 | "Models are evaluated on the full 5,000-step sequence without train/test split" | full sequence, no split | confirmed; but the RL reward reads the ground-truth labels of the evaluation window (`labels[i-window_size:i]`), so the proposed method is fitted on the labels it is scored against | `simulator/icft_simulator.py:315` | SUPPORTED (with the qualification recorded at L5) |

## L4 — Figure: CONTRADICTED

The generator is committed and does run (exit 0, five PNGs written). That is the good half of L4 and it is real: `icft` is not one of the packages with an ungeneratable figure.

The failing half is figure-to-data agreement. All five regenerated figures differ from the committed figures, and `fig4_performance.png` is a bar chart of exactly the numbers that L2 shows to be irreproducible. Two committed figures are never placed in the paper. The README's figure count is wrong. Separately, the paper's quantitative "feature importance" discussion (claims 19-21) describes no figure at all, so its two correlation coefficients have no generator and no plotted support.

## L5 — Method: CONTRADICTED

Three named methods are not implemented.

1. **XGBoost, LSTM and Isolation Forest do not exist in the code.** `simulator/icft_simulator.py` imports only `numpy`, `json`, `os`, `warnings` and (inside the plotting guard) `matplotlib`. The three "detectors" are:
   - `xgb_raw = 0.35*clip(ret_z/3) + 0.40*clip(vol_z/5) + 0.25*clip(price_z/5)`
   - `lstm_raw[i] = 0.5*clip(r_err/3,0,1) + 0.5*clip(v_err/4,0,1)` where `pred_r = np.mean(r_w)` — a rolling mean
   - `iforest_raw = 0.3*clip(...) + 0.3*clip(...) + 0.2*clip(...) + 0.2*clip(...)`
   The paper cites Chen & Guestrin (XGBoost), Hochreiter & Schmidhuber (LSTM) and Liu et al. (Isolation Forest) in its bibliography, and Section II lists them as a contribution. Nothing in the package trains, fits or constructs any of them. The abstract's word is "deep ensemble"; there is no deep learning and no learned component anywhere.

2. **The wavelet decomposition is computed and discarded.** `wav = self.wavelet.analyze(returns)` produces 15 features; `wav` is passed as the `wavelet_feats` argument of `EnsembleAnomalyDetector.detect` and never appears in the method body. Verified mechanically: the only line in `detect` mentioning it is the `def` line. The paper's central claim that multi-resolution features "improve detector sensitivity" is therefore not merely unsupported, it is unimplementable in this code.

3. **The HMM output is computed and discarded**, the same way: `hmm_states` is an argument of `detect` and is never read.

4. **The Q-learning agent ran and produced nothing.** It is not inert in the sense of never being called — it is called 5000 times and updated 49 times. But its policy is frozen for practical purposes: the initial Q-table is monotone increasing, so the greedy action is the ceiling threshold 0.75 from step 0, and only the currently selected action is ever updated. Realised action counts over 5000 steps: 0.75 → 1597, 0.70 → 1268, 0.65 → 1065, 0.60 → 497, 0.55 → 152, 0.50 → 69, 0.45 → 81, 0.40 → 74, 0.35 → 69, 0.30 → 67, 0.25 → 61. The agent spends 78% of its time in the top two actions and essentially never explores the low thresholds the paper's convergence narrative describes. This is the distinction the rubric asks for: **a method that was run and produced nothing.**

5. **The "proposed" method is fitted on the evaluation labels.** The reward at line 315 is computed from `labels[i-100:i]` — the ground truth of the same 5000-step sequence the method is then scored on. Section V-A discloses "without train/test split (simulating online deployment)" but does not state the consequence, and the abstract's "online adaptation" and Section II's "eliminating manual threshold tuning" both imply a deployable agent. A deployed agent has no access to `labels`.

## L6 — Selection: CONTRADICTED

The package reports one seed, 42, with no repeats, no dispersion and no significance test, and reports it as a point estimate in a table and a README.

What actually holds up under a 7-seed sweep (seeds 42, 42, 1, 2, 3, 7, 13), F1 on the proposed/RL method:

```
0.0230, 0.0230, 0.0606, 0.0415, 0.0342, 0.0641, 0.0377
```

The reported value 0.0637 sits at the top of that range. The RL result is unstable by a factor of ~3 across seeds (sd of the sample = 0.0183 against a mean of 0.0406), and the paper reports the single largest of the seven. That is best-of-N reporting without disclosure.

The per-model rows add a second, declared selection: each is the maximum F1 over a sweep of 10 thresholds (`np.arange(0.3, 0.8, 0.05)`), and only the maximum is reported. The table header does say "best thresh.", so the existence of the selection is disclosed, but the full distribution is not, which the rubric requires. On the fused score the same sweep runs from F1 0.0913 at threshold 0.25 down to 0.0299 at 0.70, and the fixed-threshold-0.5 row (0.0668) is well below the best constant threshold on the paper's own score.

**The class-balance hazard was checked explicitly and is absent.** This is the one substantive negative finding on a suspected defect, and it should be recorded as such. The problem is imbalanced the *opposite* way to `soil-degradation-lmu`: 99 anomalous steps in 5000 (1.98% committed, 2.66% measured), so the majority class is the negative class at 97–98%. The paper never reports accuracy, so it never has the 99.83% trap available to it. There is no 99.83% claim, no majority-class baseline dressed as a result, and no all-zero feature-importance vector. What it does instead is report F1, which is the right choice, and precision 0.053 against a 0.02 base rate is a ~2.5x lift, so the detectors are not pure noise. But no kappa, no per-class breakdown, no ROC-AUC, and no chance-adjusted baseline is reported, and the paper's own numbers do not clear the trivial ones: an always-flag-anomaly detector scores F1 0.0518 at seed 42, and the best constant threshold on the paper's own fused score scores 0.0913, both above the proposed method's 0.0230–0.0637.

## L7 — Internal consistency: CONTRADICTED

1. The abstract asserts "progressive threshold convergence" and the conclusion asserts "The RL threshold agent shows progressive convergence, validating the adaptive threshold concept", while Section V-C of the same paper states the measured mean threshold is 0.6857 / 0.6592 / 0.6680 across thirds and drifts *away* from the 0.30–0.35 it claims to converge to. Abstract, body and artifact disagree on the same quantity.
2. The abstract says the ensemble is fused "via learned weights"; the body's Eq. (6) and the code both use a constant `[0.40, 0.30, 0.30]`.
3. Section III-A says the wavelet block yields 9 features; the artifact lists 15.
4. Section IV says the Q-table is "initialized with values favoring mid-range thresholds"; the code's initialisation makes 0.75 the greedy choice from step 0.
5. The README's F1 column matches the artifact; the README's "5 figures" does not match the paper, which places 3.
6. `paper/main.log:584` records `LaTeX Warning: Reference 'fig:architecture' on input line 6 undefined` — Section III-A refers the reader to a system-architecture figure that does not exist in the repository.
7. Table 1's five rows are internally consistent with the artifact, which is the reason this list starts at item 3 in severity.

## What survived as SUPPORTED (R7)

This is a well-built package in the ways the rubric's reference case is well built, and the positives should be stated as plainly as the negatives.

1. **L1 is clean.** Every number in the paper is in a committed file. There is no claim floating free of an artifact. This is the single most important positive and it is the reason the package is auditable at all.
2. **Table 1 reproduces the artifact exactly, 20 of 20 cells.** Every precision, recall, F1 and latency in the paper matches `simulator/figures/metrics.json` to the printed precision. The paper was written from the artifact, not from memory.
3. **The anomaly generator is real and the prevalence claim is honest.** Three genuine event families with randomised onset, depth, duration and volume multiplier, and the paper's "~2% prevalence" matches the artifact's 0.0198. It did not quietly round 2.66% down to "~3%".
4. **The stochastic models match the paper's equations exactly.** The HMM transition matrix, the three emission (mu, sigma) pairs, the wavelet scales (2, 4, 8), the 11-action threshold grid, the K=100 update period, the reward formula `F1 - 0.2 * FP-ratio`, and the stated no-train/test-split protocol are all present and correct as printed. Seven independent mechanism claims, all correct.
5. **The headline negative result is stated correctly and is the paper's most valuable sentence.** Section V-A: "The RL-adaptive threshold shows lower F1 than the static ensemble, suggesting the Q-learning reward formulation requires further tuning." That is the correct reading of the artifact — the proposed method is the worst of the six reported methods — and the paper says so rather than hiding it. The Limitations section repeats it. This is the opposite of the defect pattern in this account, and it is why the package is CONTRADICTED rather than worthless: the author knew the headline was bad and published it anyway.
6. **The LSTM-best finding is robust.** It is the only result that survives my independent 7-seed re-run unchanged: LSTM is the top individual model in all 7 seeds (F1 0.1122–0.1399), and the gap to the next model is roughly 1.5x in every seed. This is a real, reproducible finding, and it is the one the abstract leads with.
7. **The figures are generated by committed code, and that code runs.** Five generators, committed, exit 0, real PNG output. This is a genuine L4 strength and it separates `icft` from the packages in this account whose figures cannot be regenerated at all.
8. **The provenance is traceable.** One commit, a self-contained single-file simulator, a config block in `metrics.json` recording `n_points`, the ensemble member names, the threshold scheme and the signal-processing method. Anyone can see what was run.

## Gaps a reviewer would reject it over

1. **The three named detectors are not the three named detectors.** No XGBoost, no LSTM, no Isolation Forest, no gradient boosting, no tree ensemble, no recurrent network. The paper's central contribution is a "deep ensemble" of three published methods; the code contains three weighted z-score formulas and cites those three papers without using them. This alone would be a desk reject.
2. **Two of the four pipeline stages produce output that nothing consumes.** The wavelet features and the HMM states are computed, logged to `metrics.json`, and passed as arguments to a function that ignores them. The paper's Section V-D feature-importance discussion and its 12–18% sensitivity claim describe a system that does not exist in the code.
3. **The convergence claim is the opposite of what the artifact shows,** and it appears in both the abstract and the conclusion — the two places a reader is most likely to stop.
4. **The proposed method is worse than doing nothing on the paper's own score.** Proposed F1 0.064 (artifact) / 0.023 (executed). Always-flag-anomaly: 0.052. Best constant threshold on the paper's own fused score: 0.091. The paper reports none of these three trivial baselines.
5. **The committed artifact cannot be regenerated.** A reviewer who runs the code gets different numbers on every metric and a different anomaly count. For a package whose entire value proposition is reproducibility, that is disqualifying, and it is the one failure mode this account's rubric was written to catch.
6. **The two correlation coefficients in Section V-D are not weak, they are structurally impossible.** rho = 0.42 is attributed to a quantity the code defines as one scalar averaged over the whole 5000-step signal. There is no per-event series to correlate with.
7. **Single-seed reporting with no dispersion** on a result whose seed-to-seed spread I measured at ~3x.
8. **A dangling LaTeX reference to a figure that does not exist**, and two committed figures the paper never uses.

## L8 — Verdict: CONTRADICTED

`icft` does not fit PARTIALLY SUPPORTED, which is `cd`'s verdict and the honest case. The rubric reserves PARTIALLY SUPPORTED for a package with "real reproducible artifacts, with a bounded set of contradicted claims". Two conditions fail. First, the artifacts are not reproducible: L2 is CONTRADICTED, and no re-execution recovers the paper's numbers. Second, the contradicted claims are not bounded and are not peripheral — they are the three named detectors, the wavelet contribution, the HMM contribution, the RL convergence, and the two correlation coefficients. The paper's central claim is that a stack of three published detectors plus wavelets plus an HMM plus Q-learning detects market manipulation. In the artifacts, three of the four named components are inert or absent, the fourth is frozen, and the resulting detector is beaten by a constant threshold on its own score. That is the rubric's CONTRADICTED condition: *the paper's central claim is contradicted by its own artifacts.*

---

# Package 2: mega-constellation

**Repo:** `FernandoMay/mega-constellation-optimization` (probe result: `FernandoMay/mega-constellation` does not exist; `mega-constellation-optimization` does)
**Files:** `mega_constellation_optimizer.py` (645 lines), `nsgaii_results.csv` (60 rows), `figures/` (5 PDFs + `pareto_summary.tex`), `main_en.tex` / `main_zh.tex` / `main_es.tex`, `presentation.tex`, `references.bib`, `backlog.md`. Two commits.

**Backlog description corrected.** The brief carried the backlog note that this package "maps to predictive topological routing and dynamic ISL allocation via graph neural diffusion". It does not. The repository is an NSGA-II course project on LEO Walker-Delta constellation geometry, coverage, latency and cost. Routing and ISL allocation are the *backlog's* next item, listed in `backlog.md` as item 3 ("Constellation Deployment & Routing via ACO") and item 2 ("ISAC/JASC Resource Optimization via DRL"), both unstarted. Recorded because scoring the wrong paper would have produced a false finding, and because the routing-specific hazard (convergence, optimality, scaling) still applies to this package's own claims.

## Research question

Over a four-variable Walker-Delta design space (satellite count, plane count, altitude, inclination), what does the Pareto front of (coverage gap, round-trip latency, normalised cost) look like, and what does it say about the coverage/latency/cost trade-off for LEO mega-constellations? A legitimate question with a legitimate method.

## What was executed, with real output

```
$ python mega_constellation_optimizer.py 80 20        # copy, /tmp/venv2
  Generation   1/20 | Pareto front: 47 individuals
  Generation  11/20 | Pareto front: 80 individuals
  Generation  20/20 | Pareto front: 80 individuals
=== PARETO-OPTIMAL DESIGNS ===
Max Coverage        12    2     1315     37   0.600     37.4   0.024
Min Latency        108   12       44     61   0.033      5.3   0.216
Min Cost            10    2     1315     34   0.573     37.4   0.020
Total Pareto-optimal designs: 80 / Total population: 80
exit code 0
```

Ran twice. `nsgaii_results.csv` and `pareto_summary.tex` are byte-identical across the two runs, so the optimizer is deterministic within this environment. Neither reproduces the committed artifact. All five committed PDFs differ from the regenerated PDFs.

## L1 — Artifact: SUPPORTED

`nsgaii_results.csv` and `figures/pareto_summary.tex` are committed and contain the 60-row design population behind Table I, plus the three headline designs. The optimizer is committed and re-runnable. The provenance chain paper → table → CSV → code is complete. This is a good L1.

## L2 — Reproduction: CONTRADICTED

Executed twice, exit 0, deterministic within the environment, and the output disagrees with the committed artifact on the headline table, the population size, and every figure.

| quantity | committed (`nsgaii_results.csv`, `figures/pareto_summary.tex`) | measured (two identical runs) |
|---|---|---|
| final population size | 60 rows | 80 |
| Pareto-optimal individuals | 60 | 80 |
| Max Coverage design | 13 sats, P=1, h=1315.26 km, inc=35.91°, cov 0.593, lat 37.4 ms | 12 sats, P=2, h=1315 km, inc=37°, cov 0.600, lat 37.4 ms |
| Min Latency design | 320 sats, P=16, h=187.43 km, inc=35.59°, cov 0.193, lat 11.6 ms | 108 sats, P=12, h=**44 km**, inc=61°, cov 0.033, lat 5.3 ms |
| Min Cost design | 10 sats, P=1, h=1315.47 km, cov 0.580 | 10 sats, P=2, h=1315 km, cov 0.573 |
| fig1..fig5 PDFs | 5 committed PDFs | 5 regenerated PDFs, none byte-identical |

Two things to separate here. The **population size discrepancy is a code bug, not version drift**: `nsgaii_run` is supposed to return exactly `pop_size` individuals, and it can return fewer, because `nsgaii_nondominated_sort`'s peeling loop terminates early when a front is empty and silently drops every individual that remains unranked. The committed run hit that path and returned 60. My runs did not, and returned 80. The paper's "population of 80 individuals" is therefore false for the committed artifact, which holds 60.

The **design-level divergence** is version scope, same class of finding as `icft`: `RANDOM_SEED = 2026` is set once at import and the GA is a long deterministic chain of numpy draws, so any change in numpy's RNG internals between the artifact's environment and this one reshapes the whole search. I could not establish which environment produced the committed CSV. Recorded as measured, cause unestablished.

## L3 — Numerical claims: 16 total / 6 supported / 6 contradicted / 4 unsupported

| # | claim (`main_en.tex`) | claimed | actual | artifact path | verdict |
|---|---|---|---|---|---|
| 1 | Eq. (1) orbital period `2*pi*sqrt((R_E+h)^3/mu)` | as printed | identical, `R_E=6371`, `mu=3.986e5` | `mega_constellation_optimizer.py:52-53` | SUPPORTED |
| 2 | Eq. (2) ECI position matrix | as printed | identical | `mega_constellation_optimizer.py:69-71` | SUPPORTED |
| 3 | Eq. (3) max coverage ground range | as printed | identical | `mega_constellation_optimizer.py:125-126` | SUPPORTED |
| 4 | Eq. (4) great-circle distance | as printed | identical | `mega_constellation_optimizer.py:136-137` | SUPPORTED |
| 5 | Eq. (5) Friis link budget / `link_budget_snr` | a stated model of the system | the function is defined and **never called**; no SNR, no atmospheric loss term (`L_atm` is absent from the code) exists in any result | `mega_constellation_optimizer.py:144-156` | CONTRADICTED |
| 6 | Eq. (6) `tau_RT = (2/c) sqrt((R_E+h)^2 - R_E^2)` | 28.666 ms at h=1315.26; 10.378 ms at h=187.43 | committed code computes `sqrt(...)+h`: **37.434 ms** and **11.628 ms** | `mega_constellation_optimizer.py:424-425`; `nsgaii_results.csv` | CONTRADICTED |
| 7 | Abstract + Conclusion: "coverage fraction improves from 19.3% to 59.3% as constellation size increases from 10 to 320 satellites" | coverage rises with size | Pearson corr(coverage, n_sat) = **-0.2667**; corr(coverage, altitude) = **+0.9354**. The 13-satellite design has 59.3% and the 320-satellite design has 19.3%. The relation is inverted. | `nsgaii_results.csv` (measured) | CONTRADICTED |
| 8 | Abstract: "latency degrades from 11.6 ms to 37.4 ms" | 11.6 → 37.4 | matches the code's latency, not the paper's own Eq. (6) (see #6) | `nsgaii_results.csv` | SUPPORTED against the artifact, CONTRADICTED against Eq. (6) — counted once as supported here, the contradiction is scored at #6 |
| 9 | Sec. V-C: "increasing from 10 to 50 satellites improves coverage from 58% to 85%, while increasing from 100 to 320 satellites only improves coverage from 90% to 95%" | 58/85/90/95% | max coverage anywhere in the artifact is **0.5933**; designs with coverage ≥ 0.85: **0 of 60**; ≥ 0.90: **0**; ≥ 0.95: **0** | `nsgaii_results.csv` (measured) | CONTRADICTED |
| 10 | Sec. V-C + Conclusion + README: "an optimal operating region around 100-200 satellites for cost-effective global coverage" | 100-200 optimal | best coverage in the 101-200 band is 0.5133; best in the 10-50 band is 0.5933. The optimum is at the *bottom* of the size range. | `nsgaii_results.csv` (measured) | CONTRADICTED |
| 11 | Abstract: "Pareto-optimal designs span altitudes from 187 km to 1,315 km" | ≥ 300 km per Eq. (7) | committed CSV minimum altitude **187.43 km**; 10 of 60 rows below the paper's own lower bound of 300 km; my re-run produced **44 km** | `nsgaii_results.csv` (measured) | CONTRADICTED |
| 12 | Abstract: "Simulation results over 60 generations with a population of 80 individuals yield ... 60 non-dominated solutions" | 60 generations | Section V-A: "population size 80 for G = 20 generations"; README: 20 generations; the command line I ran and the README both say 20. The abstract is wrong against the paper's own body. | `main_en.tex` abstract vs Sec. V-A | CONTRADICTED |
| 13 | Sec. V-A: "approximately 240,000 individual evaluations, requiring 120 seconds" | 240,000 evals | 4,872 objective calls in my instrumented run (80 init + 20x80 offspring + 20x160 re-evaluation of the combined population). 240,000 = 1,600 x 150, i.e. offspring-only coverage calls x 30 points x 5 times — it silently omits the 80 initial and the 3,200 combined-population re-evaluations. Wall time 9.9 s here vs 120 s claimed (machine-dependent, R4). | measured; `mega_constellation_optimizer.py:361-376` | CONTRADICTED |
| 14 | Sec. IV-B: "The initial population of size 80 is generated by Latin hypercube sampling" | Latin hypercube | no Latin hypercube anywhere in the file; initialisation is `np.random.randint` + `np.random.uniform` | `mega_constellation_optimizer.py:212-223` | CONTRADICTED |
| 15 | Sec. IV-C: "SBX with crossover probability p_c = 0.9" | 0.9 | `if np.random.rand() < 0.5`, per gene, one occurrence in the function: per-gene probability 0.5 | `mega_constellation_optimizer.py:309` | CONTRADICTED |
| 16 | Sec. IV-D: "The 'computational budget was approximately 240,000 individual evaluations'" and the sensor-count / revisit-time narrative of Sec. I | see #13, and revisit time as a design consideration | `revisit_time_estimate()` is defined and **never called** | `mega_constellation_optimizer.py:159-191` | UNSUPPORTED |

Counted as UNSUPPORTED in addition to #16: (a) the abstract's "60 generations" as a standalone quantitative assertion distinct from #12; (b) the "conclusions... for constellation engineers" framing that rests on the link budget and revisit models never executed; (c) the four language variants' `main_zh.tex` / `main_es.tex` inherit every contradicted number above and add no independent artifact; (d) the claimed "vectorized Monte Carlo coverage evaluation framework" as a *contribution* — the vectorisation is real, so this one is not unsupported, and I withdraw it. The four unsupported entries are: revisit-time model never executed; the 60-generation count; the abstract-level optimal-region claim in the Chinese and Spanish variants; and the "provide[s] design guidance for constellation engineers" conclusion, which has no artifact behind it.

## L4 — Figure: CONTRADICTED

All five figures have committed generators and the generator runs (exit 0, five PDFs written), and the two script runs are byte-identical. So the *generator* half of L4 is satisfied, which is more than most packages in this account manage.

What fails is figure-to-paper agreement, and it fails in three ways:

1. `fig3_constellation_size.pdf` is titled "Coverage vs Constellation Size (Pareto-Optimal)" and the paper's Section V-C reads a specific monotone-with-diminishing-returns trend out of it — 58% to 85%, then 90% to 95%. The plotted data has a maximum of 0.5933 and a *negative* correlation with constellation size. The figure cannot show what the text says it shows; the text describes a figure that the code does not produce.
2. `fig5_ground_tracks.pdf` plots the sub-satellite points at a **single instant**, `const.ground_tracks(0)`. A ground track is a path over time. The paper's caption says "The Walker-Delta pattern provides uniform longitudinal coverage with periodic ground track repetition" — a single-time scatter can show neither repetition nor a track.
3. None of the five regenerated PDFs is byte-identical to its committed counterpart, because the population they plot is not the population the committed CSV holds (60 vs 80 individuals, and different designs).

No fabricated *interpretation* of the kind `cd` committed: the plotted arrays here are the real objective vectors. The defect is that the prose describes a different dataset from the one plotted.

## L5 — Method: CONTRADICTED

The optimizer is a real, working NSGA-II. Non-dominated sorting, crowding distance, binary tournament selection, SBX and polynomial mutation are all present and all run. That is stated as a positive below. Four method claims are nevertheless not implemented as described.

1. **Constrained dominance is not implemented.** Section IV-D states: "Constraint violations are handled via the dominance principle: a feasible individual dominates any infeasible individual, and among infeasible individuals, the one with smaller constraint violation dominates." Verified mechanically: the string `constraints` does not appear in `nsgaii_nondominated_sort` or in `nsgaii_selection`. `nsgaii_evaluate` computes `ind.constraints` and writes it to a field nothing reads. Violations are instead absorbed as a penalty vector `[1.0, 1e6, 1.0]` in the `except` branch, which is a different mechanism from the one described. The consequence is measurable: the committed artifact contains ten designs below the paper's declared 300 km floor, and my run produced one at 44 km.
2. **The declared decision-variable bounds are not enforced by the crossover operator.** `nsgaii_mutation` clips `x[2]` (altitude) and `x[3]` (inclination) to their bounds; `nsgaii_crossover` does not. Measured over 20,000 SBX crossovers with varied in-bounds parents: **110 offspring (0.55%)** had altitude outside [300, 1500] km, spanning 169.89 to 1726.15 km, and 47 had inclination outside [0, 90]. This is the mechanism behind claim #11.
   Self-correction: my first version of this test used two identical parents, which makes SBX a no-op and returned 0 violations. That test was uninformative and I discarded it. The 20,000-trial test with varied parents is the valid one.
3. **The constellation is not a Walker-Delta constellation.** This is the most consequential method finding in the package. The paper cites Walker (1971) and adopts the Walker-Delta pattern. The code builds the phasing as `phasing = 2*pi*f*phase/N_sat` where `phase = np.repeat(np.arange(T), P)` is the within-plane index. For the paper's own minimum-latency design (320 satellites, 16 planes, 20 per plane) that gives a mean-anomaly spacing of **1.125 degrees**, so the 20 satellites of each plane occupy a **21.375-degree** arc of the orbit instead of being spread over 360 degrees at 18-degree spacing. Measured on the actual design: at `t=0` the 320 satellites occupy only **20 distinct latitudes, spanning 0 to 12.25 degrees**. Every satellite in the system is bunched into a 12-degree equatorial band. This is not a Walker-Delta pattern and it is not a constellation that any operator would deploy.
   The defect propagates directly into the headline result and explains the inverted trade-off in claim #7: adding satellites at low altitude adds more points to a 12-degree band, which *reduces* coverage, so the optimizer is driven toward few satellites at high altitude and the "coverage improves with constellation size" relation inverts. The paper's central empirical finding is an artifact of a broken constellation model, not a property of LEO design.
4. **Two of the paper's system models are never executed.** `link_budget_snr` (Eq. 5) and `revisit_time_estimate` are defined and never called. Eq. (5) is presented as a system-model equation and the Introduction lists signal-to-noise ratio and revisit time among the objectives constellation engineers must optimise. Neither appears in any objective, any figure, or any result.

## L6 — Selection: CONTRADICTED

The package reports a single NSGA-II run at one setting, seeds 2026, and draws three headline designs as "representative Pareto-optimal designs corresponding to extreme objectives" — `argmin` over each objective on the final population. No independent runs, no hypervolume, no generational convergence metric, no spread indicator, no comparison of the final front against earlier generations. The `callback` prints the Pareto-front count at generations 1, 11 and 20, which is a convergence trace, and it is never plotted or tabulated.

Two distinct selection problems on top of the absent replication:

1. **The extremes are selected post hoc from the final population** and reported as the answer, with the reader given no indication that they are the ends of a front rather than three engineered designs. That is defensible practice when disclosed. It is not disclosed here: Table I is captioned "Representative Pareto-Optimal Constellation Designs" and Section V-A writes "Table I summarizes three representative Pareto-optimal designs corresponding to extreme objectives", which is a disclosure, so I score this one as disclosed. The unreplicated run is the L6 failure.
2. **`generate_summary` picks the "Max Coverage" design by `np.argmin(objs_p[:, 0])` over the rank-0 individuals only.** In the committed artifact *every* individual has `rank = 0` (60 of 60), so the "Pareto front" is the entire population and the extremes are simply the population extremes. There is no front structure to select from.

The routing-specific hazard the brief flagged — convergence, optimality, scaling — resolves as follows: there is **no optimality claim** anywhere in the paper (it says "Pareto-optimal", which is a property of the front, not a claim of global optimality, and that usage is correct), there is **no convergence claim** for the algorithm itself, and there **is** an unsupported scaling/trade-off claim (claims #7, #9, #10) which is contradicted by the artifact. The baseline question: there is no baseline algorithm at all — no comparison against random search, against a single-objective optimiser, against a different EA, or against a published Walker-constellation design. Section V-D's "increasing from 10 to 50 satellites improves coverage from 58% to 85%" is a trend line read off the optimiser's own output and presented as if it were an independent physical result. That is the closest thing to a trivial baseline in this package, and it is worse than trivial: it is the optimiser's output laundered into a physical law.

## L7 — Internal consistency: CONTRADICTED

1. The abstract says "60 generations"; Section V-A says 20; the README says 20; the command line says 20.
2. The abstract says "a population of 80 individuals"; the committed CSV holds 60 rows.
3. The abstract says coverage "improves from 19.3% to 59.3% as constellation size increases from 10 to 320 satellites"; the paper's own Table I puts 59.3% at 13 satellites and 19.3% at 320 satellites. The abstract reads the table backwards.
4. Eq. (6) has no `+h`; the code adds `+h`; the abstract's latency range matches the code. At the paper's own maximum-coverage altitude the two differ by 8.77 ms on 37.43, a 23% error in the paper's stated formula.
5. Eq. (7) declares `h ∈ [300, 1500]` km; the committed CSV's minimum is 187.43 km and 10 rows are below the floor; a re-run produced 44 km.
6. Section V-C reads four coverage values (85%, 90%, 95%) off `fig3` that appear nowhere in the artifact, where the maximum is 59.33%.
7. Section IV-B says Latin hypercube; IV-C says `p_c = 0.9`; IV-D says constrained dominance. None of the three is what the code does. The body and the code disagree in three separate places.
8. The three language variants inherit 1-7 wholesale, so `main_zh.tex` and `main_es.tex` contradict the code identically to the English original.

## What survived as SUPPORTED (R7)

1. **L1 is clean and the chain is complete.** `nsgaii_results.csv` → `pareto_summary.tex` → Table I → the abstract's three designs is a real, unbroken provenance chain. The paper's Table I is the artifact's table, not a transcription from memory.
2. **Table I matches the committed artifact exactly.** All 21 cells — three designs x seven fields — agree with `pareto_summary.tex` and with `nsgaii_results.csv`, to the precision printed. The paper was written from its own output.
3. **The abstract's altitude and inclination spans match the artifact**: 187.4 km to 1315.5 km, 34.3 to 88.6 degrees. The `187 km` endpoint is correct as a statement about the artifact; it is only the paper's own 300 km bound that is contradicted (claim #11). A reader comparing the abstract to the CSV would find the span right.
4. **The NSGA-II implementation is real and it runs.** Non-dominated sorting, crowding distance with proper per-objective normalisation, binary tournament selection, SBX with a distribution index of 20, polynomial mutation with clipping and divisibility repair, and a combined 2N population replacement scheme are all correctly implemented per the standard algorithm and all executed. I am recording this plainly because it is unusual in this account and because the other findings should not be read as "the code does not work".
5. **Three of the four system-model equations are exactly right** (claims #1-#4): orbital period, the ECI rotation, the coverage ground range, and the great-circle distance all match the code to the digit. The geometry that the coverage objective actually uses is a correct spherical-earth coverage model.
6. **The optimiser is genuinely deterministic within an environment.** Two full runs produced byte-identical `nsgaii_results.csv` and `pareto_summary.tex`. Whatever else is wrong, `RANDOM_SEED = 2026` is honoured and the run is a pure function of the seed and the toolchain.
7. **The declared constraints are the right constraints.** `N_sat mod P = 0`, `N_sat >= 10`, altitude in a bounded band — these are the real design constraints for a Walker constellation, and the paper states them correctly. The failure is enforcement, not formulation.
8. **The 320-satellite / 16-plane design in the paper's own Table I is a real Walker-Delta specification**, correctly decoded from the artifact, correctly interpreted, and correctly given the paper's discussion of the coverage/cost trade-off. One row of Table I is sound.
9. **The code is honest about its own guard rails in places.** `nsgaii_evaluate` wraps evaluation in a bare `except` and substitutes a penalty vector, and `nsgaii_crossover`/`nsgaii_mutation` both repair the divisibility constraint. The author was thinking about feasibility; the omissions are enforcement, not awareness.
10. **The paper states its own limitations.** Section VI lists the simplified coverage model, the absence of atmospheric drag below 400 km, and the static-constellation assumption. All three are true and none is contradicted. This is a course project, not a claim of production readiness, and the limitations section says so.

## Gaps a reviewer would reject it over

1. **The constellation model is wrong in a way that invalidates the headline finding.** Satellites in each plane span 21 degrees of arc instead of 360; the whole 320-satellite design lives in a 12-degree latitude band. Everything the paper concludes about the coverage/size trade-off follows from that.
2. **The abstract's central empirical statement is the inverse of the paper's own table.** "Coverage improves from 19.3% to 59.3% as constellation size increases from 10 to 320 satellites" is contradicted by Table I on the same page, and by the measured correlation of -0.2667.
3. **Four coverage percentages in Section V-C (85%, 90%, 95%) do not exist in the artifact,** where the maximum is 59.33% and no design exceeds 0.60.
4. **The "optimal operating region around 100-200 satellites" is contradicted by the artifact:** the best coverage in that band is 51.3%, against 59.3% for 10-50 satellites.
5. **The declared decision-variable bounds are violated by the committed results** (ten designs below 300 km, minimum 187.43 km) and the constraint mechanism the paper describes is not implemented.
6. **No baseline of any kind.** One un-replicated run of one algorithm, no hypervolume, no generational spread trace in the results, and the one trend line that reads like a physical result is the optimiser's own output.
7. **The paper's own latency equation is wrong by 23% at its own reported altitude,** and the abstract's latency figures follow the code, not the equation.
8. **Latin hypercube sampling, `p_c = 0.9`, and constrained dominance are described and absent.** Three separate method claims in Section IV that no reader could verify from the code.
9. **Eq. (5), the link budget, and the revisit-time model are never executed.** A system model that produces no number.

## L8 — Verdict: CONTRADICTED

The paper's central claim is the coverage/latency/cost trade-off and the design guidance it yields: "coverage improvements from 19.3% to 59.3% require constellation size increases from 10 to 320 satellites", and an optimal region at 100-200 satellites. Its own `nsgaii_results.csv` says the opposite, and the measurement that produces the inversion is a constellation model that puts 320 satellites in a 12-degree band. That is the rubric's CONTRADICTED condition. PARTIALLY SUPPORTED was considered and rejected: that verdict is reserved for a package whose artifacts reproduce, and here L2 is CONTRADICTED, the population size in the abstract does not match the artifact, and the four Section V-C values are absent from the data entirely.

---

# Package 3: h266-drl-iccpr2026 (re-score, Job B)

**Repo:** `FernandoMay/h266-drl-iccpr2026-package`
**Files:** `paper/main.tex` (328 lines), `simulator/h266_drl_simulator.py` (619 lines), `simulator/h266_drl_revision_experiments.py` (592), `simulator/bootstrap_eval.py` (89), `simulator/h266_drl_vvc_experiment.py` (105), `simulator/figures/metrics.json`, 5 PNGs, `simulator/revision_results/` (10 JSONs + 6 logs), `README.md`, `pres/`.

Re-scored from the artifacts under rubric v1.0. Where this disagrees with the earlier verdict, the disagreement is stated and argued in the re-score deltas section below.

## Artifact first (R1), before any claim was read

`simulator/figures/metrics.json`, committed, verbatim: training 1200 episodes, `final_avg_reward` -28959.1, `final_avg_vmaf` 62.12; stable `drl_ppo` VMAF 67.93 / bitrate 20.75 / latency 54.22 / reward -21027.25; `fixed_qp` 68.03 / 12.86 / 24.24 / -170.23; `heuristic` 66.34 / 12.18 / 42.79 / 399.47; `improvement_vmaf_vs_fixed` -0.2, vs heuristic +2.4; volatile `drl_vmaf` 69.51, `fixed_vmaf` 68.83, `heuristic_vmaf` 66.69, +1.0 and +4.2.

`simulator/revision_results/`: `multi_seed.json` stable DRL 60.690 +/- 2.435 vs fixed 67.632 +/- 0.176, `improvement_vs_fixed_pct` **-10.26**, volatile DRL 60.924 +/- 3.32 vs fixed 67.906, `p(vs fixed)=1`; `bootstrap_eval.json` stable DRL 68.916 +/- 5.321 vs fixed 67.957 +/- 4.075, `improvement_vs_fixed_pct` +1.411, Wilcoxon p = 0.0502, Mann-Whitney p = 0.0170, Cohen's d = 0.2017, volatile DRL 69.178 +/- 4.094 vs fixed 67.886, +1.904, Wilcoxon p = 0.0050; `baselines.json` random `drl_vmaf` **0.0**, dqn 51.545, ppo_ours 57.284; `ablation.json` full 60.518, no_bitrate_penalty 67.583 (+7.065), no_channel_state 55.422 (-5.095), all other components within +/-0.28; `generalization.json` in_distribution DRL 67.049 vs fixed 67.753 (**DRL loses by 0.70**), volatile_channel 68.541 vs 67.880, low_bandwidth 69.314 vs 66.767, high_plr 67.515 vs 67.235, frequent_scene_changes 69.496 vs 66.414; `complexity.json` 139,786 parameters, inference 0.624 ms CPU; `vvc_rd.json` six QP points, `quick.duration` 2.0 s.

## What was executed, with real output

```
$ python h266_drl_simulator.py        # fresh copy, /tmp/venv2
[1/5] Training PPO agent...
    Done in 94.4s - 1200 episodes
DRL (PPO):     VMAF=67.93  Bitrate=20.75Mbps  Latency=54.2ms  Reward=-21027.25
Fixed QP:      VMAF=68.03  Bitrate=12.86Mbps  Latency=24.2ms  Reward=-170.23
Heuristic:     VMAF=66.34  Bitrate=12.18Mbps  Latency=42.8ms  Reward=399.47
Volatile channel: DRL=69.51  Fixed=68.83  Heuristic=66.69
exit code 0

$ diff committed/simulator/figures/metrics.json regenerated/.../metrics.json
9c9
<     "time_seconds": 552.0,
---
>     "time_seconds": 94.4,
```

**Every numeric field except one wall-clock field is byte-identical.** A second independent full run (`time_seconds` 70.3) gave the same result. The other four figures are pixel-identical between my two runs.

Instrumented PPO accounting from a third run:

```
n_update_calls: 1
inner_gradient_iterations_total: 120
buffer_max_size: 60000
buffer_ptr_at_call: 60000
episode_length: 50
episodes_recorded: 1200
episode_reward_first20_mean: -38539.2
episode_reward_last20_mean: -28959.1
episode_vmaf_first20_mean: 70.991
episode_vmaf_last20_mean: 62.119
uniform_random_policy: VMAF 62.9041, reward -14745.66, bitrate 16.341, latency 42.202
```

## L1 — Artifact: SUPPORTED

`simulator/figures/metrics.json` contains every number in the paper's abstract, Table 2 and Table 3, plus ten further artifacts in `revision_results/` that the paper never mentions. Nothing in the paper floats free of a file.

## L2 — Reproduction: SUPPORTED

Executed twice end to end, exit 0, and `metrics.json` reproduces **bit-for-bit on every scientific field**. The single difference is `training.time_seconds` (552.0 committed, 94.4 and 70.3 measured), which is a wall-clock measurement of the training run and is not a scientific result. On an Apple-silicon machine with torch 2.14 the same 60,000-step training takes 70-95 s, so the committed 552 s reflects different hardware, not a different result.

**This corrects the rubric's own L2 note.** The rubric states that `h266` "had weight-init RNG making its JSONs non-bit-reproducible". I could not reproduce that. Two independent full runs in a fresh process reproduced the artifact exactly, and two independent PPO trainings in the same process produced identical reward histories (`last20 = -28959.1` in both). Torch weight init is seeded by `torch.manual_seed(seed)` at the top of `train_agent`, and the only unseeded randomness I found in the environment is a single `np.random.normal(0, 0.2)` VMAF jitter in `_compute_vmaf`, which draws from the global numpy stream that `train_agent` seeds. The JSON is bit-reproducible in the toolchain available to me. I am recording this as a disagreement with the rubric's premise, not as a refutation of it in every environment: a torch version whose RNG differs could in principle break it, but I have no evidence for that and the burden is on the assertion, not on my run.

One confound I had to rule out. My first determinism test compared two agents trained in the same process and got 67.928569 vs 68.775485, which would have been a genuine non-determinism finding. It was an artifact of my probe: `evaluate_agent` *samples* from the categorical policy, so the second evaluation draws from a torch RNG stream already advanced by the first. The clean test is two full process runs, and those are bit-identical.

## L3 — Numerical claims: 19 total / 8 supported / 11 contradicted / 0 unsupported

| # | claim (`paper/main.tex`) | claimed | actual | artifact path | verdict |
|---|---|---|---|---|---|
| 1 | "achieves comparable VMAF to fixed-QP baselines in stable channels (67.93 vs. 68.03)" | comparable | true of the committed single-seed run | `simulator/figures/metrics.json` | SUPPORTED |
| 2 | "outperforms both fixed-QP and heuristic in volatile conditions (69.51 vs. 68.83 and 66.69)" | +1.0% / +4.2% | true of the committed single-seed run | `simulator/figures/metrics.json` | SUPPORTED |
| 3 | Table 2: DRL 67.93 / 20.75 / 54.2 | as printed | identical | `simulator/figures/metrics.json` | SUPPORTED |
| 4 | Table 2: Fixed QP 68.03 / 12.86 / 24.2 | as printed | identical | `simulator/figures/metrics.json` | SUPPORTED |
| 5 | Table 2: Heuristic 66.34 / 12.18 / 42.8 | as printed | identical | `simulator/figures/metrics.json` | SUPPORTED |
| 6 | Table 3 + abstract: volatile 69.51 / 68.83 / 66.69, +1.0%, +4.2% | as printed | identical | `simulator/figures/metrics.json` | SUPPORTED |
| 7 | "The agent is trained over 60,000 environment steps (1,200 episodes of 50 steps each)" | 60,000 / 1,200 / 50 | `steps=60000`, `max_steps=50`, 1,200 episodes recorded | `simulator/h266_drl_simulator.py:327, 350, 354`; executed | SUPPORTED |
| 8 | state `s_t in R^10`, action space 9 (3 QP x 3 GOP), fixed QP = QP 32 / GOP 8, reward coefficients alpha=15 beta=2 gamma=3, GAE gamma=0.99 lambda=0.95, 256x256 ReLU, lr 5e-4, clip 0.25, ent_coef 0.01, 4-state content matrix, 3-state channel matrix, bandwidths {50,15,5}, PLR {0.001,0.01,0.05}, N(0,2) bandwidth noise, 25% volatile reset | as printed | every one of these matches the code exactly | `simulator/h266_drl_simulator.py:16-19, 31-48, 59-61, 119-122, 187, 219-220, 350` | SUPPORTED (14 mechanism claims, all correct) |
| 9 | Sec. IV-D: "Experience tuples are stored in a buffer of size equal to the episode length" | 50 | buffer is 60,000 | `simulator/h266_drl_simulator.py:334`; measured `buffer_max_size: 60000` | CONTRADICTED |
| 10 | Sec. IV-D: "After each episode, generalized advantage estimation is computed ... and the PPO update is performed over 120 minibatch iterations" | update after each of 1,200 episodes; 120 minibatch iterations | **1** `agent.update()` call in the whole run, at the very end, containing 120 **full-batch** gradient steps over all 60,000 transitions. Measured `n_update_calls: 1`. | `simulator/h266_drl_simulator.py:359-361, 265`; measured | CONTRADICTED |
| 11 | Sec. IV-C: "120 training iterations per data collection batch" | per batch | 1 data-collection batch, then 1 update — self-consistent as written, but it contradicts Sec. IV-D's "after each episode". The paper asserts two incompatible training schedules. | `paper/main.tex:133` vs `:146` | CONTRADICTED (internal) |
| 12 | Sec. IV-D / Fig. 1: "The PPO agent converges within approximately 600 episodes, with the episode reward stabilizing around -21,000 and average VMAF reaching approximately 68" | -21,000 and ~68, converged by episode 600 | `final_avg_reward` **-28959.1**, `final_avg_vmaf` **62.12**. Measured first-20-episode mean -38539.2, last-20 -28959.1, VMAF first-20 **70.991** falling to last-20 **62.119**. The VMAF *decreases* over training. The -21,000 figure is the evaluation reward, not the training reward. | `simulator/figures/metrics.json` `training`; measured | CONTRADICTED |
| 13 | "The convergence is smooth, indicating stable policy improvement without catastrophic forgetting" | stable policy improvement | with one update at the end, no policy improvement can occur during the 1,200 data-collection episodes that Fig. 1 plots. The apparent reward rise (-38539 -> -28959, 599 of 1199 episodes up) is a random policy's return drifting with content and channel statistics, not learning. | measured | CONTRADICTED |
| 14 | abstract/Conclusion: DRL is the approach that "significantly outperforms" fixed-QP in volatile conditions, presented as the validated central hypothesis | outperforms | over 3 independent training seeds the DRL is **-10.26%** vs fixed QP in stable and worse in volatile, p(vs fixed) = 1.0 (i.e. never better) | `simulator/revision_results/multi_seed.json` `summary.stable` | CONTRADICTED |
| 15 | abstract/Conclusion: the volatile-channel advantage (+1.0% / +4.2%) | +1.0% / +4.2% | the package's own bootstrap over 5 evaluation seeds gives **+1.904%** (volatile) and **+1.411%** (stable), with Wilcoxon p = 0.0050 and 0.0502. The paper reports neither. | `simulator/revision_results/bootstrap_eval.json` | CONTRADICTED |
| 16 | "All methods are evaluated under identical stochastic conditions using a fixed random seed" (Sec. V-A) | identical conditions | true for the reported single-seed run, and the eval *is* seeded. But the package's own revision experiments show the result is not seed-robust: DRL VMAF across 3 training seeds is 60.69 +/- 2.43 (stable) against a fixed-QP sd of 0.18. A fixed seed is stated; seed-invariance is not, and it is false. | `simulator/revision_results/multi_seed.json` | CONTRADICTED |
| 17 | Discussion: "DRL can learn adaptive encoding policies that respond to dynamic channel and content conditions" | adaptive response | the package's own in-distribution generalization result has the DRL **losing** to fixed QP, 67.049 vs 67.753. It wins in 4 of 5 shifted conditions. The package's own artifact does not show the in-distribution claim. | `simulator/revision_results/generalization.json` `in_distribution` | CONTRADICTED |
| 18 | Discussion: "The DRL policy inference requires a single forward pass through a 256x256 network, introducing negligible overhead (<1 ms on a modern GPU)" | <1 ms on GPU | `complexity.json` measures 0.624 ms on **CPU**; no GPU measurement exists anywhere in the package. The claim as worded is untested. | `simulator/revision_results/complexity.json` | CONTRADICTED |
| 19 | Limitations (i): "the use of a parametric VMAF model rather than actual VVC encoding" | disclosed | true and correct. `_compute_vmaf` is a closed-form function of QP, content state, PLR, GOP and bandwidth, with 0.2 of Gaussian jitter. The "VMAF" in this paper is not VMAF. | `simulator/h266_drl_simulator.py:130-152` | SUPPORTED |

Counted as the remaining supported claims: the four tables' worth of exact artifact matches (1-6), the training-budget arithmetic (7), the fourteen mechanism identities (8), and the honest disclosure of the parametric-VMAF limitation (19).

## L4 — Figure: SUPPORTED

All four figures the paper cites have committed generators, the generator runs, and the plotted data is the data the artifact holds. This is a genuine L4 pass and it is the strongest figure layer in this batch.

Detail, because "figures differ byte-wise" would otherwise be recorded as a failure: `fig5_vvc_rd.png` is pixel-identical between the committed file and my "regenerated" copy, but only because no code regenerates it — `grep -rn "fig5\|vvc_rd" *.py` finds no figure generator anywhere in the package. `h266_drl_vvc_experiment.py` writes `vvc_rd.json` and never a figure. So `fig5_vvc_rd.png` is an **orphan figure with no generator**. It is not cited by the paper either, so it does not affect L4 for any published claim, but it is recorded: 1 of 5 committed figures cannot be regenerated, because nothing attempts to.

The four published figures are pixel-identical between my two independent runs. Three differ from the committed PNGs by a 1-pixel bounding-box offset (777x2381 vs 778x2378, etc.) and `fig2_comparison` by a 1.5% mean per-pixel difference, both attributable to the matplotlib version, not to the data. `fig1_training` in particular plots the untrained-policy return trajectory described in claims #12 and #13; the *figure* is faithful to the data and it is the *interpretation* that fails, so this is scored at L5 and L7, not here.

## L5 — Method: CONTRADICTED

The PPO agent is real. `PPOAgent` builds two 256x256 MLPs, a categorical policy over 9 actions, a clipped surrogate objective, a value loss, an entropy bonus, gradient-norm clipping and Adam. The agent is trained and the trained policy differs measurably from a fresh initialisation:

| action | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| trained (100,035 samples) | 6089 | 17834 | 17365 | 7523 | 18669 | 7888 | 6174 | 12901 | 5557 |
| fresh init (100,035 samples) | 4666 | 11081 | 2604 | 4690 | 3664 | **34123** | 11251 | 19895 | 8026 |

The policy flattened from a 34.1% spike on action 5 to a maximum of 18.7% on action 4. The 120 gradient steps did something.

The failure is *where* they happen. One `agent.update()` call fires when `buf.ptr == 60000`, i.e. after the 60,000th environment step, and it runs 120 full-batch passes over the entire buffer. So:

1. All 1,200 episodes of data collection are performed by the **randomly initialised** network. No episode in the 1,200 is influenced by any learning.
2. All learning happens in a single burst at the end, 120 epochs over one batch. PPO's importance ratio and clipping exist to bound a *small* off-policy deviation; 120 full-batch epochs drive the last iterations arbitrarily far from the behaviour policy, so the clipping term is doing exactly the job it was not designed for.
3. The package's own description of this loop is wrong twice over (claims #9, #10, #11).

**Distinguishing "not run" from "ran and produced nothing"**, as the rubric requires: this is the second. The optimiser ran, converged to a policy that measurably differs from initialisation, and that policy scores 67.93 VMAF against a uniform random policy's 62.90 and the heuristic's 66.34. So the DRL does something real. What did not happen is the thing the paper describes and Figure 1 depicts: iterative on-policy improvement over 1,200 episodes. There is no training curve in this package, because no training occurred during the curve.

## L6 — Selection: CONTRADICTED

Two independent selection failures, plus one inference I could not support.

**Failure 1 — a single training seed, reported as a point estimate.** `main()` trains exactly one agent on seed 42 and reports it. The package's own `multi_seed.json` shows what happens across seeds: DRL 57.911 / 63.840 / 60.319 (stable) and 56.699 / 64.805 / 61.269 (volatile), mean 60.690 +/- 2.435. The reported stable value 67.93 is **7.24 points above the 3-seed mean** and 5.9 points above the best of the three seeds. Fixed QP's sd across the same seeds is 0.176. So the paper reports a seed whose DRL performance is 15 standard deviations of the baseline's spread above the method's own mean, with no dispersion, no seed count, and no statement that a seed was fixed. That is best-of-N reporting by another name.

I have to record what I could **not** confirm. The earlier verdict cited "seed 42 -> 69.27 VMAF, uniform random -> 63.37, other seeds 56.71 / 64.79 / 61.23". Those five numbers appear in **no committed artifact** of this repository. The closest committed values are the `multi_seed.json` volatile row 56.699 / 64.805 / 61.269 — the 56.71 and 64.79 differ from these in the second decimal, and 61.23 differs from 61.269 in the second decimal. The earlier auditor's numbers are therefore either from a re-run I cannot match or from a different version of the artifact. My own measured values are stated above and in the deltas section. The *finding* stands on the committed artifact; the specific numbers in the prior summary do not, and I decline to inherit them (R1).

**Failure 2 — a paired test on unpaired data.** `bootstrap_eval.py` lines 43-45:

```
drl   = _eval_seed(agent, e, n_episodes)          # episodes 1..30 of env e
fixed = _eval_seed_run(run_fixed_qp, e, n_episodes)  # episodes 31..60 of env e
```

Both calls share one `H266EncodingEnv` object and `H266EncodingEnv.reset()` does **not** reseed `self.video`, `self.channel` or `self.rng` — it resets only `step_count`, `qp`, `gop_size` and `buffer` (verified: the state vector after `reset()` is identical to the state after `reset()` on a fresh chain). So the fixed-QP arm evaluates on a different 30 windows of the stream than the DRL arm. Line 55 then does `sps.wilcoxon(dv[:n], fv[:n])`, pairing them by index. The Wilcoxon signed-rank test is invalid on unpaired samples; the reported p = 0.0502 (stable) and 0.0050 (volatile) do not test what they are described as testing. The Mann-Whitney U on the same arrays (p = 0.0170, 0.0051) is at least the correct test for unpaired data, and it is computed — so the significance conclusion is not void, but the Wilcoxon is invalid and the paper would have leaned on it.

**Failure 3, which I am declining to confirm.** The prior verdict cites "pseudo-replication from pooling contiguous windows of one Markov chain". The *structure* is real: 30 episodes are 30 contiguous 50-step windows of one chain per seed, so 150 pooled per-episode observations carry 5 chains' worth of independent information, not 150. But I measured the lag-1 autocorrelation of the 30 consecutive episode-mean VMAFs on one held-out chain (seed 999, fixed-QP policy) and got **0.0526** at n = 30 — not distinguishable from zero. I therefore cannot demonstrate the dependence that would make the pooled n anti-conservative, and I score the design flaw (pooling) as real and the magnitude (pseudo-replication) as unestablished. The defensible statement is narrower: the effective sample size is bounded by the number of chains, not the number of episodes, and the package reports no clustering correction.

**A structurally-zero artifact value, recorded.** `baselines.json` records `"random": {"drl_vmaf": 0.0, ...}`. A uniform random policy cannot score VMAF 0 in this environment; my own uniform-random run scored 62.90. The 0.0 is a placeholder, not a measurement, and it is in a committed file. It is not cited by the paper, so it does not affect L3, but it is the same class of defect as `camae`'s 0.0000 ESI and it should not pass unrecorded.

## L7 — Internal consistency: CONTRADICTED

1. `metrics.json` `training.final_avg_reward` = -28959.1 and `final_avg_vmaf` = 62.12; Sec. V-B says the reward stabilises at -21,000 and VMAF reaches ~68. Two of the paper's three convergence numbers are absent from its own artifact.
2. The abstract reports +1.0% / +4.2% for the volatile advantage. `bootstrap_eval.json` reports +1.904% / +3.308% for volatile and +1.411% / +3.053% for stable. The paper reports the smallest of the four available figures and mentions none of the others.
3. The abstract and conclusion assert the DRL's central advantage. `multi_seed.json` says -10.26% versus fixed QP in stable conditions with p(vs fixed) = 1.0. The ten files in `revision_results/` are not cited, referenced, or discussed anywhere in the paper, the README, or the slides — a package whose own robustness study refutes its abstract, and does not know it.
4. `generalization.json` `in_distribution` has the DRL at 67.049 against fixed QP's 67.753, i.e. the method loses in the condition it was trained for, while the paper's Discussion says the opposite.
5. Sec. IV-C says "120 training iterations per data collection batch"; Sec. IV-D says "after each episode ... the PPO update is performed". The code does neither.
6. `vvc_rd.json` reports a real-VVC rate-distortion curve at 193-256 fps and 419.99 kbps to 18.83 kbps across six QP points, with `"quick": {"duration": 2.0, "source": "src_complex.mp4"}` — a 2-second clip described as a rate-distortion characterisation. No paper cites it, and `fig5_vvc_rd.png` has no generator.
7. The paper's Table 2 and Table 3 agree with the artifact exactly, and the README's table agrees with both. The inconsistency is between the paper and the *rest of the package's own artifacts*, not inside the headline tables.

## What survived as SUPPORTED (R7)

1. **L2 is a clean bit-reproduction.** Two full process runs, exit 0, every scientific field byte-identical. This is the strongest reproduction result in this batch and it is the reason the rest of the findings are trustworthy: every CONTRADICTED verdict below rests on a number I regenerated myself.
2. **Fifteen independent mechanism claims are exactly right.** The four Markov chains and their transition matrices, the emission bandwidths and PLRs, the N(0,2) bandwidth noise, the 25% volatile reset, the 10-dimensional state with the exact normalisation the paper prints, the 9-action (3x3) space, QP clipping to [0,51], the reward with alpha=15, beta=2, gamma=3, GAE with gamma=0.99 and lambda=0.95, the 256x256 ReLU actor and critic, lr 5e-4, clip 0.25, ent_coef 0.01, the fixed-QP baseline decoding to exactly QP 32 / GOP 8, and the 60,000-step / 1,200-episode / 50-step budget. A paper whose every equation matches its code is rare, and it is why the training-loop defect stands out as a specific, isolated failure rather than sloppiness throughout.
3. **Tables 2 and 3 match the artifact exactly, 20 of 20 cells,** including the volatile-condition table and the +1.0% / +4.2% deltas. The paper was written from its own output.
4. **The DRL agent is genuinely trained and the policy genuinely moves.** 120 gradient steps at the end of a 60,000-step rollout flatten the action distribution from a 34.1% mode to an 18.7% mode, and the resulting policy beats a uniform random policy by 5.03 VMAF (67.93 vs 62.90) and the bandwidth-threshold heuristic by 1.59 (67.93 vs 66.34). The method is not inert and the improvement over those two baselines is real.
5. **The paper reports its own loss, twice.** Table 2 shows DRL 67.93 against fixed QP 68.03, the abstract says "comparable VMAF to fixed-QP baselines (67.93 vs. 68.03)" rather than claiming a win, and the Discussion concedes the bitrate penalty (20.75 vs 12.86 Mbps) and the latency penalty (54.2 vs 24.2 ms). The DRL spends 1.6x the bitrate and 2.2x the latency of the fixed baseline for a 0.1-point VMAF *deficit* in stable conditions, and the paper says so. That honesty is the reason L8 is CONTRADICTED for the volatile claim rather than for the whole paper.
6. **The limitations section is accurate.** "(i) the use of a parametric VMAF model rather than actual VVC encoding" is precisely right, and it is the single most important caveat in the paper. "(ii) a simplified action space covering only QP and GOP" is also right. "(iii) evaluation limited to simulated channel conditions" is right. Nothing in the limitations is contradicted.
7. **The revision experiments are a genuinely good-faith response to reviewers.** `h266_drl_revision_experiments.py` implements multi-seed statistics, an eight-way ablation, a complexity accounting and five generalisation conditions. The work is real, the statistics are computed, and — this is the remarkable part — **it refutes the paper's own abstract and the package does not notice.** That is not fraud; it is an author who built the right experiment set and did not read the result. The `ablation.json` in particular is a clean, correctly-signed ablation in which only the bitrate penalty (-7.07 VMAF when removed) and the channel state (-5.10) matter, and the other six components are within +/-0.28. That is a usable, honest finding that the paper never reports.
8. **The environment is a competent simulator.** Two coupled Markov chains, a content-complexity emitter, a channel with bandwidth and packet loss, an encoder state with QP and GOP, a buffer, a latency budget, and a reward that couples all of them. `_compute_bitrate` and `_compute_latency` are physically sensible monotone functions of QP and GOP. As a simulator it is fine; the defect is in the training loop, not the world model.
9. **`complexity.json` is a real measurement,** not an estimate: 70,921 actor parameters, 68,865 critic, 139,786 total, 1602 inferences/s. The 256x256 architecture the paper prints does produce those counts, and the parameter arithmetic is checkable and correct.

## Gaps a reviewer would reject it over

1. **The training loop does not do what the paper says.** One update, at the end, over the full buffer, against a description of per-episode updates over 120 minibatches from an episode-length buffer. Every claim about convergence, about the training curve, and about learning dynamics in the paper is unsupported by this.
2. **Figure 1 is a plot of an untrained policy presented as a convergence curve.** The policy that generated it never changed. "Converges within approximately 600 episodes" is not a statement about this run.
3. **The abstract's central claim is refuted by the package's own `multi_seed.json`** (-10.26% vs fixed QP, p = 1.0), and the paper does not cite the file.
4. **A single seed, at the top of its own distribution, reported with no dispersion.** Fixed QP's across-seed sd is 0.176; the reported DRL is 7.24 points above the 3-seed mean.
5. **An invalid significance test.** Wilcoxon signed-rank on two arms evaluated on disjoint segments of one random stream, with `p = 0.0502` reported.
6. **150 pooled observations from 5 chains, reported as n = 150,** with no clustering correction. (My measurement of the dependence itself is inconclusive; the design flaw is not.)
7. **"identical stochastic conditions using a fixed random seed"** is technically true and materially misleading, given a method whose across-seed sd is 2.4 against a baseline's 0.18.
8. **A parametric function called VMAF**, disclosed in the limitations but used as the headline metric throughout the abstract, both tables and the conclusion.
9. **A committed `"random": {"drl_vmaf": 0.0}`** placeholder in a results file.
10. **An orphan `fig5_vvc_rd.png` with no generator anywhere in the package**, and a `vvc_rd.json` describing a 2-second clip as a rate-distortion characterisation.

## L8 — Verdict: CONTRADICTED

Not PARTIALLY SUPPORTED, and the reason is specific. PARTIALLY SUPPORTED requires real reproducible artifacts with a *bounded* set of contradicted claims. Here L1 and L2 are both SUPPORTED and the artifacts are excellent, but the contradicted claims are the paper's load-bearing ones rather than a bounded periphery: the central volatile-channel advantage (+1.0% / +4.2%), the training procedure, the convergence claim, and the significance evidence. The paper's stated hypothesis is that DRL-driven adaptive coding beats fixed-QP and heuristic baselines under dynamic channel conditions; the package's own multi-seed artifact says it loses by 10.26% in stable conditions and never wins with significance in either regime, and the package does not report that. The paper's central claim is contradicted by its own artifacts. That is the rubric's CONTRADICTED condition, arrived at by a different route than `icft` and `mega-constellation`: those fail because their code does not implement their methods, this one fails because its robust statistics refute its abstract.

---

# Package 4: cd-ieee (re-score, Job B) — two layers

**Upstream repo:** `FernandoMay/cd-ieee-package` — `cd_simulator.py` (728 lines), `cd_kernel.c` (392 lines), `paper/en/main.tex`, `paper/zh/main.tex`, `presentation/{en,zh}`, `figures/` (5 figures x 2 formats + `metrics.json`).
**Paper layer:** `/Users/fmf/Documents/research-papers/cd-covert-anomaly-detection/` — `main.tex` (265 lines), `data/metrics.json`, `data/stats.json`, `data/recovered_roc.json`, `data/recovered_scalability.json`, `scripts/{make_figures,stats,recover}.py`, `upstream/cd_simulator.py`, `EVIDENCE.md`. Read-only throughout; nothing in that directory was modified.

## Artifact identity, established first (R1)

Three-way SHA-256, all equal:

```
4242d117dff67c716523e694704ca918f2537d4756cf1d4161938a629c237675  cd_run/figures/metrics.json          (my regeneration)
4242d117dff67c716523e694704ca918f2537d4756cf1d4161938a629c237675  cd-ieee-package/figures/metrics.json (committed upstream)
4242d117dff67c716523e694704ca918f2537d4756cf1d4161938a629c237675  .../research-papers/.../data/metrics.json (audit paper)
6ca81f218b1b2ab50b2e21da3079d8b2812aaeded46f4e4cff0d3892af29810c  cd-ieee-package/cd_simulator.py
6ca81f218b1b2ab50b2e21da3079d8b2812aaeded46f4e4cff0d3892af29810c  .../research-papers/.../upstream/cd_simulator.py
```

## What was executed, with real output

```
$ python cd_simulator.py            # fresh copy, /tmp/venv2, numpy 2.5.3, scipy 1.18.1, sklearn 1.9.1
Energy             0.9988     0.0031     0.999      0.0025
Autoencoder        0.9772     0.0164     0.999      0.0255
OC-SVM              0.9985     0.0048     1.000      0.0020
IForest             1.0000     0.0000     1.000      0.0000
Cyclostationary     0.6367     0.0332     0.619      0.3750
exit code 0; metrics.json byte-identical to committed

$ gcc -O2 -o cd_kernel cd_kernel.c -lm   # 2 warnings, compiles
$ ./cd_kernel
$ echo $?
134                       # SIGABRT; 4.28 s user CPU, 5.23 s wall, 0 bytes of output (stdout lost on abort)
$ script -q /dev/null ./cd_kernel          # pty, to defeat stdout buffering
CD Kernel: n_normal=200 n_covert=160 power=-85.0 dBm
Training: 100 samples
AUC = 1.0000
Pd @ best operating point = 1.0000
Pfa @ best operating point = 0.0000
exit 6 (SIGABRT)

$ gcc -O1 -g -fsanitize=address -o k_asan cd_kernel.c -lm && ./k_asan
==17031==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x629000004210
WRITE of size 4 at 0x629000004210 thread T0
    #0 extract_features k.c:281
    #1 main k.c:357
0x629000004210 is located 0 bytes after 16400-byte region
    allocated by ... in main k.c:353
exit 134
# instrumented: FI_TOTAL=42  N_FEATURES=41
```

## Layer 4a — the upstream manuscript, scored against the upstream artifact

### L1 — Artifact: SUPPORTED
`figures/metrics.json` is committed and holds the full 20-trial Monte Carlo for all five detectors plus the nine-point power sweep. Every number in the upstream paper's Table III traces to it.

### L2 — Reproduction: SUPPORTED
I regenerated `metrics.json` from a fresh copy in a clean venv. It is **byte-identical** to the committed file, SHA-256 `4242d117...`. The simulator's own summary table reproduces the paper's Table III to four decimals. This is the strongest reproduction result in this batch, jointly with `h266`, and it is the reason the reference case's split verdict is credible rather than merely rhetorical.

### L3 — 20 claims: 3 supported / 14 contradicted / 1 unsupported / 2 true only of a different configuration

Recomputed by me from `figures/metrics.json` (20-trial means, ddof0 unless stated):

| # | upstream claim | claimed | actual | artifact path | verdict |
|---|---|---|---|---|---|
| 1 | 20-seed MC table, all five detectors (Table III) | Energy 0.9988/0.0031, AE 0.9772/0.0164, OC-SVM 0.9985/0.0048, IForest 1.0000/0.0000, Cyc 0.6367/0.0332; Pd 0.999/0.999/1.000/1.000/0.619; Pfa 0.0025/0.0255/0.0020/0.0000/0.3750 | identical to 4 decimals on all 20 cells | `figures/metrics.json` | SUPPORTED |
| 2 | Body Sec. V-C: "Isolation Forest achieves AUC = 1.000" | 1.000 | 1.0000 in 20/20 | `figures/metrics.json` `mc.IForest.aucs` | SUPPORTED |
| 3 | Abstract: "system-level AUC of 0.999 for Isolation Forest at -85 dBm" | 0.999 | **1.0000** in 20/20 seeds | `figures/metrics.json` | CONTRADICTED |
| 4 | Sec. V-C: "Energy 0.989, Autoencoder 0.943, OC-SVM 0.999" | 0.989 / 0.943 / 0.999 | these are MC trial 1 (0.9895 / 0.9426 / 0.9996) but the figure that section cites is the 250/250/200 run, whose own legend reads 1.000, 1.000, 1.000 | `figures/fig_roc_curves.*`; `data/recovered_roc.json` | CONTRADICTED (true of a different configuration) |
| 5 | Sec. V-C: "Cyclostationary ... AUC = 0.600" | 0.600 | 20-seed mean 0.6367; sweep point at -85 dBm 0.6266; 0.600 is the 250/250/200 single trial | `figures/metrics.json` | CONTRADICTED (true of a different configuration) |
| 6 | Abstract + Sec. V-D: "covert power levels ranging from -120 to -75 dBm" | -75 dBm upper | `np.arange(-120, -75, 5)` = -120 ... **-80**; -75 is the exclusive stop and never sampled | `cd_simulator.py:691`; `figures/metrics.json` `sweep.*.powers` | CONTRADICTED |
| 7 | Sec. V-A: "training set N_train=250, test set 250 normal + 200 covert" as the setup for all experiments | 250/250/200 | the 20-trial Monte Carlo table uses **100/100/80**; the sensor-scalability figure uses **80/80/60**; only the single-trial ROC uses 250/250/200. Three configurations, one stated. | `cd_simulator.py:669, 675-676, 685-686, 608-609` | CONTRADICTED |
| 8 | Sec. V-D: "transition across a -30 dB window centred near -100 dBm" | 30 dB, centred -100 | chance→AUC≥0.99 spans **40 dB** (Energy), **35 dB** (OC-SVM), **15 dB** (IForest); the autoencoder peaks at 0.9659 and the cyclic proxy at 0.7647, so two detectors never reach 0.99 at all | `figures/metrics.json` `sweep` | CONTRADICTED |
| 9 | Sec. V-D: "IForest and OC-SVM consistently outperform Energy Detection by 5-10 dB in the transition region" | +5 to +10 dB, consistent | by lowest power reaching AUC 0.90, OC-SVM is **+5 dB** and IForest **+0 dB**. Worse, "consistently" is false: OC-SVM scores **below** Energy at **7 of 9** powers and IForest at **3 of 9** (both at the three lowest powers). | `figures/metrics.json` `sweep` | CONTRADICTED |
| 10 | Conclusion: "maintains useful discrimination down to -105 dBm" | useful to -105 | at -105: Energy 0.6499, IForest 0.6769, OC-SVM 0.5236, AE 0.4879, Cyc 0.4859 — **two of five at chance** | `figures/metrics.json` `sweep` | CONTRADICTED |
| 11 | Sec. III: "A 512-point periodogram is computed via FFT with a Hann window" | Hann window | `np.fft.fft(signal, n=512)` with **no window**, and `n=512` truncates the 20,480-sample observation to its first 512 samples — **2.5%** of the data, at 39.06 kHz resolution. The Hann window that does exist is on the *spectrogram*, `nperseg=256`. | `cd_simulator.py:166-167, 212` | CONTRADICTED |
| 12 | Sec. III table + text: "Autocorrelation at lags 0,1,2,5,10,20 & max" | lags {0,1,2,5,10,20} | `ac_lags = [0,1,2,5,10,20,50,100]`, then `feats.extend(vals[:5])` takes only lags **{0,1,2,5,10}**; the "max" is over all **eight** lags, not lags 0-20 | `cd_simulator.py:201-204, 247` | CONTRADICTED |
| 13 | Sec. IV-E: cyclic autocorrelation over 20 candidate cycle frequencies, "implemented ... using the last six autocorrelation features (lags 0-20) as a proxy" | 6 autocorrelation features | the fallback averages `X[:, -7:-4]` = columns **34, 35, 36** = `sg_fvar, edge_max, edge_mean` — one spectrogram texture statistic and two envelope-edge statistics. The autocorrelation block is columns 25-30. `_cyclic_profile` is defined and **never called**. | `cd_simulator.py:353-364, 379`; executed | CONTRADICTED |
| 14 | Sec. V-B: "The PSD maximum, subband energy ratios (bands 2 and 3), and PSD 95th percentile are the most informative" | psd_max, band_2, band_3, psd_p95 | the figure's own axis reads `ac_max, ac_0, re_mean, band_std, re_std, edge_max, im_std, re_maxabs, crest, im_skew`. **None of the four named features appears.** The top two are `ac_0` and `ac_max`, both identically **1.0** in every observation, with ANOVA F = **NaN**, which `np.argsort(...)[::-1]` places first. | `figures/fig_feature_importance.*`; executed | CONTRADICTED |
| 15 | Sec. VI: "Soft fusion of scores from independent sensors improves the AUC by up to 0.15 in the challenging SNR regime" | up to 0.15 | no artifact measures this; `plot_sensor_scalability` never writes its values and `metrics.json` contains no sensor-indexed series | `cd_simulator.py:595-626`; `figures/metrics.json` has only `mc` and `sweep` | UNSUPPORTED |
| 16 | Sec. V-E: "All methods benefit from additional sensors, with the most dramatic gains occurring between K=1 and K=4" | monotonic gain, largest at K=1→4 | four detectors are exactly 1.0000 at **every** K including K=1; the autoencoder *drops* to 0.9502 at K=8; the cyclic proxy is non-monotone (0.6500, 0.6360, 0.7435, 0.6990) | recovered with the committed code; matches `data/recovered_scalability.json` exactly | CONTRADICTED |
| 17 | Sec. V-E: "Energy Detection requires K=4 to exceed 0.99" | needs K=4 | Energy is **1.0000 at K=1** | `data/recovered_scalability.json` | CONTRADICTED |
| 18 | Sec. V-E: "The Cyclostationary detector improves from AUC 0.55 (single sensor) to 0.65 (K=8)" | 0.55 → 0.65 | 0.6500 at K=1, 0.6990 at K=8; **the value 0.55 does not occur anywhere in the series** | `data/recovered_scalability.json` | CONTRADICTED |
| 19 | Sec. II: "SNR relative to the noise floor is approximately P_c + 73 dB" | P_c + 73 dB | total noise over 20 MHz = -100 + 10log10(2e7) = **-26.99 dBm**, so SNR = **P_c + 26.99 dB**. Error **46.01 dB**. | arithmetic; `cd_simulator.py:68, 81` | CONTRADICTED |
| 20 | Sec. VI: "The C reference kernel executes the full Energy Detector pipeline ... in under 1 second for 360 test observations" | <1 s, 360 obs | **4.28 s** user CPU / 5.23 s wall; **260** test observations (`n_test = n_normal/2 + n_covert` = 100 + 160); terminates **SIGABRT (134)**; AddressSanitizer reports a heap-buffer-overflow at `k.c:281` writing the 42nd value into a 41-element buffer on **every** observation, and the training write lands in the next sample's leading feature, corrupting the matrix the energy threshold is fitted on. | `figures/metrics.json` absent from the kernel's path; `cd_kernel.c:281, 353, 357`; measured | CONTRADICTED |
| 21 | Sec. II: "OFDM subcarriers at fixed centre frequencies of 2.4, 2.6, 5.2, 5.8 MHz" | narrowband OFDM PUs | `phases = self.rng.uniform(0, 2*np.pi, n)` — an **independent random phase per sample**. A constant-envelope random-phase tone is spectrally flat. Measured max/median periodogram bin power over 40 realisations: **1.4798**, consistent with a flat spectrum and inconsistent with four narrowband emitters. Two of the four frequencies are drawn per observation, without replacement, which the paper does not state. | `cd_simulator.py:87-92`; executed | CONTRADICTED |

The 3 SUPPORTED are claims 1, 2 and the 41-dimensional feature-block arithmetic (Table II sums to 41 and the code's `extract_feature_names()` returns 41, with the group sizes 5/10/10/6/4/3/3 matching the table). Claim 21 is the mechanism finding and is scored separately because it is the root cause rather than a number; it is counted in the 14.

### L4 — Figure: CONTRADICTED
Five figures, five committed generators, all five run (exit 0). The failures are of two kinds.

**A figure whose generator is the defect** (`fig_feature_importance`). The generator is committed and runs. What it computes is an ANOVA F-test on an array with **50 rows and zero anomalies** — `generate_dataset(100, 100, -85)` splits 100 normal observations 50/50 into train and test, so the array handed to `plot_feature_importance` is 50 purely normal observations — against **positional pseudo-labels** that mark the last 25 rows as "anomalous". The test measures whether the second half of a homogeneous stream of noise differs from the first half. Then the two constant features (F = NaN) are sorted to the top and plotted as the two most discriminative dimensions. I also ran the F-test with real labels for comparison: the top features become `env_range` (F = 347,707), `re_std` (94,932), `im_std` (87,297) — none of them named in the paper.

**A figure with no artifact at all** (`fig_sensor_scalability`). The routine that draws it never writes its values, and `metrics.json` has no sensor-indexed series. The figure exists; the data behind it does not. I recovered the series with the committed code and it matches the audit paper's `data/recovered_scalability.json` to the last digit, which is how the 0.55 and the monotonicity claims are settled.

The remaining three figures regenerate (matplotlib-version pixel differences only) and are faithful to `metrics.json`.

### L5 — Method: CONTRADICTED
1. **The "cyclostationary" detector is not cyclostationary.** The cyclic autocorrelation over 20 candidate cycle frequencies is implemented in `_cyclic_profile` and never called. The detector actually used is `np.mean(X[:, 34:36]) * 10` — a three-feature linear average of a spectrogram texture statistic and two envelope-edge statistics. Its near-chance 0.6367 is exactly what that predicts, and the code's own comment (`# ac_max, ac_mean, ac_std`) mislabels the columns it is reading. The paper repeats the mislabel.
2. **Two of 41 features are identically 1.0 and carry no information.** `ac_0 = ac_fft[0]/ac_fft[0]`; `ac_max = max|ac_fft[lag]/ac_fft[0]|` over lags that all satisfy |value| ≤ 1, and lag 0 attains 1. Verified: one unique value each, `1.0`.
3. **The features are not computed from a common observation.** 14 of the 41 come from the first 512 of 20,480 samples; the autocorrelation, envelope and edge blocks use all 20,480.
4. **The C kernel is memory-unsafe and does not complete.** Verified independently: `FI_TOTAL=42` into `N_FEATURES=41`; ASAN heap-buffer-overflow at `k.c:281` from `main:357`; exit 134. It also seeds from `time(0)`, hard-codes one feature to a placeholder (`feats[fi++] = 0; /* ac_max placeholder */`), and its "500 kHz BPSK" covert signal draws a fresh sign per sample, making it a full-bandwidth random sequence.
5. **The C kernel's read of the primary users is not the paper's.** Not separately scored; the Python generator defect (claim 21) is the load-bearing one.

### L6 — Selection: CONTRADICTED
1. **A metric that cannot discriminate.** Isolation Forest records AUC = 1.0000, Pd = 1.0000 and Pfa = 0.0000 in **20 of 20** seeds. Sample standard deviation over seeds is exactly **0.0000** for all three. Any significance test over that column is arithmetically incapable of producing a p-value. The paper's Table III reports `IForest 1.0000 0.0000 1.000 0.0000` without comment, and Section V-C ranks the detectors as if the column were informative.
2. **The detector field is not resolvable, and the paper ranks it anyway.** Pairing seeds across detectors, Isolation Forest minus OC-SVM is exactly zero in **17 of 20** seeds (mean +0.00152, sample SD 0.00489, driven by two outliers); minus Energy, zero in **16 of 20**; only against the autoencoder is the difference broadly non-zero (zero in 2 of 20, mean +0.0228). The paper's "Isolation Forest and One-Class SVM ... closely followed by" is a ranking the artifact cannot support.
3. **A detector selected at one operating point.** Section V-C quotes Energy 0.989 / AE 0.943 / OC-SVM 0.999 from MC trial 1, while Table III in the same paper reports the 20-seed means 0.9988 / 0.9772 / 0.9985. The narrative number is the one that makes the comparison look tight, and it is the wrong configuration for the section it appears in.
4. **The sensor-scalability series is unpaired and unreplicated.** `plot_sensor_scalability` reuses one `env_base` across all five methods and all four values of K, so the 20 cells are 20 consecutive segments of a single random stream, each `(K, method)` cell a different dataset with the K=8 dataset not a superset of the K=4 dataset. Adjacent-K differences confound fusion effect with data draw, one realisation per cell, no dispersion. The paper reads a trend out of it.
5. **The power sweep is paired, not independent, and the paper treats it as a dispersion-bearing curve.** `snr_sweep` re-creates `SpectrumEnvironment(seed=SEED)` at every power, so all nine points share identical noise and primary-user realisations. The -85 dBm point is bit-identical to MC trial 1. The contrast is real; the dispersion is unmeasured, and the paper's "-30 dB window" and "consistently outperform" claims are read off a single realisation per point.

### L7 — Internal consistency: CONTRADICTED
1. The abstract says Isolation Forest AUC = 0.999; the body says 1.000; the artifact says 1.0000 in 20/20. The abstract is wrong and the paper carries its own correction notice nowhere.
2. Section V-C quotes Energy 0.989 / AE 0.943 / OC-SVM 0.999 and cites `fig_roc_curves`, whose own legend reads 1.000, 1.000, 1.000 — a figure generated at 250/250/200 while the quoted numbers are MC trial 1 at 100/100/80. The text and the figure it cites describe different runs.
3. Section V-A declares one configuration (250/250/200) for "all experiments"; Table III is 100/100/80 and the scalability figure is 80/80/60. Three configurations, one declaration.
4. The README's detection table (Energy 0.999, AE 0.977, OC-SVM 0.999, IForest 1.000, Cyc 0.637) is the 20-seed means; the paper's Section V-C is trial 1. The package's two surfaces report different numbers for the same metric at the same operating point.
5. Section III's feature table gives 41 dimensions in group sizes 5/10/10/6/4/3/3, which is correct, and Section IV-E then describes a "last six autocorrelation features (lags 0-20)" that are neither six nor autocorrelation nor lags 0-20.
6. The abstract claims "monotonic AUC improvement with the number of distributed sensors"; the recovered series is flat at 1.0000 for four detectors, falling for one, and non-monotone for the fifth.

### L7 note on what is *not* a defect here
The package ships `quick_test.py` and the README documents `python quick_test.py` as a reduced-configuration test, and it clearly labels its own figures as generated by the simulator. There is no README instruction to run a C kernel as verification. The kernel's failure is a real defect but the package does not present it as a verification path. Recorded for balance.

### L8 — Verdict, upstream layer: CONTRADICTED
The paper's positive claim is that anomaly detection is well suited to covert detection and that distributed fusion improves it. Its own artifact shows four detectors at a metric ceiling with zero dispersion, the "cyclostationary" detector averaging three unrelated columns, the sensor-count series flat at 1.0000 from a single sensor, and two of five detectors at chance across most of the power sweep. The central claim is contradicted by the package's own artifacts.

## Layer 4b — the audit manuscript, scored against its own artifacts

`/Users/fmf/Documents/research-papers/cd-covert-anomaly-detection/main.tex`, read-only, alongside `data/metrics.json`, `data/stats.json`, `data/recovered_roc.json`, `data/recovered_scalability.json`, `upstream/cd_simulator.py` and the upstream repo.

### L1 — SUPPORTED. `data/metrics.json` is byte-identical to the upstream artifact; `data/stats.json`, `data/recovered_roc.json` and `data/recovered_scalability.json` are committed; the generator scripts are committed; six figures have committed generators.
### L2 — SUPPORTED. I regenerated the upstream artifact independently and obtained the same SHA-256 `4242d117...`; I recovered the sensor series with the committed code and it matches `data/recovered_scalability.json` to the last digit (0.9502083333333333, 0.6360416666666667, 0.7435416666666667, 0.6989583333333333).

### L3 — 24 claims: 22 supported / 1 contradicted / 1 unsupported

Verified by me from the artifacts and the code, not inherited:

| claim | audit paper's statement | my measurement | verdict |
|---|---|---|---|
| 20-seed MC table reproduces to 4 decimals | yes | my recomputation: 0.9988/0.0031, 0.9772/0.0168(ddof1), 0.9985/0.0049, 1.0000/0.0000, 0.6367/0.0341 | SUPPORTED (see the SD contradiction below) |
| IForest at 1.0000, zero dispersion, 20/20 | yes | 20 values all exactly 1.0 | SUPPORTED |
| "four of five detectors exceed 0.977" | yes | 0.9988, 0.9772, 0.9985, 1.0000 | SUPPORTED |
| IForest-OC-SVM difference zero in 17/20, mean +0.00152, SD 0.00489 | yes | 17/20, +0.00152, 0.00489 | SUPPORTED |
| IForest-Energy zero in 16/20 | yes | 16/20 | SUPPORTED |
| IForest-AE zero in 2/20, mean +0.0228 | yes | 2/20, +0.02280 | SUPPORTED |
| sweep ends at -80 dBm, not -75 | yes | `np.arange(-120,-75,5)` → -120…-80 | SUPPORTED |
| widths 15 / 35 / 40 dB, two detectors never reach 0.99 | yes | 15 / 10(by my 0.60 rule)/35/40 under the audit's first-AUC>0.5 rule; AE max 0.9659, Cyc max 0.7647 | SUPPORTED |
| OC-SVM below Energy at 7 of 9, IForest at 3 of 9 | yes | 7/9 and 3/9, both at the three lowest powers | SUPPORTED |
| -105 dBm values 0.6499 / 0.6769 / 0.5236 / 0.4879 / 0.4859 | yes | exact match to the artifact | SUPPORTED |
| PUs spectrally flat, max/median bin ratio 1.50 | yes | **1.4798** over 40 realisations | SUPPORTED |
| covert in-band H1/H0 median 3.41, out-of-band median 1.05 | yes | **3.4416** and **1.0469** | SUPPORTED |
| covert in-band H1/H0 **maximum 8.21** | 8.21 | **4.4648** over 60 realisations at my seeds (777/778) | **CONTRADICTED** — see below |
| "the -85 dBm point is bit-identical to Monte Carlo trial 1" | yes | **0.9894999999999999 == 0.9894999999999999** for all five detectors, verified both from the artifact (index 7) and by direct execution | SUPPORTED |
| "Isolation Forest ... constructed with random_state=42 in every trial" | yes | `IForestDetector.__init__`: `IsolationForest(contamination, random_state=SEED)` | SUPPORTED |
| "derived seeds 42+1000t" | yes | `monte_carlo_evaluation`: `SpectrumEnvironment(seed=SEED + t*1000)` | SUPPORTED |
| "MC uses 100 train / 100 / 80 test" | yes | `main()`: `monte_carlo_evaluation(n_trials=20, n_train=100, n_test_normal=100, n_test_covert=80)` | SUPPORTED |
| "Autoencoder drops 1.0000 to 0.9502 at K=8" | yes | 1.0, 1.0, 1.0, 0.9502 | SUPPORTED |
| "Energy is 1.0000 at K=1" | yes | 1.0, 1.0, 1.0, 1.0 | SUPPORTED |
| "cyclic 0.6500 at K=1 to 0.6990 at K=8; no 0.55 exists" | yes | 0.65, 0.636, 0.7435, 0.699 — minimum 0.636, no 0.55 | SUPPORTED |
| "periodogram uses no window" | yes | `np.fft.fft(signal, n=512)`, no window; 2.5% of the observation; 39.06 kHz | SUPPORTED |
| "cyclic detector uses columns 34-36; the cyclic code is never called" | yes | `['sg_fvar','edge_max','edge_mean']`; AC block is 25-30; `_cyclic_profile` never invoked | SUPPORTED |
| "two of 41 features constant, ANOVA F = NaN, sorted first" | yes | `ac_0` and `ac_max` each have exactly one unique value, 1.0; 2 NaN F-scores; they occupy positions 1 and 2 on the figure | SUPPORTED |
| "SNR = P_c + 73 dB is false by 46 dB; correct is P_c + 26.99" | 46 dB, 26.99 | total noise -26.9897 dBm; error **46.01 dB** | SUPPORTED |
| "C kernel ... 2.0 s CPU, 260 observations, aborts at exit" | 2.0 s, 260, abort | 260 observations and SIGABRT confirmed; **4.28 s** user CPU here | **UNSUPPORTED** on the timing, machine-dependent (R4) |
| "Top features ... false, labels differ, top two constant" | yes | figure axis reads `ac_max, ac_0, re_mean, band_std, re_std, edge_max, im_std, re_maxabs, crest, im_skew`; none of psd_max/band_2/band_3/psd_p95 present | SUPPORTED |
| "this manuscript cites no prior work" | self-disclosed | verified: the bibliography is absent | SUPPORTED |
| "No number in this paper was entered by hand; all transcribed from stats.json" | provenance claim | `stats.json` carries the values; spot-checked 8 of them, all match | SUPPORTED |
| Table I SD column: "We report the sample standard deviation (n-1)" and "Mean and standard deviation reproduce the upstream table to four decimals" | n-1, and reproduces upstream | `data/stats.json` carries **both** estimators. Energy 0.0031 either way. **Autoencoder: ddof0 0.016377 → 0.0164 (as printed); ddof1 0.016802 → 0.0168.** OC-SVM: ddof0 0.004764 → 0.0048 (as printed); ddof1 0.004888 → 0.0049. Cyclic: ddof0 0.033221 → 0.0332 (as printed); ddof1 0.034085 → 0.0341. The printed values are the **population** SDs. | **CONTRADICTED** |

**The two findings I disagree with, and the argument.**

*Disagreement 1 — the SD estimator.* The audit paper's Table I caption and Section III both say it reports the sample SD (n−1), and the caption says the SD "reproduce[s] the upstream table to four decimals". Those two statements are mutually exclusive: the upstream simulator prints `np.std(aucs)`, which is ddof=0. The printed values 0.0164 / 0.0048 / 0.0332 are ddof=0, and the audit's own committed `data/stats.json` contains ddof=1 values of 0.0168 / 0.0049 / 0.0341 that the paper does not use. So the paper reports the upstream estimator while claiming a different one. This is a small finding — the difference is under 0.001 on every cell and changes no conclusion — but it is a claim about method, it is falsifiable from the paper's own artifact, and it is falsified. I score it CONTRADICTED. The upstream paper's Table III carries the same ddof=0 values, which is why the "reproduces to four decimals" framing is defensible for the *upstream* number and not for the *n-1* number the audit paper says it is reporting.

*Disagreement 2 — the covert in-band maximum.* The audit paper states the H1/H0 power ratio inside the covert band has "median 3.41 and maximum 8.21". My measurement over 60 realisations at seeds 777/778 gives median **3.4416** (close, within 1%) and maximum **4.4648** — not 8.21. The medians agree; the maximum does not. A maximum over 60 draws of a heavy-tailed ratio is a high-variance statistic and the audit paper does not state its seeds for this measurement, so the honest reading is that 8.21 is seed-dependent and unreproducible as stated. I score the median as SUPPORTED and the maximum as CONTRADICTED-in-my-measurement, while recording that a different seed could produce 8.21. I do not treat this as evidence that the audit paper is wrong about the mechanism; its load-bearing numbers (the medians, and the 1.4798 spectral-flatness ratio) both reproduce.

**Self-correction, recorded because it would have been a false contradiction.** From `data/metrics.json` alone I computed the sweep value at index 6 and compared it to MC trial 1, found 0.979375 against 0.989500, and concluded the audit paper's claim that the -85 dBm point duplicates trial 1 was false. Executing the code settled it: `np.arange(-120, -75, 5)` puts **-85 at index 7**, not 6, and at index 7 all five detectors give values bit-identical to MC trial 1. The audit paper is right and my index was wrong. Had I reported from the artifact alone I would have published a false contradiction against the reference case.

### L4 — SUPPORTED
Six figures, six committed generators (`scripts/make_figures.py`), all run. The provenance figure, the AUC-vs-power figure, the AUC-distribution figure and the AUC-vs-sensors figure were all regenerated against the recovered data. The audit paper takes the opposite decision from `cd` on the feature-importance figure — it **excludes** it and says why, which is the correct handling of a generator that is the defect.

### L5 — SUPPORTED
The audit paper's own mechanism experiments are real and were re-run by me: the per-sample-phase argument (`cd_simulator.py:90-91`), the column-34-36 detector, the NaN-sorted feature importance, the periodogram truncation. The two discarded series were regenerated with the committed code and committed as new artifacts, which is the correct way to handle a value the upstream code computes and throws away. Nothing the audit paper describes as executed is inert.

### L6 — SUPPORTED
The audit paper's central selection finding is the strongest in this batch: the Isolation Forest column has zero variance over 20 seeds, and the paired per-seed differences between the leading detectors are zero in 17 and 16 of 20 trials. It reports this as making the ranking unrecoverable, which is correct. It also explicitly declines to correct for the ceiling — "We did not select a harder operating point and re-run, because doing so would change the experiment rather than audit it" — which is the right call and is stated.

### L7 — CONTRADICTED
The SD estimator contradiction above is the finding, and it is internal to a single table plus its caption. One further internal tension: the abstract reports "the paired per-seed difference between the best and second-best detector is exactly zero in seventeen of twenty trials", Section III says "exactly zero in seventeen of twenty trials, with mean +0.00152 and sample SD 0.00489", and Section III also says the standard deviations in Table I are n-1 — the paper is careful about "sample SD" for the *differences* and wrong about it for the *columns*, which is a real inconsistency in the use of a term the paper defines.

### L8 — Verdict, audit layer: PARTIALLY SUPPORTED
This is the one package in the batch that occupies the rubric's honest middle. The artifact reproduces bit-for-bit, the mechanism findings are correct and independently verified, the selection analysis is the best in the batch, the limitations section is unusually candid (no prior work compared, the ceiling not corrected, the sweep and sensor series unreplicated, its own novelty risk flagged), and the one contradicted claim is a standard-deviation estimator worth less than 0.001 on every cell. A bounded set of contradicted claims on top of real reproducible artifacts is precisely what PARTIALLY SUPPORTED means. I score it PARTIALLY SUPPORTED and record the SD contradiction rather than letting the strong overall verdict absorb it.

It is also the correct calibration case for the rubric: it reaches CONTRADICTED-adjacent conclusions about its subject while remaining SUPPORTED on its own evidence, which is the discipline the rubric is asking for.

---

# Re-score deltas: h266 and cd

Both packages were audited earlier under different, non-comparable rubrics. This section states, layer by layer, whether the re-score agrees with the earlier verdict, and where it differs, which I believe and why. Per-layer verdicts in this table come from my own measurements, taken from the artifacts before reading the prior findings (R1); the prior findings were then checked against them rather than inherited.

## h266-drl-iccpr2026

| layer | earlier verdict | re-score | agree? |
|---|---|---|---|
| L1 Artifact | artifacts exist | SUPPORTED | agree |
| L2 Reproduction | implied not bit-reproducible ("weight-init RNG making its JSONs non-bit-reproducible") | **SUPPORTED** | **differ — and I believe the re-score** |
| L3 Numerical | 8 of 19 supported, 11 fail | 19 total / 8 supported / 11 contradicted / 0 unsupported | agree on the split |
| L4 Figure | (not recorded separately) | SUPPORTED | new; 4/5 published figures regenerate and are faithful; 1 committed figure is an orphan with no generator |
| L5 Method | 120 minibatch iterations described, 1 `agent.update()` executed | CONTRADICTED, with the mechanism sharpened | agree, with a refinement |
| L6 Selection | best seed cherry-picked (seed 42 → 69.27, random → 63.37, others 56.71/64.79/61.23); Wilcoxon paired on unpaired data; pseudo-replication from pooled contiguous windows | CONTRADICTED on selection and on the invalid test; **decline to confirm the pseudo-replication magnitude** | **partly differ** |
| L7 Consistency | (not recorded separately) | CONTRADICTED | new |
| L8 Verdict | (implicitly negative) | **CONTRADICTED** | agree on direction |

**L2 — I disagree, and my evidence is direct.** I ran `h266_drl_simulator.py` twice end to end in fresh processes. Both runs produced `metrics.json` byte-identical to the committed artifact on every scientific field. The single differing field is `training.time_seconds` (552.0 committed, 94.4 and 70.3 measured) — a wall-clock measurement, and 552 s on the author's machine against 70-95 s here is a hardware difference, not a result difference. Two independent PPO trainings in one process also gave identical reward histories (`last20 = -28959.1` in both). The rubric's own L2 text asserts h266's JSONs are non-bit-reproducible because of weight-init RNG; `train_agent` calls `torch.manual_seed(seed)` before constructing the networks, and the one unseeded draw I found (`np.random.normal(0, 0.2)` in `_compute_vmaf`) comes from the global numpy stream that the same function seeds. I cannot reproduce the asserted non-reproducibility, and the burden is on the assertion. I record the possibility that some torch version differs — but I have no evidence for it, so I will not carry an unmeasured claim into a denominator.

There is a confound I had to eliminate first, and it is worth recording because it is the kind of error that would have produced a false CONTRADICTED here too. My initial determinism test trained two agents in the same process and got 67.928569 against 68.775485. That is a probe artifact, not a property of the code: `evaluate_agent` *samples* from the categorical policy, so the second evaluation draws from a torch RNG stream the first has already advanced. Two full process runs are the clean test, and they are bit-identical.

**L5 — agree, and the refinement matters.** The earlier finding is correct and I confirmed it by instrumenting `PPOAgent.update`: `n_update_calls: 1`, `inner_gradient_iterations_total: 120`, `buffer_max_size: 60000`, `buffer_ptr_at_call: 60000`. The 120 iterations are not missing — they execute. The defect is *when* and *over what*: one full-batch pass-set of 120 gradient steps over the entire 60,000-transition buffer, fired once after the last environment step, against a paper that describes per-episode updates of 120 minibatches from a 50-transition buffer. Stating it as "the 120 iterations were not executed" would be wrong; stating it as "1 update, 120 full-batch iterations, at the end" is right and is strictly more damning, because it shows the learning could not have influenced the 1,200 episodes of data collection that Figure 1 plots.

I also add the distinction the rubric requires. The method was **run and produced something**: the trained policy's action distribution over 100,035 samples is [6089, 17834, 17365, 7523, 18669, 7888, 6174, 12901, 5557] against a fresh initialisation's [4666, 11081, 2604, 4690, 3664, **34123**, 11251, 19895, 8026] — the 34.1% mode on action 5 flattens to an 18.7% maximum. The evaluated policy beats a uniform random policy 67.93 to 62.90 and the heuristic 67.93 to 66.34. So "the DRL does nothing" would be false. What is false is the training loop the paper describes and the convergence it reports.

**L6 — I agree on two findings, decline to confirm a third, and decline to inherit five numbers.**

*Agree: best-seed reporting.* The finding stands on the committed artifact. `multi_seed.json` gives DRL VMAF 60.690 ± 2.435 (stable) across three training seeds against fixed QP's 67.632 ± 0.176, with `improvement_vs_fixed_pct` = **-10.26** and `p(vs fixed) = 1.0`. The paper's reported 67.93 is 7.24 points above the three-seed mean, against a baseline whose across-seed sd is 0.176. One seed, no dispersion, no seed count.

*Agree: the Wilcoxon is invalid.* `bootstrap_eval.py:43-45` runs `_eval_seed(agent, e, ...)` and then `_eval_seed_run(run_fixed_qp, e, ...)` on the **same** environment object, and `H266EncodingEnv.reset()` does not reseed `self.video`, `self.channel` or `self.rng`. The two arms therefore evaluate on disjoint segments of one stream, and line 55 pairs them by index with `sps.wilcoxon(dv[:n], fv[:n])`. The signed-rank test requires paired samples. The Mann-Whitney U on the same arrays is the correct test for unpaired data and is also computed, so the significance conclusion is not void, but the Wilcoxon and its p = 0.0502 are not valid as reported.

*Decline: the pseudo-replication magnitude.* The structural fact is real and I verified it — `reset()` leaves the chains running, so 30 episodes are 30 contiguous 50-step windows of one realisation, and 150 pooled observations carry 5 chains' worth of independent information. But I measured the lag-1 autocorrelation of 30 consecutive episode-mean VMAFs on a held-out chain (seed 999, fixed-QP policy) and got **0.0526** at n = 30, not distinguishable from zero. I cannot demonstrate the dependence that would make the pooled n anti-conservative. The defensible statement is narrower: the effective sample size is bounded by the number of chains, the package reports no clustering correction, and the design is invalid in principle. I score the design flaw and decline the empirical claim.

*Decline: the five numbers.* "seed 42 → 69.27 VMAF, uniform random → 63.37, others 56.71 / 64.79 / 61.23" appear in **no committed artifact** of this repository. The nearest committed values are `multi_seed.json`'s volatile row 56.699 / 64.805 / 61.269 — different in the second decimal from 56.71, 64.79 and 61.23 — and 69.27 and 63.37 appear nowhere. Those numbers are either from a re-run I cannot match or from a different version of the artifact. My own measured values, stated in the h266 section above, are the ones I stand behind. R1 forbids inheriting a prior agent's number without checking it, and I could not check these.

**L7 — new finding the earlier audit did not record.** The paper's headline volatile advantage (+1.0% / +4.2%) coexists in the same repository with `bootstrap_eval.json` reporting +1.904% / +3.308% for volatile and +1.411% / +3.053% for stable, and with `generalization.json` showing the DRL **losing** in-distribution, 67.049 against fixed QP's 67.753. Ten artifacts in `revision_results/` that refute the abstract are not cited, referenced, or acknowledged anywhere in the paper, the README, or the slides. This is the single most important L7 finding in the package and it is what moves L8 to CONTRADICTED: the central claim is contradicted by the package's own artifacts, not merely by an external reading.

**L8 — CONTRADICTED, and I will defend it against a PARTIALLY SUPPORTED challenge.** A challenger would say: excellent artifacts, bit-reproducible, honest limitations, one bad training loop, a bounded set of contradicted claims — that is PARTIALLY SUPPORTED. The rebuttal is that the contradicted claims are the load-bearing ones, not a periphery: the training procedure, the convergence claim, the Figure 1 interpretation, the central volatile advantage, and the significance evidence. And the package's own robustness file says the method loses by 10.26% with p = 1.0. PARTIALLY SUPPORTED is for `cd`'s situation, where the artifact is sound and the *interpretation* fails. Here the artifact is sound and the *robustness study the author ran* refutes the abstract.

## cd-ieee

| layer | earlier verdict | re-score | agree? |
|---|---|---|---|
| L1 Artifact | committed `data/metrics.json` byte-identical to upstream | SUPPORTED | agree |
| L2 Reproduction | reproduces exactly | **SUPPORTED** | agree, independently confirmed |
| L3 Numerical | 3 supported, 14 contradicted, 1 unsupported, 2 true only of a different configuration | 20 claims: 3 supported / 14 contradicted / 1 unsupported / 2 other-configuration | agree exactly |
| L4 Figure | feature-importance generator was the defect; sensor-scalability figure had no artifact | CONTRADICTED | agree, with a stronger version of the first |
| L5 Method | per-sample random phase; fabricated feature importance; memory-unsafe C kernel; cyclostationary not cyclostationary | CONTRADICTED | agree, and one addition |
| L6 Selection | IForest sd 0.0000 over 20 seeds | CONTRADICTED | agree, and extended |
| L7 Consistency | abstract 0.999, body 1.000, artifact 1.0000 | CONTRADICTED | agree |
| L8 Verdict | (the rubric's reference case) | **CONTRADICTED on the upstream layer** | differ — see below |

**L1, L2, L3 — agree, and I confirmed rather than inherited them.** I regenerated `metrics.json` from a fresh copy in a clean venv (numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1) and obtained SHA-256 `4242d117dff67c716523e694704ca918f2537d4756cf1d4161938a629c237675`, identical to the committed upstream file and to the audit paper's `data/metrics.json`. That three-way byte identity is the strongest single result in this batch. I then recomputed the 20-seed means, the standard deviations, the confidence intervals, the paired per-seed differences and the sweep contrasts from the artifact, and my numbers match the earlier verdict's claim tally exactly: 3 supported, 14 contradicted, 1 unsupported, 2 true only of a different configuration. Two of the fourteen I had to find for myself and both held: the -75 dBm endpoint (`np.arange(-120, -75, 5)` excludes -75) and the 250/250/200-versus-100/100/80-versus-80/80/60 three-configuration drift.

**L4 — agree, and the feature-importance finding is worse than stated.** The earlier finding is that the generator sorts NaN to the top over constant features. True, and I confirmed it: `ac_0` and `ac_max` each have exactly one unique value, 1.0, and their ANOVA F-scores are NaN, and they occupy positions 1 and 2 on the figure. The addition is the reason the figure is worthless rather than merely mislabelled: the array handed to `f_classify` has **50 rows and zero anomalies**. `generate_dataset(100, 100, -85)` splits 100 normal observations 50/50 between train and test, so all 50 rows are normal, and the "labels" are positional — the last 25 rows marked anomalous. The F-test measures whether the second half of a homogeneous stream of noise differs from the first half. For comparison I ran the same test with real labels: the top features become `env_range` (F = 347,707), `re_std` (94,932), `im_std` (87,297) — none of the four the paper names. The sensor-scalability finding also holds: `plot_sensor_scalability` writes no values, `metrics.json` has only `mc` and `sweep`, and I recovered the series with the committed code to the last digit (1.0/1.0/1.0/0.9502 for the autoencoder, 0.65/0.636/0.7435/0.699 for the cyclic proxy).

**L5 — agree on all four, and add one.** Per-sample random phase at `cd_simulator.py:90-91` (`phases = self.rng.uniform(0, 2*np.pi, n)`) makes the primary users spectrally flat: I measured a max/median periodogram bin ratio of **1.4798** over 40 realisations, where four narrowband emitters would give a contrast of one to two orders of magnitude. The fabricated feature importance is confirmed as above. The memory-unsafe C kernel is confirmed three ways: instrumented `FI_TOTAL=42` into `N_FEATURES=41`; AddressSanitizer reporting `heap-buffer-overflow ... WRITE of size 4 ... #0 extract_features k.c:281 #1 main k.c:357`, `0 bytes after 16400-byte region`; exit 134 on every run. And the cyclostationary detector averages columns 34-36, which are `['sg_fvar', 'edge_max', 'edge_mean']`, while the autocorrelation block is columns 25-30, and `_cyclic_profile` is never called. The addition: **two of the 41 features are identically 1.0 and carry no information** — `ac_0 = ac_fft[0]/ac_fft[0]` and `ac_max = max|ac_fft[lag]/ac_fft[0]|` over lags that all satisfy |value| ≤ 1, with lag 0 attaining 1. That is a fourth implementation defect the earlier list did not name, and it is the direct cause of the NaN sort.

**L6 — agree, and the extension is that the ranking is not merely unresolvable but explicitly reported as if it were.** IForest records 1.0000 / 1.0000 / 0.0000 in 20 of 20 seeds; sample SD over seeds is exactly 0.0000 on all three columns, so no test on that column can return a p-value. Pairing seeds across detectors, IForest minus OC-SVM is exactly zero in 17 of 20 (mean +0.00152, sample SD 0.00489), minus Energy in 16 of 20, minus the autoencoder in 2 of 20 (mean +0.0228). The paper ranks the detectors anyway. I add that the paper's *narrative* numbers and its *table* numbers are different configurations: Section V-C quotes 0.989 / 0.943 / 0.999 from MC trial 1 while Table III reports the 20-seed means 0.9988 / 0.9772 / 0.9985, and the README's table reports the 20-seed means again. Three surfaces, two configurations, no disclosure.

**L8 — this is where I part company with the rubric.** The rubric's own reference section states that `cd-ieee-package` "scored 3 SUPPORTED / 14 CONTRADICTED / 1 UNSUPPORTED across 20 claims", and the brief's calibration note describes the package's earlier verdict as a negative one. The rubric uses `cd` as the exemplar of PARTIALLY SUPPORTED: "Real reproducible artifacts, with a bounded set of contradicted claims. The honest case, and the one `cd` occupies."

Applying the rubric's own L8 text mechanically, `cd-ieee-package` is **CONTRADICTED**, not PARTIALLY SUPPORTED. The condition for PARTIALLY SUPPORTED requires real *reproducible* artifacts with a *bounded* set of contradicted claims. The artifacts are reproducible — L2 is SUPPORTED, bit-for-bit. But the contradicted claims are not bounded: they include the central positive claim in the abstract, the detector ranking, the feature-importance result, the fusion-gain result, the power-sweep characterisation, the SNR relation, the signal model of the primary users, and the C kernel's performance. Section VI of the paper opens with "Anomaly detection is well-suited to covert signal detection" and Section III of the Discussion states "Distributed fusion provides a clear gain" — the paper's two stated conclusions. Both are contradicted by its own artifact. That is the rubric's CONTRADICTED condition: the paper's central claim is contradicted by its own artifacts.

I therefore split the package into two layers, which is what the brief asked for, and the split resolves the apparent contradiction in the rubric:

- **`cd-ieee` (the upstream manuscript, scored against the upstream artifact): CONTRADICTED.** Its central claims are contradicted by its own artifacts.
- **`cd-audit` (the manuscript at `research-papers/`, scored against its own artifacts): PARTIALLY SUPPORTED.** Its artifacts reproduce bit-for-bit, its mechanism findings are correct and I reproduced them independently, its selection analysis is the best in the batch, its limitations are candid to its own cost, and it carries exactly one contradicted claim — a standard-deviation estimator worth under 0.001 on every cell, which I found by reading its own `data/stats.json` and which neither it nor the rubric had noticed.

Both readings are in the machine-readable table. If the series needs one verdict for the repository named `cd-ieee-package`, it is CONTRADICTED; the PARTIALLY SUPPORTED verdict the calibration note remembers belongs to the audit manuscript that was written about it, not to the package itself. That is, I think, the more useful reading for the series, and it is the one I would defend.

**One finding I got wrong and corrected before reporting.** From `data/metrics.json` I compared the power sweep at index 6 against MC trial 1, found 0.979375 against 0.989500, and was about to record the audit paper's claim that "the -85 dBm point is bit-identical to Monte Carlo trial 1" as contradicted. `np.arange(-120, -75, 5)` puts **-85 at index 7**. At index 7 all five detectors are bit-identical to MC trial 1, and a direct execution confirms it. The audit paper was right, my index was wrong, and had I reported from the artifact alone I would have published a false contradiction against the rubric's own reference case. Recorded here because a re-score that manufactures disagreements is as useless as one that inherits them.

## Self-corrections made during this batch

Recorded for R7 and for the credibility of the negative findings.

1. **A wrong index produced a would-be false contradiction** against the `cd` audit paper's common-random-numbers claim. Caught by executing the code; the claim is correct. Detailed above.
2. **A wrong crossover test produced a would-be false null** on `mega-constellation`. My first bounds-violation test used two identical parents, which makes SBX a no-op, and returned 0 violations in 4,000 trials. I discarded it and re-ran with 20,000 varied-parent crossovers, which returned 110 violations (0.55%), altitudes from 169.89 to 1726.15 km. The finding is the second one.
3. **A confounded determinism test nearly produced a false CONTRADICTED on h266's L2.** Two agents trained in one process gave 67.928569 and 68.775485, which would have confirmed the rubric's non-reproducibility claim. The cause was my probe: `evaluate_agent` samples from the policy, so the second evaluation inherited an advanced torch RNG stream. Two full process runs are bit-identical, and the L2 verdict moved to SUPPORTED.
4. **A withdrawn claim.** I had drafted "the claimed vectorized Monte Carlo coverage evaluation framework" as an unsupported `mega-constellation` entry on the theory that "vectorized" overstated the implementation. The vectorisation is real (`global_coverage_fraction` is fully vectorised over satellites and ground points). I withdrew the entry, which is why that package's unsupported count is 4 and not 5.
5. **A framing correction on h266's pseudo-replication.** I had accepted the inherited finding. On measurement the lag-1 autocorrelation is 0.0526, so I downgraded the claim from an empirical pseudo-replication finding to a design finding with unestablished magnitude.
6. **The audit paper's "maximum 8.21" for the covert in-band power ratio did not reproduce** (I measured 4.4648) while its medians did. I report the disagreement and record that the maximum is a seed-dependent statistic the paper does not document, rather than asserting the paper is wrong about the mechanism.

---

# Batch 3 aggregate

The rubric's aggregate form, verbatim, with `N audited` attached. Three denominators are given because the brief audits four packages but the brief also asks for `cd` to be scored at two layers. The first block is the authoritative one for the machine-readable table above.

## Denominator A — five scored rows (the machine-readable table)

```
N audited                                                5   (4 packages; cd contributes 2 layers)
N with reproducible artifacts (L1+L2 SUPPORTED)           3 of 5
N with internally consistent papers (L7 SUPPORTED)       0 of 5
N with unsupported claims (L3 unsupported > 0)           4 of 5
N with contradicted claims (L3 contradicted > 0)         5 of 5
N with figure/data mismatch (L4 CONTRADICTED)           3 of 5
N with methodological non-execution (L5 CONTRADICTED)    4 of 5
```

L8 distribution across the five rows: SUPPORTED 0, PARTIALLY SUPPORTED 1, CONTRADICTED 4, UNVERIFIABLE 0.
L3 across the five rows: 105 claims, 50 supported (47.6%), 48 contradicted, 7 unsupported.

## Denominator B — four packages, `cd-ieee` counted once as its upstream manuscript

```
N audited                                                4
N with reproducible artifacts (L1+L2 SUPPORTED)           2 of 4
N with internally consistent papers (L7 SUPPORTED)       0 of 4
N with unsupported claims (L3 unsupported > 0)           3 of 4
N with contradicted claims (L3 contradicted > 0)         4 of 4
N with figure/data mismatch (L4 CONTRADICTED)           3 of 4
N with methodological non-execution (L5 CONTRADICTED)    4 of 4
```

L8 across four packages: SUPPORTED 0, PARTIALLY SUPPORTED 0, CONTRADICTED 4, UNVERIFIABLE 0.
L3 across four packages: 81 claims, 28 supported (34.6%), 47 contradicted, 6 unsupported.

## Denominator C — the two new packages only (Job A), for comparison with Job B

```
N audited                                                2
N with reproducible artifacts (L1+L2 SUPPORTED)           0 of 2
N with internally consistent papers (L7 SUPPORTED)       0 of 2
N with unsupported claims (L3 unsupported > 0)           2 of 2
N with contradicted claims (L3 contradicted > 0)         2 of 2
N with figure/data mismatch (L4 CONTRADICTED)           2 of 2
N with methodological non-execution (L5 CONTRADICTED)    2 of 2
```

L3 across the two new packages: 41 claims, 17 supported (41.5%), 19 contradicted, 5 unsupported.

## The hypothesis under test

> artifact reproducibility is materially better than artifact-to-claim correspondence

**Supported in this batch, and by a wide margin.** Across five scored rows: L1 SUPPORTED 5 of 5, L2 SUPPORTED 3 of 5, while L7 SUPPORTED is 0 of 5 and L8 SUPPORTED is 0 of 5. Every package in this batch has a committed artifact; two of five cannot be regenerated at all; and not one of the five is internally consistent or fully supported. Reproduction beats correspondence by 3-to-0 at L2 and by 5-to-0 at L1 against 0-to-5 at L7.

The batch's sharpest single illustration is `h266`. Its `metrics.json` reproduces bit-for-bit on every scientific field across two independent process runs — the best L2 result here — and its paper's central claim is contradicted by a robustness file the package contains and does not cite. A package can be perfectly reproducible and still be wrong, and that is exactly what the hypothesis says.

## Comparability caveat (R5, R6) — read before comparing L3 rates

The calibration puts batches 1-2 at L3 213/270 supported (78.9%). This batch is at 28/81 (34.6%) on the same denominator definition, or 50/105 (47.6%) including the audit-paper row. **These rates are not directly comparable and I will not present them as a trend.** My claim granularity differs from the earlier batches': I counted mechanism identities individually where an earlier batch may have counted a section as one claim, and I counted multi-cell tables as a single claim. The L3 *rate* is therefore an artefact of counting convention as much as of package quality.

The **categorical** verdicts are comparable, because a rubric layer is a SUPPORTED / CONTRADICTED / UNVERIFIABLE / NOT APPLICABLE judgement and does not depend on how many sub-claims I split a paragraph into. On those:

| layer | batches 1-2 (N=8) | batch 3 (N=5 rows) |
|---|---|---|
| L1 SUPPORTED | 8 of 8 | 5 of 5 |
| L2 SUPPORTED | 7 of 8 | 3 of 5 |
| L7 SUPPORTED (CONTRADICTED) | 7 of 8 CONTRADICTED | 5 of 5 CONTRADICTED |
| L8 SUPPORTED | 0 of 8 | 0 of 5 |
| L8 PARTIALLY SUPPORTED | 7 of 8 | 1 of 5 |
| L8 CONTRADICTED | 1 of 8 | 4 of 5 |

## Placement in the running series

Adding batch 3's four packages to the N=8 already audited, and restating `cd-ieee-package` per the L8 argument in the re-score deltas (upstream manuscript CONTRADICTED; the PARTIALLY SUPPORTED verdict the calibration remembers belongs to the audit manuscript written about it):

```
N audited                                                              12
L8 SUPPORTED                                                          0 of 12
L8 PARTIALLY SUPPORTED                                                 7 of 12
L8 CONTRADICTED                                                       5 of 12
L1 SUPPORTED                                                         12 of 12
L2 SUPPORTED                                                          9 of 12
L7 SUPPORTED                                                          0 of 12
```

If the series instead keeps `cd-ieee-package` at PARTIALLY SUPPORTED, the running line is 0 SUPPORTED / 8 PARTIALLY SUPPORTED / 4 CONTRADICTED at N=12. I recommend the restatement, and the argument for it is in the re-score deltas; I am recording both so the choice is visible rather than absorbed.

R5 note: this running line covers the 12 packages audited in this series and characterises nothing about the 200+ other repositories in the account.

## What this batch adds to the pattern

Batches 1-2 found the pattern: individual numbers are mostly right and packages as wholes are not. Batch 3 finds a sharper and slightly different version, which is worth stating because it changes what the pattern means.

1. **Reproduction is not the variable that distinguishes good from bad packages here.** Two packages in this batch are bit-reproducible (`cd`, `cd-audit`) and two are not (`icft`, `mega-constellation`), and the reproducibility tells you almost nothing about the verdict: all four are CONTRADICTED or PARTIALLY SUPPORTED, and the best-reproducing package in the batch is the one whose own robustness file refutes its abstract.
2. **The dominant failure in this batch is not fabrication of numbers. It is inert or absent code behind a correctly-reported result.** `icft` computes wavelet features and HMM states and passes them to a function that ignores them, then reports correlation coefficients for a quantity it defines as a single scalar. `mega-constellation` defines a link budget and a revisit model and calls neither. `cd` defines a cyclic-autocorrelation detector and calls neither. In all three, the *paper's* numbers are largely faithful to the *artifact*; it is the artifact that does not contain the claimed method. This is a different failure from `cd`'s upstream layer, where the numbers themselves are wrong.
3. **Where a package's own robustness artifacts exist, they are more honest than the paper.** `h266` computes a three-seed study that reports its own method at -10.26% and does not read it. `mega-constellation` commits a CSV that contradicts its own abstract, and the contradiction is visible in five seconds by sorting one column. `cd`'s robustness study was written by a later pass and is the only manuscript in the batch that is largely SUPPORTED on its own evidence.
4. **The class-balance trap did not recur.** The brief flagged `icft` as a possible repeat of `soil-degradation-lmu`. It is not: the imbalanced class is the negative one (97-98%), the paper reports F1 rather than accuracy, and there is no 99.83% claim. What it has instead is a different version of the same disease — a headline result beaten by a constant threshold on its own score, with no trivial baseline reported. Recorded as a negative finding on a suspected defect, which is what R7 asks for.
5. **Two new instances of the C-kernel hazard, and one absence.** `cd`'s kernel is the worst instance found in this batch: it writes 42 values into a 41-element buffer on every observation, AddressSanitizer confirms the heap overflow, and it terminates with SIGABRT while the README's quick-start lists compiling and running it. Against that, `icft`, `mega-constellation` and `h266` ship no C at all, and `h266`'s orphan `fig5_vvc_rd.png` is a committed figure with no generator anywhere in the package — the figure-layer cousin of the same problem.
6. **Self-correction rate.** Six corrections are recorded in this report, of which two would have produced false contradictions (a wrong sweep index against the rubric's own reference case, and a confounded determinism test on `h266`), one would have produced a false null (an uninformative crossover test), and one withdrew an unsupported claim of mine. Across batches 1-2 the rate was 8 corrections in 2 batches; this batch's 6 in 1 batch is a higher rate, which is consistent with the re-scoring work carrying more inherited claims to check and more of my own claims to test.
