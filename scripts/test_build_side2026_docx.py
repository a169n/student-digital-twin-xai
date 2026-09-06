"""Checks for the LaTeX subset the .docx builder understands.

The builder exists because a hand-maintained Word copy drifted from the .tex.
Its failure mode now is quieter: a construct it does not recognise could be
dropped, and nobody reads a 5-page Word file closely enough to notice one
missing clause. inline() raises on anything it cannot convert, so these pin that
it converts what the paper contains and still raises on what it does not.

Usage:  python scripts/test_build_side2026_docx.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_side2026_docx import (  # noqa: E402
    _strip_comments,
    collect_citations,
    collect_labels,
    inline,
    parse_authors,
    resolve_blind,
)

LABELS = {"sec:agree": "V-B", "tab:cohorts": "I", "fig:spread": "1"}
CITES = {"swamy2022": 8, "hooker2021": 15}


def flat(parts):
    return "".join(s for s, _, _ in parts)


def test_inline_resolves_references():
    out = flat(inline(r"See Section~\ref{sec:agree} and Table~\ref{tab:cohorts}.", LABELS, CITES))
    assert out == "See Section V-B and Table I."


def test_inline_numbers_citations_in_bibliography_order():
    out = flat(inline(r"as shown \cite{swamy2022,hooker2021}", LABELS, CITES))
    assert out == "as shown [8, 15]"


def test_inline_carries_emphasis():
    parts = inline(r"the \emph{above} and \textbf{below}", LABELS, CITES)
    assert ("above", False, True) in parts
    assert ("below", True, False) in parts


def test_inline_converts_maths_and_typography():
    out = flat(inline(r"$\tau$ 0.408, 22.5\,\% --- a range of $\tfrac{1}{4}$", LABELS, CITES))
    assert "τ 0.408" in out
    assert "22.5 %" in out
    assert "—" in out and "1/4" in out


def test_inline_refuses_unknown_commands():
    try:
        inline(r"a \footnote{surprise} b", LABELS, CITES)
    except ValueError:
        return
    raise AssertionError("unhandled LaTeX was silently dropped")


def test_labels_and_citations_are_numbered_in_document_order():
    tex = (
        r"\section{One}\label{s1}" "\n"
        r"\subsection{First}\label{sub1}" "\n"
        r"\subsection{Second}\label{sub2}" "\n"
        r"\section{Two}\label{s2}" "\n"
        r"\begin{figure}\label{f1}\end{figure}" "\n"
        r"\begin{thebibliography}{00}\bibitem{a}A\bibitem{b}B\end{thebibliography}"
    )
    labels = collect_labels(tex)
    assert labels["s1"] == "I" and labels["s2"] == "II"
    assert labels["sub1"] == "I-A" and labels["sub2"] == "I-B"
    assert labels["f1"] == "1"
    assert collect_citations(tex) == {"a": 1, "b": 2}


AUTHOR_TEX = r"""\newif\ifblind
\blindfalse  % \blindtrue for anonymous review

\begin{document}
\title{A Title}
\ifblind
\author{\IEEEauthorblockN{Anonymous submission}}
\else
\author{
\IEEEauthorblockN{A. B. First}
\IEEEauthorblockA{\textit{Master degree student} \\
\textit{Some University} \\
first@example.org}
\and
\IEEEauthorblockN{C. D. Second*}
\IEEEauthorblockA{\textit{PhD} \\
second@example.org}
}
\fi
"""


def test_trailing_comments_are_stripped():
    # The switch line carries "% \blindtrue ..."; reading that as the setting
    # produced an anonymous Word file from a named .tex.
    stripped = _strip_comments(AUTHOR_TEX)
    assert r"\blindfalse" in stripped
    assert r"\blindtrue" not in stripped


def test_named_branch_is_taken_and_title_survives():
    resolved = resolve_blind(_strip_comments(AUTHOR_TEX))
    assert r"\title{A Title}" in resolved  # \newif\ifblind must not swallow it
    assert "Anonymous submission" not in resolved
    assert "A. B. First" in resolved


def test_anonymous_branch_hides_the_names():
    blind = AUTHOR_TEX.replace(r"\blindfalse", r"\blindtrue")
    resolved = resolve_blind(_strip_comments(blind))
    assert "Anonymous submission" in resolved
    assert "A. B. First" not in resolved
    assert "first@example.org" not in resolved


def test_author_block_parses_through_nested_braces():
    resolved = resolve_blind(_strip_comments(AUTHOR_TEX))
    authors = parse_authors(resolved)
    assert [name for name, _ in authors] == ["A. B. First", "C. D. Second*"]
    # \textit{...} inside the affiliation must not end the argument early.
    assert authors[0][1] == [
        r"\textit{Master degree student}",
        r"\textit{Some University}",
        "first@example.org",
    ]


def test_affiliation_lines_render_as_italic_text():
    parts = inline(r"\textit{Some University}", LABELS, CITES)
    assert parts == [("Some University", False, True)]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("all checks passed")
