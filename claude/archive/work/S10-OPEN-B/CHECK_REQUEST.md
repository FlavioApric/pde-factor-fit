# CHECK_REQUEST — S10-OPEN-B

Richiesta di audit (proof-checker + kill-argument dove indicato). Nessuno stato è DIMOSTRATO finché l'audit non chiude.

1. **S10B-T1 ([F4⁻], §1).** Verificare:
   - la regola dei segni (conteggio Σ_{j∈S}(j−1)) e la formula del modulo di ρ;
   - la divisione a destra e il confronto dei coefficienti (q_1 = 0, q_0 = −2(log W)″);
   - l'identificazione di b con il coefficiente di e^{−ikx} nella convenzione OPF5D-L3 (eventuale normalizzazione 1/T);
   - l'uso di L4 per lo spettro.

   Kill-argument: cercare N, κ, c per cui W si annulla (escluso da f > 0).
2. **S10B-T2 (§2).** Prova classica. Verificare che OPF5C-T5 sia enunciato in una indeterminata, e la D_F-stabilità di J_u.
3. **S10B-P3 (§3).** Verificare:
   - Passo 3 (apertura delle condizioni SB_j) e l'invarianza dei tempi candidati sotto le perturbazioni θ_i, ψ_i;
   - che la densità sia richiesta in C^3 (o C^5 per C1): le perturbazioni sono C^∞.
4. **S10B-L4 (= L-loc, §4).** Punto principale. Verificare:
   - 4.1, margine dalla semicontinuità;
   - 4.2, convessità solo nella finestra per t ≤ t_b;
   - 4.4, Lemma U e L3′ con il margine η_0 al posto della convessità globale; ordine delle costanti.

   Kill-argument su 4.4: una seconda nascita con minimizzante non degenere vicino ma esterno alla finestra.
5. **S10B-C1 (§5).** Controesempio. Verificare la connessione delle strisce e la continuità L² di Λ. V-ex `sympy/s10b_annulus.out` 3/3.
6. **S10B-T3 ([Hm], §6).** Verificare:
   - il segno della trasformazione di Gardner per +6uu_x;
   - il Passo 4 (terminazione e j_1 ≤ n−2);
   - gli esponenti di GN e γ < 2.

   Confermare che [Hm] in OPF5D-P14/P15 sia esattamente "sup_t ‖u‖_{H^m} < ∞". SymPy `sympy/s10b_hm.out` 4/4.
7. **§7, §8, §10, §11 (esiti (c)).** Controllare che le riduzioni siano corrette e che nessuna affermi più di quanto provato. §10, S10B-P10: controllo logico.
8. **§9.** Verificare:
   - L8′ (OPF5C-L8 non usa K ≤ 2N−1 altrove);
   - la riproducibilità di `s10b_delta.py N 2N dmax graded` per N ≤ 5 (N = 5: ~55 min).

   Lo script è una copia invariata di `OP-F5C/sympy/opf5c_delta.py` più `opf5c_gd.pkl`.

**Stato delle verifiche numeriche alla consegna.**
- `s10b_hm.out`: 4/4 OK.
- `s10b_annulus.out`: 3/3 OK.
- `s10b_delta_K2N_graded.out`: N ≤ 4 completo.
- `s10b_delta_big_graded.out`: N = 5 completo; (6,12) e (6,11) ancora in esecuzione, nessun valore riportato.
- `s10b_f4.out`: il primo run (F1 fino a N = 5, F4 simbolica) è andato in timeout senza uscita. Il run ridotto (F1 N ≤ 4, F2/F3 N ≤ 6, F4 numerica) dà 21/22 OK.
  - L'unico FAIL è F5 per N = 3 (residuo 2.3e-14). È un **artefatto di `lambdify`**: in `s10b_f4_f5check.out` il residuo relativo vale 2.08e-15 a 40, 80 e 120 cifre, cioè non dipende dalla precisione, quindi entra un valore a doppia precisione.
  - Con sostituzione esatta (x, k razionali) ed `evalf` a 60 cifre il residuo relativo è 8.5e-198.
  - F5 N = 3 è quindi da considerare OK. L'audit lo verifichi.

---

## rev2 (27/10/2026) — richieste di audit per il secondo giro

I fix redazionali del primo audit sono applicati in PROOF_PACKAGE.md, sezione «Recepimento dell'audit (rev2)». Le richieste nuove sono:

1. **S10B-P11 (R11).** Verificare:
   - la decomposizione ‖Sf‖² = Σ_α‖Σ_jχ_αf_j‖²;
   - che 𝒦_0, definito da (𝒦_0f)_i = −Σ_{j≠i}P_iχ_0²P_jf_j, sia compatto e autoaggiunto sotto (L-int);
   - il passaggio «𝒢 + 𝒦 coercivo ⇒ 𝒢 Fredholm ⇒ ran S chiuso».

   Verificare anche che (L-int) e (L-v) siano enunciati abbastanza precisi da costituire una riduzione legittima di OPR2-Q2′. Non è richiesto di provare (L).
2. **S10B-E8 (R8).** Verificare che l'equivalenza INT-Q1 «no» ⟺ (R) segua da S4ID-P8 (parte lineare nulla e forma iniziale in I_PW) e che il ramo T6 sia stato tolto correttamente.
3. **R5 (C1-a).** Verificare l'argomento δ_p ∉ H^{−1} per il foro puntiforme con m ≥ 1, e l'esempio H(x − p_1)H(y − p_2) per m = 0.
4. **R9 (L8-b).** Verificare la prova di P_k^{(2N)} = I_k + (y_{2N} − Φ(k;·)) via l'isomorfismo del grafico.
5. **Verifiche rigenerate.**
   - Eseguire `D:\ProblemaBase\.venv\Scripts\python.exe -I sympy\s10b_f4.py noF1`; atteso `sympy/s10b_f4_rev2.out`, 18/18 OK.
   - F1 (N ≤ 4) è in `sympy/s10b_f4.out`, 4/4.

   Il run δ_N per N = 6 è NON ESEGUITO: è stato fermato dopo circa 3 h 28 min senza uscita.
