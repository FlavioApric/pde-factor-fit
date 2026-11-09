# PLAN — F4-ALG (Fase 4, sprint di scouting, strada (v) algebra differenziale — HUB)
Data: 26/10/2026 · Agente: F4-ALG · Regole: FASE4_SCOUTING.md (lette per intero), PROTOCOLLO.md, skills-local/session-protocol, route-scout, claim-lifecycle.

## 0. Contesto letto (Passo 0)
FASE4_SCOUTING.md, RIPRESA.md (ultimo AGGIORNAMENTO 26/10: sprint di scouting avviato, F4-ALG = hub), PROTOCOLLO.md, NOTAZIONE.md (v1+v2), PROBLEM.md (G★′, ladder L5 = non lineare), GATE3.md (decisione di struttura: oggetto canonico M = R·u ≅ R/Ann(u), ancora da approvare), claims/LEDGER.md, ROUTES.md (RT-R7a/b/c), work/C3/PROOF_PACKAGE.md (C3-L1, L2, L3, T1, T6, C2, P3), work/P4/PROOF_PACKAGE.md (P4-T1, T2 modulo ciclico, T4/T5 decidibilità), work/II/PROOF_PACKAGE.md §10, research/R7 (R7-L4). Inbox inbox/F4-ALG.md vuota all'inizio.

## 1. Skill caricate (lettura integrale dei SKILL.md; nessuno script _vendor eseguito)
1. skills-local/session-protocol (per primo), skills-local/route-scout, skills-local/claim-lifecycle — workflow, stati, consegne.
2. _vendor/Auto-claude-code-research-in-sleep/skills/research-lit — ricerca: solo sorgente `web` (WebSearch/WebFetch); helper Python (arxiv_fetch, verify_papers) NON eseguiti (script _vendor vietati) ⇒ ogni voce bibliografica marcata verificata solo se controllata a mano su pagina editore/arXiv/zbMATH, altrimenti "da verificare".
3. _vendor/scientific-agent-skills/skills/literature-review — registrare stringhe di ricerca e data (NOTE.md §Ricerca), sintesi tematica, niente conteggi PRISMA (scouting, non revisione sistematica).
4. _vendor/Auto-claude-code-research-in-sleep/skills/novelty-check — per il candidato principale: 3–5 claim, ≥3 formulazioni di ricerca per claim, blocco "verdict limits" applicato da me (revisore esterno escluso: niente Codex; limite dichiarato nel verdetto).
5. _vendor/math-skill (modo `proof`: esplorazione separata dalla prova, controesempi prima) + _vendor/scientific-agent-skills/skills/sympy — verifiche in research/F4-ALG/sympy/, `D:\ProblemaBase\.venv\Scripts\python.exe -I`, solo come controllo.

## 2. Domanda decisiva
L'ideale differenziale di una soluzione, I(u) = {F ∈ ℂ{y} : F(u, u_t, u_x, …) ≡ 0} (anello dei polinomi differenziali in una indeterminata y, derivazioni ∂_t, ∂_x), è l'analogo non lineare corretto di Ann(u)? In particolare, sul banco Burgers u_t + uu_x = νu_xx e poi KdV u_t + 6uu_x + u_xxx = 0:
- (I) esiste un criterio "I(u) = componente generale di [F]" alla C3-T1 (unicità ⟺ test su u)?
- (S) la decomposizione di Ritt–Raudenbush in componenti prime corrisponde a "componente = fattore" (somma u = Σu_j)?
- (E) l'algebra differenziale dà E_int in forma chiusa o una stima?
Più: rapporto con il modulo canonico R·u (GATE3 §2), dimensione differenziale (polinomio di Kolchin ↔ funzione di Hilbert di R/Ann(u)), implicitizzazione differenziale (dati in forma chiusa, es. N-solitoni).

## 3. Caso di prova minimo e scala
1. Lineare come controllo (L2: calore, trasporto): I(u) ∩ {polinomi lineari} = Ann(u)·y; differenza tra I(u) = [P(∂)y] e Ann(u) = (P).
2. Burgers: (a) ideale [F_B] primo? (b) criterio per I(u) = [F_B]; (c) trasporto attraverso Cole–Hopf u = −2νφ_x/φ (contatto F4-LIN); (d) esempi: shock (φ = 1 + e^{θ}), u = x/t (φ = nucleo del calore).
3. KdV: 1-solitone (R7-L4), 2-solitone (campo ℂ(E₁,E₂)), equazioni stazionarie di Novikov (contatto F4-INT).

