# 002 — licence — gate (final)

Task: apply ruling R8 to the README copyright line, run the tests, stage
the 8 paths by explicit path and propose the commit message. This is the
final gate of task 002. Stops before committing: nothing committed,
nothing pushed.

Tests: py_compile on all tracked .py files, and the two data-dependent
scripts, tests/golden/check_golden.py and
tests/validation/compare_manual.py. Both PASS (T2). There is no other
automated test suite.

## Rulings recorded

- **R1:** LICENSE bytes stay exactly as downloaded.
- **R2:** no LICENSE.fr.
- **R3:** no per-file licence headers.
- **R4:** no rewrapping of the added README text.
- **R5:** keep the Acknowledgements section.
- **R6:** existing mentions of the internal technical note in README
  and docs stay unchanged.
- **R7:** keep the word "derived" in the acknowledgement. See premise
  checks: the README word is "deriving".
- **R8:** the copyright line names "The Flavunato authors (see
  CITATION.cff)", not individuals or institutions. Applied (change 1).
- **Review defect, accepted as-is:** see Errata.
- **UNREQUESTED from the implement step:** deleting the root
  `__pycache__/`: DROPPED. Extra scratch folders `out/`, `regen/`,
  `pycache/`: ACCEPTED.

## Errata

- **002-licence-implement.md, V5:** it quotes one line of the tracked
  file docs/references/README.md (the `HEAD:docs/references/README.md:6`
  hit). Ruled acceptable because the file is tracked and public.
  Recorded here only; the frozen report is not edited.

## Files touched

| Path | Change |
|---|---|
| `README.md` | one line replaced (change 1) |
| `prompt_outputs/002-licence-gate.md` | new; this report |
| `prompt_outputs/002-licence.diff.txt` | regenerated |
| git index | the 8 paths staged by explicit path; the intent-to-add entries become real entries |
| frozen/carried files | unchanged (G2); staged unchanged |
| `<scratchpad>/t002g_*.py`, `out/`, `regen/`, `pycache/` | outside the repo: start, readme, tests, msg and stage scripts; saved output and local test logs; the cmp regeneration; bytecode |

Approval: the prompt fixed the file list, which rule 9 counts as
approval.

## Premise checks (prompt vs files)

| Prompt premise | Finding |
|---|---|
| HEAD == origin/main == 32a4e6c… | Holds (G1). |
| Three frozen reports at the given bytes/sha256 | Hold (G2). |
| LICENSE 21396 bytes / 014e06…5f2f; CITATION.cff 950 bytes | Hold; both blob ids also match the `index 0000000..` lines of the implement-step artifact (G2). |
| The old copyright line exists | Holds, once (G3). |
| R7 "keep the word 'derived'" | **Differs in wording.** The README says "deriving" (G3). Nothing changed: I read the ruling as keeping the verb. |
| The two test scripts write nothing but stdout | Holds by reading, so both were run. `_paths.require()` only prints and exits (tests/_paths.py:35-45). check_golden.py imports `build` from generate_golden.py (tests/golden/check_golden.py:15); generate_golden.py writes only in `main()` (tests/golden/generate_golden.py:139-145), which check_golden.py never calls. compare_manual.py only reads the xlsx (tests/validation/compare_manual.py:53). The one `open(` in the imported library modules is a read (flavunato/element_spectra.py:140). generate_golden.py was not run. |
| Order as in 001-bootstrap-gate4.md | Followed: report, then artifact and cmp, then stage by explicit path. Then the numstat and status blocks below were refreshed and the cycle repeated until the report stopped changing, so the last stage holds the final report and artifact. |

## Change

**1. README.md copyright line (R8).** Replaced in place with the file's
CRLF working-tree ending kept. One line differs, line 53 (G3 and
"README change" below):

> -Copyright (c) 2026 Berke Santos, Giuseppe Legrottaglie
> +Copyright (c) 2026 The Flavunato authors (see CITATION.cff)

README.md vs HEAD is `12 0` before and after: the line was itself
added in this task, so the change does not alter the counts.

## Tests

From T1–T3 below:

| Test | Exit | Verdict |
|---|---|---|
| py_compile, 11 tracked .py files | — | PASS, 0 failures |
| tests/golden/check_golden.py | 0 | PASS |
| tests/validation/compare_manual.py | 0 | PASS (Validation A; Validation B is report-only) |

