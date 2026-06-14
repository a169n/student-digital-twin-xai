import {
  Card,
  CardContent,
  CardDescription,
  CardHeader
} from "@/components/ui/card";
import { formatNumber, formatPercent } from "@/lib/platform/format";
import type { CohortSummary } from "@/lib/platform/types";

export function CohortCards({ cohort }: { cohort: CohortSummary }) {
  const cards = [
    {
      label: "Cohort size",
      value: cohort.studentCount.toString(),
      detail: cohort.courseId ?? "Single course"
    },
    {
      label: "Mean predicted grade",
      value: formatNumber(cohort.meanPredictedFinalGrade, 1),
      detail: `Retrospective actual avg ${formatNumber(cohort.meanActualFinalGrade, 1)}`
    },
    {
      label: "Mean overall mastery",
      value: formatNumber(cohort.meanOverallMastery, 1),
      detail: `Activity ${formatNumber(cohort.meanActivityScore, 1)}`
    },
    {
      label: "Predicted below pass mark",
      value: cohort.atRiskCount.toString(),
      detail: `Mastery <60: ${cohort.lowMasteryCount} · Activity <40: ${cohort.lowActivityCount}`
    },
    {
      label: "Current risk mix",
      value: `${cohort.riskDistribution.high} high`,
      detail: `${cohort.riskDistribution.medium} medium · ${cohort.riskDistribution.low} low`
    },
    {
      label: "Attendance avg",
      value: formatPercent(cohort.meanAttendanceRate),
      detail: cohort.currentWeek != null ? `Current week ${cohort.currentWeek}` : ""
    }
  ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {cards.map((card) => (
        <Card key={card.label}>
          <CardHeader>
            <CardDescription>{card.label}</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-1">
            <strong className="text-2xl font-semibold tracking-tight">
              {card.value}
            </strong>
            {card.detail ? (
              <span className="text-xs text-muted-foreground">{card.detail}</span>
            ) : null}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
