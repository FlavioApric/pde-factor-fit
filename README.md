# pde-factor-fit, branch `ml-layers`

Learned layers on top of the factor pipeline for linear PDEs: what worked, what did not, and the ideas that remain.
By **Flavio Pricoco**. Code: MIT. Paper: CC BY 4.0.

**Read first:** [`paper/ml_layers/main.pdf`](paper/ml_layers/main.pdf) (21 pages; the table of verdicts is Table 5): the pipeline and the learning inside it, the contract and protocol, **every layer as designed** (L0, L1, L2a-d, V0/V1, the controller C, L5, L6, the differentiable core), what was built and what happened, the controller in detail, what was never built, appendices with the failure-mode table, acceptance protocol and test inventory.

| layer | verdict |
|---|---|
| LB exact memo | go, on by default (bit-identical, ~0.5 % faster) |
| V1 failure detector | no-ship (AUROC 0.85, detection 0-8 % at a 5 % false-alarm level) |
| LB learned skip, L2b, L2c, L2d, H0 | no-go |
| L0 seeds | closed, no gain |
| C controller | not built (oracle ceiling 8/12, 0/12 with a real trigger) |

## Layout
```
paper/ml_layers/    the paper (LaTeX, built PDF)        paper/shared/   class fallback, macros, bibliography
src/pdefactor/      pipeline snapshot + learned/ layers  tests/          pytest, incl. the off-is-bit-identical golden test
benchmarks/ml_layers/  experiment scripts (ll_*.py), results/ and sessions/ (the reports and data behind every number)
variants/s_interp/   the separate interpolation variant (its notes, experiment scripts, session scripts and outputs; its source modules are identical to `src/pdefactor/interp/` and are not duplicated)
paper/ml_explained/, paper/ml_pipeline_note/   the explained edition of the ML layers and the original pipeline note
claude/             rules, map, status, notes for Claude sessions
```

## Run
```bash
pip install -e ".[dev]" joblib
pytest -q tests/test_learned_off.py tests/test_ml_contract.py tests/test_runconfig.py   # ~4 min
```

## Important
`src/` is the pipeline version the layers were built on (main at `eaa8f9c` + layers), not the current `main`. Porting the layer hooks
to the current pipeline is open work (paper, section 9, item 5). See [`claude/STATUS.md`](claude/STATUS.md).

Other branches: `main` (algorithm and papers), `analytical` (proofs), `model-expansion`. See [`claude/REPO_MAP.md`](claude/REPO_MAP.md).
License: [`LICENSE`](LICENSE) (MIT), [`LICENSE-papers.md`](LICENSE-papers.md) (CC BY 4.0). Cite: [`CITATION.cff`](CITATION.cff).
