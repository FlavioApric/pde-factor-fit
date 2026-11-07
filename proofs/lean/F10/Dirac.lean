import Mathlib

/-!
# Fattorizzazione Dirac / Klein–Gordon (S10-LEAN, bersaglio 2)

Claim (LEDGER Fase 8, S8-SYS): H-DIRAC, passo (C1): in rappresentazione chirale
`X = p₀ − σ·p`, `Y = p₀ + σ·p`, `XY = YX = KG · I₂`, `KG = p₀² − |p|²`; quindi
`(γ^μ p_μ)² = KG · I₄` e `(γ·p − m)(γ·p + m) = (KG − m²) · I₄`. È la premessa algebrica di
H-DIRAC(a) (`M_D ≅ (R/(KG − m²))²`), di SYS-E1/E2 e di FW-1.

Quadro: `R` anello commutativo (nel progetto `R = ℂ[p₀, p₁, p₂, p₃]`, `p_μ = i∂_μ`), `A` una
`R`-algebra (nel progetto `Mat_N(R)`). Le relazioni di Clifford si assumono in forma diagonale
(`γ_μ² = η_μ`, `γ_μγ_ν + γ_νγ_μ = 0` per `μ ≠ ν`), che copre Minkowski e Pauli.
-/

namespace PBLean.F10.Dirac

section Abstract

variable {R A : Type*} [CommRing R] [Ring A] [Algebra R A]

/-- Se gli `x_μ` anticommutano a due a due, `(Σ x_μ)² = Σ x_μ²`. -/
lemma sum_mul_self_of_anticomm {ι : Type*} [DecidableEq ι] (s : Finset ι) (x : ι → A)
    (h : ∀ μ ν, μ ≠ ν → x μ * x ν + x ν * x μ = 0) :
    (∑ μ ∈ s, x μ) * (∑ μ ∈ s, x μ) = ∑ μ ∈ s, x μ * x μ := by
  induction s using Finset.induction_on with
  | empty => simp
  | insert a s ha ih =>
    rw [Finset.sum_insert ha, Finset.sum_insert ha]
    have cross : x a * (∑ μ ∈ s, x μ) + (∑ μ ∈ s, x μ) * x a = 0 := by
      rw [Finset.mul_sum, Finset.sum_mul, ← Finset.sum_add_distrib]
      exact Finset.sum_eq_zero fun ν hν => h a ν (fun hav => ha (hav ▸ hν))
    calc (x a + ∑ μ ∈ s, x μ) * (x a + ∑ μ ∈ s, x μ)
        = x a * x a + (x a * (∑ μ ∈ s, x μ) + (∑ μ ∈ s, x μ) * x a)
            + (∑ μ ∈ s, x μ) * (∑ μ ∈ s, x μ) := by noncomm_ring
      _ = x a * x a + ∑ μ ∈ s, x μ * x μ := by rw [cross, add_zero, ih]

/-- **Clifford ⇒ Klein–Gordon.** `γ_μ² = η_μ · 1`, `γ_μγ_ν + γ_νγ_μ = 0` (`μ ≠ ν`) ⇒
`(Σ p_μ γ_μ)² = (Σ η_μ p_μ²) · 1` per ogni `p : ι → R`. -/
theorem clifford_sq {ι : Type*} [Fintype ι] [DecidableEq ι] (γ : ι → A) (η : ι → R)
    (hsq : ∀ μ, γ μ * γ μ = η μ • (1 : A))
    (hanti : ∀ μ ν, μ ≠ ν → γ μ * γ ν + γ ν * γ μ = 0) (p : ι → R) :
    (∑ μ, p μ • γ μ) * (∑ μ, p μ • γ μ) = (∑ μ, η μ * p μ ^ 2) • (1 : A) := by
  rw [sum_mul_self_of_anticomm _ _ fun μ ν hμν => by
    rw [smul_mul_smul_comm, smul_mul_smul_comm, mul_comm (p ν), ← smul_add, hanti μ ν hμν,
      smul_zero]]
  rw [Finset.sum_smul]
  refine Finset.sum_congr rfl fun μ _ => ?_
  rw [smul_mul_smul_comm, hsq, smul_smul, sq, mul_comm (p μ * p μ)]

