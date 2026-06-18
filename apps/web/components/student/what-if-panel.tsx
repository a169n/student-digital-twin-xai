import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { formatNumber, formatSigned } from "@/lib/platform/format";
import type { ExplanationContribution, ExplanationSummary } from "@/lib/platform/types";

function WhatIfRow({ contribution }: { contribution: ExplanationContribution }) {
  const gain = Math.abs(contribution.contribution);
  return (
    <div className="what-if-row">
      <div className="what-if-row__label">
        <strong>{contribution.featureLabel}</strong>
        <span>
          now {formatNumber(contribution.value, 2)} → median{" "}
          {formatNumber(contribution.referenceMedian, 2)}
        </span>
      </div>
      <div className="what-if-row__gain">
        <span className="what-if-row__arrow">↑</span>
        <strong>{formatSigned(gain, 2)} pts</strong>
      </div>
    </div>
  );
}

export function WhatIfPanel({ explanation }: { explanation: ExplanationSummary }) {
  const actionable = explanation.topNegative.filter(
    (c) => c.value !== null && c.referenceMedian !== null && c.value < (c.referenceMedian ?? 0)
  );

  if (actionable.length === 0) return null;

  const candidates = actionable.slice(0, 3);
  const totalGain = candidates.reduce((sum, c) => sum + Math.abs(c.contribution), 0);
  const baseline = explanation.predictedFinalGrade ?? 0;

  return (
    <Card className="what-if-panel">
      <CardHeader>
        <CardTitle>Counterfactual scenarios · what-if analysis</CardTitle>
        <CardDescription>
          Estimated change in predicted grade if flagged factors reached cohort median. Derived from
          local SHAP contributions — approximate, not causal.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        {candidates.map((c) => (
          <WhatIfRow key={c.feature} contribution={c} />
        ))}
        <p className="what-if-panel__summary">
          If all flagged factors reached median: estimated gain{" "}
          <strong>{formatSigned(totalGain, 2)} pts</strong> — predicted grade{" "}
          <strong>{formatNumber(baseline, 1)}</strong> →{" "}
          <strong>{formatNumber(baseline + totalGain, 1)}</strong>.
        </p>
      </CardContent>
    </Card>
  );
}
