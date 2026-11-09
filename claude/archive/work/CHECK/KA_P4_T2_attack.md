# Kill-argument P4-T2 — Thread 1 (memo d'attacco), subagente Claude fresco a3a6b4be4aec9658d, 25/10/2026, verbatim
**Rejection memo: P4-T2**

The headline result is false as stated. It claims "u identifies P (Ann(u) = (P)) ⟺ W has no joint eigenvectors". The theorem only proves (v)(a), "Ann(u) principal ⟺ J = R ⟺ σ_p(u) = ∅". Being principal is not the same as being equal to (P) for the given P, so only the direction "identifies ⇒ no eigenvectors" holds.

Here is a counterexample, checked by the same argument the file uses in P4-C2(a). Take Ω = (0,1)×(−1,1), u = e^{x²} and P = τ².
- P(∂)u = 0.
- For any Q, Q(∂)u = Q(0,∂_x)e^{x²}. Since e^{x²} is not EP, this vanishes only when Q(0,ξ) ≡ 0. So Ann(u) = (τ), G = τ and J = R.
- By (ii), σ_p(u) = V(J) = ∅, so W has no joint or generalized eigenvectors.
- Yet Ann(u) = (τ) ≠ (τ²), so u does not identify P.

The same happens for any P = τ·H with H not constant. The spectral condition sees only J. It cannot see G_u, and G_u is the only thing that decides identification, through C3-T6. Saying "u identifies P" also requires G_u ∼ P, which is exactly C3-T1(a). P4-T2 neither replaces that criterion nor recovers it. So the "spectral dichotomy" restates principality, which C3-T6 already gives, and contributes nothing to the identification problem.

The proof also has supporting defects:
- **(ii), V(J) ⊆ σ_p:** this step depends on the isomorphism in (iii), and only an aside says it is independent.
- **(v)(b), radical part:** it rests on C3-T2(a), whose status is "not audited". It also writes ℓ(∂)q_k where it means ℓ(z_k+∂)q_k. That makes the stated way of choosing ℓ wrong, because (∂_t − τ_{z_k})q_k ≠ 0 holds whenever q_k ≠ 0 and τ_{z_k} ≠ 0.
- **"Casi limite":** it says u = 0 is excluded and that I = R is admitted. These contradict each other, since I = R ⟺ u = 0.

Verdict: reject in its current form.
