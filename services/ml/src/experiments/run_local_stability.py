"""exp_025 — is ONE student's factor list reproducible?

exp_022 asked whether two accepted estimators agree on a cohort's global feature
ranking (tau 0.41 permutation vs shap; self-agreement 0.59 for shap, 0.34 for
permutation). Those are cohort-level numbers. The teacher-facing screen shows a
LOCAL attribution: why THIS student is flagged. Nothing in the global result
transfers to it — a local attribution has no averaging over a heterogeneous
cohort to smooth it, and no reason to be noisier either. It has to be measured.

Two local estimators on one fitted model, per student:

    shap        TreeSHAP with an interventional background sample
    occlusion   set feature j to the background median, measure the change in p

Both depend on a background draw, and that dependency is the reference point
this experiment is built around: before asking whether two methods agree on a
student, ask what ONE method gives when nothing changes but the background
sample. TreeSHAP variance shrinks as the background grows, so a bare "local
explanations are unstable" claim is partly a configuration artifact. The
background size is therefore a reported parameter, not a hidden default.

Outputs, per student: self-agreement of each estimator across background draws,
cross-estimator agreement, and the covariates a confidence gate could key on
(distance to the flag threshold, length of active history).

The estimators are pluggable (ESTIMATORS) so exp_027 can ask whether the
shap-occlusion agreement is a property of that one pair. The default pair and
its output columns are exp_025's, unchanged.

Usage (from services/ml):
    uv run python -m src.experiments.run_local_stability --fraction 0.33
"""

from __future__ import annotations

import argparse
import itertools
from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd
import shap
from lime.lime_tabular import LimeTabularExplainer
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
from src.experiments.stability import jaccard_topk, kendall_tau, kendall_tau_scores

REPO = Path(__file__).resolve().parents[4]
OUT = REPO / "data" / "artifacts" / "experiments" / "exp_025_local_stability"
MODEL = "gradient_boosting"
TOP_K = 3
# Smaller than exp_022's 1500: every student here costs `repeats` background
# draws of interventional TreeSHAP, and the per-student statistics converge long
# before the cohort is exhausted.
EVAL_CAP = 400
GATE_TAU = 0.80  # "this factor list reproduces itself" threshold used by the gate
MIN_BACKGROUND = 10  # below this a background draw is too thin to attribute against
VARY_MODES: tuple[str, ...] = ("background", "model", "both")


def _order(scores: np.ndarray) -> list[str]:
    """Feature names for one student, most important first, by |attribution|."""
    return [tb.CANON[i] for i in np.argsort(-np.abs(scores))]


def _shap_matrix(model, x_eval: np.ndarray, background: np.ndarray) -> np.ndarray:
    values = shap.TreeExplainer(
        model, data=background, feature_perturbation="interventional"
    ).shap_values(x_eval, check_additivity=False)
    values = np.asarray(values)
    if values.ndim == 3:  # (n, features, classes) on some shap versions
        values = values[..., -1]
    return values


def _occlusion_matrix(model, x_eval: np.ndarray, background: np.ndarray) -> np.ndarray:
    """Local one-at-a-time perturbation to the background median.

    Deterministic given the background, exactly as TreeSHAP is, so both
    estimators are exposed to the same source of variation and their
    self-agreement numbers sit on one scale.
    """
    baseline = np.median(background, axis=0)
    base_p = model.predict_proba(x_eval)[:, 1]
    out = np.empty_like(x_eval, dtype=float)
    for j in range(x_eval.shape[1]):
        perturbed = x_eval.copy()
        perturbed[:, j] = baseline[j]
        out[:, j] = base_p - model.predict_proba(perturbed)[:, 1]
    return out


def _lime_matrix(model, x_eval: np.ndarray, background: np.ndarray, seed: int) -> np.ndarray:
    """LIME with library defaults: a local linear surrogate on quartile-discretised samples.

    Unlike TreeSHAP and occlusion, LIME has randomness of its own (the 5000
    perturbation samples per student). Its random_state is the same fixed value
    in every repeat, so that — on the principle stated in _occlusion_matrix — it
    is deterministic given (model, background) and only the declared source of
    variation moves. Its own sampling noise is measured apart (lime_seed_tau).
    """
    explainer = LimeTabularExplainer(
        background, feature_names=list(tb.CANON), mode="classification", random_state=seed
    )
    out = np.zeros_like(x_eval, dtype=float)
    for i, x in enumerate(x_eval):
        explanation = explainer.explain_instance(
            x, model.predict_proba, labels=(1,), num_features=len(tb.CANON)
        )
        for j, weight in explanation.as_map()[1]:
            out[i, j] = weight
    return out


