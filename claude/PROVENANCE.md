# PROVENANCE: what every part of branch `model-expansion` is, why it is here, where it came from

| now | what it is | why it is here | came from (old repo) | in the paper? |
|---|---|---|---|---|
| `paper/model_expansion.tex` + `.pdf` | 21-page paper: ladder L0-L10, six-step algorithm with the guarantee contract, directions, the four founding questions, routes and ideas, worked examples, minimal route, open questions, and an appendix with the full specification step by step | the deliverable | new text from the specification `ProblemaBase/ALGORITMO_ESTESO.md`, `research/SYNTHESIS-2.md`, `ROUTES.md`, `piano di ricerca.md`, `PDEFactorML/ROADMAP_FOR_CLAUDE.md` | it is the paper |
| `code/ex_L6_dirac.py`, `ex_L7_poschl_teller.py`, `ex_L8_stark.py`, `ex_L9_L10_dict.py` and `.out` | four symbolic / high-precision worked examples, 35 checks (messages in Italian) | they check the examples of the paper | `ProblemaBase/work/S9-ALG/sympy` | Section "Four worked examples" |
| `code/out_of_class_inject.py` | generators of inputs outside the pipeline's class | the detect-and-refuse route needs test data | `PDEFactorML/analysis/exp/ll_inject.py` (branch `larned-layers`) | Section "A minimal route" |
| `tests/test_examples.py` | runs the four examples | verification | new | no |
| `claude/notes/ALGORITMO_ESTESO_it.md` | the full specification of the extended pipeline (Italian) | source of the paper's appendix | `ProblemaBase/ALGORITMO_ESTESO.md` | rendered in English as the appendix |
| `claude/archive/` | README of the examples and of the earlier paper folder | history | new / earlier layout | no |

Removed as redundant: a copy of the pipeline (`src/`, 34 test files) that this branch carried; the pipeline is on branch `main`. The proofs, routes registry and syntheses that the paper summarises are on branch `analytical`. The complete old-vs-new inventory is `INVENTORY.md` on branch `main`.
