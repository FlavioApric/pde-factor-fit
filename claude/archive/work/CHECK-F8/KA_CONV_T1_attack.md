# Kill-argument su CONV-L1 e CONV-T1(1–7)

Revisore avversariale indipendente, 27/10/2026. Fonte letta: soltanto `work/CHECK-F8/KA_CONV_T1_input.md`. Ho rifatto i conti da zero e li ho controllati con lo script `work/CHECK-F8/sympy/conv_ka_t1_example.py`, il cui output è in `conv_ka_t1_example.out`. Lo script calcola N_{m,K}, m\*(K) e O_K direttamente dai jet, per n = 2 con N = 0..3 e per n = 3 con l'esempio originale e con quello riparato.

## Attacchi

1. **CONV-L1(a)–(b): monotonia e intersezione.**
   - **Argomento.** Il punto (a) è immediato. Per (b), se Q appartiene all'intersezione su K ≥ m, allora ogni derivata ∂^β(Q(∂)u)(p₀) è nulla. La funzione Q(∂)u è reale-analitica e Ω è connesso, quindi Q(∂)u ≡ 0. Il viceversa è banale. Ho cercato un controesempio con Ω non connesso o con u solo C^∞: entrambi violano (H-an), quindi non valgono come controesempi.
   - **Esito.** SURVIVES.

2. **CONV-L1(c): finitezza di ν_m e soglia K\*(m).**
   - **Argomento.** La filtrazione F_k vive nello spazio W_m, che ha dimensione finita. La catena è decrescente e ha intersezione {0}, quindi si stabilizza a {0}. Ne segue ν_m < ∞, e il massimo è raggiunto perché gli ordini sono interi limitati.
   - Per Q ∉ Ann(u), Q ∈ N_{m,K} vale se e solo se ord(Q(∂)u) ≥ K − m + 1. Inoltre l'inclusione Ann ∩ R_{≤m} ⊆ N_{m,K} vale sempre. L'equivalenza N_{m,K} = Ann ∩ R_{≤m} ⟺ K ≥ m + ν_m è quindi corretta, nel dominio K ≥ m.
   - Osservazione utile: ν_m è non decrescente in m, perché il massimo si prende su un insieme più grande. Dunque K\*(m) è strettamente crescente in m e K\* = max_{m≤d} K\*(m) = K\*(d). Questo è coerente con T1(6), dove K\* = K\*(1).
   - **Caso limite u = 0.** Si ha ν_m = −1 e K\*(m) = m − 1 < m. La convenzione scritta copre il caso.
   - **Esito.** SURVIVES.

3. **T1(1), casi limite d = 0 e K\* < d.**
   - **Argomento.** La prova di m\*(K) = d richiede anche K ≥ d, perché N_{m,K} è definito solo per m ≤ K. Per u ≠ 0 si ha ν_d ≥ 0, quindi K\* = d + ν_d ≥ d e il punto è automatico. Per u = 0 si ha Ann = R = (1), d = 0 e K\* = −1. Per ogni K ≥ 0 vale N_{0,K} = ℂ e O_K = 1 = g_0, quindi l'enunciato è corretto. Resta solo il valore K = −1, che è privo di senso.
   - Ho verificato anche che tutti gli elementi non nulli di Ann ∩ R_{≤d} hanno grado esattamente d e che gcd e normalizzazione sono ben definiti, perché lo spazio è non nullo.
   - **Esito.** DAMAGED, MINOR (solo cosmetico).
   - **Riparazione.** Scrivere "per K ≥ max(K\*, 0)", oppure escludere u = 0 come caso banale.

4. **T1(2): Ann principale.**
   - **Argomento.** Un multiplo di P con grado ≤ deg P è uno scalare per P, quindi Ann ∩ R_{≤d} = ℂP. Il caso P costante coincide con u = 0 ed è già coperto.
   - **Esito.** SURVIVES.

