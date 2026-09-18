# Known issues

Behaviours worth knowing about, recorded for reference. Calculation behaviour
is unchanged throughout: the golden regression still reproduces the thesis
results. Items marked **open** are live in the current code. Items marked
**resolved** say how — by a documented decision, or by a code change with the
commit that made it.

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
`simulated_counts` with only 1139 (`flavunato/uncertainty.py:285,296`). Both
are passed to `calculate_chi_squared_for_roi`
(`flavunato/uncertainty.py:303`, called from `flavunato/gui.py:1544` and
`flavunato/uncertainty.py:704`).

**Alignment is correct.** The function slices both arrays by array index
(`:351-352`), and both axes start at channel 0 and are contiguous, so index
== channel number for both. `[a:b]` selects the same physical channels on
each array. The length mismatch shortens the valid range; it does not
misalign anything.

**ROIs beyond channel 1138 are handled silently.** `:345` clamps `roi_end`
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
   is computed unconditionally (`:504-507`) and populates
   `sigma_stat_chi2_adjusted*` / `sigma_total_chi2_adjusted*` (`:517`),
   which are exported to Excel.
2. `sigma_total` — only when chi-squared adjustment is selected
   (`:565-570`). The GUI default is `'none'` (`flavunato/gui.py:914`), so it
   is inert unless the user changes the radio button.
3. Depth-profile row selection — always. `create_depth_profile` picks the
   reported row per element with `el_df['chi2_reduced'].idxmin()` (`:704`),
   so chi-squared decides which ROI's concentration and uncertainty appear
   in the profile regardless of adjustment method.

## 3. Audit items from the read-only review
**status: resolved**

Found during the initial verification pass; all are cosmetic or dead code, and
none affects numerical output.

| Item | Location | Status |
|---|---|---|
| Warning strings and messageboxes named old module files | `flavunato/gui.py:27,44,71,1505,1963` | fixed (R2a) |
| Header and window title said "Version 15" / "v15" | `flavunato/gui.py:1,3,79` | fixed (R2a) — title now `Flavunato v{__version__}` |
| Docstring example and notes named old module files | `flavunato/element_spectra.py:14,27`, `flavunato/uncertainty.py:412` | fixed (R2a) |
| `ELEMENT_SPECTRUM_AVAILABLE = False` set inside the *uncertainty* except block, clobbering the flag set at `:41` | `flavunato/gui.py:72` | fixed (R2b) — line deleted. The flag is never read, so there was no user-visible change; see item 6 |
| `COLOR_NAMES` imported, never used | `flavunato/uncertainty.py:119` | fixed (R2c) — import dropped; still defined and used in `flavunato/element_spectra.py:73,577` |
| `json` imported, never used | `flavunato/gui.py:17` | fixed (R2c) |
| `calculate_uncertainty_for_element` defined, called from nowhere | `flavunato/uncertainty.py:1077` | fixed (R2c) |
| `calculate_uncertainty_v6`, `process_single_file_v6`, `process_batch_v6` aliases, zero references | `flavunato/uncertainty.py:625,838,937` | fixed (R2c) |
| `DEFAULT_SYSTEMATIC_UNCERTAINTIES` defined, zero references | `flavunato/uncertainty.py:1095` | fixed (R2c) |

