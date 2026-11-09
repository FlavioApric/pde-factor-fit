# ATTACK — DEVIL-A · Gate 1 · 22/10/2026

Oggetto: G★′ e il verdetto "componente = fattore" (`research/SYNTHESIS.md` §1, §3, §5), con prove in R2, R4, R5, R8, PR-C2b e `ROUTES.md`.
Skill caricate (Regola 2, lettura del SKILL.md, nessuno script `_vendor` eseguito): `kill-argument` (eseguito solo il thread di ATTACCO: memo singolo ≤ 200 parole, poi scomposizione in obiezioni con gravità; Codex escluso, il revisore fresco sono io); `scientific-critical-thinking` (distinguere dati da interpretazione, "D" da "verificato su esempi", gravità proporzionata, rimedio per ogni obiezione).
Nessun calcolo nuovo: i controesempi sotto sono elementari e verificabili a mano.

---

## 1. Memo di rigetto (≤ 200 parole)

> G★′ dichiara di risolvere la domanda dell'utente cambiandola. Gli appunti A6, A8 e A9 chiedono componenti **per termine** e prevedono già E_int ≠ 0 (A9: f̂ = e_{n1} + e_{n2} + E_int). Dimostrare che "A8 è falso" confuta quindi una tesi che l'utente non sostiene. Il sostituto, "componente = fattore", è vuoto proprio nel caso in cui la parte (iii) funziona. Ogni evoluzione del 1° ordine in t ha simbolo P = τ − a(ξ), di grado 1 in τ e quindi irriducibile: calore, avvezione-diffusione, Airy, KdV linearizzata hanno **un solo fattore**, e la scomposizione (ii) restituisce u = u. Viceversa i fattori esistono (onda, trave, Laplace) solo dove G3 cade (PR-C2b P4). Le due metà dell'architettura non si sovrappongono su nessuna equazione della scala dei casi. Inoltre (i) è dimostrata su 𝕋 (R4-T4/T5), mentre (ii) vale su ℝ ed è falsa su 𝕋 (R2-C1): nessun dominio regge entrambe. Il "teorema unificante" è dualità di Oberst più Nullstellensatz più Prony modo per modo (Mourrain 2018); R4-T4 è un'interpolazione di Lagrange. La parte (iii) è la moltiplicatività di un moltiplicatore di Fourier. Resta una riformulazione corretta ma sostanzialmente classica, che non consegna la teoria per termine richiesta. Rigetto.

---

## 2. Obiezioni numerate

### O1 — CRITICA · Le due metà di G★′ hanno domini di non-banalità disgiunti
**Punto attaccato:** SYNTHESIS §5 (ii)+(iii) ("dentro ogni fattore, leggere i termini…"), §1.3, §1.4.
**Argomento.** Per u_t = a(∂_x)u il simbolo è P = τ − a(ξ), monico di grado 1 in τ, primitivo e quindi irriducibile in ℂ[ξ][τ] (Gauss). La decomposizione primaria ha una sola componente, perciò (ii) è banale su tutto il dominio di (iii). Lo stesso vale per i simboli non polinomiali di PR-C2b P1. Al 2° ordine in t, (ii) è non banale solo se P si fattorizza: onda (τ−cξ)(τ+cξ), trave (τ−iξ²)(τ+iξ²), Laplace (τ−iξ)(τ+iξ). Klein–Gordon τ² − ξ² − m² e il telegrafo sono irriducibili. Inoltre al 2° ordine in t G3 cade (PR-C2b P4).
**Controesempio.** Avvezione-diffusione u_t = Du_xx − cu_x: è il caso modello di "due termini", e (ii) dà una sola componente. KG: (ii) dà una sola componente e (iii) non vale (τ = ±√(ξ²+m²) non è additivo).
**Conseguenza.** Nessuna equazione della scala L0–L4 usa entrambi gli strati. L'architettura "fattori, poi termini dentro i fattori" è vuota per costruzione.
**Rimedio.** Dichiarare che la decomposizione per fattori è un pre-processing ortogonale e non il cuore di G★′, oppure cambiare strada (§3).

