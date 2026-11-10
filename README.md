# pde-factor-fit · branch `model-expansion`

**What this branch is.** How to go beyond the base class (linear, constant coefficients, scalar, 1+1 dimensions): nonlinear equations, variable and time-dependent coefficients, systems, nonlocal laws. It gives the ladder of levels L0-L10, the six-step extended algorithm with a contract of guarantees, the answers to the four founding questions, the routes tried (introducing linearity, a direct equation, a change of variables) and what became of your ideas, four checked worked examples, the minimal route for extending the code, and the full specification step by step.

**Open this first:** [`paper/model_expansion.pdf`](paper/model_expansion.pdf) (21 pages; LaTeX source `paper/model_expansion.tex`).

> **Who this branch is for.** For people who want to *extend* the algorithm. Today the algorithm (branch `main`) handles only **linear equations with constant coefficients**; it does not handle nonlinear terms, variable coefficients, systems or nonlocal laws. What you find here is **not working, optimised extension code**: it is the thinking done so far on how to extend it, namely a ladder of levels, a specified extended algorithm with the guarantees it could offer, the routes tried and parked, and small symbolic examples that check the key identities. Treat it as starting points, considerations and open questions to build on, not as a tool to run on data.

| folder | what is in it |
|---|---|
| `paper/` | the paper: one `.tex` and one `.pdf` |
| `code/` | the four worked examples (`ex_L6_dirac.py`, `ex_L7_poschl_teller.py`, `ex_L8_stark.py`, `ex_L9_L10_dict.py`, each with its stored output `.out`) and `out_of_class_inject.py`, the generators of inputs outside the class (nonlinear, variable coefficient, fractional, two laws, coloured noise, aliasing) |
| `tests/` | `test_examples.py`: runs the four examples (35 checks) |
| `claude/` | for Claude sessions: rules, status, map, the full specification of the extended algorithm in Italian (`claude/notes/`), where each file came from (`claude/PROVENANCE.md`) |

## Quick start

1. **Read:** [`paper/model_expansion.pdf`](paper/model_expansion.pdf): the ladder of levels, the extended algorithm, the routes tried, four worked examples, and (appendix) the step-by-step specification.
2. **Run a worked example** (Python 3.10 or newer; sympy only):

```bash
git clone -b model-expansion https://github.com/FlavioApric/pde-factor-fit.git
cd pde-factor-fit
pip install -e ".[dev]"
python code/ex_L8_stark.py            # 0.5 s; prints PASS lines, ends with "5/5 PASS"
pytest -q tests/test_examples.py      # all four examples, about 2 min
```
Each example `code/ex_L*.py` is a standalone symbolic check of one level of the ladder (L6 Dirac, L7 Poeschl-Teller, L8 Stark with time-dependent potential, L9/L10 dictionary); its stored output is the `.out` next to it. The comments inside are in Italian, the printed lines are `PASS`/`FAIL`.

## Which file do I open / run?

| I want to ... | file |
|---|---|
| understand what extends and what does not | `paper/model_expansion.pdf` |
| see the extended algorithm step by step (inputs, outputs, guarantees, failures) | appendix of the paper; the original Italian specification is `claude/notes/ALGORITMO_ESTESO_it.md` |
| check a worked example | `code/ex_L6_dirac.py`, `ex_L7_poschl_teller.py`, `ex_L8_stark.py`, `ex_L9_L10_dict.py` |
| generate test inputs outside the base class (nonlinear, variable coefficient, fractional, two laws, coloured noise, aliasing) | `code/out_of_class_inject.py` (needs the pipeline: `pip install -e ".[pipeline]"`, installs it from `main`) |

**Status:** specification and symbolic checks only; nothing here is implemented in the pipeline. The pipeline lives on `main`, the proofs on `analytical`.

## Troubleshooting

| symptom | fix |
|---|---|
| `ModuleNotFoundError: pdefactor` in `out_of_class_inject.py` | `pip install -e ".[pipeline]"` (the generators call the pipeline from `main`) |
| an example prints FAIL | report it with the printed line; they are deterministic |
| LaTeX errors | `cd paper && latexmk -pdf model_expansion.tex` needs TeX Live; the bibliography is embedded |

## Folders

| folder | what is in it |
|---|---|
| `paper/` | the paper: one `.tex` and one `.pdf` |
| `code/` | the four worked examples (each with its stored output `.out`) and `out_of_class_inject.py` |
| `tests/` | `test_examples.py`: runs the four examples (35 checks) |
| `claude/` | for Claude sessions: rules, status, map, the full Italian specification (`claude/notes/`), where each file came from (`claude/PROVENANCE.md`) |

Glossary: *level L0-L10* = a rung of the ladder of extensions (L0 is the base class); *contract* = what the extended algorithm promises at each level (classes A/B/C/Limit); *gauge* = a transformation of the unknown that leaves the law unchanged.
Licenses: code MIT ([`LICENSE`](LICENSE)), papers CC BY 4.0 ([`LICENSE-papers.md`](LICENSE-papers.md)); please cite via [`CITATION.cff`](CITATION.cff). Author: Flavio Pricoco.
