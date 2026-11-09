# PLAN — R2 · Nuclei di operatori differenziali e classi di funzioni
Data: 22/10/2026 · Item: C2, C4, P1 · Notazione: `NOTAZIONE.md` v1 · Protocollo: `PROTOCOLLO.md`

## 1. Domande (dal piano + aggiunte motivate)
- **Q1 = C4.2 / G2.** Per `P = P_1 P_2 ∈ R = ℂ[∂_t,∂_x]`: è vero `ker P = ker P_1 + ker P_2`? È una somma diretta? Quale intersezione? Enunciato esatto via successione esatta `0→R/(P_1P_2)→R/(P_1)⊕R/(P_2)→R/(P_1,P_2)→0` + iniettività (Malgrange / Ehrenpreis–Palamodov). In quali spazi (C^∞(Ω), D'(Ω), Ω convesso; S'? L²?) e con quali ipotesi (coprimalità; P_1,P_2 non coprimi?).
- **Q2 = G1 / C4.1.** Se `L = L_1 + L_2` (somma di termini): `ker L ∩ (ker L_1 + ker L_2)` = ? Verificare l'inclusione in `ker(L, L_1L_2)` (o qualcosa di più fine) e la dimensione finita (V(P_1)∩V(P_2) finita ⇒ dimensione finita?). Statuto di A8.
- **Q3 = C4.4.** Numerabilità: rappresentazione integrale di Ehrenpreis–Palamodov su V(P) (frame continuo) vs base numerabile (𝕋, serie di Fourier ristrette a V(P)∩(ℂ×iℤ)); casi ODE (dim. finita), PDE (dim. infinita; quando esiste base di Schauder/Riesz di esponenziali-polinomi?).
- **Q4 = C2.6 (ladder ᵈ: coeff. polinomiali, classi olonome) + C2.6 (serie 1: trasporto).** Funzioni D-finite/olonome: definizione, chiusura per somma/prodotto (con bound d'ordine), cosa dice ciò su ker(L) per L a coeff. polinomiali; trasporto come esempio di Ehrenpreis (V(P) retta ⇒ g(x−ct)).
- **Q5 = Coeff. variabili (C4.2 nel caso D-moduli).** Fattorizzazione L = L_1L_2 nell'anello di Ore/Weyl: ker L ⊇ ker L_2, L_2(ker L) ⊆ ker L_1; somma diretta ker L = ker L_1' ⊕ ker L_2 quando? (LCLM, Picard–Vessiot, decomposizione di moduli: D/DL ≅ D/DL_1 ⊕ D/DL_2 ⟺ ...). Galois differenziale: quando i "componenti" sono canonici.
- **Q6 = P1 (contributo R2).** Struttura algebrica di E_int nel quadro additivo per somma di termini: la proiezione su ker L_n è ben definita? Commento dal lato modulo (sizigie). Rispondere a R5 su "quando E_int = 0".
- **Q7 (aggiunta).** Noetherian operators (Cid-Ruiz–Sturmfels, primary decomposition) per P non ridotti (fattori ripetuti P = Q^m ⇒ polinomi·esponenziali), e EPGP (Härkönen–Lange-Hegermann–Raiță) come "encoder analitico" (collegamento G6 / RT-7).

## 2. Skill (Regola 2) e ordine d'uso
1. `anthropic-skills:deep-research` — invocata con Skill; workflow di ricerca/sintesi (ricerca condotta inline, senza spawn di subagenti salvo necessità).
2. `research-lit`, `arxiv`, `paper-lookup` (`_vendor\...\SKILL.md`, lette con Read, NON eseguo script) — per stringhe di ricerca e verifica riferimenti (arXiv IDs, DOI).
3. `math-skill` (modalità proof) — per le dimostrazioni brevi (G2 per ODE e PDE; controesempio G1).
4. `sympy` SKILL — script in `research/R2/sympy/` eseguiti con `.venv\Scripts\python.exe -I` (es. ker di (∂_t−∂_x²)(∂_t+∂_x), intersezione, esempio G1).
5. `scientific-critical-thinking` — passata finale di critica sulle affermazioni (cosa è noto / aperto / falso).

## 3. Fonti e stringhe di ricerca
- Hörmander, *ALPDO II*, cap. 7 (Thm 7.6.13/7.6.14, rappresentazione esponenziale), cap. 15 (Fundamental Principle, Thm 15.x).
- Ehrenpreis, *Fourier Analysis in Several Complex Variables* (1970); Palamodov, *Linear Differential Operators with Constant Coefficients* (1970); Malgrange, Ann. Inst. Fourier 6 (1955-56); Björk, *Rings of Differential Operators* (1979), cap. 8.
- Oberst, "Multidimensional constant linear systems" (Acta Appl. Math. 1990) — teorema di dualità / cogeneratore iniettivo (chiave per G2!).
- Cid-Ruiz–Sturmfels "Primary decomposition with differential operators" (arXiv 2101.03643); Chen–Cid-Ruiz–Härkönen–Krone–Leykin (Noetherian operators); Härkönen–Lange-Hegermann–Raiță "Gaussian Process Priors for Systems of Linear PDEs with Constant Coefficients" (ICML 2023, arXiv 2212.14319); Ait El Manssour–Härkönen–Sturmfels "Linear PDE with constant coefficients" (arXiv 2108.10406).
- Kauers–Paule, *The Concrete Tetrahedron* (2011) cap. 7; Stanley "Differentiably finite power series" (1980); Lipshitz (1989); Zeilberger (1990).
- van der Put–Singer, *Galois Theory of Linear Differential Equations* (2003); Singer "Testing reducibility" / LCLM; Ore (1933).
- Stringhe: "fundamental principle Ehrenpreis Palamodov statement", "injective cogenerator C infinity Oberst", "kernel of product of differential operators sum of kernels", "D-finite closure properties order bound", "Noetherian operators primary ideal", "least common left multiple kernel sum".

## 4. Comunicazione
- R3, R4: TABELLA operatore → V(P) → classe di funzioni (ker) → struttura (dim, base/frame) in `inbox/R3.md`, `inbox/R4.md`; leggere le loro tabelle.
- R5: rispondere alle DOMANDE su "quando E_int = 0" (fattorizzazione, commutazione, V(P_1)∩V(P_2)).
- central: `PLAN-READY R2`, eventuali `NEW-ROUTE`, `DONE R2`.
- Inbox `inbox/R2.md`: lettura all'inizio, a metà, prima della consegna.

## 5. Criterio di "fatto"
- REPORT.md con: enunciato esatto (ipotesi, spazio, riferimento preciso) del teorema G2/C4.2; stato di G1 (dimostrato/corretto/confutato) con script SymPy; risposta C4.4; scheda D-finite/olonome (C2.6) con proprietà di chiusura e bound; caso coeff. variabili (Ore/LCLM/Galois); mappa su C2/C4/P1 con stati noto/aperto/falso.
- sources.bib, open_questions.md, script in `research/R2/sympy/` con output citati.
- Messaggi TABELLA inviati a R3, R4; inbox controllata 3 volte; `DONE R2`.
