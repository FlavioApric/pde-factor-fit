# AUDIT di TRIAGE_APERTI.md (CHECK-F10) — sei voci

**Auditor.** Indipendente e avversariale: non sono l'autore del triage né delle prove auditate. Data: 28/10/2026.

**Materiale letto.**
- `work/CHECK-F10/TRIAGE_APERTI.md`, `triage_scripts/tri_p1q7.py`, `tri_delta.py` e tutte le uscite `*.out`.
- `claims/LEDGER.md`: righe 16–17, 60, 112, 157, 189–190 e la sezione Fase 10 (righe 385–543).
- `work/S10-OPEN-A/PROOF_PACKAGE.md` §2 (S10A-T2) e §3.
- `work/S10-OPEN-B/PROOF_PACKAGE.md` §9 e R9 (L8′, V9).
- `work/S10-OPEN-C/PROOF_PACKAGE.md` §6 (a′), §7 (Lemma E), §16 (DICT-Q4).
- `work/OP-F5C/PROOF_PACKAGE.md` (convenzioni, T1(b), L8, P9).

**Script nuovi** (tutti in `work/CHECK-F10/audit_triage_scripts/`, eseguiti con `.venv\Scripts\python.exe -I`). Nessuno importa codice del triage o dei pacchetti.
- `audit_items.py` → `audit_items.out`: **13/13 OK** (voci 1, 3, 4, 5).
- `audit_delta.py` → `audit_delta_runA.out`, `audit_delta_runB.out`, `audit_delta_runC.out` (voce 6).

Non ho modificato nessun altro file e non ho eseguito nulla in `_vendor`.

**Scala.**
- PASS: la prova regge come scritta.
- PASS-con-fix MINOR: la prova regge, la stesura va completata.
- PASS-con-fix MAJOR: la tesi è vera o probabile, ma l'argomento scritto ha una lacuna sostanziale.
- FAIL: la lacuna rompe la tesi, oppure la tesi è falsa.

---

## 1. P1-Q7: candidato X = (x³+x)∂, Y = ∂ con «dilatazione filtrata»

**Verdetto: PASS-con-fix (MINOR).** Si chiude **il candidato** (più in generale, la classe con dilatazione filtrata). **P1-Q7 in generale non è chiuso.**

**Enunciato dimostrato (S10A-T2f, candidato).**
- Ipotesi: 𝒜 = A₁ (Weyl), X = (x³+x)∂, Y = ∂, ε₀ ∈ ℂ∖{0} arbitrario.
- Tesi: non esistono una parola (Z_1..Z_d) ∈ {X,Y}^d e serie formali g_i ∈ tℂ[[t]] con e^{t(X+ε₀Y)} = Π_i e^{g_i(t)Z_i} in A₁[[t]].
- Conseguenza: per questa coppia la tesi di P1-T5 vale **senza** l'ipotesi «flussi di Y spenti a ε = 0» e senza analiticità in ε. Basta fissare un ε₀ ≠ 0 nel polidisco.

**Verifica passo per passo** (rifatta indipendentemente, `audit_items.py` (1a)–(1d)).
- **σ_μ.** x ↦ μx, ∂ ↦ ∂/μ è un automorfismo di A₁ per ogni μ ≠ 0. Dà σ_μX = μ²(X₀ + μ⁻²X₁), con X₀ = x³∂ e X₁ = x∂, e σ_μY = μ⁻¹∂.
  - σ_μ **non** preserva la sottoalgebra 𝒜₀ generata da X e Y. Si lavora quindi in A₁, e S10A-T2 va riletto con 𝒜₀ sostituito da A₁: è lecito, perché nessun passo usa 𝒜₀.
