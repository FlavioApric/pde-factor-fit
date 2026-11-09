# S10-OPEN-C — PROOF_PACKAGE (27/10/2026)

Sessione S10-OPEN-C, Fase 10. Il compito è chiudere con esito onesto i problemi aperti di Fase 8 elencati in `PLAN.md`. Ogni esito è di uno di tre tipi:
- (a) prova;
- (b) controesempio;
- (c) ostruzione dimostrata, oppure problema lasciato APERTO con una riformulazione o una sottodomanda, scritto «APERTO — riformulato come …» o «APERTO — sottodomanda: …». L'etichetta «ridotto a» è riservata alle riduzioni con l'implicazione provata; dopo l'audit (rev2) nessuna delle «riduzioni» di questo pacchetto lo è, e l'etichetta è stata tolta ovunque.

**rev2 (27/10/2026).** Il pacchetto è stato rivisto dopo `work/CHECK-F10/AUDIT_S10-OPEN-C.md`. La sezione finale «Recepimento dell'audit (rev2)» **prevale** sulle sezioni 0–17 in caso di contrasto. Nel testo delle sezioni 1–17 ho cambiato solo le etichette di stato e aggiunto rimandi.

Tutto quello che segue è **prova scritta, DA AUDITARE**. Gli stati sono solo proposti, in `LEDGER_ROWS.md`; li registra il coordinatore. Dove la prova usa un risultato esterno non letto in questa sessione, lo indico come **CON-FONTE (non letta)**.

**Verifiche.** Comando: `D:\ProblemaBase\.venv\Scripts\python.exe -I work/S10-OPEN-C/sympy/s10openc_checks.py`. Lo script fa solo controlli: nessuna prova si appoggia sul calcolo. Esito: **34/34 OK** (dettaglio in `CHECK_REQUEST.md` §0). Per rev2 c'è un secondo script, `work/S10-OPEN-C/sympy/rev2_checks.py`, con lo stesso comando: **43/43 OK**.

**Convenzioni.**
- L_0 := i∂_t + ∂_x², come in S8-VAR. In S8-ENC invece L_q := −∂_x² + q e l'equazione è iu_t = L_qu.
- Il «DM2 con rumore» di GATE8 §5, ATTACK-8 O8 e VAR-Q19 si legge come **DM-δ** (NOTAZIONE v6, riga 116).
- Skill caricate: nessuna oltre al protocollo di sessione e al ciclo di vita dei claim, letti in Fase 8. Nessuno script `_vendor`, niente ML.

## 0. Tabella degli esiti

| # | problema | predizione (PLAN) | esito |
|---|---|---|---|
| 1 | VAR-P11(e) | (a) | **(a)** prova autonoma (§1) |
| 1′ | VAR-L2-cor | da CON-FONTE a DIMOSTRATO | **(a)** la dipendenza da Pazy cade; DIMOSTRATO se l'audit conferma §1 |
| 2 | VAR-Q18 | (b) | **(b)** controesempio di rango 2 (§2); per gli operatori di moltiplicazione: APERTO |
| 3 | VAR-Q10 | (a) | **(a)** esiste u con \|Z\| > 0 e int Z = ∅ (§3) |
| 4 | VAR-Q17 | (a) + (c) | **(a)** per V(x) e V_0(x) + v(t); **(c)** per V(t, x) (§4) |
| 5 | VAR-P12(d) | (b) + (c) | **(b)** nella classe quadratica; **(c)** per il caso generale (§5) |
| 6 | VAR-C3Q2-open | (a) parziale + (b) | **(a)** criterio di rango; **(b)** per VAR-Q12; **(a)** per i dati olonomi; resta aperto il caso non monico (§6) |
| 7 | Q-S8SYS-1 | dicotomia | **(a)** formale in ℚ[ξ, m][[t]]; **(b)** a t fisso (§7) |
| 8 | II-T2(b′) derogatorio | (a) + (b) | **(a)** criterio per reticoli; **(b)** la forma di Jordan non decide (§8) |
| 9 | Maxwell Q6 | (a) | **(a)** un campo identificante esiste su ogni Ω connesso (§9) |
| 10 | ENC-T2(c′), classe principale | (a) | **(a)** in forma forte (§10) |
| 11 | ENC-Q4 | (a) + (c) | **(a)** (S) non vuota per {q_0 + c} con DM-φ; **(c)** nella lettura DM3 (§11) |
| 12 | ENC-Q10 | (a) parziale + (c) | **(a)** encoder non locale esplicito di Darboux; **(c)** per V reale (§12) |
| 13 | DICT-ILIM-Hs | (a) | **(a)** (§13) |
| 14 | DICT-U3d-v | (a) | **(a)** velocità esplicita per ogni nucleo c.m.; ottimalità APERTA (§14) |
| 15 | DICT-Q3 | (c) + (b) | **(c)** riformulato come problema di divisione (APERTO); **(b)** il test puntuale e formale non basta in C^∞ (§15) |
| 16 | DICT-Q4 | (a) + (b) | **(a)** caratterizzazione (Amitsur, CON-FONTE); **(b)** atomi di media (§16) |
| 17 | Robustezza DM-δ / VAR-Q19 | (a) | **(a)** minimax Θ(ε^{1/3}) (§17) |

Le predizioni del PLAN sono confermate. Ci sono due scostamenti, entrambi nella direzione di un enunciato più forte:
- in §7(b) l'argomento si accorcia: basta il lemma dei polinomi esponenziali, senza la stima |G| ≥ …;
- in §14 la velocità vale in L¹(0, T) per ogni nucleo c.m., non solo su [δ, T].

---

## 1. VAR-P11(e): soluzioni classiche con B ∈ C¹ (prova autonoma)

**Quadro.**
- X è uno spazio di Banach e A_0 genera un semigruppo C_0, T(t), con ‖T(t)‖ ≤ M_0 per t ∈ [0, T].
- B ∈ C¹([0, T]; 𝓛(X)), e indico β_0 := sup‖B‖ e β_1 := sup‖B′‖.
- U(t, s) è il propagatore di Dyson–Phillips (VAR-P11(a)–(d)), dato dall'equazione mite u(t) = T(t − s)x + ∫_s^tT(t − r)B(r)u(r)dr.

**Enunciato.** Se x ∈ D(A_0), allora u = U(·, s)x appartiene a C¹([s, T]; X) ∩ C([s, T]; D(A_0)) e vale u′(t) = (A_0 + B(t))u(t). Si tratta quindi di una soluzione classica, ed è l'unica: ogni soluzione classica è mite, e la soluzione mite è unica per Gronwall.

**Lemma C (convoluzione C¹).** Siano f ∈ C¹([s, T]; X) e F(t) := ∫_s^tT(t − r)f(r)dr. Allora:
- F ∈ C¹, con F′(t) = T(t − s)f(s) + ∫_s^tT(t − r)f′(r)dr;
- F(t) ∈ D(A_0), con A_0F(t) = F′(t) − f(t).

*Prova.*
- *Derivata.* Si scrive F(t) = ∫_0^{t−s}T(σ)f(t − σ)dσ. Il rapporto incrementale vale
  h^{−1}[F(t + h) − F(t)] = h^{−1}∫_{t−s}^{t−s+h}T(σ)f(t + h − σ)dσ + ∫_0^{t−s}T(σ)h^{−1}[f(t + h − σ) − f(t − σ)]dσ.
  Il primo termine tende a T(t − s)f(s) per continuità forte e uniforme. Il secondo tende a ∫T(σ)f′(t − σ)dσ per convergenza dominata, perché f′ è uniformemente continua. La continuità di F′ si vede sulla formula.
- *Dominio.* Per h > 0 si ha h^{−1}(T(h) − I)F(t) = h^{−1}[F(t + h) − F(t)] − h^{−1}∫_t^{t+h}T(t + h − r)f(r)dr. Il secondo membro tende a F′(t) − f(t). ∎

**Prova dell'enunciato.**
1. *La candidata derivata.* Sia y_0 := A_0x + B(s)x. Sia v ∈ C([s, T]; X) l'unica soluzione dell'equazione di Volterra lineare
   v(t) = T(t − s)y_0 + ∫_s^tT(t − r)[B′(r)u(r) + B(r)v(r)]dr,
   dove u è la soluzione mite, già nota. La soluzione esiste ed è unica per iterazione di Picard, perché il nucleo è limitato da M_0β_0.
2. *La candidata soluzione.* Sia w(t) := x + ∫_s^tv. Si pone f := Bw, che è C¹ con f′ = B′w + Bv. Sia poi z(t) := T(t − s)x + ∫_s^tT(t − r)f(r)dr.
3. *Derivata di z.* Per il Lemma C e x ∈ D(A_0):
   z′(t) = T(t − s)A_0x + T(t − s)B(s)x + ∫_s^tT(t − r)[B′w + Bv](r)dr.
   Quindi v(t) − z′(t) = ∫_s^tT(t − r)B′(r)[u(r) − w(r)]dr.
4. *Gronwall.* Sia e := u − w. Si ha:
   - u − z = ∫_s^tT(t − r)B(r)e(r)dr;
   - (w − z)′ = v − z′ = ∫_s^tT(t − r)B′(r)e(r)dr, con (w − z)(s) = 0.

   Quindi ‖e(t)‖ ≤ M_0β_0∫_s^t‖e‖ + (t − s)M_0β_1∫_s^t‖e‖ ≤ C∫_s^t‖e‖, da cui e ≡ 0. Allora u = w ∈ C¹ con u′ = v, e anche u = z.
5. *Classicità.* u(t) = T(t − s)x + F(t) con F come nel Lemma C (f = Bu). T(t − s)x ∈ D(A_0) e F(t) ∈ D(A_0), quindi u(t) ∈ D(A_0) e
   A_0u = T(t − s)A_0x + F′ − Bu = z′ − Bu = u′ − Bu.

   Ne segue u′ = A_0u + Bu, e A_0u = u′ − Bu è continua. ∎

**Conseguenza per VAR-L2-cor.** La prova di S8-VAR usa P11(e) per portare la soluzione con dato in D(H_0) nella classe (SF). La cita con B = −iV(t), cioè la moltiplicazione, e con V ∈ C¹([0, T]; L^∞(J; ℝ)), quindi B ∈ C¹([0, T]; 𝓛(L²)). Le ipotesi di §1 sono soddisfatte e la dipendenza CON-FONTE da Pazy cap. 5 cade. **Proposta:** VAR-P11(e) e VAR-L2-cor DIMOSTRATO, se l'audit conferma §1. Il resto della catena di L2-cor era già auditato da S-CHECK-F8 (AUDIT_S8-VAR_L2cor).

## 2. VAR-Q18: B solo continuo in norma (controesempio)

**Enunciato.** Esistono X di Hilbert, A_0 antiaggiunto e B ∈ C([0, T]; 𝓛(X)) antiaggiunto in ogni t con questa proprietà: per un x_* ∈ D(A_0) e per ogni t ∈ (0, T] con sin(nt) ≠ 0, dove n := ‖x‖ è il numero della costruzione (rev2, C-2), si ha U(t, 0)x_* ∉ D(A_0). In particolare VAR-P11(e) è falso senza l'ipotesi C¹.

**Costruzione.**
- ℋ è uno spazio di Hilbert, A è antiaggiunto non limitato e genera il gruppo unitario T(t). Si fissa x ∈ ℋ ∖ D(A), x ≠ 0, e si pone n := ‖x‖.
- X := ℋ ⊕ ℂ e A_0 := A ⊕ 0.
- f(t) := T(t)x e B(t)(y, c) := (c f(t), −⟨y, f(t)⟩), con il prodotto scalare lineare nel primo argomento.

**Verifiche.**
- *B è antiaggiunto.* ⟨B(y, c), (y′, c′)⟩ = c⟨f, y′⟩ − ⟨y, f⟩c̄′ = −⟨(y, c), B(y′, c′)⟩.
- *B è continuo in norma.* ‖B(t) − B(t′)‖ ≤ 2‖T(t)x − T(t′)x‖ → 0.
- *B non è C¹.* Se lo fosse, t ↦ B(t)(0, 1) = (T(t)x, 0) sarebbe derivabile, quindi x ∈ D(A).
- *Il dato.* x_* := (0, 1) ∈ D(A_0).

**Soluzione esplicita.** Sia C(t) := sin(nt)/n. Si pone y(t) := C(t)T(t)x e c(t) := C′(t) = cos(nt).
- *Prima componente.* Nell'equazione mite compare ∫_0^tT(t − r)c(r)f(r)dr = (∫_0^tc)T(t)x = C(t)T(t)x = y(t).
- *Seconda componente.* c(t) = 1 − ∫_0^t⟨y(r), f(r)⟩dr = 1 − n²∫_0^tC, perché ⟨T(r)x, T(r)x⟩ = n². L'identità cos(nt) = 1 − n²∫_0^tsin(nr)/n dr vale (SymPy T7: C″ = −n²C, C(0) = 0, C′(0) = 1).

Per unicità della soluzione mite, U(t, 0)x_* = (C(t)T(t)x, cos nt). Per 0 < t < π/n si ha C(t) ≠ 0, e T(t)x ∉ D(A) perché D(A) è invariante per T(±t). ∎

**Portata.**
- Risponde negativamente a VAR-Q18 nella forma astratta, e quindi anche a ENC Q13: (H-P0) non è automatica per perturbazioni limitate continue in norma.
- *Resta APERTO* il sottocaso fisico B(t) = −iV(t)· con V ∈ C([0, T]; L^∞(J; ℝ)), cioè operatori di moltiplicazione. Il controesempio usa un B di rango 2 che non è una moltiplicazione. **APERTO** (sottocaso residuo, nessuna riduzione): P11(e) per moltiplicazioni continue in norma ma non C¹.

## 3. VAR-Q10: zeri di misura positiva con interno vuoto (esistenza)

