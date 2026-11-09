# PLAN — SCOUT-2 (horizon scout: analisi / fisica matematica / segnali / controllo) — Fase 1
Data: 2026-10-22. Fonti lette prima di pianificare: `D:\piano di ricerca.md` (§0B, §1.2, §1.4, §1.6 "Breadth safeguards" e "Where the open slot applies"), `NOTAZIONE.md`, `PROTOCOLLO.md`, `ROUTES.md` (RT-1…RT-7, RT-ω).

## 1. Domande
Mandato (§1.6, Fase 1 v4): cercare SOLO fuori dalle strade seminate RT-1…RT-7 formulazioni alternative di
(Q1) "operatore dal nucleo" (u ↦ L con u ∈ ker L; C3, P4, D2);
(Q2) "scomposizione di u in componenti per termine" (A5, A8, A9, C4, F6);
(Q3) "termine d'interazione E_int" (A9, B2, P1, P3), e il fallback D1 "encoding+grouping ⇒ E_int→0".
Campi da scandire (dal mandato): identificazione di sistemi (subspace identification, realizzazione di Ho–Kalman, osservabilità ⇔ identificabilità); separazione cieca delle sorgenti (BSS analitica); tempo-frequenza e trasformate adattate (Wigner, wavelet, trasformate "di operatore"); scattering; matrici di trasferimento; momenti/Prony multidimensionale; Koopman; omogeneizzazione; rinormalizzazione.
Domande aggiuntive motivate:
- (Q4) Esiste una formulazione in cui il problema "u ∈ ker L, L=ΣT_k" è un problema di REALIZZAZIONE (sistema 2D/Roesser, behaviours di Willems) — dove identificabilità e scomposizione sono già teoremi?
- (Q5) Esiste un quadro in cui E_int ha già un nome e un teorema (ANOVA/Hoeffding, cumulanti, multiple-scale/RG secular terms, scattering multiplo/Born series)?
- (Q6) Per ogni strada: è analitica (vincolo k3), è già coperta da RT-1…RT-7 o da R1–R8 (allora AVVISO, non NEW-ROUTE)?

## 2. Skill (Regola 2) — ordine e uso
1. `anthropic-skills:deep-research` è invocabile ma coordina subagenti; per non duplicare lavoro e costo uso il suo equivalente in Markdown `_vendor\academic-research-skills\deep-research\SKILL.md` (letto con Read) come workflow (domanda → fonti → sintesi → verifica). Dichiarato anche in REPORT.
2. `_vendor\Auto-claude-code-research-in-sleep\skills\idea-discovery\SKILL.md` e `_vendor\scientific-agent-skills\skills\scientific-brainstorming\SKILL.md`: generazione/filtro delle strade candidate per campo.
3. `…\skills\research-lit\SKILL.md`, `…\skills\arxiv\SKILL.md`, `…\skills\semantic-scholar\SKILL.md` (solo istruzioni, nessuno script): ricerca letteratura via WebSearch/WebFetch.
4. `…\skills\novelty-check\SKILL.md`: per ogni strada, controllare che non sia già una RT seminata né un tema assegnato a R1–R8.
5. `_vendor\scientific-agent-skills\skills\scientific-critical-thinking\SKILL.md`: verdetto (punti deboli, ipotesi non verificabili, criterio di kill).
Nessuno script `_vendor` eseguito. Eventuali controlli SymPy (solo come controllo, k3) in `research/SCOUT-2/sympy/` con `.venv\Scripts\python.exe -I`.

## 3. Stringhe di ricerca previste
"2D Roesser realization Ho-Kalman PDE", "behavioral systems theory PDE Willems Pillai Shankar autonomous behaviour identification", "subspace identification from a single trajectory persistency of excitation fundamental lemma", "identifiability linear PDE single solution", "multidimensional Prony / ESPRIT / MUSIC exponential sums identifiability", "Hankel tensor 2D harmonic retrieval uniqueness", "blind source separation deterministic / sparse component analysis / morphological component analysis", "empirical mode decomposition synchrosqueezing", "Wigner–Ville cross terms interference", "Koopman generator identification eigenfunction", "inverse scattering Born series multiple scattering interaction", "transfer matrix product scattering matrix composition Redheffer star product", "homogenization correctors interaction", "renormalization group multiple scales Chen–Goldenfeld–Oono", "Hoeffding/ANOVA decomposition interaction term", "Mori-Zwanzig projection memory term".

## 4. Comunicazione
- `inbox/central.md`: PLAN-READY, una NEW-ROUTE per strada (idea, punti A1…H3, costo, criterio fissato in anticipo), DONE.
- AVVISO a R1 (Hilbert/regolarizzazione), R4 (identificazione), R5 (E_int) quando una strada li tocca direttamente.
- Inbox `inbox/SCOUT-2.md` letta: inizio (vuota), metà, prima della consegna.

## 5. Criterio di "fatto"
PLAN.md; REPORT.md con un verdetto ≤1 pagina per strada (idea, teorema-ancora con fonte, relazione con RT/R#, costo, promozione/kill, giudizio); sources.bib; open_questions.md; NEW-ROUTE in central; AVVISI inviati; `DONE SCOUT-2`.
