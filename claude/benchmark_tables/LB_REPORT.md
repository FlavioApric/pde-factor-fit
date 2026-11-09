# S-LEARNED-LB — REPORT (feasibility stage, 2026-10-30)

Layer LB (speed / budget), opt-in via `Learned(budget=...)`. Plan: `PLAN.md` (this folder). Scope follows the
user decisions of 2026-10-30: feasibility only (a go / no-go / unclear verdict, final tuning later on the
final pipeline), accuracy before speed (the normal-use profile must harm 0 runs), and a separate fast
profile for training and screening runs that may harm up to 2 %.

## 1. Verdict

| part | verdict | evidence |
|---|---|---|
| **Learned skip, profile `exact`** (0 harm) | **no-go at this data size** | Cross-fitted over all 165 fit+cal runs, the largest λ with 0 harmed runs saves 0.2 % of runtime. On G test (51 runs, exact replay) it skips nothing: 0.0 % saved, 0 harmed. |
| **Learned skip, profile `fast`** (≤ 2 % harm) | **no-go at this data size** | CRC at α = 0.02 on the cal split (n = 44 < 49) cannot skip at all. Cross-fitted CRC (n = 165) saves 0.7 % at 2/165 harmed runs (conservative label). On G test it skips nothing. |
| **Exact memo** (stage `"modes"`) | **go** (exact; modest gain) | Bit-identical by construction and by test. 0 harmed in 47 G-test pairs, 10 null pairs, 10 named cases and 10 same-load timing pairs; 0 coefficient differences. Same-load paired timing (§5.2): total runtime ratio 0.928 [0.896, 0.948], per-run geometric mean 0.875 [0.817, 0.930]. |

Both profiles, as shipped (opt-in), on the same G-test rows: `exact` gives 0 harmed of 47 (95 % bound 6.2 %). `fast` was not run as a
separate arm. Its replay on the same 51 rows skips nothing, so it equals `exact` there (C2: replay of a
skip-free run is exact): 0 harmed, and the speed-up is the memo's alone (about 7 % total).

Why the learned skip cannot pay off now: the ceiling is low and the signal is weak.
- **Ceiling.** A perfect classifier skips every guarded step that leaves the state unchanged. It would save 17 % of total runtime on fit+cal (11 % median per run) and 14 % on G test (4 % median).
- **Signal.** `alternatives`, the largest guarded step, changes the state in 64 of 133 runs. `grow` changes it in 10 of 49 runs and `complex` in 14 of 52. Most of the time sits in steps that change the state in every run and are not optional (`decide`, `bootstrap`, `refine`, `split_layer`).
- **Data.** With 0 harm required, a skip rule needs both a separable signal and enough held-out runs to bound the harm. Neither holds at n = 165.

The layer stays opt-in and off by default. The code, the tests and a one-command retrain (§7) are ready, so on the final pipeline the decision is a rerun, not new work.

## 2. What was built

