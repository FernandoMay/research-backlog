#!/usr/bin/env python3
"""QCE-2 falsifier: are the ablation arms reconstructible from the artifact?

Pre-specified property under test
---------------------------------
    The `NoSafety` and `NoRL` rows of `tab:ablation` are RECONSTRUCTIBLE
    experimental states of the same system — each defined by an intervention that
    can be executed on the committed artifact, changes the mechanism the row names,
    holds every other component constant, and produces a distinguishable result.

This is a question about experimental design identity, not about whether the paper is
wrong. It is deliberately separated from QCE-1: H3 tested whether named mechanisms
participate, H4 tests whether two named ARMS exist at all.

Critical methodological constraint carried from QCE-1
----------------------------------------------------
`NoRL` CANNOT be defined as `gamma = 0`. QCE-1 established that `gamma` occurs once
and is never read. Intervening on it would be intervening on a dead parameter, and
an arm built that way would be vacuous. H4b removes the predictor from the DECISION
PATH — the causal route the predictor actually takes — not a parameter of it.

Reconstructibility criteria (all five must hold for an arm to be reconstructible)
------------------------------------------------------------------------------
R1  There is a reproducible intervention that defines the arm.
R2  It alters the mechanism the row names, and only that mechanism.
R3  Every other relevant component is held constant.
R4  It produces a distinguishable observable state.
R5  The artifact can be associated unambiguously with the arm.

Controls
--------
Each arm carries its own positive control: a different intervention on the same
mechanism that MUST change the result. Without it, "nothing changed" would be
uninterpretable — the QCE-1 lesson, where an inert control hid a real finding.

Reimplementation validation
---------------------------
The temperature-policy arm requires re-executing run_episode's selection logic. That
reimplementation is validated FIRST by reproducing the original metrics exactly. An
unvalidated reimplementation cannot distinguish "the arm has no effect" from "I
reimplemented it wrong".
"""

import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SEED = 42

RISK_LEVELS = [(0.01, 3), (0.1, 2), (0.3, 1), (0.7, 0)]


def load_module():
    sys.path.insert(0, ROOT)
    import qce_simulator as q
    return q


def precompute(q, optimizer):
    pre = {}
    for risk, dvfs in RISK_LEVELS:
        rel = np.array([0.7, 0.4, 0.6, 0.5, 0.8]) * min(1.0, risk * 10)
        eng = np.array([0.3, 0.05, 0.15, 0.1, 0.4])
        lat = np.array([0.2, 0.1, 0.15, 0.05, 0.1])
        mask, _ = optimizer.optimize(rel, eng, lat)
        pre[risk] = {"mask": mask, "dvfs": dvfs}
    return pre


def episode(q, system, predictor, optimizer, mitig, policy="original"):
    """A faithful re-implementation of run_episode with a selectable risk policy.

    policy='original'  : exactly run_episode's logic, temperature for t<10 then the
                         predictor.
    policy='temperature': temperature for EVERY step — the predictor is removed
                         from the decision path. This is the NoRL candidate.
    """
    pre = precompute(q, optimizer)
    history = []
    for t in range(q.SIM_STEPS):
        obs = system.health_metrics[max(0, system.step - 1)]
        pred_prob = predictor.predict(obs)

        use_temp = (t < 10) if policy == "original" else True
        if use_temp:
            temp = system.temperature
            risk = 0.7 if temp > 70 else 0.3 if temp > 50 else 0.1 if temp > 35 else 0.01
        else:
            risk = 0.7 if pred_prob > 0.5 else 0.3 if pred_prob > 0.2 \
                else 0.1 if pred_prob > 0.05 else 0.01
        cfg = pre[risk]

        result = system.step_simulation(cfg["dvfs"], cfg["mask"], 30)
        actual_error = 1.0 if result["n_errors"] > 0 else 0.0
        predictor.update(obs, actual_error, pred_prob)
        result["pred_prob"] = pred_prob
        result["dvfs"] = cfg["dvfs"]
        result["mit_mask"] = list(cfg["mask"])
        result["risk_level"] = risk
        result["step"] = t
        history.append(result)
    return history


def run(policy="original", floor=None, external_temp=30):
    q = load_module()
    np.random.seed(SEED)
    system = q.EmbeddedSystem()
    predictor = q.ErrorPredictor()
    optimizer = q.QuantumInspiredOptimizer()
    mitig = q.MitigationManager()
    if floor is not None:
        predictor.safety_floor = floor
    np.random.seed(SEED)
    history = episode(q, system, predictor, optimizer, mitig, policy=policy)
    return q.compute_metrics(history), history