No data was missing, so neither test was skipped. Only verdict and
summary lines are quoted (rule 20). The full output stays in local logs
under `<scratchpad>/out/`. `git status --porcelain -uall` is identical
before and after the tests, and so is the same listing with
`--ignored` (T3). The status comparison catches new, removed and
re-flagged paths, not a rewrite of an already-ignored file; for that
the evidence is the code reading above.

## Proposed commit message

Measured by `t002g_msg.py` below. Trailer excluded; the COMMIT step
appends it (rule 8).

```
Add CeCILL-B license and citation metadata

Add the official CeCILL-B v1.0 English text as LICENSE, unmodified,
and a CITATION.cff validated with cffconvert, so that releases can be
archived on Zenodo and cited by version DOI.

Add Acknowledgements and License sections to the README. The
copyright line refers to the authors listed in CITATION.cff.

Include the task 001 commit and push reports.
```

All lines are within limits. Claims checked against the diff:

- "official", "unmodified" and "validated with cffconvert": the diff
  shows the LICENSE and CITATION.cff contents. The source and the
  validation are evidenced in 002-licence-implement.md (L1–L2, V3, V2),
  which this commit includes, not by the diff lines themselves.
- "so that releases can be archived on Zenodo and cited by version
  DOI": a purpose. Nothing in the diff configures Zenodo (no tag, no
  `.zenodo.json`). True as intent, not as a change.
- The message does not mention the task 002 reports and the artifact
  that the commit also adds. It omits them; it does not misstate them.

## UNREQUESTED — ACCEPT OR DROP

None.

## Verification output

All blocks are script output inserted by `t002_insert.py`.

### Start state: `python t002g_start.py`

```
=== G1. fetch, branch, HEAD, origin ===
git fetch exit 0: exit 0 -> PASS
branch is main: main -> PASS
HEAD == 32a4e6c...: 32a4e6ce9e79ec10e627ba0df8d84c5b9b2d2dc1 -> PASS
origin/main == 32a4e6c...: 32a4e6ce9e79ec10e627ba0df8d84c5b9b2d2dc1 -> PASS
behind/ahead: behind 0, ahead 0 -> PASS

=== G2. Frozen/carried files (LF form) ===
prompt_outputs/001-bootstrap-commit.md: working-tree bytes 9784 | CR bytes 0
  LF form: bytes 9784 (want 9784) sha256 b721740d228165f9f22e627c81a24a4036f0aac12efb25e4954663304653734d -> PASS
prompt_outputs/001-bootstrap-push.md: working-tree bytes 5739 | CR bytes 0
  LF form: bytes 5739 (want 5739) sha256 5440ae87298fe16da6e2e9550f0d6b1d40759a112c580249a6de00abfec18c09 -> PASS
prompt_outputs/002-licence-implement.md: working-tree bytes 27369 | CR bytes 0
  LF form: bytes 27369 (want 27369) sha256 e15f74f9e5eb335fc228d70bdc0bed66d3a379d39f2b8ba9997a6316a5e0c4c1 -> PASS
LICENSE: working-tree bytes 21396 | CR bytes 0
  LF form: bytes 21396 (want 21396) sha256 014e062e7d6b3b9e686bb8cb642479d6cc8bb775d8ee185908b669b8daaf5f2f -> PASS
CITATION.cff: bytes 950 | CR 0 | sha256 b405d47a815c54e0d908e61521dd4d761730257ad361739f42d2078f56a10a48
  CITATION.cff bytes == 950: 950 -> PASS
  CITATION.cff blob matches implement artifact 'index 0000000..d69b935': d69b935059bbdd5c373b377e6f6abb6a799b375d -> PASS
  LICENSE blob matches implement artifact 'index 0000000..da41897': da418978d4e89266df4fc6ea19c6424c879a9bd8 -> PASS

=== G3. README.md before the change ===
numstat README.md vs HEAD (before): 12	0	README.md
README.md bytes 2399 | CRLF 56 | bare LF 0
old copyright line occurs once: 1 -> PASS
'deriving' in the acknowledgement (ruling R7 says 'derived'): [b'deriving'] -> PASS

=== G4. Status and index ===
   A CITATION.cff
   A LICENSE
   M README.md
   A prompt_outputs/001-bootstrap-commit.md
   A prompt_outputs/001-bootstrap-push.md
   A prompt_outputs/002-licence-implement.md
   A prompt_outputs/002-licence.diff.txt
nothing staged: [] -> PASS

RESULT: ALL PASS
```

