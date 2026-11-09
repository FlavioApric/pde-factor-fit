# S-PHASE4-ML — external libraries, repos and algorithms as extra layers: vetted shortlist

Goal: find what can be added as an extra layer within PHASE4_ML_PLAN's rules (proposal, calibration or flag; off = today) and gives a **significant** improvement. A candidate is listed only with a stated reason and, where it could be measured here, a measurement on this repo.

## 0. The measured fact that orders the list

**E15 (seed upper bound).** On held-out exponential sums, through the exact `extract_modes_ic` selection, one bin at a time:

| arm | order acc | \|dλ\|/CRB median | p90 | merged pairs acc |
|---|---|---|---|---|
| control (equal starts, no seeds) | 0.829 | 0.94 | 4.41 | 0.167 |
| ESPIRA (AAA on the DFT) | 0.826 | 0.98 | 4.28 | 0.167 |
| **oracle (true poles as seeds)** | 0.829 | 0.93 | 4.40 | 0.167 |

- Even the true poles do not improve the per-bin step. After VarPro the step is already CRB-efficient (median ≈ 0.94 of the CRB).
- The merged pairs that fail are information-limited under the order IC; that is the PHASE4 P0 "absent" class.
- Hence **no seed or proposal method can give a significant gain here**: not L0 (learned, E12), not ESPIRA, not SAMP, not DeepFreq-style networks. The gains must come from:
  - (a) information the GP throws away (high κ, 400 pts at 5 %);
  - (b) the structure decision;
  - (c) calibration of what is reported.

The shortlist below is ranked by that.

## 1. Shortlist, ranked by expected gain on the documented failures (PHASE4 §1)

