# Known issues

Documentation only. No behaviour has been changed; per CLAUDE.md rule 3 these
are recorded, not fixed.

## 1. Experimental channel 0 holds a non-physical value
**status: open (documentation only)**

In the `.xnra` experimental spectrum, channel 0 contains 2300 counts while
channels 1-17 are all 0. The value is an artefact, not signal. The
element-spectrum export omits channel 0 entirely (it runs 1..4099 against the
`.xnra`'s 0..4098), so the two sources disagree about whether the channel
exists at all.

**ROIs must not include channel 0.** No ROI in `tests/golden/rois.json` does.

Channel numbering, verified numerically against the example files: metadata
channel N *is* `.xnra` channel N -- the experimental and simulated columns
match the `.xnra` spectra at shift 0 (100% exact, maxdiff 0) and not at +-1
(~56% / ~22%). Both ROI selections in
`calculate_element_counts_from_spectrum` therefore cover the same physical
channels, despite one masking by channel number
(`flavunato/element_spectra.py:359`) and the other slicing by array index
(`flavunato/element_spectra.py:398-401`). There is no off-by-one.

## 2. raw_counts / simulated_counts length mismatch
**status: open, not investigated**

`parse_xnra_full` returns `raw_counts` with 4099 points but
`simulated_counts` with only 1139 (`flavunato/uncertainty.py:287,299`). Both
are passed to `calculate_chi_squared_for_roi`
(`flavunato/uncertainty.py:306`, called from `flavunato/gui.py:1543`).

All ROIs currently in `rois.json` fall inside 0..1138, so the shorter array
covers them. The behaviour for an ROI extending beyond channel 1138 has not
been investigated. With `adjustment_method = "none"` the chi-squared result
does not affect any uncertainty (`chi2_factor` stays 1.0), so this does not
influence present results.

## 3. Audit items from the read-only review
**status: open**

Found during the initial verification pass; all are cosmetic or dead code, and
none affects numerical output.

| Item | Location |
|---|---|
| Warning string says `xnra_element_spectra`, import is `.element_spectra` | `flavunato/gui.py:44` |
| Warning string says `xnra_uncertainty_v9`, import is `.uncertainty` | `flavunato/gui.py:71` |
| `ELEMENT_SPECTRUM_AVAILABLE = False` set inside the *uncertainty* except block, clobbering the flag set at `:40` | `flavunato/gui.py:70` |
| `COLOR_NAMES` imported, never used | `flavunato/uncertainty.py:119` |
| `json` imported, never used | `flavunato/gui.py:17` |
| Window title and header say "v15" / "Version 15" in a file named `flavunato/gui.py` | `flavunato/gui.py:1,3,77` |
| `calculate_uncertainty_for_element` defined, called from nowhere | `flavunato/uncertainty.py:1077` |

## 4. The A_A definition, and the choice of reference ROIs
**status: resolved (documentation)**

`A_A = round(sum(sim_A[ROI]))` -- the integrated **simulated** counts in the
ROI (`flavunato/element_spectra.py:404`). Comments at
`flavunato/element_spectra.py:395,403` show it replaced an earlier
experiment-anchored definition before version control. The repo version is
confirmed as the thesis version. This explains part of the VALIDATION B
deltas.

The supervisor's ROIs are **not needed**. He counted MEASURED counts; the
program integrates SIMULATED partial counts. VALIDATION B therefore compares
two different methods and can never be an equality test -- its deltas are a
tracked diagnostic, not a defect. `tests/golden/rois.json` accordingly uses
each element's full simulated support (`roi_source: "reference"`), chosen for
reproducibility.

Note that Zr's xlsx count (1 150 000) exceeds the element's entire simulated
integral (1 128 896.2, +1.84%), so it is unreachable at any ROI under the
current definition.

## 5. CLI help crashes on Windows cp1252 consoles
**status: resolved**

`python -m flavunato.uncertainty --help` failed with `UnicodeEncodeError` on
Windows cp1252 consoles (`Ω` in the argparse help). Pre-existing (reproduced
on v1.0-thesis code).

Fixed: both CLI `main()` functions now reconfigure stdout to UTF-8 with
`errors="replace"` at start (`flavunato/uncertainty.py:1104`,
`flavunato/element_spectra.py:600`). Both CLIs print non-ASCII —
`uncertainty` at 18 call sites, `element_spectra` via `plot_element_spectra`
(`:588,590`). The GUI is untouched.

Workaround, still valid for older Python without `sys.stdout.reconfigure`
or for other tools: set `PYTHONIOENCODING=utf-8` (cmd) or
`$env:PYTHONIOENCODING='utf-8'` (PowerShell).
