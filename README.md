# pde-factor-fit, branch `analytical`

The mathematics: what an exact solution of a linear PDE remembers about its equation. Identification, factor decomposition, the interaction term,
the limits of exactness, and a nonlinear extension. By **Flavio Pricoco**. Papers and documentation: CC BY 4.0. Code: MIT.

**Read first:** [`paper/analytical/main.pdf`](paper/analytical/main.pdf) (30 pages): running example, the grouping principle ("groups are factors, not terms"), the stability angle,
the interaction term, when a solution determines its equation, Burgers across a shock, limits, full proofs (Appendix A) and a primer for newcomers (Appendix B).

```
paper/analytical/   the paper (LaTeX + built PDF)       paper/shared/    class fallback, macros, bibliography, figures used by the theory
proofs/             29 proof packages + the claim ledger (LEDGER.md)      proofs/lean/   Lean 4 formalisation of the algebraic core
verification/       94 symbolic / high-precision checks behind the proofs (RESULTS.md: which pass)
tests/              quick subset of the checks as pytest             claude/   rules, map, status, notes for Claude sessions
```

```bash
pip install -e ".[dev]"
pytest -q tests/test_verification.py        # 8 quick checks, ~30 s
cd paper/analytical && latexmk -pdf main.tex
```

Honest status: every statement carries a label (proved / proved mod. a cited theorem / conditional / open / false). The reviewers of the proofs were independent Claude agents,
not human referees; Lean covers fifteen core algebraic theorems. Notes and proof packages are in Italian and English (the working language of the first version was Italian).

Other branches: `main` (algorithm and the two SIMODS papers), `ml-layers`, `model-expansion`. See [`claude/REPO_MAP.md`](claude/REPO_MAP.md).
License: [`LICENSE`](LICENSE) (MIT), [`LICENSE-papers.md`](LICENSE-papers.md) (CC BY 4.0). Cite: [`CITATION.cff`](CITATION.cff).
