# PLAN — OP-F5D · rimozione dei CONDIZIONALI residui (26/10/2026)
Skill: skills-local/session-protocol, skills-local/claim-lifecycle (proof-writer → SymPy → CHECK_REQUEST per revisore indipendente; nessuno script _vendor eseguito).
Input letti: REPORT_FINALE §4, §6.2; claims/LEDGER.md (righe CONDIZIONALE); research/CIT-AUDIT/AUDIT-F5.md; work/S4-INTEG, S4-ID, OP-NL, OP-R2, S4-TERM.

## Bersagli e strategia
1. (Lax) per ogni n [OP-P17, M ≥ 4]: prova propria via serie formale F(ζ) (integrale primo ½FF″ − ¼F′² + (v+ζ)F² = ζ) e operatori B_n = (−1)^n Σ_j (f_j∂ − ½f_j′)L^{n−j}; identificazione con K_n = 𝓡^nK_0.
2. INT-T1(C) direzione inversa (uguaglianza dell'ambiguità) per v ∈ 𝒮: lemma del centralizzatore 𝒵 = span{B_n, 𝓛^m}; caso Λ infinito banale; caso r ≡ 0: soluzioni di Jost continue/C¹ in k fino a 0, a continua con |a| = 1, zeri semplici e finiti, incollamento ⇒ operatore A che intreccia L e −∂², P = A∂A^T commuta con L ⇒ relazione di Novikov. Invarianza di Λ nel tempo dalla coppia di Lax (F1 dimostrato per i flussi K_c).
3. INT-T1(B) senza F-MS: identità Wronskiano = f di Hirota (Cauchy/Vandermonde), divisione di Crum, autofunzioni esplicite.
4. INT-T2: (ZC) per ogni n (serie W(ζ), A²+BC = 1, riduzione r = −q̄); Jost di ZS con Volterra. Uguaglianza dell'ambiguità: declassare/limitare.
5. S4ID-P8, OPR2-P7: (H-as)/(SR) con derivate ridotte a Grunert–Teschl (letto) + limiti uniformi nel tempo di ‖∂^m u‖ (leggi di conservazione di Gardner, prova propria) + interpolazione.
6. S4T-T3(iv) senza Kuznetsov: stima O(√ν) diretta dalla formula di Cole–Hopf (misura di Gibbs, convessità in x).
7. [F1]: la funzione di Lax–Oleinik è soluzione entropica di Kružkov (limite di viscosità evanescente via Cole–Hopf + Laplace); resta solo l'unicità di Kružkov, presupposta dalla definizione di S_B.
## Fonti
Grunert–Teschl arXiv:0807.5041 (Thm 4.4/Cor 4.5, Thm 5.4), eventualmente Kružkov 1970 (mathnet.ru). Registro in FONTI.md.
## Fatto quando
PROOF_PACKAGE.md con ID OPF5D-*, SymPy in sympy/ (esiti), FONTI.md, CHECK_REQUEST.md, DONE in inbox/central.md.
