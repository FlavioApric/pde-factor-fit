# KA OPR2-T1 — Thread 2 (arbitrato), subagente Claude fresco a6721c94793e77916, 26/10/2026
Input: KA_OPR2_T1_input.md + KA_OPR2_T1_attack.md (solo quelli). Controlli propri (scratchpad scheck16_adj_a.py): commutatore A1 residuo 0; spostamento di s residuo 0; sup_ξ(1−e^{−Lξ²})/|ξ| ≈ 0.64√L, sup(1−e^{−Lξ²})/ξ² = L (L = 0.1, 1, 5, 50).
| punto | contenuto | verdetto | severità | fix |
|---|---|---|---|---|
| AP1 | identità esatta di v − u nel Passo 7, controllo uniforme in ε | answered_by_current_text | — | — |
| AP2 | commutatore, Hũ_1 = 0 (χ̃ = 1 e Eg_j = g_j su Ω) | answered | — | — |
| AP3 | supporti e ordine r → δ → K → ε₀; g_j ∈ H^m | answered (formulazione) | minor | scrivere δ < (b−a+cT)/2 (χ_1, χ_2 a supporti disgiunti) e un intorno aperto di supp∇θ_i |
| AP4 | OPR2-L0 (norme L¹, ∂_t e Duhamel) | answered | — | — |
| AP5 | riduzioni c ≤ 0, c = 0 via OPF-T5(b), paragrafo Estensione | answered (Estensione solo abbozzata) | — | — |
| AP6 | catena ⟺ della Tesi: γ_2, c_F non definiti nel testo | partially_answered | minor | definire/rinviare c_F, γ_2 (C12-P7(b)) |
| AP7 | CON-FONTE (Hörmander, Stein); "le altre disuguaglianze" del Passo 3(a) implicite | partially_answered | minor | scrivere 3r + ε₀ < min(T, b−a); per il rettangolo estensione per riflessione d'ordine m (evita Stein) |
Difetti aggiuntivi (tutti minor): D1 Passo 2 "B ∈ C^∞(N)" → C^∞(N̄); D2 K := [a−cT+δ/2, b−δ/2] esplicito (Ω_K usa int K); D3 Passo 1 una frase in più sulle fette; D4 Estensione: "PROVA SCRITTA" → abbozzo.
Net assessment (arbitro): nessun difetto matematico, nessun critical/major; restano presentazione e fonti. Conteggi: answered 5, partially 2 (minor), still_unresolved 0.
## Verdetto (calcolato da S-CHECK-16 con la tabella della skill): **PASS** (nessun still_unresolved; i partially sono minor → fix T1-1..T1-4 nell'audit).
