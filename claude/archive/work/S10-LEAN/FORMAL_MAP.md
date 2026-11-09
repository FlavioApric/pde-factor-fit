# FORMAL_MAP — S10-LEAN (Fase 10)

Progetto: `C:\Users\<user>\PBLean`, moduli `PBLean/F10/*.lean` (copia in `D:\ProblemaBase\PBLean_src\F10\`). Controllo assiomi: `PBLean/F10/Axioms.lean`. Per ogni teorema l'esito di `#print axioms` è riportato nella colonna «assiomi» (testo completo in `BUILD_LOG.md`). Abbreviazioni: **std** = `[propext, Classical.choice, Quot.sound]`; **pq** = `[propext, Quot.sound]`. Esito verificato con `lake build` del 27/10/2026: 85 dichiarazioni controllate (teoremi, lemmi e definizioni di `F10`), nessuna dipende da `sorryAx` o da altri assiomi. Nessun `sorry` nei sorgenti.

Legenda della portata: **piena** = l'enunciato formale dice quanto la riga del LEDGER (nella parte indicata); **parte** = formalizzata solo la parte algebrica nominata, il resto è dichiarato «fuori portata (libreria)» in fondo; **caso** = formalizzato un caso particolare dell'enunciato del LEDGER.

## 1. `F10/Morita.lean` — nuclei per moduli su Mat_k(R)

Quadro: `R` anello commutativo, `M` un `R`-modulo qualsiasi, `P ∈ Mat_{ℓ×k}(R)` agisce su `M^k` con `(Pu)_i = Σ_j P_ij • u_j` (`matOp`); `Sol_M(P) = ker matOp P`.

| ID LEDGER | nome Lean | enunciato formale in prosa | portata | assiomi |
|---|---|---|---|---|
| quadro SYS (Sol ≅ Hom(M_P, 𝒜), usato in SYS-T1, SYS-EX, SYS-S1) | `PBLean.F10.Morita.matEnd` | `P ↦ matOp P` è un omomorfismo di anelli `Mat_k(R) → End_R(M^k)`: `M^k` è un `Mat_k(R)`-modulo | piena | std |
| idem | `PBLean.F10.Morita.rowSpan_le_ker_iff` | per `u ∈ M^k`: `U_P = R^{1×ℓ}P` sta nel nucleo di `φ_u : r ↦ Σ_j r_j • u_j` se e solo se `P u = 0` | piena | std |
| idem | `PBLean.F10.Morita.malgrange` | isomorfismo `R`-lineare `Sol_M(P) ≅ Hom_R(R^{1×k}/U_P, M)` (composto di `solEquiv` e `quotHomEquiv`) | piena | std |
| SYS-C1 (passo det), CONV-MZ1 | `PBLean.F10.Morita.det_smul_eq_zero_of_mem_Sol` | `P ∈ Mat_k(R)`, `P u = 0` ⇒ `(det P) • u = 0` | piena (CONV-MZ1: `DU = 0 ⇒ (det D)U_i = 0`) | std |
| II-T3 per sistemi | `PBLean.F10.Morita.end_kernel_decomposition` | endomorfismi `T₁, T₂, a, b` di un `R`-modulo con `aT₁ + bT₂ = 1`, `T₁T₂ = T₂T₁`, `bT₁ = T₁b`, `aT₂ = T₂a`: `ker(T₁T₂) = ker T₁ ⊕ ker T₂`, `u = (bT₂)u + (aT₁)u` con le componenti nei due nuclei, `bT₂` è l'identità su `ker T₁` e nullo su `ker T₂` | estensione di II-T3 (ipotesi di commutazione esplicite) | std |
| idem | `PBLean.F10.Morita.matrix_kernel_decomposition` | `P₁, P₂, A, B ∈ Mat_k(R)` con `AP₁ + BP₂ = I`, `P₁P₂ = P₂P₁`, `BP₁ = P₁B`, `AP₂ = P₂A`: per ogni `R`-modulo `M`, `Sol_M(P₁P₂) = Sol_M(P₁) ⊕ Sol_M(P₂)` con `u = (BP₂)u + (AP₁)u` | idem | std |
| bersaglio 5 (spezzamento per det; collegato a SYS-C1) | `PBLean.F10.Morita.sol_split_of_det` | `P ∈ Mat_k(R)`, `det P = d₁d₂`, `ad₁ + bd₂ = 1`: `Sol_M(P) = (Sol_M(P) ∩ ker d₁) ⊕ (Sol_M(P) ∩ ker d₂)`, `d_i` scalare su ogni componente (`scalarKer d = ker(d•)` su `M^k`) | nuovo enunciato algebrico (nessuna riga LEDGER dedicata; conseguenza di SYS-C1 + II-T3) | std |

## 2. `F10/Dirac.lean` — fattorizzazione Dirac / Klein–Gordon

| ID LEDGER | nome Lean | enunciato formale in prosa | portata | assiomi |
|---|---|---|---|---|
| H-DIRAC (premessa), SYS-E1 | `PBLean.F10.Dirac.clifford_sq` | in ogni `R`-algebra `A`, se `γ_μ² = η_μ·1` e `γ_μγ_ν + γ_νγ_μ = 0` per `μ ≠ ν`, allora `(Σ_μ p_μγ_μ)² = (Σ_μ η_μ p_μ²)·1` per ogni `p` | piena (relazioni di Clifford in forma diagonale) | std |
| idem | `PBLean.F10.Dirac.massive_factor` | `(D − m)(D + m) = D² − m²` | piena | pq |
| idem | `PBLean.F10.Dirac.scalar_sub_mul_add` | `(a − S)(a + S) = (a + S)(a − S) = a² − S²` per `a ∈ R` scalare | piena | pq |
| idem | `PBLean.F10.Dirac.pauli_sq`, `pauli_anticomm` | le matrici di Pauli soddisfano `σ_i² = I`, `σ_iσ_j + σ_jσ_i = 0` (`i ≠ j`) | piena | std |
| H-DIRAC (C1) | `PBLean.F10.Dirac.XY_eq_KG` | in `Mat₂(ℂ[p₀,p₁,p₂,p₃])`, con `X = p₀I − σ·p`, `Y = p₀I + σ·p`: `XY = YX = KG·I₂`, `KG = p₀² − (p₁² + p₂² + p₃²)` | piena | std |
| Dirac² = KG (bersaglio 2) | `PBLean.F10.Dirac.diracChiral_sq` | `γ^μp_μ = [[0, X], [Y, 0]]` (chirale, `Mat₄`): `(γ^μp_μ)² = KG·I₄` | piena | std |
| H-DIRAC(a) (premessa) | `PBLean.F10.Dirac.dirac_massive` | `(γ·p − m)(γ·p + m) = (KG − m²)·I₄` per ogni `m ∈ ℂ[p]` | piena | std |
| H-DIRAC(d) (lemma) | `PBLean.F10.Dirac.antidiag_sq` | in `Mat₂(S)`, `S` commutativo: `[[0, x], [y, 0]]² = (xy)·I₂` | piena | std |
| H-DIRAC(d) (1+1) | `PBLean.F10.Dirac.dirac2_sq` | `[[0, p₀ − p₁], [p₀ + p₁, 0]]² = (p₀² − p₁²)·I₂` | piena | std |

Nota: H-DIRAC(a) («`M_D ≅ (R/q)²`», `q` primo) non è formalizzato: serve la primalità di `KG − m²` e l'isomorfismo di moduli (fuori portata in questa fase, vedi fondo).

## 3. `F10/Gauge.lean` — invarianza di gauge, parte algebrica

Quadro: `K` anello commutativo (funzioni), `𝕜` anello dei coefficienti costanti, `∂_μ` derivazioni `𝕜`-lineari di `K`, `∇_μ u = ∂_μ u − a_μu` componente per componente su `K^k` (nel progetto `a = iA`), gauge `g ∈ Kˣ`, `a′_μ = a_μ + g⁻¹∂_μg` (`gaugeTransform`; nel progetto `A′ = A + (1/i)g⁻¹dg`). Operatori `L_A = op D V a F`: `F` polinomio non commutativo a coefficienti in `𝕜` nelle `∇_μ` e in una famiglia di operatori `K`-lineari `V_i` di `K^k` (potenziali moltiplicativi anche matriciali, matrici costanti).

| ID LEDGER | nome Lean | enunciato formale in prosa | portata | assiomi |
|---|---|---|---|---|
| G-L0 | `PBLean.F10.Gauge.nabla_covariant` | `∇^{a′}_μ(gu) = g ∇^a_μ u` | piena | pq |
| G-L0 | `PBLean.F10.Gauge.op_covariant` | `L_{A′} ∘ (g·) = (g·) ∘ L_A` per ogni operatore polinomiale nelle `∇_μ` con coefficienti costanti e potenziali `K`-lineari | piena (anche per `g` non della forma `e^{iχ}` globale, come nella prova di G-T2(b)) | std |
| G-L0, G-T2(b) | `PBLean.F10.Gauge.sol_gauge` | `L_A u = 0 ⟺ L_{A′}(gu) = 0`, cioè `Sol(L_{A′}) = g·Sol(L_A)` | piena | std |
| G-T2(b) | `PBLean.F10.Gauge.invariant_data_gauge` | se `O(gu) = O(u)` per ogni `u`, ogni soluzione `u` di `L_A` dà la soluzione `gu` di `L_{A′}` con gli stessi dati `O`: i dati invarianti non distinguono `A` da `A′` | parte (la conclusione «si ricostruisce al più [A]» è questa indistinguibilità) | std |
| SYS-N3(c), ultima frase | `PBLean.F10.Gauge.gauge_fixing_u_trivial` | `g u = u` con una componente `u_j` non divisore di zero ⇒ `g = 1` | parte | pq |

## 4. `F10/Filtration.lean` — filtrazione a livello finito di 𝓓_n

Quadro astratto: `O` spazio degli operatori su un campo `𝕜`, `V_n` sottospazi crescenti (`V_n = span 𝓓_n`), `ev_u : O → F` lineare; `K_n = V_n ∩ ker ev_u` (`kernelAt`); `Fit n` := esiste `c ∈ V_n`, `c ≠ 0`, `ev_u c = 0`. Istanza: `O = 𝕜[ζ_σ]`, `V_n = R_{≤n}` (grado totale), `ev_u(Q) = Q • u` in un `R`-modulo `F`.

| ID LEDGER | nome Lean | enunciato formale in prosa | portata | assiomi |
|---|---|---|---|---|
| DICT §0 | `PBLean.F10.Filtration.kernelAt_mono` | `n ≤ m ⇒ K_n ⊆ K_m` | piena | std |
| DICT §0 | `PBLean.F10.Filtration.kernelAt_compat` | `K_n = K_{n+1} ∩ V_n` | piena | std |
| DICT §0 | `PBLean.F10.Filtration.iSup_kernelAt` | `⋃_n K_n = (⋃_n V_n) ∩ ker ev_u` | piena | std |
| DICT §0 (misfit) | `PBLean.F10.Filtration.not_fit_iff` | misfit al livello `n` ⟺ `K_n = 0` | piena | std |
| DICT-GR (livelli) | `PBLean.F10.Filtration.fit_mono` | fit a livello `m` e `m ≤ n` ⇒ fit a livello `n` | piena | pq |
| DICT-N1iii (passo di rango) | `PBLean.F10.Filtration.finrank_le_kernelAt_add` | `dim V_n ≤ dim K_n + dim(im ev_u)` (dimensioni finite) | parte (l'inclusione stretta richiede `dim R_{≤n} = C(n+N,N)`) | std |
| DICT §0, coeff. costanti | `PBLean.F10.Filtration.Rle_mono`, `iSup_Rle`, `mul_mem_Rle` | `R_{≤m} ⊆ R_{≤n}` per `m ≤ n`; `⋃ R_{≤n} = R`; `R_{≤m}R_{≤n} ⊆ R_{≤m+n}` | piena | std |
| DICT §0 / C3-L1 | `PBLean.F10.Filtration.iSup_kernelAt_Rle` | `⋃_n (Ann(u) ∩ R_{≤n}) = Ann(u)` | piena | std |
| DICT-GR (b), regola R2 | `PBLean.F10.Filtration.consequences_le_kernelAt` | `Lu = 0 ⇒ (L) ∩ R_{≤n} ⊆ Ann(u) ∩ R_{≤n}` | piena | std |
| DICT-N1iii (passo di rango) | `PBLean.F10.Filtration.finrank_Rle_le` | `dim R_{≤n} ≤ dim(Ann(u) ∩ R_{≤n}) + dim_𝕜(R·u)` se `R·u` ha dimensione finita | parte | std |

## 5. `F10/Comax.lean` — scomposizione comassimale per i sistemi

Quadro: `R` anello commutativo, `L` un `R`-modulo (nel progetto `R^{1×k}`), `𝒜` un `R`-modulo qualsiasi; per `U ≤ L`, `Sol(U) = {φ ∈ Hom_R(L, 𝒜) | φ|_U = 0}` (= `Hom_R(L/U, 𝒜)` per `quotHomEquiv`, e = `Sol_𝒜(P)` per `U = U_P` per `malgrange`).

| ID LEDGER | nome Lean | enunciato formale in prosa | portata | assiomi |
|---|---|---|---|---|
| SYS-S1(ii), prima parte | `PBLean.F10.Comax.Sol_sup` | `Sol(U₁ + U₂) = Sol(U₁) ∩ Sol(U₂)` su ogni `𝒜` | piena | std |
| SYS-S1(i⇐) con `N = 0`; estensione di II-T3 | `PBLean.F10.Comax.Sol_inf_of_sup_eq_top` | se `U₁ + U₂ = L`, allora per ogni `𝒜`: `Sol(U₁ ∩ U₂) = Sol(U₁) ⊕ Sol(U₂)` (somma e intersezione nulla). Con `U₁ ∩ U₂ = U_P` è «somma dei nuclei = Sol(P)» | caso `N = 0` (dove `Ext¹(N, 𝒜) = 0` è banale) | std |
| II-T3 (ponte) | `PBLean.F10.Comax.scalar_case` | `aP₁ + bP₂ = 1` ⇒ `(P₁) + (P₂) = R` e `(P₁) ∩ (P₂) = (P₁P₂)`: il caso `k = 1` di `Sol_inf_of_sup_eq_top` è II-T3 | piena | std |

## 6. Facoltativi

| ID LEDGER | nome Lean | enunciato formale in prosa | portata | assiomi |
|---|---|---|---|---|
| SYS-T0 (passo finale) | `PBLean.F10.SmithT0.socle_le_one_iff` | `K` algebricamente chiuso, `e : Fin r → K[X]` con `e_i ∣ e_j` per `i ≤ j`: `(∀z, #{i : e_i(z) = 0} ≤ 1) ⟺ e_i` unità per ogni `i < r − 1` | parte (non formalizzati: esistenza della forma di Smith per `M_P`, zoccoli, gcd dei minori, rinvio a SYS-EX) | std |
| DICT-N1(i) | `PBLean.F10.BaireN1.isMeagre_iUnion_compact` | `E` normato su un campo normato completo, di dimensione infinita: un'unione numerabile di compatti è magra | caso normato (non F-spazi come `C^∞(Ω)`, `S^m`) | std |
| DICT-N1(i) (lemma) | `PBLean.F10.BaireN1.interior_eq_empty_of_isCompact` | in tale `E` ogni compatto ha interno vuoto (Riesz) | piena per il caso normato | std |

## Fuori portata (libreria)
- Algebra di Weyl / polinomi di Ore: VAR-*, ENC-*, DICT-R6, DICT-RANGO (coefficienti variabili).
- C₀-semigruppi: VAR-P11, ENC-P0, ENC-P0′, POLE-N, CONV-T7 (Dyson/Magnus).
- Analisi e topologia: iniettività di `C^∞(ℝ^n)` (SYS-EX, SYS-S1(i⇒)), de Rham e `Ext¹` (SYS-S1(i⇐) con `N ≠ 0`), olonomie (G-T2(a)), principio del massimo (SYS-N3(c), esistenza dei `k`), Baire in F-spazi non normati e prevalenza (DICT-N1(i) generale, DICT-N1v), Carleman (VAR-L*).
- Algebra commutativa non disponibile in forma usabile: zoccoli, dualità di Matlis, sistemi inversi di Macaulay, `Ass(M_P)` via Fitting (SYS-EX, SYS-N1, SYS-C1, H-DIRAC(a)–(d), LAME-3); `dim R_{≤n} = C(n+N, N)` (inclusione stretta di DICT-N1iii).
- SYS-N3(a)(b): identità con `Re`/`Im` e `Δρ/ρ` su funzioni: richiederebbero un modello di `C^∞` con coniugio; non tentate.
