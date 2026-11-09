# CHECK_REQUEST — OP-R2 (per S-CHECK: audit proof-checker + kill-argument sui claim marcati KA)
File da auditare: work/OP-R2/PROOF_PACKAGE.md (autosufficiente salvo le dipendenze citate con stato LEDGER). Controlli: work/OP-R2/sympy/opr2_checks.py → opr2_checks.out (29/29 OK; D3 numerico a 60 cifre). Comando: `D:\ProblemaBase\.venv\Scripts\python.exe -u -I work/OP-R2/sympy/opr2_checks.py`.

## Claim e punti da controllare
| ID | enunciato | dove | punti critici per il revisore | KA |
|---|---|---|---|---|
| OPR2-L0 | calore con sorgente G_0 + ∂_xG_1: z ∈ H^m, ‖z‖ ≤ C(‖G_0‖+‖G_1‖)_{H^m} | §1 | norme L¹ dei nuclei; commutazione di ∂_t con Duhamel (sorgente nulla vicino a r = −1) | no |
| **OPR2-T1** | densità di ker_{H^m}(calore) + ker_{H^m}(trasporto) in ker_{H^m}P, P = (τ−ξ²)(τ+cξ), rettangolo, ogni m | §1 | Passo 2 (F ∈ H^m_loc via media lungo le corde); Passo 3(a) (traslati compatti in Ω); Passo 6 (ũ_1 ∈ H^m: supporti di θ_i, χ_i, ∇θ_i); Passo 7(ii) (χ_1(s) − θ_1 nullo dove F è cattivo); c = 0 via OPF-T5(b); compatibilità con OPF-O1 e O1-1 (AUDIT_OP-FUN: ostruzione per simmetrie globali, qui locali) | **sì** (chiude OPF-Q1 / P2-Q1 residuo) |
| OPR2-L1 | proiettori con prodotti compatti ⇒ somma chiusa (Fredholm) | §2 | Σ*Σ = I + compatto ⇒ immagine chiusa | no |
| **OPR2-T2** | trasporti reali, m = 0, Ω convesso, (H∠): somma chiusa ⟺ ogni classe parallela chiusa | §2 | stima HS ∫_Ω dz/(ℓ_pℓ_{p′}); nuclei di proiezione limitati (Gram) o ≤ C/ℓ; (⇒) via ambiguità EP di C12-T1′ | sì (risponde a OPF-Q2 nel candidato) |
| OPR2-C2a | candidato "due paralleli + uno trasversale": coppie chiuse ⇒ tripla chiusa | §2 | casi inf ℓ_v = 0 / inf ℓ_w = 0 | no |
| OPR2-L3, **OPR2-T3**, OPR2-P3′ | coeff. variabili: socle senza molteplicità (in part. fattori a due a due non simili in Frac(𝔄)[∂_t;δ]) ⇒ criterio con r ≤ m test D_iu ∉ 𝒯; socle con molteplicità ⇒ infiniti atomi | §3 | biiezione saturati ↔ 𝔎-sottomoduli (Ore, estensione di δ — CON-FONTE); Jordan–Hölder; uso di OP-ALG-T4 e della saturazione di L_u (OP-ALG-C1(iii)) | sì (chiude OP-ALG-Q1) |
| **OPR2-L2**, OPR2-C2 | P4-L7 su ogni Ω connesso, p₀ ∈ Ω∩(K∩ℝ)², u intera; ⇒ OP-ALG-T3(f) per ogni dominio | §3 | crescita a_k ≤ C^k; convergenza in ℂ²; indipendenza di g^{(i)}; centramento in p₀ di e | sì (chiude OP-ALG-Q2) |
| OPR2-P4 | δ_N(K) ≤ N+1 per K ≥ 2N (Novikov integrato) | §4 | (Nov) CON-FONTE come S4ID-T3(d); costante d'integrazione = 0 per decadimento | no |
| OPR2-L5, **OPR2-T5** | forma chiusa di δ_d; ‖u − v − νδ − dδ_d‖_{H^k} ≤ C(ν+|d|)² prima dello shock; E^add di KdV–Burgers con resto O((ν+|d|)²) | §5 | stime d'energia (antisimmetria di ∂³, dissipazione); bootstrap con (LWP) CON-FONTE; uso di k+1 nel Passo 2 | sì (chiude S4T-Q2) |
| OPR2-P6 | INT-Q1: nessuna relazione d'ordine ≤ 1 se r ≢ 0 | §6 | compatibilità −c′φ² = 0; analiticità in x per estendere l'ODE a ℝ | no |
| OPR2-P7 | un autovalore: J_u ⊆ J_{φ_κ} | §6 | condizionale a (SR) con derivate — CON-FONTE da verificare | no |
| OPR2-O8, OPR2-O9 | ostruzioni: soluzioni autosimili con J_u ≠ 0; p irriducibile compatibile con i vincoli di solitone e di S4ID-P8 | §6 | calcolo F2, F3 | no |

## Fonti da verificare (CIT-AUDIT)
Ipoellitticità del calore (Hörmander ALPDO II cap. 11); estensione di Stein (Singular Integrals cap. VI §3); Ore/Goodearl–Warfield (localizzazione, estensione delle derivazioni); (LWP) per KdV–Burgers con ν > 0 (Pazy §6.3, Henry cap. 3); Novikov 1974 / Lax 1975 (equazione stazionaria degli N-solitoni); Kay–Moses (solitone senza riflessione); risoluzione in solitoni con derivate (Grunert–Teschl 2009 senza derivate).

## Domande precise al revisore
1. OPR2-T1 Passo 7(iii): la continuità delle traslazioni per u_1 ∈ H^m(Ω_K) è applicata su supp∇θ_i ∩ Ω, i cui traslati restano in Ω_K: verificare che r, δ, ε siano scelti in quest'ordine senza circolarità.
2. OPR2-T2: la formula del nucleo di Π_pΠ_{p′} (fattore 1/|sin∠|) e il cambio di variabili nell'integrale HS.
3. OPR2-T3: la tesi "r ≤ ℓ ≤ m" e la scelta di D_i ∈ 𝔇 (denominatori sinistri).
4. OPR2-T5: il passaggio da Y′ ≤ … a √Y quando Y può annullarsi (usare (Y+η)^{1/2} e η → 0).
