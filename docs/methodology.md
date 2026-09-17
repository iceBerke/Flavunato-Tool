# Methodology

How Flavunato computes concentration uncertainties from SIMNRA ion beam
analysis (IBA) data.

The uncertainty formalism follows the internal technical note of
Diallo [@diallo2025iba], whose Eqs. (D1)–(D6) are reproduced below. Everything that
is not taken from that note — numerical conventions, the estimator for the
detected counts, additional cross-section values, fit-quality thresholds and
the optional AUC rescaling — is a **program choice** and is labelled as such
throughout. Such choices are implementation decisions of this software, not
recommendations of the cited note.

---

## Overview

Flavunato reads a SIMNRA `.xnra` file together with the corresponding
element-spectrum export (a tab-separated `.txt` file), and reports, for each
element in each layer of the fitted model, a concentration and its
uncertainty.

**From the `.xnra` file** (XML, IDF schema with SIMNRA extensions) the program
takes the fitted layer model — layer thicknesses in $10^{15}\ \text{atoms/cm}^2$
and elemental concentrations as atomic fractions — together with the
experimental and simulated spectra, the energy calibration
$E = \text{offset} + \text{gain}\times\text{channel}$, and the beam and
geometry metadata. Isotope-resolved concentrations are retained separately
from element totals; element totals are formed by summing isotopes of the same
element after stripping the mass number.

**From the element-spectrum export** the program takes the per-element and
per-isotope simulated partial spectra, channel by channel. These carry the
information the `.xnra` does not: how the total simulated spectrum decomposes
into individual elemental contributions.

**From the user** the program takes the regions of interest (ROIs, as channel
ranges with an associated element list), the charge–solid-angle uncertainty
$\Delta_{Q\Omega}$, the cross-section uncertainty $\Delta_{\sigma_A}$, and the
choice of adjustment method.

The program does **not** perform the spectrum fit; that is done in SIMNRA
[@mayer1999simnra]. Flavunato consumes a converged fit and propagates
uncertainties onto it.

---

## Areal density and detected counts

The number of counts detected for element $A$ is [@diallo2025iba, Eq. 1]

$$
A_A = \frac{Q \cdot \Omega \cdot \int_0^{x_A^0} f \cdot N_A^{A_m B_n}(x) \cdot \sigma_A(x)\, dx}{\cos \alpha} \tag{D1}
$$

where $Q$ is the collected charge, $\Omega$ the detector solid angle, $f$ a
normalization factor, $N_A^{A_m B_n}(x)$ the atomic concentration profile of
element $A$, $\sigma_A(x)$ the reaction cross section, and $\alpha$ the
incidence angle.

Inverting this relation gives the areal atomic density
[@diallo2025iba, Eq. 2]

$$
N_A = N_A^{A_m B_n} \cdot x = \frac{\cos \alpha \cdot A_A}{Q \cdot \Omega \cdot \sigma_A} \tag{D2}
$$

**Scope note.** Flavunato does not evaluate Eqs. (D1)–(D2). Concentrations and layer
thicknesses are read directly from the converged SIMNRA layer model.
Eqs. (D1)–(D2) are reproduced here because they establish *why* $A_A$, $Q\Omega$ and
$\sigma_A$ are the three quantities that carry uncertainty into $C_A$: they
are the terms through which the measurement enters the concentration. The
*Uncertainty budget* below propagates precisely these three terms.

---

## Detected counts $A_A$

$A_A$ is the count of element $A$ at its reference peak, integrated over the
ROI. Flavunato offers two estimators.

### Spectrum method

All results reported in this work use this method.

**Program choice.** $A_A$ is the integrated *simulated partial spectrum* of
element $A$ over the ROI:

$$
A_A = \operatorname{round}\!\left( \sum_{i \in \text{ROI}} y_i^{\mathrm{sim},A} \right)
$$

where $y_i^{\mathrm{sim},A}$ is the simulated contribution of element $A$ in
channel $i$, taken from the element-spectrum export. The ROI is **inclusive at
both ends**: channels $i$ with $i_\mathrm{start} \le i \le i_\mathrm{end}$.

