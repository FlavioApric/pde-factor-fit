# R3 — PLAN (Fase 1, Regola 1)

Agente: R3 · Tema: catalogo termine-per-termine dei pezzi di PDE lineari 1D · Item: C2 (core ladder C2.1ᵈ–C2.7ᵈ), C4 (C4.1–C4.4, lato catalogo)
Data: 2026-10-22 · Notazione: `NOTAZIONE.md` v1 (L = Σ λ_k T_k, simbolo P(τ,ξ) con e^{τt+ξx}, V(P), Ann(u), E_int).

## 1. Domande (dal piano §1.3 C2/C4, tabella Phase 1 riga R3, card schema 1–9)
Per ciascuna voce del catalogo — ∂_t, ∂_x / trasporto ∂_t+c∂_x, diffusione ∂_t−D∂_xx, dispersione ∂_t+∂_xxx (Airy), reazione ∂_t−r, coeff. dipendenti da x (Euler–Cauchy, Frobenius, x∂_x, Hermite/OU, Legendre, Bessel), Laplaciano polare/cilindrico (Bessel), trave ∂_t²+∂_x⁴, più ODE a coeff. costanti (C2.1ᵈ) e Sturm–Liouville (C2.13):
- Q1 (card 1) operatore canonico T e simbolo p(τ,ξ);
- Q2 (card 2) ker T / classe soluzioni, base {e_{n,i}}, numerabile vs continua;
- Q3 (card 3) funzioni speciali e trasformate; soluzione fondamentale / funzione di Green; autofunzioni;
- Q4 (card 4) decomposizione: fattorizzazione ⇒ additivo; somma di termini commutanti ⇒ moltiplicativo; non commutanti ⇒ commutatori;
- Q5 (card 5) dati per C1: blocchi di Gram con altre classi, sistema duale/biortogonale;
- Q6 (card 6) attributi Asse 4 (S1–S15) essenziali;
- Q7 (card 7) tag di rilevanza (★◆▲■●◇○);
- Q8 (card 8) fonti esatte;
- Q9 (card 9) verifica SymPy T e = 0 (script in `sympy/`).
Domande trasversali (aggiunte motivate, servono a C4 e al cluster R2↔R3↔R4):
- Q10 (C4.1/A8) per le combinazioni del catalogo (trasporto+diffusione, diffusione+dispersione, diffusione+reazione, trave = fattorizzazione) cosa succede a ker(L₁+L₂) vs ker L₁ + ker L₂? Controesempio esplicito ad A8 come scritta + forma moltiplicativa corretta (verifica SymPy).
- Q11 (C4.2) ker(P₁P₂) = ker P₁ + ker P₂ su esempi del catalogo (trave: ∂_x⁴−k⁴ = (∂_x²−k²)(∂_x²+k²)).
- Q12 (C4.4) quali classi sono numerabili (problemi su 𝕋 o intervallo, SL regolare) e quali continue (ℝ, spettro continuo).
- Q13 (Idea II/F1) per ogni termine: modo e^{τt+ξx} con τ = p(ξ) — la "relazione di dispersione" è la tabella operatore→classe nella forma più compatta.
- Q14 (ω) strade nuove → NEW-ROUTE.

## 2. Skill (Regola 2) — ordine e uso
1. `anthropic-skills:deep-research` — NON invocata con Skill perché coordina subagenti (spawn non autorizzato in questo ruolo); al suo posto carico `_vendor\academic-research-skills\deep-research\SKILL.md` leggendolo e ne seguo il workflow (scoping → fonti → sintesi con citazioni).
2. `paper-lookup` (`_vendor\scientific-agent-skills\skills\paper-lookup\SKILL.md`) / `research-lit` — letti, per la strategia di ricerca bibliografica (WebSearch/WebFetch su DLMF, OCW, se necessario).
3. `sympy` (`_vendor\scientific-agent-skills\skills\sympy\SKILL.md`) e `math-skill` (`_vendor\math-skill\SKILL.md`, modalità solver) — letti; verifiche T e = 0 in `research/R3/sympy/*.py`, eseguite con `D:\ProblemaBase\.venv\Scripts\python.exe -I`. Nessuno script dei `_vendor` eseguito.
4. `citation-management` (`_vendor\scientific-agent-skills\skills\citation-management\SKILL.md`) — letto, per `sources.bib`.

## 3. Fonti / stringhe di ricerca
Evans PDE (2nd ed., AMS 2010) §2.1–2.4, §4.3; Courant–Hilbert vol. I cap. V–VII, vol. II; Polyanin *Handbook of Linear PDEs for Engineers and Scientists* (2002/2nd ed. 2016) cap. 1 (eq. del calore), 3, 4, 7–8 (terzo/quarto ordine); DLMF cap. 9 (Airy), 10 (Bessel), 14 (Legendre), 18 (ortogonali: Hermite), 13 (ipergeometriche confluenti); Zettl *Sturm–Liouville Theory* (AMS 2005); Titchmarsh *Eigenfunction Expansions*; MIT 18.03 (2010) e 18.303 (2006); Guenther–Lee (Dover 1996); Myint-U–Debnath 4th ed. (2007); Coddington–Levinson; Ehrenpreis; Hörmander vol. II.
Stringhe: "fundamental solution linearized KdV Airy kernel", "Euler-Bernoulli beam fundamental solution Fresnel", "Sturm-Liouville completeness Zettl", "DLMF 9.2 Airy", "DLMF 10.2 Bessel", "Mehler kernel Hermite".

## 4. Comunicazione
- Leggo `inbox/R3.md` all'inizio, a metà, prima della consegna; raccolgo schede da PR-C2a…e.
- Invio TABELLA operatore→classe a `inbox/R2.md` e `inbox/R4.md`; integro le loro.
- NEW-ROUTE in `inbox/central.md` se emerge una strada nuova.
- Scrivo solo in `research/R3/` + `inbox/`.

## 5. Criterio di "fatto"
- REPORT.md con ≥ 12 schede (card 1–9) per le voci elencate, ciascuna con script SymPy eseguito e output citato (PASS);
- sezione C4: stato di A8 sul catalogo (controesempio + forma moltiplicativa) verificato SymPy;
- tabella operatore→classe inviata a R2, R4; schede PR-C2 integrate (o annotata la loro assenza);
- sources.bib, open_questions.md; `DONE R3` in inbox/central.md.
