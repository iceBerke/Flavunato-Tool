# 001 — bootstrap — gate 3

Task: apply the rulings on points 1–2 of 001-bootstrap-gate2.md (point 3:
no change), run a read-only audit of the rule files, and restage by
explicit path. This replaces 001-bootstrap-gate2.md as the final gate of
task 001. Stops before committing: nothing committed, nothing pushed.

No test suite was run: the tests need local-only data (see
001-bootstrap-implement.md, TESTS). py_compile was run per rule 4
(section E).

## Errata

None for 001-bootstrap-gate2.md. I re-read its premise table, change
quotes, deleted-line list and ruling points against the files and found no
error. Nothing new for the two earlier reports.

## Files touched

| Path | Change |
|---|---|
| `CLAUDE.md` | rule 8 only, lines 39–40 (section B). Working rules block identical (B1). |
| `DECISIONS.md` | "Prompt/file differences" entry only (section B). |
| `.gitignore` | unchanged (B3) |
| `prompt_outputs/001-bootstrap-gate3.md` | new — this report |
| `prompt_outputs/001-bootstrap.diff.txt` | regenerated |
| three frozen reports | unchanged (section A); restaged by explicit path |
| `<scratchpad>/check_gate3.py`, `audit_quotes.py`, `insert_block.py`, `cmp_gate3.sh` | outside the repo: measurement, audit quotes, verbatim insertion of script output into this report, artifact/cmp/staging |

Approval: the prompt fixed the file list and the steps, which rule 9
counts as approval.

## Premise checks (prompt vs files)

| Prompt premise | Finding |
|---|---|
| Three frozen reports at the given bytes and sha256 | All three match in both forms; each index blob equals the working file (section A). |
| DECISIONS.md entry at expected lines 15–16 | True before the edit (section B: old line 16 replaced, line 15 unchanged). After the edit it spans 15–17 (audit quotes). |
| Rule 8 lacks an explicit count | True: "Every commit ends with the default Co-Authored-By trailer" (section B, `-39`/`-40`). |

## Changes

Quoted from section B (gate-2 staged version vs working tree).

**1. DECISIONS.md, "Prompt/file differences"**

Before:

> - **Prompt/file differences** are reported; work stops only when a
>   difference blocks the task (CLAUDE.md rule 19).

After:

> - **Prompt/file differences** are reported; work stops only when a
>   difference blocks the task or would make the output assert something
>   false or unverified (CLAUDE.md rule 19).

C2 confirms that the only change is the inserted clause. The clause's
wording is copied from rule 19.

**2. CLAUDE.md rule 8**

Before:

> Every commit ends with the default
> Co-Authored-By trailer, separated from the body by a blank line.

After:

> Every commit ends with exactly one
> default Co-Authored-By trailer, separated from the body by a blank line.

C1 confirms the only word change is "the" → "exactly one". The two lines
were rewrapped in place, with no line added; the longest rule 8 line is
in section B.

Deleted lines vs HEAD: listed by `cmp_gate3.sh gen` in the "Every deleted
line" section below.

## AUDIT (read-only)

Scope: every line of CLAUDE.md, DECISIONS.md and the .gitignore comments,
after the two edits. Quotes are from `python <scratchpad>/audit_quotes.py`,
pasted verbatim under "Audit quotes". The cross-reference and existence
checks are in section D of the verification output.

### Findings

**A1 — CONTRADICTION: rule 9 vs Working rules, first bullet.**

> CLAUDE.md:45–47: "9. ANNOUNCE BEFORE ACTING, AND WAIT. For any task
> that changes files, first report the exact file list, what each change
> is, and why. Then stop and wait for approval before writing anything."

> CLAUDE.md:113–114: "- Every prompt gets a report in prompt_outputs/,
> named NNN-<label>-<step>.md, written before replying in chat."

Take a change prompt that does not fix its file list (rule 9's exception
at :49–50 does not apply). Rule 9 forbids writing anything before
approval, but the working rule requires a report file before the reply
that asks for approval. Both cannot be followed.
Recommend: add to rule 9, after "before writing anything", the words
"except this prompt's own report, which carries the announcement".
**Fix before this commit**: this commit is meant to leave the rules
consistent, and the fix is one clause.

