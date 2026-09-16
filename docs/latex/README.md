# LaTeX output

`methodology.tex` is generated from `../methodology.md`. Edit the Markdown,
never the `.tex` — regenerating overwrites it.

## Regenerate

One command, from the repository root:

```
pandoc docs/methodology.md -f markdown -t latex --natbib --lua-filter=docs/latex/thesis.lua -o docs/latex/methodology.tex
```

No manual post-processing. `thesis.lua` drops the Markdown `---` separators,
which pandoc would otherwise render as
`\begin{center}\rule{0.5\linewidth}{0.5pt}\end{center}`.

The generated file is a **fragment**, not a standalone document (no
`\documentclass`, no `\begin{document}`).

Headings carry no manual numbers, so LaTeX numbers them according to the
thesis's own sectioning. Cross-references within the text name the target
section in italics rather than by number.

## Use in Overleaf

1. Upload `methodology.tex` and `flavunato.bib` to the project.
2. Include the fragment where the chapter should appear:

   ```latex
   \input{methodology}
   ```

3. Add the bibliography, e.g. with natbib:

   ```latex
   \usepackage[numbers]{natbib}
   ...
   \bibliographystyle{unsrtnat}
   \bibliography{flavunato}
   ```

   If the thesis already has a `.bib`, merge the two entries from
   `flavunato.bib` into it instead of adding a second bibliography.

The thesis copy may be edited freely in Overleaf; the repo `.tex` is
regenerated from the Markdown.

Citations are emitted as `\citep{...}` (11 occurrences), which requires
natbib. If the thesis uses biblatex instead, regenerate with `--biblatex`
rather than `--natbib`, and the citations become `\autocite{...}`.

## Required packages

The fragment uses these; they must be in the thesis preamble:

```latex
\usepackage{amsmath}    % \sqrt, \frac, \text, \operatorname
\usepackage{booktabs}   % \toprule, \midrule, \bottomrule
\usepackage{longtable}  % the three tables
\usepackage{array}      % \arraybackslash in the column specifications
\usepackage{calc}       % \real{...} in the longtable column widths
\usepackage{caption}    % see "uncaptioned tables" below
\usepackage{hyperref}   % \texorpdfstring, emitted in headings containing math
\usepackage[numbers]{natbib}
```

Most thesis templates already load all of these. `hyperref` is normally loaded
last.

The fragment also uses `\tightlist`, which pandoc defines in its own preamble.
Because this is a fragment rather than a standalone document, declare it once
in the thesis preamble:

```latex
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
```

`\real` comes from `calc`, so loading that package is enough.

### Uncaptioned tables

For tables without a caption, pandoc emits

```latex
{\def\LTcaptype{none} % do not increment counter
\begin{longtable}...
```

`longtable` alone then raises `LaTeX Error: No counter 'none' defined` (three
times, once per table). LaTeX recovers and still produces output, but the
errors are noisy. Loading the `caption` package is the intended remedy —
pandoc's own standalone template loads it for exactly this purpose.

Verified locally: the fragment compiles and produces a PDF with `amsmath`,
`booktabs`, `longtable`, `array`, `calc` and `natbib`, with all citations
resolved. Not verified locally: the `caption` and `hyperref` lines above, since
`caption.sty` and hyperref's dependency `infwarerr.sty` are absent from the
local TeX installation. Both are standard in TeX Live and on Overleaf.

## Heading levels

The fragment starts at `\section` — one `\section` (Methodology), 10
`\subsection`, 9 `\subsubsection`. If the thesis needs it to be a `\chapter`,
regenerate with:

```
pandoc docs/methodology.md -f markdown -t latex --natbib --lua-filter=docs/latex/thesis.lua --shift-heading-level-by=-1 -o docs/latex/methodology.tex
```
