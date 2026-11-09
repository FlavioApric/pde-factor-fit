# KA attack report: OPF5A-T2 / Lemma U (S-CHECK-20, 26/10/2026)

The only project file read was work/CHECK/KA_OPF5A_U_input.md. The scripts are in the scratchpad (s20ka_sym.py, s20ka_psi0.py, s20ka_psi0b.py).

## Attack 1: normal form coefficients and scalings
- **Target:** Ψ_τ → Ψ_0 = ξA + κ3A⁴/24 − A²/(2t*²), with remainder O(√τ|A|⁵).
- **Attack:** I redid the expansion by hand. Write s = √τA, x − a* = t u0(a*) − tτ^{3/2}ξ. Then:
  - U0(a*+s) − U0(a*) = u0* s − s²/(2t*) + κ3 s⁴/24 + O(s⁵).
  - The quadratic part of the kernel gives −(x−a*)s/t + s²/(2t) = −u0* s + τ^{3/2}ξ s + s²/(2t).
  - Adding them: τ²[ξA − A²/(2 t t*) + κ3A⁴/24] + O(τ^{5/2}|A|⁵). This uses 1/(2t) − 1/(2t*) = −τ/(2tt*).
  - The effective weight is exp(−τ²Ψ/2ν) = exp(−Ψ/2ν̂) with ν̂ = ν/τ².
  - u − v = (a(x) − ⟨y⟩)/t = √τ(A_m − ⟨A⟩)/t, and dx = tτ^{3/2}dξ, so ∫|u−v|dx = τ²∫|A_m − ⟨A⟩|dξ.
  - At ξ = 0 the minima are at A² = 6/(κ3t*²), with Ψ_0'' = 3/t*² − 1/t*² = 2/t*².
  - For ∂_A⁴ of the remainder, u0 ∈ C⁵ gives O(√τ|A|). So C⁴ convergence on compacts holds.
- **Outcome:** SURVIVES, with one MINOR correction. The quadratic coefficient of Ψ_τ is 1/(2tt*), not 1/(2t*²). The remainder is therefore O(√τ|A|⁵ + τA²), not only O(√τ|A|⁵). This does not affect convergence on compacts.

## Attack 2: is there a bad regime of τ?
- **Target:** whether e/ν − 2log(1/max(τ,√ν)) is O(ν) uniformly in τ (here e = ‖u−v‖_{L¹}).
- **Attack, analytic:** the constants are chosen in this order: K'(b) from 2C/c1, then Ξ, then (ν̂0, C_L3) from L3 on {Ψ_τ}, then K1 ≥ ν̂0^{-1/2}, then K'(a) from K1. There is no circularity.
  - For every τ ≥ K1√ν we have ν̂ ≤ ν̂0. That includes τ ~ ν^{1/3}, τ ~ ν^{1/4}, and τ ~ τ0 (ν̂ tiny).
  - L3 needs only ν̂ ≤ ν̂0, not ν̂ → 0. So there is no intermediate regime left uncovered.
- **Attack, numerical:** full Hopf solution against Lax–Oleinik for u0 = −sin y − ε sin 2y.
  - ε = 0 is the odd case, with κ4 = 0. ε = 0.3 is asymmetric: the A⁵ term is present and the shock drifts.
  - Grid: ν = 1e-4, 1e-5, 1e-6 and τ/√ν from 0.3 to 100, including τ = ν^{1/3}, ν^{1/4}, 0.05 and 0.1. The x-grid is geometric around the located shock; the y-grid spacing is at most min(√ν, ν^{1/4})/40.
  - **Result:** e/ν − 2log(1/max(τ,√ν)) lies in [2.80, 3.09] for ε = 0 and in [1.67, 2.71] for ε = 0.3.
  - At fixed τ/√ν the values agree across ν to within 0.01 for ε = 0. That is the expected profile function of τ/√ν with an O(1) limit. No logarithmic drift appears.
- **Outcome:** SURVIVES. No counterexample regime.

## Attack 3: uniformity of L3 over {Ψ_τ}
- **Target:** degenerate minimizers, inflection points and folds, the range |ξ| ≤ Ξ, the matching region |A| ≈ K', and tails up to z0/√τ.
- **Degenerate global minimizers:** for Ψ_0, global minimizers have A_m² ≥ 6/(κ3t*²), so Ψ_0'' ≥ 2/t*² uniformly. The fold points (A² = 2/(κ3t*²), ξ_f = ±(2√2/3)/(t*³√κ3)) are only metastable. Numerically their gap at the fold is about 4.46 for κ3 = t* = 1, so the margin η is positive.
  - The stated argument ("a degenerate global min needs Ψ''' = 0, but Ψ''(0) < 0") is correct.
  - The Laplace leftover e^{−η/4ν̂}ν̂^{−1/2} is ≤ ν̂ once ν̂0 is small. This is fine, because ν̂0 is chosen after η.
- **Slopes:** ∂_ξ f_12 = A_1 − A_2 (envelope theorem). Near ξ = 0 this is about 2√6/(t*√κ3), which is nonzero.
- **Tails:** the bound ψ ≥ c1(z⁴ + α²z²) − Cτz² holds for any base point. In rescaled form it reads Ψ_τ − m ≥ cZ⁴ − CZ², which is ≥ cZ⁴/2 for |Z| ≥ R.
  - Compact |Z| ≤ R is covered by C⁴ convergence.
  - For |z| ≥ z0, the original Φ_x − m ≥ c gives e^{−c/ν}·O(ν^{−1/4}), which is negligible.
