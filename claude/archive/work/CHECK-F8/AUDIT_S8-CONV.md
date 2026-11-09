# AUDIT S8-CONV — S-CHECK-F8-CONV · 27/10/2026

Revisore: S-CHECK-F8-CONV, proof-checker indipendente. Oggetto: `work/S8-CONV/PROOF_PACKAGE.md` (§0–§9, §K), con `CHECK_REQUEST.md`, `LEDGER_ROWS.md` e i quattro script in `work/S8-CONV/sympy/`. Ho letto solo enunciati, ipotesi e prove; non ho letto il contesto della sessione autrice (`PLAN.md`, `open_questions.md`).

Contesto letto:
- `NOTAZIONE.md` v5: DM2, DM3, (H-ID);
- `claims/LEDGER.md`: righe C3-P1[M2], C3-L3, C3-T3;
- `work/C3/PROOF_PACKAGE.md` §5: enunciato di C3-P1[M2];
- `research/CIT-AUDIT/AUDIT-6.md`: righe 6, 19 e 25;
- `ROUTES.md`: righe RT-S2d e RT-R2a, per controllare la fedeltà delle letture dei due FALSO.

Skill caricate leggendo i SKILL.md, senza eseguire script `_vendor`: `skills-local/claim-lifecycle`, `_vendor/.../proof-checker` (tassonomia a due assi FATAL/CRITICAL/MAJOR/MINOR), `_vendor/.../kill-argument` (attacco, poi aggiudicazione), `scientific-critical-thinking` (giudizio finale sullo stato).

Kill-argument: due subagenti nuovi, ciascuno con il solo file `KA_CONV_<claim>_input.md`, che contiene un estratto verbatim. I file `_input`, `_attack` e `_adjudication` di T1 e T2 sono in questa cartella.

Script SymPy e numerica indipendenti, eseguiti con `python -I`:
- `sympy/conv_t8_strang.py` → `.out`: **15/15 PASS**;
- `sympy/conv_misc.py` → `.out`: **30/30 PASS**.

Script degli attaccanti: `sympy/conv_ka_t1_example.py`, `sympy/conv_ka_t2_check.py`.

## 0. Verdetti

