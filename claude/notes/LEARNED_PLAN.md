# S-LEARNED — optional learned layers as calibration and optimisation: PLAN

Session **S-LEARNED**, 2026-10-29, working copy `D:\Larned layers` (own git repo, branch `learned-layers` cut from `phase4-ml`).
It implements the adopted parts of `analysis/PHASE4_ML_PLAN.md` (S-PHASE4-PLAN) and continues `sessions/S-PHASE4-ML` (the cloud session: L0, L2b, L2c, V1, remedy table, E12–E16).
It removes nothing from either. Phase A (this file) is planning only. Phase B starts after the parent session approves.

Status words: **build / re-gate / conditional / closed**. Theory IDs refer to THEORY_TO_ALGO (main copy, T1–T60) and the LEDGER. "No theory: empirical" means what it says.

---

## 0. What I read, and what it changes

Read:
- `piano di ricerca.md` (Context, §1.1–1.2, §1.5 ladder, §1.6 protocol);
- `PDEFactorML/CLAUDE.md`, the main plan `to-plan-use-the-groovy-chipmunk.md` (Phase 4, v2.9–v2.13);
- `analysis/PHASE4_ML_PLAN.md` (whole), `THEORY_TO_ALGO.md` (main copy, T1–T60);
- `sessions/S-PHASE4-ML/{REPORT, LAYER_CANDIDATES}.md` and `results/e14_calibration.md`;
- the code: `loop.py` (`run_loop` in full), `refine_raw.py`, `bayes_split.py`, `aggregate.py`, `core/structfit.py`, `learned/*`;
- from the main copy `D:\PDEFactorML` (read-only): `simulator.py`, `validate.py`, `analysis/exp/e13_random_pdes.py`, `benchmarks/out/e13_random.*`, and the skills `session-start`, `pdefactor-core`.

Rule 7 graph query: `graphify query` on the high-κ / identifiability topic returns only generic nodes. The decisions below rest on THEORY_TO_ALGO rows that already cite LEDGER status (R2-T6, T13/T40/T46, T44, T5/T6, CONV-T5). New rows are proposed in §8.

### 0.1 Measured facts the plan is built on (not re-litigated)

| fact | source | consequence here |
|---|---|---|
| Even the true poles as seeds do not improve the per-bin step (VarPro is CRB-efficient at nt = 32–64; misses are information-limited) | E15 | **L0 closed** for this regime; no seed work |
| A raw-data damped matched filter + VarPro reaches the raw CRB at κ = 1–4 (heat, 400 pts, 5 %) and recovers κ = 4, which the GP path never finds; κ ≥ 5 is absent (amp/σ < 0.4) | E16 | the **high-κ candidate-mode layer** has the largest measured gain; κ above the information limit must end as ID-KER/UNDECIDED |
| Monotone, theory-signed interval inflation + Mondrian conformal moves coefficient coverage 0.756 → 0.923 on held-out families | E14 | **L2c** is the one learned layer that passed; wire it in and re-gate on the new corpus |
| Out of family, the raw P(top) is better calibrated than isotonic or Venn–Abers maps; V1 catches 0.39 of wrong sets | E14 LOFO | L2b and V1 stay off unless an in-prior corpus reverses this (**re-gate only**) |
| E14 used grids, a stand-in posterior (`fake_posterior`) and the pre-v2.13 pipeline | E14 | every gate is re-run on the new corpus |

### 0.2 This copy is behind the main session (blocking for Phase B)

`D:\Larned layers\PDEFactorML` has the cloud branch's `learned/`, but **not** main's newer deterministic work, which exists only *uncommitted* in `D:\PDEFactorML`:
- `simulator.py` (families F1–F5) and `validate.py` (V0.1, V0.2, V0.3, V0.10, V0.13) are missing;
- `loop.py` (79 differing lines: V0.1-triggered growth `PRED_LOGP`, merge moves for any order pair, `MERGE_DX0`, grid FFT in `_grid_obs`);
- `refine_raw.py` (65 lines: the exact per-DFT-bin grid evidence `_grid_spectrum`);
- `core/structfit.py` (31 lines: `_branch_point`);
- `e13_random_pdes.py`, plus the tests `test_simulator.py`, `test_validate.py`, `test_refine_grid.py`, `test_general.py`.

The learned layers must sit on the pipeline the user actually runs, so step **B0** imports that state first (§5). Main's tree is still moving, so B0 takes a **dated snapshot** and records a sha256 per file in `sessions/LEARNED/SYNC.md`. Re-syncing later is a merge of those files only; the learned code touches `loop.py` only at the hook lines listed in §3.

---

## 1. Principles (binding for every layer)

