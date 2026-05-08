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
    <div className="cohort-cards">
      {cards.map((card) => (
        <div className="cohort-card" key={card.label}>
          <span className="cohort-card__label">{card.label}</span>
          <strong className="cohort-card__value">{card.value}</strong>
          {card.detail ? <span className="cohort-card__detail">{card.detail}</span> : null}
        </div>
      ))}
    </div>
  );
}
