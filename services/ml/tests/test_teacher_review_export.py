import numpy as np
import pandas as pd

from src.experiments import transfer_benchmark as tb
from src.export import export_teacher_review_payload as ex


def _cohort(n: int = 240, seed: int = 0) -> tb.Cohort:
    rng = np.random.default_rng(seed)
    x = pd.DataFrame(rng.random((n, len(tb.CANON))) * 10, columns=list(tb.CANON))
    # Passing rises with activity, so risk must fall with it.
    y = (x["cum_active_days"] + rng.normal(0, 1, n) > 5).astype(int).to_numpy()
    return tb.Cohort(cohort_id="oulad_AAA_2013J", institution="OULAD", module="AAA", X_raw=x, y=y)


def test_risk_is_probability_of_not_passing():
    frame = ex.cohort_explanations(_cohort())
    assert frame["risk"].between(0, 1).all()
    by_outcome = frame.groupby("y")["risk"].mean()
    assert by_outcome[0] > by_outcome[1]  # non-passers carry more risk
    assert frame["flagged"].mean() > 0
    flagged_min = frame.loc[frame["flagged"], "risk"].min()
    assert (frame.loc[~frame["flagged"], "risk"] <= flagged_min).all()


def test_self_tau_matches_the_run_local_stability_definition():
    frame = ex.cohort_explanations(_cohort())
    assert frame["self_tau"].between(-1, 1).all()
    assert len(frame["top_by_repeat"].iloc[0]) == ex.REPEATS


def _row(attribution):
    return pd.Series(
        {
            "institution": "OULAD",
            "cohort_id": "c1",
            "student_row": 7,
            "course": "AAA",
            "week": 13,
            "n_weeks": 39,
            "cohort_size": 240,
            "pass_rate": 0.5,
            "model_auc": 0.8,
            "risk": 0.72,
            "risk_rank_pct": 0.9,
            "risk_below_pct": 0.85,
            "risk_tied_pct": 0.1,
            "ranked_students": 128,
            "flagged": True,
            "self_tau": 0.62,
            "attribution": list(attribution),
            "top_by_repeat": ["cum_active_days"] * 3 + ["cum_clicks"] * 2,
            "value": [float(v) for v in range(7)],
            "course_median": [1.0] * 7,
        }
    )


def test_direction_follows_the_sign_towards_passing():
    case = ex.build_case(_row([0.5, -2.0, 0.0, 0.1, 0.0, 0.0, 0.0]), "OU-1")
    names = [f["feature"] for f in case["factors"]]
    assert names == ["cum_active_days", "cum_clicks", "cum_social"]
    assert case["factors"][0]["direction"] == "raises_risk"  # negative towards passing
    assert case["factors"][1]["direction"] == "lowers_risk"


def test_zero_attribution_is_no_effect_not_lowers_risk():
    case = ex.build_case(_row([3.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0]), "OU-1")
    assert case["factors"][2]["direction"] == "no_effect"


def test_shares_sum_to_one_over_all_seven_features():
    shares = ex._shares(np.array([0.5, -2.0, 0.0, 0.1, 0.4, -0.3, 0.2]))
    assert abs(shares.sum() - 1.0) < 1e-12


def test_reliability_and_recomputations():
    case = ex.build_case(_row([0.5, -2.0, 0.0, 0.1, 0.0, 0.0, 0.0]), "OU-1")
    rel = case["reliability"]
    assert rel["verdict"] == "unstable" and rel["threshold"] == ex.ls.GATE_TAU
    assert rel["recomputations"][0] == {
        "feature": "cum_active_days",
        "label": ex.FEATURE_LABELS["cum_active_days"],
        "count": 3,
    }


def test_case_carries_no_student_identifier():
    case = ex.build_case(_row([0.5, -2.0, 0.0, 0.1, 0.0, 0.0, 0.0]), "OU-1")
    assert set(case) == {
        "caseId",
        "displayName",
        "institution",
        "source",
        "context",
        "risk",
        "riskRankPct",
        "riskBelowPct",
        "riskTiedPct",
        "flagged",
        "factors",
        "reliability",
        "features",
    }
    assert set(case["source"]) == {"cohortId", "studentRow"}
    assert case["riskBelowPct"] == 0.85 and case["riskTiedPct"] == 0.1
    assert case["context"]["rankedStudents"] == 128


