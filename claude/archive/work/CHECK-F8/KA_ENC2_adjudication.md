# KA ENC2 — aggiudicazione (S-CHECK-F8-ENC-rev2, 27/10/2026)

Attacco: `KA_ENC2_attack.md`, scritto da un subagente indipendente che ha letto solo `KA_ENC2_input.md`; script dell'attaccante `sympy/enc2_ka_checks.py` (output `.out`, ogni sezione dà il risultato atteso). Verdetti dichiarati: ENC-P0(b)^cl **WOUNDED**, ENC-P0(b)^loc **KILLED come scritto**, ENC-T2(c′) **SURVIVES** nella lettura "u′ ∈ C^∞(Ω) arbitrarie".
Avvertenza di metodo: il prompt dell'attaccante elencava alcune piste dal mio controllo preliminare (dominio di W con V solo continuo, regolarità di q, definizione di "certifica", caso d = 0, lineare indipendenza, "equivalentemente", copertura di ENC-1). Su quelle piste l'attacco non è cieco. Sono contributi autonomi: il controesempio esplicito a P0(b)^loc (P2), la lettura "su soluzioni" di P4 e il controesempio con vincolo di grado di P7(b).
Verifica dell'aggiudicatore: ho ricontrollato a mano P2 (W(g + w·f) := g su X ⊕ w·X, con X ∩ w·X = {0} per w continua e liscia su nessun intervallo) e P7(a) (u = e^{x²}, q = 0, u′ = u + e^{αt}x^M: τ(τ − α) e τσ^k stanno in Ann_0(u′) per k > M/2, τ no, quindi l'ideale non è principale). Entrambi sono corretti.

## Punti dell'attacco

**P1 — Con V solo continuo, W viene applicato fuori dal suo dominio (proposto CRITICAL).** *Verdetto: still_unresolved; accolto come MAJOR.* Coincide con il mio ENC2-1, che alzo da MINOR a MAJOR. Con W: C^∞(J) → C^∞(J) e V ∈ C(I × J) l'enunciato è mal tipizzato. Nella lettura "l'identità vale dove ha senso" diventa falso (V = t·w con w liscia su nessun intervallo, W = Id, c = 0: l'ipotesi vale a vuoto). Non lo considero CRITICAL perché la lettura letterale non è un enunciato falso ma un enunciato senza senso, e la riparazione è una riga: (i) V(t, ·) ∈ C^∞(J), oppure (ii) W: D_W → 𝒟′(J) con C(J)·C^∞_c(J) ⊂ D_W e dim ker W < ∞ **su tutto D_W**.

**P2 — Controesempio esplicito a P0(b)^loc (proposto CRITICAL).** *Verdetto: still_unresolved; accolto.* Il nucleo è richiesto finito solo su C^∞_c(U), mentre la prova produce elementi m·φ_k ∈ C_c(U) ∖ C^∞_c(U). Con X := C^∞_c(U), W(g + w·f) := g e V = t·w, l'identità vale, ker W|_X = {0}, e V − c non è autonomo. **ENC-P0(b)^loc è FALSO come scritto.** Severità: MAJOR, per lo stesso criterio usato in ENC2-4 dell'audit rev. 2: il claim è nuovo, DA AUDITARE e non registrato, non sta sul cammino critico, e la riparazione (quella di P1, con "nucleo finito su tutto D_W" oppure V(t, ·) ∈ C^∞(U)) è una riga. Dopo la riparazione la prova "quella di P0(b)^cl" è corretta.

**P3 — Codominio di W non detto in ^loc (MINOR).** *Verdetto: accolto, MINOR.* Scrivere "W: D_W → 𝒟′(U), identità in 𝒟′(U)".

**P4 — "Equivalentemente" non è un'equivalenza (proposto MAJOR).** *Verdetto: accolto; severità MINOR.* Coincide con la nota di ENC2-1. Il verso "intrecciamento su C^∞(I × J) ⟹ identità" è immediato (u indipendente da t). Il viceversa richiede che W sia sequenzialmente continuo su C^∞(J), perché commuti con ∂_t. La lettura "su soluzioni" è più debole e non è provata. Nota: l'attaccante legge l'equazione come u_t = −u_xx + Vu (calore all'indietro), ma nel pacchetto il quadro è i u_t = L_{V(t)}u ("i" nell'estratto è ambiguo con l'articolo). Per Schrödinger le fette temporali delle soluzioni sono più ricche, ma l'implicazione resta comunque non provata. È MINOR perché la frase è accessoria e la prova non la usa. *Riparazione:* "In particolare, se W è sequenzialmente continuo su C^∞(J), W intreccia i∂_t − L_{V(t)} e i∂_t − L_0 − c(t) su C^∞(I × J)", eliminando la lettura sulle soluzioni.