| rank | candidate | type | layer / insertion | expected gain | evidence | owner |
|---|---|---|---|---|---|---|
| 1 | **FINUFFT** type-3 NUFFT ([flatironinstitute/finufft](https://github.com/flatironinstitute/finufft), Apache-2.0, `pip install finufft`) + generalised Lomb–Scargle (astropy `LombScargle`, BSD-3) | library | L1a(i) raw-residual mode scan on scattered data, `loop.run_loop` before refine | **high**: the main remaining failure (heat/TPD 400 pts at 5 %) has its information in the raw data (κ ≤ 4: matched-filter SNR ≈ 26 at κ = 3), and the GP loses it (T44). NUFFT makes the (κ, λ) scan over all raw points O(N log N) | PHASE4 §1 estimate; T44 | deterministic: local session |
| 2 | **Spectral-mixture / S-EPGP interpolation prior** (GPyTorch `SpectralMixtureKernel`, MIT; [haerski/EPGP](https://github.com/haerski/EPGP), MIT; GP-HM, Fang et al. ICLR 2024, [arXiv:2311.04465](https://arxiv.org/abs/2311.04465), code on GitHub) | library + algorithm | L1a(ii) a GP prior option that does not shrink fast decays (a log-domain mixture-weight prior prunes excess frequencies; Kronecker structure on grids) | **high on 400 pts**: removes the stationary-kernel prior mismatch that gives fast decays no mass | R2-T6 / T34; GP-HM reports high-frequency recovery | deterministic prior: local session; the hyperprior is learnable (L2d) |
| 3 | **Simulation-based calibration of parameter intervals under approximate Bayes** ([arXiv:2407.04659](https://arxiv.org/abs/2407.04659)) | algorithm | L2c alternative to conformal for **coefficient and weight intervals**: corrects marginal posterior intervals with asymptotic coverage guarantees. Conformal covers predictions, not parameters | **medium–high** on the open weight undercoverage (w_cover90 0.50 in 3 cells) once the `coef_draws` model fix is in | paper. For Gaussian intervals, re-choosing the nominal level by simulation is the same as one width factor per quantity; that is `IntervalInflator`'s pooled conformal quantile (regime_feature=None), so E14's L2c arm already measures this correction | **ML (this session)**: covered by `IntervalInflator`, E14 |
| 4 | **Inductive Venn–Abers** (Vovk, Petej, Fedorova 2015; PyPI `venn-abers` does not build here, so it is reimplemented in `learned/calibrate.VennAbersCalibrator`) | algorithm | L2b, P(top structure) → P(right set) | **medium**: built for small calibration sets (ours: ~10² runs), where one isotonic map overfits | E14 compares raw / isotonic / Venn–Abers on held-out families | **ML (this session)**: implemented, tested |
| 5 | **Conformal risk control, multi-label** (MAPIE `risk_control`, BSD-3) and **conformal outlier p-values** ([nonconform](https://proceedings.mlr.press/v329/hennhofer26a.html), [msesia/conditional-conformal-pvalues](https://github.com/msesia/conditional-conformal-pvalues)) | library | V1 report set, OOD gate | **medium** (safety, not accuracy): bounds the missed-failure rate in-prior and withholds V1 off-prior | implemented in `learned/validator.py`; MAPIE and nonconform are the cross-checks | **ML (this session)** |
| 6 | **CP4SBI** local conformal calibration of credible sets ([arXiv:2508.17077](https://arxiv.org/abs/2508.17077)) + **sbi** 0.27 (Apache-2.0) / **BayesFlow** 2.1 (MIT) | library + algorithm | L6 amortised cross-check, made locally calibrated | low now (L6 is deferred); high only if L6 is built | paper | ML, deferred |
| 7 | **Weak-form SINDy for PDEs** (WSINDy, Messenger & Bortz 2021, [MathBioCU/WSINDy_PDE](https://github.com/MathBioCU/WSINDy_PDE); `pysindy.WeakPDELibrary`, MIT) | library | a **structure-proposal provider** to the decider (its candidate term sets join the declared enumeration and are scored by raw evidence), and the strongest non-Bayesian baseline | low–medium: reported robust above 10 % noise on gridded data, but it needs a grid (so a GP first on scattered data) and gives no factor structure | paper | baseline: S-BASELINES-BENCH |
| 8 | **Robust low-rank Hankel recovery under spikes** (Xie, Liu, Mansour, Boufounos, ICASSP 2020, [MERL TR2020-052](https://merl.com/publications/TR2020-052)) | algorithm | outlier-robust per-bin fit (the T45 outlier-bin mixture already covers the bin level) | low: no outlier failure is in the census | paper, no code | — |
| 9 | **Reversible-jump / trans-dimensional samplers** (Eryn, [arXiv:2303.02164](https://arxiv.org/abs/2303.02164); non-reversible jump, Gagnon & Doucet) | library | an exact posterior over the number of exponentials per bin, instead of BIC | low: E15's oracle shows the order step is information-limited, so a better posterior over r changes the reported uncertainty, not the accuracy | E15 | — |

## 1b. Measured: rank 1 on the failure cell it targets (E16)

Heat, 400 scattered points, 5 % noise, 3 seeds. λ(κ) from today's GP path (`fit_gp` → `extract_modes_ic`, GLS) vs a raw-data matched-filter scan with joint VarPro on the scattered observations (the L1a(i) candidate):

| κ | true λ | raw scan median \|dλ\| | raw-data CRB | GP path median \|dλ\| (modes found) | amp/σ |
|---|---|---|---|---|---|
| 1 | −0.3 | 0.003 | 0.005 | 0.009 (3/3) | 35.7 |
| 2 | −1.2 | 0.022 | 0.024 | 0.033 (3/3) | 18.4 |
| 3 | −2.7 | 0.260 | 0.219 | 0.455 (3/3) | 6.8 |
| 4 | −4.8 | 1.437 | 1.375 | — (0/3) | 1.5 |
| 5 | −7.5 | 7.1 | 0.9 | — (0/3) | 0.2 |
| 6 | −10.8 | 7.3 | 5.3 | — (0/3) | 0.35 |

What this shows:
- The raw scan reaches the raw-data CRB at κ = 1–4. It is 1.5–3× more accurate than the GP path at κ ≤ 3, and it recovers a 4th wavenumber that the GP path never finds. That is one more equation per factor for the identifiability count (T13, T40).
- At κ ≥ 5 the information is absent (amp/σ < 0.4; the λ error is far above its scale). The correct output there is ID-KER / UNDECIDED, and no layer, learned or not, should "recover" it.
- This matches PHASE4 §1's estimate and confirms rank 1 as the largest available gain.

## 2. Measured and rejected as layers (no significant gain possible or measured)

| candidate | result | where |
|---|---|---|
| L0 learned seeds (Xie–Wakin–Tang / DeepFreq design, own PyTorch code) | v1 (MSE heatmap) identical to the equal-start control; the oracle upper bound (E15) shows no seed can help. **Gate failed: stays off.** The code and hook are kept for other sampling regimes (a much shorter nt, non-uniform t) | E12, E15 |
| ESPIRA ([arXiv:2106.15140](https://arxiv.org/abs/2106.15140), `scipy.interpolate.AAA`) | same as control | E15 |
| SAMP ([arXiv:2502.17047](https://arxiv.org/abs/2502.17047)) | not run; bounded by the E15 oracle (the order IC decides, and seeds cannot move it) | E15 |
| DeepFreq pretrained ([sreyas-mohan/DeepFreq](https://github.com/sreyas-mohan/DeepFreq)) | no licence, undamped only; bounded by E15 anyway | RESEARCH.md |
| Neural operators / PDE foundation models / diffusion priors | rejected in PHASE4 §L1b (prior hallucination, gridded, no UQ); nothing new found | PHASE4 |

## 3. Recommendation
1. **Local session (deterministic, biggest gain):** FINUFFT raw-residual scan (L1a(i)), then a spectral-mixture / S-EPGP prior option (L1a(ii)). These target the failure where the information exists and is lost.
2. **This session (ML):**
   - finish E14 on the corpus: isotonic vs Venn–Abers for L2b, monotone + conformal for L2c;
   - switch on whichever passes the held-out-family gate (PHASE4 §9).
3. **Close L0** with the E15 bound, and record it in THEORY_TO_ALGO as the empirical answer to T10 / P2-Q3 *under the BIC order rule*.
