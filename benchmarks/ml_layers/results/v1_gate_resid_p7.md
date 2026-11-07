# V1 gate (resid_p7; clean 95 rows, dropped 0 without resid, 0 of a design the injected rows lack; I 100 rows, 40 timeout/crash)

## Split (fit / cal / test); alpha = 0.05

| arm | false alarm G/S test [95 % hi] | false alarm N | detection I test | aliasing | coloured | fractional | heteroscedastic | nonlinear | two_laws | varcoef | level 0 / 1 / 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B0_v0 | 0.294 [0.560] (n=17) | nan | 0.400 (n=15) | 0.50 | 0.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | nan / 0.40 / nan |
| B1_minp | 0.000 [0.195] (n=17) | nan | 0.333 (n=15) | 0.50 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | nan / 0.33 / nan |
| B2_iforest | 0.176 [0.434] (n=17) | nan | 0.067 (n=15) | 0.00 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan / 0.07 / nan |
| B3_mahal | 0.059 [0.287] (n=17) | nan | 0.400 (n=15) | 0.50 | 1.00 | 0.33 | 1.00 | 0.00 | 0.00 | 0.00 | nan / 0.40 / nan |
| B4_knn | 0.059 [0.287] (n=17) | nan | 0.400 (n=15) | 0.50 | 1.00 | 0.33 | 1.00 | 0.00 | 0.00 | 0.00 | nan / 0.40 / nan |
| V1_hgb | 0.000 [0.195] (n=17) | nan | 0.067 (n=15) | 0.00 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan / 0.07 / nan |

V1 − B0 detection (paired bootstrap): -0.333 [-0.600, -0.067]; type accuracy on flagged test runs 1.00

## LOFO (held-out family: all its rows)

| family | B0_v0 FA / det | B1_minp FA / det | B2_iforest FA / det | B3_mahal FA / det | B4_knn FA / det | V1_hgb FA / det |
|---|---|---|---|---|---|---|
| F1 | 0.17 / 0.26 | 0.04 / 0.37 | 0.00 / 0.04 | 0.00 / 0.30 | 0.00 / 0.30 | 0.04 / 0.04 |
| F2 | 0.18 / 0.44 | 0.00 / 0.32 | 0.00 / 0.00 | 0.00 / 0.32 | 0.00 / 0.32 | 0.00 / 0.08 |
| F3 | 0.19 / 0.47 | 0.00 / 0.40 | 0.00 / 0.00 | 0.10 / 0.47 | 0.10 / 0.47 | 0.05 / 0.07 |
| F4 | 0.27 / 0.33 | 0.00 / 0.17 | 0.27 / 0.00 | 0.09 / 0.17 | 0.09 / 0.17 | 0.09 / 0.00 |
| F5 | 0.18 / 0.37 | 0.00 / 0.41 | 0.06 / 0.00 | 0.06 / 0.41 | 0.06 / 0.41 | 0.00 / 0.00 |

LOFO pooled V1 − B0 detection: -0.330 [-0.440, -0.230]

## LOTO (held-out injection type)

| type | B0_v0 det | B1_minp det | B2_iforest det | B3_mahal det | B4_knn det | V1_hgb det | V1 wrong-type rate |
|---|---|---|---|---|---|---|---|
| aliasing | 0.64 | 0.50 | 0.07 | 0.50 | 0.50 | 0.07 | 1.00 |
| coloured | 0.00 | 0.88 | 0.12 | 1.00 | 1.00 | 0.00 | 0.00 |
| fractional | 0.31 | 0.00 | 0.00 | 0.12 | 0.06 | 0.00 | 0.00 |
| heteroscedastic | 0.47 | 1.00 | 0.00 | 1.00 | 1.00 | 0.00 | 0.00 |
| nonlinear | 0.53 | 0.07 | 0.00 | 0.07 | 0.07 | 0.13 | 1.00 |
| two_laws | 0.19 | 0.06 | 0.00 | 0.06 | 0.00 | 0.00 | 0.00 |
| varcoef | 0.29 | 0.07 | 0.00 | 0.07 | 0.07 | 0.00 | 0.00 |

