import Mathlib

/-!
# Filtrazione a livello finito di 𝓓_n (S10-LEAN, bersaglio 4)

Claim (LEDGER Fase 8, S8-DICT): quadro di §0 (dizionario filtrato `𝓓_0 ⊂ 𝓓_1 ⊂ …` di insiemi
finiti; nucleo di Gram al livello `n` = `Ann(u) ∩ span 𝓓_n`; fit / misfit), la parte
algebrica di DICT-GR (b) (`⟨L⟩_n ⊂ nucleo` sempre) e il passo di rango di DICT-N1iii
(`dim(Ann(u) ∩ R_{≤n}) ≥ dim R_{≤n} − dim R·u`).
Non formalizzato: `dim R_{≤n} = C(n+N, N)` e quindi l'inclusione stretta di DICT-N1iii.

Quadro astratto: `O` spazio degli operatori su un campo `𝕜`, `V_n ⊆ O` sottospazi crescenti
(`V_n = span 𝓓_n`), `ev_u : O → F`, `Q ↦ Q u` (lineare). Istanza a coefficienti costanti:
`O = R = 𝕜[ζ_1, …, ζ_N]`, `V_n = R_{≤n}` (grado totale ≤ n), `ev_u(Q) = Q • u`.
-/

namespace PBLean.F10.Filtration

open Module

section Abstract

variable {𝕜 O F : Type*} [Field 𝕜] [AddCommGroup O] [Module 𝕜 O] [AddCommGroup F] [Module 𝕜 F]
variable (V : ℕ → Submodule 𝕜 O) (ev : O →ₗ[𝕜] F)

/-- Nucleo al livello `n`: `K_n = V_n ∩ ker ev_u` (nucleo di Gram, C3-L1). -/
def kernelAt (n : ℕ) : Submodule 𝕜 O := V n ⊓ LinearMap.ker ev

/-- Fit (omogeneo) al livello `n`: esiste `c ≠ 0` in `V_n` con `ev_u(c) = 0`. -/
def Fit (n : ℕ) : Prop := ∃ c ∈ V n, c ≠ 0 ∧ ev c = 0

variable {V}

lemma kernelAt_mono (hV : Monotone V) : Monotone (kernelAt V ev) :=
  fun _ _ h => inf_le_inf_right _ (hV h)

/-- Compatibilità fra livelli: `K_n = K_{n+1} ∩ V_n`. -/
lemma kernelAt_compat (hV : Monotone V) (n : ℕ) :
    kernelAt V ev n = kernelAt V ev (n + 1) ⊓ V n := by
  apply le_antisymm
  · exact le_inf (kernelAt_mono ev hV (Nat.le_succ n)) inf_le_left
  · intro x ⟨⟨_, hk⟩, hn⟩
    exact ⟨hn, hk⟩

/-- Esaustività: `⋃_n K_n = (⋃_n V_n) ∩ ker ev_u`; con `⋃ V_n = O` è `Ann(u)`. -/
theorem iSup_kernelAt (hV : Monotone V) :
    ⨆ n, kernelAt V ev n = (⨆ n, V n) ⊓ LinearMap.ker ev := by
  apply le_antisymm
  · exact iSup_le fun n => inf_le_inf_right _ (le_iSup V n)
  · rintro x ⟨hx, hk⟩
    obtain ⟨n, hn⟩ := (Submodule.mem_iSup_of_directed V hV.directed_le).mp hx
    exact Submodule.mem_iSup_of_mem n ⟨hn, hk⟩

/-- Misfit al livello `n` ⟺ `ev_u` è iniettiva su `V_n` ⟺ `K_n = 0`. -/
theorem not_fit_iff (n : ℕ) :
    ¬ Fit V ev n ↔ kernelAt V ev n = ⊥ := by
  rw [Submodule.eq_bot_iff]
  constructor
  · rintro h x ⟨hx, hk⟩
    by_contra hne
    exact h ⟨x, hx, hne, hk⟩
  · rintro h ⟨x, hx, hne, hk⟩
    exact hne (h x ⟨hx, hk⟩)

/-- Il fit si conserva salendo di livello. -/
theorem fit_mono (hV : Monotone V) {m n : ℕ} (hmn : m ≤ n) (h : Fit V ev m) : Fit V ev n := by
  obtain ⟨c, hc, hne, hk⟩ := h
  exact ⟨c, hV hmn hc, hne, hk⟩

/-- **Passo di rango (DICT-N1iii).** `dim V_n ≤ dim K_n + dim(im ev_u)`. -/
theorem finrank_le_kernelAt_add (n : ℕ) [FiniteDimensional 𝕜 (V n)]
    [FiniteDimensional 𝕜 (LinearMap.range ev)] :
    finrank 𝕜 (V n) ≤ finrank 𝕜 (kernelAt V ev n) + finrank 𝕜 (LinearMap.range ev) := by
  let φ : V n →ₗ[𝕜] LinearMap.range ev :=
    (ev.comp (V n).subtype).codRestrict _ fun x => LinearMap.mem_range_self ev x
  have h1 := LinearMap.finrank_range_add_finrank_ker φ
  have h2 : finrank 𝕜 (LinearMap.range φ) ≤ finrank 𝕜 (LinearMap.range ev) :=
    Submodule.finrank_le _
  have h3 : LinearMap.ker φ = (kernelAt V ev n).comap (V n).subtype := by
    ext x
    simp only [LinearMap.mem_ker, Submodule.mem_comap, Submodule.coe_subtype, kernelAt,
      Submodule.mem_inf, SetLike.coe_mem, true_and, φ]
    rw [Subtype.ext_iff]
    rfl
  have h4 : finrank 𝕜 (LinearMap.ker φ) = finrank 𝕜 (kernelAt V ev n) := by
    rw [h3]
    exact (Submodule.comapSubtypeEquivOfLe (inf_le_left : kernelAt V ev n ≤ V n)).finrank_eq
  omega

