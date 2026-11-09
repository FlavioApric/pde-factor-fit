# E12 — L0 learned seeds vs pencil + BIC (held-out exponential sums)

n = 1500 draws (seed 12345), nulls = 300 pure-noise series that pass the SNR gate + 300 single pole.

## pencil+BIC
order accuracy 0.848; null/single-pole over-order rate 0.018; 270 s

White noise (the CRB is exact here):

| SNR dB / spacing | n | order acc | over-order | |dλ|/CRB median | p90 |
|---|---|---|---|---|---|
| 20-40 / single/none | 151 | 0.967 | 0.026 | 1.40 | 4.20 |
| 20-40 / |ds|<1.5 | 17 | 0.000 | 0.000 | 0.02 | 0.58 |
| 20-40 / |ds|>=1.5 | 33 | 0.545 | 0.000 | 0.78 | 2.87 |
| <20 / single/none | 328 | 0.985 | 0.003 | 1.07 | 3.57 |
| <20 / |ds|<1.5 | 1 | 0.000 | 0.000 | 0.06 | 0.06 |
| <20 / |ds|>=1.5 | 4 | 0.750 | 0.000 | 0.68 | 2.44 |
| >=40 / single/none | 203 | 0.966 | 0.025 | 1.58 | 14.03 |
| >=40 / |ds|<1.5 | 66 | 0.167 | 0.000 | 0.33 | 3.71 |
| >=40 / |ds|>=1.5 | 130 | 0.777 | 0.031 | 1.47 | 11.58 |

AR(1) noise (white-noise selection and CRB, both misspecified; order columns only):

| SNR dB / spacing | n | order acc | over-order |
|---|---|---|---|
| 20-40 / single/none | 93 | 0.978 | 0.022 |
| 20-40 / |ds|<1.5 | 5 | 0.000 | 0.000 |
| 20-40 / |ds|>=1.5 | 19 | 0.684 | 0.053 |
| <20 / single/none | 180 | 0.972 | 0.022 |
| <20 / |ds|<1.5 | 1 | 0.000 | 0.000 |
| <20 / |ds|>=1.5 | 4 | 1.000 | 0.000 |
| >=40 / single/none | 137 | 0.891 | 0.102 |
| >=40 / |ds|<1.5 | 43 | 0.209 | 0.000 |
| >=40 / |ds|>=1.5 | 85 | 0.706 | 0.047 |

## pencil+BIC+2nd start (control)
order accuracy 0.847; null/single-pole over-order rate 0.018; 521 s

White noise (the CRB is exact here):

| SNR dB / spacing | n | order acc | over-order | |dλ|/CRB median | p90 |
|---|---|---|---|---|---|
| 20-40 / single/none | 151 | 0.967 | 0.026 | 1.40 | 4.20 |
| 20-40 / |ds|<1.5 | 17 | 0.000 | 0.000 | 0.02 | 0.58 |
| 20-40 / |ds|>=1.5 | 33 | 0.545 | 0.000 | 0.78 | 2.87 |
| <20 / single/none | 328 | 0.985 | 0.003 | 1.08 | 3.57 |
| <20 / |ds|<1.5 | 1 | 0.000 | 0.000 | 0.06 | 0.06 |
| <20 / |ds|>=1.5 | 4 | 0.750 | 0.000 | 0.68 | 2.44 |
| >=40 / single/none | 203 | 0.961 | 0.030 | 1.60 | 14.03 |
| >=40 / |ds|<1.5 | 66 | 0.167 | 0.000 | 0.33 | 3.53 |
| >=40 / |ds|>=1.5 | 130 | 0.785 | 0.023 | 1.43 | 11.11 |

AR(1) noise (white-noise selection and CRB, both misspecified; order columns only):

| SNR dB / spacing | n | order acc | over-order |
|---|---|---|---|
| 20-40 / single/none | 93 | 0.978 | 0.022 |
| 20-40 / |ds|<1.5 | 5 | 0.000 | 0.000 |
| 20-40 / |ds|>=1.5 | 19 | 0.684 | 0.053 |
| <20 / single/none | 180 | 0.972 | 0.022 |
| <20 / |ds|<1.5 | 1 | 0.000 | 0.000 |
| <20 / |ds|>=1.5 | 4 | 1.000 | 0.000 |
| >=40 / single/none | 137 | 0.883 | 0.109 |
| >=40 / |ds|<1.5 | 43 | 0.209 | 0.000 |
| >=40 / |ds|>=1.5 | 85 | 0.694 | 0.059 |

## pencil+BIC+L0
order accuracy 0.847; null/single-pole over-order rate 0.018; 533 s

White noise (the CRB is exact here):

| SNR dB / spacing | n | order acc | over-order | |dλ|/CRB median | p90 |
|---|---|---|---|---|---|
| 20-40 / single/none | 151 | 0.967 | 0.026 | 1.40 | 4.20 |
| 20-40 / |ds|<1.5 | 17 | 0.000 | 0.000 | 0.02 | 0.58 |
| 20-40 / |ds|>=1.5 | 33 | 0.545 | 0.000 | 0.78 | 2.87 |
| <20 / single/none | 328 | 0.985 | 0.003 | 1.08 | 3.57 |
| <20 / |ds|<1.5 | 1 | 0.000 | 0.000 | 0.06 | 0.06 |
| <20 / |ds|>=1.5 | 4 | 0.750 | 0.000 | 0.68 | 2.44 |
| >=40 / single/none | 203 | 0.961 | 0.030 | 1.60 | 14.03 |
| >=40 / |ds|<1.5 | 66 | 0.167 | 0.000 | 0.33 | 3.53 |
| >=40 / |ds|>=1.5 | 130 | 0.785 | 0.023 | 1.43 | 11.11 |

AR(1) noise (white-noise selection and CRB, both misspecified; order columns only):

| SNR dB / spacing | n | order acc | over-order |
|---|---|---|---|
| 20-40 / single/none | 93 | 0.978 | 0.022 |
| 20-40 / |ds|<1.5 | 5 | 0.000 | 0.000 |
| 20-40 / |ds|>=1.5 | 19 | 0.684 | 0.053 |
| <20 / single/none | 180 | 0.972 | 0.022 |
| <20 / |ds|<1.5 | 1 | 0.000 | 0.000 |
| <20 / |ds|>=1.5 | 4 | 1.000 | 0.000 |
| >=40 / single/none | 137 | 0.883 | 0.109 |
| >=40 / |ds|<1.5 | 43 | 0.209 | 0.000 |
| >=40 / |ds|>=1.5 | 85 | 0.694 | 0.059 |
