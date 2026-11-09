# KA attack — OPF5B-T1 (density of Σ_j ker_{H^m(Ω)} Q_j in ker_{H^m(Ω)} P)

Referee: adversarial (kill-argument). Source read: only `KA_OPF5B_T1_input.md`. C12-T1′ is assumed true as quoted.

## Attack points

### A1. Counterexample search (one variable / degenerate P, m = 0, non-smooth Ω, repeated factors)
**Verdict: survives.**
The proof does not use ellipticity, hypoellipticity, a principal-part condition or boundary regularity beyond convexity. P depending on one variable (e.g. P = ∂_1(∂_1−1)), m = 0 (zero extension, so Pũ ≠ 0 outside Ω, which the proof never uses), and corner domains (triangle, parallelogram) all go through. The only structural input on P is P ≠ 0, which gives P̃ ≥ c_P > 0. The inclusion Σ𝓗_j ⊂ ker P is immediate because P = c∏Q_j. I found no counterexample. The statement amounts to density of solutions defined near Ω̄, combined with C12-T1′, and that density is a classical kind of result for convex (and star-shaped) sets, proved by the same translation-plus-correction technique.

### A2. Step 1: partition of unity, ε-independence
**Verdict: survives.**
K_0 = Ω̄ ∖ ∪B(p_i,ρ/8) is compact and lies in Ω, since every boundary point is in some B(p_i,ρ/8). {Ω_0, B(p_i,ρ/4)} covers Ω̄. A smooth partition of unity with Σθ_i = 1 on an open V ⊃ Ω̄ exists by the standard construction for a compact set. Nothing depends on ε except τ_i = ε(o−p_i), and that dependence is intended.

### A3. Step 2: geometry of local inward translations
**Verdict: survives.**
The identity y₀+τ_i+q = (1−ε)y₀ + ε(z+q/ε) with z = o+y₀−p_i is correct. If |y₀−p_i| ≤ ρ/2 and |q| < ερ/2, then |z+q/ε−o| < ρ, so z+q/ε ∈ B(o,ρ) ⊂ Ω. The lemma "y₀ ∈ Ω̄, w ∈ Ω, ε ∈ (0,1] ⇒ (1−ε)y₀+εw ∈ Ω" is the standard fact for convex open sets. ε = 1 is harmless.
For the consequence: Ω̄ is compact, so a nearest point y₀ with |y−y₀| < ερ/4 exists. If y ∈ supp θ_i ⊂ B(p_i,ρ/4), then |y₀−p_i| < ρ/4+ερ/4 ≤ ρ/2. Also y+τ_i = (y₀+τ_i)+(y−y₀) with |y−y₀| < ερ/4 < ερ/2, so y+τ_i ∈ Ω. The required radius is not tight, and no step needs the boundary to be smooth.

### A4. Step 3/7: does P(∂)v = 0 really hold on a neighbourhood of Ω̄?
**Verdict: survives.**
On V_ε, θ_i·P(∂)ũ_i is a distribution supported in supp θ_i ∖ O_i. By Step 2, V_ε ∩ supp θ_i ⊂ O_i, so this support does not meet the open set V_ε, and the term vanishes there. The identity Σ_i[P,θ_i]ũ = [P,Σθ_i]ũ = P((Σθ_i)ũ) − (Σθ_i)Pũ vanishes on V, because Σθ_i ≡ 1 on V. Note that Pũ ≠ 0 outside Ω does not matter: the commutator only involves derivatives of Σθ_i, which are zero on V. Hence P(v) = g − P(z) = g − g = 0 on V_ε. V_ε = {dist(·,Ω̄) < ερ/4} ∩ V is open and contains Ω̄. Correct.
For i = 0 (τ_0 = 0), supp θ_0 ⊂ Ω_0 ⊂ Ω, where Pũ = Pu = 0. Correct.

### A5. Leibniz / commutator formula and symbol bounds (Step 5, L1(b))
**Verdict: survives.**
P(∂)(θf) = Σ_α (∂^αθ/α!) P^{(α)}(∂)f is Hörmander's Leibniz formula for constant-coefficient operators, so [P,θ] = Σ_{α≠0}. The symbol of P^{(α)}(∂) is P^{(α)}(iζ), and ∂_ζ^α p(ζ) = i^{|α|}P^{(α)}(iζ), so |P^{(α)}(iζ)| = |p^{(α)}(ζ)| ≤ P̃(ζ). Therefore ‖P^{(α)}(∂)w‖_{2,k_m/P̃} ≤ ‖w‖_{2,k_m}.
Multiplying by the fixed function ∂^αθ_i is bounded on B_{2,k} for temperate k by L1(c): Young's inequality with (2π)^{-2}φ̂*f̂ is correct under the convention f̂ = ∫e^{-ix·ζ}f. k_m/P̃ is temperate by L1(a): the Taylor argument for P̃ is correct, and the swap argument gives temperance of 1/P̃. The constants depend only on P, m and the θ_i, not on ε.

