# S-BASELINES-BENCH — PLAN

I am **S-BASELINES-BENCH** (Phase 2). I own `src/pdefactor/baselines/`, `benchmarks/`, `tests/test_baselines_bench.py` and `sessions/S-BASELINES-BENCH/`, and I implement plan §Phase 2 / v2.6 item 2 (benchmark grid, baselines and metrics; skill `benchmark-protocol`). Nothing is committed and no branch is switched, because the folder is shared.

## 1. Goal and done criterion
- Baselines: PDE-FIND, Weak SINDy, Ensemble SINDy and SBR (PySINDy optimizers), and BOP-DMD (PyDMD). All of them read the same gridded input (scattered input is interpolated first) and return a `BaselineResult` holding the recovered operator symbol P(τ, ξ), its sympy factors, the factor structure, an optional structure distribution, and the runtime. "Not applicable" is reported when something is not available.
- Benchmark: the 10 `CASES` × noise {0, 1e-3, 1e-2, 5e-2} × sampling {grid, 2000 scattered, 400 scattered} × 5 seeds (noise 0 on the full grid uses 1 seed, because it is deterministic). Methods: core v2, core v1 and the 5 baselines.
- Done: the full grid runs; `REPORT.md` has the table, the failure cases and the runtimes; `tests/test_baselines_bench.py` (fast smoke) is green.

## 2. API
```python
# pdefactor.baselines
BaselineResult(method, applicable, reason, P, coeffs, m, factors, structure, structure_probs, runtime, info)
pdefind(u, t, x, noise=0., **kw)  ->  BaselineResult   # strong form, STLSQ path, BIC selection over (m, threshold)
weak_sindy(u, t, x, noise=0., **kw)
ensemble_sindy(u, t, x, noise=0., **kw)                # EnsembleOptimizer(STLSQ), bagging, on the weak system
sbr_sindy(u, t, x, noise=0., **kw)                     # pysindy.SBR (NUTS) on the weak system
bopdmd(u, t, x, noise=0., **kw)                        # BOPDMD eigs -> (lambda, i kappa) -> monic LS symbol fit
factor_symbol(coeffs, m, decimals=2, real=True) -> (factors, structure)  # round -> sympy.factor_list -> LS refine
BASELINES = {name: fn}
# benchmarks/
interp.griddata_placeholder(ts, xs, ys, t, x, L) -> (U, sigma_eff)     # PLACEHOLDER until S-INTERP's GP
bench.make_input(case, noise, sampling, seed, interpolator) -> (U, t, x, sigma, meta)
bench.run_method(name, U, t, x, sigma) -> dict row
bench.run_grid(..., workers) -> benchmarks/out/runs.jsonl  (resumable)
report.summarise(runs.jsonl) -> benchmarks/out/summary.md, reliability.png
```
Symbol convention, the same as the core's: the library term ∂_t^a ∂_x^b u corresponds to τ^a ξ^b, and the model ∂_t^m u = Σ c_ab ∂_t^a∂_x^b u gives P = τ^m − Σ c_ab τ^a ξ^b.

## 3. Choices and the result behind each one
- **Linear library {∂_t^a∂_x^b u : a < m, b ≤ 4}, m ∈ {1, 2, 3}** (no theory: empirical, plus fairness). The truth is linear with constant coefficients, and core v2 searches m ≤ 3 and dx ≤ 4, so the baselines get the same model class. PySINDy's `PDELibrary`/`WeakPDELibrary` cannot target u_tt with mixed u_tx terms, so the features are ours and the optimizers are PySINDy's.
- **Derivatives**: spectral in x (periodic grid), second-order central differences in t (equivalent to `ps.FiniteDifference(order=2)`), dropping 3 rows at each edge in t.
- **Choosing m and the threshold**: BIC over the STLSQ threshold path (Mangan et al. 2017). This gives the baseline its best standard chance. No theory: empirical.
- **Factoring**: coefficients are rounded to d decimals, then `sympy.factor_list(extension=I)`, then the factor coefficients are refined by least squares against the unrounded P. d = 2 is a hand tolerance (CONV-T5: there is no data-free alternative), and the sensitivity to d ∈ {1, 3} is reported on the full grid.
- **Complex fields** (schrodinger): the system is stacked into real and imaginary parts with complex coefficients. Real fields use real coefficients.
- **BOP-DMD**: `svd_rank=0` (optimal hard threshold), plain fit. κ of each mode is the signed FFT peak. The fit is a monic least-squares fit over (m, dx) chosen by BIC.
- **Scattered input**: `griddata` (linear, periodic padding in x, nearest fill), clearly a **PLACEHOLDER**. σ_eff = √(σ² + σ_holdout²), where σ_holdout comes from a 10 % hold-out. The interpolator is an argument of `make_input`, so the GP can replace it later.
- **Weights**: only the cores return weights. The truth weights are `Field.weights` on the grid; beam is skipped (see its note). Baselines get n/a.
- **Calibration**: the event is "this structure equals the true structure". Predicted probabilities are core v2's `structures` posterior, the Ensemble member frequency and the SBR sample frequency. Reported as a reliability diagram (10 bins), ECE and Brier score.

## 4. Parameters
These are benchmark design constants, not loop or grouping parameters, so CLAUDE rule 4 does not apply. Baseline hyperparameters use the library defaults or a BIC path (above). Weak test functions: K = 200, p = 6, H_t = T/4, H_x = L/4, fixed seed. Ensemble: 50 bagged models. SBR: 300 warmup, 500 samples.

## 5. Tests (first)
`tests/test_baselines_bench.py`:
1. `factor_symbol` on exact wave / TPD / telegraph coefficients gives the right structure.
2. PDE-FIND and Weak SINDy recover transport on the exact grid (factor_set = 1).
3. BOP-DMD recovers transport on the exact grid.
4. The interpolator placeholder returns a finite grid and σ_eff > 0.
5. `run_method` gives a complete row for every method on a tiny case (SBR with reduced samples).
6. The metrics: `match_err` and the reliability/ECE code on a hand example.
