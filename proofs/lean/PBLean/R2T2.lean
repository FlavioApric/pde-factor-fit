import Mathlib

/-!
# R2-T2 al livello L0 (ODE, n = 1) — S5-LEAN

Claim (research/R2/REPORT.md, [R2-T2] punti 2 e 4; usato da C12-T1 per le ODE):
per `f, g` coprimi `ker(fg) = ker f + ker g`; per `n = 1` coprimi ⇒ `(f, g) = R` (Bézout) ⇒
somma diretta.

Formalizzazione al livello L0: `T` endomorfismo `K`-lineare di uno spazio vettoriale `V` su un
campo `K` (per le ODE: `T = d/dx` su `C^∞(I)` o `𝒟′(I)`), `p, q ∈ K[X]` coprimi
(nessun fattore comune non invertibile, `IsRelPrime`).
Allora `ker (pq)(T) = ker p(T) ⊔ ker q(T)` e `ker p(T) ⊓ ker q(T) = 0`.
Prova: lemmi di Mathlib `Polynomial.sup_ker_aeval_eq_ker_aeval_mul_of_coprime`,
`Polynomial.disjoint_ker_aeval_of_isCoprime` (Bézout `IsCoprime`), più `IsRelPrime → IsCoprime`
in `K[X]` (dominio a ideali principali).
-/

namespace PBLean.R2T2

open Polynomial

variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-- R2-T2 (L0): `ker (pq)(T) = ker p(T) ⊕ ker q(T)` per `p, q` coprimi. -/
theorem ker_mul_eq_sup_of_relPrime (T : V →ₗ[K] V) {p q : K[X]} (hpq : IsRelPrime p q) :
    LinearMap.ker (aeval T (p * q)) = LinearMap.ker (aeval T p) ⊔ LinearMap.ker (aeval T q) ∧
    Disjoint (LinearMap.ker (aeval T p)) (LinearMap.ker (aeval T q)) := by
  have hc : IsCoprime p q := hpq.isCoprime
  exact ⟨(Polynomial.sup_ker_aeval_eq_ker_aeval_mul_of_coprime T hc).symm,
    Polynomial.disjoint_ker_aeval_of_isCoprime T hc⟩

/-- Punto 4 di R2-T2: in `K[X]` coprimi ⇒ `(p, q) = K[X]` (Bézout). -/
theorem span_eq_top_of_relPrime {p q : K[X]} (hpq : IsRelPrime p q) :
    Ideal.span ({p, q} : Set K[X]) = ⊤ := by
  obtain ⟨a, b, hab⟩ : IsCoprime p q := hpq.isCoprime
  rw [Ideal.eq_top_iff_one, ← hab]
  exact Ideal.add_mem _ (Ideal.mul_mem_left _ _ (Ideal.subset_span (by simp)))
    (Ideal.mul_mem_left _ _ (Ideal.subset_span (by simp)))

end PBLean.R2T2
