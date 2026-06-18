"""Build the master-student IMWP defense presentation strictly following the
official 9-slide template (defense_presentation_per_template.pptx).

Style: strict minimalism — white background, black text, no colors, no shadows,
no decorative lines/plates. Tables: black borders only, no fill. Charts:
black/white/grayscale only.

All metrics are taken verbatim from the frozen experiment artifacts in
data/artifacts/experiments/ (no invented numbers):
  - Model comparison  : exp_013_comparison_baselines (OULAD DDD 2013J, student_group)
  - Ablation          : exp_006 (DDD 2013J) + exp_009 (BBB 2013J), gradient boosting RMSE
  - XAI stability      : exp_007 (within-DDD) + exp_010 (cross-cohort DDD vs BBB), Kendall tau
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_TICK_MARK
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "data" / "artifacts" / "presentation_assets"
ASSETS.mkdir(parents=True, exist_ok=True)
OUT_PPTX = ROOT / "defense_presentation_per_template.pptx"

# ----------------------------------------------------------------------------
# Palette (grayscale only)
# ----------------------------------------------------------------------------
BLACK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_AXIS = RGBColor(0x40, 0x40, 0x40)
GRID = RGBColor(0xD9, 0xD9, 0xD9)
# Grayscale series shades (dark -> light)
G1 = RGBColor(0x2B, 0x2B, 0x2B)
G2 = RGBColor(0x70, 0x70, 0x70)
G3 = RGBColor(0xA6, 0xA6, 0xA6)
G4 = RGBColor(0xD0, 0xD0, 0xD0)

FONT = "Calibri"

# ----------------------------------------------------------------------------
# REAL DATA (verbatim from artifacts)
# ----------------------------------------------------------------------------

# exp_013_comparison_baselines  (OULAD DDD 2013J, student_group split)
MODEL_APPROACHES = [
    "Logistic\nRegression",
    "Random\nForest",
    "Gradient Boosting\n(LMS-only)",
    "GB + Twin + XAI\n(this work)",
]
MODEL_F1 = [0.854, 0.861, 0.863, 0.861]
MODEL_AUC = [0.951, 0.947, 0.953, 0.953]
# Regression RMSE (final score 0-100); LR not used for regression here.
RMSE_APPROACHES = ["Random Forest", "GB (LMS-only)", "GB + Twin\n(this work)"]
RMSE_VALUES = [13.633, 12.658, 12.724]

# Ablation: gradient boosting regression RMSE (lower is better)
# exp_006 (DDD 2013J), exp_009 (BBB 2013J)
ABL_FEATURE_SETS = ["A_simple", "B_lms", "B_lms\n+mastery", "C_twin"]
ABL_SERIES = {
    "DDD · student-grouped": [13.866, 12.660, 12.721, 12.641],
    "DDD · temporal-forward": [13.666, 9.561, 9.180, 9.585],
    "BBB · student-grouped": [12.387, 10.697, 10.620, 10.610],
    "BBB · temporal-forward": [10.230, 6.311, 5.284, 5.546],
}

# XAI explanation stability — Kendall tau (threshold 0.90 not reached anywhere)
# Rows = feature sets; columns = comparison scenario
XAI_ROWS = ["B_lms", "B_lms+mastery", "C_twin"]
XAI_COLS = ["Within DDD\n(SG vs TF)", "Cross-cohort\n(student-grouped)", "Cross-cohort\n(temporal-forward)"]
XAI_TAU = np.array(
    [
        [0.792, 0.541, 0.610],  # exp_007 within-DDD; exp_010 cross SG/TF
        [0.681, 0.613, 0.565],
        [0.550, 0.465, 0.321],
    ]
)


# ----------------------------------------------------------------------------
# Heatmap (matplotlib, grayscale)
# ----------------------------------------------------------------------------
def build_xai_heatmap(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200)
    # Greys: high tau -> light, low tau -> dark. Use reversed so low stability is dark.
    im = ax.imshow(XAI_TAU, cmap="Greys", vmin=0.2, vmax=1.0, aspect="auto")
    ax.set_xticks(range(len(XAI_COLS)))
    ax.set_xticklabels(XAI_COLS, fontsize=9, color="black")
    ax.set_yticks(range(len(XAI_ROWS)))
    ax.set_yticklabels(XAI_ROWS, fontsize=9, color="black")
    ax.tick_params(length=0)
    for i in range(XAI_TAU.shape[0]):
        for j in range(XAI_TAU.shape[1]):
            val = XAI_TAU[i, j]
            # Greys cmap: high tau -> dark cell, low tau -> light cell.
            # White text only on the dark (high-tau) cells; black elsewhere.
            txt_color = "white" if val >= 0.72 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    color=txt_color, fontsize=11)
    for spine in ax.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(0.8)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Kendall τ (rank agreement)", fontsize=8, color="black")
    cbar.ax.tick_params(labelsize=7, color="black")
    cbar.outline.set_edgecolor("black")
    ax.set_title("XAI explanation stability — every τ < 0.90 stability threshold",
                 fontsize=9.5, color="black", pad=8)
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor="white", bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------------
# pptx helpers
# ----------------------------------------------------------------------------
def _set_font(run, size, bold=False, italic=False, color=BLACK):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color


def add_blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def add_title(slide, text, top=Inches(0.35), size=24):
    box = slide.shapes.add_textbox(Inches(0.6), top, Inches(12.13), Inches(1.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    _set_font(run, size, bold=True)
    return box


def add_bullets(slide, items, left=Inches(0.6), top=Inches(1.5),
                width=Inches(12.13), height=Inches(5.4), size=16, line_spacing=1.15):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        if isinstance(item, tuple):
            level, text = item
        else:
            level, text = 0, item
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = level
        p.line_spacing = line_spacing
        p.space_after = Pt(6)
        # bullet marker for level-0/1
        marker = "" if text == "" else ("•  " if level == 0 else "–  ")
        run = p.add_run()
        run.text = marker + text
        _set_font(run, size if level == 0 else size - 1, bold=(level == 0 and text.endswith(":")))
    return box


def style_chart_common(chart, legend=True):
    chart.has_title = False
    if legend:
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(9)
        chart.legend.font.name = FONT
        chart.legend.font.color.rgb = BLACK
    else:
        chart.has_legend = False
    # axes fonts
    for axis in (chart.category_axis, chart.value_axis):
        axis.tick_labels.font.size = Pt(9)
        axis.tick_labels.font.name = FONT
        axis.tick_labels.font.color.rgb = BLACK
        axis.format.line.color.rgb = GRAY_AXIS
    # gridlines subtle
    va = chart.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = GRID
    va.major_gridlines.format.line.width = Pt(0.5)
    chart.category_axis.has_major_gridlines = False
    chart.category_axis.major_tick_mark = XL_TICK_MARK.OUTSIDE


def color_series(chart, shades):
    for i, ser in enumerate(chart.series):
        fill = ser.format.fill
        fill.solid()
        fill.fore_color.rgb = shades[i % len(shades)]
        line = ser.format.line
        line.color.rgb = BLACK
        line.width = Pt(0.5)


# ----------------------------------------------------------------------------
# Build presentation
# ----------------------------------------------------------------------------
def build():
    heatmap_path = ASSETS / "xai_stability_heatmap.png"
    build_xai_heatmap(heatmap_path)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ----- Slide 1: Title -----
    s = add_blank_slide(prs)
    tbox = s.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(11.53), Inches(2.6))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "An Explainable Student Digital Twin for Teacher-Facing Learning Analytics"
    _set_font(r, 34, bold=False)
    # subtitle block (template lines)
    sub = s.shapes.add_textbox(Inches(1.3), Inches(4.5), Inches(10.73), Inches(2.4))
    stf = sub.text_frame
    stf.word_wrap = True
    sub_lines = [
        "Aibyn Talgat · Astana IT University · [[Educational program]] · [[study period]]",
        "Master's dissertation",
        "Scientific supervisor: [[name, academic degree and title, affiliation]]",
    ]
    for i, line in enumerate(sub_lines):
        p = stf.paragraphs[0] if i == 0 else stf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(8)
        r = p.add_run()
        r.text = line
        _set_font(r, 16, italic=(i == 1))

    # ----- Slide 2: 1. Relevance -----
    s = add_blank_slide(prs)
    add_title(s, "1. Relevance of the research / Актуальность исследования")
    add_bullets(s, [
        "LMS store large volumes of learning activity, but their built-in analytics are descriptive — they rarely predict or explain student outcomes.",
        "Teachers need timely, interpretable, per-student insight to intervene early, not retrospective aggregate dashboards.",
        "Modern ML risk models are increasingly accurate but opaque (\"black box\"), which limits teacher trust and real adoption.",
        "An open question in learning analytics: do engineered \"digital-twin\" features actually beat a competent LMS baseline — and are the explanations stable enough to rely on?",
        "Reproducible, leakage-aware and honest evaluation (including negative results) is under-reported in the field.",
    ], size=17)

    # ----- Slide 3: 2. Purpose and objectives -----
    s = add_blank_slide(prs)
    add_title(s, "2. The purpose and objectives of the research / Цель и задачи исследования")
    add_bullets(s, [
        "Purpose:",
        (1, "Design and rigorously evaluate an explainable, teacher-facing Student Digital Twin — a lean, time-aware weekly student-state representation with an XAI layer — and test whether feature richness improves prediction."),
        "Objectives:",
        (1, "Build a versioned, leakage-aware weekly student-state data model and an end-to-end teacher-facing interface."),
        (1, "Implement and compare a model family: Ridge / Linear, Logistic Regression, Random Forest, Gradient Boosting (grade and pass-risk)."),
        (1, "Run a nested feature ablation (A_simple → B_lms → B_lms+mastery → C_twin) on real public data."),
        (1, "Add a perturbation-based XAI layer (permutation importance + local perturbation) and measure explanation stability (Kendall τ)."),
        (1, "Externally validate across two OULAD cohorts (DDD, BBB) and a second institution (KU Leuven)."),
    ], size=15, line_spacing=1.1)

    # ----- Slide 4: 4. Object and subject -----
    s = add_blank_slide(prs)
    add_title(s, "4. Object and subject of research / Объект и предмет исследования")
    add_bullets(s, [
        "Object:",
        (1, "The process of teacher-facing learning analytics — predicting and explaining student academic progression from LMS interaction and assessment data."),
        "",
        "Subject:",
        (1, "An explainable Student Digital Twin representation (lean weekly student-state features) and the predictive value plus explanation stability of its engineered features relative to a competent LMS baseline."),
    ], size=17)

    # ----- Slide 5: 5. Methods + initial data + model comparison charts -----
    s = add_blank_slide(prs)
    add_title(s, "5. Scientific methods used / Применяемые научные методы.  Initial data / Используемые исходные данные")
    add_bullets(s, [
        "Methods:",
        (1, "Supervised ML: Ridge/Linear (grade), Logistic Regression, Random Forest, Gradient Boosting (pass)."),
        (1, "Nested feature ablation with fixed-model comparison."),
        (1, "Two splits: student-grouped (generalization) and temporal-forward (early warning)."),
        (1, "Perturbation XAI: permutation importance + local median-replacement."),
        (1, "Stability: Kendall τ rank correlation + Jaccard top-k; bootstrap CIs."),
        "Initial data:",
        (1, "OULAD DDD 2013J — 1,938 students, 67,830 weekly snapshots."),
        (1, "OULAD BBB 2013J — 2,237 students, 80,532 weekly snapshots."),
        (1, "KU Leuven 1819 — 1,495 students (engagement-only)."),
        (1, "Grain: 1 row = 1 student × 1 week."),
    ], left=Inches(0.6), top=Inches(1.35), width=Inches(6.1), height=Inches(5.6),
        size=13, line_spacing=1.05)

    # Chart 5a: F1 / ROC-AUC clustered (classification) — top right
    cd = CategoryChartData()
    cd.categories = MODEL_APPROACHES
    cd.add_series("F1", MODEL_F1)
    cd.add_series("ROC-AUC", MODEL_AUC)
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                            Inches(6.9), Inches(1.3), Inches(6.1), Inches(2.95), cd)
    ch = gf.chart
    style_chart_common(ch)
    color_series(ch, [G1, G3])
    ch.value_axis.minimum_scale = 0.8
    ch.value_axis.maximum_scale = 1.0
    ch.value_axis.tick_labels.number_format = "0.00"
    ch.value_axis.tick_labels.number_format_is_linked = False
    tb = s.shapes.add_textbox(Inches(6.9), Inches(1.02), Inches(6.1), Inches(0.3))
    rp = tb.text_frame.paragraphs[0]; rr = rp.add_run()
    rr.text = "Classification (pass) — OULAD DDD 2013J, student-grouped"
    _set_font(rr, 10, bold=True)

    # Chart 5b: RMSE single series (regression) — bottom right
    cd2 = CategoryChartData()
    cd2.categories = RMSE_APPROACHES
    cd2.add_series("RMSE (final score 0-100)", RMSE_VALUES)
    gf2 = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                             Inches(6.9), Inches(4.55), Inches(6.1), Inches(2.55), cd2)
    ch2 = gf2.chart
    style_chart_common(ch2, legend=False)
    color_series(ch2, [G2])
    ch2.value_axis.minimum_scale = 11.0
    ch2.value_axis.maximum_scale = 14.0
    ch2.value_axis.tick_labels.number_format = "0.0"
    ch2.value_axis.tick_labels.number_format_is_linked = False
    tb2 = s.shapes.add_textbox(Inches(6.9), Inches(4.27), Inches(6.1), Inches(0.3))
    rp2 = tb2.text_frame.paragraphs[0]; rr2 = rp2.add_run()
    rr2.text = "Regression (final score) — RMSE, lower is better"
    _set_font(rr2, 10, bold=True)

    # ----- Slide 6: n1. Conclusions per task + ablation chart -----
    s = add_blank_slide(prs)
    add_title(s, "n1. Conclusions on the scientific work done for each task / Выводы по проделанной научной работе по каждой задаче")
    add_bullets(s, [
        "Data model & UI: a leakage-aware weekly Student Digital Twin and an end-to-end teacher interface were built (reproducible pipeline).",
        "Models: all four families reach F1 0.85–0.86 and ROC-AUC 0.95 on DDD — the pass target is genuinely predictive (never F1 = 1.0).",
        "Ablation (right): engineered Twin value is course- and split-dependent, not robust. Mastery helps only on BBB temporal-forward (6.31 → 5.28 RMSE); on DDD and on student-grouped splits it is null.",
        "XAI: explanations are interpretable but regime-sensitive (see Conclusion).",
        "External check: across 2 OULAD cohorts + KU Leuven, added feature richness does not robustly improve prediction.",
    ], left=Inches(0.6), top=Inches(1.55), width=Inches(6.3), height=Inches(5.4),
        size=14, line_spacing=1.08)

    cd3 = CategoryChartData()
    cd3.categories = ABL_FEATURE_SETS
    for name, vals in ABL_SERIES.items():
        cd3.add_series(name, vals)
    gf3 = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                             Inches(7.1), Inches(1.55), Inches(5.95), Inches(5.1), cd3)
    ch3 = gf3.chart
    style_chart_common(ch3)
    color_series(ch3, [G1, G2, G3, G4])
    ch3.value_axis.minimum_scale = 0.0
    ch3.value_axis.maximum_scale = 15.0
    ch3.value_axis.tick_labels.number_format = "0"
    ch3.value_axis.tick_labels.number_format_is_linked = False
    tb3 = s.shapes.add_textbox(Inches(7.1), Inches(1.27), Inches(5.95), Inches(0.3))
    rp3 = tb3.text_frame.paragraphs[0]; rr3 = rp3.add_run()
    rr3.text = "Ablation — gradient boosting RMSE (lower is better)"
    _set_font(rr3, 10, bold=True)

    # ----- Slide 7: 6. IMWP results (two tables) -----
    s = add_blank_slide(prs)
    add_title(s, "6. Results of the implementation of the IMWP / Результаты выполнения ИПРМ", size=22)

    # Sub-heading 1
    h1 = s.shapes.add_textbox(Inches(0.6), Inches(1.25), Inches(12.1), Inches(0.35))
    rp = h1.text_frame.paragraphs[0]; rr = rp.add_run()
    rr.text = "1. Scientific internships / Научная стажировка"
    _set_font(rr, 14, bold=True)

    intern_headers = ["№", "Internship organization /\nМесто прохождения стажировки",
                      "Period /\nСроки", "Results /\nРезультаты", "Mark /\nОтметка"]
    intern_rows = [["1", "[[organization]]", "[[dates]]", "[[results]]", "[[ ]]"]]
    add_table(s, intern_headers, intern_rows,
              Inches(0.6), Inches(1.7), Inches(12.13), Inches(1.3),
              col_widths=[0.6, 5.0, 2.3, 2.7, 1.53])

    # Sub-heading 2
    h2 = s.shapes.add_textbox(Inches(0.6), Inches(3.5), Inches(12.1), Inches(0.35))
    rp = h2.text_frame.paragraphs[0]; rr = rp.add_run()
    rr.text = "2. Plan for publishing scientific papers / План издания научных публикаций"
    _set_font(rr, 14, bold=True)

    pub_headers = ["№", "Title of the article / thesis\nНаименование статьи / тезиса",
                   "Publication / conference\nИздание / конференция",
                   "Completion dates /\nСроки", "Mark /\nОтметка"]
    pub_rows = [[
        "1",
        "Does Feature Richness Help? A Reproducible, Honest Evaluation of a Student Digital Twin and Its Explanation Stability Across Two Institutions",
        "IEEE SIST 2026 — Computational Intelligence track (Applications of CI in Education)",
        "[[submission date]]",
        "In preparation",
    ]]
    add_table(s, pub_headers, pub_rows,
              Inches(0.6), Inches(3.95), Inches(12.13), Inches(1.6),
              col_widths=[0.6, 4.6, 4.0, 1.7, 1.23], body_size=10)

    # ----- Slide 8: n2. Author's publications -----
    s = add_blank_slide(prs)
    add_title(s, "n2. Author's publications and the master student's personal contribution / Публикации автора и персональный вклад магистранта", size=20)
    add_bullets(s, [
        "Publication (in preparation): A. Talgat. \"Does Feature Richness Help? A Reproducible, Honest Evaluation of a Student Digital Twin and Its Explanation Stability Across Two Institutions.\" Target: IEEE SIST 2026, Computational Intelligence track.",
        "Personal contribution of the master student:",
        (1, "Conceived the research question and the falsifiable, dependency-driven experiment design."),
        (1, "Built the full reproducible, leakage-aware pipeline (data model, models, ablation, XAI)."),
        (1, "Ran all experiments on OULAD DDD/BBB 2013J and KU Leuven 1819 and produced the frozen artifacts."),
        (1, "Performed the explanation-stability analysis (Kendall τ) and wrote the manuscript."),
        "[[Add co-authors and their contribution share if applicable]]",
    ], size=15, line_spacing=1.1)

    # ----- Slide 9: Conclusion + XAI heatmap -----
    s = add_blank_slide(prs)
    add_title(s, "Conclusion / Заключение")
    add_bullets(s, [
        "The full Digital Twin was not justified: engineered feature richness does not robustly beat a competent LMS baseline.",
        "The finding is honest and heterogeneous across 2 OULAD cohorts + 2 institutions — course- and split-dependent, not a uniform win.",
        "XAI explanations are interpretable but regime-sensitive: Kendall τ 0.55–0.79 within a course, 0.32–0.61 across cohorts — every value below the 0.90 stability bar (heatmap).",
        "Contribution is methodological and cautionary: a reproducible, leakage-aware protocol + teacher UI + a documented synthetic-target circularity failure mode — not an accuracy record.",
    ], left=Inches(0.6), top=Inches(1.5), width=Inches(6.4), height=Inches(5.4),
        size=15, line_spacing=1.12)

    s.shapes.add_picture(str(heatmap_path), Inches(7.0), Inches(2.0),
                         width=Inches(6.0))

    prs.save(OUT_PPTX)
    print(f"Saved: {OUT_PPTX}")


def add_table(slide, headers, rows, left, top, width, height, col_widths=None,
              header_size=10, body_size=11):
    """Minimalist table: black borders only, no fill."""
    n_rows = len(rows) + 1
    n_cols = len(headers)
    gf = slide.shapes.add_table(n_rows, n_cols, left, top, width, height)
    table = gf.table
    table.first_row = False  # disable banded header styling
    table.horz_banding = False
    if col_widths:
        total = sum(col_widths)
        for j, w in enumerate(col_widths):
            table.columns[j].width = Emu(int(width * (w / total)))
    # header
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        _fill_cell(cell, h, header_size, bold=True)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            _fill_cell(table.cell(i, j), val, body_size, bold=False)
    return table


def _fill_cell(cell, text, size, bold):
    cell.fill.background()  # no fill
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = Inches(0.06)
    cell.margin_right = Inches(0.06)
    cell.margin_top = Inches(0.03)
    cell.margin_bottom = Inches(0.03)
    tf = cell.text_frame
    tf.word_wrap = True
    tf.clear()
    p = tf.paragraphs[0]
    for k, line in enumerate(str(text).split("\n")):
        if k == 0:
            run = p.add_run()
        else:
            p = tf.add_paragraph()
            run = p.add_run()
        run.text = line
        _set_font(run, size, bold=bold)
    _set_cell_border(cell)


def _set_cell_border(cell, color="000000", width_pt=1.0):
    """Add black borders on all four sides via raw XML.

    DrawingML CT_TableCellProperties requires lnL, lnR, lnT, lnB to appear in
    that order and BEFORE the fill element, otherwise PowerPoint ignores them.
    """
    from pptx.oxml.ns import qn

    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    w = str(int(width_pt * 12700))
    for idx, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        for el in tcPr.findall(qn(tag)):
            tcPr.remove(el)
        ln = tcPr.makeelement(qn(tag), {"w": w, "cap": "flat"})
        fill = ln.makeelement(qn("a:solidFill"), {})
        clr = ln.makeelement(qn("a:srgbClr"), {"val": color})
        fill.append(clr)
        ln.append(fill)
        tcPr.insert(idx, ln)  # insert before fill, preserving lnL/R/T/B order


if __name__ == "__main__":
    build()