No experimental normalisation is applied. The statistical uncertainty derived
from this quantity (see *Counting statistics*) therefore reflects the
*predicted* counting statistics of the fitted model, not the measured ones.
This is a deliberate consequence of the estimator: it is reproducible from the
fit alone and separates element $A$ from the overlapping contributions of other
elements in the ROI, but it will underestimate scatter if the fit itself is
poor. This is assessed separately (see *Fit quality*).

In isotope mode the same integral is taken over the isotope-resolved partial
spectrum instead of the element total.

Two diagnostics are recorded alongside $A_A$ but do not enter any
uncertainty: the element fraction
$f_A = \sum_{\text{ROI}} y^{\mathrm{sim},A} / \sum_{\text{ROI}} y^{\mathrm{sim,total}}$,
and the experimental ROI sum $\sum_{\text{ROI}} y^{\mathrm{exp}}$.

### Approximate fallback — not recommended

**Program choice.** If no element-spectrum export has been loaded, the program
falls back to $A_A = \lfloor R \cdot C_A \rfloor$, where $R$ is the
experimental ROI total and $C_A$ the atomic fraction. This assumes counts
partition in proportion to atomic concentration, which ignores the
cross-section and stopping differences between elements; for a heavy element
in a light matrix it can be wrong by orders of magnitude.

**Always load the metadata file.** Results obtained with the fallback are not
suitable for quantification. Every exported row records which estimator was
used in its `aa_method` field; rows must read `spectrum`.

---

## Uncertainty budget

### Combination

The uncertainty on the concentration $C_A$ combines three independent
contributions [@diallo2025iba, Eq. 3]:

$$
\Delta C_A = \sqrt{(\Delta_{Q\Omega})^2 + (\Delta_{\sigma_A})^2 + (\Delta_{A_A})^2} \tag{D3}
$$

All three terms are **relative** uncertainties (dimensionless fractions).
$\Delta_{Q\Omega}$ and $\Delta_{\sigma_A}$ are constant across all elements and
all layers of a given measurement; only $\Delta_{A_A}$ varies, through the
counting statistics of each element.

**Program convention.** Flavunato reports each term twice: as the relative
quantity above, and as an *absolute* quantity scaled by the concentration,
$\Delta C_A^{\text{abs}} = C_A \cdot \Delta C_A$. The absolute form is the
uncertainty on the concentration expressed in the same units as the
concentration itself (percentage points of atomic fraction); the relative form
is the one to quote when comparing elements. Exported column names carry the
suffix `_rel_percent` or `_percent` respectively.

### Charge and solid angle, $\Delta_{Q\Omega}$

$\Delta_{Q\Omega}$ covers the combined uncertainty on the analysis charge and
the detector solid angle. Following [@diallo2025iba], it is estimated as the
standard deviation of the set of ratios between the simulated
Particle$\cdot$sr values and the corresponding raw (measured) Particle$\cdot$sr
values obtained during normalisation. The estimate is valid for samples
originating from the same analysis session, and is a property of the
experimental setup rather than of any element.

**Program choice.** $\Delta_{Q\Omega}$ is a user input, expressed in percent
(default 3 %). It is *not* derived from the `.xnra` file: the program does not
compute the ratio statistics above, which must be formed by the analyst across
the session's samples and entered manually. The spectrum-plotting module does
read the beam fluence and the detector solid angle from the file — converting
millisteradians to steradians where the unit attribute requires it — and
displays their product as Particle$\cdot$sr, which is the quantity entering the
ratios; but this value is used for display only and never feeds the
uncertainty calculation.

### Counting statistics, $\Delta_{A_A}$

The statistical contribution is Poissonian [@diallo2025iba, Eq. 4]:

$$
\Delta_{A_A} = \frac{\sqrt{A_A}}{A_A} = \frac{1}{\sqrt{A_A}} \tag{D4}
$$

**Program choice.** When $A_A = 0$ the term is undefined and is set to
"not a number"; the combination of Eq. (D3) then proceeds over the two remaining
terms only. See *Assumptions and limitations* for why this case requires
attention.

### Cross sections, $\Delta_{\sigma_A}$

$\Delta_{\sigma_A}$ depends on the nuclear reaction, not on the element as
such. The note gives four values [@diallo2025iba]:

| Reaction | $\Delta_{\sigma_A}$ | Source |
|---|---|---|
| $\mathrm{M}x(\alpha,\alpha)\mathrm{M}x$ | 0 % | Diallo 2025; reading it as Rutherford is this program's |
| $^{16}\mathrm{O}(d,\alpha_0)^{14}\mathrm{N}$ | 2 % | Diallo 2025 |
| $^{1}\mathrm{H}(^{4}\mathrm{He},{}^{1}\mathrm{H})^{4}\mathrm{He}$ | 2 % | Diallo 2025 |
| $^{12}\mathrm{C}(d,p_0)^{13}\mathrm{C}$ | 5 % | Diallo 2025 |

**Program additions.** The following are *not* in the cited note. They were
added to the program's default table and their provenance is not recorded in
the source; they must be justified independently before being relied upon.

| Reaction | $\Delta_{\sigma_A}$ | Status |
|---|---|---|
| $^{15}\mathrm{N}(p,\alpha\gamma)^{12}\mathrm{C}$ | 3 % | program addition, provenance unverified |
| $^{2}\mathrm{H}(^{4}\mathrm{He},{}^{2}\mathrm{H})^{4}\mathrm{He}$ | 3 % | program addition, provenance unverified |

**Program addition — isotope defaults.** For isotope-resolved work the program
carries a per-isotope default table, each entry mapped to one of the reactions
above:

| Species | Default $\Delta_{\sigma_A}$ | Basis |
|---|---|---|
| H, $^{1}$H | 2 % | Diallo 2025 |
| $^{2}$H | 3 % | program addition, unverified |
| C, $^{12}$C | 5 % | Diallo 2025 |
| $^{13}$C | 5 % | program addition, unverified |
| N, $^{14}$N, $^{15}$N | 3 % | program addition, unverified |
| O, $^{16}$O | 2 % | Diallo 2025 |
| $^{17}$O, $^{18}$O | 2 % | program addition, unverified |
| other isotopes of H, C, N, O | element value | via element key |
| any other element | 0 % (Rutherford) | Diallo 2025 for $\mathrm{M}x(\alpha,\alpha)\mathrm{M}x$; limiting it to Rutherford (typically heavy) targets is this program's reading |

$^{13}$C, $^{17}$O and $^{18}$O reuse the value of the main isotope, although
they are usually measured through different reactions; these values have no
basis in the cited note.

Lookup proceeds from a user-supplied override, to the exact isotope key, to the
element key obtained by stripping the mass number, and finally to the 0 %
Rutherford fallback.

All stable isotopes of H, C, N and O — $^{1}$H, $^{2}$H, $^{12}$C,
$^{13}$C, $^{14}$N, $^{15}$N, $^{16}$O, $^{17}$O, $^{18}$O — are listed
explicitly, so the element-key step is reached only by a non-stable entry such
as $^{3}$H or $^{14}$C, or by a mistyped name. Such an entry silently takes the
element's value **and its reaction label**: $^{3}$H is reported with
$\sigma = 2\,\%$ and the reaction $^{1}$H($^{4}$He,$^{1}$H)$^{4}$He, $^{14}$C
with $\sigma = 5\,\%$ and $^{12}$C(d,p$_0$)$^{13}$C.

The 0 % fallback is reached only when the base element is absent from the table
altogether. The cited note gives 0 % for the reaction
$\mathrm{M}x(\alpha,\alpha)\mathrm{M}x$; treating absence from the table as
equivalent to "measured by Rutherford scattering" is this program's reading,
not a statement of the note. The fallback therefore applies to any unlisted
species regardless of how it was actually measured: $^{7}$Li, for example,
silently receives a 0 % cross-section uncertainty even when its cross section
is not Rutherford.

**The global cross-section input is not consulted in isotope mode.** For an ROI
entry carrying a mass number, the value comes only from the table above or from
an explicit per-isotope override; the single cross-section field that applies
to element-mode entries is ignored. This is a known limitation of the current
version.

---

## Fit quality

### Reduced chi-squared

Agreement between simulated and experimental spectra is quantified by
[@diallo2025iba, Eq. 5]

$$
\chi^2_\nu = \frac{1}{\nu} \sum_{i=1}^{N} \frac{\left(y_i^{\exp} - y_i^{\mathrm{sim}}\right)^2}{\sigma_i^2} \tag{D5}
$$

with $\nu = N - p$ degrees of freedom, $N$ the number of channels in the ROI
and $p$ the number of fitted parameters.

