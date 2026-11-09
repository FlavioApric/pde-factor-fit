# S-LEARNED-V1 — corpus I, then the re-gates of V1 (validator) and L2b (calibrated P(top)): PLAN

Session: S-LEARNED-V1 (worktree `ll-validator-1b737b`). Implements `sessions/LEARNED/PLAN.md` §2.2 (corpus I), §3.6 (L2b), §3.7 (V1), under the §2.4 gate and the §9 generality rule. Files owned: `analysis/exp/ll_corpus.py` (corpus I only), `analysis/exp/ll_inject.py`, `analysis/exp/ll_v1*.py`, `src/pdefactor/learned/validator.py`, `src/pdefactor/learned/ptop.py`, `src/pdefactor/learned/resid.py` (new, deterministic diagnostics), the hook at the end of `run_loop` (`_depth == 0`), `tests/test_learned_v1.py`, `tests/test_learned_ptop.py`, `tests/test_learned_inject.py`.

Research: `RESEARCH.md` § S-LEARNED-V1 — 2026-10-29.

## 0. What changes from E14, and why a re-gate can come out differently

| E14 (failed) | here |
|---|---|
| grids only, stand-in posterior, pre-v2.13 pipeline | G + S + N from `random_pde` (in-prior, F1–F5), current pipeline |
| V1 features all-NaN in several columns | V0 exports (`features.export_features`) + V0 battery + step log + new residual diagnostics (§3) |
| no injected failures: V1 could only learn "wrong set" | corpus I, 7 types × 3 strengths, so V1 learns failure *signatures* |
| L2b: isotonic and Venn–Abers only (high variance) | adds temperature / Platt on logit P(top) (1–2 parameters) and a feature-conditional logistic arm |

Both layers are report-only. §2.4 items 2–5 (right-set, false-confident, nulls, named cases) hold **by construction**: a test proves labels, factors, intervals and evidence are bit-identical with the flag on. So no second pipeline arm is run; every gate is computed offline from the off-arm rows. This saves all on-arm compute.

---

## 1. Corpus I (injected failures) — first deliverable

