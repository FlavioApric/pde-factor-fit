# AUDIT S10-COL (27/10/2026)

Auditor: S-CHECK-COL. Oggetto: `work/S10-COL/PROOF_PACKAGE.md` (S10COL-L1, -L2, -L3, -TA, -TB, -TC e il §5, cioè il Passo B sostitutivo di S10A-T3), `work/S10-COL/LEDGER_ROWS.md` e `work/S10-COL/sympy/`. Contesto letto: `work/S10-OPEN-A/PROOF_PACKAGE.md` §3 (S10A-T3), `work/CHECK-F10/AUDIT_S10-OPEN-A.md` (fix A-7) e `research/CIT-AUDIT/AUDIT-COL.md`.

Controlli indipendenti: `work/CHECK-F10/sympy/col_sym.py` → `col_sym.out` (12/12 OK) e `work/CHECK-F10/sympy/col_kill.py` → `col_kill.out` (TUTTO OK, negativi compresi). Li ho eseguiti con `D:\ProblemaBase\.venv\Scripts\python.exe -I`. Ho rieseguito a mano anche gli script del prover: le uscite combaciano con i file `.out`.

## Verdetti

| claim | verdetto | fix | stato proposto |
|---|---|---|---|
| S10COL-L1 ($D(p)$ è un cono convesso aperto) | **PASS** | — | DIMOSTRATO |
| S10COL-L2 (cono di carta ⊂ $D(p)$) | **PASS** | — | DIMOSTRATO |
| S10COL-L3 (dalla direzione alle traiettorie) | **PASS** | — | DIMOSTRATO |
| S10COL-TA (campo di carta entrante) | **PASS** | — | DIMOSTRATO |
| S10COL-TB ($V\cdot\nu\ge\kappa$ q.o. ⟹ $-V(p)\in D(p)$ ovunque) | **PASS-con-fix** (redazionale) | COL-1 | DIMOSTRATO |
| S10COL-TC = (COL-ii) | **PASS** | — | DIMOSTRATO (con TA oppure TB) |
| §5, Passo B sostitutivo di S10A-T3 | **PASS-con-fix** (redazionale) | COL-2, COL-3 | — |
| S10A-T3 dopo la sostituzione | **PASS-con-fix** (redazionale) | COL-2, COL-3, più A-7(b),(c) già prescritti | **DIMOSTRATO mod F1, F2**, senza [COL] |
| [COL] | (COL-ii): DIMOSTRATO tramite S10COL-TC. (COL-i): CON-FONTE (Grisvard 1.5.1.9), invariato e non più usato da S10A-T3 | — | — |

Il kill-argument non ha trovato controesempi (§11). Tutti i fix sono redazionali e nessuno tocca la logica.

---

## 1. §0 (convenzioni e fatti elementari)

