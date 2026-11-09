# PROOF_PACKAGE S5-LEAN — Fase 5: formalizzazione Lean 4 + Mathlib (26/10/2026)

Skill caricate: session-protocol, formalize-claim, lean-formalize (solo istruzioni; nessuno script _vendor), proof-checker (revisore = subagente Claude fresco, solo confronto enunciati).
Ambiente: Lean 4.35.0, Mathlib v4.35.0 (progetto C:\Users\<user>\PBLean; nessun `lake update`, nessun cambio di versione).
Sorgenti: C:\Users\<user>\PBLean\PBLean\*.lean, copiati in D:\ProblemaBase\PBLean_src\ (con lakefile, toolchain, manifest). Entry point `PBLean.lean` importa tutti i moduli; `PBLean/Axioms.lean` esegue `#print axioms`.
**Build:** `lake build` → `Build completed successfully (9056 jobs)` (log: work/S5-LEAN/build.log). Nessun `sorry`, nessun `axiom` aggiunto (grep sui sorgenti: 0 occorrenze).
**Assiomi:** tutti i 15 teoremi esportati dipendono **solo** da `[propext, Classical.choice, Quot.sound]`.
**Nota tecnica:** i primi due `lake build` paralleli sono falliti con `failed to read file …olean.private` (I/O di Mathlib sotto build concorrente su Windows, non errori del codice); al terzo tentativo build completa. Ogni file era già stato compilato singolarmente con `lake env lean` senza errori.
**Revisione (proof-checker, subagente fresco, read-only):** nessun CRITICAL/MAJOR, nessun MISMATCH, nessun rischio di vacuità. 2 MINOR su C12P2.lean (omissioni non dichiarate) → **recepiti**: aggiunta nel header la riga "Fuori portata".

---

