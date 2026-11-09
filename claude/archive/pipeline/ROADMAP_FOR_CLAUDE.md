# ROADMAP_FOR_CLAUDE — where everything is, if you want to extend the algorithm or the ML layers

Pointer file for a Claude session. It explains nothing; it says **where to look**. Written 2026-11-01 on main `5c25e27`.
Paths: `PB` = `D:\ProblemaBase` (analytic theory, **read-only**); `PDF` = `D:\PDEFactorML` (code, main); `LL` = `D:\Larned layers\PDEFactorML` (ML layers, separate copy, branch `learned-layers`).

## 0. Rules before touching anything

- Read first: `PDF/CLAUDE.md` (rules 1–8; rule 8 = every change general, tested on held-out families), `PDF/HANDOFF.md` §00 (latest state), `PDF/analysis/THEORY_TO_ALGO.md` (T1–T103; next free row **T104**, add-only).
- Use only DIMOSTRATO rows (or CON-FONTE with a verified source) of `PB/claims/LEDGER.md` as foundations. Query the theory graph: `cd D:/ProblemaBase && graphify query "<topic>"`; the code graph is `PDF/graphify-out/graph.html` (+ `GRAPH_REPORT.md`).
- Do not write in `PB` (only its `graphify-out`). Leave `PDF/EXPLAINED/` alone (the user edits it). Never read `D:\Larned layers\<private notes file>`.
- Output contract: labels `FIT-COMPATIBLE / MISFIT / ID-KER(class) / UNDECIDED`, never "law identified". An honest UNDECIDED beats a wrong FIT-COMPATIBLE.
- Workflow used so far: one switch per change (`PDEFACTOR_*` env), A/B on micro-suites of ≤ 15 inputs (`PDF/benchmarks/micro.py <suite> --tag X --ref Y`), full suite (`.venv/Scripts/python.exe -m pytest -q`, ≈ 13 min), `test_ml_contract.py` green, CRLF-safe patching (Python, no `sed -i`), commits only via the `D:/` repo, no push without asking.

## 1. Where the pipeline is today (scope of what exists)

Scope: **linear, constant-coefficient, autonomous, scalar 1+1 PDE**, symbols monic in τ, simply connected rectangles (CLAUDE.md rule 6; `PDF/HANDOFF.md` §00 and §4).
Code map (`PDF/src/pdefactor/`): `core/` (analytic core: `variety.py`, `structfit.py`, `components.py`, `spectral.py`, `analyze.py`), `loop.py` (outer Bayesian loop), `refine_raw.py` (raw-data evidence, BRANCH_ARD), `bayes_split.py`, `validate.py` (V0.1, T96), `raw_gof.py` (T88), `interp/` (GP, EPGP, SKI), `domain/` (quadtree, cell fits), `aggregate.py`, `cluster.py`, `symbols.py`, `simulator.py` / `synthetic.py` (random PDE families F1–F5, named cases), `baselines/` (SINDy variants, DMD).
Results to compare against: `PDF/benchmarks/out/p8_final_v5.md` (30 inputs, pipeline 30/30, 0 false-confident, vs SINDy/DMD), `PDF/benchmarks/out/e2e_summary.md`, E13 (`PDF/analysis/exp/e13_random_pdes.py`, `e13_summary.py`), `PDF/sessions/S-BASELINES-BENCH/REPORT.md`.

## 2. Extending the algorithm: nonlinearity, variable coefficients, time dependence, systems, higher dimension, non-local

