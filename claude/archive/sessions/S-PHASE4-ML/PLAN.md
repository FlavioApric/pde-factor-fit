# S-PHASE4-ML — PLAN

Session **S-PHASE4-ML** (2026-10-29, cloud). Scope: the **learned** layers of `analysis/PHASE4_ML_PLAN.md` only. The deterministic layers (P0 oracle study and scoring, P0.3 simulator, V0 battery, L1a, controller C) belong to the local session and are not touched here.

Rules in force: CLAUDE.md 1–7, plus PHASE4 §2:
- off = today, bit-for-bit;
- a learned output is a proposal, a calibration or a flag only;
- the likelihood in the final comparison is fixed;
- the switch-on gate;
- the prior tag;
- the core changes only through an optional argument, with tests.

| step | layer | files | status |
|---|---|---|---|
| A1 | L0 seed hook in the core (`SEED_PROVIDER`, `seeds=`) | `core/structfit.py` | done, tests |
| A2 | L0 training distribution (generic exponential sums) | `learned/expsum.py` | done, tests |
| A3 | L0 network (2-D (Re s, Im s) heatmap + order head; Xie–Wakin–Tang / DeepFreq architecture) | `learned/expseeds.py` | in progress (torch CPU) |
| A4 | L0 experiment: λ efficiency vs CRB, order accuracy vs pencil+BIC, by SNR and spacing | `analysis/exp/e12_l0_seeds.py` | after A3 |
| B1 | L2b isotonic P(top) + loss-derived thresholds | `learned/calibrate.py` | done, tests |
| B2 | L2c monotone interval inflation + Mondrian conformal | `learned/calibrate.py` | done, tests |
| B3 | V1 one-vs-rest GBM + conformal risk control + OOD gate | `learned/validator.py` | done, tests |
| B4 | offline remedy ordering for C | `learned/remedy.py` | done, tests |
| W | wiring of B1–B4 into `loop.py` / `validate.py` / `controller.py` | — | waits for the local session's V0, P0.3 and C on main |
| C | L1b (gated by P0.1), L6 (deferred), L5 (rejected) | — | not built |

Periodic sync: `git fetch origin main` before each step; merge, not rebase.

## Status at the end of the session
L0 gate failed (E12, E15). L2c gate passed (E14). L2b and V1 gates failed under LOFO (E14). Remedy order is built but needs controller runs. L1b, L6 and L5 were not built. See REPORT.md.
