# KA OP-ALG-T1 — memo d'attacco (Thread 1, subagente Claude fresco aa6338d40139718c7, 26/10/2026; input KA_OPALG_T1_input.md; verbatim)

**Rejection memo: OP-ALG-T1 (iv)–(v) is not proved, because of a field-of-definition gap.**

M3-hol lets u be any analytic solution of I ⊂ A_2(K), K = ℚ̄. Its jets only have to lie in the larger field 𝕂, and (v) lets the ideal I live over K. OP-ALG-P1 decides "L_*u = 0" only for L_* ∈ A_2(K). OP-ALG-L1, L2 and L4 and (AC) are also stated only over K. But Ann(u) need not be generated over K.

**Counterexample.** Take I = (∂_t², ∂_t(∂_x−1), (∂_x−1)²) ⊂ A_2(ℚ). It is holonomic, with solution space span{e^x, te^x, xe^x}. Let u = e^x(t+πx) and p₀ = 0. Every jet lies in ℚ[π], so 𝕂 = ℚ(π) is computable with decidable equality, and the input is admissible. Then:
- R·u = span{u, e^x}, which has dimension 2.
- (π∂_t − ∂_x + 1)u = 0.
- So Ann(u) = (πτ−(ξ−1), (ξ−1)²), an ideal of colength 2 that is not defined over ℚ̄.

**How (iv) fails.** Take 𝓛 = span{τ, ξ−1}, which has a basis in K[τ,ξ]. Then Ann(u)∩𝓛 = ℂ·(πτ−ξ+1). The proof cites P4-T4(i) with "the oracle of zero given by (i)". But (i) cannot test π∂_t − ∂_x + 1, so P4-T4(i) is being used with an oracle that is too weak for its hypotheses.

**How (v) fails.** Here G_u = 1 and w₀ = u. Within the stated tools, the procedure can only certify elements of Ann(u)∩K[τ,ξ]_{≤B}. Those elements generate (τ, ξ−1)², which has colength 3. That is strictly smaller than Ann(u), so the output generators are wrong.

**What a repair needs.** P1, L1, L2 and L4 would have to be redone over 𝕂. That means eliminants for M ∈ A_2(𝕂), computable arithmetic and root-finding in 𝕂, and outputs given over 𝕂 instead of K. None of this is stated or proved. As written, the theorem claims more than its proof chain delivers.
