# KA OPR2-T1 — Thread 1 (attacco), subagente Claude fresco a8cb4aa6299c2b88c, 26/10/2026
Input: work/CHECK/KA_OPR2_T1_input.md (solo quello). Memo verbatim:

MEMO (kill attempt on OPR2-T1)

I could not find a fatal defect. The strongest attack I can make goes after how the proof is glued together, and it fails. Take the hardest step, Passo 7. It claims an exact identity, v − u = Σ[θ_i(u∘τ_i − u) + (χ_i − θ_i)(F(s∓σ) − F)] − z. That identity needs u = u_1 + F(s) on Ω∩B(C_i,2r) after translation, and it needs every term to be controlled in H^m uniformly in ε.

I checked each ingredient concretely:
- **Commutator.** H(θw) = θHw + (θ_t + θ_xx)w − 2∂_x(θ_x w) is correct, so Hũ_1 = 0 holds exactly.
- **Supports.** {s > b−δ}∩Ω ⊂ B(C_1,r), so supp∇θ_i and supp(χ_i − θ_i)∩{χ_i ≠ 1} stay at s-levels in a compact subset of S. That keeps g_0, g_1 ∈ H^m and gives F(·∓σ) → F there.
- **Order of constants.** r, then δ, then a compact K covering the annuli enlarged by σ_0, then ε_0. Nothing circular.
- **Lemma L0.** ‖K_1‖_{L¹} ≤ √(T′+1). ∂_t commutes with the Duhamel integral because χ̃ vanishes near r = −1. The constant does not depend on ε, so z → 0.
- **Translation continuity.** Valid, since the translated points land in Ω (respectively in Ω_K).
- **c ≤ 0 cases.** The reflection x ↦ a+b−x is exact. c = 0 falls back on OPF-T5(b), which is taken as given.
- **Extension paragraph.** y+τ lies at distance ≥ ερ/2 from ∂Ω, which is sound.

What is left is not mathematical. The ⟺ chain in the Tesi rests on C12-P7(a) and on γ_2 and c_F, which are not defined in this text. The Hörmander and Stein citations are labelled CON-FONTE with unverified numbers. And "the other inequalities hold for r, ε small" in step 3(a) is left implicit, although it is trivially true.

VERDICT: cannot kill
