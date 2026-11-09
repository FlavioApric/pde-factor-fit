# ATTACK-9 — DEVIL-9 contro `ALGORITMO_ESTESO.md` (specifica di Fase 9, S9-ALG)

27/10/2026. Sessione DEVIL-9, avviata dal coordinatore. Piano: `research/DEVIL/PLAN-9.md`.

**Materiale attaccato.** `ALGORITMO_ESTESO.md` (§0–§11, passi 1–8, esempi 9.1–9.5 = L6–L10); `work/S9-ALG/{PLAN,open_questions}.md` e i quattro script in `work/S9-ALG/sympy/`. Riferimenti: `claims/LEDGER.md` (con la tabella delle decisioni del coordinatore al Gate 8, che prevale sulle celle delle righe di sessione), `PROBLEM.md` v3.1 (G★″), `GATE8.md`, `NOTAZIONE.md` v1–v5, `research/DEVIL/ATTACK-8.md`.

**Skill applicate.** `skills-local/claim-lifecycle` (stati e regola di fondamento); kill-argument (`_vendor`, solo lettura, thread di ATTACCO: memo unico, poi obiezioni atomiche). Nessuno script `_vendor` eseguito.

**SymPy/mpmath.** `research/DEVIL/sympy9/devil9_checks.py` → `devil9_checks.out` (vedi §3). Solo verifica.

---

## 1. Memo d'attacco (≤ 250 parole)

La specifica è onesta nei dettagli e sbagliata in due punti strutturali.

Primo: la catena CONV-T7. Il passo 2 (scelta del livello, R4) è sempre di classe (C). Per la regola stessa di §0.4, un passo (C) rende (C) tutto ciò che sta a valle. Quindi ogni uscita del passo 8 è (C), e le promesse di §8 punti 1–2 («certificato (A)/(B)») sono false per costruzione. In più CONV-T7 maggiora distanze con costanti di Lipschitz, ma i passi 1–3 hanno uscite discrete e Ann(·) è discontinuo ovunque (CONV-T3). Va separata la *completezza* (classe (C), condizionata a «livello n, classe K») dalla *correttezza* (catena numerica 4→6, dove CONV-T7 si applica davvero).

Secondo: DM1 = EP e ID-ann. Per un dato EP la varietà di Ann(u) è finita, quindi Ann(u) non è mai (P) (C3-C2, P4-T2). Gli esempi 9.1–9.3 usano dati in forma chiusa non EP, cioè un modello M3-hol che la tassonomia di §0.3 non contiene; e M2⁺ (getto più ideale olonomo, P4-T5/P4-T6) manca anche se il passo 1 lo cita.

Il resto è riparabile: certificazione DM2 inesistente (CONV-T1), fondamenti CON-FONTE non verificati, C3-A1 (PROVA SCRITTA) usato in classe (A), Magnus attribuito alla parte sbagliata di VAR-T10, modi di fallimento incompleti (CONV-D1, C12-P10, OPA-T3, CONV-B1), DM-δ senza norma (VAR-P3), precondizione del Gate 8 (CIT su Oberst) non soddisfatta. L'encoder è usato correttamente come traduzione.

Verdetto proposto: **passa con fix obbligatori** (O1, O2, O3, O4, O14). Nessuna FATAL.

---

## 2. Obiezioni

Legenda: **FATAL** = la specifica va riscritta; **CRITICAL** = da correggere prima del Gate 9, invalida una promessa centrale; **MAJOR** = errore locale con conseguenze su un passo o un esempio; **MINOR** = imprecisione, citazione o costo.

### O1 — CRITICAL — La catena CONV-T7 è (C) per costruzione

- **Claim colpito.** §0.4 («un passo (C) rende (C) tutta la catena a valle»), §2 (passo 2, livello R4, classe (C)), §8 punti 1–2 («uscita certificata (A)/(B)»).
- **Controesempio/Lacuna.** Il passo 2 è sempre (C): nessun algoritmo sa a priori il livello n a cui l'annullatore compare (R4, CONV-T1). Per §0.4 tutte le uscite sono quindi (C), e §8 punti 1–2 contraddicono §0.4. Inoltre il bound della catena d ≤ Σ_i (∏_{j>i} L_j) ε_i richiede uscite metriche e passi lipschitziani; i passi 1–3 hanno uscite discrete (un ideale, un livello, una classe), e Ann(·) è discontinuo in ogni punto (CONV-T3), quindi L_j non esiste. Infine i passi 1–3 non hanno la riga «Contratto».
- **Rimedio.** Trattare i passi 1–3 come *condizionamento* («al livello n, nella classe K»), non come anelli della catena. Applicare CONV-T7 solo alla sottocatena numerica 4→6. Riformulare §8: «completezza (C); correttezza condizionata (A)/(B) al livello e alla classe dichiarati». Aggiungere il «Contratto» ai passi 1–3.

