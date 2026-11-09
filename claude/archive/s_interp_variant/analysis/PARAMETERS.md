# Parameters and control quantities (Phase 0b, deliverable 0b.1)

Experiments: `analysis/exp/e1_noise.py` (core), `e1b_structfit.py` (structured fit), `e2_gamma.py`, `e3_domain.py`, `e4_theory.py`, `e5_bayes_split.py`. Raw outputs are in `analysis/exp/out/`, which is gitignored and can be regenerated. Theory IDs refer to `THEORY_TO_ALGO.md`.

Control column: **C** = we control it, **E** = we can only estimate it from data, **N** = neither (we only report it).

| Parameter / quantity | Affects | Governing result | Control | How estimated | Default (v2) | Evidence | Verdict |
|---|---|---|---|---|---|---|---|
| Factor tolerance `ftol` (core v1: 5e-2) | whether P is factored | CONV-T5 (no data-free threshold) | C | — | **removed** | E1: KG and telegraph are falsely factored from 1e-4 noise | **reject**. Replace with BIC model comparison over structures (`structfit`) |
| Structure set (k ≤ 3 factors, m_j ∈ {1,2}, dx_j ≤ 4) | factor set | C12-P2, II-C1 | C | posterior over structures | m_max 3, dx_max 4 | E1b: 10/10 cases right up to 1e-3 noise, 8/10 at 1e-1 | **adopt** |
| σ_λ (uncertainty of each dispersion point) | residual units, BIC | Cramér–Rao | E | full Fisher over all exponentials in the same FFT bin | — | a 2×2 CRB underestimated σ and caused overfitting; the full-bin Fisher fixed it | **adopt (full bin)** |
| Noise scale s on σ_λ | BIC | — | E | Jeffreys prior, s ≥ 1 | — | without the floor, exact data overfit | **adopt** |
| Robust residual cap | outlier modes (unresolved exponentials) | — | C | cap z² at (3s)² | c = 3 | fixed cap: TPD 1.0 up to 1e-2. Adaptive s: needed on the 2-D pencil, slightly worse on TPD at 1e-2 (0.7) | **modify**: v2 uses a mixture likelihood with outlier fraction and s marginalised |
| γ_N (= 1 − c_F for N = 2) | amplification γ_N^{-1/2} of component errors | P2-T3, P2-T4, P2-C2 | E (fixed domain), **C through the domain** | full block Gram of kernel bases on the cell and band | floor to be set by empirical Bayes | E2: γ_N ∝ T² and ∝ L² for small cells; set by the lowest κ in the band | **adopt** as an error bar, stop rule and domain criterion |
| Time span T | γ_N, branch slopes | P2-T3 | C (window) | — | as long as the cell allows | E2: TPD γ = 5e-4 (T = 0.1) → 0.17 (T = 2) → 0.73 (T = 8) | **adopt**: prefer long windows in t (splitting in t is cheap and causal, but costs γ) |
| x-window L | γ_N, Δκ | P2-T3 | C | — | ≥ 2π/κ_min of the band | E2: γ falls about 300× from L = 2π to L = 0.5 | **adopt**: minimum cell size from γ_N, not by hand |
| κ-band [κ_min, κ_max] | γ_N, identifiability | P2-P6, R4-T4 | C | SNR cut | drop the lowest κ if it alone limits γ | E2: removing κ = 1, 2 raises γ_beam from 0.06 to 0.87 | **adopt** a band choice by evidence |
| SNR cut `snr_min` | modes kept | — | C | — | 3 | E1: missing diffusion modes at high κ | keep; with structfit, missing branches no longer break the fit |
| Pencil order | λ bias | P2-Q3 (open) | C | rank of the Hankel matrix | — | TPD outliers at k = ±5 come from an unresolved exponential merged into another | **modify**: per-bin order by an information criterion (Phase 1 v2) |
| Discriminant-square test (m = 2) | reducibility | C12-P2 | — | root pairing | — | exact: perfect (gap 0 vs 2.0 and 0.8). Noise 1e-3: wave 0.62 vs telegraph 0.64, so they overlap | **reject as a hard test**; keep as a feature. Structfit's evidence already does this statistically |
| Shared κ = 0 mode (δ(P) > 0) | split ambiguity | C12-T2, C12-T1 | N | n_shared | — | E4: core OK on exact data (shared = 1). At 1e-3 noise the core merges into one quadratic; structfit is right (p = 0.89) | structfit **adopt** |
| Repeated roots (Q²) | multiplicity | OPF5B-T6 | — | — | — | E4: core and structfit both return a confident simple factor (p = 0.96) | **gap** → v2 adds a confluent-Prony (A + Bt)e^{λt} model to the comparison, and labels UNDECIDED when it wins |
| Prior scale τ² (split layer) | shrinkage | 0b.10 | E | empirical Bayes (closed-form evidence) | grid 1e-6..1e2 | E5 works | **adopt** |
| Split-layer likelihood | coverage of w intervals | 0b.10 | C | — | — | E5: coverage 0.65–0.85 at nominal 0.90 | **modify**: real (conjugate-pair) parametrisation for real fields; noise from the GP posterior (K_post) |
| E_int, ρ | stop rule | OPA-T3, P1-P1(e) | N | sampled distribution only | — | not re-measured here (core tests pass) | keep as a distribution |
| ε₁, ε₂, γ floor | loop | CONV-T5 | E | empirical Bayes on single-factor nulls (0b.8) | — | Phase 3 | keep plan |

## Default parameters for v2
- Structure search: k ≤ 3, m_j ∈ {1, 2}, dx_j ≤ 4, 8 random + 2 sorted initialisations, 30 alternating iterations.
- σ_λ: full-bin CRB × bin noise σ/√n_x. Scale s ≥ 1 with a Jeffreys prior. Residual cap 3s.
- Grid per cell: nt ≥ 48, nx ≥ 64. T and L as large as the cell allows. Cell accepted only if γ_N ≥ γ_floor (empirical Bayes).

## Phase 1 v2 update (2026-10-28)
- **Pencil order: adopted.** Per-bin order is chosen by BIC among r0..r0+2 (`extract_modes_ic`). With it, transport+diffusion at 1e-2 noise goes from 0.7 to 1.0.
- **Repeated roots: adopted.** The confluent test (BIC, simple pair vs (A+Bt)e^{λt}) labels (τ+ξ)² UNDECIDED. It also flags beam at 1e-1, where the branches are unresolved.
- **Core v2 regression (E1c).** The right factor set is found in 58 of the 60 (case, noise) cells, against 56 for the prototype. The failures are transport+diffusion at 3e-2 (0.7) and at 1e-1 (0).