1. **Off = today, bit-for-bit.** `run_loop(..., learned=None)` (the default) and `learned=Learned()` (all flags off) both reproduce the B0 snapshot exactly. This is checked by a golden test on stored outputs (factor strings, labels, intervals, evidence) from 6 draws.
2. **Propose, calibrate or flag; never decide.** A learned output is one of:
   - a candidate (mode, factor, structure) that the raw-data evidence − Occam then scores;
   - a global constant or interval scale fitted offline;
   - a report flag.

   Labels (FIT-COMPATIBLE / MISFIT / ID-KER(class) / UNDECIDED) come only from the deterministic evidence and the identifiability rules. "Law identified" is never printed.
3. **Fixed likelihood.** Nothing learned changes the noise model, the Occam rule or the structure prior per run. Constants that define the likelihood are global (L2d), fitted once and versioned.
4. **Monte Carlo, never linearisation.** Interval scales act on the Monte Carlo/Laplace draws themselves. Coefficient draws feeding the weight posterior (`coef_draws`) are scaled *before* `split_layer`, so the weights inherit the calibration by Monte Carlo.
5. **Switch-on gate** (§2.4): held-out simulated PDEs, leave-one-family-out (LOFO), equal or better calibration, clean nulls. A layer that fails stays off; its code, tests and the measured reason stay in the repo.
6. **Prior tag.** Every output that depends on the simulator prior carries `PRIOR_TAG` (`prior: sim-v2` for the new corpus).
7. **Grouping is by factors only.** No layer touches `aggregate`'s clustering or track matching (PHASE4 L5, T8/P2-P4).
8. **Scope:** linear, constant-coefficient, 1+1. Out-of-scope data (nonlinear, variable coefficients, fractional) appear only as *injected failures* for flags (V1), never as targets.

---

## 2. Common harness (built once in B0/B1, used by every gate)

### 2.1 Configuration: one dataclass, one line per layer
`src/pdefactor/learned/config.py`:
```python
@dataclass(frozen=True)
class Learned:
    intervals: str = "off"        # L2c: "off" | "coef" | "coef+weights"
    highk: str = "off"            # H0/H1: "off" | "scan" | "scan+net"
    constants: str = "default"    # L2d: "default" | "sim-v2" (global calibrated constants file)
    budget: bool = False          # LB: learned skip of expensive optional steps
    prob_calibration: bool = False  # L2b: calibrated P(top) in the report (never a label)
    validator: bool = False       # V1: learned failure flags + OOD score (report only)
    controller: bool = False      # C: targeted reruns under the honesty rule
OFF = Learned()
```
`run_loop` gets one keyword, `learned: Learned | None = None`. Each hook is `if learned and learned.<flag>: ...`. Model files live in `src/pdefactor/learned/models/` (versioned, with the corpus hash and `PRIOR_TAG`).

### 2.2 Simulator corpus (`analysis/exp/ll_corpus.py`)
Draws come from main's `simulator.random_pde` (F1–F5, exact dispersion checked), never from the named cases.

| corpus | design | runs | use |
|---|---|---|---|
| **G** grid | F1–F5 × seeds 100–135 × noise {1 %, 5 %}, one noisy grid (benchmark grid path, bootstrap B = 16) | 360 | every gate |
| **S** scattered | F1–F5 × seeds 200–211 × {400 pts @ 5 %, 2000 pts @ 1 %}, `fit_gp` posterior | 120 | H0/H1, L2c on GP samples |
| **N** nulls | (a) pure noise, 20 grids + 20 scattered sets; (b) single-factor F1/F3 draws are already "no extra factor" nulls | 40 + the single-factor runs | null gates |
| **I** injected failures (built in B6) | 6 injection types × 20: AR(1) noise in x, two laws in two time halves, fractional |ξ|^α symbol, weak nonlinearity ε u u_x (split-step), variable coefficient c(x)(1 + ε cos x) (split-step), κ above the time Nyquist | 120 | V1 / C only |

- **Splits, fixed now and never changed:** seeds 100–119 / 200–206 = *fit*; 120–127 / 207–208 = *calibrate*; 128–135 / 209–211 = *test*. LOFO: fit and calibrate on four families, test on the fifth. The named cases (`synthetic.CASES`, `GENERAL_CASES`) are an **external test only**, never fitted.
- **What each run stores:**
  - the truth;
  - main's `identifiable()` oracle per factor (truth-only, not circular);
  - the `LoopResult` summary and the V0 report;
  - per-coefficient (estimate, interval, true value), matched by `simulator.match`;
  - the weights and their intervals;
  - per-step timings and a per-step "changed the factor set" bit (for LB);
  - the final raw residual per κ bin (for H1).
