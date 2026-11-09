# QUEUE t83b — A/B of T98 + T99 (finest exact split), for the lead

Branch `t83-two-pairs`. Switches (all default off; off == main 6c0f34a):
- `PDEFACTOR_CONJ_HALF=1`, `PDEFACTOR_BRANCH_ARD=1` (T98, unchanged).
- `PDEFACTOR_SPLIT_FINEST` (T99): defaults to the value of `PDEFACTOR_BRANCH_ARD`, so arm A below has it on.
  An exact split (T80, same product to rounding) is repeated until no factor splits exactly any more.

Run from `C:/Users/<user>/pdef-wt/t83-two-pairs/PDEFactorML` with
`PYTHONPATH=<wt>/PDEFactorML/src;<wt>/PDEFactorML`, `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`.
Reference = `heldout_t94`, `conjugate_t94` (main) in `benchmarks/out/micro/` (already used by the t83 arm).

## Arm A (all on)

    set PDEFACTOR_CONJ_HALF=1
    set PDEFACTOR_BRANCH_ARD=1

1. two_pairs grid 1 % and 5 %, seed 0 (> 20 min per input):

       python benchmarks/bench_e2e.py --cases two_pairs --samplings grid --noises 0.01 0.05 --seeds 0 --methods pipeline --workers 1 --out benchmarks/out/two_pairs_t83b.jsonl

2. held-out suite:

       python benchmarks/micro.py heldout --tag t83b --ref t94 --workers 1

3. conjugate suite:

       python benchmarks/micro.py conjugate --tag t83b --ref t94 --workers 1

## Arm C (optional: the new rule alone, on main's evidence)

    set PDEFACTOR_SPLIT_FINEST=1   (CONJ_HALF and BRANCH_ARD unset)

       python benchmarks/micro.py conjugate --tag t83bfin --ref t94 --workers 1 --sampling grid

Adopt only if two_pairs improves and heldout + conjugate do not regress (GOLD RULE).
Look at: beam grid rows (the split pair (tau -+ 0.300 i xi^2), note "repeated to the finest exact split" where the
ARD score picked tau (tau^2 + c xi^4), then "redundant factor(s) dropped by the split layer"); two_pairs 1 % must keep
(tau -+ 0.30 i xi^2)(tau + 0.19 -+ 0.10 i xi^2) (label expected UNDECIDED, T69, separate item).