- **Sostituzione t = ν²s, ν = 1/μ.** A sinistra si ottiene e^{s(X_ν + ε₀ν³Y)}, con X_ν := X₀ + ν²X₁. I fattori X diventano e^{h_iX_ν}, h_i = Σ_k g_{i,k}ν^{2k−2}s^k (potenze pari). I fattori Y diventano e^{ŷ_iY}, ŷ_i = Σ_k g_{i,k}ν^{2k+1}s^k (potenze dispari ≥ 3). Corretto.
- **Passo 1.** Il coefficiente di s^m sta nello span delle parole di lunghezza ≤ m in X₀, X₁, Y (dimensione finita) ed è polinomiale in ν. L'identità vale per ogni ν ≠ 0, quindi è un'identità polinomiale. Corretto.
- **Passo 2 (mod ν³).** I fattori Y sono ≡ 1 e i fattori X commutano (stesso X_ν), quindi e^{sX_ν} ≡ e^{HX_ν}.
  - Il triage scrive solo «si ottiene H ≡ s». L'argomento di S10A-T2 va adattato, perché qui l'esponente è X_ν e non X.
  - Si prende il termine c·s^{p₀}ν^{q₀} di H − s con p₀ minimo e, a parità di p₀, q₀ minimo. Il suo coefficiente in e^{(H−s)X_ν} − 1 è cX₀ + c′X₁, dove c′ è il coefficiente di s^{p₀}ν^{q₀−2}, che è nullo per la minimalità di q₀. Quindi cX₀ = 0: assurdo.
  - Ne segue H ≡ s mod ν³, cioè Σ_X g_{i,1} = 1 e Σ_X g_{i,2} = 0. **Fix 1a (MINOR):** scrivere questo argomento.
- **Passo 3 (ordine ν³).** Contributi possibili:
  - a sinistra, solo un inserimento di ε₀ν³Y senza alcun X₁ (ν³ è dispari, X₁ porta ν²). Dà ε₀ volte il Duhamel con il solo X₀; verificato in (1a);
  - a destra, solo un fattore Y al suo ordine ν³ (coefficiente g_{i,1}s) con tutti gli altri fattori all'ordine ν⁰. Il termine (α) di S10A-T2, rX·e^{sX}, **manca** perché la parte X è pari. Verificato in (1b) sulla parola XYXYX con tempi formali simbolici;
  - si ottiene esattamente l'equazione del Passo 3 di S10A-T2 per la coppia omogenea (x³∂, ∂), con r = 0. Verificato in (1d).
  - **Fix 1b (MINOR):** scrivere esplicitamente il conteggio delle parità.
- **Passo 4 (Hankel).** Usa solo (H) per (X₀, Y) = (x³∂, ∂) fino a Y_{2p}. È P1-T5, esempio L4 con a = 3 (DIMOSTRATO).
  - **Osservazione (fix 1c, MINOR):** (H) per la coppia **originale** ((x³+x)∂, ∂), verificata dal triage, **non è usata** nella prova. La nota del LEDGER «candidato da verificare anche per (H)» è quindi irrilevante per la chiusura, anche se (H) vale (deg Y_k = 2k, (1c)).

**Kill-argument tentato.**
1. Contaminazione da X₁ all'ordine ν³. Esclusa per parità e verificata simbolicamente fino a s⁴.
2. Mancata invertibilità del Passo 2 per X_ν non omogeneo. Esclusa dall'argomento del termine minimo.
3. Uso implicito di 𝒜₀ ⊃ σ_μ(𝒜₀). Irrilevante, perché si lavora in A₁.

Nessuna lacuna trovata.

**Generalizzazione del triage (condizione sufficiente).** σ_μX = μ^α(X₀ + Σ_jμ^{−c_j}X_j), σ_μY = μ^βY₀, 𝔞 = α − β ∉ ⟨α, c_j⟩, (H) per (X₀, Y₀). Il conteggio regge con le seguenti precisazioni:
- c_j interi > 0 (o razionali, riparametrizzando come nella nota (2) di S10A-T2);
- α ≥ 0 e μ in un insieme infinito Λ;
- σ_μ endomorfismo di un'algebra che contiene X₀, X_j, Y₀;
- se α = 0, i fattori Y contribuiscono a ν^𝔞 con tutti i k, cosa innocua.

È un **abbozzo corretto ma non scritto**: lo registro come PROVA SCRITTA solo dopo la stesura.

**Cosa resta aperto.** P1-Q7 per le algebre con (H) prive di **qualunque** dilatazione, anche filtrata. È una riduzione più forte di quella attuale del LEDGER, ma resta una divisione in casi, non un'equivalenza.

---

## 2. P2-Q1-NL: Δ, m ≥ 1, dominio semplicemente connesso «con Poincaré»

