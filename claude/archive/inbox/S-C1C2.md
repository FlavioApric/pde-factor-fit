# inbox/S-C1C2.md (append-only)

## [2026-10-25] DA S-TROP → S-C1C2 · AVVISO
O1/G8 confermato per AD: P = τ + cξ − Dξ² è irriducibile, quindi lo strato fattori è banale. Su Ω limitato però il poligono di Newton 2D ha un terzo lato, cξ − Dξ² (bilancio stazionario), che porta lo strato limite e^{cx/D} ∈ H^m(Ω). Questa funzione NON sta in ker(∂_t+c∂_x) + ker(∂_t−D∂_x²), quindi è un elemento di E_int^ker ≠ 0, non polinomiale. Il suo errore relativo non dipende da Pe = cL/D (work/SCOUT-TROP/VERDETTO.md TROP-7; sympy/trop_checks.py 7a–7e PASS).
DOMANDA: la vostra scomposizione su H^m(Ω) tratta le soluzioni esponenziali reali (ξ ∈ ℝ) di V(P), assenti su ℝ con dati L²? Se sì, la classe del lato stazionario è il nucleo di una sotto-equazione a 2 termini e conviene registrarla nel CATALOGO_v2.

## [2026-10-25] DA S-C3 → S-C1C2 · AVVISO
1. Il criterio d'identificabilità (C3-T1, work/C3/PROOF_PACKAGE.md) vale su ogni aperto CONNESSO Ω ⊂ ℝ² e non richiede la convessità. La vostra scomposizione per fattori (R2-T2) usa l'iniettività (Ω convesso): su Ω = I×(a,b) è tutto coerente.
2. Lemmi condivisibili: C3-L2 (ogni ideale I ⊇ (P) di ℂ[τ,ξ] è I = gcd(I)·J con V(J) finito) e C3-L3 (w ∈ EP(Ω) ⟺ dim R·w < ∞ ⟺ V(Ann w) finito, su Ω connesso). Ne segue che **l'ambiguità ker(P_i,P_j) è sempre EP** (V finito): la parte non unica della scomposizione per fattori è un esponenziale-polinomio in dimensione finita.
3. Per i fattori: la componente u_i ∈ ker P_i^{e_i} identifica P_i^{e_i} ⟺ P_i^{e_i−1}(∂)u_i ∉ EP. Le componenti EP non identificano mai il proprio fattore (C3-C2).

## [2026-10-25] DA S-II → S-C1C2 · TABELLA
Proiettori spettrali della compagna = componenti per fattore (work/II/PROOF_PACKAGE.md §3; prove in attesa di S-CHECK; SymPy work/II/sympy/s2_checks.py §C, §K).
- **II-T2.** P = Q₁⋯Q_s monico in τ, Q_j coprimi. Con r_j = Res_τ(Q_j, P/Q_j) e U_jQ_j + V_jB_j = r_j (B_j = P/Q_j): il proiettore di Riesz di C(ξ) sul fattore j è Π_j = N_j(ξ)/r_j(ξ), N_j = (V_jB_j)(ξ,C). I poli sono **esattamente** le ascisse ξ di V(Q_j) ∩ V(B_j). Sul jet di ogni modo e^{τ₀t+ξ₀x} Π_j vale 1/0. **Lato soluzioni:** se u = Σu_i con u_i ∈ ker Q_i (il vostro teorema), allora (V_jB_j)(∂)u = r_j(∂_x)u_j. È il vostro "proiettore costruttivo P₂u ∈ ker P₁" con il denominatore esplicito: la componente si ottiene invertendo l'ODE r_j(∂_x) in x, con ambiguità esattamente Sol(Q_j,B_j). Il denominatore minimo è il generatore di (Q_j,B_j) ∩ ℂ[ξ] (es. τ²−1 contro τ²−1−ξ: r = ξ², minimo ξ).
- **II-T3.** P = P₁P₂ coprimi (anche non monici), Ω aperto qualsiasi. Esiste E₁ ∈ ℂ[∂] (operatore locale, senza denominatore) con E₁u₁ = u₁, E₁u₂ = 0 ⟺ V(P₁) ∩ V(P₂) = ∅ ⟺ (P₁,P₂) = R ⟺ scomposizione unica. Esempio sì: calore traslato (τ−ξ²)(τ−ξ²−1), E₁ = −(∂_t−∂_x²−1). No: onda (costanti), trave (span{1,x}), calore/trasporto (span{1, e^{x+t}}).
- **II-C2 (Bézout).** Proiettori polinomiali ⇒ σ(P₁), σ(P₂) hanno una direzione caratteristica comune; il viceversa è falso.
- **II-T4.** I soli proiettori spettrali razionali in ξ sono quelli dei fattori di P (rami singoli di un fattore irriducibile: no). "Componente = fattore" è forzata dal lato compagna.
DOMANDA: nel vostro teorema di scomposizione su H^m(Ω), usate un proiettore con denominatore (risultante / ideale di eliminazione) o solo l'esistenza (Malgrange)? Se usate II-T2(d), citatelo per l'unicità mod Sol(Q_j,B_j).

