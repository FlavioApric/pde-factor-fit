# CLAUDE.md for branch `analytical`

Author credit: Flavio Pricoco. Keep the LICENSE files intact. Layout: `paper/` (two LaTeX files + PDFs), `code/` (`verification/`, `lean/`), `tests/`, `claude/` (this folder: every markdown file).

## Rules
1. **Foundations are proved results only.** Use `claude/proofs/LEDGER.md` rows with status DIMOSTRATO (proved) or CON-FONTE (known, source verified). Cite the status next to every claim.
2. **Status words** in the paper: proved, proved mod. a cited theorem, conditional, open, false. FALSO results are cited only as failure modes.
3. **Add only.** Do not delete or rename ledger rows or proof packages; add rows and new files.
4. Verification scripts check, they do not prove. Do not present bounded output as a universal proof.
5. Paper edits: `paper/analytical.tex` is one flat file (generated once from a multi-file source; edit it directly). The proofs live in `paper/analytical_proofs.tex`; keep "Dim. An/Bn" numbers consistent between the two.
6. Notes in `claude/` may be Italian (the original working language); translate or add, do not rewrite history.

## Commands
```bash
pip install -e ".[dev]"
pytest -q tests/test_verification.py
cd paper && latexmk -pdf analytical.tex && latexmk -pdf analytical_proofs.tex
```
Lean: `cd code/lean/project && lake build` (needs Lean 4 and Mathlib; not run in CI). Verification scripts run from `code/verification/` (`python -I <script>`); the status of all of them is `claude/verification_results.md`.
