# AUDIT P2 — claim di S-P2 (regolarizzazione): P2-T3, L1, T2, T4, T5, P7, C1, P3, P4, T1, P2, P5, P6
Revisore: S-CHECK-4 (4ª tornata) · 25/10/2026
**Fonte esaminata.** `work/P2/CHECK_REQUEST.md` (notazione, Fatti F1–F6, enunciati e prove di P2-T3, L1, T2, T5, C1, P3, P4, T1). `work/P2/PROOF_PACKAGE.md` è stato letto **solo per riferimenti puntuali**, dichiarati qui: §4 [P2-P2] (enunciato, prova, osservazione sulle classi "pure"); §7 [P2-T4], [P2-P5]; §8 "Richiamo" (definizioni di Λ_j, δ, μ_c, κ, assenti dalla CHECK_REQUEST) e [P2-P7]; §9 [P2-P6]. Non ho letto §10–§14 (passaggio avversariale, mappa, righe LEDGER, messaggi) né le parti di commento.
**Fatti esterni usati come dati.** F1 = C12-T1, F2 = C12-L2, F3 = C12-T3, F4 = C12-C1, F6 = C12-P4(a) (DIMOSTRATO, LEDGER). **F5** (P1-P2(c), P1-L1) e P1-P1(e), P1-T2, P1-L2: al momento della richiesta "audit in corso"; **ora DIMOSTRATO** da S-CHECK-3 (AUDIT_P1.md: P1-P2 PASS-con-fix(P2-1,P2-2), P1-L1 PASS-con-fix(L1-1,L1-2), P1-P1(e) PASS-con-fix(P1e-1,P1e-2), P1-T2 PASS-con-fix(T2-1,T2-2)); la registrazione nel LEDGER spetta al coordinatore. Le dipendenze da F5 sono quindi **scaricate** (condizionate alla registrazione).
**Skill caricate** (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-checker (Phase 0.5 enunciati canonici e micro-claim, checklist A–H, Phase 1.5 red team, severità a due assi, acceptance gate; il reviewer sono io, niente Codex/LaTeX), scientific-critical-thinking (mostrato vs affermato; stato proporzionato), sympy.
**SymPy/numpy:** `work/CHECK/sympy/audit_p2.py` → `audit_p2.out`, **ESITO 72/72 OK** (.venv -I). I controlli numerici sono di coerenza su esempi finiti: non sostituiscono le prove, che ho controllato a mano passo per passo.

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| **P2-T3** (a)–(d) | **PASS-con-fix(T3-1, T3-2)** | **DIMOSTRATO** (due sottospazi chiusi di un Hilbert qualsiasi; tabella (e): ogni riga eredita lo stato della fonte di c_F) |
| ⇒ C12-P7(b) | — | la direzione "⇒" passa da CON-FONTE (Deutsch 9.35, non verificato) a **DIMOSTRATO** via P2-T3(b), per **due** sottospazi |
| **P2-L1** | **PASS-con-fix(L1-1)** | DIMOSTRATO |
| **P2-T2** (a)–(c) | **PASS-con-fix(T2-1, T2-2, T2-3)** | **DIMOSTRATO** (rettangolo; "⇒" anche su Ω s.c. con C12-L2′); "⇐" dipende da F5 = P1-P2(c), ora DIMOSTRATO (S-CHECK-3) |
| **P2-T4** | **PASS-con-fix(T4-1)** | DIMOSTRATO (teorema); applicazione (i) per selezioni non lineari dopo T4-1; (ii) dipende da P1-P1(e), DIMOSTRATO |
| **P2-T5** (i)–(v) | **PASS-con-fix(T5-1, T5-2)** | DIMOSTRATO |
| **P2-P7** | **PASS** | DIMOSTRATO |
| **P2-C1** (a),(b) | **PASS-con-fix(C1-1)** | DIMOSTRATO (la scelta tra le due alternative di (b) per m ≥ 1 resta P2-Q1 APERTO) |
| **P2-P3** (i)–(iii) | **PASS** (fix notazionale P3-1 facoltativo) | DIMOSTRATO |
| **P2-P4** (a),(b) | **PASS** | DIMOSTRATO |
| **P2-T1** | **PASS** | DIMOSTRATO |
| **P2-P2** | **PASS** | DIMOSTRATO (coefficienti costanti); variante a coefficienti polinomiali = dipende da C12-P5 (non auditata qui) |
| **P2-P5** (a),(b) | **PASS-con-fix(P5-1)** | DIMOSTRATO ((a) dipende da P1-T2(ii), P1-L1(d), P1-L2, DIMOSTRATO) |
| **P2-P6** (a)–(c) | **PASS** | DIMOSTRATO |

Nessun rilievo FATAL o CRITICAL sui claim di S-P2. Un rilievo **MAJOR di portata, esterno ai claim** (O-1): la condizione "c_F < 1" di C12-P7 / G★′ punto 2 ha senso solo per **due** fattori; per N ≥ 3 i c_F a coppie non decidono la chiusura (controesempio). Tutti gli altri rilievi sono MINOR.

## 1. Enunciati canonici (Phase 0.5)
- **T3.** ∀H Hilbert (reale o complesso), ∀ℋ₁,ℋ₂ ⊂ H chiusi con A := ℋ₁⊖ℐ ≠ 0 ≠ B := ℋ₂⊖ℐ: con S(ω₁,ω₂) = ω₁+ω₂ su W = ℋ₁⊕ℋ₂, T = S*S, γ := inf σ(T|_{(ker S)^⊥}):
  (a) σ(T|_{(ker S)^⊥}) = (1+σ(K)) ∪ ({2} se ℐ ≠ 0), σ(K) = −σ(K) ⊂ [−c_F, c_F], ±c_F ∈ σ(K); (b) γ = 1−c_F; ℋ₁+ℋ₂ chiuso ⟺ c_F < 1; allora ‖S^†‖ = (1−c_F)^{−1/2}, ottimale; (c) ∀α>0 ‖R_α‖² = sup_{σ(T)} λ/(λ+α)²; sup_α ‖R_α‖ = (1−c_F)^{−1/2} se c_F<1, = ∞ se c_F = 1; (d) c_F<1, u ∈ ℋ₁+ℋ₂ ⇒ ∀α>0 ‖ω_α−S^†u‖ ≤ α/(1−c_F+α)‖S^†u‖; c_F = 1 ⇒ ∃u ∈ M∖(ℋ₁+ℋ₂), e ∀ tale u: Sω_α → u, ‖ω_α‖ → ∞ (α→0).
- **L1.** ∀Ω limitato, ∀m, ∀Q ≠ 0 di ordine k con Q(∂)ℋ_n = 0 ∀n: ∀u ∈ H^m: dist_{H^m}(u,M) ≥ ‖Q(∂)u‖_{H^{m−k}}/C_Q.
- **T2.** Ω rettangolo limitato, N ≥ 2, a_n distinti, a−a_n ≠ 0: ∀u ∈ ker_{H^m}(∂_t−a(∂_x)): (a) Q(∂)u = g(∂_x)u e dist(u,M) ≥ ‖g(∂_x)u‖_{H^{m−k}}/C_Q; (b) u ∈ M ⟺ g(∂_x)u = 0, e {u ∈ ker(∂_t−a) : u ∈ M} = Sol(R/𝔍), dim = K, EP; (c) ∀R come in P2-T1: lim r_α = E^⊥(u), ≠ 0 ∀u ∉ Sol(R/𝔍).
- **T4.** ∀X,Y normati, ∀V ⊆ X, ∀Φ: V→Y lineare, ∀(R_α) mappe X→Y Lip(R_α) ≤ L_α con R_αv → Φv ∀v ∈ V: ‖Φ‖ ≤ liminf_{α→0} L_α.
- **T5.** ℐ di dimensione finita, Φ_j frame di Parseval **di ℋ_j**, ipotesi ℓ¹ su u_j e su ℐ: (i) insieme ammissibile = u+{(z,−z): z ∈ ℐ}, minimo esiste; (ii) κ_ℐ ≤ κ < 1/2 ⇒ ogni minimizzatore dista ≤ 2δ/(1−2κ_ℐ); (iii) (basi o.n.) [∀ split supportato sui grappoli è l'unico minimizzatore] ⟺ NSP sul gauge; (iv) basi adattate: NSP ⟺ nessun ε_k nei grappoli; (v) ℐ = 0 ⇒ ammissibile = punto.
- Gli altri enunciati sono riportati nelle rispettive sezioni.

## 2. Dipendenze (DAG, nessun ciclo)
T1 ← (Pitagora). L1 ← continuità di ∂ su H^σ. T2 ← L1, F2 (C12-L2), F1 (C12-T1), F5 (P1-P2(c), P1-L1). T3 ← teorema spettrale, mappa aperta, T1 (solo in (d)). T4 ← nessuno (elementare); applicazioni ← T3(b), P1-P1(e). T5 ← nessuno (finito-dimensionale su ℐ). P7 ← T5(iv), F6. C1 ← F3, F4, T1, T3. P3 ← Mazur, compattezza debole, F1. P4 ← mappa aperta (implicita), compattezza debole. P5 ← P1-T2(ii), P1-L1(d), P1-L2, Plancherel. P6 ← Lagrange. Nessun riferimento in avanti; T3 non usa T2 né T5.

## 3. Micro-claim ed esiti
### 3.1 P2-T3 (priorità 1)
| MC | passo | esito |
|---|---|---|
| T3.1 | S*h = (P_{ℋ₁}h, P_{ℋ₂}h); ker S = {(z,−z): z ∈ ℐ} | OK |
| T3.2 | W = (A⊕B) ⊕ Δ ⊕ ker S, ortogonale. **Domanda (a): vale con ℐ di dimensione infinita?** Sì: ℋ_j = A_j ⊕ ℐ è una scomposizione ortogonale di un chiuso in due chiusi (non serve dim ℐ < ∞); A⊕B = A×B e Δ = {(z,z)} sono chiusi (Δ è immagine isometrica di ℐ a meno del fattore √2); le tre ortogonalità sono verificate nel testo | OK |
| T3.3 | T(z,z) = (2z,2z); T(a,b) = (a+Π_Ab, b+Π_Ba) perché P_ℐb = 0 per b ⊥ ℐ | OK |
| T3.4 | K autoaggiunto: ⟨K(a,b),(a′,b′)⟩ = ⟨b,a′⟩+⟨a,b′⟩ = ⟨(a,b),K(a′,b′)⟩ | OK (anche nel caso complesso: entrambi i membri sono la stessa espressione) |
| T3.5 | ‖K‖ ≤ c_F: ‖Π_Ab‖ = sup_{a′∈A,‖a′‖=1}\|⟨a′,b⟩\| ≤ c_F‖b‖ | OK |
| T3.6 | sup σ(K) = sup rango numerico ≥ c_F: rotazione di fase di b (resta in B), x = (a,b)/√2, ⟨Kx,x⟩ = Re⟨a,b⟩ | OK; quindi ‖K‖ = c_F |
| T3.7 | UKU* = −K con U(a,b) = (a,−b) unitario ⇒ σ(K) = −σ(K), inf σ(K) = −c_F | OK (verifica: UK(a,−b) = U(−Π_Ab, Π_Ba) = −K(a,b)) |
| T3.8 | σ(T|_{(ker S)^⊥}) = (1+σ(K)) ∪ σ(T|_Δ); 1 ± c_F ∈ σ(T) | OK (spettro di una somma diretta ortogonale di operatori invarianti = unione) |
| T3.9 | (b) γ = min(1−c_F, 2) = 1−c_F (serve A⊕B ≠ 0, cioè l'ipotesi A ≠ 0 ≠ B) | OK — **formula spettrale confermata** (audit_p2 T3a/T3b, 6 coppie reali e complesse con dim ℐ = 0..3 e dimensioni diverse) |
| T3.10 | im S chiusa ⟺ S limitata dal basso su (ker S)^⊥ (mappa aperta) ⟺ γ > 0 (⟨Tω,ω⟩ = ‖Sω‖²; inf rango numerico = min σ su sottospazio invariante) | OK. È la direzione "⇒" di C12-P7(b) (chiuso ⇒ γ>0 ⇒ c_F<1), ora **provata**: non serve Deutsch |
| T3.11 | ‖S^†‖² = sup_{ω⊥ker S} ‖ω‖²/‖Sω‖² = 1/γ, ottimale (γ ∈ σ) | OK (audit_p2 T3b ‖S^+‖) |
| T3.12 | (c) R_αR_α* = T(T+α)^{−2}; ‖R_α‖² = sup_{σ(T)} λ/(λ+α)²; per λ ≥ γ: λ/(λ+α)² < 1/λ ≤ 1/γ; γ/(γ+α)² → 1/γ | OK (audit_p2 T3c). Nota: per ogni α fissato ‖R_α‖ < γ^{−1/2} strettamente; il sup su α non è raggiunto |
| T3.13 | (c), c_F = 1: T|_{A⊕B} iniettivo (T(a,b)=0 ⇒ ‖S(a,b)‖² = 0 ⇒ a = −b ∈ ℐ∩A = 0); **domanda (c): "0 nello spettro, iniettivo ⇒ 0 non isolato"**: corretto — un punto isolato λ₀ dello spettro di un autoaggiunto ha proiezione spettrale E({λ₀}) ≠ 0 e Ran E({λ₀}) = ker(T−λ₀); quindi 0 isolato ⇒ autovalore, contro l'iniettività. Poi ‖R_{λ_k}‖² ≥ λ_k/(2λ_k)² | OK (audit_p2: blocchi con angolo θ_k → 0, sup_α‖R_α‖ ≥ 1/(2√λ_k) → ∞) |
| T3.14 | (d) ω_α − ω^† = −α(T+α)^{−1}ω^†, ω^† ∈ (ker S)^⊥ invariante; norma = α/(γ+α), raggiunta | OK (audit_p2 T3d: uguaglianza sull'autovettore di γ) |
| T3.15 | (d), c_F = 1: u ∈ M∖im S esiste per (b); Sω_α → u per P2-T1 (R = ½‖·‖² finito su W ⇒ densità); norme limitate lungo α_k → 0 ⇒ limite debole ω con Sω = u (S debolmente continua) ⇒ assurdo. Quindi liminf_{α→0}‖ω_α‖ = ∞ | OK. L'argomento non usa c_F = 1: vale per ogni u ∈ M∖im S |
| T3.16 | Tikhonov: ω_α = (T+α)^{−1}S*u è il minimizzatore di ½‖u−Sω‖²+(α/2)‖ω‖² (gradiente S*(Sω−u)+αω = 0, funzionale strettamente convesso) | OK; coerente con J_α di P2-D1 con R = ½‖·‖² |
| T3.17 | **più di due sottospazi**: la prova non li usa (W = ℋ₁⊕ℋ₂). Ma la tesi non si estende a N ≥ 3 nella forma "c_F < 1" → **O-1**, fix **T3-1** | portata |
| T3.18 | tabella (e): i valori di c_F sono presi da C12-P4(a),(b), C12-P8, C12-T3. Ho ricontrollato solo la riga dei trasporti paralleli con c = 0: γ² = Γ₁₂²/(Γ₁₁Γ₂₂) = tanh(dT/2)/(dT/2) per d₁ = 0, d₂ = d (audit_p2 T3e, simbolico), γ → 1 per dT → 0 | OK; le altre righe ereditano lo stato della fonte → **T3-2** |

**Osservazione (O-2, non un difetto).** (b) dà anche l'equivalenza della norma di Aronszajn con costanti esplicite: ‖u‖_K² := min{‖u₁‖²+‖u₂‖²} = ‖S^†u‖² ≤ ‖u‖²/(1−c_F) e ‖u‖² = ‖Sω‖² ≤ ‖S‖²‖ω‖² con ‖S‖² = max σ(T) = 2 se ℐ ≠ 0, 1+c_F se ℐ = 0. Questo copre la parte "norma di Aronszajn equivalente ⟺ somma chiusa" di C12-T5(e)/gram.md, con costanti.

### 3.2 P2-L1
| MC | passo | esito |
|---|---|---|
| L1.1 | Q(∂): H^m → H^{m−k} continua, anche per m < k (composizione di ∂_j: H^σ → H^{σ−1}, F-notazione) | OK |
| L1.2 | "Q(∂)v = 0 in 𝒟′" ⇒ Q(∂)v = 0 in H^{m−k}: serve l'iniettività H^σ(Ω) → 𝒟′(Ω) per σ < 0, vera perché C_c^∞ è denso in H_0^{−σ} | OK ma implicito → **L1-1** (MINOR) |
| L1.3 | si annulla su Σℋ_n e per continuità su M; ‖Qu‖ = ‖Q(u−v)‖ ≤ C_Q‖u−v‖; inf su v ∈ M | OK |
| L1.4 | C_Q ≤ Σ\|q_α\| per m ≥ k (β ↦ α+β iniettiva, \|α+β\| ≤ m) | OK |
| L1.5 | caso Q = 0 (C_Q = 0): la tesi divide per 0 | serve Q ≠ 0 (allora C_Q > 0: Q(∂) non si annulla sugli esponenziali) → **L1-1** |

### 3.3 P2-T2 (priorità 2)
| MC | passo | esito |
|---|---|---|
| T2.1 | **Domanda (a): Q(∂)u = g(∂_x)u in 𝒟′ per u ∈ H^m, anche m = 0.** Sì: gli operatori a coefficienti costanti commutano su 𝒟′(Ω), e l'induzione del testo è corretta. Prova più corta (facoltativa, **T2-1**): Q(τ,ξ) − g(ξ) si annulla su τ = a(ξ), quindi Q − g = (τ−a)·H con H ∈ R (divisione per il monico τ−a), e Q(∂)u − g(∂_x)u = H(∂)(∂_t−a(∂_x))u = 0. Per N = 2: Q − g = (τ−a)τ (audit_p2 T2a, identità operatoriale) | OK |
| T2.2 | norma H^{m−k} di g(∂_x)u: è la norma della stessa distribuzione Q(∂)u ∈ H^{m−k} (iniettività L1-1) | OK |
| T2.3 | (b) "⇒": u ∈ M ⇒ Q(∂)u = 0 (L1: Q annulla M) ⇒ g(∂_x)u = 0 ⇒ u ∈ Sol(R/𝔍) | OK |
| T2.4 | **Domanda (b): R/𝔍 ≅ ℂ[ξ]/(g).** R → ℂ[ξ], τ ↦ a(ξ), suriettivo con nucleo (τ−a) (divisione per il monico τ−a in ℂ[ξ][τ]); il quoziente per l'immagine di 𝔍 è ℂ[ξ]/(g). g ≠ 0 perché ogni a−a_n ≠ 0; dim = K (K = 0 ammesso: allora Sol = 0) | OK |
| T2.5 | F2 su rettangolo con dim R/𝔍 = K < ∞: dim Sol = K, EP. Radici semplici: K esponenziali distinti, linearmente indipendenti, base; g(ζ) = 0 ⇒ a(ζ) = a_n(ζ) per qualche n ⇒ modo in D_n | OK (audit_p2 T2b: AD, radice 0 tripla; tre termini, K = 5, cinque radici, ciascuna in una classe) |
| T2.6 | (b) "⇐": u EP, Q(∂)u = 0; fattori τ−a_n irriducibili non associati; F1 dà u = Σu_n in 𝒟′; F5 (P1-P2(c) + P1-L1(b),(c)): ogni tale scomposizione ha u_n ∈ 𝔅 ⊂ H^m; quindi u_n ∈ D_n, u ∈ ΣD_n ⊆ M | OK **condizionato a F5**, che è ora DIMOSTRATO (S-CHECK-3) → **T2-3** (aggiornare dipendenze e stato) |
| T2.7 | red team: F5 si può evitare con sola algebra? No. Con J_n := 𝔍+(τ−a_n) = (τ−a_n, a−a_n) si ha 𝔍 ⊆ ∩J_n ma in generale 𝔍 ≠ ∩J_n (AD: ξ² ∈ J₁∩J₂, ξ² ∉ 𝔍; audit_p2), e infatti la componente (x−ct)² − (2D/c)(x−ct) ∈ D₁ non sta in Sol(R/J₁). Le componenti stanno in D_n ma non in un modulo finito "per termine": serve davvero un argomento analitico come F5 | conferma della necessità della dipendenza |
| T2.8 | esempio AD: base {1, x−ct, (x−ct)²+2Dt}, scomposizione esplicita in D₁ + D₂ | OK (audit_p2, simbolico) |
| T2.9 | (c): "per **ogni** regolarizzatore il residuo limite è E^⊥(u)" vale sotto le ipotesi di P2-T1 (densità di S(dom R) in M). Per R qualsiasi resta vero, e basta per B8, che ‖r_α‖ ≥ dist(u,M) = ‖E^⊥(u)‖ > 0 per ogni ω | OK con precisazione → **T2-2** (MINOR) |
| T2.10 | "su Ω semplicemente connesso" ("⇒", riga LEDGER proposta): F2 va sostituito da C12-L2′ (DIMOSTRATO); "⇐" usa F5, provato su rettangolo | portata coerente con la riga proposta |

### 3.4 P2-T4 (priorità 3)
| MC | passo | esito |
|---|---|---|
| T4.1 | ‖R_αv − R_α0‖ ≤ L_α‖v‖; R_α0 → Φ0 = 0 (0 ∈ V); R_αv → Φv; quindi ‖Φv‖ = lim‖R_αv − R_α0‖ ≤ liminf L_α‖v‖ | OK. **Quantificatore:** per ogni v fissato il limite esiste e la stima vale con liminf; poi sup su ‖v‖ = 1. Corretto anche per R_α non lineari: l'unico uso della struttura è la differenza con R_α0 |
| T4.2 | **Banach–Steinhaus:** non è usato e non serve. (B–S darebbe il viceversa: per R_α lineari su X di Banach, convergenza puntuale su tutto X ⇒ sup ‖R_α‖ < ∞; qui la convergenza è solo su V e la conclusione è una minorazione.) | OK |
| T4.3 | "Φ illimitata ⇒ L_α → ∞": liminf L_α = ∞ | OK; in particolare nessuna successione α_k → 0 con L_{α_k} limitate |
| T4.4 | Applicazione (i): Φ = S^†|_{ℋ₁+ℋ₂} lineare, illimitata ⟺ c_F = 1 (T3(b)). Ma il testo estende a "ogni procedura di split (Tikhonov, ℓ¹, MCA, …) che converga allo split esatto": il limite di ℓ¹/MCA è una selezione σ non lineare e in generale ≠ S^†, quindi **non** è coperta da T4 con Φ = S^† | LACUNA (MINOR, applicazione) → **T4-1**: la stessa prova dà Lip(Φ) ≤ liminf L_α per Φ qualsiasi (‖Φv−Φw‖ = lim‖R_αv−R_αw‖); e ogni selezione esatta σ (Sσ(u) = u) ha Lip(σ) ≥ ‖S^†‖, perché σ(u)−σ(0) ∈ S^{−1}(u) ha norma ≥ ‖S^†u‖. Con c_F = 1 entrambe danno L_α → ∞ per ogni procedura (audit_p2 T4-1) |
| T4.5 | Applicazione (ii): X = H^m, Y = L²(Ω), V = EP ∩ ker Q, Φ = E^add (lineare); P1-P1(e) (ora DIMOSTRATO) dà Φ illimitata (enunciato in L²(Ω)/H^m, coerente) | OK |

### 3.5 P2-T5 (MCA) e P2-P7
Definizioni (dal PROOF_PACKAGE §8, "Richiamo": **non presenti nella CHECK_REQUEST** → **T5-1**): Λ_j insiemi di indici; δ := ‖1_{Λ₁^c}Φ₁*u₁‖₁ + ‖1_{Λ₂^c}Φ₂*u₂‖₁; μ_c(Λ,Φ;Ψ) := sup_j Σ_{i∈Λ}\|⟨φ_i,ψ_j⟩\|; κ := max{μ_c(Λ₁,Φ₁;Φ₂), μ_c(Λ₂,Φ₂;Φ₁)}.
| MC | passo | esito |
|---|---|---|
| T5.1 | (i) ammissibile = {(u₁+z,u₂−z)}; f finita, convessa, continua su ℐ (dim finita); coercività: ‖Φ₁*z‖₁ ≥ ‖Φ₁*z‖₂ = ‖z‖ (Parseval in ℋ₁) | OK |
| T5.2 | (ii) disuguaglianze su Λ₁, Λ₁^c: ‖1_Λ(a+b)‖ ≥ ‖1_Λa‖−‖1_Λb‖, ‖1_{Λ^c}(a+b)‖ ≥ ‖1_{Λ^c}b‖−‖1_{Λ^c}a‖; somma = ‖a‖−2‖1_{Λ^c}a‖+‖b‖−2‖1_Λb‖. **Segni**: corretti; con f(z) ≤ f(0) si ottiene ‖Φ₁*z‖₁+‖Φ₂*z‖₁ ≤ 2δ + 2(‖1_{Λ₁}Φ₁*z‖₁+‖1_{Λ₂}Φ₂*z‖₁) | OK |
| T5.3 | **Domanda (ii): basta Φ₂ Parseval in ℋ₂ e z ∈ ℋ₂?** Sì: z = Σ_j⟨z,φ_j^{(2)}⟩φ_j^{(2)} converge in norma in ℋ₂ ⊂ H; il prodotto scalare con φ_i^{(1)} ∈ H è continuo; Tonelli sulle somme di moduli. Non serve che Φ₁ sia un frame di H: basta φ_i^{(1)} ∈ H. Simmetricamente per z ∈ ℋ₁ | OK |
| T5.4 | (1−2κ)(‖Φ₁*z‖₁+‖Φ₂*z‖₁) ≤ 2δ; ‖v₁−u₁‖+‖v₂−u₂‖ = 2‖z‖ ≤ ‖Φ₁*z‖₂+‖Φ₂*z‖₂ ≤ somma delle ℓ¹ | OK (audit_p2 T5ii: 48 istanze con κ < 1/2, tutti i minimizzatori entro la stima). κ_ℐ ≤ κ e la stessa catena con κ_ℐ: OK (‖Φ_j*z‖₁ > 0 per z ≠ 0) |
| T5.5 | (iii) "⇐": δ = 0, f(z) ≥ f(0) + [NSP] > f(0) | OK (non usa le basi o.n.) |
| T5.6 | **Domanda (iii) "⇒": completezza del controesempio.** u₁ := −Φ₁(1_{Λ₁}Φ₁*z) ∈ ℋ₁, u₂ := Φ₂(1_{Λ₂}Φ₂*z) ∈ ℋ₂, supporti in Λ_j, coefficienti in ℓ¹ (perché Φ_j*z ∈ ℓ¹ per ipotesi); Φ₁*Φ₁ = I serve davvero (con un frame di Parseval Φ*Φ è solo un proiettore); Φ₁*(u₁+z) = 1_{Λ₁^c}Φ₁*z, Φ₂*(u₂−z) = −1_{Λ₂^c}Φ₂*z; f(z) ≤ f(0) con z ≠ 0 ⇒ (u₁,u₂) non è l'unico minimizzatore. Il quantificatore è giusto: "⇒" nega "per ogni split supportato" esibendone uno | OK (audit_p2 T5iii, 300 istanze) |
| T5.7 | (iv) Φ₁*z = Φ₂*z = (⟨z,ε_k⟩) sugli indici di ℐ, 0 altrove; test z = ε_k ⇒ A₁ = A₂ = ∅; viceversa ovvio | OK |
| T5.8 | (iv) "gli split recuperati esattamente sono quelli con u_j ⊥ ℐ": per grappoli fissati, gli split supportati sono ⊥ ℐ (inclusione); l'uguaglianza vale per la scelta massimale Λ_j = indici di ℋ_j⊖ℐ, dove f(z) = f(0) + 2‖z‖₁ (audit_p2 T5iv). Non ogni u ∈ ℋ₁+ℋ₂ ha uno split ⊥ ℐ (solo u ∈ A+B) | OK con precisazione → **T5-2** (MINOR) |
| T5.9 | (v) ℐ = 0 ⇒ punto | OK |
| P7.1 | ⟨A⊗1,1⊗B⟩_{H^m} = ⟨A⊗1,1⊗B⟩_{L²} = ∫A·conj(∫B) (sopravvive solo β = 0); ⟨A⊗1,1⟩_{H^m} = \|J\|∫A | OK (audit_p2 P7 in H¹ su (0,1)×(0,2)) |
| P7.2 | Gram incrociata = δ_{k0}δ_{l0}; κ = 0 se 0 ∉ Λ₁∪Λ₂, κ = 1 altrimenti; f(z) = cost + \|⟨u₁,e₀⟩+z‖1‖\| + \|⟨u₂,e₀⟩−z‖1‖\| (‖1‖ = \|Ω\|^{1/2} in ogni H^m) | OK; coerente con c_F = 0 (tabella T3(e)) |

### 3.6 P2-C1
| MC | passo | esito |
|---|---|---|
| C1.1 | (a)(i) F3: u = e^{d₁t}F(s)+e^{d₂t}G(s), F,G ∈ L²_loc(S); cambio (t,s) di determinante 1 | OK |
| C1.2 | **Domanda (a): il troncamento 1_{K_N}(s)u resta in ker f + ker g in 𝒟′?** Sì: 1_{K_N}F ∈ L²(K_N) ⊂ L¹_loc(S), quindi e^{d₁t}1_{K_N}F ∈ ker_{𝒟′}f per la clausola L¹_loc di F3; la stima L² usa Ω′ ⊂ [−M′,M′]² | OK |
| C1.3 | DCT: \|u−u_N\| ≤ \|u\|, u_N → u q.o. (∪K_N = S) | OK; somma densa in ker_{L²}fg |
| C1.4 | (a)(ii) C12-T3 + densità ⇒ esiste u ∈ ker fg ∖ (ℋ₁+ℋ₂); T3(d) | OK; "E^{fatt}_{L²}(u) ≠ 0" non è definito nella CHECK_REQUEST (si intende u ∉ ℋ₁+ℋ₂) → **C1-1** (MINOR) |
| C1.5 | (b) u ∉ ℋ₁+ℋ₂: una scomposizione con v_j ∈ ℋ_j ⊂ ker_{𝒟′} coinciderebbe con quella unica (δ = 0, f−g = 1) le cui componenti ∉ H^m; dicotomia u ∉ M (T1) / u ∈ M∖im S (T3(b),(d)) | OK |

### 3.7 P2-P3, P2-P4, P2-T1, P2-P2, P2-P5, P2-P6
| MC | passo | esito |
|---|---|---|
| P3.1 | (ii) R(ω_α) ≤ R(ω′) + ε_α/α per **ogni** rappresentazione esatta ω′ con R(ω′) < ∞ (non solo ω^†); coercività ⇒ limitatezza; residuo ≤ 2(αR(ω^†)+ε_α) → 0 | OK |
| P3.2 | **Domanda (ii): Mazur** — sottolivelli {R ≤ t} convessi e chiusi in norma ⇒ debolmente chiusi ⇒ R debolmente s.c.i. (anche con valori +∞) | OK |
| P3.3 | stretta convessità ⇒ unicità del minimo sull'affine chiuso ω^†+ker S (S limitata ⇒ ker S chiuso); principio delle sottosuccessioni | OK |
| P3.4 | R = ½‖·‖²: limsup‖ω_α‖ ≤ ‖ω*‖ + debole ⇒ forte | OK; qui S^†u indica la preimmagine di norma minima anche se im S non è chiusa (in T3 S^† è definita solo per c_F < 1) → **P3-1** (facoltativo, notazione) |
| P3.5 | (iii) nucleo H^m = nucleo 𝒟′ (EP ⊂ H^m su Ω limitato); in (T) δ = Σ_{n<m} deg(a_n−a_m) | OK |
| P4.1 | (a) EM chiuso; distanze; E(ℋ₁+ℋ₂) chiuso in EH chiuso ⟺ ℋ₁+ℋ₂ chiuso | OK |
| P4.2 | (b) (EM)^⊥ = 0 tramite Ey ∈ span{w} ⇒ ⟨y,e_k⟩ costante ⇒ y = 0; limitatezza ⇒ limite debole in M (convesso chiuso) ⇒ u ∈ M | OK (audit_p2 P4b: dist(Ew,EM) = 0.0128 a N = 10⁴) |
| T1.1 | Pitagora; ε_α-minimalità con R ≥ 0; limsup ≤ η ∀η | OK. Nessuna ipotesi su S oltre la linearità; ε_α → 0 basta |
| P2.1 | ker p_n(D) in 𝒟′(J) = span{x^je^{ρx}} (soluzioni distribuzionali lisce); lcm: molteplicità max; Σℋ_n = ker ℓ(D) | OK (audit_p2: ‖P^⊥e^x‖² = 20e − 7e²/2 − 57/2 ≈ 3.94·10⁻³) |
| P2.2 | osservazione "classi pure" ker a_n(∂_x): Q = lcm(a_n)(ξ) annulla le classi; E^⊥ = 0 ⇒ u ∈ ker(τ−a) ∩ ker lcm(a_n)(∂_x), dim deg lcm (serve a_n ≠ 0) | OK |
| P5.1 | (a) ‖e^{sa_n}−I‖ ≤ e^{\|s\|\|a_n\|(ρ′)}−1 (serie); prodotto e somma su \|S\| ≥ 2 | OK dato P1-T2(ii), P1-L2; \|a_n\|(ρ′) (norma "pesata" del polinomio, da P1-L2) non è definita nel testo → **P5-1** (MINOR) |
| P5.2 | (b) Plancherel; e_{≥2} a coefficienti ≥ 0 ⇒ \|e_{≥2}(z)\| ≤ e_{≥2}(\|z\|) ≤ e_{≥2}(β) (monotonia); AD: β₁ ≤ 2, β₂ ≤ 1 | OK (audit_p2 P5b: max \|z₁z₂\| = 2.0000 sulla griglia) |
| P6.1 | colonne di V^{−1} = coefficienti dei polinomi di Lagrange; ‖·‖_{1→1} = max ℓ¹ delle colonne; (a) submoltiplicatività; (b) coefficiente direttore; (c) h^dk!(d−k)! minimo a k = ⌊d/2⌋ | OK (audit_p2 P6, nodi razionali esatti, d = 2..5) |

## 4. Rilievi e fix (proposti, non applicati ai file di S-P2)
- **T3-1** (MINOR sul claim; vedi O-1 per la portata) Dichiarare in T3 "due sottospazi" e aggiungere la versione per N ≥ 3: con S: ⊕_{j=1}^Nℋ_j → H, γ_N := inf σ(S*S|_{(ker S)^⊥}); la prima metà di (b) dà Σℋ_j chiuso ⟺ γ_N > 0, ‖S^†‖ = γ_N^{−1/2}; (c) e (d) valgono parola per parola con γ_N al posto di 1−c_F (usano solo σ(T) ⊂ {0} ∪ [γ_N, ‖S‖²] e, per γ_N = 0, l'iniettività di T su (ker S)^⊥). Solo l'identità γ = 1−c_F è specifica di N = 2.
- **T3-2** (MINOR) Tabella (e): indicare che ogni riga eredita lo stato della fonte di c_F (C12-P4(a),(b), C12-P8, C12-T3); qui è ricontrollata solo la formula tanh della riga c = 0.
- **L1-1** (MINOR) Ipotesi Q ≠ 0; una riga sull'iniettività H^σ(Ω) → 𝒟′(Ω) per σ < 0 (densità di C_c^∞ in H_0^{−σ}), usata per passare da "Q(∂)v = 0 in 𝒟′" a "= 0 in H^{m−k}" e in T2(a).
- **T2-1** (facoltativo) Prova di (a) in una riga: Q − g ∈ (τ−a)R (si annulla su τ = a(ξ)).
- **T2-2** (MINOR) In (c): "per ogni R che soddisfa le ipotesi di P2-T1 il residuo limite è E^⊥(u); per **ogni** R, ‖r_α‖ ≥ ‖E^⊥(u)‖".
- **T2-3** (MINOR, stato) Sostituire "P1-P2(c) prova scritta, audit in attesa" con "P1-P2(c), P1-L1 DIMOSTRATO (S-CHECK-3, PASS-con-fix)". Aggiungere la nota T2.7: la dipendenza analitica non è eliminabile con la sola algebra degli ideali J_n.
- **T4-1** (MINOR, applicazione (i)) Enunciare T4 anche per Φ: V → Y qualsiasi con Lip(Φ) ≤ liminf L_α, e aggiungere: ogni selezione esatta σ di S ha Lip(σ) ≥ ‖S^†‖. Solo così (i) copre ℓ¹, MCA e ogni selezione non lineare.
- **T5-1** (MINOR) Riportare nella CHECK_REQUEST/enunciato le definizioni di Λ_j, δ, μ_c, κ (ora solo nel "Richiamo" del §8) e precisare che in (ii) Φ₁ non deve essere un frame di H.
- **T5-2** (MINOR) In (iv): "gli split supportati sui grappoli sono ⊥ ℐ; con Λ_j = indici di ℋ_j⊖ℐ, ogni split con u_j ⊥ ℐ (coefficienti ℓ¹) è l'unico minimizzatore (f(z) = f(0)+2‖z‖₁)".
- **C1-1** (MINOR) Definire E^{fatt}_{L²}(u) ≠ 0 come "u ∉ ℋ₁+ℋ₂".
- **P3-1** (facoltativo) Notazione S^†u per la preimmagine di norma minima con im S non chiusa.
- **P5-1** (MINOR) Definire \|a_n\|(ρ′) (o rimandare esplicitamente a P1-L2).

## 5. Red team (Phase 1.5) — esito (audit_p2.py, 72/72 OK)
1. **T3, formula spettrale**: 6 coppie (reali e complesse, dim ℐ ∈ {0,1,2,3}, dimensioni diverse): dim ker S = dim ℐ; min σ su (ker S)^⊥ = 1−c_F (c_F da angoli principali tra A e B); max = 2 se ℐ ≠ 0, 1+c_F altrimenti; spettro di K simmetrico; sup_α‖R_α‖ = (1−c_F)^{−1/2}; (d) con uguaglianza sull'autovettore; ‖S^+‖ = (1−c_F)^{−1/2}. Un caso con c_F ≈ 1−9·10⁻⁵ (dim 3 e 5 in ℝ⁸) passa.
2. **T3, c_F = 1**: somma diretta di blocchi 2D con angolo θ_k = 2^{−k}: sup_α‖R_α‖ ≥ 1/(2√λ_k) fino a ≈ 2.9·10³.
3. **N ≥ 3 (O-1)**: tre rette a 120° in ℝ²: γ₃ = 1.5 mentre 1−max c_F = 0.5; tre rette quasi complanari in ℝ³ (inclinazione ε): c_F a coppie ≈ 0.5 e γ₃ ≈ ε²/3 → 0. Somma diretta ortogonale dei blocchi con ε_k → 0: tre sottospazi chiusi con intersezioni nulle, **somme a coppie chiuse (c_F ≈ 1/2)** e somma tripla **non chiusa**. Viceversa la somma tripla può essere chiusa con una coppia non chiusa (ℋ₃ = H). I c_F a coppie non decidono nulla per N ≥ 3.
4. **T2**: identità Q(∂)u = g(∂_x)u sui modi (AD, tre termini) e come identità operatoriale Q − g = (τ−a)τ (N = 2); K = Σdeg(a−a_n); ogni radice di g in una classe; base AD e scomposizione esplicita; 𝔍 ≠ J₁∩J₂ (Gröbner).
5. **T5**: 300 istanze in ℝ⁸ (ℐ di dim 1, basi o.n. ruotate): stima DK su ogni minimizzatore (κ < 1/2 in 48 istanze); NSP ⟹ unicità; NSP falsa ⟹ il controesempio della prova funziona; basi adattate.
6. **P7, P2, P4(b), P5(b), P6, T4**: vedi tabelle (esatti dove possibile).
Candidati controesempio cercati e non trovati: violazione di T3(b) con ℐ ≠ 0 di dimensione > 1; violazione della stima 2δ/(1−2κ); NSP vera con minimizzatore non unico.

## 6. Portata (scientific-critical-thinking)
- **O-1 (MAJOR di portata, esterno ai claim di S-P2: C12-P7, gram.md, PROBLEM.md G★′ punto 2).** "Le componenti stanno in H^m per ogni u ⟺ la somma è chiusa (⟺ c_F < 1) e densa": l'equivalenza "chiusa ⟺ c_F < 1" è un fatto su **due** sottospazi. Con N ≥ 3 fattori primari c_F non è definito, e i c_F a coppie non sono né necessari né sufficienti (red team 3). Proposta di testo: "… ⟺ la somma dei nuclei è chiusa e densa in ker_{H^m}P; la chiusura equivale a γ_N := inf σ(S*S|_{(ker S)^⊥}) > 0, e per N = 2 a c_F < 1 (P2-T3)". Il resto di G★′ punto 2 non cambia. Da sottoporre all'utente insieme alla precisazione "densa" già segnalata.
- **O-2.** P2-T3(b) chiude anche, con costanti, l'equivalenza della norma di Aronszajn con quella di H sulla somma (due sottospazi).
- **O-3.** Mostrato vs affermato: P2-T2 è un teorema su H^m(Ω) con Ω rettangolo e dizionario (T) = nuclei dei termini **di evoluzione** ∂_t − a_n(∂_x); con le classi "pure" ker a_n(∂_x) la conclusione B8 resta (osservazione di P2-P2, verificata). B8 "falso salvo uno spazio di dimensione K" è quindi dimostrato per questi due dizionari, non per dizionari arbitrari.
- **O-4.** P2-C1(b) lascia APERTO quale alternativa valga per m ≥ 1 (P2-Q1): corretto non dichiararlo.

## 7. Acceptance gate
1. Zero FATAL/CRITICAL aperti: **sì**.
2. Ipotesi esplicite e interscambi giustificati: sì dopo L1-1, T5-1, C1-1, P5-1 (definizioni mancanti nel testo autosufficiente); scarichi delle dipendenze: F5 e P1-P1(e) ora DIMOSTRATO (S-CHECK-3).
3. Uniformità dichiarate: T3(c) (sup su α non raggiunto), T4 (liminf su α → 0), T5(ii) (costante 2/(1−2κ)): sì.
4. Red team eseguito su tutti i claim chiave: sì (§5).
**Esito: PASS** per tutti i claim, con i fix MINOR elencati; una correzione di portata (O-1) per C12-P7/G★′ con N ≥ 3.
