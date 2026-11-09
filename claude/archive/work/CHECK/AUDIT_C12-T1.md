# AUDIT C12-T1 (+ C12-L3, C12-L1, C12-L2): scomposizione per fattori in 𝒟′/C^∞ su un rettangolo
Revisore: S-CHECK-2C (2ª tornata, parte C) · 25/10/2026
Fonte esaminata: SOLO `work/C1C2/CHECK_REQUEST.md` (§0, C12-L3, C12-L1, C12-L2, C12-T1). `work/C1C2/PROOF_PACKAGE.md` **non è stato letto**, né per intero né per riferimenti puntuali.
Skill caricate (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-checker (il reviewer sono io: Phase 0.5 enunciati canonici e micro-claim, checklist, Phase 1.5 red team, severità a due assi, acceptance gate; niente Codex/LaTeX), scientific-critical-thinking (separare ciò che è dimostrato da ciò che è affermato fuori dall'enunciato), sympy.
SymPy: `work/CHECK/sympy/audit_c12.py` → `audit_c12.out`, **ESITO GLOBALE: OK (70/70)**. Le sezioni qui rilevanti sono L3, L1, L2, T1 e "Dominio: corona". Un controllo è stato riscritto in quadratura mpmath perché SymPy non chiude ∫e^{2s}log²s; riguarda C1 ed è dichiarato nell'altro audit.

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| C12-L3 (a)–(c) | **PASS-con-fix(L3-1, L3-2)** | DIMOSTRATO |
| C12-L1 (a)–(d) | **PASS-con-fix(L1-1, L1-2)** | DIMOSTRATO |
| C12-L2 (1)–(3) | **PASS-con-fix(L2-1, L2-2)** | DIMOSTRATO |
| C12-T1 (i)–(iv) | **PASS-con-fix(T1-1)** | DIMOSTRATO (Ω rettangolo) |

Non ci sono rilievi FATAL, CRITICAL o MAJOR: tutti i rilievi sono MINOR e i relativi fix sono scritti qui sotto, in §4. Aggiungo due osservazioni di portata (§6), che non sono difetti della prova:
- **O-1.** Sulla corona circolare T1(i) è **falso**, con un controesempio verificato. L'ipotesi sul dominio non si può quindi ridurre a "Ω connesso".
- **O-2.** La stessa prova vale, così com'è, su ogni Ω semplicemente connesso. È uno schizzo da scrivere, non un claim auditato.

## 1. Enunciati canonici (Phase 0.5)
R = ℂ[τ,ξ] (UFD noetheriano). Ω = I×J, con I, J intervalli aperti, eventualmente illimitati. 𝒜 ∈ {𝒟′(Ω), C^∞(Ω)}, con τ, ξ che agiscono come ∂_t, ∂_x. Sol_𝒜(M) := Hom_R(M,𝒜).
- **L3.** Per f,g,h ∈ R∖0:
  - (a) se gcd(f,g) = 1, allora (f,g) ∩ ℂ[ξ] ∋ r ≠ 0 e (f,g) ∩ ℂ[τ] ∋ s ≠ 0, quindi dim R/(f,g) ≤ deg r·deg s;
  - (b) se gcd(f,g) = gcd(f,h) = 1, allora dim R/(f,gh) = dim R/(f,g) + dim R/(f,h);
  - (c) (f,g) = R ⟺ V(f) ∩ V(g) = ∅.
- **L1.** Su Ω = I×J, con θ ∈ C_c^∞(J), ∫θ = 1:
  - (a) ker_{𝒟′}∂_x = 𝒟′(I)⊗1;
  - (b) esiste 𝒥 lineare con ∂_x𝒥 = id e ∂_t𝒥 = 𝒥∂_t;
  - (c) se D_xφ = D_tψ, esiste w con D_tw = φ e D_xw = ψ;
  - (d) ker D_t ∩ ker D_x = ℂe_{(p,q)}.
- **L2.** Per ogni R-modulo M con dim_ℂ M < ∞:
  - (1) Ext¹_R(M,𝒜) = 0;
  - (2) dim Sol_𝒜(M) = dim M;
  - (3) Sol(M) è fatto di EP, ed è lo stesso spazio (restrizioni di funzioni intere) per ogni rettangolo.
- **T1.** Sia P = c∏_{j=1}^s Q_j, con Q_j = P_j^{m_j}, P_j irriducibili a due a due non associati. Allora:
  - (i) ker P = Σ_j ker Q_j;
  - (ii) dim ker Σ = δ(P) := Σ_{i<j} dim R/(Q_i,Q_j), e le componenti degli elementi di ker Σ sono EP;
  - (iii) la scomposizione è unica ⟺ δ = 0 ⟺ V(Q_i) ∩ V(Q_j) = ∅ per ogni i ≠ j;
  - (iv) se u ∈ C^∞, ogni scomposizione in 𝒟′ è liscia.

## 2. Dipendenze (DAG, nessun ciclo)
- L3 dipende da: risultante [CLO cap. 3 §6], UFD, simultanea triangolabilità di operatori commutanti in dimensione finita.
- L1 dipende solo dall'operatore K.
- L2 dipende da L1(c),(d), dalla risoluzione di Koszul, dalla successione lunga dell'Ext nella prima variabile [Weibel], da L1(a) nella versione torta e dalle ODE 1D distribuzionali.
- T1 dipende da L3(a),(b),(c) e da L2(1),(2),(3).

Nessun riferimento in avanti.

## 3. Micro-claim ed esiti per passo
### C12-L3
| MC | passo | esito |
|---|---|---|
| L3.a1 | deg_τf = 0 ⇒ r = f; deg_τ f, deg_τ g ≥ 1 ⇒ Res_τ(f,g) ∈ (f,g) ∩ ℂ[ξ] | OK (controllo: Res = ξ⁴−ξ−1, ridotto a 0 da una base di Gröbner di (f,g)) |
| L3.a2 | Res_τ = 0 ⟺ fattore comune di grado positivo in τ (con i gradi effettivi) | OK; numerazione delle proposizioni di CLO → **L3-2** |
| L3.a3 | R/(f,g) è un quoziente di ℂ[ξ]/(r) ⊗ ℂ[τ]/(s) ⇒ dim ≤ deg r·deg s | OK (controllo: 4 ≤ 4·2) |
| L3.b1 | ·g: R/(f,h) → R/(f,gh) è ben definita, l'immagine coincide col nucleo della proiezione, ed è iniettiva | OK. L'esattezza usa solo gcd(f,g) = 1; gcd(f,h) = 1 serve solo per la finitezza. Non serve gcd(g,h) = 1 (controllo con g = h) |
| L3.b2 | additività anche quando V(f), V(g), V(h) hanno un punto comune, con molteplicità | OK (controlli: tre parabole tangenti in 0 danno (4,2,2); punto triplo (1,1) dà (6,4,2)) |
| L3.c1 | "⇐": autovettore comune di τ, ξ su N = R/(f,g) ≠ 0 ⇒ (p,q) ∈ V(f) ∩ V(g) | OK **se f, g sono coprimi**; manca il caso non coprimo → **L3-1** |
| L3.c2 | "⇒": (f,g) ⊆ 𝔪_{(p,q)} | OK |

### C12-L1
| MC | passo | esito |
|---|---|---|
| L1.K1 | Kψ liscia; supporto in pr_t(supp ψ) × [min, max] di (pr_x supp ψ ∪ supp θ); sopra il massimo l'integrale vale Ψ − Ψ·∫θ = 0 | OK (controllo su J = (0,1): Kψ(·,1) = 0). **Qui si usa il rettangolo**: pr_t(K) × conv(pr_x K ∪ supp θ) ⊂ Ω → **L1-2** (esplicitare) |
| L1.K2 | K continua da 𝒟_K a 𝒟_{K″}; K∂_xψ = ψ; ∂_xKψ = ψ − θ⊗Ψ; K∂_t = ∂_tK | OK (controlli simbolici) |
| L1.a | ⟨φ,ψ⟩ = −⟨∂_xφ,Kψ⟩ + ⟨φ,Ψ⊗θ⟩. Ψ ∈ C_c^∞(I) e χ ↦ χ⊗θ è continua da C_c^∞(I) in C_c^∞(Ω), quindi c ∈ 𝒟′(I) e φ = c⊗1. Unicità: ⟨c,χ⟩ = ⟨c⊗1, χ⊗θ⟩ | OK (punto "da verificare" chiuso) |
| L1.b1 | 𝒥 := −K^t è una distribuzione e ∂_x𝒥 = id | OK |
| L1.b2 | ∂_t𝒥 = 𝒥∂_t per dualità: ⟨∂_t𝒥φ,ψ⟩ = ⟨φ,K∂_tψ⟩ = ⟨φ,∂_tKψ⟩ = ⟨𝒥∂_tφ,ψ⟩ | OK (punto "da verificare" chiuso) |
| L1.b3 | "su C^∞, 𝒥φ = ∫_{x̄}^xφ dy" | **impreciso**: la 𝒥 duale vale ∫_{x̄}^xφ dy − c_θ(t), con c_θ(t) = ∫θ(x)∫_{x̄}^xφ dy dx (controllo: differenza ≈ −2.3·10⁻⁴ ≠ 0; la formula corretta è verificata) → **L1-1** |
| L1.c | il twist con e è biiettivo; w_0 = 𝒥ψ̃; ∂_x(∂_tw_0 − φ̃) = 0 ⇒ c⊗1; primitiva C di c in 𝒟′(I); w̃ = w_0 − C⊗1 | OK. Il passo usa solo ∂_x𝒥 = id e la commutazione delle derivate distribuzionali, **non** [∂_t,𝒥] = 0. La primitiva 1D va scritta → **L1-2** |
| L1.d | ∂_xw̃ = 0 ⇒ w̃ = c⊗1; c′ = 0 su un intervallo ⇒ c costante | OK |

### C12-L2
| MC | passo | esito |
|---|---|---|
| L2.i1 | Koszul 0 → R → R² → R → R/𝔪 → 0 esatta ((τ−p, ξ−q) è una successione regolare) | OK (β∘α = 0, sizigie calcolate) |
| L2.i2 | una risoluzione proiettiva del primo argomento calcola Ext^•_R(M,N) per **ogni** N: non serve alcuna ipotesi su 𝒜 | OK (punto "da verificare" chiuso); riferimento → **L2-1** |
| L2.i3 | β* = (D_t, D_x), α* = −D_x(·) + D_t(·); Hom = ker β* = ℂe (L1(d)); Ext¹ = ker α*/im β* = 0 (L1(c)) | OK |
| L2.ii | autovettore comune ⇒ S ≅ R/𝔪 ⊂ M. Successione lunga con Ext¹(M/S) = Ext¹(S) = 0 ⇒ Ext¹(M) = 0 e Hom(M) → Hom(S) suriettiva ⇒ dim = n | OK |
| L2.iii1 | Ann(M) contiene i polinomi minimi s(τ), r(ξ) | OK |
| L2.iii2 | r(∂_x)w = 0 ⇒ w = Σc_{kl}⊗x^le^{ρ_kx}: induzione su deg r con ker(∂_x−ρ) = 𝒟′(I)⊗e^{ρx} e soluzioni particolari c̃⊗r_l(x)e^{μx} (μ ≠ ρ: r_l di grado l; μ = ρ: x^{l+1}/(l+1)) | OK (punto "da verificare" chiuso; controlli simbolici in entrambi i casi) |
| L2.iii3 | θ_{kl} ∈ C_c^∞(J) biortogonali; s(∂_t)c_{kl} = 0 ⇒ c_{kl} ∈ EP(I) | OK; esistenza delle θ_{kl} non scritta → **L2-2** |
| L2.iii4 | Sol_{C^∞(ℝ²)}(M) ha dimensione n, la restrizione è iniettiva (EP nullo su un aperto ⇒ nullo) ⇒ Sol_{𝒜(Ω)}(M) = restrizioni, lo stesso spazio per ogni rettangolo | OK (controllo: a = (τ², ξ²−τ), dim Sol = dim R/a = 4) |

### C12-T1
| MC | passo | esito |
|---|---|---|
| T1.1 | (f) ∩ (g) = (fg) (UFD) ⇒ 0 → R/(fg) → R/(f)⊕R/(g) → R/(f,g) → 0 esatta | OK |
| T1.2 | ι*(u_1,u_2) = (u_1,u_2)∘ι = u_1 + u_2; π*(w) = w∘π ↦ (w, −w) | OK (punto "da verificare" chiuso) |
| T1.3 | Ext¹(R/(f,g),𝒜) = 0 (L3(a) + L2(1)) ⇒ Σ suriettiva; ker Σ = π*(Sol(R/(f,g))), di dimensione dim R/(f,g) (L2(2)) | OK |
| T1.4 | induzione: Σ = Σ_2∘(id⊕Σ′); B := id⊕Σ′ è suriettiva ⇒ dim ker(Σ_2B) = dim ker B + dim ker Σ_2 (ker B ha dimensione finita per induzione) | OK (punto "da verificare" chiuso) |
| T1.5 | dim ker Σ_2 = dim R/(Q_1,P′) = Σ_{j≥2} dim R/(Q_1,Q_j) (L3(b) iterato: Q_1 è coprimo con Q_j e con ∏_{l>j}Q_l) | OK. **Non serve alcuna inclusione–esclusione**: la molteplicità di intersezione è additiva anche nei punti comuni a tre o più varietà (§5) |
| T1.6 | componenti di N: w_j ∈ ker Q_j ∩ ker∏_{i≠j}Q_i = Sol(R/(Q_j,B_j)), di dimensione finita ⇒ EP (L2(3)) | OK. Coerente con C3-L3(e) e con II-T2: la proiezione π_j(N) è **tutto** Sol(R/(Q_j,B_j)), applicando (i) a B_j |
| T1.7 | (iii): unicità ⟺ N = 0 ⟺ δ = 0 ⟺ (Q_i,Q_j) = R per ogni i<j ⟺ V(Q_i) ∩ V(Q_j) = ∅ (L3(c); Q_i, Q_j coprimi) | OK |
| T1.8 | (iv): esiste una scomposizione liscia; due scomposizioni in 𝒟′ differiscono per un elemento di N_{𝒟′}, fatto di EP lisci | OK |
| T1.9 | s = 1 (δ = 0) e costante c: banali | OK |

## 4. Rilievi e fix (proposti, non applicati ai file di S-C1C2)
- **L3-1 · CASE_INCOMPLETE · UNJUSTIFIED/LOCAL→chiusa qui · MINOR · ADD_DERIVATION.**
  - *Problema.* L'enunciato (c) vale per f, g ∈ R∖0 qualunque, ma il "⇐" usa (a), che richiede f, g coprimi.
  - *Fix.* Se f, g non sono coprimi, hanno un fattore comune π non costante e V(π) ⊆ V(f) ∩ V(g). V(π) ≠ ∅: se deg_τπ ≥ 1, per quasi ogni ξ_0 il polinomio π(·,ξ_0) ha una radice; altrimenti π ∈ ℂ[ξ] non costante ha una radice ξ_0 e ℂ×{ξ_0} ⊆ V(π).
  - *Conclusione.* V(f) ∩ V(g) = ∅ implica che f, g sono coprimi, e allora vale (a).
  - *In alternativa.* Mettere "f, g coprimi" nelle ipotesi di (c), che è l'unico uso fatto in T1.
- **L3-2 · REFERENCE_MISMATCH (possibile) · COSMETIC · MINOR · ADD_REFERENCE.**
  - *Problema.* Il rimando "CLO cap. 3 §6, Prop. 3 e 5" va verificato sull'edizione citata: la numerazione cambia tra le edizioni. Nella 4ª ed. il caso "su UFD k[x_2..x_n]" è la Proposizione 5 di §3.6? Va controllato da CIT-AUDIT.
  - *Cosa scrivere nel testo.*
    1. Res_τ(f,g) ∈ (f,g), perché esistono A, B con Af + Bg = Res (regola di Cramer sulla matrice di Sylvester).
    2. Res = 0 ⟺ fattore comune di grado positivo in τ, quando i gradi usati sono quelli effettivi (coefficienti direttori ≠ 0 in ℂ[ξ]).
- **L1-1 · NORMALIZATION_MISMATCH · UNCLEAR/COSMETIC · MINOR · ADD_DERIVATION.**
  - *Problema.* Così com'è scritto, "su C^∞, 𝒥φ = ∫_{x̄}^xφ(t,y)dy" è falso per la 𝒥 definita per dualità.
  - *Formula corretta.* Integrando per parti in x si ottiene 𝒥φ = Φ − c_θ, con Φ(t,x) = ∫_{x̄}^xφ(t,y)dy e c_θ(t) = ∫_Jθ(x)Φ(t,x)dx, che è liscia (verificato con SymPy). Questo dà anche che 𝒥(C^∞) ⊆ C^∞.
  - *Fix, a scelta.*
    1. Scrivere questa formula.
    2. Oppure dire che su C^∞ si **usa un altro operatore**, 𝒥_∞φ := Φ, che ha le stesse due proprietà: ∂_x𝒥_∞ = id, e [∂_t,𝒥_∞] = 0 per derivazione sotto il segno di integrale su un segmento compatto [x̄,x] ⊂ J.
  - *Effetto sulla prova.* Nessuno: entrambe le scelte bastano.
- **L1-2 · UNPROVEN_SUBCLAIM · COSMETIC · MINOR · ADD_DERIVATION.**
  - *(c) Primitiva 1D.* Per c ∈ 𝒟′(I) si fissa θ_1 ∈ C_c^∞(I) con ∫θ_1 = 1. Si pone K_1χ(t) := ∫_{inf I}^t(χ − θ_1∫χ) e ⟨C,χ⟩ := −⟨c,K_1χ⟩. Allora C′ = c.
  - *Commutazione non necessaria in (c).* Va precisato che lì [∂_t,𝒥] = 0 non serve. Si usa solo ∂_x∂_t = ∂_t∂_x nel senso delle distribuzioni. La commutazione resta vera (MC L1.b2).
  - *Dove entra il rettangolo.* Va dichiarato: nel supporto di Kψ (pr_t K × conv(pr_x K ∪ supp θ) ⊂ Ω) e quindi in L1(a). Su un dominio non convesso in x, (a) è falso (vedi il dominio a "U" in AUDIT_C3-T1, rilievo L3-1).
- **L2-1 · REFERENCE_MISMATCH · COSMETIC · MINOR · ADD_REFERENCE.**
  - *Problema.* "Weibel §2.4–2.5" non è il punto esatto.
  - *Riferimenti da citare.*
    1. Che Ext^i_R(M,N) si calcoli con una risoluzione proiettiva di M, per N **qualsiasi**: è il teorema di bilanciamento, Weibel Thm 2.7.6 (Ext è definito come R^i Hom_R(M,−)(N)).
    2. La successione lunga nella prima variabile: Weibel §2.5 / Cor. 2.7.? (numero da verificare).
  - *Effetto sulla prova.* Il contenuto è standard e corretto, e non usa ipotesi su 𝒜.
- **L2-2 · UNPROVEN_SUBCLAIM · COSMETIC · MINOR · ADD_DERIVATION.**
  - *Problema.* L'esistenza delle θ_{kl} ∈ C_c^∞(J) biortogonali alle x^le^{ρ_kx} non è scritta.
  - *Argomento.* Le funzioni sono linearmente indipendenti su J (L3(b) di S-C3, oppure Wronskiano). Se T: θ ↦ (∫g_aθ)_a non fosse suriettiva su ℂ^n, esisterebbe c ≠ 0 con Σc_ag_a = 0 come distribuzione, quindi anche puntualmente: assurdo. Stesso argomento del fix L3-3 in AUDIT_C3-T1.
- **T1-1 · SCOPE (ipotesi sul dominio) · UNCLEAR/COSMETIC · MINOR · STRENGTHEN_ASSUMPTION testuale.**
  - *Situazione.* L'enunciato è correttamente ristretto ai rettangoli.
  - *Problema.* Nel LEDGER e negli usi a valle (S-P1 e successivi) l'ipotesi va riportata **come condizione essenziale e non tecnica**. Sulla corona {1 < |y| < 2} la tesi (i) è falsa per P = τξ (O-1, §6).
  - *Fix.* Aggiungere all'enunciato o a un'osservazione: "(i)–(iii) richiedono una condizione topologica su Ω. Valgono sui rettangoli (qui), sui convessi (Malgrange–Ehrenpreis, fuori dall'enunciato) e, con la stessa prova, sui semplicemente connessi (O-2). Sono false sulla corona."
  - *Facoltativo, utile per S-P1/II.* Scrivere in (ii) che π_j(N) = Sol(R/(Q_j,B_j)) e che δ(P) = Σ_{i<j} m_im_j·Σ_z I_z(P_i,P_j), sommando sulle molteplicità di intersezione locali (additività L3(b) in entrambi gli argomenti).

## 5. Red team (Phase 1.5) — esito
Script `audit_c12.py`, sezioni L3, L1, L2, T1, Corona.
1. **δ(P) con tre o più fattori (domanda del coordinatore).** Ho calcolato la dimensione di N in due modi indipendenti:
   - con la formula Σ_{i<j} dim R/(Q_i,Q_j), contando i monomi standard di una base di Gröbner;
   - direttamente, con un ansatz EP punto per punto. Per L3(b) di S-C3 la condizione Σw_j = 0 si spezza per esponente z: si cercano polinomi q_j con Q_j(z+∂)q_j = 0 e Σq_j = 0, di grado ≤ 6 e ≤ 8 (risultato stabile).

   Esiti:
   - E1 (τ, ξ, τ−ξ: tre rette per 0): 3 = 3. L'inclusione–esclusione darebbe 3 − 1 = 2, che è **sbagliato**. La verifica a mano: (−αx+γ) + (−αt−β−γ) + (α(t+x)+β) = 0, con tre parametri.
   - E2 (τ−ξ², τ, τ−2ξ²: tre parabole tangenti in 0): 6 = 6.
   - E3 (τ−ξ², (τ−ξ)², (ξ−1)²: punto **triplo** (1,1) con molteplicità, più il punto (0,0)): contributi locali 8 + 2 = 10 = formula.
   - E4 (quattro fattori lineari, punti (0,0), (0,1), (1,0), (½,½)): 3+1+1+1 = 6 = formula.

   **Conclusione:** la formula a coppie è esatta. L'additività della molteplicità di intersezione assorbe i punti multipli, e il passo induttivo di T1 lo dimostra (MC T1.4–T1.5).
2. **s = 2:** calore/trasporto (dim 2, punti (0,0), (1,1)), onda (1), trave τ²+ξ⁴ contro τ (4). In tutti i casi la dimensione dell'ansatz coincide con dim R/(Q_1,Q_2).
3. **L1(b):** controesempio alla formula integrale come identità per la 𝒥 duale (L1-1). La formula corretta è verificata.
4. **L2:** dim Sol(R/a) = dim R/a per un ideale non radicale, a = (τ², ξ²−τ), di dimensione 4.
5. **Dominio (O-1): controesempio verificato a T1(i) fuori dalle ipotesi.** Ω = {1 < |(t,x)| < 2}, P = τξ, u = α(x)β(t), con α, β lisce, α = β = 0 sotto −½ e = 1 sopra ½. Siccome supp(α′β′) ⊆ [−½,½]², che è disgiunto da Ω, si ha ∂_t∂_xu = 0 e u ∈ C^∞(Ω). Supponiamo u = a + b con ∂_ta = 0 e ∂_xb = 0, in C^∞ o in 𝒟′.
   - Sulle quattro regioni connesse R1 = {x<−½, t<−½}, R2 = {x<−½, t>½}, R3 = {x>½, t<−½}, R4 = {x>½, t>½} (intersecate con Ω) u vale rispettivamente 0, 0, 0, 1. Quindi a = c_i e b = u − c_i su R_i.
   - Le rette x = ±1,5 incontrano Ω in un solo intervallo, e a è costante lungo di esso (L1(a) su un rettangolo (−0,7;0,7)×(x±0,1) ⊂ Ω). Ne segue c_1 = c_2 e c_3 = c_4.
   - Le rette t = ±1,5 incontrano Ω in un solo intervallo, e b è costante lungo di esso. Ne segue −c_1 = −c_3 e −c_2 = 1−c_4.
   - Il sistema è incompatibile (SymPy: nessuna soluzione), quindi u ∉ ker∂_t + ker∂_x.
   - L'ostruzione è la classe di Čech di H¹(Ω;ℂ) = ℂ. Non contraddice T1, che è enunciato su rettangoli.
6. **Coerenza con il LEDGER.**
   - *C3-L3(e).* "Ambiguità EP" è coerente: T1(ii) dà EP sul rettangolo, C3-L3 lo dà su ogni connesso.
   - *II-T2.* "Ambiguità della componente j = Sol(Q_j,B_j)" è coerente: MC T1.6.
   - *II-T3.* "Unica ⟺ V ∩ V = ∅, Ω qualsiasi" è coerente: nel caso comassimale M = 0 e Ext¹(0,𝒜) = 0 su ogni Ω, quindi (i)–(iii) valgono anche sulla corona. La corona mostra che, invece, per coppie non comassimali l'esistenza dipende dal dominio.

Nessun controesempio agli enunciati come scritti.

## 6. Portata (scientific-critical-thinking)
- **Dimostrato.** Su ogni rettangolo aperto Ω = I×J, anche illimitato, e per 𝒜 = 𝒟′ o C^∞, valgono:
  - la scomposizione per fattori ker P = Σker Q_j;
  - l'ambiguità di dimensione esatta δ(P) = Σ_{i<j} dim R/(Q_i,Q_j), fatta di EP;
  - l'unicità ⟺ comassimalità a coppie;
  - la regolarità (iv).

  È G★′ punto 2 (strato fattori) nel caso 𝒟′/C^∞.
- **Non dimostrato qui.**
  - (a) La versione H^m(Ω): è falsa in generale, vedi C12-C1 nell'altro audit.
  - (b) Domini non rettangolari. La nota "convesso via Malgrange–Ehrenpreis" è fuori dall'enunciato e sarebbe CON-FONTE.
- **O-1 (verificato).** T1(i) è falso sulla corona. Il dominio non si può indebolire a "connesso", a differenza di C3-T1.
- **O-2 (schizzo, non auditato).** La prova usa il rettangolo solo per L1(c),(d), cioè per Ext¹(R/𝔪,𝒜) = 0 e Hom(R/𝔪,𝒜) = ℂ.
  - Il twist con e trasforma il complesso di Koszul nel complesso di de Rham. Quindi Ext¹(R/𝔪,𝒜) ≅ H¹_dR(Ω), anche per 𝒟′, dove le correnti calcolano la stessa coomologia, e Hom(R/𝔪,𝒜) = ℂ se Ω è connesso.
  - L2(iii) si ottiene dalla restrizione delle soluzioni intere, per uguaglianza delle dimensioni.
  - Ne segue che L2 e T1 valgono su ogni Ω ⊂ ℝ² **semplicemente connesso**.
  - È un'estensione da scrivere e auditare: la propongo come claim nuovo (C12-T1′), non la registro.
- **Kill-argument.** C12-T1 è sul cammino critico di G★′, quindi claim-lifecycle prevede il passaggio kill-argument. Non risulta fatto (colonna "no" nella TABELLA di S-C1C2). Gli attacchi più forti sono il dominio (O-1) e la norma (C12-C1), e li ho registrati entrambi. Raccomando un kill-argument breve, con questi due attacchi come punto di partenza.

## 7. Acceptance gate
| condizione | esito |
|---|---|
| 0 FATAL/CRITICAL | ✔ |
| Ipotesi esplicite (rettangolo; coprimalità in L3(a),(b); L3-1 chiude (c)) | ✔ |
| Ipotesi scaricate a ogni applicazione | ✔ |
| Controesempi tentati su tutti i lemmi chiave (formula di δ con s = 3, 4 e punto triplo; dominio) | ✔ |
| Nessuna O(·) | ✔ |

**Stati proposti:** C12-L3, C12-L1, C12-L2, C12-T1 **DIMOSTRATO** (T1 con ipotesi "Ω rettangolo", essenziale per O-1). I fix MINOR L3-1, L3-2, L1-1, L1-2, L2-1, L2-2 e T1-1 vanno recepiti nel testo di S-C1C2.
