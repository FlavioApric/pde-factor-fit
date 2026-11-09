# PR-C2b — REPORT (Fase 1) · Asse 1, T2–T9: famiglie di PDE lineari

Agente PR-C2b · 2026-10-22 · Notazione `NOTAZIONE.md` v1 · Protocollo `PROTOCOLLO.md` (Regole 1–4).
*(Salvato dal coordinatore dalla risposta finale di PR-C2b: la scrittura diretta era bloccata dall'ambiente.)*

## 0. Sintesi
- **23 schede** in `cards/`: 15 COMPLETE (★/◆, card schema 1–9): C2.6, C2.7, C2.8, C2.9, C2.10, C2.11, C2.12, C2.19, C2.20, C2.21, C2.22, C2.30, C2.35, C2.37, C2.38; 8 BREVI (▲■●◇): C2.18 (+ sotto-scheda ★ Lagrange), C2.25, C2.31 (+ sotto-scheda ★ Klein–Gordon), C2.34, C2.39, C2.42, C2.46, C2.23. Tutti gli item di T2–T9 coperti.
- **SymPy**: 6 script in `sympy/`, **168/168 PASS** (`out_t2.txt` 18, `out_t3.txt` 42, `out_t4_t5.txt` 34, `out_t6_t7.txt` 31, `out_t8.txt` 26, `out_t9.txt` 17), eseguiti con `D:\ProblemaBase\.venv\Scripts\python.exe -I`; numerica solo come controllo (Jacobi–Anger, $e^{A+B}\ne e^Ae^B$).
- **Risultati** (§2): blocchi di Gram inter-classe [P1]; intersezioni $\dim\mathbb C[\tau,\xi]/(P_i,P_j)$ [P2]; E_int nei tre regimi [P3]; **G3 fallisce** per il 2° ordine in $t$ [P4] e per Caputo [P5], con sostituti espliciti; duale esplicito del calore [P6]; RKHS di Bergman come prototipo di C1.0 [P7]; identificabilità = generatore di Ann(u), non L [P8].

## 1. Skill caricate (Regola 2)
- `anthropic-skills:deep-research` NON invocata via Skill (coordina subagenti); letto `_vendor/academic-research-skills/deep-research/SKILL.md` e seguito il workflow ridotto scoping → fonti → verifica → sintesi ("ogni claim ha citazione / non verificabile = marcato").
- `paper-lookup`, `citation-management`, `sympy`, `math-skill` (solver): SKILL.md letti.
- Lookup via WebSearch/WebFetch: OCW 18.303; Crossref (Wei–Norman, Wilcox, Kwaśnicki, Caffarelli–Silvestre, Casas); arXiv/Cambridge (Ait El Manssour–Härkönen–Sturmfels); AMS (Rosenbloom–Widder); mathnet (Gurevich).
- Nessuno script `_vendor` eseguito.

## 2. Proposizioni

**[PR-C2b-P1] Blocchi di Gram tra classi esponenziali (C1.0, C1.3).**
- Ipotesi: $\Omega=[0,T]\times\mathbb T$; classi $K_P$ di equazioni d'evoluzione scalari a coeff. costanti del 1° ordine in $t$, $u_t=a_P(\partial_x)u$, modi $e_{P,k}=e^{ikx+\tau_P(k)t}$, $\tau_P(k)=a_P(ik)$ (anche simboli non polinomiali: $|k|^{2s}$, $\hat J(k)-1$).
- Enunciato: $\langle e_{P,k},e_{Q,l}\rangle_{L^2(\Omega)}=2\pi\,\delta_{kl}\,\frac{e^{sT}-1}{s}$, $s=\tau_P(k)+\overline{\tau_Q(k)}$ ($2\pi T$ se $s=0$). Il Gram del dizionario unione è **block-diagonale in $k$**; ogni blocco è un Gram di esponenziali su $[0,T]$, definito positivo ⟺ i $\tau_P(k)$ sono distinti.
- Coerenze asintotiche verificate: calore–trasporto $\mu_k\sim\sqrt{2/(DT)}/k$; Schrödinger–Airy $\le 2/(T|k^3-k^2|)$; onda destra–sinistra $|\sin(ckT)|/(ckT)$, nulla per $T=\pi/c$; non locale ($J*u-u$)–calore $\mu_k\sim 2/(k\sqrt{D(1-e^{-2T})})$.
- Prova: ortogonalità di $e^{ikx}$ su $\mathbb T$ + integrale elementare in $t$ (SymPy t9). Stato: DIMOSTRATO.
- Conseguenza congetturale: Riesz uniforme per $|k|>k_0$ via Gershgorin (Q1). Attenzione: i modi con $\tau_P(k)=\tau_Q(k)$ sono i punti di $V(P)\cap V(Q)$ sul reticolo; lì il blocco è singolare.

**[PR-C2b-P2] Intersezioni di classi (C4, G1, G2, PR-C2.4).**
- $\ker P_i\cap\ker P_j=\ker(P_i,P_j)$ ha dimensione $\dim\mathbb C[\tau,\xi]/(P_i,P_j)$ (Ehrenpreis–Palamodov; Hörmander ALPDO II cap. 7); **finita ⟺ $\gcd(P_i,P_j)=1$**.
- Tabella (Groebner, SymPy t8) per trasporto, calore, Airy, Schrödinger, onda, trave, KG, Laplace, reazione (scheda C2.19): valori = Bezout $\deg P_i\deg P_j$ meno intersezioni all'infinito (trasporto–calore 2, Airy–onda 6, onda–trave 8); ∞ solo per trasporto|onda e Schrödinger|trave.
- Stato: DIMOSTRATO-CON-FONTE + verificato sui 36 casi.
- Correzione a G1: aggiungere l'ipotesi "coprimi"; se $P_1\mid L$, $\ker P_1\subset\ker L$ e l'intersezione è infinita (caso G2, non controesempio).

**[PR-C2b-P3] E_int nei tre regimi (A8, A9, P1, P3, G3).**
1. *Fattorizzazione* $P=P_1P_2$ coprimi: $\ker P=\ker P_1+\ker P_2$, E_int = 0 modulo $\ker(P_1,P_2)$. **Proiettore costruttivo**: $P_2u\in\ker P_1$. Esempi verificati: onda (d'Alembert, $(\partial_t+c\partial_x)u=2cg'$); Laplace (olomorfa + antiolomorfa); trave = due Schrödinger coniugati (intersezione $\{1,x\}$); sistemi iperbolici ($\ell_j\cdot U=g_j$). In 2 variabili niente Bezout: l'ambiguità è esattamente $\ker(P_1,P_2)$. DIMOSTRATO-CON-FONTE.
2. *Somma di termini commutanti, 1° ordine in $t$*: $e^{t\sum A_n}=\prod e^{tA_n}$; $E_{int}=\sum_{|S|\ge2}\prod_{n\in S}(S_n-I)u_0$ ($2^N-N-1$ termini; $N=2$: $(S_1-I)(S_2-I)u_0$, bilineare = $h(e_1,e_2)$). Log-simbolo additivo, identificazione lineare $O(N)$ (avvezione–diffusione: determinante $i\kappa_1\kappa_2(\kappa_2-\kappa_1)$). DIMOSTRATO (t8).
3. *Non commutanti*: (a) trasporto + $r(x)$: soluzione esatta $\exp(-\int_0^tr(x-cs)ds)u_0(x-ct)$, $[A,B]=cr'$, Zassenhaus al 2° ordine verificato (t2), E_int in forma chiusa; (b) algebra di Lie finita: OU, $\{\partial_x^2,x\partial_x,x^2\}$ genera $\mathfrak{sl}_2\oplus$centro ⇒ Wei–Norman (1963) ⇒ E_int chiuso (Mehler); Casas (1996) per PDE; (c) algebra infinita ⇒ Dyson/Magnus troncati (P3). (a),(b) DIMOSTRATO-CON-FONTE; classificazione (a)/(b)/(c) = PROPOSTA come criterio di trattabilità di E_int.

**[PR-C2b-P4] G3 fallisce per equazioni del 2° ordine in $t$ (onda, KG, telegrafo, trave).**
- (i) Generatore quadratico: $\tau^2=a_1(\xi)+a_2(\xi)$ ⇒ $\tau=\pm\sqrt{a_1+a_2}$ non additive (KG: $\sqrt{\kappa^2+m^2}\ne\kappa+m$).
- (ii) Nella riduzione compagna (via b) termini scalari commutanti diventano blocchi non commutanti; telegrafo: $[A_w,A_d]=\begin{psmallmatrix}0&-2a\\-2ac^2k^2&0\end{psmallmatrix}\ne0$, $e^{A_w+A_d}\ne e^{A_w}e^{A_d}$.
- Sostituto: per ogni modo $k$ il problema è $m\times m$; l'algebra generata sta in $\mathfrak{gl}_m$ ⇒ Wei–Norman chiude modo per modo; oppure $u=e^{-at}w$ (telegrafo → KG).
- Stato: DIMOSTRATO (SymPy t8). Correzione a G3 e a PR-C2e §0.2 (CONFLITTO inviato, accolto dal coordinatore).

**[PR-C2b-P5] G3 fallisce per Caputo; la subordinazione la ripristina.**
- $0<\alpha<1$: $E_\alpha(-(a+b)t^\alpha)\ne E_\alpha(-at^\alpha)E_\alpha(-bt^\alpha)$ (coeff. di $xy$: $2/\Gamma(2\alpha+1)$ vs $1/\Gamma(\alpha+1)^2$, uguali ⟺ $\alpha=1$).
- $E_\alpha(-\lambda t^\alpha)=\int_0^\infty M_\alpha(\sigma)e^{-\lambda\sigma t^\alpha}d\sigma$; dentro l'integrale lo split è esatto: $u(t)=\int M_\alpha(\sigma)S_1(\sigma t^\alpha)S_2(\sigma t^\alpha)u_0\,d\sigma$; E_int è un effetto di mistura in forma chiusa.
- Stato: non-semigruppo DIMOSTRATO (t9); subordinazione DIMOSTRATO-CON-FONTE (Mainardi 2010; Gorenflo et al. 2014), verificata per $\alpha=1/2$ ($E_{1/2}(-z)=e^{z^2}\mathrm{erfc}\,z$). Per la spazio-frazionaria G3 vale.

**[PR-C2b-P6] Duale esplicito per la classe del calore (C1.4, P3).**
- $v_n=\partial_\xi^ne^{D\xi^2t+\xi x}|_0$ (polinomi del calore), $w_m=(-\partial_x)^mG=(4Dt)^{-m/2}H_m(x/\sqrt{4Dt})G$.
- $\int_{\mathbb R}v_n(x,-t)w_m(x,t)dx=n!\delta_{nm}$. Prova: per parti ($\partial_xv_n=nv_{n-1}$) e $\int v_k(x,-t)G(x,t)dx=\delta_{k0}$. Fonte: Rosenbloom–Widder (1959). DIMOSTRATO-CON-FONTE, verificato per $n,m\le4$ (t3).
- La gaussiana di B5 è $w_0$; le funzioni di Hermite sono le sue derivate. Analoghi per Airy e Schrödinger (polinomi $p_n$, $q_n$ verificati come soluzioni) aperti: Q2.

**[PR-C2b-P7] Prototipo di C1.0.**
- $\ker\partial_{\bar z}\cap L^2(\mathbb D)$ è un RKHS con $K(z,w)=\frac1{\pi(1-z\bar w)^2}=\sum_ne_n(z)\overline{e_n(w)}$ (Bergman); la classe armonica è somma di olomorfa e antiolomorfa, ortogonali salvo le costanti: è la costruzione $\mathcal H_{\mathcal D}$, $K=\sum e_{n,i}\otimes e_{n,i}$ del piano. DIMOSTRATO-CON-FONTE (Hedenmalm–Korenblum–Zhu 2000), verificato (t4).
- Continuo↔numerabile: Helmholtz, onde piane (Herglotz, frame su $S^1$) ↔ $J_n(kr)e^{in\theta}$ via Jacobi–Anger: risposta concreta ad A7.

**[PR-C2b-P8] G★(i) recupera il generatore di Ann(u), non necessariamente L (C3, G4).**
- $L=P_1P_2$, $u\in\ker P_1$ (onda con solo $f(x-ct)$; trave con un solo fattore) ⇒ $P_1\in\mathrm{Ann}(u)$; nessun procedimento basato su $u$ distingue $L$ da $P_1Q$.
- Mono-modo $e^{ikx+\tau t}$: Ann contiene $\partial_x-ik$ e $\partial_t-\tau$ ⇒ $L$ determinato solo dal vincolo $P(\tau,ik)=0$.
- Simboli non polinomiali (C2.37/38): identificabili solo sul supporto di $\hat u_0$; servono ipotesi di classe finita.
- DIMOSTRATO (elementare); conferma e precisa G4 (Q8).

## 3. Mappa sugli item del piano
| item | contributo | dove |
|---|---|---|
| C2 | 23 schede T2–T9, base numerabile/continua per famiglia, SymPy PASS | `cards/` |
| PR-C2.2/2.3 | 15 complete + 8 brevi | `cards/` |
| PR-C2.4 | intersezioni [P2]; nuclei condivisi: gaussiana (C2.7, C2.12, C2.21 Mehler), Airy (C2.10, C2.23 Tricomi, C2.46), Bessel (C2.31 KG, C2.12 $I_0$, C2.35, C2.23 Keldysh, membrane C2.8), Hermite (C2.7 $w_n$, C2.21 OU), Poisson/Cauchy (C2.9, C2.20 DtN, C2.38 $s=\frac12$) | C2.19 |
| PR-C2.5 | termini×famiglie + righe nuove ($t\partial_t+x\partial_x$, $a\partial_t$ con $\partial_t^2$, $y\partial_x^2$, $y\partial_y^2$, RL≠Caputo, memoria→Cattaneo) | inbox/PR-C2e.md |
| C1.0–C1.4 | [P1], [P6], [P7], Jacobi–Anger | C2.7, C2.9, C2.35 |
| C4 / A8 | [P2], [P3] | C2.8, C2.12, C2.19 |
| P1 | $E_{int}=(S_1-I)(S_2-I)u_0$ | C2.12 |
| P3 | regimi (a)(b)(c) | C2.6, C2.21, C2.12 |
| II (via b) | [P4]: la compagna crea non-commutatività; Jordan ↔ termini secolari | C2.12, C2.22 |
| G3 | confermata (1° ordine, coeff. costanti, anche simboli non polinomiali); falsa per 2° ordine in $t$ e Caputo | P4, P5 |
| G1/G2 | confermate con coprimalità esplicita | P2 |
| G4 | precisata | P8 |
| G6 | numerabile su $\mathbb T$/intervallo, continua su $\mathbb R$; limite: Gurevich per non locali in 2D | C2.37, Q5 |
| D1 | Fourier/log-simbolo, coordinate caratteristiche, $u=e^{-at}w$, Cole–Hopf, Appell, subordinazione | C2.6, C2.12, C2.25, C2.38 |

## 4. Integrazione PR-C2a
Nessun messaggio di PR-C2a in inbox; letti `research/PR-C2a/components_T1.md` e le schede C2.1–C2.3. Corrispondenze: Airy ($D^2-x$) → Tricomi e nucleo di $\partial_t+\partial_x^3$; Bessel → Riemann di KG ($J_0$), telegrafo ($I_0$), Helmholtz ($J_n$), Keldysh ($\sqrt yI_1$); Hermite ($-2xD$) → $w_n$ del calore e OU; Euler ($xD$) → Black–Scholes $x^\xi e^{\xi^2t}$ e Lagrange $g(x/t)$; $(D-\lambda)^m$ → polinomi del calore/Airy come $\partial_\xi^n$ degli esponenziali. Concordanza: 1° ordine a coefficiente variabile ⇒ moltiplicativo, esteso a trasporto + $r(x)$ con Dyson esatto.

## 5. Comunicazioni
- inbox/PR-C2e.md: RISPOSTA+TABELLA e CONFLITTO su §0.2 (P4, P5).
- inbox/R3.md: TABELLA schede ★ + 5 punti per il catalogo.
- inbox/central.md: PLAN-READY, avviso REPORT bloccato, DONE.

## 6. Stato e limiti
- Noto/dimostrato: P1, P2, P3 (1, 2, 3a, 3b), P4, P5, P6, P7, P8. Proposta: classificazione (a)/(b)/(c). Aperto: Q1–Q8 (Q9 chiuso).
- Fonti DA VERIFICARE in `sources.bib`: pagine di Schwartz 1947, anno della 4a ed. di Myint-U–Debnath, numero d'articolo di Jin–Rundell; Guenther–Lee, Polyanin, Myint-U–Debnath citati a livello di capitolo.
