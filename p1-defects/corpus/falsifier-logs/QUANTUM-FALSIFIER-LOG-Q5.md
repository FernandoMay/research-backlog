==============================================================================
Q5 falsifier — the meaning of the 'gap' column in fig3
property: the QAOA gap is an approximate expectation value minus the exact
         ground energy, both on normalised states of the same Hamiltonian
==============================================================================

  [INFO] F1 is `np.min(H)` the ground energy of H?
         H shape (256,) (a 1-D diagonal, not a matrix), Hermitian residual 0.0e+00
         min(H) = 1.000000   max(H) = 8.000000
         smallest eigenvalue of the operator diag(H): 1.000000
         H is non-negative: True; min(H) == 0 means the instance is SATISFIABLE: False
         this instance has m/n = 4.50 at n=8, m=36. The 3-SAT satisfiability
         threshold is near 4.27, so a ground energy of 1 is expected here rather than 0.
         exp_depth uses n=12, m=60, i.e. m/n = 5.0, further above the transition.
         np.min(H) is the exact ground energy, and for a penalty counting
         violations it is 0 whenever the instance is satisfiable. The reported
         gap therefore reduces to `be` with no reference term.
  [PASS] F1 np.min(H) is the ground energy

  [INFO] F2 is `be` a proper expectation value on a normalised state?

         positive control — noise = 0, where every step is unitary:
         ||psi||^2 == 1 at every depth to 1e-9. The control can discriminate, so the
         failures below are informative.

         measured under the configuration exp_depth actually uses (noise=0.02):
           p      ||psi||^2      scale   gap as reported   gap renormalised         bias
           1     0.96017873   0.960179        2.17145832         2.30298749   -1.315e-01
           2     0.92291395   0.922914        2.64190681         2.94609574   -3.042e-01
           3     0.88628010   0.886280        2.24256842         2.65862713   -4.161e-01
           4     0.85043503   0.850435        2.24303991         2.81338939   -5.703e-01
  [FAIL] F2 the reported gap is not an expectation value. Largest bias 5.703e-01.
         The bias VARIES with p by 4.388e-01 across depths, so the depth trend in
         fig3 mixes the circuit-depth effect with a normalisation artefact that itself
         varies with depth. The two cannot be separated by the reported column.

  [INFO] F3 what does the depth curve actually vary?
         `be` is the minimum of 35 uniform random parameter draws (Q2 established the
         search is random). The parameter space is [0,pi]^{2p}, so it grows with depth:
           p=1: 2 parameters searched, 35 draws, 1.225e+03 possible settings
           p=2: 4 parameters searched, 35 draws, 1.501e+06 possible settings
           p=3: 6 parameters searched, 35 draws, 1.838e+09 possible settings
           p=4: 8 parameters searched, 35 draws, 2.252e+12 possible settings
         Holding the draw count fixed while the space grows means the statistic being
         plotted is a sample minimum over a changing-dimensional space, not a
         convergence curve. Whether the observed direction agrees with a genuine
         depth effect cannot be settled from the reported column alone.

         direct check — same depth, nested prefixes of ONE draw sequence:
           p=2, best of the first   5 draws -> reported gap 3.101942
           p=2, best of the first  15 draws -> reported gap 2.604952
           p=2, best of the first  35 draws -> reported gap 2.604952
         the reported 'gap' is a running minimum over random draws: True monotone.
         With the draw count fixed at 35 across p=1..4, the only thing that
         changes with p is the dimension of the space being sampled. The
         reported column is therefore a statistic of the optimiser's budget
         before it is a statistic of the circuit's depth.
==============================================================================
FAILED: F2-gap-not-a-proper-expectation-value, F3-gap-tracks-draw-count-not-depth

Implementation fact: H is a non-negative penalty counting violated
clauses and np.min(H) is its exact ground energy, which is 1 rather than
0 because the instances sit above the 3-SAT threshold; `be` is
on a state that is not normalised,
with a bias that varies with p; and the quantity is a minimum over a
fixed number of random draws.
Claim correspondence: NOT ADJUDICATED. What the depth curve is taken
to show is Q6.

## Falsifier defects found while building Q5 (all retained)

1. **`np.diag(H)` on a 1-D array fabricates a matrix.** `make_H` returns a 1-D
   array holding the *diagonal* of the cost operator. Calling `np.diag(H)` on it
   BUILDS a matrix with H on the diagonal — a 256x256 identity for H = [1,2,...].
   The test printed `min over assignments = 0.000000` and would have concluded
   every instance is satisfiable. The true minimum is 1. This is the most
   consequential accessor error in the Quantum package so far, because it
   supported the opposite conclusion on the headline fact.
2. **A stale PASS message survived a corrected computation.** The F1 branch still
   asserted "0 whenever the instance is satisfiable ... the reported gap reduces to
   `be`" after the computation had been corrected to report a ground energy of 1.
   A passing branch whose text contradicts its own numbers is worse than a failing
   branch, because it is believed.
3. **F3's budget test re-seeded per budget.** k=5, 15 and 35 were run with seeds
   `300 + draws`, so the three runs saw different random streams. The resulting
   non-monotone 3.05 -> 2.24 -> 2.67 was mostly seed noise presented as a trend.
   The test now draws one sequence of 35 candidates and takes nested prefixes of
   it, which yields the honest monotone 3.101942 -> 2.604952 -> 2.604952.

## Why F2's bias is worse than a constant offset

The normalisation factor is not constant across depth:

    p=1  ||psi||^2 = 0.960179   bias -1.315e-01
    p=2  ||psi||^2 = 0.922914   bias -3.042e-01
    p=3  ||psi||^2 = 0.886280   bias -4.161e-01
    p=4  ||psi||^2 = 0.850435   bias -5.703e-01

It falls monotonically with depth, so the artefact is confounded with exactly the
independent variable fig3 plots. A constant multiplicative error would be
survivable — it would scale every point equally and leave the trend intact. A
depth-dependent one cannot be removed by rescaling, and the reported column
contains no way to detect it. This is a cross-falsifier consequence: Q3's A1
defect propagates into Q5's headline quantity with the same sign and a magnitude
that grows with depth.

Note also that the raw reported gaps do NOT fall monotonically with p
(2.171, 2.642, 2.243, 2.243) while the renormalised gaps do
(2.303, 2.946, 2.659, 2.813) — and neither is monotone. The falsifier does not
claim a direction for the depth effect; it establishes only that the reported
column is not the quantity its label names, and that its error is depth-coupled.

## Numbers in this log must not be compared to any published figure

`exp_depth` uses n=12, m=60, 35 draws. This falsifier uses n=8, m=36, 35 draws,
one instance, to stay bounded. The gap values here (2.171, 2.642, 2.243, 2.243)
are a different experiment on a different instance and are not a reproduction of
fig3.

## Disposition boundaries

- Implementation fact: the gap's reference term is the exact ground energy (1, not
  0); the approximate term is a depth-dependent normalisation artefact; the
  statistic is a running minimum over a fixed draw count in a growing-dimensional
  space.
- Scientific interpretation: NOT adjudicated. Whether a penalty Hamiltonian is an
  appropriate cost operator is a modelling choice.
- Claim correspondence: NOT ADJUDICATED. What the depth curve is taken to
  demonstrate is Q6.
