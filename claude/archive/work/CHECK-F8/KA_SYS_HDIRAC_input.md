# KA input H-DIRAC — preparato da S-CHECK-F8-SYS (27/10/2026). Testo estratto VERBATIM da work/S8-SYS/PROOF_PACKAGE.md (righe 10, 15–17, 90–92, 216–234): notazione, lemmi usati, enunciati H-DIRAC-1/2, ipotesi e prove. Compito del revisore: kill-argument (trovare un controesempio o un passo falso).

Fatti esterni citati: SYS-EX (criterio d'esistenza: esiste u identificante ⟺ dim_ℂ Hom_R(R/m, M_P) ≤ 1 per ogni m massimale, su Ω aperto connesso); C3-L3 (progetto: su Ω connesso, le soluzioni di un ideale di colunghezza finita sono esponenziali-polinomi). Le verifiche SymPy C1–C7 sono identità polinomiali (XY = YX = KG·I_2, YX − m² = (KG − m²)I, det D = (KG − m²)², irriducibilità di KG − m²).

**Notazione.** R = ℂ[ζ_1, …, ζ_n], con ζ_j ↔ ∂_j (per i sistemi di evoluzione ζ = (τ, ξ) ↔ (∂_t, ∂_x)). Ω ⊂ ℝ^n è un aperto, 𝒜 ∈ {C^∞(Ω), 𝒟′(Ω)}. Le righe agiscono a sinistra: P ∈ R^{l×k} agisce su u ∈ 𝒜^k. U_P := R^{1×l}P ⊆ R^{1×k} è il modulo delle righe e M_P := R^{1×k}/U_P. Sol_𝒜(P) ≅ Hom_R(M_P, 𝒜). Per u ∈ 𝒜^k: Ann(u) := {r ∈ R^{1×k} : r(∂)u = 0}, M_u := R^{1×k}/Ann(u), e φ_u : M_P → 𝒜, [r] ↦ r(∂)u, che è ben definita se u ∈ Sol(P). Ann(u)/U_P = ker φ_u. "u identifica P" significa Ann(u) = U_P, cioè φ_u iniettiva. Per un ideale massimale m: soc_m(M) := Hom_R(R/m, M) = {x ∈ M : m x = 0}; m_λ := (ζ_1 − λ_1, …, ζ_n − λ_n). EP indica gli esponenziali-polinomi. Modello di dato: DM3 (u noto esattamente) in tutto il pacchetto, salvo G-T2, che usa DM-inv.

### [SYS-L0] Test d'iniettività su un sottomodulo essenziale — standard
Sia φ : M → F un omomorfismo di R-moduli e sia E ⊆ M essenziale (ogni sottomodulo non nullo di M interseca E in modo non banale). Allora φ è iniettiva se e solo se φ|_E è iniettiva.
*Prova.* ker φ ∩ E = ker(φ|_E). Se questo è 0, ker φ è un sottomodulo che interseca E banalmente, quindi è nullo per essenzialità. ∎

### [SYS-C1] Sistemi quadrati non singolari in n ≥ 2 variabili — prova scritta
*Enunciato.* Siano n ≥ 2 e P ∈ R^{k×k} con det P ≠ 0. Allora soc_m(M_P) = 0 per ogni m massimale, quindi su ogni Ω aperto connesso esiste u ∈ Sol(P) che identifica P. Inoltre Ass(M_P) è costituito dai primi di altezza 1 che dividono det P.
*Prova.* La successione 0 → R^{1×k} → R^{1×k} → M_P → 0 (moltiplicazione a destra per P) è esatta, perché det P ≠ 0 rende P iniettiva. Applicando Hom_R(R/m, −) si ottiene la successione esatta Hom(R/m, R^k) → Hom(R/m, M_P) → Ext¹_R(R/m, R)^k. Il primo termine è nullo (R è un dominio). Il terzo è nullo perché m è generato da una successione regolare di lunghezza n ≥ 2, e quindi Ext^i(R/m, R) = 0 per i < n (complesso di Koszul; Weibel 4.5, numerazione da verificare). Dunque soc_m(M_P) = 0 e si applica SYS-EX. Per Ass: pd M_P ≤ 1, quindi per Auslander–Buchsbaum depth M_p ≥ ht p − 1 per ogni primo p. Se p ∈ Ass(M_P), allora depth M_p = 0, quindi ht p ≤ 1; p ≠ 0 perché M_P è di torsione, e p ⊇ (det P), quindi p è un fattore primo di det P. ∎

## 7. Risposta a "λ ∈ Mat 4×4" in forma hamiltoniana — H-DIRAC, prova scritta, SymPy C1–C7
*Classe.* 𝒞 := {L = I_4 ∂_t + Σ_{k=1}^3 α^k ∂_k + B : α^k, B ∈ Mat_4(ℂ) arbitrarie}. È la forma hamiltoniana ψ_t = −α·∇ψ − iβmψ, con B = iβm. Non si assumono le relazioni di Clifford. Dato: DM3, ψ ∈ C^∞(Ω)^4 in una base fissata.

### [H-DIRAC-1] Identificazione esatta dei coefficienti
*Enunciato.* Sia L_0 ∈ 𝒞, e sia ψ ∈ Sol(L_0) che identifica L_0 (Ann(ψ) = U_{L_0}). Se L ∈ 𝒞 e Lψ = 0, allora L = L_0: le matrici α^k e B sono determinate da ψ, senza ambiguità GL a sinistra e senza coniugio.
*Prova.* Le righe di L stanno in Ann(ψ) = R^{1×4}L_0, quindi L = V L_0 con V ∈ R^{4×4}. Sia W := V − I, così che L − L_0 = W L_0. L − L_0 = Σ(α^k − α_0^k)ξ_k + (B − B_0) non contiene τ e ha grado ≤ 1. Supponiamo W ≠ 0 e sia W_d ≠ 0 la sua componente omogenea di grado massimo d. La componente di grado d + 1 di W L_0 è W_d (τI + Σα_0^k ξ_k). È non nulla, perché det(τI + α_0·ξ) = τ^4 + … ≠ 0, quindi τI + α_0·ξ non è un divisore di zero in Mat_4(R).
- Se d ≥ 1, il grado d + 1 ≥ 2 contraddice "grado ≤ 1".
- Se d = 0, W è costante e W L_0 ha coefficiente di τ uguale a W ≠ 0, mentre L − L_0 non contiene τ: contraddizione.
Dunque W = 0 e L = L_0. ∎
*Lettura.* L'ambiguità D ~ VD della forma covariante γ^μ ∂_μ è solo un artefatto della forma: γ^0 D è la forma hamiltoniana (C6) e la normalizzazione "coefficiente di ∂_t = I" la elimina. Il coniugio α ↦ SαS^{−1} di Pauli (F6-HOR) compare solo con il modello di dato "ψ a meno di un cambio di base costante" (ψ ↦ Sψ), che non è DM3.

### [H-DIRAC-2] Esistenza e test
*Enunciato.* Per Dirac massivo (m ≠ 0) in 3+1, in rappresentazione chirale D = [[−m, X], [Y, −m]] con X = p_0 − σ·p, Y = p_0 + σ·p, XY = YX = KG · I_2, KG := p_0² − |p|² (C1).
(a) M_D ≅ (R/q)^{1×2} con q := (KG − m²), primo (C5), generato dalle classi di e_3 ed e_4. Quindi μ_q = 2 e Ass(M_D) = {q}.
(b) Esiste sempre ψ ∈ Sol(D) che identifica D (SYS-C1, n = 4).
(c) ψ identifica D ⟺ (ψ_3, ψ_4) sono R/q-indipendenti: r_3(∂)ψ_3 + r_4(∂)ψ_4 = 0 ⇒ r_3, r_4 ∈ q.
(d) In 1+1, D_2 = [[−m, p_0 − p_1], [p_0 + p_1, −m]], M_{D_2} ≅ R/q è ciclico, generato da e_2, e ψ identifica D_2 ⟺ ψ_2 ∉ EP.
*Prova.* (a) In M_D le righe di D sono nulle. Le prime due danno e_top = (1/m) X e_bot (m è invertibile). Sostituendo nelle ultime due si ha (1/m)(YX − m²) e_bot = ((KG − m²)/m) e_bot = 0 (C4). Quindi M_D ≅ R^{1×2}/R^{1×2}(KG − m²)I_2 = (R/q)². (c) E = M_D stesso è libero su R/q con base e_3, e_4: si applica SYS-L0, e φ_ψ(r_3 e_3 + r_4 e_4) = r_3(∂)ψ_3 + r_4(∂)ψ_4. (d) Analogamente M_{D_2} ≅ R/q, generato da e_2 (C7). In ℂ[τ, ξ] ogni ideale che contiene strettamente il primo q di altezza 1 ha colunghezza finita. Quindi Ann(ψ_2) ⊋ q ⟺ ψ_2 è annullata da un ideale di colunghezza finita ⟺ ψ_2 ∈ EP (C3-L3). Infine ψ_1 = (p_0 − p_1)ψ_2/m. ∎
**Risposta alla domanda dell'utente.** Un operatore con coefficienti λ ∈ Mat_4(ℂ) costanti è un elemento di Mat_4(R): l'oggetto è il modulo M_D, non un'algebra non commutativa nuova. In forma hamiltoniana, da una ψ nota in una base fissata, le matrici α^k e βm si leggono **esattamente** non appena ψ identifica il sistema. Una tale ψ esiste sempre (SYS-C1). Il test è un'indipendenza di molteplicità 2 sulle componenti chirali basse (3+1), oppure "ψ_2 non è EP" (1+1).
