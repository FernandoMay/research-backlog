#!/usr/bin/env python3
"""Recover the two result series that the upstream package computed but never persisted.

Upstream `cd_simulator.py` discards the AUC-vs-K series in
`plot_sensor_scalability()` and the raw ROC point arrays in
`plot_roc_curves()`. Both are recomputed here using the *verbatim* upstream
module in `upstream/cd_simulator.py` and the *exact* call signatures used by
upstream `main()`, so the recovered numbers are the numbers the committed
figures were drawn from.

Nothing here is an estimate. Every value written to `data/` is computed by
committed upstream code at the committed call sites.

Outputs
-------
data/recovered_roc.json          ROC point arrays for Figure ROC (n=250/250/200,
                                 seed 42) - the configuration upstream
                                 `main()` passes to `plot_roc_curves()`.
data/recovered_scalability.json  AUC vs K (n=80/80/60, covert power -85 dBm),
                                 reproducing upstream's single shared
                                 `env_base` chain across 5 methods x 4 K.

Run:  python scripts/recover.py
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "upstream"))

import cd_simulator as S  # noqa: E402  (verbatim upstream module)

DATA = os.path.join(ROOT, "data")


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def recover_roc():
    """Upstream main(): env=SEED, n_train=250, 250 normal, 200 covert, -85 dBm."""
    env = S.SpectrumEnvironment(seed=S.SEED)
    res = S.run_all_methods(env, n_train=250, n_test_normal=250,
                            n_test_covert=200, covert_power_db=-85)
    return {
        "description": "Single-trial ROC at covert power -85 dBm, K=4, seed 42. "
                       "Reproduces the legend values of upstream fig_roc_curves.",
        "config": {"seed": S.SEED, "n_train": 250, "n_test_normal": 250,
                   "n_test_covert": 200, "n_sensors": 4, "covert_power_db": -85},
        "methods": {
            m: {"auc": res[m]["auc"], "best_pd": res[m]["best_pd"],
                "best_pfa": res[m]["best_pfa"],
                "fpr": res[m]["fpr"], "tpr": res[m]["tpr"]}
            for m in S.METHODS
        },
    }


def recover_scalability():
    """Upstream plot_sensor_scalability(): one shared env_base, n=80/80/60."""
    n_list = [1, 2, 4, 8]
    env_base = S.SpectrumEnvironment(seed=S.SEED)
    out = {}
    for method in S.METHODS:
        aucs = []
        for n in n_list:
            r = S.run_all_methods(env_base, n_train=80, n_test_normal=80,
                                  n_test_covert=60, covert_power_db=-85,
                                  n_sensors=n)
            aucs.append(r[method]["auc"])
        out[method] = {"K": n_list, "auc": aucs}
    return {
        "description": "AUC vs number of sensors, covert power -85 dBm. "
                       "Single realisation per (method, K): upstream reuses one "
                       "env_base across the whole sweep, so each point is a "
                       "different dataset and points are NOT nested or paired.",
        "config": {"seed": S.SEED, "n_train": 80, "n_test_normal": 80,
                   "n_test_covert": 60, "covert_power_db": -85, "K": n_list},
        "methods": out,
    }


def main():
    upstream = os.path.join(ROOT, "upstream", "cd_simulator.py")
    print("upstream cd_simulator.py sha256:", sha256(upstream))
    print("data/metrics.json          sha256:",
          sha256(os.path.join(DATA, "metrics.json")))

    print("\n[1/2] recovering ROC point arrays (n=250/250/200)...")
    roc = recover_roc()
    for m, v in roc["methods"].items():
        print(f"   {m:<16} AUC={v['auc']:.6f}")
    with open(os.path.join(DATA, "recovered_roc.json"), "w") as fh:
        json.dump(roc, fh, indent=1)

    print("\n[2/2] recovering AUC vs K (n=80/80/60)...")
    scal = recover_scalability()
    for m, v in scal["methods"].items():
        pairs = "  ".join(f"K={k}:{a:.4f}" for k, a in zip(v["K"], v["auc"]))
        print(f"   {m:<16} {pairs}")
    with open(os.path.join(DATA, "recovered_scalability.json"), "w") as fh:
        json.dump(scal, fh, indent=1)

    print("\nwrote data/recovered_roc.json, data/recovered_scalability.json")


if __name__ == "__main__":
    main()
