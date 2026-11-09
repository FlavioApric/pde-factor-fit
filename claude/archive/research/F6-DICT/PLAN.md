# PLAN — F6-DICT (hub) · dizionario universale filtrato 𝓓_∞, teorema negativo N1, certificato di misfit, migliore approssimazione, regole di arricchimento
Data 26/10/2026. Scheda: FASE6_SCOUTING.md (riga F6-DICT, temi R12 + R14, P-D: D1–D4). Vincolo dell'utente: **niente ML** (solo teoria analitica; i lavori ML compaiono solo come prior art).
Input letti: FASE6_SCOUTING.md, PIANO_FASI_6-11.md, PROTOCOLLO.md, PROBLEM.md (G★′, G★′-NL, precisazioni S5-INT), NOTAZIONE.md (v3), claims/LEDGER.md (C3-T1, C3-P1[M2]/[gen], C3-T6, P4-T2, P4-T5, P4-L7, R5-T2, C12-T1′, P1-T2/T3), research/F4-ALG/VERDETTO.md, work/S4-ID/PLAN.md (P-a: I(u) ∩ V = [F] ∩ V), work/C3/PROOF_PACKAGE.md §5 (C3-P1, C3-P2). inbox/F6-DICT.md: solo AVVIO. AVVISO del coordinatore: PLAN-READY/TABELLA/DONE in `inbox/central-F6.md` (non in central.md).

## Skill caricate (dichiarazione)
1. `skills-local/session-protocol` (letto per intero, seguito: PLAN → PLAN-READY → inbox → consegna → DONE).
2. `skills-local/route-scout` (letto: triage, criteri fissati prima, verdetto PROMUOVI/PARCHEGGIA/ELIMINA).
3. `skills-local/claim-lifecycle` (letto: stati onesti; qui solo "candidato"/"prova scritta", nessun DIMOSTRATO; righe LEDGER proposte, non scritte).
4. `_vendor/Auto-claude-code-research-in-sleep/skills/novelty-check/SKILL.md` (letto: fasi A, B con WebSearch; fase C "Codex" non disponibile → omessa e dichiarata, revisore esterno escluso).
5. `_vendor/math-skill/SKILL.md` modo `proof` (letto: esplorazione separata dalla prova, controesempi prima).
6. SymPy solo come verifica: `research/F6-DICT/sympy/*.py` con `.venv\Scripts\python.exe -I`. Nessuno script `_vendor` eseguito.
(`anthropic-skills:deep-research` non invocata: la ricerca bibliografica è mirata a fonti note, fatta con WebSearch/WebFetch e marcata "verificata"/"da verificare".)

## Domande (con ID)
- **D1-U1** locali lineari: enunciato esatto di Peetre (ipotesi: linearità, supp Tu ⊆ supp u, nessuna continuità; tesi: ordine localmente finito, coeff. C^∞) → dizionario 𝓓^{lin}_n = {x^β∂^α}, densità in quale topologia τ₁; coeff. polinomiali, analitici, lisci, singolari (fuori dal quadro C^∞: cosa resta).
- **D1-U2** locali non lineari: enunciato esatto di Slovák (Kolář–Michor–Slovák, numero del teorema; Navarro–Sancho) — finitezza dell'ordine solo locale anche nella direzione del getto → polinomi nel getto, Stone–Weierstrass sui compatti di J^k; sin u, e^u.
- **D1-U3** non locali lineari: nuclei di Schwartz (Hörmander ALPDO I Thm 5.2.1), invarianza per traslazioni → convoluzione/moltiplicatori; classi S^m (separabilità! densità con perdita ε di ordine), |ξ|^s, razionali, log; memoria (nuclei completamente monotoni → somme di esponenziali → sistema locale aumentato) e ritardo.
- **D1-U4** sistemi: Mat_k, gauge (rinvio a F6-SYS).
- **D1-U5** (aggiunta motivata: è la forma "per tutto") operatori continui qualsiasi C^∞(Ω) → C^∞(Ω): polinomi di Fréchet/Volterra su compatti (Fréchet 1910, Prenter 1970; Boyd–Chua 1985 per memoria evanescente).
- **N1** teorema negativo: (i) Baire: rappresentazione esatta in span 𝓓_∞ magra in ogni classe di Fréchet infinito-dimensionale; (ii) nessun dato finito certifica l'identificazione (C3-P1, P4-T5); (iii) non monotonia in n per soluzioni EP/forma chiusa; (iv) uscita finita ⇒ al più numerabili operatori ⇒ identificazione solo nel limite. Confine vero/falso esplicito.
- **D2** certificato di misfit: Hahn–Banach (formula della distanza), Gram (λ_min > 0, rapporto di determinanti), forma debole con funzioni test (niente derivate di u), versione con coefficienti limitati (min–max) e con coni (Farkas); asimmetria Σ₁/Π₁ (misfit finitamente certificabile, fit no).
- **D3** migliore approssimazione con stima: proiezione/equazioni normali, stima a posteriori dell'errore sui coefficienti (residuo/√λ_min), velocità (Jackson, Bernstein, n-larghezze di Kolmogorov: ottimalità d'ordine del dizionario polinomiale).
- **D4** regole di arricchimento: funzione di altezza, livello minimo con nucleo + controllo delle conseguenze (S4-ID P-a), arricchimento guidato dal residuo per famiglie di atomi, arresto (principio di discrepanza, Lepskii).
- **CONV** legame con F6-CONV: teorema candidato "identificazione nel limite" (lemma di Tikhonov su compatti, modulo di stabilità, rumore).
- **ISE** domanda guida comune (I/S/E) e **NOV** novelty-check.

