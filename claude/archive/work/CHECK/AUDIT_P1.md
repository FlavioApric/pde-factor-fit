# AUDIT P1 — struttura di E_int (claim di S-P1)
Revisore: S-CHECK-3 (3ª tornata) · 25/10/2026
Fonte esaminata: `work/P1/CHECK_REQUEST.md` (per intero). **Riferimenti puntuali dichiarati** a `work/P1/PROOF_PACKAGE.md`, solo per i claim che la CHECK_REQUEST non riporta ma che il coordinatore ha chiesto di auditare: §4 P1-D2 (definizione, righe 80–85), §4 P1-E1 (righe 133–136, solo lettura), §5 P1-T3 (righe 141–157), §6 P1-P3 (righe 183–188), §8 P1-P5 e P1-C1 (righe 241–249). Nessun'altra parte del PROOF_PACKAGE è stata letta (in particolare non §10 kill-argument né i commenti dell'autore).
Lemmi esterni usati come dati (LEDGER, DIMOSTRATI): C12-T1 (rettangolo), C12-T2(i), C12-L1, C12-P1(b), II-L1, II-T7(a); R5-T2(i–iii) su Banach.
Skill caricate (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-checker (il reviewer sono io: Phase 0.5 enunciati canonici e micro-claim, checklist A–H, Phase 1.5 red team, severità a due assi, acceptance gate; niente Codex/LaTeX), scientific-critical-thinking (separare ciò che è dimostrato da ciò che è affermato nelle "Letture"; stato proporzionato), sympy.
SymPy: `work/CHECK/sympy/audit_p1.py` → `audit_p1.out` (esito in §5).

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| P1-P1(e) (E^add non continua in H^m(Ω), AD) | **PASS-con-fix(P1e-1, P1e-2)** — rafforzabile a ogni t₀ ∈ Ī | DIMOSTRATO |
| P1-P1(a),(c),(d) | **PASS-con-fix(P1a-1)** | DIMOSTRATO |
| P1-P1(b) (Tychonoff) | **PASS-con-fix(P1b-1)** | CON-FONTE (F. John cap. 7; numero di pagina da CIT-AUDIT) |
| P1-L1 | **PASS-con-fix(L1-1, L1-2)** | DIMOSTRATO |
| P1-L2 | **PASS** | DIMOSTRATO |
| P1-L3 | **PASS-con-fix(L3-1, L3-2)** | DIMOSTRATO |
| P1-T2 (i)–(v) | **PASS-con-fix(T2-1, T2-2)** | DIMOSTRATO (classe 𝔅) |
| **R5-T2[H1]** | — | **FALSO nella forma H^m** (come estensione continua: controesempio AD, P1-P1(e)); **vero in 𝔅** (P1-T2) → proposta di sdoppiamento della riga, §4 |
| P1-T5 | **PASS-con-fix(T5-1, T5-2, T5-3)** | DIMOSTRATO |
| P1-C1 (R5-Q5 falsa) | **PASS-con-fix(C1-1, C1-2)** | R5-Q5 **FALSO** (come scritta) |
| P1-L5 | **PASS** | DIMOSTRATO |
| P1-T3 | **PASS-con-fix(T3-1, T3-2)** | DIMOSTRATO (nel modello di costo dichiarato) |
| P1-P4 | **PASS-con-fix(P4-1, P4-2, P4-3, P4-4)** | DIMOSTRATO; coerente con II-T7(e′)/II-T7-cons |
| P1-T4 | **PASS** (teorema di Lie CON-FONTE) | DIMOSTRATO (+ CON-FONTE Humphreys §4.1 Cor. A) |
| P1-P5 | **PASS** | DIMOSTRATO |
| P1-P6 | **PASS-con-fix(P6-1, P6-2)** | DIMOSTRATO (generatori standard CON-FONTE) |
| P1-L4 | **PASS** | DIMOSTRATO |
| P1-P2 (a)–(c) | **PASS-con-fix(P2-1, P2-2)** | DIMOSTRATO |
| P1-P3 | **PASS-con-fix(P3-1)** | DIMOSTRATO |

Nessun rilievo FATAL, CRITICAL o MAJOR. Tutti i rilievi sono MINOR (precisione, citazioni, portata delle "Letture"). Due osservazioni di portata (§3): **O-1** P1-P1(e) vale per **ogni** t₀ ∈ Ī, non solo t₀ = 0 (verificato); **O-2** l'ipotesi "flussi di Y spenti a ε = 0" in P1-T5 è usata in modo essenziale dalla prova; se si possa togliere è APERTO (nuovo P1-Q7 proposto).

## 1. Enunciati canonici (Phase 0.5)
- **𝔅.** B_ρ(J) = {f ∈ C^∞(J): sup_j ρ^{−j}‖f^{(j)}‖_{L²(J)} < ∞}; 𝔅_ρ(Ω) analogo con ∂_t^i∂_x^j; J, I limitati.
- **P1-L3(a).** ∀A ∈ ℂ[ξ], ∀ρ > 0, ∀t₀ ∈ Ī, ∀v ∈ C(Ī;B_ρ): (∂_t − A(∂_x))v = 0 in 𝒟′(Ω) ⇒ v ∈ C¹(Ī;B_ρ) e v(t) = e^{(t−t₀)A(∂)}v(t₀) ∀t ∈ Ī.
- **P1-T2.** ∀u ∈ 𝔅_ρ(Ω) ∩ ker(τ − Σ_n a_n), ∀t₀ ∈ Ī, ∀ρ′ > ρ: (i) ∃! u_n ∈ 𝔅 con (∂_t − a_n)u_n = 0, u_n(t₀) = u₀; (ii) u(t) = Σ_S Π_{n∈S}(e^{(t−t₀)a_n} − I)u₀ in B_{ρ′} ∀t ∈ Ī, E^mult ≡ 0; (iii) forma spettrale per u₀ = ∫e^{ζx}dμ₀, supp μ₀ compatto; (iv) ∀u ∈ C^∞(Ω) ∩ ker Q, ∀t₀ ∈ I: identità nel getto formale.
- **P1-P1(e).** Q = τ + cξ − Dξ², c, D > 0, I = (0,T), t₀ = 0: ∀m ∈ ℕ, sup{‖E^add‖_{L²(Ω)}/‖u‖_{H^m(Ω)} : u EP, Qu = 0, u ≠ 0} = +∞.
- **P1-T5.** 𝒜 ℂ-algebra associativa unitaria; X, Y ∈ 𝒜 con (H): {X, Y₀, Y₁, …} linearmente indipendente. ∄ d ∈ ℕ, ∄(Z_1..Z_d) ∈ {X,Y}^d, ∄ g_i olomorfe su un polidisco U ∋ (0,0) con g_i(0,ε) = 0 e (Z_i = Y ⇒ g_i(·,0) ≡ 0), tali che ∀ε con (0,ε) ∈ U: e^{t(X+εY)} = Π_i e^{g_i(t,ε)Z_i} in 𝒜[[t]].
- **P1-P4(c).** ∀ρ′ > 0: T*(ρ′) := sup{T: φ₁(t;ζ) ≠ 0 ∀|t| ≤ T, |ζ| ≤ ρ′} ≥ log2/K(ρ′); ∀|t| < T*: fattorizzazione di Gauss di e^{tC(∂_x)} in Mat₂(𝒞).
- **P1-P6.** X = L²(0,L), c, D > 0: ∀t ≥ L/c, S₁(t)S₂(t) = S₂(t)S₁(t) = 0 e S(t) iniettivo.

## 2. Micro-claim ed esiti per passo

### 2.1 P1-P1(e) (priorità 1)
| MC | passo | esito |
|---|---|---|
| e.1 | u_ζ = e^{a(ζ)t+ζx}, a = Dζ² − cζ, è in ker Q | OK (SymPy P1e.1) |
| e.2 | flussi per termine (in 𝔅, P1-T2(i)): u₁ = e^{−cζt}u₀, u₂ = e^{Dζ²t}u₀; E^add = z₁z₂e^{ζx} | OK (P1e.2) |
| e.3 | ‖u_ζ‖²_{H^m} ≤ C_m(1+ζ)^{4m}T e^{2aT}e², usando a^{2i}ζ^{2j} ≤ D^{2i}ζ^{4i+2j}, a > 0 per ζ > c/D | OK; **C_m dipende da D** (e da m), non è universale → **P1e-1** (MINOR) |
| e.4 | \|z₁\| ≥ ½ ⟸ cζt ≥ log2 ⟸ t ≥ T/2, ζ ≥ 2log2/(cT) | OK |
| e.5 | \|z₂\| = e^{Dζ²t} − 1 ≥ ½e^{Dζ²t} ⟺ Dζ²t ≥ log2 ⟸ t ≥ T/2, ζ² ≥ 2log2/(DT) | OK (domanda specifica: condizione corretta, direzione giusta) |
| e.6 | per ζ^{−2} ≤ T/2: ∫_{T−ζ^{−2}}^T e^{2Dζ²t}dt ≥ ζ^{−2}e^{−2D}e^{2Dζ²T}, quindi ‖E‖² ≥ e^{−2D}e^{2Dζ²T}e²/(16ζ²) | OK (SymPy P1e.5, ζ = 3, 6, 12) |
| e.7 | rapporto dei quadrati ≥ c_m ζ^{−2}(1+ζ)^{−4m}e^{2(Dζ²−a)T} = c_m ζ^{−2}(1+ζ)^{−4m}e^{2cζT} → ∞ | OK (P1e.3: esponente esatto 2cζT; P1e.4 numerico) |
| e.8 | E^add lineare su 𝔅 ∩ ker Q, illimitata H^m → L² ⇒ nessuna estensione continua a ker_{H^m}Q, qualunque sia la densità | OK (una mappa lineare illimitata su un sottospazio non si estende per continuità alla chiusura) |
| e.9 | portata: il controesempio vale per t₀ = 0 | OK come scritto; **vale per ogni t₀ ∈ Ī** → **O-1**, fix facoltativo **P1e-2** |

### 2.2 P1-P1(a)–(d)
| MC | passo | esito |
|---|---|---|
| a.1 | in (t, y = x+t) l'equazione diventa w_t = 0 sul parallelogramma {0<t<T, a+t<y<b+t}; le sezioni in t sono intervalli | OK. La citazione "C12-L1" è impropria (C12-L1 è sul rettangolo); per v liscia basta il calcolo elementare → **P1a-1** (MINOR) |
| a.2 | v = F(x+t), F ∈ C^∞((a,b+T)) estensione liscia di f; libera su (b,b+T) | OK |
| b.1 | soluzione di Tychonoff liscia su Ω̄, v(0,·) = 0, v ≢ 0 | CON-FONTE (classica). "Dimensione infinita" non è argomentata: basta la famiglia v_σ(t,x) = v(t−σ,x), σ ∈ (0,T), linearmente indipendente (supporti in t che iniziano in σ) → **P1b-1** (MINOR) |
| c.1, d.1 | non-unicità fuori da 𝔅; in 𝔅 unicità (P1-T2(i)); u₀ = 0 ma v ≠ 0 per τ − ξ² | OK (la v di (b) non sta in 𝔅, coerente con P1-L3(a)) |

### 2.3 P1-L1, P1-L2, P1-L3
| MC | passo | esito |
|---|---|---|
| L1.a | completezza: limiti g_j in L², g_{j+1} = g_j′ in 𝒟′, g₀ ∈ H^∞ ⊂ C^∞ | OK (anche in 2D: H^∞(Ω) ⊂ C^∞(Ω), Sobolev su rettangolo) |
| L1.b | ‖u‖²_{H^m} ≤ C(m+2,2)·max(1,ρ)^{2m}‖u‖² | OK |
| L1.c | ‖∂^j(x^le^{ζx})‖ ≤ C_l(1+j)^l max(\|ζ\|,η)^j η^{−l} | OK a meno della costante: per η ≥ 1 il fattore corretto è max(1,η^{−l}) → **L1-1** (MINOR) |
| L1.d1 | H¹(I;L²(J)) ↪ C(Ī;L²(J)) con C_I = max(\|I\|^{−1/2},\|I\|^{1/2}) | OK (media in s e Cauchy–Schwarz) |
| L1.d2 | identificazione del rappresentante continuo con u(t,·) per t ∈ I, e u(t) ∈ H^∞(J) agli estremi | OK ma implicito: per t ∈ I vale u(t,x) − u(s,x) = ∫_s^t∂_tu puntualmente; agli estremi i limiti in L² delle ∂_x^ju(t) sono le derivate del limite (chiusura) → **L1-2** (MINOR, una riga) |
| L1.d3 | continuità in B_{ρ′} con ρ′ > ρ (coda (ρ/ρ′)^j uniforme) | OK (domanda specifica: tracce corrette) |
| L2.1 | ‖A(∂)‖ ≤ \|A\|(ρ); serie esponenziale in 𝓛(B_ρ); commutazione e e^{X+Y} = e^Xe^Y | OK |
| L2.2 | ζ ↦ e_ζ ∈ B_ρ olomorfa per \|ζ\| < ρ (stima Σ_j(\|ζ\|/ρ)^je^{\|ζ\|R}) | OK; la somma in B_ρ coincide con e^{ζx} via B_ρ ↪ L² |
| L2.3 | e^{sA}(x^le_ζ) = ∂_ζ^l(e^{sA(ζ)}e_ζ) | OK (SymPy L2c.1 per A = −cξ + Dξ³, l = 2, k ≤ 4) |
| L3.a1 | test φ⊗ψ, integrazione per parti in x (ψ a supporto compatto), F := −∫φ′v − ∫φA v ∈ B_ρ (Bochner) con ⟨F,ψ⟩ = 0 ∀ψ ⇒ F = 0 | OK (domanda specifica: il passaggio 𝒟′(Ω) → 𝒟′(I;B_ρ) è corretto; serve solo la classe dei test prodotto, che è contenuta in quella di 𝒟(Ω); ψ ↦ ⟨·,ψ⟩ è continuo su B_ρ e commuta con Bochner) |
| L3.a2 | derivata distribuzionale a valori in B_ρ nulla ⇒ costante (Hahn–Banach); v ∈ C¹(Ī) | OK; se t₀ ∈ ∂I serve la continuità su Ī di w(t) = v(t) − v(t₀) − ∫_{t₀}^tAv: costante su I, quindi su Ī → **L3-2** (MINOR, esplicitare) |
| L3.a3 | w(t) = e^{−(t−t₀)A}v(t) ha derivata nulla | OK |
| L3.b | v(t) = e^{(t−t₀)A}f è C^∞ in t a valori B_ρ; stima 𝔅_{ρ″} | OK per la stima; manca la riga "v è C^∞ congiuntamente su Ω" (da B_ρ ↪ C^k(J̄) per ogni k: C^∞(Ī;C^k(J̄)) ∀k ⇒ C^∞(Ω̄)) → **L3-1** (MINOR) |
| L3.c | sistemi, norma di riga massima | OK |

### 2.4 P1-T2 (priorità 1)
| MC | passo | esito |
|---|---|---|
| T2.i1 | u ∈ C(Ī;B_{ρ′}) (L1(d)); L3(a) con A = a ⇒ u(t) = e^{(t−t₀)a}u₀ | OK |
| T2.i2 | esistenza u_n ∈ 𝔅 (L3(b)); unicità: v ∈ 𝔅_{ρ₁} ⇒ L3(a) in B_{ρ₂}, ρ₂ > max(ρ₁,ρ′); L2(b) | OK |
| T2.ii | e^{(t−t₀)a} = Π_n e^{(t−t₀)a_n}; sviluppo del prodotto di elementi che commutano; |S| ≤ 1 dà u₀ e u_n − u₀; regolarità via L3(b) | OK |
| T2.iii | u₀ = ∫e_ζ dμ₀ come Bochner in B_{ρ′} | OK se ρ′ > max(ρ, r): la prova ri-sceglie ρ′ "> r" senza dirlo; la continuità di ζ ↦ e_ζ ∈ B_{ρ′} su {\|ζ\| ≤ r} segue dall'olomorfia su \|ζ\| < ρ′ (L2(c)); l'integrale di Bochner coincide con quello puntuale (accoppiamento con ψ, Fubini) → **T2-1** (MINOR; domanda specifica: sì, la continuità vale) |
| T2.iv1 | ∂_t^ku = a(∂_x)^ku per u liscia in ker Q | OK |
| T2.iv2 | exp(X+Y) = expX·expY per X, Y ∈ s·End[[s]] commutanti; coefficiente multinomiale con ≥ 2 indici positivi | OK (SymPy T2iv.1, T2iv.2, N = 3, k ≤ 6) |
| T2.iv3 | per u ∈ 𝔅 la serie è Taylor della funzione intera s ↦ E^add(t₀+s) | OK (l'estensione intera coincide con E^add su Ī) |
| T2.port | "(A) la limitatezza di Ω non ha alcun ruolo nella prova" | sovradimensionato: L1(c), L1(d) usano \|I\|, \|J\| < ∞ (gli EP stanno in L² solo su J limitato). Non cambia la tesi → **T2-2** (MINOR, riformulare: "non ha ruolo nell'identità algebrica; entra solo nella definizione della classe") |
| T2.v | I-1, I-2(a), I-2(b) dell'audit R5-T2 soddisfatte in 𝔅 | OK |

### 2.5 P1-T5 e P1-L5 (priorità 2)
| MC | passo | esito |
|---|---|---|
| L5.a–d | lemmi formali in 𝒜[[t]] | OK (SymPy L5b con g = t + t², matrici 3×3 non commutanti) |
| T5.0 | e^{gZ} ben definito: g_i(·,ε) ∈ tℂ{t} | OK (g_i(0,ε) = 0) |
| T5.1 | ε = 0: e^{(G−t)X} = 1 ⇒ G = t (coefficiente di t^m, X ≠ 0) | OK (SymPy T5.p1). Usa in modo essenziale g_i(·,0) ≡ 0 per Z_i = Y |
| T5.2a | derivata in ε coefficiente per coefficiente | OK: il coefficiente di t^m di ciascun membro è combinazione, con coefficienti olomorfi in ε (polinomi nei coefficienti di Taylor g_{i,k}(ε), k ≤ m), di parole di lunghezza ≤ m in X, Y: vive in un sottospazio di dimensione finita, dove derivare è lecito. Va scritto → **T5-2** (MINOR; domanda specifica 1: sì) |
| T5.2b | Duhamel formale: ∂_εe^{t(X+εY)}\|₀ = e^{tX}Σ_k(−1)^kt^{k+1}/(k+1)!·Y_k | OK (SymPy T5.duh, coefficienti t⁰..t⁵, matrici generiche) |
| T5.2c | membro destro: fattori X danno rXe^{tX}; fattori Y danno q_ie^{G_iX}Ye^{(t−G_i)X} (solo perché g_i(t,0) = 0 ⇒ ∂_εe^{g_iY}\|₀ = q_iY) | OK |
| T5.3 | coefficiente di t^m coinvolge solo X, Y₀..Y_m (q_iτ_i^k ∈ t^kℂ[[t]]); (H) ⇒ r = 0 e Σq_iτ_i^k = t^{k+1}/(k+1) ∀k; germi convergenti su disco comune ⇒ uguaglianza di funzioni | OK (domanda specifica 2: corretto; i q_i, τ_i sono un numero finito di germi convergenti) |
| T5.4 | Hankel: H_n = WᵀD_qW ha rango ≤ p; H_n = t·diag(t^i)·Hilb_n·diag(t^j) ha rango n per t > 0 (Hilbert = Gram, def. pos.); n = p+1; p = 0 separato | OK, completo (SymPy T5.hank n ≤ 6; T5.rank p = 1,2,3 con atomi complessi; domanda specifica 3: sì) |
| T5.H | esempio X = x^a∂, Y = ∂: ad_X(x^b∂) = (b−a)x^{a+b−1}∂, Y_k = c_kx^{k(a−1)}∂, c_k = Π_{j<k}(j(a−1)−a) ≠ 0 per a ≥ 3 (a−1 ∤ a); gradi distinti e ≠ a ⇒ (H) | **OK** (SymPy T5.H per a = 3,4,5, k ≤ 7: formula di c_k esatta, gradi 0, a−1, 2(a−1), … distinti e mai uguali ad a; i monomi x^n∂ sono indipendenti in A₁). Per a = 2: Y₁ = −2x∂, Y₂ = 2x²∂, **Y₃ = 0** (c₃ contiene 2(a−1)−a = 0): l'orbita è finita (il testo dice solo "finita", corretto) |
| T5.hyp | ipotesi "flussi di Y spenti a ε = 0" | usata in T5.1 e T5.2c; **non** ridondante per la prova. Non trovo né una prova senza di essa né un controesempio: è APERTO → **O-2** (domanda specifica 4) |
| T5.prec | precisione di "flussi dei termini" e "tempi analitici" | "flussi dei termini" = fattori e^{gZ} con Z ∈ {X, Y} esattamente (le costanti λ_n si assorbono nei tempi): preciso. "Tempi analitici" = g_i olomorfe congiuntamente in (t,ε) su un intorno di (0,0): preciso; va detto che il polidisco è comune e che l'identità vale ∀ε di un intorno fisso → **T5-1** (MINOR). La "Lettura" su 𝔈^mult richiede un passo in più: se 𝔈^mult = Π e^{h_iZ_i} con h_i(·,0) ≡ 0 per Z_i = Y, allora e^{t(X+εY)} = e^{tX}e^{tεY}Π e^{h_iZ_i} è della forma esclusa (il tempo tε del fattore Y si annulla a ε = 0) → **T5-3** (MINOR, scriverlo) |
| T5.port | (H) falsa per ⟨∂², x^k⟩ (ad localmente nilpotenti) | OK |

### 2.6 P1-C1 (riferimento puntuale PROOF_PACKAGE §8)
| MC | passo | esito |
|---|---|---|
| C1.1 | "𝔈^mult(t) = e^{−tT₁}e^{t(T₁+T₂)}" | **ERRORE di scrittura**: per D3(c) 𝔈^mult = (e^{tT₁}e^{tT₂})^{−1}e^{tA} = e^{−tT₂}e^{−tT₁}e^{t(T₁+T₂)}; la formula scritta manca il fattore e^{−tT₂} ed è falsa se [T₁,T₂] ≠ 0 (SymPy C1.1 con matrici nilpotenti 2×2) → **C1-1** (MINOR: la conclusione resta, con 3 esponenziali nello span; SymPy C1.2) |
| C1.2 | ambiente in cui e^{−tT_n} esiste | in 𝒜[[t]] o per termini che generano gruppi; per termini parabolici su L² (e^{−t∂²}) l'inverso non esiste come operatore → **C1-2** (MINOR: dire "nel quadro formale"). R5-Q5 come scritta è FALSA: confermato |

### 2.7 P1-T3 (riferimento puntuale PROOF_PACKAGE §5)
| MC | passo | esito |
|---|---|---|
| T3.1 | modello: dato EP (ζ_k, p_k), deg p_k ≤ L; costo unitario per operazioni in ℂ e per exp | dichiarato; è un modello real-RAM con oracolo exp (nessuna complessità in bit) → **T3-2** (MINOR, portata) |
| T3.a | traslazione di Taylor O((L+1)(d_n+1)); exp troncato O((L+1)²); prodotto di N serie O(N(L+1)²); ∂_ζ^l e lettura O((L+1)²) | OK; somma = O(M[N(L+1)² + (L+1)Σ(d_n+1)]) |
| T3.b | DP su Π(1+λz_n): O(N²(L+1)²) per esponenziale | OK (SymPy T3.1: DP = forza bruta, N = 7) |
| T3.c | tabella {c_S}: M(2^N−N−1) voci, Ω(M2^N), raggiunto | OK per L = 0; per L > 0 ogni voce è una serie troncata e il costo raggiunto è Θ(M2^N(L+1)²) → **T3-1** (MINOR) |
| T3.d | "O(eⁿ)" falso per valore e aggregati, vero solo per la tabella | OK, coerente con R5-T2(iv) ristretto del LEDGER |

### 2.8 P1-P4 (coerenza con II-T7)
| MC | passo | esito |
|---|---|---|
| P4.a | U = (u,∂_tu), L1(d) + L3(c); e^{tC(ζ)} = [[φ₁,φ₂],[φ₁′,φ₂′]]; sostituzione ζ ↦ ∂_x termine a termine con maggiorante Σ\|t\|^k\|C\|(ρ′)^k/k! | OK |
| P4.b | σ_𝒞(∂_x) ⊂ {\|ζ\| ≤ ρ′}; 1/f olomorfa vicino al disco; calcolo funzionale (Rudin FA 10.27) | OK. Si può evitare la citazione: in 𝒞 commutativa, f(∂) è invertibile ⟺ nessun carattere χ lo annulla, e χ(f(∂)) = f(χ(∂)) ≠ 0 perché χ(∂) ∈ σ_𝒞(∂) (la sostituzione in serie commuta con i caratteri, che sono continui) → **P4-1** (MINOR; domanda specifica: corretto) |
| P4.c1 | \|φ₁−1\| ≤ e^{\|t\|K} − 1; T* ≥ log2/K; inf\|φ₁\| ≥ 2 − e^{TK} | OK |
| P4.c2 | Gauss 2×2 su anello commutativo con φ₁ invertibile; det = e^{−tb} (Liouville) | OK (SymPy P4.1) |
| P4.c3 | log continuo in t, olomorfo in ζ, come elemento di 𝒞 | OK con un passo da scrivere: per compattezza φ₁(t;·) non si annulla su un disco \|ζ\| < ρ″ con ρ″ > ρ′ (uniforme per \|t\| ≤ T < T*), il ramo h₁(t;·) è olomorfo lì, la sua serie di Taylor converge con raggio > ‖∂_x‖ e definisce h₁(t;∂) ∈ 𝒞 con e^{h₁(∂)} = φ₁(∂); la continuità t ↦ h₁(t;∂) in norma segue dalla convergenza uniforme delle serie su \|ζ\| ≤ ρ‴ ∈ (ρ′,ρ″) (stime di Cauchy) → **P4-2** (MINOR; domanda specifica: corretto) |
| P4.c4 | "Questo è E^mult_int per un fattore del 2° ordine" | impreciso: è una forma chiusa del propagatore (coordinate di Wei–Norman); 𝔈^mult = (Π e^{tλ_nT_n})^{−1}·(forma di Gauss) → **P4-3** (MINOR, lessico) |
| P4.c5 | t reale o complesso in T* | non specificato; il bound e il caso onda valgono in entrambi i casi (per l'onda il primo zero minimo è a \|ζt\| = π/2 in ζ = iρ′) → **P4-4** (MINOR) |
| P4.d | onda: T* = π/(2ρ′) | OK |
| P4.coer | coerenza con II-T7(e′)/II-T7-cons (LEDGER: II-T7(e) vero solo per p reale; KG locale sui modi reali \|cξ\| < m, t* = π/(2√(m²−c²ξ²))) | **coerente**: P1-P4 non afferma globalità, solo un tempo uniforme su un disco di modi. Per KG, T*(ρ′) = π/(2√(m²+c²ρ′²)) (minimo in ζ = iρ′) ≤ t* di ogni modo reale del disco, e ≥ log2/K (SymPy P4.2, P4.3, m = 2, c = 1, ρ′ = 0.5, 1, 3). Nessun T uniforme sui modi di Fourier (II-T7) perché lì ρ′ = ∞ |

### 2.9 P1-T4, P1-P5
| MC | passo | esito |
|---|---|---|
| T4.a | Lie: catena di ideali con quozienti di dimensione 1 | CON-FONTE: Humphreys, *Introduction to Lie Algebras…*, §4.1 Cor. A (enunciato che ricordo identico: catena di ideali 0 = L₀ ⊂ … ⊂ L_n = L, dim L_i = i, per L risolubile su campo alg. chiuso di car. 0); numero da confermare in CIT-AUDIT |
| T4.b | Ad(P_{i−1})X_i triangolare con M_ii = exp(Σλ_jig_j); sistema triangolare risolto per quadrature; g_l intere | OK |
| T4.c,d | 𝔈^mult con d funzioni intere; identità di funzioni intere per operatori limitati | OK |
| T4.OU | g₁ = −t, g₂ = (1−e^{−2t})/2 | OK (SymPy T4.OU: e^{−tx∂}e^{g₂∂²}x^n risolve u_t = u_xx − xu_x con dato x^n, n ≤ 6) |
| P5.a | Wei–Norman locale: Ξ(0) = I, ODE analitica | OK |
| P5.b | sl₂, A = E − F: g₂₁ = −tan t | OK (SymPy P5.1) |

### 2.10 P1-P6
| MC | passo | esito |
|---|---|---|
| P6.1 | A₁ autoaggiunto ≤ 0 ⇒ contrazioni | OK (CON-FONTE standard) |
| P6.2 | A₂ inflow: risolvente, ‖R(λ)‖ ≤ 1/λ, trasformata di Laplace di S₂ = R(λ) ⇒ generatore A₂ | OK (SymPy P6.2). Per Hille–Yosida va detto che A₂ è chiuso e densamente definito (lo è) → **P6-1** (MINOR) |
| P6.3 | M A M^{−1} = D∂² − c²/(4D) con lo stesso dominio | OK (SymPy P6.1) |
| P6.4 | e^{tB} iniettivo (autovalori e^{tμ_k} ≠ 0 in base ON), S(t) = M^{−1}e^{tB}M iniettivo | OK |
| P6.5 | E^mult = S(t), errore relativo 1, 𝔈^mult non esiste | OK |
| P6.6 | (d) "il E^mult è creato interamente dalle condizioni al bordo" | lettura, non teorema (confronta spazi diversi) → **P6-2** (MINOR: marcarla come "Lettura") |

### 2.11 P1-L4, P1-P2, P1-P3
| MC | passo | esito |
|---|---|---|
| L4.1 | variazione delle costanti: r(∂)w = F | OK (SymPy L4.1, L4.2 per r = (ξ−1)(ξ−2), F = e^{2t+3x}(1+x²)) |
| L4.2 | N_j ≤ C₀‖F‖ per j < δ (\|x−y\| ≤ \|J\|) | OK |
| L4.3 | ricorrenza per j ≥ δ e induzione forte N_j ≤ KR^j | OK (le due metà ≤ KR^j/2 usano R ≥ 1, R ≥ ρ, R ≥ 2Σ\|r_l\|/\|ℓ\|) |
| P2.a,b | comassimale: u_j = E_j(∂)u ∈ 𝔅; 𝒩 ⊂ EP ⊂ 𝔅 | OK |
| P2.c1 | Vandermonde: Δ(∂_x)u_j = F_j ∈ 𝔅; L4 ⇒ w | OK |
| P2.c2 | ker_{𝒟′}Δ(∂_x) = 𝒟′(I)⊗V_Δ sul rettangolo | OK; l'induzione richiede, oltre a ker ∂_x, una soluzione particolare di Δ′(∂_x)h = c(t)⊗e^{ρx}, che si prende tensoriale c(t)⊗φ(x) con φ ∈ V_Δ (ODE 1D con forzante EP) → **P2-1** (MINOR; domanda specifica: descrizione corretta) |
| P2.c3 | γ ∈ 𝔅 ∩ ker Δ(∂_x); biortogonali ψ_m; ‖γ_m^{(i)}‖ ≤ Cρ^i | OK |
| P2.c4 | c′ − Mc = γ, ĉ′ liscia ⇒ c liscia; c^{(i)} = M^ic + Σ M^{i−1−p}γ^{(p)}; ‖c^{(i)}‖ ≤ C′(2max(1,‖M‖,ρ))^i | OK (1+i ≤ 2^i). Se t₀ ∈ ∂I la formula integrale usa γ ∈ C(Ī), vero perché γ_m ∈ H^∞(I) → **P2-2** (MINOR; domanda specifica: stime corrette) |
| P2.c5 | h ∈ 𝔅, u_j = w + h ∈ 𝔅 | OK |
| P3.1 | cambiare scomposizione cambia E_int per termini di un elemento dell'immagine lineare di 𝒩 (dim ≤ δ(P)); in generale ≠ 0 | OK (SymPy P3.1: a₁ = ξ²+ξ in due termini, a₂ = 2ξ² in un termine, w = e^{2t+x} ∈ ker∩ker: E₁[w] = (e^s−1)²e^x ≠ 0). Scrivere "modulo l'immagine dell'applicazione lineare 𝒩 → ⊕_j, w ↦ (E_{int,j}[w_j])_j" → **P3-1** (MINOR) |

## 3. Osservazioni di portata (non difetti)
**O-1 (P1-P1(e) per ogni t₀).** Con t₀ ∈ Ī qualsiasi, E^add(t) = e^{at₀}z₁z₂e^{ζx} con z_n calcolati in s = t − t₀.
- t₀ < T: integrando su [T − ζ^{−2}, T] si ottiene il rapporto dei quadrati ≳ ζ^{−2}(1+ζ)^{−4m}e^{2cζ(T−t₀)} → ∞.
- t₀ = T (base finale): per ζ > 0, s < 0, z₁ = e^{cζ|s|} − 1 cresce e \|z₂\| → 1; il rapporto ≳ e^{2cζT}/poly(ζ) → ∞.
SymPy P1e.4 (c = D = T = 1, m = 2, t₀ = 0, 0.5, 1): rapporto crescente e > 10⁶ in ζ = 80. Fix facoltativo **P1e-2**: enunciare (e) per ogni t₀ ∈ Ī (la scelta del tempo base non salva la continuità).
**O-2 (ipotesi di P1-T5).** Senza "g_i(·,0) ≡ 0 per Z_i = Y" il Passo 1 non conclude (a ε = 0 compaiono fattori in Y) e il Passo 2 perde la forma q_iY. Ostacoli banali: parole con fattori Y adiacenti a tempi opposti si riducono; e^{gY} = 1 in 𝒜[[t]] forza g = 0 (stesso argomento del Passo 1), quindi la periodicità (e^{2πiY} = 1) non dà controesempi nel quadro formale. Non ho né prova né controesempio per il caso generale: proposta **P1-Q7 APERTO** ("P1-T5 senza l'ipotesi sui flussi di Y a ε = 0").

## 4. R5-T2[H1]: decisione proposta per il LEDGER
- La riga "R5-T2 su H^m(Ω) limitato" non è un enunciato preciso. Le due versioni precise sono ora decise:
  - **R5-T2[H^m] (FALSO):** "u ↦ E^add_int si estende per continuità da 𝔅 ∩ ker Q a ker_{H^m(Ω)}Q" è FALSO per l'avvezione–diffusione (P1-P1(e), DIMOSTRATO; per ogni m e, con O-1, per ogni t₀). Inoltre fuori da una classe di unicità i flussi per termine non sono nemmeno determinati (P1-P1(a)–(d)).
  - **R5-T2[𝔅] (DIMOSTRATO):** nella classe 𝔅 di tipo esponenziale su rettangolo limitato senza condizioni al bordo vale la formula esatta, con flussi per termine unici, E^mult ≡ 0, forma spettrale e getto formale (P1-T2).
- Il no-go generale (ogni Q con ≥ 2 termini non costanti) resta P1-Q6 APERTO: la riga FALSO è esistenziale (AD).

## 5. Red team SymPy (Phase 1.5)
Script `work/CHECK/sympy/audit_p1.py` → `audit_p1.out`. Esito: vedi coda di questo file (§5.1), aggiornato dopo l'esecuzione.
Tentativi di controesempio, tutti non riusciti salvo dove indicato:
- P1-P1(e): ricerca di t₀ che renda E^add limitata (t₀ = 0.5, 1): nessuno (O-1).
- P1-T5: (H) per a = 2 fallisce come previsto (Y₃ = 0); per a = 3,4,5 regge; Hankel con atomi complessi: rango ≤ p sempre.
- P1-C1: formula a due esponenziali falsa (trovato, C1-1), conclusione vera.
- P1-P4: KG con modi immaginari: T* esatto ≥ bound in tutti i casi.
- P1-P3: ambiguità non nulla trovata (conferma della tesi "in generale ≠ 0").

## 6. Fix proposti (tutti MINOR, da applicare da S-P1)
- **P1e-1** dichiarare C_m = C_m(D) in (e). **P1e-2** (facoltativo) enunciare (e) per ogni t₀ ∈ Ī (O-1).
- **P1a-1** sostituire "C12-L1" con il fatto elementare per funzioni lisce su un dominio con sezioni in t connesse. **P1b-1** argomentare "dimensione infinita" con le traslate v(t−σ,x).
- **L1-1** max(1,η^{−l}) al posto di η^{−l}. **L1-2** una riga sull'identificazione delle tracce con u(t,·) e sugli estremi.
- **L3-1** liscezza congiunta di v in (b). **L3-2** caso t₀ ∈ ∂I in (a).
- **T2-1** in (iii) scegliere esplicitamente ρ′ > max(ρ,r). **T2-2** riformulare "la limitatezza di Ω non ha ruolo".
- **T5-1** polidisco comune e intorno fisso di ε nell'enunciato; 𝒜 unitaria. **T5-2** giustificazione della derivata in ε per coefficiente (dimensione finita). **T5-3** scrivere il passaggio da 𝔈^mult all'enunciato nella "Lettura".
- **C1-1** 𝔈^mult = e^{−tT₂}e^{−tT₁}e^{t(T₁+T₂)}. **C1-2** precisare il quadro formale.
- **T3-1** costo della tabella Θ(M2^N(L+1)²) per L > 0. **T3-2** dichiarare "real-RAM con oracolo exp; nessuna complessità in bit".
- **P4-1** argomento con i caratteri al posto di Rudin 10.27 (o tenerlo come CON-FONTE). **P4-2** log in 𝒞 su disco più grande e continuità in t. **P4-3** "forma chiusa del propagatore", non "E^mult". **P4-4** dire se t è reale.
- **P6-1** A₂ chiuso e densamente definito. **P6-2** (d) come "Lettura".
- **P2-1** soluzione particolare tensoriale nell'induzione per ker Δ(∂_x). **P2-2** caso t₀ ∈ ∂I.
- **P3-1** "modulo l'immagine lineare di 𝒩".

## 7. Acceptance gate
0 FATAL / 0 CRITICAL; ipotesi esplicite e scaricate (con i fix MINOR); nessuna stima O(·) senza dipendenze dichiarate (P1-T3 nel suo modello); red team eseguito su tutti i lemmi chiave. Gate superato per tutti i claim della tabella §0.

### 5.1 Esito dell'esecuzione
`audit_p1.out`: **ESITO GLOBALE: OK (32/32)**. Rispetto alla prima esecuzione ho corretto tre test del revisore, non claim di S-P1:
- P1e.4: per t₀ = 0.5 il rapporto cresce come e^{cζ(T−t₀)}/ζ^{10}, quindi serviva ζ fino a 80;
- T5.H, caso a = 2: lo zero dell'orbita è Y₃, non Y₂;
- P5.1: confronto di exp(matrice) dopo rewrite(cos).
Rapporti misurati (c = D = T = 1, m = 2, ζ = 10, 20, 40, 80):
| t₀ | rapporti |
|---|---|
| 0 | 6.6 · 1.1e7 · 9.1e21 · 1.9e54 |
| 0.5 | 2.9e−4 · 2.2e−2 · 3.9e4 · 3.4e19 |
| 1 | 66 · 2.1e8 · 3.6e23 · 1.5e56 |
