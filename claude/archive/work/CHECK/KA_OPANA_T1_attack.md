# KA OPA-T1 — Thread 1 (attacco), subagente Claude fresco a343adcdc022c0067, 26/10/2026
Input: work/CHECK/KA_OPANA_T1_input.md (solo quello). Memo verbatim:

**Rejection memo, OPA-T1 / OPA-C1**

The local asymptotics are not where the paper fails. I recomputed ρ = ½log(J⁻/J⁺) from W_± ∝ e^{−Φ(a±)/2ν}J(a±)^{−1/2}, the layer value 2log((1+e^ρ)(1+e^{−ρ})) = 4log(2cosh(ρ/2)), the Lemma 2 remainders, and the OPA-C1 integral 2log((1+t)/(1−t cos b)) (≈1.210 at t=2). All of them hold. What fails is the conclusion drawn in line 28: "S4T-Q1 è risolto … Θ(ν), senza fattore logaritmico."

What the proof establishes is a limit as ν→0 at one fixed t. The constants that drive it are δ, j₀, η, r₀ in Lemma 1(iii). They come from compactness and finite subcovers, so none of them is quantitative. The remainder in Step B is an unquantified o(ν) from dominated convergence, as Residual Risk (2) admits. So the proof gives no bound for any actual ν, and no uniformity in t.

That uniformity is exactly what the question is about. Tang–Teng's ν|logν| is a uniform-in-time statement. The paper's own OPA-R1 shows the claimed constant blows up: Λ(t) ~ 2log(1/(t−t*)) as t↓t*, and the rate at t* is ν|logν|. Therefore sup_{t∈[t*,T]} ‖S(t)u₀−S_B(t)u₀‖₁/ν = ∞, and the logarithm is not removed. It has only been moved into a t-dependent constant.

Hypothesis (H_t) is also verified only for ε sin x. For generic data it fails at every later shock birth (J=0 at a minimizer) and every collision (triple minimizer). The same blow-up recurs there, and the theorem says nothing about it.

**Verdict:** Reject the S4T-Q1 resolution claim. At most, OPA-T1 is a pointwise-in-t, non-quantitative expansion under (H_t). It does not answer S4T-Q1, and "senza fattore logaritmico" is an overclaim.
