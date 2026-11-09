# PLAN — S10-LEAN (Fase 10, formalizzazione del nucleo algebrico di Fase 8)

Progetto Lean: `C:\Users\<user>\PBLean` (Lean 4.35.0, Mathlib v4.35.0). Moduli nuovi in `PBLean/F10/*.lean`, importati da `PBLean.lean`; controllo assiomi in `PBLean/F10/Axioms.lean`. Copia dei sorgenti in `D:\ProblemaBase\PBLean_src\F10\`.

Requisiti: `lake build` passa; nessun `sorry`; `#print axioms` per ogni teorema, ammessi solo `propext`, `Classical.choice`, `Quot.sound`.

## Bersagli (uno per modulo)

| # | modulo | LEDGER | contenuto formale previsto |
|---|---|---|---|
| 1 | `F10/Morita.lean` | SYS (quadro: Sol(P) ≅ Hom(M_P, 𝒜)); SYS-C1 (passo det) | azione di Mat_{ℓ×k}(R) su M^k; isomorfismo di Malgrange Sol_M(P) ≅ Hom_R(R^{1×k}/R^{1×ℓ}P, M); II-T3 per matrici che commutano (Mat_k(R) agisce su M^k); Sol(P) ⊆ ker(det P) |
| 2 | `F10/Dirac.lean` | SYS-E1, H-DIRAC (C1: XY = YX = KG·I₂), FW-1 (premessa) | relazioni di Clifford astratte ⇒ (Σ p_μγ^μ)² = (Σ η^{μν}p_μp_ν)·1 e (D − m)(D + m) = (KG − m²)·1 in ogni R-algebra; istanza: matrici di Pauli e rappresentazione chirale, in Mat(ℂ[p₀,…,p₃]) |
| 3 | `F10/Gauge.lean` | G-L0, G-T2(b) e SYS-N3(c), parte algebrica | covarianza ∇_{a+g⁻¹∂g}(g u) = g ∇_a u in un anello differenziale; L_{A′}(g u) = g L_A u per ogni polinomio non commutativo nelle ∇_μ con coefficienti costanti e potenziali K-lineari (matriciali); g·Sol(L_A) = Sol(L_{A′}); g u = u con u non divisore di zero ⇒ g = 1 |
| 4 | `F10/Filtration.lean` | DICT §0 (livelli), DICT-N1(iii) (passo di rango), DICT-GR / R2 (⟨L⟩_n ⊂ nucleo) | filtrazione astratta V_n, nucleo a livello n K_n = V_n ∩ ker ev_u: monotonia, compatibilità K_n = K_{n+1} ∩ V_n, esaustività, fit/misfit; dim K_n ≥ dim V_n − dim(R·u); istanza R_{≤n} = polinomi di grado totale ≤ n, esaustiva e moltiplicativa |
| 5 | `F10/Comax.lean` | SYS-S1(ii) (prima parte), SYS-S1(i⇐) nel caso N = 0, estensione di II-T3 | per sottomoduli U₁, U₂ di R^{1×k}: Sol(U₁ + U₂) = Sol(U₁) ∩ Sol(U₂) sempre; se U₁ + U₂ = R^{1×k}, Sol(U₁ ∩ U₂) = Sol(U₁) ⊕ Sol(U₂) per ogni R-modulo 𝒜; spezzamento per fattori comassimali di det P |
| 6a | `F10/SmithT0.lean` (facoltativo) | SYS-T0, passo combinatorio | per invarianti e_1 ∣ … ∣ e_r ≠ 0 in ℂ[s]: (∀λ, #{i : e_i(λ) = 0} ≤ 1) ⟺ e_1, …, e_{r−1} unità |
| 6b | `F10/BaireN1.lean` (facoltativo) | DICT-N1(i) | in uno spazio normato completo di dimensione infinita su ℝ o ℂ, un'unione numerabile di compatti è magra (caso normato dell'enunciato per F-spazi) |

## Fuori portata (libreria)
- Algebra di Weyl / polinomi di Ore: tutti gli enunciati a coefficienti variabili (VAR-*, ENC-*, DICT-R6) non si formalizzano.
- C₀-semigruppi (VAR-P11, ENC-P0, CONV-T7 nella parte Dyson/Magnus).
- Analisi: iniettività di C^∞(ℝ^n) (Malgrange), de Rham, olonomie (G-T2(a)), principio del massimo (SYS-N3(c) per l'esistenza di k), Carleman, Peetre, Baire in F-spazi non normati, prevalenza.
- Teoria dei moduli che Mathlib non ha in forma usabile qui: zoccoli, dualità di Matlis, sistemi inversi di Macaulay, Ass(M_P) via Fitting (SYS-EX, SYS-C1, SYS-N1).
- Dimensione di R_{≤n} come coefficiente binomiale (serve per l'inclusione stretta di DICT-N1(iii)): si formalizza solo la disuguaglianza di rango.

## Revisore
Sessione separata: confronta ogni enunciato di `FORMAL_MAP.md` con la riga del LEDGER (stesse ipotesi, nessun indebolimento silenzioso; dove l'enunciato formale è una parte o un caso, `FORMAL_MAP.md` lo dichiara).