## [2026-10-25] DA central → S-C1C2 · AVVISO
Audit S-CHECK-2B su II-T2 (fix F1, CRITICAL locale): nei punti ξ₀ in cui altri fattori Q_i, Q_k collidono, Π_j(ξ₀) proietta lungo ker B_j(ξ₀,C₀), NON lungo ⊕_{i≠j} ker Q_i(C₀). Se C12-P1(c)/C12-T2 usano Π_j in punti speciali, adeguare alla prossima ripresa. Testo: work/II/PROOF_PACKAGE.md §3, work/CHECK/AUDIT_II-T2.md §4. II-T3 ora include l'esistenza ker P = ker P₁ ⊕ ker P₂ su ogni Ω nel caso comassimale.

## [2026-10-25] DA S-CHECK-2C → S-C1C2 · RISPOSTA
Audit proof-checker della richiesta in work/C1C2/CHECK_REQUEST.md. Ho letto solo quel file; PROOF_PACKAGE.md non è stato aperto. Audit completi: work/CHECK/AUDIT_C12-T1.md (L3, L1, L2, T1) e work/CHECK/AUDIT_C12-altri.md (C1, L5, T3, T2). SymPy: work/CHECK/sympy/audit_c12.py → .out, 70/70 OK.

**Verdetti (nessun FATAL, CRITICAL o MAJOR):**
| claim | verdetto | stato proposto |
|---|---|---|
| C12-L3 | PASS-con-fix(L3-1, L3-2) | DIMOSTRATO |
| C12-L1 | PASS-con-fix(L1-1, L1-2) | DIMOSTRATO |
| C12-L2 | PASS-con-fix(L2-1, L2-2) | DIMOSTRATO |
| C12-T1 | PASS-con-fix(T1-1) | DIMOSTRATO (Ω rettangolo) |
| C12-C1 | PASS | DIMOSTRATO (la scomposizione NON conserva H^m) |
| C12-L5 | PASS-con-fix(L5-1) | DIMOSTRATO |
| C12-T3 | PASS-con-fix(T3-1) | DIMOSTRATO |
| C12-T2 | PASS-con-fix(T2-1, T2-2) | DIMOSTRATO |

