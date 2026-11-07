# PHASE 4 — optional learned layers: research, critical evaluation, plan

Session **S-PHASE4-PLAN** (2026-10-29). Planning and research only: no pipeline code. It extends plan §Phase 4 and §v2.12 (L1–L5) of `to-plan-use-the-groovy-chipmunk.md` and removes nothing from them.

Inputs read:
- `CLAUDE.md`, `analysis/THEORY_TO_ALGO.md` (T1–T50), `PARAMETERS.md`, `LIMITS.md`, `GROUPING.md`, `DOMAIN.md`, `RESEARCH.md`, `benchmarks/out/e2e_summary.md`;
- the code of `loop.py` (including the local session's uncommitted v2.12 work: `_refine_alternatives`, `coef_draws`, `split_quadratics(test=)`, the "T51" comment), `refine_raw.py`, `bayes_split.py`, `core/structfit.py`, `interp/gp.py`, `interp/epgp.py`, `synthetic.py`, `aggregate.py`, `bench_e2e.py`;
- the ProblemaBase LEDGER rows cited below (read-only).

The local session was not touched; this file was written in a separate git worktree.

Status words: **adopt / modify / reject / defer**. Theory IDs refer to THEORY_TO_ALGO / LEDGER. "(m)" after a reference means the arXiv id was quoted from memory by the research pass and not opened; check it before citing it in a paper.

---

## 0. Summary

| layer | user item | verdict | one-line reason |
|---|---|---|---|
| **P0** oracle information study + scoring + simulator extension | — (new, prerequisite) | **adopt, first** | Without it, a layer that "fixes" 400 pts @ 5 % may only be importing its training prior. The current amplitude law makes κ ≥ 5 undetectable whatever the method. |
| **L0** learned seeds for the per-bin exponential fit | — (new) | **adopt** (as a proposal) | It is the one place the theory itself leaves to ML (T10 / P2-Q3 open). Trained on generic exponential sums, so it is PDE-agnostic and does not need to extrapolate across families. |
| **L1** high-κ correction after the GP | 1 | **modify**: L1a deterministic first, L1b learned proposal only if P0 shows information that L1a misses | A corrector that reads the GP and "outputs missing parts" can only undo a known linear filter (no learning needed) or hallucinate. The information is in the raw data (T44), and the stationary t-kernel is the wrong prior for e^{−Dκ²t}. |
| **L2** learned calibration of method constants and intervals | 2 | **modify**: fewer degrees of freedom; thresholds from decision theory; monotone recalibration plus conformal | About 60 constants, ~30–50 affordable BO evaluations and 10 cases: tuning them all overfits. Calibrating the *probabilities* lets the thresholds follow from a loss. |
| **V** validator (diagnosis) | 3 | **modify**: V0 deterministic posterior-predictive battery, then V1 learned multi-label combiner; decisions move to the controller | A classifier P(valid) is calibrated only under the simulator prior, and the failures that matter most (out of scope) are OOD. Diagnosis and action in one network make neither testable. |
| **C** meta-controller | 4 | **modify**: rule table driven by V0/V1 with an *honesty rule*; offline ordering of remedies; no online BO/RL | "Search until it passes" is the garden of forking paths. The fix: the controller may change proposals and computation, never the likelihood or prior of the final comparison. |
| **L5** learned grouping encoder | 5 | **reject now / defer** | R1-P9, P2-P4: features must be analytic. Current failures are not grouping failures. A learned metric hides disagreement. In 2+1 with non-comaximal factors (CONV-D1) it would pick arbitrarily. |
| **L6** amortised NPE posterior | (v2.12 L3) | **defer, demoted** to an SBC-validated cross-check | The user is right that it must not compete. Its value is speed and a calibration check, never a label. |

The central position of this plan, which corrects the user's framing in one sentence:

> **ML may change *where* the Bayesian algorithm looks and *how fast* it gets there, and it may calibrate the *prior* on a declared simulator distribution. It may never change *what the data say* about a candidate.**

Every learned output is (i) a **proposal** (candidate modes, factors, structures, initial values, interpolation priors), scored afterwards by the exact raw-data evidence with its Occam term; or (ii) a **calibration** of a prior or constant, fitted offline, SBC-checked and reported as prior-dependent; or (iii) a **diagnostic flag**.

A proposal works like an *enumeration* aid: it decides which candidates get scored, not how they score. This is close to, but not the same as, an importance or MCMC proposal. Correct importance weights would need the proposal density after VarPro refinement, which is not available, so the plan does not claim importance-sampling exactness. What it claims, and enforces with the null gates of §9, is weaker: a candidate's score does not depend on who proposed it. Visiting more candidates can still inflate P(top) on nulls, and §4 C limits that. This is the defensible meaning of "ML as pre-calibration of a Bayesian algorithm". Where the user writes "the network outputs the missing parts" or "the validator decides", the plan replaces it with "proposes" and "flags".

---

## 1. Current state and failure census (as of the local session's uncommitted v2.12 work)

Benchmark (run 6, committed `80fedb5`): the pipeline is ≥ every SINDy variant in all 9 cells. Right set: grid 1.00/1.00/0.93, 2000 pts 1.00/0.97/0.90, 400 pts 1.00/0.93/0.73 at noise 0.1/1/5 %. cover90 (coef.) 0.75–0.93; w_cover90 0.50–1.00.

Remaining failures after the refine pass (plan v2.12), with a classification this plan proposes. The "class" column is a hypothesis that P0 must test:

| failure | probable class | evidence |
|---|---|---|
| TPD 400 @1 % s1, @5 % s0/s1; heat/TPD 400 @5 % as transport/τ only | **GP loss with information present** (κ ≤ 3–4), **information absent** above | estimate below; T35, T44 |
| beam 400 @5 % s0; beam 2000 @5 % s2 (regressed to τ) | partly GP loss, partly search (conjugate pair not proposed) | v2.12 |
| Schrödinger grid @5 % s0, 400 @1 % s1: spurious m = 2 factor | **search/selection**: the decider scored the chosen structure with coefficients read off biased modes | `_refine_alternatives` docstring (T51, local) |
| TPD 2000 @1 %, @5 % s1: right product, not split | **decision rule** (split-quadratic test after refinement) | v2.12 item 2 |
| weight cover90 0.50 at grid/1 %, 400/1 %, 2000/0.1 % | **model**: factor uncertainty not propagated into weights (now `coef_draws`); grids have one sample | v2.4, v2.10 |
| note example 5 %: weight interval misses | same | v2.10 |

**Back-of-envelope information estimate** (estimate, to be replaced by P0). `synthetic.py` uses the amplitude law a_κ = e^{−(κ/1.5)²/2} (3·10⁻⁴ at κ = 6) and heat λ = −0.3κ², on T = 2, uniform scattered points. The matched-filter SNR of a real mode on the raw data is

SNR_κ ≈ √(n · 2a_κ² · (1 − e^{4λ})/(−4λ)) / σ.

With n = 400 and σ = 0.05·std(u) ≈ 0.045, this gives SNR ≈ 26 at κ = 3, ≈ 4 at κ = 4 and ≈ 0.45 at κ = 5.

So the raw data plausibly carry the dx + 1 = 3 distinct κ that identifiability needs (T13, T40), and the GP throws part of them away. Above κ ≈ 4, *at 400 pts @ 5 %*, nothing can detect them. Caveats:
- The grid and 2000 points have more information.
- Detection SNR at the true (κ, λ) is not identification, which needs the CRB on λ.
- TPD's weaker branch is worse than heat.

P0.1 replaces this estimate. Where information is absent, the correct output is ID-KER/UNDECIDED, not a "fix". The consequences:
- (a) L1a (deterministic) should close most of the 400 @5 % gap.
- (b) Any learned layer that recovers κ ≥ 5 on this benchmark is reproducing its training prior.
- (c) The simulator's amplitude law is itself a prior: a layer trained on it learns "high κ is tiny". The generator must randomise it (P0.3).

---

## 2. Rules for every learned layer (additions to CLAUDE.md rules 3–5, proposed)

1. **Off = today.** Every layer has a switch. Off reproduces the deterministic pipeline bit-for-bit (a regression test on the benchmark jsonl).
2. **Proposal, calibration or flag only** (§0). No learned output enters a likelihood, and none changes a label by itself. The labels FIT-COMPATIBLE / MISFIT / ID-KER / UNDECIDED come only from the evidence and the identifiability rules (rule 5; DICT-A-iii, T17).
3. **Fixed likelihood in the final comparison.** All candidates that compete in the final posterior are scored with the same noise model, the same Occam rule and the same prior over structures. Constants that define the likelihood are set globally (L2), never per run (§6, honesty rule).
4. **Switch-on gate** (Phase 4 rule, made concrete in §9). On held-out simulated PDE *families*, the layer must give right-set ≥ off, coefficient error ≤ off, coverage within ±5 % of nominal and not worse than off, a false-FIT-COMPATIBLE rate ≤ off, and pass the null tests. Model selection never sees the held-out family (Gulrajani & Lopez-Paz 2021, [arXiv:2007.01434](https://arxiv.org/abs/2007.01434) (m)).
5. **Prior dependence is reported.** Any output that depends on the simulator prior (L2 maps, V1 probabilities, L6 posterior) carries the tag `prior: sim-v<k>` in the report.
6. **The core stays deterministic** (rule 3). Learned seeds enter `core/` only through an optional `seeds=` argument whose absence is today's code path, with tests.

---

## 3. P0 — prerequisites (no ML). Do these first.

### P0.1 Oracle information study
- **Purpose.** Split every failure into information absent / present but lost by the GP / present but lost by search. This decides whether any learned layer is needed and stops one from being credited for prior-driven answers.
- **What.** For every failing (case, sampling, noise, seed), on the *raw* observations:
  - (i) the Fisher information and CRB of each true mode (λ_j, a_j) at the true values (reuse `domain/extract.fisher_sigmas` logic on the scattered design);
  - (ii) `raw_evidence` of the true structure at the true coefficients, and after `refine_raw.refine` started at the truth, against the pipeline's answer;
  - (iii) the per-κ matched-filter SNR.
- **Classification.**
  - *Absent*: defined **without reference to the pipeline's output**, to avoid a circular benchmark. Compute the *expected* Fisher information of the design (sampling points, T, L, noise σ), per factor **branch** (TPD has one weak branch per κ, so heat's numbers do not carry over), averaged over noise. A factor is absent when fewer than dx + 1 distinct κ have a CRB on λ below a declared tolerance (e.g. 10 % of |λ|, and smaller than half the distance to the nearest other branch). The correct label is then ID-KER/UNDECIDED, and the benchmark is updated to count that as correct.
  - *Lost by GP*: the oracle evidence wins, but no GP sample proposes the structure.
  - *Lost by search*: some sample proposes it, but the loop drops it.
- **Insertion.** `analysis/exp/e10_oracle.py` (experiment only); results go to PARAMETERS.md.
- **Effort.** 0.5 session. **Theory.** T13/T30 (C3-T4), T40/T46 (R4-T4), T44 (R2-T6), DICT-A-iii.

### P0.2 Benchmark scoring that rewards honest abstention
- Add "correct-abstain" (ID-KER/UNDECIDED where P0.1 says absent) and "false-confident" (FIT-COMPATIBLE with a wrong set) to `benchmarks/report.py`. Report risk–coverage curves (selective prediction, Geifman & El-Yaniv 2017, [arXiv:1705.08500](https://arxiv.org/abs/1705.08500) (m)).
- Without this, every learned layer is pushed toward overconfidence.

### P0.3 Simulator extension (`synthetic.py`, next to `case`, reusing `modal_component`)
Today there are 10 fixed cases plus 3 extra, and the seed only changes phases. Needed:
- **Random symbols by family.** Draw the structure (k ≤ 3, m_j ∈ {1, 2}, dx_j ≤ 4), then the coefficients from a declared prior with a stability constraint (Re λ(κ) ≤ ε on the band), conjugate pairs for real fields, and optional κ = 0 shared modes and repeated factors.
- **Random excitation.** Number and range of κ (3–12, up to a random k_max), amplitude law (Gaussian of random width, power law κ^{−p}, flat), random T, L and phases.
- **Random sampling and noise.** Grid / 2000 / 400 / random n ∈ [200, 5000]; white, AR(1)-coloured, heteroscedastic, Student-t outliers.
- **Failure injection, labels known by construction.**
  - variable coefficient c(x) = c₀(1 + ε cos x);
  - weak nonlinearity ε u u_x, by a split-step solver;
  - fractional |ξ|^α;
  - two laws in two halves;
  - a single excited mode;
  - κ above the sampling Nyquist;
  - a degree beyond the start bounds (dx = 5–6);
  - a near-reducible irreducible factor (telegraph with small damping);
  - a reducible product with a nearly square discriminant.
- **Families for leave-one-family-out (LOFO).**
  - F1: real first order (transport, advection-diffusion, heat, KG-type low order);
  - F2: dispersive with a complex symbol (Schrödinger, Airy, beam, fifth order);
  - F3: second order in τ (wave, KG, telegraph);
  - F4: products and superpositions with k ≥ 2;
  - F5: edge cases (κ = 0 shared, repeated, single mode).
  - Held-out axes: a whole family; a degree (train dx ≤ 3, test dx = 4); the noise colour; the density.
- **Effort.** 1 session, with tests (exact dispersion of every draw).

---

## 4. Layers

### L0 — learned seeds for the per-bin exponential fit (new) — **ADOPT as a proposal**

- **Purpose.** The pencil is biased at low SNR, and its order choice fails when exponentials merge (v2.9 item 1; T10 / P2-Q3 **APERTO**: Prony/Hankel conditioning has no theory). THEORY_TO_ALGO §2 names this as "where ML can add something the theory does not give". A learned estimator gives better *seeds* (order and λ) for the existing BIC order choice and VarPro refinement.
- **Insertion point.** `core/structfit.extract_modes_ic` (structfit.py:129) gets an optional `seeds=` input: a list of candidate (order, λ-set) per bin. The BIC order selection (structfit.py:165) and VarPro then decide among {pencil, learned} seeds. The learned model runs outside the core, in a new `pdefactor/learned/expseeds.py`, called from `aggregate.run_core`. Off means the pencil only (today).
- **Model type.** A 1-D CNN or small transformer over the nt-length complex series of one κ-bin (real and imaginary channels), with a set-valued output. Either (a) a DeepFreq-style "pseudo-spectrum" head on a fine complex-λ grid (Izacard, Mohan, Fernandez-Granda, NeurIPS 2019, "Data-driven estimation of sinusoid frequencies", [arXiv:1906.00823](https://arxiv.org/abs/1906.00823) (m), built for undamped lines and extended here to the damped half-plane), plus an order head; or (b) a mixture-density head over λ with an order classifier. Prefer (a): peaks are easy to hand to VarPro, and its errors are visible. About 10⁵ parameters.
- **Inputs / outputs.** Input: one bin series y_κ(t) (from a GP sample, or the grid FFT) and its whitening (the `BinNoise` Toeplitz factor). Output: order probabilities r = 0..8 and the top-K λ candidates per order.
- **Training data.** Generic damped exponential sums Σ_j a_j e^{λ_j t} with random r ≤ 8, random λ (including near-merged pairs, Δλ down to 0.1/T), random amplitude ratios (down to 10⁻³), white and coloured noise at SNR 1–10⁴. These are **not PDE solutions**: by Ehrenpreis–Palamodov (R2-T6, T34) every bin of every in-scope field is such a sum, so the model never sees a PDE family and cannot overfit one. Size: 10⁶–10⁷ series, generated on the fly (seconds per 10⁴); training takes about an hour on the T2000.
- **Libraries.** PyTorch (in .venv via GPyTorch) + Lightning (skill present). No pretrained model exists for damped complex exponentials; DeepFreq's code is a template only (check its licence before reuse).
- **Calibration / acceptance.**
  - On held-out synthetic sums: λ-bias and efficiency against the CRB; order-selection accuracy against the pencil + BIC, by SNR and spacing.
  - On the benchmark: mode recall at fixed false-mode rate.
  - Switch-on gate (§2.4).
  - Key test: the BIC/VarPro *output* with learned seeds must be at least as good as without on every case. Seeds can only add basins of the *likelihood*, which is not the same as accuracy: a better optimum at a higher order can pass BIC and add a false mode. So L0 is also subject to the null gate (no extra modes on single-mode and pure-noise bins).
- **Risks and guards.**
  - *Risk:* it proposes spurious modes. *Guard:* BIC per bin plus the decider's raw evidence; seeds never bypass the order IC.
  - *Risk:* coloured GP noise outside the training range. *Guard:* train on Toeplitz-whitened inputs, using the same whitening as the GLS.
- **Effort.** 1 session. **Theory.** T10 (P2-Q3, open), T23 (rank in τ), T24 (confluent → UNDECIDED stays, unchanged).

### L1 — high-κ correction after interpolation (user item 1) — **MODIFY**

**Critical evaluation of the user's design.** The proposal is "raw data + interpolant (+ factor weights) → network → the missing high-κ parts". The objections:
1. **The known part needs no learning.**
   - For a stationary kernel at roughly uniform density, the posterior **mean** is asymptotically the filter H(ω) = S(ω)/(S(ω) + σ²/ρ) (equivalent kernel: Rasmussen & Williams ch. 7, [PDF](http://gaussianprocess.org/gpml/chapters/RW7.pdf); explicit cutoff and N_eff: Cao et al. 2025, [arXiv:2507.05067](https://arxiv.org/abs/2507.05067)). This is a heuristic description here: the pipeline's kernel has a non-stationary e^{β(t+t′)} envelope.
   - The core runs on posterior **samples**, which put prior-scale variance back where H is small. High-κ content is therefore not removed but *replaced by prior-shaped noise*, which is worse for the pencil than a clean zero.
   - Undoing H naively is an inverse filter that amplifies noise where H is small. A regularised (Wiener-type) inverse is stable, but it is again a shrinkage with the same prior-dependence.
   - So the "linear" correction is either unnecessary (it adds no information) or harmful.
2. **The unknown part is prior.** Whatever the network adds beyond what the raw data support comes from its training distribution. With the current simulator that distribution says "high-κ modes are e^{−κ²/4.5} small", so it learns to add nothing, or it learns the benchmark's specific λ(κ). Either way the output is a hallucination with respect to an unknown PDE (Rahaman 2019, [arXiv:1806.08734](https://arxiv.org/abs/1806.08734) (m); Xu 2020, [arXiv:1901.06523](https://arxiv.org/abs/1901.06523) (m): neural interpolants have *more* spectral bias than a GP, not less).
3. **The GP is the wrong input.** T44 already showed that the raw observations, not the GP mean, carry the evidence. Feeding the GP to the corrector carries its loss forward.
4. **The real cause is prior mismatch, which is not fixable by learning.** The interpolant uses separable stationary Matérn/RBF kernels with an optional e^{β(t+t′)} envelope (`interp/gp.py:48, 74`). A fast decay e^{−10t} is broadband in t, so a kernel whose length-scale is fitted to the slow modes gives it almost no prior mass. The theory (R2-T6) says what the right prior is: superpositions of e^{λt+iκx}, i.e. a spectral measure on (λ, κ) with λ in the left half-plane, which is EPGP with an *unknown* variety.
5. **Agreement with the user.** The gating idea ("it only proposes; the raw evidence decides") is exactly right and is kept for every variant below.

**L1a — deterministic (first; it may make L1b unnecessary).**
- **(i) Raw-data residual mode search.** After `decide_structure` and before the refine pass (loop.py ~L1238, inside the depth-0 cleanup):
  - form the raw residual r = y − ŷ of the current structure (its EPGP posterior mean on the observations);
  - scan a matched-filter / generalised Lomb–Scargle score for damped exponentials over (κ ∈ lattice, λ ∈ left-half-plane grid) on r. FINUFFT type-3 evaluates all κ at the scattered points fast (Barnett et al. 2019, [arXiv:1808.06736](https://arxiv.org/abs/1808.06736) (m); `finufft` 2.5.1, Apache-2.0);
  - refine the peaks by variable projection on the raw data (Golub & Pereyra 2003);
  - pass the found modes as `free_modes`/candidates to the decider and as *candidate factor additions* (lowest-degree factor through the found modes plus an existing factor's family) to `refine_raw.refine(candidates=...)`;
  - acceptance has a **look-elsewhere problem**: under the null (zero amplitude) λ is not identified (the Davies problem), so ½p log n is not a valid penalty for the *maximum* of a scan. The threshold for adding a scanned mode or factor is therefore taken from the null distribution of the maximum scan statistic: a parametric bootstrap of the residual under the current fit, or the Gross–Vitells upcrossing bound. Only then are raw evidence − Occam compared. The search is greedy (orthogonal-matching-pursuit style) with a fixed maximum of added factors (1 by default), and the null gate of §9 includes this scan.
- **(ii) Variety-aware interpolation prior, as a GP option.** An S-EPGP-type prior with learnable spectral points (Härkönen, Lange-Hegermann, Raiță, ICML 2023, [arXiv:2212.14319](https://arxiv.org/abs/2212.14319); [haerski/EPGP](https://github.com/haerski/EPGP), MIT, notebooks only). Two variants:
  - (a) on the *union of the current candidate varieties*: `interp/epgp.fit_epgp` already exists but is not chained in;
  - (b) a variety-free "Laplace-domain" prior, Σ over κ of a mixture over decay rates, plus an additive short-time component.
  Spectral-mixture kernels (Wilson & Adams 2013, [arXiv:1302.4245](https://arxiv.org/abs/1302.4245) (m); GP-HM, Fang et al., ICLR 2024, [arXiv:2311.04465](https://arxiv.org/abs/2311.04465)) are the generic version (`gpytorch.kernels.SpectralMixtureKernel`, GPyTorch 1.15.2, MIT). Because the decider works on raw evidence, the interpolant is a *proposal mechanism* for the structure, so trying another prior is legitimate (§6). For the *weights* the interpolant matters (the split layer uses the samples), so there the prior family is mixed by evidence (as `fit_gp` already does over families), never chosen per run by outcome.
- **(iii) Kronecker GP on grids** (plan v2.11 open item; KBASS-style, Long et al. AISTATS 2024, [arXiv:2310.05387](https://arxiv.org/abs/2310.05387), [long-da/KBASS](https://github.com/long-da/KBASS), MIT, JAX, grid-only). This gives grids posterior samples, so they share the scattered-data path, and the bootstrap stops overwriting the refined intervals (today `bootstrap_intervals` replaces them on grids).
- **Training data:** none. **Effort:** 1.5 sessions ((i) 0.5, (ii) 0.75, (iii) 0.25 if KBASS is used only as a reference). **Theory:** R2-T6/T34, T35 (DICT-ILIM-Hs), T44, T13/T40 (identifiability count per added factor), CONV-T5 (no data-free threshold, hence evidence).
- **Acceptance:** P0.1 "lost by GP" cases recovered; no new false factors on the null set (single-factor data, pure noise); switch-on gate.

**L1b — learned proposal (only if P0.1 still shows "information present, missed" after L1a).**
- **Purpose.** Amortise the multimodal part of L1a(i): two or more close damped modes in the residual, where a greedy matched filter resolves one merged peak.
- **Insertion.** Same place as L1a(i). It replaces the grid scan by proposals and is followed by the same VarPro + evidence.
- **Model type.** A conditional density estimator q(mode set | residual summary): a permutation-invariant set encoder over the raw residual points (t, x, r) (Deep Sets, Zaheer 2017, [arXiv:1703.06114](https://arxiv.org/abs/1703.06114) (m); Set Transformer, Lee 2019, [arXiv:1810.00825](https://arxiv.org/abs/1810.00825) (m)), or more cheaply over the NUFFT residual spectrum per κ. The head is a mixture density or normalising flow over (λ, a) per κ (zuko 1.6.0, MIT). Proposals are drawn, refined and scored, and they enter the declared candidate enumeration of §4 C. No importance weights are claimed: the density of a proposal after VarPro is not computable. The scan threshold of L1a(i) applies.
- **Training data.** Residuals of the pipeline (after L1a) on P0.3 draws, with the true missing modes as targets. About 3–5 k runs (≈ 10–15 h on 6 workers). **Train families ≠ test families (LOFO)**: the target is "modes in a residual", so the family-dependence should be weak. If LOFO shows it is not, reject L1b.
- **Rejected alternatives for this role** (reasons from the research pass):
  - FNO / DeepONet / `neuraloperator` 2.0.0 (MIT): forward surrogates for a known PDE; FNO truncates high Fourier modes by design.
  - PDE foundation models (Poseidon, [HF](https://huggingface.co/camlab-ethz/Poseidon-B), CC-BY-NC; MPP; DPOT; The Well 1.2.0, BSD-3): 2-D/3-D gridded fluids, no calibrated UQ, outputs a smoothed field again.
  - Scattered-input reconstructors (GNOT, OFormer, CORAL, AROMA, Senseiver): trained per family; they reconstruct the prior.
  - Diffusion priors (DiffusionPDE, [arXiv:2406.17763](https://arxiv.org/abs/2406.17763); score-based data assimilation, Rozet & Louppe 2023, [francois-rozet/sda](https://github.com/francois-rozet/sda), MIT; FreqNO-DPS, [arXiv:2606.03936](https://arxiv.org/abs/2606.03936)): need a prior trained on the target family, which is circular for identification, and DPS-type guidance is not exact Bayes.
  - SIREN / Fourier features (Sitzmann 2020, [arXiv:2006.09661](https://arxiv.org/abs/2006.09661) (m); Tancik 2020, [arXiv:2006.10739](https://arxiv.org/abs/2006.10739) (m)): no UQ, a hand-set frequency prior; kept as the existing ablation (`interp/ensemble.py`).
  - PROSE-PDE ([arXiv:2404.12355](https://arxiv.org/abs/2404.12355)), the closest pretrained "identifier": gridded, mostly nonlinear training families, no posterior. It is at most a structure proposal and not worth the dependency.
- **Effort.** 1.5 sessions. **Verdict.** L1 = **modify**: L1a adopt; L1b conditional.

### L2 — learned calibration (user item 2) — **MODIFY**

**Critical evaluation.** The proposal is to tune LOG_BF_STRONG, P_CONCENTRATED, z, CAP, snr_min, bootstrap size, interval scale factors and Occam weights, plus an optional features → constants map that "extrapolates beyond the training PDEs". The objections:
1. **Budget.** The code has about 60 method constants (Appendix A). One evaluation of a constant setting on a 300-run benchmark subset costs about 1 h on 6 workers (pipeline median 17 s, p90 181 s at 400 pts). That allows about 30–50 BO evaluations, which is enough for 4–5 constants at most. A features → constants hypernetwork, trained on that, is pure overfitting.
2. **The constants are of three kinds, and only one kind should be tuned.**
   - *Likelihood-defining* (CAP, z, snr_min, EPS_GRID, JITTER, the GP hyperpriors, the Occam rule): they change what the evidence *is*.
   - *Decision* thresholds (P_CONCENTRATED, LOG_BF_STRONG, p_more = 0.5, the MISFIT mass 0.5, 2·SE): they act on probabilities.
   - *Computational* settings (inits, ALT_TOP, W_DRAWS, B, S_LOOP, ndraw): more is better, subject to cost.
   Decision thresholds should not be tuned at all once the probabilities are calibrated: they follow from a stated loss. Computational settings are set by a cost–accuracy curve. Only likelihood-defining constants need data, and those must be **global**, not per-run.
3. **"Extrapolates beyond the training PDEs" cannot be guaranteed by any method.** Conformal guarantees hold under exchangeability with the calibration set, i.e. within the simulator prior. Weighted conformal (Tibshirani 2019, [arXiv:1904.06019](https://arxiv.org/abs/1904.06019) (m)) and "beyond exchangeability" (Barber 2023, [arXiv:2202.13415](https://arxiv.org/abs/2202.13415) (m)) degrade by a total-variation term that cannot be bounded for out-of-scope classes. Extrapolation is therefore *measured* (LOFO), not promised, and it is made more likely by using few features that are dimensionless and theory-defined, with monotonicity fixed by the theory.
4. **Fix the model before recalibrating.** Weight undercoverage has a known model cause: factor uncertainty was not propagated, and grids have one sample. The local session is fixing it with `coef_draws`, and L1a(iii) adds GP samples on grids. Recalibrating first would hide that.

**Design.**
- **L2a — diagnostics, no learning (first).**
  - SBC per family on P0.3 draws (Talts 2018, [arXiv:1804.06788](https://arxiv.org/abs/1804.06788) (m); Modrák 2023, [arXiv:2211.02383](https://arxiv.org/abs/2211.02383) (m)): rank histograms of the true coefficients and weights within the reported posteriors.
  - TARP coverage (Lemos 2023, [arXiv:2302.03026](https://arxiv.org/abs/2302.03026) (m)).
  - Reliability diagrams and ECE of the structure posterior (already used: T29), per family and per feature regime.
  - Insertion: `benchmarks/report.py` + `analysis/exp/e11_sbc.py`.
  - Size: about 300 draws per family × 5 families ≈ 1.5 k runs (≈ 5 h).
- **L2b — structure-probability calibration and decision-theoretic thresholds.**
  - Keep two penalties apart. ½p log n is the **parameter-integration** term, which grows with n. Calibrate it through the *scale of the coefficient prior* (a g-prior on the factor coefficients, so the n-dependence is right on 400 points and on grids alike), not by a global α. Separately, fit a **structure prior** log π(st) = −β₁·k − β₂·Σ(m_j + dx_j), with β by hierarchical empirical Bayes over the simulated corpus. It is n-independent and tagged prior-dependent. Then apply an isotonic recalibration of the top-structure probability if the reliability diagram still deviates (Kuleshov 2018, [arXiv:1807.00263](https://arxiv.org/abs/1807.00263) (m)).
  - Data hygiene: three disjoint splits of the simulated corpus: *fit* (β, g, isotonic and monotone maps), *calibrate* (the conformal step) and *test* (LOFO report).
  - Then derive every decision threshold from a declared loss: for example, accept a regroup when P(top) > L_false/(L_false + L_miss). P_CONCENTRATED and LOG_BF_STRONG become *outputs* of the loss, not tuned constants.
  - Insertion: the Occam term at loop.py:405/409/1255 and refine_raw.py:174 (one function `occam(p, n, k)`), and the thresholds in loop.py (P_CONCENTRATED L30, LOG_BF_STRONG L592, p_more L1195, the MISFIT mass L1064).
  - Model: two scalar hyperparameters plus an isotonic map. Library: scikit-learn `IsotonicRegression`.
- **L2c — interval recalibration (only for what L2a still shows after the model fixes).**
  - One **monotone** inflation map per quantity type (coefficient, weight) on 3–5 dimensionless theory features:
    - the split amplification γ_N^{−1/2}·σ/|w| (T5/T6, P2-T3/P2-T4): non-decreasing;
    - the mode-count margin n_κ − (dx + 1) (T13/T40): non-increasing;
    - the Vandermonde condition κ_Vand (T9, P2-P6): non-decreasing;
    - the per-factor SNR: non-increasing;
    - the posterior-sample disagreement (T48): non-decreasing.
  - Model: LightGBM / sklearn `HistGradientBoosting` with `monotonic_cst`, or a monotone GAM. `tensorflow-lattice` 2.1.1 (2024) is stale, so it is not used.
  - On top: Mondrian / conditional conformal (Gibbs, Cherian, Candès 2023, [arXiv:2305.12616](https://arxiv.org/abs/2305.12616)) over regimes (family-free bins of the features), on the *calibrate* split only. This gives finite-sample coverage *within the simulator prior*. MAPIE 1.6.0 (BSD-3) or crepes 0.9.1 (BSD-3). Coefficient intervals exist only when the selected structure contains the factor, so coverage is reported **conditional on correct selection**, together with the selection rate. Unconditional exchangeability does not hold.
  - Insertion: at the end of `refine_factors` (loop.py ~L869-875), `bootstrap_intervals` (L740) and `split_layer` (L495-496); off means the scale is 1.
  - Training: the L2a corpus plus 1 k extra runs.
- **L2d — likelihood-defining constants, once and globally.**
  - Multi-objective BO over at most 4–5 constants (CAP, z, snr_min (split layer), EPS_GRID upper bound, JITTER) on a fixed 300-run P0.3 subset. Objectives: right-set, false-confident rate, SBC deviation.
  - Libraries: Ax 1.3.1 / BoTorch 0.18.1 (MIT) or SMAC3 2.4.1 (BSD-3); offline only.
  - Selected on families F1–F4, checked on F5 and on the held-out noise colour.
- **Acceptance.** Coverage within ±5 % per family on LOFO; reliability ECE ≤ off; benchmark ≥ off. If a map helps in-family but hurts LOFO, it is rejected.
- **Effort.** L2a 0.5, L2b 0.75, L2c 0.75, L2d 0.5 sessions (plus compute).
- **Theory.** CONV-T5 (no data-free threshold, so thresholds are prior-relative), T5/T6 (γ_N floor), T9, T13, T18/T29 (discrete outputs → reliability).

### V — validator (user item 3) — **MODIFY** into V0 (deterministic) + V1 (learned combiner)

**Critical evaluation.** The proposal: input = all outputs of every previous loop iteration (coefficient Gaussians, structure posterior, weights and intervals, E_int, c_F, γ_N, ρ, κ support, labels, domain outputs, the first whole-data run, simulation results); output = P(valid) + a failure diagnosis + *decisions* (parameters, interpolation weights, frequencies) for the next loop. The objections:
1. **P(valid) is prior-relative.** A classifier trained on `synthetic.py` outputs P(valid | features, simulator prior). On real data its calibration is unknown, and the most important failures there (nonlinear, variable coefficients, fractional, mixed regimes) are exactly the OOD inputs on which a classifier is least reliable. Simulation-based inference reports overconfidence as the common failure (Hermans et al., "A trust crisis in SBI", [arXiv:2110.06581](https://arxiv.org/abs/2110.06581) (m)).
2. **"All outputs" is too many inputs.** They are high-dimensional and variable-size, against the 2–5 k affordable labelled runs (§1 budget). A Set Transformer over raw outputs needs roughly 10× more data. The model would learn the simulator's quirks: "Schrödinger seed 1 at 1 % has a τ² factor".
3. **Most diagnoses are computable deterministically.** They are posterior-predictive checks with a known null. A learned model should *combine* such checks, not replace them.
4. **Diagnosis and action must be separate.** A network that both diagnoses and chooses the next parameters cannot be tested component-wise. Its decisions also change the likelihood per run, which breaks the honest final comparison (§6). Decisions therefore go to the controller C, which uses a remedy table.
5. **The re-simulation idea is right and important.** It is the parametric bootstrap / posterior predictive check: simulate the fitted PDE with fitted amplitudes at the *same design and noise*, rerun the relevant statistics, and compare. It becomes the null distribution of every V0 test.

**V0 — deterministic diagnostic battery** (insertion: a new `pdefactor/validate.py`, called after `LoopResult` at loop.py ~L1303, read-only on the result).

Each statistic has a parametric-bootstrap null: B re-simulations from the fitted law, using the user's simulation hook, plus the same design and noise draws. The output is a p-value or e-value per statistic, with the statistics listed in the report.

| id | statistic | detects | theory |
|---|---|---|---|
| V0.1 | raw-residual energy and whiteness per κ band (NUFFT of the raw residual vs its re-simulated null) | high-κ loss, missing factor | T35, T44 |
| V0.2 | mode-count margin per factor, n_κ − (dx + 1), with observed roots ≤ m per κ | ID-KER, interpolating factor | T13, T40, T46 |
| V0.3 | evidence gap to the 2nd structure and to "± one factor" (refined, T51), and the posterior entropy | unresolved ambiguity, spurious factor | T18, T39 |
| V0.4 | per-sample disagreement (raw evidence spread, T48; track co-occurrence) | local optimum, multimodal posterior | T48 |
| V0.5 | Ljung–Box / spectral flatness of raw residuals in t, and a variogram in x | correlated noise, misspecified noise model | T36, T37 |
| V0.6 | **trend of the selected degree across a noise sweep**: data are degraded on purpose (added noise at several levels, or subsampling), and the selected (m, dx) is compared with a simulated null. At a fixed noise level the curve always saturates (DX_LIMIT), so a single curve proves nothing | **out of class**: if Ann(u) = 0 the discrepancy-selected degree m(δ) → ∞ as δ → 0 (CONV-T5), so a selected degree that keeps rising as the effective noise falls points to a fractional or non-polynomial symbol, or variable coefficients. The test can only lower the effective noise down to the data's own σ, so it has low power; it is reported as a flag, never as "no finite degree" from one dataset | CONV-T5 |
| V0.7 | λ(κ) drift across t-windows and across subdomains (from `domain_report` / quadtree): Bayes factor "one law" vs "per-cell laws" | variable coefficients, mixed regimes | C12-T1′, T1 |
| V0.8 | amplitude-scaling and κ-coupling test: energy at κ₁ ± κ₂ not on any variety, and λ depending on the amplitude between t-windows | nonlinearity (out of scope) | R2-T6 (linear solutions decouple in κ) |
| V0.9 | discriminant-square gap (C12-P2/P3) and the split-quadratic test after refinement | unsplit reducible / near-reducible irreducible | T3, T49 |
| V0.10 | c_F, γ_N, γ_N^{−1/2}σ vs the weight value | weights not separable at this σ (floor) | T5, T6 |
| V0.11 | confluent test outcome (A + Bt)e^{λt} | repeated factor | T24 |
| V0.12 | classifier two-sample test, observed residual field vs re-simulated residual fields (C2ST, Lopez-Paz & Oquab 2017, [arXiv:1610.06545](https://arxiv.org/abs/1610.06545) (m)) | any remaining misfit (omnibus) | — (empirical) |
| V0.13 | heldout-in-time score (the existing `heldout_score`) on the final structure | overfit | T15 |

- **Calibration of the p-values.** Plug-in parametric-bootstrap and posterior-predictive p-values are conservative, not uniform (Robins, van der Vaart, Ventura, JASA 2000). They are calibrated by a double bootstrap on the simulated corpus, or by conformal p-values against correct-fit simulations (Bates et al. 2023). The 13 statistics are combined into one omnibus statistic before any test, which avoids a multiplicity correction at a coarse resolution. B ≥ 200 for the omnibus statistic, B = 20 only for screening.
- **Effort.** 1.5 sessions (V0.1–V0.11 reuse existing functions; V0.12 needs a small classifier, sklearn GBM).
- **Cost.** B = 200 re-simulations × a partial rerun (core + raw evidence only, no GP) ≈ 10–20 min per run, run only at the end of a run. B = 20 screening ≈ 1–3 min.

**V1 — learned multi-label combiner.**
- **Purpose.** Turn the V0 vector into calibrated probabilities over failure modes (§8 table), plus an OOD score. Use them to order the controller's remedies and to set the report's flags.
- **Insertion.** `validate.py`, after V0. Off means V0 p-values only.
- **Model type.**
  - Gradient-boosted trees (LightGBM / sklearn HGB), one-vs-rest per failure mode, with monotone constraints where a statistic's direction is known.
  - Inputs: the V0 statistics plus permutation-invariant aggregates of the factor list (number of factors; max/min/sum over factors of the coefficient z-scores, the κ-support size, inclusion probability, ρ, the Vandermonde condition).
  - Domain and subdomain outputs enter as the V0.7 block of the *same* model, not as a second model: a second model halves the data per model and the heterogeneity signal is already one Bayes factor.
  - Deep Sets / Set Transformer only if the corpus exceeds ~50 k runs, which is not planned.
  - Several failures can co-occur, so the outputs are multi-label. Single-label conformal sets do not apply; the set of reported modes is controlled by **conformal risk control** (Angelopoulos et al., [arXiv:2208.02814](https://arxiv.org/abs/2208.02814) (m)), with a missed-failure rate ≤ 10 % within the simulator prior, via MAPIE.
  - OOD score: conformal outlier p-values on the V0 vector (Bates et al., Ann. Stat. 2023, [arXiv:2104.08279](https://arxiv.org/abs/2104.08279) (m)) and a Mahalanobis distance (Lee 2018, [arXiv:1807.03888](https://arxiv.org/abs/1807.03888) (m)). If OOD, V1's probabilities are not shown and the report says "outside the validator's training range".
- **Training data.** Failure-injected P0.3 runs, labels known by construction. About 4 k runs: ≈ 12–15 h for the pipeline, plus ≈ 22 h for V0 screening at B = 20 (≈ 2 min × 4 k / 6 workers), so 1.5 days in total. LOFO over families *and* over injected failure types (train on 7 of 9 injection types, check that the two held-out ones score OOD or "other" rather than being misassigned).
- **Calibration and acceptance.**
  - Per-mode reliability and conformal set coverage on LOFO.
  - The decisive test: does V1's remedy ordering reduce the controller's number of actions (cost) at equal final accuracy, compared with a fixed order? If not, keep V0 only.
- **Risks and guards.**
  - *Risk:* label leakage through seeds or case names. *Guard:* features exclude all identifiers.
  - *Risk:* a shortcut on noise level. *Guard:* stratify by noise.
  - *Risk:* overconfidence. *Guard:* conformal sets, the OOD gate, prior tag.
- **Libraries.** scikit-learn 1.9.1 (installed), LightGBM (MIT), MAPIE 1.6.0 (BSD-3).
- **Effort.** 1 session plus compute.
- **On the user's "amortised inference as validator".** sbi 0.27.0 (Apache-2.0: NPE, NLE, NRE, BNRE; SBC/TARP/L-C2ST diagnostics) or BayesFlow 2.1.0 (MIT; amortised model comparison, Radev et al. [arXiv:2004.10629](https://arxiv.org/abs/2004.10629) (m); misspecification detection by MMD in summary space, Schmitt et al. [arXiv:2112.08866](https://arxiv.org/abs/2112.08866) (m)) *can* be used as validators: train an NPE on the pipeline's summary features and check whether the pipeline's answer lies in its high-density region (L-C2ST, Linhart 2023, [arXiv:2306.03580](https://arxiv.org/abs/2306.03580) (m), for the per-observation check). This is L6 below. It needs about 10⁴ runs and validates only in-prior. V0 + V1 give the same failure information for less data and with an interpretable reason, so L6 is deferred.

### C — meta-controller (user item 4) — **MODIFY**

**Critical evaluation.** The proposal: the validator decides whether to loop again and how (rerun with other parameters, switch to the learned encoder, raise the order, change any core/loop parameter), instead of looping blindly. The idea of a *targeted* loop is right: the current loop already does this in fixed order (degree growth, regroup, complex rerun, alternatives). The objections:
1. **Garden of forking paths** (Gelman & Loken 2013, [PDF](http://www.stat.columbia.edu/~gelman/research/unpublished/p_hacking.pdf) (m)). If the controller changes the likelihood (CAP, snr_min, the noise model, the Occam weight) until the validator passes, the final evidence is the maximum over a search. Its probabilities are then inflated, and the output contract is broken in spirit even when the labels are formally right. Marginal likelihood under data-dependent choices loses its meaning (Lotfi et al., ICML 2022, [arXiv:2202.11678](https://arxiv.org/abs/2202.11678) (m)).
2. **Online BO or RL per run is unaffordable and opaque.** About 10 actions per run, each costing 10 s–3 min, so there is no budget for BO per dataset. An RL policy needs orders of magnitude more episodes (e.g. Li & Malik, [arXiv:1606.01885](https://arxiv.org/abs/1606.01885) (m)) and gives no reason for its choices.
3. **"Switch to a learned encoder"** is rejected (L5).

**Design.**
- **Honesty rule (the key rule of Phase 4).** The controller may change only:
  - (a) the **candidate set**: proposals from L0, L1a/L1b, higher (m, dx), split/merge moves, complex rerun, alternatives;
  - (b) **computational settings** that do not change the target: more GP samples, restarts, ALT_TOP, ndraw;
  - (c) the **interpolation prior** used to *generate proposals*. This is legitimate because the decider scores on raw evidence, so the interpolant is a proposal mechanism, except for the weights (§L1a(ii)).
  
  It may **not** change likelihood-defining constants or the structure prior per run. Then every candidate ever visited is scored under one fixed prior and likelihood, and the search changes *which* candidates are evaluated, not *their* evidence.

  **This alone does not stop inflation.** Two effects remain:
  - Renormalising the posterior over the *visited* set drops the mass of unvisited structures, and visiting more near-ties raises the chance that one wins on a null.
  - More restarts give a better optimum and therefore a higher Laplace/BIC-type score.

  Required, therefore:
  - (1) **Declare the candidate space before the run.** All structures up to the degree limits, with the structure prior split evenly within each complexity class (L2b). Proposals only decide *which* members get scored. The report is the posterior over all visited structures (BMA; stacking, Yao et al. 2018, [arXiv:1704.02030](https://arxiv.org/abs/1704.02030) (m), as a robustness check under M-open), plus an **upper bound on the unvisited prior mass** times the best attainable evidence, which is reported as a missing-mass term.
  - (2) **Equal refine budget per candidate**, fixed in advance (the same restarts and iterations), so that no candidate wins by extra optimisation.
  - (3) The noise model (white / coloured) is a *model* choice. Both versions are **always** candidates from the start, not added after a diagnosis.
  - (4) The null gate of §9 (forking-paths test) is the empirical check of (1)–(3).
- **Remedy table** (diagnosis → actions, in order):

  | diagnosis (V0/V1) | action |
  |---|---|
  | high-κ loss (V0.1) | L1a(i) search → L0 seeds → L1a(ii) prior → L1b; stop with ID-KER if V0.2 fails |
  | degree too low (V0.6 saturating) | the existing `_grow` |
  | out of class (V0.6 non-saturating, V0.7, V0.8) | **stop**: MISFIT/UNDECIDED with the reason, domain report (v2.9.4) |
  | local optimum / disagreement (V0.4) | more inits and samples, ALT_TOP ↑ |
  | spurious factor (V0.3) | `raw_subset` / refine drop (exists) |
  | unsplit reducible (V0.9) | `split_quadratics` |
  | near-reducible irreducible (V0.9) | none: keep irreducible, report |
  | weights inseparable (V0.10) | none: report the floor |
  | correlated noise (V0.5) | none extra: coloured-noise candidates are always in the declared space; report which noise model wins |
  | repeated factor (V0.11) | stop: UNDECIDED (T24) |

  Within a diagnosis, the order of remedies is learned **offline** as the empirical success rate per remedy on failure-injected runs, i.e. an offline contextual-bandit estimate with no online exploration.
- **Held-out confirmation, decided before the run.** The split must be fixed *before* any search; otherwise the trigger and the split both depend on X and independence is lost. Mode "confirm" is a per-run switch chosen by the user before running; it is not triggered by the number of actions:
  - Gaussian **data fission** (Leiner, Duan, Wasserman, Ramdas, JASA 2023, [arXiv:2112.11079](https://arxiv.org/abs/2112.11079)) or **data thinning** (Neufeld et al., JMLR 2024, [arXiv:2301.07276](https://arxiv.org/abs/2301.07276)): with X ~ N(μ, Σ) and Z ~ N(0, Σ) for the **known** Σ, f(X) = X + τZ and g(X) = X − Z/τ are independent. The whole controller runs on f; the final structure gets one pre-specified evidence comparison on g. It is valid only when Σ is known or estimated independently (e.g. replicate measurements, or an instrument spec). With σ from ML-II, coloured, heteroscedastic or Student-t noise, independence fails.
  - Otherwise: a **random point split fixed before the run** (search on one half, confirm on the other). Simpler and valid under any noise; it halves the density.
  - Cost in both cases: lower SNR per half, which hurts the high-κ case most. Report which mode was used.
- **Budget and stopping.**
  - At most K = 4 actions with the equal refine budget per candidate; stop when no diagnosis is active, or when V1's expected gain per unit cost falls below a threshold.
  - No anytime-validity claim. The confirmation is **one** pre-specified comparison on the held-out part. A Bayes factor is an e-value only against a simple null (or one averaged under the null's own prior), not for composite nulls with nuisance parameters or Laplace/BIC approximations; and anytime validity concerns data arriving over time, not repeated searches on the same data. If a frequentist guarantee is wanted, use split-likelihood-ratio universal inference on the held-out part (Wasserman, Ramdas, Balakrishnan, PNAS 2020, [arXiv:1912.11436](https://arxiv.org/abs/1912.11436) (m)).
- **Insertion.** A new `pdefactor/controller.py` wrapping `run_loop`. The current loop's fixed-order steps become table entries. Off means today's fixed order.
- **Training.** Only the offline remedy-success table: the V1 corpus with each remedy applied, about 2 k extra runs.
- **Libraries.** None needed online. Offline: pandas/sklearn; SMAC3 only if the table is replaced by algorithm selection (not planned).
- **Acceptance.**
  - Benchmark ≥ off and fewer actions per run.
  - **The forking-paths test**: on null data (single-factor and pure noise), the false-FIT-COMPATIBLE rate with the controller must equal the rate without it (±MC error); on data-fission-confirmed runs, coverage holds.
- **Effort.** 1 session.

### L5 — learned grouping encoder (user item 5) — **REJECT now, DEFER**

- **Theory.** R1-P9 and P2-P4 (DIMOSTRATO, LEDGER row 59): no stable linear encoder makes E_int → 0, and the log-symbol (nonlinear) reads terms linearly, so the grouping features must be analytic (T8). Grouping is by factors only (v2.9.4), and today's failures are not grouping failures (§1).
- **Where it would harm.**
  - (i) A learned metric over factor tracks merges or splits tracks without an evidence statement. That hides disagreement which `aggregate` (DP + finite-k BIC, T25) currently reports.
  - (ii) Augmentations define invariances; wrong ones merge branches that are close at low κ, which is exactly where the data are.
  - (iii) New factor types are OOD and get confident wrong embeddings.
  - (iv) In 2+1 / 3+1 with non-comaximal factors the decomposition ambiguity is infinite-dimensional (CONV-D1, DIMOSTRATO), so an encoder would choose a decomposition arbitrarily.
  
  No published contrastive encoder for clustering dispersion branches exists (research pass, §H).
- **Where it could help later.**
  - Variable coefficients through frozen-coefficient cells: matching local factors across many cells with drifting coefficients;
  - 2+1 with comaximal factors and many κ-vectors.
  
  Even there, the baseline is deterministic first: Hungarian matching with a Mahalanobis cost using each track's posterior covariance (`agg.Sigma`). A learned similarity is used only as the cost matrix of that matching, evaluated by ARI against injected regimes. It never replaces the evidence.
- **Effort if revisited:** 1 session.

### L6 — amortised posterior (NPE) as cross-check — **DEFER**

- **Purpose.** A second posterior over structure and coefficients from summary features, for speed and as an SBC calibration check of the Bayesian layer (Phase 4 original bullet).
- **Insertion.** After `LoopResult`. It reads `extract_modes_ic` modes with σ_λ, the decider's evidence, the refined coefficients and the split outputs.
- **Model.** NPE with a flow (sbi 0.27.0); the structure as a categorical head (BayesFlow amortised model comparison). Prefer conservative BNRE (Delaunoy 2022, [arXiv:2208.13624](https://arxiv.org/abs/2208.13624) (m)) for the coefficients.
- **Data.** At least 10⁴ runs; the cheaper core-only route on grids is possible.
- **Use.** If it agrees with the pipeline, report it. If it disagrees, raise a flag and show it tagged prior-dependent. If the pipeline says UNDECIDED, show it as extra information but never as a label. L-C2ST per observation.
- **Why deferred.** Its information is already covered by V0/V1 at a fraction of the data, and its validity is in-prior only.

### Differentiable core (v2.12 L5)
Not needed. `refine_raw` already optimises the raw evidence over the factor coefficients, which is the end-to-end step of the note's Q2.2 without touching the core. Unchanged.

---

## 5. Critical summary of the user's proposal: what to change

1. **"The correction layer outputs the missing parts" → "it proposes candidate modes from the raw residual".** Most of the gap is fixable deterministically (L1a). The rest may be information-absent, where ID-KER is the right answer. Do P0 before any network. The user's own gating recommendation (raw evidence decides) is correct and kept.
2. **The GP is not the only culprit; its prior is.** Change the interpolation prior towards the theory (EP / S-EPGP, decay mixtures) before correcting its output.
3. **Train where the theory makes the problem universal.** The best learned component (L0) is trained on generic exponential sums, not on PDEs. By R2-T6 that is all an in-scope field is per κ-bin, so it does not need to "extrapolate beyond the training PDEs". This answers the user's generality requirement better than any features → constants map.
4. **Calibrate probabilities, not thresholds.** Thresholds then follow from a loss. Tune only the few likelihood-defining constants, globally, once.
5. **Learned calibration cannot promise extrapolation.** It can be measured with LOFO and made likely with few monotone, dimensionless, theory-defined features. Say so in the report.
6. **The validator diagnoses; it does not decide.** Build the deterministic posterior-predictive battery first, with the user's re-simulation as its null. The learned part only combines and orders. "All outputs of all iterations" as input is replaced by theory statistics plus permutation-invariant aggregates.
7. **The controller must obey the honesty rule.** Proposals and computation may change; the likelihood and prior of the final comparison may not. Report the posterior over all visited structures; confirm long searches on fissioned data.
8. **The user is right about** keeping everything optional and calibrated; using simulation as a check; a targeted outer loop instead of a blind one; the learned encoder only later and inside the bigger loop; and the amortised posterior not competing.
9. **One more change the user did not ask for:** the benchmark must reward correct abstention (P0.2). Otherwise every layer optimises toward false confidence on 400 pts @ 5 %.

---

## 6. Ordered build plan

Each step has a gate. A step that fails its gate stays off and is reported.

| # | step | depends on | effort (sessions) | compute | gate |
|---|---|---|---|---|---|
| 1 | P0.3 simulator extension (random families, failure injection, LOFO splits) | — | 1 | — | exact dispersion test for every draw |
| 2 | P0.1 oracle information study + P0.2 scoring | 1 | 0.5 | ~2 h | every failure classified absent / GP / search |
| 3 | L2a SBC + reliability per family (no learning) | 1 | 0.5 | ~5 h | report only |
| 4 | V0 battery + re-simulation null (`validate.py`) | 1 (+ the user's simulation hook) | 1.5 | ~10–20 min/run at B = 200 | calibrated omnibus p-value has a ±5 % false-alarm rate on correct fits |
| 5 | L1a(i) raw residual search; (iii) grid GP | 2 | 0.75 | — | "lost by GP" cases recovered, nulls clean |
| 6 | C controller with honesty rule and fixed order | 4, 5 | 1 | — | forking-paths null test |
| 7 | L1a(ii) EP/decay interpolation prior | 2 | 0.75 | GP refits | right-set ↑ at 400 pts, coverage of u unchanged |
| 8 | L2b calibrated Occam prior + loss-derived thresholds | 3 | 0.75 | ~5 h | ECE ↓, LOFO |
| 9 | L2c monotone + conformal intervals (after the local `coef_draws` fix) | 3, 8 | 0.75 | ~3 h | coverage ±5 % per family on LOFO |
| 10 | L2d global BO on ≤ 5 likelihood constants | 8 | 0.5 | ~40 h | LOFO not worse |
| 11 | V1 learned combiner + OOD + conformal risk control; offline remedy order for C | 4, 6 | 1 | ~1.5 days | fewer actions at equal accuracy |
| 12 | L0 learned exponential seeds | — (parallel to 5–11) | 1 | 1 h GPU | λ efficiency vs CRB; benchmark ≥ off |
| 13 | L1b learned residual proposal | 2 says needed after 5, 7, 12 | 1.5 | ~15 h | LOFO; nulls clean |
| 14 | L6 NPE cross-check | 11 | 1 | ~10⁴ runs | SBC |
| 15 | L5 encoder | only with 2+1 or variable coefficients in scope | 1 | — | ARI vs Hungarian baseline |

Deterministic fixes that the local session already has in progress (refining top alternatives, split quadratics after refinement, coefficient draws into weights) come before steps 3, 9 and 11. They are not duplicated here.

Parallelism: steps 1–2 first. Then {3, 4, 12} can run in parallel, then {5, 7}, then 6, then {8, 9}, then {10, 11}.

---

## 7. Where each layer plugs in (call-graph view)

```
bench_e2e.load_input → fit_gp (interp/gp.py:438)            ← L1a(ii) prior option; L1a(iii) grid GP
run_loop (loop.py:1043)                                       ← C wraps it (controller.py)
  _run → run_core → analyze_structured → extract_modes_ic    ← L0 seeds= (outside core, optional arg)
       → aggregate (DP, finite-k)                            (L5 would sit in align/_align_tracks: rejected)
  _grow (degree growth)                                       ← C action "degree"
  decide_structure (raw_evidence − Occam)                     ← L2b occam(); L1a/L1b free_modes candidates
  regroup / _merge_tracks / screen_samples                    ← L2b thresholds (P_CONCENTRATED, LOG_BF_STRONG)
  recursion
  depth-0 cleanup: kappa_support, complex rerun, raw_subset,
     conjugate_closure, refine (support_path, refine_raw,
     split_quadratics, _refine_alternatives)                  ← L1a(i) residual search → refine(candidates=)
  bootstrap_intervals (grid)                                  ← L2c scale; replaced by L1a(iii)
  split_layer (coef_draws)                                    ← L2c scale for weights
  LoopResult                                                  ← V0 (validate.py) → V1 → C; L6 reads here
```

---

## 8. Failure modes per pipeline phase: detector and fixer

D = deterministic detector, V1 = learned combiner, OOD = out-of-distribution score, C = controller action. A "—" in the fixer column means "report only; no method can fix it (theory floor)".

| phase | failure mode | symptom | detector | fixer | theory |
|---|---|---|---|---|---|
| 0 data / model class | nonlinear PDE | κ-coupling, amplitude-dependent λ | V0.8, OOD | — (out of scope): MISFIT + reason | R2-T6 (linearity) |
| 0 | variable coefficients | λ(κ) drifts across cells or t-windows | V0.7, V0.6 | — (out of scope); subdomain report | Weyl algebra (parked), C12-T1′ |
| 0 | fractional / non-polynomial symbol | evidence keeps rising with degree | V0.6 | — : UNDECIDED "no finite degree" | CONV-T5 (m(δ) → ∞) |
| 0 | two laws in two regions | per-cell posteriors disagree | V0.7 | subdomain report (v2.9.4) | T1, C12-T1′ |
| 0 | non-simply-connected region | — | by construction (rectangles) | — | T1, C12-P10 |
| 0 | correlated / non-Gaussian noise | non-white residuals | V0.5 | coloured-noise candidates (C) | T36, T37 |
| 0 | outliers | heavy-tailed residuals | V0.5, V0.12 | robust (outlier-bin mixture exists) | T45 |
| 0 | too few κ per factor | margin < 0 | V0.2 | — : ID-KER | T13, T30, T40, T41 |
| 0 | single exponential per factor | one |κ| | V0.2 | — : ID-KER (lowest-degree factor printed) | T41, ATTACK-9 |
| 0 | κ above sampling Nyquist (aliasing) | modes at wrong κ | V0.1 (null mismatch), design check | — : report | — (empirical) |
| 0 | information absent (high κ below noise) | P0.1 oracle | P0.1, V0.1 | — : ID-KER/UNDECIDED (correct-abstain) | T13, DICT-A-iii |
| 1 GP | high-κ shrinkage (posterior filter) | raw residual energy at high κ | V0.1 | L1a(i), L1a(ii), L0, L1b | T35, T44 |
| 1 | ML-II overconfidence | u-coverage < nominal | PIT / coverage (exists) | Laplace-IS / NUTS (exists) | McLeod–Simpson (RESEARCH) |
| 1 | GP-mean artefact decay (fake τ + c) | spurious κ-independent factor | V0.3 | raw evidence (exists) | T39, T44 |
| 1 | stationary-kernel prior mismatch | fast decays absent from all samples | V0.1 + P0.1 "lost by GP" | L1a(ii) | R2-T6 |
| 1 | correlated posterior errors | BIC overfit | — (handled) | GLS `BinNoise` (exists) | T36, T37 |
| 2 modes | pencil λ bias at low SNR | λ off by > CRB | refine evidence gain | VarPro (exists), L0 | v2.9.1, T10 |
| 2 | wrong pencil order / merged exponentials | outlier modes | BIC per bin (exists) | L0 seeds | T10 (P2-Q3) |
| 2 | leakage on non-periodic cells | spurious κ | domain extractor | kernelfit (exists) | T32 |
| 2 | snr cut drops weak modes | missing κ | V0.2 margin | snr_min (L2d global) | — |
| 3 structfit | degree / dictionary too low | structured residual, saturating growth | V0.6, V0.13 | `_grow` (C) | II-C1, T23 |
| 3 | local optimum of the alternating fit | samples disagree | V0.4 | restarts, screening (T48), C | T48 |
| 3 | spurious factor (κ-independent, m = 2) | low inclusion, small evidence gap | V0.3 | raw_subset, `_refine_alternatives` | T39, T40, T46, T47 |
| 3 | equivalent dx choices | split structure mass | V0.3 (entropy) | — : report the posterior | T26 |
| 3 | unsplit reducible factor | square discriminant | V0.9 | split_quadratics (C) | T3, C12-P2/P3 |
| 3 | near-reducible irreducible | two damped transports vs a telegraph | V0.9 | merge-into-product candidate (exists) | T49 |
| 3 | real field, factor reducible only over C | no conjugate pair | V0.3 | complex rerun (exists) | T42, C12-T1 |
| 3 | shared κ = 0 mode | n_shared > 0 | core | min-norm split (exists) | T2, T7 |
| 3 | repeated factor Q² | confluent wins | V0.11 | — : UNDECIDED | T24 |
| 4 pooling | label switching | mixed tracks | Hungarian (exists) | — | S-AGG |
| 4 | DP over-counts k | spurious tiny clusters | finite-k BIC (exists) | — | T25, T27 |
| 4 | multimodal posterior over structures | entropy high, samples split | V0.3, V0.4 | more samples (C); report | T18 |
| 5 decider | miscalibrated Occam / prior | reliability off | L2a | L2b | CONV-T5 |
| 5 | interpolating (inadmissible) factor | equations ≤ unknowns | V0.2 | admissibility rule (exists) | T40, T46 |
| 5 | structure scored with biased coefficients | wrong choice reversed by refinement | V0.3 after refine | `_refine_alternatives` (local, T51) | — (empirical) |
| 6 regroup / recursion | spurious child factors | children not distinct | `_distinct` (exists) | — | — |
| 6 | missed recursion (unsplit group) | ρ, c_F high | ρ̄/c̄_F dists | — | T22, T12 |
| 7 split layer | weight undercoverage | SBC ranks | L2a | `coef_draws` (local), L2c | T5, T38 |
| 7 | inseparable weights (γ_N small) | wide intervals | V0.10 | — : report the floor | T5, T6 (P2-T4) |
| 7 | τ² empirical-Bayes edge | τ² at a grid bound | diagnostic | grid range (L2d) | T38 |
| 8 bootstrap | intervals conditional on the selected structure | undercoverage on grids | L2a | L1a(iii), L2c | T50 |
| 8 | grid bootstrap overwrites refined intervals | inconsistent intervals | code review | L1a(iii) | — |
| 9 refine_raw | support path stops early / drops a real term | evidence lower than the full support | V0.3 | path rule (local fix), C | — |
| 9 | Laplace interval inaccurate (non-Gaussian) | SBC | L2a | bootstrap / L2c | T12 |
| 10 domain | γ floor violated in small cells | huge component errors | γ_N | stop rule (exists) | T33, T5 |
| 11 output | confident wrong label | false-FIT-COMPATIBLE | P0.2 metric | everything above; abstain | T17, rule 5 |
| all | controller search inflates evidence | null false-positive ↑ | forking-paths test (§4 C) | honesty rule, data fission | — (statistics) |
| all | learned layer OOD | OOD score high | V1 OOD | layer output suppressed | — |

---

## 9. Acceptance protocol common to all layers

1. **Regression:** the switch off reproduces the run-6 jsonl exactly (the refine-pass version once committed).
2. **LOFO:** train and select on 4 of the families F1–F5, test on the 5th. Families are defined by **factor type**, and a held-out factor type is also removed from the products (F4), otherwise F4 leaks it; also hold out a degree, the noise colour and the density. Report in-family and LOFO side by side. **A layer that helps only in-family is rejected.**
3. **Nulls:** single-factor data must give no extra factor; pure noise must give UNDECIDED / MISFIT; data from a held-out injected failure must not be labelled FIT-COMPATIBLE.
4. **Calibration:** SBC rank histograms and TARP per family; coverage within ±5 % of nominal; reliability ECE of the structure probabilities.
5. **Benchmark:** right-set, exact structure, coefficient error, weight error, correct-abstain, false-confident, runtime. Against off and against the best SINDy variant (PySINDy 2.1.0, MIT).
6. **Audit:** `experiment-audit` and `result-to-claim` skills, with a fresh-context subagent reviewer, before any claim.

---

## 10. Library and model catalogue (verified by the research pass unless marked)

| name | URL | version (date) | licence | framework | role here | verdict |
|---|---|---|---|---|---|---|
| GPyTorch | [cornellius-gp/gpytorch](https://github.com/cornellius-gp/gpytorch) | 1.15.2 (2026-02-28) | MIT | PyTorch | spectral-mixture / custom EP kernels (L1a(ii)) | adopt (installed) |
| EPGP / S-EPGP | [haerski/EPGP](https://github.com/haerski/EPGP) | no release (20 commits) | MIT | notebooks | reference for learned spectral points on a variety | adapt (re-implement, as `interp/epgp.py`) |
| LODE-GPs | [ABesginow/LODE-GPs](https://github.com/ABesginow/LODE-GPs) | — | MIT | Sage + GPyTorch | Smith-form kernels (ODE only) | ignore (reference) |
| KBASS | [long-da/KBASS](https://github.com/long-da/KBASS) | no release | MIT | JAX | Kronecker GP + spike-and-slab discovery | baseline; idea for grid GP |
| FINUFFT | [flatironinstitute/finufft](https://github.com/flatironinstitute/finufft) | 2.5.1 (date unverified) | Apache-2.0 | C++/Python | type-3 NUFFT on scattered (t, x) (L1a(i), V0.1) | adopt |
| astropy LombScargle | [astropy](https://github.com/astropy/astropy) | 8.0.2 | BSD-3 | numpy | 1-D sanity check | baseline |
| PyTorch + Lightning | pytorch.org | (installed) | BSD-3 / Apache-2.0 | — | L0, L1b training | adopt |
| zuko | [probabilists/zuko](https://github.com/probabilists/zuko) | 1.6.0 (2026-03-10) | MIT | PyTorch | flows for L1b / L6 | adopt if L1b |
| nflows | — | unverified, believed unmaintained | MIT | PyTorch | — | ignore (use zuko) |
| sbi | [sbi-dev/sbi](https://github.com/sbi-dev/sbi) | 0.27.0 (2026-08-04) | Apache-2.0 | PyTorch | NPE/NRE/BNRE, SBC, TARP, L-C2ST (diagnostics from memory) | adopt for L2a diagnostics; L6 deferred |
| BayesFlow | [bayesflow-org/bayesflow](https://github.com/bayesflow-org/bayesflow) | 2.1.0 (2026-10-23) | MIT | Keras 3 | amortised model comparison; misspecification MMD | alternative to sbi for L6 |
| swyft / lampe | — | 0.4.5 (2023) / 0.9.0 (2024) | MIT | PyTorch | — | ignore (dormant) |
| MAPIE | [scikit-learn-contrib/MAPIE](https://github.com/scikit-learn-contrib/MAPIE) | 1.6.0 (2026-10-19) | BSD-3 | sklearn | Mondrian / CQR / conformal risk control (L2c, V1) | adopt |
| crepes | [henrikbostrom/crepes](https://github.com/henrikbostrom/crepes) | 0.9.1 (2026-06-12) | BSD-3 | numpy | conformal predictive systems | alternative |
| scikit-learn | — | 1.9.1 (installed) | BSD-3 | — | isotonic, HGB with `monotonic_cst`, GBM | adopt |
| LightGBM | microsoft/LightGBM | (unverified) | MIT | — | monotone GBM (L2c, V1) | adopt |
| tensorflow-lattice | — | 2.1.1 (2024-07-30) | Apache-2.0 | TF | lattice models | reject (stale, TF dependency) |
| Ax / BoTorch | facebook/Ax, pytorch/botorch | 1.3.1 / 0.18.1 (2026-06) | MIT | PyTorch | offline multi-objective BO (L2d) | adopt offline only |
| SMAC3 | [automl/SMAC3](https://github.com/automl/SMAC3) | 2.4.1 (2026-09-10) | BSD-3 | Python | offline configuration | alternative to Ax |
| NumPyro / PyMC | — | 0.22 (installed) | Apache-2.0 | JAX | hierarchical EB of the Occam prior (L2b) | adopt |
| PySINDy | [dynamicslab/pysindy](https://github.com/dynamicslab/pysindy) | 2.1.0 (2026-01-08) | MIT | numpy | Weak / Ensemble / SBR baselines | baseline (installed) |
| neuraloperator | neuraloperator/neuraloperator | 2.0.0 (2025-10-22) | MIT | PyTorch | FNO etc. | reject for this task |
| PDEBench | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) | code MIT (data licence unverified) | MIT | PyTorch | 1-D advection/diffusion as external test data | baseline data only |
| Poseidon | [HF camlab-ethz/Poseidon-B](https://huggingface.co/camlab-ethz/Poseidon-B) | — | CC-BY-NC-4.0 | PyTorch | 2-D foundation model | reject (licence, domain) |
| DPOT, MPP, UPS, The Well | (see §L1b) | — | various (DPOT unverified) | — | 2-D/3-D gridded | reject |
| PROSE-PDE | [arXiv:2404.12355](https://arxiv.org/abs/2404.12355) | — | unverified | PyTorch | symbolic + solution, 1-D gridded | ignore (proposal at most) |
| ICON | [LiuYangMage/in-context-operator-networks](https://github.com/LiuYangMage/in-context-operator-networks) | — | unverified | JAX | in-context operators, no operator output | ignore |
| sda (score-based DA) | [francois-rozet/sda](https://github.com/francois-rozet/sda) | — | MIT | PyTorch/JAX | diffusion prior for fields | reject (circular prior) |
| DiffusionPDE | [arXiv:2406.17763](https://arxiv.org/abs/2406.17763) | — | unverified | PyTorch | sparse reconstruction with a known PDE | reject |
| DeepFreq (template for L0) | Izacard et al. 2019 (m) | — | check | PyTorch | learned line-spectrum estimator | adapt (idea) |

Not verified: the licences of DPOT, DiffusionPDE, ICON and the PDEBench data; the finufft and astropy release dates; the PySINDy SBR optimizer details; whether `sbi.diagnostics` includes TARP and L-C2ST; the DeepFreq arXiv id. A "SymPDE" paper could not be identified.

---

## 11. Proposed additions for MAIN to merge (add-only)

**THEORY_TO_ALGO.md, §7 Phase 4 (proposed rows).** Under CLAUDE.md rule 7 only DIMOSTRATO or verified CON-FONTE results are foundations. T53, T55 (the decision-theory part) and T56 are therefore marked **heuristic / standard statistics, not theory rows**; MAIN may keep them in a separate "heuristics" list.

| # | result (status) | what it says | decision |
|---|---|---|---|
| T52 | R2-T6 (CON-FONTE) | every in-scope field is, per κ, a finite sum of damped exponentials | learned per-bin seeds (L0) are trained on generic exponential sums, not on PDEs: PDE-family-agnostic by construction |
| T53 | heuristic: equivalent kernel (R&W ch. 7), asymptotic, stationary kernel | GP mean ≈ a low-pass filter S/(S + σ²/ρ); samples refill the stopband with prior-shaped noise | no deconvolution of the GP; high-κ recovery only from raw-data parametric search with a look-elsewhere threshold (L1a) |
| T54 | CONV-T5 (DIMOSTRATO) | Ann(u) = 0 ⇒ the selected degree m(δ) → ∞ as δ → 0 | the selected degree's trend across a noise-degradation sweep is an out-of-class *flag* (V0.6), never a label from one dataset |
| T55 | CONV-T5 + decision theory (standard) | no data-free threshold; thresholds are prior-relative | calibrate the structure probabilities and the Occam prior on a declared simulator prior; derive thresholds from a stated loss (L2b) |
| T56 | heuristic, statistics (forking paths; data fission, Leiner et al. 2023) | search with data-dependent choices inflates the evidence | honesty rule: declared candidate space and fixed likelihood and prior; equal refine budget; report the missing mass; a held-out split fixed before the run (fission only with known Σ) |
| T57 | R1-P9, P2-P4 (DIMOSTRATO), CONV-D1 (DIMOSTRATO) | analytic features only; infinite ambiguity in 1+d for non-comaximal factors | no learned grouping encoder; at most a learned cost inside Hungarian matching, later |
| T58 | C3-T4, R4-T4 + oracle CRB (empirical, P0) | below the information limit no method recovers a mode | the benchmark scores correct abstention; a learned layer is never credited for answers below the oracle limit |

**RESEARCH.md, `## S-PHASE4-PLAN — 2026-10-29`:** the §10 table (verdicts adopt / adapt / baseline / ignore / reject as above), plus the papers cited in §4.

**Plan, a v2.13 section (proposed, add-only):** "Phase 4 order = §6 of `analysis/PHASE4_ML_PLAN.md`. P0 (oracle information, abstention scoring, simulator families) comes before any learned layer. The honesty rule (T56) governs the controller."

---

## 12. Review record (fresh-context adversarial review, applied)

A fresh-context reviewer attacked the first draft. Each point it raised, and how it was resolved:
1. **Fission applied after the search.** Fixed: the split is fixed before the run, and fission is allowed only with a known Σ (§4 C).
2. **Honesty-rule gaps.**
   - Visited-set renormalisation and restart count can inflate P(top): fixed by the declared space, equal budget and missing-mass term.
   - The noise-model switch contradicted the rule: both noise models are now always candidates.
   - The importance-weight claim was wrong: dropped (§0, L1b).
3. **False e-value / anytime-validity claim.** Removed; one pre-specified held-out comparison, with universal inference as an option.
4. **Look-elsewhere problem in the L1a scan.** Threshold from the null distribution of the maximum.
5. **V0 p-values are not uniform; B too small; V1 budget missing V0.** Double-bootstrap / conformal calibration, an omnibus statistic, B ≥ 200, and the budget re-done.
6. **T53 misstated (mean vs samples, non-stationary kernel, rule 7).** Restated; T53, T55 and T56 marked heuristic.
7. **SNR estimate overreach; circular "absent" criterion.** Caveats added; "absent" defined from the expected Fisher information per branch, independently of the pipeline.
8. **L2b conflated the parameter-integration and structure-prior penalties.** Separated (g-prior scale + n-independent structure prior).
9. **Calibration data reuse, multi-label conformal, LOFO leakage through products.** Fixed by three-way splits, conformal risk control, conditional-on-selection coverage, and factor-type families removed from products.
10. **V0.6 misread CONV-T5 (the limit δ → 0, not a fixed-δ curve).** Restated as a noise-sweep trend flag.
11. **(Lesser) L0 "only adds basins".** L0 is now under the null gate too.

## Appendix A — method constants, classified (from the code, `loop.py` unless noted)

- **Likelihood-defining (global; L2d tunes at most 4–5 of them).**
  - CAP = 3 (L31; structfit cap = 3.0)
  - z = 3 (L206, L766; share_z 3.0 structfit:406)
  - EPS_GRID (L287)
  - the Occam term ½p log n (L405/409/1255; refine_raw:174)
  - snr_min (bayes_split:93 default 3; split layer 0.5 L466; structfit:129 3)
  - JITTER = 1e-3 (structfit:41)
  - TAU2_GRID (bayes_split:32)
  - the GP hyperpriors (gp.py:116-124)
  - `_raw_kmax` (L306)
  - the robust-scale 0.455 (L785; structfit:281)
  - outlier z² ≥ 9s² (structfit:444)
  - confluent Δ = 2 log nobs (structfit:372)
  - BIC penalty per bin 4r log(2nt) (structfit:165)
- **Decision thresholds (from calibrated probabilities + a loss, L2b; not tuned).**
  - P_CONCENTRATED = 0.9 (L30)
  - LOG_BF_STRONG = log 150 (L592)
  - MISFIT + ID-KER mass 0.5 (L1064)
  - p_more ≥ 0.5 (L1195)
  - 2·SE held-out (L1073, 1100)
  - outlier_frac_misfit 0.5 (structfit:406)
  - recursion "disjoint 90 %" rule
  - GAMMA_FLOOR 0.02, TIE_BIC 2 (quadtree:29-30; domain report only)
- **Computational (a cost–accuracy curve; the controller may raise them).**
  - S_LOOP = 8, BOOT = 16 (bench_e2e:44-45)
  - W_DRAWS = 16 (L416)
  - split ndraw = 200 (L451)
  - decider top = 5, ndraw = 2 (L341, 384)
  - ALT_TOP = 2 (L974)
  - split_quadratics ndraw = 400 (L898)
  - inits 8 + 2, iters 30 (structfit:238)
  - DP settings (aggregate:216)
  - GP S, H (gp.py:438)
  - max_full = 6, L-BFGS maxiter 200 (refine_raw:157, 114)
  - max_depth = 2 (L1044)
  - DX_LIMIT 8, M_LIMIT 4 (L29)
- **Numerical tolerances (not tuned; tested for insensitivity only).** SVD/QR keeps, jitters, clips and imaginary-part tolerances.