def _kernelshap_prob_matrix(model, x_eval: np.ndarray, background: np.ndarray) -> np.ndarray:
    """Exact interventional Shapley values of the predicted probability — a control.

    With 7 features nsamples="auto" enumerates all 2^7 - 2 coalitions, so this
    is not an approximation. On the log-odds it would reproduce "shap" and add
    nothing; on the probability it differs from "shap" only by the output space.
    It is therefore not a third method: it isolates how much of the
    shap-occlusion disagreement is the link function, since occlusion works in
    probability space.

    l1_reg=False because shap's default ("num_features(10)") still runs a LARS
    feature selection under full enumeration, and it can drop a feature with a
    small but nonzero value — which then reads as an exact zero, and as a tie.
    """
    explainer = shap.KernelExplainer(lambda z: model.predict_proba(z)[:, 1], background)
    return np.asarray(explainer.shap_values(x_eval, nsamples="auto", l1_reg=False, silent=True))


# name -> (model, x_eval, background, seed) -> (n_students, n_features) attributions.
# Only LIME consumes the seed; the others are deterministic given model and background.
ESTIMATORS: dict[str, Callable[..., np.ndarray]] = {
    "shap": lambda model, x, bg, seed: _shap_matrix(model, x, bg),
    "occlusion": lambda model, x, bg, seed: _occlusion_matrix(model, x, bg),
    "lime": _lime_matrix,
    "kernelshap_prob": lambda model, x, bg, seed: _kernelshap_prob_matrix(model, x, bg),
}
DEFAULT_ESTIMATORS: tuple[str, ...] = ("shap", "occlusion")  # exp_025's pair


def _mean_pairwise_tau(orders: list[list[str]]) -> float | None:
    taus = []
    for a, b in itertools.combinations(range(len(orders)), 2):
        tau = kendall_tau(orders[a], orders[b])
        if tau is not None:
            taus.append(tau)
    return float(np.mean(taus)) if taus else None


def _mean_pairwise_jaccard(orders: list[list[str]]) -> float | None:
    pairs = list(itertools.combinations(range(len(orders)), 2))
    if not pairs:
        return None
    return float(np.mean([jaccard_topk(orders[a], orders[b], TOP_K) for a, b in pairs]))


def _mean_cross(orders_a: list[list[str]], orders_b: list[list[str]]) -> tuple[float | None, float]:
    """Two estimators compared on the same repeat, averaged over repeats: (tau, top-k Jaccard)."""
    taus = [t for t in map(kendall_tau, orders_a, orders_b) if t is not None]
    jaccard = [jaccard_topk(a, b, TOP_K) for a, b in zip(orders_a, orders_b, strict=True)]
    return (float(np.mean(taus)) if taus else None), float(np.mean(jaccard))


def _mean_defined(values) -> float | None:
    defined = [v for v in values if v is not None]
    return float(np.mean(defined)) if defined else None


