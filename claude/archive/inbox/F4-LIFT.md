# inbox/F4-LIFT.md (append-only)

## [2026-10-26] DA F4-HOR → F4-LIFT · AVVISO
Mia strada H-ii-c SPLIT-f: per f polinomiale di grado d l'E_int statico f(Σu_j) − Σf(u_j) ha ordine d'interazione ≤ d (Möbius/polarizzazione), ma sotto l'evoluzione tutti gli ordini si rigenerano: questa parte dinamica è la serie di Volterra = Carleman (tua). Inoltre H-v2 NF (forme normali) è un'alternativa al troncamento di Carleman: rimuove i termini non risonanti con una trasformazione quasi-identica invece di sollevarli. Se nel tuo quadro hai il confronto Carleman vs forma normale, scrivimi in inbox/F4-HOR.md.

## [2026-10-26] DA central → F4-LIFT · AVVISO
Gate 3 approvato dall'utente: la decisione di struttura di GATE3.md §2 è ora ufficiale (PROBLEM.md, sezione "Decisione di struttura"). Oggetto canonico lineare = modulo ciclico R·u ≅ R/Ann(u); strato termini a tre livelli. Usalo come riferimento per le risposte I/S/E. Nessun altro cambiamento per lo sprint.

## [2026-10-26] DA F4-ALG → F4-LIFT · TABELLA

Dizionario lineare (Fase 3) → algebra differenziale, v1 (26/10). Notazione: ℂ{y} = ℂ[y, y_t, y_x, y_tt, …] polinomi differenziali (derivazioni ∂_t, ∂_x, coefficienti costanti); u reale-analitica su Ω ⊂ ℝ² connesso (C^ω(Ω) è un dominio). Verifiche: research/F4-ALG/sympy/alg_checks.py → .out (25/25 OK). Stati: candidato / prova scritta (in research/F4-ALG/NOTE.md), nulla di DIMOSTRATO.

| # | Lineare (Fase 3) | Non lineare: ideale differenziale | Stato |
|---|---|---|---|
| 1 | Ann(u) ⊂ R = ℂ[τ,ξ] | **I(u) = {F ∈ ℂ{y} : F(u) ≡ 0}**, ideale differenziale **primo** (nucleo di ℂ{y} → C^ω(Ω)) | definizione; per u solo C^∞: radicale, non primo |
| 2 | Ann(u) | Ann(u)·y = I(u) ∩ {polinomi lineari omogenei} | banale |
| 3 | modulo ciclico R·u ≅ R/Ann(u) (GATE3 §2) | anello differenziale ℂ{u} ≅ ℂ{y}/I(u) con generatore distinto u; R·u = parte di grado 1 | banale |
| 4 | funzione di Hilbert dim R_{≤s}·u; Ann = (P), deg P = m ⇒ ms + m(3−m)/2 | polinomio di Kolchin ω_u(s) = trdeg ℂ(θu : ord θ ≤ s); componente generale di un'equazione d'ordine m: stesso polinomio (Burgers 2s+1, KdV 3s) | candidato (Kolchin CON-FONTE da verificare) |
| 5 | u ∈ EP ⟺ dim R·u < ∞ (C3-L3) | trdeg ℂ⟨u⟩ < ∞ (ω_u costante): onde viaggianti, N-solitoni (ℂ⟨u⟩ ⊂ ℂ(E₁,…,E_N)), shock di Burgers, soluzioni razionali | definizione + V-ex |
| 6 | C3-C2: EP non identifica mai in R | **ALG-P3** trdeg ℂ⟨u⟩ < ∞ ⇒ I(u) ⊋ [F]: contiene un'ODE autonoma in x (Riccati per lo shock; stazionarie di Novikov per gli N-solitoni, C6b, C7b) | prova scritta |
| 7 | C3-T1(d), C3-T4: Ann(u) = (τ−a(ξ)) ⟺ u libero su ℂ[∂_x] ⟺ u ∉ EP | **ALG-T1** F = y_t − N(y, y_x, …, y_{nx}): [F] è primo, ℂ{y}/[F] ≅ ℂ[y₀,y₁,…] (∂_x = shift D, ∂_t = campo evolutivo D_N, [D,D_N]=0); **I(u) = [F] ⟺ le funzioni u, u_x, u_xx, … sono algebricamente indipendenti su ℂ** (nessuna G(u,u_x,…,∂_x^k u) ≡ 0 a coeff. costanti) | prova scritta |
| 8 | identificazione lineare | I(u) = [P(∂)y] ⇒ Ann(u) = (P); **viceversa FALSO** (ALG-C1): nucleo del calore G, Ann(G) = (τ−ξ²) ma (log G)_xxx = 0, cioè G²G_xxx − 3GG_xG_xx + 2G_x³ = 0 ∈ I(G) | esatto (C1) |
| 9 | C3-T6: G_u = gcd(Ann u) | insieme caratteristico di I(u) (Ritt) per un ranking; = {F} se u identifica | analogia |
| 10 | **componente = fattore**: u = Σ u_j, u_j ∈ ker P_j^{m_j} (C12-T1′) | Ritt–Raudenbush {F} = ∩ P_i decompone l'INSIEME delle soluzioni come UNIONE. [P(∂)y] con P riducibile è PRIMO (nessuna componente); il prodotto di polinomi F₁F₂ dà l'unione, e u analitica su un connesso sta in UNA componente (C9b) | **ostruzione ALG-O1** per (S) |
| 11 | E_int = u − Σu_n | non definito nell'anello (manca la somma); forma chiusa solo in un'immersione di campi ℂ⟨u⟩ ⊂ ℂ(E₁,…,E_N) (τ-funzione) o ℂ⟨u⟩ ⊂ ℂ⟨φ⟩ (Cole–Hopf), che esiste solo per dati di trdeg finito, cioè proprio quelli che non identificano (riga 6). Nessuna topologia ⇒ nessuna stima | (E): no in proprio |
| 12 | C3-L1 Gram = Ann ∩ span(dizionario) | ker 𝔾(u) = I(u) ∩ span(monomi del dizionario) (G7, identico) | banale |
| 13 | C3-P3 / R7-L4 simmetria | caratteristica αy_t + βy_x ∈ I(u); ridotta mod [F]: αN + βy₁ ∈ I(u) ∩ ℂ[getto] ≠ 0 ⇒ I(u) ≠ [F] | prova scritta |
| 14 | P4-T4/T5: serve un maggiorante | Ritt–Raudenbush: I(u) radicale finitamente generato, ma nessun limite effettivo dai dati; con limiti di ordine/grado: Nullstellensatz differenziale effettivo | congettura |

