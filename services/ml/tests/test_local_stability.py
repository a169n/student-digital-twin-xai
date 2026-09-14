import numpy as np
import pandas as pd

from src.experiments import run_local_stability as ls
from src.experiments import transfer_benchmark as tb


def _cohort(n: int = 120, seed: int = 0) -> tb.Cohort:
    rng = np.random.default_rng(seed)
    x = pd.DataFrame(rng.random((n, len(tb.CANON))) * 10, columns=list(tb.CANON))
    # A learnable signal, so the fitted model has something to attribute.
    y = (x["cum_clicks"] + rng.normal(0, 1, n) > 5).astype(int).to_numpy()
    return tb.Cohort(cohort_id="c", institution="A", module="m", X_raw=x, y=y)


def test_identical_rankings_score_perfect_agreement():
    """The metric must read 1.0 when nothing varies; anything less is a bug, not stability."""
    order = list(tb.CANON)
    assert ls._mean_pairwise_tau([order, order, order]) == 1.0
    assert ls._mean_pairwise_jaccard([order, order]) == 1.0


def test_background_never_covers_the_whole_training_set():
    """Otherwise every repeat draws the same rows and self-agreement is 1.0 by construction.

    Two small Zambia cohorts did exactly that at background=50, and reported
    perfect local stability that was an artifact of the cap, not a measurement.
    """
    rows = ls.cohort_students(_cohort(n=120), seed=0, repeats=3, background=10**6)
    train_n = int(120 * 2 / 3)
    assert rows and rows[0]["background_n"] <= train_n // 2
    assert not all(r["self_tau_shap"] == 1.0 for r in rows)


def test_cohort_too_small_for_a_background_draw_is_skipped():
    assert ls.cohort_students(_cohort(n=24), seed=0, repeats=3, background=50) == []


def test_per_student_rows_carry_gate_covariates_and_summarise():
    rows = ls.cohort_students(_cohort(n=200), seed=0, repeats=3, background=20)
    frame = pd.DataFrame(rows)
    assert frame["flagged"].mean() > 0  # the top-risk slice is non-empty
    assert (frame["margin"] >= 0).all()
    assert frame["cross_tau"].between(-1, 1).all()

    summary, gate, predictability = ls.summarise(frame)
    assert list(summary["metric"]) == list(ls.METRICS)
    assert gate["gate_pass_rate"].between(0, 1).all()
    assert list(predictability["covariate"]) == list(ls.COVARIATES)


def test_order_ranks_by_absolute_attribution():
    scores = np.zeros(len(tb.CANON))
    scores[2] = -5.0  # a strongly negative contribution is still the top factor
    scores[0] = 1.0
    assert ls._order(scores)[:2] == [tb.CANON[2], tb.CANON[0]]


def test_vary_modes_measure_different_things():
    """model-mode must not silently reduce to background-mode, or the comparison is empty."""
    kwargs = dict(seed=0, repeats=3, background=20)
    by_mode = {
        mode: pd.DataFrame(ls.cohort_students(_cohort(n=200), vary=mode, **kwargs))
        for mode in ls.VARY_MODES
    }
    assert all(set(f["vary"]) == {mode} for mode, f in by_mode.items())
    taus = {mode: f["self_tau_shap"].mean() for mode, f in by_mode.items()}
    assert taus["model"] != taus["background"]
    assert taus["both"] != taus["background"]


def test_unknown_vary_mode_is_rejected():
    import pytest

    with pytest.raises(ValueError, match="vary must be one of"):
        ls.cohort_students(_cohort(), seed=0, repeats=2, background=20, vary="everything")


def test_gate_curve_trades_coverage_for_agreement():
    frame = pd.DataFrame(
        {
            # self-agreement and cross-agreement move together here, so gating
            # on the cheap signal must visibly raise the expensive one.
            "self_tau_shap": [0.1, 0.3, 0.5, 0.7, 0.9],
            "cross_tau": [0.0, 0.2, 0.4, 0.6, 0.8],
            "cross_jaccard_top3": [0.2, 0.3, 0.4, 0.5, 0.6],
        }
    )
    curve = ls.gate_curve(frame)
    assert curve["coverage"].iloc[0] == 1.0
    assert curve["coverage"].is_monotonic_decreasing
    assert curve["mean_cross_tau"].is_monotonic_increasing
