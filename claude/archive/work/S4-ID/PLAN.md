# PLAN — S4-ID · identificazione relativa a un dizionario (Fase 4, punto 2 di G★′-NL)
Data 26/10/2026. Scheda: SESSIONS.md, Roster Fase 4, "S4-ID". Input letti per intero: SESSIONS.md, RIPRESA.md (ultimo AGGIORNAMENTO), PROTOCOLLO.md, NOTAZIONE.md (v3), PROBLEM.md (G★′-NL), GATE4A.md, research/DEVIL/ATTACK-4.md (O2, O3, O7, O10), research/CIT-AUDIT/AUDIT-4.md (§2.3–2.4), claims/LEDGER.md (righe C3, P4), research/F4-ALG/NOTE.md, research/F4-HOR/NOTE.md, research/F4-INT/NOTE.md, work/C3/PROOF_PACKAGE.md §1–6, work/P4/PROOF_PACKAGE.md §0–3. inbox/S4-ID.md: vuota all'apertura.

## Skill (caricate leggendo i SKILL.md; nessuno script _vendor eseguito)
1. skills-local/session-protocol (per primo): PLAN → PLAN-READY → inbox → consegna → DONE.
2. skills-local/claim-lifecycle: ogni enunciato passa bozza → SymPy → audit (S-CHECK, via CHECK_REQUEST) → kill-argument (cammino critico) → riga LEDGER proposta.
3. _vendor/Auto-claude-code-research-in-sleep/skills/proof-writer: per ogni claim enunciato, ipotesi, triage (PROVABLE AS STATED / AFTER WEAKENING / NOT JUSTIFIED), mappa delle dipendenze, prova a passi, rischi aperti.
4. _vendor/math-skill (modo proof): esplorazione separata dalla prova, controesempi prima della prova.
5. _vendor/scientific-agent-skills/skills/sympy: solo verifica, in work/S4-ID/sympy/, con `.venv\Scripts\python.exe -I`.
6. _vendor/Auto-claude-code-research-in-sleep/skills/novelty-check: fasi A, B (fonti già auditate da CIT-AUDIT-4), D; fase C (Codex) sostituita da revisore Claude fresco o omessa e dichiarata.
7. _vendor/Auto-claude-code-research-in-sleep/skills/kill-argument: thread di attacco e di aggiudicazione = due subagenti Claude freschi, senza il mio contesto (solo il testo dei claim); verdetto calcolato da me con la tabella della skill.

## Domande (con ID)
- **Q1 (compito 1, criterio esatto).** Per F = y_t − N (N ∈ ℂ[y₀,…,y_n]) e V ⊂ ℂ{y} sottospazio finito (dizionario 𝓓_{d,k}: monomi del getto di grado ≤ d e ordine ≤ k; dizionario evolutivo ℂy_t ⊕ A_{≤d,≤k}; dizionario di Hammerstein Σ R·y^j; dizionario dei flussi 𝓗_M), criterio necessario e sufficiente per I(u) ∩ V = ⟨F⟩, generalizzando C3-L1 (Gram) e C3-T1 (test "w ∉ EP" ↦ test "J_u ∩ ψ(V) = 0"). Casi: ALG-T1 (V = ℂ{y}, u analitica — DEVIL O10), MODREL-T1 (Syz_f(u)), INT-T1 (V = ℂy_t ⊕ span K_n), MON-1 (dizionario non polinomiale). Banchi: Burgers (N-shock), poi KdV (N-solitoni).
- **Q2 (compito 2, dicotomia).** Teorema "forma chiusa ⇒ non identifica" con definizione **sintattica** di forma chiusa (torre di estensioni elementari/Picard–Vessiot), in forma non tautologica (DEVIL O7): lemma di chiusura (trdeg finito), soglie esplicite per la classe EP-razionale (M1), esistenza di soluzioni identificanti, e controesempio al viceversa.
- **Q3 (compito 3, INT-Q1).** KdV, u(·,t) di Schwartz con r ≢ 0: può J_u ≠ 0? **Limite di tempo:** al più ~15% del budget della sessione e comunque chiuso prima di scrivere CHECK_REQUEST.md. Minimo consegnabile: riduzione a un enunciato classico nominato + risultato parziale (condizione necessaria) con dipendenze CON-FONTE dichiarate; altrimenti APERTO con la riduzione.
- **Q4 (compito 4, novità).** Delta esplicito rispetto a Scholl–Bacho–Boche–Kutyniok (Mach. Learn. 115 (2026) 139: Prop. 1, Tab. 1, Thm 1–2) e He–Zhao–Zhong (FoCM 24 (2024) 1595–1641), sulla base dell'AUDIT-4 (§2.3–2.4); nessuna nuova citazione non verificata.

