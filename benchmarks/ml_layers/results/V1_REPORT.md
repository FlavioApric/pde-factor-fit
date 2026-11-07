# S-LEARNED-V1 — feasibility REPORT: corpus I, V1 (learned validator), L2b (calibrated P(top))

Scope (user, 2026-10-30): feasibility verdicts only, not final tuning. Each layer gets go / no-go / unclear,
with an effect size, a paired bootstrap CI and n. Both layers are report-only: they never change a label,
factor, interval, structure or weight (`tests/test_learned_v1.py::test_flags_on_change_only_the_report`;
`tests/test_learned_off.py` stays bit-identical with every layer off). So the gates are computed offline on
off-arm corpus rows. Verdicts are on this branch's base (3071bde). They do not include main's later
output-changing commits 91f3581, 0390fd0 and 867dcc0.

## Verdicts

| layer | verdict | effect [95 % paired bootstrap CI] | n |
|---|---|---|---|
| V1 failure score (injected vs clean) | **go (feasible); not shippable yet** | LOFO AUROC 0.900 [0.825, 0.975] vs V0 0.681; V1 − V0 = **+0.219 [+0.078, +0.289]**. On FIT-COMPATIBLE runs only (the confident case): 0.759 vs 0.515, **+0.244 [+0.083, +0.359]**. On fresh base draws (level 1, seeds 402/403): 0.85 vs 0.70 | 49 clean, 92 scored injected (28 base draws), 5 folds |
| V1 at α = 0.05 (conformal operating point, ship gate PLAN 3.5) | **unclear: cannot be evaluated at this n** | — | < 19 clean cal rows per fold, so p ≥ 1/(n_cal+1) > 0.05 and nothing can flag |
| V1 wrong-set flag (target b) | **unclear: cannot be evaluated at this n** | flags every run (false flag 1.00 on every fold): with < 9 calibration positives the risk-control threshold is the floor, the same artefact as α = 0.05 | 1–9 positives per fold (all-sources run) |
| L2b calibrated P(top), y = right or equivalent | **no-go** | best ΔBrier vs raw −0.032 [−0.073, +0.007] (logit-features); temperature −0.031 [−0.067, +0.003]; every arm worse than raw on F1 | 94 scored G+S rows + 30 CRASH/TIMEOUT |
| L2b, y = right only | **no-go** (fails every-fold rule) | ΔBrier −0.134 [−0.216, −0.049] (temperature), but worse than raw on F1 (Brier 0.233 vs 0.120) | same |

All V1 CIs use a paired **cluster** bootstrap over base draws (seeds) within each family. 21 of the 28
injected rows per family are variants of one draw (seed 400), so a row bootstrap would be too narrow.

V1 reading:
- The learned score separates injected failures from clean runs better than V0's omnibus test, and the CI
  excludes 0 in the primary configuration. This also holds on FIT-COMPATIBLE runs only. There, V0 is at
  chance (0.515), and these runs are where a failure goes unseen.
- The label one-hot is a legitimate run-time input. Part of the all-runs AUROC is V1 reading the pipeline's
  own UNDECIDED / ID-KER output: injected rows are 54 % FIT-COMPATIBLE, clean rows 82 %.
- The headline is draw-specific. In each family, one base draw (seed 400) supplies 21 of the 28 injected
  rows, and those rows score higher than fresh draws: at level 1, V1 gives 0.96 on draw 400 and 0.85 on
  draws 402/403 (V0: 0.80 vs 0.70). The held-out family is never in training, so this is draw-to-draw
  variance, not leakage. **Take about 0.85 as the estimate for unseen draws.**
- The residual diagnostics help:
  - without them, V1 − V0 = +0.150 [+0.004, +0.218];
  - B1 (V0 plus the resid statistics, Bonferroni-combined min-p, no learning) gives +0.125 [−0.045, +0.211];
  - on the base-draw control alone (14 clean rows), V1 − V0 = +0.106 [−0.062, +0.248]: unclear, CI too wide
    at n = 14.
- The ship gate (detection at a 5 % false alarm, per LOFO fold) needs at least 19 clean calibration rows per
  fold. About 100 clean, same-pipeline, 5 %-noise grid rows (20 per family, fresh draws) would make it
  evaluable.

