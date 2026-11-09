# AUDIT_S10-OPEN-A — S-CHECK-F10-A (27/10/2026)

Revisore: S-CHECK-F10-A, indipendente da S10-OPEN-A. Ho letto `skills-local/claim-lifecycle/SKILL.md` e, in sola lettura, `_vendor/.../proof-checker/SKILL.md`, di cui uso la tassonomia degli errori. Ho letto anche i cinque file di `work/S10-OPEN-A/` e i suoi script SymPy, le righe citate di `claims/LEDGER.md` (14, 16, 17, 57, 58, 61, 64, 67, 70, 75, 80, 110, 111, 114, 137, 138, 140, 146–149, 151, 152, 154, 156, 166, 167, 170, 182, 291) e le loro sedi: `work/OP-ANA/PROOF_PACKAGE.md` §4, `work/OP-F5B/PROOF_PACKAGE.md` §1, `work/P1/PROOF_PACKAGE.md` P1-D1 e P1-T5, `NOTAZIONE.md` riga 44. Non ho eseguito nessuno script di `_vendor`.

Le verifiche SymPy sono indipendenti e scritte da me. Gli script stanno in `work/CHECK-F10/sympy/` e sono stati eseguiti con `.venv\Scripts\python.exe -I`:
- `a_q6.py`: 8/8 OK. Identità RD sui modi, lemma L1(ii) con due costanti, intreccio $Q(e^{\kappa t}f)=e^{\kappa t}Q'f$, stima di Leibniz, dicotomia numerica RD/ADR su una famiglia di modi diversa da quella di S10 ($\zeta=a+i\sqrt{a^2-a}$, $a<0$) e su modi oscillanti.
- `a_q7.py`: 16/16 OK. Hankel destra e sinistra, quadratura di Gauss (kill-argument), automorfismo di Weyl su funzioni test, Passo 3 in un'algebra libera troncata (parola $YXYX$, $\alpha=1$, $\beta=-1$).
- `a_p2q1.py`: 8/8 OK. Flussi sull'anello, ${*dz}=-i\,dz$, ${*d\log|z|}=d\arg z$, $\delta(\Delta)=1$, test Monte Carlo del Passo 2′ su un sopra-grafico lipschitziano (200000 punti, 0 violazioni).

## 1. Tabella degli esiti

| claim | verdetto | fix | stato proposto |
|---|---|---|---|
| S10A-L1 | PASS | — | DIMOSTRATO |
| S10A-T1 | PASS-con-fix | A-2 | DIMOSTRATO |
| S10A-C1 | PASS-con-fix | A-3 | DIMOSTRATO |
| P1-Q6 (enunciato letterale) | PASS (la confutazione regge) | A-1, A-3 | FALSO (controesempio: reazione–diffusione); la forma "≥ 2 monomi di grado ≥ 1" è DIMOSTRATO (OPA-T3(b) + S10A-T1); P1-Q6-ND resta APERTO e non fa parte dell'enunciato |
| S10A-T2 | PASS-con-fix (kill-argument: sopravvive) | A-4, A-5 | DIMOSTRATO |
| P1-Q7 | PASS-con-fix | A-6 | APERTO — ridotto ad algebre con (H) senza dilatazione pesata (Dil); sotto (Dil) DIMOSTRATO (S10A-T2) |
| S10A-T3 | PASS-con-fix sulla parte logica; dipende da una fonte non verificata | A-7 | APERTO — ridotto a [COL] (campo trasversale/collare per lipschitziani). Diventa CON-FONTE (DIMOSTRATO mod [COL]) solo dopo che CIT-AUDIT avrà verificato la fonte |
| S10A-P1 | PASS-con-fix | A-8 | DIMOSTRATO per l'anello, (i) completo. (ii): DIMOSTRATO, con la premessa topologica CON-FONTE Rudin RCA 13.11 (già PARZIALE in CIT-AUDIT-3) oppure resa elementare con A-8 |
| P2-Q1, OPF-Q3 (riga aggregata) | PASS-con-fix | A-9 | convessi: DIMOSTRATO (OPF5B-T1, invariato); domini con buchi: FALSO come enunciato universale (S10A-P1); lipschitziani semplicemente connessi: APERTO — ridotto a [COL]; non lipschitziani e codimensione esatta: APERTO |
| C12-P7, "chiusa ma non densa" | PASS | — | DIMOSTRATO (esempio differenziale: S10A-P1(i), $m\ge1$) |
| S10A-L2 | PASS | — | DIMOSTRATO |
| S10A-C2 | PASS | — | DIMOSTRATO |
| C12-Q2 = OPF-Q2 | PASS | A-10 (solo dicitura) | APERTO — ridotto a terne con ≥ 2 coppie $\Pi_i\Pi_j$ non compatte (S10A-C2), fuori dai trasporti reali (OPR2-T2) |
| C3-Q1 | PASS-con-fix | A-11 | DIMOSTRATO come classificazione per modello di dati (composizione di righe DIMOSTRATO; M3-hol mod (AC)) |
| §0: righe "già chiuse" | PASS-con-fix | A-1, A-12 | vedi §3: tutte confermate |

