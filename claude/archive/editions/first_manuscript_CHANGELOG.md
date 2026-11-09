# Editorial change log (paper v2)

Source: `paper.tex` (backup of the previous version: `paper_v1_backup.tex` / `paper_v1_backup.pdf`). Compiled with `latexmk -pdf paper.tex` (MiKTeX): 22 pages, no errors, no undefined references or citations, 4 overfull lines of 1.5-7 pt left.

## Verification statement
- Compiled: yes. Rendered and inspected visually: pages 3, 5, 8, 12, 14, 19, 20, 22 of the new PDF and pages 3, 7, 12, 14, 15, 16 of the old one. Not every page was inspected.
- Mathematical content compared with the previous version only by reading the edits; no statement, equation, or reference was changed except as listed under "Content-affecting edits".

## Layout and typography
- Long displays split with `aligned`: spectral formula (3.x), gamma_N / sum map S (Thm 5.5), Dyson series (6.x), Burgers t^2 computation (7.1), worked-example EP test.
- Theorem 4.1 reformatted as items (a), (b), (c); wording unchanged.
- Proofs now use the `proof` environment (QED placement consistent).
- Added `leadin` (question / why / result / needs) before Sections 2, 4, 5, 6, 7 and `takeaway` ("Why it matters") after Lemma 2.5, Thm 4.1, Sec 5, Sec 6.
- Floats placed with `[!htb]`; widow/club penalties; larger table row spacing; ragged-right table cells; badges and ledger tags one size larger.
- Figure 1 enlarged with section tags inside the boxes; Figure 9 redrawn (top-down, larger font, decision branch readable); Figure 5 and Figure 4 labels de-overlapped; Figure 6 split into labelled panels (a), (b) with legend below panel (b); captions now say what to notice.
- Fixed a rendering defect: stray "[]" after the "false" badge in two propositions.

## Exposition
- Status labels explained before Table 1 (new subsection 1.2); notation table (Table 2) and roadmap added; appendix glossary gets a "Used in" column.
- Transitions added at the start of every section and between Sections 5-6 and 6-7.
- Table 3 (the seven steps at a glance) added to Section 8; complexity table numbered and referenced.
- Worked example restructured as a numbered list with aligned equations.
- Concept anchors: `Ann(e^x)` example after the annihilator definition; illustration of G_u and the point spectrum after Prop 4.2.
- Bibliography entries are now actually cited (Malgrange-Ehrenpreis, Bezout, Hormander, Dyson, Engel-Nagel, Cole-Hopf, Krujkov, Novikov, Palamodov).

## Content-affecting edits (all remove unsupported material I had added in v1)
- Removed the claim "components lie in H^m since c_F < 1 for the two transport directions" in the worked example; replaced by a pointer to Theorem 5.5.
- Removed "polynomial in the degree / polynomial for 2 variables" for factorization; kept "standard computer-algebra operation".
- Removed the parenthetical "Fig. 2 is the picture of its principal symbol" in Sec. 3.3.

## Unresolved issues for the author (also shown as red "Editor's note" in the PDF where relevant)
1. Step 1 of the algorithm (Gram-matrix kernel) comes from the notation file; the research ledger assumes a candidate annihilator P is given. Confirm it is the intended Step 1.
2. Symbols M, d, L in Proposition 6.2 (complexity) are not defined; supply definitions.
3. Fisher-KPP is in the abstract and the benchmark list, but no statement about it appears in the body (ledger S4T-P5). Add a statement or remove from the abstract.
4. Overloaded symbols (S, D, J, sigma, c) are documented in Table 2's caption but not renamed; renaming would touch many formulas, so left to the author.
5. The "Ehrenpreis-Palamodov" glossary entry is context only (not used in the body); "Stein" is cited in Thm 5.5 but has no bibliography entry.
6. In Theorem 4.1 only the easy direction is proved in the text; the converse is deferred to the project's proof package.
7. The Gaussian example of Figure 6 and the Lagrange projector formula (5.x) were derived by me in v1, consistent with the ledger (P1-T2, II-T2) but not literally in it; please check.
8. Examples suggested but not added: a short worked example for the exact sequence of the dictionary criterion (Thm 7.3), and a small example of a nonzero point spectrum with several factors.

---
# Round 3 (v3)
- Density: Figure 6 caption shortened, its interpretation moved into a "A concrete case" paragraph with displayed formulas; editor notes moved out of the text flow into Appendix D (red superscripts E1-E7 in the text); Sec. 4.3 bullets became Table 3; the "after the shock" results are three displayed lines with sources below; the algorithm steps use Does / How / Returns blocks; the worked example is a sequence of boxes (goal, computation, outcome) with the derivative of f and g shown; Friedrichs figure annotations moved into text; the steps table no longer floats; appendices start on a new page; wide displays fixed.
- Added (nothing replaced): a section brief "Starting from / Why this section / Role in the paper" at the start of every section; Appendix B (primer with integer, ODE and numerical examples of ideals, annihilators, exponential-polynomials, Chinese remainder theorem, companion matrix) with pointers from Sec. 2 and Sec. 5; Appendix C (scope of the paper versus the research); Appendix D (notes for the author).
- Accuracy fix: Table 3 now states that the "no finite certificate" result for general (non-jet) data on convex sets is cited from Malgrange, as in the ledger, not proved.
- Compiled: yes, 29 pages, no errors, no undefined references; 2 overfull lines of 2.6 and 5.6 pt remain. Inspected at page level: contact sheets of all pages plus close views of pages 3, 18, 25, 28.