## 4. Criteri fissati PRIMA di cercare (non si modificano dopo)
- **PROMUOVI** se valgono tutte: (P1) almeno uno fra I/S/E ha sul banco Burgers–KdV un enunciato candidato con prova scritta che non sia la mera riformulazione di un teorema noto (novelty-check ≠ ABANDON); (P2) almeno due fra I/S/E hanno risposta "sì" o "parziale" con enunciato; (P3) il dizionario serve concretamente ad almeno due altre strade (F4-LIN/INT/LIFT/HOR), cioè traduce un loro enunciato in un enunciato su I(u).
- **PARCHEGGIA** se: il dizionario è coerente e dà (I) almeno parziale, ma (S) e (E) sono "no" con ostruzione (l'algebra differenziale funziona da linguaggio/hub e da test di identificabilità, non da strada di dimostrazione autonoma); oppure se il candidato principale risulta CON-FONTE (noto) e il contributo è solo di traduzione.
- **ELIMINA** se: (E1) anche (I) fallisce (nessun criterio per I(u) = componente generale, neppure per equazioni di evoluzione); oppure (E2) il dizionario si rompe sul modello di dato del progetto (I(u) non definito o non primo per la classe di dati rilevante e nessuna classe sostitutiva ragionevole); oppure (E3) tutto si riduce a teoremi noti senza delta e senza servizio alle altre strade.
- Costo: stimato in sessioni di Fase 4 (S = 1 sessione con audit, M = 2–3, L = >3).

## 5. Fonti / stringhe di ricerca previste
Ritt, *Differential Algebra* (1950); Kolchin, *Differential Algebra and Algebraic Groups* (1973) — basis theorem, componente generale, polinomio di dimensione; Kondratieva–Levin–Mikhalev–Pankratiev (1999); Boulier et al. Rosenfeld–Gröbner (1995/2009); Gao, implicitizzazione di parametrizzazioni differenziali razionali (2003); identificabilità differenziale-algebrica (Ljung–Glad 1994; Hong–Ovchinnikov–Pogudin–Yap; identificabilità di modelli PDE, Byrne et al.); Nullstellensatz differenziale effettivo (Golubitsky–Kondratieva–Ovchinnikov–Szanto; Ovchinnikov–Pogudin–Vo); equazioni stazionarie di Novikov / soluzioni finite-gap; Hölder (Γ differenzialmente trascendente); calcolo variazionale formale (Gel'fand–Dikii, Olver) per l'algebra dei polinomi differenziali di un'equazione di evoluzione; scoperta di PDE da dati (PDE-FIND). Stringhe: "differential ideal of a solution identifiability PDE", "differential algebra structural identifiability partial differential equations", "implicitization differential rational parametric", "Kolchin dimension polynomial general component", "Novikov equation N-soliton stationary KdV", "Hölder gamma differentially transcendental".

## 6. Comunicazione (hub)
- Appena pronto lo schema del dizionario: TABELLA a inbox/F4-LIN.md, F4-INT.md, F4-LIFT.md, F4-HOR.md (con una domanda mirata a ciascuno).
- Leggere inbox/F4-ALG.md: inizio (fatto: vuota), metà (dopo le verifiche SymPy), prima di consegnare; rispondere a ogni DOMANDA.
- central: PLAN-READY F4-ALG; TABELLA righe ROUTES; eventuali NEW-ROUTE; DONE F4-ALG.

## 7. Criterio di "fatto"
PLAN.md, NOTE.md (lavoro di dettaglio + ricerca registrata), VERDETTO.md (1 pagina: I/S/E, enunciati candidati, ostruzioni, costo, novità, raccomandazione secondo §4), sources.bib (stato di verifica per voce), open_questions.md, sympy/*.py + .out, TABELLA alle 4 inbox, righe ROUTES + DONE in central. Stati: solo "candidato" / "prova scritta" / "V-ex" / "CON-FONTE (da verificare)". Nessun DIMOSTRATO.
