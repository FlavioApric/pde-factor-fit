# REPORT FINALE — Fondamenti analitici (Fasi 0–5)
Progetto: teoria analitica dietro l'algoritmo che, da una soluzione esatta u di una PDE 1D, ricostruisce l'operatore L con u ∈ ker L e scompone u in componenti per termine più un termine d'interazione E_int (piano `D:\piano di ricerca.md`).
Coordinatore: sessione centrale. Data di chiusura: 26/10/2026. Stato di ogni enunciato: `claims/LEDGER.md` (v2, vocabolario unificato). Questo report è la sintesi per il passaggio alla sessione fork (Fasi 6–11). Versione 2 (26/10 sera): include la tornata finale OP-F5A…D (§6.2–6.3) e la bibliografia verificata (BIBLIOGRAFIA.md).

> Legenda degli stati: **DIMOSTRATO** = prova completa passata da un revisore indipendente (S-CHECK); **PROVA SCRITTA** = prova completa non ancora auditata; **CON-FONTE (verificata)** = teorema pubblicato con riferimento controllato; **CONDIZIONALE** = dimostrato a meno di un fatto citato non letto; **V-ex** = verificato solo su esempi; **APERTO**; **FALSO** = controesempio verificato.

---
## 1. In una pagina
1. **Identificazione (caso lineare) — risolta come caratterizzazione.** Su ogni aperto connesso Ω ⊂ ℝ², u ∈ D′ con P(∂)u = 0 identifica P (Ann(u) = (P)) se e solo se ciascun (P/P_i)(∂)u non è un esponenziale-polinomio (C3-T1, DIMOSTRATO). La versione "spettrale" corretta è Ann(u) = (P) ⟺ σ_p = ∅ e G_u ∼ P (P4-T2). Nessun dato finito certifica l'identificazione (C3-P1); con un maggiorante di dim(R·u ∩ EP) diventa decidibile, senza no (P4-T4/T5); esiste una classe decidibile esplicita (P4-T6, modulo un'assunzione di calcolo). Per u EP basta il jet di ordine 2d−1 (C3-T3, ottimo).
2. **Scomposizione per fattori — dimostrata nella forma riformulata con l'utente.** Su Ω semplicemente connesso, in D′/C^∞, ker P = Σ ker P_j^{m_j} con ambiguità esponenziale-polinomiale di dimensione esatta δ(P) = Σ_{i<j} dim R/(Q_i,Q_j) (C12-T1′). Falsa su domini con buchi (C12-P10). Non conserva H^m (C12-C1): le componenti stanno in H^m per ogni u ⟺ somma dei nuclei chiusa (γ_N > 0; per 2 fattori ⟺ c_F < 1) e densa (C12-P7, P2-C2). **La densità è ora un teorema su ogni convesso limitato e per ogni P** (OPF5B-T1, DIMOSTRATO mod Hörmander ALPDO II Thm 10.2.1 e Stein, fonti verificate): su convessi resta una sola condizione, γ_N > 0.
3. **Termini dentro i fattori ed E_int — risposta netta, in parte negativa.** Nel caso commutante E_int ha forma chiusa esatta nella classe 𝔅 di tipo esponenziale (P1-T2), calcolabile in O(N) (valore) / O(N²) (ordini) mentre la tabella completa costa Θ(2^N) (P1-T3); ma **non è continua in H^m(Ω)** (P1-P1(e), FALSO R5-T2[H^m]) e quindi non è regolarizzabile stabilmente (P2-T4). L'unica scomposizione per termine continua trovata (bilancio, P3-T6) richiede un principio di selezione esterno.
4. **Non lineare (Fase 4) — la domanda per termine (A9): esatta prima dello shock, esito misto oltre.** Per Burgers E_int^A9 = (t²/2)·anticommutatore dei due termini + … (S4T-T1, DIMOSTRATO) ha forma chiusa al primo ordine in ν prima dello shock (S4T-T2, DIMOSTRATO). Oltre lo shock: in L^∞/H^s E_int ha salti indipendenti da ν, ma questo è forzato dalla definizione A9 (il flusso del solo uu_x fa lo shock); l'unico risultato negativo non forzato riguarda l'errore di splitting E^mult_AB, il cui ordine in ν scende a ≤ 1/2 in L¹ (S4T-T3(iii), DIMOSTRATO mod [F1]); **l'ordine in L¹ di E_int^A9 stesso oltre lo shock è Θ(ν) a t fissato** (OPA-T1, DIMOSTRATO mod [F1], sotto la condizione di non degenerazione (H_t) che vale per esempio per ε sin x): ogni shock contribuisce 4ν log(2cosh(ρ/2)); **uniformemente in t** l'errore L¹ è 2ν log(1/max(|t−t*|, √ν)) + O(ν), quindi sup_{t≤T} = ν|log ν| + O(ν) con coefficiente esatto 1 e costante Γ esplicita al tempo dello shock (OPF5A-T1/T2/C1: DIMOSTRATO, mod [F1] dopo lo shock; tutto (0,T] per dati con una sola nascita di shock come sin x; in generale CONDIZIONALE al lemma di localizzazione L-loc). [F1] è ora ridotto all'unicità di Kružkov (1970, Thm 1 §3, verificata sul testo primario). L'errore di splitting AB è Θ(√ν) (OPF5D-T6, DIMOSTRATO). **La risposta alla domanda per termine è quindi positiva in L¹ anche oltre lo shock, con tasso uniforme esatto.** L'identificazione non lineare è esatta solo **relativa a un dizionario e modulo le conseguenze differenziali di F** (S4ID-T1); "forma chiusa ⇒ non identifica" è un teorema (ALG-P3, S4ID-T4).
5. **Struttura (Gate 3):** oggetto canonico = modulo ciclico R·u ≅ R/Ann(u); matrice compagna = strumento di calcolo; tensore simbolo = invariante geometrico; componente = fattore; strato "termini" a tre livelli.

