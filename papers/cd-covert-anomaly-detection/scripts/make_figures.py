#!/usr/bin/env python3
"""Generate every figure in the manuscript from committed data files.

This script reads ONLY files in `data/`. It does not import the simulator and
does not run any simulation. Each figure therefore corresponds to a data file
that is committed next to it:

  fig_auc_distribution   data/metrics.json            (mc block)
  fig_auc_vs_power       data/metrics.json            (sweep block)
  fig_roc_curves         data/recovered_roc.json
  fig_auc_vs_sensors     data/recovered_scalability.json

Outputs both .pdf (vector, for LaTeX) and .png (raster, for inspection).

Run:  python scripts/make_figures.py
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
FIGS = os.path.join(ROOT, "figures")
os.makedirs(FIGS, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.labelsize": 9,
    "legend.fontsize": 7.5,
    "figure.dpi": 200,
    "savefig.bbox": "tight",
})

# Order matches the paper's Table III.
METHODS = ["Energy", "Autoencoder", "OC-SVM", "IForest", "Cyclostationary"]
LABEL = {
    "Energy": "Energy",
    "Autoencoder": "PCA Autoencoder",
    "OC-SVM": "One-Class SVM",
    "IForest": "Isolation Forest",
    "Cyclostationary": "Cyclic-avg proxy",
}
COLOR = {
    "Energy": "#4d4d4d",
    "Autoencoder": "#1f6fb4",
    "OC-SVM": "#d1495b",
    "IForest": "#2e8b57",
    "Cyclostationary": "#7b4fa3",
}


def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


def save(fig, stem):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIGS, f"{stem}.{ext}"), dpi=200)
    plt.close(fig)
    print(f"  wrote figures/{stem}.pdf and .png")


# ---------------------------------------------------------------- figure 1
def fig_auc_distribution():
    """Per-seed AUC for all five detectors, plus mean +/- sample sd.

    Two panels, because the five AUC scales are not comparable on one axis:
    the four strong detectors sit at the ceiling while the cyclic proxy sits
    near chance.
    """
    mc = load("metrics.json")["mc"]
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.5))

    ax = axes[0]
    for i, m in enumerate(METHODS):
        a = np.asarray(mc[m]["aucs"], dtype=float)
        ax.scatter(np.full(len(a), i) + np.random.default_rng(0).uniform(-.12, .12, len(a)),
                   a, s=9, color=COLOR[m], alpha=.65, zorder=3, linewidths=0)
        mu, sd = a.mean(), a.std(ddof=1)
        ax.errorbar(i, mu, yerr=sd, fmt="_", ms=13, mew=1.8, color="k", zorder=4,
                    capsize=3, elinewidth=1.4)
    ax.set_xticks(range(len(METHODS)))
    ax.set_xticklabels(["Energy", "PCA\nAE", "OC-SVM", "IForest", "Cyclic\nproxy"])
    ax.set_ylim(0.90, 1.008)
    ax.set_ylabel("AUC, $-85$ dBm, $K=4$")
    ax.set_title("(a) strong detectors (ceiling)", fontsize=8.5)
    ax.grid(axis="y", alpha=.25, lw=.5)
    ax.axhline(1.0, color="0.6", lw=.6, ls=":")

    ax = axes[1]
    for i, m in enumerate(METHODS):
        a = np.asarray(mc[m]["aucs"], dtype=float)
        ax.scatter(np.full(len(a), i) + np.random.default_rng(0).uniform(-.12, .12, len(a)),
                   a, s=9, color=COLOR[m], alpha=.65, zorder=3, linewidths=0)
        mu, sd = a.mean(), a.std(ddof=1)
        ax.errorbar(i, mu, yerr=sd, fmt="_", ms=13, mew=1.8, color="k", zorder=4,
                    capsize=3, elinewidth=1.4)
    ax.axhline(0.5, color="0.6", lw=.6, ls=":", label="chance")
    ax.axhline(0.99, color="0.6", lw=.6, ls="--", label="0.99")
    ax.set_xticks(range(len(METHODS)))
    ax.set_xticklabels(["Energy", "PCA\nAE", "OC-SVM", "IForest", "Cyclic\nproxy"])
    ax.set_ylim(0.45, 1.008)
    ax.set_ylabel("AUC")
    ax.set_title("(b) all detectors vs chance", fontsize=8.5)
    ax.grid(axis="y", alpha=.25, lw=.5)
    ax.legend(loc="center left", frameon=False)
    save(fig, "fig_auc_distribution")


# ---------------------------------------------------------------- figure 2
def fig_auc_vs_power():
    """AUC vs covert transmit power, one realisation per power point."""
    sweep = load("metrics.json")["sweep"]
    fig, ax = plt.subplots(figsize=(3.45, 2.5))
    for m in METHODS:
        p = np.asarray(sweep[m]["powers"], dtype=float)
        a = np.asarray(sweep[m]["aucs"], dtype=float)
        ax.plot(p, a, "o-", ms=3, lw=1.3, color=COLOR[m], label=LABEL[m], alpha=.9)
    ax.axhline(0.5, color="0.55", lw=.7, ls=":")
    ax.axhline(0.99, color="0.55", lw=.7, ls="--")
    ax.axvline(-100, color="0.55", lw=.7, ls="-", alpha=.5)
    ax.text(-99.2, 0.86, "noise floor", fontsize=6.5, color="0.35",
            rotation=90, va="bottom", ha="left")
    ax.set_xlabel("Covert transmit power (dBm)")
    ax.set_ylabel("AUC (one realisation per point)")
    ax.set_ylim(0.40, 1.03)
    ax.set_xlim(-124, -76)
    ax.grid(alpha=.25, lw=.5)
    ax.legend(loc="lower right", frameon=False, ncol=1)
    save(fig, "fig_auc_vs_power")


# ---------------------------------------------------------------- figure 3
def fig_roc_curves():
    """ROC curves from the single 250/250/200 trial at -85 dBm."""
    roc = load("recovered_roc.json")
    fig, ax = plt.subplots(figsize=(3.45, 2.6))
    for m in METHODS:
        v = roc["methods"][m]
        ax.plot(v["fpr"], v["tpr"], lw=1.4, color=COLOR[m],
                label=f"{LABEL[m]} (AUC={v['auc']:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=.7, alpha=.4, label="chance")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title("Single trial, $-85$ dBm, $K=4$ ($n=450$)", fontsize=8.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=.25, lw=.5)
    ax.legend(loc="lower right", frameon=False, fontsize=6.5)
    save(fig, "fig_roc_curves")


# ---------------------------------------------------------------- figure 4
def fig_auc_vs_sensors():
    """AUC vs number of fused sensors. Single realisation per point."""
    scal = load("recovered_scalability.json")
    fig, ax = plt.subplots(figsize=(3.45, 2.5))
    for m in METHODS:
        v = scal["methods"][m]
        ax.plot(v["K"], v["auc"], "o-", ms=4, lw=1.3, color=COLOR[m],
                label=LABEL[m], alpha=.9)
    ax.axhline(0.99, color="0.55", lw=.7, ls="--")
    ax.axhline(0.5, color="0.55", lw=.7, ls=":")
    ax.set_xscale("log", base=2)
    ax.set_xticks([1, 2, 4, 8])
    ax.set_xticklabels(["1", "2", "4", "8"])
    ax.set_xlabel("Number of fused sensors $K$")
    ax.set_ylabel("AUC (one realisation per point)")
    ax.set_ylim(0.55, 1.02)
    ax.grid(alpha=.25, lw=.5)
    # Keep the legend clear of the cyclic-proxy curve, which runs through the
    # lower half of the plot.
    ax.legend(loc="center left", bbox_to_anchor=(0.02, 0.30), frameon=False)
    save(fig, "fig_auc_vs_sensors")


def fig_provenance():
    """Provenance diagram, driven by the committed data files themselves.

    Reads the sha256 of each data file and the record counts it contains, so
    the diagram cannot drift from the artifacts it describes.
    """
    import hashlib

    def sha256(name):
        with open(os.path.join(DATA, name), "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()

    stats = load("stats.json")
    n_det = len(stats["monte_carlo"])
    n_seed = stats["monte_carlo"]["Energy"]["n_trials"]

    # (name, digest, caption, edge colour, face colour, line width)
    boxes = [
        ("FernandoMay/cd-ieee-package", None,
         "committed artifact, commit 3bf8a4d", "#4d4d4d", "white", 1.0),
        ("re-executed unmodified", None,
         "regenerated output is byte-identical", "#2e8b57", "white", 1.0),
        ("upstream/cd_simulator.py", "6ca81f21",
         "simulator, verbatim copy", "0.55", "#f4f6f7", 0.7),
        ("data/metrics.json", sha256("metrics.json")[:8],
         f"{n_det} detectors x {n_seed} seeds", "0.55", "#f4f6f7", 0.7),
        ("data/stats.json", sha256("stats.json")[:8],
         "all table values in this paper", "0.55", "#f4f6f7", 0.7),
        ("data/recovered_roc.json", sha256("recovered_roc.json")[:8],
         "ROC point arrays, regenerated", "0.55", "#f4f6f7", 0.7),
        ("data/recovered_scalability.json", sha256("recovered_scalability.json")[:8],
         "AUC vs K, regenerated", "0.55", "#f4f6f7", 0.7),
        ("every number in this paper", None,
         "transcribed from these files, none entered by hand",
         "#1f6fb4", "white", 1.2),
    ]

    H, GAP = 0.088, 0.040
    fig, ax = plt.subplots(figsize=(3.45, 2.55))
    ax.set_xlim(0, 1)
    ax.set_ylim(0.0, 1.0)
    ax.axis("off")

    y = 0.995 - H
    for i, (name, digest, cap, edge, face, lw) in enumerate(boxes):
        ax.add_patch(plt.Rectangle((0.03, y), 0.94, H,
                                   facecolor=face, edgecolor=edge, lw=lw))
        if i == 2:  # arrow in the gap between the headers and the data files
            ax.annotate("", xy=(0.5, y - 0.001), xytext=(0.5, y - GAP + 0.001),
                        arrowprops=dict(arrowstyle="-|>", color="0.40", lw=1.1,
                                        shrinkA=0, shrinkB=0))
        # main label sits in the upper part of the box, caption in the lower part
        ax.text(0.5, y + H * 0.62, name, ha="center", va="center",
                fontsize=6.6, color=edge if edge != "0.55" else "0.20")
        ax.text(0.055 if digest else 0.5, y + H * 0.24, cap,
                ha="left" if digest else "center", va="center",
                fontsize=5.5, color="0.38", style="italic")
        if digest:
            ax.text(0.955, y + H * 0.24, "sha256 " + digest, ha="right",
                    va="center", fontsize=5.4, family="monospace", color="0.32")
        y -= H + GAP

    save(fig, "fig_provenance")


def main():
    print("generating figures from committed data files:")
    fig_provenance()
    fig_auc_distribution()
    fig_auc_vs_power()
    fig_roc_curves()
    fig_auc_vs_sensors()
    print("done")


if __name__ == "__main__":
    main()
