# CHECK_REQUEST — OP-NL (per S-CHECK, proof-checker) · 26/10/2026
Testo da auditare: `work/OP-NL/PROOF_PACKAGE.md`. Le prove sono complete in quel file; qui: quadro minimo, fatti importati, claim con priorità, punti delicati, domande. Non serve altro contesto.

## Quadro minimo
- A = ℂ[y_0, y_1, …] (y_j = ∂_x^jy), D: y_j ↦ y_{j+1}. Per u liscia su Ω: J_u = {p ∈ A : p(u, u_x, …) ≡ 0 su Ω}. A_{≤d,≤K}: grado ≤ d in y_0..y_K; A_{≤d}: grado ≤ d, ordine qualsiasi.
- Equazione di evoluzione F = y_t − N; S4ID-T1 (DIMOSTRATO): u identifica F modulo le conseguenze nel dizionario V ⟺ J_u ∩ ψ(V) = 0; nel dizionario evolutivo ℂy_t ⊕ M (N ∈ M ⊂ A): identifica in senso stretto ⟺ J_u ∩ M = 0 (S4ID-C1).
- KdV u_t + 6uu_x + u_xxx = 0, L = −∂² − u, gerarchia K_0 = −u_x, K_{n+1} = (∂² + 4u + 2u_x∂^{−1})K_n; 𝓗_M = {u_t = Σ_{n≤M}c_nK_n}; q_d(λ) = Σd_nλ^n.

## Fatti importati (NON da auditare; stato del loro autore)
- S4ID-T2 (DIMOSTRATO, S-CHECK-10), in particolare dalla sua prova: (I) per gli N-shock non risonanti, p ∈ J_u ⟺ p(u, Du, …) = 0 nel campo ℂ(X_1..X_N), DX_i = k_iX_i, u = −2νDφ/φ, φ = 1 + ΣX_i; (II) r_j := D^jφ/φ = Σ_ik_i^jX_i/φ, con r_1..r_N algebricamente indipendenti; R_N ∈ J_u di grado N+1.
- S4ID-T3(a)(b) (DIMOSTRATO), S4ID-C1, C2 (DIMOSTRATO / CON-FONTE), S4ID-T4(i) (DIMOSTRATO), S4ID-P8 (CONDIZIONALE, logica PASS).
- INT-T1(A), UC-ω, Lemma B1 (DIMOSTRATO, S-CHECK-9).
- CON-FONTE dichiarate (da CIT-AUDIT, non da auditare): funzione implicita reale-analitica (Krantz–Parks); analiticità delle soluzioni di ODE analitiche (Cauchy–Kovalevskaya, già verificata da CIT-AUDIT-5); (WP) buona posizione di KdV in 𝒮; asintotica di Airy (DLMF 9.7); (Lax) per n ≥ 4, (ZC) per n ≥ 4; teorema fondamentale dei polinomi simmetrici.

