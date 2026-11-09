# AUDIT C3 — claim secondari: C3-P1, C3-T4, C3-T3, C3-T2(c)(d), C3-T5
Revisore: S-CHECK-2D (2ª tornata, parte D) · 25/10/2026

**Fonte e indipendenza.** Per questi claim S-C3 non ha mandato una CHECK_REQUEST. Da `work/C3/PROOF_PACKAGE.md` ho estratto solo tre cose:
- **§1–§2**: notazione, definizione di EP(Ω), modelli M1/M2. Servono per capire gli enunciati.
- **§5**: C3-T2, C3-T3, C3-P1, cioè enunciato, ipotesi e prova.
- **§6**: C3-T4 e C3-T5, cioè enunciato, ipotesi e prova.

Non ho usato §0, §7–§11, il titolo-stato dei claim, le "Conseguenze"/"Esempi" e i rimandi a script di S-C3 come prova, né la sua inbox. Uso come lemmi già DIMOSTRATI quelli di `AUDIT_C3-T1.md`: C3-L2, C3-L3 (a)–(e), Fatto (F), C3-T1, C3-T6.

**Skill caricate** (lettura dei SKILL.md, nessuno script _vendor eseguito):
- skills-local/session-protocol (per prima) e skills-local/claim-lifecycle;
- proof-checker. Il reviewer sono io. Ho seguito: Phase 0.5 (enunciati canonici, micro-claim), Phase 1 checklist A–H, Phase 1.5 red team, severità a due assi, acceptance gate. Niente Codex/LaTeX;
- scientific-critical-thinking, per separare ciò che è mostrato da ciò che è affermato;
- sympy.

**SymPy.** `work/CHECK/sympy/audit_c3_2d.py` → `audit_c3_2d.out`, eseguito con `.venv\Scripts\python.exe -I`.
- **ESITO GLOBALE: OK** (58 controlli, 0 FAIL).
- 2 righe INFO, che non sono test.
- 1 controllo [STRUTTURALE]: P1-d.

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| C3-P1 | **PASS-con-fix(P1-1 MAJOR, P1-2, P1-3)** | **DIMOSTRATO per il modello M2** (jet in un punto, Ω connesso qualsiasi), con la prova autosufficiente di P1-1(B). **Enunciato generale** (funzionali continui qualsiasi, Ω convesso): resta **CON-FONTE in attesa di verifica della citazione**. Finché la citazione non è verificata, non va usato come DIMOSTRATO |
| C3-T4 (a)(b) | **PASS-con-fix(T4-1)** | DIMOSTRATO |
| C3-T3 (i)(ii) | **PASS** (nota T3-2) | DIMOSTRATO |
| C3-T3 (iii) | **PASS-con-fix(T3-1 MAJOR, chiusa qui)**: la prova data era SymPy per d = 2,3,4 (V-ex) | DIMOSTRATO dopo il fix |
| C3-T2 (c)(d) | **PASS-con-fix(T2-1, T2-2, T2-3)** | DIMOSTRATO |
| C3-T5 (a)(b)(c) | **PASS-con-fix(T5-1, T5-2, T5-3)** | DIMOSTRATO |

Non ci sono FATAL né CRITICAL. I MAJOR sono due: P1-1, la dipendenza da una fonte non verificata, e T3-1, l'ottimalità mostrata solo su esempi. Il MAJOR T3-1 è chiuso qui. P1-1 è chiuso qui per M2 e resta aperto, in attesa della fonte, per l'enunciato generale. Gli altri rilievi sono MINOR.

## 1. Enunciati canonici (Phase 0.5)
Notazione: R = ℂ[τ,ξ]; Ω ⊂ ℝ² aperto connesso; EP(Ω) e Ann(·) come in AUDIT_C3-T1 §1; E_P := ker P ∩ EP(Ω).

**C3-P1.** Ipotesi: Ω convesso; P non costante; u ∈ C^∞(Ω) con P(∂)u = 0; ℓ_1,…,ℓ_N ∈ C^∞(Ω)′.
Tesi: esiste v ∈ E_P con ℓ_j(v) = ℓ_j(u) per ogni j. In particolare Ann(v) ⊋ (P).

