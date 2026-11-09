# PR-C2b — PLAN (Fase 1, Regola 1)

Agente: PR-C2b · Blocco: Asse 1, T2–T9 (famiglie di PDE lineari) di §1.3-C2-TAX · Item: PR-C2.2, PR-C2.3 (+ contributi a PR-C2.4, PR-C2.5), C2, C4, C1.0
Data: 2026-10-22 · Notazione: `NOTAZIONE.md` v1 (L = Σ λ_k T_k, simbolo P(τ,ξ) con e^{τt+ξx}, V(P), Ann(u), 𝔾(u), E_int, S_n(t)).

## 1. Domande

### 1.1 Item del blocco e tipo di scheda
| T | item | tag (piano) | scheda |
|---|---|---|---|
| T2 primo ordine | C2.6 trasporto | ★▲ | COMPLETA (parte lineare) |
| | C2.18 primo ordine generale (Lagrange ★) | ▲(★) | breve + sotto-scheda completa per Lagrange lineare |
| | C2.25 Hamilton–Jacobi / iconale | ▲ | breve |
| T3 parabolico | C2.7 diffusione | ★▲ | COMPLETA |
| | C2.21 parabolico generale | ★ | COMPLETA |
| | C2.39 diffusione non lineare | ▲ | breve |
| T4 iperbolico | C2.8 onde | ★◇ | COMPLETA |
| | C2.22 sistemi iperbolici | ★■ | COMPLETA |
| | C2.31 relativistico (Klein–Gordon ★) | ■◇ | breve + sotto-scheda completa KG |
| T5 ellittico | C2.9 ellittico | ★◇ | COMPLETA |
| | C2.20 BVP ellittici | ★◇ | COMPLETA |
| | C2.34 potenziale / analisi armonica | ◇ | breve |
| | C2.35 Helmholtz / autovalori | ★◇ | COMPLETA |
| T6 dispersivo | C2.10 dispersivo (Airy) | ★ | COMPLETA |
| | C2.30 quantistico (Schrödinger libero ★) | ★●▲ | COMPLETA (parte libera) |
| | C2.46 dispersivo non lineare | ▲ | breve |
| T7 reazione | C2.11 reazione/crescita | ★▲ | COMPLETA (parte lineare) |
| | C2.42 pattern formation | ▲■ | breve |
| T8 composti (banco di prova di E_int) | C2.12 avvezione–diffusione, telegrafo, onda smorzata | ★ | COMPLETA |
| | C2.19 ordine superiore (fattorizzazione) | ★ | COMPLETA |
| | C2.23 tipo misto (Tricomi, Keldysh) | ◇ | breve |
| T9 non locale | C2.37 integrali / non locali | ◆★ | COMPLETA |
| | C2.38 frazionarie | ◆★ | COMPLETA |

### 1.2 Domande per ogni scheda (card schema 1–9 del piano)
Q1 operatore/i canonico/i T e simbolo P(τ,ξ); Q2 ker T, base {e_{n,i}}, numerabile vs continua; Q3 funzioni speciali e trasformate (soluzione fondamentale, Green, autofunzioni); Q4 decomposizione in componenti: fattorizzazione ⇒ additiva (E_int = 0 modulo ker(P_1,P_2)), somma di termini commutanti ⇒ moltiplicativa, non commutanti ⇒ commutatori; Q5 dati per C1: blocchi di Gram con le altre classi, sistema duale/biortogonale, insieme di indici; Q6 attributi S1–S15; Q7 tag; Q8 fonti; Q9 verifica SymPy T e = 0.

### 1.3 Domande trasversali (aggiunte motivate da G★, G1–G7 di NOTAZIONE)
- QX1 (C4/G1–G2, PR-C2.4) Per ogni coppia di termini che compare in T8: ker P_1 ∩ ker P_2 e dimensione di ker(P_1,P_2) (deve essere finita: lunghezza di ℂ[τ,ξ]/(P_1,P_2)).
- QX2 (C1.0) Formula generale dei blocchi di Gram tra classi esponenziali a coefficienti costanti su 𝕋×[0,T] e coerenza inter-classe in funzione della frequenza.
- QX3 (G3/P3) Dove la regola "somma di termini commutanti ⇒ prodotto" vale, dove fallisce (secondo ordine in t, Caputo, coefficienti variabili) e cosa la sostituisce (Zassenhaus/Wei–Norman, subordinazione).
- QX4 (G4/C3) Nota di identificabilità per famiglia: quando u determina il simbolo.
- QX5 (Idea II, via (b)) Sistemi del primo ordine/matrice compagna: dove la riduzione introduce non-commutatività.
- QX6 (ω) Strade nuove → NEW-ROUTE in inbox/central.md.

