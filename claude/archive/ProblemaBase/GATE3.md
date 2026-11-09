# GATE 3 — bilancio della Fase 3 e decisioni da prendere (bozza del coordinatore, 26/10/2026)

Piano, Fase 3: *«Gate 3: un pacchetto di teoremi per il caso lineare più la decisione di struttura»*; *«se C3 conclude che l'approccio per componenti non è il migliore, il Gate 3 può rimodellare la struttura C/P, con l'approvazione dell'utente»*.
Fonti: `claims/LEDGER.md` (stato di ogni claim), `PROBLEM.md` (G★′), `ROUTES.md`, `work/*/PROOF_PACKAGE.md`, `work/CHECK/AUDIT_*.md`. Gli stati qui sotto sono quelli del LEDGER al 26/10: DIMOSTRATO = passato dal revisore indipendente S-CHECK.

## 1. Stato di G★′ punto per punto

| Punto di G★′ | Stato | Teoremi chiave (LEDGER) | Cosa resta |
|---|---|---|---|
| **1. Identificazione** | **Caratterizzato** su Ω ⊂ ℝ² connesso; decidibilità **parziale** | C3-T1: Ann(u) = (P) ⟺ (P/P_i)(∂)u ∉ EP per ogni i (Ω connesso necessario). C3-T6: si ricostruisce G_u = gcd Ann(u) da qualsiasi annullatore. C3-T3: per u EP il jet di ordine 2d−1 basta (soglia ottima). C3-P1: nessun dato finito certifica Ann(u) = (P) (jet: dimostrato; dati generali su convessi: Malgrange, fonte verificata). C3-T4/T5: scala L2, L3 (onda, KG, telegrafo, trave). P4-T2: Ann(u) = (P) ⟺ σ_p = ∅ e G_u ∼ P. P4-T6: classe decidibile (P monico in τ, u analitica, dati di Cauchy D-finiti), modulo un'assunzione di calcolo | C3-Q1 nel caso olonomo generale; minimalità del maggiorante di P4-T4 (T5-1); lemma P4-L7 da controllare in modo indipendente; L4 (coeff. variabili): C3-Q2 aperto |
| **2. Scomposizione per fattori** (riformulato con te il 25/10) | **Dimostrato** nella forma riformulata | C12-T1′: su Ω semplicemente connesso, in D′/C^∞, ker P = Σ ker Q_j con ambiguità EP di dimensione δ(P) = Σ_{i<j} dim R/(Q_i,Q_j). C12-P10: falsa su Ω con buchi per qualche P. C12-C1: non conserva H^m. C12-P7 + P2-C2: componenti in H^m ⟺ somma chiusa (γ_N > 0; per N = 2 ⟺ c_F < 1) e densa. II-T2/T3/T4: proiettori della compagna, polinomiali ⟺ varietà disgiunte, razionali in ξ ⟺ fattori | densità in generale (P2-Q1); C12-Q2 (esempio differenziale con N = 3); C12-Q6 (Ω non semplicemente connesso, P fissato); coeff. variabili oltre le ODE (C12-Q5) |
| **3. Termini dentro i fattori, E_int** | **Risposta netta, in parte negativa** | R5-T2[𝔅] = P1-T2: formula esatta di E_int nella classe di tipo esponenziale 𝔅. **R5-T2[H^m] FALSO**: E^add non è continua in H^m per avvezione–diffusione (P1-P1(e)). P2-T4: quindi non è regolarizzabile stabilmente. P1-T4/P5: algebra di Lie risolubile ⇒ esatto con d funzioni; non risolubile ⇒ solo locale. P1-T5: impossibilità per prodotti finiti di flussi dei termini. P3-T1: Dyson–Phillips converge per ogni t. P3-T3: dal bordo Θ(t^{5/4}) (dati modali finiti). P3-T6(i–v): decomposizione "di bilancio" continua in H^m, selezionata da un principio (non da un teorema). TROP-3′/TROP-4: regimi di scala | P1-Q6 (no-go generale), P1-Q7, P3-Q-bordo, P1-Q5 a ε = 1, ⟨∂², x^k⟩ (P1-Q3) |
| **4. Complessità e impossibilità** | **Dimostrato** | P1-T3: valore O(M(N+Σd)), aggregati per ordine O(MN²), tabella completa Θ(M2^N(L+1)²): "B2 O(eⁿ)" è falso salvo per l'output completo. Impossibilità: A8 per somma di termini (R2-T3), B8 (P2-T2), regolarizzazione stabile (P2-T4), certificati finiti (C3-P1), scatola nera (P4-T5), R5-Q5 come scritta falsa | — |
| **5. Modello di dato** | **Fissato** (S-C3 §2) | M1 formula/EP, M2 jet in un punto, M3 u ∈ H^m noto esattamente; complessità per M1/M2 (C3-A1) | M3 con u olonoma = C3-Q1 |

