import { directionLabel, formatPercent, recomputationSummary } from "@/lib/review/format";
import type { ReviewCase } from "@/lib/review/types";

const fmt = (x: number) => (Number.isInteger(x) ? String(x) : x.toFixed(1));
const ARROW = { raises_risk: "↑", lowers_risk: "↓", no_effect: "–" } as const;

export function FactorList({ item }: { item: ReviewCase }) {
  const { selfTau, threshold, verdict, recomputations } = item.reliability;
  const unstable = verdict === "unstable";
  const runs = recomputations.reduce((sum, r) => sum + r.count, 0);
  return (
    <section className="review-section" aria-labelledby="factors-title">
      <h3 id="factors-title">What drives this prediction</h3>
      {unstable ? (
        <p className="review-caution" role="note">
          The ranking of all {item.features.length} activity measures shifts when it is recomputed
          (agreement {selfTau.toFixed(2)}, below {threshold.toFixed(2)}). Check below whether the
          top factor held before acting on it.
        </p>
      ) : null}
      <ol className={`factor-list${unstable ? " is-unsettled" : ""}`}>
        {item.factors.map((f) => (
          <li key={f.feature} className="factor-list__row">
            <span className={`factor-list__arrow is-${f.direction}`} aria-hidden="true">
              {ARROW[f.direction]}
            </span>
            <span className="factor-list__text">
              <span className="factor-list__label">{f.label}</span>
              <span className="factor-list__detail">
                {fmt(f.value)} for this student, course median {fmt(f.courseMedian)};{" "}
                {directionLabel(f.direction)}
              </span>
            </span>
            <span className="factor-list__weight">
              <span className="factor-list__bar" aria-hidden="true">
                <span style={{ width: `${f.share * 100}%` }} />
              </span>
              <span className="factor-list__share">{formatPercent(f.share)}</span>
            </span>
          </li>
        ))}
      </ol>
      <p className="factor-list__note">
        Percentages are each factor&apos;s share of the whole explanation (all{" "}
        {item.features.length} activity measures). A factor&apos;s push depends on the other
        factors, so a value below the course median can still push the estimate down; the median is
        there for orientation only.
      </p>
      <details className="review-details">
        <summary>Which factor came first in each of the {runs} computations</summary>
        <p>{recomputationSummary(recomputations)}.</p>
      </details>
    </section>
  );
}
