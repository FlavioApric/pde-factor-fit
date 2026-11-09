# Integrating the learned layers onto current main

The learned-layers branch (`D:\Larned layers`, branch `learned-layers`) has base commit `8420846`, but its B0 commit (266e5ca) copied main's PDEFactorML files up to `66a5064` (sha256 per file in its `sessions/LEARNED/SYNC.md`). So 6cae4a5, 9e8b42e, 1250454 and 66a5064 are already in it. Missing as of 2026-10-30: 91f3581, 0390fd0 and 867dcc0 (they change outputs), c3457c9 and 66b5893 (speed only), and anything later. Its "all layers off" golden files and gate tables therefore describe main at 66a5064. Its plan: finish the on/off verdicts on that base (still a valid "does it help"), then sync once to main, regenerate the off golden file and re-gate only the layers that passed. This note lists what changed and the checklist for rebasing and re-gating. Nothing here merges anything; the user decides that.

## What changed on main since 8420846

| commit | change | outputs change? | layers it touches |
|---|---|---|---|
| 6cae4a5 | v2.13 generalisation: growth in m or dx, merges and duplicates for any order, branch points vs confluence (T51–T60) | yes | all (factors, labels) |
| 9e8b42e | random-PDE simulator by family (P0.3), E13 abstention-aware scoring | no (new tools) | corpora: use `simulator` F1–F5 |
| 1250454 | V0 diagnostic battery (`validate.py`), V0.1-triggered degree growth (T61), E13 data-equivalent scoring | yes | V1 (overlaps V0), L2d (`PRED_LOGP`) |
| 66a5064 | grid evidence per DFT bin pair (exact) | no (speed) | — |
| 91f3581 | refinement-stage merges, conjugate-closed splits, Occam per product (T63–T65) | yes | C, L2b, V1 |
| 0390fd0 | same-model alternatives skipped (T66) | yes | C |
| c3457c9 | core `confluent_test` by VarPro + LM (T67), same decisions 86/86, ~100× faster | decisions no; coefficients differ in the ~7th digit (not bit-identical) | LB: timeouts drop; off golden must be regenerated |
| 867dcc0 | same-model signature on the product (T68); confluent bins re-checked on final factors (T69) | yes (beam pair, damped beam label) | C, L2b, V1 |
| 66b5893 | grid evidence batched (equal to the reference to rtol 1e-8, 4×); one process per benchmark input; `benchmarks/micro.py` suites | decisions no; refined coefficients differ in the ~7th digit (not bit-identical) | all runners; off golden must be regenerated |
| e1fb9ae | same-family split tie rule (T70); complex split checked against the refined unsplit real factor (T71); every scored / pooled alternative refined, `ALT_TOP = None` (T72); confluent re-check on the product of the final factors (T73); bare-mention tie rule `_beats`, `LOG_BF_BARE` (T74); grid bootstrap of the refined estimator (T75, narrower grid intervals); `tests/test_ml_contract.py` | yes (beam 5 %, damped beam, labels) | C (ALT_TOP knob kept), L2b, V1 |

## Interfaces the layers use, as they are now on main
- Core: `analyze_structured(...)`, `extract_modes_ic(..., seeds=)` and `SEED_PROVIDER` (L0 hook, unchanged), `confluent_test` (same signature).
- Loop: `run_loop(samples, t, x, sigma, pis=None, *, bounds, refine, grow, ...)`; `LoopResult.note` is now stored in benchmark rows (`note` field), which gives a per-input trace of the loop's decisions.
- New in main that a layer may reuse instead of re-implementing: `validate.py` (V0 battery, `predictive_bins`, `_log10sf`), `simulator.py` (families F1–F5), `loop._supports` (same-model signature), `loop._relabel_branch_points`.
- Benchmark runner: `bench_e2e._run_pool(todo, out, workers)` now runs one process per input with a per-input timeout (`STALL`), so a crash or hang costs one input. `bench_e2e.py --one '[[case, noise, sampling, seed], [methods]]'` runs a single input.

## Rebase and re-gate checklist
1. Rebase `learned-layers` onto current main (or merge main into it); resolve conflicts in `loop.py` first, the file that changed most.
2. Regenerate every "all off" golden file from the rebased code, and check it against main: off must equal main bit for bit.
3. Rerun the gate corpora on the rebased code. Old gate tables are void, because the reference pipeline changed (labels on beam and damped beam, splits, growth).
4. Use the micro-suites (`benchmarks/micro.py`, at most 15 inputs each, aimed at one problem) for quick on/off checks, and the full corpora only for the final gate.
5. Theory rows stay prefixed `LL-T<n>`; main uses T1–T76 (T77 next; T76 is off by default).
6. Accuracy before speed: a layer may only make the pipeline faster when it is exact (same decisions); LB at 0 % harm.

Note (2026-10-30, from the learned-layers session's check): "speed only" on main means the same decisions (labels, structures, supports), not bit-identical numbers. Floating-point order and optimiser paths move refined coefficients around the 7th digit, so any layer that relies on bit-identical off output must regenerate its golden file at the sync.

## Added 2026-10-30 (main handoff)
| commit | change | outputs change? | layers it touches |
|---|---|---|---|
| 125b1f2 | T76 per-bin amplitude prior scale, behind `refine_raw.TAU2_PER_BIN` / env `PDEFACTOR_TAU2_PER_BIN` (default off); new `_basis_groups`, `_grid_spectrum(groups=)`; `_basis` signature unchanged | no (off by default) | none while off; with it on, every evidence value changes |
| 435b048 | V0.1 `predictive_bins`: exponential columns scaled per mode (growing modes no longer crash the SVD) | no where nothing overflowed; crashes become results | V1 (features from V0.1), all corpora (the 25 crashed runs can be rerun) |

Main handoff for the next session: `HANDOFF.md` (repository root of PDEFactorML).
