# Kill-argument su CONV-T2 ("teorema di Gold analitico")

Revisore avversariale indipendente, 27/10/2026. Fonte letta: solo `work/CHECK-F8/KA_CONV_T2_input.md`. Ho rifatto tutti i conti da zero. Lo script di controllo è `work/CHECK-F8/sympy/conv_ka_t2_check.py`.

Il riferimento a T1 (citato nella "Lettura") non è nel file di input. Le affermazioni che ne dipendono le ho ricostruite io, e lo segnalo dove serve.

## Sintesi della prova (come la ricostruisco)

1. **Passo 0.** Se φ sbaglia su un polinomio, la prova è finita. Altrimenti φ converge a "legge" su ogni polinomio.
2. **Lemma (Passo 2).** Per ogni coppia (m, L) esiste un blocco finito di coordinate del jet, di ordine in (L, K₀]. Un'opportuna scelta y\* di queste coordinate dentro il box forza Ann ∩ R_{≤m} = 0, qualunque siano le altre coordinate.
3. **Diagonale (Passi 3–4).** Si alternano due mosse: si inserisce un blocco y\* e si aspetta che φ dica "legge" sul polinomio troncato. Il limite è una funzione intera con Ann = 0, sulla quale φ dice "legge" infinite volte.

L'architettura è quella classica di Gold e Putnam, e il punto delicato è tutto nel lemma: deve essere locale, cioè dipendere solo da un blocco finito di ordini superiori a L. Ho attaccato ogni anello.

## Attacchi

### Attacco 1 — Punto (ii) del Passo 2: a cosa serve?

**Punto attaccato.** Il punto (ii) dice che g = |z|^{2(L+1)} e^{|z|²} si annulla in 0 all'ordine 2(L+1) > L. Il dubbio è se la prova abbia bisogno che i coefficienti di g di ordine ≤ L siano nulli, per esempio per rendere compatibile il blocco di g con il polinomio p_k già fissato.

**Argomento.** Ho seguito ogni uso di g nei punti (iii)–(v).

- In (iii) servono solo due fatti: g è intera e Ann(g) = 0. L'intersezione della catena N^{>L}_{m,K}(g) è l'insieme dei Q tali che Qg è un polinomio di grado ≤ L. Allora τ^{L+1}Q ∈ Ann(g) = 0, e poiché R è un dominio Q = 0. L'ordine di annullamento di g non entra mai.
- In (iv) g serve solo a garantire che il minore Δ, visto come polinomio nelle variabili y, non sia identicamente nullo.
- Il blocco che viene davvero inserito in u è y\*. Non è il jet di g: è un punto qualunque del box fuori da Z. Quindi la compatibilità di g con p_k non è mai richiesta.

Il punto (ii) è perciò codice morto. Con g = e^{|z|²} (cioè h = 1 nel punto (i)) la prova funziona identica.

**Verifica sympy (n = 2).** Ho calcolato il primo K₀ per cui le righe |β| > L hanno rango pieno, con g di partenza e con e^{|z|²}:

| (m, L) | K₀ con g di partenza | K₀ con e^{\|z\|²} |
|---|---|---|
| (1, 0) | 3 | 3 |
| (1, 2) | 7 | 5 |
| (2, 1) | 6 | 6 |
| (2, 3) | 10 | 8 |

In tutti i casi il rango è pieno, pari a dim R_{≤m}. Il fattore |z|^{2(L+1)} peggiora soltanto K₀.

**Esito.** SURVIVES. Il punto (ii) non è falso, è solo inutile. C'è una conseguenza editoriale **MINOR**: (ii) suggerisce una dipendenza che non esiste, e un lettore può credere che la correttezza dipenda dal far coincidere g con p_k.

**Riparazione.** Eliminare (ii), oppure annotare: "non usato; si può prendere g = e^{|z|²}".

### Attacco 2 — Punto (i): Ann(g) = 0

**Argomento.** Per induzione sul grado:

∂_j(h e^{|z|²}) = (∂_j h + 2 z_j h) e^{|z|²}.

