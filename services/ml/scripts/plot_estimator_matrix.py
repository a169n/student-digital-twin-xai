"""exp_027: the 3x3 local agreement matrix, background draws and model refits side by side.

Across background draws every cross-method cell sits far below both methods'
self-agreement on the diagonal; under model refits the diagonal itself falls to
the cross level. The two panels side by side are what show that.
One sequential hue on a fixed 0-1 scale, so the two panels compare by eye; each
cell prints tau-b and its cohort-cluster interval. KernelSHAP is a control (it
equals TreeSHAP up to the output space) and stays out of the figure; its numbers
are in matrix.csv and the experiment doc.

Usage (from services/ml):
    uv run python scripts/plot_estimator_matrix.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
EXP = REPO / "data" / "artifacts" / "experiments" / "exp_027_local_estimator_matrix"
RUNS = {"f33_background": "(a) background draw varies", "f33_model": "(b) model refit varies"}
ESTIMATORS = {"shap": "TreeSHAP", "occlusion": "Occlusion", "lime": "LIME"}
# One hue, light to dark: the teal the gate-calibration figure uses for its primary line.
CMAP = LinearSegmentedColormap.from_list("agreement", ["#f2f6f8", "#1f5f7a"])
INK_DARK, INK_LIGHT = "#1a1a1a", "#ffffff"

plt.rcParams.update(
    {
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
        "font.size": 8,
    }
)


def cells(run: str) -> pd.DataFrame:
    m = pd.read_csv(EXP / run / "matrix.csv")
    m = m[(m["metric"] == "tau_b") & m["est_a"].isin(ESTIMATORS) & m["est_b"].isin(ESTIMATORS)]
    return m.set_index(["est_a", "est_b"])


def draw(ax, run: str, title: str) -> plt.cm.ScalarMappable:
    m = cells(run)
    names = list(ESTIMATORS)
    grid = np.full((len(names), len(names)), np.nan)
    for i, a in enumerate(names):
        for j, b in enumerate(names[: i + 1]):
            key = (b, a) if (b, a) in m.index else (a, b)
            row = m.loc[key]
            grid[i, j] = row["tau_mean"]
            ink = INK_LIGHT if row["tau_mean"] > 0.62 else INK_DARK
            label = f"{row['tau_mean']:.2f}\n[{row['tau_ci_low']:.2f}, {row['tau_ci_high']:.2f}]"
            ax.text(j, i, label, ha="center", va="center", fontsize=7.5, color=ink)
    image = ax.imshow(grid, cmap=CMAP, vmin=0, vmax=1)
    ax.set_xticks(range(len(names)), [ESTIMATORS[n] for n in names])
    ax.set_yticks(range(len(names)), [ESTIMATORS[n] for n in names])
    ax.tick_params(length=0, labelsize=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(title, fontsize=9)
    return image


def main() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.0), dpi=220)
    for ax, (run, title) in zip(axes, RUNS.items(), strict=True):
        image = draw(ax, run, title)
    bar = fig.colorbar(image, ax=axes, fraction=0.03, pad=0.03)
    bar.set_label("Kendall τ-b between two factor lists (diagonal: method vs itself)", fontsize=7.5)
    bar.ax.tick_params(labelsize=7)
    for ext in (".png", ".pdf"):
        fig.savefig(EXP / f"estimator_matrix{ext}", bbox_inches="tight")
    plt.close(fig)
    print("written to", EXP / "estimator_matrix.pdf")


if __name__ == "__main__":
    main()
