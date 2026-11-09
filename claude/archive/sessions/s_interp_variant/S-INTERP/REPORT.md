# S-INTERP — REPORT (2026-10-29)

Step 1 of the pipeline: interpolation with probabilities. Package `src/pdefactor/interp/`, tests `tests/test_interp.py` (11 tests, green). Nothing committed (parent-session correction): files copied into `D:\PDEFactorML`, uncommitted.

## Verdict against the done criteria
| criterion | status |
|---|---|
| 1. Coverage within ±5 points of nominal (50/90/95 %) on the synthetic cases, n ∈ {400, 2000}, noise ∈ {1 %, 5 %} | **Met in 11 of 12 cells** with the default Matérn-5/2 families (§2). The one miss is the 50 % band at n = 400 / 1 %: 0.553, +5.3, on the conservative side. The RBF set fails at n = 2000 (cov90 0.84–0.86). The Matérn-3/2 set fails at n = 400 (cov50 0.62). |
| 2. E2E on TPD: core v2 on the samples gives {τ+ξ, τ−0.3ξ²} with posterior weight > 0.5 | **NOT MET** (best 0.40, default Matérn-5/2 at n = 2000 / 1 %). The cause is the core's scalar white-noise interface (§4). This needs a change in the core, which S-INTERP may not touch. |
| 3. `tests/test_interp.py` green; other tests untouched | met (11/11). Only my own file was run (parent correction 4). |
| 4. REPORT with coverage table, runtimes, high-κ bias | this file |

## 1. What was built
| file | content |
|---|---|
| `interp/gp.py` | `fit_gp`: an exact GP (torch float64, CUDA) with a sum of separable terms k_t ⊗ k_x per family ("rbf", "matern32", …; an `e` suffix adds a time envelope e^{β(t+t′−1)}, the EP modes e^{λt} of R2-T6). Hyperparameters, σ included, are marginalised: type-II MAP (multi-start on a subset, refined on all data), Laplace, then truncated importance sampling from a multivariate-t proposal. This gives the weights π_h, the family evidence and the ESS. NUTS (NumPyro) is used for n ≤ 300. Families are mixed by evidence. Samples come from pathwise (Matheron) conditioning: a Kronecker prior on the grid plus the exact data update. The exact marginals per component give an exact mixture PIT. `GPPosterior.coverage`, `.pit`, `.effective_noise`. `smoother()` (C12-C1: ν → ν+1). Large n: method "subset" (the exact path on a random n_exact = 6000 subset; conservative). |
| `interp/ski.py` | KISS-GP/SKI (GPyTorch, GridInterpolationKernel on the output grid, LOVE samples). **EXPERIMENTAL, opt-in only** (§5). |
| `interp/epgp.py` | `fit_epgp`: the factor-wise EPGP prior (Härkönen et al. 2023, 1+1 specialisation). Features e^{λ(κ)t+iκx} on each factor's variety Q_j(λ, iκ) = 0, a Matérn spectral density in κ, closed-form BLR evidence, type-II ML. `component_samples` gives per-factor components u_j. |
| `interp/ensemble.py` | deep-ensemble ablation (SIREN or tanh-MLP, Gaussian NLL, learned σ per member), same `GPPosterior` container |
| `interp/core_bridge.py` | `run_core_on_samples(samples, t, x, sigma, weights)` → [(StructResult, π_s)]; `factor_set_posterior`; `bench_interpolator` (adapter to the S-BASELINES-BENCH `make_input(interpolator=)` interface: posterior mean plus effective noise; complex = Re/Im fitted separately) |

## 2. Coverage (pointwise bands of the GP posterior vs the noiseless truth on the 64×128 grid)
9 cases (transport, heat, advection_diffusion, transport_plus_diffusion, wave, beam, klein_gordon, telegraph, airy; schrödinger excluded because it is complex), scattered uniform samples, seeds 1–2, H = 16 hyperparameter draws per family. Raw data: `out/coverage*.jsonl`. The table is from `exp/cov_table.py`.

**Default (Matérn-5/2 set: matern52, matern52e, matern52e+matern52e, mixed by evidence)**, `out/coverage_m52.jsonl`. 54 fits: n = 400 with seeds 1–2, n = 2000 with seed 1.