**C3-T4.** Ipotesi: P = τ − a(ξ), u ∈ D′(Ω), P(∂)u = 0.
- (a) Ann(u) = (P) ⟺ u ∉ EP(Ω).
- (b) Ipotesi aggiuntive: u = Σ_k q_k e^{⟨z_k,·⟩} con z_k distinti e q_k ≠ 0, e n ≥ deg a. Poniamo D = Σ_k(deg_x q_k + 1). Allora
  {b ∈ ℂ[ξ]_{≤n} : τ − b ∈ Ann u} = a + ∏_k(ξ−ξ_k)^{δ_k+1}·ℂ[ξ]_{≤n−D}.

**C3-T3.** Ipotesi: 0 ≠ u ∈ EP(Ω), d = dim R·u, p_0 ∈ Ω.
- (i) Per ogni n ≥ 0: Ann(u)_{≤n} = {Q ∈ R_{≤n} : ∂^β(Q(∂)u)(p_0) = 0 per ogni |β| ≤ d−1}.
- (ii) Ann(u) = (Ann(u)_{≤d}).
- (iii) Per u = Σ_{j=1}^d e^{jx} e n = d, il jet di ordine 2d−2 non basta.

**C3-T2(c).** Ipotesi: modi semplici (q_k costanti non nulle); P ridotto; Z ⊂ V(P); n ≥ deg P; |Z ∩ V(P_i)| > n·deg P_i per ogni i.
Tesi: Ann(u)_{≤n} = P·R_{≤n−deg P}.

**C3-T2(d).** Per P = τ − ξ² e per ogni n ≥ 1 esistono Z ⊂ V(P) con |Z| = 2n e Q ∈ Ann(u)_{≤n} con P ∤ Q.

**C3-T5.**
- (a) Ipotesi: c ≠ 0 (va scritto c ∈ ℝ∖{0}, vedi T5-1); u = f(x−ct) + g(x+ct), con f ∈ D′(J_f) e g ∈ D′(J_g). Tesi: Ann(u) = (τ²−c²ξ²) ⟺ f ∉ EP(J_f) e g ∉ EP(J_g).
- (b) P = KG oppure telegrafo è irriducibile, quindi Ann(u) = (P) ⟺ u ∉ EP.
- (c) Per P = τ² + ξ⁴: Ann(u) = (P) ⟺ (∂_t ± i∂_x²)u ∉ EP, per entrambi i segni.

## 2. Dipendenze (DAG, nessun ciclo)
- **P1** dipende dalla densità di E_P in ker_{C^∞}P su Ω convesso, una fonte esterna (Malgrange/Hörmander), più Hahn–Banach in dimensione finita (banale). La variante M2 dipende invece da L3(a),(b), (F) e L2 (finitezza di V(f,g)).
- **T4** dipende da T1(a) e da T2(a), che a sua volta dipende da L3(a),(b),(c).
- **T3(i)** dipende dall'analiticità degli EP e dalla connessione di Ω.
- **T3(ii)** dipende dalla teoria delle basi di Gröbner con un ordine graduato.
- **T2(c)** dipende da T2(a) e dal teorema di Bézout (Fulton).
- **T5** dipende da T1(a), da L3(b) e dal criterio del determinante per le coniche.

Nessun riferimento in avanti.

## 3. Micro-claim ed esiti per passo

### C3-P1
| MC | passo | esito |
|---|---|---|
| P1.1 | Λ = (ℓ_j) ristretta a ker P è lineare e continua (ker P è chiuso in C^∞(Ω)) | OK |
| P1.2 | E_P denso in ker P ⇒ Λ(E_P) denso in Λ(ker P) | OK, data la densità |
| P1.3 | Λ(E_P) è un sottospazio di ℂ^N, quindi chiuso, e allora Λ(E_P) = Λ(ker P) | OK |
| P1.4 | **Densità** [Malgrange 1956, AIF 6; Hörmander ICASV Thm 7.6.14, "numerazione da ricontrollare"] | **LACUNA di fonte** → **P1-1** (MAJOR: UNJUSTIFIED + LOCAL finché la citazione non è verificata) |
| P1.5 | v ∈ E_P ⇒ Ann(v) ⊋ (P): (P) ⊆ Ann(v); V(Ann v) è finito (L3(e)) mentre V(P) è infinito (F), quindi Ann(v) ≠ (P). Il caso v = 0 dà Ann = R | OK (P1-2: va scritta la riga) |
| P1.6 | ruolo della convessità | OK: è necessaria per funzionali generali, non per M2 (red team) → **P1-3** |

