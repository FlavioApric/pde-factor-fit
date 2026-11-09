# KA OP-ALG-T3 — arbitrato (Thread 2, subagente Claude fresco ae3695bfc02ca6010, 26/10/2026; letti solo KA_OPALG_T3_input.md e KA_OPALG_T3_attack.md; sintesi fedele, punti integrali)

### Point P1: (b) is circular
Verdict: partially_answered. Correct: (b)'s proof says "χ ≤ 𝒜 è la definizione"; last clause correct. Nothing false; a tautology presented as a thesis; real content of "minimum" is in (a) and (d)/(f). Severity: minor. Fix: demote (b) to a remark.

### Point P2: ordering ignores complexity; (a) adds nothing
Verdict: answered_by_current_text as mathematics; interpretive part open. Checked (a): χ ≤ 𝔇 with N = max(D, deg P) correct and computable by P4-T4(i); 𝔇 ≤ χ: search terminates exactly when Ann ≠ (P), a strict dimension gap at n gives a witness of degree ≤ n. D2 is plain oracle computability, so (a) is true as stated; but it follows almost at once from P4-T4(i),(ii), and "minimo assoluto" reads as more than computability-equivalence. Severity: minor. Fix: state in D2 and the Lettura that ≤ is uniform oracle computability without resource bound.

### Point P3: (f) proved only for ∃Ω, p₀
Verdict: answered_by_current_text for the statement of (f): the Tesi is explicitly existential ("esistono Ω ∋ 0 e p₀ = 0"). Adversary checked against D2 quantifiers: e valid (P(∂)e = 0, P̃(∂)e = κe^{⟨z₀,·⟩}, κ ≠ 0); jets match; zero answers on 𝒬∩(P̃) match; on 𝒬′ proper affine subspaces + hyperplanes c_z = 0, finitely many, cannot cover over infinite K; adaptivity by induction; χ(u′) = 0 by C3-C2; count dim R·u′ ≥ |V(Ann u′)| ≥ |supp S_F| ≥ dim S_F ≥ |F| − N₀ > B (F avoids other exponents); F chosen after B, k₀, 𝒬. No gap in (f) as stated.

### Point P4: Lettura/headline universal
Verdict: still_unresolved. The Lettura ("B è strettamente più forte se P ha almeno due fattori contati con molteplicità") drops the quantifier on (Ω, p₀); only P4-L7 (local, (−ε,ε)², p₀ = 0) is available; for other (Ω, p₀) the order is a different relation and no transfer argument is given. (a), (c), (d), (e) hold for every Ω, p₀. Severity: major (overclaim in headline, not a false theorem). Fix: add "per qualche (Ω, p₀), p. es. un quadrato piccolo attorno a 0" or prove a global analogue of P4-L7.

### Point P5: SymPy check on a different instance
Verdict: still_unresolved, cosmetic. QMIN uses the heat kernel at p₀ = (1,0), k₀ = 2, 6 operators: illustration on a different (Ω, p₀). Severity: minor. Fix: label as illustration.

## Summary
answered 2 (P2 as mathematics, P3); partially 1 (P1); unresolved 2 (P4 major, P5 minor); critical 0.

## Net assessment
No mathematical statement in T3 (a)–(f) is false or unproved as written. (a) correct but near-immediate from P4-T4(i),(ii); (b) tautology; (c),(d),(e) correct for every (Ω,p₀); (f) existential and its adversary valid. Defects are of presentation and scope: the Lettura (and summaries) drop the ∃(Ω,p₀) qualifier; "minimo assoluto" suggests more than computability-equivalence.

## Top action items
1. Rewrite the Lettura/summaries with "per qualche (Ω, p₀)" or prove a global P4-L7.
2. Demote (b) to a remark; state that ≤ is unbounded oracle computability.
3. Relabel QMIN as an illustration on a different instance.
