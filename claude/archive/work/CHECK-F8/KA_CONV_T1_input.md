# KA input — CONV-T1 (preparato da S-CHECK-F8-CONV, 27/10/2026)

Testo estratto VERBATIM da work/S8-CONV/PROOF_PACKAGE.md (§0.1 notazione, §1 intro, §1.1 CONV-L1, §1.2 CONV-T1) più l'enunciato del lemma esterno usato (C3-P1[M2], dal LEDGER e da work/C3/PROOF_PACKAGE.md §5). Compito del revisore: kill-argument, cioè trovare un controesempio, un passo falso, un'ipotesi mancante o un enunciato più forte di quanto la prova dia. Non si richiede di valutare la novità.

## Lemma esterno usato (DIMOSTRATO nel LEDGER, qui come scatola nera)
**C3-P1[M2].** Ipotesi: Ω ⊂ ℝ² aperto connesso (non serve la convessità), p_0 ∈ Ω, P ∈ ℂ[τ,ξ] non costante, K ≥ 0, u ∈ C^∞(Ω) con P(∂)u = 0. Tesi: esiste v ∈ E_P (soluzioni esponenziali-polinomiali di P(∂)v = 0, quindi funzioni intere) con ∂^αv(p_0) = ∂^αu(p_0) per ogni |α| ≤ K, e Ann(v) ⊋ (P).
**C3-T3.** Per u esponenziale-polinomiale (EP) con d_u = dim R·u, il jet di ordine 2d_u − 1 in un punto determina Ann(u).

## Testo verbatim
- R_n := ℂ[τ, ξ_1, …, ξ_{n−1}] (variabili duali di ∂_t, ∂_{x_1}, …); per n = 2 si scrive R = ℂ[τ, ξ]. R_{≤m} := polinomi di grado totale ≤ m; dim R_{≤m} = binom(m+n, n). Q(∂) è l'operatore ottenuto sostituendo ∂_t a τ e ∂_{x_j} a ξ_j.
- Per u in un R_n-modulo di funzioni o distribuzioni su Ω: Ann(u) := {Q ∈ R_n : Q(∂)u = 0 su Ω}.
- ord_{p₀}(f) := ordine di annullamento in p₀ di una funzione analitica f (∞ se il germe è nullo).
- **Modelli di dato (NOTAZIONE v5):** DM2 = jet esatto in un punto; DM3 = u ∈ H^m(Ω) (qui anche con rumore dichiarato). **Modello di calcolo** (fix O9 di DEVIL-6): CONV-L1/T1/T2 sono nel modello BSS (numeri reali esatti, operazioni esatte), non nel modello di Turing; CONV-T2 vale perfino per funzioni arbitrarie dei jet.
- Valori singolari: σ_1(Φ) ≤ σ_2(Φ) ≤ … (ordine **crescente**, come in F6-CONV; in DICT σ indica altro: fix O9).

## §1 Identificazione nel limite lungo la filtrazione (modello DM2, calcolo BSS)

**Ipotesi (H-an).** Ω ⊂ ℝ^n aperto connesso, p₀ ∈ Ω, u reale-analitica su Ω. Dato al passo K: il jet j_K u = (∂^γ u(p₀))_{|γ|≤K}.
Per m ≤ K: **N_{m,K} := {Q ∈ R_{≤m} : ∂^β(Q(∂)u)(p₀) = 0 per ogni |β| ≤ K − m}**. È calcolabile da j_K u: se Q = Σ_α q_α ξ^α (con ξ^α che indica anche le potenze di τ), allora ∂^β(Qu)(p₀) = Σ_α q_α ∂^{α+β}u(p₀) e |α + β| ≤ K. In forma matriciale N_{m,K} è il nucleo della matrice M_{m,K}(j) con righe indicizzate da β (|β| ≤ K − m), colonne da α (|α| ≤ m) ed elemento j_{α+β}.

