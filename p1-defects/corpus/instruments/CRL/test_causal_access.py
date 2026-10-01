#!/usr/bin/env python3
"""CRL causal-access falsifier.

Property under test.

    The experiment must have causal access to the property it claims to measure.
    An arm whose metric ignores the stressor cannot report the effect of
    removing a mechanism, at any failure rate.

The comparison the paper sets up varies, on the face of it, one factor: the
presence of the control plane. Read the two arms and two things change.

    with CRL     crl.run_simulation(...)     failure_probability = 0.20
        for node in ready_nodes:
            if agent and agent.state in (IDLE, EXECUTING):   node.status = "completed"
        ... then self.run_cycle(agents, dag)

    without CRL  inline loop in run_comparison
        for node in ready_nodes:
            node.status = "completed"
        # no run_cycle

So the arm labelled "without CRL" differs from the other in the completion guard
AND in whether the recovery loop runs. That is a confound in the package's own
comparison, and this falsifier exists to separate the mechanism question from the
measurement question rather than to reproduce the confound.

**The arms are replicated exactly as written.** An earlier probe in this audit
called run_cycle inside both arms, which made the baseline recover like the CRL
and produced zero failed agents at p=1.00 -- a result that contradicted the
defect. That probe was wrong, not the package, and the error is recorded here
because the same mistake is available to anyone who reads the loop quickly.

Three controls:

    F1a  reproduce the ceiling. At every failure rate, both arms as written
         report the same completion. Expected: reproduced. This is the effect
         the manuscript itself names at L150.
    F1b  causal opportunity. Fail the agent assigned to a ready node
         immediately before the marking loop, so the guard decision is
         load-bearing. The question is not whether the metric IMPROVES. It is
         whether the guard's decision changes the outcome at all.
    F1c  negative control. Build two arms that are identical by construction.
         They must agree exactly. If they do not, the instrument is measuring
         something other than the guard, and no other result here can be
         trusted.
"""

import importlib.util
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "src" / "crl_simulation.py"

N_AGENTS, N_TASKS, N_CYCLES = 10, 20, 200
SEED = 7


def load_module():
    import random
    sys.path.insert(0, str(TARGET.parent))
    spec = importlib.util.spec_from_file_location("crl_target", TARGET)
    module = importlib.util.module_from_spec(spec)
    sys.modules["crl_target"] = module
    spec.loader.exec_module(module)
    return module, random


def run_arm(m, random, p_fail, guarded, run_cycle, *,
            pre_fail_assigned=False, max_injections=None):
    """One arm. `guarded` and `run_cycle` are the two things the package's own
    arms vary, so they are exposed as independent switches rather than conflated
    into an arm label.

    pre_fail_assigned is the F1b intervention: before the marking loop, fail the
    agent assigned to a node that is ready to be marked. The guard's decision
    then decides whether that node completes.

    max_injections caps the stressor dose. It exists because the first version of
    F1b had no cap and the two arms then received wildly different exposure: the
    guarded arm never drained and absorbed 200 injections while the unguarded arm
    drained in four cycles and absorbed 3. A 45-point difference in completion
    under a 66-fold difference in dose measures the dose, not the guard.
    """
    np.random.seed(SEED)
    random.seed(SEED)
    runner = m.SimulationRunner(num_agents=N_AGENTS, num_tasks=N_TASKS)
    agents = runner.create_agents()
    dag = runner.create_dag(agents)
    crl = m.CognitiveResilienceLayer()

    failed_agents_total = 0
    cycles = 0
    mods = 0

    for cycle in range(N_CYCLES):
        if dag.is_complete():
            break

        capped = (max_injections is not None
                  and failed_agents_total >= max_injections)
        if pre_fail_assigned:
            ready = dag.get_ready_nodes(
                {n.node_id for n in dag.nodes if n.status == "completed"})
            if not capped:
                for node in ready:
                    a = next((x for x in agents
                              if x.agent_id == node.agent_id), None)
                    if a is not None and a.state is not m.AgentState.FAILED:
                        a.state = m.AgentState.FAILED
                        failed_agents_total += 1
                        break
        elif not capped and random.random() < p_fail:
            active = [a for a in agents if a.state != m.AgentState.FAILED]
            if active:
                random.choice(active).state = m.AgentState.FAILED
                failed_agents_total += 1

        ready_nodes = dag.get_ready_nodes(
            {n.node_id for n in dag.nodes if n.status == "completed"})

        for node in ready_nodes:
            if guarded:
                agent = next((a for a in agents if a.agent_id == node.agent_id), None)
                if agent and agent.state in (m.AgentState.IDLE, m.AgentState.EXECUTING):
                    node.status = "completed"
            else:
                node.status = "completed"

        if run_cycle:
            res = crl.run_cycle(agents, dag)
            mods += len(res["modifications"])

        cycles = cycle + 1

    completed = sum(1 for n in dag.nodes if n.status == "completed")
    return {
        "completion": completed / max(len(dag.nodes), 1),
        "cycles": cycles,
        "failures_injected": failed_agents_total,
        "failed_at_end": sum(1 for a in agents if a.state is m.AgentState.FAILED),
        "modifications": mods,
    }


