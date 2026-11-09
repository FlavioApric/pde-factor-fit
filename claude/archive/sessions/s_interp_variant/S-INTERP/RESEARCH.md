
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
