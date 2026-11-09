# QUEUE t83 — A/B of PDEFACTOR_CONJ_HALF + PDEFACTOR_BRANCH_ARD (T98), for the lead

Branch `t83-two-pairs`. Two switches, both default off (off == main 6c0f34a):
- `PDEFACTOR_CONJ_HALF=1`: complex-coefficient rerun of a real field on the half plane kappa > 0, reports lcm(A, conj A).
- `PDEFACTOR_BRANCH_ARD=1`: model-comparison scores (refine_factors logev) with one prior scale per root branch in excited bins (grid path only).
CONJ_HALF alone finds the true two_pairs factors but the per-bin evidence then reverts the split; the pair is meant to be
tested together (arm A). Arm B (BRANCH_ARD alone) isolates the evidence change, which touches every grid input.

Run from `C:/Users/flavi/pdef-wt/t83-two-pairs/PDEFactorML` with
`PYTHONPATH=<wt>/PDEFactorML/src;<wt>/PDEFactorML`, `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`.
Reference = `heldout_t94`, `conjugate_t94` (main): copy those jsonl files into `benchmarks/out/micro/` of the worktree first.
two_pairs grid takes > 20 min per input (main: ~25 min with bootstrap).

## Arm A (both switches on)

    set PDEFACTOR_CONJ_HALF=1
    set PDEFACTOR_BRANCH_ARD=1

1. two_pairs grid 1 % and 5 %, seed 0:

       python benchmarks/bench_e2e.py --cases two_pairs --samplings grid --noises 0.01 0.05 --seeds 0 --methods pipeline --workers 1 --out benchmarks/out/two_pairs_t83.jsonl

   OFF arm for 5 % (not in the micro suites): same command with both env vars unset, `--out benchmarks/out/two_pairs_t83off.jsonl`.

2. held-out suite:

       python benchmarks/micro.py heldout --tag t83 --ref t94 --workers 1

3. conjugate suite:

       python benchmarks/micro.py conjugate --tag t83 --ref t94 --workers 1

## Arm B (only PDEFACTOR_BRANCH_ARD=1), if arm A regresses anything on the grid rows

       python benchmarks/micro.py heldout --tag t83ard --ref t94 --workers 1 --sampling grid
       python benchmarks/micro.py conjugate --tag t83ard --ref t94 --workers 1 --sampling grid

Adopt only if two_pairs improves and heldout + conjugate do not regress (GOLD RULE).
Look at: the notes "complex-coefficient run on the half plane" and "the split over C is not kept"; the equation for
two_pairs grid should be (tau -+ 0.30 i xi^2)(tau + 0.19 -+ 0.10 i xi^2). Expected label still UNDECIDED: the confluent
bin kappa = +-1 lies between the two pairs and the T69 relabel criterion (roots within 4/T at < half the |kappa|) fails
(3 of 5) at T = 2; that is a separate open item.
