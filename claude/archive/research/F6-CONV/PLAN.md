# PLAN — F6-CONV (Fase 6, scouting; R13 + R15; P-C, rumore, dimensione, bordo)

Data: 26/10/2026. Scout: F6-CONV. Stato: scouting (preparatorio, reversibile). Nessun claim DIMOSTRATO: solo "candidato" o "prova scritta".

## Skill caricate (Regola 2: lettura integrale/strumentale del SKILL.md, nessuno script _vendor eseguito)
1. `skills-local/session-protocol` — orientamento, PLAN, inbox, consegne (letta per intera).
2. `skills-local/route-scout` — criteri fissati prima, verdetto promote/park/merge/kill (letta per intera).
3. `skills-local/claim-lifecycle` — stati onesti; qui solo bozza + SymPy (proof-checker e kill-argument rinviati a Fase 8).
4. `_vendor/.../novelty-check` (Fasi A–B: claim chiave, ricerca web; Fase C revisore esterno non disponibile → limite dichiarato).
5. `_vendor/math-skill` (modo `proof`: mappa del problema, passo cardine, controllo dei casi limite).
6. `_vendor/scientific-agent-skills/.../scientific-critical-thinking` (verdetto: separare supportato / ipotesi / da verificare).
7. SymPy (`.venv\Scripts\python.exe -I research/F6-CONV/sympy/<script>.py`) solo come verifica.

## Domande (dal roster e dal compito)
- **Q1 (C1, consistenza).** Al crescere dei dati (jet più lungo, più campioni, dominio più grande) l'uscita converge all'operatore vero? Formulare "identificazione nel limite" lungo una filtrazione 𝓓_n (coordinata con F6-DICT), con velocità, e i limiti esatti dati da C3-P1 (nessun certificato finito), P4-T5 (scatola nera), C3-T3 (soglia 2d−1).
- **Q2 (C1, stabilità condizionale).** Stime di tipo Lipschitz/Hölder/log sotto ipotesi a priori (insieme sorgente), regola di scelta del parametro (discrepanza), nello spirito di Engl–Hanke–Neubauer/Isakov; raccordo con P2-T4 (niente regolarizzazione uniformemente lipschitziana).
- **Q3 (C2, località).** Quando la legge che genera u è differenziale, non locale (frazionaria, integrale, memoria, ritardo) o assente (Ann(u)=0)? Criteri, teoremi di impossibilità; legame con Peetre e con U1/U3 di F6-DICT.
- **Q4 (C3, parti iterative).** Enunciato uniforme per splitting (Lie/Strang, A9), Dyson–Phillips (P3-T1), Magnus (coordinato con F6-VAR).
- **Q5 (casi extra).** Dati rumorosi; dimensione Ω ⊂ ℝ^{1+d}, d ≥ 2 (cosa sopravvive di C3-T1, C12-T1′: Ehrenpreis–Palamodov, Hartogs); condizioni al bordo (P3-T3).
- **Q6.** Domanda guida comune (I/S/E) per ogni strada; novelty-check.

## Criteri FISSATI PRIMA DI CERCARE (route-scout §1)
Una strada (= enunciato candidato + metodo) è:
- **PROMUOVI** se (a) dà un enunciato candidato con ipotesi esplicite e prova scritta (o fonte con numero di teorema), (b) risponde a una delle domande Q1–Q5 in forma che il LEDGER non contiene già, (c) è compatibile con i teoremi negativi C3-P1, P4-T5, P2-T4, R5-T2[H^m] FALSO (non li contraddice; se li usa, li cita), (d) è analitica (niente ML/statistica come metodo), (e) costo stimato in Fase 8 ≤ 1 sessione S8-CONV.
- **PARCHEGGIA** se l'enunciato è plausibile ma la prova poggia su una fonte non verificata, su un caso solo V-ex, o costa > 1 sessione.
- **ELIMINA** se contraddice un teorema del LEDGER, richiede ML/regressione statistica come metodo, oppure è identica a un risultato noto senza contributo al progetto (in quel caso si registra come CON-FONTE candidata, non come strada).
- **Teorema negativo** = sempre tenuto (anche se piccolo) se marca il confine di un enunciato positivo promosso (regola N1).

## Fonti / stringhe previste
Gold 1967 (identification in the limit), Angluin 1980 (tell-tale), Engl–Hanke–Neubauer 1996, Isakov (Inverse Problems for PDE), Wedin 1972 (sin θ), Adams–Fournier (interpolazione), Peetre 1959/60, Hörmander ALPDO/ICASV (7.6, Ehrenpreis–Palamodov), Palamodov 1970, Ehrenpreis 1961 (Hartogs), Trotter 1959, Chernoff 1968, Kato, Engel–Nagel III.1 e III.3, Moan–Niesen 2008 / Blanes–Casas–Oteo–Ros 2009 (Magnus), Jahnke–Lubich 2000, Hansen–Ostermann, Einkemmer–Ostermann 2015 (riduzione d'ordine con Dirichlet), Kechris (classi di Baire). Stringhe: "identification in the limit differential equation", "order reduction Strang splitting Dirichlet 1.25", "Poisson semigroup harmonic extension", "consistency sparse identification PDE" (solo per confronto di novità).

## Contatti
- F6-DICT (hub): interfaccia filtrazione 𝓓_n ↔ consistenza (proprietà F1–F3 richieste alla filtrazione), U1/U3 ↔ località.
- F6-VAR: Magnus/Dyson per V(t,x) — io do l'enunciato uniforme, loro i raggi.
- central-F6: PLAN-READY, TABELLA, DONE (avviso del coordinatore: NON `inbox/central.md`).

## Criterio di "fatto"
VERDETTO.md (1–2 pp.) con: risposta a Q1–Q5, enunciati candidati con ipotesi, teoremi negativi, I/S/E, costo, novità, raccomandazione per strada secondo i criteri sopra; NOTE.md con le prove scritte; sympy/ con almeno i controlli degli esempi chiave; sources.bib; open_questions.md; TABELLA e DONE in inbox/central-F6.md.
