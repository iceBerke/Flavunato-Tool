"""Regression check: rerun the program and compare with reference.json.

Exit 0 = PASS (or SKIP when data is absent), exit 1 = drift detected.
Tolerance 1e-12, applied as an absolute difference on every numeric field.
"""

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import _paths  # noqa: E402

from generate_golden import build  # noqa: E402

TOL = 1e-12


def key_of(row):
    return (row["roi_name"], row["element"], row["layer"])


def differs(a, b):
    """True when two recorded values disagree beyond TOL."""
    if isinstance(a, bool) or isinstance(b, bool):
        return a != b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if math.isnan(a) and math.isnan(b):
            return False
        if math.isnan(a) or math.isnan(b):
            return True
        return abs(a - b) > TOL
    return a != b


def main():
    _paths.require(
        _paths.XNRA, _paths.METADATA, _paths.ROIS_JSON, _paths.REFERENCE_JSON
    )

    with open(_paths.REFERENCE_JSON, encoding="utf-8") as fh:
        ref = json.load(fh)
    cur = build()

    problems = []

    if ref.get("schema") != cur["schema"]:
        problems.append(
            ("(file)", "schema", ref.get("schema"), cur["schema"], float("nan"))
        )
    if ref.get("roi_source") != cur["roi_source"]:
        problems.append(
            ("(file)", "roi_source", ref.get("roi_source"), cur["roi_source"], float("nan"))
        )

    ref_rows = {key_of(r): r for r in ref["rows"]}
    cur_rows = {key_of(r): r for r in cur["rows"]}

    for key in sorted(ref_rows.keys() - cur_rows.keys()):
        problems.append(("/".join(map(str, key)), "(row)", "present", "MISSING", float("nan")))
    for key in sorted(cur_rows.keys() - ref_rows.keys()):
        problems.append(("/".join(map(str, key)), "(row)", "absent", "NEW", float("nan")))

    for key in sorted(ref_rows.keys() & cur_rows.keys()):
        rrow, crow = ref_rows[key], cur_rows[key]
        for field in sorted(set(rrow) | set(crow)):
            rval, cval = rrow.get(field), crow.get(field)
            if differs(rval, cval):
                if isinstance(rval, (int, float)) and isinstance(cval, (int, float)):
                    delta = abs(rval - cval)
                else:
                    delta = float("nan")
                problems.append(("/".join(map(str, key)), field, rval, cval, delta))

    label = f"{cur['n_rows']} rows, tol {TOL:g}, roi_source={cur['roi_source']}"
    if not problems:
        print(f"PASS  golden regression: {label}")
        return 0

    print(f"FAIL  golden regression: {len(problems)} difference(s); {label}\n")
    print(f"{'ROW':<14} {'FIELD':<32} {'REFERENCE':>22} {'CURRENT':>22} {'DELTA':>12}")
    print("-" * 106)
    for row, field, rval, cval, delta in problems:
        rtxt = f"{rval!r}" if not isinstance(rval, float) else f"{rval:.17g}"
        ctxt = f"{cval!r}" if not isinstance(cval, float) else f"{cval:.17g}"
        dtxt = "-" if math.isnan(delta) else f"{delta:.3e}"
        print(f"{row:<14} {field:<32} {rtxt:>22} {ctxt:>22} {dtxt:>12}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