**The `_v9` / `_v6` naming is intentional, not stale.** It denotes the
algorithm revision (the French expert's formula generation), not a file
version: `calculate_uncertainty_v9` and the `_v6` aliases were API names
(`process_batch_v9` has since been removed with the command-line entry points,
c0f5d0d), and the matching text at `flavunato/gui.py:47,799,807,1500` and
`flavunato/uncertainty.py:2,301,458` describes them correctly. The
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

The ROIs behind the reference spreadsheet are **not needed**. Its author
counted MEASURED counts; the program integrates SIMULATED partial counts.
VALIDATION B therefore compares two different methods and can never be an
equality test -- its deltas are a tracked diagnostic, not a defect.
`tests/golden/rois.json` accordingly uses each element's full simulated support
(`roi_source: "reference"`), chosen for
reproducibility.

Note that Zr's xlsx count (1 150 000) exceeds the element's entire simulated
integral (1 128 896.2, +1.84%), so it is unreachable at any ROI under the
current definition.

## 5. CLI help crashes on Windows cp1252 consoles
**status: resolved (code removed in c0f5d0d)**

`python -m flavunato.uncertainty --help` failed with `UnicodeEncodeError` on
Windows cp1252 consoles (`Ω` in the argparse help). Pre-existing (reproduced
on v1.0-thesis code). It was first fixed by reconfiguring stdout to UTF-8 at
the start of each CLI `main()`; both entry points have since been removed, so
the failing path no longer exists.

See item 14 for the equivalent limitation in the graphical interface.

## 6. Element spectrum code paths are unguarded
**status: open**

`ELEMENT_SPECTRUM_AVAILABLE` (`flavunato/gui.py:41,43`) is assigned but
**never read**. `PLOTTING_AVAILABLE` and `UNCERTAINTY_AVAILABLE` each gate
their feature (`:1962`, `:1501`); the element spectrum flag gates nothing.

Verified by blocking `flavunato.element_spectra` via `sys.modules`: the
except block at `:42-45` defines only `ELEMENT_SPECTRUM_AVAILABLE` and
`ELEMENT_COLORS`, so all six imported functions are left **undefined** —
`parse_element_spectrum`, `get_element_spectrum_summary`,
`get_available_elements`, `get_available_isotopes`,
`calculate_element_counts_from_spectrum`, `plot_element_spectra`.

Calling them raises `NameError` at `flavunato/gui.py:1245, 1252, 1399, 1438,
1480, 1581`. Every one of those sites sits inside an `except Exception`
(at `:1244, 1398, 1437, 1479, 1521`), and `NameError` is an `Exception`, so
the app does not crash: the user gets a dialog such as
`Failed to load element spectrum: name 'parse_element_spectrum' is not
defined` (`:1283, 1416, 1455, 1497, 1719`) instead of a clear
"feature unavailable" message.

Candidate: add an `ELEMENT_SPECTRUM_AVAILABLE` guard like the
plotting/uncertainty ones. Not done — it is new behaviour, not a cleanup.

## 7. chi-squared and A_A disagree on the ROI end channel
**status: open**

`roi_end` is documented as *exclusive* in `calculate_chi_squared_for_roi`
(`flavunato/uncertainty.py:331`) and sliced exclusively (`:351-352`), so
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

When no element-spectrum export is loaded, A_A falls back to

    A_A = int(roi_counts * concentration)

(`flavunato/gui.py:1591`),
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

Methodology states: always load the element-spectrum export.
Candidate for v1.1: a clear warning, or block the calculation outright.

## 9. Element name mismatch gives A_A = 0 silently
**status: open**

If the requested element or isotope name is not found in the element-spectrum
export — after the exact and case-insensitive fallbacks — the function returns
`0, 0.0, 0` (`flavunato/element_spectra.py:381`) with no exception and no
message.

`A_A = 0` then makes `sigma_stat_rel` NaN (`flavunato/uncertainty.py:495-497`)
and the `else` branch at `:531` **drops the statistical term from the
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

Rows whose concentration is 0 are dropped earlier (`:1575-1576`), so this
bites specifically when the layer model and the spectrum export disagree on
naming (e.g. `Zr` versus `90Zr`). UNVERIFIED whether SIMNRA produces such a
divergence in practice; the example pair is internally consistent.

Candidate for v1.1: warn and mark the row.

## 10. Mouse-wheel scrolling likely does not work on Linux
**status: open**

The scrollable panels bind `<MouseWheel>` (`flavunato/gui.py:175`, `:832`),
which is the Windows and macOS event name. X11 reports wheel movement as
`<Button-4>` and `<Button-5>`, and neither is bound anywhere, so the wheel is
expected to do nothing on Linux. The scrollbars themselves still work, so the
panels remain usable by dragging.

UNVERIFIED: inferred from the bindings; not tested on a Linux machine.

## 11. All-NaN chi-squared makes the depth profile raise
**status: open**

`create_depth_profile` selects the reported row per element with
`el_df['chi2_reduced'].idxmin()` (`flavunato/uncertainty.py:704`). If every row
for an element in a layer has `chi2_reduced = NaN` — which happens when the
`.xnra` carries no simulated spectrum, so `calculate_chi_squared_for_roi`
returns NaN for every ROI — pandas raises
`ValueError: Encountered all NA values`.

This surfaces as the generic dialog `Export failed: ...` from the catch-all
handler (`flavunato/gui.py:1824`), which does not say that chi-squared was the
cause.

Results themselves are unaffected: the uncertainty calculation tolerates a NaN
chi-squared (`chi2_factor` falls back to 1.0). Only the depth-profile export
fails.

## 12. Global cross-section input ignored for isotope entries
**status: open**

In isotope mode — which cannot currently be switched on, see item 15 — an ROI
entry beginning with a mass number takes the
`if isotope_mode and is_isotope` branch (`flavunato/gui.py:1563-1568`), which
obtains the cross-section uncertainty from
`get_isotope_cross_section_uncertainty(entry, overrides)`. That function takes
only the species name and the override dictionary
(`flavunato/uncertainty.py:414-447`) — **the global "Cross-section σ (%)" field
is never passed to it and cannot affect the result.** The field is used only in
the `else` branch (`flavunato/gui.py:1572`), i.e. for element-mode entries.

The lookup has four exits, all verified by running it:

| Entry | Result | Exit |
|---|---|---|
| `12C` with an override | the override | custom override (`:433`) |
| `12C` | 5 % | exact isotope key (`:437`) |
| `13C`, `17O`, `18O` | value of the main isotope | exact isotope key (`:437`), unverified value |
| `14C`, `3H`, `15O`, `13N` | the **element** value (5 %, 2 %, 2 %, 3 %) | element key after stripping the mass number (`:443`) |
| `28Si`, `90Zr`, `180Hf` | 0 % | Rutherford fallback (`:447`) — correct when scattering is Rutherford |
| `7Li` | **0 %** | Rutherford fallback (`:447`) — **wrong when it is not** |

Two exits deserve attention.

All stable isotopes of H, C, N and O are listed explicitly as exact keys
(`1H`, `2H`, `12C`, `13C`, `14N`, `15N`, `16O`, `17O`, `18O` —
`flavunato/uncertainty.py:135-160`), so the element-key step is reached only by
a non-stable entry such as `3H` or `14C`, or by a mistyped name. Such an entry
silently takes the element's value **and its reaction label**: `3H` is reported
as 2 % with `ERDA: 1H(4He,1H)4He`, and `14C` as 5 % with `NRA: 12C(d,p0)13C`.

The 0 % fallback is reached whenever the base element is absent from the table.
The cited note gives 0 % for the reaction `Mx(a,a)Mx`; equating "absent from
the table" with "measured by Rutherford scattering" is this program's reading.
The fallback therefore fires regardless of the reaction actually used, so it is
right for a species whose cross section really is Rutherford and wrong for one
whose is not. Raising the global field corrects neither exit.

No workaround is needed at present, and none is available. Item 15 keeps the
isotope branch out of reach, so every entry takes the global field and this
issue has no effect on any result the program can currently produce. It becomes
live again if item 15 is fixed; the remedy then is an explicit per-isotope
override for every species that is not `1H`, `12C` or `16O` and is not measured
by Rutherford scattering — which also requires the override rows restored. See
the provenance table in `docs/methodology.md` under *Cross sections*.

## 13. Licence not yet chosen
**status: open**

Licence not yet chosen; to be decided with the lab/CNRS before public release.

There is no `LICENSE` file and no licence statement in the README or the
documentation, so default copyright applies and the code is not open source as
it stands. `docs/software_overview.md` therefore states only that the software
is available from the authors on request.

## 14. GUI console output fails when stdout is not UTF-8
**status: open**

The parsing and plotting code prints progress messages containing non-ASCII
symbols: 19 such `print()` calls in `flavunato/plotting.py` (for example `📂`
at `:17`, `✓` at `:74`, `⚠️` at `:78`) and two in
`flavunato/element_spectra.py` (`:588`, `:590`). Nothing reconfigures stdout —
the `sys.stdout.reconfigure` calls that once did so belonged to the
command-line entry points and went with them in c0f5d0d.

In a real Windows console this is fine: Python writes to the console through a
UTF-16 path that does not use the code page, and launching
`python -m flavunato` from a plain `cmd` window, loading an `.xnra` and
generating both a spectrum plot and an element-spectrum plot works without
error (tested).

The failure appears when console output is **redirected** — piped to another
command, written to a log file, or captured by some IDE run panels. Python
then falls back to the locale encoding, `cp1252` on a typical French or
English Windows install, and the first non-ASCII message raises
`UnicodeEncodeError`. Inside the interface that surfaces as a
`Failed to generate plot: 'charmap' codec can't encode ...` dialog, so the
plot is lost rather than the program crashing.

Workaround: set `PYTHONIOENCODING=utf-8` before launching, or start with
`pythonw`, which has no stdout to redirect.

Fix proposal (v1.1): reconfigure stdout to UTF-8 with `errors="replace"` at
the start of the GUI `main()`, as the command-line entry points used to do.
Not implemented.

## 15. Isotope mode cannot be switched on
**status: open**

The isotope-resolved uncertainty path is implemented but unreachable. Three
things block it independently.

The mode flag is constructed `False` and never assigned again:

```python
# flavunato/gui.py:905-909
# Isotope mode has been removed from the UI. Keep variables defined
# so downstream code (override helpers, calc loop) still works; they
# just always report "disabled / no overrides".
self.isotope_mode = tk.BooleanVar(value=False)
self.isotope_override_container = ttk.Frame(left_panel)  # orphan, not gridded
```

There is no `.set(` on it anywhere and no widget is bound to it, so the test
at `flavunato/gui.py:1563` never takes the isotope branch and the call to
`get_isotope_cross_section_uncertainty` at `:1566` is dead. The default table
at `flavunato/uncertainty.py:135-160` is consulted only from that function, so
it is dead too; `gui.py:56` imports it and never uses it.

The override rows are equally unreachable. `add_isotope_override_row`
(`flavunato/gui.py:1069`) is never called, so `isotope_override_widgets` stays
empty and `get_isotope_overrides()` (`:1101-1113`) always returns `{}`. The
container frame is created but never gridded (`:909`).

Consequences, in the current code:

- every ROI entry takes the element branch (`flavunato/gui.py:1569-1573`), so
  a name written `28Si` is summed into `Si` and takes the global cross-section
  field;
- concentrations come from `layer['concentrations']` (`:1571`), the
  isotope-summed dict, never from `layer['isotope_concentrations']` (`:1564`),
  although the parser fills both (`flavunato/uncertainty.py:264-275`);
- `A_A` is integrated over the element partial spectrum, since
  `use_isotope` at `:1587` is always `False`;
- item 12 has no present effect, for the same reason.

Isotope **plotting** is not affected and works normally: the Element/Iso Data
tab's button is wired at `flavunato/gui.py:685-686` to
`plot_isotope_spectra_gui` (`:1418`).

No test covers the path. `tests/golden/generate_golden.py:88` passes
`use_isotope=isotope_mode`, read from `tests/golden/rois.json:14`, which is
`false`; `tests/validation/compare_manual.py:140` hard-codes `False`.
`check_golden.py` guards `roi_source` (`:52-54`) but not `isotope_mode`, so a
flipped flag would not be caught the way a changed `roi_source` is.

Fix proposal (v1.1): restore the isotope toggle and the override rows in the
uncertainty tab, then cover the path with a test. Not implemented. Until then
the documentation describes the formalism as implemented, not as available.
