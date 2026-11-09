# ATTACK-8 — avvocato del diavolo prima del Gate 8

27/10/2026 · sessione DEVIL-8 · piano in `PLAN-8.md`.

**Materiale attaccato.** G★″ (PROBLEM v3, punti 1–6), SYNTHESIS-2 (§0–§3), ROUTES (tabella del Gate 6), NOTAZIONE v5, i cinque pacchetti `work/S8-{SYS,VAR,ENC,DICT,CONV}` (LEDGER_ROWS, PROOF_PACKAGE nelle sezioni citate, RECEPIMENTO dove esiste), gli audit `work/CHECK-F8/AUDIT_S8-*.md`, le revisioni 2 `AUDIT_S8-ENC_rev2.md` e `AUDIT_S8-DICT_rev2.md`, `AUDIT_S8-CONV_T2prime.md`, `KA_ENC2_input.md`, la coda di `inbox/central-F6.md` (fino a `DONE S-CHECK-F8-DICT-rev2`).

**Skill applicate.** Revisione avversaria (cercare il controesempio prima dell'argomento), auto-correzione (ritiro esplicito di due miei errori di DEVIL-6), regola "gli stati scendono soltanto".

**SymPy** (`sympy8/devil8_checks.py`, eseguito con `.venv\Scripts\python.exe -I`; uscita in `sympy8/devil8_checks.out`): **12/12 PASS**.
- (A) Per i u_t = (−∂² + x²)u il flusso classico è x″ = −4x. La fattorizzazione chirp·libero·chirp si rompe al primo zero di b(t) = sin(2t)/2, cioè a t = π/2, dove cos t = 0. La rottura a t = π vale solo per H/2.
- (C) Per V = 0, u = (1 + 4a_0t)^{−1/2}e^{ia(t)x²} con a = a_0/(1 + 4a_0t) è soluzione. Il rappresentante pseudo-conforme ha θ(t) = t/(1 + 4a_0t) ≠ t. È il testimone di ENC2-4.
- (D) Avron–Herbst: per V = β(t)x, la trasformazione u = e^{i(−B(t)x + g(t))}w(t, x − s(t)) con B′ = β, s′ = −2B, g′ = −B² porta w libera. Il tempo resta invariato (θ = id).
- (E) Per ogni u senza zeri, (∂_t − u_t/u)u = (∂_x − u_x/u)u = 0. In un anello di coefficienti chiuso per derivazione Ann(u) contiene sempre operatori del primo ordine: è la vacuità di VAR-N1.
- (F) Nella classe u_t = a u_xx + b u con u = t + sin x si ha ker Φ_u = 0, ma nessuna legge della classe esiste.
- (H) ε^{N+1}e^{1/(3ε)} → ∞ per N = 5, 20. Nessuna stima d'ordine finito vale per ⟨e^{1/(1−t)}, φ⟩: la parte 𝒟′ di SYS-S1-C regge.

---

## 1. Memo d'attacco (≤ 250 parole)

F8 ha prodotto lemmi solidi: il cammino critico ENC-1 → C1 → T2 → R6 regge, VAR-T1 in (SF) regge, CONV-T2′ è corretto. Nessuna obiezione FATAL. Il problema è il **testo di G★″**, che oggi afferma cose che F8 ha dimostrato false.

PROBLEM v3, punto 4, e SYNTHESIS-2, §0 e §2, dicono ancora «encoder cieco ⟺ identificabilità congiunta». ENC-N1 è FALSO; ENC-N1′ è soltanto un lemma di riduzione. Dicono anche «le eccezioni quadratiche cambiano il tempo». È FALSO: Avron–Herbst ha θ = id. La correzione ENC-P0′-DIC, scritta dal revisore, è a sua volta FALSO come scritta. Due di queste frasi le ho introdotte io in DEVIL-6 (F6). Anche la mia F5 era sbagliata: in H = −∂² + x² la rottura a cos t = 0 esiste. SYNTHESIS-2, §1, riporta l'errore.

Sul piano strategico, RT-ENC non aggiunge potere identificativo: l'encoder richiede q, e la versione "cieca" coincide per definizione con l'identificabilità. Va parcheggiata come strada; i lemmi restano. La nozione "identifica" ha almeno cinque significati non equivalenti: con ker Φ_u = 0, u è "identificabile" anche quando nessuna legge esiste (SymPy F). Tutte le risposte positive vivono in DM3 (dato esatto). Quasi tutto il DIMOSTRATO è classico o probabilmente noto.

Gate 8a: restano attive SYS, IDV, DICT e CONV; ODE-GAL si restringe a C3-Q2; NA ed ENC vanno parcheggiate; RT-5, RIGID, STOKES e CONV-BORDO tornano parcheggiate; Mori–Zwanzig, R2a e POLE vanno eliminate. Gate 8b: revisione **limitata** di Gate 3 (anello dei coefficienti, mappa residuo); G★′-NL resta invariato.

---

## 2. Obiezioni

Severità: FATAL (G★″ crolla), CRITICAL (un testo centrale afferma un FALSO; va corretto prima del Gate), MAJOR (lacuna di contenuto o di strategia che cambia stati o strade), MINOR (redazione, notazione, citazione).

### O1 — CRITICAL — G★″ e SYNTHESIS-2 enunciano ENC-N1, che è FALSO
- **Claim colpito.** PROBLEM.md riga 45 (punto 4): «ENC-N1 (encoder cieco ⟺ identificabilità congiunta)». SYNTHESIS-2 riga 10, riga 39 (tabella, «prova scritta») e riga 70.
- **Controesempio.** LEDGER_ROWS S8-ENC: «ENC-N1 (F6) | FALSO (testimone: ENC-N1′(iv))». ENC-N1′ è DIMOSTRATO solo **come lemma di riduzione**: "cieco" è definito in modo da coincidere con l'identificabilità congiunta. Non è un teorema di equivalenza.
- **Rimedio.** Nel punto 4 e nel punto 6 di G★″ sostituire con: «ENC-N1′: la costruzione cieca si riduce all'identificazione congiunta di (q, u); nessun guadagno identificativo». In SYNTHESIS-2 la riga 39 diventa FALSO, con il rinvio a N1′.

### O2 — CRITICAL — «Le eccezioni quadratiche cambiano il tempo» è FALSO, e così la sua correzione
- **Claim colpito.** SYNTHESIS-2 riga 10 e riga 38 («eccezione = trasformazioni che cambiano il tempo (F6)»), insieme alla negativa ENC-P0 del punto 6 di G★″.
- **Controesempio.** (i) Avron–Herbst, V = β(t)x: θ = id (SymPy D; ENC-P0-sintesi è già FALSO). (ii) ENC-P0′-DIC, «θ = id ⟺ α ≡ 0», è FALSO come scritto (AUDIT_S8-ENC_rev2, ENC2-4): già per V = 0 esiste un rappresentante pseudo-conforme con θ(t) = t/(1 + 4a_0t) (SymPy C). La forma corretta è esistenziale: «esiste un rappresentante con θ = id ⟺ α ≡ 0».
- **Origine.** La frase viene dalla mia F6 di DEVIL-6, poi dal testo del revisore ENC-2. **Ritiro F6** nella parte "cambiano il tempo".
- **Rimedio.** G★″/SYNTHESIS-2: «per V(t, x) generico nessun encoder indipendente da t (ENC-P0(b), (b)^cl); le eccezioni quadratiche in x si trattano con trasformazioni metaplettiche e di gauge; il tempo va riparametrizzato solo se α ≢ 0 (forma esistenziale, ENC2-4)».

### O3 — MAJOR — F5 di DEVIL-6 era un errore di normalizzazione
- **Claim colpito.** SYNTHESIS-2 riga 35: «F5: nessuna rottura a cos t = 0 per l'oscillatore (chirp·libero·chirp per |t| < π)».
- **Controesempio.** Nella normalizzazione del progetto, H = −∂² + x², b(t) = sin(2t)/2 si annulla a t = π/2, dove cos t = 0 (SymPy A; AUDIT_S8-VAR, VAR-6). |t| < π vale per H/2.
- **Rimedio.** Ritiro F5. Riga 35: «in H = −∂² + x² la parola chirp·libero·chirp si rompe esattamente a cos t = 0 e si attraversa con la lente (VAR-T10, VAR-6); la frase F6 originale era corretta». NOTAZIONE v6 deve fissare H = −∂² + x² come normalizzazione unica dell'oscillatore.

### O4 — MAJOR — Il contratto CONV-T7 etichetta Magnus come (B) senza la condizione di normalità
- **Claim colpito.** S8-CONV PROOF_PACKAGE §9 (riga 297): «V ∈ C([0,T];L^∞) → (B) … Magnus se ∫‖A‖ < π», con fonte Casas 2007 e la nota «costante π non letta».
- **Lacuna.** VAR-T10(4) è CON-FONTE: Casas, Thm 3.4, chiede che Y(t; ε) sia normale in dimensione infinita (VAR-5). Per Schrödinger A = −iH(t) non è limitato; Magnus ha senso solo in rappresentazione d'interazione, con A_I(t) = e^{iH_0t}V(t)e^{−iH_0t}. CONV e VAR sono incoerenti su questo punto.
- **Rimedio.** Nel contratto: «(B) Dyson; Magnus (B) solo in dimensione finita o sotto l'ipotesi di Casas, Thm 3.4, nella rappresentazione d'interazione». La proposizione CONV-T7 non cambia (non usa Magnus); cambia la riga del contratto.

### O5 — MAJOR — "Identifica" ha cinque significati, e uno conta come identificabili dati senza legge
- **Claim colpito.** L'uso trasversale di "identifica" in G★″, punto 3.
- **Lacuna.** (1) SYS/C3: Ann(u) = (P) (NOTAZIONE v1, riga 74). (2) DICT-RANGO: ker Φ_u = 0. (3) VAR: V determinato in forma fissata, mappa residuo. (4) ENC: identificazione di una famiglia modulo costanti, (E2). (5) CONV/DICT-ILIM: identificazione nel limite. Nel senso (2), u = t + sin x è "identificabile" nella classe u_t = a u_xx + b u, ma non risolve alcuna legge della classe (SymPy F). DICT-3 corregge il "⟺" per u con zeri, non questo punto.
- **Rimedio.** NOTAZIONE v6: etichette ID-ann, ID-ker, ID-res, ID-fam, ID-lim. Ogni riga DIMOSTRATO deve dire quale significato usa. ID-ker vale solo **dato che una legge esiste** (ipotesi (H-ex) esplicita).

### O6 — MAJOR — Novità: quasi tutto il DIMOSTRATO di F8 è classico o probabilmente noto
- **Claim colpito.** Le parti positive di G★″ (punti 2–5) presentate come risultati del progetto.
- **Lacuna.** SYS-T1 è Matlis 1958 (declassato). SYS-EX e SYS-N1: probabilmente Oberst 1993, letto solo nell'abstract. VAR-L1 e L2: Saut–Scheurer 1987. ENC-1: Marchenko. ENC-K1′: probabilmente Andrianov–Sokolov 2003. DICT-N1(i)–(iii), B2 e R3 sono classici. CONV-T2 è un Σ⁰₂ standard. CONV-D2 è Malgrange. G-T2 è Aharonov–Bohm / Wu–Yang. F8 assorbe solo parzialmente la mia F8 di DEVIL-6: Oberst 1990 resta non letto.
- **Rimedio.** Prima del Gate 9, CIT-AUDIT obbligatorio su Oberst 1990 e 1993, Saut–Scheurer 1987 e Andrianov–Sokolov 2003. In G★″ il contributo dichiarato deve essere la **composizione** (L6–L10) e le negative nuove (VAR-T1(c)-F, ENC-P0(b)^cl, DICT-N1(vi), CONV-R1-F, CONV-MZ3-F, SYS-S1-C), non i singoli lemmi positivi.

### O7 — MAJOR (strategica) — RT-ENC non aggiunge potere identificativo
- **Claim colpito.** RT-ENC attiva nel Gate 6.
- **Argomento.** ENC-T2 vale **a q noto** (lo dice il pacchetto stesso). Il q va preso dalla mappa residuo di VAR-T1. La versione cieca è N1′, una riduzione per definizione. ENC-P0 è negativa. In F8 nessun risultato di identificazione richiede l'encoder: R6 lo usa come traduzione, non come fonte di informazione.
- **Rimedio.** Parcheggiare RT-ENC come strada (Gate 8a), con trigger ENC-Q4 o ENC-Q10. I lemmi ENC-1, C1, T2, P0(b)^cl e A9 restano patrimonio di RT-DICT e RT-IDV.

### O8 — MAJOR — Robustezza: tutte le risposte positive vivono in DM3
- **Claim colpito.** G★″, punto 3 (identificazione) e punto 5 (algoritmo).
- **Lacuna.** VAR-T1, DICT-R6 e CONV-T5 assumono il dato esatto (DM3). In DM2 (rumore) l'unica stima è la nitidezza Hölder 1/3 di VAR-P3, che è una stima di modulo e non certifica nulla. DICT-ILIM-Hs resta CANDIDATO. Un Gate che chiami "identificazione" il risultato DM3 promette troppo.
- **Rimedio.** In G★″ scrivere «identificazione in DM3; in DM2 solo i moduli di VAR-P3 e la negativa DICT-N1(ii)». Aprire una domanda di robustezza (DM2 con livello di rumore noto) come obiettivo della Fase 9, non come claim.

### O9 — MAJOR — L'oggetto canonico di Gate 3 è vacuo con coefficienti chiusi per derivazione
- **Claim colpito.** L'oggetto canonico (D·u, u) di Gate 3, quando si passa ai coefficienti variabili (L7–L9).
- **Controesempio.** VAR-N1: per ogni u senza zeri, 𝒦[∂]/Ann(u) ≅ 𝒦u, che ha rango 1 (SymPy E). L'oggetto non distingue nulla.
- **Rimedio.** Vedi Gate 8b: specificare l'anello dei coefficienti (ℂ(x)[∂], Weyl A_n, oppure coefficienti in una classe fissata) e aggiungere la mappa residuo ρ_u come oggetto canonico per le classi strutturate.

### O10 — MAJOR — Fix delle revisioni 2 non ancora recepiti: le righe "DIMOSTRATO dopo fix" non sono promuovibili
- **Claim colpito.** ENC-P0(b)^cl, P0(b)^loc, P0′ (nucleo denso), POLE-N^cl e T2(c′), che rev2 propone DIMOSTRATO dopo ENC2-1…6. DICT-MAG-NU, che rev2 propone DIMOSTRATO dopo MAG-1 e MAG-2. CONV-T2′, proposto DIMOSTRATO dopo T2P-1…3.
- **Lacuna.** In `work/S8-CONV/PROOF_PACKAGE.md` non c'è alcuna etichetta T2P (grep vuoto). I LEDGER_ROWS di ENC e DICT riportano ancora DA AUDITARE. Promuovere senza recepimento significa promuovere un testo diverso da quello auditato. MAG-1, inoltre, cambia l'ipotesi (A e V dipendenti da (t, x)): non è redazione.
- **Rimedio.** Recepimento rev2 (ENC2-1…6, MAG-1…5, T2P-1…3) prima della promozione. Gli stati proposti al §6 sono condizionati.

### O11 — MINOR — NOTAZIONE v5: «α, β identificati esattamente» senza condizione
NOTAZIONE v5 (righe 95–125) lo afferma senza condizioni, ma H-DIRAC è DIMOSTRATO con H-DIRAC-1 e H-DIRAC-2 come ipotesi. **Rimedio:** aggiungere «sotto H-DIRAC-1, 2».

### O12 — MINOR — NOTAZIONE (E2) con c costante contro ENC-P0(b) con c(t)
(E2) è definita non autonoma con c costante; ENC-P0(b) e (b)^cl ammettono c(t). **Rimedio:** in NOTAZIONE v6 (E2) con c ∈ C(I), e il caso costante come (E2₀).

### O13 — MINOR — Etichetta "(ID)" in DICT-GR contro "(H-ID)" di NOTAZIONE
Sono due nomi per la stessa ipotesi, oppure due ipotesi con quasi lo stesso nome. **Rimedio:** unificare in (H-ID) e dirlo nel pacchetto.

### O14 — MINOR — S-O1 è citata in G★″, punto 2, ma F8 non l'ha toccata
PROBLEM riga 43 cita «ostruzione S-O1» accanto a SYS-S1 e VAR-T6. Nessun pacchetto F8 la riesamina, e SYS-S1-C (FALSO) modifica il contesto (Ext¹ ≠ 0). **Rimedio:** controllare che S-O1 non dipenda dalla forma falsa di SYS-S1-C; altrimenti segnarla da riallineare.

### O15 — MINOR — DICT-MAG-NU replica SYS-N3(c); la riga di SYS-N3 è ambigua
MAG-NU è SYS-N3(b)(c) localizzata, con k = −∇^⊥χ (lo ammette AUDIT_S8-DICT_rev2, MAG-4, e l'audit dichiara di non essere indipendente). Il riassunto di SYS-N3 nel LEDGER («campi a divergenza nulla») non dice **quale** divergenza: è div(|u|²B) = 0, non div B = 0. **Rimedio:** una sola riga canonica (SYS-N3), con MAG-NU come corollario «u con zeri fuori da supp χ»; nel riassunto scrivere div(ρ²B) = 0.

### O16 — MINOR — ENC-A9(b) dichiarato DIMOSTRATO ma (b3) = VAR-T10
VAR-T10(3)(iii) è CON-FONTE + V-ex. La riga ENC-A9(b) eredita lo stato peggiore per (b3). **Rimedio:** stato per parti (§6).

### O17 — MINOR — SYNTHESIS-2 §0.2(b′): «V identificato esattamente, anche se dipende dal tempo»
VAR-T1(c) mostra che con int Z(u) ≠ ∅ c'è una fascia di silenzio; VAR-T1(c)-Q10 è APERTO. **Rimedio:** aggiungere «fuori dalle fasce di silenzio, in (SF)».

### O18 — MINOR — Strade riaperte nel Gate 6 mai toccate in F8
RT-5 (→ SYS), RIGID e STOKES (→ IDV), CONV-BORDO: nessun pacchetto F8 le cita (grep). **Rimedio:** tornano PARCHEGGIATA (Gate 8a).

### O19 — MINOR — DICT-R6(f) poggia su ENC-T2(c′), ancora DA AUDITARE
R6 è DIMOSTRATO, ma (f) cita ENC-T2(c′) (MAG-5). **Rimedio:** citare DICT-N1(ii) e il Teorema A, come propone rev2. (a)–(e) non ne dipendono.

### O20 — MINOR — VAR-L2-cor è DA AUDITARE e nato su domanda di ENC
Nessuna riga DIMOSTRATO di ENC deve citarlo finché non viene auditato. Oggi nessuna lo fa (ENC lo ha chiesto, non lo usa nel cammino critico). **Rimedio:** vincolo esplicito in RIPRESA.

### O21 — MINOR — SYS-S1-C, parte 𝒟′: corretta, manca un'ipotesi scritta
Ho rivisto la prova del revisore (audit SYS-5). k_C − k_B = β(t)e^{1/(1−t)} non si estende come distribuzione oltre t = 1, se β(1) ≠ 0 e supp ρ ⊂ (1, 2) (SymPy H: nessuna stima d'ordine finito). **Rimedio:** scrivere β(1) ≠ 0 nell'enunciato. Lo stato FALSO di SYS-S1-C è confermato.

**Conteggio:** FATAL 0 · CRITICAL 2 · MAJOR 8 · MINOR 11.

---

## 3. Coerenza tra sessioni

| flusso | esito | nota |
|---|---|---|
| VAR → ENC | **coerente, con riserva** | ENC-T2 a q noto, q da VAR-T1 (mappa residuo): coerente. ENC-A9(b3) = VAR-T10, che va ereditato per parti (O16). VAR-L2-cor è DA AUDITARE e non è usato (O20). La normalizzazione H = −∂² + x² è la stessa in VAR e in ENC2-4. |
| CONV → DICT | **coerente** | CONV-T2 / T2′ (Σ⁰₂) e DICT-ILIM coincidono nella nozione "nel limite". DICT-N1(iv)-bc rinvia ad AUDIT_S8-CONV. CONV-D1 (n ≥ 3) è compatibile con lo scalare C12-T1′ in n = 2. **Incoerenza:** il contratto CONV-T7 (Magnus) contro VAR-T10(4) (O4). |
| SYS → DICT | **coerente** | SYS-N3 (div(ρ²B) = 0, B = −k/ρ²) coincide con DICT-MAG / MAG-NU. MAG-NU è una replica localizzata (O15). |
| SYS → ENC | **coerente** | FW-1 (Foldy–Wouthuysen) e H-DIRAC usano le stesse ipotesi. NOTAZIONE v5 non riporta la condizione (O11). |
| ENC → DICT | **coerente** | Il cammino critico ENC-1 → C1 → T2 → R6 è invariato dopo il recepimento S8-ENC e rev2. La citazione (f) è da sistemare (O19). |
| Notazione contro NOTAZIONE v5 | **3 scarti** | (E2) con c costante (O12); "(ID)" contro (H-ID) (O13); «α, β identificati esattamente» senza condizione (O11). In più, "identifica" è sovraccarico (O5). |
| DIMOSTRATO su DA AUDITARE | **2 casi** | DICT-R6(f) → ENC-T2(c′) (O19). Righe "DIMOSTRATO dopo ENC2-k / MAG-k / T2P-k" senza recepimento (O10). Nessun altro trovato. |
| Ipotesi incompatibili | **nessuna** | Il punto più delicato, SYS-S1-C (Ext¹ ≠ 0), contro lo scalare C12-T1′: non c'è conflitto, perché N ha lunghezza finita in n = 2. |

### Assorbimento di F1–F10 (ATTACK-6)

| fix | esito |
|---|---|
| F1 | ✓ assorbito, ma ha prodotto errori formali, corretti da DICT-2 e DICT-3 |
| F2 | ✓ (SYS-E1 sostituisce "P1-T5 no") |
| F3 | ✓ |
| F4 | ✓ |
| F5 | **errato da parte mia**: ritirato (O3) |
| F6 | **parzialmente errato da parte mia**: la parte "cambiano il tempo" è ritirata (O2) |
| F7 | ✓ |
| F8 | parziale: Oberst 1990 non letto, Oberst 1993 letto solo nell'abstract (O6) |
| F9 | ✓ quasi tutto |
| F10 | ✓ |

---

## 4. Gate 8a — strade

| strada | proposta | motivo |
|---|---|---|
| RT-SYS | **ATTIVA (ridotta)** | Restano aperti Maxwell (Q6), II-T2(b′) e Q-S8SYS-1. Il CIT su Oberst 1993 è un prerequisito di qualsiasi rivendicazione su ℝ^n. |
| RT-IDV | **ATTIVA** | VAR-T1 in (SF) regge. Aperti VAR-Q10 (int Z = ∅) e VAR-Q17 (soluzioni miti). È la sorgente di q per tutto il resto. |
| RT-ODE-GAL | **ATTIVA, ristretta a C3-Q2** (o fusa in RT-IDV) | C3-Q2 è chiuso per L monico in ∂_t. Resta solo il caso generale (VAR-C3Q2-open, VAR-Q12/13). |
| RT-NA | **PARCHEGGIATA** | Quasi tutto è CON-FONTE (Wei–Norman, Casas, Pazy). Trigger: VAR-Q8, VAR-Q11, VAR-Q18. |
| RT-ENC | **PARCHEGGIATA come strada** | Nessun potere identificativo (O7). I lemmi restano. Trigger: ENC-Q4, ENC-Q10. |
| RT-DICT | **ATTIVA** | Porta allo strato algoritmico della Fase 9 (R6, ILIM, RANGO). Aperti DICT-Q3, Q4 e ILIM-Hs. |
| RT-CONV | **ATTIVA** | Contratto T7 per ALGORITMO_ESTESO, con O4 da sistemare. CONV-T2′ da promuovere dopo T2P. |
| RT-5 (→ SYS) | **PARCHEGGIATA** | Mai toccata in F8 (O18). |
| RIGID, STOKES (→ IDV) | **PARCHEGGIATA** | Mai toccate in F8 (O18). |
| CONV-BORDO | **PARCHEGGIATA** | Mai toccata in F8 (O18). |
| Mori–Zwanzig (→ CONV) | **ELIMINATA come strada** | Il criterio è FALSO (CONV-MZ3-F). I lemmi MZ1–MZ3 restano. |
| RT-R2a (→ CONV) | **ELIMINATA** | Il criterio è FALSO (CONV-R1-F, f = ξ, g = τ). Resta il lemma CONV-R1. |
| Faddeev (→ ENC) | **FUSA** nel lemma FAD-1 | Un lemma, non una strada. |
| POLE (→ ENC) | **ELIMINATA** | POLE-N è negativo. |
| gamblets (→ ENC) | **ELIMINATA** (osservazione GAM-O1) | Solo CON-FONTE (Owhadi 2017). |
| MICRO / FW (→ SYS/ENC) | **FUSA** in FW-1 | — |
| MPUM (→ SYS/CONV) | **FUSA** (SYS-R1, VAR-VMPUM) | Il delta VMPUM è ristretto (VAR-4). Il CIT è ancora da fare. |
| NS-EQUIV, NS-GALDAR | **FUSE** in RT-ENC (ora parcheggiata); NS-EQ-Ω è un lemma | — |
| NS-EXPALG | **FUSA** in RT-DICT ✓ | — |
| PAINLEVÉ | **STRUMENTO** (DICT-R4) | — |
| F4-ALG | **FUSA** (N1(v)-ALG) | — |

---

## 5. Gate 8b — rivedere Gate 3 o G★′-NL?

**Gate 3: sì, revisione limitata.**
1. *Anello dei coefficienti.* Con coefficienti in un campo chiuso per derivazione l'oggetto (D·u, u) è vacuo: 𝒦[∂]/Ann(u) ≅ 𝒦u per ogni u senza zeri (VAR-N1, SymPy E). Gate 3 va enunciato con l'anello specificato (ℂ[∂] per i coefficienti costanti, ℂ(x)[∂] o Weyl A_n per quelli polinomiali, oppure una classe parametrica fissata). Per le classi strutturate (L7–L9) l'oggetto canonico deve includere la mappa residuo ρ_u. È questo che VAR-T1 e DICT-RANGO usano davvero.
2. *"Componente = fattore" per i sistemi.* Richiede Ext¹(N, 𝒜) = 0: SYS-S1-C è FALSO su un dominio semplicemente connesso. Per il caso scalare C12-T1′ (n = 2, N di lunghezza finita) non cambia nulla; è coerente con CONV-D1 per n ≥ 3. Gate 3 deve dichiarare questa ipotesi per i sistemi.
3. Nessun'altra parte di Gate 3 è toccata da F8.

**G★′-NL: no.** Nessun claim F8 lo contraddice. DICT-NS (DIMOSTRATO) e CONV-B1–B3 sono compatibili. Il materiale F8 è lineare in u, o nonlineare solo nei parametri (DICT-RANGO), e non tocca la parte NL. Rivederlo ora sarebbe lavoro senza un innesco.

---

## 6. Stati proposti (solo verso il basso)

Convenzione: "=" significa invariato rispetto alla proposta in LEDGER_ROWS (o in rev2, se più recente); "↓" indica un declassamento o una condizione aggiunta. Nessuno stato sale.

### S8-SYS
| ID | stato proposto |
|---|---|
| SYS-T1 | = DIMOSTRATO come strumento, CON-FONTE in sostanza (Matlis) |
| SYS-R1 | = DIMOSTRATO |
| SYS-N1 | = DIMOSTRATO; nessuna novità (Oberst 1993, da leggere) |
| EX-L1, EX-L2 | = DIMOSTRATO |
| SYS-EX | = DIMOSTRATO; nessuna novità su ℝ^n fino al CIT su Oberst 1990/1993 |
| SYS-EX-C | = DIMOSTRATO |
| SYS-T0 | = DIMOSTRATO (classico) |
| SYS-C1 | = DIMOSTRATO |
| SYS-S1(i⇒), SYS-S1(i⇐) | = DIMOSTRATO |
| SYS-S1-C | = FALSO; parte 𝒟′ rivista da DEVIL-8: corretta, con β(1) ≠ 0 da scrivere (O21) |
| SYS-S1(ii) | = DIMOSTRATO |
| LAME-3 | = DIMOSTRATO con λ + 2μ ≠ 0 |
| SYS-E1, SYS-E2, SYS-E3 | = DIMOSTRATO |
| G-L0 | = DIMOSTRATO |
| G-T2 | = DIMOSTRATO, CON-FONTE in sostanza |
| SYS-N3 | = DIMOSTRATO; nel riassunto scrivere div(ρ²B) = 0 (O15) |
| G-T0 | = osservazione |
| H-DIRAC | = DIMOSTRATO sotto H-DIRAC-1, 2 (allineare NOTAZIONE, O11) |
| SYS-II-T2-C | = FALSO |
| II-T2(b′), Q-S8SYS-1 | = APERTO |

### S8-VAR
| ID | stato proposto |
|---|---|
| VAR-N1 | = DIMOSTRATO |
| VAR-T1(a) | = DIMOSTRATO |
| VAR-L0, VAR-L1 | = DIMOSTRATO (nessuna priorità) |
| VAR-L2 | = DIMOSTRATO (Saut–Scheurer probabile; CIT) |
| VAR-L2-cor | = DA AUDITARE; non citabile da righe DIMOSTRATO (O20) |
| VAR-T1(b) | = DIMOSTRATO in C^{1,2} e in (SF) |
| VAR-T1(c) | = DIMOSTRATO (i)–(iii) |
| VAR-T1(c)-Q10 | = APERTO |
| VAR-T1(c)-F | = FALSO |
| VAR-P3 | = DIMOSTRATO come stima di modulo; ↓ **non** è un certificato di robustezza (O8) |
| VAR-P4 | = DIMOSTRATO dopo VAR-2 |
| VAR-P5(a)(b) | = DIMOSTRATO |
| VAR-P5(c) | = DIMOSTRATO nella classe puntuale; nella classe continua solo la direzione indicata |
| VAR-T2a | = DIMOSTRATO |
| VAR-T6 | = CON-FONTE |
| VAR-E1 | = DIMOSTRATO dopo VAR-3 |
| VAR-E2 | = DIMOSTRATO |
| VAR-VMPUM | = CON-FONTE (solo abstract) |
| VAR-P8(a) | = DIMOSTRATO |
| VAR-P8(b) | = "⟹" DIMOSTRATO; "⟸" CON-FONTE |
| VAR-P8(c) | = DIMOSTRATO |
| VAR-P8(d) | = forma chiusa DIMOSTRATO; sviluppo V-ex |
| VAR-P9 | = DIMOSTRATO |
| VAR-P11 | = (a)–(d) DIMOSTRATO; (e) CON-FONTE (B ∈ C¹) |
| VAR-T10 | = (1), (3)(i)–(ii) DIMOSTRATO; (3)(iii) CON-FONTE + V-ex; (2), (5) CON-FONTE; (4) CON-FONTE con normalità (Casas) |
| VAR-T10-F | = FALSO solo nella forma indicata; la frase F6 su cos t = 0 è VERA (O3) |
| VAR-P12 | = (a)–(c) DIMOSTRATO; (d) APERTO |
| VAR-C3Q2 | = (a)–(g) DIMOSTRATO; chiuso per L monico in ∂_t |
| VAR-C3Q2-open | = APERTO |

### S8-ENC
| ID | stato proposto |
|---|---|
| ENC-D | = DEFINIZIONE |
| ENC-K0 | = DIMOSTRATO |
| ENC-1 | = DIMOSTRATO (Marchenko come confronto) |
| ENC-U1 | = DIMOSTRATO |
| ENC-C1 | = DIMOSTRATO |
| ENC-T2 | = DIMOSTRATO come lemma a q noto, nel sottoanello pari |
| ENC-T2(c′) | ↓ PROVA SCRITTA; DIMOSTRATO solo dopo il recepimento di ENC2-6 (O10) |
| ENC-P0(a) | = DIMOSTRATO sotto (H-P0) |
| ENC-P0(b) | = DIMOSTRATO (portata: non esclude un encoder di tipo ENC-1) |
| ENC-P0(b)^cl | ↓ PROVA SCRITTA; DIMOSTRATO solo dopo ENC2-1 (O10) |
| ENC-P0(b)^loc | ↓ PROVA SCRITTA; DIMOSTRATO solo dopo ENC2-1 (O10) |
| ENC-P0′ | astratto = DIMOSTRATO; nucleo denso ↓ DIMOSTRATO solo dopo il recepimento rev2; esempi: identità DIMOSTRATO, unicità CON-FONTE |
| ENC-P0′-DIC | ↓ **FALSO come scritto** (ENC2-4; SymPy C). La forma esistenziale («esiste un rappresentante con θ = id ⟺ α ≡ 0») è PROVA SCRITTA, da auditare dopo il recepimento |
| ENC-P0-sintesi (rev. 1) | = FALSO come scritto |
| POLE-N | = DIMOSTRATO dopo ENC-4 |
| POLE-N^cl | ↓ PROVA SCRITTA; DIMOSTRATO solo dopo ENC2-5 |
| ENC-N1 (F6) | = FALSO; da togliere da G★″ (O1) |
| ENC-N1′ | = DIMOSTRATO **solo** come lemma di riduzione |
| ENC-K1′ | = DIMOSTRATO dopo ENC-9; nessuna novità (Andrianov–Sokolov) |
| ENC-K1 | = CON-FONTE da verificare |
| ENC-TAB | = SINTESI; correggere la colonna "eccezioni" (O2) |
| ENC-A9(a) | = DIMOSTRATO |
| ENC-A9(b) | ↓ (b1), (b2) corretta e (b4) DIMOSTRATO; (b3) CON-FONTE + V-ex (eredita VAR-T10(3)(iii); O16) |
| NS-EQ-Ω | = DIMOSTRATO dopo ENC-10 |
| FAD-1 | = DIMOSTRATO dopo ENC-11 |
| GAM-O1 | = OSSERVAZIONE + CON-FONTE |
| FW-1 | = DIMOSTRATO per il caso libero; con V CON-FONTE |
| ENC-L1 | = FUSO in VAR-P8(a) |

### S8-DICT
| ID | stato proposto |
|---|---|
| DICT-U1 | = DIMOSTRATO |
| DICT-U1b | = singolari e L^p DIMOSTRATO; velocità CON-FONTE |
| DICT-U2, DICT-N2 | = DIMOSTRATO |
| DICT-U3c | = DIMOSTRATO; caso dipendente da x CON-FONTE |
| DICT-U3d | = DIMOSTRATO |
| DICT-U3d-v | = CANDIDATO |
| DICT-RIT1, DICT-N3, DICT-CS1, DICT-U4 | = DIMOSTRATO |
| DICT-N1, N1iii, N1iv-bc, N1v | = DIMOSTRATO (N1(i)–(iii) classici: nessuna novità) |
| DICT-RANGO | = DIMOSTRATO come ID-ker; ↓ non è "identificazione" senza (H-ex) (O5) |
| DICT-RANGO-cor | = DIMOSTRATO dopo DICT-2 e DICT-3; stessa riserva (H-ex) |
| DICT-MAG | = rinviato a SYS-N3 (DIMOSTRATO lì) |
| DICT-MAG-NU | ↓ PROVA SCRITTA; DIMOSTRATO solo dopo MAG-1 e MAG-2. Corollario di SYS-N3(c), non un claim autonomo (O15) |
| DICT-N1vi | = FALSO |
| DICT-MF, DICT-A | = DIMOSTRATO |
| DICT-A-iii | = DIMOSTRATO dopo DICT-1 |
| DICT-B2 | = DIMOSTRATO (classico) |
| DICT-B3 | = CON-FONTE da verificare |
| DICT-R3 | = DIMOSTRATO (classico) |
| DICT-GR | = DIMOSTRATO; etichetta (ID) → (H-ID) (O13) |
| DICT-R6 | = DIMOSTRATO per (a)–(e); ↓ (f) va riscritto con la citazione di N1(ii) e del Teorema A, altrimenti dipende da DA AUDITARE (O19) |
| DICT-ILIM, ILIM-H0 | = DIMOSTRATO |
| DICT-ILIM-Hs | = CANDIDATO |
| DICT-NS | = DIMOSTRATO |
| DICT-2KINK | = V-ex |
| DICT-AX | = CON-FONTE |
| DICT-R4, DICT-PAINLEVE | = STRUMENTO |

### S8-CONV
| ID | stato proposto |
|---|---|
| CONV-L1, T1, T2 | = DIMOSTRATO (T2: Σ⁰₂ standard, nessuna novità) |
| CONV-T2′ | = PROVA SCRITTA; DIMOSTRATO solo dopo che T2P-1…3 sono applicati nel PROOF_PACKAGE (oggi assenti; O10) |
| CONV-T3, T5, T6 | = DIMOSTRATO |
| CONV-T4 | = DIMOSTRATO; numero del teorema di Stein CIT |
| CONV-P6, P7, P8 | = DIMOSTRATO (P7: tricotomia relativa a 𝒦) |
| CONV-D1 | = DIMOSTRATO |
| CONV-D2 | = CON-FONTE (Malgrange; solo C^∞) |
| CONV-B1, B2, B3 | = DIMOSTRATO |
| CONV-T8 | = DIMOSTRATO in L²; ordine 1 in L^∞ V-ex |
| CONV-R1 | = DIMOSTRATO |
| CONV-R1-F | = FALSO |
| CONV-MZ1, MZ2, MZ3 | = DIMOSTRATO |
| CONV-MZ3-F | = FALSO |
| CONV-T7 | proposizione = DIMOSTRATO; contratto ↓ la voce "Magnus (B)" diventa condizionata (dimensione finita, oppure ipotesi di Casas Thm 3.4 in rappresentazione d'interazione); altrimenti Dyson (O4) |

---

## 7. Verdetto e fix per il coordinatore

**Verdetto.** G★″ **sopravvive** come impianto (nessuna obiezione FATAL), ma **non passa il Gate 8 nel testo attuale**: O1 e O2 sono frasi FALSO in PROBLEM e in SYNTHESIS-2.

**Fix, in ordine.**
1. PROBLEM, punti 4 e 6, e SYNTHESIS-2, righe 10, 38, 39 e 70: togliere ENC-N1 e "cambiano il tempo" (O1, O2).
2. SYNTHESIS-2 riga 35: ritirare la mia F5 (O3). NOTAZIONE v6: normalizzazione H = −∂² + x².
3. Recepimento rev2 (ENC2-1…6, MAG-1…5) e T2P-1…3 prima di qualsiasi promozione (O10).
4. Contratto CONV-T7: Magnus condizionato (O4).
5. NOTAZIONE v6: etichette ID-*, (H-ex), (E2) con c(t), (H-ID), condizione di H-DIRAC (O5, O11–O13).
6. Gate 8a e 8b come ai §4 e §5.
7. CIT-AUDIT prima del Gate 9: Oberst 1990/1993, Saut–Scheurer, Andrianov–Sokolov (O6).
8. MINOR O14–O21 secondo il §2.
