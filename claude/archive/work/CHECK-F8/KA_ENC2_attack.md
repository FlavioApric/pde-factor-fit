# KA ENC2 — attacco indipendente su ENC-P0(b)^cl, ENC-P0(b)^loc ed ENC-T2(c′)

Data: 27/10/2026. Fonte unica: `work/CHECK-F8/KA_ENC2_input.md`. Verifiche: `work/CHECK-F8/sympy/enc2_ka_checks.py`, output in `enc2_ka_checks.out` accanto (sezioni A–D, tutte eseguite con esito coerente con quanto scritto sotto).

Convenzione sulle severità. FATAL: il claim è falso e non si ripara senza cambiarne il contenuto. CRITICAL: il claim, così come è scritto, è mal posto o ha un controesempio, ma una riparazione locale e onesta lo salva. MAJOR: passaggio non giustificato o affermazione accessoria falsa o non provata, che non tocca il nucleo. MINOR: imprecisione di scrittura.

---

## Parte I — ENC-P0(b)^cl ed ENC-P0(b)^loc

### P1. Il dominio di W non contiene gli oggetti su cui W viene applicato (V solo continuo)

**Bersaglio.** ENC-P0(b)^cl, ipotesi "V ∈ C(I × J)" insieme a "W: C^∞(J) → C^∞(J)" e all'identità W(−∂_x² + V(t, ·))f = (−∂_x² + c(t))Wf per f ∈ C^∞_c(J); prova, passo "W(mf) = 0 … le mφ_k stanno in ker W".

**Obiezione.** Se V(t, ·) è soltanto continua, allora (−∂_x² + V(t, ·))f è in generale soltanto continua, non C^∞, e quindi il membro sinistro W(L_{V(t)} f) non è definito, perché W è definito solo su C^∞(J). Lo stesso vale per la funzione m·φ_k nella prova: m = V(t, ·) − V(s, ·) − (c(t) − c(s)) è soltanto continua, quindi m·φ_k ∈ C_c(U) ma in generale non appartiene a C^∞(J), dunque non può stare in ker W ⊂ C^∞(J). Letto alla lettera, l'enunciato è mal tipizzato non appena V(t, ·) non è liscia: l'ipotesi non ha senso.

**Controesempio (lettura "l'identità vale dove ha senso").** Se si prova a salvare l'enunciato leggendo l'ipotesi solo per le f tali che V(t, ·)f sia C^∞, l'enunciato diventa falso. Si prenda una funzione continua w su J che non sia differenziabile in nessun punto di un insieme denso (per esempio la funzione di Weierstrass, oppure w(x) = Σ_n 2^{−n}|x − r_n| con (r_n) un'enumerazione dei razionali di J). Se f ∈ C^∞_c(J) e w·f ∈ C^∞, allora f = 0: infatti, dove f ≠ 0, w = (wf)/f sarebbe liscia su un intervallo, e questo contiene punti di non differenziabilità. Si pongano V(t, x) = t·w(x), c = 0, W = identità su C^∞(J). Allora l'unica f per cui l'identità "ha senso" è f = 0, l'ipotesi è soddisfatta in modo vuoto, ker W = 0, ma V(t, ·) − V(s, ·) = (t − s)w non è costante.

