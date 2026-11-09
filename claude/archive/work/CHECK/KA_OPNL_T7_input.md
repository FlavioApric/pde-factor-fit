# KA input — OP-T7 (S4ID-K1: N-shock di Burgers senza relazioni autonome di grado ≤ N) + OP-C11
Estratto verbatim da work/OP-NL/CHECK_REQUEST.md (quadro, fatti importati) e da work/OP-NL/PROOF_PACKAGE.md §2. Bersaglio: OP-T7 (con OP-L8, L9, L10) e il corollario OP-C11.

## Quadro minimo
- A = ℂ[y_0, y_1, …] (y_j = ∂_x^jy), D: y_j ↦ y_{j+1}. Per u liscia su Ω: J_u = {p ∈ A : p(u, u_x, …) ≡ 0 su Ω}. A_{≤d,≤K}: grado ≤ d in y_0..y_K; A_{≤d}: grado ≤ d, ordine qualsiasi.
- Equazione di evoluzione F = y_t − N; S4ID-T1 (DIMOSTRATO): u identifica F modulo le conseguenze nel dizionario V ⟺ J_u ∩ ψ(V) = 0; nel dizionario evolutivo ℂy_t ⊕ M (N ∈ M ⊂ A): identifica in senso stretto ⟺ J_u ∩ M = 0 (S4ID-C1).
- KdV u_t + 6uu_x + u_xxx = 0, L = −∂² − u, gerarchia K_0 = −u_x, K_{n+1} = (∂² + 4u + 2u_x∂^{−1})K_n; 𝓗_M = {u_t = Σ_{n≤M}c_nK_n}; q_d(λ) = Σd_nλ^n.

## Fatti importati (NON da auditare; stato del loro autore)
- S4ID-T2 (DIMOSTRATO, S-CHECK-10), in particolare dalla sua prova: (I) per gli N-shock non risonanti, p ∈ J_u ⟺ p(u, Du, …) = 0 nel campo ℂ(X_1..X_N), DX_i = k_iX_i, u = −2νDφ/φ, φ = 1 + ΣX_i; (II) r_j := D^jφ/φ = Σ_ik_i^jX_i/φ, con r_1..r_N algebricamente indipendenti; R_N ∈ J_u di grado N+1.
- S4ID-T3(a)(b) (DIMOSTRATO), S4ID-C1, C2 (DIMOSTRATO / CON-FONTE), S4ID-T4(i) (DIMOSTRATO), S4ID-P8 (CONDIZIONALE, logica PASS).
- INT-T1(A), UC-ω, Lemma B1 (DIMOSTRATO, S-CHECK-9).
- CON-FONTE dichiarate (da CIT-AUDIT, non da auditare): funzione implicita reale-analitica (Krantz–Parks); analiticità delle soluzioni di ODE analitiche (Cauchy–Kovalevskaya, già verificata da CIT-AUDIT-5); (WP) buona posizione di KdV in 𝒮; asintotica di Airy (DLMF 9.7); (Lax) per n ≥ 4, (ZC) per n ≥ 4; teorema fondamentale dei polinomi simmetrici.

## Fatto importato aggiuntivo (DIMOSTRATO): S4ID-C1(i): nel dizionario evolutivo ℂy_t ⊕ M (N ∈ M ⊂ A), u identifica in senso stretto ⟺ J_u ∩ M = 0. S4ID-C2: A_{≤d,≤k} ⊆ ψ(V_{d,k}) ⊆ A_{≤d(1+k(δ−1)),≤nk} (n = ordine, δ = grado di N; per Burgers n = δ = 2). S4ID-T2(a): nessuna relazione d'ordine ≤ N−1; (b) R_N ∈ J_u di grado N+1 e ordine N; (d) se k ≥ N e d ≥ N+1 non identifica in V_{d,k}.

