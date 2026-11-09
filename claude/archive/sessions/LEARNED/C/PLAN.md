# S-LEARNED-C — adaptive controller `Learned(controller=True)`: PLAN

Session S-LEARNED-C, 2026-10-29, worktree `ll-controller-577bc7` (branch `claude/ll-controller-577bc7`, from `learned-layers` at 3071bde).
It replaces the 3-action spec of `sessions/LEARNED/PLAN.md` §3.8 by the requirements of the parent's brief `LL-brief-C.md` (user decisions of 2026-10-29). §3.8 stays in that file unchanged (add-only); this plan supersedes it for layer C.
Status: **plan only. No code is written before the parent approves.**

Read before writing: `CLAUDE.md`, `sessions/LEARNED/PLAN.md` (§1, §2, §3.8, §9), `LL-common-brief.md`, `LL-brief-C.md`, `LL-knob-inventory.md`, `loop.py:run_loop` in full, `learned/{config,remedy,features}.py`, `validate.py` (flag codes), `analysis/exp/{ll_corpus,ll_gate}.py`, `analysis/THEORY_TO_ALGO.md`, the shared `ll_S.jsonl` rows (52 rows: off and highk arms). Research: `RESEARCH.md` § S-LEARNED-C.

---

## 0. Facts this plan is built on

| fact | source | consequence |
|---|---|---|
| One full `run_loop` costs 10–1200 s; S median 194 s; 7 of 52 S rows hit the 1200 s cap | `ll_S.jsonl` | 20 full reruns per case are not affordable. Exploration loops must be cheap (§3.3), and loops are capped by wall clock as well as count |
| Time share on S: decide 27 %, alternatives 26 %, recurse 18 %, core 13 %, refine 5 %, grow 4 %, complex 4 %, split 4 % | `steps` of `ll_S.jsonl` | a remedy that only touches refine / alternatives / split should not recompute the core: per-call memo of `_run` (§3.3) |
| The V0 flags seen on S are V0.2 (10) and V0.3 (6); off right-set on S ≈ 14/22 finished (incl. equivalent), 1 false-confident | `ll_S.jsonl` | the head-room is in wrong-abstain and ambiguous-structure cases; false-confident is rare, so any new false-confident is visible |
| Most (b) knobs are module constants or hard-coded call defaults, not `run_loop` arguments | knob inventory | first build step: a typed `RunConfig` threaded through, defaults = today's literals |
| Labels come from the frozen scoring (evidence formula, Occam, structure prior, label thresholds) | user decision 2026-10-29 | the controller chooses **configurations**; the label is always the frozen pipeline's output on a configuration |

---

## 1. Goal, done criterion, failure modes

### 1.1 Goals (what "better" means; there is no single target)
- **G1 (primary).** Right-set rate (`right` + `equivalent`, `ll_gate.right_set`) goes up, paired by draw.
- **G2.** Convert wrong-abstain on identifiable draws (oracle `all_ident`) and false-confident into right.
- **G3.** Never create a false discovery: no new false-confident on G/S, N or I, at any loop depth.
- **G4.** Stop early when more loops cannot help: low identifiability (§5), or no confident diagnosis.
- **G5.** Bounded cost: ≤ 20 loops, a wall-clock budget, and runtime/actions reported per run.
- **G6.** Deterministic: same data, same loops, same answer.

### 1.2 Done criterion
The gate of §7 passes on the test split and on every LOFO fold, or it fails and the layer stays off with the measured reason in `sessions/LEARNED/C/REPORT.md`. Either way: `RunConfig` merged with the off golden green; the controller, tests, logs and policy files committed.

