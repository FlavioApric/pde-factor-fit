# MATRICE DELLE COMPONENTI — PR-C2.5 (la lista delle componenti chiesta da A6)

Agente: PR-C2e · 2026-10-22 · versione 1 (da integrare con le schede PR-C2a/b/c/d quando compaiono).
Notazione `NOTAZIONE.md`: simbolo con `∂_t↔τ`, `∂_x↔ξ` (Laplace/Ehrenpreis, `e^{τt+ξx}`); per Fourier `ξ = iκ`. Per un'equazione di evoluzione `u_t = a(∂_x)u` il **generatore** è `a(∂_x)` e il suo nucleo di semigruppo è `K(t,x) = (2π)^{-1}∫ e^{iκx + t a(iκ)} dκ`.
Controlli simbolici: `sympy/check_components.py` (output in `sympy/check_components.out.txt`; tutti i residui = 0).

## 0. Osservazione di struttura (risultato principale per A6/C2)
1. **Il nucleo di un monomio isolato è banale** (polinomi: `ker ∂_x^n = {Σ_{j<n} a_j(t)x^j}`, `ker ∂_t = {g(x)}`). Le "classi di funzioni" di A5 nascono solo da **bilanciamenti**: un termine temporale (`∂_t`, `∂_t²`, `i∂_t`, `∂_t^β`) contro un termine spaziale. Quindi l'unità corretta di "componente" per G★ è la coppia **(derivata temporale, generatore spaziale a_n(∂_x))**, cioè la sotto-equazione a un termine `∂_t − a_n(∂_x)`, il cui nucleo `K_n(t,·)` è la classe `{e_{n,i}}`. Per ODE (H0 caso `u=u(x)`) il ruolo di `∂_t` è preso dal parametro spettrale: la classe di `p(∂_x)` è `{x^k e^{λx} : p(λ)=0}`.
2. Con questa scelta, per coefficienti costanti tutti i generatori commutano ⇒ `u = K_1(t)*…*K_N(t)*u_0` (quadro moltiplicativo, §1.2-2b) e `∂_t log û = Σ_n a_n(iκ)` (additivo nel log-simbolo, G3). Le righe V (coefficienti variabili) introducono commutatori (§1.2-2c); le righe NL e N cambiano la natura dell'oggetto (vedi §3).

---

## 1. Catalogo dei termini elementari (righe)

Colonne: ID · termine · simbolo (coeff. costanti) · ruolo S7 (sim = dissipativo/crescita, antisim = conservativo) · **nucleo/classe della sotto-equazione a un termine** · decadimento `‖K(t)‖_∞` · tag · item principali.

### 1A. Lineari a coefficienti costanti (anello `ℂ[τ,ξ]`, commutano tutti)
| ID | termine | simbolo | S7 | classe (sotto-eq. a un termine) | decad. | tag | item |
|---|---|---|---|---|---|---|---|
| C-t | `∂_t` | `τ` | — | lato temporale del bilanciamento | — | ★ | tutte le evolutive |
| C-tt | `∂_t²` | `τ²` | — | `ker = a(x)+t b(x)`; con spazio: onde/travi | — | ★ | C2.8, C2.22, C2.31, C2.33 |
| C-it | `i∂_t` | `iτ` | — | Schrödinger (fattore i nel tempo) | — | ★ | C2.30 |
| C-0 | reazione `c·u` | `c` | sim | `u_t=cu`: `e^{ct}g(x)`; nucleo `e^{ct}δ(x)` | `e^{ct}` | ★ | C2.11, C2.12, C2.31 (massa), C2.1 |
| C-x | `∂_x` (con velocità c) | `ξ` | antisim | `u_t+cu_x=0`: `g(x−ct)`; nucleo `δ(x−ct)` | nessuno | ★ | C2.6, C2.12, C2.18, C2.22 |
| C-xx | `∂_x²` (D>0) | `ξ²` | sim | calore: `(4πDt)^{-1/2}e^{-x²/4Dt}`, Hermite | `t^{-1/2}` | ★ | C2.7, C2.12, C2.21, C2.41, C2.53 |
| C-ixx | `i∂_x²` | `iξ²` | antisim | Schrödinger: Fresnel `(4πit)^{-1/2}e^{ix²/4t}` | `t^{-1/2}` | ★ | C2.30, C2.10 |
| C-xxx | `∂_x³` | `ξ³` | antisim | Airy: `(3t)^{-1/3}Ai(x/(3t)^{1/3})` | `t^{-1/3}` | ★ | C2.10, C2.46, C2.45 (lineariz. KdV) |
| C-xxxx | `∂_x⁴` (segno −) | `ξ⁴` | sim | iperdiffusione: `F^{-1}[e^{-κ⁴t}]` (funzioni `₀F₂`, oscillante) | `t^{-1/4}` | ★ | C2.19, C2.33 (con `∂_t²`), Kuramoto–Sivashinsky (▲) |
| C-xn | `∂_x^n`, n≥5 | `ξ^n` | sim (n pari) / antisim (n dispari) | Airy generalizzate / iper-Airy | `t^{-1/n}` | ★ | C2.19 |
| C-tx | `∂_t∂_x` | `τξ` | — | `ker = a(t)+b(x)`; forma caratteristica dell'onda `u_{ηζ}=0` | — | ★ | C2.8 (coord. caratteristiche), C2.17 |
| C-txx | `∂_t∂_x²` | `τξ²` | — | pseudo-parabolico/Sobolev; BBM `u_t−u_{txx}` | — | ★▲ | C2.46 (BBM), C2.19 |
| C-y | `∂_y`, `∂_y²` (2ª var. spaziale) | `η`, `η²` | — | Laplace/Poisson; Tricomi | — | ◇ | C2.9, C2.20, C2.23, C2.34, C2.35 |

