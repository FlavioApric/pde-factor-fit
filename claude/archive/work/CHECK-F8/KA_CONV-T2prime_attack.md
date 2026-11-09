# KA CONV-T2′ — attacco indipendente (27/10/2026)

Fonte letta: solo `work/CHECK-F8/KA_CONV-T2prime_input.md`. Script di verifica: `work/CHECK-F8/sympy/conv2_ka_lemma.py` (esito: "lemma checks ok").

Lo script controlla, per n = 2 e n = 3 e per M = 0, …, 3, con q intero casuale ed ε = 1/(N−1)!, tre cose. Primo, τ^N annulla v. Secondo, v − q ha ordine N − 1 in t, quindi j_M v = j_M q. Terzo, 15 operatori Q casuali a coefficienti complessi, ridotti con grado in τ minore di N e non nulli, danno sempre Q(∂)v ≠ 0. Verifica anche la formula c_j = (N−1)!/(N−1−j)!. È un controllo a campione, non una prova, ma è coerente con il lemma.

## Punti d'attacco

1. **Lemma Ann(v) = (τ^N): divisione per τ^N.** Nessun difetto. τ^N è monico in τ, quindi la divisione euclidea in ℂ[ξ][τ] dà Q = τ^N Q′ + Σ_{j<N} τ^j Q_j(ξ), con resto unico. Il termine τ^N Q′ annulla v. L'espansione Q(∂)v = P₀ + ε e^{|x|²} Σ_j c_j t^{N−1−j} r_j(x) è corretta: Q_j(∂_x) commuta con ∂_t^j, e ∂_t^j t^{N−1} = c_j t^{N−1−j} con c_j ≠ 0 perché j ≤ N − 1. P₀ è un polinomio, perché derivate di un polinomio.

2. **Separazione tra polinomio ed e^{|x|²}·polinomio.** Nessun difetto. Se R ≠ 0 come polinomio in (t, x), esiste x₀ con R(·, x₀) non nullo, e questo si annulla solo in un numero finito di t. Quindi esiste t₀ reale con R(t₀, ·) ≠ 0. Un polinomio complesso non nullo in x ha restrizione non nulla a quasi ogni semiretta s ↦ sω, e lì |R(t₀, sω)| ≥ c > 0 per s grande. Allora |e^{s²}R(t₀, sω)| batte ogni polinomio in s, contro l'uguaglianza con −P₀(t₀, sω)/ε. Coefficienti complessi e moduli non creano problemi. R = 0 implica r_j = 0 per ogni j, perché i monomi t^{N−1−j} sono distinti e i coefficienti stanno in ℂ[x]. La nota dell'aggiudicatore è corretta: per j₀ ≥ 1 il coefficiente di t^{N−1−j₀} in P₀ non è nullo in generale, perciò serve la separazione globale. Il testo la fa.

3. **Uso del punto (i) in n − 1 variabili.** Nessun difetto. Con h = 1 e Q_j ≠ 0 si ha Q_j(∂_x)e^{|x|²} = e^{|x|²}(Q_{j,top}(2x) + grado inferiore) ≠ 0. Il punto (i) vale su ℂ: il prodotto di polinomi non nulli è non nullo, e ogni derivata alza il grado di al più 1, con parte principale 2z_j·(parte principale). Serve n − 1 ≥ 1, cioè n ≥ 2, ed è proprio l'ipotesi.

4. **Realtà di v e appartenenza a 𝒞.** MINOR (notazione). Il lemma dice "q un polinomio", senza "reale". Perché v sia una funzione intera reale servono q reale ed ε reale. Nella costruzione q_k è reale (y\* è reale, p_k è un troncamento di Taylor di una funzione reale) ed ε_k è reale, quindi l'uso è corretto. Conviene scrivere "q ∈ ℝ[t, x]" e "ε ∈ ℝ ∖ {0}".

5. **Passo 0′.** Nessun difetto. "Non converge a 'legge'" copre sia l'oscillazione sia la convergenza a "nessuna legge". In entrambi i casi u = v ∈ 𝒞 è un controesempio, perché la risposta corretta per v è "legge". Nel caso opposto, convergere a "legge" vuol dire che φ_K(j_K v) = "legge" da un certo K in poi. Quindi al passo 3 si può sempre scegliere H_{k+1} grande quanto si vuole, in particolare H_{k+1} ≥ N_k − 1.

6. **Compatibilità degli ordini.** Nessun difetto. La catena è strettamente crescente: H_k < L′_k (perché K̄(k, H_k) ≥ k + H_k + 1), L′_k < N_k − 1 = L′_k + 1 ≤ H_{k+1}. Si ha deg p_k ≤ H_k, quindi in q_k gli ordini (H_k, L′_k] contengono esattamente y\*_k/γ!·z^γ, con ∂^γ q_k(0) = y\*_{k,γ}, coerente con la convenzione j_γ = ∂^γ u(0). La coda di v_k ha ordine L′_k + 1 e non tocca il blocco. Ogni ordine sta in uno e un solo intervallo: (H_k, L′_k] (blocco) oppure (L′_k, H_{k+1}] (coda troncata di v_k). Il passo k + 1 modifica solo gli ordini > H_{k+1}. Perciò la serie formale limite è ben definita, e j_{H_{k+1}} u = j_{H_{k+1}} p_{k+1} = j_{H_{k+1}} v_k.

