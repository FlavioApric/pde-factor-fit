# P8 summary (2026-10-31)

Cells: 10 synthetic cases x {grid 1 %, grid 5 %, 400 points 5 %}, seed 0 (30 inputs). "right" = factor_set; "struct ok" = struct_ok; outcome = `benchmarks/micro.py outcome()` (an answer is a claim only when labelled FIT-COMPATIBLE; SINDy methods have no labels, so every wrong SINDy answer counts as false-confident; repeated-root truths count UNDECIDED as right).
SINDy rows and the "pipeline (run 6)" row are from `e2e_run6.jsonl` (see `p8_sindy_arm.md`: inputs unchanged since run 6). "pipeline (now)" = current main, defaults (layers off), `benchmarks/out/p8_pipeline.jsonl` (the run also produced 400 1 % rows, which are not P8 cells and are excluded here). Runtime = sum of per-input wall time in s (pipeline now: 4 workers sharing a 6-core machine with other jobs).

| method | grid 0.01 | grid 0.05 | 400 0.05 | total right | struct ok | right (outcome) | abstain | false-confident | error | runtime s |
|---|---|---|---|---|---|---|---|---|---|---|
| pipeline (now) | 10/10 | 10/10 | 9/10 | 29/30 | 29/30 | 29 | 0 | 1 | 0 | 6604 |
| pipeline (run 6) | 10/10 | 8/10 | 8/10 | 26/30 | 26/30 | 26 | 3 | 1 | 0 | 1539 |
| pipeline + ML | pending (P7 not done) | pending | pending | pending | pending | pending | pending | pending | pending | pending |
| pdefind | 1/10 | 0/10 | 3/10 | 4/30 | 11/30 | 4 | 0 | 26 | 0 | 24 |
| weak_sindy | 9/10 | 6/10 | 8/10 | 23/30 | 21/30 | 23 | 0 | 7 | 0 | 94 |
| ensemble_sindy | 8/10 | 6/10 | 5/10 | 19/30 | 20/30 | 19 | 0 | 11 | 0 | 158 |
| sbr_sindy | 8/10 | 6/10 | 6/10 | 20/30 | 20/30 | 20 | 0 | 10 | 0 | 438 |
| bopdmd | 1/10 | 0/10 | 0/10 | 1/30 | 1/30 | 1 | 0 | 29 | 0 | 117 |

## Pipeline per input: run 6 -> now

