# AUDIT S10-OPEN-B, rev2 · auditor S-CHECK-F10-B2 · 27/10/2026

Oggetto: la sezione «Recepimento dell'audit (rev2)» (R1, R3–R12) di `work/S10-OPEN-B/PROOF_PACKAGE.md`, confrontata con l'audit precedente `work/CHECK-F10/AUDIT_S10-OPEN-B.md`. Ho letto anche, per i claim nuovi, l'enunciato e la prova di S4ID-P8 (`work/S4-ID/PROOF_PACKAGE.md`, §6), le righe di LEDGER su S4ID-P8, INT-Q1 e OPR2-Q2′, e il testo di F5A-12 in `work/CHECK/AUDIT_OP-F5A.md`.

Tutti i calcoli sono stati eseguiti con `D:\ProblemaBase\.venv\Scripts\python.exe -I`. Non ho eseguito script in `_vendor`. Ho scritto solo questo file e gli script `work/CHECK-F10/sympy/b2_*.py`; le loro uscite sono riportate qui sotto e non sono salvate nel progetto.

## 0. Sintesi

| claim | verdetto | stato proposto |
|---|---|---|
| S10B-T1 ([F4⁻]), fix T1-a, b, c | PASS | DIMOSTRATO |
| INT-T1(B) | segue da T1 | DIMOSTRATO, con la convenzione «multi-solitone = soluzione di Hirota» (T1-c) |
| S10B-P3, fix P3-a, b | PASS-con-fix (P3-c, redazionale) | DIMOSTRATO (densità); «aperta e densa» DIMOSTRATO dopo P3-c |
| S10B-L4 (L-loc), fix L4-a … e | PASS (una precisazione redazionale, non bloccante) | DIMOSTRATO mod [F1]; OPF5A-C1 DIMOSTRATO mod [F1] |
| S10B-C1, fix C1-a | PASS (una precisazione redazionale, non bloccante) | DIMOSTRATO |
| S10B-T3 / fix R-1 (R6) | PASS | DIMOSTRATO per u ∈ C(ℝ;𝒮); S4ID-P8, OPR2-P7 CONDIZIONALI su [GT-u] e (WP) |
| [GT-u] (R7) | PASS | APERTO, senza riduzione |
| S10B-E8 (R8), nuovo | PASS-con-fix (E8-a) | DIMOSTRATO come implicazione mod S4ID-P8, quindi CONDIZIONALE su [GT-u] e (WP); INT-Q1 APERTO |
| S10B-L8′, fix L8-a, b (R9) | PASS | DIMOSTRATO |
| S10B-V9 (R9) | invariato | N ≤ 4: DIMOSTRATO (computer-assisted) mod (Nov); N = 5 e δ_5(8): PROVA SCRITTA assistita da calcolo, non riprodotti; N = 6 NON ESEGUITO |
| OPR2-Q3 (R10) | PASS | APERTO, caratterizzato da P10 |
| S10B-P11 (R11), nuovo | PASS (kill-argument non riuscito) | DIMOSTRATO |
| OPR2-Q2′ (R11) | — | APERTO; condizione sufficiente (L-v) a ogni vertice, perché (L-int) è dimostrabile (§11.4) |

Calcoli:
- `s10b_f4.py noF1` rieseguito: **18/18 OK** in 47 s, uscita identica riga per riga a `sympy/s10b_f4_rev2.out`;
- `b2_t1a_jost.py` 10/10 OK (fix T1-a);
- `b2_p3_zero_min.py` 6/6 OK (lacuna P3-c);
- `b2_l8_novikov.py` 6/6 OK (fix L8-a);
- `b2_e8_ipw.py` 9/9 OK (precisione di (R));
- `b2_p11_lint.py` 7/7 OK (identità della prova di P11; (L-int) per Hilbert–Schmidt).

Nota di forma: la sezione di recepimento salta da R1 a R3, e la verifica rigenerata (che nel mandato era il punto 2) sta dentro R1. Inoltre la tabella del §0 del pacchetto riporta ancora gli stati della prima versione. La nota in testa al file dice che la sezione R prevale, quindi non c'è ambiguità, ma conviene aggiornare il §0 o rinviare alla tabella R12.

---

## 1. R1: S10B-T1, fix T1-a, T1-b, T1-c

