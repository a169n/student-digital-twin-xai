import Link from "next/link";
import { notFound } from "next/navigation";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { ResearchBanner } from "@/components/common/research-banner";
import { RiskBadge } from "@/components/common/risk-badge";
import { ExplanationPanel } from "@/components/student/explanation-panel";
import { TimelineChart } from "@/components/student/timeline-chart";
import { formatNumber, formatPercent, formatSigned } from "@/lib/platform/format";
import { tryLoadStudentDetail } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

type Params = { studentId: string };

export default async function StudentDetailPage({ params }: { params: Params }) {
  const detail = await tryLoadStudentDetail(params.studentId);
  if (!detail) {
    return (
      <main className="page">
        <PlatformUnavailableNotice />
      </main>
    );
  }

  if (detail.studentId !== params.studentId) {
    notFound();
  }

  const summaryCards = [
    {
      label: "Predicted final grade",
      value: formatNumber(detail.predictedFinalGrade, 1)
    },
    {
      label: "Actual final grade",
      value: formatNumber(detail.actualFinalGrade, 1)
    },
    {
      label: "Overall mastery",
      value: formatNumber(detail.overallMastery, 1)
    },
    {
      label: "Activity score",
      value: formatNumber(detail.activityScore, 1)
    },
    {
      label: "Attendance",
      value: formatPercent(detail.attendanceRate)
    },
    {
      label: "Assignment avg",
      value: formatNumber(detail.assignmentAverage, 1)
    },
    {
      label: "Quiz avg",
      value: formatNumber(detail.quizAverage, 1)
    },
    {
      label: "3-week trend",
      value: formatSigned(detail.scoreTrend3w, 3)
    }
  ];

  return (
    <main className="page page--student">
      <ResearchBanner />

      <header className="page-header page-header--student">
        <div>
          <p className="eyebrow">Student Twin · {detail.courseId}</p>
          <h1>{detail.studentLabel}</h1>
          <div className="page-header__chips">
            <RiskBadge value={detail.riskBadge} />
            <span className="chip">Week {detail.currentWeek}</span>
            {detail.cohortLabel ? <span className="chip">Cohort {detail.cohortLabel}</span> : null}
            {detail.trajectoryLabel ? (
              <span className="chip chip--muted">
                Generation trajectory · {detail.trajectoryLabel}
              </span>
            ) : null}
          </div>
        </div>
        <div className="page-header__actions">
          <Link href="/dashboard" className="page-header__secondary">
            ← Back to dashboard
          </Link>
        </div>
      </header>

      <section className="summary-cards">
        {summaryCards.map((card) => (
          <div className="summary-card" key={card.label}>
            <span className="summary-card__label">{card.label}</span>
            <strong className="summary-card__value">{card.value}</strong>
          </div>
        ))}
      </section>

      <section className="section section--two-thirds">
        <article className="panel">
          <TimelineChart timeline={detail.timeline} />
        </article>
        <article className="panel">
          <h3>Weekly snapshots</h3>
          <table className="weekly-table">
            <thead>
              <tr>
                <th>Wk</th>
                <th>Pred</th>
                <th>Mastery</th>
                <th>Activity</th>
                <th>Risk</th>
              </tr>
            </thead>
            <tbody>
              {detail.timeline.map((row) => (
                <tr key={row.weekNumber}>
                  <td>{row.weekNumber}</td>
                  <td>{formatNumber(row.predictedFinalGrade, 1)}</td>
                  <td>{formatNumber(row.overallMastery, 1)}</td>
                  <td>{formatNumber(row.activityScore, 1)}</td>
                  <td>
                    <RiskBadge value={row.riskLevel} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>
      </section>

      <section className="section">
        {detail.explanation ? (
          <ExplanationPanel explanation={detail.explanation} />
        ) : (
          <article className="panel">
            <h3>No frozen explanation case for this student</h3>
            <p className="muted">
              The XAI experiment (<code>exp_004_xai_on_lean_twin</code>) selected five
              representative student snapshots — one per case archetype. This student is not one of
              those archetypes, so no local perturbation explanation is materialized in the frozen
              artifacts. Global drivers from the lean Twin permutation analysis are available on the{" "}
              <Link href="/research-demo">research overview</Link>.
            </p>
          </article>
        )}
      </section>

      <footer className="page-footer">
        <p>
          This Twin view is a read-only projection of frozen data. The model is not retrained from
          the UI; predictions, mastery, and risk are served through the FastAPI application store
          seeded from the frozen artifacts.
        </p>
      </footer>
    </main>
  );
}
