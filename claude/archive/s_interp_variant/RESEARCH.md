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
