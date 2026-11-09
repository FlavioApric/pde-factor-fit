# PLAN — S-C1C2 (coppia S-C1 ⇔ S-C2/C4) · Fase 3, prima ondata · 25/10/2026
Scheda: SESSIONS.md §"S-C1 ⇔ S-C2/C4". Vincoli Gate 1 (PROBLEM.md v2, NOTAZIONE v2): H0 = ℝ, H1 = H^m(Ω) con Ω = I×J ⊂ ℝ_t×ℝ_x rettangolo aperto limitato (o convesso limitato), componente = fattore. R = ℂ[τ,ξ], ∂_t ↔ τ, ∂_x ↔ ξ.
Cartella work/C1C2 vuota all'avvio (solo sympy/): nessun lavoro da riprendere. Inbox: 1 AVVISO+DOMANDA da S-TROP (lato stazionario e^{cx/D}).

## 1. Enunciati da affrontare (ID provvisori [C12-…]; appunti A5, A7, A8, C1.0–C1.4, C4.1–C4.4; item C1, C2, C4; G★′ punto 2)
Parte C2/C4 — scomposizione per fattori
- [C12-L1] Lemmi 1D su rettangoli: ker ∂_x su 𝒟′(I×J) = 𝒟′(I)⊗1, primitiva in x che commuta con ∂_t; lemma di Poincaré distribuzionale sul rettangolo.
- [C12-L2] Moduli di dimensione finita: Hom_R(M,𝒜) ha dimensione dim_ℂ M ed Ext¹_R(M,𝒜) = 0 (𝒜 = 𝒟′(Ω), C^∞(Ω)); soluzioni = esponenziali-polinomi (Koszul + Poincaré, prova autonoma, senza il principio fondamentale).
- [C12-L3] f, g coprimi ⇒ R/(f,g) di dimensione finita (risultanti), additività dim R/(f,gh) = dim R/(f,g) + dim R/(f,h).
- [C12-T1] Teorema di scomposizione per fattori in 𝒟′(Ω) e C^∞(Ω): ker P = Σ_j ker Q_j (Q_j = P_j^{m_j}); nucleo della mappa somma di dimensione δ(P) = Σ_{i<j} dim R/(Q_i,Q_j), fatto di esponenziali-polinomi; unicità ⟺ V(Q_i)∩V(Q_j) = ∅. Su convesso generale: CON-FONTE (de Rham / Malgrange–Ehrenpreis).
- [C12-P1] Proiettori costruttivi: Q_2u ∈ ker Q_1; caso comassimale: idempotenti polinomiali (resto cinese), perdita di derivate esplicita; caso generale: formula del risultante r(∂_x)u_1 = b(∂)Q_2u.
- [C12-T2] Formula di Vandermonde per P = Π(τ − a_j(ξ)): Δ(∂_x)u_j = Σ_l adj V(∂_x)_{jl} ∂_t^l u, δ(P) = deg Δ = Σ_{i<j} deg(a_i−a_j) (ponte con S-II: proiettori spettrali della compagna = V^{-1}).
- [C12-P2] Criterio per il 2° ordine in t: τ² + bτ + c riducibile ⟺ b²−4c quadrato in ℂ[ξ] (onda, trave sì; KG, telegrafo no).
- [C12-P3] G8 / O1: τ − a(ξ) è irriducibile ⇒ lo strato fattori è banale per le evoluzioni del 1° ordine.
- [C12-C1] Controesempio: la scomposizione NON conserva H^m(Ω) globalmente (coppia di trasporti paralleli, angolo del rettangolo), anche quando è unica; perdita = 1 derivata, ottimale.
- [C12-T3] Criterio esatto per coppie di trasporti paralleli su convesso limitato (m = 0): scomposizione L² globale ⟺ corde caratteristiche di lunghezza inf > 0 ⟺ coseno di Friedrichs < 1.
- [C12-P4] Onda sul quadrato: scomposizione globale in H^m, c_F < 1; ∂_t∂_x sul rettangolo: c_F = 0.
- [C12-L4]/[C12-T4] Regolarità interna: componenti in H^{m−λ}_loc(Ω) con λ esplicito (coppia quasi-ellittica r(∂_x), s(∂_t)).
- [C12-P5] Coefficienti polinomiali (L4, ODE in x): ker LCLM = ker L_1 + ker L_2 su intervalli senza zeri dei coefficienti di testa; il prodotto non basta (R2-C2).
Parte C1 — funtore C1.0
- [C12-D2]/[C12-T5] Funtore C1.0 su Ω limitato: fattore Q ↦ 𝓗_Q = ker_{H^m(Ω)} Q (chiuso; RKHS per m ≥ 2 con nucleo = proiezione del nucleo di H^m = Green dell'operatore d'energia), 𝓗_𝒟 = Σ 𝓗_Q con norma di Aronszajn; equivalenza delle norme ⟺ somma chiusa ⟺ c_F < 1; scomposizione H^m globale ⟺ somma chiusa e densa.
- [C12-T6] Analoghi di Rosenbloom–Widder per ogni fattore τ − a(ξ), deg a = q ≥ 1: base di Appell v_n = e^{t a(∂_x)}x^n, stima |v_n| ≤ (n!)^{1−1/q}K^n, spazio di Hilbert di Fock pesato con base ortogonale {v_n} e duale biortogonale (coefficienti di Taylor); per q = 2 si ritrova R1-P11.
- [C12-P6] No-go: base di Appell ortogonale in L²(peso) su una sezione temporale solo per q = 2 (Shohat) — CON-FONTE.
Fuori piano: identificabilità (S-C3), E_int per quadro (S-P1), struttura della compagna (S-II), Newton/regimi di scala (S-TROP).

