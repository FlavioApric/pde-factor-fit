# KA OPF-T4 — Thread 2 (arbitrato, subagente Claude fresco a804939cd10dfce86, 26/10/2026)
Input: KA_OPFUN_T4_input.md + KA_OPFUN_T4_attack.md (nient'altro). Testo dell'arbitro, riportato per punti (fedele).

- **P1 — la costruzione esplicita di (iii) copre solo tensori decomponibili.** partially_answered, minor. Lettura corretta; ma la costruzione è lineare: per ξ = Σ_k[θ_k]⊗n_k ∈ ker ι si pone Φ_j := Σ_kφ_k n_{k,j}, Q_j(∂)Φ_j monodroma termine a termine, ι(ξ)=0 ⇒ Q_j(∂)Φ_j = Q_j(∂)α_j, h_j := Φ_j − α_j, Σ_jh_j = −Σ_jα_j (Σ_j n_{k,j} = 0 per ogni k); le differenze di Čech del sollevamento sono Σ_k c^k_{ab} n_k = cociclo di ξ. Equivalente: θ forma chiusa a valori in 𝒩. Fix: riscrivere (iii) per ξ generale.
- **P2 — ker ι non è generato da tensori puri in ker ι.** partially_answered, minor. Vero e irrilevante: la costruzione lavora sulla somma intera.
- **P3 — "non nulla se [θ]≠0 e (w_j)≠0" solo per tensori puri.** partially_answered, minor. Fix: "∂u = ξ, non nulla se ξ ≠ 0; u ∉ im Σ_Ω per esattezza".
- **P4 — (ii) non identifica la preimmagine astratta con l'u esplicito.** partially_answered, minor. Identificazione scritta nel caso puro; caso generale = estensione lineare di P1 (tre righe).
- **P5 — (iv)(e) vale solo perché δ(τξ)=1.** answered_by_current_text. Con 𝒩 di dimensione 1 ogni tensore è puro; (a)–(c) usano solo (ii) e H¹(𝒦_j) ≅ 𝒜/Q_j𝒜.
- **P6 — l'Esito sovra-afferma ("chiuso", "esplicito").** answered_by_current_text. Il criterio e il limite dimensionale poggiano su (i)–(ii), completi; "esplicito" non compare nell'Esito.

**Summary:** answered 2, partially 4 (tutti minor), still_unresolved 0; critical 0, major 0.
**Net assessment (arbitro):** il teorema sopravvive intatto; la correzione è qualche riga di esposizione in (iii).
**Top action items:** (1) (iii) per ξ = Σ_k[θ_k]⊗n_k con primitiva 𝒩-valente; (2) "∂u = ξ ≠ 0 ⇒ u ∉ im Σ_Ω"; (3) una frase che dica che (i), (ii) e i corollari (a)–(e) non usano la parte "u esplicito" di (iii).

**Verdetto (calcolato da S-CHECK-14 con la tabella della skill):** 0 still_unresolved, partially solo minor ⇒ **PASS** (`defense_survives_with_minor_partial_only`).
