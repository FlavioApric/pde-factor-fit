# MIT 18.03 Differential Equations, Spring 2010 (Miller, Mattuck): mappa sul catalogo C2 e su G★
Fonte: https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/lecture-notes/ (indice consultato il 2026-10-22: 39 lezioni + esami).

| Lezioni | Contenuto | Item | Cosa serve a G★ (con verifica) |
|---|---|---|---|
| L1–L2 | campi di direzioni, esistenza e unicità; numerica ○ | C2.3 | solo come riferimento |
| L3–L4 | lineari del 1° ordine, fattore integrante | C2.3 ★ | $T = D+a$, nucleo $e^{-\int a}$, identificazione $a=-(\log u)'$ (c2_3) |
| L5–L6 | complessi, esponenziali complessi | C2.1 | radici complesse ↔ $e^{ax}\cos bx$ (c2_1) |
| L7 | risposta a ingressi esponenziali e sinusoidali; guadagno e fase | C2.2 | $y=\mathrm{Re}[e^{i\omega x}/p(i\omega)]$ (c2_2) |
| L8–L9 | autonome, linea di fase, stabilità; lineare vs nonlineare | C2.3 ▲ | logistica, $\mathrm{sgn}F'$ (c2_3) |
| L11–L12 | modi, polinomio caratteristico, smorzamento | C2.1 ★ | nucleo esponenziale-polinomiale (c2_1) |
| **L13–L14** | **exponential response formula**, guadagno complesso | C2.1–C2.2 ★ | **$p(D)e^{rt}=p(r)e^{rt}$ = azione del simbolo** (F1, §1.2-3); shift rule (c2_1) |
| **L15** | **operatori**, coefficienti indeterminati, **risonanza** | C2.1–C2.2 ★ | algebra $\mathbb C[D]$; $x^ke^{rx}/p^{(k)}(r)$ (c2_1) |
| L16–L18 | risposta in frequenza, LTI, sovrapposizione, RLC | C2.2 | linearità ⇒ split additivo forzante/nucleo |
| L20–L22 | serie di Fourier, soluzioni periodiche, risonanza | C2.14 (→PR-C2d) | $p(D)$ su $e^{int}$: moltiplicatore $p(in)$ |
| L23–L24 | gradino e delta, risposta al gradino e all'impulso | C2.2, C2.36 | Green causale $g$ (c2_2) |
| **L25** | **convoluzione** | C2.2, C2.36 ★ | $y=g*f$ (Duhamel, c2_2); composizione moltiplicativa di §1.2-2b |
| L26–L28 | Laplace, applicazione alle ODE | C2.14 | $\mathcal L[u]=q/p$ razionale (c2_1, c2_2) |
| **L29–L30** | **pole diagram**, **funzione di trasferimento** | C2.2 ★ | transfer = $1/p(s)$ = simbolo inverso; poli = $V(p)$ (c2_2) |
| L32–L35 | sistemi lineari, autovalori complessi o ripetuti, piano delle fasi | C2.2 ■ | Jordan ↔ $x^ke^{\lambda x}$ (c2_2) |
| **L36** | **modi normali ed esponenziale di matrice** | C2.2 ■, II-b | $e^{xC(p)}$, $g=[e^{xC}]_{0,m-1}$ (c2_2) |
| L37–L39 | sistemi nonlineari, linearizzazione, cicli limite, caos | Fase 4 ▲ | fuori dal blocco lineare (segnalato a PR-C2c) |

**Lettura chiave per II e P1.** L'ERF, la funzione di trasferimento e la convoluzione sono le tre facce del calcolo simbolico:
- moltiplicazione per $p$ sugli esponenziali;
- inversione di $p$ nel dominio di Laplace;
- convoluzione nel dominio $x$.

È esattamente il dizionario "termine → simbolo → nucleo" di cui G★ ha bisogno nel caso ODE.