## 2. Audit dei claim nuovi

### S10A-L1 — PASS
Ipotesi complete: rettangolo, classe 𝔅 di P1-D1, termini $a_n$ non costanti, costanti $c_k$. (i) L'intreccio $Q(\partial)(e^{\kappa s}v)=e^{\kappa s}Q'(\partial)v$ è corretto (a_q6 (3)). La stima di Leibniz è corretta con la norma di P1-D1, $\sup_{i,j}\rho^{-i-j}\|\partial_t^i\partial_x^jw\|$: $\sum_l\binom il|\gamma|^l\rho^{i-l+j}=(\rho+|\gamma|)^i\rho^j\le(\rho+|\gamma|)^{i+j}$, con il fattore $e^{|\gamma|T}$ (a_q6 (5)). L'inversa è la moltiplicazione per $e^{-\kappa s}$, quindi $M$ è una biiezione. (ii) Verificato simbolicamente (a_q6 (2)). (iii) La traccia in $t_0$ è limitata $H^1(\Omega)\to L^2(J)$: è il teorema di traccia standard sul rettangolo (P1-L1(d) va bene).

### S10A-T1 — PASS-con-fix (A-2)
(a) $E^{add}\circ M=E'+B$ con $M$ isomorfismo $H^m$ e $B$ limitato da $H^1$, quindi da $H^m$ per $m\ge1$. L'equivalenza è corretta. (b) Il passaggio da $H^{m+1}$ a $H^m$ è corretto: la stessa successione testimonia l'illimitatezza perché $\|u\|_{H^m}\le\|u\|_{H^{m+1}}$. Per $m=0$ serve l'illimitatezza in $H^1$, che è data. (c) $N=1$: P1-T2(i) dà $E'=0$. Il caso $N=0$ è enunciato male (A-2), ma la conclusione è vera.

### S10A-C1 — PASS-con-fix (A-3)
Con ≥ 2 monomi di grado ≥ 1, la parte non costante $Q'$ soddisfa le ipotesi di OPA-T3(b), cioè gradi distinti ≥ 1, $N\ge2$, (ND) automatica. Con S10A-T1(b) segue l'illimitatezza per ogni $m$ e ogni $t_0$. Con ≤ 1 monomio non costante si applica S10A-T1(c). La formula RD $E^{add}=(e^{sr}-1)(v(t)-v_0)$ è verificata (a_q6 (1)). Numericamente, su una famiglia di modi indipendente da quella di S10:
- RD: $R=0.126,\,0.054,\,0.021,\,0.0076$, che decresce;
- ADR: $R=0.22,\,6.1,\,2.5\cdot10^4,\,2.2\cdot10^{12}$, che esplode.

