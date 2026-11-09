# PATCH_GATE3 — revisione limitata di Gate 3 (GATE8 §3) e patch di SYNTHESIS-2 §0.2(b′) (ATTACK-8 O17)

Sessione S10-INT, 27/10/2026. Questo file contiene **solo proposte di testo**. I file del coordinatore (GATE3.md, PROBLEM.md, research/SYNTHESIS-2.md) non sono stati toccati. Ogni blocco «vecchio» è copiato esattamente dal file indicato, così che la sostituzione si possa fare con una ricerca letterale.

Fonti del mandato:
- GATE8 §3, punti 1 e 2: anello dei coefficienti specificato; per L7–L9 l'oggetto canonico include ρ_u; per i sistemi «componente = fattore» richiede Ext¹(N, 𝒜) = 0; C12-T1′ scalare invariato; «nessun'altra parte di Gate 3 è toccata».
- GATE8 §5 e GATE9 §4: la patch di SYNTHESIS-2 §0.2(b′), «fuori dalle fasce di silenzio, in (SF)».
- NOTAZIONE v6 (voci «Anello dei coefficienti» e «Sistemi»), che è già scritta: le patch qui sotto la rendono coerente con il testo di Gate 3.

Claim citati (stati dal LEDGER): VAR-N1 DIMOSTRATO; VAR-T1(a), (b), (c)(i)–(iii) DIMOSTRATO; VAR-T1(c)-F FALSO; VAR-T2a DIMOSTRATO; VAR-C3Q2(a)–(g) DIMOSTRATO; SYS-S1(i⇒), (i⇐), (ii) DIMOSTRATO; SYS-S1-C FALSO; C12-T1′ DIMOSTRATO; II-T2 DIMOSTRATO.

---

## P1. GATE3.md, §2, punto 1 (anello dei coefficienti e oggetto canonico)

**Vecchio** (GATE3.md, §2, riga che inizia con «1. **Oggetto canonico»):

> 1. **Oggetto canonico: il modulo ciclico M = R·u ≅ R/Ann(u)** (coeff. costanti), oppure la coppia (D·u, u) (coeff. variabili). Contiene l'identificazione (C3-T1, P4-T2: Ann(u) = G_u·J_u, R·u ∩ EP ≅ R/J_u) e la scomposizione (i suoi idempotenti, dopo aver invertito il risultante, sono le componenti per fattore: II-T2).

**Nuovo:**

> 1. **Oggetto canonico, con l'anello dei coefficienti dichiarato** (revisione limitata di Gate 8b, punto 1; NOTAZIONE v6). Ogni enunciato di questo tipo dichiara l'anello 𝒟 in cui si calcola Ann_𝒟(u) = {Q ∈ 𝒟 : Qu = 0}:
>    - **𝒟 = ℂ[∂] = ℂ[∂_t, ∂_x]** (coefficienti costanti): l'oggetto canonico è **il modulo ciclico M = R·u ≅ R/Ann(u)**. Contiene l'identificazione (C3-T1, P4-T2: Ann(u) = G_u·J_u, R·u ∩ EP ≅ R/J_u) e la scomposizione (i suoi idempotenti, dopo aver invertito il risultante, sono le componenti per fattore: II-T2).
>    - **𝒟 = ℂ(x)[∂] oppure l'algebra di Weyl A_n** (coefficienti razionali o polinomiali): l'oggetto canonico è la coppia (𝒟·u, u), con Ann_𝒟(u) ideale sinistro (VAR-T2a in ℂ(x)[∂]; VAR-C3Q2 in A_2).
>    - **𝒟 = una classe parametrica fissata** {L_θ : θ ∈ Θ} (per esempio iψ_t = −ψ_xx + V(t,x)ψ con V in una classe dichiarata): l'oggetto è l'insieme dei compatibili θ_0 + ker Φ_u (VAR-T1(a)).
>    - **Classi strutturate L7–L9:** l'oggetto canonico è la coppia ((𝒟·u, u), ρ_u), dove ρ_u(Q) = Qu/u su {u ≠ 0} è la mappa residuo (VAR-T1).
>
>    *Avvertenza (VAR-N1).* Se i coefficienti stanno in un campo 𝒦 chiuso per derivazione che contiene u_t/u e u_x/u, la coppia (𝒦[∂]·u, u) è vacua: per ogni u senza zeri 𝒦[∂]/Ann(u) ≅ 𝒦u, e Ann(u) contiene sempre operatori di ordine 1. Per questo la scrittura «(D·u, u) (coeff. variabili)» senza anello dichiarato non definisce un oggetto canonico.

