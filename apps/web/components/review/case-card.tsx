import { formatPercent, riskHeadline } from "@/lib/review/format";
import type { ReviewCaseDetail } from "@/lib/review/types";

import { DecisionForm } from "./decision-form";
import { FactorList } from "./factor-list";
import { ReliabilityScale } from "./reliability-scale";

export function CaseCard({ detail }: { detail: ReviewCaseDetail }) {
  const item = detail.case;
  const c = item.context;
  return (
    <article className="review-card" aria-labelledby="case-title">
      <header className="review-card__head">
        <h2 id="case-title">{item.displayName}</h2>
        <p className="review-card__where">
          Course {c.course} at {item.institution}, week {c.week} of {c.nWeeks}
        </p>
        <p className="review-card__risk">
          {riskHeadline(item.risk, item.riskBelowPct, item.riskTiedPct, c.rankedStudents)}
        </p>
        <p className="review-card__context">
          {c.cohortSize.toLocaleString("en-GB")} students took this course and{" "}
          {formatPercent(c.passRate)} passed. How well the model orders students on this course: AUC{" "}
          {c.modelAuc.toFixed(2)}, where 0.5 would be guessing and 1 a perfect ordering.
        </p>
      </header>
      <ReliabilityScale reliability={item.reliability} scale={detail.scaleContext} />
      <FactorList item={item} />
      <DecisionForm
        key={item.caseId}
        caseId={item.caseId}
        factors={item.factors}
        decisions={detail.decisions}
      />
    </article>
  );
}
