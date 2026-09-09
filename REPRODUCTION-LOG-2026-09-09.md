# Reproduction Log — 2026-09-09

## Environment

- Isolated environment: `/tmp/research-env`
- Python: 3.14
- Core packages: NumPy, SciPy, Matplotlib, NetworkX, SymPy, Pandas, Jinja2, PyTest
- No private credentials, API keys, private datasets, or remote machines used.

## LEO Routing Package

Repository: `FernandoMay/leo-routing-itft2026-package`

Command:

```bash
python simulator/leo_routing_simulator.py
```

Outcome: completed successfully.

| Metric | Dijkstra | NSGA-II | NSGA-II + Q-learning |
|---|---:|---:|---:|
| Average latency (ms) | 24.35 | 24.17 | 25.10 |
| Delivery rate (%) | 80.00 | 74.50 | 78.00 |
| Resilience (%) | 77.83 | 77.83 | 77.83 |
| Coverage (%) | 100.00 | 100.00 | 100.00 |

Interpretation: the hybrid method does not improve every metric in the current implementation. Its defensible contribution is the multi-objective/adaptive framework, not a universal performance gain.

## XING ICCIA Package

Repository: `FernandoMay/xing-iccia2026`

Command:

```bash
python xing_simulator.py
```

Outcome: completed successfully after installing declared rendering dependencies.

| Metric | Relaxed | Constrained | Delta |
|---|---:|---:|---:|
| RAI - XING | 7.6832 | 7.2803 | -5.2% |
| GRE - XING | 0.7028 | 0.6419 | -8.7% |
| CRL - XING | 0.0448 | 0.0544 | +21.6% |
| Total quality | 7.6426 | 7.8010 | +2.1% |
| Total cost | 0.0975 | 0.1013 | +3.9% |
| Total latency | 0.8213 | 0.8550 | +4.1% |

The run used 60 trials, 15 tasks/DAG, constraint activation at trial 30, and seed 42. Raw CSV and generated figures were produced by the simulator.

## FCSTN Package

Repository: `FernandoMay/fcstn`

Command:

```bash
python -m pytest test_fcstn.py -q
```

Outcome: **15 passed, 7 failed**.

The failures are concentrated in the NDAN/BCI preprocessing path: `bci_processor.py` calls `signal.iirnotch` without importing `scipy.signal`. This repository is therefore not yet a valid source for published BCI metrics. The fix must be made and tested in the upstream repository before FCSTN results are used in a manuscript.

## Reproduction Policy

- A metric enters a paper only after the exact command completes in a clean environment.
- A failed validation run is recorded as a blocker, not hidden.
- Existing PDF claims are not treated as evidence without regenerating the underlying result.
- Hardware, human-subject, BCI, and biomedical results require separate safety, ethics, and provenance gates.