- La definizione di carta è corretta: $C$ è un aperto qualsiasi, non per forza un cilindro, e $\Omega\cap C=\{y_n>g(y')\}\cap C$. L'estensione di McShane conserva la costante, quindi lavorare con $g$ definita su tutto $\mathbb R^{n-1}$ non costa nulla. Distanze e palle sono invarianti per l'isometria $R$, quindi i conti in coordinate di carta sono leciti.
- (F1) è corretta, e serve davvero che $C$ sia aperto (i punti $x_k\in\Omega$ cadono definitivamente in $C$).
- (F2): per $|z-x|<m:=\min(b/\sqrt{1+L^2},\mathrm{dist}(x,\complement C))$ si ha $z\in C$ e $z_n-g(z')\ge b-\sqrt{1+L^2}|z-x|>0$, quindi $B(x,m)\subset\Omega$ e $\mathrm{dist}(x,\complement\Omega)\ge m$. Corretta. L'identità usata è (S2) del prover; l'ho ricontrollata.
- (F3) è corretta.

## 2. S10COL-L1 e la definizione quantitativa di $D(p)$ — PASS

**Definizione 1.1.** $D(p)$ è definito solo da Ω e p: le carte non compaiono. L'uniformità è quella giusta per il Teorema C: la stima vale per tutti gli $x\in\bar\Omega$ vicini a p (quindi anche per i punti di bordo vicini, non solo per p), per tutte le velocità $u$ vicine a $w$ e con una costante lineare in t. Questo è esattamente ciò che serve a L3, dove la velocità media $u=\frac1t\int_0^tW(\psi_s x)\,ds$ è solo vicina a $W(p)$.

$0\notin D(p)$: con $x=p$ e $u=0\in B(0,r)$ si avrebbe $\mathrm{dist}(p,\complement\Omega)\ge at>0$, mentre $p\in\partial\Omega\subset\complement\Omega$. L'argomento del pacchetto ("una palla di centro p starebbe in Ω") è equivalente.

**(i) Apertura.** Con testimone $(r/2,a)$, $B(\tilde w,r/2)\subset B(w,r)$ e $B(p,r/2)\subset B(p,r)$. Corretta.

**(ii) Omogeneità.** Con $\rho=\min(r,\lambda r,r/\lambda)$ si ha $|u/\lambda-w|<\rho/\lambda\le r$ e $\lambda t\le\lambda\rho\le r$. Corretta (col_sym "L1(ii)"). Il termine $\lambda r$ nel minimo non serve, ma è innocuo.

**(iii) Somma.** È il punto 1 della lista del prover. La scomposizione $u_k=w_k+\tfrac12(u-w_1-w_2)$ dà $|u_k-w_k|<\rho/2\le r_k$. Il punto $x_1=x+tu_1$ soddisfa $\mathrm{dist}(x_1,\complement\Omega)\ge a_1t>0$, quindi $x_1\in\Omega\subset\bar\Omega$: è questo che permette di riapplicare il testimone di $w_2$ partendo da $x_1$. Inoltre $|x_1-p|<\rho+\rho(|w_1|+\rho/2)\le\rho(2+|w_1|)\le r_2$; la differenza è $\rho(1-\rho/2)\ge0$ per $\rho\le1$ (col_sym "L1(iii)"). Infine $x_1+tu_2=x+tu$, e il testimone è $(\rho,a_2)$. Corretta.

**Combinazioni.** Si tolgono i coefficienti nulli e si procede per induzione con (ii) e (iii). Corretta.

**(i) del mandato, in sintesi.** $D(p)$ è un cono convesso aperto, non contiene 0 e contiene il cono di ogni carta per p (L2). L'enunciato non ne afferma la non vuotezza: per Ω lipschitziano la dà L2, e il pacchetto mostra (Oss. 4.2) che fuori dai lipschitziani può essere vuoto. Ho controllato anche il two-brick, che è vuoto in un punto (K3, §11).

## 3. S10COL-L2 — PASS

È il punto 2 della lista del prover. Si ha $r\le d/(2(2+|z|))<d$, quindi $x\in C$ e (F1) si applica. Poi $|y-p|<r(2+|z|)\le d/2$ (col_sym "L2": la differenza è $r(1-r)\ge0$), da cui $\mathrm{dist}(y,\complement C)>d/2$. Si ha $u_n-L|u'|\ge\delta-\sqrt{1+L^2}|u-z|\ge\delta/2$ e $y_n-g(y')\ge t(u_n-L|u'|)\ge t\delta/2$. Per (F2), e poiché $t\le r\le1$, la distanza è $\ge t\min(\delta/(2\sqrt{1+L^2}),d/2)$. La direzione $e$ ha coordinate $(0,1)$, quindi sta in Γ. Corretta. Nota: se $C=\mathbb R^n$, allora $d=\infty$ e il vincolo sparisce; nessun problema.

## 4. S10COL-L3 — PASS

Si ha $|\psi_s x-p|<\rho_p(1+M)\le\eta$ per $s\le t\le\rho_p$, quindi $|u-W(p)|\le r/2$. Inoltre $x\in B(p,r)$ e $t\le r$. Il testimone si applica al punto finale $x+tu=\psi_t(x)$. Corretta. Basta che W sia continuo e a supporto compatto ($M<\infty$); la classe $C^1$ serve solo per il flusso.

## 5. S10COL-TA — PASS

Se $\theta_i(p)>0$, allora $p\in\mathrm{supp}\,\theta_i\subset C_i$, quindi $e_i\in D(p)$ per L2. Ne segue $W(p)=\sum_{I(p)}\theta_i(p)e_i\in D(p)$ per L1, con $I(p)\neq\emptyset$ per ipotesi.

**Ruolo di $\theta_i\ge0$.** È essenziale. Con un $\theta_j(p)<0$, il termine $\theta_j(p)e_j$ è un multiplo negativo di una direzione entrante, che non sta in $D(p)$, e la somma può uscire dal cono. Il controllo negativo K4neg1 (una direzione invertita, equivalente a un coefficiente negativo) produce 39 uscite. L'ipotesi è nell'enunciato, quindi non c'è un fix su TA: il fix è su S10A-T3 (COL-3).

**Compatibilità tra carte.** L'osservazione del pacchetto è corretta: non serve alcuna relazione fra le carte, perché ogni $e_i$ attivo in p sta nello stesso cono intrinseco $D(p)$. L'ho stressata in K4: sul pettine con fessure strette, due carte che contengono uno stesso punto del bordo hanno direzioni a 171.9°, e palle di carte su lati opposti di una fessura, che si sovrappongono fuori dal bordo, hanno direzioni a 180°. Il risultato è 0 violazioni (§11). L'argomento finale del §7 del pacchetto è corretto: $e_i,e_j\in D(p)$ con D(p) convesso e $0\notin D(p)$ implica $e_i\neq-e_j$, quindi due direzioni di carta in uno stesso punto del bordo non sono mai esattamente opposte.

## 6. S10COL-TB — PASS-con-fix (COL-1, redazionale)

Il punto (ii) del mandato chiede se l'ipotesi q.o. implichi davvero $-V(p)\in D(p)$ nei punti di non differenziabilità. La risposta è sì: la prova non valuta mai $\nabla g$ in $p'$.

- **Ingresso nella carta.** $p=(p',g(p'))$ per (F1) e per l'apertura di $\Omega\cap C$. Corretto.
- **Passo 1.** Per $y'\in B'(p',2\delta)$ si ha $q\in B(p,\eta)$, quindi $|w-W(q)|<\kappa/4+\kappa/4=\kappa/2$. Poi $w_n-w'\cdot\nabla g\ge(\kappa-|w-W(q)|)\sqrt{1+|\nabla g|^2}\ge\kappa/2$, per Cauchy–Schwarz (S3 del prover; il minimo in $|\nabla g|=0$ è in col_sym "TB P1"). L'insieme eccezionale non dipende da w: è l'unione dei punti di non differenziabilità e di quelli dove fallisce l'ipotesi. Corretto.
- **Passo 2 (Fubini).** È il punto 3 della lista del prover. $T(x',s)=(x'+sw',s)$ ha determinante 1, quindi $T^{-1}(N\times\mathbb R)$ è nullo. N è misurabile perché la misura di Lebesgue è completa. Per Tonelli applicato alla sua indicatrice, per q.o. $x'$ la sezione $\{s:x'+sw'\in N\}$ è nulla. Il segmento resta in $B'(p',2\delta)$ (col_sym "TB P2"). $f(s)=g(x'+sw')$ è lipschitziana, quindi assolutamente continua, e nei punti di differenziabilità di g la regola della catena dà $f'(s)=\nabla g\cdot w'$. Il caso $w'=0$ è banale: serve $w_n\ge\kappa/2$, che il Passo 1 dà in un qualunque punto buono. Il passaggio a ogni $x'$ funziona perché i punti buoni hanno misura piena, quindi sono densi in $B'(p',\delta)$, e $x'\mapsto g(x'+tw')-g(x')$ è continua. **È proprio questo passaggio che copre i punti angolosi**: anche $x'=p'$, e in generale ogni $x'$ dove g non è differenziabile, ottiene la disuguaglianza per continuità dai segmenti vicini. Corretto.
- **Passo 3.** Si ha $u\in B(W(p),\kappa/4)$, e $|u'|\le|W(p)|+1$ dà $t\le\delta/(1+|u'|)$ (col_sym "TB P3"). La distanza di $y$ da $\complement C$ si stima come in L2, e $y_n-g(y')\ge t\kappa/2$. Il Passo 2 si applica con $w=u$, con un argomento di Fubini per ciascun $u$, cosa lecita perché l'insieme N non dipende da u. Corretto. Il vincolo $r<\delta$ è implicato da $r\le\delta/(2+|W(p)|)$.

**Controllo numerico mirato** (§11, K1 e K2). Ho preso $g(x)=x\sin\log|x|$: in 0 g non è differenziabile e $g'$ riempie $[-\sqrt2,\sqrt2]$ in ogni intorno di 0. Ho preso poi uno zig-zag $|x|\,\mathrm{tri}(\log_2|x|)$ con angoli che si accumulano in 0. Con campi non costanti con $\kappa>0$ q.o., il testimone in p=0 vale con margine $\ge\kappa/2$ su 400000 terne $(x,u,t)$, e i flussi uscenti dai 119 angoli e da 0 restano dentro con $(y_2-g)/t\ge0.60$. Nel caso limite, con $W(0)$ sul bordo del cono di Clarke, l'estremo inferiore essenziale di κ tende a 0 vicino al punto: l'ipotesi di TB fallisce da sola, quindi non c'è controesempio.

**Fix COL-1 (redazionale).** L'Osservazione 3.2 è dichiarata "non usata altrove". È però proprio ciò che serve per applicare TB al campo di (COL-i) nella forma geometrica delle fonti ("q.o. su ∂Ω" con la normale intrinseca), come fanno l'"Esito in breve" e la riga [COL] del ledger. Va scritto: "TB nella forma per carte non usa l'Oss. 3.2; per passare dalla forma geometrica a quella per carte si usa l'Oss. 3.2". Nella colonna "dipende da" della riga S10COL-TB va aggiunto "(Oss. 3.2 per la forma geometrica)". Ho rifatto la prova dell'Oss. 3.2: le due inclusioni del cono di Bouligand e la chiusura di $T(p)$ sono corrette, e la corrispondenza dei nulli di $\mathcal H^{n-1}$ fra le carte segue dalla bi-lipschitzianità dei grafici. Per S10A-T3 il fix è irrilevante, perché S10A-T3 usa TA.

L'Osservazione 3.3 è corretta: $e_n\cdot(-\nu)=1/\sqrt{1+|\nabla g|^2}$ (col_sym "Oss 3.3"), e il minimo di una funzione continua positiva su un compatto è positivo.

## 7. S10COL-TC — PASS

**(a).** $\sigma_1=\min_j\rho_{p_j}/2$ funziona come numero di Lebesgue: se $|x-p|<\sigma_1$ e $p\in B(p_j,\rho_{p_j}/2)$, allora $|x-p_j|<\rho_{p_j}$, e $t\le\sigma_1\le\rho_{p_j}$. I punti lontani si trattano con (F3) e con $\sigma_1-Mt\ge ct$ per $t\le\sigma_1/(M+c)$ (col_sym "TC(a)"). Le conseguenze seguono da (F3) e dalla biiettività di $\Phi_\sigma$. Corretto. Le costanti non dipendono da σ (Oss. 4.1 corretta).

**(b)** (punto (iii) del mandato e punto 4 della lista del prover). Si ha $\tau>0$ perché Ω è aperto. $y=\psi_\tau(x)\notin\Omega$: o l'estremo inferiore è raggiunto, oppure y è limite di $\psi_{t_k}x\in\complement\Omega$ con $t_k\downarrow\tau$, e $\complement\Omega$ è chiuso. $y\in\bar\Omega$ come limite per $t\uparrow\tau$. Dunque $y\in\partial\Omega$. Con $h<\min(\tau,\sigma_0)$, il punto $z=\psi_{\tau-h}(x)$ sta in Ω e (a) dà $\psi_h(z)\in\Omega$, contro $y\notin\Omega$. Contraddizione. Il prolungamento a ogni $s>0$ per $x\in\bar\Omega$ usa la proprietà di gruppo. Corretto. Osservazione: l'argomento usa solo che (a) vale su $(0,\sigma_0]$ con $\sigma_0>0$; la costante c non serve, quindi non c'è circolarità.

**(c).** $|\Phi_\sigma x-x|\le M\sigma$. $\Phi_\sigma$ è un diffeomorfismo di $\mathbb R^n$, quindi $\Phi_\sigma(\Omega)$ è aperto, omeomorfo a Ω e ha lo stesso $b_1$. Si ha $M>0$ perché $W(p)\neq0$ ($0\notin D(p)$), quindi "$C>M$" ha senso. Corretto.

## 8. §5 — Passo B sostitutivo e indipendenza di S10A-T3 da [COL] — PASS-con-fix (COL-2, COL-3)

Punto (iv) del mandato e punto 5 della lista del prover.

- **I dati del Passo 1′ sono dati del Teorema A.** I cilindri $C_i$ con $\Omega\cap C_i=\{y_2>\varphi_i(y_1)\}\cap C_i$ sono carte nel senso del §0 (Ω sta sopra il grafico, quindi $e_i$ è la direzione verticale entrante). Si ha $\theta_i\in C_c^\infty(C_i')\subset C_c^\infty(C_i)$; questo resta vero anche con la modifica A-7(b), che introduce $C_i''$ ma lascia i supporti in $C_i$. $\theta_0$ ha supporto in $\Omega_0\Subset\Omega$, quindi si annulla su ∂Ω. Da $\sum_{i\ge0}\theta_i=1$ su un intorno di $\bar\Omega$ segue $\sum_{i\ge1}\theta_i=1>0$ su ∂Ω. Il campo è una somma finita di funzioni $C_c^\infty$. Le ipotesi di TA sono quindi soddisfatte, **purché $\theta_i\ge0$**.
- **TA + TC bastano.** Il testo proposto prende σ con $M\sigma<r_\varepsilon/4$. Allora $U=\Phi_\sigma(\Omega)\subset\{\mathrm{dist}(\cdot,\bar\Omega)\le M\sigma\}\subset\{\mathrm{dist}<r_\varepsilon/4\}=V'_\varepsilon$, e $\bar\Omega\subset U$ per TC(b), oppure per TC(a) se si prende anche $\sigma\le\sigma_0$. Infine $b_1(U)=b_1(\Omega)$ per TC(c). La Precisazione (2) del Passo D resta valida: basta un σ con $M\sigma<\min_kr_{\varepsilon_k}/4$, e TC(b) evita perfino il vincolo $\sigma\le\sigma_0$.
- **Indipendenza da [COL].** La catena è L1, L2 → TA e L1(def.), L3 → TC. Usa solo compattezza, continuità, il flusso di un campo $C^\infty_c$ e i fatti (F1)–(F3). Non usa normali, Rademacher, Fubini né alcuna fonte bibliografica. Dunque S10A-T3 non dipende più né da (COL-i) né da (COL-ii). Le dipendenze residue di S10A-T3 sono quelle già registrate: F1, F2, OPF5B-T1 Passi 3–7, OPF-T4(ii).

**Fix COL-2 (redazionale, collisione di notazione).** In S10A-T3 la lettera V indica già l'intorno aperto di $\bar\Omega$ su cui $\sum\theta_i=1$ (Passo 1′), e compare in $V_\varepsilon:=\{\dots\}\cap V$ e in $V'_\varepsilon$. Il Passo B proposto chiama V anche il campo vettoriale. Va rinominato il campo, per esempio $X:=-\sum_{i\ge1}\theta_ie_i$ con flusso $\Phi^X_\sigma$, oppure l'intorno.

**Fix COL-3 (redazionale, $\theta_i\ge0$).** Nel Passo 1′ di S10A-T3 si scriva "una partizione dell'unità **non negativa** $\theta_0,\theta_i\ge0$". La costruzione standard la dà, ma TA ne ha bisogno (§5 di questo audit), quindi va detta.

**A-7.** Il fix A-7(a) (registrare S10A-T3 come condizionato a [COL]) è superato da questa sostituzione. I fix A-7(b) (ordine delle definizioni di $C_i''$ e $d_i$) e A-7(c) (prendere ε abbastanza piccolo da avere $\{\mathrm{dist}<r_\varepsilon/2\}\subset V$) restano da applicare al testo di S10A-T3: sono indipendenti da [COL] ed entrambi redazionali o di una riga. Il fix A-7(d) va rovesciato: le righe derivate (P2-Q1 "densità sui lipschitziani semplicemente connessi", OPF5B-C1(d)) perdono il condizionamento a [COL]. Per OPF5B-C1(d) cade solo il condizionamento: il suo stato di "osservazione non auditata" non cambia per effetto di questo audit.

## 9. LEDGER_ROWS.md

Le righe sono coerenti con il pacchetto. Aggiornamenti dopo questo audit:
- S10COL-L1, -L2, -L3, -TA, -TC: stato **DIMOSTRATO**; proof-checker "S-CHECK-COL PASS"; per TA e TC, kill-argument "S-CHECK-COL: sopravvissuto (col_kill K1–K4)".
- S10COL-TB: **DIMOSTRATO**, "S-CHECK-COL PASS-con-fix(COL-1)"; nella colonna "dipende da" va aggiunta l'Oss. 3.2 per la forma geometrica.
- [COL]: (COL-ii) **DIMOSTRATO** (S10COL-TC, con TA o con TB+(COL-i)); (COL-i) CON-FONTE, invariato; S10A-T3 non usa più [COL].
- S10A-T3: **DIMOSTRATO mod F1, F2**, senza [COL], a condizione che il testo di S10A-T3 incorpori il §5 con COL-2 e COL-3 e i fix A-7(b),(c). Proof-checker: "S-CHECK-COL PASS-con-fix(COL-2, COL-3)". Dipende da: OPF5B-T1 Passi 3–7, OPF-T4(ii), F1, F2, S10COL-TA, S10COL-TC.

## 10. Script del prover

- `s10col_sym.py`: le identità (S1)–(S4) sono corrette e corrispondono agli usi indicati. Va notato che (S4) verifica solo il caso scalare, ma la scomposizione è lineare, quindi basta.
- `s10col_flow.py`: l'ho riletto. Le carte di vertice sono verificate per campionamento contro il ray casting. κ è calcolato come $W\cdot n_{in}=V\cdot\nu$, e la stima con RK4 ha passo adeguato rispetto ai valori di c. Il controllo negativo è significativo. Un limite: il dominio è stellato e le carte coprono il bordo solo con le palle di vertice. Per questo ho aggiunto un dominio non stellato con angoli rientranti, fessure strette e carte di lato (K4).

## 11. Kill-argument (col_kill.py) — sopravvissuto

- **K1, tangenti oscillanti** (la "spirale" nel senso lipschitziano, cioè un grafico la cui tangente ruota infinite volte in un cono limitato): $g(x)=x\sin\log|x|$, con $g'$ che copre $[-\sqrt2,\sqrt2]$ fino a $|x|=10^{-12}$ (col_sym K1). Il campo è non costante, con κ=0.389. Il testimone di $W(0)\in D(0)$ ha margine 0.644 ≥ κ/2 su 400000 terne. Il flusso da 3001 punti di bordo, compreso 0, ha $(y_2-g)/t\ge0.674$. Nel caso limite $W(0)=(1,\sqrt2)/\sqrt3$, sul bordo del cono di Clarke, κ vale circa $10^{-10}$ su ogni intorno di 0: l'ipotesi fallisce da sola. Una vera spirale che si avvolge infinite volte non è un grafico lipschitziano in alcuna direzione, perché le tangenti coprirebbero tutto $S^1$, quindi è esclusa dalle ipotesi; in quel caso $D(p)=\emptyset$ con lo stesso argomento della fessura (Oss. 4.2).
- **K2, angoli che si accumulano**: zig-zag $0.4|x|\,\mathrm{tri}(\log_2|x|)$, con $|g'|\le0.777$. Il campo è non costante, con κ=0.383. Il flusso dai 119 angoli (fino a $2^{-30}$) e da 0 ha $(y_2-g)/t\ge0.599$.
- **K3, two-brick** in $\mathbb R^3$, nel punto $(1,1,0)$. Nessuna delle 20000 direzioni entra da entrambe le facce $z=0$ vicine a p, quindi $D(p)=\emptyset$, coerente con il fatto che il two-brick non è lipschitziano. Inoltre $\max_w\min_{\text{facce}}w\cdot\nu=0$: le normali $\pm e_3$ si accumulano in p, quindi nessun campo continuo ha $V\cdot\nu\ge\kappa>0$ q.o. Le ipotesi di TA e di TB falliscono entrambe: nessun controesempio.
- **K4, pettine** (non stellato, 12 angoli rientranti, fessure di larghezza 1 e 0.15). Carte di vertice e di lato (119 e 289), con direzioni casuali al 3%/97% del cono ammissibile e pesi casuali in [0.2, 1], che non sommano a 1. Le carte di vertice sono verificate: 0 disaccordi. Il ricoprimento dà $\min\sum\phi\approx0.21$, e $\kappa\approx10^{-2}$. Direzioni di carte con un punto di bordo comune formano fino a 171.9°. Su 5296 punti iniziali, 0 violazioni, con $c_{emp}=\kappa$ entro il 1%.
- **Controlli negativi.** Una direzione di carta invertita (che equivale a un $\theta_i<0$) dà 39 uscite. Direzioni tangenti su un lato danno κ=0 e $c_{emp}\approx10^{-16}$: si perde l'uniformità, come previsto.

Conclusione del kill-argument: nessun dominio lipschitziano tra quelli provati (tangenti oscillanti, angoli che si accumulano, angoli rientranti con fessure strette e carte quasi opposte) produce un campo con $V\cdot\nu\ge\kappa$ q.o., o un campo di carta con $\theta_i\ge0$, che non entri uniformemente. Gli unici fallimenti osservati violano un'ipotesi: il dominio non è lipschitziano (two-brick), oppure $\theta_i<0$, oppure $\kappa=0$.
