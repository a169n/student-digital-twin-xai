import { verdictLabel } from "@/lib/review/format";
import type { Verdict } from "@/lib/review/types";

// Teal and amber, never red: an unstable explanation is a reason for caution,
// not an alarm about the student.
export function VerdictChip({ verdict }: { verdict: Verdict }) {
  return <span className={`verdict-chip is-${verdict}`}>{verdictLabel(verdict)}</span>;
}
