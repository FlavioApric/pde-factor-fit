import Mathlib

/-!
# DICT-N1(i), caso normato (S10-LEAN, bersaglio 6b, facoltativo)

Claim (LEDGER Fase 8, S8-DICT, DICT-N1 (i)): in un F-spazio `X` di dimensione infinita,
un'unione numerabile di compatti (immagini di atomi con finiti parametri) è magra; quindi gli
operatori rappresentabili esattamente da un dizionario numerabile formano un insieme magro.
Qui si formalizza il caso in cui `X` è uno spazio normato su un campo normato completo
(per esempio `ℝ`, `ℂ`): Riesz (una palla chiusa compatta forza la dimensione finita) più la
definizione di insieme magro. Il caso F-spazio non normato (per esempio `C^∞(Ω)`, `S^m`) non è
coperto: Mathlib ha il teorema di Riesz solo per spazi normati.
-/

namespace PBLean.F10.BaireN1

variable {𝕜 E : Type*} [NontriviallyNormedField 𝕜] [CompleteSpace 𝕜]
  [NormedAddCommGroup E] [NormedSpace 𝕜 E]

/-- In uno spazio normato di dimensione infinita un compatto ha interno vuoto. -/
theorem interior_eq_empty_of_isCompact (hinf : ¬ FiniteDimensional 𝕜 E) {C : Set E}
    (hC : IsCompact C) : interior C = ∅ := by
  rw [Set.eq_empty_iff_forall_notMem]
  intro x hx
  obtain ⟨ε, hε, hball⟩ := Metric.isOpen_iff.mp isOpen_interior x hx
  have hsub : Metric.closedBall x (ε / 2) ⊆ C :=
    (Metric.closedBall_subset_ball (by linarith)).trans (hball.trans interior_subset)
  have hcpt : IsCompact (Metric.closedBall x (ε / 2)) :=
    hC.of_isClosed_subset Metric.isClosed_closedBall hsub
  exact hinf (FiniteDimensional.of_isCompact_closedBall 𝕜 (by linarith) hcpt)

/-- **DICT-N1(i), caso normato.** Un'unione numerabile di compatti è magra. -/
theorem isMeagre_iUnion_compact (hinf : ¬ FiniteDimensional 𝕜 E) (C : ℕ → Set E)
    (hC : ∀ n, IsCompact (C n)) : IsMeagre (⋃ n, C n) := by
  apply isMeagre_iUnion
  intro n
  apply IsNowhereDense.isMeagre
  rw [(hC n).isClosed.isNowhereDense_iff]
  exact interior_eq_empty_of_isCompact hinf (hC n)

end PBLean.F10.BaireN1
