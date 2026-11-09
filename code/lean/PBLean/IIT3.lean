import Mathlib

/-!
# II-T3, esistenza nel caso comassimale (fix II-T3-F2) — S5-LEAN

Claim (LEDGER riga II-T3, DIMOSTRATO; work/II/PROOF_PACKAGE.md §[II-T3], [fix II-T3-F2]):
sotto `(P₁, P₂) = R`, con `a P₁ + b P₂ = 1`, per **qualunque** `R`-modulo `F`:
`ker_F P = ker_F P₁ ⊕ ker_F P₂` (`P = P₁ P₂`), con `u = (b P₂) u + (a P₁) u`,
`(b P₂) u ∈ ker P₁`, `(a P₁) u ∈ ker P₂`; e `E₁ := b P₂` è il proiettore di componente:
`E₁ u₁ = u₁` su `ker P₁`, `E₁ u₂ = 0` su `ker P₂`.

Formalizzazione: `R` anello commutativo qualsiasi (nel progetto `R = ℂ[τ, ξ]`, che agisce su
`F = C^∞(Ω), 𝒟′(Ω), …` tramite `τ ↦ ∂_t`, `ξ ↦ ∂_x`), `M` un `R`-modulo qualsiasi,
`ker_M r := {m | r • m = 0}`.
-/

namespace PBLean.IIT3

variable {R M : Type*} [CommRing R] [AddCommGroup M] [Module R M]

/-- `ker_M r = {m ∈ M | r • m = 0}` (nucleo dell'operatore `r(∂)`). -/
abbrev smulKer (r : R) : Submodule R M := LinearMap.ker (LinearMap.lsmul R M r)

@[simp] lemma mem_smulKer {r : R} {m : M} : m ∈ smulKer (M := M) r ↔ r • m = 0 := by
  simp [smulKer]

/-- II-T3 (esistenza, caso comassimale). -/
theorem kernel_decomposition {P₁ P₂ a b : R} (h : a * P₁ + b * P₂ = 1) :
    smulKer (M := M) (P₁ * P₂) = smulKer P₁ ⊔ smulKer P₂ ∧
    Disjoint (smulKer (M := M) P₁) (smulKer P₂) ∧
    (∀ u ∈ smulKer (M := M) (P₁ * P₂),
      (b * P₂) • u ∈ smulKer P₁ ∧ (a * P₁) • u ∈ smulKer P₂ ∧ u = (b * P₂) • u + (a * P₁) • u) ∧
    (∀ u ∈ smulKer (M := M) P₁, (b * P₂) • u = u) ∧
    (∀ u ∈ smulKer (M := M) P₂, (b * P₂) • u = 0) ∧
    (∀ u ∈ smulKer (M := M) (P₁ * P₂), (b * P₂) • ((b * P₂) • u) = (b * P₂) • u) := by
  -- ingredienti
  have split : ∀ u : M, u = (b * P₂) • u + (a * P₁) • u := by
    intro u
    rw [← add_smul, add_comm, h, one_smul]
  have h1 : ∀ u ∈ smulKer (M := M) (P₁ * P₂), (b * P₂) • u ∈ smulKer P₁ := by
    intro u hu
    rw [mem_smulKer] at hu ⊢
    rw [smul_smul, show P₁ * (b * P₂) = b * (P₁ * P₂) by ring, mul_smul, hu, smul_zero]
  have h2 : ∀ u ∈ smulKer (M := M) (P₁ * P₂), (a * P₁) • u ∈ smulKer P₂ := by
    intro u hu
    rw [mem_smulKer] at hu ⊢
    rw [smul_smul, show P₂ * (a * P₁) = a * (P₁ * P₂) by ring, mul_smul, hu, smul_zero]
  have hid : ∀ u ∈ smulKer (M := M) P₁, (b * P₂) • u = u := by
    intro u hu
    rw [mem_smulKer] at hu
    have := split u
    rw [mul_smul a, hu, smul_zero, add_zero] at this
    exact this.symm
  have hzero : ∀ u ∈ smulKer (M := M) P₂, (b * P₂) • u = 0 := by
    intro u hu
    rw [mem_smulKer] at hu
    rw [mul_smul, hu, smul_zero]
  refine ⟨?_, ?_, fun u hu => ⟨h1 u hu, h2 u hu, split u⟩, hid, hzero, ?_⟩
  · apply le_antisymm
    · intro u hu
      rw [split u]
      exact Submodule.add_mem_sup (h1 u hu) (h2 u hu)
    · apply sup_le
      · intro u hu
        rw [mem_smulKer] at hu ⊢
        rw [mul_comm, mul_smul, hu, smul_zero]
      · intro u hu
        rw [mem_smulKer] at hu ⊢
        rw [mul_smul, hu, smul_zero]
  · rw [Submodule.disjoint_def]
    intro u hu1 hu2
    rw [split u, hzero u hu2, mul_smul a, (mem_smulKer).mp hu1, smul_zero, add_zero]
  · intro u hu
    exact hid _ (h1 u hu)

end PBLean.IIT3
