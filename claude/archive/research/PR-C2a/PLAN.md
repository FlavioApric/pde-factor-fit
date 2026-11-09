# PLAN — PR-C2a (Fase 1, pre-ricerca PR-C2, blocco Asse 1 T1: ODE lineari C2.1–C2.5 + MIT 18.03 Spring 2010)

Data: 2026-10-22 · Cartella: `research/PR-C2a/` · Notazione: `NOTAZIONE.md` v1 (simbolo con convenzione `e^{ξx}` ↔ `ξ`; caso ODE: variabile `x`, per 18.03 si usa `t` ⇔ `x`).

## 1. Domande (dal piano + aggiunte motivate)
Dal piano (§1.3 C2, §1.3-C2-EXT, §1.3-C2-TAX, card schema, PR-C2):
- Q1 (C2.1 ★) Per `p(D)` a coeff. costanti: classe del nucleo (esponenziali-polinomi `x^k e^{λx}`), base fondamentale, ruolo delle radici multiple/complesse; fattorizzazione ⇒ split additivo (G2 nel caso ODE).
- Q2 (C2.2 ★■) ODE forzate e sistemi: Green/risposta all'impulso, variazione dei parametri, ERF `p(D)e^{rx}=p(r)e^{rx}` e risonanza (formula `p'(r)`), esponenziale di matrice, Jordan ↔ classi `x^k e^{λx}`, matrice compagna (via II-b), matrici fondamentali, Abel/Liouville.
- Q3 (C2.3 ★▲) primo ordine lineare (fattore integrante, nucleo `exp(-∫a)`), separabili/esatte/omogenee; Bernoulli/Riccati/Clairaut/Lagrange come casi ▲ con linearizzazioni esatte (Bernoulli → lineare; Riccati ↔ ODE lineare del 2° ordine via `y = w'/(qw)`): questo è un "encoder" analitico (D1, G7).
- Q4 (C2.4 ★) coeff. variabili: Euler–Cauchy (`x^r (log x)^k`), Frobenius (punti singolari regolari, indiciale, casi di differenza intera → log), irregolari (asintotica, Stokes), riduzione d'ordine, serie di potenze, WKB; holonomia/D-finitezza.
- Q5 (C2.5 ★◇) ODE di funzioni speciali: operatore, nucleo, base, ortogonalità/peso (Gram per C1), relazione con l'ipergeometrica (Riemann P-symbol), origine da separazione delle variabili.
- Q6 (PR-C2.5) quali termini elementari compaiono: `∂`, `∂²`, `∂^n`, `x·`, `x²·`, `x∂`, `x²∂²`, `(1−x²)∂²`, `1/x`, …
Aggiunte motivate (per G★/C3/C4):
- Q7 Identificabilità ODE: `u` determina `L` (minimo annullatore) — Wronskiano/Hankel/Prony; punto di contatto con R4/C3 (solo segnalazione, non risoluzione).
- Q8 Per ogni classe: dati per C1 (prodotti scalari/Gram, peso, sistema duale/biortogonale, numerabile vs continuo).
- Q9 Per somme di termini nel caso ODE: `ker(L1+L2)` vs `ker L1 + ker L2` (esempi espliciti: `D²+1` vs `D²` e `1`), per alimentare G1.

## 2. Skill (Regola 2) — ordine e uso
1. `academic-research-skills\deep-research\SKILL.md` (letto con Read; NON invocata `anthropic-skills:deep-research` perché richiede sottoagenti, che non posso lanciare): workflow di ricerca (scoping → fonti → sintesi) applicato al blocco T1.
2. `scientific-agent-skills\skills\paper-lookup\SKILL.md` (Read): per riferimenti precisi (DLMF capitoli, articoli classici: Frobenius 1873, Fuchs, Kovacic 1986 per Liouvillian, Stokes).
3. `math-skill\SKILL.md` (Read, modalità `solver`) + `scientific-agent-skills\skills\sympy\SKILL.md` (Read): per scrivere gli script `sympy/*.py` che verificano `T e = 0` per ogni scheda ★/◆.
4. `scientific-agent-skills\skills\citation-management\SKILL.md` (Read): per `sources.bib`.
Nessuno script dei repository `_vendor` viene eseguito.

## 3. Fonti / stringhe di ricerca previste
- MIT OCW 18.03 Spring 2010 lecture notes (Miller): https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/lecture-notes/ (ERF, operatori, convoluzione, funzione di trasferimento, esponenziale di matrice).
- Coddington–Levinson *Theory of ODEs* (1955); Ince *Ordinary Differential Equations* (1926/1956); Hartman; Teschl *ODEs and Dynamical Systems* (AMS GSM 140); Birkhoff–Rota; Wasow *Asymptotic expansions for ODEs*; Olver *Asymptotics and Special Functions*; Bender–Orszag.
- DLMF (cap. 9 Airy, 10 Bessel, 13 confluenti, 14 Legendre, 15 ipergeometrica, 18 polinomi ortogonali, 30 sferoidali, 31 Heun); Abramowitz–Stegun; Nikiforov–Uvarov *Special Functions of Math. Physics*.
- Kauers–Paule *The Concrete Tetrahedron*; Stanley 1980 (D-finite); van der Put–Singer *Galois Theory of Linear Differential Equations*; Kovacic 1986.
- Higham *Functions of Matrices*; Gohberg–Lancaster–Rodman *Matrix Polynomials*.
- Stringhe: "exponential response formula", "exponential shift rule", "Frobenius method indicial equation logarithmic case", "Riccati linearization second order", "holonomic closure properties", "Wronskian annihilating operator".

## 4. Scambi (grafo di comunicazione)
- → PR-C2b (`inbox/PR-C2b.md`, TABELLA): appena pronta, lista operatore ODE → classe → base (mattoni dei nuclei PDE separati).
- → R3 (`inbox/R3.md`, TABELLA): schede ★ (link alle card).
- → central: `PLAN-READY PR-C2a`, poi `DONE PR-C2a`; eventuali NEW-ROUTE.
- Lettura `inbox/PR-C2a.md`: inizio (vuota al 22/10), a metà, prima della consegna.

## 5. Criterio di "fatto"
- `cards/` con: schede COMPLETE (punti 1–9) per C2.1, C2.2, C2.3 (parte lineare), C2.4, C2.5 (più sotto-schede per ciascuna famiglia speciale), ognuna con script SymPy in `sympy/` eseguito e output citato (`T e = 0` simbolicamente); schede brevi per le parti ▲ (Bernoulli, Riccati, Clairaut, Lagrange, autonome) e ■ (sistemi).
- Contributo alla matrice componenti PR-C2.5 (`components_T1.md`).
- `REPORT.md` (risultati mappati su C/P/II, teoremi chiave con fonte precisa, stato), `sources.bib`, `open_questions.md`; messaggi a PR-C2b e R3; `DONE PR-C2a` in central.
