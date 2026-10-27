# 001 — bootstrap — gate 2

Task: apply the rulings on points 1–3 of 001-bootstrap-gate.md (rules 19,
12, 15), restage by explicit path, re-propose the commit message. This
replaces 001-bootstrap-gate.md as the final gate of task 001. Stops before
committing: nothing committed, nothing pushed.

No test suite was run: the tests need local-only data (see
001-bootstrap-implement.md, TESTS). py_compile was run per rule 4
(section E).

## Errata for 001-bootstrap-gate.md (frozen, not edited)

1. Its ruling points missed a contradiction already present after gate 1.
   DECISIONS.md:15–16 records that work "stops only when a difference
   blocks the task", while rule 19 as amended then also stopped when the
   output "would assert something false". This gate's change widens the
   gap; see ruling point 1.

No new errata for 001-bootstrap-implement.md.

## Files touched

| Path | Change |
|---|---|
| `CLAUDE.md` | rules 12, 15, 19 only (section B: every changed line lies in those rules; Working rules block and rule 20 identical) |
| `prompt_outputs/001-bootstrap-gate2.md` | new — this report |
| `prompt_outputs/001-bootstrap.diff.txt` | regenerated |
| `.gitignore`, `DECISIONS.md`, both frozen reports | unchanged since gate 1; restaged by explicit path (no-op for content) |
| `<scratchpad>/check_gate2.py`, `<scratchpad>/cmp_gate2.sh` | outside the repo: measurement; artifact/cmp/staging |

Approval: the prompt fixed the file list and the steps, which rule 9
counts as approval.

## Premise checks (prompt vs files)

| Prompt premise | Finding |
|---|---|
| Frozen reports: implement 20967 B / 51ee07…59e6, gate 17511 B / cb6b28…298a | Both match in working-tree and LF-normalised form; each index blob equals the working file (section A). |
| Rule 19 has the two stop sentences quoted in the prompt | Yes, at the gate-1 lines 101–103 (section B, `-` lines). |
| Rule 12 contains "and that `git log origin/<branch>..HEAD` is empty afterwards" | Yes, at gate-1 lines 72–73 (section B, `-73`). |
| Rule 15 has a line longer than its neighbours | Yes: gate-1 line 81 (`-81` in section B). Its new length is in section D. |
| "rule 8" holds the trailer's key, count and position | Key and position: yes. Count: implied, not stated (ruling point 2). |

## Changes

Before and after are quoted from section B, which diffs the gate-1 staged
CLAUDE.md against the working tree.

**1. Rule 19** — the two stop sentences are merged; "Doing this is never a
failure to follow instructions." is kept (C1).

```
-101:     the task or would make the output assert something false. If the task
-102:     asks you to assert something unverified, stop and say so rather than
-103:     complying. Doing this is never a failure to follow instructions.
+102:     the task or would make the output assert something false or unverified.
+103:     Doing this is never a failure to follow instructions.
```

**2. Rule 12** — the push-report list gains the trailer check (C2).

Before:

> A push task's report records the commits pushed with their hashes and
> subjects, the remote and branch, the exit code, and that `git log
> origin/<branch>..HEAD` is empty afterwards. Commit and push reports are
> written after the commit, …

After:

> A push task's report records the commits pushed with their hashes and
> subjects, the remote and branch, the exit code, and that `git log
> origin/<branch>..HEAD` is empty afterwards and that the trailer's key,
> count and position match rule 8. Commit and push reports are written
> after the commit, …

```
-73:     `git log origin/<branch>..HEAD` is empty afterwards. Commit and push
+73:     `git log origin/<branch>..HEAD` is empty afterwards and that the
+74:     trailer's key, count and position match rule 8. Commit and push
```

The clause was inserted exactly where the prompt placed it. The result is
grammatical: two coordinated "that" clauses. An alternative with smoother
punctuation is "…, the exit code, that `git log …` is empty afterwards,
and that the trailer's …". It would delete the existing "and" before the
first "that", so I did not use it.

**3. Rule 15** — the paragraph is rewrapped with the same words (C3). Its
line lengths are in section D.

```
-81:     the summary must be visible in the diff written to `prompt_outputs/`. Before
-82:     reporting, re-read that file and check the summary against it. If
-83:     something you did is not in the diff, say so explicitly and explain
+82:     the summary must be visible in the diff written to `prompt_outputs/`.
+83:     Before reporting, re-read that file and check the summary against it.
+84:     If something you did is not in the diff, say so explicitly and explain
```

### Every deleted line (artifact vs HEAD)