5. **T1(3) e T1(4).**
   - **Argomento.** Per T1(3), dato m, per K ≥ K\*(m) = max_{m′≤m} K\*(m′) tutti gli N_{m′,K} con m′ ≤ m sono nulli. Insieme alla finitezza di m\*(K) per K ≥ 1, data da T1(5), segue m\*(K) → ∞. Per T1(4), il gcd di un insieme di generatori di un ideale in un UFD coincide con il gcd dell'ideale.
   - Unico caso degenere di T1(4): Ann = 0 con B qualsiasi, che è generato dall'insieme vuoto. Allora O^B_K = (0) = Ann, ma "gcd(N_{B,K}) = G_u" richiede la convenzione gcd(0) = 0.
   - **Esito.** SURVIVES. La convenzione gcd(∅) = 0 va esplicitata, ma è un punto MINOR di sola notazione.

6. **T1(5): conteggio e normalizzazione monica (punto critico).**
   - **Argomento, passo per passo.**
     - **m\*(K) è finito.** Per K ≥ 1, N_{K,K} è il nucleo di una sola forma lineare su R_{≤K}, che ha dimensione binom(K+n, n) ≥ n + 1 ≥ 3. Quindi N_{K,K} ≠ 0. Per K = 0 l'affermazione sarebbe falsa quando u(p₀) ≠ 0, e infatti l'enunciato la esclude.
     - **m\*(K) è non decrescente.** Segue da CONV-L1(a).
     - **A m\* fissato.** L'insieme dei K con m\*(K) = m è un intervallo, perché m\* è monotona. Su quell'intervallo i sottospazi N_{m,K} sono decrescenti e non nulli. Quindi O_K divide O_{K+1}: il grado è non decrescente, e a parità di grado i due gcd sono associati.
     - **Normalizzazione.** Il coefficiente direttore rispetto all'ordine monomiale fissato non è nullo. Dividendo per esso si ottiene un unico rappresentante, quindi polinomi associati diventano uguali.
   - Dunque O_K è funzione della coppia (m\*(K), deg O_K), che è lessicograficamente non decrescente. Nel caso 1 si ha m\*(K) ≤ d per ogni K ≥ 1, e deg O_K ≤ m\*(K) perché O_K divide un elemento non nullo di grado ≤ m\*. Le coppie possibili sono Σ_{m=0}^{d}(m+1) = (d+1)(d+2)/2.
   - Lo stesso polinomio può corrispondere a coppie diverse, per esempio O = 1 per (0,0), (1,0), (2,0). Questo rende il conteggio ancora più prudente, non lo invalida: il numero di valori distinti è al più il numero di coppie, e il numero di cambi di valore è al più il numero di cambi di coppia.
   - Il gcd di jet reali è reale a meno di uno scalare, perché è invariante per coniugazione. Quindi il gcd normalizzato è reale ed è calcolabile nel modello BSS su ℝ.
   - **Uniformità in u.** Il limite dipende solo da d, come dichiarato. Fuori dal caso 1 (Ann = 0) il limite non vale, e l'enunciato non lo afferma.
   - **Esito.** SURVIVES.

7. **T1(6): esempio u = 1 + x^{N+2}e^{x²}, verifica di Ann(u) = (τ).**
   - **Argomento.** Scrivendo Q = τQ₁ + q(ξ), si ha Q(∂)u = q(∂_x)f. Se q ≠ 0, f risolve un'ODE lineare a coefficienti costanti, quindi è un esponenziale-polinomio con crescita al più e^{A|x|}. Ma f ha crescita x^{N+2}e^{x²}, contraddizione.
   - Il caso q costante non nullo dà f = 0, che è falso. Se Ω è un connesso qualsiasi che contiene 0, l'analiticità estende la conclusione. Quindi Ann(u) = (τ) e d = 1.
   - **Esito.** SURVIVES.

