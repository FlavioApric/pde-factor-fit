# AUDIT C12-C1, C12-L5, C12-T3, C12-T2
Revisore: S-CHECK-2C (2ª tornata, parte C) · 25/10/2026
Fonte esaminata: SOLO `work/C1C2/CHECK_REQUEST.md` (sezioni C12-C1, C12-L5, C12-T3, C12-T2). `work/C1C2/PROOF_PACKAGE.md` **non è stato letto**.
Skill caricate: le stesse di AUDIT_C12-T1.md (session-protocol, claim-lifecycle, proof-checker, scientific-critical-thinking, sympy). Nessuno script _vendor è stato eseguito.
SymPy: `work/CHECK/sympy/audit_c12.py` → `audit_c12.out`, sezioni C1, L5/T3, T2. **ESITO GLOBALE: OK (70/70).** Due controlli di C1 usano la quadratura `mpmath`, perché SymPy non chiude ∫e^{2s}log²s:
- la norma H² finita è ≈ 1.1206;
- la coda ∫_{s>ε}|∂_s²u_2|² cresce di 9.21 ≈ log 10⁴ tra ε = 10⁻⁴ e ε = 10⁻⁸.

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| C12-C1 (controesempio H^m) | **PASS** | DIMOSTRATO (quindi l'enunciato "la scomposizione conserva H^m" è FALSO) |
| C12-L5 (a)–(b) | **PASS-con-fix(L5-1)** | DIMOSTRATO |
| C12-T3 (a)⟺(b)⟺(c)⟺(d) + corollario | **PASS-con-fix(T3-1)** | DIMOSTRATO |
| C12-T2 (i)–(iv) | **PASS-con-fix(T2-1, T2-2)** | DIMOSTRATO |

Nessun rilievo FATAL, CRITICAL o MAJOR.

## 1. Enunciati canonici (Phase 0.5)
- **C1.** Ω = (0,1)², f = τ−ξ, g = τ−ξ−1. Per ogni m ≥ 0 esiste u ∈ H^m(Ω) ∩ C^∞(Ω) con fgu = 0, la cui scomposizione (unica) u = u_1+u_2 ha u_1, u_2 ∈ H^{m−1}∖H^m.
- **L5.** Sia D ⊂ ℝ²_{(s,r)} aperto convesso e φ ∈ 𝒟′(D) con ∂_rφ = 0. Allora esiste un'unica F ∈ 𝒟′(S) con φ = F∘pr_s. Se φ ∈ L²_loc, allora F ∈ L²_loc.
- **T3.** Sia Ω convesso limitato, c ∈ ℝ, d_1 ≠ d_2. Per i trasporti paralleli f, g, nelle coordinate (t, s = x−ct) le corde hanno lunghezza ℓ(s). Sono equivalenti: inf ℓ > 0 ⟺ stima L² delle componenti ⟺ ℋ_1+ℋ_2 chiuso ⟺ c_F < 1.
- **T2.** P = ∏(τ−a_j(ξ)) con a_j distinti. Valgono:
  - Δ(∂_x)u_j = Σ_l adj(V)_{jl}(∂_x)∂_t^lu;
  - δ(P) = deg Δ;
  - comassimale ⟺ Δ ∈ ℂ^×;
  - i proiettori della compagna sono Π_j = v_jw_j^T, polinomiali ⟺ comassimale, altrimenti con poli nelle collisioni.

## 2. Micro-claim ed esiti
### C12-C1
| MC | passo | esito |
|---|---|---|
| C1.1 | s = x+t: con ∂_t\|_x = ∂_t\|_s + ∂_s e ∂_x = ∂_s si ha f = ∂_t\|_s e g = ∂_t\|_s − 1. Il determinante è 1, quindi le norme H^m sono equivalenti | OK |
| C1.2 | Ω′ = {0<t<1, t<s<t+1}. Ω′_c = Ω′ ∩ {s<1} = {0<t<s<1}. Gli angoli (1,0), (0,1), (1,1) hanno s ∈ {1,2}, dove G è liscia | OK |
| C1.3 | fu = Ge^t e g(Ge^t) = 0. Siccome f − g = 1, si ha u_2 = fu = e^tG e u_1 = −gu = −G | OK (verificato nelle coordinate originali per m = 0..4) |
| C1.4 | stime: per k ≥ 1, ∫_0^s e^{2t} ≤ e²s; per k = 0, \|e^t−1\| ≤ et ⇒ ≤ e²s³/3. Si usano j ≤ m−1 con peso s e j ≤ m con peso s³ | OK (punto "da verificare" chiuso: con k = 0 e j = m basta il peso s³) |
| C1.5 | G^{(j)} = s^{m−1−j}(α_j log s + β_j) per j ≤ m−1, con α_{m−1} = (m−1)!, e G^{(m)} = (m−1)!/s | OK (verificato per m = 1..4) |
| C1.6 | finitezza di tutti gli integrali pesati (m = 0..4), e ‖u‖_{H²(Ω′_c)} con calcolo diretto | OK |
| C1.7 | ∫\|∂_s^mu_2\|² ≥ ∫\|G^{(m)}\|²s ds = ∞ (vale anche per m = 0). Poiché u ∈ H^m, segue u_1 ∉ H^m | OK |
| C1.8 | u_2 = f(∂)u ∈ H^{m−1}, perché ∂_j: H^σ → H^{σ−1} (per m = 0 vale con H^{−1} = (H¹_0)′) | OK |

### C12-L5
| MC | passo | esito |
|---|---|---|
| L5.1 | su ogni rettangolo Q ⊂ D si ha φ\|_Q = F_Q⊗1 (L1(a)) | OK |
| L5.2 | per s_0 ∈ pr Q_1 ∩ pr Q_2, il segmento verticale {s_0}×[r_1,r_2] è compatto e contenuto in D (convessità), quindi esiste un rettangolo sottile Q ⊂ D che lo contiene. Q∩Q_i è un rettangolo, e per l'unicità in L1(a) si ha F_Q = F_{Q_i} vicino a s_0 | OK (punto "da verificare" chiuso). La convessità serve **solo** per la connessione delle fette verticali |
| L5.3 | incollamento (Hörmander Thm 2.2.4) su S = ∪ pr Q; φ = F∘pr_s localmente, quindi globalmente; unicità | OK |
| L5.4 | (b) ∫φθ dr = F, e Cauchy–Schwarz dà F ∈ L²(s_a,s_b) | OK, ma serve **Q ⋐ D** perché φ ∈ L²(Q) → **L5-1** |

### C12-T3
| MC | passo | esito |
|---|---|---|
| T3.1 | ∂_t + c∂_x = ∂_t\|_s. Ω′ è convesso; ℓ = β − α è concava (β concava, α convessa) e continua sull'intervallo aperto S | OK (punto "da verificare" chiuso) |
| T3.2 | f − g = κ ⇒ u_2 = κ^{−1}fu e u_1 = −κ^{−1}gu, uniche (anche in 𝒟′) | OK |
| T3.3 | L5 nella versione torta dà u_i = e^{d_it}F_i(s) in 𝒟′. Il pairing con χ⊗η_i (η biortogonali su un intervallo di t) dà F = ∫u η_1 dt ∈ L²_loc | OK. È questo pairing, e non L5(b), a dare L²_loc: u_i non è noto in L²_loc |
| T3.4 | (a)⇒(b): la Gram Γ(α,β) è definita positiva e continua sul compatto {−M ≤ α, α+ℓ_0 ≤ β ≤ M}, quindi λ_min ≥ γ. Si integra per Fubini (Jacobiano 1) | OK (det Γ > 0 su campioni) |
| T3.5 | (b)⇒(c): ker_{L²}fg è chiuso (fg: L² → H^{−2} continua) e coincide con ℋ_1+ℋ_2 | OK |
| T3.6 | (c)⇒(d): ℋ_1 ∩ ℋ_2 = 0, mappa aperta, rotazione di fase ⇒ ‖x_k+y_k‖ → 0: assurdo | OK |
| T3.7 | (d)⇒(a): da c_F < 1 segue ‖x+y‖² ≥ (1−c_F)(‖x‖²+‖y‖²), quindi la somma è chiusa. Contronominale: se inf ℓ = 0, allora ℓ → 0 a un estremo (una concava su un intervallo aperto ha inf uguale al minimo dei limiti agli estremi) | OK (punto "da verificare" chiuso) |
| T3.8 | esistono E_k disgiunti con sup ℓ² ≤ 4^{−k}; G = Σc_k𝟙_{E_k} è localmente limitata in S. \|h_s(t)\| ≤ C_1ℓ(s) (Lipschitz di e^{λt} su [−M,M], \|t−α(s)\| ≤ ℓ) | OK (punti "da verificare" chiusi; stima di Lipschitz su campioni) |
| T3.9 | ‖u‖² ≤ C_1²Σ4^{−k} < ∞ e ‖e^{d_2t}G‖² = ∞. Per l'unicità, u ∉ ℋ_1+ℋ_2; u_N → u con u_N ∈ ℋ_1+ℋ_2 (componenti limitate su un dominio limitato) | OK. Che e^{d_it}F_i(s) stia in 𝒟′ con F_i ∈ L¹_loc(S) non è scritto → **T3-1** |
| T3.10 | Corollario: sul rettangolo con c ≠ 0 le corde in direzione (1,c) tendono a 0 agli angoli (quadrato, c = 1: ℓ = 1−\|s\|), quindi c_F = 1; con c = 0, ℓ ≡ \|I\| | OK |

### C12-T2
| MC | passo | esito |
|---|---|---|
| T2.1 | i fattori τ−a_j sono monici di grado 1, quindi irriducibili e non associati: si applica T1 con m_j = 1 | OK |
| T2.2 | (i) ∂_t^lu_j = a_j(∂_x)^lu_j, U = V(∂_x)**u**, adj(V)V = ΔI in ℂ[ξ]^{k×k}; vale per **ogni** scomposizione | OK (simbolico, k = 3) |
| T2.3 | (ii) R/(τ−a_i,τ−a_j) ≅ ℂ[ξ]/(a_i−a_j), quindi δ = Σdeg(a_i−a_j) = deg Δ (ℂ[ξ] è un dominio). Ogni elemento di N soddisfa Δ(∂_x)w_j = 0 | OK (3 esempi: δ = deg Δ con la formula di Gröbner) |
| T2.4 | (iii) comassimale ⟺ ogni a_i−a_j ∈ ℂ^× ⟺ Δ ∈ ℂ^× | OK |
| T2.5 | (iv) le colonne di V sono autovettori della compagna, Π_j = v_je_j^TV^{−1} e ΔΠ_j(∂_x)U = v_jΔ(∂_x)u_j | OK nella convenzione "compagna con 1 sulla sopradiagonale e ultima riga −c_j" → **T2-2** |
| T2.6 | Δ non costante ⇒ "una radice ρ annulla qualche a_i−a_j, e Π_j ha lì un polo" | **impreciso negli indici**: il polo ce l'hanno Π_i e Π_j **coinvolti** nella collisione, non tutti i Π in ρ. Esempio: a = (0, ξ, 2), dove Π_3 è regolare in ρ = 0. Anche l'argomento del limite si può semplificare → **T2-1** |

## 3. Rilievi e fix (proposti, non applicati)
- **L5-1 · REGULARITY_GAP · COSMETIC · MINOR · ADD_DERIVATION.**
  - *Problema.* In (b) il rettangolo va scelto relativamente compatto, Q ⋐ D, in modo che φ ∈ L²(Q).
  - *Fix.* Si prova ⟨F,χ⟩ = ⟨φ,χ⊗θ⟩ = ∫χ(s)(∫φθ dr)ds per Fubini. Per Cauchy–Schwarz ‖∫φθ dr‖_{L²(s_a,s_b)} ≤ ‖θ‖_{L²}‖φ‖_{L²(Q)}. Ogni s ∈ S ha un tale Q attorno a sé.
  - *Facoltativo.* Dire che "convesso" si può indebolire a "fette {s = s_0} ∩ D connesse".
- **T3-1 · UNPROVEN_SUBCLAIM · COSMETIC · MINOR · ADD_DERIVATION.**
  - *(d)⇒(a), buona definizione di u.* Nella costruzione di (d)⇒(a), F e G sono localmente limitate su S, ma non vicino a s_-. Va detto che sono in L¹_loc(S), che e^{d_it}F_i(s) ∈ L¹_loc(Ω′) perché un compatto di Ω′ si proietta in un compatto di S, e che f(e^{d_1t}F) = 0 in 𝒟′.
  - *Convenzione nella Gram.* In (a)⇒(b) si scrive ∫|Fe^{d_1t}+Ge^{d_2t}|² = (F,G)Γ(F,G)^*. Con Γ_{ab} = ∫e^{d_at}\overline{e^{d_bt}} la forma corretta è (F,G)Γ(F̄,Ḡ)^T, cioè va trasposta. È irrilevante per la stima λ_min.
- **T2-1 · QUANTIFIER_ERROR (indici) · UNCLEAR/LOCAL · MINOR · WEAKEN_CLAIM testuale + ADD_DERIVATION.**
  - *Riformulazione.* "Per ogni j, Π_j ha un polo esattamente nei punti ρ in cui a_j(ρ) = a_i(ρ) per qualche i ≠ j. Se Δ non è costante, ogni Π_j ha almeno un polo."
  - *Perché ogni Π_j ha un polo.* Se a_j−a_i ∈ ℂ^× per ogni i ≠ j, allora a_i−a_l = (a_j−a_l)−(a_j−a_i) è costante per ogni i, l, quindi Δ ∈ ℂ^×.
  - *Prova breve del polo* (sostituisce l'argomento Jordan/non derogatoria). Π_j è razionale. Se fosse limitata vicino a ρ, avrebbe un limite Π. Da Π_jv_j = v_j e Π_jv_i = 0, passando al limite, si ottiene Πv_j(ρ) = v_j(ρ) e Πv_i(ρ) = 0. Ma v_i(ρ) = v_j(ρ), perché a_i(ρ) = a_j(ρ), e la sua prima coordinata è 1: assurdo.
  - *Regolarità.* Nei ρ in cui a_j(ρ) è semplice, Π_j è regolare: è il proiettore di Riesz di un autovalore semplice, analitico.
  - *Verifica SymPy.* Insieme dei poli di Π_j = punti di collisione del ramo j, in 3 esempi con 9/9 proiettori.
- **T2-2 · NORMALIZATION_MISMATCH · COSMETIC · MINOR.**
  - *Problema.* Va fissata la convenzione della compagna C(ξ): 1 sulla sopradiagonale e ultima riga (−c_0,…,−c_{k−1}). Solo con questa convenzione (1,a,…,a^{k−1})^T è autovettore **destro**; con la trasposta è autovettore sinistro.
  - *Coerenza con II-T2.* II-T2 usa il jet (u,∂_tu,…), che va nella stessa convenzione. Va citata.

## 4. Red team (Phase 1.5) — esito
1. **C1.** Ho verificato, per m = 0..4, la scomposizione esplicita nelle coordinate (t,x), la formula di G^{(m)}, la finitezza delle norme di u e la divergenza per u_2. Per m = 2 c'è anche un calcolo diretto sul triangolo: ‖u‖² ≈ 1.12, e la coda di u_2 è logaritmica.
   - *Tentativo di rottura.* Il caso m = 0 è il più delicato (H^{−1} come duale di H¹_0; u = (e^t−1)/s). Regge.
   - *Coerenza con T3.* C1 con m = 0 è il caso c = −1, d_1 = 0, d_2 = 1 di T3 sul quadrato, dove c_F = 1.
   - *"Perdita esattamente una derivata".* È esatto nella scala intera H^m (u_j ∈ H^{m−1}∖H^m). Non ho verificato l'ottimalità in scala frazionaria, e l'enunciato non la afferma.
2. **T3.**
   - Gram definita positiva su campioni.
   - Identità c_F² = tanh(dT/2)/(dT/2) per {1, e^{dt}} su (0,T): è la formula citata come C12-P8, e la verifica conferma la coerenza.
   - Versione continua di (d)⇒(a) sul triangolo, con G = 1/s: ∫G²ℓ³ < ∞, ma ∫G²ℓ = ∞.
   - Corda del quadrato ℓ = 1−|s|.
3. **L5.** Non c'è controesempio con D convesso. Il dominio a "U" (AUDIT_C3-T1, L3-1) mostra che senza fette connesse (a) fallisce: è un'ipotesi necessaria, ed è presente.
4. **T2.**
   - Identità Δ = ∏(a_j−a_i) e adj(V)V = ΔI.
   - δ = deg Δ in 3 esempi: (0, ξ, ξ+1) → 2; (0, ξ², −ξ) → 5; (0, ξ, 2) → 2.
   - Poli dei Π_j: è emersa l'imprecisione T2-1. Con a = (0, ξ, 2), Π_3 non ha poli in 0.

Nessun controesempio agli enunciati come scritti, una volta applicato T2-1, che è testuale.

## 5. Portata (scientific-critical-thinking)
**Dimostrato.**
- La scomposizione per fattori **non** conserva H^m(Ω), nemmeno su un quadrato con fattori comassimali. La perdita è di una derivata, ed è raggiunta (C1).
- Per coppie di trasporti paralleli su un convesso limitato, la scomposizione L² globale vale esattamente quando le corde caratteristiche non degenerano. Questo equivale a c_F < 1 (T3, m = 0).
- Per fattori di grado 1 in τ c'è una formula esplicita di Vandermonde, con δ = deg Δ e un ponte esatto con i proiettori della compagna (T2), coerente con II-T2 e II-T4.

**Non dimostrato.**
- T3 per m ≥ 1, e per fattori non di trasporto.
- Il criterio geometrico generale. È C12-Q1…Q5, APERTO.
- Il viceversa "c_F < 1 ⟸ somma chiusa" di C12-P7 nel caso generale, che è CON-FONTE (Deutsch) da verificare: qui è dimostrato solo per i trasporti.

## 6. Acceptance gate
| condizione | esito |
|---|---|
| 0 FATAL/CRITICAL | ✔ |
| Ipotesi esplicite (Ω convesso limitato in T3, a_j distinti in T2, m ∈ ℕ in C1) | ✔ |
| Teoremi invocati con le ipotesi scaricate (mappa aperta su un Banach, Fubini/Tonelli, incollamento di fasci, Cauchy–Schwarz) | ✔ |
| Controesempi tentati | ✔ |
| Nessuna O(·) | ✔ |

**Stati proposti.**
- C12-C1 **DIMOSTRATO**, quindi l'enunciato "scomposizione in H^m" è **FALSO**.
- C12-L5, C12-T3, C12-T2 **DIMOSTRATO**, con i fix MINOR L5-1, T3-1, T2-1 e T2-2.
