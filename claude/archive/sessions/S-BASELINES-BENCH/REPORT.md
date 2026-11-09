# S-BASELINES-BENCH — REPORT (2026-10-28)

**Status:** done criterion met.
- The full grid ran: 560 inputs × 7 methods = 3920 rows, with 0 crashes.
- The smoke tests pass (`tests/test_baselines_bench.py`, 18 tests, about 55 s).
- Nothing was committed and no package was installed. pysindy 2.1.0, pydmd 2025.8.1, numpyro 0.22 and jax 0.12 were already present.

## What was built
- `src/pdefactor/baselines/`. Every baseline maps gridded u[t, x] to a `BaselineResult`, which holds:
  - the symbol P (monic in τ^m);
  - its coefficients;
  - its sympy factors and their structure;
  - an optional structure distribution;
  - the runtime.

  | baseline | what it does |
  |---|---|
  | `pdefind` | Strong form. Spectral ∂_x, `ps.FiniteDifference(order=4)` in t, `ps.STLSQ`. BIC over the threshold path and over m ∈ {1, 2, 3}. |
  | `weak_sindy` | Weak form: 200 bump test functions ((s−a)(b−s))^6, the math of `WeakPDELibrary`, extended to ∂_t^m targets and mixed ∂_t^a∂_x^b terms. Same STLSQ + BIC. |
  | `ensemble_sindy` | `ps.EnsembleOptimizer`: 50 bagged STLSQ models on the weak system. The median gives the model, and member frequencies give the structure distribution. |
  | `sbr_sindy` | `ps.SBR` (horseshoe, NUTS, 300 warmup + 500 samples) on the weak system. The structure distribution comes from 100 posterior samples. |
  | `bopdmd` | `pydmd.BOPDMD` with 8 time delays, a noise-edge rank and bagging (20 trials). Unstable eigenvalues are dropped using its own std. Each (λ, iκ) point (κ = every significant FFT peak of the mode) feeds a monic least-squares symbol fit, with (m, dx) chosen by BIC. The adapter is ours; the eigenvalues are BOP-DMD's. |
  | `factor_symbol` | Rounds to d = 2 decimals, runs `sympy.factor_list(extension=I)`, then refines the factor coefficients by least squares against the unrounded P. |

- `benchmarks/`:
  - `bench.py` runs the grid and is resumable, writing `benchmarks/out/runs.jsonl`.
  - `interp.py` holds the **PLACEHOLDER** griddata interpolator. It is pluggable: `make_input(..., interpolator=f)` with `f(ts, xs, ys, t, x, L, sigma, seed) -> (U, sigma_eff)`.
  - `metrics.py` reuses `e1_noise.truth` and `match_err` with tolerance 0.05.
  - `report.py` writes `benchmarks/out/summary.md` (all tables, per case, all failure cells) and `benchmarks/out/reliability.png`.
- Grid:
  - the 10 `CASES` (field seed 0, as in E1/E1c);
  - noise σ ∈ {0, 1e-3, 1e-2, 5e-2} × std(|u|);
  - sampling ∈ {64×128 grid, 2000 scattered, 400 scattered};
  - seeds 0–4 (exact gridded data is run once).

