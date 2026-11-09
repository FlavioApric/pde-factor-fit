import Mathlib

/-!
# Invarianza di gauge dell'identificazione, parte algebrica (S10-LEAN, bersaglio 3)

Claim (LEDGER Fase 8, S8-SYS): G-L0 (covarianza degli operatori nelle `∇_μ`), G-T2(b)
(con dati invarianti si identifica al più l'orbita di gauge) e SYS-N3(c), ultima frase (una
trasformazione di gauge che fissa `u` con `u` non divisore di zero è `g = 1`).
Non formalizzati (analisi/topologia): G-T2(a) (olonomie, de Rham), SYS-N3(a)–(c) parte
analitica (principio del massimo).

Quadro algebrico: `K` anello commutativo di funzioni (nel progetto `C^∞(Ω; ℂ)`), `𝕜` campo dei
coefficienti costanti (`ℂ`), `∂_μ : K → K` derivazioni `𝕜`-lineari, potenziale `a_μ ∈ K`
(nel progetto `a_μ = i A_μ`), `∇_μ u := ∂_μ u − a_μ u` sulle componenti di `u ∈ K^k`.
Gauge: `g ∈ Kˣ` (nel progetto `g : Ω → U(1)`), `a′_μ := a_μ + g⁻¹ ∂_μ g`, cioè
`A′ = A + (1/i) g⁻¹ dg`.
Operatori: ogni polinomio non commutativo `F` a coefficienti in `𝕜` nelle `∇_μ` e in una
famiglia di operatori `K`-lineari `V_i` su `K^k` (potenziali moltiplicativi, anche matriciali,
e matrici costanti), valutato con `FreeAlgebra.lift`.
-/

namespace PBLean.F10.Gauge

variable {𝕜 K : Type*} [CommRing 𝕜] [CommRing K] [Algebra 𝕜 K]
variable {n ι k : Type*}

/-- Moltiplicazione per `g ∈ K` sulle componenti di `u ∈ K^k`. -/
def gmul (g : K) : Module.End 𝕜 (k → K) where
  toFun u j := g * u j
  map_add' u v := by funext j; simp [mul_add]
  map_smul' c u := by funext j; simp [mul_smul_comm]

lemma gmul_apply (g : K) (u : k → K) (j : k) : gmul (𝕜 := 𝕜) g u j = g * u j := rfl

/-- Derivata covariante `∇_μ u = ∂_μ u − a_μ u`. -/
def nabla (D : n → Derivation 𝕜 K K) (a : n → K) (μ : n) : Module.End 𝕜 (k → K) where
  toFun u j := D μ (u j) - a μ * u j
  map_add' u v := by funext j; simp [mul_add]; abel
  map_smul' c u := by funext j; simp [smul_sub, mul_smul_comm]

lemma nabla_apply (D : n → Derivation 𝕜 K K) (a : n → K) (μ : n) (u : k → K) (j : k) :
    nabla (k := k) D a μ u j = D μ (u j) - a μ * u j := rfl

/-- Potenziale trasformato `a′_μ = a_μ + g⁻¹ ∂_μ g`. -/
def gaugeTransform (D : n → Derivation 𝕜 K K) (g : Kˣ) (a : n → K) : n → K :=
  fun μ => a μ + ↑g⁻¹ * D μ g

/-- **G-L0 (generatori).** `∇^{a′}_μ (g u) = g ∇^a_μ u`. -/
theorem nabla_covariant (D : n → Derivation 𝕜 K K) (g : Kˣ) (a : n → K) (μ : n) (u : k → K) :
    nabla D (gaugeTransform D g a) μ (gmul (𝕜 := 𝕜) (g : K) u) = gmul (𝕜 := 𝕜) (g : K) (nabla D a μ u) := by
  funext j
  simp only [nabla_apply, gmul_apply, gaugeTransform, Derivation.leibniz, smul_eq_mul]
  have h := g.inv_mul
  linear_combination (-(D μ g * u j)) * h

/-- Valutazione di un polinomio non commutativo `F` nelle `∇_μ` (generatori `inl μ`) e nei
potenziali `K`-lineari `V_i` (generatori `inr i`). -/
noncomputable def op (D : n → Derivation 𝕜 K K) (V : ι → Module.End K (k → K)) (a : n → K) :
    FreeAlgebra 𝕜 (n ⊕ ι) →ₐ[𝕜] Module.End 𝕜 (k → K) :=
  FreeAlgebra.lift 𝕜 (Sum.elim (nabla D a) fun i => (V i).restrictScalars 𝕜)

