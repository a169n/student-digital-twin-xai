"use server";

import { revalidatePath } from "next/cache";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

export type SaveState = { error: string | null; savedAt: string | null };

// Posts from the Next.js server, so the browser never calls the API directly
// and the API needs no CORS opening.
export async function saveDecision(
  caseId: string,
  _prev: SaveState,
  formData: FormData
): Promise<SaveState> {
  const action = String(formData.get("action") ?? "");
  const factor = formData.get("factor");
  const note = formData.get("note");
  const body: Record<string, string> = { action };
  if (action === "factor_looks_wrong" && factor) body.factor = String(factor);
  if (note && String(note).trim()) body.note = String(note);
  try {
    const response = await fetch(
      `${API_BASE_URL}/review/cases/${encodeURIComponent(caseId)}/decisions`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      }
    );
    if (!response.ok) {
      const detail = await response.json().catch(() => null);
      return {
        error: `Not saved (${response.status}): ${JSON.stringify(detail?.detail ?? "")}`,
        savedAt: null
      };
    }
    revalidatePath("/review");
    return { error: null, savedAt: new Date().toISOString() };
  } catch {
    return { error: "Not saved: the API is not reachable.", savedAt: null };
  }
}
