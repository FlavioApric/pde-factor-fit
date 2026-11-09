# SESSIONS

Every session starts with the `session-start` skill and ends with `sessions/<ID>/REPORT.md`.

| ID | owns | done criterion | status |
|---|---|---|---|
| MAIN | `src/pdefactor/core/`, `symbols.py`, `synthetic.py`, `analysis/`, `loop.py`, plan | Phase 0, 0b, 1, 3 | Phase 1 exact tests green (20/20) |
| S-INTERP | `src/pdefactor/interp/` | S posterior samples with weights π_s; coverage within ±5 % of nominal on the synthetic cases | not started (Phase 2) |
| S-AGG-CLUSTER | `aggregate.py`, `cluster.py` | 𝒲, k_eff, ρ̄, c̄_F; ARI ≥ 0.9 on the two-regime case with exact components | not started (Phase 2) |
| S-BASELINES-BENCH | `baselines/`, `benchmarks/` | benchmark grid + PySINDy/BOP-DMD + metrics of `benchmark-protocol` | not started (Phase 2) |
| S-PHASE4-ML | `src/pdefactor/learned/`, optional `seeds=` hook in `core/structfit.py`, `analysis/exp/e12–e14`, `tests/test_learned.py` | learned layers of PHASE4_ML_PLAN (L0, L2b/L2c, V1, remedy order) built with off switches; each passes or fails its gate and is reported | done 2026-10-29: L2c passes its gate; L0, L2b and V1 fail theirs (kept off); see sessions/S-PHASE4-ML/REPORT.md (PR #1) |

## Skills (expected in `.claude/skills/`)
- Project: session-start, pdefactor-core, benchmark-protocol.
- K-Dense: scikit-learn, pymc, sympy, pytorch-lightning, statsmodels, matplotlib, scientific-visualization, exploratory-data-analysis, uncertainty-and-units, experimental-design, scientific-critical-thinking, hypothesis-generation, literature-review, statistical-analysis.
- ARIS: experiment-plan, ablation-planner, run-experiment, analyze-results, result-to-claim, experiment-audit, novelty-check, research-lit, kill-argument (reviewer = a fresh Claude subagent).
- lonexreb: formal-math-ai.
- ML (added 2026-10-29, S-LEARNED parallel build): K-Dense shap, pymoo, stable-baselines3, statistical-power, get-available-resources; affaan-m/ecc mle-workflow (SKILL.md only, read before install).
- In git worktrees `.claude/` is absent (gitignored): read the skills from `D:\Larned layers\PDEFactorML\.claude\skills\<name>\SKILL.md`.
