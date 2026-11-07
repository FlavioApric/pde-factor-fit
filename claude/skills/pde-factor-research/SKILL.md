---
name: pde-factor-research
description: Navigate and extend the pde-factor-fit repository (factor structure of linear PDEs from data). Use when asked to run the pipeline, read a paper, add tests or benchmarks, or continue the research on the analytical, ml-layers or model-expansion branches.
---

# pde-factor-research

1. Read `claude/CLAUDE.md` (rules) and `claude/STATUS.md` (current state) on the branch you work on.
2. Pick the branch: `main` for the algorithm and the papers, `analytical` for proofs, `ml-layers` for learned layers,
   `model-expansion` for nonlinear, variable-coefficient and other extensions.
3. Navigate with `claude/MAP.md` (graph) and `claude/REPO_MAP.md` (all branches).
4. Run quick tests before and after a change: `pytest -q tests/test_core_exact.py tests/test_ml_contract.py`.
5. Output labels are `FIT-COMPATIBLE`, `MISFIT`, `ID-KER(class)`, `UNDECIDED`; never claim a law is identified.
6. Credit: the author is Flavio Pricoco; keep `LICENSE` and `LICENSE-papers.md` intact.