## Main table — factor-set recovery rate (n runs) / median coef_err of the correct runs
| method | sampling | σ=0 | σ=1e-3 | σ=1e-2 | σ=5e-2 |
|---|---|---|---|---|---|
| **core_v2** | grid | 1.00 (10) / 0 | **1.00** (50) / 2e-05 | **1.00** (50) / 3e-04 | **0.90** (50) / 2e-03 |
| core_v1 | grid | 1.00 / 0 | 0.66 / 7e-05 | 0.60 / 5e-04 | 0.56 / 4e-03 |
| pdefind | grid | 1.00 / 5e-07 | 0.30 / 3e-02 | 0.10 / 2e-03 | 0.00 / — |
| weak_sindy | grid | 1.00 / 3e-04 | 1.00 / 3e-04 | 0.90 / 9e-04 | 0.62 / 1e-02 |
| ensemble_sindy | grid | 1.00 / 2e-04 | 1.00 / 3e-04 | 0.82 / 6e-04 | 0.58 / 2e-02 |
| sbr_sindy | grid | 1.00 / 4e-04 | 0.92 / 3e-04 | 0.72 / 2e-03 | 0.58 / 1e-02 |
| bopdmd | grid | 0.50 / 2e-04 | 0.06 / 3e-02 | 0.04 / 5e-02 | 0.02 / 5e-02 |
| **core_v2** | 2000 | 0.66 / 3e-03 | 0.68 / 3e-03 | 0.70 / 3e-03 | **0.70** / 5e-03 |
| core_v1 | 2000 | 0.50 | 0.52 | 0.52 | 0.48 |
| pdefind | 2000 | 0.10 | 0.10 | 0.10 | 0.10 |
| **weak_sindy** | 2000 | **0.76** / 7e-04 | **0.76** | **0.72** | 0.50 |
| ensemble_sindy | 2000 | 0.76 | 0.72 | 0.68 | 0.54 |
| sbr_sindy | 2000 | 0.68 | 0.68 | 0.68 | 0.56 |
| bopdmd | 2000 | 0.00 | 0.00 | 0.00 | 0.00 |
| core_v2 | 400 | 0.18 / 1e-02 | 0.18 | 0.22 | 0.22 |
| core_v1 | 400 | 0.22 | 0.22 | 0.24 | 0.20 |
| pdefind | 400 | 0.10 | 0.10 | 0.08 | 0.08 |
| **weak_sindy** | 400 | **0.46** / 1e-02 | **0.46** | **0.48** | **0.50** |
| ensemble_sindy | 400 | 0.48 | 0.48 | 0.44 | 0.44 |
| sbr_sindy | 400 | 0.48 | 0.48 | 0.46 | 0.50 |
| bopdmd | 400 | 0.00 | 0.00 | 0.00 | 0.00 |

Each noisy cell has 50 runs (10 cases × 5 seeds). The per-case tables are in `benchmarks/out/summary.md`.

**What the table supports:**
1. **Gridded data.** core_v2 is the only method with a rate ≥ 0.90 at every noise level. It is also 10–100× more accurate in its coefficients at noise > 0.
2. **Scattered data, with the placeholder interpolator.** The weak-form SINDy baselines match or beat core_v2: 0.76 vs 0.66 at 2000 points, and 0.46 vs 0.18 at 400 points. The core's advantage depends on the quality of the interpolant. The table does not show that core_v2 is better on scattered data.
3. **Hardest case.** transport_plus_diffusion fails for every method on scattered data (0.0–0.2).

## Structure posterior calibration
The full reliability diagram is in `benchmarks/out/reliability.png`. Pooled ECE over all listed structures (dominated by many pairs near p ≈ 0):

| method | grid | 2000 | 400 |
|---|---|---|---|
| core_v2 | 0.006 | 0.019 | 0.053 |
| ensemble_sindy | 0.152 | 0.269 | 0.338 |
| sbr_sindy | 0.250 | 0.330 | 0.386 |

Top-structure calibration (confidence vs accuracy) is the fairer view:

| method | sampling | mean p(top) | accuracy of top | runs with p(top) ≥ 0.9 / their accuracy |
|---|---|---|---|---|
| core_v2 | grid | 0.89 | 0.99 | 98 / 0.99 |
| core_v2 | 2000 | 0.80 | **0.65** | 74 / **0.70** |
| core_v2 | 400 | 0.76 | **0.27** | 79 / **0.38** |
| ensemble_sindy | grid | 0.88 | 0.76 | 106 / 0.88 |
| ensemble_sindy | 2000 | 0.85 | 0.66 | 117 / 0.67 |
| ensemble_sindy | 400 | 0.78 | 0.40 | 75 / 0.41 |
| sbr_sindy | grid | 0.89 | 0.66 | 113 / 0.79 |
| sbr_sindy | 2000 | 0.85 | 0.53 | 126 / 0.56 |
| sbr_sindy | 400 | 0.79 | 0.32 | 92 / 0.37 |

