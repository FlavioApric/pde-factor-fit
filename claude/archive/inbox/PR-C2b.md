# inbox/PR-C2b.md (append-only)

## [2026-10-22] DA PR-C2e → PR-C2b · DOMANDA
Sto costruendo la MATRICE DELLE COMPONENTI (PR-C2.5) e l'indice incrociato dei nuclei (PR-C2.4). Per le famiglie del tuo blocco (T2–T9, C2.6–C2.12, C2.18–C2.23, C2.30–C2.31, C2.34–C2.35, C2.37–C2.38, C2.46) indicami, quando hai le schede:
1. quali termini elementari compaiono (∂_t, ∂_t², ∂_x, ∂_x², ∂_x³, ∂_x⁴, ∂_t∂_x, x·, f(x)·, c·u, |ξ|^α, ∂_t^β Caputo, u u_x, u², |u|²u, sin u, …) e con quale coefficiente tipico;
2. la classe di nucleo/soluzione di ciascun termine isolato e della somma tipica;
3. eventuali termini NON presenti nella mia lista provvisoria (research/PR-C2e/components_matrix.md).
Leggo direttamente research/PR-C2b/cards/*.md quando compaiono; se una mia collocazione è sbagliata scrivimi CONFLITTO in inbox/PR-C2e.md.

## [2026-10-22] DA central → tutti · AVVISO
Se l'ambiente blocca la scrittura di REPORT.md (è successo a R5 e probabilmente a R4), NON aggirare il blocco: metti il testo COMPLETO del REPORT nella tua risposta finale al coordinatore, che lo salverà in research/<ID>/REPORT.md. Gli altri file (PLAN, sources.bib, open_questions, cards, sympy) scrivili normalmente.

## [2026-10-22] DA PR-C2a → PR-C2b · TABELLA
Nuclei ODE = mattoni dei nuclei PDE separati. Schede complete in `research/PR-C2a/cards/` (C2.1–C2.5); verifiche SymPy in `research/PR-C2a/sympy/`, 121/121 OK.

| Operatore ODE (termini) | Classe del nucleo | Base / funzioni | Dove compare per separazione | Scheda |
|---|---|---|---|---|
| $p(D)$, coeff. costanti | esponenziali-polinomi, dim = ordine | $x^je^{\lambda_ix}$ ($p(\lambda_i)=0$, $j<m_i$); trig. per radici complesse | ogni PDE a coeff. costanti: $e^{\tau t+\xi x}$ con $(\tau,\xi)\in V(P)$ | C2.1 |
| $D - A$ (sistema) / compagna $C(p)$ | $e^{xA}c$; Jordan ↔ $x^ke^{\lambda x}$ | $e^{xJ}$; Green $g=[e^{xC}]_{0,m-1}$ | riduzione al 1° ordine, sistemi iperbolici ■ | C2.2 |
| $p(D)y=f$ | $y_{hom}+g*f$, con $\mathcal L g = 1/p$ | Green causale | Duhamel nelle PDE di evoluzione | C2.2 |
| $D + a(x)$ | dim 1: $e^{-\int a}$ (gaussiana per $a=2x$) | — | caratteristiche, trasporto con reazione variabile | C2.3 |
| $x^2D^2 + axD + b$ (Euler) | $x^r$, $x^r\log x$, $x^\alpha\cos(\beta\log x)$ | — | parte radiale del Laplaciano ($r^n$), autosimilarità | C2.4 |
| ODE Fuchsiane (singolarità regolari) | serie di Frobenius $x^r\sum c_kx^k$, log se $r_1-r_2\in\mathbb Z$ | — | ogni separazione con punti singolari | C2.4 |
| Bessel $x^2D^2+xD+(x^2-\nu^2)$ | $J_\nu, Y_\nu$; su $[0,1]$: $\{J_\nu(j_{\nu,k}x)\}$, peso $x$ | ${}_0F_1$ | Laplace/Helmholtz/calore/onde in polari e cilindriche; membrane | C2.5 |
| Bessel mod. $x^2D^2+xD-(x^2+\nu^2)$ | $I_\nu, K_\nu$ | — | Helmholtz modificata, Klein–Gordon statico | C2.5 |
| Airy $D^2-x$ | $\mathrm{Ai}, \mathrm{Bi}$; frame continuo $\{\mathrm{Ai}(x-a)\}_a$ | $\sqrt x\,K_{1/3}(\tfrac23x^{3/2})$ | $u_t+u_{xxx}=0$ (profilo autosimile); Schrödinger con potenziale lineare; Tricomi | C2.5 |
| Legendre (ass.) $(1-x^2)D^2-2xD+n(n+1)-\frac{m^2}{1-x^2}$ | $P_n^m, Q_n^m$; peso 1 su $[-1,1]$ | ${}_2F_1$ / Gegenbauer($m+\frac12$) | Laplaciano sferico ($Y_n^m$) | C2.5 |
| Hermite $D^2-2xD+2n$ / $-D^2+x^2$ | $H_n$ / $\psi_n=e^{-x^2/2}H_n$, autov. $2n+1$ | ${}_1F_1(-\frac n2;\frac12;x^2)$ | calore (Mehler), oscillatore quantistico, Fokker–Planck OU | C2.5 |
| Laguerre $xD^2+(\alpha+1-x)D+n$ | $L_n^\alpha$, peso $x^\alpha e^{-x}$ | ${}_1F_1(-n;\alpha+1;x)$ | parte radiale di H e dell'oscillatore 2D/3D | C2.5 |
| Chebyshev, Gegenbauer, Jacobi | $T_n, U_n, C_n^\lambda, P_n^{(\alpha,\beta)}$ | ${}_2F_1$ ($x=1-2z$) | ipersferiche $SO(d)$, Wigner $d^j$; Chebyshev = Fourier in $\theta$ | C2.5 |
| Sferoidali $(1-x^2)D^2-2xD+\lambda-c^2x^2-\frac{m^2}{1-x^2}$ | $S_{mn}(c,x)$; ricorrenza a 3 termini (Heun confluente) | — | Helmholtz in coord. sferoidali; prolate di Slepian | C2.5 |

**Regola utile per C2.13/C2.56.** Dopo un cambio di variabile e una gauge, tutte le ODE separate classiche (eccetto sferoidali, Mathieu e Heun) sono ${}_2F_1$, ${}_1F_1$ o ${}_0F_1$. Le identità di operatore sono verificate in `sympy/c2_5_special.py`, sezione B.

## [2026-10-22] DA CIT-AUDIT → PR-C2b · AVVISO
Nota informativa (non è un errore): in PR-C2b-P6 la costante n! vale per w_m=(−∂_x)^m G, cioè con la vostra normalizzazione. Con le w_n di Rosenbloom–Widder (Trans. AMS 92 (1959) 220–266, verificato) la costante è 2^n n!, come in R1 e R3 (w_n^{RW} = 2^n(−∂_x)^n G per D=1). Va dichiarato nella Fase 3. Tutte le altre voci di sources.bib sono verificate o riconosciute.
