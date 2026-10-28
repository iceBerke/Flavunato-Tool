# 003 — version — implement

Task: bump the code version to 1.1.0 in flavunato/__init__.py and record
it in CLAUDE.md. Stops at the review gate: nothing staged, nothing
committed, nothing pushed. The intent-to-add entries made for the diff
are the only index change.

Tests: py_compile on all tracked .py files, and
tests/golden/check_golden.py and tests/validation/compare_manual.py,
all PASS (T1, T2). **Manual test only:** the GUI window title. Berke
launches the GUI before the push and confirms that it reads
"Flavunato v1.1.0". I did not launch it; the import check (I1) only
builds the title string, without a window.

## Errata

None for the task 002 reports.

## Files touched

| Path | Change |
|---|---|
| `flavunato/__init__.py` | the `__version__` line only; LF ending kept (A1, C7) |
| `CLAUDE.md` | one line inserted after line 4; line 4 unchanged; CRLF working-tree ending kept (A1, C7) |
| `prompt_outputs/003-version-implement.md` | new; this report |
| `prompt_outputs/003-version.diff.txt` | new; the diff artifact |
| git index | intent-to-add for every untracked path in `git status`, by explicit path |
| `<scratchpad>/t003_*.py`, `t002g_tests.py`, `t002_insert.py`, `out/`, `regen/`, `pycache/` | outside the repo: check, apply, import, message, diff, test and insert scripts; saved output, local test logs and the matplotlib cache; the cmp regeneration; bytecode |
| `<scratchpad>/__pycache__/` | outside the repo, **not in the prompt's list**: see Deviations |

Approval: the prompt fixed the file list, which rule 9 counts as
approval.

## Premise checks (prompt vs files)

| Prompt premise | Finding |
|---|---|
| HEAD == origin/main == 640158e…, after fetch | Holds (C1). |
| Carried reports at the given bytes/sha256 | Hold before and after the change (C1). |
| `__version__ = "1.0.0"` in flavunato/__init__.py | Holds, once (A1). |
| CLAUDE.md line 4 is "Code version 1.0.0 corresponds to the git tag v1.0-thesis." | Holds (C2); unchanged afterwards (C7). |
| "the GUI window title is built from it" | Holds: flavunato/gui.py:20 imports `__version__`, flavunato/gui.py:77 sets `self.root.title(f"Flavunato v{__version__}")` (C4). |
| "main has changed since" v1.0-thesis | Holds: 6 commits touch flavunato/ or run_flavunato.py after the tag (C5). Point P2. |
| DECISIONS.md restates something about versions | It does not: 0 hits (C6). |
| py_compile 11 files, 0 failures; both tests PASS | Hold (T1, T2). |

## Changes

From C7 (`git diff -U0 HEAD`):

```
@@ -4,0 +5 @@ Code version 1.0.0 corresponds to the git tag v1.0-thesis.
+Code version 1.1.0 adds licence and citation metadata; the golden test checks that its results match v1.0-thesis.
@@ -1 +1 @@
-__version__ = "1.0.0"
+__version__ = "1.1.0"
```

**Deleted line:** `__version__ = "1.0.0"` in flavunato/__init__.py,
replaced by the 1.1.0 line. It is the only deleted line.

**Import check (I1):** `flavunato.__version__` is `'1.1.0'`.
`flavunato.gui` imports, all three `*_AVAILABLE` flags are True, no Tk
root exists, and `main()` was not called.

## POINTS TO SURFACE FOR YOUR RULING

**P1. Other places that state a version (C3).** None needs changing, in
my reading:
- docs/software_overview.md:78 and docs/latex/software_overview.tex:83
  say the current code "reproduces every recorded result of version
  1.0.0 (git tag `v1.0-thesis`)". That is about the thesis version and
  stays true.
- docs/notes/known_issues.md:81 records the title as
  `Flavunato v{__version__}`, which still holds.
- README.md and CITATION.cff state no version number (C3: no hit).
  CITATION.cff has no `version` field by the task-002 design.
- The prompt_outputs/001-* hits are historical and frozen.

**P2. Has the code changed since v1.0-thesis?** Yes. `git log
v1.0-thesis..HEAD -- flavunato/ run_flavunato.py` lists 6 commits (C5).
By subject, they cover the package restructure, the removal of the
command-line entry points and dead code, an import-flag fix, messages
and title text, and CLI console output. With rename detection, the
`.py` diff since the tag is non-trivial (C8). No subject says it
changes a calculation. The golden test passes (T2).

**P3. Wording of the new CLAUDE.md line.** "adds licence and citation
metadata" names only task 002. Against 1.0.0, version 1.1.0 also
contains the restructure and removals listed in P2. Keep, or reword.

