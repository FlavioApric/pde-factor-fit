# pde-factor-fit

Reading the **factor structure of a linear PDE** from data. For linear equations with constant coefficients the
natural unit is not the term but the *factor of the symbol*: every Fourier mode of a solution lies on the zero set of
one factor, so the modes fall into groups. This repository holds the theory, the algorithm, the code and the papers.

By **Flavio Pricoco**. Open for everyone to use under permissive licenses; please keep the credit (see [License](#license)).

## Start here

| I want to... | go to |
|---|---|
| read the main paper (one idea first, running example, results) | [`paper/B_proposed_structure/main.pdf`](paper/B_proposed_structure/main.pdf) |
| read the same paper in the analytical-first order | [`paper/A_user_structure/main.pdf`](paper/A_user_structure/main.pdf) |
| see how the two differ | [`paper/COMPARISON.md`](paper/COMPARISON.md) |
| run the algorithm | `pip install -e .` then see [`src/pdefactor`](src/pdefactor) and [`tests/`](tests) |
| see benchmarks and stored results | [`benchmarks/`](benchmarks) |
| work on it with Claude | [`claude/`](claude) (rules, map, status) |

## Branches

| branch | content | paper |
|---|---|---|
| `main` | the algorithm, tests, benchmarks and the two SIMODS manuscripts | Structure A and B |
| `analytical` | all theory and proofs (annihilators, factor decomposition, interaction term, identification, limits) | one paper, B style |
| `ml-layers` | learned layers on top of the pipeline: what worked, what did not, ideas | one paper, B style |
| `model-expansion` | extending the model: nonlinear, variable coefficients, time dependence, systems, non-local | one paper, B style |

Every branch has the same skeleton: `paper/`, code (`src/`), `tests/` and `benchmarks/`, and a `claude/` folder
with `CLAUDE.md` (rules), `MAP.md` (graph of the branch) and `STATUS.md` (what worked, what did not).
The graph of the whole repository is [`claude/REPO_MAP.md`](claude/REPO_MAP.md).

```mermaid
flowchart LR
  main[main: algorithm + papers A/B] --> analytical[analytical: theory + proofs]
  main --> mll[ml-layers: learned layers]
  main --> mex[model-expansion: beyond linear constant coefficients]
  analytical -. theorems used by .-> main
  mll -. extends .-> main
  mex -. extends .-> main
```

## Quick start

```bash
pip install -e ".[dev]"
pytest -q                      # full suite is slow (~13 min); tests/test_core_exact.py is quick
cd paper/B_proposed_structure && latexmk -pdf main.tex
```

## Cite

See [`CITATION.cff`](CITATION.cff) (GitHub shows a "Cite this repository" button).

## License

- Code: MIT, see [`LICENSE`](LICENSE).
- Papers, figures and documentation: CC BY 4.0, see [`LICENSE-papers.md`](LICENSE-papers.md).

Both licenses allow any use, including commercial, and both require that you credit Flavio Pricoco.