---
## 2. Percorso e decisioni dell'utente
| fase / gate | esito | file |
|---|---|---|
| Step 0 (skill) | parziale: skill vendorizzate lette come SKILL.md; installazione globale e Mathpix mai fatte; Lean installato in Fase 5 | BOARD.md |
| Fase 1 (ricerca, 15 agenti) + CIT-AUDIT + DEVIL-A | 15/15 REPORT; A8 "somma di termini" FALSO; componenti naturali = fattori | research/*, research/SYNTHESIS.md |
| **Gate 1** (utente) | G★′, A8 = "componente = fattore", H0 = ℝ, H1 = H^m(Ω) limitato | PROBLEM.md |
| Fase 2 | 6 skill di progetto (skills-local/), roster | SESSIONS.md |
| **Gate 2** (utente) | roster approvato | — |
| Fase 3 (8 sessioni + 11 tornate di audit) | pacchetto lineare | work/{C1C2,C3,II,P1,P2,P3,P4,SCOUT-TROP,CHECK} |
| G★′ punto 2 riformulato (utente) | Ω semplicemente connesso; H^m ⟺ γ_N > 0 e densa | PROBLEM.md |
| **Gate 3** (utente) | decisione di struttura approvata, Fase 3 chiusa | GATE3.md |
| Fase 4 sprint di scouting (5 scout) + DEVIL-4 (FAIL sulla v1) + CIT-AUDIT-4 | v2 della proposta | research/F4-*, GATE4A.md |
| **Gate 4a** (utente) | G★′-NL (A9 con flussi dei singoli termini) + S4-TERM, S4-ID, S4-INTEG | PROBLEM.md, NOTAZIONE.md v3 |
| Gate 4b e gate residui di Fase 5 | approvati per delega riferita dalla sessione fork ("tutti i gate approvati automaticamente"), registrazione revocabile | BOARD.md, RIPRESA.md |
| Fase 5 | integrazione (S5-INT, S5-FIX), LEDGER v2, NOTAZIONE v4, CIT-AUDIT-5, formalizzazione Lean (S5-LEAN) | work/S5-*, PBLean_src/ |

---
## 3. Pacchetto di teoremi — caso lineare (Fasi 1–3), stati del LEDGER
### 3.1 Identificazione (G★′ punto 1)
- **C3-T1** DIMOSTRATO: Ω ⊂ ℝ² connesso (necessario), u ∈ D′, P(∂)u = 0: Ann(u) = (P) ⟺ (P/P_i)(∂)u ∉ EP ∀i; V(Ann u) = V(P) ⟺ (P/P_i^{e_i})(∂)u ∉ EP; P ridotto ⇒ equivalenza; P monico in τ ⇒ test sul t-jet (= II-C1, prove indipendenti). Lemmi C3-L2 (I = gcd(I)·J, V(J) finito), C3-L3 (EP ⟺ dim R·w < ∞).
- **C3-T6** DIMOSTRATO: G_u = gcd Ann(u) si ricostruisce da qualsiasi annullatore con il test EP; Ann principale ⟺ G_u(∂)u = 0.
- **C3-T2(a,c,d), C3-T3, C3-T4, C3-T5** DIMOSTRATO: dati EP (soglia di Bézout, non migliorabile in generale), jet di ordine 2d−1, evoluzioni u_t = a(∂_x)u, onda/KG/telegrafo/trave.
- **C3-P1** DIMOSTRATO (jet) / CON-FONTE verificata (dati generali su convessi, Malgrange AIF 6 Chap. I §2 Thm 2): nessun dato finito certifica Ann(u) = (P).
- **P4-T2** DIMOSTRATO: modulo ciclico, spettro dei caratteri V(Ann u), σ_p = V(J_u) finito, R·u ∩ EP ≅ R/J_u; **Ann(u) = (P) ⟺ σ_p = ∅ e G_u ∼ P** (correzione del coordinatore a una formulazione troppo forte: controesempio P = τ, u = e^{x²}).
- **P4-T4/T5/T6, P4-L7** DIMOSTRATO (T6 modulo l'assunzione di calcolo (AC) su ℚ̄): decidibilità con maggiorante; impossibilità a scatola nera senza; classe decidibile. Minimalità del maggiorante APERTA (P4-Q-min). **C3-Q1 PARZIALE.**
- **P4-C1** DIMOSTRATO: a coefficienti variabili l'algebra di Weyl è semplice ⇒ la restrizione a End(R·u) è sempre iniettiva e non identifica (eˣ, 𝓛 = span{1,∂}).
### 3.2 Scomposizione per fattori (G★′ punto 2)
- **C12-T1** (rettangolo) e **C12-T1′** (Ω semplicemente connesso, H¹_dR = 0) DIMOSTRATO; **C12-P10** DIMOSTRATO (forma con premessa sull'indice): falsa su Ω con buchi per qualche P (Laplaciano, log|z−α|²). C12-Q6 APERTO (condizione esatta per P fissato).
- **C12-C1** FALSO l'enunciato "conserva H^m" (perdita esatta di una derivata). **C12-T3, C12-P7(a–d), P2-T3, P2-C2** DIMOSTRATO: H^m globale ⟺ chiusa e densa; chiusa ⟺ γ_N > 0 (N = 2: c_F < 1); per N ≥ 3 i c_F a coppie non decidono (controesempio in Hilbert astratto; per operatori differenziali APERTO, C12-Q2).
- **II-T2, II-T3, II-C2, II-T4, II-P5, II-T7(a–e′)** DIMOSTRATO: proiettori della compagna Π_j = N_j/r_j con poli esatti; polinomiali ⟺ varietà disgiunte; razionali in ξ ⟺ fattori; normalità della compagna (corregge R6-T3/R7-T5, FALSO per m = 2); Wei–Norman globale ⟺ Wronskiani ≠ 0.
### 3.3 Termini ed E_int (G★′ punto 3)
- **R5-T2[𝔅] = P1-T2** DIMOSTRATO; **R5-T2[H^m] = P1-P1(e)** FALSO (non continuità per avvezione–diffusione, ogni m e ogni t₀).
- **P1-T3** DIMOSTRATO: valore O(M(N+Σd)), aggregati per ordine O(MN²), tabella Θ(M2^N(L+1)²) — "B2 O(eⁿ)" vale solo per l'output completo.
- **P1-T4/P5/T5, R5-Q5** : Lie risolubile ⇒ esatto con d funzioni; non risolubile ⇒ locale; nessun prodotto finito di flussi dei termini riproduce e^{t(X+εY)} (P1-T5); R5-Q5 come scritta FALSA.
- **P2-T1..T5, P2-C1** DIMOSTRATO: B8 falso fuori da uno spazio EP finito (avvezione–diffusione: span{1, x−ct, (x−ct)²+2Dt}); regolarizzazione solo nel gauge finito; nessuna regolarizzazione uniformemente lipschitziana di mappe illimitate; MCA ridotta all'ambiguità finita (RT-R1a fusa).
- **P3-T1..T6(i–v), P3-T6(vi′)** DIMOSTRATO: Dyson–Phillips per ogni t (ordine pari dissipativo + perturbazione di ordine minore L^∞; anche Dirichlet; Miyadera–Voigt, Engel–Nagel verificato); E_int dal bordo Θ(t^{5/4}) per dati modali finiti (P3-T3); forma chiusa con εx; duali (Rosenbloom–Widder ⟺ deg Re a(iκ) pari ≥ 2); decomposizione di bilancio. **P3-T6(vi)** FALSO; RT-S2a (Faddeev) PARCHEGGIATA.
### 3.4 Impossibilità registrate
A8 per somma di termini (R2-T3); B8 (P2-T2); continuità di E_int in H^m (P1-P1(e)); regolarizzazione stabile (P2-T4); certificati finiti d'identificazione (C3-P1); scatola nera (P4-T5); restrizione a coefficienti variabili (P4-C1); scomposizione su domini con buchi (C12-P10); fattorizzazione finita dei flussi (P1-T5).

---
## 4. Non lineare (Fase 4, G★′-NL)
### 4.1 Scouting e scelta
Cinque scout (F4-ALG, F4-LIN, F4-INT, F4-LIFT, F4-HOR); DEVIL-4 ha bocciato la prima proposta (nessuna sessione mirava a E_int nel senso A9) e il coordinatore l'ha accolto; CIT-AUDIT-4 ha ridimensionato la novità (ALG-T1 in parte in Scholl et al. 2026; 4ν ln 2 elementare). Decisione (Gate 4a): G★′-NL e tre sessioni.
### 4.2 S4-TERM — E_int nel senso A9 (punto 1)
Audit S-CHECK-11 (44/44; kill-argument sulla versione corretta: WARN). DIMOSTRATO: S4T-T1 jet in t (coefficiente t² = ½Σ T_n′[T_m]; Burgers −ν(u₀u₀‴ + 2u₀′u₀″)t², verificato anche a mano), S4T-T2 forma chiusa prima dello shock al 1° ordine in ν con resto ν²ε²t³, S4T-P3 esplosione a t*, S4T-P5 Fisher–KPP (stima non uniforme in t), S4T-P6, S4T-C1 (nessuna fattorizzazione finita dei flussi, per ogni dato). Oltre lo shock (S4T-T3, mod [F1] Lax–Oleinik = Kružkov): (i),(ii) salti di E^add indipendenti da ν, **forzati dalla definizione A9** (correzione d'inquadramento T3-1); (iii) unico negativo non forzato: liminf ν^{-1/2}‖E^mult_AB‖_{L¹} ≥ 2D√(t/π); (iv) Θ(√ν) — ora DIMOSTRATO senza Kuznetsov (OPF5D-T6). **S4T-Q1 chiuso da OP-ANA (OPA-T1, audit S-CHECK-15):** a t fissato e sotto (H_t), ‖E_int^A9‖_{L¹} = Θ(ν), contributo per shock 4ν log(2cosh(ρ/2)) — risposta positiva; non uniforme in t (OPA-Q1 aperto). KdV–Burgers: jet DIMOSTRATO; resto della correzione dispersiva O((ν+|d|)²) prima dello shock DIMOSTRATO mod (LWP) (OPR2-T5, audit S-CHECK-16).
### 4.3 S4-ID — identificazione relativa a un dizionario (punto 2)
Audit S-CHECK-10 (61/61) e S-CHECK-13 (OP-NL). DIMOSTRATO: S4ID-T1 riduzione esatta 0 → [F]∩V → I(u)∩V → J_u∩ψ(V) → 0 (u solo C^∞, Ω qualsiasi); S4ID-P1: nei dizionari completi la forma letterale del punto 2 è falsa salvo (2,n) ⇒ precisazione "modulo [F] ∩ V" (PROBLEM.md, testo ristretto); S4ID-T2 + OP-T7 (S4ID-K1): per Burgers N-shock criterio completo nel dizionario evolutivo (identifica ⟺ d ≤ N); S4ID-T3 + OP-P14: per KdV N-solitoni ideale principale (Π_N), deg Π_2 = 8 generico (certificato esatto), OP-K15 deg Π_N = (N+2)2^{N−1} ora DIMOSTRATO (OPF5C-T2, §6.2); S4ID-T4 "chiusura + soglia + esistenza". INT-Q1: "no" per dati Schwartz mai analitici (OP-C3′, mod buona posizione), APERTO per dati analitici con tre ostruzioni dimostrate (OP-O5 Airy, OPR2-O8 Painlevé II, OPR2-O9′). Coefficienti variabili (OP-ALG-T4, OPR2-T3): criterio esatto con fattori non simili.
### 4.4 S4-INTEG — lemmi di trasporto (punto 3), audit S-CHECK-9
DIMOSTRATO: lemma della striscia dei cumulanti e raggio F4L-P3 (≥ 2πν/osc(U₀), ottimale; anche su (0,L)); ALG-L1/T1/P3/P4/P6 (u analitica); MODREL-T1; INT-T1 nella classe 𝓗_M; Hirota (E_int a coppie, ∫ = 0, O(N³)); F4LIN-T2. Direzione "identifica" di INT-T1(C) e INT-T2 senza fonti di scattering per M ≤ 3 (OP-P17/P18). Ora (OP-F5D, §6.2): M ≥ 4 e direzione inversa DIMOSTRATI; restano CONDIZIONALI la continuazione unica su Ω limitato (UC), INT-T1(B) [F4⁻] e l'identificazione dei dati misura. **KIEFFER-C DIMOSTRATO**: arXiv:2512.12019 letto dal coordinatore (work/KIEFFER/LETTURA.md): la tesi "raggio infinito" non è dimostrata nel loro testo e la loro stessa eq. (30) ha zeri del denominatore a δ finito per ogni x.

---
## 5. Fase 5 — integrazione e formalizzazione
- **S5-INT:** nessun teorema cade, nessuna incompatibilità fra strade; precisazioni di portata (INT-4, INT-10, INT-16) in PROBLEM.md; **teorema di sintesi S5-SINT** (catena identificazione → fattori → termini → complessità) con sei punti di rottura R-1…R-6; lemmi S5-L1 (le ipotesi cumulate sono compatibili) e S5-L2 (PROVA SCRITTA).
- **S5-FIX:** fix MINOR applicati nei package; **LEDGER v2** adottato (backup v1); **NOTAZIONE v4** appesa.
- **CIT-AUDIT-2…5:** nessun valore di verità cambiato; due passi portanti ora con prova propria; citazioni con numero non confermato elencate (non portanti).
- **Lean 4 + Mathlib (S5-LEAN), riverificato dal coordinatore:** progetto C:\Users\<user>\PBLean (Lean 4.35.0), copia in D:\ProblemaBase\PBLean_src; `lake build` OK (9056 job), nessun `sorry` né `axiom`, tutti i 15 teoremi dipendono solo da propext, Classical.choice, Quot.sound; enunciati formali confrontati con quelli informali da un revisore indipendente (nessun disaccordo). Formalizzati: R5-T2(i) nucleo algebrico (formula di E_int additivo per flussi commutanti); II-T3 (scomposizione comassimale con proiettore esplicito, su ogni anello commutativo e modulo); R2-T2 a livello L0; C12-P2/P3 (riducibilità del fattore quadratico, irriducibilità di τ − a: promossi a DIMOSTRATO); II-P5 per k = 2 (normalità della compagna); II-T3 (i)⟺(ii) via Nullstellensatz. Non formalizzato: C3-L3(b) (manca la libreria di spazi di funzioni). Copertura: il nucleo algebrico dei risultati lineari; la parte analitica (distribuzioni, semigruppi, Sobolev, Ehrenpreis) richiede librerie che Mathlib non ha.

---
## 6. Problemi aperti — chiusura (sessioni OP-ANA, OP-ALG, OP-FUN, OP-NL, OP-R2; audit S-CHECK-12…16)
### 6.1 Chiusi (DIMOSTRATO salvo dove indicato)
| ID | esito | dove |
|---|---|---|
| INT-18 | G★′ punto 1 riscritto attorno a G_u = gcd Ann(u) (applicato in PROBLEM.md sotto delega, revocabile) | PROBLEM.md, work/OP-ALG §5 |
| C3-Q1, P4-Q1 | decidibile nel modello olonomo analitico (OP-ALG-T1, modulo (AC)) | work/OP-ALG |
| P4-Q-min | per decidere basta la risposta (≡ limite sul grado di un testimone); il maggiorante B ≡ G_u, strettamente più forte su qualche dominio; OP-ALG-Q2: vale su ogni dominio (OPR2-L2) | work/OP-ALG, work/OP-R2 |
| C3-Q2, OP-ALG-Q1 | coefficienti variabili: criterio esatto per P monico in ∂_t con fattori non simili; teorema negativo in A_2; controesempio a I = G·J | work/OP-ALG, work/OP-R2 |
| P1-Q2 | strato termini per P qualsiasi (molteplicità: E^mult = 0; grado ≥ 2 in τ: E^mult ≢ 0; non monici: non unicità, formula in 𝒦_K) | work/OP-FUN |
| P1-Q6 | E^add non continua in H^m per ≥ 2 termini non proporzionali; eccezione esatta per termini proporzionali | work/OP-ANA |
| P2-Q1, OPF-Q1 | densità della somma dei nuclei: simmetrie affini contraenti, trasporti paralleli, calore × trasporto (ogni c, ogni m) | work/OP-FUN, work/OP-R2 |
| C12-Q6 | criterio coomologico esatto su Ω non semplicemente connesso | work/OP-FUN |
| P3-Q-bordo | E_int dal bordo: Θ(t^{k/2+3/4}), k = ordine di contatto | work/OP-ANA |
| S4T-Q1 | E_int^A9 oltre lo shock: Θ(ν) a t fissato (mod [F1]) | work/OP-ANA |
| S4T-Q2 | KdV–Burgers: resto O((ν+|d|)²) prima dello shock (mod (LWP)) | work/OP-R2 |
| S4ID-K1 | dimostrata (OP-T7): criterio completo per Burgers | work/OP-NL |
| KIEFFER-C | dimostrato sul testo originale | work/KIEFFER |
### 6.2 Ultima tornata (OP-F5A…D, 26/10/2026; audit S-CHECK-17…20, ognuno con kill-argument sui teoremi principali, tutti sopravvissuti)
| ID | esito | stato (LEDGER) | dove |
|---|---|---|---|
| P1-Q5 (dati compatibili) | coniugazione esatta; ‖E^mult‖ = |c|(Ñ_k/k!)D^{k/2−1/4}√(u₀^{(k)}(0)²+u₀^{(k)}(L)²)·t^{k/2+3/4}(1+O(t^{1/2})), ∀k ≥ 1 | **CHIUSO**, DIMOSTRATO | work/OP-F5A |
| OPA-Q1 | tasso uniforme ν|log ν| + O(ν), coefficiente 1, costante Γ (Pearcey P = 1.188654; Γ(sin) = 2.57495, confermata numericamente) | **CHIUSO** mod [F1] per dati a una nascita di shock; CONDIZIONALE [L-loc] in generale | work/OP-F5A |
| OPA-Q2 | "(H_t) fallisce su un insieme discreto" è FALSO per C²; vale fuori da un chiuso nullo; insieme finito per Morse+(SB); punti tripli: costante 2ν log((Σp_j)²/(p₁p_n)) | **CHIUSO** per la classe aperta Morse+(SB); densità di (SB) CONDIZIONALE (abbozzo) | work/OP-F5A |
| OPF-Q3, P2-Q1 | densità di Σ ker_{H^m}Q_j in ker_{H^m}P, ∀P, ∀Ω convesso limitato ⊂ ℝ², ∀m (non trovato in letteratura in questa forma) | **CHIUSO** su convessi, DIMOSTRATO mod 2 fonti verificate | work/OP-F5B |
| EX-Q1, EX-BES | OP-ALG-T4 per P non monico (forma saturata; criterio di π-torsione); Bessel radiale: u_G = t⁻¹e^{−x²/4t} identifica | **CHIUSO**, DIMOSTRATO | work/OP-F5B |
| OP-K15 | Π_N(k) = polinomio caratteristico di y_N; grado totale (N+2)2^{N−1}; criterio KdV: identifica ⟺ d < (N+2)2^{N−1} | **CHIUSO**, DIMOSTRATO mod Novikov 1974 (verificata) | work/OP-F5C |
| δ_N(K) | 9 valori esatti (computer-assisted, riprodotti indipendentemente); maggioranti ∀N | PARZIALE; OPF5C-Q1 APERTO | work/OP-F5C |
| OP-P17, OP-P18 | Lax e curvatura nulla ∀n; **errore di segno in OP-P18 a n = 0 trovato e corretto** | DIMOSTRATO ∀M | work/OP-F5D, work/OP-NL |
| INT-T1(C), INT-T2 inverse | Novikov per ogni potenziale senza riflessione (centralizzatore); NLS con molteplicità; **la versione senza molteplicità è FALSA** (mod [DP], fonte secondaria verificata) | DIMOSTRATO (INT-T2 a tempo fissato; dinamico mod L9-ZS + (UC)) | work/OP-F5D |
| S4T-T3(iv) | Θ(√ν) per lo splitting AB, da Cole–Hopf; Kuznetsov non più necessario | DIMOSTRATO | work/OP-F5D |
| [F1] | Lax–Oleinik = soluzione di Kružkov | DIMOSTRATO mod Kružkov 1970 Thm 1 §3 (verificata sul testo primario) | work/OP-F5D |

### 6.3 Ancora aperti o condizionali (con risultato parziale e ostruzione documentati)
| ID | problema | stato / ostruzione | dove |
|---|---|---|---|
| INT-Q1 (dati analitici) | KdV, r ≢ 0, u analitica: esiste un'ODE autonoma in x? | APERTO. Nuovo parziale OPF5C-T6: relazioni con origine non singolare ⇒ code esponenziali; ordine ≤ 3 ⇒ 0 o 1-solitone (con decadimento sull'intero getto). Ostruzione residua: relazioni singolari nell'origine, esattamente dove sta la relazione cubica di Airy | work/OP-F5C, OP-NL, OP-R2 |
| OPA-Q1 generale | più nascite di shock | CONDIZIONALE al lemma L-loc (enunciato scritto nell'audit S-CHECK-20) | work/OP-F5A |
| OPA-Q2 densità | densità della classe Morse+(SB) | abbozzo (Sard a parametri finiti) | work/OP-F5A |
| OPR2-Q2′ | cunei con direzioni degeneri | PARZIALE: modello tangente chiuso e diretto (OPF5B-P8); manca la localizzazione al poligono | work/OP-F5B |
| OPR2-Q3 | zoccolo ripetuto, "nessun test finito" | PARZIALE: DIMOSTRATO sotto (I) esistenza di soluzione identificante e (II) | work/OP-F5B |
| OPF5C-Q1 | δ_N(K) per N generale e N < K < 2N−2 | APERTO (congetture δ_N(2N−1) = N+2, δ_N(2N−2) = N+4, δ_N(2N) = N+1) | work/OP-F5C |
| S4ID-P8, OPR2-P7 | asintotica con derivate | CONDIZIONALE [GT-u] (uniformità in x non enunciata da Grunert–Teschl; pista Deift–Zhou 1994) e [Hm] | work/OP-F5D |
| INT-T1(B) | N-solitoni di Hirota senza riflessione | CONDIZIONALE [F4⁻] (fonte primaria in questa forma non trovata; verificato N = 2) | work/OP-F5D |
| domini non convessi | densità di OPF5B-T1 fuori dai convessi | APERTO | work/OP-F5B |
| Step 0 | installazione globale delle skill, Mathpix | decisione dell'utente | BOARD.md |

---
## 7. Mappa dei file
- Stato e decisioni: PROBLEM.md, NOTAZIONE.md (v1–v4), BOARD.md, RIPRESA.md, ROUTES.md, SESSIONS.md, GATE3.md, GATE4A.md, FASE4_SCOUTING.md, claims/LEDGER.md (v2) + backup.
- Ricerca: research/R1–R8, PR-C2a–e, SCOUT-1/2, SYNTHESIS.md, DEVIL/, CIT-AUDIT/ (AUDIT, AUDIT-2…5), F4-*.
- Prove: work/{C1C2, C3, II, P1, P2, P3, P4, SCOUT-TROP, S4-TERM, S4-ID, S4-INTEG, S5-INT, S5-FIX, S5-LEAN}/PROOF_PACKAGE.md; audit in work/CHECK/AUDIT_*.md; SymPy in */sympy/.
- Lean: C:\Users\<user>\PBLean (progetto), D:\ProblemaBase\PBLean_src (copia dei sorgenti). Il tentativo D:\ProblemaBase\PBLean è abbandonato (disco lento; si può cancellare).
- Ultima tornata: work/OP-F5{A,B,C,D}/PROOF_PACKAGE.md (con fix S5-FIX5/6/7 e "Bibliografia verificata"), audit work/CHECK/AUDIT_OP-F5{A,B,C,D}.md + KA_OPF5*.
- **Bibliografia: BIBLIOGRAFIA.md** (112 fonti per tema, stato di verifica, tabella claim → fonte, problemi) e **BIBLIOGRAFIA.bib**.
- Grafo della documentazione: graphify-out/ (vedi §10).

