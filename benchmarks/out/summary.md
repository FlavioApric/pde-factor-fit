# Benchmark summary

rows: 3920, method errors (crashes): 0. Scattered inputs use the griddata PLACEHOLDER interpolator.

## Factor-set recovery: rate (n runs) / median coef_err of correct runs

| method | sampling | σ=0 | σ=0.001 | σ=0.01 | σ=0.05 |
|---|---|---|---|---|---|
| core_v2 | grid | 1.00 (10) / 0e+00 | 1.00 (50) / 2e-05 | 1.00 (50) / 3e-04 | 0.90 (50) / 2e-03 |
| core_v2 | 2000 | 0.66 (50) / 3e-03 | 0.68 (50) / 3e-03 | 0.70 (50) / 3e-03 | 0.70 (50) / 5e-03 |
| core_v2 | 400 | 0.18 (50) / 1e-02 | 0.18 (50) / 1e-02 | 0.22 (50) / 1e-02 | 0.22 (50) / 2e-02 |
| core_v1 | grid | 1.00 (10) / 0e+00 | 0.66 (50) / 7e-05 | 0.60 (50) / 5e-04 | 0.56 (50) / 4e-03 |
| core_v1 | 2000 | 0.50 (50) / 6e-03 | 0.52 (50) / 7e-03 | 0.52 (50) / 5e-03 | 0.48 (50) / 1e-02 |
| core_v1 | 400 | 0.22 (50) / 1e-02 | 0.22 (50) / 1e-02 | 0.24 (50) / 2e-02 | 0.20 (50) / 1e-02 |
| pdefind | grid | 1.00 (10) / 5e-07 | 0.30 (50) / 3e-02 | 0.10 (50) / 2e-03 | 0.00 (50) / — |
| pdefind | 2000 | 0.10 (50) / 1e-04 | 0.10 (50) / 2e-04 | 0.10 (50) / 8e-04 | 0.10 (50) / 3e-02 |
| pdefind | 400 | 0.10 (50) / 7e-03 | 0.10 (50) / 8e-03 | 0.08 (50) / 8e-03 | 0.08 (50) / 2e-02 |
| weak_sindy | grid | 1.00 (10) / 3e-04 | 1.00 (50) / 3e-04 | 0.90 (50) / 9e-04 | 0.62 (50) / 1e-02 |
| weak_sindy | 2000 | 0.76 (50) / 7e-04 | 0.76 (50) / 7e-04 | 0.72 (50) / 4e-03 | 0.50 (50) / 1e-02 |
| weak_sindy | 400 | 0.46 (50) / 1e-02 | 0.46 (50) / 1e-02 | 0.48 (50) / 1e-02 | 0.50 (50) / 2e-02 |
| ensemble_sindy | grid | 1.00 (10) / 2e-04 | 1.00 (50) / 3e-04 | 0.82 (50) / 6e-04 | 0.58 (50) / 2e-02 |
| ensemble_sindy | 2000 | 0.76 (50) / 1e-03 | 0.72 (50) / 1e-03 | 0.68 (50) / 5e-03 | 0.54 (50) / 2e-02 |
| ensemble_sindy | 400 | 0.48 (50) / 2e-02 | 0.48 (50) / 2e-02 | 0.44 (50) / 1e-02 | 0.44 (50) / 2e-02 |
| sbr_sindy | grid | 1.00 (10) / 4e-04 | 0.92 (50) / 3e-04 | 0.72 (50) / 2e-03 | 0.58 (50) / 1e-02 |
| sbr_sindy | 2000 | 0.68 (50) / 4e-03 | 0.68 (50) / 4e-03 | 0.68 (50) / 1e-02 | 0.56 (50) / 2e-02 |
| sbr_sindy | 400 | 0.48 (50) / 2e-02 | 0.48 (50) / 2e-02 | 0.46 (50) / 1e-02 | 0.50 (50) / 2e-02 |
| bopdmd | grid | 0.50 (10) / 2e-04 | 0.06 (50) / 3e-02 | 0.04 (50) / 5e-02 | 0.02 (50) / 5e-02 |
| bopdmd | 2000 | 0.00 (50) / — | 0.00 (50) / — | 0.00 (50) / — | 0.00 (50) / — |
| bopdmd | 400 | 0.00 (50) / — | 0.00 (50) / — | 0.00 (50) / — | 0.00 (50) / — |

