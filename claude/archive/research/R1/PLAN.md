# R1 — PLAN (Fase 1, Regola 1)

Tema: spazi di Hilbert ↔ ML in forma analitica. RKHS, teorema del rappresentante, regolarizzazione di Tikhonov, L¹ vs L² (compressed sensing: RIP, coerenza, NSP), processi gaussiani come oggetti analitici, teoria spettrale Koopman/DMD.
Item: C1 (C1.0–C1.4), P2 (P2.1–P2.3); domanda B8 ("ℒ_ALT elimina E_int?"), C1 di Pg.C ("ci sono regolarizzazioni che lo eliminano?").
Notazione: `NOTAZIONE.md` (L = Σλ_k T_k, Φ(u), 𝔾(u), Ann(u), K_n, E_int).

## 1. Domande
Dal piano:
- **C1.0** Funtore catalogo C2 → (𝓗_𝒟, Gram G, nucleo K, sistema duale): ben definito? positività, completezza, limiti di Riesz in funzione della coerenza inter-classe.
- **C1.1** Spazi candidati: L², H^k, RKHS con K(x,y)=Σ e_{n,i}(x)e_{n,i}(y), spazi analitici/Bargmann (Fock), spazio di Ehrenpreis L²(V(P),μ) (G6, RT-7).
- **C1.2** Teorema del rappresentante → ω in forma chiusa (inverso della Gram); limite α→0 (pseudo-inversa / interpolazione a norma minima).
- **C1.3** Completezza, minimalità, proprietà di Riesz (A7: le basi devono essere numerabili? → frame continui).
- **C1.4** Sistema duale/biortogonale e^†_{n,i} (alimenta P3).
- **P2.1** Teoremi di recupero esatto (NSP, coerenza, RIP, ERC di Tropp) specializzati a dizionari di nuclei (gaussiane del calore, esponenziali, Airy).
- **P2.2** Coerenza tra classi (gaussiane vs Airy, esponenziali vs esponenziali).
- **P2.3** Altri regolarizzatori (B7): TV, group-L¹ (per componente, "grouping" di D1), reweighted L¹, norma atomica / super-risoluzione.
- **B8** ℒ_ALT (L¹) elimina E_int? Prova che L² non può (distribuisce il peso).
Aggiunte motivate:
- **R1-a** Distinguere i DUE problemi di sparsità presenti nel progetto: (i) sparsità dei coefficienti dell'operatore λ (stile SINDy: 𝔾(u)λ=0, λ sparso) ⇒ legame con identificabilità (R4); (ii) sparsità della sintesi di u nel dizionario delle classi ⇒ decomposizione u=Σu_n (A8). B8 vive in (ii).
- **R1-b** Dizionari continui (parametro reale: esponenziali e^{λx}, gaussiane di varianza variabile) ⇒ norma atomica / super-risoluzione (Candès–Fernandez-Granda; Prony) invece del CS discreto.
- **R1-c** Processi gaussiani: posterior mean = interpolante RKHS (Kimeldorf–Wahba); GP vincolati a PDE lineari (EPGP) come prior "in ker L".
- **R1-d** Koopman/DMD: per u_t=Au a coeff. costanti, DMD esatta = Prony multicanale; spettro di Koopman del flusso lineare = simbolo.

## 2. Skill (Regola 2) — ordine e uso
1. `anthropic-skills:deep-research` (strumento Skill) — impostare il workflow di ricerca/sintesi (domande → fonti → sintesi narrativa con citazioni). Nessun subagente aggiuntivo se non necessario.
2. `_vendor\Auto-claude-code-research-in-sleep\skills\research-lit\SKILL.md` e `…\skills\openalex\SKILL.md` / `scientific-agent-skills\skills\paper-lookup\SKILL.md` (lettura SKILL.md, nessuno script eseguito) — verifica dei riferimenti bibliografici (titoli, anni, DOI) via ricerca web.
3. `_vendor\math-skill\SKILL.md` modo `proof` — dimostrazioni delle proposizioni nuove/specializzazioni (es. Gram di gaussiane, coerenza, controesempio B8).
4. `scientific-agent-skills\skills\sympy\SKILL.md` — controlli simbolici (prodotti scalari gaussiana–gaussiana, coerenze), con `.venv\Scripts\python.exe -I`.
5. `scientific-agent-skills\skills\scientific-critical-thinking\SKILL.md` — valutazione finale dei claim (noto / aperto / probabilmente falso).

## 3. Fonti e stringhe di ricerca previste
Core: Aronszajn 1950 (Theory of reproducing kernels); Schölkopf–Herbrich–Smola 2001 (generalized representer theorem) e Schölkopf–Smola 2002; Kimeldorf–Wahba 1971; Engl–Hanke–Neubauer 1996 (cap. 2–5); Candès–Romberg–Tao 2006; Candès–Tao 2005; Candès 2008 (RIP); Donoho 2006; Donoho–Elad 2003; Donoho–Huo 2001; Gribonval–Nielsen 2003; Tropp 2004 (Greed is good), 2006 (Just relax); Foucart–Rauhut 2013 (libro); Christensen (frames); Young (nonharmonic Fourier series); Candès–Fernandez-Granda 2014; Chandrasekaran–Recht–Parrilo–Willsky 2012 (atomic norm); Eldar–Mishali 2009 / Eldar–Kuppinger–Bölcskei 2010 (block sparsity); Rasmussen–Williams 2006; Mezić 2005; Rowley et al. 2009; Tu et al. 2014; Härkönen–Lange-Hegermann–Raiță 2023 (EPGP); Bach–Jenatton–Mairal–Obozinski (structured sparsity); Rudin–Osher–Fatemi 1992; Candès–Wakin–Boyd 2008 (reweighted L¹).
Stringhe: "representer theorem generalized", "null space property basis pursuit exact recovery", "exact recovery condition Tropp", "mutual coherence uncertainty principle Donoho Elad", "block sparsity coherence Eldar", "super-resolution atomic norm minimum separation", "Gaussian process linear PDE constraints Ehrenpreis", "dynamic mode decomposition Prony Koopman", "Müntz–Szász exponentials completeness", "Riesz basis exponentials Kadec".

## 4. Comunicazione
- **R1 → R4**: TABELLA dei teoremi di recupero esatto (ipotesi, conclusione, fonte) + DOMANDA: le vostre condizioni di identificabilità (Prony, annullatore, Ehrenpreis) in termini di rango/coerenza.
- **PR-C2d → R1**: ricevo spazi funzionali (Axis 2/3). Controllo `inbox/R1.md` inizio, metà, fine.
- **central**: PLAN-READY R1; eventuali NEW-ROUTE (es. norma atomica/super-risoluzione come strada per C1/P2; GP-Ehrenpreis); DONE R1.
- R5 (E_int) / R2: AVVISO se il risultato B8 dipende dalla definizione di E_int.

## 5. Criterio di "fatto"
- REPORT.md con: per ciascuna di C1.0–C1.4, P2.1–P2.3, B8 un enunciato preciso (ipotesi esatte, fonte con capitolo/teorema), la specializzazione a nuclei del calore / esponenziali / Airy, stato ∈ {noto, aperto, probabilmente falso}; ID `[R1-T#]`, `[R1-P#]`, `[R1-C#]`, `[R1-Q#]`.
- Almeno un controllo SymPy su un claim specializzato (Gram/coerenza gaussiane) con output citato.
- sources.bib con tutte le fonti citate; open_questions.md; tabella inviata a R4; `DONE R1`.