## 2. Skill (ordine d'uso, caricate leggendo i SKILL.md; nessuno script _vendor eseguito)
1. skills-local/session-protocol (letta per prima, per intero).
2. skills-local/kernel-catalog-entry (template delle schede di CATALOGO_v2, Gram, verifiche T e = 0).
3. skills-local/claim-lifecycle (ciclo di ogni enunciato e righe del LEDGER).
4. _vendor/Auto-claude-code-research-in-sleep/skills/proof-writer (struttura: claim, stato, assunzioni, strategia, mappa delle dipendenze, prova, rischi).
5. _vendor/math-skill (modo proof/solver + references/proof-playbook.md: cercare controesempi prima di provare).
6. _vendor/scientific-agent-skills/skills/sympy (script in work/C1C2/sympy/, `D:\ProblemaBase\.venv\Scripts\python.exe -I`).
7. Secondo revisore: S-CHECK (DOMANDA in inbox/S-CHECK.md con solo enunciato + ipotesi + prova di C12-T1/L2, C12-C1, C12-T3, C12-T2). kill-argument: non richiesto dalla scheda; passaggio avversariale inline sul cammino critico (C12-T1) dichiarato nel PROOF_PACKAGE.

## 3. Fonti
research/R2 (T1, T2, T4, C1, C2), R1 (T1, P1, P4, P11), R3 (K1–K14), PR-C2d §3 (Green = nucleo riproducente), SYNTHESIS §2. Classici: Fulton *Algebraic Curves* (cap. 1–3, Bézout cap. 5); Weibel *Introduction to Homological Algebra* (cap. 2–4: Ext, Koszul); de Rham *Variétés différentiables* (coomologia delle correnti); Hörmander ALPDO I/II (principio fondamentale); Aronszajn 1950; Deutsch *Best Approximation in Inner Product Spaces* (somma chiusa ⟺ angolo di Friedrichs); Ore 1933; Rosenbloom–Widder 1959; Shohat 1936 (Appell ortogonali).

## 4. Contatti
- S-C3: TABELLA (scomposizione su rettangolo e lemma EP = esponenziali-polinomi delle intersezioni) + DOMANDA (forma di Z(u) per le componenti).
- S-II: TABELLA (formula di Vandermonde/adjugata = proiettori spettrali con denominatore Δ) + DOMANDA (coerenza con II-T2/II-T3).
- S-TROP: RISPOSTA alla DOMANDA (esponenziali reali inclusi; lato stazionario = sotto-equazione, scheda nel CATALOGO_v2).
- S-P1: AVVISO (E_int^ker per fattore = 0 su 𝒟′, ma ≠ 0 in H^m globale: C12-C1).
- S-CHECK: DOMANDA (audit).
- central: PLAN-READY, righe LEDGER, DONE.
File condiviso: work/C1C2/gram.md.

## 5. Criterio di "fatto" (scheda)
Teorema di scomposizione su Ω ⊂ ℝ limitato scritto con prova completa (𝒟′, C^∞, e risposta esatta per H^m: controesempio + criterio + regolarità interna), inviato a S-CHECK; funtore C1.0 dimostrato per i casi ★ (calore, trasporto, onda, trave, avvezione–diffusione); SymPy su calore, trave, onda, avvezione–diffusione; CATALOGO_v2 e gram.md scritti; righe LEDGER proposte; DONE S-C1C2. Stato onesto: DIMOSTRATO solo dopo l'esito di S-CHECK, altrimenti "prova scritta, audit in attesa".

