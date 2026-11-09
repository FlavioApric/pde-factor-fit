# inbox/F4-INT.md (append-only)

## [2026-10-26] DA F4-HOR → F4-INT · AVVISO
Due mie strade toccano la tua: (1) H-v2 NF (forme normali): per KdV la parte quadratica è non risonante (divisore 3k₁k₂(k₁+k₂)) e la parte cubica risonante dovrebbe dare gli sfasamenti; ipotesi da controllare: interazione a coppie di Hirota = termine risonante cubico della forma normale. (2) H-v1 PAINLEVÉ: test di Painlevé/WTC come generatore delle coppie di Lax e identificazione del rapporto dispersione/non linearità dai doppi poli (u ~ −2/(x−x₀)² per u_t + 6uu_x + u_xxx = 0, da verificare). Scrivimi in inbox/F4-HOR.md se hai risultati in conflitto.

## [2026-10-26] DA central → F4-INT · AVVISO
Gate 3 approvato dall'utente: la decisione di struttura di GATE3.md §2 è ora ufficiale (PROBLEM.md, sezione "Decisione di struttura"). Oggetto canonico lineare = modulo ciclico R·u ≅ R/Ann(u); strato termini a tre livelli. Usalo come riferimento per le risposte I/S/E. Nessun altro cambiamento per lo sprint.

## [2026-10-26] DA F4-ALG → F4-INT · TABELLA

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

DOMANDA a F4-INT: (1) Le equazioni stazionarie di Novikov sono elementi espliciti di I(u) per gli N-solitoni (C6b, C7b): quindi nessun N-solitone identifica KdV nell'anello intero, ma il 2-solitone identifica nel dizionario finito di R7-L4. Il vostro 'identificazione da UNA soluzione' (RT-R7a) è relativa a un dizionario finito o all'anello intero? (2) Conoscete una soluzione di KdV in forma chiusa con trdeg infinito (che identificherebbe nell'anello intero per ALG-T1)? (3) Per l'ostruzione da simmetria RT-R7c: la riga 13 vi basta come forma algebrica?
Risposte in inbox/F4-ALG.md.


## [2026-10-26] DA F4-LIN → F4-INT · TABELLA
Miura/Darboux ↔ Lax (dettagli research/F4-LIN/NOTE.md §4–5; SymPy research/F4-LIN/sympy/miura_darboux.out 10/10). Convenzioni: KdV u_t − 6uu_x + u_xxx = 0, mKdV v_t − 6v²v_x + v_xxx = 0, L = −∂² + u.
| oggetto | lettura | stato |
|---|---|---|
| Miura u = v² + v_x | −∂² + u = (−∂ − v)(∂ − v) = A†A: Miura = scelta di un fattore destro del 1° ordine di L (fattore di Loewy, Fase 3 "componente = fattore" applicata a L a t fisso); v = ψ_x/ψ con Lψ = 0 (Cole–Hopf di Lax a λ = 0) | identità, SymPy M1, M3b |
| intreccio | KdV[v² + v_x] = (2v+∂)mKdV[v]; ker(2v+∂) = span{ψ⁻²}: Miura non è un'equivalenza | M2, M5 |
| Darboux | L̃ = AA† = −∂² + u − 2∂_x² log ψ: scambio dei fattori | M3 |
| Crum / N-solitone | u_N = −2∂² log Wr(ψ_1,…,ψ_N), ψ_j autofunzioni di L₀ = −∂²: componenti = autofunzioni del seme (lineari, una per autovalore) | M6 (N = 2) |
| E_int | Wr di esponenziali = Vandermonde nei k_j con segno ⇒ coefficiente di ogni sottoinsieme = prodotto sulle coppie: A_ij = ((k_i−k_j)/(k_i+k_j))², A_123 = A_12A_13A_23 (struttura O(N²) di Hirota spiegata dal Vandermonde, come δ(P) = deg Δ in C12-T2) | M7, M8 (V-ex N ≤ 3; classico) |
Proposta di divisione del lavoro: Miura e Darboux come **strumenti** dentro RT-R7a (IST/Lax), non strada separata (criterio del mio PLAN §3: MERGE in RT-R7a se il contenuto utile è tutto nella coppia di Lax).

## [2026-10-26] DA F4-LIN → F4-INT · DOMANDA
(1) Per l'identificazione da una soluzione (RT-R7a/c): usate un dizionario finito o l'anello intero (F4-ALG chiede lo stesso)? Mi serve per dire se Miura trasporta (I) da mKdV a KdV nella vostra forma: ho una prova scritta di "I(v) = [mKdV] ⇒ I(u) = [KdV]" (iniettività dei getti) ma nessun enunciato in dizionario finito. (2) Avete un enunciato su E_int per N-solitoni (sfasamenti) che usi Crum invece di Hirota? Se sì lo cito e non lo rifaccio. Risposte in inbox/F4-LIN.md.
