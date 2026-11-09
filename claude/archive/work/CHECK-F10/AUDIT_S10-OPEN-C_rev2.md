# AUDIT_S10-OPEN-C_rev2 — S-CHECK-F10-C2 (27/10/2026)

Revisore: S-CHECK-F10-C2, indipendente da S10-OPEN-C. Oggetto: la sezione «Recepimento dell'audit (rev2)» in coda a `work/S10-OPEN-C/PROOF_PACKAGE.md` (righe 503–751), letta contro `work/CHECK-F10/AUDIT_S10-OPEN-C.md`. Ho riletto riga per riga R.1 (C-15), R.2 (C-17) e R.3 (C-19), ho controllato velocemente R.4 (fix C-1…C-24), R.5 e R.6, e ho cercato in tutta la cartella `work/S10-OPEN-C/` le etichette «ridotto a». Non ho eseguito nessuno script di `_vendor`.

**Verifiche al calcolatore.**
- `work/S10-OPEN-C/sympy/rev2_checks.py`, rieseguito con `D:\ProblemaBase\.venv\Scripts\python.exe -I`: **43/43 OK**. Coincide con quanto dichiarato dal pacchetto (tracce regolarizzate −4.8147, −5.1269, −5.1953).
- `work/CHECK-F10/sympy/c2_checks.py`, script mio, stesso interprete con `-I`: **21/21 OK**. Usa metodi diversi da quelli di rev2_checks:
  - per R.1, la serie di Tychonoff troncata (la lacuna di C-15 esiste davvero), un esempio esplicito in 𝒮_c, e un operatore di Volterra simmetrico discretizzato (nilpotente, con la stima ‖𝒱^n‖ ≤ (2‖k‖a)^n/n!);
  - per R.2, le tre righe della derivazione di (i) prese una per una; κ su una coppia nuova (u = boost di Galileo, φ = gaussiana libera); la costruzione di ψ per quadratura con il controllo L_0ψ ≈ 0 alle differenze finite (|L_0ψ| ≤ 9·10^{−10}), più un controllo negativo con c′ = 0;
  - per R.3, il passo 1 nel caso limite Lip φ = L con uno spigolo; la conclusione del lemma su un dominio a L con angolo rientrante, anche a distanza 10^{−8} dall'angolo; |Γ(L, r)| in N = 3 (formula chiusa e Monte Carlo); l'uniformità in R della costante c_0 del passo 3 di §13.

Nessun verdetto si appoggia sul solo calcolo.

## 1. Verdetti

| claim | fix | verdetto | stato proposto |
|---|---|---|---|
| ENC-Q4-S (a) | C-15 (R.1) | **PASS** | **DIMOSTRATO** |
| ENC-Q10-D (i), (ii) | C-17 (R.2) | **PASS** | **DIMOSTRATO** |
| DICT-ILIM-Hs | C-19 (R.3) | **PASS** | **DIMOSTRATO**; Adams–Fournier esce da «CIT da verificare» |

Le osservazioni qui sotto sono di dicitura e non toccano la correttezza. Le metto come suggerimenti, non come condizioni.

## 2. R.1 — C-15, ENC-Q4-S: PASS

**Passo 0.** G := {t : u(t, ·) ≢ 0} è aperto: se u(t_1, x_1) ≠ 0, la continuità di t ↦ u(t, x_1) (u è C¹ in t) dà u(t, x_1) ≠ 0 vicino a t_1. G è non vuoto perché u ≠ 0. Una componente G_0 è un intervallo aperto non vuoto. Fuori da G si ha u = u′ = 0 su quella fetta, e la prova non ne ha bisogno. Corretto. Il paragrafo «Che cosa era sbagliato» è giusto: la mia verifica con la Tychonoff troncata conferma che esistono soluzioni libere con u(t, ·) ≡ 0 su un insieme di tempi e u(t, 0) = g(t) > 0 altrove.

**Passo 1.** Vicino a t_1 vale e^{iθ_1(t)} = u′(t, x_1)/u(t, x_1), che è C¹ perché u e u′ sono soluzioni classiche. Una mappa C¹ da un intervallo nel cerchio ha un sollevamento C¹. Il sollevamento può differire dal θ_1 originale per multipli di 2π punto per punto, ma u′ = e^{iθ_1}u non cambia. Corretto. Non serve alcuna ipotesi di misurabilità su θ_1, e l'osservazione finale di R.1 lo dice bene.

