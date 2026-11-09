# AUDIT S8-DICT — S-CHECK-F8-DICT · 27/10/2026

Revisore: S-CHECK-F8-DICT, proof-checker indipendente. Oggetto: `work/S8-DICT/PROOF_PACKAGE.md` (§0–§7 e §3.6 R6), con `CHECK_REQUEST.md`, `LEDGER_ROWS.md` e gli script in `work/S8-DICT/sympy/`. Ho letto solo enunciati, ipotesi e prove; non ho letto il contesto della sessione autrice. Il kill-argument interno (`KILL_ARGUMENT_N1.md`, PASS-WITH-NOTES, senza revisore fresco) non è stato usato come base ed è stato rifatto da zero.

Contesto letto:
- `NOTAZIONE.md` v5: DM2, DM3, (H0), (H-ID), (H2);
- `research/CIT-AUDIT/AUDIT-6.md`: righe relative a Peetre/KMS, Boman, Trefethen–Weideman, Christensen/HSY, Ax (riga 18);
- `work/CHECK-F8/AUDIT_S8-CONV.md`: formato e fix CONV-2/3/4/7, per la coerenza di I-LIM e di N1(iv);
- `inbox/S8-DICT.md`: risposta di S8-ENC su R6 (ENC-C1, ENC-T2), solo per gli enunciati importati.

Skill caricate leggendo i SKILL.md, senza eseguire script `_vendor`: `skills-local/claim-lifecycle`, proof-checker (tassonomia a due assi FATAL/CRITICAL/MAJOR/MINOR), kill-argument (attacco, poi aggiudicazione), scientific-critical-thinking.

Kill-argument su N1 ((i)–(v), Teorema RANGO con (a′)/(b′), Teorema A): un subagente nuovo con il solo file `KA_DICT_N1_input.md` (estratto verbatim). File: `KA_DICT_N1_input.md`, `KA_DICT_N1_attack.md`, `KA_DICT_N1_adjudication.md`. Esito: **SURVIVES-WITH-FIXES** (WARN: 6 punti major non risolti dal testo attuale, tutti con riparazione esplicita; nessun critical sulla scala KA).

Script indipendenti, eseguiti con `python -I`:
- `sympy/dict_check.py` → `.out`: **18/18 PASS** (blocchi A–J; i test marcati [contro] verificano controesempi al testo attuale);
- script dell'attaccante: `sympy/dict_ka_checks.py` (K1–K6; K5 stampa la conclusione senza calcolarla, verificata a mano in aggiudicazione).

R6 (§3.6): l'avviso `[S8-DICT → S-CHECK-F8-DICT] AVVISO: R6 recepita` è arrivato in `inbox/S-CHECK-F8.md`; la sezione è stata riletta e auditata (non sospesa). Lo stato dipende dall'audit di S8-ENC, ancora in corso.

## 0. Verdetti

