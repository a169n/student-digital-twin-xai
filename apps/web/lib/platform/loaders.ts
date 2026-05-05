import { fetchJson } from "@/lib/api/client";

import type {
  DashboardData,
  ExplanationSummary,
  PlatformStatus,
  PredictionSnapshot,
  ResearchSummary,
  StudentDetail,
  StudentSummary,
  StudentWeekRow
} from "./types";

export async function tryLoadPlatformStatus(): Promise<PlatformStatus | null> {
  return tryFetch(() => fetchJson<PlatformStatus>("/platform/status"));
}

export async function tryLoadDashboard(): Promise<DashboardData | null> {
  return tryFetch(() => fetchJson<DashboardData>("/dashboard"));
}

export async function tryLoadStudents(): Promise<StudentSummary[] | null> {
  return tryFetch(() => fetchJson<StudentSummary[]>("/students"));
}

export async function tryLoadStudentDetail(studentId: string): Promise<StudentDetail | null> {
  return tryFetch(() => fetchJson<StudentDetail>(`/students/${studentId}`));
}

export async function tryLoadStudentSnapshots(studentId: string): Promise<StudentWeekRow[] | null> {
  return tryFetch(() => fetchJson<StudentWeekRow[]>(`/twins/${studentId}/snapshots`));
}

export async function tryLoadLatestPredictions(): Promise<PredictionSnapshot[] | null> {
  const payload = await tryFetch(() =>
    fetchJson<{ predictions: PredictionSnapshot[] }>("/predictions/latest")
  );
  return payload?.predictions ?? null;
}

export async function tryLoadExplanationCases(): Promise<ExplanationSummary[] | null> {
  return tryFetch(() => fetchJson<ExplanationSummary[]>("/explanations/cases"));
}

export async function tryLoadResearchEvidence(): Promise<ResearchSummary | null> {
  return tryFetch(() => fetchJson<ResearchSummary>("/research/evidence"));
}

async function tryFetch<T>(loader: () => Promise<T>): Promise<T | null> {
  try {
    return await loader();
  } catch {
    return null;
  }
}
