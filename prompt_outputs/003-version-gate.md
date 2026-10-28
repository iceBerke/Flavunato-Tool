# 003 — version — gate (final)

Task: apply rulings P3 and P4 to the CLAUDE.md version line, rerun the
tests, stage the 7 paths by explicit path and propose the commit
message. This is the final gate of task 003. Stops before committing:
nothing committed, nothing pushed.

Tests: py_compile on all tracked .py files, the import check, and the
two data-dependent scripts, tests/golden/check_golden.py and
tests/validation/compare_manual.py. All PASS (I1, T1–T3). The GUI window
title is manual-test-only: Berke launches the GUI before the push and
confirms that the title reads "Flavunato v1.1.0". It was not launched
here.

## Rulings recorded

- **P1:** no other "1.0.0" mention changes; they refer to the thesis
  version.
- **P2:** confirmed: the code has changed since v1.0-thesis (implement
  C5, C8).
- **P3 + P4:** the CLAUDE.md line is reworded and wrapped. Applied
  (change 1).
- **P5:** the commit message no longer claims that the golden test
  proves thesis reproduction; it says that the golden regression test
  still passes (proposed message below).
- **UNREQUESTED from the implement step:** the stale citation in
  docs/notes/known_issues.md:81 (gui.py:1,3,79 vs :77): DROPPED for
  now; it goes to a later docs task. Not changed.
- **Deviations from the implement step** (`<scratchpad>/__pycache__/`,
  MPLCONFIGDIR under `out/`): ACCEPTED.

## Errata

None. No new audit was made of the earlier reports.

## Files touched

| Path | Change |
|---|---|
| `CLAUDE.md` | the implement-step line replaced by two lines (change 1) |
| `prompt_outputs/003-version-gate.md` | new; this report |
| `prompt_outputs/003-version.diff.txt` | regenerated |
| git index | the 7 paths staged by explicit path; the intent-to-add entries become real entries |
| `flavunato/__init__.py` | unchanged by this prompt (G3); staged with its implement-step change |
| frozen and carried reports | unchanged (G2, D0); staged unchanged |
| `<scratchpad>/t003g_*.py`, `out/`, `regen/`, `pycache/`, `out/mplconfig/` | outside the repo: start, apply, tests, msg, stage and re-read scripts; saved output and local test logs; the cmp regeneration; bytecode; the matplotlib cache |

Approval: the prompt fixed the file list, which rule 9 counts as
approval. The import check reuses `<scratchpad>/t003_import.py` from
the implement step, unchanged.

## Premise checks (prompt vs files)

| Prompt premise | Finding |
|---|---|
| HEAD == origin/main == 640158e… | Holds (G1). |
| Three frozen/carried reports at the given bytes/sha256 (LF form) | Hold, before (G2) and at staging (D0). |
| flavunato/__init__.py already reads `__version__ = "1.1.0"` | Holds (G3). |
| CLAUDE.md line 5 is the implement-step line; line 4 is the 1.0.0 line | Hold (G3). |
| New lines are 72 and 64 chars; CLAUDE.md numstat vs HEAD `2 0` | Hold (A1). |
| P2 cites implement C5 and C8 | Both sections exist in 003-version-implement.md. |
| Tests: 11 files 0 failures; import check, check_golden and compare_manual PASS | Hold (I1, T1–T3). |
| Order as in 002-licence-gate.md | Followed: report, then artifact and cmp, then stage by explicit path; the numstat and status blocks below were refreshed and the cycle repeated until the report stopped changing, so the last stage holds the final report and artifact. |
| New CLAUDE.md wording "the golden test compares its results with v1.0-thesis" | **Still depends on P5.** The ruled P5 change covers the commit message only. The golden test compares results with the local `reference.json`; that it holds v1.0-thesis results rests on tests/README.md:23 ("Generate `reference.json` from the v1.0-thesis code BEFORE any refactoring"), and how the local file was generated cannot be checked from the repo: UNVERIFIED. Nothing changed. |
| New CLAUDE.md wording "the restructured package" | Supported by commit f66c01a "Restructure modules into flavunato package" in implement C5. |