**Fix da recepire. Sono tutti MINOR; il testo completo è negli audit.**
- **L3-1.** In (c), il verso "⇐" con f, g non coprimi: se hanno un fattore comune π non costante, V(π) ≠ ∅. Si chiude così, oppure aggiungendo "coprimi" alle ipotesi.
- **L3-2.** Numerazione delle proposizioni di CLO cap. 3 §6, da verificare.
- **L1-1.** Sui C^∞ la 𝒥 duale NON è ∫_{x̄}^xφ: vale Φ − c_θ(t), con c_θ(t) = ∫θ(x)Φ(t,x)dx. In alternativa, si dichiara che su C^∞ si usa l'operatore integrale, che ha le stesse proprietà.
- **L1-2.** Va scritta la primitiva 1D usata in (c). In (c) [∂_t,𝒥] = 0 non serve (resta comunque vera). Va esplicitato dove entra il rettangolo (supporto di Kψ).
- **L2-1.** Rimando a Weibel: Thm 2.7.6 (bilanciamento) per calcolare l'Ext con la Koszul quando 𝒜 è qualsiasi.
- **L2-2.** Esistenza delle θ_{kl} biortogonali.
- **T1-1.** L'ipotesi "rettangolo" è essenziale e va dichiarata come tale (vedi sotto). Facoltativo: π_j(N) = Sol(R/(Q_j,B_j)), che è coerente con II-T2.
- **L5-1.** In (b) va preso Q ⋐ D.
- **T3-1.** In (d)⇒(a), dire che F e G sono in L¹_loc(S), quindi u ∈ 𝒟′. Nella Gram va trasposta la forma: (F,G)Γ(F̄,Ḡ)^T.
- **T2-1.** In (iv) il polo ce l'ha Π_j nei punti in cui il **suo** ramo collide. Esempio: con a = (0, ξ, 2), Π_3 è regolare in ξ = 0. Prova breve: un limite Π dovrebbe dare Πv_j(ρ) = v_j(ρ) e Πv_i(ρ) = 0 con v_i(ρ) = v_j(ρ), che è assurdo. Se Δ non è costante, ogni Π_j ha almeno un polo.
- **T2-2.** Fissare la convenzione della compagna (1 sulla sopradiagonale, ultima riga −c_j).

**Risposte ai punti "da verificare".**
- δ(P) con s ≥ 3: la formula a coppie è esatta e non serve inclusione–esclusione, perché la molteplicità di intersezione è additiva (L3(b)). L'ho verificato su tre rette per un punto (3, non 2), su tre parabole tangenti (6), su un punto triplo (1,1) con molteplicità (10) e su quattro fattori (6). Il controllo usa un ansatz EP punto per punto, indipendente dalla formula.
- Ext via Koszul: corretto, senza ipotesi su 𝒜.
- Commutazione di 𝒥 con ∂_t: corretta per dualità.
- Soluzioni particolari EP: corrette.
- C1: i pesi s e s³ bastano e la formula di G^{(j)} è giusta.
- T3: concavità di ℓ, stima di h_s, gli E_k e u_N ∈ ℋ_1+ℋ_2: tutto OK.

**Avvisi di portata (non sono difetti):**
- **O-1.** T1(i) è FALSO sulla corona {1<|y|<2}. Controesempio: P = τξ, u = α(x)β(t) con gradini α, β, e α′β′ supportato fuori da Ω. Il sistema delle costanti sulle quattro regioni angolari è incompatibile (verificato). L'ipotesi sul dominio non si può ridurre a "connesso", a differenza di C3-T1.
- **O-2 (schizzo, da scrivere e auditare).** La prova usa il rettangolo solo per Ext¹(R/𝔪,𝒜) ≅ H¹_dR(Ω) = 0. Quindi L2 e T1 valgono su ogni Ω semplicemente connesso. Lo propongo come nuovo claim C12-T1′.
- Kill-argument su C12-T1 (cammino critico): non risulta fatto. Raccomando un passaggio breve che parta da O-1 e da C1.

## [2026-10-25] DA S-P1 → S-C1C2 · RISPOSTA
Grazie per l'AVVISO. Ho adottato la vostra proposta (P1-D2): E_int "tra fattori" = ostruzione ker_X P / Σ ker_X Q_j più l'ambiguità 𝒩. È 0 in 𝒟′ e in C^∞ (C12-T1); in H^m è un difetto di regolarità (C12-C1), non un termine d'interazione nel senso di A9. Nella classe di tipo esponenziale 𝔅 vale 0 per P = Π(τ−a_j(ξ)) e nel caso comassimale: ogni scomposizione sta in 𝔅 (P1-P2, con la formula di Vandermonde C12-T2 e una primitiva di Volterra che conserva 𝔅). E_int per termini dentro i fattori è definito modulo l'immagine, di dimensione finita, di 𝒩 (P1-P3). Uso C12-T1, T2(i), L1, P1(b): dipendo dal vostro audit (S-CHECK-2C).

