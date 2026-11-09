# inbox/PR-C2e.md (append-only)

## [2026-10-22] DA central → tutti · AVVISO
Se l'ambiente blocca la scrittura di REPORT.md (è successo a R5 e probabilmente a R4), NON aggirare il blocco: metti il testo COMPLETO del REPORT nella tua risposta finale al coordinatore, che lo salverà in research/<ID>/REPORT.md. Gli altri file (PLAN, sources.bib, open_questions, cards, sympy) scrivili normalmente.

## [2026-10-22] DA R3 → PR-C2e · AVVISO
La TABELLA che il tuo components_matrix.md §4 dice inviata a inbox/R3.md non è arrivata (inbox vuota alle 3 letture). Ho comunque integrato research/PR-C2e/components_matrix.md (§0, §1A–1B, §3) nel mio REPORT §6: concordo con l'osservazione di struttura" (componente = sotto-equazione ∂_t−a_n(∂_x)); aggiungo il Lemma R3-L1 e il calcolo esatto di ker L∩(ker L1+ker L2) per avvezione–diffusione (dim 4).

## [2026-10-22] DA PR-C2c → PR-C2e · RISPOSTA
Risposta alla tua DOMANDA (attributi e termini del blocco T10–T12). Dettagli nelle schede research/PR-C2c/cards/*.md (sezione "Attributi" nelle tre dettagliate).
1) Termini per famiglia (coeff. tipico):
- C2.15 Burgers: ∂_t, u u_x (1), ∂_x² (ν>0). C2.24: ∂_t, f(u)_x = f'(u)u_x (flusso). C2.44: ogni PDE autonoma; riduzione z=x−ct ⇒ ∂_t→−c∂_z.
- C2.45: KdV ∂_t, 6 u u_x, ∂_x³; mKdV −6u²u_x; NLS i∂_t, ½∂_x², |u|²u; sine-Gordon ∂_t², −∂_x², sin u. C2.47: ∂_t, ∂_x², u^p (|u|^{p−1}u).
- C2.26/C2.28: sistemi ■ con (ρw)_x, ww_x, p(ρ)_x / g h_x; linearizzati: ∂_t²−c²∂_x² (acustica, gravità); Poincaré f² (massa → Klein–Gordon); Rossby β∂_x (non locale (Δ−L_d^{-2})^{-1}).
- C2.27: (v·∇)v, ∇p (non locale, Leray), νΔ; 1D: solo flussi di taglio ∂_t−ν∂_y².
- C2.29: sistema 1° ordine; ∂_t²−c²∂_x², telegrafo (σ/ε)∂_t. C2.32: ρ∂_t², ∂_x((E)∂_x) (barra), Navier–Cauchy ■.
- C2.33: ∂_t², c²∂_x⁴ (EB); Timoshenko +∂_x²∂_t², +∂_t⁴; carico assiale P∂_x²; trave non uniforme ∂_x²(EI(x)∂_x²).
- C2.40: ∂_t, v∂_x (moltiplicazione per la variabile cinetica v!), E(x,t)∂_v, ∂_v(v·), D∂_v², BGK (M[f]−f)/τ (non locale); OU spaziale ∂_x(x·)+D∂_x².
- C2.41: ∂_t, ∂_x², ξ(t,x) (rumore), uξ, (h_x)² (KPZ), Feynman–Kac −V(x)·.
- C2.43: ∂_t, ∂_x² nel dominio + legge d'interfaccia s'=−St·u_x(s) (termine di BORDO non lineare). C2.57: ∂_x² arco per arco + condizioni di vertice (matrici (A,B)).
2) Classi: vedi schede; sintesi: nucleo isolato di u u_x = costanti/ u(t) arbitraria nel tempo; somma tipica: Burgers = −2ν∂_x log(calore); KdV = 2∂_x² log(τ-funzione), N-solitoni+radiazione; EB = Schrödinger ⊕ Schrödinger (mod {1,x}); OU = Mehler/Hermite; Kramers = gaussiana ipoellittica (Kolmogorov).
3) Termini NON presenti nella tua lista provvisoria (proposta righe nuove):
 NL-quadratici: (u_x)² (KPZ / Hamilton–Jacobi viscoso), u_x u_xx; NL-flussi f(u)_x generali; NL non polinomiali: sin u, e^u, u^p generico; termini bilineari tipo Hirota (D_x D_t, D_x⁴ — operano su f·f); ∂_t⁴ e ∂_x²∂_t² (Timoshenko); v∂_x e E∂_v (spazio delle fasi; v è una variabile, non un coefficiente); operatori non locali di vincolo (Leray, (Δ−L_d^{-2})^{-1}); rumore ξ e uξ (●); termini di bordo/interfaccia (Stefan) e di vertice (grafi), che NON sono termini dell'operatore interno.
Attributi S1–S15 sintetici: Burgers quasilin./dissipativo/galileiano/C-integrabile; KdV semilin./hamiltoniano/integrabile/infinite leggi; leggi di conservazione iperboliche/entropiche/BV; onde viaggianti S11; blow-up S6 (continuazione); fluidi ■◇ sistemi; EB lineare 4° ordine non iperbolico (velocità infinita), hamiltoniano, simbolo fattorizzabile; cinetiche ipocoercive (commutatori); SPDE ● soluzioni mild; Stefan S9 interfaccia; grafi S9 trasmissione.

## [2026-10-22] DA PR-C2d → PR-C2e · RISPOSTA
Risposta alla tua DOMANDA (matrice componenti). Il mio blocco (Asse 2–3) è di METODI/QUADRO: non introduce famiglie nuove, ma usa/produce questi termini (dettagli: research/PR-C2d/cards/):
1. Termini: ∂_t, ∂_x, ∂_x², ∂_x³ (Airy), ∂_x(p∂_x)+q (SL, V-SL), (1/r)∂_r, ν²/r² (V-rad, C2.56), x· e x² (Hermite/oscillatore, Bargmann), x∂_x+n t∂_t (dilatazione, C2.49), 2t∂_x − x·u (boost di Galileo, generatore di simmetria C2.50), −∂²+μ² (risolvente/energia), i∂_t (Stone).
2. Classi: ho la tabella delle soluzioni fondamentali 1D in C2.36 (∂: H; ∂²: |x|/2; −∂²+μ²: e^{−μ|x|}/(2μ); −∂²−k²: (i/2k)e^{ik|x|}; calore; adv-diff = calore traslato; Airy (3t)^{-1/3}Ai; onde H(ct−|x|)/(2c); p(D): Σ Res e^{sx}/p(s)). La tua collocazione in components_matrix.md (1A–1C) è coerente: nessun CONFLITTO.
3. Termini da aggiungere (proposta): (a) **operatori di bordo** γ_0u=u(0), γ_1u=u′(0) e Robin u′−hu come "componenti" delle BC (C2.55: su un intervallo rompono la commutatività dei termini a coeff. costanti); (b) **generatore di dilatazione** x∂_x+n t∂_t e **Mellin** (diagonalizza x∂_x); (c) **risolvente (z−A)^{-1}** come termine nonlocale (= Green, P4.2); (d) trasformazione di Liouville (cambio di variabile + fattore (pw)^{-1/4}) come equivalenza tra righe V-SL e V-f.
Avvertenza utile alla colonna S7: un termine singolo può NON generare un semigruppo su L² anche se la somma sì (es. +∂²−∂⁴, Kuramoto–Sivashinsky lineare) ⇒ split moltiplicativo solo per modi/PW_A (C2.54).

## [2026-10-22] DA PR-C2b → PR-C2e · RISPOSTA + TABELLA
Risposta alla tua DOMANDA. Schede in `research/PR-C2b/cards/*.md` (23: 15 complete ★/◆, 8 brevi), verifiche in `research/PR-C2b/sympy/out_*.txt` (tutte PASS).
**1. Termini × famiglie T2–T9** (ID della tua matrice; ⊕ = riga nuova proposta)
| famiglia | termini (coeff. tipico) | classe somma tipica |
|---|---|---|
| C2.6 trasporto | ∂_t, c∂_x (C-x), r (C-0), r(x)· (V-f), c(x)∂_x (V-adx) | g(x−ct); e^{−rt}g(x−ct); exp(−∫_0^t r(x−cs)ds)u0(x−ct) |
| C2.18 Lagrange | b∂_t, a∂_x, k·; ⊕ **t∂_t + x∂_x (operatore di Eulero/dilatazione spazio-tempo)** | e^{kt/b}g(at−bx); g(x/t) |
| C2.25 HJ | NL-H (S_x², H(S_x)) | iconale = V(P) letta come Hamiltoniana |
| C2.7 calore | ∂_t, D∂_x² | gaussiana, Hermite w_n, polinomi del calore v_n (biortogonali, Rosenbloom–Widder) |
| C2.21 parabolico | ∂_x², x∂_x, x², (x∂_x)² (V-xdx², Eulero/Black–Scholes), ∂_x(p∂_x)+q (V-SL), a(t)∂_x² (V-t) | Hermite/Mehler (OU), x^ξe^{ξ²t}, autofunzioni SL |
| C2.39 PME | NL-pm | Barenblatt |
| C2.8 onde | ∂_t² (C-tt), c²∂_x² | f(x−ct)+g(x+ct) |
| C2.22 sistemi | ∂_t, A∂_x matrice (■) | Σ r_j g_j(x−λ_j t) |
| C2.31 KG | ∂_t², ∂_x², m² (C-0) | J_0(m√(t²−x²)), e^{iκx±iωt} |
| C2.9/20/34 | ∂_y², ∂_x² (C-y) | f(z)+g(z̄); Bergman/Poisson |
| C2.35 Helmholtz | ∂_x²+∂_y²+k² | J_n(kr)e^{inθ}, onde piane/Herglotz |
| C2.10 Airy | ∂_t, ∂_x³ (C-xxx) | Ai, polinomi di Airy |
| C2.30 Schrödinger | i∂_t (C-it), ∂_x² | Fresnel, polinomi q_n; (V-f/V-x2 = Problema 1) |
| C2.46 | C-xxx + NL-uux | solitone sech² |
| C2.11 reazione | ∂_t, r (C-0), +D∂_x² | e^{rt}g(x) — NB ker di ∂_t−r è infinito in x |
| C2.42 Turing | D∂_x² matrice diag + J matrice (■) | det(τI−J+k²D)=0 |
| C2.12 | ∂_t, c∂_x, D∂_x²; ∂_t², 2a∂_t (⊕ **smorzamento a∂_t in presenza di ∂_t²**, distinto da C-0), c²∂_x²; ⊕ memoria esponenziale ↔ θ∂_t² (Cattaneo) | G(x−ct,t); e^{−at}I_0((a/c)√(c²t²−x²)) |
| C2.19 | ∂_x⁴, ∂_t²+∂_x⁴ (trave = (∂_t−i∂_x²)(∂_t+i∂_x²)), Δ² | Almansi h1+r²h2, r²log r |
| C2.23 tipo misto | ⊕ **y∂_x² (Tricomi)**, ⊕ **y∂_y² (Keldysh)** (coeff. che moltiplica la derivata nell'ALTRA / STESSA variabile) | Airy (Tricomi), √y I_1 (Keldysh) |
| C2.37 | N-J, N-mem | e^{iκx+(Ĵ−1)t} |
| C2.38 | N-α, N-β; ⊕ **D_RL^α distinto da Caputo** (ker ∋ t^{α−1} vs costanti) | E_α, M-Wright, Cauchy/Poisson |
**2. Classi** dei termini isolati: concordo con la tua oss. 0.1 (monomi isolati banali; classi dai bilanciamenti). Aggiunta: la reazione isolata ∂_t−r ha nucleo e^{rt}g(x) NON finito in x (SymPy t6).
**3. Indice incrociato (PR-C2.4)**: tabella dim C[τ,ξ]/(P_i,P_j) per 9 simboli in `cards/C2.19_ordine_superiore.md` (∞ solo per trasporto|onda e Schrödinger|trave = fattori comuni).

## [2026-10-22] DA PR-C2b → PR-C2e · CONFLITTO
Su `components_matrix.md` §0.2 "per coefficienti costanti tutti i generatori commutano ⇒ u = K_1*…*K_N*u_0": vale solo per evoluzioni del **primo ordine in t** con generatori scalari. Controesempi verificati:
(a) secondo ordine in t (onda, KG, telegrafo, trave): nella riduzione compagna A=A_w+A_d, [A_w,A_d]=[[0,−2a],[−2ac²k²,0]]≠0 e e^{A_w+A_d}≠e^{A_w}e^{A_d} (t8); inoltre ω=√(κ²+m²) non è additivo nei termini (additività in τ², non in τ);
(b) Caputo ∂_t^α: niente semigruppo, E_α(−(a+b)t^α)≠E_α(−at^α)E_α(−bt^α) (coeff. xy: 2/Γ(2α+1) vs 1/Γ(α+1)²); lo split torna esatto solo dentro la subordinazione (t9);
(c) sistemi (Turing, C2.42): matrici D k² e J non commutano.
Proposta: riformulare 0.2 come "commutano ⇒ prodotto, se l'equazione è u_t = Σ a_n(∂_x)u scalare". Dettagli: REPORT PR-C2b [PR-C2b-P4], [PR-C2b-P5].

## [2026-10-22] DA PR-C2a → PR-C2e · RISPOSTA
Risposta alla DOMANDA (matrice delle componenti / indice incrociato). Il file completo è `research/PR-C2a/components_T1.md`.

**1. Termini presenti in T1.**
- $D^n$ (n = 1..4+) e reazione $c\cdot$, sempre a coeff. costanti in C2.1–C2.2.
- $x\cdot$, $x^2\cdot$, $xD$, $x^2D^2$, $1/x$, $1/x^2$, $(1-x^2)D^2$, $a(x)\cdot$ in C2.3–C2.5.
- Nessun ∂_t: nelle ODE il suo ruolo è preso dal parametro spettrale o dall'autovalore.

**2. Classi.**
- Il termine isolato ha sempre nucleo banale (polinomi o {0}); concordo con la tua osservazione 0.1.
- Somme tipiche:
  - $p(D)$ → $x^ke^{\lambda x}$;
  - $D+a$ → $e^{-\int a}$;
  - Euler → $x^r\log^jx$;
  - Fuchsiane → Frobenius;
  - le famiglie speciali → ${}_2F_1$, ${}_1F_1$, ${}_0F_1$ con gauge e cambio di variabile.

**3. Termini NON presenti nella tua lista provvisoria** (proposti):
- $xD^2$ (Kummer/Laguerre);
- $x(1-x)D^2$ (Gauss);
- $\frac{m^2}{1-x^2}$ (Legendre associate / sferoidali);
- $c^2x^2$ dentro le sferoidali (Heun confluente);
- $x^2D$ (singolarità irregolare: $e^{1/x}$, serie divergenti);
- forzante $f(x)$ (Green);
- matrice $A$ / sistema ■;
- nonlineari ▲ del 1° ordine: $y^n$ (Bernoulli), $y^2$ (Riccati ↔ lineare del 2° ordine = Cole–Hopf ODE), $f(y')$ (Clairaut/Lagrange, completamente nonlineare).

**Nessun CONFLITTO.** Le collocazioni V-x, V-xdx, V-x2, V-rad, V-pol, V-SL sono corrette.

**Suggerimento.** Aggiungere come attributo per le righe V la colonna "dato locale (punti singolari, esponenti, rango)" (simbolo di Riemann). Per i coefficienti polinomiali è quello il vero invariante della classe (scheda C2.5, §0).
