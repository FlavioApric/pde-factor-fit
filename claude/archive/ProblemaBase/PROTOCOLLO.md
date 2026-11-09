# Protocollo del gruppo di ricerca (session-protocol, Fase 1)

Coordinatore: la sessione centrale. È l'unica che modifica `BOARD.md`, `PROBLEM.md`, `NOTAZIONE.md` (glossario) e `ROUTES.md` (gli altri propongono via inbox).
Fonte di verità del problema: `D:\piano di ricerca.md` (il piano). Notazione: `D:\ProblemaBase\NOTAZIONE.md`.

## Regola 1 — Pianificare PRIMA di agire
Prima di qualsiasi ricerca, calcolo o scrittura di risultati, ogni agente scrive `research/<ID>/PLAN.md` con:
1. domande a cui deve rispondere (copiate dal piano + eventuali aggiunte motivate);
2. skill che userà, in che ordine e per cosa (vedi Regola 2);
3. fonti/stringhe di ricerca previste;
4. con quali agenti deve scambiare cosa (vedi grafo di comunicazione);
5. criterio di "fatto".
Poi scrive in `inbox/central.md` una riga `PLAN-READY <ID>` e prosegue.

## Regola 2 — Caricare le skill
"Caricare una skill" = invocarla con lo strumento Skill se è disponibile nella tua lista, ALTRIMENTI leggere integralmente il suo `SKILL.md` (dal percorso sotto) con Read e seguirne il workflow. Nel PLAN.md e nel REPORT.md dichiara esplicitamente quali skill hai caricato e come. Gli script contenuti nei repository `_vendor` NON vanno eseguiti (sono codice di terze parti non ancora approvato): usa solo le istruzioni Markdown. La skill `anthropic-skills:deep-research` è installata e invocabile con Skill.
Registro skill (radice `D:\ProblemaBase\_vendor\`):
- Ricerca: `academic-research-skills\deep-research\SKILL.md` · `Auto-claude-code-research-in-sleep\skills\research-lit\SKILL.md` · `…\skills\openalex\SKILL.md` · `…\skills\arxiv\SKILL.md` · `…\skills\semantic-scholar\SKILL.md` · `scientific-agent-skills\skills\paper-lookup\SKILL.md` · `scientific-agent-skills\skills\literature-review\SKILL.md` · `scientific-agent-skills\skills\citation-management\SKILL.md`
- Matematica: `math-skill\SKILL.md` (modalità `proof`/`solver`) · `scientific-agent-skills\skills\sympy\SKILL.md` · `Auto-claude-code-research-in-sleep\skills\formula-derivation\SKILL.md` · `…\skills\proof-writer\SKILL.md` · `…\skills\proof-checker\SKILL.md` (revisore = subagente Claude indipendente, NIENTE Codex) · `…\skills\kill-argument\SKILL.md` · `…\skills\lean-formalize\SKILL.md` (solo Fase 5)
- Critica/idee: `scientific-agent-skills\skills\scientific-critical-thinking\SKILL.md` · `…\hypothesis-generation\SKILL.md` · `…\scientific-brainstorming\SKILL.md` · `Auto-claude-code-research-in-sleep\skills\novelty-check\SKILL.md` · `…\skills\idea-discovery\SKILL.md`
SymPy: `D:\ProblemaBase\.venv\Scripts\python.exe -I script.py` (sympy, numpy, scipy, mpmath installati).

## Regola 3 — Comunicare
- Messaggi asincroni: file `inbox/<ID-destinatario>.md`, solo append, formato
  `## [AAAA-MM-GG] DA <mittente> → <destinatario> · TIPO` con TIPO ∈ {TABELLA, DOMANDA, RISPOSTA, NEW-ROUTE, CONFLITTO, AVVISO}.
- Leggi la TUA inbox all'inizio, a metà lavoro e prima di consegnare; rispondi alle DOMANDE ricevute.
- Grafo di comunicazione (dal piano): R2↔R3↔R4 (tabelle operatore→classe di funzioni); R1↔R4 (sparsità ⇔ identificabilità); R5↔R2 (quando E_int=0); R6↔R7 (matrice, simbolo, geometria); R8 legge tutti e segnala sovrapposizioni; PR-C2a→PR-C2b (nuclei ODE → nuclei PDE separati); PR-C2b↔PR-C2e (attributi); PR-C2d→R1 (spazi); tutti i PR-C2 → R3; gli SCOUT → central (NEW-ROUTE).
- Nuovo approccio non previsto dal piano → `inbox/central.md` con tipo `NEW-ROUTE` (idea, punti degli appunti collegati, criterio di promozione/eliminazione).
- Scrivi risultati SOLO nella tua cartella `research/<ID>/` + messaggi in `inbox/`.

## Regola 4 — Consegne di Fase 1
`research/<ID>/PLAN.md`, `REPORT.md` (risultati mappati su item C/P/II, teoremi chiave enunciati con precisione e fonte esatta, stato: noto / aperto / probabilmente falso), `sources.bib`, `open_questions.md`. Ultima riga in `inbox/central.md`: `DONE <ID>`.

## Aggiunta Fase 2 (25/10/2026)
Skill di progetto in `D:\ProblemaBase\skills-local\`: `session-protocol` (questo protocollo in forma operativa, da caricare per primo), `kernel-catalog-entry`, `claim-lifecycle`, `formalize-claim` (solo Fase 5), `spec-sync` (coordinatore), `route-scout`. Registro claim: `claims/LEDGER.md`. Roster delle sessioni di Fase 3: `SESSIONS.md`. In Fase 3 le cartelle di lavoro sono `work/<ID>/`.
