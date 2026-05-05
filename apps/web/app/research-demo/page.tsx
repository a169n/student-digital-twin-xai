import Link from "next/link";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { ResearchBanner } from "@/components/common/research-banner";
import { formatNumber, formatSigned } from "@/lib/platform/format";
import { tryLoadExplanationCases, tryLoadResearchEvidence } from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function ResearchDemoPage() {
  const [research, cases] = await Promise.all([
    tryLoadResearchEvidence(),
    tryLoadExplanationCases()
  ]);
  if (!research || !cases || !research.leanTwin || !research.oulad || !research.xai.dominance) {
    return (
      <main className="page">
        <PlatformUnavailableNotice />
      </main>
    );
  }

  const highlightedCase = cases.find((item) => item.caseType === "at_risk") ?? cases[0] ?? null;
  const maxAbs = highlightedCase
    ? Math.max(
        ...[...highlightedCase.topPositive, ...highlightedCase.topNegative].map(
          (item) => item.absContribution
        ),
        1
      )
    : 1;

  return (
    <main className="page page--research">
      <ResearchBanner />

      <section className="research-hero">
        <div>
          <p className="eyebrow">Defense overview</p>
          <h1>From full Twin ambition to a defensible lean Twin</h1>
          <p className="page-header__lede">
            A read-only view of the frozen evidence base: the full Twin was not justified, the lean
            mastery-centered Twin (<code>B_lms_plus_mastery</code>) was carried forward with
            caveats, XAI is retained as a model-behavior signal, and the OULAD benchmark is recorded
            as mixed external evidence.
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
          <h2>Experiment sequence</h2>
          <p className="muted">Frozen evidence chain, exp_001 → exp_005.</p>
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

      <section className="section section--two-column">
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

        <article className="panel">
          <h2>XAI method and dominance audit</h2>
          <p className="muted">
            Method: <strong>{research.xai.method}</strong>. SHAP used:{" "}
            {research.xai.shapUsed ? "yes" : "no"}.
          </p>
          <div className="bar-list">
            {research.xai.topGlobalFeatures.slice(0, 6).map((feature) => (
              <div className="bar-row" key={feature.feature}>
                <span>{feature.featureLabel}</span>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{
                      width: `${Math.max(feature.importanceShare * 100, 2)}%`
                    }}
                  />
                </div>
                <strong>{formatNumber(feature.importanceShare, 3)}</strong>
              </div>
            ))}
          </div>
          <p className="caveat">
            Dominance outcome: <strong>{research.xai.dominance.outcome}</strong>. Top feature{" "}
            <code>{research.xai.dominance.topFeature}</code> holds{" "}
            {formatNumber(research.xai.dominance.top1Share, 3)} of importance share; average local
            mastery share is {formatNumber(research.xai.dominance.averageLocalMasteryShare, 3)}.
          </p>
        </article>
      </section>

      {highlightedCase ? (
        <section className="section section--two-column">
          <article className="panel">
            <h2>Representative cases</h2>
            <ul className="case-list">
              {cases.map((item) => (
                <li key={`${item.caseType}-${item.weekNumber}`}>
                  <span className="case-list__type">{item.caseTypeLabel}</span>
                  <strong>
                    Week {item.weekNumber} · pred {formatNumber(item.predictedFinalGrade, 1)} ·
                    actual {formatNumber(item.actualFinalGrade, 1)}
                  </strong>
                  <span className="muted">{item.riskLevelContext} risk context</span>
                </li>
              ))}
            </ul>
          </article>

          <article className="panel">
            <h2>{highlightedCase.caseTypeLabel} · prediction & explanation</h2>
            <p className="muted">
              Predicted {formatNumber(highlightedCase.predictedFinalGrade, 2)} · actual{" "}
              {formatNumber(highlightedCase.actualFinalGrade, 2)} · error{" "}
              {formatSigned(highlightedCase.predictionError, 2)}
            </p>
            <div className="contribution-list">
              {[...highlightedCase.topNegative, ...highlightedCase.topPositive]
                .slice(0, 5)
                .map((item) => (
                  <div className="contribution-row" key={item.feature}>
                    <div className="contribution-row__label">
                      <strong>{item.featureLabel}</strong>
                      <span>
                        value {formatNumber(item.value, 2)} / median{" "}
                        {formatNumber(item.referenceMedian, 2)}
                      </span>
                    </div>
                    <div className="contribution-row__bar">
                      <div
                        className={
                          "contribution-row__fill " +
                          (item.direction === "raises_prediction"
                            ? "contribution-row__fill--up"
                            : "contribution-row__fill--down")
                        }
                        style={{
                          width: `${Math.max((item.absContribution / maxAbs) * 100, 4)}%`
                        }}
                      />
                    </div>
                    <strong className="contribution-row__delta">
                      {formatSigned(item.contribution, 2)}
                    </strong>
                  </div>
                ))}
            </div>
            <p className="caveat">{highlightedCase.teacherAssessment}.</p>
          </article>
        </section>
      ) : null}

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
        <p className="muted">
          Open the cohort view to see how this evidence appears at the cohort and individual student
          level.
        </p>
        <div className="research-cta">
          <Link className="button" href="/dashboard">
            Open teacher dashboard
          </Link>
          <Link className="button button--ghost" href="/students">
            Browse student roster
          </Link>
        </div>
      </section>
    </main>
  );
}