### 1B. Coefficienti variabili (algebra di Weyl `A_1 = ℂ⟨x,∂_x⟩`, `[∂_x,x]=1`)
| ID | termine | simbolo / trasformata che lo diagonalizza | classe | tag | item |
|---|---|---|---|---|---|
| V-x | moltiplicazione `x·` | in Fourier `x ↦ i∂_κ` (non è un moltiplicatore) | Airy (`y″=xy`); potenziale lineare (Avron–Herbst) | ★ | C2.5, C2.23 (Tricomi `y u_xx`), C2.30 |
| V-xdx | `x∂_x` (dilatazione) | Mellin: `x∂_x ↦ s` | potenze `x^r`, `x^r log x` (Euler–Cauchy) | ★ | C2.4, C2.49, C2.50, Ornstein–Uhlenbeck |
| V-x2 | `x²·` | Hermite (oscillatore) | Mehler; Hermite `H_n(x)e^{-x²/2}` | ★ | C2.5, C2.30, C2.7 |
| V-f | `f(x)·` (potenziale V) | — | dipende da f (Problema 1) | ● | C2.30, C2.11 variabile |
| V-adx | `a(x)∂_x` (velocità variabile) | caratteristiche `ẋ=a(x)` | `g(Ψ(x)−t)`, `Ψ′=1/a` | ★ | C2.6, C2.18 |
| V-SL | `∂_x(p(x)∂_x)+q(x)` | Sturm–Liouville | autofunzioni SL, nucleo `Σe^{-λ_n t}φ_nφ_n` | ★◆ | C2.13, C2.21, C2.4 |
| V-rad | `(ν/x)∂_x`, `ν²/x²` (radiale/singolare) | Hankel | Bessel `J_ν, Y_ν, I_ν, K_ν` | ★◇ | C2.5, C2.56, C2.8 (membrane), C2.31 |
| V-pol | coeff. polinomiali tipo `(1−x²)∂_x²−2x∂_x` | — | Legendre, Jacobi, Gegenbauer, Chebyshev, ipergeometriche (olonome) | ★◇ | C2.5, C2.13 |
| V-per | `q(x)` periodico | Floquet–Bloch | Hill/Mathieu, funzioni di Bloch | ◆ | C2.21′ (periodici), livello L0.5 della scala |
| V-t | coeff. dipendenti da t `a(t)∂_x²` | cambio di tempo `s=∫a` | come C-xx con `t→∫a` | ★ | C2.21 |

