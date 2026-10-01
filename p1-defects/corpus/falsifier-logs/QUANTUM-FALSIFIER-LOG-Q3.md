==============================================================================
Q3 falsifier — the `noise` parameter and the channel axioms
property: the noise rate is a physical depolarizing channel, so that
         performance measured at different noise levels is like-for-like
==============================================================================

  [INFO] positive control — the true channel rho -> (1-lam)rho + lam*I/N:
         Born probabilities sum to 1 for all 3 states x 4 levels,
         and the channel preserves trace and positivity on rho. The control can
         discriminate, so the failures below are informative.

  [INFO] A1 normalisation — does the applied map return a state?
         state                       noise=0.05      noise=0.15      noise=0.30      noise=0.50
         basis |0..0>                  0.908594        0.739844        0.521875        0.296875
         uniform |+..+>                0.926406        0.787656        0.600625        0.390625
         random normalised             0.901060        0.719622        0.488568        0.257224
  [FAIL] A1 the map does not preserve normalisation. Largest deviation from 1: 0.742776
         The output of `qaoa_run` is not a quantum state and |psi|^2 does not sum to 1.
         Energies computed as conj(state) @ (H*state) are therefore scaled by a
         noise-dependent factor and are NOT comparable across noise levels.

  [INFO] A2 the mixing target must itself be a normalised state:
         the code mixes toward ones(N)/N, whose ||.||^2 = 0.062500 for N = 16
         its norm is 0.250000; a state has norm 1.000000
  [FAIL] A2 the mixing target is not a state. A convex combination that
         includes a non-state endpoint cannot produce a state.

  [INFO] A3 linearity — a channel is linear, so it must send 0 to 0:
         T(0) = noise*ones(N)/N, whose ||.||^2 = 5.625000e-03 (a channel requires exactly 0)
         T(2a - 0.5b) - (2T(a) - 0.5T(b)) has norm 9.375000e-03
  [FAIL] A3 the map is AFFINE, not linear: it has a constant term noise*ones(N)/N and
         does not send the zero vector to zero. A quantum channel is linear and
         satisfies T(0) = 0, so this operation is not a channel on the amplitude
         vector regardless of what it does to normalisation.

  [INFO] A4 the density reading, constructed explicitly:
         basis |0..0>       trace 1.000000 -> 1.000000   min eigenvalue -1.909e-17
         uniform |+..+>     trace 1.000000 -> 1.000000   min eigenvalue -1.877e-17
         Read this way the map IS trace-preserving and positive, but it replaces part
         of rho with the uniform PURE state rather than the maximally mixed
         state — a biased, not a depolarizing, channel. It is also NOT the
         map the code executes. Both readings are recorded; neither rescues
         the amplitude reading, which is the one in use.
  [PASS] A4 trace and positivity hold under the density reading (see note)

  [INFO] A5 known-state intervention — basis state at noise = 0.5:
         code : p[0] = 0.282227   sum p = 0.296875   min p = 9.766e-04
         true : p[0] = 0.531250   sum p = 1.000000   min p = 3.125e-02
  [FAIL] A5 the code's probabilities sum to 0.296875 where a channel's must sum to 1.
         Its first-amplitude probability is 0.282227 against the true 0.531250,
         and its least probable outcome gets 9.766e-04 against the true 3.125e-02: the code
         collapses probability mass rather than distributing it.

  [INFO] downstream exposure — where the missing normalisation lands:
         noise=0.05  raw sum p = 0.926406   after best_sat_from_state renormalisation = 1.000000
         noise=0.15  raw sum p = 0.787656   after best_sat_from_state renormalisation = 1.000000
         noise=0.30  raw sum p = 0.600625   after best_sat_from_state renormalisation = 1.000000
         noise=0.50  raw sum p = 0.390625   after best_sat_from_state renormalisation = 1.000000
         `best_sat_from_state` renormalises (probs /= probs.sum()), so the SAT RATIO
         silently absorbs this defect. `optimize_qaoa` evaluates conj(state) @ (H*state)
         WITHOUT renormalising, so the energy it compares is computed on a non-state.
==============================================================================
FAILED: A1-normalisation-not-preserved, A2-mixing-target-not-a-state, A3-affine-not-linear, A5-not-a-depolarizing-channel

Implementation fact: the `noise` parameter applies a convex blend of
amplitudes toward ones(N)/N. The map is affine rather than linear, its
endpoint is not a state, and its output does not preserve normalisation.
Claim correspondence: NOT ADJUDICATED. Whether the manuscript's
'depolarizing noise' narrative corresponds to this is Q6.

## Falsifier defects found while building Q3 (all retained)

1. **The positive control used a formula that does not describe a channel.** The
   first control was `psi -> sqrt(1-lam)*psi + sqrt(lam)*|+..+>`. It reported
   ||.||^2 = 1.25 at lam=0.5. That arithmetic is CORRECT and the formula is
   wrong: <basis|+..+> = 1/sqrt(N) is not zero, so the cross term survives and
   the blend cannot be unit-norm. The depolarizing channel acts on rho and has no
   simple amplitude-vector form. The control was rebuilt on rho and now passes.
   Had this not been caught, every result below would have been rejected along
   with it — correctly — but for the wrong stated reason.
2. **A3 reported "not linear" without naming the mechanism.** The residual
   9.375e-03 is exactly noise/2N, the constant term. The map is AFFINE: it fails
   linearity specifically because T(0) != 0. A test that reports a symptom without
   its cause invites a repair that removes the symptom instead of the defect.
3. **A5 inherited the broken control.** Its "true" reference was the same invalid
   amplitude formula, so the comparison could not have been meaningful.

## Why A4 passing does not rescue the operation

Read as a density map, (1-lam)*rho + lam*ones(N)/N is trace-preserving and
positive. It is therefore a legitimate channel — but it mixes toward the uniform
PURE state, not the maximally mixed state, so it is a BIASED channel rather than
a depolarizing one. Two independent reasons it does not match the label:

  - it is biased rather than depolarizing, and
  - it is not the map the code executes.

The code applies the expression to the amplitude vector inside `qaoa_run`. A4 is
recorded as passing so the record shows both readings were examined, not only the
one that failed.

## The consequential asymmetry

`best_sat_from_state` renormalises (`probs /= probs.sum()`), so the SAT RATIO
column absorbs this defect completely and the noise curve in fig1 is not directly
invalidated by A1. `optimize_qaoa` evaluates `conj(state) @ (H*state)` WITHOUT
renormalising, so every energy it compares across noise levels is computed on a
non-state and scaled by a different factor at each noise level. Any selection
made under noise therefore optimises a quantity that is not the cost Hamiltonian.

This asymmetry is the finding with consequences for the figures. The A1 failure
alone is an axiom violation; the asymmetry is what reaches the artifact.

## Disposition boundaries

- Implementation fact: affine amplitude blend toward a non-state; output not
  normalised; downstream asymmetry between the two consumers.
- Scientific interpretation: not adjudicated. Whether a state-vector-level noise
  proxy is an acceptable shortcut is a modelling decision, not a bug verdict.
- Claim correspondence: NOT ADJUDICATED. The axis label "Depolarizing Noise Rate"
  versus this operation is Q6.
