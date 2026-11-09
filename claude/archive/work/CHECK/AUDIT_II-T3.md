# AUDIT II-T3 (+ corollario II-C2) — proiettori polinomiali ⟺ varietà disgiunte
Revisore: S-CHECK-2B · 25/10/2026
Fonte esaminata: SOLO `work/II/CHECK_REQUEST.md` §II-T3 e §Corollario II-C2.
Skill: session-protocol, claim-lifecycle, proof-checker, scientific-critical-thinking, sympy.
SymPy: `work/CHECK/sympy/audit_ii.py` → `audit_ii.out` sezione "II-T3 / II-C2" (OK, 10 controlli); `audit_round2.out` (OK).

**Verdetti: II-T3 PASS. II-C2 PASS-con-fix(II-C2-F1)** (solo terminologia: "forma iniziale" va detta "parte omogenea di grado massimo").

## 1. Enunciato canonico
P = P₁P₂, P₁,P₂ ∈ R = ℂ[τ,ξ] non costanti, senza fattori comuni; Ω ⊆ ℝ² aperto non vuoto; F = C^∞(Ω). TFAE: (i) V(P₁)∩V(P₂) = ∅ in ℂ²; (ii) (P₁,P₂) = R; (iii) R/(P) → R/(P₁)×R/(P₂) iso; (iv) ∃E₁ ∈ R: E₁ = id su ker_F P₁, E₁ = 0 su ker_F P₂; (v) ker_F P₁ ∩ ker_F P₂ = {0}.
II-C2: (i) ⇒ σ(P₁), σ(P₂) (parti omogenee di grado massimo) hanno uno zero comune in ℙ¹.

## 2. Micro-claim
| MC | Passo | Esito |
|---|---|---|
| MC-1 | (i)⟺(ii) Nullstellensatz debole | OK |
| MC-2 | (ii)⇒(iii) CRT per ideali comassimali | OK |
| MC-3 | (iii)⇒(ii) dalla suriettività | OK |
| MC-4 | (ii)⇒(iv) E₁ = bP₂ | OK: E₁u₂ = b(P₂u₂) = 0; E₁u₁ = (1 − aP₁)u₁ = u₁. Esempio non banale P₁ = τξ − 1, P₂ = ξ, −P₁ + τP₂ = 1, E₁ = τξ: verificato |
| MC-5 | (ii)⇒(v) | OK |
| MC-6 | (iv)⇒(i), (v)⇒(i) con w = e^{τ₀t+ξ₀x} | OK: w ∈ C^∞(Ω), w ≠ 0 perché Ω ≠ ∅; E₁w = w e E₁w = 0 |
| MC-7 | II-C2: Bézout in ℙ² | OK: due curve proiettive di grado ≥ 1 si intersecano sempre; se non si incontrano nel piano affine si incontrano su ζ = 0, dove P_i^h(τ,ξ,0) = σ(P_i) |

## 3. Problemi trovati
- **II-T3-F1 · scope (ipotesi superflue) · COSMETIC · MINOR.** "Non costanti" e "senza fattori comuni" non servono alle equivalenze (con un fattore comune (i)–(v) sono tutte false; con P₁ costante sono tutte vere). Innocue; segnalate perché l'enunciato potrebbe sembrare più ristretto di quanto è. Inoltre la prova usa di F solo che contenga gli esponenziali e sia un R-modulo: vale identica per D′(Ω), H^m_loc ecc. *Fix facoltativo:* WEAKEN (cioè allargare) le ipotesi.
- **II-T3-F2 · completamento utile, non un errore · MINOR (ADD_DERIVATION).** L'enunciato non dice che sotto (ii) vale anche l'**esistenza**: ker_F P = ker_F P₁ ⊕ ker_F P₂, con u = (bP₂)u + (aP₁)u, (bP₂)u ∈ ker P₁ e (aP₁)u ∈ ker P₂ (verificato su u = w₁ + w₂). È una riga e su Ω qualunque (non solo convesso) rende la scomposizione esplicita e polinomiale: vale la pena enunciarla, perché nel caso V(P₁)∩V(P₂) ≠ ∅ l'esistenza dipende dalla geometria di Ω (R2-T2 su convessi).
- **II-C2-F1 · NORMALIZATION_MISMATCH (terminologia) · UNCLEAR/LOCAL · MINOR.** "Forme iniziali" in algebra commutativa/tropicale indica spesso la parte di grado **minimo** (o rispetto a un peso). Con la parte di grado minimo l'enunciato è falso (P₁ = τ, P₂ = τ − 1: V disgiunte, parti di grado minimo τ e −1 senza zeri comuni). La prova usa P^h|_{ζ=0} = parte di grado **massimo** (simbolo principale). *Fix:* sostituire "forme iniziali" con "parti omogenee di grado massimo (simboli principali)".
- **II-C2-F2 · nota di scope.** Il viceversa è falso (verificato: P₁ = τ − ξ², P₂ = τ − ξ² − ξ hanno σ = −ξ² comune ma V∩V = {(0,0)}); S-II lo dichiara già ("viceversa falso").

## 4. Red team
| Tentativo | Esito |
|---|---|
| tre coppie disgiunte (τ, τ−1), (τ−ξ², τ−ξ²−1), (τξ−1, ξ) | Gröbner = [1]; σ con fattore lineare comune in tutte |
| coppia con un punto comune (τ, τ−ξ²) | 1 ∈ ker P₁ ∩ ker P₂: (v) falsa, come previsto |
| lettura "grado minimo" di σ | controesempio (F1 di II-C2) |
| viceversa di II-C2 | falso, già dichiarato |

## 5. Stato proposto
**II-T3: DIMOSTRATO** (prova completa, risultati classici citati correttamente: Nullstellensatz, CRT). Novità: bassa (riformulazione di fatti standard nel linguaggio dei nuclei), ma corretta.
**II-C2: DIMOSTRATO** con la correzione terminologica F1.