- On the grid, core_v2's structure posterior is well calibrated and slightly underconfident.
- On scattered data it is **overconfident**: p ≥ 0.9 is right only 70 % of the time at 2000 points and 38 % at 400. The cause is that one deterministic interpolant is analysed with a single σ_eff, so interpolation bias is not propagated. This is the expected gap that the S-INTERP posterior samples should close (CLAUDE rule 4: Monte Carlo over interpolants).
- Ensemble and SBR frequencies are overconfident everywhere, including on the grid.

## Labels (core) and weights
- core_v2 labels:
  - grid: FIT-COMPATIBLE 100 % up to 1e-2. At 5e-2, 6 % are UNDECIDED, all of them beam: the confluent test fires on unresolved branches, as in PARAMETERS.md.
  - 2000 points: FIT-COMPATIBLE 84–94 %, ID-KER 2–8 %, UNDECIDED 4–8 %.
  - 400 points: ID-KER 8–16 %, UNDECIDED 10–12 %, MISFIT 0.
- core_v1 at 400 points gives MISFIT 20–26 % and ID-KER 26–32 %.
- How core_v2 labels its **wrong** answers:
  - grid: 4 FIT-COMPATIBLE, 1 UNDECIDED;
  - 2000 points: 51 FIT-COMPATIBLE, 9 ID-KER, 3 UNDECIDED;
  - 400 points: 117 FIT-COMPATIBLE, 23 ID-KER, 20 UNDECIDED.

  Most wrong answers on scattered data are still labelled FIT-COMPATIBLE. The label does not flag interpolation bias, which is the same overconfidence as in the calibration section.
- Weight error, counted only on the multi-factor cases with defined truth weights:
  - core_v2: TPD grid median 9.7e-4 (max 1.1e-2); wave grid 1.7e-4; wave at 2000 points 1.8e-3.
  - core_v1: wave grid 4.3e-5.
  - Single-factor cases give 0 trivially, which is why the pooled table in summary.md shows a median of 0.
  - Baselines return no weights (n/a).

## Runtime per run (s): median [IQR]
On 6 workers with other sessions running; the full grid took 2796 s (about 47 min) of wall time.

| method | grid | 2000 | 400 |
|---|---|---|---|
| core_v2 | 1.08 [0.57, 3.34] | 1.10 [0.51, 4.42] | 0.87 [0.41, 2.35] |
| core_v1 | 0.10 [0.06, 0.14] | 0.12 | 0.09 |
| pdefind | 0.61 [0.47, 0.94] | 0.60 | 0.56 |
| weak_sindy | 2.67 [2.17, 3.30] | 2.53 | 2.41 |
| ensemble_sindy | 4.25 [3.43, 5.65] | 3.88 | 3.95 |
| sbr_sindy | 12.4 [10.4, 17.4] | 11.8 | 11.5 |
| bopdmd | 1.61 [1.28, 2.84] | 1.25 | 1.17 |

The interpolation time (griddata plus hold-out) is not counted in the method runtimes.

## Failure cases (honest list)
1. **core_v2, transport_plus_diffusion at 5e-2 (grid): 0.2.** The structure is right ((1,1),(1,2)) in 4 of 5 runs, but the diffusion coefficients are off by more than 0.05. This is a known failure (PARAMETERS.md E1c). Beam at 5e-2 gets 0.8, with 3 of 5 runs UNDECIDED (confluent).
2. **core_v2 on scattered data**:
   - transport_plus_diffusion is 0.0 at both densities.
   - At 400 points, the KG, telegraph, wave, beam and TPD cells are 0–0.2.
   - Even with exact samples, core_v2 at 400 points gets transport and heat only 0.2. The linear interpolant's bias (σ_eff ≈ 0.12, about 10 % of std u) breaks the pencil.
   - These are failures of the placeholder interpolator as much as of the core. They need re-measuring with the GP.