- **Cost.** Grid pipeline runtime is 14 s (F1) to 875 s (F4) in main's E13 log. With 8 workers and a 1200 s cap per run (a timeout is recorded and treated identically in both arms), G takes ≈ 2–3 h, S ≈ 3 h (GP fits), and N and I ≈ 1–2 h. All of it runs in the background.

### 2.3 Metrics (extends main's E13 scoring)
- **Factor set:**
  - *right*: FIT-COMPATIBLE with the right set;
  - *correct-abstain*: ID-KER/UNDECIDED where the oracle says not identifiable;
  - *false-confident*: FIT-COMPATIBLE with a wrong set;
  - *wrong-abstain*.
- **Coefficients:** coefficient error (matched).
- **Calibration:**
  - coverage of 90 % coefficient and weight intervals, conditional on correct selection and reported with the selection rate;
  - SBC rank histograms (χ² against uniform);
  - interval score (Winkler);
  - ECE/Brier of P(top).
- **Cost:** runtime (median, p90).
- **Comparisons are paired by draw:**
  - exact McNemar for rates;
  - bootstrap over draws for coverage, error and runtime;
  - non-inferiority margin 0.02 on rates; coverage tolerance ±0.05 around nominal.

### 2.4 The gate (every layer)
A layer switches on only if all of these hold on the *test* split **and** on every LOFO fold:
1. **Primary target** improved (stated per layer), with a paired CI excluding 0.
2. **Right-set** ≥ off − 0.02, and **false-confident** ≤ off (paired).
3. **Calibration** equal or better:
   - |coverage − 0.90| not larger than off by more than 0.02;
   - within ±0.05 for any interval the layer touches;
   - ECE of P(top) ≤ off + 0.02.
4. **Nulls clean:**
   - pure noise is never FIT-COMPATIBLE;
   - single-factor draws gain no extra factor at a rate above off (within Monte Carlo error);
   - injected out-of-class data are never newly FIT-COMPATIBLE.
5. **External check:** the named cases are not worse in any cell.
6. **Review:** a fresh-context reviewer subagent (`experiment-audit` / `result-to-claim`) passes the claim.

If the in-family result passes but LOFO fails, the layer stays off.

---

## 3. Layers

