# open_questions — S8-CONV · 27/10/2026

## Domande ancora aperte da F6-CONV
- **CONV-Q1.** Senza maggiorante, è identificabile nel limite G_u = gcd Ann(u) quando Ann(u) non è principale? L\* converge a g_d, che può essere un multiplo proprio di G_u (§1.2, nota).
- **CONV-Q2.** Esiste una soglia di jet esplicita K\* per classi più larghe di EP, per esempio funzioni di ordine di crescita finito? T1(6) mostra che una soglia funzione del solo d non esiste.
- **CONV-Q3.** Qual è una versione quantitativa di T2 in termini di complessità dei cambi di mente, cioè il numero di errori in funzione della crescita di u?
- **CONV-Q4.** Si può caratterizzare la classe N_𝒦 quando 𝒦 è la classe dei sistemi aumentati con un numero finito di variabili ausiliarie?
- **CONV-Q5.** Esistenza della scomposizione ker(Q_1Q_2) = ker Q_1 + ker Q_2 su domini non convessi in 1+d (P-convessità, fenomeno di Hartogs–Ehrenpreis). Strada parcheggiata.
- **CONV-Q7.** Stabilità di T4 e T5 con rumore non deterministico (stocastico), con tassi in probabilità.
- **CONV-Q8.** Margine ρ_d esplicito per famiglie concrete (calore, onde) come funzione di Ω.
- **CONV-Q9.** Risolta da S8-VAR (inbox/S8-CONV, VAR-T10, prova scritta non auditata). Le etichette A/B/C per V(t, x) sono recepite in PROOF_PACKAGE §9. Resta aperta solo la parte "V illimitato non quadratico": (C) per la serie, e integratori troncati con perdita di regolarità.
- **CONV-Q6.** Risolta al primo ordine in ε da CONV-T8 (§6). La parte residua è in CONV-Q6′ e in CONV-Q12.

## Domande nuove
- **CONV-Q10.** Chiusa in positivo: è CONV-T2′ (PROOF_PACKAGE §1.3′), riparazione proposta dall'audit F8 (fix CONV-8). Stato: PROVA SCRITTA, da auditare.
- **CONV-Q11.** Mori–Zwanzig a coefficienti variabili: "legge chiusa locale ⟺ eliminazione finita" (F6-HOR) vale nella direzione ⇐ a coefficienti costanti (MZ1). Va cercata una versione con l'algebra di Weyl (moduli D, eliminazione nell'anello degli operatori a coefficienti polinomiali).
- **CONV-Q12.** Ordine L^∞ di Strang nel quadro di P3-T3. Numericamente l'ordine è 1 (V-ex, §6). Si chiede una prova, con la stima puntuale della serie modale vicino a x = 0.
- **CONV-Q6′.** Va verificata la norma degli ordini 1 (Dirichlet) e 1,5 (Neumann/Robin) in Dang–Einkemmer–Ostermann 2025, arXiv:2504.10125, per confrontarli con 5/4 in L² e 1 in L^∞ di CONV-T8. Aggiornamento post-Gate 8: CIT-AUDIT-8 conferma il titolo, ma la norma non è nell'abstract; resta aperta.
- **CONV-Q13.** Ordini superiori in ε per CONV-T8: la riduzione a 5/4 di Strang vale per l'errore completo e non solo per il coefficiente di ε? Si chiede anche il caso di dati non modali in H¹_0 o H².
- **CONV-Q14.** T4(b) e T5 con s reale non intero, via interpolazione complessa o reale: sono stati ritirati dall'enunciato.
- **CONV-Q15.** Chiusa: dopo il fix CONV-4 dell'audit F8, T1(7) vale per ogni n ≥ 2 con la prova del polinomio di Taylor, senza C3-P1[M2].
- **CONV-Q16.** Bordo: identificazione di una condizione al bordo con margine positivo usando un dizionario quoziente per le conseguenze tangenziali (CONV-B3). Va precisata la definizione e va dimostrato l'analogo di T4.
- **CONV-Q17.** (Dall'audit F8, fix CONV-1.) Per Ω convesso, D′(Ω) è un R_n-modulo iniettivo, e quindi vale ker(Q_1Q_2) = ker Q_1 + ker Q_2 anche in D′(Ω)? La fonte verificata (Malgrange exp. 246, p. 83) lo dichiara probabile ma non ottenuto con quel metodo. Da verificare in Palamodov 1970, cap. VII, e in Hörmander ICASV (CIT-AUDIT-8). CONV-D2 è ristretto a C^∞ fino ad allora. Aggiornamento post-Gate 8: CIT-AUDIT-8 §5 non ha trovato una fonte; l'esclusione è mantenuta.
