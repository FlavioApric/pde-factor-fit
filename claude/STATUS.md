# STATUS (state at 2026-11-07)

## Adopted and on by default
Pipeline with the bundle CONJ_HALF, BRANCH_ARD (-> SPLIT_FINEST, PATH_CLASS, PATH_FULL, RAW_GOF_FINAL), per-bin bound clamp,
bootstrap that keeps copies dropping a bare split-off factor, SPLIT_CI and IDKER_FINAL. Each has an env switch
`PDEFACTOR_*` (`=0` disables).

## Results
- Final benchmark (30 inputs: 10 cases x grid 1 %, grid 5 %, 400 points 5 %): pipeline 30/30 right, 0 false-confident;
  weak SINDy 23, ensemble 19, SBR 20, PDE-FIND 4, BOP-DMD 1. Table: `benchmarks/p8_final_v5.md`.
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
