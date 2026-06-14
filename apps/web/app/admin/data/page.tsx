import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
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
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[
            {
              label: "Payload schema version",
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
            { label: "XAI explanation cases", value: status.explanationCaseCount }
          ].map((card) => (
            <Card key={card.label}>
              <CardHeader>
                <CardDescription>{card.label}</CardDescription>
              </CardHeader>
              <CardContent>
                <strong className="text-2xl font-semibold tracking-tight">{card.value}</strong>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>Cohort identity</h2>
          <p className="muted">The single real cohort backing every view in this demo.</p>
        </div>
        <Card>
          <CardHeader>
            <CardDescription>Source cohort</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <strong className="text-2xl font-semibold tracking-tight">OULAD DDD 2013J</strong>
            <p className="muted">
              Open University Learning Analytics Dataset, course module DDD, presentation 2013J.
              All snapshots, predictions, and explanation cases are seeded from this single
              real-world cohort.
            </p>
          </CardContent>
        </Card>
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
          <Card>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Artifact</TableHead>
                    <TableHead>Path</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {artifactEntries.map(([key, path]) => (
                    <TableRow key={key}>
                      <TableCell>{key}</TableCell>
                      <TableCell>
                        <code>{path}</code>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        ) : (
          <p className="muted">No source artifacts were recorded for this import.</p>
        )}
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>Fields null by design</h2>
          <p className="muted">Honest gaps in the OULAD cohort — not missing data bugs.</p>
        </div>
        <Card>
          <CardContent className="flex flex-col gap-3">
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
          </CardContent>
        </Card>
      </section>
    </>
  );
}
