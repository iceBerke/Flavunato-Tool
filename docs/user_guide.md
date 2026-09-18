# User guide

How to use Flavunato. For the equations behind the numbers, see
[methodology](methodology.md).

## The file bar

At the top of the window, above the tabs. Click **Browse…** and select the
`.xnra` file. This selection is shared by every tab.

The GUI handles **one file at a time**. Several samples means one analysis per
sample: load each `.xnra` with its own element-spectrum export, calculate, and
export the results before moving to the next.

## Loading the element spectrum — "Element/Iso Data" tab

Go to the **Element/Iso Data** tab and click **Load File…**, then choose the
element-spectrum export that SIMNRA produced for this measurement (a
tab-separated `.txt`).

**Do this every time.** Without it, Flavunato falls back to an approximate
estimate of the detected counts that ignores the differences in cross section
and stopping between elements, and can be wrong by orders of magnitude. The
only signs are an amber status label and a `⚠` in the status line after
calculation, and that warning is suppressed if even one row used the proper
method ([known issue 8](notes/known_issues.md)).

Once loaded, the tab lists the elements and isotopes found in the file. Tick
the ones you want and use **Plot Element Spectra**, **Plot Isotope Spectra** or
**Plot All Selected**. The **All** / **None** buttons select or clear a whole
list. **Clear** unloads the file.

## The "Uncertainty (v9)" tab

### Uncertainty components

**Q·Ω Uncertainty (%)** — default 3. **This field is in percent: type `3` for
3 %.** It is the combined uncertainty on the analysis charge and the detector
solid angle, a property of the setup, identical for every element in the
measurement.

*How to estimate it.* Following Diallo (2025): take the ratios of the
simulated Particle·sr values to the corresponding measured Particle·sr values
recorded during normalisation, across the samples of one analysis session (the
cited note says "analysis section"; read here as session, pending confirmation
by the author), and use the standard deviation of that set. The estimate is
valid for samples from the same session. Flavunato does not compute this for you — form the ratios
yourself and type the result in.

**Default Reaction** — selects the cross-section uncertainty for the reaction
you are using. Choosing a reaction fills in the σ field automatically; the
field only becomes editable for a custom reaction.

**Cross-section σ (%)** — default 0, which is correct for pure Rutherford
backscattering. Non-Rutherford reactions have a non-zero value. Also in
percent.

**Isotope mode** — **not available in this version.** The uncertainty tab has
no isotope toggle, so every ROI entry is treated as an element: a name written
with a mass number, for example `28Si`, is summed into the element total and
takes the global **Cross-section σ (%)** field. The isotope-resolved path
exists in the code but cannot be switched on; see
[known issue 15](notes/known_issues.md). It would in any case only work if the
`.xnra` layer model itself used isotope names.

Isotope *plotting* is unaffected — see *Element/Iso data*, which lists and
plots per-isotope spectra from the same export.

### Isotope σ overrides

> **Not available in this version.** No override row can be created, so the
> built-in defaults below cannot be replaced from the interface. The section is
> kept because the defaults themselves still describe what the program would
> apply, and the warnings under it matter for reading any isotope-resolved
> result. See [known issue 15](notes/known_issues.md).

Were isotope mode available, overrides would apply only to ROI entries whose
name begins with a mass number. An entry written `Si` would take the global
**Cross-section σ (%)** field even if an override for `28Si` existed; only
`28Si` would pick the override up, and with isotope mode off overrides would be
ignored entirely.

Each override row would take an isotope name and a σ in percent, with `×` to
remove the row. An isotope with no override falls back to the built-in default
for that isotope, then to the element default, and finally to 0 %.

