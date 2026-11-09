# S-DOMAIN — PLAN (Phase 2, plan v2.2)

Session S-DOMAIN; owns `src/pdefactor/domain/`, `tests/test_domain.py`, `analysis/exp/domain_*`.
Plan section: v2.2 "Domain strategy" (DOMAIN.md, decision 1–4).

## Goal / done
- E3 sub-window test: right structure for transport_plus_diffusion ((1,1),(1,2)) and wave ((1,1),(1,1)) on L = π at noise 1e-3.
- Two-regime field: left half → τ+ξ, right half → τ−0.3ξ²; quadtree split found near x = π.
- `pytest tests/test_domain.py` green; REPORT.md with tables vs `pencil2d.py`.

## Theory → choices
- Rectangular cells only, quadtree keeps them simply connected: C12-T1′ (DIMOSTRATO), C12-P10 (DIMOSTRATO) — THEORY_TO_ALGO T1.
- Stop on γ_N < floor, γ_N from the full block Gram (`core.components.gamma_N`): P2-T3 / P2-C2 (DIMOSTRATO) — T5.
- Stop when a factor has < n+1 distinct κ (R4-T4); spread κ preferred (P2-P6, DIMOSTRATO — T9).
- Extractor conditioning: P2-Q3 APERTO — T10: **no theory, empirical** comparison (a)/(b)/(c).
- Windowing/padding never encodes BCs: CONV-B1 (DIMOSTRATO) — T19; the extractor returns only interior modes, and filters spatially non-oscillatory (Re μ ≠ 0) x-exponentials.
- Prefer x-splits at equal evidence: DOMAIN.md decision 3 (γ ∝ T²).

## API
`domain/extract.py`
- `extract_fft_tukey(u, t, x, noise, pad=4)` → `Extraction`  (a)
- `extract_esprit(u, t, x, noise, ...)` → `Extraction`        (b) x-first multichannel ESPRIT, BIC order for κ, per-κ BIC pencil in t
- `extract_cadzow(u, t, x, noise, ...)` → `Extraction`        (c) 2-D Cadzow then (b)
- `Extraction`: `modes: core.spectral.Modes`, `sig_lam`, `sig_kappa`, `rss`, `n_samples`, `noise`, `method`.
- `fit_cell(ext, t, ...)` → `(best Fit, ranked, sig_eff)`: core `fit_structure` / `candidate_structures` with the
  extractor's own σ (σ_λ from a full 2-D Fisher, + |dλ/dκ| σ_κ from the first-pass fit).
`domain/quadtree.py`
- `Cell(t0,t1,x0,x1)`, `cell_evidence(u, t, x, cell, noise, ...)` → `CellFit` (BIC on the data of the cell).
- `quadtree(u, t, x, noise, gamma_floor=GAMMA_FLOOR, ...)` → list of leaf `CellFit` after merge.

## Evidence of a cell (data-level, comparable between parent and children since they cover the same samples)
BIC = RSS_free/σ² + χ²_struct + k·ln N, with k = 2·#modes (amplitudes) + #distinct κ + npar(structure) + 2·#outlier modes.
(χ²_struct is the CRB-unit cost of moving each λ onto the fitted variety: to first order the RSS increase.)

## Parameters
- `gamma_floor`: default from experiment (γ_N of the true structures across cell sizes vs structure recovery); to be replaced by
  empirical Bayes on single-factor nulls (CLAUDE.md rule 4) — stated as a TODO hyperparameter.
- min cell size (samples): structural (needs ≥ 2·#κ samples per direction), not tuned.
- split positions: fractions {1/4, 3/8, 1/2, 5/8, 3/4}, chosen by evidence (not hand-set).
- ESPRIT/pencil thresholds: snr_min = 3 as in core; orders by BIC.

## Tests first (`tests/test_domain.py`)
1. exact multi-κ field on a non-periodic window: ESPRIT recovers κ and λ to 1e-6.
2. TPD and wave on L = π, noise 1e-3: best structure correct.
3. two-regime: halves give their own law; quadtree first split within 0.5 of π.
4. Cadzow keeps a low-rank field fixed and reduces noise.

## Addendum (added during implementation): data-level kernel fit

The point-level BIC above fails under noise on L ≤ π (RESEARCH.md addendum, REPORT.md table F). Added
`domain/kernelfit.py` and `domain/fit.analyze_cell`:
- κ grid: Blackman–Harris band of the data, step 2π/(oversample·(L + 2T)); kernel columns e^{λ(κ) t + iκ x} for every
  root λ of each factor at each grid κ (Re λ capped).
- evidence: BIC = RSS/σ² + (2·dof + 2·npar)·ln N, dof = numerical rank of the kernel basis, σ known.
- fit: VarPro with analytic gradient (dRSS = −2 Re rᴴ(∂B)a, ∂λ/∂c = −ξ^b λ^k / Q_λ), L-BFGS-B, separable Gram
  (Hadamard product of the t and x Grams), Cholesky solve.
- candidates: core.structfit.candidate_structures; seeds from the point extractor, from absolute factorisation of
  fitted m ≥ 2 symbols (core.variety.factorise) and greedy ξ-degree reduction, decided by BIC.
- quadtree evidence = this BIC (additive over cells covering the same samples).