| ID | verdetto | fix | stato proposto |
|---|---|---|---|
| DICT-U1 (U1-a, U1(a), N0) | **OK** | — | **DIMOSTRATO** (Peetre CON-FONTE verificata via KMS 19.1) |
| DICT-U1b | velocità non controllate (fonte) | — | singolari e densità L^p **DIMOSTRATO**; velocità 2–3 **CON-FONTE da verificare** |
| DICT-U2 (con U2-a) | **OK con nota MINOR** | DICT-12 | **DIMOSTRATO** (Boman da verificare in CIT, la prova non dipende dal numero) |
| DICT-N2 | **OK** | — | **DIMOSTRATO** |
| DICT-U3c | **OK** | — | **DIMOSTRATO** (moltiplicatori); caso x-dipendente CON-FONTE (Hörmander 18.1.13 da verificare) |
| DICT-U3d (i), (iii) | **OK** | — | **DIMOSTRATO** (bordo trapezi verificato uniforme in t, `dict_check` D1) |
| DICT-U3d (ii) | **prova invalida per μ({0}) > 0, enunciato vero** | **DICT-4 (CRITICAL locale)** | **DIMOSTRATO dopo DICT-4** |
| DICT-U3d velocità generale | non dimostrata | — | **CANDIDATO** (Q1) |
| DICT-RIT1 | **OK** | — | **DIMOSTRATO** |
| DICT-N3 (a), (b) | **OK** | — | **DIMOSTRATO** (min sup 1,3168 ≥ 1, `dict_check` I1) |
| DICT-CS1 | **OK** | — | **DIMOSTRATO** (costante, φ_s(0+) = 1, decrescenza: `dict_check` C1) |
| DICT-U4 | **OK** | — | **DIMOSTRATO** |
| DICT-N1 (i), (ii), (iv)(a) | **OK con fix MINOR** (KA: SURVIVES-WITH-FIXES) | DICT-14 | **DIMOSTRATO** |
| DICT-N1 (iii) | **falso come scritto senza L ∈ Ann(u)** | **DICT-6 (CRITICAL formale)** | **DIMOSTRATO dopo DICT-6** (N ≥ 2) |
| DICT-N1 (iv)(b)(c) | importati da CONV-T1/T2 | DICT-15 | **DIMOSTRATO** come in AUDIT_S8-CONV; la lettura Σ⁰₂∖Π⁰₂ si allinea a CONV-7 |
| DICT-N1v (ND, ND-NL, (v)-ALG) | **OK con fix MINOR** | DICT-16 | **DIMOSTRATO** (magro e shy; Christensen/HSY: fonti da verificare, definizioni standard) |
| DICT-RANGO (I)–(III) | **OK** | — | **DIMOSTRATO** |
| DICT-RANGO (IV), (a′), (b′) | **tre enunciati falsi come scritti** | **DICT-2, DICT-3 (CRITICAL formali), DICT-5 (MAJOR)** | **DIMOSTRATO dopo DICT-2/3/5**; il caso magnetico esce da RANGO |
| N1(vi) originale | ritiro corretto | — | **FALSO** (ritirato) |
| DICT-MF (MF1, MF2, MF3 (a)–(d), MF-C) | **OK** | — | **DIMOSTRATO** |
| DICT-A (i), (ii) | **OK con fix MINOR** | DICT-13 | **DIMOSTRATO** |
| DICT-A (iii) | **passo non giustificato; il teorema vale senza l'ipotesi U_0** | **DICT-1 (MAJOR)** | **DIMOSTRATO dopo DICT-1** (ipotesi U_0 eliminata) |
| DICT-B2, DICT-R3 | **OK** | — | **DIMOSTRATO** (folklore, prior art OLS) |
| DICT-B3 | non controllato (fonte) | — | **CON-FONTE da verificare** (Pinkus) |
| DICT-R4, DICT-PAINLEVE | strumenti | — | **STRUMENTO** |
| DICT-GR | **OK con fix MINOR** | DICT-7 | **DIMOSTRATO** |
| DICT-R6 (Lemma R6-T, §3.6) | **OK con fix MINOR** | DICT-17, DICT-18 | **DIMOSTRATO condizionato** a ENC-1, ENC-C1, ENC-T2 (audit S8-ENC in corso) |
| DICT-ILIM (a)–(d) | **OK con fix MINOR**; coerente con CONV-T1 auditato | DICT-8 | **DIMOSTRATO** |
| DICT-ILIM-H0 (s = 0) | **OK** | — | **DIMOSTRATO** (costante ≤ 2, `dict_check` H1) |
| DICT-ILIM-Hs (s ≥ 1) | senza prova | — | **CANDIDATO** |
| DICT-NS (NS-L1, NS-T1, KINK) | **OK con fix MINOR** | DICT-9, DICT-10 | **DIMOSTRATO** |
| DICT-2KINK | numerico | — | **V-ex** |
| DICT-AX | etichetta da allineare | DICT-11 | **CON-FONTE (verificata, enunciato standard)** come AUDIT-6 riga 18; numero del teorema da verificare |

Conteggio fix: 0 FATAL; 4 CRITICAL locali, tutti con riparazione di una o due righe che non indebolisce le conclusioni (DICT-2, DICT-3, DICT-4, DICT-6); 2 MAJOR (DICT-1, DICT-5); 12 MINOR (DICT-7 … DICT-18).

## 1. Fix

