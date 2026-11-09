# pde-factor-fit · branch `model-expansion`

**What this branch is.** How to go beyond the base class (linear, constant coefficients, scalar, 1+1 dimensions): nonlinear equations, variable and time-dependent coefficients, systems, nonlocal laws. It gives the ladder of levels L0-L10, the six-step extended algorithm with a contract of guarantees, the answers to the four founding questions, the routes tried (introducing linearity, a direct equation, a change of variables) and what became of your ideas, four checked worked examples, the minimal route for extending the code, and the full specification step by step.

**Open this first:** [`paper/model_expansion.pdf`](paper/model_expansion.pdf) (21 pages; LaTeX source `paper/model_expansion.tex`).

| folder | what is in it |
|---|---|
| `paper/` | the paper: one `.tex` and one `.pdf` |
| `code/` | the four worked examples (`ex_L6_dirac.py`, `ex_L7_poschl_teller.py`, `ex_L8_stark.py`, `ex_L9_L10_dict.py`, each with its stored output `.out`) and `out_of_class_inject.py`, the generators of inputs outside the class (nonlinear, variable coefficient, fractional, two laws, coloured noise, aliasing) |
| `tests/` | `test_examples.py`: runs the four examples (35 checks) |
| `claude/` | for Claude sessions: rules, status, map, the full specification of the extended algorithm in Italian (`claude/notes/`), where each file came from (`claude/PROVENANCE.md`) |

```bash
pip install -e ".[dev]" && pytest -q tests/test_examples.py        # ~2 min
cd paper && latexmk -pdf model_expansion.tex
```
The extension is a specification plus symbolic checks; it is **not** implemented in the pipeline. The pipeline itself lives on branch `main` (`pip install -e ".[pipeline]"` installs it for the generators). The proofs are on branch `analytical`.
Licenses: code MIT, paper CC BY 4.0; cite via `CITATION.cff`. Author: Flavio Pricoco.
