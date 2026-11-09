# KA input — OPF5D-T3 + L6 (KdV: senza riflessione ⇒ operatore d'intreccio via Liouville ⇒ Novikov; uguaglianza dell'ambiguità)
Estratto verbatim da work/OP-F5D/PROOF_PACKAGE.md §0.4, §1 (solo enunciato T1), §3 (L3–L8, T3) e da work/OP-NL/PROOF_PACKAGE.md (enunciati di OP-L16, OP-P17). Bersaglio: L3, L4, L5, L6, L7, L8, T3.

## Convenzioni
KdV del progetto: L = −∂² − v, K_0 = −v′, K_{n+1} = 𝓡K_n, 𝓡 = ∂² + 4v + 2v′∂^{−1} (antiderivata polinomiale differenziale senza termine costante), K_1 = −(v‴ + 6vv′); K_d := Σd_nK_n, q_d(λ) := Σd_nλ^n. NLS focusing: U = [[−iζ, q],[r, iζ]], r = −q̄, flussi T_0 = iq, T_1 = q_x, T_2 = i(q_xx + 2|q|²q), T_3 = −(q_xxx + 6|q|²q_x). Trasposta formale: (Σa_j∂^j)^T := Σ(−∂)^j∘a_j (senza coniugio).

## Fatti importati (NON da auditare; enunciati soltanto)
- OPF5D-T1 (enunciato):
*Enunciato.* Nell'anello 𝒜 dei polinomi differenziali in v (coefficienti razionali) esistono f_0 = 1, f_1 = −v/2, f_2, … ∈ 𝒜 tali che, posto
B_n := (−1)^n Σ_{j=0}^n (f_j∂ − ½f_j′) L^{n−j},
(a) [B_n, L] = (−1)^n·2f′_{n+1} (operatore di moltiplicazione) per ogni n ≥ 0;
(b) K_n = 2(−4)^n f′_{n+1}, cioè a_n := 2(−4)^n f_{n+1} è l'antiderivata senza termine costante di K_n e K_{n+1} = 𝓡K_n con ∂^{−1}K_n = a_n; quindi **[B_n, L] = 4^{−n}K_n[v]**;
(c) B_n = ∂^{2n+1} + Σ_{j<2n} b_{n,j}∂^j con b_{n,j} ∈ 𝒜 **senza termine costante** (nessun termine ∂^{2n}).
Quindi l'ipotesi (Lax) di OP-P17 vale per ogni n, per v liscia arbitraria (identità fra operatori).
- OP-L16 (enunciato):
*Enunciato.* v ∈ 𝒮(ℝ) (complessa ammessa), k ∈ ℂ∖0 con Im k ≥ 0. Esiste un'unica soluzione ψ_+(k,·) di −ψ″ − vψ = k²ψ con e^{−ikx}ψ_+ → 1 per x → +∞, e per ogni m ≥ 0: ∂_x^mψ_+ = (ik)^me^{ikx} + o(e^{−(Im k)x}) per x → +∞. Analogamente ψ_−(k,·) ~ e^{−ikx} per x → −∞. ψ_± dipendono con continuità da k (per k reale ≠ 0).
- OP-P17 (enunciato; ora vale per ogni M grazie a T1):
*Enunciato.* Sia v ∈ 𝒮(ℝ) reale, d ∈ ℝ^{M+1} (M ≤ 3, o M qualsiasi sotto (Lax)), K_d[v] = Σd_nK_n[v] = 0. Allora: (i) q_d(−4k²) = 0 per ogni k > 0 con b(k) ≠ 0, dove ψ_−(k) = a(k)ψ_+(−k) + b(k)ψ_+(k) (cioè R(k) = b/a ≠ 0; a(k) ≠ 0 per k reale ≠ 0); (ii) q_d(4κ²) = 0 per ogni autovalore −κ² < 0 di L in L².

