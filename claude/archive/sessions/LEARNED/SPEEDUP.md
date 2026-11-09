# How to make learning and testing the layers faster (S-LEARNED, 2026-10-30)

The user asked how training and testing the learned layers can be sped up when needed. Training the models themselves is cheap: logistic models and gradient boosting fit in seconds. **Almost all of the time goes into producing corpus rows, i.e. running the pipeline on each case.** So the speed-ups below either produce fewer rows, make each row cheaper, or reuse rows.

## 1. What the time is spent on (measured on the shared rows, 153 runs: S 41, G 32, N 80)

| finding | number | what it means |
|---|---|---|
| H0 on vs off, finished pairs | **68 of 68 give the same answer**; the on arm costs +52 % time (5557 s vs 3665 s) | almost all of the on-arm compute is spent on cases where the layer changes nothing |
| S runs that CRASH or TIMEOUT | **22 of 41 (54 %)**; each TIMEOUT burns the full 1200 s | about half of S's compute produces no usable row |
| tail runs | the slowest 10 % of runs use 29 % (S) and 50 % (G) of the time | a few hard cases set the wall-clock |
| step time vs how often the step changes the result | `recurse` 1370 s, changes 1 %; `grow` 934 s, 2 %; `complex` 427 s, 0 %; `bootstrap` 1107 s (only needed for coverage) | several expensive steps almost never change the answer |
| pure-noise N runs | median 2 s | the null tests are cheap; never cut them |

## 2. Methods, ranked by gain per effort

| # | method | how | expected gain | effort | risk / guard |
|---|---|---|---|---|---|
| 1 | **Skip on-arms that cannot act** | Each layer exposes a cheap `would_act(state)` check at its hook. If it says no, the on row is a copy of the off row. This is exact, because with the layer not acting the output is the off output, which the golden test already guarantees. | H0 now: about −50 % of the on-arm cost. Applies to every layer with a trigger (H0, V1, C's early stop). | small | Test: for each layer, `would_act=False` ⇒ output bit-identical to off on the golden cases. Report the trigger rate. |
| 2 | **Fork at the hook** (shared prefix) | Run off once up to the hook, snapshot the state, and run each arm from the snapshot. It uses C's `_memo` (the one shared memo mechanism). | Saves the prefix (core + grow + decide, about 50–70 % of a run) for every extra arm | medium | Test: snapshot → resume equals a full run. |
| 3 | **Replay from logs instead of rerunning** | Record the quantities each decision compares against a threshold, then evaluate new thresholds offline. Already done for `PRED_LOGP` (`lp_trace`) and for LB's guard features. Extend it to the per-mode SNRs (snr_min), the candidate evidences (L2b P(top)) and the interval draws (L2c). | Threshold layers (L2d, LB, L2b, L2c) can be evaluated with **zero reruns**; only the finally chosen value is confirmed by real runs | small–medium | A replay is exact only while the downstream path is unchanged. Mark rows where the threshold would change a later step, and rerun only those. |
| 4 | **Sequential (anytime-valid) gates** | Run cases in a random order stratified by family, so any prefix stays balanced. After each batch, update a confidence sequence on the paired difference (Howard et al. 2021; Waudby-Smith & Ramdas 2023, betting CS). Stop when it excludes 0 (success), excludes the smallest useful effect (futility), or n is reached. | Typically 30–60 % fewer runs when the answer is clearly yes or clearly no; the early reads of L2d and H0 are both "clearly nothing". | small | The CS stays valid under optional stopping, so stopping early is honest (an ordinary CI is not). The null tests still run in full. |
| 5 | **Remove the waste: crashes and timeouts** | (a) Fix the known crash bugs in main: `bayes_split.raw_evidence` IndexError, `refine_factors` ZeroDivisionError, `validate.predictive_bins` SVD failure. (b) A timeout scaled per family (e.g. 3× the off median), since a timeout counts as not-right anyway. (c) Longest-expected-first scheduling (LPT), so the slow tail starts first. | S: up to about 2× (54 % of rows wasted today). G wall-clock: −20–30 % from scheduling. | (a) main's work; (b)(c) small | (a) must be fixed in main with tests, not in a layer branch. (b) the same timeout for off and on. |
| 6 | **Screen on low fidelity, confirm on full** (successive halving / Hyperband, Li et al. 2018) | When many arms are compared (L2d's thresholds, C3's settings), run all arms on cheap settings (fewer GP samples, bootstrap 0, ALT_TOP 1, one seed per family) and promote only the top third to full runs. | 3–5× fewer full runs in the arm search | medium | Only for choosing arms, never for the final gate. Check first that the rank correlation between cheap and full is high (Spearman ≥ 0.7 on a pilot), or skip this method. |
| 7 | **Turn off outputs the metric doesn't use** | In screening runs, set `bootstrap=0` when the metric is right-set or false-confident (only L2c's coverage needs the bootstrap). | −10–15 % per run | trivial | Gate runs keep the full settings. |
| 8 | **One corpus, every export** | Every corpus run records the union of all layers' exports (V0, resid, lp_trace, guard features, per-mode SNRs, step log, code sha), so one row serves every layer and no session reruns a case for a missing field. | Avoids the duplicate runs seen today (L2d / LB / C each ran parts of the off arm on G) | small | Rows carry the pipeline sha; a row from another sha is rejected automatically. |
| 9 | **Spend logging on informative cases** (active learning) | For C's remedy logs, choose which (case, remedy) to run by Thompson sampling on the current RemedyTable posterior, instead of uniformly at random. Skip cases where off is already right and confident. | 2–3× fewer logged runs for the same policy quality | medium | Keep a uniform-random slice (about 20 %) so the policy evaluation stays unbiased (inverse-propensity weights). |
| 10 | **More hardware** | Run the slot pool across a second machine or cloud workers; the slots are just lock files plus a job list. | Linear in the cores added | setup + cost | Needs the user's OK. A GPU does not help: the pipeline is CPU numerical code. |