**P5 — "Copre l'encoder di Volterra di ENC-1" (MINOR).** *Verdetto: accolto, MINOR.* Nella forma (i) vale per W_q con q ∈ C^∞(J°). Nella forma (ii) vale anche per q continuo, perché W_q agisce su C(J) ed è iniettivo su C⁰. Va scritta la conclusione esplicita: se un W_q indipendente dal tempo soddisfa l'ipotesi, allora V(t, x) = q(x) + c(t) + costante.

**P6 — Lineare indipendenza, casi degeneri.** *Verdetto: nessuna obiezione*, coincide con il mio controllo.

**P7 — "Certifica" non definito; falso con vincolo di grado; lacuna nella classe principale (proposto MAJOR).** *Verdetto: accolto come MAJOR.* Alzo il mio ENC2-6 da MINOR a MAJOR (OVERSTATED + LOCAL).
- Nella classe dei dati senza vincoli (u′ ∈ C^∞(Ω), che è il modello DM3 del pacchetto) l'enunciato è vero e la prova è completa.
- (b) Relativamente a classi con un vincolo a priori sul grado del generatore l'enunciato è **falso**: il 4-getto di e^{x²} certifica Ann = (τ) fra gli annullatori principali di grado totale ≤ 1.
- (a) Nella classe degli annullatori principali (quella di T2(b)) la perturbazione h = e^{αt}(x − x_1)^M fa uscire dalla classe, quindi la prova non basta. La versione in quella classe è **APERTA**.
La frase "nessun getto certifica" si presta a essere letta in G★″ come un limite generale. Per questo va circoscritta.
*Riparazione:* definire "un getto j^N u in (t_1, x_1) certifica A se ogni u′ ∈ C^∞(Ω) con lo stesso N-getto soddisfa A"; aggiungere che con vincoli a priori sul grado l'enunciato è falso (controesempio P7(b)) e che la versione nella classe degli annullatori principali è aperta.

**P8 — Ipotesi Ann_q(u) = (P_*) non dichiarata (MINOR).** *Verdetto: partially_answered.* La prova mostra che esiste u′ con lo stesso getto e P_* ∉ Ann_q(u′); non serve sapere se Ann_q(u) = (P_*). Va però detto esplicitamente che l'enunciato vale per ogni u ∈ C^∞(Ω). MINOR.

**P9 — "q aumenta il grado" (MINOR).** *Verdetto: accolto.* Coincide con il mio ENC2-6(b): il resto è (x − x_1)^{M−2j+2}g_j con g_j liscia, con q ∈ C^∞ (ipotesi di ENC-C1).

**P10 — Casi degeneri di T2(c′).** *Verdetto: nessuna obiezione*, coincide con T2c′2 e T2c′3.

## Esito

- **ENC-P0(b)^cl: SURVIVES dopo ENC2-1** (MAJOR: ipotesi (i) o (ii); più "equivalentemente" → "in particolare" e la copertura di ENC-1 scritta per esteso, MINOR).
- **ENC-P0(b)^loc: KILLED come scritto**; **SURVIVES dopo ENC2-1** (nucleo finito su tutto D_W, oppure V(t, ·) liscio su U; codominio 𝒟′(U)).
- **ENC-T2(c′): SURVIVES dopo ENC2-6** (MAJOR: definizione di "certifica" sulla classe C^∞(Ω) senza vincoli; versione con vincolo di grado FALSA; versione nella classe principale APERTA).

Effetto sul cammino critico ENC-1 → C1 → T2 → R6: **nessuno**. ENC-P0(b)^cl non è usato da R6. ENC-T2(c′) è un'osservazione accessoria che R6 non usa. ENC-T2(a)(b)(c) ed ENC-C1 sono invariati e restano DIMOSTRATO.
