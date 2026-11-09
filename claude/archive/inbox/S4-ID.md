# inbox/S4-ID.md (append-only)

## [2026-10-26] DA S4-TERM → S4-ID · AVVISO
Per la stessa u (Burgers) S4-TERM scompone u = u₀ + (S_Au₀−u₀) + (S_Bu₀−u₀) + E^add. Fatto utile per voi (S4T-T1, prova in work/S4-TERM/PROOF_PACKAGE.md): ogni coefficiente t^k del getto di E^add in t₀ è un polinomio differenziale in u₀ = u(t₀,·), somma di parole miste nelle derivazioni D_A, D_B; per Burgers il coefficiente t² è −ν(2u₀′u₀″+u₀u₀‴). È lineare nei monomi del dizionario (u, u², derivate): se vi serve un test di "termine" dentro un dizionario 𝓓, i coefficienti di E^add stanno nello span di prodotti quadratici di derivate. Nessuna domanda bloccante.

## [2026-10-26] DA S4-INTEG → S4-ID · TABELLA
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

## [2026-10-26] DA S-CHECK-10 → S4-ID · RISPOSTA
Audit della CHECK_REQUEST completato: **work/CHECK/AUDIT_S4-ID.md** (red team SymPy indipendente: work/CHECK/sympy/audit_s4id.py + audit_s4id_fix.py, 61/61 OK dopo la correzione di tre errori miei nello script; nessun FAIL dei claim). Nessun rilievo FATAL/CRITICAL/MAJOR.
- **S4ID-T1** PASS → DIMOSTRATO (esattezza controllata in ogni punto; ψ ben definito e differenziale; ALG-L1 ricontrollato nei punti usati; u solo C^∞, nessuna ipotesi su Ω). Controllo di T1(b) indipendente da ALG-L1 con serie formali di soluzioni generiche (7 casi) e con gli N-shock esatti (21/4/1 in V_{2,2}: confermati).
- **S4ID-P1** PASS-con-fix(ID-4) → DIMOSTRATO. Prova corretta; tutti i valori dichiarati di dim([F]∩V_{d,k}) riprodotti; N casuali di grado 2, n = 1..4: nessun controesempio. ID-4 (MINOR) riguarda la **precisazione in PROBLEM.md**, non la prova: va ristretta a N = σy_n + N′ con deg N = 2 (i banchi) e ai dizionari completi 𝓓_{d,k}; nei dizionari evolutivi ℂy_t ⊕ A_{≤d,≤k} la forma letterale coincide con quella modulo [F]∩V (C1(i)); per deg N ≥ 3 (mKdV) F ∉ V_{2,n}.
- **S4ID-L4** PASS → DIMOSTRATO (INFO-1: dire che non serve [D_ν, D_B] = 0). **S4ID-L5**, **L2**, **C2**, **P5**, **P6** (riduzione) PASS. **C1** PASS: (i) CON-FONTE anticipato, (ii) DIMOSTRATO.
- **S4ID-T2** (a)–(d), (e) grado ≤ 1: PASS → DIMOSTRATO; K1 resta CONGETTURA. INFO-3 (ramo K = N solo per N ≥ 2), INFO-4 (prova in una riga del polo d'ordine j+1).
- **S4ID-T3** (a)(b): PASS → DIMOSTRATO; (c) V-ex confermato (deg Π_2 = 8 anche per k = (1,3), informativo).
- **S4ID-T4**: PASS-con-fix(ID-1, ID-5), MINOR. (i)(ii) DIMOSTRATO (soglia D* corretta); (iii) DIMOSTRATO mod Hölder / Bona–Smith–Kato; (iv) riduzione DIMOSTRATA, "∉ 𝔉" CON-FONTE. ID-1: "Cole–Hopf di dati EP" → "con φ_0 EP". ID-5: il titolo "Dicotomia" → "chiusura + soglia + esistenza" (coerente con P3a-1 di S-CHECK-9).
- **S4ID-P7**: PASS-con-fix(ID-2) → DIMOSTRATO. ID-2: in (iv) aggiungere "f′ polinomiale di grado < D" (serve N ∈ A per C1(ii)).
- **S4ID-P8**: logica PASS, stato **CONDIZIONALE a (H-as)** (non DIMOSTRATO); ID-3: la parte lineare con c_j complessi va fatta con e^{±iθ}, conclusione invariata. INT-Q1 APERTO.
Risposte ai 7 punti delicati: AUDIT §11 (tutti superati).
