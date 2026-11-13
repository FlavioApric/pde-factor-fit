# STATUS (state at 2026-11-13)

## Adopted and on by default
Pipeline with the bundle CONJ_HALF, BRANCH_ARD (-> SPLIT_FINEST, PATH_CLASS, PATH_FULL, RAW_GOF_FINAL), per-bin bound clamp,
bootstrap that keeps copies dropping a bare split-off factor, SPLIT_CI and IDKER_FINAL. Each has an env switch
`PDEFACTOR_*` (`=0` disables).

## Results
- Large random-PDE benchmark (final, 2026-11-13; `benchmarks/bench_large.py`, table `claude/benchmark_tables/large.md`):
  300 independent random equations (F1-F5, 60 each), grid, noise 1 %, none used in development. 285 finished:
  pipeline 187 right + 88 equivalent = 96.5 % (Wilson 93.7-98.1), 0 false-confident (upper 95 % 1.0 %), 9 abstentions,
  1 crash (F4-10); weak SINDy 28.4 %, 204 false-confident; paired sign test p = 8e-59. 15 draws hit the 3 h limit
  (F4 12, F5 3); counting them as failures: 275/300 = 91.7 %.
- Final benchmark (30 inputs: 10 cases x grid 1 %, grid 5 %, 400 points 5 %): pipeline 30/30 right, 0 false-confident;
  weak SINDy 23, ensemble 19, SBR 20, PDE-FIND 4, BOP-DMD 1. Table: `claude/benchmark_tables/p8_final_v5.md`.
- 20 random equations not used in development: 12 right + 7 equivalent + 1 correct abstention, 0 false-confident
  (library-regression baselines: at most 6 right).
- Full test suite: 238 passed.

## Not adopted (code kept, switch off; reopen only with new evidence)
GROW_PAST, EPGP_REINTERP, FIT_GUARD / ALT_PRE: regressions on held-out families.

## Open
1. `two_pairs` keeps the true factors but is UNDECIDED (confluent relabel); UNDECIDED may be the correct honest answer.
2. BRANCH_ARD does not charge a factor with no excited branch (bare tau bias).
3. Beam, 400 points, one seed: 90 % interval covers 0.5 (honest miss).
4. Weights over the ambiguity of a shared zero mode; coloured (AR(1)) noise is in no suite; benchmark seeds share one field in
   the older tables (the paper uses independent fields); some constants are hand-set (LOG_BF_STRONG, CAP, z, snr_min).

## Layout change (2026-11-09)
Papers are flat files in `paper/` (`structure_A`, `structure_B`, `explained`, with `paper/figures/`); `src/` became `code/pdefactor/`; `analysis/exp` and the paper experiment scripts are in `code/experiments/`; repository tools in `code/tools/`; stored results in `benchmarks/out` and `benchmarks/data`; all markdown (including benchmark tables) in `claude/`. The graph of the repository is in `claude/graph/`, the inventory in `claude/INVENTORY.md`.