### O2 — CRITICA · Cambio della domanda (bait-and-switch) rispetto ad A6/A8/A9
**Punto attaccato:** SYNTHESIS §1.2–1.3, §3 riga G1/G2, §5 (ii). Raccomandazione R2 §9: "definire le componenti come fattori".
**Argomento.** A9 scrive f̂ := e_{n1} + e_{n2} + **E_int** (sottolineato due volte): l'utente si aspetta già che la somma diretta fallisca e vuole studiare il resto. "A8 è falso" (R2-T3) colpisce quindi la lettura letterale di A8, non il programma. Il piano stesso (§1.2 fatto 2(a)) dava lo split per fattori come **già noto** (Bézout / Malgrange–Ehrenpreis). Mettere i fattori al centro promuove a risultato una premessa del piano. Il glossario elenca "significato di 'componente' (termine singolo vs sotto-equazione)" come elemento **mancante**, da decidere con l'utente (piano, riga 141). Gli agenti l'hanno deciso senza l'utente.
**Conseguenza.** Il verdetto "componente = fattore" (R4 §3, RT-R2b, RT-R4a) non è un risultato: è una scelta di definizione che svuota la domanda dell'utente.
**Rimedio.** Al Gate 1 presentare la scelta come opzione esplicita, non come verdetto. Tenere "componente = termine (o sotto-equazione ∂_t − a_n)" come lettura primaria e i fattori come strumento.

### O3 — CRITICA · Nessun dominio sostiene insieme (i) e (ii) (ℝ contro 𝕋)
**Punto attaccato:** §5 (che non fissa H0), §1.1, §1.3, RT-R2a.
**Argomento.**
- (i) è dimostrata su 𝕋 o su 𝕋×I: R4-T4, R4-T5 (Fourier modo per modo) e R4-T6 (Parseval in x).
- (ii) vale su ℝ e sui convessi (R2-T1/T2) ed è **falsa** su 𝕋 con risonanze (R2-C1: u = t).
- Su ℝ l'identificazione è più debole. Le soluzioni temperate del calore su ℝ² sono polinomi, quindi Ann(u) è 0-dimensionale (R4 §2, nota a T5). La rappresentazione è solo un frame continuo con misura non unica (R2-T6). Per n ≥ 2 la sintesi spettrale in C^∞(ℝⁿ) può fallire (Gurevich 1975, citato da PR-C2b come limite). La frase "sintesi spettrale su Z(u) sempre univoca" (SYNTHESIS P4) è dimostrata solo nel caso commutativo e modo per modo.

**Conseguenza.** G★′ è un collage di due teoremi su due spazi diversi.
**Rimedio.** Fissare H0 prima di approvare G★′. Su 𝕋, (ii) richiede il criterio di non-risonanza R2-P2 come ipotesi esplicita. Su ℝ, (i) va ridimostrata in una classe precisa (PW_A, crescita esponenziale), oggi APERTO.

### O4 — MAGGIORE · Il "teorema unificante" è un corollario di risultati noti
**Punto attaccato:** SYNTHESIS §1.1 ("Il contributo nuovo possibile è un teorema unificante") e §5 (i); R4 §1 ("probabilmente nuovo ma elementare"); R8 §2.1 ("rischio che sia corollario diretto di Ehrenpreis–Palamodov").
**Argomento.** Ingredienti:
- (a) **Dualità di Oberst** (Oberst 1990, Acta Appl. Math. 20; R2-D1/T1). Per un cogeneratore iniettivo, sottomoduli e behaviour sono in corrispondenza biunivoca. Il più piccolo behaviour che contiene u è Sol(R/Ann(u)), quindi "ker P è il modello minimo di u ⟺ Ann(u) = (P)" è la dualità stessa. È anche l'MPUM di Willems e, in 2-D, Rapisarda–Antoulas 2016.
- (b) R4-T5(b) con P ridotto: (P) ⊆ Ann(u) e V(Ann u) = V(P) danno √Ann(u) = (P), quindi Ann(u) = (P). È il Nullstellensatz in una riga.
- (c) Il calcolo di Ann(u) per esponenziali-polinomi con molteplicità è Mourrain FoCM 2018 e Kunis–Peter–Römer–von der Ohe 2016.
- (d) La soglia di Bézout (T5(c)) è un'applicazione diretta.
- (e) R4-T4 ("⟺ |S| ≥ n+1") è interpolazione di Lagrange di un polinomio di grado ≤ n in n+1 nodi distinti iκ. È anche il caso 1D di Stanhope–Rubin–Swigon (x₀ ciclico) e di He–Zhao–Zhong Thm 3.2.

