# KA input — OP-T1 (relazione autonoma ⇒ analiticità su un sottointervallo; dato mai analitico ⇒ J_u = 0) + OP-E3, OP-C3′
Estratto verbatim da work/OP-NL/CHECK_REQUEST.md (quadro, fatti importati) e da work/OP-NL/PROOF_PACKAGE.md §1 (OP-T1, OP-E3, OP-C3′). Bersaglio: OP-T1 (a)(b)(c) e il suo uso per rispondere a INT-Q1 per la classe di OP-C3′.

## Quadro minimo
- A = ℂ[y_0, y_1, …] (y_j = ∂_x^jy), D: y_j ↦ y_{j+1}. Per u liscia su Ω: J_u = {p ∈ A : p(u, u_x, …) ≡ 0 su Ω}. A_{≤d,≤K}: grado ≤ d in y_0..y_K; A_{≤d}: grado ≤ d, ordine qualsiasi.
- Equazione di evoluzione F = y_t − N; S4ID-T1 (DIMOSTRATO): u identifica F modulo le conseguenze nel dizionario V ⟺ J_u ∩ ψ(V) = 0; nel dizionario evolutivo ℂy_t ⊕ M (N ∈ M ⊂ A): identifica in senso stretto ⟺ J_u ∩ M = 0 (S4ID-C1).
- KdV u_t + 6uu_x + u_xxx = 0, L = −∂² − u, gerarchia K_0 = −u_x, K_{n+1} = (∂² + 4u + 2u_x∂^{−1})K_n; 𝓗_M = {u_t = Σ_{n≤M}c_nK_n}; q_d(λ) = Σd_nλ^n.

## Fatti importati (NON da auditare; stato del loro autore)
- S4ID-T2 (DIMOSTRATO, S-CHECK-10), in particolare dalla sua prova: (I) per gli N-shock non risonanti, p ∈ J_u ⟺ p(u, Du, …) = 0 nel campo ℂ(X_1..X_N), DX_i = k_iX_i, u = −2νDφ/φ, φ = 1 + ΣX_i; (II) r_j := D^jφ/φ = Σ_ik_i^jX_i/φ, con r_1..r_N algebricamente indipendenti; R_N ∈ J_u di grado N+1.
- S4ID-T3(a)(b) (DIMOSTRATO), S4ID-C1, C2 (DIMOSTRATO / CON-FONTE), S4ID-T4(i) (DIMOSTRATO), S4ID-P8 (CONDIZIONALE, logica PASS).
- INT-T1(A), UC-ω, Lemma B1 (DIMOSTRATO, S-CHECK-9).
- CON-FONTE dichiarate (da CIT-AUDIT, non da auditare): funzione implicita reale-analitica (Krantz–Parks); analiticità delle soluzioni di ODE analitiche (Cauchy–Kovalevskaya, già verificata da CIT-AUDIT-5); (WP) buona posizione di KdV in 𝒮; asintotica di Airy (DLMF 9.7); (Lax) per n ≥ 4, (ZC) per n ≥ 4; teorema fondamentale dei polinomi simmetrici.

## Domanda INT-Q1 (dal package)
**Domanda (F4-INT INT-P4 / S4ID §6).** KdV, u(t,·) ∈ 𝒮(ℝ) per ogni t, coefficiente di riflessione r ≢ 0: può esistere p ∈ A∖0 con p(u(t,·)) ≡ 0 su ℝ per ogni t (cioè J_u ≠ 0)?

## Fatto importato aggiuntivo (DIMOSTRATO): S4ID-T1(c): I(u)∩V = [F]∩V ⟺ J_u∩ψ(V) = 0 (per ogni dizionario V, u ∈ C^∞(Ω), Ω aperto); ALG-T1(b): J_u = 0 ⇒ I(u) = [F].