### 2.1 What the theory already says (read these in this order)
1. **Ladder and targets:** `PB/PROBLEM.md` — G★′ (linear), **G★′-NL** (nonlinear, Phase 4), **G★″** with the ladder **L6 systems → L7 variable coefficients V(x) → L8 non-autonomous V(t,x) → L9 non-local (symbols, memory, delay, fractional) → L10 filtered universal dictionary**.
2. **Final reports:** `PB/REPORT_FINALE.md` (§4 nonlinear, §6 open problems, §7 file map, §8 honest limits), `PB/CHIUSURA_F10.md` (§2 main outcomes of Phases 8–11, §3 what stays open), `PB/RIPRESA.md`, `PB/BOARD.md`.
3. **Routes chosen and parked:** `PB/ROUTES.md` (Gate 6 table: RT-SYS, RT-IDV, RT-ODE-GAL, RT-NA, RT-ENC, RT-DICT, RT-CONV; parked ones: Weyl for PDE, Koopman, homogenisation…), `PB/GATE6.md`, `PB/GATE4A.md`, `PB/research/SYNTHESIS-2.md` (§3 encoder table, §4 routes, §5 G★″).
4. **Open-problem registry:** `PB/PROBLEMI_APERTI.md` (class B = no known route; class C = blocked on offline sources), triaged in `PB/work/CHECK-F10/TRIAGE_APERTI.md`, audit in `work/CHECK-F10/AUDIT_TRIAGE.md`.
5. **Bibliography:** `PB/BIBLIOGRAFIA.md` / `.bib` (112 sources by topic, verification status, claim → source table). Notation: `PB/NOTAZIONE.md`.

### 2.2 Extension by direction: theory, proofs, open problems

| direction | what is proven (LEDGER prefix → proof package) | where to read | open problems |
|---|---|---|---|
| **Nonlinear** (Burgers, KdV–Burgers, Fisher–KPP; dictionary-relative identification) | `S4T-*` (interaction term E_int in the sense A9, jet in t, closed form before the shock) → `PB/work/S4-TERM/PROOF_PACKAGE.md`; `S4ID-*` (identification relative to a dictionary, Burgers N-shock, KdV N-soliton ideals) → `PB/work/S4-ID/`; `INT-*`, `ALG-*`, `F4L*` (Cole–Hopf, IST, Hirota lemmas) → `PB/work/S4-INTEG/`, `PB/work/OP-F5{A,B,C,D}/`, `PB/work/KIEFFER/` | `PB/REPORT_FINALE.md` §4; `PB/research/F4-{ALG,LIN,INT,LIFT,HOR}/`; `PB/FASE4_SCOUTING.md` | INT-Q1 (KdV autonomous ODE in x), [GT-u₀], [GT-u_m], [F4⁻], OPA-Q1/[L-loc] (several shocks), OPA-Q2; `PB/PROBLEMI_APERTI.md` §1–§3 |
| **Nonlinear, dictionary / non-polynomial** (sine-Gordon, e^u) | `DICT-*` (47 rows): U1–U4, N1, misfit certificates MF1–MF3, rules R1–R6, R-STOP, I-LIM → `PB/work/S8-DICT/PROOF_PACKAGE.md`, `KILL_ARGUMENT_N1.md`; research `PB/research/F6-DICT/` | `PB/research/SYNTHESIS-2.md`, `PB/ROUTES.md` (NS-EXPALG fused into RT-DICT) | DICT-Q3(c) (division with variable rank), U3(a), U5 (parked) |
| **Variable coefficients V(x)** (L7) | `VAR-*` (47 rows): VAR-T1/T2 structured identification, boundary VAR-N1 (empty intrinsic vs structured), VAR-T6 decomposition, VAR-P8 (Wei–Norman finite ⟺ deg V ≤ 2) → `PB/work/S8-VAR/PROOF_PACKAGE.md`; research `PB/research/F6-VAR/` | `PB/PROBLEM.md` G★″, `PB/research/F6-VAR/VERDETTO.md` | VAR-Q18 (multiplications), VAR-P12(d), VAR-C3Q2-open / VAR-Q13 (non-monic), VAR-Q17(b), Weyl algebra for PDE (parked) |
| **Non-autonomous V(t,x)** (L8, time dependence) | VAR-P9/T10, `ENC-P0(b)`, `(b)^cl`: no t-independent encoder for generic V(t,x); quadratic cases via metaplectic/gauge transforms; `DM-φ` (data up to global time phase) → `PB/work/S8-VAR/`, `PB/work/S8-ENC/PROOF_PACKAGE.md`, `PB/work/S8-CONV/` (CONV-T7 iterative contract) | `PB/research/F6-ENC/`, `PB/research/F6-CONV/` | ENC-Q4 (reading DM3 needs the class W(t) defined) |
| **Analytic encoders** (Volterra/GLM, Darboux–Crum) | `ENC-*` (37 rows), `ENC-T2`, `ENC-N1′` → `PB/work/S8-ENC/` (also `LEDGER_ROWS.rev2.md`) | `PB/research/SYNTHESIS-2.md` §3 | joint identification of (q, u) has no identification gain (ENC-N1′) |
| **Systems** (Dirac, Maxwell, Lamé) (L6) | `SYS-*` (22 rows): SYS-T1/N1/T0/S1, gauge G-T2, SYS-N3, SYS-E (E_int for Dirac 1+1) → `PB/work/S8-SYS/PROOF_PACKAGE.md`; research `PB/research/F6-SYS/` | `PB/ROUTES.md` RT-SYS | SYS-DIRAC-POL (complex t, m) |
| **Higher dimension 2+1 / 3+1** | CONV-D1: ambiguity is infinite unless the factors are comaximal (`PDF/analysis/THEORY_TO_ALGO.md` T20); `C12-*` (split and decomposition) → `PB/work/C1C2/`, `PB/work/C3/` | `PDF/analysis/LIMITS.md`, `PDF/analysis/PHASE4_ML_PLAN.md` §4 L5 (iv) | C12-Q1, C12-Q2 = OPF-Q2 (sum closure N ≥ 3), P2-Q1-NL (non-Lipschitz domains), P2-Q1-COD |
| **Convergence / noise / boundary** | `CONV-*` (26 rows): CONV-T1…T7, T6 locality trichotomy → `PB/work/S8-CONV/PROOF_PACKAGE.md`; Phase 10 collection `PB/work/S10-COL/PROOF_PACKAGE.md`, `S10-INT`, `S10-OPEN-{A,B,C}` | `PB/research/F6-CONV/` | OPR2-Q3 (repeated plinth), OPR2-Q2′ (wedges), OPF5C-Q1 (δ_N(K) for general N) |
| **Non-monic symbols** (BBM type) | Identifiability Ann(u) = (P) proven only for P monic in τ (II-C1 = C3-T1(d)); candidate: fit c(ξ)τ − a(ξ) | `PDF/analysis/LIMITS.md` ("Non-monic symbols") | VAR-C3Q2-open |
| **Non-local / fractional / memory** (L9) | `HOR` research only (no LEDGER prefix) → `PB/research/F6-HOR/VERDETTO.md`, `PB/research/F4-HOR/` | `PB/ROUTES.md` (L9 row) | CONV-T5: m(δ) → ∞ ⇒ pipeline can only say UNDECIDED "no finite degree" |