> **Only `H`/`1H`, `C`/`12C`, `O`/`16O` and the 0 % elastic-α value come from
> the cited method.** Every other entry in the built-in table — `2H`, `13C`,
> `N`, `14N`, `15N`, `17O`, `18O` — is an unverified addition of this program.
>
> **Any element not in the table receives 0 %**, including light ones such as
> `7Li`. The cited method gives 0 % for elastic α scattering, `Mx(α,α)Mx`;
> reading this as Rutherford and applying it to every unlisted species is this
> program's interpretation, so the value is only right when that species' cross
> section really is Rutherford.
>
> All stable isotopes of H, C, N and O are listed, so a non-stable or mistyped
> entry such as `3H` or `14C` silently takes the element's σ and its reaction
> label instead.
>
> For any light isotope outside the trusted set, the default should not be
> relied on: an explicit override from a documented source would be needed,
> which is not currently possible. The full table with its provenance is in
> [methodology](methodology.md#uncertainty-budget), under *Cross sections*.

Because isotope mode cannot be switched on, the global **Cross-section σ (%)**
field currently applies to every entry, including one written `28Si`. Were the
path re-enabled, that entry would take the table value or an override and the
field would be ignored for it — see
[known issue 12](notes/known_issues.md).

### Adjustment method

| Option | Meaning |
|---|---|
| **Standard (Eq. 3)** | the default; no rescaling. This is Eq. (D3) in the methodology. |
| **χ²-Adjusted (Eq. 6)** | rescales the statistical term by √χ²ᵥ when the fit is worse than the counting statistics predict. This is Eq. (D6). |
| **AUC-Adjusted** | rescales by the area mismatch instead. Not part of the cited method — a Flavunato addition, for comparison only. |

The labels "Eq. 3" and "Eq. 6" in the interface refer to equations **(D3)** and
**(D6)** in the [methodology](methodology.md).

Leave this on **Standard** unless you have a reason not to, and record which
setting you used — it changes the reported uncertainty.

### Layers to calculate

Tick the layers to include. **All** / **None** select or clear them. The list
populates once an `.xnra` file is loaded.

Layers are numbered in the order they appear in the `.xnra` file, starting at
1; Flavunato does not reorder them. SIMNRA writes the layer stack from the
surface inwards, so layer 1 is normally the surface layer and the highest
number the substrate — but this comes from the file, not from Flavunato. If it
matters, check layer 1's composition against what you expect at the surface.

### Regions of interest (ROIs)

Each row is: **Name**, **Start Ch**, **End Ch**, **Elements/Isotopes**
(comma-separated, e.g. `Zr,Hf`). Channels are inclusive at both ends.

- **+ Add ROI** adds an empty row; `×` on a row deletes it.
- **Clear All** empties the list.
- **Load Defaults** fills in example ROIs for the selected reaction. **These
  are generic placeholders with no relation to your sample** — treat them as a
  starting shape and replace the channel ranges with your own.

A row is only used if the element list is non-empty **and** the start channel
is below the end channel. Rows that fail either test are dropped silently, so
check that the number of result rows matches what you expect.

Type numbers with a **`.`** as the decimal separator. A comma is rejected with
an error dialog.

### Calculating

Click **Calculate Uncertainties**. The status line afterwards reports how many
results were produced, the adjustment method, the Q·Ω value, and whether the
counts came from the element spectrum (`A_A: spectrum ✓`) or the approximate
fallback (`A_A: approximate ⚠`).

## Reading the results table

| Column | Meaning |
|---|---|
| `Layer` | layer number in the `.xnra` model (see *Layers to calculate*) |
| `Element` | element or isotope |
| `Conc(%)` | concentration from the fitted model, in atomic percent |
| `Stat(rel)` | counting-statistics uncertainty, relative |
| `Q·Ω(rel)` | charge/solid-angle uncertainty, relative — constant across rows |
| `σ(rel)` | cross-section uncertainty, relative — constant per reaction |
| `±Total` | the three combined in quadrature, under the selected adjustment |
| `ROI` | which region of interest produced this row |
| `A_A` | detected counts for this element in the ROI |
| `f_A` | this element's share of the simulated total in the ROI (diagnostic) |
| `χ²/ν` | reduced chi-squared for the ROI — fit quality, not an uncertainty |
| `Status` | the symbol below |
| `AUC` | simulated ÷ measured area in the ROI; near 1 means correct normalisation |

Relative columns are the ones to quote when comparing elements; `±Total` is
scaled by the concentration.

### χ² status symbols

| Symbol | Label | χ²ᵥ |
|---|---|---|
| `✓✓` | Perfect | 0.90 – 1.10 |
| `✓` | Great | 1.10 – 3.0 |
| `⚠` | Not OK | 3.0 – 10.0 |
| `✗` | Very bad | > 10.0 |
| `⚠` | Too low | < 0.90 |
| `?` | N/A | not available |

A value below 0.90 is flagged too: it usually means overestimated
uncertainties or an over-parameterised fit, not a better result.

## Exporting

**Export Results** writes every result row. Choose `.xlsx` (sheet
`Uncertainties_v9`) or `.csv`. This is the full record, including the
`aa_method` and `element_counts` columns used by the checklist below.

**Export Depth Profile** writes a layer-by-layer table: thickness, and per
element the concentration and its uncertainty. As `.xlsx` it has three sheets —
`Depth Profile`, `Raw Data` and `Parameters` (the settings used). As `.csv`
only the profile is written.

When an element was measured in more than one ROI within a layer, the profile
reports the ROI with the **lowest χ²ᵥ**. Ties go to whichever ROI was defined
first. This applies whether or not you selected a χ² adjustment.

Neither dialog suggests a folder or filename — pick both yourself.

## Plots

The **General**, **Raw Data**, **Smoothed Data**, **Simulated Data**,
**Appearance** and **Axes & Limits** tabs control the spectrum plot: which
series are drawn, their colours and markers, fonts, legend, axis ranges and
labels. **Generate Plot** draws it; **Export Plot** saves `.png` or `.pdf`.

Element and isotope plots are produced from the Element/Iso Data tab instead.

With `mplcursors` installed, hovering a curve shows a tooltip. On the spectrum
plot it gives the series name, the channel, the energy in keV (from the
calibration) and the counts. On element and isotope plots it gives the series
name with its colour name, then the x value with its unit (`Ch` or `keV`,
following the selected axis mode) and the counts.

There are no keyboard shortcuts and no menu bar.

## Before using results — checklist

Run through this before quoting any number.

1. **`aa_method` reads `spectrum` in every row.** Any `approximate` row used
   the fallback estimate and is not suitable for quantification. The status
   line can show `✓` even when some rows fell back —
   [known issue 8](notes/known_issues.md).
2. **`element_counts` is greater than 0 in every row.** A zero means the
   element name was not found in the element-spectrum export. The statistical
   term is then dropped and the uncertainty comes out *smaller* than a correct
   one, with no warning — [known issue 9](notes/known_issues.md).
3. **Element names match the export exactly.** Compare the names in your ROI
   rows against the element and isotope lists shown in the Element/Iso Data
   tab. This is what prevents point 2.
4. **ROIs start at channel 1 or above.** Channel 0 of the experimental
   spectrum can hold a non-physical value and is absent from the element
   spectrum — [known issue 1](notes/known_issues.md).
5. **ROIs end inside the simulated range.** An ROI reaching past the last
   simulated channel is silently truncated, and one entirely beyond it gives no
   χ² at all — [known issue 2](notes/known_issues.md).
6. **Record which adjustment method was used.** `Standard` is the default and
   the one to use unless you have a reason otherwise; the choice changes the
   reported uncertainty and is saved on the `Parameters` sheet of the
   depth-profile export.

Also worth knowing: χ²ᵥ selects which ROI appears in the depth profile even
when no χ² adjustment is applied ([known issue 2](notes/known_issues.md)), and
the ROI end channel is treated inclusively for the counts but exclusively for
χ² ([known issue 7](notes/known_issues.md)).
