# C' oracle sweep (single actions from today's default; full settings; cap 1200 s per run)

| case | off | V1 flag | actions run | rescuing actions | crash / timeout |
|---|---|---|---|---|---|
| F2 s401 ['grid', 0.05] | false-confident | False | 15 | lower_degree | 0 |
| F2 s402 ['grid', 0.05] | false-confident | False | 15 | lower_degree, wide_alternatives | 0 |
| F2 s604 ['grid', 0.05] | false-confident | False | 15 | lower_degree | 0 |
| F2 s606 ['grid', 0.05] | TIMEOUT | None | 6 | lower_degree, narrow_band, varpro | 3 |
| F2 s609 ['grid', 0.05] | false-confident | False | 15 | lower_degree, skip_grow, wide_alternatives | 0 |
| F2 s612 ['grid', 0.05] | abstain | False | 15 | - | 0 |
| F2 s618 ['grid', 0.05] | false-confident | False | 15 | - | 0 |
| F3 s608 ['grid', 0.05] | TIMEOUT | None | 6 | lower_degree, varpro | 4 |
| F4 s601 ['grid', 0.05] | TIMEOUT | None | 6 | - | 6 |
| F4 s609 ['grid', 0.05] | abstain | False | 15 | lower_degree, sigma_reest | 0 |
| F4 s617 ['grid', 0.05] | false-confident | False | 15 | - | 0 |
| F5 s603 ['grid', 0.05] | TIMEOUT | None | 6 | lower_degree, narrow_band, sigma_reest, skip_grow, skip_recurse, varpro | 0 |

- off failures in the sweep: 12
- oracle ceiling (any action rescues): 8/12 = 67%
- V1 triggers (flag at alpha 0.05, held-out family): 0/12 failures
- ceiling with V1 as the trigger (flagged and rescued): 0/12 = 0%
- rescues per action: lower_degree 8, varpro 3, wide_alternatives 2, narrow_band 2, skip_grow 2, sigma_reest 2, skip_recurse 1
- V1 false alarms on clean cases the off run gets right (or abstains correctly): 3/86
