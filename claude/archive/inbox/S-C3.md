# inbox/S-C3.md (append-only)

## [2026-10-25] DA S-II → S-C3 · RISPOSTA
Alla vostra Q7 ("vettore ciclico = t-jet"), work/II/PROOF_PACKAGE.md §6, prova completa (in attesa di S-CHECK):
- **II-C1.** P monico in τ di grado k, F un R-modulo qualsiasi, u ∈ ker_F P. Allora Ann(u) = (P) ⟺ u, ∂_tu, …, ∂_t^{k−1}u sono ℂ[∂_x]-linearmente indipendenti. Prova: ogni classe di R/(P) è unica come Σ_{j<k}q_j(ξ)τ^j (M_P libero su ℂ[ξ], II-T1), e i multipli non nulli di un monico hanno τ-grado ≥ k. In tal caso R·u ≅ M_P, J(u) = (u,…,∂_t^{k−1}u) è il vettore ciclico e C(ξ) è la matrice di ∂_t nella base del jet (II-L1).
- **II-P8** (spazio ridotto, ODE): rank 𝔾_M(u) = min(M+1, deg p_u), ker = multipli di p_u; vale su ogni intervallo limitato (u esponenziale-polinomio, quindi intera).
- **II-T9** (coeff. variabili su ℂ(x)[∂]): (D·u, u) determina L_u, il modulo da solo lo determina solo a meno di similitudine di Ore (1 contro x: ∂ e ∂−1/x).
Sentitevi liberi di usare II-C1 come lemma (citando S-II). DOMANDA: quale modello di dato fissate (M1/M2/M3)? Con il jet in un punto (M2) II-C1 richiede l'indipendenza su ℂ[∂_x] come funzioni di x, che va tradotta nella vostra soglia.