### O2 — CRITICAL — DM1 = EP non dà mai ID-ann

- **Claim colpito.** §0.3 (DM1 = EP), §0.5 e §3a «Senso» (ID-ann in DM1), §8 punto 1.
- **Controesempio/Lacuna.** Per u EP la varietà di Ann(u) è finita, quindi Ann(u) ≠ (P) per ogni P non banale (C3-C2, P4-T2; fix P1-2 di C3-P1). SymPy (B): u = e^{−t}cos x risolve il calore, ma Ann(u) contiene ∂_t + 1 e ∂_x² + 1, che non sono multipli di τ − ξ². Lo stesso accade al dato traslato di L7. Gli esempi 9.1–9.3 funzionano solo perché usano dati in forma chiusa *non* EP (onde di Dirac generiche, Pöschl–Teller, Airy), che non stanno in DM1.
- **Rimedio.** In DM1 ammettere solo ID-ker o l'identificazione relativa in una classe finita (C3-T4, C3-T2(c)). Introdurre esplicitamente un modello «forma chiusa non EP / olonomo» (M3-hol o DM1-cf), che è quello che 9.1–9.3 usano davvero.

### O3 — MAJOR — DM2 «certificato con bound» non esiste

- **Claim colpito.** §1 e §8 punto 3 («DM2 certificato con bound, C3-T3, CONV-T1»).
- **Controesempio/Lacuna.** C3-T3 richiede u EP (quindi ricade in O2). CONV-T1 dice letteralmente che non esiste certificato corretto in DM2, perché K* non è maggiorato da d. SymPy (C): per N = 2, 4, 6 il getto d'ordine N in (0,0) di G(t+1, x) (non EP) coincide con quello di un polinomio del calore v_N (EP). Nessun numero finito di coefficienti distingue i due dati. La specifica stessa, in §0.3, attribuisce a DM2 solo ID-lim: contraddizione interna.
- **Rimedio.** In DM2 dichiarare solo ID-lim, uscita (C). Un bound esiste solo in M2⁺ (vedi O4).

### O4 — MAJOR — Tassonomia DM senza M2⁺ e M3-hol

- **Claim colpito.** §0.3 (elenco DM1, DM2, DM3, DM-φ, DM-inv, DM-δ), passo 1 (cita P4-T5, P4-T6/OP-ALG-T1).
- **Controesempio/Lacuna.** NOTAZIONE v4 elenca M1, M2, M2⁺, M3. P4-T5 e P4-T6/OP-ALG-T1 danno decidibilità esatta, modulo (AC), da getto più ideale olonomo: è M2⁺, non DM2. Il passo 1 lo usa senza che il modello sia nella tassonomia, e §0.3 dice «DM2 solo ID-lim», in contrasto col passo 1.
- **Rimedio.** Aggiungere M2⁺ (getto + ideale olonomo dichiarato) e M3-hol (forma chiusa olonoma) alla tassonomia, con il senso ID-* ammesso in ciascuno.

### O5 — MAJOR — H-DIRAC mal etichettato; il modo di fallimento di L6 è falso

- **Claim colpito.** §3b (H-DIRAC), §9.1(c) («dato EP: rango deficitario»).
- **Controesempio/Lacuna.** La premessa di H-DIRAC è ID-ann, ma il test di rango 8 è un test ID-ker. SymPy (A): con 4 onde piane di Dirac 1+1 (k ∈ {1/2, 1, 3/2, 2}, rami alterni), dunque un dato EP, le righe per modo hanno rango esatto 8, l'SVD puntuale ha rango 8 (valori singolari da 0,367 a 22,3) e la soluzione unica è (A, B) = (−iσ_x, mσ_z). Il fallimento dichiarato non avviene. Il criterio ψ_2 ∉ EP riguarda ID-ann, non il rango.
- **Rimedio.** Separare H-DIRAC-ann (premessa non EP) da H-DIRAC-ker (rango 8, ammesso anche con dato EP a ≥ 4 modi generici). Correggere §9.1(c).