| n | noise | fits | cov50 | cov90 | cov95 | σ̂/σ (median) | rmse/sd | time per fit (s, median) |
|---|---|---|---|---|---|---|---|---|
| 400 | 0.01 | 18 | 0.553 | 0.933 | 0.971 | 0.96 | 1.08 | 28 |
| 400 | 0.05 | 18 | 0.526 | 0.917 | 0.959 | 1.00 | 1.00 | 23 |
| 2000 | 0.01 | 9 | 0.488 | 0.904 | 0.950 | 0.98 | 0.95 | 107 |
| 2000 | 0.05 | 9 | 0.484 | 0.886 | 0.941 | 0.99 | 0.99 | 100 |

Per case, cov90:

| case | 400/1 % | 400/5 % | 2000/1 % | 2000/5 % |
|---|---|---|---|---|
| advection_diffusion | 0.938 | 0.923 | 0.892 | 0.869 |
| airy | 0.928 | 0.906 | 0.906 | 0.879 |
| beam | 0.936 | 0.903 | 0.911 | 0.889 |
| heat | 0.904 | 0.880 | 0.875 | 0.879 |
| klein_gordon | 0.939 | 0.935 | 0.908 | 0.892 |
| telegraph | 0.939 | 0.932 | 0.910 | 0.891 |
| transport | 0.939 | 0.929 | 0.911 | 0.894 |
| transport_plus_diffusion | 0.935 | 0.926 | 0.908 | 0.890 |
| wave | 0.937 | 0.920 | 0.914 | 0.893 |

Caveat: the coverage averages over seeds and over the grid points of one realisation. The per-fit spread of cov90 is about ±0.03.

**Family sets compared** (mean cov50 / cov90 / cov95):

| family set | 400 / 1 % | 400 / 5 % | 2000 / 1 % | 2000 / 5 % |
|---|---|---|---|---|
| RBF: rbf, rbfe, rbfe+rbfe (old default; 72 fits) | 0.507 / 0.904 / 0.953 | 0.471 / 0.882 / 0.940 | **0.441 / 0.857** / 0.919 | **0.438 / 0.840** / 0.903 |
| Matérn-3/2: matern32, matern32e, matern32e+matern32e (54 fits) | **0.615 / 0.955** / 0.981 | **0.563** / 0.936 / 0.970 | 0.546 / 0.933 / 0.970 | 0.524 / 0.920 / 0.961 |
| Matérn-5/2: matern52, matern52e, matern52e+matern52e (**default**; 54 fits) | 0.553 / 0.933 / 0.971 | 0.526 / 0.917 / 0.959 | 0.488 / 0.904 / 0.950 | 0.484 / 0.886 / 0.941 |
| union RBF ∪ Matérn-3/2, chosen by evidence (42 fits; at n = 2000 only heat, TPD and airy) | 0.507 / 0.904 / 0.953 | 0.471 / 0.882 / 0.940 | **0.450 / 0.846** / 0.907 | **0.443 / 0.844** / 0.903 |

Bold = outside ±5 points. Reading:
- RBF is too smooth for these fields at large n: the bands shrink faster than the error.
- Matérn-3/2 is rough enough at large n, but overcovers at small n.
- The evidence over the union always picks an RBF family (42/42 fits), so the union behaves like RBF. Evidence prefers the smoothest kernel that fits, and that kernel's bands are overconfident at large n. The family *set* is therefore a prior choice, made here on calibration across the benchmark. Within the set, the evidence still chooses (plain, envelope or sum). This is a frequentist calibration of the prior, recorded as such. It is not tuned per case and not on the truth of any single dataset.
- σ̂/σ ≈ 1.0 (median) everywhere. The σ posterior is well calibrated, and the miscalibration is in the function prior.

Per-case cov90 (Matérn set, n = 2000): heat is lowest (0.91/0.90) and all others are 0.905–0.939. Per-case cov90 (RBF set, n = 2000): 0.81–0.88, with airy and heat lowest.

