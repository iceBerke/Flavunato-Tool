# 001 — bootstrap — implement

Task: append the WORKING RULES block to CLAUDE.md, create prompt_outputs/,
report conflicts. Stops at the review gate: nothing committed, nothing
pushed. No tests were run (docs-only task); see TESTS.

No earlier reports in prompt_outputs/, so no errata.

## Files touched

| Path | Change |
|---|---|
| `CLAUDE.md` | WORKING RULES block appended after one blank line; nothing else changed (checks A1–A5 below) |
| `prompt_outputs/001-bootstrap-implement.md` | new — this report |
| `prompt_outputs/001-bootstrap.diff.txt` | new — diff artifact, generated after this report is final |
| git index | intent-to-add entry for this report (`git add -N`, explicit path), required so the diff shows the new file |
| `<scratchpad>/verify_001.py` | outside the repo — measurement script (step 4) |
| `<scratchpad>/cmp_001.sh` | outside the repo — writes the artifact, regenerates it outside the repo, runs cmp |
| `<scratchpad>/pycache/`, `<scratchpad>/regen/` | outside the repo — py_compile bytecode; regenerated diff for cmp |

`<scratchpad>` is the session temp directory; its absolute path is given
in chat only, because this report is public.

Approval: the prompt fixed the file list and the instructions to carry it
out, which CLAUDE.md rule 9 (lines 45–46) counts as approval.

## Premise checks (prompt vs files)

| Prompt premise | Finding |
|---|---|
| reports go to a gitignored `reviews/` with `latest_report.md` / `latest.diff` | Matches: CLAUDE.md:53–58, `.gitignore:41` (section D) |
| prompt_outputs/ is committed | It does not exist yet and `prompt_outputs/x` is not ignored. But **`prompt_outputs/001-bootstrap.diff.txt` IS ignored by `.gitignore:26:*.txt`** (section D), so the diff artifact cannot be committed as named without `git add -f` or a .gitignore change. Point (b). |
| Commits carry the Co-Authored-By trailer | True for 30 of 34 commits; the 4 earliest have no trailer (section E). Point (e). |
| `git add -N <every new untracked file, listed from git status>` | `git status` lists `.claude/settings.local.json` (section G). It existed before this task and is local Claude Code config. **I did not add it**, reading "new" as "created by this task"; adding it would put local settings into a public artifact. Your ruling. The diff artifact is ignored, so git status does not list it. |
| "nothing staged" | `git add -N` makes an intent-to-add index entry (no content staged). The prompt requires it; noted so it is not a surprise in `git status`. |
| "Run no tests" | CLAUDE.md rule 4 (lines 31–32) requires `py_compile` after each step. I treated it as a compile check, not a test, and ran it with bytecode redirected outside the repo (section B). Accept or drop under UNREQUESTED. |

## Step 2 — WORKING RULES vs existing CLAUDE.md

Quotes are from `cat -n CLAUDE.md` run before the edit; lines 1–94 are
unchanged (check A1), so the numbers still hold.

**WR1 — reports in prompt_outputs/, NNN-<label>-<step>.md, before chat,
append-only, errata in next report.** CONFLICTS (location, naming,
overwritten copies); SILENT on append-only and errata.

> 53 12. Every task writes its artifacts to `reviews/` at the repository root,
> 54     never to a temp or scratch directory:
> 55     `reviews/YYYY-MM-DD_HHMM_<slug>_report.md`, and for change tasks
> 56     `reviews/YYYY-MM-DD_HHMM_<slug>.diff`. Copy both to
> 57     `reviews/latest_report.md` and `reviews/latest.diff`, and report the
> 58     absolute path in the reply. Tasks with no diff write the report anyway.

`latest_report.md` / `latest.diff` are overwritten every task, which
conflicts with "append-only". "Written before replying in chat" agrees
with line 58 ("report the absolute path in the reply").