### README change: `python t002g_readme.py`

```
numstat before: 12	0	README.md
bytes 2399 -> 2404 | CRLF 56 -> 56 | bare LF 0
numstat after:  12	0	README.md
lines differing (working tree): [53] of 57 vs 57
  -53: Copyright (c) 2026 Berke Santos, Giuseppe Legrottaglie
  +53: Copyright (c) 2026 The Flavunato authors (see CITATION.cff)
git diff -U0 HEAD -- README.md:
  @@ -44,0 +45,12 @@ Mayer, M. (1999), AIP Conf. Proc. **475**, 541–544,
  +
  +## Acknowledgements
  +
  +We thank Babacar Diallo for deriving the uncertainty formulas
  +implemented in `flavunato/uncertainty.py`.
  +
  +## License
  +
  +Copyright (c) 2026 The Flavunato authors (see CITATION.cff)
  +
  +Flavunato is distributed under the CeCILL-B Free Software License
  +Agreement, version 1.0. See [LICENSE](LICENSE) for the full text.
```

### Tests: `python t002g_tests.py <scratchpad>`

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
git status --porcelain -uall: 7 lines before, 7 after
  identical before vs after: same -> PASS
same with --ignored (names not printed): 65 lines before, 65 after
  identical before vs after: same -> PASS

RESULT: ALL PASS
```

### Commit message: `python t002g_msg.py`

```
  L1   42 chars (max 50) PASS | Add CeCILL-B license and citation metadata
  L2    0 chars (max 72) PASS | 
  L3   67 chars (max 72) PASS | Add the official CeCILL-B v1.0 English text as LICENSE, unmodified,
  L4   69 chars (max 72) PASS | and a CITATION.cff validated with cffconvert, so that releases can be
  L5   44 chars (max 72) PASS | archived on Zenodo and cited by version DOI.
  L6    0 chars (max 72) PASS | 
  L7   60 chars (max 72) PASS | Add Acknowledgements and License sections to the README. The
  L8   60 chars (max 72) PASS | copyright line refers to the authors listed in CITATION.cff.
  L9    0 chars (max 72) PASS | 
  L10  45 chars (max 72) PASS | Include the task 001 commit and push reports.
subject 42 chars | no trailing period: PASS
line 2 blank: PASS
longest body line: 69 chars
trailer lines in message: 0
non-ASCII chars: 0 | lines 10
RESULT: ALL PASS
```

## Diff artifact and staging

`python t002g_stage.py <scratchpad>` runs `git add -N` on every
untracked path from `git status` (explicit paths), writes the artifact
with the prompt's command, regenerates it to
`<scratchpad>/regen/002-licence.diff.txt` and runs cmp. It then stages
the 8 paths with `git add -- <path>`, one at a time, and checks each
staged blob against its working file (LF form). The final run, made
after this report was complete, is in chat. It also checks that the
three blocks below match the live state verbatim.

The deletions column of both numstat blocks is 0 on every row: no line
is deleted.

### Artifact numstat

```
22	0	CITATION.cff
515	0	LICENSE
12	0	README.md
216	0	prompt_outputs/001-bootstrap-commit.md
142	0	prompt_outputs/001-bootstrap-push.md
307	0	prompt_outputs/002-licence-gate.md
552	0	prompt_outputs/002-licence-implement.md
```

### git diff --cached --numstat

```
22	0	CITATION.cff
515	0	LICENSE
12	0	README.md
216	0	prompt_outputs/001-bootstrap-commit.md
142	0	prompt_outputs/001-bootstrap-push.md
307	0	prompt_outputs/002-licence-gate.md
552	0	prompt_outputs/002-licence-implement.md
1810	0	prompt_outputs/002-licence.diff.txt
```

## Final state

### git status --porcelain -uall

```
A  CITATION.cff
A  LICENSE
M  README.md
A  prompt_outputs/001-bootstrap-commit.md
A  prompt_outputs/001-bootstrap-push.md
A  prompt_outputs/002-licence-gate.md
A  prompt_outputs/002-licence-implement.md
A  prompt_outputs/002-licence.diff.txt
```