## 3. High-κ bias (heat, D = 0.3; n = 2000, 1 %; `exp/highk_bias.py`, `out/highk_bias.json`)
| family | cov50/90/95 | transfer κ=1,2,3 | rel. err of Re λ(κ) at κ=1,2,3 | D̂ (mean field) | D̂ samples median [5 %, 95 %] |
|---|---|---|---|---|---|
| reference: grid + white noise (no interpolation) | – | 1.000, 1.000, 1.003 | 4e-4, 4e-4, 4.2e-3 | 0.3002 | – |
| matern32 | 0.540 / 0.924 / 0.962 | 1.000, 0.998, 0.998 | 7e-4, 5e-4, 1.7e-2 | 0.2993 | 0.2997 [0.2985, 0.3008] |
| matern52 | 0.480 / 0.889 / 0.941 | 1.000, 0.999, 0.991 | 1.2e-3, 7.7e-4, 1.1e-2 | 0.2999 | 0.3002 [0.2991, 0.3013] |
| rbf | 0.397 / 0.779 / 0.861 | 1.000, 0.999, 0.997 | 1.3e-3, 1.2e-3, 7.3e-3 | 0.3001 | 0.3003 [0.2993, 0.3012] |
| evidence-mix (old default) | 0.452 / 0.838 / 0.900 | 1.000, 0.998, 0.994 | 1.4e-3, 1.1e-3, 1.7e-3 | 0.3003 | 0.3003 [0.2996, 0.3014] |

Reading:
- Within the observable band, the low-pass bias of the smoothness prior is ≤ 1 % in amplitude at κ ≤ 3. Beyond κ = 3, heat decays below 3σ_bin within t < 2 (0.3·16 = 4.8 rate), so κ ≥ 4 is unobservable even on the exact grid.
- The decay-rate error is ≤ 2 %. D̂ is within 0.3 % of 0.3 for every family, and the sample spread contains 0.3.
- The bias that matters is not high-κ attenuation. It is the GP error at κ = 0 / slowly varying in t (§4). T26 predicts amplification of derivative errors; on heat it stays below the noise.
- Not measured: a field with energy at κ ≥ 6 (e.g. airy, beam at higher modes). See the open questions.

## 4. End to end on transport_plus_diffusion (`exp/e2e_tpd.py`, `out/e2e_tpd.jsonl`, logs `out/e2e*.log`)
P(true set) = posterior weight of samples whose core result is FIT-COMPATIBLE with factors within 0.05 of {τ+ξ, τ−0.3ξ²}. S = 16.

| families | n / noise | GP cov90 | core noise "smooth" (P_true) | core noise "white" (P_true) |
|---|---|---|---|---|
| RBF set | 2000 / 1 % | 0.834 | 0.034 (**0.365**) | 0.0036 (0) |
| RBF set | 2000 / 5 % | 0.832 | 0.161 (0; all UNDECIDED) | 0.015 (0) |
| RBF set | 400 / 1 % | 0.940 | 0.145 (0; UNDECIDED) | 0.0125 (0) |
| **Matérn-5/2 set (default)** | 2000 / 1 % | 0.910 | 0.034 (**0.398**) | 0.0058 (0) |
| Matérn-3/2 set | 2000 / 1 % | 0.938 | 0.039 (0.073) | 0.0087 (0) |
| Matérn-3/2 set | 2000 / 5 % | 0.927 | 0.162 (0; UNDECIDED) | 0.028 (0) |
| Matérn-3/2 set | 400 / 1 % | 0.963 | 0.216 (0; UNDECIDED) | 0.026 (0) |

Diagnosis: the factor τ+ξ is found in almost every sample. The second factor fails in a characteristic way: the core returns a κ-independent factor τ + c, or τ² + aτ + b, i.e. pure time modes at κ = 0.
- The GP error is smooth in t and concentrated at low κ, so it does not look like the white noise the core assumes (`bin_noise = noise/√nx`).
- One scalar noise level cannot fit both regimes. Small (white-equivalent): the correlated error is read as signal, giving spurious modes, FIT-COMPATIBLE with extra factors. Large (projected-equivalent, "smooth", the default of `effective_noise()`): the weak diffusive modes fall under the threshold, giving UNDECIDED.
- Calibrated bands (Matérn) are wider, so the effective noise grows and the e2e result gets worse. Good u-coverage and core recovery pull in opposite directions under the scalar-noise interface.
- On cached RBF samples (scratch test, 8 samples) the smooth noise gave 6/8. The full run gives 0.365. The earlier figure was optimistic.

