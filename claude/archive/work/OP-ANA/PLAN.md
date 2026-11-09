# PLAN — OP-ANA (chiusura Fasi 4–5: problemi aperti di natura analitica) · 26/10/2026

Letti (session-protocol, passo 0): RIPRESA.md (fino all'ultimo AGGIORNAMENTO), REPORT_FINALE.md §6, skills-local/session-protocol e claim-lifecycle, NOTAZIONE.md (v1–v4), PROBLEM.md, claims/LEDGER.md (righe S4T, P3-T3, P3-Q-bordo, P1-Q5, P1-Q6), work/S4-TERM/PROOF_PACKAGE.md (§§2–6, 11, 13), work/P3/PROOF_PACKAGE.md (P3-P1, P3-T2, P3-T3), work/P1/PROOF_PACKAGE.md (P1-D3, P1-T2, P1-P1(e), P1-P6, §12).

## Skill caricate (lette per intero o nelle parti di workflow; nessuno script `_vendor` eseguito)
1. `skills-local/session-protocol` (per primo) e `skills-local/claim-lifecycle` — stati, righe LEDGER, consegne.
2. `_vendor/Auto-claude-code-research-in-sleep/skills/proof-writer/SKILL.md` — triage (PROVABLE AS STATED / AFTER WEAKENING / NOT JUSTIFIED), mappa delle dipendenze, nessun passo nascosto, rapporto di blocco se serve.
3. `_vendor/math-skill/SKILL.md`, modo `proof` — esplorazione separata dalla prova, controesempi presto, verifica indipendente.
4. `_vendor/scientific-agent-skills/skills/sympy/SKILL.md` — solo controllo (SymPy/mpmath in `work/OP-ANA/sympy/`, `D:\ProblemaBase\.venv\Scripts\python.exe -I`).
5. `_vendor/Auto-claude-code-research-in-sleep/skills/research-lit/SKILL.md` — solo sorgente `web` (WebSearch) per stabilire se i risultati sono noti (Tang–Teng, Goodman–Xin, Wang; riduzione d'ordine degli splitting con bordo; lemma di Turán–Nazarov).

## Problemi, predizioni, criteri d'uscita
### Q1 = S4T-Q1 (priorità 1): ordine in $L^1$ di $E^{add}$ per Burgers oltre lo shock, $\nu\to0$
- Riduzione già disponibile: S4T-T3(vi) $\big|\|E^{add}\|_{L^1}-\|S(t)u_0-S_B(t)u_0\|_{L^1}\big|\le2\pi\nu t\|u_0''\|_\infty$.
- **Strategia (prova propria, niente fonti esterne):** Cole–Hopf/Hopf [F2] dà $u-v=(a(x)-\langle y\rangle_{\mu_{t,x}})/t$ con $\mu\propto e^{-\Phi_{t,x}/2\nu}$; metodo di Laplace con resti espliciti (identità di integrazione per parti $\int\psi'e^{-\psi/\varepsilon}=$ bordo) lontano dagli shock; analisi a due pozzi (logistica) nello strato $|x-x_s|\lesssim\nu$.
- **Predizione:** classe (H$_t$) = a tempo $t$ fissato ogni minimizzante di Lax–Oleinik è non degenere ($J=1+tu_0'>0$) e gli shock sono un insieme finito con esattamente due minimizzanti. Allora $\|E^{add}(t)\|_{L^1}=\Lambda(t)\,\nu+o(\nu)$ con costante esplicita $\Lambda=\int_{\mathbb T}t|u_0''(a)/J^2-u_0''(x)|dx+4\sum_s\log(2\cosh(\rho_s/2))$, $\rho_s=\tfrac12\log(J_s^-/J_s^+)$: **Θ(ν), non ν|log ν|**; il $|\log\nu|$ compare solo a tempi degeneri (formazione di uno shock: scala di Pearcey).
- **Criterio d'uscita:** prova completa del teorema in (H$_t$) + verifica che $u_0=\varepsilon\sin x$ soddisfa (H$_t$) per ogni $t>t^*$ + controllo numerico (mpmath, quadratura di Cole–Hopf) della costante; oppure controesempio; altrimenti PARZIALE con ostruzione.

### Q2 = P3-Q-bordo (priorità 2): tasso di $E^{mult,(1)}$ per AD Dirichlet su $(0,L)$, $u_0$ generale
- **Strategia:** identità esatta del commutatore $\partial S^D(s)f=S^N(s)f'$ ($f\in H^1_0$) ⇒ $E^{mult,(1)}(t)u_0=-c\int_0^tS^D(t-s)(S^N(s)-S^D(s))u_0'\,ds$; nucleo $K^N-K^D=2\sum_jG_s(x+y-2jL)>0$ (Poisson); localizzazione ai bordi, modello sul semiasse, autosimilarità parabolica.
- **Predizione:** se $u_0'(x)=\gamma_0x^\alpha+O(x^{\alpha+\beta})$ vicino a 0 (e analogo in $L$), $\|E^{mult,(1)}(t)u_0\|=|c|N_\alpha D^{\alpha/2+1/4}(\gamma_0^2+\gamma_L^2)^{1/2}t^{5/4+\alpha/2}(1+o(1))$; per $u_0$ liscio con prima derivata non nulla al bordo di ordine $k$: $t^{k/2+3/4}$ ($k=1$: 5/4 ✔ P3-T3; $k=2$: 7/4 ✔ V-ex $x^2(L-x)^2$); dato piatto ai bordi: $O(t^\infty)$. Bound uniforme $\le C|c|\|u_0'\|_\infty t^{5/4}$ per ogni $u_0\in H^1_0\cap W^{1,\infty}$.
- **Criterio d'uscita:** prova completa; controllo: $N_0=\sqrt{J/\pi}$ (costante dell'audit S-CHECK-5) e $N_1\sqrt8\approx0.44$–$0.45$ (V-ex) via mpmath.

### Q3 = P1-Q6 (priorità 3): no-go di continuità in $H^m(\Omega)$ di $E^{add}$
- **Strategia:** dati esponenziali $u_\zeta=e^{a(\zeta)t+\zeta x}$; rapporto ridotto a una somma esponenziale in $s=t-t_0$ con esponenti $\{0,a,a_n\}$; scelta di direzioni $\zeta=re^{i\theta}$ (argomento di Fourier sugli archi) o della curva $a(\zeta)\in i\mathbb R$.
- **Predizione:** (a) termini monomi $\lambda_n\xi^{l_n}$ con gradi distinti $\ge1$, $N\ge2$: illimitato per ogni $m$ e ogni $t_0\in\bar I$ (generalizza P1-P1(e)); (b) **eccezione**: termini affinemente proporzionali a coefficienti reali $a_n=\theta_na+\kappa_n$: continuo da $H^1$ ⟺ i tempi riscalati $t_0+\theta_n(t-t_0)$ restano in $\bar I$; (c) gruppi generali non proporzionali: illimitato (con il lemma di Turán–Nazarov, CON-FONTE, per i casi con più esponenti allo stesso livello).
- **Criterio d'uscita:** prove di (a),(b); (c) prova condizionale o PARZIALE con ostruzione precisa.

### Q4 = P1-Q5 a ε = 1 (se c'è tempo)
- **Strategia:** $E^{mult}(t)=E^{mult,(1)}(t)u_0+\sum_{j\ge2}S^{(j)}(t)u_0-S_0(t)R_V(t)u_0$ con stime $O(t^{3/2})$ dei resti (Dyson–Phillips, $\|\partial S^D(r)\|\le(2eDr)^{-1/2}$, inflow).
- **Predizione:** se $(u_0'(0),u_0'(L))\ne0$: $\|E^{mult}(t)u_0\|=\Theta(t^{5/4})$ con la stessa costante del 1° ordine; altrimenti solo $O(t^{3/2})$ (PARZIALE).

## Consegne
`work/OP-ANA/PROOF_PACKAGE.md` (incrementale, salvato dopo ogni risultato), `CHECK_REQUEST.md` (autosufficiente per S-CHECK), `sympy/` (op_q1_burgers.py, op_q2_bordo.py, op_q3_nogo.py), TABELLA LEDGER e DONE in `inbox/central.md`. Stati: solo PROVA SCRITTA / CONDIZIONALE / V-ex / APERTO (nessun DIMOSTRATO prima di S-CHECK). Contatti: S-CHECK (via central), coordinatore.
