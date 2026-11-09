# AUDIT-COL — verifica della fonte [COL] (S10A-T3)

Verificatore: CIT-COL. Data: 2026-10-27.
Oggetto: la fonte [COL] di `work/S10-OPEN-A/PROOF_PACKAGE.md` §3, richiesta dal fix A-7(a) di `work/CHECK-F10/AUDIT_S10-OPEN-A.md`.

## 0. Cosa si deve verificare

[COL] contiene due affermazioni di natura diversa, e conviene separarle.

- **(COL-i) Esistenza del campo.** Un aperto limitato lipschitziano Ω ammette un campo liscio V, a supporto compatto, uniformemente trasversale a ∂Ω e uscente. Trasversale qui vuol dire $V\cdot\nu\ge\kappa>0$ quasi ovunque su ∂Ω, con ν la normale esterna.
- **(COL-ii) Inclusioni del flusso.** Per $0<\sigma\le\sigma_0$ si ha $\bar\Omega\subset\Phi_\sigma(\Omega)\subset\{\mathrm{dist}(\cdot,\bar\Omega)<C\sigma\}$.

Il pacchetto stesso osserva che l'inclusione esterna è elementare ($C=\sup|V|$), e così il fatto che $\Phi_\sigma(\Omega)$ sia diffeomorfo a Ω. Il punto da verificare è quindi (COL-i) insieme all'inclusione interna $\bar\Omega\subset\Phi_\sigma(\Omega)$, cioè $\Phi_{-\sigma}(\bar\Omega)\subset\Omega$, come chiede l'audit A-7.

Nota a margine: il pacchetto enuncia [COL] in $\mathbb R^2$, la richiesta in $\mathbb R^n$. Le fonti trattano $\mathbb R^n$, quindi la differenza non pesa.

Metodo: ricerca web (Google Books, con i suoi snippet di ricerca interna, poi arXiv e ar5iv, pagine degli editori). Non ho potuto leggere il testo integrale di nessuna delle tre fonti. Google Books mostra solo snippet, con OCR in parte illeggibile, e la ricerca interna al libro è bloccata da un CAPTCHA, che non ho aggirato. Springer (HMT) richiede l'accesso. Per Verchota non ho trovato il PDF. I verdetti si basano su snippet della fonte primaria e su citazioni puntuali in lavori secondari.

## 1. Grisvard, *Elliptic Problems in Nonsmooth Domains*, Lemma 1.5.1.9

Dati bibliografici: Pitman, Monographs and Studies in Mathematics 24, 1985; ristampa SIAM Classics in Applied Mathematics 69, 2011 (ISBN 9781611972023). Esiste anche la versione preliminare *Boundary Value Problems in Non-smooth Domains* (1980, note di corso), con la stessa numerazione.

Riscontri:
- Uno snippet di Google Books della versione 1980 apre il lemma con "Lemma 1.5.1.9 : Let Ω be a bounded open subset of IR with a Lipschitz". Il seguito, con OCR rovinato, nomina un campo vettoriale liscio, scritto come combinazione $\sum_k\theta_k(\cdot)$ dei campi delle carte locali, e una minorazione con una costante positiva.
- Uno snippet dell'edizione SIAM 2011 mostra un campo vettoriale, il prodotto con la normale ν, una costante del tipo $1/\sqrt{1+L^2}$ con L costante di Lipschitz, e il rimando al Teorema 1.5.1.10, che usa il Lemma 1.5.1.9.
- arXiv:2010.15766 (integrabilità superiore per funzionali (p,q)) cita testualmente "[30, Lemma 1.5.1.9.]", cioè Grisvard, per l'esistenza di κ>0 e di X liscio con X·ν ≥ κ q.o. su ∂Ω. Poi usa il flusso di X per costruire domini dilatati $\Omega^s\supset\bar\Omega$, ma solo per domini $C^{1,\alpha}$ (Lemma 2.6) e con una prova propria.
- Il libro di Dalla Riva, Lanza de Cristoforis e Musolino (*Singularly Perturbed Boundary Value Problems*, Springer 2021) cita "Grisvard [112, Lemma 1.5.1.9]" per un campo trasversale con estremo inferiore essenziale di $a\cdot\nu$ positivo su insiemi lipschitziani.

Verdetto: **VERIFICATO per (COL-i)**, contenuto e numero. Il Lemma 1.5.1.9 dà un campo liscio con $\mu\cdot\nu\ge\delta>0$ q.o. su ∂Ω, per Ω limitato lipschitziano in $\mathbb R^n$. Il lemma **non** contiene (COL-ii): non parla di flussi né di inclusioni. Riserva: l'enunciato esatto l'ho ricostruito da snippet con OCR parziale e da due citazioni secondarie concordi. Non l'ho letto per intero.