**WR2 — every claim in a prompt is unverified; report differences instead
of adapting.** AGREES on verification; CONFLICTS on the remedy (stop vs
report).

> 23 1. VERIFY BEFORE ACTING. Statements in prompts may be wrong; rule 19
> 24    governs how to check them.

> 90     instruction to write something you cannot verify. Check every premise
> 91     against the actual code before acting on it. If a premise is wrong, or
> 92     the task asks you to assert something unverified, stop and say so
> 93     rather than complying.

Rule 19 says *stop*; WR2 says *report*, without saying whether to stop.

**WR3 — do only what the prompt names; extras under "UNREQUESTED — ACCEPT
OR DROP".** AGREES on scope; differs on mechanism.

> 47 10. SCOPE IS A CEILING, not a suggestion. If a task says "investigate, do
> 48     not implement", building a prototype to test an idea is implementing.
> 49     If you believe the task needs something outside its stated scope, say
> 50     so and stop. Never do it and disclose it afterwards.

Rule 10 says *stop*; WR3 says *list and do not implement*.

**WR4 — every figure from a pasted command; never restate a figure that
lives elsewhere, quote it.** AGREES with rules 14 and 4; CONFLICTS with
rule 16's wording.

> 70 14. Do not state a path, file or fact as verified unless you ran a command
> 71     that checked it. Mark anything else "UNCLEAR" or "UNVERIFIED".

> 31 4. ONE STEP AT A TIME. After each step: run `python -m py_compile` on all
> 32    modules and show `git diff --stat`.

> 77 16. ACCOUNT FOR DELETIONS. State the insertion and deletion counts and what
> 78     every deleted line was. A deletion you did not mention is the most
> 79     expensive kind of error here.

Rule 16 says *state* the counts; WR4 and this prompt say quote them and do
not restate them.

**WR5 — diff artifact via `git diff --output=`, verified by cmp against a
regeneration outside the repo.** CONFLICTS on location and extension;
SILENT on method.

> 55     `reviews/YYYY-MM-DD_HHMM_<slug>_report.md`, and for change tasks
> 56     `reviews/YYYY-MM-DD_HHMM_<slug>.diff`. Copy both to

> 72 15. THE DIFF IS THE CLAIM. Every change, addition or deletion described in
> 73     the summary must be visible in the diff written to `reviews/`. Before

> 68 13. The diff must include new files: run `git add -N <new paths>` before
> 69     `git diff`, or the new file is missing from what Berke reviews.

Rule 13 AGREES. Rule 12's "never to a temp or scratch directory" (line 54)
is in tension with "regeneration outside the repo", unless it is read as
covering deliverables only.

**WR6 — measure with a script file; every check prints what it measured
beside its verdict.** SILENT. Closest is line 61, "the measured subject and
longest body line", which does not say how to measure.

**WR7 — stage by explicit path, never glob or `git add .`.** SILENT.

**WR8 — never commit without an approved message; never push without a
separate push approval.** AGREES.

> 51 11. Never commit or push until Berke has reviewed the summary and the diff
> 52     and said to proceed. No exceptions.

> 64     It says nothing about pushing — the push is a separate task with its
> 65     own report. A push task's report records the commits pushed with their

WR8 adds explicit approval of the message text itself.

**WR9 — subject max 50, body lines max 72, imperative.** AGREES; rule 8 is
stricter and adds the trailer.

> 36 8. Commit messages follow the 50/72 rule: subject line max 50 chars,
> 37    imperative mood, no trailing period; blank line; body wrapped at 72
> 38    chars explaining what and why. Every commit ends with the default
> 39    Co-Authored-By trailer, separated from the body by a blank line.
> 40    Trailers are exempt from the 72-char wrap and must never be wrapped.

WR9's "body lines max 72" has no trailer exemption. No practical clash
today: the trailer in use is 66 chars (section E). A longer model name
could exceed 72.