Mathematics-to-code correspondence for the **current** scope is `PDF/analysis/THEORY_TO_ALGO.md`: T8, T20 (1+d), T13/T30/T40/T41 (identifiability), T55 (Monte Carlo weights), T69 (confluent relabel), T88–T103 (latest). Read the row for the algorithm you are about to change.

### 2.3 What the pipeline already does when the law is outside its scope
- Detectors for each deviation: `PDF/analysis/PHASE4_ML_PLAN.md` §8 (table "Failure modes per pipeline phase": nonlinear PDE → V0.8 amplitude/κ-coupling, variable coefficients → V0.7/V0.6 λ(κ) drift across cells and t-windows, fractional → V0.6, two laws → V0.7, …). Fixer there is "out of scope: MISFIT + reason" or "subdomain report". Code: `PDF/src/pdefactor/validate.py` (V0.1 omnibus; V0.2–V0.8 planned in the table), `domain/` (cells), `aggregate.py` / `cluster.py` (two regimes).
- **Entry points for an extension** (existing code to build on): per-cell fits and frozen-coefficient cells (`domain/fit.py`, `domain/quadtree.py`, `aggregate.py`, `cluster.py`; `PDF/sessions/S-DOMAIN/`, `S-AGG-CLUSTER/`, `analysis/DOMAIN.md`); dictionary baselines (`baselines/sindy.py`, `common.py`); simulator hooks for out-of-class data: `PDF/analysis/PHASE4_ML_PLAN.md` §P0.3 and (in LL) `analysis/exp/ll_inject.py` (injects `nonlinear`, `varcoef`, `fractional`, `two_laws`, `coloured`, `heteroscedastic`, `aliasing`).
- Minimal route suggested by the plan documents: (1) detect and refuse (V0.7/V0.8, already specified), (2) frozen-coefficient cells for slowly varying V(x) (S-DOMAIN, S-AGG-CLUSTER), (3) only then structured identification VAR-T1 with a declared coefficient class; nonlinear via a declared dictionary (S4ID/DICT), never "free-form".

