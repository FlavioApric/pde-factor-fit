# R7 — PLAN (Fase 1) · Geometria, simmetria, spettro, non linearità

Agente: R7 · Item: II (II.4, II.3, F6, G6), Fase 4 (L5, G3–G4, A6 "V·d/dx V") · Data: 2026-10-22
Notazione: `NOTAZIONE.md` (v1). Congettura di riferimento: **G7** (+ legami con G3, G5, G6).

## 1. Domande
Copiate dal piano (§1.3 II, §1.5 L5, Phase 4, tabella R7):
- Q1 (II.4) Quali sono i gruppi di simmetria di Lie delle PDE lineari campione (trasporto, calore, Airy, onda) e come le loro algebre di Lie producono (a) le funzioni speciali (Vilenkin–Miller), (b) le soluzioni invarianti/separate, cioè le "classi di funzioni" e_{n,i} di A5/A6?
- Q2 (II.4, G6 "ruotare") Gruppi di rotazione e rappresentazioni → funzioni speciali: SO(2), SO(3), E(2), gruppo di Heisenberg/Schrödinger; Bessel, Hermite, Legendre come coefficienti matriciali / basi di autovettori di operatori di Casimir o di sottoalgebre.
- Q3 (F1/F2, II.3) Teorema spettrale e calcolo funzionale: enunciato esatto (Reed–Simon) per operatori autoaggiunti e normali; quando â = Σ f(λ_a) v_a⊗v_a è legittimo; spettro continuo (frame continuo, legame con G6).
- Q4 (F6 "rompere il sistema per direzioni") Diagonalizzazione simultanea / spettro congiunto: teoremi (matrici: commutanti diagonalizzabili; operatori: autoaggiunti fortemente commutanti → misura spettrale congiunta). Controesempi (Nelson: commutano sul dominio comune ma non fortemente).
- Q5 (II.4, G5/G6) Varietà caratteristica V(P): ruolo geometrico (Ehrenpreis), invarianza sotto simmetrie (azione del gruppo sul simbolo), legame con lo spettro congiunto di (∂_t, ∂_x).
- Q6 (G7, A6, L5, Phase 4) Survey breve dei metodi non lineari: Koopman (Mezić), Carleman (convergenza/troncamento, Kowalski–Steeb), Cole–Hopf (Burgers ↔ calore = V·V_x di A6), Lax pairs/IST (KdV, NLS), Hirota e 2-solitone (sfasamenti = "E_int non lineare"), Miura/Bäcklund, identificazione lineare nei parametri (dizionario con u u_x).
- Q7 (aggiunta motivata) Le simmetrie (gruppo di Lie dell'equazione) agiscono sul problema inverso: se g è simmetria di L, allora u e g·u identificano lo stesso L ⇒ invarianza della Gram 𝔾; utile per C3/G4 e per R6 (invarianti).
- Q8 (aggiunta motivata, per R5) Strutture di algebra di Lie rilevanti per E_int: algebra generata dai termini T_k (nilpotente/risolubile ⇒ Zassenhaus/BCH finita), esempi (Heisenberg: [∂_x, x]=1; sl(2): {∂², x², x∂+1/2}).

## 2. Skill (Regola 2) — ordine e uso
1. `anthropic-skills:deep-research` — invocata con Skill per il workflow di ricerca (piano → fonti → sintesi). Se richiede subagenti, eseguo la ricerca direttamente (un solo agente) seguendone il workflow.
2. `academic-research-skills\deep-research\SKILL.md`, `research-lit`, `arxiv`, `paper-lookup` — lette (Read) per le stringhe di ricerca/verifica fonti. Nessuno script `_vendor` eseguito.
3. `math-skill\SKILL.md` (modalità proof) — per enunciati con ipotesi esatte e mini-dimostrazioni (lemmi R7).
4. `scientific-agent-skills\skills\sympy\SKILL.md` — verifiche simboliche: Cole–Hopf, 2-solitone KdV (Hirota) e sfasamento, simmetrie del calore (prolungamento), Miura, linearità nei parametri. Script in `research/R7/sympy/`, eseguiti con `.venv\Scripts\python.exe -I`.
5. `scientific-brainstorming` — strade di Fase 4 (NEW-ROUTE).
6. `scientific-critical-thinking` — stato noto/aperto/probabilmente falso di G7 e delle affermazioni del piano.

## 3. Fonti / stringhe
Olver, *Applications of Lie Groups to Differential Equations* (GTM 107, 2a ed. 1993): Ch.2 (prolungamento, Thm 2.31/2.36), Ex. 2.41 (calore), Ch.3 (soluzioni invarianti), Ch.5 (simmetrie generalizzate/KdV).
Vilenkin, *Special Functions and the Theory of Group Representations* (AMS 1968); Vilenkin–Klimyk; Miller, *Lie Theory and Special Functions* (1968), *Symmetry and Separation of Variables* (1977).
Reed–Simon I (Thm VII.2, VIII.5, VIII.6), Schmüdgen *Unbounded Self-adjoint Operators* (Ch.5, strongly commuting; Nelson's example).
Koopman 1931; Mezić 2005 (Nonlinear Dyn.), Budišić–Mohr–Mezić 2012; Kowalski–Steeb 1991; Forets–Pouly 2017; Amini–Sun–Motee 2021 (convergenza Carleman); Hopf 1950, Cole 1951; Lax 1968; Gardner–Greene–Kruskal–Miura 1967; Zakharov–Shabat 1972; Ablowitz–Segur 1981; Ablowitz–Clarkson 1991; Hirota 1971/2004; Miura 1968; Rogers–Schief (Bäcklund); Rudy et al. 2017 (PDE-FIND).
Stringhe: "Carleman linearization convergence error bound", "Koopman operator spectrum Burgers Cole-Hopf", "Koopman KdV", "joint spectral measure strongly commuting", "heat equation symmetry group Appell Hermite".

## 4. Scambi
- R6 ↔ R7: rispondo su simmetrie/rotazioni/simbolo; ricevo la tabella invarianti (companion vs tensore) → integrazione in REPORT §II.4.
- R7 → R5: strutture di algebra di Lie per E_int (Q8), sfasamenti dei solitoni come E_int non lineare.
- R7 → central: `PLAN-READY R7`, NEW-ROUTE per strade di Fase 4, `DONE R7`.
- Controllo `inbox/R7.md`: inizio, metà, prima della consegna.

## 5. Criterio di "fatto"
REPORT.md con: teoremi enunciati con ipotesi esatte + fonte (cap./teorema), stato (noto / aperto / probabilmente falso), mappa su II.3/II.4/F6/G6/L5/G7; verifiche SymPy eseguite e citate (Cole–Hopf, 2-solitone KdV, simmetrie calore); sources.bib; open_questions.md; messaggi a R6/R5/central inviati; `DONE R7`.
