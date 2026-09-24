import math
from fractions import Fraction

import numpy as np
import pandas as pd

from src.experiments import run_gate_calibration as gc
from src.experiments import run_local_stability as ls


def _frame(sizes=(("A", 30), ("A", 7), ("B", 100), ("B", 33)), seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    parts = []
    for k, (inst, n) in enumerate(sizes):
        # A coarse grid, as in exp_025, so ties in the gate signal actually occur.
        self_tau = rng.choice(np.linspace(0.3, 1.0, 8), n)
        parts.append(
            pd.DataFrame(
                {
                    "cohort_id": f"c{k}",
                    "institution": inst,
                    "self_tau_shap": self_tau,
                    "cross_tau": 0.5 * self_tau + rng.normal(0, 0.2, n),
                    "cross_jaccard_top3": rng.random(n),
                }
            )
        )
    return gc.prepare(pd.concat(parts, ignore_index=True))


def test_calibrated_coverage_per_cohort_is_ceil_c_n_over_n():
    d = _frame()
    for c in gc.COVERAGES:
        kept = pd.Series(gc.top_share(d, "rank_calibrated", c)).groupby(d["cohort_id"])
        for cohort, shown in kept.mean().items():
            n = int((d["cohort_id"] == cohort).sum())
            # Exact decimal arithmetic: 0.55 * 100 must keep 55, not 56.
            assert shown == math.ceil(Fraction(str(c)) * n) / n


def test_global_regime_reproduces_exp025_gate_curve():
    d = _frame()
    ours = gc.curves(d).query("regime == 'global' and group == @gc.POOLED")
    ref = ls.gate_curve(d).merge(ours, left_on="threshold", right_on="level")
    assert len(ref) == len(ls.gate_curve(d))
    assert np.allclose(ref["coverage_x"], ref["coverage_y"])
    assert np.allclose(ref["mean_cross_tau_x"], ref["mean_cross_tau_y"])


def test_oracle_bounds_calibrated_gate_at_equal_coverage():
    curve = gc.curves(_frame()).set_index(["regime", "level", "group"])
    oracle, calibrated = curve.loc["oracle"], curve.loc["cohort_calibrated"]
    assert (oracle["coverage"] == calibrated["coverage"]).all()
    assert (oracle["mean_cross_tau"] >= calibrated["mean_cross_tau"] - 1e-12).all()

    op = gc.operating_point(_frame(), c_star=0.5).set_index(["regime", "group"])
    assert np.allclose(op.loc["oracle", "efficiency"], 1.0)


def test_tie_breaking_is_deterministic():
    d = _frame().assign(self_tau_shap=0.8)  # every student tied
    first, second = (gc.top_share(gc.prepare(d), "rank_calibrated", 0.4) for _ in range(2))
    assert (first == second).all()
    assert 0 < first.sum() < len(d)


def test_lift_is_zero_at_full_coverage():
    curve = gc.curves(_frame())
    full = curve[
        ((curve["regime"] == "global") & (curve["level"] == 0.0))
        | ((curve["regime"] != "global") & (curve["level"] == 1.0))
    ]
    assert len(full) == 3 * 3  # three regimes x (A, B, pooled)
    assert np.allclose(full["coverage"], 1.0)
    assert np.allclose(full["lift"], 0.0)


def test_bootstrap_resamples_whole_cohorts():
    """One cohort holds most students: a student-level bootstrap would be narrow here."""
    d = _frame(sizes=(("A", 500), ("A", 5), ("A", 5), ("A", 5), ("A", 5)))
    d.loc[d["cohort_id"] == "c0", "cross_tau"] = 0.9
    d.loc[d["cohort_id"] != "c0", "cross_tau"] = 0.0

    draws = list(gc.cohort_resamples(d, n_boot=200, seed=0))
    for f in draws[:20]:
        sizes = f.groupby("cohort_id").size()
        assert set(sizes) <= {500, 5}  # every drawn cohort arrives whole
    means = np.array([f["cross_tau"].mean() for f in draws])
    assert np.percentile(means, 97.5) - np.percentile(means, 2.5) > 0.3


def test_spread_is_undefined_when_an_institution_shows_nobody():
    d = _frame(sizes=(("A", 30), ("B", 40), (gc.SMALL, 10)))
    d.loc[d["institution"] == gc.SMALL, "self_tau_shap"] = 0.3  # below the gate everywhere
    sp = gc.spread(gc.operating_point(gc.prepare(d), c_star=0.5))
    tau = sp.query("regime == 'global' and metric == 'mean_cross_tau'").set_index("includes_zambia")
    assert tau.loc[True, ["spread", "min_group", "max_group"]].isna().all()
    assert np.isfinite(tau.at[False, "spread"])
    coverage = sp.query("regime == 'global' and metric == 'coverage' and includes_zambia")
    assert coverage["min_group"].item() == gc.SMALL  # 0 shown is still a coverage


def test_interval_reports_how_many_replicates_it_rests_on():
    point = pd.DataFrame({"group": ["A", "B"], "x": [1.0, 2.0]})
    reps = pd.DataFrame({"group": ["A"] * 4 + ["B"] * 4, "x": [1, 2, np.nan, 3, 2, 2, 2, 2]})
    out = gc.attach_ci(point, reps, ["group"], ["x"]).set_index("group")
    assert out["x_n_boot"].to_dict() == {"A": 3, "B": 4}


def test_another_quality_column_is_what_gets_retained(tmp_path):
    """--quality must change the measured agreement, not just the directory name."""
    raw = _frame().drop(columns=["n_cohort", "rank_calibrated", "rank_oracle"])
    raw["cross_taub_shap__lime"] = 1.0 - raw["cross_tau"]  # opposite relation to the gate signal
    raw["cross_jaccard_top3_shap__lime"] = 0.25
    path = tmp_path / "students.csv"
    raw.to_csv(path, index=False)

    legacy, _ = gc.load(path)
    swapped, _ = gc.load(path, "cross_taub_shap__lime")
    at = gc.GATE_TAU
    keep = lambda d: gc.retained(d, d["self_tau_shap"].to_numpy() >= at).loc[gc.POOLED]  # noqa: E731
    assert keep(legacy)["lift"] > 0 > keep(swapped)["lift"]
    assert keep(swapped)["mean_cross_jaccard_top3"] == 0.25
    # The oracle must rank by the swapped measure too, not by the legacy one.
    assert (swapped["rank_oracle"] != legacy["rank_oracle"]).any()


def test_output_directories_cannot_collide():
    other = gc.EXPERIMENTS / "exp_027_local_estimator_matrix"
    names = {
        gc.output_name(gc.SRC, "f33_background", gc.DEFAULT_QUALITY),
        gc.output_name(gc.SRC, "f33_background", "cross_taub_shap__lime"),
        gc.output_name(other, "f33_background", gc.DEFAULT_QUALITY),
        gc.output_name(other, "f33_background", "cross_taub_shap__lime"),
    }
    assert len(names) == 4
    assert gc.output_name(gc.SRC, "f33_background", gc.DEFAULT_QUALITY) == "f33_background"
