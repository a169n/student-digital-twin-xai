import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
import { formatNumber, formatSigned } from "@/lib/platform/format";
import { tryLoadResearchEvidence } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function AdminModelPage() {
  const research = await tryLoadResearchEvidence();

  if (!research || !research.leanTwin || !research.oulad) {
    return <PlatformUnavailableNotice />;
  }

  return (
    <>
      <section className="section">
        <div className="section__heading">
          <h2>Model &amp; evaluation</h2>
          <p className="muted">
            Frozen evidence base for the lean mastery-centered Twin
            (<code>B_lms_plus_mastery</code>): regression accuracy, the held-out pass-risk
            classifier, the OULAD external benchmark, and the caveats that bound every claim.
          </p>
        </div>
        <div className="hero-metrics">
          <div>
            <span>Lean RMSE</span>
            <strong>{formatNumber(research.leanTwin.leanRmse, 3)}</strong>
          </div>
          <div>
            <span>Δ vs B_lms</span>
            <strong>{formatSigned(research.leanTwin.leanDelta, 3)}</strong>
          </div>
          <div>
            <span>OULAD primary Δ</span>
            <strong>{formatSigned(research.oulad.grouped.delta, 3)}</strong>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>Claim guardrails</h2>
          <p className="muted">What this model can show, and what it must not overclaim.</p>
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <Card>
            <CardHeader>
              <CardDescription>Pass-risk classifier</CardDescription>
              <CardTitle>F1 &asymp; 0.861 · ROC-AUC &asymp; 0.953</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                Pass-risk is a held-out classifier on real OULAD data (F1 &asymp; 0.861, ROC-AUC
                &asymp; 0.953, never 1.000). The schema-controlled synthetic course is retained only
                as a controlled faithfulness probe, not as primary evidence.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardDescription>Target circularity</CardDescription>
              <CardTitle>Synthetic target is not independent</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                In the synthetic course the final grade is a deterministic function of the
                model&rsquo;s own features, so synthetic regression accuracy is not evidence of
                generalization. Only the real OULAD results are treated as external evidence.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardDescription>OULAD transfer</CardDescription>
              <CardTitle>Mixed external evidence</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                The lean analogue improves the temporal split but not the primary grouped split, so
                transfer remains a caveat.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardDescription>Interventions</CardDescription>
              <CardTitle>No causal scenario claim</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                The model is predictive and explanatory only. It is not causal: it does not simulate
                teacher actions or claim that any intervention changes an outcome.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      <section className="section">
        <div className="section__heading">
          <h2>Experiment sequence</h2>
          <p className="muted">Frozen public-first evidence chain.</p>
        </div>
        <ol className="timeline-list">
          {research.timeline.map((item) => (
            <li key={item.id} className="timeline-list__item">
              <span className="timeline-list__tag">{item.id}</span>
              <div>
                <h3>{item.title}</h3>
                <p>{item.result}</p>
                <strong>{item.decision}</strong>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="section">
        <Card>
          <CardHeader>
            <CardTitle>Lean Twin carry-forward</CardTitle>
            <CardDescription>
              Why <code>B_lms_plus_mastery</code> was preferred over the full Twin and why mastery is
              kept despite redundancy with cumulative LMS scores.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
          <dl className="metric-list">
            <div>
              <dt>Baseline RMSE</dt>
              <dd>{formatNumber(research.leanTwin.baselineRmse, 3)}</dd>
            </div>
            <div>
              <dt>Lean RMSE</dt>
              <dd>{formatNumber(research.leanTwin.leanRmse, 3)}</dd>
            </div>
            <div>
              <dt>Δ vs baseline</dt>
              <dd>{formatSigned(research.leanTwin.leanDelta, 3)}</dd>
            </div>
            <div>
              <dt>Drop overall_mastery cost</dt>
              <dd>{formatSigned(research.leanTwin.withoutOverallDelta, 3)}</dd>
            </div>
          </dl>
          <p>
            Validation improved on weeks {research.leanTwin.earlyWeeksImproved.join(", ") || "—"}
            {research.leanTwin.lateWeeksImproved.length > 0
              ? ` and later weeks ${research.leanTwin.lateWeeksImproved.join(", ")}`
              : ""}
            . Flags carried forward:{" "}
            {research.leanTwin.flags.length > 0 ? research.leanTwin.flags.join("; ") : "none"}.
          </p>
          </CardContent>
        </Card>
      </section>

      <section className="section section--two-column">
        <Card>
          <CardHeader>
            <CardTitle>OULAD benchmark</CardTitle>
            <CardDescription>{research.oulad.shortConclusion}</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Split</TableHead>
                <TableHead>B_lms</TableHead>
                <TableHead>Lean</TableHead>
                <TableHead>Δ</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell>Grouped</TableCell>
                <TableCell>{formatNumber(research.oulad.grouped.baselineRmse, 3)}</TableCell>
                <TableCell>{formatNumber(research.oulad.grouped.leanRmse, 3)}</TableCell>
                <TableCell>{formatSigned(research.oulad.grouped.delta, 3)}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Temporal</TableCell>
                <TableCell>{formatNumber(research.oulad.temporal.baselineRmse, 3)}</TableCell>
                <TableCell>{formatNumber(research.oulad.temporal.leanRmse, 3)}</TableCell>
                <TableCell>{formatSigned(research.oulad.temporal.delta, 3)}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
          <p className="caveat">
            {research.oulad.rowCounts.snapshots.toLocaleString()} snapshots ·{" "}
            {research.oulad.rowCounts.students.toLocaleString()} students · weeks{" "}
            {research.oulad.weekMin}–{research.oulad.weekMax}.
          </p>
          </CardContent>
        </Card>

        <Card className="panel--caveat">
          <CardHeader>
            <CardTitle>Limitations</CardTitle>
          </CardHeader>
          <CardContent>
          <ul>
            {research.limitations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
          </CardContent>
        </Card>
      </section>

      <section className="section artifact-strip">
        <h2 className="muted">Frozen artifact backing</h2>
        <div className="artifact-strip__list">
          {Object.values(research.sourceArtifacts).map((artifact) => (
            <code key={artifact}>{artifact}</code>
          ))}
        </div>
      </section>
    </>
  );
}
