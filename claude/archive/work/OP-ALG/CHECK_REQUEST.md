# CHECK_REQUEST — OP-ALG (audit proof-checker + kill-argument consigliato su T1 e T3)
Data 26/10/2026. Revisore: subagente Claude indipendente, senza il contesto di OP-ALG. Testo da auditare: **work/OP-ALG/PROOF_PACKAGE.md §§1–5** (prove complete lì; questo file elenca enunciati, ipotesi, dipendenze esterne e punti delicati, in modo che l'audit non richieda altri file oltre a quello). SymPy di controllo: work/OP-ALG/sympy/op_alg_checks.py → .out (40/40 OK; controllo, non prova).

## Convenzioni minime
R = ℂ[τ,ξ], Q(∂) = Q(∂_t,∂_x); Ω ⊂ ℝ² aperto connesso; EP(Ω) = restrizioni di somme finite Σq_k(t,x)e^{τ_kt+ξ_kx}; Ann(u) = {Q ∈ R : Q(∂)u = 0}; G_u = gcd Ann(u), Ann(u) = G_u·J_u con V(J_u) finito. A_2(K) algebra di Weyl su K = ℚ̄, filtrazione di Bernstein; A_2/I olonomo ⟺ dim F_k(A_2/I) = O(k²). (AC): aritmetica esatta in ℚ̄, radici in ℚ̄ di polinomi univariati, test "∈ ℤ_{≥0}".

## Fatti importati (già DIMOSTRATI nel progetto; enunciati qui per l'audit)
- **C3-L3.** (b) Σq_ke^{⟨z_k,·⟩} = 0 su un aperto non vuoto, z_k distinti, q_k polinomi ⇒ q_k = 0. (c) per w EP, V(Ann w) = insieme degli esponenti. (e) w ∈ EP(Ω) ⟺ dim R·w < ∞ ⟺ V(Ann w) finito.
- **C3-T1.** P(∂)u = 0, P = c∏P_i^{e_i}: (a) Ann(u) = (P) ⟺ (P/P_i)(∂)u ∉ EP ∀i; (b) V(Ann u) = V(P) ⟺ (P/P_i^{e_i})(∂)u ∉ EP ∀i; (e) Ann(u) = (P) ⟺ G_u ∼ P. **C3-T6.** G_u ∼ ∏P_i^{f_i}, f_i = e_i − max{k : (P/P_i^k)(∂)u ∈ EP}. **C3-T3(ii).** w EP ≠ 0 ⇒ Ann(w) generato in grado ≤ dim R·w. **C3-C2.** u EP, P non costante ⇒ Ann(u) ≠ (P).
- **P4-T2(iii),(v)(a).** R·u ∩ EP = R·G_u(∂)u ≅ R/J_u, J_u = Ann(G_u(∂)u); Ann(u) principale ⟺ R·u ∩ EP = 0.
- **P4-T4.** Modello M2⁺ (oracolo dei getti in p₀ + oracolo di zero per Q(∂)u): (i) Ann(u) ∩ 𝓛 calcolabile per 𝓛 di dimensione finita; (ii) "Ann(u) ≠ (P)" semi-decidibile (si cerca n con dim(Ann∩R_{≤n}) > dim((P)∩R_{≤n})); (iii) dato B ≥ dim(R·u∩EP), "Ann(u) = (P)" decidibile e G_u calcolabile.
- **P4-T5 (Passi 2–3).** Se Ann(ũ) = (P̃), getti in K, p₀ ∈ K²: per ogni k₀ esiste v₁, combinazione K-lineare di funzioni EP in ker P̃ con esponenti in K², con lo stesso k₀-getto di ũ; per ogni Q ∉ (P̃) esiste e_Q dello stesso tipo con k₀-getto nullo e Q(∂)e_Q ≠ 0.
- **P4-L7.** Per ogni P̃ ∈ K[τ,ξ] non costante esiste ũ reale-analitica su (−ε,ε)², getti in 0 in K, Ann(ũ) = (P̃).
- **P4-L4.** Λ ∈ ℂ[x]⟨∂_x⟩∖0, h analitica vicino a x₀ con Λh = 0: se h^{(k)}(x₀) = 0 per k ≤ K₀(Λ,x₀) (massima radice intera ≥ 0 dell'indiciale in x₀), allora h ≡ 0 vicino a x₀.
- Fatti di algebra non commutativa (CON-FONTE generico, Goodearl–Warfield cap. 6): un dominio noetheriano è di Ore; rango additivo; torsione = sottomodulo; modulo senza torsione non nullo ha rango ≥ 1.

## Claim da auditare (ordine di priorità)
1. **OP-ALG-T1** (§2): nel modello M3-hol (u reale-analitica su Ω connesso, I ⊆ Ann_{A_2}(u) olonomo con generatori in A_2(K), getti in p₀ ∈ Ω∩K² calcolabili in un campo computabile 𝕂, P ∈ K[τ,ξ] fattorizzato) sono decidibili il test di zero e il test EP, quindi "Ann(u) = (P)", "V(Ann u) = V(P)"; calcolabili G_u, Ann∩𝓛, generatori, B. Catena: L1 (eliminanti per conteggio) → L2 (indiciale a parametro) + L3 (restrizione) + P4-L4 → P1 (test di zero) ; L4 (confinamento EP) → P2 (EP ⟺ a*(∂_t)w = b*(∂_x)w = 0) → T1. **Punti delicati:** L1(b) terminazione della ricerca; L2 quando t₀ è singolare; L4 il conteggio del monomio t^{D+ν} e la definizione di δ_τ; T1(v) uso di C3-T3(ii).
2. **OP-ALG-T3** (§3): ordine dei dati D2; χ ≡ 𝔇; 𝔅 ≡ 𝔊; per P irriducibile ridotto 𝔅 ≡ χ; per Σe_i ≥ 2, 𝔅 ≰ χ (avversario: u = ũ + e con Ann(ũ) = (P/P_1); u′ = v₁ + Σλ_Qe_Q + Σc_ze^{⟨z,·⟩} + e). **Punti delicati:** Ann(u) ⊆ (P̃); stesse risposte di zero; conteggio dim R·u′ ≥ |supp S_F| > B.
3. **OP-ALG-T4, L5, P5** (§4): criterio saturato per P monico in ∂_t in 𝔇 ∈ {ℂ[x]⟨∂_x⟩[∂_t], A_2}; stabilità di 𝒯_𝔄 per ∂_t; u olonoma non identifica in A_2.
4. **OP-ALG-C1 + Lemma NT** (§4): P = (∂_t − x∂_x)(∂_t − x∂_x + 1); u^{(λ)} = (1+λ∂_x)u_2, u_2 = e^{−t}exp(x²e^{2t}); Q_λ = P_2 + λ∂_xP_1; L_λ ∩ L_μ = 𝔇P; nessun test finito; u* identifica. **Punti delicati:** Lemma NT (passaggio da Φ(t,x,e^t) ≡ 0 a Φ ≡ 0 e indipendenza delle gaussiane); saturazione e argomento di rango.
5. **INT-18** (§5): verifica che con P(∂)u = 0 la condizione σ_p = ∅ di P4-T2 è ridondante e testo proposto.
Esito richiesto: per ciascun claim PASS / PASS-con-fix / FAIL con id dei rilievi; kill-argument su T1 e T3 (cammino critico di G★′ punto 1).
