# S-AGG-CLUSTER — REPORT (2026-10-28)

Nothing is committed (per the task rules, the main session commits). No package was installed into `.venv`: scikit-learn 1.9.1, scipy 1.18.1 and numpy 2.5.4 were already there.

## What was built
Files: `src/pdefactor/aggregate.py`, `src/pdefactor/cluster.py`, `tests/test_aggregate_cluster.py` (11 tests). Experiment scripts: `analysis/exp/agg_probe.py`, `agg_check.py`, `agg_two_regime.py`. Raw outputs: `analysis/exp/out/agg_*.txt`.

**`aggregate.py`**: from [(StructResult, π_s)] to the note's 𝒲 and its statistics.
- `fake_posterior` provides the S-INTERP stand-in (the exact grid plus independent noise draws, π_s = 1/S). `run_core` calls core v2 per sample as a black box; a `core=` hook accepts another analyser.
- `factor_vector` encodes each factor's monic coefficients, zero-padded to (m ≤ 2, dx ≤ 4). Equivalent structures, such as (1,2) with c₂ = 0 and (1,1), give the same vector. So the structure posterior's split over dx does not split the cloud.
- **Alignment.** Tracks are the DP clusters: matching by coefficient distance, only within equal τ-degree m (II-C1), distinct within a sample (Hungarian on −log responsibility). The no-DP path `align` matches by Hungarian to a reference sample.
- Per-track quantities: W_j, θ̄_j and Σ_j; k_eff = exp(H(W)) and the note's k_det = ⌈k_eff⌉.
- **Distributions over samples (`Dist`: mean and quantiles, Monte Carlo only)** of k_eff, ρ, c_F and γ_N. ρ uses the closed Fourier form of E_int (`core.components.eint_ratio`, called, not edited).
- Co-occurrence matrices; the structure posterior pooled over samples, and pooled by k.
- **DP posterior over k.** A variational DP mixture (sklearn `BayesianGaussianMixture`, stick-breaking) is fitted per m on the observed factors plus tokens drawn ∝ π_s w_j, with one isotropic scale. γ₀ is chosen by the ELBO on a grid (empirical Bayes). Over-split clusters are merged by a BIC test (below). P(k) is Monte Carlo: s ~ π, a label per factor ~ responsibilities, k = number of distinct labels.
- `finite_k_posterior` (BIC over finite GMMs) is reported next to the DP count. The DP count is not a consistent estimator of k (Miller & Harrison 2013).

**`cluster.py`**: domain grouping on rectangles.
- `rectangles`, `adjacency` (shared edge), `connected_split`, and `has_hole` (CLAUDE.md rule 6 / C12-T1′: a group must not enclose another).
- `exact_provider` feeds each rectangle the exact component(s) it overlaps, on a periodic x-grid over the rectangle's time span. This implements "exact components as input"; see "Failures" for why.
- **`window_features`.** The core runs on S fake posterior samples per window. Features are analytic only (P2-P4):
  - the mass of the window's factors on each **global** 𝒲 cluster;
  - the two largest energy fractions;
  - γ_N.

  Each is computed per posterior sample and π-averaged. The features' spread inside a window is the covariance floor (empirical Bayes). `encode` applies PCA on top, optionally.