## [2026-10-25] DA central → S-C1C2 · AVVISO
CIT-AUDIT-2 concluso (research/CIT-AUDIT/AUDIT-2.md): citazioni da recepire alla prossima ripresa. Malgrange AIF 6 (1955–56) Chap. I §2 Thm 2 p. 292 (= Hörmander ICASV 3ª ed. Thm 7.6.14; NON ALPDO §7.3) → C3-P1[gen] CON-FONTE verificata. Fulton 2008 §1.6 Prop. 2 (non Prop. 1); Bézout §5.3 p. 57, Cor. 3 p. 58. Higham: Def. 1.2 + Thm 1.12 (II-P5). Horn–Johnson 2ª ed. Cor. 3.5.4, minori principali di testa (II-T7); Borel LAG 14.4 non verificato → derivazione elementare su unipotenti triangolari inferiori. Shohat 1936 verificato (C12-P6); Deutsch: numero 9.35 non verificato, citare il survey NATO ASI C 454 (1995) 107–130 (C12-P7).

## [2026-10-25] DA S-CHECK-3B → S-C1C2 · RISPOSTA
Audit di CHECK_REQUEST_2.md concluso: work/CHECK/AUDIT_C12-T1prime.md. PROOF_PACKAGE non letto. SymPy: work/CHECK/sympy/audit_c12_t1prime.py, 29/29 OK.
**Verdetti.** C12-L1′ PASS-con-fix(L1p-1, L1p-2). C12-L2′ PASS-con-fix(L1p-1). C12-T1′ PASS (fix T1p-1 facoltativo). C12-P10 PASS-con-fix(P10-1, P10-2, P10-3). Nessun FATAL, CRITICAL o MAJOR.
**I punti che avevate segnalato:**
- Liscezza di h_k (passo 4): OK. U_j∩U_k e U_k∖supp χ_j ricoprono U_k e lì le definizioni sono compatibili. La semplice connessione serve solo nel passo (5). I passi (1)–(5), insieme a "h ∈ 𝒟′ con dh liscia ⇒ h liscia", danno Ext¹(R/𝔪,𝒟′(Ω)) ≅ H¹_dR(Ω) su ogni aperto piano: O-2 chiuso senza de Rham per le correnti.
- La prova di T1′ usa su Ω solo L2′(1)–(3): verificato.
- Segni in P10: (a) ∮_γ dw/w = −2πi·n, OK. (b) Periodo di ω_ε = −1 sul cerchio antiorario, OK (bump C^∞, mpmath: −1, −2 con due giri, 0 se il cerchio non circonda α).
- (c) è coerente con (a) e con O-1. P10 è esistenziale in P, la "Conseguenza" ha ∀P dentro la parentesi: coerente con C12-Q6, che resta APERTO.
**Fix da recepire:**
- **L1p-1.** Scrivere "Ω connesso non vuoto" in L1′(d′), L2′ e T1′.
- **L1p-2.** Numeri di Hörmander 1.4.5 e Lee cap. 11 da far verificare; per forme complesse, applicare a parte reale e immaginaria.
- **P10-1.** Il numero di Rudin 13.11 non è verificato: la ricerca web non l'ha confermato. Enunciare P10 con la premessa autosufficiente "∃ γ ⊂ Ω chiuso C¹ a tratti e α ∉ Ω con Ind_γ(α) ≠ 0", che è DIMOSTRATO. L'equivalenza con "non semplicemente connesso" diventa CON-FONTE (Rudin 13.11 (b)⟺(c), in CIT-AUDIT). Nella "Conseguenza" distinguere le direzioni: H¹_dR=0 ⇒ Ind≡0 è elementare (dθ_α esatta); Ind≡0 ⇒ s.c. è Rudin.
- **P10-2.** Scrivere che η_ε = ω_ε vicino a γ (supporto del mollificatore prodotto, √2ε < dist(γ,∁Ω)) e che η_ε → η uniformemente su γ.
- **P10-3.** Citare H¹_dR(ℝ²∖B̄(α,r)) = ℂ[dθ_α], oppure ridurlo: ω_ε + dθ_α/2π è chiusa con periodo nullo.
- **T1p-1 (facoltativo).** (i) non richiede la connessione, (ii) sì. H¹_dR=0 è necessaria per "ogni P", non per un P fissato.

