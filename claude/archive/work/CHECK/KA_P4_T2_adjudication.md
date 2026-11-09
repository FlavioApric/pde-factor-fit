# Kill-argument P4-T2 — Thread 2 (arbitrato), subagente Claude fresco acc5928ba08659033, 26/10/2026
Input dato al revisore: solo `KA_P4_T2_input.md` e `KA_P4_T2_attack.md` (nessun altro contesto, nessun file scritto dal revisore). Testo dell'arbitrato riportato verbatim sotto; verdetto calcolato da S-CHECK-6 con la tabella della skill kill-argument (non dal revisore).

## Verdetto calcolato
Conteggi: answered_by_current_text 2 (P2, P4) · partially_answered 3 (P1 major, P3 major, P5 minor) · still_unresolved 2 (P6 minor, P7 minor).
Riga della tabella: ≥1 still_unresolved a severità major/minor, nessun critical ⇒ **WARN** (`reason_code: unresolved_major_or_minor`).
Lettura di S-CHECK-6: nessun punto critico; l'enunciato matematico (v)(a) regge (il controesempio u = e^{x²}, P = τ² confuta solo l'etichetta "u identifica ⟺ nessun autovettore", non la tesi, che è a una direzione). Fix richiesti: KA-T2-1 (titolo/etichetta + frase "Ann(u) = (P) ⟺ σ_p = ∅ e G_u ∼ P"), KA-T2-2 (ℓ(∂)q_k → ℓ(z_k+∂)q_k), KA-T2-3 (casi limite u = 0 ⟺ I = R), KA-T2-4 (inlinare C3-T2(a) da C3-L3(a),(b)). Riportati in AUDIT_P4.md.

---
## Arbitrato (verbatim)
### Point P1: Headline biconditional "u identifies ⟺ no eigenvectors" is false
**Attack claim**: The headline result claims "Ann(u) = (P) ⟺ W has no joint eigenvectors". Only "Ann principal ⟺ σ_p = ∅" is proved, so only "identifies ⇒ no eigenvectors" holds.
**Verdict**: partially_answered
**Evidence (or lack of)**: The theorem itself does not make the biconditional claim. (v)(a), line 38, states "Ann(u) principale ⟺ J = R ⟺ σ_p(u) = ∅ ⟺ W ∩ EP = 0". The identification clause is explicitly one-way: "In particolare, se u identifica (Ann(u) = (P), P non costante), W non ha autovettori congiunti né generalizzati". However, the file's own title line (line 1) labels the result "dicotomia 'u identifica ⟺ nessun autovettore'". The section heading "Dicotomia" in (v) also invites that reading. The mathematical statement is correct. The label attached to it overclaims, and the attack quotes the label accurately.
**Severity if unresolved**: major (headline overclaim, but the fix is one line; the body is correct)
**If unresolved, recommended fix**: Change the title and the (v) heading to "dicotomia 'Ann(u) principale ⟺ nessun autovettore'; identificazione ⇒ nessun autovettore (non viceversa)".

### Point P2: Counterexample u = e^{x²}, P = τ²
**Attack claim**: With u = e^{x²} on (0,1)×(−1,1) and P = τ², u has no eigenvectors but Ann(u) = (τ) ≠ (τ²). So "no eigenvectors ⇒ identifies P" fails.
**Verdict**: answered_by_current_text
**Evidence (or lack of)**: My check confirms the counterexample. ∂_t u = 0, so Q(∂)u = Q(0,∂_x)e^{x²}. A nonzero constant-coefficient ODE in x annihilating e^{x²} would force it to be EP, which it is not, because the degree of ∂_x^k e^{x²}/e^{x²} grows without bound. So Ann = (τ), G = τ, J = R, σ_p = ∅, and P(∂)u = ∂_t²u = 0. Ann ≠ (τ²).
This is fully consistent with (v)(a): Ann is principal and σ_p = ∅. It refutes only the converse "σ_p = ∅ ⇒ Ann = (P)", which the theorem text never asserts. It does confirm that the line-1 label is wrong (see P1).
**Severity if unresolved**: n/a
**If unresolved, recommended fix**: n/a (optionally add it as a remark showing the converse fails).