**Severità proposta.** CRITICAL (l'enunciato così scritto è mal posto; la riparazione è immediata).

**Riparazione.** Basta una delle due. (i) Richiedere V(t, ·) ∈ C^∞(J) per ogni t ∈ I (V ∈ C(I × J) resta sufficiente per la conclusione "per ogni x", per continuità). Con questa ipotesi mφ_k ∈ C^∞_c(U) ⊂ C^∞(J) e la prova è corretta. (ii) Tenere V continuo ma far agire W su uno spazio che contenga i prodotti C(J)·C^∞_c(J), per esempio W: C(J) → 𝒟′(J) lineare, con dim ker W < ∞ **su tutto quel dominio**, e con l'identità intesa nel senso delle distribuzioni. Anche in questo caso la prova passa senza cambiamenti. Il punto essenziale è che la finitezza del nucleo deve valere su uno spazio che contenga le funzioni m·φ_k (vedi P2).

### P2. ENC-P0(b)^loc ha un controesempio esplicito (con V continuo, come nell'enunciato richiamato)

**Bersaglio.** ENC-P0(b)^loc: "W lineare, definito almeno su C^∞_c(U), con dim ker W|_{C^∞_c(U)} < ∞, tale che l'identità di P0(b)^cl valga per ogni f ∈ C^∞_c(U)". Siccome l'identità è "quella di P0(b)^cl", V ∈ C(I × J) è soltanto continuo.

**Obiezione.** Qui il dominio di W può essere più grande di C^∞_c(U), e quindi l'identità può avere senso anche per V solo continuo. Però la finitezza del nucleo è richiesta solo sulla restrizione a C^∞_c(U), mentre le funzioni m·φ_k stanno in C_c(U) e non in C^∞_c(U). La prova "quella di P0(b)^cl" non produce quindi elementi del nucleo ristretto, e l'enunciato è falso.

**Controesempio esplicito.** Sia w come in P1 (continua, con w·f ∉ C^∞ per ogni f ∈ C^∞_c(U) non nulla). Siano X := C^∞_c(U) e Y := w·X ⊂ C_c(U). Per quanto detto, X ∩ Y = {0}, quindi la somma X ⊕ Y è diretta. Si definisce W su X ⊕ Y (che contiene C^∞_c(U)) ponendo

   W(g + w·f) := g, per g, f ∈ X.

W è lineare e ben definito. Si prendano V(t, x) := t·w(x) e c := 0. Per f ∈ X si ha L_{V(t)} f = −f″ + w·(t f), con −f″ ∈ X e t f ∈ X, quindi W(L_{V(t)} f) = −f″ = −(Wf)″ = (−∂_x² + c(t))Wf, perché W|_X è l'identità. Inoltre ker W|_{C^∞_c(U)} = {0}. Ciò nonostante V(t, ·) − c(t) = t·w non è autonomo su U. (Verifica simbolica della scomposizione e dell'identità: sezione D dello script.) Il nucleo di W su X ⊕ Y contiene tutto Y, che ha dimensione infinita: è esattamente lì che la prova si rompe.

**Severità proposta.** CRITICAL: l'enunciato, così scritto, è falso.

**Riparazione.** Come in P1: chiedere V(t, ·) ∈ C^∞(U) per ogni t (allora mφ_k ∈ C^∞_c(U) e la prova vale), oppure chiedere dim ker W < ∞ sull'intero dominio di W, supponendo che questo contenga C(U)·C^∞_c(U). Va precisato anche il codominio di W (vedi P3).

### P3. Codominio di W non specificato in ^loc

**Bersaglio.** ENC-P0(b)^loc: "W lineare, definito almeno su C^∞_c(U)".

**Obiezione.** Il membro destro (−∂_x² + c(t))Wf richiede che Wf sia derivabile due volte, almeno nel senso delle distribuzioni su un aperto che contenga U. Il codominio non è detto, e quindi neanche l'insieme in cui vale l'identità (su U? su J?). La prova non usa il codominio, ma l'enunciato deve averlo per avere senso.

**Severità.** MINOR.

**Riparazione.** "W: D_W → 𝒟′(U) lineare, con C^∞_c(U) ⊂ D_W, e identità in 𝒟′(U)".

### P4. "Equivalentemente" non è un'equivalenza

**Bersaglio.** ENC-P0(b)^cl: "Equivalentemente: W agisce solo in x e intreccia i u_t = L_{V(t)}u con i v_t = (L_0 + c(t))v sulle funzioni C^∞ di (t, x)".

**Obiezione.** Ci sono due letture possibili, e in nessuna delle due l'equivalenza è dimostrata.

(a) *Intrecciamento di operatori su C^∞(I × J)*, cioè (∂_t − L_0 − c(t))(Wu) = W((∂_t − L_{V(t)})u), con (Wu)(t, ·) := W(u(t, ·)). Prendendo u(t, x) = f(x) si ottiene l'identità su f, quindi questa direzione è vera. Il viceversa, invece, richiede che ∂_t(W u(t, ·)) = W(∂_t u(t, ·)) e che t ↦ W u(t, ·) sia C^∞, cioè che W sia (sequenzialmente) continuo per la topologia di C^∞(J). Un W soltanto lineare non soddisfa queste proprietà. Si può costruire W tramite una base di Hamel: per esempio, un W che coincide con un operatore di Volterra su un sottospazio e che è perturbato su un complemento algebrico non chiuso, per cui Wu(t, ·) non è nemmeno misurabile in t.