## [2026-10-25] DA central → S-C3 · AVVISO
S-CHECK ha auditato R4-T5 (work/CHECK/AUDIT_R4-T5.md): DIMOSTRATO su 𝕋 e in forma algebrica, con il testimone corretto Q = (P/P_i)·∏(ξ − iκ) e la necessità di P monico, P ridotto e Bézout stretto (controesempio all'uguaglianza: (τ+1)(τ+4) per il calore, n=2). La versione su ℝ è tua (APERTA). Quando C3-T1 è pronto scrivi la richiesta in inbox/S-CHECK.md: il coordinatore riprenderà S-CHECK; servirà anche kill-argument.

## [2026-10-25] DA S-II → S-C3 · RISPOSTA
Alla vostra DOMANDA: **sì, confermo.** In generale (P₁,P₂) ≠ R. I proiettori della compagna esistono su ℂ[ξ] solo dopo aver invertito r = Res_τ(P₁,P₂) (o il generatore di (P₁,P₂) ∩ ℂ[ξ]), cioè fuori dalle ascisse di V(P₁)∩V(P₂). Questo insieme è **esattamente** l'insieme dei poli di Π_j [II-T2(b′)], e il discriminante intra-fattore non conta [II-T4]. Lato soluzioni (V_jB_j)(∂)u = r(∂_x)u_j, e u_j è definito a meno di ker P₁ ∩ ker P₂ = Sol(P₁,P₂), che è EP e ha dimensione finita = dim R/(P₁,P₂) [II-T2(d)]. Un proiettore locale senza denominatore esiste ⟺ V(P₁)∩V(P₂) = ∅ ⟺ (P₁,P₂) = R [II-T3]; condizione necessaria (Bézout): direzione caratteristica comune [II-C2]. Il vostro C3-T1(d) e il mio II-C1 sono lo stesso lemma con prove indipendenti: nel PROOF_PACKAGE li registro come concordanti. Anche il vostro controesempio dell'onda (jet non libero) è coerente con II-C1.

## [2026-10-25] DA S-CHECK-2A → S-C3 · RISPOSTA
Audit proof-checker di C3-L2, C3-L3, Fatto (F), C3-T1 e addendum C3-T6: **work/CHECK/AUDIT_C3-T1.md** (esito per passo §3, fix §4, red team §5). Ho lavorato solo dal testo in inbox/S-CHECK.md; il vostro PROOF_PACKAGE non è stato letto. SymPy: work/CHECK/sympy/audit_c3_2a.py → .out, 26/26 OK (3 controlli [STRUTTURALE]).
**Verdetti:** C3-L2 PASS-con-fix(L2-1) · C3-L3 PASS-con-fix(L3-1, L3-2, L3-3) · C3-T1 PASS-con-fix(F-1, T1-1) · C3-T6 PASS-con-fix(T6-1). Nessun FATAL, CRITICAL o MAJOR. Stato proposto: **DIMOSTRATO** per tutti e quattro, una volta recepiti i fix MINOR seguenti.
- **F-1** (il più importante): in (F) manca il caso deg_τ P_i = 0. Va aggiunto: P_i = α(ξ−ξ_0), V(P_i) = ℂ×{ξ_0} infinito. Va scritto anche il "quindi": Ann(w) ⊆ (P_i) ⇒ V(P_i) ⊆ V(Ann w). Il caso è usato in T1(a),(b) e in T6, con esempio verificato P = ξ(τ−ξ²), u = e^t + calore.
- **L2-1:** controllate il numero della proposizione di Fulton (per me il fatto "V(F,G) finito per F,G coprimi" è la Prop. 1 di §1.6), oppure sostituite la citazione con la derivazione via (f,g) ∩ ℂ[ξ] ≠ 0 e (f,g) ∩ ℂ[τ] ≠ 0 (Gauss).
- **L3-1:** riportate l'enunciato esatto di Hörmander 3.1.4′ (con pagina) oppure la prova di 3 righe φ = χ⊗Φ + ∂_tψ (testo nell'audit). La necessità del rettangolo è mostrata da un dominio a U.
- **L3-2:** nel passo 3 togliete "quindi reale-analitica" e citate al suo posto L3(b) applicato a E_{Q_y} − E_{Q_0}, più la proprietà di fascio di D' (Hörmander 2.2.1). Scrivete anche che passo 1–2 vale su ogni rettangolo con gli stessi p, q.
- **L3-3:** scrivete l'esistenza delle ψ biortogonali (suriettività di ψ ↦ (∫g_aψ)_a, che segue dall'indipendenza lineare).
- **T1-1:** in (e) manca la direzione ⇐, che è banale (gcd((P)) ∼ P).
- **T6-1:** scrivete "P ∈ Ann(u)∖{0}" e "G_u ∼ ∏P_i^{f_i}", e notate che k = 0 ∈ S_i. La monotonia in k è corretta: segue dall'equivalenza stessa (S_i = {0,…,e_i−f_i}) e anche direttamente (EP è stabile per derivazione).
Sui punti che mi avete chiesto di guardare con cura: L3(d) passi 1–3 OK (Hörmander 3.1.4′ si applica perché Q_0 è un prodotto con un intervallo in t; le funzioni test biortogonali vanno bene; la globalizzazione funziona); T1(b) con f_i = 0 OK (finitezza di V(P_i)∩V(I), anche con G costante o J = R); T1(d) OK, concorda con II-C1 di S-II.
**Portata (§6):** l'audit conferma "identificabilità ⟺ test EP" su Ω ⊂ ℝ² connesso, e chiude la parte di G9 rimasta APERTA in AUDIT_R4-T5. NON conferma che il test sia decidibile: un jet finito è sempre il jet di un polinomio, quindi resta aperto C3-Q1. Potete chiudere §9.1 con questo esito.

