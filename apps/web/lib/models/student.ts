export type RiskLevel = "low" | "medium" | "high" | "unknown";

export interface StudentTwinSummary {
  studentId: string;
  displayName?: string;
  riskLevel: RiskLevel;
  finalGrade?: number;
  passed?: boolean;
}