/-- Livelli dati da insiemi finiti di atomi: `V_n = span 𝓓_n` ha dimensione finita. -/
example (D : Finset O) : FiniteDimensional 𝕜 (Submodule.span 𝕜 (D : Set O)) := inferInstance

end Abstract

/-! ## Istanza a coefficienti costanti: `V_n = R_{≤n}` -/

section ConstCoeff

variable {σ 𝕜 F : Type*} [Field 𝕜] [AddCommGroup F] [Module (MvPolynomial σ 𝕜) F]
  [Module 𝕜 F] [IsScalarTower 𝕜 (MvPolynomial σ 𝕜) F]

/-- `R_{≤n}`: polinomi di grado totale `≤ n` (span di `𝓓_n = {ζ^α : |α| ≤ n}`). -/
noncomputable abbrev Rle (n : ℕ) : Submodule 𝕜 (MvPolynomial σ 𝕜) := MvPolynomial.restrictTotalDegree σ 𝕜 n

lemma Rle_mono : Monotone (Rle (σ := σ) (𝕜 := 𝕜)) := by
  intro m n h p hp
  rw [MvPolynomial.mem_restrictTotalDegree] at hp ⊢
  exact hp.trans h

/-- Esaustività: `⋃_n R_{≤n} = R`. -/
lemma iSup_Rle : ⨆ n, Rle (σ := σ) (𝕜 := 𝕜) n = ⊤ := by
  rw [eq_top_iff]
  intro p _
  exact Submodule.mem_iSup_of_mem p.totalDegree
    ((MvPolynomial.mem_restrictTotalDegree σ _ p).mpr le_rfl)

/-- Moltiplicatività: `R_{≤m} · R_{≤n} ⊆ R_{≤m+n}`. -/
lemma mul_mem_Rle {m n : ℕ} {p q : MvPolynomial σ 𝕜} (hp : p ∈ Rle (𝕜 := 𝕜) m)
    (hq : q ∈ Rle (𝕜 := 𝕜) n) : p * q ∈ Rle (𝕜 := 𝕜) (m + n) := by
  rw [MvPolynomial.mem_restrictTotalDegree] at hp hq ⊢
  exact (MvPolynomial.totalDegree_mul p q).trans (add_le_add hp hq)

/-- `ev_u : R → F`, `Q ↦ Q • u`. -/
noncomputable def evAt (u : F) : MvPolynomial σ 𝕜 →ₗ[𝕜] F :=
  (LinearMap.toSpanSingleton (MvPolynomial σ 𝕜) F u).restrictScalars 𝕜

/-- Esaustività dei nuclei: `⋃_n (Ann(u) ∩ R_{≤n}) = Ann(u)`. -/
theorem iSup_kernelAt_Rle (u : F) :
    ⨆ n, kernelAt (Rle (σ := σ) (𝕜 := 𝕜)) (evAt u) n = LinearMap.ker (evAt u) := by
  rw [iSup_kernelAt _ Rle_mono, iSup_Rle, top_inf_eq]

/-- **DICT-GR (b) / R2:** se `L u = 0`, allora `(L) ∩ R_{≤n} ⊆ Ann(u) ∩ R_{≤n}`. -/
theorem consequences_le_kernelAt (u : F) {L : MvPolynomial σ 𝕜} (hL : L • u = 0) (n : ℕ) :
    (Ideal.span {L}).restrictScalars 𝕜 ⊓ Rle n ≤ kernelAt (Rle (σ := σ) (𝕜 := 𝕜)) (evAt u) n := by
  rintro x ⟨hx, hn⟩
  refine ⟨hn, ?_⟩
  obtain ⟨c, rfl⟩ := Ideal.mem_span_singleton'.mp hx
  simp [evAt, mul_smul, hL]

/-- **Passo di rango di DICT-N1iii a coefficienti costanti:**
`dim R_{≤n} ≤ dim(Ann(u) ∩ R_{≤n}) + dim_𝕜 (R·u)` quando `R·u` ha dimensione finita. -/
theorem finrank_Rle_le (u : F) (n : ℕ) [FiniteDimensional 𝕜 (Rle (σ := σ) (𝕜 := 𝕜) n)]
    [FiniteDimensional 𝕜 (LinearMap.range (evAt (σ := σ) (𝕜 := 𝕜) u))] :
    finrank 𝕜 (Rle (σ := σ) (𝕜 := 𝕜) n) ≤
      finrank 𝕜 (kernelAt (Rle (σ := σ) (𝕜 := 𝕜)) (evAt u) n) +
        finrank 𝕜 (LinearMap.range (evAt (σ := σ) (𝕜 := 𝕜) u)) :=
  finrank_le_kernelAt_add _ n

end ConstCoeff

end PBLean.F10.Filtration
