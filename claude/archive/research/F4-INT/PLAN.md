# PLAN — F4-INT (Fase 4, sprint di scouting) · IST / Lax / Hirota
Agente F4-INT · 26/10/2026 · roster: FASE4_SCOUTING.md · strade: RT-R7a, RT-R7c (ROUTES.md) · item: C3/G4/G7, P1/B2, A8, Fase 4 (L5).
Scouting preparatorio e reversibile: nessuna strada promossa da me, nessun claim DIMOSTRATO. Stati ammessi per i miei enunciati: **candidato**, **prova scritta** (schizzo completo non auditato), **V-ex**, **CON-FONTE (da verificare)** se il numero di teorema non è controllato.

## 0. Skill (dichiarate; caricate leggendo i SKILL.md, nessuno script _vendor eseguito)
1. `skills-local/session-protocol` (per primo), `skills-local/route-scout` (nota → PLAN → ricerca/prova → verdetto 1 pagina → riga ROUTES), `skills-local/claim-lifecycle` (stati).
2. `_vendor/Auto-claude-code-research-in-sleep/skills/research-lit/SKILL.md` — ricerca web (WebSearch/WebFetch), abstract, sintesi; fonti solo verificate o marcate "da verificare".
3. `_vendor/Auto-claude-code-research-in-sleep/skills/novelty-check/SKILL.md` — fasi A (claim), B (ricerca multi-query), D (rapporto) con il blocco "NOVELTY VERDICT LIMITS"; fase C (revisore Codex) **non eseguita** (decisione utente: niente Codex) → limite del verdetto dichiarato.
4. `_vendor/math-skill/SKILL.md` modo `proof` — esplorazione separata dalla prova, controesempi prima.
5. `_vendor/scientific-agent-skills/skills/sympy/SKILL.md` — verifiche esatte in `research/F4-INT/sympy/` con `.venv\Scripts\python.exe -I`, solo come controllo (vincolo k3).