## 3. Recommended order
1. **Now, in the layer branches, cheap:** #8 (one row schema with the sha), #4 (sequential gates in `ll_gate.py`), #7, #5(b)(c).
2. **Next:** #1 (`would_act` per layer), #3 (replay for snr_min / P(top) / intervals).
3. **For the final tuning on the final pipeline:** #2 (fork at the hook), #6 (multi-fidelity arm search), #9 (active logging). Fix #5(a) in main before that run.

Rough total for the final tuning round with steps 1–3: the same verdicts from about 3–5× less CPU. The largest single items are the on-arm no-ops (#1) and the crash/timeout waste on S (#5).

## 4. What is never cut
- The off golden test.
- The null tests: N, and C's forking-paths test at every depth.
- The paired design: the same cases and the same timeout for off and on.
- LOFO by family.

These are the safety checks, and they are cheap.

## 5. Built: `analysis/exp/fastrun.py` (2026-10-30)
A general harness that works for any corpus, any learned arm and any pipeline version. It wraps `ll_corpus` (same cases, same `run_one`, same CPU slots) and is tested in `tests/test_fastrun.py` (7 tests).
- `fastrun.py run …` (same case options as `ll_corpus`, plus `--arms off X Y`):
  - **reuse:** `--reuse <globs>` copies rows with the same case, arm and pipeline sha; `--accept-nosha` also takes legacy rows;
  - **order:** stratified by family, longest first inside a round, arms of a case together;
  - **online runtime model:** updated after every run;
  - **sequential stop:** `--sequential --delta`;
  - **per-case cap:** `--adaptive-cap k`, the same cap for every arm of a case.

  New rows carry `code_sha`, the tree hash of `src/` plus `-dirty`.
- `fastrun.py train --rows <globs>` refits the runtime model (`analysis/exp/models/runtime.json`) from whatever rows exist. It retrains in seconds and adapts by itself when the pipeline changes. Measured on 336 rows from every session: median leave-one-out error ×1.9, against ×7.7 for a single global median.
- `fastrun.py replay --rows … --arm X` shows what stopping and ordering would have saved on rows that already exist.

**Measured honestly, on the current H0 rows (S 22, N 40, G 21 pairs):**
- The anytime-valid stop needs about 55 identical pairs to conclude "gain < 0.1" at α = 0.05; 26 pairs for < 0.2. Today's corpora are at or below that size, so **sequential stopping saves nothing at the feasibility stage**. It pays off in the final tuning, on larger corpora.
- Ordering by predicted runtime changes the 4-worker makespan by −7 % (S), +4 % (N) and +17 % (G): **no reliable gain** at these sizes. Keep the default order.
- **The real savings now:** reuse (no duplicate runs between sessions), `--adaptive-cap` on screening runs (the slowest 10 % of runs take 29–50 % of the time), `bootstrap=0` when coverage is not measured, replay for threshold layers, and copying the off row when a layer does not act.
- **Reusing current off rows across branches is allowed with `--accept-nosha`** while every branch passes the off golden test: the off output is then bit-identical, whatever the branch.

## 6. Accuracy before speed (user direction, 2026-10-30)
The user's words, relayed: "we are always prefering accuracy to speed even i it means significatly more ofc". What this means for the methods above:
- **Allowed:** speed-ups that give exactly the same decisions: reuse by sha (#1 of §5), forking at the hook (#2), exact replay (#3), copying the off row when the layer provably does not act (#1 of §2), scheduling, and more hardware. Also allowed: stopping a *test* early with a valid sequential rule (#4).
- **Screening only, never in a gate or a shipped default:** the per-case cap (`--adaptive-cap`), low-fidelity screening (#6) and `bootstrap=0` (#7). A verdict is always confirmed at full settings and the full timeout. A low-fidelity screen may not discard an arm unless the rank check holds, and in doubt the arm goes to full runs.
- **LB (speed layer):** the target is **0 % harmed runs**, not 2 %. A skip is allowed only when it is proven exact, or when it shows 0 harmed runs with a high-probability upper bound small enough to pass; otherwise LB stays off. It is opt-in in any case.
- **C (controller):** the stopping rule weighs accuracy far above time. The cost term is only a tie-breaker, and the wall-clock budget is generous.
- **Addition (user, 2026-10-30):** a faster version that may lose up to 2 % accuracy is also wanted, as an opt-in side result for training and screening runs. LB therefore ships two opt-in profiles:
  - `budget="exact"`: 0 % harm, the candidate for normal use;
  - `budget="fast"`: at most 2 % harmed runs with a high-probability guarantee, for training and screening only, never on by default.

  The default pipeline stays at full accuracy.
