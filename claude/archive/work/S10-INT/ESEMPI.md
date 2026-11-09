# ESEMPI — esempi da manuale attraverso ALGORITMO_ESTESO (Fase 10, S10-INT)

Sessione S10-INT, 27/10/2026. Specifica di riferimento: `ALGORITMO_ESTESO.md` rev. 2 (approvata al Gate 9), con le convenzioni §0.1–§0.5. Notazione: NOTAZIONE v6.

**Che cosa sono questi esempi.** Sono verifiche **V-ex** (SymPy/mpmath), non teoremi. Gli script stanno in `work/S10-INT/sympy/`, sono eseguiti con `D:\ProblemaBase\.venv\Scripts\python.exe -I <script>.py` e la loro uscita è salvata nei file `.out` accanto. Gli esiti sono riassunti al §6. Dove un esempio usa un argomento scritto qui e non presente nel LEDGER, l'argomento è marcato **PROVA SCRITTA** (non auditato) e compare in `LEDGER_ROWS.md`.

**Schema di ogni esempio.**
- dato, modello di dato (§0.3) e anello dei coefficienti (Gate 8b, NOTAZIONE v6);
- passi 1 → 7 con i claim usati e il loro stato;
- etichetta d'uscita (§0.5) e senso ID-*;
- contratto a due strati (§0.4): **completezza** (passi 1–3) e **correttezza condizionata** (passi 4 → 6), ciascuna in (A), (B), (C) o (Lim).

**Riepilogo**

| es. | dato | livello | modello | anello / classe | uscita | senso | completezza / correttezza |
|---|---|---|---|---|---|---|---|
| a-4 | Dirac 1+1, 4 onde piane generiche | L6 | DM1 | classe hamiltoniana K_H (8 incognite) | `IDENTIFICATA[ID-ker, DM1]` | ID-ker, (H-ex) | (A) / (A) |
| a-1 | Dirac 1+1, 1 onda piana | L6 | DM1 | K_H | `NON-DECISO` (famiglia compatibile di dim. 6) | nessuno | (A) / (A) del calcolo |
| b-coh | oscillatore, stato coerente | L7–L8 | DM3 | {−∂² + V(t,x)}; A_2 | `IDENTIFICATA[ID-res, DM3]`; ID-ann in A_2 | ID-res; ID-ann | (C) / (A) |
| b-HG | oscillatore, Hermite–Gauss | L7 | M3-hol | {−∂² + V}; A_2 | `IDENTIFICATA[ID-res, M3-hol]`; mai ID-ann in A_2 | ID-res | (C) / (A) |
| b-enc | oscillatore, passo 5 | L8 | — | parola chirp·libero·chirp | (A) per cos t ≠ 0; non esiste a cos t = 0 | — | — / (A) a tratti |
| c | Pöschl–Teller | L7 | DM3 (non M3-hol su ℂ(x), vedi §3) | {−∂² + V(x)}; ℂ(tanh x)[∂] per il passo 6 | `IDENTIFICATA[ID-res, DM3]`; ID-fam in DM-φ | ID-res; ID-fam | (C) / (A); Darboux (C) |
| d | calore frazionario | L9 | DM1 e M3-hol | ℂ[∂] (fallisce); FRAC parametrica | locale: misfit, poi surrogato; FRAC: identificata; unione: `NON-DECISO` | ID-ker relativo; ID-ann del sollevamento | (C) / (A) |
| e | Maxwell nel vuoto | L6 | DM1 | classe hamiltoniana generale (144) e simmetrica (99) | generale: ID-fam modulo vincoli; simmetrica: `IDENTIFICATA[ID-ker, DM1]` | ID-fam; ID-ker | (A) / (A) |

---

## 1. EX10-a — Dirac libero 1+1, m ≠ 0

**Script:** `sympy/ex10_a_dirac.py` (13/13 PASS).

**Convenzione** (ALGORITMO_ESTESO §9.1). iψ_t = Hψ, H = −iσ_x∂_x + mσ_z, con m = 1 e base fissata α = σ_x, β = σ_z (H-DIRAC-1, H-DIRAC-2). La classe in cui si cerca la legge è la **classe hamiltoniana** K_H: iψ_t = Aψ_x + Bψ, con A, B ∈ Mat_2(ℂ), quindi 8 incognite. La legge vera è (A, B) = (−iσ_x, mσ_z).

**Dato.** ψ = Σ_j v_j e^{i(k_jx − ω_jt)} con ω_j = ±√(k_j² + 1), (H_{k_j} − ω_j)v_j = 0 e H_k = kσ_x + mσ_z. Si usano terne pitagoriche, così le frequenze sono razionali e il dato è EP esatto:
- (a-4) quattro modi: (k, ω) = (3/4, 5/4), (4/3, −5/3), (5/12, 13/12), (12/5, −13/5);
- (a-1) il solo primo modo.