## Full grid, per case: factor-set rate at σ = 0, 0.001, 0.01, 0.05

| case | core_v2 | core_v1 | pdefind | weak_sindy | ensemble_sindy | sbr_sindy | bopdmd |
|---|---|---|---|---|---|---|---|
| transport | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 0.6 0.2 0.0 |
| heat | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 0.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 0.0 0.0 0.0 |
| advection_diffusion | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 0.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 |
| transport_plus_diffusion | 1.0 1.0 1.0 0.2 | 1.0 0.0 0.0 0.0 | 1.0 0.0 0.0 0.0 | 1.0 1.0 0.6 0.0 | 1.0 1.0 0.2 0.0 | 1.0 0.2 0.0 0.0 | 0.0 0.0 0.0 0.0 |
| wave | 1.0 1.0 1.0 1.0 | 1.0 1.0 0.6 0.4 | 1.0 0.0 0.0 0.0 | 1.0 1.0 0.6 0.2 | 1.0 1.0 0.4 0.0 | 1.0 1.0 0.2 0.0 | 1.0 0.0 0.0 0.0 |
| beam | 1.0 1.0 1.0 0.8 | 1.0 0.6 0.4 0.0 | 1.0 0.0 0.0 0.0 | 1.0 1.0 1.0 0.0 | 1.0 1.0 0.8 0.0 | 1.0 1.0 0.0 0.0 | 0.0 0.0 0.0 0.0 |
| klein_gordon | 1.0 1.0 1.0 1.0 | 1.0 0.0 0.0 0.0 | 1.0 0.0 0.0 0.0 | 1.0 1.0 1.0 0.6 | 1.0 1.0 1.0 0.4 | 1.0 1.0 1.0 0.4 | 1.0 0.0 0.0 0.0 |
| telegraph | 1.0 1.0 1.0 1.0 | 1.0 0.0 0.0 0.2 | 1.0 0.0 0.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 0.4 | 1.0 0.0 0.0 0.0 |
| airy | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 0.0 0.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.2 0.2 |
| schrodinger | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 0.0 0.0 0.0 | 1.0 1.0 0.8 0.4 | 1.0 1.0 0.8 0.4 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 |

## 2000 scattered, per case

| case | core_v2 | core_v1 | pdefind | weak_sindy | ensemble_sindy | sbr_sindy | bopdmd |
|---|---|---|---|---|---|---|---|
| transport | 0.8 0.8 0.8 1.0 | 1.0 0.8 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 |
| heat | 0.8 0.8 1.0 1.0 | 0.8 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 |
| advection_diffusion | 0.8 0.8 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 |
| transport_plus_diffusion | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.2 0.0 0.0 | 0.2 0.2 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 |
| wave | 0.6 0.6 0.8 0.8 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.4 0.4 0.2 0.2 | 0.2 0.2 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 |
| beam | 0.6 0.6 0.6 0.4 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 1.0 0.8 0.8 0.0 | 1.0 0.6 0.8 0.0 | 0.0 0.0 0.2 0.0 | 0.0 0.0 0.0 0.0 |
| klein_gordon | 0.8 0.8 0.6 0.4 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 1.0 1.0 0.8 0.0 | 1.0 1.0 0.6 0.2 | 1.0 1.0 0.8 0.4 | 0.0 0.0 0.0 0.0 |
| telegraph | 0.6 0.6 0.4 0.4 | 0.4 0.4 0.2 0.0 | 0.0 0.0 0.0 0.0 | 1.0 1.0 1.0 0.4 | 1.0 1.0 1.0 0.8 | 1.0 1.0 0.8 0.2 | 0.0 0.0 0.0 0.0 |
| airy | 0.8 0.8 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 |
| schrodinger | 0.8 1.0 0.8 1.0 | 0.8 1.0 1.0 0.8 | 0.0 0.0 0.0 0.0 | 0.2 0.2 0.4 0.4 | 0.2 0.2 0.4 0.4 | 0.8 0.8 1.0 1.0 | 0.0 0.0 0.0 0.0 |

