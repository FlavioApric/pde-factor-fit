# KA input — OPF5D-T6 (Burgers viscoso periodico: ‖S(t)u_0 − v(t)‖_{L¹} = O(√ν) dalla formula di Cole–Hopf)
Estratto verbatim da work/OP-F5D/PROOF_PACKAGE.md §6 (notazioni, T6) e da work/S4-TERM/PROOF_PACKAGE.md (enunciato S4T-L2). Bersaglio: T6, passi (1)–(5) e la stima finale; (6) è un corollario.

## Quadro
Burgers viscoso u_t + uu_x = νu_xx su 𝕋 = ℝ/2πℤ; S(t)u_0 = soluzione classica (Cole–Hopf, [F2] DIMOSTRATO: u(t,x) = (x − E_{μ_x}y)/t con μ_x(dy) ∝ exp(−Φ_x(y)/2ν)dy su ℝ). v = formula di Lax–Oleinik. E^{mult}_{AB}, S_A (calore), S_B, S4T-T3(iii),(vi): da S4-TERM, usati solo nel passo (6).
Notazioni di S4-TERM §2/§6: u_0 ∈ C¹(𝕋) reale (basta Lipschitz), U_0(y) = ∫_0^yu_0, Φ_x(y) = U_0(y) + (x−y)²/2t, u = S(t)u_0 = (x − E_{μ_x}y)/t (Cole–Hopf, [F2] DIMOSTRATO), v(t,x) = (x − a(x))/t (Lax–Oleinik, a(x) ∈ argmin Φ_x, S4T-L2). M := 1/t + ‖u_0′‖_∞.