**Conseguenza.** SYNTHESIS §1.1 scrive "dimostrato in Fase 1 … non è in letteratura". È vero solo come enunciato non scritto altrove, non come contenuto matematico. Un revisore lo classificherebbe "folklore / corollario".
**Rimedio.** Presentare (i) come riscrittura unificata con fonti (Oberst + Mourrain + HZZ), senza rivendicare novità. La novità va cercata altrove (O1/§3).

### O5 — MAGGIORE · La parte (iii) è banale nel suo dominio, e i "termini" vi si dissolvono
**Punto attaccato:** §1.4, §5 (iii), R5-T2, PR-C2b P3.2; "il O(eⁿ) di B2 è falso".
**Argomento.**
- A coefficienti costanti e al 1° ordine in t tutti i termini commutano. Il semigruppo è il moltiplicatore e^{tΣa_n(iκ)}: "log-simbolo additivo" è la sua definizione.
- E_int^add = Σ_{|S|≥2}Π(S_n − I)u₀ è l'espansione per inclusione-esclusione di un prodotto.
- L'identificazione tramite log-simbolo è il dispositivo di prova di He–Zhao–Zhong (R8 §2.1).
- "B2 falso" è un uomo di paglia. Il valore di E_int si ottiene sempre per sottrazione in O(N) una volta noti gli u_n. Il 2^N conta i monomi dell'espansione, non il costo, e il piano lo diceva già (§1.2 fatto 2(b)).
- Il quadro scelto come "giusto" (moltiplicativo) ha E_int^mult ≡ I per termini commutanti (R5-T4): l'interazione **sparisce**. Nel quadro additivo, invece, E_int dipende dalla definizione (R5-D1 ne dà quattro), e non c'è un criterio che ne scelga una.
- "Termini = coefficienti lineari nel log-simbolo" vuol dire solo "coordinate di a(ξ) nella base dei monomi". Non aggiunge informazione rispetto a λ.

**Conseguenza.** Nel dominio di (iii) la domanda "per termine" è vuota (quadro moltiplicativo) oppure arbitraria (quadro additivo). Il caso interessante, termini non commutanti, è affidato a Wei–Norman (1963) più una congettura (R5 "Corollario-tesi: CONGETTURA").
**Rimedio.** Scegliere e giustificare **una** definizione canonica di E_int (ad esempio per minimalità o naturalità, RT-S1b/S1c) e spostare il peso sul caso non commutante o non del 1° ordine.

### O6 — MAGGIORE · Lo stato "D" poggia in parte su verifiche per esempi, schizzi e congetture
**Punto attaccato:** legenda di SYNTHESIS ("D = dimostrato … con verifica SymPy") e tabelle §2–§3.
**Evidenze.**
- R5-P5 (∂²+x): "DIMOSTRATO **sugli esponenziali**". È una verifica su una famiglia, non un teorema sull'operatore. Va esteso per densità con stime, che mancano.
- R5 "Corollario-tesi" (finita risolubile ⇒ E_int esatto; infinita ⇒ solo serie) è una **CONGETTURA**. SYNTHESIS §1.5 la enuncia come fatto, e §2 riga P1/B4 la classifica "D (congettura strutturata…)": il conflitto di etichetta è evidente.
- R5-T7: "per operatori differenziali queste serie sono **solo formali**". Proprio il caso dell'utente.
- G1 "=": R5 la dà come APERTA, R2-T3 la dichiara DIMOSTRATA. Il ledger non registra la riconciliazione. In più l'uguaglianza richiede coprimalità e iniettività, quindi è falsa su 𝕋 e per termini monomiali nella stessa variabile (R2 §4, ultimo esempio).
- R2-T7: "schizzo; V(P) singolare APERTO". R2-P2: "schizzo completo". R4-T6: solo radici semplici. R4-T5: solo P ridotto e monico in τ, su 𝕋×I.
- PR-C2b P2: "verificato sui **36 casi**". La proposizione generale è citata (Ehrenpreis–Palamodov), non dimostrata qui.
- Numerazioni di teoremi non verificate sul testo: Hörmander 7.6.13/14, Engel–Nagel II.2.7, Pazy, Wei–Norman, Miller (CIT-AUDIT: 123 classici non verificati online).
- Nessun `proof-checker` indipendente è stato eseguito. Gli 11 REPORT sono trascrizioni del coordinatore (SYNTHESIS §7).

