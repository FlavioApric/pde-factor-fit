# KA OPR2-L2 — Thread 1 (attacco), subagente Claude fresco abac053fe417c06b3, 26/10/2026
Input: work/CHECK/KA_OPR2_L2_input.md (solo quello). Memo verbatim:

KA memo on OPR2-L2 / OPR2-C2. I read only KA_OPR2_L2_input.md.

**Strongest argument against (about 200 words).** The lemma holds up. The weak spot is the corollary, which is proved only by pointing to other results. It says the local proof of OP-ALG-T3(f) transfers to any connected Ω because "only the base instance is local". The other steps are P4-T5 Passi 2–3, P4-T2(v)(a), C3-L3(c) and C3-C2, and none of them is reproduced or quoted in this file. So the step "they hold for any connected Ω and any p₀" is asserted, not checked. Two places where this could fail:

- **The class 𝒰(P,Ω,p₀).** Its definition is not given here. If membership or the majorant 𝔅 involves anything global on Ω (bounds, integrability, behaviour near ∂Ω), the adversary's exponentials e^{⟨z₀,y−p₀⟩} and the entire ũ may not lie in 𝒰 when Ω is unbounded. Then 𝔅 ≰ χ does not follow.
- **The perturbation in Passo 2.** If it relied on ε-smallness or on Taylor truncation at 0 in (−ε,ε)², the transfer fails.

The lemma itself gives no foothold, and every item I checked concretely passed:
- Growth: a_k ≤ C^k follows from a linear recurrence with positive coefficients.
- Uniform bound: |g^{(i)}| ≤ Σ R^n/(n!)² ≤ e^{2√R} holds uniformly in i, so U is entire and termwise differentiation is valid.
- Recursion: it gives P(∂)U = 0 exactly. A SymPy truncation for P = τ²+ξτ+ξ² gives zero residual.
- Independence of the g^{(i)}: the coefficient matrix 1/(n!(n+i)!) has full rank 13 for N = 12.
- Choice of λ: r_i^λ ≢ 0 because P/P_i is monic of τ-degree below m.
- Slice: the restriction to the slice preserves EP.
- C3-T1(a): the criterion is correct on any connected Ω.
- Jets: they stay in K under translation by p₀ ∈ (K∩ℝ)² and A ∈ GL₂(ℚ).

So this is a documentation gap in the corollary, not an exhibited error.

Script: scratchpad scheck16_ka_1.py. No project files were written.

VERDICT: cannot kill