Gli esponenziali con esponenti distinti sono linearmente indipendenti su ogni aperto. Quindi il sistema puntuale su Ω equivale al sistema modo per modo (ik_jA + B)v_j = ω_jv_j, cioè 2 equazioni per modo.

### Passi
| passo | contenuto | claim → stato |
|---|---|---|
| 1. modello | **DM1** (formula EP). Anello: matrici su ℂ[∂_t, ∂_x] (L6), più la classe parametrica finita K_H. Sensi raggiungibili: **solo ID-ker relativo a una classe finita**; mai ID-ann (§0.3) | P4-T2 DIMOSTRATO; C3-T2(c,d) DIMOSTRATO |
| 2. livello | L6, sistemi a coefficienti costanti; atomi ∂_x, 1 con coefficienti matriciali | — |
| 3b. identificazione | **H-DIRAC-ker**: rango del sistema lineare = 2·(numero di modi) fino a 8. Con 4 modi il rango è 8, la soluzione è unica ed è la legge vera, quindi vale (H-ex). **H-DIRAC-ann** non si applica: il dato è EP e ∏_j(∂_x − ik_j)·I ∈ Ann(ψ), ma questo operatore non annulla l'onda k = 0 (che risolve Dirac), quindi non sta in U_P | H-DIRAC DIMOSTRATO (sotto H-DIRAC-1/2, m ≠ 0); DICT-RANGO DIMOSTRATO (ID-ker sotto (H-ex)); VAR-T1(a) DIMOSTRATO (compatibili = θ_0 + ker Φ_u) |
| 4. misfit/fit | non serve: il dato è esatto e il calcolo è in ℚ(i). Controllo puntuale numerico come in §9.1: con 4 modi i valori singolari vanno da 7,7e-2 a 17,1 (rango 8); con 1 modo sei valori singolari sono < 1e-30 (rango 2) | — |
| 5. encoder | nessuno (coefficienti costanti) | — |
| 6. fattori | (i∂_t − H)(i∂_t + H) = −(τ² − ξ² + m²)I e τ² − ξ² + m² è irriducibile su ℚ(i): **un solo fattore**, nessuna scomposizione non banale. I proiettori sulle energie ±√(ξ² + m²) non sono polinomiali (II-T2: polinomiali ⟺ varietà disgiunte) | II-T2 DIMOSTRATO; C12-T1′ (vacuo: un fattore) |
| 7. contratto | sottocatena 4 → 6 vuota o esatta | CONV-T7 |

### Uscita e contratto
- **(a-4), 4 onde piane generiche.** `IDENTIFICATA[ID-ker, DM1]`, relativa alla classe K_H. Completezza **(A)**: DM1 relativo a una classe finita dichiarata. Correttezza **(A)**: rango esatto, soluzione unica. Il rango cresce come 2, 4, 6, 8 con 1, 2, 3, 4 modi.
- **(a-1), una sola onda piana.** Rango 2 su 8, dim ker Φ_u = 6. ID-ker fallisce. Uscita: **`NON-DECISO`** per l'identificazione, con l'insieme compatibile θ_0 + ker Φ_u, affine di dimensione 6, dichiarato come sottoprodotto (VAR-T1(a)). Il calcolo è (A).
- **Caso non generico.** Due modi allo stesso k, sui due rami ±ω, danno rango 4: ID-ker richiede modi generici (almeno due valori distinti di k), non solo «≥ 4 modi».

**Lettura** (conferma ATTACK-9 §3(A) e la correzione O5 di §9.1). Il fallimento di ID-ker dipende dal numero e dalla genericità dei modi, non dal fatto che il dato sia EP. L'essere EP esclude invece **ID-ann** (H-DIRAC-ann richiede ψ_2 ∉ EP).

**Osservazione per il coordinatore (etichette §0.5).** Per un dato esatto con insieme compatibile non ridotto a un punto, §0.5 non ha un'etichetta esplicita: `FIT-COMPATIBILE` è pensata per i dati numerici, `NON-DECISO` per il budget esaurito. Qui uso `NON-DECISO` con la famiglia compatibile dichiarata. Un'etichetta `COMPATIBILI(θ_0 + ker Φ_u)` sarebbe più precisa.

---

## 2. EX10-b — Schrödinger armonico, H = −∂² + x²

**Script:** `sympy/ex10_b_oscillatore.py` (19/19 PASS).

Equazione: iu_t = −u_xx + x²u. È la normalizzazione unica di NOTAZIONE v6. La classe strutturata in cui si cerca il potenziale è {iψ_t = −ψ_xx + V(t,x)ψ}, livello L8 (L7 se V(x)).

