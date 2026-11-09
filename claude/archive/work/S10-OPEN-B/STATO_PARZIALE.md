# S10-OPEN-B · stato parziale (sessione interrotta per limite d'uso, 2026-10-27)

Nessuno stato DIMOSTRATO è rivendicato. Le prove sono progettate ma non ancora scritte per esteso in PROOF_PACKAGE.md (da fare). Esiti proposti:

| problema | esito proposto | nota |
|---|---|---|
| INT-T1(B) / [F4⁻] | (a) prova progettata | Wronskiano dei semi φ_j = e^{−κ_j x} + ε_j c_j e^{κ_j x}, minori di Cauchy, intertwining senza citare Crum ⇒ b ≡ 0. SymPy `s10b_f4.py` in esecuzione, uscita non ancora prodotta |
| OPF5C-T5 | (a) prova progettata | J = [A]:H_A^∞ con A di rango minimo, pseudo-divisione di Ritt |
| OPA-Q2 (densità Morse+(SB)) | (a) prova progettata | perturbazioni εψ, εΘ′ sequenziali |
| OPA-Q1 / L-loc | (a) prova progettata | localizzazione di T1, T2, L2, Lemma U |
| densità OPF5B-T1 su non convessi | (b) controesempio verificato | corona quadrata, P = ∂x∂y; `sympy/s10b_annulus.out` 3/3 OK |
| [Hm] | (a) prova progettata | leggi di Gardner (u = w + εw_x − ε²w²) + Gagliardo–Nirenberg; `sympy/s10b_hm.out` 4/4 OK. Esistenza globale in 𝒮 resta ipotesi |
| [GT-u] (S4ID-P8 / OPR2-P7) | (c) APERTO — ridotto a uniformità in k_0 della costante di Hölder in GT 0807.5041 (5.20)–(5.21) |
| INT-Q1 | (c) APERTO — ridotto a T6 + S4ID-P8 (mod [GT-u]) e relazioni con forma iniziale in I_PW singolari nell'origine |
| OPF5C-Q1 (δ_N) | parziale + (c) | δ_N(2N) = N+1 ∀k per N ≤ 4 (`sympy/s10b_delta_K2N_graded.out`, computer-assisted, con L8 esteso a K = 2N e OPR2-P4); δ_5(8) = 9 (uscita OP-F5C + P7(b)). Caso generale ridotto a limiti inferiori graduati a k = 0. Run N = 5, 6 in corso (`s10b_delta_big_graded.out`) |
| OPR2-Q3 | (c) caratterizzazione esatta | criterio finito ⟺ ¬(I) oppure famiglia {L_u} con insieme di intersezione finito in 𝔇∖𝔇P |
| OPR2-Q2′ | (c) APERTO — ridotto al lemma di localizzazione (L) |

Da fare: PROOF_PACKAGE.md, CHECK_REQUEST.md, LEDGER_ROWS.md, open_questions.md, riga DONE in inbox.

**Superato** da PROOF_PACKAGE.md (consegna completa, 27/10/2026).