## 2. Verchota, J. Funct. Anal. 59 (1984), Teorema 1.12

Dati bibliografici: G. Verchota, "Layer potentials and regularity for the Dirichlet problem for Laplace's equation in Lipschitz domains", J. Funct. Anal. 59 (1984), n. 3, 572–611. Un lavoro del 1989 (Ann. Fac. Sci. Toulouse) scrive "vol. 56", ma le pagine coincidono e le altre fonti dicono 59: la "56" è un refuso di quella fonte. Il numero "Teorema 1.12" è quello citato dalla maggior parte dei lavori. Qualcuno scrive "Proposition 1.12", e si cita anche l'Appendice della tesi di Verchota.

Contenuto, ricostruito da arXiv:1701.08332 (Teorema 2.9, "theorem 1.12 in [Ver84]") e da altri lavori che lo riportano:
- esiste una successione di domini $C^\infty$ $\Omega_j\subseteq\Omega$, con omeomorfismi bi-lipschitziani $\Lambda_j:\partial\Omega\to\partial\Omega_j$ e $\sup_q|q-\Lambda_j(q)|\to0$;
- costanti di Lipschitz uniformi e jacobiani limitati dall'alto e dal basso;
- (parte v) esiste un campo $C^\infty$ h con $\langle h(\Lambda_j q),\nu(\Lambda_j q)\rangle\ge C>0$ uniformemente in j e q.

L'approssimazione dall'esterno compare a parte (Definizione 1.13 di Verchota, citata da 1701.08332).

Verdetto: **PARZIALE**. Il Teorema 1.12 è un teorema di approssimazione dall'interno con domini lisci. Contiene come ingrediente un campo liscio uniformemente trasversale, quindi (COL-i) in forma indiretta, ma non l'enunciato sul flusso né l'inclusione $\bar\Omega\subset\Phi_\sigma(\Omega)$. I dati bibliografici sono corretti (59, 1984, 572–611). Non ho letto il testo originale.

## 3. Hofmann–Mitrea–Taylor, J. Geom. Anal. 17 (2007)

Dati bibliografici completi: S. Hofmann, M. Mitrea, M. Taylor, "Geometric and transformational properties of Lipschitz domains, Semmes–Kenig–Toro domains, and other classes of finite perimeter domains", J. Geom. Anal. 17 (2007), n. 4, 593–647, DOI 10.1007/BF02937431.

Riscontri:
- Il risultato principale, riportato dal riassunto e da più lavori secondari: sotto ipotesi di fondo deboli, un dominio è lipschitziano se e solo se ammette un campo vettoriale continuo trasversale.
- arXiv:2512.13098 (Teorema 2.4) cita "[22, Cor. 2.13]" per questo fatto: ogni dominio lipschitziano limitato non vuoto ha un campo liscio "(globally) transversal". Lo stesso lavoro rimanda a HMT, pp. 633–634, per la bi-lipschitzianità della parametrizzazione $(s,t)\mapsto s+t\,k(s)$ di uno strato esterno a ∂Ω.
- arXiv:1201.0047 (Lemma 4.4) cita [Grisvard, HMT] come fonti standard del campo trasversale.

Verdetto: **DATI CORRETTI**, con contenuto trovato solo in forma indiretta (quindi PARZIALE quanto alla verifica). Il pacchetto cita genericamente "transversal vector fields"; la sede precisa per (COL-i) è il **Corollario 2.13**. Le pp. 633–634 contengono un risultato vicino a (COL-ii): uno strato esterno parametrizzato in modo bi-lipschitziano lungo il campo. Non è però enunciato come inclusione del flusso, e non ho potuto leggerlo direttamente. La caratterizzazione "trasversale ⟺ lipschitziano", in particolare il fatto che vicino a ogni $x_0\in\partial\Omega$ il dominio sia un sopragrafico lipschitziano nella direzione $h(x_0)$, è il pezzo che serve a dimostrare l'inclusione (vedi §4).

## 4. Conclusione su [COL]

- **(COL-i), esistenza del campo trasversale: VERIFICATA.** La sede principale è Grisvard, Lemma 1.5.1.9, con numero e contenuto riscontrati. HMT 2007, Cor. 2.13, la conferma in forma indiretta.
- **(COL-ii), inclusione interna $\bar\Omega\subset\Phi_\sigma(\Omega)$: NON TROVATA in forma letterale** in nessuna delle tre fonti. Grisvard si ferma al campo. Verchota 1.12 approssima dall'interno senza usare il flusso. HMT ha la caratterizzazione con i sopragrafici e lo strato esterno bi-lipschitziano, ma non un enunciato sul flusso.

