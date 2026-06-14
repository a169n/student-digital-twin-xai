import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
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
        <div className="guardrail-grid">
          <article className="guardrail-card">
            <span>Pass-risk classifier</span>
            <strong>F1 &asymp; 0.861 · ROC-AUC &asymp; 0.953</strong>
            <p>
              Pass-risk is a held-out classifier on real OULAD data (F1 &asymp; 0.861, ROC-AUC
              &asymp; 0.953, never 1.000). The schema-controlled synthetic course is retained only
              as a controlled faithfulness probe, not as primary evidence.
            </p>
          </article>
          <article className="guardrail-card">
            <span>Target circularity</span>
            <strong>Synthetic target is not independent</strong>
            <p>
              In the synthetic course the final grade is a deterministic function of the model&rsquo;s
              own features, so synthetic regression accuracy is not evidence of generalization. Only
              the real OULAD results are treated as external evidence.
            </p>
          </article>
          <article className="guardrail-card">
            <span>OULAD transfer</span>
            <strong>Mixed external evidence</strong>
            <p>
              The lean analogue improves the temporal split but not the primary grouped split, so
              transfer remains a caveat.
            </p>
          </article>
          <article className="guardrail-card">
            <span>Interventions</span>
            <strong>No causal scenario claim</strong>
            <p>
              The model is predictive and explanatory only. It is not causal: it does not simulate
              teacher actions or claim that any intervention changes an outcome.
            </p>
          </article>
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
        <article className="panel">
          <h2>Lean Twin carry-forward</h2>
          <p className="muted">
            Why <code>B_lms_plus_mastery</code> was preferred over the full Twin and why mastery is
            kept despite redundancy with cumulative LMS scores.
          </p>
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
        </article>
      </section>

      <section className="section section--two-column">
        <article className="panel">
          <h2>OULAD benchmark</h2>
          <p className="muted">{research.oulad.shortConclusion}</p>
          <table className="result-table">
            <thead>
              <tr>
                <th>Split</th>
                <th>B_lms</th>
                <th>Lean</th>
                <th>Δ</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Grouped</td>
                <td>{formatNumber(research.oulad.grouped.baselineRmse, 3)}</td>
                <td>{formatNumber(research.oulad.grouped.leanRmse, 3)}</td>
                <td>{formatSigned(research.oulad.grouped.delta, 3)}</td>
              </tr>
              <tr>
                <td>Temporal</td>
                <td>{formatNumber(research.oulad.temporal.baselineRmse, 3)}</td>
                <td>{formatNumber(research.oulad.temporal.leanRmse, 3)}</td>
                <td>{formatSigned(research.oulad.temporal.delta, 3)}</td>
              </tr>
            </tbody>
          </table>
          <p className="caveat">
            {research.oulad.rowCounts.snapshots.toLocaleString()} snapshots ·{" "}
            {research.oulad.rowCounts.students.toLocaleString()} students · weeks{" "}
            {research.oulad.weekMin}–{research.oulad.weekMax}.
          </p>
        </article>

        <article className="panel panel--caveat">
          <h2>Limitations</h2>
          <ul>
            {research.limitations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
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