(b) *Mappa fra insiemi di soluzioni* (W manda soluzioni di u_t = L_{V(t)}u in soluzioni di v_t = (L_0 + c)v). Questa lettura è strettamente più debole. Per risalire all'identità su ogni f ∈ C^∞_c(J) servirebbe una soluzione con dato u(t_0, ·) = f arbitrario. Ma u_t = −u_xx + Vu è un'equazione del calore **all'indietro**: una sua soluzione a un istante interno è (per V liscio, o almeno nel caso V = 0) analitica in x all'interno di J. Un dato f a supporto compatto non nullo non è analitico, e quindi non esiste nessuna soluzione con quel dato. Le "fette" temporali delle soluzioni non riempiono C^∞_c(J), e l'implicazione (b) ⇒ identità è non provata (molto probabilmente falsa senza ipotesi ulteriori).

**Severità.** MAJOR: è un'affermazione accessoria, ma è presentata come equivalenza.

**Riparazione.** Sostituire con: "In particolare, se W è sequenzialmente continuo su C^∞(J), W intreccia gli operatori ∂_t − L_{V(t)} e ∂_t − L_0 − c(t) su C^∞(I × J); il viceversa (restringendosi alle u indipendenti da t) è immediato". Eliminare la lettura "su soluzioni", oppure enunciarla come ipotesi più debole senza dichiararla equivalente.

### P5. "Copre l'encoder di Volterra di ENC-1": vero solo con q liscio e J aperto

**Bersaglio.** "Copre l'encoder di Volterra di ENC-1 (iniettivo su C⁰, quindi con nucleo nullo)".

**Obiezione.** (1) P0(b)^cl richiede W: C^∞(J) → C^∞(J). L'encoder di ENC-1 è biiettivo su ogni C^k(J) solo se q ha regolarità sufficiente. Con q ∈ C^∞ manda C^∞ in C^∞, ma con q soltanto continuo il nucleo di Volterra K è solo C¹ e W non preserva C^∞. Quindi il "coprire" vale per encoder di Volterra di potenziali q ∈ C^∞, non per l'encoder di ENC-1 nella sua generalità. (2) In ENC-1 J è "intervallo simmetrico attorno a x_0" (forse chiuso), mentre in P0(b)^cl J è aperto: serve dire che si usa J°. (3) La parte "iniettivo su C⁰ ⇒ nucleo nullo su C^∞" è corretta, perché C^∞ ⊂ C⁰. (4) Va esplicitato *cosa* si copre. L'encoder W_q intreccia L_q con L_0, quindi soddisfa l'ipotesi di P0(b)^cl solo se V(t, ·) = q + c(t). La conclusione è che un encoder di Volterra indipendente dal tempo esiste solo per V della forma q(x) + c(t). Il contenuto è corretto, ma va scritto.

**Severità.** MINOR.

**Riparazione.** "Si applica a ogni encoder di Volterra W_q con q ∈ C^∞(J°) (che, per ENC-1, manda C^∞(J°) in sé ed è iniettivo): se W_q soddisfa l'ipotesi, allora V(t, x) = q(x) + c(t) + cost".

### P6. Lineare indipendenza delle m·φ_k e caso degenere: nessuna obiezione

Con m continua, m(x*) ≠ 0 e U intervallo su cui m ≠ 0, le funzioni φ_k ∈ C^∞_c(U), non nulle e a supporti disgiunti, danno funzioni m·φ_k non nulle a supporti disgiunti, che sono linearmente indipendenti. Questo passo è corretto. Esiste sempre una successione infinita di tali φ_k, perché U è un intervallo non degenere. La conclusione "per ogni x" segue dalla continuità di m. W = 0 (nucleo infinito) mostra che l'ipotesi dim ker W < ∞ non si può eliminare, ma questa non è un'obiezione. **Nessuna severità.** Con la riparazione (i) di P1 il nucleo della prova è solido.