### C3-T4
| MC | passo | esito |
|---|---|---|
| T4.a1 | τ − a(ξ) è irriducibile: grado 1 in τ, monico. Una fattorizzazione avrebbe un fattore in ℂ[ξ] che divide il coefficiente 1 | OK |
| T4.a2 | T1(a) con r = 1, e_1 = 1, P/P_1 = 1, w_1 = u | OK |
| T4.a3 | Ann = (P) e τ − b = P·A ⇒ A = 1 (confronto dei gradi in τ) ⇒ b = a | OK |
| T4.b1 | P ∈ Ann ⇒ P(z_k) = 0 (L3(c)) ⇒ τ_k = a(ξ_k); quindi z distinti ⟺ ξ distinti | OK |
| T4.b2 | τ − b = P + (a − b)(ξ) ⇒ [τ − b ∈ Ann ⟺ c(∂_x)u = 0], con c = a − b | OK |
| T4.b3 | c(ξ_k+∂_x)q_k = Σ_j c^{(j)}(ξ_k)∂_x^j q_k/j! (Taylor, c polinomio) | OK |
| T4.b4 | sistema triangolare: il coefficiente di x^{δ_k−j} coinvolge solo c^{(0..j)}(ξ_k), con pivot r_{δ_k}(t)·δ_k!/(δ_k−j)! ≢ 0, quindi c^{(j)}(ξ_k) = 0 per j ≤ δ_k. Il viceversa è immediato. q_k può dipendere da t: la prova lo prevede (r_l(t)) | OK (controllo: AD con q = x + 4t) |
| T4.b5 | molteplicità δ_k+1 nei ξ_k distinti ⟺ ∏(ξ−ξ_k)^{δ_k+1} divide c; deg c ≤ n ⟺ deg b ≤ n, **perché deg a ≤ n** | OK. L'ipotesi deg a ≤ n è essenziale: se deg a > n l'insieme può non essere vuoto anche quando D ≤ n non vale (per esempio un modo singolo dà b costante) → T4-1 |
| T4.b6 | identificato in 𝓔_n ⟺ D ≥ n+1; con modi semplici D = M | OK (controlli: calore D = 4 e AD D = 3, dimensione affine max(0, n+1−D) per n = 2…6) |