### Point P3: The spectral dichotomy restates C3-T6 and adds nothing for identification
**Attack claim**: The spectral condition sees only J, never G_u. Identification needs G_u ∼ P (C3-T1(a)/C3-T6). P4-T2 neither replaces nor recovers that criterion, so it contributes nothing.
**Verdict**: partially_answered
**Evidence (or lack of)**: The observation is correct. Identification of P means Ann principal and G_u ∼ P. σ_p detects only V(J) (ii), and (iv) shows the "continuous" part R/(G) has no eigenvectors at all. So spectral data cannot tell G_u apart from P.
The text does not claim to recover C3-T1(a). Its contribution is real but limited:
- a spectral and EP characterization of principality, σ_p = ∅ ⟺ W ∩ EP = 0, beyond C3-T6's "G_u(∂)u = 0";
- the structure results (iii) and (iv).

This is a framing and scope issue. The position is sustainable only if the result is presented as a structure theorem for the cyclic module plus a *necessary* spectral condition for identification. Presented as an identification criterion, it does not hold up. Nothing in the text says explicitly that identification additionally requires G_u ∼ P.
**Severity if unresolved**: major (as currently headlined)
**If unresolved, recommended fix**: Add one sentence after (v)(a): "Ann(u) = (P) ⟺ σ_p(u) = ∅ e G_u ∼ P; la condizione spettrale non vede G_u (es. u = e^{x²}, P = τ²)".

### Point P4: V(J) ⊆ σ_p depends on the isomorphism of (iii)
**Attack claim**: Step (ii), V(J) ⊆ σ_p, uses the isomorphism R/J ≅ R·G(∂)u from (iii). Its independence is asserted only in an aside.
**Verdict**: answered_by_current_text
**Evidence (or lack of)**: I checked the proof of (iii) on line 51. (⊇) uses Ann(G(∂)u) = (I : G) = J and C3-L3. (⊆) uses Fact (F) and primality. The isomorphism uses only surjectivity and the kernel J. None of these uses V(J) ⊆ σ_p.
The only use of (ii) in (iii) is the "generalized eigenvectors are EP" clause, which is the eigenvector-form part of (ii) and is proved independently on line 48. So the aside "(la cui prova non usa questo passo)" is true and there is no circularity.
The step itself is correct. v̄ ≠ 0 in R/J, so (vG)(∂)u ≠ 0. (τ−τ_z)v ∈ J gives ((τ−τ_z)vG)(∂)u ∈ (GJ)(∂)u = 0, and the same holds for ξ. This is an ordering and presentation issue only. The dependency map's "(iii) ← (ii)" is slightly imprecise but not wrong.
**Severity if unresolved**: n/a (at most minor: the step could be moved after (iii))
**If unresolved, recommended fix**: n/a

### Point P5: (v)(b) radical clause rests on C3-T2(a), which is unaudited
**Attack claim**: The radical/diagonal characterization in (v)(b) depends on C3-T2(a), whose status is "not audited".
**Verdict**: partially_answered
**Evidence (or lack of)**: The dependency is real, and the text discloses it: "C3-T2(a) [prova scritta, non auditata; usata solo in P4-T2(v)(b)]" (line 15).
The fact itself is immediate from audited lemmas. By C3-L3(a), Q(∂)u = Σ_k (Q(z_k+∂)q_k)e^{⟨z_k,·⟩}. By C3-L3(b), this vanishes iff every coefficient vanishes. So the risk is negligible. Still, the text discloses the gap without closing it, although closing it takes two lines.
**Severity if unresolved**: minor
**If unresolved, recommended fix**: Inline the two-line derivation from C3-L3(a),(b) in (v)(b) and drop the dependence on unaudited C3-T2(a).

