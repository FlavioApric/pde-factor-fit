# S-INTERP — PLAN (2026-10-28)

I am **S-INTERP** (Phase 2). I own `src/pdefactor/interp/` and implement plan step 1 (interpolation with probabilities) and the v2 phase order item 2. I work in worktree `D:\PDEFactorML-S-INTERP` on branch `s-interp`. The core is a black box (`pdefactor.core.structfit.analyze_structured`).

## Goal and done criterion
- S posterior samples û_s on a uniform (t, x) grid with weights π_s (Σπ_s = 1), plus σ̂, from scattered noisy samples (t_i, x_i, y_i).
- **Done:**
  1. The pointwise credible bands of the GP posterior cover the true u at the nominal level ±5 points (50 %, 90 %, 95 %). Measured on the synthetic cases with n ∈ {400, 2000} and noise ∈ {1 %, 5 %}.
  2. End to end on `case("transport_plus_diffusion")`: core v2 on the samples gives the factor set {τ+ξ, τ−0.3ξ²} in most samples (posterior weight > 0.5).
  3. `tests/test_interp.py` passes and the existing 39 tests stay green.
  4. `REPORT.md` contains the coverage table, the runtimes and the high-κ bias measurement.

## Theory → choices (THEORY_TO_ALGO rows)
| choice | motivation |
|---|---|
| GP posterior with Monte Carlo samples, not a point interpolant | T12 (OPA-T3, P1-P1(e)): E_int is discontinuous, so it can only be taken as a distribution over samples. T18 (CONV-T3): the discrete outputs get a posterior. |
| σ as a posterior quantity (σ̂ and its samples), passed to the core | T15 (CONV-T5): the threshold cannot be estimated without a data model, so it uses the GP posterior σ̂. |
| hyperparameters by type-II ML + Laplace + importance weights; NUTS for small n | CLAUDE.md rule 4. No theory on the GP itself, so the choice is empirical, with the literature in RESEARCH.md (ML-II undercovers). |
| separable kernel k_t ⊗ k_x; family (Matérn 3/2, 5/2, RBF) chosen by Laplace evidence, mixed by posterior weight | no theory: empirical (Bayesian model comparison, as in the structfit of T15) |
| optional periodic-in-x kernel, only when the user states the period | T19 (CONV-B1): BCs are invisible to Ann(u). Periodicity is prior knowledge of the domain, never learned. The default is non-periodic. |
| smoothness one order higher for components (ν → ν+1) in the EPGP pass | T11 (C12-C1, FALSO: the components lose exactly one derivative) |
| high-κ bias measured on the decay rates λ(κ), not only on u | T26 (DICT-ILIM-Hs, DIMOSTRATO): an L² error controls derivatives only with θ < 1. T9 (P2-P6): high κ matters for the Vandermonde inversion. |
| EPGP features e^{λ(κ)t+iκx} on each factor's variety | T25 (R2-T6, DIMOSTRATO-CON-FONTE), Härkönen et al. 2023 |
| deep ensemble only as an ablation | no theory: empirical (RESEARCH.md) |
| noise level handed to the core = equivalent white noise of the sample deviations | no theory: empirical. The core's bin noise assumes white noise (`noise/√nx`), but GP errors are correlated. Calibrated end to end on TPD. |

## API (`pdefactor.interp`)
```python
@dataclass
class GPPosterior:
    t, x: np.ndarray                 # grid axes
    samples: np.ndarray              # (S, nt, nx) posterior draws of the latent field
    weights: np.ndarray              # (S,) pi_s, sum 1
    sigma_hat: float                 # posterior mean of the noise std (data units)
    sigma_samples: np.ndarray        # (S,) noise std of the hyperparameter draw behind each sample
    mean, var: np.ndarray            # weighted mixture mean / variance on the grid
    comp_mean, comp_var: np.ndarray  # (S, nt, nx) Gaussian marginal of each sample's hyper draw (exact PIT)
    info: dict                       # kernel posterior, theta_hat, ESS, method, runtime
    def pit(u_true) -> np.ndarray     # mixture CDF at the truth, per grid point
    def coverage(u_true, levels=(.5,.9,.95)) -> dict
    def effective_noise() -> float    # equivalent white-noise std for the core

fit_gp(t, x, y, *, grid=(t_grid, x_grid) | (nt, nx), S=32, kernels=("matern32","matern52","rbf"),
       period_x=None, method="auto"|"laplace"|"nuts"|"ski", device="auto", seed=0) -> GPPosterior
smoother(kernel) -> kernel           # one order smoother (C12-C1): matern32 -> matern52 -> rbf

ensemble.fit_ensemble(t, x, y, *, grid, M=5, arch="siren"|"mlp", steps, seed) -> GPPosterior-like result
epgp.fit_epgp(t, x, y, factors, *, kappa_max, n_kappa, smooth_shift=1, period_x=None) -> EPGPPosterior
    .sample(S, t_grid, x_grid) -> (S, nt, nx); .component_samples(S, ...) -> (S, J, nt, nx)
run_core_on_samples(samples, t, x, sigma, weights=None, **core_kw) -> list[(StructResult, pi_s)]
factor_set_posterior(results) -> dict[frozenset(str factor) -> prob]
```

