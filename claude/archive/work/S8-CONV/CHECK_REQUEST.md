# CHECK_REQUEST — S8-CONV → S-CHECK-F8 · 27/10/2026

Pacchetto: `work/S8-CONV/PROOF_PACKAGE.md`. Controlli numerici e simbolici in `work/S8-CONV/sympy/*.py`, con i relativi `.out`; tutti riportano "TUTTI PASS". Si chiede un audit come proof-checker su ciascun claim qui sotto. Nessun claim è stato promosso a DIMOSTRATO da questa sessione.

## Claim da auditare (in ordine di priorità per il cammino critico)
| priorità | ID | § | stato proposto | dove guardare |
|---|---|---|---|---|
| 1 | CONV-L1, CONV-T1(1–7) | §1.1–1.2 | PROVA SCRITTA | conteggio di T1(5); esempio di T1(6); uso di C3-P1[M2] in T1(7) |
| 1 | CONV-T2 | §1.3 | PROVA SCRITTA | passi 2(iii)–(iv), 3, 4 |
| 1 | CONV-T5(1–3) | §2.3 | PROVA SCRITTA | ramo L² e punto 3 |
| 2 | CONV-T3, CONV-T4(a–c) | §2.1–2.2 | PROVA SCRITTA | ipotesi (α)–(γ); interpolazione con l'estensione di Stein |
| 2 | CONV-T6(1–4), CONV-P6, CONV-P7 | §3 | PROVA SCRITTA | trascendenza del ramo di Lambert; ideale primo I_J |
| 2 | CONV-T8(a–d) (risposta a CONV-Q6) | §6 | PROVA SCRITTA (L^∞: V-ex) | minorante di Strang |
| 3 | CONV-P8, CONV-D1(a–c) | §4.1–4.2 | PROVA SCRITTA | Krull in D1(a) |
| 3 | CONV-B1, B2, B3 | §5 | PROVA SCRITTA | conteggio D + 1 in B2 |
| 3 | CONV-R1(a–c) (RT-R2a) | §7 | PROVA SCRITTA | definizione di "risonante"; isomorfismo modale |
| 3 | CONV-MZ1–MZ3 | §8 | PROVA SCRITTA; criterio RT-S2d **FALSO** | controesempio a21 = 0, a12 = 1 |
| 4 | CONV-T7 (proposizione di composizione) | §9 | PROVA SCRITTA | ipotesi di Lipschitz sugli ingressi calcolati |
| — | CONV-D2 | §4.3 | CON-FONTE (da verificare) | solo verifica di citazione (CIT) |