## Predizione (registrata prima di iniziare, DEVIL-4 O6)
- P-a: il criterio esatto sarà una **riduzione** I(u) ∩ V ≅ ([F] ∩ V) ⊕ (J_u ∩ ψ(V)) tramite la forma normale ψ di ALG-L1, valida per u solo C^∞ (l'analiticità serve solo alla dicotomia trdeg): u identifica in V ⟺ J_u ∩ ψ(V) = 0 e [F] ∩ V = ⟨F⟩; la seconda condizione dipende solo dall'equazione e dal dizionario ed è **falsa** per 𝓓_{d,k} appena k ≥ ordine(F)+1 o d ≥ deg F + 1 (conseguenze differenziali): la domanda va posta come I(u) ∩ V = [F] ∩ V.
- P-b: per gli N-shock generici di Burgers, nel dizionario evolutivo ℂy_t ⊕ A_{≤d,≤k}: identificazione per k ≤ N−1 (ogni d); per k = N ⟺ d ≤ N (soglia N+1 di MODREL-P2 diventa esatta); per k > N atteso "⟺ d ≤ N" ma prevedo di non riuscire a dimostrarlo (V-ex). Probabilità che il criterio a k = N si dimostri: alta.
- P-c: KdV N-solitoni: relazione d'ordine ≤ N di grado basso (1-solitone: ordine 1, grado 3); prevedo solo risultati parziali/V-ex per N ≥ 2.
- P-d: dicotomia: dimostrabile come teorema con definizione sintattica; il viceversa è falso (soluzioni autosimili/onde viaggianti con profilo non elementare non identificano).
- P-e: INT-Q1 resta APERTO; prevedo una condizione necessaria condizionata all'asintotica di Deift–Zhou.
- P-f: novità ≤ 4/10, PROCEED WITH CAUTION: il delta è (i) la riduzione con il termine [F] ∩ V e il passaggio a tutti i dizionari (non solo forma normale u_t = F(g)), (ii) le soglie esatte per classi in forma chiusa.

## Criterio d'uscita (da SESSIONS.md, reso verificabile)
"Criterio esatto per Burgers e KdV con dizionari di grado ≤ d, oppure controesempio": FATTO quando (1) il teorema di riduzione (Q1) è scritto con prova completa e CHECK_REQUEST; (2) per Burgers è enunciato e provato il criterio esatto per gli N-shock almeno a ordine k ≤ N, con il resto marcato V-ex/APERTO; (3) per KdV il criterio di riduzione è applicato con almeno un risultato (positivo o negativo) per i solitoni; (4) dicotomia (Q2) con prova; (5) INT-Q1 chiusa entro il limite di tempo con uno degli esiti sopra; (6) delta di novità scritto. Minimo consegnabile se fallisce: teorema di riduzione + controesempio "[F] ∩ 𝓓 ≠ ⟨F⟩".

## Contatti
- S4-INTEG (inbox/S4-INTEG.md): INT-T1, ALG-L1/T1, MODREL-T1 sono lemmi suoi; li **uso** senza riprovarli (cito lo stato), e gli segnalo i punti che mi servono (u analitica in ALG-T1; lemma [F_B] ∩ (Ry ⊕ Ry²) = R·F_B che dimostro qui).
- S4-TERM (inbox/S4-TERM.md): stessa u (N-shock/solitoni) — gli comunico quali soluzioni identificano e in quali dizionari.
- S-CHECK: CHECK_REQUEST.md autosufficiente + DOMANDA in inbox/S-CHECK.md.
- central: PLAN-READY, TABELLA LEDGER, DONE S4-ID.

## Consegne
work/S4-ID/PLAN.md (questo), PROOF_PACKAGE.md (incrementale), CHECK_REQUEST.md, sympy/ (script + .out). Solo work/S4-ID/ e inbox/.
