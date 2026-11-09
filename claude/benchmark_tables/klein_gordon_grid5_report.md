# Final report

## 1. PDE

- equation: `(1.0*tau**2 - 0.9997*xi**2 + 0.9996) u = 0`
- grid nt×nx = 64×128, T = 2, L = 6.283, sigma = 0.05273, samples = 1
- truth: `tau**2 - xi**2 + 1.0` — factor set matches: **True** (worst rel. err 0.0003922)

## 2. Model chosen

- label: **FIT-COMPATIBLE**
- bounds (m, dx): [3, 4], regrouped: True
- P(k): {'1': 1.0}
- core labels: {'FIT-COMPATIBLE': 1.0}
- dropped as redundant: none
- note: structure ((2, 2),) chosen by data-level evidence; all samples regrouped at it. factors refined on the observations (log evidence 12379.7 -> 12379.2, 2 real coefficient(s) kept by evidence). coefficient intervals from 16 parametric-bootstrap refits at the final structure.

| structure | posterior | log evidence |
|---|---|---|
| ((2, 2),) | 1.000 | -800.9 |

## 3. Posterior / distribution

- k_eff = 1.000 (k_det = 1), per sample q05/50/95 = 1/1/1
- P(k) structures {'1': 1.0}; DP {'1': 1.0}; finite-BIC {'1': 1.0}
- tracks: W=1.000 `tau**2 - 0.9988978338*xi**2 + 0.0024537023*xi + 1.0027355734`
- c_F q05/50/95: 0/0/0; gamma: 1/1/1
- cloud size 1; theta_bar and its sd are in report.json

## 4. Factors

### factor 0: `1.0*tau**2 - 0.999726652904698*xi**2 + 0.999607753911417`

- W = 1.0000, status: not checked; refined on the observations (terms tau^0 xi^1 dropped by evidence), kappa support: [1.0, 2.0, 3.0, 4.0]
- fit: 16 kernel modes, alone explains 99.92% (rel. residual 0.0288); ‖u_j‖ = 167.6, weight from u_j = 1.0000

| term | median | q05 | q95 |
|---|---|---|---|
| tau^0 xi^0 | 0.99961 | 0.99519 | 1.0051 |
| tau^0 xi^2 | -0.99973 | -1.002 | -0.9977 |
| tau^2 xi^0 | 1 | 1 | 1 |

## 5. Fit per loop level

- joint relative residual of the mean field on all kernels: 0.02876

| bounds | p_fit | held-out (mean, se) | accepted | note |
|---|---|---|---|---|
| [3, 4] | 1.000 | None | True |  |

## 6. Friedrichs / superposition layer

- pairwise (display only, γ_N above is the headline): operator-norm distance [[0.0]], Friedrichs angle (rad) [[0.0]]

## 7. Interaction term E_int

- rho = ‖E_int‖/‖u(T)-u0‖: {'q05': 0.0, 'q50': 0.0, 'q95': 0.0, 'mean': 0.0} — not computed by core v2 (structfit); reported for completeness
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
- run_loop kwargs: {'case': 'klein_gordon', 'noise': 0.05, 'seed': 0, 'protocol': 'bench_e2e grid', 'bootstrap': 16}
- meanings: analysis/PARAMETERS.md (meaning, defaults, verdicts)

## 9. Images

- frequency grid {'kappa': 120, 're_tau': 96, 'im_tau': 96} pixels over box {'kappa': [-5.0, 5.0], 're_tau': [-0.001, 0.001], 'im_tau': [-6.119, 6.119]}
![directions.png](directions.png)
![directions_uncertainty.png](directions_uncertainty.png)
![operator_space.png](operator_space.png)
![modes_and_components.png](modes_and_components.png)
![distributions.png](distributions.png)