### O6 — MAJOR — La regola di fondamento ammette CON-FONTE non verificati

- **Claim colpito.** §0.1 («fondamento: DIMOSTRATO o CON-FONTE»).
- **Controesempio/Lacuna.** Il LEDGER distingue CON-FONTE (riferimento non verificato) da CON-FONTE (verificata). La specifica fonda passi su: VAR-T6 («da verificare»), DICT-B3 («da verificare»), VAR-P11(e) (Pazy) sotto Dyson in classe (B), VAR-L2-cor, DICT-ILIM via Whitney–Stein («da verificare»).
- **Rimedio.** Richiedere CON-FONTE (verificata) come fondamento, oppure marcare questi passi «condizionati a verifica» con l'elenco esplicito delle citazioni da chiudere.

### O7 — MAJOR — C3-A1 (PROVA SCRITTA) usato in classe (A)

- **Claim colpito.** §7 (C3-A1 in classe (A)).
- **Controesempio/Lacuna.** C3-A1 è PROVA SCRITTA nel LEDGER (la specifica lo riconosce). La correttezza dell'algoritmo fa parte dell'enunciato di C3-A1, quindi un'uscita (A) che dipende da C3-A1 viola §0.1.
- **Rimedio.** Declassare a «(A) condizionato a C3-A1» finché C3-A1 non è DIMOSTRATO, o promuoverlo prima del Gate 9.

### O8 — MAJOR — Trotter–Kato in (B) contro VAR-T10(5); manca la riga nel LEDGER

- **Claim colpito.** §7 (splitting/Trotter–Kato, classe (B)).
- **Controesempio/Lacuna.** VAR-T10(5) colloca splitting e Trotter–Kato per V generico non limitato in classe (C). Trotter–Kato non ha una riga nel LEDGER.
- **Rimedio.** Classe (B) solo per V limitato (o relativamente limitato con ipotesi dichiarate); altrimenti (C). Chiedere al coordinatore una riga LEDGER o togliere la citazione.

### O9 — MAJOR — Magnus attribuito alla parte sbagliata di VAR-T10

- **Claim colpito.** §7 («Magnus limitato ∫‖A‖ < π», attribuito alle parti DIMOSTRATO (1), (3) di VAR-T10).
- **Controesempio/Lacuna.** Il criterio ∫‖A‖ < π è la parte (4), CON-FONTE (Casas, Thm 3.4); per V ∈ L^∞ in dimensione infinita è CON-FONTE condizionata. La parte (3)(iii) è CON-FONTE + V-ex, non DIMOSTRATO. Per una PDE il Magnus (B) è quasi vuoto: nel troncamento finito ‖H‖ cresce con la dimensione, e per Stark (L8) ∫‖A_I‖ = ∞.
- **Rimedio.** Citare VAR-T10(4) con il suo stato; dichiarare che il Magnus (B) vale solo per generatori limitati o troncamenti con ‖H_N‖ τ < π; per L8 classe (C).

### O10 — MAJOR — «Misfit certificato (A)» calcolato con quadratura in virgola mobile

- **Claim colpito.** §4 passo 6 (misfit MF2, classe (A)), §9.5.
- **Controesempio/Lacuna.** Un certificato (A) richiede un'inclusione rigorosa (aritmetica intervallare o bound d'errore della quadratura); la specifica usa `mp.quad` senza bound. SymPy (G): la formula MF2 come rapporto di determinanti di Gram non è calcolabile in mpmath né a 15 né a 30 cifre (eccezione nel `det`, matrice singolare quando l'atomo ∂_t sta nello span, dato che u_t = u_xx). Il residuo per minimi quadrati, invece, è stabile: r_2 ≈ 3,9·10⁻²³ a 15 cifre e ≈ 6,5·10⁻³⁵ a 30 cifre. La mia ipotesi di un misfit spurio a 15 cifre è **smentita**; resta la lacuna formale (nessuna inclusione) e il costo non dichiarato della precisione di lavoro (circa log₁₀(1/λ_min) cifre; l'esempio 9.5 ne usa 25).
- **Rimedio.** Calcolare r_2 con minimi quadrati (QR) e non col rapporto di determinanti; dichiarare la precisione di lavoro come costo; per la classe (A) richiedere un'inclusione rigorosa, altrimenti classe (B).