### 1C. Nonlocali (simboli non polinomiali; S8)
| ID | termine | simbolo | classe | tag | item |
|---|---|---|---|---|---|
| N-α | `−(−∂_x²)^{α/2}`, 0<α≤2 | `−|κ|^α` | leggi α-stabili (Lévy); α=1 Cauchy/Poisson `t/π(x²+t²)`; α=2 calore | ◆★ | C2.37, C2.38, C2.49′ |
| N-H | trasformata di Hilbert `H∂_x²` | `∝ i sgn(κ)κ²` | Benjamin–Ono (con `uu_x`): solitoni razionali (lorentziani) | ▲ | C2.46 |
| N-J | `J*u − u` | `Ĵ(κ)−1` | `e^{-t}Σ t^n J^{*n}/n!` (Poisson composto) | ◆ | C2.37 |
| N-β | Caputo `∂_t^β`, 0<β<1 | Laplace `s^β` | Mittag-Leffler `E_β(−κ²t^β)`, funzione M di Wright in x | ◆★ | C2.38 |
| N-mem | memoria `∫_0^t k(t−s)u_xx(s)ds` | Laplace `k̂(s)` | dipende da `k` | ◆ | C2.37 |

### 1D. Non lineari (▲; monomi del jet, G7)
| ID | termine | equazione tipo | linearizzazione esatta / classe | item |
|---|---|---|---|---|
| NL-uux | `u u_x` | Burgers, KdV | Cole–Hopf (Burgers → calore); IST (KdV); solitone `(k²/2)sech²(k(x−k²t)/2)` | C2.15, C2.45, C2.46 |
| NL-u2 | `u²`, `u(1−u)` | logistica, Fisher–KPP | fronti viaggianti (forma chiusa Ablowitz–Zeppetella per una velocità) | C2.11, C2.42 |
| NL-u3 | `u−u³` | Allen–Cahn | kink `tanh(x/√2)` | C2.42, C2.44 |
| NL-cub | `|u|²u` | NLS | IST; solitone `sech` | C2.30, C2.45, C2.46 |
| NL-sin | `sin u` | sine-Gordon | IST; kink `4 arctan e^{γ(x−vt)}` | C2.45 |
| NL-u2ux | `u²u_x` | mKdV | Miura → KdV | C2.45 |
| NL-pm | `(u^m)_xx` | mezzi porosi | Barenblatt (autosimile) | C2.39 |
| NL-pl | `(|u_x|^{p−2}u_x)_x` | p-Laplaciano | autosimili di tipo Barenblatt | C2.39 |
| NL-H | `u_x²`, `H(u_x)` | Hamilton–Jacobi, KPZ det. | `u_t=νu_xx+u_x²` → `e^{u/ν}` calore (Cole–Hopf); Hopf–Lax | C2.25, C2.18 |
| NL-up | `u^p` (sorgente) | blow-up | autosimili, Fujita | C2.47 |
| NL-flux | `f(u)_x` | leggi di conservazione | caratteristiche, shock (Rankine–Hugoniot) | C2.24, C2.15 |
| NL-chem | `(u v_x)_x` | Keller–Segel (sistema ■) | — | C2.42 |

### 1E. Termini affini / forzanti (non parte di `L`, ma della sotto-equazione)
| ID | termine | ruolo | item |
|---|---|---|---|
| F-src | sorgente `f(t,x)` | Duhamel `∫_0^t K(t−s)*f(s)ds`; esce dall'ipotesi `Lu=0` (H3) | C2.2, C2.6, C2.8, C2.36 |
| F-noise | `σẆ`, `uẆ` | rumore additivo/moltiplicativo (●, escluso da H3) | C2.41, C2.56′ |

---

## 2. Matrice di incidenza termine × famiglia (Asse 1)

Legenda: **●** termine che definisce la famiglia · **○** compare in varianti/membri · vuoto = assente.

