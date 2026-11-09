# S-BASELINES-BENCH — research notes (2026-10-28)

This file holds the research notes for this session, because `RESEARCH.md` at the repo root belongs to MAIN. MAIN may copy them across under `## S-BASELINES-BENCH — 2026-10-28`.

## Fresh search (baselines and benchmark methodology)
| item | verdict | reason |
|---|---|---|
| PySINDy 2.1.0 (installed): STLSQ, EnsembleOptimizer, SBR (numpyro) | baseline | Standard sparse regression. We use its optimizers on our own linear derivative library (see PLAN §3 for why we do not use its `PDELibrary`). |
| WSINDy-PDE (Messenger & Bortz 2021, arXiv 2007.02848, MathBioCU/WSINDy_PDE, MATLAB) | adapt (math only) | Weak form with compactly supported polynomial test functions. Re-implemented in numpy using the same math as `pysindy.WeakPDELibrary` (bump ((s−a)(b−s))^p), so that time orders m ≥ 2 and mixed ∂_t^a∂_x^b terms are possible. |
| Ensemble-SINDy (Fasel et al. 2022) | baseline | Bagging over the weak-form rows. Inclusion frequencies give a structure "probability" whose calibration can be measured. |
| SBR (Hirsh et al. 2022, regularised horseshoe) | baseline | Posterior coefficient samples give a structure distribution after factoring each sample. NUTS is run on the weak system (~200 rows) to keep it affordable. |
| PyDMD 2025.8.1 BOPDMD (Sashidhar & Kutz 2022) | baseline | Eigenvalues λ_j and modes. κ_j comes from the mode's FFT peak, then a monic symbol is least-squares fitted on the (λ, iκ) points and factored. The fitting step is our adapter. |
| Fourier Weak SINDy (arXiv 2604.20141, L4DC 2026) | ignore (for now) | Spectral test-function selection. It is evaluated on ODEs only, so it is a possible later upgrade of the weak baseline. |
| MDBench (arXiv 2509.20529, 2025) | adapt (protocol) | Model-discovery benchmark with PDE-FIND, WSINDy, E-SINDy, Bayesian SINDy and DeePyMoD. It confirms that this set of baselines is the community standard. Its metrics are equation-level; we add factor-level metrics. |
| Bayesian spike-and-slab group lasso (arXiv 2102.01432) | ignore | Close to SBR, with no maintained code. |
| DeePyMoD, EPDE, PySR | ignore (this phase) | Optional per RESEARCH.md; heavier, and not needed for the done criterion. |
| Reliability diagram + ECE + Brier (Guo et al. 2017; DeGroot–Fienberg) | adopt | Used for the calibration of the structure posteriors. |

## Theory → benchmark decisions (proposed rows for analysis/THEORY_TO_ALGO.md; MAIN owns that file)
| result (status) | decision here |
|---|---|
| CONV-T5 (DIMOSTRATO): no data-free threshold | Baselines need a hand rounding tolerance before `sympy.factor_list`. This is reported as a weakness of factoring a fitted symbol, and the sensitivity to the number of decimals d is measured. |
| CONV-T3 (DIMOSTRATO): Ann(·) discontinuous | Structure correctness is scored as a discrete event, and its probability is checked with a reliability diagram. |
| C3-T4 / ATTACK-9 (DIMOSTRATO): mode count | Sparse scattered data (400 points) is expected to fall below identifiability. The label share is reported, not hidden. |
| DM-δ-MINIMAX (DIMOSTRATO): Θ(ε^{1/3}) | The empirical coef_err vs noise slope is reported per method. |