### 1.1 Design
- Base draw: `simulator.random_pde(family, seed)`, F1–F5, the G grid (nt = 64, nx = 128, T = 2, L = 2π), noise 5 % of std(u) (the G design). Grid only: aliasing is defined by the grid's Δt, and scattered I would need ≈ 400 GP fits (§6, option).
- Failure targets only, never fitting targets (PLAN §1.8). Rows carry `corpus="I"`, `inject={type, strength_level, strength_value, params}`, and the usual off-arm fields (`label`, `category` vs the base draw's truth, `export`, `v0`, `steps`, …), plus the new `resid` diagnostics (§3.1).
- **Strength is scale-free and common across types** (rule 8). For the four law deviations the strength is the omnibus χ² z-score of the injected deviation against the noise:
  z_inj = ‖u_inj − u_clean‖² / (σ² √(2N)), N = nt·nx.
  This is exactly the V0.1 omnibus statistic's expected excess if the clean law were fitted perfectly (no theory row: standard χ² detection). Levels z ∈ {2, 8, 32}: "barely visible" (below the V0 Bonferroni line), "visible", "obvious". The injection parameter ε is set per draw by bisection to hit z (monotone in ε for every type; tested). For noise types the strength is the noise-structure parameter itself (dimensionless).

| type | generator (all generic in the factor structure and order) | strength levels |
|---|---|---|
| `two_laws` | law A on t < T/2, law B on t ≥ T/2, continuous in u and ∂ₜʲu at T/2: B = A's polynomial with every non-leading coefficient multiplied by (1 + ε·g), g ~ N(0,1) fixed per draw; second half integrated from A's state at T/2 by the companion-form solver below | z ∈ {2, 8, 32} |
| `coloured` | stationary Gaussian noise, AR(1) in x and in t (separable), correlation ρ, marginal variance = σ² | ρ ∈ {0.3, 0.6, 0.9} |
| `heteroscedastic` | σ(t,x) = σ₀·h(t,x), h = 1 + a·|u|/max|u| (signal-dependent) for even seeds, h = exp(a′·t/T) for odd seeds; mean variance = σ² | max σ / min σ ∈ {2, 5, 20} |
| `nonlinear` | Q(∂ₜ,∂ₓ)u = ε·u·uₓ (Burgers-type) | z ∈ {2, 8, 32} |
| `varcoef` | the ξ-dependent part of Q's lowest τ-order term multiplied by (1 + ε cos x) | z ∈ {2, 8, 32} |
| `fractional` | every mode's λ(κ) shifted by −ε|κ|^α (fractional dissipation, α ~ U(0.3, 1.7), |α − 1| > 0.1), exact modal sum (no solver) | z ∈ {2, 8, 32} |
| `aliasing` | time rescaling Q(τ/s, ξ): all λ multiplied by s so that max|Im λ| = r·π/Δt (a legal linear law, under-sampled) | r ∈ {1.2, 2, 3} |

- **Solver for `two_laws`, `nonlinear`, `varcoef`:** pseudo-spectral method of lines on the companion (first-order-in-time) form of Q made monic in τ, RK4 with sub-steps |λ_max|·dt ≤ 0.5, 2/3 de-aliasing for the nonlinear term. Initial state (u, ∂ₜu, …, ∂ₜ^{m−1}u at t = 0) from the exact modal sum. **Test:** ε = 0 reproduces the exact field to ≤ 1e-8 relative on every family (F4 products expanded, F5 third order). Generic in the order m and in the factor structure.
- **Seeds and splits (fixed now):** seeds 400–403 per (type, level, family): 400–401 = fit, 402 = cal, 403 = test. `SEEDS["I"]` and `DESIGNS["I"] = [("grid", 0.05)]` added to `ll_corpus.py`; injection params drawn from `rng([7, type_index, seed])`, independent of the base draw.
- **Size:** 7 types × 3 levels × 5 families × 4 seeds = **420 runs**.
- **Compute:** G-grid runtimes 14 s (F1) – 875 s (F4), cap 1200 s; injected runs can hit the cap more often (timeout recorded as a row with `label="TIMEOUT"`, kept as a feature-less failure row). Estimate ≈ 420 × ~180 s / 3 slots ≈ **7 h** background through `slots`. Order: test seeds last; F4 last within each seed so the other families arrive early for the controller session. Cut if needed: drop seed 401 (→ 315 runs).
- **Delivery:** when complete, copy to `D:\Larned layers\PDEFactorML\analysis\exp\out\ll_I.jsonl` (the one allowed write) and message the parent. A partial file (all families, seeds 400 + 402) is copied first if the controller session needs it earlier.

### 1.2 Tests first (`tests/test_learned_inject.py`)
1. ε = 0 / ρ = 0 / ratio 1 / r = clean scale: every generator returns the clean field (or white noise) exactly or to 1e-8.
2. The bisection hits z_inj within 5 % on one draw per family.
3. AR(1) noise: empirical lag-1 correlation within ±0.05 of ρ; marginal variance within ±5 %.
4. Heteroscedastic: variance-ratio and mean variance as specified.
5. Aliasing: max|Im λ|·Δt/π = r.
6. Nonlinear/varcoef solver: energy and dispersion check at ε = 0 (exact), and ε > 0 moves z monotonically.
7. Rows: `corpus="I"` rows never enter G/S fits (a guard in the loaders).

---

## 2. Hook and API

- `run_loop`, after `out.steps = log.rows` (end, `_depth == 0`), one block:
  ```python
  if _depth == 0 and (ll.validator or ll.prob_calibration):
      from .learned.report import attach   # learned/validator.py + learned/ptop.py
      attach(out, ll, data=l2c_data(...), grid=(u_mean, t, x, sigma))
  ```
  It writes only `out.learned_report` (new `LoopResult` field, default `None`) and appends one line to `out.note`. Nothing else is touched.
- `learned/resid.py` (deterministic, no learning): `diagnostics(factors, u, t, x, sigma) -> dict` (§3.1).
- `learned/validator.py`: keep `Validator` (one-vs-rest + risk control + Mahalanobis OOD); add `FailureDetector` (binary failure score + conformal false-alarm threshold + open-set type report), `featurise(row) -> vector`, `load()/save()` of a versioned model under `learned/models/v1-<corpus hash>.joblib` with `PRIOR_TAG`.
- `learned/ptop.py`: `PTopCalibrator(method="temperature"|"platt"|"isotonic"|"venn-abers"|"logit-features")`, `ece_adaptive`, `brier`; reuses `calibrate.ProbabilityCalibrator` / `VennAbersCalibrator`.
- Report fields: `learned_report = {"v1": {"p_failure", "flag", "type" | "other" | None, "p_ood", "tag"}, "p_top_calibrated": float, "p_top_interval": (lo, hi) (Venn–Abers only), "tag"}`. Never a label.
- **Off:** `learned=None` / `Learned()` → `learned_report is None`, golden file and `tests/test_learned_off.py` green.

### 2.1 Tests first (`tests/test_learned_v1.py`, `tests/test_learned_ptop.py`)
1. Flag on vs off on 3 draws (one grid, one scattered, one null): `label`, `factors`, intervals, `structures`, `evidence` bit-identical; only `learned_report` and one `note` line differ.
2. `resid.diagnostics` on pure white noise with a correct fit: every test statistic's p-value is uniform (KS over 200 noise draws, p > 0.01); on AR(1) ρ = 0.6 the whiteness p-value < 1e-3.
3. Scale invariance (rule 8): diagnostics unchanged (to 1e-10) when u, σ are multiplied by 10³ and when t, x are rescaled with the law.
4. `FailureDetector` conformal threshold: false alarm on exchangeable synthetic clean scores ≤ α + MC error (1000 draws).
5. Open-set: a type absent in training is reported as "other" or OOD on a synthetic 2-D example.
6. `PTopCalibrator`: monotone maps; temperature = 1 is the identity; ECE/Brier against hand values.

---

## 3. V1

### 3.1 Features (all dimensionless; no identifiers, no family, no seed)
- V0 battery: `V0Report.features()` (v01_*, v02, v03, v10, v13).
- V0 exports: `features.export_features` (κ_Vand, per-factor SNR, disagreement, split floor) aggregated by `factor_aggregates`.
- Step log: per step `changed` bits and the runtime fractions (no absolute seconds).
- Run summary: `p_top`, n_factors, label one-hot (the label is an input, never an output).
- **New residual diagnostics** (`learned/resid.py`), on the per-κ-bin time residual of the V0.1 projection (same algebra as `validate.predictive_bins`, so no new fit):
  - whiteness in t: Ljung–Box Q over lags 1..⌊√nt⌋ pooled over bins (→ log p); lag-1 autocorrelation;
  - whiteness in x: lag-1 autocorrelation of the physical-space residual along x; spectral flatness of the residual over κ (Wiener entropy);
  - heteroscedasticity: Breusch–Pagan n·R² of r² on (|û|, t) (→ log p);
  - stationarity in time: log ratio of residual energy t ≥ T/2 vs t < T/2 (two laws);
  - Nyquist fraction: residual energy share in the top 1/8 of temporal frequencies (aliasing);
  - κ-trend: slope of log residual energy per bin vs log|κ| (fractional, high-κ loss).
  Theory: T50 (the bootstrap and the evidence assume white Gaussian noise at σ) motivates whiteness and heteroscedasticity; the simulator's Nyquist bound (`LAM_MAX`) motivates the Nyquist fraction; the rest: "no theory: standard misspecification tests".
- Rows of G/S/N need `resid` too. **Question 1 below.**

### 3.2 Targets
- (a) failure vs clean: I rows = failure (by type); G/S/N rows = clean-data runs.
- (b) run failure on clean data (the old V1 role, PLAN §3.7): wrong set, missing factor, spurious factor, coefficient miss (from `category`, `ok`, `coef`); "information absent" from the oracle.
- (c) failure type (7 I types + "clean"), open-set.

### 3.3 Models compared (simplest first)
| arm | description |
|---|---|
| B0 | V0 only: omnibus log p as the score (no learning) |
| B1 | V0 + resid diagnostics, best single statistic per type, Bonferroni-combined (no learning) |
| B2 | isolation forest on the feature vector (unsupervised; brief's baseline) |
| B3 | Mahalanobis (Ledoit–Wolf) distance (existing OOD gate) |
| B4 | kNN distance (k = 10, standardised) |
| V1 | HGB (monotone where the sign is known, e.g. Ljung–Box log p ↓ ⇒ failure ↑) binary failure score + HGB multi-class type head |
All scores are conformalised the same way: threshold = the ⌈(1 − α)(n + 1)⌉-th clean calibration score, α = 0.05, so false alarm on clean runs ≤ 0.05 (Bates et al. 2023).

### 3.4 Evaluation
- Fit on fit split, conformal threshold on cal split (clean G/S cal runs), evaluate on test split. Never tuned on test.
- **LOFO by family:** train on 4 families (I + G/S), calibrate on cal of those 4, test on the 5th.
- **LOTO by type:** train on 6 of 7 types (+ all clean); the held-out type must be detected (failure score) and reported "other"/OOD, never a confident wrong type (type head with conformal threshold on seen types).
- Metrics: detection rate on I-test at false alarm 0.05 on G/S-test, per type and level; false alarm realised; type accuracy on seen types; wrong-confident-type rate on held-out types; for target (b) missed-failure and false-flag.

### 3.5 Gate (V1 on only if all hold, on the test split and on every LOFO fold)
1. **Primary:** detection@FA=0.05 on I improves over B0 (V0 alone), paired bootstrap over runs, 95 % CI excluding 0; also ≥ the best baseline B1–B4 (point estimate).
2. Realised false alarm on G/S test ≤ 0.05 + MC error (binomial 95 %), and on N.
3. LOTO: on every held-out type, wrong-confident-type rate ≤ 0.10, and detection of the held-out type ≥ B0's.
4. Target (b) (PLAN §3.7): missed-failure ≤ 0.12 and false-flag ≤ 0.10 per fold; if this alone fails, V1 ships only the failure/OOD score, not the wrong-set flag (stated in the report).
5. §2.4 items 2–5: by construction (test 2.1.1), plus a check run on N and the named cases with the flag on (one pass, ≈ 30 min).
6. Fresh-context review (`experiment-audit`, `result-to-claim`, `kill-argument` as a fresh Claude subagent).
- "Useful detection rate" (brief): ≥ 0.5 at level "visible" (z = 8 / middle level) averaged over types, else V1 stays off with that number as its reason.
- PLAN §3.7's decisive test (V1 remedy order vs C's fixed order) belongs to the controller session; I hand over the model and scores.

---

## 4. L2b — calibrated P(top structure is right)

- y = `category == "right"` (also report with `equivalent` counted right); x = raw `p_top`.
- Data: G + S (all splits), off arm. N excluded (no truth structure), reported separately (calibrated P(top) on nulls must be ≤ raw).
- Arms: raw (identity), temperature (1 parameter on logit), Platt (2), isotonic, inductive Venn–Abers (E14's), logit-features (logistic on logit p + ≤ 4 dimensionless exports: min SNR, max κ_Vand, disagreement, v03_gap; L2-regularised, C by inner CV on fit only).
- Protocol: LOFO by family (fit on 4, test on 5th) and the fixed test split. Metrics: Brier (primary, proper), adaptive ECE (15 equal-mass bins), reliability diagram; paired bootstrap of Brier difference vs raw.
- **Gate (PLAN §3.6):** on every LOFO fold, Brier and ECE ≤ raw, and the pooled Brier difference CI excludes 0. If several arms pass, the one with fewest parameters ships. Otherwise L2b stays off (E14's result confirmed in-prior), with the numbers.
- Theory: T54 / TL-3 (out-of-family maps don't transfer) is the hypothesis under test; "no theory: empirical" for the arm choice.
- Compute: minutes.

---

## 5. Order of work

1. Venv (common brief) and `pytest -q` baseline.
2. Tests §1.2 → `ll_inject.py` + corpus I in `ll_corpus.py` → launch I in the background (≈ 7 h).
3. While I runs: tests §2.1 → `resid.py`, `ptop.py`, validator additions, hook. Commit "V1: corpus I injection + residual diagnostics".
4. L2b gate on G + S (as soon as the parent's G is complete). Commit.
5. V1 gate when I + G + S + N are complete. Commit.
6. REPORT.md, review subagent, full pytest, commit.

## 6. Questions for the parent (default in brackets)

1. **Residual diagnostics on G/S/N.** V1 needs `resid` on the clean corpora. G and N are not run yet. Can `_features` in `ll_corpus.py` on `learned-layers` gain one call `row["resid"] = resid.diagnostics(...)` (≈ 10 ms per run) before G/N start? I'd send the patch as a commit on my branch to cherry-pick. [Default: yes. Otherwise I re-run the off arm of the G/S fit+cal+test seeds that V1 needs, ≈ the cost of G again.]
2. A new `LoopResult.learned_report` field (default `None`), shared with other report-only layers. [Default: yes, I add it; other layers write their own key in the dict.]
3. Corpus I is grid-only at 5 % noise, 420 runs. A scattered subset (coloured + heteroscedastic + two_laws at 400 pts, 90 runs, ≈ 3 h of GP fits) is optional. [Default: grid only; add scattered if the controller session needs it.]
4. Strength levels z ∈ {2, 8, 32} for law deviations. [Default: as stated.]
