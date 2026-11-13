# pde-factor-fit

**Reading the factor structure of a linear PDE from data.** For a linear equation with constant coefficients, the natural unit is not the term but the *factor of the symbol*: every Fourier mode of a solution lies on the zero set of one factor, so the modes fall into groups, and learning the equation means finding those groups. This repository holds the theory, the algorithm, the code and the papers. Author: **Flavio Pricoco**.

## This branch: the SIMODS submission (`simods-submission`)

The paper compacted to SIAM's limit and submitted to the *SIAM Journal on Mathematics of Data Science*, with its
supplementary materials:

| file | what it is |
|---|---|
| [`paper/simods.pdf`](paper/simods.pdf) | **the paper** (17 pages in SIAM's class: 16 of text + references; limit 20): one idea, groups are factors, built around the two groupings, with the 285-equation benchmark as the main evidence |
| [`paper/simods_supplement.pdf`](paper/simods_supplement.pdf) | the supplementary materials (12 pages): proofs of the main results written to be read, interaction term, complete algorithm and parameters, further cases, guide to the output, beyond the linear case |
| [`paper/simods_reading.pdf`](paper/simods_reading.pdf), [`paper/simods_supplement_reading.pdf`](paper/simods_supplement_reading.pdf) | the same two documents in SIAM's class without the review line numbers, for reading |
| `paper/parts/` | the editable sources, one file per section; `code/tools/assemble_simods.py paper` writes `paper/simods.tex` and `paper/simods_supplement.tex` from them |
| `code/experiments/make_fig_evidence.py` | draws the new evidence figure `paper/figures/fig_evidence.pdf` |
| `code/experiments/make_figs_simods.py` | draws the paper's figures at the SIAM text width in Computer Modern (`paper/figures/simods/`), from the same data and drawing code as `make_figs.py` |
| `code/tools/build_supplement_zip.py` | builds the code-and-data archive sent as supplementary material (a byte-exact snapshot of this repository's code and benchmark data plus the worked-example run) |

To rebuild the PDFs, put SIAM's class `siamonline250211.cls` and `siamplain.bst` (from
https://epubs.siam.org/journal-authors) in `paper/`, then run `pdflatex` on `simods.tex` and `simods_supplement.tex`
twice each, alternating, so that the cross-references between paper and supplement resolve. Without the class the
paper builds with the fallback in its preamble, for reading only.

The longer papers below are unchanged and remain the complete record.

## Open this first

[`paper/structure_B.pdf`](paper/structure_B.pdf): the main paper (41 pages): one idea first, a running example, the algorithm, the benchmark. [`paper/structure_A.pdf`](paper/structure_A.pdf) is the same paper in the order theory first, then algorithm. [`paper/reading_results.pdf`](paper/reading_results.pdf) (10 pages) explains how to **read the results**: every returned parameter and distribution, which test each p-value comes from, and how to read the direction images.
Each paper is one `.tex` file with its `.pdf` (figures in `paper/figures/`).

> **Structure A and Structure B are the same paper, written in two alternative orders.** Same results, same proofs, same numbers: Structure B opens with the idea and a running example (best for a first read); Structure A develops the theory first and the algorithm after (best if you prefer to see the mathematics before the method). Read one, not both. `reading_results` is a separate guide to reading the output.

## Results in one table

| benchmark | inputs | this method: right or equivalent | this method: wrong without warning | best baseline |
|---|---|---|---|---|
| **large random-PDE benchmark** (final) | 285 independent random equations, 5 families, grid, 1 % noise; none used in development | **275 / 285 = 96.5 %** (95 % CI 93.7-98.1) | **0** (upper 95 % bound 1.0 %) | weak SINDy: 81 / 285 = 28.4 %, wrong without warning on 204 |
| development benchmark | 10 equations x 3 designs (grid 1 %, grid 5 %, 400 scattered points 5 %) | 30 / 30 | 0 | weak SINDy: 25 / 30, wrong without warning on 5 |
| independent repetitions | the two grid designs, 3 new fields and noise draws each | 60 / 60 | 0 | weak SINDy: 47 / 60, wrong without warning on 13 |

In the large benchmark 15 of the 300 planned draws (12 in family F4, 3 in F5) hit the 3-hour time limit and have no result; counting every one of them as a failure still gives 275 / 300 = 91.7 %. Full table with per-family results and paired tests: [`claude/benchmark_tables/large.md`](claude/benchmark_tables/large.md); raw rows: [`benchmarks/out/large.jsonl`](benchmarks/out/large.jsonl). Development and repetition tables: [`claude/benchmark_tables/p8_final_v5.md`](claude/benchmark_tables/p8_final_v5.md).

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
| `paper/` | the papers (`.tex` + `.pdf`) and `figures/` |
| `code/` | `pdefactor/` the algorithm (Python package), `experiments/` experiment and figure scripts, `tools/` repository tools (paper checks, graphs, coverage) |
| `tests/` | pytest suite (224 tests) |
| `benchmarks/` | benchmark scripts (the final large benchmark is `bench_large.py` + `large_report.py`), and `out/`, `data/` with the stored results behind the papers' numbers |
| `claude/` | for Claude sessions: rules, status, map, theory-to-code table, plans, reports, graph of the repository, inventory, where each file came from (`claude/PROVENANCE.md`) |

## Quick start (3 minutes)

You need Python 3.12 or newer. Nothing else.

```bash
git clone https://github.com/FlavioApric/pde-factor-fit.git
cd pde-factor-fit
pip install -e ".[dev]"            # installs the package `pdefactor` (numpy, scipy, sympy, matplotlib, ...)
python -m pdefactor.demo           # simulates a PDE, runs the algorithm, prints the answer (about 10 s)
```

Expected output (the last lines):

```
label=FIT-COMPATIBLE  equation: (1.0*tau + 0.999*xi + 0.0082) * (1.0*tau - 0.2859*xi**2) u = 0
...
In plain words:
  the data are consistent with a product of the factors printed below (NOT a proof the law is that equation)
```

That is the whole algorithm on a toy problem: the data were generated by `(d_t + d_x)(d_t - 0.29 d_x^2) u = 0` (transport times diffusion) plus 5 % noise, and the algorithm recovered both factors **separately**, which is the point of the method. `tau` stands for `d/dt`, `xi` for `d/dx`.
Other built-in cases: `python -m pdefactor.demo --list`, e.g. `python -m pdefactor.demo heat --noise 0.02`.

## What do I run? (the only files you need)

| I want to ... | run / open |
|---|---|
| see the algorithm work in 10 seconds | `python -m pdefactor.demo` |
| get a full report with figures for a case | `python benchmarks/final_report.py --case transport_plus_diffusion --noise 0.05 --out my_run` (then open `my_run/`) |
| use it from my own Python code | `from pdefactor.loop import run_loop` (see below) |
| reproduce the large random-PDE benchmark | `python benchmarks/bench_large.py --seeds 0-59 --noises 0.01 --workers 6` (resumable; hours), then `python benchmarks/large_report.py` |
| check that everything works | `pytest -q tests/test_core_exact.py` (seconds); `pytest -q` is the full suite (about 55 min) |
| read the idea | `paper/structure_B.pdf` |
| rebuild a paper | `cd paper && latexmk -pdf structure_B.tex` |

Everything else under `code/` is either the library you import (`code/pdefactor/`), scripts that produced the papers' numbers and figures (`code/experiments/`), or repository tools (`code/tools/`). **You never run files inside `code/pdefactor/` directly**; you import them after `pip install -e .`.

## Use it on your own data

The algorithm takes a field `u(t, x)` sampled on a regular grid, **periodic in x**, and an estimate `sigma` of the noise standard deviation:

```python
import numpy as np
from pdefactor.loop import run_loop

t = np.linspace(0, 2, 64)                              # times, shape (nt,)
x = np.linspace(0, 2*np.pi, 128, endpoint=False)       # positions, shape (nx,), periodic
u = ...                                                # your data, shape (nt, nx)
sigma = 0.01                                           # noise std (estimate)

res = run_loop([u], t, x, sigma)                       # the list may hold several noisy/posterior copies of u
print(res.label)                                       # FIT-COMPATIBLE / MISFIT / UNDECIDED / ID-KER(...)
print(res.equation())                                  # product of factors, e.g. (1.0*tau - 0.4998*xi**2) u = 0
print(res.summary())                                   # everything: weights, intervals, evidence, notes
```

Checked example: `u = e^{-t/2} cos x + 0.5 e^{-2t} sin 2x` plus noise returns `(1.0*tau - 0.4998*xi**2) u = 0`, i.e. `u_t = 0.5 u_xx`.
Scattered (non-grid) data: first interpolate with `pdefactor.interp` (Gaussian-process posterior samples), then pass the samples to `run_loop`; the paper (section on interpolation) explains this step.

## How to read the result

| label | meaning |
|---|---|
| `FIT-COMPATIBLE` | the data are consistent with the printed product of factors within the search bounds. **This is never a claim that the law is identified** |
| `MISFIT` | no structure inside the bounds explains the data (try a larger search bound, or the model is outside the class) |
| `ID-KER(class)` | the factors are identified by the kernel of the operator, in the stated contract class |
| `UNDECIDED` | the data cannot decide between structures (more data, less noise, or longer time window) |

`W` is the weight of a factor (share of the field's energy), `[clean ...]` marks a factor found on its own component, `P(k)` is the posterior over the number of factors, `split layer` reports whether two nearby factors can be told apart (Friedrichs angle).

## Troubleshooting

| symptom | fix |
|---|---|
| `ModuleNotFoundError: pdefactor` | run `pip install -e .` from the repository root, with the same Python you run scripts with |
| `ModuleNotFoundError: matplotlib/torch/numpyro` | `pip install -e ".[dev]"`; torch/numpyro are only needed for the `ml` extra: `pip install -e ".[ml]"` |
| Python version error | use Python 3.12 or newer |
| result is `MISFIT` on your data | check that x is periodic and `sigma` is realistic; see paper section "decidability" |
| full test suite is slow | it takes about 55 min by design; use `pytest -q tests/test_core_exact.py tests/test_demo.py` for a quick check |

## Code tour (`code/pdefactor/`)

| file | role |
|---|---|
| `loop.py` | **entry point** `run_loop`: the whole pipeline (levels, regrouping, split, decision) |
| `core/` | the analytic core: spectral modes (matrix pencil), factor fit (`structfit.py`), varieties |
| `aggregate.py` | pools the per-sample results into a distribution over factors (Dirichlet-process clustering) |
| `bayes_split.py` | Friedrichs-angle split layer: are two factors really two? |
| `interp/` | step 1: Gaussian-process interpolation with posterior samples for scattered data |
| `domain/` | non-periodic / irregular domains (cells, quadtree) |
| `synthetic.py`, `simulator.py` | exact solutions with ground truth, random PDEs for benchmarks |
| `demo.py` | the 10-second demo |
| `learned/`, `baselines/` | optional: learned layers and comparison methods (see branch `ml-layers`) |

## More

`claude/REPO_MAP.md` shows how the four branches relate; `claude/PROVENANCE.md` says where every file came from. Licenses: code MIT ([`LICENSE`](LICENSE)), papers CC BY 4.0 ([`LICENSE-papers.md`](LICENSE-papers.md)); please cite via [`CITATION.cff`](CITATION.cff). Author: Flavio Pricoco.
