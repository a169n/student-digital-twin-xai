"""Figure 1 for the explanation-instability paper: every comparison on one scale.

The paper's argument is an ordering, so the figure has to put all of it on a
single axis: the noise floor, the two ceilings, the three explainer pairs, the
three transfer rungs, and the random baseline. A reader should be able to see in
one glance that switching the explanation method lands below switching the
training cohort.

Usage (from services/ml):
    uv run python scripts/plot_explanation_instability.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
ART = REPO / "data" / "artifacts" / "experiments"
FIG = REPO / "docs" / "dissertation" / "figures" / "side2026"

# Colour encodes WHAT was changed, which is the paper's independent variable.
FAMILY = {
    "reference": "#8a8a8a",
    "explainer": "#b7791f",
    "sample": "#1f5f7a",
    "institution": "#7a3b2e",
}
LABEL = {
    "reference": "reference point",
    "explainer": "explanation method changed",
    "sample": "training sample changed",
    "institution": "institution changed",
}

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 8.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.6,
    }
)


def collect() -> pd.DataFrame:
    ceiling = pd.read_csv(ART / "exp_018_explanation_ceiling" / "f33" / "summary.csv").set_index("reference")
    explainer = pd.read_csv(ART / "exp_022_explainer_agreement" / "f33" / "summary.csv").set_index("pair")
    pairs = pd.read_csv(ART / "exp_014_transfer_ladder" / "f33" / "pairs.csv")
    overlap = pd.read_csv(ART / "exp_017_contamination" / "f33" / "pair_overlap.csv")
    gbm = pairs[(pairs.model == "gradient_boosting") & (pairs.representation == "raw")].merge(
        overlap[["source", "target", "is_clean"]], on=["source", "target"], how="left"
    )
    gbm["is_clean"] = gbm["is_clean"].astype("object").fillna(True).astype(bool)
    clean = gbm[gbm.is_clean]

    def rung(distance: str) -> float:
        return float(clean.loc[clean.distance == distance, "explanation_tau"].mean())

    rows = [
        ("Same model, only the random seed differs", ceiling.loc["floor (same model, reseeded)", "tau"], "reference"),
        ("Two models, halves of one cohort", ceiling.loc["ceiling, ladder-matched evaluation set", "tau"], "sample"),
        ("Permutation vs SHAP", explainer.loc["permutation vs shap", "tau"], "explainer"),
        ("Permutation vs drop-column", explainer.loc["drop_column vs permutation", "tau"], "explainer"),
        ("Same course, next year's students", rung("D1_same_module"), "sample"),
        ("SHAP vs drop-column", explainer.loc["drop_column vs shap", "tau"], "explainer"),
        ("Another course, same institution", rung("D2_other_module"), "institution"),
        ("Another institution", rung("D3_other_institution"), "institution"),
        ("Two independent random rankings", 0.0, "reference"),
    ]
    return pd.DataFrame(rows, columns=["label", "tau", "family"]).sort_values("tau", ascending=True)


def main() -> None:
    d = collect()
    FIG.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.6, 3.4), dpi=220)

    ys = np.arange(len(d))
    ax.barh(ys, d["tau"], height=0.62, color=[FAMILY[f] for f in d["family"]])
    for y, (tau, family) in enumerate(zip(d["tau"], d["family"])):
        ax.text(tau + 0.012, y, f"{tau:.3f}", va="center", fontsize=8, color=FAMILY[family])

    ax.set_yticks(ys)
    ax.set_yticklabels(d["label"], fontsize=8)
    ax.set_xlabel("agreement between the two feature rankings (Kendall tau)", fontsize=8.5)
    ax.set_xlim(0, 0.82)
    ax.axvline(0.0, color="#c8c8c8", lw=0.8)

    handles = [plt.Rectangle((0, 0), 1, 1, color=FAMILY[k]) for k in ("explainer", "sample", "institution", "reference")]
    ax.legend(
        handles,
        [LABEL[k] for k in ("explainer", "sample", "institution", "reference")],
        frameon=False,
        fontsize=7.5,
        loc="lower right",
    )
    fig.tight_layout()
    for ext in (".png", ".svg"):
        fig.savefig(FIG / f"fig1_explanation_instability{ext}", bbox_inches="tight")
    plt.close(fig)
    print(d.to_string(index=False))
    print("\nwritten to", FIG / "fig1_explanation_instability.png")


if __name__ == "__main__":
    main()
