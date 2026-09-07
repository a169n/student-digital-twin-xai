#!/usr/bin/env python3
"""Render the SIDe 2026 submission from main.tex into an IEEE-formatted .docx.

The conference wants the IEEE double-column conference template and a blind
submission. Word is the second required format, and the previous version of this
script carried its own copy of the manuscript text. That copy drifted: the .tex
reported a failed replication while the .docx still announced a successful one.
So this reads main.tex and converts it, and there is exactly one manuscript.

It handles the LaTeX subset the paper actually uses --- sectioning, enumerate,
booktabs tabulars, figures, thebibliography, and inline \\emph, \\textbf, \\cite,
\\url,
\\ref and a handful of maths and accents. Anything outside that subset raises
rather than being silently dropped, because a paper that quietly loses a sentence
on the way to Word is worse than one that fails to build.

Layout follows the IEEE conference template: US Letter, 0.75/1.0 in vertical and
0.625 in horizontal margins, full-width title block, two-column body with a
0.25 in gutter, Times New Roman at 24 pt title, 9 pt abstract, 10 pt body, 8 pt
references. Author names and the repository URL are absent: review is blind.

Usage:
    python scripts/build_side2026_docx.py
    # -> docs/dissertation/side2026_submission/SIDe2026_submission.docx

Dependencies: python-docx
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

REPO = Path(__file__).resolve().parents[1]
SUB = REPO / "docs" / "dissertation" / "side2026_submission"
TEX = SUB / "main.tex"
OUT = SUB / "SIDe2026_submission.docx"
FONT = "Times New Roman"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


# ---------------------------------------------------------------------------
# LaTeX -> plain text, with the label and citation numbering resolved
# ---------------------------------------------------------------------------

ACCENTS = {
    r"\'a": "\u00e1", r"\'e": "\u00e9", r"\'i": "\u00ed", r"\'o": "\u00f3",
    r"\'u": "\u00fa", r"\'z": "\u017a", r'\"a': "\u00e4", r'\"o': "\u00f6",
    r'\"u': "\u00fc", r"\~n": "\u00f1", r"\c{c}": "\u00e7",
}
SYMBOLS = {
    r"\tau": "\u03c4", r"\times": "\u00d7", r"\lceil": "\u2308", r"\rceil": "\u2309",
    r"\ldots": "\u2026", r"\alpha": "\u03b1", r"\Delta": "\u0394",
}


def _strip_comments(tex: str) -> str:
    """Drop LaTeX comments, whole-line and trailing alike.

    Trailing ones matter: the line that sets the anonymity switch carries
    "% \\blindtrue for anonymous review" after it, and a parser that reads only
    whole-line comments finds that token and builds the wrong author block.
    An escaped \\% is a literal percent sign and is left alone.
    """
    out = []
    for line in tex.split("\n"):
        cut = re.search(r"(?<!\\)%", line)
        if cut is not None:
            line = line[: cut.start()].rstrip()
            if not line:
                continue
        out.append(line)
    return "\n".join(out)


def collect_labels(tex: str) -> dict[str, str]:
    """Map every \\label to the number the reader will see.

    Sections, subsections, tables and figures are numbered in order of
    appearance, exactly as LaTeX does it. Starred sections take no number, so a
    label inside one resolves to its title instead.
    """
    labels: dict[str, str] = {}
    sec = sub = tab = fig = 0
    pending: list[str] = []  # labels seen before their counter increments
    for m in re.finditer(
        r"\\(section|subsection)\*?\{([^}]*)\}|\\begin\{(table\*?|figure\*?)\}"
        r"|\\label\{([^}]*)\}",
        tex,
    ):
        kind, title, env, label = m.group(1), m.group(2), m.group(3), m.group(4)
        if kind == "section":
            starred = m.group(0).startswith("\\section*")
            if not starred:
                sec += 1
                sub = 0
            pending = [ROMAN[sec - 1] if not starred else title]
        elif kind == "subsection":
            sub += 1
            pending = [f"{ROMAN[sec - 1]}-{chr(ord('A') + sub - 1)}"]
        elif env:
            if env.startswith("table"):
                tab += 1
                pending = [ROMAN[tab - 1]]
            else:
                fig += 1
                pending = [str(fig)]
        elif label:
            labels[label] = pending[0] if pending else "?"
    return labels


def collect_citations(tex: str) -> dict[str, int]:
    keys = re.findall(r"\\bibitem\{([^}]*)\}", tex)
    return {k: i + 1 for i, k in enumerate(keys)}


def inline(text: str, labels: dict[str, str], cites: dict[str, int]) -> list[tuple[str, bool, bool]]:
    """Convert one LaTeX paragraph into (run text, bold, italic) triples."""
    t = text
    t = re.sub(r"\\label\{[^}]*\}", "", t)  # already resolved into numbers
    t = re.sub(r"\\cite\{([^}]*)\}", lambda m: "[" + ", ".join(
        str(cites.get(k.strip(), "?")) for k in m.group(1).split(",")) + "]", t)
    t = re.sub(r"\\ref\{([^}]*)\}", lambda m: labels.get(m.group(1), "?"), t)
    t = re.sub(r"\\tfrac\{(\d+)\}\{(\d+)\}", r"\1/\2", t)
    t = re.sub(r"\\(?:url|text(?:tt)?)\{([^}]*)\}", r"\1", t)
    for k, v in SYMBOLS.items():
        t = t.replace(k, v)
    for k, v in ACCENTS.items():
        t = t.replace(k, v)
    t = t.replace("$", "").replace("~", " ")
    t = t.replace(r"\,", "\u2009").replace(r"\%", "%").replace(r"\&", "&")
    t = t.replace("{,}", ",").replace(r"\ ", " ")
    t = t.replace("---", "\u2014").replace("--", "\u2013")
    t = t.replace("``", "\u201c").replace("''", "\u201d")

    parts: list[tuple[str, bool, bool]] = []
    pos = 0
    for m in re.finditer(r"\\(emph|textit|textbf)\{([^{}]*)\}", t):
        if m.start() > pos:
            parts.append((t[pos:m.start()], False, False))
        parts.append((m.group(2), m.group(1) == "textbf", m.group(1) != "textbf"))
        pos = m.end()
    if pos < len(t):
        parts.append((t[pos:], False, False))

    cleaned = []
    for s, b, i in parts:
        # Not \s+: that class includes the thin space just inserted for "22.5 %".
        s = re.sub(r"[ \t\n\r]+", " ", s.replace("\\\\", " "))
        if s:
            cleaned.append((s, b, i))
    leftover = [s for s, _, _ in cleaned if "\\" in s]
    if leftover:
        raise ValueError(f"unhandled LaTeX in: {leftover[0][:120]!r}")
    return cleaned


# ---------------------------------------------------------------------------
# Word building blocks
# ---------------------------------------------------------------------------


def set_columns(section, count: int, space_twips: int = 360) -> None:
    """python-docx exposes no column API, so write w:cols into the sectPr."""
    cols = section._sectPr.xpath("./w:cols")[0]
    cols.set(qn("w:num"), str(count))
    cols.set(qn("w:space"), str(space_twips))
    cols.set(qn("w:equalWidth"), "1")


def para(doc, *, size=10, align=None, space_after=4, indent=0.0, keep=False):
    p = doc.add_paragraph()
    fmt = p.paragraph_format
    fmt.space_after = Pt(space_after)
    fmt.space_before = Pt(0)
    fmt.line_spacing = 1.0
    if align is not None:
        p.alignment = align
    if indent:
        fmt.first_line_indent = Inches(indent)
    if keep:
        fmt.keep_with_next = True
    return p


def runs(p, parts, size=10):
    for text, bold, italic in parts:
        r = p.add_run(text)
        r.font.name = FONT
        r.font.size = Pt(size)
        r.bold, r.italic = bold, italic
    return p


def text_para(doc, s, *, size=10, align=None, bold=False, italic=False, space_after=4, indent=0.0):
    return runs(para(doc, size=size, align=align, space_after=space_after, indent=indent),
                [(s, bold, italic)], size=size)


# ---------------------------------------------------------------------------
# Document assembly
# ---------------------------------------------------------------------------


def env_body(tex: str, name: str) -> str:
    m = re.search(r"\\begin\{" + name + r"\}(.*?)\\end\{" + name + r"\}", tex, re.S)
    if not m:
        raise ValueError(f"environment {name} not found")
    return m.group(1).strip()


def paragraphs(block: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", block) if p.strip()]


def add_table(doc, block: str, number: str, labels, cites) -> None:
    caption = re.search(r"\\caption\{(.*?)\}\s*\n", block, re.S).group(1)
    tabular = re.search(r"\\begin\{tabular\}\{[^}]*\}(.*?)\\end\{tabular\}", block, re.S).group(1)
    rows = []
    for line in tabular.split("\\\\"):
        line = re.sub(r"\\(top|mid|bottom)rule", "", line).strip()
        # A spanning cell becomes its text plus the empty cells it covered, so
        # every row still has the same number of columns as the header.
        line = re.sub(
            # The column spec can itself contain braces, as in {@{}l}.
            r"\\multicolumn\{(\d+)\}\{(?:[^{}]|\{[^{}]*\})*\}\{([^{}]*)\}",
            lambda m: m.group(2) + " &" * (int(m.group(1)) - 1),
            line,
        )
        if line:
            rows.append([c.strip() for c in line.split("&")])
    if not rows:
        raise ValueError("empty tabular")

    runs(para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, keep=True),
         [(f"TABLE {number}", False, False)], size=8)
    runs(para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, keep=True),
         inline(caption, labels, cites), size=8)

    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    for i, row in enumerate(rows):
        for j, cell in enumerate(row[: len(rows[0])]):
            c = t.cell(i, j)
            c.text = ""
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            runs(p, inline(cell, labels, cites) or [("", False, False)], size=8)
            if i == 0:
                for r in p.runs:
                    r.bold = True
    para(doc, space_after=6)


def add_figure(doc, block: str, number: str, labels, cites) -> None:
    src = re.search(r"\\includegraphics\[[^\]]*\]\{([^}]*)\}", block).group(1)
    caption = re.search(r"\\caption\{(.*?)\}\s*\n", block, re.S).group(1)
    # The PDF figures are vector; Word needs a raster, and the plotting scripts
    # write a PNG beside every PDF for exactly this.
    png = SUB / "figures" / (Path(src).stem + ".png")
    if not png.exists():
        png = REPO / "docs" / "dissertation" / "figures" / "side2026" / (Path(src).stem + ".png")
    if not png.exists():
        raise FileNotFoundError(f"no PNG for {src}; run the plotting script")
    p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p.add_run().add_picture(str(png), width=Inches(3.3))
    runs(para(doc, space_after=8), [(f"Fig. {number}. ", False, False)] +
         inline(caption, labels, cites), size=8)


def resolve_blind(tex: str) -> str:
    """Take the branch of every \\ifblind ... \\else ... \\fi that LaTeX would take.

    The manuscript carries an anonymous and a named variant of the author block
    and of the repository sentence. Word has no conditionals, so the choice has
    to be made here, from the same \\blindtrue / \\blindfalse the .tex sets --- or
    the two formats disagree about whether the paper is anonymous.
    """
    switch = re.search(r"\\blind(true|false)\b", tex)
    anonymous = bool(switch) and switch.group(1) == "true"
    # The declaration goes first: \newif\ifblind contains the token \ifblind, so
    # leaving it in makes the conditional match start there and swallow the
    # title along with everything else up to the first \else.
    tex = re.sub(r"\\newif\\ifblind|\\blind(?:true|false)\b", "", tex)
    return re.sub(
        r"\\ifblind(.*?)\\else(.*?)\\fi",
        lambda m: m.group(1) if anonymous else m.group(2),
        tex,
        flags=re.S,
    )


def parse_authors(tex: str) -> list[tuple[str, list[str]]]:
    """(name, affiliation lines) for each author in the \\author block."""
    start = tex.index("\\author")
    chosen = braced(tex, tex.index("{", start))

    authors: list[tuple[str, list[str]]] = []
    for m in re.finditer(r"\\IEEEauthorblock([NA])\{", chosen):
        body = braced(chosen, m.end() - 1)
        if m.group(1) == "N":
            authors.append((body.strip(), []))
        elif authors:
            authors[-1][1].extend(
                line.strip() for line in body.split("\\\\") if line.strip()
            )
    return authors


def braced(text: str, open_at: int) -> str:
    """The argument starting at the brace in text[open_at], braces balanced.

    A regex cannot do this: an author block contains \\textit{...}, and a
    non-greedy {(.*?)} stops at that inner closing brace, which is how the first
    version of this parser silently found no authors at all.
    """
    assert text[open_at] == "{", "expected a brace"
    depth = 0
    for i in range(open_at, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_at + 1 : i]
    raise ValueError("unbalanced braces in the author block")


def add_authors(doc, tex: str) -> None:
    authors = parse_authors(tex)
    if not authors:
        raise ValueError("no author block found in main.tex")
    if len(authors) == 1 and not authors[0][1]:
        text_para(doc, authors[0][0], size=11, align=WD_ALIGN_PARAGRAPH.CENTER,
                  space_after=10)
        return

    # Six authors in one row leaves ~1.2 in per cell, which breaks the emails
    # across four lines. Wrap at three per row, as \linebreakand does in the .tex.
    per_row = min(len(authors), 3)
    rows = -(-len(authors) // per_row)
    table = doc.add_table(rows=rows, cols=per_row)
    table.autofit = True
    cells = [c for row in table.rows for c in row.cells]
    for cell, (name, lines) in zip(cells, authors):
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        runs(p, [(name, False, False)], size=11)
        for line in lines:
            q = cell.add_paragraph()
            q.alignment = WD_ALIGN_PARAGRAPH.CENTER
            q.paragraph_format.space_after = Pt(0)
            runs(q, inline(line, {}, {}), size=9.5)
    para(doc, space_after=10)


def build() -> Path:
    tex = resolve_blind(_strip_comments(TEX.read_text(encoding="utf-8")))
    labels = collect_labels(tex)
    cites = collect_citations(tex)

    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(10)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)

    first = doc.sections[0]
    for s in (first,):
        s.page_width, s.page_height = Inches(8.5), Inches(11)
        s.top_margin, s.bottom_margin = Inches(0.75), Inches(1.0)
        s.left_margin = s.right_margin = Inches(0.625)
    set_columns(first, 1)

    title = re.search(r"\\title\{(.*?)\}\s*\n", tex, re.S).group(1)
    runs(para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10),
         inline(title, labels, cites), size=20)
    add_authors(doc, tex)

    two = doc.add_section(WD_SECTION.CONTINUOUS)
    two.page_width, two.page_height = Inches(8.5), Inches(11)
    two.top_margin, two.bottom_margin = Inches(0.75), Inches(1.0)
    two.left_margin = two.right_margin = Inches(0.625)
    set_columns(two, 2)

    runs(para(doc, space_after=4),
         [("Abstract\u2014", True, False)] +
         [(s, True, i) for s, _, i in inline(env_body(tex, "abstract"), labels, cites)], size=9)
    runs(para(doc, space_after=8),
         [("Index Terms\u2014", True, True)] +
         [(s, False, True) for s, _, _ in inline(env_body(tex, "IEEEkeywords"), labels, cites)],
         size=9)

    body = tex[tex.index("\\end{IEEEkeywords}") + len("\\end{IEEEkeywords}"):]
    body = body[: body.index("\\begin{thebibliography}")]

    # Split on the structures that must be handled as blocks; everything between
    # them is ordinary prose.
    pattern = re.compile(
        r"\\section\*?\{[^}]*\}|\\subsection\{[^}]*\}"
        r"|\\begin\{table\*?\}.*?\\end\{table\*?\}"
        r"|\\begin\{figure\*?\}.*?\\end\{figure\*?\}"
        r"|\\begin\{enumerate\}.*?\\end\{enumerate\}",
        re.S,
    )
    sec = sub_i = tab = fig = 0
    pos = 0
    for m in pattern.finditer(body):
        for chunk in paragraphs(body[pos:m.start()]):
            runs(para(doc, indent=0.2, space_after=4), inline(chunk, labels, cites))
        block = m.group(0)
        if block.startswith("\\section"):
            name = re.match(r"\\section\*?\{(.*)\}", block, re.S).group(1)
            if block.startswith("\\section*"):
                label = name.upper()
            else:
                sec += 1
                sub_i = 0
                label = f"{ROMAN[sec - 1]}. {name.upper()}"
            runs(para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, keep=True),
                 [(label, False, False)], size=10)
        elif block.startswith("\\subsection"):
            sub_i += 1
            name = re.match(r"\\subsection\{(.*)\}", block, re.S).group(1)
            runs(para(doc, space_after=3, keep=True),
                 [(f"{chr(ord('A') + sub_i - 1)}. ", False, True)] + inline(name, labels, cites),
                 size=10)
        elif block.startswith("\\begin{table"):
            tab += 1
            add_table(doc, block, ROMAN[tab - 1], labels, cites)
        elif block.startswith("\\begin{figure"):
            fig += 1
            add_figure(doc, block, str(fig), labels, cites)
        else:
            items = block[block.index("}") + 1 : block.rindex("\\end{enumerate}")]
            for i, item in enumerate(re.findall(r"\\item\s+(.*?)(?=\\item|\Z)", items, re.S), 1):
                runs(para(doc, indent=0.2, space_after=3),
                     [(f"{i}) ", False, False)] + inline(item, labels, cites))
        pos = m.end()
    for chunk in paragraphs(body[pos:]):
        runs(para(doc, indent=0.2, space_after=4), inline(chunk, labels, cites))

    runs(para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, keep=True),
         [("REFERENCES", False, False)], size=10)
    bib = re.search(
        r"\\begin\{thebibliography\}\{[^}]*\}(.*?)\\end\{thebibliography\}", tex, re.S
    ).group(1)
    for i, item in enumerate(re.findall(r"\\bibitem\{[^}]*\}(.*?)(?=\\bibitem|\Z)", bib, re.S), 1):
        runs(para(doc, space_after=2), [(f"[{i}] ", False, False)] + inline(item, labels, cites),
             size=8)

    doc.save(OUT)
    return OUT


if __name__ == "__main__":
    path = build()
    print("written", path)