**Conseguenza.** Le prove SymPy verificano identità su istanze scelte, non i teoremi. Lo stato "D" è credibile per i lemmi algebrici brevi (R2-T2, R2-T3, R4-T1/T4). È sovrastimato per tutto ciò che riguarda E_int non commutante e ℝ.
**Rimedio.** Introdurre lo stato "V-ex" (verificato su esempi) separato da "D". Far passare `proof-checker` su R2-T3, R4-T5 e R5-T2 prima del Gate 3.

### O7 — MAGGIORE · Il modello di calcolo di "algoritmo" e "complessità polinomiale" non è definito
**Punto attaccato:** §5 (iv), R4 §3 ("costo polinomiale").
**Argomento.** "Data una soluzione esatta u": come è data? Come espressione simbolica, come jet in un punto o come campioni? R4-T4(d) dice: grado ignoto ⟺ supp û₀ **infinito**, cioè servono infiniti modi. Ann(u) per u non D-finita / non olonoma non è calcolabile con un numero finito di operazioni. "Polinomiale" non ha né variabile né input.
**Rimedio.** Fissare la classe dei dati (ad esempio u esponenziale-polinomiale con M modi, o u olonoma data dal suo D-modulo) e misurare il costo in M, N, grado.

### O8 — MAGGIORE · La promessa sui coefficienti variabili è vuota o classica
**Punto attaccato:** §5 incipit ("e poi in una classe a dimensione finita di coefficienti variabili"), riga C3 sui coefficienti variabili.
**Argomento.**
- Con coefficienti arbitrari l'identificazione è impossibile: Scholl Prop. 10 all'ordine ≥ 2. All'ordine 1 è puntuale e banale: V = E + u''/u (R8 §4, Problema 1).
- Con una classe a dimensione finita torna il guessing D-finito (Kauers; ore_algebra), noto.
- La scomposizione (ii) diventa Loewy / LCLM (Ore 1933, van der Put–Singer), nota. (iii) diventa Wei–Norman più una congettura.

**Conseguenza.** Il "poi" di G★′ non aggiunge contenuto nuovo dimostrato.
**Rimedio.** Togliere la clausola da G★′ oppure trasformarla in un sotto-problema aperto esplicito.

### O9 — MINORE · Le "componenti per fattore" non sono identificabili oltre Ann(u)
**Punto attaccato:** §5 (ii) contro PR-C2b P8.
**Argomento.** Se u ∈ ker P₁ con L = P₁P₂ (onda con il solo f(x − ct)), u determina solo Ann(u) ∋ P₁. La "scomposizione per i fattori di P" parla dei fattori dell'annullatore di u, non di L. Va scritto.

### O10 — MINORE · Su 𝕋 il verdetto "componente = fattore" eredita E_int ≠ 0 dalle risonanze
**Punto attaccato:** §1.3, §3 riga G2.
**Argomento.** Anche dove (ii) è non banale, su 𝕋 compare un termine d'interazione nei modi risonanti (R2 §7). L'affermazione "E_int = 0 per fattori" va quindi condizionata a H0.

### O11 — MINORE · Il verdetto C3.3 (componenti = "carta di coordinate") è una preferenza estetica
**Punto attaccato:** R4 §3, SYNTHESIS riga C3.3.
**Argomento.** Che Ann(u) sia "canonico" e il dizionario "dipendente dalle coordinate" è vero, ma l'utente vuole proprio le coordinate (termini fisici: diffusione, trasporto, dispersione). Canonicità non vuol dire pertinenza.

---

