# KA OPR2-T3 — Thread 1 (attacco), subagente Claude fresco aeb592a933bbbff95, 26/10/2026
Input: work/CHECK/KA_OPR2_T3_input.md (solo quello). Memo verbatim:

MEMO (kill argument, OPR2-T3 / Lettura)

The "Lettura" says the right condition is a multiplicity-free socle. It claims this is strictly weaker than non-similarity, and gives as the witness that 𝔎/𝔎(∂_t − a)² is uniserial when ∂_t is central. That witness is false for non-central a in K = Frac(A_1).

Take 𝔇 = 𝒟, so δ = 0 and ∂_t is central, and take a = x. For every c ∈ ℂ:
(∂_t − x + (∂_x+c)^{-1})(∂_t − x − (∂_x+c)^{-1}) = (∂_t − x)².
Check: the cross terms give [x,(∂_x+c)^{-1}] = (∂_x+c)^{-2}, which cancels −(∂_x+c)^{-2}. More generally, a right factor ∂_t − x − e exists exactly when e² = [x,e]; e = 0 and e = (∂_x+c)^{-1} both solve it.

So M_K = 𝔎/𝔎(∂_t − x)² has a continuous family of distinct simple submodules 𝔎(∂_t − x − (∂_x+c)^{-1})/𝔎P. They are pairwise isomorphic, since (∂_x+c)(x)(∂_x+c)^{-1} = x + (∂_x+c)^{-1}. The socle is therefore S⊕S, not uniserial, with infinitely many atoms. This is the OP-ALG-C1 obstruction again, inside the paper's own showcase example. The example only works for central a (e.g. a ∈ ℂ). As written, the Lettura's evidence for "strictly weaker than non-similarity" is wrong and needs a correct example.

Second defect: the Tesi's parenthetical "D_i is, up to a left factor in K, a right divisor of P with P = A_iD_i" is false whenever deg A_i ≥ 2. A nonzero element of S_i = 𝔎D/𝔎P has the form kD with k ∈ 𝔎 of degree < deg A_i, not only K·D. The criterion survives this, because any nonzero element of the atom works. The stated description of the tests does not survive.

The core T3 proof (saturated ↔ 𝔎-submodules, an atom inside L_u, r ≤ ℓ ≤ m) and Example (i) check out.

VERDICT: weak reject
