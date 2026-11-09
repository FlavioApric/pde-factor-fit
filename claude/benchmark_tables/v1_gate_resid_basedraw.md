# V1 gate (resid_basedraw; clean 14 rows, dropped 0 without resid, 0 of a design the injected rows lack; I 92 rows, 48 timeout/crash)

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
| B0_v0 | 0.779 [0.683, 0.879] | +0.000 [+0.000, +0.000] | 0.70 | 0.81 | 0.59 | 1.00 | 0.80 |
| B1_minp | 0.794 [0.721, 0.930] | +0.015 [-0.076, +0.162] | 0.93 | 0.90 | 0.75 | 0.60 | 0.80 |
| B2_iforest | 0.702 [0.649, 0.863] | -0.077 [-0.169, +0.116] | 0.70 | 0.64 | 0.75 | 0.60 | 0.82 |
| B3_mahal | 0.748 [0.632, 0.896] | -0.032 [-0.179, +0.147] | 0.96 | 0.62 | 0.78 | 0.60 | 0.77 |
| B4_knn | 0.748 [0.631, 0.894] | -0.031 [-0.180, +0.143] | 0.96 | 0.62 | 0.76 | 0.60 | 0.80 |
| V1_hgb | 0.886 [0.764, 0.978] | +0.106 [-0.062, +0.248] | 0.95 | 0.95 | 0.75 | 0.80 | 0.98 |

FIT-COMPATIBLE runs only (clean 11, injected 50):

| arm | AUROC [95 % CI] | − B0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0_v0 | 0.689 [0.542, 0.859] | +0.000 [+0.000, +0.000] | 0.71 | 0.75 | 0.61 | nan | nan |
| B1_minp | 0.875 [0.843, 1.000] | +0.186 [+0.071, +0.366] | 0.96 | 0.89 | 0.78 | nan | nan |
| B2_iforest | 0.617 [0.423, 0.870] | -0.072 [-0.358, +0.189] | 0.60 | 0.61 | 0.64 | nan | nan |
| B3_mahal | 0.772 [0.583, 0.963] | +0.083 [-0.199, +0.322] | 0.94 | 0.62 | 0.75 | nan | nan |
| B4_knn | 0.763 [0.573, 0.963] | +0.074 [-0.213, +0.313] | 0.94 | 0.62 | 0.72 | nan | nan |
| V1_hgb | 0.872 [0.689, 1.000] | +0.183 [-0.110, +0.367] | 0.96 | 0.94 | 0.72 | nan | nan |

| type | B0_v0 | B1_minp | B2_iforest | B3_mahal | B4_knn | V1_hgb |
|---|---|---|---|---|---|---|
| aliasing | 0.87 | 0.87 | 0.80 | 0.88 | 0.88 | 0.97 |
| coloured | 0.27 | 0.75 | 0.67 | 0.69 | 0.69 | 0.85 |
| fractional | 0.73 | 0.88 | 0.58 | 0.68 | 0.69 | 0.82 |
| heteroscedastic | 0.64 | 0.94 | 0.57 | 0.84 | 0.84 | 0.94 |
| nonlinear | 0.85 | 0.85 | 0.97 | 0.83 | 0.83 | 0.96 |
| two_laws | 0.78 | 0.80 | 0.65 | 0.70 | 0.70 | 0.93 |
| varcoef | 0.88 | 0.56 | 0.74 | 0.66 | 0.66 | 0.76 |
| level 0 | 0.67 | 0.83 | 0.55 | 0.60 | 0.60 | 0.90 |
| level 1 | 0.83 | 0.80 | 0.76 | 0.78 | 0.78 | 0.89 |
| level 2 | 0.81 | 0.86 | 0.70 | 0.84 | 0.84 | 0.93 |
| injected level 1, draw 400 | 0.82 | 0.87 | 0.76 | 0.80 | 0.79 | 0.95 |
| injected level 1, fresh draws 402/403 | 0.85 | 0.80 | 0.80 | 0.80 | 0.80 | 0.86 |

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

clean G/S rows: 1 crash, 5 timeout (not right; excluded from FA)

## Target (b): run failure on clean data (missed / false flag; risk control alpha = 0.10)


## Gate

- passed: False
- ships_wrong_set_flag: False
- reason: no fit/cal split rows
