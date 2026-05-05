import {
  formatNumber,
  formatSigned,
  loadResearchDemoData
} from "@/lib/research-demo/artifacts";

export const dynamic = "force-static";

function featureLabel(name: string) {
  return name.replaceAll("_", " ");
}

export default function ResearchDemoPage() {
  const data = loadResearchDemoData();
  const caseItem = data.highlightedCase;
  const maxContribution = Math.max(
    ...caseItem.lean_top_contributions.map((item) => item.abs_contribution)
  );

  return (
    <main className="research-demo">
      <section className="research-hero">
        <div>
          <p className="eyebrow">Defense demo</p>
          <h1>Student Digital Twin XAI Research Package</h1>
          <p className="hero-copy">
            A read-only view of the fixed evidence base: full Twin rejected,
            lean mastery-centered Twin carried forward with caveats, XAI retained
            as model-behavior explanation, and OULAD recorded as mixed external
            benchmark evidence.
          </p>
        </div>
        <div className="hero-metrics" aria-label="Core result metrics">
          <div>
            <span>Lean RMSE</span>
            <strong>{formatNumber(data.leanTwin.leanRmse)}</strong>
          </div>
          <div>
            <span>Delta vs B_lms</span>
            <strong>{formatSigned(data.leanTwin.deltaRmse)}</strong>
          </div>
          <div>
            <span>OULAD primary delta</span>
            <strong>{formatSigned(data.oulad.grouped.delta)}</strong>
          </div>
        </div>
      </section>

      <section className="research-section">
        <div className="section-heading">
          <p className="eyebrow">Experiment sequence</p>
          <h2>Fixed Evidence Chain</h2>
        </div>
        <div className="timeline-grid">
          {data.timeline.map((item) => (
            <article className="panel timeline-panel" key={item.id}>
              <span className="tag">{item.id}</span>
              <h3>{item.title}</h3>
              <p>{item.result}</p>
              <strong>{item.decision}</strong>
            </article>
          ))}
        </div>
      </section>

      <section className="research-section two-column">
        <article className="panel">
          <p className="eyebrow">Lean Twin conclusion</p>
          <h2>B_lms_plus_mastery</h2>
          <dl className="metric-list">
            <div>
              <dt>B_lms RMSE</dt>
              <dd>{formatNumber(data.leanTwin.baselineRmse)}</dd>
            </div>
            <div>
              <dt>Lean Twin RMSE</dt>
              <dd>{formatNumber(data.leanTwin.leanRmse)}</dd>
            </div>
            <div>
              <dt>Drop overall_mastery cost</dt>
              <dd>{formatSigned(data.leanTwin.withoutOverallDelta)}</dd>
            </div>
          </dl>
          <p className="body-note">
            The candidate improved weeks {data.leanTwin.earlyWeeks.join(", ")}
            {data.leanTwin.laterWeeks.length > 0
              ? ` and later weeks ${data.leanTwin.laterWeeks.join(", ")}`
              : ""}{" "}
            in the mastery validation protocol.
          </p>
        </article>

        <article className="panel">
          <p className="eyebrow">XAI result</p>
          <h2>Global Importance</h2>
          <div className="bar-list">
            {data.xai.topFeatures.map((feature) => (
              <div className="bar-row" key={feature.feature}>
                <span>{featureLabel(feature.feature)}</span>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{ width: `${Math.max(feature.importance_share * 100, 2)}%` }}
                  />
                </div>
                <strong>{formatNumber(feature.importance_share)}</strong>
              </div>
            ))}
          </div>
          <p className="body-note">
            Dominance audit outcome: {data.xai.dominance.outcome}. SHAP used:{" "}
            {data.xai.shapUsed ? "yes" : "no"}.
          </p>
        </article>
      </section>

      <section className="research-section two-column">
        <article className="panel">
          <p className="eyebrow">Student-state examples</p>
          <h2>Representative Cases</h2>
          <div className="case-list">
            {data.cases.map((item) => (
              <div className="case-row" key={`${item.student_id}-${item.case_type}`}>
                <span>{item.case_type.replaceAll("_", " ")}</span>
                <strong>
                  {item.student_id}, week {item.week_number}
                </strong>
                <em>{item.risk_level_context} risk context</em>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <p className="eyebrow">Prediction and explanation</p>
          <h2>{caseItem.case_type.replaceAll("_", " ")}</h2>
          <dl className="metric-list compact">
            <div>
              <dt>Student</dt>
              <dd>{caseItem.student_id}</dd>
            </div>
            <div>
              <dt>Actual final grade</dt>
              <dd>{formatNumber(caseItem.actual_final_grade, 2)}</dd>
            </div>
            <div>
              <dt>Predicted final grade</dt>
              <dd>{formatNumber(caseItem.predicted_final_grade, 2)}</dd>
            </div>
          </dl>
          <div className="contribution-list">
            {caseItem.lean_top_contributions.slice(0, 5).map((item) => (
              <div className="contribution-row" key={item.feature}>
                <span>{featureLabel(item.feature)}</span>
                <div className="bar-track">
                  <div
                    className={item.contribution >= 0 ? "bar-fill positive" : "bar-fill negative"}
                    style={{
                      width: `${Math.max((item.abs_contribution / maxContribution) * 100, 2)}%`
                    }}
                  />
                </div>
                <strong>{formatSigned(item.contribution, 2)}</strong>
              </div>
            ))}
          </div>
          <p className="body-note">{caseItem.teacher_meaningfulness_assessment}.</p>
        </article>
      </section>

      <section className="research-section two-column">
        <article className="panel">
          <p className="eyebrow">OULAD benchmark</p>
          <h2>Mixed External Evidence</h2>
          <table className="result-table">
            <thead>
              <tr>
                <th>Split</th>
                <th>B_lms</th>
                <th>Lean</th>
                <th>Delta</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Grouped</td>
                <td>{formatNumber(data.oulad.grouped.baseline.rmse)}</td>
                <td>{formatNumber(data.oulad.grouped.lean.rmse)}</td>
                <td>{formatSigned(data.oulad.grouped.delta)}</td>
              </tr>
              <tr>
                <td>Temporal</td>
                <td>{formatNumber(data.oulad.temporal.baseline.rmse)}</td>
                <td>{formatNumber(data.oulad.temporal.lean.rmse)}</td>
                <td>{formatSigned(data.oulad.temporal.delta)}</td>
              </tr>
            </tbody>
          </table>
          <p className="body-note">
            {data.oulad.rowCounts.snapshots.toLocaleString()} snapshots,
            {data.oulad.rowCounts.students.toLocaleString()} students, weeks{" "}
            {data.oulad.weekMin}-{data.oulad.weekMax}.
          </p>
        </article>

        <article className="panel caveat-panel">
          <p className="eyebrow">Defense caveats</p>
          <h2>Claim Discipline</h2>
          <ul>
            {data.limitations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      </section>

      <section className="research-section artifact-strip">
        <p className="eyebrow">Frozen artifact backing</p>
        <div>
          {data.sourceArtifacts.map((artifact) => (
            <code key={artifact}>{artifact}</code>
          ))}
        </div>
      </section>
    </main>
  );
}