**T1-a.** Ho rifatto i Wronskiani. Con ψ_+(k) ~ e^{ikx} a +∞, ψ_−(k) ~ e^{−ikx} a −∞ e ψ_−(k) = a(k)ψ_+(−k) + b(k)ψ_+(k), si ha W(ψ_+(k), ψ_+(−k)) = −2ik e W(ψ_−(k), ψ_−(−k)) = 2ik. Da qui a(k)a(−k) − b(k)b(−k) = 1 e ψ_+(k) = a(k)ψ_−(−k) − b(−k)ψ_−(k), come scritto in R1. Il coefficiente di e^{−ikx} in ψ_+ a −∞ è −b(−k), quello di e^{ikx} è a(k). Poiché il Passo 4 lo trova nullo per ogni k ∈ ℝ∖0, b ≡ 0.

`b2_t1a_jost.py` lo controlla in tre modi:
- in forma astratta, su uno spazio di soluzioni di dimensione 2 con Wronskiano antisimmetrico;
- esattamente per u = gδ;
- per un potenziale non simmetrico u = (3/2)δ(x) − (1/3)δ(x − 1).

Il terzo caso serve perché per u pari b è immaginario puro su ℝ e −b(−k) coincide con b(k). Nel caso non simmetrico invece, a k = 7/10, il coefficiente vale 0.0229 + 1.2824i mentre b(k) = −0.0229 + 1.2824i. La correzione T1-a era quindi necessaria come enunciato, anche se non cambiava la conclusione b ≡ 0.

**T1-b.** L'argomento è corretto. h := a − R è analitica in Im k > 0, continua fino a ℝ∖0 e nulla su ℝ∖0. Per riflessione di Schwarz si estende a una funzione analitica sul dominio connesso (Im k ≠ 0) ∪ (ℝ∖0), nulla su un intervallo, quindi è identicamente nulla. Gli zeri di a nel semipiano superiore sono quelli di R, cioè iκ_1, …, iκ_N, e OPF5D-L4 si applica. Il controllo dell'audit precedente (`audit_f4.py`) era già un'identità nella variabile simbolica s = ik, quindi copriva anche la continuazione analitica.

**T1-c.** La portata è scritta correttamente: S10B-T1 prova il contenuto spettrale per ogni t fissato, mentre il fatto che t ↦ u(t) risolva KdV è il teorema di Hirota, assunto come definizione della classe dei multi-solitoni (INT-P5/P6, OPF5D-C2).

**Verifica rigenerata.** Ho rieseguito `s10b_f4.py noF1`: 18/18 OK, con gli stessi numeri di `s10b_f4_rev2.out` (F4 ≤ 1.8·10⁻⁴¹; F5 4.75·10⁻¹⁹⁷ e 4.42·10⁻¹⁹⁶; F6 ≤ 9.05·10⁻¹⁷). Il FAIL del run precedente (F5, N = 3, 2.3·10⁻¹⁴) scompare con la sostituzione esatta: è coerente con un artefatto di `lambdify`. F1 per N ≤ 4 è in `s10b_f4.out` (4/4). La tolleranza di F6 (10⁻¹⁰) è larga, ma l'errore osservato è dell'ordine atteso e^{−2κ_1·40} ≈ 4·10⁻¹⁸ moltiplicato per costanti O(10), quindi il test è informativo.

**Verdetto: PASS.** S10B-T1 → **DIMOSTRATO**. INT-T1(B) → **DIMOSTRATO**, con la convenzione T1-c.

---

## 2. R3: S10B-P3, fix P3-a, P3-b

**P3-b** è corretto: supporti in finestre di lunghezza < 2π, esclusione dei traslati m_i + 2πn tramite X(m_i + 2πn) = x_i + 2πn, stima in norma C^r. L'osservazione che 0 < ε < η_i è superflua è recepita correttamente.

**P3-a** è corretto nella parte essenziale: l'insieme dei candidati è fissato prima, ψ_i sposta solo u_0′(m_i), θ_i non tocca punti né valori critici. C'è però una lacuna nella frase aggiunta.

