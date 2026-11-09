# S-PHASE4-ML — REPORT

Session S-PHASE4-ML, 2026-10-29 (cloud). It covers the learned layers of `analysis/PHASE4_ML_PLAN.md`. The deterministic layers (P0, V0, L1a, C) belong to the local session. Branch `claude/relaxed-mendel-k3gpne`, PR #1.

## 1. What was built

All of it is off by default, and off = today. A golden test checks that off reproduces `origin/main`'s `extract_modes_ic` bit-for-bit on 20 configurations.

| layer | module | status |
|---|---|---|
| L0 hook | `core/structfit.extract_modes_ic(seeds=)`, `SEED_PROVIDER` | done. Honesty rule enforced: seeds only inside r0..r0+extra, one per order, equal starts per order |
| L0 data | `learned/expsum.py` (generic damped exponential sums; white + AR(1) noise) | done |
| L0 net | `learned/expseeds.py` (damping-frequency heatmap + count head; focal loss; cached provider) | **gate failed** (E12, E15): stays off |
| L2b | `learned/calibrate.ProbabilityCalibrator`, `VennAbersCalibrator`, `loss_threshold` | **gate failed** under LOFO (E14): stays off |
| L2c | `learned/calibrate.IntervalInflator` (monotone GBM + Mondrian conformal) | **gate passed** on held-out families (E14) |
| V1 | `learned/validator.Validator` (one-vs-rest GBM, conformal risk control, OOD gate with shrinkage) | **gate failed** under LOFO (E14): stays off |
| C order | `learned/remedy.RemedyTable` (Beta lower bound per remedy) | done; needs the controller's offline runs |
| adapters | `learned/features.py` (`LoopResult` → rows, no identifiers) | done |
| L1b | — | not built: gated by P0.1 ("present but missed" after L1a), which is the other session's |
| L6 | — | deferred (PHASE4 §L6) |
| L5 | — | rejected (PHASE4 §L5) |

Tests: `tests/test_learned.py`.

## 2. L0 — learned seeds (E12)

**Verdict: gate failed, L0 stays off.** The code and hook are kept, and the reason is measured, not guessed.

- **E12 v1** (20k steps; 1500 held-out sums; three arms through the exact per-bin selection):
  - pencil + BIC: order accuracy 0.848;
  - the equal-start control: 0.847;
  - pencil + BIC + L0: 0.847.
  - |dλ|/CRB is the same in every arm, and so is the null over-order rate (0.018).
  - A diagnosis showed that the MSE heatmap had collapsed: peak heights 0.004–0.09, so almost no proposals came out. Fixed with a CenterNet focal loss. The count head was already good: 0.77 accuracy vs 0.35 for the pencil's rank rule.
- **E15, the upper bound** (287 white-noise sums):

| arm | order acc | \|dλ\|/CRB median | p90 | merged pairs acc |
|---|---|---|---|---|
| control (equal starts) | 0.829 | 0.94 | 4.41 | 0.167 |
| ESPIRA (AAA on the DFT) | 0.826 | 0.98 | 4.28 | 0.167 |
| **oracle: the true poles as seeds** | 0.829 | 0.93 | 4.40 | 0.167 |

  - Even perfect seeds do not change the outcome. After VarPro the per-bin step is CRB-efficient, and the merged pairs it misses are information-limited under the BIC order rule.
  - So the focal-loss L0 was not retrained to completion: no seed provider can pass the gate here.
  - This is the empirical answer to T10 / P2-Q3 *for this sampling regime* (nt = 32–64 uniform). L0 could still matter for much shorter or non-uniform records, which are not in scope now.

## 3. L2b / L2c / V1 on held-out families (E13 → E14)

Corpus E13: 126 loop runs on grids with a stand-in posterior (`fake_posterior`, S = 4), at noise 0.1 / 1 / 5 %, 2 seeds:
- the 10 v1 CASES (train families);
- the 11 GENERAL_CASES (held out; plan v2.13).

| layer | protocol | off | on | gate |
|---|---|---|---|---|
| **L2c** monotone inflation + Mondrian conformal | fit/calibrate on v1 families (grouped); test on the 11 held-out families | coverage of nominal 90 % coefficient intervals 0.756 | **0.923** (median width × 1.53) | **pass** (±5 % of nominal) |
| L2b isotonic | LOFO over all 21 families | ECE 0.141, Brier 0.140 | ECE 0.214, Brier 0.169 | **fail**: worse out-of-family |
| L2b inductive Venn–Abers | LOFO | ECE 0.141 | ECE 0.242, Brier 0.145 | **fail** |
| V1 "wrong factor set" flag | LOFO | — | catches 0.39 of 18 wrong sets at a 0.08 false-flag rate; OOD gate never triggered | **fail**: missed rate 0.61 ≫ α = 0.1 |

