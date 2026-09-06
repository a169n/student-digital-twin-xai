"""exp_022 — do two accepted explanation methods agree with each other on one model?

The transfer ladder shows that a model's feature ranking barely survives being
moved, and exp_018 shows the ranking is already unstable to resampling within a
single cohort. Both measure ONE estimator against itself. This experiment adds
the axis that decides how the finding should be read: given the SAME fitted
model and the SAME data, do different, equally standard importance methods even
produce the same ranking?

If they do not, the ranking is not a property of the model that transfer
degrades. It is an artifact of the estimator, and no amount of keeping the model
local makes a teacher-facing factor list trustworthy.

Three estimators, all applied to one fitted model on held-out data:

    permutation   the ladder's estimator; shuffle a column, measure AUC loss
    shap          mean |SHAP value| per feature (TreeSHAP)
    drop_column   refit without each feature and measure AUC loss. Expensive,
                  but it is what Hooker, Mentch and Zhou argue a defensible
                  variable-importance estimate requires, since permutation
                  evaluates the model off its own data manifold.

Agreement is Kendall tau and top-3 Jaccard, the same statistics the ladder uses,
so the numbers sit on one scale with exp_014 and exp_018.

Usage (from services/ml):
    uv run python -m src.experiments.run_explainer_agreement --fraction 0.33
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import numpy as np
import pandas as pd
import shap
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from src.experiments import transfer_benchmark as tb
from src.experiments.models import build_classification_model
from src.experiments.run_transfer_ladder import (
    load_ku,
    load_oulad,
    load_oviedo,
    load_ukzn,
    load_zambia,
)
from src.experiments.stability import jaccard_topk, kendall_tau

REPO = Path(__file__).resolve().parents[4]
OUT = REPO / "data" / "artifacts" / "experiments" / "exp_022_explainer_agreement"
MODEL = "gradient_boosting"
TOP_K = 3
EVAL_CAP = 1500  # matches the ladder's ranking subsample


def _order(scores: np.ndarray) -> list[str]:
    return [tb.CANON[i] for i in np.argsort(-scores)]


def rankings(X_tr, y_tr, X_ev, y_ev, seed: int) -> dict[str, list[str]]:
    model = build_classification_model(MODEL, seed=seed).fit(X_tr, y_tr)

    perm = permutation_importance(
        model, X_ev, y_ev, scoring="roc_auc", n_repeats=tb.IMPORTANCE_REPEATS, random_state=seed
    ).importances_mean

    shap_values = shap.TreeExplainer(model).shap_values(X_ev)
    if shap_values.ndim == 3:  # (n, features, classes) on some versions
        shap_values = shap_values[..., -1]
    shap_scores = np.abs(shap_values).mean(axis=0)

    # Drop-column: refit without each feature; the loss is that feature's worth.
    base = roc_auc_score(y_ev, model.predict_proba(X_ev)[:, 1])
    drop = np.empty(X_tr.shape[1])
    for j in range(X_tr.shape[1]):
        keep = [k for k in range(X_tr.shape[1]) if k != j]
        refit = build_classification_model(MODEL, seed=seed).fit(X_tr[:, keep], y_tr)
        drop[j] = base - roc_auc_score(y_ev, refit.predict_proba(X_ev[:, keep])[:, 1])

    return {"permutation": _order(perm), "shap": _order(shap_scores), "drop_column": _order(drop)}


def cohort_agreement(cohort: tb.Cohort, seed: int) -> list[dict]:
    X, y = cohort.X("raw"), cohort.y
    try:
        tr, ev = train_test_split(np.arange(len(y)), test_size=1 / 3, stratify=y, random_state=seed)
    except ValueError:
        return []
    if min(len(set(y[tr])), len(set(y[ev]))) < 2:
        return []
    if len(ev) > EVAL_CAP:
        ev = ev[:EVAL_CAP]

    ranks = rankings(X[tr], y[tr], X[ev], y[ev], seed)
    rows = []
    for a, b in itertools.combinations(sorted(ranks), 2):
        rows.append(
            {
                "cohort_id": cohort.cohort_id,
                "institution": cohort.institution,
                "n_students": cohort.n,
                "seed": seed,
                "pair": f"{a} vs {b}",
                "tau": kendall_tau(ranks[a], ranks[b]),
                "jaccard_top3": jaccard_topk(ranks[a], ranks[b], TOP_K),
            }
        )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fraction", type=float, default=0.33)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--run", default="f33")
    args = ap.parse_args()

    weekly = {**load_oulad(), **load_ku(), **load_ukzn(), **load_zambia(), **load_oviedo()}
    canon = {cid: tb.canonical_from_weekly(f) for cid, f in weekly.items()}
    cohorts = tb.make_cohorts(canon, args.fraction)
    print(f"cohorts: {len(cohorts)}", flush=True)

    rows: list[dict] = []
    for i, cohort in enumerate(cohorts, 1):
        for seed in range(args.seeds):
            rows.extend(cohort_agreement(cohort, seed))
        if i % 10 == 0:
            print(f"  {i}/{len(cohorts)} cohorts done", flush=True)

    frame = pd.DataFrame(rows)
    summary = (
        frame.groupby("pair")
        .agg(
            observations=("tau", "size"),
            tau=("tau", "mean"),
            tau_sd=("tau", "std"),
            jaccard_top3=("jaccard_top3", "mean"),
        )
        .reset_index()
    )
    by_institution = frame.groupby(["institution", "pair"])["tau"].mean().unstack().reset_index()

    tb.write_outputs(OUT / args.run, pairs=frame, summary=summary, by_institution=by_institution)
    print("\n=== agreement BETWEEN explanation methods, same model, same data ===")
    print(summary.round(3).to_string(index=False))
    print("\n=== reference points from the ladder and exp_018 ===")
    print("  same estimator, two models on disjoint halves of one cohort : tau 0.338")
    print("  transferred model vs local, another institution             : tau 0.034")
    print("  two independent random rankings                             : tau 0.000")
    print("\n=== by institution ===")
    print(by_institution.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
