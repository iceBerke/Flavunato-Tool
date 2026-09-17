# Tests

Headless (no Tkinter). They reproduce the GUI's uncertainty path by calling
the same functions the GUI calls -- `flavunato/gui.py` does no maths of its own.

| Script | Purpose | Can fail? |
|---|---|---|
| `golden/generate_golden.py` | Writes `golden/reference.json` from current program output | no |
| `golden/check_golden.py` | Reruns and compares against `reference.json`, tolerance 1e-12 | **yes**, exit 1 on drift |
| `validation/compare_manual.py` | A: formula vs the reference xlsx, tolerance 1e-9. B: measured (xlsx) vs simulated (program) counts — different methods, deltas expected | A **yes**; B report-only |
| `_paths.py` | shared helper: on-disk file names and the skip-if-missing guard | not run directly |

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
`examples/README.md`. `golden/reference.json` is generated locally by
`generate_golden.py` and is gitignored too, so neither the data nor anything
derived from it enters the repository. Every script exits 0 with a `SKIP:`
message when data is absent, so a clone without it still passes.

The golden and validation tests need the local example data (see
`examples/README.md`); without it they skip, so a fresh clone or CI cannot
detect regressions.

Before committing, confirm nothing from `examples/` except `README.md`, and no
`reference.json`, is staged:

```
git status --porcelain -uall
```

## ROIs

`golden/rois.json` is committed and holds the ROI ranges plus each element's
Q·Ω and σ. The GUI cannot express per-element Q·Ω or σ (single widgets at
`flavunato/gui.py:857,883`, read once at `:1525-1526`), so the scripts supply
each element's own pair; everything else matches the GUI.

Each ROI spans the element's **full simulated support** (`roi_source:
"reference"`), chosen for reproducibility — deliberately not the ROIs behind
the reference spreadsheet. `check_golden.py` fails if `roi_source` changes,
so the basis cannot be swapped silently.

Those ROIs are not needed: the spreadsheet counted **measured** counts, while
the program integrates **simulated** partial counts
(`flavunato/element_spectra.py:404`). Validation B therefore compares two
different methods and can never be an equality test — its deltas are a
tracked diagnostic, not a defect.

See `docs/notes/known_issues.md` for open issues.
