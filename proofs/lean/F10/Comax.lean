import Mathlib

/-!
# Scomposizione comassimale per i sistemi (S10-LEAN, bersaglio 5)

Claim (LEDGER Fase 8, S8-SYS): SYS-S1(ii), prima parte («Sol(Q₁) ∩ Sol(Q₂) = Sol(N)», cioè la
soluzione dei due sistemi insieme è la soluzione di U₁ + U₂), e SYS-S1(i⇐) nel caso
`N = R^{1×k}/(U₁ + U₂) = 0` (comassimale), dove `Ext¹(N, 𝒜) = 0` è automatico. È l'estensione ai
sistemi di II-T3 (PBLean.IIT3): per `k = 1`, `U_i = (P_i)`, `U₁ + U₂ = R` è la comassimalità
e `U₁ ∩ U₂ = (P₁P₂)`.

Quadro: `R` anello commutativo, `L` un `R`-modulo (nel progetto `L = R^{1×k}`, righe),
`𝒜` un `R`-modulo qualsiasi (nel progetto `C^∞(Ω)` o `𝒟′(Ω)`). Per un sottomodulo `U ≤ L`,
`Sol(U) := {φ : L →ₗ[R] 𝒜 | U ≤ ker φ}`, cioè `Hom_R(L/U, 𝒜)`; con `L = R^{1×k}` e `U = U_P`
è `Sol_𝒜(P)` tramite l'isomorfismo di Malgrange (PBLean.F10.Morita).
-/

namespace PBLean.F10.Comax

variable {R L A : Type*} [CommRing R] [AddCommGroup L] [Module R L] [AddCommGroup A] [Module R A]

/-- `Sol(U) = {φ ∈ Hom_R(L, 𝒜) | φ|_U = 0}` come sottomodulo di `Hom_R(L, 𝒜)`. -/
def Sol (U : Submodule R L) : Submodule R (L →ₗ[R] A) where
  carrier := {φ | U ≤ LinearMap.ker φ}
  add_mem' {φ ψ} hφ hψ x hx := by
    simp only [LinearMap.mem_ker, LinearMap.add_apply] at *
    rw [hφ hx, hψ hx, add_zero]
  zero_mem' x _ := by simp
  smul_mem' c φ hφ x hx := by
    simp only [LinearMap.mem_ker, LinearMap.smul_apply] at *
    rw [hφ hx, smul_zero]

@[simp] lemma mem_Sol {U : Submodule R L} {φ : L →ₗ[R] A} :
    φ ∈ Sol U ↔ ∀ x ∈ U, φ x = 0 := Iff.rfl

/-- `Sol` è antitona: più relazioni, meno soluzioni. -/
lemma Sol_antitone {U V : Submodule R L} (h : U ≤ V) : Sol (A := A) V ≤ Sol U :=
  fun _ hφ x hx => (mem_Sol.mp hφ) x (h hx)

/-- SYS-S1(ii), prima parte: `Sol(U₁ + U₂) = Sol(U₁) ∩ Sol(U₂)`, su ogni modulo `𝒜`. -/
theorem Sol_sup (U₁ U₂ : Submodule R L) : Sol (A := A) (U₁ ⊔ U₂) = Sol U₁ ⊓ Sol U₂ := by
  ext φ
  simp only [Submodule.mem_inf, mem_Sol]
  constructor
  · intro h
    exact ⟨fun x hx => h x (Submodule.mem_sup_left hx),
      fun x hx => h x (Submodule.mem_sup_right hx)⟩
  · rintro ⟨h₁, h₂⟩ x hx
    obtain ⟨a, ha, b, hb, rfl⟩ := Submodule.mem_sup.mp hx
    rw [map_add, h₁ a ha, h₂ b hb, add_zero]

/-- Mappa somma `U₁ × U₂ → L`. -/
def sumMap (U₁ U₂ : Submodule R L) : (U₁ × U₂) →ₗ[R] L :=
  U₁.subtype.coprod U₂.subtype

lemma sumMap_apply (U₁ U₂ : Submodule R L) (p : U₁ × U₂) :
    sumMap U₁ U₂ p = (p.1 : L) + p.2 := rfl

lemma sumMap_surjective {U₁ U₂ : Submodule R L} (h : U₁ ⊔ U₂ = ⊤) :
    Function.Surjective (sumMap U₁ U₂) := by
  intro x
  have hx : x ∈ U₁ ⊔ U₂ := h ▸ Submodule.mem_top
  obtain ⟨a, ha, b, hb, rfl⟩ := Submodule.mem_sup.mp hx
  exact ⟨(⟨a, ha⟩, ⟨b, hb⟩), rfl⟩

