# Tests

Headless (no Tkinter). They reproduce the GUI's uncertainty path by calling
the same functions the GUI calls -- `xnra_gui_v18.py` does no maths of its own.

| Script | Purpose | Can fail? |
|---|---|---|
| `golden/generate_golden.py` | Writes `golden/reference.json` from current program output | no |
| `golden/check_golden.py` | Reruns and compares against `reference.json`, tolerance 1e-12 | **yes**, exit 1 on drift |
| `validation/compare_manual.py` | A: formula vs the supervisor's xlsx, tolerance 1e-9. B: program A_A vs xlsx counts | A **yes**; B report-only |

Run from the repo root:

```
python tests/golden/generate_golden.py
python tests/golden/check_golden.py
python tests/validation/compare_manual.py
```

## Generating the baseline

**Generate `reference.json` from the v1.0-thesis code BEFORE any refactoring:**

```
git checkout v1.0-thesis
python tests/golden/generate_golden.py
git checkout main
```

The golden file must capture thesis behaviour, not post-refactor behaviour.
Regenerating it from refactored code silently blesses whatever changed and
defeats the point of the test.

## Data policy

The three input files are real IBA data and are **never committed**; see
`examples/README.md`. `golden/reference.json` is derived from them and is
gitignored too. Every script exits 0 with a `SKIP:` message when data is
absent, so a clone without it still passes.

Before committing, confirm nothing from `examples/` except `README.md`, and no
`reference.json`, is staged:

```
git status --porcelain -uall
```

## ROIs

`golden/rois.json` is committed and holds the ROI ranges plus each element's
Q·Ω and σ. The GUI cannot express per-element Q·Ω or σ (single widgets at
`xnra_gui_v18.py:857,883`, read once at `:1525-1526`), so the scripts supply
each element's own pair; everything else matches the GUI.

The ROIs are currently **placeholders** (each element's full simulated
support), not the supervisor's. Every run prints a `roi_source=placeholder`
warning, and `check_golden.py` fails if that field changes. Replace the ranges
and set `roi_source` to `supervisor` once the real ROIs are known, then
regenerate the baseline.

See `docs/notes/known_issues.md` for open issues.