Ogni derivata alza di 1 il grado del fattore polinomiale, e il termine di testa si moltiplica per 2z_j. Il contributo ∂_j h e le parti di Q di grado inferiore danno solo termini di grado < q + deg h. Il termine di testa è Q_top(2z)·h_top, che non è nullo perché ℂ[z] è un dominio. I coefficienti complessi di Q non creano problemi.

L'indicizzazione z = (t, x) ↔ (τ, ξ) è coerente.

**Esito.** SURVIVES.

### Attacco 3 — Punto (iii): finitezza di K₀ e K₀ > L

**Argomento.**

- La catena N^{>L}_{m,K}(g) è decrescente in K e vive nello spazio di dimensione finita R_{≤m}. Ha intersezione 0, quindi si stabilizza a 0 per un K finito. La finitezza è corretta.
- Che K₀ > L non è detto esplicitamente, ma il Passo 3 lo usa ("L′_k > K_k"). Vale: per K − m ≤ L non ci sono righe con |β| > L, quindi N^{>L}_{m,K} = R_{≤m} ≠ 0. Ne segue K₀ ≥ m + L + 1 > L. Nei test sympy si ha sempre K₀ ≥ m + L + 1.
- La matrice ha entrate reali (g è reale). Rango reale pieno di colonna implica nucleo complesso nullo. Questo serve perché Q ha coefficienti in ℂ.

**Esito.** SURVIVES.

**Riparazione MINOR.** Esplicitare la riga "K₀ ≥ m + L + 1, perché per K − m ≤ L il vincolo è vuoto".

### Attacco 4 — Punto (iv): località del minore e box

**Argomento.**

- **Località.** L'elemento di posto (β, α) è j_{α+β}. Con |β| > L e |α| ≤ m, |β| ≤ K₀ − m si ha L < |β| ≤ |α + β| ≤ K₀. Quindi Δ è un polinomio a coefficienti reali nelle sole variabili y = (j_γ) con L < |γ| ≤ K₀, che sono in numero finito.
- **Non nullità.** Δ(jet di g) ≠ 0 per costruzione.
- **Box.** Lo zero-set di un polinomio non nullo è chiuso e ha interno vuoto. Il box ha lati γ!/|γ|! > 0, quindi ha interno non vuoto. Dunque B ∖ Z ≠ ∅, anzi è aperto e denso in B. Si può perfino scegliere y\* razionale, cioè il primo punto razionale di B° ∖ Z in un'enumerazione fissata, che rende la costruzione priva di scelta (vedi Attacco 7).
- **Scopo del box.** Il box serve solo a dare |c_γ| ≤ 1/|γ|! e quindi l'interezza di u. Il fattore γ!/|γ|! è proprio quello giusto, perché c_γ = j_γ/γ!.

**Esito.** SURVIVES.

### Attacco 5 — Punto (v): conclusione del lemma

**Argomento.**

- N_{m,K₀}(j′) ⊆ N^{>L}_{m,K₀}(j′), perché la prima impone più condizioni (tutti i |β| ≤ K₀ − m). Δ(y\*) ≠ 0 dà N^{>L} = 0, quindi anche N_{m,K₀}(j′) = 0.
- L'inclusione Ann(u′) ∩ R_{≤m} ⊆ N_{m,K₀}(j′) è banale: se Qu′ = 0, tutte le derivate in 0 si annullano. Non serve nemmeno l'analiticità.
- La parentesi su m′ ≤ m è superflua ma corretta.

**Esito.** SURVIVES.

### Attacco 6 — Passi 3–4: costruzione diagonale e limite intero

**Argomento.** Ho controllato in ordine:

- **Notazione.** "K_0 := 0" è subito seguito da "scegliamo K_0 tra questi". Inoltre K₀ (il K₀(m, L) del lemma) e K_0 (il primo elemento della successione) sono graficamente quasi identici. La lettura corretta è: p_0 = 0 e K_0 è un qualunque K ≥ 0 con φ_K(j_K 0) = "legge". Esiste per il Passo 0, anzi tali K sono cofiniti.
- **Monotonia stretta.** K_{k+1} ≥ L′_k + 1 > L′_k > K_k, quindi la successione K_k è strettamente crescente.
- **Gli ordini fissati non vengono toccati.** Al passo k si aggiungono monomi di ordine in (K_k, L′_k]. I passi successivi toccano solo ordini > K_{k+1} > L′_k. Gli intervalli [0, K_0], (K_k, L′_k] e (L′_k, K_{k+1}] partizionano ℕ, e ogni coefficiente viene fissato una sola volta. Ne seguono:
  - j_{K_k} u = j_{K_k} p_k, dunque φ_{K_k}(j_{K_k} u) = "legge" per infiniti indici distinti;
  - il blocco di u di ordine in (K_k, L′_k] è esattamente y\*_k.
