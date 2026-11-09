# PROOF_PACKAGE — S10-COL (27/10/2026)

Prover: S10-COL. Oggetto: prova autonoma di (COL-ii), l'inclusione del flusso usata nel Passo B di S10A-T3 (`work/S10-OPEN-A/PROOF_PACKAGE.md` §3). Riferimenti: `research/CIT-AUDIT/AUDIT-COL.md` §4 (schema) e `work/CHECK-F10/AUDIT_S10-OPEN-A.md`, fix A-7.

**Esito in breve.** (COL-ii) è dimostrata in $\mathbb R^n$, $n\ge2$, in due versioni:
- per il campo di carta $V=-\sum_i\theta_ie_i$ (Teorema A + Teorema C). Questa versione non usa né le normali né (COL-i), e in S10A-T3 elimina del tutto la dipendenza da [COL];
- per un campo qualsiasi $V\in C^1_c$ con $V\cdot\nu\ge\kappa>0$ q.o. su $\partial\Omega$ (Teorema B + Teorema C), cioè per il campo dato da (COL-i).

In entrambi i casi si ha, per ogni $\sigma>0$, $\Phi_{-\sigma}(\bar\Omega)\subset\Omega$, quindi $\bar\Omega\subset\Phi_\sigma(\Omega)$. Inoltre esistono $\sigma_0,c>0$ con $\mathrm{dist}(\Phi_{-\sigma}(\bar\Omega),\partial\Omega)\ge c\sigma$ per $0<\sigma\le\sigma_0$.

Il "punto delicato" di AUDIT-COL §4, cioè la compatibilità dei coni nelle zone di sovrapposizione delle carte, si risolve con un oggetto intrinseco: il cono $D(p)$ delle direzioni entranti (§1). È definito solo a partire da Ω, è un cono convesso aperto e contiene il cono di **ogni** carta che passa per p. Non serve quindi nessuna condizione di compatibilità tra carte.

---
## §0. Convenzioni

