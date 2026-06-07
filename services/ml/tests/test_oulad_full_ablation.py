from pathlib import Path

import pandas as pd

from src.benchmarks.oulad_adapter import (
    OuladCourseFilter,
    OuladRawPaths,
    build_weekly_snapshots,
)
from src.generator.config import REPO_ROOT

OULAD = REPO_ROOT / "datasets" / "oulad"


def _snapshots() -> pd.DataFrame:
    raw = OuladRawPaths(
        assessments=OULAD / "assessments.csv",
        courses=OULAD / "courses.csv",
        student_info=OULAD / "studentInfo.csv",
        student_registration=OULAD / "studentRegistration.csv",
        student_vle=OULAD / "studentVle.csv",
        vle=OULAD / "vle.csv",
        student_assessment=OULAD / "studentAssessment.csv",
    )
    return build_weekly_snapshots(
        raw,
        course_filter=OuladCourseFilter("DDD", "2013J"),
        min_week=4,
        max_week=None,
    ).snapshots


def test_trend_and_index_columns_present():
    snaps = _snapshots()
    for col in [
        "assessment_score_trend_to_date",
        "clicks_trend_to_date",
        "engagement_index_oulad",
        "performance_index_oulad",
        "discipline_index_oulad",
    ]:
        assert col in snaps.columns, f"missing {col}"


def test_index_columns_are_bounded_unit_interval():
    snaps = _snapshots()
    for col in ["engagement_index_oulad", "performance_index_oulad", "discipline_index_oulad"]:
        series = snaps[col].dropna()
        assert (series >= -1e-9).all() and (series <= 1.0 + 1e-9).all(), f"{col} out of [0,1]"


def test_indices_use_fixed_denominator_on_partial_nan():
    import numpy as np
    from src.benchmarks.oulad_adapter import _add_trend_and_index_features

    df = pd.DataFrame(
        {
            "code_module": ["DDD"],
            "code_presentation": ["2013J"],
            "id_student": ["1"],
            "week_number": [4],
            "cumulative_assessment_score_mean_to_date": [np.nan],
            "cumulative_assessment_weighted_score_to_date": [np.nan],
            "current_week_clicks": [0.0],
            "assessment_submission_rate_due_to_date": [1.0],
            "late_submission_rate_to_date": [np.nan],
            "banked_assessment_rate_to_date": [np.nan],
            "has_vle_activity_to_date": [np.nan],
        }
    )
    out = _add_trend_and_index_features(df)
    # performance: both components NaN -> filled 0 -> mean([0,0]) = 0.0
    assert abs(float(out["performance_index_oulad"].iloc[0]) - 0.0) < 1e-9
    # discipline: [1.0, (1 - NaN)->0, NaN->0] -> mean = 1/3 (NOT 1.0)
    assert abs(float(out["discipline_index_oulad"].iloc[0]) - (1.0 / 3.0)) < 1e-9
    # engagement: [1.0, NaN->0] -> mean = 0.5 (NOT 1.0)
    assert abs(float(out["engagement_index_oulad"].iloc[0]) - 0.5) < 1e-9
