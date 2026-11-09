# PLAN — S-P3 (duali e perturbazioni) · Fase 3, terza ondata · 25/10/2026
Scheda: SESSIONS.md §S-P3. Gate 1: H0 = ℝ, H1 = H^m(Ω) con Ω limitato (rettangolo dove serve C12-T1), componente = fattore (G★′). Item: P3 (P3.1–P3.4), C1.4 (duali), P1 (E_int al 1° ordine); appunti A9, B2, B3, C1.4; strada RT-S2a (SCOUT-2 S2-A).
Prima esecuzione: nessun file precedente in work/P3/.

## 1. Domande / enunciati da affrontare
**A. Dyson/Kato con ipotesi verificabili (R5-T9, R5-T10).**
- A1 (quadro del Gate 1). Su Ω limitato senza BC non esiste un propagatore (P1-P1: flussi non determinati). Dove vive allora Dyson? Risposta da dare con enunciati: (i) identità formale di getti in t per ogni soluzione liscia; (ii) in 𝔅 (P1-D1); (iii) su ℝ in L²; (iv) su intervallo con BC.
- A2. Teorema di Dyson–Phillips con convergenza **globale in t** e stima esplicita (Mittag-Leffler) sotto ipotesi leggibili dal simbolo: termine principale parabolico di ordine q, perturbazione di ordine r < q con coefficienti L^∞. Generalizza R5-T9(c). Controesempi che mostrano che le ipotesi servono (stesso ordine; termine principale dispersivo).
- A3 (Kato modo per modo). Rami di P + εT come funzioni analitiche di ε con raggio esplicito (Rouché) e derivata prima = accoppiamento con i duali di Lagrange.
**B. Regole di selezione ed elemento di matrice al 1° ordine (PR-C2d §4 P3.2, R5-P10).**
- B1. Formula dei cammini: termine di ordine j di Dyson nella base propria di A0 = Σ_cammini ΠV × differenza divisa di e^{tz} sui λ del cammino (Hermite–Genocchi). Corollari: 1° ordine = PR-C2d P3.2; terminazione con filtrazione (R5-P10 generalizzata).
- B2. E_int al 1° ordine nei quadri additivo e moltiplicativo; controllo: il caso commutante ridà R5-T2.
- B3. E_int dal bordo (P1-P6 lo lascia a S-P3, insieme a P1-Q5): avvezione–diffusione con Dirichlet su (0,L): elementi di matrice V_mn, regola di parità, ordine in t per t → 0 (riduzione d'ordine).
- B4 (L4). Perturbazione εx di un fattore τ − a(ξ): forma chiusa, Dyson finito di ordine deg a, regole di selezione nella base di Appell.
**C. Duali biortogonali come strumento di estrazione.** Lagrange (compagna, II-P5(b), II-T2, C12-T2); Appell/funzionali di getto a tempo t (C12-T6); Rosenbloom–Widder generalizzato (PR-C2b P6): esistenza di duali integrali covarianti ⟺ condizione sul simbolo; cosa resta su Ω limitato.
**D. Verdetto su RT-S2a (Faddeev–Lippmann–Schwinger).** Criterio esplicito (quello di SCOUT-2 + uno di merge fissato qui, §5 di PROOF_PACKAGE prima della valutazione). Teoremi: scomposizione di bilancio, continuità in H^m (contro P1-P1(e)), sistema N×N e convergenza, pesi a_i/a, legame E^add = Σ_i E^{(i)}, dipendenza da L0, ostruzione nel caso non regolarizzante.

## 2. Skill (in ordine d'uso)
1. `skills-local/session-protocol` — letta per prima, per intero (fatto).
2. `skills-local/claim-lifecycle` — ciclo di ogni enunciato, righe LEDGER (fatto: letta).
3. `_vendor/Auto-claude-code-research-in-sleep/skills/proof-writer/SKILL.md` — triage (PROVABLE AS STATED / AFTER WEAKENING / NOT JUSTIFIED), mappa delle dipendenze, prova a passi numerati, rischi (letta).
4. `_vendor/math-skill/SKILL.md` (modo `proof`, + references/proof-playbook.md) — controesempi prima delle prove, esplorazione separata dalla prova (letta).
5. `_vendor/scientific-agent-skills/skills/sympy/SKILL.md` — verifiche simboliche in work/P3/sympy/ con `D:\ProblemaBase\.venv\Scripts\python.exe -I` (letta). La numerica compare solo come controllo, marcata.
6. proof-checker: affidato a S-CHECK (CHECK_REQUEST.md + DOMANDA in inbox/S-CHECK.md). Nessuno script `_vendor` eseguito.

## 3. Fonti
Engel–Nagel 2000 (III.1, III.3.14–3.16 Miyadera–Voigt); Pazy 1983 §3.1; Kato 1976 (II §1–2: perturbazione analitica in dim. finita); Hermite–Genocchi (de Boor, *Divided differences*, Surveys in Approx. Theory 2005); Opitz 1964 / McCurdy–Ng–Parlett 1984 (exp di matrici triangolari = differenze divise); Faddeev 1961, Watson 1953 (via SCOUT-2); Rosenbloom–Widder 1959 (via PR-C2b P6). Numerazioni marcate "da verificare" quando non controllate.

## 4. Contatti
- S-P1 (chiusa): RISPOSTA alla TABELLA ricevuta (inbox/S-P1.md) — cosa uso e cosa chiudo (P1-Q5 al 1° ordine).
- S-II (chiusa): AVVISO con P3-P2 (Kato/duali di Lagrange) se utile.
- S-P2 (in parallelo): TABELLA — componenti di bilancio continue in H^m (rilevante per B8/E_int^⊥).
- S-CHECK: DOMANDA di audit. central: PLAN-READY, TABELLA LEDGER, DONE.

## 5. Criterio di "fatto"
PROOF_PACKAGE.md con: A2 (Dyson globale) + controesempi, B1 (formula dei cammini), B3 (bordo: elemento di matrice + ordine in t dimostrato), B4 (εx), C (duali), D (verdetto motivato con criterio scritto prima); sympy con esiti; CHECK_REQUEST autosufficiente sui claim principali; righe LEDGER in central; DONE S-P3. Nessun claim marcato DIMOSTRATO senza audit.

## Ripresa — audit 5 (25/10/2026, dopo S-CHECK-5)
Letti, in quest'ordine: RIPRESA.md (ultimo AGGIORNAMENTO: DONE S-CHECK-5, decisione RT-S2a PARCHEGGIATA), skills-local/session-protocol (per primo), skills-local/claim-lifecycle, questo PLAN, PROOF_PACKAGE.md, inbox/S-P3.md (RISPOSTA di S-CHECK-5; AVVISI di S-P1 ripresa e di central), work/CHECK/AUDIT_P3.md, ROUTES.md (riga "RT-S2a — REVISIONE": PARCHEGGIATA), claims/LEDGER.md (righe P3-*, P1-Q5, nota CIT-AUDIT-3), research/CIT-AUDIT/AUDIT-3.md (#8 Engel–Nagel verificato su fonte primaria).
**Compito:** recepire i fix di AUDIT_P3.md nel PROOF_PACKAGE, marcando ogni modifica con `[fix <id>]`; nessun nuovo claim oltre a quelli richiesti dai fix.
**Fix da applicare (in ordine di severità):**
1. **T6-vi (CRITICAL)** — P3-T6(vi): restringere alla famiglia {L₀^Σ} (→ (vi′)); aggiungere la famiglia L₀^θ = ∂_t − θΣa_i, θ ∈ [0,1), come controesempio all'enunciato originale (scomposizioni esatte, equivarianti, non degeneri, componenti dipendenti da θ, anch'esse quadrature di u); enunciare il **principio di bilancio termine per termine** ∂_t u^{(i)} = a_i(∂_x)u, u^{(i)}(t₀) = 0 come principio di selezione (non teorema), con la dipendenza da t₀ (scelta dell'inversa destra di ∂_t) esplicitata.
2. **V-1 (MAJOR)** — §7.1 contributo netto 1 (e §1, §8): togliere "l'unica scomposizione … continua in H^m"; l'unicità vale solo sotto il bilancio per termine.
3. **T3-1 (MAJOR)** — P3-T3: la "Lettura (2)" vale solo per dati modali finiti; osservazione di portata dopo (iii); caso u₀ = x²(L−x)² (‖E‖ ~ t^{7/4}) come V-ex; nuovo APERTO P3-Q-bordo (α, β, γ) in §10.
4. MINOR: L2-1 (lemma di continuità del prodotto), L2-2 (Engel–Nagel GTM 194 Thm III.3.14 p. 196, Cor. III.3.15, Cor. III.3.16 p. 199 — verificato CIT-AUDIT-3), C1-1 (spettro dei moltiplicatori + Hille–Yosida), T2-1 (formula di Cauchy per F_j, elimina de Boor), T2-2 (ipotesi di (b) in (e)), P1-1 (Hadamard con c complesso: w → +∞), T3-2 (frase BCH in (v)), T3-3 (E^{mult,(1)} su D(V) = H¹; c < 0), T3-4 (dipendenza delle costanti da N), T6-1 (E^{(i)} = G_i a_i Σ_{j≠i} u^{(j)} = E_int^{(i)} di SCOUT-2).
5. **§7 riscritto** secondo la decisione del coordinatore (ROUTES.md): RT-S2a **PARCHEGGIATA** (revocato il MERGE); P3-T6(i), (iv), (v) entrano in RT-2 come quadro (f) di P1-D3 **solo a coefficienti costanti**, con il principio di bilancio dichiarato; riapertura = criterio (b) originale di SCOUT-2 a coefficienti variabili, in qualunque spazio (P3-Q4 riformulato).
6. Tabella stati (§1) e righe §12 allineate al LEDGER (DIMOSTRATO / CON-FONTE verificata / FALSO / APERTO); §0 aggiornato (audit avvenuto).
**Skill:** session-protocol, claim-lifecycle (stati = ultimo controllo superato: non si alza nulla oltre il LEDGER; FALSO per (vi) come scritta); sympy (controllo breve della famiglia θ e del principio di bilancio in work/P3/sympy/p3_ripresa5.py, solo conferma dei calcoli dell'audit). Nessuno script _vendor.
**Messaggi:** AVVISO a inbox/S-P1.md (P1-Q5 chiuso al 1° ordine solo per dati modali finiti; P3-Q-bordo; RT-S2a parcheggiata); DONE "S-P3 (ripresa audit)" in inbox/central.md.
**Criterio di fatto:** tutti i fix marcati `[fix <id>]` nel PROOF_PACKAGE; §7 riscritto; tabella stati = LEDGER; AVVISO a S-P1; DONE in central. Scrittura solo in work/P3/ e inbox/.
