# P8 final report

Cells: 10 synthetic cases x {grid 1 %, grid 5 %, 400 5 %}, seed 0 (30 inputs).

Sources:

- pipeline: 30 rows (benchmarks\out\p8_pipeline_v5.jsonl)
- pipeline + ML: 30 rows (= pipeline arm (V1 NO-SHIP (stays off), controller C' not built, LB memo bit-identical))
- pdefind: 30 rows (benchmarks\out\e2e_run6.jsonl + benchmarks\out\p8_sindy_schrodinger_cplxsigma.jsonl)
- weak_sindy: 30 rows (benchmarks\out\e2e_run6.jsonl + benchmarks\out\p8_sindy_schrodinger_cplxsigma.jsonl)
- ensemble_sindy: 30 rows (benchmarks\out\e2e_run6.jsonl + benchmarks\out\p8_sindy_schrodinger_cplxsigma.jsonl)
- sbr_sindy: 30 rows (benchmarks\out\e2e_run6.jsonl + benchmarks\out\p8_sindy_schrodinger_cplxsigma.jsonl)
- bopdmd: 30 rows (benchmarks\out\e2e_run6.jsonl + benchmarks\out\p8_sindy_schrodinger_cplxsigma.jsonl)
- pipeline (run 6): 30 rows (benchmarks\out\e2e_run6.jsonl)

## Totals over the 30 P8 inputs

| arm | n | right | equivalent | abstain-ok | abstain | false-confident | wrong | CRASH | right+equiv | factor_set | struct_ok | coef cover90 (n) | weight cover90 (n) | runtime median s | runtime total s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pipeline | 30/30 | 30 | 0 | 0 | 0 | 0 | 0 | 0 | 30 | 30 | 30 | 0.94 (30) | 1.00 (6) | 127.4 | 6923 |
| pipeline + ML | 30/30 | 30 | 0 | 0 | 0 | 0 | 0 | 0 | 30 | 30 | 30 | 0.94 (30) | 1.00 (6) | 127.4 | 6923 |
| pdefind | 30/30 | 4 | 1 | 0 | 0 | 25 | 0 | 0 | 5 | 4 | 11 | - | - | 0.6 | 24 |
| weak_sindy | 30/30 | 23 | 2 | 0 | 0 | 5 | 0 | 0 | 25 | 23 | 21 | - | - | 3.0 | 89 |
| ensemble_sindy | 30/30 | 19 | 3 | 0 | 0 | 8 | 0 | 0 | 22 | 19 | 20 | - | - | 4.8 | 153 |
| sbr_sindy | 30/30 | 20 | 0 | 0 | 0 | 10 | 0 | 0 | 20 | 20 | 20 | - | - | 14.1 | 446 |
| bopdmd | 30/30 | 1 | 0 | 0 | 0 | 29 | 0 | 0 | 1 | 1 | 1 | - | - | 1.5 | 46 |
| pipeline (run 6) | 30/30 | 26 | 0 | 0 | 3 | 1 | 0 | 0 | 26 | 26 | 26 | 0.84 (30) | 0.50 (6) | 5.2 | 1539 |

## Per design

Cells: right+equivalent / abstain(-ok) / false-confident / wrong / CRASH (n).

| arm | grid 1 % | grid 5 % | 400 5 % |
|---|---|---|---|
| pipeline | 10/0/0/0/0 (10) | 10/0/0/0/0 (10) | 10/0/0/0/0 (10) |
| pipeline + ML | 10/0/0/0/0 (10) | 10/0/0/0/0 (10) | 10/0/0/0/0 (10) |
| pdefind | 1/0/9/0/0 (10) | 1/0/9/0/0 (10) | 3/0/7/0/0 (10) |
| weak_sindy | 10/0/0/0/0 (10) | 7/0/3/0/0 (10) | 8/0/2/0/0 (10) |
| ensemble_sindy | 9/0/1/0/0 (10) | 7/0/3/0/0 (10) | 6/0/4/0/0 (10) |
| sbr_sindy | 8/0/2/0/0 (10) | 6/0/4/0/0 (10) | 6/0/4/0/0 (10) |
| bopdmd | 1/0/9/0/0 (10) | 0/0/10/0/0 (10) | 0/0/10/0/0 (10) |
| pipeline (run 6) | 10/0/0/0/0 (10) | 8/1/1/0/0 (10) | 8/2/0/0/0 (10) |

## Per input

| input | pipeline | pipeline + ML | pdefind | weak_sindy | ensemble_sindy | sbr_sindy | bopdmd | pipeline (run 6) |
|---|---|---|---|---|---|---|---|---|
| advection_diffusion grid 1 % | right | right | false-confident | right | right | right | false-confident | right |
| airy grid 1 % | right | right | false-confident | right | right | right | false-confident | right |
| beam grid 1 % | right | right | false-confident | right | right | false-confident | false-confident | right |
| heat grid 1 % | right | right | false-confident | right | right | right | false-confident | right |
| klein_gordon grid 1 % | right | right | false-confident | right | right | right | false-confident | right |
| schrodinger grid 1 % | right | right | false-confident | right | right | right | false-confident | right |
| telegraph grid 1 % | right | right | false-confident | right | right | right | false-confident | right |
| transport grid 1 % | right | right | right | right | right | right | right | right |
| transport_plus_diffusion grid 1 % | right | right | false-confident | right | false-confident | false-confident | false-confident | right |
| wave grid 1 % | right | right | false-confident | equivalent | equivalent | right | false-confident | right |
| advection_diffusion grid 5 % | right | right | false-confident | right | right | right | false-confident | right |
| airy grid 5 % | right | right | false-confident | right | right | right | false-confident | right |
| beam grid 5 % | right | right | false-confident | false-confident | false-confident | false-confident | false-confident | right |
| heat grid 5 % | right | right | false-confident | right | right | right | false-confident | right |
| klein_gordon grid 5 % | right | right | false-confident | right | right | false-confident | false-confident | right |
| schrodinger grid 5 % | right | right | false-confident | false-confident | false-confident | right | false-confident | abstain |
| telegraph grid 5 % | right | right | false-confident | right | right | right | false-confident | right |
| transport grid 5 % | right | right | equivalent | right | right | right | false-confident | right |
| transport_plus_diffusion grid 5 % | right | right | false-confident | false-confident | false-confident | false-confident | false-confident | false-confident |
| wave grid 5 % | right | right | false-confident | equivalent | equivalent | false-confident | false-confident | right |
| advection_diffusion 400 5 % | right | right | right | right | right | right | false-confident | right |
| airy 400 5 % | right | right | false-confident | right | right | right | false-confident | right |
| beam 400 5 % | right | right | false-confident | false-confident | false-confident | false-confident | false-confident | abstain |
| heat 400 5 % | right | right | right | right | right | right | false-confident | right |
| klein_gordon 400 5 % | right | right | false-confident | right | equivalent | false-confident | false-confident | right |
| schrodinger 400 5 % | right | right | false-confident | right | false-confident | right | false-confident | right |
| telegraph 400 5 % | right | right | false-confident | right | right | right | false-confident | right |
| transport 400 5 % | right | right | right | right | right | right | false-confident | right |
| transport_plus_diffusion 400 5 % | right | right | false-confident | false-confident | false-confident | false-confident | false-confident | abstain |
| wave 400 5 % | right | right | false-confident | right | false-confident | false-confident | false-confident | right |

## False-confident and wrong rows

- pipeline: none
- pipeline + ML: none
- pdefind (25): advection_diffusion grid 1 %, airy grid 1 %, beam grid 1 %, heat grid 1 %, klein_gordon grid 1 %, schrodinger grid 1 %, telegraph grid 1 %, transport_plus_diffusion grid 1 %, wave grid 1 %, advection_diffusion grid 5 %, airy grid 5 %, beam grid 5 %, heat grid 5 %, klein_gordon grid 5 %, schrodinger grid 5 %, telegraph grid 5 %, transport_plus_diffusion grid 5 %, wave grid 5 %, airy 400 5 %, beam 400 5 %, klein_gordon 400 5 %, schrodinger 400 5 %, telegraph 400 5 %, transport_plus_diffusion 400 5 %, wave 400 5 %
- weak_sindy (5): beam grid 5 %, schrodinger grid 5 %, transport_plus_diffusion grid 5 %, beam 400 5 %, transport_plus_diffusion 400 5 %
- ensemble_sindy (8): transport_plus_diffusion grid 1 %, beam grid 5 %, schrodinger grid 5 %, transport_plus_diffusion grid 5 %, beam 400 5 %, schrodinger 400 5 %, transport_plus_diffusion 400 5 %, wave 400 5 %
- sbr_sindy (10): beam grid 1 %, transport_plus_diffusion grid 1 %, beam grid 5 %, klein_gordon grid 5 %, transport_plus_diffusion grid 5 %, wave grid 5 %, beam 400 5 %, klein_gordon 400 5 %, transport_plus_diffusion 400 5 %, wave 400 5 %
- bopdmd (29): advection_diffusion grid 1 %, airy grid 1 %, beam grid 1 %, heat grid 1 %, klein_gordon grid 1 %, schrodinger grid 1 %, telegraph grid 1 %, transport_plus_diffusion grid 1 %, wave grid 1 %, advection_diffusion grid 5 %, airy grid 5 %, beam grid 5 %, heat grid 5 %, klein_gordon grid 5 %, schrodinger grid 5 %, telegraph grid 5 %, transport grid 5 %, transport_plus_diffusion grid 5 %, wave grid 5 %, advection_diffusion 400 5 %, airy 400 5 %, beam 400 5 %, heat 400 5 %, klein_gordon 400 5 %, schrodinger 400 5 %, telegraph 400 5 %, transport 400 5 %, transport_plus_diffusion 400 5 %, wave 400 5 %
- pipeline (run 6) (1):
  - transport_plus_diffusion grid 5 %: false-confident, label FIT-COMPATIBLE, cover90 0.86: 1.0*tau + 0.9988554428*xi; 1.0*tau + 1.0043967281*xi; 1.0*tau - 0.2631272871*xi**2

## E13 random PDEs (20 draws, families F1, F2, F3, F4, F5, seeds [0, 1, 2, 3], noise [0.01])

| method | n | right | equivalent | abstain-ok | abstain | false-confident | wrong | CRASH | right+equiv | resolvable right |
|---|---|---|---|---|---|---|---|---|---|---|
| pipeline | 20 | 12 | 7 | 1 | 0 | 0 | 0 | 0 | 19 | 11/16 |
| core | 20 | 5 | 3 | 3 | 3 | 6 | 0 | 0 | 8 | 5/16 |
| pdefind | 20 | 2 | 0 | 0 | 0 | 18 | 0 | 0 | 2 | 2/16 |
| weak_sindy | 20 | 5 | 1 | 0 | 0 | 14 | 0 | 0 | 6 | 4/16 |
| ensemble_sindy | 20 | 6 | 1 | 0 | 0 | 13 | 0 | 0 | 7 | 5/16 |

Pipeline per family:

| family | n | right | equivalent | abstain-ok | abstain | false-confident | wrong | CRASH |
|---|---|---|---|---|---|---|---|---|
| F1 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| F2 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| F3 | 4 | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| F4 | 4 | 1 | 2 | 1 | 0 | 0 | 0 | 0 |
| F5 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |

Right factors but abstained (pipeline; e13_summary.classify checks `ok` first, so these count as right above although no law is claimed): F1-3 (ID-KER), F4-1 (UNDECIDED).

Equivalent factors but abstained (pipeline; classify tests equivalence before the label, so these count as equivalent above although no law is claimed): F3-2 (UNDECIDED, resolvable), F4-0 (UNDECIDED, not resolvable), F4-3 (UNDECIDED, resolvable).

False-confident / wrong / CRASH (pipeline, core):

- core F1-3: false-confident, truth ['tau + 0.000151*xi**4 - 0.00228*xi**3'] -> FIT-COMPATIBLE ['tau - 0.0022763328*xi**3']
- core F3-0: false-confident, truth ['tau**2 - 0.535*tau*xi + 9.32e-5*xi**4 - 0.114*xi**2'] -> FIT-COMPATIBLE ['tau - 0.7016070998*xi + 0.0025328411', 'tau + 0.1638296533*xi - 0.0014567542']
- core F3-3: false-confident, truth ['tau**2 - 0.84*tau*xi + 0.0831*tau + 5.49e-5*xi**4'] -> FIT-COMPATIBLE ['tau - 0.843189069*xi + 0.0833721028', 'tau + 0.0023582796']
- core F5-0: false-confident, truth ['tau**3 + 0.342*tau**2 - 0.427*tau*xi**2 + 0.95*tau + 0.26'] -> FIT-COMPATIBLE ['tau + 0.0114272181', 'tau**2 + 0.3161891559*tau - 0.4276180478*xi**2 - 0.0015969039*xi + 0.9044569989']
- core F5-2: false-confident, truth ['tau**3 + 1.34*tau**2 - 0.283*tau*xi**2 + 0.996*tau + 0.271'] -> FIT-COMPATIBLE ['tau + 0.0152436131', 'tau**2 + 0.0011653858*tau*xi**3 - 0.0032858075*tau*xi**2 + 0.0376134759*tau*xi + 1.1785413081*tau - 0.0062624346*xi**3 - 0.3028207984*xi**2 - 0.1206595217*xi + 0.4335279654']
- core F5-3: false-confident, truth ['tau**3 + 0.923*tau**2 - 0.915*tau*xi**2 + 1.8*tau + 0.519'] -> FIT-COMPATIBLE ['tau + 0.04743913', 'tau**2 - 0.0045359296*tau*xi**2 + 0.0018640752*tau*xi + 0.8334013314*tau - 0.9046146106*xi**2 - 0.0053092279*xi + 1.6880480598']

## Notes

- Not independent trials. All 30 P8 inputs are seed 0: within one seed the arms see the identical noisy input, and the designs of one case share the noise draw (same generator seed, different noise scale or sampling). Arm differences are paired comparisons on the same data; the 30 rows are 10 cases x 3 correlated designs, not 30 independent draws, so no binomial interval over 30 applies. The same holds for E13: every method runs on the same draw.
- P8 classes come from benchmarks/micro.py outcome(); equivalent = same product polynomial as the truth (simulator.match), without the chi^2 half of e13_summary.equivalent. P8 rows carry no resolvability flag, so abstentions count as abstain, not abstain-ok.
- SINDy methods have no labels (n/a), so every wrong SINDy answer is false-confident.
- factor_set / struct_ok are the bench_e2e columns (metrics.score), shown for comparison with earlier tables. coef cover90 = fraction of true coefficients inside the 90 % intervals; weight cover90 = true weights inside the split layer's 90 % intervals (only where the truth has per-factor weights and a split was reported); means over the rows that have them.
- Runtime = per-input wall time. Pipeline arms ran with several workers on a shared machine, so their wall times include contention; SINDy times are from run 6.