## Criteri fissati PRIMA della ricerca (per sotto-strada U1, U2, U3, U4, U5, N1, D2, D3, D4)
- **PROMUOVI** se: (P1) esiste un enunciato candidato con ipotesi esplicite, topologia esplicita e prova scritta (o riduzione a un teorema pubblicato con riferimento verificato: DOI/numero di teorema); (P2) serve G★″ (identificazione, misfit o convergenza) ed è analitico; (P3) novità ≥ "delta verificabile" (anche se gli ingredienti sono classici, l'assemblaggio con certificato/livello/limite non deve essere già pubblicato in forma identica) OPPURE è un lemma di confine necessario (teorema negativo).
- **PARCHEGGIA** se: enunciato vero ma (a) solo con riferimenti "da verificare" sul cammino critico, oppure (b) la topologia in cui vale è troppo debole per dare stime (densità senza velocità né stabilità), oppure (c) novità nulla ma utile come lemma citabile.
- **ELIMINA** se: l'enunciato universale desiderato è falso (controesempio) e nessuna variante più debole serve G★″; oppure richiede ML.
- Regola di onestà: un enunciato "universale" senza topologia dichiarata o senza il teorema negativo che ne marca il confine non può essere PROMOSSO.

## Predizioni (registrate prima di iniziare)
- U1, U2, U3, U5 veri in topologie di convergenza su compatti / perdita ε di ordine; S^m NON separabile alla stessa ordine (teorema negativo N2, atteso dimostrabile con blocchi diadici).
- N1 vero in tutte e quattro le forme; il confine: "approssimazione + certificato + limite" sì, "identificazione esatta universale da una soluzione" no.
- Novità: bassa per U1–U5 (ingredienti classici; Chen–Chen 1995, Boyd–Chua 1985 coprono U5); delta atteso in N1 come teorema di confine organizzato, nel certificato debole e nella stima a posteriori con λ_min, nel teorema I-LIM. Novelty ≈ 3–5/10.

## Fonti previste
Peetre, Math. Scand. 7 (1959) e 8 (1960); Slovák, Ann. Global Anal. Geom. 6 (1988); Kolář–Michor–Slovák 1993 §19; Navarro–Sancho arXiv:1411.7499; Hörmander ALPDO I (Thm 5.2.1; cap. 4 convoluzione), III (cap. 18 simboli); Treves TVS (polinomi densi in C^∞); Pinkus "n-Widths in Approximation Theory"; Beylkin–Monzón (somme di esponenziali); Bernstein (funzioni completamente monotone); Fréchet 1910, Prenter 1970, Boyd–Chua 1985, Chen–Chen 1995; Zhang–Schaeffer 2019 (SINDy); He–Zhao–Zhong FoCM 2024; Scholl et al. 2026; Mathé–Pereverzev 2003 (Lepskii); Engel–Nagel (Trotter–Kato).

## Contatti (hub)
F6-CONV (filtrazione ↔ consistenza: TABELLA con I-LIM e la regola di arresto; DOMANDA sulle ipotesi di stabilità), F6-SYS (U4 matrici e gauge: TABELLA), F6-VAR (coeff. variabili/singolari: DOMANDA sugli atomi singolari e sul dizionario olonomo), central-F6 (PLAN-READY, TABELLA, DONE).

## Criterio di "fatto"
PLAN, VERDETTO (1–2 pp.), NOTE (prove), sources.bib, open_questions.md, sympy/ con .out; inbox letta 3 volte; messaggi ai contatti; `DONE F6-DICT` in inbox/central-F6.md.
