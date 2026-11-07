# S-LEARNED — handoff (updated 2026-11-01, P7; first written 2026-10-30)

## 0. P7 update (ML re-sync, merges, re-gates; all local on `learned-layers`, nothing pushed)

Pipeline: main eaa8f9c + S-LEARNED. Every result below is on that code (src unchanged from 76d0b55 on).

**Sync and merges** (`learned-layers` fast-forwarded to `ll-sync`; the worktree branch `ll-sync` = `learned-layers`):
- Full suite on ll-sync 0ce0b1f (PYTHONPATH = worktree `src`): **223 passed, 1 skipped, 0 failed** (the old `test_aggregate_cluster` errors are gone on main). c27a81b brings the 3 HANDOFF commits in, so the ff works.
- **V1 merged** (19a481e, from 045f466): 4 add/add conflicts in S-LEARNED files only; loop.py clean. Tests: 118 passed.
- **LB merged** (c12673e, from 6fda114; it also carries C's early controller/runconfig code, opt-in, off): 9 loop.py conflicts, main's code kept in every hunk; LB's knob reads, `_lb_skip` guards and `_fp` step fingerprints added on top. One compat fix: `controller._delta("wide_alternatives")` with main's `ALT_TOP = None`. Tests: off golden + test_learned + ml_contract 43 passed; budget/runconfig/v1/layers/p3/p4/t77 72 passed; controller 15 passed.
- **LB exact memo is on by default** (user decision): `budget.MEMO_DEFAULT`, env `PDEFACTOR_LB_MEMO=0` turns it off. The off golden passes with it on.
- **V1 downgrade option** (76d0b55): `Learned(validator="downgrade")` turns a V1-flagged FIT-COMPATIBLE into UNDECIDED (factors kept; never an upgrade). Off when layers are off; tests added. **Not shipped** (gate below), so no `v1.joblib` exists and the option does nothing until a model passes.

**Corpora** (shared `analysis/exp/out/`, all current pipeline, full settings: B = 16, cap 1200 s):
- `ll_V.jsonl`: corpus **V**, 100 clean 5 % grid rows, F1–F5 × seeds 600–619 (fresh; fit 600–607, cal 608–615, test 616–619); 79 scored, 21 TIMEOUT (F4 11, F5 6, F2 2, F3 2). 24–28 clean cal rows per LOFO fold, so the α = 0.05 gate is evaluable. Fast check first: `ll_V_fast.jsonl` (20 rows, LL_BOOT = 0, cap 300 s; screening only).
- `ll_I_p7.jsonl`: corpus I re-run on this pipeline (140 rows; 100 scored, 37 TIMEOUT, 3 CRASH). The old `ll_I.jsonl` is from 66a5064 and is not mixed in.
- `ll_Gmatch_p7.jsonl`: matched clean control (20 rows, seeds 400–403; 16 scored).

**V1 re-gate** (`V1/results/v1_gate_resid_p7.md`; clean 95, injected 100):
- LOFO AUROC **0.847 [0.720, 0.914]**, vs V0 +0.222 [+0.018, +0.356]; FIT-COMPATIBLE only 0.922, +0.295 [+0.057, +0.412].
- Conformal α = 0.05: the false alarm is within the bound (split 0/17; LOFO 0.00–0.09 per fold, all inside the binomial MC band). But **detection is 0.00–0.08 per fold**, below V0's 0.26–0.47. The HGB score separates on average (AUROC) but not in the far tail that α = 0.05 needs.
- Gate: primary_split, primary_lofo, loto and useful_mid_level all **fail**. **Verdict: NO-SHIP** (no model saved, V1 stays off).
- Downgrade replay (LOFO, held-out rows):
  - clean: 3/95 flagged; false-confident **7 → 7**; right 46 → 45, equivalent 37 → 36 (2 correct answers lost, 0 false answers removed);
  - injected: false-confident 3 → 2, right 26 → 24.
  - So the downgrade, at this operating point, buys almost no safety. Not recommended.

**LB memo re-gate**: off golden identical with the memo on. Paired timing (`ll_lb_memo_timing_p7.jsonl`, G test seeds 128/129 × F1–F5, grid 5 %, arms interleaved, 2 workers): 10/10 pairs give identical label, factors, coefficients and weights. Time ratio memo/no-memo: total **0.995 [0.992, 1.000]**, geometric mean 0.997 [0.993, 1.003]. The memo does fire (e.g. F2 128: 6 hits / 8 misses), but main's faster confluent test (c3457c9, 66b5893) removed the 7 % it used to save. It stays on, as the user decided: exact, no harm, ~0.5 % gain.

**Controller C′ data** (`C/cprime_oracle_p7.md`; harness `analysis/exp/ll_Cprime.py`; C′ not built; C is still under evaluation):
- Cases: every non-timeout off failure in V + Gmatch (8: 6 false-confident, 2 abstain). Plus 4 of the 21 V timeouts (first seed per family F2–F5).
- Actions: the 13 remedies + skip_grow + skip_recurse + grow_past (epgp_reinterp is NA on grids; more_samples is NA on one grid). For timeout cases only the 6 actions that can make a run cheaper were run (lower_degree, narrow_band, sigma_reest, varpro, skip_grow, skip_recurse). The rest only add work to a run already past the cap and are counted as not rescued.
- **Oracle ceiling: 8/12 off failures = 67 %** (5/8 non-timeout, 3/4 timeouts). lower_degree rescues 8; varpro 3; the others ≤ 2. The ceiling is an upper bound: the harm of each action on cases off gets right was not measured.
- **With V1 as the trigger: 0/12.** V1 flags none of these failures (timeouts have no features at all).
- V1 false alarms on clean cases off gets right or correctly abstains: 3/86.
- Reading (data, not a decision): remedies exist (lower_degree above all), but V1 cannot point at the cases that need them. A trigger with resolution on false-confident runs is the open problem, not the action space.

**Not done / open:**
- N nulls not re-run on this pipeline (the V1 gate ran without nulls).
- The 25 SVD-bug reruns of §3.5 are superseded by the new corpora.
- `125b1f2` (main) committed a stray gitlink `Larned layers` (mode 160000) at the repo root; it came in with the sync. Left as is (main's commit).


Work stopped at the user's request. All verdicts below are **feasibility verdicts** on base main@66a5064 (the B0 copy). Final tuning is redone on the final pipeline (memory: learned-layers-feasibility-scope). Nothing was pushed, and nothing was merged into main.

## 1. Verdicts per layer

| layer | verdict | key numbers | report / commit |
|---|---|---|---|
| **V1** (failure detector) | **GO (feasible), not shippable yet** | LOFO AUROC 0.900 vs V0 0.681, Δ +0.219 [+0.078, +0.289] (paired cluster bootstrap; 49 clean, 92 injected). FIT-COMPATIBLE only: +0.244 [+0.083, +0.359]. Without resid: +0.150 [+0.004, +0.218]. Conformal α = 0.05 ship gate not evaluable (< 19 clean cal rows per fold). Cannot flag the 48/140 I runs that crash or time out (its features come from the output). | `sessions/LEARNED/V1/REPORT.md` on `claude/ll-validator-1b737b` (045f466) |
| **LB exact "modes" memo** | **GO** (exact speed-up) | 0 harmed runs and 0 coefficient diffs (G test 47 pairs, N 10, named 10/10, timing 10/10). Same-load time ratio 0.928 [0.896, 0.948]; per-run geo-mean 0.875 [0.817, 0.930]. Proposed on by default, since the output is bit-identical; **the user decides the default at the merge into main.** | `sessions/LEARNED/LB/REPORT.md` on `claude/ll-budget-287936` (6fda114) |
| LB learned skip (`budget="exact"` / `"fast"`) | NO-GO | Cross-fit saving 0.2 % (exact) / 0.7 % (fast, 2/165 harmed); skips nothing on G test; oracle ceiling only 14–17 %. | same LB report |
| L2d (global constants) | NO-GO | snr_min 2.5: +0.000 [0, 0]; theory cut 3.26: +0.053 [0, +0.158], which is 1 run and a timing artifact. PRED_LOGP replay over −5…−2 changes 0–1/62 runs (scores are bimodal). Every LOFO fold picks today's values (3 / −3). Theory rows LL-T30, LL-T31. | `sessions/LEARNED/L2d/REPORT.md` on `claude/ll-constants-1018c9` (50a0f19) |
| L2c (interval calibration) | NO-GO | 114 test cells: off coverage 0.895 (nominal 0.90). The scalar model (0.965) and the gbm (0.982) over-cover with wider intervals; neither is in [0.85, 0.95] on every LOFO fold. | `analysis/exp/out/ll_l2c_final.md` (learned-layers; code `analysis/exp/ll_l2c.py`) |
| L2b (P(top) calibration) | NO-GO | Raw P(top) ≥ 0.999 on 96 % of rows, so there is no resolution. Right-or-equivalent: best ΔBrier −0.032 [−0.073, +0.007]. | V1 report |
| H0 (high-κ scan) | NO-GO | Identical label + factors: G test 80/80 pairs, N 40/40, S 29/30 (the one difference: highk TIMEOUT where off is "equivalent"), named 22/22 (suite stopped at 45/60). Anytime CS on G: "no gain" (±0.069). It never changes an answer and only adds time. | rows `analysis/exp/out/ll_{G,S,N,named}.jsonl` (learned-layers) |
| H1 | not built | Only needed if H0 had shown a need. | — |
| C (controller) | NO-GO for now (safe, no gain) | N forking-paths null test passes at every depth 0–12 (fission and none). Corpus I null test stopped early: 6/35 cases of a stratified subset ran, and only 1 is usable (it passes at every depth; the other 5 crashed in the off run on the SVD bug), so it is not evidence either way. A harness bug (trace depths scored with ok=False) was fixed and the traces rescored; N is unchanged. C0 on G: 16 completed cases, 0 changed, gain +0.000 [0, 0] (plus 1 timeout at the 6 h cap and 1 off-run SVD crash). **Oracle ceiling 1/13 off-failures (8 %, a lower bound: only 1.9 of 13 remedies logged per case).** C1 learning curve is flat, so more data does not help. Bottleneck: diagnosis. The false-confident failures trigger no diagnosis. | `sessions/LEARNED/C/REPORT.md` on `claude/ll-controller-577bc7` (6d86b25; full pytest stopped before finishing, so not test-verified; oracle in `analysis/exp/out/ll_C_oracle.md`) |

Also relevant for main: with every layer off, the pipeline is **false-confident on 9/80 G-test cases**.

## 2. Where the data are
- **Shared data folder:** `D:\Larned layers\PDEFactorML\analysis\exp\out\` (gitignored). Index: `DATA_INDEX.json` / `DATA_INDEX.md`, rebuilt with `python analysis/exp/fastrun.py index`.
  - **H0 / off corpora:** `ll_G.jsonl` (G test, off + highk, 160 rows), `ll_S.jsonl` (60), `ll_N.jsonl` (80), `ll_named.jsonl` (90).
  - **LB fit+cal (off, lb_log):** `ll_G_fitcal_off.jsonl` (140), `ll_S_fitcal_off.jsonl` (50). Caveat: these ran on a frozen copy of 6b065d1. They are separable from the learned-layers rows (`step:raw_subset_frac`), so do not mix them into training without care. Paired verdicts are unaffected.
  - **Corpus I** (injected failures, V1): `ll_I.jsonl` (140).
  - **Each session's complete out/ folder:** `out/sessions/{LB,L2d,V1,C}/`. Copied there because archiving a session deletes its worktree. This includes V1's matched clean control `ll_Gmatch.jsonl` and C's logs, null tables and oracle.
- **Golden files:** `PDEFactorML/tests/data/learned_off_golden.json` (all layers off; made by `tests/data/make_learned_off_golden.py`), `structfit_golden.npz`.
- **Models** (on the session branches): LB `src/pdefactor/learned/models/lb_exact.pkl`, `lb_fast.pkl`; L2d `constants_sim-v2.json` (= today's values); C `controller_*.pkl` and `controller_banned.json` (C worktree); V1: see its report.
- **Tools** (learned-layers):
  - `analysis/exp/fastrun.py`: reuse by code sha, online runtime model `analysis/exp/models/runtime.json`, anytime-valid stop;
  - `analysis/exp/slots.py`: 10 CPU slots with reservations;
  - `ll_corpus.py`, `ll_gate.py`, `ll_named.py`, `ll_l2c.py`;
  - `sessions/LEARNED/SPEEDUP.md`: the speed-up methods.
- **Retrain commands:** `ll_budget_fit.py --retrain` (LB), `ll_l2d.py --retrain --workers 4` (L2d), plus V1 and C in their reports.

## 3. Sync state
- **Target:** main `125b1f2` ("Update D: contents", 2026-10-30 15:07). It includes 91f3581, 0390fd0, 867dcc0 (change outputs), c3457c9 and 66b5893 (speed, not bit-identical: the coefficients differ in the 7th digit), e1fb9ae (T70–T75, `test_ml_contract.py`) and 435b048 (V0.1 SVD overflow fix).
- **Done:** the merge is on branch **`ll-sync`** (worktree `.claude/worktrees/ll-sync`), committed there as **da223f4** and NOT on learned-layers (its full test suite was stopped before finishing).
  - Conflicts: only `loop.py`, 5 hunks, where our step-log `log.mark` lines met main's new code. Both sides were kept.
  - Every other file was checked against a 3-way merge with base 66a5064, and the line endings were kept.
  - The test result at commit time is in the ll-sync commit message.
- **Left to do:**
  1. Regenerate the off golden file on `ll-sync` (`tests/data/make_learned_off_golden.py`). The old golden describes 66a5064.
  2. Run the full suite, then fast-forward learned-layers to ll-sync.
  3. Merge the passing session branches (V1, LB memo), each with the full suite and the golden test. **Needs the user's OK.**
  4. Re-gate V1 on the synced code. This needs ~100 clean 5 %-noise grid rows with fit/cal splits to test the conformal α = 0.05 false-alarm gate (ship / no ship). Re-check the LB memo: golden identical, plus paired timing.
  5. Rerun the 25 runs that crashed on the SVD bug, now fixed by 435b048: 12 LB G fit+cal, 11 corpus I, 1 C0 G test, 1 L2d (G F4 seed 101); plus the 5 C corpus I null cases.

## 4. Recommended next steps
1. Finish the sync (steps 3.1–3.2), merge V1 and the LB memo, then re-gate them (3.4). Then write the final REPORT.md (B9), a per-layer on/off table in simple terms.
2. **C redesign, on the final pipeline:**
   - V1's failure score becomes C's trigger and diagnosis input;
   - first measure the true ceiling with a full remedy sweep: all ~13 remedies on every off-failure case, about 20 cases × 13 = 260 runs;
   - build C+V1 only if the ceiling is clearly above 8 %, say ≥ 30 %. Otherwise the gain has to come from main's algorithm.
3. **Main-side issues** (report, don't fix in layer branches):
   - false-confident 9/80 on G test;
   - `refine_factors` ZeroDivisionError;
   - `bayes_split.raw_evidence` IndexError;
   - `test_aggregate_cluster` IndexError (6 known errors);
   - S timeouts (26/50 LB S runs).
4. Optional V1 extension: an input-only check that runs before the pipeline, to cover runs that crash or time out.
5. Still pending from before: the CLAUDE.md rule-8 edit needs the user's OK.

## 5. Worktrees and branches (`D:\Larned layers\.claude\worktrees\`)
| worktree / branch | state | keep? |
|---|---|---|
| `ll-sync` / `ll-sync` | sync merge with main 125b1f2 | **keep** (next step) |
| `ll-budget-287936` / `claude/ll-budget-287936` (6fda114) | LB final; session archived; worktree left detached | keep the **branch**; the worktree can go |
| `ll-constants-1018c9` / `claude/ll-constants-1018c9` (50a0f19) | L2d final; archived | keep the branch (theory rows, retrain recipe); the worktree can go |
| `ll-validator-1b737b` / `claude/ll-validator-1b737b` (045f466) | V1/L2b final; archived | keep the **branch**; the worktree can go |
| `ll-controller-577bc7` / `claude/ll-controller-577bc7` | C final (6d86b25); session archived | keep the branch; the worktree can go |
| `ll-budget-0414d5`, `ll-budget-79adbf`, `ll-constants-048653`, `ll-constants-2c67d8`, `ll-controller-26973c`, `ll-controller-7ad049`, `ll-validator-c22e56`, `ll-validator-d407b2` (all at 3071bde) | unused duplicates from session restarts | **delete** (worktrees and branches) |
| `ll-speedsync` (empty folder) | leftover from the speed-up test | delete |
| `refs/remotes/dmain/head` | main 125b1f2, fetched read-only from `D:\` | keep until the sync lands |

Data from deleted worktrees is already in `analysis/exp/out/sessions/`.

**Shared notes:** `LL-status.md` (project board) and `LL-common-brief.md` in `C:\Users\<user>\AppData\Roaming\Claude-Secondo\side-session-notes\local_628a9ee6-108f-40ec-b913-3e04fabbd2d0\`.