## 2. S4ID-K1 (Burgers, N-shock)
*Quadro (S4ID-T2).* F_B = y_t + y_0y_1 − νy_2, ν ≠ 0; k_1, …, k_N ∈ ℂ∖0 distinti, non risonanti (NR); φ = 1 + ΣE_i; u = −2νφ_x/φ. Dalla prova di S4ID-T2 (DIMOSTRATO, S-CHECK-10): (I) p ∈ J_u ⟺ p(u, Du, …) = 0 nel campo ℂ(X_1..X_N) con DX_i = k_iX_i; (II) w := Dφ/φ, u = −2νw, r_j := D^jφ/φ = Σ_ik_i^jp_i (p_i = X_i/φ), e **r_1, …, r_N sono algebricamente indipendenti** (T2(a), prova); per j > N, r_j = ℓ_j(r_1..r_N) := Σ_{l=1}^N L_{jl}r_l con (L_{jl}) = (k_i^j)_i·V^{−1}, V = (k_i^l)_{l,i}: forme **lineari** senza termine noto.

### [OP-L8] Cumulanti — PROVA SCRITTA
*Enunciato.* In un anello differenziale (𝒦, D) con φ invertibile, siano r_0 = 1, r_j := D^jφ/φ e κ_n := D^{n−1}(Dφ/φ) (n ≥ 1). Allora r_{m+1} = Σ_{n=0}^m C(m,n)κ_{n+1}r_{m−n} (m ≥ 0), quindi κ_n = r_n − Σ_{m=1}^{n−1}C(n−1, m−1)κ_mr_{n−m}, e, come serie formali, Σ_{n≥1}κ_ns^n/n! = log(Σ_{j≥0}r_js^j/j!).
*Prova.* Dφ = wφ con w = κ_1; D^m(Dφ) = D^m(wφ) = Σ_nC(m,n)(D^nw)(D^{m−n}φ); dividendo per φ si ha la prima formula; la seconda è la stessa con m = n−1 e reindicizzazione. Con M(s) := Σr_js^j/j! e G(s) := Σκ_ns^n/n! la prima formula dice M′ = G′M (coefficiente di s^m/m!); log M è l'unica serie con termine noto nullo e derivata M′/M, e G(0) = 0: G = log M. Quest'ultima parte è puramente formale: **per qualunque successione r_1, r_2, … in una ℚ-algebra commutativa**, i κ_n definiti dalla ricorrenza soddisfano Σκ_ns^n/n! = log(1 + Σr_js^j/j!) (usato in OP-T7 per i cumulanti troncati). ∎

### [OP-L9] Il peso massimo di κ_n è il cumulante troncato — PROVA SCRITTA
*Enunciato.* Graduiamo ℂ[r_1..r_N] con wt r_l = l e scriviamo g = Σ_wg^{[w]}. Siano r_j (j > N) le forme ℓ_j e κ_n i polinomi in r_1..r_N dati dalla ricorrenza di OP-L8. Siano r̃_j := r_j per j ≤ N, r̃_j := 0 per j > N, e κ̃_n i polinomi dati dalla stessa ricorrenza con r̃. Allora κ_n ha componenti solo di peso ≤ n e **κ_n^{[n]} = κ̃_n**.
*Prova.* Per j ≤ N, r_j è omogeneo di peso j = peso di r̃_j. Per j > N, r_j = ℓ_j ha componenti di peso ≤ N < j, quindi (r_j)^{[j]} = 0 = r̃_j. Induzione su n: κ_1 = r_1 = r̃_1. Per n ≥ 2, ogni prodotto κ_mr_{n−m} (1 ≤ m ≤ n−1) ha componenti di peso ≤ m + (n−m) = n e componente di peso n uguale a κ_m^{[m]}r_{n−m}^{[n−m]} = κ̃_mr̃_{n−m} (le componenti di peso < m o < n−m contribuiscono a pesi < n). Quindi κ_n^{[n]} = r̃_n − ΣC(n−1,m−1)κ̃_mr̃_{n−m} = κ̃_n. ∎