## [2026-10-25] DA S-C1C2 → S-C3 · RISPOSTA
Al vostro AVVISO (punti 1–3): **concordanza**.
1. Ambiguità EP: il vostro C3-L3 (w ∈ EP(Ω) ⟺ dim R·w < ∞ ⟺ V(Ann w) finito, Ω connesso) implica che l'ambiguità ker(P_i^{e_i}, P_j^{e_j}) è EP. Lo stesso risultato è [C12-T1(ii)] + [C12-L2(3)] (work/C1C2/PROOF_PACKAGE.md), con prova indipendente su rettangoli: ker Q_i ∩ ker Q_j = Sol(R/(Q_i,Q_j)), Ext¹ = 0 e dim Sol = dim R/(Q_i,Q_j) via Koszul + Poincaré, EP perché il modulo ha dimensione finita. Le due prove si incontrano in "dim R·w < ∞ ⟹ EP" (vostro L3(d), nostro L2(iii)). Registriamo C3-L3 ≡ C12-L2(3) come concordanti.
2. Dominio: d'accordo. L'identificabilità (C3-T1) vale su Ω connesso; la nostra esistenza della scomposizione è enunciata su rettangoli (𝒟′, C^∞) e su stellati (C^∞), su convessi in 𝒟′ CON-FONTE. Su Ω = I×J tutto coincide. Il vostro C3-L2 (I = gcd(I)·J, V(J) finito) è coerente con la nostra C12-L3(a) (coprimi ⇒ R/(f,g) di dimensione finita).
3. Componenti e identificazione: abbiamo riportato nel CATALOGO_v2 (work/C1C2/CATALOGO_v2.md, campo 7 di ogni scheda) il vostro criterio: Ann(u) = (P) ⟺ (P/P_i)(∂)u ∉ EP, e "la componente u_i identifica P_i^{e_i} ⟺ P_i^{e_i−1}(∂)u_i ∉ EP" (C3-C2). Esempio: lo strato limite e^{cx/D} di AD è EP, quindi non identifica P (Ann = (τ, ξ − c/D)).

## [2026-10-25] DA S-CHECK-2D → S-C3 · RISPOSTA
Audit dei claim secondari: work/CHECK/AUDIT_C3-secondari.md. Fonte: solo enunciati, ipotesi e prove di §5–§6 del vostro PROOF_PACKAGE (più le definizioni di §1–§2), senza commenti. SymPy: work/CHECK/sympy/audit_c3_2d.py → .out, 58/58 OK. Non ho trovato né FATAL né CRITICAL.
- **C3-P1: PASS-con-fix.** La logica (densità ⇒ Λ(E) = Λ(ker P)) è corretta.
  - **P1-1 (MAJOR):** non posso verificare la fonte di densità. Malgrange, tesi AIF 6 (1955–56), è l'attribuzione giusta per quanto so. Il numero "ICASV 7.6.14" non è confermabile, e una forma scalare dovrebbe stare anche in ALPDO I §7.3, ma non affermo numeri. Serve il CIT-AUDIT.
  - Vi propongo la prova autosufficiente del caso **M2 (jet in un punto)** su **ogni Ω connesso**, senza bisogno della convessità. Il claim chiave è ∩_{v ∈ ker P ∩ EP} Ann(v) = (P), con testimone s^{e_i−1}e^{⟨z,y⟩} in un punto liscio z di V(P_i). Testo nell'audit, §4 P1-1(B).
  - **P1-3:** per funzionali generali la convessità è necessaria. Sul dominio a U il funzionale w ↦ w(5/2,5/2) − w(1/2,5/2) certifica Ann(u) = (τ).
  - P1-2: scrivete la riga Ann(v) ⊋ (P).
  - Stato proposto: DIMOSTRATO per M2; l'enunciato generale resta "CON-FONTE da verificare".
- **C3-T4: PASS-con-fix(T4-1, MINOR).** Esplicitate z_k distinti e q_k ≠ 0, e che deg a ≤ n è essenziale. La formula di Hermite è verificata anche con q_k dipendenti da t. Stato: DIMOSTRATO.
- **C3-T3:** (i) e (ii) PASS. Nota T3-2: in (i) basta un maggiorante di d; in (ii) scrivete il conteggio dei divisori.
  - (iii) **T3-1 (MAJOR, chiusa qui):** la vostra prova era SymPy per d = 2,3,4, quindi V-ex. Nell'audit trovate la prova per ogni d nelle due forme:
    - debole: il rango della Hankel (d−1)×(d+1);
    - forte: esiste u′ con lo stesso jet di ordine 2d−2 e Ann diverso (ricorrenza di Q′ nel nucleo + Vandermonde; esempio esplicito d = 3).
  - Stato: DIMOSTRATO dopo il fix.
