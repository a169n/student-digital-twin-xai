from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ResearchMetadataRecord(Base):
    __tablename__ = "research_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    schema_version: Mapped[str] = mapped_column(String(32), nullable=False)
    imported_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    source_payload_path: Mapped[str] = mapped_column(Text, nullable=False)
    source_artifacts_json: Mapped[str] = mapped_column(Text, nullable=False)
    feature_directions_json: Mapped[str] = mapped_column(Text, nullable=False)
    xai_json: Mapped[str] = mapped_column(Text, nullable=False)
    experiments_json: Mapped[str] = mapped_column(Text, nullable=False)
    limitations_json: Mapped[str] = mapped_column(Text, nullable=False)


class StudentRecord(Base):
    __tablename__ = "students"

    student_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    student_label: Mapped[str] = mapped_column(String(128), nullable=False)
    cohort_label: Mapped[str | None] = mapped_column(String(64))
    trajectory_label: Mapped[str | None] = mapped_column(String(64))
    course_id: Mapped[str] = mapped_column(String(64), nullable=False)
    current_week: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_final_grade: Mapped[float | None] = mapped_column(Float)
    passed: Mapped[bool | None] = mapped_column(Boolean)

    snapshots: Mapped[list[TwinSnapshotRecord]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )
    explanation_case: Mapped[ExplanationCaseRecord | None] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class TwinSnapshotRecord(Base):
    __tablename__ = "twin_snapshots"
    __table_args__ = (
        UniqueConstraint("student_id", "week_number", name="uq_snapshot_student_week"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("students.student_id"), nullable=False)
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    predicted_final_grade: Mapped[float | None] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(16), nullable=False)
    risk_score: Mapped[float | None] = mapped_column(Float)
    activity_score: Mapped[float | None] = mapped_column(Float)
    assignment_average: Mapped[float | None] = mapped_column(Float)
    quiz_average: Mapped[float | None] = mapped_column(Float)
    attendance_rate: Mapped[float | None] = mapped_column(Float)
    overall_mastery: Mapped[float | None] = mapped_column(Float)
    current_topic_mastery: Mapped[float | None] = mapped_column(Float)
    engagement_index: Mapped[float | None] = mapped_column(Float)
    performance_index: Mapped[float | None] = mapped_column(Float)
    discipline_index: Mapped[float | None] = mapped_column(Float)
    score_trend_3w: Mapped[float | None] = mapped_column(Float)
    activity_trend_3w: Mapped[float | None] = mapped_column(Float)
    attendance_trend_3w: Mapped[float | None] = mapped_column(Float)

    student: Mapped[StudentRecord] = relationship(back_populates="snapshots")


class ExplanationCaseRecord(Base):
    __tablename__ = "explanation_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(
        ForeignKey("students.student_id"), nullable=False, unique=True
    )
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    case_type: Mapped[str] = mapped_column(String(64), nullable=False)
    actual_final_grade: Mapped[float | None] = mapped_column(Float)
    predicted_final_grade: Mapped[float | None] = mapped_column(Float)
    prediction_error: Mapped[float | None] = mapped_column(Float)
    risk_level_context: Mapped[str] = mapped_column(String(16), nullable=False)
    passed: Mapped[bool | None] = mapped_column(Boolean)
    mastery_share: Mapped[float | None] = mapped_column(Float)
    teacher_assessment: Mapped[str] = mapped_column(Text, nullable=False)

    student: Mapped[StudentRecord] = relationship(back_populates="explanation_case")
    contributions: Mapped[list[ExplanationContributionRecord]] = relationship(
        back_populates="case",
        cascade="all, delete-orphan",
        order_by="ExplanationContributionRecord.rank",
    )


class ExplanationContributionRecord(Base):
    __tablename__ = "explanation_contributions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("explanation_cases.id"), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    feature: Mapped[str] = mapped_column(String(128), nullable=False)
    value: Mapped[float | None] = mapped_column(Float)
    contribution: Mapped[float] = mapped_column(Float, nullable=False)
    abs_contribution: Mapped[float] = mapped_column(Float, nullable=False)
    direction: Mapped[str] = mapped_column(String(32), nullable=False)
    reference_median: Mapped[float | None] = mapped_column(Float)

    case: Mapped[ExplanationCaseRecord] = relationship(back_populates="contributions")


class ReviewMetadataRecord(Base):
    """Payload-level context for the review screen (scale context, labels, provenance)."""

    __tablename__ = "review_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)


class ReviewCaseRecord(Base):
    """One precomputed teacher-review case, stored as the exporter wrote it."""

    __tablename__ = "review_cases"

    case_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    institution: Mapped[str] = mapped_column(String(64), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)


class ReviewDecisionRecord(Base):
    """A teacher's decision on a case. Append-only; survives a re-import of the cases.

    case_id is a position-based pseudonym that a re-export can hand to another
    student, so each decision also records which source student it was about
    and is only shown while the case still points at that student.
    """

    __tablename__ = "review_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    source_key: Mapped[str] = mapped_column(String(128), nullable=False)
    action: Mapped[str] = mapped_column(String(32), nullable=False)
    factor: Mapped[str | None] = mapped_column(String(64))
    note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
