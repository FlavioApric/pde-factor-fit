# CHECK_REQUEST — OP-F5D (per S-CHECK, revisore indipendente senza contesto; claim-lifecycle passo 3–4)
Pacchetto: `work/OP-F5D/PROOF_PACKAGE.md`. Script: `work/OP-F5D/sympy/` (lax_all 34/34, zc_all 32/32, burgers_l1 11/11, solitons.py: TIMEOUT 15 min x2, nessun output — controlli V-ex su Crum/Novikov N=2,3 NON eseguiti; L6/T3 restano solo con prova scritta).
Dare al revisore solo enunciato, ipotesi e prova di ciascun punto.

## Priorità (cammino critico; kill-argument consigliato)
1. **OPF5D-T3 + L6** (KdV: senza riflessione ⇒ operatore d'intreccio via Liouville ⇒ Novikov). Punti da attaccare: (a) continuità di Ψ in k = 0 dai due lati (L3(ii) C¹ in k, L5(i) caso w(0) = 0 con |w′(0)| ≥ 2); (b) cancellazione dei poli in −iκ_j (semplicità, L4); (c) crescita polinomiale nel semipiano inferiore tramite |𝔅T| ≤ 1; (d) segno/normalizzazione di P = A∂A^T (coefficiente direttore 1) e uso della trasposta senza coniugio; (e) passaggio "parte reale" per ottenere d* ∈ ℝ^{N+1}.
2. **OPF5D-T4** (NLS con molteplicità): calcolo dei poli di mσ_3m^{−1} (coefficiente 2λw⊗w^⊥ ≠ 0), identificazione β_n ↔ d̃_n, lemma L12 nel caso M = 0.
3. **OPF5D-T6** (Burgers, O(√ν) da Cole–Hopf): forte convessità di G_0 (passo 3), Fubini/periodicità (passo 4), Jensen, lemma delle derivate di convesse (passo 5), costante finale.
4. **OPF5D-T1 / T2** (Lax e curvatura nulla ∀n): telescopio (T1 passo 5), identificazione con la gerarchia del progetto (T1(b)), induzione A_m′ = qC_m − rB_m (T2(a)).

## Altri punti
- OPF5D-R1 (segno a n = 0 in OP-P18): verificare contro work/OP-NL/sympy/lax_checks.out (V_0 = diag(i,0)).
- OPF5D-L9: regolarità in t delle soluzioni di Jost nella classe (Cl).
- OPF5D-P14/P15: correttezza della lettura di GT (Thm 4.4, Cor 4.5, Thm 5.4, letti sul PDF arXiv:0807.5041v2) e dell'interpolazione L13 (scelta α = 3/4, m > 3j); il fatto [GT-u] (uniformità in x) va confermato sul testo.
- OPF5D-T7: passaggio al limite nelle disuguaglianze entropiche; che [K-U] sia l'unico fatto residuo.
- OPF5D-R2: dipende da [DP]; verificare che T4 implichi davvero la falsità della forma senza molteplicità.

## Domande per CIT-AUDIT
- [GT-u]: GT dichiarano l'uniformità dell'errore in x nelle regioni? (Thm A.6, §6.)
- [Hm]: fonte primaria per sup_t‖u‖_{H^m} < ∞ (KVZ rinviano a [26, §3]).
- [K-U]: numero ed enunciato del teorema di unicità in Kružkov 1970.
- [DP]: soluzione a doppio polo di NLS (Zakharov–Shabat 1972; Olmedilla 1987) in 𝒮.
- [F4⁻]: Kay–Moses / formula di Wronskiano per N-solitoni (N qualsiasi).