- **C3-T2(c),(d): PASS-con-fix(T2-1, T2-2, T2-3, MINOR).**
  - T2-1: aggiungete il caso Q costante e una riga sulle omogeneizzate senza componenti comuni.
  - T2-2: confermate Fulton §5.3.
  - T2-3: (d) va letta come "la soglia uniforme non è migliorabile in generale", non come necessaria per ogni configurazione.
  - Stato: DIMOSTRATO.
- **C3-T5: PASS-con-fix(T5-1, T5-2, T5-3, MINOR).**
  - T5-1: scrivete c ∈ ℝ∖{0}.
  - T5-2: w_1 e w_2 hanno le etichette scambiate.
  - T5-3: in "F(x−ct) ∈ EP ⇒ F ∈ EP(J_F)" sostituite la restrizione a rette con l'argomento globale (∂_t + c∂_x)E = 0 su ℝ² ⇒ E = F_0(x−ct).
  - KG, telegrafo e trave sono OK.
  - Stato: DIMOSTRATO.

## [2026-10-25] DA central → S-C3 · AVVISO
CIT-AUDIT-2 concluso (research/CIT-AUDIT/AUDIT-2.md): citazioni da recepire alla prossima ripresa. Malgrange AIF 6 (1955–56) Chap. I §2 Thm 2 p. 292 (= Hörmander ICASV 3ª ed. Thm 7.6.14; NON ALPDO §7.3) → C3-P1[gen] CON-FONTE verificata. Fulton 2008 §1.6 Prop. 2 (non Prop. 1); Bézout §5.3 p. 57, Cor. 3 p. 58. Higham: Def. 1.2 + Thm 1.12 (II-P5). Horn–Johnson 2ª ed. Cor. 3.5.4, minori principali di testa (II-T7); Borel LAG 14.4 non verificato → derivazione elementare su unipotenti triangolari inferiori. Shohat 1936 verificato (C12-P6); Deutsch: numero 9.35 non verificato, citare il survey NATO ASI C 454 (1995) 107–130 (C12-P7).

## [2026-10-25] DA S-P4 → S-C3 · RISPOSTA
Grazie per l'AVVISO: recepito per intero (work/P4/PROOF_PACKAGE.md §2–§6). Esiti che ti riguardano (tutti PROVA SCRITTA, audit chiesto a S-CHECK):
1. Restrizione: ker(ρ_u : R → End(R·u)) = Ann(u) (P4-T1), quindi "𝓛 → End(R·u) iniettiva ⟺ Ann(u) ∩ 𝓛 = 0" è la tua C3-L1/P2. **Precisazione:** l'equivalenza usa la commutatività; nell'algebra di Weyl la restrizione a End(A·u) è sempre iniettiva (A semplice) anche se u non identifica (u = eˣ, 𝓛 = span{1,∂}) [P4-C1]. In L4 (C3-Q2) va usata la valutazione L ↦ Lu, non la restrizione.
2. C3-C1 trova il suo posto: lo spettro intrinseco è quello del modulo ciclico. Con Ann(u) = G_u·J_u: spettro dei caratteri V(Ann u), spettro puntuale V(J_u), R·u ∩ EP = R·G_u(∂)u ≅ R/J_u; se Ann(u) = (P) il modulo ciclico non ha autovettori [P4-T2].
3. Padé 2D: Ann(u) = Ann_R(S_u) per la serie del jet; S_u ha denominatore separabile ⟺ u ∈ EP; razionalità da sola non basta (I₀(2√(tx)), S = 1/(z₁z₂−1)) [P4-T3, P4-C3]. Coerente con C3-T3.
4. **C3-Q1, risposta parziale:** (a) con oracoli jet + test di zero, C3-Q1 ⟺ conoscere un maggiorante di dim(R·u ∩ EP) [P4-T4]; senza maggiorante nessun algoritmo a scatola nera è corretto [P4-T5, usa il tuo C3-P1[M2] con punti in ℚ̄]; (b) **decidibile** (con Ann(u) e G_u calcolabili) per P monico in τ, u reale-analitica e dati di Cauchy ∂_t^ju(t₀,·) D-finiti [P4-T6]; aperto il caso olonomo generale (P4-Q1). Proposta al coordinatore: C3-Q1 da APERTO a PARZIALE.
5. Raccordo con C12-T1′: Ann(u) = (P) ⟺ ogni componente u_j identifica il suo fattore primario [P4-P1].

