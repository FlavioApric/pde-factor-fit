# PLAN — F6-HOR (scout di orizzonte, Fase 6) · 26/10/2026

## 0. Mandato
Revisione una tantum di TUTTE le strade parcheggiate (e, in breve, delle eliminate/fuse con motivi) di ROUTES.md e dei verdetti di Fase 1/4 (SCOUT-1, SCOUT-2, F4-*) rispetto ai nuovi problemi P-A (sistemi/Dirac/gauge), P-B (coefficienti variabili e non autonomi: B1 identificare V, B2 rimuovere V), P-C (convergenza C1/C2/C3), P-D (dizionario universale, misfit, migliore approssimazione, arricchimento) e casi extra (non locali/frazionari/ritardo, rumore, dimensione > 1+1, bordo, potenziali singolari, non linearità non polinomiali sine-Gordon, e^u). Piano originale, Fase 5: "Parked routes from all phases are reviewed one final time before Problema 1/2 reopen". Più almeno una strada NON-seme scoutata o eliminata con motivi.

## 1. Skill caricate (lettura integrale/strutturale di SKILL.md, nessuno script _vendor eseguito)
1. `skills-local/session-protocol` (Passi 0–4), `skills-local/route-scout` (procedura NEW-ROUTE → verdetto), `skills-local/claim-lifecycle` (stati onesti: candidato / prova scritta / V-ex; nulla DIMOSTRATO).
2. `_vendor/.../novelty-check` (fasi A–B, verdict limits; fase C cross-model non eseguita: Codex escluso dall'utente → REVIEW_UNAVAILABLE).
3. `_vendor/math-skill` (modo `proof`: controesempi presto) + SymPy solo come verifica (`.venv\Scripts\python.exe -I research/F6-HOR/sympy/<script>.py`).
4. `_vendor/scientific-agent-skills/.../scientific-critical-thinking` (struttura del verdetto: punti forti, criticità per gravità, rimedio).
5. Ricerca: WebSearch diretto (al posto di research-lit/arxiv, i cui script non si eseguono); `anthropic-skills:deep-research` NON usato (orchestra sotto-agenti: non autorizzato).

## 2. Criteri fissati PRIMA di cercare
### 2a. Revisione delle strade parcheggiate — esito per ciascuna
- **RIAPRI → <scout>** se TUTTE: (R1) il trigger di parcheggio registrato è scattato con l'apertura di P-A/P-B/P-C/P-D o di un caso extra, oppure la strada dà a uno di essi un oggetto che i semi di FASE6_SCOUTING.md non contengono già; (R2) è analitica (niente ML, niente regressione statistica come metodo); (R3) si può scrivere un enunciato candidato o una domanda decisiva con caso di prova minimo nella scala L6–L10; (R4) almeno una risposta I/S/E (regola 3) è "sì" o "parziale".
- **RESTA PARCHEGGIATA** se il trigger non è scattato oppure scatta ma la strada è già coperta da un seme dello scout competente (allora: "coperta da <seme>", nota informativa).
- **ELIMINA (kill)** se: viola il vincolo no-ML, oppure il suo contenuto si riduce a un lemma già registrato senza oggetto nuovo per P-A…P-D, oppure il caso di prova minimo la confuta.
- Eliminate di fasi precedenti: si conferma l'eliminazione salvo che (R1)–(R4) valgano ora (allora RIAPRI).
### 2b. Strade NON-seme (non elencate in FASE6_SCOUTING.md)
- **PROMUOVI (→ NEW-ROUTE + scout destinatario)** se: (N1) caso di prova minimo superato in SymPy (V-ex) o enunciato con fonte verificata; (N2) dà a P-A…P-D qualcosa che i semi non danno (enunciato di esistenza/non esistenza, criterio decidibile, encoder esplicito); (N3) novelty-check fasi A–B non ABANDON, oppure, se noto, la lettura per il progetto è nuova e dichiarata; (N4) analitica.
- **PARCHEGGIA** se (N1) e (N4) valgono ma (N2) è solo parziale o il costo supera una sessione di Fase 8 senza un enunciato chiaro.
- **ELIMINA** se (N2) fallisce (contenuto già in un seme o in un lemma registrato) o se il caso di prova la confuta.
### 2c. Fatto quando
Ogni strada parcheggiata/eliminata di ROUTES.md + GATE4A + verdetti SCOUT/F4 ha una riga con decisione e motivo; ≥ 1 non-seme con verdetto motivato e caso di prova; risposta I/S/E per ogni strada che raccomando di riaprire; NEW-ROUTE in inbox (central-F6.md per avviso del coordinatore) e avviso agli scout toccati; consegne PLAN, VERDETTO, NOTE, sources.bib, open_questions; `DONE F6-HOR`.

## 3. Inventario da rivedere (dalla lettura iniziale)
Parcheggiate: RT-5, RT-S1e RIGID, RT-S1f STOKES, RT-R1b, RT-S2d Mori–Zwanzig, RT-S2a Faddeev, RT-R7a fuori da 𝓗, Koopman, PAINLEVÉ(+POLE), NLSPEC, HAANTJES, MON (identificazione), F4-ALG autonoma. In scouting/sospese: RT-S1b NAT, RT-S1c MOB, RT-S1d EXT, RT-R2a (H0 ℝ/𝕋). Eliminate/fuse con motivi: RT-S1g MICRO (core), SPLIT-f, S4-LIFT autonoma, RT-S2c MPUM, RT-D2, RT-R4a, RT-R1a, RT-S1h, RT-R7c, WIENER, e dagli scout: Clifford (parcheggiata fino a Fase 5), Galois parametrizzato, probabilità libera, Riemann–Hilbert come encoder, gamblets/omogeneizzazione, Magnus/Floquet–Hill, rinormalizzazione, deconvoluzione cieca, ICA, Prony multivariato.
Non-seme candidate: (a) gruppoide di equivalenza / trasformazioni ammissibili (Lie–Ovsiannikov) come encoder di V; (b) Galois differenziale (Picard–Vessiot, Kovacic) + monodromia banale (Adler–Moser, Duistermaat–Grünbaum) per l'esistenza di un encoder differenziale; (c) algebra differenziale esponenziale (Ax–Schanuel) + test di Painlevé per sine-Gordon/e^u; (d) Clifford (verificare se è seme), quiver, fasci/microlocale (Kashiwara–Schapira, varietà caratteristica dei sistemi). Casi di prova minimi: oscillatore armonico (lens/Niederer), −2/x² e Pöschl–Teller (Darboux), kink di sine-Gordon e Liouville; Dirac libero (varietà caratteristica, proiettori ±).

## 4. Contatti
→ central-F6 (PLAN-READY, NEW-ROUTE, TABELLA, DONE); → F6-SYS, F6-VAR, F6-ENC, F6-DICT, F6-CONV per le strade riaperte verso di loro (AVVISO/NEW-ROUTE). Leggo inbox/F6-HOR.md all'inizio, a metà e prima di consegnare.

## 5. Nota di processo
Il compito iniziale chiedeva `inbox/central.md`; il coordinatore (AVVISO 26/10) ha poi chiesto di usare `inbox/central-F6.md`. Seguo l'AVVISO: nessuna scrittura in central.md.