## 3. Open problems in the algorithm itself (constant-coefficient 1+1, not extensions)

State at 2026-11-01 (`PDF/HANDOFF.md` §00 "Open"; §3–§4 for older detail):
1. **two_pairs** keeps the true factors but is UNDECIDED (T69 confluent relabel). Started and STOPPED unfinished (2026-11-01, at the user's request): branch `t69-confl` (worktree `C:\Users\<user>\pdef-wt\t69-confl`), nothing adopted; the outcome may be "UNDECIDED is the correct honest answer".
2. **BRANCH_ARD bare-τ bias:** a factor with no excited branch costs nothing in the score (T99 note). Started and STOPPED unfinished (2026-11-01): branch `bare-tau` (`C:\Users\<user>\pdef-wt\bare-tau`), planned switch `PDEFACTOR_BARE_CHARGE`; nothing adopted, no A/B result.
3. Beam 400 s1 cover90 0.5 (honest 90 % miss); CONJ_HALF complex run still refines badly there (reverted by evidence) — see T103 row and branch `scat-beam`.
4. G11 weights over the δ(P) ambiguity (shared κ = 0 mode); AR(1)/coloured noise not in any suite; benchmark seeds share one field (independent fields per seed is a benchmark change); hand-set constants (LOG_BF_STRONG, P_CONCENTRATED, CAP, z, snr_min) — `PDF/HANDOFF.md` §3; classified list: `PDF/analysis/PHASE4_ML_PLAN.md` Appendix A and `PDF/analysis/PARAMETERS.md`.
5. Not adopted, code kept off (re-open only with new evidence): T83 GROW_PAST, T84/T90 EPGP_REINTERP, T97 FIT_GUARD / ALT_PRE — rows in `THEORY_TO_ALGO.md`, reasons in `HANDOFF.md` §00.
6. Theory-side leftovers that would change the algorithm: `PB/PROBLEMI_APERTI.md` (C12-Q1, OPR2-Q2′, OPR2-Q3, …) and the pipeline-side limits in `PDF/analysis/LIMITS.md`.
7. Work trees with finished or parked branches (do not delete without the user): `C:\Users\<user>\pdef-wt\{t82-f5131,t83-two-pairs,p8-report,t95-f4128,t96-v01-guard,int-t97,int-final,int-boot,scat-beam,t69-confl,bare-tau}`; list and status in `PDF/HANDOFF.md` §00.

## 4. Machine-learning work

### 4.1 Where it is
- Design and critical evaluation: `PDF/analysis/PHASE4_ML_PLAN.md` (layers L0, L1, L2, V, C, L5, L6; build order §6; call-graph §7; failure-mode/detector/fixer table §8; acceptance protocol §9; library catalogue §10; review record §12; Appendix A constants), `PDF/analysis/ML_INTEGRATION.md`, `PDF/sessions/S-PHASE4-ML/{PLAN,RESEARCH}.md`, original pipeline note `PB/NOTE_ML/ml_pipeline_note.tex`.
- Implementation and data (**separate copy**): `LL/` on branch `learned-layers` (synced to main as `ll-sync` = 28ae435, local, not pushed; worktree `D:\Larned layers\.claude\worktrees\ll-sync`).
  - Code: `LL/src/pdefactor/learned/` (`validator.py` V1, `budget.py` / `memo.py` LB, `controller.py` + `remedy.py` + `runconfig.py` C, `calibrate.py` L2, `expseeds.py` / `expsum.py` L0, `highk.py` H0, `ptop.py` L2b, `resid.py`, `features.py`, `apply.py`, `config.py`, `models/`).
  - Experiments: `LL/analysis/exp/ll_*.py` (`ll_corpus.py`, `ll_gate.py`, `ll_v1.py`, `ll_ptop.py`, `ll_C_*.py`, `ll_Cprime.py`, `ll_budget_*.py`, `ll_l2c.py`, `ll_inject.py`, `ll_named.py`, `fastrun.py`), data in `LL/analysis/exp/out/` (index `DATA_INDEX.md` / `.json`; corpora G, S, N, named, I).
  - Session plans/reports: `LL/sessions/LEARNED/{PLAN,SPEEDUP,SYNC,HANDOFF}.md`, `V1/{PLAN,REPORT}.md` + `V1/results/`, `LB/{PLAN,REPORT,fit_results*}.md`, `C/{PLAN,cprime_oracle_p7}.md`.
  - Tests: `LL/tests/test_learned*.py`, `test_runconfig.py`, `test_ml_contract.py`, `test_learned_off.py` (all layers off must equal main bit for bit; golden file `tests/data/learned_off_golden.json`, regenerate with `tests/data/make_learned_off_golden.py`). `test_ml_contract.py` must also stay green on `PDF` main.
- Theory rows of the ML side are prefixed `LL-T<n>` (kept on the layers' side). Main's own rows are `T<n>`.

### 4.2 What was tested, and the verdicts

| layer | what it is | tested on | verdict | evidence |
|---|---|---|---|---|
| **LB exact memo** | exact speed-up (mode-extraction cache) | 165 offline runs, G test paired, nulls, named | **GO, on by default** (0 runs harmed, 0 coefficient differences, time ratio 0.875) — but after main's own speed-ups (bincount, T87) it is bit-identical and no longer faster | `LL/sessions/LEARNED/LB/REPORT.md` |
| **V1** learned failure detector / validator (HGB on pipeline features + residual features) | flags likely-wrong answers; option "downgrade to UNDECIDED" | corpus I (100 rows, 40 timeout/crash), clean 5 % grid rows (95), LOFO F1–F5, LOTO injection types, conformal α = 0.05 | **NO-SHIP**. Feasibility (main@66a5064): LOFO AUROC 0.900 vs V0 0.681. On the final pipeline (P7): detection 0–8 % per family; V1 − B0 detection −0.33 [−0.60, −0.07]; zero detection of the injected `nonlinear`, `varcoef`, `two_laws`; cannot flag crashes/timeouts (its features come from the output) | `LL/sessions/LEARNED/V1/REPORT.md`, `V1/results/v1_gate_resid_p7.md` |
| **C / C′** controller (rule table, remedies, honesty rule, R0 fallback) | re-runs with other settings when diagnosed | G corpus (16 valid pairs), P7 oracle sweep on 12 off-failures (15 single actions each, cap 1200 s) | **not built (user decision 2026-11-01)**. Old: ceiling 1/13. P7 oracle ceiling 8/12 (rescuers: lower_degree 8, varpro 3, wide_alternatives 2, narrow_band 2, skip_grow 2, sigma_reest 2, skip_recurse 1), but with a trigger the ceiling is 0/12 (V1, T96, V0.1, T88 flag none; 3/12 if a timeout counts as a trigger) | `LL/sessions/LEARNED/C/cprime_oracle_p7.md`, `LL/analysis/exp/out/cprime_trigger_p7.md`, `PDF/benchmarks/cprime_trigger.py` |
| **L2d** global constants (BO) | tune LOG_BF_STRONG etc. | LOFO F1–F5 | **NO-GO** (every fold picks today's constants) | `LL/analysis/exp/out/sessions/L2d/` |
| **L2c** interval calibration | recalibrate coverage | G test | **NO-GO** (coverage already 0.895 at nominal 0.90) | idem |
| **L2b** calibrated P(top) | calibrate structure probability | G, S | **NO-GO** (raw P(top) ≥ 0.999 on 96 % of rows; nothing to calibrate) | `V1/REPORT.md` L2b tables |
| **H0** high-κ scan | find missed high-κ energy | G | **NO-GO** (never changes an answer) | session out dirs |
| **LB learned skip** | learned early stop | G | **NO-GO** | `LB/REPORT.md` |
| **L0** learned seeds for the per-bin exponential fit | proposal only | planned | untested beyond sketches; the one place theory leaves to ML (T10 / P2-Q3) | `PDF/analysis/PHASE4_ML_PLAN.md` §4 L0, `PDF/analysis/exp/e12_l0_seeds.py`, `e15_seed_bounds.py` |
| **L5** learned grouping encoder | — | — | rejected/deferred (R1-P9, P2-P4: features must be analytic; CONV-D1 in 2+1) | `PHASE4_ML_PLAN.md` §4 L5 |
| **L6** NPE amortised posterior | cross-check only | — | deferred | §4 L6 |
| pipeline + ML | all layers | P8 | pipeline + ML = pipeline (30/30, 0 false-confident either way) | `PDF/benchmarks/out/p8_final_v5.md` |

### 4.3 Open ML problems and candidate solutions
1. **No signal for the residual failures.** The 12 remaining failures of P7 are false-confident or timeouts that no detector flags. *Candidates:* analytic V0.x battery beyond V0.1/T96 (V0.5 coloured residuals, V0.6 noise-sweep trend of the selected degree, V0.7 λ(κ) drift, V0.8 amplitude/κ-coupling — specified in `PHASE4_ML_PLAN.md` §V, not all implemented); the best remedy found is `lower_degree` (8/12), so a deterministic "also report the lower-degree law as alternative" rule (data-equivalent set, T-rows around T51/T100) may capture the gain without a controller.
2. **V1 cannot see crashes/timeouts** (48/140 on corpus I). *Candidates:* time/crash as an explicit trigger (3/12 rescued by C′ oracle); budget model `LL/.../budget.py` for predicting timeouts; per-stage profiling in `LL/sessions/LEARNED/SPEEDUP.md`.
3. **V1 is prior-relative** (calibrated under the simulator prior) and does not extrapolate to out-of-class laws (0 detection of nonlinear/varcoef/two_laws). *Candidates:* an OOD score on analytic features (OOD in §8 table), conformal with Mondrian groups by family (`PHASE4_ML_PLAN.md` §V and Appendix refs to MAPIE), training only where the theory makes the problem universal (§5 item 3).
4. **Conformal gate data:** needs ~100 clean 5 % grid rows (95 collected in P7); more rows per family would tighten the false-alarm bound [0.195 at n = 17 test].
5. **Hand-set constants remain** (L2d NO-GO): the honest route is decision-theoretic thresholds + monotone recalibration (`PHASE4_ML_PLAN.md` §L2), not BO over ~60 constants.
6. **If ML is ever resumed:** start from `LL/HANDOFF.md`/`sessions/LEARNED/HANDOFF.md`, regenerate the off golden file after every main change, re-gate only V1/LB, rerun the 25 crashed runs (SVD bug, fixed in 435b048). Speed-up recipes for corpora: `LL/sessions/LEARNED/SPEEDUP.md`, `analysis/exp/fastrun.py`.

## 5. Benchmarks and baselines (to measure any extension)
- Final compact benchmark: `PDF/benchmarks/p8_report.py` → `benchmarks/out/p8_final_v5.md` (10 cases × {grid 1 %, grid 5 %, 400 pts 5 %}); pipeline vs weak/ensemble/SBR SINDy, PDE-FIND, BOP-DMD (`src/pdefactor/baselines/`, `sessions/S-BASELINES-BENCH/`).
- Micro-suites: `benchmarks/micro.py` (`heldout`, `conjugate`, `fc`, `edge`, `intervals`, …), score classes in `analysis/exp/e13_summary.py` (right / equivalent / abstain-ok / abstain / false-confident / wrong / CRASH; `chi2_gap` for data-equivalence).
- Random PDEs: `analysis/exp/e13_random_pdes.py` (families F1–F5 from `src/pdefactor/simulator.py`); out-of-class injection: `LL/analysis/exp/ll_inject.py`.
- Test suite: `PDF/tests/` (238 tests); to add a family or a new class of laws, follow `tests/test_t103_split_ci_idker.py` and `tests/test_t100_path_class_ard.py` as templates.
