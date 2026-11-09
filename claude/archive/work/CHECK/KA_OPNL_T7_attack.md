# KA OP-T7 — memo d'attacco (Thread 1, subagente Claude fresco a9050556dea50320c, 26/10/2026; input KA_OPNL_T7_input.md; verbatim)

Rejection memo: OP-T7

Verdict: I tried hard to break OP-T7 and could not. I find the theorem proved as stated. My strongest objection is about scope: OP-C11 claims more than it proves, mainly in part (b).

I checked every step and each one holds:
- The cumulant recurrence: D^m(wφ)/φ is expanded by Leibniz, and G = log M follows formally.
- OP-L9: every weight bound is applied component by component, so the integral-domain property is never needed.
- ι(κ̃_n) = −(n−1)!P_n: this holds because ι is a ring homomorphism and the recurrence is formal.
- The map α ↦ μ(α) is a bijection from multisets to partitions, and ℓ(μ(α)) = |α| ≤ N.
- OP-L10: when partitions of one length are ordered by length, the matrix is block-diagonal and also triangular.
- Passing from ℂ(X) to ℂ[r] works because r_1..r_N are algebraically independent (imported).
- The edge cases are handled: constants give W = 0 with P_∅ = 1; N = 1 is consistent with the traveling-wave Riccati relation; k_i ≠ 0 makes V invertible.
- The result is sharp, since the argument fails exactly at |α| = N+1.

Strongest objection (OP-C11):
1. The corollary is titled "Criterio completo", but part (b) is not a complete criterion. It decides only two cases: d(k+1) ≤ N, and k ≥ N with d ≥ N+1. Everything in between is left open. For example, k ≥ N with d ≤ N, or k < N with d(k+1) > N.
2. The positive branch of (b) is nearly empty:
   - The header constraint "d ≥ 2, K ≥ 2" is stated for K, but (b) uses a lowercase k with no constraint and says "per ogni k".
   - If F_B must lie in V_{d,k}, then k ≥ 2 and d ≥ 2. That gives d(k+1) ≥ 6, so the positive branch says nothing for N ≤ 5.
   - For k < 2 the claim is ill-posed, because F_B is not in the dictionary.

Part (a) is complete and correct. Part (b) should be restated: drop the word "complete", constrain k, and state the gap explicitly.