### [OP-T1] Una relazione autonoma forza l'analiticità — PROVA SCRITTA
*Ipotesi.* I ⊂ ℝ intervallo aperto, g ∈ C^∞(I) a valori **reali**, J_g(I) := {p ∈ A : p(g, g′, g″, …) ≡ 0 su I}.
*Tesi.* (a) Se J_g(I) ≠ 0, esiste un sottointervallo aperto non vuoto I′ ⊂ I su cui g è reale-analitica. (b) Quindi, se g non è reale-analitica su nessun sottointervallo aperto di I ("g mai analitica su I"), J_g(I) = 0. (c) (Per un'equazione di evoluzione F = y_t − N qualsiasi.) Sia Ω ⊇ (t₀−ε, t₀+ε) × I, oppure u ∈ C^∞([t₀, t₀+ε) × I) e Ω ⊇ (t₀, t₀+ε) × I, con u soluzione C^∞ su Ω. Se u(t₀,·) è mai analitica su I, allora J_u = 0; quindi (S4ID-T1(c), ALG-T1(b)) I(u) = [F] e u identifica F modulo le conseguenze in **ogni** dizionario V.
*Triage.* PROVABLE AS STATED. *Strategia.* Relazione reale minimale → separante non nullo → funzione implicita analitica → ODE analitica → analiticità della soluzione.
*Dipendenze.* (IFT-ω) teorema della funzione implicita reale-analitico (Krantz–Parks, *A Primer of Real Analytic Functions*, 2ª ed., Thm 2.3.5: CON-FONTE, numero da verificare); (ODE-ω) se F è reale-analitica vicino a η₀, l'unica soluzione C¹ di Y′ = F(Y), Y(x₀) = η₀ è reale-analitica vicino a x₀ (Cauchy–Kovalevskaya per ODE: la soluzione analitica esiste per maggioranti; l'unicità C¹ è Picard–Lindelöf perché F è localmente lipschitziana; CON-FONTE verificata da CIT-AUDIT-5 come "Cauchy–Kovalevskaya, Driver Thm 4.7").
*Prova.*
1. *Relazione reale.* Sia p ∈ J_g(I)∖0, p = p_R + ip_I con p_R, p_I ∈ ℝ[y]. Poiché g è reale, p_R(g-getto) = Re p(g-getto) = 0 e p_I(g-getto) = 0; uno dei due è ≠ 0. Dunque J^ℝ := J_g(I) ∩ ℝ[y] ≠ 0.
2. *Scelta minimale.* Per q ∈ ℝ[y] non costante sia ord q il massimo j con y_j presente. Una costante non nulla non sta in J^ℝ. Scelgo q ∈ J^ℝ∖0 con ord q =: K minimo e, fra questi, con grado m ≥ 1 in y_K minimo.
3. *K = 0.* q ∈ ℝ[y_0] ha grado ≥ 1, quindi un numero finito di zeri; g(I) è contenuto in essi ed è connesso: g è costante su I, quindi analitica.
4. *K ≥ 1: il separante.* s := ∂q/∂y_K ≠ 0. Se m ≥ 2, s ha ordine K e grado m−1 < m in y_K; se m = 1, s ∈ ℝ[y_0..y_{K−1}]∖0, quindi è una costante non nulla oppure ha ordine < K. In ogni caso, per la minimalità, s ∉ J^ℝ: la funzione continua x ↦ s(g(x), …, g^{(K)}(x)) non è identicamente nulla, ed esiste x₀ ∈ I con s(ξ₀) ≠ 0, ξ₀ := (g, …, g^{(K)})(x₀).
5. *Funzione implicita.* q è un polinomio, q(ξ₀) = 0 (step 2), ∂q/∂y_K(ξ₀) ≠ 0. Per (IFT-ω) esistono intorni U di η₀ := (ξ₀_0..ξ₀_{K−1}) in ℝ^K e W di ξ₀_K in ℝ e φ: U → W reale-analitica con {(η, ζ) ∈ U × W : q(η, ζ) = 0} = grafico di φ. Per continuità del getto esiste δ > 0 con (g, …, g^{(K−1)})(x) ∈ U e g^{(K)}(x) ∈ W per |x − x₀| < δ; poiché q(getto) = 0, g^{(K)} = φ(g, …, g^{(K−1)}) su (x₀−δ, x₀+δ).
6. *ODE analitica.* Y := (g, …, g^{(K−1)}) è C¹ e risolve Y′ = F(Y), F(η) := (η_1, …, η_{K−1}, φ(η)), F reale-analitica su U. Per (ODE-ω) Y è reale-analitica vicino a x₀, quindi lo è la sua prima componente g. Questo prova (a); (b) è la contronominale.
7. *(c).* Se p ∈ J_u, p(u-getto) = 0 su Ω e, per continuità del getto in t (nel secondo caso), anche sulla fetta t = t₀: p ∈ J_{u(t₀,·)}(I) = 0 per (b). ∎
*Osservazioni.* (1) Il teorema non usa la struttura di KdV né r: è un'ostruzione di **regolarità**, non dispersiva. (2) Rafforza S4ID-T4(iii): l'ipotesi "g differenzialmente trascendente" è sostituita da "g mai analitica" (più debole: per (b) mai analitica ⇒ differenzialmente trascendente su ogni sottointervallo) e generica. (3) Per equazioni con effetto regolarizzante (Burgers con ν > 0; KdV con dati a decadimento esponenziale, dove u(t) è analitica per t ≠ 0 — fatto noto, non usato) la fetta non analitica può essere solo quella iniziale: (c) va letto con la relazione richiesta **anche** in t₀ (come nella formulazione di INT-Q1: "per ogni t"). Per la variante "per ogni t ≥ T₀" con T₀ > t₀ il teorema non dice nulla.