### A6. Step 6: H^m(Ω) control of the correction z = E*g
**Verdict: survives.**
g has compact support in the fixed set K, so E*g is defined and P(z) = g. If φ = 1 near the compact set Ω̄ − K, then ((1−φ)E)*g is supported in supp(1−φ)+K, which misses a neighbourhood of Ω̄. Hence z = (φE)*g there. \widehat{(φE)*g} = \widehat{φE}·ĝ holds because both factors have compact support, and \widehat{φE} is a smooth function. The bound sup|P̃\widehat{φE}| < ∞ is exactly the statement φE ∈ B_{∞,P̃}. With kP̃ = k_m this gives ‖z‖_{H^m(Ω)} ≤ C‖g‖_{2,k} ≤ C″Σ‖w_i‖_{H^m}.
This is the classical gain of P̃ regularity for E*: B^{comp}_{2,k} → B^{loc}_{2,kP̃} (Hörmander). E, φ and K are fixed, so no constant depends on ε. I found no gap.

### A7. Step 4: smallness of w_i
**Verdict: survives.**
ũ = Ext u is fixed, and |τ_i| ≤ ε·diam Ω. Continuity of translations in H^m (dominated convergence in Fourier) gives ‖w_i‖ → 0. ‖θ_iw_i‖_{H^m} ≤ C‖w_i‖_{H^m} holds with fixed θ_i.

### A8. Boundary behaviour on non-smooth convex Ω; F2 (Stein)
**Verdict: survives (citation correct in substance).**
A bounded convex open set in ℝ² with nonempty interior is a Lipschitz domain (standard, e.g. Grisvard 1.2.2). Stein, *Singular Integrals and Differentiability Properties of Functions*, Ch. VI §3 (Theorem 5) gives a universal linear extension operator for Lipschitz ("minimally smooth") domains. It is bounded L^p_k(D) → L^p_k(ℝⁿ) for every k ≥ 0 and 1 ≤ p ≤ ∞, so in particular H^m(Ω) → H^m(ℝ²). Using the zero extension for m = 0 is fine.
The boundary is used only through Ext and through the convexity lemma in Step 2. No trace theory is involved.

### A9. F1 (Hörmander ALPDO II, Thm 10.2.1)
**Verdict: minor gap (citation form only).**
As I recall it, Thm 10.2.1 of ALPDO II is stated in a global weighted form. For every P ≠ 0 (and ε > 0) there is a fundamental solution E with E/cosh(ε|x|) ∈ B_{∞,P̃}, with a norm estimate. The input's form E ∈ B^{loc}_{∞,P̃} follows from this. Write φE = (φ cosh(ε|x|))·(E/cosh(ε|x|)) and use the stability of B_{∞,k} under multiplication by C_c^∞ functions (Hörmander Thm 10.1.? ; the B_{∞} analogue of L1(c)).
The conventions match Hörmander's after the identification P(∂) = p(D), D = −i∂, p(ξ) = P(iξ). P̃ is then exactly Hörmander's P̃ for p, and the Fourier transform conventions agree. The classical form is also Theorem 3.1.1 of Hörmander's 1963 book. The input itself flags the number as unverified. **Fix:** cite it as "Thm 10.2.1 (E/cosh|x| ∈ B_{∞,P̃}), hence E ∈ B^{loc}_{∞,P̃}", and add one line on multiplication by C_c^∞ in B_{∞,k}. This is not fatal.

### A10. Step 8: mollification, convex neighbourhood, C12-T1′
**Verdict: survives.**
W is the metric η_1-neighbourhood of the convex compact set Ω̄, so it is convex and open, and so is W′. v ∈ H^m_loc(ℝ²), so v*ρ_η is C^∞. For x ∈ W′ and η < η_1/2 we have B(x,η) ⊂ W, so P(v*ρ_η) = (Pv)*ρ_η = 0 on W′. v_η → v in H^m(Ω) is standard. C12-T1′ on W′ gives smooth v_{η,j}. Ω̄ ⊂ W′ is compact and Ω is bounded, so v_{η,j}|_Ω ∈ H^m(Ω). The order "first ε, then η" is correct.

### A11. Minor / presentational items
**Verdict: minor gaps (non-fatal).**
- (i) The hypothesis P ≠ 0 (c ≠ 0) is needed for P̃ ≥ c_P > 0 and for F1. It is implicit; state it.
- (ii) The second half of the thesis ("Quindi (C12-P7(a)) … ⟺ γ_N > 0 ⟺ c_F < 1") depends on C12-P7(a), which is not in the input. I did not verify it. It should be labelled as a corollary that depends on that external result.
- (iii) The SymPy references (A1, A2, A3) are numerical sanity checks with no probative weight. All three steps they accompany are proved analytically in the text, so this is harmless.
- (iv) In Step 6, "Ω̄ − K (insieme limitato)" is in fact compact, and that is what is needed for φ ∈ C_c^∞ with φ = 1 on a neighbourhood of it. This is trivial.
- (v) L1(b): "norm ≤ 1 up to i^{|α|}" depends on the normalisation of the norms; the constants are irrelevant.

## Overall verdict: **SURVIVES WITH MINOR FIXES**

I found no counterexample and no fatal gap. The local-inward-translation geometry (Step 2), the claim that P(∂)v = 0 on an open neighbourhood of Ω̄ (Step 7), the ε-uniform B_{2,k_m/P̃} bound on g, and the P̃-regularity gain of E* (Steps 5–6) are all correct. The fixes are purely about citations and presentation: the precise form of Hörmander Thm 10.2.1 (weighted global form, with B^{loc} as a consequence), the explicit hypothesis P ≠ 0, and marking the C12-P7 consequences as dependent on an external result.
