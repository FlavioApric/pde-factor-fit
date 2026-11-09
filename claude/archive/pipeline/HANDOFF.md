# HANDOFF — PDEFactorML main session (written 2026-10-30)

For the next session that continues the main-session work (outer loop, refinement, decider, benchmarks, generalisation). Read this file first, then `CLAUDE.md`, then `analysis/THEORY_TO_ALGO.md`.

## 00. Update 2026-11-01 (supersedes the state in §1–§8 where they disagree)

**Main = `74765a2` (local, not pushed).** Adopted since 2026-10-30, all on by default (env `=0` disables each):
- T77–T81, T85 WARM_BINS, T87 triangular solve, T88 RAW_GOF, T89/T91 complex σ, T92 run_loop purity, T93 (T88 calibrated);
- T94 SVD guard; T95 df-adjusted excited-band equivalence (benchmark scoring, `e13_summary.EQUIV_DF`);
- T96 GRID_SMOOTH_GOF (excited-band Neyman smooth residual test, downgrade only);
- exact evidence speed-ups from T97 (bincount profile sums, vectorised `_basis_groups`);
- the bundle T98–T102: CONJ_HALF (half-plane complex fit of real fields) + BRANCH_ARD (one prior scale per root branch), with SPLIT_FINEST (T99), PATH_CLASS (T100), RAW_GOF_FINAL (T101b), PATH_FULL (T102) following BRANCH_ARD; per-bin bound clamp (T101a); bootstrap keeps copies that drop a bare split-off factor;
- T103 (scat-beam, cherry-picked): SPLIT_CI (intervals of an exact split carried through the split map by Monte Carlo, instead of zero-width) and IDKER_FINAL (core ID-KER mass re-checked on the reported factors; kappa support recomputed on the final factors and shared by a conjugate pair). Both default = BRANCH_ARD (`PDEFACTOR_SPLIT_CI`, `PDEFACTOR_IDKER_FINAL`).
- NOT adopted (switch off, code kept): T83 GROW_PAST, T84/T90 EPGP_REINTERP, T97 FIT_GUARD / ALT_PRE (fc regressions F2-135, F4-128, F4-209).

**Results (A/B v5, bundle on; refs = main before):**
- final benchmark P8, 30 inputs (10 cases × grid 1 %, grid 5 %, 400 points 5 %): pipeline **30/30 right, 0 false-confident** (ref 29 + 1 FC); weak SINDy 23, ensemble 19, SBR 20, PDE-FIND 4, BOP-DMD 1. Report: `benchmarks/out/p8_final_v5.md` (generator `benchmarks/p8_report.py`).
- E13, 20 random draws: pipeline 12 right + 7 equivalent + 1 abstain-ok, 0 false-confident (ref 10 + 9 + 1 FC); SINDy ≤ 6 right.
- heldout 13/14 right factors (ref 11, false-confident 1 → 0); conjugate 11/11 (ref 10); fc 4 right / 8 equivalent / 0 FC.
- Costs of the bundle, now fixed by T103 (single runs, no suite A/B): beam 400 s0/s2 cover90 0.5 → 1.0, beam 2000 s2 and P8 beam 400 1 % FIT-COMPATIBLE again, E13 F1-3 ID-KER under-claim gone. Beam 400 s1 stays at cover90 0.5 (honest 90 % miss, v4 too).
- Full suite on main: all green after updating the default-switch tests.

**ML layers (P7, `D:\Larned layers`, `learned-layers` = `ll-sync` = 28ae435, local):** V1 validator NO-SHIP (detection 0–8 % per family), stays off; LB memo on (bit-identical, no longer faster); controller C′ not built — oracle ceiling 8/12 failures, but no trigger finds them (V1 0/12; T96 / V0.1 / T88 0/12; data in `sessions/LEARNED/C/cprime_oracle_p7.md` and `analysis/exp/out/cprime_trigger_p7.md`). So pipeline + ML = pipeline. **Decision on C (user, 2026-11-01): C and C′ are NOT built.** The ML layers stay as they are (V1 off, LB memo on); pipeline + ML = pipeline.

**Open:** T69 confluence relabel (two_pairs keeps the true factors but stays UNDECIDED); BRANCH_ARD does not charge a factor with no excited branch (bare τ, T99 note); two_pairs 5 %; the CONJ_HALF complex run on beam 400 s1 still refines badly (evidence reverts it correctly).

