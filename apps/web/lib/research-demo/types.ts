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
  activityScore: number | null;
  assignmentAverage: number | null;
  quizAverage: number | null;
  attendanceRate: number | null;
  overallMastery: number | null;
  currentTopicMastery: number | null;
  scoreTrend3w: number | null;
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
  };
  xai: {
    method: string;
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
    };
    recommendation: {
      outcome: string;
      decisionText: string;
      flags: string[];
    };
  };
  oulad: {
    rowCounts: { snapshots: number; students: number };
    weekMin: number;
    weekMax: number;
    outcome: string;
    shortConclusion: string;
    grouped: { baselineRmse: number | null; leanRmse: number | null; delta: number | null };
    temporal: { baselineRmse: number | null; leanRmse: number | null; delta: number | null };
  };
  limitations: string[];
  sourceArtifacts: Record<string, string>;
};

export type ResearchDemoData = {
  cohort: CohortSummary;
  students: StudentSummary[];
  research: ResearchSummary;
  cases: ExplanationSummary[];
};

export type ResearchDemoPayload = {
  schemaVersion: string;
  sourceArtifacts: Record<string, string>;
  cohort: {
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
    topAtRisk: string[];
    topImproving: string[];
  };
  students: Array<{
    studentId: string;
    studentLabel: string;
    cohortLabel: string | null;
    trajectoryLabel: string | null;
    courseId: string;
    currentWeek: number;
    current: {
      predictedFinalGrade: number | null;
      riskLevel: string;
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
    };
    actualFinalGrade: number | null;
    passed: boolean | null;
    weeklyTimeline: Array<{
      weekNumber: number;
      predictedFinalGrade: number | null;
      riskLevel: string;
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
    }>;
    explanation: PayloadCase | null;
  }>;
  xai: {
    method: string;
    shapUsed: boolean;
    topGlobalFeatures: Array<{
      feature: string;
      rank: number;
      importanceShare: number;
    }>;
    dominance: {
      topFeature: string;
      top1Share: number;
      averageLocalMasteryShare: number;
      outcome: string;
      flags: string[];
    };
    metrics: {
      baselineRmse: number;
      leanRmse: number;
      leanDelta: number;
      withoutOverallDelta: number;
    };
    recommendation: {
      outcome: string;
      decisionText: string;
      flags: string[];
    };
  };
  featureDirections: Record<string, string>;
  cases: PayloadCase[];
  experiments: {
    timeline: ExperimentTimelineItem[];
    leanTwin: {
      baselineRmse: number | null;
      leanRmse: number | null;
      leanDelta: number | null;
      withoutOverallDelta: number | null;
      earlyWeeksImproved: number[];
      lateWeeksImproved: number[];
      flags: string[];
    };
    oulad: {
      rowCounts: { snapshots: number; students: number };
      weekMin: number;
      weekMax: number;
      outcome: string;
      shortConclusion: string;
      grouped: {
        baseline: { feature_set: string; model: string; rmse: number; split: string } | null;
        lean: { feature_set: string; model: string; rmse: number; split: string } | null;
        delta: number | null;
      };
      temporal: {
        baseline: { feature_set: string; model: string; rmse: number; split: string } | null;
        lean: { feature_set: string; model: string; rmse: number; split: string } | null;
        delta: number | null;
      };
    };
  };
  limitations: string[];
};

export type PayloadCase = {
  studentId: string;
  weekNumber: number;
  caseType: string;
  actualFinalGrade: number | null;
  predictedFinalGrade: number | null;
  predictionError: number | null;
  riskLevelContext: string;
  passed: boolean | null;
  masteryShare: number | null;
  teacherAssessment: string;
  topContributions: Array<{
    feature: string;
    value: number | null;
    contribution: number;
    absContribution: number;
    direction: "raises_prediction" | "lowers_prediction";
    referenceMedian: number | null;
  }>;
};
