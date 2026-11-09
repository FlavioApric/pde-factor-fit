# RESEARCH — survey and verdicts

Every session appends a section `## <ID> — <date>` (see the `session-start` skill). Verdicts: **adopt** (use as is), **adapt** (copy and modify the idea or code), **baseline** (compare against it), **ignore**.

## Main session — 2026-10-28 (Phase 0)

### Whole pipeline
No public repository does "data → factors of the symbol → components → grouping → recursion". The pipeline is new; its parts are not.

### Step 1: interpolation with probabilities
| item | verdict | reason |
|---|---|---|
| GPyTorch (cornellius-gp/gpytorch) | adopt | GPU exact GP up to ~10⁴ points, SKI/KISS-GP beyond that; posterior samples on a grid. Fits the T2000 4 GB. |
| NumPyro / PyMC (HMC/NUTS) | adopt | marginalise GP hyperparameters when n is small; DP mixtures; hierarchical priors (plan 0b.8). |
| EPGP (haerski/EPGP; Härkönen, Lange-Hegermann, Raiță, ICML 2023) | adapt | GP priors supported on the Ehrenpreis–Palamodov variety, i.e. on solutions of a given P. One GP per factor is exactly the refinement pass (step 6 → step 1). |
| Deep ensembles / SIREN | baseline/ablation | uncertainty is less calibrated than a GP; kept as the S-INTERP ablation. |

### Step 2: analytic core
| item | verdict | reason |
|---|---|---|
| Matrix pencil (Hua–Sarkar 1990) | adopt (implemented) | exponential fit in t per wavenumber, giving points of the dispersion variety. |
| SymPy `factor_list` | adopt for exact symbols only | it fails on float coefficients, so numerical factorisation is our own root-tracking test (`core/variety.py`). |
| GPCA (Vidal–Ma–Sastry 2005) | adapt (idea) | fit one polynomial on a union of varieties and segment by factor. This is the same structure as our fit-P / factor / assign. |
| He–Zhao–Zhong, "How much can one learn a PDE from its solution?" | adopt (check) | identifiability needs enough Fourier modes (≥ n+1 for degree n). Used in the ID-KER label. |
| BOP-DMD (PyDMD; Askham–Kutz 2018) | baseline | gives eigenvalues λ with uncertainty; no factor structure. |

### Step 4: grouping and clustering
| item | verdict | reason |
|---|---|---|
| scikit-learn GMM / BayesianGaussianMixture (DP prior) / Spectral | adopt | the posterior over k comes from the DP prior; the note's deterministic k = ⌈k_eff⌉ is kept as a comparison. |
| dominant-balance (Callaham et al., Nat. Commun. 2021) | adapt/baseline | GMM on local term magnitudes; domain grouping (type B). |
| Tetali et al., wave-informed matrix factorisation | ignore (no code) | closest idea, but there is no implementation. |

### Baselines for the whole equation
| item | verdict | reason |
|---|---|---|
| PySINDy (dynamicslab/pysindy): WeakPDELibrary, EnsembleOptimizer, SBR | baseline | standard sparse regression; no factor or component decomposition. |
| DeePyMoD, EPDE, PySR | optional baseline | heavier (EPDE: evolutionary; PySR needs Julia). Only if time allows. |

### Phase 4 (trainable)
| item | verdict | reason |
|---|---|---|
| sbi (sbi-dev/sbi) | adopt later | neural posterior estimation, amortised, validated by SBC against the Bayesian layer. |

### Suggested by the user, judged
| item | verdict | reason |
|---|---|---|
| K-Dense-AI/scientific-agent-skills | adopt (14 skills) | scikit-learn, pymc, sympy, pytorch-lightning, statsmodels, matplotlib, scientific-visualization, exploratory-data-analysis, uncertainty-and-units, experimental-design, scientific-critical-thinking, hypothesis-generation, literature-review, statistical-analysis. |
| Yuuqq/research-grade-skills | ignore | trimmed fork of K-Dense; nothing extra. |
| lonexreb/claude-code-math-skills | adopt (formal-math-ai) | analysis and proof checking. |
| sympy | adopt | symbols, exact catalogue. |
| OpenDCAI/DataFlex | ignore | LLM data scheduling; not related. |
| ultralytics/yolov5 | ignore | image object detector, AGPL; not related. |
| ARIS skills (ProblemaBase/_vendor) | adopt (9) | experiment-plan, ablation-planner, run-experiment, analyze-results, result-to-claim, experiment-audit, novelty-check, research-lit, kill-argument. The reviewer backend (Codex MCP) is not installed, so a fresh Claude subagent is the reviewer. |

