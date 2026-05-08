from __future__ import annotations

from typing import Any

from src.db.models import (
    ExplanationCaseRecord,
    ExplanationContributionRecord,
    StudentRecord,
    TwinSnapshotRecord,
)

KNOWN_RISK = {"low", "medium", "high"}

FEATURE_LABELS: dict[str, str] = {
    "activity_score_to_date": "Activity score",
    "avg_assignment_score_to_date": "Assignment average",
    "avg_quiz_score_to_date": "Quiz average",
    "attendance_rate_to_date": "Attendance rate",
    "on_time_submission_rate_to_date": "On-time submission rate",
    "late_submissions_to_date": "Late submissions",
    "missed_assignments_to_date": "Missed assignments",
    "time_spent_to_date": "Time spent (min)",
    "avg_attempt_count_to_date": "Avg. attempts",
    "overall_mastery": "Overall mastery",
    "current_topic_mastery": "Current topic mastery",
    "score_trend_3w": "3-week score trend",
    "activity_trend_3w": "3-week activity trend",
    "attendance_trend_3w": "3-week attendance trend",
}

CASE_TYPE_LABELS: dict[str, str] = {
    "strong_performer": "Strong performer",
    "at_risk": "At risk",
    "improving_trajectory": "Improving trajectory",
    "declining_trajectory": "Declining trajectory",
    "borderline_medium": "Borderline (medium)",
}


def feature_label(feature: str) -> str:
    return FEATURE_LABELS.get(feature, feature.replace("_", " "))


def case_type_label(case_type: str) -> str:
    return CASE_TYPE_LABELS.get(case_type, case_type.replace("_", " "))


def risk_badge(value: str | None) -> str:
    if not value:
        return "unknown"
    normalized = value.lower()
    return normalized if normalized in KNOWN_RISK else "unknown"


def contribution_to_dto(row: ExplanationContributionRecord) -> dict[str, Any]:
    return {
        "feature": row.feature,
        "featureLabel": feature_label(row.feature),
        "value": row.value,
        "contribution": row.contribution,
        "absContribution": row.abs_contribution,
        "direction": row.direction,
        "referenceMedian": row.reference_median,
    }


def explanation_to_dto(row: ExplanationCaseRecord | None) -> dict[str, Any] | None:
    if row is None:
        return None

    contributions = [contribution_to_dto(item) for item in row.contributions]
    top_positive = sorted(
        [item for item in contributions if item["direction"] == "raises_prediction"],
        key=lambda item: item["absContribution"],
        reverse=True,
    )
    top_negative = sorted(
        [item for item in contributions if item["direction"] == "lowers_prediction"],
        key=lambda item: item["absContribution"],
        reverse=True,
    )
    return {
        "studentId": row.student_id,
        "studentLabel": row.student.student_label if row.student else row.student_id,
        "caseType": row.case_type,
        "caseTypeLabel": case_type_label(row.case_type),
        "predictedFinalGrade": row.predicted_final_grade,
        "actualFinalGrade": row.actual_final_grade,
        "predictionError": row.prediction_error,
        "riskLevelContext": row.risk_level_context,
        "passed": row.passed,
        "masteryShare": row.mastery_share,
        "teacherAssessment": row.teacher_assessment,
        "topPositive": top_positive,
        "topNegative": top_negative,
        "weekNumber": row.week_number,
    }


def snapshot_to_dto(row: TwinSnapshotRecord) -> dict[str, Any]:
    return {
        "weekNumber": row.week_number,
        "predictedFinalGrade": row.predicted_final_grade,
        "riskLevel": risk_badge(row.risk_level),
        "riskScore": row.risk_score,
        "activityScore": row.activity_score,
        "assignmentAverage": row.assignment_average,
        "quizAverage": row.quiz_average,
        "attendanceRate": row.attendance_rate,
        "overallMastery": row.overall_mastery,
        "currentTopicMastery": row.current_topic_mastery,
        "engagementIndex": row.engagement_index,
        "performanceIndex": row.performance_index,
        "disciplineIndex": row.discipline_index,
        "scoreTrend3w": row.score_trend_3w,
        "activityTrend3w": row.activity_trend_3w,
        "attendanceTrend3w": row.attendance_trend_3w,
    }


def student_summary_to_dto(row: StudentRecord) -> dict[str, Any]:
    current = max(row.snapshots, key=lambda item: item.week_number, default=None)
    explanation = explanation_to_dto(row.explanation_case)
    top_factors = []
    if explanation:
        top_factors = sorted(
            [*explanation["topPositive"][:2], *explanation["topNegative"][:2]],
            key=lambda item: item["absContribution"],
            reverse=True,
        )[:3]

    return {
        "studentId": row.student_id,
        "studentLabel": row.student_label,
        "cohortLabel": row.cohort_label,
        "trajectoryLabel": row.trajectory_label,
        "courseId": row.course_id,
        "currentWeek": row.current_week,
        "predictedFinalGrade": current.predicted_final_grade if current else None,
        "actualFinalGrade": row.actual_final_grade,
        "passed": row.passed,
        "riskBadge": risk_badge(current.risk_level if current else None),
        "riskScore": current.risk_score if current else None,
        "activityScore": current.activity_score if current else None,
        "assignmentAverage": current.assignment_average if current else None,
        "quizAverage": current.quiz_average if current else None,
        "attendanceRate": current.attendance_rate if current else None,
        "overallMastery": current.overall_mastery if current else None,
        "currentTopicMastery": current.current_topic_mastery if current else None,
        "scoreTrend3w": current.score_trend_3w if current else None,
        "hasExplanation": explanation is not None,
        "explanationCaseType": explanation["caseType"] if explanation else None,
        "topExplanationFactors": top_factors,
    }


def student_detail_to_dto(row: StudentRecord) -> dict[str, Any]:
    summary = student_summary_to_dto(row)
    timeline = [
        snapshot_to_dto(item)
        for item in sorted(row.snapshots, key=lambda item: item.week_number)
    ]
    explanation = explanation_to_dto(row.explanation_case)
    return {**summary, "timeline": timeline, "explanation": explanation}