| input | run 6 label | run 6 right | run 6 outcome | now label | now right | now outcome | now time s | now factors |
|---|---|---|---|---|---|---|---|---|
| advection_diffusion grid 0.01 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 16 | 1.0*tau - 0.300084317362626*xi**2 + 1.00003777663993*xi |
| airy grid 0.01 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 33 | 1.0*tau + 0.0499876055661831*xi**3 |
| beam grid 0.01 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 737 | 1.0*tau + 0.300022408464036*I*xi**2; 1.0*tau - 0.300022408464036*I*xi**2 |
| heat grid 0.01 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 25 | 1.0*tau - 0.300062272535313*xi**2 |
| klein_gordon grid 0.01 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 163 | 1.0*tau**2 - 0.999945085718317*xi**2 + 0.999921664773414 |
| schrodinger grid 0.01 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 41 | 1.0*tau - 0.299976482300445*I*xi**2 |
| telegraph grid 0.01 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 303 | 1.0*tau**2 + 0.8001552327471*tau - 0.999798714530156*xi**2 |
| transport grid 0.01 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 14 | 1.0*tau + 1.00002468117188*xi |
| transport_plus_diffusion grid 0.01 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 476 | 1.0*tau + 1.00011867653877*xi; 1.0*tau - 0.299577309214567*xi**2 |
| wave grid 0.01 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 125 | 1.0*tau - 0.9999666587837*xi; 1.0*tau + 0.9999666587837*xi |
| advection_diffusion grid 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 19 | 1.0*tau - 0.300422030727247*xi**2 + 1.00018938029267*xi |
| airy grid 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 30 | 1.0*tau + 0.0499367406173454*xi**3 |
| beam grid 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 418 | 1.0*tau - 1.94849765120485e-16*xi**2 + 0.300105977279165*I*xi**2; 1.0*tau + 4.03125849487897e-16*xi**2 - 0.300105977279161*I*xi**2 |
| heat grid 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 28 | 1.0*tau - 0.300311265936475*xi**2 |
| klein_gordon grid 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 208 | 1.0*tau**2 - 0.999727407514226*xi**2 + 0.999606381814829 |
| schrodinger grid 0.05 | ID-KER | False | abstain | FIT-COMPATIBLE | True | right | 38 | 1.0*tau - 0.299881959987729*I*xi**2 |
| telegraph grid 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 391 | 1.0*tau**2 + 0.800776661408748*tau - 0.998990205324216*xi**2 |
| transport grid 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 16 | 1.0*tau + 1.00012385270215*xi |
| transport_plus_diffusion grid 0.05 | FIT-COMPATIBLE | False | false-confident | FIT-COMPATIBLE | True | right | 372 | 1.0*tau + 1.00058822381244*xi; 1.0*tau - 0.297956918731529*xi**2 |
| wave grid 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 187 | 1.0*tau - 0.999832183542648*xi; 1.0*tau + 0.999832183542648*xi |
| advection_diffusion 400 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 47 | 1.0*tau - 0.297535841617899*xi**2 + 1.00171103485133*xi |
| airy 400 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 82 | 1.0*tau + 0.0503092876972857*xi**3 |
| beam 400 0.05 | UNDECIDED | False | abstain | FIT-COMPATIBLE | True | right | 669 | 1.0*tau + 9.79187874717864e-16*xi**2 + 0.301430963888965*I*xi**2; 1.0*tau + 1.55838815701741e-16*xi**2 - 0.301430963888966*I*xi**2 |
| heat 400 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 69 | 1.0*tau - 0.301248693496561*xi**2 |
| klein_gordon 400 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 539 | 1.0*tau**2 - 1.00405163522857*xi**2 + 0.991233145167747 |
| schrodinger 400 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 97 | 1.0*tau - 0.300621756522853*I*xi**2 |
| telegraph 400 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 487 | 1.0*tau**2 + 0.79226168765493*tau - 1.00331713999574*xi**2 |
| transport 400 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 82 | 1.0*tau + 1.00173067877912*xi |
| transport_plus_diffusion 400 0.05 | UNDECIDED | False | abstain | FIT-COMPATIBLE | False | false-confident | 456 | 1.0*tau + 1.01099072999215*xi; 1.0*tau + 0.790702151079221 - 0.189285425943035*I; 1.0*tau + 0.79070215107922 + 0.189285425943035*I |
| wave 400 0.05 | FIT-COMPATIBLE | True | right | FIT-COMPATIBLE | True | right | 436 | 1.0*tau - 1.00175492686777*xi; 1.0*tau + 1.00175492686777*xi |

## Notes

- Pipeline now: 29/30 right (run 6: 26/30). Fixed vs run 6: schrodinger grid 5 % (ID-KER -> right),
  transport_plus_diffusion grid 5 % (false-confident -> right), beam 400 5 % (UNDECIDED -> right).
  No abstentions, no errors, no timeouts (40/40 inputs ran, incl. the 10 non-P8 400 1 % rows).
- New false-confident: transport_plus_diffusion 400 5 % s0 (run 6: UNDECIDED). Reported
  (tau + 1.011 xi)(tau^2 + 1.581 tau + 0.661), the xi^2 term of the diffusion factor lost; truth
  (tau + xi)(tau - 0.3 xi^2). Labelled FIT-COMPATIBLE with the default T88 RAW_GOF on: the raw
  goodness-of-fit check did not turn it into MISFIT on this input (HANDOFF said the edge-suite TPD 400 5 %
  case is MISFIT under T88, not rerun; it is not caught here). cover90 0.6.
- Best SINDy method (weak_sindy) 23/30 right, 21/30 struct ok, 7 wrong answers (no abstention possible).
- Runtime: pipeline now 6604 s summed over the 30 P8 inputs vs 1539 s in run 6 (4.3x; now measured with
  4 workers alongside other jobs, so wall times are inflated by contention). SINDy totals 24-438 s.
- pipeline + ML: pending (P7 not done).