**WR10 — anything tests cannot reach needs a manual run by the user before
push.** SILENT.

## Points for your ruling

**(a) Conflicts, with recommendations**

1. *Report location and naming* (WR1 vs rule 12). Recommend: adopt
   prompt_outputs/ and NNN-<label>-<step>.md, amend rule 12 to match, drop
   the `latest_*` copies because they conflict with append-only, and amend
   the comment at `.gitignore:39–40`, which cites rule 12.
2. *Diff artifact location and extension* (WR5 vs rules 12 and 15).
   Recommend: amend rules 12 and 15 to prompt_outputs/. The `.txt`
   extension needs a ruling together with (b).
3. *Stop vs report* (WR2 vs rule 19). Recommend: report every difference;
   stop only when the difference blocks the task or would make the output
   assert something false.
4. *Stop vs list* (WR3 vs rule 10). Recommend: WR3's heading is how extras
   are surfaced; stop only if the named scope cannot be finished without
   the extra.
5. *State vs quote counts* (WR4 vs rule 16). Recommend: change rule 16 to
   "quote the numstat block and account for every deleted line".
6. *Scratch directory* (rule 12 line 54 vs WR5 and this prompt's script
   outside the repo). Recommend: limit rule 12's ban to deliverables;
   verification scratch may live outside the repo.
7. *Trailer exemption* (WR9 vs rule 8). Recommend: say in WR9 that rule 8's
   trailer exemption applies.
8. *py_compile vs "run no tests"* (rule 4 vs this prompt). Recommend: rule
   4 stays mandatory, with bytecode kept out of the repo.

**(b) .gitignore and prompt_outputs/.** `prompt_outputs/x` is not ignored
(exit 1). `prompt_outputs/001-bootstrap.diff.txt` is ignored by
`.gitignore:26:*.txt` (exit 0). See section D. .gitignore not edited.
Options: a negation such as `!prompt_outputs/*.txt` after line 26, or a
`.diff` extension. Whether `*.diff` is ignored: UNVERIFIED (not checked).

**(c) Proposed rule for public reports (not added):**

> Reports in prompt_outputs/ are public. They never contain credentials or
> tokens; the contents of, or excerpts from, gitignored or local-only files
> (examples/, tests/golden/reference.json, docs/references/, reviews/,
> unpublished notes); or absolute paths outside the repository. Write
> paths outside the repository as placeholders such as <scratchpad> or
> <home>. Measurement scripts print such paths as placeholders too.

tests/README.md:11 says `tests/_paths.py` holds "on-disk file names". So
some local data file names may already be public; UNVERIFIED whether they
match the files in examples/. That is why the wording above does not ban
file names.

**(d) reviews/.** Gitignored (`.gitignore:41`); it holds 31 entries
(section F). Not touched. Recommend: keep it as a local archive and do not
migrate it. Its reports were written on the assumption they were private,
so none should move into prompt_outputs/ without a per-file audit.

**(e) Trailer.** The exact line in git log, from section E:

    Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>

