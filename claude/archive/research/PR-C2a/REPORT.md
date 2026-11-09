# REPORT — PR-C2a (Fase 1): Asse 1 T1, ODE lineari C2.1–C2.5 + MIT 18.03 Spring 2010
Data 2026-10-22 · Cartella research/PR-C2a/ · Notazione NOTAZIONE.md v1
*(Salvato dal coordinatore dalla risposta finale di PR-C2a: la scrittura diretta era bloccata dall'ambiente.)*

## 0. Skill caricate (Regola 2)
- academic-research-skills\deep-research\SKILL.md — Read (anthropic-skills:deep-research non invocata: richiede sottoagenti); workflow scoping → fonti → sintesi.
- scientific-agent-skills\skills\paper-lookup\SKILL.md — Read; criteri di provenienza; nessuna chiamata API (fonti: libri di testo e DLMF).
- math-skill\SKILL.md (solver) — Read; mappa del problema, verifica aggressiva.
- scientific-agent-skills\skills\sympy\SKILL.md — Read; script sympy/*.py esatti; numerica solo come controllo per I_ν e K_ν.
- scientific-agent-skills\skills\citation-management\SKILL.md — Read; formato di sources.bib (29 voci).

Nessuno script _vendor eseguito. Unica fonte web: indice delle lecture notes MIT 18.03 Spring 2010 (WebFetch, 2026-10-22).

## 1. Deliverable
- cards/C2.1_coeff_costanti.md ★ — completa, 34/34 OK
- cards/C2.2_forzate_sistemi.md ★■ — completa, 16/16 OK
- cards/C2.3_primo_ordine.md ★▲ — completa per la parte lineare, schede brevi ▲ (Bernoulli, Riccati, Clairaut, Lagrange…); 18/18 OK
- cards/C2.4_coeff_variabili.md ★ — completa, 14/14 OK
- cards/C2.5_funzioni_speciali.md ★◇ — completa + 11 sotto-schede; 39/39 OK
- cards/MIT_18.03_mappa.md
- components_T1.md (contributo a PR-C2.5)
- sources.bib, open_questions.md (7 punti)

Totale: 121/121 OK; output in sympy/*.out.txt.

## 2. Risultati
Stati: NOTO = teorema in letteratura; VERIF = verificato qui in SymPy; FALSO; PROPOSTA.

### 2.1 C2 (catalogo)
**[T1-1] Nucleo a coeff. costanti** — NOTO + VERIF. ker p(D) generato da x^j e^{λ_i x}, j < m_i; dim = deg p (Coddington–Levinson 1955 cap. 3). Caratterizzazione inversa: i sottospazi di dimensione finita invarianti per traslazione sono esattamente i ker p(D) (Anselone–Korevaar, Proc. AMS 15, 1964).

**[T1-2] ERF, shift rule, risonanza** — NOTO + VERIF. p(D)e^{rx} = p(r)e^{rx}; p(D)(e^{rx}g) = e^{rx}p(D+r)g; soluzione risonante x^k e^{rx}/p^{(k)}(r) (MIT 18.03 L13, L15). Per II/F1: azione del simbolo sulle autofunzioni di D.

**[T1-3] Green** — NOTO + VERIF. g = L^{-1}[1/p] = [e^{xC(p)}]_{0,m−1}; soluzione forzata y = g*f (Coddington–Levinson cap. 3; 18.03 L24–L30, L36).

**[T1-4] Jordan ↔ radici multiple** — NOTO + VERIF. La forma di Jordan della compagna C(p) riproduce le molteplicità; C(p) non derogatoria, unico invariante di similitudine p (→ II.1/R6).

**[T1-5] Primo ordine** — NOTO + VERIF. ker(D+a) generato da e^{−∫a}; D+a = μ^{-1}Dμ (gauge). Linearizzazioni esatte verificate: Bernoulli, Riccati (↔ lineare del 2° ordine), Lagrange.

**[T1-6] Frobenius e asintotica** — NOTO + VERIF (su J0). Equazione indiciale e caso logaritmico; punti irregolari: singolarità essenziali, serie divergenti; WKB con residuo relativo esatto 5Q'²/(16Q²) − Q''/(4Q) (Coddington–Levinson cap. 4–5; Wasow 1965; Olver 1974).

**[T1-7] Riduzione ipergeometrica** — NOTO + VERIF (identità di operatore, parametri simbolici). Jacobi ⊃ Gegenbauer ⊃ Legendre, Chebyshev; Legendre associate via gauge; tutte → ₂F₁. Hermite, Laguerre → ₁F₁. Bessel → ₀F₁; Airy → Bessel di ordine 1/3. Sferoidali non ipergeometriche: ricorrenza a tre termini (Heun confluente). Fonti: DLMF cap. 9, 10, 13, 14, 15, 18, 30; Nikiforov–Uvarov.

**[T1-8] Gram** — NOTO + VERIF. Legendre 2/(2n+1); Hermite √π 2^n n!; Laguerre Γ(n+α+1)/n!; Chebyshev π, π/2; esponenziali: Gram di tipo Cauchy (j+k)!/(s1+s2)^{j+k+1}.

### 2.2 C4 / G1–G2
**[T1-9] Fattorizzazione** — NOTO + VERIF. p = p1·p2 coprimi ⇒ ker p = ker p1 ⊕ ker p2, proiettori differenziali da Bezout; a coeff. variabili lo split esatto vale per LCLM, non per il prodotto (van der Put–Singer).

**[T1-10] A8 additivo per somma di termini** — FALSO (controesempio VERIF). sin x ∈ ker(D²+1), ma ker(D²+1) ∩ (ker D² + ker 1) = {0}. Nel simbolo i termini si sommano linearmente (Vandermonde).

**[T1-11] Componenti naturali** — PROPOSTA (per C4.1/C3.3). Coeff. costanti: i fattori primari (D−λ)^m. Coeff. polinomiali: i dati locali nei punti singolari (simbolo di Riemann; rigidità di Katz — cfr. RT-S1e).

### 2.3 C3 / G4
**[T1-12] Annullatore a coeff. costanti** — NOTO + VERIF. Ann(u) = (p_u) principale; ricostruzione dal nucleo del jet (Wronski/Hankel/Prony): u = e^x + x e^{−2x} ⇒ p = (D−1)(D+2)²; L identificabile ⟺ ordine = deg p_u.

**[T1-13] Primo ordine, coeff. variabile** — VERIF (elementare). a = −(log u)' sempre unico dove u ≠ 0.

**[T1-14] Coeff. polinomiali** — NOTO. Annullatori = ideale sinistro; principale in C(x)<D>; in A_1 al più 2 generatori (Stafford 1978); metodo: guessing D-finito (Kauers) → R4.

### 2.4 P1/P3/II
**[T1-15] Sistemi** — NOTO. e^{x(A1+A2)} = e^{xA1}e^{xA2} se [A1,A2] = 0, altrimenti BCH/Zassenhaus; autovettori sinistri = sistema duale e† di P3 (→ R5/R6).

**[T1-16] Riccati come Cole–Hopf ODE** — NOTO + VERIF. Riccati → lineare del 2° ordine via derivata logaritmica: prototipo di Cole–Hopf, candidato encoder analitico D1 (G7).

## 3. Comunicazioni
- PR-C2b (TABELLA): operatore ODE → classe → base → dove compare per separazione.
- PR-C2e (RISPOSTA): matrice delle componenti, 9 termini nuovi, nessun conflitto.
- R3 (TABELLA): schede ★.

## 4. Limiti
- Per n generico la verifica passa da identità di operatore e ricorrenze esatte; controllo diretto per n = 0..6.
- I_ν, K_ν: identità esatta + controllo numerico (solo verifica).
- Sferoidali: verificata solo la struttura (ricorrenza e limite c → 0).
- Sezioni di Teschl da confermare (open_questions punto 7).
