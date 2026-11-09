# pde-factor-fit

**Reading the factor structure of a linear PDE from data.** For a linear equation with constant coefficients, the natural unit is not the term but the *factor of the symbol*: every Fourier mode of a solution lies on the zero set of one factor, so the modes fall into groups, and learning the equation means finding those groups. This repository holds the theory, the algorithm, the code and the papers. Author: **Flavio Pricoco**.

## Open this first

[`paper/structure_B.pdf`](paper/structure_B.pdf): the main paper (41 pages): one idea first, a running example, the algorithm, the benchmark. [`paper/structure_A.pdf`](paper/structure_A.pdf) is the same paper in the order theory first, then algorithm. [`paper/explained.pdf`](paper/explained.pdf) is the algorithm explained step by step in plain language (46 pages).
Each paper is one `.tex` file with its `.pdf` (figures in `paper/figures/`).

## The four branches

| branch | what it holds | open |
|---|---|---|
| **`main`** (you are here) | the algorithm, its tests and benchmarks, and the three papers above | `paper/structure_B.pdf` |
| `analytical` | the mathematics, all eleven phases: identification, factor decomposition, interaction term, systems, variable coefficients, dictionary, with all proofs | [`paper/analytical.pdf`](https://github.com/FlavioApric/pde-factor-fit/blob/analytical/paper/analytical.pdf) (130 pp) and [`paper/analytical_proofs.pdf`](https://github.com/FlavioApric/pde-factor-fit/blob/analytical/paper/analytical_proofs.pdf) (263 pp) |
| `ml-layers` | machine learning on top of the pipeline: every layer designed, which worked, which did not, why | [`paper/ml_layers.pdf`](https://github.com/FlavioApric/pde-factor-fit/blob/ml-layers/paper/ml_layers.pdf) (39 pp) |
| `model-expansion` | going beyond linear constant coefficients: the ladder of extensions, the routes tried, worked examples | [`paper/model_expansion.pdf`](https://github.com/FlavioApric/pde-factor-fit/blob/model-expansion/paper/model_expansion.pdf) (21 pp) |

## Folders of this branch

| folder | what is in it |
|---|---|
| `paper/` | the three papers (`.tex` + `.pdf`) and `figures/` |
| `code/` | `pdefactor/` the algorithm (Python package), `experiments/` experiment and figure scripts, `tools/` repository tools (paper checks, graphs, coverage) |
| `tests/` | pytest suite (224 tests) |
| `benchmarks/` | benchmark scripts, and `out/`, `data/` with the stored results behind the papers' numbers |
| `claude/` | for Claude sessions: rules, status, map, theory-to-code table, plans, reports, graph of the repository, inventory, where each file came from (`claude/PROVENANCE.md`) |

## Quick start

```bash
pip install -e ".[dev]"
pytest -q tests/test_core_exact.py          # quick; the full suite takes ~55 min
cd paper && latexmk -pdf structure_B.tex
```
Optional extras for some tests and benchmarks: `pip install -e ".[ml,baselines]"`.
`claude/REPO_MAP.md` shows how the four branches relate. Licenses: code MIT ([`LICENSE`](LICENSE)), papers CC BY 4.0 ([`LICENSE-papers.md`](LICENSE-papers.md)); please cite via [`CITATION.cff`](CITATION.cff).
