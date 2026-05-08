import type { StudentWeekRow } from "@/lib/platform/types";

type Series = {
  label: string;
  accessor: (row: StudentWeekRow) => number | null;
  color: string;
  range?: [number, number];
};

const BASE_SERIES: Series[] = [
  {
    label: "Predicted final grade",
    accessor: (row) => row.predictedFinalGrade,
    color: "#1d4ed8"
  },
  {
    label: "Overall mastery",
    accessor: (row) => row.overallMastery,
    color: "#0f766e"
  },
  {
    label: "Activity score",
    accessor: (row) => row.activityScore,
    color: "#b45309"
  },
  {
    label: "Risk score x100",
    accessor: (row) => (row.riskScore === null ? null : row.riskScore * 100),
    color: "#b91c1c"
  }
];

const VIEWBOX_WIDTH = 720;
const VIEWBOX_HEIGHT = 220;
const PADDING = { top: 18, right: 24, bottom: 28, left: 36 };

function buildPath(
  rows: StudentWeekRow[],
  accessor: (row: StudentWeekRow) => number | null,
  weekToX: (week: number) => number,
  valueToY: (value: number) => number
): string {
  let path = "";
  let started = false;
  for (const row of rows) {
    const value = accessor(row);
    if (value === null || value === undefined) continue;
    const x = weekToX(row.weekNumber);
    const y = valueToY(value);
    path += `${started ? "L" : "M"}${x.toFixed(1)},${y.toFixed(1)} `;
    started = true;
  }
  return path.trim();
}

export function TimelineChart({
  timeline,
  title = "Weekly Twin trajectory"
}: {
  timeline: StudentWeekRow[];
  title?: string;
}) {
  if (timeline.length === 0) {
    return <p className="muted">No weekly data available.</p>;
  }
  const minWeek = Math.min(...timeline.map((row) => row.weekNumber));
  const maxWeek = Math.max(...timeline.map((row) => row.weekNumber));
  const innerWidth = VIEWBOX_WIDTH - PADDING.left - PADDING.right;
  const innerHeight = VIEWBOX_HEIGHT - PADDING.top - PADDING.bottom;
  const minValue = 0;
  const maxValue = 100;

  const weekToX = (week: number) =>
    PADDING.left +
    (maxWeek === minWeek ? innerWidth / 2 : ((week - minWeek) / (maxWeek - minWeek)) * innerWidth);

  const valueToY = (value: number) =>
    PADDING.top + innerHeight - ((value - minValue) / (maxValue - minValue)) * innerHeight;

  const yTicks = [0, 25, 50, 75, 100];

  return (
    <figure className="timeline-chart" aria-label={title}>
      <figcaption className="timeline-chart__title">{title}</figcaption>
      <svg
        viewBox={`0 0 ${VIEWBOX_WIDTH} ${VIEWBOX_HEIGHT}`}
        role="img"
        preserveAspectRatio="xMidYMid meet"
      >
        {yTicks.map((tick) => {
          const y = valueToY(tick);
          return (
            <g key={tick}>
              <line
                x1={PADDING.left}
                x2={VIEWBOX_WIDTH - PADDING.right}
                y1={y}
                y2={y}
                stroke="#e5e7eb"
                strokeDasharray="3 3"
              />
              <text x={PADDING.left - 6} y={y + 4} textAnchor="end" fontSize="10" fill="#6b7280">
                {tick}
              </text>
            </g>
          );
        })}
        {timeline.map((row) => (
          <text
            key={row.weekNumber}
            x={weekToX(row.weekNumber)}
            y={VIEWBOX_HEIGHT - 8}
            textAnchor="middle"
            fontSize="10"
            fill="#6b7280"
          >
            W{row.weekNumber}
          </text>
        ))}
        {BASE_SERIES.map((series) => {
          const path = buildPath(timeline, series.accessor, weekToX, valueToY);
          if (!path) return null;
          return (
            <g key={series.label}>
              <path
                d={path}
                fill="none"
                stroke={series.color}
                strokeWidth={2}
                strokeLinejoin="round"
                strokeLinecap="round"
              />
              {timeline.map((row) => {
                const value = series.accessor(row);
                if (value === null || value === undefined) return null;
                return (
                  <circle
                    key={`${series.label}-${row.weekNumber}`}
                    cx={weekToX(row.weekNumber)}
                    cy={valueToY(value)}
                    r={3}
                    fill={series.color}
                  />
                );
              })}
            </g>
          );
        })}
      </svg>
      <ul className="timeline-chart__legend">
        {BASE_SERIES.map((series) => (
          <li key={series.label}>
            <span className="timeline-chart__swatch" style={{ backgroundColor: series.color }} />
            {series.label}
          </li>
        ))}
      </ul>
    </figure>
  );
}