From `bash <scratchpad>/cmp_gate2.sh <scratchpad> gen`, run before this
report. The numbers are artifact line numbers from that run.

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
96:-    the summary must be visible in the diff written to `reviews/`. Before
97:-    reporting, re-read that file and check the summary against it. If
98:-    something you did is not in the diff, say so explicitly and explain
103:-16. ACCOUNT FOR DELETIONS. State the insertion and deletion counts and what
104:-    every deleted line was. A deletion you did not mention is the most
105:-    expensive kind of error here.
116:-    against the actual code before acting on it. If a premise is wrong, or
117:-    the task asks you to assert something unverified, stop and say so
118:-    rather than complying. Doing this is never a failure to follow
119:-    instructions.
```

Compared with the gate-1 list in 001-bootstrap-gate.md, the only new
deleted lines are 97–98: HEAD's rule 15 lines, now deleted because of the
rewrap. Every other line is the same text with the reasons given there.
Rule 19's HEAD lines (116–119) were already deleted at gate 1; this gate
changes only their replacement.

## Points for your ruling

1. **DECISIONS.md contradicts the new rule 19.** DECISIONS.md:15–16:

   > - **Prompt/file differences** are reported; work stops only when a
   >   difference blocks the task (CLAUDE.md rule 19).

   CLAUDE.md:101–102:

   > Report every difference between the prompt and the files; stop only
   > when the difference blocks the task or would make the output assert
   > something false or unverified.

   DECISIONS.md is out of this prompt's scope, so I did not edit it.
   Recommend: add "or would make the output assert something false or
   unverified" to DECISIONS.md:16.
2. **Rule 8 does not state a trailer count.** The new rule 12 text asks
   that the trailer's "key, count and position match rule 8". Rule 8
   (CLAUDE.md:39–44) says:

   > Every commit ends with the default
   > Co-Authored-By trailer, separated from the body by a blank line.
   > … Only the Co-Authored-By trailer, with the model name Claude
   > Code supplies; no other trailers (e.g. session links).

   The key (Co-Authored-By) and the position (last, after a blank line)
   are stated. The count is only implied by "the … trailer". Recommend
   stating "exactly one" in rule 8.
3. **"Assert something unverified" vs marking things UNVERIFIED.** This
   is a tension rather than a contradiction. CLAUDE.md:34 (rule 5) says:

   > Mark anything unverified as "UNVERIFIED".

   CLAUDE.md:79–80 (rule 14) says:

   > Do not state a path, file or fact as verified unless you ran a command
   > that checked it. Mark anything else "UNCLEAR" or "UNVERIFIED".

   Rule 19 now stops when the output "would assert something … unverified".
   I read a statement marked UNVERIFIED as not an assertion, so the rules
   agree. Say if you want that written into rule 19.
4. **Staged content against rule 20.** Section H lists 22 hits. They are
   the same files and line numbers as the gate-1 scan, which I read by
   hand there: the words "tokens" or "Secrets" in rule text, the
   pre-existing `.gitignore:13` and `:15`, and reports quoting those. This
   report adds hits of the same kind. There are no credentials, no
   absolute paths outside the repo and no local `examples/` file names.
   The final rescan, which includes this report, is in chat.

## Commit message

Quoted from 001-bootstrap-gate.md by script (section F, which also
confirms it equals the file measured at gate 1). All lines are within
limits.

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

The body is still accurate after this gate. The rule 19, 12 and 15
changes fall under "align the existing rules with them". The push
trailer check is part of "the trailer choice", which DECISIONS.md:11–12
already records. The body does not mention the new push-report
requirement, but nothing it says is false. Trailer not included; COMMIT
adds it.

## UNREQUESTED — ACCEPT OR DROP

- None implemented. The three recommendations in ruling points 1–3 are
  proposals only.

## Verification

`python <scratchpad>/check_gate2.py <scratchpad>`, run from the repo root
before this report and before restaging. Output, verbatim:

```
=== A. Frozen reports ===
prompt_outputs/001-bootstrap-implement.md [working-tree] bytes 20967 (want 20967) PASS | sha256 51ee072e994b1b237565e67a75949746ad566dd5272c44586a668b07c16259e6 PASS
prompt_outputs/001-bootstrap-implement.md [LF-normalised] bytes 20967 (want 20967) PASS | sha256 51ee072e994b1b237565e67a75949746ad566dd5272c44586a668b07c16259e6 PASS
  index blob 9af43e1db5264575f2596b464e73c2bf0cc1b2f8 | working clean blob 9af43e1db5264575f2596b464e73c2bf0cc1b2f8 | index == working: PASS
prompt_outputs/001-bootstrap-gate.md [working-tree] bytes 17511 (want 17511) PASS | sha256 cb6b28131b474dbdde0e6dfdb3863a23dee62e99290dbaee69bd03577dcc298a PASS
prompt_outputs/001-bootstrap-gate.md [LF-normalised] bytes 17511 (want 17511) PASS | sha256 cb6b28131b474dbdde0e6dfdb3863a23dee62e99290dbaee69bd03577dcc298a PASS
  index blob 94c53ee79d78fdcab11b19b2b3d55fc2fb139bf2 | working clean blob 94c53ee79d78fdcab11b19b2b3d55fc2fb139bf2 | index == working: PASS

