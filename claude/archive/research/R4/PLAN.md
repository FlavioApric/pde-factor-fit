# PLAN — R4 · Identificazione dell'operatore / problemi inversi (C3, P4)

Data: 22/10/2026 · Agente: R4 · Cartella: `research/R4/`

## 1. Domande (dal piano §1.3, C3/P4, ladder §1.5; + aggiunte motivate)
- **C3.1** Mappa della letteratura su "operatori dal nucleo" (u ↦ Ann(u)): Prony/Hankel, annihilating filter/FRI, Wronskiano/Gram del jet, eliminazione differenziale (Ritt, Rosenfeld–Gröbner, Boulier), guessing D-finito (Kauers, ore_algebra, gfun), Ehrenpreis–Palamodov (varietà dal supporto della misura), identificabilità di PDE da una soluzione, inverso Sturm–Liouville (Borg, Gel'fand–Levitan, Marchenko, Freiling–Yurko).
- **C3.2** Teorema di identificabilità: quando UNA soluzione determina L (a meno di scala / a meno di cosa). Testare la congettura G4 (NOTAZIONE) ai livelli L0, L2, L3 del ladder; individuare il controesempio/limite a L1, L4.
- **C3.3** Verdetto: approccio a componenti vs ideale annullatore vs simbolo.
- **P4.1** Sintesi spettrale Â = Σ λ e⊗e^†: esistenza/unicità.
- **P4.2** Via risolvente/funzione di Green come "Â⁻¹".
- **P4.3** Legame P4 ↔ C3.2.
- **Aggiunte (motivate):**
  - A-R4.1 Identificabilità *su dizionario fisso* (Gram del jet 𝔾(u)): dim ker 𝔾 = 1 ⟺ ?  — è la versione usata dall'algoritmo (H4), distinta dall'ideale Ann(u). Serve a R1 (sparsità).
  - A-R4.2 Ruolo dei coefficienti variabili: Ann(u) nell'algebra di Weyl è un ideale sinistro *mai principale* "in modo canonico" → non unicità strutturale (ogni Q·L annulla u; operatori di ordine 1 con coeff. razionali u'/u). Quantificare.
  - A-R4.3 Identificabilità "per termine" (le componenti λ_k T_k) vs identificabilità dell'operatore intero.

## 2. Skill (Regola 2) — ordine e uso
1. `academic-research-skills\deep-research\SKILL.md` (Read; la versione `anthropic-skills:deep-research` richiede di lanciare sotto-agenti, non consentito a me senza richiesta utente → uso il workflow Markdown e ricerca diretta). Per: struttura domanda→fonti→sintesi.
2. `Auto-claude-code-research-in-sleep\skills\research-lit\SKILL.md`, `…\arxiv\SKILL.md`, `…\openalex\SKILL.md` (Read; solo istruzioni, nessuno script vendor eseguito) → interrogazioni manuali via WebSearch/WebFetch su arXiv/OpenAlex.
3. `math-skill\SKILL.md` modalità proof → dimostrazioni di [R4-T#] (L0, L2, L3).
4. `scientific-agent-skills\skills\sympy\SKILL.md` → script in `research/R4/sympy/` (Prony/Hankel su esponenziale-polinomio; Gram del jet; controesempi), eseguiti con `.venv\Scripts\python.exe -I`.
5. `…\novelty-check\SKILL.md` → cosa di C3.2 è già noto.
6. `scientific-agent-skills\skills\scientific-critical-thinking\SKILL.md` → revisione critica di G4 e del verdetto C3.3.

## 3. Fonti / stringhe di ricerca
- Prony / FRI: Vetterli–Marziliano–Blu 2002 (IEEE TSP); Dragotti–Vetterli–Blu 2007 (Strang–Fix); Hua–Sarkar matrix pencil; Peter–Plonka (generalized Prony, 2013); Plonka–Tasche; Stampfer–Plonka.
- Differential elimination: Ritt 1950; Kolchin 1973; Boulier–Lazard–Ollivier–Petitot 1995/2009 (Rosenfeld–Gröbner); Ljung–Glad 1994 (identifiability via differential algebra); Ollivier.
- Guessing: Kauers "Guessing handbook"/ "The holonomic toolkit"; Kauers–Jaroschek–Johansson (ore_algebra); Salvy–Zimmermann (gfun); Beckermann–Labahn (Hermite–Padé).
- Identifiabilità PDE: Xu? "identifiability of linear PDEs from a single solution" (arXiv, ~2023–2024: Scholl, Bacho, Kutyniok et al.); He–Ha–Huang (identifiability of PDE models); Kalman/observability.
- Ehrenpreis–Palamodov: Hörmander vol. II cap. 7; Björk; Cid-Ruiz–Homs–Sturmfels (Primary ideals and their differential equations, 2021); Ait El Manssour–Härkönen–Sturmfels (Linear PDE with constant coefficients 2021).
- Inverso SL: Borg 1946; Gel'fand–Levitan 1951; Marchenko; Levinson; Freiling–Yurko 2001; Hochstadt–Lieberman 1978.
- Wronskiano: annullatore L(y) = W(y_1..y_n,y)/W(y_1..y_n) (Ince; van der Put–Singer).
- Stringhe: "identifiability linear PDE single solution", "annihilating filter finite rate of innovation", "guessing holonomic", "Rosenfeld-Groebner identifiability", "inverse Sturm-Liouville uniqueness Borg".

## 4. Comunicazione
- R2↔R3↔R4: invio a R2 e R3 tabella "classe di funzioni → operatore minimo ricostruibile / condizione di identificabilità"; leggo le loro tabelle operatore→classe.
- R1↔R4: invio a R1 condizioni di identificabilità (unicità del vettore λ ⟺ dim ker 𝔾 = 1; cosa garantisce la sparsità).
- NEW-ROUTE a central se emergono strade (es. "identificazione via ideale annullatore/Gröbner invece che per componenti").
- Inbox R4 controllata: inizio, metà, prima di consegnare.

## 5. Criterio di "fatto"
- REPORT.md con: mappa letteratura C3.1; teoremi C3.2 enunciati con ipotesi esatte, fonte o dimostrazione, stato; verifica SymPy di almeno Prony/Hankel (L0), identificabilità per evoluzione (L2), controesempi per L1/L4; verdetto C3.3; P4.1–P4.3.
- sources.bib, open_questions.md; messaggi a R1/R2/R3; `DONE R4` in central.
