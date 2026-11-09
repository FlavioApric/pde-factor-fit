# Handover from the fork session (2026-10-31) to the main session

The fork (session 1c39d277) stops writing. Main session takes over everything; the user wants it
done by a subagent of the main session, with no duplicate work. Nothing pushed. Nothing stopped.

## Committed on main (D:/ repo, local only, newest last)
771b4b5 T77–T84 (T77–T81 adopted on by default; T83 GROW_PAST, T84 EPGP_REINTERP off) ·
366b0f3 T87 triangular solve in `_per_bin_neg` (~100×, exact; also carried your WARM_BINS = T85, T86 row) ·
f4629c1 numbering note (second T85 = T87) · 9532d55 T88 RAW_GOF (on) · 14d13be T89 grid complex σ ·
fff5919 T90 verdict: EPGP_REINTERP not adopted (cover90 1.00→0.50 on beam 2000 s2 / 400 s0, 2.1× time) ·
7fbef14 T91 scattered complex σ · eaa8f9c P8 SINDy arm files.
Full suite before T87/T88: 179 passed. Quick tests after each later commit: green.

## Verified results (adopted config)
heldout grid 10/11 = ref; heldout 400 10/12 (ref 9, false-confident 1→0); conjugate 10/11 (ref 5);
intervals 14/14 (ref 13); edge = v1 (TPD 400 5 % false-confident, now MISFIT by T88 — not rerun);
fc: false-confident 5→1 (F5-131 grid 5 %, open T82), crash 1→0; F4-209 400 5 % timed out (rerun below).
P3 (T83): premise wrong — two_pairs never hits M_LIMIT; with switch (4,4) +47 nats but still UNDECIDED,
odd-ξ fits at confluent κ=0 (open). Needs held-out A/B before any adoption.

## STILL RUNNING (do not restart; read their outputs)
- E13 rerun (P6), started 02:43, one process per family: PIDs 36928 (F4), 41832 (F5); F1–F3 done.
  Output benchmarks/out/e13_v4_F{1..5}.jsonl (+ .log). Pipeline + SINDy methods, seeds 0–3, 1 %.
  Next: merge the 5 files, classify misses (abstain / data-equivalent / wrong) with e13_summary.py.
- F4-209 rerun with T87: PIDs 3820 (pool) + 30864 (child), log benchmarks/out/micro/draws_fc_f4209_t85.log,
  rows appended to benchmarks/out/micro/draws_fc_cand1.jsonl. Started before T88 → expect
  false-confident; T88 should flag it (raw GoF −inf in your study).
- PID 8072 `gof_calib.py` is YOUR session's scratch script.
- P7a sync agent (subagent of the fork, cannot be transferred): resets the partial copy in
  D:/Larned layers/.claude/worktrees/ll-sync, syncs main → ll-sync per SYNC.md, re-applies the learned
  hooks, checks off == main, commits on ll-sync only. It will report to the fork; the fork forwards
  its report to you. Do not start a second sync.

## Remaining plan for the main session's subagent
1. P6: finish E13 classification (above).
2. P8 pipeline arm: `benchmarks/out/p8_sindy_arm.md` inputs (10 cases × grid 1 %/grid 5 %/400 5 %, s0),
   current main, ≤ 8 CPU; then the pipeline+ML arm after P7.
3. P7 after the sync commit: corpus (small, grid-first, ~100 clean 5 % grid rows for the conformal gate,
   1200 s cap), V1 retrain + LOFO + conformal α=0.05, downgrade-to-UNDECIDED option; LB memo re-gate;
   local merge V1+LB after gates (user OK'd); controller C′ oracle sweep with V1 trigger — C stays
   under evaluation, bring the data to the user.
4. Before P8: calibrate T88 (`raw_gof_log10p`) over all cached scattered inputs under the TRUE law —
   it searches excited bins only up to kmax_max=16, so energy beyond |n|=16 could give a false MISFIT.
   Open items: T82 F5-131, T83 two_pairs, T90 interval narrowing in EPGP refit.
5. Ask the user before: any push, Azure VM, controller decision, deleting worktrees.