### b-coh. Stato coerente
u_c = exp(−x²/2 + √2 α(t)x − α(t)²/2 − it), con α(t) = α_0e^{−2it}. SymPy verifica che u_c risolve l'equazione.

| passo | contenuto | claim → stato |
|---|---|---|
| 1. modello | **DM3** (forma chiusa esatta, con prova simbolica). **Non è M3-hol**: u_c non è D-finita (sotto). Anello dichiarato: la classe parametrica {−∂² + V(t,x)}; per l'identificazione intrinseca, A_2 = ℂ[t,x]⟨∂_t, ∂_x⟩ | — |
| 1′. anello sbagliato | nel campo ∂-chiuso 𝒦 = ℂ(x, e^{2it}) si ha (∂_x + x − √2α)u_c = 0: un annullatore d'ordine 1, quindi l'oggetto (𝒦[∂]·u, u) è **vacuo**. È proprio la situazione per cui Gate 8b chiede di dichiarare l'anello (PATCH_GATE3 P1) | VAR-N1 DIMOSTRATO |
| 2. livello | L8, forma fissata, V incognito | — |
| 3c. identificazione | u_c non ha zeri, quindi int Z(u) = ∅ e ρ_u = (iu_t + u_xx)/u = **x²** esattamente (**ID-res**). In DM-φ: ρ(e^{iφ}u) = x² − φ′(t), quindi solo **ID-fam** (V modulo c(t)) | VAR-T1(c)(i)–(iii) DIMOSTRATO; VAR-P4 DIMOSTRATO |
| 3c′. ID-ann in A_2 | L = i∂_t + ∂_x² − x² è monico in ∂_t (a meno del fattore i) con M ∈ B. Per VAR-C3Q2(c), Ann_{A_2}(u) = A_2L ⟺ u non è D-finita. **Argomento (PROVA SCRITTA, EX10-b-ND):** ∂_x^bu_c/u_c è un polinomio in α di grado esatto b (SymPy, b ≤ 5; in generale per induzione, perché ∂_x(p(α)u) = (p′_x + p·(−x + √2α))u). α = α_0e^{−2it} è trascendente su ℂ(t,x) per α_0 ≠ 0, quindi u, ∂_xu, ∂_x²u, … sono ℂ(t,x)-indipendenti: lo span ha dimensione infinita e u_c non è D-finita. Dunque u_c **identifica L in A_2 (ID-ann)** | VAR-C3Q2(c) DIMOSTRATO; EX10-b-ND PROVA SCRITTA |
| 4. misfit/fit | non serve (prova simbolica) | — |
| 5. encoder | parola metaplettica, vedi b-enc | VAR-T10(3) |
| 6. termini | i due termini −∂² e x² non commutano. E^mult è il commutatore a due tempi più O(t³) (VAR-P9); la forma chiusa di E_int per V = x² è ENC-A9(b3), CON-FONTE + V-ex. Qui non è ricalcolata | VAR-P9 DIMOSTRATO; ENC-A9(b3) CON-FONTE + V-ex → condizionato a verifica |

**Uscita.** `IDENTIFICATA[ID-res, DM3]` con V = x². Inoltre `IDENTIFICATA[ID-ann, DM3]` in A_2, condizionata a EX10-b-ND (PROVA SCRITTA). In DM-φ: ID-fam. **Contratto:** completezza **(C)**, perché la forma dell'equazione è scelta a priori (R4); correttezza **(A)** (prova simbolica).

### b-HG. Combinazione di Hermite–Gauss
u_h = e^{−x²/2}(e^{−it} + 2x e^{−3it}) = h_0e^{−it} + h_1e^{−3it}.

| passo | contenuto | claim → stato |
|---|---|---|
| 1. modello | **M3-hol** (gaussiana per polinomio, D-finita) | — |
| 3c. identificazione | zeri solo in punti isolati: x = −e^{2it}/2 reale ⟺ t ∈ (π/2)ℤ, per esempio (0, −1/2) e (π/2, 1/2); a t = π/4 il fattore è 1 − 2ix, senza zeri reali. Dunque int Z(u) = ∅ e ρ_u = x² su {u ≠ 0}: **ID-res** | VAR-T1(c) DIMOSTRATO |
| 3c′. A_2 | u_h è D-finita: R = (H − 1)(H − 3) ∈ B = ℂ[t,x]⟨∂_x⟩ la annulla. Quindi Ann_{A_2}(u_h) ≠ A_2L: **mai ID-ann in A_2**. Come gli stati stazionari, «non identificano in A_2» (S8-VAR §5) | VAR-C3Q2(d) DIMOSTRATO |

**Uscita.** `IDENTIFICATA[ID-res, M3-hol]` con V = x²; niente ID-ann. **Contratto:** (C) / (A).

