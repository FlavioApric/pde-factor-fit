# PLAN — OP-F5C · INT-Q1 (dati analitici) e OP-K15 / δ_N(K)
Data 26/10/2026 · Cartella work/OP-F5C/ · scrittura solo qui e in inbox/.
**Skill caricate (lettura SKILL.md, nessuno script _vendor eseguito):** skills-local/session-protocol, skills-local/claim-lifecycle, _vendor/.../proof-writer (enunciato, triage, prova), _vendor/math-skill (controesempi prima), _vendor/scientific-agent-skills/skills/sympy (controllo).
**Input letti:** REPORT_FINALE §4.3, §6.2; LEDGER (righe S4ID-T3, OP-*, OPR2-*); NOTAZIONE v4; work/OP-NL, work/OP-R2, work/S4-ID PROOF_PACKAGE; AUDIT_OP-NL/OP-R2/S4-ID.

## Problema 2 — OP-K15 (priorità: sembra chiudibile)
Strategia (nuova, predizione registrata prima del calcolo): coordinate di Mumford/Novikov.
1. (Nov) ⇒ i getti d'ordine ≤ 2N−1 dell'N-solitone giacciono su M_k = {(U,V): U | V² − R_k}, R_k = −λG_∞(λ)², tramite il cambio triangolare pesato getti ↔ coefficienti di (U, V) = (G, G′/2) (Gelfand–Dickey).
2. M_k irriducibile di dim N (stratificazione per molteplicità delle radici di U) e ridotto ⇒ M_k = chiusura dei getti dei solitoni.
3. Bezout pesato: le proiezioni sui getti (y_0..y_{N−1}) e (y_1..y_N) sono finite ("regolari all'infinito") di grado Π(pesi eq.)/Π(pesi incognite) = 2^N e (N+2)2^{N−1}.
4. Polinomio caratteristico ⇒ Π_N monico in y_N, W_N = (N+2)2^N, deg_{y_N}Π_N = 2^N; deg Π_N = (N+2)2^{N−1} ⟺ condizione (★)_N (nessun punto del livello razionale con y_1 = … = y_N = 0, y_0 ≠ 0).
5. (★)_N: prova generale se possibile; altrimenti certificato esatto (Gröbner su ℚ) per N ≤ N_max.
δ_N(K), N < K < 2N: tentare lo stesso metodo (proiezioni su y_0..y_K: fibre ⇒ grado minimo); almeno limiti superiori/inferiori dimostrati.
Predizione: il punto 3 per (y_0..y_{N−1}) è elementare; (★) è la parte dura.

## Problema 1 — INT-Q1 (dati analitici)
1. Riduzione strutturale: J_u ≠ 0 ⇒ J_u = [p]:s_p^∞, p irriducibile d'ordine K ≥ 2, e D_F p ∈ J_u (vincolo differenziale compatibile = varietà invariante K-dimensionale).
2. Ostruzione locale-analitica: ogni soluzione analitica non viaggiante soddisfa localmente un'EDO analitica autonoma compatibile d'ordine 2 ⇒ una prova deve usare l'algebricità/globalità di p.
3. Corollari condizionali (H-as con derivate): ordine minimo ≥ 3.
4. Tentativi: trascendenza differenziale via asintotica x → ±∞, Galois differenziale; esito onesto.

## Contatti
inbox/central.md (PLAN-READY, righe LEDGER proposte, DONE). Revisore: subagente indipendente via CHECK_REQUEST.md (lanciato dal coordinatore).

## Criterio di "fatto"
PROOF_PACKAGE.md (ID OPF5C-*), CHECK_REQUEST.md, script in sympy/ con esiti, righe LEDGER proposte, DONE OP-F5C.
