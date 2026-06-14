import Link from "next/link";

import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { ExplanationPanel } from "@/components/student/explanation-panel";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { formatNumber } from "@/lib/platform/format";
import {
  tryLoadExplanationCases,
  tryLoadResearchEvidence
} from "@/lib/platform/loaders";

export const dynamic = "force-dynamic";

export default async function AdminExplainabilityPage() {
  const [research, cases] = await Promise.all([
    tryLoadResearchEvidence(),
    tryLoadExplanationCases()
  ]);

  if (!research || !cases) {
    return <PlatformUnavailableNotice />;
  }

  const { xai } = research;

  return (
    <>
      {/* ── Section 1: Global feature importance ── */}
      <section className="section">
        <div className="section__heading">
          <h2>Global feature importance</h2>
          <p className="muted">
            Permutation-based importance shares across the seeded OULAD cohort. These reflect
            model-behavior, not causal relationships.
          </p>
        </div>

        <div className="bar-list">
          {xai.topGlobalFeatures.map((feature) => (
            <div className="bar-row bar-row--ranked" key={feature.feature}>
              <span className="bar-row__rank">#{feature.rank}</span>
              <span className="bar-row__label">{feature.featureLabel}</span>
              <div className="bar-track">
                <div
                  className="bar-fill"
                  style={{ width: `${Math.max(feature.importanceShare * 100, 2)}%` }}
                />
              </div>
              <strong className="bar-row__value">
                {formatNumber(feature.importanceShare, 3)}
              </strong>
            </div>
          ))}
        </div>

        {xai.topGlobalFeatures.length === 0 && (
          <p className="muted">No global feature importance data available.</p>
        )}
      </section>

      {/* ── Section 2: Dominance audit ── */}
      <section className="section">
        <div className="section__heading">
          <h2>Dominance audit</h2>
          <p className="muted">
            How concentrated is the model&apos;s reliance on a single feature? A high
            top-1 share indicates the model leans heavily on one signal.
          </p>
        </div>

        <Card>
          <CardContent>
          <dl className="metric-list">
            <div>
              <dt>XAI method</dt>
              <dd>{xai.method ?? "—"}</dd>
            </div>
            <div>
              <dt>SHAP used</dt>
              <dd>{xai.shapUsed ? "Yes" : "SHAP not used"}</dd>
            </div>
            {xai.dominance ? (
              <>
                <div>
                  <dt>Top feature</dt>
                  <dd>
                    <code>{xai.dominance.topFeature}</code>
                  </dd>
                </div>
                <div>
                  <dt>Top-1 importance share</dt>
                  <dd>{formatNumber(xai.dominance.top1Share, 3)}</dd>
                </div>
                <div>
                  <dt>Average local mastery share</dt>
                  <dd>{formatNumber(xai.dominance.averageLocalMasteryShare, 3)}</dd>
                </div>
                <div>
                  <dt>Outcome</dt>
                  <dd>{xai.dominance.outcome}</dd>
                </div>
              </>
            ) : (
              <div>
                <dt>Dominance data</dt>
                <dd className="muted">Not available for this cohort.</dd>
              </div>
            )}
          </dl>

          {xai.dominance && xai.dominance.flags.length > 0 && (
            <p className="caveat">
              Flags: {xai.dominance.flags.join("; ")}.
            </p>
          )}

          <p className="caveat">
            These numbers describe model behavior on this cohort. They do not imply that
            the top feature causally drives student outcomes.
          </p>
          </CardContent>
        </Card>

        {xai.recommendation && (
          <Card className="panel--caveat mt-4">
            <CardHeader>
              <CardTitle>Recommendation</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-2">
              <p>{xai.recommendation.decisionText}</p>
              <p className="muted">Outcome: {xai.recommendation.outcome}</p>
              {xai.recommendation.flags.length > 0 && (
                <p className="caveat">Flags: {xai.recommendation.flags.join("; ")}.</p>
              )}
            </CardContent>
          </Card>
        )}
      </section>

      {/* ── Section 3: Representative cases ── */}
      <section className="section">
        <div className="section__heading">
          <h2>Representative cases</h2>
          <p className="muted">
            Local model-behavior explanations for representative students. Each panel shows
            which features push the prediction up or down for that student at that week.
          </p>
        </div>

        {cases.length === 0 ? (
          <p className="muted">No explanation cases available.</p>
        ) : (
          <div className="explanation-cases">
            {cases.map((explanationCase) => (
              <div key={`${explanationCase.studentId}-${explanationCase.caseType}-${explanationCase.weekNumber}`}>
                <div className="explanation-cases__student-link">
                  <Link href={`/students/${explanationCase.studentId}`}>
                    Open {explanationCase.studentLabel} Twin view &rarr;
                  </Link>
                </div>
                <ExplanationPanel explanation={explanationCase} />
              </div>
            ))}
          </div>
        )}
      </section>
    </>
  );
}