*Motivazione.* GATE8 §3.1, testualmente. Esempi della vacuità in `work/S10-INT/ESEMPI.md`: EX10-b (𝒦 = ℂ(x, e^{2it}), (∂_x + x − √2α)u = 0) ed EX10-c (𝒦 = ℂ(tanh x), (∂_x + tanh x)u_b = 0).

---

## P2. GATE3.md, §2, «Raccomandazione del coordinatore» («componente = fattore» per i sistemi)

**Vecchio** (GATE3.md, §2, fine del paragrafo «**Raccomandazione del coordinatore:**»):

> Non propongo di rimodellare oltre la struttura C/P.

**Nuovo** (la frase vecchia resta; si aggiunge un capoverso subito dopo):

> Non propongo di rimodellare oltre la struttura C/P.
>
> *Portata di «componente = fattore»* (revisione limitata di Gate 8b, punto 2).
> - **Scalare:** invariato. C12-T1′ (n = 2, Ω semplicemente connesso, N = R/(Q_i, Q_j) di lunghezza finita δ(P)) resta come approvato.
> - **Sistemi** (L6; oggetto M_u = R^{1×k}/Ann(u), non ciclico): siano U_i := U_{Q_i} ⊇ U_P i moduli delle righe dei fattori e N := R^{1×k}/(U_1 + U_2). Allora Sol(Q_1) + Sol(Q_2) = Sol(P) ⇒ U_1 ∩ U_2 = U_P su ogni Ω (SYS-S1(i⇒)). Il viceversa vale **solo sotto Ext¹_R(N, 𝒜) = 0** (SYS-S1(i⇐)), per esempio su Ω convesso, oppure per N di lunghezza finita con H¹_dR(Ω) = 0, oppure banalmente per N = 0 (fattori comassimali). Senza questa ipotesi il viceversa è FALSO, anche su Ω semplicemente connesso (SYS-S1-C: dominio a U, N ≅ R/(ξ) di lunghezza infinita). L'ambiguità è Sol(N), di dimensione ℓ(N) (SYS-S1(ii)).

La frase «*componente = fattore* resta (approvata al Gate 1, ora dimostrata)» del primo periodo **non cambia**: la restrizione compare come «portata», nello stile delle «Precisazioni di portata» di PROBLEM.md, così il testo approvato dall'utente il 26/10 resta letterale.

---

## P3. GATE3.md, coda della sezione «ESITO DEL GATE 3» (registrazione della revisione)

**Vecchio** (ultima riga del file):

> - Residui MINOR non bloccanti (recepimenti in coda e claim non auditati fuori dal cammino critico, §4) passano alla verifica di integrazione della Fase 5.

**Nuovo** (la riga vecchia resta; se ne aggiunge una):

> - Residui MINOR non bloccanti (recepimenti in coda e claim non auditati fuori dal cammino critico, §4) passano alla verifica di integrazione della Fase 5.
> - **Revisione limitata (Gate 8b, GATE8 §3; applicata in Fase 10 su proposta di S10-INT):** §2 punto 1 con l'anello dei coefficienti dichiarato e ρ_u per L7–L9 (VAR-N1); «componente = fattore» per i sistemi solo sotto Ext¹(N, 𝒜) = 0 (SYS-S1(i⇐), SYS-S1-C FALSO). C12-T1′ scalare invariato. Nessun'altra parte di Gate 3 è toccata.

---

## P4 (consigliata, a discrezione del coordinatore). PROBLEM.md, «Decisione di struttura (Gate 3 …)»

PROBLEM.md ripete in sintesi il testo di Gate 3. Se si applicano P1 e P2, conviene allinearlo; altrimenti PROBLEM e GATE3 divergono.

