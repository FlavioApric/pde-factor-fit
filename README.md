# pde-factor-fit, branch `analytical`

The mathematics: what an exact solution of a linear PDE remembers about its equation. Identification, factor decomposition, the interaction term,
the limits of exactness, and a nonlinear extension. By **Flavio Pricoco**. Papers and documentation: CC BY 4.0. Code: MIT.

**Read first:** [`paper/analytical/main.pdf`](paper/analytical/main.pdf) (57 pages, all **eleven phases 0-10**): Part I (Sections 1-6): running example, the grouping principle ("groups are factors, not terms"), the stability angle,
the interaction term, when a solution determines its equation, Burgers across a shock. Part II (Sections 7-16): systems and gauge, variable coefficients, convergence and noise, the analytic encoder, the universal dictionary and misfit certificate,
what Phase 10 changed, the extended algorithm, limits of all phases, the complete list of open problems, directions not taken. Appendices: full proofs, glossary of classical tools, primer for newcomers.

**The complete editions in their original format** (every chapter and every proof card): [`paper/analytical_complete/`](paper/analytical_complete): `paper_tutte_le_fasi.pdf` (117 pp, phases 0-10) and the companion **`dimostrazioni_tutte_le_fasi.pdf`
(263 pp, catalogue of 155 proofs)**. Also `analytical_phases05/` (76 + 116 pp, phases 0-5), `analytical_explained/` (plain-language edition), `analytical_original/` (the first long manuscript).

```
paper/analytical/   the 57-page paper (LaTeX + PDF)     paper/analytical_complete/  117 pp paper + 263 pp proofs catalogue (original format)
paper/shared/       class fallback, macros, bibliography    paper/analytical_phases05, analytical_explained, analytical_original: earlier editions
proofs/             29 proof packages + the claim ledger (LEDGER.md)      proofs/lean/   Lean 4 formalisation of the algebraic core
verification/       all symbolic / high-precision scripts of every session (RESULTS.md: which pass)
claude/archive/     plans, reports, audits, scouting notes, claim ledgers, inbox (work/, research/, claims/, origin/)
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
