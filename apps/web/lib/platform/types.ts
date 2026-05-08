export type RiskBadge = "low" | "medium" | "high" | "unknown";

export type RiskDistribution = {
  low: number;
  medium: number;
  high: number;
};

export type ExplanationContribution = {
  feature: string;
  featureLabel: string;
  value: number | null;
  contribution: number;
  absContribution: number;
  direction: "raises_prediction" | "lowers_prediction";
  referenceMedian: number | null;
};

export type ExplanationSummary = {
  studentId: string;
  studentLabel: string;
  caseType: string;
  caseTypeLabel: string;
  predictedFinalGrade: number | null;
  actualFinalGrade: number | null;
  predictionError: number | null;
  riskLevelContext: string;
  passed: boolean | null;
  masteryShare: number | null;
  teacherAssessment: string;
  topPositive: ExplanationContribution[];
  topNegative: ExplanationContribution[];
  weekNumber: number;
};

export type StudentSummary = {
  studentId: string;
  studentLabel: string;
  cohortLabel: string | null;
  trajectoryLabel: string | null;
  courseId: string;
  currentWeek: number;
  predictedFinalGrade: number | null;
  actualFinalGrade: number | null;
  passed: boolean | null;
  riskBadge: RiskBadge;
  riskScore: number | null;
  activityScore: number | null;
  assignmentAverage: number | null;
  quizAverage: number | null;
  attendanceRate: number | null;
  overallMastery: number | null;
  currentTopicMastery: number | null;
  scoreTrend3w: number | null;
  hasExplanation: boolean;
  explanationCaseType: string | null;
  topExplanationFactors: ExplanationContribution[];
};

export type StudentWeekRow = {
  weekNumber: number;
  predictedFinalGrade: number | null;
  riskLevel: RiskBadge;
  riskScore: number | null;
  activityScore: number | null;
  assignmentAverage: number | null;
  quizAverage: number | null;
  attendanceRate: number | null;
  overallMastery: number | null;
  currentTopicMastery: number | null;
  engagementIndex: number | null;
  performanceIndex: number | null;
  disciplineIndex: number | null;
  scoreTrend3w: number | null;
  activityTrend3w: number | null;
  attendanceTrend3w: number | null;
};

export type StudentDetail = StudentSummary & {
  timeline: StudentWeekRow[];
  explanation: ExplanationSummary | null;
};

export type CohortSummary = {
  courseId: string | null;
  studentCount: number;
  currentWeek: number | null;
  meanPredictedFinalGrade: number | null;
  meanActualFinalGrade: number | null;
  meanOverallMastery: number | null;
  meanActivityScore: number | null;
  meanAttendanceRate: number | null;
  riskDistribution: RiskDistribution;
  atRiskCount: number;
  lowMasteryCount: number;
  lowActivityCount: number;
  topAtRisk: StudentSummary[];
  topImproving: StudentSummary[];
};

export type DashboardData = {
  cohort: CohortSummary;
  students: StudentSummary[];
};

export type ExperimentTimelineItem = {
  id: string;
  title: string;
  result: string;
  decision: string;
};

export type ResearchSummary = {
  timeline: ExperimentTimelineItem[];
  leanTwin: {
    baselineRmse: number | null;
    leanRmse: number | null;
    leanDelta: number | null;
    withoutOverallDelta: number | null;
    earlyWeeksImproved: number[];
    lateWeeksImproved: number[];
    flags: string[];
  } | null;
  xai: {
    method: string | null;
    shapUsed: boolean;
    topGlobalFeatures: Array<{
      feature: string;
      featureLabel: string;
      rank: number;
      importanceShare: number;
    }>;
    dominance: {
      topFeature: string;
      top1Share: number;
      averageLocalMasteryShare: number;
      outcome: string;
      flags: string[];
    } | null;
    recommendation: {
      outcome: string;
      decisionText: string;
      flags: string[];
    } | null;
  };
  oulad: {
    rowCounts: { snapshots: number; students: number };
    weekMin: number | null;
    weekMax: number | null;
    outcome: string | null;
    shortConclusion: string | null;
    grouped: { baselineRmse: number | null; leanRmse: number | null; delta: number | null };
    temporal: { baselineRmse: number | null; leanRmse: number | null; delta: number | null };
  } | null;
  limitations: string[];
  sourceArtifacts: Record<string, string>;
};

export type PlatformStatus = {
  seeded: boolean;
  studentCount: number;
  snapshotCount: number;
  explanationCaseCount: number;
  payloadSchemaVersion: string | null;
  lastImportedAt: string | null;
  sourcePayloadPath: string | null;
  sourceArtifacts: Record<string, string>;
};

export type PredictionSnapshot = {
  studentId: string;
  studentLabel: string;
  courseId: string;
  weekNumber: number;
  predictedFinalGrade: number | null;
  actualFinalGrade: number | null;
  passed: boolean | null;
  riskLevel: RiskBadge;
  riskScore: number | null;
  featureSet: string;
  source: string;
};
