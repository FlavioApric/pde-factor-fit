# AUDIT S8-VAR — S-CHECK-F8-VAR · 27/10/2026

**Revisore.** S-CHECK-F8-VAR, proof-checker indipendente.

**Oggetto.** Il pacchetto S8-VAR: `work/S8-VAR/PROOF_PACKAGE.md` §1–§8, `CHECK_REQUEST.md`, `LEDGER_ROWS.md` e gli 8 script in `work/S8-VAR/sympy/`. Ho letto solo enunciati, ipotesi e prove, senza il contesto della sessione autrice.

**Riferimenti.** `NOTAZIONE.md` v5 (DM-φ, mappa residuo) e `research/CIT-AUDIT/AUDIT-6.md` (righe 19, 59, 66, 84–86).

**Skill.** Ho letto i SKILL.md di claim-lifecycle, proof-checker (Phase 0.5, checklist A–H, red team, severità a due assi, acceptance gate), kill-argument e scientific-critical-thinking. Non ho eseguito nessuno script `_vendor`. Il formato segue `work/CHECK/AUDIT_OP-F5A.md`.

**Kill-argument su VAR-T1.** File `KA_VAR_T1_{input,attack,adjudication}.md`. L'input è un estratto verbatim di §1.2–§1.5 e della stima di Cauchy di §7.1, att. 9; ho tolto il "Respinto" dell'autore. L'attacco è di un subagente indipendente che ha letto solo l'input. Esito: **SURVIVES**, con un rilievo MAGGIORE di portata.

**Numerica indipendente** (`work/CHECK-F8/sympy/`, eseguita con python -I, tutti gli script danno "TUTTO OK"):
- `var_carleman`: prova simbolica dell'identità di Carleman tramite l'operatore di Eulero–Lagrange.
- `var_misc`: controesempi e casi limite per E1, VMPUM, P3, P5(c), P9(d), T10(ii), la portata L^∞ di T1(b), E2 e la stima di Cauchy.
- `var_num`: Pöschl–Teller ℓ = 1, 2 confrontato con uno split-step di Strang, e l'oscillatore confrontato con lo sviluppo esatto in funzioni di Hermite. Il metodo è diverso da quello di s8_pt e s8_osc.

Ho rieseguito gli 8 script dell'autore: tutti danno "TUTTO OK".

## 0. Verdetti

