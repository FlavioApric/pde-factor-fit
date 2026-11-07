import Mathlib

/-!
# R5-T2(i) — nucleo algebrico (S5-LEAN, Fase 5)

Claim del LEDGER (riga R5-T2(i–iii), DIMOSTRATO; research/R5/REPORT.md §2, [R5-T2]):
termini a due a due commutanti, `u = Σ_{S ⊆ [N]} Π_{n∈S} (S_n − I) u₀`, quindi
`E_int^add = Σ_{|S| ≥ 2} Π_{n∈S} (S_n − I) u₀`.

Qui si formalizza il **nucleo algebrico** a tempo fissato `t`:
* (a) in un anello commutativo `A`: `Π_n (1 + x_n) = Σ_S Π_{n∈S} x_n`, e per un `A`-modulo `M`
  la scomposizione per ordine `Π(1+x_n)•u₀ = u₀ + Σ_n x_n•u₀ + E`,
  `E = Σ_{|S|≥2} (Π_{n∈S} x_n)•u₀`;
* (b) per endomorfismi `S_0, …, S_{N-1}` a due a due commutanti di un `R`-modulo `M`
  (es. gli operatori `S_n(t)` dei semigruppi commutanti valutati a `t` fissato):
  la composizione ordinata `S_0 ∘ ⋯ ∘ S_{N-1}` è `Σ_T Π_{n∈T}(S_n − 1)` e
  `(S_0⋯S_{N-1}) u₀ = u₀ + Σ_n (S_n − 1) u₀ + E`, `E = Σ_{|T|≥2} Π_{n∈T}(S_n − 1) u₀`.

Non formalizzato (fuori dal nucleo algebrico): che `u(t) = S_1(t)⋯S_N(t)u₀` sia la soluzione mild
(R5-T1, CON-FONTE), la topologia di Banach, le stime di costo (ii–iii).
-/

namespace PBLean.R5T2

open Finset

/-- (a) Espansione di `Π(1 + x_n)` sui sottoinsiemi, in un anello commutativo. -/
theorem prod_one_add_eq_sum_powerset {ι A : Type*} [CommRing A] (s : Finset ι) (x : ι → A) :
    ∏ n ∈ s, (1 + x n) = ∑ T ∈ s.powerset, ∏ n ∈ T, x n :=
  Finset.prod_one_add s

/-- I sottoinsiemi di cardinalità < 2 sono `∅` e i singoletti. -/
lemma sum_powerset_card_lt_two {ι B : Type*} [DecidableEq ι] [AddCommMonoid B]
    (s : Finset ι) (f : Finset ι → B) :
    ∑ T ∈ s.powerset with ¬ 2 ≤ T.card, f T = f ∅ + ∑ n ∈ s, f {n} := by
  have hset : (s.powerset.filter fun T => ¬ 2 ≤ T.card) = insert ∅ (s.image fun n => {n}) := by
    ext T
    simp only [mem_filter, mem_powerset, mem_insert, mem_image]
    constructor
    · rintro ⟨hT, hc⟩
      have : T.card = 0 ∨ T.card = 1 := by omega
      rcases this with h0 | h1
      · exact Or.inl (Finset.card_eq_zero.mp h0)
      · obtain ⟨a, rfl⟩ := Finset.card_eq_one.mp h1
        exact Or.inr ⟨a, hT (mem_singleton_self a), rfl⟩
    · rintro (rfl | ⟨a, ha, rfl⟩)
      · simp
      · simp [ha]
  rw [hset, sum_insert, sum_image]
  · intro a _ b _ hab
    exact Finset.singleton_injective hab
  · simp

/-- (a′) Scomposizione per ordine: `Π(1+x_n)•u₀ = u₀ + Σ_n x_n•u₀ + E`,
con `E = Σ_{T ⊆ s, |T| ≥ 2} (Π_{n∈T} x_n)•u₀` (forma di `E_int^add`). -/
theorem prod_one_add_smul_decomp {ι A M : Type*} [DecidableEq ι] [CommRing A]
    [AddCommGroup M] [Module A M] (s : Finset ι) (x : ι → A) (u₀ : M) :
    (∏ n ∈ s, (1 + x n)) • u₀ =
      u₀ + ∑ n ∈ s, x n • u₀ + ∑ T ∈ s.powerset with 2 ≤ T.card, (∏ n ∈ T, x n) • u₀ := by
  rw [Finset.prod_one_add, Finset.sum_smul,
    ← Finset.sum_filter_add_sum_filter_not s.powerset (fun T => 2 ≤ T.card),
    sum_powerset_card_lt_two]
  simp only [prod_empty, one_smul, prod_singleton]
  abel

