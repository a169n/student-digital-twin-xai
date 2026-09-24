import { fetchJson } from "@/lib/api/client";

import type { ReviewCaseDetail, ReviewCaseSummary } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

export async function tryLoadReviewCases(): Promise<ReviewCaseSummary[] | null> {
  try {
    return await fetchJson<ReviewCaseSummary[]>("/review/cases");
  } catch {
    return null;
  }
}

export type CaseLoad =
  | { status: "ok"; detail: ReviewCaseDetail }
  | { status: "not_found" }
  | { status: "unavailable" };

export async function tryLoadReviewCase(caseId: string): Promise<CaseLoad> {
  try {
    // redirect "manual": a path that collapses to the list endpoint must not be
    // followed and then read as a case.
    const response = await fetch(`${API_BASE_URL}/review/cases/${encodeURIComponent(caseId)}`, {
      cache: "no-store",
      redirect: "manual"
    });
    if (response.status === 404) return { status: "not_found" };
    if (!response.ok) return { status: "unavailable" };
    const detail = (await response.json()) as ReviewCaseDetail;
    return detail && typeof detail === "object" && "case" in detail
      ? { status: "ok", detail }
      : { status: "unavailable" };
  } catch {
    return { status: "unavailable" };
  }
}
