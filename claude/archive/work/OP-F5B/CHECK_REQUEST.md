# CHECK_REQUEST — OP-F5B · 26/10/2026
Richiesta di audit (proof-checker, revisore = subagente Claude indipendente) e kill-argument per il pacchetto work/OP-F5B/PROOF_PACKAGE.md. Controlli dell'agente: work/OP-F5B/sympy/opf5b_checks.py → opf5b_checks.out (21/21 OK).

## Priorità
1. **OPF5B-T1** (§1; kill-argument richiesto: chiude P2-Q1 per ogni P su ogni convesso limitato e assorbe OPF-T5 e la densità di OPR2-T1). Punti da attaccare:
   - F1: enunciato esatto di Hörmander ALPDO II Thm 10.2.1 (E ∈ B^{loc}_{∞,P̃}) e numero; se la fonte desse solo E/cosh|x| ∈ B_{∞,P̃}, verificare che basti (si usa solo φE ∈ B_{∞,P̃} per φ ∈ C_c^∞).
   - Passo 2: geometria delle traslazioni locali su un convesso qualsiasi (punto y₀ ∈ Ω̄, raggio ερ/2, ε ≤ 1).
   - Passi 5–7: formula di Leibniz, stima ‖g‖_{2,k} ≤ CΣ‖w_i‖_{H^m} con k = k_m/P̃, costanti indipendenti da ε; che P(∂)v = 0 sull'intorno V_ε (uso di Σθ_i ≡ 1 su V).
   - Passo 8: convessità degli intorni metrici, mollificazione, applicazione di C12-T1′ in C^∞.
   - Coerenza con il LEDGER: nessuna somma "chiusa e non densa" è registrata altrove? (Atteso: no.)
2. **OPF5B-T2, P3, C4** (§2, EX-Q1): saturazione e localizzazione di Ore (per A_2 CON-FONTE); P3(vi) test di π-torsione; calcolo dell'azione destra su 𝒟/x𝒟 (D3) e iniettività (argomento del grado in η); u_G ∉ 𝒯_{A_1}.
3. **OPF5B-L5, T6, P7** (§3, OPR2-Q3 parziale): L_{Ru*}/𝔇P = ker E_R; necessità di (I); spezzamento per P_1(P_1 + c) e iniettività di J su moduli di rango 1.
4. **OPF5B-P8** (§4, OPR2-Q2′ parziale): unitarietà della Mellin con il peso r dr; struttura dei nuclei sul cono; indipendenza per monodromia (caso σ = 0: polo); stima |G_{jk}| ≤ C/|σ|.

## Domande per il revisore
- T1 usa solo C12-T1′, F1, F2 e lemmi elementari: c'è un passo che richieda ipotesi su P (ipoellitticità, simmetrie)?
- P3(iv): l'equivalenza "T4 alla lettera ⟺ assenza di π-torsione" è corretta in entrambe le direzioni (con (v) per la direzione negativa)?
- T6: la formulazione di "criterio a test finiti" coincide con quella di OP-ALG-C1(iv)?
