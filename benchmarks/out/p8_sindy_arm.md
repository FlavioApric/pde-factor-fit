# P8 SINDy arm (2026-10-31)

Cells: 10 synthetic cases x {grid 1 %, grid 5 %, 400 points 5 %}, seed 0 (30 inputs). "right" = factor_set.
The SINDy rows are reused from run 6 (`e2e_run6.jsonl`): the inputs are unchanged (FIELD_SEED off), and
the only input fix since (complex-field noise std, `bench.CPLX_SIGMA`) leaves all 45 Schrödinger grid
baseline rows identical in factor_set / struct_ok (`p8_sindy_schrodinger_cplxsigma.jsonl`).
The pipeline row is run 6 (old reference); the P8 pipeline and pipeline + ML arms are still to run.

| method | grid 0.01 | grid 0.05 | 400 0.05 | total right | struct ok |
|---|---|---|---|---|---|
| pipeline (run 6) | 10/10 | 8/10 | 8/10 | 26/30 | 26/30 |
| pdefind | 1/10 | 0/10 | 3/10 | 4/30 | 11/30 |
| weak_sindy | 9/10 | 6/10 | 8/10 | 23/30 | 21/30 |
| ensemble_sindy | 8/10 | 6/10 | 5/10 | 19/30 | 20/30 |
| sbr_sindy | 8/10 | 6/10 | 6/10 | 20/30 | 20/30 |
| bopdmd | 1/10 | 0/10 | 0/10 | 1/30 | 1/30 |