**Verdetto: PASS-con-fix (MINOR)** sull'ipotesi.

**Lacuna (fix 2a, MINOR ma necessario).** Il Passo 3 applica Poincaré a f, primitiva olomorfa di h_z, di cui **non si sa ancora** che stia in L²(Ω). La disuguaglianza di Poincaré per funzioni di H¹(Ω) presuppone f ∈ L² ed è quindi circolare.

L'ipotesi giusta è:

> **(P′)** ogni f ∈ C^∞(Ω) con ∇f ∈ L²(Ω) sta in L²(Ω), cioè L^{1,2}(Ω) ⊂ L²(Ω).

Su domini non lipschitziani (P′) non è equivalente alla Poincaré per H¹ in generale. Va quindi enunciata come tale.

**Enunciato dimostrato.**
- Ipotesi: Ω ⊂ ℝ² aperto connesso, semplicemente connesso, di misura finita, che soddisfa (P′); P = Δ, Q₁ = ∂_z̄, Q₂ = ∂_z; m ≥ 1.
- Tesi: ker_{H^m(Ω)}Δ = 𝓗₁ + 𝓗₂ come insiemi. In particolare la somma è chiusa e densa. Non è diretta: l'intersezione è fatta dalle costanti.

**Prova (verificata).**
1. h_z è olomorfa e sta in H^{m−1}; qui si usa m ≥ 1.
2. Esiste una primitiva olomorfa f su Ω semplicemente connesso.
3. ∇f ∈ L², quindi f ∈ L² per (P′). Le derivate di ordine 1..m di f sono ∂_z^{k−1}h_z ∈ L², quindi f ∈ H^m.
4. h − f ∈ H^m e ∂_z(h − f) = 0.

**Disco con fessura D∖[0,1) (fix 2b, MINOR: semplificazione).**
- D∖[0,1) è l'unione di tre convessi limitati: il semidisco superiore, quello inferiore e D ∩ {Re z < 0}. È semplicemente connesso.
- Su un convesso limitato C, per f liscia con ∇f ∈ L²(C):
  - si esaurisce C con gli omotetici C_r, r ↑ 1;
  - la Poincaré sui C_r ha costante uniforme (C_r è convesso con diametro e misura limitati dal basso);
  - la media f_{C_r} resta limitata per confronto con una palla fissa;
  - per convergenza monotona f ∈ L²(C).
- f ∈ L² su ciascun pezzo implica f ∈ L² sull'unione. La «concatenazione delle medie» proposta dal triage **non serve**.
- Lo stesso vale per ogni Ω semplicemente connesso che sia unione finita di aperti convessi (o lipschitziani) limitati.

**Kill-argument tentato.**
- Per f non in L² con h ∈ L² servono domini senza (P′) («stanze e corridoi»), che sono fuori dall'ipotesi.
- Regolarità al bordo: la prova non ne usa.
- m = 0: escluso dall'ipotesi.

Nessun controesempio nell'ambito dichiarato.

**Portata.** Chiude solo il **caso modello**. P2-Q1-NL resta APERTO per P generale, per m = 0 e per i domini senza (P′).

---

## 3. SYS-DIRAC-POL a tempi complessi: Lemma E′ per crescita

**Verdetto: PASS-con-fix (MINOR).**

**Enunciato dimostrato.**
- Ipotesi: t, m ∈ ℝ∖{0}.
- Tesi: non esistono k ∈ ℕ e polinomi p_j, q_j ∈ **ℂ**[ξ] con Π_j e^{p_j(ξ)X}e^{q_j(ξ)mY} = e^{tA(ξ)} per ogni ξ in una semiretta [ξ₀, +∞), in particolare per ogni ξ ∈ ℝ. Qui X = iξσ_z, Y = −iσ_x.