**P4. Length of the new CLAUDE.md line.** It is 113 chars (A1) and was
inserted as given. The rule text in CLAUDE.md is wrapped (rules 8, 9
and 12 measured at most 75 chars in 001-bootstrap-gate4.md, section
D). Keep on one line, or wrap?

**P5. "the golden test checks that its results match v1.0-thesis".**
check_golden.py compares against the local-only
tests/golden/reference.json (tests/golden/check_golden.py:38-44).
tests/README.md:23 says to generate that file from the v1.0-thesis
code. Whether the local file was in fact generated that way cannot be
checked from the repository: UNVERIFIED. The same applies to the
commit message (below). The test covers one sample (T2: 20 rows), not
every possible input.

## Proposed commit message

Measured by `t003_msg.py` (M1). Trailer excluded; the COMMIT step
appends it (rule 8).

```
Bump version to 1.1.0 for the first release

Set __version__ to 1.1.0 so that the GUI title matches the release
tag. The code has changed since v1.0-thesis (version 1.0.0); the
golden test confirms that it reproduces the thesis results. Record
the new version in CLAUDE.md.

Include the task 002 commit and push reports.
```

All lines are within limits. Claims checked against the diff and the
checks:

- "so that the GUI title matches the release tag": the title string
  becomes `Flavunato v1.1.0` (I1). The tag v1.1.0 does not exist yet;
  it is the planned release tag. True as intent.
- "The code has changed since v1.0-thesis (version 1.0.0)": supported
  (C5, C8; P2). CLAUDE.md:4 ties 1.0.0 to v1.0-thesis.
- "the golden test confirms that it reproduces the thesis results":
  the test passes (T2), but the reference file's provenance is
  UNVERIFIED (P5).
- "Record the new version in CLAUDE.md" and "Include the task 002
  commit and push reports": both visible in the artifact (numstat
  below).
- Not mentioned: the task 003 report and the artifact. They are
  omitted, not misstated.

## Deviations

- The import check imports matplotlib (via flavunato/plotting.py:11).
  To keep its font cache inside the approved folder I ran it with
  `MPLCONFIGDIR=<scratchpad>/out/mplconfig`. matplotlib built a fresh
  cache there (I1, first line). No other environment change.
- While deriving `t003_diff.py` I ran `python -m py_compile` on it,
  which wrote `<scratchpad>/__pycache__/`, a folder not in the
  prompt's list. It is outside the repository and holds only that
  script's bytecode. I left it in place.

## UNREQUESTED — ACCEPT OR DROP

- docs/notes/known_issues.md:81 cites `flavunato/gui.py:1,3,79` for the
  title, but the title is now set at flavunato/gui.py:77 (C4). This is
  a stale citation (rule 18). Not fixed.

## Verification output

All blocks are script output inserted by `t002_insert.py`.

### C1–C6. Before the change: `python t003_check.py before`