## LOFO AUROC, injected vs clean (alpha-free; 5 held-out families; mean of per-family AUROC; CI: paired cluster bootstrap over base draws)

all scored runs:

| arm | AUROC [95 % CI] | − B0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0_v0 | 0.625 [0.512, 0.724] | +0.000 [+0.000, +0.000] | 0.59 | 0.68 | 0.61 | 0.64 | 0.61 |
| B1_minp | 0.738 [0.634, 0.816] | +0.114 [-0.042, +0.264] | 0.71 | 0.78 | 0.82 | 0.67 | 0.72 |
| B2_iforest | 0.624 [0.544, 0.785] | -0.000 [-0.116, +0.216] | 0.75 | 0.61 | 0.60 | 0.35 | 0.81 |
| B3_mahal | 0.726 [0.628, 0.857] | +0.101 [-0.037, +0.302] | 0.82 | 0.73 | 0.74 | 0.48 | 0.86 |
| B4_knn | 0.705 [0.604, 0.845] | +0.080 [-0.069, +0.290] | 0.80 | 0.71 | 0.70 | 0.44 | 0.87 |
| V1_hgb | 0.847 [0.720, 0.914] | +0.222 [+0.018, +0.356] | 0.85 | 0.88 | 0.96 | 0.73 | 0.81 |

FIT-COMPATIBLE runs only (clean 70, injected 50):

| arm | AUROC [95 % CI] | − B0 [95 % CI] | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|---|
| B0_v0 | 0.627 [0.483, 0.783] | +0.000 [+0.000, +0.000] | 0.60 | 0.64 | 0.61 | 0.75 | 0.54 |
| B1_minp | 0.781 [0.659, 0.900] | +0.154 [-0.049, +0.344] | 0.72 | 0.79 | 0.81 | 0.88 | 0.71 |
| B2_iforest | 0.686 [0.556, 0.871] | +0.059 [-0.117, +0.294] | 0.67 | 0.56 | 0.58 | 0.75 | 0.88 |
| B3_mahal | 0.818 [0.722, 0.948] | +0.191 [+0.018, +0.406] | 0.78 | 0.70 | 0.73 | 0.88 | 1.00 |
| B4_knn | 0.802 [0.696, 0.947] | +0.175 [-0.002, +0.402] | 0.75 | 0.68 | 0.70 | 0.88 | 1.00 |
| V1_hgb | 0.922 [0.786, 0.960] | +0.295 [+0.057, +0.412] | 0.86 | 0.87 | 0.96 | 1.00 | 0.92 |

| type | B0_v0 | B1_minp | B2_iforest | B3_mahal | B4_knn | V1_hgb |
|---|---|---|---|---|---|---|
| aliasing | 0.80 | 0.87 | 0.74 | 0.81 | 0.78 | 0.82 |
| coloured | 0.30 | 0.92 | 0.85 | 1.00 | 1.00 | 0.97 |
| fractional | 0.62 | 0.67 | 0.51 | 0.61 | 0.57 | 0.80 |
| heteroscedastic | 0.71 | 1.00 | 0.68 | 1.00 | 1.00 | 0.92 |
| nonlinear | 0.69 | 0.53 | 0.66 | 0.63 | 0.63 | 0.78 |
| two_laws | 0.48 | 0.72 | 0.53 | 0.53 | 0.53 | 0.82 |
| varcoef | 0.64 | 0.49 | 0.62 | 0.71 | 0.66 | 0.90 |
| level 0 | 0.49 | 0.63 | 0.52 | 0.59 | 0.58 | 0.77 |
| level 1 | 0.66 | 0.77 | 0.66 | 0.76 | 0.73 | 0.85 |
| level 2 | 0.78 | 0.78 | 0.74 | 0.84 | 0.84 | 0.92 |
| injected level 1, draw 400 | 0.71 | 0.77 | 0.52 | 0.64 | 0.59 | 0.83 |
| injected level 1, fresh draws 402/403 | 0.60 | 0.76 | 0.75 | 0.84 | 0.82 | 0.83 |

