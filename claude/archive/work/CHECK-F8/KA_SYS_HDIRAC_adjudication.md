# KA H-DIRAC — aggiudicazione (S-CHECK-F8-SYS, 27/10/2026)

Attacco: `KA_SYS_HDIRAC_attack.md`, scritto da un subagente indipendente che ha letto solo `KA_SYS_HDIRAC_input.md`. Esito dichiarato: **WOUNDED (lieve)**.
Verifica dell'aggiudicatore: prove rifatte a mano; eliminazione unimodulare ricontrollata in `sympy/sys_check_f8.py` (HD1–HD3, OK).

## Punti dell'attacco

**P1 — H-DIRAC-2(d) falso su Ω non connesso (attacco principale, proposto MAJOR).**
*Accusa.* Né l'enunciato né la prova di H-DIRAC-2 dichiarano Ω connesso. Con Ω = B_1 ⊔ B_2, ψ_2 = e^{λ·x} su B_1 e 0 su B_2 (KG(λ) = m²), ψ_2 non è EP ma Ann(ψ_2) ⊇ m_λ ⊋ q, quindi ψ non identifica D_2.
*Verifica.* Il controesempio è corretto. La notazione del pacchetto (riga 10) dice solo "Ω ⊂ ℝ^n è un aperto"; SYS-C1, SYS-EX e C3-L3 chiedono Ω connesso, ma il §7 non lo ripete.
*Verdetto: still_unresolved nel testo, riparazione banale.* Severità: per la tassonomia è INVALID + LOCAL. Considerato che il pacchetto lavora ovunque con Ω connesso e che l'ipotesi manca solo nel §7, la classifico **MINOR con obbligo di fix** (fix **SYS-9(a)**: "Ω aperto connesso non vuoto" nelle ipotesi di H-DIRAC-2; oppure "EP su ogni componente connessa" in (d)).

**P2 — Prova di (b) su Ω sconnesso.** Assorbito da SYS-9(a).

**P3 — H-DIRAC-1 (attacco fallito).** Concordo: la componente di grado d + 1 di W L_0 è W_d(τI + α_0·ξ), e det(τI + α_0·ξ) è monico di grado 4 in τ (HD3), quindi W_d = 0. Non servono ipotesi su m, su B, sull'hermitianità o su Clifford. H-DIRAC-1 vale per ogni L_0 ∈ 𝒞.

**P4 — Eliminazione in (a) (attacco fallito).** Concordo: E D F = diag(−mI, (KG − m²)/m · I) con E, F unimodulari (HD1), e le classi di e_3, e_4 sono una base (HD2). Non si perde nessuna relazione.

**P5 — Primalità di KG − m² e colunghezza finita in (d) (attacchi falliti).** Concordo.

**P6 — SYS-C1: manca l'inclusione "fattori primi di det P ⊆ Ass" (MINOR).** Accolto: fix **SYS-3**. Non tocca H-DIRAC, dove Ass è calcolato direttamente.

**P7 — Riferimento Weibel (MINOR).** Accolto (CIT-AUDIT-8).

**P8 — Fattore −i tra γ^0 D e la classe 𝒞 (MINOR).** Accolto: con p_μ = i∂_μ il coefficiente di ∂_t in γ^0 D è iI. Un'unità costante non cambia U_D, ma il testo deve dirlo e fissare la convenzione p ↔ ζ. Fix **SYS-9(b)**.

**P9 — (c) "test" è una riformulazione dell'iniettività (MINOR).** Accolto: nella "Risposta" va scritto "criterio" e non "test", e va detto che non è certificabile da dati finiti (come C3-P1). Fix **SYS-9(c)**.

## Riepilogo
Punti: 9. still_unresolved: 1 (P1, fix banale); accolti MINOR: 4; non riusciti: 4.

## Verdetto
**SURVIVES** dopo il fix SYS-9 (ipotesi Ω connesso, fattore −i, "criterio" invece di "test"). H-DIRAC-1 sopravvive integralmente. La risposta all'utente ("α^k e βm si leggono esattamente da una ψ identificante, che esiste sempre") è confermata, e vale per **ogni** L_0 ∈ 𝒞: det L_0 è monico in τ, quindi SYS-C1 si applica sempre (osservazione da aggiungere).
