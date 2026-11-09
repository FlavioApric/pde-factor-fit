# CATALOGO_v2 — schede dei casi ★ (S-C1C2, 25/10/2026)
Template: `skills-local/kernel-catalog-entry` (NOTAZIONE v2: componente = fattore; $H^m(\Omega)$, $\Omega=I\times J$ rettangolo aperto limitato, $I=(0,T)$, $|J|=L$; $R=\mathbb C[\tau,\xi]$, $\partial_t\leftrightarrow\tau$, $\partial_x\leftrightarrow\xi$).
Le schede **aggiornano** (non duplicano) le voci esistenti: research/R3/REPORT.md K3, K4, K11, K12; research/PR-C2b/cards C2.06, C2.07, C2.08, C2.12; research/PR-C2c/cards C2.33. Gli ID [C12-…] rimandano a work/C1C2/PROOF_PACKAGE.md; i Gram tra fattori sono in work/C1C2/gram.md.
Skill usate: kernel-catalog-entry (template), sympy (`sympy/c12_catalog.py` → `c12_catalog.out` **54/54 PASS**; più `c12_appell.out` 65/65, `c12_factors.out` 48/48, `c12_gram.out` 8/8). Nessuno script `_vendor` eseguito.
Notazione comune. Per un fattore di evoluzione $\tau-a(\xi)$, $\deg a=q\ge1$: base di Appell $v_n$ definita da $\sum_n v_n z^n/n!=e^{z(x-x_0)+t\,a(z)}$, spazio di Fock pesato $\mathcal F_{a,\rho}$ con peso $w_n=(n!)^{2(1-1/q)}\rho^{2n}$, $\rho>K=e^{X+TA}$ ($A=\sum|\alpha_l|$, $X=\sup_J|x-x_0|$) [C12-T6]. Esponenziali $e_{(\sigma,\zeta)}:=e^{\sigma t+\zeta x}$, $(\sigma,\zeta)\in V(P)$. Gram di esponenziali in forma chiusa: gram.md §1.
Stato di ogni scheda: lo stato del contenuto analitico è quello degli ID citati (prove scritte, audit S-CHECK in attesa per C12-T1, L2, C1, T3, T2); i fatti algebrici elementari (fattorizzazioni, dimensioni) sono verificati in SymPy in modo esatto.

