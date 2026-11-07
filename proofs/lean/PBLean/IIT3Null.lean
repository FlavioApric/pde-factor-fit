import Mathlib

/-!
# II-T3 (i) ⟺ (ii) = C12-L3(c) — S5-LEAN (bersaglio facoltativo)

Claim (work/II/PROOF_PACKAGE.md §[II-T3], (i) ⟺ (ii), "Nullstellensatz debole";
work/C1C2/PROOF_PACKAGE.md §[C12-L3](c)): per `P₁, P₂ ∈ R = ℂ[τ, ξ]`:
`(P₁, P₂) = R ⟺ V(P₁) ∩ V(P₂) = ∅` in `ℂ²`.

Formalizzazione: `K` campo algebricamente chiuso, `σ` insieme finito di variabili
(il caso del progetto è `K = ℂ`, `σ = Fin 2`, istanza `ii_t3_i_iff_ii_C2`).
Prova: Nullstellensatz di Mathlib (ideali massimali = `vanishingIdeal {x}`).
C12-L3(c) nel package richiede `f, g ≠ 0`: qui l'ipotesi non serve (l'enunciato vale per ogni coppia).
-/

namespace PBLean.IIT3Null

open MvPolynomial

theorem span_pair_eq_top_iff_no_common_zero {K σ : Type*} [Field K] [IsAlgClosed K] [Finite σ]
    (P₁ P₂ : MvPolynomial σ K) :
    Ideal.span ({P₁, P₂} : Set (MvPolynomial σ K)) = ⊤ ↔
      ¬ ∃ x : σ → K, eval x P₁ = 0 ∧ eval x P₂ = 0 := by
  constructor
  · rintro htop ⟨x, h1, h2⟩
    have hle : Ideal.span ({P₁, P₂} : Set (MvPolynomial σ K)) ≤ RingHom.ker (eval x) := by
      rw [Ideal.span_le]
      rintro p (rfl | rfl)
      · exact h1
      · exact h2
    rw [htop, top_le_iff] at hle
    have : (1 : MvPolynomial σ K) ∈ RingHom.ker (eval x) := by rw [hle]; trivial
    simp at this
  · intro hno
    by_contra hne
    obtain ⟨M, hM, hle⟩ := Ideal.exists_le_maximal _ hne
    obtain ⟨x, rfl⟩ := (MvPolynomial.isMaximal_iff_eq_vanishingIdeal_singleton).mp hM
    apply hno
    refine ⟨x, ?_, ?_⟩
    · have := hle (Ideal.subset_span (by simp : P₁ ∈ ({P₁, P₂} : Set _)))
      rw [mem_vanishingIdeal_singleton_iff] at this
      simpa [MvPolynomial.coe_aeval_eq_eval] using this
    · have := hle (Ideal.subset_span (by simp : P₂ ∈ ({P₁, P₂} : Set _)))
      rw [mem_vanishingIdeal_singleton_iff] at this
      simpa [MvPolynomial.coe_aeval_eq_eval] using this

/-- Caso del progetto: `R = ℂ[τ, ξ]` (`MvPolynomial (Fin 2) ℂ`), zeri in `ℂ²`. -/
theorem ii_t3_i_iff_ii_C2 (P₁ P₂ : MvPolynomial (Fin 2) ℂ) :
    Ideal.span ({P₁, P₂} : Set (MvPolynomial (Fin 2) ℂ)) = ⊤ ↔
      ¬ ∃ x : Fin 2 → ℂ, eval x P₁ = 0 ∧ eval x P₂ = 0 :=
  span_pair_eq_top_iff_no_common_zero P₁ P₂

end PBLean.IIT3Null
