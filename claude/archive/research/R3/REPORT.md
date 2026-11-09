# R3 — REPORT: catalogo termine-per-termine dei pezzi di PDE lineari 1D (C2, C4)

Agente R3 · Fase 1 · 2026-10-22 · Notazione `NOTAZIONE.md` v1 (simbolo `P(τ,ξ)` con modo `e^{τt+ξx}`; Fourier `ξ=iκ`).
*(Salvato dal coordinatore dalla risposta finale di R3: la scrittura diretta era bloccata dall'ambiente.)*

**Skill caricate (Regola 2):** `academic-research-skills/deep-research` (letta; scoping → fonti → sintesi; `anthropic-skills:deep-research` non invocata perché coordina subagenti); `scientific-agent-skills/sympy` (verifiche); `math-skill` (solver/proof); `citation-management` (`sources.bib`). Nessuno script `_vendor` eseguito.

**Verifiche:** 12 script in `research/R3/sympy/` (`s01`–`s12`), `.venv\Scripts\python.exe -I`; log in `sympy/run_all.log`: **139/139 PASS** (138 simbolici esatti, 1 numerico a 30 cifre: Fourier–Bessel, residuo 3·10⁻³³).

**Stati:** DIM = dimostrato qui; DIM-F = noto con fonte; CONG = congettura; FALSO = con controesempio; APERTO.

## 0. Risultati chiave
1. **Catalogo C2 core:** 14 schede complete (§2); ogni classe verificata con T e = 0.
2. **Tabella in una formula:** a coeff. costanti la tabella operatore→classe è il modo `e^{τt+ξx}` con `(τ,ξ)∈V(P)`. La classe "di un termine" esiste solo come sotto-equazione bilanciata `∂_t − a_n(∂_x)`; un monomio isolato ha nucleo banale (DIM): `ker ∂_x^n` = polinomi di grado < n in x con coefficienti funzioni di t; `ker ∂_t = {g(x)}`. Concorda con PR-C2e §0.
3. **Coefficienti variabili:** il ruolo di Fourier/Laplace passa a Mellin per `x∂_x` (classe `x^s`, `x^s log x`), Hermite/Mehler per sl(2) generata da `{∂², x², x∂+½}`, Hankel/Bessel per i termini radiali. Airy, Bessel, Hermite, Legendre sono nuclei di operatori a coeff. polinomiali (olonomi): livello L1.
4. **C4 (R3-L1, R3-P1):** per termini commutanti, u=a+b con L1a=0, L2b=0 risolve (L1+L2)u=0 ⟺ L2a=−L1b=:w, e allora w∈ker L1∩ker L2. Per avvezione–diffusione le soluzioni additivamente decomponibili sono esattamente span{1,s,s²+2Dt,s³+6Dts}, s=x−ct (dim 4 = lunghezza di ℂ[τ,ξ]/(P1+P2,P1P2)). **A8 come scritta è FALSA**; forma corretta moltiplicativa, u=S_tr(t)S_heat(t)u0, E_int=(S1−I)(S2−I)u0, additività nel log-simbolo.
5. **Fattorizzazione ⇒ split additivo:** trave ∂_t²+∂_x⁴=(∂_t−i∂²)(∂_t+i∂²), coppia di Schrödinger coniugate con intersezione {a+bx}; onde: intersezione = costanti.
6. **Duale numerabile per il calore (RT-R3a):** polinomi del calore v_n e funzioni di Appell w_n, ⟨v_n(·,−t),w_m(·,t)⟩=2^n n! δ_nm (Rosenbloom–Widder 1959). Risponde in parte ad A7 e C1.4; base di rappresentazione, non di identificazione (R4).

## 1. Schema delle schede
1 operatore e simbolo; 2 nucleo/classe/base (numerabile o continua); 3 funzioni speciali, trasformate, soluzione fondamentale/Green, autofunzioni; 4 decomposizione (fattorizzazione ⇒ additivo; somma commutante ⇒ moltiplicativo; non commutante ⇒ commutatori); 5 dati per C1 (Gram, duale); 6 attributi Asse 4; 7 tag; 8 fonti; 9 verifica SymPy.

## 2. Catalogo
### K1 — ODE a coeff. costanti (C2.1ᵈ / C2.1, C2.2; L0)
1. p(D)=Π(D−λ_j)^{m_j}, simbolo p(ξ). 2. ker = span{x^k e^{λ_j x}, k<m_j}, dim = deg p; radici complesse ⇒ e^{αx}cos βx, e^{αx}sin βx [DIM-F: Coddington–Levinson cap. 3; MIT 18.03 L11–L14]. 3. ERF p(D)e^{rx}=p(r)e^{rx} (azione del simbolo); Green causale = Σ Res e^{ξx}/p(ξ); Jordan ↔ x^k e^{λx}. 4. Decomposizione primaria ker p = ⊕_j ker(D−λ_j)^{m_j}, E_int=0; Jordan = estensione non spezzata (RT-S1d). 5. Gram di Cauchy 1/(λ_i+λ_j) in L²(0,∞); duale: Prony/Hankel (R4). 6. Ordine m, spettro = radici. 7. ★ 8. Coddington–Levinson; MIT 18.03 L11–L30; Myint-U–Debnath cap. 2. 9. `s01` 7/7 PASS (controprova x³e^{ax}: residuo 6(a−b)e^{ax}; Wronskiano e^{2ax}).

### K2 — ∂_t e ∂_t² isolati
ker ∂_t={g(x)}, ker ∂_t²={a(x)+t b(x)}: classi banali; il termine temporale è solo il "lato" del bilanciamento. ★ · `s02` PASS.

### K3 — Trasporto ∂_t+c∂_x (C2.2ᵈ / C2.6)
Simbolo τ+cξ; nucleo g(x−ct) (classe continua); velocità variabile a(x): g(t−Ψ(x)), Ψ′=1/a; a=x: g(xe^{−t}) [DIM-F: Evans §2.1]. Nucleo δ(x−ct), moltiplicatore e^{−iκct}. Commuta con tutti i termini a coeff. costanti (cambio di riferimento); con coeff. variabili commutatori, [x∂,∂²]=−2∂² (verificato). Gram = autocorrelazione di g. Iperbolico, unitario. ★ · Evans §2.1; MIT 18.303 L16–18; Myint-U–Debnath cap. 5 · `s02` 5/5 PASS.

### K4 — Diffusione ∂_t−D∂² (C2.3ᵈ / C2.7, C2.21)
Simbolo τ−Dξ². Classi: modi e^{−Dκ²t+iκx} (continui su ℝ, numerabili su 𝕋/intervallo); polinomi del calore v_n=e^{tD∂²}x^n=Σ_j n!/(j!(n−2j)!) x^{n−2j}(Dt)^j; Hermite–Gauss ∂_x^nG=(−1)^n(4Dt)^{−n/2}H_n(x/√(4Dt))G; similarità erf(x/√(4Dt)). Soluzione fondamentale G=(4πDt)^{−1/2}e^{−x²/4Dt} [DIM-F: Evans §2.3.1 Thm 1]; trasformata di Appell G(t,x)u(−1/t,x/t) manda soluzioni in soluzioni (verificata); v_n(x,−1/2D)=He_n(x) (n=3,4); Green su intervallo = Σe^{−λ_n t}φ_nφ_n. Somme con trasporto/reazione/dispersione commutanti ⇒ prodotti G(t,x−ct), e^{rt}G, G*Ai_t. Duale: w_n=k(x,t)v_n(x/t,−1/t), ⟨v_n(·,−t),w_m(·,t)⟩=2^n n!δ_nm (n,m≤3); u=Σa_n v_n, a_n=⟨u,w_n⟩/2^n n!, per soluzioni intere di ordine di crescita < 2 [DIM-F: Rosenbloom–Widder 1959; Widder 1975, da riscontrare]. Parabolico, smoothing, dissipativo. ★◆ · Evans §2.3; Widder; Polyanin 2002 cap. 1; MIT 18.303 L1–9; Guenther–Lee · `s03` 14/14, `s11` PASS.

### K5 — Dispersione ∂_t+∂³ (C2.4ᵈ / C2.10) e Schrödinger libero
Simbolo τ+ξ³; Schrödinger τ−iξ². Classi: e^{iκx+iκ³t}; (3t)^{−1/3}Ai(x/(3t)^{1/3}) (e Bi); Appell x³−6t, x⁴−24tx. Nucleo di Airy (Ai″=xAi) [DIM-F: DLMF §9], decadimento t^{−1/3}; Fresnel (4πit)^{−1/2}e^{ix²/4t}, t^{−1/2}. Commuta con diffusione e trasporto (KdV–Burgers lineare: G*K). ∞ irregolare ⇒ Stokes (RT-S1f). Ortogonalità continua ∫Ai(x+a)Ai(x+b)dx=δ(a−b) (Vallée–Soares; da verificare). Velocità di gruppo 3κ². ★ · DLMF 9; Polyanin; Evans §4.3 · `s04` 8/8 PASS.

### K6 — Reazione ∂_t−r (C2.5ᵈ / C2.11 lineare)
Classe e^{rt}g(x); stazionario ∂²−m²=(∂−m)(∂+m): e^{±mx}; Green di −∂²+m² su ℝ: e^{−m|x|}/2m (verificato). r·I commuta con tutto; E_int additivo = (e^{rt}−1)(S−I)u0. ★ · `s05` 4/4 PASS.

### K7 — Euler–Cauchy / x∂_x (C2.6ᵈ-a / C2.4)
x²∂²+ax∂+b; x=e^y ⇒ coeff. costanti; Mellin x∂ ↦ s. Classe x^s, x^s log x [DIM-F: Coddington–Levinson cap. 4]. Singolare regolare in 0, invarianza di scala. ★ · `s06` PASS.

### K8 — Hermite / oscillatore / OU / Mehler (C2.6ᵈ-b / C2.5, C2.30)
h_n=H_n e^{−x²/2}, (−∂²+x²)h_n=(2n+1)h_n, base ortonormale completa di L²(ℝ). OU: e^{−nt}He_n e^{−x²/2}. Mehler (2π sinh2t)^{−1/2}exp(−[(x²+y²)cosh2t−2xy]/(2sinh2t)) risolve ∂_t−∂²+x² [DIM-F: DLMF §18.18; verificato]. Termini non commutanti ma generano sl(2) ⇒ Wei–Norman, E_int in forma chiusa. Gram = identità; versione esatta della "gaussiana" di B5. ★◆ · DLMF 18; Courant–Hilbert I cap. V; Lebedev · `s06` PASS.

### K9 — Legendre (C2.6ᵈ-c)
∂((1−x²)∂)+n(n+1), S–L singolare su [−1,1]; P_n, Q_n (Q_0=artanh x, Q_1=x artanh x−1); {P_n} completo, ⟨P_m,P_n⟩=2δ_mn/(2n+1); separazione del Laplaciano sferico (r^lP_l, r^{−l−1}P_l armoniche); singolari regolari ±1 con esponenti 0,0. ★◇ · DLMF 14, 18 · `s06`, `s09` PASS.

### K10 — Bessel e Laplaciano polare/cilindrico/sferico (C2.6ᵈ-d / C2.56)
J_n(kr)e^{inθ} (e Y_n) per Helmholtz; armoniche r^{±n}e^{inθ}, log r; cilindriche J_n(kr)e^{inθ}e^{kz}, I_n(kr)e^{inθ}cos kz; sferiche r^lP_l, r^{−l−1}P_l, 1/r; calore radiale e^{−k²t}J_0(kr), nucleo 2D e^{−r²/4t}/4πt. n numerabile e k continuo su ℝ²; su disco k=j_{n,m}. Frobenius: indiciale r²−ν²; ν=½ ⇒ sin x/√x. Fondamentali −(2π)^{−1}log r, (4πr)^{−1}. Radiale e angolare non commutano (fattore r^{−2}) ma separano per SO(2). Ortogonalità di Fourier–Bessel con peso x (verificata numericamente). ★◇ · DLMF 10; Watson; MIT 18.303 L19–28 · `s06`, `s07` 20/20, `s09` PASS.

### K11 — Trave di Euler–Bernoulli ∂_t²+∂_x⁴ (C2.33, ★ 1D)
τ²+ξ⁴=(τ−iξ²)(τ+iξ²), fattori commutanti e coprimi ⇒ ker = ker(∂_t−i∂²)+ker(∂_t+i∂²), intersezione {a+bx} (dim 2, verificata). Modi cos(k²t)sin(kx); stazionario cos, sin, cosh, sinh(kx); nucleo = somma dei due Fresnel coniugati (verificato). Caso modello di split additivo esatto. ★◇ · Polyanin–Nazaikinskii 2016; Graff 1975 · `s08` 12/12 PASS.

### K12 — Onde
(τ−cξ)(τ+cξ); d'Alembert [Evans §2.4.1]; intersezione = costanti; split additivo esatto. `s10` PASS.

### K13 — Sturm–Liouville (C2.13)
−(py′)′+qy=λwy. Regolare: autovalori semplici → ∞, n-esima autofunzione con n−1 zeri, base ortonormale di L²_w [DIM-F: Zettl 2005 (numeri dei teoremi da riscontrare); Coddington–Levinson cap. 7]. Singolare: Weyl (punto-limite/cerchio-limite), Titchmarsh–Kodaira. Identità di Lagrange (verificata) ⇒ ortogonalità. Forma di Liouville −y″+Qy=λy ↔ Problema 1, Gel'fand–Levitan (R4). Per C1: 𝓗=L²_w, base numerabile. ★◆ · `s09` 8/8 PASS.

### K14 — V V_x (C2.7ᵈ, ▲)
Burgers via Cole–Hopf u=−2νφ_x/φ: Burgers[u]=−2ν∂_x(heat[φ]/φ) (verificato); fronte da φ=1+e^{−kx+νk²t}. Hopf 1950; Cole 1951 · `s12` 2/2 PASS.

## 3. C4: enunciati
**[R3-L1] Lemma (DIM).** L1, L2 commutanti, u=a+b, L1a=0, L2b=0 ⇒ ((L1+L2)u=0 ⟺ L2a=−L1b=:w); allora w∈ker L1∩ker L2 e u∈ker(L1L2). Corollario: S:=ker(L1+L2)∩(ker L1+ker L2) ⊆ ker(L1+L2)∩ker(L1L2); uguaglianza per simboli coprimi quando vale G2 (R2). Coincide con Sol(L1+L2, L1²) di R2 (modulo L1+L2, L1L2 ≡ −L1²).

**[R3-P1] (DIM).** L1=∂_t+c∂_x, L2=−D∂²: S=span{1, s, s²+2Dt, s³+6Dts}, dim 4. Dim.: ker L1∩ker L2=span{1,s}; per il lemma −Dg″ ∈ span{1,s} ⇒ g cubico; b determinato modulo span{1,s}. Controllo: Gröbner {τ+cξ−Dξ², ξ⁴}, lunghezza 4 = 2·I_0(τ+cξ, ξ²) (formula di R2).

**[R3-C1] FALSO: A8 additivo.** G(t,x−ct) ∈ ker L ma ∉ S; ker L ha dimensione infinita, la parte decomponibile dimensione finita.

**[R3-P2] Somme commutanti.** u=S1S2u0, E_int=(S1−I)(S2−I)u0, ∂_t log û=a1+a2; con N termini 2^N addendi (l'O(eⁿ) di B2) contro O(N) nel log-simbolo; coincide con la Möbius di RT-S1c.

**[R3-P3] Fattorizzazione.** Trave, onde, Helmholtz, Laplace in (t,x) si spezzano additivamente in modo esatto modulo un'intersezione di dimensione finita; su 𝕋 lo split fallisce in caso di risonanza (R2).

| Regime | Esempi | E_int |
|---|---|---|
| fattorizzazione | onde, trave, Π P_j | 0 modulo intersezione finita |
| somma commutante | avvezione–diffusione, reazione–diffusione, KdV–Burgers lineare | moltiplicativo; additivo bilineare |
| non commutante, algebra di Lie finita | OU/Mehler | forma chiusa (Wei–Norman) |
| non commutante, algebra infinita | — | serie di commutatori (R5) / Problema 1 |

## 4. Mappatura sugli item
- C2: K1–K14 coprono C2.1ᵈ–7ᵈ e C2.1, 4, 5, 6, 7, 10, 11, 13, 33, 56.
- C4.1: A8 FALSA come scritta (R3-C1). C4.2: confermata su trave e onde. C4.3: R3-P2. C4.4: numerabile su intervalli/𝕋, continuo su ℝ, salvo la base di Appell del calore.
- C1.0/C1.4: Gram e duali per Hermite, Legendre, Fourier–Bessel, polinomi del calore.
- II/F1: ERF = azione del simbolo; Mellin, Hankel, Hermite come "encoder" analitici per i coeff. variabili.

## 5. Stato
Noto: K1–K13. Dimostrato qui: R3-L1, R3-P1, R3-C1, R3-P2; trave = coppia di Schrödinger. Falso: A8 additivo; "ogni termine ha una classe propria". Aperto: open_questions.md.

## 6. Integrazione col cluster
- PR-C2a–d: nessuna scheda pervenuta alla consegna.
- PR-C2e: components_matrix.md integrata, concordanza piena.
- R2: "parte additiva = Sol(L1+L2, L1²), dim 2·ΣI_p" coincide con R3-L1/P1; caveat di risonanza su 𝕋. D-moduli delle funzioni speciali inviati: Hermite ∞ irregolare ρ=2; Airy ρ=3/2; Bessel 0 regolare e ∞ ρ=1; Legendre fuchsiana a 3 punti; le somme richiedono LCLM con singolarità apparenti.
- R4, righe identificabili da una soluzione: ODE ⟺ annullatore minimo di grado = ordine; evoluzione: da un modo con κ≠0; calore/Airy/Fresnel tra tutte le P: più di n·deg P punti spettrali; polinomi del calore e dispersivi NON identificano (ideale 0-dimensionale); somme finite di modi non identificano (e^{−t}cos x+e^{−4t}cos 2x risolve anche u_tt+5u_t+4u=0); trave e onde: Z(u) infinito su entrambi i fattori; coeff. C^∞ liberi: mai. R4 concorda con R3-L1.
- NEW-ROUTE: RT-R3a RW-DUAL.
- Da verificare sul testo: numeri dei teoremi in Zettl, equazione DLMF di Mehler, ortogonalità continua di Ai (Vallée–Soares).