## 1. R5-T2(i), nucleo algebrico — FORMALIZZATO
- **Informale** (research/R5/REPORT.md [R5-T2]; LEDGER R5-T2(i–iii) DIMOSTRATO): termini a due a due commutanti, u = Σ_{S⊆[N]} Π_{n∈S}(S_n−I)u₀, E_int^add = Σ_{|S|≥2} Π_{n∈S}(S_n−I)u₀.
- **File:** PBLean/R5T2.lean. **Teoremi:**
  - `prod_one_add_eq_sum_powerset` : `∏ n ∈ s, (1 + x n) = ∑ T ∈ s.powerset, ∏ n ∈ T, x n` (A anello commutativo).
  - `prod_one_add_smul_decomp` : `(∏ n ∈ s, (1 + x n)) • u₀ = u₀ + ∑ n ∈ s, x n • u₀ + ∑ T ∈ s.powerset with 2 ≤ T.card, (∏ n ∈ T, x n) • u₀` (M un A-modulo).
  - `prod_one_add_decomp` (versione d'anello).
  - `commuting_endomorphisms_decomp` : per `S : Fin N → Module.End R M` con `∀ i j, Commute (S i) (S j)`: `(List.ofFn S).prod = ∑ T, (List.ofFn fun n => if n ∈ T then S n - 1 else 1).prod` e `∀ u₀, (List.ofFn S).prod u₀ = u₀ + ∑ n, (S n - 1) u₀ + ∑ T with 2 ≤ T.card, (…).prod u₀`.
- **Specializzazione dichiarata:** a t fissato, S_n := S_n(t) come endomorfismi lineari (la continuità non interviene). Fuori portata: u(t) = Π S_n(t)u₀ soluzione mild (R5-T1, CON-FONTE), topologia di Banach, stime di costo (ii–iii).
- **Revisione:** MATCH-WITH-DECLARED-SPECIALIZATION.

## 2. II-T3, esistenza nel caso comassimale (fix II-T3-F2) — FORMALIZZATO
- **Informale** (work/II §[II-T3] fix F2; LEDGER II-T3 DIMOSTRATO): con aP₁+bP₂=1, per ogni R-modulo F: ker P = ker P₁ ⊕ ker P₂, u = (bP₂)u + (aP₁)u, (bP₂)u ∈ ker P₁, (aP₁)u ∈ ker P₂; E₁ = bP₂ proiettore (E₁u₁ = u₁, E₁u₂ = 0).
- **File:** PBLean/IIT3.lean. **Teorema** `kernel_decomposition` (R anello commutativo, M R-modulo, `smulKer r := ker (lsmul R M r)`): `smulKer (P₁*P₂) = smulKer P₁ ⊔ smulKer P₂ ∧ Disjoint … ∧ (∀ u ∈ ker(P₁P₂), (b*P₂)•u ∈ ker P₁ ∧ (a*P₁)•u ∈ ker P₂ ∧ u = (b*P₂)•u + (a*P₁)•u) ∧ (∀ u ∈ ker P₁, (b*P₂)•u = u) ∧ (∀ u ∈ ker P₂, (b*P₂)•u = 0) ∧ (idempotenza su ker(P₁P₂))`.
- **Generalizzazione:** R qualsiasi (nel progetto R = ℂ[τ,ξ] che agisce via ∂). **Revisione:** MATCH.

## 3. R2-T2 al livello L0 (punti 2 e 4, n = 1) — FORMALIZZATO
- **Informale** (research/R2/REPORT.md [R2-T2]): f,g coprimi ⇒ ker(fg) = ker f + ker g; n = 1: coprimi ⇒ (f,g) = R (Bézout) ⇒ somma diretta.
- **File:** PBLean/R2T2.lean. **Teoremi:** `ker_mul_eq_sup_of_relPrime` (K campo, V K-spazio, T : V →ₗ V, `IsRelPrime p q`): `ker (aeval T (p*q)) = ker (aeval T p) ⊔ ker (aeval T q) ∧ Disjoint …`; `span_eq_top_of_relPrime`: `Ideal.span {p, q} = ⊤`. Prova: `Polynomial.sup_ker_aeval_eq_ker_aeval_mul_of_coprime`, `Polynomial.disjoint_ker_aeval_of_isCoprime`, `IsRelPrime.isCoprime`.
- **Specializzazione dichiarata:** solo n = 1 (L0); per n ≥ 2 il punto 2 (che richiede Ext¹ = 0 / C12-L2) non è formalizzato. **Revisione:** MATCH-WITH-DECLARED-SPECIALIZATION.

## 4. C12-P2 / C12-P3 — FORMALIZZATI (parte algebrica)
- **Attenzione di stato:** nel package C1C2 sono "prova scritta (elementare, non auditata)", senza riga propria nel LEDGER v2. La formalizzazione Lean ne verifica meccanicamente la parte algebrica (proposta: promuovere quella parte).
- **File:** PBLean/C12P2.lean (K campo con `NeZero (2:K)`, generalizza ℂ; `K[X][X]` = K[ξ][τ]). **Teoremi:**
  - `quadratic_reducible_iff` : `¬ Irreducible (X^2 + C b * X + C c) ↔ ∃ d, b^2 - 4*c = d^2`.
  - `quadratic_factor` : se b²−4c = d², `X^2 + C b X + C c = (X − C a₊)(X − C a₋)`, a± = 2⁻¹(−b ± d).
  - `X_sub_C_irreducible` : `Irreducible (X - C a)`.
  - `first_order_factor` : p₁ ≠ 0 ⇒ ∃ P̃, `C p₁ * X - C p₀ = C (gcd p₁ p₀) * P̃ ∧ Irreducible P̃`.
- **Fuori portata (dichiarato nel header):** δ(P) = deg d, caso d = 0 come unica componente primaria, descrizione delle componenti/nuclei in C12-P3. **Revisione:** MATCH-WITH-DECLARED-SPECIALIZATION (2 MINOR recepiti).

## 5. II-P5, caso k = 2 — FORMALIZZATO
- **Informale** (work/II §[II-P5](c), (1)⟺(4) per k = 2, fix F1; LEDGER II-P5 DIMOSTRATO): compagna di s²+p₁s+p₀ normale ⟺ |p₀| = 1 e p̄₀p₁ = −p̄₁. Forma verificata a mano: CC*−C*C = [[1−|p₀|², −p̄₁−p̄₀p₁],[−p₁−p₀p̄₁, |p₀|²−1]].
- **File:** PBLean/IIP5.lean. **Teoremi:** `companion2_normal_iff` : `C * Cᴴ = Cᴴ * C ↔ ‖p₀‖ = 1 ∧ conj p₀ * p₁ = -conj p₁` con `C = !![0, 1; -p₀, -p₁]`; `companion2_isStarNormal_iff` (stessa equivalenza con `IsStarNormal`).
- Fuori portata: k = 1, k ≥ 3, equivalenze con (2), (3). **Revisione:** MATCH.

## 6. (facoltativo) II-T3 (i)⟺(ii) = C12-L3(c) — FORMALIZZATO
- **Informale:** (P₁,P₂) = R ⟺ V(P₁)∩V(P₂) = ∅ in ℂ² (Nullstellensatz debole).
- **File:** PBLean/IIT3Null.lean. **Teoremi:** `span_pair_eq_top_iff_no_common_zero` (K alg. chiuso, σ finito): `Ideal.span {P₁, P₂} = ⊤ ↔ ¬ ∃ x, eval x P₁ = 0 ∧ eval x P₂ = 0`; `ii_t3_i_iff_ii_C2` (K = ℂ, σ = Fin 2). Prova: `MvPolynomial.isMaximal_iff_eq_vanishingIdeal_singleton`.
- Ipotesi f,g ≠ 0 di C12-L3 non necessaria (rafforzamento dichiarato). **Revisione:** MATCH.

## Non formalizzati
- C3-L3(b) (indipendenza lineare di esponenziali-polinomi): non tentato — richiede un modello di funzioni/distribuzioni e derivate non presente in forma utilizzabile; fuori dal "senza grandi librerie".
- Parti analitiche di tutti i claim sopra (spazi di funzioni, ∂ come azione di R, semigruppi C₀): modellate astrattamente come moduli/endomorfismi, come dichiarato.

## Output `#print axioms` (da build.log)
Tutti: `depends on axioms: [propext, Classical.choice, Quot.sound]` per R5T2.{prod_one_add_eq_sum_powerset, prod_one_add_smul_decomp, prod_one_add_decomp, commuting_endomorphisms_decomp}, IIT3.kernel_decomposition, R2T2.{ker_mul_eq_sup_of_relPrime, span_eq_top_of_relPrime}, C12P2.{quadratic_reducible_iff, quadratic_factor, X_sub_C_irreducible, first_order_factor}, IIP5.{companion2_normal_iff, companion2_isStarNormal_iff}, IIT3Null.{span_pair_eq_top_iff_no_common_zero, ii_t3_i_iff_ii_C2}.
