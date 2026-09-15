# Example data (local only — never committed)

The regression and validation tests need the three files below. They are **not**
in the repository: they are real IBA measurement data. Obtain them from the
maintainer and place them in this directory unchanged, keeping the exact
filenames (note the spaces, `°` U+00B0 and `µ` U+00B5).

| File | Purpose |
|---|---|
| `RBS_AJU 16-4-400°C-200nm_C0911000_80µC.xnra` | SIMNRA spectrum + layer model |
| `RBS_AJU 16-4-400°C-200nm_C0911000_80µC-metadata.txt` | SIMNRA element-spectrum export |
| `BD-Stoichiometry ZrOx_AJU_for test_2.xlsx` | Manual reference, sheet `Stoichiometry ZrOx CV` |

Everything in this directory except this README is gitignored (`examples/*`
with `!examples/README.md`). `tests/golden/reference.json` is likewise
generated locally and ignored, since it is derived from this data.

Without these files the tests skip with a message and exit 0, so a clone
without the data still passes CI.