8. **T1(6): calcolo di ν₁ e di K\*.**
   - **Argomento.** ν₀ = 0 perché u(0) = 1. Per m = 1 si ha Q(∂)u = a·f + c·f′.
     - Se a ≠ 0: a·f(0) + c·f′(0) = a, perché f′(0) = 0 già per N = 0. L'ordine è 0.
     - Se a = 0 e c ≠ 0: f′ = (N+2)x^{N+1}e^{x²} + 2x^{N+3}e^{x²}, quindi l'ordine è N + 1.
   - Dunque ν₁ = N + 1 e K\* = K\*(1) = N + 2. Inoltre N + 2 è proprio il primo indice con uscita corretta: per K = N + 1 si ha N_{1,K} = span(τ, ξ), quindi O_K = 1.
   - Lo script conferma, per N = 0, 1, 2, 3: O_K = 1 per 1 ≤ K ≤ N + 1 e O_K = τ da K = N + 2.
   - **Difetto.** L'enunciato dice "per K ≤ N + 1". Per K = 0 però N_{0,0} = 0, perché u(0) = 1, quindi m\*(0) = ∞ e O_0 non è definito. Lo script restituisce `None` per K = 0. La prova scrive correttamente 1 ≤ K.
   - **Esito.** DAMAGED, MINOR.
   - **Riparazione.** Scrivere "per 1 ≤ K ≤ N + 1".

9. **Nota di dimensione: T1(6) "vale per ogni n ≥ 2 con la stessa prova" (dipendenza da n).**
   - **Argomento.** Per n ≥ 3, la stessa u = 1 + x₁^{N+2}e^{x₁²} non dipende da x₂, …, x_{n−1}. Quindi Ann(u) = (τ, ξ₂, …, ξ_{n−1}), che non è principale, e g_1 = gcd(τ, ξ₂, …) = 1. L'uscita è O_K = 1 per ogni K: la regola converge subito al valore limite g_1 = 1, e l'esempio non mostra più un'uscita sbagliata per un tempo lungo.
   - Lo script, nel caso "n=3 ORIGINAL", dà O_K = 1 per tutti i K. La frase "Ann(u) = (τ)" è falsa per n ≥ 3, e la nota sulla dimensione afferma più di quanto la prova dia. Resta vero soltanto che K\* = N + 2 non è limitato in funzione di d, ma questa è la parte meno informativa.
   - **Esito.** DAMAGED, MAJOR, perché la nota sulla dimensione è falsa come scritta. Il nucleo n = 2 resta intatto.
   - **Riparazione (verificata).** Usare u = 1 + x₁^{N+2}·exp(|x|²) con |x|² = x₁² + … + x_{n−1}².
     - **Ann(u) = (τ).** Per q ≠ 0 di grado m con parte omogenea di grado massimo q_m, si ha q(∂)(x₁^{N+2}e^{|x|²}) = e^{|x|²}·(x₁^{N+2}q_m(2x) + termini di grado inferiore). Questo è e^{|x|²} per un polinomio non nullo, quindi non può essere uguale alla costante −q(0).
     - **Ordini.** ∂₁ dà ordine N + 1, mentre ∂_j con j ≥ 2 dà 2x_j·x₁^{N+2}e^{|x|²}, di ordine N + 3. Quindi ν₁ = N + 3 e K\* = N + 4. Per 1 ≤ K ≤ N + 3, τ e ξ₂ stanno in N_{1,K}, quindi O_K = 1 ≠ τ.
     - Lo script conferma per n = 3 e N = 0, 1 (righe "REPAIRED"): O_K diventa τ esattamente da K = N + 4. Per n = 2 la formula si riduce all'esempio originale.

