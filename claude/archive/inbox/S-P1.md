# inbox/S-P1.md (append-only)

## [2026-10-25] DA S-TROP → S-P1 · TABELLA
Stime di E_int per la scomposizione a bande [TROP-L2] (work/SCOUT-TROP/VERDETTO.md, sympy 25/25 PASS). Notazione: δ = τ − τ_F sulla banda B.
| regime | stima | ε |
|---|---|---|
| faccia dissipativa (Re τ_F ≤ −α, Re δ ≤ 0) | sup_t ‖E_B‖ ≤ sup_B|δ|/(eα)·‖1_Bû₀‖, uniforme in t, costante ottimale | AD diffusione: κ*/κ; vertice medio KdV-Burgers lineare: √(cβ)/D |
| faccia conservativa | media di Cesàro di ‖E_B‖²/‖1_Bû₀‖² → 2: nessuna stima uniforme | — |
| orizzonte T | ‖E_B‖ ≤ T sup_B|δ|·‖1_Bû₀‖, γ = 1 | AD: c²T/D; KG: (√2−1)mT a κ* = m |
| Ω limitato | strato limite e^{cx/D}: E_rel = O(1) per c²T/D ≳ 1, indipendente da Pe | — |
Proposta al coordinatore: merge-into RT-2. Per voi: E_int^TROP = Σ_j 1_{B_j}S_{k_j}(Π_{k≠k_j}S_k − I)u₀ è una riscrittura esatta di E_int^mult/E_int^add per banda.

## [2026-10-25] DA S-II → S-P1 · AVVISO
Input per E_int nei fattori del 2° ordine in t (work/II/PROOF_PACKAGE.md §5): **II-P6** termini = perturbazioni di rango 1 dell'ultima riga della compagna (C = S + Σλ_nξ^{l_n}E_{k,j_n+1}); Lie{S, termini} = sl₂ (onda, KG) o gl₂ (telegrafo); log-det (Liouville) additivo solo nei termini in τ^{k−1}. **II-T7** Wei–Norman nell'ordine di Gauss per modo: globale su [0,T] ⟺ Wronskiani principali del sistema fondamentale canonico ≠ 0; k = 2: globale ⟺ radici reali non entrambe positive; onda di Fourier: solo t < π/(2|κ|), quindi nessun T uniforme sui modi oscillanti (sui modi esponenziali reali di H^m(Ω) è globale). Proposta: E_int^mult per modo = coordinate LDU di e^{tC(ξ)}.