## 400 scattered, per case

| case | core_v2 | core_v1 | pdefind | weak_sindy | ensemble_sindy | sbr_sindy | bopdmd |
|---|---|---|---|---|---|---|---|
| transport | 0.2 0.2 0.2 0.2 | 0.6 0.6 0.6 0.6 | 1.0 1.0 0.8 0.8 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 |
| heat | 0.2 0.2 0.2 0.2 | 0.6 0.6 0.6 0.4 | 0.0 0.0 0.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 |
| advection_diffusion | 0.4 0.4 0.8 0.6 | 0.4 0.4 0.6 0.4 | 0.0 0.0 0.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 |
| transport_plus_diffusion | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 |
| wave | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.2 0.2 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 |
| beam | 0.0 0.0 0.0 0.2 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 |
| klein_gordon | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.2 0.2 0.2 0.2 | 0.2 0.2 0.0 0.0 | 0.2 0.2 0.2 0.2 | 0.0 0.0 0.0 0.0 |
| telegraph | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.2 0.2 0.4 0.6 | 0.2 0.2 0.2 0.4 | 0.2 0.2 0.0 0.0 | 0.0 0.0 0.0 0.0 |
| airy | 0.8 0.8 0.8 0.8 | 0.6 0.6 0.6 0.6 | 0.0 0.0 0.0 0.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 1.0 1.0 1.0 1.0 | 0.0 0.0 0.0 0.0 |
| schrodinger | 0.2 0.2 0.2 0.2 | 0.0 0.0 0.0 0.0 | 0.0 0.0 0.0 0.0 | 0.2 0.2 0.2 0.2 | 0.2 0.2 0.2 0.0 | 0.4 0.4 0.4 0.8 | 0.0 0.0 0.0 0.0 |

## Exact structure (degrees, |c| ≥ 1e-2) rate

| method | grid | 2000 | 400 |
|---|---|---|---|
| core_v2 | 0.99 | 0.70 | 0.30 |
| core_v1 | 0.66 | 0.58 | 0.32 |
| pdefind | 0.38 | 0.33 | 0.37 |
| weak_sindy | 0.85 | 0.71 | 0.54 |
| ensemble_sindy | 0.82 | 0.69 | 0.54 |
| sbr_sindy | 0.76 | 0.60 | 0.48 |
| bopdmd | 0.14 | 0.03 | 0.00 |

## Core labels

| method | sampling | σ | FIT-COMPATIBLE | MISFIT | ID-KER | UNDECIDED | ERROR |
|---|---|---|---|---|---|---|---|
| core_v2 | grid | 0 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| core_v2 | grid | 0.001 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| core_v2 | grid | 0.01 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| core_v2 | grid | 0.05 | 0.94 | 0.00 | 0.00 | 0.06 | 0.00 |
| core_v2 | 2000 | 0 | 0.92 | 0.00 | 0.02 | 0.06 | 0.00 |
| core_v2 | 2000 | 0.001 | 0.94 | 0.00 | 0.02 | 0.04 | 0.00 |
| core_v2 | 2000 | 0.01 | 0.90 | 0.00 | 0.06 | 0.04 | 0.00 |
| core_v2 | 2000 | 0.05 | 0.84 | 0.00 | 0.08 | 0.08 | 0.00 |
| core_v2 | 400 | 0 | 0.74 | 0.00 | 0.16 | 0.10 | 0.00 |
| core_v2 | 400 | 0.001 | 0.78 | 0.00 | 0.12 | 0.10 | 0.00 |
| core_v2 | 400 | 0.01 | 0.82 | 0.00 | 0.08 | 0.10 | 0.00 |
| core_v2 | 400 | 0.05 | 0.78 | 0.00 | 0.10 | 0.12 | 0.00 |
| core_v1 | grid | 0 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| core_v1 | grid | 0.001 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| core_v1 | grid | 0.01 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| core_v1 | grid | 0.05 | 0.94 | 0.00 | 0.06 | 0.00 | 0.00 |
| core_v1 | 2000 | 0 | 0.82 | 0.02 | 0.16 | 0.00 | 0.00 |
| core_v1 | 2000 | 0.001 | 0.80 | 0.02 | 0.18 | 0.00 | 0.00 |
| core_v1 | 2000 | 0.01 | 0.86 | 0.00 | 0.14 | 0.00 | 0.00 |
| core_v1 | 2000 | 0.05 | 0.86 | 0.02 | 0.12 | 0.00 | 0.00 |
| core_v1 | 400 | 0 | 0.50 | 0.22 | 0.28 | 0.00 | 0.00 |
| core_v1 | 400 | 0.001 | 0.52 | 0.20 | 0.28 | 0.00 | 0.00 |
| core_v1 | 400 | 0.01 | 0.54 | 0.20 | 0.26 | 0.00 | 0.00 |
| core_v1 | 400 | 0.05 | 0.42 | 0.26 | 0.32 | 0.00 | 0.00 |

