# V1 gate (resid_allsources; clean 101 rows, dropped 15 without resid, 101 of a design the injected rows lack; I 92 rows, 48 timeout/crash)

## Split (fit / cal / test); alpha = 0.05

| arm | false alarm G/S test [95 % hi] | false alarm N | detection I test | aliasing | coloured | fractional | heteroscedastic | nonlinear | two_laws | varcoef | level 0 / 1 / 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B0_v0 | 0.000 [0.100] (n=35) | 0.000 | 0.000 (n=12) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan / 0.00 / nan |
| B1_minp | 0.000 [0.100] (n=35) | 0.000 | 0.000 (n=12) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan / 0.00 / nan |
| B2_iforest | 0.000 [0.100] (n=35) | 0.000 | 0.000 (n=12) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan / 0.00 / nan |
| B3_mahal | 0.000 [0.100] (n=35) | 0.000 | 0.000 (n=12) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan / 0.00 / nan |
| B4_knn | 0.000 [0.100] (n=35) | 0.000 | 0.000 (n=12) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan / 0.00 / nan |
| V1_hgb | 0.000 [0.100] (n=35) | 0.000 | 0.000 (n=12) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan / 0.00 / nan |

V1 − B0 detection (paired bootstrap): +0.000 [+0.000, +0.000]; type accuracy on flagged test runs nan

## LOFO (held-out family: all its rows)

| family | B0_v0 FA / det | B1_minp FA / det | B2_iforest FA / det | B3_mahal FA / det | B4_knn FA / det | V1_hgb FA / det |
|---|---|---|---|---|---|---|
| F1 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 |
| F2 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 |
| F3 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 |
| F4 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 |
| F5 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 |

LOFO pooled V1 − B0 detection: +0.000 [+0.000, +0.000]

## LOTO (held-out injection type)

| type | B0_v0 det | B1_minp det | B2_iforest det | B3_mahal det | B4_knn det | V1_hgb det | V1 wrong-type rate |
|---|---|---|---|---|---|---|---|
| aliasing | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| coloured | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| fractional | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| heteroscedastic | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| nonlinear | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| two_laws | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| varcoef | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## LOFO AUROC, injected vs clean (alpha-free; 5 held-out families; mean of per-family AUROC; CI: paired cluster bootstrap over base draws)

all scored runs:

| arm | AUROC [95 % CI] | − B0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0_v0 | 0.640 [0.553, 0.765] | +0.000 [+0.000, +0.000] | 0.60 | 0.70 | 0.64 | 0.57 | 0.68 |
| B1_minp | 0.710 [0.608, 0.829] | +0.070 [-0.063, +0.136] | 0.76 | 0.77 | 0.70 | 0.61 | 0.71 |
| B2_iforest | 0.647 [0.560, 0.776] | +0.007 [-0.100, +0.112] | 0.74 | 0.58 | 0.46 | 0.65 | 0.80 |
| B3_mahal | 0.715 [0.607, 0.837] | +0.074 [-0.070, +0.166] | 0.80 | 0.74 | 0.59 | 0.60 | 0.85 |
| B4_knn | 0.709 [0.606, 0.827] | +0.069 [-0.072, +0.162] | 0.80 | 0.72 | 0.56 | 0.62 | 0.85 |
| V1_hgb | 0.826 [0.699, 0.923] | +0.185 [+0.036, +0.266] | 0.90 | 0.80 | 0.93 | 0.60 | 0.90 |

FIT-COMPATIBLE runs only (clean 75, injected 50):

| arm | AUROC [95 % CI] | − B0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0_v0 | 0.551 [0.438, 0.762] | +0.000 [+0.000, +0.000] | 0.60 | 0.68 | 0.67 | 0.33 | 0.47 |
| B1_minp | 0.663 [0.542, 0.888] | +0.112 [-0.045, +0.336] | 0.76 | 0.79 | 0.80 | 0.67 | 0.31 |
| B2_iforest | 0.546 [0.409, 0.759] | -0.005 [-0.134, +0.125] | 0.64 | 0.58 | 0.48 | 0.33 | 0.69 |
| B3_mahal | 0.627 [0.504, 0.846] | +0.077 [-0.031, +0.219] | 0.76 | 0.76 | 0.58 | 0.33 | 0.69 |
| B4_knn | 0.618 [0.500, 0.844] | +0.068 [-0.030, +0.214] | 0.76 | 0.74 | 0.57 | 0.33 | 0.69 |
| V1_hgb | 0.928 [0.722, 0.964] | +0.377 [+0.048, +0.494] | 0.89 | 0.78 | 0.97 | 1.00 | 1.00 |

