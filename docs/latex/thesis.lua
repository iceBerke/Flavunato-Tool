-- Pandoc filter for the thesis export of docs/methodology.md.
-- Drops the Markdown section separators (---), which pandoc would
-- otherwise render as \begin{center}\rule{...}{...}\end{center}.

function HorizontalRule()
  return {}
end
