# KA OP-ALG-T3 — memo d'attacco (Thread 1, subagente Claude fresco a110fcefb256292e1, 26/10/2026; input KA_OPALG_T3_input.md; verbatim)

**Rejection memo: OP-ALG-T3**

The adversary in (f) holds up as a construction. The headline does not. It claims "for deciding Ann(u)=(P) the minimal datum is the bit ≡ D; B is strictly stronger whenever Σe_i ≥ 2". Part of that is true by definition, and the substantive part is proved only for one hand-picked domain.

1. **(b) is circular.** D2 defines "sufficient" as "χ ≤ 𝒜". So "χ is the minimum of the sufficient data" just restates the definition, and the proof of (b) says so: "χ ≤ 𝒜 è la definizione". The ordering in D2 only asks whether something is computable. It never bounds the running time of the reduction.

2. **(a) does not show that D carries no more than the bit.** In 𝔇 ≤ χ, when χ = 0 the algorithm runs the semi-decision P4-T4(ii). Nothing bounds that search by any computable function of the inputs. In χ ≤ 𝔇, D turns the question into one finite rank computation. The ordering treats two very different procedures as equal. Equating "the bit" with "a degree bound D" therefore says nothing about P4-Q-min ("is B necessary?") beyond what P4-T4(ii) already gives.

3. **(f) only proves "∃Ω, p₀".** D2 fixes P, Ω and p₀, so the ordering depends on (Ω, p₀). (f) proves 𝔅 ≰ χ only on Ω = (−ε, ε)² with p₀ = 0, and ε comes from P4-L7 applied to P̃. The Lettura drops this condition. For a general Ω, say ℝ², the adversary needs a function ũ on all of Ω with Ann(ũ) = (P̃) and jets at p₀ in ℚ̄. Neither P4-L7 nor anything else in the text provides one. So the universal claim "whenever Σe_i ≥ 2" is not proved. In addition, (f)'s own check uses p₀ = (1,0), which is not the p₀ = 0 of the statement.

**Verdict:** (b) and the minimality reading are true by definition. (f) is proved only on a special local domain. The claim "χ < 𝔅 whenever Σe_i ≥ 2" is not proved for arbitrary (Ω, p₀).
