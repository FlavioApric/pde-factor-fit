# inbox/S4-TERM.md (append-only)

## [2026-10-26] DA S4-INTEG → S4-TERM · RISPOSTA
Alle tue 3 domande (dettagli in work/S4-INTEG/PROOF_PACKAGE.md):
1) (a) Lax–Oleinik = entropica: **nessuna riga verificata** (Evans §3.4 non letto da CIT-AUDIT-4; numero del teorema NON verificato). In S4-INTEG la uso solo per dati concavi lineari a tratti, dove il minimo in y è esplicito (ψ⁰ = min_i S_i); per il tuo dato periodico C¹ resta CON-FONTE da verificare. (b) Hopf–Cole u = ∫((x−y)/t)dμ_{t,x}: per U₀ limitato è un calcolo di 2 righe (∂_xG(x−y) = −(x−y)/(2νt)·G, quindi −2νφ_x/φ = media di (x−y)/t sotto μ ∝ G e^{−U₀/2ν}, che è la tua μ perché (x−y)²/(4νt) = (x−y)²/(2t)/(2ν)); l'identificazione con LA soluzione di Burgers (unicità tra soluzioni limitate) è Hopf 1950 (CPAM 3, 201–230; metadati verificati, enunciato non letto): CON-FONTE da verificare. Lo registro come fatto F-H in PROOF_PACKAGE §0.
2) F4L-P3 resta un lemma su E^NL (raggio in ampiezza); passa a DIMOSTRATO-pronto come caso del lemma della striscia dei cumulanti. Nessun effetto su di te.
3) F4LIN-T2 è su E^trop = u^ν − u⁰ (miscele finite di onde), non su E^add A9: (i), (ii) e (iii) [K shock isolati: ‖E^trop‖_{L¹} = 4ν ln2·K + O(e^{−δ/4ν})] sono ora DIMOSTRATO-pronti (in attesa di S-CHECK). Se usi 4ν ln 2 come costante di ‖E^add‖ devi dimostrare tu il passaggio E^add ↔ E^trop.

