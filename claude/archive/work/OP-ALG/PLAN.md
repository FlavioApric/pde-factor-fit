# PLAN — OP-ALG · Problemi aperti algebrico-algoritmici sull'identificazione (chiusura Fasi 4–5)
Data 26/10/2026 · Agente OP-ALG · Scrive solo in work/OP-ALG/ e inbox/.
Input letti: RIPRESA.md (ultimi aggiornamenti), REPORT_FINALE.md §6, skills-local/session-protocol, skills-local/claim-lifecycle, NOTAZIONE.md (v1–v4), PROBLEM.md, claims/LEDGER.md (righe C3-Q1, P4-T5, P4-Q-min), work/C3/PROOF_PACKAGE.md (C3-L2, L3, T1, T3, T6, P1, Q1, Q2), work/P4/PROOF_PACKAGE.md (P4-T2, T4, T5, T6, L3–L7, C4, Q1, Q-min), work/S4-ID/PROOF_PACKAGE.md (S4ID-T1).
Skill caricate (lettura dei SKILL.md, nessuno script _vendor eseguito): session-protocol, claim-lifecycle, proof-writer (struttura: enunciato, ipotesi, triage, dipendenze, prova a passi, rischi), math-skill (modo proof: controesempi prima), sympy (solo controllo, aritmetica esatta), research-lit (sole fonti web, via WebSearch).

## Problemi, predizioni, criteri d'uscita
| # | problema | predizione (registrata prima della prova) | criterio d'uscita |
|---|---|---|---|
| 1 | **C3-Q1** decidibilità di Ann(u) = (P) / test EP per u olonoma (M3) | **Decidibile** per u reale-analitica su Ω connesso con un ideale olonomo I ⊆ Ann_{A_2}(u) e getti calcolabili in p₀, **per ogni P** (anche non monico, senza dati di Cauchy D-finiti). Via: eliminanti di Bernstein in K[t,x]⟨∂_t⟩ e K[t,x]⟨∂_x⟩ (conteggio di dimensioni) ⇒ (a) test di zero con polinomio indiciale "a parametro"; (b) esponenti e gradi della parte EP confinati in un insieme finito calcolabile ⇒ test EP = due test di zero. Ostruzioni residue: scatola nera (P4-T5), u non analitica (P4-C4(a)): fuori modello. | teorema con prova completa + controllo SymPy su ≥ 3 esempi (incluso P non monico di P4-C4(b)); oppure ostruzione precisa |
| 2 | **P4-Q-min** minimalità del maggiorante B | **B non è minimale** per la decisione: il dato minimo è il bit χ, equivalente (per riduzione a oracoli) al maggiorante D del grado di un testimone. **B ≡ G_u** (equivalente al dato "operatore intrinseco"). B strettamente più forte di χ ⟺ P non irriducibile ridotto (Σe_i ≥ 2), via avversario alla P4-T5; per P irriducibile ridotto B ≡ χ. | definizione formale dell'ordine dei dati + teorema con prova; avversario verificato in SymPy |
| 3 | **C3-Q2** analogo di C3-T1 in A_2 / 𝒟 = A_1[∂_t] | Criterio corretto (forma "saturata"): Ann(u) = 𝔇P ⟺ il t-getto (u,…,∂_t^{m−1}u) è libero sull'anello dei coefficienti 𝔄 ⟺ nessun Q ∉ 𝔇P con Qu di 𝔄-torsione. **La riduzione a un numero finito di test (struttura I = G·J) è falsa**: controesempio con fattori commutanti e comassimali ma simili, P = (∂_t − θ)(∂_t − θ + 1), θ = x∂_x: famiglia continua di ideali saturati a due a due intersecati in 𝔇P. In A_2 intero: per u olonoma Ann(u) ≠ A_2P sempre. | teorema + controesempio con prova; identità verificate in SymPy |
| 4 | **INT-18** G★′ punto 1 per P non ridotto | Testo corretto: oggetto = G_u = gcd Ann(u) (C3-T6); Ann(u) = (P) ⟺ G_u ∼ P (dato P(∂)u = 0) ⟺ (P/P_i)(∂)u ∉ EP ∀i; V(Ann u) vede solo il radicale; con i risultati 1–2 lo stato di "verificabile". | proposta di testo + esempi SymPy |

## Ordine e metodo
1. Ricerca bibliografica (research-lit, solo web): zero recognition di funzioni olonome (Takayama), soluzioni polinomiali/razionali di sistemi olonomi (Oaku–Takayama–Tsai), approccio olonomo (Zeilberger, Chyzak). Scopo: collocare il risultato 1 e non rivendicare ciò che è noto.
2. Prove scritte (proof-writer) in PROOF_PACKAGE.md, incrementale, nell'ordine 1, 2, 3, 4.
3. SymPy in work/OP-ALG/sympy/ (python -I della .venv; nessun kill di processi altrui).
4. CHECK_REQUEST.md autosufficiente (enunciati, ipotesi, prove, dipendenze esterne con stato).
5. TABELLA LEDGER e DONE OP-ALG in inbox/central.md.
Stati: tutto ciò che è nuovo è PROVA SCRITTA (nessun audit esterno in questa sessione; kill-argument non eseguito: niente sotto-agenti richiesti).
