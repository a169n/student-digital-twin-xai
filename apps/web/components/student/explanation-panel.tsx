import { formatNumber, formatSigned } from "@/lib/platform/format";
import type { ExplanationContribution, ExplanationSummary } from "@/lib/platform/types";

function ContributionRow({
  contribution,
  scale
}: {
  contribution: ExplanationContribution;
  scale: number;
}) {
  const width = Math.max((contribution.absContribution / scale) * 100, 4);
  return (
    <div className="contribution-row" key={contribution.feature}>
      <div className="contribution-row__label">
        <strong>{contribution.featureLabel}</strong>
        <span>
          value {formatNumber(contribution.value, 2)} (median{" "}
          {formatNumber(contribution.referenceMedian, 2)})
        </span>
      </div>
      <div className="contribution-row__bar">
        <div
          className={
            "contribution-row__fill " +
            (contribution.direction === "raises_prediction"
              ? "contribution-row__fill--up"
              : "contribution-row__fill--down")
          }
          style={{ width: `${width}%` }}
        />
      </div>
      <strong className="contribution-row__delta">
        {formatSigned(contribution.contribution, 2)}
      </strong>
    </div>
  );
}

export function ExplanationPanel({ explanation }: { explanation: ExplanationSummary }) {
  const allContribs = [...explanation.topPositive, ...explanation.topNegative];
  const scale = Math.max(...allContribs.map((item) => item.absContribution), 1);

  return (
    <div className="explanation-panel">
      <header className="explanation-panel__header">
        <span className="explanation-panel__case-tag">{explanation.caseTypeLabel}</span>
        <h3>Lean Twin explanation · week {explanation.weekNumber}</h3>
        <p className="muted">
          Predicted {formatNumber(explanation.predictedFinalGrade, 2)} · actual{" "}
          {formatNumber(explanation.actualFinalGrade, 2)} · error{" "}
          {formatSigned(explanation.predictionError, 2)} · risk context{" "}
          {explanation.riskLevelContext}
        </p>
      </header>

      <div className="explanation-panel__columns">
        <section>
          <h4>Top positive factors</h4>
          {explanation.topPositive.length === 0 ? (
            <p className="muted">No raising factors in the top six.</p>
          ) : (
            explanation.topPositive
              .slice(0, 4)
              .map((item) => (
                <ContributionRow key={item.feature} contribution={item} scale={scale} />
              ))
          )}
        </section>
        <section>
          <h4>Top negative factors</h4>
          {explanation.topNegative.length === 0 ? (
            <p className="muted">No lowering factors in the top six.</p>
          ) : (
            explanation.topNegative
              .slice(0, 4)
              .map((item) => (
                <ContributionRow key={item.feature} contribution={item} scale={scale} />
              ))
          )}
        </section>
      </div>

      <p className="explanation-panel__interpretation">
        <strong>Teacher-facing read.</strong> {explanation.teacherAssessment}.
      </p>

      <p className="explanation-panel__caveat">
        Explanations come from a permutation-importance + local perturbation analysis on the lean
        Twin model. They describe how the model behaves around this snapshot — they are not causal
        claims about the student.
      </p>
    </div>
  );
}