### 1.3 Failure modes I design against
| # | failure | guard |
|---|---|---|
| FM1 | forking paths: searching knobs until a spurious structure fits | cross-fitted data fission (§4): search on fold A, confirm on independent fold B, swap; a change of factor set is kept only if confirmed in both directions; else the off answer stands |
| FM2 | nuisance inflation: a larger σ̂ or a wider band makes noise "fit" | σ̂ only from structure-free estimators, fixed before fission; never optimised against structure evidence; a band change is a candidate, scored by frozen evidence − Occam |
| FM3 | high-κ / high-degree overfit at moderate noise | H0's null-calibrated threshold; the held-out guards in `run_loop` stay; degree-lower is a remedy too |
| FM4 | compute blow-up, timeouts | caps (20 loops, wall clock = max(3 × off runtime, 600 s), configurable); memo of the core; cheap exploration configs; a timeout is recorded identically in both arms |
| FM5 | oscillation (revisiting a config) | visited-config set keyed by the config hash; never rerun one |
| FM6 | policy fitted to the families it saw | LOFO policies; dimensionless features only (rule 8) |
| FM7 | wrong diagnosis wastes loops | index stop (§6.3): stop when no remedy has predicted gain above its cost |
| FM8 | nondeterminism (torch threads, RNG) | every seed derived from a sha256 of the input arrays; `torch.use_deterministic_algorithms` where GP refits run; a determinism test |
| FM9 | fission with a wrong σ̂ breaks fold independence | the forking-paths null test on N and I measures exactly this; σ̂ error enters as a known bias, reported |
| FM10 | interaction with other layers (H0, LB, L2c, L2d) | H0 is a remedy, not a precondition; LB is held off inside controller loops (its skip decisions are about the off pipeline); L2c applies once to the final run; L2d constants are read, never changed |

---

## 2. Control space (requirement 1)

