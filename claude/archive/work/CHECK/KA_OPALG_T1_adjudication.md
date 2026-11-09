# KA OP-ALG-T1 — arbitrato (Thread 2, subagente Claude fresco af69745e092fcf96b, 26/10/2026; letti solo KA_OPALG_T1_input.md e KA_OPALG_T1_attack.md; testo integrale)

Hand-check of the counterexample: I = (∂_t², ∂_t(∂_x−1), (∂_x−1)²) is constant-coefficient with characteristic ideal (τ, ξ−1)² (colength 3, zero-dimensional) → A_2/I holonomic, solutions span{e^x, te^x, xe^x}. u = te^x + πxe^x: ∂_tu = e^x, ∂_xu = u + πe^x, so (∂_x−1)u = πe^x = π∂_tu, i.e. (π∂_t − ∂_x + 1)u = 0; also (∂_x−1)²u = 0, ∂_t²u = 0, R·u = span{u, e^x}. Ann(u) = (πτ − ξ + 1, (ξ−1)²), colength 2, tangent direction at (0,1) is [π:1] → not defined over ℚ̄. Ann(u) ∩ ℚ̄[τ,ξ] = (τ, ξ−1)² (colength 3). Nit: D1 requires 𝕂 ⊇ K, so take 𝕂 = ℚ̄(π) (still computable with decidable equality); counterexample admissible.

### Point P1: Ann(u) need not be generated over K
Verdict: still_unresolved. D1(iii)–(iv) only require I ⊆ Ann with I over K and jets in 𝕂; nothing asserts K-rationality of Ann(u) (true only for G_u in (iii), since G_u ∼ ∏P_i^{f_i}). Severity: major for (iv)–(v); none for (i)–(iii). Fix: remark that Ann(u)∩𝓛 and generators of J_u are 𝕂-rational, not K-rational in general; outputs over 𝕂.

### Point P2: zero oracle in (iv) too weak
Verdict: still_unresolved (as text stands). aτ + b(ξ−1) kills u iff a + bπ = 0; proof of (iv) cites "oracolo di zero dato da (i)", which covers only A_2(K). Severity: major for (iv). Fix: extend OP-ALG-P1 to v = Σc_kQ_k(∂)u (c_k ∈ 𝕂, Q_k ∈ A_2(K)) with a simultaneous eliminant over K: S_h → N^r, L ↦ (L·Q_k·1̄)_k has image of dim ≤ rC(h+d)² while dim S_h ~ h³/6, so a nonzero L ∈ S_t(K) kills every Q_ku, hence v; same for L′_n ∈ S_x(K) for ∂_t^nv. L2, L3, P4-L4, (AC) unchanged; only equality tests in 𝕂 on jets (already assumed).

### Point P3: (v) returns wrong generators
Verdict: partially_answered. B is fine (G_u ∈ K[τ,ξ], w₀ has eliminants over K, L4 and B := dim E(w₀) work; C3-T3(ii) field-independent). The generator step goes through (iv) and inherits P2. "Outputs wrong generators" overstated: the step is unjustified, not provably wrong. Separate gap: (v) never assumes P(∂)u = 0 or Ann(u) ≠ 0 but needs G_u (e.g. u = e^{tx}, Ann(u) = 0). Severity: major for generators; minor for B. Fix: compute Ann(w₀)∩R_{≤B} over 𝕂 after extending P1; add hypothesis "P(∂)u = 0 for a given P" to (v).

### Point P4: repair needs the whole chain over 𝕂
Verdict: partially_answered — repair not in text, but the memo's cost claim is wrong: operators lie in A_2(K)⊗_K𝕂, the simultaneous eliminant stays over K; L2, L3, L4 never see 𝕂; no root-finding in 𝕂. Severity: minor. Fix: write "simultaneous eliminant" as a corollary of OP-ALG-L1.

### Point P5: scope
Verdict: answered_by_current_text for (i)–(iii): every operator tested there (Q, P, P/P_i^k, a*(∂_t)Q(∂), b*(∂_x)Q(∂)) lies in A_2(K); jets enter only via equality in 𝕂. On the counterexample with P = τ², (iii) runs correctly (G_u = 1, Ann(u) ≠ (τ²) detected).

## Summary
answered 1 (P5); partially 2 (P3, P4); unresolved 2 (P1, P2); critical none.

## Net assessment
The headline survives: deciding "L_*u = 0", "Q(∂)u ∈ EP", "Ann(u) = (P)", "V(Ann u) = V(P)" and computing G_u is fully supported. Part (iv) and the generator half of (v) have a real gap (correct counterexample), local and cheap to close with a simultaneous Bernstein eliminant over K. The bound B in (v) (answer to P4-Q1) is unaffected. (v) needs the explicit hypothesis P(∂)u = 0.

## Top action items
1. Corollary of OP-ALG-L1 (simultaneous eliminant over K); extend OP-ALG-P1 to 𝕂-combinations; cite it in (iv).
2. Restate (iv)–(v) over 𝕂; include e^x(t+πx) as remark.
3. Add P(∂)u = 0 (given P ∈ K[τ,ξ]) to (v).
