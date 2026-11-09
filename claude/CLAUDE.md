# CLAUDE.md for branch `model-expansion`

Author credit: Flavio Pricoco. Keep the LICENSE files intact. Layout: `paper/` (one `.tex` + `.pdf`), `code/` (examples and generators), `tests/`, `claude/` (every markdown file).

## Rules
1. Never print "law identified" from finite numerical data. Labels: `FIT-COMPATIBLE`, `MISFIT`, `ID-KER(class)`, `UNDECIDED`; `IDENTIFIED[sense, model]` only with an exact symbolic proof.
2. Every output carries two labels: completeness (almost always class C) and conditional correctness (A, B, C, Lim). Name the sense of "identify" (ID-ann, ID-ker, ID-res, ID-fam, ID-lim).
3. Foundations are only proved results (or known results with a verified source), see branch `analytical` (`claude/proofs/`). Cite the status next to every claim.
4. Compute the misfit residual by least squares, never by a ratio of Gram determinants.
5. Out-of-class data: detect and refuse first; extend by declared classes, never free-form.
6. Do not edit `claude/notes/ALGORITMO_ESTESO_it.md` except to translate or add; it is the source specification (the paper's appendix renders it in English).
7. `paper/model_expansion.tex` is one flat file; edit it directly.

## Commands
```bash
pip install -e ".[dev]"
pytest -q tests/test_examples.py
cd paper && latexmk -pdf model_expansion.tex
```
