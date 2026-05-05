"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

import { RiskBadge } from "@/components/common/risk-badge";
import { formatNumber, formatPercent } from "@/lib/platform/format";
import type { StudentSummary } from "@/lib/platform/types";

type FilterKey = "all" | "at_risk" | "low_mastery" | "low_activity" | "with_explanation";

const FILTERS: Array<{ key: FilterKey; label: string }> = [
  { key: "all", label: "All" },
  { key: "at_risk", label: "Predicted < 60" },
  { key: "low_mastery", label: "Mastery < 60" },
  { key: "low_activity", label: "Activity < 40" },
  { key: "with_explanation", label: "Has explanation" }
];

type SortKey = "label" | "predicted" | "actual" | "mastery" | "activity" | "risk";

const SORT_LABELS: Record<SortKey, string> = {
  label: "Student",
  predicted: "Predicted",
  actual: "Actual",
  mastery: "Mastery",
  activity: "Activity",
  risk: "Risk"
};

function applyFilter(
  students: StudentSummary[],
  filter: FilterKey,
  query: string
): StudentSummary[] {
  const trimmed = query.trim().toLowerCase();
  return students.filter((student) => {
    if (trimmed) {
      const haystack = [
        student.studentLabel,
        student.studentId,
        student.cohortLabel,
        student.trajectoryLabel
      ]
        .filter((s): s is string => Boolean(s))
        .join(" ")
        .toLowerCase();
      if (!haystack.includes(trimmed)) return false;
    }
    if (
      filter === "at_risk" &&
      (student.predictedFinalGrade === null || student.predictedFinalGrade >= 60)
    ) {
      return false;
    }
    if (
      filter === "low_mastery" &&
      (student.overallMastery === null || student.overallMastery >= 60)
    ) {
      return false;
    }
    if (
      filter === "low_activity" &&
      (student.activityScore === null || student.activityScore >= 40)
    ) {
      return false;
    }
    if (filter === "with_explanation" && !student.hasExplanation) {
      return false;
    }
    return true;
  });
}

function compareNullable(a: number | null, b: number | null, direction: 1 | -1): number {
  if (a === null && b === null) return 0;
  if (a === null) return 1;
  if (b === null) return -1;
  return (a - b) * direction;
}

function applySort(
  students: StudentSummary[],
  sort: SortKey,
  ascending: boolean
): StudentSummary[] {
  const direction = ascending ? 1 : -1;
  const out = [...students];
  out.sort((a, b) => {
    switch (sort) {
      case "label":
        return a.studentLabel.localeCompare(b.studentLabel) * direction;
      case "predicted":
        return compareNullable(a.predictedFinalGrade, b.predictedFinalGrade, direction);
      case "actual":
        return compareNullable(a.actualFinalGrade, b.actualFinalGrade, direction);
      case "mastery":
        return compareNullable(a.overallMastery, b.overallMastery, direction);
      case "activity":
        return compareNullable(a.activityScore, b.activityScore, direction);
      case "risk": {
        const order: Record<string, number> = {
          high: 0,
          medium: 1,
          low: 2,
          unknown: 3
        };
        return (order[a.riskBadge] - order[b.riskBadge]) * direction;
      }
      default:
        return 0;
    }
  });
  return out;
}

export function StudentTable({ students }: { students: StudentSummary[] }) {
  const [filter, setFilter] = useState<FilterKey>("all");
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState<SortKey>("predicted");
  const [ascending, setAscending] = useState(true);

  const visible = useMemo(() => {
    const filtered = applyFilter(students, filter, query);
    return applySort(filtered, sort, ascending);
  }, [students, filter, query, sort, ascending]);

  const toggleSort = (key: SortKey) => {
    if (key === sort) {
      setAscending((prev) => !prev);
    } else {
      setSort(key);
      setAscending(key === "label" ? true : false);
    }
  };

  return (
    <div className="student-table">
      <div className="student-table__controls">
        <div className="student-table__filters" role="tablist">
          {FILTERS.map((option) => (
            <button
              type="button"
              key={option.key}
              className={
                "student-table__chip" +
                (filter === option.key ? " student-table__chip--active" : "")
              }
              onClick={() => setFilter(option.key)}
            >
              {option.label}
            </button>
          ))}
        </div>
        <input
          className="student-table__search"
          type="search"
          placeholder="Search by student label, code, cohort..."
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </div>
      <div className="student-table__meta">
        Showing {visible.length} of {students.length} students
      </div>
      <table>
        <thead>
          <tr>
            {(Object.keys(SORT_LABELS) as SortKey[]).map((key) => (
              <th key={key}>
                <button
                  type="button"
                  className="student-table__sort"
                  onClick={() => toggleSort(key)}
                >
                  {SORT_LABELS[key]}
                  {sort === key ? (ascending ? " ↑" : " ↓") : ""}
                </button>
              </th>
            ))}
            <th>Top factors</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {visible.map((student) => (
            <tr key={student.studentId}>
              <td>
                <div className="student-table__label">
                  <strong>{student.studentLabel}</strong>
                  <span>{student.studentId}</span>
                </div>
              </td>
              <td>{formatNumber(student.predictedFinalGrade, 1)}</td>
              <td>{formatNumber(student.actualFinalGrade, 1)}</td>
              <td>{formatNumber(student.overallMastery, 1)}</td>
              <td>{formatNumber(student.activityScore, 1)}</td>
              <td>
                <RiskBadge value={student.riskBadge} />
              </td>
              <td className="student-table__factors">
                {student.topExplanationFactors.length === 0 ? (
                  <span className="muted">—</span>
                ) : (
                  student.topExplanationFactors.map((factor) => (
                    <span
                      key={factor.feature}
                      className={
                        "student-table__factor" +
                        (factor.direction === "raises_prediction"
                          ? " student-table__factor--up"
                          : " student-table__factor--down")
                      }
                    >
                      {factor.featureLabel}
                    </span>
                  ))
                )}
              </td>
              <td>
                <Link href={`/students/${student.studentId}`} className="student-table__cta">
                  Open twin →
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {visible.length === 0 ? (
        <p className="student-table__empty">No students match the current filters.</p>
      ) : null}
      <p className="student-table__caveat">
        Attendance values like {formatPercent(0.65)} are 0–1 ratios. Predicted grades come from the
        frozen lean Twin model.
      </p>
    </div>
  );
}
