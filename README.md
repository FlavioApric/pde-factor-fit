# pde-factor-fit · branch `ml-layers`

**What this branch is.** Machine learning on top of the factor pipeline: every learned layer that was designed (L0 seeds, L1 high-wavenumber correction, L2 calibration, V0/V1 validator, the controller C, L5 encoder, L6 posterior), which ones were built and gated, and the honest verdicts. Result: one layer ships (an exact memo); the others are negative results with code, data and gates kept.

**Open this first:** [`paper/ml_layers.pdf`](paper/ml_layers.pdf) (39 pages; LaTeX source `paper/ml_layers.tex`). Table 5 lists every verdict; appendices hold the failure-mode table, the acceptance protocol, the test inventory, the explained edition and the original pipeline note.

| folder | what is in it |
|---|---|
| `paper/` | the paper: one `.tex` and one `.pdf` |
| `code/` | `pdefactor/` the pipeline snapshot the layers were built on, with the learned layers in `pdefactor/learned/`; `s_interp_variant/` the separate interpolation variant (scripts, outputs) |
| `tests/` | pytest: the layers, the "off equals the pipeline bit for bit" golden test, the interface pin |
| `benchmarks/` | experiment and gate scripts (`ll_*.py`), `runtime.json`, and `results/` (stored result tables, logs and session data behind every number) |
| `claude/` | for Claude sessions: rules, status, map, session plans and reports (`claude/archive/`), the Phase 4 plan (`claude/notes/`), where each file came from (`claude/PROVENANCE.md`) |

```bash
pip install -e ".[dev]" joblib
pytest -q tests/test_learned_off.py tests/test_ml_contract.py tests/test_runconfig.py     # ~4 min
```
**Important:** `code/pdefactor` is the pipeline version the layers were built on (main at an earlier commit plus the layers), not the current `main`; porting the hooks is open work (paper, ideas section).
Other branches: `main` (the algorithm and its two papers), `analytical`, `model-expansion`. Licenses: code MIT, papers CC BY 4.0; cite via `CITATION.cff`. Author: Flavio Pricoco.
