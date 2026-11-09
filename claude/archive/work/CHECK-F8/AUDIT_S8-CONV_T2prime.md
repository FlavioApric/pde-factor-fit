# Mini-audit di CONV-T2′ e verifica a campione del recepimento (S-CHECK-F8-CONV, 27/10/2026)

**Oggetto.**
- `work/S8-CONV/PROOF_PACKAGE.md`: §1.3′ [CONV-T2′] alle righe 102–124 e §R (recepimento) alle righe 331–356.
- `work/S8-CONV/LEDGER_ROWS.md`, riga 10.
- Nella cartella non esiste un file RECEPIMENTO separato: il recepimento è la sezione §R del PROOF_PACKAGE.

**Materiali prodotti.**
- `KA_CONV-T2prime_input.md`, `KA_CONV-T2prime_attack.md` (scritto da un subagente indipendente) e `KA_CONV-T2prime_adjudication.md`.
- `sympy/conv2_t2prime.py` con il relativo `.out` (18/18 PASS).
- `sympy/conv2_ka_lemma.py`, lo script dell'attaccante.

## Verdetto: **PASS-con-fix** (4 fix MINOR, tutti redazionali)

CONV-T2′ è corretto. Propongo lo stato **DIMOSTRATO** dopo l'applicazione di T2P-1 … T2P-3; T2P-4 è facoltativo. La promozione spetta al coordinatore.

## 1. Prova riga per riga

