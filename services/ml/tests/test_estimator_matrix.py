import itertools
from math import factorial

import numpy as np
import pandas as pd
import pytest
import shap

from src.experiments import run_estimator_matrix as em
from src.experiments import run_local_stability as ls
from src.experiments import transfer_benchmark as tb
from src.experiments.models import build_classification_model
from src.experiments.stability import kendall_tau, kendall_tau_scores


def _cohort(n: int = 120, seed: int = 0) -> tb.Cohort:
    rng = np.random.default_rng(seed)
    x = pd.DataFrame(rng.random((n, len(tb.CANON))) * 10, columns=list(tb.CANON))
    y = (x["cum_clicks"] + rng.normal(0, 1, n) > 5).astype(int).to_numpy()
    return tb.Cohort(cohort_id="c", institution="A", module="m", X_raw=x, y=y)


@pytest.fixture(scope="module")
def fitted():
    cohort = _cohort()
    x = cohort.X("raw")
    model = build_classification_model(ls.MODEL, seed=0).fit(x[:80], cohort.y[:80])
    return model, x[80:84], x[:20]  # model, students to explain, background


def _exact_shapley(f, x: np.ndarray, background: np.ndarray) -> np.ndarray:
    """Interventional Shapley value by brute force over every coalition."""
    n = len(x)

    def value(coalition: tuple[int, ...]) -> float:
        z = background.copy()
        z[:, list(coalition)] = x[list(coalition)]
        return float(f(z).mean())

    phi = np.zeros(n)
    for j in range(n):
        others = [k for k in range(n) if k != j]
        for size in range(n):
            weight = factorial(size) * factorial(n - size - 1) / factorial(n)
            for s in itertools.combinations(others, size):
                phi[j] += weight * (value(s + (j,)) - value(s))
    return phi


def test_every_estimator_returns_finite_attributions(fitted):
    model, x, bg = fitted
    for name, estimator in ls.ESTIMATORS.items():
        values = estimator(model, x, bg, 0)
        assert values.shape == (len(x), len(tb.CANON)), name
        assert np.isfinite(values).all(), name


def test_lime_is_deterministic_given_model_background_and_seed(fitted):
    """Otherwise LIME's own sampling noise would leak into 'vary=background' self-agreement."""
    model, x, bg = fitted
    lime = ls.ESTIMATORS["lime"]
    assert np.array_equal(lime(model, x, bg, 0), lime(model, x, bg, 0))
    assert not np.array_equal(lime(model, x, bg, 0), lime(model, x, bg, 1))


def test_kernelshap_on_log_odds_duplicates_treeshap(fitted):
    """Why KernelSHAP is a control and not a third method: on the same output it IS TreeSHAP."""
    model, x, bg = fitted
    kernel = shap.KernelExplainer(model.decision_function, bg).shap_values(
        x, nsamples="auto", l1_reg=False, silent=True
    )
    np.testing.assert_allclose(kernel, ls._shap_matrix(model, x, bg), atol=1e-6)


def test_kernelshap_prob_is_exact_shapley_in_probability_space():
    """Every feature matters a little here, which is where shap's default l1_reg bites.

    With l1_reg="num_features(10)" rows 160 and 186 come out up to 3e-5 off:
    LARS drops a small attribution even though every coalition was enumerated.
    """
    rng = np.random.default_rng(1)
    x = rng.random((200, len(tb.CANON))) * 10
    weights = np.array([1.0, 0.5, 0.3, 0.2, 0.1, 0.05, 0.02])
    y = ((x - 5) @ weights + rng.normal(0, 1, 200) > 0).astype(int)
    model = build_classification_model(ls.MODEL, seed=0).fit(x[:150], y[:150])
    bg, students = x[:20], x[155:190]
    kernel = ls.ESTIMATORS["kernelshap_prob"](model, students, bg, 0)
    for values, student in zip(kernel, students, strict=True):
        exact = _exact_shapley(lambda z: model.predict_proba(z)[:, 1], student, bg)
        np.testing.assert_allclose(values, exact, atol=1e-10)


def test_tau_b_does_not_depend_on_feature_index_under_ties():
    """Why the tau_b columns exist: renumbering features moves the strict tau, not tau-b."""
    tied = np.array([0, 0, 0, 0, 0.2, 0.5, 1.0])  # occlusion-like: exact zeros
    untied = np.array([0.04, 0.03, 0.02, 0.01, 0.2, 0.5, 1.0])
    renumber = [3, 2, 1, 0, 4, 5, 6]
    strict = [
        kendall_tau(ls._order(a), ls._order(b))
        for a, b in ((tied, untied), (tied[renumber], untied[renumber]))
    ]
    assert strict[0] == 1.0 and strict[1] < 0.9
    assert kendall_tau_scores(tied, untied) == pytest.approx(15 / np.sqrt(15 * 21))
    assert kendall_tau_scores(tied[renumber], untied[renumber]) == kendall_tau_scores(tied, untied)
    assert kendall_tau_scores(tied * 0, untied) is None  # constant: nothing to rank


