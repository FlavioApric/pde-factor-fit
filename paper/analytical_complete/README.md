# The complete analytical edition (Phases 0-10) in its original format

| file | content |
|---|---|
| `paper_tutte_le_fasi.pdf` / `.tex` | the paper, 117 pages: Part I (chapters 1-10: the constant-coefficient theory and its nonlinear extension), Part II (chapters 11-21: systems and gauge, variable coefficients, convergence and noise, the analytic encoder, the universal dictionary, what Phase 10 changed, the extended algorithm, limits, the complete list of open problems, directions not taken) |
| `dimostrazioni_tutte_le_fasi.pdf` / `.tex` | the companion catalogue of proofs, 263 pages: Part I A1-A31, Part II A32-A53, Part III B1-B72, Part IV B73-B155 and 43 list cards; every "Dim. An / Bn" in the paper points here |
| `p_ch*.tex`, `c_*.tex`, `preamble_all.tex` | chapter sources of the paper, proof-card sources of the catalogue, shared preamble |
| `REPORT.md`, `STATE.md`, `tiers.md` | build report, state of the work, dependency tiers (Italian) |

Build (the two documents cross-reference each other, so run them alternately):

```bash
pdflatex dimostrazioni_tutte_le_fasi.tex && pdflatex paper_tutte_le_fasi.tex
pdflatex dimostrazioni_tutte_le_fasi.tex && pdflatex paper_tutte_le_fasi.tex
```

The 57-page paper in `../analytical/` is the SIAM-style edition of the same material (Part I in the order of the main paper's Structure B, Part II from chapters 12-21 of this edition).
Earlier editions: `../analytical_phases05/` (phases 0-5: 76-page paper, 116-page catalogue), `../analytical_explained/` (plain-language edition), `../analytical_original/` (the first long manuscript).
