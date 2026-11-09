# CHECK_REQUEST — S-P1 → S-CHECK · 25/10/2026
Richiesta di audit secondo `proof-checker`. Il revisore deve ricevere **solo** questo file: contiene enunciati, ipotesi e prove; non serve il resto del contesto. Le prove sono copiate da work/P1/PROOF_PACKAGE.md (stessi ID). SymPy di controllo: `work/P1/sympy/p1_checks.py` → `.out` (29/29 PASS) e `p1_checks2.py` → `.out` (3/3 PASS).

## Ordine di priorità (cammino critico: E_int)
1. **P1-L1, P1-L2, P1-L3 → P1-T2** (sez. A, B). Formula esatta di R5-T2 nella classe 𝔅 di tipo esponenziale, su rettangolo limitato senza condizioni al bordo; serve a chiudere la riga LEDGER R5-T2[H1]. Il kill-argument ha dato WARN; le azioni applicate sono in PROOF_PACKAGE §10.
2. **P1-P1(e)** (sez. B). La mappa u ↦ E^add non è continua in H^m(Ω) per l'avvezione–diffusione: risposta negativa a R5-T2 nel quadro H1. Un giudice del kill-argument l'ha già verificata, con 3 difetti minori ora corretti.
3. **P1-T5** (sez. C). Impossibilità della fattorizzazione in flussi dei termini quando l'orbita ad_X^k Y è infinita; sostituisce R5-Q5, che come scritta è falsa (P1-C1, banale).
4. **P1-L4, P1-P2(c)** (sez. D). Componenti per fattore in 𝔅 per P = Π(τ − a_j(ξ)).
5. **P1-P4** (sez. E). Fattori del 2° ordine: fattorizzazione di Gauss per operatori, tempo uniforme T*.
6. **P1-P6** (sez. F). E_int dal bordo.
7. P1-T4 (sez. G). Bassa priorità: in gran parte classico (Lie, Wei–Norman).

## Notazione minima e fatti esterni usati
- $R=\mathbb C[\tau,\xi]$, con $\tau\leftrightarrow\partial_t$ e $\xi\leftrightarrow\partial_x$. $\Omega=I\times J$, con $I$, $J=(a,b)$ intervalli aperti limitati. EP = esponenziale-polinomio $\sum p_k(t,x)e^{\sigma_kt+\zeta_kx}$.
- Per $A=\sum_l\alpha_l\xi^l$: $|A|(r):=\sum_l|\alpha_l|r^l$.
- **C12-T1** (fatto esterno, S-C1C2, in audit separato). Sia $\Omega$ un rettangolo, $P=c\prod Q_j$ con $Q_j$ potenze di irriducibili non associati. Allora $\ker_{\mathcal D'}P=\sum_j\ker_{\mathcal D'}Q_j$; il nucleo $\mathcal N$ della mappa somma ha dimensione finita $\delta(P)$ ed è fatto di EP.
- **C12-T2(i)** (Vandermonde). Sia $P=\prod_j(\tau-a_j(\xi))$ con $a_j$ distinti, e sia $V=[a_j^l]$, $\Delta=\det V$. Per ogni scomposizione vale $\Delta(\partial_x)u_j=\sum_l\mathrm{adj}(V)_{jl}(\partial_x)\partial_t^lu$.
- **C12-L1.** Sul rettangolo: $\ker_{\mathcal D'}\partial_x=\mathcal D'(I)\otimes1$, ed esistono primitive in $x$ che commutano con $\partial_t$.
- **C12-P1(b).** Nel caso comassimale $u_j=E_j(\partial)u$, con $E_j\in R$.
- **II-L1 / II-T7(a).** $Q(\partial)u=0\iff\partial_t(u,\partial_tu)=C(\partial_x)(u,\partial_tu)$ per $Q=\tau^2+b\tau+c$, e $e^{tC(\zeta)}=\begin{psmallmatrix}\varphi_1&\varphi_2\\\varphi_1'&\varphi_2'\end{psmallmatrix}$.
- **CON-FONTE** (da controllare come citazioni):
  - soluzione di Tychonoff (F. John, *PDE*, cap. 7);
  - Rudin, *Functional Analysis*, Thm 10.27 (calcolo funzionale olomorfo);
  - Humphreys §4.1 Cor. A (teorema di Lie);
  - Wei–Norman 1963/1964;
  - generazione dei semigruppi standard (Lumer–Phillips, Hille–Yosida).

## Domande specifiche al revisore
- **P1-L3(a).** È corretto il passaggio dall'equazione in $\mathcal D'(\Omega)$ all'equazione in $\mathcal D'(I;B_\rho)$? Il passaggio usa test di tipo prodotto $\varphi\otimes\psi$ e l'iniettività $B_\rho\hookrightarrow L^2(J)$. Anche le traccia agli estremi di $\bar I$ in P1-L1(d) vanno controllate.
- **P1-T2(iii).** Serve la continuità di $\zeta\mapsto e^{\zeta x}\in B_{\rho'}$ sul supporto della misura (con $\rho'$ maggiore del raggio del supporto).
- **P1-P1(e).** Controllare le costanti e la condizione $D\zeta^2t\ge\log2$.
- **P1-T5.**
  - È legittimo derivare in $\varepsilon$ coefficiente per coefficiente?
  - La riduzione alle somme di momenti $\sum q_i\tau_i^k=t^{k+1}/(k+1)$ usa che i germi convergono su un disco comune: è corretta?
  - L'argomento di rango di Hankel è completo?
  - L'ipotesi "flussi di Y spenti a ε = 0" è davvero necessaria, o si può togliere?
- **P1-P2(c).** Controllare la descrizione di $\ker_{\mathcal D'}\Delta(\partial_x)$ sul rettangolo e le stime sull'ODE con forzante di tipo esponenziale.
- **P1-P4(b,c).** Controllare il calcolo funzionale nell'algebra commutativa $\mathcal C$ e l'esistenza del logaritmo continuo in $t$ e olomorfo in $\zeta$.

## A. Classe e lemmi (P1-D1, P1-L1, P1-L2, P1-L3)
### [P1-D1] Definizione
Per $\rho>0$:
$$B_\rho(J):=\{f\in C^\infty(J):\ \|f\|_{B_\rho}:=\sup_{j\ge0}\rho^{-j}\|f^{(j)}\|_{L^2(J)}<\infty\},\qquad \mathfrak B_\rho(\Omega):=\{u\in C^\infty(\Omega):\ \|u\|_{\mathfrak B_\rho}:=\sup_{i,j\ge0}\rho^{-i-j}\|\partial_t^i\partial_x^ju\|_{L^2(\Omega)}<\infty\},$$
$B(J):=\bigcup_\rho B_\rho(J)$, $\mathfrak B(\Omega):=\bigcup_\rho\mathfrak B_\rho(\Omega)$ ("funzioni di tipo esponenziale su $\Omega$").
*Interpretazione (non usata nelle prove).* Per Taylor e Sobolev, $f\in B_\rho(J)$ si estende a una funzione intera di tipo esponenziale $\le\rho$; è la classe "PW_A" suggerita da PR-C2d §3.7 ("ogni componente genera un gruppo limitato") e la versione su $\Omega$ limitato della proposta I-3 dell'audit.

### [P1-L1] Proprietà della classe — prova scritta
(a) $B_\rho(J)$ e $\mathfrak B_\rho(\Omega)$ sono spazi di Banach; $\partial_x:B_\rho\to B_\rho$ è limitato con $\|\partial_x\|\le\rho$ (idem $\partial_t,\partial_x$ su $\mathfrak B_\rho$).
(b) $\mathfrak B_\rho(\Omega)\hookrightarrow H^m(\Omega)$ e $B_\rho(J)\hookrightarrow H^m(J)$ con continuità, per ogni $m$; $\rho\le\rho'\Rightarrow\|f\|_{B_{\rho'}}\le\|f\|_{B_\rho}$.
(c) Ogni EP sta in $\mathfrak B(\Omega)$: $t^kx^le^{\sigma t+\zeta x}\in\mathfrak B_\rho$ per ogni $\rho>\max(|\sigma|,|\zeta|)$.
(d) (tracce) Se $u\in\mathfrak B_\rho(\Omega)$, la mappa $t\mapsto u(t,\cdot)$ si estende a $\bar I$ e appartiene a $C(\bar I;B_{\rho'}(J))$ per ogni $\rho'>\rho$, con $\sup_t\|u(t)\|_{B_\rho}\le C_I(1+\rho)\|u\|_{\mathfrak B_\rho}$, $C_I:=\max(|I|^{-1/2},|I|^{1/2})$.
**Prova.** (a) Se $(f_k)$ è di Cauchy in $B_\rho$, ogni $(f_k^{(j)})_k$ è di Cauchy in $L^2(J)$ con limite $g_j$, e $g_{j+1}=g_j'$ in $\mathcal D'(J)$ (limite di distribuzioni); quindi $g_0\in H^\infty(J)\subset C^\infty(J)$, $g_0^{(j)}=g_j$, e $\rho^{-j}\|g_j-f_k^{(j)}\|\le\limsup_l\rho^{-j}\|f_l^{(j)}-f_k^{(j)}\|$ è piccolo uniformemente in $j$. $\|f'\|_{B_\rho}=\rho\sup_j\rho^{-(j+1)}\|f^{(j+1)}\|\le\rho\|f\|_{B_\rho}$. Identico per $\mathfrak B_\rho$.
(b) $\|u\|^2_{H^m}=\sum_{i+j\le m}\|\partial_t^i\partial_x^ju\|^2\le\binom{m+2}{2}\max(1,\rho)^{2m}\|u\|^2_{\mathfrak B_\rho}$. La monotonia in $\rho$ è immediata.
(c) $\partial_x^j(x^le^{\zeta x})=\sum_{i\le\min(j,l)}\binom ji\frac{l!}{(l-i)!}x^{l-i}\zeta^{j-i}e^{\zeta x}$, dunque $\|\partial_x^j(x^le^{\zeta x})\|_{L^2(J)}\le C_l(1+j)^l\max(|\zeta|,\eta)^{j}\eta^{-l}$ per ogni $\eta>0$ (se $\zeta=0$ le derivate di ordine $>l$ sono nulle). Poiché $(1+j)^l(\mu/\rho)^j$ è limitata per $\mu<\rho$, si ottiene $\le C\rho^j$ per $\rho>|\zeta|$; lo stesso in $t$ e per il prodotto (Leibniz non serve: le variabili sono separate).
(d) Per $v$ con $v,\partial_tv\in L^2(\Omega)$ si ha $v\in C(\bar I;L^2(J))$ e $\sup_t\|v(t)\|\le C_I(\|v\|_{L^2(\Omega)}+\|\partial_tv\|_{L^2(\Omega)})$ (immersione $H^1(I;L^2(J))\hookrightarrow C(\bar I;L^2(J))$: $v(t)=v(s)+\int_s^t\partial_tv$, media in $s$ e Cauchy–Schwarz). Con $v=\partial_x^ju$: $\sup_t\|\partial_x^ju(t)\|\le C_I(1+\rho)\rho^j\|u\|_{\mathfrak B_\rho}$. Per la continuità in $B_{\rho'}$: dato $\epsilon$, si sceglie $j_0$ con $2C_I(1+\rho)\|u\|(\rho/\rho')^j<\epsilon$ per $j\ge j_0$; per $j<j_0$ ogni $t\mapsto\rho'^{-j}\partial_x^ju(t)$ è continua in $L^2(J)$. ∎

### [P1-L2] Flussi dei termini — prova scritta, SymPy C1 (6/6)
Sia $A\in\mathbb C[\xi]$. Su $B_\rho(J)$: $\|A(\partial_x)\|\le|A|(\rho)$; per $s\in\mathbb C$ la serie $e^{sA(\partial_x)}:=\sum_{k\ge0}\frac{s^k}{k!}A(\partial_x)^k$ converge in norma in $\mathcal L(B_\rho)$, con $\|e^{sA(\partial_x)}\|\le e^{|s||A|(\rho)}$. Inoltre:
(a) $s\mapsto e^{sA(\partial_x)}$ è intera, $\frac{d}{ds}e^{sA(\partial_x)}=A(\partial_x)e^{sA(\partial_x)}$, $e^{(s+r)A}=e^{sA}e^{rA}$; per $A,A'\in\mathbb C[\xi]$: $e^{sA(\partial_x)}e^{rA'(\partial_x)}=e^{rA'(\partial_x)}e^{sA(\partial_x)}$ e $e^{s(A+A')(\partial_x)}=e^{sA(\partial_x)}e^{sA'(\partial_x)}$.
(b) L'operatore non dipende da $\rho$: per $\rho<\rho'$ l'operatore su $B_{\rho'}$ ristretto a $B_\rho$ è quello su $B_\rho$.
(c) $e^{sA(\partial_x)}(x^le^{\zeta x})=\partial_\zeta^l\big(e^{sA(\zeta)}e^{\zeta x}\big)$ per ogni $\zeta\in\mathbb C$, $l\in\mathbb N$.
**Prova.** $\|A(\partial)\|\le\sum|\alpha_l|\|\partial\|^l\le|A|(\rho)$ (P1-L1a). (a) $A(\partial),A'(\partial)$ commutano (polinomi nello stesso operatore); in un'algebra di Banach $e^{X+Y}=e^Xe^Y$ se $XY=YX$ (prodotto di Cauchy di serie assolutamente convergenti); derivazione termine a termine. (b) stessa serie, inclusione continua. (c) Per $|\zeta|<\rho$ la funzione $\zeta\mapsto e_\zeta:=e^{\zeta x}\in B_\rho(J)$ è olomorfa: $\sum_n|\zeta|^n\|x^n/n!\|_{B_\rho}\le\sum_n\sum_{j\le n}|\zeta|^n\rho^{-j}R^{n-j}|J|^{1/2}/(n-j)!=|J|^{1/2}\sum_j(|\zeta|/\rho)^j\,e^{|\zeta|R}<\infty$, $R:=\max(|a|,|b|)$. $A(\partial)^ke_\zeta=A(\zeta)^ke_\zeta$ dà $e^{sA(\partial)}e_\zeta=e^{sA(\zeta)}e_\zeta$. Un operatore limitato commuta con $\partial_\zeta^l$ di una funzione olomorfa a valori in $B_\rho$, e $\partial_\zeta^le_\zeta=x^le_\zeta$. Per $\zeta$ qualsiasi si sceglie $\rho>|\zeta|$ e si usa (b). ∎
SymPy C1: per $A=\xi^2$ e $A=-c\xi+\beta\xi^3$, $l=0,1,2$, i coefficienti in $s$ fino a $s^5$ della serie coincidono con quelli di $\partial_\zeta^l(e^{sA(\zeta)}e^{\zeta x})$.

