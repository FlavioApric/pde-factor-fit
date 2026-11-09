# AUDIT S8-ENC rev. 2 — S-CHECK-F8-ENC · 27/10/2026

Revisore: S-CHECK-F8-ENC (mini-audit richiesto dalla coordinatrice). Oggetto: i sei claim nuovi della rev. 2 di `work/S8-ENC/PROOF_PACKAGE.md` (§3 e §4), elencati in `CHECK_REQUEST.md` sezione "Rev. 2" (R1–R7), più un controllo a campione del recepimento dei fix ENC-1…ENC-15 (`RECEPIMENTO.md`) e dei declassamenti a FALSO. L'audit precedente resta in `AUDIT_S8-ENC.md`, e la numerazione dei nuovi fix riparte da ENC2-1.
Verifiche indipendenti: `work/CHECK-F8/sympy/enc2_check_rev2.py` → `enc2_check_rev2.out` (**15/15 OK**). Gli script dell'autore (`enc_recep.py`) non sono stati usati come prova.
Kill-argument breve su ENC-P0(b)^cl ed ENC-T2(c′), indicati dalla coordinatrice come vicini al cammino critico ENC-1 → C1 → T2 → R6 (di fatto R6 non li usa): `KA_ENC2_input.md` (estratto verbatim), `KA_ENC2_attack.md` (subagente indipendente, script `sympy/enc2_ka_checks.py`), `KA_ENC2_adjudication.md`. Esiti in §3.

## 0. Verdetti sui claim nuovi

| ID | verdetto | fix | stato proposto |
|---|---|---|---|
| ENC-P0(b)^cl | PASS-con-fix: la prova è corretta, ma le ipotesi non sono coerenti (V solo continuo, W definito solo su C^∞); "equivalentemente" non provato (KA P1, P4, P5) | **ENC2-1 (MAJOR)** | **DIMOSTRATO** dopo ENC2-1 |
| ENC-P0(b)^loc | **FAIL come scritto, PASS dopo fix**: controesempio esplicito del KA (P2), perché il nucleo è chiesto finito solo su C^∞_c(U) | **ENC2-1 (MAJOR)** | **FALSO come scritto**; **DIMOSTRATO** dopo ENC2-1 |
| ENC-P0′ su nucleo denso | PASS: prova corretta senza (H-P0); va scritto 0 ∈ I | ENC2-2 (MINOR) | **DIMOSTRATO** |
| esempi di P0′ su 𝒮(ℝ) | PASS-con-fix: lente e classe β(t)x + γ(t) verificate (L1–L3, BG1–BG2); Avron–Herbst è chiamato "istanza di P0(a)", che richiede (H-P0) | ENC2-3 (MINOR) | identità **DIMOSTRATO**; unicità del gruppo ed essenziale autoaggiuntezza **CON-FONTE** |
| ENC-P0′-DIC | **FAIL come scritto, PASS nella forma corretta**: "θ ≠ id ⟺ α ≢ 0" è falso per i singoli rappresentanti (V = 0 ha il rappresentante pseudo-conforme con θ(t) = t/(1 + 4a_0t), DIC3); vale "esiste un rappresentante con θ = id ⟺ α ≡ 0" | **ENC2-4 (MAJOR)** | **FALSO come scritto**; **DIMOSTRATO** nella forma di ENC2-4, con Bluman–Shtelen CON-FONTE per la forma dell'ansatz |
| POLE-N^cl | PASS-con-fix: il passaggio "∂_tW = 0" è corretto (POLE2); la scelta di un intervallo libero da poli "ai due tempi" non basta, serve un rettangolo [s, t] × U libero da poli (POLE3) | ENC2-5 (MINOR) | **DIMOSTRATO** dopo ENC2-5 |
| ENC-T2(c′) | PASS-con-fix: termine di ordine minimo, caso d = 0 e caso M = 2d verificati anche con q non polinomiale (T2c′1–T2c′4); "certifica" non definito, e con vincoli di grado l'enunciato è falso (KA P7) | **ENC2-6 (MAJOR)** | **DIMOSTRATO** (osservazione) nella classe C^∞(Ω) senza vincoli, dopo ENC2-6; con vincolo di grado **FALSO**; nella classe degli annullatori principali **APERTO** |