## Change

**1. CLAUDE.md version line (P3, P4).** The implement-step line 5 is
replaced in place by two lines, with the file's CRLF working-tree
endings kept (A1). Line 4 is unchanged (A1). The diff vs HEAD shows two
added lines after line 4 and no deleted line in CLAUDE.md (A1, and the
re-read below):

> +Code version 1.1.0 is the restructured package with licence and citation
> +metadata; the golden test compares its results with v1.0-thesis.

The implement-step line was never committed, so it does not appear as
a deletion against HEAD.

## Tests

From I1 and T1–T3 below:

| Test | Exit | Verdict |
|---|---|---|
| py_compile, 11 tracked .py files | — | PASS, 0 failures |
| import check (`python -B`, MPLCONFIGDIR under `<scratchpad>/out/`) | 0 | PASS: `__version__` '1.1.0', gui imports, no Tk root, main() not called |
| tests/golden/check_golden.py | 0 | PASS |
| tests/validation/compare_manual.py | 0 | PASS (Validation A; Validation B is report-only) |
| GUI window title | — | manual-test-only; Berke, before the push |

No data was missing, so neither data test was skipped. Only verdict
lines are quoted (rule 20); the full output stays in local logs under
`<scratchpad>/out/`. `git status --porcelain -uall` is identical before
and after the tests, and so is the listing with `--ignored` (T3).
generate_golden.py was not run.

## Proposed commit message

Measured by `t003g_msg.py` below. Trailer excluded; the COMMIT step
appends it (rule 8).

```
Bump version to 1.1.0 for the first release

Set __version__ to 1.1.0 so that the GUI title matches the release
tag. The code has changed since v1.0-thesis (version 1.0.0); the
golden regression test still passes. Record the new version in
CLAUDE.md.

Include the task 002 commit and push reports.
```

All lines are within limits (M1). Claims checked against the diff and
the checks:

- "Set __version__ to 1.1.0": in the diff (flavunato/__init__.py).
- "so that the GUI title matches the release tag": the title reads
  `__version__` (flavunato/gui.py:20, :77; implement C4), and I1 shows
  the title string would be 'Flavunato v1.1.0'. No v1.1* tag exists
  yet (D7), so "matches the release tag" is intent, not a change. The
  window itself is manual-test-only.
- "The code has changed since v1.0-thesis (version 1.0.0)": implement
  C5 and C8; CLAUDE.md:4 maps 1.0.0 to v1.0-thesis.
- "the golden regression test still passes": T2.
- "Record the new version in CLAUDE.md": in the diff (change 1).
- "Include the task 002 commit and push reports": both are staged
  (cached numstat below).
- The message does not mention the task 003 reports and the artifact
  that the commit also adds. It omits them; it does not misstate them.

## UNREQUESTED — ACCEPT OR DROP

None new.

## Verification output

All blocks are script output inserted by `t002_insert.py`.

### G1–G4. Start state: `python t003g_start.py`

