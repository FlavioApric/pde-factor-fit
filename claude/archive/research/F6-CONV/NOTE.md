# NOTE — F6-CONV (sviluppo e prove scritte; stato: scouting, NESSUN claim DIMOSTRATO)

Convenzioni: R = ℂ[τ,ξ] (in §5 R_n = ℂ[τ,ξ_1,…,ξ_d]); R_{≤m} = polinomi di grado ≤ m (dimensione binom(m+2,2)); filtrazione 𝓓_m := R_{≤m} (livello U1 a coeff. costanti di F6-DICT). Modelli M1/M2/M3 come in GATE3/work/C3 §2. "Prova scritta" = prova completa scritta qui, non auditata (serve S-CHECK in Fase 8). Script: `sympy/conv_learner.py`, `sympy/conv_locality.py`, `sympy/conv_stab.py` (+ `.out`).

---
## §1 (C1) Identificazione nel limite lungo la filtrazione

### Dati e regola
Ipotesi (H-an): Ω ⊂ ℝ² aperto connesso, p₀ ∈ Ω, u reale-analitica su Ω (per u solo C^∞ tutto vale con Ann(u) sostituito dall'annullatore della serie di Taylor in p₀, che contiene Ann(u)). Dato al passo K: il jet j_K u = (∂^γ u(p₀))_{|γ|≤K} (modello M2).

Per m ≤ K: **N_{m,K} := {Q ∈ R_{≤m} : ∂^β(Q(∂)u)(p₀) = 0 ∀|β| ≤ K−m}** — calcolabile dal solo j_K u (∂^β Q u(p₀) = Σ q_α ∂^{α+β}u(p₀), |α+β| ≤ K).

**Regola del grado minimo L\*:** m\*(K) := min{m ≤ K : N_{m,K} ≠ 0} (∞ se non esiste); uscita O_K := gcd(N_{m\*(K),K}) (generatore normalizzato). Variante con maggiorante B: O^B_K := ideale generato da N_{B,K}.

### [CONV-L1] Stabilizzazione per livello — prova scritta
Per m fissato: (a) N_{m,K+1} ⊆ N_{m,K} (al passo K+1 le condizioni sono un soprainsieme); (b) ∩_K N_{m,K} = Ann(u) ∩ R_{≤m}; (c) la catena si stabilizza: N_{m,K} = Ann(u) ∩ R_{≤m} per K ≥ K\*(m) := m + ν_m(u), dove
  **ν_m(u) := max{ord_{p₀}(Q u) : Q ∈ R_{≤m} ∖ Ann(u)}** (ordine di annullamento in p₀), che è finito; e K\*(m) è il minimo indice con questa proprietà.
*Prova.* (b) Q ∈ ∩_K N_{m,K} ⟺ Qu ha serie di Taylor nulla in p₀ ⟺ (analiticità, Ω connesso) Qu ≡ 0 su Ω. (c) ord(Qu) dipende solo dalla classe di Q in W_m := R_{≤m}/(Ann ∩ R_{≤m}); gli insiemi {[Q] ∈ W_m : ord(Qu) ≥ k} ∪ {0} sono sottospazi lineari decrescenti in k con intersezione {0} (per (b)); in uno spazio di dimensione finita la catena diventa {0} a un k finito: dunque ν_m < ∞. Infine Q ∉ Ann sta in N_{m,K} ⟺ ord(Qu) ≥ K−m+1; quindi N_{m,K} = Ann ∩ R_{≤m} ⟺ ν_m ≤ K−m. ∎

### [CONV-T1] Identificazione nel limite (classe principale) e con maggiorante — prova scritta
Sotto (H-an):
1. Se Ann(u) ≠ 0 e d := min{deg Q : 0 ≠ Q ∈ Ann(u)}, allora per K ≥ K\* := max_{m≤d} K\*(m) si ha m\*(K) = d e O_K = g_d := gcd(Ann(u) ∩ R_{≤d}).
2. **Se Ann(u) = (P), allora O_K = P per ogni K ≥ K\***: convergenza esatta in un numero finito di passi, senza conoscere deg P.
3. Se Ann(u) = 0, allora m\*(K) → ∞ (il grado dell'uscita diverge).
4. (Maggiorante, cfr. P4-T4) Se Ann(u) è generato da Ann(u) ∩ R_{≤B}, allora O^B_K = Ann(u) per K ≥ K\*(B); in particolare gcd(N_{B,K}) = G_u (C3-T6) da quel passo in poi.
5. **Cambi di ipotesi (mind changes), uniformi:** m\*(K) è non decrescente in K e, a m\* fisso, deg O_K è non decrescente; perciò nel caso 2 il numero di cambi dell'uscita è ≤ (d+1)(d+2)/2, d = deg P, **per ogni u** (velocità alla Gold in "numero di errori", uniforme). Il **tempo** di convergenza K\* invece non è limitato da alcuna funzione di d (punto 6).
6. **Non uniformità del tempo.** Per ogni N esiste u con Ann(u) = (τ) (d = 1) e K\*(u) ≥ N+2: u = f(x) = 1 + x^{N+2}e^{x²} (f non EP ⇒ Ann(u) = (τ) per C3-T1/II-L1, ODE-test; ∂_x u ha ordine N+1 in 0 ⇒ ξ ∈ N_{1,K} finché K−1 ≤ N). SymPy: `conv_learner.out` (a), N = 3: uscita 1 per K ≤ 4, τ da K = 5 = N+2. Più in generale K\* = max_{m≤d}(m + ν_m(u)) per CONV-L1 è la formula esatta (velocità "a posteriori" in termini degli ordini di annullamento).
7. **Mai certificabile (raccordo con C3-P1).** Per nessun K il dato j_K u permette di sapere che K ≥ K\*: per C3-P1[M2] lo stesso jet j_K u è compatibile con u′ con Ann(u′) ⊋ (P), e al passo K L\* dà su u′ la stessa uscita (stessi dati); inoltre, per il punto 6, nessuna funzione di (d, K) maggiora K\*. La convergenza è "in the limit" nel senso di Gold: corretta da un certo passo, senza segnale di arrivo.
*Prova.* 1: per m < d, Ann ∩ R_{≤m} = 0, quindi N_{m,K} = 0 per K ≥ K\*(m) (CONV-L1); a m = d, N_{d,K} = Ann ∩ R_{≤d} ≠ 0 per K ≥ K\*(d). 2: Ann ∩ R_{≤deg P} = ℂP. 3: per ogni m, N_{m',K} = 0 per m' ≤ m e K ≥ max_{m'≤m}K\*(m'). 4: CONV-L1 a m = B. 5: N_{m,K} = 0 ⇒ N_{m,K+1} = 0 (monotonia (a)), quindi m\* non decresce; a m\* fisso N decresce, il gcd di un sottospazio più piccolo è un multiplo del precedente, quindi cambia solo crescendo di grado (≤ m+1 valori: 0..m); somma su m = 0..d. 6: calcolo diretto (sopra). ∎
**Nota (velocità nella classe EP).** Per u EP con d_u = dim R·u, C3-T3 dà una soglia esplicita (jet di ordine 2d_u − 1 determina Ann(u)): è il solo caso con K\* uniforme noto; fuori da EP il punto 6 mostra che una soglia uniforme non esiste.
**Nota (Ann non principale, senza maggiorante).** L\* converge a g_d, che può essere un multiplo proprio di G_u (es. Ann = G·(τ, ξ²) ⇒ g_d = Gτ). Se G_u sia identificabile nel limite senza maggiorante è **APERTO** (CONV-Q1).

### [CONV-T2] Teorema di Gold analitico: la località non si decide nel limite — prova scritta
**Enunciato.** Sia φ = (φ_K)_K una qualunque successione di funzioni (anche non calcolabili, non continue) φ_K : {jet di ordine K} → {"legge", "nessuna legge"}. Allora esiste una funzione intera reale u su ℝ² tale che φ_K(j_K u) non converge a 1_{Ann(u)≠0}. In particolare nessuna procedura, nemmeno idealizzata, converge (corretta da un certo K in poi) sia su tutte le u con Ann(u) ≠ 0 sia su tutte le u con Ann(u) = 0; e nessun learner identifica nel limite la classe {u : Ann(u) principale} ∪ {u : Ann(u) = 0} (con uscita "nessuna legge" per la seconda).
**Prova.** Se φ sbaglia nel limite su qualche polinomio (Ann ≠ 0: ∂_t^{deg+1} lo annulla) abbiamo finito. Altrimenti φ converge a "legge" su ogni polinomio. Spazio dei jet formali reali J = ℝ^{ℕ²} con topologia prodotto. Per m ≥ 0 sia C_m := {j ∈ J : Ann(j) ∩ R_{≤m} ≠ 0}.
(i) C_m è chiuso: Ann(j) ∩ R_{≤m} ≠ 0 ⟺ N_{m,K}(j) ≠ 0 ∀K (catena decrescente di sottospazi non nulli di dimensione finita ha intersezione non nulla), e ciascuna condizione "rango non pieno" è chiusa (minori nulli).
(ii) Passo cardine (evitare C_m restando vicini a un polinomio). Sia p un polinomio e L ≥ deg p. Sia g := (t²+x²)^{L+1} e^{t²+x²}: Ann(g) = 0 (la parte di grado massimo di Q(∂)g/e^{t²+x²} è Q_top(2t,2x)(t²+x²)^{L+1} ≠ 0) e g si annulla all'ordine > L in 0. Per K grande la sottomatrice delle righe |β| > L della matrice di N_{m,K} per il jet p + c·g coinvolge solo i coefficienti di ordine > L, cioè quelli di c·g, ed ha rango pieno (altrimenti per ogni K esisterebbe Q ≠ 0 di grado ≤ m con Qg polinomio di grado ≤ L, e allora ∂_t^{L+1}Q ∈ Ann(g), assurdo — si usa la stabilizzazione come in CONV-L1). Quindi un minore di quella sottomatrice è un polinomio non identicamente nullo nei coefficienti liberi di ordine in (L, K]: l'insieme delle scelte di tali coefficienti per cui N_{m,K} = 0 è aperto e denso, e contiene scelte con |c_γ| ≤ 1/(|γ|!)².
(iii) Costruzione. Poniamo p₀ = 0, K₀ = 0. Al passo k: dato il polinomio p_k e K_k ≥ deg p_k con φ_{K_k}(j_{K_k}p_k) = "legge", scegliamo con (ii) (m = k, L = K_k) coefficienti di ordine in (K_k, L′_k] con |c_γ| ≤ 1/(|γ|!)² tali che ogni jet che li estende abbia N_{k,L′_k} = 0, quindi stia fuori da C_k; sia p_{k+1} il polinomio troncato all'ordine L′_k. Poiché φ converge a "legge" su p_{k+1}, esiste K_{k+1} ≥ L′_k + 1 con φ_{K_{k+1}}(j_{K_{k+1}}p_{k+1}) = "legge". Il limite u_∞ := lim p_k ha coefficienti |c_γ| ≤ 1/(|γ|!)² ⇒ intera reale; j_{K_k}u_∞ = j_{K_k}p_k ⇒ φ dice "legge" infinite volte; u_∞ ∉ ∪_k C_k ⇒ Ann(u_∞) = 0. ∎
**Lettura.** "Ann(u) ≠ 0" è *verificabile nel limite* (la regola "dì legge al passo K se m\*(K) = m\*(K−1)" è definitivamente corretta quando Ann ≠ 0 e sbaglia infinite volte se Ann = 0) ma non *decidibile nel limite*. Topologicamente: {Ann ≠ 0} è F_σ (∪_m C_m) ma non G_δ nello spazio dei jet (Baire: C_m chiusi senza interno per (ii); i polinomi sono densi), cioè Σ⁰₂ ∖ Π⁰₂ — coerente con la caratterizzazione classica "decidibile nel limite ⟺ Δ⁰₂" della teoria dell'apprendimento formale (Kelly 1996; da verificare il numero) e con il teorema di Gold (1967: classi "superfinite" non apprendibili da testo). È il confine N1(iv) di F6-DICT reso esatto.

### Altre forme di "dati che crescono"
- **Campionamento più fine (M3 discretizzato).** Dati su griglia di passo h: le differenze finite di ordine r danno jet/feature con errore O(h^r) in norma L² ⇒ rientra in §2 con δ = C h^r: consistenza per h → 0 con velocità Lipschitz/Hölder (CONV-T4/T5).
- **Dominio più grande.** Ann_{Ω′}(u) ⊆ Ann_Ω(u) per Ω ⊆ Ω′. Per u analitica non cambia nulla; per P iperbolico (u non analitica) Ann_Ω può scendere strettamente al crescere di Ω e la stabilizzazione della catena discendente non è garantita a priori (R non è artiniano): **APERTO** (CONV-Q3).

---
## §2 Dati rumorosi: discontinuità, stabilità condizionale, consistenza con regola di scelta

### [CONV-T3] Discontinuità ovunque dell'identificazione — prova scritta
Sia X uno spazio di funzioni su Ω (H^m(Ω), C^k(Ω̄), C^∞, funzioni intere con topologia compatta-aperta) in cui i polinomi sono densi e che contiene g = e^{t²+x²}. Allora sia {Ann = 0} sia {Ann ≠ 0} sono densi, e la mappa u ↦ Ann(u) (a valori nell'insieme discreto degli ideali) non è continua in alcun punto; in particolare non è continua in nessuna u con Ann(u) = (P).
*Prova.* Densità di {Ann ≠ 0}: polinomi. Densità di {Ann = 0}: per u ∈ X e m fissato, Φ_{u+εg} = Φ_u + εΦ_g su R_{≤m}; Φ_g è iniettivo (Ann(g) = 0), quindi esistono funzionali ψ_1..ψ_r (test o valori di derivate) con matrice (⟨Qg,ψ_i⟩) di rango pieno; un minore di (⟨Q(u+εg),ψ_i⟩) è un polinomio in ε con coefficiente direttivo ≠ 0, quindi si annulla per un numero finito di ε. Unione su m: Ann(u+εg) = 0 per ogni ε fuori da un insieme numerabile. ∎
È la forma "qualitativa" di P2-T4 (nessuna regolarizzazione uniformemente lipschitziana): ciò che è stabile è solo relativo a un livello 𝓓_n e con margine.

### [CONV-T4] Stabilità condizionale lipschitziana e hölderiana a livello 𝓓_n — prova scritta
Quadro M3: Ω limitato lipschitziano, base fissata {∂^α : |α| ≤ n} di 𝓓_n (M elementi), operatore di feature Φ(u): ℂ^M → L²(Ω), λ ↦ Σ λ_α ∂^α u; valori singolari σ_1(Φ) ≤ σ_2(Φ) ≤ …; norma ‖e‖_{H^n}² := Σ_{|α|≤n}‖∂^α e‖²_{L²}.
**Ipotesi di margine (insieme sorgente):** Φ(u)λ\* = 0 con |λ\*| = 1 e σ_2(Φ(u)) ≥ ρ > 0 (⟺ Ann(u) ∩ 𝓓_n = ℂλ\*: identificazione relativa con gap ρ).
(a) **Lipschitz.** Se ‖ũ − u‖_{H^n} ≤ δ e λ̃ (|λ̃| = 1) minimizza ‖Φ(ũ)λ‖, allora **sin∠(λ̃, λ\*) ≤ 2δ/ρ**. L'ordine δ/ρ è ottimale (esempio 2×2: A = diag(0,ρ), E = [[0,0],[δ,0]] ⇒ sin θ = δ/√(ρ²+δ²)).
(b) **Hölder.** Se il rumore è solo in L² (‖ũ₀ − u‖_{L²} ≤ δ) e vale il limite a priori ‖u‖_{H^{n+s}} ≤ 𝔐 (s > 0), sia ũ ∈ B_𝔐(H^{n+s}) con ‖ũ − ũ₀‖_{L²} ≤ δ (esiste: u stessa). Allora sin∠ ≤ 2C_Ω (2δ)^{s/(n+s)} (2𝔐)^{n/(n+s)} / ρ.
(c) **Certificato di misfit col rumore.** Se σ_1(Φ(ũ)) > δ allora Ann(u) ∩ 𝓓_n = 0 (certificato finito); il "fit" non è mai certificabile (CONV-T3, C3-P1). Asimmetria Π/Σ coerente con F6-DICT D2.
*Prova.* (a) E := Φ(ũ) − Φ(u): ‖Eλ‖ ≤ Σ|λ_α|‖∂^α(ũ−u)‖ ≤ |λ|·‖ũ−u‖_{H^n} (Cauchy–Schwarz), quindi ‖E‖ ≤ δ. Scriviamo λ̃ = cλ\* + w, w ⊥ λ\*, |w| = sin θ. Allora ρ sin θ ≤ ‖Φ(u)w‖ = ‖Φ(u)λ̃‖ ≤ ‖Φ(ũ)λ̃‖ + δ ≤ ‖Φ(ũ)λ\*‖ + δ ≤ ‖Φ(u)λ\*‖ + 2δ = 2δ. (b) e := ũ − u: ‖e‖_{L²} ≤ 2δ, ‖e‖_{H^{n+s}} ≤ 2𝔐; disuguaglianza di interpolazione ‖e‖_{H^n} ≤ C_Ω‖e‖_{L²}^{s/(n+s)}‖e‖_{H^{n+s}}^{n/(n+s)} su domini lipschitziani limitati (Adams–Fournier, cap. 5; numero del teorema da verificare) e poi (a). (c) Disuguaglianza di Weyl per valori singolari: σ_1(Φ(u)) ≥ σ_1(Φ(ũ)) − ‖E‖ > 0. ∎
SymPy/numerica di controllo: `conv_stab.out` (20000 prove casuali del rapporto sin θ/(2δ/ρ) ≤ 1; esempio 2×2 simbolico).
**Osservazione (filtrazione).** ρ_n(u) := σ_2(Φ_n(u)) non è monotona in n in modo utile per n > d (il nucleo diventa P·R_{≤n−d}, dimensione > 1): per questo la stabilità va formulata al livello minimo d, cioè con la regola di CONV-T5. Il margine ρ → 0 avvicinandosi all'insieme non identificabile è esattamente la ragione di P2-T4.

### [CONV-T5] Consistenza con regola di discrepanza (scelta del livello) — prova scritta
Regola R_δ: m(δ) := min{m : σ_1(Φ_m(ũ)) ≤ δ_m}, uscita λ̃(δ) := vettore singolare minimo di Φ_{m(δ)}(ũ), con δ_m = δ (rumore in H^m) o δ_m = C_Ω(2δ)^{s/(m+s)}(2𝔐)^{m/(m+s)} (rumore L² + limite a priori). Sia Ann(u) = (P), d = deg P, s_m := σ_1(Φ_m(u)) > 0 per m < d, ρ_d := σ_2(Φ_d(u)) > 0.
1. Se δ_m < s_m/2 per ogni m < d (vero per δ < δ₀(u)), allora m(δ) = d e sin∠(λ̃(δ), P) ≤ 2δ_d/ρ_d → 0: **consistenza con velocità** (Lipschitz in δ, o Hölder δ^{s/(d+s)}).
2. Se Ann(u) = 0: m(δ) → ∞ per δ → 0 (divergenza del livello = segnale "nel limite" di assenza di legge, mai una decisione: CONV-T2).
3. Se Ann(u) non principale con grado minimo d: λ̃(δ) converge al sottospazio Ann ∩ R_{≤d} con sin∠ ≤ 2δ_d/σ_{r+1}, r = dim(Ann ∩ R_{≤d}).
4. δ₀(u) = ½ min_{m<d} s_m non è calcolabile da dati finiti (altrimenti si certificherebbe il grado minimo, contro C3-P1/P4-T5): stessa struttura dei teoremi di convergenza della regolarizzazione con principio di discrepanza (Morozov; Engl–Hanke–Neubauer cap. 4), dove le velocità valgono sotto condizione sorgente.
*Prova.* Weyl: |σ_1(Φ_m(ũ)) − s_m| ≤ δ_m. Per m < d: σ_1(Φ_m(ũ)) ≥ s_m − δ_m > δ_m, quindi m non è scelto; per m = d: σ_1 ≤ 0 + δ_d. Poi CONV-T4. 2 e 3 analoghi. ∎

---
## §3 (C2) Località: differenziale, non locale, nessuna legge

### Livello operatore (Peetre) — CON-FONTE da verificare
Peetre (1959/60): un operatore lineare T: C_c^∞(Ω) → C^∞(Ω) con supp Tf ⊆ supp f è localmente differenziale di ordine localmente finito (senza ipotesi di continuità). Caso invariante per traslazioni: T = convoluzione con k ∈ D′; locale ⟺ supp k ⊆ {0} ⟺ k = Σ c_α ∂^αδ (struttura delle distribuzioni a supporto puntuale) ⟺ simbolo polinomiale. Quindi a livello di operatori: **locale ⟺ differenziale ⟺ simbolo polinomiale** (U1 di F6-DICT).

### Livello dato (una soluzione) — [CONV-T6] criterio spettrale — prova scritta
Quadro: u(t,x) = ∫ e^{a(κ)t + iκx} f̂(κ) dκ, f̂ ∈ L¹ a supporto compatto S, a continua su S (soluzione della legge non locale u_t = a(D_x)u; include frazionari, semigruppi di Poisson/KG, memoria e ritardo sui modi esponenziali). Allora su ogni Ω connesso:
1. **Ann(u) = I(Γ) := {Q ∈ R : Q(a(κ), iκ) = 0 per q.o. κ ∈ S}** (ideale di annullamento del grafo del simbolo sopra il supporto spettrale).
2. Se S contiene un intervallo J su cui a è reale-analitica: Ann(u) ≠ 0 ⟺ a|_J è una funzione algebrica; in tal caso (S unione finita di intervalli su cui a è analitica) Ann(u) è principale, generato dal prodotto dei polinomi minimi dei rami distinti, e L\* (CONV-T1) converge a esso. Se a è trascendente su J, **Ann(u) = 0: nessuna legge differenziale**, pur esistendo la legge non locale.
3. **Non identificabilità della legge non locale:** ogni moltiplicatore b con b = a su S genera lo stesso dato; la legge è determinata solo su Γ. Se a è algebrica su S, legge locale e legge non locale sono **indistinguibili** da u.
4. **Nessuna legge (invariante per traslazioni) affatto:** se u = ∫ e^{i(ωt+κx)} ĝ(ω,κ) dω dκ con supp ĝ con interno non vuoto in ℝ², nessun moltiplicatore reale-analitico non nullo annulla u.
*Prova.* 1: Q(∂)u = ∫ Q(a(κ),iκ) e^{…} f̂ dκ; per t fissato è una funzione intera di x (f̂ a supporto compatto), nulla su un intervallo ⇒ nulla su ℝ ⇒ Q(a(κ),iκ) f̂(κ) = 0 q.o. (iniettività di Fourier). 2: Q(a(κ),iκ) è analitica su J: nulla su J o con zeri isolati; nulla per q.o. κ ∈ J ⟺ identicamente nulla ⟺ (a, iκ) soddisfa una relazione algebrica. I polinomi che si annullano su un ramo analitico algebrico formano l'ideale primo del polinomio minimo (irriducibile); su più rami, intersezione = prodotto dei minimi distinti. 3: ovvio da 1. 4: m(ω,κ)ĝ = 0 con m analitica nulla su un aperto ⇒ m ≡ 0. ∎
**Esempi verificati (`conv_locality.out`).** Poisson e^{−t|D|}: τ = −|κ| su entrambi i lati ⇒ τ² + ξ² = 0: **u è armonica** (legge non locale ⇒ legge locale di Laplace; L\* restituisce τ²+ξ², `conv_learner.out` (b)). e^{−t√(1−∂²)}: τ² + ξ² − 1 = 0 (Klein–Gordon ellittico). Memoria esponenziale ∫_{−∞}^t e^{−a(t−s)}u_xx ds: τ(τ+a) = ξ² (**telegrafo**, Cattaneo). Frazionario |κ|^{2s} con 2s ∈ ℚ su un semiasse: algebrico. Frazionario irrazionale (λ_j = j^{√2}): il grado minimo dell'annullatore del dato a M modi cresce con M (2,2,3,3 per M = 2..5) mentre per il calore resta 2 — V-ex del punto 2. Ritardo u_t(t) = u_xx(t−σ): τ = e^{−στ}ξ², trascendente ⇒ Ann = 0 per dati con spettro infinito.
**Tricotomia raffinata (C2).** (L) legge locale nelle variabili date: Ann(u) ≠ 0; (L⁺) legge locale solo dopo aver aggiunto variabili (estensione di Caffarelli–Silvestre per (−Δ)^s; memoria completamente monotona → somme di esponenziali → sistema locale aumentato; mappe Dirichlet-to-Neumann al bordo): invisibile ad Ann(u) nelle variabili date; (N) nessuna legge nella classe ammessa (punto 4). "Locale o non locale" **non è una proprietà di u ma della coppia (u, classe di leggi)**: da una soluzione si identifica al più la chiusura di Zariski del grafo del simbolo.
**Decidibilità (raccordo con T2/T4).** La località si *refuta* con certificato finito a ogni livello (CONV-T4(c)), si *verifica nel limite*, non si *decide nel limite* (CONV-T2).

---
## §4 (C3) Parti iterative: "contratto di convergenza" uniforme — [CONV-T7] candidato (enunciato di composizione)
Ogni passo s_i dell'algoritmo è etichettato:
- **(A) finito/esatto:** eliminazione su 𝓓_n (C3-A1); Gauss/Wei–Norman globale ⟺ Wronskiani ≠ 0 (II-T7); prodotti finiti per Lie risolubile (P1-T4); formula E_int in 𝔅 (P1-T2, 2^N termini); splitting di moltiplicatori commutanti su ℝ (E^mult = 0, R5-T2).
- **(B) serie/iterazione convergente con maggiorante esplicito e resto a posteriori:** Dyson–Phillips con B limitato, ‖S(t) − Σ_{k≤N}S_k(t)‖ ≤ M e^{ωt} Σ_{k>N}(M‖B‖t)^k/k! (Engel–Nagel III.1; P3-T1 per ordine pari dissipativo + perturbazione di ordine inferiore, Miyadera–Voigt CON-FONTE III.3.14); Magnus per A(s) **limitati** con ∫_0^t‖A(s)‖ds < π (Moan–Niesen 2008); splitting Lie/Strang per generatori non commutanti sotto le ipotesi di Trotter–Kato–Chernoff (stabilità + nucleo), con velocità sotto regolarità; integratori di Magnus troncati per Schrödinger non autonomo (Hochbruck–Lubich 2003) — tutti con ipotesi da verificare caso per caso (F6-VAR per V(t,x)).
- **(C) asintotico/divergente o senza garanzia:** serie di Magnus/BCH con generatori illimitati senza ipotesi; E^mult per algebre non risolubili (P1-T5: nessun prodotto finito; espansione solo locale); splitting con bordo non omogeneo/Dirichlet con **riduzione d'ordine** (Einkemmer–Ostermann 2015; Dang–Einkemmer–Ostermann 2025: Strang ridotto a ordine 1 con Dirichlet) — il difetto Θ(t^{5/4}) di P3-T3 è un'istanza del fenomeno.
**Enunciato (composizione).** Se la catena garantita contiene solo passi (A)/(B), con maggioranti ε_i(N_i) e passi a valle lipschitziani di costanti L_j, l'errore totale è ≤ Σ_i (Π_{j>i} L_j) ε_i(N_i) (telescopica); un passo (C) non può stare nella catena garantita e va dichiarato. La sola parte non iterativa ma "al limite" è l'identificazione (§1), che converge in tempo finito ma non certificabile. Prova: telescopica standard. Novità: nulla come teorema; valore come **specifica** (ALGORITMO_ESTESO, passo 7).

---
## §5 Dimensione > 1+1 (Ω ⊂ ℝ^{1+d}, d ≥ 2)

### [CONV-P8] Riduzione indipendente dalla dimensione — prova scritta
R_n = ℂ[τ,ξ_1..ξ_d], P = ∏P_i ridotto (P_i irriducibili distinti), u in un qualunque R_n-modulo di funzioni/distribuzioni su un qualunque Ω, P(∂)u = 0, w_i := (P/P_i)(∂)u. Allora **Ann(u) = (P) ⟺ Ann(w_i) = (P_i) per ogni i**.
*Prova.* ⇒: se Qw_i = 0, Q(P/P_i) ∈ Ann(u) = (P) ⇒ P_i | Q (P_i primo, coprimo con P/P_i). ⇐: se Qu = 0 allora Qw_i = (P/P_i)Qu = 0 ⇒ Q ∈ (P_i) per ogni i ⇒ P | Q. ∎
In 1+1: Ann(w_i) ⊋ (P_i) ⟺ V(Ann w_i) finito ⟺ w_i EP (C3-L3) — è C3-T1. In 1+d, d ≥ 2: Ann(w_i) ⊋ (P_i) ⟺ w_i risolve un sistema **sovradeterminato** (P_i, Q) con varietà di dimensione ≥ d−1 ≥ 1 (Krull), e lo spazio delle soluzioni è **infinito-dimensionale** (es. d = 2: P_i = τ − ξ_1, Q = ξ_2, w = f(t+x) qualsiasi). Conseguenze: C3-T1 sopravvive come caratterizzazione ma la classe eccezionale non è più EP; C3-T3 (soglia di jet finita) non ha analogo; CONV-T1/T2/T4/T5 valgono senza modifiche (le prove usano solo dim R_{≤m} < ∞, analiticità, interpolazione).
**Scomposizione (C12-T1′).** Esistenza su Ω convesso: iniettività di D′(Ω), C^∞(Ω) come R_n-moduli (principio fondamentale di Ehrenpreis–Palamodov; Malgrange; Hörmander ICASV cap. 7.6 — numeri da verificare). Ambiguità: per d ≥ 2, dim R_n/(Q_i,Q_j) è finita **solo se è 0** (se V(Q_i) ∩ V(Q_j) ≠ ∅ ogni componente ha dimensione ≥ n−2 ≥ 1 per il teorema dell'altezza di Krull); dunque "δ(P) finito ⟺ δ(P) = 0 ⟺ fattori a due a due comassimali", e altrimenti l'ambiguità è infinito-dimensionale. Domini: la condizione topologica H¹_dR = 0 (C12-T1′) va sostituita da condizioni di P-convessità; per le parti sovradeterminate vale il fenomeno di Hartogs–Ehrenpreis (estensione attraverso compatti), quindi l'ostruzione C12-P10 da "buchi compatti" potrebbe sparire per d ≥ 2: **APERTO** (CONV-Q5).
**E_int.** R5-T2/P1-T2 (semigruppi commutanti in uno spazio di Banach) sono indipendenti dalla dimensione: sopravvivono.

---
## §6 Condizioni al bordo
1. Ann(u) è interno/locale: le condizioni al bordo **non sono visibili** in Ann(u). Per identificarle serve un dizionario di bordo 𝓑_n = {b_j γ_j} (tracce γ_0, γ_1, …, continue H^{n+1}(Ω) → H^{n+1/2−j}(∂Ω)); CONV-T4/T5 si trasportano parola per parola sostituendo Φ con la mappa di feature di traccia (candidato, non scritto in dettaglio).
2. Il bordo rompe la commutazione: E_int dal bordo (P3-T3, Θ(t^{5/4})) ⇒ i passi di splitting passano da (A) a (B)/(C) con riduzione d'ordine.
3. Il bordo crea non località da leggi locali (Dirichlet-to-Neumann): caso (L⁺) della tricotomia.
4. Effetto su C1: con bc omogenee su (0,L) le soluzioni sono serie modali Σ c_k e^{λ_k t} sin(kπx/L); Ann(u) = I({(λ_k, ±ikπ/L)}) e vale CONV-T6 con S discreto infinito: Ann ≠ 0 ⟺ i punti stanno su una curva algebrica (es. λ_k = a(ikπ/L) con a polinomio).
