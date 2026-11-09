# pde-factor-fit · branch `analytical`

**What this branch is.** The mathematics behind the project: what one exact solution of a linear PDE remembers about its equation (identification, splitting into factors, the interaction term, the limits of exactness) and its extension to nonlinear equations, systems, variable coefficients, encoders and dictionaries: **all eleven phases (0-10)**.

**Open this first:** [`paper/analytical.pdf`](paper/analytical.pdf), the paper (130 pages; LaTeX source `paper/analytical.tex`). All proofs are in [`paper/analytical_proofs.pdf`](paper/analytical_proofs.pdf) (263 pages, 155 proofs; source `paper/analytical_proofs.tex`); the paper cites each proof as "Dim. An/Bn".

| folder | what is in it |
|---|---|
| `paper/` | the paper and the proofs, one `.tex` and one `.pdf` each |
| `code/` | `verification/` the symbolic and high-precision checks behind the proofs (and their outputs), `lean/` the Lean 4 formalisation |
| `tests/` | `test_verification.py`: a quick subset of the checks as pytest |
| `claude/` | everything else, for Claude sessions: rules, status, map, the 29 proof packages and the claim ledger (`claude/proofs/`), all plans, reports, audits and literature notes (`claude/archive/`), where each file came from (`claude/PROVENANCE.md`) |

## Quick start (no Python needed to read it)

1. **Read:** open [`paper/analytical.pdf`](paper/analytical.pdf). Part I is the theory of Phases 0-5 (concise first, then each phase in full), Part II is Phases 6-10, then limits, open problems and appendices. Every proof is in [`paper/analytical_proofs.pdf`](paper/analytical_proofs.pdf); when the paper says "Dim. A12" or "Dim. B40", look up that number there.
2. **Check a result yourself** (Python 3.10 or newer):

```bash
git clone -b analytical https://github.com/FlavioApric/pde-factor-fit.git
cd pde-factor-fit
pip install -e ".[dev]"
pytest -q tests/test_verification.py                  # 8 symbolic checks, about 30 s, expect "8 passed"
cd code/verification && python s8_galois.py           # one check by hand, 2 s
```
Expected output of the last command: a list of `[OK] ...` lines ending with `RISULTATO: TUTTO OK` (the scripts were written in Italian; `TUTTO OK` = all OK). Every script in `code/verification/` is standalone: run it from inside that folder with `python <name>.py`; its stored output is next to it as `<name>.out`.
3. **Rebuild the PDFs:** `cd paper && latexmk -pdf analytical.tex` (or `analytical_proofs.tex`); needs a LaTeX installation.

## Which file do I open?

| I want to ... | open |
|---|---|
| understand the idea and the results | `paper/analytical.pdf`, first chapters (running example, results table, dependency graph of the 11 phases) |
| see the proof of a theorem | `paper/analytical_proofs.pdf` (index at the front; "Dim. An" = Part A, "Dim. Bn" = Part B) |
| see a computer check of a claim | `code/verification/` (scripts + `.out`); file names are `<session>__<name>`-style, the proof card names the script |
| see the Lean formalisation | `code/lean/` (Lean 4, `lake build`; fifteen core algebraic theorems) |
| see how a claim was reviewed | `claude/proofs/` (one package per theorem group) and `claude/proofs/LEDGER*` (status of every claim) |

## How to read a status label

`proved` / `proved modulo a cited theorem` / `conditional` (needs a stated hypothesis) / `open` / `false` (a counterexample is given). Identification comes in several senses, written ID-ann, ID-ker, ID-res, ID-fam, ID-lim; the paper says exactly which one each theorem proves. The proofs were reviewed by independent Claude agents, not human referees.

## Troubleshooting

| symptom | fix |
|---|---|
| `pip install -e .` complains about packages | use the `analytical` branch's own `pyproject.toml` (it installs only the checks' dependencies); do not mix with `main` |
| a verification script is slow or hangs | the quick subset in `tests/` finishes in seconds; the full set (534 files) includes long high-precision runs, run those one by one |
| LaTeX errors | needs a recent TeX Live; the papers are single files with the bibliography embedded, nothing else to install |

## Folders

| folder | what is in it |
|---|---|
| `paper/` | the paper and the proofs, one `.tex` and one `.pdf` each |
| `code/` | `verification/` the symbolic and high-precision checks behind the proofs (and their outputs), `lean/` the Lean 4 formalisation |
| `tests/` | `test_verification.py`: a quick subset of the checks as pytest |
| `claude/` | everything else, for Claude sessions: rules, status, map, the 29 proof packages and the claim ledger (`claude/proofs/`), plans, reports, audits and literature notes (`claude/archive/`), where each file came from (`claude/PROVENANCE.md`) |

Glossary: *symbol* = the polynomial in (d/dt, d/dx) that defines the equation; *factor* = an irreducible piece of it; *interaction term* = what is lost when two factors are fitted separately instead of together; *Friedrichs angle* = how distinguishable two solution families are.
The other branches are `main` (the algorithm and its papers), `ml-layers` and `model-expansion`.
Licenses: code MIT ([`LICENSE`](LICENSE)), papers CC BY 4.0 ([`LICENSE-papers.md`](LICENSE-papers.md)); please cite via [`CITATION.cff`](CITATION.cff). Author: Flavio Pricoco.
