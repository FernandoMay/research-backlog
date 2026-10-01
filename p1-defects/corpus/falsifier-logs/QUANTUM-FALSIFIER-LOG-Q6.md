==============================================================================
Q6 falsifier — claim correspondence, Quantum package
property: each claim in main.tex describes the artifact and code it is
         attributed to
==============================================================================

  [INFO] C4 marker located at main.tex:86: \item \textbf{Measurement:} Sampling from the output probability distr

  [INFO] every line mentioning WalkSAT, with the numbers on it:
    main.tex: 22  We present a comprehensive numerical study of the Quantum Approximate Optimization Algorithm (QA
              numbers: ['0.986', '0.967', '2.8']   artifact mean 0.9556
    main.tex: 33  \item Quantitative comparison against classical solvers (WalkSAT, random sampling) across proble
    main.tex: 71  Classical SAT solvers fall into two main categories: complete solvers based on the Davis--Putnam
    main.tex:123  \item[WalkSAT:] A stochastic local search algorithm~\cite{selman1996} that flips variables in un
              numbers: ['0.3']   artifact mean 0.9556
    main.tex:150  Fig.~\ref{fig:noise} shows QAOA's performance under varying depolarizing noise rates. The algori
              numbers: ['0.97', '0.5', '0.964', '0.042', '0.876', '0.005']   artifact mean 0.9556
    main.tex:160  Fig.~\ref{fig:scaling} demonstrates QAOA's scaling characteristics across problem sizes. For $n=
              numbers: ['0.994', '0.972', '0.981', '0.959', '0.877', '0.874']   artifact mean 0.9556
    main.tex:200  To confirm the significance of QAOA's advantage over WalkSAT, we performed a paired $t$-test on 
              numbers: ['0.979', '0.009', '0.954', '0.029', '0.001', '1.14']   artifact mean 0.9556
    main.tex:202  We also analyzed the correlation between instance hardness (measured by WalkSAT performance) and
              numbers: ['0.96', '4.3']   artifact mean 0.9556
    main.tex:235  WalkSAT baseline & SAT ratio & 0.967 & 0.042 \\
              numbers: ['0.967', '0.042']   artifact mean 0.9556
    main.tex:245  Our results demonstrate that QAOA with shallow depth ($p \leq 2$) is competitive with classical 
    main.tex:262  \item QAOA with $p=2$ achieves SAT ratios up to 0.986, outperforming WalkSAT (0.967) by approxim
              numbers: ['0.986', '0.967']   artifact mean 0.9556
  artifact ws_m over the 11 noise levels: [0.9722, 0.9639, 0.9139, 0.9694, 0.9639, 0.9667, 0.95, 0.9722, 0.9556, 0.9722, 0.9111]
  artifact mean 0.9556  std 0.0214
  values stated for the OVERALL WalkSAT baseline: {'0.954': [200], '0.964': [150], '0.967': [22, 235, 235, 262]}
  values stated for WalkSAT at a specific n: {'0.972': 160, '0.959': 160}
  values matching the artifact mean 0.9556 to 3 decimals: NONE

  [CONTRADICTED] C1: main.tex:101 uses beta with H_B and labels it the mixing step, while qaoa_run applies cost_op(state, beta[l], H) then mixer(state, gamma[l])

  [CONTRADICTED] C10: main.tex:160 reads the random baseline as evidence of increasing instance hardness, but a random assignment satisfies a random 3-clause with probability 7/8 = 0.8750 independently of n and of the instance. The artifact's rand_m is [0.8767, 0.872, 0.8709, 0.8741], monotone decreasing: False, and its spread (0.0057) is far smaller than the discrepancy at n=14. The column carries no hardness information

  [CONTRADICTED] C11: the package maps readout to noise 0.075 and zne to 0.045, so less noise must score higher. The artifact's ranking by score is ['readout', 'both', 'zne', 'none'] while the ranking by applied noise is ['both', 'zne', 'readout', 'none']; monotonic in noise: False. The paper's ordering, its 'measurement errors dominate' reading and the implementation's parameterisation cannot all be right

  [CONTRADICTED] C12: main.tex:200 reports a PAIRED t-test, but Q4 F1 measured that the two arms share zero instances, so the data cannot be paired

  [UNSUPPORTED ] C13: metrics.json stores only per-level means and standard deviations; it contains no per-trial values (per-trial keys found: []). A t-test, its p-value and Cohen's d cannot be recomputed from the artifact

  [CONTRADICTED] C14: main.tex:209 budgets shots for the simulation, but the package draws no shots; the measurement is exact. The hardware-planning figures downstream of it are consequently unfounded

  [CONTRADICTED] C15: main.tex:146 states every configuration is repeated 5-6 times, but exp_depth draws one instance and one run per depth and reports no dispersion for the sat or gap columns (Q4 F3)

  [CONTRADICTED] C16: main.tex:248 attributes the performance plateau to the channel preserving the relative ranking of assignments. Q3 established the operation is an affine amplitude blend toward a vector of norm 1/sqrt(2^n), not a channel on the density matrix, so it has no established action on eigenstates or on orderings. The explanation is stated in terms of a property the implementation does not have

  [CONTRADICTED] C17: main.tex:248 claims the channel preserves the spectral ordering of the cost Hamiltonian's eigenstates. The implemented map acts on the amplitude vector and was never constructed on rho, so no statement about its action on eigenstates is supported

  [SUPPORTED   ] C18: main.tex:257 discloses that the classical optimisation uses random initialisation rather than gradient or Bayesian methods. Q2 independently established exactly this: candidate generation is independent of the objective and the objective only ranks. This limitation is accurate as written

  [CONTRADICTED] C2: three different noise operators: eq (main.tex:116) states the density map (1-lam)rho + lam*I/2^n; Algorithm 1 (main.tex:104) states an amplitude blend with lam/sqrt(2^n); the code blends amplitudes with noise/N

  [CONTRADICTED] C4: main.tex:86 claims sampling from the output distribution, but best_sat_from_state reads exact |psi|^2, takes the top 10 basis states and evaluates all of them; the package contains no shot sampling at all

  [CONTRADICTED] C5: main.tex:123 specifies a restart probability of 0.3, but walk_sat is a single 2000-flip run that returns on satisfaction; the string 'restart' does not appear in the simulator

  [CONTRADICTED] C6: main.tex:150 claims WalkSAT was evaluated on identical instances; Q4 F1 measured zero shared instances between the two arms

  [CONTRADICTED] C7: the manuscript gives 3 different values for the SAME overall WalkSAT baseline (0.954, 0.964, 0.967) at lines [22, 150, 200, 235, 262], and separately 2 per-n values that disagree with all of them. The artifact's mean over the 11 noise levels is 0.9556 +- 0.0214. Values matching the artifact to 3 decimals: none

  [CONTRADICTED] C8: main.tex:170 says the gap 'decreases marginally from 5.71 at p=1 to 5.97 at p=4', but the artifact's gap series is [5.7075, 6.6804, 6.2409, 5.9694]: p=4 (5.9694) is HIGHER than p=1 (5.7075), and the series rises to 6.6804 at p=2 before falling. The quoted endpoints are accurate; the direction word is not

  [CONTRADICTED] C9: main.tex:160 says the QAOA-WalkSAT gap stays at 2-3%, but the artifact's per-n gaps are {8: 0.0222, 10: 0.0044, 12: 0.0111, 14: 0.0222}; only 2 of 4 lie in the stated 2-3% band, and at n=10 the gap is 0.0044

==============================================================================
claims examined: 17
  CONTRADICTED   15
  UNSUPPORTED    1
  SUPPORTED      1

  A CONTRADICTED claim is one where a measured value or the code itself
  disagrees with the text. An UNSUPPORTED claim is one the artifact cannot
  settle at all — it is not thereby false. A SUPPORTED claim is accurate.
  C18 is recorded so that one accurate self-limiting statement is not
  averaged away by the surrounding contradictions; it is the same pattern
  observed in CRL and the opposite of LEO and ISAC.

  Scientific merit is NOT adjudicated here. No claim is assigned a
  scientific disposition; that is Q7 and requires the second matrix.

## Defects found by the release gate after this falsifier was first written

`tests/release_gate.py` requires every falsifier to be RED **and** to have a working
positive control. It rejected the first version of this file on two counts.

1. **This falsifier had no positive control at all.** It had never agreed with
   anything, so nothing demonstrated that its CONTRADICTED verdicts meant anything
   rather than being a checker that rejects every input. This is the same defect
   class the programme exists to detect, found in the programme's own instrument. A
   synthetic control now runs the same extraction and comparison logic against a
   synthetic manuscript and artifact whose correspondence is known in advance, and
   requires the checker to report them as matching.
2. **It expressed verdicts in a vocabulary the gate could not read.** Per-claim
   verdicts are CONTRADICTED / UNSUPPORTED / SUPPORTED, which is more informative than
   FAIL / PASS per claim, but it left the gate seeing zero FAILs. The per-claim
   vocabulary is kept and a single uniform failure line was added.

Q4 was rejected by the same gate for marking its positive controls as `[INFO]` rather
than `[PASS]` — the controls had been passing and the gate could not see it. Marking
is not decoration: an invisible passing control is an unverified one.

A third defect was found earlier in this file and is described above: C4's marker
pattern never matched, so the sampling claim was silently omitted from the first
report. The claim count moved from 16 to 17 once the pattern was fixed and asserted
present.

**Fourteen falsifier defects across six falsifiers in this package.** All are
retained. Three of them (Q2's zero-gradient control, Q3's non-channel control
formula, and `np.diag` on a 1-D array) each invalidated a result before it was
reported, and one (C4's dead pattern) silently reduced the scope of a report that was
otherwise believed complete.
