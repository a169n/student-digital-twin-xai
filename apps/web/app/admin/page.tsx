import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { PlatformStatusStrip } from "@/components/common/platform-status-strip";
import { CohortCards } from "@/components/dashboard/cohort-cards";
import { tryLoadDashboard, tryLoadPlatformStatus } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function AdminOverviewPage() {
  const [status, dashboard] = await Promise.all([
    tryLoadPlatformStatus(),
    tryLoadDashboard(),
  ]);

  if (!status || !dashboard) {
    return <PlatformUnavailableNotice />;
  }

  return (
    <>
      <section className="section">
        <div className="section__heading">
          <h2>System health</h2>
          <p className="muted">Live provenance from the seeded research payload.</p>
        </div>
        <PlatformStatusStrip status={status} />
        <div className="cohort-cards" style={{ marginTop: "var(--space-4, 1rem)" }}>
          <div className="cohort-card">
            <span className="cohort-card__label">Schema version</span>
            <strong className="cohort-card__value">
              {status.payloadSchemaVersion ?? "unknown"}
            </strong>
          </div>
          <div className="cohort-card">
            <span className="cohort-card__label">Last imported</span>
            <strong className="cohort-card__value">
              {status.lastImportedAt
                ? status.lastImportedAt.replace("T", " ").split(".")[0]
                : "Not imported"}
            </strong>
          </div>
          <div className="cohort-card">
            <span className="cohort-card__label">Students</span>
            <strong className="cohort-card__value">{status.studentCount}</strong>
          </div>
          <div className="cohort-card">
            <span className="cohort-card__label">Weekly snapshots</span>
            <strong className="cohort-card__value">{status.snapshotCount}</strong>
          </div>
          <div className="cohort-card">
            <span className="cohort-card__label">XAI explanation cases</span>
            <strong className="cohort-card__value">{status.explanationCaseCount}</strong>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>Cohort analytics</h2>
          <p className="muted">Aggregate statistics for the seeded OULAD cohort.</p>
        </div>
        <CohortCards cohort={dashboard.cohort} />
      </section>
    </>
  );
}
