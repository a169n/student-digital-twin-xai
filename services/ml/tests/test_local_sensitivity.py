import numpy as np
import pandas as pd
import pytest

from src.experiments import run_local_sensitivity as sens
from src.experiments import run_local_stability as ls
from src.experiments import transfer_benchmark as tb
from src.experiments.models import build_classification_model


def _data(n: int = 200, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Every feature carries some signal, so no attribution is zero by construction."""
    rng = np.random.default_rng(seed)
    x = rng.random((n, len(tb.CANON))) * 10
    weights = np.array([1.0, 0.5, 0.3, 0.2, 0.1, 0.05, 0.02])
    return x, ((x - 5) @ weights + rng.normal(0, 1, n) > 0).astype(int)


def _cohort(n: int = 120) -> tb.Cohort:
    x, y = _data(n)
    return tb.Cohort("c", "A", "m", pd.DataFrame(x, columns=list(tb.CANON)), y)


def test_logistic_shap_is_coef_times_centred_scaled_input():
    """Exact interventional Shapley of a linear score: w_j * (z_j - mean_bg z_j)."""
    x, y = _data()
    model = ls._build("logistic_regression", 0).fit(x[:150], y[:150])
    bg, students = x[:20], x[160:170]
    scaler, linear = model.named_steps["scaler"], model.named_steps["model"]
    expected = linear.coef_[0] * (scaler.transform(students) - scaler.transform(bg).mean(axis=0))
    np.testing.assert_allclose(ls.ESTIMATORS["shap"](model, students, bg, 0), expected, atol=1e-10)


def test_random_forest_shap_is_kernelshap_prob():
    """A forest's raw output is the probability: the two exact values must coincide."""
    x, y = _data()
    model = ls._build("random_forest", 0).fit(x[:150], y[:150])
    bg, students = x[:20], x[160:170]
    tree = ls.ESTIMATORS["shap"](model, students, bg, 0)
    kernel = ls.ESTIMATORS["kernelshap_prob"](model, students, bg, 0)
    np.testing.assert_allclose(tree, kernel, atol=1e-6)  # shap's tree walk carries float32 noise


def test_only_the_forest_loses_its_threads():
    assert ls._build("random_forest", 0).n_jobs == 1
    gbm = build_classification_model("gradient_boosting", seed=0).get_params()
    assert ls._build("gradient_boosting", 0).get_params() == gbm


def test_model_name_reaches_every_fit(monkeypatch):
    """vary="model" refits per repeat; a refit on the default family would mix models."""
    built = []
    real = ls._build
    monkeypatch.setattr(ls, "_build", lambda name, seed: built.append(name) or real(name, seed))
    rows = ls.cohort_students(
        _cohort(), seed=0, repeats=3, background=10, vary="model", model_name="logistic_regression"
    )
    assert rows and built == ["logistic_regression"] * 3


def test_auc_reads_p_risk_as_probability_of_passing():
    students = pd.DataFrame(
        {
            "cohort_id": ["a"] * 4 + ["b"] * 4,
            "y": [0, 0, 1, 1] * 2,
            "p_risk": [0.1, 0.2, 0.8, 0.9] * 2,
        }
    )
    assert sens.model_auc(students) == 1.0


def test_reference_check_holds_a_partial_run_to_its_own_cohorts(tmp_path, monkeypatch):
    ref = tmp_path / "ref.csv"
    ref.write_text("cohort_id,x\na,1\na,2\nb,3\n")
    monkeypatch.setattr(sens, "REFERENCE", ("f33_gbm", ref))
    ours = tmp_path / "ours.csv"
    ours.write_text("cohort_id,x\na,1\na,2\n")
    sens.check_reference(ours, limit_cohorts=1)
    with pytest.raises(RuntimeError):
        sens.check_reference(ours, limit_cohorts=None)  # the full run must match all of it
    ours.write_text("cohort_id,x\na,1\na,9\n")
    with pytest.raises(RuntimeError):
        sens.check_reference(ours, limit_cohorts=1)


def _row(**changes) -> dict:
    """A config on which every claim holds, with week-2-like numbers."""
    row = {
        "config": "f33_gbm",
        "fraction": 0.33,
        "model": "gradient_boosting",
        "institutions": "KU Leuven;OULAD;Oviedo;UKZN;Zambia",
        "auc_mean": 0.75,
        "strict_shap__occlusion": 0.35,
        "taub_occlusion__kernelshap_prob": 0.36,
    }
    for name, (mean, low, high) in {
        "self_shap": (0.80, 0.78, 0.82),
        "self_occlusion": (0.68, 0.66, 0.70),
        "self_lime": (0.57, 0.55, 0.59),
        "shap__occlusion": (0.36, 0.33, 0.39),
        "shap__lime": (0.40, 0.38, 0.43),
        "occlusion__lime": (0.14, 0.12, 0.16),
    }.items():
        row |= {f"taub_{name}": mean, f"taub_{name}_ci_low": low, f"taub_{name}_ci_high": high}
    for method, spread in (("occlusion", 0.345), ("lime", 0.064)):
        row |= {
            f"gate_{method}_c_star": 0.557,
            f"gate_{method}_cal_minus_global_ci_low": -0.01,
            f"gate_{method}_spread_no_gate_no_zambia": spread,
            **{f"gate_{method}_spearman_within_ci_low_{sens._slug(i)}": 0.2 for i in sens.LARGE},
        }
    return row | changes


def _holds(**changes) -> dict[str, str]:
    return {claim: rule(_row(**changes))[0] for claim, rule in sens.CRITERIA.items()}


def test_every_claim_holds_on_week_two_numbers():
    assert set(_holds().values()) == {sens.YES}


@pytest.mark.parametrize(
    ("claim", "changes"),
    [
        ("C1", {"taub_shap__lime_ci_high": 0.56}),  # above LIME's self ci_low 0.55
        ("C2", {"taub_occlusion__lime": 0.37}),  # no longer the smallest mean
        ("C2", {"taub_occlusion__lime_ci_high": 0.34}),  # overlaps shap-occlusion
        ("C3", {"strict_shap__occlusion": 0.40}),  # |0.36 - 0.40| >= 0.03
        ("C4", {"taub_occlusion__kernelshap_prob": 0.40}),
        ("C5", {"gate_lime_spearman_within_ci_low_oviedo": -0.01}),
        ("C6", {"gate_occlusion_cal_minus_global_ci_low": 0.004}),
        ("C7", {"gate_lime_spread_no_gate_no_zambia": 0.2}),  # >= 0.5 x 0.345
    ],
)
def test_each_claim_can_fail(claim, changes):
    holds = _holds(**changes)
    assert holds.pop(claim) == sens.NO
    assert set(holds.values()) == {sens.YES}  # the others are untouched


@pytest.mark.parametrize(
    ("claim", "changes"),
    [
        ("C1", {"taub_self_lime_ci_low": np.nan}),
        ("C4", {"model": "random_forest"}),  # shap already is kernelshap_prob there
        ("C5", {"gate_occlusion_spearman_within_ci_low_ukzn": np.nan}),
        ("C6", {"gate_lime_c_star": 0.04}),  # below 0.05: nothing to compare
        ("C7", {"institutions": "OULAD;Zambia"}),  # one large institution, spread 0 by construction
    ],
)
def test_claim_is_not_evaluable(claim, changes):
    assert _holds(**changes)[claim] == sens.NA


def test_c6_counts_calibration_that_hurts_as_adding_nothing():
    # exp_026's LIME result: calibrated minus global CI [-0.037, -0.006].
    assert _holds(gate_lime_cal_minus_global_ci_low=-0.037)["C6"] == sens.YES


def test_conditions_flag_weak_models_without_dropping_them():
    table = sens.conditions(pd.DataFrame([_row(), _row(config="f25_lr", auc_mean=0.59)]))
    assert len(table) == len(sens.CRITERIA) * 2
    flags = table.drop_duplicates("config").set_index("config")["model_flag"]
    assert flags.to_dict() == {"f33_gbm": "ok", "f25_lr": "weak model"}
    assert set(table["holds"]) <= {sens.YES, sens.NO, sens.NA}


def test_a_defined_failure_outranks_an_undefined_term():
    """'For every ...' rules: one evaluable failure decides NO even if another term is undefined."""
    assert sens._all_of([("a", False, ""), ("b", None, "")])[0] == sens.NO
    assert sens._all_of([("a", True, ""), ("b", None, "")])[0] == sens.NA
    assert sens._all_of([("a", True, ""), ("b", True, "")])[0] == sens.YES