---
# C2.07 / K4 — Calore $\partial_t-D\partial_x^2$   [★]
1. **Operatore e simbolo.** $P=\tau-D\xi^2$ ($D>0$; nel seguito $D=1$ salvo avviso). Irriducibile (grado 1 in $\tau$, primitivo): **una sola componente**, $m_1=1$ [C12-P3].
2. **Nucleo e classe.** $\ker_{H^m(\Omega)}P$ = soluzioni del calore in $H^m(\Omega)$ (chiuso). Base numerabile: polinomi del calore (Rosenbloom–Widder) $v_n=\sum_{k\le n/2}\frac{n!}{k!(n-2k)!}t^k(x-x_0)^{n-2k}$ (per $D=1$), base ortonormale $\{v_n/\sqrt{n!\rho^{2n}}\}$ di $\mathcal F_{\xi^2,\rho}$, immerso con continuità in ogni $H^k(\Omega)$ [C12-T6(iii),(v)]. $\mathcal F$ contiene tutti gli esponenziali $e^{\zeta x+\zeta^2t}$, $\zeta\in\mathbb C$ (anche reali, assenti in $L^2(\mathbb R)$), $\|e_\zeta\|^2=e^{\rho^2|\zeta|^2}$ [T6(iv)]. Densità di $\mathcal F$ in $\ker_{H^m(\Omega)}P$: **APERTO** (C12-Q3; in $\ker_{C^\infty}$ CON-FONTE Malgrange).
3. **Funzioni speciali / Green.** Nucleo del calore $G(t,x)=(4\pi Dt)^{-1/2}e^{-x^2/4Dt}$; polinomi di Hermite: $v_n(-s,x)$ ortogonali in $L^2(G_s)$ con norme $(2s)^nn!$ (R1-P11, ritrovato in T6(v)).
4. **Decomposizione.** Strato fattori banale ($\delta=0$, nessuna ambiguità) [C12-P3]. Termini dentro il fattore: evoluzione del 1° ordine in $t$ ⇒ log-simbolo $a(\xi)=D\xi^2$ (S-P1).
5. **Dati per C1.** $\mathcal H_P=\ker_{H^m}P$ è un RKHS per $m\ge2$ con nucleo $K_P(\cdot,w)=\Pi_Pk_m(\cdot,w)$ = Green del problema d'energia vincolato a $\ker P$ [C12-T5(a),(b)]; forma chiusa di $K_P$: APERTO. Nucleo della norma di Fock: $\sum_nv_n(z)\overline{v_n(z')}/(n!\rho^{2n})$ (forma chiusa tipo Mehler: da verificare). Duale biortogonale: $\delta_n(u)=\partial_x^nu(0,x_0)/n!$, rappresentante $v_n/w_n$ [T6(iii)]. Gram di esponenziali: gram.md §1.
6. **Asse 4.** S1[ord=(1,2); lin; $P=\tau-D\xi^2$; parabolico; coeff. costanti; scalare] S3[$V(P)$ = parabola; vel. infinita] S5[base num. (Appell/RW); duale = coeff. di Taylor in $x$ a $t=0$] S6[regolarizzante; backward no] S13[identificabile ⟺ $u\notin$ EP].
7. **Identificabilità.** $P$ irriducibile ⇒ $\mathrm{Ann}(u)=(P)\iff u\notin\mathrm{EP}(\Omega)$ (C3-T1(a) con $P/P_1=1$, work/C3).
8. **Fonti.** Rosenbloom–Widder, Trans. AMS 92 (1959) (polinomi del calore; da verificare pagina); Widder, *The Heat Equation* (1975) cap. 9–10 (da verificare); research/R1 (P11), R3 K4, PR-C2b C2.07.
9. **SymPy.** `c12_catalog.py` CA: $e^{\zeta x+\zeta^2t}$ e $v_0..v_5$ in $\ker P$, irriducibilità (8 PASS); `c12_appell.py` calore (RW, ortogonalità $L^2(G_s)$, stima di crescita). Non verificato: densità di $\mathcal F$, forma chiusa di $K_P$.
Stato: DIMOSTRATO per i punti 1, 4 (elementari); prova scritta (audit non richiesto) per 2, 5 (C12-T5, T6); APERTO densità e nucleo in forma chiusa.

