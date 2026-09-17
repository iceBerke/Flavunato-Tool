# Flavunato

A Python/Tkinter desktop tool for ion beam analysis (IBA). Flavunato reads
SIMNRA `.xnra` files together with their element-spectrum exports and reports,
for every element in every layer of the fitted model, a concentration and its
uncertainty — combining the charge–solid-angle, cross-section and counting
contributions, with optional χ² or AUC rescaling. It also plots spectra and
exports results and depth profiles to Excel or CSV.

## Quick start

```bash
git clone https://github.com/iceBerke/Flavunato-Tool.git
cd Flavunato-Tool
pip install -r requirements.txt
python -m flavunato
```

A virtual environment is recommended — see [Installation](docs/installation.md).

## Documentation

- [Installation](docs/installation.md) — Python version, virtual environment, dependencies, launch commands.
- [User guide](docs/user_guide.md) — the GUI tab by tab, and a checklist to run before using results.
- [Methodology](docs/methodology.md) — the equations, the uncertainty budget, assumptions and limitations.
- [Tests](tests/README.md) — golden regression and validation against a manual calculation.
- [Known issues](docs/notes/known_issues.md) — open behaviours and their workarounds.

## Thesis version

The revision used for the thesis analysis is tagged `v1.0-thesis`; later
commits are verified against it by a regression test at a tolerance of 1e-12,
so the reported numbers are unchanged.

## Citation

The uncertainty formalism is from Diallo (2025), *IBA Uncertainties*, internal
technical note, CEMHTI-CNRS Orléans. The spectra are fitted in SIMNRA —
Mayer, M. (1999), AIP Conf. Proc. **475**, 541–544,
[doi:10.1063/1.59188](https://doi.org/10.1063/1.59188). BibTeX entries are in
[`docs/latex/flavunato.bib`](docs/latex/flavunato.bib).
