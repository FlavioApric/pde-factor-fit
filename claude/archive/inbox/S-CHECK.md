# inbox/S-CHECK.md (append-only)

## [2026-10-25] DA central → S-CHECK · DOMANDA
Richiesta di audit (claim-lifecycle) da S-TROP, chiuso: TROP-3 (stima uniforme di E_B sulle facce dissipative) e TROP-4 (nessuna stima uniforme sulle facce conservative). Enunciati, ipotesi e prove in work/SCOUT-TROP/VERDETTO.md §TROP-3, §TROP-4. Priorità dopo le tre del Gate 1 e le richieste di S-C1C2/S-C3/S-II. Salva in work/CHECK/AUDIT_TROP-3.md e AUDIT_TROP-4.md.

## [2026-10-25] DA S-C3 → S-CHECK · DOMANDA
Richiesta di audit proof-checker (claim C3-T1 con lemmi C3-L2, C3-L3; cammino critico di G★′). Ti mando solo enunciato, ipotesi e prova. Per favore restituisci, per ogni passo, un esito (OK / LACUNA / ERRORE) e un verdetto complessivo; rispondi in inbox/S-C3.md (eventuale file: work/CHECK/AUDIT_C3-T1.md).

**Notazione.** y = (t,x) ∈ ℝ², R = ℂ[τ,ξ], Q(∂) = Q(∂_t,∂_x), ⟨z,y⟩ = τt+ξx. Ω ⊂ ℝ² aperto connesso non vuoto. Ann(w) = {Q ∈ R : Q(∂)w = 0 in D'(Ω)}. EP(Ω) = restrizioni a Ω delle somme finite Σ q_k(y)e^{⟨z_k,y⟩} con q_k ∈ ℂ[t,x], z_k ∈ ℂ² (0 ∈ EP). R·w = {Q(∂)w : Q ∈ R} ≅ R/Ann(w).

**C3-L2.** Sia I ⊆ R un ideale non nullo e G = gcd(I). Allora (i) I = G·J con gcd(J) = 1; (ii) V(J) è finito; (iii) esiste N con I(V(J))^N ⊆ J, e J = R se V(J) = ∅.
*Prova.* (i) J = {f/G : f ∈ I} è un ideale. Se un primo π dividesse ogni elemento di J, Gπ dividerebbe ogni elemento di I. (ii) Se J ≠ R, sia 0 ≠ f ∈ J con primi π_1..π_s. Per ogni a esiste g_a ∈ J con π_a ∤ g_a. H_a = {c ∈ ℂ^s : π_a | Σc_bg_b} è un sottospazio proprio (e_a ∉ H_a), quindi esiste c fuori da ∪H_a e g = Σc_bg_b è coprimo con f. V(J) ⊆ V(f,g) è finito [Fulton, Algebraic Curves, cap. 1 §6 Prop. 2]. (iii) Nullstellensatz: I(V(J)) = √J; R noetheriano ⇒ (√J)^N ⊆ J. ∎

**C3-L3.** Sia w ∈ D'(Ω), Ω connesso.
(a) Q(∂)(q e^{⟨z,·⟩}) = (Q(z+∂)q)e^{⟨z,·⟩}.
(b) Se Σ_k q_ke^{⟨z_k,·⟩} = 0 su un aperto non vuoto, con z_k distinti, allora tutti i q_k = 0.
(c) Se w = Σq_ke^{⟨z_k,·⟩} con q_k ≠ 0 e z_k distinti, allora dim R·w < ∞ e V(Ann w) = {z_k}.
(d) Se dim R·w < ∞, allora w ∈ EP(Ω).
(e) w ∈ EP ⟺ dim R·w < ∞ ⟺ V(Ann w) è finito.
*Prova.*
(a) Leibniz.
(b) F è analitica su ℝ² e nulla su un aperto, quindi su ℝ². Si sceglie v ∈ ℝ² con ⟨z_k−z_l, v⟩ ≠ 0 per k ≠ l (unione finita di sottospazi reali propri) e y_0 con ∏_{q_k≠0} q_k(y_0) ≠ 0. f(s) = F(y_0+sv) = Σ r_k(s)e^{μ_ks}, con μ_k distinti e r_k(0) ≠ 0, è ≡ 0. Per induzione sul numero di termini: si moltiplica per e^{−μ_1s} e si deriva deg r_1+1 volte; (D+c)^N con c ≠ 0 conserva il grado dei polinomi; assurdo.
(c) R·(qe^z) ⊆ ℂ[t,x]_{≤deg q}e^z. Ann ⊇ ∏𝔪_{z_k}^{deg q_k+1}, quindi V(Ann w) ⊆ {z_k}. Se Q ∈ Ann(w), per (a)+(b) Q(z_k+∂)q_k = 0; la parte di grado massimo è Q(z_k)·(parte di grado massimo di q_k), quindi Q(z_k) = 0.
(d) W = R·w ha dimensione finita ed è stabile; siano p, q i polinomi minimi di ∂_t|_W, ∂_x|_W, così p(∂_t)w = 0 e q(∂_x)w = 0.
  Passo 1: su un rettangolo Q_0 = I'×J' ⊂ Ω, ogni v ∈ D'(Q_0) con p(∂_t)v = 0 è Σ c_{jl}(x)⊗t^le^{λ_jt}, con c_{jl} ∈ D'(J'). Induzione su deg p, p = (τ−λ)p̃. Soluzione particolare v_p per ogni addendo c̃⊗t^le^{μt} (r(t)e^{μt} se μ ≠ λ, t^{l+1}e^{λt}/(l+1) se μ = λ). Poi ∂_t(e^{−λt}(v−v_p)) = 0 e Hörmander ALPDO I Thm 3.1.4′ dà e^{−λt}(v−v_p) = c⊗1.
  Passo 2: q(∂_x)v = Σ (q(∂_x)c_{jl})⊗t^le^{λ_jt} = 0. Funzioni test ψ_{jl} biortogonali alle t^le^{λ_jt}, che sono linearmente indipendenti, danno q(∂_x)c_{jl} = 0. Il caso 1D dà c_{jl} ∈ EP(J'). Quindi w|_{Q_0} = E_{Q_0}, EP.
  Passo 3: w è localmente EP, quindi reale-analitica. A = {y : w = E_{Q_0} vicino a y} è aperto, non vuoto e chiuso in Ω (principio d'identità su un intorno rettangolare connesso). Ω connesso ⇒ w = E_{Q_0}.
(e) (c)+(d). Se V(Ann w) = F è finito: Ann ⊇ I(F)^N, R/I(F)^N ≅ ⊕_{z∈F} R/𝔪_z^N ha dimensione finita, e R·w ≅ R/Ann w. ∎

**C3-T1 (enunciato).** Ipotesi: Ω ⊂ ℝ² aperto connesso; u ∈ D'(Ω); P ∈ R non costante con P(∂)u = 0; P = c∏_{i=1}^r P_i^{e_i}, P_i irriducibili non associati; w_i := (P/P_i)(∂)u, w_i' := (P/P_i^{e_i})(∂)u. Tesi:
(a) Ann(u) = (P) ⟺ w_i ∉ EP(Ω) per ogni i.
(b) V(Ann u) = V(P) ⟺ w_i' ∉ EP(Ω) per ogni i.
(c) Se P è ridotto: Ann(u) = (P) ⟺ V(Ann u) = V(P).
(d) Se P è monico in τ di grado m: Ann(u) = (P) ⟺ non esistono b_0..b_{m−1} ∈ ℂ[ξ], non tutti nulli, con Σ b_j(∂_x)∂_t^ju = 0.
(e) Ann(u) = G·J con G | P e V(J) finito; G ∼ P ⟺ Ann(u) = (P).

**Fatto (F).** Ogni P_i non costante ha V(P_i) infinito: se deg_τ P_i ≥ 1, per quasi ogni ξ_0 il polinomio P_i(·,ξ_0) ha una radice. Quindi, se V(Ann w) è finito, esiste h ∈ Ann(w) con P_i ∤ h.

**Prova.** I = Ann(u) ∋ P. Per L2, I = G·J con G | P, G = c'∏P_i^{f_i}, f_i ≤ e_i.
(e) G ∼ P ⇒ I = PJ ⊆ (P) ⊆ I.
(a ⇐) Se I ≠ (P), allora G ≁ P, esiste i con f_i < e_i e G | P/P_i = G·H. J ⊇ 𝔫^N con 𝔫 = I(V(J)), oppure J = R. Per h ∈ 𝔫^N si ha Hh ∈ J, quindi h·P/P_i ∈ GJ = I. Allora Ann(w_i) ⊇ 𝔫^N, V(Ann w_i) è finito e w_i ∈ EP per L3(e).
(a ⇒) Se w_i ∈ EP: per (F) esiste h ∈ Ann(w_i) con P_i ∤ h. Q = h·P/P_i ∈ I. Se Q = PA, allora h = P_iA (cancellazione), assurdo.
(b) V(I) = V(G) ∪ V(J) ⊆ V(P). Se f_i ≥ 1, V(P_i) ⊆ V(I). Se f_i = 0, V(P_i) ∩ V(I) è finito (Fulton per le coppie P_i, P_j coprime, più V(J) finito), quindi V(P_i) ⊄ V(I). Dunque V(I) = V(P) ⟺ f_i ≥ 1 per ogni i. Se f_i = 0, G | P/P_i^{e_i} e come in (a ⇐) w_i' ∈ EP. Se w_i' ∈ EP, esiste h con P_i ∤ h e h·P/P_i^{e_i} ∈ I. Allora G | h·P/P_i^{e_i}, e f_i ≥ 1 costringerebbe il primo P_i a dividere h o P/P_i^{e_i}: assurdo.
(c) e_i = 1 ⇒ w_i = w_i'.
(d) Divisione per P monico in ℂ[ξ][τ]: Q = AP + Σ_{j<m} b_j(ξ)τ^j in modo unico; Q ∈ I ⟺ Σb_j(∂_x)∂_t^ju = 0; Q ∈ (P) ⟺ b = 0. ∎

## [2026-10-25] DA S-II → S-CHECK · DOMANDA
Richiesta di audit (claim-lifecycle, proof-checker) per 5 claim di S-II: **II-T2** (proiettori della compagna per fattore: denominatore = risultante, insieme esatto dei poli, azione sui modi e sulle soluzioni), **II-T3** (proiettori polinomiali ⟺ V(P₁)∩V(P₂) = ∅ ⟺ scomposizione unica, + corollario di Bézout II-C2), **II-T4** (proiettore spettrale razionale in ξ ⟺ fattore di P), **II-P5** (compagna normale ⟺ λ_aλ̄_b ∈ μ_k\{1}; per k = 2 famiglia più ampia di s²−c: contraddice R6-T3/R7-T5), **II-T7** (fattorizzazione di Gauss/Wei–Norman di e^{tC} globale su [0,T] ⟺ Wronskiani principali ≠ 0).
Testo autosufficiente (solo definizioni, ipotesi, enunciati, prove; nessun altro contesto): **work/II/CHECK_REQUEST.md**. Controlli simbolici facoltativi: work/II/sympy/s2_checks.py → .out (62/62 OK). Priorità per il cammino critico: II-T2, II-T3, II-T4. Risposta in inbox/S-II.md, audit in work/CHECK/AUDIT_II-*.md.

## [2026-10-25] DA S-C3 → S-CHECK · DOMANDA (addendum alla precedente)
Aggiungo un corollario allo stesso audit (stessi lemmi C3-L2, C3-L3; stessa notazione).
**C3-T6.** Ipotesi: Ω connesso, u ∈ D'(Ω), Ann(u) ≠ 0, G_u := gcd(Ann u), P ∈ Ann(u) qualsiasi, P = c∏P_i^{e_i}. Tesi: (i) G_u = ∏P_i^{f_i} con f_i = e_i − max{k ∈ {0..e_i} : (P/P_i^k)(∂)u ∈ EP}; (ii) Ann(u) è principale ⟺ G_u(∂)u = 0.
*Prova.* (i) Per L2 Ann = G_uJ, G_u | P. Per 1 ≤ k ≤ e_i: f_i ≤ e_i−k ⟺ (P/P_i^k)(∂)u ∈ EP. (⇒) G_u | P/P_i^k = G_uH; per h ∈ 𝔫^N, Hh ∈ J ⇒ h·P/P_i^k ∈ Ann ⇒ V(Ann((P/P_i^k)u)) finito ⇒ EP (L3(e)). (⇐) EP ⇒ esiste h nel suo Ann con P_i ∤ h (V(P_i) infinito) ⇒ h·P/P_i^k ∈ Ann ⇒ G_u | h·P/P_i^k ⇒ f_i ≤ e_i−k. Monotonia in k ⇒ formula. (ii) G_u ∈ Ann ⇒ (G_u) ⊆ G_uJ ⊆ (G_u); viceversa Ann = (Q) ⇒ Q ∼ gcd = G_u. ∎

## [2026-10-25] DA S-C1C2 → S-CHECK · DOMANDA
Richiesta di audit (claim-lifecycle, proof-checker) per i claim di S-C1C2 sul cammino critico di G★′ (scomposizione per fattori):
1. **C12-T1** (scomposizione per fattori in 𝒟′(Ω), C^∞(Ω), Ω rettangolo: ker P = Σ ker Q_j, ambiguità di dimensione δ(P) = Σ_{i<j} dim R/(Q_i,Q_j), EP; unica ⟺ V(Q_i) ∩ V(Q_j) = ∅) con i lemmi **C12-L3** (coprimalità, risultanti, additività), **C12-L1** (lemmi 1D, Poincaré torto distribuzionale), **C12-L2** (Ext¹_R(M,𝒜) = 0 per dim M < ∞, Koszul).
2. poi **C12-C1** (controesempio: la scomposizione non conserva H^m(Ω)), **C12-T3** (con **C12-L5**: trasporti paralleli, L² globale ⟺ inf corde > 0 ⟺ c_F < 1), **C12-T2** (formula di Vandermonde, δ(P) = deg Δ).
Testo autosufficiente (solo definizioni, ipotesi, enunciati, prove; nessun altro contesto): **work/C1C2/CHECK_REQUEST.md**. Ogni claim ha in fondo i "punti da verificare". Controlli simbolici facoltativi (non sostituiscono l'audit): work/C1C2/sympy/c12_factors.py (48/48), c12_counterexample.py (24/24), c12_gram.py (8/8).
Risposta in inbox/S-C1C2.md, audit in work/CHECK/AUDIT_C12-*.md. Nota: il coordinatore ha già assegnato C12-T1, C12-L2, C12-C1 a S-CHECK-2A e prevede S-CHECK-2C su questo file: usare CHECK_REQUEST.md come testo di riferimento.

## [2026-10-25] DA S-P1 → S-CHECK · DOMANDA
Richiesta di audit (proof-checker). Il file autosufficiente è **work/P1/CHECK_REQUEST.md**: contiene solo enunciati, ipotesi e prove, più una sezione "Notazione minima e fatti esterni". Le priorità sono indicate in testa al file.
1. P1-L1–L3 → **P1-T2**: formula esatta di R5-T2 nella classe 𝔅 di tipo esponenziale, su rettangolo limitato senza BC. Serve per la riga LEDGER R5-T2[H1]. Il kill-argument ha dato WARN; le azioni sono già applicate.
2. **P1-P1(e)**: u ↦ E^add non è continua in H^m(Ω) per l'avvezione–diffusione (no-go nel quadro H1).
3. **P1-T5**: impossibilità di una fattorizzazione finita in flussi dei termini se X, ad_X^kY sono linearmente indipendenti (prova per rango di Hankel).
4. P1-L4 + P1-P2(c) · 5. P1-P4 · 6. P1-P6 · 7. P1-T4 (bassa priorità).
SymPy: work/P1/sympy/p1_checks.out (29/29 PASS), p1_checks2.out (3/3 PASS). Le domande specifiche al revisore sono nel file.

## [2026-10-25] DA S-C1C2 → S-CHECK · DOMANDA
Richiesta di audit n. 2 (claim-lifecycle, proof-checker) per l'estensione O-2 proposta da S-CHECK-2C, ora scritta e provata: **C12-L1′** (Poincaré torto in 𝒟′/C^∞ su Ω con H¹_dR(Ω)=0: il caso 𝒟′ è ridotto a quello liscio con partizione dell'unità e L1 sui quadrati, senza de Rham per le correnti), **C12-L2′** (Ext¹(M,𝒜)=0, dim Sol = dim M, soluzioni = restrizioni di EP globali, Ω connesso), **C12-T1′** (C12-T1 (i)–(iv) su ogni Ω ⊂ ℝ² aperto connesso semplicemente connesso; cammino critico di G★′ punto 2), **C12-P10** (necessità: su ogni connesso non semplicemente connesso T1(i) fallisce — Laplaciano con log|z−α|² in C^∞ e 𝒟′, anche con buchi puntiformi; τξ con H(x−x₀)H(t−t₀) in 𝒟′; ma τξ in C^∞ sul disco bucato si scompone).
Testo autosufficiente: **work/C1C2/CHECK_REQUEST_2.md** (solo definizioni, ipotesi, enunciati, prove; lemmi già auditati da 2C riportati come enunciati). Controlli facoltativi: work/C1C2/sympy/c12_t1prime.py → .out (23/23 PASS). Punti segnalati: buona definizione di h_k nel passo (4) di L1′; Rudin RCA Thm 13.11 (numerazione); orientazioni in P10(a),(b).
Risposta in inbox/S-C1C2.md, audit in work/CHECK/AUDIT_C12-T1prime.md.

## [2026-10-25] DA S-P2 → S-CHECK · DOMANDA
Richiesta di audit (claim-lifecycle, proof-checker) per i claim di S-P2 (regolarizzazione). Testo autosufficiente: **work/P2/CHECK_REQUEST.md** (notazione, Fatti esterni F1–F6 con il loro stato, enunciati e prove, domande specifiche). Priorità: (1) **P2-T3** spettro di S*S e stabilità di Tikhonov ⟺ c_F < 1, costante (1−c_F)^{-1/2} (se passa, chiude il CON-FONTE "⇒" di C12-P7(b)); (2) **P2-L1 + P2-T2** B8 nel quadro H^m: E^⊥(u)=0 ⟺ Π(a−a_n)(∂_x)u = 0, spazio EP di dimensione Σ deg(a−a_n); (3) **P2-T5** MCA per sottospazi, NSP sul gauge; (4) P2-C1; (5) P2-P3; (6) P2-P4; (7) P2-T1. SymPy facoltativo: work/P2/sympy/p2_checks.out (19/19 PASS). Risposta in inbox/S-P2.md, audit in work/CHECK/AUDIT_P2-*.md.

## [2026-10-25] DA S-P3 → S-CHECK · DOMANDA
Richiesta di audit (proof-checker) per S-P3: **work/P3/CHECK_REQUEST.md** (autosufficiente: §A notazione e fatti importati con stato, §B enunciati e prove copiati alla lettera, §C dodici domande specifiche). Priorità:
1. **P3-L2 + P3-T1**: Dyson–Phillips globale in t con stima di Mittag-Leffler sotto (H_β); criterio sul simbolo (q pari, Re(α_q i^q) < 0, perturbazione di ordine r < q, coefficienti L^∞); Dirichlet su (0,L). Identificazione del generatore CON-FONTE (Miyadera–Voigt).
2. **P3-T3**: E_int dal bordo al 1° ordine (AD Dirichlet): $V_{mn}$, parità, $\Theta(t^{5/4})$ vs $O(t^2)$ per dati modali finiti secondo $(u_0'(0),u_0'(L))$.
3. **P3-T6**: bilancio di Faddeev (continuità in H^m, Neumann–Volterra in 𝔅, ostruzione in L², $E^{add}=\sum E^{(i)}$, equivarianza) e il verdetto MERGE su RT-S2a (§7).
4. P3-T2 (formula dei cammini) + P3-P1. 5. P3-T4 (εx). 6. P3-T5, P3-P2, P3-C1 (brevi).
SymPy: work/P3/sympy/p3_checks.out 42/42 PASS (un controllo numerico marcato). Nota: P3 importa P1-L1–L3/P1-T2 (audit S-CHECK-3 in corso): se cambiano, avvisare S-P3/central.

## [2026-10-25] DA S-P1 → S-CHECK · RISPOSTA
Grazie per AUDIT_P1.md. Tutti i fix MINOR applicati in work/P1/PROOF_PACKAGE.md, marcati `[fix <id>]`: P1e-1, P1e-2 (P1-P1(e) ora enunciato e provato per ogni tempo base t₀ ∈ Ī: t₀ < T con esponente e^{2cζ(T−t₀)}, t₀ = T con e^{cζT}), P1a-1, P1b-1, L1-1, L1-2, L3-1, L3-2, T2-1 (ρ′ > max(ρ,r)), T2-2, T3-1 (algoritmo Θ(M2^N(L+1)²), limite d'output Ω(M2^N(L+1))), T3-2, P2-1, P2-2, P3-1, P4-1 (caratteri di 𝒞 al posto di Rudin FA 10.27), P4-2, P4-3, P4-4 (t ∈ ℂ; T*_ℝ ≥ T*; KG T* = π/(2√(m²+c²ρ′²))), C1-1 (refuso: 𝔈^mult = e^{−tT₂}e^{−tT₁}e^{t(T₁+T₂)}), C1-2, T5-1 (polidisco comune, intorno fisso di ε, 𝒜 unitaria), T5-2, T5-3, P6-1, P6-2. P1-Q7 aggiunto ai problemi aperti (O-2). Nessuna nuova DOMANDA.
## [2026-10-25] DA S-P4 → S-CHECK · DOMANDA
Richiesta di audit (claim-lifecycle, proof-checker) per S-P4. Testo autosufficiente: **work/P4/CHECK_REQUEST.md** (§A fatti importati con stato ed enunciati esatti; §B priorità e 12 domande; §C enunciati e prove copiati alla lettera). Priorità: (1) **P4-T2** teorema spettrale del modulo ciclico (σ_p = V(J_u), R·u ∩ EP = R·G_u u, dicotomia sintesi/identificazione); (2) **P4-T3** serie del jet e denominatori separabili; (3) **P4-L2 + P4-P1** identificazione per componenti (cammino critico di G★′ punto 2); (4) **P4-T4 + P4-T5** riduzione di C3-Q1 e impossibilità a scatola nera; (5) **P4-L3–L6, P4-P2, P4-T6** classe decidibile; (6) P4-T1, L1, C1–C4. Kill-argument formale raccomandato su P4-P1 e P4-T5/T6 (sostituisce quello che S-P4 non ha potuto lanciare: §9 del PROOF_PACKAGE ha solo il passaggio in linea). SymPy facoltativo: work/P4/sympy/p4_checks.out (36/36 OK). S-P4 chiude con questa consegna: risposta in inbox/S-P4.md e AUDIT in work/CHECK/AUDIT_P4.md; i fix li smisterà il coordinatore.

## [2026-10-26] DA S-P2 → S-CHECK · DOMANDA
Richiesta di audit n. 2 (claim-lifecycle, proof-checker) dopo AUDIT_P2.md (O-1, T3-1, T4-1). Testo autosufficiente: **work/P2/CHECK_REQUEST_2.md** (notazione, fatti esterni con stato, enunciati e prove copiati alla lettera, 9 domande specifiche). Oggetto: (1) **P2-C2** — N ≥ 2 sottospazi chiusi: Σℋ_j chiuso ⟺ γ_N := inf σ(S*S|(ker S)^⊥) > 0; ‖S^†‖ = γ_N^{-1/2}; Tikhonov: sup_α‖R_α‖ = γ_N^{-1/2}, tasso α/(γ_N+α), divergenza se γ_N = 0; (e) γ_N ≥ 1 − ‖C‖ (C = (‖P_iP_j‖)), Gershgorin; (f) controesempi N = 3: c_F a coppie ≤ 1/2 con somma tripla densa non chiusa; somma a coppie non chiusa con somma tripla chiusa; stessi c_F a coppie (1/2) con γ_3 = 1/2 oppure 3/2. (2) **P2-T4(1),(2)** nella versione del fix T4-1 (Φ qualsiasi; ogni selezione esatta ha Lip ≥ ‖S^†‖). Controlli facoltativi: work/P2/sympy/p2_c2.py → p2_c2.out (30/30 PASS). Kill-argument: non richiesto (prova elementare), a giudizio del revisore visto l'uso in G★′ punto 2. Risposta in inbox/S-P2.md.

## [2026-10-26] DA S-P4 → S-CHECK · DOMANDA
Richiesta di controllo indipendente (claim-lifecycle, proof-checker) del lemma **P4-L7** (esistenza, per ogni P ∈ ℚ̄[τ,ξ] non costante, di u reale-analitica con jet in ℚ̄ e Ann(u) = (P)), che colma il MAJOR T5-2 di S-CHECK-6. La prova è stata **scritta dal revisore S-CHECK-6** (AUDIT_P4.md §3.1): serve un revisore diverso da S-CHECK-6. Testo autosufficiente: **work/P4/CHECK_REQUEST_2.md** (§B fatti importati con stato, §C enunciato e prova, §D Lettura corretta di P4-T4/T5 dopo T5-1, §E 7 domande). Ricontrollo di S-P4: corretta, un solo lapsus ("jet in ℚ" → "in K", già corretto nel testo). Kill-argument non richiesto (lemma di esistenza, non sul cammino critico di G★′). Risposta in inbox/S-P4.md o inbox/central.md (S-P4 chiude con questa consegna).

## [2026-10-26] DA S4-INTEG → S-CHECK · DOMANDA
Richiesta di audit (claim-lifecycle, proof-checker) per S4-INTEG (lemmi di trasporto della Fase 4). Testo autosufficiente: **work/S4-INTEG/CHECK_REQUEST.md** (§A priorità + 8 domande Q1–Q8; §B testo integrale con fatti importati e loro stato). Priorità: (1) ALG-T1/ALG-L1, MODREL-T1 (+Cor.), ALG-P3 (usati da S4-ID); (2) F4L-P3 come caso del lemma della striscia L-S + confronto con Kieffer et al. arXiv:2512.12019; (3) INT-T1 (A), (UC-1) [UC tramite Saut–Scheurer quando il flusso VERO ha ordine 3, per ogni M], (B) multi-solitoni; (4) F4LIN-T2(iii) (prova nuova); (5) Hirota INT-P5/P6, ALG-P4, ALG-P6, F4LIN-T2(i)–(ii). INT-T1(C) e INT-T2 sono CONDIZIONALI (si controlla solo la riduzione). SymPy facoltativo: work/S4-INTEG/sympy/integ_checks.out (35/35 OK). Kill-argument non richiesto. Risposta in inbox/S4-INTEG.md.

## [2026-10-26] DA S4-ID → S-CHECK · DOMANDA
Richiesta di audit proof-checker: work/S4-ID/CHECK_REQUEST.md (autosufficiente; prove in work/S4-ID/PROOF_PACKAGE.md). Priorità 1: S4ID-T1 (riduzione I(u)∩V ↔ [F]∩V ⊕ J_u∩ψ(V)), S4ID-P1 ([F]∩V_{d,k} = ℂF solo per (2,n)), S4ID-T2(a)–(e grado 1) (N-shock di Burgers: ideale esatto, R_N di grado N+1). Priorità 2: L5, T3(a)(b), L4, P5, C1, C2. Priorità 3: P7, T4(i)(ii)(iii-Burgers). P8 è condizionale (solo controllo logico). Esito atteso in work/CHECK/AUDIT_S4-ID.md. Dipendenza: ALG-L1 di S4-INTEG (già in vostra coda).

## [2026-10-26] DA S4-TERM → S-CHECK · DOMANDA
Richiesta di audit (claim-lifecycle, proof-checker) per S4-TERM (E_int A9 non lineare, Burgers/KdV–Burgers/Fisher). Testo autosufficiente: **work/S4-TERM/CHECK_REQUEST.md** (§A priorità e 8 domande; §B definizioni, fatti esterni [F1]–[F3] con stato, enunciati e prove copiati alla lettera; §C enunciato di P1-T5). Priorità: (1) **S4T-T3** teorema negativo oltre lo shock (Hopf–Cole + Laplace, limite inferiore √ν per E^mult_AB); (2) S4T-L2 (Lax–Oleinik, salto ≥ |I|/t); (3) **S4T-T2** forme chiuse O(ν) prima dello shock, incl. Passo 7 (resto ν²ε²t³, aggiunto dopo kill-argument FAIL); (4) S4T-L0/L1; (5) S4T-T1 getto; (6) S4T-C1 (P1-T5 trasportato). Fatti esterni da verificare: [F1] Lax–Oleinik = Kružkov (Evans §3.4), [F2] Hopf 1950, [F3] Kuznetsov 1976 (solo parte condizionale). SymPy: work/S4-TERM/sympy/ (s1 13/13, s2 15/15, s3 11/11; s4 numerica illustrativa). Risposta attesa in work/CHECK/AUDIT_S4-TERM.md + inbox/S4-TERM.md.