## 8. Limiti onesti
- Novità complessiva modesta: molti mattoni sono classici (Malgrange–Ehrenpreis, Nullstellensatz, Cole–Hopf, IST); il contributo è il pacchetto di caratterizzazioni, i teoremi negativi e i controesempi, con stati verificati.
- I revisori sono subagenti Claude indipendenti, non referee umani; il kill-argument è stato fatto senza Codex.
- Politica delle fonti (decisione dell'utente, 26/10): i risultati possono poggiare su teoremi pubblicati purché la fonte sia verificata. Bibliografia: 112 fonti, 34 con numero di teorema controllato, 75 con contenuto controllato (45 solo nei metadati), 0 non trovate, 3 citazioni errate corrette (Humphreys Cor. B, Gel'fand–Dikii 1976, DLMF 9.7.10). Numeri portanti ancora non controllati: Krantz–Parks Thm 2.3.5 (OP-T1), Cohen GTM 138 per (AC), Hörmander SCV 1.4.4, Runge in Rudin; fonti verificate solo su testo secondario: Hörmander ALPDO II 10.2.1, Stein VI §3.1 Thm 5, KVZ (per [Hm]), Bilman–Buckingham (per [DP]); Tang–Teng verificato sul preprint.
- Interruzioni per limite d'uso API: tutti gli agenti ripresi dai file; nessuna perdita rilevata.

