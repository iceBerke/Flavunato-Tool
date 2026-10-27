# 001 — bootstrap — gate

Task: apply the rulings to CLAUDE.md and .gitignore, create DECISIONS.md,
stage by explicit path, propose the commit message. Stops before
committing: nothing committed, nothing pushed.

No test suite was run: the tests need local-only data (see
001-bootstrap-implement.md, TESTS). py_compile was run per rule 4
(section E below).

## Errata for 001-bootstrap-implement.md (frozen, not edited)

1. Premise table, row "prompt_outputs/ is committed": "It does not exist
   yet" is wrong as written. The directory existed when the report was
   written, since the report was in it. It should read "it did not exist
   before task 001".
2. Its CLAUDE.md and tests/README.md quotes come from `cat -n` runs whose
   full output was not pasted; only the quoted excerpts were. Under the
   new working rule on figures, the line numbers should have come with
   pasted command output. Section A1 of that report shows lines 1–94 were
   unchanged, so the numbers were correct.

## Files touched

| Path | Change |
|---|---|
| `CLAUDE.md` | rules 4, 8, 10, 12, 15, 16, 19 amended; rule 20 added; Working rules block unchanged (B1–B3) |
| `.gitignore` | `.claude/settings.local.json` added; `!prompt_outputs/*.txt` added after `*.txt`; reviews/ comment rewritten |
| `DECISIONS.md` | new, five rulings dated 2026-10-27 |
| `prompt_outputs/001-bootstrap-gate.md` | new — this report |
| `prompt_outputs/001-bootstrap.diff.txt` | regenerated |
| `prompt_outputs/001-bootstrap-implement.md` | unchanged (section A); staged |
| `<scratchpad>/check_gate.py`, `<scratchpad>/cmp_gate.sh`, `<scratchpad>/commit_msg.txt` | outside the repo: measurement, artifact/cmp/staging, commit message under test |
| `<scratchpad>/pycache/`, `<scratchpad>/regen/` | outside the repo: bytecode; regenerated diff for cmp |

Approval: the prompt fixed the file list and the steps, which rule 9
counts as approval.

## Premise checks (prompt vs files)

| Prompt premise | Finding |
|---|---|
| Frozen report: 20967 bytes, sha256 51ee07…59e6, LF | Matches in both forms; the file has no CRLF (section A). |
| `*.txt` at expected line 26 | True at HEAD. I added `.claude/settings.local.json` above it in the IDE / OS block, so `*.txt` is now line 27 and the negation line 28 (section D shows `.gitignore:27` and `:28`). |
| Comment citing rule 12 at expected lines 39–40 | True at HEAD (diff hunk `@@ -36,8 +38,8 @@`, deleted lines quoted below); now lines 41–42. |
| "Rules 1/19" (a3) | Rule 1 only defers to rule 19 ("rule 19 governs how to check them"), so only rule 19 was changed. Rule 1 is unchanged. |
| Verify that the artifact is NOT ignored with `git check-ignore -v` | With `-v`, git exits 0 for any matching pattern, including a `!` negation. My script's first run read exit 0 as "ignored" and printed FAIL for the artifact and for the `requirements.txt` control. The printed patterns (`!prompt_outputs/*.txt`, `!requirements.txt`) showed both are *not* ignored. I fixed the verdict to read the pattern; section D is the rerun. I used `--no-index` so that a staged file still gets checked against the patterns. |
| Where to put `.claude/settings.local.json` | Not specified; I put it in the `# IDE / OS` block. |

## Changes, item by item

Diff hunks are in the artifact; the deleted lines are listed below.

- **a1, a6 — rule 12.** Reports go to `prompt_outputs/NNN-<label>-<step>.md`,
  with one diff artifact per task, `prompt_outputs/NNN-<label>.diff.txt`.
  The `latest_*` copies are dropped. The scratch-directory ban now reads
  "(this covers deliverables only; verification scratch may live outside
  the repo)". This sentence is appended at the end: "Commit and push
  reports are written after the commit, stay untracked, and are committed
  with the next task." The rest of rule 12 is unchanged, including
  "Report the absolute path in the reply".
