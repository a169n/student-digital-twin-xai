// Pure copy and number formatting for the review screen. No imports, so the
// node:test suite can load it directly with type stripping.

export const REVIEW_ACTIONS = [
  "contact_student",
  "keep_monitoring",
  "no_action_needed",
  "factor_looks_wrong"
] as const;

const ACTION_LABELS: Record<(typeof REVIEW_ACTIONS)[number], string> = {
  contact_student: "Contact the student",
  keep_monitoring: "Keep monitoring",
  no_action_needed: "No action needed",
  factor_looks_wrong: "A factor looks wrong"
};

export function actionLabel(action: (typeof REVIEW_ACTIONS)[number]): string {
  return ACTION_LABELS[action];
}

export function verdictLabel(verdict: "stable" | "unstable"): string {
  return verdict === "stable" ? "Stable explanation" : "Unstable explanation";
}

export function directionLabel(direction: "raises_risk" | "lowers_risk" | "no_effect"): string {
  // "Pushes the estimate", not "raises risk": the push is relative to the
  // model's average case and depends on the other factors, so a low value can
  // push the estimate down; "raises risk" next to a median invites a causal read.
  if (direction === "raises_risk") return "pushes the estimate up";
  if (direction === "lowers_risk") return "pushes the estimate down";
  return "no push either way";
}

export function formatPercent(share: number): string {
  return `${Math.max(Math.round(share * 100), share > 0 ? 1 : 0)}%`;
}

// Only strictly lower risks count as "higher than"; a large block of students
// with the identical estimate (often those with no activity at all) is named.
export function riskHeadline(
  risk: number,
  belowPct: number,
  tiedPct: number,
  rankedStudents: number
): string {
  const head = `${formatPercent(risk)} risk of not passing. Higher than for ${formatPercent(belowPct)} of the ${rankedStudents} students assessed in this course`;
  return tiedPct >= 0.05
    ? `${head}; ${formatPercent(tiedPct)} have the same estimate.`
    : `${head}.`;
}

export function recomputationSummary(items: { label: string; count: number }[]): string {
  return items.map((item) => `${item.label} ×${item.count}`).join(", ");
}

// Where the needle's value label sits relative to the needle, so it never
// spills past either end of the 0-1 scale.
export function needleAlign(tau: number): "start" | "center" | "end" {
  if (tau < 0.06) return "start";
  if (tau > 0.94) return "end";
  return "center";
}