---
## 9. Stato finale (26/10/2026, sera)
- Fix d'audit: tutti recepiti (S5-FIX4 completato dalla sessione parallela; S5-FIX5/6/7 per la tornata OP-F5). Ogni tornata ha il suo REPORT in work/S5-FIX*/.
- Tutti gli enunciati della tornata OP-F5 sono passati da un revisore indipendente con kill-argument; nessun teorema principale è caduto. Errori trovati e corretti dai revisori: L9 di OP-F5C (falso con g ∈ C¹, vero con C²), lacuna in OPF5C-T6(b) (ipotesi sul getto), costante di Pearcey (1.188654), segno in OP-P18.
- Da fare solo se l'utente lo chiede: passaggio alla sessione fork (Fasi 6–11), che nel frattempo ha creato FASE6_SCOUTING.md, GATE6.md, PIANO_FASI_6-11.md, SESSIONS-F8.md, research/F6-* (non toccati da questa sessione).
- Dettagli cronologici in RIPRESA.md.

## 10. Grafo della documentazione (/graphify, 26/10/2026 notte)
- Output: `graphify-out/graph.html` (interattivo, si apre nel browser), `graphify-out/GRAPH_REPORT.md` (audit), `graphify-out/graph.json`.
- Corpus: 391 file (387 documenti, 4 PDF), circa 727k parole; esclusi `_vendor/`, `_tools/`, `PBLean*`, `.venv/`, script e `.bib` (`.graphifyignore`).
- Grafo: 2197 nodi, 5891 archi, 130 comunità. Archi: 93% EXTRACTED, 7% INFERRED, 0% AMBIGUOUS. Le etichette delle comunità sono automatiche: ognuna prende il nome del suo nodo più connesso.
- Nodi più connessi: `claims/LEDGER.md` (86 archi), C3-T1 (79), C12-T1′ (43), INT-T1 (40), S4T-T3 (40), P1-T2 (36), C12-T1 (34), II-T2 (33), OPA-T1 (33), P4-T2 (31).
- Limiti:
  - L'estrazione è stata fatta da 23 subagenti, che sui file grandi (PROOF_PACKAGE, audit, CATALOGO_v2) hanno letto solo intestazioni, tabelle di stato e sezioni iniziali. Il grafo copre quindi i claim principali e le loro dipendenze, non i dettagli interni delle prove.
  - 757 archi duplicati tra chunk sono stati fusi (health check: 0 archi pendenti, 1 self-loop).
  - 321 nodi sono isolati.
  - Il manifest per `--update` non è stato salvato: per aggiornare il grafo serve una ricostruzione completa.
- Il grafo serve a orientarsi. Lo stato dei claim fa fede solo in `claims/LEDGER.md`.
