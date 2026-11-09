# AUDIT S4-TERM — E_int non lineare nel senso A9 (Burgers, KdV–Burgers, Fisher–KPP)
Revisore: S-CHECK-11 (11ª tornata) · 26/10/2026
Fonte esaminata: `work/S4-TERM/CHECK_REQUEST.md` (per intero). **Riferimenti puntuali dichiarati a `work/S4-TERM/PROOF_PACKAGE.md`:** §1 (tabella e riga 26 "Esito"), §6 Oss. 7.6 (r. 152–154), §7 S4T-T4 e S4T-P6 (r. 157–175: non copiati nella CHECK_REQUEST, richiesti dal coordinatore), §9 r. 188 (LIN-Q3), §11 (S4T-Q1..Q5), §12 (righe LEDGER), §13 (kill-argument v1, eccezione del coordinatore). Nient'altro di work/S4-TERM letto (né PLAN, né gli script s1–s5: il red team è indipendente).
Fatti importati usati come dati: P1-T5 (DIMOSTRATO, LEDGER; enunciato in CHECK_REQUEST §C, confrontato parola per parola con l'uso in S4T-C1(e)), P1-P1(a) (DIMOSTRATO; solo Oss. 7.6). Fatti esterni [F1]–[F3]: vedi §4.
Skill caricate (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-checker (il revisore sono io: enunciati canonici, micro-claim, checklist A–H, red team, severità a due assi, acceptance gate; niente Codex/LaTeX), kill-argument (revisori = due subagenti Claude freschi senza contesto; verdetto calcolato da me con la tabella della skill), sympy.
SymPy/numpy: `work/CHECK/sympy/audit_s4term.py` → `audit_s4term.out` (esito in §5).

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| Lemma J (i),(ii) + applicazione | **PASS-con-fix(J-1)** | DIMOSTRATO |
| **S4T-T1** (i)–(v) | **PASS** (serie intera, t², omogeneità ν^aε^{b+1}, scala, KdVB, Fisher riverificati in modo indipendente via Hopf–Cole fino a t⁴) | DIMOSTRATO |
| S4T-L0 | **PASS** | DIMOSTRATO |
| S4T-L1 | **PASS-con-fix(L1-1)** | DIMOSTRATO (mod [F2]-regolarità, §4) |
| **S4T-T2** (forme chiuse, stima grezza) | **PASS** | DIMOSTRATO |
| **S4T-T2 Passo 7** (resto ν²ε²t³) | **PASS-con-fix(T2-1 MINOR, T2-2 MINOR)** — equazione di ŵ esatta (verificata simbolicamente); (1) va scritto con Taylor misto in (s,λ) e il regime εT max(−w₀′) ≤ θ va usato per K₁ = O(ε) | DIMOSTRATO |
| S4T-P3 | **PASS** (costanti M₂, M₃ e limite verificati; numerica sin x entro 1%) | DIMOSTRATO |
| S4T-L2 (a)–(d) | **PASS** | DIMOSTRATO (identificazione con S_B: CON-FONTE [F1]) |
| **S4T-T3** (i),(ii),(v),(vi),(vii) | **PASS-con-fix(T3-1 MAJOR di cornice, T3-2, T3-3)** | DIMOSTRATO mod [F1] (CON-FONTE); (iii)/(v) anche mod [F2] (vedi §4: [F2] è in realtà dimostrabile qui, fix F2-1) |
| **S4T-T3 (iii)** (liminf ‖·‖_∞ ≥ D/2; liminf ν^{-1/2}‖E^mult_AB‖_{L¹} ≥ 2D√(t/π)) | **PASS** — (U⁺) con costante 4e^{1/4}t√Mν^{3/2}/d² corretta, ν ≤ M usato correttamente, limite del calore e Fatou corretti, costante esatta | DIMOSTRATO mod [F1], [F2] |
| S4T-T3 (iv) | **PASS** come enunciato CONDIZIONALE | CONDIZIONALE [F3] (Kuznetsov 1976, CON-FONTE da verificare) |
| **S4T-Q1** (ordine L¹ di E^add oltre lo shock; punto P4 del kill-argument v1) | correttamente registrato **APERTO**; nessun enunciato numerato lo assume (§2.6) | APERTO |
| S4T-T4 (i) | **PASS** | DIMOSTRATO |
| S4T-T4 (ii) | **PASS** | CONDIZIONALE [H-KB] (buona posizione classica di KdV–Burgers su 𝕋: CON-FONTE da verificare) |
| S4T-T4 (iii) | formula di δ_d **verificata** (equazione lagrangiana esatta); resto mancante | candidato (V-ex) — APERTO S4T-Q2 |
| S4T-P5 (i)–(iii) | **PASS-con-fix(P5-1)** | DIMOSTRATO |
| S4T-P6 | **PASS** (formula esatta all'ordine ε², confronto indipendente con Hopf–Cole fino a t⁴) | DIMOSTRATO (formale in ε, come dichiarato) |
| **S4T-C1** (a)–(e) | **PASS-con-fix(C1-1, C1-2)** | DIMOSTRATO (e): via P1-T5; la "Lettura" richiede il fix C1-1 |
| Oss. 7.6 | interpretazione con argomento breve corretto | osservazione (nessuno stato) |
| Kill-argument su S4T-T3 corretto | **WARN** (reason_code unresolved_major_or_minor): 0 / 5 / 1 (P2 major, cornice dell'Esito) | → fix T3-1 obbligatorio |

Rilievi: nessun FATAL, nessun CRITICAL. 1 MAJOR (T3-1: cornice "teorema negativo"/"PR3 ✔ in L∞" nell'Esito e nel titolo, confermato dal kill-argument); il resto MINOR. Nessun enunciato numerato è risultato falso.

## 1. Enunciati canonici (Phase 0.5)
- **S4T-T1.** ∀N, ∀T_1..T_N ∈ 𝒫, ∀Ω, ∀u ∈ C^∞(Ω) soluzione di u_t = ΣT_n(u), ∀t₀: in C^∞(J)[[s]], [s^k/k!]Ê^add = Σ_{w∈[N]^k non costante} D_w u₀ (valutato in u₀ = u(t₀,·)); per Burgers [s^k]Ê^• = Σ_{a+b=k, a,b≥1} ν^a c_{a,b}[u₀], c_{a,b} omogeneo di grado b+1, peso 2a+b. (Getto formale: nessuna convergenza affermata.)
- **S4T-T2.** ∀u₀ ∈ C^∞(𝕋) reale non costante, ∀T < t*, ∀ν > 0, ∀t ∈ [0,T], ∀a: E^•(t,X(t,a)) = ν·(forma chiusa) + R^•, ‖R^•(t)‖_∞ ≤ ν²C_•(t) (costanti esplicite in t, K₁..K₄, indipendenti da ν); raffinamento: ∀θ < 1, ∀w₀, ∀T: ∃C(θ,w₀,T) tale che ∀ε con εT max(−w₀′) ≤ θ, ∀ν > 0, ∀t ≤ T: ‖R^•(t)‖ ≤ Cν²ε²t³. (La C del raffinamento non è esplicita: Nota d'onestà.)
- **S4T-T3(iii).** ∀u₀ ∈ C^∞(𝕋) reale non costante, ∀t > t*, ∀ salto x₀ di S_B(t)u₀ con ampiezza D: liminf_{ν→0}‖E^mult_AB(t)‖_∞ ≥ D/2 e liminf_{ν→0} ν^{-1/2}‖E^mult_AB(t)‖_{L¹(𝕋)} ≥ 2D√(t/π) (t fisso; limite in ν solo).
- **S4T-T3(vi).** ∀ν > 0, ∀t: |‖E^add(t)‖_{L¹} − ‖S(t)u₀ − S_B(t)u₀‖_{L¹}| ≤ 2πνt‖u₀″‖_∞. (Nessuna affermazione sul tasso.)

## 2. Micro-claim ed esiti per passo

### 2.1 Lemma J e S4T-T1 (priorità 1)
| MC | passo | esito |
|---|---|---|
| J.1 | (i) regola della catena ∂_tG[w] = (D_PG)[w] (G polinomio differenziale, w liscia) | OK |
| J.2 | (ii) ∂_s^j∂_τ^iΨ(0,0) = (D_{P2}^iD_{P1}^ju₀)[w₀]; ordine: il flusso applicato **prima** nel tempo (P₂) sta a **sinistra** (ordine di Gröbner) | OK — verificato in modo indipendente: getto di S_A(t)S_B(t)u₀ calcolato componendo serie (caratteristiche, poi calore) = e^{tD_B}e^{tD_A}u₀ fino a t³ (audit_s4term) |
| J.3 | applicazione su 𝕋, T < t*: liscezza congiunta di (s,τ) ↦ S_A(s)S_B(τ)u₀, S_B(s)S_A(τ)u₀ (L1(c)); E^• liscia in t ⇒ serie di Taylor = serie formale | OK; **J-1 (MINOR, REGULARITY_GAP):** Lemma J(i) per u = S(t)u₀ richiede u ∈ C^∞([0,T)×𝕋) **fino a t = 0**; S4T-L1 dà stime uniformi ma la liscezza in t = 0 (compatibilità banale sul toro) va detta in una riga (il calore e il trasporto la danno esplicitamente; per u: regolarità parabolica con dato liscio, oppure Hopf–Cole con φ₀ = e^{−U₀/2ν} liscia) |
| T1.1 | (ΣD_n)^k = Σ_w D_w in End(𝒫); parole costanti = getti di Ŝ_n | OK |
| T1.2 | [s²] = ½Σ_{m≠n}D_mD_nu₀ = ½Σ_{m≠n}T_n′[T_m] | OK (identità; SymPy) |
| T1.3 | Burgers: A′B + B′A = −ν(4u₀′u₀″+2u₀u₀‴) ⇒ −ν(2u₀′u₀″+u₀u₀‴); B′A − A′B = 2νu₀′u₀″ ⇒ [s²]Ê^mult_AB = νu₀′u₀″, [s²]Ê^mult_BA = −νu₀′u₀″ | OK (a mano e SymPy; anche per composizione esplicita dei flussi) |
| T1.4 | **serie completa**: coefficienti di t², t³, t⁴ di E^add dalle parole miste = quelli del calcolo indipendente u (Hopf–Cole) − calore − caratteristiche + u₀, dato ε(sin x + ½cos 2x), ε, ν simbolici | OK (k = 2,3,4) |
| T1.5 | omogeneità: D_A conserva il grado, +2 di peso, ×ν; D_B +1 grado, +1 peso ⇒ parola (a,b): ν^a, grado b+1, peso 2a+b, a,b ≥ 1 | OK (argomento corretto; verificato su tutti i monomi fino a k = 4) |
| T1.6 | ⇒ ogni coefficiente O(νε²), nessun termine ε¹; per E^mult: nessun termine ν⁰ né ε¹ | OK (SymPy k ≤ 4) |
| T1.7 | scala w(τ,x) = ε^{-1}u(τ/ε,x) risolve w_τ = (ν/ε)w_xx − ww_x; idem i flussi dei termini ⇒ E(t;ε,ν)[w₀] = εẼ(εt;ν/ε)[w₀] | OK (a mano; coerente: nel getto il coefficiente di t^k ha grado totale k+1 in (ε,ν), SymPy) |
| T1.8 | esempio sin: 3/2 νε² sin 2x | OK |
| T1.9 | (iv) KdV–Burgers: formula di [s²]; −νdu₀^{(5)} = interazione calore × Airy (O(ε)), sparisce raggruppando L = A+C | OK (SymPy; la seconda affermazione è immediata: [D_A,D_C] = 0 e il termine viene da D_AD_C + D_CD_A = 2D_AD_C) |
| T1.10 | (v) Fisher: rν(u₀″−u₀′²−2u₀u₀″), [s²]Ê^mult_AR = rνu₀′² | OK (a mano e SymPy) |
Esito: **S4T-T1 PASS**. L'affermazione del coordinatore (coefficiente t² verificato a mano) è confermata, e il resto della serie (t³, t⁴) coincide con un calcolo indipendente.

### 2.2 S4T-L0, S4T-L1
| MC | passo | esito |
|---|---|---|
| L0.1 | (a) z = g + θe^{(K+1)t}: Lz ≥ θe^{(K+1)t} > 0; t₁ > 0 per continuità e compattezza; z_t(t₁,x₁) ≤ 0 (derivata sinistra, t₁ ∈ (0,T]), z_x = 0, z_xx ≥ 0 | OK. **Domanda 4:** con ν = 0 non serve g_xx; le ipotesi (g ∈ C([0,T]×𝕋), g_t, g_x continue su (0,T]×𝕋) sono sufficienti |
| L0.2 | (b) Y = e^{Kt}(‖g(0)‖+∫F), Y′ ≥ KY + F, L(Y ∓ g) ≥ (K+c)Y ≥ 0 | OK |
| L1.1 | (o) X diffeomorfismo, J ≥ 1 − T/t*, soluzione classica ⇒ entropica | OK |
| L1.2 | (a) p_t + wp_x + p² − νp_xx = 0; M₀ − p ≥ 0; ϑ′ = −ϑ², ϑ(0) = m₀; c = p+ϑ limitata | OK |
| L1.3 | (b) Leibniz: coefficiente di p₁p_j = j+1 (i = 1 e i = j), K = (j+1)K₁, induzione; Y_j indipendenti da ν | OK (**domanda 5**: sì, Y_j dipendono solo da K₁, ‖u₀^{(i)}‖, i ≤ j) |
| L1.4 | (c) calore: contrazione, commuta con ∂_x, min ∂_xh ≥ m₀ ⇒ t*(h(τ)) ≥ t*; le stime (a),(b) dipendono solo da queste quantità | OK |
| L1.5 | u = S(t)u₀ classica su [0,T]×𝕋 (usata in (a) per applicare L0) | **L1-1 (MINOR):** dipende da [F2] o dalla teoria parabolica classica (esistenza globale della soluzione liscia di Burgers viscoso sul toro); dichiararlo nelle ipotesi (vedi §4, F2-1: si chiude con Hopf–Cole) |

### 2.3 S4T-T2 (priorità 2)
| MC | passo | esito |
|---|---|---|
| T2.1 | Passo 1: uu_x − vv_x = ue_x + v_xe; L0(b) con ν = 0, c = v_x, F = νK₂ ⇒ ‖e‖ ≤ νK₂te^{K₁t} | OK |
| T2.2 | Passo 2: (e_x)_t + u(e_x)_x + (u_x+v_x)e_x = νu_xxx − v_xxe; K = 2K₁ | OK |
| T2.3 | Passo 3: coefficienti 2u_x+v_x, u_xx+2v_xx, v_xxx; K = 3K₁ | OK (derivazione rifatta a mano) |
| T2.4 | Passo 4: J_t = v_xJ, d/dt(δJ) = Jv_xx, v_xx(t,X) = u₀″/J³, ∫₀^t(1+su₀′)^{-2}ds = t/J ⇒ δ = tu₀″/J² | OK (a mano; SymPy: δ risolve l'equazione come serie, v_xx = u₀″/J³) |
| T2.5 | Passo 5: e_t + (ve)_x + ee_x = νu_xx ⇒ w_t + (vw)_x = νe_xx − ee_x; ‖w‖ ≤ ν²ρ | OK |
| T2.6 | Passo 6: Taylor con resto integrale in C(𝕋), h″ = ν²∂⁴h | OK |
| T2.7 | conclusioni: δ − tu₀″ → ν t[u₀″(a)/J² − u₀″(X)]; δ − tv_xx = t²u₀′u₀″/J³; E^mult_BA: ẽ, ζ = u₀″/J, w̃, δ − tζ = −t²u₀′u₀″/J²; costanti ρ̃ (t·t² = t³) | OK (tutte le identità rifatte a mano) |
| T2.8 | **controllo forte**: il coefficiente di ν¹ dei getti veri (Hopf–Cole, calcolo indipendente) di E^add, E^mult_AB, E^mult_BA coincide con lo sviluppo in t delle tre forme chiuse a **tutti gli ordini fino a t⁵** e a tutti gli ordini in ε | OK (SymPy, dato ε(sin x + ½cos 2x)) |
| T2.9 | Passo 7: equazione ŵ_t + (vŵ)_x − νŵ_xx = ν²∂²(δ − tu₀″) − (vr_h)_x − ee_x, ŵ(0) = 0 | OK — **domanda 3:** l'equazione è corretta (verificata come identità simbolica esatta con u, h, v, δ generiche sostituendo le quattro equazioni) |
| T2.10 | Passo 7 (2),(3): stime O(ν²s²) con prodotti di due norme | OK; **T2-2 (MINOR, CONSTANT_DEPENDENCE_HIDDEN):** "quadratica" significa "prodotto di due quantità O(ε)" e usa K₁ = O(ε), che vale **solo** nel regime εT max(−w₀′) ≤ θ (K₁ ≥ 1/(t*−T) ≤ ε max(−w₀′)/(1−θ)) e con e^{cK₁T} limitato da una costante di θ e w₀. Va scritto: le Q_• sono funzioni di (‖w₀^{(j)}‖)_{j≤5}, θ, T moltiplicate per ε²; nessuna uniformità in T affermata |
| T2.11 | Passo 7 (1): ‖∂_x²(δ(s) − su₀″)‖ ≤ s²Q₁ con Q₁ = O(ε²) | **T2-1 (MINOR, LOGICAL_GAP di stesura):** "valor medio applicato due volte" non basta così scritto: due applicazioni separate danno O(s²) **oppure** O(λ²), non il prodotto. L'argomento corretto è Taylor misto: g(s,λ) := ∂_x²(δ_λ(s) − sλu₀″) con g(0,λ) = g_s(0,λ) = 0 e g(s,0) = g_λ(s,0) = 0 per ogni s, λ ⇒ |g(s,1)| ≤ (s²/4)·sup_{σ≤s, μ≤1}|∂_s²∂_λ²g(σ,μ)|, e il sup è finito perché J_λ ≥ 1 − θ per λ ∈ [0,1] (liscezza congiunta in (s,λ,x) delle formule lagrangiane); con u₀ = εw₀, ∂_λ² porta ε². SymPy: g = O(s²) e O(λ²) (getto s ≤ 4). Fix: sostituire la frase con questo argomento (ADD_DERIVATION) |
| T2.12 | Passo 7 per E^mult_AB, E^mult_BA: R^AB = ŵ − (S_A−I−νt∂²)(v(t)−u₀), R^BA = ŵ − ŵ̃, equazione di ŵ̃ | OK (rifatto a mano; SymPy: la parte ν² dei getti veri di R^add, R^AB, R^BA parte da t³ e non ha termine ε¹, fino a t⁵) |
**Domanda 3 (Passo 7(1)):** il punto va reso esplicito (T2-1), ma l'enunciato è vero. **Esito T2: PASS** (stima grezza) e **PASS-con-fix(T2-1, T2-2)** (raffinamento).

### 2.4 S4T-P3
| MC | passo | esito |
|---|---|---|
| P3.1 | M_p in z² = 1/(2p−1): M₂ = 3√3/16, M₃ = 25√5/216 | OK (SymPy) |
| P3.2 | J = η + (tκ/2)y²(1+O(y)) (perché 1+tm₀ = η), u₀″ = κy(1+O(y)) | OK |
| P3.3 | regione I: riscalamento, errore (1+δ)^{-p} uniforme in z, il massimo z = (2p−1)^{-1/2} è dentro; limite √(2κ/t*)M_p | OK |
| P3.4 | regione II: η^{p−1/2}·Cη^{(1−2p)/4} = Cη^{(2p−1)/4} → 0; regione III limitata | OK |
| P3.5 | prefattori t → t*, t²|u₀′| → t* vicino ad a* (|u₀′−m₀| = O(η^{1/2}) in regione I); termine tu₀″(X) limitato: |sup|f−g| − sup|f|| ≤ sup|g| | OK |
| P3.6 | numerica u₀ = sin x (κ = 1, t* = 1), η = 10⁻⁴: rapporti con i limiti previsti | OK (§5) |
**PASS.** L'"Interpretazione (non dimostrata)" (scala di Pearcey, ν|log ν|) è etichettata correttamente.

### 2.5 S4T-L2 e S4T-T3 (priorità 3)
| MC | passo | esito |
|---|---|---|
| L2.1 | (a) coercività (|U₀(y)| ≤ ‖u₀‖|y|), Φ′ = 0, Φ″ ≥ 0, |x−a| ≤ t‖u₀‖ | OK |
| L2.2 | (b) monotonia (scambio) | OK |
| L2.3 | (c) limiti laterali per ogni selezione (monotonia + compattezza + continuità congiunta) | OK |
| L2.4 | (d) **domanda 2:** componenti di N_t limitate (N_t ≠ ℝ perché ∫u₀′ = 0, periodicità ⇒ lunghezza < 2π): OK; immagine dei minimizzanti evita N_t (Φ″ ≥ 0 ai minimi): OK; x₀ finito (|x − a^±| ≤ t‖u₀‖); per x > x₀: a^−(x) ≥ a^+(x″) ≥ β con x″ ∈ (x₀,x) (monotonia (b)); per x < x₀: a^+(x) < β e a^+(x) ∉ (α,β) ⇒ ≤ α; (c) ⇒ a^+(x₀) ≥ β, a^−(x₀) ≤ α | OK |
| L2.5 | v(t,x₀^−) − v(t,x₀^+) = (a^+−a^−)/t = D ≥ |I|/t; i limiti laterali sono limiti su tutti gli x, quindi limiti essenziali del rappresentante q.o. ⇒ nessun rappresentante continuo | OK (numerica sin x, t = 2: D = 1.8955 ≥ |I|/t = 1.0472) |
| T3.1 | (i) E^add = [u − h + u₀] − v: salto +D; ‖·‖_∞ ≥ D/2; seminorma di Gagliardo ∫₀^r∫₀^r(ξ+η)^{-2} = +∞ ⇒ ∉ H^{1/2} (e ∉ H^s, s ≥ 1/2) | OK. Usa: u(t) continua (classica), [F1] (identificazione di v con S_B) |
| T3.2 | (ii) ‖h_x − u₀′‖ ≤ νt‖u₀‴‖ < δ/t ⇒ 1 + th_x < 0 su N_t^δ; L2(d) per il dato liscio h(t) al tempo t | OK |
| T3.3 | (iii) (U⁺): Φ_x(y) − Φ_x(a^+) = [Φ_{x₀}(y) − Φ_{x₀}(a^+)] + d(a^+−y)/t (calcolo diretto, rifatto); per y > a^+: ≤ Mz²/2; numeratore ≤ (2νt/d)²; denominatore ≥ √(ν/M)e^{−1/4} **per ν ≤ M** | OK — **domanda 1:** la condizione ν ≤ M serve perché ∫₀^{√(M/ν)}e^{−w²/4}dw ≥ ∫₀¹e^{−w²/4}dw ≥ e^{−1/4}; è usata correttamente perché il risultato è un limite ν → 0 (per ν ≤ M = 1/t + ‖u₀′‖ la stima vale; il limite inferiore non ne è toccato). Costante: (2νt/d)²e^{1/4}√(M/ν)/t = 4e^{1/4}t√Mν^{3/2}/d² ✔ |
| T3.4 | (U⁻) simmetrica (a^− minimizza Φ_{x₀}; per y > a^−: Φ_x(y) − Φ_x(a^−) ≥ d(y−a^−)/t con x = x₀−d) | OK |
| T3.5 | calore: H(x₀+λ√(νt)) → v₊ + DΦ_N(−λ/√2) (convergenza dominata, |v| ≤ ‖u₀‖, limiti laterali di L2(c)); a sinistra → v₋ − DΦ_N(−λ/√2) | OK |
| T3.6 | con d = λ√(νt): u ≤ v₊ + λ√(ν/t) + 4e^{1/4}√M√ν/λ² ⇒ E ≤ −DΦ_N(−λ/√2) + o(1) (per λ > 0 fisso); λ ↓ 0 ⇒ liminf‖E‖_∞ ≥ sup_λ DΦ_N(−λ/√2) = D/2 | OK |
| T3.7 | L¹: cambio di variabile, Fatou (integrando ≥ 0, liminf puntuale per ogni λ > 0), Λ → ∞, ∫₀^∞Φ_N(−s)ds = 𝔼Z₊ = 1/√(2π) ⇒ √t·D·√2/√(2π) = D√(t/π) per lato; due lati ⇒ 2D√(t/π); salti distinti con finestre disgiunte | OK (SymPy per l'integrale; numerica §5) |
| T3.8 | (iv) ‖G_σ*f − f‖_{L¹} ≤ σ√(2/π)TV(f), σ = √(2νt) ⇒ 2√(νt/π)TV; v(t) ∈ BV (= x/t − a(x)/t, a monotona) | OK; Θ(√ν) **CONDIZIONALE [F3]**, etichettato correttamente |
| T3.9 | (v) argmin unico per tutti gli x tranne un insieme numerabile (intervalli [a^−,a^+] con interni disgiunti); concentrazione di Laplace (inf_{|y−a|≥r}(Φ_x−Φ_x(a)) > 0, code gaussiane, massa locale ≳ √ν); convergenza dominata | OK (usa [F2] per la formula di u) |
| T3.10 | (vi) E^add − (u − v) = −(h − u₀), ‖h−u₀‖_{L¹} ≤ 2π‖h−u₀‖_∞ ≤ 2πνt‖u₀″‖ | OK |
| T3.11 | (vii) S_B commuta con u ↦ εu(ε·,·) (Lax–Oleinik: Φ scala); D = εD̂(εt), D̂(τ) ≥ |Î(τ)|/τ | OK come enunciato di scala. **T3-3 (MINOR, SCOPE):** il confronto "la legge del getto predice |E^add| ∼ ντ²", violazione di ordine ε/ν, confronta con una legge che (i) dichiara già inapplicabile oltre t*; riformulare come enunciato di scala (salto ∝ ε, indipendente da ν; prima dello shock lo sviluppo è in ν/ε) — rilievo P6 del kill-argument |
| T3.12 | cornice: titolo "Teorema negativo oltre lo shock", Lettura ("non ha risposta positiva"), Esito ("scatta il ramo teorema negativo", "PR3 ✔ in L∞") | **T3-1 (MAJOR, OVERSTATED + GLOBAL sul criterio d'uscita, SCOPE_OVERCLAIM):** gli enunciati numerati sono veri, ma (i),(ii) sono conseguenze della definizione A9 (lo dice l'Esito (a)), e l'unica affermazione negativa non definitoria, (iii), riguarda la composizione E^mult_AB, non l'errore additivo. La quantità che isola l'interazione additiva in L¹ è aperta (Q1) e la numerica (≈10ν) va nel verso **positivo**. Fix (WEAKEN_CLAIM sulla cornice): titolo "Oltre lo shock: ostruzione nelle norme che vedono i salti (forzata da A9) e ordine √ν dello splitting AB in L¹"; Esito come esito diviso: (a) L∞/H^s: negativo per definizione di A9; (b) L¹: negativo (ordine ≤ 1/2) solo per E^mult_AB; (c) L¹ per E^add: APERTO, numericamente O(ν). Ritirare "PR3 ✔ in L∞" come evidenza (al più "PR3 vale in L∞ per costruzione") |
| T3.13 | T3-2 (MINOR): la Lettura di T3 dice "Θ(√ν) in L¹ … (dimostrato; Θ(√ν) solo CONDIZIONALE …)": la parentesi "dimostrato" va riferita esplicitamente al solo limite inferiore; e "il flusso vero lo tiene su ν/D" è un'affermazione non dimostrata (va marcata "euristica") | fix di testo |

### 2.6 Punto critico P4 del kill-argument v1 = S4T-Q1 (verifica di registrazione)
Domanda del coordinatore: l'ordine L¹ di E^add oltre lo shock è registrato APERTO e nessun enunciato lo assume?
- Registrazione: §1 Esito (c) "in L¹ la domanda per E^add resta aperta"; T3(v) prova solo lim = 0; T3(vi) è un'equivalenza esatta ("se e solo se"), non un'affermazione di tasso, e dice "**non dimostrato qui** (S4T-Q1)"; §11 S4T-Q1 APERTO con congettura Θ(ν) esplicitamente marcata come tale (4ν ln 2 per shock: F4LIN-T2 riguarda E^trop, dichiarato); §12 riga LEDGER di T3 riporta solo "(vi) ‖E^add‖_{L¹} = O(ν) ⟺ tasso di viscosità evanescente O(ν)"; riga "S4T-Q1..Q5 APERTO". ✔
- Uso: ho cercato in tutti gli enunciati numerati (T1–T4, P3, P5, P6, C1, L0–L2) e nelle Letture un uso di "‖E^add‖_{L¹} = O(ν)" oltre lo shock: **nessuno**. Le uniche frasi d'ordine in L¹ riguardano E^mult_AB (√ν, limite inferiore dimostrato, Θ condizionale) e la numerica (≈10ν, marcata "osservato, non dimostrato"). LIN-Q3 (§9 r. 188) parla di E^mult_AB. ✔
- Residuo: la Lettura di T3(vi) cita "atteso classico" O(ν) per soluzioni a tratti lisce (Goodman–Xin 1992, Tang–Teng 1997) come CON-FONTE da verificare; l'arbitro del kill-argument osserva che la letteratura potrebbe dare O(ν|log ν|) con formazione dello shock: la congettura Θ(ν) di Q1 va quindi scritta "O(ν) o O(ν|log ν|)". MINOR.
**Esito: correttamente registrato APERTO; nessun enunciato lo assume.** Il kill-argument sulla versione corretta lo conferma (P4 sceso da still_unresolved critical a partially_answered major = problema aperto, non errore).

### 2.7 S4T-T4, S4T-P5, S4T-P6, S4T-C1
| MC | passo | esito |
|---|---|---|
| T4.1 | (i) getto KdVB per ε sin x: −(ε/2)(2dν cos x + 5dε cos 2x − 3εν sin 2x) | OK (SymPy) |
| T4.2 | (ii) E^add = u − S_Au₀ − S_Cu₀ − S_Bu₀ + 2u₀ (N = 3); S_Cu₀ ∈ C^∞; salti di S_B | OK, CONDIZIONALE [H-KB] (esistenza con u(t) ∈ C(𝕋): classico per dati lisci, fonte da indicare) |
| T4.3 | (iii) δ_d: v_xxx(t,X) = u₀‴/J⁴ − 3tu₀″²/J⁵; d/dt(δ_dJ) = −Jv_xxx; formula chiusa | OK (SymPy: identità esatta); resto non stimato ⇒ candidato, APERTO S4T-Q2 (dichiarato) |
| P5.1 | invarianza di [0,1]; (ii) e_t = νu_xx + r(1−u−ρ)e con |r(1−u−ρ)| ≤ r; p₁, p₂ e Q₂; E^add = e − (h−u₀) | OK |
| P5.2 | (iii) u ≥ S_A(t)u₀ > 0, confronto con L(t−t₁,m₁) (c = −r(1−u−L) limitata), u → 1, h → ū₀, ρ → 1_{u₀>0}; E_∞ ≢ 0 (casi u₀ > 0 e u₀(x₁) = 0, ū₀ < 1) | OK; **P5-1 (MINOR, QUANTIFIER):** "non esiste C con ‖E^add(t)‖ ≤ Cν per ogni t" va letto "per ogni t e ogni ν" (C indipendente da ν): a ν fisso la stima con C = sup_t‖E^add(t)‖/ν è banalmente vera. Precisare il quantificatore |
| P5.3 | L(t,z) risolve l'ODE, ∂_zL(t,0) = e^{rt} | OK (SymPy) |
| P6.1 | Duhamel, divisore K² − k_l² − k_m² = 2k_lk_m; parte ε² del trasporto −tu₀u₀′; calore lineare | OK |
| P6.2 | sviluppo del bracket −νt²(k_l²+k_lk_m+k_m²) + O(t³); confronto con la parte ε² del getto **indipendente** (Hopf–Cole) per ε(sin x + ½cos 2x), t ≤ 4; caso sin = DEVIL-4 | OK (SymPy) |
| C1.1 | (a) [D_P,D_Q] = D_{D_PQ − D_QP} (G″ simmetrica) | OK (classico, Olver; SymPy su test) |
| C1.2 | (b) simbolo ρ_aq; (c) Burgers Q_k = (−1)^{k+1}(2ν)^ku_ku_{k+1}, KdVB ρ^kq_B, Fisher −r(−2ν)^ku_k² | OK (SymPy k ≤ 4 / k ≤ 3) |
| C1.3 | (d) indipendenza: pesi distinti (Burgers, Fisher), componente di grado minimo (KdVB) | OK (SymPy: rango pieno di X, Y, ad¹..ad⁴ per KdVB a parametri generici). **C1-2 (MINOR, notazione):** per Fisher "Q₀ = Y" è falso (Y ha anche la parte lineare ru₀); l'indipendenza vale comunque (la parte lineare di una combinazione nulla dà c_X = c_Y = 0 perché ν, r ≠ 0), ma va scritto |
| C1.4 | (e) applicazione di P1-T5: 𝒜 = End_ℂ(𝒫) associativa unitaria, (H) verificata, conclusione identica all'enunciato di §C | OK |
| C1.5 | Lettura: "nessuna formula finita … riproduce Burgers neppure come getto" | **C1-1 (MINOR, LOGICAL_GAP):** P1-T5 dà la disuguaglianza in End(𝒫)[[t]]; per passare al getto applicato a u₀ serve una riga: e^{tD_P} e i loro prodotti sono omomorfismi di algebre di 𝒫[[t]] che commutano con ∂, quindi sono determinati dall'immagine di u₀ (u_k = ∂^ku₀) ⇒ uguaglianza su u₀ ⟺ uguaglianza in End(𝒫)[[t]]. La conclusione vale come identità di getti **per tutti i dati** (in 𝒫[[t]]), non per un dato w₀ fissato (per w₀ costante tutto coincide). Aggiungere la riga e il qualificatore |

## 3. Rilievi e fix (proof-checker, Phase 2: proposti, non applicati)
| id | severità | categoria | fix (strategia) |
|---|---|---|---|
| T3-1 | **MAJOR** (OVERSTATED + GLOBAL sul criterio d'uscita della scheda; nessun enunciato numerato falso) | SCOPE_OVERCLAIM | WEAKEN_CLAIM nella cornice: titolo e Esito come esito diviso (§2.5 T3.12); ritirare "PR3 ✔ in L∞" come evidenza; il ramo del criterio d'uscita va deciso dal coordinatore sapendo che la parte non definitoria negativa riguarda solo E^mult_AB |
| T2-1 | MINOR | LOGICAL_GAP (stesura) | ADD_DERIVATION: Taylor misto in (s,λ) con J_λ ≥ 1 − θ (§2.3 T2.11) |
| T2-2 | MINOR | CONSTANT_DEPENDENCE_HIDDEN | dichiarare che "quadratica" = O(ε²) con costanti in (θ, w₀, T) e che K₁ = O(ε) solo nel regime |
| J-1 | MINOR | REGULARITY_GAP | una riga sulla liscezza di u fino a t = 0 |
| L1-1 | MINOR | HIDDEN_ASSUMPTION | dichiarare l'esistenza globale classica di S(t)u₀ (chiusa da F2-1) |
| F2-1 | MINOR | ADD_DERIVATION | [F2] si dimostra qui: φ > 0 risolve il calore (calcolo), u = −2νφ_x/φ risolve Burgers (calcolo di due righe), φ₀ = e^{−U₀/2ν} è liscia con crescita al più esponenziale ⇒ u liscia su [0,∞)×𝕋 con u(0) = u₀; unicità tra soluzioni classiche per energia (già scritta). La citazione di Hopf 1950 diventa superflua |
| T3-2 | MINOR | UNCLEAR | "(dimostrato …)" → "(limite inferiore dimostrato …)"; "lo tiene su ν/D" → euristica |
| T3-3 | MINOR | SCOPE | (vii) come enunciato di scala, senza il rapporto "violazione ≳ ε/ν" |
| Q1-1 | MINOR | UNCLEAR | congettura di S4T-Q1: "Θ(ν) oppure Θ(ν|log ν|)" (formazione dello shock) |
| P5-1 | MINOR | QUANTIFIER_ERROR (di formulazione) | "C indipendente da ν" |
| C1-1 | MINOR | LOGICAL_GAP | riga sugli omomorfismi; qualificatore "per tutti i dati" |
| C1-2 | MINOR | UNCLEAR | Fisher: Q₀ ≠ Y; argomento della parte lineare |
Acceptance gate (proof-checker): (1) nessun FATAL/CRITICAL aperto ✔; (2) ipotesi esplicite e interscambi giustificati (DCT in T3.5/T3.9 con dominazione |v|, |u| ≤ ‖u₀‖; Fatou con integrando ≥ 0) ✔, con J-1/L1-1 da scrivere; (3) O(·) con dipendenze dichiarate ✔ dopo T2-2; (4) red team eseguito su tutti i lemmi chiave ✔ (§5).

## 4. Fatti esterni
- **[F1] Lax–Oleinik = soluzione entropica di Kružkov** (Evans, PDE, 2ª ed., §3.4.2–3.4.3; Kružkov 1970): enunciato classico, ma **non verificato riga per riga** in questa tornata (nessuna lettura della fonte; numerazione non controllata). Stato: **CON-FONTE (da verificare)**. Nota: per u₀ periodico C¹ si potrebbe evitare la fonte verificando direttamente che v = (x − a(x))/t soddisfa la formulazione debole e la condizione di Oleinik v(x+z) − v(x) ≤ z/t (immediata dalla monotonia di a) e invocando l'unicità di Oleinik/Kružkov: resta comunque un teorema di unicità esterno. Tutti gli items di T3 e L2(d) ("S_B(t)u₀ non ha rappresentante continuo") dipendono da [F1] solo per identificare v con S_B; gli enunciati su v come funzione di Lax–Oleinik sono dimostrati qui.
- **[F2] Hopf–Cole**: la parte di calcolo è verificata (u = u₀ − 2νP_x/P, usata nel red team come strumento indipendente, coincide con i getti di Burgers fino a t⁵); l'unicità per energia è corretta; con F2-1 lo stato diventa **DIMOSTRATO** (la citazione Hopf 1950 resta come riferimento storico, non portante).
- **[F3] Kuznetsov 1976** (‖S(t)u₀ − S_B(t)u₀‖_{L¹} ≤ C√(νt)TV(u₀)): classico, **non verificato**: **CON-FONTE (da verificare)**; usato solo in T3(iv) e nelle frasi "Θ(√ν)", tutte marcate CONDIZIONALE. ✔
- Goodman–Xin 1992, Tang–Teng 1997 (in T3(vi) e P3 Interpretazione): citati come attesa, nessun enunciato dipende da essi. ✔
- [H-KB] (T4(ii)): buona posizione globale di KdV–Burgers su 𝕋 per dati lisci: classica, fonte da indicare; T4(ii) resta CONDIZIONALE.

## 5. Red team SymPy (Phase 1.5) — `work/CHECK/sympy/audit_s4term.py` → `audit_s4term.out`
**Esito: 44/44 OK** (.venv -I; script eseguito per intero, nessuno script _vendor o di work/S4-TERM usato). Strumento indipendente: getti veri di S(t)u₀ calcolati con **Hopf–Cole** (u = u₀ − 2νP_x/P, P = Σ(νt)^kR_{2k}/k!), S_B con le caratteristiche (Picard su v = f(x − tv)), S_A con la serie del calore, tutto come serie in t con x codificato da z = e^{ix} (aritmetica esatta di polinomi di Laurent); confronti con test di nullità esatti/numerici a 30 cifre in punti razionali casuali.
- T1: [s²] Burgers e formula ½ΣT_n′[T_m]; omogeneità ν^a/grado b+1/peso 2a+b (tutti i monomi, k ≤ 4); **serie di E^add dalle parole miste = calcolo indipendente per t⁰..t⁴** (dato ε(sin x + ½cos 2x), ε, ν simbolici); legge di scala [t^k]E(ε, ν = με) = ε^{k+1}[t^k]E(1,μ); esempio DEVIL-4; [t²]E^mult_AB = νu₀′u₀″ e [t²]E^mult_BA = −νu₀′u₀″ per **composizione esplicita dei flussi**; Lemma J(ii): getto di S_A(t)S_B(t)u₀ = e^{tD_B}e^{tD_A}u₀ (k ≤ 3, ordine di Gröbner confermato); E^mult senza parole costanti (k ≤ 4); KdVB [s²] e caso sin; Fisher [s²]E^add, [s²]E^mult_AR.
- T2: coefficiente di ν¹ dei getti veri di E^add, E^mult_AB, E^mult_BA = sviluppo delle tre forme chiuse **fino a t⁵**, tutti gli ordini in ε (u₀ = ε sin x); parte ν² dei tre resti = O(t³) e senza termine ε¹ (t ≤ 5); Passo 4 (δ e v_xx = u₀″/J³ come serie); **Passo 7: equazione di ŵ come identità esatta** (u, h, v, δ funzioni generiche); Passo 7(1): ∂²(δ − su₀″) = O(s²) e O(λ²).
- P3: M₂ = 3√3/16, M₃ = 25√5/216; u₀ = sin x (κ = 1, t* = 1): η^{3/2}sup|E₁^add| = 0.45659, 0.45901, 0.45925 (η = 10⁻², 10⁻³, 10⁻⁴) → 0.45928; η^{5/2}sup|E₁^AB| = 0.35962, 0.36536, 0.36594 → 0.36600; η^{3/2}sup|E₁^BA| = 0.45052, 0.45840, 0.45919 → 0.45928.
- L2/T3: sin x, t = 2: D = 1.895494 ≥ |I|/t = 1.047198; ∫₀^∞Φ_N(−s)ds = 1/√(2π) (simbolico); ∫₀¹e^{−w²/4} ≥ e^{−1/4}; Hopf–Cole numerico **indipendente** (quadratura vettorizzata con log-sum-exp, Lax–Oleinik per minimizzazione su griglia, calore per quadratura gaussiana): sup|E^mult_AB| = 0.752, 0.837, 0.889 ↗ D/2 = 0.948; ‖E^mult_AB‖_{L¹(finestra)}/√ν = 2.742, 2.887, 2.951 ↗ 2D√(t/π) = 3.025 (ν = 10⁻², 2.5·10⁻³, 6.25·10⁻⁴). Coincide con la numerica s4 dichiarata (2.74, 2.90, 2.96).
- C1: caratteristiche di ad^k (Burgers k ≤ 4, Fisher k ≤ 4 con Q₀ ≠ Y, KdVB simbolo ρ^kq_B k ≤ 3); [D_P,D_Q] = D_{D_PQ−D_QP} su test; rango pieno di X, Y, ad¹..ad⁴ per KdVB.
- T4(iii): v_xxx(t,X) = u₀‴/J⁴ − 3tu₀″²/J⁵ e d/dt(δ_dJ) = −Jv_xxx esatti. P5: L(t,z) e ∂_zL(t,0) = e^{rt}. P6: bracket = −νt²(k_l²+k_lk_m+k_m²) + O(t³); **formula di E^add_[2] = parte ε² del getto Hopf–Cole fino a t⁴** (due modi); caso sin: E^add_[2] = (2νte^{4νt} − e^{2νt} + 1)e^{−4νt}sin 2x/(4ν), [t²] = 3/2 ν sin 2x.
Contro-esempi cercati: nessuno trovato (getti, forme chiuse, costanti, limiti). Nessun candidato aperto.

## 6. Kill-argument sulla versione corretta di S4T-T3 — skill kill-argument, revisori = subagenti Claude freschi
Input: `work/CHECK/KA_S4T_T3_input.md` (definizioni, [F1]–[F3], L2, T3 (i)–(vii) con prove, Esito §1, S4T-Q1: testo alla lettera). Memo: `KA_S4T_T3_attack.md` (Thread 1, a1c9a9eeb80866b1d); arbitrato: `KA_S4T_T3_adjudication.md` (Thread 2, ae95d318d522a4e33). Nessuno dei due ha visto l'audit, il kill-argument v1 o le correzioni.
**Sintesi dell'attacco:** (i),(ii) sono tautologie di A9 (salto di S_B); (iii) è l'errore classico del calore su un salto, Θ(√ν) da [F3] non verificato; [F1] non verificato; la sola norma che isola l'interazione (‖E^add‖_{L¹}) è aperta e la numerica ≈10ν suggerisce una risposta **positiva**; (vii) confronta con un fantoccio. "Reject: il verdetto negativo è un artefatto della definizione A9."
**Arbitrato:** P1 (i),(ii) definitori — partially (major, cornice; enunciati veri, (ii) ricontrollato); **P2 "PR3 ✔ in L∞" e ramo negativo su fatti definitori — still_unresolved (major)**; P3 (iii) classico, [F3] — partially (minor; limite inferiore ricontrollato a mano senza [F3]); P4 L¹ di E^add aperto — partially (major: problema aperto dichiarato, nessun enunciato lo assume); P5 [F1]/[F3] — partially (minor); P6 (vii) fantoccio — partially (minor). Conteggi 0 / 5 / 1.
**Verdetto (calcolato da me con la tabella della skill): WARN** (reason_code: unresolved_major_or_minor). Rispetto alla v1 (FAIL, P4 critical) il punto critico è chiuso come registrazione (APERTO dichiarato, non assunto); resta un MAJOR di cornice, che coincide con il mio T3-1. Valutazione netta dell'arbitro: "gli enunciati numerati reggono … il punto debole è lo strato interpretativo".
**Concordanza con l'audit:** piena. Il kill-argument non ha trovato errori negli enunciati numerati; i suoi rilievi P1/P2 = T3-1, P6 = T3-3, P4 = Q1-1/§2.6. Nessun rilievo nuovo da verificare con SymPy.

## 7. Conseguenze per LEDGER (proposte al coordinatore)
Vedi TABELLA LEDGER in inbox/central.md (S-CHECK-11). Sintesi: T1, L0, L1, T2 (con Passo 7 dopo T2-1/T2-2), P3, L2, T3 (i)(ii)(iii)(v)(vi)(vii) → DIMOSTRATO mod [F1] (CON-FONTE) [e, per (iii),(v), mod F2-1 che lo chiude]; T3(iv) CONDIZIONALE [F3]; T4(i) DIMOSTRATO, T4(ii) CONDIZIONALE [H-KB], T4(iii) candidato (V-ex); P5, P6, C1 DIMOSTRATO (con fix MINOR); S4T-Q1..Q5 APERTO. Fix obbligatorio prima del Gate 4b: **T3-1** (cornice dell'Esito).