**P3-c (MINOR, redazionale).** R3 dice che nel Passo 1 si sceglie ε generico «in modo che nessun valore critico di u_0′ sia nullo». Con le sole perturbazioni del Passo 1 questo non è possibile. I bump ψ_i stanno solo nei candidati m_i, cioè nei minimi con valore critico < 0, e non spostano un minimo locale con valore critico esattamente 0. `b2_p3_zero_min.py` lo mostra con u_0′ = −cos x − cos 2x:
- x = π è un minimo locale non degenere di u_0′ con valore 0;
- x = 0 è il candidato, con t = 1/2;
- il bump del Passo 1 in 0 sposta il valore in 0 di ε e lascia invariato il valore in π;
- una perturbazione C^r di norma δ/2 porta il valore in π a −δ/2 e crea un nuovo tempo candidato t = 2/δ.

Quindi un tale u_0 sta in Morse+(SB) ma non ne è un punto interno in C^3 se (SB) si richiede per tutti i tempi. La correzione è semplice: si aggiunge un bump dello stesso tipo (con ε > 0) in ogni minimo locale di u_0′ con valore 0, che diventa positivo e non è un candidato. Lo si può fare anche in tutti i punti critici. La costruzione del Passo 1 vale per qualunque punto critico di Morse.

Questa lacuna **non** tocca la densità: ũ_0 sta in Morse+(SB) anche con un minimo a valore 0, perché quel minimo non è un candidato. Tocca solo l'affermazione «aperta e densa», che dopo P3-c va letta così: Morse+(SB)+(nessun valore critico nullo) è aperto e denso in C^r. In alternativa si può restare con «per perturbazioni piccole su (0, T] con T fissato», dove la lacuna non c'è (il nuovo tempo 2/δ supera T).

**Verdetto: PASS-con-fix (P3-c).** S10B-P3 (densità) → **DIMOSTRATO**. L'enunciato «aperta e densa» è DIMOSTRATO una volta applicato P3-c, che è redazionale e non richiede un nuovo audit.

---

## 3. R4: S10B-L4 (L-loc), fix L4-a … L4-e

- **L4-a.** L'ordine z_0 → (r_b, τ_b, η_0) → τ_b < dist(t_b, T_1∖{t_b}) → ν_0 è esplicito e non circolare. Il punto 2 è lecito per ogni z_0: per (SB) l'unico minimizzante a t_b in x_b è a_b, quindi Φ_{x_b} − min Φ_{x_b} > 0 sul compatto |α| ≥ z_0 (la coda sul rivestimento è controllata da (x − a)²/2t), e il margine persiste per continuità in (t, x).
- **L4-b.** La biiezione locale è corretta. Per t ≤ t_b, J_t = (t/t_b)J_{t_b} + η, con J_{t_b} ≥ 0 sulla finestra e nullo solo in a_b, quindi J_t > 0 su W_b∖{a_b}. X_t è strettamente crescente su W_b, il minimizzante di ogni x con |x − x_b| < r_b sta in |α| < z_0/2 per 4.1 ed è unico (convessità in finestra più margine), e x ↦ a(x) è l'inversa di X_t|_{W_b}. La monotonia di J_t su ciascun lato di a_b segue da z_0 < distanza dagli altri punti critici.

  *Precisazione redazionale, non bloccante.* La formula finale di L4-b, «∫|∂_aJ_t|/J_t da = 2 log(1/max(√ν, η)) + O(1)», non vale per l'integrale preso su tutto l'intervallo: quello dà 2 log(1/η) + O(1), perché J_t(a_b) = η. Il taglio a √ν viene dalla regione interna del Passo 3 di T1, come nella prova originale. Basta scrivere «sull'intervallo esterno alla regione interna del Passo 3».
- **L4-c.** Corretto. Le stime di T2 «Struttura» sono locali in |z| ≤ z_0, con il margine per |z| ≥ z_0. Le stime di 4.2 non sono più usate per t > t_b.
- **L4-d.** Corretto. Per OPF5A-L4 un minimizzante degenere sta in un minimo locale di u_0′ e il suo tempo appartiene a T_1. Con τ_b < dist(t_b, T_1∖{t_b}), per t ≠ t_b nella finestra temporale non ci sono minimizzanti degeneri, e a t = t_b l'unico è (x_b, a_b) per (SB). Quindi J > 0 sull'insieme chiuso 𝒦_b, e J ≥ 2j_0 > 0 per compattezza.
- **L4-e.** La tabella elenca i tre punti indicati dall'audit precedente, con i sostituti giusti.

Ho cercato un quarto uso globale non elencato. Le identità ⟨ψ′⟩ = 0 e ⟨zψ′⟩ = 2ν sono globali, cioè valgono come identità integrali sul rivestimento. Il Passo 3 di T1 è già locale. Il Lemma U e L3′ sono locali. Non ho trovato altri usi della convessità o dell'unicità globale.

