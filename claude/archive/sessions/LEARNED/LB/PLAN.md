# S-LEARNED-LB — budget/speed layer: PLAN

Session S-LEARNED-LB, 2026-10-29, worktree `ll-budget-287936` (branch from `learned-layers` 3071bde).
It implements `sessions/LEARNED/PLAN.md` §3.5 (flag `budget`) under §1, §2.4 and §9 (rule 8). Research: `RESEARCH.md` § S-LEARNED-LB. Status: planning; nothing is built before approval.

---

## 0. What the data says already (corpus S, off arm, 30 finished runs, 11 crashes, 11 timeouts)

Seconds summed over the 30 finished runs, from the `steps` log (`changed` = the step altered the note or the factor count):

| step | share of time | runs where changed | optional? |
|---|---|---|---|
| decide | 0.265 | 28/30 | no (structure choice; note always written) |
| alternatives | 0.261 | 17/30 | yes |
| recurse | 0.175 | 1/30 | yes |
| core | 0.132 | 0/30 | no |
| refine | 0.048 | 30/30 | no |
| grow | 0.042 | 2/30 | yes |
| complex | 0.041 | 0/30 | yes |
| split_layer | 0.035 | 30/30 | no |
| split_branches, kappa_support, raw_subset, bootstrap | < 0.002 each | — | too cheap to be worth a risk |

Consequences:
1. On finished runs the skippable time is at most about 0.52 of the total (alternatives + recurse + grow + complex). Alternatives change the answer often (17/30), so the realistic saving from skips alone is closer to 0.2–0.3. The §3.5 aim of a 25 % lower median may not be reached by skips alone; it is stated as an aim, and the gate primary is the one in the brief: lower median runtime with a paired CI excluding 0.
2. A third of S runs (F3/F4/F5 at 2000 pts, F5 at 400) time out at 1200 s and leave **no step log**. Where their time goes is unknown. A profiling pass (P0) comes first.
3. G and N rows do not exist yet in the shared out folder. LB depends on corpus G for most of its training and calibration rows.

## 1. Goal and done criterion

Make `run_loop` faster without changing its answers.
- **Done:** `Learned(budget=True)` passes the gate of §7 on the test split and every LOFO fold, or it stays off with the code, the tests and the measured reason in `REPORT.md`.
- "Harm" is defined as in CALM: disagreement with the off run of the same draw, not error against the truth. A run is **harmed** if its label or its final factor set (the factor strings) differs from off.

## 2. Components

### 2.1 LB-skip: per-step skip classifiers under risk control (the core)
- **Steps guarded:** `grow` (the whole growth loop), `recurse`, `complex`, `alternatives`. A step is guarded only if its mean share of runtime on the fit split is ≥ 0.02. This is a scale-free inclusion rule; it is re-evaluated on G. Steps that always change the output by design (`refine`, `bootstrap`, `split_layer`) are never skipped: skipping them changes intervals, which this layer must not do.
- **Label.** The off run logs `changed` for every step. If `changed = False`, the step left the note and the factor list exactly as they were, so skipping it leaves the run bit-identical (claim C1, tested in §4). If `changed = True`, the final answer may or may not differ. LB uses `changed` as the loss label, which is **conservative**: it over-counts harm. An optional refinement (§5, R2) reruns only the `changed = True` events with the step forced off, to get the true harm bit and allow more skips.
- **Why the off logs give the exact loss of the on arm (claim C2).** Steps run in a fixed order. If every earlier skipped step had `changed = False`, the state at the next step equals the off state, so its features equal the logged ones. The first skipped step with `changed = True` already makes the run count as harmed. So the per-run loss L_i(λ) = 1[some step skipped at λ has changed = True] is computed exactly from off logs, with no on-arm runs. This is what makes calibration cheap.
- **Features** (computed at the guard, before the step; all dimensionless per rule 8): P(top), structure entropy, P(k) of the top k, number of factors, max order in τ, max order in ξ, V0.1 omnibus log p (`lp`), evidence gap when available, log(σ / std u), log n_obs, log sample count, grid-or-scattered flag, real-or-complex flag, the `changed` bits of earlier steps, and step-specific ones (number of grow options; number of pooled structures with P ≥ 0.01; for `alternatives`, the gaps of the next structures). No elapsed seconds (machine-dependent).
- **Models compared** (one per step, same features):
  1. **constant** per step (simplest baseline): skip the step always or never, with the per-step choice made by risk control on the calibrate split;
  2. L2 logistic regression;
  3. `HistGradientBoostingClassifier` (default settings, small `max_iter`; no tuning on test).
  The model that passes risk control with the largest calibrate-split saving is chosen on calibrate, then gated once on test.
