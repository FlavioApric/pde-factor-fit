import Mathlib

/-!
# II-P5, caso k = 2 — S5-LEAN

Claim (LEDGER riga II-P5, DIMOSTRATO; work/II/PROOF_PACKAGE.md §[II-P5](c), equivalenza
(1) ⟺ (4) per k = 2, [fix II-P5-F1]): la compagna `C` di `p(s) = s² + p₁ s + p₀` (ξ fissato) è
normale ⟺ `|p₀| = 1` e `p̄₀ p₁ = −p̄₁`.

Convenzione del package: `C = [[0, 1], [−p₀, −p₁]]` (`C v(λ) = λ v(λ)`, `v(λ) = (1, λ)`).
Calcolo: `C Cᴴ − Cᴴ C = [[1 − |p₀|², −p₁p̄₀ − p̄₁], [−p₀p̄₁ − p₁, |p₀|² − 1]]`.
-/

namespace PBLean.IIP5

open Matrix ComplexConjugate

/-- Matrice compagna di `s² + p₁ s + p₀` nella convenzione del package. -/
def companion2 (p₀ p₁ : ℂ) : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; -p₀, -p₁]

/-- II-P5 (k = 2): `C Cᴴ = Cᴴ C ⟺ ‖p₀‖ = 1 ∧ conj p₀ · p₁ = −conj p₁`. -/
theorem companion2_normal_iff (p₀ p₁ : ℂ) :
    companion2 p₀ p₁ * (companion2 p₀ p₁)ᴴ = (companion2 p₀ p₁)ᴴ * companion2 p₀ p₁ ↔
      ‖p₀‖ = 1 ∧ conj p₀ * p₁ = -conj p₁ := by
  have hn : conj p₀ * p₀ = ((‖p₀‖ : ℝ) : ℂ) ^ 2 := Complex.conj_mul' p₀
  constructor
  · intro h
    have h00 := congrFun (congrFun h 0) 0
    have h01 := congrFun (congrFun h 0) 1
    simp [companion2, Matrix.mul_apply, Fin.sum_univ_two] at h00 h01
    refine ⟨?_, ?_⟩
    · have h2 : ((‖p₀‖ : ℝ) : ℂ) ^ 2 = 1 := by
        rw [← hn]; linear_combination -h00
      have h3 : ‖p₀‖ ^ 2 = 1 := by exact_mod_cast h2
      have h4 : 0 ≤ ‖p₀‖ := norm_nonneg _
      nlinarith [h3, h4]
    · linear_combination -h01
  · rintro ⟨h0, h1⟩
    have hn1 : conj p₀ * p₀ = 1 := by rw [hn, h0]; simp
    have hn2 : p₀ * conj p₀ = 1 := by rw [mul_comm]; exact hn1
    have h1' : p₀ * conj p₁ = -p₁ := by
      have := congrArg conj h1
      simpa using this
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [companion2, Matrix.mul_apply, Fin.sum_univ_two] <;>
      first
        | linear_combination -hn1
        | linear_combination -h1
        | linear_combination h1'
        | linear_combination hn2
        | linear_combination -hn2
        | linear_combination hn1
        | linear_combination h1
        | linear_combination -h1'

/-- Forma con `IsStarNormal` (definizione di Mathlib: `Cᴴ` commuta con `C`). -/
theorem companion2_isStarNormal_iff (p₀ p₁ : ℂ) :
    IsStarNormal (companion2 p₀ p₁) ↔ ‖p₀‖ = 1 ∧ conj p₀ * p₁ = -conj p₁ := by
  rw [← companion2_normal_iff, isStarNormal_iff, Commute, SemiconjBy, Matrix.star_eq_conjTranspose]
  exact ⟨fun h => h.symm, fun h => h.symm⟩

end PBLean.IIP5