**Program choices.** Two quantities the note leaves open are fixed as follows.

- $p = 1$, so $\nu = N - 1$.
- $\sigma_i = \sqrt{\max\left(y_i^{\exp},\, 4\right)}$. The Poisson uncertainty
  $\sqrt{y^{\exp}}$ is floored at 4 counts to avoid division by zero in empty
  channels. The floor suppresses the contribution of near-empty channels
  rather than letting them dominate; it has no effect in channels with at
  least 4 counts.

### Interpretation

**Program choice.** The following thresholds are used to label fit quality in
the interface and in exported results. They are a reporting convenience of the
program and carry no statistical authority.

| Range | Label |
|---|---|
| $0.90 \le \chi^2_\nu \le 1.10$ | Perfect |
| $1.10 < \chi^2_\nu \le 3.0$ | Great |
| $3.0 < \chi^2_\nu \le 10.0$ | Not OK |
| $\chi^2_\nu > 10.0$ | Very bad |
| $\chi^2_\nu < 0.90$ | Too low |

A value below 0.90 is flagged because it generally indicates overestimated
uncertainties or an over-parameterised fit, not a better result.

### AUC ratio

**Program addition.** Alongside $\chi^2_\nu$ the program computes a
normalisation check, the ratio of integrated areas over the ROI:

$$
\mathrm{AUC} = \frac{\sum_{i \in \text{ROI}} y_i^{\mathrm{sim}}}{\sum_{i \in \text{ROI}} y_i^{\exp}}
$$

A value near unity indicates that simulated and measured yields are correctly
normalised, independently of whether the *shape* agrees. This quantity does
not appear in the cited note.

---

## Adjusted uncertainty

When $\chi^2_\nu > 1$, the fit residuals exceed what counting statistics alone
predict, which may indicate underestimated uncertainties or unmodelled
systematic effects. In that case the statistical term may be rescaled by
$\sqrt{\chi^2_\nu}$, giving [@diallo2025iba, Eq. 6]

$$
\Delta C_A^{\mathrm{adj}} = \sqrt{(\Delta_{Q\Omega})^2 + (\Delta_{\sigma_A})^2 + \left(\sqrt{\chi^2_\nu}\, \Delta_{A_A}\right)^2} \tag{D6}
$$

The note is explicit that the reduced chi-squared is *not* an independent
contribution to the uncertainty budget — it is a goodness-of-fit indicator,
not a physical source of uncertainty — and that the correction applies only
when $\chi^2_\nu$ significantly exceeds unity. Otherwise the standard
expression of Eq. (D3) is used.

**Program implementation.** The rescaling factor is computed as
$\sqrt{\max\left(\chi^2_\nu,\, 1\right)}$, clamped at unity so that a fit with
$\chi^2_\nu < 1$ can never *reduce* the reported uncertainty. The adjustment is
applied only when the analyst selects it; **the default is no adjustment**, so
that quoted uncertainties follow Eq. (D3) unless stated otherwise. The program
also computes and exports the adjusted values unconditionally, in columns
suffixed `_chi2_adjusted_percent`, so that both can be compared without
recomputation.

The program does not decide what counts as "significantly exceeds unity"; that
judgement remains with the analyst, informed by the thresholds in
*Interpretation*.

**Program addition — AUC adjustment.** A third option rescales the statistical
term by $\max\left(\mathrm{AUC},\, 1/\mathrm{AUC}\right)$ instead. This
penalises normalisation mismatch in either direction. It is an addition of the
program and has no basis in the cited note; it is reported for comparison only.

---

## Depth profiles

A depth profile tabulates, layer by layer, the concentration of each element
and its uncertainty.

**Program choice.** When an element has been quantified in more than one ROI
within the same layer, the program reports the row with the **lowest**
$\chi^2_\nu$, on the reasoning that the best-fitting region gives the most
reliable determination. Each profile row carries the layer number, the layer
thickness in $10^{15}\ \text{atoms/cm}^2$, and per element the concentration
(in atomic percent, 2 decimals) with its uncertainty (3 decimals) taken from
the column matching the selected adjustment method.

This selection is applied regardless of whether a $\chi^2$ adjustment was
chosen for the uncertainty itself; $\chi^2_\nu$ therefore influences the
reported profile even under the default setting.

