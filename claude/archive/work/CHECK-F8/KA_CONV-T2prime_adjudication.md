# KA CONV-T2′ — aggiudicazione (S-CHECK-F8-CONV, 27/10/2026)

Attacco: `KA_CONV-T2prime_attack.md`, scritto da un subagente indipendente che ha ricevuto solo `KA_CONV-T2prime_input.md`, cioè l'estratto verbatim di §1.3′ con il lemma di evitamento come contesto. L'attacco ha 13 punti e propone **SURVIVES-WITH-FIXES**, senza difetti FATAL, CRITICAL o MAJOR. Lo script dell'attaccante è `sympy/conv2_ka_lemma.py` (esito "lemma checks ok").

Verifica dell'aggiudicatore. Ho rifatto a mano il lemma della famiglia test e i passi 0′, 2′, 3′ (dettaglio in `AUDIT_S8-CONV_T2prime.md` §1). Il controllo indipendente è `sympy/conv2_t2prime.py`, con esito 18/18 PASS.

## Punti dell'attacco
- **Lemma Ann(v) = (τ^N), punti 1–3: accolti, nessun difetto.** La divisione per τ^N è sempre possibile. La parte polinomiale P₀ e la parte e^{|x|²}R si separano perché e^{|x|²}·(polinomio non nullo) non è un polinomio. Il punto (i) del lemma di §1.3 si usa in n − 1 ≥ 1 variabili, e l'argomento vale anche con coefficienti complessi. Il mio script verifica Ann(v) ∩ R_{≤m} = (τ^N) ∩ R_{≤m} tramite i nuclei dei jet, per m ≤ N + 1, in n = 2 (tre casi) e in n = 3 (un caso). Verifica anche che 13 operatori fuori da (τ^N) non annullano v, tra cui un caso con j₀ ≥ 1.
- **Realtà di q ed ε, punto 4: accolto, MINOR.** Perché v sia una funzione intera reale, e quindi stia in 𝒞, servono q ∈ ℝ[t, x] ed ε ∈ ℝ ∖ {0}. La costruzione rispetta questa condizione, ma il lemma non la dichiara. Fix **T2P-1**.
- **Costruzione e limite, punti 5–8 e 10: accolti, nessun difetto.** Vale la catena H_k < L′_k < N_k − 1 ≤ H_{k+1}, e ogni ordine cade in un solo intervallo. Inoltre p_{k+1} estende p_k, j_{H_{k+1}}u = j_{H_{k+1}}v_k, il punto (iv) si applica a u e non c'è circolarità. Il mio script simula k = 0, 1, 2 con un learner fittizio e ottiene (H_k, L′_k, N_k) = (0, 2, 4), (3, 6, 8), (7, 12, 14). Su questa simulazione verifica N_{k,L′_k}(jet di u) = 0 per ogni k, che i blocchi stanno nel box e che le code non toccano i blocchi.
- **Interezza, punto 9: accolto, MINOR di notazione.** La stima è corretta, e ε_k = 1/(N_k − 1)! è necessaria (con ε_k = 1 il raggio in t sarebbe finito). Nella stima, però, k indica sia il passo sia il grado, e su ℂ^n va scritto e^{Σ|x_i|²}. Fix **T2P-2**.
- **Identificazione nel limite, punto 11: accolto, MINOR.** La riduzione da identificatore a decisore è corretta. Il testo non fissa però lo spazio delle uscite (ideali dati da generatori) né la nozione di convergenza (uscita definitivamente uguale ad Ann(u)). Fix **T2P-3**.
- **Caso n = 1, punto 12: respinto.** L'attaccante non poteva vederlo dall'estratto, ma il pacchetto enuncia e prova T2 per ogni n ≥ 1 (§1.3, fix CONV-6(d)). La frase su n = 1 è quindi corretta così com'è.
- **Notazione esterna, punto 13: accolto come MINOR facoltativo.** In §1.3(ii) si scrive "Qg₀" per Q(∂)g₀. Riguarda il testo di contesto, non T2′. Fix facoltativo **T2P-4**.

## Verdetto
**SURVIVES-WITH-FIXES**, con fix solo redazionali (T2P-1 … T2P-4). Nessun passo della prova è falso, e le ipotesi sono sufficienti una volta dichiarati reali q ed ε.