| ID | verdetto | fix | stato proposto |
|---|---|---|---|
| CONV-L1 | **OK** | — | **DIMOSTRATO** |
| CONV-T1(1–7) | **OK con fix MINOR** (KA: SURVIVES-WITH-FIXES) | CONV-2, CONV-3, CONV-4 | **DIMOSTRATO** (T1(6) per n = 2 come scritto; per n ≥ 3 con l'esempio di CONV-3) |
| CONV-T2 | **OK con fix MINOR** (KA: SURVIVES-WITH-FIXES) | CONV-6, CONV-7 | **DIMOSTRATO** per ogni n ≥ 1; la "Lettura" Σ⁰₂/Π⁰₂ va riscritta o declassata a commento (CONV-7) |
| corollario ritirato (CONV-Q10) | ritiro **corretto** rispetto alla prova scritta; **riparabile** | CONV-8 | APERTO → **PROVA SCRITTA (dall'audit)**: da scrivere nel pacchetto e da auditare |
| CONV-T3 | **OK con fix MINOR** | CONV-10 | **DIMOSTRATO** (esempi con Ω regolare) |
| CONV-T4(a–c) | **OK con fix MINOR** | CONV-12 | **DIMOSTRATO**; il numero del teorema di Stein resta per CIT |
| CONV-T5(1–3) | **OK con fix MINOR** | CONV-11, CONV-13 | **DIMOSTRATO** |
| CONV-T6(1–4) | **OK** | — | **DIMOSTRATO** |
| CONV-P6(a–c) | **OK** | — | **DIMOSTRATO** |
| CONV-P7 | **OK** | — | **DIMOSTRATO** |
| CONV-P8 | **OK** | — | **DIMOSTRATO** |
| CONV-D1(a–c) | **OK** | — | **DIMOSTRATO** |
| CONV-D2 | **fonte verificata solo in parte** | **CONV-1 (MAJOR)** | **CON-FONTE (verificata) per C^∞(Ω)**: Malgrange, exp. 246, Thm 3.2(2), p. 83. **Per D′(Ω) la fonte citata non lo copre**: da verificare (Palamodov 1970 / Hörmander) |
| CONV-B1, B2, B3 | **OK** | — | **DIMOSTRATO** |
| CONV-T8(a–d) | **OK con fix MINOR** | CONV-5 | **DIMOSTRATO** (L²); **V-ex confermato** per l'ordine 1 in L^∞ (pendenze 1,002 / 1,004 / 0,998) |
| CONV-R1(a–c) | **OK** | — | **DIMOSTRATO** |
| CONV-R1-F (RT-R2a senza clausola) | **FALSO confermato** | — | **FALSO** (f = ξ, g = τ) |
| CONV-MZ1, MZ2, MZ3 | **OK** | — | **DIMOSTRATO** |
| CONV-MZ3-F (RT-S2d) | **FALSO confermato**, ma il controesempio copre una sola lettura | CONV-9 | **FALSO** (con il controesempio a12 = 0, a21 = 1, che copre entrambe le letture) |
| CONV-T7 | **OK** (proposizione elementare; il contratto è una specifica) | — | proposizione **DIMOSTRATO**; contratto: specifica, nessuno stato |

Nessun FATAL e nessun CRITICAL. C'è un solo MAJOR, CONV-1: è di citazione e riguarda solo la parte D′ di CONV-D2. Nessun nuovo FALSO matematico nelle prove. I due FALSO dichiarati sono confermati.

## 1. Fix numerati

**CONV-1 (MAJOR · REFERENCE_MISMATCH · LOCAL: CONV-D2).**
- *Verifica.* Ho letto la fonte primaria: Malgrange, *Systèmes différentiels à coefficients constants*, Sém. Bourbaki 15e année 1962/63, exp. 246 (texte remanié mai 1963), vol. 8 (1964), pp. 79–89, scansione Numdam SB_1962-1964__8__79_0.
  - p. 83, **Théorème 3.2**: «Pour tout ouvert convexe Ω ⊂ ℝ^n, (1) ℰ′(Ω) est un A-module totalement plat, (2) ℰ(Ω) est un A-module injectif», con il viceversa: ogni aperto connesso che soddisfa (1) o (2) è convesso.
  - Stessa pagina, Théorème 3.1(2): 𝒟′(Γ) è iniettivo per Γ compatto convesso.
  - Stessa pagina, l'autore aggiunge: «Il me paraît probable que 𝒟′(Ω) est aussi un A-module injectif, mais la méthode suivie ne donne pas ce résultat.»
  - Convenzione: A = ℂ[X_1, …, X_n] agisce con X_j ↦ −i∂/∂x_j. È un automorfismo d'anello rispetto a ξ_j ↦ ∂_j, quindi l'iniettività si trasferisce.
- *Problema.* CONV-D2 afferma l'iniettività per C^∞(Ω) **e** D′(Ω), citando in blocco Malgrange exp. 246, Palamodov 1970 e Hörmander ICASV §7.6. La parte C^∞ è esattamente il Thm 3.2(2). La parte D′ **non** è in exp. 246, che la dichiara anzi non ottenuta. Palamodov e Hörmander non li ho verificati.
- *Riparazione.*
  - (i) Scrivere «C^∞(Ω) iniettivo per Ω convesso: Malgrange, exp. 246, Thm 3.2(2), p. 83 (verificato)».
  - (ii) Per D′(Ω), o togliere il caso o citarlo come «da verificare» (Palamodov 1970, cap. VII; Hörmander ICASV, numero da verificare), da affidare a CIT-AUDIT-8.
  - Il passo omologico è corretto e l'ho rifatto: la successione 0 → R/(Q_1Q_2) → R/(Q_1) ⊕ R/(Q_2) → R/(Q_1, Q_2) → 0 è esatta perché (Q_1) ∩ (Q_2) = (Q_1Q_2) in un UFD; `conv_misc` controlla un esempio con Gröbner. Hom(·, 𝒜) è esatto per 𝒜 iniettivo. Il passo serve solo Ext¹(R/(Q_1, Q_2), 𝒜) = 0.
- *Stato.* CON-FONTE (verificata) per 𝒜 = C^∞(Ω); per 𝒜 = D′(Ω), CON-FONTE da verificare.

**CONV-2 (MINOR · casi degeneri di T1).**
- In T1(6) l'uscita O_0 non è definita (m\*(0) = ∞ se u(p₀) ≠ 0): scrivere «per 1 ≤ K ≤ N+1».
- In T1(1) per u = 0 (d = 0, K\*(0) = −1): scrivere K ≥ max(K\*, 0).
- In T1(4): fissare gcd(∅) := 0 (o escludere Ann = 0).
- Nota facoltativa: ν_m è non decrescente in m, quindi K\* = K\*(d).

**CONV-3 (MINOR · OVERSTATED nella nota "Dimensione" di §1.2).** La frase «L1 e T1(1)–(6) valgono per ogni n ≥ 2 con la stessa prova» è falsa per T1(6). Per n ≥ 3, u = 1 + x_1^{N+2}e^{x_1²} è annullata anche da ξ_2, …, quindi Ann(u) non è principale e l'uscita resta 1 per ogni K (KA T1, punto 4).
- *Riparazione* (dell'attaccante, verificata nell'argomento): u = 1 + x_1^{N+2}e^{|x|²}, con Ann(u) = (τ) per ogni n ≥ 2. Per n = 3 l'attaccante calcola K\* = N + 4; non ho rifatto la costante.
- La conclusione «K\* non è limitato da funzioni di d» resta vera per ogni n.

**CONV-4 (MINOR, consigliato · T1(7)).** La prova via C3-P1[M2] è corretta per u a valori complessi; l'enunciato non chiede valori reali. Si può dare una prova più corta e più generale. Si prende u′ := T_K u, il polinomio di Taylor. Ha lo stesso K-jet, e Ann(u′) ⊇ (τ^{K+1}, ξ_j^{K+1}) ha codimensione finita. Quindi Ann(u′) ≠ (P) per P non costante, perché V(P) è infinito se n ≥ 2. Così T1(7) vale per ogni n ≥ 2, con funzioni reali, senza dipendere da C3-P1 e senza la restrizione Ω ⊂ ℝ². Va anche detto che il contenuto di T1(7) è elementare.

**CONV-5 (MINOR · costante in T8(d)).** Il maggiorante «|V_{m1}| ≤ 8|c|/(3Lm) per m ≥ 2» è falso. Per m = 2, |V_{21}| = 8|c|/(3L), il doppio del valore dichiarato; per m = 4, 1,067 contro 0,667 (`conv_t8_strang`). Il bound corretto è 16|c|/(3Lm), da m² − 1 ≥ ¾m². Cambia solo la costante C; l'ordine Θ(h^{5/4}) non cambia.

**CONV-6 (MINOR · editoriali su CONV-T2).**
- (a) Il punto (ii) del passo 2 è superfluo. Con g₀ = e^{|z|²} la prova funziona identica, come confermano `conv_misc` e il KA. Va tolto o dichiarato inessenziale.
- (b) Scrivere K₀ ≥ m + L + 1 in (iii).
- (c) Rinominare K_0 della successione, che collide con K₀ del lemma, e togliere «K_0 := 0» seguito da una scelta diversa.
- (d) T2 vale per ogni n ≥ 1, perché n ≥ 2 non è usato.
- (e) Scrivere «indipendente dal modello di calcolo» invece di «modello BSS».

**CONV-7 (MINOR · DAMAGED · la "Lettura" di T2).** «{Ann ≠ 0} è Σ⁰₂ e non Π⁰₂» non specifica lo spazio (jet delle funzioni intere) né la topologia. Il rinvio a Kelly 1996, «capitolo da verificare», non è necessario. Riparazione: o fissare lo spazio dei jet delle funzioni intere con la topologia dei cilindri {j_K = a}, osservando che la non-Π⁰₂ segue dalla costruzione dei passi 2–4; oppure ridurre la frase a «verificabile ma non decidibile nel limite», senza la gerarchia di Borel. La regola di verifica nel limite «dì legge se m\*(K) = m\*(K−1)» è corretta.

**CONV-8 (MINOR, positivo · CONV-Q10).** Il ritiro del corollario è giustificato rispetto alla prova scritta: per n ≥ 2 il passo 0 può dare un polinomio, il cui Ann ha codimensione finita e non è principale. Il corollario è però **riparabile** (KA T2, attacco 10; verifica dell'aggiudicatore in `KA_CONV_T2_adjudication.md`).
- Si sostituiscono i polinomi con v = q + ε t^{N−1}e^{|x|²}, con N = deg q + 2. Vale Ann(v) = (τ^N), che è principale. La prova separa la parte polinomiale dalla parte e^{|x|²}·polinomio e usa Ann_x(e^{|x|²}) = 0.
- Con ε_k = 1/(N_k−1)! il limite è intero, maggiorato da e^{|t|+|x|²}.
- Non c'è circolarità.

Esito: CONV-Q10 diventa PROVA SCRITTA (dall'audit). S8-CONV deve scrivere il passo 0′ e il passo 3′ nel pacchetto; il testo andrà poi auditato.

**CONV-9 (MINOR · supporto del FALSO di MZ3).** ROUTES scrive il criterio di RT-S2d come «E_int = 0 ⟺ [𝒫, L] = 0». Il controesempio del pacchetto (a12 = 1, a21 = 0) confuta la lettura «memoria nulla». Non confuta la lettura «memoria **e** rumore nulli», perché lì il rumore e^{ta22}v̂(0) è ≠ 0 e il commutatore anche (`conv_misc`). Riparazione: aggiungere il controesempio a12 = 0, a21 = 1. Lì la componente û è esattamente chiusa (memoria e rumore nulli), ma [𝒫, A] = [[0, 0], [−1, 0]] ≠ 0. Così il FALSO vale per entrambe le letture. La forma corretta è già nel pacchetto: memoria nulla ⟺ a12·a21 = 0; memoria e rumore nulli ⟺ a12 = 0.

**CONV-10 (MINOR · esempi di T3).** «H^m(Ω) e C^k(Ω̄) con Ω limitato»: la densità dei polinomi (ipotesi (β)) può fallire per Ω irregolare. Su un dominio con una fessura, una funzione H¹ con salto attraverso la fessura non si approssima con funzioni lisce fino al bordo. Riparazione: «Ω limitato lipschitziano» (o con la proprietà del segmento). Il teorema astratto non cambia.

**CONV-11 (MINOR · T5).**
- (a) In T5(3), «u′ ∈ C^∞(Ω̄)» richiede u ∈ C^∞(Ω̄). Scrivere «u′ − u ∈ C^∞(Ω̄)», oppure aggiungere l'ipotesi.
- (b) La regola R_δ del ramo L² usa δ_m = C_{Ω,m,s}(…), quindi richiede una costante di interpolazione esplicita, o almeno un suo maggiorante noto. Va dichiarato tra le ipotesi della regola.

**CONV-12 (MINOR / CIT · T4(b)).** L'interpolazione via Fourier e la disuguaglianza di Hölder con esponenti (n_0+s)/s e (n_0+s)/n_0 sono corrette e le ho rifatte. Serve E_S limitato anche su L² (k = 0), e l'operatore di Stein lo è. A memoria, il numero è Stein 1970, cap. VI §3.1, Thm 5 (operatore di estensione universale per domini lipschitziani, W^{k,p} per ogni k): **da verificare in CIT-AUDIT-8**.

**CONV-13 (MINOR · notazione in T5(3)).** «r» indica sia dim(Ann ∩ R_{≤d}) sia dim R_{≤d}, che è il grado del polinomio in ε. Rinominare.

## 2. CONV-L1 e CONV-T1: controllo passo per passo
Rifatti a mano.
- **L1(a)–(c).** In (c) F_k è un sottospazio di W_m. La catena F_k è stazionaria con intersezione {0}, quindi ν_m < ∞. Per Q ∉ Ann vale Q ∈ N_{m,K} ⟺ ord(Qu) ≥ K − m + 1.
- **T1(1)–(4).** Corretti. In T1(2), Ann ∩ R_{≤d} = ℂP perché ogni elemento non nullo di (P) ha grado ≥ deg P.
- **T1(5)** (domanda 1 della CHECK_REQUEST). O_K è funzione della coppia (m\*, deg O_K): a m\* fisso, N_{m,K+1} ⊆ N_{m,K} dà gcd(N_{m,K}) | gcd(N_{m,K+1}). A grado uguale i due gcd sono associati e coincidono dopo la normalizzazione monica rispetto a qualunque ordine monomiale fissato. La coppia è non decrescente nell'ordine lessicografico, quindi visita ciascun valore su un intervallo. Le coppie possibili sono Σ_{m=0}^d (m+1) = (d+1)(d+2)/2. Corretto; `conv_misc` lo controlla su un esempio.
- **T1(6)** (domanda 2). Con a ≠ 0, ord(af + cf′) = 0 perché f(0) = 1 e f′(0) = 0: nessuna combinazione con a ≠ 0 dà ordine più alto. ν₁ = N + 1. L'argomento di crescita è corretto: un esponenziale-polinomio è O((1+|x|)^M e^{A|x|}), e f cresce come e^{x²}. `conv_misc` lo conferma per N = 1, 2, 3. Per n ≥ 3 si veda CONV-3.
- **T1(7)** (domanda 3). La citazione di C3-P1[M2] corrisponde al LEDGER e a `work/C3` §5. L'ipotesi è Ω ⊂ ℝ² aperto connesso, senza convessità. La tesi è che esiste v ∈ E_P con lo stesso K-jet e Ann(v) ⊋ (P), dunque v è intera e quindi analitica. La quantificazione «per ogni K e ogni u con Ann(u) = (P)» coincide. Si veda anche CONV-4.
- **Kill-argument.** SURVIVES-WITH-FIXES: `KA_CONV_T1_adjudication.md`.

## 3. CONV-T2: controllo passo per passo (domande 4–5)
- **Passo 0.** Corretto: per un polinomio la risposta giusta è «legge».
- **Passo 2(i).** La parte omogenea di grado massimo di Q(∂)(h e^{|z|²}) è Q_top(2z)·h_top. Un polinomio complesso non nullo non si annulla identicamente su ℝ^n.
- **Passo 2(ii).** Vero ma superfluo (CONV-6a).
- **Passo 2(iii).** Corretto: se Qg ha serie senza termini di grado > L, Qg è un polinomio perché g è intera. Allora τ^{L+1}Q ∈ Ann(g) = 0.
- **Passo 2(iv).** Corretto: le righe |β| > L contengono j_{α+β} con L < |α+β| ≤ K₀. Il box |j_γ| ≤ γ!/|γ|! ha interno non vuoto, e lo zero di un polinomio non nullo è chiuso e senza punti interni.
- **Passo 2(v).** N ⊆ N^{>L}.
- **Passi 3–4.** I coefficienti c_γ = j_γ/γ! soddisfano |c_γ| ≤ 1/|γ|! e Σ_k #{|γ| = k}‖z‖^k/k! < ∞: u è intera reale. I passi successivi modificano solo ordini > K_{k′} ≥ K_k, quindi j_{K_k}u = j_{K_k}p_k e i blocchi y\*_k restano in u. Si ha Ann(u) ∩ R_{≤k} = 0 per ogni k.
- **«Nessuna regola, nemmeno non calcolabile».** Corretto: le φ_K non sono mai usate se non tramite i loro valori.
- **Corollario ritirato.** Si veda CONV-8.
- **Kill-argument.** SURVIVES-WITH-FIXES: `KA_CONV_T2_adjudication.md`.

## 4. Rumore (T3, T4, T5), domande 6–7
- **T3.** Il determinante D(ε) ha grado r e coefficiente direttivo det(⟨Q_α g₀, ψ_i⟩) ≠ 0, quindi si annulla in al più r valori di ε. L'unione su m è numerabile e u + εg₀ → u. Unico rilievo: CONV-10.
- **T4.**
  - (a) Catena di disuguaglianze corretta. L'esempio A = diag(0, ρ), E = [[0,0],[δ,0]] dà seno δ/√(ρ²+δ²): ottimalità d'ordine.
  - (b) L'esponente vale per n_0, s interi, con costante C_{Ω,n_0,s} dall'estensione e dalle equivalenze di norme su ℝ^D (domanda 6).
  - (c) Weyl.
- **T5.**
  - (1) Il ramo H e il ramo L² sono corretti; nel ramo L² vale ‖e‖_{H^{m+s}} ≤ ‖e‖_{H^{d+s}} per m ≤ d.
  - (2) Corretto.
  - (3) Ann(p) ∩ R_{≤d} = 0 via la parte omogenea di grado minimo: i monomi ∂^αp sono distinti e non nulli perché α_i ≤ |α| ≤ d (`conv_misc`, d = 1, 2, 3). Q₀τ^{d+1} ∈ Ann(u + εp) (`conv_misc` sul calore con d = 2). d(u′) ∈ (d, 2d+1], quindi δ₀(u′) ≤ ½s_d(u′) ≤ ½|ε|‖Q₀(∂)p‖. La conseguenza su Ψ è corretta (domanda 7). Rilievi: CONV-11, CONV-13.

## 5. Località (T6, P6, P7), domande 8–9
- **T6(1).** Derivazione sotto il segno; la trasformata di una funzione L¹ a supporto compatto è intera in x, e la trasformata di Fourier è iniettiva.
- **T6(2)** (domanda 8). I_J è primo perché è il nucleo verso un dominio. Non è massimale perché iκ non è costante. In ℂ[τ, ξ] (dimensione 2) un primo non nullo e non massimale ha altezza 1; in un UFD i primi di altezza 1 sono principali. L'intersezione di primi principali distinti è generata dal prodotto.
- **T6(3)–(4).** Corretti.
- **P6(a).** Gli esponenti iα + j sono distinti (gli indici sono scambiati rispetto al testo, senza effetto).
- **P6(b)** (domanda 9). La catena è corretta. a è algebrica su ℂ(κ), quindi e^{σa} = −κ²/a è algebrica su ℂ(κ). a è non costante, quindi trascendente su ℂ; il grado di trascendenza di ℂ(κ, a) è 1, quindi κ è algebrica su ℂ(a) (scambio) e quindi lo è anche e^{σa}. H(y, e^{σy}) è intera e nulla su a(J), che contiene un intervallo reale, quindi è identicamente nulla. Per C3-L3(b), H = 0. L'identità di Lambert è controllata numericamente in `conv_misc`.
- **P6(c).** Corretto.
- **P7.** Corretto (e^t sin x non risolve l'equazione con ritardo: 1 ≠ −e^{−σ}).

## 6. Dimensione (P8, D1, D2), domanda 14
- **P8.** Corretto per ogni R_n-modulo.
- **D1(a).** Per il teorema dell'ideale principale di Krull, i primi minimali su (Q_1, Q_2) hanno altezza ≤ 2, quindi le componenti hanno dimensione ≥ n − 2 ≥ 1 se n ≥ 3. Allora V è infinito, R/(Q_1, Q_2) ha dimensione infinita (Nullstellensatz) e ci sono infiniti esponenziali indipendenti in ker Q_1 ∩ ker Q_2.
- **D1(b)–(c).** Corretti (`conv_misc` per (c)).
- **D2.** Si veda CONV-1.

## 7. Bordo (B1–B3), domanda «conteggio D + 1»
- **B1(b).** dim R·u = 2 = dim R/(τ+κ₀, ξ²+μ²): uguaglianza.
- **B2.** ∂^γ compare come ∂^α (una volta) e come ∂_j∂^α (al più D volte): totale ≤ D + 1. `conv_misc` lo controlla per (D, n_0) = (2,2), (3,2), (2,3).
- **B3.** ∂_t è tangente a Γ = {x_1 = c}, quindi la traccia di ∂_t w è ∂_t(w|_Γ) = 0. Corretto.

## 8. CONV-T8 (Strang Θ(h^{5/4}) in L²), domande 10–11
Controllo indipendente in `sympy/conv_t8_strang.py`, 15/15 PASS.
- **Forma chiusa (a).** Le identità b/(a−b) = 1/(e^x−1) e (a+b)/(a−b) = coth(x/2) sono verificate simbolicamente. V_{21} è ricalcolato dall'integrale. Il confronto con la somma diretta dei prodotti modali dà errore 2·10^{−36}.
- **Pendenze L²** per h = 4^{−3}…4^{−7}:
  - Strang 1,2542 → 1,2513 → 1,2504 → 1,2502 (→ 5/4); ‖G^{Str}‖/h^{5/4} si stabilizza a 8,367·10^{−5};
  - Lie 0,921 → 0,966 → 0,984 → 0,992 (→ 1).
- **Minorante (c)** (domanda 10). Le stime sono rifatte a mano, tutte corrette:
  - il conteggio dei pari in W_h dà ≥ 1/(4√(κh)) per κh ≤ 1/36 (verificato anche numericamente su cinque valori);
  - e^{λ_1T} − e^{λ_mT} ≥ ½e^{λ_1T}, perché κ(m²−1)T ≥ n_h ≥ 1 > ln 2;
  - la monotonia di |φ_S| segue dalla funzione di Langevin (verificata su una griglia), con |φ_S| ≤ min(x/12, ½);
  - φ\* = 0,08198.

  Il minorante è rispettato numericamente, con margine di circa 25×.
- **Maggiorante (c).** Corretto.
- **(d).** Ordine Θ(h^{5/4}) confermato: pendenze 1,169 → 1,230 → 1,245 → 1,249. La costante intermedia è sbagliata (CONV-5).
- **Significato** (domanda 11). G_h è il coefficiente di ε con il passo di trasporto I + εhV: ho rifatto il calcolo del primo ordine del prodotto. Per il passo di inflow la derivata in ε = 0 coincide, perché gli stati intermedi S_0(kh)u_0 stanno in H¹_0 e lo strato di bordo contribuisce O(ε^{3/2}) in L². La lettura è corretta, e il pacchetto dichiara giustamente che non serve all'enunciato.
- **[V-ex] L^∞** vicino a x = 0: pendenze 1,002, 1,004, 0,998. L'ordine 1 è confermato **solo numericamente**: resta V-ex.
- **Confronto con Einkemmer–Ostermann.** È correttamente presentato come analogia di meccanismo. AUDIT-6 dice «Dirichlet non omogeneo» e il pacchetto lo recepisce. La norma di Dang–Einkemmer–Ostermann 2025 resta non verificata, come dichiarato.

## 9. CONV-R1 e il FALSO di RT-R2a, domanda 12
- Bézout in ℂ(ξ)[τ] dà Af + Bg = r(ξ) ≠ 0, e i k risonanti stanno in Z = {r(ik) = 0}, che è finito.
- La costruzione per k ∉ Z, con |r(ik)| ≥ c per |k| grande, conserva il decadimento rapido dei coefficienti.
- La mappa u ↦ ([û_k])_{k risonante} è ben definita e suriettiva (somme finite). Il suo nucleo è ker f + ker g, per la costruzione applicata ai modi non risonanti e per i fatti sulle ODE. La codimensione è Σ deg gcd(f_k, g_k).
- La clausola sulle rette contenute è necessaria: se f_k ≡ 0, ker f_k = C^∞(I) e la scomposizione del modo è banale.
- **FALSO confermato.** RT-R2a in ROUTES dichiara il criterio «esatto: nessuna risonanza V(f) ∩ V(g) ∩ (ℂ × iℤ)». Con f = ξ, g = τ si ha V(f) ∩ V(g) = {(0, 0)} ⊂ ℂ × iℤ, eppure ker(τξ) = {A(t) + B(x)} = ker ξ + ker τ (`conv_misc`). Il controesempio confuta la direzione «scomposizione ⇒ nessuna risonanza».
- Esempio di R2 (`conv_misc`): Z = {0}, deg gcd = 1, testimone u = t.

## 10. CONV-MZ, domanda 13
- **MZ1.** adj(D)·D = det(D)·I.
- **MZ2.** Duhamel; l'equazione eliminata det(τ − A) è verificata simbolicamente.
- **MZ3.** ℂ[ξ] è un dominio e e^{ta22} ≠ 0. 𝒫A − A𝒫 = [[0, a12], [−a21, 0]].
- **FALSO** confermato per entrambe le letture, con il complemento CONV-9.

## 11. CONV-T7
La proposizione di composizione è una somma telescopica, corretta sotto l'ipotesi di Lipschitz sugli insiemi dichiarati. Il contratto (A)/(B)/(C)/(Lim) è una specifica e non ha stato. Le etichette (B) citano Casas 2007 per operatori limitati su spazi di Hilbert, coerentemente con AUDIT-6 riga 19; la costante π resta non letta, come dichiarato.

## 12. Giudizio finale (scientific-critical-thinking)
Il pacchetto distingue con cura gli stati: PROVA SCRITTA, CON-FONTE, V-ex, FALSO. Le prove reggono un controllo riga per riga e due kill-argument indipendenti. I difetti trovati sono:
- una citazione sovradichiarata: D′ in CONV-D2, che la fonte primaria dichiara non dimostrato con quel metodo;
- un esempio fuori portata in dimensione n ≥ 3 (T1(6) nella nota);
- una costante sbagliata (T8(d));
- un controesempio che copre una sola lettura del criterio RT-S2d;
- difetti editoriali in T2.

Nessuno cambia un enunciato principale. Le novità sono basse per L1/T1 (dichiarato) e reali per T8 (5/4 in L², forma chiusa esplicita) e R1 (criterio esatto con la clausola sulle rette). Un'osservazione utile per il coordinatore: CONV-Q10 appare chiudibile in positivo (CONV-8).

## 13. Righe proposte per il LEDGER (al coordinatore)
| ID | stato | proof-checker | kill-argument |
|---|---|---|---|
| CONV-L1 | DIMOSTRATO | S-CHECK-F8-CONV 27/10 PASS | (con T1) SURVIVES-WITH-FIXES |
| CONV-T1(1–7) | DIMOSTRATO (T1(6): n = 2; n ≥ 3 con l'esempio di CONV-3) | PASS-con-fix (CONV-2, 3, 4) | sì, SURVIVES-WITH-FIXES |
| CONV-T2 | DIMOSTRATO (ogni n ≥ 1; nessuna ipotesi sulle φ_K) | PASS-con-fix (CONV-6, 7) | sì, SURVIVES-WITH-FIXES |
| CONV-Q10 | PROVA SCRITTA (dall'audit; da scrivere nel pacchetto e auditare) | — | — |
| CONV-T3 | DIMOSTRATO | PASS-con-fix (CONV-10) | no |
| CONV-T4(a–c) | DIMOSTRATO (numero di Stein: CIT) | PASS-con-fix (CONV-12) | no |
| CONV-T5(1–3) | DIMOSTRATO | PASS-con-fix (CONV-11, 13) | no |
| CONV-T6(1–4), CONV-P6(a–c), CONV-P7 | DIMOSTRATO | PASS | no |
| CONV-P8, CONV-D1(a–c) | DIMOSTRATO | PASS | no |
| CONV-D2 | CON-FONTE (verificata) per C^∞(Ω): Malgrange exp. 246 Thm 3.2(2) p. 83; per D′(Ω): da verificare | MAJOR CONV-1 | no |
| CONV-B1, B2, B3 | DIMOSTRATO | PASS | no |
| CONV-T8(a–d) | DIMOSTRATO (L²); ordine 1 in L^∞: V-ex (confermato numericamente) | PASS-con-fix (CONV-5) | no |
| CONV-R1(a–c) | DIMOSTRATO | PASS | no |
| CONV-R1-F | FALSO (f = ξ, g = τ) | confermato | no |
| CONV-MZ1, MZ2, MZ3 | DIMOSTRATO | PASS | no |
| CONV-MZ3-F | FALSO (con il controesempio a12 = 0, a21 = 1 di CONV-9) | confermato con fix CONV-9 | no |
| CONV-T7 | proposizione DIMOSTRATO; contratto = specifica | PASS | no |