---

## Assumptions and limitations

The following constrain the interpretation of the results and should be stated
alongside any quoted uncertainty.

**Single $\Delta_{Q\Omega}$ and $\Delta_{\sigma_A}$ per run.** The interface
accepts one value of each, applied to every element and layer. This matches
the formalism, in which both are constant for a measurement, but means that a
sample requiring different cross-section uncertainties per element (for
instance RBS for a heavy element and NRA for a light one in the same spectrum)
must be processed in more than one run, or through the isotope-resolved path.

**The statistical term is an ROI quantity, not a per-layer one.** $A_A$ is
integrated over the ROI across the whole depth sampled by that ROI. The same
$A_A$, and hence the same $\Delta_{A_A}$, is therefore applied to every layer
in which the element appears. The layer-to-layer variation in the reported
absolute uncertainty comes only from the concentration scaling described in
*Combination*, not from layer-resolved counting statistics. Depth-resolved
counting uncertainties are outside the scope of this formalism.

**Background and peak overlap are not included.** Eq. (D3) combines charge,
cross-section and counting terms only. No variance is attributed to background
subtraction, to overlap between the partial spectra of different elements
within an ROI, or to the layer model itself (number of layers, thickness
assignment). Where ROIs overlap — a common situation for adjacent heavy
elements — the resulting correlation is not propagated. Quoted uncertainties
are therefore lower bounds on the total uncertainty.

**The ROI end channel is treated inconsistently.** $A_A$ includes the final
channel of the ROI, whereas the $\chi^2_\nu$ summation excludes it. The two
quantities in a given result row thus describe windows differing by one
channel. The effect on $\chi^2_\nu$ is of order 0.1–1 % for the ROI widths used
here. The behaviour is retained deliberately, since the results reported in
this work were produced with it; it is recorded as a known issue and is a
candidate for correction in a future version.

**A missing element name yields $A_A = 0$ without warning.** If an element
named in an ROI is absent from the element-spectrum export — for example
through a naming difference between the layer model and the export — the
lookup returns zero counts silently. The statistical term then becomes
undefined and is dropped from Eq. (D3), so the reported uncertainty collapses to
$\sqrt{(\Delta_{Q\Omega})^2 + (\Delta_{\sigma_A})^2}$. Because this is
*smaller* and visually cleaner than a correct value, the failure is easy to
miss. The diagnostic is the exported `element_counts` column, which reads 0 for
any affected row; it should be checked before results are used.

**$\chi^2_\nu$ is restricted to the simulated channel range.** An ROI extending
beyond the last simulated channel is silently truncated to that range, and one
lying entirely beyond it returns an undefined $\chi^2_\nu$. In practice no
useful ROI lies there, since the simulation carries no signal beyond its own
range.

---

## Validation

Two independent checks are maintained.

**Agreement with the manual calculation.** The program's implementation of
Eq. (D3) is compared against a manual spreadsheet calculation by the author
of the method, independent of the code [@diallo2025iba]. Supplied
with the same detected counts and the same $\Delta_{Q\Omega}$ and
$\Delta_{\sigma_A}$ per element, the program reproduces the manual relative and
absolute uncertainties for every layer and element to within $10^{-9}$; the
largest observed deviation is at the level of floating-point rounding
($\sim 10^{-18}$). This validates the uncertainty formula and its combination,
independently of how $A_A$ is obtained.

The counts themselves are *not* expected to agree: the manual calculation used
measured counts, whereas the program integrates the simulated partial spectrum
(see *Spectrum method*). The two are different estimators of $A_A$, so that
comparison is reported as a diagnostic and never as a pass/fail criterion.

**Regression against the thesis version.** A regression test compares the
current program output with the tagged thesis version (`v1.0-thesis`) at an
absolute tolerance of $10^{-12}$ on every numeric field; all later code changes
reproduce it exactly.

<!-- repo-only:start -->

The test requires the measurement data, which is not distributed with the
source; without it the test reports a skip rather than a pass.

---

## References

- `diallo2025iba` — the uncertainty formalism, Eqs. (D1)–(D6).
- `mayer1999simnra` — the simulation program producing the fitted models.

Entries are defined in `docs/latex/flavunato.bib`.

<!-- repo-only:end -->
