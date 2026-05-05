import Link from "next/link";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { ResearchBanner } from "@/components/common/research-banner";
import { formatNumber } from "@/lib/platform/format";
import { tryLoadDashboard, tryLoadResearchEvidence } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const [dashboard, research] = await Promise.all([tryLoadDashboard(), tryLoadResearchEvidence()]);

  if (!dashboard || !research) {
    return (
      <main className="page page--home">
        <PlatformUnavailableNotice />
      </main>
    );
  }

  const { cohort } = dashboard;

  return (
    <main className="page page--home">
      <ResearchBanner />
      <section className="hero">
        <p className="eyebrow">Student Digital Twin · XAI research platform</p>
        <h1>A teacher-facing view of the lean Twin and its model-behavior explanations.</h1>
        <p className="hero__lede">
          The system you see here is a minimal research platform seeded from frozen evidence.
          Predictions come from <code>B_lms_plus_mastery</code> on a synthetic 10-week course; the
          XAI panel uses the same lean Twin model. Nothing is retrained from this UI.
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
            <span>OULAD outcome</span>
            <strong>{research.oulad?.outcome ?? "-"}</strong>
          </div>
        </div>
      </section>
    </main>
  );
}
