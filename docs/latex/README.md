# Document export

`methodology.tex` and `software_overview.tex` are generated from the Markdown
in `../`. Edit the Markdown, never the `.tex` — regenerating overwrites it.

## LaTeX export

One command each, from the repository root:

```
pandoc docs/methodology.md -f markdown -t latex --natbib --lua-filter=docs/latex/thesis.lua -o docs/latex/methodology.tex
pandoc docs/software_overview.md -f markdown -t latex --natbib --lua-filter=docs/latex/thesis.lua -o docs/latex/software_overview.tex
```

No manual post-processing. `thesis.lua` drops the Markdown `---` separators,
which pandoc would otherwise render as
`\begin{center}\rule{0.5\linewidth}{0.5pt}\end{center}`.

The generated file is a **fragment**, not a standalone document (no
`\documentclass`, no `\begin{document}`).

Headings carry no manual numbers, so LaTeX numbers them according to the
thesis's own sectioning. Cross-references within the text name the target
section in italics rather than by number.

Content between `<!-- repo-only:start -->` and `<!-- repo-only:end -->` in
`methodology.md` is excluded from the LaTeX export. It stays visible when the
Markdown is read on GitHub, but never reaches the thesis.

## Use in Overleaf

1. Upload the `.tex` fragments you need and `flavunato.bib` to the project.
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

Citations are emitted as `\citep{...}` — 11 occurrences in
`methodology.tex`, 2 in `software_overview.tex` — which requires
natbib. If the thesis uses biblatex instead, regenerate with `--biblatex`
rather than `--natbib`, and the citations become `\autocite{...}`.

## Required packages

The fragment uses these; they must be in the thesis preamble:

```latex
\usepackage[T1]{fontenc} % accents (Orleans) and copy-pasteable underscores
\usepackage{amsmath}    % \sqrt, \frac, \text, \operatorname, \tag
\usepackage{booktabs}   % \toprule, \midrule, \bottomrule
\usepackage{longtable}  % the four tables in methodology.tex
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

### Tables

The tables have no captions. Load the `caption` package (listed above);
without it LaTeX reports harmless "No counter none defined" errors.

### Tested

`methodology.tex` compiled successfully on Overleaf with the preamble above
(report class, pdfLaTeX).

### Heading levels

By default Methodology is a `\section` (for use inside an existing chapter).
To make it a standalone `\chapter`, regenerate with:

```
pandoc docs/methodology.md -f markdown -t latex --natbib --lua-filter=docs/latex/thesis.lua --shift-heading-level-by=-1 -o docs/latex/methodology.tex
```

## Word (.docx) export

For readers who want Word rather than LaTeX. One command each, from the
repository root:

```
pandoc docs/methodology.md --lua-filter=docs/latex/thesis.lua --lua-filter=docs/latex/docx.lua --citeproc --bibliography=docs/latex/flavunato.bib --metadata reference-section-title="References" -o docs/methodology.docx
pandoc docs/software_overview.md --lua-filter=docs/latex/thesis.lua --lua-filter=docs/latex/docx.lua --citeproc --bibliography=docs/latex/flavunato.bib --metadata reference-section-title="References" -o docs/software_overview.docx
```

`docx.lua` reports how many equation tags it converted, e.g.
`docx.lua: converted 6 equation tags` for `methodology.md`.

Unlike LaTeX, Word has no `.bib` step, so `--citeproc` resolves the citations
at build time and appends the reference list.
`--metadata reference-section-title` supplies the heading above it, which
citeproc otherwise omits.

Three things to know:

- **The `.docx` is generated locally and not committed.** `.gitignore`
  excludes it. Rebuild it when the Markdown changes; never edit the `.docx`
  and expect the change to survive.

- **`\tag{}` must be the last token of a display equation.** `docx.lua`
  matches it only at the end of a `$$...$$` block; a `\tag` anywhere else is
  ignored and the label disappears from the Word file. Check the reported
  count: `methodology.md` should convert 6.

- **The equations are Word-native OMML** (`m:oMath`), not images, so they stay
  editable and searchable. Microsoft Word renders them correctly. LibreOffice
  does not: rendering the built file through it leaves every equation blank,
  inline and display alike. Prose, headings, tables, citations and the
  References list survive there intact — only the equations are lost. Open the
  `.docx` in Word.
