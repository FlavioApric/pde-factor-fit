# Kill-argument S4T-T3 (versione corretta) — Thread 2, arbitrato · subagente Claude fresco ae95d318d522a4e33 · 26/10/2026
Input: KA_S4T_T3_input.md + KA_S4T_T3_attack.md (nient'altro). Sintesi fedele per punti (testo integrale nella risposta del subagente; riportato qui in forma condensata).

| punto | accusa | classificazione | severità |
|---|---|---|---|
| P1 | (i),(ii) sono conseguenze della definizione A9 (salto di Lax–Oleinik di S_B) | partially_answered — enunciati veri, prova (ii) ricontrollata (1+t h_x < 1+t u₀′+δ < 0 su N_t^δ); Esito (a) onesto, ma titolo "Teorema negativo" e Lettura ("non ha risposta positiva") non circoscritti; A9 scelta sostenibile | major (cornice) |
| P2 | "PR3 ✔ in L∞" e "scatta il ramo teorema negativo" poggiano su un fatto definitorio; la sola norma che isola l'interazione (L¹ di E^add) è aperta | **still_unresolved** — nessun enunciato numerato falso; il problema è l'interpretazione dell'Esito | **major** |
| P3 | (iii) classico; Θ(√ν) da [F3] | partially_answered — limite inferiore ricontrollato a mano senza [F3] ((U⁺), costante 4e^{1/4}t√Mν^{3/2}/d², limite del calore, Fatou, 1/√(2π) ⇒ D√(t/π) per lato); "nessuna novità" (Lettura) vs "sostanziale" (Esito) in tensione | minor |
| P4 | ‖E^add‖_{L¹} aperto e la numerica suggerisce ordine 1 | partially_answered — nessun enunciato numerato assume O(ν) in L¹; (v) solo → 0; (vi) riduzione esatta corretta; aperto e dichiarato (Q1); possibile O(ν|log ν|) | major (problema aperto, non errore) |
| P5 | dipendenza da [F1] (e [F3]) non verificati | partially_answered — dipendenze dichiarate; [F1] classico; S4T-L0 non incluso nell'input | minor |
| P6 | (vii) confronto con un fantoccio (legge del getto oltre t*) | partially_answered — matematica corretta (D = εD̂(τ) indipendente da ν); il rapporto "violazione ≳ ε/ν" confronta con una legge che (i) già dichiara inapplicabile | minor |

Conteggi: answered 0 · partially 5 · still_unresolved 1 (major, nessun critical).
**Verdetto (calcolato da S-CHECK-11 con la tabella della skill, non dall'arbitro): WARN** (reason_code: unresolved_major_or_minor).
Valutazione netta dell'arbitro (sintesi): gli enunciati numerati reggono ((i)–(iii), (v)–(vii) ricontrollati; la costante 2D√(t/π) è dimostrata senza [F3]; nessun enunciato assume O(ν) in L¹ per E^add); il punto debole è lo strato interpretativo (Esito, titolo di T3, Lettura). Azioni: (1) riscrivere Esito e titolo come esito diviso (A9-forzato / negativo L¹ solo per E^mult_AB / aperto e numericamente O(ν) per E^add in L¹), ritirare "PR3 ✔ in L∞" come evidenza; (2) attaccare S4T-Q1 (Tang–Teng, Goodman–Xin: O(ν) vs O(ν|log ν|)); (3) verificare [F1]–[F3], riformulare (vii) come enunciato di scala.
Confronto con la v1 (PROOF_PACKAGE §13: FAIL, P4 still_unresolved critical): il punto critico P4 è sceso a partially_answered (major): ora è registrato APERTO e nessun enunciato lo assume; resta un rilievo major di cornice (P2).