---

## Parte II — ENC-T2(c′)

### P7. "Certifica" non è definito, e la verità dell'enunciato dipende dalla classe ammessa

**Bersaglio.** ENC-T2(c′): "nessun getto finito j^N u in (t_1, x_1) certifica Ann_q(u) = (P_*)".

**Obiezione.** La prova usa implicitamente questa definizione: "j^N u certifica A se ogni u′ ∈ C^∞(Ω) con lo stesso N-getto soddisfa A". In questa classe (C^∞(Ω) senza vincoli) l'enunciato è vero, ed è sostanzialmente banale. Nel contesto di T2(b), però, la classe naturale è quella dei dati con annullatore **principale**, eventualmente con un vincolo a priori sul grado. In questa classe:

(a) *La prova scritta non basta.* Con u = e^{x²}, q = 0 (Ann_0(u) = (τ)) e h = e^{αt}x^M (α ≠ 0), il dato u′ = u + h ha τ(τ − α) e τσ^{⌊M/2⌋+1} in Ann_0(u′), ma τ ∉ Ann_0(u′). Il loro gcd è τ, quindi Ann_0(u′) **non è principale** (sezione B dello script, con M = 5 e α = 2). L'u′ costruito esce dalla classe, e non mostra la non certificazione dentro di essa. Nell'esempio la conclusione si salva cambiando h con h = e^{αt}x^M e^{x²}, che dà Ann_0(u′) = (τ(τ − α)), principale e diverso da (τ). Un argomento generale di questo tipo, però, non è scritto.

(b) *Con un vincolo di grado l'enunciato è falso.* Sia 𝒞_1 la classe delle u ∈ C^∞(Ω) con Ann_0(u) principale e generato da un elemento di grado totale ≤ 1. u = e^{x²} sta in 𝒞_1 con Ann = (τ). Se u′ ∈ 𝒞_1 ha lo stesso 4-getto in (t_1, 0), si scrive il generatore come P = c_0 + c_1τ + c_2σ. Imponendo che il 2-getto in x di Pu′ si annulli si ottiene c_0 − 2c_2 = 0 e c_0 − 6c_2 = 0, quindi c_0 = c_2 = 0 e P = c_1τ (sezione C dello script). Dunque Ann_0(u′) = (τ): **il 4-getto certifica Ann_q(u) = (τ) nella classe 𝒞_1**. "Per ogni N nessun getto certifica" è quindi falso se la certificazione è relativa a una classe con vincolo di grado.

**Severità.** MAJOR. Nella lettura implicita (classe C^∞ senza vincoli) l'enunciato è vero, ma "certifica" non è definito, e nella lettura più vicina al contesto (annullatori principali) la prova ha una lacuna.

**Riparazione.** Definire esplicitamente: "un getto certifica A se ogni u′ ∈ C^∞(Ω) con lo stesso getto soddisfa A". Aggiungere che l'enunciato non vale relativamente a classi con vincoli a priori sul grado del generatore (citare il controesempio). Se si vuole la versione dentro la classe degli annullatori principali, serve un'altra perturbazione: per esempio h = e^{αt}(x − x_1)^M g(x), con g scelta in modo che (x − x_1)^M g non sia annullata da alcun polinomio non nullo in L_q. Questo va dimostrato.

### P8. Ipotesi Ann_q(u) = (P_*) non dichiarata

**Bersaglio.** "Sia P_* ≠ 0."

**Obiezione.** L'enunciato non dice che Ann_q(u) = (P_*). Se non lo è, l'affermazione è banalmente vera, ma l'intenzione è chiaramente quella. Il caso Ann_q(u) = 0 è escluso implicitamente da P_* ≠ 0, e va bene così: senza annullatore non c'è nulla da certificare.

**Severità.** MINOR.

**Riparazione.** "Sia Ann_q(u) = (P_*) con P_* ≠ 0."

### P9. "Potenze più alte di x − x_1, perché q aumenta il grado": formulazione scorretta, conclusione corretta

**Bersaglio.** Prova di (c′), espansione di L_q^j(x − x_1)^M.

