# S-PHASE4-ML — RESEARCH (prebuilt models and layers, 2026-10-29)

The question asked: does a prebuilt model or library already exist for each learned layer, and should it be reused?

## L0: learned exponential / pole estimation
| candidate | what it is | reuse? |
|---|---|---|
| DeepFreq — Izacard, Mohan, Fernandez-Granda, NeurIPS 2019, [arXiv:1906.00823](https://arxiv.org/abs/1906.00823), [github.com/sreyas-mohan/DeepFreq](https://github.com/sreyas-mohan/DeepFreq) | a frequency-representation CNN plus a counting module, pretrained weights (`.pth`), PyTorch | **Architecture only.** No licence file in the repository (so the code cannot be vendored), and it handles *undamped* sinusoids only: its weights do not apply to damped poles. |
| Xie, Wakin, Tang, "Data-driven parameter estimation of contaminated damped exponentials", Asilomar 2021, [IEEE 9723189](https://ieeexplore.ieee.org/document/9723189/) | a representation net from samples to a **2-D frequency–damping spectrum**, plus a counting net | **This is exactly L0's design** and is adopted as the template. No public code was found. Reimplemented in `learned/expseeds.py`. |
| SAMP, structure-aware matrix pencil — Segman, Amar, Talmon, [arXiv:2502.17047](https://arxiv.org/abs/2502.17047) (2025) | a deterministic model-order detector for damped exponentials; reported close to the CRB at low SNR and better than standard MP and the information criteria | **Not ML**, so it is out of scope for this session. Flagged for the local session as a deterministic competitor to L0 and as a baseline for e12. |
| Model-based NN for line spectra ([arXiv:2202.06485](https://arxiv.org/abs/2202.06485)); SignalNet ([arXiv:2106.05490](https://arxiv.org/abs/2106.05490)) | undamped lines | no |
| deep unfolding / learned ESPRIT | none found for pole estimation | — |

Conclusion: no licensed, pretrained model for damped complex exponentials exists. L0 is trained from scratch on generic exponential sums (`learned/expsum.py`), on CPU in this container.

## L2 / V1: calibration, risk control, OOD
| library | use | decision |
|---|---|---|
| scikit-learn `IsotonicRegression`, `HistGradientBoosting*` with `monotonic_cst` (BSD-3) | L2b isotonic map; L2c monotone inflation; V1 classifiers | **used** (already a dependency) |
| MAPIE ≥ 1.x `risk_control` (`PrecisionRecallController` / `MultiLabelClassificationController`, CRC/RCPS/LTT) (BSD-3), [docs](https://mapie.readthedocs.io/en/latest/api/risk-control/) | multi-label conformal risk control | equivalent; the CRC step is about 15 lines, implemented in `validator._risk_threshold` to avoid an API that changes between versions. MAPIE remains the cross-check |
| nonconform (Hennhöfer et al. 2026, PMLR v329), unquad, fcnd, msesia/conditional-conformal-pvalues | conformal outlier p-values | the OOD gate needs one p-value from one score, which is implemented directly; these are the references |
| crepes (BSD-3) | Mondrian conformal | implemented directly in `IntervalInflator.calibrate` |
| LightGBM (MIT) | faster GBM | optional; sklearn HGB is enough at 2–5 k runs |

## Not reused (agreeing with PHASE4 §L1b, L5, L6)
PDE foundation models, neural operators, diffusion priors and contrastive encoders: see PHASE4 §4 and §10. No new evidence was found that changes those verdicts.

Network note: arxiv.org and par.nsf.gov are outside this cloud session's allowed domains. The papers were checked through search snippets only, and the architecture details of Xie et al. are reconstructed from the abstract.