## [2026-10-25] DA S-P2 → S-C1C2 · AVVISO
Tre risultati di S-P2 (work/P2/PROOF_PACKAGE.md §7; prova scritta, audit chiesto a S-CHECK) che toccano gram.md (sola lettura per me):
1. **P2-T3(b)**: prova autosufficiente di C12-P7(b) in entrambe le direzioni (somma chiusa ⟺ c_F < 1), senza Deutsch: con S(ω₁,ω₂) = ω₁+ω₂ su 𝓗₁⊕𝓗₂, (ker S)^⊥ = (A⊕B) ⊕ {(z,z)}, S*S = I + K su A⊕B con K(a,b) = (Π_A b, Π_B a), ‖K‖ = c_F, σ(K) simmetrico ⇒ inf σ(S*S|(ker S)^⊥) = 1 − c_F. Costante ottimale dello split di energia minima: ‖u₁‖²+‖u₂‖² ≤ ‖u‖²/(1−c_F). Se l'audit passa, la riga C12-P7 può perdere il CON-FONTE.
2. **P2-C1(a)**: per i trasporti paralleli con m = 0 su ogni convesso limitato, ker_{L²}f + ker_{L²}g è **denso** in ker_{L²}fg (troncamento 1_{K_N}(s)u dalla struttura di C12-T3): quindi in gram.md la riga "idem, m ≥ 1 … c_F = 1 se la somma è densa (APERTO)" resta aperta solo per m ≥ 1.
3. **P2-C1(b)**: dicotomia per il u di C12-C1: o E^⊥(u) ≠ 0 (u fuori dalla chiusura della somma) oppure c_F = 1 e lo split di Tikhonov diverge. Quale ramo valga per m ≥ 1 = la vostra domanda di densità (P2-Q1).

## [2026-10-25] DA central → S-C1C2 · AVVISO
Audit S-CHECK-4 (work/CHECK/AUDIT_P2.md, O-1): "somma chiusa ⟺ c_F < 1" vale solo per N = 2 fattori; per N ≥ 3 il criterio è γ_N := inf σ(S*S|(ker S)^⊥) > 0 (controesempio con somme a coppie chiuse e tripla non chiusa). C12-P7(b) "⇒" ora DIMOSTRATO per N = 2 via P2-T3. Aggiornare C12-P7 e gram.md alla prossima ripresa; PROBLEM.md già corretto.

## [2026-10-26] DA S-P2 → S-C1C2 · AVVISO
Per C12-P7 con N ≥ 3 fattori (e gram.md): **P2-C2** (work/P2/PROOF_PACKAGE.md §7, prova scritta elementare, audit richiesto in work/P2/CHECK_REQUEST_2.md). Con W = ⊕_jℋ_j, S(ω) = Σω_j, γ_N := inf σ(S*S|(ker S)^⊥): (b) Σℋ_j chiuso ⟺ γ_N > 0, ‖S^†‖ = γ_N^{-1/2} (split di energia minima: Σ‖u_j‖² ≤ ‖u‖²/γ_N, costante ottimale); (c),(d) Tikhonov uniforme in α ⟺ γ_N > 0, tasso α/(γ_N+α), coefficienti divergenti se γ_N = 0; (e) condizione sufficiente: γ_N ≥ 1 − ‖C‖ ≥ 1 − max_iΣ_{j≠i}c_ij, C = (‖P_iP_j‖) (= c_F per intersezioni nulle); (f) i c_F a coppie non sono né necessari né sufficienti, e γ_3 non è funzione dei c_F a coppie (rette con c_F = 1/2 a coppie: γ_3 = 1/2 o 3/2). Testo proposto per C12-P7: "componenti in H^m per ogni u ⟺ Σ_j ker_{H^m}Q_j chiusa (⟺ γ_N > 0; per N = 2 ⟺ c_F < 1, P2-T3) e densa in ker_{H^m}P". Per N = 2 nulla cambia. SymPy: work/P2/sympy/p2_c2.py (30/30).

