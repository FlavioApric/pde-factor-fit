# AUDIT-GTU — verifica di [GT-u]

Verificatore: CIT-GT. Data: 2026-10-27.
Punti nel progetto: `work/S10-OPEN-B/PROOF_PACKAGE.md` §7 (riga 265 e segg.), R6, R7 (riga 433 e segg.), tabella finale (righe 537–539).

## Fatto da verificare

[GT-u]: per KdV con dato di decadimento rapido, l'asintotica nella regione di similarità x/t ≤ −C, con errore O(t^{−α}) di Grunert–Teschl, vale uniformemente per x/t in compatti della regione, ed eventualmente anche con le derivate in x.

## Nota sulla numerazione

In Grunert–Teschl (arXiv:0807.5041v2, MPAG 12 (2009) 287–324) **non esiste un "Thm 1.1"**. L'introduzione descrive le regioni in prosa (formula (1.5)) e rimanda a Thm 4.4 (regione solitonica) e Thm 5.4 (regione di similarità). Ogni riferimento a "GT Thm 1.1" va corretto in "GT Thm 5.4", o tolto.

## Fonte 1 — Grunert–Teschl 2009 (letta: pp. 1–3, 18–26, 30 del PDF arXiv v2)

**Thm 5.4 (p. 22).** Ipotesi sul dato: solo il momento (5.26), ∫(1+|x|)^6 |q(x,0)| dx < ∞. Solitoni ammessi: la fase δ(k_0) contiene la somma su κ_j. Conclusione: le formule (5.27) per ∫_x^∞ q e (5.28) per q valgono "in the similarity region, x/t ≤ −C for some C > 0", con errore O(t^{−α}) per ogni 1/2 < α < 1. L'enunciato non contiene la parola "uniformly" e non dice nulla sulla dipendenza della costante da k_0. Il dato riflessione di GT è collegato all'equazione q_t = 6qq_x − q_xxx (convenzione di segno diversa dal progetto; vedi R6).

**Thm 5.1 (p. 19).** È il problema modello sulla croce, attribuito a Deift–Zhou [10] con prova in Krüger–Teschl [25]. Termina con una clausola esplicita di uniformità rispetto ai parametri. Per brevità la parafraso: se R_j e Φ dipendono da un parametro, l'errore è uniforme in quel parametro purché r stia in un compatto del disco unitario e le costanti di (5.4)–(5.6) (C, α, L, ρ_0) siano indipendenti dal parametro. Citazione breve: "the error term is uniform with respect to this parameter".

**Applicazione (pp. 20–21).** Thm 5.1 si applica con parametro k_0, dopo il cambio di variabile (5.16). Le stime di Hölder (5.20)–(5.21) sono enunciate solo come "there is an L > 0", per k_0 fissato. Il dato r di (5.22) ha |r| = |R(k_0)|. Per x/t in un compatto di (−∞, −C] si ha k_0 = √(−x/12t) in un compatto di (0, ∞). Lì |R(k_0)| ≤ ρ < 1, perché |R(k)| < 1 per k ≠ 0 e R è continuo. Quindi la prima ipotesi della clausola, r in un compatto di 𝔻, è soddisfatta. La seconda ipotesi, costanti L uniformi in k_0, non è verificata nel testo. È plausibile (T̃ e R sono regolari e dipendono con continuità da k_0, e la stima di Hölder del Lemma 5.3 viene da un risultato classico), ma GT non la scrive.

**Thm 5.2 (decoupling) e §6.** L'errore di Thm 5.2 "depends on the distance of k to Σ"; in GT la geometria dipende da k_0 tramite ε. Nel §6, Lemma 6.2 e il "Lipschitz estimate … (uniformly in t)" di p. 26 non dicono nulla sull'uniformità in k_0. Il §6 richiede R ∈ C^5, che segue da (4.32).

**Derivate.** Remark 5.5 (p. 23): (5.28) si ottiene "formally" derivando (5.27) in x. GT aggiunge che la legittimità di questo passo si mostra come in Deift–Zhou [11] (CMP 165 (1994) 175–191), ma che il loro metodo la evita. GT quindi **non** enuncia asintotiche per ∂_x^m q, m ≥ 1, e non dimostra la derivabilità termine a termine. [11] non è stato letto.

**Verdetto GT: PARZIALE.** L'asintotica, le ipotesi sul dato (momento (1+|x|)^6, solitoni ammessi) e l'errore O(t^{−α}) sono VERIFICATI. L'uniformità per x/t in compatti **non è enunciata**, ma la prova la fornisce quasi interamente tramite la clausola di Thm 5.1: manca solo il controllo uniforme in k_0 delle costanti L di (5.20)–(5.21) e di ε. Le derivate in x non sono in GT. Rispetto a R7 la valutazione è più favorevole: la frase "Deift–Zhou non è letto" va aggiornata, perché il meccanismo di uniformità è già scritto in GT Thm 5.1.

## Fonte 2 — Deift–Zhou, Annals 137 (1993) 295–368 (mKdV)

