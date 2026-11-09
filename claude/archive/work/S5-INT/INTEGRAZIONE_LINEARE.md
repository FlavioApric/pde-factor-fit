# INTEGRAZIONE_LINEARE — S5-INT · Fase 5, parte 1 (pacchetto lineare, Fasi 1–3)
Data 26/10/2026 · Sessione S5-INT · Piano: work/S5-INT/PLAN.md · Scrive solo in work/S5-INT/ e inbox/. **Nessun file di altre sessioni né il LEDGER è stato modificato**: tutto ciò che segue è una proposta.

**Skill caricate** (lettura integrale dei SKILL.md; nessuno script `_vendor` eseguito): skills-local/session-protocol (per primo), skills-local/claim-lifecycle (vocabolario degli stati, righe LEDGER), skills-local/spec-sync (passo 3: definizioni superate nei PROOF_PACKAGE → AVVISI proposti), `_vendor/Auto-claude-code-research-in-sleep/skills/proof-checker` (**solo** la checklist di coerenza: DAG delle dipendenze, registro delle ipotesi con il punto in cui ciascuna è scaricata, tabella dei simboli tipizzata, categorie HIDDEN_ASSUMPTION / REFERENCE_MISMATCH / SCOPE_OVERCLAIM, severità a due assi FATAL/CRITICAL/MAJOR/MINOR), `_vendor/scientific-agent-skills/skills/scientific-critical-thinking` (separare ciò che è provato da ciò che è assunto; ogni rilievo con luogo, osservazione, conseguenza, rimedio).
**SymPy:** non usato: nessuna verifica di questa sessione richiede calcolo simbolico (i due lemmi proposti in §3.4 hanno prove brevi, da far auditare).
**Fonti lette:** RIPRESA.md (aggiornamenti fino a "/goal ... Fase 5"), PROTOCOLLO, NOTAZIONE v1–v3, PROBLEM (G★′, punto 2 riformulato, decisione di struttura, G★′-NL), GATE3, LEDGER (intero, 78 righe), ROUTES; work/{C3,C1C2,II,P1,P2,P3,P4}/PROOF_PACKAGE.md (sezioni con gli enunciati e le prove dei teoremi sul cammino critico, tabelle stati), LEDGER/VERDETTO per SCOUT-TROP; work/CHECK/AUDIT_C3-T2a.md, AUDIT_gammaN.md, AUDIT_P4-L7.md, AUDIT_R2-T3.md; research/CIT-AUDIT/AUDIT-2.md, AUDIT-3.md (riepiloghi), AUDIT-4 (via inbox/central.md).

**Scala di severità** (proof-checker, asse stato × impatto): **CRITICAL** = falso, o non giustificato su un teorema principale; **MAJOR** = vero solo con ipotesi più forti / conclusione più debole di come è scritto in un documento di sintesi (GATE3, PROBLEM, LEDGER) o non giustificato su un claim secondario; **MINOR** = notazione, riferimento, dipendenza non dichiarata, testo non allineato, senza effetto sulla verità; **INFO** = osservazione.

## 0. Sintesi
1. **Nessun teorema principale cade.** Lungo tutte le catene di dipendenza dei sette teoremi richiesti (C3-T1, C12-T1′, P1-T2, P2-T3/P2-C2, P3-T1/T3, P4-T2, P4-T6) le ipotesi dei lemmi usati sono scaricate nel contesto d'uso. Nessun rilievo FATAL o CRITICAL. Nessuna strada torna "active" per incompatibilità (§3.5).
2. **La composizione verso G★′ si spezza in quattro punti** (tutti di portata, nessuno di verità), che i documenti di sintesi (GATE3 §1, PROBLEM G★′, alcune righe LEDGER) non dichiarano o dichiarano in parte (§3.3, rilievi MAJOR INT-4, INT-10, INT-16, INT-18):
   - **R-1 fattori → termini:** lo strato "termini" (P1-T2, P1-P3) richiede Ω **rettangolo**, u ∈ **𝔅**, e fattori della forma **τ − a_j(ξ)** con a_j distinti (oppure fattori comassimali). Per fattori con molteplicità ≥ 2 o di grado ≥ 2 in τ non comassimali, l'esistenza della scomposizione in 𝔅 è APERTA (P1-Q2) e il quadro P1-D3 non è definito.
   - **R-2 spazio dei dati:** il livello 1 vale in D′ ⊇ H^m; il livello 2 vale in D′/C^∞ e in H^m solo con somma chiusa (γ > 0) **e** densa (densità APERTA, P2-Q1); il livello 3 vale solo in 𝔅 ed è **non continuo** in H^m (P1-P1(e)). Lo stesso u ∈ H^m(Ω) non attraversa la catena.
   - **R-3 modello di dato:** la complessità O(N) di E_int (P1-T3) è provata nel modello M1 (EP), dove l'identificazione nell'anello intero **non vale mai** (C3-C2): nel modello M1 la catena deve passare per l'identificazione relativa a una classe (C3-T4(b), C3-T2(c)); nel modello M3 manca un algoritmo (C3-Q1 parziale).
   - **R-4 quadri di Dyson e bordo:** P3-T1(a),(b) e P3-T3 vivono su L²(ℝ) o su (0,L) con Dirichlet, non nel quadro di G★′ (Ω limitato senza condizioni al bordo); con i livelli 1–2 compongono solo tramite 𝔅 (P3-T1(c), P3-T4).