**Lettura di P1-Q6.** NOTAZIONE.md riga 44 dice: "Termine: un monomio $\lambda_kT_k$ di $L$". La reazione $r\,\mathrm{id}$ è il monomio di grado 0, quindi è un termine. La riga originale (LEDGER r. 14) dice "≥ 2 termini", e la lettura di OPA dice "≥ 2 termini non proporzionali". Entrambe sono falsificate da $u_t=Du_{xx}+ru$. Di conseguenza la frase del triage di OPA §4 ("è vero per i monomi (la definizione di termine di NOTAZIONE)") e la chiusura "P1-Q6 CHIUSO" di LEDGER r. 148 dicono più di quanto provato: valgono solo per monomi **non costanti**. La correzione di S10 è giusta.

### S10A-T2 — PASS-con-fix (A-4, A-5)
Ho rifatto la prova riga per riga.
- **Passo 0.** $\sigma_\mu$ è unitario, quindi $\sigma_\mu(e^{gZ})=e^{g\sigma_\mu Z}$ coefficiente per coefficiente, e i coefficienti stanno in $\mathcal A_0$. La sostituzione $t=\nu^\alpha s$ è un riscalamento della variabile formale ed è lecita. Gli esponenti $\alpha k-w_i$ valgono $\alpha(k-1)\ge0$ per i fattori X e $\ge\alpha-\beta=\mathfrak a\ge1$ per i fattori Y. Questo usa $\alpha\ge0$ e $k\ge1$, cioè $g_i\in t\mathbb C[[t]]$ (a_q7 (5), valutazioni).
- **Passo 1.** Il coefficiente di $s^m$ coinvolge solo i $g_{i,k}$ con $k\le m$ e parole di lunghezza $\le m$. Le coordinate in $W_m$ sono quindi polinomi in ν, e l'uguaglianza su un insieme infinito dà l'identità polinomiale. Corretto.
- **Passo 2.** Modulo $\nu^{\mathfrak a}$ restano i fattori X, che commutano. L'argomento del termine minimo richiede un ordine ben fondato: si usa il grado totale in $(s,\nu)$, che è ≥ 1 perché ogni $h_i$ ha valutazione in $s$ almeno 1, e i prodotti hanno grado totale strettamente maggiore. Corretto.
- **Passo 3** (il punto chiesto dal CHECK_REQUEST). I contributi misti (un fattore Y all'ordine $\nu^{\mathfrak a}$ più un fattore X a un ordine ≥ 1) hanno ordine $>\mathfrak a$ e non compaiono. Verificato esplicitamente in un'algebra libera troncata con tempi generici (a_q7 (5)). Il coniugio $e^{-\tau X}Ye^{\tau X}=\sum_k(-\tau)^k\mathrm{ad}_X^kY/k!$ e la formula di Duhamel formale sono corretti.
- **Passo 4.** Per ogni potenza di $s$ la relazione è finita, quindi (H) si applica. Il determinante di Hankel da $p$ nodi è identicamente nullo per $n=p+1$ (a_q7 (2), $p\le3$). Quello destro vale $\varepsilon_0^ns^{n^2}\det\mathrm{Hilb}_n\ne0$ (a_q7 (1), $n\le6$).
- **Esempi.** Weyl: verificato su funzioni test concrete, con $\sigma X=\mu^{a-1}X$, $\sigma Y=\mu^{-1}Y$ e il commutatore preservato (a_q7 (4)). Algebra libera e ℤ-graduazione: corretti.

### S10A-T3 — PASS-con-fix sulla logica; condizionato a [COL] (A-7)
- **Passo 2′.** La stima $y_2-\varphi(y_1)\ge\varepsilon-|q_2|-L|q_1|\ge\varepsilon-\sqrt{1+L^2}|q|>\varepsilon/2$ è corretta (Cauchy–Schwarz). Il test Monte Carlo dà 0 violazioni (a_p2q1 (8)). L'ordine delle definizioni di $C_i''$ e $d_i$ è però circolare come è scritto: va sistemato con A-7(b).
- **Passi 3–7.** Li ho riletti in OPF5B-T1. Il Passo 3 usa solo $V_\varepsilon\cap\mathrm{supp}\,\theta_i\subset O_i$, che è dato dal Passo 2′. Il Passo 4 usa solo $|\tau_i|\to0$. I Passi 5–7 usano il compatto fisso $K$, F1, F2 e L1. Nessuno usa la convessità, come dice la mappa delle dipendenze di OPF5B ("Passo 2 ← convessità"; il Passo 8 è sostituito qui dai Passi B–D).
- **Passo D.** L'indipendenza lineare in $\mathcal K/S$ è aperta (Gram, proiezione di norma ≤ 1). Un solo $U$ per tutti i $v_k$ si ottiene come nella Precisazione 2. $w_j|_\Omega\in C^\infty(\bar\Omega)\subset H^m$ perché $\bar\Omega\subset U$ è compatto. La contraddizione è corretta. Il Passo C usa OPF-T4(ii) per $C^\infty(U)$ su un aperto qualunque, che è DIMOSTRATO (r. 138).
- **[COL].** Le sedi (Grisvard Lemma 1.5.1.9, Verchota JFA 59 (1984) Thm 1.12, Hofmann–Mitrea–Taylor JGA 17 (2007)) **non** compaiono in `research/CIT-AUDIT/sources_verified.bib` né in nessun AUDIT-n. La fonte è non verificata. Il contenuto è standard e credibile. Resta da verificare soprattutto l'inclusione $\bar\Omega\subset\Phi_\sigma(\Omega)$, cioè $\Phi_{-\sigma}(\bar\Omega)\subset\Omega$, che richiede la trasversalità uniforme. Finché la fonte non è verificata il teorema non può essere registrato come DIMOSTRATO né come CON-FONTE.

### S10A-P1 — PASS-con-fix (A-8)
- **Flusso.** $\Phi_\gamma(\log|z|)=2\pi$, e il flusso è nullo su $z^n$ e $\bar z^n$, $n\ne0$, incluse le potenze negative (a_p2q1 (1),(2)).
- **Formule.** ${*dz}=-i\,dz$ e ${*d\operatorname{Re}F}=d\operatorname{Im}F$ sono corrette (a_p2q1 (3),(4)).
- **Laurent.** Per $h$ armonica complessa sull'anello, $\partial_zh$ è olomorfa. Il coefficiente di $z^{-1}$ e quello coniugato producono $a\log z+b\log\bar z$, e la monodromia impone $a=b$. Il flusso vale $2\pi c$ (a_p2q1 (5)).
- **Regolarità.** $f\in H^m$ da $f'\in H^{m-1}$ con la stima in polari: corretto per $m\ge1$.
- **Continuità del flusso.** La conclusione è corretta, ma la catena di stime scritta è confusa (A-8(a)).
- Codimensione esatta 1 $=\delta(\Delta)\,b_1$, con $\delta(\Delta)=1$ (a_p2q1 (7)). È coerente con il limite di S10A-T3 e con OPF-T4.

### S10A-L2, S10A-C2 — PASS
$\Pi_r(B_M)\subset\sum_{i<r}\Pi_r\Pi_i(B_C)$ perché $\Pi_rh_i=\Pi_r\Pi_ih_i$ per $h_i\in\mathcal H_i$. Il teorema della mappa aperta si applica, essendo $M$ chiuso e quindi di Banach. OPR2-L1 con due sottospazi va bene. Controllo indipendente: $\Pi_A\Pi_B$ compatto implica $\dim(A\cap B)<\infty$, e la norma su $(A\cap B)^\perp$ è $<1$ perché è raggiunta, quindi $A+B$ è chiuso. Il corollario C2 è un conteggio corretto. La riduzione è **dimostrata** e il suo enunciato è corretto.

## 3. Voci "già chiuse da righe successive" (§0 di S10)

| voce | domanda originale | riga di chiusura | copre davvero? |
|---|---|---|---|
| II-L1(b) | biiezione del t-jet | r. 70 DIMOSTRATO, S-CHECK-6 PASS | sì |
| P4-T5 "esattamente", P4-Q-min (r. 67, 80) | minimalità del maggiorante | r. 111 OP-ALG-T3 (il minimo è χ ≡ D; B è strettamente più forte su qualche dominio) e r. 156 (ogni dominio) | sì: la domanda ha risposta precisa, cioè B non è minimo e il minimo è identificato |
| OP-ALG-Q1/Q2 (r. 114) | test finito; T3(f) per ogni dominio | r. 154, r. 156 | sì |
| EX-Q1 | OP-ALG-T4 per P non monico (Bessel), `work/S5-EX/REPORT.md` | r. 170 OPF5B-C4 | sì. Nota: EX-Q1 non è nella r. 163 citata da S10 (A-1) |
| OPF-Q1 (r. 137) | densità calore × trasporto | r. 151 | sì per la densità. La chiusura resta APERTA (C12-Q1), come S10 dice correttamente |
| OPF-Q3 (r. 137) | trave sul parallelogramma | r. 166–167 (il parallelogramma è convesso) | sì |
| P1-Q5 = OPA-P4 (r. 61, 149) | E_int dal bordo a ε = 1, dati compatibili | r. 182 OPF5A-T5, **S-CHECK-20 PASS-con-fix, KA sopravvissuto** | sì (A-12: l'audit esiste) |
| P3-Q-bordo (r. 75) | tasso per dati generali e ordine esatto | r. 146 OPA-T2 (Θ(t^{k/2+3/4})) + r. 182 | sì |
| C12-Q6 (r. 53) | condizione esatta fuori dai semplicemente connessi | r. 138 OPF-T4 | sì, con le parti (iii), (iv)(c,d) mod CON-FONTE |
| C3-Q1 (r. 64) | decidibilità | r. 110 (M3-hol), r. 67/111/156 (M2⁺), r. 291 CONV-T2 (limite) | sì per modello (A-11) |
| P1-Q6 | — | r. 148 dice "CHIUSO" | **no**: la chiusura era scritta solo per termini non costanti; il residuo reale è stato chiuso ora da S10A-T1/C1 (A-3) |

## 4. Esiti di tipo riduzione od ostruzione

- **P1-Q7.** La "riduzione" è una divisione in casi: sotto (Dil) il problema è chiuso, fuori resta aperto. Il caso sotto (Dil) è dimostrato. Che il residuo sia esattamente le algebre senza (Dil) è vero per costruzione. L'enunciato è corretto, ma va detto che è una divisione in casi e non un'equivalenza (A-6).
- **C12-Q2.** La riduzione (S10A-C2) è dimostrata ed enunciata correttamente.
- **P2-Q1.** La parte "FALSO con buchi" è dimostrata. La parte "densità sui lipschitziani semplicemente connessi" è una riduzione a [COL], non una prova (A-7, A-9).
- **P1-Q6-ND.** È fuori dall'enunciato (i termini sono monomi, per cui (ND) vale sempre). Corretto.

## 5. Kill-argument sul claim più forte: S10A-T2

Scelgo S10A-T2 perché toglie un'ipotesi di un teorema DIMOSTRATO, vale a $\varepsilon_0$ fisso e con tempi solo formali.

Attacchi tentati:
1. **Algebre di dimensione finita.** In SU(2), con gli angoli di Eulero, parole finite esistono. Ma (H) chiede infiniti $\mathrm{ad}_X^kY$ linearmente indipendenti, impossibile in dimensione finita. Niente.
2. **Quozienti nilpotenti dell'algebra libera.** Lì (H) vale fino a un ordine finito e le parole finite esistono (coordinate di seconda specie). È il punto da controllare: la prova usa davvero (H) fino a $Y_{2p}$? Il sistema dei momenti $\sum_{i=1}^pq_i\tau_i^k=\varepsilon_0s^{k+1}/(k+1)$ è **risolubile** per $k=0,\dots,2p-1$: è la quadratura di Gauss–Legendre su $[0,s]$ con $p$ nodi. Fallisce esattamente a $k=2p$ (a_q7 (3), residui $-1/12$, $-1/180$, $-1/2800$ per $p=1,2,3$). Quindi la prova usa (H) in modo essenziale e ottimale per il passo di Hankel. Non c'è falla: in un'algebra con (H) completa il vincolo $k=2p$ è sempre presente.
3. **Dilatazione con $\beta=\alpha$.** Esiste in ogni algebra graduata con X e Y dello stesso grado, ma non soddisfa (Dil), che chiede $\beta<\alpha$. La prova fallisce lì, correttamente.
4. **σ_μ non iniettivo.** La prova usa solo l'identità trasformata e (H) in $\mathcal A_0$. Siccome $\sigma_\mu X=\mu^\alpha X\ne0$, la non iniettività non danneggia nulla.
5. **Contributi misti al Passo 3 con $\mathfrak a>1$.** Esclusi, verificati simbolicamente (a_q7 (5)).

Giudizio: **SOPRAVVIVE**. Ne viene un rafforzamento facoltativo (A-4).

Sul claim più delicato per lo stato, S10A-T3, il kill-argument chiesto (un lipschitziano semplicemente connesso con somma non densa) non trova nulla: S10A-P1 richiede un buco e gli esempi con $\delta(P)=0$ sono densi. Questo non sostituisce però la verifica di [COL].

## 6. Fix

- **A-1 (bookkeeping, §0 e §1 di S10).** "r. 229" (P1-Q6 CHIUSO) e "r. 231" (OPA-P4) sono righe della tabella di `work/OP-ANA/PROOF_PACKAGE.md`, non di `claims/LEDGER.md`. Nel LEDGER le righe giuste sono: P1-Q6 originale r. 14, chiusura r. 147–148; P1-Q5 r. 61, OPA-P4 r. 149. "NOTAZIONE (r. 44)" va scritto come `NOTAZIONE.md` riga 44. EX-Q1 non è nella r. 163: la sua sede è `work/S5-EX/REPORT.md`, con chiusura alla r. 170.
- **A-2 (S10A-T1(c), caso $N=0$).** $\ker\tau$ contiene solo funzioni di $x$, quindi $E'(v)=v(t)-v_0\equiv0$, non solo "limitata". Va scritto: "$E'=0$ anche per $N=0$; in entrambi i casi $E^{add}\circ M=B$".
- **A-3 (S10A-C1 e riga P1-Q6).** (a) Citare l'enunciato originale "≥ 2 termini" (r. 14) accanto alla lettura di OPA; il controesempio RD vale per entrambe. (b) Il coordinatore deve **declassare** la r. 148 ("P1-Q6 CHIUSO"), sostituendola con: FALSO come scritto; DIMOSTRATO per "≥ 2 monomi di grado ≥ 1" (OPA-T3(b) + S10A-T1(b)). Va segnalata come imprecisa anche la frase del triage di OPA §4 sui monomi, che dimentica il grado 0. (c) Dire esplicitamente che, con ≤ 1 monomio non costante, la limitatezza è provata solo per $m\ge1$; il caso $m=0$ non è affermato.
- **A-4 (S10A-T2, rafforzamento facoltativo).** Per una parola fissata con $p$ fattori Y la prova usa (H) solo per $X,Y_0,\dots,Y_{2p}$. La quadratura di Gauss mostra che $2p$ è ottimale per il passo di Hankel. Si può aggiungere come osservazione.
- **A-5 (S10A-T2, conseguenza per P1-Q7).** Va scritto che $\varepsilon_0$ si prende con $0<|\varepsilon_0|<$ raggio del polidisco. Va scritto anche che è l'ipotesi $g_i(0,\varepsilon)=0$ di P1-T5 a dare $g_i(\cdot,\varepsilon_0)\in t\mathbb C[[t]]$, come chiede S10A-T2.
- **A-6 (P1-Q7, dicitura).** Scrivere: "APERTO — dimostrato sotto (Dil) (S10A-T2); residuo: algebre con (H) senza (Dil)". Il candidato $(x^3+x)\partial,\partial$ resta da verificare anche per (H).
- **A-7 (S10A-T3).** (a) Stato: **APERTO — ridotto a [COL]**. [COL] non è in `sources_verified.bib`: serve una richiesta CIT-AUDIT specifica per Grisvard Lemma 1.5.1.9, Verchota 1984 Thm 1.12 e Hofmann–Mitrea–Taylor 2007, sull'inclusione $\bar\Omega\subset\Phi_\sigma(\Omega)\subset\{\mathrm{dist}<C\sigma\}$. Dopo la verifica: CON-FONTE/DIMOSTRATO mod [COL]. (b) Passo 2′: definire prima $C_i'':=\{\mathrm{dist}(\cdot,C_i')<d_i'/4\}$ con $d_i':=\mathrm{dist}(C_i',\partial C_i)$, poi $d_i:=\mathrm{dist}(C_i'',\partial C_i)\ge\tfrac34d_i'$, e prendere $\varepsilon\le\varepsilon_1:=\min_id_i/4$. Così $y_0+\tau_i+q\in C_i$ per $y_0\in\bar C_i''$. (c) Nel Passo A prendere ε abbastanza piccolo da avere $\{\mathrm{dist}(\cdot,\bar\Omega)<r_\varepsilon/2\}\subset V$, così che $V_\varepsilon$ sia un intorno metrico e la mollificazione su $V'_\varepsilon$ sia lecita. (d) Le righe derivate (P2-Q1 "densità sui lipschitziani semplicemente connessi", OPF5B-C1(d) "assorbita") vanno registrate come condizionate a [COL].
- **A-8 (S10A-P1).** (a) Stima interna, da riscrivere così: $|\nabla h(y)|\le\frac{C}{\delta}\sup_{B(y,\delta/2)}|h|\le\frac{C'}{\delta^2}\|h\|_{L^2(\Omega)}$ (media su palle di raggio $\delta/2$ e Cauchy–Schwarz). La catena "$\frac C{\delta^2}\cdot\frac1\delta\|h\|_{L^1}$" è dimensionalmente confusa, anche se la conclusione è giusta. (b) Per (ii) citare CIT-AUDIT-3 #1 (Rudin RCA 13.11: contenuto verificato, numero no). In alternativa la premessa si fa elementare: per Ω limitato lipschitziano con $b_1\ge1$, $\partial\Omega$ ha almeno due componenti; una componente limitata del complementare ha interno non vuoto, e una curva parallela a quella componente nelle carte lipschitziane fa da ciclo γ.
- **A-9 (riga P2-Q1).** Sostituire "domini con buchi: FALSO in generale" con: "falso come enunciato universale: per $P=\Delta$ su ogni lipschitziano con $b_1\ge1$ (S10A-P1); per $\delta(P)=0$, densità su ogni lipschitziano (S10A-T3(a)), mod [COL]".
- **A-10 (C12-Q2, dicitura).** Nella "Lettura" di S10A-C2 l'affermazione sui trasporti ("due lati richiedono tre fattori della stessa classe") vale perché OPR2-T2 dà interazione Hilbert–Schmidt per direzioni diverse. È un'osservazione, non parte della riduzione.
- **A-11 (C3-Q1).** "CHIUSO per modello" non è uno stato di NOTAZIONE. Va scritto: "DIMOSTRATO come classificazione per modello (composizione di P4-T5+P4-L7, OP-ALG-T3, OPR2-C2, OP-ALG-T1 mod (AC), CONV-T2 r. 291); nessuna matematica nuova". La r. 64 "PARZIALE" è già superata dalla r. 110.
- **A-12 (§0, P1-Q5).** L'audit della r. 182 esiste (S-CHECK-20 PASS-con-fix(F5A-7,8), KA sopravvissuto): la chiusura è confermata e la riserva "non ho riletto l'audit" si può togliere.
