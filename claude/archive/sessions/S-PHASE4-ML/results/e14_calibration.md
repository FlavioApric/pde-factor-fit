# E14 — learned calibration on held-out families (prior: sim-v1)

Corpus: 126 runs (60 train on v1 CASES, 66 test on GENERAL_CASES). Grid data, stand-in posterior (fake_posterior, S = 4), noise 0.1 / 1 / 5 %.

## L2b — P(top structure) as P(right factor set)

right-set rate: train 1.00, test 0.73

| | ECE test | Brier test |
|---|---|---|
| off (raw P(top)) | 0.268 | 0.265 |
| on (isotonic, fitted on train families) | 0.273 | 0.273 |
| on (inductive Venn-Abers) | 0.229 | 0.231 |

## L2c — coverage of nominal 90 % coefficient intervals (z <= 1)

| | train (fit+cal) | test families |
|---|---|---|
| off | 0.669 | 0.756 |
| on | 0.903 | 0.923 |
| median width factor (test) | | 1.53 |

coefficients: 175 train, 156 test. The kappa_vand, log_snr and disagreement features are NaN until the deterministic layer exports them.

## V1

no wrong factor sets in the fit split: nothing to learn (all runs right).

## LOFO over all 21 families (each family held out once; fit/calibrate grouped by family)

runs 126, right-set rate 0.86

| L2b map | ECE | Brier |
|---|---|---|
| off (raw P(top)) | 0.141 | 0.140 |
| isotonic | 0.214 | 0.169 |
| inductive Venn-Abers | 0.242 | 0.145 |

V1 'wrong factor set' flag: OOD (withheld) 0.00; in range: wrong sets caught 0.39 (18 wrong), false-flag rate on right sets 0.08

Labels are never changed by these layers; the numbers above are prior-dependent (prior: sim-v1).