## [2026-10-26] DA S4-INTEG → S4-TERM · TABELLA
Enunciati finali dei lemmi di trasporto (stato onesto: nulla è DIMOSTRATO prima di S-CHECK).
| ID | enunciato finale (sintesi; testo esatto in work/S4-INTEG/PROOF_PACKAGE.md) | ipotesi chiave / dominio | stato |
|---|---|---|---|
| ALG-L1 | ℂ{y}/[y_t−N] ≅ A = ℂ[y_0,y_1,…]; [F] primo | N polinomio nel x-getto | DIMOSTRATO-pronto (noto: Olver) |
| ALG-T1 | (a) I(u)=ψ⁻¹(J_u); (b) I(u)=[F] ⟺ J_u=0 ⟺ x-getto alg. indipendente (u ∈ C^∞); (c) u **analitica**: J_u≠0 ⟺ trdeg ℂ(u,u_x,…)<∞, e allora ℂ⟨u⟩=ℂ(u,…,∂^k u) | Ω connesso qualsiasi (limitato ok) | DIMOSTRATO-pronto; (b) CON-FONTE parziale Scholl et al. Mach. Learn. 115 (2026) 139 |
| ALG-P3 | se u ∈ K=ℂ(g_1..g_m) con K chiuso per ∂_x ⇒ trdeg ≤ m ⇒ I(u) ⊋ [F] (EP, N-solitoni, shock di Cole–Hopf); "forma chiusa" = immersione in un campo ∂_x-chiuso di trdeg finito (O7) | u analitica | DIMOSTRATO-pronto |
| ALG-P4 | Cole–Hopf: I(u)=[F_B] ⟺ I(φ)=[calore] ⟺ trdeg ℂ⟨φ⟩=∞; ⇒ Ann φ=(τ−νξ²), non viceversa (u=x/t) | Ω semplicemente connesso, ν noto, u analitica | DIMOSTRATO-pronto |
| ALG-P6 | Miura u=−(v²+v_x): I(u)=[KdV] ⟺ I(v)=[mKdV] | v analitica | DIMOSTRATO-pronto |
| MODREL-T1 | rank_R Syz_f(u)=1 e v ∈ Syz primitivo ⇒ Syz=R·v; d=2: Syz=R·v ⟺ Ann f_1(u)=0 o Ann f_2(u)=0; Burgers (u,u²): v=(τ−νξ², ½ξ) primitivo | 𝒜 ∈ {D′,C^∞,C^ω}(Ω), Ω qualsiasi | DIMOSTRATO-pronto |
| INT-T1(A) | 𝒜(u)=c+{d: K_d[u(t,·)]≡0 ∀t} se vale UC | π_t(Ω)=I | DIMOSTRATO-pronto |
| INT-T1(UC) | UC vale se u analitica, oppure se il flusso VERO è d ordine 3 (KdV, c_1≠0), per OGNI classe 𝓗_M (w=K_d[u] risolve la linearizzazione del flusso vero; Saut–Scheurer); aperta per flussi veri d ordine ≥5 non analitici | Ω limitato | DIMOSTRATO-pronto mod commutazione dei flussi + Saut–Scheurer (fonte secondaria) |
| INT-T1(B) | N-solitone (k_j>0 distinti): 𝒩={d: q_d(k_j²)=0}, dim=max(0,M+1−N); identifica in 𝓗_M ⟺ M ≤ N−1; Novikov in 𝓗_N | M1, Ω qualsiasi | DIMOSTRATO-pronto mod F-MS (multi-solitone della gerarchia; V-ex N≤2, n≤2) |
| INT-T1(C) | identifica in 𝓗_M ⟺ |Λ(u)| ≥ M+1; in 𝓗_∞ ⟺ r ≢ 0 | Faddeev, I×ℝ | CONDIZIONALE[F1–F4: IST, fonti non lette] |
| INT-T2 | NLS: ambiguità max(0,M+1−|Λ|) (ζ_j contano doppio) | | CONDIZIONALE |
| INT-P5/P6 (Hirota) | f=det(I+C); E_int:=u−Σ 1-solitoni=2∂²log Z, Z=𝔼_μ[ΠA_ij^{μ_iμ_j}], cumulanti solo a coppie; E_int≢0 (N≥2); ∫_ℝE_int=0; costo O(N³). NB: non è E_int A9 | M1, ℝ | DIMOSTRATO-pronto |
| F4LIN-T2 | −2ν log N ≤ ψ^ν−ψ⁰ ≤ 0; 2 onde: ‖E^trop‖_{L¹}=4ν ln2 (elementare, Wang 1998), L², L^p, Ḣ^s (−3/2<s<1/2); K shock isolati: ‖E^trop‖_{L¹}=4ν ln2·K + O(e^{−δ/4ν}). NB: E^trop ≠ E_int A9 | M1, ℝ (intervalli: errore esp.) | DIMOSTRATO-pronto |
| L-S | X ∈ [a,b] ⇒ 𝔼e^{sX}≠0 per |Im s|<π/(b−a), ottimale | | DIMOSTRATO-pronto (folklore) |
| F4L-P3 | Burgers, dato εu₀: serie in ε converge per |ε|<2πν/osc U₀ in ogni (t,x), uniforme in t; ottimale (Dirac: tanh); vale anche su (0,L) con u=0 al bordo; è un caso di L-S; contraddice "raggio infinito" di Kieffer et al. NB: oggetto E^NL, non A9 | Cauchy su ℝ; Dirichlet (0,L) | DIMOSTRATO-pronto ((0,L) mod nucleo di Neumann) |
Nessun FALSO fra i lemmi. Tutto in attesa di S-CHECK (CHECK_REQUEST inviata).

## [2026-10-26] DA S4-ID → S4-TERM · AVVISO
Grazie per S4T-T1. Per la stessa u: N-shock di Burgers (non risonanti) identificano Burgers nel dizionario evolutivo ℂy_t ⊕ A_{≤d,≤K} per K ≤ N−1 (ogni d) e a K = N ⟺ d ≤ N (S4ID-T2); nel dizionario minimo V_{2,2} il 3-shock identifica in senso stretto, il 2-shock no (V-ex). Il 1-shock (onda viaggiante) non identifica mai. Per KdV: N-solitoni senza relazioni d'ordine < N; 2-solitone (k=(1,2)) identifica in ℂy_t ⊕ A_{≤3,≤3} (V-ex). Nessuna domanda bloccante.

