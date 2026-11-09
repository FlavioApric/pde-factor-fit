# FASI05 — report

## Deliverables
- `paper_fasi05.pdf` (72 pp.): complete edition of the paper, Phases 0–5. 11 chapters + glossary. Every theorem points to its proof as "Dim. ID, Catalogue p. N".
- `dimostrazioni_fasi05.pdf` (116 pp.): catalogue of proofs. Part I = 31 load-bearing proofs (A1–A31); Part II = 72 further proofs (B1–B72) by phase; final index by ledger ID with page.
- `../VOLUMES/Punto_di_partenza.pdf`: the former Volume I (Phases 0–8 overview), kept as the starting point. Its LaTeX sources and the old Volume II were deleted.
- Sources: `preamble05.tex` (shared style), `p_*.tex` (paper), `c_*.tex` (catalogue), `tiers.md` (Part I/II selection from the graph).
- Build: `pdflatex dimostrazioni_fasi05.tex`, `pdflatex paper_fasi05.tex`, twice each (xr-hyper cross-references in both directions).

## Layout rules applied
Displayed formulas, generous spacing, chapter brief (Starting from / Why / Role), motivation → intuition → statement → example → consequence, coloured boxes (theorem blue, definition green, example violet, intuition amber, warning/counterexample red), proofs as Idea + numbered Steps + "Why it works" + "Uses".

## Verification
- Both documents compile with 0 errors and 0 undefined references. Overfull boxes: paper 1 (1.9 pt), catalogue 0.
- All 51 "Dim." references in the paper resolve to a card in the catalogue (script check).
- Visual check: contact sheets of all 72 + 116 pages.

## Coverage and honesty
- Full proofs: 103 results. Proofs marked *condensed* (all steps and key formulas, routine computations referred to the research file): A27 (OPA-T1), A28 (OPF5A-T2), A31 (OPF5C-T2), B38, B52.
- Listed without proof (label + research file): TROP-3′/4, R5-P6/T4, P3-T2/T4/T5, INT-T1 and scattering (OPF5D), Hirota (INT-P5/P6), OPF5C structure lemmas, S4ID-L2/L5/C1/C2/P5–P7, OP-NL criteria, ALG-T1, MODREL-T1, F4LIN-T2, OPR2-P4/P6/O8/O9′, OPF5A-T3/T4/C1, plus cited, conditional, open and false results.
- Correction found while writing: Volume I and the old paper said P1-T5 covers ∂² and x^k (k ≥ 3). It does not (its hypothesis fails there; that case is open, P1-Q3). Fixed in the paper (Ch. 8, Ch. 11) and in the catalogue (A24).
- Proofs are transcribed and restructured from `work/*/PROOF_PACKAGE.md`; they were not re-audited. B65 Step 4–5 and A27/A28 follow the package; B71 step 2 and B72 are short summaries of the package arguments.
- Not included: Phases 6–11 (wait for Phase 11), the ~60-equation catalogue, Lean sources.