def main():
    print("property: the experiment has causal access to the property it claims")
    print("         to measure")
    print("=" * 78)

    m, random = load_module()
    failures = []

    # --- F1a: reproduce the ceiling -----------------------------------------
    print(f"  [INFO] F1a the package's two arms exactly as written, across p_fail:")
    print(f"         {'p':>5} | {'CRL arm (guarded+cycle)':<26} | {'baseline (unguarded, no cycle)':<30}")
    ceiling = True
    for p in (0.05, 0.20, 0.50, 0.90, 1.00):
        crl = run_arm(m, random, p, guarded=True, run_cycle=True)
        base = run_arm(m, random, p, guarded=False, run_cycle=False)
        print(f"         {p:>5.2f} | {crl['completion']:>7.2%} cyc{crl['cycles']:<3} "
              f"fail{crl['failures_injected']} mods{crl['modifications']:<3} | "
              f"{base['completion']:>7.2%} cyc{base['cycles']:<3} "
              f"fail{base['failures_injected']}")
        if abs(crl["completion"] - base["completion"]) > 1e-9:
            ceiling = False

    if ceiling:
        print(f"  [PASS] F1a the ceiling is reproduced: both arms report an identical "
              f"completion at every")
        print(f"           failure rate, including p=1.00. This is the effect the "
              f"manuscript itself names at")
        print(f"           L150, so the defect is real but the paper is not unaware of it.")
    else:
        print(f"  [FAIL] F1a the ceiling was expected and not reproduced; the arms differ "
              f"somewhere")
        failures.append("F1a-ceiling-not-reproduced")

    # --- F1b: causal opportunity --------------------------------------------
    print(f"  [INFO] F1b fail the agent assigned to a ready node immediately before the "
          f"marking loop,")
    print(f"         so the guard's decision decides that node's outcome:")
    # Dose-matched. The dose is calibrated first by letting the unguarded arm run
    # uncapped to see how many injections it absorbs before draining, then both
    # arms receive exactly that many.
    probe = run_arm(m, random, 0.0, guarded=False, run_cycle=False,
                    pre_fail_assigned=True)
    dose = probe["failures_injected"]
    print(f"         calibrating the stressor dose from the unguarded arm: {dose} "
          f"injection(s) before it drains")
    guarded = run_arm(m, random, 0.0, guarded=True, run_cycle=True,
                      pre_fail_assigned=True, max_injections=dose)
    unguarded = run_arm(m, random, 0.0, guarded=False, run_cycle=False,
                        pre_fail_assigned=True, max_injections=dose)
    print(f"         guarded   completion {guarded['completion']:>7.2%}  "
          f"failures injected {guarded['failures_injected']}  cycles {guarded['cycles']}")
    print(f"         unguarded completion {unguarded['completion']:>7.2%}  "
          f"failures injected {unguarded['failures_injected']}  cycles {unguarded['cycles']}")

    if guarded["failures_injected"] != unguarded["failures_injected"]:
        print(f"  [FAIL] F1b the arms did not receive the same dose "
              f"({guarded['failures_injected']} vs {unguarded['failures_injected']}); "
              f"a completion")
        print(f"         difference would measure exposure rather than the guard")
        failures.append("F1b-dose-mismatch")
    elif abs(guarded["completion"] - unguarded["completion"]) > 1e-9:
        print(f"  [PASS] F1b the guard has causal access to the reported metric: an "
              f"intervention that")
        print(f"           reaches the guard changes the outcome by "
              f"{abs(guarded['completion'] - unguarded['completion']):.2%}.")
        print(f"           The mechanism the paper credits with resilience is connected to "
              f"the number it")
        print(f"           reports. The ceiling in F1a is therefore a property of the "
              f"stressor never")
        print(f"           arriving during the window in which the guard acts -- not "
              f"evidence that the")
        print(f"           mechanism is inert.")
    else:
        print(f"  [FAIL] F1b the guard has NO causal access to the reported metric.")
        print(f"           An intervention that necessarily reaches the guard's decision "
              f"left both arms at")
        print(f"           {guarded['completion']:.2%}. The mechanism the paper credits "
              f"with resilience is not")
        print(f"           connected to the outcome the paper reports, so no comparison "
              f"at any failure")
        print(f"           rate can speak to whether it works.")
        failures.append("F1b-no-causal-access")

    # --- F1c: negative control ----------------------------------------------
    print(f"  [INFO] F1c negative control: two arms identical by construction must agree:")
    a = run_arm(m, random, 0.20, guarded=True, run_cycle=True)
    b = run_arm(m, random, 0.20, guarded=True, run_cycle=True)
    c = run_arm(m, random, 0.20, guarded=False, run_cycle=False)
    d = run_arm(m, random, 0.20, guarded=False, run_cycle=False)
    if a == b and c == d:
        print(f"  [PASS] F1c identical arms agree exactly "
              f"({a['completion']:.2%} guarded, {c['completion']:.2%} unguarded)")
        print(f"           The instrument therefore reports a difference only when one "
              f"exists, and the F1b")
        print(f"           result is about the guard rather than about the harness.")
    else:
        print(f"  [FAIL] F1c identical arms disagree: {a} vs {b}, {c} vs {d}")
        print(f"         The harness is nondeterministic, so no other result in this "
              f"file can be trusted.")
        failures.append("F1c-harness-nondeterministic")

    print("=" * 78)
    if failures:
        print("FAILED: " + ", ".join(failures))
        print()
        print("The package's own comparison varies two things at once -- the completion")
        print("guard and whether run_cycle runs -- so the arm labels do not isolate a")
        print("mechanism. That confound is a finding of this row, not an artefact of the")
        print("replication.")
        return 1
    print("PASSED: the experiment has causal access to what it reports")
    return 0


if __name__ == "__main__":
    sys.exit(main())