- **a2 — reviews/ mentions.** Found in tracked files outside reviews/ and
  prompt_outputs/ before the edit (Grep for `reviews/|latest_report|latest\.diff`):

  ```
  .gitignore:41:reviews/
  CLAUDE.md:53:12. Every task writes its artifacts to `reviews/` at the repository root,
  CLAUDE.md:55:    `reviews/YYYY-MM-DD_HHMM_<slug>_report.md`, and for change tasks
  CLAUDE.md:56:    `reviews/YYYY-MM-DD_HHMM_<slug>.diff`. Copy both to
  CLAUDE.md:57:    `reviews/latest_report.md` and `reviews/latest.diff`, and report the
  CLAUDE.md:73:    the summary must be visible in the diff written to `reviews/`. Before
  ```

  - CLAUDE.md:53, 55–57 became the rule 12 text above (prompt_outputs/).
  - CLAUDE.md:73 (rule 15) now says `prompt_outputs/`.
  - `.gitignore:41` `reviews/` stays; the comment above it now says it is
    a local archive and that reports go to prompt_outputs/.
  - CLAUDE.md:69, "what Berke reviews", is the verb, not the folder, so
    it is unchanged.

  After the edit, section C shows the only remaining mentions: rule 20's
  list of local-only paths, the `.gitignore` pattern, and DECISIONS.md.
- **a3 — rule 19.** Now: "Report every difference between the prompt and
  the files; stop only when the difference blocks the task or would make
  the output assert something false." The existing "If the task asks you
  to assert something unverified, stop and say so rather than complying."
  is kept. See ruling point 1.
- **a4 — rule 10.** "say so and stop" becomes: list the extra under
  "UNREQUESTED — ACCEPT OR DROP", do not implement it, and stop only if
  the named scope cannot be finished without it.
- **a5 — rule 16.** Now: "Quote the numstat block and account for every
  deleted line."
- **a7 — rule 8.** Appended: the exemption also covers the body-line limit
  in the Working rules section; only the Co-Authored-By trailer, with the
  model name Claude Code supplies; no other trailers (e.g. session links).
- **a8 — rule 4.** Now: "(mandatory; bytecode written outside the repo)".
- **c — rule 20.** Added with the given wording, wrapped to the file's
  4-space indent. B4 confirms the words are identical once whitespace is
  normalised.
- **.gitignore.** The two lines and the comment above; nothing else.
- **DECISIONS.md.** Five entries, one per ruling.

### Every deleted line

From `bash <scratchpad>/cmp_gate.sh <scratchpad> gen`, run before this
report. The numbers are artifact line numbers from that run; the deleted
text does not change on regeneration.

```
22:-# Review artifacts: per-task reports and diffs, local only. See CLAUDE.md
23:-# rule 12.
37:-   modules and show `git diff --stat`.
47:-   Trailers are exempt from the 72-char wrap and must never be wrapped.
59:-    If you believe the task needs something outside its stated scope, say
60:-    so and stop. Never do it and disclose it afterwards.
67:-12. Every task writes its artifacts to `reviews/` at the repository root,
68:-    never to a temp or scratch directory:
69:-    `reviews/YYYY-MM-DD_HHMM_<slug>_report.md`, and for change tasks
70:-    `reviews/YYYY-MM-DD_HHMM_<slug>.diff`. Copy both to
71:-    `reviews/latest_report.md` and `reviews/latest.diff`, and report the
72:-    absolute path in the reply. Tasks with no diff write the report anyway.
86:-    `git log origin/<branch>..HEAD` is empty afterwards.
95:-    the summary must be visible in the diff written to `reviews/`. Before
100:-16. ACCOUNT FOR DELETIONS. State the insertion and deletion counts and what
101:-    every deleted line was. A deletion you did not mention is the most
102:-    expensive kind of error here.
113:-    against the actual code before acting on it. If a premise is wrong, or
114:-    the task asks you to assert something unverified, stop and say so
115:-    rather than complying. Doing this is never a failure to follow
116:-    instructions.
```

- 22–23: the old .gitignore comment (rewritten).
- 37: rule 4 (rewrapped with the a8 text).
- 47: rule 8's last line (now ends in ";" and continues with a7).
- 59–60: rule 10 (a4).
- 67–72: rule 12 head (a1, a6).
- 86: rule 12 last line (re-added with the a1 sentence).
- 95: rule 15 (a2).
- 100–102: rule 16 (a5).
- 113–116: rule 19 (a3, rewrapped).

Numstat at that run:

```
4	2	.gitignore
59	19	CLAUDE.md
16	0	DECISIONS.md
375	0	prompt_outputs/001-bootstrap-implement.md
```

## Points for your ruling