- **Skip rule.** Skip step s when p̂_s(changed) ≤ λ. A single λ is shared across steps (one scalar keeps L_i monotone in λ and needs no multiple-testing split). λ is chosen by conformal risk control at α = 0.02 (`validator._risk_threshold`, reused), which gives E[L] ≤ α for exchangeable in-prior runs. LTT (P(R ≤ α) ≥ 1 − δ, δ = 0.1) is computed as well and reported; it becomes the rule if the calibrate split has ≥ 114 usable runs.
- **Guarantee scope.** The bound holds in-prior (sim-v2, the calibrate split's distribution). Out of family it is checked empirically by LOFO, and on the named cases. The note says which steps were skipped, so a reader can rerun with the layer off.

### 2.2 LB-cache: exact memoisation (deterministic companion, same flag)
- Inside one `run_loop` call, calls that are pure functions of their arguments and are repeated with equal arguments are computed once. Seen in the code already: `heldout_score(u_mean, …, bounds, …)` for the current class is recomputed on every growth iteration; `extract_modes_ic(u_ref, …)` is called with the same arguments before `raw_subset` and before `refine`; `_run` may be called again for a class already run. P0 measures which of these matter; only those are cached.
- It changes no number, so it carries no risk budget. It is bit-identical by test. It is behind `budget=True` here; if it passes, the REPORT proposes it to S-LEARNED as a default-on change (that is the parent's decision, since off must stay bit-identical to B0 including runtime-independent outputs, which it would).

### 2.3 LB-timeout: early "will hit the cap" predictor (corpus-level, built only if it passes)
- **Where:** in the corpus harness only (`analysis/exp/ll_budget_corpus.py`), never in `run_loop`, never as a label. A predicted timeout ends the run early and records `TIMEOUT` (`budget-predicted`), exactly what the off arm would record.
- **Target:** binary "runtime ≥ cap" from features available after `core` (and after `grow`). A binary target at the cap avoids the censoring problem of runtime regression (Hutter et al. 2014).
- **Loss:** aborting a run that would have finished. Risk control at α = 0.02 on the calibrate split, same machinery.
- **Gain:** CPU-hours per corpus (the simulation budget the user cares about), reported separately from the per-run median, which it would distort.
- **Cheaper GP settings:** not built. GP S, bootstrap B and W_DRAWS stay fixed (§3.5 of the LEARNED plan); a change of Monte Carlo size changes intervals, which no "provably not needed" criterion in hand covers. Listed in the REPORT as an open option only.

## 3. API and hook

`src/pdefactor/learned/budget.py`:
```python
STEPS = ("grow", "recurse", "complex", "alternatives")

@dataclass
class BudgetModel:                     # fitted offline, stored in learned/models/lb_v1.joblib
    steps: tuple
    kind: str                          # "constant" | "logistic" | "hgb"
    lam: float                         # risk-control threshold
    alpha: float = 0.02
    meta: dict                         # corpus hash, PRIOR_TAG, constants version, n_cal
    def p_change(self, step, feats) -> float: ...
    def skip(self, step, feats) -> bool: ...    # p_change <= lam; False for unknown steps

def features(step, state) -> dict      # dimensionless, NaN when undefined
def load(path=None) -> BudgetModel | None
def fit(rows, kind, alpha, cal_rows) -> BudgetModel
def replay(row, model) -> dict          # offline on-arm from an off row: harmed?, seconds saved
class Memo: ...                          # per-run_loop exact cache (LB-cache)
```
Hook in `loop.py`, one guard per guarded step, only when `ll.budget` and `_depth == 0`:
```python
if ll.budget and _depth == 0 and lb.skip("recurse", lb.features("recurse", st)):
    note += "recursion skipped by LB (budget layer, risk 0.02). "
else:
    <today's code, unchanged>
```
`_depth == 0` keeps child runs identical (recursion children never see the layer). The `steps` log still records the step, with 0 s and `changed = False`, plus a `skipped` marker. With `budget=False` no line of today's path runs differently.

## 4. Tests written first (`tests/test_learned_budget.py`)
1. **Off unchanged:** `test_learned_off.py` and the golden file stay green (no edit to them).
2. **Never-skip model is identical to off:** `budget=True` with a model whose λ < 0 gives the same label, factors, intervals and evidence as off on the golden draws (also covers LB-cache bit-identity).
3. **Skip is noted:** an always-skip model writes each skipped step into `LoopResult.note` and into `steps`.
4. **C1, exactness:** on draws where off logs `changed = False` for step s, forcing s off gives bit-identical output (F1 grid, heat scattered, a named case).
5. **C2, replay:** `replay(off_row, model)` equals the real on run (harm bit; saved seconds within timing noise) on 3 draws.
6. **Risk control:** synthetic scores with known loss: CRC returns the largest λ with (n R̂ + 1)/(n + 1) ≤ α; monotonicity of L in λ; LTT p-value rule; cross-check against MAPIE's controller on the same synthetic data (test skipped if MAPIE is absent).
7. **Features:** dimensionless (invariant when u, σ are scaled by the same factor and t, x are rescaled with the coefficients), NaN-safe.
8. **Children untouched:** a recursion child run never consults the model.

## 5. Data, corpora and compute

| id | what | runs | compute (slot pool, background) |
|---|---|---|---|
| P0 | profile: cProfile + a streamed step log (monkeypatched `_Steps.mark` in my script, no loop.py change) on 6 S draws that time out (F3/F4/F5 × 2000 pts, F5 400) with cap 2400 s, plus 4 finished F3/F4 runs | 10 | ≈ 2–3 h on 4 slots |
| R0 | fit/cal data: off rows of G (fit 100–119, cal 120–127) and S (fit 200–206, cal 207–208) from the shared folder; read-only | 0 new | 0 (waits for S-LEARNED's G) |
| R1 | if G is late or lacks rows: my own off runs of G-fit/cal in my worktree's `analysis/exp/out/ll_lb_G.jsonl` | ≤ 280 | ≈ 3 h on 6 slots |
| R2 | optional, only if the conservative label leaves most time unskippable: rerun the `changed = True` events of fit/cal with that step forced off, to get the true harm bit | ≈ number of such events (S: ~20 alternatives events per 30 runs) | ≈ 2 h |
| E | evaluation: offline replay on test (G 128–135, S 209–211), every LOFO fold, N; then **one real on-arm pass** of the test split + N + named cases with the final model, to check the replay and measure real runtime | 110 + N + named | ≈ 3 h |

Training and calibration take seconds. LOFO costs no extra runs because of replay (C2): each fold refits the model and λ on four families and replays the fifth.

Calibration-size check: the calibrate split has about 80 (G) + 20 (S) = 100 runs, minus crashes and timeouts. CRC at α = 0.02 needs n ≥ 49 and tolerates about one harmed calibrate run at n = 100. LTT needs n ≥ 114, so LTT is reported but CRC is the rule unless calibrate grows. If calibrate is too small for any skip after the conservative label, R2 is run before concluding.

## 6. Theory citations
- Skip under risk control: TL-4 (heuristic, statistics: conformal risk control; proposed in LEARNED PLAN §8). Skipping removes candidates and never changes a score.
- C1/C2 (exactness of a no-change skip, exact replay): no theory row; a determinism invariant of the code, checked by tests 4–5.
- Features and models: no theory: empirical.
- Timeout predictor: no theory: empirical (Hutter et al. 2014 for the method).
- LB-cache: no theory needed; pure-function memoisation, bit-identical by test 2.

## 7. Gate (§2.4, unchanged, applied to the test split and every LOFO fold)
- **Primary:** median runtime lower than off, paired bootstrap 95 % CI of the difference excluding 0 (`ll_gate.py --target runtime`), on the real on-arm pass; the replay estimate is reported next to it. p90 reported. Timeouts are counted at the cap in both arms (LB-skip and LB-cache only; LB-timeout is reported as CPU-hours separately).
- **Required:**
  - harmed runs ≤ 0.02 on test, with the CRC guarantee on calibrate stated, and per LOFO fold;
  - right-set ≥ off − 0.02 and false-confident ≤ off (paired);
  - coverage not worse by more than 0.02 (expected identical: no interval step is skipped);
  - nulls clean (N: never FIT-COMPATIBLE; no extra factor on single-factor draws);
  - named cases not worse in any cell (`ll_named.py`), in particular the beam (the `complex` step's reason to exist);
  - fresh-context review subagent (`experiment-audit` / `result-to-claim`) passes the claim.
- If replay and real runs disagree on any harm bit, C2 is false: the layer stays off until the cause is found.

## 8. Order of work after approval
1. Own venv (common brief recipe); tests of §4 written and failing.
2. P0 profiling in the background; meanwhile `budget.py` skeleton, guards, LB-cache.
3. R0 (or R1) rows → fit three model kinds → CRC/LTT → replay on cal.
4. LB-cache measured on P0 draws; LB-timeout built only if P0 shows it is feasible.
5. Gate E; `REPORT.md`; full `pytest -q`; commit on my branch.

## 9. Questions for the parent (defaults in brackets)
1. When will G off rows (fit + cal) land in the shared out folder? [Default: start P0 now; run R1 myself if G is not there when P0 ends.]
2. LB-cache is exact and could be default-on later; it is behind `budget=True` here. [Default: keep it behind the flag; propose in REPORT.]
3. Harm = disagreement with off (label or factor strings), not error vs truth. [Default: yes, as in CALM.]

## 10. Erratum to §0 (added before approval; §0 is kept as written)
`ll_S.jsonl` holds both the off and the `highk` arms; §0 pooled them. Off arm only: 22 draws so far (10 FIT-COMPATIBLE, 3 UNDECIDED, 2 ID-KER, 5 TIMEOUT, 2 CRASH); 15 have a step log. Shares of finished-run time, with runs where `changed`: recurse 0.287 (1/15), decide 0.262 (14/15), alternatives 0.203 (9/15), core 0.131 (0/15), grow 0.035 (1/15), split_layer 0.032, refine 0.031, complex 0.018 (0/15), the rest < 0.002. So recursion is the largest and safest skip candidate; `complex` falls below the 0.02 inclusion rule on S and is re-checked on G. The conclusions of §0 (skips alone are bounded at about half of finished-run time; timeouts are unprofiled; G is needed) are unchanged.
