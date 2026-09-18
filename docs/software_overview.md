# Software overview

## Purpose and scope

Flavunato is a desktop application that turns a converged SIMNRA fit into
concentration uncertainties. For each element assigned to a region of interest,
in each selected layer, it reports a concentration with the combined
uncertainty from the charge–solid-angle product, the reaction cross section and
the counting statistics. It does **not** fit spectra: the layer model and
simulated spectrum are taken as given from SIMNRA [@mayer1999simnra], and
Flavunato propagates uncertainties onto the fitted concentrations.

## Inputs

Two files describe a measurement. The `.xnra` file, an XML document in the IDF
schema with SIMNRA extensions, supplies the fitted layer model — thicknesses
and concentrations — with the measured and simulated spectra and the energy
calibration. The element-spectrum export, a tab-separated text file from
SIMNRA, supplies the per-element and per-isotope partial spectra, read rather
than recomputed: they show how the simulated total decomposes by element. It is
technically optional: without it the counts are estimated from the region's
total counts and the concentration, which can be badly wrong, so it should
always be supplied; each result records which estimate was used.

The analyst supplies the regions of interest, the charge–solid-angle and
cross-section uncertainties, and the choice of adjustment. Results are given
per element. An isotope-resolved path is implemented but cannot be switched on
in this version.

## Implemented calculations

The uncertainty formalism follows the internal technical note of Diallo
[@diallo2025iba]. Its first two equations, for the detected-count relation and
the areal density, are background only: concentrations come from the SIMNRA
fit, so Flavunato does not evaluate them. The other four — the combined
uncertainty, the Poisson statistical term, the reduced chi-squared and its
adjusted uncertainty — are implemented.

Rescaling the statistical term by the reduced chi-squared is optional and off
by default: quoted uncertainties follow the standard combination unless the
analyst selects it. A third option rescales instead by the ratio of simulated
to measured counts over the region, taken in whichever direction exceeds unity
— an addition of this program, not in the cited method. Whichever is chosen,
the export lists the standard value and both rescaled ones. The
isotope-resolved path carries a built-in table of per-isotope default
cross-section uncertainties, partly from the cited note; because that path is
unreachable, every result uses the single cross-section value the analyst
supplies.

Definitions, assumptions and limitations are in the methodology section.

## Interface and outputs

The graphical interface is a tabbed window, with the `.xnra` selected in a file
bar above the tabs. One tab loads the element-spectrum export, another gathers
the uncertainty inputs and regions of interest; the rest control the plot. One
plot overlays the measured, smoothed and simulated spectra; a second shows the
individual element and isotope contributions, optionally with those spectra.
Both use a channel or energy axis with adjustable limits.

Results export as a spreadsheet or delimited text. For each region, layer and
element it gives the concentration, the uncertainty components and their total,
the counts used, the fit-quality indicators and the input parameters, so a
result traces back to its settings. A depth-profile export tabulates
concentration and uncertainty layer by layer; the spreadsheet form also carries
the raw results and parameters. Figures are saved as PNG or PDF.

## Implementation and validation

Flavunato is written in Python with NumPy, Matplotlib, pandas and openpyxl, and
uses Tkinter, bundled with Python. It was developed and used on Windows with
Python 3.14; Linux and macOS are untested.

Two checks are maintained. The first compares the standard combined
uncertainty, without chi-squared rescaling, with a manual spreadsheet
calculation by the author of the method, independent of the code, using its own
counts; absolute differences stay below $10^{-9}$. The second reproduces every
recorded result of version 1.0.0 (git tag `v1.0-thesis`), including the
chi-squared quantities, with absolute differences below $10^{-12}$, showing
that later changes do not alter the results for the reference data.

Flavunato was developed by Berke Santos and Giuseppe Legrottaglie. Development
was assisted by Claude (Anthropic), an AI assistant, used for code drafting,
review and documentation. The authors verified the implementation against a
manual calculation by the author of the method and a regression test.

The software is available from the authors on request.