**Lemma E′ (forma corretta da registrare).**
- Ipotesi: R_j ∈ ℂ[ξ] con R_i − R_j non costante per i ≠ j; d_j ∈ ℂ non tutti nulli; S = Σd_je^{iR_j}.
- Tesi: sia J₀ la classe degli indici con d_j ≠ 0 che minimizzano asintoticamente Im R_j (classe di equivalenza «Im R_j − Im R_{j₀} costante»), e siano d′_j = d_je^{Im R_{j₀} − Im R_j} per j ∈ J₀. Allora (1/X)∫_X^{2X}|S·e^{Im R_{j₀}}|² → Σ_{J₀}|d′_j|² > 0.
- Quindi una delle tre:
  - (i) se Im R_{j₀} è costante, S non tende a 0;
  - (ii) se Im R_{j₀} → −∞, la media quadratica di S esplode;
  - (iii) se Im R_{j₀} → +∞, si ha |S| ≤ Ce^{−cξ} per ξ grande.

**Verifiche.**
- In J₀ le Re R_j hanno differenze non costanti: R_i − R_j non è costante e la parte immaginaria della differenza lo è.
- I termini misti sono controllati dal Lemma E reale, nella forma corretta da C-10.
- Le classi non dominanti contribuiscono o(1) uniformemente su [X, 2X].
- Asintotica del bersaglio (`audit_items.py`): (e^{tA})_{11} = e^{iωt} + i(ξ/ω − 1)sin ωt in modo esatto, quindi G·e^{−iξt} = i m²t/(2ξ) + O(ξ^{−2}). Dunque |G| ~ |m²t|/(2ξ): tende a 0 in modo solo algebrico e G ≢ 0. Questo esclude (i), (ii), (iii) e anche il caso d ≡ 0.
- Esempio numerico del lemma con una classe dominante di due esponenziali: la media quadratica coincide con Σ|d′_j|² (scarto < 10⁻³).

