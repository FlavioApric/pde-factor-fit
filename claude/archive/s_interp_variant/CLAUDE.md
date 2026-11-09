# PDEFactorML — working rules

Goal: the pipeline of `D:\ProblemaBase\NOTE_ML\ml_pipeline_note.tex`. Data (t,x,y) → interpolants with probabilities → analytic core per interpolant (factors, components, terms, E_int, c_F) → distribution over factors → grouping → recursion → equation with probabilities.
Plan: `C:\Users\<user>\.claude-secondo\plans\to-plan-use-the-groovy-chipmunk.md`. When editing plans, only add; never remove or rename.

## Rules
1. **Separation.** `D:\ProblemaBase` (the analytic theory) is read-only from here. Code lifted from it carries a comment `# origin: <path>:<line>`.
2. **Every session starts with the `session-start` skill.** It covers: skills check, research first, a PLAN before code, and a REPORT at the end.
3. **The analytic core (`src/pdefactor/core/`) is deterministic and delicate.** The outer layer calls it only as a black box on each posterior sample. Change the core only with tests covering the change.
4. **The outer layer is Bayesian.** Loop, regrouping, thresholds and hyperparameters are estimated by posterior inference, not fixed by hand. Uncertainty is propagated by Monte Carlo, never by linearisation (E_int and Ann(·) are discontinuous).
5. **Output contract.** Never print "law identified" from numerical data. Labels: `FIT-COMPATIBLE`, `MISFIT`, `ID-KER(class)`, `UNDECIDED` (ALGORITMO_ESTESO §0.5).
6. **Domains.** The factor split is proven only on simply connected Ω (C12-T1′). Analyse rectangles/convex cells, never a region with holes.
7. **Use the analytic work to choose algorithms.** Before choosing or changing an algorithm, read `analysis/THEORY_TO_ALGO.md` and query the ProblemaBase graph (`cd D:/ProblemaBase && graphify query "<topic>"`), then the LEDGER rows it points to. Use only DIMOSTRATO rows, or CON-FONTE rows with a verified source, as foundations. Add new findings to THEORY_TO_ALGO.md.

## Commands
- Python: `D:\PDEFactorML\.venv\Scripts\python.exe`
- Tests: `.venv/Scripts/python.exe -m pytest -q`
- Vendored skill repos are in `.vendor/` (gitignored). Read a SKILL.md before using it; never run vendor scripts.
