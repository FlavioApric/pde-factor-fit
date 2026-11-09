# QUEUE t96 (branch t96-v01-guard): A/B of the T96 fit guard with PATH_CLASS

Candidate arm = `PDEFACTOR_PATH_CLASS=1 PDEFACTOR_FIT_GUARD=1` (tag `t96`). The two T96 speed-ups
(`refine_raw._profile_bins` by bincount, vectorised `_basis_groups`) are always on and bit-identical
(`tests/test_t96.py`); `PDEFACTOR_BASIS_FAST=0` restores the old basis loop if a check is wanted.
Optional third arm `t96pre` adds `PDEFACTOR_ALT_PRE=1` (refined alternatives also from the pre-regroup
posterior; on F3-3 it does not replace PATH_CLASS, see THEORY_TO_ALGO row T9x-t96).

Run everything from the worktree so `pdefactor` resolves there (check `pdefactor.__file__`), one suite at a time.

```sh
cd C:/Users/flavi/pdef-wt/t96-v01-guard/PDEFactorML
export PYTHONPATH="C:/Users/flavi/pdef-wt/t96-v01-guard/PDEFactorML/src;C:/Users/flavi/pdef-wt/t96-v01-guard/PDEFactorML"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export PDEFACTOR_PATH_CLASS=1 PDEFACTOR_FIT_GUARD=1
PY=D:/PDEFactorML/.venv/Scripts/python.exe
$PY -c "import pdefactor; print(pdefactor.__file__)"   # must be under t96-v01-guard

# references (read-only copies from the main checkout, so --ref finds them)
mkdir -p benchmarks/out/micro
for f in heldout_v4 heldout_t94 conjugate_v4 conjugate_t94 edge_v3 draws_fc_v0 draws_fc_t94; do
  cp -n D:/PDEFactorML/benchmarks/out/micro/$f.jsonl benchmarks/out/micro/ 2>/dev/null; done
for F in F1 F2 F3 F4 F5; do cp -n D:/PDEFactorML/benchmarks/out/e13_v4_$F.jsonl benchmarks/out/; done

# 1. held-out (grid first, then 400)
$PY benchmarks/micro.py heldout --tag t96 --ref v4 --workers 3 --sampling grid  > benchmarks/out/micro/heldout_t96.log 2>&1
$PY benchmarks/micro.py heldout --tag t96 --ref v4 --workers 3 --sampling 400   > benchmarks/out/micro/heldout_t96_400.log 2>&1
$PY benchmarks/micro.py heldout --tag t96 --ref t94 --report

# 2. conjugate
$PY benchmarks/micro.py conjugate --tag t96 --ref v4 --workers 3 > benchmarks/out/micro/conjugate_t96.log 2>&1
$PY benchmarks/micro.py conjugate --tag t96 --ref t94 --report

# 3. edge (holds P8 TPD 400 5 % s0, one of the two T94 rows)
$PY benchmarks/micro.py edge --tag t96 --ref v3 --workers 3 > benchmarks/out/micro/edge_t96.log 2>&1

# 4. fc draws (F4-209 400 5 % is the slow one; its reference took 5652 s, STALL = 10800 s)
$PY benchmarks/micro_draws.py fc --tag t96 --ref t94 --workers 3 > benchmarks/out/micro/draws_fc_t96.log 2>&1

# 5. E13 F1-F5, 4 seeds, 1 % (bootstrap 0 as e13_v4), one family per process
for F in F1 F2 F3 F4 F5; do
  $PY analysis/exp/e13_random_pdes.py --families $F --seeds 0 1 2 3 --noise 0.01 --methods pipeline \
      --out benchmarks/out/e13_t96_$F.jsonl > benchmarks/out/e13_t96_$F.log 2>&1
done
# compare with e13_v4_F*.jsonl (and the T94 PATH_CLASS-only rows: scratchpad e13_t94.jsonl)

# 6. single draws: F4-128 grid 5 % (t95 case) and the T94 rows
$PY benchmarks/micro_draws.py --one '["F4",128,"grid",0.05]'
$PY benchmarks/micro_draws.py --one '["F2",2,"grid",0.01]'
$PY benchmarks/micro_draws.py --one '["F3",3,"grid",0.01]'
```

Expected from the T96 single-draw checks (E13 harness, bootstrap 0): F2-2 grid 1 % right (guard refuses
the xi^3 pair: Schwarz -4149.0 vs -4132.1), F3-3 grid 1 % right (313 s vs 417 s at T94), see THEORY_TO_ALGO
T9x-t96 for F4-128. Adopt only if heldout / conjugate / edge / fc outcomes are not worse than v4 and E13 is
not worse than v4 in false-confident rows.