def cohort_students(
    cohort: tb.Cohort,
    *,
    seed: int,
    repeats: int,
    background: int,
    vary: str = "background",
    estimators: tuple[str, ...] = DEFAULT_ESTIMATORS,
) -> list[dict]:
    """Per-student stability under one source of variation.

    ``vary`` decides what is allowed to move between repeats, and it is the
    axis that makes these numbers comparable to exp_022's cohort-level ones:

        background  the deployed model is fixed, only the background draw moves.
                    This is the operational question: the screen shows one
                    model, and the teacher should not see a different factor
                    list on a page reload.
        model       the background is fixed, the model is refit on a bootstrap
                    of its own training set. exp_022's 0.592 varies the model
                    this way, so only this mode sits on the same scale.
        both        both move. The loosest reading, and the closest thing to
                    "would a different team building the same system have
                    shown this student the same reasons".

    The evaluation split never moves, in any mode — the students have to be the
    same ones across repeats for a per-student statistic to mean anything.

    ``estimators`` other than exp_025's default pair add self_tau_<e> /
    self_jaccard_<e> per estimator and cross_tau_<a>__<b> /
    cross_jaccard_top3_<a>__<b> per pair; the legacy shap-occlusion columns stay
    whenever both are present. With "lime", lime_seed_tau is LIME's noise floor:
    repeat 0 against a rerun on the same model and background with seed + 1.

    Those tau columns compare factor LISTS, so exact ties in |attribution| —
    common for occlusion, whose perturbation often crosses no split — are
    broken by feature index. Each also gets a tie-aware twin on the |attribution|
    vectors (self_taub_<e>, cross_taub_<a>__<b>; a repeat with a constant vector
    is skipped), plus tied_<e> (share of repeats with any exact tie) and
    zeros_<e> (mean exact zeros per repeat) to show how much there is to fix.
    """
    if vary not in VARY_MODES:
        raise ValueError(f"vary must be one of {VARY_MODES}, got {vary!r}")
    unknown = [e for e in estimators if e not in ESTIMATORS]
    if unknown:
        raise ValueError(f"unknown estimators {unknown}; known: {tuple(ESTIMATORS)}")
    x_all, y = cohort.X("raw"), cohort.y
    try:
        train, evaluate = train_test_split(
            np.arange(len(y)), test_size=1 / 3, stratify=y, random_state=seed
        )
    except ValueError:
        return []
    if min(len(set(y[train])), len(set(y[evaluate]))) < 2:
        return []
    if len(evaluate) > EVAL_CAP:
        evaluate = evaluate[:EVAL_CAP]

    x_train, x_eval = x_all[train], x_all[evaluate]
    model = build_classification_model(MODEL, seed=seed).fit(x_train, y[train])

    # The flagged set is meant to be the riskiest FLAG_RATE of the cohort; a
    # student's distance to that cut is the first thing a gate would key on.
    # TODO(ml): y is `passed`, so this is P(pass) and `flagged` marks the 20 %
    # LEAST at risk; `p_risk` and `margin` inherit the inversion (exp_025 and
    # exp_027 students.csv). No agreement number uses them. Fix with
    # 1 - predict_proba[:, 1] under a new experiment id, not in place.
    risk = model.predict_proba(x_eval)[:, 1]
    threshold = float(np.quantile(risk, 1 - tb.FLAG_RATE))

    # Half the training set at most. A background draw that covers the whole
    # training set is identical every repeat, so the cohort reports perfect
    # self-agreement by construction rather than by measurement — that is what
    # the two small Zambia cohorts did at background=50 before this cap.
    bg_size = min(background, len(x_train) // 2)
    if bg_size < MIN_BACKGROUND:
        return []

    fixed_bg = x_train[
        np.random.default_rng(seed * 1000).choice(len(x_train), size=bg_size, replace=False)
    ]
    per_repeat: dict[str, list[np.ndarray]] = {est: [] for est in estimators}
    for repeat in range(repeats):
        rng = np.random.default_rng(seed * 1000 + repeat)
        if vary == "model":
            bg = fixed_bg
        else:
            bg = x_train[rng.choice(len(x_train), size=bg_size, replace=False)]

        if vary == "background" or repeat == 0:
            fitted = model
        else:
            # Bootstrap the training rows rather than reseeding the estimator:
            # GradientBoostingClassifier at subsample=1.0 is deterministic, so
            # random_state alone would vary nothing at all.
            boot = rng.choice(len(x_train), size=len(x_train), replace=True)
            if len(set(y[train][boot])) < 2:
                boot = np.arange(len(x_train))
            fitted = build_classification_model(MODEL, seed=seed).fit(
                x_train[boot], y[train][boot]
            )

        if repeat == 0:
            first_model, first_bg = fitted, bg
        for est in estimators:
            per_repeat[est].append(ESTIMATORS[est](fitted, x_eval, bg, seed))

    lime_floor = (
        ESTIMATORS["lime"](first_model, x_eval, first_bg, seed + 1)
        if "lime" in estimators
        else None
    )

    feature_idx = {name: i for i, name in enumerate(tb.CANON)}
    rows: list[dict] = []
    for i in range(len(evaluate)):
        orders = {
            est: [_order(mats[r][i]) for r in range(repeats)] for est, mats in per_repeat.items()
        }
        row = {
            "cohort_id": cohort.cohort_id,
            "institution": cohort.institution,
            "n_students": cohort.n,
            "vary": vary,
            "background_n": bg_size,  # the estimator's variance depends on it; report it
            "student_row": int(evaluate[i]),
            "y": int(y[evaluate[i]]),
            "p_risk": float(risk[i]),
            "flagged": bool(risk[i] >= threshold),
            "margin": float(abs(risk[i] - threshold)),
            "active_weeks": float(x_eval[i, feature_idx["active_weeks"]]),
            "weeks_since_active": float(x_eval[i, feature_idx["weeks_since_active"]]),
            "cum_clicks": float(x_eval[i, feature_idx["cum_clicks"]]),
        }
        if "shap" in estimators and "occlusion" in estimators:
            cross_tau, cross_jaccard = _mean_cross(orders["shap"], orders["occlusion"])
            row.update(
                self_tau_shap=_mean_pairwise_tau(orders["shap"]),
                self_tau_occlusion=_mean_pairwise_tau(orders["occlusion"]),
                self_jaccard_shap=_mean_pairwise_jaccard(orders["shap"]),
                cross_tau=cross_tau,
                cross_jaccard_top3=cross_jaccard,
            )
        if tuple(estimators) != DEFAULT_ESTIMATORS:
            mag = {est: [np.abs(m[i]) for m in mats] for est, mats in per_repeat.items()}
            for est in estimators:
                row[f"self_tau_{est}"] = _mean_pairwise_tau(orders[est])
                row[f"self_jaccard_{est}"] = _mean_pairwise_jaccard(orders[est])
                row[f"self_taub_{est}"] = _mean_defined(
                    kendall_tau_scores(u, v) for u, v in itertools.combinations(mag[est], 2)
                )
                row[f"tied_{est}"] = float(np.mean([len(np.unique(v)) < len(v) for v in mag[est]]))
                row[f"zeros_{est}"] = float(np.mean([np.count_nonzero(v == 0) for v in mag[est]]))
            for a, b in itertools.combinations(estimators, 2):
                pair = f"{a}__{b}"
                row[f"cross_tau_{pair}"], row[f"cross_jaccard_top3_{pair}"] = _mean_cross(
                    orders[a], orders[b]
                )
                row[f"cross_taub_{pair}"] = _mean_defined(map(kendall_tau_scores, mag[a], mag[b]))
        if lime_floor is not None:
            row["lime_seed_tau"] = kendall_tau(orders["lime"][0], _order(lime_floor[i]))
        rows.append(row)
    return rows


METRICS = ("self_tau_shap", "self_tau_occlusion", "cross_tau", "cross_jaccard_top3")
COVARIATES = ("margin", "p_risk", "active_weeks", "weeks_since_active", "cum_clicks")


def summarise(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary = pd.DataFrame(
        {
            "metric": list(METRICS),
            "students": [int(frame[m].notna().sum()) for m in METRICS],
            "mean": [float(frame[m].mean()) for m in METRICS],
            "sd": [float(frame[m].std()) for m in METRICS],
            "p10": [float(frame[m].quantile(0.10)) for m in METRICS],
            "median": [float(frame[m].median()) for m in METRICS],
        }
    )
    gate = (
        frame.assign(gated=frame["self_tau_shap"] >= GATE_TAU)
        .groupby("institution")
        .agg(
            students=("gated", "size"),
            gate_pass_rate=("gated", "mean"),
            mean_self_tau_shap=("self_tau_shap", "mean"),
            mean_cross_tau=("cross_tau", "mean"),
        )
        .reset_index()
    )
    # Can the gate be predicted from what the screen already knows about the
    # student? Spearman, because none of these are linearly related.
    predictability = pd.DataFrame(
        {
            "covariate": list(COVARIATES),
            "spearman_vs_self_tau_shap": [
                float(frame[[c, "self_tau_shap"]].corr(method="spearman").iloc[0, 1])
                for c in COVARIATES
            ],
            "spearman_vs_cross_tau": [
                float(frame[[c, "cross_tau"]].corr(method="spearman").iloc[0, 1])
                for c in COVARIATES
            ],
        }
    )
    return summary, gate, predictability


def gate_curve(frame: pd.DataFrame, *, column: str = "self_tau_shap") -> pd.DataFrame:
    """Coverage vs quality of what survives a confidence gate.

    A fixed GATE_TAU is arbitrary — it passes 59% of students in one condition
    and 0.1% in another. What a deployment actually needs is the trade-off
    curve: at each threshold, how many students still get a factor list, and is
    the list they get any better. "Better" here is cross-estimator agreement,
    because that is the part a gate cannot fix by construction — an explanation
    that reproduces itself but that a second accepted method contradicts is
    reproducibly wrong, not trustworthy.

    The gate is only worth building if retained cross-agreement rises as
    coverage falls. If the curve is flat, the cheap signal carries no
    information about the expensive one and the honest move is to say so.
    """
    rows = []
    for threshold in np.round(np.arange(0.0, 1.0, 0.05), 2):
        kept = frame.loc[frame[column] >= threshold]
        if kept.empty:
            break
        rows.append(
            {
                "threshold": float(threshold),
                "coverage": float(len(kept) / len(frame)),
                "students_shown": int(len(kept)),
                "mean_cross_tau": float(kept["cross_tau"].mean()),
                "mean_cross_jaccard_top3": float(kept["cross_jaccard_top3"].mean()),
            }
        )
    return pd.DataFrame(rows)


def load_cohorts(fraction: float) -> list[tb.Cohort]:
    """All 63 benchmark cohorts of the five institutions, cut at ``fraction`` of the course."""
    weekly = {**load_oulad(), **load_ku(), **load_ukzn(), **load_zambia(), **load_oviedo()}
    canon = {cid: tb.canonical_from_weekly(f) for cid, f in weekly.items()}
    return tb.make_cohorts(canon, fraction)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fraction", type=float, default=0.33)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--repeats", type=int, default=5, help="draws per estimator")
    ap.add_argument("--background", type=int, default=50, help="rows per background sample")
    ap.add_argument("--vary", choices=VARY_MODES, default="background", help="what moves per draw")
    ap.add_argument("--run", default=None, help="output subfolder; defaults to f<pct>_<vary>")
    args = ap.parse_args()
    # The run name carries the vary mode so the three conditions cannot silently
    # overwrite each other, which the registry's lifecycle rules forbid.
    run = args.run or f"f{int(round(args.fraction * 100))}_{args.vary}"

    cohorts = load_cohorts(args.fraction)
    print(f"cohorts: {len(cohorts)}", flush=True)

    rows: list[dict] = []
    for i, cohort in enumerate(cohorts, 1):
        rows.extend(
            cohort_students(
                cohort,
                seed=args.seed,
                repeats=args.repeats,
                background=args.background,
                vary=args.vary,
            )
        )
        if i % 10 == 0:
            print(f"  {i}/{len(cohorts)} cohorts done ({len(rows)} students)", flush=True)

    frame = pd.DataFrame(rows)
    summary, gate, predictability = summarise(frame)
    tb.write_outputs(
        OUT / run,
        students=frame,
        summary=summary,
        gate_by_institution=gate,
        gate_curve=gate_curve(frame),
        predictability=predictability,
    )
    tb.dump_json(
        OUT / run / "config.json",
        {
            "model": MODEL,
            "vary": args.vary,
            "fraction": args.fraction,
            "seed": args.seed,
            "repeats": args.repeats,
            "background_size": args.background,
            "eval_cap": EVAL_CAP,
            "top_k": TOP_K,
            "gate_tau": GATE_TAU,
            "flag_rate": tb.FLAG_RATE,
        },
    )

    print("\n=== per-student explanation stability ===")
    print(summary.round(3).to_string(index=False))
    print("\n=== reference points ===")
    print("  same estimator, cohort-level, across seeds (exp_022 shap) : tau 0.592")
    print("  two estimators, cohort-level, same model   (exp_022)      : tau 0.410")
    print("  two independent random rankings                           : tau 0.000")
    print(f"\n=== gate at self_tau_shap >= {GATE_TAU} ===")
    print(gate.round(3).to_string(index=False))
    print("\n=== is the gate predictable from what the screen already shows? ===")
    print(predictability.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
