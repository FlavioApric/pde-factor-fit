# KA OP-T1 — memo d'attacco (Thread 1, subagente Claude fresco a14f9b6c1253d0a41, 26/10/2026; input KA_OPNL_T1_input.md; verbatim)

Rejection memo: OP-T1

I tried hard to break the proofs and could not. OP-T1(a)(b)(c) is correct.
- Step 1 (reduction to real coefficients) works because g is real.
- The minimal choice by order, then degree, is sound, and so is the separant argument. For m ≥ 2, s has degree exactly m−1 in y_K (characteristic 0). For m = 1, s is either a nonzero constant or has order < K.
- The real-analytic implicit function theorem and analytic-ODE steps are applied correctly. Uniqueness among C¹ solutions holds because F is locally Lipschitz.
- The slice argument holds in both the open case and the half-open case. The half-open case needs u to be C^∞ up to t₀, and that is assumed.
- The OP-E3 arithmetic checks out. Exactly one k_m exists. On [8m, 8√2m], e^{−s}s^{8m} ≥ e^{−8√2m}(8m)^{8m}. The Cauchy-estimate ratio is ½(16mρe^{−2√2})^{4m} → ∞.

The strongest objection is about what OP-C3′ actually shows. The explicit datum is g = e^{−x²}F, which has Gaussian decay on both sides. By the smoothing fact the package itself states in Remark (3), u(t,·) is real-analytic for every t ≠ 0. So J_u = 0 is witnessed only at the single slice t = 0, or by continuity from any window that touches 0. For any observation window [T₀, T₁] with T₀ > 0, OP-T1 says nothing. Whether a polynomial relation holds there is exactly as open as before.

The "no" therefore answers INT-Q1 only in its literal "per ogni t" form, through a regularity artefact at a single instant. It says nothing about the dispersive or identification content the question was asking about. The Portata section adds a contradiction: it excludes exponentially decaying data from the result's reach, yet the chosen example decays faster than any exponential.

Verdict: the mathematics is right, but OP-C3′ overclaims its relevance to INT-Q1. It should be restated as an answer about the t = 0 slice only.