1. **Rule 19 now contradicts itself.** The new text says:

   > Report every difference between the prompt and the files; stop only
   > when the difference blocks the task or would make the output assert
   > something false.

   The kept text says:

   > If the task asks you to assert something unverified, stop and say so
   > rather than complying.

   "Stop only when" lists two conditions; the kept sentence adds a third
   (unverified, not false). I kept it because a3 did not ask for its
   removal. Options: drop it and rely on rule 14 ("Mark anything else
   UNCLEAR or UNVERIFIED"), or add "or unverified" to the new sentence.
   I recommend the latter, because it keeps the guard against unverified
   public claims.
2. **The push trailer check has no home in CLAUDE.md.** DECISIONS.md
   records "A push task checks the trailer's key, count and position
   only." No CLAUDE.md rule says a push checks trailers. Rule 12's list of
   what a push report records does not mention it:

   > A push task's report records the commits pushed with their
   > hashes and subjects, the remote and branch, the exit code, and that
   > `git log origin/<branch>..HEAD` is empty afterwards.

   Should rule 12 gain it?
3. **Rule 15 now has one line longer than its neighbours.** I kept the
   edit to a single line instead of rewrapping the paragraph. Rewrap or
   leave?
4. **Rule 4 timing.** "After each step" — I ran py_compile with each run
   of the check script, not after each individual edit.
5. **Staged content against rule 20.** Section H read by hand: all 6 hits
   are the words "tokens" or "Secrets" in rule text, the pre-existing
   `.gitignore:13` and `:15`, or the frozen report's quoted proposal. None
   is a credential. No absolute paths outside the repo were found, and no
   local `examples/` file name occurs. No breach found. The frozen report
   names `.claude/settings.local.json` and counts the entries in reviews/;
   both are names or counts, not contents. This report and the final
   artifact are rescanned after staging; the result is in chat.

## UNREQUESTED — ACCEPT OR DROP

- Extra check-ignore controls in section D (`docs/notes.txt`,
  `prompt_outputs/sub/x.txt`, `requirements.txt`). Measurement only.
- Rule 15 rewrap (point 3): not done.

## Verification

`python <scratchpad>/check_gate.py <scratchpad>`, run from the repo root
before this report (after the section D fix). Output, verbatim:

```
=== A. Frozen report prompt_outputs/001-bootstrap-implement.md ===
working-tree form: bytes 20967 | sha256 51ee072e994b1b237565e67a75949746ad566dd5272c44586a668b07c16259e6
  bytes == 20967: PASS | sha256 == given: PASS
LF-normalised form: bytes 20967 | sha256 51ee072e994b1b237565e67a75949746ad566dd5272c44586a668b07c16259e6
  bytes == 20967: PASS | sha256 == given: PASS
CRLF count: 0 | LF count: 375
git hash-object (clean form): 9af43e1db5264575f2596b464e73c2bf0cc1b2f8
index entry: 100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0	prompt_outputs/001-bootstrap-implement.md

=== B. Working rules block in CLAUDE.md unchanged ===
block chars in CLAUDE.md (from header to EOF, LF): 1243
block chars from implement-step artifact '+' lines: 1243
B1 CLAUDE.md block == implement artifact block: PASS
block chars from <scratchpad>/verify_001.py literal: 1243
B2 CLAUDE.md block == verify_001.py literal: PASS
B3 exactly one blank line before header: PASS
rule 20 words in CLAUDE.md: 53 | given: 53
B4 rule 20 == given wording (whitespace-normalised): PASS
CLAUDE.md line endings: CRLF 134 | bare LF 0 -> PASS
.gitignore line endings: CRLF 48 | bare LF 0 -> PASS

=== C. Mentions of reviews/ / latest_* (working tree) ===
  CLAUDE.md:107 |     reviews/, unpublished notes); or absolute paths outside the
  .gitignore:43 | reviews/
  DECISIONS.md:9 | - **reviews/ stays a local, gitignored archive.** It is not migrated.

=== D. git check-ignore --no-index -v ===
  exit 0 | pattern !prompt_outputs/*.txt | ignored False (want False) prompt_outputs/001-bootstrap.diff.txt -> PASS
  exit 0 | pattern .claude/settings.local.json | ignored True (want True) .claude/settings.local.json -> PASS
  exit 0 | pattern reviews/ | ignored True (want True) reviews/x -> PASS
  exit 0 | pattern *.txt | ignored True (want True) notes.txt -> PASS
  exit 0 | pattern *.txt | ignored True (want True) docs/notes.txt -> PASS
  exit 0 | pattern *.txt | ignored True (want True) prompt_outputs/sub/x.txt -> PASS
  exit 0 | pattern !requirements.txt | ignored False (want False) requirements.txt -> PASS

=== E. py_compile on all tracked .py files (rule 4) ===
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

=== F. Proposed commit message (<scratchpad>/commit_msg.txt) ===
  L1   45 chars (max 50) PASS | Adopt working rules and public prompt reports
  L2    0 chars (max 72) PASS | 
  L3   67 chars (max 72) PASS | Append the shared working rules to CLAUDE.md and align the existing
  L4   67 chars (max 72) PASS | rules with them: reports and diff artifacts now go to the committed
  L5   66 chars (max 72) PASS | prompt_outputs/ folder, reviews/ stays a local archive, and public
  L6   59 chars (max 72) PASS | reports must not contain credentials or local-only content.
  L7    0 chars (max 72) PASS | 
  L8   70 chars (max 72) PASS | Record these rulings and the trailer choice in a new DECISIONS.md, and
  L9   69 chars (max 72) PASS | let .gitignore admit prompt_outputs/*.txt while ignoring local Claude
  L10  14 chars (max 72) PASS | Code settings.
blank line 2: PASS
subject trailing period: PASS

=== G. git diff --stat HEAD / git status ===
 .gitignore                                |   6 +-
 CLAUDE.md                                 |  78 ++++-
 DECISIONS.md                              |  16 +
 prompt_outputs/001-bootstrap-implement.md | 375 ++++++++++++++++++++
 prompt_outputs/001-bootstrap.diff.txt     | 555 ++++++++++++++++++++++++++++++
 5 files changed, 1009 insertions(+), 21 deletions(-)
 M .gitignore
 M CLAUDE.md
 A DECISIONS.md
 A prompt_outputs/001-bootstrap-implement.md
 A prompt_outputs/001-bootstrap.diff.txt
HEAD: 02eb764

=== H. Public-report scan of the files to be staged ===
  CLAUDE.md:105 pattern (?i)\btoken | or tokens; the contents of, or excerpts from, gitignored or local-only
  .gitignore:13 pattern (?i)secret | # Secrets (never commit the PAT)
  .gitignore:15 pattern (?i)\btoken | *.token
  prompt_outputs/001-bootstrap-implement.md:185 pattern (?i)\btoken | > tokens; the contents of, or excerpts from, gitignored or local-only files
  missing: prompt_outputs/001-bootstrap-gate.md
  prompt_outputs/001-bootstrap.diff.txt:123 pattern (?i)\btoken | +    or tokens; the contents of, or excerpts from, gitignored or local-only
  prompt_outputs/001-bootstrap.diff.txt:365 pattern (?i)\btoken | +> tokens; the contents of, or excerpts from, gitignored or local-only files
examples/ local file names checked: 3
hits: 6 (each needs a human read; 0 -> PASS) -> FAIL
```

Notes:
- Section H's FAIL is the script's "0 hits" bar. The hits were read by
  hand; see ruling point 5.
- In section G, the stat counts the old artifact (`555`) because `git add
  -N` had made it intent-to-add. The artifact excludes itself, so it does
  not appear in its own diff.
- `.claude/settings.local.json` no longer shows as untracked (section G),
  consistent with section D.

## Proposed commit message (approval needed; trailer not included)

```
Adopt working rules and public prompt reports

Append the shared working rules to CLAUDE.md and align the existing
rules with them: reports and diff artifacts now go to the committed
prompt_outputs/ folder, reviews/ stays a local archive, and public
reports must not contain credentials or local-only content.

Record these rulings and the trailer choice in a new DECISIONS.md, and
let .gitignore admit prompt_outputs/*.txt while ignoring local Claude
Code settings.
```

All lines are within limits (section F). No fixes proposed. One content
check: the body says "reports and diff artifacts now go to the committed
prompt_outputs/ folder". That matches rule 12 as amended. Commit and push
reports are the exception: they stay untracked until the next task. The
message does not mention that; it is accurate as a summary.

## Staged state

`git diff --cached --numstat` after `bash <scratchpad>/cmp_gate.sh
<scratchpad> stage` (explicit paths). The rows for this report and the
artifact were not final at that point:

```
4	2	.gitignore
59	19	CLAUDE.md
16	0	DECISIONS.md
335	0	prompt_outputs/001-bootstrap-gate.md
375	0	prompt_outputs/001-bootstrap-implement.md
896	0	prompt_outputs/001-bootstrap.diff.txt
```

The same run showed `git status`: `M` for CLAUDE.md and .gitignore, `A` for
the other four paths, and no unstaged changes. The artifact and this
report were then regenerated and re-staged; their final rows are in chat.