3. **Non vacuità della catena:** manca nel LEDGER un enunciato che mostri che le ipotesi cumulate sono soddisfacibili insieme (u ∈ 𝔅, identificante, con fattori τ − a_j). Propongo il lemma **S5-L1** (§3.4, prova breve, da auditare): u = Σ_j ∫₀¹ e^{a_j(ζ)t+ζx}dζ.
4. **Notazione:** 24 collisioni o sinonimi (§2), i più pericolosi: **N** = numero di termini (P1, NOTAZIONE) ma numero di fattori in γ_N; **S** = semigruppo ma anche mappa somma (P2, C12-P7), che in C12-T1/P1-D2 si chiama Σ; **P_i** = fattore irriducibile ma anche proiettore ortogonale (P2-C2(e)); **E^mult** con due definizioni (v2 forma invertibile; v3/P1-D3 differenza); **c_F** (Friedrichs, modulo l'intersezione) contro ‖P_iP_j‖ (Dixmier) in P2-C2(e); **B** con sei significati; Ω con cinque quadri diversi non dichiarati in NOTAZIONE (v2 H1 dice ancora "rettangolo o convesso"). Proposta: NOTAZIONE v4 (§2.3).
5. **Residui:** nessuno dei fix MINOR di S-CHECK-7 e S-CHECK-8 è recepito nei PROOF_PACKAGE (C2-1, C2-2, P7-1..4, T2a-1, L7-1, L7-2, LD-1); l'AVVISO P1-Q5 è recepito solo in parte; la verifica CIT-AUDIT-2 di Malgrange non è recepita in work/C3 (C3-P1[gen] ancora "CON-FONTE da verificare"). Diverse intestazioni e tabelle stati sono indietro rispetto al LEDGER (§4).
6. **LEDGER:** 23 righe incoerenti, incomplete o duplicate (§5, L-1…L-23), nessuna con uno stato sbagliato in senso matematico; tre con stati fuori vocabolario ("DIMOSTRATO (bozza)", "APERTO-con-prova", "PARZIALE").

---
## 1. Coerenza delle ipotesi lungo le catene di dipendenza

### 1.1 C3-T1 (identificazione) — ipotesi scaricate
| lemma usato | ipotesi del lemma | contesto d'uso in C3-T1 | esito |
|---|---|---|---|
| C3-L2 (I = G·J, V(J) finito, Nullstellensatz) | I ≠ 0 ideale di ℂ[τ,ξ] | I = Ann(u) ∋ P ≠ 0 | ✔ |
| Fatto (V) (sostituisce Fulton §1.6 Prop. 2) | f, g senza fattori comuni | P_i, P_j irriducibili non associati; Q e P_i coprimi | ✔ |
| C3-L3(a)–(e) | Ω aperto **connesso**, w ∈ D′(Ω) | Ω connesso (ipotesi di T1), w_i = (P/P_i)(∂)u ∈ D′ | ✔ |
| C3-L3(d) Passo 3 | proprietà di fascio di D′ (Hörmander ALPDO I «2.2.1», numero NON verificato, CIT-AUDIT-2 #3b) | standard, non portante | INFO |
| Fatto (F) (V(P_i) infinito) | P_i irriducibile, quindi non costante | include il caso P_i ∈ ℂ[ξ] [F-1] | ✔ |
| (d) divisione euclidea | **P monico in τ** | ipotesi esplicita di (d) | ✔ |
Spazio: u ∈ D′(Ω) ⊇ H^m(Ω): coerente con G★′ (H1). Dominio: nessuna ipotesi oltre la connessione; la limitatezza non serve. **Nessun mismatch.**
Valle: C3-T6 (Ω connesso, Ann ≠ 0) ✔; P4-T2 (Ω connesso) ✔; P4-P1 (Ω connesso **e** s.c., per C12-T1′) ✔; P4-T4(iii), P4-T6 (applicano C3-T1(a),(b) con P fattorizzato in irriducibili **su ℂ**) ✔ — **ma** P4-L7 applica C3-T1(a) a fattori dichiarati irriducibili in K[τ,ξ] senza dire che lo sono in ℂ[τ,ξ] → INT-14 (L7-1, MINOR: vero perché K = ℚ̄ è algebricamente chiuso).

### 1.2 C12-T1′ (scomposizione per fattori) — ipotesi scaricate
| lemma | ipotesi | uso | esito |
|---|---|---|---|
| C12-L3(a)–(c) | f, g ∈ R∖0 coprimi | Q_i = P_i^{m_i}, Q_j coprimi | ✔ |
| C12-L1′(c′),(d′) | Ω aperto, H¹_dR(Ω) = 0; (d′) Ω connesso **non vuoto** | Ω di T1′ | ✔ |
| C12-L2′(1)–(3) | Ω connesso non vuoto, H¹_dR = 0, dim M < ∞ | M = R/(Q_i,Q_j), finito per L3(a) | ✔ |
| Weibel Thm 2.7.6 (bilanciamento Ext) | R-modulo qualsiasi | — | ✔ (verificato su fonte secondaria, CIT-AUDIT-2) |
| "s.c. ⇒ H¹_dR = 0" | Lee ISM cap. 11 (numero non verificato) | unica direzione usata | INFO (classica, non portante) |
Spazio D′ / C^∞. **Nessun mismatch.** Osservazioni:
- **INT-2 (INFO).** PROBLEM.md G★′ punto 2, P1-D2 e GATE3 dicono "Ω limitato, connesso e semplicemente connesso": la **limitatezza non serve** a T1′; serve solo per "EP ⊂ H^m(Ω)" e per C12-P7. Nessun effetto; va detto dove serve (NOTAZIONE v4, §2.3).
- **INT-3 (MINOR).** Riga LEDGER C12-T1, colonna ipotesi: "convesso in D′ CON-FONTE" è superata da C12-T1′ (che lo dimostra). Idem II-T2(d) ("esistenza della scomposizione, teorema di S-C1C2 / R2-T2 sui convessi") e II-T3 ("Dimensione dell'ambiguità (CON-FONTE, da S-C1C2/R2-T2). Su Ω convesso"): rinviare a C12-T1′(i),(ii), che vale su ogni Ω s.c.
- **INT-3b (MINOR, positivo).** R2-T3(b)–(e) (LEDGER: "Ω convesso", dipende da R2-T1 CON-FONTE Malgrange–Ehrenpreis) si **estende** a Ω ⊂ ℝ² connesso s.c. senza fonte: (b) è C12-T1′(i) per L₁, L₂ coprimi; il conteggio (c) dim Sol(R/J) = dim R/J per J 0-dimensionale è C12-L2′(2). Proposta di riga aggiornata in §5.

### 1.3 P1-T2 (E_int esatto nella classe 𝔅) e la sua composizione
| lemma | ipotesi | uso | esito |
|---|---|---|---|
| P1-L1 (𝔅_ρ Banach, tracce) | Ω = I × J **rettangolo**, I, J **limitati** | idem | ✔ |
| P1-L2 (flussi e^{sA(∂_x)} su B_ρ) | A ∈ ℂ[ξ] | a_n ∈ ℂ[ξ] | ✔ |
| P1-L3 (Cauchy nella classe, unicità) | v ∈ C(Ī; B_ρ), t₀ ∈ Ī | u ∈ 𝔅_ρ ⇒ u ∈ C(Ī; B_ρ′) per P1-L1(d) | ✔ |
| quadro: fattore Q = τ − a(ξ) | grado 1 in τ, monico | ipotesi | ✔ |
P1-T2 da solo: **nessun mismatch**. La composizione con lo strato "fattori" invece è ristretta:
- **INT-4 (MAJOR, SCOPE_OVERCLAIM nei documenti di sintesi).** Per passare da C12-T1′ (componenti u_j ∈ D′(Ω), Ω s.c., fattori Q_j = P_j^{m_j} qualsiasi) a P1-T2 (u ∈ 𝔅(I×J), Q = τ − a(ξ)) servono **insieme**: Ω rettangolo; u ∈ 𝔅; ogni fattore di grado 1 in τ, monico, con m_j = 1, cioè P = ∏_j(τ − a_j(ξ)) con a_j distinti (P1-P2(c), P1-P3), oppure fattori a due a due comassimali (P1-P2(a)). Fuori da questa classe: (i) m_j ≥ 2 (es. (τ−ξ²)²): P1-D3 non è definito; (ii) fattori irriducibili di grado ≥ 2 in τ (Klein–Gordon, telegrafo): solo la forma di Gauss/Wei–Norman di P1-P4 in 𝔅, nessuna formula per termini analoga a P1-T2; (iii) P non monico in τ (es. ξτ − 1): nessuno strato "termini"; (iv) fattori non comassimali di grado ≥ 2: esistenza della scomposizione in 𝔅 APERTA (P1-Q2). GATE3 §1 riga 3 e PROBLEM.md "Decisione di struttura" ("termine = strato dentro il fattore, a tre livelli") non riportano la restrizione. *Rimedio:* aggiungere a GATE3/PROBLEM la clausola "per P = ∏(τ − a_j(ξ)), a_j distinti, o fattori comassimali; u ∈ 𝔅(I×J)".
- **INT-5 (MINOR, dipendenza nascosta da un claim non auditato).** P1-P2(a) (DIMOSTRATO) cita "u_j = E_j(∂)u (C12-P1(b))"; C12-P1 è "prova scritta (non auditata)". *Rimedio:* citare II-T3 (ii)⇒(iv) (DIMOSTRATO) per s = 2 e, per s fattori a due a due comassimali, gli idempotenti del teorema cinese in R/(P) (stessa prova di II-T3).
- **INT-6 (MINOR).** Quadro H^m: P1-D2 dice "Ω = I×J rettangolo" per X ∈ {H^m, 𝔅}; C12-P7 dice "Ω limitato lipschitziano connesso". Allineare (C12-P7 non usa la struttura a prodotto).

### 1.4 P2-T3 / P2-C2 (stabilità, γ_N) e uso in C12-P7
| lemma | ipotesi | uso | esito |
|---|---|---|---|
| P2-T3 | due sottospazi chiusi di un Hilbert | ℋ_j = ker_{H^m(Ω)}Q_j | ✔ se ℋ_j chiusi: giustificazione da riscrivere (P7-2) |
| P2-C2(a)–(d) | N ≥ 2 sottospazi chiusi non tutti nulli | idem | ✔ |
| P2-C2(e) uguaglianza N = 2, (f) | **usa P2-T3(b)** | dichiarato "Nessuna dipendenza da P2-T3" | **INT-7 (MINOR) = C2-1 non recepito** |
| P2-C2(e) stima γ_N ≥ 1 − ‖C‖ | intersezioni a coppie **nulle**, C = (‖P_{ℋ_i}P_{ℋ_j}‖) | nuclei di fattori: ℋ_i ∩ ℋ_j = Sol(R/(Q_i,Q_j)) ≠ 0 appena V(Q_i) ∩ V(Q_j) ≠ ∅ | **INT-8 (MINOR, portata)** |
| C12-P7(c) = P2-C2(b) | prodotto scalare di H^m fissato | non fissato | **P7-3 non recepito (MINOR)** |
- **INT-8.** La condizione sufficiente calcolabile γ_N ≥ 1 − ‖C‖ non si applica direttamente al caso differenziale con intersezioni non nulle, che è il caso generico per fattori non comassimali. Rimedio proposto (lemma **S5-L2**, §3.4): quozientare le intersezioni, che hanno dimensione finita.
- **INT-9 (INFO, noto).** C12-P7(a) richiede chiusura **e** densità; P2-T3/P2-C2 danno solo la chiusura. Densità APERTA in generale (P2-Q1), provata per m = 0 nei trasporti paralleli su convessi limitati (P2-C1(a)). Coerente con PROBLEM.md.
- **INT-9b (MINOR).** Convenzioni: C12-P7 pone γ_N := +∞ se (ker S)^⊥ = 0, P2-C2 esclude il caso "tutti nulli"; e γ_N dipende dal raggruppamento dei fattori (raggruppare Q₂Q₃ in un solo sottospazio cambia γ). Da scrivere in NOTAZIONE v4.

### 1.5 P3-T1 / P3-T3 (Dyson–Phillips, E_int dal bordo)
| lemma | ipotesi | uso | esito |
|---|---|---|---|
| P3-L2(a)–(c),(e) | X Banach, A₀ genera C₀-semigruppo, (H_β) β < 1 | (a) L²(ℝ), (b) L²(0,L) Dirichlet, (c) B_ρ(J) | ✔ |
| P3-L2(d) Miyadera–Voigt | V ∈ 𝓛(X₁, X) | verificato in (a), (b) | ✔ (Engel–Nagel Thm III.3.14, Cor. III.3.15–3.16, CIT-AUDIT-3 primaria) |
| P3-T3 ← P3-T1(b), P3-P1, P3-T2 | **dati modali finiti** (u₀ ∈ span{e_n : n ≤ N}) | dichiarato nel testo di P3 | ✔ |
- **INT-10 (MAJOR, framework, in GATE3).** P3-T1(a) richiede x ∈ ℝ (Ω illimitato in x: compatibile con H0 ma non con H1 "Ω limitato"); P3-T1(b) e P3-T3 richiedono condizioni di Dirichlet, che non fanno parte del dato di G★′. P3 §2 lo dice correttamente ("su Ω limitato senza condizioni al bordo non esiste un operatore di evoluzione su H^m(Ω)"), ma GATE3 §1 riga 3 elenca "P3-T1: Dyson–Phillips converge per ogni t" e "P3-T3: dal bordo Θ(t^{5/4})" come parte del punto 3 di G★′ senza il quadro. *Rimedio:* in GATE3/sintesi finale scrivere "[su L²(ℝ) o (0,L) con Dirichlet]".
- **INT-10b (MINOR).** La definizione E^{mult,(1)} := S^{(1)}u₀ − tS₀(t)Vu₀ (P3-P1) è la derivata in ε dell'errore di splitting con ordine "prima S₀, poi il flusso di V"; nel caso Dirichlet il flusso del solo trasporto non è un semigruppo su L²(0,L) senza una condizione di inflow (P3-T3(vi) lo identifica con il flusso di inflow di P1-P6). Va detto accanto alla definizione, e in NOTAZIONE v4 (§2.3, voce E_int).
- **INT-11 (MINOR).** LEDGER: P3-T3 e la riga collettiva P3 hanno "dipende da —"; P3-T1 dipende da P3-L2(d) (CON-FONTE, riga propria) e P3-T1(c) da P1-L2; P3-T3 da P3-T1(b), P3-P1, P3-T2. P3-T4(f) e P3-T5 usano la base di Appell di **C12-T6** (non auditato), però solo come definizione (v_n(t,·) = e^{ta(∂)}(x−x₀)^n): INFO.

### 1.6 P4-T2 (modulo ciclico, σ_p)
| lemma | ipotesi | uso | esito |
|---|---|---|---|
| C3-L2, Fatto (F) | I ≠ 0 | Ann(u) ≠ 0 (u risolve P) | ✔ |
| C3-L3(a),(c),(e) | Ω connesso | idem | ✔ |
| C3-T2(a) (in (v)(b)) | Ω aperto non vuoto (T2a-1: la connessione non serve), z_k distinti, q_k ≠ 0 | idem | ✔ (AUDIT_C3-T2a §3) |
| C3-T1(a) | Ω connesso | idem | ✔ |
Fix T2-4 (bicondizionali falsi) recepito nel testo (§0 punto 3, (vi)). **Nessun mismatch.** INT-12 (MINOR): LEDGER "dipende da C3-T1, C3-T2(a)" senza C3-L2, C3-L3.

### 1.7 P4-T6 (classe decidibile)
| lemma | ipotesi | uso in P4-T6 | esito |
|---|---|---|---|
| P4-L6(a)–(c) | **P monico in τ**, v analitica su Ω connesso, {t₀}×J₀ ⊂ Ω | (H1)–(H3) | ✔ |
| II-L1(b) (dentro P4-L6(b)) | P monico in τ, F R-modulo qualsiasi | F = C^∞(ℝ²) | ✔ |
| P4-L3, P4-L4, P4-L5, P4-P2 | L ∈ K[x]⟨∂⟩, dati in K, (AC) | (H4) | ✔ modulo (AC) |
| P4-P2 → C3-T3(i) | u EP, Ω connesso, maggiorante d′ ≥ d (nota T3-2) | G(t,x) = g(x) su (−1,1)×J₀ | ✔ |
| C3-T3(ii) | w₀ ∈ EP | w₀ = G_u(∂)u ∈ EP per P4-T2(iii) | ✔ |
| P4-T4(i) (= prova di C3-P2) | u analitica, Ω connesso, oracoli | oracoli dai Passi 0–1 | ✔ |
| C3-T1(a),(b), C3-T6 | P fattorizzato in irriducibili **su ℂ** | (H1) lo richiede esplicitamente | ✔ |
- **INT-13 (MINOR).** (AC) è "CON-FONTE generico"; la fonte proposta (Cohen, GTM 138, cap. 4) non è verificata (CIT-AUDIT futuro, già in RIPRESA).
- **INT-14 (MINOR) = L7-1, L7-2 non recepiti.** P4-L7 (usato da P4-T5 per la portata "per ogni P") dichiara P_i "irriducibili" in K[τ,ξ] e l'automorfismo Q ↦ Q^A "di K[τ,ξ]", mentre C3-T1(a) è enunciato in ℂ[τ,ξ].
- **INT-15 (INFO, coerenza P4-T5 ↔ P4-T6).** I testimoni di P4-L7 hanno, dopo il cambio di coordinate razionale A, dati di Cauchy D-finiti (λ_je^{x²}, annullati da ∂ − 2x) sulla retta non caratteristica A{t′ = 0}: stanno quindi nella classe decidibile di P4-T6 (nelle coordinate y′). Non c'è contraddizione con P4-T5, perché l'impossibilità riguarda il **modello a scatola nera** (jet + test di zero, nessuna descrizione finita), non la classe di funzioni; la Portata di P4-T5 lo dice. Conseguenza utile (osservazione, da far confermare): l'ipotesi "P monico in τ" di P4-T6 si può sostituire con "dati di Cauchy D-finiti su una retta razionale non caratteristica", per il passo (1) di P4-L7; P4-C4(b) mostra che la fetta va presa trasversale.
- **INT-12b (MINOR).** LEDGER P4-T6 "dipende da II-L1(b)" soltanto: mancano C3-T1, C3-T3, C3-T6, P4-T2(iii), P4-T4(i), P4-L3..L6, P4-P2.

### 1.8 Altre dipendenze nascoste rilevate per via
- **INT-19 (MINOR).** P4-T1(iv) dipende da C3-L1 (non auditato): il testo di P4 lo dice, la riga LEDGER collettiva P4 ("DIMOSTRATO") no.
- **INT-20 (INFO).** C3-T4(b) usa C3-T2(a): quando C3-T4 fu auditato C3-T2(a) era PROVA SCRITTA; ora è DIMOSTRATO (S-CHECK-7): la catena è chiusa a posteriori. Aggiornare "dipende da" di C3-T4.
- **INT-21 (INFO).** II-T2(b′) (⇒) usa "il centralizzatore di una matrice non derogatoria è ℂ[C₀]" con Horn–Johnson, *Topics*, Thm 4.4.17, "numerazione da verificare": fatto standard, ma è un passo portante del caso con polo. Proposta: due righe di prova (una matrice che commuta con una compagna è un polinomio in essa: è determinata dalla sua azione sul vettore ciclico e_k, F1′), oppure CIT-AUDIT.

### 1.9 Riepilogo dei mismatch (sezione 1)
| ID | dove | tipo | severità |
|---|---|---|---|
| INT-4 | fattori → termini (P1-P2/P1-P3 vs C12-T1′); GATE3 §1 r.3; PROBLEM "Decisione di struttura" | SCOPE_OVERCLAIM | **MAJOR** |
| INT-10 | P3-T1(a)(b), P3-T3 fuori dal quadro di G★′; GATE3 §1 r.3 | SCOPE (framework) | **MAJOR** |
| INT-16 | P1-T3 (modello M1) vs C3-C2 (EP non identifica); §3.3 R-3 | composizione per modello di dato | **MAJOR** (nella sintesi) |
| INT-18 | PROBLEM G★′ punto 1 ("tramite V(Ann u)") | OVERSTATED: vale per P ridotto (C3-T1(c)); in generale serve C3-T1(a) o C3-T6 | **MAJOR** (testo approvato; correzione da sottoporre all'utente) |
| INT-3, 3b, 5, 6, 7, 8, 9b, 10b, 11, 12, 12b, 13, 14, 19 | vedi sopra | dipendenze / riferimenti / portata locale | MINOR |
| INT-2, 9, 15, 20, 21 | — | osservazioni | INFO |
**INT-18 (dettaglio).** PROBLEM.md G★′ punto 1: "ricostruire il generatore dell'ideale Ann(u) tramite la sua varietà V(Ann u)". Ann(u) in generale non è principale (Ann(u) = G_u·J_u, P4-T2), e V(Ann u) = V(P) non implica Ann(u) = (P) se P non è ridotto (C3-T1(b) contro (a); es. P = (τ−ξ²)², u = G: V(Ann u) = V(P), Ann(u) = (τ−ξ²) ≠ (P)). Formulazione proposta: "ricostruire G_u = gcd Ann(u) (C3-T6) e decidere Ann(u) = (P) (C3-T1(a)); per P ridotto equivalentemente V(Ann u) = V(P) (C3-T1(c))". Anche "algoritmi polinomiali" (punto 4) va qualificato: P1-T3 è nel modello real-RAM con oracolo exp; C3-A1 non è auditato; la complessità di P4-T6 non è stimata.

---
## 2. Notazione

### 2.1 Simboli con due o più significati
| simbolo | significati (file) | rischio | proposta |
|---|---|---|---|
| **N** | numero di **termini** (NOTAZIONE v1, P1, P2-T2, P3) · numero di **fattori/sottospazi** in γ_N (PROBLEM pt 2, C12-P7, P2-C2) · esponente del Nullstellensatz (C3-L2) · troncamento modale (P3-T3) · grado del testimone N = B + deg P − 1 (P4-T4) | alto: "N = 2 vs N ≥ 3" in PROBLEM si legge come numero di termini | N solo per i termini; numero di fattori **s** (come C12-T1); γ_N → **γ_s** o γ(ℋ₁,…,ℋ_s) |
| **S** | semigruppo S(t), S_n(t) (NOTAZIONE) · **mappa somma** ⊕ℋ_j → H (P2-T3, P2-C2, C12-P7) · sottoinsieme S ⊆ [N] (P1-T2, P1-T3) · S_i (C3-T6) · matrice di Sylvester (C12-L3) · S^{(n)}, S_ε (P3) | alto (S*S e S(t) nello stesso paragrafo di P2-T4/P1-P1(e)) | mappa somma = **Σ** (già in C12-T1, P1-D2): γ = inf σ(Σ*Σ|_{(ker Σ)^⊥}); sottoinsiemi = 𝒮 o A ⊆ [N] |
| **Σ vs S** | stesso oggetto (mappa somma) con due nomi: Σ_X (C12-T1, P1-D2) e S (P2, C12-P7) | concetto con due nomi | unificare in Σ |
| **P_i** | fattore irriducibile (C3, C12, P4) · proiettore ortogonale P_{ℋ_i} (P2-C2(e): C = (‖P_iP_j‖)) · P₁, P₂ fattori coprimi qualsiasi (II-T3) | alto in P2-C2 | proiettori ortogonali = **Π_{ℋ}** |
| **C** | compagna C(ξ) (NOTAZIONE, II) · matrice dei coseni C (P2-C2(e)) · costanti | medio | matrice dei coseni = **𝐂** o K_F |
| **E^mult** | v2: "E_int^mult := S_1⋯S_N^{-1}S" (forma invertibile, scritta in modo ambiguo) · v3 e P1-D3(c): S − S_1⋯S_N (differenza) · P1-D3: 𝔈^mult per la forma invertibile | concetto con due definizioni | E^mult = differenza; 𝔈^mult := (S_1⋯S_N)^{-1}S |
| **E^fatt vs E^ker** | E^fatt_X(P) = ker_XP / im Σ_X (fattori, P1-D2) · E_int^ker = ker L/(ker L ∩ Σ ker L_n) (termini, v2, R2-T3) | stesso schema, oggetti diversi | tenere entrambi con definizione esplicita in v4 |
| **c_F** | coseno di Friedrichs di due sottospazi, modulo l'intersezione (C12-T3, P2-T3, C12-P7(b): c_F(ℋ₁⊖𝓘, ℋ₂⊖𝓘)) · in P2-C2(e) ‖Π_iΠ_j‖ (coseno di Dixmier, = c_F solo se ℋ_i ∩ ℋ_j = 0) | medio | definire c_F e c₀ := ‖Π_iΠ_j‖ in v4 |
| **γ** | γ_N (P2, C12-P7) · γ = 1 − β (P3-L2) · cammino γ (C12-P10) · autovalore minimo della Gram (C12-T3) · γ_m coefficienti (P1-P2) · γ = (∂_t − a_j)h (P1-P2) | basso (locale) | — |
| **B** | 𝔅_ρ(Ω), B_ρ(J) (P1) · maggiorante B ≥ dim(R·u∩EP) (P4-T4) · B(L) (P4-L3) · B_u = ∂_x|_W (P4) · B_j = P/Q_j cofattore (II-T2, P4-P1) · item B8, B2 | medio | maggiorante P4 → **b_EP**; B_u → X_u; cofattore → P̂_j |
| **W** | R·u (P4) · ⊕ℋ_j (C12-P7, P2) | medio | R·u = **M_u** (come PROBLEM "M = R·u"); somma hilbertiana = ⊕ℋ_j |
| **M** | modulo M = R·u (PROBLEM) · modelli di dato M1/M2/M3, M2⁺ · numero di esponenziali (C3-D1, P1-T3) · dimensione del dizionario (NOTAZIONE v1) · costante di semigruppo (P3-L2) · matrice (P1-P2) · M_P, M_sys (II) | medio | modelli di dato: lasciare M1–M3, M2⁺; il resto locale |
| **J** | intervallo J (C12, P1) · J_u (C3-T6, P4-T2) · J_K jet in un punto (C3-P1) · J t-jet (II-L1(b)) · 𝒥 primitiva (C12-L1) | medio | jet: **j_K**, **j_t** |
| **G** | G_u = gcd Ann(u) · G nucleo del calore (C3 S2b, P4 C6d) · G funzione di Green (P1-L4) · 𝔾 Gram | medio in P4 ("G identifica" con G_u nella stessa pagina) | nucleo del calore = **K_t** o 𝒢 |
| **σ** | σ_m(P) simbolo principale (NOTAZIONE, II-P2) · σ_p(u) spettro puntuale (P4) · σ(T) spettro · σ_k esponenti in t (C12, P1) · Sobolev H^σ (C12 §1) | medio: σ_p si legge come simbolo di grado p | σ_p(u) → **spec_p(u)**; esponenti → z_k |
| **ρ** | raggio della classe 𝔅_ρ · radici ρ_k di Δ (P1-P2(c), nella stessa prova di 𝔅_ρ) · ρ_k esponenti in x (C12-L2) · ρ_u restrizione (P4) · mollificatore ρ_ε | medio in P1-P2 | radici → ξ_k |
| **m** | Sobolev H^m · molteplicità m_j (C12, PROBLEM) · grado m di P (P4-L6, P4-L7) · grado totale (II-P2) | medio | Sobolev m; molteplicità **e_j** (come C3/P4); deg P = d_P |
| **e** | molteplicità e_i (C3) · ‖e^{ζx}‖ (P1-P1(e), segnalato nel testo) · e_{(p,q)} esponenziale (C12) · e_k simmetriche elementari (P1-T2) · e_j idempotenti (II-T2, P4) · e_n autovettori (P3) | basso (locale) | — |
| **δ** | δ(P) ambiguità · δ_k = deg q_k (C3-T2) · δ_λ (P4-L3) · δ in TROP · δ MCA | basso | — |
| **F** | R-modulo F (II) · faccia F del poligono (TROP: τ_F) · c_F · F_j Vandermonde | basso | faccia → Φ |
| **E_P / E_j** | E_P = ker P ∩ EP (C3-P1), E_P^K (P4-T5) · E_j proiettore polinomiale (II-T3, C12-P1) | basso | — |
| **R** | anello ℂ[τ,ξ] · R_α regolarizzatore (P2) · R raggio (P1-L2, P1-L4) · R_{≤n} | basso | — |
| **Q_j** | componente primaria P_j^{m_j} (C12, P1-D2, P4) · fattore coprimo qualsiasi (II-T2) · Q generico (C3) | medio: II-T2 non richiede fattori primari | in v4: "Q_j = P_j^{e_j} (componente); fattori coprimi generici: F_1…F_s" |
| **identifica** | assoluto: Ann(u) = (P) (C3-T1, P4) · relativo: dim(Ann(u) ∩ 𝓛) = 1 (C3-D1, C3-L1, C3-T4, P4-T1(ii), G★′-NL pt 2) | medio | due termini: "identifica" e "identifica in 𝓛" |
| **Ω** | rettangolo I×J (C12 §1 default, P1, P2-P5, P2-T2 ⇐) · aperto connesso (C3, P4) · connesso s.c. (C12-T1′, P4-P1, PROBLEM pt 2) · convesso limitato (C12-T3, P2-C1, C3-P1[gen]) · limitato lipschitziano connesso (C12-P7) · NOTAZIONE v2 H1: "I×(a,b) oppure convesso limitato" | alto: v2 H1 è superata e non elenca s.c. | gerarchia esplicita (§2.3) |

### 2.2 Concetti con due nomi o definizioni da allineare
- **EP**: definito (in modo equivalente) in C3 §1 (z_k ∈ ℂ², ⟨z,y⟩), C12 §1 (σ_k t + ρ_k x), P1 §2 (σ_k t + ζ_k x), P4 §1; **assente da NOTAZIONE**. Proposta: definizione unica di C3 §1 in v4.
- **𝔅**: definito solo in P1-D1 (rettangolo limitato); usato in P2, P3 senza richiamo del dominio. Assente da NOTAZIONE.
- **γ_N e c_F**: definiti in C12-P7 / P2-T3 / P2-C2 e citati in PROBLEM.md; assenti da NOTAZIONE.
- **E_int nei vari quadri**: NOTAZIONE v1 (indefinito), v2 (add, mult, log, ker, ⊥, ∥), v3 (A9 non lineare); P1-D3 (formale, add, mult, 𝔈^mult, log, regimi), P1-D2 (E^fatt), P3-P1 (E^{add,(1)}, E^{mult,(1)}), P2 (E^⊥_F), TROP (E_B), Fase 4 (E^NL, E^trop, E^mix). Serve una tabella unica (§2.3).
- **Stati**: NOTAZIONE v2 e claim-lifecycle elencano DIMOSTRATO, CON-FONTE, V-ex, APERTO, FALSO; nei PROOF_PACKAGE è in uso "PROVA SCRITTA (non auditata)", nel LEDGER "APERTO-con-prova", "DIMOSTRATO (bozza)", "PARZIALE", in II "PC-attesa". Proposta: uno stato ufficiale **PROVA SCRITTA** (prova completa, non auditata), che sostituisce i quattro.
- **Molteplicità**: e_i (C3, P4) e m_j (C12, PROBLEM, P1-D2). **Numero di fattori**: r (C3, P4), s (C12, II-T2, P1-D2), k (P1-P2/P3), N (C12-P7, P2-C2).
- **Modelli di dato**: M1, M2, M3 (C3-D1, GATE3), M2⁺ (P4 §6) e "dati modali finiti" (P3-T3): solo il primo gruppo è in GATE3; nessuno in NOTAZIONE.
- **Tempo base t₀** (P1-D3) e **fetta t₀** (P4-L6): stesso simbolo, ruoli diversi (innocuo).

### 2.3 Proposta di testo per NOTAZIONE.md, "Versione 4 (Fase 5, integrazione lineare)" — solo aggiunte
```
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
```

---
## 3. Composizione verso G★′

### 3.1 Teorema di sintesi del caso lineare (proposta S5-SINT; catena di riferimenti al LEDGER, nessuna prova nuova salvo §3.4)
**Ipotesi cumulate.** Coefficienti costanti, R = ℂ[τ,ξ], P = c∏_{j=1}^s P_j^{e_j} non costante, u ∈ D′(Ω) con P(∂)u = 0. Il dominio e lo spazio crescono con il livello:
- (H-1) livello 1: Ω aperto connesso;
- (H-2) livello 2: in più H¹_dR(Ω) = 0 (D′, C^∞); per H^m anche Ω limitato lipschitziano;
- (H-3) livello 3: Ω = I×J rettangolo limitato, u ∈ 𝔅(Ω), e P = ∏_{j=1}^s(τ − a_j(ξ)) con a_j distinti (oppure fattori a due a due comassimali), a_j = Σ_n a_{j,n}.

**(I) Identificazione** [H-1]
- (I.a) Ann(u) = (P) ⟺ (P/P_i)(∂)u ∉ EP(Ω) ∀i — **C3-T1(a)**; V(Ann u) = V(P) ⟺ (P/P_i^{e_i})(∂)u ∉ EP ∀i — C3-T1(b); per P ridotto le due coincidono — C3-T1(c); per P monico in τ, test sul t-jet — C3-T1(d) (= II-C1).
- (I.b) operatore intrinseco G_u = gcd Ann(u), ricostruito da un annullatore qualsiasi con Σe_i test "∈ EP?" — **C3-T6**; struttura spettrale Ann(u) = G_u·J_u, R·u ∩ EP ≅ R/J_u, Ann(u) = (P) ⟺ σ_p = ∅ e G_u ∼ P — **P4-T2**.
- (I.c) per componente [H-2]: Ann(u) = (P) ⟺ Ann(u_j) = (P_j^{e_j}) ∀j — P4-P1 (← C12-T1′, P4-L2).
- (I.d) dati: nessun jet finito certifica Ann(u) = (P) — C3-P1[M2]; nessun dato finito, su Ω convesso — C3-P1[gen] (CON-FONTE Malgrange, verificata); dati EP non identificano mai — C3-C2 (prova scritta); identificazione relativa con dati EP: Bézout — C3-T2(c,d), L2 — C3-T4, L3 — C3-T5; jet di ordine 2d−1 per u EP — C3-T3.
- (I.e) decidibilità: semi-decidibile e riduzione a un maggiorante — P4-T4; impossibile a scatola nera per ogni P — P4-T5 + P4-L7; decidibile per P monico in τ, u analitica, dati di Cauchy D-finiti — P4-T6 (modulo AC); caso olonomo generale APERTO (P4-Q1), minimalità APERTA (P4-Q-min).

**(II) Scomposizione per fattori** [H-2]
- (II.a) ker P = Σ_j ker Q_j in D′/C^∞, ambiguità EP di dimensione δ(P) = Σ_{i<j}dim R/(Q_i,Q_j), unica ⟺ varietà disgiunte — **C12-T1′** (sul rettangolo C12-T1); necessità di H¹_dR = 0 per ogni P — C12-P10.
- (II.b) proiettori: P monico in τ ⇒ Π_j = N_j/r_j, poli = ascisse di V(Q_j)∩V(B_j) — II-T2; polinomiali ⟺ varietà disgiunte, su ogni Ω — II-T3; solo i fattori danno proiettori razionali in ξ — II-T4; Vandermonde per fattori τ − a_j — C12-T2.
- (II.c) H^m: falso in generale — C12-C1; componenti in H^m ∀u ⟺ somma chiusa e densa — C12-P7(a); chiusa ⟺ γ > 0 — C12-P7(c) = P2-C2(b); s = 2: γ = 1 − c_F — P2-T3(b); trasporti paralleli, m = 0 — C12-T3; densità in generale APERTA (P2-Q1); s ≥ 3: c_F a coppie non decidono — C12-P7(d), P2-C2(f).
- (II.d) stabilità: Tikhonov uniforme ⟺ γ > 0, costante γ^{-1/2} ottimale — P2-T3, P2-C2(c); nessuna regolarizzazione lipschitziana di una mappa illimitata — P2-T4.

**(III) Termini dentro i fattori** [H-3]
- (III.a) ogni scomposizione per fattori ha componenti in 𝔅 — P1-P2(c) (comassimale: P1-P2(a)); per ogni fattore flussi intrinseci, u = Σ_S∏(e^{(t−t₀)a_{j,n}} − I)u_j(t₀), E^mult ≡ 0, forma spettrale e_{≥2}(z) — **P1-T2**; somma a due livelli, E_int per termini definito modulo uno spazio di EP di dimensione ≤ δ(P) — P1-P3.
- (III.b) teorema negativo: E^add non si estende con continuità a H^m (avvezione–diffusione, ogni t₀) — P1-P1(e) (riga R5-T2[H^m] FALSO); quindi nessuna regolarizzazione stabile — P2-T4; no-go generale APERTO (P1-Q6).
- (III.c) convenzione continua: decomposizione di bilancio u^{(i)}, continua in H^m, E^add = ΣE^{(i)} — P3-T6(i)–(v); principio di selezione, unicità nella famiglia L₀^Σ — P3-T6(vi′); l'unicità assoluta è FALSA — P3-T6(vi).
- (III.d) termini non commutanti: Lie risolubile ⇒ esatto e globale — P1-T4; non risolubile ⇒ locale — P1-P5; prodotti finiti di flussi impossibili per orbite aggiunte infinite — P1-T5; R5-Q5 come scritta FALSA — P1-C1; perturbazione εx in forma chiusa — P3-T4; Dyson formale per ogni u liscia — P3-L1; Dyson–Phillips globale **[su L²(ℝ) o (0,L) Dirichlet]** — P3-T1; dal bordo **[(0,L) Dirichlet, dati modali finiti]** Θ(t^{5/4}) / O(t²) — P3-T3; regimi di scala **[ℝ]** — TROP-3′, TROP-4.
- (III.e) 2° ordine in t: propagatore e Gauss in 𝔅 — P1-P4; Wei–Norman modo per modo ⟺ Wronskiani — II-T7.

**(IV) Complessità e impossibilità**
- valore di E_int O(M(N+Σd_n)), aggregati O(MN²), tabella Θ(M2^N(L+1)²) **[modello M1, real-RAM con oracolo exp]** — P1-T3 (R5-T2(iv) ristretto);
- A8 per somma di termini falso: ker(L₁+L₂) ∩ (ker L₁ + ker L₂) di dimensione finita — R2-T3; B8 falso fuori dallo spazio EP del fattore — P2-T2; certificati finiti impossibili — C3-P1; scatola nera — P4-T5; regolarizzazione — P2-T4; prodotti di flussi — P1-T5.

### 3.2 Ipotesi cumulate della catena completa (I)→(IV) su un solo dato u
Ω = I×J rettangolo limitato; P = ∏_{j=1}^s(τ − a_j(ξ)), a_j ∈ ℂ[ξ] distinti (quindi P monico in τ, ridotto, fattori di grado 1 in τ); u ∈ 𝔅(Ω) ∩ ker P; per la parte algoritmica: o u ∈ EP (M1, identificazione solo relativa) o u analitica con dati di Cauchy D-finiti (P4-T6, modulo AC). In più, per leggere le componenti in H^m(Ω): γ > 0 e densità (aperta in generale). La catena è **non vacua** per S5-L1 (§3.4).

### 3.3 Dove la catena si spezza
| # | punto | perché | stato | cosa servirebbe |
|---|---|---|---|---|
| **R-1** | (II) → (III) per fattori generali | P1-T2/P1-P3 solo per τ − a_j(ξ) distinti o comassimali; molteplicità ≥ 2 e fattori di grado ≥ 2 in τ non comassimali senza quadro; esistenza in 𝔅 APERTA | **P1-Q2 APERTO**; P1-D3 non definito per Q_j = P_j^{e_j}, e_j ≥ 2 | P1-Q2 (via Ehrenpreis in spazi di tipo esponenziale, o C12-A1 + P1-L4); una definizione di "termini" per fattori (τ − a)^e (sistema di Jordan, II-L1) |
| **R-2** | spazio | (I) in D′ ⊇ H^m; (II) in H^m solo con γ > 0 e densità; (III) solo in 𝔅, non continuo in H^m | teorema negativo P1-P1(e) (scelta del Gate 3, livello ii) | nulla da riparare: va dichiarato; P2-Q1 (densità) resta il buco di (II) |
| **R-3** | modello di dato | P1-T3 (costo) è in M1; in M1 Ann(u) ≠ (P) sempre (C3-C2): l'identificazione è solo relativa (C3-T4(b): Σ(deg q_k+1) ≥ n+1; C3-T2(c)); in M3 nessun algoritmo generale | C3-Q1 PARZIALE | dichiarare la catena separatamente per M1 (relativa, costi polinomiali) e per M3/M2⁺ (assoluta, decidibile solo nella classe di P4-T6) |
| **R-4** | Dyson e bordo | P3-T1(a),(b), P3-T3 in quadri (ℝ; Dirichlet) estranei a G★′ | documentato in P3 §2, non in GATE3 | qualificare in GATE3/sintesi finale |
| R-5 | s ≥ 3 con intersezioni non nulle | la stima calcolabile γ ≥ 1 − ‖C‖ richiede intersezioni nulle | — | S5-L2 (§3.4) |
| R-6 | coefficienti variabili (L4) | solo C12-P5 (non auditato), C3-Q2 APERTO, II-T9 CON-FONTE | fuori dal pacchetto dimostrato | il teorema di sintesi è solo a coefficienti costanti |

### 3.4 Due lemmi di raccordo proposti (PROVA SCRITTA in questo file; da auditare prima di entrare nel LEDGER)
**[S5-L1] Le ipotesi (H-3) sono soddisfacibili da un u identificante.** Sia Ω = I×J rettangolo limitato, P = ∏_{j=1}^s(τ − a_j(ξ)) con a_j ∈ ℂ[ξ] distinti, c_j ∈ ℂ∖{0}, e
u(t,x) := Σ_j c_j ∫₀¹ e^{a_j(ζ)t+ζx} dζ.
Allora u ∈ 𝔅(Ω), P(∂)u = 0 e Ann(u) = (P).
*Prova.* (1) u_j := c_j∫₀¹e^{a_j(ζ)t+ζx}dζ risolve (∂_t − a_j(∂_x))u_j = 0 (derivazione sotto il segno, integrando liscio su [0,1]×Ω̄). ∂_t^i∂_x^l u_j = c_j∫₀¹a_j(ζ)^iζ^l e^{…}dζ, quindi |∂_t^i∂_x^l u_j| ≤ |c_j| |a_j|(1)^i e^{|a_j|(1)T₁+X₁} con T₁ = sup_I|t|, X₁ = sup_J|x|, e ‖∂_t^i∂_x^lu_j‖_{L²(Ω)} ≤ C ρ^{i+l} con ρ := max(1, |a_j|(1)): u_j ∈ 𝔅_ρ(Ω) (P1-D1). (2) Per C3-T1(a) (P ridotto: P_i = τ − a_i, irriducibili e non associati perché a_i ≠ a_j), basta w_i := (P/P_i)(∂)u ∉ EP(Ω). Si ha (τ − a_l)(∂)u_j = c_j∫(a_j − a_l)(ζ)e^{…}dζ, quindi w_i = c_i∫₀¹h_i(ζ)e^{a_i(ζ)t+ζx}dζ con h_i := ∏_{l≠i}(a_i − a_l) ≢ 0 (i termini j ≠ i si annullano perché contengono il fattore τ − a_j). (3) Se w_i ∈ EP(Ω), dim R·w_i < ∞ (C3-L3(c)) e quindi esiste q ∈ ℂ[ξ]∖0 con q(∂_x)w_i = 0 (polinomio minimo di ∂_x su R·w_i). Fissato t ∈ I, F_t(x) := ∫₀¹q(ζ)h_i(ζ)e^{a_i(ζ)t}e^{ζx}dζ è intera in x ∈ ℂ e nulla sull'intervallo J, quindi identicamente nulla; in particolare F_t(iy) = 0 per ogni y ∈ ℝ, cioè la trasformata di Fourier della funzione continua a supporto compatto g := q h_i e^{a_i(·)t}1_{[0,1]} è nulla, dunque g = 0 q.o. e q h_i ≡ 0 su [0,1]: impossibile per due polinomi non nulli. Quindi w_i ∉ EP per ogni i e Ann(u) = (P). ∎
*Osservazioni.* (a) La rappresentazione spettrale di P1-T2(iii) si applica con μ₀ = misura di Lebesgue su [0,1] (supporto compatto): E^add_{int,j} = c_j∫₀¹e_{≥2}(z_j(t−t₀,ζ))e^{a_j(ζ)t₀+ζx}dζ, esplicito. (b) Il lemma risponde alla domanda "esistono dati identificanti nella classe dove lo strato termini è esatto?": sì, e non sono EP (coerente con C3-C2). (c) Non serve SymPy: ogni passo è un'applicazione diretta di C3-T1(a), C3-L3(c), P1-D1.

**[S5-L2] Criterio calcolabile per s ≥ 3 fattori con intersezioni non nulle (raccordo P2-C2(e) ↔ C12-P7).** Siano ℋ_1,…,ℋ_s ⊂ H chiusi con F_j := Σ_{i≠j}(ℋ_i ∩ ℋ_j) di dimensione finita (vero per i nuclei di fattori coprimi: ℋ_i ∩ ℋ_j = Sol(R/(Q_i,Q_j)), C12-T1′(ii), C12-P7). Siano ℋ_j′ := ℋ_j ⊖ F_j. Allora (i) ℋ_i′ ∩ ℋ_j′ = 0 per i ≠ j; (ii) Σℋ_j = Σℋ_j′ + ΣF_j; (iii) Σℋ_j è chiusa ⟺ Σℋ_j′ è chiusa; quindi P2-C2(e) applicato agli ℋ_j′ dà la condizione sufficiente γ(ℋ_1′,…,ℋ_s′) ≥ 1 − ‖𝐂′‖, 𝐂′ = (‖Π_{ℋ_i′}Π_{ℋ_j′}‖), per la chiusura di Σℋ_j.
*Prova (schizzo).* (i) ℋ_i′ ∩ ℋ_j′ ⊆ (ℋ_i ∩ ℋ_j) ∩ F_j^⊥ ⊆ F_j ∩ F_j^⊥ = 0. (ii) ℋ_j = ℋ_j′ ⊕ F_j (F_j ⊆ ℋ_j chiuso). (iii) "⇒" no: va provato. [fix CIT5-4, S5-FIX: la citazione di Kato IV §5.2 (sede non verificata, research/CIT-AUDIT/AUDIT-5.md #4) è sostituita dal lemma di AUDIT-5 §2.3.] *Lemma.* Siano X, Y spazi di Banach, A ∈ ℒ(X,Y) e F ⊂ Y di dimensione finita con A(X) + F = Y. Allora A(X) è chiuso in Y. *Prova.* Sia F′ ⊆ F un complemento algebrico di A(X) ∩ F in F, così che Y = A(X) ⊕ F′. Z := X/ker A × F′ è di Banach; S([x], f) := Ax + f è lineare, limitata e biiettiva Z → Y (se Ax + f = 0 allora f ∈ A(X) ∩ F′ = 0 e Ax = 0); per il teorema della mappa aperta è un isomorfismo topologico, e A(X) = S(X/ker A × {0}) è chiuso. ∎ *Applicazione.* Y := V + F con F := ΣF_j, chiuso in H per ipotesi di "⇒", quindi di Hilbert; X := ⊕ℋ_j′ (somma hilbertiana), A := Σ′, (x_j) ↦ Σx_j, limitato; A(X) = V, A(X) + F = Y, dim F < ∞: il Lemma dà V chiuso. "⇐": V chiuso ⇒ V + F chiuso (somma di un chiuso e di un sottospazio di dimensione finita). ∎ *Stato:* PROVA SCRITTA (schizzo), da auditare; non usata altrove.
*[fix S5L2-1, S5-FIX3] (v) — portata, forma corretta.* (Questo testo non contiene una clausola (v): la portata è stata aggiunta come (v) nella versione completa di work/OP-FUN/PROOF_PACKAGE.md §6, e lì l'audit S-CHECK-14 l'ha trovata FALSA in generale. La correzione si registra anche qui.) (v) La condizione ‖𝐂′‖ < 1 è solo sufficiente e forza V somma diretta: se esiste una relazione (y_j), y_j ∈ ℋ_j, Σy_j = 0, le cui parti y_j′ := y_j − Π_{F_j}y_j ∈ ℋ_j′ sono **non tutte nulle e sommano a 0**, allora ‖𝐂′‖ ≥ 1 e il criterio tace (esempio: τ, ξ, τ − ξ sul rettangolo, dove Π_{F_j} è la stessa media per tutti i j). **La sola esistenza di relazioni non generate dalle intersezioni a coppie non basta:** controesempio in ℝ³, ℋ_1 = ⟨e_1, e_3⟩, ℋ_2 = ⟨e_2, e_3⟩, ℋ_3 = ⟨e_1 + e_2 + 2e_3⟩: F_1 = F_2 = ⟨e_3⟩, F_3 = 0, relazioni di dimensione 2 (quelle generate dalle coppie: dimensione 1), eppure ‖𝐂′‖ = 1/√3 < 1. *Stato vigente (claims/LEDGER.md, S-CHECK-14):* S5-L2 **DIMOSTRATO** per (i)–(iv) e per (v) corretta (prova completa in work/OP-FUN §6); (v) nella forma "relazione non generata dalle intersezioni a coppie ⇒ ‖𝐂′‖ ≥ 1" **FALSA**. Nessun claim dipende da (v).

### 3.5 Le strade tornano "active"?
Il piano prevede che l'integrazione possa rivelare incompatibilità tra strade che funzionavano da sole. **Non ne ho trovate**: nessun enunciato DIMOSTRATO contraddice un altro, e ogni passaggio tra catene scarica le ipotesi. I punti di rottura R-1…R-6 sono di **portata** (classi in cui la composizione è dimostrata), non di verità. Propongo comunque di registrare in ROUTES.md, sotto RT-2/RT-3 (attive), il sotto-obiettivo **P1-Q2** (scomposizione in 𝔅 per fattori non comassimali di grado ≥ 2 in τ, e quadro "termini" per fattori con molteplicità) come condizione per chiudere R-1; e sotto RT-4 il sotto-obiettivo "catena M1 relativa" (R-3). Decisione del coordinatore.

---
## 4. Residui

### 4.1 Fix MINOR degli audit: confronto audit ↔ testo dei PROOF_PACKAGE (stato al 26/10, verificato con grep e lettura)
| fix | audit | luogo atteso | stato nel testo | chi |
|---|---|---|---|---|
| **C2-1** (dipendenza da P2-T3(b) in P2-C2(e) uguaglianza N = 2 e (f)) | AUDIT_gammaN §7 | work/P2/PROOF_PACKAGE.md §7, riga "Dipendenze" di P2-C2 | **NON recepito**: c'è ancora "Nessuna dipendenza da P2-T3: la prova è autonoma." | S-P2 |
| **C2-2** ("γ_3 ≥ 1" da SS* ≥ I) | AUDIT_gammaN §7 | P2-C2(f), *Non necessità* | **NON recepito**: "blocco per blocco VVᵀ = aaᵀ+bbᵀ+I ≥ I, quindi γ_3 ≥ 1" senza σ(S*S)∖0 = σ(SS*)∖0 | S-P2 |
| **P7-1** ("indipendenti" → solo "densa ⇏ chiusa") | AUDIT_gammaN §7 | work/C1C2 C12-P7(a) | **NON recepito**: "Le due condizioni sono indipendenti" | S-C1C2 |
| P7-2 (chiusura di ker_{H^m}P) | idem | C12-P7 prova (a) | non recepito alla lettera, ma §1 di C1C2 definisce H^σ per σ < 0 (duale di H^{−σ}_0): basta aggiungere il rinvio a §1 | S-C1C2 |
| **P7-3** (prodotto scalare di H^m fissato; γ dipende da esso) | idem | C12-P7(c) o ipotesi | **NON recepito** | S-C1C2 |
| **P7-4** (ε_k > 0; riga "c_F = sup dei blocchi"; esistenza di ℋ₁, ℋ₂ con somma non chiusa) | idem | C12-P7(d) | **NON recepito** (il "Viceversa" è ancora senza rinvio) | S-C1C2 |
| T2a-1 (Ω aperto non vuoto basta per C3-T2(a); q_k ≠ 0 solo per V(Ann u)) | AUDIT_C3-T2a §5 | work/C3 §5 C3-T2, Ipotesi | **NON recepito** (INFO, facoltativo) | S-C3 |
| **L7-1** (irriducibilità dei P_i in ℂ[τ,ξ], richiesta da C3-T1(a)) | AUDIT_P4-L7 | work/P4 P4-L7 enunciato e passo (3) | **NON recepito** | S-P4 |
| **L7-2** (automorfismo Q ↦ Q^A su ℂ[τ,ξ], non solo K[τ,ξ]) | idem | P4-L7 passo (1) | **NON recepito** ("automorfismo K-lineare di K[τ,ξ]") | S-P4 |
| L7-3 ("dati di Cauchy D-finiti" vale rispetto alla retta A{t′=0}) | idem | **LEDGER** riga P4-L7 | in parte: la colonna "stato" lo dice, la colonna "enunciato" no (§5, L-17) | coordinatore |
| LD-1 (dire "decidibile con la procedura di P4-T4(iii), con max(D, deg P) al posto di N") | idem | P4-T4 *Lettura* | recepito nella sostanza ("Ann(u) = (P) ⟺ … R_{≤max(D,deg P)} … (confronto calcolabile per (i))"); manca solo la parola "decidibile" (facoltativo) | S-P4 |
| intestazione P4-L7 "controllo indipendente in attesa" | S-CHECK-8 DONE | work/P4 §6 | **superata** (S-CHECK-8 PASS-con-fix) | S-P4 |
| **AVVISO P1-Q5** ("solo dati modali finiti"; dati generali P3-Q-bordo APERTO) | inbox/S-P1.md, RIPRESA 26/10 | work/P1 righe 5, 42, 327, 354 | **in parte**: riga 354 ha "per dati modali finiti" nell'enunciato del tasso, ma righe 5, 42, 354 dicono "P1-Q5 chiuso al 1° ordine" senza qualifica; P3-Q-bordo non citato; "audit S-CHECK-5 in corso" superato | S-P1 |
| CIT-AUDIT-2 #1a–1b (Malgrange AIF 6, Chap. I §2 Thm 2 p. 292, verificato; Hörmander ICASV Thm 7.6.14) | AUDIT-2 | work/C3: righe 3, 11, 32, 137, 150, 238, 248 | **NON recepito**: C3-P1[gen] ancora "CON-FONTE da verificare" (LEDGER: "CON-FONTE (verificata)") | S-C3 |
| CIT-AUDIT-2 #2b (Fulton §5.3 p. 57, Cor. 3 p. 58) | AUDIT-2 | work/C3 C3-T2(c) [fix T2-2], tabella r. 242 | **NON recepito** ("collocazione da confermare") | S-C3 |
| CIT-AUDIT-2 #6a (Higham Thm 1.12, secondaria) e #5a (Horn–Johnson 2ª ed. Cor. 3.5.4, parziale) | AUDIT-2 | work/II II-P5(a), §13 | **NON recepito** ("numerazione da verificare") | S-II |
| CIT-AUDIT-3 #7 (Rudin FA 10.27 non più usato) | AUDIT-3 | work/P1 tabella §11 riga P1-P4 | **residuo**: "(+ CON-FONTE Rudin FA 10.27)" nella tabella, mentre la prova (fix P4-1) usa l'argomento dei caratteri | S-P1 |
| CIT-AUDIT-3 #1, 2a, 2c, 3 (Rudin RCA 13.11, Hörmander 1.4.5, Lee cap. 11, CLO) | AUDIT-3 | work/C1C2 | recepito ("numero non verificato") | — |
| CIT-AUDIT-4 | AUDIT-4 | solo verdetti di Fase 4 (F4-*, S4-*) | fuori dal perimetro lineare | parte 2 di S5-INT |

### 4.2 Testi e tabelle stati indietro rispetto al LEDGER (nessun effetto sulla verità)
- work/C3: C3-T2(a) "PROVA SCRITTA" (intestazione §5 e r. 221) → DIMOSTRATO (S-CHECK-7); C3-P1[gen] (sopra).
- work/C1C2 tabella §2 riga C12-P7 e prova (c) "(prova scritta, audit in attesa)" → (a), (c), (d) DIMOSTRATO (S-CHECK-7, AUDIT_gammaN).
- work/II tabella 0-bis: II-L1 "PC-attesa" → II-L1(b) DIMOSTRATO (S-CHECK-6); II-C1 = C3-T1(d) (DIMOSTRATO): proporre "DIMOSTRATO (= C3-T1(d))"; II-T2(d) e II-T3 rinviano a "R2-T2 sui convessi" (→ C12-T1′, INT-3).
- work/P2 tabella §1: P2-C2 "prova scritta, audit richiesto", P2-T4 "(in audit)" → DIMOSTRATO (S-CHECK-7).
- work/P3 tabella §1 riga P3-T6(vi′): "nessuna riga LEDGER propria" → la riga esiste.
- work/P4: le intestazioni dei claim dicono ancora "PROVA SCRITTA" (P4-T1, T2, T4, T6, L1–L6, P1, P2, C1–C4); la tabella §11 è allineata; P4-L7 come sopra.
- work/P1 r. 354: "audit S-CHECK-5 in corso" → concluso.

### 4.3 Claim mai auditati (fuori dal cammino critico salvo dove indicato)
- **C3:** C3-L1 (Gram = annullatore nel dizionario; **usato da P4-T1(iv)**), C3-D1, C3-T2(b), C3-C1, C3-C2 (corollario; usato da P4-T5 passo 4 e nella lettura di R-3), C3-P2 (la sua prova è riscritta e auditata dentro P4-T4(i)), C3-P3, C3-P4, C3-P5(a) (prova scritta; **usato da P4-C4(a)**, che il testo dice "DIMOSTRATO condizionatamente"), C3-P5(b) (CON-FONTE da verificare: Petrowsky, Hörmander ALPDO II §11.4), C3-A1.
- **C1C2:** C12-P1 (**usato da P1-P2(a)**, INT-5), C12-P2, C12-P3, C12-P4, C12-L4, C12-T4, C12-P5 (L4, LCLM), C12-D2, C12-T5 (funtore C1.0, Aronszajn), C12-T6 (Appell; usato come definizione da P3-T4(f), P3-T5), C12-P8, C12-P9.
- **II:** II-L1(a), II-T1, II-P2, II-P6, II-P8, II-C1 (= C3-T1(d)), II-P10(b,c), II-T7-cons (i)–(v) (asintotica e (vi) V-ex).
- **SCOUT-TROP:** TROP-5, 6, 7, 8 (LEDGER: "DIMOSTRATO (bozza)", proof-checker "da fare").
- **P1:** P1-E1 (calcolo esplicito, letto da S-CHECK-3 ma non come claim).
- Nessuno in P2, P4 (tutto auditato da S-CHECK-4/6/7/8).
**Dipendenze di claim DIMOSTRATI da claim non auditati:** P1-P2(a) ← C12-P1(b) (rimedio: II-T3); P4-T1(iv) ← C3-L1 (dichiarato nel testo, non nel LEDGER); P4-C4(a) ← C3-P5(a) (dichiarato); P3-T4(f), P3-T5 ← C12-T6 (solo definizione della base, INFO).

### 4.4 Citazioni con numero non confermato (contenuto confermato o standard)
| citazione | usata in | grado | portante? |
|---|---|---|---|
| Rudin, RCA 3ª ed., Thm 13.11 | C12-P10 (Conseguenza, "Ind ≡ 0 ⇒ s.c.") | PARZIALE (contenuto sì) | no (solo la traduzione topologica) |
| Lee, ISM 2ª ed., cap. 11 / cap. 17 | C12-L1′ Oss. 2, C12-P10 | PARZIALE (capitolo) | no |
| Hörmander ALPDO I Thm 1.4.5 (partizione dell'unità), «2.2.1/2.2.4» (fascio) | C12-L1′, C3-L3(d) | PARZIALE / NO | no (fatti standard) |
| Hörmander ALPDO I Thm 3.1.4′ | C3-L3 Fatto (H) | NO | no (sostituito da prova) |
| Cox–Little–O'Shea cap. 3 §5–6 | C12-L3, II-T2(a) | PARZIALE (dipende dall'edizione) | no (prova scritta) |
| Humphreys §4.1 «Cor. A» (teorema di Lie) | P1-T4 | PARZIALE | sì, ma enunciato classico |
| Horn–Johnson *Topics* Thm 4.4.17 (centralizzatore di una non derogatoria) | II-T2(b′) | mai controllato | **sì** (passo (⇒) di (b′); INT-21) |
| Horn–Johnson *Matrix Analysis* §3.5 (Cor. 3.5.4?) | II-T7 | PARZIALE | sì, classico |
| Borel LAG Prop. 14.4 | II-T7 | NO | no |
| Deutsch, Thm 9.35 | (non più usato: P2-T3) | PARZIALE | no |
| Higham Thm 1.12 | II-P5(a) | SÌ (secondaria) | — (testo da aggiornare) |
| Cohen GTM 138 cap. 4 | P4 (AC) | mai controllato | sì (assunzione (AC)) |
| Cauchy–Kovalevskaya (Folland, *Intro to PDE*, cap. 1) | P4-L7 | "CON-FONTE da documentare" | sì, classico |
| Kato, *Perturbation Theory*, I §5.3–5.4 (Riesz) | II-T2(b), II-P5 | mai controllato | no (prova algebrica nel testo) |
| Atiyah–Macdonald Prop. 7.14, 2.4 | C3-L2(iii), II-T1 | mai controllato | sì, classici |
| Kato IV §5.2 (immagine di operatore di codimensione finita è chiusa) | S5-L2 (proposto qui) | da verificare | sì per S5-L2 |
| Hörmander ALPDO II §11.4 (Petrowsky) | C3-P5(b) | "da verificare" | no (claim non auditato) |

---
## 5. Righe LEDGER incoerenti, incomplete o duplicate (proposte; il LEDGER non è stato toccato)
| # | riga (ID) | problema | proposta |
|---|---|---|---|
| L-1 | R2-T3 | ipotesi "Ω convesso", dipende da R2-T1 CON-FONTE; ora C12-T1′ e C12-L2′ danno (b)–(e) su ogni Ω connesso s.c. senza fonte | ipotesi "Ω ⊂ ℝ² aperto connesso con H¹_dR = 0 (in particolare convesso)"; dipende da "C12-T1′(i), C12-L2′(2), Fulton (cap. 3, indici)"; la riga va ricontrollata (una riga di verifica, INT-3b) |
| L-2 | C12-T1 | ipotesi "convesso in D′ CON-FONTE" superata; kill-argument "formale raccomandato" ma C1C2 §11.1 riporta il kill-argument formale (ripresa 2) | ipotesi: "Ω rettangolo (s.c.: C12-T1′)"; kill-argument: "formale, C1C2 §11.1" |
| L-3 | TROP-5,6,7,8 | stato "DIMOSTRATO (bozza)" non è uno stato ammesso; proof-checker "da fare" | "PROVA SCRITTA (non auditata)"; TROP-6 AD V-ex |
| L-4 | II-L1, II-T1, II-P2, II-P6, II-P8, II-C1, II-P10 | stato "APERTO-con-prova" fuori vocabolario; contiene II-L1 di cui (b) è ora riga propria DIMOSTRATO; II-C1 = C3-T1(d) DIMOSTRATO | spezzare: II-C1 → "DIMOSTRATO (= C3-T1(d))"; II-L1(a) e gli altri → "PROVA SCRITTA" |
| L-5 | C3-T2(a) | enunciato "(vedi work/C3 §5)" segnaposto; prova "AUDIT_P4.md" (l'audit è AUDIT_C3-T2a.md, S-CHECK-7); ipotesi "—" | enunciato: "Ann(u) = {Q : Q(z_k+∂)q_k = 0 ∀k}, V(Ann u) = {z_k}"; ipotesi "Ω aperto non vuoto, z_k distinti, q_k ≠ 0"; prova "work/C3 §5 + work/CHECK/AUDIT_C3-T2a.md" |
| L-6 | II-L1(b) | enunciato "(vedi work/II #II-L1)" segnaposto | "J : ker_F P → {(∂_t − C(∂_x))U = 0} biiettiva, per ogni R-modulo F" |
| L-7 | P1-L5 | enunciato "(lemma di S-P1, vedi work/P1 §)" senza sezione | "lemmi formali (Dyson, BCH di base) in 𝒜[[t]]", work/P1 §8 |
| L-8 | C12-P7(b) "⇒" | ID dice "⇒", enunciato dice "⟺"; colonna ipotesi contiene commento; (b) "⇐" non ha riga | unire con C12-P7(a,c,d): "C12-P7(a–d)" DIMOSTRATO (S-CHECK-4 per (b), S-CHECK-7 per (a),(c),(d)) |
| L-9 | C12-P7(a,c,d) | proof-checker "da richiedere" ma auditato (S-CHECK-7, PASS-con-fix P7-1..4) | proof-checker: "S-CHECK-7 26/10 PASS-con-fix(P7-1..P7-4)"; prova + AUDIT_gammaN.md |
| L-10 | P2-C2 | proof-checker "richiesto (S-CHECK-7)" ma fatto; "dipende da —" ma (e),(f) usano P2-T3(b) (C2-1) | proof-checker "S-CHECK-7 26/10 PASS-con-fix(C2-1, C2-2)"; dipende da "P2-T3(b) (solo (e) N = 2 e (f))"; prova + AUDIT_gammaN.md |
| L-11 | P2-T4 (riga collettiva) e P2-T4 (aggiornato) | **duplicato** | tenere solo "P2-T4 (aggiornato)", togliere P2-T4 dalla riga collettiva |
| L-12 | C3-Q1 | stato "PARZIALE"; "regge a condizione di recepire T5-1, T5-2" (recepiti da S-P4 ripresa); proof-checker "richiesto" (fatto: S-CHECK-6) | stato "APERTO (risultati parziali: P4-T4, P4-T5+P4-L7, P4-T6)"; togliere la condizione; proof-checker "S-CHECK-6 (P4)" |
| L-13 | P4-T5 | "serve controllo indipendente" di P4-L7: fatto (S-CHECK-8) | "P4-L7 DIMOSTRATO (S-CHECK-8)" |
| L-14 | P4-T6 | "dipende da II-L1(b)" incompleto | aggiungere C3-T1, C3-T3, C3-T6, P4-T2(iii), P4-T4(i), P4-L3..L6, P4-P2; nota (AC): Cohen GTM 138 da verificare |
| L-15 | riga collettiva P4 | P4-T1 "DIMOSTRATO" senza la riserva su (iv) (← C3-L1, non auditato) | "(iv) condizionato a C3-L1" |
| L-16 | P4-T2 | "dipende da C3-T1, C3-T2(a)" | aggiungere C3-L2, C3-L3, Fatto (F) |
| L-17 | P4-L7 | colonna enunciato "(analitica, dati di Cauchy D-finiti)" è sovradimensionata (L7-3); il package dice "jet in K" | enunciato: "∀P ∈ ℚ̄[τ,ξ] non costante ∃ u reale-analitica vicino a 0, jet in ℚ̄, Ann(u) = (P) (dati di Cauchy D-finiti sulla retta non caratteristica A{t′=0})" |
| L-18 | P1-Q5, P3-Q-bordo (+ P3-Q1, P3-Q2 solo nel package P3) | sovrapposizione: P3-Q2 = P1-Q5 a ε = 1; P3-Q1 ⊂ P3-Q-bordo | P1-Q5: "= P3-Q2 (ε = 1)"; P3-Q-bordo: "contiene P3-Q1" |
| L-19 | P3-T3 e riga collettiva P3 | "dipende da —" | P3-T1 ← P3-L2 (incl. L2(d) CON-FONTE, riga propria), P1-L2 per (c); P3-T3 ← P3-T1(b), P3-P1, P3-T2 |
| L-20 | C3-T4 | "dipende da C3-T1" | aggiungere C3-T2(a) (ora DIMOSTRATO) |
| L-21 | C12-L1′, L2′ | ipotesi "Ω non vuoto": L2′ richiede anche connesso e H¹_dR = 0 (il corollario Ext¹ ≅ H¹_dR vale su ogni aperto) | "L1′(c′): H¹_dR = 0; (d′), L2′: Ω connesso non vuoto con H¹_dR = 0; corollario: ogni aperto" |
| L-22 | II-T9 | prova "#II-T9" senza file | "work/II/PROOF_PACKAGE.md §6 II-T9" |
| L-23 | riga collettiva P1 (P1-P2) | dipendenza da C12-P1(b) non auditato (INT-5) | sostituire la citazione con II-T3 nel package; nel LEDGER "P1-P2(a) ← II-T3" |
Righe di sole note citazioni ("nota citazioni, CIT-AUDIT-2/3"): non sono claim; proposta: spostarle in research/CIT-AUDIT/sources_verified.bib o in una sezione "Citazioni" in fondo al LEDGER.
Nuove righe proposte (stato PROVA SCRITTA, da auditare): **S5-L1** (non vacuità di (H-3)), **S5-L2** (criterio con intersezioni non nulle), **S5-SINT** (teorema di sintesi = catena di riferimenti; nessuna prova nuova oltre S5-L1).

---
## 6. Tabella finale delle azioni
| azione | file | chi |
|---|---|---|
| Qualificare lo strato "termini" (rettangolo, u ∈ 𝔅, P = ∏(τ − a_j) distinti o comassimali) e i quadri di P3-T1/P3-T3 (ℝ, Dirichlet, dati modali finiti) | GATE3.md §1 r. 3, PROBLEM.md "Decisione di struttura" (INT-4, INT-10) | coordinatore |
| Proporre all'utente la correzione di G★′ punto 1 ("G_u = gcd Ann(u); V(Ann u) solo per P ridotto") e la qualifica di "algoritmi polinomiali" (punto 4) | PROBLEM.md (INT-18) | coordinatore → utente |
| Dichiarare la catena per modello di dato (M1 relativa / M2⁺–M3 assoluta) | REPORT_FINALE.md (R-3) | coordinatore |
| NOTAZIONE v4 (§2.3): domini, EP, 𝔅, Σ e γ_s, c_F/c₀, Π_ℋ, tabella E_int, modelli di dato, stato PROVA SCRITTA | NOTAZIONE.md | coordinatore |
| Aggiungere lo stato PROVA SCRITTA | skills-local/claim-lifecycle/SKILL.md | coordinatore |
| Correggere le righe L-1…L-23 (§5); aggiungere S5-L1, S5-L2, S5-SINT come PROVA SCRITTA | claims/LEDGER.md | coordinatore |
| Audit di S5-L1 e S5-L2 (brevi) | work/S5-INT/INTEGRAZIONE_LINEARE.md §3.4 | S-CHECK (revisore nuovo) |
| Recepire C2-1, C2-2; tabella §1 (P2-C2, P2-T4 DIMOSTRATO) | work/P2/PROOF_PACKAGE.md | S-P2 |
| Recepire P7-1, P7-2 (rinvio a §1), P7-3, P7-4; tabella §2 e prova (c) di C12-P7 (DIMOSTRATO); unificare S → Σ in C12-P7 | work/C1C2/PROOF_PACKAGE.md (+ gram.md §2bis) | S-C1C2 |
| Recepire T2a-1; C3-T2(a) DIMOSTRATO; C3-P1[gen] CON-FONTE verificata (Malgrange AIF 6, Chap. I §2 Thm 2 p. 292; Hörmander ICASV Thm 7.6.14); Fulton §5.3 p. 57 / Cor. 3 p. 58 | work/C3/PROOF_PACKAGE.md | S-C3 |
| Recepire L7-1, L7-2 (LD-1 facoltativo); intestazioni dei claim allineate al LEDGER; P4-L7 "S-CHECK-8 PASS" | work/P4/PROOF_PACKAGE.md | S-P4 |
| P1-Q5: "chiuso al 1° ordine **solo per dati modali finiti**; dati generali P3-Q-bordo APERTO" (righe 5, 42, 354); togliere "Rudin FA 10.27" dalla tabella; "audit S-CHECK-5 concluso"; P1-P2(a): citare II-T3 al posto di C12-P1(b) | work/P1/PROOF_PACKAGE.md | S-P1 |
| II-T2(d), II-T3: rinviare a C12-T1′ al posto di "R2-T2 sui convessi"; tabella 0-bis (II-L1(b), II-C1); Higham 1.12 verificato; II-T2(b′): prova di due righe del centralizzatore, o CIT-AUDIT | work/II/PROOF_PACKAGE.md | S-II |
| P3: tabella §1 riga P3-T6(vi′); ordine dei flussi e flusso di inflow nella definizione di E^{mult,(1)} | work/P3/PROOF_PACKAGE.md | S-P3 |
| CIT-AUDIT-5: Cohen GTM 138 (AC), Cauchy–Kovalevskaya (Folland), Horn–Johnson *Topics* 4.4.17, Atiyah–Macdonald 7.14/2.4, Kato IV §5.2 (S5-L2), Petrowsky (C3-P5(b)) | research/CIT-AUDIT/ | CIT-AUDIT |
| Registrare in ROUTES.md i sotto-obiettivi P1-Q2 (R-1) sotto RT-2/RT-3 e "catena M1 relativa" (R-3) sotto RT-4; nessuna strada torna "active" per incompatibilità | ROUTES.md | coordinatore |
| AVVISI (spec-sync passo 3) dopo NOTAZIONE v4: Ω (v2 H1 superata), E^mult (v2), S per la mappa somma, P_i per i proiettori | inbox/S-P1, S-P2, S-P3, S-C1C2, S-C3, S-II, S-P4 | coordinatore |
| Audit facoltativo dei claim mai auditati usati da claim DIMOSTRATI: C3-L1 (P4-T1(iv)), C3-P5(a) (P4-C4(a)), C12-P1(b) (se non sostituito da II-T3) | §4.3 | S-CHECK |
