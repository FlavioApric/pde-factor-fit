# KA CONV-T2 — aggiudicazione (S-CHECK-F8-CONV, 27/10/2026)

Attacco: `KA_CONV_T2_attack.md`, scritto da un subagente indipendente che ha ricevuto solo `KA_CONV_T2_input.md`. L'attacco contiene 11 punti; l'esito proposto è **SURVIVES-WITH-FIXES**. Script dell'attaccante: `sympy/conv_ka_t2_check.py`.

Verifica dell'aggiudicatore. Ho rifatto a mano i passi 0–4 (si veda `AUDIT_S8-CONV.md` §3). Il controllo indipendente è in `sympy/conv_misc.py`, sezione T2. Con g = |z|^{2(L+1)}e^{|z|²} in n = 2, la sottomatrice M^{>L}_{m,K₀} ha rango pieno per (m, L) = (0,0), (1,0), (1,1), (2,1), con K₀ = 2, 3, 5, 6. In tutti i casi le coordinate del jet che compaiono hanno ordine in (L, K₀]. Lo stesso K₀(1,1) esiste anche con g₀ = e^{|z|²}, cioè senza il punto (ii).

## Passo cardine (ii) e affermazione "nessuna regola, nemmeno non calcolabile"
- **(ii): accolto, il punto è superfluo (MINOR, editoriale).** I passi (iii)–(v) usano solo che g è intera e che Ann(g) = 0. Le righe |β| > L contengono in ogni caso solo coordinate di ordine > L, qualunque sia g. Nel jet di u si inserisce y\*, non il jet di g. Dunque l'annullamento di g in 0 all'ordine 2(L+1) non serve, e la prova funziona identica con g₀ = e^{|z|²}. Lo confermano sia il mio script sia quello dell'attaccante. Il punto (ii) non è falso: suggerisce soltanto una dipendenza che non esiste. Fix **CONV-6**: togliere (ii), oppure dichiararlo inessenziale.
- **"Nessuna regola": accolto, l'enunciato è corretto.** La prova non usa alcuna proprietà delle φ_K: né calcolabilità, né continuità, né misurabilità, né l'assioma di scelta. Il passo 0 è una dicotomia sulle φ e i passi 3–4 interrogano le φ solo su jet di polinomi. Sono coperti anche i learner con memoria, perché j_K contiene j_{K′} per ogni K′ < K, e quelli con insiemi di uscite qualunque, tramite la mappa uscita ↦ {legge, nessuna legge}. Restano fuori, e non sono rivendicati, tre casi: i learner randomizzati con successo di probabilità < 1, i dati diversi dal jet in un punto (fuori dal modello DM2) e i jet rumorosi (quelli sono trattati in T3–T5). Per i learner randomizzati che riescono quasi certamente l'estensione proposta dall'attaccante è plausibile, ma non l'ho verificata. Va registrata come osservazione, non come parte del claim.

## Altri punti
- **(iii): K₀ ≥ m + L + 1 va scritto esplicitamente (MINOR).** Senza questa condizione non ci sono righe con |β| > L. Fix CONV-6.
- **(iv)–(v) e passi 3–4: accolti, nessun difetto matematico.** Ho controllato che |c_γ| ≤ 1/|γ|! dia l'interezza, che K_k sia strettamente crescente e che gli ordini già fissati non vengano più toccati. Difetto di notazione MINOR: K_0 della successione collide con K₀ del lemma, e "K_0 := 0" è seguito da una scelta diversa. Fix CONV-6.
- **n ≥ 2: accolto (MINOR).** L'ipotesi non è usata: T2 vale per ogni n ≥ 1. Va dichiarato, oppure motivata la restrizione. Fix CONV-6.
- **"Lettura" (Σ⁰₂ e non Π⁰₂): accolto come DAMAGED-MINOR.** Lo spazio e la topologia non sono specificati. Il contenuto matematico (la regola di verifica nel limite, e la non decidibilità nel limite, che è T2 stesso) è corretto. L'equivalenza con "non Π⁰₂" richiede invece di fissare lo spazio (jet delle funzioni intere) e la topologia rilevante per l'apprendimento (cilindri j_K = a). Il rinvio a Kelly 1996 non è necessario, perché la non-Π⁰₂ segue dalla costruzione stessa, ed è fragile. Fix **CONV-7**: o specificare lo spazio e la topologia, o ridurre la "Lettura" a "verificabile ma non decidibile nel limite" senza la gerarchia di Borel.
- **Modello di calcolo: accolto (MINOR).** Scrivere "T2 è indipendente dal modello di calcolo" invece di collocarlo nel modello BSS. Fix CONV-6.

