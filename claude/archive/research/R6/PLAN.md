# R6 — PLAN (Fase 1, Idea II: formulazione matrice/tensore)

Data: 2026-10-22 · Agente: R6 · Item: II (II.1, II.2, II.3; contributo a II.4 via R7), domande E4, E5, F1/F2, F3–F6, G6, congettura G5 (NOTAZIONE.md), ROUTES RT-5 / RT-6.

## 1. Domande (dal piano + aggiunte motivate)
Dal piano (0B D2–G6, §1.2 punto 3, item II, tabella Fase 1):
- Q1 (D2, H4) Formalizzare "J_φ·Φ = 0": che oggetto è J_φ = ∂_i⊗∂_j? (tensore simbolo / jet / Gram del jet). Relazione con `λ ∈ ker 𝔾(u)`.
- Q2 (D3–D4, via a) Il tensore J^n_φ = ∂⊗…⊗∂ e J_{ω,λ} = λ⊗J_φ: quale struttura matematica (Sym^n, simbolo principale/simbolo totale come polinomio, tensore dei coefficienti)? Quali invarianti (GL₂/O₂: discriminante, invarianti di forme binarie; autovalori di tensori di Qi/Lim; HOSVD)?
- Q3 (D5, E1, via b) La compagna C(p); la "non-matrice" con ultima riga f_k(x) = matrice su anello (ℂ[x], C^∞, algebra di Weyl A₁). Invarianti: polinomio caratteristico, Jordan/Frobenius (forme normali razionali), Smith (su ℂ[D]), Jacobson/Teichmüller (su anelli di Ore), modulo D/DL. Verificare G5.
- Q4 (E4) Quale costruzione conserva più invarianti per l'ordine del sistema? Tabella II.1, sotto quale gruppo (similitudine, gauge x-dipendente, cambio di coordinate, GL/O sulle variabili).
- Q5 (E5, G6) Spazio ridotto: SVD/HOSVD/Tucker di J_ω; cosa significa per un operatore? (rango del Gram del jet, rango di Hankel, rango tensoriale del simbolo).
- Q6 (F1, F2, E2, E3) â = f(J·Φ) = Σ f(λ_a) v_a⊗v_a: calcolo funzionale di matrici (Higham), caso non diagonalizzabile (Jordan, derivate di f), autovettori generalizzati di tensori; versione operatoriale (simbolo, Fourier multiplier). Link C4.3: log-simbolo additivo (II.3).
- Q7 (F6, G6) "Rompere il sistema per direzioni": diagonalizzazione simultanea, decomposizione primaria/spettrale della compagna ⇔ fattorizzazione di p ⇔ split ker P = ⊕ ker P_i (link con G2, C4.2).
- Q8 (II.2) Coefficienti variabili: matrici su A₁, D-moduli, forma normale di Jacobson; ciclicità (lemma del vettore ciclico, Katz) — ogni sistema ⇔ un'equazione scalare.
- Q9 (G3–G4) Brevemente: cosa resta per f(S·x) non lineare (solo pointer, Fase 4).
Aggiunte motivate:
- Q10 Problemi agli autovalori polinomiali (Gohberg–Lancaster–Rodman): linearizzazione L(λ)=Σ A_jλ^j → pencil compagno; serve per Problema 2 (coeff. Mat 4×4, solo lettura) e perché ogni linearizzazione "forte" conserva divisori elementari finiti e infiniti (= invarianti completi).
- Q11 Spazi di jet (Olver): J_φ·Φ = 0 come sottovarietà dello spazio dei jet; prolungamento; relazione con il Gram del jet.
- Q12 Identificazione dalla via (b): dalla soluzione u alla compagna (Hankel/Krylov: la matrice di Wronski/Hankel del jet di u dà C(p) per similitudine) — ponte con C3/R4.