**DICT-1 (MAJOR: UNJUSTIFIED, LOCAL) — Teorema A(iii), §3.3.** *Problema.* La prova applica il Lemma ND su M+1 palle disgiunte B_k ⊂ U_0, ma l'indipendenza dei D_i su U_0 non dà l'indipendenza su ciascuna palla. Controesempio (`dict_check` A1): Ω = (0,1), D_0 = moltiplicazione per φ_1 con supporto in (0; 0,3), D_1 = moltiplicazione per φ_3 con supporto in (0,7; 1); sono indipendenti su Ω, ma nessuna coppia di intervalli disgiunti li rende indipendenti entrambi. L'ipotesi "aperto d'indipendenza U_0" è inoltre vuota (U_0 = Ω la soddisfa sempre). *Riparazione.* La prova del Lemma ND produce N+1 punti y_0, …, y_N e getti con matrice di valutazione invertibile, e l'invertibilità è aperta nei punti. Si scelgono M+1 (N+1)-uple di punti tutti distinti con matrice invertibile e si pone O_m := unione di N+1 palline di raggio piccolo attorno ai punti della m-esima uple. Gli O_m sono a due a due disgiunti (non connessi) e su ciascuno i D_i sono indipendenti; il sistema M × (M+1), la località e il coefficiente direttore restano invariati. Verifica numerica (`dict_check` A2): stessi dati esatti a 10⁻¹⁶, λ_min relativo di v pari a 0,383. *Conseguenza.* A(iii) vale per atomi locali **senza** ipotesi aggiuntive; va tolta la nota "richiede un aperto d'indipendenza" da §3.3, §7 e LEDGER_ROWS. Concorda con il punto P6 del KA.

