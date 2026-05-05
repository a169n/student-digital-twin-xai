"""Generate dissertation-ready figures and tables from frozen experiment artifacts.

This script is intentionally read-only with respect to experiment folders. It
reads existing JSON/CSV artifacts and writes curated SVG/Markdown outputs under
docs/dissertation/.
"""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "data" / "artifacts" / "experiments"
FIGURES = ROOT / "docs" / "dissertation" / "figures"
TABLES = ROOT / "docs" / "dissertation" / "tables"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def round3(value: float) -> str:
    return f"{value:.3f}"


def signed3(value: float) -> str:
    return f"{value:+.3f}"


def best_regression_rows(
    rows: Iterable[dict],
    *,
    target: str,
    split: str,
    order: list[str] | None = None,
) -> list[dict]:
    best: dict[str, dict] = {}
    for row in rows:
        if row.get("task") != "regression":
            continue
        if row.get("target") != target or row.get("split_strategy") != split:
            continue
        metrics = row.get("metrics") or {}
        rmse = metrics.get("rmse", row.get("metric_rmse"))
        if rmse is None:
            continue
        normalized = {
            "feature_set": row["feature_set"],
            "model": row["model"],
            "rmse": float(rmse),
            "mae": float(metrics.get("mae", row.get("metric_mae", 0))),
            "r2": float(metrics.get("r2", row.get("metric_r2", 0))),
            "split_strategy": split,
        }
        current = best.get(row["feature_set"])
        if current is None or normalized["rmse"] < current["rmse"]:
            best[row["feature_set"]] = normalized
    values = list(best.values())
    if order:
        index = {name: idx for idx, name in enumerate(order)}
        values.sort(key=lambda item: index.get(item["feature_set"], len(index)))
    else:
        values.sort(key=lambda item: item["rmse"])
    return values


def write_markdown_table(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def svg_bar_chart(
    title: str,
    subtitle: str,
    labels: list[str],
    values: list[float],
    value_label: str,
    colors: list[str] | None = None,
    width: int = 900,
    height: int | None = None,
) -> str:
    row_height = 44
    top = 88
    left = 270
    chart_width = width - left - 70
    height = height or top + row_height * len(labels) + 58
    max_value = max(values) if values else 1
    palette = colors or ["#2563eb"] * len(labels)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="24" y="34" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#111827">{html.escape(title)}</text>',
        f'<text x="24" y="58" font-family="Arial, sans-serif" font-size="13" fill="#4b5563">{html.escape(subtitle)}</text>',
    ]
    for idx, (label, value) in enumerate(zip(labels, values)):
        y = top + idx * row_height
        bar_width = 0 if max_value == 0 else value / max_value * chart_width
        color = palette[idx % len(palette)]
        parts.extend(
            [
                f'<text x="24" y="{y + 19}" font-family="Arial, sans-serif" font-size="13" fill="#111827">{html.escape(label)}</text>',
                f'<rect x="{left}" y="{y}" width="{chart_width}" height="24" fill="#f3f4f6"/>',
                f'<rect x="{left}" y="{y}" width="{bar_width:.1f}" height="24" fill="{color}"/>',
                f'<text x="{left + bar_width + 8:.1f}" y="{y + 17}" font-family="Arial, sans-serif" font-size="12" fill="#111827">{html.escape(value_label.format(value))}</text>',
            ]
        )
    parts.append("</svg>")
    return "\n".join(parts)


