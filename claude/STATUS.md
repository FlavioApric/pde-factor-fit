# STATUS of `ml-layers` (2026-11-07)

Pipeline pinned in `src/`: main at `eaa8f9c` (plus the layers). Current `main` is later (bundle T98-T103, split intervals, final raw-GOF).
Merge attempt: 3-way merge of `loop.py` conflicts in 7 hunks, `core/structfit.py` in 6; not done, because the verdicts must be re-gated on the merged code.

| layer | verdict | where |
|---|---|---|
| LB exact memo | go, on (`PDEFACTOR_LB_MEMO=0` disables) | `learned/memo.py`, `budget.py` |
| LB learned skip | no-go | `benchmarks/results/LB_REPORT.md` |
| V1 | no-ship; `Learned(validator="downgrade")` exists, does nothing without a model | `results/V1_REPORT.md`, `v1_gate_resid_p7.md` |
| L2b, L2c, L2d | no-go | `results/V1_REPORT.md`; L2c in `ll_l2c.py` |
| H0 | no-go | `learned/highk.py` |
| L0 | closed | `learned/expseeds.py` |
| C | not built; oracle table in `results/C_cprime_oracle_p7.md` | `learned/controller.py` (early code, off) |

## Open
1. Port the layer hooks to current main and re-gate (V1 first, then the C oracle sweep).
2. A trigger with resolution on false-confident runs (V1 flags 0/12 of the failures a rerun could fix).
3. Input-only validator for crashes, timeouts and out-of-class data.
4. N nulls were not re-run on the final pipeline.
5. Main-side issues seen by the layers: false-confident 9/80 on G test (earlier pipeline), `refine_factors` ZeroDivisionError, `bayes_split.raw_evidence` IndexError.

Tests: 106 passed on the learned and contract tests plus 24 passed after regenerating the golden file on Linux.
Long notes: `claude/notes/` (Phase 4 plan, S-LEARNED plan and handoff, written for the earlier setup; Windows paths there are historical).

## Completeness (2026-11-09)
The paper now covers every layer of the plan (21 pages): pipeline ML, P0 prerequisites, L0, L1, L2a-d, V0/V1, the controller C in full, L5, L6, differentiable core, build order, failure-mode table, acceptance protocol, test inventory.
All session plans/reports are in `claude/archive/sessions/`; the S-INTERP variant is in `variants/s_interp/`. `INVENTORY.md` on `main` lists every old file and its new place.

## Layout change (2026-11-09)
The paper is one flat file (`paper/ml_layers.tex`, 39 pp): the explained edition and the original pipeline note are now appendices of it (coverage checked). `src/` became `code/`; `variants/s_interp` became `code/s_interp_variant/` (+ notes in `claude/archive/s_interp_variant/`); scripts and results are flat in `benchmarks/`.
