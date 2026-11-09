# V1 gate (noresid_allsources; clean 101 rows, dropped 0 without resid, 116 of a design the injected rows lack; I 92 rows, 48 timeout/crash)

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
| B1_minp | 0.640 [0.553, 0.765] | +0.000 [+0.000, +0.000] | 0.60 | 0.70 | 0.64 | 0.57 | 0.68 |
| B2_iforest | 0.603 [0.520, 0.741] | -0.037 [-0.155, +0.096] | 0.68 | 0.54 | 0.41 | 0.62 | 0.77 |
| B3_mahal | 0.628 [0.512, 0.768] | -0.012 [-0.161, +0.097] | 0.70 | 0.59 | 0.41 | 0.62 | 0.82 |
| B4_knn | 0.622 [0.514, 0.772] | -0.019 [-0.157, +0.100] | 0.71 | 0.56 | 0.39 | 0.64 | 0.82 |
| V1_hgb | 0.717 [0.590, 0.816] | +0.077 [-0.082, +0.166] | 0.82 | 0.64 | 0.84 | 0.65 | 0.63 |

FIT-COMPATIBLE runs only (clean 75, injected 50):

| arm | AUROC [95 % CI] | − B0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0_v0 | 0.551 [0.438, 0.762] | +0.000 [+0.000, +0.000] | 0.60 | 0.68 | 0.67 | 0.33 | 0.47 |
| B1_minp | 0.551 [0.438, 0.762] | +0.000 [+0.000, +0.000] | 0.60 | 0.68 | 0.67 | 0.33 | 0.47 |
| B2_iforest | 0.509 [0.358, 0.721] | -0.042 [-0.206, +0.101] | 0.55 | 0.50 | 0.43 | 0.33 | 0.72 |
| B3_mahal | 0.524 [0.373, 0.727] | -0.027 [-0.188, +0.090] | 0.60 | 0.58 | 0.38 | 0.33 | 0.72 |
| B4_knn | 0.503 [0.363, 0.732] | -0.048 [-0.204, +0.089] | 0.62 | 0.54 | 0.33 | 0.33 | 0.69 |
| V1_hgb | 0.844 [0.641, 0.896] | +0.293 [-0.052, +0.398] | 0.78 | 0.57 | 0.90 | 1.00 | 0.97 |

| type | B0_v0 | B1_minp | B2_iforest | B3_mahal | B4_knn | V1_hgb |
|---|---|---|---|---|---|---|
| aliasing | 0.67 | 0.67 | 0.87 | 0.91 | 0.91 | 0.55 |
| coloured | 0.27 | 0.27 | 0.72 | 0.84 | 0.86 | 0.82 |
| fractional | 0.64 | 0.64 | 0.44 | 0.52 | 0.48 | 0.75 |
| heteroscedastic | 0.59 | 0.59 | 0.32 | 0.35 | 0.35 | 0.66 |
| nonlinear | 0.81 | 0.81 | 0.75 | 0.73 | 0.73 | 0.75 |
| two_laws | 0.66 | 0.66 | 0.60 | 0.61 | 0.62 | 0.70 |
| varcoef | 0.64 | 0.64 | 0.62 | 0.61 | 0.60 | 0.81 |
| level 0 | 0.59 | 0.59 | 0.55 | 0.62 | 0.62 | 0.73 |
| level 1 | 0.66 | 0.66 | 0.63 | 0.63 | 0.63 | 0.71 |
| level 2 | 0.74 | 0.74 | 0.59 | 0.64 | 0.61 | 0.78 |
| injected level 1, draw 400 | 0.74 | 0.74 | 0.63 | 0.70 | 0.67 | 0.86 |
| injected level 1, fresh draws 402/403 | 0.64 | 0.64 | 0.64 | 0.59 | 0.61 | 0.61 |

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