### 2.1 Classes
- **a (frozen per case):** everything in the knob inventory marked a: `P_CONCENTRATED`, `CAP`, `PRED_LOGP`, growth trigger, held-out guards, `kappa_support z`, `support_path z`, `EPS_GRID`, split-layer `snr_min`, `LOG_BF_STRONG`, complex-rerun `p_more`, the Occam term, structfit `snr_min`, `cap`, robust scale, confluent BIC, `share_z`, `outlier_frac_misfit`, outlier z², `CONCENTRATION_GRID`, `TAU2_GRID`, bayes_split `snr_min`, `Z90`. Only L2d may change them, once and globally. The controller asserts they are unchanged before and after every loop (test T4).
- **Global (b), owned by L2d / LB, not by C:** pure Monte Carlo sizes whose right value does not depend on the equation (`W_DRAWS`, split_layer `ndraw`, `split_quadratics ndraw`, `bootstrap B`, DP `draws`), step skipping (LB), `heldout frac`, `JITTER`, `confluent sep`, `M_MAX/DX_MAX` padding, DP `tokens`. C may still *raise* an MC size as a remedy for a measured symptom (a multimodal posterior), never lower it.
- **Per case (b) + nuisance, owned by C** (the declared space; every field typed, today's default first):

| group | knob | default | where today |
|---|---|---|---|
| class | `bounds` start (m, dx) | (3, 4) | `START_BOUNDS` |
| class | `dx_limit`, `m_limit` | 8, 4 | `DX_LIMIT`, `M_LIMIT` |
| class | `grow`, `recurse`, `max_depth` | True, True, 2 | `run_loop` args |
| core | `max_order`, `extra` | 8, 2 | `extract_modes_ic` |
| core | `inits`, `iters` | 8, 30 | `fit_structure` |
| core | `varpro` (VarPro poles) | False | `run_loop(refine=)` |
| decider | `top`, `min_mass`, `decide_ndraw` | 5, 1e-6, 2 | `decide_structure` |
| search | `alt_top` | 2 | `ALT_TOP` |
| search | `merge_dx0` | True | `MERGE_DX0` |
| search | `split_propose` | 0.05 | `SPLIT_PROPOSE` (proposal only) |
| search | `highk` | "off" | H0 (`Learned.highk`) |
| refine | `max_full`, `maxiter` | 6, 200 | `refine_raw.refine` (equal for all candidates of one final comparison) |
| aggregate | `dp_components`, `k_max` | 8, 4 | `dp_posterior_k`, `finite_k_posterior` |
| samples | `n_samples` used of the posterior | all given (corpus: 8 of 16 cached) | caller |
| GP (re-interpolation) | `S`, `H`, `families`, `grid`, `n_exact`, `n_nuts`, `min_family_prob`, `map_n_sub`, `map_max_iter`, hyperprior centres (lengthscale, noise) | `fit_gp` defaults | `interp/gp.py` |
| nuisance | `sigma` (white), noise model (`white` / `coloured`: draws from an AR/spectral residual fit), per-region σ (cells of `domain_report`) | input | `run_loop(sigma=, noise_draws=)` |
| nuisance | signal band `kmax` | `_raw_kmax` (largest observed \|n\| + 2) | `_raw_kmax` (a band width, and H0 widens it) |
| nuisance | effective SNR (read, used by the stop rule) | — | V0 export `log_snr` |

Knobs the inventory missed that I add: `min_mass`, `merge_dx0`, `n_samples`, `map_n_sub`/`map_max_iter`, the `refine` (VarPro) path, per-region σ, the GP hyperprior centres as proposals (they are b: GP weights are not label evidence on scattered data, where labels use the raw evidence; on grid data no GP runs). `_raw_kmax` I classify **nuisance (per case)**: it defines which bins enter the likelihood, so changing it is a candidate change that the frozen evidence then scores, with H0's null threshold when widening.

### 2.2 `RunConfig` (first build step)
- `src/pdefactor/learned/runconfig.py`: `@dataclass(frozen=True) class RunConfig` with the fields above, defaults equal to today's literals, `replace(**delta)`, a stable `key()` (sha256 of the sorted fields), and `DEFAULT = RunConfig()`.
- `run_loop(..., config: RunConfig | None = None)`. `None` means today's code path. Inside, each literal becomes `cfg.<field>` where `cfg = config or DEFAULT`; module constants keep their names and values (other sessions read them) and `DEFAULT` reads them, so L2d's `patched()` still works.
- Threading into the core: `run_core(..., max_order=, extra=, inits=, iters=)` pass-through keywords with today's defaults (`aggregate.run_core` already forwards `**core_kw`; `analyze_structured` and `extract_modes_ic` get the keywords; `fit_structure` already takes `inits/iters`). This touches `core/` → tests T2.
- Re-interpolation: `learned/controller.py:reinterpolate(raw, cfg, seed)` calls `fit_gp` with the GP fields and returns (samples, pis, noise_draws). Only for scattered data with `raw` given.
- Hook region in `loop.py`: the signature, the `cfg` line, and literal → `cfg.` substitutions. No change of behaviour with `config=None`; the golden off test and a new test "`config=RunConfig()` equals `config=None` bit for bit on the 6 golden draws" guard it.

---

## 3. The loop (requirement 2)

### 3.1 API
```python
def run_controlled(samples, t, x, sigma, pis=None, *, raw=None, noise_draws=None, bootstrap=0,
                   learned=None, policy=None, max_loops=20, budget_s=None, fission=True,
                   seed=None, **run_loop_kw) -> ControlledResult
```
- `ControlledResult`: the final `LoopResult` (`result`), `actions` (list of (loop, diagnosis, remedy, config key, seconds, accepted)), `n_actions`, `stop_reason`, `visited` (posterior over visited structures + `missing_mass`), `fission` info (τ, σ̂ used, fold seeds), `confirmed` (bool per changed structure and direction), `runtime`.
- `learned=Learned(controller=True)` in the corpus harness calls `run_controlled` instead of `run_loop` (`ll_corpus.py` arm `controller`). `run_loop` itself never calls the controller (no recursion; LOFO-safe).

### 3.2 Steps
1. **Off run** on the full data with `RunConfig()` → `R0` (this is also the fallback answer). Diagnose `R0` (§6.1).
2. **Early stop** (§5) if identifiability fails or no diagnosis is active → return `R0` with the reason.
3. **Fission** (§4) → folds A, B (independent, same design).
4. **Search on A** (loop k = 1, 2, …): the policy picks (diagnosis, remedy) → config `c_k` = `c_{k−1}` + delta (cumulative, so remedies compose); run on A with the cheap exploration profile; diagnose; update the visited set; stop by the index rule (§6.3), the caps, or no remedy left.
5. **Pick** `c*_A` = the visited config whose run on A has the best frozen refined evidence − Occam *and* resolves the most diagnoses (lexicographic: fewer active diagnoses, then evidence).
6. **Confirm on B:** refine on B, with equal refine budget, the final structure of `c*_A` and that of `R0`; one comparison of evidence − Occam on B. Swap roles (search on B, confirm on A) → `c*_B`.
7. **Final run** on the full data with the accepted config, with the full (non-exploration) profile:
   - if `R0`'s factor set and label are unchanged by `c*` → report the `c*` run (better coefficients / intervals allowed; no forking risk to the factor set);
   - if the factor set changes → accept only if confirmed in **both** directions; else report `R0`, and note "controller proposal not confirmed out of fold".
8. **Report:** labels from the final run's frozen scoring; `visited` posterior; actions; stop reason.

### 3.3 Cheap exploration
- Exploration profile on folds: `split=False`, `bootstrap=0`, `report_domain=False` (they do not change the factor set or label before the split layer; the split layer can drop redundant factors, so it runs in step 6–7).
- Per-call memo of `_run` keyed by (config fields that affect the core, structures, real flag, sample bytes hash): a remedy on refine/alternatives/split reuses the core results. Memo lives in the controller, passed as `run_loop(..., _memo=)`; `_memo=None` (default) is today's path.
- Wall clock: `budget_s = max(3 × off runtime, 600 s)` by default; checked before each loop with the predicted cost of the next remedy (from the LB-style cost model, §6.2).

---

## 4. Honesty rule, re-examined (requirement 3)

| old rule | keep / change | why |
|---|---|---|
| frozen scoring | **keep** (user decision) | it is the only label authority; a per-case scoring change is the classic forking path |
| declared search space (structures within `bounds`) | **change**: the declared space is the typed `RunConfig` (§2.1) plus the nuisance estimates; structures are whatever runs on those configs produce | declaring structures only restricted; declaring the knob space is what controls the multiplicity |
| equal refine budget per candidate | **change**: equal only in the final comparison (step 6), exploration may be cheap | the forking risk is in the comparison, not in the search |
| report everything | **keep, sharpened**: posterior over all visited structures (weight ∝ exp(held-out evidence − Occam) on the confirm fold, averaged over both directions) + Good–Turing missing mass N₁/N over loop proposals | gives the reader the multiplicity |
| optional confirm split | **change: mandatory cross-fitted data fission** whenever the factor set would change | protects against false discoveries at no data cost (see below) |

**Fission (Leiner et al. 2025):** with white Gaussian noise of known σ, draw Z ~ N(0, σ̂² I) from the case seed; A = y + τZ, B = y − Z/τ, τ = 1. A and B are independent, each with noise variance 2σ̂², and keep the design (same grid, same scattered points), so the same pipeline runs on each. Coloured noise: Z ~ N(0, Σ̂) from the coloured model. Scattered data: fission `raw.ys`, then re-interpolate each fold (`reinterpolate`, GP cost counted). Grid data with GP-free path: fission the grid.
- **Why accepting only when confirmed both ways protects:** a structure that the search on A found by fitting A's noise has no reason to beat `R0` on B's independent noise (universal-inference logic: search on one part, one pre-specified comparison on the other). Requiring it in both directions makes a spurious acceptance need two independent coincidences.
- **σ̂ dependence:** fission is exact only for known σ. σ̂ comes before fission from structure-free estimators (input σ; else the GP noise posterior on scattered data, or the high-band MAD on a grid). The null test (§7) checks the residual dependence empirically. No theory beyond that: stated as a limit.
- **Cost of fission:** each fold has half the information, so the search is less sensitive than on the full data. That is the price of the guarantee; the final run uses the full data.

Alternatives compared in the build (on N + a G subset, before the full corpus): (a) cross-fitted fission (default), (b) single fission A→B without swap, (c) no fission, search on the full data with the final comparison on the full data (the old rule). (c) is the forking-paths control: it should fail the null test at depth if forking paths are real here; if it does not, (b) or (c) are cheaper and the plan says so.

---

## 5. High noise (requirement 5)

- **Identifiability check before any search** (T13, T40, T46): per factor of `R0`, the number of distinct |κ| with modes above noise vs the coefficients needed (V0.2 margin), and the export `log_snr`. If every factor has margin < 0, or no mode is above noise, the controller **stops with no search**, reason "SNR below identifiability: <counts>".
- **Label question (open, see §10 Q1):** the brief asks to "stop early with UNDECIDED". The common rule says a layer never sets a label. Default: the controller does not relabel; it returns `R0` (whose frozen label at such SNR is normally UNDECIDED or ID-KER) and adds the reason to the note. If `R0` says FIT-COMPATIBLE below the identifiability level, that is a frozen-scoring finding for L2d and is reported, not overridden.
- **Never search until something fits:** the loop stops on the index rule, not on "a FIT-COMPATIBLE appeared"; a new FIT-COMPATIBLE needs the out-of-fold confirmation.
- **Moderate-noise remedies to measure** (one-step logs, §6.4): more GP samples (`n_samples` 8 → 16, `S` 16 → 32), narrower band (`kmax` to the bins with mode SNR ≥ the frozen `snr_min`), lower degree bounds (start (2, 2), `dx_limit` −2), aggregating draws (more samples pooled in `run_core`), more restarts. Reported per noise level in REPORT.md.

---

## 6. Policy (requirement 4)

### 6.1 Diagnosis (deterministic signals → multi-label)
Signals already in `LoopResult` / V0 (no new scoring): UNDECIDED reasons (no modes / too few modes / confluent), MISFIT outlier fraction, ID-KER unsupported degree, V0.1 (data unexplained at κ), V0.2 margin, V0.3 (next structure within log BF 3), V0.10 (weights inseparable), sample disagreement and screened samples, bounds at `DX_LIMIT/M_LIMIT`, growth rejected by the overfit guard, factors dropped by raw_subset / refine / split layer, H0 band widening, timeout. Diagnoses (14): `too_few_modes`, `misfit_outliers`, `degree_unsupported`, `confluent`, `unexplained_kappa`, `ident_margin`, `ambiguous_structure`, `weights_inseparable`, `samples_disagree`, `at_class_limit`, `growth_overfit`, `spurious_dropped`, `low_snr`, `timeout`. The calibrated version (§6.2) predicts per remedy, so the diagnosis model and the reward model are one model.

### 6.2 Models compared (simplest first; ship the simplest that passes)
| arm | what | trained on |
|---|---|---|
| **C0 rules** (baseline) | `RemedyTable` default order (PHASE4 §4 C table extended to the remedies of §6.4), fixed depth K = 3, no learning | — |
| **C1 table** | `RemedyTable` Beta lower bound per (diagnosis, remedy), per unit cost, index stop | one-step logs |
| **C2 contextual** (option i) | per-remedy success model p_r(x) (L2-logistic on dimensionless features + diagnosis one-hots; isotonic calibration on the cal split), cost model c_r(x) (log-runtime ridge), Weitzman-style index stop. Offline exploration by Thompson sampling (bootstrap ensemble of the logistic); at deployment greedy on the 10 % lower bound (deterministic) | one-step + multi-step logs |
| **C3 BO** (option ii) | Optuna TPE (seeded) over the continuous knobs on fold A, objective = fold-B evidence − Occam of the run's final structure, 20 trials | run live on a subset (G-test F1–F3, 30 cases) only |
| C4 offline RL (option iii) | IQL (d3rlpy) on the logged transitions | only if C2 vs C3 leaves a clear gap (pre-registered: C3 − C2 right-set > 0.05 with CI excluding 0) |

Features: the V0 exports (`kappa_vand`, `log_snr`, `disagreement`, `split_floor`, `log_nobs`, `mode_margin`, `rel_width`), the diagnosis bits, loop index, remedies already applied (one-hot), noise design. All dimensionless (rule 8).

### 6.3 Stopping rule (learned)
Continue while max_r [p_r(x) · G − λ · ĉ_r(x)] > 0 and caps hold, where p_r = calibrated lower bound of "this remedy turns the current wrong/unsure output into a better one", G = 1 (one case fixed), ĉ_r = predicted seconds, λ = price per second. λ is one global knob, chosen on the fit split as the knee of right-set vs runtime and then frozen; reported. Also stop when no diagnosis is active, when every applicable remedy was tried, or on a confident `low_snr`. (Weitzman's index for binary rewards; values are correlated, so indices are recomputed after each loop — heuristic, stated.)

### 6.4 Remedies (discrete config deltas; cumulative)
`more_samples` (n_samples ×2, or GP S ×2 by re-interpolation), `more_restarts` (inits ×2, iters ×2), `wide_alternatives` (alt_top 4, top 8), `highk_scan` (H0 on), `narrow_band`, `lower_degree` (start (2,2), dx_limit −2), `raise_limit` (dx_limit +2, m_limit +1), `max_order_up` (max_order 12, extra 4), `varpro` (core VarPro poles), `coloured_noise` (noise model from residual AR/spectral fit), `regp` (GP refit with three-family set and hyperprior centres from the data scale; scattered only), `more_mc` (decide_ndraw 8, split ndraw ×4), `refine_budget` (max_full 10, maxiter 400; applied to both arms of the final comparison), `deeper_recursion` (max_depth 3). Each has a precondition (e.g. `regp` needs `raw`), a predicted cost, and a seed derived from the case hash.

### 6.5 Training logs (randomised actions)
- **One-step logs:** for each fit-split case of G, S (and I when V1 delivers `ll_I.jsonl`), from the off state, apply each *applicable* remedy whose precondition holds, plus one uniformly random non-indicated remedy (ε-exploration with recorded propensity), on the full data with the exploration profile. Record the category change vs truth, the false-confident flag, runtime. Reward: +1 wrong/abstain → right; −3 → new false-confident; 0 otherwise; cost separate.
- **Multi-step logs:** on 30 % of the cases, a random sequence of 3–5 remedies (uniform over applicable ones, propensities recorded), for the sequential features and the stop model.
- **Off-policy evaluation:** IPS and doubly robust (Dudík et al. 2011) estimates of C1/C2 policy value on the logs before any live gate run; a policy whose DR value is not above C0's is not taken to the live gate.
- **Null logs:** the same randomised actions on N (fit seeds 300–309) → the per-remedy false-FC rate, used as a hard constraint (a remedy with any N false-FC at depth 1 is removed from the policy for that diagnosis).

---

## 7. Gate (§2.4 unchanged, plus C's requirements)

Run with `analysis/exp/ll_gate.py --arm controller --target right`, on the test split (G 128–135, S 209–211) with **LOFO policies** (the policy for a test case is the one trained without its family: one live run per test case serves both the test-split and the LOFO check; this is stricter than an in-family policy).
1. Right-set improves, paired bootstrap CI excluding 0 (§2.4.1).
2. Right-set ≥ off − 0.02 and false-confident ≤ off (§2.4.2).
3. Coverage not worse by > 0.02 (§2.4.3).
4. **Forking-paths null test:** on N (all 40) and I (V1's corpus, when available), the false FIT-COMPATIBLE rate is ≤ off **at every loop depth k = 0…20**: the would-be output after each loop is recorded with the stopping rule disabled (forced depth 20), and the confirm step applied at each k.
5. Named cases (`ll_named.py`) not worse in any cell.
6. Per family (LOFO table), runtime (median, p90) and actions per run (mean, histogram) reported.
7. Fresh-context reviewer subagent (`experiment-audit`, `result-to-claim`, `kill-argument`).

If C2 passes, C0/C1 are also reported; the simplest arm that passes ships. If none pass, the layer stays off.

---

## 8. Tests (written before the code)

| test | checks |
|---|---|
| T1 `test_learned_off.py` (existing) | stays green |
| T2 `test_runconfig.py` | `RunConfig()` fields equal today's literals (read from the modules); `run_loop(config=RunConfig())` = `run_loop(config=None)` bit for bit on the 6 golden draws; core pass-through keywords with defaults give identical `analyze_structured` output; a non-default `inits` reaches `fit_structure` (spy) |
| T3 `test_learned_controller.py::test_off_identity` | `Learned(controller=False)` path unchanged; `run_controlled` with a policy that never acts returns `R0` exactly |
| T4 `::test_frozen_scoring` | every class-a constant hashed before and after `run_controlled`; equal |
| T5 `::test_fission` | A, B independent: empirical correlation of the fold noises ≈ 0 over 2000 draws; A + B = 2y (τ = 1); same seed → same folds |
| T6 `::test_confirm_required` | a stub policy that forces a spurious extra factor on a pure-noise grid: the final label is `R0`'s, note says "not confirmed" |
| T7 `::test_determinism` | two runs on the same input → identical actions, configs, result |
| T8 `::test_caps` | max_loops and budget_s respected; actions reported; visited configs never repeated |
| T9 `::test_early_stop` | pure-noise and κ-poor inputs stop with no loop and a reason |
| T10 `::test_visited_report` | visited posterior sums to 1 − missing_mass; missing_mass = N₁/N on a constructed sequence |
| T11 `::test_memo` | memoised `_run` gives the same result as unmemoised; second call does not recompute (counter) |

---

## 9. Data and compute

- **Inputs:** shared off rows in `D:\Larned layers\PDEFactorML\analysis\exp\out\` (`ll_S.jsonl` now; G and N when the parent's runs write them; `ll_I.jsonl` from V1). GP caches from `...\analysis\exp\cache\`. My outputs: `analysis/exp/out/ll_C_*.jsonl` in this worktree.
- **Scripts:** `analysis/exp/ll_C_logs.py` (randomised one-/multi-step logs, through `slots.Pool()`), `ll_C_train.py` (C1/C2 fit, OPE), `ll_C_bo.py` (C3 subset), corpus arm `controller` in `ll_corpus.py`.
- **Estimates** (median off runtime ≈ 150 s; memo saves ≈ 40 % on refine-side remedies; ≈ 5 applicable remedies per case):
  - one-step logs: G-fit 200 + S-fit 70 cases × ~5 × ~110 s ≈ 41 slot-h; N 40 × 5 × ~30 s ≈ 2 slot-h;
  - multi-step logs: 80 cases × 4 × 110 s ≈ 10 slot-h;
  - live gate: G-test 80 + S-test 30 + N 40 (forced depth 20 on N) + named ≈ (K + 3) × off per diagnosed case + fission GP refits ≈ 35 slot-h;
  - C3 BO subset: 30 × 20 × ~60 s ≈ 10 slot-h.
  - Total ≈ 100 slot-h; at 6 of the 10 machine slots ≈ 17 h wall, all in the background, below-normal priority, `OMP_NUM_THREADS=1`.
- **Cuts if over budget (in order):** S logs to 400 pts only; multi-step logs to 40 cases; C3 dropped (reported as not run); N forced depth to 10.

---

## 10. Questions for the parent (defaults in brackets; I start the build on approval with the defaults)

1. Early stop at low SNR: relabel to UNDECIDED, or keep the frozen label and add the reason? [Keep the frozen label; reason in the note; a FIT-COMPATIBLE below the identifiability level is reported to L2d.]
2. Core change: pass-through keywords `max_order`, `extra`, `inits`, `iters` in `analyze_structured` / `extract_modes_ic` with today's defaults, covered by T2. [Yes.]
3. `loop.py` hook region: signature (`config=`, `_memo=`) plus literal → `cfg.` substitutions across `run_loop` and the helpers it calls. This is wider than one hook line; merge conflicts with H0/L2c/LB hooks are textual only. [Yes; I rebase on `learned-layers` before handing over.]
4. CPU: 6 of the 10 slots for ≈ 17 h of background logs and gate runs. [Yes, shared fairly through `slots.py`.]
5. Corpus I: wait for V1's `ll_I.jsonl` for the null test; if it is late, gate on N and report I as pending. [Yes.]

---

## 11. Proposed THEORY_TO_ALGO rows (add-only; numbers for MAIN to assign)

| # | result (status) | what it says | decision |
|---|---|---|---|
| TC-1 | data fission, Gaussian case (Leiner et al. 2025, CON-FONTE) | with known Σ, y + Z and y − Z are independent with the same design | controller search on one fold, confirmation on the other, swapped; σ̂ fixed before fission |
| TC-2 | universal inference (Wasserman et al. 2020, CON-FONTE) | arbitrary search on one part and one pre-specified comparison on an independent part keeps validity | a factor-set change is accepted only if confirmed out of fold in both directions; else the off answer stands |
| TC-3 | Weitzman 1979 (CON-FONTE; optimal for independent boxes) | open by reservation index, stop when no index beats the current value | learned stop: continue while max_r p_r G − λ c_r > 0; heuristic under correlation |
| TC-4 | T13, T40, T46 (DIMOSTRATO / CON-FONTE) | fewer distinct observed κ than coefficients cannot identify a factor | no controller search when every factor's V0.2 margin is negative |

---

## 12. Parent's approval (2026-10-29, add-only)

Approved. Answers:
- Q1: C never relabels. It returns R0 with the reason in the note; a FIT-COMPATIBLE below the identifiability level is reported to L2d.
- Q2: yes; pass-through keywords with today's defaults, covered by T2 and the golden test.
- Q3: yes. ONE memo mechanism: C owns the `_memo=` parameter and its key design; LB's exact per-run cache (behind `budget=True`) uses it. Interface agreed with LB directly. Literal → `cfg.` substitutions stay mechanical: one line per constant, no reformatting.
- Q4: up to 6 slots; first-come in `slots.py`, so wall clock stretches. One-step logs run first (they unblock C1/C2).
- Q5: gate on N, I marked pending if late (V1 promised I at ≈ 7 h).

Additions:
- Step 7 with the factor set unchanged: if c* changes coefficient intervals, coverage for the c* runs is reported separately (L2c is calibrated on off runs; with C on its scale may not apply).
- Alternative (c), no fission, runs in the null test at every depth. If (c) passes too, the report says so plainly.
- A remedy removed by the N null logs stays removed for the gate; no re-adding after looking at the test split.