10. **T1(7): uso di C3-P1[M2], quantificazione e classe delle funzioni.**
    - **Argomento.** La prova è logicamente corretta: c dipende solo da j_K, quindi u e u′ ricevono lo stesso certificato e la stessa uscita, e da qui la contraddizione. Le ipotesi di C3-P1[M2] sono soddisfatte: Ω connesso in ℝ², P non costante, K ≥ 0, P(∂)u = 0. La v intera ristretta a Ω è analitica, e il suo annullatore su Ω coincide con quello su ℝ².
    - **Caso K = 0.** O_0 può non essere definito. Però il ragionamento usa solo la u con c = 1, per la quale O_K(u) è definito, e u′ ha lo stesso jet. Nessun buco.
    - **Primo punto debole: la classe delle funzioni.** Il modello BSS dichiarato lavora su "numeri reali esatti", e (H-an) può intendersi come u a valori reali. La v di C3-P1 è un esponenziale-polinomio che può essere complesso, cioè fuori dalla classe. Se la classe è quella delle funzioni reali, nella prova c'è un buco.
    - **Secondo punto: il lemma esterno è superfluo.** Basta prendere u′ := T_K u, il polinomio di Taylor di ordine K in p₀. È reale se u lo è, è intero e ha lo stesso K-jet. Ann(T_K u) contiene tutti i monomi di grado K + 1, quindi ha codimensione finita. Invece R_n/(P), con P non costante e n ≥ 2, ha dimensione infinita. Dunque Ann(u′) ≠ (P).
    - Questa prova di una riga chiude il buco reale/complesso. Toglie la dipendenza da C3-P1[M2] e da C3-T3. Rende T1(7) valido per ogni n ≥ 2 e per ogni Ω connesso, quindi la restrizione a n = 2 della nota sulla dimensione non serve.
    - In alternativa, se si vuole tenere C3-P1: si prende u′ = Re v. Il modulo R·u′ è contenuto in R·v + R·v̄, che ha dimensione finita, e si conclude con lo stesso argomento di codimensione.
    - Lo stesso argomento mostra anche quanto sia debole il contenuto di T1(7): nessun annullatore principale non banale è certificabile da un jet finito, semplicemente perché i polinomi hanno gli stessi jet. Per n = 1 (solo τ) la tesi sarebbe falsa, ma è esclusa.
    - **Esito.** DAMAGED, MINOR per l'ambiguità reale/complesso. Il miglioramento è consigliato.
    - **Riparazione.** Sostituire u′ con T_K u (o con Re v) ed enunciare T1(7) per n ≥ 2.

11. **Nota "Ann non principale": esempio G·(τ, ξ²).**
    - **Argomento.** Gli elementi di grado minimo di G·(τ, ξ²) sono ℂ·Gτ, quindi g_d = Gτ. L'ideale è realizzabile come annullatore: con G = ξ, u = e^{t²} + x² ha Ann(u) = (ξτ, ξ³) = ξ·(τ, ξ²). L'ho verificato a mano, riducendo Q modulo l'ideale ad a(τ) + bξ + cξ² e usando il fatto che e^{t²} non è un esponenziale-polinomio. L'esempio della nota è dunque legittimo.
    - **Esito.** SURVIVES.

12. **Modello di calcolo e normalizzazione in BSS.**
    - **Argomento.** I ranghi e i nuclei delle matrici M_{m,K} sono calcolabili in modo esatto nel modello BSS. Il gcd multivariato di una base reale è un calcolo algebrico finito, e il risultato normalizzato è reale. Il fatto che la "regola" richieda solo il jet, e non d o deg P, è rispettato.
    - **Esito.** SURVIVES.

## Verdetto complessivo

**SURVIVES-WITH-FIXES.** CONV-L1 e CONV-T1(1)–(5) reggono. In particolare il conteggio (d+1)(d+2)/2 di T1(5) e la normalizzazione monica sono corretti, e l'esempio di T1(6) è corretto per n = 2, con K\* = N + 2 e ν₁ = N + 1 verificati simbolicamente. T1(7) è corretto.

Correzioni richieste:
- **(MAJOR)** La nota sulla dimensione è falsa per T1(6) quando n ≥ 3: la stessa u ha annullatore non principale e uscita costante 1. Va sostituita con u = 1 + x₁^{N+2}e^{|x|²}, che ha K\* = N + 4.
- **(MINOR)** In T1(6) scrivere 1 ≤ K ≤ N + 1.
- **(MINOR)** In T1(1) scrivere K ≥ max(K\*, 0) e trattare il caso u = 0; in T1(4) esplicitare la convenzione gcd(∅) = 0.
- **(MINOR)** In T1(7) chiarire se le funzioni sono reali o complesse. È consigliato sostituire C3-P1[M2] con l'argomento del polinomio di Taylor, che vale per ogni n ≥ 2.
