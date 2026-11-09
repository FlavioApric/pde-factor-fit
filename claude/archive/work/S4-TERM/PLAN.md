# PLAN — S4-TERM (Fase 4, sessione prioritaria) · 26/10/2026
Oggetto: punto 1 di G★′-NL (PROBLEM.md). **E_int = A9 di NOTAZIONE v3** (flussi dei *singoli* termini; non E^NL, E^trop, E^mix — DEVIL-4 O1).

## 0. Skill caricate (Regola 2: lettura integrale dei SKILL.md, nessuno script _vendor eseguito)
1. `skills-local/session-protocol` (per prima) · 2. `skills-local/claim-lifecycle`
3. `_vendor/Auto-claude-code-research-in-sleep/skills/formula-derivation/SKILL.md` — fissare l'oggetto invariante (E^add, E^mult_{AB}, E^mult_{BA}) e classificare ogni passo identità / proposizione / approssimazione.
4. `_vendor/Auto-claude-code-research-in-sleep/skills/proof-writer/SKILL.md` — PROOF_PACKAGE con stato per claim (PROVABLE AS STATED / AFTER EXTRA ASSUMPTION / NOT JUSTIFIED).
5. `_vendor/math-skill/SKILL.md` (modo `proof`: controesempi presto, esplorazione separata dalla prova).
6. `_vendor/scientific-agent-skills/skills/sympy/SKILL.md` — solo verifica (work/S4-TERM/sympy/, `.venv\Scripts\python.exe -I`).
7. `_vendor/Auto-claude-code-research-in-sleep/skills/kill-argument/SKILL.md` — sul risultato principale; revisori = due subagenti Claude freschi (attacco ~200 parole; aggiudicazione per punti), niente Codex.

## 1. Domande (G★′-NL punto 1; appunti A9, B1; item P1/P3)
Burgers u_t = A(u) + B(u), A = ν∂², B(u) = −uu_x. S_A = calore; S_B = semigruppo entropico di Kružkov di u_t + (u²/2)_x = 0 (anche oltre lo shock); S = flusso pieno.
E^add(t) = S(t)u₀ − S_A(t)u₀ − S_B(t)u₀ + u₀; E^mult_{AB} = S(t)u₀ − S_A(t)S_B(t)u₀; E^mult_{BA} = S(t)u₀ − S_B(t)S_A(t)u₀.
- Q1 (getto): sviluppo in t con resto; coefficiente t² (atteso ½{A,B′} per E^add, commutatore per E^mult); dipendenza da ε (ampiezza) e ν.
- Q2 (prima dello shock, t < t* = −1/min u₀′ = 1/(ε max(−w₀′))): stima con ordine e costanti esplicite; forma chiusa?
- Q3 (oltre t*): stima di ordine esplicito oppure teorema negativo.
- Q4: KdV–Burgers, Fisher–KPP (non integrabili).
- Q5: costo e confronto con il lineare (P1-T2/T3, P1-T5).
**Dominio (O4).** Ω limitato: solo il quadro formale (getto in t, modello M2) è canonico; i flussi S_n su Ω sono determinati solo per il termine iperbolico (velocità finita), non per il calore (P1-P1). Il **caso di controllo dichiarato è 𝕋** (e ℝ dove indicato).

## 2. Predizioni (registrate PRIMA del lavoro, DEVIL-4 O6)
- PR1: coefficiente t² di E^add = ½(A′B + B′A)(u₀) = −ν(2u₀′u₀″ + u₀u₀‴); di E^mult_{AB} = ½(B′A − A′B)(u₀) = νu₀′u₀″, E^mult_{BA} = −νu₀′u₀″. Ogni coefficiente t^k è O(ν·ε²) (nessun termine lineare in ε).
- PR2: prima di t*, ‖E^add(t)‖_∞ = O(ν) con costante che esplode a t → t* (attesa potenza di (1 − t/t*)).
- PR3: oltre t* **teorema negativo** in L^∞: E^add eredita il salto di S_B(t)u₀ (indipendente da ν); in L¹ la stima sopravvive con ordine peggiore (attesa ν^{1/2} per lo splitting).
- PR4: KdV–Burgers: stessa ostruzione (S_B identico). Fisher–KPP: nessuno shock, stima O(ν) su ogni [0,T] ma non uniforme in t.
- Probabilità a priori che il criterio d'uscita scatti con un **teorema negativo** (non con una stima t² oltre lo shock): ~80%.

## 3. Criterio d'uscita (SESSIONS.md, scheda S4-TERM)
Una stima di ordine esplicito (atteso t²) valida oltre lo shock, **oppure** un teorema negativo registrato (con prova scritta e CHECK_REQUEST). Minimo consegnabile se la sessione fallisce: teorema del getto (Q1) + teorema negativo in L^∞ (Q3) con prove.

## 4. Strumenti e input
Serie di Lie / derivazioni evolutive (Gröbner); caratteristiche e Lax–Oleinik (CON-FONTE: Evans PDE §3.4); Hopf–Cole + metodo di Laplace (Hopf 1950); principio del massimo parabolico; Kružkov, Brezis–Pazy (quadro); NF-1 (F4-HOR), F4L-P2 (F4-LIFT), LIN-Q3 (F4-LIN), P1-T2/T3/T5, P3-T1.

## 5. Contatti
S4-INTEG (DOMANDA: stato di F4L-P3 e di Lax–Oleinik/Kružkov come lemmi di trasporto); S4-ID (AVVISO: stesse u; il getto di E^add è un polinomio differenziale in u₀, utile come test di dizionario); S-CHECK (CHECK_REQUEST); central (PLAN-READY, TABELLA LEDGER, DONE).

## 6. Consegne
work/S4-TERM/PLAN.md, PROOF_PACKAGE.md (incrementale), CHECK_REQUEST.md, KILL_ARGUMENT.md, sympy/. TABELLA LEDGER in inbox/central.md; DONE S4-TERM.