- $\Omega\subset\mathbb R^n$ è aperto e limitato, con $n\ge2$. La connessione non serve. $\complement\Omega:=\mathbb R^n\setminus\Omega$ è chiuso e non vuoto.
- **Carta lipschitziana** $(C,R,g,L)$: $C$ è un aperto; $R$ è un'isometria affine di $\mathbb R^n$, con coordinate $y=R(x)=(y',y_n)$; $g:\mathbb R^{n-1}\to\mathbb R$ è L-lipschitziana; e vale
  $$\Omega\cap C=\{x\in C:\ y_n>g(y')\}.$$
  Se g è data solo sulla proiezione di $R(C)$, la si estende con McShane, $g(y'):=\inf_z\,(g(z')+L|y'-z'|)$, che conserva la costante. La **direzione verticale** della carta è $e:=(dR)^{-1}e_n$, un vettore unitario. Per un vettore $z$ si scrive $(z',z_n):=dR\,z$ (parte lineare di R). Il **cono di carta** è $\Gamma:=\{z:\ z_n>L|z'|\}$.
- Ω è **lipschitziano** se ogni $p\in\partial\Omega$ sta in una carta lipschitziana. Per compattezza bastano finite carte $(C_i,R_i,g_i,L_i)$, $i=1..N$, con $\partial\Omega\subset\bigcup_iC_i$. La convenzione con il dominio "sotto il grafico" (Grisvard) si riduce a questa con una riflessione.
- **Normale.** Nella carta, dove g è differenziabile (q.o. per Rademacher), la normale esterna nel punto $(y',g(y'))$ è $\nu=(dR)^{-1}(\nabla g,-1)/\sqrt{1+|\nabla g|^2}$. "Quasi ovunque su $\partial\Omega$" (misura superficiale) equivale a "per quasi ogni $y'$" nella carta, perché $y'\mapsto(y',g(y'))$ è bi-lipschitziana. L'indipendenza di ν dalla carta è nell'Osservazione 3.2; il Teorema B non ne ha bisogno.
- **Flusso.** $V\in C^1_c(\mathbb R^n;\mathbb R^n)$ ha flusso globale $\Phi_s$, un gruppo a un parametro di diffeomorfismi $C^1$; se V è $C^\infty$, sono $C^\infty$. Si pone $W:=-V$ e $\psi_t:=\Phi_{-t}$, che è il flusso di W. $M:=\sup|V|$.
- **Fatti elementari.**
  (F1) Se $(C,R,g,L)$ è una carta e $x\in\bar\Omega\cap C$, allora $x_n\ge g(x')$. Infatti $x=\lim x_k$ con $x_k\in\Omega$; siccome C è aperto, $x_k\in\Omega\cap C$ definitivamente, dunque $x_{k,n}>g(x_k')$, e si passa al limite.
  (F2) Se $x\in C$ e $b:=x_n-g(x')>0$, allora $\mathrm{dist}(x,\complement\Omega)\ge\min\big(b/\sqrt{1+L^2},\ \mathrm{dist}(x,\complement C)\big)$. Infatti, per $|z-x|$ minore di quel minimo, $z\in C$ e $z_n-g(z')\ge b-|z_n-x_n|-L|z'-x'|\ge b-\sqrt{1+L^2}\,|z-x|>0$ (Cauchy–Schwarz, SymPy (S2)), dunque $z\in\Omega$.
  (F3) Per $y\in\Omega$ si ha $\mathrm{dist}(y,\partial\Omega)=\mathrm{dist}(y,\complement\Omega)$. La disuguaglianza "≥" vale perché $\partial\Omega\subset\complement\Omega$. Per "≤": sia z un punto di $\complement\Omega$ più vicino a y. Il primo punto del segmento $[y,z]$ che non sta in Ω sta in $\partial\Omega$, a distanza $\le|y-z|$.

---
## §1. Il cono delle direzioni entranti

**Definizione 1.1.** Per $p\in\partial\Omega$, $D(p)$ è l'insieme dei $w\in\mathbb R^n$ per cui esistono $r>0$ e $a>0$ tali che
$$\mathrm{dist}(x+tu,\ \complement\Omega)\ge a\,t\qquad\forall\,x\in\bar\Omega\cap B(p,r),\ u\in B(w,r),\ t\in(0,r].$$
In particolare $x+tu\in\Omega$, perché la distanza è positiva e $\complement\Omega$ è chiuso. Si dice che $(r,a)$ **testimonia** $w\in D(p)$.

$D(p)$ dipende solo da Ω e da p, non da carte. Si ha $0\notin D(p)$: con $x=p$ e $u$ arbitrario in $B(0,r)$, una palla di centro p starebbe in Ω, contro $p\in\partial\Omega$.

### [S10COL-L1] Lemma ($D(p)$ è un cono convesso aperto) — PROVA SCRITTA
(i) Se $(r,a)$ testimonia $w\in D(p)$, allora $B(w,r/2)\subset D(p)$, con testimone $(r/2,a)$. (ii) $w\in D(p)$ e $\lambda>0$ implicano $\lambda w\in D(p)$. (iii) $w_1,w_2\in D(p)$ implicano $w_1+w_2\in D(p)$. Di conseguenza ogni combinazione $\sum_k\lambda_kw_k$ con $\lambda_k\ge0$ non tutti nulli e $w_k\in D(p)$ sta in $D(p)$.

*Prova.* (i) Se $|\tilde w-w|<r/2$ e $u\in B(\tilde w,r/2)$, allora $u\in B(w,r)$, e $B(p,r/2)\subset B(p,r)$, $t\le r/2\le r$.
(ii) Sia $(r,a)$ il testimone di w e sia $\rho:=\min(r,\lambda r,r/\lambda)$. Per $x\in\bar\Omega\cap B(p,\rho)$, $u\in B(\lambda w,\rho)$ e $t\in(0,\rho]$ si scrive $x+tu=x+(\lambda t)(u/\lambda)$. Qui $|u/\lambda-w|<\rho/\lambda\le r$ e $0<\lambda t\le\lambda\rho\le r$, quindi la distanza è $\ge a\lambda t$. Il testimone è $(\rho,\lambda a)$.
(iii) Siano $(r_1,a_1)$ e $(r_2,a_2)$ i testimoni, e sia $\rho:=\min\big(1,r_1,r_2,\,r_2/(2+|w_1|)\big)$. Per $x\in\bar\Omega\cap B(p,\rho)$, $u\in B(w_1+w_2,\rho)$ e $t\in(0,\rho]$, si pone $u_k:=w_k+\tfrac12(u-w_1-w_2)$, così che $u_1+u_2=u$ e $|u_k-w_k|<\rho/2$ (SymPy (S4)). Il punto $x_1:=x+tu_1$ soddisfa $\mathrm{dist}(x_1,\complement\Omega)\ge a_1t>0$, quindi $x_1\in\Omega$. Inoltre $|x_1-p|<\rho+\rho(|w_1|+\rho/2)\le\rho(2+|w_1|)\le r_2$. Applicando il testimone di $w_2$ a $x_1$, $u_2$, $t$ si ottiene $\mathrm{dist}(x_1+tu_2,\complement\Omega)\ge a_2t$, e $x_1+tu_2=x+tu$. Il testimone è $(\rho,a_2)$.
L'ultima affermazione segue togliendo i termini con $\lambda_k=0$ e applicando (ii) e (iii). ∎

### [S10COL-L2] Lemma (il cono di ogni carta è entrante) — PROVA SCRITTA
Sia $(C,R,g,L)$ una carta lipschitziana. Allora $\Gamma\subset D(p)$ per ogni $p\in\partial\Omega\cap C$; in particolare $e\in D(p)$.

*Prova.* Si lavora nelle coordinate della carta. Siano $z\in\Gamma$, $\delta:=z_n-L|z'|>0$ e $d:=\mathrm{dist}(p,\complement C)>0$. Si sceglie $r\in(0,1]$ con $\sqrt{1+L^2}\,r\le\delta/2$ e $r(2+|z|)\le d/2$. Siano $x\in\bar\Omega\cap B(p,r)$, $u\in B(z,r)$, $t\in(0,r]$ e $y:=x+tu$.
- $x\in C$ perché $r<d$, quindi $x_n\ge g(x')$ per (F1).
- $|y-p|<r+r(|z|+r)\le r(2+|z|)\le d/2$, quindi $y\in C$ e $\mathrm{dist}(y,\complement C)\ge d/2$.
- $u_n-L|u'|\ge\delta-|u_n-z_n|-L|u'-z'|\ge\delta-\sqrt{1+L^2}\,r\ge\delta/2$.
- $y_n-g(y')\ge x_n-g(x')+tu_n-L\,t|u'|\ge t\delta/2$.

Per (F2), $\mathrm{dist}(y,\complement\Omega)\ge\min\big(t\delta/(2\sqrt{1+L^2}),\,d/2\big)\ge t\,a$ con $a:=\min\big(\delta/(2\sqrt{1+L^2}),\,d/2\big)$, perché $t\le1$. Infine $e$ ha coordinate $(0,1)$, quindi $e\in\Gamma$. ∎

### [S10COL-L3] Lemma (da una direzione entrante alle traiettorie) — PROVA SCRITTA
Siano $W\in C^1_c(\mathbb R^n;\mathbb R^n)$, $\psi_t$ il suo flusso, $p\in\partial\Omega$ e $W(p)\in D(p)$ con testimone $(r,a)$. Allora esiste $\rho_p\in(0,r]$ tale che
$$\mathrm{dist}(\psi_t(x),\complement\Omega)\ge a\,t\qquad\forall\,x\in\bar\Omega\cap B(p,\rho_p),\ t\in(0,\rho_p].$$

*Prova.* Sia $M:=\sup|W|$. Per continuità esiste $\eta>0$ con $|W(y)-W(p)|\le r/2$ per $|y-p|\le\eta$. Si pone $\rho_p:=\min\big(r,\eta/(1+M)\big)$. Per $x\in\bar\Omega\cap B(p,\rho_p)$, $t\in(0,\rho_p]$ e $s\in[0,t]$ si ha $|\psi_s(x)-p|\le|x-p|+sM<\rho_p(1+M)\le\eta$. Quindi
$$\psi_t(x)=x+t\,u,\qquad u:=\frac1t\int_0^tW(\psi_s(x))\,ds,\qquad|u-W(p)|\le\frac1t\int_0^t|W(\psi_s x)-W(p)|\,ds\le\frac r2<r.$$
Siccome $x\in\bar\Omega\cap B(p,r)$, $u\in B(W(p),r)$ e $t\le r$, il testimone dà la tesi. ∎

---
## §2. Il campo di carta (via diretta, senza normali)

### [S10COL-TA] Teorema A (il campo di carta è entrante in ogni punto) — PROVA SCRITTA
Sia Ω limitato lipschitziano con carte $(C_i,R_i,g_i,L_i)$, $i=1..N$, che ricoprono $\partial\Omega$, e siano $e_i$ le direzioni verticali. Siano $\theta_i\in C_c^\infty(C_i)$ con $\theta_i\ge0$ e $\sum_i\theta_i>0$ su $\partial\Omega$; per esempio una partizione dell'unità subordinata al ricoprimento, oppure somme finite di funzioni bump. Si pone
$$W:=\sum_{i=1}^N\theta_i\,e_i\in C_c^\infty(\mathbb R^n;\mathbb R^n),\qquad V:=-W.$$
Allora $W(p)\in D(p)$ per ogni $p\in\partial\Omega$.

*Prova.* Sia $I(p):=\{i:\theta_i(p)>0\}$, non vuoto per ipotesi. Per $i\in I(p)$ si ha $p\in\mathrm{supp}\,\theta_i\subset C_i$, quindi $p\in\partial\Omega\cap C_i$ e $e_i\in D(p)$ (S10COL-L2). Ne segue $W(p)=\sum_{i\in I(p)}\theta_i(p)e_i\in D(p)$ per S10COL-L1. ∎

*Sulla compatibilità tra carte.* Non serve alcuna ipotesi sulle carte che si sovrappongono: $e_i$ e $e_j$ possono formare angoli grandi, e $e_j$ può stare fuori dal cono $\Gamma_i$. Per esempio, nel semipiano $\{y_2>0\}$ con $e_1=(0,1)$, $L_1=1$, ed $e_2$ inclinata di 60°, $L_2=\tan60^\circ$, si ha $e_2\notin\Gamma_1$. Entrambe stanno però in $D(p)$, che è intrinseco e convesso, e questo basta. È il motivo per cui l'argomento di AUDIT-COL §4, punto 2, che richiedeva $-V\in\Gamma_i$ per ogni carta contenente il punto, non è necessario. Nel test numerico (§6) le direzioni di carte adiacenti formano fino a 66°.

---
## §3. Un campo qualsiasi con $V\cdot\nu\ge\kappa$ (compatibilità con (COL-i))

### [S10COL-TB] Teorema B (trasversalità q.o. ⟹ direzione entrante in ogni punto) — PROVA SCRITTA
Sia Ω limitato lipschitziano con le carte di §0. Sia $V\in C^1_c(\mathbb R^n;\mathbb R^n)$ con $V\cdot\nu\ge\kappa>0$ q.o. su $\partial\Omega$. Precisamente, per ogni carta $(C,R,g,L)$ dell'atlante e per quasi ogni $y'$ con $q:=R^{-1}(y',g(y'))\in C$:
$$V(q)\cdot\nu(q)\ge\kappa,\qquad\text{cioè}\qquad W_n(q)-W'(q)\cdot\nabla g(y')\ge\kappa\sqrt{1+|\nabla g(y')|^2},\quad W:=-V$$
(l'equivalenza è un'identità, SymPy (S1)). Allora $W(p)\in D(p)$ per ogni $p\in\partial\Omega$.

*Prova.* Siano $p\in\partial\Omega$ e $(C,R,g,L)$ una carta con $p\in C$; si lavora nelle sue coordinate. Si ha $p=(p',g(p'))$: per (F1) $p_n\ge g(p')$, e se fosse $p_n>g(p')$ allora $p\in\Omega\cap C$, che è aperto, contro $p\in\partial\Omega$. Sia $\eta>0$ con $B(p,\eta)\subset C$ e $|W(y)-W(p)|\le\kappa/4$ su $B(p,\eta)$. Per continuità di g esiste $\delta>0$ tale che, per $|y'-p'|<2\delta$, il punto $q=(y',g(y'))$ sta in $B(p,\eta)$.

