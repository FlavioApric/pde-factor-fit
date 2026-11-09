# KA OPF5A-T5 (+L5) — aggiudicazione (S-CHECK-20, 26/10/2026)
Attacco: KA_OPF5A_T5_attack.md. Esito: **SURVIVES**.
Verifica indipendente dell'aggiudicatore: calcolo termine a termine dei nuclei rifatto (j=0 diretto → T1; j=0 riflesso → B0; j=1 riflesso → B_L − ∫G(ξ+s−ct)ũ; somma → R_L), scala t^{k/2+5/4} del resto, esponente D^{k/2−1/4}.
Numerica: attaccante (L=1.3, (D,c)=(0.3,1.7),(2.0,−0.8), k=1,2,3, anche un solo estremo attivo): rapporto →1 con errore relativo ∝ t^{1/2}. Aggiudicatore (s20_opf5a (4), c=0.7, D=0.3, k=1): Richardson 0.171438 vs predetto 0.171442. Ñ_1=0.234005, Ñ_2=0.325244 (quad indipendente), Ñ_3=0.6103437 (attaccante).
Accolto (MINOR): per c<0 S_2 va definito come trasporto con inflow in L [F5A-7].
**Verdetto: SURVIVES.**