**Enunciato.** Il claim è completo per n ≥ 2.
- 𝒞 e la dicotomia sono ben definiti, e la risposta corretta su 𝒞 è determinata.
- Il caso n = 1 coincide con T2, perché ogni ideale di ℂ[τ] è principale e T2 è enunciato per n ≥ 1.
- La riduzione "identificatore ⇒ decisore" (φ_K := "legge" se e solo se l'uscita è non nulla) è corretta: se le uscite convergono ad Ann(u), φ converge alla risposta giusta.

**Lemma della famiglia test.**
- τ^N v = 0, perché deg_t q ≤ M < N e ∂_t^N t^{N−1} = 0.
- La divisione Q = τ^N Q′ + Σ_{j<N} τ^j Q_j(ξ) esiste sempre.
- Q(∂)v = P₀ + εe^{|x|²}Σ c_j t^{N−1−j} r_j(x), con c_j ≠ 0. Il punto (i) di §1.3, applicato con h = 1 in n − 1 variabili, dà r_j ≠ 0 se Q_j ≠ 0.
- Separazione. Se R ≠ 0, esiste t₀ reale con R(t₀, ·) ≠ 0. Su una retta generica per l'origine, R(t₀, s w) è un polinomio non nullo in s, e e^{s²|w|²} per quel polinomio non è un polinomio. Quindi R = 0. Poiché le potenze di t sono distinte, ogni r_j = 0, quindi ogni Q_j = 0. L'argomento vale anche con coefficienti complessi.
- j_M v = j_M q: la coda ha ordine N − 1 = M + 1.
- La nota di riga 109 è corretta: confrontare un solo coefficiente basta solo per j₀ = 0.
- Unica lacuna: q ed ε vanno dichiarati reali. Altrimenti v non è una funzione intera reale e non sta in 𝒞 (fix T2P-1).

**Passo 0′.** La dicotomia è corretta. Se φ fallisce su un v, allora v ∈ 𝒞 con risposta "legge", e il controesempio è v. Altrimenti φ → "legge" su tutta la famiglia. L'insieme su cui si quantifica è {q + εt^{N−1}e^{|x|²} : N ≥ deg q + 2, ε ≠ 0}, ed è esattamente quello usato al passo 2′ con M = L′_k.

**Passo 2′.**
1. p_k ha grado ≤ H_k, quindi q_k ha sugli ordini (H_k, L′_k] proprio i coefficienti del blocco y\*_k, nel box.
2. N_k = L′_k + 2 e ε_k dipendono solo da L′_k: non c'è circolarità.
3. H_{k+1} ≥ N_k − 1 = L′_k + 1 > H_k esiste per il passo 0′. Ne segue che H_k è strettamente crescente, e "infinite volte" significa su infiniti indici distinti.
4. p_{k+1} = T_{H_{k+1}}v_k estende p_k fino all'ordine H_k.
- Che H_0 = 0 sia scelto senza condizioni su φ è corretto: φ si interroga solo agli indici H_{k+1}.

**Passo 3′.**
- Ogni ordine cade in un solo intervallo, (H_k, L′_k] (blocco) oppure (L′_k, H_{k+1}] (troncamento della coda k), quindi la serie formale è ben definita. Lo stesso vale per la descrizione dei termini ε_k t^{N_k−1}x^{2β}/β!.
- *Interezza.* I coefficienti dei blocchi sono ≤ 1/|γ|!, quelli delle code ≤ ε_k/β!. Poiché gli N_k sono distinti, Σ_k |t|^{N_k−1}/(N_k − 1)! ≤ e^{|t|}. La serie di potenze converge quindi assolutamente su ℂ^n, e u è intera e reale. Due difetti di notazione: nella stima k indica sia il passo sia il grado, e su ℂ^n va scritto e^{Σ|x_i|²} (fix T2P-2).
- j_{H_{k+1}}u = j_{H_{k+1}}v_k, quindi φ dice "legge" infinite volte.
- Ann(u) ∩ R_{≤k} ⊆ N_{k,L′_k}(j u) = 0 per il punto (iv), perché le coordinate del jet di u sugli ordini (H_k, L′_k] sono y\*_k. Dunque Ann(u) = 0, u ∈ 𝒞, e la risposta corretta è "nessuna legge". ∎

**Ipotesi.** Le ipotesi sono sufficienti con T2P-1. n ≥ 2 serve davvero: il lemma richiede la variabile x.

## 2. Verifica SymPy indipendente (`sympy/conv2_t2prime.py`, 18/18 PASS)
- **(A)** In n = 2, con deg q = 0, 1, 2 (N = 2, 3, 4):
  - τ^N v = 0;
  - dim N_{m,K}(v) = dim (τ^N) ∩ R_{≤m} per m ≤ N + 1, con K = N + 12;
  - ogni elemento del nucleo sta in (τ^N);
  - j_M v = j_M q.
- **(B)** In n = 3, con q = 1 + t − x₁x₂ e N = 4: stessa uguaglianza dei nuclei per m ≤ 5, con K = 16.
  - Al primo tentativo, con K = 12, il nucleo per m = 5 aveva dimensione 8 invece di 4.
  - Era una soglia K finita troppo bassa, non un difetto: con K = 16 i nuclei coincidono.
- **(C)** Dodici operatori casuali fuori da (τ^N), più uno con j₀ ≥ 1, non annullano v.
- **(D)** Simulazione dei passi 2′ e 3′ per k = 0, 1, 2, con un learner fittizio che sceglie H_{k+1} = N_k − 1.
  - Si ottiene (H_k, L′_k, N_k, H_{k+1}) = (0, 2, 4, 3), (3, 6, 8, 7), (7, 12, 14, 13).
  - p_{k+1} estende p_k, le code non toccano i blocchi e i blocchi stanno nel box.
  - N_{k,L′_k}(jet di u) = 0 per ogni k.

## 3. Kill-argument
L'esito è **SURVIVES-WITH-FIXES** (si veda `KA_CONV-T2prime_adjudication.md`).
- L'attaccante non ha trovato difetti FATAL, CRITICAL o MAJOR.
- Sono accolti i MINOR su: realtà di q ed ε; modello e nozione di identificazione; notazione della stima di interezza; "Qg₀" in §1.3(ii).
- È respinto il punto sul caso n = 1: T2 copre n ≥ 1 nel pacchetto.

## 4. Verifica a campione del recepimento dei 13 fix
Ho controllato tutti e 13 i fix sul testo del pacchetto, non solo sulla tabella di §R.

| fix | dove l'ho trovato | esito |
|---|---|---|
| CONV-1 | §4.3 (r. 215–217), §0.3 (r. 34), §Z (r. 324), riga D2 del ledger: "solo C^∞(Ω)", Malgrange exp. 246 Thm 3.2(2) p. 83, D′ escluso (CONV-Q17) | recepito |
| CONV-2 | T1(1) K ≥ max(K\*, 0); T1(4) gcd({0}) := 0 (r. 64); T1(6) 1 ≤ K ≤ N+1 | recepito |
| CONV-3 | r. 66 e 74: u = 1 + x₁^{N+2}e^{|x|²}, Ann = (τ), K\* ≥ N + 2, con prova | recepito |
| CONV-4 | r. 75: u′ := T_K u, per ogni n ≥ 2 | recepito |
| CONV-5 | r. 256: 16\|c\|/(3Lm); la vecchia costante 8\|c\|/(3Lm) non compare più | recepito |
| CONV-6 | r. 81–99: punto (ii) tolto (nota r. 89), g₀ = e^{\|z\|²}, K̄ ≥ m+L+1, H_k, n ≥ 1, "indipendente dal modello di calcolo" (anche r. 14) | recepito |
| CONV-7 | r. 100: "Lettura" dichiarata commento, rinvio a Kelly tolto | recepito |
| CONV-8 | §1.3′ (questo audit) | recepito |
| CONV-9 | r. 288–289: secondo controesempio a₁₂ = 0, a₂₁ = 1; righe 28–29 del ledger | recepito, con un residuo (sotto) |
| CONV-10 | r. 130: Ω limitato lipschitziano, con la nota sulla fessura | recepito |
| CONV-11 | r. 155: u′ − u ∈ C^∞(Ω̄) | recepito |
| CONV-12 | r. 142: Stein cap. VI §3.1 Thm 5, da verificare in CIT-AUDIT-8 | recepito |
| CONV-13 | r. 158: N_d := dim R_{≤d} | recepito |

**Residuo (MINOR, editoriale).** In §Z, riga 327, la voce FALSO per CONV-MZ3 cita solo la prima lettura ("memoria nulla ⟺ [𝒫, A] = 0"). Il testo di §8 e il ledger coprono invece entrambe le letture. Fix **T2P-5**: allineare §Z.

## 5. Elenco dei fix (tutti MINOR)
- **T2P-1.** Nel lemma di §1.3′, scrivere "q ∈ ℝ[t, x]" ed "ε ∈ ℝ ∖ {0}", perché v deve essere intera reale per stare in 𝒞.
- **T2P-2.** Nella stima di interezza:
  - rinominare l'indice del grado (ad esempio d al posto di k);
  - su ℂ^n scrivere e^{Σ|x_i|²};
  - facoltativo: dire che blocchi e code occupano ordini disgiunti, per cui la maggiorazione è termine a termine.
- **T2P-3.** Nel "In particolare" dell'enunciato, precisare il modello dell'identificatore:
  - uscita al passo K = un ideale di R_n (per esempio dato da generatori), funzione arbitraria di j_K u come in T2;
  - successo = uscita definitivamente uguale ad Ann(u).
  - Facoltativo: esplicitare H_{k+1} > H_k, in modo che gli indici "legge" siano infiniti e distinti.
- **T2P-4** (facoltativo). In §1.3(ii), scrivere Q(∂)g₀ al posto di "Qg₀".
- **T2P-5.** In §Z, riga 327, la voce FALSO di CONV-MZ3 deve citare entrambe le letture, come §8 e il ledger.

**Riga del ledger** (LEDGER_ROWS r. 10). È coerente con l'enunciato, l'ipotesi n ≥ 2 e la dipendenza dal lemma di evitamento (che include il punto (i)). Dopo T2P-1 … T2P-3 propongo lo stato DIMOSTRATO, con la verifica `conv2_t2prime` e il revisore S-CHECK-F8-CONV.
