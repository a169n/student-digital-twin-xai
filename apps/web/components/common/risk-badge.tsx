import type { RiskBadge as RiskBadgeKind } from "@/lib/platform/types";

const LABELS: Record<RiskBadgeKind, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
  unknown: "Unknown"
};

export function RiskBadge({ value }: { value: RiskBadgeKind }) {
  return <span className={`risk-badge risk-badge--${value}`}>{LABELS[value]}</span>;
}
