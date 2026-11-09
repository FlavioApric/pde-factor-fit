# AUDIT II-P5 — normalità della compagna; proiettori ortogonali e Lagrange
Revisore: S-CHECK-2B · 25/10/2026
Fonte esaminata: SOLO `work/II/CHECK_REQUEST.md` §II-P5.
Skill: session-protocol, claim-lifecycle, proof-checker, scientific-critical-thinking, sympy.
SymPy: `work/CHECK/sympy/audit_ii.py` → `audit_ii.out` sezione "II-P5" (OK, 6 controlli); `audit_round2.out` sezione "II-P5" (OK, 4 controlli).

**Verdetto: PASS** (rilievi MINOR). Confermato anche il CONFLITTO con l'enunciato di Fase 1 "normale ⟺ s^m − c, |c| = 1".

## 1. Enunciato canonico
C ∈ Mat_k(ℂ) compagna di p(s) = s^k + Σ_{j<k}p_js^j (coefficienti complessi). TFAE: (1) C normale; (2) radici semplici e λ_aλ̄_b ∈ μ_k \ {1} per ogni a ≠ b; (3) k = 1; oppure k = 2, |p₀| = 1, p̄₀p₁ = −p̄₁; oppure k ≥ 3, p = s^k − c, |c| = 1. Inoltre, radici semplici ⇒ Π_a = v(λ_a)w_aᵀ (w_aᵀ riga a di V⁻¹) e w_aᵀv(τ) = ℓ_a(τ).

## 2. Micro-claim
| MC | Passo | Esito |
|---|---|---|
| MC-1 | normale ⇒ diagonalizzabile; non derogatoria e diagonalizzabile ⇒ radici semplici | OK |
| MC-2 | radici semplici: autospazi = ℂv(λ_a) (F0) | OK |
| MC-3 | C normale ⟺ autospazi a due a due ortogonali | OK (diagonalizzabile con base ortogonale di autovettori ⟺ unitariamente diagonalizzabile) |
| MC-4 | ⟨v(λ_a),v(λ_b)⟩ = Σ_{j<k}z^j, z = λ_aλ̄_b; = 0 ⟺ z ≠ 1 e z^k = 1 | OK (per z = 1 la somma è k ≠ 0) |
| MC-5 | (2)⇒(3), k ≥ 3: |λ_a||λ_b| = 1 per ogni coppia ⇒ |λ_a| = 1 | OK **perché k ≥ 3** (tre indici distinti: |λ_b| = |λ_c| e poi |λ_b|² = 1); per k = 2 il passo è falso ed è infatti escluso |
| MC-6 | λ_a/λ_b ∈ μ_k\{1}, k valori distinti ⇒ {λ_a} = λ_1μ_k ⇒ p = s^k − λ_1^k | OK |
| MC-7 | (3)⇒(1), k ≥ 3: C = S + c e_ke_1ᵀ permutazione ciclica pesata, unitaria | OK (anche (3)⇒(2) diretto: le radici sono λ_1μ_k) |
| MC-8 | k = 2: CC* − C*C = [[1−|p₀|², −p₁p̄₀ − p̄₁],[−p₀p̄₁ − p₁, |p₀|²−1]] | OK (ricalcolato in SymPy) |
| MC-9 | k = 1 | OK (scalare; (2) vacuo) |
| MC-10 | Lagrange: Π_a = v_aw_aᵀ, w_aᵀv(τ) = ℓ_a | OK (C = V diag(λ) V⁻¹; w_aᵀv(λ_b) = δ_ab, grado < k) — verificato su radici 1, 2, −1 |

## 3. Problemi trovati
- **II-P5-F1 · esposizione · MINOR.** Il ramo k = 2 di (3) è dimostrato via (1) (commutatore), non via (2): va detto che per k = 2 la catena è (1)⟺(3) diretta e (1)⟺(2) da MC-4. Utile anche la forma esplicita: |p₀| = 1, p₀ = e^{iθ}, p₁ = i r e^{iθ/2} con r ∈ ℝ; equivalentemente λ₂ = −1/λ̄₁ (radici non necessariamente di modulo 1: λ₁ = 2 + i, λ₂ = −1/(2−i) dà una compagna normale, verificato). *Fix:* ADD_DERIVATION di due righe.
- **II-P5-F2 · ADD_REFERENCE · MINOR.** risultati di questo tipo (compagne normali per k ≥ 3 = permutazioni cicliche pesate unitarie) sono probabilmente in letteratura, ma non ho verificato alcuna fonte: lo stato resta DIMOSTRATO per prova propria, la novità va dichiarata bassa.
- **Conflitto con Fase 1** ("normale ⟺ s^m − c, |c| = 1 per ogni m", R6-T3/R7-T5): **confermato FALSO per m = 2**. Controesempio verificato: s² + s − 1, compagna [[0,1],[1,−1]] simmetrica reale, quindi normale, e non della forma s² − c. Per m ≥ 3 l'enunciato di Fase 1 è corretto (20 cubiche casuali non normali; s³ − e^{2πi/3} normale).

## 4. Red team
| Tentativo | Esito |
|---|---|
| famiglia k = 2 con |λ| ≠ 1 | normale: (3) k = 2 regge e mostra che |λ| = 1 NON è necessario per k = 2 |
| cubiche casuali | nessuna normale: coerente |
| s³ − 1/2 (|c| ≠ 1) | non normale: coerente |
| radici multiple | non diagonalizzabile: coerente con MC-1 |

## 5. Stato proposto
**DIMOSTRATO** (con F1 testuale). Il claim di Fase 1 R6-T3/R7-T5 va registrato **FALSO per k = 2** (vero per k ≥ 3), controesempio s² + s − 1.