def _course(inst: str, cid: str, n: int, auc: float, rng) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "institution": inst,
            "cohort_id": cid,
            "student_row": range(n),
            "self_tau": rng.choice(np.linspace(0.3, 1.0, 8), n),
            "flagged": [i % 3 == 0 for i in range(n)],
            "model_auc": auc,
            # rows 1, 4, 7 … are non-flagged but in the upper half of risk
            "risk_rank_pct": [
                0.9 if i % 3 == 0 else (0.7 if i % 3 == 1 else 0.2) for i in range(n)
            ],
        }
    )


def _selection_frame():
    rng = np.random.default_rng(1)
    parts = []
    for inst in ex.INSTITUTIONS:
        parts += [_course(inst, f"{inst}_c{k}", 30, 0.8, rng) for k in range(2)]
        parts.append(_course(inst, f"{inst}_chance", 30, 0.45, rng))  # never picked
        # A small course: one flagged student and one in the upper half, no calm one.
        parts.append(_course(inst, f"{inst}_small", 2, 0.8, rng))
    frame = pd.concat(parts, ignore_index=True)
    frame.loc[0, "self_tau"] = np.nan  # a constant ranking must never be picked
    return frame


def test_selection_is_per_course_deterministic_unique_and_complete():
    frame = _selection_frame()
    first, second = ex.select_cases(frame), ex.select_cases(frame)
    pd.testing.assert_frame_equal(first, second)
    assert ex.INSTITUTIONS["Zambia"] == "ZM"
    assert set(first["institution"]) == set(ex.INSTITUTIONS)
    assert not first.duplicated(["cohort_id", "student_row"]).any()
    assert first["self_tau"].notna().all()
    assert (first["model_auc"] > 0.5).all()
    for cid, g in first.groupby("cohort_id"):
        if cid.endswith("_small"):
            assert g["flagged"].tolist() == [True]  # takes what the course has
        else:
            assert g["flagged"].sum() == 2 and (~g["flagged"]).sum() == 1
        # The calm example comes from the lower half of the course's risk.
        assert (g.loc[~g["flagged"], "risk_rank_pct"] <= 0.5).all()
    assert len(first) == len(ex.INSTITUTIONS) * (2 * 3 + 1)


def test_flagged_picks_sit_closest_to_the_course_reliability_percentiles():
    frame = _selection_frame()
    chosen = ex.select_cases(frame)
    pool = frame.dropna(subset=["self_tau"])
    for cid in (f"{inst}_c0" for inst in ex.INSTITUTIONS):
        flagged = pool[(pool["cohort_id"] == cid) & pool["flagged"]]["self_tau"]
        picks = chosen[(chosen["cohort_id"] == cid) & chosen["flagged"]]["self_tau"].tolist()
        for q, tau in zip(ex.FLAGGED_PERCENTILES, picks, strict=True):
            target = np.percentile(flagged, q)
            assert abs(tau - target) == (flagged - target).abs().min()


def test_course_label_names_the_run_not_just_the_module():
    cases = {
        ("oulad_BBB_2013J", "OULAD", "BBB"): "BBB 2013J",
        ("ku_Globaleconom_2021", "KU Leuven", "Globaleconom"): "Globaleconom 2020/21",
        ("oviedo_C1112_1415", "Oviedo", "C1112"): "C1112 2014/15",
        ("ukzn_ISTN101_2021", "UKZN", "ISTN101"): "ISTN101 2021",
        ("zambia_ICT1110_2020", "Zambia", "ICT1110"): "ICT1110 2020",
    }
    for (cid, inst, module), label in cases.items():
        assert ex.course_label(cid, inst, module) == label


def test_tied_risks_share_a_midrank_and_flagging_follows_it():
    """A course where most students look identical must not flag them all as the riskiest 20 %."""
    risk = np.array([0.46] * 93 + [0.1] * 7)
    rank, flagged = ex._risk_ranks(risk)
    assert np.allclose(rank[:93], 0.07 + 0.93 / 2)  # midrank of the tied block
    assert not flagged.any()
    top = np.array([0.99] * 25 + list(np.linspace(0.1, 0.5, 75)))
    rank, flagged = ex._risk_ranks(top)
    assert np.allclose(rank[:25], 0.75 + 0.25 / 2)  # the riskiest tied block is flagged
    assert flagged[:25].all() and not flagged[25:].any()


def test_strict_share_below_and_tied_share_for_a_tied_top_block():
    """The headline must not claim a student is riskier than peers who share the same risk."""
    top = np.array([0.99] * 25 + list(np.linspace(0.1, 0.5, 75)))
    below, tied = ex._risk_share_below(top)
    assert np.allclose(below[:25], 0.75) and np.allclose(tied[:25], 0.25)
    assert np.allclose(tied[25:], 0.01)