**Bilancio onesto.** Le parti 1, 2, 4, 5 hanno un teorema per il caso lineare a coefficienti costanti. La parte 3 dà una risposta più dura di quanto si sperasse al Gate 1: la scomposizione **per termine** con E_int esiste ed è esatta in una classe di funzioni di tipo esponenziale, ma **non è continua** nello spazio dei dati scelto (H^m su Ω limitato), quindi non è stabile. L'unica scomposizione per termine continua trovata (bilancio, P3-T6) richiede un principio di selezione esterno. Le obiezioni di DEVIL-A al Gate 1 (O1: per le evoluzioni del 1° ordine lo strato "fattori" è banale e tutto il contenuto per termine sta nello strato log-simbolo) si sono confermate.

## 2. Decisione di struttura (piano: "il centro decide la struttura matrice: via a vs b vs simbolo")
Proposta di S-II (`work/II/PROOF_PACKAGE.md` §10), confermata dall'audit e dal lavoro di S-C3/S-P4:
1. **Oggetto canonico, con l'anello dei coefficienti dichiarato** (revisione limitata di Gate 8b, punto 1; NOTAZIONE v6). Ogni enunciato di questo tipo dichiara l'anello 𝒟 in cui si calcola Ann_𝒟(u) = {Q ∈ 𝒟 : Qu = 0}:
   - **𝒟 = ℂ[∂] = ℂ[∂_t, ∂_x]** (coefficienti costanti): l'oggetto canonico è **il modulo ciclico M = R·u ≅ R/Ann(u)**. Contiene l'identificazione (C3-T1, P4-T2: Ann(u) = G_u·J_u, R·u ∩ EP ≅ R/J_u) e la scomposizione (i suoi idempotenti, dopo aver invertito il risultante, sono le componenti per fattore: II-T2).
   - **𝒟 = ℂ(x)[∂] oppure l'algebra di Weyl A_n** (coefficienti razionali o polinomiali): l'oggetto canonico è la coppia (𝒟·u, u), con Ann_𝒟(u) ideale sinistro (VAR-T2a in ℂ(x)[∂]; VAR-C3Q2 in A_2).
   - **𝒟 = una classe parametrica fissata** {L_θ : θ ∈ Θ} (per esempio iψ_t = −ψ_xx + V(t,x)ψ con V in una classe dichiarata): l'oggetto è l'insieme dei compatibili θ_0 + ker Φ_u (VAR-T1(a)).
   - **Classi strutturate L7–L9:** l'oggetto canonico è la coppia ((𝒟·u, u), ρ_u), dove ρ_u(Q) = Qu/u su {u ≠ 0} è la mappa residuo (VAR-T1).

   *Avvertenza (VAR-N1).* Se i coefficienti stanno in un campo 𝒦 chiuso per derivazione che contiene u_t/u e u_x/u, la coppia (𝒦[∂]·u, u) è vacua: per ogni u senza zeri 𝒦[∂]/Ann(u) ≅ 𝒦u, e Ann(u) contiene sempre operatori di ordine 1. Per questo la scrittura «(D·u, u) (coeff. variabili)» senza anello dichiarato non definisce un oggetto canonico.
2. **Via (b), la compagna, = strumento di calcolo**, relativo alla direzione t (serve lc_τ(P) costante): proiettori costruttivi con poli esatti, evoluzione modo per modo, criterio di Wei–Norman (II-T7).
3. **Via (a), il tensore simbolo, = invariante geometrico "all'infinito"**, non struttura: decide dove la (b) è piena e fa da ostruzione ai proiettori polinomiali (II-C2).
4. ⋆-prodotto (RT-R6a): fuso in RT-6, come calcolo.
5. F1 (forma ortogonale Σf(λ)v⊗v) sostituita dalla forma biortogonale; la forma ortogonale vale solo nel caso normale (II-P5).

**Raccomandazione del coordinatore:** approvare 1–5. Inoltre, per la parte 3, registrare come struttura C/P: *componente = fattore* resta (approvata al Gate 1, ora dimostrata), mentre *termine* diventa uno strato **dentro il fattore**, con tre livelli distinti: (i) identità esatta in 𝔅, (ii) non continuità in H^m (teorema negativo), (iii) decomposizione di bilancio continua come scelta di convenzione. Non propongo di rimodellare oltre la struttura C/P.