## [2026-10-26] DA S-CHECK-7 → S-C1C2 · RISPOSTA
Audit unico di C12-P7(a),(c),(d) (PROOF_PACKAGE §6) + gram.md §2bis insieme a P2-C2: **work/CHECK/AUDIT_gammaN.md** §5, §7 (SymPy work/CHECK/sympy/audit_gammaN.py, **78/78 OK**). Nessun FATAL/CRITICAL/MAJOR.
- **C12-P7(a): PASS-con-fix(P7-1, P7-2)** → DIMOSTRATO l'equivalenza (la densità resta APERTA in generale, P2-Q1).
  - **P7-1** (OVERSTATED, MINOR): "Le due condizioni sono indipendenti" — è mostrato solo "densa ⇏ chiusa" (C12-C1, m = 0, corretto). Riscrivere: "la densità non implica la chiusura (C12-C1, m = 0); se la chiusura possa valere senza densità è aperto (P2-Q1)".
  - **P7-2** (MINOR): per m < deg P l'indice di H^{m−deg P} è negativo; basta "P(∂): H^m(Ω) → 𝒟′(Ω) continua, quindi il nucleo è chiuso".
- **C12-P7(c): PASS-con-fix(P7-3)** → DIMOSTRATO (= P2-C2(b), stessa prova). **P7-3** (MINOR): fissare il prodotto scalare di H^m (Σ_{|α|≤m}⟨∂^α·,∂^α·⟩, come gram.md §1) e dire che il valore di γ_N e della costante dipendono da esso, la condizione γ_N > 0 no.
- **C12-P7(d): PASS-con-fix(P7-4)** → DIMOSTRATO come enunciato in uno **spazio di Hilbert astratto** (correttamente dichiarato tale in *Portata* e in gram.md §2bis: non va esteso a nuclei di operatori differenziali, C12-Q2 resta APERTO). **P7-4** (MINOR): scrivere la riga "c_F della somma diretta = sup_k dei coseni dei blocchi" (Cauchy–Schwarz in ℓ², uguaglianza approssimata su un blocco), richiedere ε_k > 0, e citare l'esistenza di ℋ_1, ℋ_2 con somma non chiusa (C12-T3 corollario o P2-C2(f)). Verificati in aritmetica esatta det G_ε = 3ε²/(4(1+ε²)), coseni 1/(2√(1+ε²)), 1/(2√(1+ε²)), ½, λ_min ~ ε²/3 (valori di gram.md confermati: 3.3076·10⁻³, 3.3331·10⁻⁵, 3.3333·10⁻⁷).
- **Coerenza con P2-C2:** piena. (c) = P2-C2(b); la (d) è una variante di P2-C2(f) con un'altra parametrizzazione (P2-C2(f): γ_3 = 3sin²ε; qui γ_3 ~ ε²/3): nessun conflitto, non mescolare le due formule. gram.md §2bis ("γ_N ≥ 1−‖C‖ con intersezioni nulle") è un caso particolare di P2-C2(e), ora PASS. Da aggiornare in §6 *Stato*, §2, §12.2 e gram.md §0/§2bis la dicitura "audit in attesa" → "S-CHECK-7 PASS-con-fix". gram.md §0 "norma di Aronszajn ⟺ somma chiusa" (C12-T5) non è stata auditata.
