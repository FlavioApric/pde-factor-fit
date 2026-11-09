# KA OPF5D-T4 — aggiudicazione (S-CHECK-17, 26/10/2026)
Input: KA_OPF5D_T4_input.md. Attacco: KA_OPF5D_T4_attack.md (subagente fresco). Aggiudicatore: S-CHECK-17, con un ricontrollo indipendente a mano (poli di mσ_3m^{−1}, identificazione β_n ↔ d̃_n, L12 con M = 0).

**Esito: SOPRAVVISSUTO** (nessuna obiezione FATALE o MAJOR).

| punto dell'attacco | verdetto | riparazione |
|---|---|---|
| L10: «ρ continuo su ℝ» è falso se a ha zeri reali. Controesempio: q = ½ sech x; per ζ = 0 si ha rotazione di π/2, quindi a(0) = 0 e \|b(0)\| = 1 | **fondato, MINOR** (= F5D-6) | Ho verificato il controesempio. Nella definizione di Λ_m, nel caso (⇒) ρ ≢ 0 di T4 e in L10, sostituire ρ con b (continuo). Aggiungere «ρ ≡ 0 ⟺ b ≡ 0, perché uno zero reale di a forza \|b\| = 1». La logica della prova non cambia: b(ξ)Ω̃_d(ξ) = 0 e b ≢ 0 continuo implicano Ω̃_d ≡ 0. |
| T4, ultima frase (INT-T2 dinamico): dipende da L9 per ZS (non scritto) e da (UC) | **fondato, MINOR** (= F5D-7) | T4 a tempo fissato è completo. La versione INT-T2 va enunciata «mod L9-ZS (prova da scrivere, analoga a L9) e (UC)». |
| L10, «dimensione 1»: argomento abbozzato | MINOR presentazione (= F5D-8) | Due soluzioni L²(+∞) avrebbero Wronskiano costante ≠ 0 e tendente a 0: contraddizione. Una riga. |

Ho controllato in modo indipendente i punti seguenti.
- mσ_3m^{−1} = m_1⊗m_2^⊥ + m_2⊗m_1^⊥ (det m = 1) è lineare in m_1. Il polo in ζ_j ha quindi ordine ≤ m_j e coefficiente d'ordine −m_j pari a 2λw⊗w^⊥ ≠ 0, anche per m_j ≥ 2.
- Ṽ_0 = −(i/2)σ_3 e T̃_0 = −iq = −T_0: R1 è necessario. Con il vecchio Ω_d gli zeri del 1-solitone sarebbero reali, e il controllo di burgers_l1 (B_3 + η²B_1 = 0) lo conferma con Ω̃ ∝ ζ² + η².
- Il limite x → +∞ per ζ reale passa per m_+ → I e per il coniugio con una matrice diagonale unitaria.
- In L12 con M = 0 si usa la parte diagonale di un difetto fuori diagonale.

**Stato dopo l'aggiudicazione:** L10 è OK con fix MINOR; L11 e L12 sono OK; T4 è OK con fix MINOR. Il kill-argument è sopravvissuto. Stato proposto: **DIMOSTRATO** a tempo fissato. INT-T2 dinamico resta mod L9-ZS e (UC).
