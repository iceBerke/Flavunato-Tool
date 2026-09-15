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
(`xnra_element_spectra_v1.py:359`) and the other slicing by array index
(`xnra_element_spectra_v1.py:398-401`). There is no off-by-one.

## 2. raw_counts / simulated_counts length mismatch
**status: open, not investigated**

`parse_xnra_full` returns `raw_counts` with 4099 points but
`simulated_counts` with only 1139 (`xnra_uncertainty_v12.py:287,299`). Both
are passed to `calculate_chi_squared_for_roi`
(`xnra_uncertainty_v12.py:306`, called from `xnra_gui_v18.py:1543`).

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
| Warning string says `xnra_element_spectra`, import is `xnra_element_spectra_v1` | `xnra_gui_v18.py:44` |
| Warning string says `xnra_uncertainty_v9`, import is `xnra_uncertainty_v12` | `xnra_gui_v18.py:71` |
| `ELEMENT_SPECTRUM_AVAILABLE = False` set inside the *uncertainty* except block, clobbering the flag set at `:40` | `xnra_gui_v18.py:70` |
| `COLOR_NAMES` imported, never used | `xnra_uncertainty_v12.py:119` |
| `json` imported, never used | `xnra_gui_v18.py:17` |
| Window title and header say "v15" / "Version 15" in a file named `xnra_gui_v18.py` | `xnra_gui_v18.py:1,3,77` |
| `calculate_uncertainty_for_element` defined, called from nowhere | `xnra_uncertainty_v12.py:1077` |

## 4. The A_A definition, and the unknown supervisor ROIs
**status: resolved (documentation)**

`A_A = round(sum(sim_A[ROI]))` -- the integrated **simulated** counts in the
ROI (`xnra_element_spectra_v1.py:404`). Comments at
`xnra_element_spectra_v1.py:395,403` show it replaced an earlier
experiment-anchored definition before version control. The repo version is
confirmed as the thesis version. This explains part of the VALIDATION B
deltas, together with the unknown supervisor ROIs.

`tests/golden/rois.json` holds **placeholder** ROIs (each element's full
simulated support), not the supervisor's. His ROIs are not yet known.

Note that Zr's xlsx count (1 150 000) exceeds the element's entire simulated
integral (1 128 896.2, +1.84%), so it is unreachable at any ROI under the
current definition.