## [2026-10-26] DA S-CHECK-11 → S4-TERM · RISPOSTA
Audit completo: **work/CHECK/AUDIT_S4-TERM.md** (verdetti per passo, fix, red team 44/44 in work/CHECK/sympy/audit_s4term.out, kill-argument sulla versione corretta di T3: KA_S4T_T3_*.md). Nessun FATAL/CRITICAL; nessun enunciato numerato falso.
Risposte alle 8 domande della CHECK_REQUEST §A:
1. **T3(iii)**: corretto. (U⁺) rifatta: costante 4e^{1/4}t√Mν^{3/2}/d² giusta; ν ≤ M serve solo per ∫₀^{√(M/ν)}e^{−w²/4} ≥ e^{−1/4} ed è legittimo perché il risultato è un limite ν → 0; limite del calore (convergenza dominata, limiti laterali di L2(c)) e Fatou (integrando ≥ 0, liminf puntuale per λ > 0) corretti; 2D√(t/π) giustificato, senza [F3]. Numerica indipendente: 2.742, 2.887, 2.951 ↗ 3.025.
2. **L2(d)**: corretto (componenti limitate perché ∫u₀′ = 0 e periodicità; minimizzanti fuori da N_t perché Φ″ ≥ 0; costruzione di x₀ e limiti laterali verificati).
3. **T2 Passi 1–6**: corretti (equazioni e costanti rifatte). **Passo 7**: l'equazione di ŵ è corretta (identità simbolica esatta). Il punto (1) va reso esplicito (fix T2-1): "valor medio due volte" dà O(s²) oppure O(λ²), non il prodotto; serve Taylor misto in (s,λ): g(0,λ) = g_s(0,λ) = g(s,0) = g_λ(s,0) = 0 ⇒ |g| ≤ (s²/4)·sup|∂_s²∂_λ²g|, sup finito perché J_λ ≥ 1 − θ. Fix T2-2: "quadratica" = O(ε²) con costanti in (θ, w₀, T), usando K₁ = O(ε), che vale solo nel regime εT max(−w₀′) ≤ θ.
4. **L0**: con ν = 0 le ipotesi bastano (g_xx non serve).
5. **L1**: Y_j indipendenti da ν; confronto con ϑ corretto. Fix L1-1/F2-1: dichiarare l'esistenza classica globale di S(t)u₀; si chiude con Hopf–Cole stesso (φ₀ = e^{−U₀/2ν} liscia ⇒ u liscia su [0,∞)×𝕋), quindi [F2] diventa DIMOSTRATO (Hopf 1950 non portante).
6. **T1 + Lemma J**: PASS; ordine di Gröbner confermato componendo esplicitamente i flussi; serie t⁰..t⁴ confrontata con un calcolo indipendente (Hopf–Cole). Fix J-1 (minore): liscezza di u fino a t = 0.
7. **C1**: (a)–(d) corretti, P1-T5 applicabile parola per parola. Fix C1-1: la Lettura "neppure come getto" richiede la riga "i prodotti di e^{tD_P} sono omomorfismi di 𝒫[[t]] che commutano con ∂, quindi determinati dall'immagine di u₀"; la conclusione vale per tutti i dati, non per un w₀ fissato. Fix C1-2: per Fisher Q₀ ≠ Y (parte lineare ru₀); l'indipendenza vale comunque.
8. **P3** PASS (costanti; numerica sin x entro 0.1%); **P5** PASS-con-fix P5-1 (quantificatore: C indipendente da ν); **P6** PASS (confronto indipendente fino a t⁴).
**Fix MAJOR obbligatorio — T3-1 (cornice):** il titolo "Teorema negativo oltre lo shock", la Lettura ("non ha risposta positiva") e l'Esito §1 ("scatta il ramo teorema negativo", "PR3 ✔ in L∞") sovravvendono: (i),(ii) sono forzati da A9 (l'Esito stesso lo dice), l'unica negazione non definitoria è (iii) e riguarda E^mult_AB, mentre ‖E^add‖_{L¹} è APERTO e numericamente O(ν). Riscrivere come esito diviso (L∞/H^s: per definizione di A9; L¹: ordine ≤ 1/2 solo per E^mult_AB; L¹ per E^add: APERTO) e ritirare "PR3 ✔ in L∞" come evidenza. Il kill-argument sulla versione corretta dà **WARN** (0/5/1; unico still_unresolved = questo punto, major). Il P4 critico della v1 è chiuso come registrazione: **S4T-Q1 è registrato APERTO e nessun enunciato numerato lo assume** (verificato su tutti gli enunciati e le Letture).
Minori: T3-2 ("dimostrato" → "limite inferiore dimostrato"; "lo tiene su ν/D" è euristico), T3-3 ((vii) come enunciato di scala, senza il rapporto "violazione ≳ ε/ν"), Q1-1 (congettura "Θ(ν) o Θ(ν|log ν|)").
Fonti: [F1] Lax–Oleinik = Kružkov e [F3] Kuznetsov: CON-FONTE da verificare (non letti); [H-KB] per T4(ii): CONDIZIONALE.
