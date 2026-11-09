# CLAUDE.md: working rules for this repository (branch `main`)

Repository `pde-factor-fit` by Flavio Pricoco (MIT code, CC BY 4.0 papers). Keep the author credit and never write another name on the papers.
Layout: `paper/` (three flat `.tex` files + PDFs), `code/` (`pdefactor/`, `experiments/`, `tools/`), `tests/`, `benchmarks/`, `claude/` (every markdown file).

## What this is
Pipeline that reads the factor structure of a **linear, constant-coefficient, autonomous, scalar 1+1 PDE** from data: samples of the field -> modes -> analytic core (factors, components, interaction term) -> Bayesian outer loop -> distribution over equations with a label. Map: `claude/MAP.md`; theory-to-code table: `claude/archive/pipeline/analysis/THEORY_TO_ALGO.md`.

## Rules (binding)
1. **Output contract.** Labels are `FIT-COMPATIBLE`, `MISFIT`, `ID-KER(class)`, `UNDECIDED`. Never print "law identified". An honest `UNDECIDED` beats a wrong `FIT-COMPATIBLE`.
2. **Every change is general.** It must hold for any factor structure, order and coefficient scale, be justified by theory or a scale-free criterion, and be tested on held-out families, never only on the case that exposed the bug.
3. **Accuracy before speed.** A speed-up is allowed only if it is exact (same decisions).
4. **Keep the structure.** Same pipeline steps, outputs and interfaces. `tests/test_ml_contract.py` pins the entry points the learned layers (branch `ml-layers`) use; keep old interfaces and add new ones.
5. **The core (`code/pdefactor/core/`) is deterministic.** Change it only with tests. The outer layer is Bayesian: Monte Carlo, no linearisation.
6. **Domains.** The split is proven on simply connected regions. Use rectangles or convex cells.
7. **Theory first.** Only proven results (branch `analytical`) are foundations.
8. **Docs are add-only.** Do not delete or rename rows of the theory-to-algorithm table; add new ones.
9. **Papers.** `paper/structure_A.tex`, `structure_B.tex` and `explained.tex` are flat files; the two structures share their text (keep them in step). Run `python code/tools/paper_checks.py` before committing.

## Commands
```bash
pip install -e ".[dev]"
pytest -q tests/test_core_exact.py tests/test_ml_contract.py tests/test_validate.py     # quick
pytest -q                                                                          # full, ~55 min
cd paper && latexmk -pdf structure_B.tex
python code/experiments/make_figs.py        # regenerate paper/figures from benchmarks/data
```

## Out of scope (parked)
Nonlinear, variable coefficients, fractional, 2+1 / 3+1, non-monic symbols: see branch `model-expansion`. Learned layers: `ml-layers`. Proofs: `analytical`.