## Enunciati e prove da attaccare
Ipotesi comune: v ∈ 𝒮(ℝ) reale. Notazioni: ψ_±(k,x) soluzioni di Jost (OP-L16), m_±(k,x) := e^{∓ikx}ψ_±(k,x); per k ∈ ℝ∖0: ψ_−(k) = a(k)ψ_+(−k) + b(k)ψ_+(k), 2ik·a(k) = W(ψ_−(k), ψ_+(k)) =: w(k) (W(f,g) = fg′ − f′g), T := 1/a, R := b/a. Λ(v) := {4κ_j²} ∪ {−4k² : k > 0, R(k) ≠ 0} (−κ_j² autovalori L² di L). 𝒩(v) := {d ∈ ℝ^{M+1} : K_d[v] ≡ 0}.

### [OPF5D-L3] Jost C¹ fino a k = 0 (Schwartz) — PROVA SCRITTA
(i) Per ogni x fissato, k ↦ m_±(k,x) è continua e limitata sul semipiano chiuso Im k ≥ 0 (incluso k = 0), analitica all'interno; |m_+(k,x)| ≤ exp((1+|x|)∫(1+|y|)|v|). (ii) k ↦ m_±(k,x), ∂_xm_±(k,x) sono C¹ sul semipiano chiuso (incluso 0). (iii) m_±(k,x) → 1 per |k| → ∞ nel semipiano chiuso, |m_± − 1| ≤ e^{∫|v|/|k|} − 1.
*Prova.* m_+ = 1 + ∫_x^∞D_k(y−x)v(y)m_+(y)dy, D_k(s) = ∫_0^se^{2iks′}ds′: per Im k ≥ 0, s ≥ 0: |D_k(s)| ≤ min(s, 1/|k|), |∂_kD_k(s)| = |∫_0^s2is′e^{2iks′}ds′| ≤ s². La serie di Volterra con nucleo maggiorato da (y − x)|v(y)| ≤ (|y| + |x|)|v(y)| converge uniformemente in k (Gronwall dà (i)); derivando termine a termine in k il nucleo è maggiorato da (|y|+|x|)²|v(y)|, integrabile perché v ∈ 𝒮: la serie derivata converge uniformemente, quindi (ii) per m_+; ∂_xm_+ = −∫_x^∞e^{2ik(y−x)}v m_+dy si tratta allo stesso modo. (iii) dalla maggiorazione 1/|k|. Simmetrico per m_−. ∎

### [OPF5D-L4] Zeri di a: immaginari puri e semplici — PROVA SCRITTA
a è analitica in Im k > 0, continua fino a ℝ∖0, a(k) → 1 per |k| → ∞ (Im k ≥ 0); |a|² = 1 + |b|² ≥ 1 su ℝ∖0. Gli zeri di a in Im k > 0 sono esattamente i iκ_j (−κ_j² autovalori), e sono **semplici**.
*Prova.* a → 1: w = 2ik m_−m_+ + m_−∂_xm_+ − ∂_xm_−·m_+ in x = 0 (con ∂_xm_± = O(1) uniformemente) dà a = m_−(k,0)m_+(k,0) + O(1/|k|) → 1 per L3(iii). |a|² − |b|² = 1: Wronskiano di ψ_− e ψ̄_− per v reale. Zeri: a(k_0) = 0 ⟺ ψ_−(k_0) ∥ ψ_+(k_0) ∈ L² (decadono esponenzialmente ai due estremi) ⟺ k_0² autovalore L², necessariamente reale negativo (L autoaggiunto), quindi k_0 = iκ. Semplicità: a k_0 = iκ, ψ_− = γψ_+ con γ ∈ ℝ∖0 e ψ_+(iκ,·) reale (equazione di Volterra reale). Con ψ̇ := ∂_kψ (che soddisfa −ψ̇″ − vψ̇ = k²ψ̇ + 2kψ): (W(ψ_−, ψ̇_+))′ = −2kψ_−ψ_+ e (W(ψ̇_−, ψ_+))′ = 2kψ_−ψ_+; ψ̇_+ = O(|x|e^{−κx}) a +∞ (stime di Cauchy in k di m_+, uniformi in x ≥ x_0) e ψ_− decade a +∞, quindi W(ψ_−, ψ̇_+)(x) = ∫_x^∞2k_0ψ_−ψ_+; analogamente W(ψ̇_−, ψ_+)(x) = ∫_{−∞}^x2k_0ψ_−ψ_+. Sommando: w′(k_0) = 2k_0γ∫_ℝψ_+² ≠ 0, e w′(k_0) = 2ik_0a′(k_0), quindi a′(iκ) ≠ 0. ∎

