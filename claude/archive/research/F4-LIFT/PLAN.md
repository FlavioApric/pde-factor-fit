# F4-LIFT — PLAN di scouting (Fase 4, sprint di scouting) · 26/10/2026

Strade del piano Fase 4: **(i)** sollevamenti lineari (Carleman: immersione polinomiale in ℓ²/spazio di Fock; Koopman: operatore di composizione e suo spettro) e **(iii)** uno spazio di Hilbert costruito per assorbire la non linearità.
Stato: scouting preparatorio e reversibile (FASE4_SCOUTING.md). Nessun claim DIMOSTRATO; ogni enunciato nuovo è "candidato", "prova scritta" o "V-ex".

## 0. Letture fatte (Passo 0 di session-protocol)
FASE4_SCOUTING.md, RIPRESA.md (ultimo AGGIORNAMENTO 26/10, avvio sprint Fase 4), PROTOCOLLO.md, NOTAZIONE.md (v1+v2), PROBLEM.md (G★′), GATE3.md, claims/LEDGER.md, ROUTES.md, inbox/F4-LIFT.md (vuota all'inizio), inbox/F4-ALG.md (vuota).
Input: research/R1/REPORT.md (R1-T1 Aronszajn, R1-P9 encoder lineari, R1-P10 DMD = Prony, R1-P11 Fock/Mehler), work/C1C2/PROOF_PACKAGE.md §8 (C12-D2, C12-T5 funtore C1.0, C12-T6 Appell/Fock F_{a,ρ}), work/P1 (classe 𝔅, P1-T2, P1-P1(e), P1-T4/T5), work/P3 (P3-T1 Dyson–Phillips), research/R7 (R7-T13 Koopman, R7-T14 Carleman, R7-P6 Cole–Hopf softmax, R7-L4 simmetria).

## 1. Skill caricate (Regola 2) e ordine d'uso
1. `skills-local/session-protocol` (per prima), `skills-local/route-scout` (workflow), `skills-local/claim-lifecycle` (stati) — lette per intero.
2. `_vendor/Auto-claude-code-research-in-sleep/skills/research-lit/SKILL.md` — letto (workflow Step 0–4; fonti: solo `web`, nessuna libreria locale/Zotero; lo script `verify_papers.py` NON viene eseguito: la verifica anti-allucinazione si fa a mano con WebSearch/WebFetch su arXiv/DOI, e ciò che non si riesce a verificare è marcato `[UNVERIFIED]` / "da verificare").
3. `_vendor/Auto-claude-code-research-in-sleep/skills/novelty-check/SKILL.md` — letto (fasi A–D, "NOVELTY VERDICT LIMITS"); il revisore esterno Codex è escluso (decisione dell'utente): valuto io, dichiarando i limiti.
4. `_vendor/math-skill/SKILL.md` — letto (modo `proof`: esplorazione separata dalla prova, controesempi presto; i suoi script NON vengono eseguiti).
5. `_vendor/scientific-agent-skills/skills/sympy/SKILL.md` — letto (aritmetica esatta, simboli con ipotesi). SymPy solo come verifica: `D:\ProblemaBase\.venv\Scripts\python.exe -I research/F4-LIFT/sympy/<script>.py`.

## 2. Domande (dalla consegna e da FASE4_SCOUTING §3)
- **D1 (decisiva, condivisa con F4-ALG):** il troncamento di Carleman all'ordine N conserva la struttura di annullatore (ideale) e di fattori di Fase 3? In che senso preciso l'ideale "si chiude" sotto troncamento?
- **D2 (E):** come si confronta l'E_int del sistema sollevato (lineare, infinito-dimensionale, due termini: parte lineare dΓ(A) e accoppiamento B) con l'E_int non lineare (u − flusso lineare; serie di Volterra)? Raggio/costo.
- **D3 (I):** identificazione dell'operatore da una soluzione: (a) via annullatore del sollevato (analogo di C3-T1); (b) via spettro di Koopman / DMD (analogo di R1-P10).
- **D4 (S):** scomposizione in componenti: i blocchi diagonali del sollevato (ordini di Volterra / autospazi di Koopman) sono l'analogo di "componente = fattore"? Quando il sollevato si diagonalizza a blocchi (forma normale) e che cosa gioca il ruolo di δ(P) (intersezioni delle varietà)?
- **D5 (iii, C1.0):** il funtore C1.0 (fattore Q ↦ RKHS ker_{H^m}Q, somma ↦ somma di Aronszajn) si estende a un funtore che assorbe i prodotti (nuclei prodotto, Fock)? Esiste uno spazio in cui la non linearità è limitata ed E_int continua (contro P1-P1(e))?
Banco di prova: **Burgers** u_t + u u_x = ν u_xx (Cole–Hopf disponibile), poi **u_t = u_xx + u²** (non integrabile, esplosione di Fujita). Caso giocattolo: ODE x′ = λx + βx².

## 3. Criteri fissati PRIMA di cercare (kill criteria)
**Strada (i) Carleman/Koopman.**
- PROMUOVI se: (P-i-1) almeno due fra I/S/E ricevono "sì" o "parziale con enunciato candidato" verificato V-ex su Burgers **e** (P-i-2) almeno uno di questi enunciati vale anche per u_t = u_xx + u² (cioè non si riduce a Cole–Hopf, che è di F4-LIN) **e** (P-i-3) D1 ha una risposta precisa (sì/no con l'oggetto che si conserva).
- PARCHEGGIA se: il contenuto si riduce a riformulazioni note (troncamento = serie di Volterra / Taylor nel dato) senza trasportare un teorema di Fase 3 oltre il caso integrabile, oppure il costo è esponenziale in N senza un enunciato che lo compensi.
- ELIMINA se: il troncamento distrugge annullatore e fattori senza alcun invariante recuperabile (l'annullatore del sollevato troncato non ha relazione con l'ideale differenziale di u) **e** lo spettro di Koopman non dà identificazione nemmeno della parte lineare.
**Strada (iii) spazio di Hilbert che assorbe la non linearità.**
- PROMUOVI se esiste uno spazio (o una scala) in cui (a) la non linearità polinomiale è un operatore limitato (anche tra gradini di una scala), (b) il funtore C1.0 si estende funtorialmente contenendo il caso lineare, (c) E_int (non lineare o del sollevato) è continua, a differenza di H^m (P1-P1(e)).
- MERGE-INTO (i) se lo spazio serve solo da ambientazione funzionale del sollevamento di Carleman senza (c).
- ELIMINA se l'assorbimento richiede ker Q chiuso per prodotti (vero solo per fattori degeneri) e nessuna versione a scala dà (c).
**Domanda condivisa con F4-ALG (chiusura dell'ideale sotto troncamento):** risposta accettabile solo se dice *quale* ideale (Veronese / valutazione, 𝔪^{N+1}, I_u ∩ modulo dei lineari-di-Carleman) è chiuso sotto la derivazione troncata, con verifica SymPy sul caso giocattolo e su Burgers.

## 4. Lavoro previsto (ordine)
1. NOTE §A — algebra del troncamento: osservabili polinomiali 𝒪, derivazione D (generatore di Koopman), ideale 𝔪 dell'equilibrio; troncamento = quoziente 𝒪/𝔪^{N+1}? difetto sulla varietà di Veronese. SymPy `s1_carleman_ode.py`.
2. NOTE §B — E: Dyson–Phillips sul sollevato (diagonale + nilpotente) vs Volterra; Lie algebra dei due termini troncati (risolubile?) → P1-T4. Burgers: raggio di convergenza della serie di Volterra via zeri complessi di Cole–Hopf. SymPy `s2_burgers_radius.py`, `s3_dyson_lift.py`.
3. NOTE §C — S: forma normale del sollevato (equazione di Sylvester a blocchi), funzioni di risonanza r_k = Σa(κ_i) − a(Σκ_i) come analogo di V(Q_i)∩V(Q_j); Burgers (Cole–Hopf = forma normale) vs u² (risonanze al 3° ordine). SymPy `s4_normal_form.py`.
4. NOTE §D — I: modulo degli annullatori "lineari di Carleman" Ann_N(u) ⊂ R^N; test su onda viaggiante e 2 fronti di Burgers (R7-L4). Koopman: invarianza dello spettro per coniugio ⇒ cosa identifica. SymPy `s5_lift_ann.py`.
5. NOTE §E — (iii): nuclei prodotto (Aronszajn §8), Fock Γ(ℋ_Q), chiusura di ker P per prodotti; classe 𝔅 come algebra (scala di Ovsyannikov).
6. Letteratura (research-lit, solo web) + novelty-check sugli enunciati candidati; `sources.bib` con stato di verifica.
7. VERDETTO.md, open_questions.md, TABELLA righe ROUTES in inbox/central.md, DONE F4-LIFT.

## 5. Fonti / stringhe di ricerca previste
"Carleman linearization error bound" (Forets–Pouly 2017; Liu et al. PNAS 2021; Amini–Sun–Motee), "Carleman linearization reaction-diffusion quantum" (An et al.), "Carleman embedding Kowalski Steeb", "Koopman analysis Burgers equation" (Page–Kerswell 2018), "Koopman spectrum conjugacy invariance" (Budišić–Mohr–Mezić 2012; Mezić 2020), "Koopman principal eigenfunctions" (Mauroy–Mezić), "Cole–Hopf normal form" / "near-identity transformation Burgers Kodama", "C-integrable Calogero", Fujita 1966, Aronszajn 1950 Part I §8 (prodotto di nuclei), Ovsyannikov / Nirenberg–Nishida.

## 6. Contatti (grafo FASE4_SCOUTING §5)
- **F4-ALG (hub):** TABELLE via inbox/F4-ALG.md; domanda condivisa: chiusura dell'ideale sotto troncamento. Leggo inbox/F4-LIFT.md all'inizio, a metà, prima di consegnare.
- **F4-LIN:** AVVISO su Cole–Hopf = forma normale del sollevato di Carleman (raccordo, non duplicazione).
- central: PLAN-READY, TABELLA ROUTES, DONE.

## 7. Criterio di "fatto"
I cinque file in research/F4-LIFT/ (PLAN, VERDETTO ≤ 1 pagina, sources.bib, open_questions, NOTE) + sympy/ con output; risposte I/S/E per (i) e (iii) con enunciati candidati, ostruzioni, costo, novità; raccomandazione secondo §3; TABELLA in central; DONE F4-LIFT.