### b-enc. Passo 5: la parola chirp·libero·chirp e la sua rottura a cos t = 0
VAR-T10(3), nella normalizzazione H = −∂² + x²: U(t) = c(t)e^{iγx²}e^{is∂²}e^{iγx²}, con γ = (cos 2t − 1)/(2 sin 2t) e s = sin(2t)/2. SymPy verifica:
- γ = −tan(t)/2, quindi γ → ∞ per t → π/2: la parola **si rompe esattamente a cos t = 0**. Questo conferma la riga VAR-T10-F (la frase F6 è VERA; F5 di DEVIL-6 è ritirata, GATE8 O3).
- s(π/2) = 0 e M(π/2) = −I: né M_12 ≠ 0 né M unipotente inferiore, quindi la parola a tre fattori non esiste.
- La parola, applicata a una Gaussiana generica exp(−bx² + cx), risolve l'equazione: i coefficienti di x² e x del residuo si annullano identicamente in (t, b, c), e il residuo costante si assorbe in c(t). Per t → 0 la parola tende all'identità.
- Sulla base di Hermite, U(π/2)h_n = e^{−i(2n+1)π/2}h_n = −i h_n(−x): U(π/2) = −i·(parità).

| voce | contenuto |
|---|---|
| contratto | **(A)** sull'intrecciamento a tre fattori, su ogni intervallo di {cos t ≠ 0}, attraversando la lente t = π/4 (VAR-T10(3)(i)–(ii) DIMOSTRATO). A cos t = 0 la traduzione a tre fattori **non è definita**. Se il passo 5 deve attraversare t = π/2, si compone con U(π/2) = −i·R (parità). Questo è esatto sulla base di Hermite ma è un'osservazione V-ex (e il nucleo di Mehler è VAR-T10(3)(iii), CON-FONTE + V-ex), non un fondamento: **condizionato a verifica** |
| Magnus | non usato. Per V = x² illimitato il Magnus (B) è quasi vuoto (§7) |

---

## 3. EX10-c — Pöschl–Teller, q = −2 sech²x

**Script:** `sympy/ex10_c_poschl_teller.py` (18/18 PASS). Le identità tra operatori sono verificate in modo esatto, coefficiente per coefficiente; le identità tra funzioni a 45 cifre in 6 punti (soglia 1e-35).

Dato (come §9.2): u = u_b + u_s, con u_b = e^{it}sech x (stato legato, E_0 = −1) e u_s = e^{−ik²t}(ik − tanh x)e^{ikx}, k = 3/2. Equazione: iu_t = L_qu, L_q = −∂² + q.

**Correzione di modello (segnalazione).** ALGORITMO_ESTESO §0.3 e §9.2 chiamano questo dato «M3-hol». Ma sech x **non è D-finita su ℂ(x)**: ha infiniti poli in iπ(n + 1/2), mentre una funzione D-finita ha un numero finito di singolarità. sech x è D-finita su ℂ(e^x) o su ℂ(tanh x), non su ℂ(x). Il modello corretto è **DM3 con prova simbolica**, oppure M3-hol relativo all'anello ℂ(e^x)[∂]. Lo stesso vale per la voce «sech» nella tabella §0.3. Da girare al coordinatore: è una correzione di etichetta, non di valore di verità.

| passo | contenuto | claim → stato |
|---|---|---|
| 1. modello | DM3 (vedi sopra). Anelli: la classe parametrica {−∂² + V(x)}, V ∈ L^∞_loc, per l'identificazione; ℂ(tanh x)[∂] (campo differenziale: tanh′ = 1 − tanh²) per la fattorizzazione | — |
| 1′. vacuità | in 𝒦 = ℂ(tanh x): (∂_x + tanh x)u_b = 0 e (∂_t − i)u_b = 0, e u_s,x/u_s = ik − (1 − tanh²)/(ik − tanh) ∈ 𝒦. Ann_{𝒦[∂]} contiene operatori d'ordine 1: (𝒦[∂]·u, u) è vacuo e serve ρ_u (PATCH_GATE3 P1) | VAR-N1 DIMOSTRATO |
| 2. livello | L7 | — |
| 3c. identificazione | ρ_u = (iu_t + u_xx)/u = q: **ID-res**. Con il solo stato legato in DM-φ: W = −φ_0′/φ_0 = tanh x e W² − W′ = q + 1 = V − E_0, cioè V solo **modulo una costante** (ID-fam), mentre con la fase osservata (DM3) ρ_{u_b} = q esattamente. **Non ID-ann** nel sottoanello ℂ[∂_t, L_q]: (L_q + 1)(L_q − k²) e (i∂_t + 1)(i∂_t − k²) annullano u | VAR-T1(b) DIMOSTRATO; VAR-P4 DIMOSTRATO |
| 5. encoder | **Darboux** A = ∂ + tanh x: Au_b = 0 (il modo legato si perde) e Au_s = −(1 + k²)e^{i(kx − k²t)}, un'onda piana, cioè un dato EP. Au risolve Schrödinger libero. A non è limitato: niente C_W | ENC-K1′ DIMOSTRATO (noto: Andrianov–Sokolov, Crum) |
| 6. fattori | **Fattorizzazione** A⁺A = L_q + 1 e AA⁺ = L_0 + 1 (partner libero); catena di Crum per ℓ = 2: A_2⁺A_2 = L_{q_2} + 4 e A_2A_2⁺ = L_{q_1} + 4, con A_2 = ∂ + 2 tanh x e q_2 = −6 sech². **Componenti = fattori** nel sottoanello commutativo ℂ[L_q], con varietà disgiunte (−1 ≠ k²): i proiettori polinomiali (L_q − k²)/(−1 − k²) e (L_q + 1)/(k² + 1) restituiscono esattamente u_b e u_s | II-T2 DIMOSTRATO (nel sottoanello commutativo); C12-T1′ (scalare) |

