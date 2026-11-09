import Mathlib

/-!
# C12-P2 e C12-P3 — S5-LEAN

**Stato nel progetto:** work/C1C2/PROOF_PACKAGE.md marca C12-P2 e C12-P3 come
"prova scritta (elementare, non auditata)"; non hanno riga propria nel LEDGER v2.

C12-P2 (work/C1C2 §[C12-P2]): `P = τ² + b(ξ)τ + c(ξ)`, `b, c ∈ ℂ[ξ]`, `D := b² − 4c`.
`P` è riducibile in `R = ℂ[ξ][τ]` ⟺ `D = d²` con `d ∈ ℂ[ξ]`; allora
`P = (τ − a₊)(τ − a₋)`, `a± = (−b ± d)/2`.

C12-P3 (work/C1C2 §[C12-P3]): `P = p₁(ξ)τ − p₀(ξ)`, `p₁ ≠ 0`: `P = h(ξ)·P̃` con
`h = gcd(p₀, p₁)` e `P̃` irriducibile; per `P = τ − a(ξ)`: irriducibile (una sola componente).

Formalizzazione: `K` campo qualsiasi con `2 ≠ 0` (generalizza `ℂ`: la chiusura algebrica non
serve), `K[X]` = `K[ξ]`, `K[X][X]` = `K[ξ][τ]` (variabile esterna = τ).
"Riducibile" = "non irriducibile" (`P` ha grado 2, quindi non è un'unità).

Fuori portata (non formalizzato, dichiarato): in C12-P2 le clausole "se d ≠ 0 fattori distinti con
δ(P) = deg d; se d = 0 una sola componente primaria (τ − a)²"; in C12-P3 la descrizione delle
componenti (fattori primari di h e P̃, nuclei c(t)⊗x^l e^{ρx}) e "u₁ = u, δ = 0" per le evoluzioni.
Formalizzati: criterio di riducibilità, fattorizzazione esplicita, fattorizzazione `h·P̃` con `P̃`
irriducibile, irriducibilità di `τ − a`.
-/

namespace PBLean.C12P2

open Polynomial

variable {K : Type*} [Field K]

/-- C12-P2: `τ² + bτ + c` non irriducibile in `K[ξ][τ]` ⟺ `b² − 4c` è un quadrato in `K[ξ]`. -/
theorem quadratic_reducible_iff [NeZero (2 : K)] (b c : K[X]) :
    ¬ Irreducible (X ^ 2 + C b * X + C c : K[X][X]) ↔ ∃ d : K[X], b ^ 2 - 4 * c = d ^ 2 := by
  have h2 : (2 : K[X]) = C 2 := (map_ofNat C 2).symm
  have : NeZero (2 : K[X]) := ⟨by rw [h2]; exact C_ne_zero.mpr two_ne_zero⟩
  set P : K[X][X] := X ^ 2 + C b * X + C c with hP
  have hdeg : P.natDegree = 2 := by rw [hP]; compute_degree!
  have hmon : P.Monic := by rw [hP]; monicity!
  have hP0 : P ≠ 0 := hmon.ne_zero
  rw [hmon.irreducible_iff_roots_eq_zero_of_degree_le_three (by omega) (by omega)]
  -- radice ⟺ discriminante quadrato
  have hroot : ∀ α : K[X], P.IsRoot α ↔ discrim 1 b c = (2 * 1 * α + b) ^ 2 := by
    intro α
    rw [← quadratic_eq_zero_iff_discrim_eq_sq one_ne_zero α, IsRoot, hP]
    simp only [eval_add, eval_pow, eval_X, eval_mul, eval_C]
    ring_nf
  have hdisc : discrim 1 b c = b ^ 2 - 4 * c := by unfold discrim; ring
  constructor
  · intro h
    obtain ⟨α, hα⟩ := Multiset.exists_mem_of_ne_zero h
    rw [mem_roots hP0, hroot, hdisc] at hα
    exact ⟨2 * 1 * α + b, hα⟩
  · rintro ⟨d, hd⟩ h0
    let α : K[X] := C (2⁻¹ : K) * (d - b)
    have hα : 2 * 1 * α + b = d := by
      have : (2 : K[X]) * C (2⁻¹ : K) = 1 := by
        rw [h2, ← C_mul, mul_inv_cancel₀ two_ne_zero, C_1]
      simp only [α, mul_one]
      linear_combination (d - b) * this
    have : α ∈ P.roots := by
      rw [mem_roots hP0, hroot, hdisc, hα, hd]
    rw [h0] at this
    simp at this

/-- C12-P2, fattorizzazione esplicita: se `b² − 4c = d²`, allora
`τ² + bτ + c = (τ − a₊)(τ − a₋)` con `a± = (−b ± d)/2`. -/
theorem quadratic_factor [NeZero (2 : K)] (b c d : K[X]) (hd : b ^ 2 - 4 * c = d ^ 2) :
    (X ^ 2 + C b * X + C c : K[X][X]) =
      (X - C (C (2⁻¹ : K) * (-b + d))) * (X - C (C (2⁻¹ : K) * (-b - d))) := by
  have hi : (2 : K[X]) * C (2⁻¹ : K) = 1 := by
    rw [show (2 : K[X]) = C 2 from (map_ofNat C 2).symm, ← C_mul, mul_inv_cancel₀ two_ne_zero, C_1]
  have hb : C (2⁻¹ : K) * (-b + d) + C (2⁻¹ : K) * (-b - d) = -b := by
    linear_combination (-b) * hi
  have hc : C (2⁻¹ : K) * (-b + d) * (C (2⁻¹ : K) * (-b - d)) = c := by
    linear_combination (C (2⁻¹ : K) * C (2⁻¹ : K)) * hd + c * (2 * C (2⁻¹ : K) + 1) * hi
  have e1 : C b = -(C (C (2⁻¹ : K) * (-b + d)) + C (C (2⁻¹ : K) * (-b - d))) := by
    rw [← C_add, hb, C_neg, neg_neg]
  have e2 : C c = C (C (2⁻¹ : K) * (-b + d)) * C (C (2⁻¹ : K) * (-b - d)) := by
    rw [← C_mul, hc]
  rw [e1, e2]
  ring

/-- C12-P3, caso evolutivo: `τ − a(ξ)` è irriducibile in `K[ξ][τ]`. -/
theorem X_sub_C_irreducible (a : K[X]) : Irreducible (X - C a : K[X][X]) :=
  irreducible_X_sub_C a

/-- C12-P3, caso generale: `p₁(ξ)τ − p₀(ξ) = h(ξ)·P̃` con `h = gcd(p₁, p₀)` e `P̃` irriducibile. -/
theorem first_order_factor [DecidableEq K] (p₀ p₁ : K[X]) (hp₁ : p₁ ≠ 0) :
    ∃ P' : K[X][X], (C p₁ * X - C p₀ : K[X][X]) = C (gcd p₁ p₀) * P' ∧ Irreducible P' := by
  obtain ⟨a, b, ha, hb, hu⟩ := extract_gcd p₁ p₀
  refine ⟨C a * X + C (-b), ?_, ?_⟩
  · rw [show (C p₁ * X - C p₀ : K[X][X]) = C (gcd p₁ p₀ * a) * X - C (gcd p₁ p₀ * b) by
      rw [← ha, ← hb]]
    simp only [C_mul, C_neg]
    ring
  · apply irreducible_C_mul_X_add_C
    · rintro rfl
      exact hp₁ (by rw [ha, mul_zero])
    · exact (gcd_isUnit_iff_isRelPrime.mp hu).neg_right

end PBLean.C12P2
