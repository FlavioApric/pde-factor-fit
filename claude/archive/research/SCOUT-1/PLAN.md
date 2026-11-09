# PLAN — SCOUT-1 · Horizon scout (algebra / geometria / rappresentazioni / visioni categoriali)

Data: 2026-10-22 · Agente: SCOUT-1 · Fase 1 · Slot: RT-ω (§1.6 "Breadth safeguards", "Where the open slot applies")
Notazione: `NOTAZIONE.md` v1. Protocollo: `PROTOCOLLO.md` (Regole 1–4).

## 1. Domande
Compito unico: guardare FUORI da RT-1…RT-7 (fattorizzazione additiva, log-simbolo, BCH/Dyson, Ann(u)/Gram/Prony, tensore simbolo, compagna/matrice su anello, spazio di Ehrenpreis) e cercare formulazioni alternative di:
- **S1 "operatore dal nucleo"** (C3, P4, §1.2-fatto 1): oggetti diversi da Ann(u) come ideale / ker 𝔾(u). Candidati: D-modulo generato da u e sua olonomia/ciclicità; dualità di Riemann–Hilbert (soluzioni ↔ sistema locale ↔ monodromia); "Galois inverso" (dalla soluzione all'equazione minima, gruppo di Galois differenziale); quiver/rappresentazioni (dati di monodromia/Stokes come rappresentazione di quiver); Macaulay inverse systems (duale di Matlis); fibrati di jet / varietà di equazioni (Vinogradov).
- **S2 "scomposizione in componenti"** (A5, A8, A9, C2, C4): decomposizioni canoniche diverse dalla fattorizzazione: decomposizione di D-moduli in indecomponibili (Krull–Schmidt), filtrazioni (Jordan–Hölder, socle), decomposizione per pendenze/Newton polygon (Levelt–Turrittin, Hukuhara), decomposizione primaria con operatori di Noether (già in R2: solo puntatore), tropicalizzazione del simbolo, decomposizione isotipica sotto il gruppo di Galois differenziale, decomposizione sotto azione di un'algebra di Lie / Hopf (coprodotto).
- **S3 "E_int"** (A9, B1, B2/P1, C2/P3): interpretazioni strutturali: gruppo Ext¹ (estensioni non spezzate), coomologia / torsione Tor, obstruction class, termini misti del coprodotto (algebra di Hopf / combinatoria di Faà di Bruno, Connes–Kreimer), differenza fra coprodotto e somma (biprodotto in categoria additiva vs prodotto tensoriale), regioni "di transizione" tropicali (più monomi dominanti simultaneamente).
- **S4 (aggiunta)** "ENCODING+GROUPING ⇒ E_int→0" (D1): funtori che rendono additivo ciò che è moltiplicativo (logaritmo, Tannaka, gruppo di Grothendieck) — cerco una versione categoriale.
- **S5 (aggiunta)** Problemi di esistenza/convergenza che queste visioni rendono teoremi: es. irregolarità di Malgrange, esistenza di forme normali formali (Hukuhara–Turrittin), sommabilità multi-summability (convergenza delle componenti formali).

Per ogni strada: idea (1 paragrafo), punti appunti collegati (A1…H3), costo, criterio di promozione/eliminazione fissato in anticipo, verdetto (1 pagina) con scientific-critical-thinking.

## 2. Skill (Regola 2), ordine e uso
1. `academic-research-skills\deep-research\SKILL.md` — Read; workflow domanda→fonti→sintesi. (La variante `anthropic-skills:deep-research` coordina sotto-agenti: non lancio sotto-agenti senza richiesta dell'utente, quindi uso il workflow Markdown con ricerca diretta WebSearch.)
2. `scientific-agent-skills\skills\scientific-brainstorming\SKILL.md` e `Auto-claude-code-research-in-sleep\skills\idea-discovery\SKILL.md` — Read; generazione indipendente delle strade PRIMA della ricerca bibliografica (per non farsi ancorare dai semi).
3. `Auto-claude-code-research-in-sleep\skills\research-lit\SKILL.md` + `…\arxiv\SKILL.md` — Read; stringhe di ricerca manuali (WebSearch), nessuno script vendor.
4. `Auto-claude-code-research-in-sleep\skills\novelty-check\SKILL.md` — Read; per ogni strada: è già coperta da RT-1…7 o da R2/R4/R6/R7? è nota in letteratura come metodo di identificazione?
5. `scientific-agent-skills\skills\scientific-critical-thinking\SKILL.md` — Read; verdetto per strada (punti deboli, ipotesi nascoste, kill-argument).

## 3. Fonti / stringhe di ricerca previste
- Riemann–Hilbert / D-moduli olonomi: Kashiwara, Mebkhout; Malgrange "Équations différentielles à coefficients polynomiaux"; Sabbah; Deligne "Équations différentielles à points singuliers réguliers".
- Galois differenziale: van der Put–Singer; Kovacic; "minimal annihilator" / "inverse problem differential Galois"; Compoint–Singer (decomposizione di operatori), van Hoeij "factorization of differential operators" e "eigenring" (Singer 1996 "Testing reducibility", eigenring End(D/DL)).
- Stokes/quiver: Boalch "quivers and Stokes data"; Malgrange–Sibuya; Levelt–Turrittin; Ramis multisummability.
- Inverse systems: Macaulay, Oberst "Multidimensional constant linear systems" (dualità modulo↔comportamento, Willems behaviors), Pommaret.
- Jet / varietà differenziali: Vinogradov–Krasil'shchik "Symmetries and conservation laws", Kruglikov–Lychagin.
- Hopf: Connes–Kreimer; Faà di Bruno Hopf algebra; Munthe-Kaas (Lie–Butcher), Ebrahimi-Fard "Magnus expansion pre-Lie".
- Tropicale: Grigoriev "Tropical differential equations"; Aroca–Garay–Toghani "fundamental theorem of tropical differential algebraic geometry".
- Categoriale: Willems behaviours come categoria abeliana; Malgrange-Oberst duality; Tannaka per sistemi lineari.

## 4. Comunicazione
- Ogni strada → `inbox/central.md` (NEW-ROUTE). AVVISO a R2 (nuclei/D-moduli/Galois), R4 (identificazione), R6 (matrici su anelli, eigenring), R7 (geometria/Lie/tropicale) quando la strada li tocca.
- Leggo `inbox/SCOUT-1.md` all'inizio (vuota), a metà e prima della consegna.

## 5. Criterio di "fatto"
PLAN.md, REPORT.md (1 verdetto/strada, mappato su C/P/II, teoremi chiave con fonte, stato noto/aperto/probabilmente falso), sources.bib, open_questions.md; ≥5 strade NEW-ROUTE con criteri fissati in anticipo; `DONE SCOUT-1` in central.