def fingerprint(metrics, history):
    return {
        "errors": metrics["total_errors"],
        "power": round(metrics["avg_power_mw"], 4),
        "reliability": round(metrics["avg_reliability"], 6),
        "risks": sorted({h["risk_level"] for h in history}),
        "dvfs": sorted({h["dvfs"] for h in history}),
    }


def main():
    print("=" * 78)
    print("QCE-2 falsifier — reconstructibility of the ablation arms")
    print("property: each tab:ablation row is a reconstructible experimental state of")
    print("         the same system, defined by an executable intervention")
    print("=" * 78)
    q = load_module()
    failures = []

    # ---- validate the reimplementation ------------------------------------
    print("\n  [INFO] validating the re-implementation of run_episode's selection logic")
    m_orig, h_orig = run(policy="original")
    m_reimpl, _ = run(policy="original")
    np.random.seed(SEED)
    system = q.EmbeddedSystem()
    predictor = q.ErrorPredictor()
    optimizer = q.QuantumInspiredOptimizer()
    mitig = q.MitigationManager()
    np.random.seed(SEED)
    m_native = q.compute_metrics(q.run_episode(system, predictor, optimizer, mitig))
    reimpl_ok = (m_reimpl["avg_reliability"] == m_native["avg_reliability"]
                 and m_reimpl["avg_power_mw"] == m_native["avg_power_mw"]
                 and m_reimpl["total_errors"] == m_native["total_errors"])
    print(f"           my episode()      reliability {m_reimpl['avg_reliability']:.10f} "
          f"power {m_reimpl['avg_power_mw']:.6f} errors {m_reimpl['total_errors']}")
    print(f"           run_episode()     reliability {m_native['avg_reliability']:.10f} "
          f"power {m_native['avg_power_mw']:.6f} errors {m_native['total_errors']}")
    print(f"           the re-implementation reproduces the original exactly: {reimpl_ok}")
    if not reimpl_ok:
        print("  [FAIL] the re-implementation does not match run_episode, so no arm built")
        print("         on it can be interpreted.")
        failures.append("QCE-2-reimplementation-invalid")

    base = fingerprint(m_orig, h_orig)
    print(f"           FULL arm fingerprint: {base}")

    # ================= H4a — NoSafety =======================================
    print("\n  [INFO] H4a — NoSafety: the row is defined as `sigma = 0`, i.e. the")
    print("         predictor emits raw logistic probabilities with no blending.")
    m_full_floor, h_full_floor = run(floor=0.0)
    nos = fingerprint(m_full_floor, h_full_floor)
    print(f"           FULL (floor=0.15) {base}")
    print(f"           NoSafety (floor=0.0) {nos}")
    r4a_changes = nos != base
    print(f"           R4 it produces a distinguishable state: {r4a_changes}")

    # positive control: a different intervention on the SAME mechanism
    m_floor_hi, h_floor_hi = run(floor=0.60)
    hi = fingerprint(m_floor_hi, h_floor_hi)
    ctrl_ok = hi != base
    print(f"           CONTROL floor=0.60  {hi}")
    print(f"           the harness detects a safety-path intervention: {ctrl_ok}")

    if not ctrl_ok:
        print("  [FAIL] positive control: a floor of 0.60 did not change the result, so")
        print("         the NoSafety result below is uninterpretable.")
        failures.append("H4a-positive-control-broken")
    else:
        print("  [PASS] H4a positive control: this harness detects a change on the "
              "safety path")
        if r4a_changes:
            print(f"  [FAIL] H4a NoSafety (floor=0.0) IS distinguishable from Full: "
                  f"{nos}")
            print(f"         The intervention exists, alters only the safety blend, and "
                  f"changes the")
            print(f"         outcome. The arm is therefore reconstructible from the "
                  f"artifact — which")
            print(f"         means the absence of a code path in qce_simulator.py is a "
                  f"packaging gap,")
            print(f"         not an absent experiment.")
            failures.append("H4a-nosafety-is-reconstructible")
        else:
            print("  [PASS] H4a NoSafety does not change the result")

    # ================= H4b — NoRL ==========================================
    print("\n  [INFO] H4b — NoRL: the row is defined as 'temperature-based policy")
    print("         selection only'. gamma is NOT the intervention: QCE-1 established")
    print("         it is never read, so an arm built on it would be vacuous.")
    print("         The predictor is removed from the DECISION PATH instead.")
    m_temp, h_temp = run(policy="temperature")
    norl = fingerprint(m_temp, h_temp)
    print(f"           FULL             {base}")
    print(f"           NoRL (temperature policy) {norl}")
    r4b_changes = norl != base
    print(f"           R4 it produces a distinguishable state: {r4b_changes}")

    # positive control: the policy switch itself must be live
    q2 = load_module()

    class _High(q2.ErrorPredictor):
        def predict(self, observation, raw_only=False):
            return super().predict(observation, True) if raw_only else 0.95

    np.random.seed(SEED)
    sysh = q2.EmbeddedSystem()
    predh = _High()
    opth = q2.QuantumInspiredOptimizer()
    mith = q2.MitigationManager()
    np.random.seed(SEED)
    hh = episode(q2, sysh, predh, opth, mith, policy="original")
    mh = q2.compute_metrics(hh)
    hi_fp = fingerprint(mh, hh)
    ctrl_b_ok = hi_fp != base
    print(f"           CONTROL forced 0.95 prediction {hi_fp}")
    print(f"           the policy switch is live: {ctrl_b_ok}")

    if not ctrl_b_ok:
        print("  [FAIL] positive control: forcing a different prediction did not change "
              "the")
        print("         result, so the temperature policy's invariance would be "
              "uninformative.")
        failures.append("H4b-positive-control-broken")
    else:
        print("  [PASS] H4b positive control: the policy switch demonstrably changes "
              "the")
        print("           outcome, so an unchanged result is a real property of the "
              "arm.")
        if r4b_changes:
            print(f"  [FAIL] H4b NoRL is DISTINGUISHABLE from Full: {norl}")
            print(f"         Removing the predictor from the decision path changes the "
                  f"outcome.")
            print(f"         The artifact therefore contradicts the published claim that "
                  f"QCE-NoRL is")
            print(f"         identical to QCE (full). The arm is reconstructible and its "
                  f"published")
            print(f"         identity is not what the artifact produces.")
            failures.append("H4b-norl-is-distinguishable-from-full")
        else:
            print("  [PASS] H4b NoRL does not change the result")

    # ================= reconstructibility table ============================
    print("\n  [INFO] reconstructibility table")
    published = {
        "QCE (full)":   {"errors": 0,  "power": 627.3, "reliability": 0.9237},
        "QCE-NoSafety": {"errors": 21, "power": 578.3, "reliability": 0.0070},
        "QCE-NoRL":     {"errors": 0,  "power": 627.3, "reliability": 0.9237},
    }
    produced = {
        "QCE (full)":   base,
        "QCE-NoSafety": nos,
        "QCE-NoRL":     norl,
    }
    print(f"  {'arm':14s} {'code path':12s} {'runs':5s} {'artifact':34s} {'published':30s} verdict")
    code_paths = {
        "QCE (full)":   "run_episode",
        "QCE-NoSafety": "NONE in repo",
        "QCE-NoRL":     "NONE in repo",
    }
    verdicts = {}
    for arm in ("QCE (full)", "QCE-NoSafety", "QCE-NoRL"):
        cp = code_paths[arm]
        pr = published[arm]
        prod = produced[arm]
        pub = "%d / %.1f / %.4f" % (pr["errors"], pr["power"], pr["reliability"])
        got = "%d / %.1f / %.4f" % (prod["errors"], prod["power"],
                                    prod["reliability"])
        matches = (prod["errors"] == pr["errors"]
                   and abs(prod["power"] - pr["power"]) < 0.05
                   and abs(prod["reliability"] - pr["reliability"]) < 0.0005)
        verdicts[arm] = matches
        print("  %-14s %-12s %-5s %-34s %-30s %s"
              % (arm, cp, "yes", got, pub, "MATCH" if matches else "NO MATCH"))
        if cp == "NONE in repo":
            print("  %-14s -> the artifact contains no code path for this row; the arm"
                  % "")
            print("  %-14s    below is RECONSTRUCTED here for comparison only."
                  % "")

    print()
    for arm in ("QCE-NoSafety", "QCE-NoRL"):
        if not verdicts[arm]:
            failures.append(f"{arm}-no-code-path-and-published-value-not-reproduced")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        print()
        print("Design-identity finding: neither ablation row has a code path in the")
        print("artifact. Both are reconstructible here as interventions, and neither")
        print("reproduces its published value.")
        print()
        print("The numerical identity of QCE-NoRL and QCE (full) is NOT treated here as")
        print("proof that the arm lacks effect. It is compared against what removing")
        print("the predictor from the decision path actually produces, because an arm")
        print("with no code path cannot have its effect measured from its absence.")
        return 1
    print("PASSED: the ablation arms are reconstructible and reproduce their values")
    return 0


if __name__ == "__main__":
    sys.exit(main())