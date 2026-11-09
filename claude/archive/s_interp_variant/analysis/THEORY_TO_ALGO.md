# THEORY → ALGORITHM: what the analytic work decides for us

Source: `D:\ProblemaBase` (read-only). Mainly `ALGORITMO_ESTESO.md` (S9-ALG rev. 2, with the Phase 10 errata) and `claims/LEDGER.md`, navigated with the graphify graph (`D:\ProblemaBase\graphify-out`, 3721 nodes). Status in brackets is the LEDGER status. Only DIMOSTRATO rows (or CON-FONTE with a verified source) are used as foundations; anything else is marked.

**Rule.** Before choosing or changing an algorithm, look up the relevant results here, and in the graph with `graphify query "<topic>"` run from `D:\ProblemaBase`. If a result is not listed here, add a row.

## 1. Decisions the theory already takes

| # | result (status) | what it says | decision in PDEFactorML |
|---|---|---|---|
| T1 | C12-T1, C12-T1′ (DIMOSTRATO); C12-P10, OPF-T4 (DIMOSTRATO) | ker P = Σ ker Q_j on rectangles and simply connected Ω; fails with holes (defect ≤ δ(P)·b₁(Ω)) | analyse only rectangles/convex cells; a quadtree keeps cells simply connected by construction; no region growing into annuli (DOMAIN.md) |
| T2 | C12-T2 (DIMOSTRATO) | P = Π(τ − a_j): δ(P) = deg Δ (discriminant); the projector Π_j has poles only where its own branch collides | **check:** the core's `n_shared` must equal the number of κ in the band where branches collide (counted with multiplicity); shared modes are exactly those κ. Add a test (wave: δ = 1; beam: δ = 2) |
| T3 | C12-P2/P3 (DIMOSTRATO, Lean) | τ² + bτ + c is reducible ⟺ b² − 4c is a square in K[ξ] | **new core cross-check for m = 2:** fit P, then test whether the discriminant polynomial is an approximate square (least-squares square root). It is more stable than root tracking for wave, beam, KG and telegraph. Phase 0b: implement next to `factorise` with tests, and compare |
| T4 | II-T2 (DIMOSTRATO, corrected form) | the companion-matrix projectors per factor give the components: (V_jB_j)(∂)u = r_j(∂_x)u_j | alternative component extractor per κ that works even at branch collisions; benchmark against the current assign-by-root |
| T5 | P2-T3, C12-P7, P2-C2 (DIMOSTRATO) | γ_N = inf σ(S*S\|(ker S)^⊥), ‖S†‖ = γ_N^{−1/2}; N = 2: γ = 1 − c_F; for N = 3 the pairwise c_F do not determine γ_3 | compute γ_N from the full block Gram matrix, never from pairwise c_F; error bars on components scale as γ_N^{−1/2}; Friedrichs-angle Bayesian layer (plan 0b.10) |
| T6 | P2-T4, P2-T1/T2 (DIMOSTRATO) | no regularisation, linear or not, beats Lip ≥ γ_N^{−1/2}; none removes E_int | γ_N^{−1/2}·σ is an **error floor**: no method is expected to beat it, and it is used as the stop criterion (in error units) |
| T7 | P2-T5 (DIMOSTRATO) | MCA / ℓ¹ separation of factors acts only on the finite gauge 𝓘 = intersection; the exact condition is a NSP on the gauge | **do not** use MCA, sparse or ℓ¹ component separation; the min-norm split on 𝓘 (already in the core) is exact and simpler. Bayesian: an equal-variance prior on 𝓘 gives the same mean |
| T8 | P2-P4 (DIMOSTRATO), R1-P9 | no stable linear encoder makes E_int → 0; the log-symbol (nonlinear) reads terms linearly | the grouping encoder = analytic features (branch/log-symbol coefficients, factor energy fractions); PCA/AE only on top of these, never on raw fields |
| T9 | P2-P6 (DIMOSTRATO) | reading the terms from the log-symbol is a Vandermonde inversion: ‖V⁻¹‖ ≥ h^{−d}/(⌊d/2⌋!⌈d/2⌉!) when the spectral points cluster at spacing h | use many **spread** κ (whole band, not a narrow one); report κ_Vand per factor next to the term coefficients; scaled/orthogonal monomials in the fit (already scaled). Small domains → Δκ = 2π/L larger, but fewer κ: trade-off measured in DOMAIN.md |
| T10 | P2-Q3 (**APERTO**) | conditioning of the Hankel/Prony step (our matrix pencil) is not covered by theory | an **empirical** study is needed in Phase 0b: pencil error vs SNR, T, spacing of λ, order; this is where ML can contribute |
| T11 | C12-C1 (FALSO), exact loss of 1 derivative | the factor split does not preserve H^m | components are one derivative rougher than u: the GP prior for the components (EPGP pass) must be one order smoother than the target; compare errors in H^{m−1} |
| T12 | OPA-T3(a–d), P1-P1(e) (FALSO as a continuous extension) | E^add is unbounded H^m → L²; E_int from approximate data is (C) | E_int and ρ only as **distributions over posterior samples** (Monte Carlo), never as point estimates with linearised error bars |
| T13 | C3-T4, C3-T2(c,d) (DIMOSTRATO); ATTACK-9 §3(A), (B) | ID-ker for u_t = a(∂_x)u needs distinct z_k and deg a ≤ n; EP data never give ID-ann; e^{−t}cos x fits any a with a(±1) = −1; ≥ 4 generic modes give full rank for Dirac 1+1 | identifiability = mode count per factor (≥ dx + 1 distinct κ, more points than unknowns): label ID-KER otherwise (implemented). The benchmark uses rich data; the note's example as written is ID-KER for diffusion |
| T14 | DM-δ-MINIMAX = VAR-Q19 (DIMOSTRATO, M > δ₀) | minimax rate Θ(ε^{1/3}) under noise | expected slope of coefficient error vs noise ≈ 1/3 in the worst case; check the empirical slope in the noise sweep |
| T15 | CONV-T5 (DIMOSTRATO) | the discrepancy rule picks the right order, but the threshold δ₀ cannot be estimated from data | do not set the fit tolerance from data alone: use the GP posterior σ̂ (Bayesian) and report the dependence; the degree (m, dx) gets a posterior, not a hard cut |
| T16 | CONV-T4 (DIMOSTRATO), DICT-B2 (DIMOSTRATO) | Lipschitz 2δ/ρ with margin σ₂ ≥ ρ; coefficient error ≤ 2η/√λ_min | report λ_min of the fit's design matrix and the margin σ₂ for every fit; the bound is vacuous when 2δ/ρ ≥ 1 (§9.5(c)), and this is flagged in the output |
| T17 | DICT-A-iii, DICT-N1(ii) (DIMOSTRATO); §0.5 | a fit is never certifiable from finite data | labels FIT-COMPATIBLE / MISFIT / ID-KER / UNDECIDED; never "identified" (implemented) |
| T18 | CONV-T3 (DIMOSTRATO) | Ann(·) is discontinuous everywhere | the discrete outputs (factor set, degree) get a posterior over discrete structures (hypothesis grouping D), not a continuous error bar |
| T19 | CONV-B1 (DIMOSTRATO) | boundary conditions are invisible to Ann(u) | the pipeline does not return BCs; FFT windowing/padding only reduces leakage and never "learns" the BC |
| T20 | CONV-D1 (DIMOSTRATO) | in 1+d, d ≥ 2, the ambiguity is infinite unless the factors are comaximal | v1 stays 1+1; any 2+1 extension must test comaximality first |
| T21 | CONV-T7 (proposition DIMOSTRATO) | chain error ≤ Σ_i (∏_{j>i} L_j) ε_i, only for steps 4 → 6 | an explicit error budget per run: ε_interp, ε_fit (residual), L_split = γ_N^{−1/2}; steps 1–3 (model, level, class) are outside the bound |
| T22 | P1-T2 = R5-T2 (DIMOSTRATO); P1-T3 | closed form of E_int for commuting terms; cost Θ(M2^N(L+1)²) | E_int via the closed Fourier form (implemented, O(N) per κ); the number of terms N inside a factor stays small |
| T23 | II-C1 = C3-T1(d) (DIMOSTRATO) | Ann(u) = (P) ⟺ u, ∂_tu, …, ∂_t^{k−1}u are ℂ[∂_x]-independent (P monic in τ) | the degree in τ (m) of the fitted P is the number of independent t-derivatives: a cheap posterior check on m via the rank of the pencil per κ |
| T24 | OPF5B-T6, C3-P1, P4-T5 (DIMOSTRATO) | no finite test for repeated socle; no finite certificate in M2; black-box impossibility | repeated factors (Q²) are out of scope for v1: if the pencil shows multiple roots (polynomial × exponential modes), output UNDECIDED with reason |