It appears on 30 of 34 commits. The 4 earliest (de8b7e1, 68dc7e4,
ee6c9d0, 55ed245) carry no trailer; the first with it is 46f60b3 "Add
Co-Authored-By rule to CLAUDE.md". No other trailer types occur.
Difference: this session's tooling supplies `Co-Authored-By: Claude Opus
5.5 (1M context) <noreply@anthropic.com>`, a different model name. That
comes from session configuration, not from git, so it is UNVERIFIED by
command. The DECISIONS.md entry needs a ruling: the fixed historical
string, or the string for the model that writes the commit. I recommend
the latter, since rule 8 says "the default" trailer and a fixed string
would misattribute.

## UNREQUESTED — ACCEPT OR DROP

- I ran `py_compile` (rule 4) despite "run no tests". Bytecode went to
  `<scratchpad>/pycache`, not the repo.
- I did not write to `reviews/` as rule 12 requires; this prompt directs
  output to prompt_outputs/. Nothing written there.
- I did not `git add -N` `.claude/settings.local.json` (see premise
  checks).
- The proposed .gitignore negation in (b) is not implemented.

## TESTS

None run. Quoted from `cat -n tests/README.md`:

> 6 | Script | Purpose | Can fail? |
> 8 | `golden/generate_golden.py` | Writes `golden/reference.json` from current program output | no |
> 9 | `golden/check_golden.py` | Reruns and compares against `reference.json`, tolerance 1e-12 | **yes**, exit 1 on drift |
> 10 | `validation/compare_manual.py` | A: formula vs the reference xlsx, tolerance 1e-9. B: measured (xlsx) vs simulated (program) counts — different methods, deltas expected | A **yes**; B report-only |
> 11 | `_paths.py` | shared helper: on-disk file names and the skip-if-missing guard | not run directly |

Run command:

> 13 Run from the repo root:
> 16 python tests/golden/generate_golden.py
> 17 python tests/golden/check_golden.py
> 18 python tests/validation/compare_manual.py

Local-only data:

> 37 The three input files are real IBA data and are **never committed**; see
> 38 `examples/README.md`. `golden/reference.json` is generated locally by
> 39 `generate_golden.py` and is gitignored too, so neither the data nor anything
> 40 derived from it enters the repository. Every script exits 0 with a `SKIP:`
> 41 message when the data is absent, so a fresh clone or CI passes without
> 42 running the checks and cannot detect regressions.

So yes, the tests need local-only data. Without it they print SKIP and exit
0.

## Verification (step 4)

Command: `python <scratchpad>/verify_001.py <scratchpad>`, run from the
repo root before this report was written. Output, verbatim:

```
=== A. CLAUDE.md byte checks ===
working-tree bytes: 6994
HEAD blob bytes (repo form, git show): 5630
HEAD bytes (working-tree form, cat-file --filters): 5724
A1 prefix == HEAD working-tree form, byte for byte: 5724 bytes compared -> PASS
A2 LF-normalised prefix == HEAD blob, byte for byte: 5630 bytes compared -> PASS
tail bytes after HEAD content: 1270
expected tail bytes (blank line + block + final newline, CRLF): 1270
A3 tail == expected (CRLF form): PASS
A4 tail == expected (LF-normalised): PASS
A5 line endings: CRLF = 118 , bare LF = 0 -> PASS
block lines: 23 | longest block line chars: 73
CLAUDE.md lines at HEAD: 94 | working tree: 118

=== B. py_compile on all tracked .py files (rule 4) ===
  exit 0 flavunato/__init__.py
  exit 0 flavunato/__main__.py
  exit 0 flavunato/element_spectra.py
  exit 0 flavunato/gui.py
  exit 0 flavunato/plotting.py
  exit 0 flavunato/uncertainty.py
  exit 0 run_flavunato.py
  exit 0 tests/_paths.py
  exit 0 tests/golden/check_golden.py
  exit 0 tests/golden/generate_golden.py
  exit 0 tests/validation/compare_manual.py
files: 11 | failures: 0 -> PASS
bytecode written under <scratchpad>/pycache, not the repo

=== C. git diff --stat / --numstat HEAD (tracked files) ===
 CLAUDE.md | 24 ++++++++++++++++++++++++
 1 file changed, 24 insertions(+)
24	0	CLAUDE.md

=== D. git check-ignore -v (exit 1 = not ignored) ===
  exit 1 prompt_outputs/x | -
  exit 1 prompt_outputs/001-bootstrap-implement.md | -
  exit 0 prompt_outputs/001-bootstrap.diff.txt | .gitignore:26:*.txt	prompt_outputs/001-bootstrap.diff.txt
  exit 0 reviews/x | .gitignore:41:reviews/	reviews/x

