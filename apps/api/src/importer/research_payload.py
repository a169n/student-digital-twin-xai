from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import delete
from sqlalchemy.orm import Session

from src.db.models import (
    ExplanationCaseRecord,
    ExplanationContributionRecord,
    ResearchMetadataRecord,
    StudentRecord,
    TwinSnapshotRecord,
)


@dataclass(frozen=True)
class ImportSummary:
    student_count: int
    snapshot_count: int
    explanation_case_count: int
    source_payload_path: str
    payload_schema_version: str


def load_research_payload(path: str | Path) -> dict[str, Any]:
    payload_path = Path(path)
    with payload_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def import_research_payload(
    session: Session,
    *,
    payload_path: str | Path,
    payload: dict[str, Any] | None = None,
) -> ImportSummary:
    resolved_payload_path = Path(payload_path).resolve()
    payload_data = payload if payload is not None else load_research_payload(resolved_payload_path)

    _clear_existing_projection(session)

    metadata = ResearchMetadataRecord(
        id=1,
        schema_version=payload_data["schemaVersion"],
        imported_at=datetime.now(timezone.utc).replace(tzinfo=None),
        source_payload_path=str(resolved_payload_path),
        source_artifacts_json=_dump(payload_data.get("sourceArtifacts", {})),
        feature_directions_json=_dump(payload_data.get("featureDirections", {})),
        xai_json=_dump(payload_data.get("xai", {})),
        experiments_json=_dump(payload_data.get("experiments", {})),
        limitations_json=_dump(payload_data.get("limitations", [])),
    )
    session.add(metadata)

    snapshot_count = 0
    for student in payload_data.get("students", []):
        session.add(
            StudentRecord(
                student_id=student["studentId"],
                student_label=student["studentLabel"],
                cohort_label=student.get("cohortLabel"),
                trajectory_label=student.get("trajectoryLabel"),
                course_id=student["courseId"],
                current_week=student["currentWeek"],
                actual_final_grade=student.get("actualFinalGrade"),
                passed=student.get("passed"),
            )
        )
        for weekly in student.get("weeklyTimeline", []):
            snapshot_count += 1
            session.add(
                TwinSnapshotRecord(
                    student_id=student["studentId"],
                    week_number=weekly["weekNumber"],
                    predicted_final_grade=weekly.get("predictedFinalGrade"),
                    risk_level=weekly.get("riskLevel", "unknown"),
                    risk_score=weekly.get("riskScore"),
                    activity_score=weekly.get("activityScore"),
                    assignment_average=weekly.get("assignmentAverage"),
                    quiz_average=weekly.get("quizAverage"),
                    attendance_rate=weekly.get("attendanceRate"),
                    overall_mastery=weekly.get("overallMastery"),
                    current_topic_mastery=weekly.get("currentTopicMastery"),
                    engagement_index=weekly.get("engagementIndex"),
                    performance_index=weekly.get("performanceIndex"),
                    discipline_index=weekly.get("disciplineIndex"),
                    score_trend_3w=weekly.get("scoreTrend3w"),
                    activity_trend_3w=weekly.get("activityTrend3w"),
                    attendance_trend_3w=weekly.get("attendanceTrend3w"),
                )
            )

    session.flush()

    explanation_case_count = 0
    for case in payload_data.get("cases", []):
        explanation_case_count += 1
        case_row = ExplanationCaseRecord(
            student_id=case["studentId"],
            week_number=case["weekNumber"],
            case_type=case["caseType"],
            actual_final_grade=case.get("actualFinalGrade"),
            predicted_final_grade=case.get("predictedFinalGrade"),
            prediction_error=case.get("predictionError"),
            risk_level_context=case.get("riskLevelContext", "unknown"),
            passed=case.get("passed"),
            mastery_share=case.get("masteryShare"),
            teacher_assessment=case.get("teacherAssessment", ""),
        )
        session.add(case_row)
        session.flush()
        for rank, contribution in enumerate(case.get("topContributions", []), start=1):
            session.add(
                ExplanationContributionRecord(
                    case_id=case_row.id,
                    rank=rank,
                    feature=contribution["feature"],
                    value=contribution.get("value"),
                    contribution=contribution["contribution"],
                    abs_contribution=contribution["absContribution"],
                    direction=contribution["direction"],
                    reference_median=contribution.get("referenceMedian"),
                )
            )

    session.commit()
    return ImportSummary(
        student_count=len(payload_data.get("students", [])),
        snapshot_count=snapshot_count,
        explanation_case_count=explanation_case_count,
        source_payload_path=str(resolved_payload_path),
        payload_schema_version=payload_data["schemaVersion"],
    )


def _clear_existing_projection(session: Session) -> None:
    session.execute(delete(ExplanationContributionRecord))
    session.execute(delete(ExplanationCaseRecord))
    session.execute(delete(TwinSnapshotRecord))
    session.execute(delete(StudentRecord))
    session.execute(delete(ResearchMetadataRecord))


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True)