**Enunciato.** Siano I := (0, 1) e Ω := I × ℝ. Esiste u ∈ C^∞(Ω̄) con queste proprietà:
- i∂_tu + ∂_x²u = 0, cioè V = 0;
- int Z(u) = ∅ e |Z(u)| > 0;
- u(t, ·) è intera in x per ogni t.

Di conseguenza VAR-T1(c) **non** si semplifica: nella classe C, V è identificato (int Z = ∅); nella classe L^∞ no, perché V = 0 e V′ = 1_{Z(u)} sono entrambe leggi (V′u ≡ 0).

**Costruzione.**
1. *Insieme di Cantor.* K ⊂ [0, 1] è un Cantor grasso: chiuso, mai denso, con |K| > 0. I suoi gap in (0, 1) sono gli intervalli aperti disgiunti I_j = (α_j, α_j + ℓ_j), con Σℓ_j ≤ 1.
2. *Funzione bump.* Siano g_0(s) := exp(−s^{−2}) per s > 0 e g_0 := 0 altrimenti, e B(s) := g_0(s)g_0(1 − s).
   - Da S8-VAR §7.1, |g_0^{(k)}(s)| ≤ k!(θs)^{−k}e^{−1/(2s²)} con θ = 1/10.
   - sup_s s^{−k}e^{−1/(2s²)} = k^{k/2}e^{−k/2} ≤ C^k(k!)^{1/2}, quindi |g_0^{(k)}| ≤ C_1^k(k!)^{3/2}.
   - Per Leibniz, |B^{(k)}| ≤ (2C_1)^k(k!)^{3/2}.
3. *La funzione g.* g := Σ_jg_j, con g_j(t) := e^{−ℓ_j^{−4}}B((t − α_j)/ℓ_j).
   - |g_j^{(k)}| ≤ e^{−ℓ_j^{−4}/2}·(2C_1)^k(k!)^{3/2}·sup_{ℓ∈(0,1]}ℓ^{−k}e^{−ℓ^{−4}/2}.
   - L'ultimo sup vale (k/(2e))^{k/4} ≤ C_2^k(k!)^{1/4} (SymPy T2 per la forma (k/4e)^{k/4} con e^{−ℓ^{−4}}).
   - e^{−ℓ^{−4}/2} ≤ ℓ su (0, 1], quindi Σ_je^{−ℓ_j^{−4}/2} ≤ 1.
   - Ne segue che tutte le serie derivate convergono uniformemente, g ∈ C^∞(ℝ) e |g^{(k)}| ≤ A^k(k!)^{7/4}.
   - Su K ogni g_j^{(k)} si annulla (B è piatta in 0 e in 1), quindi g^{(k)} = 0 su K. Inoltre g > 0 sui gap.
4. *Serie di Tychonoff.* u(t, x) := Σ_k(−i)^kg^{(k)}(t)x^{2k}/(2k)!.
   - Dato che (2k)! ≥ (k!)², il termine k è ≤ A^k|x|^{2k}/(k!)^{1/4}: la serie converge per ogni x.
   - Lo stesso vale per le serie derivate in t (g^{(k+j)} ≤ A^{k+j}((k+j)!)^{7/4} e (k + j)! ≤ 2^{k+j}k!j!) e in x.
   - Quindi u ∈ C^∞, intera in x, e L_0u = 0 termine a termine. Il residuo telescopico è verificato in SymPy T1.

**Zeri.**
- Per t ∈ K ∩ I tutti i g^{(k)}(t) sono nulli, quindi u(t, ·) ≡ 0. Ne segue Z(u) ⊃ (K ∩ I) × ℝ, che ha misura positiva (localmente |K| > 0).
- Sia W ⊂ Z(u) un aperto non vuoto. K è mai denso, quindi W contiene un punto (t, x) con t in un gap. Allora u(t, ·) è intera, si annulla su un intervallo, e quindi è ≡ 0. Ma u(t, 0) = g(t) > 0: contraddizione. Dunque int Z(u) = ∅. ∎

**Commento.** La domanda di VAR-Q10 chiedeva u ∈ C^{1,2} con V ∈ L^∞_loc. Qui V = 0 e u è C^∞, quindi la risposta è sì nella forma più forte. Lo strumento Carleman suggerito non serve, perché l'esempio è esplicito. La predizione «stessa risposta del calore» non è stata confrontata con le fonti sul calore.

## 4. VAR-Q17: osservabilità laterale per soluzioni miti

**Enunciato (a).** Sia V = V_0(x) + v(t), con V_0 ∈ L^∞(J; ℝ) e v ∈ L^∞(0, T; ℝ), nel quadro di VAR-L2-cor (stesso H_0 su J, stesse condizioni al bordo). Sia ψ_0 ∈ L²(J). Se la soluzione mite ψ è nulla q.o. su (0, T) × ω, con ω ⊂ J aperto, allora ψ_0 = 0.

*Prova.*
1. *Gauge.* ψ = e^{−i∫_0^tv}ψ̃, dove ψ̃ risolve con V_0. I due insiemi di zeri coincidono, quindi basta V = V_0(x).
2. *Mollificazione nel tempo.* H := H_0 + V_0 è autoaggiunto su D(H_0), e ψ(t) = e^{−itH}ψ_0. Siano η > 0 e φ ∈ C_c^∞(−η, η). Si pone
   ψ_φ(t) := ∫φ(s)ψ(t + s)ds = e^{−itH}φ̌(H)ψ_0, con φ̌(H) := ∫φ(s)e^{−isH}ds.
3. *Regolarità del dato.* φ̌(λ) = ∫φ(s)e^{−isλ}ds decresce più velocemente di ogni potenza, quindi φ̌(H)ψ_0 ∈ D(H^∞) ⊂ D(H_0).
4. *Applicazione di L2-cor.* ψ_φ è nulla su (η, T − η) × ω. V_0 è indipendente da t, quindi C¹ in t. VAR-L2-cor sull'intervallo (η, T − η), con il tempo traslato, dà φ̌(H)ψ_0 = 0.
5. *Limite.* Con φ_n un'approssimazione dell'identità, φ̌_n(H)ψ_0 → ψ_0 fortemente, per continuità forte del gruppo. Quindi ψ_0 = 0. ∎

**Lemma (regolarità delle medie, V(t, x) qualsiasi continuo in norma).** Per h ∈ C_c^1((0, T)) e ψ mite, ∫h(s)U(s, 0)ψ_0ds ∈ D(H_0).

*Prova.* Si scrive ψ(s) = T(s)ψ_0 + ∫_0^sT(s − r)B(r)ψ(r)dr e si usa A_0∫T(s)k(s)ds = −∫T(s)k′(s)ds per k ∈ C_c^1. Il termine di Duhamel si tratta con Fubini e lo stesso calcolo in s. ∎

Il lemma basta per (a) senza il calcolo funzionale, ma da solo non chiude il caso dipendente dal tempo.

**(c) Caso V(t, x): ostruzione.** Per V dipendente da t, ψ_φ risolve
i∂_tψ_φ = (H_0 + V(t))ψ_φ + R_φ, con R_φ(t) := ∫φ(s)[V(t + s) − V(t)]ψ(t + s)ds.
- R_φ è nulla su ω, perché lì ψ = 0. Il termine sorgente vive quindi fuori dall'insieme di osservazione.
- VAR-L2 è una continuazione unica **omogenea**: con una sorgente supportata fuori da ω non si conclude. L'idea che ogni soluzione del problema con sorgente si possa modificare lontano da ω è solo un'euristica, non un'ostruzione provata (rev2, C-6).

**APERTO — riformulato come** (è la domanda stessa, riscritta; nessuna riduzione): continuazione laterale per i∂_tψ + ∂_x²ψ = Vψ con V ∈ C([0, T]; L^∞), oppure V ∈ L^∞((0, T) × J), in una classe a regolarità negativa in t (per esempio ψ ∈ C([0, T]; L²)). Serve una stima di Carleman in H^{−1}_t, oppure una mollificazione che commuti con V(t).

## 5. VAR-P12(d): logaritmo differenziale per V(t, x)

**Enunciato (b), classe quadratica.** Siano τ_1 := π/(4ω_1) e τ_2 := π/(4ω_1), con T = τ_1 + τ_2. Sia H(t) := −∂_x² + ω(t)²x² su L²(ℝ), con ω(t) = ω_1 su [0, τ_1) e ω(t) = ω_2 := 5ω_1 su [τ_1, T), estesa per periodicità. Allora non esiste alcun operatore autoaggiunto K′ della forma di Weyl quadratica affine,
K′ = ½(a p² + b(xp + px) + c x²) + d x + e p + f, con a, …, f ∈ ℝ e p := −i∂_x,
tale che e^{−iTK′} = U(T, 0) a meno di una fase. Lo stesso vale per una regolarizzazione C^∞ di ω abbastanza vicina in L¹.

*Prova.*
1. *Monodromia.* Per Hamiltoniane quadratiche, U(t, 0)^*(x, p)U(t, 0) = M(t)(x, p) con M ∈ SL₂(ℝ), soluzione di ẋ = 2p, ṗ = −2ω²x (Heisenberg; SymPy T8c).
2. *Segmento costante.* Su un tratto a ω costante di durata τ il fattore è [[cos θ, sin θ/ω], [−ω sin θ, cos θ]], con θ = 2ωτ. I due angoli valgono θ_1 = π/2 e θ_2 = 2·5ω_1·π/(4ω_1) = 5π/2.
3. *Traccia.* tr M = −(ω_1/ω_2 + ω_2/ω_1) = −26/5 < −2 (SymPy T8a, T8b).
4. *Se esistesse K′.* Con K′ quadratico affine, e^{iTK′}(x, p)e^{−iTK′} = e^{TΞ}(x, p) + v, con Ξ ∈ sl₂(ℝ) e v ∈ ℝ². L'uguaglianza dei propagatori a meno di fase dà v = 0 ed e^{TΞ} = M.
5. *Contraddizione.* exp(sl₂(ℝ)) ⊂ {tr > −2} ∪ {−I}:
   - Ξ ellittico dà tr = 2cos;
   - Ξ parabolico dà tr = 2;
   - Ξ iperbolico dà tr = 2cosh.

   Quindi M non è un esponenziale. La traccia è continua in ω ∈ L¹ (dipendenza continua della EDO lineare), e la stessa conclusione vale per ω regolarizzata. ∎

**Osservazioni.**
- Al periodo 2T si ha tr M² = (26/5)² − 2 > 2 e gli autovalori sono positivi, quindi M² = e^{Ξ} con Ξ iperbolico. Il log quadratico esiste per U(2T, 0), a meno della fase e del segno metaplettico.
- Il potenziale ω²x² non è limitato: l'esempio esce dalla classe V ∈ L^∞ di §4.2–4.4 di S8-VAR, ma sta nella classe quadratica che S8-VAR §4.3 già usa.
- **(c) Caso generale.** Per V(t, x) limitato, oppure per logaritmi differenziali non quadratici, il problema resta **APERTO**. **Sottodomanda** (OC-3, senza implicazione verso (d)): un operatore metaplettico la cui monodromia ha traccia < −2 può essere e^{−iTK′} con K′ differenziale non quadratico? Il risultato (b) dice solo che la classe quadratica non basta. Non c'è un'ostruzione per ordini ≥ 3.

## 6. VAR-C3Q2-open: criterio intrinseco (m ≥ 2) e VAR-Q12

**Notazione.**
- A_2 = ℂ[t, x]⟨∂_t, ∂_x⟩ e B := ℂ[t, x]⟨∂_x⟩. B è un dominio di Ore a sinistra (sottoalgebra noetheriana senza divisori dello zero di A_2), con corpo dei quozienti D_B.
- Il rango di un B-modulo sinistro M è rank_BM := dim_{D_B}(D_B ⊗_B M), additivo sulle successioni esatte. D_B è piatto su B, per la localizzazione di Ore.
- L = ∂_t^m + Σ_{j<m}b_j∂_t^j, con b_j ∈ B, è monico.

**Teorema (a) (prova scritta).** Sia Lu = 0. Allora Ann_{A_2}(u) = A_2L ⟺ rank_B(A_2u) = m.

*Prova.*
1. Per la divisione di S8-VAR §5(a), A_2 = A_2L ⊕ ⊕_{j<m}B∂_t^j.
2. La mappa π: B^m → A_2u, (β_j) ↦ Σβ_j∂_t^ju, è suriettiva, perché A_2Lu = 0.
3. Un Q ∈ Ann(u) si scrive Q = Q′L + Σβ_j∂_t^j con Σβ_j∂_t^ju = 0; quindi Q ∈ A_2L ⟺ β = 0. Ne segue Ann(u) = A_2L ⟺ ker π = 0.
4. Se ker π ≠ 0, è un sottomodulo non nullo di B^m, che è senza torsione, quindi ha rango ≥ 1, e rank A_2u = m − rank ker π < m.
5. Se ker π = 0, rank A_2u = m. ∎

**Lettura.** Il criterio è intrinseco: rank_B(A_2u) non dipende da L. Corollario: se u è annullata da due operatori monici di ordini diversi, al più quello di ordine rank_B(A_2u) può generare Ann(u).

