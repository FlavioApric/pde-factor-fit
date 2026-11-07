# CLAUDE.md for branch `ml-layers`

Author credit: Flavio Pricoco. Keep LICENSE files intact.

## Rules
1. **Contract of a learned layer** (paper, section 3): off = bit-identical to the pipeline; a layer proposes, calibrates or flags, never decides a label;
   likelihood fixed; Monte Carlo, not linearisation; ship only if the gate passes in every leave-one-family-out fold; dimensionless features.
2. **Labels:** `FIT-COMPATIBLE`, `MISFIT`, `ID-KER(class)`, `UNDECIDED`. Never "law identified".
3. **Failed layers stay in the repo** with code, tests and the measured reason. Do not delete them.
4. **Re-gate on the pipeline you ship**: a verdict is tied to a pipeline version (see STATUS.md).
5. `tests/test_ml_contract.py` pins the interfaces between the pipeline and the layers. Keep old interfaces; add new ones.
6. The golden file `tests/data/learned_off_golden.json` was regenerated on Linux; regenerate with `python tests/data/make_learned_off_golden.py` after a numerical-library change, never after a code change.

## Commands
```bash
pip install -e ".[dev]" joblib
pytest -q tests/test_learned_off.py tests/test_ml_contract.py tests/test_runconfig.py
pytest -q                      # full, long
cd paper/ml_layers && latexmk -pdf main.tex
```
Experiment scripts: `benchmarks/ml_layers/ll_*.py` (corpus `ll_corpus.py`, gates `ll_gate.py`, injected failures `ll_inject.py`, retrain `ll_budget_fit.py --retrain`).
Scripts expect run outputs in `analysis/exp/out/` (not stored; regenerate with `fastrun.py`). Reports behind every number: `benchmarks/ml_layers/results/`.
