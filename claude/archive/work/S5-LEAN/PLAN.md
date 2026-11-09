# PLAN S5-LEAN — Fase 5: formalizzazione Lean 4 + Mathlib

Skill caricate (lette per intero, workflow seguito): skills-local/session-protocol, skills-local/formalize-claim, _vendor/.../lean-formalize/SKILL.md (solo istruzioni; nessuno script _vendor eseguito), proof-checker (revisore = subagente Claude fresco, solo confronto enunciato formale/informale).
Input letti: claims/LEDGER.md (v2), RIPRESA.md (ultimo AGGIORNAMENTO), research/R2/REPORT.md §R2-T2, research/R5/REPORT.md §R5-T2, work/II/PROOF_PACKAGE.md §II-T3, §II-P5, work/C1C2/PROOF_PACKAGE.md §C12-L3, §C12-P2, §C12-P3.
Ambiente: Lean 4.35.0, progetto C:\Users\<user>\PBLean (Mathlib v4.35.0 già costruito). Niente `lake update`, niente cambio di versione.

## Bersagli (in ordine)
| # | claim | stato LEDGER | file Lean | forma prevista |
|---|---|---|---|---|
| 1 | R5-T2(i) nucleo algebrico | DIMOSTRATO | PBLean/R5T2.lean | (a) anello commutativo: Π(1+x_n) = Σ_S Π_{n∈S} x_n e scomposizione u = u₀ + Σ x_n u₀ + E, E = Σ_{|S|≥2}; (b) endomorfismi a due a due commutanti S_n di un modulo: (S_0⋯S_{N−1})u₀ = Σ_T Π_{n∈T}(S_n − I)u₀ (prodotto ordinato = composizione) |
| 2 | II-T3 esistenza (fix F2) | DIMOSTRATO | PBLean/IIT3.lean | R comm., M R-modulo, aP₁+bP₂=1 ⇒ ker(P₁P₂) = ker P₁ ⊔ ker P₂, Disjoint, (bP₂) proiettore su ker P₁ lungo ker P₂ |
| 3 | R2-T2 livello L0 (punto 2 e 4, n=1) | DIMOSTRATO (R2 REPORT) | PBLean/R2T2.lean | T endomorfismo di un K-spazio, p,q coprimi in K[X] ⇒ ker(pq)(T) = ker p(T) ⊕ ker q(T) (via lemmi Mathlib) |
| 4 | C12-P2, C12-P3 | **PROVA SCRITTA (non auditata)** nel package C1C2 — da segnalare | PBLean/C12P2.lean | K campo con 2 ≠ 0 (generalizza ℂ): τ²+bτ+c ∈ K[ξ][τ] non irriducibile ⟺ b²−4c quadrato in K[ξ]; τ − a irriducibile |
| 5 | II-P5 caso k=2 | DIMOSTRATO | PBLean/IIP5.lean | C = !![0,1;−p₀,−p₁] su ℂ: C Cᴴ = Cᴴ C ⟺ ‖p₀‖ = 1 ∧ conj p₀ · p₁ = −conj p₁ (forma esatta del package, verificata a mano dal commutatore) |
| 6 | (facoltativo) II-T3 (i)⟺(ii) = C12-L3(c) | DIMOSTRATO | PBLean/IIT3Null.lean | in ℂ[τ,ξ] (MvPolynomial (Fin 2) ℂ): (P₁,P₂) = ⊤ ⟺ nessuno zero comune in ℂ² (Nullstellensatz di Mathlib) |

## Procedura per ciascuno
Enunciato formale → confronto riga per riga col testo informale (specializzazioni dichiarate) → prova → `lake build` → `#print axioms` (ammessi solo propext, Classical.choice, Quot.sound) → nessun `sorry`/`axiom` → revisione da subagente fresco (solo confronto) → PROOF_PACKAGE.md aggiornato man mano → copia in D:\ProblemaBase\PBLean_src\.
Se un bersaglio non chiude in tempo ragionevole: stato "non formalizzato" con motivo (mai sorry).

## Criterio di "fatto"
Bersagli 1–5 compilati con assiomi standard (o motivati come non formalizzati); PROOF_PACKAGE.md; TABELLA in inbox/central.md; sorgenti in PBLean_src; DONE S5-LEAN.

## Scritture
Solo C:\Users\<user>\PBLean\, D:\ProblemaBase\PBLean_src\, D:\ProblemaBase\work\S5-LEAN\, inbox/.
