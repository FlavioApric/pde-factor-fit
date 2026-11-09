# KA OPF5A-T1 — aggiudicazione (S-CHECK-20, 26/10/2026)
Attacco: KA_OPF5A_T1_attack.md (subagente indipendente, solo input). Esito dell'attacco: **SURVIVES**.
Verifica dell'aggiudicatore (indipendente, AUDIT_OP-F5A.md §T1): tutti i passi rifatti a mano (identità ⟨ψ'⟩=0, ⟨zψ'⟩=2ν; ⟨z⟩=−νq/p²+E1; |E1|≤Cν^{3/2}/A⁵; ∫_{A≥m}A^{-3}dα≤3/m²; scala di Pearcey e λ=(4/κ3)^{1/4}; m(β)=−β^{-3}+O(β^{-5}); Γ_out(sin)=4log2).
Punti accolti (MINOR): (1) P = 1.188654 (non 1.18868): confermato da s20_opf5a (B=80: 1.1886538) e dall'attaccante (1.188654) ⇒ Γ(sin)=2.574948 [F5A-1]; (2) la variante di Γ per E^add non è dimostrata [F5A-2]; (3) C⁴ basta.
Numerica indipendente (s20_opf5a (2)): (e−ν|logν|)/ν = 2.57730, 2.57576, 2.57529 per ν=1e-4,1e-5,1e-6 → 2.5749–2.5751 (estrapolazione), coerente con Γ=2.57495.
**Verdetto: SURVIVES. Nessun errore analitico.**
