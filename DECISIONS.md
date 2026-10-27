# Decisions

Rulings on how work in this repository is run. Newest last.

## 2026-10-27 — task 001, bootstrap

- **prompt_outputs/ is committed and public.** Reports there follow the
  public-report rule, CLAUDE.md rule 20.
- **reviews/ stays a local, gitignored archive.** It is not migrated.
- **Trailers.** Co-Authored-By only, with the model name Claude Code
  supplies (CLAUDE.md rule 8). A push task checks the trailer's key,
  count and position only. No session trailer.
- **.gitignore** admits prompt_outputs/*.txt; .claude/settings.local.json
  stays local.
- **Prompt/file differences** are reported; work stops only when a
  difference blocks the task or would make the output assert something
  false or unverified (CLAUDE.md rule 19).