3. **core_v1**:
   - KG and telegraph are always falsely factored into two (1,2) factors at noise ≥ 1e-3.
   - transport_plus_diffusion merges into one (2,3) factor.
   - This is the known fixed-tolerance problem (CONV-T5) that v2 removed.
4. **PDE-FIND** collapses with noise. Strong-form derivatives in t amplify the noise, and BIC then picks m = 1 for every second-order case. At 2000 and 400 points it gets only transport.
5. **Weak / Ensemble / SBR**:
   - Their errors are mainly two-factor cases at σ ≥ 1e-2: wave → (2,2) irreducible, TPD → (1,4) or (2,4), beam → (1,3).
   - **Rounding fragility**, a CONV-T5 illustration: wave fitted as τ² − 1.006ξ² rounds to 1.01, which is not a square, so it is reported irreducible.
   - Rounding sensitivity on the grid, d = 1/2/3: weak 0.82/0.85/0.73, Ensemble 0.81/0.81/0.73, SBR 0.80/0.76/0.66. No single d is right for all cases.
   - SBR's horseshoe shrinks the mixed τξ terms, so it is worse than plain Weak SINDy on two-factor cases.
6. **BOP-DMD + variety adapter**: 5/10 exact on the grid, about 0 with noise or scattered input. The causes:
   - real standing modes share an eigenvalue between ±κ, which needs time delays;
   - at 1e-2 noise only 6 singular values clear the noise edge (3 κ);
   - projected eigenvalues are biased by about 5 %;
   - mode/κ assignment becomes ambiguous.

   It is reported as is. A better adapter (per-κ DMD) would essentially be our matrix pencil.
7. **Slope of coef_err vs noise** (grid, correct runs): core_v2 1.25, core_v1 1.03, weak 0.88, Ensemble 0.99, SBR 0.95. These are all steeper than the worst case 1/3 (DM-δ-MINIMAX, T14), which is consistent with that bound. Each slope uses only 3 noise points. The PDE-FIND slope (−1.26) uses 2 points and has survivor bias, so it is not meaningful.

## Deviations and choices to flag
- Baselines get the same model class as core v2: a linear library, m ≤ 3, dx ≤ 4.
- The BIC residual floor ρ0 = 1e-3 (relative) is a hand constant. It is needed because systematic discretisation error otherwise drives BIC to m = 3 on exact data.
- PDE-FIND uses FD order 4. Order 2 failed heat and advection-diffusion even on exact data.
- PySINDy's `PDELibrary`/`WeakPDELibrary` were not used, because they cannot target u_tt with mixed terms. The features are ours; the optimizers are PySINDy's.
- Scattered noise follows the grid convention σ = noise × std(|u_grid|), complex for complex fields. It is not `synthetic.sample_scattered`, whose noise is real-only.
- Grid inputs use the same noise seeds as E1/E1c (100 + seed), so core_v2 grid rows are comparable with E1c.

## Open questions / requests to other sessions
- **S-INTERP:** plug the GP in as `interpolator=`, returning a posterior mean and σ, or loop over samples. The benchmark should then be re-run at 2000 and 400 points. The calibration table above is the baseline to beat; core_v2's top structure at 400 points is currently 27 % accurate with a mean confidence of 0.76.
- **MAIN:** add the four theory → benchmark rows in `sessions/S-BASELINES-BENCH/RESEARCH.md` to THEORY_TO_ALGO.md, and add the RESEARCH section. Consider a grid-level label or warning when σ_eff comes from a deterministic interpolant.
- Not run, and left as follow-ups: `note_example`, `EXTRA_CASES` (repeated_transport should be UNDECIDED, while the baselines will factor it confidently as (τ+ξ)²), the two-regime case (ARI), σ = 0.1, and n = 6400.