### Findings from the core build (Phase 1)
- The matrix pencil must use `V = Vh[:order].T` (no conjugation); otherwise every λ is conjugated and transport comes out as τ − ξ.
- Exact data need a round-off floor, otherwise ~10³ spurious modes appear.
- Real data with a complex factor also carry the conjugate factor. Example: real Schrödinger data give (τ − iDξ²)(τ + iDξ²) = beam. This is mathematics, not a bug.

## S-AGG-CLUSTER — 2026-10-28 (merged from sessions/S-AGG-CLUSTER/RESEARCH.md)

Fresh search for the aggregation (𝒲, posterior on k) and domain-grouping steps. Verdicts: adopt / adapt / baseline / ignore. This file is the session's addition to the root `RESEARCH.md`, which the main session merges.

| item | verdict | reason |
|---|---|---|
| scikit-learn 1.9 `BayesianGaussianMixture(weight_concentration_prior_type="dirichlet_process")` | adopt | Variational truncated stick-breaking DP. Already in `.venv` (sklearn 1.9.1), so nothing was installed. Gives the variational Beta posteriors of the sticks and the per-point responsibilities, which is enough to Monte-Carlo a posterior on the number of occupied clusters. |
| Miller & Harrison, "A simple example of Dirichlet process mixture inconsistency for the number of components" (NeurIPS 2013, arXiv:1301.2708); JMLR 2014 (Pitman–Yor generalisation) | adapt (as a caveat) | The DPM posterior on the number of clusters does not concentrate on the true k: it keeps spawning tiny clusters. Consequence here: (i) count only clusters that the cloud's *factor tokens* actually occupy within one interpolant sample, weighted by mass, not the number of non-empty sticks; (ii) report next to it a finite-mixture posterior on k (BIC/Laplace over GaussianMixture with k = 1..K), which is the consistent "mixture of finite mixtures"-style answer. Both go into the report. |
| Callaham, Koch, Brunton, Kutz, Brunton, "Learning dominant physical processes with data-driven balance models" (Nat. Commun. 12, 1016, 2021) | baseline | GMM on the local magnitudes of the equation's terms (finite-difference derivatives), then sparse PCA per cluster. The search found no maintained package; the method is short, so it is re-implemented in `cluster.dominant_balance_labels` (GMM on |∂_t u|, |∂_x u|, |∂_x² u| per point, aggregated to windows) as the comparison baseline. It needs a known term library; ours does not. |
| scikit-learn `AgglomerativeClustering(connectivity=...)`, `SpectralClustering(affinity="precomputed")` | adopt | Connectivity-constrained grouping of windows: the window adjacency graph (rectangles sharing an edge) restricts merges, so every group is a union of adjacent rectangles. Spectral clustering takes an affinity masked by the same graph. |
| Spatially constrained clustering / regime detection in PDE discovery (search 2024–2026) | ignore | Nothing newer that groups by factor structure. Closest is dominant balance (above) and DBSCAN on sparse-regression coefficients (arXiv:2604.00599), which clusters coefficient vectors, i.e. what 𝒲 already does without the per-node sparse regression. |
| Hungarian matching of factors across samples (`scipy.optimize.linear_sum_assignment`) | adopt | Structure-aware alignment: factors are matched only within the same order m in τ; cost = distance of the padded coefficient vectors. Label switching across posterior samples is the standard issue (Stephens 2000 relabelling); Hungarian to a reference is its simplest form. |

## S-BASELINES-BENCH — 2026-10-28 (merged from sessions/S-BASELINES-BENCH/RESEARCH.md)

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

## S-DOMAIN — 2026-10-28 (merged from sessions/S-DOMAIN/RESEARCH.md)

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

## S-INTERP — 2026-10-28 (Phase 2, interpolation with probabilities)