**A2 — GAP: who adds the trailer to an approved message.**

> CLAUDE.md:39–40: "Every commit ends with exactly one default
> Co-Authored-By trailer, separated from the body by a blank line."

> CLAUDE.md:130: "- Never commit without an approved message; …"

The gate prompts say "The trailer is NOT part of the approved text;
COMMIT adds it." No rule says so. Read literally, the committed message
(approved text plus trailer) is not the approved message.
Recommend: add to rule 8 "The approved message excludes the trailer; the
commit step appends it." **Fix before this commit**, or restate it in the
COMMIT prompt, because the very next step depends on it.

**A3 — GAP: the manual-run requirement has no record.**

> CLAUDE.md:134: "- Anything tests cannot reach needs a manual run by the
> user before push."

> CLAUDE.md:71–74: "A push task's report records the commits pushed with
> their hashes and subjects, the remote and branch, the exit code, and
> that `git log origin/<branch>..HEAD` is empty afterwards and that the
> trailer's key, count and position match rule 8."

No rule says who decides what "tests cannot reach", or where the user's
manual run is confirmed. The push-report list does not include it.
Recommend: add "whether a manual run was needed and, if so, the user's
confirmation" to the push-report list. **Defer** to the first push that
touches code. The task-001 push changes only documentation and rule
files (staged list below), so there is no program behaviour for tests to
miss.

No STALE REFERENCE findings: every rule number cited exists, and every
file, folder and tag checked exists (section D).

### What was checked (one line each)

- Header (:1–4): tag v1.0-thesis exists (D). "Code version 1.0.0" is a
  claim, not a reference, and was not checked.
- Modules (:6–20): all five module files, `run_flavunato.py` and
  `requirements.txt` exist; the three `*_AVAILABLE` flags exist in
  gui.py (D). The import claims are program behaviour and outside this
  audit.
- Rule 1: cites rule 19, which exists (D); consistent with it.
- Rule 2: cites rule 9, which exists (D); consistent.
- Rule 3: the golden test exists (D). "stop and ask" is a different
  trigger from rule 19, so there is no clash.
- Rule 4: consistent with the Working rules (a script runs py_compile and
  prints its result).
- Rule 5: "Mark … UNVERIFIED" vs rule 19 — no clash, per your ruling on
  gate-2 point 3.
- Rules 6, 7: no conflicts.
- Rule 8: now states the count; consistent with rule 12 :74 and
  DECISIONS :10–12. See A2.
- Rule 9: see A1.
- Rule 10: consistent with the Working rules "UNREQUESTED" bullet.
- Rule 11: consistent with Working rules :130–131.
- Rule 12: folder and naming match the Working rules and `.gitignore:28`.
  Its rule 8 cross-reference exists. "Report the absolute path in the
  reply" concerns the reply, not a report, so rule 20 does not apply.
  See A3.
- Rule 13: consistent with explicit-path staging.
- Rules 14, 17, 18: no conflicts.
- Rule 15: points to prompt_outputs/, which exists (D).
- Rule 16: consistent with the Working rules figures bullet.
- Rule 19: consistent with DECISIONS :15–17 after edit 1.
- Rule 20: all four local-only paths it names are gitignored (D).
- Working rules: see A1 (first bullet) and A3 (last bullet); the rest
  agree with rules 8, 10, 11, 12, 16.
- DECISIONS :7–8 (rule 20), :9 (reviews/ ignored, D), :10–12 (rule 8,
  rule 12), :13–14 (`.gitignore:23`, `:28`), :15–17 (rule 19): all
  consistent.
