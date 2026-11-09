# CHECK_REQUEST — S4-ID (per S-CHECK, proof-checker) · 26/10/2026
Testo da auditare: `work/S4-ID/PROOF_PACKAGE.md` (versione con fix KA-1…KA-9 e KA-R1…R7). Le prove sono **complete in quel file**; qui sotto: quadro minimo, fatti importati (con enunciato), elenco dei claim con ipotesi e collocazione, punti delicati. Non serve altro contesto.

## Quadro minimo
- ℂ{y} = ℂ[θy : θ = ∂_t^a∂_x^b], coefficienti costanti, derivazioni ∂_t, ∂_x. A = ℂ[y_0, y_1, …], y_j = ∂_x^jy. V_{d,k} = span dei monomi di grado ≤ d nei θy con |θ| = a+b ≤ k; A_{≤d,≤k} = polinomi in y_0..y_k di grado ≤ d.
- F = y_t − N, N ∈ A d'ordine n ≥ 1. D (y_j ↦ y_{j+1}), D_N (y_j ↦ D^jN) derivazioni di A. ψ: ℂ{y} → A, ∂_t^a∂_x^by ↦ D_N^aD^by_0.
- u ∈ C^∞(Ω), Ω ⊂ ℝ² aperto; I(u) = {G : G(u) ≡ 0 su Ω}; J_u = I(u) ∩ A.

## Fatti importati (NON da auditare qui; stato del loro autore)
- **[ALG-L1]** (work/S4-INTEG/PROOF_PACKAGE.md §3.1, DIMOSTRATO-pronto, in audit presso S-CHECK da S4-INTEG): ψ è un omomorfismo suriettivo di anelli differenziali (∂_x ↦ D, ∂_t ↦ D_N), ψ|_A = id, ker ψ = [F], e G − ψ(G) ∈ [F] per ogni G.
- **[ALG-T1(b)]** (stesso file §3.2): I(u) = [F] ⟺ J_u = 0.
- **[MODREL-T1]** (stesso file §3.6), **[INT-T1(B)]** (§1.1).
- **[C3-L3(b)]** (LEDGER, DIMOSTRATO): Σq_ke^{⟨z_k,·⟩} = 0 su un aperto non vuoto con z_k distinti ⇒ tutti i q_k = 0.
- CON-FONTE dichiarate (non da auditare, da verificare in CIT-AUDIT): Hölder (Γ differenzialmente trascendente); buona posizione C^∞ di KdV con dati H^∞ (Bona–Smith, Kato); Umemura–Watanabe (solo per T4(iv)); asintotica di Deift–Zhou/Grunert–Teschl (solo per P8).

## Claim da auditare (priorità: cammino critico di G★′-NL punto 2)
| priorità | ID | enunciato (sintesi) | ipotesi | dove |
|---|---|---|---|---|
| 1 | S4ID-T1 | 0 → [F]∩V → I(u)∩V →ψ J_u∩ψ(V) → 0 esatta; identificazione mod [F] ⟺ J_u∩ψ(V) = 0; I(u)∩V = ℂF ⟺ [F]∩V = ℂF e J_u∩ψ(V) = 0; Gram | u ∈ C^∞, V qualsiasi | §2 |
| 1 | S4ID-P1 (con L2) | per N = σy_n + N′ (σ ≠ 0, N′ d'ordine < n, deg N = 2): [F]∩V_{d,k} = ℂF ⟺ (d,k) = (2,n) (tra i dizionari che contengono F) | Burgers, Fisher, KdV, KdV–Burgers | §3 |
| 1 | S4ID-T2(a)–(d) | N-shock non risonanti: J_u ∩ ℂ[y_0..y_{N−1}] = 0; J_u ∩ ℂ[y_0..y_N] = (R_N), R_N esplicito (Bell) di grado N+1; ideale (R_N, DR_N, …) a ordine K ≥ N; criterio nel dizionario evolutivo | ν ≠ 0, k_i ≠ 0 distinti, (NR) | §4 |
| 1 | S4ID-T2(e) grado 1 | nessuna relazione di grado ≤ 1 | | §4 |
| 2 | S4ID-L5 | lemma di scala in ampiezza | | §4 |
| 2 | S4ID-T3(a)(b) | N-solitoni KdV: nessuna relazione d'ordine ≤ N−1; a ordine N ideale principale (Π_N); Π_1 = y_1² − k²y_0² + 2y_0³ | k_i > 0 distinti, (NR) | §4 |
| 2 | S4ID-L4, S4ID-P5 | [F_B] ∩ (Ry ⊕ Ry²) = R·F_B; Syz_f(u) ≅ I(u) ∩ H | | §4 |
| 2 | S4ID-C1, C2 | dizionari evolutivi (C1(i) è CON-FONTE: Scholl et al.); inclusioni di ψ(V_{d,k}) | | §2–3 |
| 3 | S4ID-P7 | MON-1 corretto (condizione locale dh∧du ≢ 0 sufficiente; non identificazione richiede H globale) | u ∈ C⁴ | §4 |
| 3 | S4ID-T4(i)(ii)(iii-Burgers) | torre ⇒ trdeg finito ⇒ relazione; soglia D* = (n+1)c^n − n per M1; esistenza di soluzioni identificanti (Burgers via Cole–Hopf, mod Hölder) | | §5 |
| — | S4ID-P8 | condizionale a (H-as): NON chiedo DIMOSTRATO, solo controllo della logica | | §6 |

## Punti delicati (dove guardare)
1. T1(a): uso di G − ψ(G) ∈ [F] ⊆ I(u) per u solo C^∞ (nessuna analiticità).
2. P1(c) Passo 1: l'indice dominante λ = na + b è iniettivo su Θ_+ e ≥ n+1; l'indipendenza di {1, y_0..y_n, N, ψ(θy)}; il Passo 2 per gradi (serve N_2 ≠ 0).
3. T2(I): riduzione al formale tramite (NR) e C3-L3(b); T2(a): Vandermonde + triangolarità di Bell; T2(b): divisione per un polinomio di grado 1 in y_N a coefficiente costante.
4. T3(b): "primo di altezza 1 in un UFD ⇒ principale" e il calcolo dell'altezza (trdeg dell'immagine = N).
5. L4: D_B^m(y_0²) = (−1)^m(2/(m+2))D^m(y_0^{m+2}) e q(D)(y_0^E) ≠ 0 (grading per peso).
6. T4(ii): stima deg P_j ≤ a + jb e il conteggio binomiale.
7. T4(iii): passaggio t → 0⁺ (regolarità fino a t = 0 di Cole–Hopf con g ∈ C_c^∞).
Già esaminati da un revisore avversariale fresco (kill-argument, §8) senza trovare errori: L2, P1(c), L5, T2(a)–(c), T3(a)–(b), L4, P5(i), T4(ii). Esito kill-argument: WARN (portata, non validità).

## Verifiche SymPy (controllo, non prova)
`sympy/s4id_checks.out` 61/61 OK; `sympy/s4id_checks2.out` 5/5 OK (controllo indipendente di T1(b) con derivate in t dirette).

## Richiesta
Audit proof-checker dei claim di priorità 1–2 (poi 3 se c'è capacità), con esito PASS / PASS-con-fix / FAIL per claim, in work/CHECK/AUDIT_S4-ID.md.