| item | verdict | reason |
|---|---|---|
| GPyTorch 1.15 + linear_operator 0.6 (installed) | adopt | exact GP on GPU up to n ≈ 5·10³ on the 4 GB T2000; `GridInterpolationKernel` (SKI/KISS-GP) beyond that. Separable kernel = `ProductKernel` of 1-D kernels on `active_dims`. |
| Laplace correction on the type-II ML hyperparameters + importance reweighting | adopt | McLeod–Simpson (GP-SBC) and Hadji–Szabó (ML-II credible sets can undercover) show that plug-in ML-II is overconfident. We draw θ_s from N(θ̂, H⁻¹) and reweight with p(y,θ_s)/q(θ_s), so that π_s corrects the Gaussian approximation. The ESS is reported. |
| NUTS on the hyperparameters (NumPyro 0.22, already installed) | adopt for small n | full marginalisation for n ≤ 300. Its weights are equal (π_s = 1/S). |
| Pathwise conditioning / Matheron's rule (Wilson et al. 2020, 2011.04026; BoTorch `MatheronPath`) | adapt later | it scales to many test points. On our grid (nt·nx ≈ 8·10³) the exact posterior Cholesky fits in memory, so the exact route stays the default. Matheron is the route if grids grow. |
| LOVE / `fast_pred_samples` (GPyTorch) | adopt on the SKI path | posterior samples on the grid when n is large. |
| EPGP (haerski/EPGP, MIT, 9★, notebook `demo.ipynb`; Härkönen–Lange-Hegermann–Raiță ICML 2023) and S-EPGP | adapt | we use the 1+1 specialisation. The features are e^{λ(κ)t+iκx} on the variety of each factor Q_j, with a Gaussian spectral measure in κ. A Bayesian linear regression gives a closed-form evidence and per-factor component posteriors. The code is re-implemented in numpy (no torch needed), because the repo is notebook-only. |
| B-EPGP (Jimmy000207/Boundary-EPGP) | ignore (v1) | it adds boundary conditions, which the pipeline does not use (CONV-B1, T19). |
| Spectral-mixture / GP-HM kernels (Fang et al., ICLR 2024) | baseline (later) | built for high-frequency PDE solutions. It is the remedy if the high-κ bias measured here matters. |
| Deep ensembles of SIREN (Sitzmann 2020; used as a UQ baseline in arXiv 2412.11350) | baseline/ablation | ensembles are known to be under-dispersed away from the data. Kept as the ablation in `interp/ensemble.py`, with coverage measured. |
| GP-SINDy (Meng–Qiu, arXiv 2401.11825, JCP 2025) | baseline idea | propagates the GP derivative variance into sparse regression. Our analogue is Monte Carlo over posterior samples (rule 4), not variance propagation. |
| Design-marginal calibration / LOO-coverage tuning (arXiv 2512.05611, Acharki et al.) | ignore (v1) | post-hoc recalibration. Used only if the Laplace/NUTS route fails the ±5 % coverage criterion. |

## S-LEARNED-V1 — 2026-10-29 (corpus I, V1 validator, L2b calibrated P(top))

Fresh search (GitHub, arXiv, library docs). Prior state: E14 (S-PHASE4-ML) failed both layers under LOFO on grids with a stand-in posterior.

| item | verdict | reason |
|---|---|---|
| Conformal outlier detection with a learned score (Bates, Candès, Lei, Romano, Sesia, Ann. Stat. 2023) | **adopt** | any score trained on separate data, conformalised on clean calibration runs, gives a false-alarm rate ≤ α exactly under exchangeability of the clean runs. This is the V1 gate statistic (detection on I at fixed false alarm on G/S). Already used for the OOD gate in `validator.py`. |
| Conformal evaluation of OOD scores; Mahalanobis beats the classical nonconformity score on OpenOOD and ADBench (Novello, Dalmau, Andeol, arXiv 2403.11532, 2024) | **baseline** | Mahalanobis with Ledoit–Wolf shrinkage stays as a score baseline; their conformal AUROC/FPR idea (finite-test variability) is adapted as a bootstrap CI on detection@FA. |
| ADBench (Han et al., NeurIPS 2022): no unsupervised detector dominates on tabular data | **baseline** | isolation forest (sklearn) = the unsupervised baseline the brief asks for; kNN distance as a second one. |
| Energy-based tabular OOD (arXiv 2608.14186, 2026; 2310.18677) | **ignore** | energy scores need a trained deep density/classifier on far more rows than ~1000 runs; the HGB margin plays the same role here. |
| Conformal inference for open-set classification (Xie et al., arXiv 2510.13037, 2025); OpenMax (Bendale–Boult 2016) | **adapt** | held-out failure types must end as "OOD / other", never a confident wrong type: report a type only when the classifier's top probability passes a conformal threshold fitted on seen types, else "other". The leave-one-type-out test is the open-set check. |
| Conformal risk control, multi-label (Angelopoulos et al. 2022) | **adopt (existing)** | the `Validator._risk_threshold` for the run-level failure-mode set; kept. |
| Venn–Abers (Vovk–Petej 2014; `venn-abers` on PyPI, v1.4) | **baseline** | E14's implementation is kept (no new dependency); the package is only a cross-check in a test. |
| Temperature / Platt scaling on logit P(top) (Guo et al. 2017) | **adopt (new arm)** | 1–2 parameters: the lowest-variance map, the only one likely to transfer across families with ~100 runs per fold. E14 tried only isotonic and Venn–Abers, both high-variance. |
| Isotonic regression (sklearn) | **baseline** | overfits small calibration sets (E14 confirmed out of family). |
| Beta calibration (Kull et al. 2017) | **ignore** | three parameters, no gain over Platt expected at n ≈ 100. |
| Adaptive (equal-mass) ECE + Brier with paired bootstrap; reliability diagrams | **adopt** | equal-width ECE is biased at small n; Brier is proper and is the primary score. |
| Residual whiteness: Ljung–Box/Box–Pierce portmanteau; Durbin–Watson; spectral flatness (Wiener entropy) | **adopt** | cheap, scale-free tests of the white-noise assumption of the likelihood (T50) on the per-κ-bin time residuals; target coloured noise, two laws, nonlinearity. No PDE-discovery paper found that tests residual whiteness (searched SINDy / weak-SINDy literature): this is standard time-series practice applied here. |
| Breusch–Pagan / White heteroscedasticity test (regress r² on |û|, t) | **adopt** | scale-free (R², n·R² ~ χ²) target for heteroscedastic noise. |
| Temporal Nyquist energy fraction (residual energy in the top temporal-frequency band of each κ bin) | **adopt** | aliasing leaves a residual concentrated near ±π/Δt; scale-free ratio. |
| Weak SINDy / ensemble SINDy misspecification discussion (Messenger–Bortz 2021; Fasel et al. 2022) | **ignore** | about derivative noise, not failure detection; no reusable detector. |

