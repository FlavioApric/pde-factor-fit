# Domande aperte — S9-ALG (Fase 9) · 27/10/2026

Le domande sono emerse mentre si componeva `ALGORITMO_ESTESO.md`. Nessuna è un claim nuovo. Ciascuna indica il punto della pipeline in cui il contratto scende a (C) o (Lim), oppure in cui manca un esempio.

1. **Robustezza in DM-δ** (VAR-Q19, ATTACK-8 O8). VAR-P3 dà un modulo di continuità (Hölder 1/3 nitido) e CONV-T4 una stabilità con margine ρ. Nessuno dei due è un certificato: la soglia δ₀ di CONV-T5 non è minorabile dai dati.
   - Domanda: esiste una classe a priori (limite M, |u| ≥ δ su K, margine ρ noto) in cui un dato rumoroso certifica ID-res o ID-ann?
   - Passi coinvolti: 1, 4, 7.
2. **Ambiguità DM2.** NOTAZIONE v5 chiama DM2 il getto in un punto; GATE8 §5, ATTACK-8 O8 e VAR-Q19 lo usano per i dati rumorosi. La specifica introduce DM-δ per il secondo senso. È una decisione notazionale del coordinatore (NOTAZIONE).
3. **L9 con identificazione.** L'esempio §9.4 mostra solo l'indistinguibilità (CONV-T6).
   - Manca un dato non EP che identifichi un moltiplicatore non locale in una classe finita (ID-ker sotto (H-ex)).
   - Non è provato che DICT-A(iii) (fit non certificabile) valga per atomi non locali (DICT Q4).
4. **DICT-ILIM-Hs**, CANDIDATO: corollario Hölder per s ≥ 1, via Gagliardo–Nirenberg.
5. **CONV-Q1**: ricostruire G_u nel limite senza un maggiorante B.
6. **VAR-T1(c)-Q10**, APERTO: caso L^∞ con |Z(u)| > 0 e int Z(u) = ∅.
7. **C3-Q2 in generale**: VAR-C3Q2 lo chiude solo per L monico in ∂_t in A_2.
8. **CONV-Q9**: V illimitato (oscillatore e Stark su ℝ fuori dalle classi di VAR-T10), con il contratto per Dyson e Magnus.
9. **Costo**. C3-A1 è PROVA SCRITTA non auditata e non ha una riga nel LEDGER. Il costo di R1 per livello (quadrature della Gram, condizionamento al crescere di n) non ha una stima dimostrata. Serve un audit di C3-A1 e una stima del costo di MF2/MF3 per livello.
10. **R6 in H^{2k} e con MF3**: DICT-R6 trasporta i certificati in L² con C_W². Restano da verificare il trasporto in H^{2k} e quello per il test in forma debole (MF3).
11. **Altri aperti citati**:
    - ENC-T2(c′) nella classe principale;
    - VAR-P12(d) (Floquet);
    - II-T2(b′) e Maxwell (Q6);
    - VAR-L2-cor → DIMOSTRATO, che richiede la prova autonoma di VAR-P11(e) (fix VAR-L2c-1) e un riscontro di terzi;
    - ~~DICT-R6(f) → DIMOSTRATO, dopo il recepimento di R6f-1 e R6f-2~~: chiusa, R6f-1 e R6f-2 sono recepiti nel PP §3.6 e il LEDGER dà (a)–(f) DIMOSTRATO.

## Aggiunte dopo ATTACK-9 (27/10/2026)

12. **Inclusione rigorosa per il misfit (A)** (O10). Serve un r_n con un bound d'errore di quadratura, o in aritmetica intervallare, perché il misfit sia di classe (A) e non (B).
13. **Costante di Lipschitz esplicita di q ↦ W_q** (ENC-1, C(a, Q, Q′)) (O12). Senza di essa, l'encoder con q stimato dal passo 3c resta (C).
14. **Bound di ‖W_q‖ più stretto di C_W = 1 + a²Q e^{a√Q}** (O32). Per esempio cosh(a√Q), oppure Gronwall esatto: oggi la perdita è di circa quattro ordini di grandezza a a√Q = 5.
15. **Riga LEDGER per Trotter–Kato e chiusura delle citazioni** elencate nel §10 di ALGORITMO_ESTESO (O6, O8). Il testo pieno di Oberst 1993 serve per la novità di SYS-EX (O14).
