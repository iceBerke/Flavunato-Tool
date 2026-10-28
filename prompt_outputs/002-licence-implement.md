# 002 — licence — implement

Task: add the CeCILL-B v1.0 English LICENSE, a CITATION.cff, and README
Acknowledgements and License sections. Stops at the review gate:
nothing staged, nothing committed, nothing pushed. The intent-to-add
entries made for the diff are the only index change (section D6 in
chat; V11 below shows nothing staged before them).

No test suite was run: the tests need local-only data. py_compile was
run per rule 4 (V10).

## Errata

None for the 001 reports.

## Files touched

| Path | Change |
|---|---|
| `LICENSE` | new; byte copy of the downloaded text (V3) |
| `CITATION.cff` | new; the prompt's literal with REPO_URL substituted (V1) |
| `README.md` | 12 lines appended at the end; nothing else changed (V7) |
| `prompt_outputs/002-licence-implement.md` | new; this report |
| `prompt_outputs/002-licence.diff.txt` | new; the diff artifact |
| git index | intent-to-add for every untracked path in `git status`, by explicit path (see "Diff artifact") |
| `<scratchpad>/t002_*.py` | outside the repo: start, fetch, apply, verify, quote, diff and insert scripts |
| `<scratchpad>/Licence_CeCILL-B_V1-en.txt` | outside the repo: the download |
| `<scratchpad>/venv/` | outside the repo: the cffconvert environment |
| `<scratchpad>/out/`, `regen/`, `pycache/` | outside the repo, **not in the prompt's list**: see Deviations |

Approval: the prompt fixed the file list, which rule 9 counts as
approval.

## Premise checks (prompt vs files)

| Prompt premise | Finding |
|---|---|
| Start HEAD == origin/main == 32a4e6c…, carried reports at the given bytes/sha256 | Holds (S1–S3). |
| README is `README.md` | Holds (S4). |
| Licence URL `https://cecill.info/licences/Licence_CeCILL-B_V1-en.txt` | Holds: HTTP 200, no redirect, linked from the official page `https://cecill.info/licences.en.html` (L1, L2). |
| Origin URL `https://github.com/iceBerke/Flavunato-Tool` | Holds (V1). |
| `flavunato/uncertainty.py` exists | Holds (S4). |
| No licence or copyright section in the README | Holds: 0 hits at HEAD (V6). Sections added at the end. |
| "if Babacar Diallo is not already credited" | **Differs in part.** README.md:40 at HEAD already cites "Diallo (2025), *IBA Uncertainties*" as the source of the formalism (V5). He is not named in full or thanked there; the full name appears only in `docs/latex/flavunato.bib:6`. I read "credited" as a named acknowledgement and added the section. Point R5. |
| "Do not mention any internal note of his" | My added text does not. README.md:40, unchanged, already mentions the "internal technical note" (V5). Point R6. |
| py_compile: 11 files, 0 failures | Holds (V10). |
| `git add -N <every new untracked file>` | That includes the two carried 001 reports and, on the later runs, the artifact itself. All received intent-to-add; none was modified. |

## Changes

**1. LICENSE.** Downloaded by `t002_fetch.py`, copied byte for byte by
`t002_apply.py`; LICENSE and the download have the same sha256 (V3). No
encoding, line-ending or other change.

**2. CITATION.cff.** Every line matches the prompt literal; the whole
file is byte-identical to it with REPO_URL substituted; no BOM, no CR,
one final newline, no `version` or `date-released` (V1). cffconvert
2.0.0 validates it, exit 0 (V2).

**3. README.md.** Appended after the last section (`## Citation`), in
the file's own CRLF working-tree endings; git stores LF (`text=auto`).
The HEAD README is an unchanged prefix of the new one (V7). The added
lines, from V7:

```
+
+## Acknowledgements
+
+We thank Babacar Diallo for deriving the uncertainty formulas
+implemented in `flavunato/uncertainty.py`.
+
+## License
+
+Copyright (c) 2026 Berke Santos, Giuseppe Legrottaglie
+
+Flavunato is distributed under the CeCILL-B Free Software License
+Agreement, version 1.0. See [LICENSE](LICENSE) for the full text.
```

