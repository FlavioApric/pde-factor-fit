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

## Quick start

1. **Read:** [`paper/ml_layers.pdf`](paper/ml_layers.pdf). Table 5 gives the verdict for every layer: one ships (an exact memo), the others are documented negative or deferred results.
2. **Run the algorithm with and without a learned layer** (Python 3.12 or newer):

```bash
git clone -b ml-layers https://github.com/FlavioApric/pde-factor-fit.git
cd pde-factor-fit
pip install -e ".[dev]" joblib
python - <<'PY'
import numpy as np
from pdefactor import aggregate as AG
from pdefactor.loop import run_loop
from pdefactor.synthetic import any_case, grid
from pdefactor.learned.runconfig import RunConfig

t, x, u = grid(any_case("transport_plus_diffusion"))
sigma = 0.05 * np.std(np.abs(u))
samples, pis = AG.fake_posterior(u, sigma, 3, rng=1)       # noisy copies of the field
print(run_loop(samples, t, x, sigma, pis).equation())                              # pipeline alone
print(run_loop(samples, t, x, sigma, pis, config=RunConfig(highk=True)).equation())  # with layer L1 (H0 scan) on
PY
```
Expected: both lines print `(1.0*tau + 0.999*xi + 0.0082) * (1.0*tau - 0.2859*xi**2) u = 0` (the layers never change a label by design; they propose, and the exact evidence decides).
3. **Tests** (about 4 min): `pytest -q tests/test_learned_off.py tests/test_ml_contract.py tests/test_runconfig.py`. The key test, `test_learned_off`, checks that with every layer off the output equals the pipeline bit for bit.

## Which file do I open / run?

| I want to ... | file |
|---|---|
| see which layers exist and what happened to each | `paper/ml_layers.pdf` (layers L0, L1, L2a-d, V0/V1, controller C, L5, L6) |
| read the layer code | `code/pdefactor/learned/` (`highk.py` = L1, `calibrate.py` = L2, `validator.py` = V1, `controller.py` + `remedy.py` + `runconfig.py` = C, `memo.py` = the layer that ships) |
| reproduce a gate or an experiment | `benchmarks/ll_*.py` (`ll_gate.py` final gate, `ll_C_*.py` controller, `ll_budget_*.py` budget layer); `benchmarks/fastrun.py` runs a corpus quickly; stored outputs are in `benchmarks/results/` |
| see the interpolation variant | `code/s_interp_variant/` |

The optional layers L0 and L2 need `pip install -e ".[ml]"` (torch).

## Troubleshooting

| symptom | fix |
|---|---|
| `ModuleNotFoundError: joblib` or `torch` | `pip install joblib`; torch only for `expseeds.py` (`pip install -e ".[ml]"`) |
| results differ in the last digits from the stored ones | Windows and Linux floats differ slightly; the golden test was regenerated on Linux |
| a benchmark takes very long | the `ll_*` corpus runs are hours-long by design; use `fastrun.py` with `--sequential` for early stopping |

## Folders

| folder | what is in it |
|---|---|
| `paper/` | the paper: one `.tex` and one `.pdf` |
| `code/` | `pdefactor/` the pipeline snapshot the layers were built on, with the learned layers in `pdefactor/learned/`; `s_interp_variant/` the separate interpolation variant |
| `tests/` | pytest: the layers, the "off equals the pipeline bit for bit" golden test, the interface pin |
| `benchmarks/` | experiment and gate scripts (`ll_*.py`), `runtime.json`, and `results/` (stored tables, logs and session data behind every number) |
| `claude/` | for Claude sessions: rules, status, map, session plans and reports (`claude/archive/`), the Phase 4 plan (`claude/notes/`), where each file came from (`claude/PROVENANCE.md`) |

**Important:** `code/pdefactor` is the pipeline version the layers were built on (main at an earlier commit plus the layers), not the current `main`; porting the hooks is open work (paper, ideas section). Do not install this branch and `main` into the same environment.
Glossary: *layer* = an optional learned component; *gate* = a pre-registered pass/fail test a layer must clear; *LOFO* = leave-one-family-out evaluation; *honesty rule* = the controller may only choose among options scored on data it did not tune on.
Other branches: `main` (the algorithm and its papers), `analytical`, `model-expansion`.
Licenses: code MIT ([`LICENSE`](LICENSE)), papers CC BY 4.0 ([`LICENSE-papers.md`](LICENSE-papers.md)); please cite via [`CITATION.cff`](CITATION.cff). Author: Flavio Pricoco.
