# Domain study (plan 0b.3)

## E2: γ_N against T, L and band (true factors, `e2_gamma.py`)

| case | T = 0.1 | 0.25 | 0.5 | 1 | 2 | 4 | 8 |
|---|---|---|---|---|---|---|---|
| transport+diffusion | 4.7e-4 | 3.0e-3 | 1.2e-2 | 4.6e-2 | 0.17 | 0.54 | 0.73 |
| wave | 1.7e-3 | 1.1e-2 | 4.3e-2 | 0.16 | 0.56 | 0.80 | 0.88 |
| beam | 1.6e-4 | 9.8e-4 | 3.9e-3 | 1.6e-2 | 6.1e-2 | 0.23 | 0.74 |

x-window L = 0.5, 1, 2, 3, 2π at T = 2:
- TPD: 5.4e-4, 3.1e-3, 2.1e-2, 5.8e-2, 0.17.
- Wave: 9.9e-4, 6.5e-3, 8.4e-2, 0.25, 0.56.
- Beam: 3.5e-4, 1.6e-3, 1.1e-2, 2.7e-2, 6.1e-2.

Band [κ_min, κ_max] = [1,2], [1,4], [1,6], [3,6], [5,6]:
- TPD: 0.17, 0.17, 0.17, 0.60, 0.70.
- Beam: 0.06, 0.06, 0.06, 0.87, 0.97.

So γ_N is set by the **lowest κ** in the band (smallest |Δλ(κ)|·T), and it falls **quadratically** with T and L on small cells. Small cells make components inseparable, which confirms the preliminary analysis.

## E3: non-periodic cells (`pencil2d.py`, `e3_domain.py`)
- **What was tried.** A multi-channel matrix pencil in t (shared poles across x), then a pencil in x per λ.
- **Exact data.** The modes are exact (λ to 1e-7). Even so, structfit selects the right structure only for heat, and for wave on L = π/2.
- **Noisy data.** Most modes are lost: at 1e-3, TPD keeps 7 of 24.
- **Cause.** A single stacked Hankel matrix must resolve every exponential of the cell at once: up to 18 poles with decaying amplitudes, with smoothly decaying singular values. This is the open P2-Q3 problem. On a periodic cell, by contrast, the FFT splits it into at most 4 poles per bin.
- **Two-regime test** (transport | heat glued at x = π):
  - whole domain: a wrong 3-factor structure;
  - left half: no modes;
  - right half: one quadratic.
  
  The test is inconclusive, because the extractor fails before grouping is reached.

## Decision for v2
1. Cells are **rectangles**, always simply connected (C12-T1′). Never fill holes.
2. **Multiscale quadtree, coarse to fine, with evidence.** Split a cell only when the children's evidence beats the parent's. Stop when γ_N (computed on the cell with the fitted factors) drops below a floor set by empirical Bayes on single-factor nulls, or when a factor has fewer than n+1 distinct κ (R4-T4). Merge neighbours whose structure posteriors agree.
3. **Prefer splitting in x over splitting in t** at equal evidence: γ ∝ T², and splitting in t also halves the time span.
4. **Extractor on non-periodic cells is a prerequisite.** Use Tukey-windowed FFT with padding and a leakage-aware σ_λ, or 2-D ESPRIT / structured low-rank (Cadzow) with per-bin order selection. This is the work of a new Phase 2 session, S-DOMAIN. Until it passes, the loop only splits along periodic directions or uses windowed FFT.
