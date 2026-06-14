import Link from "next/link";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { RiskBadge } from "@/components/common/risk-badge";
import { formatNumber } from "@/lib/platform/format";
import { tryLoadDashboard } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const dashboard = await tryLoadDashboard();

  if (!dashboard) {
    return (
      <main className="page">
        <PlatformUnavailableNotice />
      </main>
    );
  }

  const { cohort } = dashboard;

  const ctaCards = [
    {
      eyebrow: "Cohort workflow",
      title: "Open cohort dashboard",
      href: "/dashboard",
      detail: "See every student at a glance — risk triage, mastery, and activity in one view."
    },
    {
      eyebrow: "Individual students",
      title: "Find a student",
      href: "/students",
      detail:
        "Search the roster, open any student profile, and review their weekly prediction history."
    },
    {
      eyebrow: "Model outputs",
      title: "This week's predictions",
      href: "/predictions",
      detail: "Browse the latest predicted final grades and risk levels for the current week."
    }
  ];

  const atRiskList = cohort.topAtRisk.slice(0, 5);

  return (
    <main className="page page--home">
      <section className="hero">
        <h1>Welcome back, Ms. Carter</h1>
        <p className="hero__lede">
          DDD 2013J &middot; Week {cohort.currentWeek ?? "—"} &middot; {cohort.studentCount}{" "}
          students
        </p>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>Where do you want to go?</h2>
          <p className="muted">Direct entry into the main teacher views.</p>
        </div>
        <div className="entry-grid">
          {ctaCards.map((card) => (
            <Link className="entry-card" href={card.href} key={card.title}>
              <span className="entry-card__eyebrow">{card.eyebrow}</span>
              <strong>{card.title}</strong>
              <p>{card.detail}</p>
            </Link>
          ))}
        </div>
      </section>

      {atRiskList.length > 0 && (
        <section className="section">
          <div className="section__heading">
            <h2>Students needing attention</h2>
            <p className="muted">
              Top {atRiskList.length} students by predicted risk this week.
            </p>
          </div>
          <div className="watchlist">
            <ol>
              {atRiskList.map((student) => (
                <li key={student.studentId}>
                  <Link href={`/students/${student.studentId}`}>
                    <strong>{student.studentLabel}</strong>
                    <span>
                      Predicted grade: {formatNumber(student.predictedFinalGrade, 1)}
                    </span>
                    <em>
                      <RiskBadge value={student.riskBadge} />
                    </em>
                  </Link>
                </li>
              ))}
            </ol>
          </div>
        </section>
      )}
    </main>
  );
}