**Verdetto: PASS.** S10B-L4 → **DIMOSTRATO** (mod [F1] nella lettura di v come soluzione entropica). OPF5A-C1 (OPA-Q1) su (0, T] per Morse+(SB) → **DIMOSTRATO mod [F1]**.

---

## 4. R5: S10B-C1, fix C1-a

La nuova nota «Lettura» è corretta.
- *Caso del rettangolo pieno.* Siano R = [x_1, x_2] × [y_1, y_2] con intorni dei quattro lati in Ω, e [p_1, q_1] × [p_2, q_2] ⊂ (ℝ²∖Ω) ∩ int R. Il funzionale Λ costruito con quadratini agli angoli di R, abbastanza piccoli da stare fuori dalle fasce [p_1, q_1] × ℝ e ℝ × [p_2, q_2], si annulla su ker Q_1 + ker Q_2, perché le strisce lungo i lati sono connesse. Con u = φ_1(x)φ_2(y) si ha Λ(u) = 1, e u_xy ha supporto nel rettangolo chiuso, fuori da Ω. Per Ω limitato u ∈ H^m(Ω) per ogni m.
- *Foro puntiforme, m ≥ 1.* H^m(Ω) = H^m(quadrato), perché un punto ha capacità nulla in dimensione 2, e la stessa cosa vale per i nuclei. Una distribuzione non nulla supportata in un punto ha trasformata di Fourier polinomiale e non sta in H^{−1}(ℝ²). Quindi u_xy = 0 sul quadrato, e la densità vale per OPF5B-T1.
- *Foro puntiforme, m = 0.* u = H(x − p_1)H(y − p_2) sta in L², u_xy = δ_p e Λ(u) = 1. Corretto.

*Precisazione redazionale, non bloccante.* La «Condizione generale» va chiamata **sufficiente**: un Λ di quel tipo che separa u dalla chiusura è un testimone di non densità, ma la non densità potrebbe essere testimoniata da altri funzionali. Inoltre la parentesi «cioè supp u_xy ⊂ ℝ²∖Ω nel senso delle estensioni» presuppone un'estensione di u. La condizione di partenza, Pu = 0 su Ω, è quella che conta.