## 3. La migliore alternativa a G★′

**Proposta: G★″ "prima i termini". Strada principale RT-S1a + RT-S2b [TROP-L2] (poligono di Newton / dominant balance), con RT-S2a (identità di Faddeev–Lippmann–Schwinger) come struttura esatta e RT-S1c (Möbius) come definizione dell'ordine d'interazione. La decomposizione per fattori (RT-R2b) scende a lemma di pre-processing.**

Enunciato di lavoro:
> Per P(∂_t, ∂_x) = Σ_k λ_k ∂^{α_k} (termini = monomi, come in NOTAZIONE), sia 𝒩(P) il poligono di Newton (con pesi di scala). (a) **Componenti per termine:** a ogni faccia/vertice F di 𝒩(P) corrisponde la forma iniziale P_F, che è la sotto-equazione dei soli termini dominanti in quella banda di scale. La classe naturale di A6 è ker P_F, cioè la "classe legata a un operatore" che R3/PR-C2e dicono esistere per la sotto-equazione, non per il monomio isolato. (b) **Scomposizione esatta:** con L₀ = P_F e V_i = termini restanti, vale u = u_h − Σ_i G₀V_iu, una scomposizione additiva esatta indicizzata dai termini, valida a qualsiasi ordine in t e anche per termini non commutanti. (c) **E_int:** localizzato nelle bande di transizione tra facce, con stima ‖E_int‖/‖u‖ = O(ε^γ), dove ε e γ si leggono da 𝒩(P). Ordine d'interazione = grado di Möbius (RT-S1c). (d) Nel caso commutante del 1° ordine si riduce a G★′(iii).

**Perché è migliore.**
1. **Fedeltà alla domanda.** È per termine, come in A6/A8/A9, e tratta E_int come oggetto di studio, come in A9, invece di eliminarlo ridefinendo "componente".
2. **Non banale proprio dove G★′ è vuota (O1).** Avvezione-diffusione: due facce, trasporto a k piccolo e diffusione a k grande, con transizione al numero di Péclet. È la scomposizione fisica che l'utente ha in mente. KG: τ ~ ξ per k ≫ m (onda) e τ ~ m per k ≪ m (oscillatore), con E_int concentrato a k ~ m. Il simbolo è irriducibile, eppure le componenti per termine esistono e sono significative.
3. **Non dipende da H0 (O3).** È costruita sul simbolo, quindi vale identica su ℝ e su 𝕋. Non richiede iniettività né assenza di risonanze.
4. **Non dipende dal 1° ordine in t né dalla commutatività (O5).** Il poligono di Newton esiste per ogni P(τ, ξ). L'identità di Faddeev è esatta anche per termini non commutanti; i coefficienti variabili entrano come V_i.
5. **La novità è difendibile (O4).** R8 non trova prior art per la scomposizione per termine. Dominant balance e poligoni di Newton sono classici in asintotica, ma non come teoria della scomposizione di soluzioni esatte con stima di E_int. È un enunciato falsificabile, a differenza di un corollario di Oberst.
6. **Riusa la Fase 1.** (i) di G★′ resta valida come modulo di identificazione (riscritta con fonti, O4). La decomposizione per fattori diventa il primo passo, se P si fattorizza. R5-T2 diventa il caso limite (d). PR-C2b P1 (coerenze di Gram per k) misura già la separazione tra facce.

**Rischi onesti e criterio di eliminazione.**
- Le classi per faccia sono asintotiche, non esatte: l'esattezza richiesta dal vincolo k3 regge solo tramite (b). Le componenti di Faddeev G₀V_iu, però, non stanno in classi naturali e dipendono dalla scelta di L₀ e di G₀ (ambiguità ker L₀).
- Criterio: **eliminare** se in Fase 3 la stima O(ε^γ) non si dimostra per avvezione-diffusione e KG, oppure se contano solo i vertici estremi (allora va fusa in RT-2, come già previsto in ROUTES).

**Seconda scelta.** RT-S2a (Faddeev) da sola: esatta, additiva, per termine, senza ipotesi su commutazione, ordine o dominio. Le manca però la "classe naturale" per termine, e quindi la risposta ad A6.
