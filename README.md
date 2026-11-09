# pde-factor-fit · branch `analytical`

**What this branch is.** The mathematics behind the project: what one exact solution of a linear PDE remembers about its equation (identification, splitting into factors, the interaction term, the limits of exactness) and its extension to nonlinear equations, systems, variable coefficients, encoders and dictionaries: **all eleven phases (0-10)**.

**Open this first:** [`paper/analytical.pdf`](paper/analytical.pdf), the paper (130 pages; LaTeX source `paper/analytical.tex`). All proofs are in [`paper/analytical_proofs.pdf`](paper/analytical_proofs.pdf) (263 pages, 155 proofs; source `paper/analytical_proofs.tex`); the paper cites each proof as "Dim. An/Bn".

| folder | what is in it |
|---|---|
| `paper/` | the paper and the proofs, one `.tex` and one `.pdf` each |
| `code/` | `verification/` the symbolic and high-precision checks behind the proofs (and their outputs), `lean/` the Lean 4 formalisation |
| `tests/` | `test_verification.py`: a quick subset of the checks as pytest |
| `claude/` | everything else, for Claude sessions: rules, status, map, the 29 proof packages and the claim ledger (`claude/proofs/`), all plans, reports, audits and literature notes (`claude/archive/`), where each file came from (`claude/PROVENANCE.md`) |

```bash
pip install -e ".[dev]" && pytest -q tests/test_verification.py     # 8 checks, ~30 s
cd paper && latexmk -pdf analytical.tex                              # or analytical_proofs.tex
```

Every statement carries a status label (proved / proved modulo a cited theorem / conditional / open / false). The proofs were reviewed by independent Claude agents, not human referees; Lean covers fifteen core algebraic theorems.
The other branches are `main` (the algorithm and its two papers), `ml-layers` and `model-expansion`.
Licenses: code MIT ([`LICENSE`](LICENSE)), papers CC BY 4.0 ([`LICENSE-papers.md`](LICENSE-papers.md)); please cite via [`CITATION.cff`](CITATION.cff). Author: Flavio Pricoco.