## Claim da auditare (priorità)
| pr. | ID | enunciato (sintesi) | ipotesi | dove |
|---|---|---|---|---|
| 1 | **OP-T7** (+ OP-L8, OP-L9, OP-L10) | **S4ID-K1**: N-shock non risonanti ⇒ J_u ∩ A_{≤N} = 0 | quelle di S4ID-T2 | §2 |
| 1 | OP-C11 | criterio completo: dizionario evolutivo, K ≥ N: identifica ⟺ d ≤ N; V_{d,k}: identifica mod conseguenze se d(k+1) ≤ N | idem | §2 |
| 1 | **OP-T1** | relazione autonoma non nulla su I ⇒ g analitica su un sottointervallo; "mai analitica" ⇒ J_u = 0 per ogni equazione di evoluzione | g reale C^∞ | §1 |
| 2 | OP-E3, OP-C3′ | F = Σe^{−2^{k/2}}cos(2^kx) mai analitica; g = e^{−x²}F ∈ 𝒮; KdV con dato g: J_u = 0 (INT-Q1 "no" per questa classe) | (WP) | §1 |
| 2 | **OP-P4** | Airy: u_a = ∫e^{−ak²+ikx+ik³t}dk, Schwartz con supporto spettrale ℝ, soddisfa un'ODE autonoma cubica omogenea d'ordine 4 | a > 0, t > 0 | §1 |
| 2 | OP-O5, OP-P6 | ostruzione: le informazioni di tipo (𝒫) (asintotica dominante lungo i raggi) non decidono INT-Q1; INT-Q1 "no" ⇒ non elementarità | — | §1 |
| 2 | OP-L2 | I_PW = ideale dei getti delle soluzioni di v″ = cv | — | §1 |
| 2 | **OP-P17** | KdV: K_d[v] = 0 ⇒ q_d nullo su Λ(v) (senza F1–F4); identificazione in 𝓗_M se |Λ| ≥ M+1, in ogni 𝓗_M se R ≢ 0 | v ∈ 𝒮 reale; (Lax) (verificata n ≤ 3) | §4 |
| 2 | OP-L16 | soluzioni di Jost con asintotica delle derivate | v ∈ 𝒮 | §4 |
| 3 | OP-P18 | NLS: stessa direzione con curvatura nulla | q ∈ 𝒮; (ZC) (verificata n ≤ 3) | §4 |
| 3 | OP-L12, OP-P13, OP-P14 | quasi-omogeneità di Π; deg Π_N ≤ W_N/2 ovunque, = W_N/2 su un aperto di Zariski; N = 2: W_2 = 16, deg 8 | input di calcolo mod p | §3 |

## Punti delicati (dove guardare)
1. **OP-L9**: per j > N, r_j è una forma lineare in r_1..r_N di peso ≤ N < j; induzione sulla ricorrenza dei cumulanti. Verificare che la componente di peso n di κ_mr_{n−m} sia κ̃_mr̃_{n−m}.
2. **OP-L10**: triangolarità delle somme di potenze rispetto ai monomiali **per lunghezza** (non per dominanza); ℓ(μ) ≤ N serve per avere c_μ ≥ 1.
3. **OP-T7 passo 3**: la parte di peso massimo di un prodotto in ℂ[r] graduato; κ̃_n ≠ 0 (passo 4: ι(κ̃_n) = −(n−1)!P_n ≠ 0).
4. **OP-T1 passo 4**: minimalità (ordine, poi grado nella variabile di testa) ⇒ separante fuori da J; caso m = 1 e separante costante.
5. **OP-P4(ii)**: il cambio k = s + b con b immaginario sposta la retta d'integrazione senza teorema di Cauchy (è una sostituzione); serve Cauchy solo per l'indipendenza di 𝖠 da η′ (non necessaria per la tesi).
6. **OP-P17 passo 1**: "soluzione di Lφ = k²φ che tende a 0 a +∞ è nulla" (k reale ≠ 0); passo 3: autospazio L² di dimensione 1 e asintotiche a ±∞ con segni (Ω_d dispari).
7. **OP-O5** è un enunciato su un metodo: verificare che u_a soddisfi davvero (𝒫) (fase stazionaria / asintotica di Ai) e che la conclusione di S4ID-P8 sia compatibile con J_{u_a} ≠ 0 (q_a ∈ I_PW).
8. **OP-P13**: chiusura di Z_w (rango su ℂ(X) di una matrice a entrate polinomiali in k).

## Domande per il revisore
- D1: OP-T7 chiude S4ID-K1 nella forma di S4ID-T2(e)? (Nessuna ipotesi in più.)
- D2: OP-T1/OP-C3′ rispondono a INT-Q1 "per ogni t" per la classe dichiarata? È corretto che non coprano la variante "per t ≥ T₀ > 0"?
- D3: OP-O5 è sufficiente come "ostruzione documentata" (enunciato dimostrato che esclude una classe di prove)?
- D4: OP-P17 rende superflui F1–F4 per la direzione "identifica"? Quale direzione di INT-T1(C) resta CONDIZIONALE?

## SymPy (solo controllo; script in work/OP-NL/sympy/)
k1_checks 115/115 · airy_checks 12/12 · lax_checks 9/9 · kdv_generic 6/6 · kdv_checks N=1,2 7/7 + N=3 INFO. Calcoli mod p = 2147483629 (rango pieno mod p ⇒ indipendenza su ℚ).