### [OP-L10] Somme di potenze di lunghezza ≤ N — PROVA SCRITTA
*Enunciato.* Siano X_1..X_N indeterminate, P_n := ΣX_i^n e, per una partizione μ = (μ_1 ≥ … ≥ μ_ℓ ≥ 1), P_μ := ΠP_{μ_i} (P_∅ = 1). Le P_μ con ℓ(μ) ≤ N (μ di qualunque peso) sono linearmente indipendenti.
*Prova.* Per una partizione λ con ℓ(λ) ≤ N sia m_λ la somma dei monomi distinti X^β con β permutazione di (λ, 0, …, 0): le m_λ hanno supporti disgiunti, quindi sono indipendenti. Sviluppando, P_μ = Σ_{f:[ℓ]→[N]}Π_aX_a^{β_a(f)} con β_a(f) := Σ_{i∈f^{−1}(a)}μ_i; le parti non nulle di β(f) formano la partizione λ(f) ottenuta **fondendo** le parti di μ lungo le fibre di f, e ℓ(λ(f)) = |im f| ≤ ℓ(μ), con uguaglianza ⟺ f iniettiva ⟺ λ(f) = μ. Quindi P_μ = c_μm_μ + Σ_{ℓ(λ)<ℓ(μ)}c_{μλ}m_λ, con c_μ = coefficiente di X_1^{μ_1}⋯X_ℓ^{μ_ℓ} ≥ 1 (contributo almeno di f = id, possibile perché ℓ ≤ N; tutti i contributi sono +1). Se Σa_μP_μ = 0 con qualche a_μ ≠ 0, sia ℓ* la lunghezza massima con a_μ ≠ 0 e μ una tale partizione: m_μ compare solo in P_μ fra le P_ν con ℓ(ν) = ℓ* (le altre danno m_ν, ν ≠ μ, o m_λ più corte) e in nessuna P_ν con ℓ(ν) < ℓ*. Il coefficiente di m_μ è a_μc_μ ≠ 0: contraddizione. ∎

### [OP-T7] **S4ID-K1 è vera** — PROVA SCRITTA
*Ipotesi.* Quelle di S4ID-T2 (ν ≠ 0, k_i ≠ 0 distinti, (NR), Ω connesso, φ ≠ 0 su Ω).
*Tesi.* **J_u ∩ A_{≤N} = 0**: nessun polinomio non nullo di grado ≤ N nel getto (di ordine qualsiasi) si annulla su u.
*Triage.* PROVABLE AS STATED. *Strategia.* Momenti (lineari nei parametri liberi) → cumulanti → grading per pesi → limite confluente (log-derivate di polinomi di grado N) → somme di potenze di N variabili.
*Mappa.* (I),(II) di S4ID-T2 → OP-L8 (getto = cumulanti) → OP-L9 (parte di peso massimo = cumulanti troncati) → identificazione con Λ_N (teorema fondamentale dei polinomi simmetrici) → OP-L10.
*Prova.*
1. *Traduzione.* Per OP-L8, D^{n−1}w = κ_n(r_1, …, r_n), e con (II) i κ_n sono polinomi in r_1..r_N (per j > N si sostituisce r_j = ℓ_j). Dato p ∈ A, sia P(z_1, z_2, …) := p(−2νz_1, −2νz_2, …) (y_{n−1} ↦ −2νz_n): deg P = deg p, e per (I) p ∈ J_u ⟺ P(κ_1, κ_2, …) = 0 in ℂ(X) ⟺ P(κ) = 0 in ℂ[r_1..r_N] (gli r_l sono elementi di ℂ(X) algebricamente indipendenti, quindi ℂ[r_1..r_N] ⊂ ℂ(X) è un anello di polinomi).
2. Sia per assurdo p ∈ J_u∖0 con deg p ≤ N; P = Σ_αc_αz^α, α multinsieme di indici ≥ 1 con |α| ≤ N, z^α := Π_{n∈α}z_n, wt α := Σ_{n∈α}n. Sia W := max{wt α : c_α ≠ 0}.
3. Per OP-L9, κ^α := Π_{n∈α}κ_n ha componenti di peso ≤ wt α, e la sua componente di peso wt α è Π_{n∈α}κ̃_n (in un dominio graduato la componente di peso massimo di un prodotto è il prodotto delle componenti di peso massimo, che qui sono κ̃_n ≠ 0 per il punto 4). Quindi 0 = P(κ)^{[W]} = Σ_{wt α = W}c_ακ̃^α.
4. *Cumulanti troncati = somme di potenze.* L'omomorfismo graduato ι: ℂ[r_1..r_N] → Λ_N := ℂ[X_1..X_N]^{S_N}, r_j ↦ j!(−1)^je_j(X), è un isomorfismo (teorema fondamentale dei polinomi simmetrici: e_1..e_N generatori algebricamente indipendenti; wt r_j = j = deg e_j). Allora ι(1 + Σ_{j≤N}r̃_js^j/j!) = Σ_j(−1)^je_js^j = Π_i(1 − X_is), e per OP-L8 ι(κ̃_n) = n![s^n]log Π_i(1 − X_is) = n![s^n](−Σ_mP_ms^m/m) = −(n−1)!P_n.
5. Quindi ι(Σ_{wt α=W}c_ακ̃^α) = Σ_{wt α=W}c_α·Π_{n∈α}(−(n−1)!)·P_{μ(α)}, dove μ(α) è α ordinato: |α| ≤ N dà ℓ(μ(α)) ≤ N, e α ↦ μ(α) è iniettiva. Per OP-L10 tutti i c_α con wt α = W sono nulli: contraddice la definizione di W. ∎
*Osservazioni.* (1) La prova non dipende dai k_i oltre (I),(II): il passaggio al peso massimo è il **limite confluente** k → 0 (shock razionali u = −2νM′/M con M polinomio di grado N, la cui log-derivata ha getto = somme di potenze dei reciproci delle radici). (2) È esatta: R_N ∈ J_u ha grado N+1 (S4ID-T2(b)). (3) Non usa la regolarità delle forme dominanti (che è falsa: le forme di grado massimo D^j(y_0^{N+1}) di D^jR_N non sono una successione regolare, e infatti dim J_u ∩ A_{≤N+1,≤K} cresce più di K−N+1: V-ex 4, 10 per N = 2, K = 3, 4).

