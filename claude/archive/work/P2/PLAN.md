# PLAN — S-P2 (regolarizzazione) · Fase 3, terza ondata · 25/10/2026
Scheda: SESSIONS.md §S-P2. Prima esecuzione (cartella creata ora). Decisioni Gate 1: H0 = ℝ, H1 = H^m(Ω) con Ω limitato (rettangolo I×J salvo avviso), componente = fattore.
Item del piano: P2 (P2.1–P2.3), C1.3 (Riesz/angolo), C4; appunti A8, B5–B8, D1, Pg.C-C1, Pg.D-D1; G★′ punti 2 e 4 (PROBLEM.md).

## 1. Domande / enunciati (con ID)
- **Q-P2.1 (R1-T6 nel quadro Gate 1).** Il residuo limite di ogni regolarizzazione (Tikhonov generalizzato con R ≥ 0, ε-minimizzatori) è P_M^⊥u, M = chiusura dello span del dizionario in H^m(Ω). Due dizionari: (F) classi dei fattori 𝓗_j = ker_{H^m}Q_j; (T) classi dei termini dentro un fattore di evoluzione, D_n = ker_{H^m}(∂_t − a_n(∂_x)). → P2-T1.
- **Q-P2.2 (R1-T7 quantitativo e B8 per termini).** Stima dal basso dist(u,M) ≥ ‖Qu‖_{H^{m−k}}/C_Q per Q nell'intersezione degli ideali; per (T): E^⊥(u) = 0 ⟺ Π_n(a − a_n)(∂_x)u = 0, spazio EP di dimensione Σ_n deg(a − a_n) (analogo di R2-T3/G1); ODE: E^⊥ = 0 ⟺ lcm(L_n)u = 0. → P2-L1, P2-T2, P2-P2.
- **Q-P2.3 (R1-P8).** Il regolarizzatore agisce solo sull'ambiguità ker S = E^∥: principio di selezione (limite = rappresentazione R-minima, R convesso s.c.i. coercivo); in (F) su rettangolo l'ambiguità è 𝒩 (dim δ(P), EP; C12-T1); ℓ² = split di Aronszajn (C12-T5(c)). → P2-P3.
- **Q-P2.4 (R1-P9).** Encoder lineari limitati con inversa limitata conservano E^⊥ a meno di costanti; l'ipotesi "inversa limitata" è necessaria (controesempio con encoder compatto iniettivo che rende EM denso), al prezzo della stabilità. → P2-P4.
- **Q-P2.5 (stabilità ⟺ c_F; C12-T3, C12-P7, C12-P8).** Per due fattori: spettro di S*S su (ker S)^⊥ ⊂ [1−c_F, 1+c_F] ∪ {2} con inf = 1−c_F; ‖S^†‖ = (1−c_F)^{−1/2}; Tikhonov uniformemente stabile in α ⟺ c_F < 1; tasso α/(1−c_F+α); se c_F = 1 i coefficienti divergono sui dati della chiusura. Dicotomia per C12-C1 (m ≥ 1). → P2-T3, P2-C1.
- **Q-P2.6 (legame con P1-P1(e)).** Principio astratto: una mappa lineare illimitata (E^add per termini in H^m per AD) non ammette regolarizzazioni uniformemente lipschitziane convergenti puntualmente (lineari o no: ℓ¹ incluso). Contrasto: in 𝔅_ρ e su ℝ con dati L² la mappa è limitata con costante esplicita e_{≥2}(β). → P2-T4, P2-P5.
- **Q-P2.7 (RT-R1a, MCA).** Versione per sottospazi del teorema di Donoho–Kutyniok (errore ≤ 2δ/(1−2κ)) per i fattori, dove l'ambiguità è il gauge finito I = 𝓗_1∩𝓗_2; condizione esatta (NSP sul gauge) con basi ortonormali; calcolo di κ per una coppia della scala (τξ: κ = 0 con basi adattate, in ogni H^m); verdetto promozione/eliminazione. → P2-T5, P2-P7, VERDETTO in §8.
- **Q-P2.8 (C3-Q3, solo teoria).** Condizionamento della lettura dei termini via log-simbolo (Vandermonde): bound superiore di tipo Gautschi e inferiore h^{−d} per nodi a distanza h. → P2-P6. Hankel/Prony: APERTO dichiarato.

## 2. Skill (ordine d'uso, dichiarate)
1. `skills-local/session-protocol` — letta per intero per prima.
2. `skills-local/claim-lifecycle` — stati, righe LEDGER, nessun DIMOSTRATO senza audit.
3. `_vendor/math-skill/SKILL.md` (modo `proof`, + `references/proof-playbook.md`) — esplorazione separata dalla prova, controesempi prima (così P2-P4(b) e la condizione esatta di P2-T5(iii)).
4. `_vendor/Auto-claude-code-research-in-sleep/skills/proof-writer/SKILL.md` — triage PROVABLE AS STATED / AFTER WEAKENING / NOT JUSTIFIED per ogni claim R1 (R1-T6, T7, P8, P9) e struttura (ipotesi, strategia, dipendenze, prova, rischi).
5. `_vendor/scientific-agent-skills/skills/sympy/SKILL.md` — solo verifica, in `work/P2/sympy/` con `D:\ProblemaBase\.venv\Scripts\python.exe -I`.
6. proof-checker: NON eseguito da me (niente subagenti: non richiesti) — audit a S-CHECK tramite `work/P2/CHECK_REQUEST.md` autosufficiente + DOMANDA in inbox/S-CHECK.md. Passaggio avversariale inline (§9 del PROOF_PACKAGE) al posto del kill-argument (non sul cammino critico identificazione/fattori; tocca E_int solo come impossibilità).