| ID | verdetto | finding | stato LEDGER proposto |
|---|---|---|---|
| VAR-N1 | OK | — | **DIMOSTRATO** |
| VAR-T1(a) | OK | VAR-14 (segno) | **DIMOSTRATO** |
| VAR-L0 | OK; identità ora provata simbolicamente | VAR-17 | **DIMOSTRATO** |
| VAR-L1 | OK (KA: SURVIVES) | VAR-16 (letteratura) | **DIMOSTRATO** (prova autosufficiente; quasi certamente noto, nessuna priorità) |
| VAR-L2 | OK (KA: SURVIVES) | VAR-16 | **DIMOSTRATO** |
| VAR-T1(b) | OK come enunciato (KA: SURVIVES); **portata sovrastimata** | **VAR-1 (MAJOR)** | **DIMOSTRATO** nella classe dichiarata (u ∈ C^{1,2}). "Lacuna V ∈ L^∞ chiusa" vale solo dopo VAR-1(b) (soluzioni forti, derivazione nel §2.1 qui sotto) |
| VAR-T1(c) (i)–(iii) | OK (KA: SURVIVES) | VAR-1, VAR-14 | **DIMOSTRATO**. Caso L^∞ con \|Z(u)\| > 0 e int Z(u) = ∅: **APERTO** (VAR-Q10) |
| VAR-T1(c)-F | confutazione verificata | — | **FALSO** (controesempio di Tychonoff verificato) |
| VAR-P3 | OK con fix MINOR | VAR-10 | **DIMOSTRATO** |
| VAR-P4 | **lacuna nella prova di (a)**, enunciato vero | **VAR-2 (MAJOR)** | **DIMOSTRATO dopo VAR-2** (riparazione scritta nel §2.4) |
| VAR-P5 | (a), (b) OK; il "⟺" di (c) è falso nella classe continua | VAR-9 | (a), (b) **DIMOSTRATO**; (c) **DIMOSTRATO** nella classe puntuale (dopo VAR-9) |
| VAR-T2a | OK | — | **DIMOSTRATO** |
| VAR-T6 | OK modulo il teorema fondamentale di Picard–Vessiot | VAR-13 | **CON-FONTE** (E^G = K e corrispondenza di Galois; numero vdPS da verificare); il resto della prova è controllato |
| VAR-E1 | conclusione vera, **un passo della prova è falso** | **VAR-3 (MAJOR)** | **DIMOSTRATO dopo VAR-3** (argomento corretto nel §2.6) |
| VAR-E2 | OK | — | **DIMOSTRATO** |
| VAR-VMPUM | delta (3) **falso come scritto** | **VAR-4 (CRITICAL locale)**, VAR-12 | **CON-FONTE (solo abstract)**; delta (3) da restringere |
| VAR-P8(a) | OK | — | **DIMOSTRATO** |
| VAR-P8(b) | "⟹" OK; "⟸" è il metodo di Wei–Norman | — | "⟹" **DIMOSTRATO**; "⟸" **CON-FONTE** (Wei–Norman 1964, locale in t) |
| VAR-P8(c) | OK con fix MINOR (domini); numerica indipendente OK | VAR-8 | **DIMOSTRATO** (Crum: CON-FONTE solo per l'attribuzione) |
| VAR-P8(d) | forma chiusa OK; sviluppo O(t³) solo numerico | VAR-15 | forma chiusa **DIMOSTRATO**; sviluppo **V-ex** |
| VAR-P9 | OK | — | **DIMOSTRATO** |
| VAR-P11 | (a)–(c) OK; (d) OK con fix MINOR | VAR-11 | (a)–(d) **DIMOSTRATO**; (e) **CON-FONTE** (Pazy cap. 5) |
| VAR-T10 | (1) OK; (3)(i)–(ii) OK con fix; (4): **ipotesi di Casas non riportata** | **VAR-5 (MAJOR)**, **VAR-6 (MAJOR)**, VAR-7 | (1), (3)(i)–(ii) **DIMOSTRATO**; (3)(iii) **CON-FONTE + V-ex**; (2), (5) **CON-FONTE**; (4) **CON-FONTE** con l'ipotesi di normalità |
| VAR-T10-F | va riformulato | **VAR-6** | **FALSO** solo nella forma "la parola chirp·libero·chirp si rompe al tempo della lente/Fourier"; la frase "si rompe a cos t = 0" è **vera** nella normalizzazione del progetto H = −∂² + x² |
| VAR-P12 | (a)–(c) OK | VAR-15 | (a)–(c) **DIMOSTRATO**; (d) **APERTO** |
| VAR-C3Q2 | (a)–(e), (g) OK; (f) OK come esempio | — | (a)–(e), (g) **DIMOSTRATO**; (f) **DIMOSTRATO** (esempio d'ostruzione); caso non monico e criterio intrinseco per m ≥ 2: **APERTO** |

**Conteggio.**
- FATAL: nessuno.
- CRITICAL: uno, VAR-4. È confinato a una frase di confronto bibliografico (§2.4), non a un teorema, e si ripara con una parola.
- MAJOR: sei (VAR-1, VAR-2, VAR-3, VAR-5, VAR-6, e VAR-14 per la sola parte di enunciato). Tutti hanno una riparazione già scritta in questo audit.
- Nessun claim del cammino critico cade.

## 1. Phase 0.5 — registro degli obblighi (sintesi)

**DAG delle dipendenze.**
- Catena di identificazione: VAR-L0 → VAR-L1 → VAR-L2 → VAR-T1(b)(i) → VAR-T1(b)(ii) → VAR-P4, e VAR-L2 → VAR-T1(c)(ii).
- Catena ODE: VAR-T2a → VAR-T6 [E^G = K] → VAR-E1, VAR-E2.
- Catena di Lie: VAR-P8(a) → VAR-P8(b) → VAR-T10(5).
- Catena non autonoma: VAR-P11 → VAR-P12 e VAR-T10.
- VAR-C3Q2 è autonomo.
- Nessuna dipendenza circolare.

**Ipotesi controllate punto per punto.**
- In VAR-L1, B ⊂ N ∩ Ω e la lente sta dentro int B (8ε/3 < b, 2ε < a²).
- In VAR-L2:
  - R_s ⊂ Ω, perché φ_s ≤ b″ < sup J;
  - gli estremi del grafico stanno in W, perché [t_1 − δ, t_2 + δ] ⊂ I.
- In VAR-T1(b) servono u ≢ 0 e u_x continua.
- In VAR-T6 servono il campo delle costanti ℂ e l'estensione di Picard–Vessiot.
- In VAR-C3Q2(e) servono ĝ ∈ C_c^∞ e supporti disgiunti (1/(n(n+1)) > 2^{−n−1} ≥ 3·2^{−n−3}).

**Ordine dei limiti.** In VAR-L1 il raggio ε resta fisso e λ → ∞, con costanti dipendenti solo da B, g e ‖V‖_{L^∞(B)}. In VAR-P3 le costanti C dipendono solo da ℓ_t e ℓ_x. Non ho trovato ambiguità.

## 2. Verifica per claim

### 2.1 VAR-L0, VAR-L1, VAR-L2, VAR-T1 (cammino critico)

**VAR-L0, domanda Q1.**
- (i) P_λ = S + A è verificato simbolicamente. L'identità con q come scritto è **corretta** e ora è **provata simbolicamente** per φ generica (`var_carleman` (2)): la densità |Pz|² − |Sz|² − |Az|² − q è una divergenza totale, perché il suo operatore di Eulero–Lagrange in (a, b) è nullo. Con il segno opposto del termine incrociato fallisce (3).
  - Il conto a mano coincide con quello del package:
    - −4λ∫φ_xx z_xx z̄ = 4λ∫φ_xx|z_x|² + 4λ∫φ_xxx z_x z̄ cancella −4λφ_xxx∂_x;
    - Re(−4iλφ_xt z_x z̄) = 4λφ_xt Im(z_x z̄);
    - la parte immaginaria −2λφ_xt(|z|²)_x − 2λφ_xxt|z|² ha integrale nullo.
- (ii) L'assorbimento è corretto: 8μp² + q²/(2μ) − 4pq = (4μp − q)²/(2μ). Inoltre 4λ³φ_x²φ_xx ≥ 2μλ³.
- (iii) La mollificazione è corretta.

**VAR-L1.**
- Su s ∈ [0, b] vale μs² ≤ s/4, quindi φ ≤ −(3/4)s − (t − t_0)², e la lente sta in int B.
- Supporto di w: w = 0 per s < 0 per ipotesi, perché B ⊂ N.
- La formula di R è corretta.
- I pesi danno e^{−λε} su supp R ed e^{−λε/2} su Λ. Corretto.

**VAR-L2.**
- ∪_{s<s′}R_s = R_{s′} perché ψ > 0 su T.
- La chiusura del grafico è compatta in W, gli estremi sono coperti dal passo 0, l'η-intorno e l'inclusione R_s ⊂ R_{s*} ∪ (η-intorno) sono corretti.
- La riflessione x ↦ −x conserva L_0. Corretto.

**VAR-T1(b).**
- (i) Si ha u_x(t, x_0) = 0. Inoltre |iu_t + u_xx| ≤ C|u| q.o. tra funzioni continue, quindi la disuguaglianza vale ovunque, e da questo u_xx(t, x_0) = 0.
- L'estensione per zero è C^{1,2}: la derivata destra di u_x in x_0 è u_xx(t, x_0) = 0.
- (ii) Per Fubini, su rettangoli dove u ≠ 0 vale V = W q.o., e J ∖ X_0 è un aperto di misura piena. Corretto.

**VAR-T1(c).**
- (ii) Il quadrato di semilato r/2 sta nella palla di raggio r. Corretto.
- (iii) La stima di Cauchy |(1+ζ)^{−2} − 1| ≤ (1−θ)^{−2} − 1 ≈ 0.235 < 1/2 è corretta, e la controprova numerica (`var_misc` (9)) dà un rapporto massimo di 0.54.
- Le serie derivate sono maggiorate da j!(2/(θt))^j exp(2x²/(θt) − 1/(2t²)), che tende a 0.

**Rilievo di portata (VAR-1, accolto anche dal KA, punto A5).**
- Con u ∈ C^{1,2}, la funzione Vu = iu_t + u_xx è continua. Quindi V ha un rappresentante continuo su {u ≠ 0}, e in (b) su J ∖ X_0, dove X_0 è discreto.
- Un salto di V in x_1 forza u(·, x_1) ≡ 0 (`var_misc` (7)).
- La buca quadrata non è coperta.

**Riparazione VAR-1(b).** La verifico qui, con lo stesso metodo, nella classe

> **(SF)** u, u_x ∈ C(Ω), u_t, u_xx ∈ L²_loc(Ω), L_0u = Vu q.o.

Vale per VAR-L0, VAR-L1, VAR-L2 e VAR-T1(b), (c):
1. La densità di VAR-L0 vale per w a supporto compatto con w, w_t, w_xx ∈ L², con convergenza in L².
2. In VAR-L1, R contiene solo u e u_x, quindi R ∈ L².
3. VAR-L2 è invariato.
4. In VAR-T1(b)(i):
   - u_x(t, x_0) = 0 per continuità di u_x;
   - ũ_x = 1_{x≥x_0}u_x è continua;
   - quindi ũ_xx = 1_{x≥x_0}u_xx e ũ_t = 1_{x≥x_0}u_t nel senso delle distribuzioni, senza delta;
   - non serve u_xx(t, x_0) = 0.

### 2.2 VAR-N1, VAR-T1(a)

Corretti. La congruenza ∂^α ≡ r_α (mod J) è verificata per induzione.

### 2.3 VAR-P3

- (a) L_0e = (V_1 − V_2)u_1 + V_2e. Corretto.
- (b) Corretto: ‖e‖_{C¹} ≤ (1 + (1 + |E|)/k)k^{−1/2}.
- (c) Le due disuguaglianze di Taylor sono corrette, con un limite sul passo (VAR-10):
  - la prima, con y ± h, richiede h ≤ ℓ/2 perché uno dei due punti stia nell'intervallo;
  - la seconda, con la differenza seconda unilaterale, richiede 2h ≤ ℓ/2, cioè h ≤ ℓ/4;
  - cambiano solo le costanti.
- La nitidezza dell'esponente 1/3 vale anche per la stima su V, non solo per l'interpolazione. Lo mostra la famiglia (b) con a → 0, k → ∞: ‖V_1 − V_2‖/(‖e‖^{1/3}‖e_xxx‖^{2/3}) → 1 (`var_misc` (3): 1.001, 1.00001, 1.0000000). Conviene scriverlo.

### 2.4 VAR-P4: lacuna (VAR-2, MAJOR)

**Dove sta la lacuna.** La prova di (a) afferma "V(x) − θ′(t) = W(x) per q.o. (t,x); quindi θ′ è costante". In realtà l'uguaglianza vale solo q.o. su {u ≠ 0}, e u può tacere su intere fasce temporali anche con V = V(x).

**Esempio.** La serie di Tychonoff di VAR-T1(c)(iii) ha V = 0, che è indipendente da t, e u = 0 per t ≤ 0. Lì θ′ è arbitrario. L'enunciato (a) resta vero, ma l'argomento "θ′ ≡ c su I" è falso.

**Riparazione.** Sia S_+ := {t : u(t,·) ≢ 0}, aperto in I.
1. Ogni punto (t, x) con u(t, x) ≠ 0 ha un intorno rettangolare dove vale V(x) − W(x) = θ′(t) q.o. Quindi θ′ è localmente costante su S_+, e dunque costante, uguale a c_i, su ogni componente I_i di S_+.
2. Per VAR-T1(b)(i) applicato su I_i × J, l'insieme X_i := {x : u(t, x) ≠ 0 per qualche t ∈ I_i} ha complementare discreto. Inoltre V − W = c_i q.o. su X_i.
3. Due insiemi X_i, X_j co-discreti si intersecano in un insieme di misura positiva, quindi c_i = c_j =: c.
4. Ne segue W = V − c q.o. su J. Fuori da S_+ la fase non è vincolata, ma lì il dato è nullo.

Lo stesso commento vale per la frase di (c): la classe [u] è più grande quando u ha fasce di silenzio, ma l'insieme dei W compatibili non cambia.

### 2.5 VAR-P5

(a) e (b) sono corretti: la componente v_+ trasla come f(x − t), e Y_0 ⊃ (0, 0.5] ∪ [1.7, 2).

**(c), VAR-9.** Il "⟺" vale per la determinazione **puntuale**, cioè nella classe di tutte le funzioni matriciali, ma è falso nella classe continua.

*Controesempio* (`var_misc` (4)):
- Dirac libero con m = 0 e V = 0, ψ = f(x − t)v_+ + h(x + t)v_−, con h supportata in (0.8, 1) e x_0 = 1.
- Lo span di {ψ(t, x_0)} è la retta ℂv_+.
- Per x ∈ (0.8, 1) lo span è ℂ², quindi un W continuo con (W − V)ψ = 0 si annulla in x_0.
- Dunque V(x_0) è determinato anche se lo span in x_0 è una retta.

*Riparazione.* Dichiarare la classe puntuale, oppure enunciare: "V è determinato su un aperto U ⟺ lo span è ℂ² su un sottoinsieme denso di U".

### 2.6 VAR-T2a, VAR-T6, VAR-E1, VAR-E2

**VAR-T2a.** Corretto.

**VAR-T6.**
- (a) La corrispondenza è corretta. Nel verso inverso manca una riga (VAR-13): dim Sol_E(R) = ord R. Si ottiene così: R manda V in Sol(Q), quindi dim ker(R|V) ≥ n − ord Q = ord R.
- (b) Corretto.
- (c), domanda Q4: **sì, il passaggio è corretto.**
  - span_ℂ(G) è una sottoalgebra di dimensione finita di End(V), qualunque sia G.
  - Per un modulo semisemplice di dimensione finita, il teorema di densità di Jacobson dà come immagine il bicommutante. Con End_𝒜(S_i) = ℂ (Schur) il bicommutante è ⊕End(S_i) ⊗ 1_{m_i}.
  - S^m ≅ S ⊗ ℂ^m è ciclico ⟺ m ≤ dim S.
- (d) Corretto.
- (e) È una lettura, non un teorema. Va marcata come tale (VAR-13).

**VAR-E1 (VAR-3, MAJOR).** Il passo "ai poli di w, w′ + w² ha un polo, quindi w è un polinomio" è **falso**: w = 1/x dà w′ + w² = 0 (`var_misc` (1)), e i poli semplici di residuo 1 si cancellano. La conclusione resta vera.

*Argomento corretto.*
1. Ogni soluzione razionale ha la forma w = P + Σ_j 1/(x − a_j), con P polinomio di grado d.
2. Se d ≥ 1, all'infinito w′ + w² ha grado 2d ≥ 2 e coefficiente di testa p_d² ≠ 0, quindi non può essere x.
3. Se d = 0, w′ + w² è limitato all'infinito, mentre x non lo è.
4. Nessuna soluzione razionale esiste, e ∂² − x è irriducibile.

**VAR-E2.** Corretto. La forma w = εx + Σ1/(x − a_j) è giustificata: il coefficiente di x in w′ + w² è 2εc, quindi la costante c è nulla (`var_misc` (8)).
- Le riduzioni a Hermite sono verificate a mano: p″ − 2xp′ + (E − 1)p = 0 per ε = −1, e p″ + 2xp′ + (E + 1)p = 0 per ε = +1.
- La soluzione polinomiale è unica a meno di uno scalare, per la ricorrenza dei coefficienti.

### 2.7 VAR-VMPUM (VAR-4, CRITICAL locale; VAR-12)

**Delta (3).** La frase "un singolo segnale polinomiale-esponenziale ha VMPUM di ordine 1 in ℂ(x)[∂] (2.1(iv))" è **falsa** con la convenzione del progetto, dove EP indica le somme finite Σp_ie^{λ_ix}.
- Per u = e^x + e^{2x} si ha u′/u = (1 + 2e^x)/(1 + e^x) ∉ ℂ(x), e l'annullatore ha ordine 2, con (∂ − 1)(∂ − 2) (`var_misc` (2)).
- La frase vale solo per un singolo termine p(x)e^{λx}, che è iperesponenziale.
- *Riparazione:* "un segnale iperesponenziale (in particolare un solo termine p(x)e^{λx})".

**Citazione (VAR-12).** Il titolo di SLZ 2011 è *Exact linear modeling using Ore algebras*. Il package scrive "…with polynomial coefficients". Volume, pagine e DOI coincidono, e l'abstract è stato letto su arXiv:1004.2924.

### 2.8 VAR-P8

**(a)** Corretto:
- il lemma sul coefficiente di testa 2^jc^{(j)} vale perché [∂², a∂^k] = 2a′∂^{k+1} + a″∂^k;
- vale [f, [∂², g]] = −2f′g′;
- i gradi crescono come d + k(d − 2), strettamente se d ≥ 3.

**(b)** Corretto per la definizione data.

**(c), con Pöschl–Teller.** Ho rifatto a mano A_j†A_j = H_j + j² e A_jA_j† = H_{j−1} + j². La stima H_{j−1} + j² ≥ 2j − 1, il proiettore Q e la formula sono corretti.
- **VAR-8 (MINOR, domini).** Nell'intrecciamento, "per f ∈ H²" non basta: s ↦ U_j(t − s)A_j†U_{j−1}(s)f è derivabile se A_j†U_{j−1}(s)f ∈ D(H_j) = H², ma A_j† manda H² solo in H¹.
  - Riparazione: prendere f ∈ H⁴ = D(H_{j−1}²), che è invariante perché sech² ha tutte le derivate limitate, oppure usare l'identità dei risolventi (H_j − z)^{−1}A_j† = A_j†(H_{j−1} − z)^{−1} su H¹.
  - La conclusione è invariata.
- **Numerica indipendente** (`var_num`): split-step di Strang con dt = 2·10⁻⁴, scatola di lato 60, N = 1024. L'errore relativo è 1.1·10⁻⁸ e 5.0·10⁻⁸ per ℓ = 1 a t = 0.5 e 1.5, e 3.6·10⁻⁸ e 7.5·10⁻⁸ per ℓ = 2.

**(d)** La forma chiusa segue da (c). Lo sviluppo E^add = (t²/2)(A_1A_2 + A_2A_1) + O(t³) con A_1 illimitato è solo numerico e richiede di dichiarare i vettori su cui vale (VAR-15): V-ex.

### 2.9 VAR-P9, VAR-P11, VAR-P12

**VAR-P9.** Corretto: i termini misti di grado 2, i resti 2Σ e 3Σ, la (c) via Gronwall e la (d), dove la norma vale 1/4 (`var_misc` (5)).

**VAR-P11.** (a)–(c) corretti.
- **VAR-11 (MINOR)** in (d): il caso "costante a tratti" esce dall'ipotesi "B fortemente continuo" su cui poggiano (a)–(c).
- Riparazione: enunciare (a)–(c) per B fortemente continuo a tratti, oppure fortemente misurabile e limitato. Le prove sono identiche, perché usano solo integrali di Bochner forti e Gronwall.

**VAR-P12.** (a)–(c) corretti. In (b) basta che a_m sia limitato su supp χ. In (c) la trasformata di Fourier richiede J = ℝ: dichiararlo (VAR-15).

### 2.10 VAR-T10, con Casas 2007 e la correzione "cos t = 0"

**(1) Stark.** Verificato a mano. Le condizioni θ′ = −p² e b′ = −2p annullano i termini residui −(θ′ + p²)φ − i(b′ + 2p)φ_y.

**(3)(i)** Corretto.

**(3)(ii), VAR-7 (MINOR).** La parola L·U·L unipotente esiste se e solo se b ≠ 0 **oppure** M è unipotente inferiore, cioè b = 0 e a = d = 1, nel qual caso σ = 0 e γ_1 = −γ_2.
- Per M = I la parola degenere esiste; per M = −I no (`var_misc` (6)).
- Per l'oscillatore con H = −∂² + x², la parola manca **solo** per t ∈ π/2 + πℤ, dove U = −i·parità (verificato in `var_num`). Per t ∈ πℤ si ha U = −I, che è una parola banale.

**(3)(iii)** Verificato in modo indipendente contro lo sviluppo in funzioni di Hermite: |c| = 1, lo stesso c su due dati diversi, errore ~10⁻¹⁵ per t = 0.3, π/4, 1.3. Lo scalare resta CON-FONTE (Stone–von Neumann e Schur; Folland, cap. 4).

**VAR-6 (MAJOR, NORMALIZATION_MISMATCH), domanda Q6.** Nella normalizzazione del progetto H = −∂² + x² si ha γ(t) = (cos 2t − 1)/(2 sin 2t) = −(tan t)/2, quindi la parola chirp·libero·chirp **si rompe esattamente a cos t = 0**, dove U(t) è la parità a meno di fase.
- La riga LEDGER "VAR-T10-F: 'si rompe a cos t = 0' — FALSO" è quindi falsa nella normalizzazione del progetto.
- È vera solo nella normalizzazione H/2 di F6/DEVIL-6, dove il tempo della lente/Fourier è t = π/2 e la parola lo attraversa.
- In F6 (NOTE riga 68) la frase riguardava la fattorizzazione LDU chirp·dilatazione·libero, che a cos t = 0 si rompe davvero.

**Riformulazione proposta, invariante:**
> "La parola chirp·libero·chirp esiste per l'evoluzione U(t) ⟺ M_12(t) ≠ 0 oppure M(t) è unipotente inferiore. Per l'oscillatore costante fallisce esattamente ai multipli dispari di mezzo periodo, dove U è la parità a meno di fase, e attraversa la caustica della lente. È FALSO che fallisca al tempo della lente/Fourier, come diceva la lettura F6 nella normalizzazione H/2. Una parola fissa vale solo localmente."

Concordo con la sostanza di Q6, a condizione che la normalizzazione sia scritta esplicitamente.

**(4) Casas 2007 (VAR-5, MAJOR, REFERENCE_MISMATCH).** Ho letto il testo su arXiv:0711.2381.
- **Theorem 3.4** dice: la serie di Magnus converge per ∫_0^T‖A(s)‖ds < π se A(t) è un operatore lineare limitato su uno spazio di Hilbert H, con la norma indotta dal prodotto interno.
- Se H ha dimensione infinita, l'enunciato vale solo **"if Y is a normal operator"**. Nella prova (Theorem 3.1) la stima dello spettro tramite il lemma di Mityagin è applicata a Y(t; ε) con ε **complesso** in B, e la normalità è richiesta lì.
- Il raggio π è ottimale per un generico operatore limitato (Example 2, §3).
- Per matrici complesse di dimensione finita il teorema vale senza ipotesi aggiuntive.

Il package scrive "converge per ∫‖A‖ < π per operatori limitati su spazi di Hilbert" senza la condizione di normalità.

*Riparazione:* "Casas 2007, Thm 3.4: in dimensione finita (matrici complesse) incondizionato; su H di dimensione infinita sotto l'ipotesi che Y(t; ε) sia normale". La parentesi di Casas "in particolare se Y è unitario" va letta con cautela, perché per A = −iH(t) l'unitarietà vale per ε reale, mentre l'argomento usa ε complesso.

Le altre parti stanno così:
- il numero del teorema (3.4) è ora verificato;
- la conclusione per V ∈ L^∞ in dimensione infinita resta **CON-FONTE condizionata**;
- la nota di AUDIT-6 riga 19 ("Casas estende agli operatori limitati su Hilbert, π non letto nel testo") va completata con il numero del teorema, π letto e l'ipotesi di normalità.

**(2) e (5)** CON-FONTE, come dichiarato.

### 2.11 VAR-C3Q2

Domanda della CHECK_REQUEST: **C3-Q2 in A_2 è un risultato o un'ostruzione, e il suo stato è onesto?** È tutte e due le cose, e lo stato è onesto con una precisazione.
- **Risultato dimostrato** per L monico in ∂_t:
  - (a) l'unicità della divisione è corretta: il coefficiente di testa di Q′L è q·1;
  - (b) corretto;
  - (c) D-finita ⟺ esiste R ∈ B ∖ {0} con Ru = 0, corretto: W è chiuso per ∂_x e per ∂_t perché ∂_tu = Mu;
  - (d) corretto: per il nucleo del calore vale (1 + 4t)u_x + 2xu = 0;
  - (e), domanda Q5: **sì, l'argomento è completo.**
    - Supporti disgiunti: 1/(n(n+1)) > 2^{−n−1}.
    - ĝ è C^∞ in 0: le derivate sono O(2^{r(n+2)}e^{−n²}).
    - u risolve u_t − iu_xx = 0.
    - La trasformata di Fourier è un automorfismo di A_1, quindi l'operatore trasformato non è nullo.
    - Su (0, δ) l'ODE è regolare, f̂ è nulla sugli intervalli tra i supporti ma non è identicamente nulla, il che contraddice l'unicità di Cauchy.
    - Unico dettaglio: r_d(t_0, ·) ≢ 0 per qualche t_0, perché r_d è un polinomio non nullo. È già nel testo.
  - (g) corretto.
- **Ostruzione documentata:** (f) x∂_t non è mai identificato, perché ∂_t ∈ Ann(u) e ∂_t ∉ A_2x∂_t (dominio più filtrazione di Bernstein). La prova è corretta.
- **Aperti:** il criterio intrinseco per m ≥ 2 (VAR-Q12) e la procedura per il caso non monico (puntatore a Grigoriev–Schwarz, non letto).
- *Precisazione:* nella riga LEDGER lo stato "PROVA SCRITTA; caso non monico: ostruzione registrata" va diviso in tre: (a)–(g) DIMOSTRATO; C3-Q2 **CHIUSO per L monico in ∂_t**; **APERTO** nel caso generale. Non va letto "C3-Q2 chiuso".

## 3. Red team: controesempi tentati

| bersaglio | tentativo | esito |
|---|---|---|
| VAR-L0 | segno opposto del termine incrociato; φ generica con φ_xt, φ_xxxx ≠ 0 | identità provata simbolicamente; col segno opposto fallisce |
| VAR-T1(b) | V con salti; V = 1 su un Cantor grasso (KA) | nessun controesempio; rilievo di portata VAR-1 |
| VAR-T1(c) | stima di Cauchy su 35 coppie (t, k) | rispettata (rapporto ≤ 0.54) |
| VAR-P4 | u con fascia di silenzio (Tychonoff, V = 0) | **lacuna della prova**, enunciato vero (VAR-2) |
| VAR-P5(c) | span che è una retta solo in x_0 | **controesempio al "⟺" nella classe continua** (VAR-9) |
| VAR-E1 | w = 1/x | **controesempio al passo** (VAR-3) |
| VAR-VMPUM | e^x + e^{2x} | **controesempio al delta (3)** (VAR-4) |
| VAR-P3 | nitidezza per V | confermata (rapporto → 1) |
| VAR-P8(c) | ℓ = 1, 2 contro Strang | accordo ~10⁻⁸ |
| VAR-T10 | M = ±I, t = π/2, π | caso degenere VAR-7; normalizzazione VAR-6 |
| VAR-C3Q2(e) | ĝ con supporti che si accumulano in 0 | argomento regge |

## 4. Fix numerati

| fix | severità | claim | categoria | contenuto |
|---|---|---|---|---|
| **VAR-1** | **MAJOR** (OVERSTATED + GLOBAL) | VAR-T1(b), (c); VAR-L0–L2 | SCOPE_OVERCLAIM | (a) Dichiarare che con u ∈ C^{1,2} V è necessariamente continuo su {u ≠ 0} (in (b): fuori da X_0 discreto) e che la buca quadrata non è coperta. (b) Oppure, ed è raccomandato, riscrivere VAR-L0, VAR-L1, VAR-L2 e VAR-T1 nella classe (SF) di §2.1 (u, u_x continue; u_t, u_xx ∈ L²_loc). La derivazione è verificata qui. Solo dopo (b) la frase "lacuna V ∈ L^∞ chiusa" (Q3) è vera. |
| **VAR-2** | **MAJOR** (UNJUSTIFIED + LOCAL) | VAR-P4(a) | LOGICAL_GAP | "θ′ costante" fallisce sulle fasce di silenzio; sostituire con l'argomento per componenti di S_+ del §2.4. |
| **VAR-3** | **MAJOR** (UNJUSTIFIED + LOCAL) | VAR-E1 | LOGICAL_GAP (passo falso) | Il passo "ai poli w′ + w² ha un polo" è falso (w = 1/x); sostituire con l'argomento del §2.6. |
| **VAR-4** | **CRITICAL** (INVALID + LOCAL; confinato a §2.4) | VAR-VMPUM delta (3) | SCOPE_OVERCLAIM | "segnale EP ⇒ VMPUM di ordine 1" è falso per le somme (e^x + e^{2x}); restringere a "iperesponenziale". |
| **VAR-5** | **MAJOR** (UNDERSTATED + LOCAL) | VAR-T10(4) | REFERENCE_MISMATCH | Casas 2007, Thm 3.4: in dimensione infinita serve che Y(t; ε) sia normale; scriverlo e citarlo con il numero del teorema. Il raggio π è verificato e ottimale. |
| **VAR-6** | **MAJOR** (UNCLEAR, tocca una riga FALSO) | VAR-T10-F, VAR-T10(3) | NORMALIZATION_MISMATCH | In H = −∂² + x² la parola si rompe proprio a cos t = 0 (parità). Riformulare VAR-T10-F come nel §2.10, in modo invariante (mezzi periodi dispari, lente attraversata). |
| VAR-7 | MINOR | VAR-T10(3)(ii) | CASE_INCOMPLETE | "⟺ b ≠ 0" va sostituito con "⟺ b ≠ 0 oppure M unipotente inferiore"; per t ∈ πℤ la parola è banale. |
| VAR-8 | MINOR | VAR-P8(c) | REGULARITY_GAP | Intrecciamento: f ∈ H⁴ (oppure l'identità dei risolventi), non f ∈ H². |
| VAR-9 | MINOR | VAR-P5(c) | SCOPE_OVERCLAIM | "⟺" solo nella classe puntuale; nella classe continua usare "span = ℂ² su un sottoinsieme denso". |
| VAR-10 | MINOR | VAR-P3(c) | CONSTANT_DEPENDENCE | Passi h ≤ ℓ/2 e h ≤ ℓ/4; nitidezza per V tramite la famiglia (b). |
| VAR-11 | MINOR | VAR-P11(d) | HIDDEN_ASSUMPTION | Estendere (a)–(c) a B fortemente continuo a tratti. |
| VAR-12 | MINOR | VAR-VMPUM | citazione | Titolo SLZ: *Exact linear modeling using Ore algebras*. |
| VAR-13 | MINOR | VAR-T6(a), (e) | MISSING_DERIVATION | Aggiungere dim Sol_E(R) = ord R (una riga); marcare (e) come lettura. |
| VAR-14 | MINOR (MAJOR solo come enunciato di (c)) | VAR-T1(a), (c) | UNCLEAR | Scrivere nell'enunciato di (c) che il caso L^∞ con \|Z\| > 0 e int Z = ∅ è aperto; aggiungere una riga sull'incollamento C^∞ in t = 0; in (b)(ii) il segno (L_θ = L_0 + θ significa L_0u = −θu). |
| VAR-15 | MINOR | VAR-P8(d), VAR-P12(c) | SCOPE | Sviluppo di E^add con A_1 illimitato: V-ex, con i vettori dichiarati; in P12(c), J = ℝ. |
| VAR-16 | MINOR | VAR-L1, VAR-L2 | ADD_REFERENCE | Saut–Scheurer 1987 (JDE 66, 118–139): il risultato noto (soluzione nulla su un aperto ⇒ nulla sulla componente orizzontale, per V ∈ L^∞_loc) contiene con ogni probabilità VAR-L2 e T1(c)(ii). Da verificare in CIT-AUDIT-8; nessuna priorità. |
| VAR-17 | MINOR | VAR-L0 | evidenza | Citare la prova simbolica `work/CHECK-F8/sympy/var_carleman.py` al posto del solo controllo numerico. |

## 5. Risposte alle domande della CHECK_REQUEST

- **Q1.** Sì. L'identità è corretta ed è provata simbolicamente per φ generica (§2.1).
- **Q2.** Il contenuto di VAR-L1 e VAR-L2 è quasi certamente noto (Saut–Scheurer 1987; Isakov 1993 per le stime anisotrope). Non ho letto il testo: va a CIT-AUDIT-8. Lo stato giusto è **DIMOSTRATO (prova autosufficiente auditata), nessuna rivendicazione di novità**.
- **Q3.** Solo in parte. Nella classe u ∈ C^{1,2}, V è di fatto continuo fuori da un insieme discreto e la buca quadrata non è coperta. La lacuna L^∞ del VERDETTO F6 è chiusa dopo VAR-1(b), cioè con le soluzioni forti (SF); la derivazione è nel §2.1.
- **Q4.** Sì (§2.6).
- **Q5.** Sì, l'argomento è completo (§2.11).
- **Q6.** Sì nella sostanza, ma con la normalizzazione esplicita: in H = −∂² + x² la rottura è esattamente a cos t = 0, cioè alla parità (§2.10, VAR-6 e VAR-7).

## 6. Fonti (punti di attenzione)

- **Casas 2007:** verificato sul testo di arXiv:0711.2381: Thm 3.4, ∫‖A‖ < π, raggio ottimale, H di Hilbert, normalità di Y in dimensione infinita (VAR-5).
- **SLZ 2011:** titolo corretto (VAR-12); l'abstract è stato letto e il contenuto (VMPUM per segnali polinomiali e polinomiali-esponenziali) coincide con AUDIT-6.
- **Holmgren (Hörmander I, Thm 8.6.5):** non verificato. Non serve più, perché VAR-L1 copre V ∈ L^∞; resta solo come osservazione nel caso analitico.
- **Restano a CIT-AUDIT-8:** vdPS Prop. 1.34 / Thm 1.27, Pazy cap. 5, Folland cap. 4, Crum 1955, Saut–Scheurer 1987, Isakov 1993, Wei–Norman 1964.

## 7. Acceptance gate

| condizione | esito |
|---|---|
| (1) zero FATAL | sì |
| (1) zero CRITICAL sui claim | sì; l'unico CRITICAL (VAR-4) è una frase di confronto, già con riparazione |
| (2) ipotesi esplicite e scaricate | sì, dopo VAR-1, VAR-2, VAR-8 e VAR-11 |
| (3) dipendenze dei parametri dichiarate | sì |
| (4) red team eseguito su tutti i lemmi chiave | sì |

Gli stati della tabella §0 valgono con i fix indicati. "DIMOSTRATO dopo VAR-n" significa: la riparazione è scritta in questo audit e va riportata nel package prima che la riga del LEDGER salga.
