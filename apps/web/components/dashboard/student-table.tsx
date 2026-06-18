"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import { RiskBadge } from "@/components/common/risk-badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
import { formatNumber, formatPercent } from "@/lib/platform/format";
import type { StudentSummary } from "@/lib/platform/types";

type FilterKey =
  | "all"
  | "at_risk"
  | "low_mastery"
  | "low_activity"
  | "with_explanation"
  | "no_engagement";

const FILTERS: Array<{ key: FilterKey; label: string }> = [
  { key: "all", label: "All" },
  { key: "at_risk", label: "Predicted < 60" },
  { key: "low_mastery", label: "Mastery < 60" },
  { key: "low_activity", label: "Activity < 40" },
  { key: "no_engagement", label: "No engagement" },
  { key: "with_explanation", label: "Has explanation" }
];

type SortKey = "label" | "predicted" | "actual" | "mastery" | "activity" | "risk";

const SORT_LABELS: Record<SortKey, string> = {
  label: "Student",
  predicted: "Predicted",
  actual: "Actual (retro)",
  mastery: "Mastery",
  activity: "Activity",
  risk: "Risk"
};

const PAGE_SIZE_OPTIONS = [25, 50, 100] as const;

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
    if (
      filter === "no_engagement" &&
      !(student.overallMastery === 0 && student.assignmentAverage === null)
    ) {
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
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState<number>(25);

  const visible = useMemo(() => {
    const filtered = applyFilter(students, filter, query);
    return applySort(filtered, sort, ascending);
  }, [students, filter, query, sort, ascending]);

  const filterCounts = useMemo(() => {
    return FILTERS.reduce(
      (acc, option) => {
        acc[option.key] = applyFilter(students, option.key, "").length;
        return acc;
      },
      {} as Record<FilterKey, number>
    );
  }, [students]);

  useEffect(() => {
    setPage(1);
  }, [filter, query, sort, ascending, pageSize]);

  const pageCount = Math.max(1, Math.ceil(visible.length / pageSize));
  const currentPage = Math.min(page, pageCount);
  const startIndex = (currentPage - 1) * pageSize;
  const paged = visible.slice(startIndex, startIndex + pageSize);
  const rangeStart = visible.length === 0 ? 0 : startIndex + 1;
  const rangeEnd = Math.min(startIndex + pageSize, visible.length);

  const toggleSort = (key: SortKey) => {
    if (key === sort) {
      setAscending((prev) => !prev);
    } else {
      setSort(key);
      setAscending(key === "label" ? true : false);
    }
  };

  const sortKeys = Object.keys(SORT_LABELS) as SortKey[];

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex flex-wrap gap-2" role="tablist">
          {FILTERS.map((option) => (
            <button
              type="button"
              key={option.key}
              aria-pressed={filter === option.key}
              onClick={() => setFilter(option.key)}
              className={["filter-chip", filter === option.key ? "filter-chip--active" : ""].join(
                " "
              )}
            >
              <span>{option.label}</span>
              <strong className="filter-chip__count">{filterCounts[option.key]}</strong>
            </button>
          ))}
        </div>
        <Input
          className="h-8 lg:max-w-xs"
          type="search"
          placeholder="Search by student label, code, cohort..."
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </div>
      <div className="text-xs text-muted-foreground">
        Showing {rangeStart}–{rangeEnd} of {visible.length}
        {visible.length === students.length
          ? " students"
          : ` filtered (of ${students.length} total)`}
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            {sortKeys.map((key) => (
              <TableHead key={key}>
                <button
                  type="button"
                  className="inline-flex items-center font-medium text-foreground hover:text-primary"
                  onClick={() => toggleSort(key)}
                >
                  {SORT_LABELS[key]}
                  {sort === key ? (ascending ? " ↑" : " ↓") : ""}
                </button>
              </TableHead>
            ))}
            <TableHead>Top factors</TableHead>
            <TableHead />
          </TableRow>
        </TableHeader>
        <TableBody>
          {paged.map((student) => (
            <TableRow key={student.studentId}>
              <TableCell>
                <div className="flex flex-col">
                  <strong>{student.studentLabel}</strong>
                  <span className="text-xs text-muted-foreground">{student.studentId}</span>
                </div>
              </TableCell>
              <TableCell>{formatNumber(student.predictedFinalGrade, 1)}</TableCell>
              <TableCell>{formatNumber(student.actualFinalGrade, 1)}</TableCell>
              <TableCell>{formatNumber(student.overallMastery, 1)}</TableCell>
              <TableCell>{formatNumber(student.activityScore, 1)}</TableCell>
              <TableCell>
                <RiskBadge value={student.riskBadge} />
              </TableCell>
              <TableCell>
                {student.topExplanationFactors.length === 0 ? (
                  <span className="text-muted-foreground">—</span>
                ) : (
                  <div className="flex flex-wrap gap-1">
                    {student.topExplanationFactors.map((factor) => (
                      <span
                        key={factor.feature}
                        className="inline-flex items-center rounded-md px-1.5 py-0.5 text-xs"
                        style={
                          factor.direction === "raises_prediction"
                            ? { background: "var(--success-soft)", color: "var(--success)" }
                            : { background: "var(--danger-soft)", color: "var(--danger)" }
                        }
                      >
                        {factor.featureLabel}
                      </span>
                    ))}
                  </div>
                )}
              </TableCell>
              <TableCell>
                <Button
                  render={<Link href={`/students/${student.studentId}`} />}
                  variant="link"
                  size="sm"
                >
                  Open twin →
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {visible.length > 0 ? (
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <label className="flex items-center gap-2 text-xs text-muted-foreground">
            Rows per page
            <select
              className="h-7 rounded-md border border-border bg-background px-2 text-xs text-foreground"
              value={pageSize}
              onChange={(event) => setPageSize(Number(event.target.value))}
            >
              {PAGE_SIZE_OPTIONS.map((size) => (
                <option key={size} value={size}>
                  {size}
                </option>
              ))}
            </select>
          </label>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={currentPage <= 1}
              onClick={() => setPage(Math.max(1, currentPage - 1))}
            >
              ← Prev
            </Button>
            <span className="text-xs text-muted-foreground">
              Page {currentPage} of {pageCount}
            </span>
            <Button
              variant="outline"
              size="sm"
              disabled={currentPage >= pageCount}
              onClick={() => setPage(Math.min(pageCount, currentPage + 1))}
            >
              Next →
            </Button>
          </div>
        </div>
      ) : null}
      {visible.length === 0 ? (
        <p className="text-sm text-muted-foreground">No students match the current filters.</p>
      ) : null}
      <p className="text-xs text-muted-foreground">
        Attendance values like {formatPercent(0.65)} are 0–1 ratios. Predicted grades come from the
        frozen lean Twin model; actual final grades are retrospective evaluation fields.
      </p>
    </div>
  );
}