## 3. Fonti
research/R1/REPORT.md (§2–3: T6, T7, P8, P9, tabella T-a…T-k, RT-R1a), work/C1C2/gram.md e PROOF_PACKAGE.md (C12-T1, L2, L3, T3, P4, P7, P8, T5, C1), work/P1/PROOF_PACKAGE.md (P1-D1–D3, L1–L3, T2, P1(e), P2(c)), work/C3/PROOF_PACKAGE.md (C3-Q3), claims/LEDGER.md. Letteratura solo citata (nessuna ricerca web): Donoho–Kutyniok 2013 CPAM (Prop. 2.1, verificata da R1 su arXiv:1004.3006), Engl–Hanke–Neubauer 1996 (Tikhonov), Deutsch 2001 (angoli), Gautschi 1962 (Vandermonde) — tutte le prove qui sono autosufficienti, le citazioni sono solo di contesto.

## 4. Contatti
- S-P1 (chiusa): RISPOSTA alla TABELLA in inbox/S-P1.md (risponde il coordinatore).
- S-P3 (in parallelo): TABELLA in inbox/S-P3.md (duali canonici solo se c_F < 1; stabilità; gauge).
- S-C1C2 (gram.md, sola lettura): AVVISO in inbox/S-C1C2.md con l'identità inf σ(S*S) = 1 − c_F e la dicotomia per C12-C1.
- S-CHECK: DOMANDA (audit). central: PLAN-READY, TABELLA LEDGER, DONE S-P2.

## 5. Criterio di "fatto"
Ogni enunciato R1-T6/T7/P8/P9 riformulato nel quadro Gate 1 con prova completa (o corretto con motivo); RT-R1a con verdetto motivato da un teorema e da un calcolo di κ; legame esplicito con c_F e con P1-P1(e); SymPy di verifica eseguito con output salvato; CHECK_REQUEST.md autosufficiente; righe LEDGER proposte; DONE S-P2. Stato onesto: "prova scritta, audit richiesto" finché S-CHECK non risponde.

## Ripresa — audit 4 (25/10/2026, rilancio breve)
Input: work/CHECK/AUDIT_P2.md (S-CHECK-4, 72/72, tutti PASS / PASS-con-fix MINOR; O-1 MAJOR di portata), RISPOSTA in inbox/S-P2.md, AVVISI di central, S-P1, S-P3; PROBLEM.md G★′ punto 2 con γ_N (approvato dall'utente); LEDGER (P2-* tutti DIMOSTRATO).
Skill: session-protocol (riletta per prima), claim-lifecycle (stati: DIMOSTRATO solo dove S-CHECK-4 ha dato PASS; il nuovo corollario per N ≥ 3 resta "prova scritta, audit richiesto"). SymPy solo verifica (work/P2/sympy/p2_ripresa4.py, .venv -I).
Azioni:
1. PROOF_PACKAGE: applicare i fix marcandoli [fix <id>]: T3-1, T3-2, L1-1, T2-1 (prova alternativa Q − g ∈ (τ−a)R), T2-2, T2-3, T4-1 (Φ qualsiasi: Lip(Φ) ≤ liminf L_α; ogni selezione esatta ha Lip ≥ ‖S^†‖), T5-1 (definizioni Λ_j, δ, μ_c, κ), T5-2, C1-1, P5-1 (P3-1 facoltativo: notazione).
2. O-1: nuovo **P2-C2** (corollario per N ≥ 3 con γ_N: chiusura ⟺ γ_N > 0, ‖S^†‖ = γ_N^{-1/2}, (c),(d) di T3 con γ_N; condizione sufficiente di Gershgorin γ_N ≥ 1 − ‖C‖; controesempio: c_F a coppie né necessari né sufficienti). Formula di γ_N in funzione dei soli c_F a coppie: impossibile (controesempio) → P2-Q2 riformulato.
3. Dipendenze P1-P2(c)/P1-L1 → scaricate (DIMOSTRATO, S-CHECK-3). Tabella stati §1 e righe §12 allineate al LEDGER.
4. inbox: AVVISO a central con riga LEDGER proposta per P2-C2 + DONE "S-P2 (ripresa audit)"; AVVISO a S-C1C2 (P2-C2 serve per C12-P7 con N ≥ 3).
Criterio di fatto: tutti i fix marcati nel testo; P2-C2 con prova; SymPy eseguito; DONE in central.
**Esito ripresa (26/10, dopo lo stop):** applicati T4-1, T5-1, T5-2, P5-1; P2-C2 completato (prova elementare, sezione [P2-C2] in §7); SymPy p2_c2.py 30/30; CHECK_REQUEST_2.md + DOMANDA a S-CHECK; AVVISO a S-C1C2; riga LEDGER e DONE in central.