/-- **Scomposizione comassimale per i sistemi.** Se `U₁ + U₂ = L` (cioè `N = 0`), allora per ogni
`R`-modulo `𝒜`: `Sol(U₁ ∩ U₂) = Sol(U₁) ⊕ Sol(U₂)` (somma interna e intersezione nulla). -/
theorem Sol_inf_of_sup_eq_top {U₁ U₂ : Submodule R L} (h : U₁ ⊔ U₂ = ⊤) :
    Sol (A := A) (U₁ ⊓ U₂) = Sol U₁ ⊔ Sol U₂ ∧ Disjoint (Sol (A := A) U₁) (Sol U₂) := by
  constructor
  · apply le_antisymm
    · intro φ hφ
      -- χ(a, b) := φ(b) si annulla sul nucleo della somma, perché lì b = −a ∈ U₁ ∩ U₂
      let ψ := sumMap U₁ U₂
      let χ : (U₁ × U₂) →ₗ[R] A := φ.comp (U₂.subtype.comp (LinearMap.snd R U₁ U₂))
      have hker : LinearMap.ker ψ ≤ LinearMap.ker χ := by
        rintro ⟨a, b⟩ hab
        simp only [LinearMap.mem_ker] at hab ⊢
        rw [sumMap_apply] at hab
        have hba : (b : L) = -(a : L) := eq_neg_of_add_eq_zero_right hab
        have hb1 : (b : L) ∈ U₁ := hba ▸ U₁.neg_mem a.2
        exact (mem_Sol.mp hφ) _ ⟨hb1, b.2⟩
      let e := LinearMap.quotKerEquivOfSurjective ψ (sumMap_surjective h)
      let φ₁ : L →ₗ[R] A := ((LinearMap.ker ψ).liftQ χ hker).comp e.symm.toLinearMap
      have hφ₁ : ∀ p, φ₁ (ψ p) = χ p := by
        intro p
        have : e.symm (ψ p) = Submodule.Quotient.mk p := by
          rw [LinearEquiv.symm_apply_eq]
          rfl
        simp only [φ₁, LinearMap.comp_apply, LinearEquiv.coe_coe, this]
        rfl
      have h1 : φ₁ ∈ Sol U₁ := by
        intro x hx
        have := hφ₁ (⟨x, hx⟩, 0)
        simpa [ψ, sumMap_apply, χ, LinearMap.mem_ker] using this
      have h2 : φ - φ₁ ∈ Sol U₂ := by
        intro x hx
        have := hφ₁ (0, ⟨x, hx⟩)
        simp [ψ, sumMap_apply, χ] at this
        rw [LinearMap.mem_ker, LinearMap.sub_apply, this, sub_self]
      have : φ = φ₁ + (φ - φ₁) := by abel
      rw [this]
      exact Submodule.add_mem_sup h1 h2
    · rw [sup_le_iff]
      exact ⟨Sol_antitone inf_le_left, Sol_antitone inf_le_right⟩
  · rw [Submodule.disjoint_def]
    intro φ h₁ h₂
    have : φ ∈ Sol (U₁ ⊔ U₂) := by rw [Sol_sup]; exact ⟨h₁, h₂⟩
    ext x
    exact (mem_Sol.mp this) x (h ▸ Submodule.mem_top)

/-- Caso scalare (`L = R`, `U_i = (P_i)`): la comassimalità `a P₁ + b P₂ = 1` dà `U₁ + U₂ = R`
e `U₁ ∩ U₂ = (P₁ P₂)`, quindi `Sol(P₁P₂) = Sol(P₁) ⊕ Sol(P₂)` per ogni `𝒜` (II-T3). -/
theorem scalar_case {P₁ P₂ a b : R} (hab : a * P₁ + b * P₂ = 1) :
    (Ideal.span {P₁} ⊔ Ideal.span {P₂} : Ideal R) = ⊤ ∧
    (Ideal.span {P₁} ⊓ Ideal.span {P₂} : Ideal R) = Ideal.span {P₁ * P₂} := by
  have htop : (Ideal.span {P₁} ⊔ Ideal.span {P₂} : Ideal R) = ⊤ := by
    rw [Ideal.eq_top_iff_one, ← hab]
    exact Ideal.add_mem _ (Ideal.mem_sup_left (Ideal.mul_mem_left _ _ (Ideal.mem_span_singleton_self _)))
      (Ideal.mem_sup_right (Ideal.mul_mem_left _ _ (Ideal.mem_span_singleton_self _)))
  refine ⟨htop, ?_⟩
  rw [← Ideal.span_singleton_mul_span_singleton]
  exact (Ideal.mul_eq_inf_of_coprime htop).symm

end PBLean.F10.Comax
