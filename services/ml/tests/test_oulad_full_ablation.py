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
