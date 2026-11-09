# Analytical limits → effect on the pipeline → mitigation

| Limit (theory ID) | Concrete effect seen or expected | Mitigation / forced label |
|---|---|---|
| No data-free threshold for the noise level (CONV-T5) | a fixed `ftol` falsely factors KG and telegraph at 1e-4 noise (E1) | Bayesian model comparison over factor structures (structfit). The threshold becomes a posterior quantity |
| Fit never certifiable from finite data (DICT-A-iii) | even a posterior weight of 0.98 is relative to the structure class | output FIT-COMPATIBLE plus posterior weights over structures; never "identified" |
| Error floor γ_N^{-1/2}σ for any selection rule (P2-T4) | E2: γ_N ∝ T², L² on small cells; γ ≈ 5e-4 on T = 0.1 means a 45× amplification | error bars from γ_N. Cells too small for the γ floor are not split further |
| Split false on non-simply-connected Ω (C12-P10, OPF-T4) | an annular region of one regime | cover groups with rectangles only (CLAUDE.md rule 6) |
| Prony/Hankel conditioning open (P2-Q3) | E1: TPD outliers (an unresolved diffusion exponential merged into a transport one). E3: the multi-channel 2-D pencil on non-periodic cells fails even on exact wave data, and fails on sub-windows at 1e-3 noise | robust likelihood. Per-bin order selection. Non-periodic cells need a dedicated extractor (Phase 2 session S-DOMAIN); until then, cells are periodic or FFT-windowed |
| Repeated roots (OPF5B-T6) | E4: (τ+ξ)² is reported as a confident simple factor τ+ξ | confluent model (A+Bt)e^{λt} in the comparison → UNDECIDED |
| Shared modes / δ(P) > 0 (C12-T1, T2) | E4: κ = 0 constant shared by both factors; the noisy core merges the factors | structfit handles it. The split of the shared part follows the prior; the min-norm choice equals the posterior mean (0b.10) |
| E_int not continuous (OPA-T3, P1-P1(e)) | pointwise error propagation is meaningless | Monte Carlo over interpolants only |
| Single-exponential data (0b.6, ATTACK-9) | one mode per factor fits infinitely many laws | ID-KER relative to the class, or UNDECIDED; benchmarks use many modes |
| Loss of one derivative (C12-C1) | component estimates are rougher than u | GP prior one order smoother for components |
| No linear encoder suffices (P2-P4) | PCA on raw fields cannot group | encoder on analytic features |
| Real fields, complex model | E5: coverage 0.65–0.85 at nominal 0.90 | conjugate-pair (real) parametrisation in bayes_split |

## Non-monic symbols (added 2026-10-29, graph audit)
- **Limit:** identifiability Ann(u) = (P) is proven only for P monic in τ (II-C1 = C3-T1(d), DIMOSTRATO). For constant-coefficient laws whose leading τ-coefficient depends on ξ, e.g. the linear BBM / pseudo-parabolic u_t − u_xxt − u_xx = 0 with symbol (1+ξ²)τ − ξ², the branch λ(κ) = −κ²/(1+κ²) is rational, not polynomial. The ledger has no criterion for this class (OPF5B-T2 is the variable-coefficient saturated form; EX-Q1, non-monic in ∂_t, is APERTO).
- **Effect on the pipeline:** the core fits factors monic in τ (`variety.fit_monic`), so such a law cannot be represented. It should come out MISFIT, or as a high-dx polynomial approximation of λ(κ) on the observed band. That approximation is not the law.
- **Mitigation:** none yet. Flag as out of scope, like variable coefficients, until a theory row exists. A candidate extension (fit c(ξ)τ − a(ξ), i.e. a rational branch) needs a proven identifiability statement first (theory first, rule 7).
