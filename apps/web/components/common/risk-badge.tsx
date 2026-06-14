import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { RiskBadge as RiskBadgeKind } from "@/lib/platform/types";

const LABELS: Record<RiskBadgeKind, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
  unknown: "Unknown"
};

const STYLES: Record<RiskBadgeKind, string> = {
  low: "border-transparent bg-[var(--success-soft)] text-[var(--success)]",
  medium: "border-transparent bg-[var(--warn-soft)] text-[var(--warn)]",
  high: "border-transparent bg-[var(--danger-soft)] text-[var(--danger)]",
  unknown: ""
};

export function RiskBadge({ value }: { value: RiskBadgeKind }) {
  return (
    <Badge
      variant={value === "unknown" ? "secondary" : "default"}
      className={cn(STYLES[value])}
    >
      {LABELS[value]}
    </Badge>
  );
}