/-- Termine di massa: `(D − m)(D + m) = D² − m²`. -/
theorem massive_factor (D : A) (m : R) :
    (D - m • (1 : A)) * (D + m • (1 : A)) = D * D - (m * m) • (1 : A) := by
  simp only [sub_mul, mul_add, mul_smul_comm, smul_mul_assoc, mul_one, one_mul, smul_smul]
  module

/-- `(a − S)(a + S) = a² − S²` e `(a + S)(a − S) = a² − S²` per `a` scalare. -/
theorem scalar_sub_mul_add (a : R) (S : A) :
    (a • (1 : A) - S) * (a • (1 : A) + S) = (a * a) • (1 : A) - S * S ∧
    (a • (1 : A) + S) * (a • (1 : A) - S) = (a * a) • (1 : A) - S * S := by
  constructor <;>
  · simp only [sub_mul, add_mul, mul_add, mul_sub, mul_smul_comm, smul_mul_assoc, mul_one,
      one_mul, smul_smul]
    module

end Abstract

/-! ## Istanza: matrici di Pauli e rappresentazione chirale -/

/-- Matrici di Pauli `σ₁, σ₂, σ₃`. -/
def pauli : Fin 3 → Matrix (Fin 2) (Fin 2) ℂ :=
  ![!![0, 1; 1, 0], !![0, -Complex.I; Complex.I, 0], !![1, 0; 0, -1]]

theorem pauli_sq (i : Fin 3) : pauli i * pauli i = (1 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  rw [one_smul]
  fin_cases i <;> ext a b <;> fin_cases a <;> fin_cases b <;>
    simp [pauli, Matrix.mul_apply, Fin.sum_univ_two]

theorem pauli_anticomm (i j : Fin 3) (hij : i ≠ j) :
    pauli i * pauli j + pauli j * pauli i = 0 := by
  fin_cases i <;> fin_cases j <;> first
    | exact absurd rfl hij
    | (ext a b <;> fin_cases a <;> fin_cases b <;>
        simp [pauli, Matrix.mul_apply, Fin.sum_univ_two])

/-- Anello dei simboli `R = ℂ[p₀, p₁, p₂, p₃]`. -/
abbrev Sym := MvPolynomial (Fin 4) ℂ

/-- `p_μ ∈ R`. -/
noncomputable abbrev p (μ : Fin 4) : Sym := MvPolynomial.X μ

/-- Pauli a coefficienti in `R`. -/
noncomputable def pauliR (i : Fin 3) : Matrix (Fin 2) (Fin 2) Sym :=
  (algebraMap ℂ Sym).mapMatrix (pauli i)

theorem pauliR_sq (i : Fin 3) : pauliR i * pauliR i = (1 : Sym) • (1 : Matrix (Fin 2) (Fin 2) Sym) := by
  rw [pauliR, ← map_mul, pauli_sq, one_smul, map_one, one_smul]

theorem pauliR_anticomm (i j : Fin 3) (hij : i ≠ j) :
    pauliR i * pauliR j + pauliR j * pauliR i = 0 := by
  rw [pauliR, pauliR, ← map_mul, ← map_mul, ← map_add, pauli_anticomm i j hij, map_zero]

/-- `σ·p = Σ_k p_k σ_k`. -/
noncomputable def sigmaDotP : Matrix (Fin 2) (Fin 2) Sym := ∑ k : Fin 3, p k.succ • pauliR k

/-- `KG = p₀² − p₁² − p₂² − p₃²`. -/
noncomputable def KG : Sym := p 0 ^ 2 - (p 1 ^ 2 + p 2 ^ 2 + p 3 ^ 2)

theorem sigmaDotP_sq : sigmaDotP * sigmaDotP = (p 1 ^ 2 + p 2 ^ 2 + p 3 ^ 2) • (1 : Matrix (Fin 2) (Fin 2) Sym) := by
  rw [sigmaDotP, clifford_sq pauliR (fun _ => 1) (fun i => pauliR_sq i) pauliR_anticomm]
  simp [Fin.sum_univ_three]

/-- `X = p₀ − σ·p`, `Y = p₀ + σ·p`. -/
noncomputable def Xc : Matrix (Fin 2) (Fin 2) Sym := p 0 • 1 - sigmaDotP
noncomputable def Yc : Matrix (Fin 2) (Fin 2) Sym := p 0 • 1 + sigmaDotP

/-- **H-DIRAC (C1).** `XY = YX = KG · I₂` in `Mat₂(ℂ[p₀, …, p₃])`. -/
theorem XY_eq_KG : Xc * Yc = KG • (1 : Matrix (Fin 2) (Fin 2) Sym) ∧
    Yc * Xc = KG • (1 : Matrix (Fin 2) (Fin 2) Sym) := by
  obtain ⟨h1, h2⟩ := scalar_sub_mul_add (p 0) sigmaDotP
  have e : (p 0 * p 0) • (1 : Matrix (Fin 2) (Fin 2) Sym) - sigmaDotP * sigmaDotP = KG • 1 := by
    rw [sigmaDotP_sq, ← sub_smul, KG]
    congr 1
    ring
  exact ⟨by rw [Xc, Yc, h1, e], by rw [Xc, Yc, h2, e]⟩

/-- Operatore di Dirac libero in rappresentazione chirale: `γ^μ p_μ = [[0, X], [Y, 0]]`. -/
noncomputable def diracChiral : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) Sym :=
  Matrix.fromBlocks 0 Xc Yc 0