**Verdetto: PASS.** S10B-C1 → **DIMOSTRATO** (l'estensione di OPF5B-T1 ai domini non convessi è falsa in generale).

---

## 5. R6 (fix R-1) e R7 ([GT-u])

R6 recepisce R-1 parola per parola: S4ID-P8 e OPR2-P7 sono CONDIZIONALI su [GT-u] e (WP), e la colonna [Hm] di LEDGER passa a «S10B-T3 mod (WP)». R7 ritira la riduzione a (U) e dichiara [GT-u] APERTO senza riduzione. Entrambi sono conformi all'audit precedente.

**Verdetto: PASS.**

---

## 6. R8: S10B-E8 (claim nuovo)

### 6.1 Che cosa dice S4ID-P8

Dal §6 di `work/S4-ID/PROOF_PACKAGE.md`: sia p ∈ A (polinomi differenziali a coefficienti complessi) d'ordine ≤ K con p(u(t,·)) ≡ 0 per t ≥ T_0, e sia p = Σ_{e≥e_0}p_e la decomposizione in componenti omogenee per **grado ordinario**. Allora, sotto (H-as) (cioè [GT-u] con le derivate, quindi anche (WP) e [Hm]), si ha e_0 ≥ 1 e p_{e_0} ∈ I_PW, dove I_PW è l'insieme dei polinomi omogenei che si annullano sui getti di A cos(κx + θ), con A, κ, θ reali. In particolare p non ha parte lineare non nulla.

### 6.2 Verifica di E8

- (⇒) È banale e non usa P8.
- (⇐) Sia G ≠ 0 con G[u(t)] ≡ 0 per ogni t. Vale in particolare per t ≥ T_0, quindi P8 si applica e dà G(0) = 0 (anche direttamente, perché u(t) ∈ 𝒮) e in(G) ∈ I_PW. Allora G sta nella classe di (R), in contraddizione con (R).

L'implicazione è provata. È un'equivalenza «di restrizione», non una riduzione, come R8 stesso dice e come l'audit precedente aveva chiesto.

I quantificatori sono coerenti. INT-Q1 (S4-ID §6) chiede se possa esistere p ∈ A∖0 con p(u(t,·)) ≡ 0 per ogni t. (R) è enunciato «per ogni u», e l'equivalenza vale sia in forma universale sia per ogni u fissato.

### 6.3 Precisione di (R): fix E8-a (MINOR)

(R) usa in(G) e I_PW senza definirli dentro R8. L'unica definizione di in(G) nel pacchetto è nel §8, «parte di peso minimo nello scaling radiativo», e R8 dichiara di sostituire il §8. Va scritto in R8:
- in(G) := la componente omogenea di **grado ordinario** minimo di G. Nello scaling radiativo il getto è t^{−1/2}(v + o(1)) con lo stesso fattore per ogni derivata, quindi conta il grado ordinario e non un peso che dipende dall'ordine;
- I_PW := {polinomi omogenei che si annullano su (Aκ^j cos(θ + jπ/2))_j per ogni A, κ, θ reali}, come in S4ID-P8;
- r è il coefficiente di riflessione di u(0), e «u(0) analitico» significa analitico reale su ℝ.

Va anche osservato che in (R) la clausola «parte lineare nulla» è **ridondante**. I_PW non contiene forme lineari non nulle, e G(0) = 0 per ogni relazione soddisfatta da una u di Schwartz. Quindi in(G) ∈ I_PW implica già che la parte lineare sia nulla. La clausola non è sbagliata, ma va segnalata come conseguenza.

`b2_e8_ipw.py` controlla questi punti (9/9 OK):
- y_0y_3 − y_1y_2, y_0y_4 − y_2², y_1y_4 − y_2y_3 ∈ I_PW, con la parametrizzazione reale e con quella complessa y_j = Bμ^j + C(−μ)^j (getti di v″ = μ²v, Zariski-densa);
- la parte minima di Π_1, y_1² − k²y_0², e la parte lineare di Novikov y_4 − 5y_2 + 4y_0 non stanno in I_PW;
- nessuna forma lineare non nulla d'ordine ≤ 6 sta in I_PW;
- la componente dominante per ampiezza → 0 è la parte di grado ordinario minimo;
- la classe di (R) non è vuota (per esempio y_0y_4 − y_2² + termini di grado 3).

### 6.4 Verdetto

**PASS-con-fix (E8-a).** S10B-E8 → **DIMOSTRATO come implicazione «S4ID-P8 ⇒ (INT-Q1 "no" ⟺ (R))»**. Poiché P8 è CONDIZIONALE, E8 come enunciato su KdV è CONDIZIONALE su [GT-u] e (WP). INT-Q1 (dati analitici) resta **APERTO**.

---

## 7. R9: S10B-L8′, fix L8-a, L8-b; run N = 6

**L8-a.** Corretto. Φ è pesato-omogeneo di peso 2N + 2 in (k, y), con peso(k) = 1 e peso(y_j) = j + 2. La componente di peso massimo in y è allora la parte a k = 0, cioè y_{2N} − Φ(0; y). È monica di grado 1 nella variabile nuova y_{2N}, e un polinomio monico in una variabile nuova non è divisore di zero in (ℂ[y_0..y_{2N−1}]/(F⁺))[y_{2N}]. La successione resta regolare. La divisione per un generatore monico in y_{2N} con coefficienti polinomiali in k commuta con la specializzazione k = 0, quindi l'argomento di sollevamento di L8 si estende.

`b2_l8_novikov.py` (6/6 OK) controlla L8-a in modo indipendente dal flusso di Mumford, sui getti esatti dell'N-solitone di Hirota a 50–60 cifre:
- N = 1: y_2 = k²y_0 − 3y_0², residuo 7·10⁻⁵²;
- N = 2, con k = (1, 5/2) e (3/4, 7/5): y_4 + 10y_0y_2 + 5y_1² + 10y_0³ + c_1(y_2 + 3y_0²) + c_2y_0 = 0 con c_1 = −(k_1² + k_2²) e c_2 = k_1²k_2², residui ≤ 5·10⁻⁶⁰;
- Φ è pesato-omogeneo di peso 6, e la forma iniziale è y_4 + 10y_0y_2 + 5y_1² + 10y_0³, monica in y_4.

**L8-b.** Corretto. I generatori si annullano sui getti, e questo dà ⊇. Per ⊆: 𝒥 è il grafico di Φ sopra 𝒥′, che è denso in Z_k. La sua chiusura di Zariski è il grafico Γ di Φ|_{Z_k}. Il quoziente per (I_k, y_{2N} − Φ) è isomorfo a ℂ[Z_k], che è ridotto. Per il Nullstellensatz l'ideale è I(Γ) = I(𝒥) = P_k^{(2N)}.

**Stati e run N = 6.** Gli stati riportati in R9 sono quelli dell'audit precedente. Il run (6, 12) fermato e il (6, 11) mai avviato sono dichiarati NON ESEGUITI, in coerenza con `s10b_delta_big_graded.out`.

**Verdetto: PASS.** S10B-L8′ → **DIMOSTRATO**. Di conseguenza, come previsto dall'audit precedente (§9.3), S10B-V9 per N ≤ 4 diventa **DIMOSTRATO (computer-assisted) mod (Nov)**. N = 5 e δ_5(8) = 9 restano PROVA SCRITTA assistita da calcolo finché non vengono riprodotti; il rerun N = 5 richiede circa 55 minuti e non è stato fatto qui.

---

## 8. R10: OPR2-Q3

R10 recepisce la precisazione: P10 è la caratterizzazione, la realizzabilità degli atomi è solo sufficiente, e l'implicazione via OPF5B-T6 è un'osservazione fuori dall'enunciato. Lo stato APERTO è nella forma esatta di P10.

**Verdetto: PASS.**

---

## 9. R11: S10B-P11 (claim nuovo)

### 9.1 Precisione delle ipotesi

Il quadro è preciso. Ω è un poligono convesso limitato, Q_j = n_j·∇ + d_j con direzioni a due a due non parallele e d_j reali, K_j ⊂ L²(Ω) è chiuso, S: ℋ → L² è la mappa somma e 𝒢 = S*S. La partizione Σχ_α² = 1 su Ω̄ esiste: si prende una partizione ζ_α ≥ 0 con i supporti richiesti e si pone χ_α = ζ_α/(Σζ_β²)^{1/2}.

(L-int) e (L-v) sono enunciati con precisione: operatori compatti, costanti, «per ogni f ∈ ℋ». Due precisazioni redazionali:
- (L-v) dipende dalla scelta di χ_v. P11 usa una partizione fissata, quindi l'ipotesi va letta come «esiste una partizione per cui valgono (L-int) e (L-v)»;
- 𝒦_v deve essere compatto e autoaggiunto **su ℋ**, ed è scritto così.

### 9.2 Verifica della prova

- ‖Sf‖² = Σ_α‖χ_αSf‖² segue da Σχ_α² = 1 su Ω, con χ_α reali.
- Termine α = 0: ⟨χ_0f_i, χ_0f_j⟩ = ⟨f_i, P_iχ_0²P_jf_j⟩ perché f_i = P_if_i e f_j = P_jf_j. L'operatore 𝒦_0, con (𝒦_0f)_i = −Σ_{j≠i}P_iχ_0²P_jf_j, è compatto per (L-int) e autoaggiunto perché (P_iχ_0²P_j)* = P_jχ_0²P_i. L'identità ‖Σ_jχ_0f_j‖² = Σ_j‖χ_0f_j‖² − ⟨𝒦_0f, f⟩ è corretta: `b2_p11_lint.py` (a) la controlla su sottospazi casuali, con errore relativo 4.5·10⁻¹⁶.
- Somma: con c = min(1, c_v), il termine α = 0 ha coefficiente 1 ≥ c, e Σ_αΣ_j‖χ_αf_j‖² = ‖f‖²_ℋ. Ne segue ⟨(𝒢 + 𝒦)f, f⟩ ≥ c‖f‖².
- Un operatore autoaggiunto coercivo è invertibile (Lax–Milgram). Quindi 𝒢 = (𝒢 + 𝒦) − 𝒦 è Fredholm di indice 0, con immagine chiusa e nucleo finito. Poiché 𝒢 ≥ 0 è autoaggiunto con immagine chiusa, sul complemento ortogonale del nucleo ha spettro in [c′, ∞), quindi ⟨𝒢f, f⟩ = ‖Sf‖² ≥ c′‖f‖² su (ker S)^⊥. Ne segue che ran S, cioè K_1 + … + K_N, è chiuso.

La prova è completa e corretta.

### 9.3 Kill-argument su P11

1. *Errore nell'implicazione.* Ho controllato i tre punti in cui una prova di questo tipo di solito si rompe: il segno e la realtà della somma dei termini misti, la compattezza dell'operatore incollato su ℋ (non su L²), e il passaggio da «𝒢 Fredholm» a «S a immagine chiusa». Tutti e tre tengono.
2. *Ipotesi vacue o contraddittorie.* Se (L-int) o (L-v) fossero false in ogni caso non banale, P11 sarebbe vuoto. Per (L-int) è vero il contrario: vale sempre in questo quadro (§9.4). Per (L-v) il modello tangente di OPF5B-P8 dà la stima con 𝒦_v = 0 sul cono. Il controesempio di LEDGER (cuneo con due direzioni degeneri nello stesso punto) è esattamente un vertice in cui ci si aspetta che (L-v) fallisca, ed è coerente con la localizzazione della non compattezza vista in §9.4.
3. *Chiusura senza somma diretta.* P11 non richiede che la somma sia diretta: ker S finito-dimensionale è una conseguenza (Fredholm), non un'ipotesi. Per tre direzioni ker S contiene le relazioni polinomiali tra funzioni ridge, che hanno dimensione finita, quindi non c'è conflitto.

Il kill-argument **non riesce**.

### 9.4 (L-int) è dimostrabile (osservazione dell'audit)

R11 dice che (L-int) «non è dimostrata in questa generalità». Un argomento di Hilbert–Schmidt la dà direttamente. Lo riporto come abbozzo da redigere, non come claim registrato.

Sia d_j = 0. Su Ω convesso K_j = {g(σ_j(x))}, con σ_j la coordinata trasversa a n_j, perché ogni corda è connessa. Con la normalizzazione unitaria G ↦ G(σ_j)/ℓ_j(σ_j)^{1/2} (ℓ_j la lunghezza della corda), l'operatore P_iχ_0²P_j: K_j → K_i ha nucleo

  k(s, σ) = χ_0²(x(s, σ)) 𝟙_Ω / (|sin θ_ij| ℓ_i(s)^{1/2}ℓ_j(σ)^{1/2}),

e quindi

  ‖P_iχ_0²P_j‖²_HS = ∫_Ω χ_0⁴ / (|sin θ_ij| ℓ_i(x) ℓ_j(x)) dx.

In un poligono convesso una corda corta ha gli estremi su due lati adiacenti vicino al loro vertice comune: lati non adiacenti hanno distanza positiva, e una corda con estremi sullo stesso lato sta sul bordo. Quindi ℓ_i e ℓ_j sono limitate dal basso sul supporto di χ_0, che evita un intorno dei vertici. L'integrale è finito, e P_iχ_0²P_j è di Hilbert–Schmidt, quindi compatto. Per d_j ≠ 0 si ha K_j = {e^{−d_jτ_j}g(σ_j)}: i pesi e^{±2|d_j|diam Ω} sono limitati, e lo stesso calcolo dà un integrale finito.

`b2_p11_lint.py` (b) lo controlla sul triangolo {x, y > 0, x + y < 1} con le direzioni (1,0), (0,1) e (1,2)/√5, e con χ_0 uguale all'indicatrice di {dist dai vertici > r}:
- la formula integrale coincide con la norma di Frobenius dei proiettori discreti a bande entro il 2.5%;
- HS²(r) è finita per ogni r > 0;
- per le coppie (0,2) e (1,2) cresce come log(1/r), con incrementi 0.73, 0.64, 0.59, 0.61 e 1.93, 1.75, 1.76, 1.82 per ogni dimezzamento di r. Questo accade dove, in un vertice, degenerano entrambe le corde;
- per la coppia (0,1), con entrambe le direzioni parallele a lati, converge (incrementi 0.22, 0.10, 0.045, 0.024), perché in ogni vertice degenera al più una corda.

La non compattezza sta quindi solo ai vertici, ed è quantificata dalla divergenza logaritmica di ∫1/(ℓ_iℓ_j) vicino a un vertice in cui entrambe le corde degenerano.

### 9.5 Verdetto e stato di OPR2-Q2′

**S10B-P11: PASS.** Stato proposto: **DIMOSTRATO** (analisi funzionale elementare).

**OPR2-Q2′** (m = 0, poligono convesso, d_j reali): **APERTO**. Due correzioni di formulazione:
- «ridotto a (L-int) ∧ (L-v)» va scritto «condizione sufficiente (P11)». P11 dà una sola implicazione, e lo stesso criterio è stato applicato a OPR2-Q3 in R10;
- per §9.4, (L-int) è dimostrabile. Una volta redatto e auditato quell'argomento, la condizione sufficiente si riduce a **(L-v) a ogni vertice**, cioè a un problema puramente locale al vertice. Il passaggio dal modello tangente (OPF5B-P8) a (L-v), con gli errori (n_j·∇χ_v)f_j e i termini d_j, resta non dimostrato, come R11 dice correttamente.

P11 non tocca i fattori d'ordine ≥ 2 né m ≥ 1, che restano aperti come nella riga di LEDGER.

---

## 10. Righe proposte per il coordinatore

- S10B-T1: **DIMOSTRATO**. SymPy: s10b_f4 F1 4/4, F2–F6 18/18 (riprodotto); audit_f4 34/34; b2_t1a_jost 10/10. S-CHECK-F10-B PASS-con-fix, S-CHECK-F10-B2 PASS.
- INT-T1(B): **DIMOSTRATO**, con la convenzione «multi-solitone = soluzione di Hirota».
- S10B-P3: **DIMOSTRATO** (densità). «Morse+(SB) aperta e densa» DIMOSTRATO dopo il fix redazionale P3-c (bump anche nei minimi di u_0′ con valore 0), oppure nella forma «aperto e denso: Morse+(SB) senza valori critici nulli».
- S10B-L4: **DIMOSTRATO** mod [F1]. OPF5A-C1 / OPA-Q1 su (0, T] per Morse+(SB): **DIMOSTRATO mod [F1]**.
- S10B-C1: **DIMOSTRATO**. La «Condizione generale» della nota va detta sufficiente.
- S10B-T3: **DIMOSTRATO** per u ∈ C(ℝ;𝒮). S4ID-P8, OPR2-P7: **CONDIZIONALE** su [GT-u] e (WP).
- [GT-u]: **APERTO**.
- S10B-E8: **DIMOSTRATO** come implicazione mod S4ID-P8, quindi CONDIZIONALE su [GT-u] e (WP), dopo E8-a (definire in(G) come parte di grado ordinario minimo e I_PW dentro R8; la clausola «parte lineare nulla» è ridondante). INT-Q1 (analitici): **APERTO**, equivalente a (R).
- S10B-L8′: **DIMOSTRATO**. b2_l8_novikov 6/6.
- S10B-V9: N ≤ 4 **DIMOSTRATO (computer-assisted) mod (Nov)**; N = 5 e δ_5(8) = 9 PROVA SCRITTA assistita da calcolo, non riprodotti; N = 6 NON ESEGUITO.
- OPF5C-Q1: APERTO, ridotto al caso graduato a k = 0.
- OPR2-Q3: APERTO, caratterizzato da P10.
- S10B-P11: **DIMOSTRATO**.
- OPR2-Q2′: **APERTO**; condizione sufficiente (L-int) ∧ (L-v) via P11. (L-int) è dimostrabile per Hilbert–Schmidt (audit §9.4, da redigere), e allora resta (L-v) a ogni vertice.

---

## Appendice: script e uscite

Tutti gli script stanno in `work/CHECK-F10/sympy/` e si eseguono con `D:\ProblemaBase\.venv\Scripts\python.exe -I <script>`.

| script | contenuto | esito | tempo |
|---|---|---|---|
| `s10b_f4.py noF1` (del pacchetto) | F2–F6 | 18/18 OK, identico a `s10b_f4_rev2.out` | 47 s |
| `b2_t1a_jost.py` | T1-a in forma astratta, per u = gδ e per due delta non simmetriche | 10/10 OK | 3 s |
| `b2_p3_zero_min.py` | minimo di u_0′ a valore 0 non spostato dai bump del Passo 1 | 6/6 OK | < 1 s |
| `b2_l8_novikov.py` | y_{2N} = Φ(k; y) pesato-omogeneo e forma iniziale per N = 1, 2, sui getti di Hirota | 6/6 OK | 9 s |
| `b2_e8_ipw.py` | I_PW: esempi, assenza di forme lineari, grado ordinario | 9/9 OK | 2 s |
| `b2_p11_lint.py` | identità del termine α = 0; HS di P_iχ_0²P_j sul triangolo | 7/7 OK | 34 s |