Summary (plug points use main's line numbers after B0):

| id | kind | plugs into | flag | trains on | status |
|---|---|---|---|---|---|
| V0 | deterministic battery (main's) + feature exports | `validate.validate`; `learned/features.py` | always available, read-only | — | build exports |
| **L2c** | interval calibration (coefficients, weights) | `run_loop` after refine/bootstrap; `coef_draws` before `split_layer` | `intervals` | G + S | **build** (passed E14) |
| **H0** | high-κ candidate modes, deterministic raw-residual scan | `run_loop` depth-0, before `refine_factors` | `highk="scan"` | — | **build** |
| H1 | learned high-κ mode proposal | same spot, after H0 | `highk="scan+net"` | residuals from G + S | **conditional** |
| **L2d** | global method constants | module constants of `loop` / `structfit` / `bayes_split` | `constants` | G (fit split) | **build** |
| **LB** | run-time / search budget | before the expensive optional steps of `run_loop` | `budget` | step logs of G + S | **build** |
| L2b | P(top) calibration | `LoopResult` report | `prob_calibration` | G + S | **re-gate** (code exists) |
| V1 | learned failure flags + OOD | after V0 | `validator` | G + S + I | **re-gate** (code exists) |
| C | targeted reruns, honesty rule | wraps `run_loop` | `controller` | remedy table from I | **build last** |
| L0 | learned per-bin seeds | `extract_modes_ic(seeds=)` | (existing `SEED_PROVIDER`) | — | **closed** (E15) |
| L5 / L6 | learned grouping / amortised NPE | — | — | — | rejected / deferred (PHASE4) |

### 3.0 V0 feature exports (deterministic; prerequisite of L2c, LB, V1)
- **Where.** `learned/features.py` only. Main owns `validate.py`, so no change is made there (avoids merge conflicts).
- **What.** The features E14 lacked (NaN there), computed read-only from the `LoopResult` and the data:
  - **κ_Vand**: log₁₀ condition number of each factor's coefficient design (the per-factor Vandermonde in ξ at its κ support; T9, P2-P6);
  - **per-factor SNR**: the median matched-filter SNR of the modes on the factor's variety, |A|·√(Σ_t |e^{λt}|²·n_x)/σ (main's E13 proxy, evaluated at the *fitted* modes);
  - **disagreement**: the spread of per-sample track coefficients over the reported sd (T48); on grids, the bootstrap spread over the Laplace sd;
  - **split floor**: γ_N^{−1/2}·σ/|w| (T5/T6).
- **Tests.** Exact-data values on two hand cases; NaN-free on the corpus.
- **Cost.** Milliseconds per run.

### 3.1 L2c — interval calibration of coefficients and weights  [flag `intervals`]
- **Purpose.** Coefficient coverage on random families is below nominal (0.67–0.76 in E14), and weight cover90 is 0.50 in three benchmark cells. The intervals are conditional on the selected structure and come from Laplace or a 16-copy bootstrap. L2c rescales them per regime.
- **Where.**
  - *Coefficients:* `loop.run_loop`, at the end of the depth-0 block, after `refine_factors` / `bootstrap_intervals` have set `FactorReport.coef[(a, b)] = (mean, lo, hi)`. A new `learned.apply.scale_intervals(factors, feats, model)` widens (or narrows) each (lo, hi) about the mean.
  - *Weights, by Monte Carlo:* the same per-factor scale multiplies the deviation of each draw in `coef_draws(factors, W_DRAWS, scale=s)` (a new optional argument; `None` is today's path). The weight posterior is then recomputed from the scaled draws, not rescaled after the fact.
  - *Weights, residual:* a second, weight-specific inflator on `split["w_q"]`, applied only if, after the Monte Carlo step, the weights still miss the gate.
- **Features** (dimensionless, monotone sign fixed by theory):
  - margin n_κ − (dx + 1) (↓, T13/T40);
  - log SNR (↓);
  - κ_Vand (↑, T9);
  - disagreement (↑, T48);
  - relative half-width sd/|c| (↑);
  - log n_obs (↓);
  - weights only: γ_N^{−1/2}σ/|w| (↑, T5/T6) and c_F (↑).
- **Model.** The existing `IntervalInflator`: sklearn `HistGradientBoostingRegressor` with `monotonic_cst` on log|z| (z = (true − mean)/sd), then Mondrian split-conformal over 3 regimes of the margin. The scale is clipped to [0.5, 5].
- **Competitor that must be beaten.** One global conformal scale per quantity (a single number). If the GBM does not beat it on interval score at equal coverage, the scalar ships instead: the simpler calibration wins ties.
- **Training data.** The G + S fit split (coefficients of correctly selected factors only, plus weights); the conformal step uses the calibrate split.
- **Acceptance (primary).**
  - Coverage of the 90 % coefficient intervals within [0.85, 0.95] on every LOFO fold and on the test split.
  - Interval score ≤ off and ≤ the scalar competitor.
  - Weights: cover90 within [0.85, 0.95] wherever γ_N^{−1/2}σ/|w| < 1 (above that, the floor is reported, T6).
  - SBC histograms not worse.
  - Labels unchanged (L2c cannot change a label, which is asserted in a test).
- **Cost.**
  - Training: seconds.
  - Run-time: ~1 ms per run, plus one extra `split_layer` call when `coef+weights` is on (≈ the existing split cost, 1–10 s).
- **Theory.** T5/T6, T9, T13/T40, T48, T50, T55; conformal validity holds only within the simulator prior (PHASE4 §L2 point 3), hence the tag.

### 3.2 H0 — high-κ candidate modes from a raw-residual scan (deterministic)  [flag `highk="scan"`]
- **Purpose.** This is the failure with the largest measured headroom (E16). The GP posterior loses high-κ modes that the raw data still carry, and each extra κ is one more equation per factor (T13/T40). H0 only *proposes*; the refined raw evidence decides.
- **Where.** `loop.run_loop`, depth-0, immediately before `cand = support_path(...)` / `refine_factors(...)` (the step-5 block). The code goes in a new `learned/highk.py: scan(obs, factors, kmax, sigma) -> list[ModeProposal]`, plus `proposals_to_candidates(...)`.
- **Algorithm.**
  1. Form the raw residual r = y − ŷ of the current factors (their EPGP posterior mean on the observations, as in `refine_raw.log_evidence`).
  2. Scan it:
     - *Grid:* per DFT bin, the residual series that `validate.predictive_bins` already forms; scan the bins V0.1 flags and every bin above `_raw_kmax`.
     - *Scattered:* a damped generalised Lomb–Scargle statistic over κ ∈ lattice up to the point-density Nyquist and λ on a grid in Re λ ∈ [−LAM_MAX, RE_MAX] × Im λ ∈ [−LAM_MAX, LAM_MAX], evaluated directly (n ≤ 5000 points × ~64 κ × ~400 λ: no FINUFFT needed).
  3. Refine peaks by VarPro on the raw data; greedy OMP, at most 6 modes.
  4. **Look-elsewhere threshold.** The maximum scan statistic is compared with its null distribution, from B = 50 parametric re-simulations of the residual under the current fit (same design, same σ). A mode is kept only if p < 0.01, a level declared now (PHASE4 review point 4; the Davies problem).
  5. **Proposals, all scored by `refine_factors` evidence − ½p log n:**
     - (a) raise `kmax` to include the new κ, so the existing factors are refined with more equations (the E16 gain);
     - (b) a new factor of lowest degree through the found modes, only if they span ≥ dx + 1 distinct |κ| (otherwise the proposal is reported as ID-KER evidence and not added);
     - (c) one existing factor refitted one degree up through its modes plus the new ones.

     At most one added factor per run, with the same refine budget per candidate (honesty rule (2)).
- **Features / model / training.** None (deterministic).
- **Acceptance (primary).**
  - Scattered corpus S, and grid at 5 %: right-set ↑ (paired), λ error ↓ in high-κ bins, and the number of factors with margin ≥ 0 ↑.
  - Correct-abstain unchanged where the oracle says absent: H0 must not "recover" information-absent κ.
  - Nulls: added-factor rate on single-factor and pure-noise data ≤ off + Monte Carlo error.
- **Cost.**
  - Scan: ms to s.
  - Null bootstrap: 50 × scan ≈ seconds.
  - Refine of ≤ 3 extra candidates: ≈ 3 × today's refine (seconds to a minute).
  - Only runs when the residual or V0.1 says something is left (V0.1 omnibus p < 10⁻³ on grids; on scattered data, always).
- **Theory.** R2-T6 (fields are sums of e^{λt+iκx}), T44 (raw data, not the GP mean), T13/T40/T46 (count per added factor), CONV-T5 (no data-free threshold, hence the null bootstrap); E16.
- **Ownership note.** PHASE4 assigned L1a(i) to "the local session". The user's brief now puts high-κ candidate modes in this session's scope. To avoid double work, B2 leaves a note in the shared notes folder for main; the code lives in `learned/highk.py` and touches `loop.py` only at the hook.

### 3.3 H1 — learned high-κ proposal  [flag `highk="scan+net"`, conditional]
- **Trigger.** H1 is built only if, after H0, ≥ 10 % of the oracle-identifiable factors in corpus S still miss a visible κ (the "present but missed" class). Otherwise it is closed with that number.
- **Where.** Same as H0. Its proposals join H0's before step 4 and face the same null threshold and evidence.
- **Input.** Per κ bin, the residual time series (grid) or the per-κ NUFFT/least-squares residual projection on a time grid (scattered), whitened by σ.
- **Model.** Reuse the `expseeds` heatmap network (damping × frequency grid, count head, focal loss), retrained on *residuals* rather than clean sums. ~10⁵ parameters; PyTorch CPU.
- **Training data.** Residuals stored by corpus G + S, fit split, with the true missing modes as targets (≈ 3–5 k bins), plus synthetic exponential sums (`expsum`) for volume.
- **Acceptance.** As H0, *against H0 alone* (the reference is H0 on), with LOFO. The E15 lesson applies: if an oracle proposer (the true missing modes as proposals) does not beat H0, H1 is closed without training. That costs one corpus pass.
- **Cost.** Training ≈ 1 h; inference ms.

### 3.4 L2d — global method-level constants  [flag `constants="sim-v2"`]
- **Purpose.** Fit the few constants that shape the likelihood or the growth trigger, once and globally, on the simulator prior. Thresholds acting on probabilities are not tuned (PHASE4 §L2: they follow from a loss).
- **Constants (4, declared now).**

  | constant | where | default | grid |
  |---|---|---|---|
  | `snr_min` (mode cut) | `structfit.extract_modes_ic` | 3 | {2, 2.5, 3, 4, 5} |
  | `z` (κ support) | `loop.kappa_support` | 3 | {2, 2.5, 3, 4} |
  | `CAP` (robust cap) | `loop.CAP` / structfit | 3 | {2.5, 3, 4, 6} |
  | `PRED_LOGP` (V0.1 growth trigger) | `loop.PRED_LOGP` | −3 | {−2, −3, −5, −8} |

- **Where.** A context manager `learned.constants.patched(cfg)` sets these module-level names. `snr_min` and `z` are today default arguments: B4 lifts them to module constants (`SNR_MIN = 3.0`, `Z_SUPPORT = 3.0`) with identical behaviour. The structfit part is a core touch, covered by a test (rule 3).
- **Method.**
  1. One-factor-at-a-time scans (17 settings), then a 3 × 3 grid around the best pair. This totals ≤ 26 settings on a 60-run tune subset of G-fit (12 per family, both noises).
  2. Every setting's per-run results are stored, so **LOFO selection needs no extra runs**: choose on four families' rows, evaluate on the fifth.
  3. **Objective (lexicographic):** false-confident ≤ default (hard), then coverage not worse, then right-set + correct-abstain ↑.
- **Acceptance.** The selected setting beats the default on the test split and on every LOFO fold (§2.4), and the LOFO-selected settings agree (otherwise the constants stay default: they do not transfer).
- **Cost.** ≈ 26 × 60 runs × ~150 s / 8 workers ≈ 8 h background. Run-time cost 0.
- **Theory.** CONV-T5 (no data-free threshold), T55 rule (constants are global, never per run).

### 3.5 LB — run-time and search budget  [flag `budget`]
- **Purpose.** `run_loop` runs several expensive optional steps whose outcome is usually "no change":
  1. each growth option (a full `_run` over all samples);
  2. the complex-coefficient rerun;
  3. `_refine_alternatives` (ALT_TOP = 2 refines);
  4. `split_branches` + refine;
  5. recursion child runs;
  6. the two `heldout_score` calls.

  F3/F4 runs take 200–900 s. LB predicts, from cheap features available at that point, whether a step will change the final factor set or label, and skips it when that is unlikely.
- **Where.** One guard per step in `run_loop`: `if learned and learned.budget and lb.skip("complex_rerun", feats): note += "...skipped by LB..."; else: <today's code>`. The skip is written into `LoopResult.note`, so the report says which steps were skipped.
- **Features** (computed before the step): P(top), structure entropy, the V0.1 omnibus log p, min margin, number of factors, max m, evidence gap, σ/std(u), n_obs, sample count, and step-specific ones (number of grow options, ALT_TOP structures' evidence gaps).
- **Model.** One HGB classifier per step. The skip threshold comes from **conformal risk control** on the calibrate split, so that P(the skipped step would have changed the factor set) ≤ α = 0.02 in-prior. The existing `validator._risk_threshold` is reused.
- **Training data.** Off runs log each step's input and output factor set: the label "changed" is observed, not simulated, because every step runs when the layer is off. Corpus G + S fit and calibrate.
- **Honesty.** A skip removes candidates and never changes a score. The decision is made from features *before* the step by a fixed model, never by running both branches. The gate checks the forking-paths risk empirically (the null rows of §2.4).
- **Acceptance (primary).**
  - Median runtime ↓ ≥ 25 % and p90 ↓ on test and LOFO.
  - Final factor-set agreement with off ≥ 98 %.
  - Right-set non-inferior (margin 0.02); false-confident not higher.
- **Cost.** Training seconds; run-time < 10 ms per guard.
- **Deterministic companion (not learned, same flag group).** Monte Carlo sizes (GP S, bootstrap B, W_DRAWS) stay fixed. Adaptive MC stopping by MC-SE is listed as an option only: it changes the computation of an interval, which the regression test would then have to cover.

### 3.6 L2b — calibrated P(top) in the report  [flag `prob_calibration`, re-gate]
- The code (`ProbabilityCalibrator`, `VennAbersCalibrator`) exists. The re-gate is E14's LOFO protocol on the new in-prior corpus (G + S, P(top) vs right set).
- It switches on only if ECE and Brier beat the raw P(top) on every LOFO fold.
- It never changes a label or a threshold. It adds `p_top_calibrated` to the report, with the prior tag.
- **Cost:** minutes.

### 3.7 V1 — learned failure flags and OOD score  [flag `validator`, re-gate after the I corpus]
- **Where.** After `validate.validate(...)` (main's V0) in the corpus runner and in C. Report only.
- **Features.** V0 `features()` (v01_*, v02, v03, v10, v13) + `factor_aggregates` + the §3.0 exports. No identifiers.
- **Model.** The existing `Validator`: one-vs-rest HGB per failure mode, conformal risk control (missed-failure ≤ 0.1), and an OOD gate by conformal outlier p-value.
- **Labels** (by construction):
  - wrong set, missing factor, spurious factor, coefficient miss;
  - information absent (oracle);
  - the six I injection types.
- **Acceptance.**
  - LOFO over families *and* over injection types (train on 4 of 6; the two held-out types must score OOD or "other", never a wrong confident mode).
  - Missed-failure ≤ 0.12 and false-flag ≤ 0.10 per fold.
  - The decisive test (PHASE4): with C, V1's remedy order reduces actions per run at equal accuracy against C's fixed order. If not, V1 stays off and C uses the fixed order.
- **Cost.** Training minutes; the I corpus ≈ 1–2 h.

### 3.8 C — controller with the honesty rule  [flag `controller`, built last]
- **Where.** A new `learned/controller.py: run_controlled(samples, t, x, sigma, ..., learned)`, which wraps `run_loop` and never edits it.
- **Loop.**
  1. Run `run_loop`, then V0 (and V1 if on).
  2. Map the active diagnoses to remedies through the PHASE4 §4 C table, restricted to actions that change *candidates or computation only*:
     - H0 scan if off;
     - more GP samples / restarts (S × 2);
     - ALT_TOP 2 → 4;
     - growth already happens inside the loop.
  3. Stop at once with MISFIT/UNDECIDED on V0.2 margin < 0 (ID-KER), or on an out-of-class flag.
  4. At most K = 3 actions.
- **Honesty rule** (PHASE4 §4 C, T56 heuristic):
  - (1) the candidate space is declared before the run (all structures within `bounds`);
  - (2) equal refine budget per candidate;
  - (3) likelihood constants and structure prior frozen (L2d values if on, else defaults);
  - (4) the final report is the posterior over all visited structures, plus a missing-mass term;
  - (5) optional `confirm=True`: a random point split fixed *before* the run (search on one half, one pre-specified evidence comparison on the other).
- **Remedy order.** `RemedyTable` (Beta lower bound of success per remedy and diagnosis), fitted offline on the I + G runs with each remedy applied.
- **Acceptance.**
  - Right-set ≥ off.
  - **Forking-paths null test:** the false-FIT-COMPATIBLE rate on N and I is equal to off within Monte Carlo error.
  - With `confirm=True`, coverage holds.
  - Actions per run are reported.
- **Cost.** ≤ 3 extra loop runs, only for runs with an active diagnosis; offline ≈ 2 k extra runs (≈ 6–8 h background) for the remedy table.

### 3.9 Closed / not built
- **L0** (learned per-bin seeds): closed by E15. The hook and the network stay, off.
- **L5** (learned grouping): rejected (T8, P2-P4, CONV-D1; grouping by factors only).
- **L6** (amortised NPE): deferred (PHASE4 §L6); not in this session.

---

## 4. Tests (written before each layer's code)

- `test_learned_off.py` — golden: `learned=None` and `Learned()` both reproduce stored B0-snapshot outputs on 6 draws (F1, F2, F3 grid; heat 400 scattered; a named case; a pure-noise grid).
- `test_learned_intervals.py` — the scale is monotone in each feature by construction; labels are unchanged; `coef_draws(scale=None)` is bit-for-bit today; a scale of 1 gives today's weights.
- `test_highk.py` — a synthetic residual with one injected damped mode is found at the right (κ, λ) within 3 CRB; pure noise passes the null at the declared rate (≤ 0.02 in 200 trials); proposals never bypass `refine_factors`; heat 400 @ 5 % gains κ = 4 (E16 cell).
- `test_constants.py` — `patched()` restores every constant on exit (also on exception); the default file equals today's literals.
- `test_budget.py` — a skipped step is noted in `LoopResult.note`; with a model that never skips, the output is identical to off.
- `test_controller.py` — the honesty invariants: frozen constants (asserted), equal refine budget, the declared space, and the visited-set report containing the missing-mass term.
- Existing `test_learned.py` stays green.

---

## 5. Phase B order, commits and compute

| step | content | commit | compute (background) |
|---|---|---|---|
| **B0** | Create `PDEFactorML/.venv` (none in this copy), install the package and the test deps (sklearn, torch CPU for the gp path and L0/H1). Snapshot main's deterministic files (§0.2) → `SYNC.md` with sha256s. Merge with the branch's `seeds=` hook. Full pytest. Golden outputs. `learned/config.py` + `run_loop(learned=)` plumbing (no-op). | "S-LEARNED B0: sync main snapshot, config, golden off test" | 10 min |
| **B1** | Harness: `ll_corpus.py`, metrics, gate script `ll_gate.py`, §3.0 feature exports. Launch corpora G, S, N. | "B1: corpus harness, metrics, feature exports" | ≈ 6 h |
| **B2** | H0 scan + tests; ablation on S + G-test + N | "B2: H0 raw-residual high-kappa scan" | ≈ 3 h |
| **B3** | L2c fit/calibrate, scalar competitor, wiring (coefficients, then coef draws → weights); gate | "B3: L2c interval calibration" | minutes (reuses corpora) |
| **B4** | L2d scans + LOFO selection; module-constant lift with a test | "B4: L2d global constants" | ≈ 8 h |
| **B5** | LB step logs → classifiers → risk control; gate; L2b re-gate (cheap) | "B5: LB budget; L2b re-gate" | minutes + one gate pass ≈ 3 h |
| **B6** | Injected-failure corpus I; V1 re-gate | "B6: failure injection, V1 re-gate" | ≈ 2 h |
| **B7** | C controller + remedy table + forking-paths null test | "B7: controller with honesty rule" | ≈ 6–8 h |
| **B8** | H1, only if triggered (§3.3) | "B8: H1" or a note "H1 closed: <number>" | ≈ 2 h |
| **B9** | `sessions/LEARNED/REPORT.md` (on/off table per layer, gates, failures), proposed THEORY rows; fresh-context review | "B9: report" | — |

- Each layer is one commit with its tests and an ablation table (off vs on, test split + LOFO + nulls + named cases) in `sessions/LEARNED/results/`.
- After a layer passes, later gates are run with it **on**, so ablations stack. Each REPORT row states its reference.
- Nothing is pushed.

Total background compute ≈ 30–35 h at 8 workers. If that is too much, the cuts in order are:
1. L2d to 2 constants (`snr_min`, `PRED_LOGP`);
2. S to 400 pts only;
3. C's remedy table to the injected-failure corpus only.

---

## 6. Risks and how the plan handles them

| risk | handling |
|---|---|
| Main's uncommitted files change after the snapshot | dated sha256 snapshot (`SYNC.md`); learned code touches `loop.py` only at hooks; re-sync = re-apply the hooks |
| The corpus prior teaches "high κ is small" | the amplitude law is random in `simulator` (gauss / power / flat); the oracle `identifiable()` defines "absent" from the truth only, and H0/H1 are never credited below it |
| A layer helps in-family only | LOFO is mandatory, and the named cases are an external test |
| H0 adds spurious factors | null-max threshold, at most one added factor, the evidence decides, the null gate |
| L2c hides a model bug by inflating | the scalar competitor and the per-feature monotone signs are reported; coverage is reported conditional on selection with the selection rate |
| LB skips a step that mattered | risk control at α = 0.02; skips are written in the note; agreement with off ≥ 98 % is gated |
| Controller search inflates the evidence | honesty rule (frozen likelihood, declared space, equal budget, missing mass); forking-paths null test; optional pre-run split |
| Compute overrun | the cuts in §5 |

---

## 7. Questions for the parent session (Phase B can start without answers; the default is in brackets)

1. B0 imports main's *uncommitted* deterministic state into this copy. [Default: yes, a dated snapshot.]
2. H0 overlaps PHASE4's L1a(i), which was assigned to main. [Default: build it here behind its flag and leave a note for main.]
3. The compute budget of ≈ 30–35 h background. [Default: run it, with the §5 cuts if a corpus overruns by 50 %.]

---

## 8. Proposed THEORY_TO_ALGO rows (add-only; numbers for MAIN to assign, since main already uses T52–T60)

| # | result (status) | what it says | decision |
|---|---|---|---|
| TL-1 | no theory: empirical (E15, S-PHASE4-ML) | seeds cannot improve a CRB-efficient per-bin step at nt = 32–64 | L0 closed; learned effort goes to calibration, high-κ proposals and budget |
| TL-2 | R2-T6 + T44 + CONV-T5; E16 | raw residual scans find modes the GP loses; the scan maximum has no data-free null | H0: raw-residual scan with a parametric-bootstrap null of the maximum, the evidence decides |
| TL-3 | heuristic, statistics (split conformal, monotone GBM; E14) | dimensionless theory-signed features transfer across families; probability maps fitted on other families do not | calibrate intervals (L2c), not P(top), unless an in-prior corpus reverses it |
| TL-4 | heuristic, statistics (conformal risk control) | skipping a step is a candidate-set change, not a score change | LB skips steps under risk control α = 0.02; skips are reported |

---

## 9. Addendum (2026-10-29, B1): generality rule

The user's rule 8 of `D:\PDEFactorML\CLAUDE.md`, relayed by the parent session: every change must be general. It must hold for any factor structure, order, coefficient scale and PDE in scope, never be tuned to the case that exposed a bug; it is justified from theory or a scale-free criterion, and tested on held-out families (F1–F5, LOFO), not only on the failing case. It applies to every layer, feature and constant here. Applied so far:
- **H0 scan grid:** the first draft's hand-set ranges (Re λ ∈ [−6, 1], |Im λ| ≤ 40, scattered band 24) were replaced by ranges in units of the observation window and the sampling: Re λ·T ∈ [−8, 1] at spacing 1/T, |Im λ| up to the time Nyquist π/Δt at spacing π/(2T) (Δt = T/√n on scattered data), scattered band ≤ √n/2. The look-elsewhere threshold was already data-driven (null bootstrap).
- **L2c features:** dimensionless only (logs, ratios, counts); the model is gated by LOFO.
- **Gates:** every layer is accepted on all five families and LOFO, never on a named case.