## Fatto importato (NON da auditare): S4T-L2
**Ipotesi.** $u_0\in C^1(\mathbb R)$ $2\pi$-periodica reale, $t>0$, $\Phi_x:=\Phi_{t,x}$.
**Tesi.** (a) $\arg\min\Phi_x$ è un compatto non vuoto; ogni minimizzante soddisfa $x=a+tu_0(a)$, $1+tu_0'(a)\ge0$, $|x-a|\le t\|u_0\|_\infty$. (b) Se $x_1<x_2$, $a_i\in\arg\min\Phi_{x_i}$, allora $a_1\le a_2$. (c) Con $a^\pm(x):=\max/\min\arg\min\Phi_x$, per ogni selezione $a(\cdot)$: $\lim_{x'\downarrow x}a(x')=a^+(x)$, $\lim_{x'\uparrow x}a(x')=a^-(x)$. Quindi $v(t,\cdot)=(x-a(x))/t$ ha limiti laterali $v(t,x^\pm)=(x-a^\pm(x))/t$ in ogni punto ed è continua in x sse $\arg\min\Phi_x$ è un punto. (d) Se $t>t^*$, l'aperto periodico $N_t:=\{a:1+tu_0'(a)<0\}$ è non vuoto; per ogni sua componente $I=(\alpha,\beta)$ esiste $x_0$ con $a^-(x_0)\le\alpha<\beta\le a^+(x_0)$; il salto $D:=v(t,x_0^-)-v(t,x_0^+)=(a^+-a^-)/t\ge|I|/t>0$. In particolare $S_B(t)u_0$ non ha rappresentante continuo per ogni $t>t^*$.

## Enunciato e prova da attaccare
### [OPF5D-T6] Stima L¹ della viscosità evanescente dalla formula di Cole–Hopf — PROVA SCRITTA
*Enunciato.* Per ogni t > 0, ν > 0:
**‖S(t)u_0 − v(t)‖_{L¹(𝕋)} ≤ 8π√(2ν·log(1 + t‖u_0′‖_∞)/t).**
Di conseguenza S4T-T3(iv) vale **senza [F3]**: ‖E^{mult}_{AB}(t)‖_{L¹} ≤ 8π√(2ν log(1+t‖u_0′‖)/t) + 2√(νt/π)·TV(v(t)) = O(√ν), e con il limite inferiore (iii) **‖E^{mult}_{AB}(t)‖_{L¹} = Θ(√ν)** per t > t*; inoltre (v) ha il tasso ‖E^{add}(t)‖_{L¹} = O(√ν) (per (vi)).
*Prova.* (1) *Potenziali convessi.* h(y) := U_0(y) + y²/2t; G_ν(x) := 2ν log∫_ℝexp((xy/t − h(y))/2ν)dy, G_0(x) := sup_y(xy/t − h(y)). Entrambe convesse in x (log-somma-esponenziale; sup di affini). Φ_x(y) = h(y) − xy/t + x²/2t, quindi G_ν′ = E_{μ_x}y/t, G_0′ = a(x)/t q.o. (Danskin), e u − v = −(G_ν′ − G_0′)·1 = (G_0′ − G_ν′). Periodicità: a(x + 2π) = a(x) + 2π.
(2) *Gap di Laplace.* G_ν − G_0 = 2ν log I(x), I(x) := ∫exp(−D_x(y)/2ν)dy, D_x(y) := Φ_x(y) − min Φ_x = h(y) − xy/t + G_0(x) ≥ 0. *Limite inferiore:* Φ_x″ = u_0′ + 1/t ≤ M e Φ_x′(a) = 0 ⇒ D_x(y) ≤ M(y−a)²/2 ⇒ I(x) ≥ c_0 := √(4πν/M). Pongo ε(x) := 2ν log(I(x)/c_0) ≥ 0, cioè G_ν − c − G_0 = ε con c := 2ν log c_0.
(3) *Forte convessità di G_0.* Per x_1 < x_2 e minimizzanti a_i: a_1 ≤ a_2 (S4T-L2(b)) e x_i = a_i + tu_0(a_i) (S4T-L2(a)); y ↦ y + tu_0(y) è (tM)-lipschitziana: x_2 − x_1 ≤ tM(a_2 − a_1). Quindi G_0′ − x/(t²M) = (a(x) − x/(tM))/t è non decrescente: G_0 è (1/t²M)-fortemente convessa, e per ogni y fissato x ↦ D_x(y) è fortemente convessa, ≥ 0: D_x(y) ≥ (x − x_y)²/(2t²M) (x_y punto di minimo).
(4) *Media di I (Fubini + periodicità).* D_{x+2π}(y + 2π) = D_x(y). ∫_0^{2π}I(x)dx = ∫_0^{2π}dx∫_ℝdy e^{−D_x(y)/2ν} = ∫_0^{2π}dy∫_ℝdx e^{−D_x(y)/2ν} ≤ 2π√(4πνt²M). Per Jensen (log concavo): ∫_𝕋ε = 2ν∫_𝕋log(I/c_0) ≤ 4πν·log((2π)^{−1}∫_𝕋I/c_0) ≤ 4πν·log(tM). (tM = 1 + t‖u_0′‖ ≥ 1.)
(5) *Derivate di convesse vicine.* f := G_ν − c, g := G_0, f − g = ε ≥ 0. Per h > 0: f′(x) ≤ (f(x+h) − f(x))/h ≤ (g(x+h) − g(x))/h + ε(x+h)/h ≤ g′(x+h) + ε(x+h)/h e f′(x) ≥ (f(x) − f(x−h))/h ≥ g′(x−h) − ε(x−h)/h. Quindi |f′ − g′|(x) ≤ g′(x+h) − g′(x−h) + (ε(x+h) + ε(x−h))/h. Integrando su un periodo: ∫_0^{2π}(g′(x+h) − g′(x−h))dx = ∫_{−h}^{h}(g′(x+2π) − g′(x))dx = 4πh/t. Dunque ‖u − v‖_{L¹(𝕋)} ≤ 4πh/t + 8πν log(tM)/h; con h = √(2νt log(tM)) si ottiene 8π√(2ν log(tM)/t). (Se tM = 1, u_0 costante e u = v.)
(6) *(iv).* E^{mult}_{AB} = (u − v) − (S_Av − v) e ‖S_Av − v‖_{L¹} ≤ 2√(νt/π)TV(v(t)) (S4T-T3 prova (iv)); TV(v(t)) < ∞ (v = u_0∘a, a monotona). Limite inferiore: S4T-T3(iii). (v): (vi) + (5). ∎