**(b) VAR-Q12: dati non D-finiti che non identificano.** Siano f(y) := exp(e^y) e u(t, x) := f(x + t).
- *u non è D-finita.* Se lo fosse, A_2u sarebbe olonomo, e la restrizione a t = 0, cioè f, sarebbe D-finita in x. Ma le soluzioni intere di un'EDO lineare a coefficienti polinomiali hanno ordine di crescita finito (CON-FONTE, teoria di Wiman–Valiron, non letta), mentre exp(e^y) ha ordine infinito. **[rev2, C-8: sostituito da una prova elementare con i polinomi di Touchard; Wiman–Valiron esce dalle dipendenze.]**
- *u non identifica □.* Si ha (∂_t − ∂_x)u = 0 (SymPy T10), quindi Ann(u) ∋ ∂_t − ∂_x ∉ A_2□, con □ = ∂_t² − ∂_x² (per l'ordine in ∂_t). Dunque Ann(u) ⊋ A_2□.

Il criterio «non D-finita ⇒ identifica», vero per m = 1 (S8-VAR §5(c)), non si estende a m ≥ 2. La risposta alla seconda domanda di VAR-Q12 è sì.

**(a′) Dati olonomi.** Se A_2u è olonomo, nessun L ≠ 0 è identificato, cioè Ann(u) ≠ A_2L. Infatti A_2/A_2L ha dimensione di Gelfand–Kirillov 3, mentre un modulo olonomo di A_2 ha dimensione 2. Si usa la disuguaglianza di Bernstein (CON-FONTE classica: Björk, *Rings of Differential Operators*, cap. 1; non riletta qui).

**Resta APERTO** VAR-Q13, il caso non monico, senza riduzione. Senza monicità manca la decomposizione del passo 1, quindi l'argomento di rango non si trasporta; l'equivalenza enunciata nella prima versione («Ann(u) ⊂ A_2 ∩ D_BL ⟺ ker π = 0») non è provata ed è ritirata (rev2, C-9).

## 7. Q-S8SYS-1: prodotto di Euler di Dirac 1+1 con tempi polinomiali

**Quadro.** A(ξ) = X + mY, con X = iξσ_z e Y = −iσ_x. Si ha ω := √(ξ² + m²), A² = −ω²I ed e^{tA} = cos(ωt)I + sin(ωt)A/ω. S8-SYS (SYS-E3) dà
e^{tA} = e^{iaσ_z}e^{ibσ_x}e^{iaσ_z},
con b = −arcsin(m sin(ωt)/ω) e 2a = arctan(ξ tan(ωt)/ω) per ωt < π/2. In termini di flussi, e^{tA} = e^{g_1X}e^{g_2mY}e^{g_1X} con g_1 = a/ξ e g_2 = −b/m.

**(a) Forma formale.** g_1, g_2 ∈ ℚ[ξ, m][[t]], e l'identità di prodotto vale in Mat_2(ℚ[ξ, m][[t]]).

*Prova.* sin(ωt)/ω e tan(ωt)/ω sono serie in t a coefficienti polinomiali in ω² = ξ² + m². arctan(ξ·) e arcsin(m·) sono dispari, quindi a/ξ e b/m sono serie a coefficienti polinomiali. L'identità vale come identità analitica per |t| piccolo e reale, e quindi tra serie formali. SymPy T4a dà la polinomialità fino a t^9; T4b dà l'identità fino a t^6; T3 la verifica numerica.

Ogni troncamento è un prodotto di flussi di operatori differenziali, perché ξ ↔ −i∂_x.

**(b) A t fisso non esiste una parola finita con tempi polinomiali.** Siano t ≠ 0 e m ≠ 0 reali. Non esistono k ∈ ℕ e polinomi reali p_1, q_1, …, p_k, q_k ∈ ℝ[ξ] tali che, per ogni ξ ∈ ℝ,
W(ξ) := Π_{j=1}^{k}e^{p_j(ξ)X}e^{q_j(ξ)mY} = e^{tA(ξ)}.

*Lemma E.* Siano R_1, …, R_n ∈ ℝ[ξ] con R_i − R_j non costante per i ≠ j, e d_j ∈ ℂ. Se S(ξ) := Σd_je^{iR_j(ξ)} → 0 per ξ → +∞, allora d_j = 0 per ogni j.

*Prova del lemma.*
- (1/X)∫_X^{2X}|S|² → 0, e lo sviluppo dà Σ|d_j|² + Σ_{i≠j}d_id̄_j(1/X)∫_X^{2X}e^{i(R_i−R_j)}.
- Per Q ∈ ℝ[ξ] non costante, Q′ è definitivamente monotona e diversa da zero. Integrando per parti, |∫_X^{2X}e^{iQ}| ≤ 1/|Q′(X)| + 1/|Q′(2X)| + |1/Q′(2X) − 1/Q′(X)| = O(1), usando la monotonia di 1/Q′ (corretto in rev2, C-10).
- Quindi i termini misti tendono a 0 e Σ|d_j|² = 0. ∎

*Prova di (b).*
1. e^{pX} = diag(e^{ipξ}, e^{−ipξ}), mentre e^{qmY} = cos(qm)I − i sin(qm)σ_x è combinazione di e^{±iqm}.
2. Sviluppando il prodotto, W_{11}(ξ) = Σ_jc_je^{iP_j(ξ)} con P_j ∈ ℝ[ξ]. Si raggruppano i P_j uguali a meno di costanti, assorbendo le costanti nei coefficienti.
3. *Asintotica del bersaglio.* Per ξ → +∞, ω = ξ + m²/(2ξ) + O(ξ^{−3}) e
   (e^{tA})_{11} = cos ωt + iξ sin(ωt)/ω = e^{iξt} + i(m²t/(2ξ))e^{iξt} + O(ξ^{−2}).
4. *Applicazione del lemma.* Se W = e^{tA}, la funzione G := W_{11} − e^{iξt} è della forma del Lemma E e tende a 0. Quindi tutti i suoi coefficienti sono nulli, G ≡ 0, e W_{11} = e^{iξt} per ogni ξ.
5. *Contraddizione.* G = i(m²t/(2ξ))e^{iξt} + O(ξ^{−2}) ≠ 0 per ξ grande. ∎

**Lettura.**
- La decomposizione ZXZ è un prodotto di flussi **locali** solo come serie formale in t, cioè nel limite di tempo piccolo ordine per ordine.
- A t fisso nessun prodotto finito di flussi a tempi polinomiali, cioè di operatori differenziali, la realizza. I fattori sono moltiplicatori di Fourier non locali, coerentemente con la nota di S8-DICT §1.8.
- *Fuori portata:* tempi polinomiali complessi. Il Lemma E non copre e^{iP} con P complesso; servirebbe un ordinamento per crescita.

## 8. II-T2(b′) caso derogatorio

**Quadro.**
- A(ξ) ∈ Mat_n(ℂ(ξ)) e il polinomio caratteristico si fattorizza come Q·B, con Q e B coprimi su ℂ(ξ).
- E(ξ) := ker Q(A(ξ)) e F(ξ) := ker B(A(ξ)) sono complementari per ξ ≠ ξ_0 vicino a ξ_0.
- Il proiettore spettrale su E lungo F è P(ξ) = B(A)·B(λ)^{−1} nel caso Q = τ − λ.

**(a) Criterio (prova scritta).** P ha un polo in ξ_0 ⟺ E_0 ∩ F_0 ≠ 0, dove E_0 := lim E(ξ) ed F_0 := lim F(ξ) nella grassmanniana. Equivalentemente, det[e(ξ_0) f(ξ_0)] = 0, con e, f basi locali **saturate**.

*Prova.*
1. *Basi saturate.* Le colonne di basi razionali di E e di F si possono dividere per potenze di (ξ − ξ_0) (forma di Smith sul DVR ℂ[ξ]_{(ξ−ξ_0)}). Si ottengono matrici e(ξ), f(ξ) analitiche in ξ_0, con e(ξ_0) ed f(ξ_0) di rango pieno. Quindi i limiti esistono: E_0 = im e(ξ_0) ed F_0 = im f(ξ_0).
2. Si ha P = [e 0][e f]^{−1}.
3. Se det[e f](ξ_0) ≠ 0, P è analitico in ξ_0.
4. Se il determinante è nullo, sia v ≠ 0 in E_0 ∩ F_0. Se P fosse limitato vicino a ξ_0, un limite P_0 lungo una successione soddisferebbe P_0e(ξ_0) = e(ξ_0) e P_0f(ξ_0) = 0, quindi P_0v = v e P_0v = 0: contraddizione. ∎

**(b) La forma di Jordan di A(ξ_0) non decide (controesempio).** Siano
A_1 := [[ξ, 0, 0], [0, −ξ, 1], [0, 0, −2ξ]] e A_2 := [[ξ, 1, 0], [0, −ξ, 0], [0, 0, −2ξ]].
- Q = τ − ξ e B = (τ + ξ)(τ + 2ξ) per entrambe.
- In ξ_0 = 0 entrambe hanno forma di Jordan J_2 ⊕ J_1.
- Per A_1, P = diag(1, 0, 0), senza polo: E = ⟨e_1⟩ ed F = ⟨e_2, e_3⟩ per ogni ξ.
- Per A_2, P ha l'elemento (1, 2) uguale a 1/(2ξ): F(ξ) ∋ (1, −2ξ, 0), quindi F_0 ∋ e_1 ∈ E_0.

Verifiche: SymPy T6a–T6e (anche idempotenza e commutazione).

La congettura Q-S8SYS-4, letta come «il polo è determinato da A(ξ_0) e dalla fattorizzazione», è **FALSA**. Il polo dipende dai limiti E_0 ed F_0, cioè dal getto di primo ordine di A in ξ_0. Con diag(ξ, −ξ) (S8-SYS §8) si ha anche un attraversamento senza polo.

## 9. Maxwell (Q6, RT-SYS): esiste un campo identificante

**Quadro.**
- R := ℂ[τ, ξ_1, ξ_2, ξ_3], con n = 4.
- P ∈ R^{8×6} ha le righe τE − ξ×B (3 righe), τB + ξ×E (3), ξ·E e ξ·B.
- M_P := R^{1×6}/R^{1×8}P. SYS-EX (S8-SYS): su Ω connesso esiste una u identificante ⟺ dim soc_𝔪(M_P) ≤ 1 per ogni ideale massimale 𝔪.

**Teorema.** soc_𝔪(M_P) = 0 per ogni 𝔪. Quindi, per SYS-EX, un campo (E, B) identificante esiste su ogni Ω connesso.

*Prova.*
1. *Sizigie.* S_1 := (ξ, 0, −τ, 0) e S_2 := (0, ξ, 0, −τ), scritte a blocchi (3, 3, 1, 1), soddisfano S_iP = 0: per esempio ξ·(τE − ξ×B) − τ ξ·E = 0 (SymPy T5a).
2. *Rango.* Un minore 6×6 è non nullo (SymPy T5b), quindi rank P = 6 e il nucleo sinistro su Frac(R) ha dimensione 2, generato da S_1 e S_2.
3. *Il nucleo su R è libero.* Se sP = 0, allora s = f_1S_1 + f_2S_2 con f_i ∈ Frac(R). S_1 ed S_2 hanno supporti disgiunti, quindi f_1ξ_i ∈ R e f_1τ ∈ R. Scrivendo f_1 = a/b ridotta, b divide ξ_1, ξ_2, ξ_3 e τ, quindi b è un'unità e f_1 ∈ R. Lo stesso per f_2. Il nucleo è dunque libero di rango 2.
4. *Risoluzione.* La successione 0 → R² → R^8 → R^6 → M_P → 0 è esatta, quindi pd M_P ≤ 2.
5. *Zoccolo.* Siano k = R/𝔪 e N := R^{1×8}P. R_𝔪 è regolare di dimensione 4, quindi Ext^i(k, R) = 0 per i < 4.
   - Da 0 → N → R^6 → M_P → 0 segue Hom(k, M_P) ↪ Ext¹(k, N).
   - Da 0 → R² → R^8 → N → 0 segue Ext¹(k, R^8) → Ext¹(k, N) → Ext²(k, R²), con i due estremi nulli.

   Quindi Hom(k, M_P) = 0. ∎

**Dipendenze.** SYS-EX nella forma di S8-SYS, che usa l'iniettività di C^∞(ℝ^n) come modulo (CON-FONTE già registrata). Il teorema vale per ogni sistema con pd M_P ≤ n − 2.

## 10. ENC-T2(c′) nella classe degli annullatori principali

**Notazione** (S8-ENC): S = ℂ[τ, σ] e Ann_q(u) := {P ∈ S : P(∂_t, L_q)u = 0}, con q noto e Ω = I × J°.

**Enunciato.** Sia u ∈ C^∞(Ω) con Ann_q(u) = (P_*), P_* ≠ 0. Per ogni punto (t_1, x_1) ∈ Ω e ogni intorno della forma I × (x_1 − η, x_1 + η), con η tale che J° ∖ [x_1 − η, x_1 + η] abbia interno non vuoto (rev2, C-14), esiste u′ ∈ C^∞(Ω) con queste proprietà:
- u′ = u su I × (x_1 − η, x_1 + η), quindi u′ ha lo stesso getto di ogni ordine in (t_1, x_1);
- Ann_q(u′) = (P_*·(τ − α)), che è principale e diverso da (P_*).

Ne segue che nessun getto finito certifica Ann_q(u) = (P_*), nemmeno nella classe degli annullatori principali. Neanche i dati su una striscia intorno a x_1 lo certificano.

*Prova.*
1. *Scelta di α.* P_* ≠ 0, quindi P_*(α, σ) ≢ 0 per tutti gli α salvo un numero finito. Si sceglie un tale α, così che (τ − α) ∤ P_*.
2. *Perturbazione.* Si sceglie f ∈ C_c^∞(J° ∖ [x_1 − η, x_1 + η]) con f ≢ 0, e si pone h := e^{αt}f e u′ := u + h.
3. *Ann_q(h) = (τ − α).* Si ha P(∂_t, L_q)h = e^{αt}P(α, L_q)f. Se p(σ) := P(α, σ) ≠ 0, allora p(L_q)f = 0 è un'EDO lineare con coefficiente di testa costante non nullo e f ha supporto compatto; per unicità di Cauchy f ≡ 0, assurdo. Quindi P(α, ·) ≡ 0, cioè (τ − α) | P.
4. *Ann_q(u′) ⊇ (P_*(τ − α)).* È chiaro, perché gli operatori di S commutano.
5. *Ann_q(u′) ⊆ (P_*(τ − α)).* Sia R ∈ Ann_q(u′) e g := Ru = −Rh.
   - (τ − α)g = −R(τ − α)h = 0, quindi (τ − α)R ∈ Ann_q(u) = (P_*). Dato che τ − α è irriducibile e non divide P_*, si ha P_* | R.
   - P_*g = RP_*u = 0, quindi P_*Rh = −P_*g = 0, cioè P_*R ∈ (τ − α), e quindi (τ − α) | R.
   - P_* e τ − α sono coprimi nel dominio fattoriale S, quindi R ∈ (P_*(τ − α)). ∎

**Nota.** Con questo esempio l'osservazione di S8-ENC («u + e^{αt}x^M esce dalla classe principale») non è più un ostacolo: il supporto compatto di f mantiene principale l'annullatore.

## 11. ENC-Q4: separazione (S) non vuota

**Quadro.** S8-ENC §5, con il modello DM-φ: u ~ u′ ⟺ u′ = e^{iθ(t)}u. Le definizioni sono:
- 𝒱 = {q_0 + c : c ∈ ℝ}, con q_0 ∈ C¹(J) reale, J = [−a, a] e x_0 = 0;
- la **famiglia stretta** è W_c := encoder di Volterra di q_0 + c, normalizzato in x_0, con c_V = 0 e N_V = I (ENC-N1′(v));
- (S) dice: u ∈ 𝒮_V, u′ ∈ 𝒮_{V′}, u ~ u′ ≠ 0 e V ≠ V′ ⇒ [W_Vu] ≠ [W_{V′}u′], con le classi prese modulo fasi.

**Enunciato (a).** Per questa classe e questa famiglia le intersezioni sono non vuote, cioè esistono u ~ u′ ≠ 0 con V ≠ V′, e (S) vale. È il primo esempio con (S) non vacua. Per ENC-N1′(v), qui (C) fallisce, e coerentemente l'encoder cieco non esiste.

*Prova.*
1. *Intersezioni non vuote.* Se u ∈ 𝒮_{q_0}, allora u′ := e^{−ict}u ∈ 𝒮_{q_0+c} e u ~ u′.
2. *(S), riduzione alla fase.* Siano V = q_0 + c, V′ = q_0 + c′, δ := c′ − c ≠ 0, e u′ = e^{iθ_1}u con entrambe soluzioni non nulle. Sottraendo le equazioni su {u ≠ 0}, che è aperto e non vuoto, si trova −θ_1′ = δ. Quindi u′ = e^{iκ}e^{−iδt}u.
3. *Ipotesi per assurdo.* Supponiamo W_{V′}u′ = e^{iθ(t)}W_Vu.
4. *θ è costante.* w := W_Vu e w′ := W_{V′}u′ sono entrambe soluzioni libere: W L_q = L_0W con c_V = 0. Da w′ = e^{iθ}w segue θ′w = 0, quindi θ ≡ θ_0 su ogni intervallo dove w(t, ·) ≢ 0, cioè ovunque, perché W è invertibile e u(t, ·) ≢ 0. **[rev2, C-15: il passo «u(t, ·) ≢ 0 per ogni t» è falso in generale; la prova corretta, localizzata su una componente di {t : u(t, ·) ≢ 0}, è in rev2 e sostituisce i passi 2–7.]**
5. *Problema agli autovalori.* W_{V′} agisce solo in x, quindi e^{iκ − iδt}Zw(t) = e^{iθ_0}w(t), con Z := W_{V′}W_V^{−1}. Per ogni t, w(t) è dunque un autovettore di Z con autovalore μ(t) = e^{i(θ_0 − κ + δt)}.
6. *Z = I + 𝒱 con 𝒱 quasinilpotente.* Per ENC-1, W_V = I + ∫_{−x}^{x}H(x, s)·ds e W_{V′}^{±1} ha la stessa forma, con nuclei limitati. La composizione di due operatori di questa forma è ancora di questa forma: in ∫_{−x}^{x}H_1(x, s)∫_{−s}^{s}H_2(s, r)dr ds si ha |r| ≤ |s| ≤ |x|.

   Quindi Z = I + 𝒱 con 𝒱f(x) = ∫_{−|x|}^{|x|}k(x, r)f(r)dr e k limitato. Ponendo G_n(ρ) := max(|𝒱^nf(ρ)|, |𝒱^nf(−ρ)|) si ha G_{n+1}(ρ) ≤ 2‖k‖∫_0^ρG_n, quindi ‖𝒱^n‖_{C(J)} ≤ (2‖k‖a)^n/n! e σ(𝒱) = {0}.
7. *Conclusione.* Zw = μw con w ≠ 0 dà μ − 1 ∈ σ(𝒱) = {0}, cioè μ(t) = 1 per ogni t ∈ I. Quindi δ = 0: contraddizione. ∎

**(c) Lettura DM3 letterale** (𝒮_V ∩ 𝒮_{V′} ≠ {0} senza quoziente).
- Per V = V(x), l'intersezione è {0} per VAR-T1(b): (S) è vacua.
- Per V(t, x) le intersezioni non banali esistono. §3 dà u ∈ 𝒮_0 ∩ 𝒮_{1_Z}, ma V′ = 1_Z non è regolare e gli encoder indipendenti dal tempo non esistono (ENC-P0(b)).

**APERTO** (nessuna riduzione). Il caso naturale successivo, ENC-P0 con encoder W(t) dipendenti dal tempo, è già registrato come aperto in S8-ENC.

## 12. ENC-Q10: encoder non locali espliciti per V(t, x) non quadratico

**Quadro.** Sia u una soluzione libera senza zeri su Ω, cioè iu_t + u_xx = 0; per esempio u = x² + 2it su Ω = ℝ × (0, ∞) (SymPy T9a). Si pongono V_1 := −2∂_x²log u, che è complesso, dipende da t e non è quadratico, e Λ := ∂_x − u_x/u.

**Enunciato (a), Darboux dipendente dal tempo.**
(i) Λ manda le soluzioni libere nelle soluzioni di iχ_t + χ_xx = V_1χ, cioè L_0χ = V_1χ nella convenzione di S8-VAR (SymPy T9c: vale questo segno, non l'altro). Il nucleo di Λ è ℂu (T9e).
(ii) *Encoder esplicito non locale.* Sia χ una soluzione del modello V_1 nell'immagine di Λ. Si fissa x_0 e si pone
ψ := u·[∫_{x_0}^{x}χ/u dx′ + c(t)], con c′(t) = iκ(t) e κ(t) := (χ_x + (u_x/u)χ)(t, x_0)/u(t, x_0).
Allora Λψ = χ e ψ è libera. L'encoder χ ↦ ψ è unico modulo ℂu, cioè modulo la scelta di c(0). SymPy T9f–T9g verificano la formula su χ = Λ(x³ + 6itx).
(iii) L'encoder è **non locale** in x, per l'integrale, e **non locale in t**, perché c(t) dipende dalla storia di χ in x_0. Non serve alcun cambio del tempo: la forma normale P0′ dice comunque che il tempo non è un invariante.

*Prova di (ii).*
- Λψ = ψ_x − (u_x/u)ψ = χ per costruzione.
- Siano φ libera con Λφ = χ e ψ − φ ∈ ker Λ = {a(t)u}. Imponendo che ψ sia libera: L_0(a u) = i a′u, quindi a′ = 0.
- Il valore di κ è proprio quello che rende a costante. Infatti ψ(t, x_0) = u(t, x_0)c(t), e la condizione libera in x_0 si scrive con χ, χ_x, u e u_x in x_0, usando ψ_x = χ + (u_x/u)ψ e ψ_xx = χ_x + (u_x/u)_xψ + (u_x/u)ψ_x.

  **[rev2, C-17: la derivazione a mano di κ, e anche quella di (i), è in rev2 e sostituisce questo passo.]**

**Osservazione.** 1/u **non** risolve il modello V_1 se u_xx ≠ 0: il residuo è 2u_xx/u², cioè 4/u² per u = x² + 2it (T9d). La «seconda soluzione» standard del Darboux stazionario non si trasporta.

**(c) Residuo.**
- Per V_1 **reale**, regolare e dipendente da t non ho un esempio. Le soluzioni libere reali sono a + bx, che danno V_1 = 2b²/(a + bx)², singolare e indipendente da t.
- Che questi encoder stiano nella classe 𝔈 di (E3), cioè espliciti e con nucleo finito su 𝒴, dipende da come si legge «finito»: qui il nucleo ha dimensione 1 su ogni fetta, ma l'encoder dipende dalla storia.

**APERTO**, da riformulare come in rev2, C-18: la frase «non ho un esempio» è superata dal boost di Galileo. Il rimando al Darboux con coppie di soluzioni (Matveev–Salle, non letto) è un puntatore, non una riduzione. Bisogna anche decidere se la dipendenza dalla storia è ammessa in 𝔈.

## 13. DICT-ILIM-Hs: interpolazione C^s per s ≥ 1

**Enunciato.** Siano Ω ⊂ ℝ^N aperto limitato lipschitziano, s ≥ 0 intero e θ := 2/(2s + 2 + N). Esiste C = C(Ω, s) tale che, per ogni f ∈ C^{s,1}(Ω̄),
‖f‖_{C^s(Ω̄)} ≤ C‖f‖_{L²(Ω)}^θ‖f‖_{C^{s,1}(Ω̄)}^{1−θ}.

*Prova.*
1. *Cono.* Ω soddisfa una condizione di cono uniforme: esistono r_0 > 0 e un cono finito C_0 di altezza r_0 tali che ogni x ∈ Ω̄ è vertice di un cono C_x ⊂ Ω̄ congruente a C_0. **[rev2, C-19: dimostrato in rev2 con un lemma elementare; il rimando ad Adams–Fournier non serve più. In rev2 il vertice sta in Ω e il cono in Ω.]** Per r ≤ r_0 sia C_{x,r} := C_x ∩ B_r(x), con |C_{x,r}| = κ r^N.
2. *Taylor.* Sia M := ‖f‖_{C^{s,1}}, e sia T_x il polinomio di Taylor di grado s in x. Per y ∈ C_{x,r} il segmento [x, y] sta in C_x, e
   f(y) − T_x(y) = Σ_{|α|=s}(s/α!)(y − x)^α∫_0^1(1 − σ)^{s−1}[D^αf(x + σ(y − x)) − D^αf(x)]dσ,
   da cui |f − T_x| ≤ c_1M r^{s+1} su C_{x,r}. Per s = 0 si usa direttamente la lipschitzianità.
3. *Polinomi sul cono.* Su 𝒫_s, lo spazio dei polinomi di grado ≤ s, la norma L²(C_{0,1}) e la norma |D^βP(0)| sono equivalenti: lo spazio ha dimensione finita e il cono ha interno non vuoto. Per rotazione la costante è uniforme in x. Per scaling, |D^βP(x)| ≤ c_0r^{−|β|−N/2}‖P‖_{L²(C_{x,r})}.
4. *Stima puntuale.* ‖T_x‖_{L²(C_{x,r})} ≤ ‖f‖_2 + c_1Mr^{s+1}(κr^N)^{1/2}. Siccome D^βf(x) = D^βT_x(x),
   |D^βf(x)| ≤ c_0r^{−|β|−N/2}‖f‖_2 + c_2Mr^{s+1−|β|}.
5. *Scelta di r.* Si prende r := (‖f‖_2/M)^θ. Se r > r_0 si prende r = r_0 (vedi il passo 7).
   - Per |β| = s i due termini sono entrambi ≍ ‖f‖_2^θM^{1−θ}, perché r^{s+1+N/2} = ‖f‖_2/M.
   - Per |β| = j < s si ottiene ‖f‖_2^{θ_j}M^{1−θ_j}, con θ_j := 2(s + 1 − j)/(2s + 2 + N) > θ.
6. *Ordini bassi.* ‖f‖_2 ≤ |Ω|^{1/2}M, quindi ‖f‖_2^{θ_j}M^{1−θ_j} ≤ |Ω|^{(θ_j−θ)/2}‖f‖_2^θM^{1−θ}.
7. *Caso r > r_0.* Ciò significa ‖f‖_2 > r_0^{1/θ}M. Con r = r_0 la stima diventa |D^βf| ≤ C(‖f‖_2 + M) ≤ C′‖f‖_2, e ‖f‖_2 ≤ (|Ω|^{1/2})^{1−θ}‖f‖_2^θM^{1−θ}. ∎

**Conseguenza.** Il corollario di I-LIM (S8-DICT §4) vale per s ≥ 1 con l'esponente θ = 2/(2s + 2 + N) già dichiarato. DICT-ILIM-Hs passa da CANDIDATO a prova scritta.

## 14. DICT-U3d-v: velocità per nuclei completamente monotoni generali

**Quadro.** k(t) = ∫_{[0,∞)}e^{−λt}dμ(λ) con μ ≥ 0 e k ∈ L¹(0, T) (S8-DICT §1.4). Si pongono:
- m_k(Λ) := μ([0, Λ]);
- τ_k(Λ) := ∫_{(Λ,∞)}dμ(λ)/λ, che tende a 0 per Λ → ∞ perché k ∈ L¹;
- C_k := ∫min(T, 1/λ)dμ ≤ ‖k‖_{L¹(0,T)}/(1 − e^{−1}).

**Teorema.** Siano J ≥ 1 e Λ > 0, e siano λ_1, …, λ_J i nodi di Čebyšëv di [0, Λ]. Si pone
k_J(t) := Σ_jc_je^{−λ_jt}, con c_j := ∫_{[0,Λ]}ℓ_j(λ)dμ(λ),
dove ℓ_j sono i polinomi di Lagrange nei nodi. Allora:
(i) per ogni t ∈ [0, T], |k(t) − k_J(t)| ≤ 2(ΛT/4)^J/J!·m_k(Λ) + ∫_{(Λ,∞)}e^{−λt}dμ;
(ii) ‖k − k_J‖_{L¹(0,T)} ≤ 2T(ΛT/4)^J/J!·m_k(Λ) + τ_k(Λ);
(iii) m_k(Λ) ≤ C_k max(1/T, Λ). Con Λ_J := 4J/(e²T),
   ‖k − k_J‖_{L¹(0,T)} ≤ 2e^{−J}max(1, 4J/e²)·C_k + τ_k(4J/(e²T));
(iv) su [δ, T], in norma sup: ‖k − k_J‖_{L^∞(δ,T)} ≤ 2(ΛT/4)^J/J!·m_k(Λ) + e^{−Λδ/2}k(δ/2). Questo dà errore ≤ ε(m_k(Λ) + k(δ/2)) con Λ = 2log(1/ε)/δ e J = O((T/δ)log(1/ε)).

*Prova.*
1. *Errore di interpolazione.* Per t fissato, la funzione λ ↦ e^{−λt} ha derivata J-esima limitata da t^J ≤ T^J. L'errore dell'interpolazione di Čebyšëv con J nodi su un intervallo di lunghezza Λ è ≤ Λ^J/(2^{2J−1}J!)·T^J = 2(ΛT/4)^J/J! (resto di Lagrange e |T_J| ≤ 1: prova elementare in rev2, C-20; non serve la fonte).
2. *Termine sui λ bassi.* ∫_{[0,Λ]}e^{−λt}dμ − k_J(t) = ∫_{[0,Λ]}(e^{−λt} − Σℓ_j(λ)e^{−λ_jt})dμ.
3. *Coda.* La coda è ∫_{(Λ,∞)}e^{−λt}dμ. Questo dà (i); integrando in t si ottiene (ii).
4. *Massa.* Su [0, Λ] si ha min(T, 1/λ) ≥ min(T, 1/Λ), da cui (iii).
5. *Caso (iv).* ∫_{(Λ,∞)}e^{−λt}dμ ≤ e^{−Λδ/2}∫e^{−λδ/2}dμ = e^{−Λδ/2}k(δ/2) per t ≥ δ. Infine (ΛT/4)^J/J! ≤ (eΛT/(4J))^J ≤ e^{−J} per J ≥ e²ΛT/4. ∎

**Lettura.**
- La velocità è uniforme sulla classe dei nuclei c.m. normalizzati, a meno della sola coda τ_k: la parte d'interpolazione decade come e^{−J}.
- I pesi c_j sono reali di segno qualsiasi. In U3(d)(ii) erano ≥ 0, ma l'immersione markoviana con pesi reali resta un sistema locale aumentato.
- Per k = t^{−β} si ha τ_k(Λ) = Λ^{β−1}/((1 − β)Γ(β)): velocità algebrica J^{β−1} in L¹(0, T). La (iii) di S8-DICT dà la velocità logaritmica in errore relativo su [δ, T].
- SymPy T13 confronta la stima (ii) con l'errore L¹ calcolato per k = 1/(1 + t).

**Resta APERTO**: se la dipendenza da τ_k sia necessaria per approssimanti con J esponenziali **arbitrari**, cioè una stima inferiore non lineare. **Sottodomanda** (nessuna implicazione provata): un limite inferiore per l'approssimazione L¹ con J esponenziali di somme lacunari di esponenziali.

## 15. DICT-Q3: caso intermedio di RANGO

**Quadro.** RANGO (S8-DICT §2.6), con A_u(y) né iniettiva su un denso né suriettiva ovunque. La domanda è come si decide l'esistenza di una legge.

**(c) Riformulazione (per definizione, non è una riduzione).** Una legge θ ∈ C^∞ esiste ⟺ il problema di divisione A_u(y)θ(y) = −L_0u(y) ha una soluzione C^∞. È la definizione, letta attraverso (I) di RANGO. Le condizioni necessarie sono:
- (N1) puntuale: −L_0u(y) ∈ im A_u(y) per ogni y;
- (N2) formale: per ogni y_0 il sistema ha soluzione nelle serie formali in y_0.

**(b) In C^∞, (N1) e (N2) non bastano (controesempio).** Prendo Schrödinger con V reale e u reale, indipendente da t: u(t, x) = e^{−1/x²} per x > 0 e 0 per x ≤ 0. La legge è V = u_xx/u. Allora:
- (N1): per x ≤ 0 si ha u = u_xx = 0, quindi 0 ∈ im A_u. Per x > 0, A_u è iniettiva e suriettiva.
- (N2): in x = 0 tutte le serie sono nulle (u è piatta), quindi θ = 0 è soluzione formale. Per x ≠ 0 il caso è banale.
- Nessuna V continua esiste: su x > 0 la legge è forzata, V = u_xx/u = 4/x^6 − 6/x^4 → +∞ per x → 0⁺ (SymPy T11a–c).

**(a) Caso analitico** (CON-FONTE: Malgrange, *Ideals of Differentiable Functions*, 1966, cap. VI; teorema di Tougeron–Malgrange sui moduli generati da funzioni analitiche; non letto). Se u è reale analitica, (N2) in ogni punto implica l'esistenza di una soluzione C^∞. Per K = q = 1 l'argomento è elementare: il quoziente −L_0u/T_1u è meromorfo e formalmente olomorfo in ogni punto, quindi analitico.

**Esito.** **APERTO — riformulato come** un problema di divisione C^∞. Per u analitica è deciso dal test formale (CON-FONTE). Per u solo C^∞ il test formale e puntuale è insufficiente (controesempio). Il criterio «rango variabile» quindi non decide da solo.

## 16. DICT-Q4: Teorema A(iii) con atomi non locali

**Quadro** (S8-DICT §3.3): D_0, …, D_N sono operatori lineari continui C^∞(Ω) → D′(Ω), linearmente indipendenti; U_n è il misfit e F_n il fit.

**Proposizione.** I due enunciati sono equivalenti:
(1) per ogni M, ogni insieme ℓ_1, …, ℓ_M di funzionali lineari continui e ogni u ∈ F_n esiste v ∈ U_n con ℓ_j(v) = ℓ_j(u), cioè A(iii);
(2) per ogni sottospazio chiuso Z di codimensione finita della forma ∩ker ℓ_j esiste w ∈ Z con D_0w, …, D_Nw indipendenti.

Inoltre (2) vale se nessuna combinazione non banale Σc_iD_i ha rango finito. Se invece qualche combinazione ha rango finito, (1) fallisce.

*Prova.*
- *(2) ⇒ (1).* È l'ultimo passo della prova di S8-DICT §3.3: il polinomio s ↦ det(ℓ′_j(D_i(u + sw))) ha coefficiente direttore det(ℓ′_j(D_iw)) ≠ 0. La località serve solo a produrre w.
- *(1) ⇒ (2).* Si prende u = 0 ∈ F_n. Un v con gli stessi dati sta in Z ed è in U_n.
- *Rango infinito ⇒ (2).* Se ogni w ∈ Z avesse D_0w, …, D_Nw dipendenti, le restrizioni D_i|_Z sarebbero localmente linearmente dipendenti. Per il **lemma di Amitsur** (CON-FONTE, non letto: S. A. Amitsur, Trans. AMS 114 (1965); forma moderna in Brešar–Šemrl, Canad. J. Math. 51 (1999)) esiste c ≠ 0 con rank(Σc_iD_i|_Z) ≤ N. Allora rank(Σc_iD_i) ≤ N + codim Z < ∞.
- *Rango finito ⇒ (1) falso.* Sia D := Σc_iD_i ≠ 0 di rango finito r. Allora Z := ker D è l'intersezione di r funzionali continui (le coordinate sull'immagine, che ha dimensione finita in D′). Su Z la famiglia è dipendente e (2) fallisce. ∎

**(b) Esempio esplicito.** Atomi di media su Ω = (0, 1): D_if := ψ_i·∫_0^1f, con ψ_i = 1, x, x² indipendenti. Un solo dato esatto, ℓ(u) = ∫u = 0, certifica il fit: ogni v con ℓ(v) = 0 ha D_iv = 0 per ogni i (SymPy T12).

**Corollari.**
- Gli operatori differenziali non nulli hanno rango infinito, e si ritrova A(iii).
- Lo stesso vale per i moltiplicatori di Fourier non nulli e per le convoluzioni di Volterra k∗ con k ≢ 0 (rango infinito per Titchmarsh). Per memoria e simboli A(iii) vale quindi **condizionatamente al lemma di Amitsur**.

**Esito.** (a) caratterizzazione, con la direzione «rango infinito ⇒ A(iii)» CON-FONTE; (b) controesempio per atomi di rango finito.

## 17. Robustezza in DM-δ (VAR-Q19, ATTACK-8 O8): enunciato e risposta

**Enunciato del problema.** Classe 𝒰 = 𝒰(M, δ_0, K) delle u ∈ C³(K̄), con K = I × J compatto, tali che:
- |u| ≥ δ_0 su K;
- ‖∂^αu‖_{L^∞(K)} ≤ M per |α| ≤ 3.

A u si associa V_u := (iu_t + u_xx)/u, il potenziale complesso, che è sempre una legge. Il dato è ũ con ‖ũ − u‖_{L^∞(K)} ≤ ε, ε noto. Lo stimatore è una mappa ũ ↦ V̂. Il rischio minimax è
R(ε) := inf_{V̂}sup_{u∈𝒰}sup_{‖ũ−u‖≤ε}‖V̂(ũ) − V_u‖_{L^∞(K′)},
con K′ ⋐ K.

**Teorema.** Esistono c, C > 0, dipendenti da M, δ_0 e K, tali che per ε ≤ ε_0
cε^{1/3} ≤ R(ε) ≤ Cε^{1/3}.

*Prova del limite superiore.*
- Si sceglie V̂(ũ) := V_{u*}, dove u* ∈ 𝒰 è un qualsiasi elemento con ‖u* − ũ‖ ≤ ε. Esiste, perché u stesso lo è.
- e := u − u* soddisfa ‖e‖ ≤ 2ε e ‖e_tt‖, ‖e_xxx‖ ≤ 2M.
- VAR-P3(c) dà ‖V_u − V_{u*}‖ ≤ Cδ_0^{−1}(1 + ‖V_{u*}‖)((2ε)^{1/3}(2M)^{2/3} + (2ε)^{1/2}(2M)^{1/2} + 2ε), con ‖V_{u*}‖ ≤ 2M/δ_0.

  Per ε piccolo domina il termine ε^{1/3}.

*Prova del limite inferiore* (due punti).
- Si fissano u_1 ∈ 𝒰 con margine, |u_1| ≥ 2δ_0 e derivate ≤ M/2 (per esempio una costante), e x_0 interno a K′. **[rev2, C-24: serve l'ipotesi M > δ_0; la scelta corretta è u_1 ≡ (M + δ_0)/2, con φ riscalata ed ε_0 esplicito.]**
- Si pone h := εφ((x − x_0)/ε^{1/3}), con φ ∈ C_c^∞, φ(0) = 0, φ″(0) ≠ 0 e ‖φ‖_∞ ≤ 1. Allora ‖h‖_∞ ≤ ε e ‖∂_x^3h‖ = ‖φ‴‖ = O(1). Riscalando φ, u_2 := u_1 + h sta in 𝒰 (SymPy T14).
- In (t, x_0) si ha h = 0, quindi V_{u_2} − V_{u_1} = h_xx/u_1 = ε^{1/3}φ″(0)/u_1(t, x_0).
- Il dato ũ := u_1 + h/2 è ε-vicino a entrambe. Ogni stimatore sbaglia di almeno ½|V_{u_2} − V_{u_1}| ≥ cε^{1/3} su una delle due. ∎

**Lettura.**
- In DM-δ con a priori (M, δ_0) l'identificazione è stabile con esponente esattamente 1/3, e lo stimatore è costruttivo a meno della ricerca di u* in 𝒰. Questa è una ricerca di fattibilità convessa sulle derivate, salvo il vincolo |u| ≥ δ_0, che è locale.
- L'esponente 1/3 di VAR-P3(c) è anche minimax: la «sola stima di modulo» di O8 diventa una risposta con garanzia, nel modello dichiarato.
- Non tocca V reale né il caso con zeri, e non riguarda il rumore stocastico.

---

## Recepimento dell'audit (rev2)

Questa sezione recepisce `work/CHECK-F10/AUDIT_S10-OPEN-C.md` (S-CHECK-F10-C, 27/10/2026) e **prevale** sulle sezioni 0–17 dove le contraddice. Ho riscritto per intero i tre fix sostanziali (C-15, C-17, C-19). Per i fix redazionali C-1…C-24 do il testo corretto, sezione per sezione. Le etichette «ridotto a» sono state tolte dal testo delle sezioni 0–17 e sostituite con «APERTO», «riformulato come» o «sottodomanda», secondo il giudizio di audit §4.

**Verifiche rev2.** Comando: `D:\ProblemaBase\.venv\Scripts\python.exe -I work/S10-OPEN-C/sympy/rev2_checks.py`. Esito: **43/43 OK**. Lo script controlla le identità usate qui sotto: in generale per C-15 e C-17, su esempi o campioni per gli altri fix. Come prima, nessuna prova si appoggia sul calcolo. Non ho eseguito nessuno script di `_vendor`.

### R.1 C-15 (§11, ENC-Q4-S): prova completa con la localizzazione

**Che cosa era sbagliato.** I passi 2, 4 e 7 di §11 usavano «u(t, ·) ≢ 0 per ogni t ∈ I». Per soluzioni classiche su I × J senza condizioni al bordo questo è falso in generale. La serie di Tychonoff di §3 (V = 0) si annulla identicamente per t ∈ K ∩ I, e la stessa costruzione con q_0 = 0 dà soluzioni di 𝒮_c con lo stesso difetto (basta moltiplicare per e^{−ict}). L'enunciato (a) resta invariato; cambia la prova.

**Quadro.** È quello di §11. In particolare u ∈ 𝒮_V e u′ ∈ 𝒮_{V′} sono soluzioni classiche (C¹ in t, C² in x) di iu_t = −u_xx + Vu e di iu′_t = −u′_xx + V′u′ su I × J, con J = [−a, a]. Si ha u ~ u′ ≠ 0, cioè u′(t, ·) = e^{iθ_1(t)}u(t, ·) per ogni t, con θ_1: I → ℝ una funzione qualsiasi (nessuna regolarità è assunta). Inoltre V = q_0 + c, V′ = q_0 + c′ e δ := c′ − c. Le classi [·] sono prese modulo fasi e^{iθ(t)} con θ qualsiasi.

**Enunciato da provare.** Se δ ≠ 0, allora [W_Vu] ≠ [W_{V′}u′].

*Prova.*

0. *L'insieme buono.* Sia G := {t ∈ I : u(t, ·) ≢ 0 su J}.
   - G è aperto. Se u(t_1, x_1) ≠ 0, per continuità u(t, x_1) ≠ 0 per t vicino a t_1.
   - G non è vuoto, perché u ≢ 0.

   Si fissa una componente connessa G_0 di G. È un intervallo aperto non vuoto, e su G_0 lavoro soltanto. Fuori da G si ha u(t, ·) ≡ 0, quindi anche u′(t, ·) ≡ 0, e quei tempi non danno informazione: non servono.

1. *La fase θ_1 è C¹ su G_0, dopo una scelta del sollevamento.* Sia t_1 ∈ G_0 e sia x_1 con u(t_1, x_1) ≠ 0. Per t in un intorno N di t_1 vale u(t, x_1) ≠ 0 e
   e^{iθ_1(t)} = u′(t, x_1)/u(t, x_1),
   che è C¹ in t su N. Quindi t ↦ e^{iθ_1(t)} è C¹ su G_0 a valori nel cerchio unitario. G_0 è un intervallo, quindi esiste un sollevamento C¹, che indico ancora con θ_1, con e^{iθ_1} invariata. Cambiare θ_1 di un multiplo di 2π non cambia u′.

2. *La fase di u′ è lineare in t su G_0.* Su G_0 × J si calcola, usando l'equazione di u:
   iu′_t − (−u′_xx + V′u′) = e^{iθ_1}[(iu_t + u_xx − Vu) − θ_1′u − δu] = (−θ_1′ − δ)e^{iθ_1}u.
   Il primo membro è nullo, perché u′ ∈ 𝒮_{V′}. Per ogni t ∈ G_0 esiste x con u(t, x) ≠ 0, quindi θ_1′(t) = −δ. Ne segue che esiste κ ∈ ℝ con θ_1(t) = κ − δt su G_0, cioè u′ = e^{i(κ − δt)}u su G_0 × J. (rev2_checks: «C-15 passo 2».)

3. *Ipotesi per assurdo.* Supponiamo [W_Vu] = [W_{V′}u′]: esiste θ: I → ℝ con W_{V′}u′(t) = e^{iθ(t)}W_Vu(t) per ogni t. Si pongono w := W_Vu e w′ := W_{V′}u′. Per ENC-1 e per la scelta c_V = 0, N_V = I, sono soluzioni libere classiche (W L_q = L_0 W nella convenzione di S8-ENC). Gli operatori agiscono solo in x e sono invertibili su C(J) (ENC-1).

4. *θ è costante su G_0.* Per t ∈ G_0 si ha u(t, ·) ≢ 0, quindi w(t, ·) = W_Vu(t, ·) ≢ 0 per l'iniettività di W_V. Come nel passo 1, intorno a ogni t_1 ∈ G_0 si sceglie x_1 con w(t_1, x_1) ≠ 0. Allora e^{iθ(t)} = w′(t, x_1)/w(t, x_1) è C¹ vicino a t_1, e si prende un sollevamento C¹ di θ su G_0. w e w′ = e^{iθ}w sono entrambe libere, quindi
   0 = iw′_t + w′_xx = e^{iθ}(iw_t + w_xx) − θ′e^{iθ}w = −θ′e^{iθ}w.
   Per ogni t ∈ G_0 esiste x con w(t, x) ≠ 0, quindi θ′ ≡ 0 su G_0: θ ≡ θ_0 su G_0, perché G_0 è connesso. (rev2_checks: «C-15 passo 4».)

5. *Problema agli autovalori su G_0.* W_{V′} agisce solo in x, quindi per t ∈ G_0
   W_{V′}u′(t) = e^{i(κ − δt)}W_{V′}u(t) = e^{i(κ − δt)}Zw(t), con Z := W_{V′}W_V^{−1}.
   Per il passo 3 questo vale e^{iθ_0}w(t). Quindi Zw(t) = μ(t)w(t), con μ(t) := e^{i(θ_0 − κ + δt)}, e w(t) ≠ 0.

6. *Z = I + 𝒱 con 𝒱 quasinilpotente.* È il passo 6 di §11, invariato: la composizione di operatori di Volterra simmetrici resta di Volterra simmetrica, ‖𝒱^n‖_{C(J)} ≤ (2‖k‖a)^n/n! e σ(𝒱) = {0}. Questo passo non usa u.

7. *Conclusione.* Per t ∈ G_0, Zw(t) = μ(t)w(t) con w(t) ≠ 0 dà (μ(t) − 1) ∈ σ_p(𝒱) ⊂ σ(𝒱) = {0}, cioè μ(t) = 1. Quindi θ_0 − κ + δt ∈ 2πℤ per ogni t ∈ G_0. Il primo membro è continuo in t e G_0 è connesso, quindi è costante su G_0. G_0 è un intervallo aperto non vuoto, quindi δ = 0: contraddizione con δ ≠ 0. ∎

**Osservazioni.**
- La prova usa una sola componente G_0 e non richiede alcuna regolarità di θ_1 e di θ fuori da G_0. Le fasi arbitrarie del modello DM-φ sono quindi ammesse senza ipotesi di misurabilità.
- Il punto 1 di §11 (intersezioni non vuote, u′ = e^{−ict}u) e la lettura (c) restano invariati, salvo l'etichetta: (c) è **APERTO** senza riduzione (C-16).
- **Stato proposto:** ENC-Q4-S (a) da PROVA SCRITTA a DIMOSTRATO, dopo la rilettura di questo testo da parte del coordinatore o dell'audit (criterio dell'audit, §0).

### R.2 C-17 (§12, ENC-Q10-D): derivazione a mano di κ, e di (i)

**Notazioni.** L_0 = i∂_t + ∂_x². «Libera» vuol dire L_0f = 0, cioè f_t = if_xx. u è libera e senza zeri su Ω = I × J, con J intervallo (quindi connesso in x). Si pone U := u_x/u, così Λf = f_x − Uf = u∂_x(f/u), e V_1 := −2∂_x²log u = −2U_x.

**(i) Λ manda le soluzioni libere in soluzioni di L_0χ = V_1χ (a mano).** Sia φ libera e χ := Λφ = φ_x − Uφ.
- Da iu_t = −u_xx e u_xx/u = U_x + U² segue iU_t = ∂_x(iu_t/u) = −∂_x(U_x + U²) = −U_xx − 2UU_x.
- Da iφ_t = −φ_xx segue iχ_t = ∂_x(iφ_t) − iU_tφ − U(iφ_t) = −φ_xxx − iU_tφ + Uφ_xx.
- Inoltre χ_xx = φ_xxx − U_xxφ − 2U_xφ_x − Uφ_xx.
- Sommando: L_0χ = −iU_tφ − U_xxφ − 2U_xφ_x = (U_xx + 2UU_x)φ − U_xxφ − 2U_xφ_x = −2U_x(φ_x − Uφ) = V_1χ.

Il nucleo di Λ su ogni fetta è ℂu, perché Λf = 0 ⟺ ∂_x(f/u) = 0 e J è connesso. (rev2_checks: «C-17 (i)», in generale.)

**(ii) Formula di κ.** Sia χ nell'immagine di Λ, e sia φ libera con Λφ = χ. Il Wronskiano è
W := uφ_x − u_xφ = u(φ_x − Uφ) = uχ.
Dato che φ_t = iφ_xx e u_t = iu_xx,
∂_t(φ/u) = (uφ_t − φu_t)/u² = i(uφ_xx − φu_xx)/u² = iW_x/u²,
perché W_x = uφ_xx − u_xxφ (i termini u_xφ_x si cancellano). Da W = uχ segue W_x = u_xχ + uχ_x, quindi
∂_t(φ/u) = i(u_xχ + uχ_x)/u² = i(χ_x + (u_x/u)χ)/u.
In x = x_0 questo è iκ(t), con κ(t) := (χ_x + (u_x/u)χ)(t, x_0)/u(t, x_0). Il secondo membro dipende **solo da χ e da u**, non dalla scelta di φ. (rev2_checks: «C-17 ∂_t(φ/u) = iW_x/u²» e seguente, in generale.)

**Che ψ sia libera.** Si pone ψ := u·[∫_{x_0}^{x}χ/u dx′ + c(t)], con c ∈ C¹(I).
1. Λψ = u∂_x(ψ/u) = u·χ/u = χ.
2. Λ(ψ − φ) = 0, quindi ψ − φ = a(t)u con a(t) = (ψ/u − φ/u)(t, x_0) = c(t) − (φ/u)(t, x_0). a è C¹, perché c lo è e φ/u è C¹ in t.
3. Dato che u è libera, L_0(au) = ia′u + aL_0u = ia′u. Quindi L_0ψ = L_0φ + ia′u = ia′u.
4. u non si annulla, quindi ψ è libera ⟺ a′ ≡ 0 ⟺ c′(t) = ∂_t(φ/u)(t, x_0) = iκ(t).

Questo prova (ii): ψ è libera esattamente quando c′ = iκ.

**Unicità modulo ℂu.** Se ψ̃ è libera con Λψ̃ = χ, allora ψ̃ − ψ = b(t)u e, per il punto 3, ib′u = L_0(ψ̃ − ψ) = 0, cioè b è costante. L'encoder χ ↦ ψ è quindi unico modulo ℂu, cioè modulo la scelta di c(0).

Sull'esempio u = x² + 2it, χ = Λ(x³ + 6itx), x_0 = 1, la formula dà ψ libera con Λψ = χ e ψ − (x³ + 6itx) ∈ ℂu (rev2_checks). **Stato proposto:** ENC-Q10-D (i), (ii) da PROVA SCRITTA a DIMOSTRATO, dopo rilettura.

**C-18 ((c) e OC-7).** Esiste un esempio **reale**, regolare e dipendente da t. Sia u_G(t, x) := (x − 2kt + a)e^{i(kx − k²t)}, con k ≠ 0. È il boost di Galileo della soluzione libera x + a, quindi è libera. Infatti, per g(t, x) = v(t, x − 2kt) e Φ = kx − k²t, si ha L_0(e^{iΦ}g) = e^{iΦ}(L_0v)(t, x − 2kt). Inoltre
V_1 = −2∂_x²log u_G = 2/(x − 2kt + a)²,
reale, dipendente da t, e regolare su I × J se J ⊂ (2k sup I − a, ∞) (k > 0, I limitato). Λ_G produce soluzioni del modello reale (rev2_checks: «C-18»). L'esempio è banale, perché è un boost di Galileo di un caso stazionario, ma rende falsa la frase di §12(c) «per V_1 reale, regolare e dipendente da t non ho un esempio». Il residuo va riformulato così: **APERTO** — esistono esempi reali di Darboux dipendente dal tempo **non riconducibili per simmetria** (Galileo, lente) a potenziali stazionari? Il rimando a Matveev–Salle resta un puntatore, non una riduzione. Lo stesso vale per OC-7 (prima metà).

### R.3 C-19 (§13, DICT-ILIM-Hs): lemma del cono elementare

**Lemma (cono uniforme).** Sia Ω ⊂ ℝ^N aperto limitato con bordo lipschitziano. Per L > 0 e h > 0 sia Γ(L, h) := {z ∈ ℝ^N : z_N > L|z′|, |z| < h}, con z = (z′, z_N). Esistono L > 0, h > 0 e, per ogni x ∈ Ω, una rotazione R_x tali che
C_x := x + R_xΓ(L, h) ⊂ Ω.

*Definizione usata.* «Bordo lipschitziano» vuol dire questo: per ogni p ∈ ∂Ω esistono un moto rigido y = R_p(x − p) + p, un raggio r_p > 0 e una funzione φ_p: ℝ^{N−1} → ℝ con Lip φ_p ≤ L_p tali che, nelle coordinate y, Ω ∩ B(p, r_p) = {y ∈ B(p, r_p) : y_N > φ_p(y′)}.

*Prova.*
1. *Una carta.* Siano p ∈ ∂Ω, x ∈ Ω ∩ B(p, r_p/2), e z con z_N > L_p|z′| e |z| < r_p/2, nelle coordinate y. Allora x + z ∈ B(p, r_p). Inoltre
   x_N + z_N > φ_p(x′) + L_p|z′| ≥ φ_p(x′ + z′),
   dove la prima disuguaglianza usa x ∈ Ω ∩ B(p, r_p), cioè x_N > φ_p(x′), e la seconda è la lipschitzianità. Quindi x + z ∈ Ω ∩ B(p, r_p). Ne segue x + R_p^{−1}Γ(L_p, r_p/2) ⊂ Ω.
2. *Compattezza.* ∂Ω è compatto, quindi è coperto da un numero finito di palle B(p_i, r_i/4), i = 1, …, m. Si pongono L := max_iL_i e d_0 := min_ir_i/4. Se L ≥ L_i e h ≤ r_i/2, allora Γ(L, h) ⊂ Γ(L_i, r_i/2), perché il cono più stretto è contenuto in quello più largo.
3. *Punti vicini al bordo.* Sia x ∈ Ω con dist(x, ∂Ω) < d_0, e sia q ∈ ∂Ω con |x − q| < d_0. Si ha q ∈ B(p_i, r_i/4) per qualche i, quindi |x − p_i| < r_i/4 + d_0 ≤ r_i/2. Per il punto 1, x + R_{p_i}^{−1}Γ(L, d_0) ⊂ Ω, perché d_0 ≤ r_i/2.
4. *Punti lontani dal bordo.* Se dist(x, ∂Ω) ≥ d_0, la palla B(x, d_0) non incontra ∂Ω ed è connessa e contiene x ∈ Ω, quindi B(x, d_0) ⊂ Ω. Questa palla contiene x + RΓ(L, d_0) per ogni rotazione R.
5. Si prende h := d_0. ∎

**Proprietà usate nei passi 2–3 di §13.**
- Γ(L, h) è convesso: è l'intersezione del cono convesso {z_N > L|z′|} (|·| è una norma) con una palla. È anche stellato rispetto al vertice: se z ∈ Γ e σ ∈ (0, 1], allora σz ∈ Γ. Quindi per y ∈ C_x il segmento (x, y] sta in C_x ⊂ Ω, e il resto di Taylor del passo 2 è lecito.
- Per r ≤ h, C_{x,r} := x + R_xΓ(L, r) = C_x ∩ B_r(x), e |C_{x,r}| = κr^N con κ := |Γ(L, 1)|, per scaling (in N = 2: |Γ(L, r)| = r²arctan(1/L), rev2_checks).
- Nel passo 3 di §13 la norma di 𝒫_s su L²(R_xΓ(L, 1)) è ‖P∘R_x‖_{L²(Γ(L,1))}. Il gruppo delle rotazioni agisce su 𝒫_s con operatori di norma limitata uniformemente (gruppo compatto, spazio di dimensione finita), quindi la costante c_0 non dipende da x.
- *Da Ω a Ω̄.* La stima del passo 4 di §13 si fa per x ∈ Ω. Per f ∈ C^{s,1}(Ω̄) le derivate D^βf, |β| ≤ s, sono continue su Ω̄, quindi sup_{Ω̄}|D^βf| = sup_Ω|D^βf|. Il passo 1 di §13 va letto con «x ∈ Ω» e «C_x ⊂ Ω» al posto di «x ∈ Ω̄» e «C_x ⊂ Ω̄». Il raggio r_0 del passo 1 è h.

**Stato proposto:** DICT-ILIM-Hs DIMOSTRATO (da CON-FONTE), dopo rilettura; Adams–Fournier esce dalla lista «CIT da verificare».

### R.4 Fix redazionali e di stato, sezione per sezione

**§1, C-1.**
- *Limite sinistro nel Lemma C.* Per 0 < k ≤ t − s:
  k^{−1}[F(t) − F(t − k)] = k^{−1}∫_{t−s−k}^{t−s}T(σ)f(t − σ)dσ + ∫_0^{t−s−k}T(σ)k^{−1}[f(t − σ) − f(t − k − σ)]dσ.
  Il primo termine tende a T(t − s)f(s) per continuità forte, uniformemente su intervalli compatti. Il secondo tende a ∫_0^{t−s}T(σ)f′(t − σ)dσ: l'integrando è limitato da M_0 sup‖f′‖, converge per continuità uniforme di f′, e l'intervallo mancante ha lunghezza k → 0. Quindi F è derivabile anche da sinistra, con la stessa derivata. Per il dominio basta il limite destro, come già scritto.
- *Ogni soluzione classica è mite.* Sia v ∈ C¹([s, T]; X) ∩ C([s, T]; D(A_0)) con v′ = (A_0 + B)v. Per t fissato, g(r) := T(t − r)v(r) è derivabile su [s, t]:
  h^{−1}[g(r + h) − g(r)] = T(t − r − h)h^{−1}[v(r + h) − v(r)] + h^{−1}[T(t − r − h) − T(t − r)]v(r) → T(t − r)v′(r) − T(t − r)A_0v(r),
  per limitatezza uniforme e continuità forte nel primo termine e per v(r) ∈ D(A_0) nel secondo. Quindi g′(r) = T(t − r)B(r)v(r), che è continua. Integrando da s a t: v(t) = T(t − s)v(s) + ∫_s^tT(t − r)B(r)v(r)dr. Questo completa l'unicità dichiarata nell'enunciato.

**§2, C-2 e C-3.**
- Enunciato corretto (riportato anche in §2): n := ‖x‖ è il numero della costruzione, e U(t, 0)x_* ∉ D(A_0) per ogni t ∈ (0, T] con sin(nt) ≠ 0, non solo per t < π/n. La prova è quella di §2: y(t) = (sin(nt)/n)T(t)x ∉ D(A) se sin(nt) ≠ 0.
- *Realizzazione dentro L²(J) (facoltativa, dall'audit).* Con H_0 = −∂² di Neumann su L²(J), si prende e = costante normalizzata (H_0e = 0), x ⊥ e con x ∉ D(H_0), e B(t)y := ⟨y, e⟩f(t) − ⟨y, f(t)⟩e con f(t) = e^{−itH_0}x. È la stessa costruzione, con ℂ sostituito da ℂe; la prova è identica, perché e^{−itH_0}e = e e f(t) ⊥ e. Resta fuori solo il caso di una **moltiplicazione** (OC-1).
- C-3: VAR-Q18-mult è **APERTO**, sottocaso residuo, senza riduzione (testo di §2 corretto).

**§4, C-4, C-5, C-6.**
- *C-4, v ∈ L^∞.* Per B(t) = −i(V_0 + v(t)) misurabile e limitato in norma, la soluzione mite è ancora unica: la differenza e di due soluzioni miti soddisfa ‖e(t)‖ ≤ M_0β_0∫_0^t‖e‖, e Gronwall dà e ≡ 0. La funzione ψ(t) := e^{−iΦ(t)}e^{−itH}ψ_0, con Φ(t) := ∫_0^tv, soddisfa l'equazione di Duhamel. Per ψ_0 ∈ D(H_0), ψ è lipschitziana a valori in L², derivabile q.o. con ψ′ = −i(H + v)ψ. Allora r ↦ e^{−i(t−r)H_0}ψ(r) è lipschitziana con derivata q.o. −ie^{−i(t−r)H_0}(V_0 + v(r))ψ(r). In uno spazio di Hilbert una funzione lipschitziana è l'integrale di Bochner della sua derivata (proprietà di Radon–Nikodym), e si ottiene l'equazione mite. Per ψ_0 qualsiasi si passa al limite, perché i due membri dipendono in modo continuo da ψ_0 in L². Quindi ψ è la soluzione mite, e il gauge del passo 1 di §4 è lecito. In alternativa basta restringere v a funzioni continue a tratti.
- *C-5, lemma delle medie: il termine di bordo.* Dopo Fubini il termine di Duhamel è ∫_0^TΦ_r dr, con Φ_r := ∫_0^{T−r}h(r + σ)T(σ)y_r dσ e y_r := B(r)ψ(r). Per k ∈ C¹([0, b]) e y ∈ X vale
  ∫_0^bk(σ)T(σ)y dσ ∈ D(A_0), con A_0∫_0^bkTy = k(b)T(b)y − k(0)y − ∫_0^bk′(σ)T(σ)y dσ
  (rev2_checks, formula scalare). Con k(σ) = h(r + σ) e b = T − r si ha k(b) = h(T) = 0 e k(0) = h(r), quindi
  A_0Φ_r = −h(r)y_r − ∫_0^{T−r}h′(r + σ)T(σ)y_r dσ.
  Il termine −h(r)y_r, che la prima versione ometteva, è limitato e continuo in r, come l'altro. A_0 è chiuso, quindi ∫_0^TΦ_r dr ∈ D(A_0) (teorema di Hille per integrali di Bochner) e il lemma resta vero.
- *C-6.* VAR-Q17(b) è **APERTO**. «Continuazione laterale per soluzioni miti con V(t, x)» è la domanda riscritta, non una riduzione; l'ostruzione di §4(c) è euristica. Restano corretti la formula per R_φ e il fatto che R_φ = 0 su ω.

**§5, C-7.**
- (a) I due tratti hanno la stessa durata: τ_2 := π/(4ω_1) = τ_1, scritto così di proposito. Allora θ_1 = 2ω_1τ_1 = π/2 e θ_2 = 2ω_2τ_2 = 10ω_1·π/(4ω_1) = 5π/2. I fattori sono M_1 = [[0, 1/ω_1], [−ω_1, 0]] e M_2 = [[0, 1/ω_2], [−ω_2, 0]], e M = M_2M_1 = diag(−ω_1/ω_2, −ω_2/ω_1) = diag(−1/5, −5), con tr M = −26/5.
- (b) *Continuità in ω.* Sia ω_n una successione uniformemente limitata con ω_n² → ω² in L¹(0, T); per esempio le mollificazioni di ω costante a tratti. Siano Y_n, Y le soluzioni di Y′ = A(t)Y, Y(0) = I, con A = [[0, 2], [−2ω², 0]]. Allora
  ‖Y_n(t) − Y(t)‖ ≤ ∫_0^t‖A_n − A‖‖Y‖ + ∫_0^t‖A_n‖‖Y_n − Y‖,
  e Gronwall (con sup_n‖A_n‖_∞ < ∞ e ‖Y‖ limitato) dà Y_n → Y uniformemente. Quindi tr M_n → −26/5 < −2, e per n grande M_n non è un esponenziale. Due regolarizzazioni tanh danno tr = −4.81, −5.13, −5.20 (larghezze 0.05, 0.02, 0.005; rev2_checks).
- (c) Il risultato vale solo per i logaritmi quadratici, con potenziale non limitato. VAR-P12(d) chiede di V(t, x) generico e di logaritmi differenziali qualsiasi, e resta **APERTO**. La domanda di §5(c) è una sottodomanda (OC-3), senza implicazione verso (d).
- (d) ID separato: **VAR-P12(d)-quad** (DIMOSTRATO), invece di «(d) FALSO nella classe quadratica».

**§6, C-8 e C-9.**
- *C-8, prova elementare della non D-finitezza (sostituisce Wiman–Valiron).* Sia f(y) := exp(e^y). Si ha f^{(k)} = f·T_k(e^y), con T_0 = 1 e T_{k+1}(Z) = Z(T_k(Z) + T_k′(Z)). Infatti d/dy[fT_k(e^y)] = fe^yT_k(e^y) + fT_k′(e^y)e^y. Per induzione T_k è monico di grado k (polinomi di Touchard; rev2_checks per k ≤ 10).

  Sia u(t, x) = f(x + t), così ∂_x^ku = ∂_t^ku = f(x + t)T_k(e^{x+t}). Supponiamo Σ_{k≤K}a_k(t, x)∂_x^ku = 0 con a_k ∈ ℂ[t, x] e a_K ≠ 0. Dividendo per f ≠ 0 si ottiene Π(t, x, e^{x+t}) ≡ 0, dove Π(t, x, Z) := Σ_ka_k(t, x)T_k(Z). Il coefficiente di Z^K in Π è a_K ≠ 0, perché T_k è monico di grado k, quindi Π ≠ 0.

  Ora t, x ed e^{x+t} sono algebricamente indipendenti. Con x = y − t, Π̃(t, y, Z) := Π(t, y − t, Z) è non nullo e Π̃(t, y, e^y) ≡ 0. Si fissa t_0 con Π̃(t_0, ·, ·) ≠ 0. Allora q(y, e^y) ≡ 0 per un q ≠ 0 in ℂ[y, Z]. Scrivo q = Σ_{j≤m}p_j(y)Z^j con p_m ≠ 0: per y reale → +∞, dividendo per p_m(y)e^{my} si ottiene 1 + Σ_{j<m}(p_j/p_m)(y)e^{−(m−j)y} → 1 ≠ 0. Assurdo.

  Lo stesso vale con ∂_t al posto di ∂_x. Quindi nessun operatore non nullo di ℂ[t, x]⟨∂_x⟩, né di ℂ[t, x]⟨∂_t⟩, annulla u: u non è D-finita, nel senso che le sue derivate non generano uno spazio di dimensione finita su ℂ(t, x). Il passaggio per la restrizione a t = 0 di un olonomo diventa superfluo. Il resto di (b) è invariato: (∂_t − ∂_x)u = 0, quindi Ann(u) ∋ ∂_t − ∂_x ∉ A_2□. **Stato proposto:** VAR-C3Q2-R (b) DIMOSTRATO.
- *C-9.* VAR-Q13 (non monico) è **APERTO**, senza riduzione; l'equivalenza non provata è ritirata (testo di §6 corretto).

**§7, C-10.** Nel Lemma E, per Q ∈ ℝ[ξ] non costante e X grande (Q′ ≠ 0 e monotona su [X, 2X]), integrando per parti:
∫_X^{2X}e^{iQ} = [e^{iQ}/(iQ′)]_X^{2X} − ∫_X^{2X}e^{iQ}d(1/(iQ′)),
quindi |∫_X^{2X}e^{iQ}| ≤ 1/|Q′(X)| + 1/|Q′(2X)| + |1/Q′(2X) − 1/Q′(X)| = O(1). La variazione totale di 1/Q′ su [X, 2X] è |1/Q′(2X) − 1/Q′(X)| per monotonia. Diviso per X tende a 0, e la conclusione del lemma non cambia (rev2_checks, tre polinomi). Nella riga di Fase 8, Q-S8SYS-1 va diviso: (a) formale DIMOSTRATO, (b) a t fisso con tempi reali DIMOSTRATO, tempi complessi APERTO (OC-5).

**§8, C-11 e C-12.**
- *C-11, basi saturate.* Sia 𝒪 := ℂ[ξ]_{(ξ−ξ_0)}, che è un DVR, e sia E_𝒪 := E(ξ) ∩ 𝒪^n.
  - 𝒪^n/E_𝒪 è privo di torsione: se (ξ − ξ_0)^jv ∈ E con v ∈ 𝒪^n, allora v ∈ E, perché E è un ℂ(ξ)-sottospazio.
  - Su un PID un modulo finitamente generato privo di torsione è libero, quindi E_𝒪 è un addendo diretto di 𝒪^n.
  - È libero di rango k = dim E, perché ogni vettore di E, moltiplicato per un denominatore comune, sta in E_𝒪.

  Una base e_1, …, e_k di E_𝒪, completata a una base di 𝒪^n, si riduce modulo (ξ − ξ_0) a vettori linearmente indipendenti di ℂ^n. Quindi e(ξ_0) ha rango k. Le entrate di e sono razionali e regolari in ξ_0, quindi analitiche, e E(ξ) = im e(ξ) → im e(ξ_0) = E_0 nella grassmanniana. Lo stesso vale per F. «Dividere le colonne per potenze di (ξ − ξ_0)» da solo non basta: possono servire operazioni di colonna. Il resto della prova di §8(a) è invariato.
- *C-12, controesempio rafforzato.* Sia S la permutazione e_1 ↦ e_2, e_2 ↦ e_3, e_3 ↦ e_1, e sia A_2′ := SA_2S^{−1}. Allora:
  - A_2′(0) = A_1(0) **come matrici** (entrambe E_23);
  - A_2′ e A_1 hanno lo stesso polinomio caratteristico e la stessa fattorizzazione Q = τ − ξ, B = (τ + ξ)(τ + 2ξ);
  - il proiettore di A_2′ è SP_{A_2}S^{−1}, con un elemento 1/(2ξ) (polo), mentre quello di A_1 è diag(1, 0, 0) (rev2_checks).

  Quindi il polo non è funzione di (A(ξ_0), fattorizzazione), nemmeno a parità di matrice A(ξ_0). Q-S8SYS-4 è **FALSO** in questa lettura; la versione corretta è il criterio (a), che dipende dai limiti E_0, F_0.

**§9, C-13 (osservazione).** Per Auslander–Buchsbaum, depth (M_P)_𝔪 = 4 − pd (M_P)_𝔪 ≥ 1 se pd ≤ 3, e depth ≥ 1 equivale a Hom(k, (M_P)_𝔪) = 0. La frase finale di §9 va letta così: il teorema vale per ogni sistema con pd M_P ≤ n − 1. Qui pd M_P ≤ 2. Lo stato resta quello di SYS-C1: dipende da SYS-EX come registrato.

**§10, C-14.** Si richiede che J° ∖ [x_1 − η, x_1 + η] abbia interno non vuoto (corretto nell'enunciato di §10); altrimenti non c'è spazio per f. Il passo 5 si può accorciare come nota l'audit (da P_* | R segue Ru = 0, quindi Rh = 0 e (τ − α) | R), ma la versione scritta è corretta.

**§11, C-16.** (c) è **APERTO**, senza riduzione (testo corretto).

**§14, C-20 e C-21.**
- *C-20, errore di Čebyšëv elementare.* Sia g ∈ C^J([0, Λ]) e sia p il suo interpolante nei J nodi λ_j. Per λ non nodale si sceglie K in modo che ϕ(σ) := g(σ) − p(σ) − KΠ_j(σ − λ_j) si annulli anche in λ. ϕ ha allora J + 1 zeri, e per Rolle ripetuto ϕ^{(J)}(η) = 0 per un η: g^{(J)}(η) = KJ!. Quindi g(λ) − p(λ) = g^{(J)}(η)Π_j(λ − λ_j)/J!. Con i nodi di Čebyšëv di [0, Λ] si ha Π_j(λ − λ_j) = (Λ/2)^J2^{1−J}T_J(2λ/Λ − 1), quindi |Π| ≤ 2(Λ/4)^J. Per g(λ) = e^{−λt} si ha |g^{(J)}| = t^Je^{−λt} ≤ T^J. Ne segue la stima 2(ΛT/4)^J/J! del passo 1. Non serve la fonte (rev2_checks: max|Π| = 2(Λ/4)^J per J = 3, …, 9, ed errore effettivo sotto la stima).
- *Fattore 2 in (iv).* Con Λ = 2log(1/ε)/δ e J ≥ max(e²ΛT/4, log(1/ε)), il termine di interpolazione è ≤ 2e^{−J}m_k(Λ) ≤ 2εm_k(Λ) e la coda è ≤ e^{−Λδ/2}k(δ/2) = εk(δ/2). L'errore su [δ, T] è quindi ≤ 2εm_k(Λ) + εk(δ/2) ≤ 2ε(m_k(Λ) + k(δ/2)), con J = O((T/δ)log(1/ε)). La lettura di (iv) va corretta con questo fattore 2.
- *C-21.* L'ottimalità è **APERTA**: il limite inferiore per somme lacunari è una sottodomanda, senza implicazione provata (testo corretto).

**§15, C-22.**
- (c) è la definizione di legge riletta come problema di divisione: **APERTO — riformulato come** problema di divisione C^∞ (testo corretto).
- (a): in più variabili «meromorfa e formalmente olomorfa in ogni punto ⇒ olomorfa» richiede la fedele piattezza del completamento. Se g = a/b con a, b analitici in y_0 e â = b̂ĉ in ℂ[[y − y_0]], allora a ∈ b𝒪̂ ∩ 𝒪 = b𝒪, dove 𝒪 è l'anello delle serie convergenti in y_0. L'uguaglianza vale perché 𝒪̂ è fedelmente piatto su 𝒪 (𝒪 è locale noetheriano). Quindi a = bc con c analitico. Lo stato di (a) resta CON-FONTE (Malgrange 1966) per il caso generale.

**§16, C-23.** *Funzioni test duali.* Siano D_0w, …, D_Nw ∈ 𝒟′ linearmente indipendenti, e sia Ψ: C_c^∞ → ℂ^{N+1}, φ ↦ (⟨D_iw, φ⟩)_i. Se l'immagine di Ψ fosse un sottospazio proprio, esisterebbe c ≠ 0 con Σc_i⟨D_iw, φ⟩ = 0 per ogni φ, cioè Σc_iD_iw = 0 in 𝒟′: assurdo. Quindi Ψ è suriettiva, e si scelgono φ_j con Ψ(φ_j) = e_j. I funzionali ℓ′_j := ⟨·, φ_j⟩ danno la matrice identità, quindi det(ℓ′_j(D_iw)) = 1 ≠ 0.

**§17, C-24.** *Ipotesi di non degenerazione.* Si aggiunge al teorema l'ipotesi M > δ_0; se M < δ_0 la classe 𝒰 è vuota. Il limite inferiore si scrive così.
- u_1 :≡ (M + δ_0)/2. Allora |u_1| = δ_0 + (M − δ_0)/2 = M − (M − δ_0)/2, e le derivate sono nulle.
- Si fissa φ_0 ∈ C_c^∞((−R, R)) con φ_0(0) = 0 e φ_0″(0) ≠ 0, e si pone φ := cφ_0 con c := min(1, (M − δ_0)/2)/max_{j≤3}‖φ_0^{(j)}‖_∞. Così ‖φ‖_∞ ≤ 1 e ‖φ^{(j)}‖_∞ ≤ (M − δ_0)/2 per j ≤ 3.
- h := εφ((x − x_0)/ε^{1/3}), con ∂_x^jh = ε^{1−j/3}φ^{(j)}. Per ε ≤ 1 si ha ‖∂_x^jh‖ ≤ (M − δ_0)/2 per j ≤ 3 e ‖h‖ ≤ ε.
- ε_0 := min((M − δ_0)/4, ε_1, 1), con ε_1 := (d/R)³ e d := dist(x_0, ∂J′), così supp h ⊂ K′ per ε ≤ ε_1.
- Per ε ≤ ε_0, u_2 := u_1 + h soddisfa δ_0 ≤ |u_2| ≤ M e |∂^αu_2| ≤ (M − δ_0)/2 ≤ M per 1 ≤ |α| ≤ 3, quindi u_2 ∈ 𝒰 (rev2_checks con M = 3, δ_0 = 1).
- Il resto è invariato: V_{u_2} − V_{u_1} = ε^{1/3}φ″(0)/u_1 in (t, x_0), ũ := u_1 + h/2 è ε/2-vicino a entrambe, e R(ε) ≥ ½ε^{1/3}|φ″(0)|·2/(M + δ_0).

Le costanti c, C dipendono ora da M, δ_0, K, K′ e da φ_0. **Stato proposto:** DM-δ-MINIMAX DIMOSTRATO con l'ipotesi M > δ_0.

### R.5 Etichette «ridotto a»: elenco delle sostituzioni

| sede | prima | dopo (rev2) |
|---|---|---|
| intro, tipo (c) | «APERTO — ridotto a …» | ostruzione dimostrata, oppure «APERTO — riformulato come …» / «sottodomanda» |
| §0, riga 15 | «(c) ridotto a divisione» | «(c) riformulato come problema di divisione (APERTO)» |
| §2, VAR-Q18-mult | «ridotto a: P11(e) per moltiplicazioni …» | **APERTO**, sottocaso residuo |
| §4(c), VAR-Q17(b) | «ridotto a: continuazione laterale …» | **APERTO — riformulato come** (è la domanda stessa) |
| §5(c), VAR-P12(d) | «ridotto a: metaplettici con tr < −2 …» | **APERTO**; **sottodomanda** OC-3 senza implicazione |
| §6, VAR-Q13 | «ridotto a: rank_B e saturazione» | **APERTO**, nessuna riduzione; equivalenza ritirata |
| §11(c), ENC-Q4 DM3 | «ridotto a ENC-P0 con W(t)» | **APERTO**; ENC-P0 con W(t) già aperto in S8-ENC |
| §12(c), ENC-Q10 V reale | «ridotto a: Darboux reale (Matveev–Salle)» | **APERTO**, riformulato come in C-18; puntatore |
| §14, ottimalità | «ridotto a: limite inferiore per somme lacunari» | **sottodomanda**, APERTO |
| §15(c) e Esito | «Riduzione», «ridotto a divisione» | «Riformulazione (per definizione)», «APERTO — riformulato come» |

### R.6 Stati proposti dopo rev2

Gli stati restano proposte per il coordinatore. Per i claim passati da PROVA SCRITTA a DIMOSTRATO l'audit chiede una rilettura del testo di rev2 prima della promozione. `LEDGER_ROWS.md` non è stato modificato in questa revisione; le correzioni dell'audit §5 restano da riportare lì.

| claim | stato proposto (rev2) | fix |
|---|---|---|
| VAR-P11(e), VAR-L2-cor | DIMOSTRATO | C-1 |
| VAR-Q18-CE | DIMOSTRATO (controesempio); «P11(e) per B continuo» FALSO | C-2 |
| VAR-Q18-mult | APERTO | C-3 |
| VAR-Q10-EX | DIMOSTRATO; chiude VAR-T1(c)-Q10 | — |
| VAR-Q17(a) | DIMOSTRATO (v ∈ L^∞ con C-4) | C-4, C-5 |
| VAR-Q17(b) | APERTO | C-6 |
| VAR-P12(d)-quad (nuovo ID) | DIMOSTRATO | C-7 |
| VAR-P12(d) | APERTO | C-7(c) |
| VAR-C3Q2-R (a) | DIMOSTRATO | — |
| VAR-C3Q2-R (b) | DIMOSTRATO (Wiman–Valiron esce) | C-8 |
| VAR-C3Q2-R (a′) | CON-FONTE (Bernstein, Björk cap. 1) | — |
| VAR-Q13 | APERTO | C-9 |
| SYS-DIRAC-POL (a), (b) | DIMOSTRATO; tempi complessi APERTO | C-10 |
| II-T2(b′)-CRIT (a) | DIMOSTRATO | C-11 |
| Q-S8SYS-4 | FALSO (lettura «A(ξ_0) e fattorizzazione», anche a parità di matrice) | C-12 |
| SYS-MAXWELL | DIMOSTRATO, dipendente da SYS-EX come SYS-C1 | C-13 |
| ENC-T2(c′)-P | DIMOSTRATO | C-14 |
| ENC-Q4-S (a) | PROVA SCRITTA → DIMOSTRATO dopo rilettura di R.1 | C-15 |
| ENC-Q4 (DM3) | APERTO | C-16 |
| ENC-Q10-D (i), (ii) | PROVA SCRITTA → DIMOSTRATO dopo rilettura di R.2 | C-17 |
| ENC-Q10 residuo | APERTO, riformulato (esempi non riconducibili per simmetria) | C-18 |
| DICT-ILIM-Hs | CON-FONTE → DIMOSTRATO dopo rilettura di R.3 | C-19 |
| DICT-U3d-v (velocità) | DIMOSTRATO (Čebyšëv elementare) | C-20 |
| DICT-U3d-v (ottimalità) | APERTO | C-21 |
| DICT-Q3-R (b) | DIMOSTRATO | — |
| DICT-Q3-R (c) | APERTO (riformulato) | C-22 |
| DICT-Q3-R (a) | CON-FONTE (Malgrange 1966) | C-22 |
| DICT-Q4-C (1) ⟺ (2), rango finito | DIMOSTRATO | C-23 |
| DICT-Q4-C rango infinito | CON-FONTE (Amitsur 1965 / Brešar–Šemrl 1999) | — |
| DM-δ-MINIMAX | DIMOSTRATO con M > δ_0 | C-24 |

**CIT da verificare dopo rev2.** Escono Wiman–Valiron (C-8), la formula di Čebyšëv (C-20) e Adams–Fournier (C-19). Restano Björk (Bernstein), Malgrange 1966 e Amitsur 1965 / Brešar–Šemrl 1999.
