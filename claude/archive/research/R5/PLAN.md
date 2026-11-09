# PLAN — R5 · Termine d'interazione E_int (Fase 1, ricerca)

Data: 2026-10-22 · Agente: R5 · Item: P1 (P1.1–P1.4), P3 (P3.1–P3.4); contributi a C4.3 e a G3 (NOTAZIONE).
Cartella di lavoro: `D:\ProblemaBase\research\R5\` (+ script SymPy in `research/R5/sympy/`, solo controlli).

## 1. Domande (dal piano §1.3 P1/P3, §1.2-2(b)(c), §1.5 L2/L4; + aggiunte motivate)
P1 — struttura di E_int
- P1.1 Caso commutante: E_int = convoluzione/prodotto? Verificare G3: per `u_t=(A_1+A_2)u` a coeff. costanti `e^{tA}=e^{tA_1}e^{tA_2}`, E_int additivo `=(K_1−δ)*(K_2−δ)*u_0`; espansione additiva a 2^N termini vs O(N) nel log-simbolo.
- P1.2 Caso non commutante: BCH, Zassenhaus (formula, convergenza, raggio), Magnus (condizione ∫‖A‖<π), Trotter–Kato (prodotto, stime d'errore di splitting O(t²[A,B]) di Lie–Trotter e Strang), Duhamel; teorema di Wei–Norman (fattorizzazione esatta per algebre di Lie risolubili di dimensione finita).
- P1.3 La "matrice di funzioni E" (B2) come matrice di interazione/Gram: elementi di matrice ⟨e_m^†|L_2|e_n⟩.
- P1.4 Serve un modello locale (B3/B4)? Quando la serie è esatta/finita (algebra nilpotente/risolubile ⇒ forma chiusa esatta), quando no.
- Aggiunta P1.0 (motivata: NOTAZIONE chiede una definizione di E_int "per quadro"): definire E_int nei tre quadri additivo / moltiplicativo / log-simbolo e nel quadro "nucleo" (ker L vs ker L_1 + ker L_2, G1).
P3 — identificazione via perturbazioni/duali
- P3.1 Base duale (da C1.4; qui: autofunzioni biortogonali per operatori non autoaggiunti).
- P3.2 Termini di Dyson del 1° e 2° ordine nel quadro di interazione `U_I(t)=e^{−tL_1}e^{t(L_1+L_2)}`.
- P3.3 Convergenza (Kato): perturbazioni limitate (serie di Dyson converge in norma per ogni t), relativamente limitate (Miyadera–Voigt, Desch–Schappacher; serie di Kato–Rellich per famiglie olomorfe), regole sull'analiticità degli autovalori.
- P3.4 Regole di selezione: quando ⟨e_m^†|L_2|e_n⟩=0 (simmetrie, commutatori, gradi).
- Aggiunta Q-ker: quando ker(L_1+L_2) "si separa" — operatori commutanti, spettro congiunto, separazione delle variabili (Miller), R-separabilità; collegamento con G1/G2 (R2).

## 2. Skill (Regola 2) — ordine e uso
1. `anthropic-skills:deep-research` (strumento Skill) — workflow di ricerca/sintesi; eseguito direttamente da me (nessun sotto-agente: istruzione di non delegare).
2. `_vendor/Auto-claude-code-research-in-sleep/skills/research-lit/SKILL.md` e `_vendor/scientific-agent-skills/skills/paper-lookup/SKILL.md` (lettura con Read) — per strategia di ricerca e verifica bibliografica (via WebSearch/WebFetch dove disponibili; nessuno script _vendor eseguito).
3. `_vendor/Auto-claude-code-research-in-sleep/skills/formula-derivation/SKILL.md` + `_vendor/math-skill/SKILL.md` (modalità proof) — per le derivazioni brevi (E_int bilineare, Zassenhaus 2° ordine, Dyson 2° ordine, esempio heat+trasporto a coeff. variabile).
4. `_vendor/scientific-agent-skills/skills/sympy/SKILL.md` — controlli simbolici con `.venv\Scripts\python.exe -I`.
5. `_vendor/scientific-agent-skills/skills/scientific-critical-thinking/SKILL.md` — passata critica finale su G3 e su ogni enunciato "noto/aperto/probabilmente falso".

## 3. Fonti / stringhe di ricerca
Kato *Perturbation Theory for Linear Operators* (1995 repr.), Reed–Simon I–IV, Pazy *Semigroups* (1983), Engel–Nagel *One-Parameter Semigroups* (2000), Sakurai–Napolitano, Blanes–Casas–Oteo–Ros *The Magnus expansion and some of its applications* Phys. Rep. 470 (2009), Wei–Norman J. Math. Phys. 4 (1963), Miller *Symmetry and Separation of Variables* (1977), Trotter PAMS 1959, Chernoff JFA 1968, Hansen–Ostermann (stime splitting), Jahnke–Lubich BIT 2000, Casas–Murua (BCH convergenza), Suzuki (Zassenhaus/frattali), Kimura (Zassenhaus esplicito).
Stringhe: "Zassenhaus formula convergence domain", "BCH convergence radius log 2 / π", "Magnus expansion convergence ∫‖A‖<π", "Lie-Trotter splitting error commutator bound unbounded operators", "Wei-Norman solvable Lie algebra global", "Dyson series relatively bounded perturbation Miyadera", "separation of variables commuting symmetry operators Miller".

## 4. Comunicazione
- R5→R2 (DOMANDA): in quali casi E_int=0 (fattorizzazione/commutatività; ker(L_1+L_2) vs ker L_1+ker L_2). Integro la risposta in REPORT.
- R5→R6/R7 (AVVISO): strutture di algebre di Lie utili (algebra di Schrödinger/heat, oscillatore, sl(2) per x∂_x, ∂_x², x²; Wei–Norman).
- NEW-ROUTE → central se emergono strade nuove (es. "E_int nel quadro di interazione = elemento di gruppo, non somma").
- Inbox R5 letta: inizio (vuota), metà, prima della consegna.

## 5. Criterio di "fatto"
REPORT.md con: definizioni di E_int nei quadri; teoremi (BCH/Zassenhaus/Magnus/Trotter–Kato/Dyson/Wei–Norman/Kato/separazione) con ipotesi esatte e fonte; stato (noto/aperto/probabilmente falso) per G3, P1.1–P1.4, P3.1–P3.4; controlli SymPy citati (heat+trasporto, Zassenhaus 2° ordine, Dyson 1° ordine su esempio); sources.bib; open_questions.md; `DONE R5` in inbox/central.md.
