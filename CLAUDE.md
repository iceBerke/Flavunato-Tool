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
1. VERIFY BEFORE ACTING. Statements in prompts may be wrong; rule 19
   governs how to check them.
2. PLAN FIRST. Present the work as a numbered plan; rule 9 governs the
   approval it needs.
3. NO CALCULATION-LOGIC CHANGES. Documentation and restructuring only;
   code removal or refactoring needs explicit scope and must keep the
   golden test passing. If a calculation change seems needed, stop and
   ask.
4. ONE STEP AT A TIME. After each step: run `python -m py_compile` on all
   modules and show `git diff --stat`.
5. NO GUESSING. If unsure, ask. Mark anything unverified as "UNVERIFIED".
6. Use `git mv` for renames. Never delete files without approval.
7. Keep comments concise.
8. Commit messages follow the 50/72 rule: subject line max 50 chars,
   imperative mood, no trailing period; blank line; body wrapped at 72
   chars explaining what and why. Every commit ends with the default
   Co-Authored-By trailer, separated from the body by a blank line.
   Trailers are exempt from the 72-char wrap and must never be wrapped.
9. ANNOUNCE BEFORE ACTING, AND WAIT. For any task that changes files,
   first report the exact file list, what each change is, and why. Then
   stop and wait for approval before writing anything. This covers files
   outside the repo and throwaway test files in temp directories — if you
   would create it, name it first. If the prompt itself fixes the file
   list and says to proceed, that is the approval; do not ask twice.
10. SCOPE IS A CEILING, not a suggestion. If a task says "investigate, do
    not implement", building a prototype to test an idea is implementing.
    If you believe the task needs something outside its stated scope, say
    so and stop. Never do it and disclose it afterwards.
11. Never commit or push until Berke has reviewed the summary and the diff
    and said to proceed. No exceptions.
12. Every task writes its artifacts to `reviews/` at the repository root,
    never to a temp or scratch directory:
    `reviews/YYYY-MM-DD_HHMM_<slug>_report.md`, and for change tasks
    `reviews/YYYY-MM-DD_HHMM_<slug>.diff`. Copy both to
    `reviews/latest_report.md` and `reviews/latest.diff`, and report the
    absolute path in the reply. Tasks with no diff write the report anyway.
    A read-only task's report stands alone. A commit task's report records
    at minimum the commit hash, the staged file list, and the measured
    subject and longest body line; it names the diff file from the change
    task that produced the change rather than writing a new one, since
    post-commit `git diff` is empty and a regenerated diff would mislead.
    It says nothing about pushing — the push is a separate task with its
    own report. A push task's report records the commits pushed with their
    hashes and subjects, the remote and branch, the exit code, and that
    `git log origin/<branch>..HEAD` is empty afterwards.
13. The diff must include new files: run `git add -N <new paths>` before
    `git diff`, or the new file is missing from what Berke reviews.
14. Do not state a path, file or fact as verified unless you ran a command
    that checked it. Mark anything else "UNCLEAR" or "UNVERIFIED".
15. THE DIFF IS THE CLAIM. Every change, addition or deletion described in
    the summary must be visible in the diff written to `reviews/`. Before
    reporting, re-read that file and check the summary against it. If
    something you did is not in the diff, say so explicitly and explain
    why.
16. ACCOUNT FOR DELETIONS. State the insertion and deletion counts and what
    every deleted line was. A deletion you did not mention is the most
    expensive kind of error here.
17. Never describe a file's state from memory of what you wrote. Read it
    back from disk, or from the diff, before making a claim about it.
    Distinguish "I wrote X" from "X is on disk" — only the second is
    verified.
18. CITE, DON'T ASSERT. Any claim about program behaviour in a document or
    summary carries a file:line reference, verified against the code at the
    time of writing. Stale citations had to be corrected en masse after the
    CLI was removed.
19. CHECK THE PROMPT ITSELF. A task from Berke can contain a wrong path, a
    stale file:line, a claim about the code that is no longer true, or an
    instruction to write something you cannot verify. Check every premise
    against the actual code before acting on it. If a premise is wrong, or
    the task asks you to assert something unverified, stop and say so
    rather than complying. Doing this is never a failure to follow
    instructions.