Nessun FATAL, nessun CRITICAL. Tre MAJOR (ENC2-1, ENC2-4, ENC2-6), tutti riparabili in una o due righe; due claim nuovi sono FALSI come scritti (ENC-P0′-DIC, ENC-P0(b)^loc) e veri dopo il fix. Riepilogo dei verdetti: PASS 1 (P0′ su nucleo denso); PASS-con-fix 4 (P0(b)^cl, esempi su 𝒮, POLE-N^cl, T2(c′)); FAIL come scritti e PASS dopo il fix 2 (P0(b)^loc, P0′-DIC). **Il cammino critico ENC-1 → ENC-C1 → ENC-T2 → R6 non è toccato**: ENC-T2(a)(b)(c) e ENC-C1 sono invariati rispetto all'audit precedente (verificato sul testo), e ENC-T2(c′) è un'osservazione che R6 non usa.

## 1. Fix numerati

**ENC2-1 (MAJOR, UNJUSTIFIED + LOCAL; ENC-P0(b)^cl, ENC-P0(b)^loc; R1, R2).** Severità alzata da MINOR dopo il KA (P1, P2): per ^loc c'è un controesempio esplicito all'enunciato come scritto (X := C^∞_c(U), W(g + w·f) := g su X ⊕ w·X, con w continua e liscia su nessun intervallo, V = t·w, c = 0: identità vera, ker W|_X = {0}, V non autonomo), perché la finitezza del nucleo è chiesta solo su C^∞_c(U) mentre la prova usa m·φ_k ∈ C_c(U). La prova applica W a funzioni m·φ_k con m := V(t, ·) − V(s, ·) − (c(t) − c(s)) soltanto continua. Con W: C^∞(J) → C^∞(J) e V ∈ C(I × J), già l'identità W(−∂² + V(t, ·))f = … non ha senso per f ∈ C^∞_c(J), perché V(t, ·)f non è C^∞. Le ipotesi vanno rese coerenti in uno dei due modi:
- (i) V(t, ·) ∈ C^∞(J) per ogni t; allora m ∈ C^∞ e m·φ_k ∈ C^∞_c(J), e la prova è corretta parola per parola;
- (ii) W: D_W → 𝒟′(J) lineare, con C(J)·C^∞_c(J) ⊂ D_W (per esempio D_W = C(J)), l'identità per f ∈ C^∞_c(J) intesa nel senso delle distribuzioni e dim ker W < ∞ **su tutto D_W** (per ^loc: D_W ⊃ C(U)·C^∞_c(U), codominio 𝒟′(U), nucleo finito su tutto D_W). È la forma che copre l'encoder di Volterra di ENC-1, che agisce su C(J) ed è iniettivo su C⁰.
Risposta a R1: che W mandi o no C^∞_c in C^∞_c non conta, perché la prova usa solo la linearità di W e il fatto che m·φ_k stia nel dominio di W. La lineare indipendenza delle m·φ_k è corretta (supporti disgiunti, e m·φ_k ≢ 0 perché m non si annulla su U). La frase "Equivalentemente: W agisce solo in x e intreccia i u_t = L_{V(t)}u …" va letta come intrecciamento degli operatori i∂_t − L_{V(t)} e i∂_t − L_0 − c(t) su **tutte** le funzioni regolari di (t, x), non solo sulle soluzioni: solo così è un'equivalenza. Sulle sole soluzioni è più debole, e l'equivalenza non è provata. La frase "copre l'encoder di Volterra di ENC-1" vale con la lettura (ii) per q continuo e con la lettura (i) per q ∈ C^∞(J°); va scritta la conclusione esplicita: se un W_q indipendente dal tempo soddisfa l'ipotesi, allora V(t, x) = q(x) + c(t) + costante (KA P5). Per "equivalentemente" la riparazione è: "in particolare, se W è sequenzialmente continuo su C^∞(J), W intreccia i∂_t − L_{V(t)} e i∂_t − L_0 − c(t) su C^∞(I × J)" (KA P4).

**ENC2-2 (MINOR; ENC-P0′ su nucleo denso; R3).** La prova è corretta: per v C¹ in ℋ con v(τ) ∈ D(H_0), il rapporto incrementale di U_0(−τ)v(τ) si spezza in U_0(−τ − h)(v(τ + h) − v(τ))/h, che converge a U_0(−τ)v′ (uniforme limitatezza e continuità forte), e in (U_0(−τ − h) − U_0(−τ))v(τ)/h, che converge a iU_0(−τ)H_0v(τ) perché v(τ) ∈ D(H_0). Non serve la continuità di v nella norma del grafo. Poi v(0) = W(0)U_V(0)u_0 = W(0)u_0, e si conclude per densità. Va aggiunto "0 ∈ I" (serve θ(0) = 0 e U_V(0) = I). La formula W_id(t) = U_0(t)W(0)U_V(t)^{−1} è corretta, e lo è anche la lettura "θ non è un invariante".