**Uscita.** `IDENTIFICATA[ID-res, DM3]` con V = −2 sech²x; ID-fam in DM-φ; componenti (u_b, u_s) uniche.
**Contratto.**
- Completezza (C): forma dell'equazione scelta.
- Correttezza (A): identificazione e proiettori.
- Passo 5 di Darboux: **(C)** (§5, O7). La traduzione perde il modo legato e trasforma un dato identificante in un dato EP, quindi l'identificazione dopo la traduzione è al più ID-ker relativa.

---

## 4. EX10-d — calore frazionario ∂_t + (−∂_x²)^s, 0 < s < 1

**Script:** `sympy/ex10_d_frazionario.py` (13/13 PASS).

**Dichiarazione onesta.** (−∂_x²)^s, per s non intero, **non è un operatore differenziale**: è un moltiplicatore di Fourier di simbolo |κ|^{2s}, livello L9. Nella classe differenziale ℂ[∂] l'algoritmo **non può identificarlo, per costruzione**. Può fare soltanto tre cose:
- (i) dare misfit;
- (ii) trovare un **surrogato locale** (interpolante, oppure sollevamento polinomiale se s è razionale);
- (iii) fermarsi con `NON-DECISO`.

Solo nella classe parametrica dichiarata FRAC = {∂_t + c(−∂_x²)^σ}, cioè la famiglia FRAC del dizionario (S8-DICT §6), il parametro è identificato. La completezza è sempre (C): se la legge sta nella classe dipende dalla scelta del livello.

### d1. s = 1/4, tre modi di Fourier (DM1)
u = Σ_{k=1,2,3} e^{−k^{1/2}t + ikx}.
- **Livello LIN_1** (u_t = (a_0 + a_1∂_x)u): il sistema a(ik) = −k^{1/2}, k = 1, 2, 3, è **incompatibile**. È un `MISFIT` esatto, con contratto (A): il calcolo è in ℚ(√2, √3, i), non numerico.
- **Livello LIN_2:** esiste una legge locale unica u_t = a(∂_x)u, deg a = 2, con coefficienti in ℚ(√2, √3, i) (stampati nel `.out`). Uscita: `IDENTIFICATA[ID-ker, DM1]` **relativa a LIN_2**. (H-ex) vale sempre per un numero finito di modi, per interpolazione dei simboli (ATTACK-9 §3(E)). Ma **questa legge non è la legge frazionaria**: non annulla il modo k = 4 della legge vera. È il caso tipico in cui la correttezza è (A) e la completezza è (C).
- **Classe FRAC:** due modi con |k| distinti determinano (c, σ) = (1, 1/4) in modo unico; il terzo modo è coerente, quindi (H-ex) vale in FRAC. Uscita: `IDENTIFICATA[ID-ker*, DM1]` relativa a FRAC. L'asterisco segnala che ID-ker è definito (DICT-RANGO) per famiglie lineari nei parametri, mentre qui σ entra in modo non lineare: è iniettività della mappa θ ↦ L_θu. Etichetta da confermare dal coordinatore.
- **Unione LIN_2 ∪ FRAC:** due leggi distinte, entrambe esatte. Nessuna unicità, quindi `NON-DECISO`.

### d2. s razionale: il sollevamento polinomiale
Per s = p/q, ogni modo e^{−|k|^{2s}t + ikx} soddisfa (−∂_t)^q u = (−∂_x²)^p u. Per s = 1/4: ∂_t⁴u + ∂_x²u = 0 su ogni modo, anche con k < 0 (SymPy). Dunque, per **ogni** soluzione della legge frazionaria, il livello differenziale di grado 4 in τ trova la legge locale τ⁴ + ξ² = (τ² + iξ)(τ² − iξ). È la «legge non locale indistinguibile se il simbolo è algebrico» di CONV-T6 (DIMOSTRATO). L'algoritmo restituisce il sollevamento, non (−∂²)^{1/4}.

