<!-- Proposta S5-FIX (26/10/2026): testo di work/S5-INT/INTEGRAZIONE_LINEARE.md §2.3, pronto da appendere in fondo a NOTAZIONE.md dal coordinatore. Modifiche rispetto alla fonte: tolto il blocco di codice; aggiunta la riga di intestazione alla tabella E_int perché sia una tabella Markdown valida. Contenuto invariato. -->

## Versione 4 (proposta S5-INT, 26/10/2026) — integrazione del pacchetto lineare; nulla di v1–v3 è rimosso
### Domini (sostituisce, per i risultati di Fase 3, la frase di v2 H1 "Ω = I×(a,b) oppure convesso")
- Ω_c: aperto connesso non vuoto di ℝ² — identificazione (C3-T1, C3-T6, P4-T2, P4-T4..T6).
- Ω_sc: Ω_c con H¹_dR(Ω) = 0 (⟺ semplicemente connesso, Rudin RCA cap. 13 per "⇐") — scomposizione per fattori (C12-T1′, C12-P10, P4-P1, R2-T3 esteso).
- Ω_R: rettangolo limitato I×J — classe 𝔅 e strato "termini" (P1, P2-T2 "⇐", P2-P5(a)).
- Ω_conv: convesso limitato — C12-T3, P2-C1, C3-P1[gen] (qui la convessità è necessaria).
- "limitato" serve solo per EP ⊂ H^m(Ω) e per gli enunciati in H^m (C12-P7: limitato, lipschitziano, connesso).
### Oggetti
- EP(Ω) := restrizioni a Ω delle somme finite Σ_k q_k(y)e^{⟨z_k,y⟩}, q_k ∈ ℂ[t,x], z_k = (τ_k,ξ_k) ∈ ℂ², ⟨z,y⟩ = τt + ξx. Esponenti sempre come z_k (non σ_k, ρ_k, ζ_k).
- P = c∏_{j=1}^s P_j^{e_j} (P_j irriducibili su ℂ, non associati); componente Q_j := P_j^{e_j}; s = numero di fattori; N = numero di termini; k = deg_τP.
- Ann(u) = G_u·J_u (G_u = gcd, V(J_u) finito); M_u := R·u ≅ R/Ann(u).
- "u identifica P" ⟺ Ann(u) = (P). "u identifica in 𝓛" ⟺ dim(Ann(u) ∩ 𝓛) = 1.
- 𝔅_ρ(Ω_R), B_ρ(J): P1-D1.
- Mappa somma Σ: ⊕_jℋ_j → H, γ(ℋ_1,…,ℋ_s) := inf σ(Σ*Σ|_{(ker Σ)^⊥}) (+∞ se (ker Σ)^⊥ = 0); per i nuclei in H^m il prodotto scalare è ⟨u,v⟩ = Σ_{|α|≤m}⟨∂^αu,∂^αv⟩_{L²}; il valore di γ dipende da esso e dal raggruppamento dei fattori, la condizione γ > 0 no.
- c_F(ℋ_1,ℋ_2) := coseno di Friedrichs (sup |⟨a,b⟩| su a ∈ ℋ_1⊖𝓘, b ∈ ℋ_2⊖𝓘 unitari, 𝓘 = ℋ_1∩ℋ_2); c₀ := ‖Π_{ℋ_1}Π_{ℋ_2}‖ (Dixmier; = c_F se 𝓘 = 0). Per s = 2: γ = 1 − c_F (P2-T3).
- Proiettori ortogonali: Π_ℋ (mai P_i, riservato ai fattori).
- Modelli di dato: M1 (formula EP), M2 (jet in un punto), M2⁺ (jet + test di zero, P4 §6), M3 (u ∈ H^m(Ω) esatta); "dati modali finiti": u₀ ∈ span{e_n : n ≤ N} (P3-T3).
### E_int: tabella unica (quadro → definizione → dove)
| simbolo | definizione | quadro | dove |
|---|---|---|---|
| E^add | u − u₀ − Σ_n(S_n(t)u₀ − u₀) | 𝔅 (lineare), A9 (non lineare) | P1-D3(b), v3 |
| E^{add,form} | stessa, in getti formali in t | ogni u liscia | P1-D3(a) |
| E^mult | S(t) − S_1(t)⋯S_N(t) (dipende dall'ordine) | 𝔅, A9 | P1-D3(c), v3 |
| 𝔈^mult | (S_1⋯S_N)^{-1}S | 𝔅 | P1-D3(c) (sostituisce la scrittura di v2) |
| E^{add,(1)}, E^{mult,(1)} | coefficienti di ε¹ (ordine: prima S₀, poi il flusso di V; con Dirichlet, flusso di inflow) | semigruppi perturbati | P3-P1, P3-T3 |
| E^log | ∂_t log(densità spettrale) − Σ a_n ≡ 0 | misure a supporto compatto | P1-D3(d) |
| E^fatt_X | ker_X P / im Σ_X (fattori, non termini) | X ∈ {D′, C^∞, H^m, 𝔅} | P1-D2 |
| E^ker | ker L/(ker L ∩ Σ ker L_n) (termini) | D′, C^∞ | v2, R2-T3 |
| E^⊥, E^∥ | fuori dallo span / ambiguità nello span | regolarizzazione | v2, P2 |
| E_B, E^trop, E^NL, E^mix | strumenti di regime / Fase 4 | ℝ / non lineare | TROP, v3 |
### Stati
Aggiungere PROVA SCRITTA (prova completa, non auditata), che sostituisce "APERTO-con-prova", "PC-attesa", "DIMOSTRATO (bozza)"; "PARZIALE" solo per problemi aperti con risultati parziali (es. C3-Q1), non come stato di un claim.