/-- Versione d'anello di (a′) (`M = A`, `u₀ = 1`). -/
theorem prod_one_add_decomp {ι A : Type*} [DecidableEq ι] [CommRing A] (s : Finset ι) (x : ι → A) :
    ∏ n ∈ s, (1 + x n) =
      1 + ∑ n ∈ s, x n + ∑ T ∈ s.powerset with 2 ≤ T.card, ∏ n ∈ T, x n := by
  simpa using prod_one_add_smul_decomp (M := A) s x 1

open scoped IsMulCommutative in
/-- (b) Endomorfismi a due a due commutanti: la composizione ordinata `S_0 ∘ ⋯ ∘ S_{N-1}` è
`Σ_T Π_{n∈T}(S_n − 1)` (prodotti ordinati per indice crescente) e
`(S_0⋯S_{N-1}) u₀ = u₀ + Σ_n (S_n − 1) u₀ + Σ_{|T| ≥ 2} Π_{n∈T}(S_n − 1) u₀`. -/
theorem commuting_endomorphisms_decomp {R M : Type*} [CommRing R] [AddCommGroup M] [Module R M]
    {N : ℕ} (S : Fin N → Module.End R M) (hcomm : ∀ i j, Commute (S i) (S j)) :
    (List.ofFn S).prod =
        ∑ T : Finset (Fin N), (List.ofFn fun n => if n ∈ T then S n - 1 else 1).prod ∧
    ∀ u₀ : M, (List.ofFn S).prod u₀ =
        u₀ + ∑ n, (S n - 1) u₀ +
          ∑ T ∈ (Finset.univ : Finset (Fin N)).powerset with 2 ≤ T.card,
            (List.ofFn fun n => if n ∈ T then S n - 1 else 1).prod u₀ := by
  classical
  set A := Algebra.adjoin R (Set.range S) with hA
  have : IsMulCommutative A := Algebra.isMulCommutative_adjoin R (by
    rintro _ ⟨i, rfl⟩ _ ⟨j, rfl⟩ _
    exact hcomm i j)
  let s : Fin N → A := fun n => ⟨S n, Algebra.subset_adjoin ⟨n, rfl⟩⟩
  have hs : ∀ n, (A.val (s n)) = S n := fun n => rfl
  -- prodotto ordinato di una famiglia in `A` mappato in `End`
  have hmap : ∀ f : Fin N → A, A.val (∏ n, f n) = (List.ofFn fun n => A.val (f n)).prod := by
    intro f
    rw [← Fin.prod_ofFn, map_list_prod, List.map_ofFn]
    rfl
  have hT : ∀ T : Finset (Fin N),
      A.val (∏ n ∈ T, (s n - 1)) = (List.ofFn fun n => if n ∈ T then S n - 1 else 1).prod := by
    intro T
    rw [show ∏ n ∈ T, (s n - 1) = ∏ n, (if n ∈ T then s n - 1 else 1) by
      rw [Finset.prod_ite_mem, Finset.univ_inter], hmap]
    congr 1
    apply congrArg List.ofFn
    funext n
    split_ifs <;> simp [s]
  have hS : (List.ofFn S).prod = A.val (∏ n, (1 + (s n - 1))) := by
    rw [hmap]
    congr 1
    apply congrArg List.ofFn
    funext n
    simp [s]
  refine ⟨?_, ?_⟩
  · rw [hS, prod_one_add_eq_sum_powerset, Finset.powerset_univ, map_sum]
    exact Finset.sum_congr rfl fun T _ => hT T
  · intro u₀
    rw [hS, prod_one_add_decomp, map_add, map_add, map_one, map_sum, map_sum,
      LinearMap.add_apply, LinearMap.add_apply, LinearMap.sum_apply, LinearMap.sum_apply]
    simp only [Module.End.one_apply, hT, map_sub, map_one, hs]

end PBLean.R5T2
