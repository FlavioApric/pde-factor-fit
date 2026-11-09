# AUDIT S10-OPEN-B · auditor S-CHECK-F10-B · 27/10/2026

Oggetto: il pacchetto `work/S10-OPEN-B/` (PROOF_PACKAGE.md, CHECK_REQUEST.md, LEDGER_ROWS.md, open_questions.md, sympy/). Contesto letto: NOTAZIONE.md fino alla versione 6, claims/LEDGER.md (righe della Fase 5 su OPF5A, OPF5C, OPF5D, OPR2, S4ID), le sezioni citate di OP-F5A (L2, T1, T2, Lemma U, L3′, T4(iv), C1), OP-F5C (L1, T1, L8, P7, P9, T5), OP-F5D (L3–L9, C2, P14, P15), OP-R2 (quadro di §3.1) e AUDIT_OP-F5A (F5A-12, F5A-13).

Ho rieseguito tutti i calcoli con `D:\ProblemaBase\.venv\Scripts\python.exe -I`. Non ho eseguito nessuno script `_vendor` e ho scritto solo questo file. I miei script stanno nella scratchpad della sessione e il loro testo è riportato in Appendice, così che si possano rieseguire.

## 0. Sintesi

| claim | verdetto | stato proposto |
|---|---|---|
| S10B-T1 ([F4⁻]) | PASS-con-fix (T1-a, T1-b, T1-c) | PROVA SCRITTA; DIMOSTRATO quando si applicano i fix, che sono redazionali |
| INT-T1(B) | segue da T1 | PROVA SCRITTA mod S10B-T1 (vedi §1.5) |
| S10B-T2 (OPF5C-T5 senza fonte) | PASS | DIMOSTRATO; anche OPF5C-T5 diventa DIMOSTRATO |
| S10B-P3 (densità di (SB)) | PASS-con-fix (P3-a, P3-b) | PROVA SCRITTA |
| S10B-L4 (L-loc) | PASS-con-fix (L4-a … L4-e) | PROVA SCRITTA; OPF5A-C1 diventa PROVA SCRITTA mod [F1] |
| S10B-C1 (controesempio, domini non convessi) | PASS per l'enunciato; la nota «Lettura» è FALSA come scritta per m ≥ 1 (fix C1-a) | DIMOSTRATO (la densità di OPF5B-T1 su domini non convessi è FALSA) |
| S10B-T3 ([Hm]) | PASS | DIMOSTRATO, per soluzioni u ∈ C(ℝ;𝒮) |
| S4ID-P8, OPR2-P7 | — | CONDIZIONALE su [GT-u] **e** su (WP), l'esistenza globale in 𝒮 (fix R-1) |
| [GT-u] / (U) (§7) | controllo delle riduzioni | APERTO; (U) riformula [GT-u] e non lo riduce |
| INT-Q1 / (R) (§8) | controllo delle riduzioni | APERTO; (R) equivale a INT-Q1 modulo S4ID-P8 |
| S10B-L8′ | PASS-con-fix (L8-a, L8-b) | PROVA SCRITTA |
| S10B-V9 (δ_N(2N) = N+1 per N ≤ 5; δ_5(8) = 9) | calcoli N ≤ 4 riprodotti; N = 5 e δ_5(8) non riprodotti | PROVA SCRITTA assistita da calcolo (vedi §9.3) |
| S10B-P10 | PASS | DIMOSTRATO |
| OPR2-Q3 | — | APERTO; P10 lo caratterizza, e la realizzabilità degli atomi è solo sufficiente |
| OPR2-Q2′ (§11) | — | APERTO; (L) non è formulato con precisione, quindi non c'è riduzione |

Calcoli rieseguiti:
- `s10b_hm.py` 4/4 OK e `s10b_annulus.py` 3/3 OK, identici alle uscite consegnate;
- `s10b_delta.py N 2N N+2 graded` per N = 1..4: stessi gradi minimi 2, 3, 4, 5 (N = 4 in 15.7 s);
- tre controlli nuovi dell'audit: `audit_f4.py` 34/34 OK, `audit_hirota.py` OK, `audit_delta.py` (minoranti indipendenti per k fissato, N ≤ 4);
- un V-ex numerico per L-loc a una seconda nascita (`audit_lloc.py`).

**Nota sulle verifiche del pacchetto.** `s10b_f4.out` contiene solo F1 per N = 1, 2, 3. I controlli F2–F6 annunciati in §1 e in LEDGER_ROWS non hanno uscita su disco, quindi vanno considerati **non eseguiti**. Al loro posto vale il controllo indipendente dell'audit (§1.4).

---

## 1. S10B-T1 ([F4⁻]): N-solitoni di Hirota senza riflessione

### 1.1 Verifica riga per riga

*Passo 1.* Lo sviluppo multilineare per colonne è corretto: la colonna j del Wronskiano è la somma delle colonne di e^{−κ_jx} e di ε_jc_je^{κ_jx}. Ogni scelta S dà det[(s_jκ_j)^{a−1}e^{s_jκ_jx}] = V(s·κ)e^{Σs_jκ_jx}.

