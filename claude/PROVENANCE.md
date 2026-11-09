# PROVENANCE: what every part of branch `analytical` is, why it is here, where it came from

The earlier private research repository (called "the old repo" below) had a folder `ProblemaBase/` with all analytical work. Its content is organised here as follows.

| now | what it is | why it is here | came from (old repo) | covered in the paper? |
|---|---|---|---|---|
| `paper/analytical.tex` + `.pdf` | the paper, 130 pages, Phases 0-10: Part I (Sections 1-6, the grouping principle in Structure-B order), Part I-B (full chapters of Phases 0-5), Part II (Phases 6-10), limits, open problems, directions, appendices (proofs of the main results, glossary, primer, project bibliography of 112 sources, explained walk-throughs) | the deliverable | merge of `ProblemaBase/PAPER/paper.tex` (first manuscript), `FASI05/paper_fasi05.tex` (phases 0-5), `FASI_ALL/paper_tutte_le_fasi.tex` (phases 0-10), `PAPER_EXPLAINED/E1-E16.tex`, plus the Structure-B theory sections of the main paper | it is the paper |
| `paper/analytical_proofs.tex` + `.pdf` | the catalogue of 155 proof cards (Dim. A1-A53, B1-B155) and 43 list cards, 263 pages | all proofs, cited from the paper as "Dim. An/Bn" | `FASI_ALL/dimostrazioni_tutte_le_fasi.tex` (it contains the phases 0-5 catalogue `FASI05/dimostrazioni_fasi05.tex`) | yes: each theorem points to its card |
| `code/verification/` | 534 symbolic or high-precision scripts and their outputs, one flat folder (file names unchanged; the session each came from is in `claude/archive/` and `claude/verification_results.md`) | they check the claims; they do not prove them | `ProblemaBase/work/*/sympy`, `ProblemaBase/research/*` | cited in the proof packages |
| `code/lean/` | Lean 4 formalisation of fifteen algebraic theorems (`PBLean`, `F10`) and the lake project in `lean/project/` | machine check of core results | `ProblemaBase/PBLean_src`, `PBLean` | Section on limits |
| `tests/test_verification.py` | eight quick checks as pytest | continuous integration | new | no |
| `claude/proofs/` | 29 proof packages (one per research session) and `LEDGER.md` (the claim ledger with the status of every claim) | the full proofs and the authoritative status of each claim; the catalogue is the readable version | `ProblemaBase/work/*/PROOF_PACKAGE.md`, `claims/LEDGER.md` | status labels in the paper follow the ledger |
| `claude/notes/` | the problem statement, routes registry, open problems, final report, notation, bibliography, synthesis | the project's governing documents | `ProblemaBase/{PROBLEM,ROUTES,PROBLEMI_APERTI,REPORT_FINALE,NOTAZIONE,BIBLIOGRAFIA,SYNTHESIS-2}` | summarised in Part II and the open-problem sections |
| `claude/archive/work/` | plans, reports, audits, check requests of each session | what was tried, audited and fixed | `ProblemaBase/work/*` (non-script files) | not needed to read the paper |
| `claude/archive/research/` | literature scouting, citation audits, devil's-advocate reviews, bibliographies | where the sources and the criticisms came from | `ProblemaBase/research/*` | the bibliography appendix |
| `claude/archive/{claims,inbox,origin,ProblemaBase}/` | earlier ledger versions, the coordination inbox, the author's starting documents (`VOLUMES/Punto_di_partenza.pdf`, `piano_di_ricerca.md`), gates and board files | history of decisions | `ProblemaBase/{claims,inbox,VOLUMES,GATE*,BOARD,...}`, `piano di ricerca.md` | no |
| `claude/archive/editions/` | the non-paper files of the earlier editions and the first manuscript as a single `.tex` (`first_manuscript.tex`) | the editions were merged into the two papers; their build reports, dependency tiers and the first manuscript's editorial notes are kept | `FASI05`, `FASI_ALL`, `PAPER`, `PAPER_EXPLAINED` | see below |

## Editions merged into the paper (nothing lost)
`tools/check_coverage.py` (on branch `main`) compares the sources of each old edition with the new paper or proofs file: proof tags `\led{..}`, titles of theorems/examples/warnings, labels, headings and "Dim." references.

| old edition | pages | result of the check |
|---|---|---|
| complete edition (Phases 0-10) | 117 + 263 | 183/183 proof tags, 131/131 theorem titles, 141/141 labels present; its catalogue is `paper/analytical_proofs.tex` itself |
| phases 0-5 edition | 76 + 116 | 100/100 tags, 93/93 theorem titles, 104/104 labels present; the 116-page catalogue is a subset of the 263-page one (23/23 tags, 37/37 labels) |
| explained edition (first manuscript with explanation boxes) | 70 | the 15 explanation files E1-E16 are Section "Explained: step-by-step walk-throughs"; the theorem content is in the paper |
| first manuscript | 40 | 57/58 tags; the missing one is an editorial note; kept as `claude/archive/editions/first_manuscript.tex` |

Not copied (and why): LaTeX build files, run logs and `.err` files, backup copies of superseded drafts, the Lean toolchain installer binaries, regenerable caches. The complete old-vs-new inventory is `INVENTORY.md` on branch `main`.
