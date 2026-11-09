# LB fit / calibrate / replay

rows: 165 {'fit': 121, 'cal': 44, 'test': 0}; files ['analysis/exp/out/ll_S_fitcal_off.jsonl', 'analysis/exp/out/ll_G_fitcal_off.jsonl']; fit sha 2f7b677

## profile `exact` (rule zero, alpha = 0.02)

### calibrate split, all families

| model | lam | lam (CRC) | lam (LTT) | n | harmed | saved (total) | saved (median) |
|---|---|---|---|---|---|---|---|
| constant | -1 | -1 | -1 | 44 | 0.000 | 0.000 | 0.000 |
| logistic | 0.0287 | -1 | -1 | 44 | 0.000 | 0.038 | 0.000 |
| hgb | 0.000196 | -1 | -1 | 44 | 0.000 | 0.030 | 0.000 |

### chosen logistic, lam = 0.0287. LOFO: fit + calibrate on four families, replay on the fifth (all its rows)

| held out | kind | lam | n | harmed | 95 % bound if 0 | saved (total) | median off -> on (s) |
|---|---|---|---|---|---|---|---|
| F1 | hgb | 0.00043 | 35 | 0 | 0.082 | 0.030 | 27 -> 27 |
| F2 | hgb | 0.000285 | 35 | 1 | 0.082 | 0.060 | 40 -> 28 |
| F3 | logistic | 0.0196 | 36 | 1 | 0.080 | 0.016 | 959 -> 959 |
| F4 | hgb | 3.7e-05 | 25 | 2 | 0.113 | 0.036 | 1200 -> 1200 |
| F5 | constant | 0.2 | 34 | 1 | 0.084 | 0.032 | 826 -> 792 |
| all | | | 165 | 5 | 0.018 | | |

saved C:\Users\<user>\AppData\Local\Temp\claude\D--Larned-layers--claude-worktrees-ll-budget-287936\cd2e4c41-b494-4013-a35f-93c352966ed6\scratchpad\models\lb_exact.pkl
## profile `fast` (rule crc, alpha = 0.02)

### calibrate split, all families

| model | lam | lam (CRC) | lam (LTT) | n | harmed | saved (total) | saved (median) |
|---|---|---|---|---|---|---|---|
| constant | -1 | -1 | -1 | 44 | 0.000 | 0.000 | 0.000 |
| logistic | -1 | -1 | -1 | 44 | 0.000 | 0.000 | 0.000 |
| hgb | -1 | -1 | -1 | 44 | 0.000 | 0.000 | 0.000 |

### chosen constant, lam = -1. LOFO: fit + calibrate on four families, replay on the fifth (all its rows)

| held out | kind | lam | n | harmed | 95 % bound if 0 | saved (total) | median off -> on (s) |
|---|---|---|---|---|---|---|---|
| F1 | constant | -1 | 35 | 0 | 0.082 | 0.000 | 27 -> 27 |
| F2 | constant | -1 | 35 | 0 | 0.082 | 0.000 | 40 -> 40 |
| F3 | constant | -1 | 36 | 0 | 0.080 | 0.000 | 959 -> 959 |
| F4 | constant | -1 | 25 | 0 | 0.113 | 0.000 | 1200 -> 1200 |
| F5 | constant | -1 | 34 | 0 | 0.084 | 0.000 | 826 -> 826 |
| all | | | 165 | 0 | 0.018 | | |

saved C:\Users\<user>\AppData\Local\Temp\claude\D--Larned-layers--claude-worktrees-ll-budget-287936\cd2e4c41-b494-4013-a35f-93c352966ed6\scratchpad\models\lb_fast.pkl