## Punti delicati: domande mirate
1. **T1(5).** Il conteggio assume K ≥ 1, in modo che m\*(K) ≤ K sia finito. Va controllato che O_K sia davvero una funzione della coppia (m\*, deg O_K). L'argomento è che a m\* fisso i sottospazi N_{m,K} sono annidati, e che a grado uguale il gcd non cambia. Va verificata anche la normalizzazione monica rispetto all'ordine monomiale.
2. **T1(6).** In u = 1 + x^{N+2}e^{x²}, ν₁ = N+1 si ottiene da ord(f′) = N+1. Va verificato che ν₁ = N+1 e che nessuna combinazione a + bτ + cξ con a ≠ 0 dia un ordine più alto. Va controllato anche l'argomento di crescita per escludere che f sia un esponenziale-polinomio.
3. **T1(7).** C3-P1[M2] è citato così: "per ogni K e ogni u con Ann(u) = (P), esiste u′ analitica con lo stesso jet di ordine K e Ann(u′) ≠ (P)". Va controllato che sia esattamente l'enunciato nel LEDGER, compresa la quantificazione su Ω.
4. **T2, passo 2(iv).** Il minore Δ dipende solo dalle coordinate j_γ con L < |γ| ≤ K₀, e i box hanno raggio γ!/|γ|!. Va controllato che i coefficienti c_γ = j_γ/γ! restino ≤ 1/|γ|!, e quindi che u sia intera. Va controllato anche che i passi successivi non tocchino gli ordini già fissati.
5. **T2, corollario ritirato.** Si chiede conferma che il corollario sulla classe {Ann principale} ∪ {0} non segue dalla prova, perché al passo 0 il controesempio è un polinomio. La domanda resta aperta come CONV-Q10.
6. **T4(b) e T5, ramo L².** L'interpolazione è ‖e‖_{H^m} ≤ C‖e‖_{L²}^{s/(m+s)}‖e‖_{H^{m+s}}^{m/(m+s)}, su un dominio lipschitziano limitato, con l'estensione universale di Stein. Il numero del teorema è da verificare. Va controllato che l'esponente valga per m, s interi con questa costante.
7. **T5(3).** La perturbazione è p = t^d x_1^d ⋯ x_{n−1}^d, con Ann(p) ∩ R_{≤d} = 0 (argomento con la parte omogenea di grado minimo) e Q₀τ^{d+1} ∈ Ann(u + εp). Va controllato che d(u′) > d, così che δ₀(u′) sia ≤ ½ s_d(u′).
8. **T6(2).** I_J non è massimale perché iκ non è costante. Va controllato il passaggio "primo non nullo e non massimale in ℂ[τ, ξ] ⇒ principale".
9. **P6(b).** Il passaggio è: e^{σa} algebrica su ℂ(κ) ⇒ algebrica su ℂ(a) (perché a è trascendente su ℂ, non costante, e il grado di trascendenza è 1) ⇒ H(y, e^{σy}) ≡ 0 ⇒ contraddizione con C3-L3(b). Va controllata la catena.
10. **T8(c), minorante.** Va verificato il conteggio degli interi pari nella finestra κ(m² − 1)h ∈ [1, 4], cioè ≥ 1/(4√(κh)) per κh ≤ 1/36. Va verificata la stima e^{λ_1T} − e^{λ_mT} ≥ ½e^{λ_1T}, e la monotonia di |φ_S| tramite la funzione di Langevin.
11. **T8, significato.** G_h è il coefficiente di ε nell'errore, con il passo di trasporto troncato al primo ordine (I + εhV). Va controllato che questa sia la lettura giusta del confronto con P3-T3, dove il passo di trasporto è di inflow.
12. **R1.** Un k si dice risonante se f_k ≢ 0, g_k ≢ 0 e gcd ≠ 1. Il caso f = ξ, g = τ mostra che serve la clausola sulle rette contenute. Va controllato che la suriettività u ↦ (û_k)_{k risonante} e il nucleo diano l'isomorfismo dichiarato.
13. **MZ3.** Va confermato che il criterio della strada RT-S2d, letto come "memoria nulla ⟺ [𝒫, A] = 0", è FALSO, e che la forma corretta è a12·a21 = 0.
14. **D1(a).** Va controllato l'argomento che V(Q_1, Q_2) non vuoto implica infinito per n ≥ 3, via il teorema dell'ideale principale di Krull applicato due volte e la dimensione delle componenti ≥ n − 2.

## Citazioni da far verificare a CIT
- Stein 1970, cap. VI §3: estensione universale; numero del teorema.
- Engl–Hanke–Neubauer 1996, cap. 4–5: principio di discrepanza.
- Kelly 1996: "decidibile nel limite ⟺ Δ⁰₂".
- Hörmander ALPDO I, Thm 2.3.4 (distribuzioni supportate in un punto) e ICASV §7.6.
- Malgrange, Sém. Bourbaki exp. 246, e Palamodov 1970 (CONV-D2).
- Casas 2007: costante π.
- Dang–Einkemmer–Ostermann 2025, arXiv:2504.10125: norma degli ordini 1 e 1,5.
- Nečas 1967 e Grisvard 1985: traccia su domini lipschitziani.
- Engel–Nagel III.1: Dyson–Phillips.

## Kill-argument
Su CONV-T1 e CONV-T2 c'è un attacco interno, con la difesa punto per punto, in PROOF_PACKAGE §K. L'esito proposto è PASS-WITH-NOTES. Si chiede un revisore indipendente (DEVIL-8).