Letto solo l'annuncio, Bull. AMS 26 (1992) 119–124 (arXiv:math/9201261), con lo stesso teorema. Per dato y_0 di Schwartz (quindi sup|r| < 1, nessun solitone in mKdV defocusing), il teorema dà asintotiche "uniform leading asymptotics" nelle sei regioni della Figura 3. Nella regione oscillatoria l'errore è espresso con τ = t z_0^3, per esempio (t z_0)^{−1/2} O(τ^{−1/4}) nella regione II. Le regioni sono definite in figura e la figura nel PDF arXiv è vuota. Non c'è un enunciato sulle derivate. Il Remark 4 dice che i solitoni si possono includere "senza difficoltà", senza prova. Il paper Annals completo non è stato letto.

**Verdetto: VERIFICATO per mKdV** (uniformità enunciata nell'annuncio). Per KdV vale come **CONTENUTO DIVERSO**: equazione diversa, |r| < 1 ovunque, nessun solitone. È un'analogia di metodo, non una fonte per [GT-u].

## Fonte 3 — Deift–Venakides–Zhou, CPAM 47 (1994) 199–206

Non letto (non disponibile liberamente). Da GT p. 2: riguarda la regione di shock non collisionale −x ~ t^{1/3}(log t)^{2/3}, caso generico R(0) = −1. Questa regione è disgiunta da x/t ≤ −C. **Verdetto: CONTENUTO DIVERSO** (regione sbagliata per [GT-u]); NON TROVATO come fonte di uniformità.

## Fonte 4 — Its; Its–Novokshenov (LNM 1191, 1986)

Non letti. GT e DZ li citano per il metodo isomonodromico (NLS, Painlevé II). Nessun enunciato KdV con uniformità è stato localizzato. **Verdetto: NON TROVATO.**

## Fonte 5 — Ablowitz–Segur, Stud. Appl. Math. 57 (1977) 13–44

Non letto. Secondo GT p. 3 il risultato è formale, senza l'espressione precisa di δ(k_0) e assumendo assenza di solitoni. **Verdetto: NON TROVATO** come fonte rigorosa. Al massimo è una fonte euristica.

## Fonti secondarie emerse (non richieste, da considerare)

- Buslaev–Sukhanov, J. Sov. Math. 34 (1986) 1905–1920: secondo GT p. 1 giustificazione rigorosa dell'asintotica radiativa KdV, estesa "to all orders". È il candidato più naturale per uniformità e derivate. Non letto.
- Deift–Zhou, CMP 165 (1994): GT Remark 5.5 lo indica come fonte per la differenziabilità in x dell'asintotica. Non letto.

## Conclusione su [GT-u]

**[GT-u] non è CON-FONTE come enunciato esplicito.** Nessuna fonte letta enuncia per KdV l'uniformità per x/t in compatti di {x/t ≤ −C}, e tanto meno con le derivate in x.

Lo stato corretto è **PARZIALE / quasi-CON-FONTE (forma senza derivate)**. Formulazione proposta:

> Per q(·,0) con ∫(1+|x|)^6|q| < ∞ (solitoni ammessi), la (5.28) di GT vale con errore O(t^{−α}) uniforme per x/t in compatti di (−∞, −C]. Questo segue dalla clausola di uniformità di GT Thm 5.1 ("uniform with respect to this parameter"), applicata con parametro k_0 in un compatto di (0, ∞), dove |R(k_0)| ≤ ρ < 1. Resta da verificare che le costanti di Hölder L di (5.20)–(5.21) e l'ε della decomposizione siano limitati per k_0 nel compatto.

Questo controllo residuo è una routine sulle stime di GT stesse (continuità in k_0 di T̃, R e delle loro norme C^α), non un fatto nuovo. Va però scritto oppure preso da Buslaev–Sukhanov o Deift–Zhou 1994, che non sono stati letti.

**Forma con derivate in x: NON CON-FONTE.** GT dichiara la derivazione solo formale (Remark 5.5) e rimanda a Deift–Zhou CMP 1994 senza enunciarla. S4ID-P8 usa le derivate, quindi resta CONDIZIONALE su questa parte finché non si legge DZ CMP 165 o Buslaev–Sukhanov.

Correzioni suggerite al PROOF_PACKAGE:
1. Togliere "Thm 1.1" di GT, che non esiste.
2. In R7, distinguere [GT-u₀], l'uniformità senza derivate, che è quasi-CON-FONTE via GT Thm 5.1 con controllo residuo delle costanti, da [GT-u_m], le derivate, che è APERTO/NON CON-FONTE con candidati DZ 1994 e BS 1986.
3. La frase di R7 "Deift–Zhou non è letto" va aggiornata: l'annuncio BAMS conferma l'uniformità per mKdV (sole regioni, dato di Schwartz, senza solitoni).

Nota procedurale: lo strumento di lettura web ha salvato da sé le copie dei PDF arXiv nella cartella dei risultati degli strumenti. Non ho scaricato nulla nel progetto e non ho eseguito nulla in `_vendor`.
