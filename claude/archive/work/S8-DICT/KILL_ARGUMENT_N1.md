# KILL_ARGUMENT_N1 — S8-DICT (27/10/2026)

**Oggetto:** N1(i)–(v) con il Teorema RANGO e i corollari (a′)/(b′), PROOF_PACKAGE §2, e il Teorema A(iii), §3.3.
**Modalità:** kill-argument interno, secondo la pratica DEVIL-6. **Revisore fresco non disponibile**: nessun subagente è stato avviato, perché il task lo esclude. Il verdetto va quindi letto come auto-revisione e non sostituisce S-CHECK.

## Memo d'attacco (circa 200 parole)
N1 dice che l'identificazione di una legge da dati finiti è impossibile in generale, che il fit non è certificabile, che il dizionario non può avere un livello finito universale e che le leggi generiche non soddisfano nessuna equazione del dizionario. L'attaccante sostiene sette punti.
(P1) È tutto classico: l'impossibilità da dati finiti è folklore della teoria dell'identificazione.
(P2) "Generico" in senso di Baire è debole, perché un insieme magro può avere misura piena.
(P3) I dati di interesse sono soluzioni di qualche legge, quindi la genericità su C^∞ è irrilevante.
(P4) Il Teorema A(iii) usa perturbazioni a supporto compatto, che con atomi non locali (memoria, simboli) non restano localizzate.
(P5) Il risultato dipende dalla topologia: in H^m le cose potrebbero cambiare.
(P6) (iv) confonde i modelli di calcolo, perché con un oracolo reale BSS tutto diventa decidibile.
(P7) Il teorema di rango è banale (algebra lineare puntuale), e il caso intermedio, dove la mappa residua non è né iniettiva né suriettiva, è proprio quello interessante e resta scoperto.

## Difesa punto per punto
- **P1: risposto.** I pezzi classici sono dichiarati prior art (Hahn–Banach, Gram, Weyl, OLS). Il contenuto proprio è la combinazione: certificato di misfit Σ₁ robusto, fit non certificabile nemmeno con dati esatti finiti (A(iii)), e genericità anche in prevalenza.
- **P2: risposto.** N1(v) è dimostrato sia magro sia shy (prevalenza di Christensen e Hunt–Sauer–Yorke), con una sonda finito-dimensionale costruita su una base adattata al grado (SymPy F10). Le fonti della prevalenza restano "da verificare".
- **P3: risposto in parte.** Teorema A(iii) e N1(iii) lavorano dentro classi di soluzioni: i dati v costruiti hanno gli stessi funzionali di u. La genericità di N1(v) resta però su C^∞, e la versione relativa a una varietà di soluzioni non è dimostrata.
- **P4: non risolto, ambito ristretto.** A(iii) è enunciato solo per atomi locali, con un aperto d'indipendenza dichiarato. Gli atomi non locali sono la domanda aperta Q4.
- **P5: risposto.** U_n è aperto anche in D′ (MF3); N1(v) vale in C^∞ e, con la stessa prova, in H^m per m maggiore dell'ordine.
- **P6: risposto.** (iv) separa i modelli: (T) non decide, (BSS) decide nel limite (CONV-T1) senza bound, e CONV-T2 dà il limite del ramo rumoroso. Nessuna affermazione mescola i due modelli.
- **P7: risposto in parte.** RANGO è volutamente elementare. Il suo valore è la tricotomia identificabile / non falsificabile / intermedio, con il conteggio K·dim𝔽 contro la dimensione dei valori. Il caso intermedio (divisione e rango variabile) è la domanda aperta Q3.

## Verdetto
**PASS-WITH-NOTES.** Le note sono tre.
1. A(iii) vale solo per atomi locali (Q4).
2. La genericità di N1(v) non è relativa a varietà di soluzioni.
3. RANGO lascia aperto il caso intermedio (Q3).
Nessun claim è declassato a FALSO, tranne N1(vi) originale, già ritirato (§7). Revisore fresco non disponibile.

---

## Aggiornamento del 27/10/2026: kill-argument indipendente
S-CHECK-F8-DICT ha rifatto il kill-argument da zero, con un subagente nuovo: `work/CHECK-F8/KA_DICT_N1_{input,attack,adjudication}.md`. L'esito è **SURVIVES-WITH-FIXES**: 11 punti, 6 major, nessuno critical sulla scala KA.

Questo KA interno (PASS-WITH-NOTES) **non** aveva trovato i punti P1–P6, e il verdetto valido è quello indipendente.

I fix sono recepiti in PROOF_PACKAGE (vedi `RECEPIMENTO.md`). In particolare la nota 1 del verdetto qui sopra ("A(iii) solo per atomi locali con aperto d'indipendenza") è superata: per DICT-1 A(iii) vale per atomi differenziali senza ipotesi aggiuntive. Restano aperti solo gli atomi non locali (Q4).