### [OP-E3] Un dato di Schwartz mai analitico — PROVA SCRITTA (elementare)
*Enunciato.* F(x) := Σ_{k≥0} e^{−2^{k/2}} cos(2^kx) è C^∞ con tutte le derivate limitate e non è analitica su nessun intervallo aperto; g := e^{−x²}F ∈ 𝒮(ℝ) è reale e mai analitica su ℝ.
*Prova.* (i) Σ_k e^{−2^{k/2}}2^{kn} < ∞ per ogni n (e^{−2^{k/2}} decresce più in fretta di ogni potenza di 2^k): derivazione termine a termine, F ∈ C^∞, ‖F^{(n)}‖_∞ < ∞.
(ii) Sia x* = 2πp/2^q (p ∈ ℤ, q ≥ 0): per k ≥ q, cos(2^kx*) = 1. Per n = 4m, F^{(4m)}(x*) = Σ_k e^{−2^{k/2}}2^{4mk}cos(2^kx*) ≥ e^{−2^{k_m/2}}2^{4mk_m} − Σ_{k<q}2^{4mk}, dove k_m è l'unico intero con 2^{k_m/2} ∈ [8m, 8√2m) (l'intervallo ha rapporto √2, passo dei valori 2^{k/2}); per m grande k_m ≥ q. Allora e^{−2^{k_m/2}}(2^{k_m/2})^{8m} ≥ e^{−8√2m}(8m)^{8m}, mentre Σ_{k<q}2^{4mk} ≤ q2^{4mq}; quindi F^{(4m)}(x*) ≥ ½e^{−8√2m}(8m)^{8m} per m ≥ m₀.
(iii) Se F fosse analitica vicino a x*, varrebbero le stime di Cauchy |F^{(n)}(x*)| ≤ Cn!ρ^{−n} per qualche C, ρ > 0. Ma con (4m)! ≤ (4m)^{4m}: ½e^{−8√2m}(8m)^{8m}ρ^{4m}/(4m)! ≥ ½(16mρe^{−2√2})^{4m} → ∞. Contraddizione: F non è analitica in nessun x* della forma detta; questi punti sono densi, quindi F non è analitica su nessun intervallo aperto.
(iv) g ∈ 𝒮: le derivate di e^{−x²} sono polinomi per e^{−x²}, quelle di F sono limitate (Leibniz). Se g fosse analitica su un intervallo, lo sarebbe F = e^{x²}g. ∎

### [OP-C3′] Risposta a INT-Q1 per una classe esplicita — PROVA SCRITTA mod (WP)
*Ipotesi (WP), CON-FONTE.* Per ogni g ∈ 𝒮(ℝ) reale esiste un'unica soluzione u ∈ C^∞(ℝ × ℝ) di KdV con u(0,·) = g e u(t,·) ∈ 𝒮 per ogni t (Bona–Smith, Phil. Trans. R. Soc. A 278 (1975) 555–601 per H^s; persistenza del decadimento: Kato 1983; esistenza e unicità per dati rapidamente decrescenti via IST: Gardner–Greene–Kruskal–Miura e Marchenko §4.2, **citati come tali in Grunert–Teschl 2009 §1–2, letto**).
*Tesi.* Per ogni g ∈ 𝒮 reale mai analitica su un intervallo (p.es. OP-E3) la soluzione u di (WP) ha J_u = 0: nessuna ODE autonoma polinomiale è soddisfatta da u(t,·) per ogni t. Inoltre r ≢ 0 (se r ≡ 0, u(0,·) sarebbe un multi-solitone, Kay–Moses = F4, quindi analitica; CON-FONTE, non usato dalla tesi principale).
*Prova.* OP-T1(c) con t₀ = 0, I = ℝ. ∎
*Portata.* La classe {g ∈ 𝒮 : g mai analitica su qualche intervallo} è densa in 𝒮 (somma di g ∈ 𝒮 e εe^{−x²}F — fatto elementare non usato). Il risultato **non** usa il meccanismo dispersivo: non risponde per dati analitici (p.es. a decadimento esponenziale, il caso "generico" della letteratura IST).