**Vecchio** (PROBLEM.md, sezione «## Decisione di struttura (Gate 3, approvata dall'utente il 26/10/2026)», primo periodo):

> Oggetto canonico: il modulo ciclico M = R·u ≅ R/Ann(u) (coeff. costanti), la coppia (D·u, u) (coeff. variabili).

**Nuovo:**

> Oggetto canonico, con l'anello dei coefficienti dichiarato (revisione limitata di Gate 8b): il modulo ciclico M = R·u ≅ R/Ann(u) in ℂ[∂] (coeff. costanti); la coppia (𝒟·u, u) con 𝒟 = ℂ(x)[∂] o A_n, oppure l'insieme θ_0 + ker Φ_u in una classe parametrica fissata; per L7–L9 la coppia ((𝒟·u, u), ρ_u). In un campo di coefficienti chiuso per derivazione (D·u, u) è vacuo (VAR-N1).

**Vecchio** (stessa sezione):

> Componente = fattore (dimostrato, punto 2).

**Nuovo:**

> Componente = fattore (dimostrato, punto 2, scalare: C12-T1′ invariato); per i sistemi solo sotto Ext¹(N, 𝒜) = 0 (SYS-S1(i⇐); SYS-S1-C FALSO senza).

---

## P5. research/SYNTHESIS-2.md, §0, punto 2, voce (b′) (ATTACK-8 O17)

**Vecchio** (SYNTHESIS-2.md, riga 10, dall'inizio della voce fino a «(VAR-T1)»):

> - (b′) **identificazione strutturata**: a forma dell'equazione fissata (es. iψ_t = −ψ_xx + V(t,x)ψ) V è identificato esattamente, anche se dipende dal tempo, ⟺ la mappa residuo ρ_u(Q) = Qu/u è iniettiva sulla classe (VAR-T1):

**Nuovo:**

> - (b′) **identificazione strutturata** (senso ID-res): a forma dell'equazione fissata (es. iψ_t = −ψ_xx + V(t,x)ψ), **fuori dalle fasce di silenzio, in (SF)** (classe delle soluzioni forti di S8-VAR; ATTACK-8 O17), V è identificato esattamente, anche se dipende dal tempo, ⟺ la mappa residuo ρ_u(Q) = Qu/u è iniettiva sulla classe (VAR-T1). Per V(t,x) il criterio è int Z(u) = ∅ (V continuo) oppure |Z(u)| = 0 (V ∈ L^∞) (VAR-T1(c)); con int Z(u) ≠ ∅ c'è una fascia di silenzio e la forma senza questa ipotesi è FALSO (VAR-T1(c)-F, serie di Tychonoff):

Il resto della riga resta com'è, salvo la sottopatch facoltativa P5′.

### P5′ (facoltativa; coerenza con ATTACK-8 O8 e GATE9 §3, O31)

**Vecchio** (stessa riga 10):

> V = (iu_t + u_xx)/u su {u ≠ 0}, stabile Lipschitz da C^{1,2} (VAR-P3).

**Nuovo:**

> V = (iu_t + u_xx)/u su {u ≠ 0}, con modulo di Lipschitz da C^{1,2} sui compatti dove |u| ≥ κ (VAR-P3: stima di modulo, **non** certificato di robustezza; ATTACK-8 O8, GATE9 O31).

*Motivazione.* GATE8 §5 chiede solo P5. P5′ allinea la stessa frase alle decisioni già prese (VAR-P3 «DIMOSTRATO come stima di modulo», riga LEDGER 220; rinomina δ → κ, riga 411). La applica il coordinatore se lo ritiene opportuno.

---

## Controllo di coerenza

| testo | dopo la patch | coerente con |
|---|---|---|
| GATE3 §2.1 | anello dichiarato; ρ_u per L7–L9; avvertenza VAR-N1 | NOTAZIONE v6 «Anello dei coefficienti»; ALGORITMO_ESTESO §1 (Output) e §3c |
| GATE3 §2, raccomandazione | scalare invariato; sistemi sotto Ext¹ = 0 | NOTAZIONE v6 «Sistemi»; ALGORITMO_ESTESO §6 (Ipotesi, Fallimenti) |
| PROBLEM, decisione di struttura (P4) | come GATE3 | idem |
| SYNTHESIS-2 §0.2(b′) | «fuori dalle fasce di silenzio, in (SF)» | riga LEDGER VAR-T1(c) («fuori dalle fasce di silenzio, in (SF) (ATTACK-8 O17)»); ALGORITMO_ESTESO §3c |

Nessuno stato di claim cambia per effetto di queste patch: sono patch di portata e di testo.
