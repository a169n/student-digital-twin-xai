"""exp_026: coverage against retained cross-estimator agreement, one panel per institution.

The question the figure has to answer is whether calibrating the gate within each
cohort pulls the institutions together. The panels therefore share one y-axis:
if calibration removed the spread, the curves would end at the same height; if
the spread belongs to the institution, they stay apart whatever the regime. The
oracle curve is the ceiling any gate could reach at that coverage, and the flat
line is what no gate (or a random one) retains.

Reads one exp_026 run directory, so the figure and the operating-point table
cannot drift apart. The y-axis is the run's quality measure, named in its config.

Usage (from services/ml):
    uv run python scripts/plot_gate_calibration.py
    uv run python scripts/plot_gate_calibration.py --run <exp_026 output dir>
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "data" / "artifacts" / "experiments" / "exp_026_gate_calibration"
# Axis label per quality measure; anything unlisted falls back to its column name.
QUALITY_LABEL = {
    "cross_tau": "retained mean cross-estimator τ",
    "cross_taub_shap__occlusion": "retained mean τ-b, SHAP vs occlusion",
    "cross_taub_shap__lime": "retained mean τ-b, SHAP vs LIME",
}

PANELS = ["OULAD", "UKZN", "KU Leuven", "Oviedo", "Zambia", "ALL"]
STYLE = {
    "global": dict(color="#1f5f7a", ls="-", marker="o", ms=2.2, label="one global threshold"),
    "cohort_calibrated": dict(color="#b7791f", ls="-", label="calibrated within each cohort"),
    "oracle": dict(color="#7a3b2e", ls="--", label="oracle (ranked by cross-agreement)"),
}

plt.rcParams.update(
    {
        # fonttype 42 embeds TrueType outlines; the conference requires embedded
        # fonts and matplotlib's default Type 3 export does not provide them.
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
        "font.size": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.6,
    }
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="f33_background", help="exp_026 output directory")
    run = OUT / ap.parse_args().run
    d = pd.read_csv(run / "curves.csv")
    config = json.loads((run / "config.json").read_text())
    gate_tau, quality = config["gate_tau"], config["quality"][0]
    fig, axes = plt.subplots(2, 3, figsize=(7.4, 4.6), dpi=220, sharex=True, sharey=True)

    for ax, group in zip(axes.flat, PANELS, strict=True):
        g = d[d.group == group]
        for regime, style in STYLE.items():
            r = g[g.regime == regime].sort_values("coverage")
            ax.plot(r.coverage, r.mean_cross_tau, lw=1.0, **style)
        gate = g[(g.regime == "global") & (g.level == gate_tau)].iloc[0]
        ax.plot(gate.coverage, gate.mean_cross_tau, "o", ms=5, mfc="white", mec="#1f5f7a", mew=1.2)
        ax.axhline(g.no_gate_cross_tau.iloc[0], color="#8a8a8a", lw=0.8, ls=":")

        # Zambia is two cohorts and 40 students: plotted, but not to be read as a curve.
        note = ", 2 cohorts" if group == "Zambia" else ""
        title = "All institutions" if group == "ALL" else group
        ax.set_title(f"{title} (n = {int(g.students.iloc[0])}{note})", fontsize=9)
        ax.set_xlim(1.02, 0)
        ax.tick_params(labelsize=8)

    for ax in axes[1]:
        ax.set_xlabel("coverage (share of students shown a factor list)", fontsize=8)
    for ax in axes[:, 0]:
        ax.set_ylabel(QUALITY_LABEL.get(quality, quality), fontsize=8)

    handles = [plt.Line2D([], [], lw=1.0, **s) for s in STYLE.values()]
    handles += [
        plt.Line2D([], [], ls="", marker="o", ms=5, mfc="white", mec="#1f5f7a", mew=1.2),
        plt.Line2D([], [], color="#8a8a8a", lw=0.8, ls=":"),
    ]
    labels = [s["label"] for s in STYLE.values()]
    labels += [f"global threshold: self-agreement τ ≥ {gate_tau:.2f}", "no gate (= random gate)"]
    fig.legend(handles, labels, frameon=False, fontsize=8, loc="lower center", ncol=3)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    for ext in (".png", ".pdf"):
        fig.savefig(run / f"gate_calibration_curves{ext}", bbox_inches="tight")
    plt.close(fig)
    print("written to", run / "gate_calibration_curves.pdf")


if __name__ == "__main__":
    main()
