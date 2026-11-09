# S-AGG-CLUSTER — PLAN (2026-10-28)

Session: **S-AGG-CLUSTER** (Phase 2). Owns `src/pdefactor/aggregate.py`, `src/pdefactor/cluster.py`, `tests/test_aggregate_cluster.py`, `analysis/exp/agg_*`. Implements plan §Phase 2 "S-AGG-CLUSTER" and v2.3 (grouping A inside the core, D = posterior over structures, B = domain). The core (`analyze_structured`) is a black box.

## Goal and done criterion
- 𝒲, k_eff, ρ̄, c̄_F, γ_N (as distributions over posterior samples), a co-occurrence matrix, a DP posterior over k, and pooled structure posteriors.
- Domain grouping per rectangular window, with analytic features, GMM / k-means / spectral initialised from 𝒲 under a connectivity constraint, and dominant balance as the baseline.
- Done:
  - ARI ≥ 0.9 on transport (x < π) | heat (x > π) with exact components as input;
  - the DP posterior puts most mass on k = 2 for `transport_plus_diffusion` and k = 1 for `heat`;
  - pytest is green;
  - REPORT.md.

## Probe findings that shape the design (`analysis/exp/agg_probe.py`)
- Core v2 on whole periodic cells (48×64): 0.3 s (heat, transport) to 2–4 s (TPD). Factors are right at 0 and 1e-2 noise. The structure posterior splits mass between equivalent dx (heat: (1,2) p = 0.59, (1,3), (1,4)…), because a padded coefficient of ≈ 0 is allowed.
  → Factors are matched by **coefficients**, not by structure label. The structure posterior is also pooled by k (number of factors), which is invariant to that split.
- Non-periodic windows (x ∈ [0, π/2], Tukey): 426 spurious modes, 100 s, wrong structure. This is DOMAIN.md E3 (P2-Q3, open).
  → `cluster.py` takes the per-window input from a **provider** `field_on(rect)`. The test uses the exact component(s) active in the rectangle, evaluated on a periodic x-grid over the rectangle's time span ("exact components as input", plan §Phase 2). S-DOMAIN's extractor will plug into the same provider.

## API
`aggregate.py`
- `Sample(result: StructResult, pi: float, t, x)` — input. `fake_posterior(u, t, x, sigma, S, rng)` returns S noisy copies with π_s = 1/S, for testing without S-INTERP.
- `run_core(samples_u, t, x, sigma, pis, **core_kw) -> list[(StructResult, π_s)]` — black-box call per sample (want_components=True, for ρ).
- `factor_vector(PolySymbol, m_max, dx_max) -> real vector` — padded Re/Im coefficients, plus m.
- `align(results) -> track ids per (s, j)` — Hungarian matching to a reference, only within equal m (structure-aware); unmatched factors open new tracks.
- `Cloud` dataclass: `theta (n, d)`, `w`, `pi`, `sample`, `track`, `m`, `sympy`, `terms`.
- `aggregate(results_pis) -> Aggregate` with:
  - `cloud`;
  - `W_track`, `theta_bar`, `Sigma` per track;
  - `k_eff` (pooled, from the note), `k_det = ceil(k_eff)`;
  - per-sample distributions (value, π) of k_eff_s, ρ_s, c_F, γ_N;
  - `cooccurrence (n_track × n_track)`;
  - `structures_pooled` {structure: p}, `k_structure` {k: p};
  - `dp`: `DPResult(p_k, labels, weights, model)`;
  - `finite_k`: BIC posterior over k for finite GMMs (Miller–Harrison caveat).
- `dp_posterior_k(cloud, ...)` — variational DP mixture on mass-resampled tokens; P(k) by Monte Carlo over samples s ~ π and labels ~ responsibilities.

`cluster.py`
- `rectangles(T, L, nt_win, nx_win)` — grid of rectangles; `adjacency(rects)` — rectangles sharing an edge.
- `window_features(rects, field_on, sigma, S, core_kw) -> (F, per-window Aggregate, global Aggregate)`. Each window is aggregated over its own fake posterior samples. The global 𝒲 is the union of the window clouds (π ∝ area). Feature of a window:
  - mass on each global DP cluster (soft assignment of its factors × w × π);
  - P(k | window);
  - sorted energy fractions;
  - γ_N mean.
- `cluster_windows(F, adj, method in {gmm, kmeans, spectral, agglomerative}, k=None, init_from=global aggregate)`:
  - k: the posterior mode of the GMM-BIC over 1..K by default, with ⌈k_eff⌉ kept as a comparison;
  - k-means / GMM centres are initialised at the one-hot dominant 𝒲 clusters;
  - connectivity: spectral uses an affinity masked by the adjacency; agglomerative uses `connectivity=adj`; GMM / k-means are post-processed by splitting each label into connected components (union of adjacent rectangles).
- `dominant_balance_labels(u, t, x, rects, k)` — Callaham et al. 2021 baseline: GMM on log|u_t|, log|u_x|, log|u_xx| per point, with a majority vote per window.