### Point P6: ℓ(∂)q_k should be ℓ(z_k+∂)q_k
**Attack claim**: (v)(b) writes ℓ(∂)q_k where ℓ(z_k+∂)q_k is meant. The stated choice of ℓ is therefore wrong, since (∂_t−τ_{z_k})q_k ≠ 0 whenever q_k ≠ 0 and τ_{z_k} ≠ 0.
**Verdict**: still_unresolved
**Evidence (or lack of)**: Line 54 reads "scegliamo ℓ ∈ {τ−τ_{z_k}, ξ−ξ_{z_k}} con ℓ(∂)q_k ≠ 0" and then "Q(z_k+∂)q_k = [∏_{j≠k}ℓ_j(z_k+∂)]ℓ(∂)q_k".
The correct factor is ℓ(z_k+∂), which equals ∂_t or ∂_x. As written, ℓ(∂) = ∂_t − τ_{z_k}, so the displayed identity is false. The selection condition is also vacuous when τ_{z_k} ≠ 0: by the degree argument, ℓ(∂)q_k ≠ 0 for any nonzero q_k. The attack is right on both counts.
With ℓ(z_k+∂), the argument is correct:
- q_k non-constant gives ∂_tq_k ≠ 0 or ∂_xq_k ≠ 0;
- ∏ℓ_j(z_k+∂) = c + (degree-lowering operator), with c ≠ 0, is invertible on polynomials;
- Q ∈ ∩_j 𝔪_{z_j} = √I but Q ∉ I.

So the conclusion stands, but the written step is wrong.
**Severity if unresolved**: minor (notational slip with a correct intended proof, but a displayed equation is false)
**If unresolved, recommended fix**: Replace both occurrences of ℓ(∂)q_k with ℓ(z_k+∂)q_k (that is, ∂_tq_k or ∂_xq_k) and choose ℓ by the condition that this derivative is nonzero.

### Point P7: "Casi limite" contradiction about u = 0 and I = R
**Attack claim**: "Casi limite" says u = 0 is excluded and that I = R is admitted. These contradict each other because I = R ⟺ u = 0.
**Verdict**: still_unresolved
**Evidence (or lack of)**: Line 58 reads "u = 0 è escluso (I = R ≠ 0 è ammesso: G ∼ 1, J = R, W = 0 ...)".
I = R ⟺ 1(∂)u = 0 ⟺ u = 0, so the sentence contradicts itself. The hypotheses (u ∈ D′, I ≠ 0) do not exclude u = 0, and the degenerate case is mathematically coherent: everything is empty or zero. Only the wording is wrong.
**Severity if unresolved**: minor
**If unresolved, recommended fix**: Rewrite as "u = 0 (⟺ I = R) è ammesso dalle ipotesi ed è banale: G ∼ 1, J = R, W = 0, tutti gli insiemi vuoti".

## Summary
Total rejection points: 7
- answered_by_current_text: 2 (P2, P4)
- partially_answered: 3 (P1, P3, P5)
- still_unresolved: 2 (P6, P7)

## Net assessment
The attack's headline claim is right about the file's label but wrong about the theorem. P4-T2 (v)(a) states exactly "principal ⟺ σ_p = ∅", and states identification ⇒ no eigenvectors in one direction only. The e^{x²}, τ² counterexample is mathematically correct, but it refutes only the "u identifica ⟺ nessun autovettore" label on line 1.
The substantive criticism is about framing, and it holds. Spectral data cannot see G_u, so P4-T2 gives only a necessary condition for identification plus a spectral characterization of principality. Presented as an identification dichotomy, it overclaims.
None of the proof defects is critical. I found no circularity in V(J) ⊆ σ_p. The C3-T2(a) dependency is disclosed and trivially closable. Two wording errors remain unfixed: the ℓ(∂)/ℓ(z_k+∂) slip, which makes one displayed identity false although the intended argument is correct, and the self-contradictory u = 0 limit-case sentence.
I found no step in which the theorem as stated is false or its main step is unproved.

## Top action items (max 3)
1. Retitle the result and the (v) heading so they say "Ann(u) principal ⟺ no eigenvectors". State explicitly that Ann(u) = (P) ⟺ σ_p = ∅ and G_u ∼ P, and cite u = e^{x²}, P = τ² as the example showing the converse of the identification clause fails.
2. In (v)(b), replace ℓ(∂)q_k with ℓ(z_k+∂)q_k (∂_tq_k or ∂_xq_k) in both places, and inline the two-line proof of C3-T2(a) from C3-L3(a),(b).
3. Fix the "Casi limite" sentence: u = 0 ⟺ I = R is admitted and trivial.
