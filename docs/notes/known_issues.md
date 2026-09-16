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
**status: open**

`parse_xnra_full` returns `raw_counts` with 4099 points but
`simulated_counts` with only 1139 (`flavunato/uncertainty.py:287,299`). Both
are passed to `calculate_chi_squared_for_roi`
(`flavunato/uncertainty.py:305`, called from `flavunato/gui.py:1544` and
`flavunato/uncertainty.py:713`).

**Alignment is correct.** The function slices both arrays by array index
(`:353-354`), and both axes start at channel 0 and are contiguous, so index
== channel number for both. `[a:b]` selects the same physical channels on
each array. The length mismatch shortens the valid range; it does not
misalign anything.

**ROIs beyond channel 1138 are handled silently.** `:347` clamps `roi_end`
to `min(roi_end, len(raw), len(sim))`:

| ROI requested | result | what happened |
|---|---|---|
| 1100-1300 | chi2/nu 8.0224, dof 38 | truncated to 1100-1138, 39 of 201 channels |
| 1139-1400 | nan, dof 0 | `roi_start >= roi_end`, all-nan |

Neither case warns. A truncated ROI reports a chi-squared computed over part
of the window as if it were the whole, and `roi_counts` is likewise partial.
Practical risk is low: the simulation covers only 0..1138, so there is no
simulated signal beyond it and no reason to place an ROI there. All ROIs in
`tests/golden/rois.json` fall inside the valid range.

**Chi-squared is not display-only.** It feeds:

1. `*_chi2_adjusted` columns — always. `chi2_factor = sqrt(max(chi2/nu, 1))`
   is computed unconditionally (`:506-509`) and populates
   `sigma_stat_chi2_adjusted*` / `sigma_total_chi2_adjusted*` (`:519`),
   which are exported to Excel.
2. `sigma_total` — only when chi-squared adjustment is selected
   (`:567-572`). The GUI default is `'none'` (`flavunato/gui.py:914`), so it
   is inert unless the user changes the radio button.
3. Depth-profile row selection — always. `create_depth_profile` picks the
   reported row per element with `el_df['chi2_reduced'].idxmin()` (`:982`),
   so chi-squared decides which ROI's concentration and uncertainty appear
   in the profile regardless of adjustment method.

## 3. Audit items from the read-only review
**status: open**

Found during the initial verification pass; all are cosmetic or dead code, and
none affects numerical output.

| Item | Location | Status |
|---|---|---|
| Warning strings and messageboxes named old module files | `flavunato/gui.py:27,44,71,1505,1963` | fixed (R2a) |
| Header and window title said "Version 15" / "v15" | `flavunato/gui.py:1,3,79` | fixed (R2a) — title now `Flavunato v{__version__}` |
| Docstring example and notes named old module files | `flavunato/element_spectra.py:14,27`, `flavunato/uncertainty.py:412` | fixed (R2a) |
| `ELEMENT_SPECTRUM_AVAILABLE = False` set inside the *uncertainty* except block, clobbering the flag set at `:42` | `flavunato/gui.py:72` | fixed (R2b) — line deleted. The flag is never read, so there was no user-visible change; see item 6 |
| `COLOR_NAMES` imported, never used | `flavunato/uncertainty.py:119` | fixed (R2c) — import dropped; still defined and used in `element_spectra.py:73,577` |
| `json` imported, never used | `flavunato/gui.py:17` | fixed (R2c) |
| `calculate_uncertainty_for_element` defined, called from nowhere | `flavunato/uncertainty.py:1077` | fixed (R2c) |
| `calculate_uncertainty_v6`, `process_single_file_v6`, `process_batch_v6` aliases, zero references | `flavunato/uncertainty.py:625,838,937` | fixed (R2c) |
| `DEFAULT_SYSTEMATIC_UNCERTAINTIES` defined, zero references | `flavunato/uncertainty.py:1095` | fixed (R2c) |