- **Step log, tightened `changed` bit** (`loop._fp`, `_Steps.mark`): a step is `changed` when the label, the
  factor strings, the coefficient tuples, the evidence, the pooled structures or the bounds differ before
  and after it (parent's fix, 2026-10-29). Metadata only; the off output is unchanged (golden test green).
- **Guards** before the optional steps `grow`, `recurse`, `complex`, `alternatives` (`loop._lb_skip`, depth 0
  only; children never consult the layer). Each guard records dimensionless features (`budget.features`,
  rule 8) and asks the model whether to skip; a skip is written into the note and into `LoopResult.lb`.
- **Profiles** (`Learned.budget`, validated in `learned/config.py`):
  - `True` / `"exact"`: model `learned/models/lb_exact.pkl`; λ by the zero-harm rule (`budget.zero_threshold`).
  - `"fast"`: model `lb_fast.pkl`; λ by conformal risk control at α = 0.02 (`budget.crc_threshold`,
    Angelopoulos et al. 2022), Learn-then-Test bound reported next to it; for training and screening only.
  - With no model file the layer is log-only: guards record and never skip, output equals off.
- **Calibration** (`ll_budget_fit.py --calib crossfit`, default): λ is set on out-of-family scores of every
  fit+cal run (each family scored by a model fit on the other four), because the cal split alone (n = 44)
  is below CRC's minimum of 49 at α = 0.02. Cross-conformal calibration holds its level approximately
  (about 2α in the worst case, Barber et al. 2021); the test split is the real held-out check.
- **Exact memo** (stage `"modes"` on controller C's `learned.memo.Memo`, through `runconfig.memo()`; one memo
  mechanism, agreed with C): the core's mode extraction and confluent test depend only on the sample, the
  noise and the mode-step options (`max_order`, `extra` are in the key), not on the bounds or structures,
  so every repeated core call on the same sample in one `run_loop` (grow, refine, re-runs) reuses them.
  P0 profiling found `confluent_test` at 80–90 % of core time. Any budget profile creates a `Memo` when
  none is active; `budget.MEMO = False` switches it off (used for the log-as-off training rows).
- **Scripts**: `ll_budget_corpus.py` (log-as-off rows with guard features, `lp_trace`, `resid`, a tripwire
  that reruns plain off on the first 10 rows, `--match` to pair with another session's off rows, pipeline
  sha per row), `ll_budget_fit.py` (fit, calibrate, LOFO replay, both profiles, `--retrain`),
  `ll_budget_harm.py` (paired harm check), `ll_budget_timing.py` (§5.2), `ll_budget_named.py`, `ll_budget_identity.py`,
  `ll_budget_profile.py` (P0).

## 3. Data (pipeline shas)

| file | pipeline | rows | labels |
|---|---|---|---|
| `analysis/exp/out/ll_S_fitcal_off.jsonl` (log-as-off, S fit 200–203, cal 207) | frozen copy of `6b065d1` | 50 | 18 FIT-COMPATIBLE, 3 UNDECIDED, 2 ID-KER, 26 TIMEOUT, 1 CRASH (known `refine_factors` ZeroDivision) |
| `analysis/exp/out/ll_G_fitcal_off.jsonl` (log-as-off, G fit 100–109, cal 120–123) | frozen copy of `6b065d1` | 140 | 70 FIT-COMPATIBLE, 15 ID-KER, 13 UNDECIDED, 30 TIMEOUT, 12 CRASH (known validate SVD LinAlgError) |
| `analysis/exp/out/ll_lb_G_test.jsonl` (lb arm, G test, matched to the shared off rows) | frozen copy of `0ec3186` | 55 | 42 FIT-COMPATIBLE, 5 ID-KER, 3 UNDECIDED, 2 TIMEOUT, 3 CRASH |
| `analysis/exp/out/ll_lb_N_test.jsonl` (lb arm, N test, matched to shared `ll_N.jsonl`) | frozen copy of `0ec3186` | 10 | 10 UNDECIDED |
| `analysis/exp/out/ll_lb_named.jsonl` (off + lb, named cases) | frozen copy of `0ec3186` | 20 | 9 FIT-COMPATIBLE, 1 ID-KER per arm |
| `analysis/exp/out/ll_lb_G_timing.jsonl` (off + lb side by side, G test 128–129, grid 0.05) | frozen copy of `0ec3186` | 20 | 9 FIT-COMPATIBLE, 1 ID-KER per arm |
| shared `D:\Larned layers\PDEFactorML\analysis\exp\out\ll_G.jsonl` (off arm, G test; S-LEARNED / H0) | frozen off code (the off output is bit-identical across branches while the golden test passes) | 55 matched | |

`src/` at `6b065d1` and `0ec3186` differ only in LB files (profiles, models, the HGB pipeline); the off
path is the same. Tripwire: 10 of 10 S rows and 10 of 10 G rows gave answers identical to plain off
(label, factor strings, coefficient reprs, evidence). Fitted values are provisional and tied to these shas.

## 4. Offline replay (fit / calibrate / LOFO, 165 runs with guard features)

Full tables: `fit_results.md` (cal-split calibration) and `fit_results_crossfit.md` (cross-fitted).

| profile | calibration | chosen | λ | harmed runs | saved (total) |
|---|---|---|---|---|---|
| exact | cal split (n = 44), LOFO replay | logistic | 0.029 | 5 / 165 in LOFO | 3 % |
| exact | cross-fitted (n = 165) | hgb | 7.8e-6 | 0 / 165 (95 % bound 1.8 %) | 0.2 % |
| fast | cal split (n = 44) | — | −1 (never skips; n < 49) | 0 | 0 |
| fast | cross-fitted (n = 165) | hgb | 1.5e-5 | 2 / 165 (CRC level 2 %) | 0.7 % |

The cal-split zero-harm λ overfits the 44 calibrate runs (5 harmed out-of-family), which is why the
shipped calibration is cross-fitted. The harm label is conservative (a skipped step that changed the
state counts as harm even if the final answer would have been the same, PLAN §2.1); the optional R2
reruns that would sharpen it were not run, since even the oracle ceiling is small.

## 5. Test split (G test, paired with the shared off rows)

### 5.1 Harm and gate (`ll_budget_harm.py`, `ll_gate.py --target runtime`)

| measure | value |
|---|---|
| pairs / compared (both finished) / both stopped | 55 / 47 / 5 |
| harmed (label or factor set differs from off) | **0 of 47**, one-sided 95 % bound 6.2 % |
| coefficient / interval differences beyond 1e-9 | **0** |
| TIMEOUT on off only (finished with lb) | 3 (F3 133 grid .01, F4 132 grid .01, F5 134 grid .05) |
| skips fired | 1 (`grow`, one run) |
| right-set / false-confident | 0.636 → 0.655; 7 → 7 |
| coefficient coverage (90 %) | 0.916 → 0.918 |
| runtime, on − off (paired, 95 % bootstrap CI) | −55 s [−88, −26]; median 154 → 153 s; per-run ratio median 0.77 |

The runtime row is **not** evidence for the layer by itself: the off rows were produced by another
session at a different machine load, and the one skip cannot explain a 23 % median ratio. §5.2 measures
it cleanly.

Replay of both models on the 51 lb rows where nothing was skipped (exact by C2): `lb_exact` and `lb_fast`
skip nothing, 0.0 % saved; oracle ceiling 13.9 % total, 3.9 % median.

### 5.2 Paired timing at equal load (off and lb side by side)

`analysis/exp/out/ll_lb_G_timing.jsonl` (frozen `0ec3186`): G test seeds 128–129, design grid 0.05, all
five families, arms off and lb run in the same pool (2 workers, arms interleaved per task), so load is
shared. 10 pairs, all 10 finished in both arms with the same label and identical factor strings; **no skip
fired in any lb run**, so the difference is the memo alone.

| family / seed | off (s) | lb (s) |
|---|---|---|
| F1 128 / 129 | 62.9 / 12.9 | 58.7 / 9.5 |
| F2 128 / 129 | 12.0 / 13.9 | 8.8 / 11.0 |
| F3 128 / 129 | 406.5 / 214.2 | 379.3 / 209.7 |
| F4 128 / 129 | 248.2 / 1110.3 (ID-KER) | 240.8 / 1040.7 (ID-KER) |
| F5 128 / 129 | 390.5 / 413.4 | 360.1 / 357.3 |

| measure | value (95 % paired bootstrap CI, 10 000 resamples) |
|---|---|
| per-run ratio lb / off, geometric mean | **0.875 [0.817, 0.930]** |
| total runtime ratio | **0.928 [0.896, 0.948]** (2885 s → 2676 s) |

So the memo saves about 7 % of total runtime (12 % per run on the geometric mean; small runs gain more in
relative terms) at zero harm. The CI excludes 1. n = 10 is small; the direction agrees with the named cases
(§6, ratio 0.92) and with the confounded G-test arm (§5.1).

## 6. Nulls and named cases

**Nulls** (`analysis/exp/out/ll_lb_N_test.jsonl`, lb arm, frozen `0ec3186`, matched to the shared
`ll_N.jsonl` off arm): 10 pairs (null seeds 315–319, grid and 400-point designs), 10 compared, 0 harmed
(95 % bound 26 %), 0 coefficient differences, 0 skips fired. Every run is UNDECIDED in both arms (false
confident 0 → 0). Total runtime 36 s → 26 s (these runs are short; same load caveat as §5.1).
`ll_gate.py --nulls` fails on these files with a key-sorting TypeError (designs mix `"grid"` and `400`),
in a script shared with the other layers, so it was not edited here; the null check above was done by hand
with the same pairing keys.

**Named cases** (`analysis/exp/out/ll_lb_named.jsonl`, off and lb run side by side by
`ll_budget_named.py`, frozen `0ec3186`): 10 of 10 have the same label and identical factor strings (the
coefficients are printed to full precision), 0 skips fired. 9 FIT-COMPATIBLE, Schrödinger ID-KER in both.
Total runtime 1451 s → 1333 s (ratio 0.92). The long cases gain most (telegraph 515 → 468 s,
transport + diffusion 409 → 372 s, beam 245 → 220 s), which fits the memo, since those cases call the core
repeatedly on the same sample.

## 7. Retrain recipe (one command)

```bash
.venv/Scripts/python.exe analysis/exp/ll_budget_fit.py --retrain --workers 6 --gp-cache "D:/Larned layers/PDEFactorML/analysis/exp/cache"
```

It reruns the log-only corpus rows of S and G fit+cal on the current pipeline through
`ll_budget_corpus.py` (resumable; tripwire on), fits both profiles with cross-fitted calibration, writes
`src/pdefactor/learned/models/lb_exact.pkl` and `lb_fast.pkl` (git sha in the model's `meta`) and the
tables to `sessions/LEARNED/LB/fit_results.md`. To re-evaluate on G test against an existing off arm:

```bash
.venv/Scripts/python.exe analysis/exp/ll_budget_corpus.py --corpus G --split test --learned lb --model src/pdefactor/learned/models/lb_exact.pkl --match <off rows>.jsonl --out analysis/exp/out/ll_lb_G_test.jsonl
```

then `ll_budget_harm.py <off rows> analysis/exp/out/ll_lb_G_test.jsonl --arm lb` and
`ll_gate.py <off rows> analysis/exp/out/ll_lb_G_test.jsonl --arm lb --target runtime`.

## 8. Tests

`tests/test_learned_budget.py` (18 tests): the changed bit sees a coefficient change at the same factor
count; NaN-stable fingerprints; log-only mode is off; a never-skip model is off; a skip of an unchanged
step is exact (C1) and the offline replay matches it (C2); children never consult the layer; CRC rule,
monotone loss, n ≥ 49, agreement with the validator's risk threshold; LTT stricter than CRC; zero-harm
rule and its bound; features dimensionless and NaN-safe; the core memo is exact; the memo is released
after the call; the harm check counts; the profiles. Full suite: 214 passed; the 6 errors are the known
main bug in `tests/test_aggregate_cluster.py` (IndexError in `aggregate.py:198`), untouched. The off golden
test (`tests/test_learned_off.py`) is green.

## 9. Open points

- **Memo default-on.** §5.2 shows a real gain (about 7 % total, CI excludes 1). Proposal to S-LEARNED:
  the `"modes"` memo runs by default, independent of `budget` (it changes no output, so off stays
  bit-identical). That is the parent's decision, and the golden test would then need to run with it on.
- `ll_gate.py --nulls` and its key sort fail on mixed design types (`"grid"` vs `400`); a shared script,
  left for its owner.
- **On the final pipeline**: rerun §7. The skip only becomes worth it if the oracle ceiling grows (for example
  if `bootstrap` or `decide` became optional) or the corpus grows enough to bound harm below 1 %
  (0 of 300 held-out runs gives 1 %).
- **Known main bugs seen in the corpus** (not fixed here): `refine_factors` ZeroDivisionError (S F5 201),
  validate SVD LinAlgError (12 G rows), `test_aggregate_cluster` IndexError.
- Fresh-context review of this layer is still to do (gate criterion 6).