Quindi [COL] così come è scritta **non** è verificata da nessuna fonte con contenuto sufficiente per il passo dell'inclusione. L'inclusione però segue da (COL-i) con un argomento breve ed elementare, che conviene scrivere nel pacchetto invece di affidarlo a una citazione. Uno schema possibile:

1. Si prende V esplicito con Grisvard, $V:=\sum_i\theta_i(-e_i)$ normalizzato, dove $e_i$ è la direzione verticale della carta $C_i$ del Passo 1′ (Ω sta sopra il grafico). In ogni carta, $-e_i$ e i campi vicini a $-e_i$ puntano nel cono uscente.
2. Più direttamente, senza passare dalle normali q.o.: se $\Omega\cap C=\{y_n>\psi(y')\}$ con ψ M-lipschitziana, e un campo continuo W soddisfa $W\cdot e_n\ge c|W|$ con $c>M/\sqrt{1+M^2}$, allora per $x\in\bar\Omega\cap C'$ la traiettoria di W da x resta in $x+\Gamma$. Qui Γ è il cono aperto $\{z:\ |z'|<z_n/M\}$, che è convesso, quindi contiene gli integrali delle velocità. Per $0<s\le s_0$ si ha $y_n-\psi(y')\ge x_n-\psi(x')+z_n-M|z'|>0$, cioè la traiettoria sta in Ω. Si applica con $W=-V$. Serve che $-V$ stia nel cono di ogni carta in cui il punto si trova. Si ottiene scegliendo carte "compatibili": i coni delle carte che si sovrappongono hanno un'intersezione aperta non vuota che contiene le combinazioni convesse $\sum\theta_i e_i$. È proprio la scelta di Grisvard e HMT. In alternativa si prende una sola carta per punto, restringendo i supporti.
3. Per compattezza di ∂Ω l'argomento vale uniformemente per $0<s\le\sigma_0$, quindi $\Phi_{-s}(\partial\Omega)\subset\Omega$. Una traiettoria di −V che parte da $x\in\Omega$ non può uscire da $\bar\Omega$ prima del tempo σ: dovrebbe toccare ∂Ω in un punto y a un tempo $s_1<\sigma$, e il punto 2 applicato a y la riporterebbe subito dentro Ω. Si conclude $\Phi_{-\sigma}(\bar\Omega)\subset\Omega$, cioè $\bar\Omega\subset\Phi_\sigma(\Omega)$.

Il punto delicato è la compatibilità dei coni nelle zone dove le carte si sovrappongono. È esattamente il contenuto di "trasversale ⟹ sopragrafico lipschitziano nella direzione del campo", cioè la caratterizzazione di HMT 2007, oppure la stessa costruzione di Grisvard, se letta per intero.

**Raccomandazione per lo stato di S10A-T3.** Va registrato:
- "[COL-i] CON-FONTE Grisvard, Lemma 1.5.1.9 (verificato), con conferma in HMT 2007, Cor. 2.13";
- "[COL-ii] da dimostrare nel pacchetto (schema in AUDIT-COL §4)".

Finché il passo 2 dello schema non è scritto e auditato, S10A-T3 resta **APERTO — ridotto a [COL-ii]**. Va inoltre corretta la citazione nel pacchetto:
- Verchota non è una sede per [COL], perché il suo teorema approssima dall'interno;
- per HMT va indicato il Cor. 2.13 e, per lo strato esterno, le pp. 633–634.

## Fonti consultate

- Google Books, Grisvard, SIAM 2011 (id lJTtujsZSgkC) e versione 1980 (id OzjvAAAAMAAJ): solo snippet.
- Google Books, Dalla Riva, Lanza de Cristoforis, Musolino 2021 (id aNxFEAAAQBAJ): snippet.
- arXiv:2010.15766 (ar5iv), §2.3: citazione di Grisvard, Lemma 1.5.1.9.
- arXiv:1701.08332 (ar5iv), Teorema 2.9: riporta Verchota, Teorema 1.12.
- arXiv:2512.13098 (HTML), Teorema 2.4 e §4.1: riportano HMT, Cor. 2.13 e pp. 633–634.
- arXiv:1201.0047 (ar5iv), Lemma 4.4: cita [Grisvard, HMT].
- DOI 10.1007/BF02937431 (HMT), solo metadati.