### d3. s = 1/2, dato di Poisson (M3-hol)
u = T/(T² + x²), T = t + 1, su Ω ⊂ {t > −1} connesso. Il dato è razionale, quindi olonomo.
- **Fourier:** û(t, κ) = π e^{−T|κ|} (quadratura oscillante, errore < 1e-30), quindi u_t = −|D|u: è la legge frazionaria con s = 1/2.
- **Livello 1 in τ:** nessuna legge u_t = a(∂_x)u con deg a ≤ 4 (sistema dei coefficienti incompatibile): `MISFIT` (A) a ognuno di questi livelli. In generale CONV-T6: |κ| non è polinomiale.
- **Livello 2 in τ:** Δu = u_tt + u_xx = 0. Test C3-T1: (∂_t ∓ i∂_x)u = cost./(x ∓ iT)² ha poli, quindi non è EP. Dunque **Ann(u) = (∂_t² + ∂_x²)**: `IDENTIFICATA[ID-ann, M3-hol]` del **laplaciano**, cioè la legge locale sollevata, non quella frazionaria.
- **Passo 6:** Δ = (∂_t + i∂_x)(∂_t − i∂_x), con componenti f(x − iT) e g(x + iT) e δ(P) = dim R/(Q_1, Q_2) = 1. La legge frazionaria corrisponde alla scelta della soluzione che decade per t → ∞ (semigruppo di Poisson). È un'informazione **al bordo / all'infinito**, invisibile ad Ann(u) (CONV-B1 DIMOSTRATO).

### d4. s irrazionale, spettro infinito (solo citato, nessun controllo SymPy)
Per s irrazionale e un dato con spettro continuo, il grafo τ = −|κ|^{2s} è trascendente e Ann(u) = 0 (CONV-T6). L'algoritmo dà `MISFIT` a ogni livello differenziale e si ferma con **`NON-DECISO`** a n_max. Nella classe FRAC il parametro resta identificabile.

**Uscita complessiva e contratto.**
- Classe differenziale: `MISFIT` (A) ai livelli bassi, poi un **surrogato locale**: ID-ker relativo con un numero finito di modi, ID-ann del sollevamento per s = 1/2 con il dato di Poisson, oppure `NON-DECISO` per s irrazionale.
- Classe FRAC: identificazione del parametro (ID-ker*).
- Unione delle due classi: `NON-DECISO`.
- Completezza sempre **(C)**; correttezza (A) per i calcoli esatti.
- Manca, come in §11.2 di ALGORITMO_ESTESO, un esempio a infiniti modi in cui **la classe differenziale** distingua l'atomo non locale. Questo esempio non lo fornisce, e non lo può fornire per s razionale (d2).

---

## 5. EX10-e — Maxwell nel vuoto come sistema

**Script:** `sympy/ex10_e_maxwell.py` (17/17 PASS).

**Quadro.** c = 1, ψ = (E, B) ∈ 𝒜⁶, R = ℂ[τ, ξ_1, ξ_2, ξ_3] (n = 4). P ∈ R^{8×6} ha le righe τE − ξ×B, τB + ξ×E, ξ·E, ξ·B.