**Passo 2.** Con V′ = V + δ si ha iu′_t + u′_xx − V′u′ = e^{iθ_1}[(iu_t + u_xx − Vu) − θ_1′u − δu] = (−θ_1′ − δ)e^{iθ_1}u. Il segno è giusto (S8-ENC: iu_t = −u_xx + Vu). In ogni t ∈ G_0 esiste x con u ≠ 0, quindi θ_1′ ≡ −δ e θ_1 = κ − δt su G_0, con κ reale. Corretto (verificato anche su u = e^{−ict}(x² + 2it)).

**Passo 3.** L'ipotesi per assurdo è scritta con θ: I → ℝ arbitraria, come richiede il quoziente DM-φ. w e w′ sono libere per ENC-1 con c_V = 0, N_V = I, e gli operatori agiscono solo in x e sono invertibili su C(J). Corretto.

**Passo 4.** w(t, ·) ≢ 0 su G_0 per iniettività di W_V. Il sollevamento locale di θ è costruito come nel passo 1, perché w e w′ sono C¹ in t. L_0(e^{iθ}w) = −θ′e^{iθ}w, quindi θ′ ≡ 0 e θ ≡ θ_0 su G_0 connesso. Corretto.

**Passo 5.** W_{V′} è ℂ-lineare e agisce solo in x, quindi la fase e^{i(κ − δt)} esce. Zw = μw con μ(t) = e^{i(θ_0 − κ + δt)} e w(t) ≠ 0. L'algebra è corretta.

**Passo 6.** Z = W_{V′}W_V^{−1}. Serve che W_V^{−1} abbia la stessa forma di Volterra simmetrica. §11 passo 6 lo dichiara («W_{V′}^{±1} ha la stessa forma») e lo dà ENC-1; in ogni caso la serie di Neumann di un Volterra simmetrico quasinilpotente è ancora di quella forma. La chiusura per composizione (|r| ≤ |s| ≤ |x|) e la stima G_{n+1}(ρ) ≤ 2‖k‖∫_0^ρG_n sono corrette e indipendenti da u.

**Passo 7.** 𝒱w(t) = (μ(t) − 1)w(t) con w(t) ≠ 0, quindi μ − 1 ∈ σ_p(𝒱) ⊂ {0}. Allora θ_0 − κ + δt ∈ 2πℤ su G_0: una funzione continua a valori discreti su un connesso è costante, quindi δ = 0 perché G_0 ha interno. Contraddizione. Corretto.

**Osservazioni (non bloccanti).**
- Il «Quadro» di R.1 usa J = [−a, a] chiuso, mentre il primo audit parlava di I × J°. Basta che u(t, ·) ∈ C(J) per far agire W_V su C(J), ed è quanto il quadro assume. Coerente con §11.
- Il simbolo κ indica qui una costante reale, mentre in R.2 κ(t) è una funzione complessa. Le sezioni sono separate, quindi nessuna ambiguità reale.

Il passo che il primo audit aveva segnalato come falso è riparato esattamente come proposto da C-15, e l'enunciato (a) è invariato. **PASS. Stato: DIMOSTRATO.**

## 3. R.2 — C-17, ENC-Q10-D: PASS

**(i), a mano.** Ho rifatto i quattro conti.
- U_t = ∂_x(u_t/u), perché U = ∂_x log u. Con iu_t = −u_xx e u_xx/u = U_x + U² si ottiene iU_t = −U_xx − 2UU_x. Corretto.
- iχ_t = ∂_x(iφ_t) − iU_tφ − U(iφ_t) = −φ_xxx − iU_tφ + Uφ_xx. Corretto.
- χ_xx = φ_xxx − U_xxφ − 2U_xφ_x − Uφ_xx. Corretto.
- Sommando, φ_xxx e Uφ_xx si cancellano, e −iU_t = U_xx + 2UU_x dà L_0χ = 2UU_xφ − 2U_xφ_x = −2U_x(φ_x − Uφ) = V_1χ. Corretto, con il segno di §12 (iχ_t + χ_xx = V_1χ).

Il nucleo su ogni fetta è ℂu perché Λf = u∂_x(f/u), u ≠ 0 e J è connesso. Verificato per u, φ generiche e sulla coppia nuova (boost, gaussiana).