## Weight error (cores, runs with right factor set, beam excluded): median [IQR]

| method | grid | 2000 | 400 |
|---|---|---|---|
| core_v2 | 0.0e+00 [0e+00, 0e+00] (n=140) | 0.0e+00 [0e+00, 0e+00] (n=126) | 0.0e+00 [0e+00, 0e+00] (n=39) |
| core_v1 | 0.0e+00 [0e+00, 0e+00] (n=95) | 0.0e+00 [0e+00, 0e+00] (n=101) | 0.0e+00 [0e+00, 0e+00] (n=44) |

## Calibration of structure probabilities

| method | sampling | pairs | runs | ECE | Brier | mean p(true) |
|---|---|---|---|---|---|---|
| core_v2 | grid | 4116 | 160 | 0.006 | 0.002 | 0.88 |
| core_v2 | 2000 | 4812 | 200 | 0.019 | 0.027 | 0.54 |
| core_v2 | 400 | 4648 | 200 | 0.053 | 0.051 | 0.25 |
| core_v2 | all | 13576 | 560 | 0.023 | 0.028 | 0.53 |
| ensemble_sindy | grid | 303 | 160 | 0.152 | 0.199 | 0.73 |
| ensemble_sindy | 2000 | 402 | 200 | 0.269 | 0.311 | 0.59 |
| ensemble_sindy | 400 | 533 | 200 | 0.338 | 0.378 | 0.35 |
| ensemble_sindy | all | 1238 | 560 | 0.267 | 0.313 | 0.54 |
| sbr_sindy | grid | 291 | 160 | 0.250 | 0.281 | 0.67 |
| sbr_sindy | 2000 | 446 | 200 | 0.330 | 0.369 | 0.49 |
| sbr_sindy | 400 | 548 | 200 | 0.386 | 0.403 | 0.31 |
| sbr_sindy | all | 1285 | 560 | 0.323 | 0.364 | 0.48 |

## Rounding sensitivity of the baselines (full grid)

| method | d=1 | d=2 (default) | d=3 |
|---|---|---|---|
| pdefind | 0.18 | 0.19 | 0.19 |
| weak_sindy | 0.82 | 0.85 | 0.73 |
| ensemble_sindy | 0.81 | 0.81 | 0.73 |
| sbr_sindy | 0.80 | 0.76 | 0.66 |
| bopdmd | 0.08 | 0.08 | 0.08 |

## Slope of coef_err vs noise (full grid)

| method | slope | noises used |
|---|---|---|
| core_v2 | 1.25 | 3 |
| core_v1 | 1.03 | 3 |
| pdefind | -1.26 | 2 |
| weak_sindy | 0.88 | 3 |
| ensemble_sindy | 0.99 | 3 |
| sbr_sindy | 0.95 | 3 |

## Runtime per run (s): median [IQR]

