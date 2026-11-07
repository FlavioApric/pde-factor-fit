# LB fit / calibrate / replay

rows: 165 {'fit': 121, 'cal': 44, 'test': 0}; files ['analysis/exp/out/ll_S_fitcal_off.jsonl', 'analysis/exp/out/ll_G_fitcal_off.jsonl']; fit sha 2f7b677

## profile `exact`: cross-fitted calibration (rule zero, alpha = 0.02, n = 165)

| model | lam | runs harmed | 95 % bound if 0 | saved (total) | saved (median) | per family harmed / n |
|---|---|---|---|---|---|---|
| constant | -1 | 0 | 0.018 | 0.000 | 0.000 | F1 0/35 F2 0/35 F3 0/36 F4 0/25 F5 0/34 |
| logistic | 0 | 0 | 0.018 | 0.000 | 0.000 | F1 0/35 F2 0/35 F3 0/36 F4 0/25 F5 0/34 |
| hgb | 7.83e-06 | 0 | 0.018 | 0.002 | 0.000 | F1 0/35 F2 0/35 F3 0/36 F4 0/25 F5 0/34 |

chosen: hgb, lam = 7.83e-06 (final model fit on all 165 runs)

saved C:\Users\<user>\AppData\Local\Temp\claude\D--Larned-layers--claude-worktrees-ll-budget-287936\cd2e4c41-b494-4013-a35f-93c352966ed6\scratchpad\models\lb_exact.pkl
## profile `fast`: cross-fitted calibration (rule crc, alpha = 0.02, n = 165)

| model | lam | runs harmed | 95 % bound if 0 | saved (total) | saved (median) | per family harmed / n |
|---|---|---|---|---|---|---|
| constant | 0.0968 | 2 | 0.018 | 0.006 | 0.000 | F1 0/35 F2 0/35 F3 2/36 F4 0/25 F5 0/34 |
| logistic | 0.00211 | 2 | 0.018 | 0.001 | 0.000 | F1 0/35 F2 0/35 F3 1/36 F4 1/25 F5 0/34 |
| hgb | 1.51e-05 | 2 | 0.018 | 0.007 | 0.000 | F1 0/35 F2 1/35 F3 1/36 F4 0/25 F5 0/34 |

chosen: hgb, lam = 1.51e-05 (final model fit on all 165 runs)

saved C:\Users\<user>\AppData\Local\Temp\claude\D--Larned-layers--claude-worktrees-ll-budget-287936\cd2e4c41-b494-4013-a35f-93c352966ed6\scratchpad\models\lb_fast.pkl