=== E. Commit trailers ===
  02eb764 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-18 Split the README opening into two paragraphs
  2278bfa | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-18 Record that isotope mode is unreachable
  fbe87d4 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-18 Require a report for commit and push tasks
  023f67a | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-18 Build the Word export into docs/
  df787a4 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-18 Fold rule 1's verify requirement into rule 19
  7bf9423 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-18 Add review workflow rules to CLAUDE.md
  92cd4f6 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-18 Add Word (.docx) export for the Markdown docs
  f162c46 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-17 Sharpen documentation wording and scope claims
  7efef9a | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-17 Rename the reference in compare_manual header
  f923e77 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-17 Correct stale citations and align reference wording
  9361a9e | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-17 Drop the command line from the documentation
  c0f5d0d | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-17 Remove the command-line entry points
  f2c2259 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-17 Separate Diallo's 0 % rule from program reading
  2cfeb07 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-17 Document isotope cross-section defaults and gaps
  216b7b8 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Add README, installation and user guide
  11328eb | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Tag Diallo equations and trim thesis export
  41d5934 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Add LaTeX export of methodology
  a83c814 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Add methodology documentation and bibliography
  aea7497 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Add reference notes and document A_A fallbacks
  ccedcb2 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Document chi-squared findings and test data limit
  ccf4aca | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Remove unused imports and dead code
  fee53f4 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Stop uncertainty import failure resetting flag
  3baab9d | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Update stale module names in messages and title
  2a038c8 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Make CLI output robust on non-UTF-8 consoles
  f66c01a | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-15 Restructure modules into flavunato package
  7905b6c | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-15 Adopt full-support ROIs as reference
  08da1b2 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-15 Normalise line endings via .gitattributes
  47054c4 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-15 Add golden and manual validation tests
  ede621e | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-15 Keep example data local and document inputs
  46f60b3 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-15 Add Co-Authored-By rule to CLAUDE.md
  55ed245 | (no trailer) | 2026-09-15 Restore original xnra_* module names
  ee6c9d0 | (no trailer) | 2026-09-15 Add CLAUDE.md
  68dc7e4 | (no trailer) | 2026-09-15 Add .gitignore
  de8b7e1 | (no trailer) | 2026-09-15 Thesis version (as used for IBA analysis)
commits: 34
   30 x Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | chars: 66
   4 x (no trailer) | chars: 12

=== F. reviews/ (gitignored, not touched) ===
entries in reviews/: 31

=== G. git status --porcelain=v1 -uall ===
 M CLAUDE.md
?? .claude/settings.local.json
HEAD: 02eb764
```

Notes on what the checks prove:

- Line endings. The repo stores LF (`.gitattributes`: `* text=auto`); the
  Windows working tree has CRLF. A1 checks the working-tree form, A2 the
  repo form. The block was appended in CRLF to match the file (A5), so the
  committed content will be LF.
- Byte-for-byte limit. A3/A4 compare against a copy of the block that I
  typed into the script from the prompt. That copy and the appended text
  come from the same source, so this check cannot catch a transcription
  error in both. Compare the `+` lines in the diff artifact against your
  prompt to close that gap.
- Trailing newline. The appended text ends with a final newline (counted
  in the 1270 expected tail bytes). The prompt's block does not say
  whether it has one.

Deletions: section C shows the CLAUDE.md numstat (`24	0	CLAUDE.md`).
This report's own line count cannot appear inside itself; the numstat of
the final artifact is in the chat reply.

## Remaining steps after this report

1. `<scratchpad>/cmp_001.sh` runs `git add -N
   prompt_outputs/001-bootstrap-implement.md`, writes the artifact with
   the prompt's exact `git diff --output=` command, regenerates it into
   `<scratchpad>/regen/`, and runs cmp. The result is reported in chat.
2. Gate: nothing staged beyond the intent-to-add entry, nothing committed,
   nothing pushed.
