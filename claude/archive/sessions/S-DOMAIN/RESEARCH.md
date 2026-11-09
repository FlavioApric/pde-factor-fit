# S-DOMAIN — research notes (2026-10-28)

Fresh search (web + ProblemaBase graph). Verdict per item: adopt / adapt / baseline / ignore.

| item | verdict | reason |
|---|---|---|
| N-D ESPRIT for damped/undamped exponentials, Sahnoun–Usevich–Comon (HAL hal-01360438) | adapt | 2-D ESPRIT on the Hankel-block-Hankel matrix; costly at our sizes (4096 samples). We use its *separable* form: ESPRIT in the undamped direction (x) on a multichannel Hankel, then per-κ 1-D pencil in t. |
| Optimal Hankel-block-Hankel shape (hal-01288994) | adopt | square-ish pencil (L ≈ N/2 in x) for the multichannel x-ESPRIT. |
| MEMP (matrix enhancement + matrix pencil, Hua 1992) | baseline | same subspace as 2-D ESPRIT; the E3 prototype `pencil2d.py` is a t-first variant of it and is our baseline. |
| R-D order selection: EFT/AIC/MDL on higher-order arrays; R-D ESTER (colored noise) | adapt | per-κ order in t by BIC (as core `extract_modes_ic`); global κ order by BIC on the full 2-D LS residual over candidate orders around the noise-threshold rank. |
| Cadzow / SSA structured low-rank (Gillard 2010; IRLS Kümmerle–Verdun arXiv 1811.07472) | adapt | option (c): 2-D Cadzow on the block-Hankel matrix (rank = #2-D modes), then (b). Rank choice is the known weak point; we take it from (b)'s IC. |
| CHORD / convex LRHM (NMR, arXiv 2001.11815) | ignore | needs a regularisation weight; no gain over IC-chosen Cadzow for our sizes. |
| DMD for PDE analysis (arXiv 2203.04728) | ignore | DMD = t-first multichannel pencil = pencil2d failure mode (18 poles in one Hankel). |
| Tukey-windowed FFT + padding | baseline | option (a); main-lobe width ≈ 1.3·2π/L > Δκ = 1 on L = π, so neighbouring κ merge in a bin (expected to lose). Leakage-aware σ_λ: window sidelobe leakage of the other peaks added as noise. |

Key design idea (no theory: empirical, motivated by P2-Q3 APERTO): the pencil2d failure is the t-first Hankel that must
resolve up to 18 damped poles at once. In x all modes are **undamped** (|z| = 1), so a multichannel ESPRIT in x
(shared κ across all t rows) is well conditioned and only needs #distinct κ (12 for TPD); forward-backward averaging
is valid on the unit circle. A Vandermonde LS projection on the estimated κ then decouples the cell exactly (no
leakage), and each κ-channel is a short exponential sum in t (≤ 2 poles here), handled by the core's per-bin BIC pencil.

## Addendum (added during implementation): the free mode model is not identifiable on small cells

Finding (measured, `extract.fisher_sigmas` at the true modes; REPORT.md table F): on a non-periodic window of
length L the 2-D model Σ a_j e^{λ_j t + iκ_j x} with free real κ is ill-conditioned once the κ spacing is near the
Rayleigh limit 2π/L. For wave on L = π the Fisher σ_λ at the *true* modes is 3–20 even at noise 1e-3: a small shift
of κ is absorbed by the neighbours (∂_κ e^{iκx} = ix e^{iκx} lies almost in the span of the κ ± 1 columns on [0, π]).
So no point extractor (FFT, ESPRIT, MEMP, Cadzow, greedy NLS) can give point clouds tight enough for the structured fit
under noise on L ≤ π. This is not a tuning issue.

The *factors* are still determined: by C12-T1′ (simply connected cell) the field lies in Σ_j ker Q_j(∂_t, ∂_x),
and the band-limited kernel of a factor Q is spanned by e^{λ t + iκ x} with Q(λ, iκ) = 0 for κ on a fine grid.
Scoring u directly against that span (data-level variable projection, Golub–Pereyra) removes the free κ and the free
λ: the only unknowns are the factor coefficients. Decision: **adopt** this as the main method
(`domain/kernelfit.py`); the point extractors stay as seeds and as the E3 comparison. Sources: Golub & Pereyra,
"Separable nonlinear least squares: the variable projection method" (Inverse Problems 2003) for the gradient;
C12-T1′/C12-P10 for the kernel decomposition (DIMOSTRATO).