def test_default_estimators_keep_exp025_columns():
    frame = pd.DataFrame(ls.cohort_students(_cohort(), seed=0, repeats=2, background=10))
    assert list(frame.columns) == [
        "cohort_id", "institution", "n_students", "vary", "background_n", "student_row", "y",
        "p_risk", "flagged", "margin", "active_weeks", "weeks_since_active", "cum_clicks",
        "self_tau_shap", "self_tau_occlusion", "self_jaccard_shap", "cross_tau",
        "cross_jaccard_top3",
    ]  # fmt: skip


def test_other_estimator_tuples_add_generic_columns_and_lime_floor():
    kwargs = dict(seed=0, repeats=2, background=10)
    frame = pd.DataFrame(ls.cohort_students(_cohort(60), estimators=("lime", "shap"), **kwargs))
    expected = {
        "self_tau_lime",
        "self_jaccard_lime",
        "self_tau_shap",
        "self_jaccard_shap",
        "cross_tau_lime__shap",
        "cross_jaccard_top3_lime__shap",
        "lime_seed_tau",
        "self_taub_lime",
        "cross_taub_lime__shap",
        "tied_lime",
        "zeros_shap",
    }
    assert expected <= set(frame.columns)
    assert "cross_tau" not in frame and "self_tau_occlusion" not in frame
    assert frame["lime_seed_tau"].between(-1, 1).all()

    # Legacy shap-occlusion columns survive alongside the generic ones.
    three = ("shap", "occlusion", "kernelshap_prob")
    frame = pd.DataFrame(ls.cohort_students(_cohort(60), estimators=three, **kwargs))
    assert frame["cross_tau"].equals(frame["cross_tau_shap__occlusion"])
    assert {"cross_tau_shap__kernelshap_prob", "self_jaccard_occlusion"} <= set(frame.columns)
    assert "lime_seed_tau" not in frame
    # The fixture's model uses few features, so occlusion ties at zero; tau-b stays a tau.
    assert frame["tied_occlusion"].between(0, 1).all() and frame["tied_occlusion"].max() == 1
    assert frame["zeros_occlusion"].max() > 0
    assert frame["cross_taub_shap__occlusion"].dropna().between(-1, 1).all()


def test_unknown_estimator_is_rejected():
    with pytest.raises(ValueError, match="unknown estimators"):
        ls.cohort_students(_cohort(), seed=0, repeats=2, background=10, estimators=("shapp",))


def test_matrix_is_symmetric_with_self_agreement_on_the_diagonal():
    rng = np.random.default_rng(0)
    n = 30
    frame = pd.DataFrame({"cohort_id": np.repeat(["c1", "c2", "c3"], n // 3)})
    estimators = ("a", "b", "c")
    for est in estimators:
        frame[f"self_tau_{est}"] = rng.uniform(0, 1, n)
        frame[f"self_taub_{est}"] = rng.uniform(0, 1, n)
        frame[f"self_jaccard_{est}"] = rng.uniform(0, 1, n)
    for a, b in itertools.combinations(estimators, 2):
        frame[f"cross_tau_{a}__{b}"] = rng.uniform(-1, 1, n)
        frame[f"cross_taub_{a}__{b}"] = rng.uniform(-1, 1, n)
        frame[f"cross_jaccard_top3_{a}__{b}"] = rng.uniform(0, 1, n)
    frame.loc[:4, "cross_taub_a__c"] = np.nan  # undefined for a constant vector

    matrix = em.agreement_matrix(frame, estimators, n_boot=200)
    assert (matrix["tau_ci_low"] <= matrix["tau_mean"]).all()
    assert (matrix["tau_mean"] <= matrix["tau_ci_high"]).all()
    assert matrix.loc[matrix["metric"] == "tau_b", "jaccard_top3_mean"].isna().all()
    n_defined = matrix.set_index(["metric", "est_a", "est_b"])["n_students"]
    assert n_defined["tau_b", "a", "c"] == n - 5 and n_defined["tau_strict", "a", "c"] == n

    for metric, tau in (("tau_strict", "tau"), ("tau_b", "taub")):
        wide = em.square(matrix, metric).set_index("estimator")
        np.testing.assert_allclose(wide.to_numpy(), wide.to_numpy().T)
        for est in estimators:
            assert wide.loc[est, est] == pytest.approx(frame[f"self_{tau}_{est}"].mean())
        assert wide.loc["c", "a"] == pytest.approx(frame[f"cross_{tau}_a__c"].mean())


def test_runner_rejects_the_default_pair_before_computing(monkeypatch):
    """That pair writes only exp_025's legacy columns, which the matrix cannot read."""
    monkeypatch.setattr("sys.argv", ["run_estimator_matrix", "--estimators", "shap,occlusion"])
    monkeypatch.setattr(ls, "load_cohorts", lambda fraction: pytest.fail("computed anyway"))
    with pytest.raises(SystemExit):
        em.main()
