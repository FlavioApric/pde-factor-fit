# FASE 4 — sprint di scouting delle strade non lineari (roster v1, 26/10/2026)

**Perché parte adesso.** Il piano (Fase 4) apre con uno *sprint di scouting* (horizon scout + skill `route-scout`) e decide le strade solo al **Gate 4a** con l'utente. Lo scouting è preparatorio e reversibile: non promuove strade, non dichiara claim DIMOSTRATI, non cambia PROBLEM.md. Parte in parallelo al Gate 3 su richiesta dell'utente (26/10). Se al Gate 3 l'utente cambia la decisione di struttura, il coordinatore manda un AVVISO agli scout, e il Gate 4b ricontrolla comunque la struttura lineare.

## Regole comuni (tutti gli scout)
1. Carica per prima `skills-local/session-protocol`, poi `skills-local/route-scout` (workflow: nota → PLAN di scouting → skill di ricerca/prova → verdetto di 1 pagina → riga per ROUTES.md) e `skills-local/claim-lifecycle` (per gli stati).
2. **PLAN prima di tutto** (`research/<ID>/PLAN.md`), con **criteri di promozione ed eliminazione fissati PRIMA di cercare** (piano: "kill criteria are fixed before work starts"). Poi `PLAN-READY <ID>` in `inbox/central.md`.
3. **Domanda guida comune** (scalare per primo, Burgers u_t + u u_x = ν u_xx come banco di prova; poi KdV, NLS se pertinente): la strada permette di trasportare al caso non lineare i tre risultati lineari di Fase 3?
   - (I) **identificazione** dell'operatore da una soluzione (lineare: C3-T1, Ann(u) = (P) ⟺ test EP; P4-T2);
   - (S) **scomposizione** in componenti (lineare: C12-T1′ per fattori; P1-T2 per termini nella classe 𝔅);
   - (E) **E_int** in forma chiusa o con stima, e il suo costo (lineare: P1-T3; non continuità in H^m, P1-P1(e)).
   Rispondi per ciascuno: sì (con enunciato candidato) / parziale / no (con ostruzione), più costo e novità (novelty-check).
4. **Stati onesti.** Ogni enunciato nuovo resta "candidato" o "prova scritta"; niente DIMOSTRATO senza S-CHECK. Riferimenti solo verificati (DOI/arXiv/numero di teorema controllato) o marcati "da verificare".
5. **Comunicazione** (`inbox/<ID>.md`, solo append, formato di PROTOCOLLO.md Regola 3). Leggi la tua inbox all'inizio, a metà e prima di consegnare; rispondi alle DOMANDE. Grafo:
   - F4-ALG ↔ tutti (è il "hub": traduce ogni strada nel linguaggio dell'ideale differenziale di u, l'analogo non lineare di Ann(u));
   - F4-LIN ↔ F4-INT (Cole–Hopf/Miura/Darboux ↔ coppie di Lax e IST);
   - F4-LIFT ↔ F4-ALG (Carleman/Koopman ↔ chiusura dell'ideale);
   - F4-HOR → central (NEW-ROUTE) e → chi è toccato;
   - tutti → central (PLAN-READY, NEW-ROUTE, TABELLA righe ROUTES, DONE).
6. Scrivi solo in `research/<ID>/` e `inbox/`. Non eseguire script dei repository `_vendor`. SymPy: `D:\ProblemaBase\.venv\Scripts\python.exe -I`, script in `research/<ID>/sympy/`, solo come verifica.
7. Consegne: `PLAN.md`, `VERDETTO.md` (1 pagina: strada, risposte I/S/E, enunciati candidati, ostruzioni, costo, novità, raccomandazione PROMUOVI / PARCHEGGIA / ELIMINA secondo i criteri del PLAN), `sources.bib`, `open_questions.md`, `NOTE.md` (lavoro di dettaglio). Ultima riga in central: `DONE <ID>`. Salva su disco man mano, così il lavoro è riprendibile.

## Roster
| ID | Strade (piano Fase 4) | Contenuto | Input |
|---|---|---|---|
| **F4-LIN** | (iv) linearizzazioni esatte | Cole–Hopf (Burgers) e Cole–Hopf tropicale RT-R7b (pesi softmax, ν→0 Hopf–Lax, E_int sugli shock); Miura (KdV ↔ mKdV), Darboux/Bäcklund. Trasporto di I/S/E attraverso la mappa linearizzante: quali risultati di Fase 3 sopravvivono a una sostituzione non lineare? | research/R7, research/PR-C2c, SCOUT-1 (TROP), work/SCOUT-TROP, ROUTES RT-R7b |
| **F4-INT** | (iv) IST / Lax / Hirota | RT-R7a (IST = log-simbolo non lineare: dati di scattering evolvono con la dispersione linearizzata), Hirota (E_int a coppie per N-solitoni, sfasamenti), ostruzione da simmetria RT-R7c (1-solitone KdV non identifica). Identificazione da UNA soluzione per KdV/NLS | research/R7 §4–5, PR-C2c, ROUTES RT-R7a, RT-R7c |
| **F4-ALG** | (v) algebra differenziale (hub) | Analogo non lineare di Ann(u): ideale differenziale {F : F(u, u_t, u_x, …) = 0} (Ritt–Raudenbush, Kolchin), implicitizzazione differenziale, decomposizione in componenti primarie (analogo di "componente = fattore"), test di identificabilità a la C3-T1, dimensione differenziale; rapporto con il modulo canonico R·u della decisione di struttura (GATE3.md §2) | work/C3, work/P4, work/II §10, GATE3.md |
| **F4-LIFT** | (i) e (iii) sollevamenti | Carleman (embedding polinomiale in ℓ²/Fock), Koopman (operatore di composizione, spettro), spazio di Hilbert costruito per assorbire la non linearità. Domanda chiave: il troncamento di Carleman conserva la struttura di annullatore/fattori? E_int del sistema sollevato vs E_int non lineare | research/R1, work/C1C2 (funtore C1.0), work/P1, work/P3 (Dyson), ROUTES |
| **F4-HOR** | (ii) + (v) orizzonte | f(S·x) per componenti degli appunti (route ii); Painlevé, forme normali, operatori monotoni / semigruppi non lineari (Crandall–Liggett), teoria spettrale non lineare. Compito: scout di orizzonte, almeno una strada non-seme scoutata o eliminata con motivi (piano v4) | research/SCOUT-1, SCOUT-2, ROUTES, appunti nel piano |

## Dopo lo sprint
Il coordinatore raccoglie i VERDETTI in una tabella per il **Gate 4a** (scelta delle strade con l'utente; più strade possono andare in parallelo; criteri di eliminazione già fissati) e aggiorna ROUTES.md. Nessuna sessione di dimostrazione di Fase 4 parte prima del Gate 4a.