**ENC2-3 (MINOR; esempi di P0′ su 𝒮(ℝ); R4).**
- *Lente.* Verificata nella normalizzazione ½: u(t, x) = (cos t)^{−1/2}e^{−ix² tan t/2}v(tan t, x/cos t) risolve i u_t = −½u_xx + ½x²u (L1). La formula del pacchetto nella variabile y, v(tan t, y) = (cos t)^{1/2}e^{iy² sin t cos t/2}u(t, y cos t), è l'inversa esatta (L2), e W(t) è isometrica (L3). L'invarianza di 𝒮 sotto U_osc(t) per sviluppo di Hermite e la regolarità C^∞ in t a valori in 𝒮 sono corrette. Su I = (−π/2, π/2) vale θ(I) = ℝ.
- *Classe β(t)x + γ(t).* Verificata (BG1), e Avron–Herbst ne è il caso β = F (BG2).
- *Correzione.* Il testo dice che Avron–Herbst "è un'istanza di P0(a) su 𝒮". P0(a) richiede (H-P0), quindi V limitato, e lo stesso paragrafo dichiara Avron–Herbst fuori da (H-P0). Va scritto: "istanza di P0′ con θ = id e D_0 = 𝒮". La lente usa la normalizzazione ½, Avron–Herbst quella del progetto: va detto in una riga che i due esempi non usano la stessa normalizzazione.
- *Unicità in L².* L'argomento corretto è: se t ↦ U(t)u_0 sta nel dominio dell'hamiltoniano autoaggiunto H e risolve iu′ = Hu, allora d/dt[e^{itH}U(t)u_0] = 0. L'essenziale autoaggiuntezza su 𝒮 serve solo a dire che la chiusura dell'operatore differenziale è "l'" H del progetto. Resta CON-FONTE (Reed–Simon II §X; per −∂² + Fx anche Faris–Lavine), come dichiarato.

**ENC2-4 (MAJOR, INVALID + LOCAL; ENC-P0′-DIC, riga della tabella §6, sintesi in testa a §4; R5).** Il sistema dell'ansatz è corretto: con u = ρ^{−1/2}e^{iax²}v(T, x/ρ) e V = αx², il residuo si annulla esattamente quando T′ = 1/ρ², ρ′ = 4aρ e a′ + 4a² = −α (DIC1). La normalizzazione di a è quella del chirp e^{iax²}, con ρ(0) = 1 e T(0) = 0. La catena θ = id ⟹ ρ ≡ 1 ⟹ a ≡ 0 ⟹ α ≡ 0 è corretta (DIC2). Il verso **α ≡ 0 ⟹ a ≡ 0 è falso**: a′ + 4a² = 0 ha le soluzioni a = a_0/(1 + 4a_0t). Per V = 0 questo dà il rappresentante pseudo-conforme, con ρ = 1 + 4a_0t e θ(t) = t/(1 + 4a_0t) ≠ id (DIC3). È una simmetria classica dell'equazione libera. Quindi "θ ≠ id ⟺ α ≢ 0", letta sul singolo rappresentante, è falsa nel verso ⟸. La stessa formula compare anche nel mio `AUDIT_S8-ENC.md` (ENC-2) e in `KA_ENC_P0_adjudication.md`: l'imprecisione è nata nel mio testo, e il pacchetto l'ha recepita. *Forma corretta:* "**esiste un rappresentante puntuale più gauge con θ = id ⟺ α ≡ 0**; equivalentemente, ogni rappresentante puntuale più gauge ha θ ≠ id ⟺ α ≢ 0". La stessa correzione va fatta nella sintesi in testa a §4, nella riga della tabella §6 (riga 393: "θ = id per α ≡ 0" → "si può scegliere θ = id per α ≡ 0") e nella riga di LEDGER ENC-P0′-DIC. È MAJOR e non CRITICAL perché il claim era DA AUDITARE, non è registrato e non sta sul cammino critico, e perché la riparazione è un quantificatore.

