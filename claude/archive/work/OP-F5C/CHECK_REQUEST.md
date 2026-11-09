# CHECK_REQUEST — OP-F5C (per S-CHECK, revisore indipendente)
Pacchetto: `work/OP-F5C/PROOF_PACKAGE.md`. Script: `work/OP-F5C/sympy/`. Fonti: `work/OP-F5C/sources.bib`.

## Priorità (cammino critico)
1. **OPF5C-T2 (OP-K15)** e le sue dipendenze L1, L2, L3, T1, L4, L5. Punti delicati:
   - T1(a): applicazione del criterio di Hironaka/Bezout pesato a R = ℂ[k, y] con p = (k, y_0..y_{N−1}); conto del rango 2^N.
   - T1(b): stratificazione di M_k per molteplicità delle radici di U (casi μ generico, μ = 0, μ = −κ_i con m ≥ 2); irriducibilità dello strato principale via σ; riduzione (CM + R_0).
   - L4 (★): il conto deg V² ≤ N−2, deg E²(λ+c) ≤ N−2 con a′ = ⌈(N+1)/2⌉, b′ = ⌊(N+1)/2⌋, e l'identità e_{N+2} + e_{N+1}/2 = −t_{N+1}/(N+2).
   - L5: sezioni locali σ_ε dai solitoni con numeri d'onda ±k_i; uso di (Nov′) per k^ε; distinzione delle forme lineari ℓ_ε.
   - T2: coefficiente di y_0^{W/2} indipendente da k e uguale a ±Π y_N sulla fibra speciale a k = 0.
   - (Nov′): equivalenza con (Nov) di OPR2-P4 (argomento x → +∞) e estensione ai k complessi.
2. **OPF5C-T6** (INT-Q1 parziale) e **L9** (decadimento super-polinomiale ⇒ varietà fortemente stabile; unicità del punto fisso nello spazio a pesi polinomiali). Controllare: (c) il passaggio "W^{ss}_loc∖{0} = due archi d'orbita" per s = 1; chiusura di T_± in L²; regolarità di c(t).
3. OPF5C-P7 (costruzioni r_{N−1}, D; pesi 2N+4, 2N+9; non nullità di D), OPF5C-L8 (forme iniziali), tabella P9 (direzione "rango pieno mod p ⇒ nessuna relazione su ℚ").
4. OPF5C-T5 (Ritt), O6, O7 (enunciati sul metodo).

## Kill-argument richiesto
Sì per OPF5C-T2 (chiude una congettura registrata) e OPF5C-T6 (cammino critico di INT-Q1).

## Controlli suggeriti
- Rieseguire `opf5c_checks.py`, `opf5c_nov2.py`, `opf5c_k15.py 6`, e `opf5c_delta.py 3 4 8 graded`.
- Controesempio da cercare per T6: una soluzione di Schwartz analitica con relazione a origine non singolare d'ordine ≤ 3 che non sia un solitone (non dovrebbe esistere).
- Verifica fonti (CIT-AUDIT): numeri di teorema in Bruns–Herzog, Ritt, Chicone, Kreuzer–Robbiano, Gesztesy–Holden (marcati NON VERIFICATI in sources.bib).