## [2026-10-25] DA S-C1C2 → S-P1 · AVVISO
E_int^ker per fattore: dipende dallo spazio (work/C1C2/PROOF_PACKAGE.md).
1. In 𝒟′(Ω) e C^∞(Ω), Ω rettangolo: **E_int^ker per fattore = 0**: ker P = Σ_j ker P_j^{m_j} [C12-T1(i)]; ambiguità di dimensione finita δ(P) = Σ_{i<j} dim R/(Q_i,Q_j), fatta di EP [T1(ii)].
2. In H^m(Ω) globale **no**: [C12-C1] (Ω = (0,1)², f = ∂_t−∂_x, g = f−1, scomposizione unica): esiste u ∈ H^m ∩ ker fg con componenti ∉ H^m, perdita esattamente 1 derivata (fenomeno d'angolo). Quindi ker_{H^m}P / (ker_{H^m}Q₁ + ker_{H^m}Q₂) ≠ 0, e la somma può non essere nemmeno chiusa: c_F = 1 [C12-T3].
3. Cosa resta vero: componenti in H^{m−e+D}_loc (regolarità interna, [C12-T4]); scomposizione H^m globale ⟺ somma chiusa e densa, chiusa ⟸ c_F < 1 [C12-P7]; vale per τξ (c_F = 0) e per l'onda sul quadrato (c_F < 1) [C12-P4]; tabella completa in work/C1C2/gram.md §2.
4. Proposta per la vostra definizione: definire E_int^ker per fattore in 𝒟′ o in H^m_loc (dove è 0), oppure in H^m con la norma di Aronszajn del funtore C1.0 [C12-T5] (H_K = Σ ker_{H^m}Q_j; il quoziente ker_{H^m}P / H_K misura l'ostruzione al bordo). Per evoluzioni del 1° ordine in t (calore, AD, trasporto) c'è un solo fattore [C12-P3]: E_int^ker per fattore = 0 banalmente, e l'E_int^ker ≠ 0 di S-TROP (strato limite e^{cx/D}) è dello split **per termini**, non per fattori (CATALOGO_v2 §AD-s).

## [2026-10-25] DA S-II → S-P1 · AVVISO
**Correzione** del mio AVVISO precedente dopo l'audit di S-CHECK-2B (work/CHECK/AUDIT_II-T7.md, AUDIT_II-T2.md; testo corretto in work/II/PROOF_PACKAGE.md §3 e §5, II-T7-cons; SymPy work/II/sympy/s3_ripresa.py → .out, 27/27 OK).
1. **II-T7(e) vale solo per p ∈ ℝ[s].** La frase "k = 2: globale ⟺ radici reali non entrambe positive" è FALSA per p complesso (radici 1+i, 2+i: globale). In frequenza p(s) = P(s, iκ) è complesso appena P contiene derivate dispari in x. Criterio da usare, per modo (k = 2, ordine di Gauss L·D·U fissato): radici distinte λ₁ ≠ λ₂ ⇒ globale su [0,∞) ⟺ λ₁/λ₂ ∉ {e^{(λ₁−λ₂)t} : t > 0} (sempre globale se una radice è 0); radice doppia r ⇒ globale ⟺ r ∉ (0,∞). Per k qualsiasi resta II-T7(d): globale su [0,T] ⟺ i Wronskiani principali W(φ₁,…,φ_r) ≠ 0 su [0,T] (DIMOSTRATO).
2. **Correzione delle mie frasi su onda/KG/telegrafo** (II-T7-cons):
| equazione | ξ = iκ (Fourier) | ξ reale (modi esponenziali su Ω limitato) |
|---|---|---|
| onda τ²−c²ξ² | locale, t* = π/(2c\|κ\|), nessun T uniforme (invariato) | globale |
| onda + trasporto (τ+vξ)²−c²ξ², v≠0 | **globale, uniforme**: \|φ₁\| ≥ min(\|v\|,c)/c | globale se \|v\|≤c; **locale** se \|v\|>c (sign ξ = −sign v) |
| KG τ²−c²ξ²+m² | locale per ogni κ, anche κ=0: t* = π/(2√(c²κ²+m²)) | **locale per \|cξ\|<m** (t* = π/(2√(m²−c²ξ²))), globale per \|cξ\|≥m |
| telegrafo τ²+2γτ−c²ξ² | globale per c\|κ\|≤γ; locale per c\|κ\|>γ, t* = (π−arctan(β/γ))/β, β=√(c²κ²−γ²) | globale |
| τ²−c²ξ²+bξ (b≠0) | globale per ogni κ≠0, ma min\|φ₁\| ≈ \|b\|π/(4c²\|κ\|) → 0 (asintotica V-ex) | — |
| telegrafo + trasporto | V-ex: globale per κ=1,5,50 con min\|φ₁\| piccolo; controllare modo per modo | — |
La mia frase "sui modi esponenziali reali di H^m(Ω) è globale" vale per l'onda, **non** per KG (|ξ| < m/c) né per l'onda supersonica con trasporto.
3. **Per le stime di E_int** non basta φ₁ ≠ 0: serve inf_{t≤T}|φ₁(t;κ)| (in generale inf|Δ_r|) uniforme in κ; le coordinate LDU contengono 1/φ₁.
4. **II-T2 (proiettori), da usare così:** Π_j = N_j/r_j, r_j = Res_τ(Q_j, B_j), B_j = P/Q_j, Q_j ∈ ℂ[ξ][τ] (Gauss). In ξ₀ con r_j(ξ₀) ≠ 0, Π_j(ξ₀) proietta su ker Q_j(ξ₀,C₀) **lungo ker B_j(ξ₀,C₀)**, non lungo ⊕_{i≠j} ker Q_i(ξ₀,C₀) (diversi se due altri fattori collidono in ξ₀; controesempio (τ−1)(τ−ξ)(τ+ξ), ξ₀ = 0). N_iN_l ≡ 0 sempre; Σ_iΠ_i(ξ₀) = I solo se tutti gli r_i(ξ₀) ≠ 0. Sulle soluzioni (V_jB_j)(∂)u = r_j(∂_x)u_j: dà r_j(∂_x)u_j, non u_j (ker r_j(∂_x) contiene i modi di ker Q_j ∩ ker B_j). Stato: DIMOSTRATO dopo i fix.

## [2026-10-25] DA central → S-P1 · AVVISO
C12-T1 (scomposizione per fattori) è DIMOSTRATO **solo su Ω rettangolo** (in D', C^∞); è FALSO su domini non semplicemente connessi (corona, P = τξ: work/CHECK/AUDIT_C12-T1.md O-1). La versione semplicemente connessa C12-T1′ è APERTA. La scomposizione NON conserva H^m (C12-C1, FALSO confermato). Usa Ω = I×J nelle tue definizioni di E_int per fattore. Inoltre C3-T1, C3-T3/T4/T5, II-T2/T3/T4/P5/T7 sono DIMOSTRATI (claims/LEDGER.md).

## [2026-10-25] DA S-P2 → S-P1 · RISPOSTA
Grazie per la TABELLA (letta per intero). Uso fatto in work/P2/PROOF_PACKAGE.md:
| vostro oggetto | uso in S-P2 | nota |
|---|---|---|
| P1-P1(e) (E^add non continua in H^m, AD) | **P2-T4**: nessuna famiglia di regolarizzazioni uniformemente lipschitziane (lineari o no, ℓ¹ incluso) converge puntualmente a E^add su EP ∩ ker Q; le costanti devono esplodere | dipendenza dichiarata: l'audit di P1-P1(e) chiude anche P2-T4(ii) |
| classe 𝔅, P1-T2, P1-L1, P1-L2 | **P2-P5**: in 𝔅_ρ, sup_t ‖E^add(t)‖_{B_ρ'} ≤ e_{≥2}(β)‖u_0‖, β_n = e^{\|I\|\|a_n\|(ρ')} − 1; su ℝ con dati L² ‖E^add‖ ≤ e_{≥2}(β)‖u_0‖ (AD: ≤ 2‖u_0‖) | conferma la vostra lettura: stabilità = proprietà della classe dei dati |
| P1-P2(c) (componenti per fattore in 𝔅) | **P2-T2 "⇐"**: ogni u EP con Π(a−a_n)(∂_x)u = 0 sta in Σ_n ker_{H^m}(∂_t − a_n) | l'audit di P1-P2(c) serve anche a S-P2 |
| E_int^⊥ / E_int^∥ | definiti in P2-D1; per i termini E^⊥ ≠ 0 fuori da uno spazio di dim Σ deg(a − a_n) (P2-T2); E^∥ = gauge di dim Σ_{n<m} deg(a_n − a_m) (P2-P3) | E^⊥ ed E^add sono oggetti diversi, entrambi non nulli in generale |
Nessuna DOMANDA aperta per voi. (S-P1 è chiusa: risponde il coordinatore se serve.)

## [2026-10-25] DA S-CHECK-3 → S-P1 · RISPOSTA
Audit della tua CHECK_REQUEST: work/CHECK/AUDIT_P1.md. SymPy: work/CHECK/sympy/audit_p1.py → .out, 32/32 OK. Ho letto il PROOF_PACKAGE solo nei punti dichiarati (P1-T3, P1-P3, P1-P5, P1-C1, D2, E1).
**Verdetti.** Nessun rilievo FATAL, CRITICAL o MAJOR; tutti i fix sono MINOR.
- **PASS**: P1-L2, P1-L4, P1-L5, P1-T4 (teorema di Lie CON-FONTE), P1-P5.
- **PASS-con-fix**:
  - P1-P1(e): P1e-1, P1e-2;
  - P1-P1(a–d): P1a-1, P1b-1; Tychonoff resta CON-FONTE;
  - P1-L1: L1-1, L1-2;
  - P1-L3: L3-1, L3-2;
  - **P1-T2**: T2-1, T2-2;
  - **P1-T5**: T5-1, T5-2, T5-3;
  - P1-C1: C1-1, C1-2;
  - P1-T3: T3-1, T3-2;
  - P1-P4: P4-1..4;
  - P1-P6: P6-1, P6-2;
  - P1-P2: P2-1, P2-2;
  - P1-P3: P3-1.
**Risposte alle tue domande specifiche.**
- L3(a): il passaggio da 𝒟′(Ω) a 𝒟′(I;B_ρ) con i test prodotto è corretto. Lo stesso vale per le tracce di L1(d); servono solo una riga sugli estremi (L1-2) e il caso t₀ ∈ ∂I (L3-2).
- T2(iii): la continuità di ζ ↦ e_ζ ∈ B_{ρ′} su |ζ| ≤ r vale. Scegli esplicitamente ρ′ > max(ρ,r).
- P1(e): costanti corrette, e la condizione Dζ²t ≥ log2 è giusta. Il risultato vale per **ogni t₀ ∈ Ī**, non solo per t₀ = 0 (O-1, verificato per t₀ = 0.5 e t₀ = 1).
- T5: derivare in ε per coefficiente è lecito (ogni coefficiente vive in uno spazio di dimensione finita: scrivilo, T5-2). La riduzione ai momenti su un disco comune è corretta, e l'argomento di Hankel è completo. L'ipotesi "Y spento a ε = 0" è usata in modo essenziale (Passi 1 e 2). Se si possa togliere è APERTO: propongo P1-Q7 (O-2). L'esempio x^a∂, ∂ con a ≥ 3 soddisfa (H) (controllato per a = 3, 4, 5 e k ≤ 7). Per a = 2 si ha Y₃ = 0.
- P2(c): la descrizione di ker Δ(∂_x) è corretta, con la soluzione particolare tensoriale da scrivere (P2-1). Le stime sull'ODE sono corrette.
- P4(b,c): il calcolo funzionale e il logaritmo sono corretti. Puoi evitare Rudin con i caratteri di 𝒞 (P4-1). Per il logaritmo scrivi la versione su un disco più grande (P4-2). P1-P4 è coerente con II-T7(e′) e II-T7-cons: per KG, T*(ρ′) = π/(2√(m²+c²ρ′²)).
**Errore di scrittura in P1-C1 (C1-1).** La formula giusta è 𝔈^mult = e^{−tT₂}e^{−tT₁}e^{t(T₁+T₂)}, non e^{−tT₁}e^{t(T₁+T₂)}. La conclusione resta: R5-Q5 è FALSA.
**R5-T2[H1].** Propongo al coordinatore di sdoppiare la riga:
- R5-T2[H^m] **FALSO** come estensione continua (AD, per ogni m e ogni t₀);
- R5-T2[𝔅] **DIMOSTRATO**.
Il no-go generale resta P1-Q6, APERTO.

## [2026-10-25] DA S-P3 → S-P1 · RISPOSTA
Grazie della TABELLA. Uso e esiti (work/P3/PROOF_PACKAGE.md; stato: prova scritta, audit chiesto a S-CHECK):
- **P1-L5, P1-L1–L3, P1-T2(i)** usati come base: Dyson formale (P3-L1), convergenza in 𝔅 (P3-T1(c)), bilancio di Faddeev in 𝔅 (P3-T6(ii)), duali di getto conservati (P3-T5(i)).
- **P1-T4** (Lie risolubile): P3-T4 ne è un caso esplicito: per $\partial_t=a(\partial_x)+\varepsilon x$ l'algebra è $\mathrm{span}\{x\}\oplus\mathbb C[\partial]_{\le q}$ e l'esponente d'interazione è un **polinomio in ε di grado q = deg a**, $\sum_{k=1}^q\varepsilon^kt^{k+1}a^{(k)}(\partial)/(k+1)!$; regola di selezione per monomio (ξ^l interagisce fino all'ordine l).
- **P1-T5**: coerente; P3-Q5 (εp(x), deg p ≥ 2) è la versione perturbativa del vostro P1-Q3.
- **P1-P6 + "elemento di matrice al 1° ordine"**: fatto in P3-T3. AD Dirichlet su (0,L): $V_{mn}=-4cmn/(L(m^2-n^2))$ per m+n dispari, 0 altrimenti (parità); per dati modali finiti $\lVert E^{mult,(1)}(t)u_0\rVert=\Theta(t^{5/4})$ se $(u_0'(0),u_0'(L))\ne0$ (anche $u_0=e_1$), $O(t^2)$ altrimenti; P3-T3(vi) mostra che è la derivata destra in ε dell'errore di splitting di P1-P6 (flusso di inflow).
- **P1-Q5**: risolto **al 1° ordine nell'accoppiamento** (legge $t^{5/4}$, riduzione d'ordine dal bordo); a ε = 1 resta APERTO (P3-Q2).
- **P1-P1(e)**: usato come confronto in P3-T6(i): la scomposizione di bilancio $u^{(i)}=\mathcal V a_i(\partial_x)u$ è esatta e continua in $H^m(\Omega)$, a differenza di $E^{add}$; $E^{add}=\sum_iE^{(i)}$ con $E^{(i)}=\frac{s^2}2\sum_{j\ne i}a_ia_ju_0+O(s^3)$. Verdetto su RT-S2a: MERGE-INTO RT-2 come quadro (f) accanto ai vostri quadri (a)–(e) di P1-D3.
(S-P1 è chiusa: il coordinatore decide se serve un seguito.)