| type | B0_v0 | B1_minp | B2_iforest | B3_mahal | B4_knn | V1_hgb |
|---|---|---|---|---|---|---|
| aliasing | 0.67 | 0.75 | 0.89 | 0.90 | 0.89 | 0.71 |
| coloured | 0.27 | 0.75 | 0.87 | 0.86 | 0.87 | 0.91 |
| fractional | 0.64 | 0.66 | 0.45 | 0.52 | 0.47 | 0.84 |
| heteroscedastic | 0.59 | 0.92 | 0.52 | 0.93 | 0.91 | 0.94 |
| nonlinear | 0.81 | 0.74 | 0.74 | 0.74 | 0.74 | 0.89 |
| two_laws | 0.66 | 0.70 | 0.61 | 0.61 | 0.63 | 0.79 |
| varcoef | 0.64 | 0.50 | 0.61 | 0.61 | 0.60 | 0.87 |
| level 0 | 0.59 | 0.75 | 0.57 | 0.68 | 0.68 | 0.87 |
| level 1 | 0.66 | 0.71 | 0.67 | 0.73 | 0.73 | 0.80 |
| level 2 | 0.74 | 0.75 | 0.69 | 0.79 | 0.75 | 0.95 |
| injected level 1, draw 400 | 0.74 | 0.78 | 0.70 | 0.80 | 0.79 | 0.93 |
| injected level 1, fresh draws 402/403 | 0.64 | 0.69 | 0.67 | 0.70 | 0.70 | 0.72 |

## CRASH / TIMEOUT injected runs (LOFO pooled; no output, so no arm scores them)

| type | scored | crash | timeout | B0_v0 det / incl. bad | B1_minp det / incl. bad | B2_iforest det / incl. bad | B3_mahal det / incl. bad | B4_knn det / incl. bad | V1_hgb det / incl. bad |
|---|---|---|---|---|---|---|---|---|---|
| aliasing | 12 | 8 | 0 | 0.00 / 0.40 | 0.00 / 0.40 | 0.00 / 0.40 | 0.00 / 0.40 | 0.00 / 0.40 | 0.00 / 0.40 |
| coloured | 6 | 13 | 1 | 0.00 / 0.70 | 0.00 / 0.70 | 0.00 / 0.70 | 0.00 / 0.70 | 0.00 / 0.70 | 0.00 / 0.70 |
| fractional | 16 | 0 | 4 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 |
| heteroscedastic | 16 | 1 | 3 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 |
| nonlinear | 12 | 3 | 5 | 0.00 / 0.40 | 0.00 / 0.40 | 0.00 / 0.40 | 0.00 / 0.40 | 0.00 / 0.40 | 0.00 / 0.40 |
| two_laws | 16 | 1 | 3 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 |
| varcoef | 14 | 1 | 5 | 0.00 / 0.30 | 0.00 / 0.30 | 0.00 / 0.30 | 0.00 / 0.30 | 0.00 / 0.30 | 0.00 / 0.30 |

clean G/S rows: 20 crash, 79 timeout (not right; excluded from FA)

## Target (b): run failure on clean data (missed / false flag; risk control alpha = 0.10)

- split: missed 0.00, false flag 1.00 (pos 9, neg 26)
- LOFO F1: missed 0.00, false flag 1.00 (pos 1, neg 25)
- LOFO F2: missed 0.00, false flag 1.00 (pos 9, neg 17)
- LOFO F3: missed 0.00, false flag 1.00 (pos 4, neg 17)
- LOFO F4: missed 0.00, false flag 1.00 (pos 5, neg 6)
- LOFO F5: missed 0.00, false flag 1.00 (pos 3, neg 14)

## Gate

- primary_split: False
- primary_lofo: False
- fa_split: True
- fa_lofo: True
- loto: True
- useful_mid_level: False
- target_b: False
- passed: False
- ships_wrong_set_flag: False