### C3-T3
| MC | passo | esito |
|---|---|---|
| T3.i1 | K_k ⊇ K_{k+1}; se K_k = K_{k+1}, allora K_k è ∂-stabile (W è stabile, e w ∈ K_{k+1} ⇒ ∂w ∈ K_k) | OK |
| T3.i2 | w ∈ K_k ∂-stabile ⇒ tutte le derivate in p_0 sono nulle ⇒ w = 0 (EP analitica, Ω connesso; anzi basta l'analiticità intera di EP su ℝ²) | OK |
| T3.i3 | dim K_0 = d − 1: la valutazione in p_0 non è nulla su W ∋ u ≠ 0. Le dimensioni decrescono strettamente fino a 0, quindi K_{d−1} = 0 | OK |
| T3.i4 | Q(∂)u ∈ W, quindi Q(∂)u = 0 ⟺ Q(∂)u ∈ K_{d−1}; ordine del jet n + d − 1 | OK (controllo: u = (1+t)e^{t−x}+x, d = 4, n = 1…4) |
| T3.ii1 | R/Ann ≅ W, quindi la dimensione è d; con un ordine graduato i monomi standard formano un ideale d'ordine di d elementi. Un monomio τ^aξ^b standard ha almeno (a+1)(b+1) ≥ a+b+1 divisori standard, quindi grado ≤ d−1 | OK (il conteggio dei divisori va scritto: T3-2) |
| T3.ii2 | un generatore minimale di in(Ann) è variabile·(standard), quindi ha grado ≤ d. Elemento della base di Gröbner ridotta: deg g = deg LM(g) (ordine graduato). La base genera Ann | OK (controlli: gradi [3,2,2] ≤ 4; Ann_{≤6} ⊆ (Ann_{≤4}); #standard = d; esempio 1D con grado d raggiunto) |
| T3.ii3 | (i) con n = d ⇒ basta il jet di ordine 2d−1 | OK |
| T3.iii | "SymPy S6b (d = 2,3,4)": è un controllo su esempi, non una prova per ogni d. Inoltre "non basta" è ambiguo: si può intendere che il test con meno righe ha nucleo più grande, oppure che il jet non determina Ann | **LACUNA** → **T3-1** (MAJOR: UNJUSTIFIED + LOCAL; chiusa qui) |

### C3-T2(c),(d)
| MC | passo | esito |
|---|---|---|
| T2.c1 | Q ∈ Ann_{≤n} ⇒ Q(z_k) = 0 (T2(a), q_k costante ≠ 0) | OK |
| T2.c2 | Q = 0 è banale. Q costante ≠ 0 è impossibile perché Z ≠ ∅. Quindi Q non è costante e Bézout si applica | OK; caso non scritto → T2-1 |
| T2.c3 | P_i ∤ Q ⇒ coprimi (P_i irriducibile) ⇒ |V(Q)∩V(P_i)| ≤ deg Q·deg P_i. Si usa Bézout proiettivo sulle omogeneizzate: una componente comune H ≠ Z₀ (perché Z₀ ∤ F*) si deomogeneizza in un fattore comune non costante. Questo passaggio è affermato, non scritto | OK; → T2-1 (una riga), T2-2 (riferimento) |
| T2.c4 | contraddizione con |Z∩V(P_i)| > n·deg P_i; P_i | Q per ogni i; P_i non associati, P ridotto, R UFD ⇒ P | Q; deg A ≤ n − deg P | OK |
| T2.c5 | viceversa: P ∈ Ann(u), perché P(z_k) = 0 per i modi semplici | OK |
| T2.d | Z_n = {(j², ±j)}_{j=1..n}, 2n punti distinti su V(P); Q_n = ∏(τ − j²) ∈ ℂ[τ] si annulla su Z_n, ha grado n e non è divisibile per τ − ξ² | OK (controlli n = 1…4). La portata va formulata con cura → T2-3 |

### C3-T5
| MC | passo | esito |
|---|---|---|
| T5.a1 | (∂_t + c∂_x)u = 2c g′(x+ct), (∂_t − c∂_x)u = −2c f′(x−ct) | OK (SymPy) |
| T5.a2 | Con P_1 = τ − cξ si ha w_1 = (P/P_1)u = (∂_t + c∂_x)u = 2c g′. La prova scrive "w_1 = −2cf′", con le etichette scambiate. L'equivalenza è simmetrica, quindi non è un errore | COSMETIC → T5-2 |
| T5.a3 | P_1, P_2 irriducibili e non associati ⟺ c ≠ 0; T1(a) con r = 2 | OK |
| T5.a4 | F(x−ct) ∈ EP(Ω) ⟺ F ∈ EP(J_F). (⇐) è chiaro. (⇒) "restrizione a una retta t = t_0" più la globalizzazione: la restrizione di una distribuzione a una retta non è definita a priori, e la fetta Ω ∩ {t = t_0} può essere sconnessa | LACUNA lieve → T5-3 (fornisco una prova di 3 righe) |
| T5.a5 | in una variabile, su un intervallo, f ∈ EP ⟺ f′ ∈ EP (primitive di EP sono EP; f′ = 0 ⇒ f costante) | OK |
| T5.a6 | f(x−ct) come distribuzione su Ω richiede c reale (pull-back per una sommersione reale) | ipotesi implicita → T5-1 |
| T5.b | determinante della matrice orlata: −μ² per KG, c²α²/4 per il telegrafo. Conica non degenere ⇒ irriducibile su ℂ; T1(a) con r = 1 | OK (SymPy, più la controprova α = 0) |
| T5.c | τ² + ξ⁴ = (τ − iξ²)(τ + iξ²): i fattori sono monici di grado 1 in τ, quindi irriducibili e non associati; T1(a) | OK |

## 4. Rilievi e fix (Phase 2, proposti; non applicati ai file di S-C3)

### P1-1 · REFERENCE_MISMATCH / UNJUSTIFIED · LOCAL · **MAJOR** · ADD_REFERENCE + ADD_DERIVATION (parziale)
**Il problema.** L'unico passo non elementare di P1 è la densità di E_P in ker_{C^∞(Ω)}P per Ω convesso, cioè il teorema di approssimazione con soluzioni esponenziali-polinomiali. Non posso verificare qui la citazione. Separo ciò che so da ciò che non so:
- (i) Il fatto è un teorema classico e lo ritengo vero. È dovuto a Malgrange, tesi "Existence et approximation des solutions des équations aux dérivées partielles et des équations de convolution", Ann. Inst. Fourier 6 (1955–56). Anche Ehrenpreis lo tratta, e lo si trova nei trattati di Hörmander.
- (ii) Non so confermare il numero "ICASV Thm 7.6.14". Non so confermare nemmeno quale enunciato della tesi di Malgrange sia quello giusto. Ricordo che una forma per un solo operatore compare anche in Hörmander, ALPDO I, nel capitolo sulla trasformata di Fourier–Laplace (§7.3). Non affermo nessun numero.

**Fix (A), ADD_REFERENCE.** Il CIT-AUDIT deve verificare l'enunciato esatto, la pagina e le ipotesi (Ω convesso; topologia C^∞ o D′; operatore scalare). Finché non lo fa, l'enunciato generale di P1 è "prova scritta modulo fonte non verificata", non CON-FONTE.

**Fix (B), ADD_DERIVATION: prova autosufficiente per il modello M2.** M2 è il caso che conta per [C3-D1].

*Lemma P1-M2.* Ipotesi: Ω ⊂ ℝ² aperto connesso (non serve la convessità), p_0 ∈ Ω, P non costante, K ≥ 0, u ∈ C^∞(Ω) con P(∂)u = 0. Tesi: esiste v ∈ E_P con ∂^αv(p_0) = ∂^αu(p_0) per ogni |α| ≤ K.

*Prova.* Sia J_K(w) = (∂^αw(p_0))_{|α|≤K} ∈ ℂ^{R_{≤K}}. Il duale di ℂ^{R_{≤K}} si identifica con R_{≤K} tramite ⟨Q, J_K w⟩ = (Q(∂)w)(p_0). In dimensione finita, J_K(ker P) ⊆ J_K(E_P) equivale a J_K(E_P)^⊥ ⊆ J_K(ker P)^⊥.

1. Sia Q ∈ R_{≤K} con (Q(∂)v)(p_0) = 0 per ogni v ∈ E_P. Siccome E_P è ∂-stabile, ∂^β(Q(∂)v)(p_0) = 0 per ogni β. Q(∂)v è un EP, quindi è intera su ℂ²; con serie di Taylor nulla è nulla. Quindi Q ∈ ∩_{v∈E_P} Ann(v).
2. **Claim: ∩_{v∈E_P} Ann(v) = (P).** L'inclusione ⊇ è ovvia. Per ⊆, sia Q ≠ 0 con P ∤ Q.
   - Esiste i con f := v_{P_i}(Q) < e_i. Scriviamo Q = P_i^f Q′ con P_i ∤ Q′.
   - V(P_i) è infinito (F). V(P_i) ∩ V(∂_τP_i, ∂_ξP_i) è finito: una derivata parziale di P_i non nulla ha grado minore, quindi è coprima con P_i, e si applica L2 (la finitezza di V(f,g) vale per f, g coprimi). Anche V(P_i) ∩ V(Q′) è finito.
   - Scegliamo quindi z ∈ V(P_i) con ∇P_i(z) ≠ 0 e Q′(z) ≠ 0, e η ∈ {e_1, e_2} con ∇P_i(z)·η ≠ 0. Poniamo s = ⟨η, y⟩, cioè s = t oppure s = x.
   - Su ℂ[s] un polinomio F(z+∂) agisce come F(z) + (∇F(z)·η)d/ds + (ordine ≥ 2).
   - Quindi P_i(z+∂) abbassa il grado esattamente di 1, con coefficiente direttore che si moltiplica per ∇P_i(z)·η ≠ 0, mentre Q′(z+∂) conserva il grado (Q′(z) ≠ 0).
   - Sia v := s^{e_i−1}e^{⟨z,·⟩}. P(z+∂)s^{e_i−1} = (∏_{j≠i}P_j^{e_j})(z+∂)·P_i^{e_i}(z+∂)s^{e_i−1} = 0, quindi v ∈ E_P (L3(a)).
   - Q(z+∂)s^{e_i−1} = Q′(z+∂)P_i^f(z+∂)s^{e_i−1} ha grado e_i−1−f ≥ 0, quindi è ≠ 0, e Q(∂)v ≠ 0 (L3(a),(b)).
3. Dunque Q = PA, e (Q(∂)u)(p_0) = (A(∂)P(∂)u)(p_0) = 0, cioè Q ∈ J_K(ker P)^⊥. ∎

*Sottoprodotto.* J_K(ker P) = J_K(E_P) = ((P)_{≤K})^⊥, di dimensione dim R_{≤K} − dim R_{≤K−deg P}.

*Controlli.* P1-a: nucleo del calore in (1,0), K = 3; v EP a 7 modi con lo stesso 3-jet, calcolato esplicitamente. P1-b: P = (τ−ξ²)², rango 14 = 15 − 1. P1-c: testimone x·e^{z}.

**Esito.** Con (B), "nessun jet finito in un punto certifica Ann(u) = (P)" è DIMOSTRATO su ogni Ω connesso. Il caso con più punti, integrali o campioni sparsi resta legato alla fonte (A).

### P1-2 · UNPROVEN_SUBCLAIM · COSMETIC · MINOR · ADD_DERIVATION
Va scritto "In particolare Ann(v) ⊋ (P)". Per v ∈ E_P si ha (P) ⊆ Ann(v). V(Ann v) è finito (L3(e)) e V(P) ⊇ V(P_1) è infinito (F), quindi Ann(v) ≠ (P). Se v = 0, Ann = R.

### P1-3 · SCOPE (non è un errore) · MINOR · nota da aggiungere
La convessità è **necessaria** per l'enunciato con funzionali generali. Controesempio, sul dominio a U di AUDIT_C3-T1 (L3-1):
- Ω = (0,3)_t×(0,1)_x ∪ (0,1)×(0,3) ∪ (2,3)×(0,3), connesso e non convesso; P = τ; u = φ(x)·1_{t>2}, con φ = 0 per x < 1 e φ = 1 per x > 2.
- u ∈ C^∞(Ω) e ∂_tu = 0.
- Prendiamo ℓ(w) = w(5/2, 5/2) − w(1/2, 5/2), continuo su C^∞(Ω). Allora ℓ(u) = 1.
- Sia v ∈ ker ∂_t con Ann(v) ⊋ (τ). Per T1(a) (r = 1) v ∈ EP(Ω), cioè v = E|_Ω con ∂_tE = 0 su Ω, quindi su ℝ² (L3(b)). Allora E = E(x) e ℓ(v) = 0.
- Dunque **un solo dato finito certifica Ann(u) = (τ)**: su domini non convessi la tesi di P1 è falsa.

Per M2 (un solo punto) invece la convessità non serve (P1-M2). Va aggiunto a P1 come osservazione: rende esplicito il ruolo dell'ipotesi. Controllo [STRUTTURALE] P1-d.

### T4-1 · HIDDEN_ASSUMPTION · COSMETIC · MINOR · STRENGTHEN_ASSUMPTION testuale
Nella parte (b):
- scrivere "z_k distinti, q_k ≠ 0" (la rappresentazione è unica per L3(b));
- ricordare che **deg a ≤ n è essenziale**. Se deg a > n l'insieme {b : deg b ≤ n, τ − b ∈ Ann} è a − ∏(ξ−ξ_k)^{δ_k+1}·{h : deg(a − ∏·h) ≤ n} e può non essere vuoto. Esempio: un modo singolo e^{a(ξ_0)t+ξ_0x} è annullato da τ − a(ξ_0).

La formula enunciata è corretta sotto l'ipotesi scritta.

### T3-1 · UNPROVEN_SUBCLAIM (verifica su esempi presentata come prova, O6) · LOCAL · **MAJOR** · ADD_DERIVATION (chiusa qui)
(iii) va enunciata e provata per ogni d ≥ 1, in due forme.
- **Forma debole** (il test con meno righe fallisce). Siano p_0 qualsiasi, m_k = Σ_j j^k e^{jx_0} e Q = Σ_i q_iξ^i ∈ ℂ[ξ]_{≤d}. Le condizioni ∂_x^k(Q(∂)u)(p_0) = 0 per k ≤ d−2 sono d−1 equazioni lineari in d+1 incognite (matrice di Hankel (m_{k+i})). Il nucleo ha quindi dimensione ≥ 2, mentre Ann(u) ∩ ℂ[ξ]_{≤d} = ℂ·∏(ξ−j) ha dimensione 1. Le derivate in t sono nulle per Q ∈ ℂ[ξ], quindi l'argomento vale anche in 2D con |β| ≤ d−2.
- **Forma forte** (il jet di ordine 2d−2 non determina Ann, nemmeno sapendo che dim R·u = d). Prendiamo Q′ = Q_0 + sQ_1 nel nucleo bidimensionale, con Q_0 = ∏(ξ−j), s piccolo e ≠ 0: ha grado d e radici distinte μ_1…μ_d, e Q′ ∉ ℂ·Q_0.
  - Si risolve la Vandermonde Σ_j w_jμ_j^k = m_k per k ≤ d−1, e si pone u′ = Σ_j w_je^{μ_j x}.
  - La successione m′_k = Σ w_jμ_j^k soddisfa la ricorrenza di Q′. Anche m la soddisfa per k = 0…d−2, perché Q′ sta nel nucleo. Siccome q′_d ≠ 0, m′_k = m_k per k ≤ 2d−2.
  - Quindi u′ ha lo stesso jet di ordine 2d−2 in p_0 e Q′ ∈ Ann(u′)∖Ann(u).
  - Controlli T3-6…T3-9 (d = 3, radice prescritta 0): Q′ = ξ(5ξ²−21ξ+19)/5; momenti uguali fino all'ordine 4, diversi all'ordine 5.

Annotazione onesta (INFO T3-1b): nell'esempio 2D u = (1+t)e^{t−x}+x, nel punto scelto, |β| ≤ d−2 bastava già. La soglia d−1 vale nel caso peggiore e non è sempre raggiunta, e (iii) va letta così.

### T3-2 · nota · MINOR
- In (i) basta un maggiorante d′ ≥ d, perché K_{d′−1} ⊆ K_{d−1} = 0. Conviene dirlo, perché in M2 d non è noto.
- In (ii) va scritto il conteggio "τ^aξ^b ha (a+1)(b+1) ≥ a+b+1 divisori, tutti standard". Non serve altro.

### T2-1 · CASE_INCOMPLETE · COSMETIC · MINOR · ADD_DERIVATION
- Caso Q costante: Q ≠ 0 costante non sta in Ann perché Z ≠ ∅; Q = 0 è banale.
- Una riga per "le omogeneizzate non hanno componenti comuni": un fattore comune H di F*, G* non è la retta all'infinito, perché Z₀ ∤ F*, e la sua deomogeneizzazione è un fattore comune non costante di Q e P_i.

### T2-2 · REFERENCE (da confermare) · COSMETIC · MINOR · ADD_REFERENCE
"Fulton cap. 5 §3": per quanto ricordo, in *Algebraic Curves* §5.3 è proprio "Bézout's Theorem". Va confermato sull'edizione citata. Serve la forma con la disuguaglianza Σ_P I(P, F∩G) = deg F·deg G, più I ≥ 1 sui punti comuni. In alternativa si può usare la sola stima affine |V(f,g)| ≤ deg f·deg g, che segue da quella.

### T2-3 · SCOPE · COSMETIC · MINOR · WEAKEN_CLAIM testuale
(d) mostra che la soglia **uniforme** "> n·deg P_i" non si può sostituire con "≥ n·deg P_i" in generale (esempio P = τ − ξ²). Non dice che la soglia sia necessaria per ogni configurazione. Esempio INFO T2-c3: con P = (τ−ξ²)(τ+ξ+1), n = 3, e soli 3 punti sulla retta, la conclusione vale ancora (3 punti allineati obbligano il fattore lineare). Suggerito: "(d) La soglia non è migliorabile in generale".

### T5-1 · HIDDEN_ASSUMPTION · COSMETIC · MINOR · STRENGTHEN_ASSUMPTION
Va scritto c ∈ ℝ∖{0}. Per c ∉ ℝ, f(x−ct) non è definita per f ∈ D′(J_f). In più conviene notare che la forma di d'Alembert è un'**ipotesi** su u. Su Ω convesso vale per tutte le soluzioni, ma non è provato qui e non serve.

### T5-2 · NORMALIZATION · COSMETIC · MINOR
Con P_1 = τ − cξ si ha w_1 = (∂_t + c∂_x)u = 2cg′(x+ct) e w_2 = −2cf′(x−ct). Vanno scambiate le etichette.

### T5-3 · UNPROVEN_SUBCLAIM · COSMETIC · MINOR · ADD_DERIVATION
Prova di (⇒) in "F(x−ct) ∈ EP(Ω) ⟹ F ∈ EP(J_F)" senza restrizioni a rette:
- Sia E una formula EP globale con E|_Ω = F∘π, π(t,x) = x−ct.
- (∂_t + c∂_x)(F∘π) = 0, quindi (∂_t + c∂_x)E = 0 su Ω, quindi su ℝ² (L3(b)). Allora E(t,x) = E(0, x−ct) =: F_0(x−ct), con F_0 ∈ EP(ℝ) in una variabile.
- (F − F_0)∘π = 0 su Ω, e il pull-back per la sommersione suriettiva π : Ω → J_F è iniettivo: in coordinate (s, r) = (x−ct, t) è F ↦ F⊗1 localmente. Quindi F = F_0 su J_F.

Controllo T5-a4.

## 5. Red team (Phase 1.5): esito
1. **P1, necessità della convessità.** Dominio a U (P1-3): con funzionali generali la tesi è falsa senza convessità. Non è un controesempio a P1, che assume Ω convesso: l'ipotesi è necessaria ed è presente.
2. **P1-M2.** Nucleo del calore (non EP, identificante) e soluzione EP a 7 modi con lo stesso 3-jet, calcolata esattamente. P non ridotto: (τ−ξ²)² con soluzioni t·e^z e x·e^z.
3. **T4.** Modi con q_k dipendente da t (x² + 2t; x + 4t). La formula di Hermite vale per n = 2…6.
4. **T3.** (ii) controllato con la base di Gröbner grevlex (gradi ≤ d, monomi standard = d, nessun generatore oltre d). (iii) forma forte con un esplicito u′.
5. **T2(c).** Due fattori, punti oltre soglia: Ann_{≤3} = ℂ·P. Bézout raggiunto (6 = 3·2). (d) per n = 1…4.
6. **T5.** Testimone per g ∈ EP: Q = (ξ−1)(τ+cξ) ∈ Ann∖(P). Le coniche degenerano esattamente per α = 0 (onda). Trave: e^{it+x} ∈ ker P è EP, quindi non identifica.

Nessun controesempio agli enunciati come scritti.

## 6. Portata (scientific-critical-thinking)
- **Mostrato:** le impossibilità e le soglie dei dati finiti.
  - Un jet finito in un punto non certifica mai l'identificazione nell'anello intero (P1-M2, ogni Ω connesso).
  - Sui dati EP la soglia di Bézout è sufficiente e uniformemente ottimale.
  - Il jet di ordine 2d−1 basta per u EP con dim R·u = d, e 2d−2 non basta nel caso peggiore.
  - Per le evoluzioni, identificazione ⟺ u ∉ EP; nella classe 𝓔_n ⟺ D ≥ n+1.
  - Onda, KG, telegrafo e trave sono istanze dirette di C3-T1.
- **Non mostrato qui:** P1 per funzionali qualsiasi su Ω convesso, che dipende da una fonte non verificata (P1-1(A)). Per domini non convessi P1 nella forma generale è **falso** (P1-3). In LEDGER va quindi scritto "nessun jet finito (M2) certifica Ann = (P): DIMOSTRATO; dati finiti generali su Ω convesso: CON-FONTE da verificare".

## 7. Acceptance gate
- 0 FATAL e 0 CRITICAL ✔.
- MAJOR: T3-1 chiuso qui. P1-1 chiuso per M2; per l'enunciato generale lo stato proposto è declassato a "CON-FONTE da verificare", quindi nessuna promozione indebita ✔.
- Ipotesi esplicite dopo T4-1 e T5-1 ✔.
- Le applicazioni di T1(a), L3, (F), L2, Bézout e Gröbner hanno le ipotesi scaricate ✔.
- Controesempi tentati su ogni claim ✔. Nessuna O(·) ✔.