- .gitignore comments :13, :18, :25, :34: descriptive, no references.
  :37 cites `docs/latex/README.md`, which exists (D). :41–42 cite rule 12,
  which exists (D) and matches its content. :45–46 ("must come after
  !docs/**/*.pdf above"): `!docs/**/*.pdf` is at line 36, above
  `docs/references/*` at 47 (audit quotes).

### Audit quotes

```
--- CLAUDE.md (total lines: 134)
CLAUDE.md:37: 8. Commit messages follow the 50/72 rule: subject line max 50 chars,
CLAUDE.md:38:    imperative mood, no trailing period; blank line; body wrapped at 72
CLAUDE.md:39:    chars explaining what and why. Every commit ends with exactly one
CLAUDE.md:40:    default Co-Authored-By trailer, separated from the body by a blank line.
CLAUDE.md:41:    Trailers are exempt from the 72-char wrap and must never be wrapped;
CLAUDE.md:42:    the exemption also covers the body-line limit in the Working rules
CLAUDE.md:43:    section. Only the Co-Authored-By trailer, with the model name Claude
CLAUDE.md:44:    Code supplies; no other trailers (e.g. session links).
CLAUDE.md:45: 9. ANNOUNCE BEFORE ACTING, AND WAIT. For any task that changes files,
CLAUDE.md:46:    first report the exact file list, what each change is, and why. Then
CLAUDE.md:47:    stop and wait for approval before writing anything. This covers files
CLAUDE.md:48:    outside the repo and throwaway test files in temp directories — if you
CLAUDE.md:49:    would create it, name it first. If the prompt itself fixes the file
CLAUDE.md:50:    list and says to proceed, that is the approval; do not ask twice.

CLAUDE.md:57: 11. Never commit or push until Berke has reviewed the summary and the diff
CLAUDE.md:58:     and said to proceed. No exceptions.

CLAUDE.md:65:     A read-only task's report stands alone. A commit task's report records
CLAUDE.md:66:     at minimum the commit hash, the staged file list, and the measured
CLAUDE.md:67:     subject and longest body line; it names the diff file from the change
CLAUDE.md:68:     task that produced the change rather than writing a new one, since
CLAUDE.md:69:     post-commit `git diff` is empty and a regenerated diff would mislead.
CLAUDE.md:70:     It says nothing about pushing — the push is a separate task with its
CLAUDE.md:71:     own report. A push task's report records the commits pushed with their
CLAUDE.md:72:     hashes and subjects, the remote and branch, the exit code, and that
CLAUDE.md:73:     `git log origin/<branch>..HEAD` is empty afterwards and that the
CLAUDE.md:74:     trailer's key, count and position match rule 8. Commit and push
CLAUDE.md:75:     reports are written after the commit, stay untracked, and are
CLAUDE.md:76:     committed with the next task.

CLAUDE.md:113: - Every prompt gets a report in prompt_outputs/, named
CLAUDE.md:114:   NNN-<label>-<step>.md, written before replying in chat. Reports are
CLAUDE.md:115:   append-only; errors in an earlier report are recorded as errata in the
CLAUDE.md:116:   next one.

CLAUDE.md:130: - Never commit without an approved message; never push without a
CLAUDE.md:131:   separate push approval.
CLAUDE.md:132: - Commit messages: subject max 50 characters, body lines max 72,
CLAUDE.md:133:   imperative mood.
CLAUDE.md:134: - Anything tests cannot reach needs a manual run by the user before push.

--- DECISIONS.md (total lines: 17)
DECISIONS.md:7: - **prompt_outputs/ is committed and public.** Reports there follow the
DECISIONS.md:8:   public-report rule, CLAUDE.md rule 20.
DECISIONS.md:9: - **reviews/ stays a local, gitignored archive.** It is not migrated.
DECISIONS.md:10: - **Trailers.** Co-Authored-By only, with the model name Claude Code
DECISIONS.md:11:   supplies (CLAUDE.md rule 8). A push task checks the trailer's key,
DECISIONS.md:12:   count and position only. No session trailer.
DECISIONS.md:13: - **.gitignore** admits prompt_outputs/*.txt; .claude/settings.local.json
DECISIONS.md:14:   stays local.
DECISIONS.md:15: - **Prompt/file differences** are reported; work stops only when a
DECISIONS.md:16:   difference blocks the task or would make the output assert something
DECISIONS.md:17:   false or unverified (CLAUDE.md rule 19).

--- .gitignore (total lines: 48)
.gitignore:13: # Secrets (never commit the PAT)

.gitignore:18: # IDE / OS

.gitignore:23: .claude/settings.local.json

.gitignore:25: # Data: never commit real IBA data. examples/ holds local-only inputs.

.gitignore:28: !prompt_outputs/*.txt

.gitignore:34: # Generated outputs

.gitignore:36: !docs/**/*.pdf
.gitignore:37: # Word export of docs/*.md -- built locally, see docs/latex/README.md

.gitignore:41: # Earlier review reports and diffs: a local archive, not migrated. New
.gitignore:42: # reports go to the committed prompt_outputs/; see CLAUDE.md rule 12.

.gitignore:45: # Reference documents: local until their authors approve publication.
.gitignore:46: # Must come after !docs/**/*.pdf above -- last matching rule wins.
.gitignore:47: docs/references/*
```

## Points for your ruling

1. A1, A2, A3 above. I recommend fixing A1 and A2 before this commit
   and deferring A3.
2. **Commit message is still accurate.** The rule 8 count and the
   DECISIONS entry fall under "align the existing rules with them" and
   "Record these rulings … in a new DECISIONS.md". Nothing in the body is
   false after this gate. If A1/A2 are fixed before committing, the same
   phrases cover them.
3. **Rule 20:** no breach found. Section H's hits through gate2.md are
   the same files and line numbers as the gate-2 final scan, which I read
   by hand there. The new hits are in this report and in the artifact
   lines that carry it; the final rescan and my reading are in chat.

## UNREQUESTED — ACCEPT OR DROP

- None implemented. The A1–A3 recommendations are proposals only.

## Commit message (quoted by script from 001-bootstrap-gate.md; section F)

Not retyped here. Section F prints it line by line with lengths; all
lines are within limits. Trailer not included; COMMIT adds it.

## Verification

`python <scratchpad>/check_gate3.py <scratchpad>`, run from the repo root
before restaging, with output saved to a file and inserted here by
`insert_block.py` (no manual transcription):

```

=== A. Frozen reports ===
prompt_outputs/001-bootstrap-implement.md [working-tree] bytes 20967 (want 20967) PASS | sha256 51ee072e994b1b237565e67a75949746ad566dd5272c44586a668b07c16259e6 PASS
prompt_outputs/001-bootstrap-implement.md [LF-normalised] bytes 20967 (want 20967) PASS | sha256 51ee072e994b1b237565e67a75949746ad566dd5272c44586a668b07c16259e6 PASS
  index blob 9af43e1db5264575f2596b464e73c2bf0cc1b2f8 | working clean blob 9af43e1db5264575f2596b464e73c2bf0cc1b2f8 | index == working: PASS
prompt_outputs/001-bootstrap-gate.md [working-tree] bytes 17511 (want 17511) PASS | sha256 cb6b28131b474dbdde0e6dfdb3863a23dee62e99290dbaee69bd03577dcc298a PASS
prompt_outputs/001-bootstrap-gate.md [LF-normalised] bytes 17511 (want 17511) PASS | sha256 cb6b28131b474dbdde0e6dfdb3863a23dee62e99290dbaee69bd03577dcc298a PASS
  index blob 94c53ee79d78fdcab11b19b2b3d55fc2fb139bf2 | working clean blob 94c53ee79d78fdcab11b19b2b3d55fc2fb139bf2 | index == working: PASS
prompt_outputs/001-bootstrap-gate2.md [working-tree] bytes 18269 (want 18269) PASS | sha256 fa5d1f2c1f2b69990ac930ada7696928fe326bbef766e8f4ea3bea55d25c8ad3 PASS
prompt_outputs/001-bootstrap-gate2.md [LF-normalised] bytes 18269 (want 18269) PASS | sha256 fa5d1f2c1f2b69990ac930ada7696928fe326bbef766e8f4ea3bea55d25c8ad3 PASS
  index blob c626e74a57acbbdbc79dd679aa63f7a4cd6d15d1 | working clean blob c626e74a57acbbdbc79dd679aa63f7a4cd6d15d1 | index == working: PASS

=== B. Index (gate 2) vs working tree ===
CLAUDE.md: 1 changed hunk(s)
  replace old 39-40 -> new 39-40
    -39:    chars explaining what and why. Every commit ends with the default
    -40:    Co-Authored-By trailer, separated from the body by a blank line.
    +39:    chars explaining what and why. Every commit ends with exactly one
    +40:    default Co-Authored-By trailer, separated from the body by a blank line.
  B1 Working rules block identical: 1243 vs 1243 chars -> PASS
  B2 changed old lines all in rule 8 (old 37-44): PASS
  C1 rule 8 == old with 'ends with the default' -> 'ends with exactly one default': PASS
  rule 8 line lengths: [68, 70, 68, 75, 71, 69, 71, 57] max 75
DECISIONS.md: 1 changed hunk(s)
  replace old 16-16 -> new 16-17
    -16:   difference blocks the task (CLAUDE.md rule 19).
    +16:   difference blocks the task or would make the output assert something
    +17:   false or unverified (CLAUDE.md rule 19).
  C2 entry == old + inserted clause: PASS
.gitignore: 0 changed hunk(s)
  B3 .gitignore unchanged: PASS

=== D. Audit evidence: cross-references ===
numbered hard rules found: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
  CLAUDE.md:23 refers to rule 19 -> exists: PASS
  CLAUDE.md:25 refers to rule 9 -> exists: PASS
  CLAUDE.md:74 refers to rule 8 -> exists: PASS
  DECISIONS.md:8 refers to rule 20 -> exists: PASS
  DECISIONS.md:11 refers to rule 8 -> exists: PASS
  DECISIONS.md:17 refers to rule 19 -> exists: PASS
  .gitignore:42 refers to rule 12 -> exists: PASS
'Working rules' section header present: PASS
  exists flavunato/gui.py                 PASS
  exists flavunato/plotting.py            PASS
  exists flavunato/uncertainty.py         PASS
  exists flavunato/element_spectra.py     PASS
  exists flavunato/__main__.py            PASS
  exists run_flavunato.py                 PASS
  exists requirements.txt                 PASS
  exists tests/golden/check_golden.py     PASS
  exists docs/latex/README.md             PASS
  exists docs/references/README.md        PASS
  exists examples/README.md               PASS
  exists prompt_outputs                   PASS
  exists reviews                          PASS
  tag v1.0-thesis: PASS
  *_AVAILABLE names in flavunato/gui.py: ['ELEMENT_SPECTRUM_AVAILABLE', 'PLOTTING_AVAILABLE', 'UNCERTAINTY_AVAILABLE']
  rule-20 local path examples/x                   ignored: PASS (examples/*)
  rule-20 local path tests/golden/reference.json  ignored: PASS (tests/golden/reference.json)
  rule-20 local path docs/references/x            ignored: PASS (docs/references/*)
  rule-20 local path reviews/x                    ignored: PASS (reviews/)

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

=== F. Commit message quoted from 001-bootstrap-gate.md ===
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
blank line 2: PASS | no subject period: PASS

=== G. git status --porcelain ===
M  .gitignore
MM CLAUDE.md
AM DECISIONS.md
A  prompt_outputs/001-bootstrap-gate.md
A  prompt_outputs/001-bootstrap-gate2.md
A  prompt_outputs/001-bootstrap-implement.md
A  prompt_outputs/001-bootstrap.diff.txt
HEAD: 02eb764

=== H. Public-report scan of the files to be staged ===
  CLAUDE.md:105 pattern (?i)\btoken
  .gitignore:13 pattern (?i)secret
  .gitignore:15 pattern (?i)\btoken
  prompt_outputs/001-bootstrap-implement.md:185 pattern (?i)\btoken
  prompt_outputs/001-bootstrap-gate.md:187 pattern (?i)secret
  prompt_outputs/001-bootstrap-gate.md:187 pattern (?i)\btoken
  prompt_outputs/001-bootstrap-gate.md:286 pattern (?i)\btoken
  prompt_outputs/001-bootstrap-gate.md:287 pattern (?i)secret
  prompt_outputs/001-bootstrap-gate.md:288 pattern (?i)\btoken
  prompt_outputs/001-bootstrap-gate.md:289 pattern (?i)\btoken
  prompt_outputs/001-bootstrap-gate.md:291 pattern (?i)\btoken
  prompt_outputs/001-bootstrap-gate.md:292 pattern (?i)\btoken
  prompt_outputs/001-bootstrap-gate2.md:182 pattern (?i)secret
  prompt_outputs/001-bootstrap-gate2.md:182 pattern (?i)\btoken
  prompt_outputs/001-bootstrap-gate2.md:309 pattern (?i)secret
  prompt_outputs/001-bootstrap-gate2.md:312 pattern (?i)secret
  prompt_outputs/001-bootstrap-gate2.md:315 pattern (?i)secret
  prompt_outputs/001-bootstrap-gate2.md:322 pattern (?i)secret
  prompt_outputs/001-bootstrap-gate2.md:325 pattern (?i)secret
  missing: prompt_outputs/001-bootstrap-gate3.md
  prompt_outputs/001-bootstrap.diff.txt:125 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:369 pattern (?i)secret
  prompt_outputs/001-bootstrap.diff.txt:369 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:468 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:469 pattern (?i)secret
  prompt_outputs/001-bootstrap.diff.txt:470 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:471 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:473 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:474 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:714 pattern (?i)secret
  prompt_outputs/001-bootstrap.diff.txt:714 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:841 pattern (?i)secret
  prompt_outputs/001-bootstrap.diff.txt:844 pattern (?i)secret
  prompt_outputs/001-bootstrap.diff.txt:847 pattern (?i)secret
  prompt_outputs/001-bootstrap.diff.txt:854 pattern (?i)secret
  prompt_outputs/001-bootstrap.diff.txt:857 pattern (?i)secret
  prompt_outputs/001-bootstrap.diff.txt:1101 pattern (?i)\btoken
examples/ local file names checked: 3
hits: 36 (each needs a human read)
```

Notes:
- Section G shows `MM CLAUDE.md` and `AM DECISIONS.md`: the gate-2
  versions are staged and this gate's edits are unstaged until the stage
  step.
- Section D's cross-reference check matches "rule N" / "rules N" only.
  The reference to the "Working rules section" (CLAUDE.md:42–43) is
  covered by D's header check.

## Every deleted line (artifact vs HEAD)

From `bash <scratchpad>/cmp_gate3.sh <scratchpad> gen`, inserted by
script:

```
22:-# Review artifacts: per-task reports and diffs, local only. See CLAUDE.md
23:-# rule 12.
37:-   modules and show `git diff --stat`.
45:-   chars explaining what and why. Every commit ends with the default
46:-   Co-Authored-By trailer, separated from the body by a blank line.
47:-   Trailers are exempt from the 72-char wrap and must never be wrapped.
61:-    If you believe the task needs something outside its stated scope, say
62:-    so and stop. Never do it and disclose it afterwards.
69:-12. Every task writes its artifacts to `reviews/` at the repository root,
70:-    never to a temp or scratch directory:
71:-    `reviews/YYYY-MM-DD_HHMM_<slug>_report.md`, and for change tasks
72:-    `reviews/YYYY-MM-DD_HHMM_<slug>.diff`. Copy both to
73:-    `reviews/latest_report.md` and `reviews/latest.diff`, and report the
74:-    absolute path in the reply. Tasks with no diff write the report anyway.
88:-    `git log origin/<branch>..HEAD` is empty afterwards.
98:-    the summary must be visible in the diff written to `reviews/`. Before
99:-    reporting, re-read that file and check the summary against it. If
100:-    something you did is not in the diff, say so explicitly and explain
105:-16. ACCOUNT FOR DELETIONS. State the insertion and deletion counts and what
106:-    every deleted line was. A deletion you did not mention is the most
107:-    expensive kind of error here.
118:-    against the actual code before acting on it. If a premise is wrong, or
119:-    the task asks you to assert something unverified, stop and say so
120:-    rather than complying. Doing this is never a failure to follow
121:-    instructions.
```

Compared with the gate-2 list, the only new deleted lines are 45–46:
HEAD's rule 8 lines 39–40, replaced by edit 2. Every other line is the
same text, with the reasons given in 001-bootstrap-gate.md and
001-bootstrap-gate2.md. Line 47 was already deleted at gate 1.

## Staged state

`git diff --cached --numstat` after `bash <scratchpad>/cmp_gate3.sh
<scratchpad> stage` (explicit paths). The rows for this report and the
artifact were not final at that point:

```
4	2	.gitignore
63	23	CLAUDE.md
17	0	DECISIONS.md
344	0	prompt_outputs/001-bootstrap-gate.md
378	0	prompt_outputs/001-bootstrap-gate2.md
494	0	prompt_outputs/001-bootstrap-gate3.md
375	0	prompt_outputs/001-bootstrap-implement.md
1794	0	prompt_outputs/001-bootstrap.diff.txt
```
