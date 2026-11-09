# Kill-argument P4-T5 — Thread 2 (arbitrato), subagente Claude fresco af6b3674785288ffb, 26/10/2026
Input dato al revisore: solo `KA_P4_T5_input.md` e `KA_P4_T5_attack.md` (nessun altro contesto, nessun file scritto dal revisore). Testo dell'arbitrato riportato verbatim sotto; verdetto calcolato da S-CHECK-6 con la tabella della skill kill-argument (non dal revisore).

## Verdetto calcolato
Conteggi: answered_by_current_text 1 (P_4) · partially_answered 2 (P_1 major, P_3 minor) · still_unresolved 2 (P_2 major, P_5 major).
Riga della tabella: ≥1 still_unresolved a severità major, nessun critical ⇒ **WARN** (`reason_code: unresolved_major_or_minor`).
Lettura di S-CHECK-6: l'enunciato di P4-T5 (condizionale a un u dato con Ann(u) = (P)) è corretto, nessun passo errato (attaccante e arbitro concordano). I punti non risolti colpiscono la *Lettura* (cornice), non il teorema: "esattamente" non è provato (manca il viceversa) e B non è il dato minimo (basta un maggiorante del grado di un testimone); "il maggiorante non si può eliminare" ha contenuto per un P dato solo se esiste un u ammissibile con Ann(u) = (P) e jet in K = ℚ̄ (manca un lemma di esistenza; nel caso C8 la normalizzazione 1/√(4π) del nucleo del calore non sta in ℚ̄: va tolta). Fix: KA-T5-1 (Lettura: togliere "esattamente", B sufficiente non minimo), KA-T5-2 (esistenza di u ammissibile, oppure restringere la Lettura ai P per cui è esibito; C8 con u = t^{-1/2}e^{-x²/(4t)}), KA-T5-3 (rinominare l'ordine del jet K → k₀). Riportati in AUDIT_P4.md.

---
## Arbitrato (verbatim)
## Adjudication: hostile memo against P4-T5 and the "Lettura" of P4-T4

I read both files in full and checked P4-T5 Passi 1–5 myself. I agree with the attacker's opening concession. Passo 2's claim V_K^⊥ = (P) ∩ R_{≤K} is sound, and the jet span is closed under derivation because the g_{i,z,j} use every j < e_i. In Passo 3 the kernel has a K-basis. In Passo 4, Q(∂)v_λ is affine in λ and each H_Q is proper, and a finite union of proper affine subspaces cannot cover K^n when K is infinite. Passo 5 handles adaptive queries correctly. Edge cases are also fine. If 𝒬′ = ∅, then v = v₁. If v₁ = 0, then Ann(0) = R ⊋ (P), so the conclusion still holds. That concession is not a rejection point. The memo makes the following five.

### Point P_1: "esattamente" is unsupported (no converse)
**Attack claim**: The Lettura says C3-Q1 reduces "esattamente" to knowing a bound B ≥ dim(R·u ∩ EP). Only sufficiency is proved: nothing shows that a decider for "Ann = (P)" yields B.
**Verdict**: partially_answered
**Evidence (or lack of)**: P4-T4(iii) proves only one direction: given B, the problem is decidable. Neither P4-T4 nor P4-T5 proves that a decider produces B. My own check: a decider recovers B only on "yes" instances. If Ann(u) = (P), then G_u = P, J_u = R and dim R/J_u = 0, so B = 0. On "no" instances, a decider plus the semi-decision of (ii) finds one witness, but that gives no bound on dim R/J_u. So "esattamente" (an equivalence of information) is not established. This is a framing choice confined to the Lettura, not to the theorem itself. As written it cannot be sustained. Read as "si riduce a" (sufficiency) it is sustainable.
**Severity if unresolved**: major (the headline framing overclaims)
**If unresolved, recommended fix**: Replace "si riduce esattamente a" with "si riduce a (condizione sufficiente)", or add and prove a precise statement of what a decider does and does not yield.

### Point P_2: B is not the minimal datum; weaker information suffices
**Attack claim**: B could be replaced by strictly weaker information, such as a degree bound for one witness h·P/P_i. P4-T5 is consistent with both answers.
**Verdict**: still_unresolved
**Evidence (or lack of)**: The attacker is right. The proof of (iii) uses B only to get deg h ≤ d_i ≤ B, and from that deg Q ≤ N. Any integer D that is at least the minimal degree of some element of Ann(u)∖(P) (when one exists) suffices: compute Ann(u) ∩ R_{≤D} by (i) and compare dimensions. D carries the same information as the decision bit, since a decider plus (ii) produces it. B carries more: it also gives G_u and V(Ann u). The text never discusses whether B is minimal, and P4-T5 cannot separate B from D. This undercuts the "esattamente" framing of P_1.
**Severity if unresolved**: major
**If unresolved, recommended fix**: Add a remark that (iii) needs only a bound on the degree of one witness. Say that B is the natural datum for the stronger outputs (G_u, V(Ann u)), not the minimal one for the decision.

