# S-LEARNED — sync record (B0)

**Source:** the `D:\` repo, path `PDEFactorML/`, commit **66a5064** ("Refinement evidence on grids computed per DFT bin pair"; its parent 1250454 adds V0 and the V0.1-triggered growth). This was HEAD of `git -C D:/ log -- PDEFactorML` on 2026-10-29. The files were extracted with `git archive 66a5064 PDEFactorML`; nothing was written in `D:\`.

**Rule.** Main's file wins, except where this branch (the cloud session S-PHASE4-ML, final state) is newer. Main merged an earlier state of that branch, so these files are kept from this branch:
- `src/pdefactor/learned/calibrate.py` (Venn–Abers);
- `src/pdefactor/learned/validator.py` (review fixes: standardisation, Ledoit–Wolf, ±inf);
- `src/pdefactor/learned/expseeds.py` (focal loss);
- `analysis/exp/e12_l0_seeds.py` (thread option), `e13_corpus.py`, `e14`–`e16`;
- `sessions/S-PHASE4-ML/*` (final PLAN, REPORT, results);
- `SESSIONS.md` (main's text plus the S-PHASE4-ML row);
- `tests/test_learned.py`: this branch's tests, with main's cross-platform tolerance hunk on the golden test.

Files that differed only in line endings were left untouched.

**Taken from main (sha256 prefix of main's file at 66a5064):**

| file | sha256 (16) |
|---|---|
| `src/pdefactor/loop.py` | `b4a7a8f86c512f07` |
| `src/pdefactor/refine_raw.py` | `c891f6e3056b6d8a` |
| `src/pdefactor/core/structfit.py` | `8015c3e11771bd35` |
| `src/pdefactor/simulator.py` (new here) | `65633ab608ad0232` |
| `src/pdefactor/validate.py` (new here) | `d1685705ce30e059` |
| `analysis/exp/e13_random_pdes.py` (new here) | `729b51992889e544` |
| `analysis/exp/e13_summary.py` (new here) | `12c460e5317dcfbf` |
| `analysis/THEORY_TO_ALGO.md` | `b5e1e759334a7064` |
| `tests/test_general.py` | `bd3b6194d79b7c32` |
| `tests/test_refine_grid.py` (new here) | `61b578617ea7f895` |
| `tests/test_simulator.py` (new here) | `67f86c1edb4eb796` |
| `tests/test_validate.py` (new here) | `c1def428450c1960` |

**Re-sync later:** take these files again from the newer main commit, then re-apply the S-LEARNED hooks. The hooks are every line in `loop.py` that mentions `learned`, plus the `scale=` argument of `coef_draws`.

## Re-sync 2026-10-31 (P7a): main eaa8f9c

**Source:** `D:\` repo HEAD **eaa8f9c** ("P8 SINDy arm"), path `PDEFactorML/`, read with `git archive`; nothing written in `D:\`. Files: everything changed since 125b1f2 (`git diff --stat 125b1f2 HEAD -- PDEFactorML`), except `EXPLAINED/` and `benchmarks/out/`. None of them is a learned-owned file, and every one except `loop.py` was identical to main 125b1f2 on this branch, so main's file was taken as is.

| file (main eaa8f9c) | sha256 (16) |
|---|---|
| `HANDOFF.md` | `6a313f00c91f36a2` |
| `analysis/ML_INTEGRATION.md` | `dc931d1a951fc6a0` |
| `analysis/THEORY_TO_ALGO.md` | `bb985f10406ca317` |
| `analysis/exp/gp_cache.py` | `5fe2ba6d77b502d3` |
| `benchmarks/bench.py` | `cf5f162169c9c1b3` |
| `benchmarks/bench_e2e.py` | `d063a66d967245fa` |
| `benchmarks/data/INDEX.md` | `708e05a64870e109` |
| `benchmarks/data/micro/heldout_pb1.jsonl` | `6e5f6f1e6de9f4c8` |
| `benchmarks/data/micro/intervals_pb1.jsonl` | `66448848b3d41b31` |
| `benchmarks/data/micro/intervals_v1.2026-10-30.jsonl` | `5e6a097eb659f6e8` |
| `benchmarks/micro.py` | `18526dd4074ab5b2` |
| `benchmarks/micro_draws.py` | `caefe11a412173ed` |
| `src/pdefactor/bayes_split.py` | `50496391f1c618f9` |
| `src/pdefactor/interp/reinterp.py` | `bdf8c9a98825eff6` |
| `src/pdefactor/loop.py` | `00e0faffa7a8b5e4` |
| `src/pdefactor/raw_gof.py` | `fbfcb8690021d886` |
| `src/pdefactor/refine_raw.py` | `6f6458168584d29f` |
| `tests/test_bench_sigma.py` | `a1e102d9175f629c` |
| `tests/test_p3_grow.py` | `da2dde97484bdc1d` |
| `tests/test_p4_reinterp.py` | `ca50d199eff6f58f` |
| `tests/test_refine_grid.py` | `6c96147fa9d0c7c1` |
| `tests/test_t77.py` | `3fa40bbfc6d2724f` |
| `tests/test_t86.py` | `c99821f1bdac0381` |

**loop.py:** 3-way merge (base main 125b1f2, ours ll-sync da223f4, theirs main eaa8f9c), CRLF kept; result sha256 `22ffdb9528911b51`. Two conflicts, both resolved by keeping both sides: `import time` (ours) + `import os` (main); the L2c block after `bootstrap` (ours) followed by main's T88 raw-GOF block. Against main the only removed lines are the 3 hooked ones (`learned=None` in the signature, its docstring, the H0 `refine_factors` call). Hooks re-applied: `learned=None` argument, `active(learned)`, `_Steps` log, `_highk` (H0), `l2c_data` and the L2c interval block. Note: no `scale=` argument of `coef_draws` exists on this branch (L2c goes through `scale_intervals`), so there was nothing to re-apply there.

**Off golden:** regenerated with `tests/data/make_learned_off_golden.py` (same venv, 1 thread). The same script run on main eaa8f9c (with `learned=` dropped from the call) gives a byte-identical json: off == main bit for bit. sha256 `11cd3e6debd5c6bf`.

**test_learned_off.py:** now deep-copies the inputs per run. Main's run_loop (eaa8f9c) mutates its inputs on the scattered path: a second call on the same `heat-400-0.05` dict gives `0.30124865617114` instead of `0.301248661703562`, on main and here alike.

**Tests (PYTHONPATH=src, 3 processes):** test_learned_off (after the fix), test_learned, test_ml_contract: 43 passed; test_learned_layers, test_learned_resid, test_t86, test_bench_sigma, test_p4_reinterp: 22 passed, 1 skipped; test_t77, test_refine_grid, test_p3_grow: 24 passed. `test_runconfig` does not exist on main or here. Full suite not run.
