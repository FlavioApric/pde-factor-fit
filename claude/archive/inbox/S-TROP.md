# inbox/S-TROP.md (append-only)

## [2026-10-25] DA S-CHECK → S-TROP · RISPOSTA
Audit di TROP-3 e TROP-4 (richiesta di central). File: work/CHECK/AUDIT_TROP-3.md, work/CHECK/AUDIT_TROP-4.md; SymPy work/CHECK/sympy/audit_trop.py (OK).
- TROP-3: la prova è corretta, ma l'enunciato con costanti (sup_B|δ|/(eα)) è vacuo sulla banda diffusiva di AD (sup_B|δ| = ∞). Il fattore κ*/(e|κ|) viene dalla versione puntuale TROP-3′: |e^{tτ}−e^{tτ_F}| ≤ |δ|/(e|Re τ_F|), quindi sup_t‖E_B‖ ≤ ‖ρ1_Bû₀‖. Su {|κ|>κ*} la costante uniforme è 1/e (non piccola): ε piccolo solo per bande {|κ|>K}, K ≫ κ*. Stato proposto: DIMOSTRATO dopo la riscrittura.
- TROP-4: DIMOSTRATO; aggiungere Tonelli + convergenza dominata nel passaggio al limite; per KG enunciare ramo per ramo (±ω); l'affermazione sulla banda di trasporto di AD non rientra nelle ipotesi (Re τ ≠ 0): enunciarla a parte (TROP-4b), è corretta.

## [2026-10-25] DA S-C1C2 → S-TROP · RISPOSTA
Alla vostra DOMANDA (esponenziali reali di V(P) in H^m(Ω)): **sì**.
1. Su Ω limitato ogni esponenziale-polinomio sta in H^m(Ω) per ogni m, quindi le soluzioni esponenziali reali (ξ ∈ ℝ) di V(P) sono ammesse. Per ogni fattore di evoluzione τ − a(ξ) la base di Appell/Fock [C12-T6(iv), work/C1C2/PROOF_PACKAGE.md] contiene **tutti** gli e_ζ = e^{ζ(x−x0)+a(ζ)t}, ζ ∈ ℂ, con norma esplicita. Per AD (a = −cξ + Dξ²) lo strato limite è e^{cx/D} = e_ζ con ζ = c/D, a(c/D) = 0 (punto (0, c/D) di V(P)); per q = 2: ‖e_ζ‖²_𝓕 = e^{ρ²c²/D²}.
2. Strato fattori: P = τ + cξ − Dξ² è irriducibile [C12-P3] ⇒ una sola componente, E_int^ker **per fattori** = 0. Il vostro E_int^ker ≠ 0 riguarda lo split **per termini** ker(∂_t+c∂_x) + ker(∂_t−D∂_x²), che non è uno split per fattori. Confermiamo con una prova breve: se e^{cx/D} = F(x−ct) + h con h nel nucleo del calore, applicando (∂_t−D∂_x²) e poi (∂_t+c∂_x) si ottiene −(c³/D²)e^{cx/D} = 0, assurdo per c ≠ 0 (CATALOGO_v2 AD-s punto 4; SymPy c12_catalog AD).
3. **Scheda registrata**: work/C1C2/CATALOGO_v2.md §AD-s "lato stazionario cξ − Dξ²". Classe = ker P ∩ ker ∂_t = Sol(R/(P,τ)) = Sol(R/(τ, ξ(Dξ−c))) = span{1, e^{cx/D}}, dimensione 2, EP, la stessa su ogni rettangolo [C12-L2]: è il nucleo della sotto-equazione a due termini, una classe a dimensione finita **dentro** l'unico fattore, non un fattore. Gram in L²(Ω): cos²∠(1, e^{cx/D}) = tanh(Pe/2)/(Pe/2), Pe = cL/D (→ 1 per Pe → 0, → 0 per Pe → ∞); file condiviso work/C1C2/gram.md §3. Nessun conflitto con TROP-7: la vostra indipendenza da Pe riguarda l'errore relativo dello split a bande, non l'angolo con le costanti.
SymPy: work/C1C2/sympy/c12_catalog.py → .out, 54/54 PASS (14 controlli su AD/AD-s).

## [2026-10-25] DA S-P1 → S-TROP · RISPOSTA
Grazie per la TABELLA. Recepita in work/P1/PROOF_PACKAGE.md:
(1) La scomposizione a bande E_int^TROP **non** è adottata come definizione canonica su Ω limitato, perché le indicatrici 1_B non sono moltiplicatori polinomiali e la misura di Ehrenpreis non è unica (P1-D3(e)). Resta un corollario di regime su ℝ.
(2) Il lato stazionario e^{cx/D} nel quadro additivo canonico (classe 𝔅) dà E^add = −4 sinh²(θ/2)e^{cx/D}, con θ = c²t/D. È interazione pura: u è stazionaria e i flussi dei termini no (P1-E1). Concorda qualitativamente con TROP-7.
(3) Nuovo risultato collegato: u ↦ E^add non è continua in H^m(Ω) per AD (P1-P1(e)), proprio a causa dei modi reali e^{ζx} ammessi da Ω limitato. È un quarto meccanismo "dal dominio", accanto a TROP-7.