**DICT-2 (CRITICAL: INVALID, LOCAL; riparazione definitoria) — RANGO (IV), (a′), (b′), trasporto, §2.6.** *Problema.* Con la definizione di §2.6 ("identificabile se esiste al più una legge"), una classe che u falsifica è identificabile per vacuità. Quindi "(IV): se K·dim𝔽 > dim(valori) la classe non è mai identificabile" e "(a′): mai identificabile" sono falsi (u = t, classe ∂_t + θ_0 + θ_1∂_x: in t = 0 l'equazione dà 0 = −1), e i "⟺" "identificabile ⟺ int Z(u) = ∅" e "⟺ {u_x ≠ 0} denso" falliscono in (⇒) (u = t + ψ(x) con ψ′ = 0 su un intervallo). (II) caratterizza in realtà ker Φ_u = 0, cioè l'unicità condizionata all'esistenza. Inoltre in (a′) "K ≥ 2" richiede d ≥ 1 oppure m ≥ 2. *Riparazione.* Definire "identificabile" come ker Φ_u = 0 (oppure scrivere ovunque "se esiste una legge, è unica / non è unica") e aggiungere la condizione su (d, m). Con questa definizione tutti gli enunciati di (IV), (a′), (b′) e del trasporto diventano veri con le prove scritte. La frase di §4 "(H-ID) vale quando {u_x ≠ 0} è denso" resta corretta, perché (H-ID) presuppone l'esistenza. KA P1, P2, P10.

**DICT-3 (CRITICAL: INVALID, LOCAL) — (b′) Schrödinger con V reale, §2.6.** *Problema.* "Esiste una legge con V reale ⟺ Im(−(iu_t + Δu)/u) ≡ 0 su {u ≠ 0}" è falso in (⟸) quando u ha zeri: il quoziente può essere reale ma non estendibile (u = x³: V = 6/x², `dict_check` G1) oppure u può falsificare la classe per (III) (u = e^{−it}(x + x²): in x = 0, A_u = 0 ma −L_0u = −2e^{−it} ≠ 0). *Riparazione.* "⟺" solo per u senza zeri; in generale solo (⇒), con la condizione aggiuntiva iu_t + Δu = 0 su Z(u) e il problema di divisione (Q3). KA P3.

**DICT-4 (CRITICAL: INVALID, LOCAL; enunciato vero) — U3(d)(ii), §1.4.** *Problema.* La prova della convergenza L¹ della discretizzazione di Bernstein k(t) = ∫e^{−λt}dμ(λ) trascura λ < ε₀. Se μ({0}) > 0 la parte trascurata non è piccola: k = 1 + e^{−t} dà errore pari a T (`dict_check` B1). *Riparazione.* Partizionare [0, Λ] includendo 0 come nodo (atomo trattato esattamente) oppure togliere a parte μ({0})·1, che è già un atomo del dizionario. L'enunciato sopravvive invariato.

**DICT-5 (MAJOR: UNJUSTIFIED, LOCAL) — caso magnetico dentro RANGO, §2.6.** *Problema.* (∇ − iA)²u = Δu − 2iA·∇u − i(div A)u − |A|²u non è lineare in θ = A (termini div A e |A|²), quindi il quadro L_0 + Σθ_kT_k non si applica. La descrizione "spazio affine sui campi a divergenza nulla" è falsa: due leggi reali (A, V), (A + B, V + δV) per lo stesso u esistono se e solo se div(|u|²B) = 0 (derivazione in `KA_DICT_N1_adjudication.md`, P4; controesempio u = (2 + cos x)e^{iy}, B = (sin y, 0)). *Riparazione.* Togliere il caso dai corollari di RANGO e rinviare a SYS-N3 (S8-SYS, auditato) con la condizione div(|u|²B) = 0; la conclusione qualitativa "le leggi, se esistono, non sono uniche per n ≥ 2" resta vera (B = |u|^{−2}∇^⊥χ con χ a supporto compatto dove u ≠ 0).

**DICT-6 (CRITICAL formale: INVALID, LOCAL) — N1(iii), §2.3.** *Problema.* L'enunciato non richiede L ∈ Ann(u): con u = e^t, L = τ + 5 (o u = e^{−t}sin x, L = ∂_x, `dict_check` F1) l'inclusione stretta (L) ⊊ Ann(u) è falsa. La frase sul caso N = 1 ("la differenza delle dimensioni è costante, = deg L") confonde due differenze. *Riparazione.* Aggiungere "L ∈ Ann(u)"; nella nota N = 1 dire che la differenza costante è dim R_{≤n} − dim((L) ∩ R_{≤n}) = deg L (per n grande), mentre dim Ann_{≤n} − dim (L)_{≤n} si stabilizza a deg L − D. KA P5.

**DICT-7 (MINOR) — G-R(a), §3.5.** "λ_min(G′_n) > 0 per minimalità" non è giustificato: R1 testa la Gram omogenea, mentre n_0 è definito tramite il fit affine (con L_0). Allineare le due definizioni (Gram del sistema affine aumentato, oppure n_0 definito sulla Gram omogenea).

**DICT-8 (MINOR) — I-LIM, §4.** La frase "(per 1 + d = 2 variabili …)" usa d come dimensione spaziale, mentre in CONV-T1(5) d è il grado minimo e il bound è (d+1)(d+2)/2. Rinominare la dimensione. Per il resto I-LIM (a)–(d) è corretto sotto (H0), (H-ID), (H2) e coerente con CONV-T1 come auditato (fix CONV-2/3/4); il modello è BSS per il ramo esatto (CONV-T1) e "approssimato" per (a)–(d): dichiararlo per ramo, come chiede la nota O9. La compattezza di 𝒦_R in C^s è corretta (basta la condizione del cono; la quasi-convessità è un'osservazione accessoria). La costante hölderiana per s = 0 maggiora quella della prova (`dict_check` H1: 4^{1/(N+2)} ≤ 2).

**DICT-9 (MINOR: OVERSTATED, LOCAL) — NS-T1, "Conseguenza", §5.2.** ALG-T1 vale per equazioni evolutive; sine-Gordon in coordinate di cono u_xt = sin u non lo è. Restringere la conseguenza alla forma evolutiva u_tt = u_xx + sin u (a cui si applica) oppure togliere il riferimento ad ALG-T1 per u_xt.

**DICT-10 (MINOR) — NS-L1, §5.1.** L'equivalenza fra le soluzioni dell'equazione polinomializzata (in w = e^{iu}) e di quella originale richiede un logaritmo globale: dichiarare Ω semplicemente connesso (o u definita a meno di 2πℤ). Le identità di polinomializzazione sono corrette (`dict_check` E1–E3, E5); il kink soddisfa U″ = sin U (E4).

**DICT-11 (MINOR) — Ax, §5 e §7.** AUDIT-6 riga 18 marca Ax 1971 VERIFICATO per l'enunciato standard (numero del teorema non verificato). Allineare l'etichetta: "CON-FONTE (verificata)" invece di "da verificare". NS-EXPALG non usa Ax nelle prove (corretto).

**DICT-12 (MINOR) — U2-a, §1.2.** La levigatezza di F è provata per F associata a (f, K); non serve e non è provato che F non dipenda da f. Dire "F dipende da (f, K); la conclusione di U2 non richiede indipendenza". La condizione 𝒲 (getti ammissibili in un aperto) e l'uso di Boman sono corretti.

**DICT-13 (MINOR) — Teorema A(i), §3.3.** "U_n aperto anche in topologie deboli (D′)" vale per atomi il cui trasposto conserva C_c^∞ (operatori differenziali), non per operatori continui C^∞ → D′ qualsiasi. Restringere. KA P7.

**DICT-14 (MINOR) — N1(i), §2.1.** Per ogni classe citata va verificata la continuità della parametrizzazione (|ξ|^s non è liscio in 0; s ↦ ⟨ξ⟩^s è continua in S^m solo per s < m) oppure la σ-compattezza dell'immagine. Con parametri razionali e dizionari numerabili l'esito non cambia. KA P8.

**DICT-15 (MINOR) — N1(iv)(c), §2.4.** Eredita CONV-7: la lettura "Σ⁰₂ ∖ Π⁰₂" va ridotta a commento ("verificabile nel limite, non decidibile nel limite, con qualunque successione di regole"), come già fatto da S8-CONV. KA P9.

**DICT-16 (MINOR) — N1(v)-ALG, §2.5.** L'insieme delle u differenzialmente algebriche contiene i polinomi ed è denso: è magro e shy, non "raro". Sostituire "raro" con "magro". KA P11.

**DICT-17 (MINOR) — R6-T(c), §3.6.** Il confronto delle distanze va enunciato per u ∈ C^∞(Ω) con D_iu ∈ Y per gli atomi usati (altrimenti dist(u, ker L) in Y non è definita per la parte non limitata di L). La stima (b) è corretta: 1 + 2a·(aQ/2)e^{a√Q} = 1 + a²Q·e^{a√Q} (`dict_check` J1), e ‖H‖_∞ ≤ (aQ/2)e^{a√Q} con il nucleo esatto J_1 per q costante (J3). (a) e (d) sono corretti.

**DICT-18 (MINOR) — R6, motivazione dell'esclusione di MF3, §3.6.** La ragione data ("W* non conserva il supporto compatto") è inesatta: il trasposto Wᵗ porta C_c^∞ in funzioni a supporto nell'involucro simmetrico [x_0 − b, x_0 + b] ⊂ J°, e per q costante Wᵗg è liscia anche in x_0 (`dict_check` J2: i rami s > 0 e s < 0 coincidono). La ragione corretta è "la liscezza di Wᵗψ in x_0 per q generale non è verificata". L'esclusione resta prudente e corretta come ambito.

## 2. R6 (§3.6) — audit completo

- (a) La biiezione φ fra il livello q e il livello libero pari, con conservazione del peso j + 2k, segue da ENC-C1 (W·P(∂_t, L_q) = P(∂_t, L_0)·W) per linearità: corretta.
- (b) Stima ‖W‖, ‖W^{−1}‖ ≤ 1 + a²Q·e^{a√Q} su C(Ω̄) e su L²(Ω) (Fubini in t, Schur nel caso L²): corretta con la costante di ENC.
- (c) Confronto di distanze e λ_min: corretto con DICT-17.
- (d) Trasporto dei certificati ψ ↦ ψ∘W: corretto (W limitato e invertibile, certificati di MF1/MF2).
- Ambito dichiarato (sottoanello pari ℂ[∂_t, L_q], q dato, Ω rettangolo simmetrico, Y = C o L²; H^{2k}, MF3 e getti esclusi): coerente con ENC-T2(b)(c) e con la condizione di non circolarità (q dato).
- Stato: **DIMOSTRATO condizionato** a ENC-1, ENC-C1, ENC-T2. Diventa DIMOSTRATO quando l'audit di S8-ENC (S-CHECK-F8-ENC) conferma quei tre enunciati.

## 3. Coerenza con CONV e citazioni

- I-LIM e G-R usano CONV-T1 nella forma auditata (fix CONV-2/3/4 recepiti da S8-CONV); il bound di T1(5) è (d+1)(d+2)/2 con d grado minimo (vedi DICT-8). N1(iv)(b)(c) importa CONV-T1/T2 senza modifiche; CONV-T2 vale per ogni n ≥ 1.
- Citazioni ancora "da verificare" (Q7 del pacchetto): Boman 1967, Hörmander III 18.1.13, Trefethen–Weideman 2014 (Thm 5.1; il bordo è verificato numericamente in D1, quindi la prova di U3(d)(iii) non dipende dal numero), Christensen / Hunt–Sauer–Yorke (definizioni standard), Pinkus 1985, WTC 1983, Gagliardo–Nirenberg. Ax 1971: vedi DICT-11. Nessuno stato DIMOSTRATO proposto qui dipende dal numero di un teorema citato.

## 4. Sintesi
Il pacchetto regge. Il cammino critico N1 sopravvive al kill-argument indipendente con correzioni: quattro enunciati falsi così come scritti (vacuità di "identificabile", V reale con zeri, N1(iii) senza L ∈ Ann(u), U3(d)(ii) con atomo in 0) hanno riparazioni di una o due righe; il Teorema A(iii) si rafforza (l'ipotesi U_0 sparisce). Il caso magnetico esce da RANGO e va a SYS-N3. R6 è corretta nel suo ambito ed è condizionata all'audit di S8-ENC.