7. **Applicabilità del lemma di evitamento (iv) a u.** Nessun difetto. Il punto (iv) richiede soltanto che i coefficienti di u negli ordini (L, K̄] = (H_k, L′_k] siano y\*_k. Questo vale, come visto al punto 6. Le righe |β| > L della matrice M_{m,K̄} contengono solo j_{α+β} con L < |α + β| ≤ K̄, come da (iii), quindi gli altri coefficienti non contano. Inoltre K̄(k, H_k) dipende solo da g₀ = e^{|z|²} in n variabili e da (k, H_k). Il box B ha interno non vuoto e Z non ha punti interni, quindi y\*_k esiste. Ann(u) ∩ R_{≤k} = 0 per ogni k dà Ann(u) = 0.

8. **Circolarità.** Nessun difetto. L'ordine delle scelte è H_k, poi K̄, poi y\*_k, poi L′_k, N_k, ε_k, v_k, e solo alla fine si interroga φ per ottenere H_{k+1}. Né y\*_k né ε_k dipendono da H_{k+1}. Neppure la stima di interezza ne dipende: gli N_k distinti bastano.

9. **Interezza.** Nessun difetto sostanziale; un MINOR di notazione. I coefficienti di u nei blocchi y\* sono maggiorati da 1/|γ|!, quelli delle code da ε_k/β! sul monomio t^{N_k−1}x^{2β}. La serie maggiorante Σ_γ |z^γ|/|γ|! + Σ_k ε_k |t|^{N_k−1} Π_i e^{|x_i|²} converge su tutto ℂ^n: #{|γ| = d} cresce polinomialmente in d, e Σ_k |t|^{N_k−1}/(N_k − 1)! ≤ e^{|t|} perché gli N_k sono distinti. Quindi la serie di potenze converge assolutamente ovunque e u è intera, reale su ℝ^n. Senza ε_k piccoli (ad esempio con ε_k = 1) il raggio in t sarebbe al più 1, quindi la scelta di ε_k è necessaria ed è fatta bene. Il difetto di notazione: nella stima l'indice k indica sia il passo sia il grado (Σ_k #{|γ| = k}…). Su ℂ^n va scritto e^{Σ|x_i|²} al posto di e^{|x|²}.

10. **u ∈ 𝒞 e conclusione.** Nessun difetto. Ann(u) = 0, quindi u ∈ 𝒞 e la risposta corretta è "nessuna legge". φ_{H_{k+1}}(j_{H_{k+1}} u) = "legge" per infiniti K = H_{k+1} distinti, quindi φ non converge alla risposta corretta.

11. **Corollario sull'identificazione nel limite.** MINOR. La riduzione è corretta sia per la convergenza sintattica sia per quella semantica, perché la proprietà "l'ideale è non nullo" dipende solo dall'ideale e non dalla sua presentazione. Il testo però non precisa il modello di learner: lo spazio delle uscite (ideali dati da generatori?) e la dipendenza dal solo j_K u, come in T2. Va reso esplicito rimandando a T2. Non serve alcuna calcolabilità, e la prova non ne usa.

12. **Caso n = 1.** MINOR. Per n = 1 ogni ideale di ℂ[τ] è principale, quindi 𝒞 è la classe di tutte le funzioni intere reali, e l'enunciato coincide con T2 per n = 1. Questo è vero solo se T2 copre n = 1, cosa che dall'input non si può verificare. La costruzione di T2′ non funziona per n = 1 (non c'è la variabile x). La frase va formulata come rimando condizionato: "per n = 1 il caso è T2, se T2 vale per n = 1".

13. **Dipendenza da notazione esterna.** MINOR. L'enunciato usa "(φ_K) come in T2", non definito nell'estratto. Nel passo (ii) del contesto si scrive "Qg₀" per Q(∂)g₀, e nella notazione N_{m,K}(j) compare u invece di j. Sono imprecisioni del testo di contesto, non di T2′, ma andrebbero uniformate.

14. **Riga del ledger.** Nessun difetto. È coerente con l'enunciato (n ≥ 2, dipendenza dal lemma di evitamento di CONV-T2, stato "da auditare"). Si potrebbe aggiungere tra le dipendenze anche la definizione del modello di T2 (le successioni φ_K).

## Esito proposto

**SURVIVES-WITH-FIXES**, con fix solo redazionali: q ed ε reali nel lemma; rimando esplicito al modello di T2 e alla nozione di identificazione; formulazione condizionata del caso n = 1; indici e notazione nella stima di interezza. Non ho trovato difetti FATAL, CRITICAL o MAJOR. Il lemma Ann(v) = (τ^N), la costruzione e il passaggio al limite reggono. Se si considerano trascurabili i MINOR di notazione, l'esito è di fatto SURVIVES.