### [P1-L3] Problema di Cauchy nella classe — prova scritta
Sia $A\in\mathbb C[\xi]$, $\rho>0$, $t_0\in\bar I$.
(a) (unicità ed esistenza) Se $v\in C(\bar I;B_\rho(J))$ e $(\partial_t-A(\partial_x))v=0$ in $\mathcal D'(\Omega)$, allora $v\in C^1(\bar I;B_\rho)$ e $v(t)=e^{(t-t_0)A(\partial_x)}v(t_0)$ per ogni $t\in\bar I$.
(b) Viceversa, per $f\in B_\rho(J)$, $v(t):=e^{(t-t_0)A(\partial_x)}f$ è in $C^\infty(\bar I;B_\rho)$, risolve l'equazione, e come funzione su $\Omega$ appartiene a $\mathfrak B_{\rho''}(\Omega)$, $\rho'':=\max(\rho,|A|(\rho))$.
(c) Lo stesso vale per sistemi $\partial_tV=C(\partial_x)V$, $C\in\mathrm{Mat}_k(\mathbb C[\xi])$, su $B_\rho(J)^k$.
**Prova.** (a) Siano $\varphi\in C_c^\infty(I)$, $\psi\in C_c^\infty(J)$. L'equazione testata su $\varphi\otimes\psi$, con $v(t)\in H^\infty(J)$ e integrazione per parti in $x$ (ψ a supporto compatto), dà $\int_I[-\varphi'(t)\langle v(t),\psi\rangle-\varphi(t)\langle A(\partial)v(t),\psi\rangle]dt=0$. Quindi l'integrale di Bochner $F:=-\int\varphi'v\,dt-\int\varphi A(\partial)v\,dt\in B_\rho$ verifica $\langle F,\psi\rangle=0$ per ogni $\psi$, cioè $F=0$ in $L^2(J)$ e dunque in $B_\rho$. Allora la derivata distribuzionale di $v$, come distribuzione a valori in $B_\rho$, è $A(\partial)v\in C(\bar I;B_\rho)$; ne segue $v(t)=v(t_0)+\int_{t_0}^tA(\partial)v(s)ds$ (una distribuzione a valori in uno spazio di Banach con derivata nulla su un intervallo è costante: si applicano i funzionali continui e Hahn–Banach), e $v\in C^1$. Per $w(t):=e^{-(t-t_0)A(\partial)}v(t)$ la regola del prodotto ($C^1$ a valori operatori × $C^1$ a valori vettori) dà $w'=-A e^{\dots}v+e^{\dots}Av=0$, quindi $w\equiv v(t_0)$. (b) P1-L2(a); $\partial_t^i\partial_x^jv=A(\partial)^i\partial^je^{(t-t_0)A}f$, con norma $L^2(J)\le|A|(\rho)^i\rho^je^{|I||A|(\rho)}\|f\|_{B_\rho}$; integrando in $t$ si ottiene la stima $\mathfrak B_{\rho''}$. (c) identico, con $\|C(\partial)\|$ stimata dalla norma di riga massima delle $|C_{ij}|(\rho)$. ∎
*Osservazione (ipotesi I-2(b) dell'audit).* (a) è il "teorema di unicità" che manca su $\Omega$ limitato: nella classe, $v(t_0)=0\Rightarrow v\equiv0$. Le soluzioni alimentate dal bordo o di Tychonoff (dato iniziale nullo, $v\not\equiv0$) **non** stanno in $\mathfrak B$.

## B. Definizione usata (P1-D3) e teorema principale (P1-T2), necessità e no-go in H^m (P1-P1)
### [P1-D3] $E_{int}$ dentro un fattore di evoluzione — definizione
Fattore $Q=\tau-a(\xi)$, $a=\sum_{n=1}^Na_n$, $a_n\in\mathbb C[\xi]$ (i "termini": di solito monomi $\lambda_n\xi^{l_n}$; si ammette qualsiasi raggruppamento per l'identità algebrica, ma il quadro additivo ha significato quantitativo solo per raggruppamenti **ammissibili**, $\sup_{\kappa\in\mathbb R}\mathrm{Re}\,a_n(i\kappa)<\infty$ per ogni $n$ — es. $\pm\xi^2$ non è ammissibile). $t_0\in\bar I$ tempo base, $u_0:=u(t_0,\cdot)$.
- (a) **quadro formale (getto in t)**, per ogni $u\in C^\infty(\Omega)\cap\ker Q$ e $t_0\in I$: $\hat S_n(s):=\sum_k\frac{s^k}{k!}a_n(\partial_x)^k\in\mathrm{End}(C^\infty(J))[[s]]$, $\hat u(s):=\sum_k\frac{s^k}{k!}\partial_t^ku(t_0,\cdot)$, e
$$E^{add,form}_{int}(s):=\hat u(s)-u_0-\sum_n\big(\hat S_n(s)u_0-u_0\big)\in C^\infty(J)[[s]].$$
- (b) **quadro additivo**, per $u\in\mathfrak B(\Omega)\cap\ker Q$: $u_n(t):=e^{(t-t_0)a_n(\partial_x)}u_0$ (P1-L2, su $B_{\rho'}(J)$ con $\rho'$ di P1-L1(d)) e
$$E^{add}_{int}(t):=u(t)-u_0-\sum_{n=1}^N\big(u_n(t)-u_0\big).$$
- (c) **quadro moltiplicativo**: $E^{mult}_{int}(t):=e^{(t-t_0)a(\partial_x)}-\prod_ne^{(t-t_0)a_n(\partial_x)}\in\mathcal L(B_{\rho'})$ (errore di splitting); forma invertibile $\mathfrak E^{mult}(t):=\big(\prod_ne^{(t-t_0)a_n}\big)^{-1}e^{(t-t_0)a}$.
- (d) **log-simbolo**: per $u=\int e^{a(\zeta)t+\zeta x}d\mu(\zeta)$, $\mu$ a supporto compatto, $\partial_t\log$ della densità spettrale $=\sum_na_n(\zeta)$: $E^{log}\equiv0$ (lettura lineare dei termini, G★′-3).
- (e) **per regimi** [TROP-L2]: la scomposizione a bande usa indicatrici $1_B$ della variabile spettrale, che non sono moltiplicatori polinomiali; su $\Omega$ limitato la misura di Ehrenpreis non è unica e le bande non sono intrinseche (TROP-7). Non la si adotta come definizione canonica su $\Omega$; resta un corollario di regime su ℝ.
*Coerenza.* (a) ⊂ (b): per $u\in\mathfrak B$ la serie formale converge al quadro (b) (P1-T2(iv)). (b) è la definizione R5-D1(a) con i semigruppi sostituiti dai gruppi limitati di P1-L2. (c) è R5-D1(b).
### [P1-T2] R5-T2 nella classe di tipo esponenziale $\mathfrak B(\Omega)$ — PROVABLE AFTER EXTRA ASSUMPTION (classe 𝔅); prova scritta; SymPy C2, C3
**Portata (corretta dopo il kill-argument, §10).** P1-T2 **non** dà R5-T2 nel quadro H1 = $H^m(\Omega)$: lì il quadro additivo per termini può non esistere come mappa continua (P1-P1(e), avvezione–diffusione). R5-T2[H1] (LEDGER: R5-T2 su $H^m(\Omega)$ limitato) riceve quindi una **risposta negativa nel quadro richiesto più un risultato positivo in un'altra classe**, non una dimostrazione in $H^m$. (A) Sulla classe 𝔅 (restrizioni di funzioni intere di tipo esponenziale) vale la formula esatta di R5-T2; qui $\partial_x$ è limitato e la limitatezza di $\Omega$ non ha alcun ruolo nella prova. (B) Su $H^m(\Omega)$ limitato l'estensione continua **può mancare**: P1-P1(e) lo dimostra per l'avvezione–diffusione (enunciato esistenziale; un no-go generale per ogni $Q$ con almeno due termini non costanti è P1-Q6, APERTO). (C) Il quadro formale (getto in t) vale per ogni $u$ liscia. La limitatezza di $\Omega$ entra solo in (B): rende ammissibili i modi esponenziali reali, che i flussi dei singoli termini amplificano.
**Ipotesi.** $\Omega=I\times J$ rettangolo limitato; $Q=\tau-a(\xi)$, $a=\sum_{n=1}^Na_n$, $a_n\in\mathbb C[\xi]$; $u\in\mathfrak B_\rho(\Omega)$ con $Q(\partial)u=0$ in $\mathcal D'(\Omega)$; $t_0\in\bar I$; $\rho'>\rho$; $u_0:=u(t_0,\cdot)\in B_{\rho'}(J)$ (P1-L1(d)).
**Tesi.**
(i) *(flussi per termine intrinseci)* Per ogni $n$ esiste una e una sola $u_n\in\mathfrak B(\Omega)$ con $(\partial_t-a_n(\partial_x))u_n=0$ e $u_n(t_0,\cdot)=u_0$; è $u_n(t)=e^{(t-t_0)a_n(\partial_x)}u_0$, indipendente da $\rho,\rho'$. Inoltre $u(t)=e^{(t-t_0)a(\partial_x)}u_0$.
(ii) *(formula chiusa)* Per ogni $t\in\bar I$, in $B_{\rho'}(J)$:
$$u(t)=\sum_{S\subseteq[N]}\prod_{n\in S}\big(e^{(t-t_0)a_n(\partial_x)}-I\big)u_0,\qquad E^{add}_{int}(t)=\sum_{|S|\ge2}\prod_{n\in S}\big(e^{(t-t_0)a_n(\partial_x)}-I\big)u_0,$$
$E^{mult}_{int}\equiv0$, $\mathfrak E^{mult}\equiv I$; $u_n$ ed $E^{add}_{int}$ (come funzioni su $\Omega$) stanno in $\mathfrak B(\Omega)\subset\bigcap_mH^m(\Omega)$.
(iii) *(forma spettrale)* Se $u_0=\int_{\mathbb C}e^{\zeta x}d\mu_0(\zeta)$ con $\mu_0$ misura complessa a supporto compatto (per esempio $u$ EP con esponenziali semplici: $\mu_0=\sum_kc_k\delta_{\zeta_k}$), allora $E^{add}_{int}(t)=\int e_{\ge2}\big(z(t-t_0,\zeta)\big)e^{\zeta x}d\mu_0(\zeta)$, con $z_n(s,\zeta):=e^{sa_n(\zeta)}-1$ ed $e_{\ge2}(z):=\prod_n(1+z_n)-1-\sum_nz_n=\sum_{k\ge2}e_k(z)$. Per un addendo con molteplicità $x^le^{\zeta_kx}$: $E^{add}_{int}=\partial_\zeta^l\big[e_{\ge2}(z(t-t_0,\zeta))e^{\zeta x}\big]_{\zeta=\zeta_k}$.
(iv) *(getto formale, ogni $u$ liscia)* Se $u\in C^\infty(\Omega)\cap\ker Q$ e $t_0\in I$, allora in $C^\infty(J)[[s]]$: $\hat u=\sum_S\prod_{n\in S}(\hat S_n-I)u_0$, e il coefficiente di $s^k/k!$ in $E^{add,form}_{int}$ è
$$\sum_{\substack{k_1+\dots+k_N=k\\ \#\{n:k_n>0\}\ge2}}\frac{k!}{k_1!\cdots k_N!}\,a_1(\partial_x)^{k_1}\cdots a_N(\partial_x)^{k_N}u_0 .$$
Se $u\in\mathfrak B(\Omega)$, questa serie è la serie di Taylor in $s$ della funzione intera $s\mapsto E^{add}_{int}(t_0+s)$ (a valori in $B_{\rho'}$), quindi converge.
(v) *(ipotesi dell'audit: incorporate nella definizione di 𝔅, non verificate in $H^m$; per $H^m$ vedi la Portata (B))* I-1: i flussi sono operatori limitati che commutano, quindi commutano come gruppi. I-2(a): ogni $a_n$ genera un gruppo intero (anche $-\partial_x^2$ dentro $-\partial_x^4-\partial_x^2$). I-2(b): la classe di unicità è $\mathfrak B$ (P1-L3(a)).
**Strategia.** Ridurre tutto a un'identità in un'algebra di Banach commutativa di operatori limitati (P1-L2) più un teorema di unicità nella classe (P1-L3). **Dipendenze.** P1-L1(d) → P1-L3 → (i); P1-L2(a) → (ii); P1-L2(c) e integrale di Bochner → (iii); algebra formale → (iv).
**Prova.** (i) Per P1-L1(d) $u\in C(\bar I;B_{\rho'})$; per P1-L3(a) con $A=a$: $u(t)=e^{(t-t_0)a(\partial)}u_0$. Per P1-L3(b) con $A=a_n$, $u_n(t):=e^{(t-t_0)a_n(\partial)}u_0$ esiste e sta in $\mathfrak B$. Se $v\in\mathfrak B_{\rho_1}(\Omega)$ è un'altra soluzione con $v(t_0)=u_0$, per P1-L1(d) $v\in C(\bar I;B_{\rho_2})$ con $\rho_2>\max(\rho_1,\rho')$, e per P1-L3(a) in $B_{\rho_2}$: $v(t)=e^{(t-t_0)a_n}u_0=u_n(t)$ (P1-L2(b)). Indipendenza da $\rho$: P1-L2(b).
(ii) P1-L2(a) iterato: $e^{(t-t_0)a(\partial)}=\prod_ne^{(t-t_0)a_n(\partial)}$, quindi $E^{mult}\equiv0$. Scrivendo $e^{(t-t_0)a_n}=I+(e^{(t-t_0)a_n}-I)$ e sviluppando il prodotto di $N$ elementi che commutano dell'algebra $\mathcal L(B_{\rho'})$ si ottiene la somma sui sottoinsiemi; i termini $|S|=0$ e $|S|=1$ sono $u_0$ e $u_n(t)-u_0$. Regolarità: P1-L3(b) per ogni prodotto $\prod_{n\in S}e^{(t-t_0)a_n}u_0=e^{(t-t_0)a_S}u_0$, $a_S:=\sum_{n\in S}a_n$; combinazioni finite; P1-L1(b).
(iii) Sia $r$ con $\mathrm{supp}\,\mu_0\subset\{|\zeta|\le r\}$ e $\rho'>r$. La mappa $\zeta\mapsto e_\zeta\in B_{\rho'}$ è continua sul supporto (P1-L2(c), prova), quindi $u_0=\int e_\zeta d\mu_0$ come integrale di Bochner in $B_{\rho'}$; gli operatori limitati passano sotto l'integrale e $\prod_{n\in S}(e^{sa_n(\partial)}-I)e_\zeta=\prod_{n\in S}z_n(s,\zeta)e_\zeta$; si somma su $|S|\ge2$. Molteplicità: P1-L2(c) e linearità.
(iv) Poiché $u\in C^\infty(\Omega)$ e $\partial_tu=a(\partial_x)u$, derivando $\partial_t^ku=a(\partial_x)^ku$ in $\Omega$, e in $t_0$: $\partial_t^ku(t_0,\cdot)=a(\partial_x)^ku_0$. Quindi $\hat u=\exp(s\,a(\partial_x))u_0$ nell'anello $\mathrm{End}(C^\infty(J))[[s]]$. Gli elementi $s\,a_n(\partial_x)$ commutano, e per elementi che commutano $\exp(X+Y)=\exp X\exp Y$ coefficiente per coefficiente (binomio di Newton); dunque $\hat u=\prod_n\hat S_nu_0=\sum_S\prod_{n\in S}(\hat S_n-I)u_0$. Il coefficiente si legge da $\prod_{n\in S}(\hat S_n-I)=\prod_{n\in S}\sum_{k_n\ge1}s^{k_n}a_n^{k_n}/k_n!$. Se $u\in\mathfrak B$, la funzione $s\mapsto E^{add}_{int}(t_0+s)$ di (ii) è intera a valori in $B_{\rho'}$ (combinazione finita di funzioni intere di P1-L2(a)) e i suoi coefficienti di Taylor sono dati dalla stessa espansione, che commuta con l'inclusione $B_{\rho'}\hookrightarrow C^\infty(J)$.
(v) Riassunto di (i)–(ii) e di P1-L2, P1-L3. ∎
**SymPy.** C2: (iv) fino a $t^4$ per $N=3$ ($a_1=D\xi^2$, $a_2=-c\xi$, $a_3=\beta\xi^3$), $u_0=f(x)$ generica: PASS. C3: (iii) con molteplicità $l=2$: PASS.
**Rischi.** (1) La classe 𝔅 è una scelta: è sufficiente, non necessaria (P1-P1 mostra solo che **una** regola di selezione è necessaria). (2) Anche se $\mathfrak B\cap\ker Q$ fosse densa in $\ker_{H^m}Q$ (P1-Q1), questo **non** permetterebbe di estendere $E^{add}$, perché la mappa non è continua (P1-P1(e)). (3) $E^{add}_{int}$ dipende dal tempo base $t_0$ (già in R5 §8). (4) D3 ammette raggruppamenti arbitrari dei termini. Con termini mal posti su ℝ (es. $a_1=\xi^2$, $a_2=-\xi^2$, obiezione del kill-argument) la formula resta vera, ma $E^{add}$ cresce come $e^{s\kappa^2}$ già sui modi di Fourier. Il quadro additivo ha quindi senso quantitativo solo per termini con $\mathrm{Re}\,a_n(i\kappa)$ limitata superiormente, e anche in quel caso non in $H^m(\Omega)$ (P1-P1(e)). (5) In $H^m$ il contenuto robusto per termine è la lettura lineare del log-simbolo (D3(d)) e l'identità moltiplicativa $E^{mult}=0$ su ogni $B_\rho$, non il valore di $E^{add}$.

### [P1-P1] Senza una classe i flussi per termine non sono determinati da $u$ — prova scritta (+ CON-FONTE per (b))
Sia $I=(0,T)$, $t_0=0$.
(a) (trasporto) Per $a_n=\xi$ e $f\in C^\infty(\bar J)$ dato, le $v\in C^\infty(\Omega)$ con $\partial_tv=\partial_xv$ e $v(0,\cdot)=f$ sono esattamente $v(t,x)=F(x+t)$ con $F\in C^\infty((a,b+T))$ estensione di $f$: infinite se $T>0$.
(b) (calore) Per $a_n=\xi^2$ esiste $v\in C^\infty(\bar\Omega)$, $v\not\equiv0$, con $\partial_tv=\partial_x^2v$ e $v(0,\cdot)=0$ (soluzione di Tychonoff $v=\sum_kg^{(k)}(t)x^{2k}/(2k)!$, $g(t)=e^{-t^{-2}}$; F. John, *Partial Differential Equations*, cap. 7; Tychonoff 1935 — CON-FONTE); quindi i flussi del termine diffusivo con dato $u_0$ formano uno spazio affine di dimensione infinita.
(c) Di conseguenza, per $Q=\tau-\xi-\xi^2$ e $u\in\ker Q$ qualsiasi, $E^{add}_{int}$ "con $u_n$ soluzione qualsiasi del termine $n$ con dato $u_0$" non è una funzione di $u$. In $\mathfrak B$ invece è unica (P1-T2(i)); nel quadro formale (D3(a)) è unica per ogni $u$ liscia.
(d) L'ipotesi giusta è $u\in\mathfrak B$, non $u_0\in B(J)$: per $Q=\tau-\xi^2$ la funzione di (b) ha $u_0=0\in B(J)$ ma $u=v\ne e^{t\partial^2}u_0=0$.
(e) **(nessuna estensione continua a $H^m$)** Sia $Q=\tau+c\xi-D\xi^2$ (avvezione–diffusione, $c,D>0$), $a_1=-c\xi$, $a_2=D\xi^2$, $t_0=0$. Per ogni $m\in\mathbb N$: $\sup\{\|E^{add}_{int}\|_{L^2(\Omega)}/\|u\|_{H^m(\Omega)}:\ u\ \text{EP},\ Q(\partial)u=0\}=\infty$. Quindi $u\mapsto E^{add}_{int}$ non si estende per continuità da $\mathfrak B\cap\ker Q$ a $\ker_{H^m(\Omega)}Q$, qualunque sia la densità.
**Prova.** (a) Nelle coordinate $(t,y=x+t)$ l'equazione è $\partial_tv=0$ sul parallelogramma immagine, quindi $v=F(y)$ (C12-L1, $\ker\partial_t$ su domini convessi lungo $t$); $F$ è determinata su $J$ dal dato e libera su $(b,b+T)$, purché liscia. (b) fonte citata; la restrizione a $\bar\Omega$ è liscia perché $v$ è intera in $x$ e $C^\infty$ in $t$. (c), (d) da (a), (b) e P1-T2(i). (e) Per $\zeta>c/D$ reale sia $u_\zeta:=e^{a(\zeta)t+\zeta x}$, con $a(\zeta)=D\zeta^2-c\zeta>0$, e sia $e:=\|e^{\zeta x}\|_{L^2(J)}$. Poiché $\partial_t^i\partial_x^ju_\zeta=a^i\zeta^ju_\zeta$ e $t\mapsto e^{at}$ è crescente, $\|u_\zeta\|^2_{H^m(\Omega)}\le C_m(1+\zeta)^{4m}T\,e^{2a(\zeta)T}e^2$. D'altra parte $E^{add}_{int}(t)=z_1z_2e^{\zeta x}$, dove $|z_1|=1-e^{-c\zeta t}\ge\tfrac12$ per $t\ge T/2$ e $\zeta\ge2\log2/(cT)$, e $|z_2|=e^{D\zeta^2t}-1\ge\tfrac12e^{D\zeta^2t}$ (vale se $D\zeta^2t\ge\log2$, vero per $t\ge T/2$ e $\zeta^2\ge2\log2/(DT)$). Quindi, per $\zeta^{-2}\le T/2$: $\|E^{add}_{int}\|^2_{L^2(\Omega)}\ge\frac1{16}\int_{T-\zeta^{-2}}^Te^{2D\zeta^2t}dt\,e^2\ge\frac{e^{-2D}}{16\zeta^2}e^{2D\zeta^2T}e^2$. Il rapporto dei **quadrati** delle norme è $\ge c_m\zeta^{-4m-2}e^{2c\zeta T}\to\infty$ (quindi anche quello delle norme). Poiché $u\mapsto E^{add}$ è lineare, è illimitata e non ha estensione continua. ∎ (Qui $e$ indica $\|e^{\zeta x}\|_{L^2(J)}$, non il numero di Nepero.)
*Lettura di (e).* Il flusso del solo termine diffusivo amplifica il modo reale $e^{\zeta x}$ di un fattore $e^{D\zeta^2t}$, mentre la soluzione completa è smorzata dal trasporto di un fattore $e^{-c\zeta t}$. Su ℝ con dati $L^2$ i modi reali non compaiono ($\zeta=i\kappa$, e $|z_n|\le2$ per $t\ge0$ quando i termini sono dissipativi o dispersivi); su $\Omega$ limitato invece sì (P1-L1(c)). È un secondo meccanismo di "E_int dal dominio limitato", accanto al bordo (P1-P6), all'angolo (C12-C1) e allo strato limite (TROP-7). SymPy `p1_checks2.py` (3/3 PASS): esponente $2cT$ del rapporto, $|z_1|\to1$, esempio $\pm\xi^2$ del kill-argument.

## C. Impossibilità (P1-L5, P1-T5)
### [P1-L5] Lemmi formali — prova scritta (classico)
In $\mathcal A[[t]]$, per $g\in t\mathbb C[[t]]$ e $X,Y\in\mathcal A$:
(a) $e^{gX}:=\sum g^kX^k/k!$ è ben definito, $(e^{gX})'=g'Xe^{gX}$ e $e^{gX}e^{-gX}=1$;
(b) $e^{gX}Ye^{-gX}=\sum_kg^k\mathrm{ad}_X^kY/k!$;
(c) $U'=A(t)U$, $U(0)=1$ ha un'unica soluzione, che per $A$ costante è $e^{tA}$;
(d) se $U=\prod_{i=1}^de^{g_iX_i}$, allora $U'U^{-1}=\sum_ig_i'\,\mathrm{Ad}(P_{i-1})X_i$ con $P_{i-1}:=\prod_{j<i}e^{g_jX_j}$.
**Prova.** (a) Ogni coefficiente di $t^m$ è una somma finita, e $g$ è scalare, quindi commuta. (b) $F(\sigma):=e^{\sigma gX}Ye^{-\sigma gX}$ e $\sum\sigma^kg^k\mathrm{ad}^k_XY/k!$ risolvono entrambe $F'=g[X,F]$, $F(0)=Y$ nell'anello $\mathcal A[[t]][[\sigma]]$; si pone poi $\sigma=1$, il che è lecito perché $g\in t\mathbb C[[t]]$. (c) Ricorrenza $(m+1)U_{m+1}=\sum_{i\le m}A_iU_{m-i}$. (d) Regola del prodotto e somma telescopica. ∎
### [P1-T5] Impossibilità per orbite aggiunte infinite — prova scritta, SymPy C9
**Ipotesi.** $X,Y\in\mathcal A$ verificano (H): $X,\ Y_0:=Y,\ Y_1:=\mathrm{ad}_XY,\ Y_2:=\mathrm{ad}_X^2Y,\dots$ sono linearmente indipendenti.
**Tesi.** Non esistono una parola finita $(Z_1,\dots,Z_d)\in\{X,Y\}^d$ e funzioni $g_i(t,\varepsilon)$, olomorfe in un intorno di $(0,0)$, con $g_i(0,\varepsilon)=0$ e $g_i(t,0)\equiv0$ quando $Z_i=Y$, tali che
$$e^{t(X+\varepsilon Y)}=\prod_{i=1}^de^{g_i(t,\varepsilon)Z_i}\quad\text{in }\mathcal A[[t]]\ \text{per ogni }\varepsilon\text{ vicino a }0 .$$
*Lettura.* Consideriamo le formule chiuse che sono prodotti finiti di flussi dei termini, con tempi analitici nel tempo e nell'accoppiamento e con il flusso di $Y$ spento ad accoppiamento nullo. Nessuna di esse rappresenta il flusso completo. Detto altrimenti, $\mathfrak E^{mult}$ non è un prodotto finito di flussi dei termini uniforme nell'accoppiamento. Questo **non** significa che l'equazione non si possa risolvere (vedi l'esempio sotto).
**Prova.**
*Passo 1* ($\varepsilon=0$). I fattori in $Y$ sono l'identità, quindi $e^{tX}=e^{G(t)X}$ con $G:=\sum_{Z_i=X}g_i(t,0)$. Se fosse $G\ne t$, detto $m$ l'ordine di $G-t$, il coefficiente di $t^m$ in $e^{(G-t)X}=1$ darebbe $(G-t)_mX=0$; questo è impossibile perché $X\ne0$ per (H). Quindi $G=t$.
*Passo 2* (derivata in $\varepsilon$ in 0). Si deriva coefficiente per coefficiente in $t$; ogni coefficiente è una somma finita di funzioni olomorfe di $\varepsilon$.
- A sinistra, per Duhamel formale: $\partial_\varepsilon e^{t(X+\varepsilon Y)}|_0=e^{tX}\int_0^te^{-\sigma X}Ye^{\sigma X}d\sigma=e^{tX}\sum_k(-1)^k\frac{t^{k+1}}{(k+1)!}Y_k$ (SymPy C9c).
- A destra, per $\varepsilon=0$ tutti i fattori sono esponenziali di $X$. I fattori $Z_i=X$ contribuiscono $r(t)Xe^{tX}$ con $r=\sum_{Z_i=X}\partial_\varepsilon g_i(t,0)$. I fattori $Z_i=Y$ contribuiscono $q_i(t)e^{G_iX}Ye^{(t-G_i)X}$, con $q_i:=\partial_\varepsilon g_i(t,0)$ e $G_i:=\sum_{j<i,Z_j=X}g_j(t,0)$.
Moltiplicando a sinistra per $e^{-tX}$ e usando P1-L5(b) con $\tau_i:=t-G_i\in t\mathbb C[[t]]$, si ottiene
$$rX+\sum_k(-1)^kY_k\sum_{i:Z_i=Y}q_i\frac{\tau_i^k}{k!}=\sum_k(-1)^k\frac{t^{k+1}}{(k+1)!}Y_k .$$
*Passo 3.* Il coefficiente di $t^m$ coinvolge solo $X,Y_0,\dots,Y_m$. Per (H) si ha quindi $r=0$ e, per ogni $k\ge0$, $\sum_{i:Z_i=Y}q_i(t)\tau_i(t)^k=t^{k+1}/(k+1)$ come serie formali. Le $q_i,\tau_i$ sono un numero finito di germi convergenti su un disco comune $|t|<r_0$, quindi l'uguaglianza vale su quel disco come uguaglianza di funzioni, per ogni $k$.
*Passo 4.* Si fissano $t\in(0,r_0)$ e $p:=\#\{i:Z_i=Y\}$. La successione $m_k:=t^{k+1}/(k+1)=\sum_{i=1}^pq_i\tau_i^k$ ha matrici di Hankel $H_n=[m_{i+j}]_{i,j<n}=W^{\mathsf T}\mathrm{diag}(q)W$, con $W_{ij}=\tau_i^j$, e quindi di rango $\le p$. D'altra parte $H_n=t\,\mathrm{diag}(t^i)\,\mathrm{Hilb}_n\,\mathrm{diag}(t^j)$, dove $\mathrm{Hilb}_n=[1/(i+j+1)]$ è la matrice di Hilbert (Gram dei monomi in $L^2(0,1)$, definita positiva); quindi $H_n$ ha rango $n$. Per $n=p+1$ si ottiene una contraddizione (se $p=0$, basta $m_0=t\ne0$). ∎
SymPy C9d: $\det H_n=t^{n^2}\det\mathrm{Hilb}_n\ne0$ per $n\le7$. C9e: rango ≤ p per una somma finita.
*Esempio (L4).* In $A_1$ siano $X=x^a\partial$ e $Y=\partial$ con $a\ge3$. Da $\mathrm{ad}_X(x^b\partial)=(b-a)x^{a+b-1}\partial$ segue $Y_k=c_kx^{k(a-1)}\partial$ con $c_k=\prod_{j<k}(j(a-1)-a)\ne0$ (perché $a-1\nmid a$ per $a\ge3$). I gradi sono distinti e diversi da $a$, quindi vale (H) (SymPy C9a; per $a=2$ l'orbita è finita, C9b). Il trasporto a velocità polinomiale $u_t=(x^a+\varepsilon)u_x$ si risolve esplicitamente per caratteristiche: P1-T5 esclude solo la fattorizzazione in flussi dei termini, non l'esistenza di una forma chiusa.
*Portata.* (H) implica $\dim\mathfrak g=\infty$, ma **non** vale per $\langle\partial^2,x^k\rangle$ con $k\ge3$ (R5-P7). Lì $\mathrm{ad}_{\partial^2}$ e $\mathrm{ad}_{x^k}$ sono localmente nilpotenti sull'altro termine, e la dimensione infinita nasce dai commutatori annidati. In questi casi l'impossibilità richiede l'analisi agli ordini superiori in $\varepsilon$: **APERTO** (P1-Q3).

## D. Fattori in 𝔅 (P1-L4, P1-P2)
### [P1-L4] La primitiva di Volterra conserva 𝔅 — prova scritta
Sia $r\in\mathbb C[\xi]$ con $\deg r=\delta\ge1$, $r=\ell\xi^\delta+\sum_{l<\delta}r_l\xi^l$; siano $F\in\mathfrak B_\rho(\Omega)$ e $x_0\in J$. Sia $G$ la soluzione su ℝ di $r(\partial)G=0$ con $G^{(i)}(0)=0$ per $i<\delta-1$ e $G^{(\delta-1)}(0)=1/\ell$, e sia $w(t,x):=\int_{x_0}^xG(x-y)F(t,y)\,dy$. Allora $r(\partial_x)w=F$ e $w\in\mathfrak B_R(\Omega)$ con $R:=\max(1,\rho,2\sum_l|r_l|/|\ell|)$.
**Prova.** Per variazione delle costanti, $\partial_x^iw=\int G^{(i)}(x-y)F\,dy$ per $i\le\delta-1$ e $\partial_x^\delta w=F/\ell+\int G^{(\delta)}F$; quindi $r(\partial_x)w=F$, e $w\in C^\infty(\Omega)$. Sia $N_j:=\sup_i\rho^{-i}\|\partial_t^i\partial_x^jw\|_{L^2(\Omega)}$.
Per $j<\delta$, Cauchy–Schwarz in $y$ e integrazione in $x$ danno $N_j\le|J|\sup_{|z|\le|J|}|G^{(j)}(z)|\,\|F\|_{\mathfrak B_\rho}=:C_0\|F\|$.
Per $j\ge\delta$ si ha $\partial_x^jw=(\partial_x^{j-\delta}F-\sum_{l<\delta}r_l\partial_x^{j-\delta+l}w)/\ell$, quindi $N_j\le(\rho^{j-\delta}\|F\|+\sum_l|r_l|N_{j-\delta+l})/|\ell|$.
Sia $K:=\max(C_0,2/(|\ell|R^\delta))\|F\|$. Per induzione $N_j\le KR^j$: il primo addendo è $\le KR^j/2$ perché $\rho\le R$; il secondo è $\le KR^j\sum_l|r_l|R^{l-\delta}/|\ell|\le KR^j/2$ perché $R\ge1$, $l-\delta\le-1$ e $R\ge2\sum|r_l|/|\ell|$. Poiché $\rho^i\le R^i$, si conclude $\|w\|_{\mathfrak B_R}\le K$. ∎

### [P1-P2] Fattori in 𝔅 — prova scritta
Siano $\Omega$ un rettangolo limitato, $P=c\prod_jQ_j$ come in C12-T1 e $u\in\mathfrak B(\Omega)\cap\ker P$.
(a) (caso comassimale) Se $V(Q_i)\cap V(Q_j)=\emptyset$ per $i\ne j$, le componenti $u_j=E_j(\partial)u$ (C12-P1(b)) stanno in $\mathfrak B$.
(b) L'ambiguità $\mathcal N$ è fatta di EP, quindi sta in $\mathfrak B$: se **una** scomposizione sta in 𝔅, ci stanno **tutte**.
(c) (fattori di grado 1 in $\tau$) Sia $P=\prod_{j=1}^k(\tau-a_j(\xi))$ con $a_j$ distinti. Allora ogni scomposizione $u=\sum_ju_j$ con $u_j\in\ker_{\mathcal D'}(\tau-a_j)$ ha $u_j\in\mathfrak B(\Omega)$; quindi $\mathcal E^{fatt}_{\mathfrak B}=0$ (P1-D2).
**Prova.** (a) 𝔅 è chiusa per $\partial_t,\partial_x$ (P1-L1(a)). (b) C12-T1(ii) e P1-L1(c).
(c) Per (b) basta una scomposizione, e una scomposizione in $\mathcal D'$ esiste (C12-T1). Per la formula di Vandermonde (C12-T2(i)), $\Delta(\partial_x)u_j=F_j:=\sum_l\mathrm{adj}(V)_{jl}(\partial_x)\partial_t^lu\in\mathfrak B$.
Se $\Delta$ è costante, $u_j=F_j/\Delta$ e si conclude. Altrimenti P1-L4 dà $w\in\mathfrak B$ con $\Delta(\partial_x)w=F_j$, e $h:=u_j-w$ verifica $\Delta(\partial_x)h=0$ in $\mathcal D'(\Omega)$.
Sia $V_\Delta:=\mathrm{span}\{x^le^{\rho_kx}\}$, con $\rho_k$ le radici di $\Delta$ contate con molteplicità; $\dim V_\Delta=\deg\Delta$, con base $e_1,\dots,e_\delta$. Sul rettangolo $\ker_{\mathcal D'}\Delta(\partial_x)=\mathcal D'(I)\otimes V_\Delta$. Lo si vede fattorizzando $\Delta$ in fattori lineari, usando $\partial_x-\rho=e^{\rho x}\partial_xe^{-\rho x}$ e procedendo per induzione con $\ker\partial_x=\mathcal D'(I)\otimes1$ e con le primitive che commutano con $\partial_t$ di C12-L1. Quindi $h=\sum_mc_m(t)e_m(x)$ con $c_m\in\mathcal D'(I)$.
Inoltre $\gamma:=(\partial_t-a_j(\partial_x))h=-(\partial_t-a_j(\partial_x))w\in\mathfrak B$, e $\gamma\in\ker\Delta(\partial_x)$ perché gli operatori commutano. Le $e_m$ sono linearmente indipendenti su $J$, quindi esistono $\psi_m\in C_c^\infty(J)$ biortogonali alle $e_m$. Allora $\gamma=\sum\gamma_me_m$ con $\gamma_m(t)=\langle\gamma(t),\psi_m\rangle$, e $\|\gamma_m^{(i)}\|_{L^2(I)}\le\|\psi_m\|\,\|\partial_t^i\gamma\|_{L^2(\Omega)}\le C\rho^i$.
$V_\Delta$ è invariante per $\partial_x$: $a_j(\partial_x)e_{m'}=\sum_mM_{mm'}e_m$. Allora $c'-Mc=\gamma$ in $\mathcal D'(I)^\delta$, e $\hat c:=e^{-(t-t_0)M}c$ ha derivata $\hat c'=e^{-(t-t_0)M}\gamma$, che è liscia. Quindi $c(t)=e^{(t-t_0)M}c_*+\int_{t_0}^te^{(t-s)M}\gamma(s)ds$. Da $c^{(i)}=M^ic+\sum_{p<i}M^{i-1-p}\gamma^{(p)}$ segue $\|c^{(i)}\|_{L^2(I)}\le C'(2\max(1,\|M\|,\rho))^i$.
Con $\|\partial_x^je_m\|_{L^2(J)}\le C\rho_V^j$ (P1-L1(c)) si ottiene $h\in\mathfrak B$, e quindi $u_j=w+h\in\mathfrak B$. ∎
*Caso generale* (fattori di grado ≥ 2 in $\tau$, non comassimali): l'esistenza di una scomposizione in 𝔅 è **APERTA** (P1-Q2). Due vie possibili: il principio fondamentale di Ehrenpreis negli spazi di funzioni intere di tipo esponenziale (CON-FONTE da verificare), oppure l'algoritmo C12-A1 con le stime di P1-L4.

## E. Fattori del 2° ordine (P1-P4)
### [P1-P4] Propagatore, forma di Gauss e tempo uniforme nella classe 𝔅 — prova scritta, SymPy C6
**Ipotesi.**
- $Q=\tau^2+b(\xi)\tau+c(\xi)$ con $b,c\in\mathbb C[\xi]$.
- $u\in\mathfrak B_\rho(\Omega)$ con $Q(\partial)u=0$; $\rho'>\rho$; $U:=(u,\partial_tu)$.
- $C(\xi)=\begin{psmallmatrix}0&1\\-c&-b\end{psmallmatrix}$.
- $\varphi_1,\varphi_2$ è il sistema fondamentale canonico di $\varphi''+b(\zeta)\varphi'+c(\zeta)\varphi=0$ ($\varphi_1(0)=1$, $\varphi_1'(0)=0$, $\varphi_2(0)=0$, $\varphi_2'(0)=1$); sono funzioni intere di $(t,\zeta)$.
- $K(\rho'):=\max(1,|b|(\rho')+|c|(\rho'))$.
**Tesi.**
(a) $U(t)=e^{(t-t_0)C(\partial_x)}U(t_0)$ in $B_{\rho'}(J)^2$, e $e^{tC(\partial_x)}=\begin{psmallmatrix}\varphi_1&\varphi_2\\\varphi_1'&\varphi_2'\end{psmallmatrix}(t;\partial_x)$, dove le funzioni intere di $\partial_x$ sono definite per serie.
(b) Sia $\mathcal C$ la sottoalgebra chiusa (commutativa) di $\mathcal L(B_{\rho'})$ generata da $I$ e $\partial_x$. Se $f$ è intera e non ha zeri su $\{|\zeta|\le\rho'\}$, allora $f(\partial_x)$ è invertibile in $\mathcal C$.
(c) Sia $T^*(\rho'):=\sup\{T:\varphi_1(t;\zeta)\ne0\ \forall|t|\le T,|\zeta|\le\rho'\}$. Allora $T^*(\rho')\ge\log2/K(\rho')>0$, e per $|t|<T^*$ vale in $\mathrm{Mat}_2(\mathcal C)$ la fattorizzazione di Gauss
$$e^{tC(\partial_x)}=\begin{pmatrix}1&0\\\varphi_1'/\varphi_1&1\end{pmatrix}\begin{pmatrix}\varphi_1&0\\0&e^{-tb}/\varphi_1\end{pmatrix}\begin{pmatrix}1&\varphi_2/\varphi_1\\0&1\end{pmatrix}(t;\partial_x).$$
È la forma di Wei–Norman $e^{g_{21}E_{21}}e^{h_1E_{11}+h_2E_{22}}e^{g_{12}E_{12}}$ con 4 "simboli" $g_{21},h_1,h_2,g_{12}\in\mathcal C$; qui $h_1$ è un ramo di $\log\varphi_1$ continuo in $t$ e olomorfo sul disco. Questo è $E^{mult}_{int}$ per un fattore del 2° ordine: una forma chiusa con 4 funzioni di $\zeta$ (gl₂), **valida uniformemente su $|t-t_0|<T^*(\rho')$**.
(d) Per l'onda ($b=0$, $c=-\zeta^2$) si ha $\varphi_1=\cosh(\zeta t)$ e $T^*(\rho')=\pi/(2\rho')$ esattamente.
**Prova.** (a) $Q(\partial)u=0\iff\partial_tU=C(\partial_x)U$ (II-L1). Si applicano P1-L1(d) a $u$ e a $\partial_tu\in\mathfrak B_\rho$, poi P1-L3(c). L'identità $e^{tC(\zeta)}=\begin{psmallmatrix}\varphi_1&\varphi_2\\\varphi_1'&\varphi_2'\end{psmallmatrix}$ è un'identità di serie di potenze in $(t,\zeta)$ (II-T7(a)). Sia $|C|$ la matrice dei polinomi con i coefficienti presi in modulo: la serie $\sum_k|t|^k|C|(\rho')^k/k!$ converge, quindi si può sostituire $\zeta\mapsto\partial_x$ termine a termine ($\|\partial_x\|\le\rho'$).
(b) Il raggio spettrale non supera la norma, quindi $\sigma_{\mathcal C}(\partial_x)\subset\{|\zeta|\le\rho'\}$. $1/f$ è olomorfa in un intorno del disco. In un'algebra di Banach commutativa il calcolo funzionale olomorfo è un omomorfismo, e per le funzioni intere coincide con la serie di potenze (Rudin, *Functional Analysis*, Thm 10.27, numerazione da verificare). Quindi $(1/f)(\partial)f(\partial)=I$.
(c) $|\varphi_1-1|\le\|e^{tC(\zeta)}-I\|_\infty\le e^{|t|\|C(\zeta)\|_\infty}-1$ (norma di riga massima, che è submoltiplicativa), e $\|C(\zeta)\|_\infty=\max(1,|b(\zeta)|+|c(\zeta)|)\le K(\rho')$. Per $|t|<\log2/K$ si ha $|\varphi_1-1|<1$, quindi $\varphi_1\ne0$. Per $|t|<T^*$, $\varphi_1(t;\partial)$ è invertibile per (b). Su un anello commutativo la fattorizzazione 2×2 richiede solo l'invertibilità di $\varphi_1$, e il determinante è $e^{-tb}$ (Liouville). Per il logaritmo: per $T<T^*$ l'insieme $\{|t|\le T\}\times\{|\zeta|\le\rho'\}$ è semplicemente connesso e $\varphi_1$ non vi si annulla, quindi esiste un ramo continuo con $h_1(0,\cdot)=0$, olomorfo in $\zeta$.
(d) $\cosh w=0\iff w\in i(\pi/2+\pi\mathbb Z)$, quindi $|t|=|\pi/2+\pi n|/|\zeta|\ge\pi/(2\rho')$, con uguaglianza in $\zeta=i\rho'$. ∎
*Lettura (risponde al punto 3 dell'AVVISO corretto di S-II).* Su ℝ i modi di Fourier $\zeta=i\kappa$ sono illimitati e non esiste un $T$ uniforme (II-T7: per l'onda $t^*=\pi/(2|\kappa|)$). In 𝔅 i modi stanno nel disco $|\zeta|\le\rho$, e per $T<\log2/K$ vale $\inf_{|t|\le T,|\zeta|\le\rho}|\varphi_1|\ge2-e^{TK}>0$: la stima uniforme richiesta da S-II esiste, con costante esplicita. SymPy C6 verifica $\cosh$ e i suoi zeri, e confronta il bound con il $t^*$ esatto di KG ($m=2$, $\zeta=0,1,3/2$).

## F. Bordo (P1-P6)
### [P1-P6] Il bordo crea un $E^{mult}$ di ordine 1 — prova scritta (+ CON-FONTE per i generatori standard), SymPy C10
**Ipotesi.**
- $X=L^2(0,L)$ e $c,D>0$.
- $A_1=D\partial^2$ con $D(A_1)=H^2\cap H^1_0$ (Dirichlet) genera $S_1$.
- $A_2=-c\partial$ con $D(A_2)=\{f\in H^1:f(0)=0\}$ (inflow) genera $S_2(t)f(x)=f(x-ct)1_{x>ct}$.
- $A=D\partial^2-c\partial$ con $D(A)=H^2\cap H^1_0$ (AD con Dirichlet) genera $S$.
**Tesi.**
(a) $S_2(t)=0$ per $t\ge L/c$.
(b) $S(t)$ è iniettivo per ogni $t\ge0$.
(c) Per $t\ge L/c$ si ha $S_1(t)S_2(t)=S_2(t)S_1(t)=0$. Quindi $E^{mult}(t)=S(t)-S_1(t)S_2(t)=S(t)$: l'errore relativo è **1** per ogni dato $f\ne0$, e la forma invertibile $\mathfrak E^{mult}$ non esiste.
(d) Senza bordo (classe 𝔅, P1-T2) si ha $E^{mult}\equiv0$. Il $E^{mult}$ di (c) è quindi creato interamente dalle condizioni al bordo: queste appartengono alla somma $A$ e non si distribuiscono sui termini (la condizione di Dirichlet in $x=L$ non si può imporre al trasporto, che è del 1° ordine).
**Prova.** $A_1$ è autoaggiunto e $\le0$, quindi genera un semigruppo di contrazioni (Lumer–Phillips, o teorema spettrale; CON-FONTE standard).
Per $A_2$: per $\lambda>0$, $R(\lambda)f=\frac1c\int_0^xe^{-\lambda(x-y)/c}f(y)dy$ risolve $\lambda u+cu'=f$, $u(0)=0$ (SymPy C10b), e $\|R(\lambda)\|\le1/\lambda$ per la disuguaglianza di Young ($\|e^{-\lambda z/c}1_{z>0}\|_{L^1}=c/\lambda$). Inoltre $\int_0^\infty e^{-\lambda t}f(x-ct)1_{x>ct}dt=R(\lambda)f(x)$ (sostituzione $y=x-ct$). Per Hille–Yosida e l'unicità della trasformata di Laplace, il semigruppo di traslazione nilpotente ha generatore $A_2$. Da qui segue (a).
(b) La moltiplicazione $M:f\mapsto e^{-cx/(2D)}f$ è limitata e invertibile su $X$ e su $H^2\cap H^1_0$, e $MAM^{-1}=B:=D\partial^2-c^2/(4D)$ con lo stesso dominio (SymPy C10a). $B$ è autoaggiunto, con base $\sin(k\pi x/L)$ e autovalori $\mu_k<0$; quindi $e^{tB}=\sum e^{t\mu_k}\langle\cdot,e_k\rangle e_k$ è iniettivo, e lo è anche $S(t)=M^{-1}e^{tB}M$.
(c) Segue da (a) e (b). (d) P1-T2(ii). ∎
*Quadro.* Su $\Omega$ limitato agiscono quattro meccanismi distinti, tutti legati al bordo o al dominio:
1. le condizioni al bordo rendono i termini non commutanti, e $E^{mult}=O(1)$ (P1-P6);
2. i modi esponenziali reali rendono $E^{add}$ non continuo in $H^m$ (P1-P1(e));
3. l'angolo crea un'ostruzione di regolarità tra fattori (C12-C1);
4. la faccia stazionaria del poligono crea uno strato limite, con $E^{ker}$ per termini $\ne0$ (TROP-7, C12-P9, P1-E1).
L'elemento di matrice al 1° ordine di PR-C2d (P3.2) resta a S-P3.

## G. Risolubile (P1-T4) — priorità bassa (in larga parte classico)
### [P1-T4] Algebra finita risolubile ⇒ $E^{mult}$ esatto e globale con $d=\dim\mathfrak g$ funzioni intere — prova scritta + CON-FONTE, SymPy C7
**Ipotesi.** $\dim\mathfrak g=d<\infty$ e $\mathfrak g$ è risolubile.
**Tesi.**
(a) Esiste una base $X_1,\dots,X_d$ di $\mathfrak g$ tale che gli spazi $\mathfrak i_k:=\mathrm{span}\{X_k,\dots,X_d\}$ sono ideali (teorema di Lie; Humphreys, *Introduction to Lie Algebras and Representation Theory*, §4.1, Cor. A, numerazione da verificare — CON-FONTE).
(b) Per ogni $A=\sum_lc_lX_l\in\mathfrak g$ esistono funzioni **intere** $g_1,\dots,g_d$ con $g_i(0)=0$, ottenute con $d$ quadrature esplicite, tali che $e^{tA}=\prod_{i=1}^de^{g_i(t)X_i}$ in $\mathcal A[[t]]$.
(c) Quindi $\mathfrak E^{mult}(t)=\big(\prod_ne^{t\lambda_nT_n}\big)^{-1}e^{tA}=\prod_{n=N}^{1}e^{-t\lambda_nT_n}\prod_ie^{g_i(t)X_i}$: una forma chiusa con $d$ funzioni scalari intere.
(d) Se $\mathcal A$ agisce con operatori limitati su uno spazio di Banach $V$ (matrici modo per modo, oppure un sottospazio invariante di dimensione finita, come $\mathbb C[x]_{\le n}$ per OU), l'identità vale come identità di funzioni intere di $t\in\mathbb C$ a valori in $\mathcal L(V)$.
**Prova.** (b) $\mathrm{ad}_{X_j}$ preserva $\mathfrak i_k$ e induce sul quoziente $\mathfrak i_k/\mathfrak i_{k+1}$, che ha dimensione 1, la moltiplicazione per uno scalare $\lambda_{jk}$. Quindi $\mathrm{Ad}(e^{gX_j})X_k=e^{g\lambda_{jk}}X_k\bmod\mathfrak i_{k+1}$. Per P1-L5(b), $\mathrm{Ad}(e^{gX_j})|_{\mathfrak g}=e^{g\,\mathrm{ad}X_j}$ è una matrice di funzioni intere di $g$. Ne segue $\mathrm{Ad}(P_{i-1})X_i=\sum_{l\ge i}M_{il}X_l$, dove le $M_{il}$ sono funzioni intere di $g_1,\dots,g_{i-1}$ e $M_{ii}=\exp(\sum_{j<i}\lambda_{ji}g_j)\ne0$.
Il sistema di Wei–Norman $\sum_{i\le l}g_i'M_{il}=c_l$ è triangolare. Si ha $g_1=c_1t$; per $l\ge2$, $g_l'=M_{ll}^{-1}(c_l-\sum_{i<l}g_i'M_{il})$ ha secondo membro intero in $t$ e dipendente solo da $g_1,\dots,g_{l-1}$, quindi $g_l$ si ottiene per quadratura ed è intera.
Con queste $g$, P1-L5(d) dà $U'U^{-1}=A$, e P1-L5(c) dà $U=e^{tA}$. (La serie di Taylor di una composizione di funzioni intere coincide con la composizione formale.)
(d) I due membri sono funzioni intere a valori operatori con la stessa serie di Taylor. ∎
*Esempi.*
- OU: $X_1=x\partial$, $X_2=\partial^2$, $[X_1,X_2]=-2X_2$, $A=-X_1+X_2$. Si trova $g_1=-t$, $g_2=(1-e^{-2t})/2$, cioè $e^{t(\partial^2-x\partial)}=e^{-tx\partial}e^{g_2\partial^2}$. SymPy C7a lo verifica su $x^n$, $n\le6$; il risultato è coerente con R5-P6.
- $\partial^2+x$: $\mathrm{span}\{\partial^2,x,\partial,1\}$ è nilpotente (R5-P5).