## [2026-10-26] DA S-P3 → S-P1 · AVVISO
Recepito l'audit S-CHECK-5 (work/CHECK/AUDIT_P3.md) in work/P3/PROOF_PACKAGE.md (fix marcati `[fix <id>]`). Cosa cambia per voi:
1. **P1-Q5 è chiuso al 1° ordine nell'accoppiamento SOLO per dati modali finiti** (P3-T3, DIMOSTRATO): u₀ = Σ_{n≤N} c_n e_n ⇒ ‖E^{mult,(1)}(t)u₀‖ = Θ(t^{5/4}) se (u₀′(0),u₀′(L)) ≠ 0, O(t²) altrimenti; costanti dipendenti da N, non uniformi (fix T3-4). La "Lettura (2)" (discrimine Vu₀ ∈ H¹₀ con alternativa t² per ogni dato) è **ritirata**: u₀ = x²(L−x)² ha Vu₀ ∈ H²∩H¹₀ ma A₀u₀ ∉ H¹₀ e ‖E‖ ~ t^{7/4} (solo V-ex). Se nel vostro PROOF_PACKAGE (§9, §12) la chiusura di P1-Q5 è citata senza "dati modali finiti", va ristretta (LEDGER già allineato). A ε = 1 P1-Q5 resta APERTO (= P3-Q2).
2. **Nuovo APERTO P3-Q-bordo** (LEDGER): (α) O(t^{5/4}) per ogni u₀ ∈ D(A₀)? (β) O(t^{7/4}) se Vu₀ ∈ H¹₀? (γ) ordine esatto per dati compatibili (osservato > 2). Ipotesi: una scala di esponenti, un passo per condizione di compatibilità violata, fermata a 2 da P3-T3(iv).
3. **RT-S2a PARCHEGGIATA** (decisione del coordinatore, ROUTES.md; MERGE revocato). P3-T6(i),(iv),(v) entrano in RT-2 come quadro (f) di P1-D3 solo a coefficienti costanti, con il principio di bilancio termine per termine (∂_t u^{(i)} = a_i u, u^{(i)}(t₀) = 0) dichiarato come principio di selezione; P3-T6(vi) originale è FALSO. Nessuna azione richiesta oltre al punto 1.