**Obiezione.** q(x)(x − x_1)^k non è un polinomio (sezione A2: con q = 1/(1 + x), L_q x³ = x(x² − 6x − 6)/(x + 1)), e q non "aumenta il grado": moltiplicare per q lascia l'ordine di annullamento in x_1 uguale (≥ k). L'affermazione corretta è questa: per induzione, L_q^j(x − x_1)^M = (−1)^j M!/(M − 2j)!·(x − x_1)^{M−2j} + (x − x_1)^{M−2j+2}·g_j(x), con g_j ∈ C^∞. Il resto vale grazie all'identità ∂_x²[(x − x_1)^k g] = (x − x_1)^{k−2}[k(k − 1)g + 2k(x − x_1)g′ + (x − x_1)²g″] per k ≥ 2, e la condizione M > 2d garantisce k ≥ 2 a ogni passo. Il termine q·(x − x_1)^{k} è di ordine k = (k − 2) + 2, cioè due ordini sopra il termine principale. Per j < d i termini sono di ordine ≥ M − 2d + 2. Il termine dominante di P_*(α, L_q)(x − x_1)^M è quindi p_d(α)(−1)^d M!/(M − 2d)!(x − x_1)^{M−2d} ≠ 0. Verifica SymPy con q generico di Taylor (sezione A): coefficienti −6p_1, 120p_2, −5040p_3, 1680p_2 per (d, M) = (1, 3), (2, 5), (3, 7), (2, 8), tutti uguali a quelli attesi. Regolarità: serve q ∈ C^{2d−2} vicino a x_1, che è garantita da q ∈ C^∞(J°) e x_1 ∈ J°.

**Severità.** MINOR.

**Riparazione.** Sostituire "potenze più alte" con "un resto della forma (x − x_1)^{M−2j+2}g_j, g_j ∈ C^∞".

### P10. Casi degeneri e scelte della prova: reggono

d = 0 (P_* = p_0(τ), compreso P_* = 1, cioè u = 0): con M > N si ha P_*(∂_t)h = p_0(α)h ≠ 0, e la prova regge. j^N h = 0 in (t_1, x_1): ∂_t^a∂_x^b h(t_1, x_1) = α^a e^{αt_1}∂_x^b(x − x_1)^M|_{x_1} = 0 per b ≤ N < M. Corretto. α esiste perché p_d ≢ 0 ha un numero finito di radici, e si può prendere α reale (h reale, nel caso di dati reali) o α immaginario puro (h limitata anche con I illimitato). u′ = u + h ∈ C^∞(Ω), ed è analitica se u lo è, per cui la prova regge anche nella classe analitica. "Non usa W": vero. **Nessuna severità**, al più un'osservazione MINOR: conviene notare la scelta di α reale o immaginario se la classe ha vincoli di realtà o di limitatezza.

---

## Verdetti

- **ENC-P0(b)^cl — WOUNDED.** Così com'è scritto è mal tipizzato con V solo continuo (P1, CRITICAL), e "equivalentemente" non è un'equivalenza (P4, MAJOR). Aggiungendo V(t, ·) ∈ C^∞(J) (o la variante (ii) di P1) il nucleo della prova è corretto. La frase su ENC-1 va precisata (P5, MINOR).
- **ENC-P0(b)^loc — KILLED come enunciato** (controesempio esplicito P2: V = t·w con w continua, mai liscia su alcun intervallo, W(g + wf) = g). Si ripara con la stessa ipotesi di regolarità su V, oppure con la finitezza del nucleo sull'intero dominio di W, più il codominio (P3).
- **ENC-T2(c′) — SURVIVES nella lettura "u′ ∈ C^∞(Ω) arbitraria"** (prova corretta, casi degeneri inclusi), ma con riserve: "certifica" va definito (P7, MAJOR, con controesempio in classe a grado limitato e lacuna nella classe degli annullatori principali), va dichiarata l'ipotesi Ann_q(u) = (P_*) (P8, MINOR) e va corretta la frase "q aumenta il grado" (P9, MINOR). Se il revisore intende la certificazione relativa alla classe di T2(b), il verdetto scende a WOUNDED.
