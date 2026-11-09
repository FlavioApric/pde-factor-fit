# KA OPF5C-T2 — aggiudicazione (S-CHECK-19, 26/10/2026)

Input: `KA_OPF5C_T2_input.md` (solo enunciato, ipotesi, prova). Attacco: `KA_OPF5C_T2_attack.md` (subagente indipendente, 12 attacchi, script `sympy/s19ka_*.py`).

## Esito dell'attacco
**SOPRAVVIVE CON FIX (solo MINOR).** Nessun difetto FATALE o MAJOR. Attacchi sopravvissuti: (Nov′) (convenzioni di segno/normalizzazione, identità telescopica; resti r_m = 0 esatti su getti di N-solitoni per N = 2 (k = (1,3), (2,−5)), N = 3 (k = (1,2,−4), (2,5,7)), N = 4 (k = (1,2,3,−5))); L1, L2/T1(a) (conto del rango 2^N), L3 (parità); T1(b) (strati, irriducibilità di S°, CM + R_0) anche per k speciali N = 2: (1,i), (2,2i), (1,1+i), (3,1/3): Π_2 irriducibile, discriminante in y_2 non nullo; T1(c); L4 (rifatto a mano; Gröbner GB = {1} per N = 1..6); L5 (multinsiemi {ε_ik_i} distinti su U_0); passo di teoria dei campi χ_k = m^{[L:K(y_N)]} e nucleo = (m); argomento dei pesi e coefficiente di y_0^{W/2} (sulla fibra di Z_0 sopra (1,0..0): y_N² = −2, 5, −14 per N = 1,2,3 ⇒ coefficienti 2, 25, 14⁴; per N = 2 l'eliminante ha grado totale 8, monico in y_2 di grado 4, coefficiente di y_0^8 = 25 per ogni k testato).
Non chiuso dall'attaccante: eliminazione diretta N = 3 (timeout 600 s) — coperta dal V-ex già registrato (OP-NL §3.4, mod p: grado 20).

## Aggiudicazione dei punti sollevati
1. "Π_N(k) = ±χ_k": Π_N(k) è un generatore, definito a meno di scalare. **Accolto, MINOR** (F5C-1): normalizzare Π_N(k) := generatore monico in y_N; allora Π_N(k) = χ_k.
2. "omogeneo pesato in (k, y)" si riferisce al χ universale in ℂ[k, y_0..y_N], non a Π_N(k) a k fissato. **Accolto, MINOR** (F5C-1).
3. Dipendenza da (Nov′). **Accolto e risolto dal revisore**: (Nov′) segue da (Nov) (OPR2-P4, CON-FONTE secondaria verificata in CIT-AUDIT-F5) più l'argomento x → +∞ del pacchetto; il punto non letto in fonte ("le costanti sono e_j(κ)") si dimostra in 3 righe (linearizzazione in X = 0, vedi AUDIT F5C-2). Con l'aggiunta, T2 dipende solo da fonti verificate.

## Mio controllo indipendente (linea per linea, AUDIT_OP-F5C.md §T2)
Confermati: L3 (gradi 2N−2a−1 ≤ N−1, 2N−2b−2 ≤ N−1), L4 (a′+b′ = N+1 ⇒ deg V², deg E²(λ+c) ≤ N−2 in entrambe le parità; e_{N+2}+e_{N+1}/2 = −2(t_{N+2}+t_{N+1}) = −t_{N+1}/(N+2)), L5 (ℓ_ε distinti ⇒ fibra ridotta), T1 (rango Π 2(2N+1−m)/Π(j+2) = 2^N). Controllo indipendente aggiuntivo: `sympy/s19_delta.py gen 2 2 1,3 8` — getti di 2-solitoni calcolati direttamente da f (nessun uso di Mumford/GD/(Nov′)), k = (1,3): nessuna relazione di grado ≤ 7 (rango pieno mod p), nullità 1 a grado 8: deg Π_2 = 8 confermato.

## Verdetto
**OPF5C-T2 SOPRAVVIVE** al kill-argument. Stato proposto: **DIMOSTRATO mod fonte verificata** ((Nov) Novikov 1974 via CIT-AUDIT-F5; criterio di Hironaka Blum-Smith Cor. 2.4.19), condizionato all'inserimento dei fix MINOR F5C-1, F5C-2.
