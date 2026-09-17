# Flavunato (XNRA)
Python/Tkinter GUI for SIMNRA .xnra IBA spectra and concentration uncertainties.
Thesis version is tagged v1.0-thesis. It is the reference; never alter its behaviour.
Code version 1.0.0 corresponds to the git tag v1.0-thesis.

## Modules
The code is the `flavunato` package. The GUI is the only interface.
**Entry point**: `python -m flavunato` or `python run_flavunato.py`.

- `flavunato/gui.py` — Tkinter GUI. Holds `main()`.
- `flavunato/plotting.py` — .xnra XML parsing and spectrum plotting. Library only.
- `flavunato/uncertainty.py` — uncertainties, chi-squared, depth profiles. Library only.
- `flavunato/element_spectra.py` — SIMNRA element-spectrum .txt parsing/plotting.
  Library only.

Imports are relative: GUI → the other three; uncertainty → element_spectra.
The GUI swallows ImportError on all three, so a broken import silently
disables features instead of failing — check the `*_AVAILABLE` flags.

Dependencies in `requirements.txt`. On Linux tkinter needs `python3-tk`.

## Hard rules
1. VERIFY BEFORE ACTING. Statements in prompts may be wrong. Check every
   claim against the actual code first and report mismatches before doing anything.
2. PLAN FIRST. Present a numbered plan and wait for explicit "approved".
3. NO LOGIC CHANGES. Documentation and restructuring only. If a logic change
   seems needed, stop and ask.
4. ONE STEP AT A TIME. After each step: run `python -m py_compile` on all
   modules, show `git diff --stat`, and wait for approval before committing.
5. NO GUESSING. If unsure, ask. Mark anything unverified as "UNVERIFIED".
6. Use `git mv` for renames. Never delete files without approval.
7. Keep comments concise.
8. Commit messages follow the 50/72 rule: subject line max 50 chars,
   imperative mood, no trailing period; blank line; body wrapped at 72
   chars explaining what and why. Every commit ends with the default
   Co-Authored-By trailer, separated from the body by a blank line.
   Trailers are exempt from the 72-char wrap and must never be wrapped.