### [OPF5D-L5] Fattorizzazione di Blaschke e controllo in k = 0 — PROVA SCRITTA
Se gli autovalori sono in numero finito N, posto 𝔅(k) := Π_j(k − iκ_j)/(k + iκ_j): (i) T = 1/a è continua sul semipiano chiuso privato dei iκ_j, **incluso k = 0**; (ii) |𝔅(k)T(k)| ≤ 1 per Im k ≥ 0.
*Prova.* (i) Lontano da 0: L4. Vicino a 0: w(k) = 2ik a(k) è C¹ sul semipiano chiuso vicino a 0 (L3(ii) in x = 0); su ℝ∖0 |w(k)| = 2|k||a| ≥ 2|k|. Se w(0) ≠ 0, |w| ≥ |w(0)|/2 vicino a 0; se w(0) = 0, |w′(0)||k| + o(|k|) = |w(k)| ≥ 2|k| sull'asse reale dà |w′(0)| ≥ 2, quindi |w(k)| ≥ |k| sul semidisco chiuso vicino a 0. In entrambi i casi T = 2ik/w è limitata e continua in 0 (T(0) = 0 o 2i/w′(0)). (ii) 𝔅T è analitica in Im k > 0 (i poli semplici di T, L4, sono cancellati), continua sulla chiusura (i), |𝔅T| = |T| ≤ 1 su ℝ, 𝔅T → 1 all'infinito (L4): principio del massimo sui semidischi grandi. ∎

### [OPF5D-L6] Senza riflessione ⇒ operatore d'intreccio (Liouville) — PROVA SCRITTA
Se b ≡ 0 su ℝ∖0 e gli autovalori sono N < ∞, allora per ogni x la funzione Ψ(k,x) := Π_j(k + iκ_j)·m_+(k,x) è un **polinomio monico di grado N in k**: Ψ = Σ_{l=0}^Np_l(x)k^l, p_N = 1, p_l ∈ C^∞(ℝ). Con A := Σ_lp_l(x)(−i∂)^l (ordine N): Ae^{ikx} = Π_j(k + iκ_j)ψ_+(k,x) e **LA = AL_0**, L_0 := −∂².
*Prova.* Per Im k ≤ 0 pongo Ψ(k,x) := Π_j(k + iκ_j)·m_−(−k,x)·T(−k). Su ℝ∖0: ψ_−(−k) = a(−k)ψ_+(k) (b = 0), cioè m_−(−k,x)T(−k) = m_+(k,x): le due definizioni coincidono. Ψ è analitica in ℂ∖ℝ tranne forse in −iκ_j, dove T(−k) ha poli semplici (L4) cancellati dal fattore k + iκ_j; è continua attraverso ℝ, incluso k = 0 (L3(i), L5(i)). Per Morera Ψ(·,x) è intera. Crescita: per Im k ≥ 0, |Ψ| ≤ C_xΠ(|k| + κ_j) (L3(i)); per Im k ≤ 0, con κ := −k: Π_j(k + iκ_j)T(κ) = Π_j(k + iκ_j)·(𝔅T)(κ)/𝔅(κ), e |Π_j(k + iκ_j)/𝔅(−k)| = Π_j|k − iκ_j|, quindi |Ψ| ≤ C_xΠ(|k| + κ_j) per L5(ii). Liouville: Ψ(·,x) è un polinomio di grado ≤ N; Ψ/k^N → 1 lungo iℝ_+ (L3(iii)): monico. I p_l sono combinazioni lineari fisse di Ψ(k_0..k_N, x) (interpolazione di Lagrange), quindi C^∞. Infine (LA − AL_0)e^{ikx} = L(Π(k + iκ_j)ψ_+) − k²Ae^{ikx} = 0 per ogni k reale ≠ 0; un operatore differenziale Σe_l(x)∂^l che annulla tutti gli e^{ikx} ha Σe_l(x)(ik)^l ≡ 0, quindi e_l = 0. N = 0: Ψ = m_+ ≡ 1, ψ_+ = e^{ikx}, v ≡ 0. ∎

