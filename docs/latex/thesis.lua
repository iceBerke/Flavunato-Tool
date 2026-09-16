-- Pandoc filter for the thesis export of docs/methodology.md.
--
-- 1. Drops the Markdown section separators (---), which pandoc would
--    otherwise render as \begin{center}\rule{...}{...}\end{center}.
-- 2. Drops everything between <!-- repo-only:start --> and
--    <!-- repo-only:end -->, i.e. content that belongs in the repository
--    but not in the thesis. The markers are HTML comments, so they stay
--    invisible when the Markdown is read on GitHub.

function HorizontalRule()
  return {}
end

local function marker(block, which)
  return block.t == "RawBlock"
    and block.text:match("<!%-%-%s*repo%-only:" .. which .. "%s*%-%->") ~= nil
end

function Blocks(blocks)
  local kept, skipping = {}, false
  for _, block in ipairs(blocks) do
    if marker(block, "start") then
      skipping = true
    elseif marker(block, "end") then
      skipping = false
    elseif not skipping then
      kept[#kept + 1] = block
    end
  end
  return kept
end