/-- **G-L0.** Per ogni operatore `L_A` polinomiale nelle `∇_μ`, con coefficienti costanti e
potenziali moltiplicativi (anche matriciali): `L_{A′} ∘ g = g ∘ L_A`. -/
theorem op_covariant (D : n → Derivation 𝕜 K K) (V : ι → Module.End K (k → K)) (g : Kˣ)
    (a : n → K) (F : FreeAlgebra 𝕜 (n ⊕ ι)) :
    op D V (gaugeTransform D g a) F * gmul (𝕜 := 𝕜) (g : K) =
      gmul (𝕜 := 𝕜) (g : K) * op D V a F := by
  induction F using FreeAlgebra.induction with
  | grade0 r =>
    rw [AlgHom.commutes, AlgHom.commutes, Algebra.commutes]
  | grade1 x =>
    cases x with
    | inl μ =>
      apply LinearMap.ext
      intro u
      simp only [op, FreeAlgebra.lift_ι_apply, Sum.elim_inl, Module.End.mul_apply]
      exact nabla_covariant D g a μ u
    | inr i =>
      apply LinearMap.ext
      intro u
      simp only [op, FreeAlgebra.lift_ι_apply, Sum.elim_inr, Module.End.mul_apply,
        LinearMap.restrictScalars_apply]
      have : gmul (𝕜 := 𝕜) (g : K) u = (g : K) • u := rfl
      rw [this, LinearMap.map_smul]
      rfl
  | mul F G hF hG =>
    rw [map_mul, map_mul, mul_assoc, hG, ← mul_assoc, hF, mul_assoc]
  | add F G hF hG =>
    rw [map_add, map_add, add_mul, mul_add, hF, hG]

/-- **Corollario (soluzioni).** `L_A u = 0 ⟺ L_{A′}(g u) = 0`: `Sol(L_{A′}) = g · Sol(L_A)`. -/
theorem sol_gauge (D : n → Derivation 𝕜 K K) (V : ι → Module.End K (k → K)) (g : Kˣ)
    (a : n → K) (F : FreeAlgebra 𝕜 (n ⊕ ι)) (u : k → K) :
    op D V a F u = 0 ↔ op D V (gaugeTransform D g a) F (gmul (𝕜 := 𝕜) (g : K) u) = 0 := by
  have h := DFunLike.congr_fun (op_covariant D V g a F) u
  simp only [Module.End.mul_apply] at h
  rw [h]
  constructor
  · intro hu; rw [hu, map_zero]
  · intro hu
    funext j
    have := congrFun hu j
    rw [gmul_apply] at this
    have h' := congrArg (fun x : K => ((g⁻¹ : Kˣ) : K) * x) this
    simp only [Pi.zero_apply, mul_zero, ← mul_assoc, Units.inv_mul, one_mul] at h'
    exact h'

/-- **G-T2(b), parte algebrica.** Se un'osservazione `O` è invariante (`O(g u) = O(u)`), allora
`(A, u)` e `(A′, g u)` sono entrambe coppie operatore–soluzione con gli stessi dati: i dati
invarianti non distinguono `A` da `A′`. -/
theorem invariant_data_gauge {X : Type*} (O : (k → K) → X) (D : n → Derivation 𝕜 K K)
    (V : ι → Module.End K (k → K)) (g : Kˣ) (hO : ∀ u, O (gmul (𝕜 := 𝕜) (g : K) u) = O u)
    (a : n → K) (F : FreeAlgebra 𝕜 (n ⊕ ι)) (u : k → K) (hu : op D V a F u = 0) :
    op D V (gaugeTransform D g a) F (gmul (𝕜 := 𝕜) (g : K) u) = 0 ∧
      O (gmul (𝕜 := 𝕜) (g : K) u) = O u :=
  ⟨(sol_gauge D V g a F u).mp hu, hO u⟩

/-- **SYS-N3(c), ultima frase.** Una gauge che fissa `u` (`g u = u`), con una componente `u_j`
non divisore di zero, è `g = 1`. -/
theorem gauge_fixing_u_trivial (g : K) (u : k → K) (j : k) (hu : ∀ z : K, z * u j = 0 → z = 0)
    (hg : gmul (𝕜 := 𝕜) g u = u) : g = 1 := by
  have := congrFun hg j
  rw [gmul_apply] at this
  have h0 : (g - 1) * u j = 0 := by rw [sub_mul, one_mul, this, sub_self]
  exact sub_eq_zero.mp (hu _ h0)

end PBLean.F10.Gauge