### [OPF5D-L7] Lemma del centralizzatore — PROVA SCRITTA
Sia X un operatore differenziale a coefficienti lisci (complessi) d'ordine m tale che [X, L] sia un operatore di moltiplicazione. Allora X = Σ_{2n+1≤m}α_nB_n + Σ_{2l≤m}β_lL^l con α_n, β_l costanti.
*Prova.* X = Σ_{j≤m}x_j∂^j. Il termine d'ordine m+1 di [X, L] è 2x_m′∂^{m+1} (da [x_j∂^j, −∂²] = 2x_j′∂^{j+1} + x_j″∂^j; [x_j∂^j, −v] ha ordine ≤ j−1); poiché m+1 ≥ 1, x_m′ = 0. Se m = 2n+1, X − x_mB_n ha ordine ≤ 2n e [X − x_mB_n, L] = [X,L] − x_m4^{−n}K_n è ancora di moltiplicazione (T1); se m = 2l, X − x_m(−1)^lL^l, idem. Induzione discendente fino all'ordine 0: x_0 con [x_0, L] = x_0″ + 2x_0′∂ di moltiplicazione ⇒ x_0′ = 0. ∎

### [OPF5D-L8] Chiusura per moltiplicazione per λ — PROVA SCRITTA
Se v ∈ 𝒮 e K_d[v] = 0, allora K_{d^+}[v] = 0 dove q_{d^+} = λq_d (d^+_{n+1} = d_n). Quindi {q_d : K_d[v] = 0} ∪ {0} è (la parte di grado ≤ M di) un ideale di ℝ[λ].
*Prova.* K_{n+1} = K_n″ + 4vK_n + 2v′a_n (T1(b)), quindi K_{d^+} = (K_d)″ + 4vK_d + 2v′Σd_na_n = 2v′Σd_na_n. Σd_na_n′ = K_d = 0 ⇒ Σd_na_n costante; a_n ∈ 𝒜 senza termine costante e v ∈ 𝒮 ⇒ Σd_na_n → 0 per x → +∞; quindi = 0. ∎

### [OPF5D-T3] Uguaglianza dell'ambiguità a tempo fissato — PROVA SCRITTA
*Enunciato.* Per ogni v ∈ 𝒮(ℝ) reale e ogni M: **𝒩(v) = {d ∈ ℝ^{M+1} : q_d|_{Λ(v)} = 0}**. In particolare: se R ≢ 0, 𝒩(v) = {0} per ogni M; se R ≡ 0 con autovalori −κ_1², …, −κ_N², vale l'equazione stazionaria di Novikov K_{d*}[v] = 0 con q_{d*} = Π_j(λ − 4κ_j²), e 𝒩(v) = {d : Π_j(λ − 4κ_j²) | q_d}.
*Prova.* ⊆: OP-P17 (ora senza condizioni, T1). ⊇: se Λ è infinito il membro destro è {0}. R è continuo su (0,∞) (OP-L16), quindi Λ finito ⟹ R ≡ 0, cioè b ≡ 0, e N < ∞. L6 dà A con LA = AL_0. P := A∂A^T: dalla trasposta di LA = AL_0, A^TL = L_0A^T (L, L_0 simmetrici per la trasposta), quindi LP = AL_0∂A^T = A∂L_0A^T = A∂A^TL = PL. A = (−i)^N∂^N + …, A^T = (−1)^N(−i)^N∂^N + …, quindi P = ∂^{2N+1} + … . L7: P = Σ_{n≤N}α_nB_n + Σβ_lL^l, α_N = 1, e 0 = [P, L] = Σα_n4^{−n}K_n[v]. Parte reale (K_n[v] reali): d*_n := 4^{−n}Re α_n, d*_N = 4^{−N}, K_{d*}[v] = 0. Per OP-P17(ii) q_{d*}(4κ_j²) = 0 per ogni j: q_{d*} ha grado N e N radici distinte, q_{d*} = 4^{−N}Π(λ − 4κ_j²). Per L8 ogni d con Π(λ − 4κ_j²) | q_d sta in 𝒩(v). Per N = 0, v ≡ 0 e 𝒩 = ℝ^{M+1}. ∎
*Nota.* Non si usano: formula di Kay–Moses, Marchenko/GLM, F-MS, la forma esplicita dei multi-solitoni.