**ENC2-5 (MINOR, UNJUSTIFIED + LOCAL; POLE-N^cl; R6).** Il passaggio "intreccia i∂_t ⟹ ∂_tW = 0" è corretto: data l'identità istantanea W(t)L_{V(t)} = (L_0 + c)W(t), si ha W(i∂_t − L_V)g − (i∂_t − L_0 − c)Wg = −i(∂_tW)g per ogni g. È verificato su un polo mobile (POLE1, POLE2): per V = 2/(x − z(t))² e W = −∂ − 1/(x − z(t)), l'intrecciamento istantaneo vale e il residuo parabolico è −i(∂_tW)g ≠ 0 se z′ ≠ 0, coerentemente con la tesi. Da ∂_t w_j = 0 sul complementare dei poli, però, segue w_j(t, ·) = w_j(s, ·) su U solo se l'intero rettangolo [s, t] × U evita i poli. Un intervallo libero da poli "a entrambi i tempi" non basta: con z(t) = t, t = 0, s = 2, U = (½, 3/2), U è libero ai due tempi ma il polo lo attraversa a t = 1 (POLE3). *Riparazione:* "fissato un rettangolo [s, t] × U contenuto nel complementare dei poli", oppure enunciare la tesi localmente (in un intorno rettangolare di ogni punto regolare) e concatenare. Va anche detto che P0(b)^cl si applica con dim ker W = n perché w_n è una costante non nulla (ENC-K1′(i)) e n ≥ 1, e che V è C^∞ fuori dai poli: lo si legge dai coefficienti dell'identità istantanea, e così ENC2-1 è soddisfatta nella forma (i).

**ENC2-6 (MAJOR, OVERSTATED + LOCAL; ENC-T2(c′); R7).** Severità alzata da MINOR dopo il KA (P7): relativamente a classi con vincolo di grado l'enunciato è falso (il 4-getto di e^{x²} certifica Ann = (τ) fra gli annullatori principali di grado totale ≤ 1), e nella classe degli annullatori principali la perturbazione usata fa uscire dalla classe (u = e^{x²}, u′ = u + e^{αt}x^M ha annullatore non principale). La frase "nessun getto certifica" va quindi circoscritta alla classe C^∞(Ω) senza vincoli; la versione nella classe principale è aperta. La prova è corretta. Il termine j = d di P_*(α, L_q)(x − x_1)^M ha ordine minimo M − 2d, con coefficiente p_d(α)(−1)^dM!/(M − 2d)! ≠ 0 per M ≥ 2d. I termini j < d partono dall'ordine M − 2j ≥ M − 2d + 2, e i contributi di q alzano l'ordine. È verificato con q = sin x + e^{x/3}, d = 3 (T2c′1). Il caso d = 0 (P_* = p_0(τ), T2c′2) e il caso limite M = 2d (T2c′3) sono corretti. Il getto j^N h si annulla in (t_1, x_1), comprese le derivate miste in t (T2c′4). Da aggiungere: (a) la definizione, cioè "un getto j^N u in (t_1, x_1) certifica Ann_q(u) = (P_*) se ogni u′ della classe dei dati con lo stesso N-getto ha Ann_q(u′) = (P_*)"; la prova costruisce u′ = u + h con P_* ∉ Ann_q(u′); (b) la regolarità: L_q^d h richiede q ∈ C^{2d−2}, garantita dall'ipotesi q ∈ C^∞ di ENC-C1; (c) h deve stare nella classe dei dati (DM3 su Ω, funzioni C^∞): vero. Nota di lettura: il fatto è elementare e non usa W, quindi non aggiunge nulla al cammino di R6; serve solo a correggere la "conseguenza" della rev. 1.

## 2. Controllo a campione del recepimento (fix ENC-1…ENC-15) e dei declassamenti a FALSO