### O11 — MAJOR — Modi di fallimento del passo 6 incompleti rispetto ai teoremi negativi

- **Claim colpito.** §4 passo 6, «Modi di fallimento».
- **Controesempio/Lacuna.** Mancano: CONV-D1 (in 1+d, d ≥ 2, ambiguità infinita salvo fattori comassimali; rilevante per Lamé/Maxwell in L6); C12-P10 / OPF-T4 (Ω non semplicemente connesso); OPA-T3 / P1-P1(e) (E^add non limitato H^m → L², quindi E_int da dato approssimato è (C)); CONV-B1 (condizioni al bordo invisibili). C12-T1′ non è citato.
- **Rimedio.** Aggiungere questi cinque modi di fallimento, ciascuno con l'etichetta d'uscita (NON-DECISO o classe (C)).

### O12 — MAJOR — Il contratto del passo 5 non ha un esempio che lo rispetti

- **Claim colpito.** §5 (passo 5, traduzione via encoder, costante C_W), §9.2 (L7).
- **Controesempio/Lacuna.** L'esempio 9.2 usa un operatore di Darboux differenziale A: non limitato, con nucleo, e C_W non si applica. Applicato al dato, A trasforma un dato identificante in un dato EP. SymPy (D): il dato di Pöschl–Teller ha annullatore (L_q + 1)(L_q − k²) già nel sottoanello ℂ[∂_t, L_q], cioè non identifica i∂_t − L_q in senso ID-ann neanche prima della traduzione (vale solo ID-res). Se q viene dal passo 3c, la costante di Lipschitz di q ↦ W_q da ENC-1 (C(a, Q, Q′)) non è esplicita, quindi il passo non può essere (B).
- **Rimedio.** Distinguere traduzione limitata (W_q, ENC-1, C_W) da Darboux (non limitata, classe (C), con perdita di identificabilità dichiarata). Rendere esplicita C(a, Q, Q′) o declassare a (C). Correggere il «Senso» di L7 in ID-res.

### O13 — MAJOR — DM-δ senza norma

- **Claim colpito.** §0.3 (DM-δ: «dato a distanza δ»).
- **Controesempio/Lacuna.** La norma non è dichiarata, e VAR-P3 dice che V non è continuo dal dato in C¹. SymPy (F): u = 1 (V = 0) e u_δ = 1 + δ² sin(x/δ) hanno ‖u_δ − u‖_{C¹} ≤ δ + δ², ma |V_δ| raggiunge 1/(1 − δ²) → 1. Un DM-δ in C¹ non dà nessun controllo su V.
- **Rimedio.** Scrivere DM-δ(Y) con la norma Y dichiarata (almeno C² o H^{m} con m ≥ ordine + 1, come in VAR-P3) e propagarla nei contratti.

### O14 — MAJOR — Precondizione del Gate 8 non soddisfatta

- **Claim colpito.** Passo 3b (SYS-EX, SYS-N1, SYS-T0 come «NOTO»).
- **Controesempio/Lacuna.** GATE8 §5: «Prima del Gate 9: CIT su Oberst 1990/1993, Isakov, Andrianov–Sokolov». In `research/CIT-AUDIT/` non c'è CIT-AUDIT-9; Oberst è stato letto solo dall'abstract. Il passo 3b fonda il caso sistemi su risultati letti così.
- **Rimedio.** Fare la CIT prima del Gate 9, oppure marcare il passo 3b «condizionato a CIT Oberst» e tenerlo fuori dalle promesse di §8.

### O15 — MINOR — L'esempio 9.5(c) è vacuo

- **Claim colpito.** §9.5(c) (bound CONV-T4(a): sin ≤ 2δ/ρ).
- **Controesempio/Lacuna.** Con ρ = 0,0131 e δ = 0,00936 si ha 2δ/ρ = 1,43 > 1: il bound non dice nulla, perché sin ≤ 1 sempre. La specifica lo chiama «lasco», ma l'esempio non mostra il teorema in azione.
- **Rimedio.** Scegliere δ < ρ/2, o dichiarare l'esempio come caso vacuo.

