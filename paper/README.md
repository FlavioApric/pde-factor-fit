# Paper of branch `analytical`

`analytical/main.tex`: *What a Solution Remembers About Its Equation: Groups Are Factors, Terms Interact, and Where Exactness Ends*, by Flavio Pricoco.
Same layout idea as Structure B of the main paper: one idea first (running example), then the grouping principle, then what remains inside a group, then identification, then nonlinear.

- `analytical/sections/thy_*.tex`, `app_proofs.tex`: the theory and proofs (shared with the main paper's Structure B)
- `analytical/sections/port_*.tex`: sections ported from the long manuscript (one-variable prototype, regularity, exact interaction formula and cost, time-dependent perturbation, nonlinear, limits, primer)
- `shared/`: class fallback, macros, bibliography

Build: `cd paper/analytical && latexmk -pdf main.tex`. SIAM's `siamonline` class is not on CTAN; without it the fallback in `shared/siamshim.tex` is used.
License: CC BY 4.0 (`../LICENSE-papers.md`).
