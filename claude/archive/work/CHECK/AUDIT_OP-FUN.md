# AUDIT — OP-FUN (S-CHECK-14, revisore indipendente) · 26/10/2026

**Oggetto:** `work/OP-FUN/CHECK_REQUEST.md` (8 claim in ordine di priorità). Le prove sono in `work/OP-FUN/PROOF_PACKAGE.md` §2–§6, che la CHECK_REQUEST indica come "testo completo delle prove"; le ho lette per i claim auditati. Riferimenti puntuali esterni, dichiarati: `work/P1/PROOF_PACKAGE.md` [P1-L1], [P1-L4] (enunciato e prova, per il punto (a) di OPF-L1); `work/C1C2/PROOF_PACKAGE.md` [C12-C1] (per controllare "ogni m" in OPF-P5(ii)).
**Skill caricate** (lettura integrale dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol, skills-local/claim-lifecycle, proof-checker (enunciati canonici, micro-claim, checklist A–H, red team 1.5, severità a due assi, acceptance gate; il revisore sono io, niente Codex), kill-argument (revisori = subagenti Claude freschi, tabella dei verdetti), sympy.
**Fatti presi come dati** (LEDGER, DIMOSTRATO): C12-T1, C12-T1′, C12-L2, C12-L3(a), C12-T3, C12-C1, C12-P10, P1-L1…L4, P1-T2, P1-P2(c) [P2-1], P1-P4, P2-T3, P2-C2(b),(e), II-L1. Le CON-FONTE (Runge, de Rham, Malgrange–Ehrenpreis / P-convessità, suriettività degli ellittici, densità di $C^\infty(\bar\Omega)$) non sono auditate. Ho controllato solo dove vengono usate e con quali ipotesi.
**SymPy (red team, scritto da zero):** `work/CHECK/sympy/audit_opfun.py` → `audit_opfun.out`, **55/55 OK**. Il primo run dava 54/55: il test dell'involuzione pesata falliva per un limite di `simplify` su funzioni generiche. Rifatto con tre $w$ espliciti: OK.
**Kill-argument** su OPF-T4 e OPF-T5 (§10).

## 0. Sintesi dei verdetti
| claim | verdetto | severità massima | stato proposto |
|---|---|---|---|
| OPF-L1 | PASS | — | DIMOSTRATO |
| OPF-T1 | PASS | — | DIMOSTRATO |
| OPF-L2 | PASS | — | DIMOSTRATO |
| OPF-T2 | PASS-con-fix(T2-1) | MINOR | DIMOSTRATO |
| OPF-P3 | PASS-con-fix(P3-1, P3-2) | MINOR | DIMOSTRATO |
| OPF-P4 | PASS-con-fix(P4-1, P4-2) | MINOR | DIMOSTRATO; (b)(i) usa Runge, CON-FONTE |
| OPF-C1 | PASS-con-fix(C1-1) | MINOR | DIMOSTRATO |
| OPF-L3 | PASS | — | DIMOSTRATO (la densità di $C^\infty(\bar\Omega)$ resta CON-FONTE) |
| OPF-T5 (+ Cor. (a),(b)) | PASS-con-fix(T5-1, T5-2, T5-3); KA **WARN** | MINOR | DIMOSTRATO (Cor. (b) solo su rettangoli con lati paralleli agli assi) |
| OPF-P5 (+ estensione) | PASS | — | DIMOSTRATO |
| OPF-O1 | PASS-con-fix(O1-1) | MINOR | DIMOSTRATO (enunciato non pesato); estensione pesata verificata qui |
| OPF-T4 | PASS-con-fix(T4-1, T4-2); KA **PASS** | MINOR | DIMOSTRATO (i),(ii), limite e (iv)(a),(b),(e); (iii),(iv)(c),(d) DIMOSTRATO modulo CON-FONTE |
| OPF-P6 | PASS-con-fix(P6-1) | MINOR | DIMOSTRATO |
| OPF-P7 | PASS | — | DIMOSTRATO |
| S5-L2 | PASS-con-fix(**S5L2-1**) | CRITICAL locale, limitato a (v) | DIMOSTRATO (i)–(iv) e (v) corretta; (v) com'è scritta: FALSO in generale |

Acceptance gate: 0 FATAL. Una CRITICAL, S5L2-1, tocca solo la frase di portata (v) di S5-L2. È INVALID+LOCAL: il controesempio è verificato, nessun altro claim ne dipende. Il fix WEAKEN_CLAIM è scritto in §9 e la chiude. Tutte le altre lacune sono MINOR. Le ipotesi sono esplicite e i controesempi sono stati tentati su ogni lemma chiave.

---
## 1. OPF-L1 + OPF-T1 (esistenza della scomposizione in 𝔅 per ogni P)
**Enunciato canonico (T1).** ∀ Ω = I×J rettangolo aperto limitato, ∀ P = c∏_{j=1}^sQ_j ∈ R∖ℂ, ∀ u ∈ 𝔅(Ω) con P(∂)u = 0, ∀ (u_j) con u_j ∈ ker_{𝒟′(Ω)}Q_j e Σu_j = u: u_j ∈ 𝔅(Ω) per ogni j. Le componenti esistono per C12-T1(i).

| passo | contenuto | esito |
|---|---|---|
| T1-a | $r\in(Q_j,B_j)\cap\mathbb C[\xi]\setminus0$ e $\sigma\in(Q_j,B_j)\cap\mathbb C[\tau]\setminus0$ | OK. C12-L3(a): per $f,g$ coprimi $V(f,g)$ è finito, anche vuoto, ed entrambe le eliminanti sono non nulle. Se $Q_j,B_j\in\mathbb C[\xi]$ allora $1\in$ ideale. SymPy: 6 coppie (trave, calore×trasporto, $\xi\tau-1$, molteplicità, KG, non monico × $(\tau-1)^3$) e i certificati espliciti del package. |
| T1-b | $r(\partial_x)u_j=B(\partial)B_j(\partial)u$ | OK. $B_ju_i=0$ per $i\ne j$ perché $Q_i\mid B_j$. Composizione di operatori a coefficienti costanti in $\mathcal D'$. |
| T1-c | $F,G\in\mathfrak B_\rho$ | OK. P1-L1(a): $\|\partial\|\le\rho$ su $\mathfrak B_\rho$. |
| L1 passo 1 | P1-L4 in $x$, struttura di $\ker_{\mathcal D'}r(\partial_x)=\mathcal D'(I)\otimes V_r$ | OK (dati DIMOSTRATI). |
| L1 passo 2 | accoppiamento con $\chi\otimes\psi_m$, $\sigma(\partial_t)c_m=\gamma_m$, stima di Cauchy–Schwarz | OK. $\langle c\otimes e,\chi\otimes\psi\rangle=\langle c,\chi\rangle\int e\psi$; $\gamma\in\mathfrak B_{R'}$ per P1-L1(a),(b). |
| L1 passo 3 (punto (a)) | P1-L4 a ruoli scambiati; la primitiva non dipende da $x$ | OK. Ho riletto P1-L4 (work/P1 §[P1-L4]): $w=\int_{x_0}^xG(x-y)F(t,y)dy$, e definizione e stime sono simmetriche in $(t,x)$ sul rettangolo. Scambiando i ruoli, $\tilde w=\int_{t_*}^tG_\sigma(t-t')\gamma_m(t')dt'$ ha integrando indipendente da $x$. SymPy: $\sigma=\tau^2+1$. |
| L1 passo 3 (punto (b)) | $\ker_{\mathcal D'(I)}\sigma(\partial_t)$ = EP con stime $B$ | OK. Le soluzioni distribuzionali di un'ODE a coefficienti costanti sono classiche (C12-L2(iii)). $\|(t^le^{\mu t})^{(i)}\|\le C\eta^i$ per $\eta>|\mu|$: le derivate valgono $\sum\binom ik\mu^{i-k}(t^l)^{(k)}e^{\mu t}$ e il polinomio in $i$ è assorbito. SymPy: il rapporto con $2^i$ decresce, $\mu=3/2$. |
| L1 passo 4 (punto (c)) | somma finita di prodotti tensoriali | OK. $\delta$ addendi, ciascuno $\le C R_1^i\rho_V^j$, quindi $\mathfrak B_{\max(R_1,\rho_V)}$, con $C^\infty$ dato da $c_m$ liscia. |
| T1-d | ambiguità $\mathcal N$ ⊂ EP ⊂ 𝔅 | OK. C12-T1(ii) e P1-L1(c). |

Red team: nessun controesempio. Il controllo più forte è C12-C1: lì la stessa coppia di ODE non basta in $H^m$. In 𝔅 le stime uniformi in tutti gli ordini evitano il problema. L'osservazione del package è corretta.
**Verdetto: OPF-L1 PASS, OPF-T1 PASS → DIMOSTRATO.**

## 2. OPF-L2 + OPF-T2 (molteplicità)
- L2: P1-L1(d) dà $v,g\in C(\bar I;B_{\rho'})$. Il test su $\varphi\otimes\psi$ basta, perché un elemento di $B_{\rho'}\subset L^2(J)$ è determinato dai $\psi\in C_c^\infty$. La derivata a valori in Banach è $Av+g$. $\partial_x$ è limitato su $B_{\rho'}$, quindi $e^{sA}$ è definito per serie e vale la regola del prodotto in un'algebra di Banach. **OK.**
- T2(i): l'induzione discendente torna, perché $\int_{t_0}^t\frac{(\theta-t_0)^{i-k-1}}{(i-k-1)!}d\theta=\frac{s^{i-k}}{(i-k)!}$. SymPy: $(\partial_t-a)^3u=0$ e $(\partial_t-a)^2u\ne0$ per $e=3$. **OK.**
- T2(ii),(iii): $a_nI$ e $N_e$ commutano. Si sviluppa $\prod(I+(e^{sT}-I))$. SymPy: identità della somma sui sottoinsiemi con $a_1I,a_2I,N_3$; $E^{mult}=0$; componente 0. **OK.**
- **T2-1 (MINOR, UNCLEAR+LOCAL, WEAKEN/chiarire):** $E^{add}$ di (iii) è definito sul getto di Jordan $F$, con $e$ funzioni, e i "termini" includono $N_e$. Per $e\ge2$ la definizione scalare P1-D3(b) ("flussi dei termini col dato $u(t_0)$") **non** è definita in 𝔅, perché $u(t_0)$ non determina $u$. La componente 0 di (iii) è quindi una definizione nuova e non un'estensione di P1-D3(b). La "Lettura" del package lo dice in parte. Va scritto nell'enunciato: "$E^{add}$ nel quadro di Jordan (dato $F$)".
**Verdetto: L2 PASS, T2 PASS-con-fix(T2-1) → DIMOSTRATO.**

## 3. OPF-P3 (grado ≥ 2: $E^{mult}\not\equiv0$)
- Commutatori: $[N_0,E_{k,b}]=E_{k-1,b}-E_{k,b+1}$ (verificato su SymPy per $k=3$). I prodotti $E_{k,a}E_{k,b}=\delta_{ak}E_{k,b}$ restano nella riga $k$. L'entrata $(k-1,1)$ riceve contributi solo da $[N_0,T_{0,n}]=-c_{0,n}(\dots)$, e con il fattore $-\frac12$ e l'ordine si ottiene $\frac12\sum\varepsilon_nc_{0,n}$. **OK.**
- $c_0\not\equiv0$: per $Q$ irriducibile con $k\ge2$, se $\tau\mid Q$ allora $Q=\tau$. Con monomi distinti, $\sum\pm c_{0,n}\ne0$. **OK.**
- Il termine $O(s^3)$ vale in norma (esponenziali di operatori limitati). **OK.**
- SymPy: KG, telegrafo e un $k=3$ con 4 termini, **tutti** gli ordinamenti (6, 24, 120): entrata $(k-1,1)=\frac12\sum\varepsilon_nc_{0,n}\ne0$.
- **Red team P3-1 (MINOR, ipotesi essenziale):** con termini non distinti ($c_0=2\xi$ scritto $\xi+\xi$) esistono 2 ordinamenti su 6 in cui **l'intero** coefficiente di $s^2$ è nullo (`audit_opfun.out`). L'ipotesi "monomi distinti" è usata davvero e deve restare nell'enunciato, insieme alla convenzione su $N_0$ già scritta nella Lettura.
- **P3-2 (MINOR, UNCLEAR):** "$E^{mult}_\omega\not\equiv0$" è un enunciato sull'operatore in $\mathcal L(B^k_{\rho'})$, non su ogni dato $U(t_0)$. Aggiungere "come operatore".
**Verdetto: PASS-con-fix(P3-1, P3-2) → DIMOSTRATO.**

## 4. OPF-P4 (non monici)
- (a) $v\in\mathfrak B$: le stime sotto il segno su un compatto valgono. $Q(\partial)v=0$ perché $p_1a-p_0=0$ sul cerchio. $v(t_0)=0$ per Cauchy. Il residuo non nullo regge: $\gcd(p_0,p_1)=1$ dà $p_0(\zeta_0)\ne0$, quindi un polo di ordine esatto $\mu$ e $\alpha_\mu\ne0$, e il coefficiente di $x^{\mu-1}e^{\zeta_0x}$ è non nullo. Il disco chiuso deve contenere solo $\zeta_0$ fra gli zeri di $p_1$, come richiesto. SymPy: serie di Bessel (equazione, $v(0)=0$, $\partial_tv(0)=1$), contorno = serie a $10^{-15}$; caso $\mu=2$ ($p_1=\xi^2$, $p_0=1+\xi$): residuo $1+x$ e $v(t_0)=0$ numerico. **OK.**
- (b)(i) Runge: la versione polinomiale serve su $\hat K$, che ha complementare connesso, con $h$ olomorfa su un intorno. Le ipotesi sono scritte correttamente. La stima $\|h-q_m\|_K e^{X\max|\zeta|}|\mu|(K)$ è corretta e l'indipendenza dalla misura segue. **OK modulo CON-FONTE (Rudin RCA cap. 13).** SymPy: approssimazione esplicita di $1/\zeta$ su $|\zeta-3|\le1$.
- (ii),(iii): $a$ è olomorfa vicino a $\hat K$, perché $Z(p_1)$ è finito e disgiunto dal compatto. Unicità nella classe e omomorfismo: **OK.** La classe non è vuota (red team suggerito): gli EP con esponente in $K$ (misura di Dirac) ci stanno. SymPy: $e^{3x+t/3}$.
- **P4-1 (MINOR, OVERSTATED+LOCAL, WEAKEN):** (iv) mostra che la condizione su $\hat K$ **non si può togliere**: esiste un $K$, cioè $\gamma_\varepsilon$, per cui fallisce. Non mostra che sia necessaria per ogni $K$. Correggere "necessità" in "non rimovibilità".
- **P4-2 (MINOR, UNJUSTIFIED+COSMETIC):** la frase "gli operatori $e^{sa_n(\partial_x)}$ con $a_n$ razionale non sono definiti per serie su $B_\rho$" è informale. Va tolta o sostituita con "la serie in $\partial_x$ non ha senso perché $a_n$ non è intera". La conclusione in 𝔅 poggia comunque sulla non unicità (a).
**Verdetto: PASS-con-fix(P4-1, P4-2) → DIMOSTRATO; (b)(i) usa Runge, CON-FONTE.**

## 5. OPF-C1
È una combinazione corretta di T1, T2, P3 e P4. **C1-1 (MINOR, ADD_DERIVATION):** C1 dice "monico irriducibile di grado ≥ 2 in τ (**anche con potenza**)", ma P3 è enunciato per $Q$ irriducibile. La prova di P3(b) usa solo $\tau\nmid Q$ e $k\ge2$, che valgono per $Q^e$: SymPy, $c_0(Q^2)=\xi^2$ per $Q=\tau^2-\xi$. Va aggiunta una riga a P3: "vale per ogni $Q$ monico con $\deg_\tau\ge2$ e $\tau\nmid Q$, in particolare per le potenze". **PASS-con-fix(C1-1) → DIMOSTRATO.**

## 6. OPF-L3 + OPF-T5 (densità per simmetrie contraenti)
- L3: il cambio di variabili $\|g\circ\Phi\|^2_{L^2(\Omega)}=|\det A|^{-1}\|g\|^2_{L^2(\Phi\Omega)}$ è corretto, e i polinomi $p_{\alpha\beta}(A)$ sono limitati vicino a $I$. La densità di $C^\infty(\bar\Omega)$ (CON-FONTE, Adams–Fournier, proprietà del segmento per i lipschitziani) e la continuità uniforme danno la convergenza. Uso implicito: $\Phi_\lambda(\bar\Omega)\subseteq\bar\Omega$, che segue da $\Phi_\lambda(\Omega)\subseteq\Omega$ per continuità. **OK** (punto (a)).
- T5(S): $\nabla(w\circ\Phi)=A^{\mathsf T}(\nabla w)\circ\Phi$, quindi $P(\partial)(w\circ\Phi)=(P(A^{\mathsf T}\partial)w)\circ\Phi=\kappa(P(\partial)w)\circ\Phi$: la trasposta è giusta. SymPy: identità di catena per la trave con $w$ generica; (S) per trave, onda e $\tau\xi$.
- Punto (b): mollificazione su $\Omega_\eta$ (convesso), $P(\partial)u_\eta=0$, convergenza $H^m$ su $\overline{\Phi_\lambda\Omega}\Subset\Omega$. $U=\Phi_\lambda^{-1}(\Omega_\eta)\supset\bar\Omega$ perché $\Phi_\lambda(\bar\Omega)\subset\Omega_\eta$ quando $\eta<\delta$. $U$ è convesso, quindi vale C12-T1′ in $C^\infty(U)$. Le componenti sono lisce sul compatto $\bar\Omega\subset U$, quindi sono in $H^m(\Omega)$ con Ω limitato. La disuguaglianza finale è corretta. **OK.**
- Cor. (a): $o+\lambda(\bar\Omega-o)\subset\Omega$ per Ω convesso e $o$ interno. **OK.** Cor. (b): (C) vale coordinata per coordinata sui rettangoli. SymPy: 2000 rettangoli e centri casuali. **OK.**
- **T5-1 (MINOR, OVERSTATED+LOCAL, WEAKEN; dal KA):** l'"Esito P2-Q1" dice "per ogni $P$ (quasi) omogeneo: nessuna somma è chiusa senza essere densa" senza dominio. Va scritto: "$P$ omogeneo su ogni convesso limitato; $P$ quasi omogeneo (pesi diversi) su rettangoli con lati paralleli agli assi; altri domini aperti". Verificato in SymPy: la trave sul parallelogramma caratteristico $\{0<t<L,\ t<x<t+1\}$ con $L=2$ non ha alcun centro per cui valga (C) ($\lambda=0.99$). Con $L=0.5$ il centro esiste. L'onda soddisfa (C) sullo stesso parallelogramma.
- **T5-2 (MINOR):** nel Cor. (b) scrivere "rettangolo con lati paralleli agli assi $t$, $x$".
- **T5-3 (MINOR, COSMETIC):** "calore, Airy" come $P$ con un solo fattore sono banali ($s=1$). Scrivere "prodotti di almeno due fattori quasi omogenei con gli stessi pesi". Esempi: la trave $(\tau-i\xi^2)(\tau+i\xi^2)$, oppure $(\tau-\xi^2)(\tau+\xi^2)$. Non vale per calore × Airy, che ha pesi (2,1) e (3,1). Il caso non banale elencato è la trave.
**Verdetto: L3 PASS; T5 PASS-con-fix(T5-1, T5-2, T5-3) → DIMOSTRATO.**

## 7. OPF-P5 (trasporti paralleli, ogni m) + OPF-O1
- Punto (c), regolarità: la corda fissa $[\alpha,\beta]$ uniforme in un intorno $N$ di $s_0$ esiste, perché gli estremi della corda sono continui. $\partial_s=\partial_x$ nelle coordinate originali, quindi $\partial_s^ku\in L^2$ per $k\le m$. Cauchy–Schwarz dà $F,G\in H^m_{loc}(S)$. **OK.**
- $\Psi_\lambda(\Omega')\subseteq\Omega'$: $1+\lambda(t-1)-t=(1-t)(1-\lambda)$ (identità SymPy) e $1+\lambda t<1+t$; verificato anche su 20000 punti. Conserva i nuclei, perché $\Psi$ fissa $t$. $\sigma_\lambda([0,2])\Subset S$, quindi $F_\lambda,G_\lambda\in H^m(0,2)$, e $F_\lambda$, $e^tG_\lambda$ stanno in $H^m(\Omega')$ (Fubini sulle corde, di lunghezza ≤ 1). In coordinate originali $\Psi_\lambda$ è affine con $A\to I$, quindi OPF-L3 si applica: Ω′ è un parallelogramma, lipschitziano. **OK.**
- (ii): C12-C1 vale **per ogni** $m\in\mathbb N$. Ho controllato l'enunciato in work/C1C2 §[C12-C1]: $G_m=s^{m-1}\log s$. Il LEDGER dice "m=0..4" solo per la verifica SymPy. $\mathcal I=0$ perché $f-g=1$. P2-T3(b) dà $c_F=1$. **OK.**
- Estensione con corde annidate: verificata per i rettangoli con $L\ge cT$ (annidate verso $s_*\in[0,L-cT]$). Per $L<cT$ non esiste alcun $s_*$ (SymPy). **OK.**
- O1 come enunciato (mappe lineari, senza peso): la prova è corretta. I fattori di grado diverso non si scambiano, e $r=q=0$, $p=u^2=u$ danno $A=I$. **OK.**
- **O1-1 (MINOR, dal KA, ADD_DERIVATION):** l'attaccante osserva che anche le simmetrie affini **pesate** $w\mapsto e^{a\cdot y}w\circ\Phi$ sono utilizzabili, e che per $(\tau-\xi^2)(\tau+\xi)$ ne esiste una non banale: $v=e^{t-x}w(t,2t-x)$. È vero (SymPy, tre $w$ espliciti). Ho però risolto in generale $P(A^{\mathsf T}z+a)\sim P(z)$ fattore per fattore (`audit_opfun.out`, `sp.solve`): le **sole** soluzioni sono l'identità e quell'involuzione (det −1). Non esiste alcuna famiglia che tenda all'identità, quindi l'ostruzione al metodo resta vera anche nel caso pesato. Va aggiunto questo lemma al package. Nel frattempo "ostruzione dimostrata" vale "per simmetrie affini, anche pesate (verifica S-CHECK-14)". OPF-Q1 resta APERTO.
**Verdetto: P5 PASS → DIMOSTRATO; O1 PASS-con-fix(O1-1) → DIMOSTRATO.**

## 8. OPF-T4 (criterio coomologico, C12-Q6)
**Enunciato canonico.** ∀ Ω ⊂ ℝ² aperto connesso non vuoto, ∀ 𝒜 ∈ {𝒟′, C^∞}, ∀ P: coker Σ_Ω ≅ ker[ι: H¹(Ω;ℂ)⊗𝒩 → ⊕_jH¹(Ω;𝒦_j)] (H¹ = coomologia dei fasci); dim coker ≤ δ(P)·b₁(Ω) in ℕ∪{∞}.

| punto | contenuto | esito |
|---|---|---|
| (a) costanza globale del fascio nucleo | C12-T1′(ii) sui dischi: $\ker\Sigma_U=\mathcal N|_U$, con restrizione iniettiva (EP analitici). La sezione è localmente costante, quindi costante sui connessi: è il fascio costante (sezioni = funzioni localmente costanti). Esattezza a destra sui germi per C12-T1′(i) | OK |
| (b) $H^0$ | $H^0(\mathcal K_j)=\ker_{\mathcal A(\Omega)}Q_j$ ($\mathcal D'$ e $C^\infty$ sono fasci); $H^0(\underline{\mathcal N})=\mathcal N$ per Ω connesso | OK |
| (ii) | successione esatta lunga, coker = im ∂ = ker ι. $H^1(\underline{\mathcal N})\cong H^1(\Omega;\mathbb C)\otimes\mathcal N$ (dim 𝒩 finita, additività). Il limite vale anche per $b_1=\infty$ (banale). (ii) non usa né de Rham né fonti esterne | OK |
| (c) Čech e segno | $0\to\mathcal K_j\to\mathcal A\to\mathcal A\to0$ esatta per risolubilità locale sui dischi (CON-FONTE); $\mathcal A$ fine. Cociclo $c_{ab}w_j$, sollevamento $\varphi_aw_j$, $g_j$ incollata. Il segno è irrilevante per il nucleo. $\check H^1$ su un ricoprimento si inietta in $H^1$, e qui serve solo calcolare ι su classi rappresentate su un ricoprimento di dischi (de Rham, CON-FONTE) | OK |
| (d) costruzione di $u$ da ker ι | corretta per tensori decomponibili. Per ξ generale manca la scrittura, ma la costruzione è lineare (vedi T4-1) | OK con fix |
| (e) τξ in 𝒟′ su $D^*$ | 𝒩 = ℂ(1,−1), ι = ([θ_t], −[θ_x]). α = atan2(x,t) (taglio {x=0, t<0}) è liscia lungo ogni retta $x=c\ne0$, e β = π/2 + atan2(−t,x) (taglio {t=0, x<0}) lungo ogni $t=c\ne0$: Fubini dà $\partial_t\alpha=\theta_t$, $\partial_x\beta=\theta_x$ in 𝒟′. $u=\beta-\alpha=2\pi\,\mathbf 1_{\{t<0,x<0\}}$, cioè C12-P10(b). Tutto verificato numericamente (3000 punti, salti lungo $x=-0.3$). In $C^\infty$: ι iniettiva per (ii) + C12-P10(c) | OK |
| (f) uso delle CON-FONTE | (i),(ii) e il limite: solo teoria dei fasci standard e C12-T1′. (iii): risolubilità locale e de Rham. (iv)(c),(d): suriettività dei fattori ($\partial_{\bar z}$, $\partial_z$ su ogni aperto, in 𝒟′ e $C^\infty$), più "$b_1=0\iff$ s.c." (Rudin, già CON-FONTE in C12-P10). (iv)(a),(b),(e) non dipendono da fonti oltre (ii) e C12-P10 | OK |
| Laplaciano | SymPy: $\log r^2$ armonica; $Q_1(\vartheta)=1/(it-x)=-i/(t+ix)$ e $Q_2(\log r^2)=2/(t-ix)$ monodrome. δ = 1, $\dim=b_1$: è il teorema della coniugata logaritmica e affina C12-P10(a) | OK (CON-FONTE per la suriettività) |

- **T4-1 (MINOR, ADD_DERIVATION; dal KA, punti P1–P4):** (iii) va riscritto per un ξ = Σ_k[θ_k]⊗n_k qualsiasi in ker ι. Si pone Φ_j := Σ_kφ_kn_{k,j}, dove ogni $Q_j(\partial)(\varphi_kn_{k,j})$ è monodroma. ι(ξ) = 0 dà $Q_j\Phi_j=Q_j\alpha_j$. Con $h_j:=\Phi_j-\alpha_j$ si ha Σ_jh_j = −Σ_jα_j, perché Σ_jn_{k,j} = 0 per ogni k. Le differenze di Čech valgono Σ_kc^k_{ab}n_k, cioè ∂u = ξ, e per esattezza u ∉ im Σ_Ω se ξ ≠ 0. SymPy: identità di somma nulla.
- **T4-2 (MINOR, ADD_REFERENCE):** le CON-FONTE di (iii) e (iv)(c),(d) restano tali finché CIT-AUDIT non le verifica: Hörmander ALPDO II §10.6–10.7, Hörmander SCV 1.4.4, Warner/Bredon, Rudin RCA cap. 13. Va dichiarato che (i), (ii) e il criterio "⟺ ι iniettiva" sono indipendenti da esse.
- Coerenza con C12-P10 e C12-T1′: piena ((iv)(b) = T1′; (iv)(d),(e) = P10(a),(b),(c) con la dimensione).
**Verdetto: PASS-con-fix(T4-1, T4-2) → DIMOSTRATO per (i), (ii), il limite e (iv)(a),(b),(e); (iii) e (iv)(c),(d) DIMOSTRATO modulo le CON-FONTE dichiarate. C12-Q6 → CHIUSO.**

## 9. OPF-P6, OPF-P7, S5-L2
**OPF-P6.**
- (a)⇒(b): la Gram è definita positiva e continua sul compatto delle corde di lunghezza ≥ ℓ₀, quindi $\|\sum\omega_j\|^2\ge(\gamma/B)\sum\|\omega_j\|^2$. Anche $F_j\in L^2(S)$, perché $\Gamma_{jj}\ge\lambda_{\min}$. SymPy: la Gram di 3 esponenziali degenera solo quando ℓ → 0.
- (b)⇒(a): il passaggio da 2 a N fattori usa l'unicità della scomposizione in 𝒟′ con tutti i fattori, e la scomposizione $(e^{d_1t}F,e^{d_2t}G,0,\dots,0)$ ne è una. **OK.**
- **P6-1 (MINOR, REFERENCE_MISMATCH):** C12-T1(iii) è enunciato sul rettangolo, mentre qui Ω è convesso. Va citato C12-T1′(iii), oppure l'argomento diretto, valido su ogni aperto: fattori comassimali, $E_j\in\prod_{i\ne j}(Q_i)$ con $\sum E_j=1$, da cui $u_j=E_j(\partial)\sum_iu_i$.
- **PASS-con-fix(P6-1) → DIMOSTRATO.**

**OPF-P7.**
- $\pi_A$ è limitato su $H^m$ e idempotente; l'immagine è $\ker_{H^m}A(\partial_t)=\sum_{\mathcal T}\ker_{H^m}Q_j$ (base adattata).
- $\pi_A\pi_B=\pi_B\pi_A$ per Fubini. $E=1-(1-\pi_A)(1-\pi_B)$ è idempotente e $\mathrm{im}\,E=X+Y$. Funziona per ogni raggruppamento (sottoprodotti).
- SymPy (numpy): idempotenti obliqui tensoriali, $E^2=E$ e rango $=\dim(\mathrm{im}\,\pi_A+\mathrm{im}\,\pi_B)$.
- **PASS → DIMOSTRATO.** C12-Q2 → PARZIALE (residuo OPF-Q2 APERTO).

**S5-L2.**
- (i), (ii): OK.
- (iii): il lemma della mappa aperta è corretto. $F'$ è un complemento algebrico di $A(X)\cap F$ in $F$; $T:X/\ker A\times F'\to Y$ è biiettiva e limitata, quindi è un isomorfismo, e $A(X)=T(\cdot\times0)$ è chiuso. Direzione "⇐": $V+F=q^{-1}(q(F))$. **OK.**
- (iv): P2-C2(e) si applica a $(\mathcal H_j')$. **OK.**
- **S5L2-1 (CRITICAL locale = INVALID+LOCAL, WEAKEN_CLAIM):** (v) afferma che, se fra le componenti esiste una relazione non generata dalle intersezioni a coppie, allora $\|\mathbf C'\|\ge1$. **In generale è falso.** Controesempio verificato in ℝ³: $\mathcal H_1=\langle e_1,e_3\rangle$, $\mathcal H_2=\langle e_2,e_3\rangle$, $\mathcal H_3=\langle e_1+e_2+2e_3\rangle$. Si ha $F_1=F_2=\langle e_3\rangle$ e $F_3=0$. Le relazioni hanno dimensione 2, quelle generate dalle coppie dimensione 1, eppure $\|\mathbf C'\|=1/\sqrt3<1$. L'errore nella prova: da $\|\mathbf C'\|<1$ segue l'iniettività di Σ su $\oplus\mathcal H_j'$. Le parti $y_j'$ di una relazione sommano però a $-\sum f_j\in F$, che non è zero in generale.
  - L'**esempio** del package ($\tau,\xi,\tau-\xi$ su un rettangolo) è invece corretto. Lì $\Pi_{F_j}$ è la stessa media per tutti i $j$, quindi le parti $y_j'$ sommano a 0 e $\|\mathbf C'\|\ge1$ (SymPy in $H^1$).
  - **Fix:** sostituire (v) con: "se esiste una relazione $(y_j)$, $\sum y_j=0$, le cui parti $y_j-\Pi_{F_j}y_j$ sono non tutte nulle e **sommano a 0**, allora $\|\mathbf C'\|\ge1$ e il criterio tace. Esempio: $\tau,\xi,\tau-\xi$. La sola esistenza di relazioni non a coppie non basta (controesempio in ℝ³)."
  - Nessun claim dipende da (v).
- Tre rette a 120°: $\|\mathbf C\|=1$, OK.
- **PASS-con-fix(S5L2-1) → DIMOSTRATO per (i)–(iv) e per (v) corretta.**

## 10. Kill-argument
- **OPF-T4** (KA_OPFUN_T4_input/attack/adjudication.md): l'attacco è "la costruzione esplicita di (iii) vale solo per tensori puri". L'arbitro classifica 2 punti answered e 4 partially answered, tutti minor, e 0 unresolved: la costruzione è lineare e (i), (ii) e il criterio non dipendono da (iii). **Verdetto: PASS** (defense_survives_with_minor_partial_only) → fix T4-1.
- **OPF-T5** (KA_OPFUN_T5_*): l'attacco ha due rami. Il primo è "Esito senza dominio": la trave sul parallelogramma non soddisfa (C), calcolo corretto, ripetuto in SymPy. Il secondo è "O1 ignora le simmetrie pesate": l'involuzione è vera ma isolata, verificato in SymPy. L'arbitro classifica 3 punti answered, 2 partially (minor) e 1 still_unresolved (minor: la frase dell'Esito). **Verdetto: WARN** (unresolved_major_or_minor) → fix T5-1, T5-2, O1-1. Nessun enunciato risulta falso.

## 11. Fix proposti (riepilogo, da recepire in work/OP-FUN dal proprietario o dal coordinatore)
T2-1, P3-1, P3-2, P4-1, P4-2, C1-1, T5-1, T5-2, T5-3, O1-1, T4-1, T4-2, P6-1, **S5L2-1**: testo nelle sezioni 2–9. Solo S5L2-1 cambia un enunciato (WEAKEN di (v)). Gli altri sono precisazioni, una riga di derivazione o di riferimento.

## 12. Stato dei problemi aperti (proposta)
- P1-Q2 → CHIUSO. Residuo minore: non monici di grado ≥ 2 in τ, scritti solo come combinazione.
- P2-Q1 → CHIUSO per: trasporti paralleli sul quadrato, ogni m, e rettangoli con corde annidate; P omogeneo su ogni convesso limitato (onda, τξ, prodotti di trasporti); P quasi omogeneo su rettangoli con lati paralleli agli assi (trave). Residui: OPF-Q1 (calore × trasporto) APERTO, e quasi omogenei su convessi non rettangolari APERTO (nuovo, dal KA). P2-C1(b) → ramo (ii) per ogni m.
- C12-Q2 → PARZIALE (OPF-P6, P7); OPF-Q2 APERTO.
- C12-Q6 → CHIUSO (OPF-T4).
- S5-L2 → DIMOSTRATO, con (v) corretta.