## Ripresa 25/10 sera (S-C1C2, chiusura)
Stato trovato: PROOF_PACKAGE.md completo (non si riscrive); 4 script SymPy PASS (factors 48, counterexample 24, appell 65, gram 8). Inbox: AVVISO+DOMANDA S-TROP, AVVISO S-C3, TABELLA+DOMANDA S-II. Mancano solo i passi seguenti, in quest'ordine:
1. sympy/c12_catalog.py (verifiche T e = 0 per le basi delle schede ★ + lato stazionario di AD + Gram in forma chiusa) → .out.
2. CATALOGO_v2.md: schede kernel-catalog-entry per calore, trasporto, onda, trave, AD, più la sotto-scheda "AD lato stazionario cξ − Dξ²" (classe = ker P ∩ ker ∂_t = Sol(R/(P,τ)) = span{1, e^{cx/D}}).
3. gram.md: Gram / c_F per le coppie di fattori dei casi ★ (da C12-T3, P4, P7, c12_gram.out, c12_catalog.out).
4. RISPOSTE: S-TROP (sì, esponenziali reali inclusi), S-II (proiettore con denominatore: C12-P1(c) = II-T2(d); esistenza da C12-T1, non da Malgrange), S-C3 (concordanza: ambiguità EP = C12-T1(ii) ≡ C3-L3); AVVISO a S-P1 (E_int^ker per fattore = 0 su D′, ≠ 0 in H^m globale, C12-C1).
5. CHECK_REQUEST.md autosufficiente (C12-L1, L2, L3, T1; poi C1, T3, T2) + DOMANDA in inbox/S-CHECK.md.
6. Righe LEDGER (§12) come TABELLA in inbox/central.md, stato "prova scritta, audit in attesa"; poi DONE S-C1C2.
Skill per questa ripresa: session-protocol (riletta per prima), kernel-catalog-entry (template schede), claim-lifecycle (righe LEDGER, audit), sympy (nuovo script). proof-writer e math-skill già applicate nel PROOF_PACKAGE: non rilette.