---
# C2.06 / K3 — Trasporto $\partial_t+c\partial_x$   [★]
1. **Operatore e simbolo.** $P=\tau+c\xi$, $c\in\mathbb R$. Irriducibile: una sola componente [C12-P3].
2. **Nucleo e classe.** $\ker_{\mathcal D'(\Omega)}P=\{F(x-ct)\}$ (C12-L5, versione su convesso). In $L^2(\Omega)$: con $s=x-ct$ (determinante 1), $\|F(x-ct)\|^2_{L^2(\Omega)}=\int_S|F(s)|^2\ell(s)\,ds$, $\ell(s)$ = lunghezza della corda caratteristica (Fubini); per $c\ne0$ il peso $\ell$ si annulla ai due estremi di $S$ (angoli del rettangolo). In $H^m$: $\partial_s^jF$ con lo stesso peso. Base di Appell ($q=1$): $v_n=(x-x_0-ct)^n$, peso $w_n=\rho^{2n}$; $\mathcal F_{-c\xi,\rho}$ = funzioni $F$ olomorfe nel disco $|s-x_0|<\rho$ con coefficienti di Taylor in $\ell^2_w$ (spazio di Hardy riscalato).
3. **Funzioni speciali / Green.** Soluzione fondamentale $\delta(x-ct)H(t)$.
4. **Decomposizione.** Strato fattori banale [C12-P3]. Nessun termine da separare oltre $\partial_t$ e $c\partial_x$ (log-simbolo $a=-c\xi$, lineare).
5. **Dati per C1.** Nucleo di Fock in forma chiusa: $\sum_n\frac{(s-x_0)^n\overline{(s'-x_0)}^n}{\rho^{2n}}=\frac{\rho^2}{\rho^2-(s-x_0)\overline{(s'-x_0)}}$, $s=x-ct$ (Szegő riscalato; SymPy TR). $\mathcal H_P=\ker_{H^m}P$ RKHS ($m\ge2$) [T5]. **Coppie di trasporti** (due fattori paralleli $\partial_t+c\partial_x-d_i$): somma chiusa $\iff$ corde di lunghezza $\inf>0$; sul rettangolo con $c\ne0$: $c_F=1$ [C12-T3]; per $c=0$: $c_F=\sqrt{\tanh(\cdot)/(\cdot)}$ esplicito (gram.md §3).
6. **Asse 4.** S1[ord=(1,1); lin; $P=\tau+c\xi$; iperbolico; coeff. costanti] S3[$V(P)$ retta; vel. $c$ finita] S5[base num. (monomi in $x-ct$); duale = Taylor] S6[non regolarizzante; backward sì] S13[identificabile ⟺ $u\notin$ EP].
7. **Identificabilità.** Come calore: $\mathrm{Ann}(u)=(P)\iff u\notin\mathrm{EP}$ (C3-T1(a)).
8. **Fonti.** research/R3 K3, PR-C2b C2.06; Evans, *PDE* §2.1 (da verificare).
9. **SymPy.** `c12_catalog.py` TR: $v_0..v_6$ in $\ker P$ e uguali a $(x-x_0-ct)^n$, nucleo di Fock, irriducibilità (9 PASS); `c12_gram.py` T3 (coseno → 1 per corde corte).
Stato: punti 1–4 DIMOSTRATO (elementari); 5 prova scritta (T3 in audit S-CHECK).

---
# C2.08 / K12 — Onda $\partial_t^2-\partial_x^2$   [★]
1. **Operatore e simbolo.** $P=\tau^2-\xi^2=(\tau-\xi)(\tau+\xi)$ (velocità 1; per $c$: $\tau\mp c\xi$). Due componenti $Q_\pm=\tau\mp\xi$, molteplicità 1 [C12-P2: $b^2-4c=4\xi^2$ quadrato].
2. **Nucleo e classe.** $\ker_{\mathcal D'}Q_+=\{F(x+t)\}$, $\ker Q_-=\{G(x-t)\}$; basi di Appell $v_n^\pm=(x-x_0\pm t)^n$ (Fock con $q=1$, come il trasporto).
3. **Funzioni speciali / Green.** $E=\tfrac12H(t-|x|)$; d'Alembert.
4. **Decomposizione.** $\ker P=\ker Q_++\ker Q_-$ in $\mathcal D'(\Omega)$, $C^\infty(\Omega)$ [C12-T1]; ambiguità $\ker Q_+\cap\ker Q_-=\mathbb C$ (costanti), $\delta=\dim R/(\tau-\xi,\tau+\xi)=1$. Proiettore di Vandermonde (d'Alembert): $\partial_xu_+=\tfrac12(\partial_x+\partial_t)u$, $\partial_xu_-=\tfrac12(\partial_x-\partial_t)u$ [C12-T2], $\Delta=-2\xi$; non comassimale ⇒ nessun proiettore polinomiale (II-T3). **In $H^m$**: sul quadrato la scomposizione è globale per ogni $m$ e $c_F<1$ sui complementi delle costanti [C12-P4(b)]; su un rettangolo qualsiasi: APERTO (la prova di P4(b) usa il quadrato; si attende lo stesso esito: caratteristiche trasversali). Termini: 2° ordine in $t$ ⇒ algebra di Lie della compagna $\mathfrak{sl}_2$ (II-P6, work/II).
5. **Dati per C1.** $\mathcal H_\pm=\ker_{H^m}Q_\pm$; somma di Aronszajn $=\ker_{H^m}P$ sul quadrato, norme equivalenti [T5(e)]; split di energia minima ortogonale a $\mathcal N=\{(k,-k)\}$. Gram e $c_F$: gram.md §2.
6. **Asse 4.** S1[ord=(2,2); lin; iperbolico; coeff. costanti] S3[$V(P)$ = due rette; vel. 1] S5[base num. per fattore; duale Taylor] S6[non regolarizzante; backward sì] S13[identificabile ⟺ $(\partial_t\pm\partial_x)u\notin$ EP].
7. **Identificabilità.** $P$ ridotto: $\mathrm{Ann}(u)=(P)\iff(\partial_t+\partial_x)u\notin\mathrm{EP}$ e $(\partial_t-\partial_x)u\notin\mathrm{EP}$ (C3-T1(a)); la componente $u_\pm$ identifica $Q_\pm$ $\iff u_\pm\notin$ EP (S-C3, C3-C2). Controesempio di S-C3: $u=e^{x-t}+e^{-(x+t)^2}$ ha t-jet non libero.
8. **Fonti.** research/R3 K12, PR-C2b C2.08; Evans §2.4 (da verificare).
9. **SymPy.** `c12_catalog.py` ON: fattorizzazione, $v_n^\pm$ ($n\le5$) nei nuclei, $\dim R/(Q_+,Q_-)=1$ (8 PASS); `c12_factors.py` T1/T2 (d'Alembert); `c12_gram.py` P4 (controllo).
Stato: 1, 4 ($\mathcal D'$) prova scritta in audit (C12-T1, T2); 4 ($H^m$ quadrato) prova scritta (P4); rettangolo generale APERTO.

---
# C2.33 / K11 — Trave di Euler–Bernoulli $\partial_t^2+\partial_x^4$   [★]
1. **Operatore e simbolo.** $P=\tau^2+\xi^4=(\tau-i\xi^2)(\tau+i\xi^2)$; due componenti (rami di Schrödinger $\partial_t\mp i\partial_x^2$), molteplicità 1 [C12-P2: $b^2-4c=-4\xi^4=(2i\xi^2)^2$].
2. **Nucleo e classe.** $\ker Q_\pm$ = soluzioni di Schrödinger libero $u_t=\pm iu_{xx}$; basi di Appell $v_n^\pm=e^{\pm it\partial_x^2}(x-x_0)^n$ ($q=2$, $\alpha_2=\pm i$), spazi di Fock $\mathcal F_{\pm i\xi^2,\rho}$ con $w_n=n!\rho^{2n}$, contenenti tutti gli esponenziali $e^{\zeta x\pm i\zeta^2t}$ [C12-T6]. **No-go**: nessun peso positivo su una sezione temporale rende ortogonale la base di Appell (CON-FONTE Shohat, C12-P6): la norma di Fock è il sostituto.
3. **Funzioni speciali / Green.** Nucleo di Schrödinger $(4\pi it)^{-1/2}e^{ix^2/4t}$ per ramo (PR-C2c C2.33: trave = coppia di Schrödinger, R3).
4. **Decomposizione.** $\ker P=\ker Q_++\ker Q_-$ in $\mathcal D'$, $C^\infty$ [C12-T1]; ambiguità $\ker Q_+\cap\ker Q_-=\mathrm{span}\{1,x\}$, $\delta=\dim R/(\tau-i\xi^2,\tau+i\xi^2)=\dim R/(\tau,\xi^2)=2$. Vandermonde: $\Delta=-2i\xi^2$, $\partial_x^2u_+=\tfrac12(\partial_x^2u-i\partial_tu)$, $\partial_x^2u_-=\tfrac12(\partial_x^2u+i\partial_tu)$ [C12-T2]. Regolarità interna: componenti in $H^{m-1}_{loc}$ (C12-T4 con $r=\xi^2$, $s=\tau$; non ottimale). **In $H^m$ globale**: APERTO (C12-Q1). Termini: compagna con algebra di Lie $\mathfrak{sl}_2$ (II-P6).
5. **Dati per C1.** $\mathcal H_\pm$ RKHS ($m\ge2$); somma di Aronszajn $H_K\subseteq\ker_{H^m}P$ con uguaglianza ⟺ scomposizione globale (APERTO); $c_F$: APERTO, congettura $c_F<1$ (gram.md §2).
6. **Asse 4.** S1[ord=(2,4); lin; $P=\tau^2+\xi^4$; dispersivo (non di Kovalevskaya in $x$); coeff. costanti] S3[$V(P)$ = due parabole immaginarie; vel. infinita] S5[base num. per fattore; duale Taylor; pesi $L^2$ positivi impossibili] S6[non regolarizzante; backward sì] S13[identificabile ⟺ $(\partial_t\pm i\partial_x^2)u\notin$ EP].
7. **Identificabilità.** $P$ ridotto: $\mathrm{Ann}(u)=(P)\iff(\partial_t\pm i\partial_x^2)u\notin\mathrm{EP}$ (C3-T1(a)).
8. **Fonti.** research/R3 K11, PR-C2c C2.33; Shohat, Amer. J. Math. 58 (1936) (da verificare, CIT-AUDIT).
9. **SymPy.** `c12_catalog.py` TV: fattorizzazione, $v_n^\pm$ ($n\le5$) nei nuclei di $Q_\pm$ e di $P$, $\dim=2$, $1,x$ nei due nuclei (9 PASS); `c12_factors.py` T2 ($\Delta=-2i\xi^2$); `c12_appell.py` ramo $i\xi^2$.
Stato: 4 ($\mathcal D'$) prova scritta in audit; $H^m$ globale e $c_F$ APERTO.

---
# C2.12 — Avvezione–diffusione $\partial_t+c\partial_x-D\partial_x^2$   [★]
1. **Operatore e simbolo.** $P=\tau+c\xi-D\xi^2$ ($c\in\mathbb R$, $D>0$). Irriducibile: **una sola componente** (O1/G8 confermato, C12-P3; concorda con S-TROP).
2. **Nucleo e classe.** Fattore di evoluzione $\tau-a(\xi)$, $a(\xi)=-c\xi+D\xi^2$, $q=2$. Base di Appell $v_n=e^{t a(\partial_x)}(x-x_0)^n$; Fock $\mathcal F_{a,\rho}$ con $w_n=n!\rho^{2n}$ [C12-T6]. Il cambio galileiano $s=x-ct$ porta $\ker P$ su $\ker(\partial_t-D\partial_s^2)$ (sul dominio trasformato, che non è più un rettangolo). $\mathcal F$ contiene **tutti** gli esponenziali di $V(P)$, compresi quelli reali; in particolare lo strato limite $e^{cx/D}=e_\zeta$ con $\zeta=c/D$, $a(\zeta)=0$, $\|e_\zeta\|^2_{\mathcal F}=e^{\rho^2c^2/D^2}$ [T6(iv)].
3. **Funzioni speciali / Green.** $G(t,x)=(4\pi Dt)^{-1/2}e^{-(x-ct)^2/4Dt}$.
4. **Decomposizione.** Strato fattori banale: $\delta=0$, $E_{int}^{ker}$ **per fattori** $=0$. Lo split **per termini** $\ker(\partial_t+c\partial_x)+\ker(\partial_t-D\partial_x^2)$ non è uno split per fattori e non contiene $e^{cx/D}$ (§AD-s, punto 4). Termini dentro il fattore: log-simbolo $a=-c\xi+D\xi^2$ (S-P1); facce del poligono di Newton (S-TROP): trasporto $\tau+c\xi$, diffusione $\tau-D\xi^2$, stazionaria $c\xi-D\xi^2$ (sotto-scheda AD-s).
5. **Dati per C1.** $\mathcal H_P=\ker_{H^m}P$ RKHS ($m\ge2$) [T5]; un solo fattore ⇒ $H_K=\mathcal H_P$, norme uguali. Gram interno al fattore tra la classe stazionaria e le costanti: AD-s punto 5.
6. **Asse 4.** S1[ord=(1,2); lin; parabolico; coeff. costanti] S3[$V(P)$ parabola; vel. infinita] S5[base num. (Appell q=2); duale Taylor] S6[regolarizzante; backward no] S10[ε = 1/Pe, Pe = cL/D] S13[identificabile ⟺ $u\notin$ EP].
7. **Identificabilità.** $\mathrm{Ann}(u)=(P)\iff u\notin\mathrm{EP}$; lo strato limite da solo ($u=e^{cx/D}$, EP) **non** identifica $P$: $\mathrm{Ann}(e^{cx/D})=(\tau,\xi-c/D)$ (C3-T1, C3-C2).
8. **Fonti.** research/PR-C2b C2.12; work/SCOUT-TROP/VERDETTO.md (TROP-7: lato stazionario); Rosenbloom–Widder 1959 per il caso $c=0$.
9. **SymPy.** `c12_catalog.py` AD: irriducibilità, $v_0..v_4$ in $\ker P$, $a(c/D)=0$, più i controlli di AD-s (14 PASS in tutto); `c12_appell.py` AD ($u_t=-2u_x+3u_{xx}$).
Stato: 1, 4 DIMOSTRATO (elementari); 2, 5 prova scritta (T5, T6).

## AD-s — Lato stazionario $c\partial_x-D\partial_x^2$ di AD (sotto-equazione a due termini; richiesta S-TROP)   [★, sotto-classe]
1. **Operatore e simbolo.** Sotto-equazione $\{P=0,\ \tau=0\}$: l'ideale $(P,\tau)=(\tau,\ \xi(D\xi-c))$; la faccia $c\xi-D\xi^2$ del poligono di Newton di $P$ (S-TROP).
2. **Nucleo e classe.** $\ker P\cap\ker\partial_t=\mathrm{Sol}(R/(P,\tau))=\mathrm{span}\{1,\ e^{cx/D}\}$, dimensione $\dim R/(P,\tau)=2$, fatta di EP, la stessa su ogni rettangolo [C12-L2(2),(3)]. Su $\Omega$ limitato $e^{cx/D}\in H^m(\Omega)$ per ogni $m$ (EP). Classe **a dimensione finita**, dentro l'unico fattore: non è un fattore a sé ($V(P,\tau)=\{(0,0),(0,c/D)\}$ finito).
3. **Funzioni speciali.** Strato limite $e^{cx/D}=e^{\mathrm{Pe}\,x/L}$ (spessore $D/c=L/\mathrm{Pe}$).
4. **Decomposizione.** (a) Per fattori: nessuna (un fattore). (b) **Per termini**: $e^{cx/D}\notin\ker(\partial_t+c\partial_x)+\ker(\partial_t-D\partial_x^2)$ su nessun aperto. *Prova.* Se $e^{cx/D}=F(x-ct)+h$ con $(\partial_t-D\partial_x^2)h=0$ ($F,h\in\mathcal D'$), applicando $\partial_t-D\partial_x^2$: $-\tfrac{c^2}{D}e^{cx/D}=(\partial_t-D\partial_x^2)F(x-ct)$; applicando poi $\partial_t+c\partial_x$ (che commuta e annulla ogni funzione di $x-ct$): $-\tfrac{c^3}{D^2}e^{cx/D}=0$, assurdo per $c\ne0$. ∎ Quindi la classe AD-s contribuisce a $E_{int}^{ker}$ **dello split per termini** (S-TROP, S-P1), non dello split per fattori.
5. **Dati per C1.** Gram di $\{1,e^{cx/D}\}$ in $L^2(\Omega)$ (le funzioni non dipendono da $t$; il fattore $|I|$ si semplifica, e una traslazione di $J$ non cambia il coseno): $\langle1,1\rangle=L$, $\langle1,e\rangle=\tfrac Dc(e^{\mathrm{Pe}}-1)$, $\langle e,e\rangle=\tfrac D{2c}(e^{2\mathrm{Pe}}-1)$, e
$$\cos^2\angle(1,e^{cx/D})=\frac{\tanh(\mathrm{Pe}/2)}{\mathrm{Pe}/2},\qquad \mathrm{Pe}=cL/D,$$
$\to1$ per $\mathrm{Pe}\to0$ (strato limite indistinguibile dalle costanti), $\to0$ per $\mathrm{Pe}\to\infty$ (asintoticamente ortogonale). Nucleo riproducente della classe (dim 2): $K(x,y)=\sum_{a,b}(\Gamma^{-1})_{ab}\phi_a(x)\overline{\phi_b(y)}$, $\phi=(1,e^{cx/D})$, $\Gamma$ la Gram sopra.
6. **Asse 4.** S1[ODE in $x$ del 2° ordine; lin] S5[base finita {1, e^{cx/D}}] S10[ε = 1/Pe].
7. **Identificabilità.** Una soluzione di questa classe è EP ⇒ non identifica $P$ (C3-C2); identifica solo l'ideale $(\tau,\xi(D\xi-c))$ se ha entrambe le componenti.
8. **Fonti.** work/SCOUT-TROP/VERDETTO.md TROP-7; inbox/S-C1C2.md (AVVISO S-TROP 25/10).
9. **SymPy.** `c12_catalog.py` AD: $e^{cx/D}\in\ker P\cap\ker\partial_t\cap\ker(c\partial_x-D\partial_x^2)$; base di Gröbner $(\tau,\xi^2-\tfrac cD\xi)$ e $\dim=2$; $a(c/D)=0$; formula $\cos^2=\tanh(\mathrm{Pe}/2)/(\mathrm{Pe}/2)$ e limiti; impossibilità dello split per termini (identità chiave).
Stato: DIMOSTRATO (elementare, prova qui) per 2, 4, 5; 2 usa C12-L2 (in audit).
