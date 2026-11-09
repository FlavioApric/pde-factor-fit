# KA OPR2-T3 — Thread 2 (arbitrato), subagente Claude fresco a6962e58a6f6d6feb, 26/10/2026
Input: KA_OPR2_T3_input.md + KA_OPR2_T3_attack.md (solo quelli). Controlli a mano.
| punto | contenuto | verdetto | severità | fix |
|---|---|---|---|---|
| R1 | esempio della Lettura "(∂_t − a)² con ∂_t centrale è uniseriale" falso per a = x: (∂_t − x)² = (∂_t − x + e_c)(∂_t − x − e_c), e_c = (∂_x + c)^{-1}, e_c² = [x, e_c]; socle S ⊕ S, infiniti atomi | **still_unresolved** | minor (solo Lettura) | "(∂_t − a)² con a ∈ ℂ, 𝔇 = 𝒟"; aggiungere (∂_t − x)² come esempio d'avvertimento |
| R2 | parentetica della Tesi "D_i è, a meno di un fattore sinistro in K, un divisore destro di P" falsa se deg A_i ≥ 2 (testimone: P = ∂_t² − x irriducibile in 𝔎, D = ∂_t ammesso ma non divisore destro) | **still_unresolved** | minor (formulazione) | "D_i si può scegliere = b_iQ_i (P = A_iQ_i, A_i irriducibile, b_i ∈ 𝔄 denominatore sinistro); va bene qualunque D_i con classe in S_i∖0" |
| R3 | (∂_t − x)² riproduce l'ostruzione OP-ALG-C1 | come R1 | — | — |
| R4 | nucleo della prova ed Esempio (i) corretti | answered | — | — |
Difetti aggiuntivi: D1 (cosmetico) "D_i ∈ KS_i ∩ 𝔄^m" → "la classe di D_i sta in S_i ∩ 𝔄^m"; D2 definire "saturato" (M/N senza 𝔄-torsione) in L3(b); D3 numeri della fonte per l'estensione di δ a K non verificati.
Il criterio Ann = 𝔇P ⟺ D_iu ∉ 𝒯 (i ≤ r) **sopravvive** (L3(b),(c), finitezza r ≤ ℓ ≤ m, (⇒) da T4, (⇐) via atomo in L_u; P3′ corretto).
## Verdetto (calcolato da S-CHECK-16 con la tabella della skill): **WARN** (2 still_unresolved, entrambi minor; reason_code unresolved_major_or_minor) → fix T3-1, T3-2 obbligatori.