=== B. CLAUDE.md: index (gate 1) vs working tree ===
  replace old 73-73 -> new 73-74
    -73:     `git log origin/<branch>..HEAD` is empty afterwards. Commit and push
    +73:     `git log origin/<branch>..HEAD` is empty afterwards and that the
    +74:     trailer's key, count and position match rule 8. Commit and push
  replace old 81-83 -> new 82-84
    -81:     the summary must be visible in the diff written to `prompt_outputs/`. Before
    -82:     reporting, re-read that file and check the summary against it. If
    -83:     something you did is not in the diff, say so explicitly and explain
    +82:     the summary must be visible in the diff written to `prompt_outputs/`.
    +83:     Before reporting, re-read that file and check the summary against it.
    +84:     If something you did is not in the diff, say so explicitly and explain
  replace old 101-103 -> new 102-103
    -101:     the task or would make the output assert something false. If the task
    -102:     asks you to assert something unverified, stop and say so rather than
    -103:     complying. Doing this is never a failure to follow instructions.
    +102:     the task or would make the output assert something false or unverified.
    +103:     Doing this is never a failure to follow instructions.
old rule spans (line from-to): {12: (59, 75), 15: (80, 84), 19: (96, 103)}
B1 every changed old line lies in rule 12, 15 or 19: 7 lines -> PASS
B2 Working rules block identical: 1243 vs 1243 chars -> PASS
B3 rule 20 identical: PASS

=== C. Word checks ===
C1 rule 19 == old with the two stop sentences merged: PASS
   'Doing this is never a failure to follow instructions.' kept: PASS
C2 rule 12 == old + inserted clause: PASS
C3 rule 15 words unchanged (whitespace-normalised): 50 vs 50 words -> PASS

=== D. Line lengths in rules 12, 15, 19 (max 76) ===
  rule 12 lines 59-76 lengths [74, 72, 69, 75, 74, 54, 74, 70, 73, 70, 73, 72, 74, 71, 68, 67, 65, 33] | max 75 -> PASS
  rule 15 lines 81-85 lengths [74, 73, 73, 74, 8] | max 74 -> PASS
    continuation lines 4-space indented: PASS
  rule 19 lines 97-103 lengths [74, 73, 73, 72, 74, 75, 57] | max 75 -> PASS
    continuation lines 4-space indented: PASS

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
== <scratchpad>/commit_msg.txt (gate-1 measured file): PASS

=== G. git status --porcelain=v1 -uall ===
M  .gitignore
MM CLAUDE.md
A  DECISIONS.md
A  prompt_outputs/001-bootstrap-gate.md
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
  missing: prompt_outputs/001-bootstrap-gate2.md
  prompt_outputs/001-bootstrap.diff.txt:123 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:367 pattern (?i)secret
  prompt_outputs/001-bootstrap.diff.txt:367 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:466 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:467 pattern (?i)secret
  prompt_outputs/001-bootstrap.diff.txt:468 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:469 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:471 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:472 pattern (?i)\btoken
  prompt_outputs/001-bootstrap.diff.txt:715 pattern (?i)\btoken
examples/ local file names checked: 3
hits: 22 (each needs a human read)
```

Notes:
- `MM CLAUDE.md` in section G: the gate-1 version is staged and this
  gate's edits are unstaged until the stage step below.
- Section B diffs against the index, not HEAD. That is how it isolates
  this gate's edits from gate 1's.
- `python <scratchpad>/compare_paste.py <scratchpad>` compared the block
  above with a fresh run. Sections A–F match line for line. Section G
  differs only because of later state: the regenerated artifact shows
  `AM`, and this report shows `??`. Its output:

  ```
  pasted lines A-G: 81 | fresh lines A-G: 82
    line 80 differs:
      pasted: A  prompt_outputs/001-bootstrap.diff.txt
      fresh : AM prompt_outputs/001-bootstrap.diff.txt
    line 81 differs:
      pasted: HEAD: 02eb764
      fresh : ?? prompt_outputs/001-bootstrap-gate2.md
  A-G pasted == fresh: FAIL
  ```

  Before running it I had already fixed one transcription error of my
  own: I had pasted section G with the DECISIONS.md line out of order.

## Staged state

`git diff --cached --numstat` after `bash <scratchpad>/cmp_gate2.sh
<scratchpad> stage` (explicit paths). The rows for this report and the
artifact were not final at that point:

```
4	2	.gitignore
61	21	CLAUDE.md
16	0	DECISIONS.md
344	0	prompt_outputs/001-bootstrap-gate.md
367	0	prompt_outputs/001-bootstrap-gate2.md
375	0	prompt_outputs/001-bootstrap-implement.md
1280	0	prompt_outputs/001-bootstrap.diff.txt
```

The same run showed `git status --porcelain`: `M` for CLAUDE.md and
.gitignore, `A` for the other five paths, and no unstaged changes. The
artifact and this report were then regenerated and re-staged; their final
rows are in chat.