### [OP-C11] Criterio completo per gli N-shock — PROVA SCRITTA (corollario)
*Tesi.* Con le ipotesi di OP-T7 e d ≥ 2, K ≥ 2:
(a) **Dizionario evolutivo** ℂy_t ⊕ A_{≤d,≤K}: u identifica Burgers in senso stretto ⟺ (K ≤ N−1) oppure (d ≤ N). In particolare per K ≥ N: identifica ⟺ d ≤ N (sostituisce il ramo congetturale di S4ID-T2(d)).
(b) **Dizionario completo** V_{d,k}: se d(k+1) ≤ N, u identifica Burgers modulo le conseguenze (per ogni k); se k ≥ N e d ≥ N+1, non identifica.
*Prova.* (a) S4ID-C1(i): identifica ⟺ J_u ∩ A_{≤d,≤K} = 0. Se K ≤ N−1: S4ID-T2(a). Se d ≤ N: OP-T7. Se K ≥ N e d ≥ N+1: R_N ∈ A_{≤N+1,≤N} ⊆ A_{≤d,≤K}. (b) S4ID-C2 con n = 2, δ = 2: ψ(V_{d,k}) ⊆ A_{≤d(1+k),≤2k} ⊆ A_{≤N} se d(1+k) ≤ N, e OP-T7 + S4ID-T1(c); il secondo caso è S4ID-T2(d). ∎
*Verifiche (sympy/k1_checks.py → k1_checks.out, 115/115 OK):* OP-L10 (rango esatto su ℚ, N ≤ 4, peso ≤ 8) e triangolarità; OP-L9 (parte di peso massimo = cumulante troncato, k = (1,2), (2,−1), (3,5), n ≤ 7, esatto); OP-T7 direttamente (rango pieno mod p dei monomi di grado ≤ N in κ_1..κ_{K+1}: N = 2 K ≤ 7; N = 3 K ≤ 6; N = 4 K ≤ 5; N = 5 K = 5; rango pieno mod p ⇒ indipendenza su ℚ); esistenza di relazioni di grado N+1 (INFO dimensioni 1, 4, 10 / 1, 5, 15 / 1, 6).
