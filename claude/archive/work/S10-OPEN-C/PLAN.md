# S10-OPEN-C — PLAN (27/10/2026)

Compito: chiudere con esito onesto i problemi aperti di Fase 8 assegnati. Gli esiti possibili sono tre: (a) prova, (b) controesempio, (c) ostruzione o riduzione dimostrata («APERTO — ridotto a …»). SymPy serve solo come verifica. Gli stati in `LEDGER_ROWS.md` sono proposte: li assegna il coordinatore.

Convenzione: il «DM2 con rumore» di GATE8 §5, ATTACK-8 O8 e VAR-Q19 è letto come **DM-δ** (NOTAZIONE v6, riga 116).

| # | problema | predizione | via | limite di tempo |
|---|---|---|---|---|
| 1 | VAR-P11(e) (B ∈ C¹) | (a) | equazione di Volterra per la derivata e Gronwall; lemma sulla convoluzione C¹ | 40 min |
| 2 | VAR-Q18 (B solo continuo in norma) | (b) | X = ℋ ⊕ ℂ, B antiaggiunto di rango 2, soluzione fuori da D(A) | 30 min |
| 3 | VAR-Q10 (Z(u) di misura positiva con interno vuoto) | (a): esistenza, con V = 0 | serie di Tychonoff con g piatta su un Cantor grasso | 40 min |
| 4 | VAR-Q17 (L2-cor per dati mild) | (a) per V(x) e per V_0(x) + v(t); (c) per V(t,x) | mollificazione nel tempo | 30 min |
| 5 | VAR-P12(d) (log differenziale per V(t,x) generico) | (b) nella classe quadratica; (c) per il caso generale | monodromia in SL₂(ℝ) con tr < −2 | 30 min |
| 6 | VAR-C3Q2-open | (a) parziale: criterio di rango; (b) per VAR-Q12 | rango su B = ℂ[t,x]⟨∂_x⟩ | 30 min |
| 7 | Q-S8SYS-1 (prodotto di Euler con tempi polinomiali) | dicotomia: (a) formale, (b) a t fisso | serie in ℂ[ξ][[t]]; lemma sui polinomi esponenziali generalizzati | 45 min |
| 8 | II-T2(b′) derogatorio | (a) criterio per reticoli; (b) per la congettura «la forma di Jordan basta» | coppia A_1/A_2 3×3 | 30 min |
| 9 | Maxwell Q6 (RT-SYS) | (a) un campo identificante esiste | sizigie libere, pd ≤ 2 < 4, zoccolo nullo, SYS-EX | 30 min |
| 10 | ENC-T2(c′), classe principale | (a) in forma forte | perturbazione e^{αt}f e coprimalità | 25 min |
| 11 | ENC-Q4 | (a) per {q_0 + c} con DM-φ; (c) per la lettura DM3 letterale | Volterra quasinilpotente | 30 min |
| 12 | ENC-Q10 | (a) parziale (Darboux) + (c) | encoder non locale esplicito | 30 min |
| 13 | DICT-ILIM-Hs | (a) | condizione del cono, Taylor, equivalenza di norme sui polinomi | 30 min |
| 14 | DICT-U3d-v | (a) su [δ, T] per ogni nucleo c.m.; velocità in L¹(0,T) tramite il modulo ω_k | interpolazione di Čebyšëv nella variabile λ | 30 min |
| 15 | DICT-Q3 | (c): ridotto a un problema di divisione; (b): il test formale puntuale non basta in C^∞ | u = e^{−1/x²}1_{x>0} | 20 min |
| 16 | DICT-Q4 | (a): caratterizzazione «nessuna combinazione di rango finito» (Amitsur, CON-FONTE); (b) con atomi di media | dipendenza lineare locale | 25 min |
| 17 | VAR-L2-cor | da CON-FONTE a DIMOSTRATO, se l'audit conferma il punto 1 | — | — |
| 18 | Robustezza DM-δ / VAR-Q19 | (a): minimax Θ(ε^{1/3}) sotto vincoli a priori | due punti e stimatore consistente fattibile | 30 min |

Verifiche SymPy (`sympy/`):
- ricorrenza di Tychonoff;
- serie formale di Dirac e identità di prodotto;
- rango e sizigie di Maxwell;
- esempi II-T2;
- intertwining di Darboux e formula di κ;
- formula di VAR-Q18;
- traccia −5,2;
- ENC-T2(c′);
- esempio d'onda C3Q2;
- divisione in DICT-Q3;
- controesempio di DICT-Q4;
- interpolazione in λ di DICT-U3d-v.

Se un tentativo fallisce entro il limite di tempo, l'esito diventa (c) con la riduzione scritta oppure APERTO con il motivo.
