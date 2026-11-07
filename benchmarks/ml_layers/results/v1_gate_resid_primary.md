# V1 gate (resid_primary; clean 49 rows, dropped 0 without resid, 30 of a design the injected rows lack; I 92 rows, 48 timeout/crash)

## Split (fit / cal / test); alpha = 0.05

| arm | false alarm G/S test [95 % hi] | false alarm N | detection I test | aliasing | coloured | fractional | heteroscedastic | nonlinear | two_laws | varcoef | level 0 / 1 / 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|

## LOFO (held-out family: all its rows)

| family | B0_v0 FA / det | B1_minp FA / det | B2_iforest FA / det | B3_mahal FA / det | B4_knn FA / det | V1_hgb FA / det |
|---|---|---|---|---|---|---|

## LOTO (held-out injection type)

| type | B0_v0 det | B1_minp det | B2_iforest det | B3_mahal det | B4_knn det | V1_hgb det | V1 wrong-type rate |
|---|---|---|---|---|---|---|---|

## LOFO AUROC, injected vs clean (alpha-free; 5 held-out families; mean of per-family AUROC; CI: paired cluster bootstrap over base draws)

all scored runs:

| arm | AUROC [95 % CI] | − B0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0_v0 | 0.681 [0.598, 0.829] | +0.000 [+0.000, +0.000] | 0.69 | 0.80 | 0.65 | 0.50 | 0.77 |
| B1_minp | 0.806 [0.718, 0.901] | +0.125 [-0.045, +0.211] | 0.85 | 0.91 | 0.82 | 0.64 | 0.81 |
| B2_iforest | 0.734 [0.640, 0.852] | +0.053 [-0.091, +0.175] | 0.81 | 0.71 | 0.61 | 0.66 | 0.88 |
| B3_mahal | 0.671 [0.557, 0.827] | -0.010 [-0.181, +0.109] | 0.81 | 0.83 | 0.61 | 0.51 | 0.59 |
| B4_knn | 0.674 [0.562, 0.826] | -0.007 [-0.172, +0.107] | 0.81 | 0.82 | 0.63 | 0.51 | 0.59 |
| V1_hgb | 0.900 [0.825, 0.975] | +0.219 [+0.078, +0.289] | 0.96 | 0.94 | 0.93 | 0.69 | 0.99 |

FIT-COMPATIBLE runs only (clean 40, injected 50):

| arm | AUROC [95 % CI] | − B0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0_v0 | 0.515 [0.440, 0.789] | +0.000 [+0.000, +0.000] | 0.69 | 0.73 | 0.65 | 0.00 | 0.50 |
| B1_minp | 0.701 [0.564, 0.940] | +0.186 [-0.051, +0.406] | 0.85 | 0.93 | 0.88 | 0.50 | 0.35 |
| B2_iforest | 0.537 [0.452, 0.811] | +0.022 [-0.117, +0.158] | 0.72 | 0.70 | 0.56 | 0.00 | 0.70 |
| B3_mahal | 0.524 [0.447, 0.834] | +0.010 [-0.143, +0.207] | 0.76 | 0.84 | 0.57 | 0.00 | 0.45 |
| B4_knn | 0.527 [0.449, 0.836] | +0.013 [-0.135, +0.207] | 0.77 | 0.83 | 0.58 | 0.00 | 0.45 |
| V1_hgb | 0.759 [0.644, 0.978] | +0.244 [+0.083, +0.359] | 0.94 | 0.96 | 0.89 | 0.00 | 1.00 |

| type | B0_v0 | B1_minp | B2_iforest | B3_mahal | B4_knn | V1_hgb |
|---|---|---|---|---|---|---|
| aliasing | 0.68 | 0.83 | 0.96 | 0.78 | 0.78 | 0.87 |
| coloured | 0.30 | 0.75 | 0.84 | 0.83 | 0.83 | 0.98 |
| fractional | 0.71 | 0.87 | 0.58 | 0.51 | 0.50 | 0.95 |
| heteroscedastic | 0.66 | 0.94 | 0.61 | 0.83 | 0.82 | 0.95 |
| nonlinear | 0.86 | 0.81 | 0.90 | 0.77 | 0.79 | 0.95 |
| two_laws | 0.71 | 0.85 | 0.72 | 0.58 | 0.59 | 0.91 |
| varcoef | 0.74 | 0.61 | 0.69 | 0.60 | 0.62 | 0.87 |
| level 0 | 0.62 | 0.82 | 0.64 | 0.63 | 0.65 | 0.93 |
| level 1 | 0.72 | 0.82 | 0.78 | 0.71 | 0.70 | 0.89 |
| level 2 | 0.81 | 0.82 | 0.76 | 0.71 | 0.70 | 0.98 |
| injected level 1, draw 400 | 0.80 | 0.90 | 0.79 | 0.78 | 0.77 | 0.96 |
| injected level 1, fresh draws 402/403 | 0.70 | 0.80 | 0.77 | 0.69 | 0.69 | 0.85 |

## CRASH / TIMEOUT injected runs (LOFO pooled; no output, so no arm scores them)

| type | scored | crash | timeout | B0_v0 det / incl. bad | B1_minp det / incl. bad | B2_iforest det / incl. bad | B3_mahal det / incl. bad | B4_knn det / incl. bad | V1_hgb det / incl. bad |
|---|---|---|---|---|---|---|---|---|---|
| aliasing | 0 | 0 | 0 | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan |
| coloured | 0 | 0 | 0 | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan |
| fractional | 0 | 0 | 0 | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan |
| heteroscedastic | 0 | 0 | 0 | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan |
| nonlinear | 0 | 0 | 0 | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan |
| two_laws | 0 | 0 | 0 | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan |
| varcoef | 0 | 0 | 0 | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan | nan / nan |

clean G/S rows: 5 crash, 16 timeout (not right; excluded from FA)

## Target (b): run failure on clean data (missed / false flag; risk control alpha = 0.10)


## Gate

- passed: False
- ships_wrong_set_flag: False
- reason: no fit/cal split rows
