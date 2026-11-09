# VERDETTO — F6-ENC (P-B2: rimuovere V come "rumore" con un encoder analitico) · 26/10/2026
Skill caricate (lettura integrale dei SKILL.md): session-protocol, route-scout, claim-lifecycle, novelty-check (fasi A/B/D), math-skill (modo proof), scientific-critical-thinking. Niente ML; nessuno script `_vendor` eseguito. Dettagli e prove: `NOTE.md`; fonti: `sources.bib`; verifiche: `sympy/`.

## 1. Risposta alla domanda decisiva
**La richiesta nuda è vuota** (ENC-O1): W = 0, oppure il quadro d'interazione U_0(t)U_V(t)^{-1}, manda già ogni soluzione in una soluzione libera, ed è perfino cieco. Un encoder ha senso solo se è iniettivo (o ha un nucleo finito noto), intreccia gli operatori (W L_q = L_0 W) ed è esplicito. Con questa definizione:

| Strada | Esiste per | Tipo di W | Nucleo | Cieco? | Stato |
|---|---|---|---|---|---|
| ENC-1 operatore di trasformazione | **ogni q ∈ L¹ in 1D** (V(x)) | Volterra I + H, nucleo da Goursat, **indipendente da λ** | 0 | sì se V = V(x): q = (iu_t + u_xx)/u, poi Goursat | CON-FONTE (numero del teorema da verificare) + prova scritta dell'intertwining senza bordo; V-ex 5/5 + 2/2 |
| ENC-2 Darboux/Crum | q Darboux-banale (Pöschl–Teller, solitoni, Adler–Moser) | **differenziale** di ordine n | stati legati (dimensione n) | sì | V-ex 12/12; congettura ENC-K1 ("se e solo se") da verificare |
| ENC-3 puntuale + gauge | **V(t,x) = a(t)x² + b(t)x + c(t)** e solo questi | cambio di variabili × fase | 0 | sì | Avron–Herbst V-ex 5/5, lens/Mehler V-ex 6/6; "se e solo se": CON-FONTE secondaria (Boyer/Bluman) |
| ENC-4 Born / Lippmann–Schwinger | ogni q, ma **a λ fissato** | I + G_0^λ q (= copia dei dati di Cauchy) | 0 | banale | prova scritta; la serie converge sempre su un intervallo limitato (Volterra) |
| ENC-5 operatori d'onda Ω_±^* | V a corto raggio, ogni d, anche Dirac | globale, asintotico | stati legati | **sì, senza conoscere V**: lim e^{itH_0}u(t) | classico; fuori dal modello di dati di G★′ (Ω limitato) |
| ENC-6 omogeneizzazione | V(x/ε) periodico o stocastico | limite ε → 0 | — | sì (dipende solo da medie) | ampiezza O(1): libero; ampiezza ε^{-1}: libero + costante −⟨(∂^{-1}V)²⟩ (V-ex); ε^{-2}: V non si toglie (Bloch) |

**Esistenza, unicità, stabilità.** In 1D un encoder strutturato esatto esiste **sempre** per V = V(x): è l'operatore di trasformazione simmetrico, valido su tutte le f ∈ C² senza condizioni al bordo (prova in NOTE §2). È unico se si fissa che conservi i dati di Cauchy in x_0 (ENC-U1, candidato); senza questa normalizzazione è unico solo a meno del commutante di L_0. È stabile: lipschitziano in q ∈ L¹. È **locale** (differenziale) solo per la classe Darboux-banale, e **puntuale** solo per V quadratico. Se V dipende davvero dal tempo, non esiste un encoder che commuti con ∂_t: tutti gli intertwiner sono U_0 M U_V^{-1} (ENC-P0, prova scritta), salvo la classe quadratica.