### §1.1 [CONV-L1] Stabilizzazione per livello — PROVA SCRITTA
**Enunciato.** Sotto (H-an), per ogni m:
(a) N_{m,K+1} ⊆ N_{m,K};
(b) ∩_{K≥m} N_{m,K} = Ann(u) ∩ R_{≤m};
(c) ν_m(u) := max{ord_{p₀}(Q(∂)u) : Q ∈ R_{≤m} ∖ Ann(u)} è finito (con max ∅ := −1), e N_{m,K} = Ann(u) ∩ R_{≤m} ⟺ K ≥ K\*(m) := m + ν_m(u). *(Convenzione: se R_{≤m} ⊆ Ann(u), allora ν_m = −1 e la catena è costante da K = m.)*
**Prova.** (a) Le condizioni che definiscono N_{m,K+1} contengono quelle di N_{m,K}.
(b) Q sta nell'intersezione ⟺ ∂^β(Qu)(p₀) = 0 per ogni β ⟺ la serie di Taylor di Qu in p₀ è nulla ⟺ Qu ≡ 0 su Ω: Qu è reale-analitica e Ω è connesso (principio d'identità).
(c) Sia W_m := R_{≤m}/(Ann(u) ∩ R_{≤m}). La funzione Q ↦ ord_{p₀}(Qu) dipende solo dalla classe di Q in W_m, perché Qu = Q′u se Q − Q′ ∈ Ann(u). Per k ≥ 0 sia F_k := {[Q] ∈ W_m : ord_{p₀}(Qu) ≥ k}. Ogni F_k è un sottospazio lineare (l'ordine della somma è almeno il minimo degli ordini), F_{k+1} ⊆ F_k, e ∩_k F_k = {0} per (b). Una catena decrescente di sottospazi di uno spazio di dimensione finita è stazionaria: F_k = F_{k₀} per k ≥ k₀, quindi F_{k₀} = ∩_k F_k = {0}. Allora ogni [Q] ≠ 0 ha ord(Qu) < k₀, e ν_m ≤ k₀ − 1 < ∞. Infine, per Q ∉ Ann(u): Q ∈ N_{m,K} ⟺ ∂^β(Qu)(p₀) = 0 per |β| ≤ K − m ⟺ ord(Qu) ≥ K − m + 1. Dunque N_{m,K} = Ann(u) ∩ R_{≤m} ⟺ nessun Q ∉ Ann ha ord(Qu) ≥ K − m + 1 ⟺ ν_m ≤ K − m ⟺ K ≥ m + ν_m. ∎

### §1.2 [CONV-T1] Identificazione nel limite — PROVA SCRITTA
**Regola del grado minimo L\*.** m\*(K) := min{m ≤ K : N_{m,K} ≠ 0} (∞ se non esiste); uscita O_K := gcd(N_{m\*(K),K}) normalizzato (monico rispetto a un ordine monomiale fissato). Con maggiorante B: O^B_K := ideale generato da N_{B,K}.
**Enunciato.** Sotto (H-an):
1. Se Ann(u) ≠ 0 e d := min{deg Q : 0 ≠ Q ∈ Ann(u)}, allora per K ≥ K\* := max_{m≤d} K\*(m) vale m\*(K) = d e O_K = g_d := gcd(Ann(u) ∩ R_{≤d}).
2. Se Ann(u) = (P), allora O_K = P (normalizzato) per ogni K ≥ K\*. Il grado di P non è un dato della regola.
3. Se Ann(u) = 0, allora m\*(K) → ∞.
4. Se Ann(u) è generato da Ann(u) ∩ R_{≤B}, allora O^B_K = Ann(u) per K ≥ K\*(B); in particolare gcd(N_{B,K}) = G_u := gcd Ann(u) da quel passo in poi.
5. **(Uscite distinte, uniformi in u.)** Per K ≥ 1, m\*(K) ≤ K è finito, non decrescente in K, e a m\* fissato il grado di O_K è non decrescente e determina O_K. Nel caso 1 (in particolare nel caso 2, d = deg P) la successione (O_K)_{K≥1} assume al più (d+1)(d+2)/2 valori distinti e cambia valore al più (d+1)(d+2)/2 − 1 volte, **per ogni u**.
6. **(Tempo non uniforme.)** Per ogni N ≥ 0 la funzione u(t,x) = 1 + x^{N+2}e^{x²} (p₀ = 0) ha Ann(u) = (τ), d = 1 e K\* = N + 2; per K ≤ N + 1 l'uscita è O_K = 1 ≠ τ. Quindi K\* non è limitato da nessuna funzione di d.
7. **(Nessun certificato corretto; n = 2.)** Sia Ω ⊂ ℝ² connesso. Non esistono K e una funzione c dei jet di ordine K a valori in {0, 1} tali che: c(j_K u) = 1 implica Ann(u) = (O_K) per ogni u analitica, e c(j_K u) = 1 per almeno una u con Ann(u) principale e non banale.
**Prova.**
1. Per m < d, Ann(u) ∩ R_{≤m} = 0, quindi N_{m,K} = 0 per K ≥ K\*(m) (CONV-L1(c)); per m = d e K ≥ K\*(d), N_{d,K} = Ann(u) ∩ R_{≤d} ≠ 0. Dunque m\*(K) = d e O_K = gcd(Ann(u) ∩ R_{≤d}) per K ≥ K\*.
2. Se Ann(u) = (P), ogni elemento non nullo di Ann ha grado ≥ deg P, quindi d = deg P e Ann(u) ∩ R_{≤d} = ℂP; il gcd è P.
3. Fissato m, per K ≥ max_{m′≤m} K\*(m′) si ha N_{m′,K} = Ann(u) ∩ R_{≤m′} = 0 per ogni m′ ≤ m, quindi m\*(K) > m.
4. CONV-L1(c) con m = B: N_{B,K} = Ann(u) ∩ R_{≤B}, che genera Ann(u) per ipotesi; il gcd di un insieme di generatori di un ideale di un UFD è il gcd dell'ideale.
5. Per K ≥ 1: R_{≤K} ha dimensione binom(K+n, n) ≥ 3 e N_{K,K} è definito da una sola equazione lineare (β = 0), quindi N_{K,K} ≠ 0 e m\*(K) ≤ K. Se N_{m,K} = 0 allora N_{m,K+1} = 0 (CONV-L1(a)): perciò m\*(K+1) ≥ m\*(K). A m\* = m fissato, N_{m,K+1} ⊆ N_{m,K}, e il gcd di un sottospazio contenuto in un altro è un multiplo del gcd di quest'ultimo: deg O_K è non decrescente e, a grado uguale, O_{K+1} e O_K sono associati, cioè uguali dopo la normalizzazione. Dunque O_K è funzione della coppia (m\*(K), deg O_K), e questa coppia è non decrescente nell'ordine lessicografico. Nel caso 1, m\*(K) ≤ d per ogni K (la successione è non decrescente e vale d da K\* in poi) e 0 ≤ deg O_K ≤ m\*(K). Le coppie (m, e) con 0 ≤ e ≤ m ≤ d sono Σ_{m=0}^{d}(m+1) = (d+1)(d+2)/2; una successione non decrescente le visita ciascuna al più su un intervallo di indici, da cui il conteggio dei valori e dei cambi.
6. Scriviamo f(x) := 1 + x^{N+2}e^{x²}. *Ann(u) = (τ).* τ annulla u. Se Q ∈ Ann(u), scriviamo Q = τQ₁ + q(ξ) con q(ξ) := Q(0, ξ); allora q(∂_x)f = 0 su un intervallo. Se q ≠ 0, f è soluzione di un'ODE lineare a coefficienti costanti su un intervallo, quindi (analiticità) su ℝ è un esponenziale-polinomio, e |f(x)| ≤ C(1+|x|)^M e^{A|x|} su ℝ: falso per la crescita e^{x²}. Quindi q = 0 e τ | Q. *Calcolo di K\*.* m = 0: R_{≤0} ∖ Ann = costanti non nulle, ord(c·u) = 0 perché u(0) = 1: ν_0 = 0, K\*(0) = 0. m = 1: Q = a + bτ + cξ ∉ Ann ⟺ (a, c) ≠ (0, 0); Qu = a f + c f′. Se a ≠ 0, ord = 0; se a = 0 e c ≠ 0, ord(f′) = N + 1, perché f′ = (N+2)x^{N+1} + 2x^{N+3} + …. Quindi ν_1 = N+1, K\*(1) = N+2 = K\*. Per 1 ≤ K ≤ N+1 si ha N_{0,K} = 0, ξ ∈ N_{1,K} e τ ∈ N_{1,K}, quindi O_K | gcd(τ, ξ) = 1, cioè O_K = 1. (SymPy: `conv_t1_t2.out`, N = 2, 3, 4.)
7. Sia per assurdo c come nell'enunciato e u con Ann(u) = (P), P non costante, c(j_K u) = 1. Per C3-P1[M2] (DIMOSTRATO: nessun jet finito in un punto certifica Ann(u) = (P)) esiste u′ analitica su Ω con j_K u′ = j_K u e Ann(u′) ≠ (P). La regola L\* al passo K usa solo j_K, quindi O_K(u′) = O_K(u); poiché c(j_K u) = 1, Ann(u) = (O_K(u)) e quindi O_K(u) = P. Ma c(j_K u′) = c(j_K u) = 1 impone Ann(u′) = (O_K(u′)) = (P): contraddizione. ∎
**Nota (velocità nella classe EP).** Per u EP con d_u = dim R·u, C3-T3 dà una soglia di jet esplicita 2d_u − 1: è il solo caso con K\* noto a priori; fuori da EP il punto 6 mostra che una soglia uniforme in d non esiste.
**Nota (Ann non principale, senza maggiorante).** L\* converge a g_d, che può essere un multiplo proprio di G_u (es. Ann = G·(τ, ξ²) ⇒ g_d = Gτ). Resta APERTO se G_u sia identificabile nel limite senza maggiorante (CONV-Q1).
**Nota (dimensione).** L1 e T1(1)–(6) valgono per ogni n ≥ 2 con la stessa prova (si usano solo dim R_{≤m} < ∞, analiticità, UFD). T1(7) è enunciato per n = 2 perché C3-P1[M2] è nel LEDGER per Ω ⊂ ℝ².

