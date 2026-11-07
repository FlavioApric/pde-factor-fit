# pde-factor-fit, branch `model-expansion`

How to go beyond linear constant coefficients: nonlinear equations, variable and time-dependent coefficients, systems, nonlocal laws.
By **Flavio Pricoco**. Code: MIT. Paper: CC BY 4.0.

**Read first:** [`paper/model_expansion/main.pdf`](paper/model_expansion/main.pdf) (8 pages): the ladder of levels L0-L10, the six-step extended algorithm,
what is proved and what is impossible in each direction, four worked examples, the minimal route for extending the code, open questions.

```
paper/model_expansion/   the paper            examples/    four checked worked examples (7+11+5+12 checks)
src/pdefactor/, tests/   current pipeline     benchmarks/  out_of_class_inject.py: inputs outside the class (nonlinear, varcoef, ...)
claude/                  rules, map, status, notes (the full extended-algorithm specification, in Italian)
```

```bash
pip install -e ".[dev]"
pytest -q tests/test_examples.py        # the four examples, ~1 min
cd paper/model_expansion && latexmk -pdf main.tex
```

Status: the extended algorithm is a **specification** plus symbolic checks; it is not implemented in `src/`. The proofs are on branch `analytical`.
Other branches: `main`, `analytical`, `ml-layers`. See [`claude/REPO_MAP.md`](claude/REPO_MAP.md). Licenses: [`LICENSE`](LICENSE), [`LICENSE-papers.md`](LICENSE-papers.md). Cite: [`CITATION.cff`](CITATION.cff).