## 2. Consequences for the open design choices (Phase 0b)
- **Domain (0b.3):** T1 forces convex cells; T9 and T13 give the lower limit of cell size (enough distinct κ for the degree); T5 and T6 give the stop rule (γ_N^{−1/2}·σ̂ below the target error).
- **Grouping (0b.4):** T7 rules out ℓ¹/MCA separation; T8 fixes the encoder to analytic features; T18 motivates hypothesis grouping (D) for the discrete outputs.
- **Bayesian layer (0b.8, 0b.10):** T5, T6 and T7 fix the Gaussian split model and its prior on the gauge; T12 and T18 force Monte Carlo; T15 forces σ to be a posterior quantity.
- **Core improvements to test (core change only with tests):** T2 (δ check), T3 (discriminant square for m = 2), T4 (companion projectors), T23 (rank check on m), T24 (repeated roots → UNDECIDED).
- **Where ML can add something the theory does not give:** T10 (Prony/Hankel conditioning, open), T14/T15 (noise threshold in practice), domain scale selection.

## 3. Checks run against the current core (2026-10-28)
- T2 on exact data: wave, beam and transport+diffusion give `n_shared = 0` and 0 branch collisions in the band. This is consistent: their varieties meet only at κ = 0 (and, for transport × diffusion, at the complex point κ = i/D), and the synthetic data carry no κ = 0 mode. **Gap:** the shared-mode (gauge) path of the core is not exercised by any test. To do in Phase 0b: a case with a κ = 0 component (constant or affine in t), so that δ(P) > 0 is visible and the min-norm split is tested against C12-T2.

## 4. Phase 1 v2 results (2026-10-28)
- **T14/T15 (CONV-T5).** No data-free threshold, so the fixed `ftol` was replaced by Bayesian model comparison over factor structures (`core/structfit.py`). KG and telegraph now stay irreducible up to noise 1e-1 (E1c).
- **T2 (C12-T2).** The gap of §3 is closed: case `tpd_shared_kappa0` has the κ = 0 mode λ = 0 on both varieties. Core v2 reports `n_shared ≥ 1` on exact data, and the factors are unchanged (test_core_v2).
- **T24 (OPF5B-T6).** A repeated factor (τ+ξ)² now gives UNDECIDED through the confluent (A+Bt)e^{λt} test (BIC per bin), exact and at 1e-3. Side effect: at noise 1e-1, beam (two close branches that cannot be resolved) is also labelled UNDECIDED. This is consistent with "no finite test": unresolved and repeated cannot be told apart.
- **T3 (C12-P2).** The discriminant-square test is exact-only (E4). It is kept as a feature, not as a decision.
- **T10 (P2-Q3, open).** Per-bin pencil order by BIC fixes the merged-exponential outliers of transport+diffusion. The right factor set at 1e-2 noise went from 0.7 to 1.0 (E1b → E1c).