## S-LEARNED-LB — 2026-10-29 (budget/speed layer, `Learned(budget=True)`)

| item | verdict | reason |
|---|---|---|
| Conformal risk control (Angelopoulos, Bates, Fisch, Lei, Schuster; arXiv 2208.02814, ICLR 2024) | adopt | bounds E[loss] ≤ α for any bounded loss monotone in one threshold λ; the per-run loss "a skipped step would have changed the factor set or label" is monotone in the skip threshold. Already implemented in `learned/validator._risk_threshold` (rule (n R̂ + 1)/(n + 1) ≤ α); reused. Needs n ≥ 1/α − 1 = 49 calibration runs at α = 0.02. |
| Learn then Test (Angelopoulos, Bates, Candès, Jordan, Lei; arXiv 2110.01052) | adopt as the stricter variant | P(R(λ) ≤ α) ≥ 1 − δ via binomial-tail p-values and fixed-sequence testing over λ. With zero observed losses it needs n ≥ ln δ / ln(1 − α) = 114 runs at α = 0.02, δ = 0.1, so it is reported when the calibrate split is large enough and CRC is the default otherwise. ~20 lines of numpy; no new dependency. |
| CALM, Confident Adaptive Language Modeling (Schuster et al., NeurIPS 2022, arXiv 2207.07061) | adapt | the closest existing design: local early-exit decisions with a threshold calibrated by LTT against a *consistency* constraint with the full model's output (not against the truth). LB copies that: harm = disagreement with the off run, not error vs truth. |
| MAPIE `risk_control.BinaryClassificationController` (v1.x, LTT, Bonferroni/Holm) | baseline (test only) | same LTT machinery; not installed in the shared venv. Installed into LB's own venv only, used in one test to cross-check the in-house threshold; not a runtime dependency. |
| Hutter, Xu, Hoos, Leyton-Brown, "Algorithm runtime prediction: methods & evaluation" (AIJ 2014, arXiv 1211.0906) | adapt | empirical performance models; random forests best; timeouts are right-censored. LB's timeout predictor is a *binary* "reaches the cap" classifier, for which censoring at the cap is not a problem, so the Schmee–Hahn imputation is not needed. |
| Cascades / early-exit classifiers (BranchyNet, Teerapittayanon 2016; Viola–Jones cascades) | ignore as models, keep the idea | the idea (cheap features decide whether the expensive stage runs) is what LB does; the neural machinery does not fit 12 steps and a few hundred runs. |
| scikit-learn `HistGradientBoostingClassifier` (1.9.1, installed; monotonic_cst, native NaN) | adopt | one classifier per step; NaN-tolerant features; trains in seconds. Baselines: constant per-step skip rate, and L2 logistic regression. |
| scikit-survival / lifelines (censored runtime regression) | ignore (v1) | only needed for a runtime *regression*; the binary cap target avoids censoring. |
| Exact memoisation of repeated deterministic calls (functools-style, keyed by the call arguments inside one `run_loop` call) | adopt (deterministic companion) | zero harm by construction when the call is a pure function of its arguments; checked bit-for-bit by test. Candidates found by profiling (P0), not assumed. |
