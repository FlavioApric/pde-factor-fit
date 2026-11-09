# KA attack — OPF5B-T2 / P3 / C4

Input file read: KA_OPF5B_T2C4_input.md, and nothing else. I ran SymPy checks from the scratchpad: (1) my own normal-ordering multiplication for A_1[T]; (2) f·P_r mod x𝒟 for ∂^iT^k with i<6 and k<3; (3) P_r u_G = 0; (4) (2t∂_x + x)u_G = 0; (5) the kernel of f ↦ f·P_r on ℂ[η,T] with deg_η ≤ 6 and deg_T ≤ 2. All five passed, and the kernel is {0}.

## A. T2 (saturated form)

**A1. Ore step in (b)⇒(a′).** A′p_m^{-1} = c^{-1}A″ is the same as cA′ = A″p_m. This is the left Ore condition S·A′ ∩ 𝔇·p_m ≠ ∅.
- For 𝒟 = A_1[T] with T central, take a common left multiple in the Ore domain A_1, coefficient by coefficient (finitely many coefficients). This holds.
- The algebra checks: (cb)Q − A″P = cb·b^{-1}A′p_m^{-1}P + cbQ₀ − A″P = cbQ₀. This is nonzero, lies in 𝔇 and in N, and has degree < m, since left multiplication by a nonzero element of 𝔄 keeps the ∂_t-degree in a domain.

Verdict: **survives.**

**A2. The A_2 case.** That S = 𝔄∖0 is an Ore set in A_2 is left CON-FONTE. The statement is true; the standard reference is localization of R[θ;δ] at the regular elements of a Noetherian domain R. C4 does not use it.

Verdict: **minor gap (citation only).**

**A3. (a′)⟺(c) and (d′), (e).**
- Flatness gives K⊗_𝔄 𝔇/N ≅ 𝔎/𝔎N.
- Because the dimension is finite over the division ring K, 𝔎N ⊇ 𝔎P with equal dimension forces equality.
- (d′) works because b is invertible in 𝔎.
- (e) is trivial.
- In the monic case, a free module means saturated.

Verdict: **survives.**

## B. P3 (leading coefficient π(x))

**B1. 𝔄_π and the "π^{-N}b" form.** {π^N} is a left and right Ore set in A_1, because ad_π is locally nilpotent. So 𝔄_π is a localization of A_1, and therefore a Noetherian domain, and left fractions with a common denominator exist. Also, 𝔄_π acts on C^∞(Ω) because π ≠ 0 on Ω.

Verdict: **survives.**

**B2. Can OP-ALG-T4 be applied over 𝔄_π?** The input asserts that "the proof of T4/L5 uses only Noetherian domain". I cannot see the proof of T4. However, T2 as proved here, with 𝔄 := 𝔄_π (an Ore domain) and P̂ monic, already gives T4 over 𝔄_π:
- L5(a) for a monic P̂ with T central is division with remainder, which works over any ring.
- The (d)-part needs only 𝒯_{𝔄_π} as a set.

So (iv) does not depend on the unseen proof. Suggested fix: cite T2 (monic case) with 𝔄 = 𝔄_π instead of "T4's proof uses only this".

Verdict: **minor gap (citation / attribution only).**

**B3. Steps (iii), (iv), (v), (vi).**
- (iii) is correct.
- (iv), direction ⇒: π^N A ∈ 𝒟 ∩ Ann = 𝒟P, so A ∈ 𝒟_πP. Correct.
- (iv), direction ⇐: correct.
- (iv), the (b) equivalence: clearing denominators by π^N on the left. Correct.
- (v): correct.
- (vi), both directions: cancellation in a domain, with N chosen minimal. Correct.

Consistency check (I tried to kill this and could not): P3 claims that π-torsion-freeness alone is enough, while T2(e) involves the full S-saturation. These do not conflict. If M has no π-torsion, then M embeds into 𝒟_π/𝒟_πP, which is free over the domain 𝔄_π and hence A_1-torsion-free. So no π-torsion implies saturated, and P3(iv) agrees with T2(e).

Verdict: **survives.**

## C. C4 (radial Bessel operator, Gaussian)

**C1. 𝒟/x𝒟 and the right action.**
- x𝒟 = span{x^{a+1}∂^iT^k}, so {∂^iT^k} is a basis of the quotient.
- ∂^i x = x∂^i + i∂^{i−1}.
- ∂x∂ = x∂² + ∂, so P_r = xT − ∂x∂.
- Applied right to left in sequence: f·∂x∂ = η(ηf)′ = ηf + η²f′, which gives f·P_r = Tf′ − ηf − η²f′. This matches my independent normal-ordering code on all tested monomials.

Verdict: **survives.**

**C2. Degree argument.** The η^{d+1} coefficient is −(d+1)c_d(T) ≠ 0, and Tf′ has η-degree d−1. So the map is injective, M has no x-torsion, and P3(vi) applies. The brute-force kernel is {0}.

Verdict: **survives.**

**C3. u_G is not A_1-torsion.**
- h_{j+1} = h_j′ − (sx/2)h_j, and deg_s h_j ≤ j with top term (−sx/2)^j.
- Only j = r contributes to s^r, so its coefficient is β_r(−x/2)^r ≢ 0.
- (x,t) ↦ (x,1/t) is a diffeomorphism of open sets, so the polynomial H vanishing on an open set means H ≡ 0, a contradiction.
- The proof excludes b u_G = 0 on *any* open subset, which is stronger than needed.

Verdict: **survives.**

**C4. Passing from Ω∩{x≠0} to Ω.**
- Ω′ is nonempty because {x=0} has empty interior. Take a component Ω″ of Ω′. There π = x ≠ 0, so P3(iv) gives Ann_{Ω″} = 𝒟P_r.
- Ann_Ω ⊆ Ann_{Ω″} by restriction.
- 𝒟P_r ⊆ Ann_Ω because u_G is smooth on {t>0}, including x = 0.
- Therefore equality holds on every connected Ω ⊂ {t>0}, including Ω that meet x = 0.

Verdict: **survives.**

**C5. (c) and (d).**
- (c): x y″ + y′ + k²x y = 0 for y = J_0(kx), and P_r u_k = 0. For k = 0, u_k = 1, which is still torsion (killed by ∂_x).
- (d): (2t∂_x + x)u_G = 0 was checked. This operator is a nonzero element of degree 0 in ∂_t, so by T2 (b) fails in A_2.

Verdict: **survives.**

## Final verdict: **SURVIVES WITH MINOR FIXES**

- Fix 1: in P3(iv), justify T4 over 𝔄_π via T2 (monic case) with 𝔄 = 𝔄_π, instead of "T4's proof uses only this".
- Fix 2: for the Ore property in A_2 (T2, A_2 case), give the source (it is still CON-FONTE in the input).

C4 does not depend on either fix.