- **`cluster_windows`.** Methods: GMM, k-means, spectral (affinity masked by adjacency), and agglomerative (ward, `connectivity=adjacency`).
  - GMM and k-means are initialised at the "pure factor" centres of the dominant 𝒲 clusters (the note's θ̄_j), and are followed by a connected-component split.
  - k is the MAP of the BIC posterior; `k="keff"` uses the note's ⌈k_eff⌉.
- `dominant_balance_labels`: the Callaham et al. (2021) baseline. A GMM on log|u_t|, log|u_x|, log|u_xx| per point, then a majority vote per rectangle.

## Results against the done criterion
| criterion | result |
|---|---|
| ARI ≥ 0.9 on transport (x < π) \| heat (x > π), exact components as input | **met.** ARI = 1.0 for GMM, k-means, spectral and agglomerative, on the 2×8 and 2×6 window layouts (windows aligned with x = π), at 1e-2 noise and S = 6. No group has a hole. Test: 2×6. |
| DP posterior: most mass on k = 2 for `transport_plus_diffusion` | **met.** P(k = 2) = 1.0 at noise 1e-3 and 1e-2 (S = 8). The finite-BIC posterior also gives k = 2 (p = 1.0). W = (0.768, 0.232) against the true weights; k_eff = 1.72, so ⌈k_eff⌉ = 2. |
| DP posterior: most mass on k = 1 for `heat` | **met.** P(k = 1) = 1.0 at 1e-3 and 1e-2; k_eff = 1.000, so ⌈k_eff⌉ = 1, after the merge step (below). |
| pytest green | **met.** `tests/test_aggregate_cluster.py`: 11 passed (≈ 100 s). |

Other measured values (TPD, 1e-3 noise, S = 8):
- γ̄_N = 0.174, and c̄_F = 0.826 = 1 − γ̄ (T5, N = 2);
- ρ̄ = 0.002, rising to 0.029 at 1e-2 (the factors are single-term; ρ > 0 comes only from noise-level spurious terms);
- pooled P(k) from the structure posteriors: 0.994 on k = 2.

Two-regime numbers (`analysis/exp/out/agg_two_regime.txt`, noise 1e-2, S = 6):

| layout | k (BIC MAP) | GMM | k-means | spectral | agglomerative | dominant balance | global k_eff (⌈·⌉) |
|---|---|---|---|---|---|---|---|
| 2×8 (aligned) | 2 | 1.0 | 1.0 | 1.0 | 1.0 | 0.35 | 2.00 (2) |
| 2×6 (aligned) | 2 | 1.0 | 1.0 | 1.0 | 1.0 | 0.20 | 2.14 (3) |
| 2×5 (one window straddles π) | 3 | 1.0 | 0.63 | 0.63 | 0.63 | −0.05 | 2.47 (3) |

## What went wrong on the way, and the fixes (each one is a finding)
1. **Ungated Hungarian alignment merges different laws.** Transport and heat are both m = 1. Matching to a reference with no distance gate put them in one track, so the domain k_eff came out as 1.00. Fix: tracks = DP clusters. Any hand-set gate would have broken rule 4.
2. **Resampled tokens create fake evidence.** 50 duplicates per sample made the DP split heat into 6 clusters (k_eff = 5.7). Fix: every factor once, plus n draws ∝ mass.
3. **Per-dimension standardisation inflates negligible coefficients.** A ξ³ coefficient of 1e-4 in some samples and exactly 0 in others became a bimodal unit-scale dimension. Fix: one isotropic scale.
4. **The DP still over-splits on 8 points** (heat at 1e-2: one singleton, k_eff = 1.46, ⌈k_eff⌉ = 2), whatever γ₀ the ELBO picks; the ELBO picks the smallest, 1e-3. This is the Miller–Harrison effect. Fix: `merge_clusters`. Clusters that never co-occur in a sample are merged when BIC prefers one mean over two, with a **full** shared covariance. A diagonal covariance does not merge them (ΔBIC = 9.45 against a penalty of 8.32), because fitted coefficients are strongly correlated: corr(c₀, c₂) = 0.97. The full-covariance test merges with a small margin: 7.96 against 8.32. **The margin is thin**: with S = 8 this test sits near its threshold for heat at 1e-2. More posterior samples, or the GP's own covariance of the coefficients, would make it robust.
5. **The structure posterior over k is a poor window feature.** Heat windows give P(k = 1) = 0.72 on t ∈ [0, 1] but 0.44 on t ∈ [1, 2]. The mass is split between (1,2) and (1,0)+(1,2) with a negligible constant factor. With that feature, every method split the heat region into two t-groups (ARI 0.73). It is now off by default (`with_pk=True`). The coefficient cloud is the stable carrier of the factor identity, while the structure posterior is not.
6. **The note's ⌈k_eff⌉ is fragile.** On the 2×6 domain cloud, 1.4 % of the mass sits on spurious factors from one noisy heat window (τ + 0.30, and a τ² factor). This gives k_eff = 2.14, so ⌈k_eff⌉ = 3, while the true number of laws is 2. The BIC posterior over groups gives 2 (p = 1.0). With ⌈k_eff⌉ as k, k-means / spectral / agglomerative drop to ARI 0.85 / 0.72 / 0.85 on that layout. **Recommendation:** use the posterior over k (BIC/Laplace, or the DP count), not ⌈k_eff⌉. This answers part of the note's "proposal to be criticised" (Step 4).

## Failures and limits, stated plainly
- **Non-periodic windows do not work with the current core.** On x ∈ [0, π/2] with a Tukey window, core v2 finds 426 spurious modes, takes 100 s, and returns a wrong structure. This is DOMAIN.md E3, and P2-Q3 is open. So the ARI criterion is met **only with exact components as input** (the plan's wording): each rectangle gets the true local law on a periodic grid. Real domain grouping needs S-DOMAIN's extractor through the `core=` hook (adapter: return a StructResult-like object).
- **Straddling windows.** On the 2×5 layout, the window [4π/5, 6π/5) straddles x = π; the provider gives the overlap-weighted sum. The BIC k is 3, because the mixed windows form their own group. GMM, initialised from 𝒲, still gives ARI 1.0. k-means, spectral and agglomerative give 0.63, because they keep the mixed windows as a third group. Global k_eff = 2.47 (`agg_two_regime.txt`). Ground truth by majority overlap is ill-defined there (the overlap is exactly 50 %), so a third "mixed" group is a defensible answer. Not a done criterion; reported.
- **Dominant balance (baseline)** fails on this field. ARI = 0.35 (2×8), 0.20 (2×6), −0.05 (2×5). The glued field has the same term magnitudes on both sides up to amplitude, so local |u_t|, |u_x|, |u_xx| do not separate transport from diffusion; they would on a dominant-balance problem. This is evidence for the factor-coefficient features (P2-P4), not a fair benchmark of Callaham's method on its own problems.
- **Runtime.** TPD with S = 8: 25–95 s per aggregate (the core takes 3–10 s per sample, and other sessions share the CPU). Heat: 2–5 s. The ELBO grid fits the DP 5 times per m block.
- **`finite_k` on the domain cloud** picks k = 4 on 2×6 and 2×5. BIC counts unique points without mass weights, so a 1 % spurious factor is a full cluster. On per-field clouds (TPD, heat) it agrees with the DP. Use it as a check, not as the group count.
- **DP concentration γ₀.** The ELBO always picks the smallest grid value, 1e-3. The grid edge is binding, so the ELBO-optimal γ₀ may be smaller still; it is reported in `DPResult.concentration`.

## Proposed rows for `analysis/THEORY_TO_ALGO.md` (main session; this session may not edit it)
| # | result (status) | what it says | decision |
|---|---|---|---|
| T25 | Miller–Harrison 2013/2014 (external, CON-FONTE: NeurIPS 2013, JMLR 2014) | the DPM posterior on the number of clusters does not concentrate on the true k | the DP count of 𝒲 clusters is checked by a finite-mixture BIC test (merge step) and reported next to `finite_k`; never use the number of non-empty sticks |
| T26 | no theory: empirical (S-AGG-CLUSTER) | the structure posterior splits mass between equivalent dx and spurious extra factors (heat: P(k=2) up to 0.49) | the factor identity is read from the zero-padded coefficient cloud, not from structure labels; the structure posterior is reported, not used as a grouping feature |
| T27 | no theory: empirical | ⌈k_eff⌉ moves by 1 with ~1 % spurious mass | the number of groups = MAP of a posterior over k, not ⌈k_eff⌉ |

## Open questions
- **A coefficient covariance per factor from the core** (Cramér–Rao on the branch fit) would give the merge test and the DP a principled within-factor covariance, instead of estimating it from S = 8 samples. This would be a core change (rule 3), requested from the main session.
- Should ρ be defined on the whole field (E_int of û_s) or as a weight-averaged per-factor ρ_j, as here? The note writes ‖E_int(û_s)‖/‖û_s − u₀‖. The per-factor form is the only one computable from the core's outputs.
- The 2-D window layout (splits in t as well as in x) is supported and hole-checked. Only x-regimes were tested.

## Changes requested in other packages
- **Main / core:** an optional coefficient covariance per factor (see above). A `FactorResult.rho` for core v2 factors (it is 0 by default; I compute it in `aggregate.factor_rho`).
- **S-DOMAIN:** an adapter `analyze_cell(u, t, x, noise, want_components) -> StructResult-like`, to plug into `run_core(core=...)` / `window_features(core=...)`.
- **Main:** merge `sessions/S-AGG-CLUSTER/RESEARCH.md` into the root `RESEARCH.md`, and add T25–T27.