def svg_delta_line(title: str, subtitle: str, rows: list[dict]) -> str:
    width = 900
    height = 420
    left = 74
    right = 40
    top = 88
    bottom = 70
    chart_width = width - left - right
    chart_height = height - top - bottom
    weeks = [int(row["week"]) for row in rows]
    values = [float(row["delta_rmse_vs_baseline"]) for row in rows]
    min_value = min(values + [0])
    max_value = max(values + [0])
    pad = max((max_value - min_value) * 0.12, 0.05)
    min_axis = min_value - pad
    max_axis = max_value + pad

    def x_for(week: int) -> float:
        return left + (week - min(weeks)) / (max(weeks) - min(weeks)) * chart_width

    def y_for(value: float) -> float:
        return top + (max_axis - value) / (max_axis - min_axis) * chart_height

    points = " ".join(f"{x_for(w):.1f},{y_for(v):.1f}" for w, v in zip(weeks, values))
    zero_y = y_for(0)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="24" y="34" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#111827">{html.escape(title)}</text>',
        f'<text x="24" y="58" font-family="Arial, sans-serif" font-size="13" fill="#4b5563">{html.escape(subtitle)}</text>',
        f'<line x1="{left}" x2="{width - right}" y1="{zero_y:.1f}" y2="{zero_y:.1f}" stroke="#9ca3af" stroke-dasharray="4 4"/>',
        f'<polyline points="{points}" fill="none" stroke="#0f766e" stroke-width="3"/>',
    ]
    for week, value in zip(weeks, values):
        x = x_for(week)
        y = y_for(value)
        parts.extend(
            [
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#0f766e"/>',
                f'<text x="{x - 22:.1f}" y="{height - 38}" font-family="Arial, sans-serif" font-size="12" fill="#111827">W{week}</text>',
                f'<text x="{x - 28:.1f}" y="{y - 10:.1f}" font-family="Arial, sans-serif" font-size="12" fill="#111827">{signed3(value)}</text>',
            ]
        )
    parts.extend(
        [
            f'<text x="24" y="{top + 8}" font-family="Arial, sans-serif" font-size="12" fill="#4b5563">Delta RMSE</text>',
            f'<text x="{left}" y="{height - 16}" font-family="Arial, sans-serif" font-size="12" fill="#4b5563">Negative values favor B_lms_plus_mastery.</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts)


def svg_grouped_bars(title: str, subtitle: str, groups: list[dict]) -> str:
    width = 900
    height = 360
    left = 96
    top = 90
    chart_width = width - left - 50
    group_height = 82
    max_value = max(item["rmse"] for group in groups for item in group["items"])
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="24" y="34" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#111827">{html.escape(title)}</text>',
        f'<text x="24" y="58" font-family="Arial, sans-serif" font-size="13" fill="#4b5563">{html.escape(subtitle)}</text>',
    ]
    colors = ["#2563eb", "#0f766e"]
    for group_index, group in enumerate(groups):
        y0 = top + group_index * group_height
        parts.append(
            f'<text x="24" y="{y0 + 27}" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#111827">{html.escape(group["label"])}</text>'
        )
        for item_index, item in enumerate(group["items"]):
            y = y0 + item_index * 30
            bar_width = item["rmse"] / max_value * chart_width
            parts.extend(
                [
                    f'<rect x="{left}" y="{y}" width="{chart_width}" height="22" fill="#f3f4f6"/>',
                    f'<rect x="{left}" y="{y}" width="{bar_width:.1f}" height="22" fill="{colors[item_index]}"/>',
                    f'<text x="{left + 8}" y="{y + 16}" font-family="Arial, sans-serif" font-size="12" fill="#ffffff">{html.escape(item["feature_set"])}</text>',
                    f'<text x="{left + bar_width + 8:.1f}" y="{y + 16}" font-family="Arial, sans-serif" font-size="12" fill="#111827">{round3(item["rmse"])}</text>',
                ]
            )
    parts.append("</svg>")
    return "\n".join(parts)


def svg_sequence() -> str:
    items = [
        ("exp_001", "Full Twin not justified"),
        ("exp_002", "Lean mastery candidate"),
        ("exp_003", "Validated with redundancy caveat"),
        ("exp_004", "XAI acceptable with caveat"),
        ("exp_005", "OULAD transfer mixed"),
    ]
    width = 980
    height = 220
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="24" y="34" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#111827">Experiment Sequence</text>',
        '<text x="24" y="58" font-family="Arial, sans-serif" font-size="13" fill="#4b5563">Dependency chain for the fixed dissertation evidence base.</text>',
    ]
    box_w = 160
    gap = 30
    x = 24
    y = 90
    for idx, (label, text) in enumerate(items):
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{box_w}" height="72" rx="8" fill="#f9fafb" stroke="#d1d5db"/>',
                f'<text x="{x + 14}" y="{y + 28}" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#111827">{html.escape(label)}</text>',
                f'<text x="{x + 14}" y="{y + 51}" font-family="Arial, sans-serif" font-size="11" fill="#374151">{html.escape(text)}</text>',
            ]
        )
        if idx < len(items) - 1:
            line_x = x + box_w
            parts.extend(
                [
                    f'<line x1="{line_x}" y1="{y + 36}" x2="{line_x + gap - 8}" y2="{y + 36}" stroke="#6b7280" stroke-width="2"/>',
                    f'<polygon points="{line_x + gap - 8},{y + 36} {line_x + gap - 16},{y + 31} {line_x + gap - 16},{y + 41}" fill="#6b7280"/>',
                ]
            )
        x += box_w + gap
    parts.append("</svg>")
    return "\n".join(parts)