| method | grid | 2000 | 400 | total (s) |
|---|---|---|---|---|
| core_v2 | 1.08 [0.57, 3.34] | 1.10 [0.51, 4.42] | 0.87 [0.41, 2.35] | 1572 |
| core_v1 | 0.10 [0.06, 0.14] | 0.12 [0.06, 0.20] | 0.09 [0.03, 0.16] | 69 |
| pdefind | 0.61 [0.47, 0.94] | 0.60 [0.47, 0.89] | 0.56 [0.46, 0.83] | 524 |
| weak_sindy | 2.67 [2.17, 3.30] | 2.53 [2.08, 3.20] | 2.41 [2.06, 2.95] | 1607 |
| ensemble_sindy | 4.25 [3.43, 5.65] | 3.88 [3.39, 5.19] | 3.95 [3.44, 4.50] | 2712 |
| sbr_sindy | 12.38 [10.44, 17.35] | 11.80 [10.33, 14.96] | 11.52 [9.70, 13.55] | 7470 |
| bopdmd | 1.61 [1.28, 2.84] | 1.25 [0.88, 2.45] | 1.17 [0.75, 3.36] | 1791 |

## Full-grid cells below rate 1

- bopdmd · advection_diffusion · σ=0.0: rate 0.0; labels {'n/a': 1}; structures {'[]': 1}
- bopdmd · advection_diffusion · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 3, '[[1, 3]]': 2}
- bopdmd · advection_diffusion · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 3, '[[2, 0]]': 1}
- bopdmd · advection_diffusion · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[]': 3, '[[1, 0]]': 2}
- bopdmd · airy · σ=0.0: rate 0.0; labels {'n/a': 1}; structures {'[[1, 0], [1, 0], [1, 3]]': 1}
- bopdmd · airy · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[1, 3]]': 5}
- bopdmd · airy · σ=0.01: rate 0.2; labels {'n/a': 5}; structures {'[]': 3, '[[3, 0]]': 1}
- bopdmd · airy · σ=0.05: rate 0.2; labels {'n/a': 5}; structures {'[[3, 0]]': 3, '[[1, 0], [1, 0]]': 1}
- bopdmd · beam · σ=0.0: rate 0.0; labels {'n/a': 1}; structures {'[[2, 4]]': 1}
- bopdmd · beam · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 3, '[[3, 3]]': 1}
- bopdmd · beam · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[3, 0]]': 3, '[[2, 0]]': 1}
- bopdmd · beam · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 2, '[[1, 0]]': 2}
- bopdmd · heat · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 3, '[[1, 0], [1, 0]]': 2}
- bopdmd · heat · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 0]]': 4, '[]': 1}
- bopdmd · heat · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 5}
- bopdmd · klein_gordon · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 2, '[[2, 2]]': 2}
- bopdmd · klein_gordon · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 4, '[[3, 0]]': 1}
- bopdmd · klein_gordon · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 5}
- bopdmd · schrodinger · σ=0.0: rate 0.0; labels {'n/a': 1}; structures {'[[1, 1]]': 1}
- bopdmd · schrodinger · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[3, 0]]': 3, '[[3, 2]]': 2}
- bopdmd · schrodinger · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[3, 0]]': 3, '[]': 1}
- bopdmd · schrodinger · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[3, 0]]': 3, '[[3, 4]]': 1}
- bopdmd · telegraph · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 2, '[]': 2}
- bopdmd · telegraph · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 4, '[]': 1}
- bopdmd · telegraph · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 4, '[[3, 0]]': 1}
- bopdmd · transport · σ=0.001: rate 0.6; labels {'n/a': 5}; structures {'[[1, 1]]': 4, '[[1, 0]]': 1}
- bopdmd · transport · σ=0.01: rate 0.2; labels {'n/a': 5}; structures {'[[1, 1]]': 4, '[[1, 3]]': 1}
- bopdmd · transport · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[]': 3, '[[1, 1]]': 1}
- bopdmd · transport_plus_diffusion · σ=0.0: rate 0.0; labels {'n/a': 1}; structures {'[[3, 2]]': 1}
- bopdmd · transport_plus_diffusion · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 2, '[[1, 0]]': 2}
- bopdmd · transport_plus_diffusion · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- bopdmd · transport_plus_diffusion · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 4, '[[2, 0]]': 1}
- bopdmd · wave · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[2, 0]]': 2, '[[2, 2]]': 1}
- bopdmd · wave · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[2, 2]]': 5}
- bopdmd · wave · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[3, 0]]': 2, '[[2, 2]]': 2}
- core_v1 · beam · σ=0.001: rate 0.6; labels {'FIT-COMPATIBLE': 5}; structures {'[[1, 2], [1, 2]]': 3, '[[2, 4]]': 2}
- core_v1 · beam · σ=0.01: rate 0.4; labels {'FIT-COMPATIBLE': 5}; structures {'[[2, 4]]': 3, '[[1, 2], [1, 2]]': 2}
- core_v1 · beam · σ=0.05: rate 0.0; labels {'FIT-COMPATIBLE': 4, 'ID-KER': 1}; structures {'[[1, 2], [1, 2]]': 4, '[[1, 3], [1, 4], [1, 4]]': 1}
- core_v1 · klein_gordon · σ=0.001: rate 0.0; labels {'FIT-COMPATIBLE': 5}; structures {'[[1, 2], [1, 2]]': 5}
- core_v1 · klein_gordon · σ=0.01: rate 0.0; labels {'FIT-COMPATIBLE': 5}; structures {'[[1, 2], [1, 2]]': 5}
- core_v1 · klein_gordon · σ=0.05: rate 0.0; labels {'FIT-COMPATIBLE': 5}; structures {'[[1, 2], [1, 2]]': 5}
- core_v1 · telegraph · σ=0.001: rate 0.0; labels {'FIT-COMPATIBLE': 5}; structures {'[[1, 2], [1, 2]]': 5}
- core_v1 · telegraph · σ=0.01: rate 0.0; labels {'FIT-COMPATIBLE': 5}; structures {'[[1, 2], [1, 2]]': 5}
- core_v1 · telegraph · σ=0.05: rate 0.2; labels {'FIT-COMPATIBLE': 5}; structures {'[[1, 2], [1, 2]]': 4, '[[2, 2]]': 1}
- core_v1 · transport_plus_diffusion · σ=0.001: rate 0.0; labels {'FIT-COMPATIBLE': 5}; structures {'[[2, 3]]': 5}
- core_v1 · transport_plus_diffusion · σ=0.01: rate 0.0; labels {'FIT-COMPATIBLE': 5}; structures {'[[2, 3]]': 5}
- core_v1 · transport_plus_diffusion · σ=0.05: rate 0.0; labels {'FIT-COMPATIBLE': 3, 'ID-KER': 2}; structures {'[[1, 3], [1, 3]]': 3, '[[1, 3], [1, 4]]': 2}
- core_v1 · wave · σ=0.01: rate 0.6; labels {'FIT-COMPATIBLE': 5}; structures {'[[1, 1], [1, 1]]': 3, '[[2, 2]]': 2}
- core_v1 · wave · σ=0.05: rate 0.4; labels {'FIT-COMPATIBLE': 5}; structures {'[[2, 2]]': 3, '[[1, 1], [1, 1]]': 2}
- core_v2 · beam · σ=0.05: rate 0.8; labels {'FIT-COMPATIBLE': 2, 'UNDECIDED': 3}; structures {'[[1, 2], [1, 2]]': 5}
- core_v2 · transport_plus_diffusion · σ=0.05: rate 0.2; labels {'FIT-COMPATIBLE': 5}; structures {'[[1, 1], [1, 2]]': 4, '[[1, 1], [2, 0]]': 1}
- ensemble_sindy · beam · σ=0.01: rate 0.8; labels {'n/a': 5}; structures {'[[1, 2], [1, 2]]': 4, '[[2, 4]]': 1}
- ensemble_sindy · beam · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 3]]': 4, '[[1, 4]]': 1}
- ensemble_sindy · klein_gordon · σ=0.05: rate 0.4; labels {'n/a': 5}; structures {'[[2, 2]]': 4, '[[2, 3]]': 1}
- ensemble_sindy · schrodinger · σ=0.01: rate 0.8; labels {'n/a': 5}; structures {'[[1, 2]]': 4, '[[1, 3]]': 1}
- ensemble_sindy · schrodinger · σ=0.05: rate 0.4; labels {'n/a': 5}; structures {'[[1, 3]]': 4, '[[1, 2]]': 1}
- ensemble_sindy · transport_plus_diffusion · σ=0.01: rate 0.2; labels {'n/a': 5}; structures {'[[2, 4]]': 3, '[[1, 1], [1, 2]]': 1}
- ensemble_sindy · transport_plus_diffusion · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 4]]': 4, '[[1, 3]]': 1}
- ensemble_sindy · wave · σ=0.01: rate 0.4; labels {'n/a': 5}; structures {'[[2, 2]]': 3, '[[1, 1], [1, 1]]': 2}
- ensemble_sindy · wave · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[2, 2]]': 5}
- pdefind · advection_diffusion · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · advection_diffusion · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- pdefind · airy · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- pdefind · airy · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- pdefind · airy · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- pdefind · beam · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · beam · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · beam · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- pdefind · heat · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · heat · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 0]]': 5}
- pdefind · klein_gordon · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[2, 2]]': 5}
- pdefind · klein_gordon · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · klein_gordon · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 0]]': 5}
- pdefind · schrodinger · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · schrodinger · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- pdefind · schrodinger · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- pdefind · telegraph · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[2, 2]]': 5}
- pdefind · telegraph · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · telegraph · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 0]]': 5}
- pdefind · transport · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- pdefind · transport_plus_diffusion · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · transport_plus_diffusion · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · transport_plus_diffusion · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- pdefind · wave · σ=0.001: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · wave · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[1, 2]]': 5}
- pdefind · wave · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 1]]': 5}
- sbr_sindy · beam · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[2, 4]]': 5}
- sbr_sindy · beam · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 3]]': 5}
- sbr_sindy · klein_gordon · σ=0.05: rate 0.4; labels {'n/a': 5}; structures {'[[2, 2]]': 4, '[[2, 3]]': 1}
- sbr_sindy · telegraph · σ=0.05: rate 0.4; labels {'n/a': 5}; structures {'[[2, 2]]': 5}
- sbr_sindy · transport_plus_diffusion · σ=0.001: rate 0.2; labels {'n/a': 5}; structures {'[[2, 3]]': 4, '[[1, 1], [1, 2]]': 1}
- sbr_sindy · transport_plus_diffusion · σ=0.01: rate 0.0; labels {'n/a': 5}; structures {'[[2, 4]]': 3, '[[2, 3]]': 2}
- sbr_sindy · transport_plus_diffusion · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 4]]': 4, '[[1, 3]]': 1}
- sbr_sindy · wave · σ=0.01: rate 0.2; labels {'n/a': 5}; structures {'[[2, 2]]': 4, '[[1, 1], [1, 1]]': 1}
- sbr_sindy · wave · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[2, 2]]': 4, '[[2, 4]]': 1}
- weak_sindy · beam · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 3]]': 5}
- weak_sindy · klein_gordon · σ=0.05: rate 0.6; labels {'n/a': 5}; structures {'[[2, 2]]': 5}
- weak_sindy · schrodinger · σ=0.01: rate 0.8; labels {'n/a': 5}; structures {'[[1, 2]]': 4, '[[1, 3]]': 1}
- weak_sindy · schrodinger · σ=0.05: rate 0.4; labels {'n/a': 5}; structures {'[[1, 3]]': 4, '[[1, 2]]': 1}
- weak_sindy · transport_plus_diffusion · σ=0.01: rate 0.6; labels {'n/a': 5}; structures {'[[1, 1], [1, 2]]': 2, '[[2, 4]]': 2}
- weak_sindy · transport_plus_diffusion · σ=0.05: rate 0.0; labels {'n/a': 5}; structures {'[[1, 4]]': 4, '[[1, 3]]': 1}
- weak_sindy · wave · σ=0.01: rate 0.6; labels {'n/a': 5}; structures {'[[1, 1], [1, 1]]': 3, '[[2, 2]]': 2}
- weak_sindy · wave · σ=0.05: rate 0.2; labels {'n/a': 5}; structures {'[[2, 2]]': 4, '[[1, 1], [1, 1]]': 1}