## CRASH / TIMEOUT injected runs (LOFO pooled; no output, so no arm scores them)

| type | scored | crash | timeout | B0_v0 det / incl. bad | B1_minp det / incl. bad | B2_iforest det / incl. bad | B3_mahal det / incl. bad | B4_knn det / incl. bad | V1_hgb det / incl. bad |
|---|---|---|---|---|---|---|---|---|---|
| aliasing | 14 | 3 | 3 | 0.64 / 0.75 | 0.50 / 0.65 | 0.00 / 0.30 | 0.50 / 0.65 | 0.50 / 0.65 | 0.00 / 0.30 |
| coloured | 8 | 0 | 12 | 0.00 / 0.60 | 0.88 / 0.95 | 0.12 / 0.65 | 1.00 / 1.00 | 1.00 / 1.00 | 0.12 / 0.65 |
| fractional | 16 | 0 | 4 | 0.31 / 0.45 | 0.06 / 0.25 | 0.00 / 0.20 | 0.06 / 0.25 | 0.06 / 0.25 | 0.00 / 0.20 |
| heteroscedastic | 17 | 0 | 3 | 0.47 / 0.55 | 1.00 / 1.00 | 0.00 / 0.15 | 1.00 / 1.00 | 1.00 / 1.00 | 0.12 / 0.25 |
| nonlinear | 15 | 0 | 5 | 0.53 / 0.65 | 0.07 / 0.30 | 0.00 / 0.25 | 0.07 / 0.30 | 0.07 / 0.30 | 0.07 / 0.30 |
| two_laws | 16 | 0 | 4 | 0.19 / 0.35 | 0.12 / 0.30 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 | 0.00 / 0.20 |
| varcoef | 14 | 0 | 6 | 0.29 / 0.50 | 0.07 / 0.35 | 0.00 / 0.30 | 0.07 / 0.35 | 0.07 / 0.35 | 0.00 / 0.30 |

clean G/S rows: 0 crash, 25 timeout (not right; excluded from FA)

## Target (b): run failure on clean data (missed / false flag; risk control alpha = 0.10)

- split: missed 0.00, false flag 1.00 (pos 3, neg 14)
- LOFO F1: missed nan, false flag 1.00 (pos 0, neg 24)
- LOFO F3: missed nan, false flag 1.00 (pos 0, neg 21)
- LOFO F4: missed 0.00, false flag 1.00 (pos 3, neg 8)
- LOFO F5: missed nan, false flag 1.00 (pos 0, neg 17)

## V1 downgrade replay (held-out clean rows, LOFO; 95 rows, 3 flagged)

| category | off | downgrade |
|---|---|---|
| right | 46 | 45 |
| equivalent | 37 | 36 |
| false-confident | 7 | 7 |
| abstain-ok | 3 | 3 |
| abstain | 2 | 4 |
| other | 0 | 0 |

moved: F1 616: right -> abstain; F3 604: equivalent -> abstain

## V1 downgrade replay (held-out injected rows, LOFO; 100 rows, 4 flagged)

| category | off | downgrade |
|---|---|---|
| right | 26 | 24 |
| equivalent | 63 | 63 |
| false-confident | 3 | 2 |
| abstain-ok | 6 | 6 |
| abstain | 2 | 5 |
| other | 0 | 0 |

moved: F2 400: right -> abstain; F2 400: false-confident -> abstain; F3 400: right -> abstain

## Gate

- primary_split: False
- primary_lofo: False
- fa_split: True
- fa_lofo: True
- loto: False
- useful_mid_level: False
- target_b: False
- passed: False
- ships_wrong_set_flag: False