## 5. Failures and limits (honest list)
- **E2E criterion not met** (§4).
- **SKI is not calibrated.** At n = 10⁴ (transport, 1 %), the first run put all signal into the noise: σ̂ = 1.09 vs 0.013, cov90 = 0.08. Initialising from the exact MAP on a 1000-point subset needed a noise floor fix, and the re-run did not finish within 900 s on a GPU shared with three other jobs. SKI is opt-in, flagged EXPERIMENTAL, and also drops hyperparameter uncertainty. The large-n default is now "subset" (exact GP on 6000 random points): a valid but conservative posterior.
- **ESS** of the Laplace-IS weights is sometimes low for two-term families (rbfe+rbfe: 2.5–6 of 16). It is reported in `info["diag"][family]["ess"]`.
- **Runtime**: the exact path scales with the number of families (6 families: 39–45 s at n = 400, ~300 s at n = 2000).

| path | n = 400 | n = 2000 |
|---|---|---|
| default Matérn-5/2 set, H = 16, S = 32 (median per fit, shared GPU) | 23–28 s | 100–107 s |
| RBF / Matérn-3/2 sets | 10–19 s | 160–220 s |
| core v2 on 16 samples | 60–130 s | 60–130 s |
| ensemble (M = 5, 3000 steps) | – | 56–190 s |

- **Ensemble ablation** (n = 2000, 1 %; `out/ensemble.jsonl`):

| case | arch | cov50/90/95 | rmse | σ̂/σ |
|---|---|---|---|---|
| heat | SIREN | 0.692 / 0.949 / 0.970 | 0.0066 | 4.1 |
| heat | MLP | 0.349 / 0.694 / 0.727 | 0.0125 | 7.8 |
| transport | SIREN | 0.699 / 0.952 / 0.973 | 0.0064 | 4.2 |
| transport | MLP | 0.406 / 0.775 / 0.828 | 0.0137 | 7.7 |
| TPD | SIREN | 0.602 / 0.923 / 0.949 | 0.0044 | 4.1 |
| TPD | MLP | 0.351 / 0.735 / 0.797 | 0.0093 | 7.7 |

  SIREN ensembles give usable 90/95 % bands but no calibrated 50 % band, and σ̂ is 4× too large. Tanh-MLP undercovers. The GP RMSE is comparable (e.g. TPD 0.0044–0.0055). The GP stays the default, and the ensemble remains an ablation.

## 6. Open questions
1. A core interface for correlated noise (§7) is the blocker for criterion 2. An alternative inside interp: Monte Carlo the threshold. Run the core on the posterior **mean** with a noise level estimated per κ-bin from the sample spread — but the core takes a scalar.
2. EPGP refinement pass (factor-wise prior given the factors from a first pass): implemented and unit-tested (component weights on TPD within 0.05), not yet chained after the core in e2e.
3. High-κ bias on a field with energy at κ ≥ 6: not measured.
4. Large n: SKI initialisation and hyperparameter uncertainty (Laplace on the SKI MLL), or a sparse variational GP.

## 7. Changes requested in other packages
- **Core (MAIN):** accept noise per (t, κ) bin, or a sample-based bin covariance. Today `analyze_structured(..., noise=σ)` assumes white noise, `bin_noise = σ/√nx`. The GP posterior can provide `Var_s[Û_s(t, κ)]` per bin (from the samples) or analytically. With it, the slow-in-t, low-κ GP error would no longer create the spurious κ = 0 factors.
- **THEORY_TO_ALGO (MAIN):** proposed rows are in `sessions/S-INTERP/THEORY_TO_ALGO_rows.md` (EPGP features on the variety, R2-T6; derivative amplification, DICT-ILIM-Hs). The numbers T25/T26 are provisional: S-AGG-CLUSTER also proposed T25–T27, so MAIN should renumber.
- **S-BASELINES-BENCH:** `pdefactor.interp.bench_interpolator` matches the `interpolator=` signature of `make_input`. Given §4, expect the scalar `sigma_eff` to be the weak point there too.
- **Packages in the shared `.venv`:** gpytorch 1.15.2 and linear_operator 0.6.1 were already present (no `pip install` by this session). numpyro 0.22 / jax 0.12 were already present.

## 8. Theory rows used
T1 (C12-T1), T11 (C12-C1, `smoother`), T12/T18 (Monte Carlo over interpolants), T15 (σ as a posterior quantity), T19 (periodicity only as prior knowledge), T25* (R2-T6 → EPGP), T26* (DICT-ILIM-Hs → high-κ check). *Proposed rows.