L2b reading: raw P(top) is **saturated**. It is ≥ 0.999 on 95.8 % of the scored rows, so it has no
resolution. Raw Brier ≈ 1 − the base rate, so raw is overconfident by about 0.21 (right or equivalent) and by
about 0.40 (right). A calibrator that sees only P(top) can learn only a base rate, and base rates differ by
family: right or equivalent is 1.00 on F1, 0.77 on F2, 0.82 on F3, 0.36 on F4 and 0.75 on F5. So the pooled
gain comes from the families with a lower base rate. On F1, raw has Brier 0.000, and any shrinkage makes it
worse; the every-fold rule cannot pass there. This matches T54 / TL-3: out-of-family maps do not transfer.
To be useful, a calibrated P(top) needs an input with resolution. Raw P(top) has none.

## Data and provenance (pipeline sha per file)

`code_sha` is fastrun's stamp: `git rev-parse HEAD:./src` (the src tree).

| file | producer | rows | used for | pipeline |
|---|---|---|---|---|
| `analysis/exp/out/ll_I.jsonl` (this worktree) | V1 | 140 (92 scored, 27 CRASH, 21 TIMEOUT) | V1 failures | src tree 7c590a200c30 (commit 6a86fe8). It was run across 6a86fe8..4308c4c, where `src` changed only in `learned/` and the report-only hook in `loop.py` (off path bit-identical) |
| `analysis/exp/out/ll_Gmatch.jsonl` (this worktree) | V1 | 20 (13 scored, 1 CRASH, 6 TIMEOUT) | V1 clean, matched draws | same pipeline as I (src tree a37c87384921 at 4308c4c; non-learned src identical to 7c590a200c30) |
| shared `ll_G.jsonl` | S-LEARNED | 160 (65 off grid with resid; 35 at 5 % noise) | V1 clean, L2b | code_sha 7c590a200c30 on 41 rows, none on the rest |
| shared `ll_S.jsonl` | S-LEARNED | 45 | L2b only (scattered, no resid) | no sha |
| shared `ll_G_fitcal_off.jsonl` | LB (ll-budget-287936) | 140 (98 with resid) | sensitivity only | no sha; different pipeline (13 steps; see "Confounds") |
| shared `ll_S_fitcal_off.jsonl` | LB | 50 | sensitivity only | no sha |
| shared `ll_N.jsonl` | S-LEARNED | 80 | nulls | no sha |

Corpus I is handed to the controller session C at the path above (via the parent / DATA_INDEX).

## Corpus I (feasibility subset)

- Seven types × three levels × five families (F1–F5).
  - Seed 400 covers all 105 cells.
  - Level 1 gets one more seed per cell (402 or 403, alternating by type and family), adding 35 runs.
  - Total 140 of the planned 420. That is 28 per family and 20 per type, and the subset is balanced
    (`tests/test_learned_inject.py::test_feasibility_subset_is_balanced`).
  - Reason: LOFO on F1–F5 needs every type in every family. Level 1 is the "visible" level the brief's
    useful-detection rule reads.
- Strength normalisation is scale-free, relative to the noise σ:
  - law deviations (two_laws, nonlinear, varcoef, fractional): z = ‖u_ε − u_0‖² / (σ² √(2N)) ∈ {2, 8, 32};
  - coloured noise: AR(1) ρ ∈ {0.3, 0.6, 0.9} in t and x, with marginal variance σ²;
  - heteroscedastic: σ max/min ∈ {2, 5, 20}, with mean variance σ². Even seeds are signal-dependent, odd
    seeds a time ramp;
  - aliasing: max|Im λ|·dt/π ∈ {1.2, 2, 3}.
- **Aliasing is a frame shift, τ → τ + Vξ.** It is not the time rescale the PLAN wrote. A rescale changes
  every factor and moves the draw out of the simulator's prior. The frame shift keeps the factor structure
  and pushes the temporal frequencies past Nyquist. Truth is the shifted factors.
- CRASH / TIMEOUT counts:

  | type | crash | timeout |
  |---|---|---|
  | coloured | 13 | 1 |
  | aliasing | 8 | 0 |
  | nonlinear | 3 | 5 |
  | varcoef | 1 | 5 |
  | two_laws | 1 | 3 |
  | heteroscedastic | 1 | 3 |
  | fractional | 0 | 4 |

  None is a Windows start failure ("3221225794").

## V1 gate tables