## Corollario ritirato (CONV-Q10)
Il ritiro è corretto rispetto alla prova scritta. Per n ≥ 2, Ann(p) di un polinomio ha codimensione finita e non è principale, quindi il passo 0 può dare un controesempio fuori dalla classe 𝒞 := {Ann principale ≠ 0} ∪ {Ann = 0}.

**La riparazione dell'attaccante funziona.** L'ho verificata in modo indipendente, con una prova più pulita del passo che l'attaccante segnala come da controllare.
- *Famiglia.* Per un polinomio q di grado ≤ M, si pone N := M + 2 e v := q + ε t^{N−1}e^{|x|²}, con ε ≠ 0 e n ≥ 2.
- *Affermazione: Ann(v) = (τ^N).* τ^N annulla v. Sia Q = τ^N Q′ + Σ_{j<N} τ^j Q_j(ξ) ∈ Ann(v). Allora Q(∂)v = [polinomio] + ε e^{|x|²} Σ_{j<N} c_j t^{N−1−j} r_j(x), con c_j = (N−1)!/(N−1−j)! ≠ 0 e Q_j(∂_x)e^{|x|²} = r_j e^{|x|²}. Qui r_j ≠ 0 se Q_j ≠ 0, per il punto (i) del lemma in n − 1 ≥ 1 variabili. Se e^{|x|²}R(t, x) è un polinomio, allora R = 0. Le potenze di t sono distinte, quindi ogni r_j = 0, cioè ogni Q_j = 0, e Q ∈ (τ^N).
- *Nota sull'argomento dell'attaccante.* L'attaccante confronta il coefficiente di t^{N−1−j₀}. Quel confronto è completo solo per j₀ = 0, perché per j₀ ≥ 1 la parte polinomiale può contribuire alla stessa potenza di t. La separazione "polinomio contro e^{|x|²}·polinomio" chiude il caso generale.
- *Interezza.* Con ε_k := 1/(N_k − 1)!, le code sono maggiorate termine a termine da Σ_k |t|^{N_k−1}/(N_k−1)!·e^{|x|²} ≤ e^{|t| + |x|²}. I blocchi y\* restano sotto 1/|γ|!. Dunque u è intera.
- *Assenza di circolarità.* ε_k dipende solo da L′_k, che è noto prima di interrogare il learner sul jet di v_k.

Esito: **CONV-Q10 si chiude in positivo come PROVA SCRITTA (dall'audit)**. Enunciato: per n ≥ 2, nessuna successione di funzioni dei jet identifica nel limite, e nemmeno decide nel limite la dicotomia legge/nessuna legge, sulla classe 𝒞. Per n = 1 il corollario coincide con T2. La prova va scritta nel pacchetto da S8-CONV (passo 0′ e passo 3′) e deve passare il proprio ciclo. Non la promuovo qui a DIMOSTRATO: è una riparazione proposta in audit, non un testo auditato. Fix **CONV-8**.

## Verdetto
**SURVIVES-WITH-FIXES.** Nessun passo della prova di CONV-T2 è falso. Il passo cardine (ii) è superfluo, non sbagliato. L'affermazione "nessuna regola, nemmeno non calcolabile" è giustificata. Le correzioni sono tutte MINOR: CONV-6 (editoriali), CONV-7 (la "Lettura"), CONV-8 (CONV-Q10 riparabile). L'esito interno PASS-WITH-NOTES è confermato.