## 1. Domande (domanda guida comune I/S/E, poi specifiche)
- **(I) identificazione da UNA soluzione**, KdV e NLS. Lineare di riferimento: C3-T1 (Ann(u) = (P) ⟺ test EP), C3-T4 (L2: identifica ⟺ u ∉ EP; dati EP ⟺ interpolazione di Hermite con D ≥ n+1), C3-C2 (dati EP non identificano mai nell'anello intero), C3-P3 (ostruzione da simmetria lineare), P4-T2.
  - I.1 In quale classe d'ipotesi 𝓗 (dizionario di flussi) l'IST trasforma "u risolve u_t = K[u]" in un problema lineare sui dati di scattering? Enunciato candidato con conteggio esatto dell'ambiguità.
  - I.2 Analogo non lineare di "EP": quali soluzioni non identificano mai (multi-solitoni / riflessione nulla? soluzioni stazionarie di flussi superiori, equazioni di Novikov?).
  - I.3 Fuori da 𝓗 (dizionario generale di monomi del jet): a cosa si riduce l'ostruzione (simmetrie condizionali / ODE autonome soddisfatte da u per ogni t)?
  - I.4 Dominio limitato Ω (H0/H1): cosa serve per passare da u|_Ω ai dati di scattering (continuazione unica, analiticità)?
- **(S) scomposizione**: solitoni + radiazione come "componenti" (spettro discreto/continuo); additività solo nei dati di scattering; risoluzione in solitoni come analogo asintotico. Lineare: C12-T1′, P1-T2.
- **(E) E_int**: Hirota (coefficienti a coppie A_ij, sfasamenti additivi a coppie), forma chiusa e costo (determinante vs somma su 2^N) a confronto con P1-T3 / R5-T2; ∫E_int dx = 0 (oggi V-ex, DECLASSAMENTI A); continuità (P1-P1(e)): la mappa u ↦ dati di scattering è continua? dove no?
- **RT-R7c**: il 1-solitone non identifica — riconciliare con I.1/I.2 (versione non lineare di C3-P3).
- Termini dentro il flusso: l'IST separa i termini di KdV (u_xxx vs uu_x)? o solo i flussi commutanti della gerarchia?

## 2. Criteri fissati PRIMA di cercare
### RT-R7a (criterio ROUTES: "promuovi se l'identificazione da una soluzione è dimostrata per KdV/NLS")
Uno scouting non può produrre "dimostrata" (niente DIMOSTRATO senza S-CHECK). Traduzione operativa per la raccomandazione al Gate 4a:
- **PROMUOVI** (= proporre una sessione di dimostrazione di Fase 4) se entrambe:
  (P1) esiste un enunciato candidato di identificazione da una soluzione **sia per KdV sia per NLS**, con prova scritta che riduce tutto a fatti IST pubblicati (CON-FONTE, anche "da verificare") e con conteggio esatto dell'ambiguità, verificato in SymPy (V-ex) su almeno 1- e 2-solitone di KdV e 1-solitone + una soluzione a 2 autovalori di NLS;
  (P2) l'enunciato trasporta esplicitamente almeno uno di I/S/E di Fase 3 (es. C3-T4/C3-C2 ↔ multi-solitoni, P1-T3 ↔ Hirota) con un dizionario dichiarato.
- **PARCHEGGIA** se vale (P1) solo per una delle due equazioni, oppure se l'identificazione vale solo in una classe banale (es. solo il coefficiente di traslazione), oppure se tutto è già in letteratura senza trasporto di I/S/E.
- **ELIMINA** se (K1) l'identificazione da una soluzione è falsa per KdV in ogni classe 𝓗 non banale (controesempio), oppure (K2) l'IST richiede dati che il modello M1–M3 su Ω limitato non può dare e non c'è un argomento di continuazione unica, oppure (K3) un articolo pubblicato contiene già l'enunciato **e** il suo trasporto I/S/E (novelty: nominare l'articolo).
### RT-R7c (criterio ROUTES: "promuovi se il criterio 'u non invariante per sottoalgebre compatibili' si riconcilia con R4-T5")
- **MERGE** (in RT-R7a e/o F4-ALG; parte lineare già in RT-4 via C3-P3) se l'ostruzione da simmetria risulta un caso particolare del criterio di I.1 (insieme spettrale piccolo) o del criterio ideale-teorico di F4-ALG.
- **PROMUOVI autonoma** se dà un criterio di non identificabilità non coperto da I.1 né da F4-ALG (es. simmetrie condizionali con caratteristica nel dizionario che non sono flussi della gerarchia).
- **ELIMINA** se l'ostruzione è falsa (un 1-solitone identifica in una classe naturale che contiene la sua simmetria).
### Hirota (E)
- Utile per il Gate 4a se dà E_int in forma chiusa con costo polinomiale in N (non 2^N) e un enunciato su E_int (integrale, asintotica) dimostrabile; altrimenti nota di contesto.

## 3. Lavoro e fonti
1. Esplorazione/prova (math-skill proof): gerarchia di KdV, dispersione linearizzata ↔ evoluzione dei dati di scattering (GGKM 1967, Lax 1968, AKNS 1974, Ablowitz–Segur 1981, Deift–Trubowitz 1979, Novikov 1974, Lax 1975, Kay–Moses 1956, Hirota 1971/1973, Satsuma–Yajima 1974, Zakharov–Shabat 1972; continuazione unica Saut–Scheurer 1987; risoluzione in solitoni Eckhaus–Schuur 1983, Borghese–Jenkins–McLaughlin 2018).
2. SymPy (`sympy/int_checks.py`): flussi K_0, K_1, K_2 di KdV su N-solitoni esatti (razionali in E_i = e^{η_i}); stazionarietà di Novikov; dimensione dell'ambiguità in 𝓗_1, 𝓗_2; Kay–Moses det = Hirota; ∫E_int = 0; NLS 1-solitone e breather di Satsuma–Yajima; formula "Bernoulli/Ising" del τ.
3. Ricerca (research-lit + novelty-check): "identifiability PDE single solution KdV soliton", "uniqueness physical law learning nonlinear", "reflectionless stationary higher KdV Novikov", "generalized conditional symmetry KdV", "unique continuation KdV Saut Scheurer", "soliton resolution NLS", "tau function partition function Ising soliton".
## 4. Contatti
F4-ALG (hub): TABELLA di traduzione nel linguaggio dell'ideale differenziale I(u) (multi-solitone ↔ ideale con equazione di Novikov; simmetria condizionale ↔ elemento di I(u) di solo x). F4-LIN: Darboux/Bäcklund aggiunge un punto allo spettro Λ(u) (identificabilità +1); Miura ↔ coppie di Lax. Inbox letta all'inizio (vuota), a metà, prima di consegnare.
## 5. Fatto quando
PLAN, NOTE, sympy (output citato), sources.bib, open_questions, VERDETTO (1 pagina, I/S/E, raccomandazioni RT-R7a/R7c secondo §2), TABELLA righe ROUTES in central, risposte alle DOMANDE, `DONE F4-INT`.
