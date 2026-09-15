"""Shared paths and skip-guard for the Flavunato test scripts.

The example data is local-only (see examples/README.md). Every script calls
require() first, which prints a clear message and exits 0 when data is absent,
so a clone without the data still passes.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "examples"
GOLDEN = REPO / "tests" / "golden"

# Exact on-disk names. Note the space after "AJU", U+00B0 DEGREE SIGN and
# U+00B5 MICRO SIGN -- these differ from the underscore-only spellings that
# appear in some notes.
XNRA = EXAMPLES / "RBS_AJU 16-4-400°C-200nm_C0911000_80µC.xnra"
METADATA = EXAMPLES / "RBS_AJU 16-4-400°C-200nm_C0911000_80µC-metadata.txt"
XLSX = EXAMPLES / "BD-Stoichiometry ZrOx_AJU_for test_2.xlsx"
XLSX_SHEET = "Stoichiometry ZrOx CV"

ROIS_JSON = GOLDEN / "rois.json"
REFERENCE_JSON = GOLDEN / "reference.json"


def _display(path):
    """Repo-relative name when possible, otherwise the path as given."""
    try:
        return Path(path).resolve().relative_to(REPO)
    except ValueError:
        return path


def require(*paths):
    """Exit 0 with a clear message if any required file is missing."""
    missing = [p for p in paths if not Path(p).exists()]
    if missing:
        print("SKIP: required file(s) not found:")
        for p in missing:
            print(f"  - {_display(p)}")
        print("\nExample data is local-only; see examples/README.md.")
        if REFERENCE_JSON in missing:
            print("Run tests/golden/generate_golden.py to create reference.json.")
        sys.exit(0)


def load_rois():
    """Load rois.json and warn loudly while the ROIs are still placeholders."""
    import json

    with open(ROIS_JSON, encoding="utf-8") as fh:
        cfg = json.load(fh)
    if cfg.get("roi_source") != "supervisor":
        print(f"!! ROI source is '{cfg.get('roi_source')}' -- {cfg.get('_comment', '')}")
    return cfg


def add_repo_to_path():
    """Make the xnra_* modules importable regardless of cwd."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
