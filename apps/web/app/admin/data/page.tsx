import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { tryLoadPlatformStatus } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function AdminDataPage() {
  const status = await tryLoadPlatformStatus();

  if (!status) {
    return <PlatformUnavailableNotice />;
  }

  const artifactEntries = Object.entries(status.sourceArtifacts ?? {});

  return (
    <>
      <section className="section">
        <div className="section__heading">
          <h2>Data &amp; provenance</h2>
          <p className="muted">
            Where this demo&apos;s numbers come from, and what is intentionally absent.
          </p>
        </div>
        <div className="cohort-cards">
          <div className="cohort-card">
            <span className="cohort-card__label">Payload schema version</span>
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
          <h2>Cohort identity</h2>
          <p className="muted">The single real cohort backing every view in this demo.</p>
        </div>
        <div className="cohort-card">
          <span className="cohort-card__label">Source cohort</span>
          <strong className="cohort-card__value">OULAD DDD 2013J</strong>
          <p className="muted">
            Open University Learning Analytics Dataset, course module DDD, presentation 2013J.
            All snapshots, predictions, and explanation cases are seeded from this single
            real-world cohort.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>Source artifacts</h2>
          <p className="muted">
            Frozen research artifacts the local application projection was imported from.
          </p>
        </div>
        {status.sourcePayloadPath ? (
          <p className="muted">
            Imported payload: <code>{status.sourcePayloadPath}</code>
          </p>
        ) : null}
        {artifactEntries.length > 0 ? (
          <table className="result-table">
            <thead>
              <tr>
                <th>Artifact</th>
                <th>Path</th>
              </tr>
            </thead>
            <tbody>
              {artifactEntries.map(([key, path]) => (
                <tr key={key}>
                  <td>{key}</td>
                  <td>
                    <code>{path}</code>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="muted">No source artifacts were recorded for this import.</p>
        )}
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>Fields null by design</h2>
          <p className="muted">Honest gaps in the OULAD cohort — not missing data bugs.</p>
        </div>
        <div className="cohort-card">
          <p>
            OULAD has <strong>no attendance record and no quiz analog</strong>. The platform schema
            carries <code>attendanceRate</code>, <code>quizAverage</code>, and related
            attendance/quiz-trend fields for compatibility with richer course models, but for this
            cohort those fields are <strong>null by design</strong>.
          </p>
          <p className="muted">
            Engagement is represented by VLE activity and assessment scores only. Any view that
            shows these fields as empty is reflecting a true absence in the source data, not a
            failed import.
          </p>
        </div>
      </section>
    </>
  );
}
