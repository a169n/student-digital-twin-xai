export type RiskLevel = "low" | "medium" | "high" | "unknown";

export interface PredictionEnvelope {
  studentId: string;
  riskLevel: RiskLevel;
  finalGrade?: number;
  passed?: boolean;
  explanationId?: string;
  generatedAt: string;
}

export interface TwinSnapshotRef {
  twinSnapshotId: string;
  studentId: string;
  snapshotTime: string;
}