Effect size: LOFO AUROC, injected vs clean. Each fold trains on the other four families (all their rows) and
scores the held-out family. The tables report the mean of the per-family AUROCs. The CI is a paired cluster
bootstrap: base draws (seeds) are resampled within each family with all their rows, and every arm uses the
same draws (`ll_v1.lofo_auc`). Non-finite scores are mapped once over the pooled clean and injected scores of
a fold. The measure is α-free, because the conformal α = 0.05 operating point cannot be reached at this n.

Primary configuration: clean = `ll_Gmatch` + shared `ll_G` test, grid, 5 % noise, same pipeline as I
(`results/v1_gate_resid_primary.md`).

All scored runs (49 clean, 92 injected):

| arm | AUROC [95 % CI] | − V0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0 V0 omnibus | 0.681 [0.598, 0.829] | — | 0.69 | 0.80 | 0.65 | 0.50 | 0.77 |
| B1 V0 + resid, min-p (no learning) | 0.806 [0.718, 0.901] | +0.125 [−0.045, +0.211] | 0.85 | 0.91 | 0.82 | 0.64 | 0.81 |
| B2 isolation forest | 0.734 [0.640, 0.852] | +0.053 [−0.091, +0.175] | 0.81 | 0.71 | 0.61 | 0.66 | 0.88 |
| B3 Mahalanobis | 0.671 [0.557, 0.827] | −0.010 [−0.181, +0.109] | 0.81 | 0.83 | 0.61 | 0.51 | 0.59 |
| B4 kNN | 0.674 [0.562, 0.826] | −0.007 [−0.172, +0.107] | 0.81 | 0.82 | 0.63 | 0.51 | 0.59 |
| **V1 HGB** | **0.900 [0.825, 0.975]** | **+0.219 [+0.078, +0.289]** | 0.96 | 0.94 | 0.93 | 0.69 | 0.99 |

FIT-COMPATIBLE runs only (40 clean, 50 injected; the confident-wrong case). F4 has very few such runs, so its
fold value is unstable:

| arm | AUROC [95 % CI] | − V0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0 V0 omnibus | 0.515 [0.440, 0.789] | — | 0.69 | 0.73 | 0.65 | 0.00 | 0.50 |
| B1 min-p | 0.701 [0.564, 0.940] | +0.186 [−0.051, +0.406] | 0.85 | 0.93 | 0.88 | 0.50 | 0.35 |
| **V1 HGB** | **0.759 [0.644, 0.978]** | **+0.244 [+0.083, +0.359]** | 0.94 | 0.96 | 0.89 | 0.00 | 1.00 |

Per type, level and draw (all scored runs):

| type, level or draw | V0 | B1 | V1 |
|---|---|---|---|
| aliasing | 0.68 | 0.83 | 0.87 |
| coloured | 0.30 | 0.75 | 0.98 |
| fractional | 0.71 | 0.87 | 0.95 |
| heteroscedastic | 0.66 | 0.94 | 0.95 |
| nonlinear | 0.86 | 0.81 | 0.95 |
| two_laws | 0.71 | 0.85 | 0.91 |
| varcoef | 0.74 | 0.61 | 0.87 |
| level 0 | 0.62 | 0.82 | 0.93 |
| level 1 | 0.72 | 0.82 | 0.89 |
| level 2 | 0.81 | 0.82 | 0.98 |
| level 1, draw 400 | 0.80 | 0.90 | 0.96 |
| level 1, fresh draws 402/403 | 0.70 | 0.80 | 0.85 |

Levels 0 and 2 come from draw 400 only. Level 1 mixes draw 400 with fresh draws, so the level profile is not
a clean strength test. The level-1 dip is the draw mix.

Robustness (V1 − V0, LOFO AUROC, cluster bootstrap):

| clean rows | n clean | V1 AUROC | V1 − V0 [95 % CI] | file |
|---|---|---|---|---|
| primary (base-draw control + G test) | 49 | 0.900 | +0.219 [+0.078, +0.289] | `v1_gate_resid_primary` |
| primary, no resid features | 49 | 0.831 | +0.150 [+0.004, +0.218] | `v1_gate_noresid_primary` |
| base-draw control only | 14 | 0.886 | +0.106 [−0.062, +0.248] | `v1_gate_resid_basedraw` |
| all sources incl. LB fit+cal (5 % noise) | 101 | 0.826 | +0.185 [+0.036, +0.266] | `v1_gate_resid_allsources` |
| all sources, no resid | 101 | 0.717 | +0.077 [−0.082, +0.166] | `v1_gate_noresid_allsources` |