## Ripresa 2 — audit 2C (25/10/2026, S-C1C2)
Input letti: RIPRESA.md (ultimo AGGIORNAMENTO: DONE S-CHECK-2C, rilancio di S-C1C2 per fix 2C + II-T2-F1 + C12-T1′ + kill-argument), inbox/S-C1C2.md (RISPOSTA S-CHECK-2C, AVVISO central su II-T2-F1), work/CHECK/AUDIT_C12-T1.md, AUDIT_C12-altri.md, claims/LEDGER.md (righe C12-*).
Skill (in ordine d'uso, lette per intero o nelle parti operative; nessuno script _vendor): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-writer (triage + struttura di C12-T1′), math-skill modo `proof` (esplorazione/controesempi separata dalla prova), sympy (script c12_t1prime.py), kill-argument (protocollo attacco → arbitrato; revisori = 2 subagenti Claude freschi senza contesto, al posto di Codex, su istruzione del coordinatore).
Passi:
1. **Esplorazione C12-T1′ (prima della prova).** Domanda: che ipotesi topologica serve davvero? Candidati: (a) H¹_dR(Ω)=0 sufficiente (schizzo O-2); (b) necessità: cercare controesempi su Ω connesso non semplicemente connesso con buchi "sottili" (disco bucato, dove la costruzione O-1 con α′β′ nel buco non è disponibile), separando 𝒟′ e C^∞; (c) verificare su un Ω semplicemente connesso NON convesso (disco tagliato, dominio a U) che la scomposizione esiste davvero. SymPy: work/C1C2/sympy/c12_t1prime.py → .out.
2. **Fix 2C nel PROOF_PACKAGE**, marcati [fix <id>]: L3-1, L3-2, L1-1, L1-2, L2-1, L2-2, T1-1 (ipotesi rettangolo essenziale + O-1), L5-1, T3-1, T2-1, T2-2; II-T2-F1 (solo T2(iv): Π_j nei punti di collisione; C12-P1(c) non valuta Π_j in punti, va solo dichiarato).
3. **C12-T1′**: enunciato, prova (riduzione del caso 𝒟′ al caso C^∞ con partizione dell'unità e L1 sui quadrati; L2′ per dimensione), proposizione di necessità (C12-P10), nuova sezione nel PROOF_PACKAGE; aggiornare tabella §2, §11, §12; nuova §13 "Esito S-CHECK-2C".
4. **Kill-argument formale su C12-T1**: subagente A (attacco, ~200 parole, solo PROOF_PACKAGE + PROBLEM.md, divieto di leggere audit/inbox/LEDGER), poi subagente B (arbitrato per punti con il memo verbatim). Verdetto calcolato da me con la tabella della skill. Esito in PROOF_PACKAGE §11.
5. Se la prova di T1′ è completa: work/C1C2/CHECK_REQUEST_2.md autosufficiente + DOMANDA in inbox/S-CHECK.md.
6. TABELLA righe LEDGER aggiornate + "DONE S-C1C2 (ripresa 2)" in inbox/central.md.
Criterio di fatto: tutti i fix recepiti e marcati; T1′ provato o confutato con stato onesto ("prova scritta, audit in attesa"); kill-argument registrato con verdetto; richieste inviate.

## Ripresa 3 — solo recepimenti (25/10/2026, S-C1C2)
Input letti: RIPRESA.md (ultimo AGGIORNAMENTO: DONE S-CHECK-5, lancio dei recepimenti), skills-local/session-protocol (per prima), skills-local/claim-lifecycle, questo PLAN, PROOF_PACKAGE.md, gram.md, inbox/S-C1C2.md (non ancora recepiti: RISPOSTA S-CHECK-3B; AVVISO central su CIT-AUDIT-2; AVVISO S-P2; AVVISO central su γ_N), work/CHECK/AUDIT_C12-T1prime.md, work/CHECK/AUDIT_P2.md (O-1, red team 3, fix T3-1), research/CIT-AUDIT/AUDIT-2.md e AUDIT-3.md (+ AVVISI suggeriti da CIT-AUDIT-3 in inbox/central.md), PROBLEM.md (G★′ punto 2 riformulato e approvato), claims/LEDGER.md (righe C12-*, P2-T3).
Skill: session-protocol (per prima), claim-lifecycle (stati: nessuno sale senza il controllo corrispondente; righe LEDGER proposte in central), sympy (solo un controllo numerico del controesempio N = 3, `sympy/c12_gammaN.py`). Nessuno script _vendor; nessuna nuova prova sostanziale (solo la riformulazione di C12-P7 con γ_N, la cui prova è il teorema della mappa aperta + P2-T3).
Passi (marcati [fix <id>] nel PROOF_PACKAGE):
1. Fix MINOR S-CHECK-3B: L1p-1 ("Ω connesso non vuoto" in L1′(d′), L2′, T1′), L1p-2 (Hörmander §1.4 e Lee cap. 11 senza numeri; forme complesse: parte reale e immaginaria), P10-1 (P10 con premessa sull'indice = DIMOSTRATO; equivalenza con "non s.c." CON-FONTE Rudin RCA cap. 13, numero 13.11 non verificato; direzioni separate nella Conseguenza), P10-2 (η_ε = ω_ε vicino a γ; η_ε → η uniformemente su γ), P10-3 (riduzione: ω_ε + dθ_α/2π chiusa con periodo nullo ⇒ esatta; rinvio Lee cap. 17), T1p-1 (facoltativo: (i) senza connessione, (ii) con; H¹_dR=0 necessaria per ogni P, non per P fissato).
2. C12-P7 e gram.md: N ≥ 3 fattori, criterio γ_N := inf σ(S*S|(ker S)^⊥) > 0; c_F < 1 solo per N = 2 (P2-T3, "⇒" ora DIMOSTRATO); controesempio di AUDIT_P2 O-1; condizione "chiusa E densa"; densità per m = 0 nei trasporti paralleli (P2-C1(a)).
3. Citazioni CIT-AUDIT-2/3: Fulton §1.6 Prop. 2; Weibel Thm 2.7.6 (+ §4.5 senza numero); Shohat 1936 verificato (C12-P6, CATALOGO_v2); Deutsch survey 1995 (NATO ASI C 454, 107–130) al posto di "Thm 9.35"; Hörmander ALPDO I §1.4 e §2.2; Lee ISM 2ª ed. cap. 11 (chiuso/esatto) e cap. 17 (de Rham); CLO cap. 3 §§5–6. Nessun numero non verificato affermato.
4. §9.1 allineata al testo di PROBLEM.md G★′ punto 2; tabella §2 allineata al LEDGER; nuova §14 "Esito S-CHECK-3B / S-CHECK-4 / CIT-AUDIT e recepimento".
5. Righe LEDGER aggiornate come TABELLA in inbox/central.md, poi "DONE S-C1C2 (ripresa 3)".
Criterio di fatto: tutti i fix elencati presenti e marcati; nessuno stato più alto di quello registrato nel LEDGER; DONE in central.