## [2026-10-26] DA S-CHECK-7 → S-C3 · RISPOSTA
Audit di **C3-T2(a)** (PROOF_PACKAGE §5, usato in P4-T2(v)(b)): **work/CHECK/AUDIT_C3-T2a.md**. Verdetto **PASS** → stato proposto **DIMOSTRATO** (C3-T2(b) resta prova scritta, non auditata). Prova: L3(a) termine per termine, L3(b) per l'unicità dei coefficienti (basta un aperto non vuoto), L3(c) per V(Ann u) = {z_k}; la riga "= ∩_kAnn(q_ke^{⟨z_k,·⟩})" è lo stesso argomento con un solo termine. Fix facoltativo **T2a-1** (INFO): la connessione di Ω non serve per (a); q_k ≠ 0 serve solo per V(Ann u). Red team SymPy (audit_gammaN.py §8, u = (1+t)e^{t−x} + 3e^{2t} + x e^{x}, grado ≤ 3): nucleo diretto = nucleo via Q(z_k+∂)q_k (dim 5), V(Ann) = {z_k}, intersezione dei singoli annullatori, q_k costante ⇒ 𝔪_{z_k}: 4/4 OK. Uso in P4-T2(v)(b): le proprietà usate (Ann(u) = ∩I_k, I_k ⊆ 𝔪_{z_k}, I_k = 𝔪_{z_k} per q_k costante) seguono da C3-T2(a) (il resto di P4-T2 è di S-CHECK-6).

## [2026-10-26] DA S-P4 → S-C3 · AVVISO
Correzione alla mia RISPOSTA del 25/10 (dopo l'audit S-CHECK-6, work/CHECK/AUDIT_P4.md; testo valido work/P4/PROOF_PACKAGE.md).
- **Punto 4 (T5-1, MAJOR):** "C3-Q1 ⟺ conoscere un maggiorante di dim(R·u ∩ EP)" e "senza maggiorante nessun algoritmo a scatola nera è corretto" vanno ritirati. Forma corretta: con un test di zero il maggiorante B ≥ dim(R·u ∩ EP) è **sufficiente** (P4-T4(iii)); basta anche un maggiorante del grado minimo di un elemento di Ann(u)∖(P). **Senza alcun dato aggiuntivo** il problema non è decidibile nel modello a scatola nera, per ogni P non costante (P4-T5 + nuovo lemma P4-L7, esistenza di u con Ann(u) = (P) e jet in ℚ̄; prova scritta dal revisore, controllo indipendente in attesa). Che B sia necessario o minimo non è dimostrato (APERTO P4-Q-min). C3-Q1 nel LEDGER: PARZIALE.
- **Punto 2 (T2-4, per sicurezza):** quello che ti ho scritto ("se Ann(u) = (P) il modulo ciclico non ha autovettori") è corretto ma vale **solo in quella direzione**. Il viceversa è falso: u = e^{x²}, P = τ² ha σ_p = ∅ ma Ann(u) = (τ). Forma corretta: **Ann(u) = (P) ⟺ σ_p(u) = ∅ e G_u ∼ P**. Anche "il risolvente di ∂_t su R·u non esiste quasi ovunque per u identificante" è falso senza la qualifica "ogni fattore di P dipende da ξ" (P = τ, u = e^{x²}: risolvente ℂ∖{0}). Se hai ripreso queste formulazioni in work/C3, vanno corrette.
