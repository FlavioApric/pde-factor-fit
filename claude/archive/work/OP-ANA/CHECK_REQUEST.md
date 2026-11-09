# CHECK_REQUEST — OP-ANA (per S-CHECK) · 26/10/2026
Fonte unica: `work/OP-ANA/PROOF_PACKAGE.md`, che contiene enunciati, ipotesi e prove complete. Controlli numerici e SymPy in `work/OP-ANA/sympy/*.py → *.out`; sono solo controlli, non prove. Nessun claim è stato dichiarato DIMOSTRATO. Si chiede audit (proof-checker, revisore indipendente) in quest'ordine di priorità, con kill-argument per OPA-T1, che sta sul cammino critico di G★′-NL punto 1.

## Contesto minimo (per un revisore senza contesto)
- Burgers su 𝕋 = ℝ/2πℤ: $u_t+uu_x=\nu u_{xx}$. $S(t)$ = flusso viscoso, $S_B(t)$ = semigruppo entropico di $u_t+(u^2/2)_x=0$, $S_A(t)=e^{t\nu\partial^2}$. $E^{add}(t):=S(t)u_0-S_A(t)u_0-S_B(t)u_0+u_0$. Fatti importati (CON-FONTE, da verificare a parte): [F1] Lax–Oleinik, $S_B(t)u_0(x)=(x-a)/t$ con $a\in\arg\min\Phi_x$, $\Phi_x(y)=U_0(y)+(x-y)^2/2t$; [F2] Hopf–Cole, $S(t)u_0(x)=(x-\langle y\rangle_x)/t$ con $\langle\cdot\rangle_x$ media rispetto a $e^{-\Phi_x/2\nu}dy$. Già noto in S4-TERM: $|\|E^{add}\|_{L^1}-\|S(t)u_0-S_B(t)u_0\|_{L^1}|\le2\pi\nu t\|u_0''\|_\infty$.
- AD su $(0,L)$ con Dirichlet: $A_0=D\partial^2$, $V=-c\partial$; $E^{mult,(1)}(t)u_0:=\int_0^tS_0(t-s)VS_0(s)u_0ds-tS_0(t)Vu_0$ (coefficiente al 1° ordine nell'accoppiamento dell'errore di splitting).
- $E^{add}$ lineare (P1-D3(b)): $\Omega=(0,T)\times J$; per $u$ nella classe 𝔅 (restrizioni di funzioni intere di tipo esponenziale) con $u_t=a(\partial_x)u$, $a=\sum a_n$: $E^{add}(t)=u(t)-u_0-\sum_n(e^{(t-t_0)a_n(\partial)}u_0-u_0)$, $u_0=u(t_0)$.

## Claim da auditare
1. **OPA-T1** (§2) — sotto (H_t): $\|S(t)u_0-S_B(t)u_0\|_{L^1}=\nu\Lambda_{uv}+o(\nu)$ e $\|E^{add}\|_{L^1}=\nu\Lambda_{add}+o(\nu)$, con le costanti esplicite di §2. Punti da guardare: Lemma 1(iii) (margine uniforme per compattezza, uso di (H_t)); Lemma 2 (resti di Laplace con integrazione per parti; dipendenza delle costanti); Passo B (riduzione a due pozzi, logistica, separazione $|A+B|$, convergenza dominata nel profilo, valore $4\log(2\cosh(\rho/2))$); che l'esponente dello strato sia esattamente $\rho=\tfrac12\log(J^-/J^+)$.
2. **OPA-C1** (§2) — (H_t) per $\varepsilon\sin x$ e la forma chiusa di $\Lambda_{uv}$.
3. **OPA-L2, OPA-T2** (§3) — identità $\partial S^D(s)f=S^N(s)f'$; formula di $E^{mult,(1)}$; nucleo per Poisson; stime di localizzazione (Passi 1–6); autosimilarità e $N_\alpha>0$; forma chiusa $N_0=\sqrt{J/\pi}$; corollario (iii) con l'ordine $k$.
4. **OPA-L3, L4, L5, OPA-T3(a–d), OPA-P3** (§4) — lemma di Fourier sugli archi; criterio lungo i raggi; caratterizzazione (F); eccezione proporzionale con (TC) (entrambe le direzioni).
5. **OPA-P4** (§5) — stime dei termini di Dyson $j\ge2$ ($\|VS_0(r)\|\le|c|(2eDr)^{-1/2}$, induzione con la Beta) e resto dell'inflow.
6. **OPA-T3(e)** — solo verifica che la riduzione al lemma [Naz] sia corretta; [Naz] = Nazarov 1994 (CON-FONTE, da affidare a CIT-AUDIT).

## Controlli già eseguiti (non sostituiscono l'audit)
- `op_q1_burgers.out`: $u_0=\sin x$, $t=2$: $\|u-v\|_1/\nu\to3.9828$ (misurato 3.9842 a $\nu=5\cdot10^{-4}$), $\|E^{add}\|_1/\nu\to9.9041$ (9.9000). Dato asimmetrico ($\rho=-0.3035$): 4.6666 contro 4.6647.
- `op_q2_bordo.out` 15/15 OK: $N_0$; $e_1$ entro $10^{-4}$ relativo; $x^2(1-x)^2$: limite estrapolato 0.45996 contro il predetto 0.459965.
- `op_q3_nogo.out` 18/18 OK: crescita o limitatezza del rapporto come previsto in ogni caso (AD per ogni t₀; tre monomi; proporzionali con e senza (TC); classe (F)).

## Citazioni da verificare (CIT-AUDIT)
Tang–Teng, Math. Comp. 66 (1997) 495–526 (portata del tasso $\varepsilon|\log\varepsilon|$ / $O(\varepsilon)$; abstract confermato via web); rassegna di Tang sui tassi O(ε) (Bakhvalov, Harabetian, Fan); Hundsdorfer–Verwer 2003 cap. IV ed Einkemmer–Ostermann 2015 (riduzione d'ordine $\tau^{5/4}$ con Dirichlet); Nazarov, St. Petersburg Math. J. 5 (1994) 663–717 (lemma di Turán–Nazarov, esponente $n-1$).