- **Interezza.** |c_γ| ≤ 1/|γ|! per ogni γ. Poiché #{|γ| = k} = C(k+n−1, n−1) cresce in modo polinomiale, Σ_k C(k+n−1, n−1) R^k/k! < ∞ per ogni R. Quindi la serie converge assolutamente su tutto ℂ^n, e u è intera e reale.
- **Ann(u) = 0.** Il lemma con m = k dà Ann(u) ∩ R_{≤k} = 0 per ogni k. Poiché R = ∪_k R_{≤k}, si ha Ann(u) = 0. La risposta corretta è "nessuna legge", ma φ dice "legge" infinitamente spesso: φ non converge.
- **Uso del Passo 0.** È usato solo per p_0 = 0 e per i p_{k+1}, che sono polinomi. Corretto.

**Esito.** SURVIVES. C'è un difetto **MINOR** di notazione (la collisione K_0 / K₀ e "K_0 := 0" seguito da una scelta diversa).

**Riparazione.** Rinominare la costante del lemma, per esempio in K^♯(m, L), e scrivere "sia K_0 un indice con φ_{K_0}(j_{K_0} 0) = 'legge'".

### Attacco 7 — "Nessuna regola, nemmeno non calcolabile o non continua"

**Argomento.** Ho cercato ogni uso di proprietà di φ. Ce ne sono solo tre:

- la dicotomia del Passo 0 (logica classica);
- l'esistenza di K_{k+1} con φ_{K_{k+1}}(…) = "legge", garantita dalla convergenza;
- il fatto che φ_K vede soltanto j_K. È proprio questo che rende j_{K_k} u = j_{K_k} p_k sufficiente.