*Passo 2.* Ho rifatto i quattro casi dei fattori di ρ(S). Il caso i ∈ S, j ∉ S dà (−κ_j − κ_i)/(κ_i − κ_j) = (κ_i + κ_j)/(κ_j − κ_i) > 0, e il caso i ∉ S, j ∈ S è negativo. Il conteggio dei fattori negativi è corretto:

  C(|S|,2) + Σ_{j∈S}[(j−1) − #{i<j : i∈S}] = Σ_{j∈S}(j−1),

perché Σ_{j∈S}#{i<j : i∈S} = C(|S|,2). La formula del modulo è corretta: Π_{j∈S}d_j si spezza nelle coppie miste, che danno |ρ(S)|, e nelle coppie interne a S, contate due volte. Ne segue W = V_0e^{−Σκ_jx}f, con f a coefficienti positivi.

*Passo 3.* Il coefficiente di g^{(N−1)} in W(φ, g) è −W′ (cofattore dell'ultima colonna), quindi a_{N−1} = −W′/W. La divisione a destra per l'operatore monico A e l'argomento della dimensione su un intervallo dove r_m ≠ 0 sono corretti. Ho rifatto il confronto dei coefficienti con ∂²∘(a∂^{N−1}) = a∂^{N+1} + 2a′∂^N + …:
- all'ordine N+1: q_1 = 0;
- all'ordine N: q_0 = 2a_{N−1}′ = −2(log W)″ = −u.

Dunque L_uA = A(−∂²).

*Passo 4.* L'asintotica è corretta: a +∞ A tende all'operatore monico a coefficienti costanti con nucleo span{e^{κ_jx}}, cioè Π(∂ − κ_j); a −∞ tende a Π(∂ + κ_j). L'unicità della soluzione di Jost normalizzata è implicita: per k reale ≠ 0, una soluzione con ψe^{−ikx} → 1 a +∞ non può contenere e^{−ikx}. Va bene. **L'identificazione con b invece è imprecisa** (fix T1-a, sotto).

*Passo 5.* Corretto: u e tutte le sue derivate sono O(e^{−2κ_1|x|}).

*Passo 6.* Per t fissato si riapplicano i Passi 1–5. Che u(t) risolva KdV è il teorema di Hirota, che qui non è riprovato (fix T1-c).

### 1.2 Fix

- **T1-a (MINOR, identificazione di b).** Nella convenzione di OPF5D (ψ_−(k) = a(k)ψ_+(−k) + b(k)ψ_+(k)) i Wronskiani danno, per x → −∞,

  ψ_+(k) = a(k)ψ_−(−k) − b(−k)ψ_−(k).

  Quindi il coefficiente di e^{−ikx} in ψ_+ a −∞ è **−b(−k)**, non b(k). La conclusione non cambia: il coefficiente è nullo per ogni k ∈ ℝ∖0, dunque b ≡ 0. Va corretta la frase «il coefficiente di e^{−ikx} è b». Il coefficiente di e^{ikx} è effettivamente a(k).
- **T1-b (MINOR, a su Im k > 0).** Il Passo 4 calcola a solo su ℝ∖0. Per usare OPF5D-L4 serve una riga in più: a(k) − Π_j(k − iκ_j)/(k + iκ_j) è analitica in Im k > 0, continua fino a ℝ∖0 e nulla su ℝ∖0, quindi è identicamente nulla per il principio di riflessione (come in OPF5D-L9). Solo così gli zeri iκ_j di a nel semipiano superiore sono quelli della frazione razionale.
- **T1-c (MINOR, portata).** L'enunciato «u(t) è l'N-solitone di KdV» non fa parte di ciò che S10B-T1 prova: dipende dal teorema di Hirota (1971). Nel progetto questo teorema è trattato come definizione della classe dei multi-solitoni (INT-P5/P6, OPF5D-C2). Va scritto così, oppure accompagnato dal V-ex. L'audit ha eseguito il V-ex con `audit_hirota.py`: per N = 2, 3, in sei punti (x, t), il residuo di u_t + 6uu_x + u_xxx è ≤ 4·10⁻⁴¹ a 40 cifre. La convenzione η_j = k_jx − k_j³t corrisponde a c_j(t) = c_j(0)e^{−8κ_j³t}, come scritto.

### 1.3 Kill-argument

Richiesto: trovare N, κ, c per cui W si annulla. È impossibile: W = V_0e^{−Σκx}f con V_0 ≠ 0 e f > 0 (il termine S = ∅ vale 1 e tutti i coefficienti sono > 0). La regola dei segni, che è il punto delicato, è confermata esattamente nei test (§1.4).

Ho cercato anche un'ipotesi mancante:
- per k_i = k_j il Vandermonde si annulla, ma k distinti sono nell'ipotesi;
- c_j > 0 è necessario: con c_j < 0 il fattore ε_jc_j ha il segno sbagliato e f può annullarsi (solitone singolare). L'ipotesi è presente.

Nessun controesempio.

### 1.4 Verifica indipendente (`audit_f4.py`, 34/34 OK)

Con E = e^x, D = E·d/dE e κ interi distinti, tutto è razionale in E e i controlli sono **esatti**:
- W = V_0E^{−Σκ}f per κ = (1,2), (1,3), (2,5), (1,2,3), (1,3,4), (1,2,4,5), (1,2,3,5,7), con c_j razionali positivi casuali. Questo copre la regola dei segni e il modulo fino a N = 5.
- Per N ≤ 3 (cinque casi):
  - (−D² − u)(Ae^{sx}) = −s²Ae^{sx} come identità in (E, s);
  - (Ae^{sx})e^{−sx} → Π(s − κ_j) per E → ∞ e → Π(s + κ_j) per E → 0, cioè b ≡ 0 e la formula di a;
  - la funzione di Crum W(φ_1..φ̂_j..φ_N)/W è autofunzione di autovalore −κ_j² e decade ai due estremi.

### 1.5 Verdetto e stato

**PASS-con-fix (T1-a, T1-b, T1-c).** Stato proposto: **PROVA SCRITTA**; i tre fix sono redazionali e non richiedono un nuovo audit, quindi diventa DIMOSTRATO quando sono applicati.

Per **INT-T1(B)** (OPF5D-C2): T3 è DIMOSTRATO, quindi l'unica dipendenza aperta è S10B-T1. Stato: PROVA SCRITTA mod S10B-T1, e DIMOSTRATO quando si applicano T1-a…c. Resta ferma la convenzione che il multi-soliton sia per definizione una soluzione di KdV (Hirota), vedi T1-c. Va sostituita la riga di LEDGER.md che dice «CONDIZIONALE [F4⁻] … fonte primaria NON TROVATA»: la fonte non serve più.

---

## 2. S10B-T2: J = [A] : H_A^∞ per ideali differenziali primi in una indeterminata

### 2.1 Verifica

- *Irriducibilità di A.* Corretta, anche se non viene usata nel resto della prova.
- *H_A ∉ J.*
  - I_A ha ordine < n oppure sta in F∖0.
  - S_A ≠ 0 perché d ≥ 1 e la caratteristica è 0. Ha grado d − 1 in y_n, oppure ordine < n se d = 1 (in quel caso S_A = I_A).
  - Entrambi hanno rango minore di A, quindi stanno fuori da J per minimalità. Per primalità nessuna potenza di H_A sta in J.
- *⊇.* Immediata.
- *⊆.* La riduzione di Ritt è corretta:
  - le derivate A^{(i)}, i ≥ 1, sono lineari in y_{n+i} con iniziale S_A, e permettono di eliminare l'ordine > n;
  - la pseudo-divisione algebrica per A rispetto a y_n usa l'iniziale I_A;
  - il resto R ha rango minore di A ed è in J, quindi R = 0.
- *Applicazione.* J_u è il nucleo dell'omomorfismo P ↦ P[u] verso l'anello delle funzioni analitiche su un intervallo connesso, che è integro. Quindi J_u è primo. È differenziale perché ∂(P[u]) = (∂P)[u], ed è D_F-stabile perché ∂_t(P[u]) = (D_FP)[u]. La condizione «(I_AS_A)^m D_FA ∈ [A]» di OPF5C-T5 segue da D_FA ∈ J_u = [A] : H_A^∞.

### 2.2 Kill-argument

- Caratteristica p: S_A può essere nullo (y_n^p), ma l'ipotesi richiede caratteristica 0.
- Più indeterminate: non basta un solo polinomio, ma l'enunciato è in una indeterminata.
- OPF5C-T5 è enunciato esattamente in ℂ{y}, «una sola indeterminata, derivazione D». Ho verificato il testo in OP-F5C §4.

Nessun difetto.

*Osservazione redazionale, non bloccante.* Nell'applicazione il campo dei coefficienti va preso dentro le funzioni meromorfe sull'intervallo (in OPF5C-T5 è ℂ), perché P[u] abbia senso e l'anello d'arrivo sia integro.

### 2.3 Verdetto

**PASS.** Stato proposto: **DIMOSTRATO**. Di conseguenza OPF5C-T5 passa da CONDIZIONALE (numero Ritt/Kolchin non verificato) a **DIMOSTRATO**, con la prova autonoma S10B-T2 al posto della citazione.

---

## 3. S10B-P3: densità di (SB) dentro Morse

### 3.1 Verifica

*Passo 1.* ψ_i = (x − m_i)χ(x − m_i) è dispari attorno a m_i, quindi la sua primitiva ha supporto compatto: la perturbazione non introduce una deriva di U_0. Inoltre ψ_i(m_i) = 0, quindi x_i non cambia. ψ_i′ = 1 vicino a m_i, e ψ_i″ è supportato nella corona, dove |u_0″| ≥ c. Ne segue che i punti critici di u_0′ e le loro hessiane sono invariati, e che il solo valore critico spostato è u_0′(m_i). Corretto.

*Passo 2.*
- Un altro minimizzante a′ = m_i + 2πn (n ≠ 0) è escluso, perché un minimizzante soddisfa X_{t_i}(a′) = x_i, mentre X(m_i + 2πn) = x_i + 2πn. Quindi il sollevamento di Θ_i, nullo vicino a tutti i traslati di m_i, non crea problemi.
- La scelta di r_i è lecita: m_i è isolato in M_{t_i}(x_i), che è compatto.
- Nella finestra X_t è strettamente crescente: J_{t_i} ≥ 0 con zero isolato, perché u_0′ è monotona su ciascun lato di m_i, dato che non ci sono altri punti critici nella finestra.
- Dopo la perturbazione M_{t_i}(x_i) = {m_i}.
- La condizione 0 < ε < η_i è superflua: basta ε > 0, perché su C_i vale Φ + εΘ_i ≥ Φ ≥ Φ(m_i) + η_i.
- La perturbazione θ_i = Θ_i′ alza Φ_x **di ε per tutti gli x e tutti i t** fuori dalla finestra i. È proprio questo che rende necessario il Passo 3.

*Passo 3.* L'apertura delle condizioni SB_j in C^3 è corretta e coincide con l'apertura di Morse+(SB), già approvata in F5A-12. È la riga che mancava nello schizzo di F5A-12: i tempi candidati sono finiti e invariati esattamente da ψ_i (per j ≠ i) e da θ_i, e le condizioni ai tempi già trattati hanno margini aperti. L'ordine di scelta «ε_i minore della metà dei margini j < i» chiude l'induzione.

### 3.2 Kill-argument e fix

- **P3-a (MINOR, redazionale).** Nel Passo 1 i candidati m_1..m_p sono fissati *prima* delle perturbazioni. Un minimo locale di u_0′ con u_0′(m) = 0 esattamente non è un candidato (tempo infinito). Le perturbazioni ψ_i e θ_i non spostano il suo valore critico, quindi la densità non ha lacune. Va però scritto in modo esplicito che l'insieme dei candidati è invariato dalle perturbazioni (Passi 1–2). È anche consigliabile scegliere ε generico nel Passo 1 così che nessun valore critico sia nullo. In questo modo ũ_0 resta in Morse+(SB) anche dopo perturbazioni C^3 piccole su (0, T] con T arbitrario, cioè l'apertura di F5A-12 si applica senza eccezioni.
- **P3-b (MINOR).** Va scritto esplicitamente che tutte le perturbazioni hanno supporto in finestre di lunghezza < 2π attorno ai punti di 𝕋. Va anche scritta la topologia C^r in cui si misura ε_0: ‖ψ_i‖_{C^r} e ‖θ_i‖_{C^r} sono finiti, quindi ‖ũ_0 − u_0‖_{C^r} ≤ Σ|ε|‖·‖_{C^r} < ε_0.

Ho cercato un controesempio in cui la perturbazione crei una nuova coincidenza a un tempo t_j con j > i: viene trattato al passo j. Con j < i è escluso dal margine. Nuovi tempi candidati non nascono, perché l'insieme dei valori critici è invariato. Nessun controesempio.

### 3.3 Verdetto

**PASS-con-fix (P3-a, P3-b).** Stato proposto: **PROVA SCRITTA**. Con l'apertura (F5A-12), la classe Morse+(SB) è aperta e densa mod i fix, e OPA-Q2 «generico» cessa di essere CONDIZIONALE quando P3 sarà DIMOSTRATO.

---

## 4. S10B-L4 (= L-loc)

### 4.1 Verifica per sottosezione

**4.1 (margine).** Corretto, ma l'ordine dei quantificatori va reso esplicito (fix L4-a). Prima si sceglie z_0, piccolo quanto richiesto da 4.2; poi, per semicontinuità superiore di M e continuità di Φ_x(a) − min Φ_x, si scelgono r_b, τ_b, η_0. Questo è possibile per *ogni* z_0, perché per (SB) M_{t_b}(x_b) = {a_b}. Le code |a| → ∞ sul rivestimento sono controllate dal termine (x − a)²/2t. Il peso della regione |α| ≥ z_0 è O(ν^{−1/4}e^{−η_0/2ν}) rispetto alla massa principale, quindi trascurabile per ν ≤ ν_0(η_0).

**4.2 (geometria locale).** L'identità J_t(a_b + α) = (t/t_b)J_{t_b}(a_b + α) + η è corretta, ed è la stessa di L2(a). Per t ≤ t_b vale J_t ≥ 1 − t/t_b ≥ 0 nella finestra, perché u_0′ ≥ u_0′(a_b) vicino al minimo locale. Le stime L2(b) dentro la finestra seguono dalla convessità locale, oltre la finestra dal margine. Corretto per t ≤ t_b.

**4.3 (pre-shock).**
- Le identità del Passo 1 di T1 (⟨ψ′⟩ = 0, ⟨zψ′⟩ = 2ν) e lo sviluppo ψ′ = pz + qz²/2 + ρ_3 sono **globali**, quindi valgono senza localizzare. Servono solo le stime dei momenti, che vengono da 4.1–4.2.
- Il Passo 2 di T1 usa «dx = J_t da, X_t crescente, biiettiva» **globalmente**. Dopo la prima nascita questo è falso: J_t < 0 vicino ai minimi già passati. Va sostituito con la biiezione locale di X_t dalla finestra su |x − x_b| < r_b (fix L4-b).
- La monotonia di J_t su ciascun lato di a_b richiede che z_0 sia minore della distanza di a_b dagli altri punti critici di u_0′ (fix L4-b).
- La parte esterna |x − x_b| ≥ r_b è corretta: il compatto 𝒦_b, J > 0 su 𝒦_b e il ricoprimento a scatole di L3 (punti tripli inclusi, perché T_1 ∪ T_3 è finito per T4(iv)). Va però detto che τ_b è minore della distanza da t_b agli altri tempi di T_1 (fix L4-d). Senza questa condizione J > 0 su 𝒦_b non segue.

**4.4 (post-shock).**
- La forma normale Ψ_τ, Lemma U e L3′ sono effettivamente locali: usano il getto di u_0 in a_b fino all'ordine 5, la crescita A⁴ dentro la finestra e, per le code, il margine. Il margine c'è già in T2 dopo il fix F5A-6, quindi la sostituzione «margine al posto della convessità globale» era già stata fatta e approvata (KA U sopravvissuto).
- **Lacuna redazionale (fix L4-c).** La «regione intermedia» (|ξ| > Ξ, |x − x_b| < r_b) è trattata «con le stime L2 locali», ma 4.2 le prova solo per t ≤ t_b. Per t > t_b la finestra non è convessa. Le stime corrette sono quelle di T2, «Struttura»:

  ψ ≥ max(0, c_1(z⁴ + α²z²) − Cτz²),  ψ ≤ C(z⁴ + α²z² + τz²),  per |z| ≤ z_0,

  con il margine per |z| ≥ z_0. Sono locali e valgono qui senza modifiche, ma vanno citate al posto di 4.2.
- L'ordine delle costanti K′_{(b)} → Ξ → ν̂_0 → K_1 → K′_{(a)}, con poi τ_b ≤ min(τ_0, margine di 4.1), non è circolare: ridurre τ_b conserva 4.1.

**4.5 (conclusione).** Per τ_b minore della metà delle distanze tra nascite, è attiva al più una finestra. Il resto di (0, T] è coperto da L3. La costante di T1 a t_b dipende da η = 1 − t/t_b invece che da |t − t_b|, con una differenza O(ν). Il sup vale ν|log ν| + O(ν). Corretto.

### 4.2 Kill-argument (richiesto su 4.4)

Il caso proposto è una seconda nascita, o un minimizzante non degenere, vicino ad a_b ma fuori dalla finestra.
- Per |x − x_b| < 2r_b e |t − t_b| ≤ τ_b è escluso da 4.1. La scelta z_0 → (r_b, τ_b) è possibile per ogni z_0, quindi non c'è competizione tra «z_0 piccolo» (per Taylor) e «r_b, τ_b grandi».
- Per |x − x_b| ≥ r_b il minimizzante è non degenere e conta in 𝒦_b.
- Uno shock preesistente che entra in |x − x_b| < r_b entro τ_b è escluso per τ_b piccolo: a t_b gli shock vecchi distano positivamente da x_b, perché M_{t_b}(x_b) = {a_b}, e le velocità sono limitate.
- Una nascita simultanea in un altro punto è esclusa da (SB).

Il kill-argument **non riesce**.

V-ex dell'audit (`audit_lloc.py`), con u_0 = sin x + 0.45 sin(2x + 1):
- u_0′ ha due minimi locali, −1.4737 in a = 3.9962 e −0.5444 in a = 1.3578;
- la prima nascita è a t_1 = 0.6786, la seconda a t_2 = 1.8370, x_2 = 2.7044;
- a t_2 il minimizzante di Φ_{x_2} è a_2 (argmin 1.35772), quindi è una seconda nascita genuina, con uno shock già presente in x ≈ 3.61.

Integrale interno ∫_{|x−x_2|<0.25}|u − v|dx, Cole–Hopf con passo ν/6 in x:

| t − t_2 | ν = 10⁻³ | 3·10⁻⁴ | 10⁻⁴ |
|---|---|---|---|
| 0 | (I − pred)/ν = −1.086 | −1.085 | −1.087 |
| −0.02 | −1.354 | −1.261 | −0.458 |
| +0.02 | −0.841 | −0.398 | +0.877 |

Qui pred = 2ν log(1/max(|t − t_2|, √ν)). A t_2 lo scarto è costante a tre cifre; a |t − t_2| = 0.02 è limitato (transizione √ν ↔ d). Il risultato è coerente con la forma di L-loc dentro la finestra. È solo un V-ex: la parte esterna e l'uniformità in t non sono verificate numericamente.

### 4.3 Fix

- **L4-a.** Ordine esplicito: z_0 (da 4.2), poi r_b, τ_b, η_0 (da 4.1), poi ν_0(η_0).
- **L4-b.** In 4.3, Passo 2: sostituire «dx = J_t da» globale con la biiezione locale di X_t dalla finestra su |x − x_b| < r_b; richiedere che z_0 sia minore della distanza di a_b dagli altri punti critici di u_0′.
- **L4-c.** In 4.4, regione intermedia: citare le stime di T2, «Struttura», più il margine, non 4.2, che vale solo per t ≤ t_b.
- **L4-d.** Richiedere τ_b < dist(t_b, T_1∖{t_b}) per avere J > 0 su 𝒦_b.
- **L4-e.** Le frasi «parola per parola» (T1 Passi 1–4, Lemma U) vanno accompagnate dall'elenco dei punti in cui la prova originale usa la convessità globale o l'unicità globale. Sono tre: L2(b) per le code, il Passo 2 di T1 e la «Struttura» di T2. Per ciascuno va indicato il sostituto locale. Con L4-b e L4-c l'elenco è completo, per quanto ho verificato.

### 4.4 Verdetto

**PASS-con-fix (L4-a … L4-e).** Non ho trovato errori matematici. La prova resta in parte a livello di rinvio («si ripete»), e il rischio indicato dall'autore (4.4) è in realtà già coperto da F5A-6 e KA U. Stato proposto: **PROVA SCRITTA**. Di conseguenza **OPF5A-C1 (= OPA-Q1)** su tutto (0, T] per Morse+(SB) passa da CONDIZIONALE [L-loc] a **PROVA SCRITTA mod [F1]** (= mod [K-U], fonte verificata), e diventa DIMOSTRATO mod [F1] quando L-loc sarà DIMOSTRATO.

---

## 5. S10B-C1: controesempio alla densità fuori dai convessi

### 5.1 Verifica

- Le strisce orizzontali (0,3) × I_j, con I_1 = (0.4, 0.6) e I_2 = (2.4, 2.6), evitano [1,2]² perché y ∉ [1,2]. Sono prodotti di intervalli, quindi connesse e contenute in Ω. Lo stesso vale per le strisce verticali.
- Su un prodotto di intervalli, ∂_xF = 0 in 𝒟′ implica F = g(y) q.o., con g ∈ L²_loc. Allora (∫_{I_2×I_j} − ∫_{I_1×I_j})F = 0 e Λ(F) = 0. Simmetricamente per ∂_y.
- |Λ(F)| ≤ 25²·4·0.2‖F‖_{L²}, quindi Λ è continuo su L²(Ω) e si annulla sulla chiusura L² di ker Q_1 + ker Q_2, che contiene la chiusura H^m.
- u = φ(x)φ(y) è liscia e limitata con tutte le derivate, e u_xy = φ′(x)φ′(y) ha supporto in [1,2]², chiuso e disgiunto da Ω. Quindi u ∈ ker_{H^m(Ω)}P per ogni m. Infine Λ(u) = 1.

### 5.2 Kill-argument

Ho controllato tre possibili obiezioni: che Λ sia continuo su L² e non solo su H^m (lo è), che le strisce siano in Ω (lo sono) e che OPF5B-T1 riguardi esattamente la somma Σ ker_{H^m}Q_j con P = Q_1Q_2 coprimi (sì). Nessun difetto.

### 5.3 Nota «Lettura»: FALSA come scritta per m ≥ 1 (fix C1-a)

La nota dice che ogni Ω in cui un rettangolo coordinato con lati in Ω circonda **un punto** di ℝ² ∖ Ω dà lo stesso controesempio. Per m ≥ 1 è falso: basta un foro puntiforme. Sia Ω = (0,3)² ∖ {p}.
- Per u ∈ H^1, u_xy ∈ H^{−1} ha supporto in {p}, quindi è una combinazione finita di derivate di δ_p. Ma δ_p ∉ H^{−1}(ℝ²), perché ∫(1 + |ξ|²)^{−1}dξ = ∞. Dunque u_xy = 0 su tutto il quadrato.
- Lo stesso argomento mostra che ker_{H^m}Q_j su Ω coincide con quello sul quadrato.
- Il quadrato è convesso, quindi per OPF5B-T1 la densità vale.

Per m = 0 la nota è invece vera: u = H(x − p_1)H(y − p_2) sta in L², u_xy = δ_p è nullo su Ω e Λ(u) = 1.

**Fix C1-a:** riformulare la nota. Il controesempio vale per ogni m se ℝ² ∖ Ω contiene, dentro il rettangolo, un rettangolo coordinato chiuso con interno non vuoto: basta prendere u = φ_1(x)φ_2(y) con φ_i′ supportati nei lati di quel rettangolo. Per un foro puntiforme vale solo per m = 0. La condizione generale è l'esistenza di u ∈ H^m con supp u_xy ⊂ ℝ² ∖ Ω e Λ(u) ≠ 0.

La domanda 6 di open_questions va precisata nello stesso senso.

### 5.4 Verdetto

**PASS** per l'enunciato e la prova di S10B-C1. Stato proposto: **DIMOSTRATO**: la densità di OPF5B-T1 su domini non convessi è **FALSA** in generale, già in L². La riga di LEDGER «Domini non convessi: APERTO» (P2-Q1, OPF-Q3) diventa «FALSO in generale (S10B-C1); caratterizzazione dei domini APERTA». La nota «Lettura» va corretta (C1-a) prima della registrazione.

---

## 6. S10B-T3 ([Hm])

### 6.1 Verifica

*Passo 1.*
- Ho rifatto il segno. Per u_t − 6uu_x + u_xxx = 0 la trasformazione di Gardner classica è u = w + εw_x + ε²w². Il cambio u ↦ −u, w ↦ −w dà, per la convenzione del progetto (+6uu_x), u = w + εw_x − ε²w², con w_t + 6(w − ε²w²)w_x + w_xxx = 0. Coincide con H1, che ho rieseguito: OK.
- L'inversione formale w_n = −∂w_{n−1} + Σ_{i+j=n−2}w_iw_j è corretta.
- L'operatore (1 + ε∂ − 2ε²w) è invertibile ordine per ordine.
- La forma di conservazione −∂(3w² − 2ε²w³ + w_xx) è corretta.

*Passo 2.* L'omogeneità di peso n + 2 (pesi: ε = −1, u = 2, ∂ = 1) è corretta.

*Passo 3.* Ho rifatto la parte quadratica. ∫∂^iu ∂^{k−i}u = (−1)^{n−1−i}∫(∂^{n−1}u)², e Σ_{m=−(n−1)}^{n−1}(−1)^m = (−1)^{n−1}. Il risultato (−1)^{n+1}∫(∂^{n−1}u)² è corretto; H3 lo conferma per n ≤ 5.

*Passo 4.*
- Il potenziale Σj_i² cambia di 2(j_k − j_1 + 1) < 0 per j_1 > j_k + 1, quindi la riduzione termina.
- Alla fine j_1 ≤ j_2 + 1, quindi 2j_1 − 1 ≤ D ≤ 2n − 4 e j_1 ≤ n − 2. Corretto.

*Passo 5.*
- La disuguaglianza di Gagliardo–Nirenberg su ℝ è ‖f‖_∞ ≤ ‖f‖_2^{1/2}‖f′‖_2^{1/2}, insieme all'interpolazione L² tra M_0 e X. Per j ≤ m − 1 i due esponenti sono < 1.
- γ = (2n + 1 − 3d/2)/(n − 1) ≤ 2 − (3/2)/(n − 1) < 2 per d ≥ 3. Corretto.
- Per n = 1 (m = 0) il Passo 5 non ha senso, ma l'enunciato è banale: è la conservazione della norma L².

*Passo 6.* X² ≤ |H_{2n}(0)| + C(M_0)(1 + X^γ) con γ < 2 implica sup_tX < ∞. H_{2n}(0) è controllato da ‖u(0)‖_{H^{n−1}} con lo stesso argomento. Corretto, e senza induzione.

*Rieseguito:* `s10b_hm.py` 4/4 OK.

### 6.2 Kill-argument

Il coefficiente della parte quadratica non è mai nullo: è ±1. Un monomio di grado ≥ 3 con j_1 = n − 1 è escluso dal Passo 4. La conservazione per u ∈ C(ℝ;𝒮) è lecita: u_t = −(u_xxx + 6uu_x) ∈ C(ℝ;𝒮), quindi u ∈ C^1(ℝ;𝒮) e si può derivare sotto il segno di integrale. Nessun difetto.

### 6.3 Coerenza con OPF5D-P14/P15

In OP-F5D (riga 215) [Hm] è esattamente «sup_t‖u(t)‖_{H^m} < ∞ per KdV con dati di Schwartz», per ogni m. S10B-T3 lo prova **per la soluzione globale in 𝒮**, la cui esistenza resta un'ipotesi: è la (WP), CON-FONTE secondaria, la stessa ipotesi di OP-C3′.

### 6.4 Verdetto

**PASS.** Stato proposto: **DIMOSTRATO**, come enunciato per soluzioni u ∈ C(ℝ;𝒮(ℝ)).

**Fix R-1 (sulle righe a valle in LEDGER_ROWS).** «S4ID-P8, OPR2-P7: CONDIZIONALE solo su [GT-u]» va corretto in «CONDIZIONALE su [GT-u] e (WP)», perché senza l'esistenza globale in 𝒮 S10B-T3 non si applica. In LEDGER la colonna di [Hm] passa da «CON-FONTE secondaria KVZ» a «S10B-T3 (DIMOSTRATO) mod (WP)».

---

## 7. [GT-u]: esito (c)

La «riduzione» [GT-u] ⟸ (U), cioè «costanti di GT (5.20)–(5.21) limitate per k_0 in compatti», è corretta ma **tautologica**: (U) è [GT-u] riscritto in termini delle costanti della prova. La continuità in k_0 di ogni passo di GT §5 è un'affermazione plausibile e non verificata, come il pacchetto stesso ammette. Deift–Zhou non è letto. La lettura di GT pp. 20–24 non è stata ripetuta dall'audit. Coincide con F5D-11.

Stato proposto: **APERTO**, senza «ridotto a (U)», perché (U) non è un enunciato più semplice. S4ID-P8 e OPR2-P7 sono CONDIZIONALI su [GT-u] e (WP) (fix R-1).

## 8. INT-Q1 (dati analitici): esito (c)

Nella combinazione del pacchetto, il ramo «origine non singolare ⇒ T6» è **superfluo**, e T6 da solo non darebbe la contraddizione. Per ordine ≥ 4, T6 dà solo code esponenziali, che non contraddicono r ≢ 0. Il ramo è chiuso invece da S4ID-P8 stesso: «origine non singolare» significa parte lineare non nulla, e P8 (mod [GT-u]) esclude ogni relazione con parte lineare non nulla se r ≢ 0. Per lo stesso P8 la forma iniziale di ogni relazione sta in I_PW. Quindi

  (R) ⟺ INT-Q1 (mod S4ID-P8, mod [GT-u]):

(R) non è una riduzione, è la domanda stessa ristretta alla classe in cui P8 già confina ogni relazione. Il pacchetto lo dice in parte («non è un risultato nuovo oltre la combinazione»). L'osservazione che servono termini sottodominanti dell'asintotica e che la relazione di Airy (OP-O5) sta in questa classe è corretta e utile.

Stato proposto: **APERTO**. La formulazione corretta è «equivalente, mod S4ID-P8 e [GT-u], a (R)». Il rinvio a T6 va tolto o spiegato.

---

## 9. OPF5C-Q1: L8′ e valori di δ_N

### 9.1 L8′

La prova di OPF5C-L8 usa K ≤ 2N − 1 in un solo punto: l'uguaglianza P_k^{(K)} = (F_0..F_{N−1}) ∩ ℂ[y_0..y_K] (OPF5C-T1(c)). Il lemma di sollevamento delle sizigie di Koszul e il resto non dipendono da K. Ho verificato il testo di L8 dopo il fix F5C-4. Per K = 2N servono due precisazioni.

- **L8-a (MINOR, forma iniziale sbagliata).** Il pacchetto scrive che la forma iniziale del generatore aggiunto è y_{2N}. Non è così. Per L1 la mappa Ψ è un automorfismo polinomiale omogeneo pesato. Il flusso in x di Mumford, lo stesso che usa lo script (V′ = (V² + f)/U − (y_0 + λ)U, divisione esatta), è polinomiale e pesato. Quindi y_{2N} = Φ(k; y_0..y_{2N−1}) su Z_k, con Φ polinomio omogeneo di peso 2N + 2 in (k, y). La forma iniziale, cioè la componente di peso massimo in y, è **y_{2N} − Φ(0; y)**. La regolarità della successione non cambia: y_{2N} − Φ(0; y) è monico in una variabile nuova, quindi non è divisore di zero modulo (F⁺).
- **L8-b (MINOR, analogo di T1(c)).** Va enunciato e giustificato che P_k^{(2N)} = (F, y_{2N} − Φ(k; ·)). Questo è l'ideale del grafico di una funzione regolare su Z_k, che è ridotto (T1(b)), e coincide con l'ideale delle relazioni d'ordine 2N degli N-solitoni (chiusura di Zariski, T1(c), più il grafico). Con a e b il resto di L8 si applica parola per parola. Il calcolo graduato di `s10b_delta.py` valuta esattamente su V(F⁺, y_{2N} − Φ(0; ·)) ⊇ grafico su Ψ_0^{−1}(S°_0): lo script calcola y_{2N} dal flusso a k = 0.

Verdetto L8′: **PASS-con-fix (L8-a, L8-b)**. Stato proposto: **PROVA SCRITTA**.

### 9.2 Calcoli

- `s10b_delta.py` differisce da `OP-F5C/sympy/opf5c_delta.py` solo per la riga d'intestazione (Compare-Object). La direzione del certificato è valida: rango pieno mod p per ogni peso a gradi < best implica nessuna relazione omogenea su ℚ di grado < best. Una nullità spuria mod p potrebbe solo abbassare best, quindi il minorante resta valido.
- **Riprodotto:** N = 1..4 con K = 2N dà gradi minimi 2, 3, 4, 5 (N = 4: 15.7 s), identici a `s10b_delta_K2N_graded.out`.
- **Non riprodotto:** N = 5, K = 10 (3231 s). C'è solo l'uscita dell'autore.
- **Controllo indipendente** (`audit_delta.py`, senza Gelfand–Dickey né flusso di Mumford). I getti sono calcolati dai momenti D^mf/f dell'N-solitone di Hirota (cumulanti, y_j = 2D^{j+2}log f) mod p, per k razionali fissati:
  - k = (1,3), (2,7): nessuna relazione di grado ≤ 2 in ℂ[y_0..y_4] (nullità a grado ≤ 3 = 3);
  - k = (1,3,4), (2,5,9): nessuna di grado ≤ 3 in ℂ[y_0..y_6] (nullità a grado ≤ 4 = 4);
  - k = (1,3,4,6): nessuna di grado ≤ 4 in ℂ[y_0..y_8].

  È coerente con δ_N(2N)(k) = N + 1 per questi k. È un V-ex per k fissati e non dipende da L8′.
- δ_5(8) ≥ 9: si legge in `OP-F5C/sympy/opf5c_delta0_5.out` (run concluso, 5336 s, EXIT 0). K = 8 = 2N − 2, quindi si usa L8 (DIMOSTRATO), **non** L8′. Il maggiorante viene da OPF5C-P7(b) (δ_5(8) ≤ 9). Il run non è stato riprodotto né dall'audit né da S-CHECK-19, che è precedente al run.

### 9.3 Stati

- **S10B-V9, δ_N(2N) = N + 1 per ogni k ∈ U_0:**
  - N ≤ 4: PROVA SCRITTA assistita da calcolo (riprodotto), mod L8′ (PROVA SCRITTA) e mod (Nov) (maggiorante OPR2-P4). Diventa «DIMOSTRATO (computer-assisted)» quando L8′ sarà DIMOSTRATO.
  - N = 5: lo stesso, ma **non riprodotto**. Serve un rerun indipendente (circa 55 min).
- **δ_5(8) = 9:** PROVA SCRITTA assistita da calcolo, non riprodotto. Non dipende da L8′.
- **OPF5C-Q1:** APERTO. La «riduzione a limiti inferiori graduati a k = 0» è corretta per K = 2N − 2 e 2N − 1 via L8, e per K = 2N via L8′. È una vera riduzione: elimina il parametro k.

---

## 10. S10B-P10 e OPR2-Q3

### 10.1 Verifica

Con L_u := {T ∈ 𝔇 : Tu ∈ 𝒯} (OP-R2 §3.1) e 0 ∈ 𝒯, si ha 𝔇P ⊆ L_u per ogni u con Pu = 0.
- (⇐, ¬(I)): T_1 ∈ 𝔇P dà T_1u = 0 ∈ 𝒯 per ogni u, quindi il criterio dichiara ogni u non identificante, e questo è corretto per ¬(I).
- (⇐, insieme colpitore): corretto, usando L_u = 𝔇P per u identificante (OP-ALG-T4).
- (⇒): sotto (I), T_i ∈ 𝔇P falsificherebbe il criterio su u*, e la proprietà di colpire segue dalla definizione.
- Conseguenza 2: se gli L_{u_λ} sono a due a due intersecanti in 𝔇P, ogni T ∉ 𝔇P sta in al più uno di essi. Corretto.
- Conseguenza 3: atomi distinti corrispondono a sottomoduli semplici distinti, la cui intersezione è nulla. Corretto.

L'implicazione (I) + (II) ⇒ (II′) «via OPF5B-T6 (u_λ = R_λu*)» non è stata verificata in questo audit. È un'osservazione e non entra nell'enunciato di P10.

### 10.2 Kill-argument

- Se 𝒯 non contenesse 0, il primo caso cadrebbe; ma 𝒯 è un 𝔄-sottomodulo.
- Il «criterio» richiede l'equivalenza per *ogni* u con Pu = 0, ed è usato in questo senso.

Nessun difetto.

### 10.3 Verdetto

**P10: PASS.** Stato proposto: **DIMOSTRATO**.

**OPR2-Q3: APERTO.** Va detto con precisione che P10 è la *caratterizzazione* (nessun insieme colpitore finito di 𝓛), mentre la «realizzabilità degli atomi» è solo una condizione **sufficiente** per l'assenza di test finiti, non una riduzione equivalente. La conseguenza 1, cioè che (I) è necessaria, è DIMOSTRATA con P10.

## 11. OPR2-Q2′

(L) non è formulato in modo verificabile: le ipotesi «i lati e l'interno non danno interazioni non compatte» e la classe degli operatori di Gram non sono definite. Nessuna prova è scritta, e il pacchetto lo dice. Inoltre la riga di LEDGER per OPR2-Q2′ elenca altri casi aperti (d_j ≠ 0, ordine ≥ 2, m ≥ 1) che §11 non tocca. Stato proposto: **APERTO**, senza «ridotto a (L)».

---

## 12. Righe proposte per il coordinatore (correzioni a LEDGER_ROWS)

- S10B-T1: **PROVA SCRITTA**, DIMOSTRATO dopo T1-a…c. SymPy: audit_f4 34/34 e audit_hirota OK; s10b_f4 incompleto (solo F1, N ≤ 3). Proof-checker S-CHECK-F10-B PASS-con-fix; KA sopravvissuto.
- INT-T1(B): PROVA SCRITTA mod S10B-T1, con la convenzione «multi-soliton = soluzione di Hirota» esplicita. Si sostituisce la riga CONDIZIONALE [F4⁻].
- S10B-T2: **DIMOSTRATO**. OPF5C-T5: **DIMOSTRATO** (la fonte non serve più).
- S10B-P3: **PROVA SCRITTA** (fix P3-a, P3-b).
- S10B-L4: **PROVA SCRITTA** (fix L4-a…e), con V-ex dell'audit sulla seconda nascita. OPF5A-C1/OPA-Q1: **PROVA SCRITTA mod [F1]** per Morse+(SB).
- S10B-C1: **DIMOSTRATO** (FALSO l'estensione di OPF5B-T1 ai domini non convessi). La nota «Lettura» va corretta (C1-a).
- S10B-T3: **DIMOSTRATO**, per u ∈ C(ℝ;𝒮).
- S4ID-P8, OPR2-P7: **CONDIZIONALE** su [GT-u] e (WP) (fix R-1).
- [GT-u]: **APERTO** (togliere «ridotto a (U)»).
- INT-Q1: **APERTO**, equivalente a (R) mod S4ID-P8 e [GT-u] (togliere il rinvio a T6).
- S10B-L8′: **PROVA SCRITTA** (fix L8-a, L8-b).
- S10B-V9: PROVA SCRITTA assistita da calcolo (N ≤ 4 riprodotto; N = 5 e δ_5(8) non riprodotti).
- OPF5C-Q1: APERTO, ridotto al caso graduato.
- S10B-P10: **DIMOSTRATO**.
- OPR2-Q3: APERTO, caratterizzato da P10; la realizzabilità degli atomi è sufficiente.
- OPR2-Q2′: **APERTO**.

---

## Appendice A: `audit_f4.py` (34/34 OK)

```python
import sympy as sp, random, itertools, sys
E, s = sp.symbols('E s')
def D(g): return sp.together(E*sp.diff(g, E))
def Dn(g, n):
    for _ in range(n): g = D(g)
    return g
def wr(fs):
    n = len(fs); M = sp.Matrix(n, n, lambda a, b: Dn(fs[b], a)); return sp.factor(M.det())
ok = []
def rep(name, c): ok.append(bool(c)); print(('OK  ' if c else 'FAIL') + ' ' + name)
random.seed(5)
cases = [(1, 2), (1, 3), (2, 5), (1, 2, 3), (1, 3, 4), (1, 2, 4, 5), (1, 2, 3, 5, 7)]
for kap in cases:
    N = len(kap)
    c = [sp.Rational(random.randint(1, 9), random.randint(1, 9)) for _ in range(N)]
    eps = [(-1)**j for j in range(N)]
    phi = [E**(-kap[j]) + eps[j]*c[j]*E**kap[j] for j in range(N)]
    W = wr(phi)
    V0 = sp.Mul(*[(-kap[j]) - (-kap[i]) for i in range(N) for j in range(i+1, N)])
    d = [sp.Mul(*[sp.Rational(kap[j]+kap[l], abs(kap[j]-kap[l])) for l in range(N) if l != j]) for j in range(N)]
    k = [2*q for q in kap]; f = 0
    for r in range(N+1):
        for S in itertools.combinations(range(N), r):
            term = sp.Mul(*[c[j]*d[j]*E**(2*kap[j]) for j in S])
            term *= sp.Mul(*[sp.Rational(k[i]-k[j], k[i]+k[j])**2 for i, j in itertools.combinations(S, 2)])
            f += term
    rep('T1-W kappa=%s' % (kap,), sp.simplify(W - V0*E**(-sum(kap))*f) == 0)
    if N > 3: continue
    u = sp.together(2*D(D(f)/f))
    Ag = sp.cancel(sp.together(wr(phi + [E**s])/W/E**s)); psi = Ag*E**s
    rep('T1-L', sp.simplify((-Dn(psi, 2) - u*psi + s**2*psi)/E**s) == 0)
    rep('T1-A+', sp.expand(sp.limit(Ag, E, sp.oo) - sp.Mul(*[s - q for q in kap])) == 0)
    rep('T1-A-', sp.expand(sp.limit(Ag, E, 0) - sp.Mul(*[s + q for q in kap])) == 0)
    for j in range(N):
        others = [phi[i] for i in range(N) if i != j]
        pj = sp.cancel(wr(others)/W) if others else sp.cancel(1/W)
        r2 = sp.simplify(-Dn(pj, 2) - u*pj + kap[j]**2*pj)
        rep('T1-ev j=%d' % (j+1), r2 == 0 and sp.limit(pj, E, sp.oo) == 0 and sp.limit(pj, E, 0) == 0)
print('TOTALE: %d/%d OK' % (sum(ok), len(ok)))
```

## Appendice B: `audit_hirota.py` (OK, residuo ≤ 4·10⁻⁴¹)

```python
import mpmath as mp, itertools
mp.mp.dps = 40
def make(k, e0):
    N = len(k)
    def f(x, t):
        s = 0
        for r in range(N+1):
            for S in itertools.combinations(range(N), r):
                a = mp.mpf(1)
                for i, j in itertools.combinations(S, 2): a *= ((k[i]-k[j])/(k[i]+k[j]))**2
                s += a*mp.exp(sum(k[i]*x - k[i]**3*t + e0[i] for i in S))
        return s
    return lambda x, t: 2*mp.diff(lambda z: mp.log(f(z, t)), x, 2)
worst = 0
for k, e0 in [((mp.mpf(1), mp.mpf(2)), (0.3, -0.7)), ((mp.mpf('0.8'), mp.mpf('1.7'), mp.mpf('2.9')), (0.1, 0.5, -1.2))]:
    u = make(k, e0)
    for (x, t) in [(-1.3, 0.2), (0.4, -0.5), (2.1, 0.9)]:
        r = mp.diff(lambda s: u(x, s), t) + 6*u(x, t)*mp.diff(lambda z: u(z, t), x) + mp.diff(lambda z: u(z, t), x, 3)
        worst = max(worst, abs(r))
print(worst)
```

## Appendice C: `audit_delta.py` (minoranti indipendenti per k fissato)

```python
import random, itertools, time
import numpy as np
from math import comb
P = 2147483629
def inv(a): return pow(a % P, P-2, P)
def rank_mod(M):   # eliminazione di Gauss mod P (come in opf5c_delta.py)
    M = M.copy() % P; r = 0; rows, cols = M.shape
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0: continue
        piv = r + nz[0]
        if piv != r: M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r]*inv(int(M[r, c]))) % P
        oth = np.nonzero(M[:, c])[0]; oth = oth[oth != r]
        if len(oth): M[oth] = (M[oth] - (M[oth, c].reshape(-1, 1)*M[r]) % P) % P
        r += 1
        if r == rows: break
    return r
def jets(k, K):    # getti y_0..y_K dell'N-solitone di Hirota in un punto X casuale (D X_i = k_i X_i), via cumulanti
    N = len(k); X = [random.randrange(1, P) for _ in range(N)]; terms = []
    for r in range(N+1):
        for S in itertools.combinations(range(N), r):
            a = 1
            for i, j in itertools.combinations(S, 2): a = a*((k[i]-k[j]) % P)**2 % P*inv((k[i]+k[j])**2) % P
            for i in S: a = a*X[i] % P
            terms.append((a, sum(k[i] for i in S) % P))
    f = sum(a for a, _ in terms) % P
    F = [(sum(a*pow(l, m, P) for a, l in terms) % P)*inv(f) % P for m in range(K+3)]
    kap = [0]*(K+3)
    for n in range(1, K+3): kap[n] = (F[n] - sum(comb(n-1, m-1)*kap[m]*F[n-m] for m in range(1, n))) % P
    return [2*kap[j+2] % P for j in range(K+1)]
# per k in [(1,3),(2,7),(1,3,4),(2,5,9),(1,3,4,6)], K = 2N: rango della matrice dei monomi di grado <= N
# su #monomi+20 punti; rango pieno => nessuna relazione di grado <= N (delta_N(2N)(k) >= N+1).
```

## Appendice D: `audit_lloc.py` (V-ex di L-loc, seconda nascita)

u_0 = sin a + 0.45 sin(2a + 1), U_0 = −cos a − 0.225 cos(2a + 1). I minimi locali di u_0′ si trovano con brentq su u_0″, e la seconda nascita (t_b, a_b, x_b = a_b + t_bu_0(a_b)) si sceglie verificando che argmin Φ_{x_b} ≈ a_b. Per ν ∈ {10⁻³, 3·10⁻⁴, 10⁻⁴} e t ∈ {t_b, t_b ± 0.02} si calcola:
- la griglia in x con passo ν/6 su |x − x_b| < 0.25;
- la griglia in a con passo min(√(νt)/12, ν^{1/4}/40) su |a − a_b| < 1;
- u = Σ((x − a)/t)w/Σw, con w = exp(−(Φ − min Φ)/2ν);
- v = (x − a*)/t, con a* = argmin raffinato con interpolazione parabolica;
- I = Σ|u − v|h.

Il risultato si confronta con 2ν log(1/max(|t − t_b|, √ν)). Le uscite sono nella tabella del §4.2.
