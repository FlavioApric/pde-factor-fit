# REPORT — S5-FIX2 · Fase 5 (recepimento dei fix d'audit) · 26/10/2026
(Salvato dal coordinatore: la scrittura del subagente era bloccata dall'ambiente; testo fedele alla sua risposta finale.)
**Mandato:** applicare nei PROOF_PACKAGE di sessioni chiuse solo i fix già decisi dagli audit, marcati `[fix <id>, S5-FIX2]`; nessuno stato oltre claims/LEDGER.md; nessun fix doppio (grep). Script unico: work/S5-FIX2/l3_check.py → l3_check.out (mpmath, .venv -I).

## (1) work/S4-TERM/PROOF_PACKAGE.md ← AUDIT_S4-TERM (S-CHECK-11)
- **T3-1 (MAJOR):** esito di S4T-T3 diviso: (a) negativo in L∞/H^s per definizione di A9 ((i),(ii)); (b) in L¹ ordine ≤ 1/2 solo per E^mult_AB ((iii)); (c) ordine L¹ di E^add APERTO (S4T-Q1; numerica O(ν), verso positivo). Ritirati "scatta il ramo teorema negativo" e "PR3 ✔ in L∞". Nuovo titolo: "Oltre lo shock: ostruzione nelle norme che vedono i salti (forzata da A9) e ordine √ν dello splitting AB in L¹". Testo originale conservato come storico.
- J-1, L1-1, **F2-1** (Hopf–Cole con prova completa: [F2] DIMOSTRATO), T2-1 (Taylor misto in (s,λ)), T2-2 (regime εT·max(−w₀′) ≤ θ), T3-2, T3-3, Q1-1 (congettura Θ(ν) o Θ(ν|log ν|)), P5-1, C1-1, C1-2. Tabella stati allineata al LEDGER. §12 e §13 non toccati.
## (2) work/S4-ID/PROOF_PACKAGE.md ← AUDIT_S4-ID (S-CHECK-10)
- ID-1 (φ₀ esponenziale-polinomiale), ID-2 (f′ polinomiale di grado < D), ID-3 (coefficienti complessi in P8), ID-4 (testo ristretto: dizionari completi, N = σy_n + N′, deg N = 2; S4ID-Q3 per deg N ≥ 3), ID-5 ("Chiusura, soglia esplicita ed esistenza"). Tabella stati nuova; K1 resta APERTO finché OP-T7 non è nel LEDGER.
## (3) work/S4-INTEG/PROOF_PACKAGE.md ← AUDIT_S4-INTEG (S-CHECK-9)
- P3-1..P3-4, K-1, K-2 (rinvio a work/KIEFFER/LETTURA.md, KIEFFER-C DIMOSTRATO; controesempio con dato liscio APERTO), T1-1, P3a-1, P3a-2, M-1, P4-1, UC-1a, UC-1b, C-1, L-1, L-2, L-3. Tabella stati (§5).
- **Cifra 1.8·10⁻⁵ (L-3):** rifatta con mpmath a 40 cifre: corretta (1.816·10⁻⁵ per ν = 0.05; 2.22·10⁻¹² per ν = 0.02). L'errore era nel δ dichiarato: nella configurazione dello script δ = 1, non 2. Rapporti errore/e^{−δ/2ν}: 0.40, 0.16, 0.79 (ν = 0.1), coerenti con L-3.
## (4) work/OP-ALG/PROOF_PACKAGE.md ← AUDIT_OP-ALG (S-CHECK-12)
- **OA-1 (MAJOR):** inseriti OP-ALG-L1′ e P1′ (riparazione del revisore), T1(iv)/(v) su 𝕂, controesempio u = eˣ(t+πx). OA-2, **OB-1** ("su qualche (Ω, p₀)", nuovo OP-ALG-Q2 APERTO), OB-2, OB-3, OC-1, OI-1. Tabella stati: rinvio al LEDGER.
## (5) work/C1C2/gram.md
- Trasporti paralleli, m ≥ 1: c_F = 1, densità provata (OPF-P5), "PROVA SCRITTA, audit S-CHECK-14 in corso"; §4 aggiornato.
## Segnalazioni al coordinatore
- OP-ANA dichiara in inbox S4T-Q1 "CHIUSO in (H_t): Θ(ν)" (PROVA SCRITTA, non auditata): dopo l'audit aggiornare S4-TERM §1 Esito (c) e §11.
- gram.md §1 r. 3 ("densità provata solo per m = 0") da aggiornare dopo S-CHECK-14.
