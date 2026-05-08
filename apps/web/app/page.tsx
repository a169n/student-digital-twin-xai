import Link from "next/link";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { PlatformStatusStrip } from "@/components/common/platform-status-strip";
import { ResearchBanner } from "@/components/common/research-banner";
import { formatNumber, formatSigned } from "@/lib/platform/format";
import {
  tryLoadDashboard,
  tryLoadPlatformStatus,
  tryLoadResearchEvidence
} from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const [dashboard, research, status] = await Promise.all([
    tryLoadDashboard(),
    tryLoadResearchEvidence(),
    tryLoadPlatformStatus()
  ]);

  if (!dashboard || !research) {
    return (
      <main className="page page--home">
        <PlatformUnavailableNotice />
      </main>
    );
  }

  const { cohort } = dashboard;
  const entryCards = [
    {
      eyebrow: "Cohort workflow",
      title: "Teacher dashboard",
      href: "/dashboard",
      metric: `${cohort.atRiskCount} below 60`,
      detail:
        "Triage the imported cohort, watchlists, current heuristic risk, and latest Twin state."
    },
    {
      eyebrow: "Individual Twins",
      title: "Student roster",
      href: "/students",
      metric: `${cohort.studentCount} students`,
      detail:
        "Open any student to review weekly prediction, mastery, activity, and explanation context."
    },
    {
      eyebrow: "Model outputs",
      title: "Prediction snapshots",
      href: "/predictions",
      metric: `${cohort.currentWeek ?? "-"} week view`,
      detail: "Inspect the latest imported final-grade predictions from the lean Twin feature set."
    },
    {
      eyebrow: "XAI cases",
      title: "Representative explanations",
      href: "/research-demo#representative-cases",
      metric: `${status?.explanationCaseCount ?? 0} cases`,
      detail: "Jump to the frozen local perturbation cases and link each one to its student Twin."
    },
    {
      eyebrow: "Defense evidence",
      title: "Research evidence",
      href: "/research-demo",
      metric: `Lean RMSE ${formatNumber(research.leanTwin?.leanRmse, 3)}`,
      detail:
        "Follow the experiment chain, OULAD transfer result, XAI caveats, and artifact backing."
    }
  ];

  return (
    <main className="page page--home">
      <ResearchBanner />
      <PlatformStatusStrip status={status} />
      <section className="hero">
        <p className="eyebrow">Student Digital Twin · XAI research platform</p>
        <h1>Reviewer control center for the read-only lean Twin platform.</h1>
        <p className="hero__lede">
          Frozen experiment evidence is imported into a local SQLite projection, served by FastAPI,
          and rendered as a teacher-facing workflow. Predictions come from{" "}
          <code>B_lms_plus_mastery</code>; explanations describe model behavior, not causal truth.
        </p>
        <div className="hero__cta">
          <Link className="button" href="/dashboard">
            Open teacher dashboard
          </Link>
          <Link className="button button--ghost" href="/research-demo">
            Read the research story
          </Link>
        </div>
      </section>

      <section className="section">
        <div className="hero-metrics">
          <div>
            <span>Cohort</span>
            <strong>{cohort.studentCount}</strong>
          </div>
          <div>
            <span>Mean predicted grade</span>
            <strong>{formatNumber(cohort.meanPredictedFinalGrade, 1)}</strong>
          </div>
          <div>
            <span>Lean RMSE</span>
            <strong>{formatNumber(research.leanTwin?.leanRmse, 3)}</strong>
          </div>
          <div>
            <span>Lean Δ vs B_lms</span>
            <strong>{formatSigned(research.leanTwin?.leanDelta, 3)}</strong>
          </div>
          <div>
            <span>OULAD outcome</span>
            <strong>{research.oulad?.outcome ?? "-"}</strong>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>Review paths</h2>
          <p className="muted">
            Direct entry points into the read-only platform and evidence chain.
          </p>
        </div>
        <div className="entry-grid">
          {entryCards.map((card) => (
            <Link className="entry-card" href={card.href} key={card.title}>
              <span className="entry-card__eyebrow">{card.eyebrow}</span>
              <strong>{card.title}</strong>
              <span className="entry-card__metric">{card.metric}</span>
              <p>{card.detail}</p>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