## 2. Skill (Regola 2) — ordine e uso
1. `academic-research-skills\deep-research\SKILL.md` (letto con Read; modalità "lit-review / quick brief", eseguita in linea senza sotto-agenti) — impostazione della ricerca bibliografica. (`anthropic-skills:deep-research` non invocata: coordina sotto-agenti, non necessari qui.)
2. `Auto-claude-code-research-in-sleep\skills\research-lit\SKILL.md` + `…\skills\arxiv\SKILL.md` (lette; uso solo `web` via WebSearch/WebFetch, NESSUNO script `_vendor` eseguito) — verifica riferimenti (Lim 2005, Qi 2005, Cartwright–Sturmfels 2013, Higham 2008, GLR 1982/2009, Jacobson 1943, Coutinho 1995, Olver 1993, Gantmacher 1959).
3. `math-skill\SKILL.md` modalità `proof` — enunciati e dimostrazioni brevi (separazione esplorazione/prova, controesempi presto).
4. `scientific-agent-skills\skills\sympy\SKILL.md` — script in `research/R6/sympy/` eseguiti con `D:\ProblemaBase\.venv\Scripts\python.exe -I`: Smith form, e^{xC}, invarianti similitudine, gauge, Jacobson esempio, HOSVD rango, tensor eigen.
5. `…\skills\formula-derivation\SKILL.md` — pacchetto di derivazione per â = f(J·Φ) (stato COHERENT / REFRAMED / NOT YET).
6. `scientific-agent-skills\skills\scientific-critical-thinking\SKILL.md` — passata critica finale su E4 (cosa è dimostrato vs congettura).

## 3. Fonti / stringhe
Higham *Functions of Matrices* (SIAM 2008); Gohberg–Lancaster–Rodman *Matrix Polynomials* (1982/SIAM 2009); Gantmacher *Theory of Matrices* (1959); Jacobson *Theory of Rings* (1943) cap. 3; Cohn *Free Rings*; Coutinho *A Primer of Algebraic D-modules* (1995); Olver *Applications of Lie Groups to DEs* (1993) cap. 2–3; Lim "Singular values and eigenvalues of tensors" (CAMSAP 2005); Qi "Eigenvalues of a real supersymmetric tensor" (JSC 2005); Qi–Luo *Tensor Analysis* (SIAM 2017); Cartwright–Sturmfels "The number of eigenvalues of a tensor" (LAA 2013); De Lathauwer–De Moor–Vandewalle HOSVD (SIMAX 2000); Hillar–Lim "Most tensor problems are NP-hard" (JACM 2013); Katz cyclic vector (1987); Mackey–Mackey–Mehl–Mehrmann (linearizations, SIMAX 2006); Hörmander vol. III (simboli); Taylor *Pseudodifferential operators*; Kolchin/van der Put–Singer (forme normali, ciclicità).
Stringhe: "tensor eigenvalue number Cartwright Sturmfels", "Jacobson normal form Ore polynomial matrices", "cyclic vector lemma differential module", "strong linearization elementary divisors", "companion matrix similarity invariants", "symbol of differential operator binary form invariants".

## 4. Comunicazione
- R7 (inbox/R7.md): invio TABELLA degli invarianti (via a vs via b) + DOMANDA su simmetrie/rotazioni (gruppi che agiscono sul simbolo, O(2) su (τ,ξ), Lie point symmetries ↔ invarianti della compagna).
- R5: leggo inbox/R5 e research/R5 (algebre di Lie, BCH) quando disponibili.
- central: `PLAN-READY R6`; eventuali `NEW-ROUTE` (D-modulo/ciclicità come forma canonica; Clifford per Problema 2).
- Controllo inbox/R6.md: inizio (fatto: vuota), metà, prima della consegna.

## 5. Criterio di "fatto"
REPORT.md con: (i) tabella II.1 invarianti a vs b con teoremi e fonti esatte; (ii) risposta a E4 con stato; (iii) G5 verificata/corretta; (iv) II.2 (Weyl/Jacobson/Katz), II.3 (calcolo funzionale ↔ log-simbolo), E5 (spazio ridotto); (v) ≥5 verifiche SymPy eseguite e citate; sources.bib; open_questions.md; messaggi a R7 e central; `DONE R6`.
