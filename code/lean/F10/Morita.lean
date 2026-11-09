import Mathlib
import PBLean.F10.Comax

/-!
# Nuclei per moduli su Mat_k(R) (S10-LEAN, bersaglio 1)

Claim (LEDGER Fase 8, S8-SYS): il quadro dei sistemi, `Sol_𝒜(P) ≅ Hom_R(M_P, 𝒜)` con
`M_P = R^{1×k}/R^{1×ℓ}P` (isomorfismo di Malgrange, usato in SYS-T1, SYS-EX, SYS-S1), e il passo
algebrico di SYS-C1 / CONV-MZ1: `P u = 0 ⇒ (det P) u = 0` (adjugata).
Inoltre II-T3 per operatori matriciali che commutano (azione di `Mat_k(R)` su `M^k`).

Quadro: `R` anello commutativo (nel progetto `ℂ[τ, ξ]`), `M` un `R`-modulo qualsiasi
(`C^∞(Ω)`, `𝒟′(Ω)`), `P ∈ Mat_{ℓ×k}(R)` agisce su `M^k` con `(P u)_i = Σ_j P_ij • u_j`.
-/

namespace PBLean.F10.Morita

open PBLean.F10

variable {R M : Type*} [CommRing R] [AddCommGroup M] [Module R M]
variable {k l m : Type*} [Fintype k] [Fintype l]

/-- Azione di `P ∈ Mat_{ℓ×k}(R)` su `M^k`: `(P u)_i = Σ_j P_ij • u_j`. -/
def matOp (P : Matrix l k R) : (k → M) →ₗ[R] (l → M) where
  toFun u i := ∑ j, P i j • u j
  map_add' u v := by
    funext i
    simp only [Pi.add_apply, smul_add, Finset.sum_add_distrib]
  map_smul' c u := by
    funext i
    simp only [Pi.smul_apply, RingHom.id_apply, Finset.smul_sum]
    exact Finset.sum_congr rfl fun j _ => smul_comm _ _ _

lemma matOp_apply (P : Matrix l k R) (u : k → M) (i : l) :
    matOp P u i = ∑ j, P i j • u j := rfl

lemma matOp_mul_apply [Fintype m] (P : Matrix m l R) (Q : Matrix l k R) (u : k → M) :
    matOp (P * Q) u = matOp P (matOp Q u) := by
  funext i
  simp only [matOp_apply, Matrix.mul_apply, Finset.sum_smul, Finset.smul_sum, mul_smul]
  exact Finset.sum_comm

lemma matOp_smul_apply (c : R) (P : Matrix l k R) (u : k → M) :
    matOp (c • P) u = c • matOp P u := by
  funext i
  simp only [matOp_apply, Matrix.smul_apply, smul_eq_mul, mul_smul, Pi.smul_apply,
    Finset.smul_sum]

lemma matOp_add_apply (P Q : Matrix l k R) (u : k → M) :
    matOp (P + Q) u = matOp P u + matOp Q u := by
  funext i
  simp only [matOp_apply, Matrix.add_apply, add_smul, Finset.sum_add_distrib, Pi.add_apply]

lemma matOp_one_apply [DecidableEq k] (u : k → M) : matOp (1 : Matrix k k R) u = u := by
  funext i
  simp [matOp_apply, Matrix.one_apply, ite_smul]

/-- `Mat_k(R) → End_R(M^k)` è un omomorfismo di anelli: `M^k` è un `Mat_k(R)`-modulo. -/
def matEnd [DecidableEq k] : Matrix k k R →+* Module.End R (k → M) where
  toFun := matOp
  map_one' := LinearMap.ext matOp_one_apply
  map_mul' P Q := LinearMap.ext (matOp_mul_apply P Q)
  map_zero' := LinearMap.ext fun u => by funext i; simp [matOp_apply]
  map_add' P Q := LinearMap.ext (matOp_add_apply P Q)

/-- `Sol_M(P) := {u ∈ M^k | P u = 0}`. -/
abbrev Sol (P : Matrix l k R) : Submodule R (k → M) := LinearMap.ker (matOp P)

/-! ## Isomorfismo di Malgrange `Sol_M(P) ≅ Hom_R(R^{1×k}/R^{1×ℓ}P, M)` -/

/-- Accoppiamento riga–colonna: `u ∈ M^k` dà `φ_u : R^{1×k} → M`, `r ↦ Σ_j r_j • u_j`. -/
def rowPair (u : k → M) : (k → R) →ₗ[R] M where
  toFun r := ∑ j, r j • u j
  map_add' r s := by simp only [Pi.add_apply, add_smul, Finset.sum_add_distrib]
  map_smul' c r := by
    simp only [Pi.smul_apply, smul_eq_mul, mul_smul, RingHom.id_apply, Finset.smul_sum]