| termine \ famiglia | T1 ODE | T2 1° ord. | T3 parab. | T4 iperb. | T5 ellitt. | T6 disp. | T7 reaz. | T8 misti | T9 nonloc. | T10 NL/integr. | T11 applicati | T12 stoc. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `∂_t` | (param. spettrale) | ● | ● | | | ● | ● | ● | ● | ● | ● | ● |
| `∂_t²` | | | | ● | ○ (t come var. spaz.) | | | ● | ○ (onde fraz.) | ○ (sine-Gordon) | ● (travi, elast.) | ○ |
| `i∂_t` | | | | | | ● | | | | ○ (NLS) | | |
| `c·u` | ● | ○ | ○ | ○ (KG) | ○ (Helmholtz) | ○ | ● | ● | | ○ | ○ | ○ |
| `∂_x` | ● | ● | ○ | ● (sistemi 1° ord.) | ● | ○ | | ● | | ● | ● | ○ |
| `∂_x²` | ● | | ● | ● | ● | | ○ (RD) | ● | ○ (α=2) | ● (Burgers) | ● | ● |
| `i∂_x²` | | | | | | ● | | | | ○ (NLS) | | |
| `∂_x³` | ● | | | | | ● | | ○ | | ● (KdV) | | |
| `∂_x⁴` | ● | | ○ (iperdiff.) | | ○ (biarmon.) | | | ● | | ○ (KS) | ● (travi/piastre) | |
| `∂_x^n`, n≥5 | ● | | | | ○ (poliarm.) | ○ | | ● | | ○ (gerarchie) | | |
| `∂_t∂_x` | | | | ○ (forma caratt.) | | ○ (BBM) | | ○ | | ○ | | |
| `x·`, `x∂_x`, `x²` | ● (C2.4, C2.5) | ○ | ○ (OU) | | | ○ (oscill.) | | ● (Tricomi) | | ○ (similarità) | | ○ (OU) |
| `f(x)·`, `∂_x(p∂_x)` | ● | ○ (vel. var.) | ● (C2.21) | ○ | ● (C2.20) | ○ (V(x)) | ○ | | | | ○ | |
| `1/x`, `1/x²` | ● (Bessel) | | ○ (radiale) | ○ (membrane) | ○ (polari) | | | | | | ○ | |
| `|ξ|^α`, `J*u−u` | | | ○ | | | | | | ● | ○ (BO) | ○ (cinetiche) | ○ (Lévy) |
| `∂_t^β` | ○ (ODE fraz.) | | ○ | ○ | | | | | ● | | | |
| `u u_x`, `f(u)_x` | ○ (Riccati via Cole–Hopf) | ● (trasp. NL) | ○ (Burgers) | ○ (sist. NL) | | ● (KdV) | | | | ● | ● (fluidi) | ○ |
| `u²`, `u³`, `u^p` | ● (Bernoulli, logistica) | | ○ (blow-up) | | ○ (ellitt. semil.) | | ● (Fisher) | | | ● | ○ | ○ |
| `|u|²u`, `sin u` | | | | ○ (sine-Gordon) | | ● (NLS) | | | | ● | ○ | |
| `(u^m)_xx`, p-Lapl. | | | ● (C2.39) | | | | | | | ○ | ○ (frontiera libera) | |
| `u_x²`, `H(u_x)` | ○ (Clairaut) | ● (HJ) | | | | | | | | ○ | ○ | ○ (KPZ) |
| sorgente / rumore | ● (forzate) | ○ | ○ | ○ | ● (Poisson) | | | | | | ○ | ● |

Riassunto per A6 — **lista minima delle componenti per il core ★** (scalare, 1D, lineare, coeff. costanti): `{∂_t, ∂_t², c·u, ∂_x, ∂_x², ∂_x³, ∂_x⁴, (∂_x^n), ∂_t∂_x}` più l'estensione `{i∂_t, i∂_x²}` (coeff. complessi) e `{|ξ|^α, ∂_t^β}` (◆, nonlocale). Livello successivo (L1/E1 della scala): `{x·, x∂_x, x², 1/x, f(x)·, ∂_x(p∂_x)}`. Livello ▲: `{uu_x, u², u³, |u|²u, sin u, (u^m)_xx, u_x²}`.

---

## 3. Combinazioni canoniche = famiglie come somme di righe (banco di prova di E_int)

