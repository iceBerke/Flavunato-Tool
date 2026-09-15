"""Generate the golden reference file.

Reproduces the GUI's uncertainty path headlessly (no Tkinter). The loop below
mirrors xnra_gui_v18.py:1537-1602, which itself only orchestrates calls into
xnra_uncertainty_v12 / xnra_element_spectra_v1 -- the GUI does no maths of its
own, so calling those functions directly is faithful.

One deliberate difference: the GUI holds a SINGLE Q.Omega and a SINGLE sigma
for every element (xnra_gui_v18.py:857,883 read once at :1525-1526), so it
cannot express the per-element table this sample needs. We therefore supply
each element's own pair from rois.json. Everything else matches the GUI.

Output: tests/golden/reference.json (gitignored -- derived from local data).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import _paths  # noqa: E402

_paths.add_repo_to_path()

from xnra_element_spectra_v1 import (  # noqa: E402
    calculate_element_counts_from_spectrum,
    parse_element_spectrum,
)
from xnra_uncertainty_v12 import (  # noqa: E402
    calculate_chi_squared_for_roi,
    calculate_uncertainty_v9,
    interpret_chi2,
    parse_xnra_full,
)

SCHEMA = 1


def plain(value):
    """Cast numpy scalars to built-in types so json can serialise them."""
    if hasattr(value, "item"):
        return value.item()
    return value


def build():
    cfg = _paths.load_rois()
    data = parse_xnra_full(str(_paths.XNRA))
    spectrum = parse_element_spectrum(str(_paths.METADATA))

    isotope_mode = cfg["isotope_mode"]
    adj = cfg["adjustment_method"]
    wanted_layers = set(cfg["layers"])

    rows = []
    for entry in cfg["elements"]:
        element = entry["element"]
        roi_start, roi_end = entry["channels"]
        qomega = entry["qomega_percent"] / 100.0
        xsec = entry["xsec_percent"] / 100.0

        # GUI :1542-1552
        if data["raw_counts"] is not None and data["simulated_counts"] is not None:
            chi2_r, dof, roi_counts, auc_ratio = calculate_chi_squared_for_roi(
                data["raw_counts"], data["simulated_counts"], roi_start, roi_end
            )
            chi2_symbol, chi2_status = interpret_chi2(chi2_r)
        else:
            chi2_r, dof, roi_counts, auc_ratio = float("nan"), 0, 0, float("nan")
            chi2_symbol, chi2_status = "?", "N/A"

        # GUI :1555-1602
        for layer in data["layers"]:
            if layer["layer_num"] not in wanted_layers:
                continue

            concentration = layer["concentrations"].get(element, 0)
            if concentration <= 0:
                continue

            element_counts, element_fraction, total_exp = (
                calculate_element_counts_from_spectrum(
                    spectrum,
                    data["raw_counts"],
                    element,
                    roi_start,
                    roi_end,
                    use_isotope=isotope_mode,
                )
            )

            unc = calculate_uncertainty_v9(
                concentration,
                element_counts,
                qomega,
                xsec,
                chi2_reduced=chi2_r,
                auc_ratio=auc_ratio,
                adjustment_method=adj,
            )

            row = {
                "roi_name": entry["roi_name"],
                "element": element,
                "layer": layer["layer_num"],
                "roi_start": roi_start,
                "roi_end": roi_end,
                "thickness": plain(layer["thickness"]),
                "concentration": plain(concentration),
                "element_counts": plain(element_counts),
                "element_fraction": plain(element_fraction),
                "total_exp_counts": plain(total_exp),
                "roi_counts": plain(roi_counts),
                "chi2_reduced": plain(chi2_r),
                "chi2_dof": plain(dof),
                "chi2_symbol": chi2_symbol,
                "chi2_status": chi2_status,
                "auc_ratio": plain(auc_ratio),
                "qomega_input": qomega,
                "xsec_input": xsec,
            }
            for key, value in unc.items():
                row[f"unc.{key}"] = plain(value)
            rows.append(row)

    return {
        "schema": SCHEMA,
        "roi_source": cfg.get("roi_source"),
        "roi_comment": cfg.get("_comment"),
        "isotope_mode": isotope_mode,
        "adjustment_method": adj,
        "xnra": _paths.XNRA.name,
        "metadata": _paths.METADATA.name,
        "n_rows": len(rows),
        "rows": rows,
    }


def main():
    _paths.require(_paths.XNRA, _paths.METADATA, _paths.ROIS_JSON)
    ref = build()
    _paths.REFERENCE_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(_paths.REFERENCE_JSON, "w", encoding="utf-8") as fh:
        json.dump(ref, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(f"\nWrote {_paths.REFERENCE_JSON.relative_to(_paths.REPO)}  ({ref['n_rows']} rows)")
    print(f"{'ROI':<5} {'El':<3} {'Layer':>5} {'Conc':>8} {'A_A':>12} {'tot_rel %':>10}")
    print("-" * 50)
    for row in ref["rows"]:
        print(
            f"{row['roi_name']:<5} {row['element']:<3} {row['layer']:>5} "
            f"{row['concentration']:>8.4f} {row['element_counts']:>12d} "
            f"{row['unc.sigma_total_rel'] * 100:>10.6f}"
        )


if __name__ == "__main__":
    main()
