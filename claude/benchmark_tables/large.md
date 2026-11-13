# Large random-PDE benchmark

285 draws (equations x noise), families F1, F2, F3, F4, F5, 285 distinct equations, noise [0.01] (x std u), noisy regular grid. Each draw is an independent equation with an independent field; none was used to tune the pipeline. Intervals are 95 %.

## All draws (n = 285)

| method | right+equiv % [Wilson] | right | equivalent | abstain-ok | abstain | false-confident | wrong | CRASH | false-conf upper 95 % |
|---|---|---|---|---|---|---|---|---|---|
| pipeline | 96.5 [93.7, 98.1] | 187 | 88 | 1 | 8 | 0 | 0 | 1 | 1.0 % |
| weak_sindy | 28.4 [23.5, 33.9] | 77 | 4 | 0 | 0 | 204 | 0 | 0 | 76.0 % |

Paired on the same draws (exact sign test, right+equivalent): weak_sindy: pipeline-only 194, weak_sindy-only 0, p = 8e-59

## Noise 0.01 (n = 285)

| method | right+equiv % [Wilson] | right | equivalent | abstain-ok | abstain | false-confident | wrong | CRASH | false-conf upper 95 % |
|---|---|---|---|---|---|---|---|---|---|
| pipeline | 96.5 [93.7, 98.1] | 187 | 88 | 1 | 8 | 0 | 0 | 1 | 1.0 % |
| weak_sindy | 28.4 [23.5, 33.9] | 77 | 4 | 0 | 0 | 204 | 0 | 0 | 76.0 % |

Paired on the same draws (exact sign test, right+equivalent): weak_sindy: pipeline-only 194, weak_sindy-only 0, p = 8e-59

## Family F1 (n = 60)

| method | right+equiv % [Wilson] | right | equivalent | abstain-ok | abstain | false-confident | wrong | CRASH | false-conf upper 95 % |
|---|---|---|---|---|---|---|---|---|---|
| pipeline | 100.0 [94.0, 100.0] | 59 | 1 | 0 | 0 | 0 | 0 | 0 | 4.9 % |
| weak_sindy | 70.0 [57.5, 80.1] | 42 | 0 | 0 | 0 | 18 | 0 | 0 | 41.2 % |

Paired on the same draws (exact sign test, right+equivalent): weak_sindy: pipeline-only 18, weak_sindy-only 0, p = 7.6e-06

## Family F2 (n = 60)

| method | right+equiv % [Wilson] | right | equivalent | abstain-ok | abstain | false-confident | wrong | CRASH | false-conf upper 95 % |
|---|---|---|---|---|---|---|---|---|---|
| pipeline | 90.0 [79.9, 95.3] | 31 | 23 | 1 | 5 | 0 | 0 | 0 | 4.9 % |
| weak_sindy | 15.0 [8.1, 26.1] | 9 | 0 | 0 | 0 | 51 | 0 | 0 | 91.9 % |

Paired on the same draws (exact sign test, right+equivalent): weak_sindy: pipeline-only 45, weak_sindy-only 0, p = 5.7e-14

## Family F3 (n = 60)

| method | right+equiv % [Wilson] | right | equivalent | abstain-ok | abstain | false-confident | wrong | CRASH | false-conf upper 95 % |
|---|---|---|---|---|---|---|---|---|---|
| pipeline | 98.3 [91.1, 99.7] | 41 | 18 | 0 | 1 | 0 | 0 | 0 | 4.9 % |
| weak_sindy | 46.7 [34.6, 59.1] | 26 | 2 | 0 | 0 | 32 | 0 | 0 | 64.4 % |

Paired on the same draws (exact sign test, right+equivalent): weak_sindy: pipeline-only 31, weak_sindy-only 0, p = 9.3e-10

## Family F4 (n = 48)

| method | right+equiv % [Wilson] | right | equivalent | abstain-ok | abstain | false-confident | wrong | CRASH | false-conf upper 95 % |
|---|---|---|---|---|---|---|---|---|---|
| pipeline | 95.8 [86.0, 98.8] | 12 | 34 | 0 | 1 | 0 | 0 | 1 | 6.1 % |
| weak_sindy | 2.1 [0.4, 10.9] | 0 | 1 | 0 | 0 | 47 | 0 | 0 | 99.9 % |

Paired on the same draws (exact sign test, right+equivalent): weak_sindy: pipeline-only 45, weak_sindy-only 0, p = 5.7e-14

## Family F5 (n = 57)

| method | right+equiv % [Wilson] | right | equivalent | abstain-ok | abstain | false-confident | wrong | CRASH | false-conf upper 95 % |
|---|---|---|---|---|---|---|---|---|---|
| pipeline | 98.2 [90.7, 99.7] | 44 | 12 | 0 | 1 | 0 | 0 | 0 | 5.1 % |
| weak_sindy | 1.8 [0.3, 9.3] | 0 | 1 | 0 | 0 | 56 | 0 | 0 | 99.9 % |

Paired on the same draws (exact sign test, right+equivalent): weak_sindy: pipeline-only 55, weak_sindy-only 0, p = 5.6e-17

## False-confident / wrong / CRASH (pipeline, core)

- pipeline F4-10 noise 0.01: CRASH, truth ['tau - 0.00377*xi**2 - 0.137*xi + 0.456', 'tau**2 - 0.121*tau*xi + 0.173*tau + 0.0234*xi**4'] -> CRASH []

## Draws without a result (15 of 300 planned)

These draws hit the per-draw time limit (3 h) or failed; they carry no row, so they are NOT counted in the tables above. Reading the tables as if they were abstentions would be wrong: the denominators exclude them. Share per family: F1 0/60, F2 0/60, F3 0/60, F4 12/60, F5 3/60.

Worst case for the pipeline, counting every missing draw as a failure: 275/300 = 91.7 % right+equivalent (Wilson 95 % 88.0-94.3). The tables above are conditional on the draw finishing within the limit; the slowest draws are not a random subset.

Reading the baselines: weak_sindy always returns one equation and never abstains, so every wrong answer is counted as false-confident by construction.

- F4-1 noise 0.01
- F4-2 noise 0.01
- F4-6 noise 0.01
- F4-12 noise 0.01
- F4-15 noise 0.01
- F4-18 noise 0.01
- F4-36 noise 0.01
- F4-37 noise 0.01
- F4-38 noise 0.01
- F4-42 noise 0.01
- F4-49 noise 0.01
- F4-52 noise 0.01
- F5-0 noise 0.01
- F5-20 noise 0.01
- F5-49 noise 0.01
