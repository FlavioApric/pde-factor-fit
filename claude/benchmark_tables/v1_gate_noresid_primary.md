# V1 gate (noresid_primary; clean 49 rows, dropped 0 without resid, 30 of a design the injected rows lack; I 92 rows, 48 timeout/crash)

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
| B1_minp | 0.681 [0.598, 0.829] | +0.000 [+0.000, +0.000] | 0.69 | 0.80 | 0.65 | 0.50 | 0.77 |
| B2_iforest | 0.636 [0.535, 0.759] | -0.045 [-0.226, +0.104] | 0.70 | 0.60 | 0.55 | 0.49 | 0.84 |
| B3_mahal | 0.609 [0.502, 0.759] | -0.072 [-0.230, +0.045] | 0.68 | 0.71 | 0.56 | 0.51 | 0.59 |
| B4_knn | 0.599 [0.489, 0.762] | -0.082 [-0.248, +0.045] | 0.72 | 0.69 | 0.49 | 0.51 | 0.58 |
| V1_hgb | 0.831 [0.717, 0.920] | +0.150 [+0.004, +0.218] | 0.90 | 0.77 | 0.89 | 0.63 | 0.96 |

FIT-COMPATIBLE runs only (clean 40, injected 50):

| arm | AUROC [95 % CI] | − B0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0_v0 | 0.515 [0.440, 0.789] | +0.000 [+0.000, +0.000] | 0.69 | 0.73 | 0.65 | 0.00 | 0.50 |
| B1_minp | 0.515 [0.440, 0.789] | +0.000 [+0.000, +0.000] | 0.69 | 0.73 | 0.65 | 0.00 | 0.50 |
| B2_iforest | 0.431 [0.351, 0.692] | -0.084 [-0.247, +0.051] | 0.56 | 0.55 | 0.49 | 0.00 | 0.55 |
| B3_mahal | 0.433 [0.339, 0.687] | -0.082 [-0.271, +0.050] | 0.56 | 0.67 | 0.48 | 0.00 | 0.45 |
| B4_knn | 0.425 [0.345, 0.696] | -0.090 [-0.263, +0.061] | 0.62 | 0.66 | 0.39 | 0.00 | 0.45 |
| V1_hgb | 0.905 [0.787, 0.939] | +0.390 [+0.035, +0.476] | 0.88 | 0.73 | 0.91 | 1.00 | 1.00 |

| type | B0_v0 | B1_minp | B2_iforest | B3_mahal | B4_knn | V1_hgb |
|---|---|---|---|---|---|---|
| aliasing | 0.68 | 0.68 | 0.94 | 0.78 | 0.78 | 0.70 |
| coloured | 0.30 | 0.30 | 0.74 | 0.83 | 0.83 | 0.85 |
| fractional | 0.71 | 0.71 | 0.52 | 0.54 | 0.50 | 0.86 |
| heteroscedastic | 0.66 | 0.66 | 0.38 | 0.31 | 0.33 | 0.87 |
| nonlinear | 0.86 | 0.86 | 0.86 | 0.79 | 0.79 | 0.89 |
| two_laws | 0.71 | 0.71 | 0.60 | 0.60 | 0.59 | 0.82 |
| varcoef | 0.74 | 0.74 | 0.68 | 0.62 | 0.61 | 0.88 |
| level 0 | 0.62 | 0.62 | 0.50 | 0.60 | 0.60 | 0.86 |
| level 1 | 0.72 | 0.72 | 0.70 | 0.63 | 0.62 | 0.83 |
| level 2 | 0.81 | 0.81 | 0.63 | 0.61 | 0.58 | 0.90 |
| injected level 1, draw 400 | 0.80 | 0.80 | 0.67 | 0.72 | 0.69 | 0.96 |
| injected level 1, fresh draws 402/403 | 0.70 | 0.70 | 0.70 | 0.59 | 0.60 | 0.74 |

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