**Branches / worktrees (local; ask the user before deleting):** `C:\Users\<user>\pdef-wt\` t82-f5131, t83-two-pairs, p8-report, t95-f4128, t96-v01-guard, int-t97, int-final, int-boot, scat-beam. All merged into main except t96-v01-guard / int-t97 (T97, not adopted) and scat-beam (T103 merged).

## 0. Start here

**Rules (binding; from CLAUDE.md and the user):**
- Rule 8, the gold rule: every change is general (any factor structure, order, coefficient scale, PDE in scope). Justify it from theory or a scale-free criterion, and test it on held-out families, never only on the case that exposed the bug.
- Accuracy before speed, even when it costs a lot more time. A speed-up is allowed only if it is exact (same decisions).
- Keep the structure. Same pipeline steps, same outputs, same interfaces. An algorithm inside a step may change; a step changes only if that is indispensable.
- Work loop: micro-benchmarks of at most 15 inputs, each aimed at one problem → fix → rerun → repeat (`benchmarks/micro.py`).
- The ML layers must stay usable after every change. `tests/test_ml_contract.py` pins the entry points, helper signatures, result fields and knobs they use; when an interface has to change, keep the old one and add a new one.
- Theory first (rule 7): read THEORY_TO_ALGO, query the graphs, cite the LEDGER row. Add new rows; never remove or rename.
- Plans and docs: add only. Labels: FIT-COMPATIBLE / MISFIT / ID-KER / UNDECIDED, never "law identified".
- The core (`src/pdefactor/core/`) changes only with tests. The outer layer is Bayesian, with Monte Carlo and no linearisation.
- `D:\ProblemaBase` is read-only (only its `graphify-out` may be written). Leave `PDEFactorML/EXPLAINED/` alone; the user edits and commits it.
- Never read `D:\Larned layers\<private notes file>`.
- Out of scope (parked, raise again later): nonlinear, variable coefficients, fractional, 2+1/3+1, non-monic in τ.

**Commands:**
- Python: `D:\PDEFactorML\.venv\Scripts\python.exe`. Quick tests: `.venv/Scripts/python.exe -m pytest -q tests/test_general.py tests/test_ml_contract.py tests/test_refine_grid.py tests/test_validate.py`. The full suite takes about 30–60 min.
- Commit through the D: repository (the nested `PDEFactorML/.git` is stale), staging only `PDEFactorML/` files and never `EXPLAINED/`:
  `git -c safe.directory=D:/ -c user.name=flavi -c user.email=<email> -C D:/ add PDEFactorML/<files>`
  Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Ask the user before any push (remote ML-PDE-fit).
- Line endings: `loop.py`, `refine_raw.py` and `validate.py` are CRLF; `bayes_split.py` has mixed endings. Do not use `sed -i` (it converts to LF). Patch with a Python script that keeps the endings (examples in the previous session's scratchpad: `patch_perbin.py`, `patch_validate.py`).
- Micro suites: `.venv/Scripts/python.exe benchmarks/micro.py <suite> --tag <tag> --ref <old tag> --workers N`, plus `--report` for the table. Suites: `speed`, `conjugate`, `heldout`, `edge`, `intervals`. One process per input, resumable: inputs already in `benchmarks/out/micro/<suite>_<tag>.jsonl` are skipped.
- Archive data: `.venv/Scripts/python.exe benchmarks/archive.py` copies `benchmarks/out/*.jsonl` and `micro/*` to `benchmarks/data/` and updates `INDEX.md`. It takes no arguments, and even `--help` runs it.
- Workers: the learned-layers runs have stopped, so main may use 4 workers (more when nothing else runs). The CPU has 6 cores.
- Graphs: the code graph is `D:\PDEFactorML\graphify-out` (updated 2026-10-30 for this handoff). Use `cd D:/PDEFactorML && graphify query "<question>"`. The theory graph is `cd D:/ProblemaBase && graphify query "<topic>"`.

## 1. State of the code

| commit | what |
|---|---|
| e1fb9ae | T70–T75: tie rules (`_beats`, `LOG_BF_BARE` = 1 nat), refined-estimator grid bootstrap, ML contract test, data archive |
| 125b1f2 | (the user's commit "Update D: contents"; it also carried this session's T76 code) T76 per-bin amplitude prior scale, **off by default**: `refine_raw.TAU2_PER_BIN`, environment variable `PDEFACTOR_TAU2_PER_BIN=1`; `_basis_groups`, `_grid_spectrum(groups=)`, `_per_bin_neg` (L-BFGS-B, analytic gradient, per-bin relative bounds); `bayes_split.raw_evidence` uses it when on; 2 tests in `test_refine_grid.py` |
| 435b048 | V0.1 `predictive_bins`: exponential columns scaled per mode (a growing mode overflowed `exp(λt)` and crashed the least-squares SVD; reported by the learned-layers runs, 25 of their runs crashed on it). Test `test_v01_growing_mode_does_not_overflow` fails on the old code |
| (this handoff) | HANDOFF.md, the T76 verdict in THEORY_TO_ALGO, ML_INTEGRATION update, archived T76 partial data |

**T76 verdict: not adopted; it stays off.** Partial results with it on (the run was stopped for this handoff):
- held-out: 9/12 right, the same count as the reference (`heldout_v1`). The gain on cubic_tau comes from T75, not T76, because `heldout_v1` predates T75.
- **Regression:** `wave_lowk` (only low κ excited). The reference split it into τ ± ξ; with T76 it reports the unsplit τ² − ξ². The likely cause is that each empty bin gets its own scale and fits a little noise (under 1 nat per bin); with many empty bins this adds up and moves the split-versus-unsplit comparison. **Not verified.**
- 2–4× slower: damped_beam 400 took 9,683 s against 2,173 s, because an L-BFGS runs inside every evidence evaluation inside the refinement.
- damped_beam 400 s0 is still wrong. It is data-equivalent: the pair fits better by 1.5 nats after T76.
- Possible general repair to test: pool the empty bins under one shared scale (bins with no data energy above noise, decided by a χ² test against the noise); keep a separate scale per excited bin only. Then rerun `heldout` and `conjugate` and check `wave_lowk`, damped_beam 400 and the time.

## 2. Problems met in testing → test → solution

Each fix's full reasoning and LEDGER citation is in THEORY_TO_ALGO (T-number). Tests are in `tests/`.

| problem (where it showed) | solution | T | test |
|---|---|---|---|
| fixed `ftol` falsely factors KG and telegraph under noise (E1) | structured factor fit with posterior over structures (core v2) | v2.1 | `test_core_v2::test_noisy_factor_set` |
| repeated roots reported as a confident simple factor (E4) | confluent model → UNDECIDED; VarPro + LM confluent test | T60, T67 | `test_core_v2::test_repeated_factor_is_undecided`, `test_confluent_test_separates_repeated_from_close_poles` |
| shared κ = 0 mode merged factors | structfit handles it; min-norm split = posterior mean | 0b.10 | `test_core_v2::test_shared_kappa0_mode` |
| GP error correlated in t (heat 400) | GLS per-bin noise (`BinNoise`) | T37 | `test_phase3::test_binnoise_recovers_ar1_autocovariance`, `test_gls_with_white_draws_matches_white_core` |
| mode-level BIC prefers fake τ + c per κ | data-level decider by kernel evidence | T39 | `test_phase3::test_decider_rejects_constant_factors_per_kappa` |
| symbol through too few modes (Schrödinger 1 %) | admissibility counts observed roots, at most m per κ | T40, T46 | `test_decider_rejects_symbol_that_interpolates_few_modes`, `test_decider_counts_only_observed_branches` |
| GP mean adds its own decay as a factor (heat 400) | raw-data evidence for scattered data | T44 | `test_raw_evidence_rejects_interpolation_artifact` |
| no posterior spread on one grid | parametric bootstrap; later of the refined estimator | T50, T75 | `test_bootstrap_intervals_cover_heat_coefficient`, `test_general::test_bootstrap_of_the_refined_estimator_keeps_supported_terms` |
| real field, complex model: weight under-coverage (E5) | conjugate-pair parametrisation, empirical-Bayes τ² | T38 | `test_bayes_split_weights_cover_truth_and_null` |
| cubic in τ unreachable (orders ≤ 2) | candidates up to m_max | T57 | `test_general::test_candidates_include_order3_irreducible`, `test_core_fits_irreducible_cubic_in_tau` |
| reducible factors other than square-discriminant quadratics | branch-partition split, accepted by refined evidence | T54 | `test_split_branches_reducible_products`, `test_split_branches_leaves_irreducible_heat_and_transport` |
| absolute 1e-9 imaginary test not scale-free | `_nonreal` relative + interval | T58 | `test_nonreal_is_scale_free` |
| growth only in dx | grow (m, dx+1) and (m+1, dx) | T59 | `test_grow_options_both_directions` |
| branch point of an irreducible law flagged confluent (damped beam UNDECIDED) | branch-point test; re-check on final factors and on their product | T60, T69, T73 | `test_branch_point_of_irreducible_law_is_not_confluent`, `test_confluent_bins_rechecked_against_final_factors`, `test_confluent_bins_between_factors_rechecked_on_their_product` |
| compatible fit with structured residual | V0.1 posterior-predictive trigger | T61 | `test_validate::test_v01_calibrated_under_truth_and_flags_missing_factor` |
| refinement slow on grids | exact per-bin-pair grid evidence, batched | T62 | `test_refine_grid::test_grid_evidence_*`, `test_vectorised_grid_spectrum_equals_reference` |
| cubic_tau looked like a product of lower-order factors | refinement-stage merges | T63 | (covered by the held-out suite; cubic_tau grid right since T75) |
| split penalised for the expanded product's near-zeros | Occam on min(parameters) | T64 | `test_n_real_params_counts_the_product` |
| complex split of a real law not closed | `_conj_closed` | T65 | `test_conj_closed` |
| same model under two labels compared on optimiser noise | `_supports` same-model signature, then on the product | T66, T68 | `test_supports_identifies_the_same_model_across_structure_labels`, `test_supports_matches_a_conjugate_pair_with_its_product_only` |
| beam 5 %: conjugate split lost on a hair | same-family tie rule | T70 | conjugate suite (beam rows) |
| damped beam: complex factors only approximate the real quadratic | refine the unsplit real factor too, revert by evidence | T71 | conjugate suite (damped_beam grid) |
| junk decider pick, right structure not refined (beam 5 % s2) | refine every scored alternative (`ALT_TOP = None`) | T72 | conjugate suite |
| beam 400 5 % s1: 0.2-nat displacement by an extra term | bare-mention rule `_beats`, `LOG_BF_BARE` = 1 nat | T74 | `test_bare_mention_tie_rule`; conjugate v4: beam 400 s1 and s2 fixed |
| cubic_tau constant pruned by the core-bootstrap interval | bootstrap the refined estimator | T75 | `test_bootstrap_of_the_refined_estimator_keeps_supported_terms` |
| damped_beam 400: shared τ² penalises an unexcited κ = 0 mode | per-bin scale (T76) | T76 | `test_per_bin_evidence_equals_dense_maximum`, `test_per_bin_grid_equals_dense_and_ignores_unexcited_bins`; **not adopted** (see §1) |
| growing mode crashes V0.1 SVD (learned-layers corpora) | per-mode column scaling | (numerical) | `test_v01_growing_mode_does_not_overflow` |
| ML layers silently broken by a signature change (`_basis` gained a kwarg) | keep the old signature, add `_basis_groups` | (contract) | `test_ml_contract::test_loop_helpers_keep_their_signatures` |

**Latest micro-suite results (reference for the next loop):**

| suite | tag | right | code | notes |
|---|---|---|---|---|
| conjugate (11) | v4 | 10/11 | e1fb9ae-era | only two_pairs wrong |
| heldout (14) | v1 | 10/14 | before T75 | misses: two_pairs grid and 400, damped_beam 400 s0, cubic_tau grid (fixed by T75) |
| intervals (14) | v1 (current file, 14 rows) | 13/14 | e1fb9ae | damped_beam 400 s2 wrong; mean cover90 ≈ 0.93 |
| heldout | pb1 (T76 on) | 9/12 | 125b1f2 + T76 | stopped; see §1 |
| edge (7) | v1 | 4/7 | c304fb9 (run 2026-10-30, 966 s) | `repeated_transport` grid at 1 % and 5 %: UNDECIDED, which is the honest label for a repeated root (OPF5B-T6), but the scorer counts it as wrong, so the scorer needs fixing, not the pipeline; `transport_plus_diffusion` 400 5 %: wrong, as in run 6 (high-κ loss, §4.1); right: `tpd_shared_kappa0`, `fifth_order` (small high-order term kept), airy 400 5 %, heat 400 5 % s1 |

Full-benchmark reference: run 6 (`benchmarks/data/e2e_run6.jsonl`, summary `benchmarks/out/e2e_summary.md`): the pipeline is ≥ every SINDy variant in all 9 sampling × noise cells.

## 3. Open problems tied to generalisation

1. **two_pairs** (a real field with two complex-conjugate pairs, (τ² + 0.09ξ⁴)(τ² + 0.01ξ⁶)): wrong on grid and at 400 points. The data-equivalent answer wins because the true structure needs total m = 4 and dx = 6, which is beyond the current growth bounds (`M_LIMIT`, `DX_LIMIT`) and the conjugate canonicalisation for several pairs (G5) is only partly exercised. Next: allow growth to the class the data need when V0.1 still fails (a general rule, no case-specific bound), and test conjugate matching for n_pairs ≥ 2.
2. **Per-bin prior scale (T76)** is right in principle (R4-T4/R4-T6: empty bins carry no information) but its plain form regresses splits (§1). This decides whether the evidence is fair to laws without a constant term when κ = 0 is not excited, which is a general issue, not a damped_beam one.
3. **G11, weights over the δ(P) ambiguity** (shared κ = 0 mode, TPD weight cover about 0.4): report the weight interval over the ambiguity, with the shared part shown separately. Not started.
4. **Scale invariance and spectral variety** (plan v2.13 items 8–10: rescaled coefficients, flat or low-κ-only spectra, correlated noise): partly covered by heldout (`tpd_scaled`, `transport_fast`, `advdiff_flat`, `wave_lowk`). `wave_lowk` is the case T76 broke. AR(1) noise is not in any suite.
5. **E13 random PDEs** (simulator F1–F5, 20 draws, code before 435b048): strict right 8/20 for the pipeline vs 6/20 for the best SINDy. Among the 16 identifiable draws, 7 are right; misses F2 s0/s1, F3 s1/s2/s3, F4 s3, F5 s2/s3, F1 s3 (several are ID-KER or data-equivalent abstentions, not wrong answers). Rerun on current code, and classify each miss as honest abstention, data-equivalent or wrong.
6. **Benchmark design:** scattered "seeds" share one simulated field (`any_case` uses seed 0); only the sample points and noise change. Repeated misses are not independent evidence. Add independent fields per seed (a benchmark change, not a pipeline change).
7. **Learned calibration constants** (LOG_BF_STRONG, P_CONCENTRATED, CAP, z, snr_min) are still hand-set; L2d (learned global constants) was a no-go (§5), so they remain open.

## 4. Open problems in general (linear, constant-coefficient, autonomous 1+1 prototype)

1. **High-κ loss at 400 points and 5 % noise** (beam 400 5 % s0/s2, TPD 400): the GP smooths away fast-decaying modes. Planned general fix: factor-kernel re-interpolation (EPGP with the candidate factors' kernels, `interp/epgp.py`) before the final decision. H0 (a deterministic raw-residual scan) was a no-go (§5).
2. **Speed:** scattered 400-point cases take 35–60 min each (two_pairs 400 ≈ 49 min, damped_beam 400 ≈ 36 min, without T76). Only exact speed-ups are allowed. Candidates: profile `refine_raw` on the cached 400-point data; reuse SVDs across alternatives with the same basis; the LB exact memo (a GO from the learned layers, §5).
3. **Weight calibration:** cover90 is 0.50–1.00 per cell (run 6); propagate factor uncertainty into weights (T55 does part of it) and then calibrate offline.
4. **Grids vs scattered on one path:** a GP on grids (Kronecker) so both share one interpolation path. Not started.
5. **Non-periodic cells** (S-DOMAIN): the 2-D pencil fails; `domain/kernelfit.py` VarPro is the data-level fit. The quadtree output is optional (grouping is by factors only).
6. **Data-equivalent ties** (damped_beam 400 s0): the right output is a tie label with both laws, not a pick. Check that the report shows both when the gap is under `LOG_BF_BARE`.
7. **The edge suite** (repeated roots, shared κ = 0, small high-order terms) has not been run on the current code.
8. **Bugs reported by the learned-layers runs (not yet investigated on main):**
   - false-confident on 9/80 G test cases with every layer off; the case list is in their corpus rows `ll_G.jsonl`;
   - a `ZeroDivisionError` in `refine_factors`;
   - an `IndexError` in `bayes_split.raw_evidence`;
   - an `IndexError` in `test_aggregate_cluster` (6 known errors);
   - timeouts on corpus S (26/50 LB S runs).

   Reproduce each one from their rows, fix it generally, and add a test. The false-confident cases are the highest value, since V1 exists to catch exactly these.
9. **Out of scope, parked:** non-monic symbols (BBM-type, LIMITS.md), nonlinear, variable coefficients, fractional, higher dimensions.

## 5. ML layers (branch `learned-layers` in `D:\Larned layers`)

Verdicts (from the learned-layers session, 2026-10-30):
- **GO:** V1 (learned failure detector; it recognises when the pipeline's answer is likely wrong) and the LB exact memo (an exact speed-up).
- **NO-GO:** L2d (global constants), L2c (interval calibration), L2b (calibrated P(top)), H0 (high-κ scan), LB learned skip, C (the controller is safe, but its ceiling on G is 1/13; the bottleneck is diagnosis. Redesign it with V1 as the trigger).
- C0 on corpus G: 16 valid pairs, no answer changed (safe, no gain). Two cases gave no answer: one hit the 6 h limit, one crashed on the SVD bug (fixed in 435b048).

The detailed handoff of that session (reports, data paths, sync state, worktrees) is in **`D:\Larned layers\PDEFactorML\sessions\LEARNED\HANDOFF.md`** (requested 2026-10-30; check that it exists). What was known when this file was written is below.

**Key numbers, from that session's handoff (feasibility verdicts on main@66a5064; final tuning is redone on the final pipeline):**
- **V1:** leave-one-family-out AUROC 0.900, against 0.681 for V0 (+0.219, CI [+0.078, +0.289]). It is not shippable yet: the conformal false-alarm gate (α = 0.05) needs about 100 clean 5 %-noise grid rows. It cannot flag runs that crash or time out (48/140 on corpus I), because its features come from the pipeline's output. Report: `sessions/LEARNED/V1/REPORT.md` on branch `claude/ll-validator-1b737b` (045f466).
- **LB exact memo:** 0 runs harmed and 0 coefficient differences; per-run time ratio 0.875 [0.817, 0.930]. It is proposed as on by default; **the user decides at the merge**. Report: `sessions/LEARNED/LB/REPORT.md` on branch `claude/ll-budget-287936` (6fda114).
- **L2d:** every leave-one-family-out fold picks today's constants. **L2c:** off coverage is already 0.895 at nominal 0.90. **L2b:** raw P(top) ≥ 0.999 on 96 % of rows, so there is nothing to calibrate. **H0:** never changes an answer. **C:** the oracle ceiling is 1/13 of off-failures. Report on branch `claude/ll-controller-577bc7` (6d86b25).
- **With every layer off, the pipeline is false-confident on 9/80 cases of the G test corpus.** This is main's problem, see §4.

**Sync state:** the merge of main `125b1f2` (which includes e1fb9ae and 435b048) is done on branch **`ll-sync`**, commit **da223f4**, worktree `D:\Larned layers\.claude\worktrees\ll-sync`. It is not yet on learned-layers. Still to do there:
1. Regenerate the off golden file (`tests/data/make_learned_off_golden.py`).
2. Run the full suite, then fast-forward learned-layers.
3. Merge V1 and the LB memo (**needs the user's OK**).
4. Re-gate V1 and the LB memo.
5. Rerun the 25 runs that crashed on the SVD bug.
Since `cc8a260` changes only docs and data, ll-sync has all of main's code changes.

**ML data:** shared folder `D:\Larned layers\PDEFactorML\analysis\exp\out\`, with its index in `DATA_INDEX.md` / `DATA_INDEX.json`. It holds corpora G, S, N, named and I (`ll_*.jsonl`) and each session's complete output in `out/sessions/{LB,L2d,V1,C}/`. Golden files are in `tests/data/learned_off_golden.json`; models are on the session branches.

**Worktrees:** keep `ll-sync` and the four final branches. Eight duplicate worktrees at 3071bde and `ll-speedsync` can be deleted (list in their handoff §5); ask the user before deleting.

Older notes, kept for reference: the learned-layers branch was based on main at 66a5064. On 2026-10-30 it started syncing to main HEAD (including e1fb9ae and 435b048). Afterwards: regenerate every "all layers off" golden file (off must equal main bit for bit), re-gate only the GO layers (V1, LB exact memo), and rerun the 25 runs that crashed on the SVD bug (C0 on G: 1; LB: 12; corpus I: 11; L2d: 1). The checklist is in `analysis/ML_INTEGRATION.md`. Nothing is merged into main; the user decides that. Do not merge or push the learned-layers branches.

**Where the ML data are:** `D:\Larned layers\PDEFactorML\analysis\exp\out\` (layer runs: `ll_C_*.jsonl`, corpora G and I, banned lists, tables) and the per-layer worktrees under `D:\Larned layers\.claude\worktrees\` (`ll-budget-*`, `ll-constants-*`, `ll-controller-*`, `ll-validator-*`, `ll-sync`, `ll-speedsync`). Plan: `sessions/LEARNED/PLAN.md`; speed study: `sessions/LEARNED/SPEEDUP.md`; sync record: `sessions/LEARNED/SYNC.md`. Main's own ML plan: `analysis/PHASE4_ML_PLAN.md`.

**What main must keep for the layers:** `test_ml_contract.py` green; theory rows on the layers' side stay prefixed `LL-T<n>`; main's next number is **T77**.

## 6. Where main's data are

- Benchmark outputs: `D:\PDEFactorML\benchmarks\out\` (logs, current jsonl, `micro/<suite>_<tag>.jsonl`).
- Archive with index: `D:\PDEFactorML\benchmarks\data\` and `INDEX.md` (runs 2–7, e13 v1–v3, micro suites including the T76 `pb1` partials, core-only `runs.jsonl`, E-experiment tables).
- GP cache for scattered inputs: `D:\PDEFactorML\analysis\exp\cache\<case>_<n>_<noise>_<seed>.npz`.
- Experiments: `analysis/exp/*.py`; analysis docs: `analysis/*.md` (PARAMETERS, LIMITS, GROUPING, DOMAIN, THEORY_TO_ALGO, ML_INTEGRATION, PHASE4_ML_PLAN).
- Plan: `C:\Users\<user>\.claude-secondo\plans\to-plan-use-the-groovy-chipmunk.md` (v2.0–v2.14; add a v2.15 entry for the next step).
- Diagnostic scripts from this session (not in the repo): `C:\Users\<user>\AppData\Local\Temp\claude\D--\76162dc4-fe9c-4d7e-acbb-fea1cb8473b8\scratchpad\` (cubic_diag, dbeam_diag*, dbeam_chi2, check_perbin, patch_*).

## 7. Work stopped for this handoff

- Main: the T76 micro-suite runs (heldout pb1 stopped at 12/14, intervals pb1 at 1/14, conjugate pb1 not started). No other main process is running. Partial results are archived.
- Learned layers: all layer runs stopped (their pool is empty); the session was asked to finish or abort its sync cleanly, write its HANDOFF.md, and stay idle.

## 8. Recommended next steps, in order

1. Read `D:\Larned layers\PDEFactorML\sessions\LEARNED\HANDOFF.md` and confirm the sync state of `learned-layers`.
2. Run the `edge` suite on the current code (4 workers) for a baseline. Then build a micro suite (≤ 15 inputs) from the 9 false-confident G cases and the crash cases (§4.8), and fix those first.
3. T76 repair (empty bins pooled into one scale) → `heldout` + `conjugate` micro runs → adopt only with no regression (check `wave_lowk`, damped_beam 400, time).
4. two_pairs: growth to the needed class driven by V0.1; conjugate matching for n_pairs ≥ 2.
5. Exact speed-ups on the scattered path (profile first; consider the LB exact memo).
6. EPGP factor-kernel re-interpolation for the high-κ loss (beam/TPD 400 5 %).
7. Rerun E13 on current code and classify the misses; add independent fields per seed.
8. Then a full benchmark rerun against run 6, an update of `e2e_summary.md`, and ask the user before any push.