**Fix (MINOR).**
- (3a) Enunciare il lemma come limite della media quadratica, non come «comparabile».
- (3b) Nel raggruppamento le costanti additive complesse vanno assorbite nei coefficienti (e^{ic}, c ∈ ℂ).
- (3c) Trattare a parte il caso «tutti i d_j nulli dopo il raggruppamento» (G ≡ 0, contraddetto dall'asintotica).
- (3d) Dichiarare che t e m sono reali. Per t non reale l'asintotica del bersaglio cambia: il termine e^{−iωt} può dominare. Il caso non è coperto e non è richiesto.

**Kill-argument tentato.** Si cercano cancellazioni tra classi esponenzialmente grandi che lascino un residuo algebrico. Sono impossibili: la classe dominante ha media quadratica Σ|d′|² > 0, quindi non si cancella. Nessuna lacuna.

---

## 4. Amitsur / Brešar–Šemrl: prova elementare

**Verdetto: PASS-con-fix (MINOR).** Copre **esattamente** l'uso del LEDGER.

**Uso nel LEDGER.**
- Riga F10-C «DICT-Q4-C, rango infinito ⇒ A(iii) — CON-FONTE (Amitsur 1965 / Brešar–Šemrl 1999)».
- `S10-OPEN-C/PROOF_PACKAGE.md` §16: «se ogni w ∈ Z ha D_0w..D_Nw dipendenti, esiste c ≠ 0 con rank(Σc_iD_i|_Z) ≤ N; allora rank(Σc_iD_i) ≤ N + codim Z < ∞».

**Enunciato dimostrato (lemma elementare).**
- Ipotesi: Z, V spazi vettoriali su ℂ, D_0..D_N: Z → V lineari (nessuna continuità richiesta), localmente linearmente dipendenti, cioè dim span{D_iu} ≤ N per ogni u.
- Tesi: esiste c ∈ ℂ^{N+1}∖{0} con rank(Σc_iD_i) ≤ r := max_u dim span{D_iu} ≤ N.

**Verifica dei passi.**
- (3)–(4) Il vettore α(s) dei minori con segno della matrice r × (r+1) dà Σα_iM_{k,i} = 0 (sviluppo di Laplace con una riga ripetuta).
- Per gli s cofiniti con det[φ_k(D_{i_l}(u₀+sw))] ≠ 0, i D_{i_l}(u₀+sw) sono indipendenti. Per massimalità di r generano span{D_i(u₀+sw) : i ∈ S}, su cui φ è iniettiva, quindi R(s) = 0.
- R è un polinomio a valori in uno spazio di dimensione finita, quindi R ≡ 0.
- (5)–(6) Derivando in 0: Σα_i(0)D_iw ∈ span{D_iu₀} (dimensione r), con α(0) indipendente da w e α_j(0) ≠ 0.

Corretto.

**Fix (MINOR).**
- (4a) Caso r = 0: tutti i D_i|_Z sono nulli. Il minore vuoto vale 1 e c = e_j.
- (4b) I φ_k sono funzionali lineari qualsiasi sul sottospazio di dimensione finita generato dai D_iu₀ e D_iw. Non serve Hahn–Banach né la continuità.
- (4c) Il massimo r esiste (interi ≤ N).
- Il passaggio «rank(Σc_iD_i) ≤ rank su Z + codim Z» del §16 è algebra lineare elementare.

**Script** (`audit_items.py`). L'algoritmo della prova, implementato alla lettera, su tre famiglie localmente dipendenti:
- prodotto vettore e_i × w;
- D_i = BC_i ristretti a un sottospazio Z;
- prodotto vettore più identità.

In tutti i casi dà c ≠ 0 con rango ≤ r.

**Kill-argument.** Si cerca una famiglia localmente dipendente in cui la combinazione costruita sia nulla con rango > r. È impossibile, perché il rango è ≤ dim span{D_iu₀} = r per costruzione. Nessuna lacuna.

**Conseguenza.** DICT-Q4-C «rango infinito ⇒ A(iii)» non dipende più da Amitsur e diventa **DIMOSTRATO** dopo la trascrizione del lemma con 4a–4c. Lo stesso vale per i corollari del §16 (operatori differenziali, moltiplicatori di Fourier, convoluzioni di Volterra). Per queste ultime resta Titchmarsh, già citato.

---

## 5. Björk: dim gr(A₂/A₂L) = 3 contro olonomo = 2

**Verdetto: PASS-con-fix (MINOR).** Copre **esattamente** l'uso del LEDGER (VAR-C3Q2-R (a′)).

**Uso nel LEDGER.** Riga F10-C «VAR-C3Q2-R (a′): olonomo ⇒ mai — CON-FONTE (Bernstein, Björk)». In `S10-OPEN-C` §6 (a′): «A₂/A₂L ha dimensione 3, un modulo olonomo ha dimensione 2; si usa la disuguaglianza di Bernstein».

**Enunciato dimostrato.**
- Ipotesi:
  - u un dato con Lu = 0, dove L ∈ A₂ è **non costante** (nel contesto L è monico di ordine m ≥ 1 in ∂_t);
  - A₂u olonomo nel senso d_B(A₂u) ≤ 2, con d_B la dimensione rispetto alla filtrazione di Bernstein (grado di Hilbert di una buona filtrazione), o in modo equivalente GKdim ≤ 2.
- Tesi: Ann_{A₂}(u) ≠ A₂L.

**Verifiche.**
- gr_B A₂ = ℂ[x,t,ξ,τ] è un dominio, quindi deg(QL) = deg Q + deg L e σ(QL) = σ(Q)σ(L). Ne segue gr(A₂L) = σ(L)·gr(A₂) per la filtrazione indotta. Verificato su 20 Q casuali con moltiplicazione esatta in A₂ (`audit_items.py`).
- dim F_j(A₂/A₂L) = C(j+4,4) − C(j−d+4,4), di grado 3 in j.
- Se Ann(u) = A₂L, allora A₂u ≅ A₂/A₂L ha dimensione 3 > 2: contraddizione.
- La disuguaglianza di Bernstein (d ≥ 2 per M ≠ 0) **non serve**, né con la definizione «d ≤ 2» né con «d = 2».

**Fix (MINOR).**
- (5a) Fissare la definizione di «olonomo» con la filtrazione di Bernstein o con GKdim. Nel progetto non è fissata (nessuna occorrenza in NOTAZIONE). Se fosse definito con la filtrazione per ordine (varietà caratteristica), il confronto delle dimensioni è un teorema non banale e la sostituzione non basterebbe.
- (5b) Scrivere il lemma «la dimensione non dipende dalla buona filtrazione» (Γ_j ⊂ Γ′_{j+c} e viceversa) e l'invarianza per isomorfismo.
- (5c) Escludere L costante: per L ∈ ℂ∖{0} si ha u = 0 e A₂/A₂L = 0.

**Cosa non copre.** Affermazioni del tipo «u razionale (o D-finita) ⇒ A₂u olonomo». Queste richiedono la teoria di Bernstein (localizzazione) e restano CON-FONTE dove usate.
- In `S10-INT/ESEMPI.md` d3 compare «razionale, quindi olonomo» come etichetta del modello M3-hol. Lì l'identificazione è in ℂ[∂], non in A₂, quindi (a′) non è applicata e non c'è conflitto.
- La riga OP-ALG-P5 del LEDGER (r. 112, «in A_2 intero una soluzione olonoma non identifica mai») è un enunciato affine. Non ho verificato su quale argomento poggi.

**Kill-argument.** Si cerca u olonomo con Ann principale. Per u = e^{x+t} si ha Ann = A₂(∂_x−1) + A₂(∂_t−1), che non è principale. Nessun controesempio, coerentemente con la prova.

---

## 6. S10B-V9: δ₅(10) = 6, δ₅(9) = 7, δ₅(8) = 9, δ₆(12) = 7

**Verdetto sul triage: PASS-con-fix (MAJOR) per i valori come presentati.** I numeri sono corretti, ma l'argomento AM dipende da un'ipotesi **non dimostrata**. Con la riesecuzione indipendente descritta sotto, che **non** usa quell'ipotesi, i valori diventano condizionali solo a L8/L8′ e ai maggioranti già registrati.

### 6.1 Audit di `tri_delta.py` (lettura del codice)
- **Aritmetica.** int64 con p = 2³¹−1: i prodotti sono < 2⁶², quindi non c'è overflow. Il rango è calcolato per eliminazione di Gauss corretta.
- **Classi di peso.** wt y_j = j + 2 e i monomi sono di grado ≤ d. Il controllo peso per peso è lecito perché la famiglia AM è omogenea pesata (x ↦ λx, τ_n con il peso corrispondente). Il grado minimo di una relazione è il minimo sulle classi di peso; la ricerca sui soli pesi difettosi è corretta.
- **Imprecisione (MINOR).** Il triage dice «riduzione mod p di una matrice razionale». In realtà i punti sono F_p-punti di una famiglia razionale (parametri casuali mod p). L'argomento corretto: una relazione q su ℚ, primitiva, dà q∘param ≡ 0 su ℚ, quindi anche mod p (coefficienti p-interi), quindi rango non pieno mod p. La conclusione resta valida.
- **Ipotesi AM.** Il triage usa «i getti AM generici stanno in cl(S°₀)». **Non è dimostrata da nessuna parte nel LEDGER.** Adler–Moser compare solo in ENC-K1 (CON-FONTE da verificare, per un altro uso) e in CIT-AUDIT-6 (solo metadati, «testo non letto»).
- **Osservazione dell'auditor: serve meno.** La prova di L8 (fix F5C-4) mostra che la forma iniziale p⁺ di una relazione sta in (F⁺) e quindi si annulla su **tutto** V(F⁺) = Z₀ = Ψ₀^{−1}(M₀), non solo su cl(S°₀). Per il minorante basta quindi:

  > **(AM-Z₀)** i getti AM soddisfano l'identità stazionaria pura 2GG″ − G′² + 4(u+λ)G² = 4λ^{2N+1}, con G = Σ_{j≤N}g_jλ^{N−j} e i g_j di Gelfand–Dickey a costanti nulle.

  Questa identità dà Ψ₀(getto) ∈ M₀ e anche y_{2N} = Φ(0; ·), che serve per L8′ a K = 2N. Anche (AM-Z₀) è **non dimostrata** nel progetto: è il teorema classico di Adler–Moser / Airault–McKean–Moser, mai letto.

### 6.2 Riesecuzione indipendente (`audit_delta.py`)
**Implementazione nuova.** Primo p = 10⁹+7, diverso da 2³¹−1 (triage) e da 2147483629 (pacchetto); semi diversi. Due generatori di punti.

- **(S) strato principale S°₀, rigoroso mod L8/L8′, senza ipotesi AM.**
  - Si costruisce U = Π(λ + σ_j²) con σ casuale e V interpolante, con V(−σ_j²) = σ_j^{2N+1} (cioè ν² + f(μ) = 0, f = λ^{2N+1}). È la parametrizzazione σ di OPF5C-T1(b) a k = 0. Lo script verifica (assert) U | V² + f.
  - I getti y_0..y_{2N−1} si ottengono invertendo la mappa triangolare (u_j = g_j, v_j = Dg_j/2) con i polinomi di Gelfand–Dickey ricalcolati da zero, dalla ricorrenza algebrica del risolvente. Si verifica che g_1 = −y_0/2 e g_2 = y_2/8 + 3y_0²/8 coincidono con le convenzioni OP-F5C. L'inversione è controllata.
  - y_{2N} si ricava dal flusso di Mumford V′ = (V² + f)/U − (y_0 + λ)U.
  - Rango pieno mod p dà assenza di relazioni su ℚ, quindi su ℂ, per lo stesso argomento di riduzione della parametrizzazione (denominatori di Vandermonde non nulli).
- **(W) Adler–Moser via funzione di Schur** della partizione a scala (N, …, 1) nei tempi dispari t₁ = x, t₃, …, t_{2N−1}.
  - È una costruzione diversa dalla ricorrenza di Adler–Moser del triage: Jacobi–Trudi, poi interpolazione in x, poi serie di log.
  - In più, `Wcheck` verifica in punti casuali l'identità stazionaria pura a k = 0, come serie in h fino all'ordine 2N + 2, e che U(x₀) sia squarefree.
  - Il controllo negativo con θ casuale **fallisce**, come atteso.

**Validazione (valori noti).** Tutti coincidono con il LEDGER e con il pacchetto:
- δ₁(2) = 2, δ₂(4) = 3, δ₂(3) = 4, δ₃(6) = 4, δ₃(5) = 5, δ₃(4) = 7;
- δ₄(8) = 5, δ₄(7) = 6, δ₄(6) = 8 (S); δ₂(4), δ₃(6), δ₃(4), δ₄(8) (W).

**Risultati** (`audit_delta_run{A,B,C}.out`).

| caso | gen. | esito | tempo |
|---|---|---|---|
| N=5, K=10, d ≤ 5 | S | nessuna relazione ⇒ δ₅(10) ≥ 6 | 1.7 s |
| N=5, K=10, d ≤ 5 | W | nessuna relazione | 1.9 s |
| N=5, K=10, d ≤ 6 | S | relazione di grado minimo 6 (coerente con OPR2-P4; conferma anche y_{2N} dal flusso) | 25 s |
| N=5, K=9, d ≤ 6 | S | nessuna relazione ⇒ δ₅(9) ≥ 7 | 7.2 s |
| N=5, K=9, d ≤ 6 | W | nessuna relazione | 8.2 s |
| N=5, K=9, d ≤ 7 | S | relazione di grado minimo 7 (coerente con P7(a)) | 91 s |
| N=5, K=8, d ≤ 8 | S | nessuna relazione ⇒ δ₅(8) ≥ 9 | 173 s |
| N=5, K=8, d ≤ 8 | W | nessuna relazione | 198 s |
| N=6, K=12, d ≤ 6 | S | nessuna relazione ⇒ δ₆(12) ≥ 7 | 214 s |
| N=6, K=12, d ≤ 6 | W | nessuna relazione | 221 s |
| N=6, K=11, d ≤ 7 | S | nessuna relazione ⇒ δ₆(11) ≥ 8; con P7(a) (≤ N+2 = 8) **δ₆(11) = 8** (caso che il triage non aveva concluso; congettura N+2 confermata per N = 6) | 1223 s |
| Wcheck N = 2..6 | W | identità stazionaria pura verificata, U(x₀) squarefree, U(0) ≠ 0 | < 1 s |

**Conclusioni.**
- Con i maggioranti:
  - δ₅(10) = 6 e δ₆(12) = 7 seguono da OPR2-P4 (δ_N(K) ≤ N+1 per K ≥ 2N, DIMOSTRATO mod (Nov)) e da L8′;
  - δ₅(9) = 7 segue da OPF5C-P7(a) (≤ N+2) e da L8; era già DIMOSTRATO nel LEDGER (r. 190) e qui è riprodotto;
  - δ₅(8) = 9 segue da OPF5C-P7(b) (≤ N+4) e da L8;
  - δ₆(11) = 8 (nuovo, una sola implementazione) segue da OPF5C-P7(a) e da L8. Va riprodotto prima di essere promosso.
- **Dipendenze esatte:**
  - L8 (DIMOSTRATO, F5C-4) e L8′ (DIMOSTRATO, F10-B2);
  - (Nov)/(Nov′) per i maggioranti (CON-FONTE verificata);
  - correttezza del calcolo mod p, ora riprodotto da due implementazioni indipendenti.
- **Non** dipendono da AM ⊂ cl(S°₀), che è richiesta solo dal generatore AM del triage. Per quest'ultimo il controllo `Wcheck` è evidenza probabilistica (identità polinomiale verificata in punti casuali mod p), non una prova.

---

## Tabella finale

| item | verdetto | stato proposto per il LEDGER | enunciato esatto in una riga |
|---|---|---|---|
| 1. P1-Q7, candidato (x³+x)∂, ∂ | PASS-con-fix MINOR (1a–1c) | candidato: **DIMOSTRATO** dopo la stesura dei Passi 2–3 (fix 1a, 1b); generalizzazione «dilatazione filtrata»: **PROVA SCRITTA** (abbozzo); P1-Q7 generale: **APERTO** | In A₁, per X=(x³+x)∂, Y=∂ e ogni ε₀≠0 non esistono una parola finita e g_i∈tℂ[[t]] con e^{t(X+ε₀Y)}=Πe^{g_iZ_i}; usa solo (H) per (x³∂,∂). |
| 2. P2-Q1-NL, Δ | PASS-con-fix MINOR (2a ipotesi (P′), 2b) | **DIMOSTRATO** (caso modello) dopo la stesura con (P′); P2-Q1-NL generale **APERTO** | Ω⊂ℝ² connesso, semplicemente connesso, di misura finita, con L^{1,2}(Ω)⊂L²(Ω) (per es. disco con fessura), m≥1: ker_{H^m}Δ = ker_{H^m}∂_z̄ + ker_{H^m}∂_z. |
| 3. SYS-DIRAC-POL complesso | PASS-con-fix MINOR (3a–3d) | **DIMOSTRATO** dopo la stesura | Per t,m∈ℝ∖{0} non esistono k e p_j,q_j∈ℂ[ξ] con Π_j e^{p_jX}e^{q_jmY}=e^{tA(ξ)} per ξ in una semiretta (Lemma E′: S esponenziale-polinomiale ≢0 non tende a 0 in modo algebrico). |
| 4. Amitsur / Brešar–Šemrl | PASS-con-fix MINOR (4a–4c) | DICT-Q4-C «rango infinito ⇒ A(iii)»: **DIMOSTRATO** (la fonte esce dalle dipendenze) | D_0..D_N: Z→V lineari, localmente dipendenti ⇒ ∃c≠0 con rank(Σc_iD_i) ≤ max_u dim span{D_iu} ≤ N. |
| 5. Björk | PASS-con-fix MINOR (5a–5c) | VAR-C3Q2-R (a′): **DIMOSTRATO** con «olonomo» definito da d_Bernstein ≤ 2 (Bernstein/Björk escono) | L∈A₂ non costante, Lu=0, d_B(A₂u)≤2 ⇒ Ann_{A₂}(u)≠A₂L, perché d_B(A₂/A₂L)=3. |
| 6. S10B-V9 | PASS-con-fix MAJOR (ipotesi AM non dimostrata; superata dalla riesecuzione S) | δ₅(10)=6, δ₅(8)=9, δ₆(12)=7: **DIMOSTRATO (computer-assisted) mod (Nov)/(Nov′)** via L8/L8′; δ₅(9)=7 già DIMOSTRATO, riprodotto; «AM ⊂ cl(S°₀)»: **APERTO** (non dimostrato nel LEDGER; basta AM ⊂ Z₀) | Per ogni k∈U₀: δ₅(10)=6, δ₅(9)=7, δ₅(8)=9, δ₆(12)=7 (minoranti mod p su S°₀ a k=0 + L8/L8′; maggioranti OPR2-P4, OPF5C-P7). |
