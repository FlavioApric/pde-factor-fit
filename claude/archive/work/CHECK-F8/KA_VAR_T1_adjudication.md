# KA VAR-T1 — aggiudicazione (S-CHECK-F8-VAR, 27/10/2026)

Attacco: `KA_VAR_T1_attack.md`, scritto da un subagente indipendente che ha letto solo `KA_VAR_T1_input.md`. Esito dichiarato dall'attaccante: **SURVIVES**, con un rilievo di portata maggiore (A5) e una lacuna di portata (A6).

Verifica dell'aggiudicatore, indipendente dall'attacco (dettagli in `AUDIT_S8-VAR.md`, §2):
- L'identità di Carleman ‖P_λz‖² = ‖Sz‖² + ‖Az‖² + q(z) è ora **dimostrata simbolicamente** per φ generica, non solo verificata numericamente. In `sympy/var_carleman.py` si pone z = a + ib e si mostra che la densità |Pz|² − |Sz|² − |Az|² − q è una divergenza totale: il suo operatore di Eulero–Lagrange rispetto ad a e a b è identicamente nullo. Con il segno opposto del termine incrociato, invece, non lo è. Sono controllati simbolicamente anche P_λ = S + A, il peso (φ_xx = 2μ, φ_xxxx = 0, φ_x ∈ [−3/2, −1/2]) e la disuguaglianza di assorbimento, che si riduce a (4μp − q)²/(2μ) ≥ 0.
- La stima di Cauchy su g^{(k)} è stata controllata con mpmath su 35 coppie (t, k), con t da 0.05 a 0.9 e k fino a 16. Il rapporto massimo rispetto al maggiorante è 0.54 (`sympy/var_misc.py`).
- Ho rifatto a mano la lente di VAR-L1, la globalizzazione di VAR-L2 e il lemma di accumulazione di VAR-T1(b)(i). Concordo con i punti A2–A4 dell'attacco.

## Aggiudicazione punto per punto

| punto | accusa | verdetto | severità | azione |
|---|---|---|---|---|
| A1 | segno o termine sbagliato nel commutatore | respinto (risposto dal testo, e ora anche da una prova simbolica) | — | citare `var_carleman` nel package (fix VAR-17) |
| A2 | assorbimento e densità in VAR-L0 | respinto | — | — |
| A3 | lente, cut-off, supporto e regolarità di w | respinto | — | — |
| A4 | compattezza e s* in VAR-L2 | respinto | — | — |
| A5 | la classe L^∞ è nominale: se u ∈ C^{1,2}, V è continuo fuori da X_0 | **accolto** (rilevato anche in modo indipendente dall'aggiudicatore) | MAGGIORE (portata) | fix **VAR-1**: dichiarare la portata, oppure estendere a soluzioni forti |
| A6 | nel caso L^∞ di (c), \|Z(u)\| > 0 con int Z(u) = ∅ non è ricondotto alle fasce di silenzio | accolto come rilievo di presentazione. Il package lo dichiara già aperto (VAR-Q10), ma non nell'enunciato | MINORE | fix VAR-14: scriverlo nell'enunciato di (c) |
| A7 | regolarità C^∞ della serie di Tychonoff in t = 0 | respinto nel merito. Manca una riga sull'incollamento (derivate che tendono a 0 uniformemente, quindi l'estensione per zero è C^∞) | MINORE | fix VAR-14 |
| A8 | segno di θ in (a), "q.o. in x" in (b)(iii) | accolto come rilievo formale | MINORE | fix VAR-14 |

## Su A5: verifica e riparazione

L'osservazione è corretta. Su {u ≠ 0} la funzione (iu_t + u_xx)/u è continua e coincide con V q.o. Ne segue che un V con un salto in x_1 forza u(·, x_1) ≡ 0. Nel caso stazionario il salto di h″ in x_1 vale [V]·h(x_1), quindi h(x_1) = 0 (`var_misc` (7)). In particolare la **buca quadrata**, l'esempio canonico di potenziale L^∞, ha autofunzioni non nulle nei punti di salto e quindi non è coperta, perché le sue soluzioni non sono C^{1,2}.

L'enunciato resta vero, ma la frase "chiude la lacuna V ∈ L^∞ del VERDETTO F6" (domanda Q3 della CHECK_REQUEST) è vera solo dopo l'estensione a soluzioni forti. Ho controllato che l'estensione regge, in questa classe:

> u, u_x ∈ C(Ω), u_t, u_xx ∈ L²_loc(Ω), L_0u = Vu q.o.

I passi sono questi:
1. **VAR-L0.** La densità vale per w a supporto compatto con w, w_t, w_xx ∈ L²: w_ε → w e L_0w_ε → L_0w in L², e il peso è limitato.
2. **VAR-L1.** Il resto R contiene solo u e u_x, che sono continue, quindi R ∈ L². La stima è identica.
3. **VAR-L2.** Il passo è invariato, perché usa solo VAR-L1 e insiemi aperti.
4. **VAR-T1(b)(i).**
   - u_x(t, x_0) = 0 per continuità di u_x.
   - L'estensione ũ = 1_{x≥x_0}u ha ũ_x = 1_{x≥x_0}u_x, che è continua.
   - Quindi ũ_xx = 1_{x≥x_0}u_xx nel senso delle distribuzioni, senza delta, e ũ_t = 1_{x≥x_0}u_t.
   - In questo passo non serve u_xx(t, x_0) = 0.

## Verdetto

**SURVIVES.** Non ci sono errori analitici in VAR-L0, VAR-L1, VAR-L2 né in VAR-T1(a), (b), (c), e la serie di Tychonoff è corretta. Resta un rilievo MAGGIORE di portata (VAR-1), che si ripara con una riformulazione oppure con l'estensione a soluzioni forti appena descritta. Non serve un secondo kill-argument su VAR-T1.
