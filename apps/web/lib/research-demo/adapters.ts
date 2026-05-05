import type {
  CohortSummary,
  ExplanationContribution,
  ExplanationSummary,
  PayloadCase,
  ResearchDemoData,
  ResearchDemoPayload,
  ResearchSummary,
  RiskBadge,
  StudentDetail,
  StudentSummary,
  StudentWeekRow
} from "./types";

const KNOWN_RISK: RiskBadge[] = ["low", "medium", "high"];

const FEATURE_LABELS: Record<string, string> = {
  activity_score_to_date: "Activity score",
  avg_assignment_score_to_date: "Assignment average",
  avg_quiz_score_to_date: "Quiz average",
  attendance_rate_to_date: "Attendance rate",
  on_time_submission_rate_to_date: "On-time submission rate",
  late_submissions_to_date: "Late submissions",
  missed_assignments_to_date: "Missed assignments",
  time_spent_to_date: "Time spent (min)",
  avg_attempt_count_to_date: "Avg. attempts",
  overall_mastery: "Overall mastery",
  current_topic_mastery: "Current topic mastery",
  score_trend_3w: "3-week score trend",
  activity_trend_3w: "3-week activity trend",
  attendance_trend_3w: "3-week attendance trend"
};

const CASE_TYPE_LABELS: Record<string, string> = {
  strong_performer: "Strong performer",
  at_risk: "At risk",
  improving_trajectory: "Improving trajectory",
  declining_trajectory: "Declining trajectory",
  borderline_medium: "Borderline (medium)"
};

export function featureLabel(feature: string): string {
  return FEATURE_LABELS[feature] ?? feature.replaceAll("_", " ");
}

export function caseTypeLabel(caseType: string): string {
  return CASE_TYPE_LABELS[caseType] ?? caseType.replaceAll("_", " ");
}

function toRiskBadge(value: string | null | undefined): RiskBadge {
  if (!value) return "unknown";
  const normalized = value.toLowerCase();
  return (KNOWN_RISK as string[]).includes(normalized) ? (normalized as RiskBadge) : "unknown";
}

function adaptContribution(raw: PayloadCase["topContributions"][number]): ExplanationContribution {
  return {
    feature: raw.feature,
    featureLabel: featureLabel(raw.feature),
    value: raw.value,
    contribution: raw.contribution,
    absContribution: raw.absContribution,
    direction: raw.direction,
    referenceMedian: raw.referenceMedian
  };
}

function adaptCase(raw: PayloadCase): ExplanationSummary {
  const contributions = raw.topContributions.map(adaptContribution);
  const topPositive = contributions
    .filter((item) => item.direction === "raises_prediction")
    .sort((a, b) => b.absContribution - a.absContribution);
  const topNegative = contributions
    .filter((item) => item.direction === "lowers_prediction")
    .sort((a, b) => b.absContribution - a.absContribution);
  return {
    caseType: raw.caseType,
    caseTypeLabel: caseTypeLabel(raw.caseType),
    predictedFinalGrade: raw.predictedFinalGrade,
    actualFinalGrade: raw.actualFinalGrade,
    predictionError: raw.predictionError,
    riskLevelContext: raw.riskLevelContext,
    passed: raw.passed,
    masteryShare: raw.masteryShare,
    teacherAssessment: raw.teacherAssessment,
    topPositive,
    topNegative,
    weekNumber: raw.weekNumber
  };
}

function adaptStudentSummary(raw: ResearchDemoPayload["students"][number]): StudentSummary {
  const explanation = raw.explanation ? adaptCase(raw.explanation) : null;
  const topFactors = explanation
    ? [...explanation.topPositive.slice(0, 2), ...explanation.topNegative.slice(0, 2)]
        .sort((a, b) => b.absContribution - a.absContribution)
        .slice(0, 3)
    : [];
  return {
    studentId: raw.studentId,
    studentLabel: raw.studentLabel,
    cohortLabel: raw.cohortLabel,
    trajectoryLabel: raw.trajectoryLabel,
    courseId: raw.courseId,
    currentWeek: raw.currentWeek,
    predictedFinalGrade: raw.current.predictedFinalGrade,
    actualFinalGrade: raw.actualFinalGrade,
    passed: raw.passed,
    riskBadge: toRiskBadge(raw.current.riskLevel),
    riskScore: raw.current.riskScore,
    activityScore: raw.current.activityScore,
    assignmentAverage: raw.current.assignmentAverage,
    quizAverage: raw.current.quizAverage,
    attendanceRate: raw.current.attendanceRate,
    overallMastery: raw.current.overallMastery,
    currentTopicMastery: raw.current.currentTopicMastery,
    scoreTrend3w: raw.current.scoreTrend3w,
    hasExplanation: explanation !== null,
    explanationCaseType: explanation ? explanation.caseType : null,
    topExplanationFactors: topFactors
  };
}

