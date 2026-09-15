# Flavunato (XNRA)
Python/Tkinter GUI for SIMNRA .xnra IBA spectra and concentration uncertainties.
Thesis version is tagged v1.0-thesis. It is the reference; never alter its behaviour.

## Modules
- `xnra_gui_v18.py` — Tkinter GUI. **Entry point**: `python xnra_gui_v18.py`.
- `xnra_main_v6.py` — .xnra XML parsing and spectrum plotting. Library only.
- `xnra_uncertainty_v12.py` — uncertainties, chi-squared, depth profiles. Also a CLI.
- `xnra_element_spectra_v1.py` — SIMNRA element-spectrum .txt parsing/plotting. Also a CLI.

Imports: GUI → the other three; uncertainty → element_spectra. The `xnra_`
prefix is load-bearing — imports reference these module names, and the GUI
swallows ImportError, so a rename silently disables features instead of failing.

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