/-- `M^k ≅ Hom_R(R^{1×k}, M)`. -/
def rowEquiv [DecidableEq k] : (k → M) ≃ₗ[R] ((k → R) →ₗ[R] M) where
  toFun := rowPair
  map_add' u v := LinearMap.ext fun r => by
    simp only [rowPair, LinearMap.coe_mk, AddHom.coe_mk, LinearMap.add_apply, Pi.add_apply,
      smul_add, Finset.sum_add_distrib]
  map_smul' c u := LinearMap.ext fun r => by
    simp only [rowPair, LinearMap.coe_mk, AddHom.coe_mk, LinearMap.smul_apply, Pi.smul_apply,
      RingHom.id_apply, Finset.smul_sum]
    exact Finset.sum_congr rfl fun j _ => smul_comm _ _ _
  invFun φ j := φ (Pi.single j 1)
  left_inv u := by
    funext i
    simp [rowPair, Pi.single_apply]
  right_inv φ := LinearMap.ext fun r => by
    have hr : r = ∑ j, r j • Pi.single j (1 : R) := by
      funext i
      simp [Finset.sum_apply, Pi.single_apply]
    conv_rhs => rw [hr]
    simp [rowPair, map_sum, map_smul]

/-- Il modulo delle righe di `P`: `U_P = R^{1×ℓ} P ⊆ R^{1×k}`. -/
def rowSpan (P : Matrix l k R) : Submodule R (k → R) := Submodule.span R (Set.range fun i => P i)

/-- `u ∈ Sol(P)` se e solo se `φ_u` si annulla su `U_P`. -/
theorem rowSpan_le_ker_iff (P : Matrix l k R) (u : k → M) :
    rowSpan P ≤ LinearMap.ker (rowPair u) ↔ matOp P u = 0 := by
  rw [rowSpan, Submodule.span_le, Set.range_subset_iff, funext_iff]
  simp [rowPair, matOp_apply]

theorem map_Sol_eq [DecidableEq k] (P : Matrix l k R) :
    (Sol (M := M) P).map (rowEquiv (R := R) (M := M) (k := k)).toLinearMap =
      Comax.Sol (A := M) (rowSpan P) := by
  ext φ
  constructor
  · rintro ⟨u, hu, rfl⟩
    exact (rowSpan_le_ker_iff P u).mpr hu
  · intro hφ
    refine ⟨rowEquiv.symm φ, ?_, by simp⟩
    have h : rowPair (rowEquiv (R := R) (M := M) (k := k) |>.symm φ) = φ :=
      rowEquiv.apply_symm_apply φ
    have hφ' : rowSpan P ≤ LinearMap.ker (rowPair (rowEquiv (R := R) (M := M) (k := k) |>.symm φ)) := by
      rw [h]; exact hφ
    exact (rowSpan_le_ker_iff P _).mp hφ'

/-- **Malgrange (prima metà):** `Sol_M(P) ≅ {φ ∈ Hom_R(R^{1×k}, M) | φ|_{U_P} = 0}`. -/
noncomputable def solEquiv [DecidableEq k] (P : Matrix l k R) :
    Sol (M := M) P ≃ₗ[R] Comax.Sol (A := M) (rowSpan P) :=
  (rowEquiv (R := R) (M := M) (k := k)).ofSubmodules _ _ (map_Sol_eq P)

/-- **Malgrange (seconda metà):** `Hom_R(L/U, A) ≅ {φ ∈ Hom_R(L, A) | φ|_U = 0}`. -/
def quotHomEquiv {L A : Type*} [AddCommGroup L] [Module R L] [AddCommGroup A] [Module R A]
    (U : Submodule R L) : (L ⧸ U →ₗ[R] A) ≃ₗ[R] Comax.Sol (A := A) U where
  toFun f := ⟨f.comp U.mkQ, fun x hx => by
    simp [LinearMap.mem_ker, (Submodule.Quotient.mk_eq_zero U).mpr hx]⟩
  invFun φ := U.liftQ φ φ.2
  map_add' f g := Subtype.ext (LinearMap.add_comp _ _ _)
  map_smul' c f := Subtype.ext (LinearMap.smul_comp _ _ _)
  left_inv f := Submodule.linearMap_qext _ rfl
  right_inv φ := Subtype.ext (U.liftQ_mkQ _ _)

/-- **Isomorfismo di Malgrange:** `Sol_M(P) ≅ Hom_R(M_P, M)`, `M_P = R^{1×k}/U_P`. -/
noncomputable def malgrange [DecidableEq k] (P : Matrix l k R) :
    Sol (M := M) P ≃ₗ[R] ((k → R) ⧸ rowSpan P →ₗ[R] M) :=
  (solEquiv P).trans (quotHomEquiv (rowSpan P)).symm