function adaptTimeline(
  raw: ResearchDemoPayload["students"][number]["weeklyTimeline"]
): StudentWeekRow[] {
  return raw.map((row) => ({
    weekNumber: row.weekNumber,
    predictedFinalGrade: row.predictedFinalGrade,
    riskLevel: toRiskBadge(row.riskLevel),
    activityScore: row.activityScore,
    assignmentAverage: row.assignmentAverage,
    quizAverage: row.quizAverage,
    attendanceRate: row.attendanceRate,
    overallMastery: row.overallMastery,
    currentTopicMastery: row.currentTopicMastery,
    scoreTrend3w: row.scoreTrend3w
  }));
}

function adaptCohort(payload: ResearchDemoPayload, students: StudentSummary[]): CohortSummary {
  const byId = new Map(students.map((s) => [s.studentId, s] as const));
  return {
    courseId: payload.cohort.courseId,
    studentCount: payload.cohort.studentCount,
    currentWeek: payload.cohort.currentWeek,
    meanPredictedFinalGrade: payload.cohort.meanPredictedFinalGrade,
    meanActualFinalGrade: payload.cohort.meanActualFinalGrade,
    meanOverallMastery: payload.cohort.meanOverallMastery,
    meanActivityScore: payload.cohort.meanActivityScore,
    meanAttendanceRate: payload.cohort.meanAttendanceRate,
    riskDistribution: payload.cohort.riskDistribution,
    atRiskCount: payload.cohort.atRiskCount,
    lowMasteryCount: payload.cohort.lowMasteryCount,
    lowActivityCount: payload.cohort.lowActivityCount,
    topAtRisk: payload.cohort.topAtRisk
      .map((id) => byId.get(id))
      .filter((s): s is StudentSummary => Boolean(s)),
    topImproving: payload.cohort.topImproving
      .map((id) => byId.get(id))
      .filter((s): s is StudentSummary => Boolean(s))
  };
}

function adaptResearch(payload: ResearchDemoPayload): ResearchSummary {
  return {
    timeline: payload.experiments.timeline,
    leanTwin: payload.experiments.leanTwin,
    xai: {
      method: payload.xai.method,
      shapUsed: payload.xai.shapUsed,
      topGlobalFeatures: payload.xai.topGlobalFeatures.map((feature) => ({
        feature: feature.feature,
        featureLabel: featureLabel(feature.feature),
        rank: feature.rank,
        importanceShare: feature.importanceShare
      })),
      dominance: payload.xai.dominance,
      recommendation: payload.xai.recommendation
    },
    oulad: {
      rowCounts: payload.experiments.oulad.rowCounts,
      weekMin: payload.experiments.oulad.weekMin,
      weekMax: payload.experiments.oulad.weekMax,
      outcome: payload.experiments.oulad.outcome,
      shortConclusion: payload.experiments.oulad.shortConclusion,
      grouped: {
        baselineRmse: payload.experiments.oulad.grouped.baseline?.rmse ?? null,
        leanRmse: payload.experiments.oulad.grouped.lean?.rmse ?? null,
        delta: payload.experiments.oulad.grouped.delta
      },
      temporal: {
        baselineRmse: payload.experiments.oulad.temporal.baseline?.rmse ?? null,
        leanRmse: payload.experiments.oulad.temporal.lean?.rmse ?? null,
        delta: payload.experiments.oulad.temporal.delta
      }
    },
    limitations: payload.limitations,
    sourceArtifacts: payload.sourceArtifacts
  };
}

export function adaptDemo(payload: ResearchDemoPayload): ResearchDemoData {
  const students = payload.students.map(adaptStudentSummary);
  const cohort = adaptCohort(payload, students);
  const research = adaptResearch(payload);
  const cases = payload.cases.map(adaptCase);
  return { cohort, students, research, cases };
}

export function buildStudentDetail(
  payload: ResearchDemoPayload,
  studentId: string
): StudentDetail | null {
  const raw = payload.students.find((s) => s.studentId === studentId);
  if (!raw) return null;
  const summary = adaptStudentSummary(raw);
  const timeline = adaptTimeline(raw.weeklyTimeline);
  const explanation = raw.explanation ? adaptCase(raw.explanation) : null;
  return { ...summary, timeline, explanation };
}

export function formatNumber(value: number | null | undefined, digits = 2): string {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return value.toFixed(digits);
}

export function formatSigned(value: number | null | undefined, digits = 2): string {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  const fixed = value.toFixed(digits);
  return value >= 0 ? `+${fixed}` : fixed;
}

export function formatPercent(value: number | null | undefined, digits = 0): string {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return `${(value * 100).toFixed(digits)}%`;
}
