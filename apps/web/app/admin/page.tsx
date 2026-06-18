import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { PlatformStatusStrip } from "@/components/common/platform-status-strip";
import { CohortCards } from "@/components/dashboard/cohort-cards";
import { Card, CardContent, CardDescription, CardHeader } from "@/components/ui/card";
import { tryLoadDashboard, tryLoadPlatformStatus } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function AdminOverviewPage() {
  const [status, dashboard] = await Promise.all([tryLoadPlatformStatus(), tryLoadDashboard()]);

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
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[
            {
              label: "Schema version",
              value: status.payloadSchemaVersion ?? "unknown"
            },
            {
              label: "Last imported",
              value: status.lastImportedAt
                ? status.lastImportedAt.replace("T", " ").split(".")[0]
                : "Not imported"
            },
            { label: "Students", value: status.studentCount },
            { label: "Weekly snapshots", value: status.snapshotCount },
            {
              label: "XAI explanation cases",
              value: status.explanationCaseCount
            }
          ].map((fact) => (
            <Card key={fact.label}>
              <CardHeader>
                <CardDescription>{fact.label}</CardDescription>
              </CardHeader>
              <CardContent>
                <strong className="text-2xl font-semibold tracking-tight">{fact.value}</strong>
              </CardContent>
            </Card>
          ))}
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