/-! ## Passo del determinante (SYS-C1, CONV-MZ1) -/

/-- `P u = 0 ⇒ (det P) • u = 0` (adjugata). -/
theorem det_smul_eq_zero_of_mem_Sol [DecidableEq k] {P : Matrix k k R} {u : k → M}
    (hu : u ∈ Sol (M := M) P) : P.det • u = 0 := by
  have h := matOp_mul_apply (M := M) P.adjugate P u
  rw [Matrix.adjugate_mul, matOp_smul_apply, matOp_one_apply] at h
  rw [h, LinearMap.mem_ker.mp hu, map_zero]

/-! ## II-T3 per operatori che commutano (in particolare matrici in `Mat_k(R)`) -/

section EndDecomp

variable {N : Type*} [AddCommGroup N] [Module R N]

lemma end_mul_apply (f g : Module.End R N) (u : N) : (f * g) u = f (g u) := rfl

/-- II-T3 per endomorfismi: `a T₁ + b T₂ = 1`, `T₁ T₂ = T₂ T₁`, `b T₁ = T₁ b`, `a T₂ = T₂ a` ⇒
`ker(T₁T₂) = ker T₁ ⊕ ker T₂`, con proiettore `E₁ = b T₂`. -/
theorem end_kernel_decomposition {T₁ T₂ a b : Module.End R N} (h : a * T₁ + b * T₂ = 1)
    (h12 : Commute T₁ T₂) (hb : Commute b T₁) (ha : Commute a T₂) :
    LinearMap.ker (T₁ * T₂) = LinearMap.ker T₁ ⊔ LinearMap.ker T₂ ∧
    Disjoint (LinearMap.ker T₁) (LinearMap.ker T₂) ∧
    (∀ u ∈ LinearMap.ker (T₁ * T₂), (b * T₂) u ∈ LinearMap.ker T₁ ∧
      (a * T₁) u ∈ LinearMap.ker T₂ ∧ u = (b * T₂) u + (a * T₁) u) ∧
    (∀ u ∈ LinearMap.ker T₁, (b * T₂) u = u) ∧
    (∀ u ∈ LinearMap.ker T₂, (b * T₂) u = 0) := by
  have split : ∀ u : N, u = (b * T₂) u + (a * T₁) u := by
    intro u
    have := DFunLike.congr_fun h u
    rw [LinearMap.add_apply, Module.End.one_apply] at this
    rw [add_comm, this]
  have k1 : T₁ * (b * T₂) = b * (T₁ * T₂) := by rw [← mul_assoc, ← hb.eq, mul_assoc]
  have k2 : T₂ * (a * T₁) = a * (T₁ * T₂) := by
    rw [← mul_assoc, ← ha.eq, mul_assoc, h12.eq]
  have h1 : ∀ u ∈ LinearMap.ker (T₁ * T₂), (b * T₂) u ∈ LinearMap.ker T₁ := by
    intro u hu
    rw [LinearMap.mem_ker] at hu ⊢
    rw [← end_mul_apply, k1, end_mul_apply, hu, map_zero]
  have h2 : ∀ u ∈ LinearMap.ker (T₁ * T₂), (a * T₁) u ∈ LinearMap.ker T₂ := by
    intro u hu
    rw [LinearMap.mem_ker] at hu ⊢
    rw [← end_mul_apply, k2, end_mul_apply, hu, map_zero]
  have hzero : ∀ u ∈ LinearMap.ker T₂, (b * T₂) u = 0 := by
    intro u hu
    rw [end_mul_apply, LinearMap.mem_ker.mp hu, map_zero]
  have hzero' : ∀ u ∈ LinearMap.ker T₁, (a * T₁) u = 0 := by
    intro u hu
    rw [end_mul_apply, LinearMap.mem_ker.mp hu, map_zero]
  have hid : ∀ u ∈ LinearMap.ker T₁, (b * T₂) u = u := by
    intro u hu
    have := split u
    rw [hzero' u hu, add_zero] at this
    exact this.symm
  refine ⟨?_, ?_, fun u hu => ⟨h1 u hu, h2 u hu, split u⟩, hid, hzero⟩
  · apply le_antisymm
    · intro u hu
      rw [split u]
      exact Submodule.add_mem_sup (h1 u hu) (h2 u hu)
    · apply sup_le
      · intro u hu
        rw [LinearMap.mem_ker] at hu ⊢
        rw [h12.eq, end_mul_apply, hu, map_zero]
      · intro u hu
        rw [LinearMap.mem_ker] at hu ⊢
        rw [end_mul_apply, hu, map_zero]
  · rw [Submodule.disjoint_def]
    intro u hu1 hu2
    rw [split u, hzero u hu2, hzero' u hu1, add_zero]

end EndDecomp

/-- **II-T3 per sistemi con fattori che commutano.** `P₁, P₂, A, B ∈ Mat_k(R)` con
`A P₁ + B P₂ = I`, `P₁P₂ = P₂P₁`, `B P₁ = P₁ B`, `A P₂ = P₂ A`: su ogni `R`-modulo `M`,
`Sol_M(P₁P₂) = Sol_M(P₁) ⊕ Sol_M(P₂)`, con `u = (B P₂) u + (A P₁) u`. -/
theorem matrix_kernel_decomposition [DecidableEq k] {P₁ P₂ A B : Matrix k k R}
    (h : A * P₁ + B * P₂ = 1) (h12 : Commute P₁ P₂) (hB : Commute B P₁) (hA : Commute A P₂) :
    Sol (M := M) (P₁ * P₂) = Sol P₁ ⊔ Sol P₂ ∧ Disjoint (Sol (M := M) P₁) (Sol P₂) ∧
    (∀ u ∈ Sol (M := M) (P₁ * P₂), u = matOp (B * P₂) u + matOp (A * P₁) u) := by
  have h' : matEnd (M := M) A * matEnd P₁ + matEnd B * matEnd P₂ = 1 := by
    rw [← map_mul, ← map_mul, ← map_add, h, map_one]
  obtain ⟨e1, e2, e3, -, -⟩ := end_kernel_decomposition h' (h12.map matEnd) (hB.map matEnd)
    (hA.map matEnd)
  have hS : ∀ P : Matrix k k R, Sol (M := M) P = LinearMap.ker (matEnd (M := M) P) :=
    fun _ => rfl
  refine ⟨?_, ?_, ?_⟩
  · rw [hS, hS, hS, map_mul]; exact e1
  · rw [hS, hS]; exact e2
  · intro u hu
    rw [hS, map_mul] at hu
    have := (e3 u hu).2.2
    rw [← map_mul, ← map_mul] at this
    exact this

/-- `ker d` su `M^k` per uno scalare `d ∈ R` (componente per componente). -/
abbrev scalarKer (d : R) : Submodule R (k → M) := LinearMap.ker (LinearMap.lsmul R (k → M) d)

lemma mem_scalarKer {d : R} {u : k → M} : u ∈ scalarKer (M := M) d ↔ d • u = 0 := by
  simp [scalarKer]

/-- **Spezzamento per fattori comassimali del determinante.** `P ∈ Mat_k(R)`,
`det P = d₁ d₂`, `a d₁ + b d₂ = 1`: `Sol_M(P) = Sol_M(P) ∩ ker d₁ ⊕ Sol_M(P) ∩ ker d₂`
(`d_i` agisce componente per componente), con `u = (b d₂) • u + (a d₁) • u`. -/
theorem sol_split_of_det [DecidableEq k] {P : Matrix k k R} {d₁ d₂ a b : R}
    (hdet : P.det = d₁ * d₂) (hab : a * d₁ + b * d₂ = 1) :
    Sol (M := M) P = (Sol P ⊓ scalarKer d₁) ⊔ (Sol P ⊓ scalarKer d₂) ∧
    Disjoint (Sol (M := M) P ⊓ scalarKer d₁) (Sol P ⊓ scalarKer d₂) := by
  have split : ∀ u : k → M, u = (b * d₂) • u + (a * d₁) • u := by
    intro u; rw [← add_smul, add_comm, hab, one_smul]
  refine ⟨le_antisymm ?_ (sup_le inf_le_left inf_le_left), ?_⟩
  · intro u hu
    have hdu : P.det • u = 0 := det_smul_eq_zero_of_mem_Sol hu
    rw [split u]
    refine Submodule.add_mem_sup ⟨Submodule.smul_mem _ _ hu, ?_⟩ ⟨Submodule.smul_mem _ _ hu, ?_⟩
    · refine mem_scalarKer.mpr ?_
      rw [smul_smul, show d₁ * (b * d₂) = b * P.det by rw [hdet]; ring, mul_smul,
        hdu, smul_zero]
    · refine mem_scalarKer.mpr ?_
      rw [smul_smul, show d₂ * (a * d₁) = a * P.det by rw [hdet]; ring, mul_smul,
        hdu, smul_zero]
  · rw [Submodule.disjoint_def]
    rintro u ⟨-, h1⟩ ⟨-, h2⟩
    replace h1 := mem_scalarKer.mp h1
    replace h2 := mem_scalarKer.mp h2
    rw [split u, mul_smul, h2, smul_zero, mul_smul, h1, smul_zero, add_zero]

end PBLean.F10.Morita