No existing text was replaced, so there is no replaced text to quote.

**4. Ignore check.** `git check-ignore -v -n` prints `::` (no pattern)
for LICENSE, LICENSE.fr and CITATION.cff: none is ignored (V4).

## POINTS TO SURFACE FOR YOUR RULING

**R1. LICENSE bytes.** No reason to change them. Valid UTF-8, no BOM,
LF only, no control characters (L4–L6). `text=auto` with
`core.autocrlf=true` stores the same blob as the raw bytes, so the
stored form's sha256 equals the download's (V3). For information: the
only non-ASCII is two `à` (`C3 A0`, lines 22 and 339; L4), and lines
20, 406 and 407 end in whitespace (V9), which `git diff --check` would
flag. With `core.autocrlf=true`, git warns that the working copies of
the new LF files get CRLF the next time it checks them out (D2, in
chat); the stored form stays LF. Recommendation: keep the official
bytes as they are.

**R2. LICENSE.fr.** The official French plain text exists at
`https://cecill.info/licences/Licence_CeCILL-B_V1-fr.txt` (HTTP 200,
L7). Article 11.5 says both versions "are deemed authentic" (Q2). Not
created; your ruling.

**R3. Notice in each source file.** The text does not ask for one. No
article mentions source-file headers (Q1). The closest clauses bind a
licensee who redistributes: Article 5.3.1 ("accompanied by: 1. a copy
of the Agreement, 2. a notice relating to the limitation of both the
Licensor's warranty and liability") and Article 6.4 ("not to remove, or
modify, in any manner, the intellectual property notices attached to
the Software"). No headers added.

**R4. README placement and style.** Placement at the end, after
`## Citation`, looks right: the headings use the README's `##` style
(V6). Wrapping differs: HEAD prose lines reach 80 chars and 9 of 18 are
over 72, while the added lines are at most 65 (V7). Your text is kept
as given; rewrapping to the README's width is **proposed**, not done.

**R5. Is Babacar Diallo already credited?** See premise checks. Keep
the section, or drop it because README.md:40 already cites him.

**R6. Existing mentions of his internal note.** README.md:40 and the
docs (e.g. docs/methodology.md:6, docs/software_overview.md:32) already
call the source an "internal technical note" (V5). Unchanged, out of
scope; noted in case "do not mention" was meant more broadly.

**R7. Support for the acknowledgement sentence.** uncertainty.py:6
"implements the uncertainty formulas from the French IBA expert" and
cites `IBA-uncertainties-v3.pdf` (uncertainty.py:16, :312; V8). The
code never names Diallo; the link to him rests on README.md:40 and
docs/methodology.md:6–7. That he *derived* the formulas, rather than
compiled them, is UNVERIFIED from the repository.

**R8. Copyright line.** The year 2026 matches the history: first
commit 2026-09-15 (V12). Whether an employer also holds rights in the
code is a legal question this repository cannot answer: UNVERIFIED.

## Deviations

- The prompt allowed scripts, the download and one venv under
  `<scratchpad>`. I also created `<scratchpad>/out/` (saved script
  output, inserted below by `t002_insert.py`), `<scratchpad>/regen/`
  (the regeneration the cmp step needs) and `<scratchpad>/pycache/`
  (rule 4's bytecode). I did not name them before creating them. They
  are verification scratch only, outside the repository.
- `t002_fetch.py` also requested two cecill.info HTML pages and the
  French text, read in memory only and not saved.
- Saved output has its CRLF turned into LF when inserted here, so this
  report has no CR. The README's CRLF working-tree endings show up only
  as counts (V7, V9).

## UNREQUESTED — ACCEPT OR DROP

- A `__pycache__/` with 9 stale `.pyc` files sits in the repo root,
  ignored by `.gitignore:2`, dated 2026-09-15 to 2026-09-17 (Q3). Not
  created by this task. Removing it needs your approval (rule 6). Not
  done.

## Verification output

All blocks are script output inserted by `t002_insert.py`.

### Start state: `python t002_start.py`

```
=== S1. fetch, branch, HEAD, origin ===
git fetch exit 0: exit 0 -> PASS
branch is main: main -> PASS
HEAD == 32a4e6c...: 32a4e6ce9e79ec10e627ba0df8d84c5b9b2d2dc1 -> PASS
origin/main == 32a4e6c...: 32a4e6ce9e79ec10e627ba0df8d84c5b9b2d2dc1 -> PASS
behind/ahead: behind 0, ahead 0 -> PASS
  remote -v: origin	https://github.com/iceBerke/Flavunato-Tool.git (fetch)
  remote -v: origin	https://github.com/iceBerke/Flavunato-Tool.git (push)

=== S2. status --porcelain -uall ===
  ?? prompt_outputs/001-bootstrap-commit.md
  ?? prompt_outputs/001-bootstrap-push.md
only the 2 carried reports untracked: 2 line(s) -> PASS

=== S3. carried reports ===
prompt_outputs/001-bootstrap-commit.md working-tree bytes 9784 | CR bytes 0
  LF form: bytes 9784 (want 9784) sha256 b721740d228165f9f22e627c81a24a4036f0aac12efb25e4954663304653734d -> PASS
prompt_outputs/001-bootstrap-push.md working-tree bytes 5739 | CR bytes 0
  LF form: bytes 5739 (want 5739) sha256 5440ae87298fe16da6e2e9550f0d6b1d40759a112c580249a6de00abfec18c09 -> PASS

=== S4. paths named by the prompt ===
  tracked matches: README.md, flavunato/uncertainty.py
README.md is the tracked README: 1 -> PASS
flavunato/uncertainty.py tracked and on disk: True -> PASS
LICENSE absent before the change: absent -> PASS
LICENSE.fr absent before the change: absent -> PASS
CITATION.cff absent before the change: absent -> PASS
.zenodo.json absent before the change: absent -> PASS

RESULT: ALL PASS
```

### Download: `python t002_fetch.py <scratchpad>`

```
=== L1. Download ===
URL requested: https://cecill.info/licences/Licence_CeCILL-B_V1-en.txt
final URL after redirects: https://cecill.info/licences/Licence_CeCILL-B_V1-en.txt (host cecill.info)
HTTP status: 200
Content-Type: text/plain; charset=UTF-8 | Last-Modified: Thu, 26 Aug 2021 14:11:31 GMT
saved: <scratchpad>/Licence_CeCILL-B_V1-en.txt
bytes: 21396
sha256: 014e062e7d6b3b9e686bb8cb642479d6cc8bb775d8ee185908b669b8daaf5f2f

=== L2. Identity checks ===
title 'CeCILL-B FREE SOFTWARE LICENSE AGREEMENT': 1 match(es) -> PASS
'Version 1.0': 1 match(es) -> PASS
'CeCILL-B' count: 2 match(es) -> PASS
host is cecill.info: cecill.info -> PASS
official page https://cecill.info/licences.en.html: HTTP 200, links Licence_CeCILL-B_V1-en.txt: True
official page https://cecill.info/licences/Licence_CeCILL-B_V1-en.html: HTTP 200, links Licence_CeCILL-B_V1-en.txt: False

=== L3. First and last 3 lines (repr, line ending kept) ===
line count (splitlines): 515
  first 1: b'\n'
  first 2: b'CeCILL-B FREE SOFTWARE LICENSE AGREEMENT\n'
  first 3: b'\n'
  last L513: b'\n'
  last L514: b'\n'
  last L515: b'Version 1.0 dated 2006-09-05.\n'

=== L4. Encoding ===
valid UTF-8: yes
UTF-8 BOM: no
non-ASCII bytes: 4
  line 22 byte offset 776: 0xC3
  line 22 byte offset 777: 0xA0
  line 339 byte offset 13304: 0xC3
  line 339 byte offset 13305: 0xA0

=== L5. Line endings ===
CRLF: 0 | bare LF: 515 | bare CR: 0
ends with newline: True | last 4 bytes b'05.\n'

=== L6. Control characters other than TAB/CR/LF ===
count: 0
TAB count (allowed, for information): 0

=== L7. Official French plain text (probe only, not saved) ===
https://cecill.info/licences/Licence_CeCILL-B_V1-fr.txt: HTTP 200, final https://cecill.info/licences/Licence_CeCILL-B_V1-fr.txt, 22400 bytes, Content-Type text/plain; charset=UTF-8
```

### Apply: `python t002_apply.py <scratchpad>`

```
LICENSE written: 21396 bytes, sha256 014e062e7d6b3b9e686bb8cb642479d6cc8bb775d8ee185908b669b8daaf5f2f
REPO_URL -> https://github.com/iceBerke/Flavunato-Tool
CITATION.cff written: 950 bytes
README.md appended: 340 bytes (12 lines, CRLF)
```

### Checks: `python t002_verify.py <scratchpad>`

```
=== V1. CITATION.cff vs prompt literal ===
REPO_URL from origin (no credentials, no .git): https://github.com/iceBerke/Flavunato-Tool -> PASS
  L1   match    | cff-version: 1.2.0
  L2   match    | message: "If you use this software, please cite it as below....
  L3   match    | type: software
  L4   match    | title: "Flavunato: visualization and uncertainty analysis of...
  L5   match    | authors:
  L6   match    |   - family-names: Santos
  L7   match    |     given-names: Berke
  L8   match    |     affiliation: "Université d'Orléans, CNRS, CEMHTI UPR 307...
  L9   match    |     orcid: "https://orcid.org/0009-0007-7267-8178"
  L10  match    |   - family-names: Legrottaglie
  L11  match    |     given-names: Giuseppe
  L12  match    |     affiliation: "Institute of Materials for Electronics and...
  L13  match    |     orcid: "https://orcid.org/0009-0009-2686-6551"
  L14  match    | license: CECILL-B
  L15  match    | repository-code: "https://github.com/iceBerke/Flavunato-Tool...
  L16  match    | keywords:
  L17  match    |   - ion beam analysis
  L18  match    |   - SIMNRA
  L19  match    |   - NRA
  L20  match    |   - RBS
  L21  match    |   - ERDA
  L22  match    |   - uncertainty
  L23  match    | 
whole file byte-identical to literal: 950 vs 950 bytes -> PASS
BOM absent: no -> PASS
CR bytes: 0 -> PASS
ends with exactly one newline: b'y\n' -> PASS
no version / date-released field: [] -> PASS

=== V2. cffconvert --validate -i CITATION.cff (repo root) ===
cffconvert --version: 2.0.0 (exit 0)
  | Citation metadata are valid according to schema version 1.2.0.
cffconvert --validate exit 0: exit 0 -> PASS

=== V3. LICENSE: bytes, attributes, stored form ===
LICENSE sha256 014e062e7d6b3b9e686bb8cb642479d6cc8bb775d8ee185908b669b8daaf5f2f (21396 bytes)
download sha256 014e062e7d6b3b9e686bb8cb642479d6cc8bb775d8ee185908b669b8daaf5f2f (21396 bytes)
LICENSE byte-identical to download: 21396 vs 21396 -> PASS
  check-attr: LICENSE: text: auto
  check-attr: LICENSE: eol: unspecified
  check-attr: CITATION.cff: text: auto
  check-attr: CITATION.cff: eol: unspecified
  check-attr: README.md: text: auto
  check-attr: README.md: eol: unspecified
blob id with git's filters (stored form): da418978d4e89266df4fc6ea19c6424c879a9bd8
blob id of raw bytes (no filters):        da418978d4e89266df4fc6ea19c6424c879a9bd8
git stores LICENSE bytes unchanged: same blob -> PASS
sha256 stored form == sha256 downloaded: 014e062e7d6b3b9e686bb8cb642479d6cc8bb775d8ee185908b669b8daaf5f2f
core.autocrlf: true

=== V4. git check-ignore -v -n ===
  LICENSE: exit 1 | '::\tLICENSE' | pattern ''
  LICENSE not ignored: not ignored -> PASS
  LICENSE.fr: exit 1 | '::\tLICENSE.fr' | pattern ''
  LICENSE.fr not ignored: not ignored -> PASS
  CITATION.cff: exit 1 | '::\tCITATION.cff' | pattern ''
  CITATION.cff not ignored: not ignored -> PASS

=== V5. Babacar / Diallo in tracked files, pre-change state (HEAD) ===
-- git grep -n -i Babacar HEAD: exit 0, 1 hit(s)
  HEAD:docs/latex/flavunato.bib:6:  author  = {Diallo, Babacar},
-- git grep -n -i Diallo HEAD: exit 0, 51 hit(s)
  HEAD:README.md:40:The uncertainty formalism is from Diallo (2025), *IBA Uncertainties*, internal
  HEAD:docs/latex/flavunato.bib:5:@unpublished{diallo2025iba,
  HEAD:docs/latex/flavunato.bib:6:  author  = {Diallo, Babacar},
  HEAD:docs/latex/methodology.tex:6:The uncertainty formalism follows the internal technical note of Diallo
  HEAD:docs/latex/methodology.tex:7:\citep{diallo2025iba}, whose Eqs. (D1)--(D6) are reproduced below.
  HEAD:docs/latex/methodology.tex:52:1]{diallo2025iba}
  HEAD:docs/latex/methodology.tex:64:2]{diallo2025iba}
  HEAD:docs/latex/methodology.tex:140:contributions \citep[Eq. 3]{diallo2025iba}:
  HEAD:docs/latex/methodology.tex:165:charge and the detector solid angle. Following \citep{diallo2025iba}, it
  HEAD:docs/latex/methodology.tex:188:The statistical contribution is Poissonian \citep[Eq. 4]{diallo2025iba}:
  HEAD:docs/latex/methodology.tex:203:element as such. The note gives four values \citep{diallo2025iba}:
  HEAD:docs/latex/methodology.tex:222:\(\mathrm{M}x(\alpha,\alpha)\mathrm{M}x\) & 0 \% & Diallo 2025; reading
  HEAD:docs/latex/methodology.tex:224:\(^{16}\mathrm{O}(d,\alpha_0)^{14}\mathrm{N}\) & 2 \% & Diallo 2025 \\
  HEAD:docs/latex/methodology.tex:226:\% & Diallo 2025 \\
  HEAD:docs/latex/methodology.tex:227:\(^{12}\mathrm{C}(d,p_0)^{13}\mathrm{C}\) & 5 \% & Diallo 2025 \\
  HEAD:docs/latex/methodology.tex:283:H, \(^{1}\)H & 2 \% & Diallo 2025 \\
  HEAD:docs/latex/methodology.tex:285:C, \(^{12}\)C & 5 \% & Diallo 2025 \\
  HEAD:docs/latex/methodology.tex:288:O, \(^{16}\)O & 2 \% & Diallo 2025 \\
  HEAD:docs/latex/methodology.tex:291:any other element & 0 \% (Rutherford) & Diallo 2025 for
  HEAD:docs/latex/methodology.tex:336:\citep[Eq. 5]{diallo2025iba}
  HEAD:docs/latex/methodology.tex:405:\citep[Eq. 6]{diallo2025iba}
  HEAD:docs/latex/methodology.tex:523:\citep{diallo2025iba}. Supplied with the same detected counts and the
  HEAD:docs/latex/software_overview.tex:34:The uncertainty formalism follows the internal technical note of Diallo
  HEAD:docs/latex/software_overview.tex:35:\citep{diallo2025iba}. Its first two equations, for the detected-count
  HEAD:docs/methodology.md:7:Diallo [@diallo2025iba], whose Eqs. (D1)–(D6) are reproduced below. Everything that
  HEAD:docs/methodology.md:50:The number of counts detected for element $A$ is [@diallo2025iba, Eq. 1]
  HEAD:docs/methodology.md:62:[@diallo2025iba, Eq. 2]
  HEAD:docs/methodology.md:135:contributions [@diallo2025iba, Eq. 3]:
  HEAD:docs/methodology.md:157:the detector solid angle. Following [@diallo2025iba], it is estimated as the
  HEAD:docs/methodology.md:177:The statistical contribution is Poissonian [@diallo2025iba, Eq. 4]:
  HEAD:docs/methodology.md:191:such. The note gives four values [@diallo2025iba]:
  HEAD:docs/methodology.md:195:| $\mathrm{M}x(\alpha,\alpha)\mathrm{M}x$ | 0 % | Diallo 2025; reading it as Rutherford is this program's |
  HEAD:docs/methodology.md:196:| $^{16}\mathrm{O}(d,\alpha_0)^{14}\mathrm{N}$ | 2 % | Diallo 2025 |
  HEAD:docs/methodology.md:197:| $^{1}\mathrm{H}(^{4}\mathrm{He},{}^{1}\mathrm{H})^{4}\mathrm{He}$ | 2 % | Diallo 2025 |
  HEAD:docs/methodology.md:198:| $^{12}\mathrm{C}(d,p_0)^{13}\mathrm{C}$ | 5 % | Diallo 2025 |
  HEAD:docs/methodology.md:217:| H, $^{1}$H | 2 % | Diallo 2025 |
  HEAD:docs/methodology.md:219:| C, $^{12}$C | 5 % | Diallo 2025 |
  HEAD:docs/methodology.md:222:| O, $^{16}$O | 2 % | Diallo 2025 |
  HEAD:docs/methodology.md:225:| any other element | 0 % (Rutherford) | Diallo 2025 for $\mathrm{M}x(\alpha,\alpha)\mathrm{M}x$; limiting it to Rutherford (typically heavy) targets is this program's reading |
  HEAD:docs/methodology.md:265:[@diallo2025iba, Eq. 5]
  HEAD:docs/methodology.md:320:$\sqrt{\chi^2_\nu}$, giving [@diallo2025iba, Eq. 6]
  HEAD:docs/methodology.md:432:of the method, independent of the code [@diallo2025iba]. Supplied
  HEAD:docs/methodology.md:459:- `diallo2025iba` — the uncertainty formalism, Eqs. (D1)–(D6).
  HEAD:docs/references/README.md:6:- Diallo, B. (2025). *IBA Uncertainties*. Internal technical note,
  HEAD:docs/software_overview.md:32:The uncertainty formalism follows the internal technical note of Diallo
  HEAD:docs/software_overview.md:33:[@diallo2025iba]. Its first two equations, for the detected-count relation and
  HEAD:docs/user_guide.md:42:*How to estimate it.* Following Diallo (2025): take the ratios of the
  HEAD:prompt_outputs/001-bootstrap-implement.md:314:  f2c2259 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-17 Separate Diallo's 0 % rule from program reading
  HEAD:prompt_outputs/001-bootstrap-implement.md:317:  11328eb | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Tag Diallo equations and trim thesis export
  HEAD:prompt_outputs/001-bootstrap.diff.txt:2122:+  f2c2259 | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-17 Separate Diallo's 0 % rule from program reading
  HEAD:prompt_outputs/001-bootstrap.diff.txt:2125:+  11328eb | Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com> | 2026-09-16 Tag Diallo equations and trim thesis export
-- working tree, README.md only, after the change:
  README.md:40:The uncertainty formalism is from Diallo (2025), *IBA Uncertainties*, internal
  README.md:48:We thank Babacar Diallo for deriving the uncertainty formulas

=== V6. Licence/copyright section in README ===
HEAD:README.md: exit 1, 0 hit(s) []
working README.md: exit 0
  README.md:51:## License
  README.md:53:Copyright (c) 2026 Berke Santos, Giuseppe Legrottaglie
  README.md:55:Flavunato is distributed under the CeCILL-B Free Software License
  README.md:56:Agreement, version 1.0. See [LICENSE](LICENSE) for the full text.
Acknowledgements heading at HEAD: []
headings at HEAD: 1:# Flavunato | 12:## Quick start | 23:## Documentation | 32:## Thesis version | 38:## Citation

=== V7. README change and wrapping ===
numstat README.md: 12	0	README.md
  @@ -44,0 +45,12 @@ Mayer, M. (1999), AIP Conf. Proc. **475**, 541–544,
  +
  +## Acknowledgements
  +
  +We thank Babacar Diallo for deriving the uncertainty formulas
  +implemented in `flavunato/uncertainty.py`.
  +
  +## License
  +
  +Copyright (c) 2026 Berke Santos, Giuseppe Legrottaglie
  +
  +Flavunato is distributed under the CeCILL-B Free Software License
  +Agreement, version 1.0. See [LICENSE](LICENSE) for the full text.
HEAD README is a prefix of the new README (append only): 44 old lines, 56 new lines -> PASS
HEAD prose line lengths: max 80, lines > 72: 9 of 18
added line lengths: [0, 19, 0, 61, 42, 0, 10, 0, 54, 0, 65, 65] max 65
README working tree: CRLF 56, bare LF 0

=== V8. Support for the acknowledgement sentence (tracked files) ===
  flavunato/uncertainty.py:6:This version implements the uncertainty formulas from the French IBA expert,
  flavunato/uncertainty.py:16:THEORETICAL BACKGROUND (from IBA-uncertainties-v3.pdf)
  flavunato/uncertainty.py:97:Formulas from French IBA expert documentation (v3)
  flavunato/uncertainty.py:120:# CROSS-SECTION UNCERTAINTIES (from IBA-uncertainties-v3.pdf)
  flavunato/uncertainty.py:124:    # From IBA-uncertainties-v3.pdf (French IBA expert)
  flavunato/uncertainty.py:301:# UNCERTAINTY CALCULATIONS (v9 - French Expert Formulas + Isotope Support)
  flavunato/uncertainty.py:312:    Formula (Equation 5 from IBA-uncertainties-v3.pdf):
  flavunato/uncertainty.py:458:    Calculate uncertainties using the French expert's formulas (v9).
  README.md:40:The uncertainty formalism is from Diallo (2025), *IBA Uncertainties*, internal
  docs/methodology.md:6:The uncertainty formalism follows the internal technical note of

=== V9. Character scan ===
LICENSE: 21396 bytes | valid UTF-8 yes | BOM no | CR 0 | other control chars 0 []
  (information) lines with trailing whitespace: 3 [20, 406, 407]
CITATION.cff: 950 bytes | valid UTF-8 yes | BOM no | CR 0 | other control chars 0 []
  (information) lines with trailing whitespace: 0 []
README.md: 2399 bytes | valid UTF-8 yes | BOM no | CR 56 | other control chars 0 []
  (information) lines with trailing whitespace: 0 []

=== V10. py_compile on all tracked .py files (rule 4) ===
  exit 0 flavunato/__init__.py
  exit 0 flavunato/__main__.py
  exit 0 flavunato/element_spectra.py
  exit 0 flavunato/gui.py
  exit 0 flavunato/plotting.py
  exit 0 flavunato/uncertainty.py
  exit 0 run_flavunato.py
  exit 0 tests/_paths.py
  exit 0 tests/golden/check_golden.py
  exit 0 tests/golden/generate_golden.py
  exit 0 tests/validation/compare_manual.py
py_compile: 11 files, 0 failures; bytecode under <scratchpad>/pycache -> PASS

=== V11. Scope: files outside the list unchanged ===
tracked files changed vs HEAD == [README.md]: ['README.md'] -> PASS
nothing staged: [] -> PASS
git diff --stat:
   README.md | 12 ++++++++++++
   1 file changed, 12 insertions(+)

=== V12. Information: first and last commit dates ===
first commit: 2026-09-15 de8b7e1 | last: 2026-10-27 32a4e6c

RESULT: ALL PASS
```

### Licence passages: `python t002_quote.py`

```
=== Q1. LICENSE lines mentioning 'notice' or 'file' ===
  LICENSE:5:     Notice
  LICENSE:91: Object Code: means the binary files originating from the compilation of
  LICENSE:108: Module: means a set of sources files including their documentation that
  LICENSE:144: 3.2 One copy of the Agreement, containing a notice relating to the
  LICENSE:209: Software provided that it includes an explicit notice that it is the
  LICENSE:234:    2. a notice relating to the limitation of both the Licensor's
  LICENSE:267:       property notice for the Software,
  LICENSE:270:       intellectual property notice and license hereunder are included in
  LICENSE:276:       Software intellectual property notice,
  LICENSE:332:       notices attached to the Software;
  LICENSE:334:    2. to reproduce said notices, in an identical manner, in the copies
  LICENSE:436: thirty (30) days after notice has been sent to the Licensee and has

=== Q2. Passages ===
-- Article 5.3.1, LICENSE:226-235
  226:         5.3.1 DISTRIBUTION OF SOFTWARE WITHOUT MODIFICATION
  227: 
  228: The Licensee is authorized to distribute true copies of the Software in
  229: Source Code or Object Code form, provided that said distribution
  230: complies with all the provisions of the Agreement and is accompanied by:
  231: 
  232:    1. a copy of the Agreement,
  233: 
  234:    2. a notice relating to the limitation of both the Licensor's
  235:       warranty and liability as set forth in Articles 8 and 9,
-- Article 5.3.4, LICENSE:260-271
  260:         5.3.4 CREDITS
  261: 
  262: Any Licensee who may distribute a Modified Software hereby expressly
  263: agrees to:
  264: 
  265:    1. indicate in the related documentation that it is based on the
  266:       Software licensed hereunder, and reproduce the intellectual
  267:       property notice for the Software,
  268: 
  269:    2. ensure that written indications of the Software intended use,
  270:       intellectual property notice and license hereunder are included in
  271:       easily accessible format from the Modified Software interface,
-- Article 6.4, LICENSE:327-335
  327:       6.4 JOINT PROVISIONS
  328: 
  329: The Licensee expressly undertakes:
  330: 
  331:    1. not to remove, or modify, in any manner, the intellectual property
  332:       notices attached to the Software;
  333: 
  334:    2. to reproduce said notices, in an identical manner, in the copies
  335:       of the Software modified or not.
-- Article 11.5, LICENSE:481-484
  481:       11.5 LANGUAGE
  482: 
  483: The Agreement is drafted in both French and English and both versions
  484: are deemed authentic.

=== Q3. Root __pycache__/ (not created by this task) ===
files: 9 | mtime range 2026-09-15 .. 2026-09-17
check-ignore: .gitignore:2:__pycache__/	__pycache__/GUI_v18.cpython-314.pyc (exit 0)
```

## Diff artifact

`python t002_diff.py <scratchpad>` runs `git add -N` on every untracked
path from `git status` (explicit paths), writes the artifact with the
prompt's command, regenerates it to
`<scratchpad>/regen/002-licence.diff.txt` and runs cmp. The final run,
made after this report was complete, is in chat: it also checks that
the two blocks below match the live state verbatim.

The deletions column of the numstat block is 0 on every row: no line
is deleted.

### Numstat

```
22	0	CITATION.cff
515	0	LICENSE
12	0	README.md
216	0	prompt_outputs/001-bootstrap-commit.md
142	0	prompt_outputs/001-bootstrap-push.md
552	0	prompt_outputs/002-licence-implement.md
```

## Final state

### git status --porcelain -uall

```
 A CITATION.cff
 A LICENSE
 M README.md
 A prompt_outputs/001-bootstrap-commit.md
 A prompt_outputs/001-bootstrap-push.md
 A prompt_outputs/002-licence-implement.md
 A prompt_outputs/002-licence.diff.txt
```