def generate() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    exp001 = read_json(EXPERIMENTS / "exp_001_baseline" / "baseline_v1_results.json")
    exp002 = read_json(
        EXPERIMENTS / "exp_002_twin_ablation" / "exp_002_twin_ablation_results.json"
    )
    exp003 = read_json(
        EXPERIMENTS / "exp_003_mastery_validation" / "mastery_diagnostics.json"
    )
    exp004 = read_csv(
        EXPERIMENTS / "exp_004_xai_on_lean_twin" / "global_feature_importance.csv"
    )
    exp005 = read_json(
        EXPERIMENTS
        / "exp_005_public_benchmark_oulad"
        / "exp_005_public_benchmark_oulad_results.json"
    )

    exp001_best = best_regression_rows(
        exp001["rows"],
        target="final_grade",
        split="student_group",
        order=["A_simple", "B_lms", "C_twin"],
    )
    write_markdown_table(
        TABLES / "exp_001_best_rmse.md",
        ["Feature set", "Best model", "RMSE", "MAE", "R2"],
        [
            [
                row["feature_set"],
                row["model"],
                round3(row["rmse"]),
                round3(row["mae"]),
                round3(row["r2"]),
            ]
            for row in exp001_best
        ],
    )
    (FIGURES / "exp_001_primary_rmse_comparison.svg").write_text(
        svg_bar_chart(
            "exp_001 Primary RMSE",
            "Best regression RMSE on the synthetic student-grouped split.",
            [row["feature_set"] for row in exp001_best],
            [row["rmse"] for row in exp001_best],
            "{:.3f}",
            colors=["#64748b", "#2563eb", "#dc2626"],
        ),
        encoding="utf-8",
    )

    exp002_best = best_regression_rows(
        exp002["rows"],
        target="final_grade",
        split="student_group",
        order=[
            "B_lms_plus_mastery",
            "B_lms_plus_trends_mastery",
            "B_lms_plus_indices",
            "B_lms_plus_temporal",
            "B_lms_plus_trends",
            "B_lms",
            "C_twin_full",
        ],
    )
    baseline_rmse = next(row["rmse"] for row in exp002_best if row["feature_set"] == "B_lms")
    write_markdown_table(
        TABLES / "exp_002_ablation_best_rmse.md",
        ["Feature set", "Best model", "RMSE", "Delta vs B_lms"],
        [
            [
                row["feature_set"],
                row["model"],
                round3(row["rmse"]),
                signed3(row["rmse"] - baseline_rmse),
            ]
            for row in exp002_best
        ],
    )
    (FIGURES / "exp_002_ablation_rmse_comparison.svg").write_text(
        svg_bar_chart(
            "exp_002 Twin Ablation RMSE",
            "Best regression RMSE on the primary synthetic split; lower is better.",
            [row["feature_set"] for row in exp002_best],
            [row["rmse"] for row in exp002_best],
            "{:.3f}",
            colors=[
                "#0f766e",
                "#2563eb",
                "#2563eb",
                "#2563eb",
                "#2563eb",
                "#64748b",
                "#dc2626",
            ],
            height=460,
        ),
        encoding="utf-8",
    )

    weekly_rows = exp003["weekly_validation"]["summary"]["rows"]
    write_markdown_table(
        TABLES / "exp_003_weekly_mastery_delta.md",
        ["Week", "B_lms RMSE", "B_lms_plus_mastery RMSE", "Delta"],
        [
            [
                str(row["week"]),
                round3(row["baseline_rmse"]),
                round3(row["candidate_rmse"]),
                signed3(row["delta_rmse_vs_baseline"]),
            ]
            for row in weekly_rows
        ],
    )
    (FIGURES / "exp_003_weekly_mastery_delta.svg").write_text(
        svg_delta_line(
            "exp_003 Weekly Mastery Delta",
            "B_lms_plus_mastery minus B_lms by week on the synthetic validation protocol.",
            weekly_rows,
        ),
        encoding="utf-8",
    )

    drop_rows = exp003["drop_column_tests"]["drop_results"]
    write_markdown_table(
        TABLES / "exp_003_mastery_drop_column_effect.md",
        ["Dropped column", "RMSE after drop", "Delta vs full"],
        [
            [
                row["dropped_column"],
                round3(row["rmse"]),
                signed3(row["delta_rmse_vs_full"]),
            ]
            for row in drop_rows
        ],
    )
    (FIGURES / "exp_003_mastery_drop_column_effect.svg").write_text(
        svg_bar_chart(
            "exp_003 Drop-Column Effect",
            "RMSE increase after removing mastery features from B_lms_plus_mastery.",
            [row["dropped_column"] for row in drop_rows],
            [float(row["delta_rmse_vs_full"]) for row in drop_rows],
            "+{:.3f}",
            colors=["#2563eb", "#dc2626"],
            height=230,
        ),
        encoding="utf-8",
    )

    importance_rows = [
        row
        for row in exp004
        if row["comparison_subject"] in {"baseline", "lean_twin"} and int(row["rank"]) <= 5
    ]
    write_markdown_table(
        TABLES / "exp_004_global_importance_top_features.md",
        ["Subject", "Feature set", "Rank", "Feature", "Importance share"],
        [
            [
                row["comparison_subject"],
                row["feature_set"],
                row["rank"],
                row["feature"],
                round3(float(row["importance_share"])),
            ]
            for row in importance_rows
        ],
    )
    top_by_subject: list[dict] = []
    for subject in ["baseline", "lean_twin"]:
        subject_rows = [
            row for row in importance_rows if row["comparison_subject"] == subject
        ]
        for row in subject_rows:
            top_by_subject.append(row)
    (FIGURES / "exp_004_global_importance_comparison.svg").write_text(
        svg_bar_chart(
            "exp_004 Global Importance",
            "Top-five permutation importance shares for baseline and lean Twin.",
            [
                f'{row["comparison_subject"]}: {row["feature"]}'
                for row in top_by_subject
            ],
            [float(row["importance_share"]) for row in top_by_subject],
            "{:.3f}",
            colors=["#64748b"] * 5 + ["#0f766e"] * 5,
            height=620,
        ),
        encoding="utf-8",
    )

    oulad_grouped = best_regression_rows(
        exp005["rows"],
        target="final_weighted_score",
        split="student_group",
        order=["B_lms_oulad", "B_lms_plus_mastery_oulad"],
    )
    oulad_temporal = best_regression_rows(
        exp005["rows"],
        target="final_weighted_score",
        split="temporal_forward",
        order=["B_lms_oulad", "B_lms_plus_mastery_oulad"],
    )
    oulad_rows = oulad_grouped + oulad_temporal
    split_baselines = {
        "student_group": next(row["rmse"] for row in oulad_grouped if row["feature_set"] == "B_lms_oulad"),
        "temporal_forward": next(row["rmse"] for row in oulad_temporal if row["feature_set"] == "B_lms_oulad"),
    }
    write_markdown_table(
        TABLES / "exp_005_oulad_benchmark_summary.md",
        ["Split", "Feature set", "Best model", "RMSE", "Delta vs B_lms_oulad"],
        [
            [
                row["split_strategy"],
                row["feature_set"],
                row["model"],
                round3(row["rmse"]),
                signed3(row["rmse"] - split_baselines[row["split_strategy"]]),
            ]
            for row in oulad_rows
        ],
    )
    (FIGURES / "exp_005_oulad_rmse_comparison.svg").write_text(
        svg_grouped_bars(
            "exp_005 OULAD RMSE",
            "Best regression RMSE by split; primary grouped split is mixed against the lean candidate.",
            [
                {"label": "student_group", "items": oulad_grouped},
                {"label": "temporal_forward", "items": oulad_temporal},
            ],
        ),
        encoding="utf-8",
    )

    write_markdown_table(
        TABLES / "final_experiment_sequence.md",
        ["Experiment", "Role in final package", "Decision"],
        [
            ["exp_001_baseline", "Baseline feature-set comparison", "Full Twin not justified"],
            ["exp_002_twin_ablation", "Twin subgroup ablation", "Carry B_lms_plus_mastery"],
            ["exp_003_mastery_validation", "Mastery validation", "Carry forward with redundancy caveat"],
            ["exp_004_xai_on_lean_twin", "Lean Twin XAI", "Acceptable with caveat"],
            ["exp_005_public_benchmark_oulad", "Public benchmark stress test", "Mixed transfer evidence"],
        ],
    )
    (FIGURES / "final_experiment_sequence.svg").write_text(
        svg_sequence(),
        encoding="utf-8",
    )


if __name__ == "__main__":
    generate()
