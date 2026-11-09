# LEDGER_ROWS — S10-COL (27/10/2026)

Righe proposte per `claims/LEDGER.md`. Le scrive solo il coordinatore. Nessuno stato supera PROVA SCRITTA, perché l'audit (proof-checker e kill-argument) è ancora da fare. Prova: `work/S10-COL/PROOF_PACKAGE.md`. Controlli: `work/S10-COL/sympy/`.

| ID | enunciato (1 riga) | ipotesi | stato | prova (file#sezione) | SymPy (script, esito) | proof-checker | kill-argument | dipende da |
|---|---|---|---|---|---|---|---|---|
| **Fase 10 — S10-COL (27/10/2026)** | | | | | | | | |
| S10COL-L1 | il cono D(p) delle direzioni entranti (quantitative) in p ∈ ∂Ω è un cono convesso aperto | Ω ⊂ ℝⁿ aperto | **PROVA SCRITTA** | §1 | s10col_sym (S4) OK | richiesto | — | — |
| S10COL-L2 | in ogni carta lipschitziana (C,R,g,L): Γ = {z_n > L\|z′\|} ⊂ D(p) per ogni p ∈ ∂Ω ∩ C | carta lipschitziana | **PROVA SCRITTA** | §1 | s10col_sym (S2) OK | richiesto | — | (F1), (F2) |
| S10COL-L3 | W ∈ C¹_c, W(p) ∈ D(p) ⇒ dist(ψ_t x, ∁Ω) ≥ a t per x ∈ Ω̄ vicino a p, 0 < t ≤ ρ_p | — | **PROVA SCRITTA** | §1 | — | richiesto | — | S10COL-L1 (def.) |
| S10COL-TA | campo di carta W = Σθ_i e_i (θ_i ≥ 0 in C_c^∞(C_i), Σθ_i > 0 su ∂Ω): W(p) ∈ D(p) ∀p ∈ ∂Ω, senza condizioni di compatibilità tra carte | Ω limitato lipschitziano | **PROVA SCRITTA** | §2 | s10col_flow (1)–(4) OK | richiesto | richiesto | S10COL-L1, S10COL-L2 |
| S10COL-TB | V ∈ C¹_c con V·ν ≥ κ > 0 q.o. su ∂Ω ⇒ −V(p) ∈ D(p) ∀p ∈ ∂Ω | Ω limitato lipschitziano | **PROVA SCRITTA** | §3 | s10col_sym (S1),(S3) OK; s10col_flow (5) OK | richiesto | — | Rademacher, Fubini, (F1), (F2) |
| S10COL-TC = [COL-ii] | W = −V con W(p) ∈ D(p) ∀p ∈ ∂Ω ⇒ (a) dist(Φ_{−σ}(Ω̄), ∂Ω) ≥ cσ per 0 < σ ≤ σ₀; (b) Ω̄ ⊂ Φ_σ(Ω) ∀σ > 0; (c) Φ_σ(Ω) ⊂ {dist(·,Ω̄) ≤ Mσ}, Φ_σ(Ω) ≅ Ω | Ω ⊂ ℝⁿ aperto limitato, V ∈ C¹_c | **PROVA SCRITTA** (con S10COL-TA oppure S10COL-TB) | §4 | s10col_flow (4),(5) OK: 9464 punti, 0 violazioni; (6) controllo negativo OK | richiesto | richiesto | S10COL-L3, compattezza di ∂Ω |
| [COL] (fonte di S10A-T3) | (COL-i) campo trasversale; (COL-ii) Ω̄ ⊂ Φ_σ(Ω) ⊂ {dist < Cσ} | Ω limitato lipschitziano | (COL-i): **CON-FONTE** (Grisvard Lemma 1.5.1.9; HMT 2007 Cor. 2.13), invariato. (COL-ii): **PROVA SCRITTA** (S10COL-TC, sia per il campo di carta sia per ogni V di (COL-i)). Per S10A-T3 (COL-i) non serve più (S10COL-TA) | §2–§4 | s10col_flow, s10col_sym | richiesto | — | S10COL-TA, S10COL-TB, S10COL-TC |
| S10A-T3 (proposta) | come in `work/S10-OPEN-A` §3 | come lì, con θ_i ≥ 0 esplicito nel Passo 1′ | **PROVA SCRITTA mod F1, F2**, senza [COL], **dopo** l'audit di S10-COL e la sostituzione del Passo B (PROOF_PACKAGE §5). Fino ad allora resta APERTO — ridotto a [COL-ii] (A-7) | `work/S10-OPEN-A` §3 + `work/S10-COL` §5 | — | richiesto (Passo B nuovo) | — | OPF5B-T1 Passi 3–7, OPF-T4(ii), F1, F2, S10COL-TA, S10COL-TC |