/-- **Dirac² = Klein–Gordon:** `(γ^μ p_μ)² = KG · I₄`. -/
theorem diracChiral_sq :
    diracChiral * diracChiral = KG • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) Sym) := by
  rw [diracChiral, Matrix.fromBlocks_multiply, XY_eq_KG.1, XY_eq_KG.2, ← Matrix.fromBlocks_one,
    Matrix.fromBlocks_smul]
  simp

/-- **Dirac massivo:** `(γ·p − m)(γ·p + m) = (KG − m²) · I₄`. -/
theorem dirac_massive (m : Sym) :
    (diracChiral - m • 1) * (diracChiral + m • 1) =
      (KG - m * m) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) Sym) := by
  rw [massive_factor, diracChiral_sq, sub_smul]

/-- Blocco antidiagonale a entrate commutative: `[[0, x], [y, 0]]² = (x y) · I₂`. -/
theorem antidiag_sq {S : Type*} [CommRing S] (x y : S) :
    (!![0, x; y, 0] : Matrix (Fin 2) (Fin 2) S) * !![0, x; y, 0] = (x * y) • (1 : Matrix (Fin 2) (Fin 2) S) := by
  ext a b
  fin_cases a <;> fin_cases b <;> simp [Matrix.mul_apply, Fin.sum_univ_two, mul_comm]

/-- Caso 1+1: `[[0, p₀ − p₁], [p₀ + p₁, 0]]² = (p₀² − p₁²) · I₂`. -/
theorem dirac2_sq :
    (!![0, p 0 - p 1; p 0 + p 1, 0] : Matrix (Fin 2) (Fin 2) Sym) * !![0, p 0 - p 1; p 0 + p 1, 0] =
      (p 0 ^ 2 - p 1 ^ 2) • (1 : Matrix (Fin 2) (Fin 2) Sym) := by
  rw [antidiag_sq]
  congr 1
  ring

end PBLean.F10.Dirac
