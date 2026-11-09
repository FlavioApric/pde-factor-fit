# CHECK_REQUEST — OP-F5A (audit indipendente: proof-checker; kill-argument su T1, T2, C1)
Revisore: subagente Claude senza il contesto di OP-F5A. Leggere solo `work/OP-F5A/PROOF_PACKAGE.md` (autosufficiente: §2–§4 contengono enunciati, ipotesi e prove; §0 i fatti importati) e, per i riferimenti interni, `work/OP-ANA/PROOF_PACKAGE.md` §2.1–2.2 (OPA-T1, Lemmi 1–3) e §3 (OPA-T2). Script di controllo in `work/OP-F5A/sympy/` (evidenza, non prova): python `D:\ProblemaBase\.venv\Scripts\python.exe -I`, con timeout, file temporanei con prefisso `opf5a_`; non uccidere processi altrui.

## Quadro minimo
- Burgers viscoso su 𝕋 = ℝ/2πℤ, $u_t+uu_x=\nu u_{xx}$, $u(0)=u_0$; $S_B$ semigruppo entropico. Hopf: $u=(x-\langle y\rangle_x)/t$, $\langle\cdot\rangle_x$ media per $e^{-\Phi_x(y)/2\nu}dy$, $\Phi_x(y)=U_0(y)+(x-y)^2/2t$ ([F2], dimostrato). Lax–Oleinik: $v=S_B(t)u_0=(x-a(x))/t$, $a(x)\in\arg\min\Phi_x$ ([F1], importato; T1 non lo usa). $J_t=1+tu_0'$, $X_t(y)=y+tu_0(y)$, $t^*=-1/\min u_0'$.
- AD su (0,L): $A=D\partial^2-c\partial$ Dirichlet; $E^{mult}(t)u_0=e^{tA}u_0-S^D(t)S_2(t)u_0$, $S_2$ trasporto con inflow in 0.

## Da verificare (in ordine di priorità)
1. **OPF5A-T1** (§4): Passo 1 (identità esatte $\langle\psi'\rangle=0$, $\langle z\psi'\rangle=2\nu$, eliminazione di $\langle z^2\rangle$, segno e fattore di $-\nu q/p^2$); Passo 2 ($\int_{A\ge m}A^{-3}d\alpha\le C/m^2$; valore $2\log\frac1{\max(\sqrt\nu,\eta)}+O(1)$ dell'integrale $\int|\partial J|/J$); Passo 3; Passo 5 (scala di Pearcey: $\psi/2\nu\to\frac{\kappa_3}4Q$, cambio $\lambda=(4/\kappa_3)^{1/4}$, $m(\beta)=-\beta^{-3}+O(\beta^{-5})$, argomento $K\to\infty$). L2(b): $f(\beta)=\frac1{12}+\frac\beta3+\frac{\beta^2}2\ge\frac1{50}(1+\beta^2)$. Controllo numerico: Γ(sin) = 2.57497 (opf5a_check3 (Q)) vs Cole–Hopf 2.5821 → 2.5757 (opf5a_q1_burgers.out (A)).
2. **OPF5A-T2(b), Lemma U** (§4): forma normale $\Psi_0=\xi A+\frac{\kappa_3}{24}A^4-\frac{A^2}{2t^{*2}}$ (coefficienti e scale $x-X_t(a^*)=-t\tau^{3/2}\xi$); uniformità di OPF5A-L3 sulla famiglia $\{\Psi_\tau\}$; raccordo $|A|\approx K'$. **Kill-argument**: c'è un regime di $\tau$ (es. $\tau\asymp\sqrt\nu$, o $\tau\gg\sqrt\nu$ con $\hat\nu=\nu/\tau^2$) in cui $\|u-v\|_{L^1}-2\nu\log\frac1{\max(\tau,\sqrt\nu)}$ non è $O(\nu)$?
3. **OPF5A-L3 e T3** (§3): bound $e^{-g_j/2\nu}1_{a_j\ne a(x)}\le\sum_k e^{-f_{jk}/2\nu}1_{f_{jk}>0}$; profilo a $n$ pozzi e costante $2\nu\log\frac{(\sum p_j)^2}{p_1p_n}$ (per $n=2$ deve ridare $4\nu\log(2\cosh\frac\rho2)$). Numerica: opf5a_check2b.out (6.06117, 6.06113 vs 6.06125); lo scarto di opf5a_triple.out (6.047) è dichiarato artefatto di griglia: verificarlo.
4. **OPF5A-T4** (§3): (i) Sard 1D, chiusura di $T_1$; (iii) scatole di rami, unicità della curva d'urto in una scatola, $\frac d{dt}(s_{ij}-s_{jl})=(a_l-a_i)/2t>0$; (iv) non accumulo in $t_b$ sotto (SB). Il triage dice che "discreto" è falso per $u_0\in C^2$ generale: verificare l'enunciato corretto.
5. **OPF5A-L5, T5** (§2): calcolo termine a termine dei nuclei (in particolare il termine riflesso $j=1$ e l'origine di $R_L$); $\|K_+(\cdot,r)\|_{L^2}\le2r\|G'\|_{L^2}$; Passo 2 di T5 ($|\varrho|\le C(x^2+y+t)$, scala $t^{k/2+5/4}$). Numerica: opf5a_check3 (P), opf5a_q3_bordo 19/19.
6. **OPF5A-C1**: la localizzazione è dichiarata schizzo — dire se è accettabile come PROVA SCRITTA o va lasciata CONDIZIONALE.

## Fonti (sources.bib)
Tang–Teng 1997 (abstract verificato, testo no): usata solo per l'ordine $O(\nu|\log\nu|)$ del limite superiore uniforme. Hirsch cap. 6 (densità Morse; numero non verificato). Milnor 1965 (Sard).

## Esito richiesto
Tabella per claim: PASS / PASS-con-fix / FAIL, con fix numerati; stato raccomandato per il LEDGER; per T1/T2/C1 esito kill-argument. File: `work/CHECK/AUDIT_OP-F5A.md`.