Non si usano misurabilità, continuità né calcolabilità. Le scelte (K_{k+1} minimo, y\* primo razionale in un'enumerazione) si possono rendere canoniche, quindi non serve nemmeno l'assioma di scelta dipendente.

Ho poi esaminato modelli di learner che potrebbero sfuggire all'enunciato.

- **Storia.** j_K contiene j_{K′} per ogni K′ < K, quindi un learner con memoria è già un φ_K. Coperto.
- **Insieme di uscite qualunque.** Per esempio "legge", "nessuna legge", "non so", oppure una legge esplicita. La prova usa soltanto che, sui polinomi, l'uscita sia "legge" in modo cofinito. Basta allora leggere "risposta ≠ 'nessuna legge'" come "legge". Coperto.
- **Uscite a più valori.** Se "corretto" significa che la risposta corretta appartiene all'insieme in uscita, il learner banale che restituisce sempre {legge, nessuna legge} vince. Ma è un modello privo di contenuto, non un controesempio. Se si richiede che l'insieme converga a {risposta corretta}, si ricade nel caso precedente. Fuori enunciato e irrilevante.
- **Learner randomizzati, φ_K(ω, j_K) con nastro casuale ω.** Formalmente non sono coperti dall'enunciato, ma la prova si estende al successo con probabilità 1, assumendo misurabili gli eventi {ω : φ_K(ω, j) = legge}. Al passo k:
  - sul polinomio q_k (cioè p_k con il blocco y\*_k aggiunto) il learner converge a "legge" quasi certamente;
  - quindi P(∃ K ∈ (L′_k, M] con uscita "legge") → 1 per M → ∞;
  - si sceglie K_{k+1} = M con probabilità ≥ 1 − ε 2^{−k−1}.

  Su u il learner vede gli stessi jet, perché ω è unico e φ dipende solo da (ω, j_K). Con probabilità ≥ 1 − ε dice dunque "legge" infinite volte su una u con Ann = 0. Per successi con probabilità p < 1 l'argomento non si concatena direttamente: è una domanda aperta, non un buco.
- **Dati diversi dal jet in 0.** Per esempio campioni in più punti o il modello DM3. Sono fuori enunciato e non vanno attribuiti a T2.

**Esito.** SURVIVES. L'enunciato è onesto. Si può aggiungere, come rafforzamento facoltativo, l'estensione ai learner randomizzati con successo quasi certo.

### Attacco 8 — Ipotesi n ≥ 2

**Argomento.** Per n = 1 la prova funziona parola per parola:

- R = ℂ[τ];
- g = z^{2(L+1)} e^{z²} ha Ann = 0;
- i polinomi sono annullati da ∂_t^{deg+1}.

Quindi l'ipotesi n ≥ 2 non è usata. Rende l'enunciato più debole di quanto la prova dia, non più forte. Ha senso solo per il corollario (vedi Attacco 10), dove per n = 1 ogni ideale non nullo è principale.

**Esito.** SURVIVES. Osservazione **MINOR**: dichiarare che T2 vale per ogni n ≥ 1, oppure motivare la restrizione.

### Attacco 9 — La "Lettura": Σ⁰₂ e non Π⁰₂, ma in quale spazio e con quale topologia?

**Argomento.** L'affermazione è ambigua su due fronti.

**(a) Spazio.** "{Ann ≠ 0} = ∪_m C_m" è un'uguaglianza tra sottoinsiemi di quale insieme?

- C_m è definito su tutto lo spazio dei jet formali 𝒥.
- Su 𝒥, ∪C_m coincide con {Ann formale ≠ 0}. La catena N_{m,K}(j) è decrescente in uno spazio di dimensione finita, quindi la sua intersezione è non nulla se e solo se tutti i termini sono non nulli. L'intersezione è {Q : Q(∂)ĵ = 0 come serie formale}.
- Sui jet di funzioni analitiche, per CONV-L1(b), questo coincide con Ann(u).

Va quindi detto che o si lavora su 𝒥 con l'annullatore formale, oppure sul sottospazio E dei jet di funzioni intere reali, con la topologia indotta.

**(b) Topologia.**

- Nella topologia prodotto standard (ℝ euclideo), ogni C_m è chiuso, perché è un'intersezione sui K di "tutti i minori r×r si annullano". Quindi ∪C_m è Σ⁰₂. Questo resta vero in ogni topologia più fine.
- Ma T2 riguarda φ_K arbitrarie. La topologia naturale per i learner è quella "fine": il prodotto di ℝ discreto, in cui i cilindri {j : j_K = a} sono aperti di base. Nella topologia standard una φ_K continua a valori in un insieme discreto di due punti è costante, perché ℝ^{J_K} è connesso. Il dizionario "decidibile nel limite ⟺ Δ⁰₂" va quindi enunciato nella topologia fine. Lì lo spazio è metrizzabile completo e a dimensione zero, ma non separabile, quindi il riferimento a Kelly 1996 (pensato per spazi numerabili e di Baire) va verificato in questo contesto.
- La parte "non Π⁰₂" non ha bisogno di Kelly. La prova di T2 è letteralmente una prova diretta. Supponiamo {Ann ≠ 0} ∩ E = ∩_i U_i con gli U_i aperti fini. Ogni polinomio sta in ogni U_i, e attorno a un polinomio c'è un cilindro di base {j_K = j_K p} ⊆ U_i. La diagonale del Passo 3, con "φ dice legge" sostituito da "il cilindro di ordine K attorno a p sta in U_k", produce una u con Ann = 0 che sta in ogni U_i. Contraddizione.
- Non Π⁰₂ nella topologia fine implica non Π⁰₂ nella topologia standard, perché la standard è più grossolana. Inoltre non Π⁰₂ relativamente a E implica non Π⁰₂ in 𝒥 (la traccia su E di un Π⁰₂ è Π⁰₂ relativo).

**(c) Verificabilità nel limite.** T1 non è nel file, quindi l'ho ricostruita io. Con m\*(K) := min{m ≤ K : N_{m,K} ≠ 0}:

- m\*(K) è ben definito, perché N_{K,K} ha una sola riga e dim R_{≤K} > 1 colonne per K ≥ 1;
- è non decrescente in K, per CONV-L1(a);
- è definitivamente costante se Ann ≠ 0;
- tende a ∞ se Ann = 0, perché per ogni m la catena raggiunge 0 (CONV-L1(c)).

Quindi la regola "legge se m\*(K) = m\*(K−1)" sbaglia infinite volte quando Ann = 0 e alla fine ha ragione quando Ann ≠ 0. La lettura è coerente con quanto si ricostruisce da CONV-L1. Non ho potuto verificare T1 così com'è scritto.

**Esito.** DAMAGED, **MINOR**. Il contenuto matematico è corretto, ma l'enunciato topologico è sotto-specificato, e il rinvio a Kelly è fragile (spazio non separabile).

**Riparazione.** Riscrivere così: "Sia E l'insieme dei jet in 0 delle funzioni intere reali, con la topologia indotta dal prodotto di ℝ discreto (cilindri j_K = a). {Ann ≠ 0} ∩ E = ∪_m (C_m ∩ E) è Σ⁰₂ (anche nella topologia euclidea) e non Π⁰₂ (anche nella topologia euclidea, a fortiori). La non-Π⁰₂-ità segue direttamente dalla costruzione dei Passi 2–4." Il riferimento a Kelly va declassato a "contesto".

### Attacco 10 — Corollario ritirato: è davvero non coperto? Si può riparare?

**Punto attaccato.** "Nessun learner identifica nel limite la classe 𝒞 := {Ann principale ≠ 0} ∪ {Ann = 0}" (per n ≥ 2).

**Diagnosi del ritiro.** Il ritiro è corretto per la prova così com'è. Per n ≥ 2, Ann(p) di un polinomio contiene tutti i monomi di grado > deg p. È un ideale di colunghezza finita, non principale (contiene τ^{d+1} e ξ_1^{d+1}, che sono coprimi). Quindi il Passo 0 può produrre un controesempio fuori da 𝒞.

**La riparazione funziona.** Per n ≥ 2 basta sostituire i polinomi con "polinomi più una coda" che stanno in 𝒞 e hanno lo stesso jet basso. Scrivo z = (t, x), con x ∈ ℝ^{n−1}.

- **Famiglia test.** Siano q un polinomio di grado ≤ M e N := M + 2. Si pone v := q + ε t^{N−1} e^{|x|²}, con ε ≠ 0.
- **Affermazione: Ann(v) = (τ^N).**
  - τ^N ∈ Ann(v): v è un polinomio in t di grado ≤ N − 1 a coefficienti interi in x.
  - Viceversa, sia Q ∉ (τ^N). Modulo τ^N, Q = Σ_{j<N} τ^j Q_j(ξ). Sia j₀ il minimo indice con Q_{j₀} ≠ 0.
  - Il coefficiente di t^{N−1−j₀} in Q(∂)v riceve contributi da a_i(x) t^i solo con i − j = N − 1 − j₀ e j ≥ j₀, cioè i ≥ N − 1.
  - Poiché q ha grado in t ≤ M < N − 1, l'unico contributo è (N−1)!/(N−1−j₀)! · ε · Q_{j₀}(∂_x) e^{|x|²}.
  - Questo è ≠ 0, perché Ann_x(e^{|x|²}) = 0 in n − 1 ≥ 1 variabili (argomento del punto (i)).
  - Verifica sympy, n = 2, N = 3, v = 1 + 2t − x + ½ t² e^{x²}: N_{4,16}(v) ha dimensione 3. Questa è proprio dim((τ³) ∩ R_{≤4}) = #{τ³, τ³ξ, τ⁴}, e il nucleo è contenuto in span{τ^a ξ^b : a ≥ 3}. Poiché N_{4,16}(v) ⊇ Ann(v) ∩ R_{≤4} ⊇ (τ³) ∩ R_{≤4}, segue l'uguaglianza fino al grado 4.
- **Jet basso invariato.** t^{N−1} e^{|x|²} ha ordine N − 1 = M + 1, quindi j_M v = j_M q.
- **Nuovo Passo 0.** Se il learner sbaglia su qualche v, abbiamo un controesempio in 𝒞, con Ann principale non nullo. Altrimenti, su ogni v il learner converge a una legge (in particolare dà un'uscita ≠ "nessuna legge" in modo cofinito).
- **Nuovo Passo 3.** Dato il polinomio p_k di grado ≤ K_k:
  1. il lemma dà il blocco y\*_k su (K_k, L′_k], e si ottiene q_k := p_k + blocco;
  2. si pone N_k := L′_k + 2, ε_k := 1/(N_k − 1)!, v_k := q_k + ε_k t^{N_k−1} e^{|x|²};
  3. si sceglie K_{k+1} ≥ L′_k + 1 con uscita ≠ "nessuna legge" su j_{K_{k+1}} v_k;
  4. si pone p_{k+1} := troncamento di v_k all'ordine K_{k+1}.

  Non c'è circolarità: ε_k dipende solo da L′_k, che è noto prima di interrogare il learner.
- **Interezza.** I coefficienti di coda hanno la forma ε_k/a! sul monomio t^{N−1} x^{2a}, con |γ| = N − 1 + 2|a|. Si ha a! ≥ |a|!/(n−1)^{|a|} e (N−1)! |a|! ≥ (N−1+|a|)!/2^{N−1+|a|} ≥ ⌊|γ|/2⌋!/2^{|γ|}. Quindi |c_γ| ≤ (2(n−1))^{|γ|}/⌊|γ|/2⌋!, che basta per l'interezza. I blocchi y\* restano sotto 1/|γ|!.
- **Conclusione.** Come nel Passo 4, Ann(u) = 0, quindi u ∈ 𝒞, ma il learner dà "legge" infinite volte. Nessun learner, anche non calcolabile, identifica 𝒞 nel limite, e anzi nemmeno ne decide la dicotomia legge/nessuna legge.
- **Caso n = 1.** Ogni ideale non nullo di ℂ[τ] è principale, quindi 𝒞 è tutto e il corollario segue direttamente da T2.

**Esito.** Il corollario ritirato è recuperabile. Il ritiro è prudente ma non necessario. Questo non danneggia CONV-T2: è un'opportunità. Raccomando di chiudere CONV-Q10 con questa prova (Passo 0′ e Passo 3′), dopo una verifica indipendente del calcolo Ann(v) = (τ^N).

### Attacco 11 — Modello di calcolo (BSS) e coerenza dell'intestazione

**Argomento.** L'intestazione colloca CONV-T2 "nel modello BSS". Ma T2 è un risultato informazionale-topologico, che vale per funzioni arbitrarie, e lo dice l'intestazione stessa ("vale perfino per funzioni arbitrarie"). Non c'è contraddizione: un risultato per funzioni arbitrarie vale a fortiori per macchine BSS e di Turing.

**Esito.** SURVIVES. Suggerimento **MINOR**: scrivere "T2 è indipendente dal modello di calcolo".

## Verdetto complessivo

**SURVIVES-WITH-FIXES.**

Nessun passo della prova di CONV-T2 è falso.

- Il lemma di evitamento è corretto.
- Il punto (ii) è superfluo: (iii)–(v) usano solo Ann(g) = 0 e il fatto che g sia intera, e il blocco inserito è y\*, non il jet di g.
- K₀ è finito e soddisfa K₀ ≥ m + L + 1.
- Il minore dipende solo dagli ordini in (L, K₀].
- Il box garantisce l'interezza.
- La diagonale non tocca gli ordini già fissati, K_k è strettamente crescente, u è intera reale con Ann(u) = 0.

La prova non usa alcuna proprietà di φ, e si estende ai learner con memoria, con uscite arbitrarie e randomizzati con successo quasi certo.

Le correzioni sono tutte MINOR:

1. Togliere o annotare il punto (ii).
2. Esplicitare K₀ > L.
3. Risolvere la collisione K_0 / K₀.
4. Specificare spazio e topologia della "Lettura", cioè la topologia fine sui jet di funzioni intere. Notare che la non-Π⁰₂-ità segue direttamente dalla costruzione, senza Kelly.
5. Segnalare che l'ipotesi n ≥ 2 non serve.

Il corollario ritirato è riparabile con la famiglia v = q + ε t^{N−1} e^{|x|²}, che ha Ann = (τ^N) principale: CONV-Q10 si può chiudere positivamente.