| passo | contenuto | claim → stato |
|---|---|---|
| 1. modello | dato EP: 48 onde piane, cioè 12 vettori k con |k| razionale (quaterne pitagoriche) × 2 rami ω = ±|k| × 2 polarizzazioni E_0 ⊥ k, con B_0 = k×E_0/ω. SymPy verifica che ognuna risolve le 8 equazioni, vincoli compresi. **DM1**: solo ID-ker relativo | P4-T2 (analogo per sistemi: modulo R·ψ di lunghezza finita) |
| 2. livello | L6 | — |
| 3b. struttura | sizigie S_1 = (ξ, 0, −τ, 0) e S_2 = (0, ξ, 0, −τ) con S_iP = 0; minore 6×6 = τ²(τ² − \|ξ\|²)², quindi **rango P = 6**; □·[I 0] è combinazione delle righe (ogni componente risolve l'equazione delle onde). Esiste un campo identificante (ID-ann) su ogni Ω connesso, perché lo zoccolo è nullo, ma non è EP | SYS-MAXWELL **PROVA SCRITTA** (S10-OPEN-C §9); SYS-EX DIMOSTRATO |
| 3b. ID-ann con dato EP | r = ∏_{k_1 distinti}(∂_1 − ik_1)·e_{E_1} annulla il dato ma non l'onda con k = (0, 3, 4) ed E_1 ≠ 0: r ∈ Ann(ψ) ∖ U_P, quindi **mai ID-ann** con dati EP | — |
| 3b. ID-ker, classe generale | ∂_tψ = Σ_jA_j∂_jψ + Bψ, 4·36 = 144 incognite: **rango 132**. Il nucleo contiene le 12 direzioni di vincolo A_j ↦ A_j + w e_{E_j}^T e A_j ↦ A_j + w e_{B_j}^T (w ∈ ℂ⁶), indipendenti: aggiungere w·div E o w·div B non cambia nulla sulle soluzioni. **Per ogni dato di Maxwell** (non solo EP) ker Φ_u ⊇ questo spazio di dimensione 12: nella classe generale ID-ker è impossibile. Si identifica solo la classe modulo le combinazioni dei vincoli, cioè l'equivalenza a sinistra D ~ VD ristretta alla classe: **ID-fam**. Che il nucleo sia *esattamente* di dimensione 12 per onde piane su entrambi i rami è V-ex qui, con l'argomento EX10-e-K sotto | EX10-e-K PROVA SCRITTA; SYNTHESIS-2 §0.1 («equivalenza a sinistra») |
| 3b. ID-ker, classe simmetrica | A_j = A_j^T (63 incognite) e B qualsiasi (36), 99 incognite in tutto: **rango 99**. La soluzione è unica ed è Maxwell: A_j = [[0, L_j], [−L_j, 0]] (simmetriche), B = 0. **`IDENTIFICATA[ID-ker, DM1]`** relativa alla classe simmetrica iperbolica. Il vincolo di simmetria rompe l'ambiguità dei vincoli: w e_{E_j}^T simmetrica per ogni j obbliga w = 0 | DICT-RANGO DIMOSTRATO |
| 6. fattori ed Ext¹ | **elicità** (Riemann–Silberstein) F = E + iB, G = E − iB. Con V ∈ GL_8(ℂ) e T ∈ GL_6(ℂ) costanti, VPT = diag(P_F, P_G), P_F = [τI + iC(ξ); ξ^T] e P_G = [τI − iC(ξ); ξ^T]. Con Q_1 = «G = 0 e P» e Q_2 = «F = 0 e P», U_1 + U_2 ⊇ righe costanti di rango 6, quindi **N = 0** e **Ext¹(N, 𝒜) = 0 su ogni Ω**, anche non semplicemente connesso. U_1 ∩ U_2 = U_P (blocchi). Dunque «componente = fattore» vale: Sol(P) = Sol(Q_1) ⊕ Sol(Q_2) con proiettori costanti, ambiguità ℓ(N) = 0. **Ma** det(τI ± iC) = τ(τ² − \|ξ\|²): le due elicità hanno **la stessa varietà caratteristica** | SYS-S1(i⇐) DIMOSTRATO (caso N = 0); SYS-S1(ii) DIMOSTRATO; CONV-D1 DIMOSTRATO («salvo fattori comassimali (Lamé, Maxwell)») |

**Argomento EX10-e-K (PROVA SCRITTA).** Sia T(k) := iΣ_jk_jA_j + B, affine in k. Con entrambi i rami e due polarizzazioni, le onde piane impongono che T(k) sia prescritto sullo spazio K(k) = {(E, B) : k·E = k·B = 0}, di dimensione 4. Un elemento del nucleo è un T affine con T(k)|_{K(k)} = 0 per ogni k, cioè T(k)ψ = X(k)(k·E, k·B) con X(k) ∈ ℂ^{6×2}.
- Poiché T è affine e k·E, k·B sono lineari e coprimi come polinomi, X è costante.
- Il termine costante B si annulla su ∪_k K(k) = ℂ⁶, quindi B = 0.
- Quindi il nucleo è esattamente {A_j = −i(w_1e_{E_j}^T + w_2e_{B_j}^T)}, di dimensione 12, e il rango per insiemi sufficientemente generici di k è 132, come nel calcolo.

**Lettura.** Nel caso scalare, «componenti uniche» ⟺ «varietà disgiunte» (C12-T1′, II-T2). Per i sistemi questo criterio **non si trasferisce**: le due elicità hanno la stessa varietà (il cono di luce), eppure la scomposizione è unica e con proiettori costanti, perché N = 0. L'invariante giusto è il modulo N con Ext¹(N, 𝒜), come richiede Gate 8b (PATCH_GATE3 P2). La scomposizione per segno della frequenza invece non è polinomiale (richiede |k|), quindi non è una scomposizione per fattori in R.

**Uscita e contratto.**
- Classe generale: **ID-fam** (modulo i 12 vincoli).
- Classe simmetrica: `IDENTIFICATA[ID-ker, DM1]`.
- Componenti per elicità uniche.
- Completezza (A), perché DM1 è relativo a classi finite dichiarate; correttezza (A), perché i ranghi sono esatti in ℚ(i) (DomainMatrix su QQ_I) e i proiettori sono costanti.

---

## 6. BUILD — esiti degli script

Comando: `D:\ProblemaBase\.venv\Scripts\python.exe -I <script>.py`, dalla cartella `work/S10-INT/sympy/` (SymPy 1.14.0, mpmath 1.3.0). Nessuno script di `_vendor` è stato eseguito.

| script | esito | controlli chiave |
|---|---|---|
| `ex10_a_dirac.py` | **13/13 PASS** | rango 2, 4, 6, 8 con 1–4 modi; unicità e (H-ex) con 4 modi; rango 4 allo stesso k; puntuale: σ_min = 7,7e-2 (4 modi), 6 valori singolari < 1e-30 (1 modo); operatore estraneo in Ann; KG irriducibile |
| `ex10_b_oscillatore.py` | **19/19 PASS** | stato coerente e Hermite–Gauss risolvono; ρ_u = x²; DM-φ; vacuità in ℂ(x, e^{2it}); grado in α = b (b ≤ 5); (H − 1)(H − 3)u_h = 0; γ = −tan t/2; parola su Gaussiane generiche; U(π/2) = −i·parità |
| `ex10_c_poschl_teller.py` | **18/18 PASS** | A⁺A = L_q + 1, AA⁺ = L_0 + 1, catena ℓ = 2; ρ_u = q; W² − W′ = q + 1; vacuità in ℂ(tanh x); due annullatori estranei; proiettori; Au_b = 0, Au_s onda piana |
| `ex10_d_frazionario.py` | **13/13 PASS** | misfit LIN_1, legge unica LIN_2 (≠ frazionaria); FRAC (1, 1/4); sollevamento ∂_t⁴ + ∂_x²; Poisson: û = πe^{−T\|κ\|} (errore ≤ 2e-31), Δu = 0, test C3-T1, nessuna legge del 1° ordine con deg a ≤ 4 |
| `ex10_e_maxwell.py` | **17/17 PASS** | sizigie; minore τ²□²; □ ∈ U_P; VPT = diag(P_F, P_G); N = 0; stessa varietà; 48 onde piane; rango 132/144 (nucleo = 12 vincoli); rango 99/99 nella classe simmetrica, soluzione = Maxwell; operatore estraneo |

Note sugli script:
- In `ex10_a_dirac.py` il primo tentativo del controllo puntuale con 1 modo falliva (12/13) per un artefatto di conversione a doppia precisione (valori singolari ≈ 4e-17 invece di < 1e-20). Corretto passando a `mp.mpc` a 35 cifre. Non è un problema matematico.
- In `ex10_d_frazionario.py` la prima quadratura (non oscillante) dava errori ≈ 5e-3. È stata sostituita da `mp.quadosc`.
- `ex10_e_maxwell.py` nella prima versione (matrici simboliche di SymPy con 144 simboli e `gauss_jordan_solve`) non terminava entro 25 minuti ed è stata interrotta. La versione finale costruisce i sistemi direttamente come `DomainMatrix` su QQ_I (aritmetica esatta in ℚ(i)) e termina in pochi secondi; i controlli sono gli stessi, con l'unicità verificata da rango = numero di incognite più compatibilità del sistema aumentato.
- `ex10_c_poschl_teller.py` nella prima versione (semplificazione simbolica completa via exp) non terminava entro 400 s ed è stata interrotta. La versione finale controlla in modo esatto le identità tra operatori e numericamente (45 cifre) quelle tra funzioni.

## 7. Segnalazioni al coordinatore (nessuna modifica fatta ai suoi file)
1. **sech non è M3-hol su ℂ(x)** (§3): ALGORITMO_ESTESO §0.3 (tabella, voce M3-hol) e §9.2 vanno letti come DM3 con prova simbolica, oppure M3-hol su ℂ(e^x)[∂].
2. **Etichetta d'uscita per dati esatti non unici** (§1): manca in §0.5. Proposta: `COMPATIBILI(θ_0 + ker Φ_u)`.
3. **ID-ker in classi parametriche non lineari** (§4, FRAC): DICT-RANGO lo definisce per famiglie affini. Serve una nota in NOTAZIONE: iniettività di θ ↦ L_θu.
4. **Maxwell:** nella classe hamiltoniana generale ID-ker è strutturalmente impossibile (12 direzioni di vincolo). La classe va dichiarata: simmetrica iperbolica, oppure modulo U_P. Coerente con «equivalenza a sinistra» in SYNTHESIS-2 §0.1.
5. **Passo 5 a cos t = 0:** la composizione con U(π/2) = −i·R è V-ex ed eredita la CON-FONTE di Mehler; non va usata come fondamento finché VAR-T10(3)(iii) non è verificato.
