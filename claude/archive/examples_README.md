# Worked examples (model-expansion paper, section 5)

| script | level | checks | what it shows |
|---|---|---|---|
| `ex_L6_dirac.py` | L6 systems | 7/7 | Dirac in 1+1: Klein-Gordon factorisation, rank-8 pointwise system |
| `ex_L7_poschl_teller.py` | L7 variable coefficient | 11/11 | residual map gives V = q; Darboux translation loses the bound state |
| `ex_L8_stark.py` | L8 time dependent | 5/5 | Avron-Herbst exact solution, V up to a function of t |
| `ex_L9_L10_dict.py` | L9, L10 | 12/12 | dictionary on the heat equation: misfit, fit with bound, no law |

Run one: `cd examples && python -I ex_L6_dirac.py`. The `.out` files are stored outputs. Needs `sympy` and `mpmath`.
The scripts are symbolic or 25-40 digit checks, not proofs. Their printed messages are in Italian (the working language of the first version).