## 2. Skill (Regola 2) — ordine e uso
1. `anthropic-skills:deep-research` — NON invocata con Skill: coordina subagenti, e lo spawn non è autorizzato in questo ruolo. Al suo posto ho letto integralmente `_vendor\academic-research-skills\deep-research\SKILL.md` e ne seguo il workflow ridotto (scoping → raccolta fonti → verifica → sintesi con citazioni; regola "ogni claim ha una citazione", "difficile da verificare = non citare / marcare DA VERIFICARE").
2. `paper-lookup` (`_vendor\scientific-agent-skills\skills\paper-lookup\SKILL.md`, letto) — strategia di lookup (arXiv/Crossref/OpenAlex via WebSearch/WebFetch); nessuno script bundled eseguito.
3. `sympy` (`_vendor\scientific-agent-skills\skills\sympy\SKILL.md`, letto) + `math-skill` (`_vendor\math-skill\SKILL.md`, letto, modalità `solver`: mappa del problema → metodo → verifica sostituendo indietro) — script propri in `research/PR-C2b/sympy/*.py`, eseguiti con `D:\ProblemaBase\.venv\Scripts\python.exe -I`. Nessuno script `_vendor` eseguito.
4. `citation-management` (`_vendor\scientific-agent-skills\skills\citation-management\SKILL.md`, letto) — formato e verifica di `sources.bib` (metadati verificati; voci non verificate marcate `note = {DA VERIFICARE}`).

## 3. Fonti / stringhe di ricerca previste
- Testi del blocco: Hancock, MIT 18.303 Fall 2006 lecture notes (OCW); Guenther–Lee (Dover 1996); Myint-U–Debnath 4th ed.; Polyanin *Handbook of Linear PDEs* (2002; 2nd ed. 2016 con Nazaikinskii).
- Teoria: Evans (2010); Hörmander ALPDO I–II; Ehrenpreis (1970); Palamodov (1970); Ait El Manssour–Härkönen–Sturmfels "Linear PDE with constant coefficients"; Widder *The Heat Equation* (1975) e Rosenbloom–Widder (1959) (polinomi del calore e biortogonalità); Wei–Norman (1963); Wilcox (1967) (BCH/Zassenhaus); Engel–Nagel (2000) (semigruppi, Trotter); Schwartz (1947) (funzioni medio-periodiche); Kilbas–Srivastava–Trujillo (2006), Mainardi (2010), Gorenflo–Kilbas–Mainardi–Rogosin (2014), Kwaśnicki (2017), Caffarelli–Silvestre (2007); Vallée–Soares (Airy); DLMF cap. 9, 10, 18; Whitham (1974); Courant–Hilbert II; Otway (Keldysh); Bitsadze (tipo misto); Vázquez (mezzi porosi); Murray (Turing).
- Stringhe: "heat polynomials associated functions biorthogonal Rosenbloom Widder", "Wei Norman Lie algebraic solution linear differential equations", "linear PDE constant coefficients Ehrenpreis Palamodov Sturmfels", "Gurevich counterexample spectral synthesis", "fundamental solution telegraph equation modified Bessel I0", "M-Wright function time fractional diffusion fundamental solution", "Caffarelli Silvestre extension", "MIT OCW 18.303 Fall 2006 lecture notes".

## 4. Comunicazione (grafo del piano)
- **Ricevo** da PR-C2a i nuclei ODE (inbox/PR-C2b.md): li uso come mattoni dei nuclei separati (Bessel per membrane/Helmholtz, Airy per Tricomi, Hermite per OU, Sturm–Liouville per diffusività variabile).
- **PR-C2b ↔ PR-C2e**: invio in inbox/PR-C2e.md la tabella "termine elementare × famiglia" (per la matrice delle componenti PR-C2.5) + nuclei per l'indice incrociato PR-C2.4; rispondo alle loro DOMANDE.
- **→ R3**: invio in inbox/R3.md l'elenco/sintesi delle schede ★ con i percorsi.
- **→ central**: `PLAN-READY PR-C2b`; eventuali NEW-ROUTE; `DONE PR-C2b` alla fine.
- Inbox letta: all'inizio (fatto: vuota), a metà (dopo gli script SymPy), prima della consegna.

## 5. Criterio di "fatto"
- `cards/` con 15 schede COMPLETE (★/◆: C2.6, C2.7, C2.8, C2.9, C2.10, C2.11, C2.12, C2.19, C2.20, C2.21, C2.22, C2.30, C2.35, C2.37, C2.38) + 8 schede brevi (C2.18 con sotto-scheda Lagrange, C2.25, C2.31 con sotto-scheda KG, C2.34, C2.39, C2.42, C2.46, C2.23);
- ogni scheda completa ha la verifica SymPy T e = 0 eseguita (PASS citato) e fonti;
- REPORT.md: risultati mappati su C1/C2/C4/P1/P3/II, proposizioni con ID `[PR-C2b-P#]`, stato (noto / dimostrato qui / aperto / probabilmente falso);
- sources.bib, open_questions.md; messaggi a PR-C2e e R3; `DONE PR-C2b` in inbox/central.md.