### O16 — MINOR — DICT-R6(f) con stato vecchio

La specifica scrive «PROVA SCRITTA → DIMOSTRATO», ma la tabella del LEDGER dà già DIMOSTRATO. **Rimedio:** aggiornare.

### O17 — MINOR — VAR-L2-cor citato senza uso

Nessun passo usa l'osservazione parziale. **Rimedio:** togliere la citazione o aggiungere il passo che la usa.

### O18 — MINOR — ENC-T2 assente dal passo 5

ENC-T2 è il lemma principale dell'encoder, ma il passo 5 non lo cita. **Rimedio:** citarlo con lo stato.

### O19 — MINOR — Ipotesi di LAME-3 incomplete

Mancano λ + μ ≠ 0, μ ≠ 0, ρ ≠ 0. **Rimedio:** dichiararle.

### O20 — MINOR — Ipotesi di H-DIRAC-1/2 non dichiarate

Mancano m ≠ 0 e la base fissata delle matrici. **Rimedio:** dichiararle.

### O21 — MINOR — Citazioni a jolly

«S4T-*» e «OPF-*» nascondono membri CONDIZIONALE, APERTO e V-ex. **Rimedio:** citare gli ID singoli.

### O22 — MINOR — «Bézout su 𝕋» senza ID

È R4-T5[𝕋]. **Rimedio:** citare l'ID.

### O23 — MINOR — P1-T3 fuori posto

Citato nel passo 3a, dove non serve. **Rimedio:** spostarlo al passo in cui si usa o toglierlo.

### O24 — MINOR — C3-T4 è identificazione relativa

C3-T4 dà ID-ker in classe finita, non ID-ann. **Rimedio:** correggere il senso.

### O25 — MINOR — Nessun passo emette NON-DECISO; nessuna regola d'arresto

Il ciclo sui livelli (passo 2) non ha budget né regola d'arresto. **Rimedio:** budget dichiarato in ingresso; uscita NON-DECISO al suo esaurimento.

### O26 — MINOR — §0.5 incoerente

Dice «solo in DM3» e poi «DM1/DM3». **Rimedio:** una sola formulazione (dopo O2: DM3 e M3-hol).

### O27 — MINOR — Etichetta d'uscita mancante

DM-φ produce IDENTIFICATA[ID-fam], che non è nell'insieme delle etichette. **Rimedio:** aggiungerla.

### O28 — MINOR — L9 è banale

SymPy (E): ogni dato a modi finiti soddisfa una legge locale per interpolazione (frequenze ±1, 2: u_t = −2/3 + (1/3)∂_x²). L'indistinguibilità nonlocale/locale nell'esempio non dipende dal teorema citato. **Rimedio:** dichiararlo, o usare un dato a infiniti modi.

### O29 — MINOR — Costi

Il passo 2 conta solo LIN; il passo 5 omette il costo di Goursat; il passo 7 è O(k), non O(k²). **Rimedio:** correggere.

### O30 — MINOR — G★″ non ha un modello di rumore

DM-δ è un'estensione di PROBLEM v3.1 e va dichiarata come tale. **Rimedio:** dichiararlo in §0.3.

### O31 — MINOR — δ sovraccarico

VAR-P3 usa δ come minorante di |u|. **Rimedio:** rinominare (per esempio κ) in VAR-P3.

### O32 — MINOR — C_W molto lasco

SymPy (H): nessun controesempio al bound cosh(a√Q) ≤ C_W = 1 + a²Q e^{a√Q}, ma a a√Q = 5 si ha C_W² ≈ 1,4·10⁷ contro cosh² ≈ 5,5·10³. I certificati trasportati perdono quattro ordini di grandezza. **Rimedio:** usare ‖T‖ ≤ cosh(a√Q) (o il bound di Gronwall esatto) dove disponibile.

### Punti che reggono

- L'encoder è usato come traduzione, non come informazione: nessun passo ricava identificabilità dal solo encoder.
- Tutti gli ID citati esistono nel LEDGER, tranne C3-A1 (la specifica lo riconosce, vedi O7) e Trotter–Kato (O8).
- Gli stati ENC seguono la tabella del coordinatore al Gate 8.
- I quattro script di S9-ALG ripassano tutti (SymPy (R)).