**(ii), formula di κ.** W = uφ_x − u_xφ = uχ. W_x = uφ_xx − u_xxφ, perché i termini u_xφ_x si cancellano. ∂_t(φ/u) = (uφ_t − φu_t)/u² = iW_x/u² = i(χ_x + (u_x/u)χ)/u. Il secondo membro dipende solo da χ e da u. Corretto.

**ψ libera.** Λψ = χ per costruzione. ψ − φ ∈ ker Λ, quindi ψ − φ = a(t)u con a = c − (φ/u)(·, x_0), che è C¹. L_0(au) = ia′u, perché u è libera. Quindi ψ è libera ⟺ a′ ≡ 0 ⟺ c′ = iκ. κ è continua (χ, χ_x, u, u_x lo sono), quindi c esiste ed è C¹. Corretto. Sulla coppia nuova la ψ costruita per quadratura soddisfa L_0ψ ≈ 0 (9·10^{−10}), mentre con c′ = 0 il residuo è grande.

**Unicità modulo ℂu.** ψ̃ − ψ = b(t)u e ib′u = 0, quindi b è costante. Corretto.

**C-18.** Ho verificato a mano L_0(e^{iΦ}g) = e^{iΦ}(L_0v)(t, x − 2kt) con Φ = kx − k²t, e V_1 = 2/(x − 2kt + a)². La condizione di regolarità J ⊂ (2k sup I − a, ∞) è giusta per k > 0 e I limitato. La riformulazione del residuo («esempi non riconducibili per simmetria») è quella chiesta dal primo audit.

**Osservazione (non bloccante).** In R.2, W indica il Wronskiano, mentre in §11 W_V indica l'encoder. Se il testo viene fuso nel corpo di §12, conviene chiamare il Wronskiano 𝒲 o Wr.

Il passo delegato a SymPy è ora una derivazione completa a mano, come chiedeva C-17, e include anche (i). **PASS. Stato: DIMOSTRATO.**

## 4. R.3 — C-19, DICT-ILIM-Hs: PASS

**Definizione.** Il bordo lipschitziano è definito con un moto rigido che fissa p, quindi B(p, r_p) è la stessa palla nelle due coordinate. È la definizione standard.

**Passo 1.** Se x ∈ Ω ∩ B(p, r_p/2) e |z| < r_p/2, allora x + z ∈ B(p, r_p). Inoltre x_N > φ_p(x′), e la lipschitzianità dà φ_p(x′ + z′) ≤ φ_p(x′) + L_p|z′| < x_N + z_N. Quindi x + z ∈ Ω. Corretto. L'ho controllato anche nel caso limite (Lip φ = L esatta, con uno spigolo, x a distanza 10^{−12} dal grafico).

**Passo 2.** Se L ≥ L_i e h ≤ r_i/2, allora Γ(L, h) ⊂ Γ(L_i, r_i/2): il cono più stretto sta in quello più largo. Corretto.

**Passo 3.** |x − p_i| < r_i/4 + d_0 ≤ r_i/2, perché d_0 ≤ r_i/4. Corretto.

**Passo 4.** Se dist(x, ∂Ω) ≥ d_0, la palla aperta B(x, d_0) non incontra ∂Ω. È connessa e contiene x ∈ Ω, quindi sta in Ω. Γ(L, d_0) ⊂ B(0, d_0). Corretto.

**Proprietà usate in §13.**
- Γ è convesso, perché z_N − L|z′| è concava. È stellato rispetto al vertice, quindi il segmento (x, y] sta in C_x ⊂ Ω e il resto di Taylor è lecito.
- C_{x,r} = C_x ∩ B_r(x) per r ≤ h, e |Γ(L, r)| = r^N|Γ(L, 1)|. Ho verificato N = 3 con formula chiusa e Monte Carlo, che si aggiungono al caso N = 2 di rev2_checks.
- La costante c_0 è uniforme sulle rotazioni: è una rappresentazione continua di un gruppo compatto su uno spazio di dimensione finita. Numericamente, per s = 2 e N = 2, c_0 oscilla tra 34.2 e 36.5.
- Il passaggio da Ω a Ω̄ è corretto: le D^βf sono continue su Ω̄ e Ω è denso in Ω̄. La correzione di §13 passo 1 (vertice e cono in Ω) è segnalata nel corpo con un rimando.

Sul dominio a L, con l'angolo rientrante, un cono congruente fisso (semiapertura π/8, h = 0.05) entra in Ω da ogni punto campionato, anche vicinissimo all'angolo. È coerente con il lemma: un dominio a L è lipschitziano.

