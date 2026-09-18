-- Pandoc filter for the Word (.docx) export of docs/methodology.md.
--
-- Moves the equation label into the equation body: a display equation
-- ending in \tag{Dn} is rewritten as "<body>\qquad \text{(Dn)}".
--
-- Why: pandoc's OMML writer silently drops \tag, so without this filter
-- (D1)-(D6) vanish from the .docx while the prose still refers to them.
-- \qquad and \text{} do survive, as real spacing and upright text.
--
-- \tag{} must be the LAST token inside the $$...$$ block. A \tag anywhere
-- else does not match and is ignored -- i.e. silently dropped, as before.
--
-- LaTeX is left untouched: there \tag is already correct, so the filter
-- guards on FORMAT and the .tex output is unchanged.
--
-- Used only by the .docx commands in README.md; chain it after thesis.lua.

local converted = 0

function Math(m)
  if FORMAT:match("latex") then return nil end
  if m.mathtype ~= "DisplayMath" then return nil end
  local body, tag = m.text:match([[^(.-)%s*\tag%{(.-)%}%s*$]])
  if not tag then return nil end
  converted = converted + 1
  return pandoc.Math("DisplayMath",
    body .. [[\qquad \text{(]] .. tag .. [[)}]])
end

function Pandoc(doc)
  io.stderr:write("docx.lua: converted " .. converted .. " equation tags\n")
  return doc
end