## 2. Encoder cieco (l'interesse vero dell'utente)
- **ENC-N1 (prova scritta):** un encoder cieco esiste ⟺ la mappa (V, v) ↦ W_V^{-1}v è iniettiva. **Encoder cieco = identificazione congiunta di V e della parte libera**: coincide con B1 (F6-VAR).
- **Positivo:** V = V(x) indipendente dal tempo con dati non stazionari, oppure V quadratico in x. In questi casi V si legge puntualmente da u (dove u ≠ 0), poi W si costruisce. Asintoticamente: Ω^* senza conoscere V.
- **Teoremi negativi candidati (ENC-N2):** (a) da un solo modo stazionario, (q, λ) ~ (q + c, λ + c) e l'uscita Wu non è canonica; (b) per V(t,x) arbitrario l'identificazione è banale (V_u = (iu_t + u_xx)/u), ma non c'è un encoder strutturato; (c) gli encoder locali e asintotici cancellano gli stati legati, e le famiglie isospettrali danno lo stesso output asintotico; (d) con la classe di equazioni non fissata serve l'identificazione congiunta (P, q) (aperta).
- **Stabilità:** il collo di bottiglia è l'identificazione (q = u″/u perde due derivate ed esplode sugli zeri di u), non l'encoder (lipschitziano).

## 3. Domanda guida comune (I/S/E)
- **(I) SÌ, nel sottoanello.** Candidato **ENC-T2** (prova scritta): Ann_q(u) = φ^{-1}(Ann(Wu)) con φ(P) = P(τ, −ξ²). Se Ann(Wu) = (Q), allora Ann_q(u) è principale, con generatore lcm(Q, Q̃) oppure ξ·lcm. C3-T1 e C3-P1 si trasportano esattamente in ℂ[∂_t, L_q]. Gli operatori dispari in ∂_x si perdono, salvo q Darboux-banale (B_q = A∂A† commuta con L_q, verificato). Costo: Goursat O(n²) più C3-T1. Novità: trasporto non trovato in letteratura; ingrediente classico.
- **(S) SÌ / parziale.** Candidato **ENC-S1**: per P = ∏P_j coprimi in ℂ[τ, σ], su un rettangolo simmetrico, u = Σ W^{-1}v_j con ambiguità δ invariata; le costanti H^m si trasportano con ‖W‖‖W^{-1}‖. Da controllare: C12-T1′ per raggruppamenti coprimi. Non si trasportano i fattori non pari in ξ; la classe 𝔅 di P1-T2 non è invariante per W.
- **(E) NO in generale; SÌ esattamente nella classe con algebra risolubile.** W toglie proprio il termine potenziale, quindi E_int cinetico/potenziale diventa un difetto di coniugazione senza forma chiusa. Esattezza: V lineare (algebra risolubile di dimensione 4: Avron–Herbst, Wei–Norman, P1-T4). V quadratico: sl(2), quindi solo locale nel tempo (caustica del lens transform, coerente con P1-P5). Candidato **ENC-L1** (V-ex): ⟨∂², x^k⟩ ha dimensione infinita per k ≥ 3, contributo a P1-Q3.

## 4. Raccomandazione (criteri fissati in PLAN §3)
P1 ✔ (ENC-1 per ogni q ∈ L¹); P2 ✔ (I con ENC-T2, prova di mezza pagina); P3 ✔ (Pöschl–Teller 12/12, lens/Mehler 6/6, Avron–Herbst 5/5, più trasmutazione 5/5 + 2/2, omogeneizzazione 2/2, Lie 3/3); P4 ✔ (ENC-N1 + ENC-N2(a–d)).
**PROMUOVI** come S8-ENC, con questo perimetro: (i) ENC-1 + ENC-T2/ENC-S1 come lemmi di trasporto della Fase 9, passo 5 "encoder analitico per V" (L7: V(x) in 1D); (ii) ENC-2/ENC-3 come classi con encoder locale, con ENC-K1 ed ENC-L1 da chiudere; (iii) ENC-N1/N2 come teorema negativo dell'encoder cieco, da accoppiare a F6-VAR. **PARCHEGGIA** come sotto-strade ENC-5 (operatori d'onda: modello di dati globale, fuori G★′) ed ENC-6 (omogeneizzazione: solo approssimata, utile per il V "rumore" oscillante, L8). **ELIMINA** la lettura nuda "W u risolve la libera" (vuota, ENC-O1). Niente da eliminare per non analiticità.

**Costo stimato S8-ENC:** 1 sessione per ENC-T2/S1 + audit; 1 per ENC-K1/ENC-L1 (letteratura + prova); il caso Dirac va a F6-SYS / S8-SYS.
**Rischi (kill-argument da fare):** dipendenza di W dal punto base x_0 (non canonicità); domini non simmetrici o non rettangolari; q non liscio (H^m); d ≥ 2, dove ENC-1 non ha un analogo locale (open_questions 8).