```
=== G1. fetch, branch, HEAD, origin ===
git fetch exit 0: exit 0 -> PASS
branch is main: main -> PASS
HEAD == 640158e...: 640158e0933ae7bfab8954cd332afb4e7870759b -> PASS
origin/main == 640158e...: 640158e0933ae7bfab8954cd332afb4e7870759b -> PASS
behind/ahead: behind 0, ahead 0 -> PASS

=== G2. Frozen and carried reports (LF form) ===
prompt_outputs/002-licence-commit.md: working-tree bytes 9580 | CR bytes 0
  LF form: bytes 9580 (want 9580) sha256 b06ad2cf4de2f5b3511238a3a72769bf1cc84d16baac0802259a901bc7e6f974 -> PASS
prompt_outputs/002-licence-push.md: working-tree bytes 5970 | CR bytes 0
  LF form: bytes 5970 (want 5970) sha256 75619dd11d482e025e3450dd6584cbd6379d85bf0939e15e20d440a65564e99e -> PASS
prompt_outputs/003-version-implement.md: working-tree bytes 18284 | CR bytes 0
  LF form: bytes 18284 (want 18284) sha256 f029819a196f1562d6cf40c790f36af21452fd17f3b97e60c3f04f1ff2eb5b6c -> PASS

=== G3. flavunato/__init__.py and CLAUDE.md before the change ===
__init__.py __version__ line: ['__version__ = "1.1.0"'] -> PASS
numstat vs HEAD (before):
  1	0	CLAUDE.md
  1	1	flavunato/__init__.py
CLAUDE.md bytes 8517 | lines 140 | CRLF 140 | bare LF 0
CLAUDE.md:4 is the 1.0.0 line: Code version 1.0.0 corresponds to the git tag v1.0-thesis. -> PASS
CLAUDE.md:5 is the implement-step line: 113 chars -> PASS
implement-step line occurs once: 1 -> PASS

=== G4. Status and index ===
   M CLAUDE.md
   M flavunato/__init__.py
   A prompt_outputs/002-licence-commit.md
   A prompt_outputs/002-licence-push.md
   A prompt_outputs/003-version-implement.md
   A prompt_outputs/003-version.diff.txt
nothing staged: [] -> PASS

RESULT: ALL PASS
```

### A1. Change 1: `python t003g_apply.py`

```
numstat before: 1	0	CLAUDE.md
CLAUDE.md: bytes 8517 -> 8542 | CRLF 140 -> 141 | bare LF 0
CLAUDE.md:4 (58 chars): Code version 1.0.0 corresponds to the git tag v1.0-thesis.
CLAUDE.md:5 (72 chars): Code version 1.1.0 is the restructured package with licence and citation
CLAUDE.md:6 (64 chars): metadata; the golden test compares its results with v1.0-thesis.
CLAUDE.md:7 (0 chars): 
line 4 unchanged: PASS
new line lengths: 72, 64 (expected 72, 64) -> PASS
numstat after: 2	0	CLAUDE.md (expected 2 0) -> PASS
git diff -U0 HEAD -- CLAUDE.md:
  @@ -4,0 +5,2 @@ Code version 1.0.0 corresponds to the git tag v1.0-thesis.
  +Code version 1.1.0 is the restructured package with licence and citation
  +metadata; the golden test compares its results with v1.0-thesis.
RESULT: ALL PASS
```

### I1. Import check: `MPLCONFIGDIR=<scratchpad>/out/mplconfig python -B t003_import.py`

```
MPLCONFIGDIR under <scratchpad>/out/: True
flavunato.__version__ = '1.1.0' -> PASS
import flavunato.gui: OK
gui.__version__ = '1.1.0'
PLOTTING_AVAILABLE = True
ELEMENT_SPECTRUM_AVAILABLE = True
UNCERTAINTY_AVAILABLE = True
Tk default root created: False
main() called: no (callable present: True)
title would read: 'Flavunato v1.1.0' (string only, no window)
RESULT: ALL PASS
```

### T1–T3. Tests: `python t003g_tests.py <scratchpad>`

```
=== T1. py_compile on all tracked .py files (rule 4) ===
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
py_compile: 11 files, 0 failures; bytecode under <scratchpad>/pycache -> PASS

=== T2. Data-dependent tests ===
-- tests/golden/check_golden.py: exit 0 | stdout 1 lines | stderr 0 lines | verdict PASS
  | PASS  golden regression: 20 rows, tol 1e-12, roi_source=reference
  tests/golden/check_golden.py not FAIL: PASS -> PASS
-- tests/validation/compare_manual.py: exit 0 | stdout 45 lines | stderr 0 lines | verdict PASS
  | VALIDATION A: PASS -- all rows within 1e-09
  tests/validation/compare_manual.py not FAIL: PASS -> PASS

=== T3. Working tree unchanged by the tests ===
git status --porcelain -uall: 6 lines before, 6 after
  identical before vs after: same -> PASS
same with --ignored (names not printed): 64 lines before, 64 after
  identical before vs after: same -> PASS

RESULT: ALL PASS
```