## Choices and their theory
| choice | motivation (THEORY_TO_ALGO row, status) |
|---|---|
| ρ, c_F, γ_N, k_eff only as distributions over samples (Monte Carlo) | T12 (OPA-T3, P1-P1(e)), T18 (CONV-T3) |
| γ_N from the core's full block Gram (`res.gamma`), not from pairwise c_F | T5 (P2-T3, P2-C2) |
| ρ_j from the closed Fourier form of E_int (`core.components.eint_ratio`, called, not edited), with u0_hat from the FFT of the component at t₀; ρ_s = Σ_j w_j ρ_j | T22 (P1-T2), note §Step 3 |
| posterior over structures pooled over samples; pooled by k as well | T18 (CONV-T3), GROUPING D |
| encoder = analytic features only (coefficients, energy fractions, γ_N, structure posterior); PCA on top only | T8 (P2-P4, DIMOSTRATO) |
| no ℓ¹/MCA separation anywhere | T7 (P2-T5) |
| windows are rectangles; groups = unions of edge-adjacent rectangles (connectivity constraint) | T1 (C12-T1′); DOMAIN.md decision 1. A union of adjacent rectangles in a 1-D x-strip layout is a rectangle, so simple connectivity holds. In a 2-D layout a union can enclose a hole: this is checked (Euler characteristic of the union) and reported, not hidden |
| factor matching by coefficient distance within equal m | no theory: empirical (label switching, Stephens 2000); m is the τ-degree, an invariant of the factor (II-C1, T23) |
| variational DP mixture for P(k); finite-GMM BIC posterior next to it | no theory in ProblemaBase; Miller–Harrison 2013 (DPM inconsistent for k) |
| deterministic k = ⌈k_eff⌉ kept for comparison | note §Step 4 (a proposal, not a theorem) |
| dominant balance as a baseline | no theory: empirical (Callaham 2021) |

## Parameters and how they are set (rule 4)
- DP concentration γ₀: an uninformative Gamma-free choice is not offered by sklearn, so γ₀ = 1/K_trunc (sklearn default) is used, with sensitivity reported for γ₀ ∈ {0.01, 1, 10}. **This is a hand-set prior, reported as such.**
- Covariance floor `reg_covar`: estimated from the within-track spread of the aligned cloud (empirical Bayes; a floor of 1e-6 in standardised units on exact data).
- Number of resampled tokens for the DP fit: 50 per sample. This is a Monte-Carlo size, not a model parameter; P(k) is checked to be stable under doubling it.
- Number of domain groups: the BIC posterior over k (finite GMM), with ⌈k_eff⌉ for comparison. No fixed k.
- Fake-posterior noise σ and S: test inputs only (σ = 1e-3·std, S = 8).

## Tests first (`tests/test_aggregate_cluster.py`)
1. `factor_vector` round trip and padding invariance: (1,2) with c₂ = 0 equals (1,1).
2. Alignment: shuffled factor order across samples → same tracks.
3. TPD fake posterior: two tracks, W ≈ (0.77, 0.23) within 0.05; k_eff ∈ (1.5, 2); k_det = 2; DP P(k = 2) > 0.5 and the argmax is 2; co-occurrence of the two tracks ≈ 1.
4. Heat: DP P(k = 1) > 0.5, argmax 1; k_det = 1.
5. Distributions: γ_N for TPD ≈ 0.17; c̄_F = 1 − γ̄ (N = 2, T5); ρ̄ = 0 for single-term factors.
6. Two-regime field: ARI ≥ 0.9 for GMM, k-means, spectral and agglomerative; dominant balance ARI reported (no threshold).
7. Rectangles and adjacency: every group is edge-connected.

## Amendments during the work (added; the text above is kept)
- **Tracks = DP clusters** when the DP is fitted. The ungated Hungarian alignment merged transport and heat (both m = 1) into one track on the domain cloud (global k_eff = 1). Hungarian-to-reference (`align`) stays as the no-DP path and is tested for order invariance.
- **DP tokens.** Instead of 50 resampled tokens per sample: every observed factor once, plus n draws ∝ π_s w_j. Many duplicated tokens produced fake evidence, and heat split into 6 clusters.
- **DP scaling.** One isotropic scale (the RMS norm of the cloud) instead of per-dimension standardisation, which turned 1e-4 coefficients into unit-size bimodal dimensions.
- **DP concentration γ₀** is chosen by the ELBO over {1e-3, 1e-2, 0.1, 1, 10} (empirical Bayes), not hand-set.
- **Merge step** after the DP (`merge_clusters`). Clusters that never co-occur in a sample are merged when BIC prefers one mean over two, with a full shared covariance (fitted coefficients have corr ≈ 0.97). This addresses DPM over-splitting (Miller–Harrison).
- **Window features.** The structure-posterior P(k) is off by default (`with_pk=True` restores it). The covariance floor for window clustering is the features' posterior spread inside windows (empirical Bayes).
- **Number of domain groups** = MAP of the BIC posterior. ⌈k_eff⌉ is reported for comparison and is fragile (see REPORT).