*Portata di «componente = fattore»* (revisione limitata di Gate 8b, punto 2).
- **Scalare:** invariato. C12-T1′ (n = 2, Ω semplicemente connesso, N = R/(Q_i, Q_j) di lunghezza finita δ(P)) resta come approvato.
- **Sistemi** (L6; oggetto M_u = R^{1×k}/Ann(u), non ciclico): siano U_i := U_{Q_i} ⊇ U_P i moduli delle righe dei fattori e N := R^{1×k}/(U_1 + U_2). Allora Sol(Q_1) + Sol(Q_2) = Sol(P) ⇒ U_1 ∩ U_2 = U_P su ogni Ω (SYS-S1(i⇒)). Il viceversa vale **solo sotto Ext¹_R(N, 𝒜) = 0** (SYS-S1(i⇐)), per esempio su Ω convesso, oppure per N di lunghezza finita con H¹_dR(Ω) = 0, oppure banalmente per N = 0 (fattori comassimali). Senza questa ipotesi il viceversa è FALSO, anche su Ω semplicemente connesso (SYS-S1-C: dominio a U, N ≅ R/(ξ) di lunghezza infinita). L'ambiguità è Sol(N), di dimensione ℓ(N) (SYS-S1(ii)).

## 3. Strade (ROUTES.md) decise dal coordinatore in Fase 3
RT-R1a (MCA) → MERGE; RT-R4a (restrizione / sintesi spettrale) → MERGE in RT-4; RT-R6a (⋆-prodotto) → MERGE in RT-6; [TROP-L2] → merge in RT-2; RT-S2a (Faddeev) → **PARCHEGGIATA** (il MERGE proposto è stato revocato dopo un kill-argument FAIL). Puoi rivederle.

## 4. Cose ancora in corso o da fare prima di chiudere la Fase 3
- S-P4 ha recepito l'audit (bicondizionali falsi rimossi, P4-L7 inserito, P4-Q-min aperto); P4-L7 è DIMOSTRATO (controllo indipendente S-CHECK-8, fix MINOR L7-1..3, LD-1 da recepire). (AC) cita Cohen GTM 138: numero da verificare.
- Recepimenti MINOR in coda: S-P1 (P1-Q5 solo dati modali finiti), S-P2 (C2-1, C2-2), S-C1C2 (P7-1..4), S-C3 (T2a-1).
- Claim scritti ma mai auditati, fuori dal cammino critico: C3-T2(b), C3-L1, C3-P2..P4, C12-T5 (funtore C1.0), C12-T6 (Appell), C12-P8/P9, II-T1, II-P2, II-P6, II-P8, II-C1, II-P10, II-T7-cons.
- Citazioni con numero non confermato (contenuto confermato, non portanti): Rudin RCA 13.11, Hörmander ALPDO 1.4.5/2.2.4, Lee ISM, CLO, Humphreys "Cor. A".
- Step 0 ancora parziale: installazione globale delle skill e chiavi Mathpix, in attesa di te dal 22/10.

## 5. Decisioni che spettano a te
1. Approvi la **decisione di struttura** del §2 (punti 1–5 + lettura a tre livelli dello strato "termini")?
2. Il pacchetto di teoremi del §1 è sufficiente per chiudere la Fase 3, oppure vuoi prima l'audit dei claim non auditati del §4 (o di una parte)?
3. Vuoi riaprire qualcosa nella parte 3 (per esempio cercare uno spazio di dati diverso da H^m in cui la scomposizione per termine sia continua) prima di passare alla **Fase 4 (non linearità)**?
4. Le scelte sulle strade del §3 ti vanno bene?

---
## ESITO DEL GATE 3 (26/10/2026) — decisione dell'utente
- **Approvata** la decisione di struttura del §2 (punti 1–5) e la lettura a tre livelli dello strato "termini" (identità esatta in 𝔅 / non continuità in H^m / decomposizione di bilancio come convenzione).
- **Fase 3 chiusa** con il pacchetto di teoremi del §1.
- Domande 3 e 4 del §5 non decise esplicitamente: default del coordinatore (revocabili) — nessuna riapertura della parte 3 prima della Fase 4; scelte sulle strade del §3 confermate.
- Residui MINOR non bloccanti (recepimenti in coda e claim non auditati fuori dal cammino critico, §4) passano alla verifica di integrazione della Fase 5.
- **Revisione limitata (Gate 8b, GATE8 §3; applicata in Fase 10 su proposta di S10-INT):** §2 punto 1 con l'anello dei coefficienti dichiarato e ρ_u per L7–L9 (VAR-N1); «componente = fattore» per i sistemi solo sotto Ext¹(N, 𝒜) = 0 (SYS-S1(i⇐), SYS-S1-C FALSO). C12-T1′ scalare invariato. Nessun'altra parte di Gate 3 è toccata.