The base-draw control `ll_Gmatch` is only partly matched. Its seeds are 400–403. Seed 401 is not in corpus I
(3 of its 14 scored rows).

Conformal operating point (α = 0.05; all-sources run, `results/v1_gate_resid_allsources.md`): realised false
alarm is 0.000 on G/S test and on N, and detection is 0.000 for every arm. This is the p-value floor,
1/(n_cal + 1) > 0.05, not a property of the detector. LOTO, the type head and target (b) are vacuous for the
same reason. Target (b) flags every run. In earlier runs, before the confound fixes, the split had more cal
rows. There V1 reached false alarm 0.015 and detection 0.17 at α = 0.05. Those runs are not a verdict,
because their clean set was confounded.

### CRASH / TIMEOUT injected runs

48 of the 140 injected runs end with no output. They are counted per type in the corpus I section above. No
arm scores them, because every V1 feature is computed from the pipeline's output. Second line, counting a
crash as detected: per type, detection then equals the CRASH/TIMEOUT share. That is 0.20–0.70 for every arm
alike: coloured 0.70, aliasing and nonlinear 0.40, varcoef 0.30, the rest 0.20. Scored-row detection is 0.00
at the vacuous α = 0.05 threshold (`results/v1_gate_resid_allsources.md`). **Would the OOD score have flagged these inputs before
the crash? No.** V1 has no input-only features, so it cannot score an input whose run crashes or times out. A
crash or timeout is itself a failure signal, and the pipeline already reports it (CRASH / TIMEOUT label).

## L2b gate tables (primary: same-pipeline rows `ll_Gmatch` + `ll_G` + `ll_S`)

Every arm fails the every-fold rule: Brier and ECE must both be ≤ raw on every LOFO fold.

y = right or equivalent (`results/ptop_gate_equiv_primary.md`):

| arm | pooled Brier | ΔBrier vs raw [95 % CI] | F1 Brier (raw 0.000) | gate |
|---|---|---|---|---|
| raw | 0.2114 | — | 0.000 | — |
| temperature | 0.1801 | −0.0313 [−0.0674, +0.0030] | 0.077 | fail |
| platt | 0.1924 | −0.0190 [−0.0636, +0.0258] | 0.077 | fail |
| isotonic | 0.1993 | −0.0121 [−0.0574, +0.0334] | 0.078 | fail |
| venn-abers | 0.1884 | −0.0230 [−0.0614, +0.0145] | 0.085 | fail |
| logit-features | 0.1796 | −0.0318 [−0.0730, +0.0067] | 0.081 | fail |

y = right (`results/ptop_gate_right_primary.md`): raw pooled Brier 0.4027. All arms fall between
temperature −0.1337 [−0.2155, −0.0493] and logit-features −0.1131 [−0.2017, −0.0214]. All fail the
every-fold rule on F1 (raw 0.120, arms 0.233–0.250).

CRASH / TIMEOUT rows have no P(top) and are not calibrated: F3 0/3, F4 6/8, F5 1/12 (crash/timeout).
Right rate is 0.596 on 94 scored rows, or 0.452 counting the 30 CRASH / TIMEOUT rows as not-right. Right
or equivalent is 0.787, or 0.597 counting them.

Sensitivity with LB's fit+cal rows added (215 scored, 99 CRASH / TIMEOUT; `*_withLB.md`): for y = equivalent,
ΔBrier is −0.0531 [−0.0835, −0.0230] (temperature) and −0.0571 [−0.0931, −0.0224] (logit-features), with CI
below 0. It still fails on F1: raw 0.050, arms 0.118–0.133. LB's rows come from a
different pipeline (see below), so a calibrator fitted on them would not be calibrated for this one.

## Confounds found and removed (each one inflated V1)

1. **Design shortcut.** Clean S rows are scattered and every I row is a grid. Fix: clean rows are restricted
   to the injected rows' design, using the same rule as featurise.
2. **Step wall-time fractions.** LB's rows log one more pipeline step (13 vs 12). On `step:raw_subset_frac`
   alone, the AUROC between them and the other sets is 0.00. Fix: the `step:*_frac` features are removed from
   V1 (`validator.featurise`; test `test_featurise_shape_and_empty_row`). Wall-time fractions also depend on
   load and machine, so they are not reproducible.
