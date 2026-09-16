# Installation

Flavunato is **not pip-installable**. There is no `setup.py` or
`pyproject.toml`; it runs from a clone of the repository.

## Python version

Tested on **Python 3.14.2**. No minimum version is declared anywhere in the
project, and none is claimed here — other versions may work, but they have not
been tried.

## Virtual environment (recommended)

**Windows**

```bat
git clone https://github.com/iceBerke/Flavunato-Tool.git
cd Flavunato-Tool
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Linux / macOS**

```bash
git clone https://github.com/iceBerke/Flavunato-Tool.git
cd Flavunato-Tool
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Dependencies

From `requirements.txt`:

| Package | Minimum | Used for |
|---|---|---|
| `numpy` | 1.24 | array maths throughout |
| `matplotlib` | 3.7 | all plotting |
| `pandas` | 1.5 | results tables, depth profiles |
| `openpyxl` | 3.1 | `.xlsx` export |

`openpyxl` is never imported directly — pandas requires it to write Excel
files. Without it, `.csv` export still works but `.xlsx` fails.

### tkinter

The GUI needs `tkinter`, which is part of the standard library but is packaged
separately on many Linux distributions:

```bash
sudo apt install python3-tk        # Debian/Ubuntu
sudo dnf install python3-tkinter   # Fedora
```

On Windows and macOS the official Python installers include it.

### Optional: mplcursors

```bash
pip install mplcursors
```

Adds hover tooltips on plotted curves. It is imported inside a `try` block, so
plots work normally without it.

## Launching the GUI

Either of:

```bash
python -m flavunato
python run_flavunato.py
```

Both start the same interface.

## Command-line interface

The two analysis modules also run as command-line tools, but **only through
`python -m`**:

```bash
python -m flavunato.uncertainty --help
python -m flavunato.element_spectra --help
```

Running the files directly (`python flavunato/uncertainty.py`) fails with
`ImportError: attempted relative import with no known parent package`, because
the modules import each other relatively.

## Windows console encoding

Both command-line tools set their output encoding to UTF-8 at start, so
symbols such as `Ω` print correctly on a `cp1252` console. If you use an older
Python without `sys.stdout.reconfigure`, or pipe the output through another
tool that re-encodes it, set the encoding yourself first:

```bat
set PYTHONIOENCODING=utf-8
```

```powershell
$env:PYTHONIOENCODING='utf-8'
```

See `notes/known_issues.md` item 5.