### M1. Commit message: `python t003g_msg.py`

```
  L1   43 chars (max 50) PASS | Bump version to 1.1.0 for the first release
  L2    0 chars (max 72) PASS | 
  L3   66 chars (max 72) PASS | Set __version__ to 1.1.0 so that the GUI title matches the release
  L4   64 chars (max 72) PASS | tag. The code has changed since v1.0-thesis (version 1.0.0); the
  L5   62 chars (max 72) PASS | golden regression test still passes. Record the new version in
  L6   10 chars (max 72) PASS | CLAUDE.md.
  L7    0 chars (max 72) PASS | 
  L8   45 chars (max 72) PASS | Include the task 002 commit and push reports.
subject 43 chars | no trailing period: PASS
line 2 blank: PASS
longest body line: 66 chars
trailer lines in message: 0
non-ASCII chars: 0 | lines 8
RESULT: ALL PASS
```

## Diff artifact and staging

`python t003g_stage.py <scratchpad>` re-checks the frozen and carried
reports (D0), runs `git add -N` on every untracked path from
`git status` (explicit paths), writes the artifact with the prompt's
command, regenerates it to `<scratchpad>/regen/003-version.diff.txt`
and runs cmp. It then stages the 7 paths with `git add -- <path>`, one
at a time, and checks each staged blob against its working file (LF
form), and that no unstaged change, untracked file or intent-to-add
entry is left. The final run, made after this report was complete, is
in chat; it also checks that the three blocks below match the live
state verbatim.

### R1–R2. Re-read of the artifact (rule 15), `python t003g_reread.py`

```
=== R1. prompt_outputs/003-version.diff.txt: 1158 lines, CR bytes 0 ===
  file: CLAUDE.md
    5: @@ -2,6 +2,8 @@
    9: +Code version 1.1.0 is the restructured package with licence and citation
    10: +metadata; the golden test compares its results with v1.0-thesis.
  file: flavunato/__init__.py
    18: @@ -1 +1 @@
    19: -__version__ = "1.0.0"
    20: +__version__ = "1.1.0"
  file: prompt_outputs/002-licence-commit.md
  file: prompt_outputs/002-licence-push.md
  file: prompt_outputs/003-version-gate.md
  file: prompt_outputs/003-version-implement.md
deleted lines in the artifact: 1
  line 19 (flavunato/__init__.py): -__version__ = "1.0.0"
only deletion is the __init__.py version line: PASS

=== R2. flavunato/gui.py lines that use __version__ ===
  flavunato/gui.py:20: from . import __version__
  flavunato/gui.py:77: self.root.title(f"Flavunato v{__version__}")

RESULT: ALL PASS
```

The deletions column of both numstat blocks is 0 on every row except
flavunato/__init__.py. Its one deleted line is the
`-__version__ = "1.0.0"` line from the implement step, which the
re-read above lists as the only deleted line in the artifact.

### Artifact numstat

```
2	0	CLAUDE.md
1	1	flavunato/__init__.py
214	0	prompt_outputs/002-licence-commit.md
149	0	prompt_outputs/002-licence-push.md
349	0	prompt_outputs/003-version-gate.md
402	0	prompt_outputs/003-version-implement.md
```

### git diff --cached --numstat

```
2	0	CLAUDE.md
1	1	flavunato/__init__.py
214	0	prompt_outputs/002-licence-commit.md
149	0	prompt_outputs/002-licence-push.md
349	0	prompt_outputs/003-version-gate.md
402	0	prompt_outputs/003-version-implement.md
1158	0	prompt_outputs/003-version.diff.txt
```

## Final state

### git status --porcelain -uall

```
M  CLAUDE.md
M  flavunato/__init__.py
A  prompt_outputs/002-licence-commit.md
A  prompt_outputs/002-licence-push.md
A  prompt_outputs/003-version-gate.md
A  prompt_outputs/003-version-implement.md
A  prompt_outputs/003-version.diff.txt
```