*Passo 1 (disuguaglianza puntuale per le direzioni vicine).* Sia $w\in B(W(p),\kappa/4)$. Per quasi ogni $y'\in B'(p',2\delta)$, con $q=(y',g(y'))$, si ha $|w-W(q)|<\kappa/2$ e
$$w_n-w'\cdot\nabla g(y')=\big[W_n(q)-W'(q)\cdot\nabla g\big]+(w-W(q))\cdot(-\nabla g,1)\ge(\kappa-|w-W(q)|)\sqrt{1+|\nabla g|^2}\ge\tfrac\kappa2.$$
La disuguaglianza usa Cauchy–Schwarz (SymPy (S3)).

*Passo 2 (integrazione lungo i segmenti, Fubini).* Siano w come nel Passo 1, $x'\in B'(p',\delta)$ e $0\le t\le\delta/(1+|w'|)$. Allora
$$g(x'+tw')-g(x')\le t\,(w_n-\kappa/2).$$
Sia $N\subset B'(p',2\delta)$ l'insieme nullo dei punti dove g non è differenziabile (Rademacher) o dove il Passo 1 fallisce. La mappa $T(x',s):=(x'+sw',s)$ è lineare e invertibile su $\mathbb R^{n-1}\times\mathbb R$, quindi $T^{-1}(N\times\mathbb R)=\{(x',s):x'+sw'\in N\}$ è nullo in $\mathbb R^n$. Per Fubini–Tonelli, per quasi ogni $x'$ l'insieme $\{s:\ x'+sw'\in N\}$ è nullo in ℝ. Per un tale $x'\in B'(p',\delta)$, il segmento $\{x'+sw':0\le s\le t\}$ sta in $B'(p',2\delta)$, perché $|x'+sw'-p'|<\delta+t|w'|\le2\delta$. La funzione $f(s):=g(x'+sw')$ è lipschitziana, quindi assolutamente continua. Per quasi ogni s il punto $x'+sw'$ non sta in N; lì g è differenziabile e $f'(s)=\nabla g(x'+sw')\cdot w'\le w_n-\kappa/2$. Dunque $f(t)-f(0)=\int_0^tf'\le t(w_n-\kappa/2)$. Per un $x'\in B'(p',\delta)$ qualunque si prende una successione di punti buoni $x_k'\to x'$ in $B'(p',\delta)$ (esiste perché i punti buoni hanno misura piena) e si passa al limite, g essendo continua.