| famiglia (item) | combinazione | simbolo `P(τ,ξ)` | fattorizzazione su `ℂ[τ,ξ]` | quadro di decomposizione | nucleo |
|---|---|---|---|---|---|
| avvezione–diffusione (C2.12) | C-t + C-x + C-xx | `τ+cξ−Dξ²` | irriducibile | somma di generatori **commutanti** ⇒ `K = δ(·−ct) * G_D(t)` (moltiplicativo); additivo nel log-simbolo | gaussiana traslata |
| reazione–diffusione lin. (C2.11+C2.7) | C-t + C-0 + C-xx | `τ−a−Dξ²` | irriducibile | commutanti ⇒ `K = e^{at}G_D(t)` | gaussiana × esponenziale |
| KdV–Burgers lineare | C-t + C-xx + C-xxx | `τ−Dξ²+ξ³` | irriducibile | commutanti ⇒ `K = G_D(t)*Ai_t` | convoluzione gaussiana–Airy |
| onde (C2.8) | C-tt + C-xx | `τ²−c²ξ²` | `(τ−cξ)(τ+cξ)` | **fattorizzazione coprima ⇒ split additivo esatto** (G2): `ker = ker(∂_t−c∂_x) ⊕ ker(∂_t+c∂_x)` | d'Alembert |
| trave E–B (C2.33) | C-tt + C-xxxx | `τ²+ξ⁴` | `(τ−iξ²)(τ+iξ²)` (verificato SymPy) | split additivo: **due Schrödinger** coniugate; il nucleo di Fresnel risolve la trave (residuo 0) | Fresnel ± |
| Laplace in (t,x) (C2.9) | C-tt + C-xx (segno +) | `τ²+ξ²` | `(τ−iξ)(τ+iξ)` | split additivo olomorfo ⊕ antiolomorfo | `f(x+it)+g(x−it)` |
| Helmholtz (C2.35) | C-xx + C-0 | `ξ²+k²` | `(ξ−ik)(ξ+ik)` | split additivo | `e^{±ikx}` |
| telegrafo (C2.12) | C-tt + C-t + C-xx | `τ²+2aτ−c²ξ²` | **irriducibile** (a≠0) | sostituzione `u=e^{-at}v` ⇒ KG `v_tt−c²v_xx−a²v=0` (verificato) | `e^{-at}I_0(a√(t²−x²/c²))` |
| Klein–Gordon (C2.31) | C-tt + C-xx + C-0 | `τ²−ξ²+m²` | irriducibile | — | `J_0(m√(t²−x²))` |
| ordine alto (C2.19) | `Π_j P_j` | prodotto | per costruzione | split additivo + `ker(P_i,P_j)` di dim. finita (G2) | somma dei nuclei dei fattori |
| oscillatore / OU (C2.5, C2.30, C2.41) | C-t + C-xx + V-x2 | — (Weyl) | — | **non commutanti** ma `{∂_x², x², x∂_x+½}` chiude un'algebra `sl(2)` (verificato: `[A,B]=4C`, `[C,A]=−2A`, `[C,B]=2B`) ⇒ Zassenhaus/Wei–Norman **in forma finita** | Mehler |
| potenziale lineare (C2.30, Airy) | C-t + C-ixx + V-x | — | — | `{∂_x², ∂_x, x, 1}` chiude (Heisenberg esteso, risolubile) ⇒ fattorizzazione finita (Avron–Herbst) | Fresnel × fase × traslazione |
| Euler–Cauchy (C2.4) | V-xdx + V-x2 ∂_x² | `p(s)` in Mellin | come C2.1 in `log x` | Mellin fa per i coeff. omogenei ciò che Fourier fa per i costanti | `x^r` |
| Bessel (C2.5) | C-xx + V-rad + C-0 | — | — | separazione in coordinate polari | `J_ν, Y_ν` |
| frazionaria (C2.38) | N-β + C-xx | `s^β+κ²` | — | commutanti (in κ); non semigruppo in t | Mittag-Leffler |
| Burgers (C2.15) | C-t + NL-uux + C-xx | — | — | Cole–Hopf `u=−2νφ_x/φ` ⇒ calore (verificato) | `−2ν ∂_x log(G*e^{…})` |
| KdV (C2.45) | C-t + NL-uux + C-xxx | — | — | IST; solitone verificato | `sech²` |

**Lettura per G★ (da verificare in Fase 3, non assunta):** tre regimi di E_int già visibili nella matrice — (i) **fattorizzazione** (onde, trave, Laplace, Helmholtz, C2.19): split additivo esatto, E_int = 0 modulo `ker(P_1,P_2)` di dimensione finita; (ii) **somma di generatori commutanti** (avvezione–diffusione, KdV–Burgers lineare, reazione–diffusione): split moltiplicativo, additivo solo nel log-simbolo; (iii) **non commutanti con algebra di Lie finita** (oscillatore, potenziale lineare, OU): E_int in forma chiusa via Wei–Norman; il caso generico `f(x)` (algebra infinita) è Problema 1. Proposto a R5 come classificazione dei casi di P1/P3.

## 4. Stato di integrazione con le schede
- PR-C2a/b/c/d: DOMANDA inviata (inbox, 2026-10-22). Al momento della consegna nessuna scheda `cards/*.md` era presente; la matrice è costruita dal testo del piano + fonti standard. Da riconciliare (aggiungere righe, correggere ●/○) alla prima versione delle schede.
- Inviata a R3 (inbox/R3.md, TABELLA).
