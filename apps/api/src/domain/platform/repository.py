from __future__ import annotations

import json
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, selectinload

from src.db.models import (
    ExplanationCaseRecord,
    ExplanationContributionRecord,
    ResearchMetadataRecord,
    StudentRecord,
    TwinSnapshotRecord,
)
from src.domain.platform.projections import (
    contribution_to_dto,
    explanation_to_dto,
    feature_label,
    student_detail_to_dto,
    student_summary_to_dto,
)

LOW_ACTIVITY_THRESHOLD = 40.0
LOW_MASTERY_THRESHOLD = 60.0
AT_RISK_GRADE_THRESHOLD = 60.0


class PlatformRepository:
    def __init__(self, session: Session):
        self.session = session

    def status(self) -> dict[str, Any]:
        metadata = self._metadata()
        snapshot_count = self.session.scalar(select(func.count(TwinSnapshotRecord.id))) or 0
        case_count = self.session.scalar(select(func.count(ExplanationCaseRecord.id))) or 0
        return {
            "seeded": self.count_students() > 0,
            "studentCount": self.count_students(),
            "snapshotCount": snapshot_count,
            "explanationCaseCount": case_count,
            "payloadSchemaVersion": metadata.schema_version if metadata else None,
            "lastImportedAt": metadata.imported_at.isoformat() if metadata else None,
            "sourcePayloadPath": metadata.source_payload_path if metadata else None,
            "sourceArtifacts": self._json(metadata.source_artifacts_json, {}) if metadata else {},
        }

    def count_students(self) -> int:
        return self.session.scalar(select(func.count(StudentRecord.student_id))) or 0

    def list_students(self) -> list[dict[str, Any]]:
        rows = self.session.scalars(self._students_query().order_by(StudentRecord.student_id)).all()
        return [student_summary_to_dto(row) for row in rows]

    def get_student_detail(self, student_id: str) -> dict[str, Any] | None:
        row = self.session.scalar(
            self._students_query().where(StudentRecord.student_id == student_id)
        )
        return student_detail_to_dto(row) if row else None

    def get_snapshots(self, student_id: str) -> list[dict[str, Any]] | None:
        student = self.session.get(StudentRecord, student_id)
        if student is None:
            return None
        detail = self.get_student_detail(student_id)
        return detail["timeline"] if detail else []

    def dashboard(self) -> dict[str, Any]:
        students = self.list_students()
        return {"cohort": self._cohort(students), "students": students}

    def latest_predictions(self) -> dict[str, Any]:
        students = self.list_students()
        predictions = [
            {
                "studentId": student["studentId"],
                "studentLabel": student["studentLabel"],
                "courseId": student["courseId"],
                "weekNumber": student["currentWeek"],
                "predictedFinalGrade": student["predictedFinalGrade"],
                "actualFinalGrade": student["actualFinalGrade"],
                "passed": student["passed"],
                "riskLevel": student["riskBadge"],
                "riskScore": student["riskScore"],
                "featureSet": "B_lms_plus_mastery",
                "source": "imported_frozen_research_payload",
            }
            for student in students
        ]
        return {"predictions": predictions}

    def global_explanations(self) -> dict[str, Any]:
        metadata = self._metadata()
        if metadata is None:
            return {
                "method": None,
                "shapUsed": False,
                "topGlobalFeatures": [],
                "dominance": None,
                "recommendation": None,
            }
        xai = self._json(metadata.xai_json, {})
        return {
            "method": xai.get("method"),
            "shapUsed": xai.get("shapUsed", False),
            "topGlobalFeatures": [
                {
                    "feature": item["feature"],
                    "featureLabel": feature_label(item["feature"]),
                    "rank": item["rank"],
                    "importanceShare": item["importanceShare"],
                }
                for item in xai.get("topGlobalFeatures", [])
            ],
            "dominance": xai.get("dominance"),
            "recommendation": xai.get("recommendation"),
        }

    def explanation_cases(self) -> list[dict[str, Any]]:
        rows = self.session.scalars(
            select(ExplanationCaseRecord)
            .options(selectinload(ExplanationCaseRecord.contributions))
            .order_by(ExplanationCaseRecord.week_number, ExplanationCaseRecord.case_type)
        ).all()
        return [case for row in rows if (case := explanation_to_dto(row)) is not None]

    def research_evidence(self) -> dict[str, Any]:
        metadata = self._metadata()
        if metadata is None:
            return {
                "timeline": [],
                "leanTwin": None,
                "xai": self.global_explanations(),
                "oulad": None,
                "limitations": [],
                "sourceArtifacts": {},
            }

        experiments = self._json(metadata.experiments_json, {})
        return {
            "timeline": experiments.get("timeline", []),
            "leanTwin": experiments.get("leanTwin"),
            "xai": self.global_explanations(),
            "oulad": self._adapt_oulad(experiments.get("oulad", {})),
            "limitations": self._json(metadata.limitations_json, []),
            "sourceArtifacts": self._json(metadata.source_artifacts_json, {}),
        }

    def contribution_rows_for_case(self, case_id: int) -> list[dict[str, Any]]:
        rows = self.session.scalars(
            select(ExplanationContributionRecord)
            .where(ExplanationContributionRecord.case_id == case_id)
            .order_by(ExplanationContributionRecord.rank)
        ).all()
        return [contribution_to_dto(row) for row in rows]

    def _metadata(self) -> ResearchMetadataRecord | None:
        return self.session.get(ResearchMetadataRecord, 1)

    def _students_query(self) -> Select[tuple[StudentRecord]]:
        return select(StudentRecord).options(
            selectinload(StudentRecord.snapshots),
            selectinload(StudentRecord.explanation_case).selectinload(
                ExplanationCaseRecord.contributions
            ),
        )

    def _cohort(self, students: list[dict[str, Any]]) -> dict[str, Any]:
        if not students:
            return {
                "courseId": None,
                "studentCount": 0,
                "currentWeek": None,
                "meanPredictedFinalGrade": None,
                "meanActualFinalGrade": None,
                "meanOverallMastery": None,
                "meanActivityScore": None,
                "meanAttendanceRate": None,
                "riskDistribution": {"low": 0, "medium": 0, "high": 0},
                "atRiskCount": 0,
                "lowMasteryCount": 0,
                "lowActivityCount": 0,
                "topAtRisk": [],
                "topImproving": [],
            }

        risk_distribution = {"low": 0, "medium": 0, "high": 0}
        for student in students:
            risk = student["riskBadge"]
            if risk in risk_distribution:
                risk_distribution[risk] += 1

        sorted_by_predicted = sorted(
            [student for student in students if student["predictedFinalGrade"] is not None],
            key=lambda student: student["predictedFinalGrade"],
        )

        improvers: list[tuple[str, float]] = []
        for student in students:
            detail = self.get_student_detail(student["studentId"])
            if not detail:
                continue
            predicted_rows = [
                row for row in detail["timeline"] if row["predictedFinalGrade"] is not None
            ]
            if len(predicted_rows) < 2:
                continue
            delta = (
                predicted_rows[-1]["predictedFinalGrade"]
                - predicted_rows[0]["predictedFinalGrade"]
            )
            improvers.append((student["studentId"], delta))
        improvers.sort(key=lambda item: item[1], reverse=True)

        course_ids = {student["courseId"] for student in students}
        weeks = [student["currentWeek"] for student in students]

        return {
            "courseId": next(iter(course_ids)) if len(course_ids) == 1 else None,
            "studentCount": len(students),
            "currentWeek": max(weeks) if weeks else None,
            "meanPredictedFinalGrade": self._mean(students, "predictedFinalGrade"),
            "meanActualFinalGrade": self._mean(students, "actualFinalGrade"),
            "meanOverallMastery": self._mean(students, "overallMastery"),
            "meanActivityScore": self._mean(students, "activityScore"),
            "meanAttendanceRate": self._mean(students, "attendanceRate", digits=4),
            "riskDistribution": risk_distribution,
            "atRiskCount": sum(
                1
                for student in students
                if student["predictedFinalGrade"] is not None
                and student["predictedFinalGrade"] < AT_RISK_GRADE_THRESHOLD
            ),
            "lowMasteryCount": sum(
                1
                for student in students
                if student["overallMastery"] is not None
                and student["overallMastery"] < LOW_MASTERY_THRESHOLD
            ),
            "lowActivityCount": sum(
                1
                for student in students
                if student["activityScore"] is not None
                and student["activityScore"] < LOW_ACTIVITY_THRESHOLD
            ),
            "topAtRisk": sorted_by_predicted[:5],
            "topImproving": [
                student
                for student_id, _ in improvers[:5]
                for student in students
                if student["studentId"] == student_id
            ],
        }

    @staticmethod
    def _mean(rows: list[dict[str, Any]], field: str, digits: int = 2) -> float | None:
        values = [row[field] for row in rows if row[field] is not None]
        if not values:
            return None
        return round(sum(values) / len(values), digits)

    @staticmethod
    def _json(raw: str, fallback: Any) -> Any:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return fallback

    @staticmethod
    def _adapt_oulad(oulad: dict[str, Any]) -> dict[str, Any]:
        return {
            "rowCounts": oulad.get("rowCounts", {"snapshots": 0, "students": 0}),
            "weekMin": oulad.get("weekMin"),
            "weekMax": oulad.get("weekMax"),
            "outcome": oulad.get("outcome"),
            "shortConclusion": oulad.get("shortConclusion"),
            "grouped": {
                "baselineRmse": (oulad.get("grouped", {}).get("baseline") or {}).get("rmse"),
                "leanRmse": (oulad.get("grouped", {}).get("lean") or {}).get("rmse"),
                "delta": oulad.get("grouped", {}).get("delta"),
            },
            "temporal": {
                "baselineRmse": (oulad.get("temporal", {}).get("baseline") or {}).get("rmse"),
                "leanRmse": (oulad.get("temporal", {}).get("lean") or {}).get("rmse"),
                "delta": oulad.get("temporal", {}).get("delta"),
            },
        }