*Passo 3 (testimone).* Sia $d:=\mathrm{dist}(p,\complement C)$. Si sceglie $r\in(0,1]$ con $r<\kappa/4$, $r<\delta$, $r\le\delta/(2+|W(p)|)$ e $r(2+|W(p)|)\le d/2$. Siano $x\in\bar\Omega\cap B(p,r)$, $u\in B(W(p),r)$ e $t\in(0,r]$.
- $x\in C$ e $x_n\ge g(x')$ per (F1); inoltre $x'\in B'(p',r)\subset B'(p',\delta)$.
- $u\in B(W(p),\kappa/4)$ e $t\le r\le\delta/(2+|W(p)|)\le\delta/(1+|u'|)$, perché $|u'|\le|W(p)|+1$.
- Come in S10COL-L2, $y:=x+tu\in C$ e $\mathrm{dist}(y,\complement C)\ge d/2$.
- Per il Passo 2: $y_n-g(y')=x_n-g(x')+tu_n-\big(g(x'+tu')-g(x')\big)\ge tu_n-t(u_n-\kappa/2)=t\kappa/2$.

Per (F2), $\mathrm{dist}(y,\complement\Omega)\ge t\cdot\min\big(\kappa/(2\sqrt{1+L^2}),\,d/2\big)$. Quindi $W(p)\in D(p)$. ∎

*Osservazione 3.1 (perché non servono le normali di Clarke).* Il mandato suggeriva di passare dal cono di Clarke delle normali. Il Passo 2 lo evita: la condizione q.o. viene integrata lungo quasi ogni segmento parallelo a $w'$, e la continuità di W la estende a un intorno di direzioni e di punti. È l'argomento "normali q.o. ⟹ disuguaglianza su ogni segmento", lo stesso meccanismo che sta dietro la descrizione del gradiente di Clarke come inviluppo convesso dei limiti di $\nabla g$. Qui non si usa nessun teorema sul gradiente di Clarke: basta la disuguaglianza lungo i segmenti.

*Osservazione 3.2 (indipendenza della normale dalla carta; non usata altrove).* Se g è differenziabile in $p'$, il cono tangente di Bouligand $T(p):=\{\lim t_k^{-1}(x_k-p):\ x_k\in\bar\Omega,\ t_k\downarrow0\}$ è il semispazio $\{z_n\ge\nabla g(p')\cdot z'\}$.
- "⊂": per (F1), $x_{k,n}-p_n\ge g(x_k')-g(p')=\nabla g(p')\cdot(x_k'-p')+o(|x_k-p|)$; si divide per $t_k$.
- "⊃": se $z_n>\nabla g\cdot z'$, allora $p+tz\in\Omega$ per t piccolo; si conclude perché $T(p)$ è chiuso.

$T(p)$ dipende solo da Ω, quindi la normale esterna unitaria, l'unico ν con $T(p)=\{z\cdot\nu\le0\}$, è la stessa in tutte le carte nei punti dove entrambe le g sono differenziabili, cioè q.o. Ne segue che l'ipotesi del Teorema B nella forma "per ogni carta" equivale alla forma geometrica "q.o. su ∂Ω" delle fonti (Grisvard 1.5.1.9, HMT Cor. 2.13).

*Osservazione 3.3 (il campo di carta soddisfa anche (COL-i)).* Per il W del Teorema A, nei punti dove la normale esiste, $W\cdot(-\nu)=\sum_i\theta_i\,e_i\cdot(-\nu)$ e $e_i\cdot(-\nu)=1/\sqrt{1+|\nabla g_i|^2}\ge1/\sqrt{1+L_i^2}$ (per l'Oss. 3.2 la normale è la stessa nella carta i). Quindi $V\cdot\nu\ge\kappa:=\min_{\partial\Omega}\sum_i\theta_i/\sqrt{1+L_i^2}>0$, per compattezza e continuità. È il calcolo di Grisvard; qui non serve, perché il Teorema A dà direttamente $W(p)\in D(p)$.

---
## §4. Le inclusioni globali, con uniformità

### [S10COL-TC] Teorema C ((COL-ii)) — PROVA SCRITTA
Sia Ω aperto limitato, sia $V\in C^1_c(\mathbb R^n;\mathbb R^n)$, e si ponga $W=-V$, con $W(p)\in D(p)$ per ogni $p\in\partial\Omega$. Questo vale per il campo di carta (Teorema A) e per ogni campo con $V\cdot\nu\ge\kappa$ q.o. (Teorema B). Siano $\Phi_s$ il flusso di V e $M=\sup|V|$. Allora:
(a) esistono $\sigma_0>0$ e $c>0$ tali che, per ogni $x\in\bar\Omega$ e ogni $\sigma\in(0,\sigma_0]$, $\mathrm{dist}(\Phi_{-\sigma}(x),\complement\Omega)\ge c\sigma$. Quindi $\Phi_{-\sigma}(\bar\Omega)\subset\Omega$, $\mathrm{dist}(\Phi_{-\sigma}(\bar\Omega),\partial\Omega)\ge c\sigma$ e $\bar\Omega\subset\Phi_\sigma(\Omega)$;
(b) $\Phi_{-s}(\bar\Omega)\subset\Omega$, cioè $\bar\Omega\subset\Phi_s(\Omega)$, per **ogni** $s>0$;
(c) $\Phi_\sigma(\Omega)\subset\{\mathrm{dist}(\cdot,\bar\Omega)\le M\sigma\}\subset\{\mathrm{dist}(\cdot,\bar\Omega)<C\sigma\}$ per ogni $C>M$ e ogni $\sigma>0$. Inoltre $\Phi_\sigma(\Omega)$ è aperto e diffeomorfo a Ω tramite $\Phi_\sigma$, quindi ha gli stessi invarianti topologici, in particolare lo stesso $b_1$.

*Prova.* (a) *Ricoprimento finito.* Per S10COL-L3, ogni $p\in\partial\Omega$ ha un $\rho_p>0$ e un $a_p>0$. Per compattezza di $\partial\Omega$ esistono $p_1,\dots,p_k$ con $\partial\Omega\subset\bigcup_jB(p_j,\rho_{p_j}/2)$. Si pone $\sigma_1:=\min_j\rho_{p_j}/2$ (fa da numero di Lebesgue) e $c:=\min_ja_{p_j}$.
- *Punti vicini al bordo.* Se $x\in\bar\Omega$ e $\mathrm{dist}(x,\partial\Omega)<\sigma_1$, esiste $p\in\partial\Omega$ con $|x-p|<\sigma_1$ (∂Ω è compatto) e un j con $p\in B(p_j,\rho_{p_j}/2)$. Allora $|x-p_j|<\rho_{p_j}$, e per $t\in(0,\sigma_1]\subset(0,\rho_{p_j}]$ S10COL-L3 dà $\mathrm{dist}(\psi_t(x),\complement\Omega)\ge a_{p_j}t\ge ct$.
- *Punti lontani.* Se $x\in\bar\Omega$ e $\mathrm{dist}(x,\partial\Omega)\ge\sigma_1$, allora $x\in\Omega$ e $\mathrm{dist}(x,\complement\Omega)\ge\sigma_1$ per (F3). Siccome $|\psi_t(x)-x|\le Mt$, si ha $\mathrm{dist}(\psi_t(x),\complement\Omega)\ge\sigma_1-Mt\ge ct$ per $t\le\sigma_1/(M+c)$.

Con $\sigma_0:=\min\big(\sigma_1,\sigma_1/(M+c)\big)$ si ottiene la stima, ricordando che $\psi_\sigma=\Phi_{-\sigma}$. Le conseguenze seguono da (F3) e dalla biiettività di $\Phi_\sigma$: $\Phi_{-\sigma}(\bar\Omega)\subset\Omega\iff\bar\Omega\subset\Phi_\sigma(\Omega)$.
(b) Si mostra prima $\psi_t(\Omega)\subset\Omega$ per ogni $t\ge0$. Supponiamo per assurdo $x\in\Omega$ con $\tau:=\inf\{t\ge0:\psi_t(x)\notin\Omega\}<\infty$. Allora $\tau>0$, perché Ω è aperto. Il punto $y:=\psi_\tau(x)$ non sta in Ω (limite di punti di $\complement\Omega$, che è chiuso) e sta in $\bar\Omega$ (limite di $\psi_t(x)\in\Omega$ per $t\uparrow\tau$), quindi $y\in\partial\Omega$. Sia $h\in(0,\min(\tau,\sigma_0))$: allora $z:=\psi_{\tau-h}(x)\in\Omega$, e per (a) $y=\psi_h(z)\in\Omega$. Contraddizione. Per $s>0$ e $x\in\bar\Omega$: se $s\le\sigma_0$ si usa (a); altrimenti $\psi_s(x)=\psi_{s-\sigma_0}(\psi_{\sigma_0}(x))$ con $\psi_{\sigma_0}(x)\in\Omega$.
(c) $|\Phi_\sigma(x)-x|\le M\sigma$ per ogni x; il resto è perché $\Phi_\sigma$ è un diffeomorfismo di $\mathbb R^n$. ∎

*Osservazione 4.1 (nessuna circolarità, uniformità).* La costante $\sigma_0$ dipende solo dal ricoprimento finito $\{B(p_j,\rho_{p_j}/2)\}$ e da M. Le $\rho_{p_j}$ dipendono dal modulo di continuità di W in $p_j$, dai testimoni (S10COL-L1, -L2 oppure il Passo 3 di S10COL-TB) e quindi dalle carte, dai $\theta_i$ e da κ. Nessuna scelta dipende da σ.

*Osservazione 4.2 (dove la prova smette di funzionare).* Se Ω non è lipschitziano, $D(p)$ può essere vuoto. Nel disco con una fessura, sia p un punto interno alla fessura. Una direzione w trasversale fa attraversare la fessura ai punti x che le stanno vicino dal lato opposto: al tempo $t=h/|w\cdot n|$, con h la distanza di x dalla fessura, il punto $x+tw$ sta sulla fessura, e la stima $\ge at$ fallisce. Una direzione tangente lascia p sulla fessura. Dunque $D(p)=\emptyset$, e nessun campo soddisfa l'ipotesi del Teorema C. È coerente con il residuo (1) di S10A-T3.

---
## §5. Applicazione a S10A-T3 (sostituzione proposta nel Passo B)

Il Passo 1′ di S10A-T3 fornisce già i dati del Teorema A in $\mathbb R^2$: carte $C_i$ con direzione verticale $e_i$, grafici $\varphi_i$ $L_i$-lipschitziani, e $\theta_i\in C_c^\infty(C_i')$ con $\sum_{i\ge0}\theta_i=1$ su un intorno di $\bar\Omega$ e $\theta_0\in C_c^\infty(\Omega_0)$, dunque $\theta_0=0$ su $\partial\Omega$. Serve in più $\theta_i\ge0$, che una partizione dell'unità standard soddisfa: va detto esplicitamente. Allora $\sum_{i\ge1}\theta_i=1>0$ su $\partial\Omega$.

Testo proposto per il Passo B:
> **Passo B (un intorno con la stessa topologia).** Sia $V:=-\sum_{i\ge1}\theta_ie_i\in C_c^\infty(\mathbb R^2;\mathbb R^2)$, con $\theta_i\ge0$ e $e_i$ del Passo 1′, sia $\Phi_\sigma$ il suo flusso e sia $M:=\sup|V|$. Per S10COL-TA e S10COL-TC (`work/S10-COL/PROOF_PACKAGE.md`), per ogni $\sigma>0$ si ha $\bar\Omega\subset\Phi_\sigma(\Omega)\subset\{\mathrm{dist}(\cdot,\bar\Omega)\le M\sigma\}$, e $\Phi_\sigma(\Omega)$ è aperto e diffeomorfo a Ω. Fissato ε, si prende σ con $M\sigma<r_\varepsilon/4$: $U:=\Phi_\sigma(\Omega)$ soddisfa $\bar\Omega\subset U\subset V'_\varepsilon$ e $b_1(U)=b_1(\Omega)$.

Con questo testo [Fonte COL] non serve più a S10A-T3: né (COL-i) né (COL-ii). La dipendenza diventa S10COL-TA + S10COL-TC. La Precisazione (2) del Passo D resta valida: U dipende solo da σ, e un solo σ va bene per tutti i $\varepsilon_k$.

Proposta di stato per S10A-T3, da confermare dopo l'audit di S10-COL: "PROVA SCRITTA mod F1, F2", senza [COL]. Le righe derivate (P2-Q1 "densità sui lipschitziani semplicemente connessi", OPF5B-C1(d)) perdono il condizionamento a [COL] (A-7(d)) quando l'audit lo conferma.

---
## §6. Controlli numerici e simbolici

Si usa `D:\ProblemaBase\.venv\Scripts\python.exe -I`.

**`sympy/s10col_sym.py` → `s10col_sym.out`: 6/6 OK.**
- (S1) $W\cdot(-\nu)\sqrt{1+|\nabla g|^2}=W_n-W'\cdot\nabla g$, $|\nu|=1$, ν ortogonale al piano tangente ($n=3$).
- (S2) $(1+L^2)(a^2+b^2)-(a+Lb)^2=(La-b)^2$, usata in (F2) e in S10COL-L2.
- (S3) identità di Lagrange per Cauchy–Schwarz, usata nel Passo 1 di S10COL-TB.
- (S4) la scomposizione $u=u_1+u_2$ di S10COL-L1(iii).

**`sympy/s10col_flow.py` → `s10col_flow.out`: TUTTO OK.** Il dominio è un poligono stellato a zig-zag con 24 vertici (raggi alternati 1 e 0.6), lipschitziano e non convesso. Le carte sono palle $B(v_k,r)$, con $r=0.55\,\ell$ e $\ell$ la lunghezza dei lati. Le direzioni $e_k$ sono scelte apposta vicino al **bordo** del cono ammissibile, alternando i lati, per stressare la compatibilità. Il campo è $W=\sum_k\phi_ke_k$, con $\phi_k$ funzioni bump: non sommano a 1, come permette il Teorema A.
- (1) Le palle sono carte: 0 disaccordi tra Ω e l'epigrafico su 24×20000 punti; L massimo 35.3. Le palle non toccano lati non adiacenti (0.291 > 0.2465).
- (2) Ricoprimento: $\min_{\partial\Omega}\sum\phi_k=0.017>0$.
- (3) $\kappa=\min V\cdot\nu=6\cdot10^{-4}>0$; l'angolo massimo fra le $e_k$ di carte adiacenti è 66.1°.
- (4) Monte Carlo con 9464 punti iniziali (vertici, punti del bordo, punti vicini al bordo, punti interni), RK4 con passo $2\cdot10^{-4}$, $t\le0.04$: 0 violazioni; $\min\mathrm{dist}(\psi_tx,\complement\Omega)/t=7\cdot10^{-4}$, costante in t. Con direzioni al 20%/80% del cono: $\kappa=0.0031$, $c_{emp}=0.0033$, 0 violazioni.
- (5) Teorema B con un campo perturbato, che non è un campo di carta: $\kappa=0.0020>0$, 0 violazioni, $c_{emp}=0.0022$.
- (6) Controllo negativo: con $e_0$ invertita, fuori dal cono, il vertice 0 esce da Ω ($\mathrm{sdist}=-0.010$ dopo $t=0.01$).

Lettura: la costante empirica c è dell'ordine di κ, come prevede il Passo 3 di S10COL-TB ($y_n-g\ge t\kappa/2$). I valori piccoli vengono dal fatto che le bump valgono poco nei punti di sovrapposizione.

---
## §7. Dipendenze, rischi, punti per l'audit

- **Dipendenze esterne:** solo fatti standard di analisi reale, cioè Rademacher, Fubini–Tonelli, assoluta continuità delle funzioni lipschitziane, estensione di McShane, esistenza globale e proprietà di gruppo del flusso di un campo $C^1_c$. Nessuna fonte bibliografica. (COL-i), cioè Grisvard 1.5.1.9, serve solo per chi vuole usare un V dato da quella fonte (Teorema B); per S10A-T3 non serve.
- **Punti da controllare (proof-checker):**
  1. S10COL-L1(iii): la scelta di ρ, cioè $x_1\in B(p,r_2)$, e il fatto che $x_1\in\bar\Omega$.
  2. S10COL-L2: l'uso di (F1) richiede $x\in C$, garantito da $r<d$.
  3. S10COL-TB, Passo 2: Fubini sull'insieme $T^{-1}(N\times\mathbb R)$, e il passaggio da quasi ogni $x'$ a ogni $x'$ per continuità.
  4. S10COL-TC(b): la definizione di τ e il fatto che $y\in\partial\Omega$.
  5. §5: $\theta_i\ge0$ va aggiunto esplicitamente al Passo 1′ di S10A-T3.
- **Kill-argument suggerito:** cercare un lipschitziano e una scelta di carte e $\theta_i\ge0$ con $\sum\theta_i>0$ su ∂Ω per cui il flusso di $-V$ esca da Ω. Per il Teorema A non dovrebbe esistere, perché la prova non usa nessuna relazione tra le carte. Il candidato naturale sono carte con direzioni quasi opposte che si sovrappongono. Ma $e_i,e_j\in D(p)$ e $0\notin D(p)$, e $D(p)$ è un cono convesso, quindi $\lambda e_i+\mu e_j\ne0$ per $\lambda,\mu\ge0$ non entrambi nulli: due direzioni di carta in uno stesso punto non sono mai opposte.
