import Mathlib

/-!
# SYS-T0, passo combinatorio sulla forma di Smith (S10-LEAN, bersaglio 6a, facoltativo)

Claim (LEDGER Fase 8, S8-SYS, SYS-T0, NOTO): per un sistema di EDO `P ∈ ℂ[s]^{ℓ×k}` di rango `r`
con fattori invarianti `e_1 ∣ e_2 ∣ … ∣ e_r`, si ha `dim soc_{(s−λ)}(M_P) = #{i : e_i(λ) = 0}`
e la condizione «≤ 1 per ogni λ» equivale a `e_1 = … = e_{r−1} = 1`.
Qui si formalizza solo l'ultimo passo, puramente polinomiale: per una catena di divisibilità in
`ℂ[s]` (vale su ogni campo algebricamente chiuso),
`(∀ λ, #{i : e_i(λ) = 0} ≤ 1) ⟺ e_1, …, e_{r−1} sono unità`.
Non formalizzati: esistenza della forma di Smith per `M_P`, calcolo degli zoccoli, gcd dei minori,
e il rinvio a SYS-EX.
-/

namespace PBLean.F10.SmithT0

open Polynomial

variable {K : Type*} [Field K] [IsAlgClosed K] [DecidableEq K]

/-- Numero di fattori invarianti che si annullano in `λ` (= `dim soc_{(s−λ)}`). -/
noncomputable def rootCount {r : ℕ} (e : Fin r → K[X]) (z : K) : ℕ :=
  (Finset.univ.filter fun i => (e i).IsRoot z).card

theorem socle_le_one_iff {r : ℕ} (e : Fin r → K[X])
    (hdiv : ∀ i j : Fin r, i ≤ j → e i ∣ e j) :
    (∀ z : K, rootCount e z ≤ 1) ↔ ∀ i : Fin r, i.val + 1 < r → IsUnit (e i) := by
  constructor
  · intro h i hi
    by_contra hu
    have hdeg : (e i).degree ≠ 0 := fun h0 => hu (isUnit_iff_degree_eq_zero.mpr h0)
    obtain ⟨z, hz⟩ := IsAlgClosed.exists_root (e i) hdeg
    let j : Fin r := ⟨i.val + 1, hi⟩
    have hij : i ≤ j := by simp [j, Fin.le_def]
    have hj : (e j).IsRoot z := by
      obtain ⟨c, hc⟩ := hdiv i j hij
      simp [IsRoot, hc, eval_mul, hz.eq_zero]
    have hsub : ({i, j} : Finset (Fin r)) ⊆ Finset.univ.filter fun l => (e l).IsRoot z := by
      intro l hl
      simp only [Finset.mem_insert, Finset.mem_singleton] at hl
      rcases hl with rfl | rfl
      · simpa using hz
      · simpa using hj
    have hne : i ≠ j := by
      intro heq
      have := congrArg Fin.val heq
      simp [j] at this
    have h2 := Finset.card_le_card hsub
    rw [Finset.card_pair hne] at h2
    have := h z
    unfold rootCount at this
    omega
  · intro h z
    unfold rootCount
    rw [Finset.card_le_one]
    intro a ha b hb
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at ha hb
    have last : ∀ l : Fin r, (e l).IsRoot z → l.val + 1 = r := by
      intro l hl
      by_contra hne
      have hlt : l.val + 1 < r := by omega
      have hu := (h l hlt).map (evalRingHom z)
      exact hu.ne_zero (by simpa [IsRoot] using hl)
    exact Fin.ext (by have := last a ha; have := last b hb; omega)

end PBLean.F10.SmithT0