| fix | controllato in | esito |
|---|---|---|
| ENC-1 (A9(b2)) | PP §7 righe 449–451; §0 riga 32; LR riga 38 | recepito: stima corretta, nota di correzione con il controesempio, ottimalità di 2/3 in (a) (PP riga 439). Il declassamento "la stima di (b2) della rev. 1 è FALSO" è corretto |
| ENC-2 (sintesi di ENC-P0) | PP §4 righe 206–210, §0 riga 28, §10.2 punto 4, §12 riga 599; LR riga 29 | recepito; il declassamento a FALSO è corretto. La dicotomia ereditata va corretta con ENC2-4 |
| ENC-3 | PP §4 righe 218, 272–294 | recepito (P0′ su nucleo denso, esempi su 𝒮); resta ENC2-3 |
| ENC-4 | PP §4 righe 248–260, 300–306 | recepito (P0(b)^cl, POLE-N^cl, argomento spettrale, operatori d'onda, Lettura ristretta); restano ENC2-1, ENC2-5 |
| ENC-5 | PP §5 righe 314–357 | recepito per intero: quadro con classi, N_V, ≈, famiglia fissata, (iii) per definizione, testimone (iv), punto (v), lettura di gauge. Il declassamento di ENC-N1 (F6) a FALSO con testimone (iv) è corretto. Il punto (v) è coerente con il conto dell'audit precedente |
| ENC-6 | PP §3 righe 174, 190–198 | recepito; (c′) auditato qui (ENC2-6) |
| ENC-7 | PP riga 148 | recepito (B = −2(d/dx)K(x, −x), con spiegazione) |
| ENC-8(d) | PP riga 80 | recepito (stima fine 1 + √2·a‖K‖_∞ su L²) |
| ENC-9 | PP righe 366, 380 | recepito (Z chiuso e numerabile) |
| ENC-10(a) | PP riga 488 | recepito (0 ∈ I) |
| ENC-11 | PP righe 512–517 | recepito; la costante (Cℓ𝐕)³e^{Cℓ𝐕}‖u^{(0)}‖/3 coincide con la mia 2(Cℓ𝐕)³e^{Cℓ𝐕}/6 |
| ENC-14 | PP riga 41 (ENC-D), righe 242, 262–268 | recepito ((E1) su 𝒴, P0(b)^loc, frase per G★″, domanda a S8-VAR) |
| ENC-15 | PP righe 216, 240, 244–246, 298, 308 | recepito |

Non ho controllato riga per riga ENC-12 ed ENC-13 (frasi di istanza): la tabella di `RECEPIMENTO.md` li dichiara applicati, e le istanze di §5 (righe 352–355) corrispondono al testo richiesto. Piccola svista non bloccante: in §10.2 punto 2 il rimando "CHECK_REQUEST D3" dovrebbe essere "D6".

## 3. Kill-argument su ENC-P0(b)^cl ed ENC-T2(c′)

Dettaglio in `KA_ENC2_adjudication.md`. Avvertenza: il prompt dell'attaccante conteneva alcune piste del mio controllo preliminare; sono contributi autonomi il controesempio a ^loc (P2), la lettura "su soluzioni" (P4) e il controesempio con vincolo di grado (P7(b)).

- **ENC-P0(b)^cl: WOUNDED → SURVIVES dopo ENC2-1.** P1 accolto come MAJOR (mal tipizzato con V solo continuo); P4 e P5 MINOR.
- **ENC-P0(b)^loc: KILLED come scritto → SURVIVES dopo ENC2-1.** P2 accolto (controesempio verificato a mano); P3 MINOR.
- **ENC-T2(c′): SURVIVES nella classe C^∞(Ω) → dopo ENC2-6.** P7 accolto come MAJOR (definizione, vincolo di grado falso, classe principale aperta); P8, P9 MINOR.

**Effetto sul cammino critico: nessuno.** R6 non usa né P0(b)^cl né T2(c′); ENC-1, ENC-U1, ENC-C1, ENC-T2(a)(b)(c) restano DIMOSTRATO.

## 4. Mappa delle verifiche (`enc2_check_rev2.py`)

| test | claim | esito |
|---|---|---|
| L1, L2, L3 | lente: equazione, inversa nella variabile y, isometria | OK |
| BG1, BG2 | classe β(t)x + γ(t); Avron–Herbst con θ = id | OK |
| DIC1, DIC2 | sistema dell'ansatz; θ = id ⟹ α = 0 | OK |
| DIC3 | V = 0 con rappresentante pseudo-conforme, θ ≠ id | OK (controesempio, ENC2-4) |
| POLE1, POLE2, POLE3 | polo mobile: intrecciamento istantaneo, residuo −i(∂_tW)g, rettangolo attraversato | OK (ENC2-5) |
| T2c′1–T2c′4 | ENC-T2(c′): ordine minimo con q non polinomiale, d = 0, M = 2d, getto nullo | OK |