**The `_v9` / `_v6` naming is intentional, not stale.** It denotes the
algorithm revision (the French expert's formula generation), not a file
version: `calculate_uncertainty_v9`, `process_batch_v9` and the `_v6` aliases
are API names, and the matching text at `flavunato/gui.py:46,807` and
`flavunato/uncertainty.py:304,461,871,1112` describes them correctly. The
Excel sheet name `Uncertainties_v9` (`flavunato/gui.py:1746`) must also stay:
the thesis exports use it.

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

## 6. Element spectrum code paths are unguarded
**status: open**

`ELEMENT_SPECTRUM_AVAILABLE` (`flavunato/gui.py:42,44`) is assigned but
**never read**. `PLOTTING_AVAILABLE` and `UNCERTAINTY_AVAILABLE` each gate
their feature (`:1965`, `:1504`); the element spectrum flag gates nothing.

Verified by blocking `flavunato.element_spectra` via `sys.modules`: the
except block at `:43-46` defines only `ELEMENT_SPECTRUM_AVAILABLE` and
`ELEMENT_COLORS`, so all six imported functions are left **undefined** —
`parse_element_spectrum`, `get_element_spectrum_summary`,
`get_available_elements`, `get_available_isotopes`,
`calculate_element_counts_from_spectrum`, `plot_element_spectra`.

Calling them raises `NameError` at `flavunato/gui.py:1246, 1253, 1400, 1439,
1481, 1582`. Every one of those sites sits inside an `except Exception`
(at `:1245, 1399, 1438, 1480, 1522`), and `NameError` is an `Exception`, so
the app does not crash: the user gets a dialog such as
`Failed to load element spectrum: name 'parse_element_spectrum' is not
defined` (`:1284, 1417, 1456, 1498, 1720`) instead of a clear
"feature unavailable" message.

Candidate: add an `ELEMENT_SPECTRUM_AVAILABLE` guard like the
plotting/uncertainty ones. Not done — it is new behaviour, not a cleanup.

## 7. chi-squared and A_A disagree on the ROI end channel
**status: open**

`roi_end` is documented as *exclusive* in `calculate_chi_squared_for_roi`
(`flavunato/uncertainty.py:334`) and sliced exclusively (`:353-354`), so
chi-squared covers channels `roi_start .. roi_end - 1`. Every other ROI
consumer treats `roi_end` as *inclusive*: `calculate_element_counts_from_spectrum`
masks with `channels <= roi_end` (`flavunato/element_spectra.py:359`).

So the two quantities in the same results row describe windows that differ
by one channel: A_A includes `roi_end`, chi-squared does not.

Measured effect on the reference ROIs, roughly 0.1-1% on chi2/nu:

| El | ROI | chi2/nu as computed | chi2/nu including `roi_end` |
|---|---|---|---|
| C | 195-349 | 3.2634 (dof 153) | 3.2610 (dof 154) |
| O | 322-504 | 2.0910 (dof 181) | 2.0886 (dof 182) |
| Zr | 900-1053 | 20.5838 (dof 152) | 20.4497 (dof 153) |
| Hf | 992-1137 | 4.9524 (dof 144) | 5.0148 (dof 145) |

Kept as-is for thesis consistency: the thesis numbers were produced with
this behaviour, and `tests/golden/reference.json` pins it at 1e-12.
Candidate for v1.1.

Fix direction (v1.1): make chi2 use the inclusive ROI end, matching A_A (the
validated uncertainty convention). Expected impact: only chi2 fields change;
golden reference must then be regenerated deliberately.

## 8. The 'approximate' A_A fallback is weakly signalled
**status: open**

When no element-spectrum metadata file is loaded, A_A falls back to

    A_A = int(roi_counts * concentration)

(`flavunato/gui.py:1591`, same logic at `flavunato/uncertainty.py:755-764`),
where `roi_counts` is the *experimental* ROI total. This assumes counts
partition in proportion to atomic concentration and ignores cross-section and
stopping differences between elements, so it can be wrong by orders of
magnitude for a heavy element in a light matrix. It also makes A_A vary per
layer, whereas the `'spectrum'` method gives one A_A per ROI.

It triggers whenever `self.element_spectrum_data is None` or
`raw_counts is None` (`flavunato/gui.py:1580`).

The warning is weak: an amber panel label (`:1308`) that disappears once any
file is loaded, and a status-bar glyph after calculation (`:1705,1707`).
Crucially the test is `if 'spectrum' in aa_methods_used` (`:1704`), so a
**mixed run is reported as `spectrum` if even one row used the spectrum
method** — the warning is suppressed exactly when it matters most. No dialog,
no log line, nothing in the results table. The `aa_method` column in the
export (`:1686`) is the only reliable record.

Methodology will state: always load the metadata file.
Candidate for v1.1: a clear warning, or block the calculation outright.

## 9. Element name mismatch gives A_A = 0 silently
**status: open**

If the requested element or isotope name is not found in the element-spectrum
export — after the exact and case-insensitive fallbacks — the function returns
`0, 0.0, 0` (`flavunato/element_spectra.py:381`) with no exception and no
message.

`A_A = 0` then makes `sigma_stat_rel` NaN (`flavunato/uncertainty.py:496-499`)
and the `else` branch at `:532-533` **drops the statistical term from the
quadrature sum**, so the reported total is just the constant terms. The
uncertainty is underestimated without warning.

Demonstrated with the example pair (spectrum holds C, Hf, O, Si, Zr), asking
for a missing name at concentration 0.19, Q.Omega 3%, sigma 0%:

| | mismatched name | valid element (Zr) |
|---|---|---|
| `A_A` | 0 | 1128896 |
| `sigma_stat_rel` | NaN | 9.41e-4 |
| `sigma_total_rel` | **0.03** | 0.0300148 |

The bad row reports a *smaller, cleaner* uncertainty than the good one, which
is what makes it hard to spot. The row is still tagged `aa_method='spectrum'`
(`flavunato/gui.py:1589`), since the call returned normally. In the export the
NaN statistical fields are written as `None` (`:1664,1669,1674`), i.e. blank
cells indistinguishable from any other missing value, and the tree shows
`"N/A"` (`:1618-1628`).

Only tell: `element_counts = 0` in the export (`:1684`).

Rows whose concentration is 0 are dropped earlier (`:1574-1575`), so this
bites specifically when the layer model and the spectrum export disagree on
naming (e.g. `Zr` versus `90Zr`). UNVERIFIED whether SIMNRA produces such a
divergence in practice; the example pair is internally consistent.

Candidate for v1.1: warn and mark the row.
