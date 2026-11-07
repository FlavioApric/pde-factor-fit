# CLAUDE.md: working rules for this repository

Repository: `pde-factor-fit` by Flavio Pricoco (MIT code, CC BY 4.0 papers). Keep the author credit in every new file header
that carries a notice, and never write another name on the papers.

## What this is
Pipeline that reads the factor structure of a **linear, constant-coefficient, autonomous, scalar 1+1 PDE** from data:
samples of the field -> modes -> analytic core (factors, components, interaction term) -> Bayesian outer loop ->
distribution over equations with a label. Code: `src/pdefactor/`. Papers: `paper/`. Map: `claude/MAP.md`.

## Rules (binding)
1. **Output contract.** Labels are `FIT-COMPATIBLE`, `MISFIT`, `ID-KER(class)`, `UNDECIDED`. Never print "law identified".
   An honest `UNDECIDED` beats a wrong `FIT-COMPATIBLE`.
2. **Every change is general.** It must hold for any factor structure, order and coefficient scale, be justified by theory or a
   scale-free criterion, and be tested on held-out families, never only on the case that exposed the bug.
3. **Accuracy before speed.** A speed-up is allowed only if it is exact (same decisions).
4. **Keep the structure.** Same pipeline steps, outputs and interfaces. `tests/test_ml_contract.py` pins the entry points
   the learned layers use; keep old interfaces and add new ones.
5. **The core (`src/pdefactor/core/`) is deterministic.** Change it only with tests. The outer layer is Bayesian: Monte Carlo,
   no linearisation (the interaction term and the annihilator are discontinuous).
6. **Domains.** The split is proven on simply connected regions. Use rectangles or convex cells.
7. **Theory first.** Only proven results (see the `analytical` branch, `claude/notes/`) are foundations.
8. **Docs are add-only.** Do not delete or rename rows of the theory-to-algorithm table; add new ones.
9. **Papers.** Edit sections once in `paper/shared/sections/`; both structures include them. Run `paper/tools/hygiene.sh` and
   `paper/tools/check_notation.py` before committing.

## Commands
```bash
pip install -e ".[dev]"
pytest -q tests/test_core_exact.py tests/test_ml_contract.py tests/test_validate.py   # quick
pytest -q                                                                          # full, ~13 min
cd paper/B_proposed_structure && latexmk -pdf main.tex
```

## Out of scope (parked)
Nonlinear, variable coefficients, fractional, 2+1 / 3+1, non-monic symbols: see branch `model-expansion`.
Learned layers: see branch `ml-layers`. Proofs: see branch `analytical`.
