# CLAUDE.md for branch `analytical`

Author credit: Flavio Pricoco. Keep LICENSE files intact.

## Rules
1. **Foundations are proved results only.** Use `proofs/LEDGER.md` rows with status DIMOSTRATO (proved), or CON-FONTE (known, with a verified source). Cite status next to every claim.
2. **Status words** (paper): proved, proved mod. a cited theorem, conditional, open, false. FALSO results are cited only as failure modes.
3. **Add only.** Do not delete or rename ledger rows or proof packages; add rows and new files.
4. Verification scripts check, they do not prove. Do not present bounded output as a universal proof.
5. Paper edits: each section lives once in `paper/analytical/sections/`; theory sections `thy_*.tex` are shared in content with the main paper's Structure B (`main` branch). Keep both in step.
6. Notes in `claude/notes/` are Italian (original working language); translate or add, do not rewrite history.

## Commands
```bash
pip install -e ".[dev]"
pytest -q tests/test_verification.py
cd paper/analytical && latexmk -pdf main.tex
```
Lean: `cd proofs/lean && lake build` (needs Lean 4 and Mathlib; not run in CI).