```
=== C1. Start state ===
git fetch: exit 0 -> PASS
branch is main: main -> PASS
HEAD == 640158e...: 640158e0933ae7bfab8954cd332afb4e7870759b -> PASS
origin/main == 640158e...: 640158e0933ae7bfab8954cd332afb4e7870759b -> PASS
behind/ahead: behind 0, ahead 0 -> PASS
  ?? prompt_outputs/002-licence-commit.md
  ?? prompt_outputs/002-licence-push.md
only the 2 carried reports untracked: 2 line(s) -> PASS
prompt_outputs/002-licence-commit.md LF form: bytes 9580 (want 9580) sha256 b06ad2cf4de2f5b3511238a3a72769bf1cc84d16baac0802259a901bc7e6f974 (working-tree bytes 9580, CR 0) -> PASS
prompt_outputs/002-licence-push.md LF form: bytes 5970 (want 5970) sha256 75619dd11d482e025e3450dd6584cbd6379d85bf0939e15e20d440a65564e99e (working-tree bytes 5970, CR 0) -> PASS

=== C2. Files to change ===
flavunato/__init__.py: 22 bytes | lines 1 | CRLF 0 | bare LF 1
CLAUDE.md: 8402 bytes | lines 139 | CRLF 139 | bare LF 0
CLAUDE.md:3: Thesis version is tagged v1.0-thesis. It is the reference; never alter its behaviour.
CLAUDE.md:4: Code version 1.0.0 corresponds to the git tag v1.0-thesis.
CLAUDE.md:5: ''

=== C3. git grep over tracked files (before) ===
-- git grep -n -F '1.0.0': exit 0, 6 hit(s)
  CLAUDE.md:4:Code version 1.0.0 corresponds to the git tag v1.0-thesis.
  docs/latex/software_overview.tex:83:reproduces every recorded result of version 1.0.0 (git tag
  docs/software_overview.md:78:recorded result of version 1.0.0 (git tag `v1.0-thesis`), including the
  flavunato/__init__.py:1:__version__ = "1.0.0"
  prompt_outputs/001-bootstrap-gate3.md:144:- Header (:1–4): tag v1.0-thesis exists (D). "Code version 1.0.0" is a
  prompt_outputs/001-bootstrap.diff.txt:1073:+- Header (:1–4): tag v1.0-thesis exists (D). "Code version 1.0.0" is a
-- git grep -n -F '__version__': exit 0, 4 hit(s)
  docs/notes/known_issues.md:81:| Header and window title said "Version 15" / "v15" | `flavunato/gui.py:1,3,79` | fixed (R2a) — title now `Flavunato v{__version__ ...
  flavunato/__init__.py:1:__version__ = "1.0.0"
  flavunato/gui.py:20:from . import __version__
  flavunato/gui.py:77:        self.root.title(f"Flavunato v{__version__}")

=== C4. GUI use of __version__ (read only) ===
  flavunato/gui.py:20:from . import __version__
  flavunato/gui.py:77:        self.root.title(f"Flavunato v{__version__}")

=== C5. git log --oneline v1.0-thesis..HEAD -- flavunato/ run_flavunato.py ===
v1.0-thesis -> 55ed245
commit count: 6
  c0f5d0d Remove the command-line entry points
  ccf4aca Remove unused imports and dead code
  fee53f4 Stop uncertainty import failure resetting flag
  3baab9d Update stale module names in messages and title
  2a038c8 Make CLI output robust on non-UTF-8 consoles
  f66c01a Restructure modules into flavunato package
git diff --stat v1.0-thesis HEAD -- flavunato/ run_flavunato.py:
   flavunato/__init__.py        |    1 +
   flavunato/__main__.py        |    4 +
   flavunato/element_spectra.py |  595 ++++++++++++
   flavunato/gui.py             | 2097 ++++++++++++++++++++++++++++++++++++++++++
   flavunato/plotting.py        |  622 +++++++++++++
   flavunato/uncertainty.py     |  715 ++++++++++++++
   run_flavunato.py             |    4 +
   7 files changed, 4038 insertions(+)
tracked .py at v1.0-thesis: ['xnra_element_spectra_v1.py', 'xnra_gui_v18.py', 'xnra_main_v6.py', 'xnra_uncertainty_v12.py']

=== C6. DECISIONS.md on versions ===
git grep -i version|1.0.0|1.1.0|v1.0 DECISIONS.md: exit 1, 0 hit(s) []

RESULT: ALL PASS
```

### A1. Apply: `python t003_apply.py`

```
flavunato/__init__.py: 22 -> 22 bytes | b'__version__ = "1.0.0"\n' -> b'__version__ = "1.1.0"\n'
CLAUDE.md: 8402 -> 8517 bytes | CRLF 139 -> 140 | bare LF 0
inserted line 5: 113 chars | Code version 1.1.0 adds licence and citation metadata; the golden test checks that its results match v1.0-thesis.
```

### C1, C3, C7, C8. After the change: `python t003_check.py after`

```
=== C1. Carried reports still unchanged ===
prompt_outputs/002-licence-commit.md LF form: bytes 9580 (want 9580) sha256 b06ad2cf4de2f5b3511238a3a72769bf1cc84d16baac0802259a901bc7e6f974 (working-tree bytes 9580, CR 0) -> PASS
prompt_outputs/002-licence-push.md LF form: bytes 5970 (want 5970) sha256 75619dd11d482e025e3450dd6584cbd6379d85bf0939e15e20d440a65564e99e (working-tree bytes 5970, CR 0) -> PASS

=== C3. git grep over tracked files (after) ===
-- git grep -n -F '1.0.0': exit 0, 5 hit(s)
  CLAUDE.md:4:Code version 1.0.0 corresponds to the git tag v1.0-thesis.
  docs/latex/software_overview.tex:83:reproduces every recorded result of version 1.0.0 (git tag
  docs/software_overview.md:78:recorded result of version 1.0.0 (git tag `v1.0-thesis`), including the
  prompt_outputs/001-bootstrap-gate3.md:144:- Header (:1–4): tag v1.0-thesis exists (D). "Code version 1.0.0" is a
  prompt_outputs/001-bootstrap.diff.txt:1073:+- Header (:1–4): tag v1.0-thesis exists (D). "Code version 1.0.0" is a
-- git grep -n -F '__version__': exit 0, 4 hit(s)
  docs/notes/known_issues.md:81:| Header and window title said "Version 15" / "v15" | `flavunato/gui.py:1,3,79` | fixed (R2a) — title now `Flavunato v{__version__ ...
  flavunato/__init__.py:1:__version__ = "1.1.0"
  flavunato/gui.py:20:from . import __version__
  flavunato/gui.py:77:        self.root.title(f"Flavunato v{__version__}")

=== C7. The change vs HEAD ===
numstat (tracked):
  1	0	CLAUDE.md
  1	1	flavunato/__init__.py
tracked files changed == CLAUDE.md, flavunato/__init__.py: ['CLAUDE.md', 'flavunato/__init__.py'] -> PASS
  @@ -4,0 +5 @@ Code version 1.0.0 corresponds to the git tag v1.0-thesis.
  +Code version 1.1.0 adds licence and citation metadata; the golden test checks that its results match v1.0-thesis.
  @@ -1 +1 @@
  -__version__ = "1.0.0"
  +__version__ = "1.1.0"
CLAUDE.md:4: 'Code version 1.0.0 corresponds to the git tag v1.0-thesis.'
CLAUDE.md:5: 'Code version 1.1.0 adds licence and citation metadata; the golden test checks that its results match v1.0-thesis.'
CLAUDE.md:6: ''
CLAUDE.md:4 unchanged: Code version 1.0.0 corresponds to the git tag v1.0-thesis. -> PASS

=== C8. Extra: commits since the tag touching any .py path ===
git log --oneline v1.0-thesis..HEAD -- '*.py': 9 commit(s)
  7efef9a Rename the reference in compare_manual header
  c0f5d0d Remove the command-line entry points
  ccf4aca Remove unused imports and dead code
  fee53f4 Stop uncertainty import failure resetting flag
  3baab9d Update stale module names in messages and title
  2a038c8 Make CLI output robust on non-UTF-8 consoles
  f66c01a Restructure modules into flavunato package
  7905b6c Adopt full-support ROIs as reference
  47054c4 Add golden and manual validation tests
git diff --stat -M v1.0-thesis HEAD -- '*.py':
   flavunato/__init__.py                              |   1 +
   flavunato/__main__.py                              |   4 +
   .../element_spectra.py                             |  59 +--
   xnra_gui_v18.py => flavunato/gui.py                |  29 +-
   xnra_main_v6.py => flavunato/plotting.py           |   0
   .../uncertainty.py                                 | 497 +--------------------
   run_flavunato.py                                   |   4 +
   tests/_paths.py                                    |  62 +++
   tests/golden/check_golden.py                       |  93 ++++
   tests/golden/generate_golden.py                    | 159 +++++++
   tests/validation/compare_manual.py                 | 172 +++++++
   11 files changed, 514 insertions(+), 566 deletions(-)

RESULT: ALL PASS
```

### I1. Import check: `MPLCONFIGDIR=<scratchpad>/out/mplconfig python -B t003_import.py`

```
Matplotlib is building the font cache; this may take a moment.
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
import exit 0
```

### T1–T3. Tests: `python t002g_tests.py <scratchpad>`

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
git status --porcelain -uall: 4 lines before, 4 after
  identical before vs after: same -> PASS
same with --ignored (names not printed): 62 lines before, 62 after
  identical before vs after: same -> PASS

RESULT: ALL PASS
```

### M1. Commit message: `python t003_msg.py`

```
  L1   43 chars (max 50) PASS | Bump version to 1.1.0 for the first release
  L2    0 chars (max 72) PASS | 
  L3   66 chars (max 72) PASS | Set __version__ to 1.1.0 so that the GUI title matches the release
  L4   64 chars (max 72) PASS | tag. The code has changed since v1.0-thesis (version 1.0.0); the
  L5   66 chars (max 72) PASS | golden test confirms that it reproduces the thesis results. Record
  L6   29 chars (max 72) PASS | the new version in CLAUDE.md.
  L7    0 chars (max 72) PASS | 
  L8   45 chars (max 72) PASS | Include the task 002 commit and push reports.
subject 43 chars | no trailing period: PASS
line 2 blank: PASS
longest body line: 66 chars
trailer lines in message: 0
non-ASCII chars: 0 | lines 8
RESULT: ALL PASS
```

## Diff artifact

`python t003_diff.py <scratchpad>` runs `git add -N` on every untracked
path from `git status` (explicit paths), writes the artifact with the
prompt's command, regenerates it to
`<scratchpad>/regen/003-version.diff.txt` and runs cmp. The final run,
made after this report was complete, is in chat. It also checks that
the two blocks below match the live state verbatim.

The deletions column of the numstat block is 0 on every row except
flavunato/__init__.py, whose one deleted line is accounted for under
Changes.

### Numstat

```
1	0	CLAUDE.md
1	1	flavunato/__init__.py
214	0	prompt_outputs/002-licence-commit.md
149	0	prompt_outputs/002-licence-push.md
402	0	prompt_outputs/003-version-implement.md
```

## Final state

### git status --porcelain -uall

```
 M CLAUDE.md
 M flavunato/__init__.py
 A prompt_outputs/002-licence-commit.md
 A prompt_outputs/002-licence-push.md
 A prompt_outputs/003-version-implement.md
 A prompt_outputs/003-version.diff.txt
```