3. **Noise level.** G mixes 1 % and 5 % noise, while I is all 5 %. Fix: clean rows must match the injected
   rows' design kind and noise level (`ll_v1.py`).
4. **Pipeline drift in LB's rows.** An HGB probe, LOFO, at 5 % noise only, separates:
   - LB G fit+cal from G test: AUROC 0.83;
   - LB G fit+cal from the matched control: 0.80;
   - G test from the matched control: 0.51, indistinguishable.
   So LB's rows are excluded from the primary configuration, and the matched control validates G test.

Remaining checks against a shortcut: V1 keeps its margin on FIT-COMPATIBLE runs only, where the label carries
no signal. It also keeps its margin on fresh base draws (0.85 vs V0 0.70). The level profile is not used as
evidence, because the draw mix confounds it (see the gate tables).

## What V1 adds beyond V0 (`validate.py`)

- V0 is a battery of deterministic tests: the V0.1 omnibus predictive χ² per κ-bin, the margins, the gap and
  the held-out check.
- V1 reuses V0's projection unchanged (`learned/resid.py` calls `validate._log10sf`).
  `tests/test_learned_resid.py::test_residual_is_the_v0_projection` checks per-bin χ² equality with
  `validate.predictive_bins`.
- On that same residual, V1 adds tests that V0 does not have:
  - whiteness in t: Ljung–Box log p and lag-1 autocorrelation;
  - whiteness in x: lag-1 autocorrelation and spectral flatness;
  - heteroscedasticity: Breusch–Pagan log p;
  - time-change: half-energy ratio;
  - aliasing: Nyquist energy share;
  - κ-trend.
- V1 also adds a learned combination of these with the V0 battery, the exports and the run summary.
- What each addition contributes:
  - The resid statistics without learning (B1) add +0.125 AUROC over V0 (CI [−0.045, +0.211], crosses 0).
  - The learned combination adds about +0.094 more (V1 0.900 vs B1 0.806, point estimate). With the resid
    features removed, V1 drops to +0.150 over V0.
  - The largest gains are on the failure types V0 is built to miss: coloured noise (V0 0.30 → V1 0.98),
    heteroscedastic (0.66 → 0.95), and level 0 (0.62 → 0.93).

## Known issues (pre-existing, not V1's files)

- `validate.predictive_bins` raises `LinAlgError: SVD did not converge in Linear Least Squares` when a fitted
  factor is unstable, because Z = exp(t·λ) overflows at high κ. Most coloured-noise crashes are this. One clean
  matched run hits it too (G F4 401). It is not fixed here (main's file); the parent logs it as a known main bug.
- S rows written before `resid` existed lack it. V1 uses rows with `resid` only; L2b does not need it.
- `tests/test_aggregate_cluster`: 6 errors that pre-exist on the base.

## One-command retrain recipes

Run from `PDEFactorML/analysis/exp` with `OMP_NUM_THREADS=1 PYTHONIOENCODING=utf-8` and the venv python. Set
`S` to the shared out directory: `D:\Larned layers\PDEFactorML\analysis\exp\out`.

```bash
python ll_inject.py --run out/ll_I.jsonl --workers 6                                  # corpus I subset (resumable)
python ll_inject.py --clean-control --run out/ll_Gmatch.jsonl --workers 6             # matched clean control
python ll_v1.py --clean out/ll_Gmatch.jsonl $S/ll_G.jsonl --fail out/ll_I.jsonl --nulls $S/ll_N.jsonl --save
python ll_ptop.py out/ll_Gmatch.jsonl $S/ll_G.jsonl $S/ll_S.jsonl --equiv --save
```

`--save` writes `src/pdefactor/learned/models/{v1,ptop}.joblib` only if the gate passes. Neither passes now,
so no model ships and both flags stay off. Re-gate on the final pipeline. Add clean grid rows at 5 % noise,
with fit/cal splits, from the same pipeline as I, at least 20 per family, so the conformal gate becomes
evaluable.

## Not done (out of the feasibility scope)

- No tuning: HGB defaults, no monotone constraints, no feature selection.
- No run with the flag on over N and the named cases (PLAN 3.5 item 5). Report-only behaviour is covered by
  the tests instead.
- THEORY_TO_ALGO: no `LL-T<n>` row is added.