- **Matching:** the interior {|α| < K'√τ} maps into |ξ| ≤ Ξ for a fixed Ξ with margin; the O(√τ) shift between Ψ_τ and Ψ_0 is absorbed. The exterior bound and the L3 bound overlap without a gap.
- **Numerical check:** ∫_{|ξ|≤7.5}|A_m − ⟨A⟩|dξ / ν̂ for Ψ_0 takes the values 5.81, 5.52, 5.44, 5.42, 5.42, 5.37, 6.1 for ν̂ = 0.3 down to 3e-4. It is bounded; the last value carries some A-grid error.
  - A first run on a uniform ξ-grid seemed to show growth. That was an artifact: the shock layer (width about ν̂) was thinner than the grid spacing.
- **Outcome:** SURVIVES in substance. GAP (MINOR, presentational): L3 is stated and proved for Burgers times t in a compact set on 𝕋. Lemma U applies it to an abstract compact family of potentials on ℝ in (ξ, A). That transfer is asserted, not stated as a lemma.

## Attack 4: outer region of (b)
- **Target:** error ≤ Cν^{3/2}/(K'²τ), main term 2ν log(1/τ) + O(ν).
- **Attack:**
  - With dx = J_t dα ≍ α²dα and |E1|/t ≤ Cν^{3/2}/|α|⁵, the error is ∫_{K'√τ}^{∞} ν^{3/2} α^{−3} dα = ν^{3/2}/(2K'²τ). This is ≤ Cν/K1 for τ ≥ K1√ν.
  - The E1 term-by-term bounds hold provided w = √ν/|α| ≤ |α|, i.e. α² ≥ √ν. That is true because α² ≥ K'²τ ≥ K'²K1√ν.
  - Main term: ν∫t|u0''|/J_t dα with J_t ≈ κ3tα²/2 − τ/t* gives 2·2log(1/(K'√τ)) + O_{K'}(1).
  - The expansion of ⟨z⟩ in Passo 1 is algebraically correct; I re-derived it.
- **Outcome:** SURVIVES. GAP (MINOR): the moment bounds ⟨|z|^k⟩ ≤ Cw^k are proved in L2 only for t ≤ t*. For t = t* + τ in the exterior they follow from ψ ≥ (c1/2)(z⁴ + α²z²) and the argument of L2(c), but this is not written out.

## Attack 5: part (a), τ ≤ K1√ν
- **Target:** whether the interior contributes O(ν) and the main term is ν|log ν| + O(ν).
- **Attack:**
  - The interior x-set has width ≤ C(K'³ν^{3/4} + τK'ν^{1/4}) = O(ν^{3/4}).
  - Denominator: ψ ≤ C(1 + K'² + K1)ν on |z| ≤ ν^{1/4}. Numerator: ψ ≥ c1z⁴ − CK1√ν z². In ζ = z/ν^{1/4} this gives ⟨|z|⟩ ≤ C_Kν^{1/4}, so the interior contributes C_Kν.
  - Exterior: J ≍ α² because K'² ≥ 2CK1/c1.
  - Consistency: for √ν ≤ τ ≤ K1√ν, 2ν log(1/τ) = ν|log ν| − 2ν log(τ/√ν) = ν|log ν| + O(log K1)ν.
- **Outcome:** SURVIVES.

## Attack 6: hidden dependencies
- [F1] (Lax–Oleinik equals the entropy solution) is assumed explicitly; it was not attacked.
- The claim that every minimizer away from (x*, a*) is unique and non-degenerate for τ ≤ τ0 follows from compactness and from uniqueness at t* under (G*). OK.
- **Outcome:** SURVIVES. These are conditional on the stated hypotheses only.

## Overall verdict: SURVIVES
No regime of τ breaks the O(ν) statement, and the normal form, scalings, constant ordering, outer error and part (a) are all correct. The only gaps are MINOR and presentational:

1. **Remainder of Ψ_τ.** It should read O(√τ|A|⁵ + τA²); the τA² piece comes from 1/(2tt*) versus 1/(2t*²).
2. **Missing statement ("L3-abstract").** It would close the transfer gap:
   > Let {Ψ^λ}_{λ∈Λ} be a family of C⁴ functions on ℝ_ξ × ℝ_A, Λ compact. Assume:
   > - convergence in C⁴_loc as λ → λ0;
   > - uniform coercivity Ψ^λ(ξ,A) − min_A Ψ^λ(ξ,·) ≥ c|A − A_m|⁴ − C for large |A|;
   > - (H) for every ξ in [−Ξ−1, Ξ+1]: at most finitely many ξ with two minimizers, all global minimizers with Ψ'' ≥ j0, and |∂_ξ f_jk| ≥ s0.
   >
   > Then there are ν̂0 and C, depending only on j0, s0, the margin η, the C⁴ bounds and the coercivity constants, such that for all λ and ν̂ ≤ ν̂0
   > ∫_{|ξ|≤Ξ}|A_m − ⟨A⟩_{ν̂}| dξ ≤ Cν̂.

   The L3 proof applies verbatim. Separately, the L2(c) moment bounds should be noted for t > t* in the exterior.