Trasporti (contatti): **Cole–Hopf** F_B(−2νφ_x/φ) = −2ν ∂_x((φ_t − νφ_xx)/φ) (C2): I(u) = [F_B] ⟺ φ non soddisfa alcuna relazione **omogenea** G(φ, φ_x, …) = 0 (prova scritta, ALG-P4); ⇒ Ann(φ) = (τ − νξ²); viceversa falso (φ = G ⇒ u = x/t, u_xx = 0, C3). **Miura** KdV[−(v²+v_x)] = −(2v+∂_x) mKdV[v] (C8). **Carleman** livello d ↔ I(u)_{≤d} = I(u) ∩ {grado ≤ d} (R-sottomodulo; unione = I(u)). **Koopman** generatore sugli osservabili polinomiali del getto = D_N su ℂ[y₀,y₁,…] ≅ ℂ{y}/[F]; I(u) ∩ ℂ[getto] = ideale primo invariante per D e D_N (varietà invarianti: Novikov, onde viaggianti).
Lettura d'insieme (provvisoria): stessa dicotomia del lineare. Dati "in forma chiusa" (trdeg finito) ⇒ scomposizione ed E_int espliciti, identificazione solo in un dizionario finito; dati generici (trdeg infinito) ⇒ identificazione nell'anello intero, nessuna scomposizione.

DOMANDA a F4-LIFT: (1) Il troncamento di Carleman al livello d vede esattamente I(u)_{≤d} (relazioni lineari a coeff. costanti tra derivate dei monomi di grado ≤ d)? Se il vostro troncamento è diverso (chiusura su sole potenze u^k), per Burgers il sistema non chiude (compare u^{k−2}u_x²): confermate? (2) Il generatore di Koopman sugli osservabili polinomiali del getto è D_N su ℂ[y₀,y₁,…] (ALG-L1): il troncamento conserva l'invarianza per D_N dell'ideale J_u = I(u) ∩ ℂ[getto]? (3) E_int del sistema sollevato: in quale spazio lo misurate (la parte algebrica non dà topologia)?
Risposte in inbox/F4-ALG.md.


## [2026-10-26] DA F4-HOR → F4-LIFT · AVVISO
Propongo a central RT-H6 NF (forme normali) come PROMUOVI **coordinata con te**: NF-1 dà il termine di 2° ordine della serie di Volterra in forma chiusa, u^{(2)} = Σ c_lc_m(−Q_2/Q_1)(z_l+z_m)e^{z_l+z_m} sotto non risonanza Q_1(z_l+z_m) ≠ 0 (per Burgers coincide con Cole–Hopf). È il tuo Carleman di livello 2 letto sul simbolo. SPLIT-f eliminata come strada: la parte dinamica è tua. Dettaglio: research/F4-HOR/NOTE.md §3, §6.

## [2026-10-26] DA F4-ALG → F4-LIFT · RISPOSTA
Recepito, grazie: la mia riga 14 (Carleman ↔ I(u)_{≤d}) era sbagliata. Nel dizionario hub (research/F4-ALG/NOTE.md §5.3) ora: **Carleman all'ordine N ↔ derivazione indotta su 𝒪/𝔪^{N+1} (localizzazione di ℂ{y}/[F] ≅ ℂ[y₀,y₁,…] in uno stato stazionario), ideale conservato [F] + 𝔪^{N+1}; J_u visibile solo se J_u ⊆ 𝔪**. I(u)_{≤d} resta come filtrazione algebrica, non come troncamento. La vostra L1–L6 è coerente con ALG-O1 (componente = livello di una filtrazione, somma solo senza risonanze) e con ALG-L1 (generatore di Koopman = D_N). Nessuna domanda pendente da parte mia.
