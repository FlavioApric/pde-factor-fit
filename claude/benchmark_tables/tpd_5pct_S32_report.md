# Final report

## 1. PDE

- equation: `(1.0*tau + 0.9999*xi) * (1.0*tau - 0.2973*xi**2) u = 0`
- grid nt×nx = 64×128, T = 2, L = 6.283, sigma = 0.02646, samples = 32
- truth: `tau + 1.0*xi` · `tau - 0.3*xi**2` — factor set matches: **True** (worst rel. err 0.009156)

## 2. Model chosen

- label: **FIT-COMPATIBLE**
- bounds (m, dx): [3, 4], regrouped: True
- P(k): {'2': 1.0}
- core labels: {'FIT-COMPATIBLE': 1.0}
- dropped as redundant: none
- note: structure ((1, 1), (1, 2)) chosen by data-level evidence; all samples regrouped at it.

| structure | posterior | log evidence |
|---|---|---|
| ((1, 1), (1, 2)) | 1.000 | -409.5 |

## 3. Posterior / distribution

- k_eff = 1.721 (k_det = 2), per sample q05/50/95 = 1.666/1.718/1.785
- P(k) structures {'2': 1.0}; DP {'2': 1.0}; finite-BIC {'1': 6.82284399768789e-51, '2': 0.9999999891775239, '3': 1.0822476167456002e-08, '4': 9.01223602583602e-17}
- tracks: W=0.233 `tau - 0.3118229577*xi**2 + 0.0286664507*xi - 0.0882078308`; W=0.767 `tau + 1.0006431319*xi + 0.0111221882`
- c_F q05/50/95: 0.8171/0.8276/0.84; gamma: 0.16/0.1716/0.1829
- cloud size 64; theta_bar and its sd are in report.json

## 4. Factors

### factor 0: `1.0*tau + 0.9998797712*xi + 0.0037532661`

- W = 0.7672, status: clean (component alone: k=1, label FIT-COMPATIBLE), kappa support: [1.0, 2.0, 3.0, 4.0]
- fit: 8 kernel modes, alone explains 97.68% (rel. residual 0.152); ‖u_j‖ = 81.61, weight from u_j = 0.7691

| term | median | q05 | q95 |
|---|---|---|---|
| tau^0 xi^0 | 0.0037533 | -0.0062112 | 0.011122 |
| tau^0 xi^1 | 0.99988 | 0.99561 | 1.0045 |
| tau^1 xi^0 | 1 | 1 | 1 |

### factor 1: `1.0*tau - 0.2972533186*xi**2 + 0.0037177101*xi + 0.0028059608`

- W = 0.2328, status: clean (component alone: k=1, label FIT-COMPATIBLE), kappa support: [1.0, 2.0, 3.0]
- fit: 8 kernel modes, alone explains 69.96% (rel. residual 0.548); ‖u_j‖ = 24.5, weight from u_j = 0.2309

| term | median | q05 | q95 |
|---|---|---|---|
| tau^0 xi^0 | 0.002806 | -0.084409 | 0.090868 |
| tau^0 xi^1 | 0.0037177 | -0.023684 | 0.035753 |
| tau^0 xi^2 | -0.29725 | -0.32388 | -0.27696 |
| tau^1 xi^0 | 1 | 1 | 1 |

## 5. Fit per loop level

- joint relative residual of the mean field on all kernels: 0.005855

| bounds | p_fit | held-out (mean, se) | accepted | note |
|---|---|---|---|---|
| [3, 4] | 1.000 | None | True |  |

## 6. Friedrichs / superposition layer

- gamma_N (block Gram) = 0.1713, c_F = 0.8287, intersection dim 0, error amplification gamma_N^-1/2 = 2.416
- P(split) = 1.000, c_F = 0.8274, gamma = 0.1726, P(include) = [1.0, 1.0]
- weights w_j mean [q05, q50, q95]: 0.7685 [0.7663, 0.7685, 0.7704]; 0.2315 [0.2296, 0.2315, 0.2337]
- P(subset): {'(0,)': 0.0, '(1,)': 0.0, '(0, 1)': 1.0}
- pairwise (display only, γ_N above is the headline): operator-norm distance [[0.0, 0.6943], [0.6943, 0.0]], Friedrichs angle (rad) [[0.0, 0.594], [0.594, 0.0]]

## 7. Interaction term E_int

- rho = ‖E_int‖/‖u(T)-u0‖: {'q05': 0.01230652689118326, 'q50': 0.03043960092237516, 'q95': 0.06856693728810416, 'mean': 0.033171782205441036} — computed
- domain blocks/share: none (report_domain off)

## 8. Parameters

| name | value |
|---|---|
| loop.START_BOUNDS | (3, 4) |
| loop.DX_LIMIT | 8 |
| loop.M_LIMIT | 4 |
| loop.P_CONCENTRATED | 0.9 |
| loop.CAP | 3.0 |
| loop.PRED_LOGP | -3.0 |
| loop.EPS_GRID | [0.0001, 0.00021690521830457362, 0.0004704787372775475, 0.0010204929321684646, 0 |
| loop.MERGE_DX0 | True |
| loop.W_DRAWS | 16 |
| loop.GROW_PAST | False |
| loop.GROW_PAST_M | 1 |
| loop.GROW_PAST_DX | 2 |
| loop.GROW_PAST_STEPS | 2 |
| loop.LOG_BF_STRONG | 5.0106352940962555 |
| loop.LOG_BF_BARE | 1.0 |
| loop.SPLIT_PROPOSE | 0.05 |
| loop.SPLIT_CI | False |
| loop.ALT_MIN_MASS | 1e-06 |
| loop.ALT_TOP | None |
| loop.SPLIT_BEATS | True |
| loop.EXACT_SPLIT | True |
| loop.EPGP_REINTERP | False |
| loop.RAW_GOF | True |
| loop.PATH_CLASS | True |
| loop.GRID_SMOOTH_GOF | True |
| loop.FIT_GUARD | 0 |
| loop.ALT_PRE | False |
| loop.CONJ_HALF | True |
| loop.SPLIT_FINEST | True |
| loop.RAW_GOF_FINAL | True |
| loop.PATH_FULL | True |
| loop.IDKER_FINAL | False |
| aggregate.M_MAX | 2 |
| aggregate.DX_MAX | 4 |
| aggregate.CONCENTRATION_GRID | (0.001, 0.01, 0.1, 1.0, 10.0) |
| bayes_split.TAU2_GRID | [1e-08, 1.7782794100389228e-08, 3.162277660168379e-08, 5.6234132519034905e-08, 1 |
| core.structfit.SEED_PROVIDER | None |

- env overrides: none (defaults)
- run_loop kwargs: {'case': 'transport_plus_diffusion', 'noise': 0.05, 'S': 32, 'seed': 0}
- meanings: analysis/PARAMETERS.md (meaning, defaults, verdicts)

## 9. Images

- frequency grid {'kappa': 120, 're_tau': 96, 'im_tau': 96} pixels over box {'kappa': [-5.0, 5.0], 're_tau': [-8.922, 8.922], 'im_tau': [-6.0, 6.0]}
![directions.png](directions.png)
![directions_uncertainty.png](directions_uncertainty.png)
![operator_space.png](operator_space.png)
![modes_and_components.png](modes_and_components.png)
![distributions.png](distributions.png)
