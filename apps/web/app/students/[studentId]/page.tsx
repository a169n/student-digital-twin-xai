import Link from "next/link";
import { notFound } from "next/navigation";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
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
      label: "Heuristic risk score",
      value: formatNumber(detail.riskScore, 2)
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
                Trajectory · {detail.trajectoryLabel}
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

      <section className="section latest-state">
        <article className="panel latest-state__main">
          <h2>Latest state for week {detail.currentWeek}</h2>
          <p>
            The current Twin projects a final grade of{" "}
            <strong>{formatNumber(detail.predictedFinalGrade, 1)}</strong> with a{" "}
            <strong>{detail.riskBadge}</strong> heuristic risk label. Overall mastery is{" "}
            <strong>{formatNumber(detail.overallMastery, 1)}</strong>, activity is{" "}
            <strong>{formatNumber(detail.activityScore, 1)}</strong>, and attendance is{" "}
            <strong>{formatPercent(detail.attendanceRate)}</strong>.
          </p>
          {detail.explanation ? (
            <p className="muted">
              An explanation is available for this student:{" "}
              <strong>{detail.explanation.caseTypeLabel}</strong>. The explanation below links the
              model factors to the same week-{detail.explanation.weekNumber} snapshot.
            </p>
          ) : (
            <p className="muted">
              No explanation case is available for this student.
            </p>
          )}
        </article>
        <article className="panel latest-state__guardrail">
          <h2>How to read this</h2>
          <p>
            Predicted grade is an AI-assisted estimate to guide attention — not a final judgment. The
            recorded outcome is shown for context only.
          </p>
        </article>
      </section>

      <section className="section section--two-thirds">
        <article className="panel">
          <TimelineChart
            timeline={detail.timeline}
            title="Prediction, mastery, activity, and risk trajectory"
          />
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
                <th>Risk score</th>
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
                  <td>{formatNumber(row.riskScore, 2)}</td>
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
            <h3>No explanation available for this student</h3>
            <p className="muted">
              This student does not have a local explanation case.
            </p>
          </article>
        )}
      </section>

      <footer className="page-footer">
        <p>
          Predictions, mastery, risk, and explanation factors reflect the current week snapshot.
        </p>
      </footer>
    </main>
  );
}
