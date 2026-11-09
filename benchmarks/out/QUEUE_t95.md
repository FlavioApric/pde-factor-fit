# QUEUE t95 (branch t95-f4128): A/B of T9x-t95, `PDEFACTOR_GRID_SMOOTH_GOF=1`

Rule: on a single real noisy grid with white sigma, a final FIT-COMPATIBLE whose reported factors leave smooth
residual structure in the excited band (validate.smooth_gof_log10p, combined log10 p < -3) becomes UNDECIDED.
It changes only the final label (factors unchanged), so the grid rows of every suite can also be checked
offline on stored factors; the reruns below confirm it end to end. Run from
`C:/Users/flavi/pdef-wt/t95-f4128/PDEFactorML`, one process at a time, with

    set PYTHONPATH=C:/Users/flavi/pdef-wt/t95-f4128/PDEFactorML/src;C:/Users/flavi/pdef-wt/t95-f4128/PDEFactorML
    set OMP_NUM_THREADS=1 & set MKL_NUM_THREADS=1 & set OPENBLAS_NUM_THREADS=1
    set PDEFACTOR_GRID_SMOOTH_GOF=1

1. fc rescore (no rerun, ~1 min; expected: F4-128 -> UNDECIDED / abstain, false-confident 1 -> 0 with EQUIV_DF):

       set PDEFACTOR_EQUIV_DF=1
       D:/PDEFactorML/.venv/Scripts/python.exe benchmarks/micro_draws.py fc --rescore cand1 --tag t95 --ref-dir D:/PDEFactorML/benchmarks/out/micro

2. fc rerun, grid inputs only (pipeline; F4-128 alone took 528 s here):

       D:/PDEFactorML/.venv/Scripts/python.exe benchmarks/micro_draws.py fc --tag t95run --ref cand1 --ref-dir D:/PDEFactorML/benchmarks/out/micro --design grid --workers 1

3. heldout (expected: no change; offline check of the stored t94/cand rows: every grid FIT-COMPATIBLE row >= -0.39):

       D:/PDEFactorML/.venv/Scripts/python.exe benchmarks/micro.py heldout --tag t95 --ref t94 --sampling grid --workers 1

4. conjugate (expected: no change on the real grid rows; schrodinger grid is complex, the rule is not applied):

       D:/PDEFactorML/.venv/Scripts/python.exe benchmarks/micro.py conjugate --tag t95 --ref t94 --sampling grid --workers 1

5. E13 rescore (benchmark scoring of the stored E13 v4 rows; offline: no grid FIT-COMPATIBLE row fires; F3-3,
   the remaining false-confident, scores -2.78 and is NOT caught):

       set PDEFACTOR_EQUIV_DF=1
       D:/PDEFactorML/.venv/Scripts/python.exe analysis/exp/e13_summary.py D:/PDEFactorML/benchmarks/out/e13_v4.jsonl

   (e13_summary has no label rescore; the label rule on E13 rows needs the pipeline rerun with the switch on.)

Pass criterion: no right / equivalent grid row turns UNDECIDED (check the `smooth_gof` field of the rescored
rows: a right row keeps category "right" in the scoring even when its label is downgraded), and the
false-confident count does not rise.