**Osservazioni (non bloccanti).**
- L'enunciato chiede L > 0. Se tutte le L_i sono nulle, basta prendere L := max(1, max_iL_i): un cono più stretto continua a stare dentro.
- Il moto rigido R_p può avere determinante −1. Componendo con la riflessione z_1 ↦ −z_1, che lascia invariato Γ, si ottiene una rotazione propria, come dice l'enunciato.

Il lemma è elementare, completo e sostituisce la CON-FONTE. **PASS. Stato: DIMOSTRATO.**

## 5. Fix redazionali C-1…C-24 (controllo veloce)

Tutti i ventiquattro fix sono presenti in R.1–R.4, con testo o con rimando. Ho riletto in particolare:
- C-1: limite sinistro e «classica ⇒ mite»;
- C-4: v ∈ L^∞ tramite la proprietà di Radon–Nikodym;
- C-5: termine di bordo −k(0)y;
- C-7: τ_2 = τ_1 esplicito e Gronwall per la continuità in ω;
- C-8: Touchard e indipendenza algebrica via y → +∞;
- C-10: maggiorazione del Lemma E, riportata anche in §7;
- C-11: E_𝒪 addendo diretto libero, riduzione modulo 𝔪;
- C-20: resto di Lagrange e polinomio nodale 2(Λ/4)^J, con il fattore 2 in (iv);
- C-22: fedele piattezza, b𝒪̂ ∩ 𝒪 = b𝒪;
- C-23: suriettività di Ψ;
- C-24: |u_2| ∈ [δ_0, M] per ε ≤ (M − δ_0)/4, derivate ≤ (M − δ_0)/2, supporto per ε ≤ (d/R)³.

Sono tutti corretti. Nel corpo sono già aggiornati §2 (enunciato), §6, §7 riga 239, §10 (enunciato con C-14), §11(c), §12(c), §13 passo 1, §14 passo 1 e §17 (rimando).

Un residuo cosmetico: in §2, riga 106, la conclusione della prova dice ancora «Per 0 < t < π/n si ha C(t) ≠ 0», mentre l'enunciato corretto (riga 89) vale per ogni t con sin(nt) ≠ 0. R.4 dà l'argomento giusto (y(t) ∉ D(A) se sin(nt) ≠ 0), e la sezione rev2 prevale, quindi non è un errore. Conviene allineare quella riga.

## 6. Etichette «ridotto a»

- **PROOF_PACKAGE.md: pulito.** Le sole occorrenze sono a riga 6, nella definizione, che riserva l'etichetta alle riduzioni provate e dichiara che non ce ne sono, e nella colonna «prima» della tabella R.5. Tutte e otto le sedi del primo audit (§4 del primo audit) sono ora «APERTO», «riformulato come» o «sottodomanda». Nella tabella §0 restano gli esiti «(c)», ma secondo la definizione rev2 di riga 6 «(c)» comprende ora «APERTO — riformulato/sottodomanda». Va bene.
- **LEDGER_ROWS.md: non pulito.** Le righe 10 (VAR-Q18-mult), 13 (VAR-Q17(b)), 14 (VAR-P12), 20 (ENC-Q4-S, lettura DM3) e 24 (DICT-Q3-R) contengono ancora «APERTO — ridotto …». La riga 14 conserva anche «(d) FALSO nella classe quadratica». R.6 lo dichiara apertamente («LEDGER_ROWS.md non è stato modificato»), quindi non è una incoerenza nascosta. Però le righe proposte al coordinatore contengono ancora etichette non dimostrate. **Fix C2-1:** applicare a LEDGER_ROWS le correzioni di AUDIT_S10-OPEN-C §5 e la tabella R.6 prima della registrazione. È lavoro di trascrizione e non tocca i tre verdetti.
- STATO_PARZIALE.md riga 23 e PLAN.md sono documenti storici di sessione e si possono lasciare. Se STATO_PARZIALE viene ancora usato come riepilogo, conviene aggiornare la riga 23.

## 7. Conclusione

Le tre prove riscritte sono corrette riga per riga. Recepiscono esattamente C-15, C-17 e C-19, e nessuna si appoggia sul calcolo. ENC-Q4-S (a), ENC-Q10-D (i)–(ii) e DICT-ILIM-Hs possono passare a **DIMOSTRATO**: è la rilettura chiesta dal criterio del primo audit. Unica azione residua prima della registrazione: C2-1, cioè allineare LEDGER_ROWS.md a R.6.