Reading:
- The raw P(top) is already better calibrated out-of-family than any map fitted on other families. Risk control's guarantee needs exchangeability, which breaks across families, exactly as PHASE4 §L2 warned. L2b and V1 stay off until P0.3's random families give an in-prior corpus.
- L2c passes because its features are dimensionless and theory-signed (here only the mode-count margin, T13 / T40; κ_Vand, SNR and disagreement are still NaN), and its target is a ratio (z) that transfers across families.
- Caveats:
  - grid data only;
  - a stand-in posterior;
  - 156 held-out coefficients;
  - coverage is conditional on the factor being matched (PHASE4 §L2c).

## 4. Review record
A fresh-context adversarial review found 9 defects, all fixed in commit "review fixes":
- the seed hook widened the order range and gave seeded orders extra starts;
- seeds-off was not bit-for-bit for short series, and CRLF line endings were lost;
- L0 could not represent close pairs;
- V1 failed on all-NaN feature columns;
- grouped splits could be empty;
- feature names did not match;
- the pure-noise null was vacuous;
- the CRB was misused under AR(1) noise.

It also checked, and found correct: the conformal quantile, the risk-control search, the conformal p-value, the isotonic arguments, `monotonic_cst`, and the s = λT convention.

## 5. Proposed rows for MAIN to merge (THEORY_TO_ALGO, add-only)

| # | result (status) | what it says | decision |
|---|---|---|---|
| T52 | no theory: empirical (E15) | with VarPro and the BIC order rule, seeds (learned L0, ESPIRA, even the true poles) do not change the per-bin result on uniform records of 32–64 samples; the step is CRB-efficient, and its misses are information-limited | T10 / P2-Q3 needs no learned estimator in this regime; L0 stays off; the gains are upstream (raw-data scan, interpolation prior) |
| T53 | T44 + raw-data CRB (E16) | heat at 400 pts / 5 %: a raw-data damped matched filter + VarPro reaches the raw CRB at κ = 1–4 (1.5–3× smaller error than the GP path at κ ≤ 3) and recovers κ = 4, which the GP path misses; κ ≥ 5 has amp/σ < 0.4 (absent) | adopt the raw residual scan (L1a(i)) as the first deterministic layer; κ ≥ 5 is ID-KER / UNDECIDED territory |
| T54 | no theory: empirical (E14) | out-of-family, the raw structure probability is better calibrated than isotonic or Venn–Abers maps fitted on other families; a monotone, theory-feature interval inflation transfers (coverage 0.756 → 0.923) | switch on L2c only; L2b and V1 wait for an in-prior corpus |

## 6. Open (for MAIN / the local session)
- Wire L2c into `bootstrap_intervals` / `split_layer`, and V1 into `validate.py`, once V0 and P0.3 are on main. The adapters (`learned/features.py`) need κ_Vand, per-factor SNR and sample disagreement exported by the deterministic layer.
- SAMP (Segman, Amar, Talmon, arXiv:2502.17047), a structure-aware matrix pencil order detector, is a deterministic candidate for the order step and a baseline for L0.

## 7. Libraries and algorithms as extra layers
See `LAYER_CANDIDATES.md`. The two largest measured or expected gains are both deterministic and belong to the local session:
- the FINUFFT / Lomb–Scargle raw-data scan (E16);
- a spectral-mixture / S-EPGP interpolation prior.

On the ML side, L2c is the one layer that passed its gate.

## 8. Final verification (close of session)
- `tests/test_learned.py`: 24 passed.
- Full suite on this branch: 124 passed, 1 failed, 6 errors.
  - The 6 errors in `tests/test_aggregate_cluster.py` (IndexError in `aggregate.py:198`) reproduce on a clean `origin/main` (6db4ec3) worktree, so they come from main, not from this branch.
  - The 1 failure, `test_baselines_bench::test_run_method_row[sbr_sindy]`, is environmental: the pysindy installed in the cloud container has no `SBR`.
- Seeds off is bit-for-bit `origin/main` (golden test).
- Download everything: <https://github.com/FlavioApric/ML-PDE-fit/archive/refs/heads/claude/relaxed-mendel-k3gpne.zip>, or run `launch_phase4_ml.bat`, which fetches into `D:\wt-phase4-ml`.