### Point P_3: P4-T5 does not show "il maggiorante non si può eliminare"
**Attack claim**: P4-T5 does not prove that the bound cannot be eliminated.
**Verdict**: partially_answered
**Evidence (or lack of)**: On the literal reading, the attack is wrong. P4-T5 shows that the bare oracle model (J + Z), with no extra datum, admits no correct decider on {u} ∪ E_P^K. So deleting B without replacing it does produce impossibility, and the Portata ("riguarda il modello a scatola nera") scopes this correctly. What P4-T5 does not show is that B specifically, as opposed to some substitute datum, is indispensable. The sentence is sustainable if it means "non si può eliminare senza sostituirlo con altra informazione". It is not sustainable as a claim that B is necessary. This also depends on P_5: the impossibility needs a u with Ann(u) = (P).
**Severity if unresolved**: minor
**If unresolved, recommended fix**: Reword to "senza un dato aggiuntivo (come B) il problema non è decidibile nel modello M2⁺".

### Point P_4: Generic, trivial adversary argument that "applies to any extra datum"
**Attack claim**: This is a standard finite-information density argument. A co-semi-decidable property that is not semi-decidable cannot be decided from finite observations. The argument applies to any extra datum and singles out none. The result is correct but trivial.
**Verdict**: answered_by_current_text
**Evidence (or lack of)**: The claim that the argument "applies to any extra datum" is false. With B supplied, P4-T4(iii) makes the problem decidable. In fact the adversaries v ∈ E_P^K are told apart by B itself: for u, dim(R·u ∩ EP) = 0, while for a nonzero v ∈ EP this dimension is at least 1. So the argument does not transfer to B. The appeal to a "generic fact" is also circular. That the property is not semi-decidable is exactly what has to be proved, and the proof is the density content of Passi 2–4, specifically V_K^⊥ = (P) ∩ R_{≤K} with witnesses in K². "Trivial" is a judgement of significance, not a defect. The text makes no depth claim, and its Portata limits the scope.
**Severity if unresolved**: minor
**If unresolved, recommended fix**: n/a. Optionally, state explicitly that the adversary family is ruled out once B is supplied, to block this misreading.

### Point P_5: Existence of a u with Ann(u) = (P) is unproved, so the result may be vacuous
**Attack claim**: The "for every P" scope rests on an unproved existence claim. Apart from the heat example (C8), no real-analytic u with jets in Q̄ and Ann(u) = (P) is shown to exist. Where none exists, the result is vacuous.
**Verdict**: still_unresolved
**Evidence (or lack of)**: The theorem is stated conditionally: u is a hypothesis, so it is not false. The point still matters, more than the attacker says. Suppose that for some P no admissible u (analytic, jets in K, Ann(u) = (P)) exists. Then on the M2⁺ input class every u satisfies Ann(u) ≠ (P), the constant algorithm "no" is correct, and the problem is decidable for that P. So the Lettura's "non si può eliminare" holds for a given P only once such a u exists. The text gives no existence lemma. The only instance is C8 ("u = G in (1,0)"), and its K-membership is not visible here: the heat kernel's normalisation 1/√(4π) is not in Q̄ unless it is dropped. A plausible route exists. Cauchy–Kovalevskaya, after a K-linear change of variables that makes P non-characteristic, with rational Cauchy data gives jets in K. One would then still need to verify w_i ∉ EP for every i (C3-T1(a)). None of this is in the text.
**Severity if unresolved**: major
**If unresolved, recommended fix**: Add a lemma constructing, for every non-constant P ∈ K[τ,ξ], an admissible u with Ann(u) = (P) (for example via Cauchy–Kovalevskaya with rational data, checking w_i ∉ EP). Alternatively, restrict the Lettura's claim explicitly to those P for which such a u exists, and confirm that the C8 u has jets in K.

## Summary
Total rejection points: 5
- answered_by_current_text: 1 (P_4)
- partially_answered: 2 (P_1, P_3)
- still_unresolved: 2 (P_2, P_5)

## Net assessment
P4-T5 as stated (conditional on a given u) is correct: I found no faulty step, and the attacker found none either. The memo's claim that the argument is generic and works against any datum is mathematically wrong, because B does break the adversary. The valid objections are aimed at the framing.

First, "esattamente" claims an equivalence that is never proved, and B is demonstrably not the minimal datum: a witness-degree bound suffices. Second, the impossibility, and with it "il maggiorante non si può eliminare", is meaningful for a given P only if an admissible u with Ann(u) = (P) exists, and the text proves this nowhere in general. The second gap is substantive: without existence, the problem is trivially decidable for that P.

A minor wording issue: the letter K is used both for the field ℚ̄ and for the jet order "K ∈ ℕ", which makes "K-jet" ambiguous.

## Top action items (max 3)
1. Prove an existence lemma: for every non-constant P ∈ K[τ,ξ], some u that is real-analytic, has jets in K and satisfies Ann(u) = (P). Otherwise restrict P4-T5's interpretation to the P where such a u is exhibited, and check that the C8 instance has jets in K.
2. Rewrite the Lettura. Drop "esattamente", state that B is sufficient but not minimal (a bound on the degree of one witness already decides "Ann = (P)"), and phrase the impossibility as "senza dato aggiuntivo nel modello M2⁺".
3. Rename the jet order in P4-T5 (for example to k₀) so it no longer clashes with the field K = ℚ̄.