## Tests written first (`tests/test_interp.py`)
1. `fit_gp` on heat (n = 400, 5 %): shapes, Σπ = 1, all π ≥ 0, σ̂ within ×1.5 of the true σ.
2. Coverage at 90 % on transport (n = 400, 5 %) within [0.80, 0.99]. This is a loose bound for speed; the strict ±5 check is the REPORT benchmark.
3. Mixture PIT on the truth lies in [0, 1], and a hand-made Gaussian check matches `scipy.stats.norm.cdf`.
4. `run_core_on_samples` on TPD gives a list of length S with π, and `factor_set_posterior` sums to 1.
5. EPGP: each feature satisfies Q(∂t, ∂x)φ = 0 (symbolic check on λ). A prior draw for τ+ξ is transport-invariant: u(t,x) = u(0, x−t). On TPD data with the true factors, the posterior component weights are within 0.05 of the truth.
6. Ensemble: smoke test (2 members, 200 steps); shapes and Σπ = 1.
7. SKI path: n = 6000, smoke test, runs and returns finite samples.

## Parameters introduced and how each is estimated
| parameter | how |
|---|---|
| outputscale, ℓ_t, ℓ_x, σ_n, constant mean | posterior: type-II MAP plus Laplace plus importance weights, or NUTS for n ≤ 300. Weak log-normal priors on the standardised data, N(0, 3²) in log space. |
| kernel family | posterior over families from the Laplace evidence. Each sample's family is drawn from it. |
| S (number of samples) | user setting (default 32). The ESS of π is reported. It is a Monte Carlo budget, not a model parameter. |
| SKI grid size | the output grid itself (no extra parameter) |
| EPGP: per-factor scale s_j, spectral length ℓ_κ, σ_n | type-II ML on the closed-form BLR evidence |
| EPGP κ lattice | spacing π/L (half the FFT spacing), up to κ_max = the Nyquist limit of the grid. It is a quadrature, not a model parameter. |
| ensemble M, width, steps | ablation settings (fixed, reported) |
| effective noise for the core | computed from the sample deviations (FFT bin variance); no free constant |

## Experiments (`sessions/S-INTERP/exp/`)
- `coverage.py`: cases × n ∈ {400, 2000} × noise ∈ {1 %, 5 %} × 2 seeds. It records coverage at 50/90/95, σ̂/σ, runtime and ESS.
- `e2e_tpd.py`: TPD at n = 2000, 1 % and 5 %. It runs core v2 on each sample and reports the factor-set frequency, plus the noise passed to the core.
- `highk_bias.py`: heat and TPD. It compares the per-κ amplitude transfer |Û_mean|/|U_true| and the decay rate error λ̂(κ) − λ(κ) for each kernel family (ν = 3/2, 5/2, ∞). It also compares the D estimated by the core against the true 0.3.
- `ensemble_ablation.py`: coverage of the deep ensemble on the same grid.

## Addendum (2026-10-28, parent-session correction)
The work moves to the shared checkout `D:\PDEFactorML`, uncommitted, because the main session commits. I touch only `src/pdefactor/interp/`, `tests/test_interp.py`, `sessions/S-INTERP/` and `analysis/exp/interp_*`. Research verdicts are in `sessions/S-INTERP/RESEARCH.md`. The THEORY_TO_ALGO rows proposed for T25/T26 are in `sessions/S-INTERP/THEORY_TO_ALGO_rows.md`, for the main session to merge. Only `pytest tests/test_interp.py` is run. The temporary worktree `D:\PDEFactorML-S-INTERP` (branch `s-interp`, no commits) was used for development.

## Addendum 2 (2026-10-29): default kernel families
The benchmark replaced the PLAN's (matern32, matern52, rbf) and the interim RBF-envelope default with the Matérn-5/2 set (matern52, matern52e, matern52e+matern52e). See REPORT §2. The large-n default is "subset" (exact path on 6000 random points). SKI is experimental and opt-in.
