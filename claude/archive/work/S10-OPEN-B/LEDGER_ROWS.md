# LEDGER_ROWS — S10-OPEN-B (proposte per il coordinatore; nessuna scrittura in claims/LEDGER.md)

Formato: | ID | enunciato | ipotesi | stato | prova | SymPy | proof-checker | kill-argument | dipende da |

| ID | enunciato | ipotesi | stato | prova | SymPy | proof-checker | kill-argument | dipende da |
|---|---|---|---|---|---|---|---|---|
| S10B-T1 (= [F4⁻]) | N-solitone di Hirota, k_j = 2κ_j distinti: u ∈ 𝒮, b ≡ 0, a = Π(k−iκ_j)/(k+iκ_j), spettro {−κ_j²}; per ogni t | 0<κ_1<…<κ_N, c_j>0 | PROVA SCRITTA (da auditare) | PROOF_PACKAGE §1 | s10b_f4 21/22 + s10b_f4_f5check (F5 N=3 OK con evalf esatto) | richiesto | richiesto | OPF5D-L3, L4 |
| INT-T1(B) | come OPF5D-T3 | — | PROVA SCRITTA mod audit di S10B-T1 | §1 | — | richiesto | — | OPF5D-T3, S10B-T1 |
| S10B-T2 (OPF5C-T5 senza fonte) | J primo differenziale ≠ 0 in F{y}, car 0: J = [A]:H_A^∞, A di rango minimo | una indeterminata, una derivazione | PROVA SCRITTA (classica) | §2 | — | richiesto | — | — |
| S10B-P3 (OPA-Q2, densità) | Morse+(SB) densa in C^r(𝕋), r ≥ 3; con apertura: aperta e densa | — | PROVA SCRITTA (da auditare) | §3 | — | richiesto | richiesto | OPF5A-L4, F5A-11, F5A-12 (apertura) |
| S10B-L4 (= L-loc) | localizzazione delle nascite: 2ν log(1/max(|t−t_b|,√ν)) + O(ν) dentro, O(ν) fuori | Morse+(SB), u_0 ∈ C^5 | PROVA SCRITTA (da auditare; rischio in §4.4) | §4 | — | richiesto | richiesto (Lemma U con margine) | OPF5A-L2, L3, L3′, T1, T2, Lemma U, [F1] |
| OPF5A-C1 (= OPA-Q1) | globale su (0,T] per Morse+(SB) | come C1 | PROVA SCRITTA mod [F1], mod audit di S10B-L4 | §4.5 | — | richiesto | — | S10B-L4, [F1] |
| S10B-C1 | Ω = (0,3)²∖[1,2]², P = ∂x∂y: ker Q_1 + ker Q_2 non denso in ker_{H^m} P (neanche in L²) | — | CONTROESEMPIO (PROVA SCRITTA + V-ex) | §5 | s10b_annulus 3/3 | richiesto | — | — |
| S10B-T3 (= [Hm]) | sup_t ‖u(t)‖_{H^{n−1}} < ∞ per ogni n | u ∈ C(ℝ;𝒮) soluzione di KdV (+6uu_x) | PROVA SCRITTA (da auditare) | §6 | s10b_hm 4/4 | richiesto | — | Gagliardo–Nirenberg (standard) |
| S4ID-P8, OPR2-P7 | come OP-F5D | — | CONDIZIONALE solo su [GT-u] (mod audit di S10B-T3) | §7 | — | — | — | OPF5D-P14, P15, S10B-T3, [GT-u] |
| [GT-u] | uniformità in k_0 delle costanti di GT Thm 5.4 | — | APERTO — ridotto a (U) | §7 | — | — | — | GT 0807.5041v2 §5 |
| INT-Q1 | ODE autonoma in x per dati analitici, r ≢ 0 | — | APERTO — ridotto a (R) mod [GT-u] | §8 | — | — | — | OPF5C-T6, S4ID-P8 |
| S10B-L8′ | OPF5C-L8 vale anche per K = 2N | — | PROVA SCRITTA (breve, da auditare) | §9 | — | richiesto | — | OPF5C-L8 |
| S10B-V9 | δ_N(2N) = N+1 ∀k ∈ U_0, N ≤ 5; δ_5(8) = 9 | — | COMPUTER-ASSISTED (mod L8′, L8) | §9 | s10b_delta_K2N_graded, s10b_delta_big_graded, OP-F5C opf5c_delta0_5 | — | — | OPR2-P4, OPF5C-P7(b), L8, L8′ |
| OPF5C-Q1 | congetture δ_N per N generale | — | APERTO — ridotto a limiti inferiori graduati a k = 0 | §9 | — | — | — | — |
| S10B-P10 | criterio a test finiti esiste ⟺ ¬(I) o 𝓛 ha insieme colpitore finito in 𝔇∖𝔇P; (I) necessaria; (II) ⇒ (II′) sufficiente | — | PROVA SCRITTA (elementare) | §10 | — | richiesto | — | OP-ALG-T4, OPR2-L3, OPF5B-T6 |
| OPR2-Q3 | nessun test finito con zoccolo ripetuto | — | APERTO — ridotto a realizzabilità degli atomi + (I) | §10 | — | — | — | S10B-P10 |
| OPR2-Q2′ | chiusura per trasporti sul poligono | — | APERTO — ridotto al lemma (L) | §11 | — | — | — | OPF5B-P8, OPR2-L1 |

