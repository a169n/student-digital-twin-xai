export type ReviewAction =
  | "contact_student"
  | "keep_monitoring"
  | "no_action_needed"
  | "factor_looks_wrong";
export type Verdict = "stable" | "unstable";
export type Direction = "raises_risk" | "lowers_risk" | "no_effect";

export type ReviewDecision = {
  id: number;
  action: ReviewAction;
  factor: string | null;
  note: string | null;
  createdAt: string;
};

export type ReviewCaseSummary = {
  caseId: string;
  displayName: string;
  institution: string;
  course: string;
  risk: number;
  flagged: boolean;
  verdict: Verdict;
  selfTau: number;
  latestDecision: ReviewDecision | null;
};

export type ReviewFeature = { feature: string; label: string; value: number; courseMedian: number };
export type ReviewFactor = ReviewFeature & { direction: Direction; share: number };
export type Recomputation = { feature: string; label: string; count: number };

export type ReviewCase = {
  caseId: string;
  displayName: string;
  institution: string;
  context: {
    course: string;
    week: number;
    nWeeks: number;
    cohortSize: number;
    rankedStudents: number;
    passRate: number;
    modelAuc: number;
  };
  risk: number;
  riskRankPct: number;
  riskBelowPct: number;
  riskTiedPct: number;
  flagged: boolean;
  factors: ReviewFactor[];
  reliability: {
    selfTau: number;
    threshold: number;
    verdict: Verdict;
    recomputations: Recomputation[];
  };
  features: ReviewFeature[];
};

export type ScaleContext = {
  threshold: number;
  coverage: number;
  retainedAgreement: number;
  noGateAgreement: number;
  source: string;
};

export type ReviewCaseDetail = {
  case: ReviewCase;
  scaleContext: ScaleContext | null;
  featureLabels: Record<string, string> | null;
  decisions: ReviewDecision[];
};