**Conteggio.** FATAL 0, CRITICAL 2, MAJOR 12, MINOR 18 (totale 32).

---

## 3. SymPy/mpmath (`sympy9/devil9_checks.py`)

Esecuzione con `D:\ProblemaBase\.venv\Scripts\python.exe -I`; uscita in `sympy9/devil9_checks.out`.

- **(R)** I quattro script di S9-ALG ripassano: 7/7, 11/11, 5/5, 10/10 PASS.
- **(A)** L6, dato EP a 4 modi di Dirac: rango esatto 8, SVD rango 8, soluzione unica (−iσ_x, mσ_z). Smentisce §9.1(c) (O5).
- **(B)** u = e^{−t}cos x: annullato da ∂_t + 1 e da ∂_x² + 1 (O2).
- **(C)** Getti d'ordine 2, 4, 6 di G(t+1, x) riprodotti da polinomi del calore (O3).
- **(D)** Pöschl–Teller: (L_q + 1)(L_q − k²)u = 0 e (i∂_t + 1)(i∂_t − k²)u = 0 (O12).
- **(E)** Modi ±1, 2: legge locale interpolante u_t = −2/3 + (1/3)∂_x² (O28).
- **(F)** ‖u_δ − u‖_{C¹} ≤ δ + δ², |V_δ| = 1/(1 − δ²) (O13).
- **(G)** MF2 come rapporto di Gram: non calcolabile a 15 e 30 cifre; r_2 per minimi quadrati 3,9·10⁻²³ (15 cifre), 6,5·10⁻³⁵ (30 cifre); 2δ/ρ = 1,43 (O10, O15). L'ipotesi di un misfit spurio a 15 cifre è smentita.
- **(H)** cosh(a√Q) ≤ C_W per a√Q ∈ {0,5; 1; 3; 5}; C_W² fino a 1,4·10⁷ (O32).

Esito complessivo: rilancio finale in corso al momento della consegna; il conteggio N/N PASS è nell’ultima riga di `devil9_checks.out`. Run precedente: (R), (A)–(G) completati con i valori sopra; (H) non ancora eseguito per un errore di regex, ora corretto.

---

## 4. Proposta per il Gate 9

**Passa con fix obbligatori.** Nessuna obiezione FATAL: l'architettura a passi, l'uso dell'encoder e il sistema di etichette reggono. Prima del Gate 9 vanno corretti:

1. O1 — riformulare §0.4 e §8: completezza (C), correttezza condizionata; CONV-T7 solo su 4→6.
2. O2, O4 — rifare la tassonomia DM (DM1 senza ID-ann; aggiungere M2⁺ e M3-hol) e il «Senso» di 9.1–9.3.
3. O3 — DM2 solo ID-lim, nessun certificato.
4. O14 — CIT su Oberst, o passo 3b condizionato.

Le altre MAJOR (O5–O13) vanno corrette nella stessa revisione, ma non bloccano se marcate «condizionato» nel testo. Le MINOR sono a discrezione di S9-ALG.

Se il coordinatore preferisce non chiedere la revisione di §0.4/§8 e della tassonomia, l'alternativa è **riscrivere** §0 e §8; il resto della specifica può restare.

---

## 5. Raccomandazione DM2/DM-δ per NOTAZIONE v6

1. **DM2 resta il getto in un punto**, come in NOTAZIONE v5 e in G★″ punto 7. Non riusare «DM2» per il rumore.
2. **Il rumore è un modificatore ortogonale con norma dichiarata:** DM-δ(Y), applicabile a ogni modello (DM3^δ(Y), DM2^δ in norma di getto pesata, …). Senza Y il modello non è definito (O13).
3. **Aggiungere M2⁺** (getto + ideale olonomo) e **M3-hol** (o DM1-cf: forma chiusa olonoma non EP), con il senso ID-* ammesso in ciascuno (O2, O4).
4. **Correggere gli usi esistenti che intendono il rumore:** GATE8 §5, la riga VAR-P3, VAR-Q19, ATTACK-8 O8. Rietichettare CONV-T5, la cui etichetta nel LEDGER dice «DM3» ma tratta il rumore.
5. **Rinominare il minorante di |u| in VAR-P3** (per esempio κ), per liberare δ.
