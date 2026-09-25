import Link from "next/link";

import { formatPercent, verdictLabel } from "@/lib/review/format";
import { coursesOf } from "@/lib/review/select";
import type { ReviewCaseSummary } from "@/lib/review/types";

import { VerdictChip } from "./verdict-chip";

type Props = {
  cases: ReviewCaseSummary[];
  all: ReviewCaseSummary[];
  selectedId: string;
  institution?: string;
  course?: string;
  verdict?: string;
};

function href(params: Record<string, string | undefined>) {
  const query = new URLSearchParams(
    Object.entries(params).filter((entry): entry is [string, string] => Boolean(entry[1]))
  );
  const text = query.toString();
  return text ? `/review?${text}` : "/review";
}

export function CaseList({ cases, all, selectedId, institution, course, verdict }: Props) {
  const institutions = Array.from(new Set(all.map((c) => c.institution)));
  const courses = coursesOf(all, institution);
  return (
    <nav className="review-list" aria-label="Students to review">
      <div className="review-filters" role="group" aria-label="University">
        <Link href={href({ verdict })} aria-current={!institution ? "true" : undefined}>
          All universities
        </Link>
        {institutions.map((name) => (
          <Link
            key={name}
            href={href({ institution: name, verdict })}
            aria-current={institution === name ? "true" : undefined}
          >
            {name}
          </Link>
        ))}
      </div>
      {courses.length > 1 ? (
        <div className="review-filters" role="group" aria-label="Course">
          <Link href={href({ institution, verdict })} aria-current={!course ? "true" : undefined}>
            All courses
          </Link>
          {courses.map((name) => (
            <Link
              key={name}
              href={href({ institution, course: name, verdict })}
              aria-current={course === name ? "true" : undefined}
            >
              {name}
            </Link>
          ))}
        </div>
      ) : null}
      <div className="review-filters" role="group" aria-label="Explanation">
        {(["stable", "unstable"] as const).map((v) => (
          <Link
            key={v}
            href={href({ institution, course, verdict: verdict === v ? undefined : v })}
            aria-current={verdict === v ? "true" : undefined}
          >
            {verdictLabel(v)}
          </Link>
        ))}
      </div>
      <p className="review-list__count">
        {cases.length} of {all.length} students
      </p>
      <ul className="review-list__items">
        {cases.map((c) => (
          <li key={c.caseId}>
            <Link
              href={href({ case: c.caseId, institution, course, verdict })}
              aria-current={c.caseId === selectedId ? "page" : undefined}
              className="review-list__item"
            >
              <span className="review-list__name">{c.displayName}</span>
              <span className="review-list__risk">{formatPercent(c.risk)} risk</span>
              <span className="review-list__meta">
                {c.institution}, course {c.course}
              </span>
              <span className="review-list__status">
                <VerdictChip verdict={c.verdict} />
                {c.latestDecision ? (
                  <span className="review-list__decided">Decision saved</span>
                ) : null}
              </span>
            </Link>
          </li>
        ))}
      </ul>
      {cases.length === 0 ? <p className="muted">No students match these filters.</p> : null}
    </nav>
  );
}