---

## rev2 (27/10/2026, dopo l'audit `work/CHECK-F10/AUDIT_S10-OPEN-B.md`) — righe sostitutive e nuove

Le righe qui sotto prevalgono su quelle del primo giro con lo stesso ID. Il testo completo è in PROOF_PACKAGE.md, sezione «Recepimento dell'audit (rev2)», R1–R12. Gli stati sono proposti.

| ID | enunciato breve | stato proposto | fonte |
|---|---|---|---|
| S10B-T1 | [F4⁻]: N-solitone di Hirota ha b ≡ 0, a = Π(k−iκ_j)/(k+iκ_j), spettro {−κ_j²}, per ogni t | DIMOSTRATO (fix T1-a, b, c) | PROOF_PACKAGE R1; s10b_f4.out F1 4/4, s10b_f4_rev2.out 18/18 |
| INT-T1(B) | ramo B, con la convenzione «multi-soliton = soluzione di Hirota» | DIMOSTRATO | R1 (T1-c) |
| S10B-P3 | densità di (SB) in C^r(𝕋) | PROVA SCRITTA (fix P3-a, b) | R3 |
| S10B-L4 | L-loc | PROVA SCRITTA (fix L4-a…e) | R4; V-ex audit_lloc |
| S10B-C1 | controesempio: anello quadrato | DIMOSTRATO; nota «Lettura» corretta (C1-a: foro puntiforme solo m = 0) | R5 |
| S10B-T3 | [Hm] per u ∈ C(ℝ;𝒮) | DIMOSTRATO | §6, R6 |
| S4ID-P8, OPR2-P7 | — | CONDIZIONALE su [GT-u] **e (WP)** (fix R-1) | R6 |
| [GT-u] | uniformità in x/t di GT Thm 5.4 | APERTO (riduzione a (U) ritirata) | R7 |
| INT-Q1 | ODE autonoma in x per dati analitici | APERTO | R8 |
| **S10B-E8** (nuova) | INT-Q1 «no» ⟺ (R), mod S4ID-P8, [GT-u], (WP) | PROVA SCRITTA (equivalenza, non riduzione) | R8 |
| S10B-L8′ | estensione di L8 all'ordine 2N | PROVA SCRITTA (fix L8-a, b) | R9 |
| S10B-V9 | δ_N(2N) = N + 1 | assistita da calcolo: N ≤ 4 riprodotto; N = 5 e δ_5(8) = 9 non riprodotti; **N = 6 NON ESEGUITO** | R9; s10b_delta_big_graded.out |
| OPF5C-Q1 | — | APERTO — ridotto a limiti inferiori graduati a k = 0 | R9 |
| S10B-P10 | caratterizzazione di OPR2-Q3 | DIMOSTRATO | §10, R10 |
| OPR2-Q3 | — | APERTO, caratterizzato da P10 (atomi realizzabili: solo sufficiente) | R10 |
| **S10B-P11** (nuova) | (L-int) ∧ (L-v) ∀v ⇒ K_1 + … + K_N chiusa (poligono convesso, trasporti reali, m = 0) | PROVA SCRITTA, da auditare | R11 |
| OPR2-Q2′ | — | APERTO — ridotto a (L-int) ∧ (L-v) ∀v via S10B-P11 | R11 |
| [Hm] (colonna LEDGER) | — | da «CON-FONTE secondaria KVZ» a «S10B-T3 mod (WP)» | R6 |
