import { formatPercent, needleAlign } from "@/lib/review/format";
import type { ReviewCase, ScaleContext } from "@/lib/review/types";

import { VerdictChip } from "./verdict-chip";

type Props = { reliability: ReviewCase["reliability"]; scale: ScaleContext | null };

// Kendall tau runs from -1 to 1. The scale shows 0 to 1, where observed
// self-agreement sits, and pins anything below 0 to the left edge.
const pct = (tau: number) => `${Math.min(Math.max(tau, 0), 1) * 100}%`;

export function ReliabilityScale({ reliability, scale }: Props) {
  const { selfTau, threshold, verdict, recomputations } = reliability;
  const stable = verdict === "stable";
  const runs = recomputations.reduce((sum, r) => sum + r.count, 0);
  return (
    <section className="review-section" aria-labelledby="reliability-title">
      <div className="review-section__head">
        <h3 id="reliability-title">How repeatable is this explanation?</h3>
        <VerdictChip verdict={verdict} />
      </div>
      <p className="review-section__lede">
        {stable
          ? `Computed ${runs} times, it gives almost the same list of factors each time. Repeatable is not the same as correct.`
          : `Computed ${runs} times, the factors do not keep their order. Read the list as a rough hint.`}
      </p>
      <div
        className="reliability-scale"
        role="img"
        aria-label={`Agreement between recomputations ${selfTau.toFixed(2)} on a scale from 0 to 1; factor lists are shown as stable from ${threshold.toFixed(2)}`}
      >
        <div className="reliability-scale__track">
          <span className="reliability-scale__zone is-unstable" style={{ width: pct(threshold) }}>
            List changes
          </span>
          <span className="reliability-scale__zone is-stable">List repeats</span>
        </div>
        <span
          className="reliability-scale__cut"
          style={{ left: pct(threshold) }}
          aria-hidden="true"
        >
          <span>stable from {threshold.toFixed(2)}</span>
        </span>
        <span
          className={`reliability-scale__needle is-${verdict} align-${needleAlign(selfTau)}`}
          style={{ left: pct(selfTau) }}
          aria-hidden="true"
        >
          <span>{selfTau.toFixed(2)}</span>
        </span>
        <div className="reliability-scale__ends" aria-hidden="true">
          <span>0</span>
          <span>1</span>
        </div>
      </div>
      {scale ? (
        <details className="review-details">
          <summary>How to read this scale</summary>
          <p>
            The explanation was computed {runs} times, each time against a different sample of
            classmates. The score says how similar the orderings of all factors were: 1 means
            identical, 0 means no relation. From {scale.threshold.toFixed(2)} a list counts as
            stable; {formatPercent(scale.coverage)} of students reach it. Even stable lists only
            partly agree with a second explanation method: {scale.retainedAgreement.toFixed(2)} on
            the same scale, against {scale.noGateAgreement.toFixed(2)} without this check.
          </p>
        </details>
      ) : null}
    </section>
  );
}
