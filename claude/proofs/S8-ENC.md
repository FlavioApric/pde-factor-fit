# PROOF_PACKAGE — S8-ENC (Fase 8, problema B2: togliere V come "rumore" con un encoder analitico) · 27/10/2026

**Stati.** Nessun enunciato è DIMOSTRATO: manca l'audit di S-CHECK-F8. "Prova scritta" significa prova completa non auditata. "CON-FONTE (da verificare)" significa enunciato pubblicato con numero di teorema o pagina non controllati. "V-ex" significa verificato solo su esempi. Gli enunciati marcati FALSO hanno un controesempio esplicito.

**Revisione 2 (27/10/2026): recepimento dell'audit S-CHECK-F8-ENC** (`work/CHECK-F8/AUDIT_S8-ENC.md`, `KA_ENC_N1_*`, `KA_ENC_P0_*`). Sono applicati i fix ENC-1…ENC-15; la mappa "fix → modifica → sezione" è in `RECEPIMENTO.md`. La prima versione è conservata in `PROOF_PACKAGE.v1.md`.
- I claim nuovi sono marcati **DA AUDITARE**: ENC-P0(b)^cl, ENC-P0(b)^loc, ENC-P0′ su nucleo denso, ENC-P0′-DIC, POLE-N^cl, ENC-T2(c′).
- Gli stati "DIMOSTRATO" citati in questo testo sono quelli **proposti dal revisore** e vanno registrati da central.
- Verifica aggiuntiva: `enc_recep` 10/10.

**Revisione 2.1 (27/10/2026): recepimento post-Gate 8** (`GATE8.md`). Fonti: `work/CHECK-F8/AUDIT_S8-ENC_rev2.md` (fix ENC2-1…ENC2-6), `research/DEVIL/ATTACK-8.md` (O2, O16), `research/CIT-AUDIT/AUDIT-8.md` §5. La mappa è in `RECEPIMENTO.md`, sezione "post-Gate 8".
- La strada RT-ENC è **PARCHEGGIATA**. I lemmi di questo pacchetto passano alle strade RT-DICT (ENC-1, ENC-U1, ENC-C1, ENC-T2) e RT-IDV (ENC-P0, ENC-P0′, POLE-N, ENC-N1′, ENC-A9).
- Due claim nuovi della rev. 2 sono **FALSI come scritti** e sono sostituiti dalla versione corretta: ENC-P0(b)^loc ed ENC-P0′-DIC. ENC-T2(c′) è circoscritto alla classe C^∞(Ω) senza vincoli.
- Gli stati sono cambiati solo verso il basso. Verifica aggiuntiva: `enc_g8` 5/5.

**Skill caricate.** `skills-local/session-protocol` e `skills-local/claim-lifecycle`, con la catena proof-writer → math-skill (modo proof, controesempi e casi limite presto) → SymPy → CHECK_REQUEST per S-CHECK-F8 → kill-argument (passaggio avversariale interno, §10: i revisori esterni della skill non sono disponibili, quindi REVIEW_UNAVAILABLE) → scientific-critical-thinking per gli stati. Nessuno script `_vendor` eseguito, niente ML.

**Verifiche (SymPy/mpmath/numpy, solo controllo).** Comando: `D:\ProblemaBase\.venv\Scripts\python.exe -I work/S8-ENC/sympy/<script>.py`. Esiti:
- `enc1_goursat` 14/14 (ENC-1, ENC-U1, punto base);
- `enc_algebra` 22/22 (ENC-T2(b), ENC-K0, ENC-K1′, P0′ lente, stima di E^mult; al primo rilancio di questa sessione falliva solo per la codifica della console, corretta con `sys.stdout.reconfigure`);
- `eint_closed` 21/21 (forme chiuse di A9);
- `enc_s8b` 23/23 (getti, ricorsione di K0, passo di Darboux generico, E^mult lineare esatto, stima raffinata e limite, NS-EQUIV con bordo, Foldy–Wouthuysen, Faddeev, nucleo di Pöschl–Teller simbolico).

Totale 80/80.

**Notazione.** L_q := −∂_x² + q(x), L_0 := −∂_x², H_0 := L_0 su L²(ℝ). R := ℂ[τ, ξ] (τ ↔ ∂_t, ξ ↔ ∂_x). S := ℂ[τ, σ] (σ ↔ L). φ: S → R, φ(P)(τ, ξ) := P(τ, −ξ²). Per Q ∈ R, Q̃(τ, ξ) := Q(τ, −ξ). Ann_q(u) := {P ∈ S : P(∂_t, L_q)u = 0}. Ann(v) ⊆ R è l'annullatore di C3-T1. I modelli di dato sono quelli di NOTAZIONE v5 (DM1–DM3, DM-φ, DM-inv). E_int è sempre quello di A9; E^conj è il difetto di coniugazione di un encoder.

## 0. Confronto con la predizione (PLAN §2)

| claim | predizione | esito |
|---|---|---|
| ENC-1 | dimostrabile con q ∈ C¹; unicità nella classe di Volterra simmetrica; dipendenza da x_0 | **confermato**. Prova scritta completa (§2), con classificazione {T_{k_0}} ed ENC-U1 |
| ENC-T2 | corretto a q noto; (c) diventa "biiezione triangolare dei getti" | **confermato** (§3). In più, la prova di (c) è autonoma: non usa C3-P1 |
| ENC-P0 | P0′ con riparametrizzazione del tempo; la lente sta in P0′ | **rev. 2: la sintesi "le eccezioni cambiano il tempo" è FALSA** (Avron–Herbst ha θ = id). Valgono P0(b), le versioni classica e localizzata con le ipotesi (i)/(ii) di ENC2-1, P0′ come forma normale su nucleo denso e, in forma esistenziale, "si può scegliere θ = id ⟺ α ≡ 0" (§4, post-Gate 8) |
| ENC-N1 | "⟺" falso come scritto; forma corretta con un'ipotesi di separazione (S) | **confermato** (§5). In più c'è un esempio di encoder cieco senza identificabilità (DM-φ con (E2′)) |
| (E2) | q ≡ c ≠ 0 senza intertwiner differenziale a ogni ordine | **confermato** (§1, ENC-K0, ricorsione esplicita) |
| ENC-K1 | direzione ⇒ locale dimostrabile; caratterizzazione globale CON-FONTE | **confermato** (§6). ENC-K1′ con prova scritta, ENC-K1 declassato a CON-FONTE (Duistermaat–Grünbaum solo per V → 0) |
| E_int A9 | quattro forme chiuse e una stima di ordine t² | **confermato, con correzioni**. La costante del termine t³ è 2/3, non 1, ed è ottimale (rev. 2). La stima di (b2) della prima versione era falsa ed è corretta. Le forme lineare e di Pöschl–Teller hanno prova completa; quella quadratica è fusa in VAR-T10 (§7) |

Sono fuori predizione: NS-EQUIV su Ω limitato (§8) e le quattro strade riaperte (§9). La formula di Avron–Herbst di F6-ENC NOTE §5 era nella normalizzazione H = −½∂² + Fx. Qui è riscritta nella normalizzazione del progetto: u = e^{−iFtx − iF²t³/3} v(t, x + Ft²). Lo stesso vale per l'encoder inverso della stessa riga di NOTE (fix ENC-12).

---

## 1. Che cosa è un encoder; definizione (E2) modulo costanti

**[ENC-D] Definizione (prova scritta della buona posizione, non è un teorema).** Sia J un intervallo e sia q dato. Un *encoder strutturato* per L_q è un operatore lineare W, definito su uno spazio di funzioni 𝒴 (precisato caso per caso: C²(J), C^∞(J), L²(J)), con le tre proprietà seguenti:
- (E1) dim ker W < ∞ **sul dominio 𝒴 dell'encoder**, non solo sulle soluzioni (fix ENC-14). Con la lettura "iniettivo sulle soluzioni", un encoder per restrizione a una regione in cui V è autonomo sarebbe ammesso (§4, P0(b)^loc);
- (E2′) *modulo costanti*: W L_q = (L_0 + c)W per qualche c ∈ ℂ; quindi W commuta con ∂_t quando agisce solo in x. Nel caso non autonomo la condizione diventa W(t)(i∂_t − H(t)) = (i∂_t − H_0 − c)W(t). La versione stretta (E2) è c = 0;
- (E3) W è esplicito: differenziale, puntuale più gauge, oppure di Volterra con nucleo dato da un problema ben posto.

Con c ≠ 0 la soluzione libera è definita a meno del fattore e^{−ict}, cioè della fase globale di DM-φ. (E2′) è la scelta registrata in NOTAZIONE v5.

**[ENC-O1] Osservazione (banale).** Senza (E1)–(E3) la richiesta è vuota. W = 0 va bene, e su ℝ va bene anche il quadro d'interazione W(t) = U_0(t)U_V(t)^{−1} (F6-ENC NOTE §1).

**[ENC-K0] Proposizione (prova scritta; SymPy `enc_algebra` ordini ≤ 5, `enc_s8b` ricorsione per n ≤ 6).** Siano J ⊂ ℝ un intervallo aperto, c ∈ ℂ ∖ {0} e W = Σ_{j=0}^{n} w_j ∂^j con w_j ∈ C^∞(J; ℂ) e w_n ≢ 0. Allora W L_c ≠ L_0 W. Quindi q ≡ c ≠ 0 non ha intertwiner differenziale stretto di nessun ordine. Con (E2′) lo ha: W = I, con W L_c = (L_0 + c)W.

*Prova.* Si ha W L_c − L_0 W = [∂², W] + cW = Σ_j (w_j″∂^j + 2w_j′∂^{j+1}) + cW (`enc_s8b`, controllo 2b). Supponiamo che sia nullo e leggiamo i coefficienti.
- Coefficiente di ∂^{n+1}: 2w_n′ = 0, quindi w_n è una costante non nulla.
- Coefficiente di ∂^j per 1 ≤ j ≤ n: w_j″ + 2w_{j−1}′ + c w_j = 0.
- Coefficiente di ∂^0: w_0″ + c w_0 = 0.

*Induzione su k* = 0, …, n: w_{n−k} è un polinomio di grado esattamente k, con coefficiente di testa (−c/2)^k w_n/k!. Il passo è il seguente. Se w_j ha grado k con testa ℓ, allora w_{j−1}′ = −(w_j″ + c w_j)/2 ha grado k e testa −cℓ/2, perché w_j″ ha grado minore di k. Dunque w_{j−1} ha grado k + 1 e testa −cℓ/(2(k + 1)).

Per k = n, w_0 ha grado n e testa (−c/2)^n w_n/n! ≠ 0. Ma allora w_0″ + c w_0 ha grado n e testa c(−c/2)^n w_n/n! ≠ 0, contro l'ultima equazione. ∎

*Lettura.* (E2) stretta esclude il caso più semplice. (E2′) lo recupera, ed è la definizione usata nel resto del pacchetto.

---

## 2. ENC-1: l'operatore di trasformazione di Volterra simmetrico (ipotesi dentro l'enunciato)

**[ENC-1] Teorema (prova scritta completa; CON-FONTE in sostanza: Marchenko 1986 cap. 1, citato senza numero di teorema (CIT-AUDIT-8 §5), Povzner 1948, Levitan 1987. Le costanti non sono verificate, CIT-AUDIT-6 voce 9; SymPy `enc1_goursat` 14/14).**

*Ipotesi:*
- (H1) un punto base x_0 ∈ ℝ e un raggio a > 0; J := [x_0 − a, x_0 + a] è simmetrico attorno a x_0 (si trasla x_0 in 0);
- (H2) q ∈ C¹(J; ℂ); q complesso è ammesso;
*Notazione (definizione, non ipotesi; fix ENC-8(a)):* Δ := {(x, s) : |s| ≤ |x| ≤ a} = Δ_+ ∪ Δ_− (x ≥ 0, x ≤ 0), due triangoli chiusi uniti nell'origine.

*Tesi.*
1. Esiste un'unica K ∈ C(Δ), di classe C² su ciascun Δ_±, tale che

   K_xx − K_ss = q(x)K su Δ, K(x, x) = ½∫_0^x q, K(x, −x) = 0. (G)
2. L'operatore Tf(x) := f(x) + ∫_{−x}^{x} K(x, s) f(s) ds manda C²(J) in C²(J). Per **ogni** f ∈ C²(J), senza condizioni al bordo né in 0, valgono L_q Tf = T L_0 f, (Tf)(0) = f(0) e (Tf)′(0) = f′(0).
3. T è biiettivo su C(J) e su C²(J). L'inverso è W := T^{−1} = I + ∫_{−x}^{x} H(x, s)·ds, dove H è l'unica soluzione dello stesso tipo di H_xx − H_ss = −q(s)H, H(x, x) = −½∫_0^x q, H(x, −x) = 0. Vale W L_q = L_0 W su C²(J).
4. Se q ∈ C^∞(J), allora T e W sono biiezioni di C^∞(J).
5. (*Stima e stabilità.*) Sia Q := ‖q‖_∞. Allora ‖K‖_∞ ≤ (aQ/2)e^{a√Q}. Inoltre ‖K_q − K_{q′}‖_∞ ≤ C(a, Q, Q′)‖q − q′‖_∞, e ‖T‖, ‖W‖ ≤ 1 + 2a‖K‖_∞ (risp. ‖H‖_∞) su C(J) e su L²(J). Su L² vale anche la stima più fine 1 + √2·a‖K‖_∞.
6. (*Dipendenza dal punto base.*) T dipende da x_0 già per q costante: per q ≡ c ≠ 0 i due operatori T^{(x_0)} e T^{(x_1)} con x_0 ≠ x_1 sono diversi.

*Prova.*

**(1) Goursat.** Usiamo le coordinate caratteristiche ξ = x + s, η = x − s, con K(x, s) = Φ(x + s, x − s). Allora K_xx − K_ss = 4Φ_ξη. Le condizioni diventano Φ(ξ, 0) = ½∫_0^{ξ/2} q e Φ(0, η) = 0. Δ_+ corrisponde a {ξ, η ≥ 0, ξ + η ≤ 2a} e Δ_− a {ξ, η ≤ 0, ξ + η ≥ −2a}. Il problema (G) equivale all'equazione integrale

   Φ(ξ, η) = ½∫_0^{ξ/2} q + ¼∫_0^ξ ∫_0^η q((α + β)/2) Φ(α, β) dβ dα. (G′)

Infatti, derivando (G′) si ottiene 4Φ_ξη = q((ξ + η)/2)Φ e le condizioni al bordo, e viceversa integrando 4Φ_ξη due volte.

Approssimazioni successive: Φ_0 := ½∫_0^{ξ/2} q e δ_n := Φ_n − Φ_{n−1}. Poiché |Φ_0| ≤ aQ/2 e ∫_0^{|ξ|}∫_0^{|η|}(αβ)^n dβ dα = (|ξη|)^{n+1}/(n + 1)², per induzione |δ_n| ≤ (aQ/2)(Q|ξη|/4)^n/(n!)². Su Δ si ha |ξη| ≤ a², quindi la serie converge uniformemente con somma ≤ (aQ/2)Σ z^n/(n!)² ≤ (aQ/2)e^{2√z}, z = Qa²/4: è la stima di (5). La stessa maggiorazione applicata alla differenza di due soluzioni dà l'unicità. Le due regioni si trattano separatamente; in entrambe Φ(0, 0) = 0, quindi K è continua su Δ.

Regolarità:
- Φ_ξ = ¼q(ξ/2) + ¼∫_0^η q((ξ + β)/2)Φ(ξ, β)dβ;
- Φ_η = ¼∫_0^ξ q((α + η)/2)Φ(α, η)dα;
- Φ_ξη = ¼q((ξ + η)/2)Φ;
- Φ_ξξ = ⅛q′(ξ/2) + ¼∫_0^η [½q′((ξ + β)/2)Φ + q((ξ + β)/2)Φ_ξ](ξ, β)dβ, e simmetricamente Φ_ηη.

Tutte sono continue perché q ∈ C¹. Quindi Φ ∈ C² su ciascuna regione e K ∈ C²(Δ_±).

**(2) Intrecciamento.** Fissiamo x ≠ 0 e poniamo g := Tf. La regola di Leibniz, con K(x, −x) ≡ 0, dà

   g′ = f′ + K(x, x)f(x) + ∫_{−x}^{x}K_x f ds,
   g″ = f″ + (d/dx)K(x, x)·f(x) + K(x, x)f′(x) + K_x(x, x)f(x) + K_x(x, −x)f(−x) + ∫K_xx f.

Integrando per parti due volte,

   ∫_{−x}^{x}K f″ = K(x, x)f′(x) − K(x, −x)f′(−x) − K_s(x, x)f(x) + K_s(x, −x)f(−x) + ∫K_ss f.

Sostituendo in −g″ + qg + f″ + ∫K f″ (cioè L_q g − T L_0 f), i coefficienti sono:
- di f(x): q − (d/dx)K(x, x) − K_x(x, x) − K_s(x, x) = q − 2(d/dx)K(x, x) = 0;
- di f(−x): −K_x(x, −x) + K_s(x, −x) = −(d/dx)K(x, −x) = 0;
- di f′(x) e f′(−x): si cancellano;
- sotto l'integrale: −K_xx + K_ss + qK = 0.

Per x < 0 il calcolo è identico, con l'integrale orientato.

*Passaggio per x = 0.* g è C¹ su J: g′ è continua su ciascun lato e in 0 vale f′(0) da entrambi i lati, perché K(0, 0) = 0 e l'integrale si annulla. Su ciascun lato g″ = qg + T(f″). Il secondo membro è continuo su tutto J: T manda C(J) in C(J), perché K è limitata e l'integrale tende a 0 per x → 0. Per il teorema del valor medio applicato a g′, una funzione C¹ con derivata seconda laterale continua e con lo stesso limite da entrambi i lati è C² (risposta a D1 confermata dal revisore). Quindi g ∈ C²(J) e l'intrecciamento vale su tutto J.

Dati di Cauchy: g(0) = f(0) e g′(0) = f′(0) + 2K(0, 0)f(0) = f′(0).

**(3) Inverso.** Il nucleo H esiste per lo stesso argomento di (1), con q((ξ − η)/2) al posto di q((ξ + η)/2) e il segno opposto. Il calcolo di (2), a ruoli scambiati, dà L_0 T′ = T′ L_q su C², dove T′ := I + ∫H. Il coefficiente di f(x) è −2(d/dx)H(x, x) − q = 0. T′ conserva i dati di Cauchy.

Poniamo S := T′T su C²(J). S commuta con L_0 e conserva i dati di Cauchy. Inoltre ha la forma I + ∫_{−x}^{x}R(x, s)ds con R continua: nella composizione l'integrale doppio vive su |s| ≤ |y| ≤ |x|.

Per k ∈ ℂ, la funzione S e^{k·} risolve y″ = k²y con dati (1, k), quindi coincide con e^{k·}. Dunque ∫_{−x}^{x}R(x, s)e^{ks}ds = 0 per ogni k. Per l'unicità della trasformata di Fourier–Laplace di una funzione continua a supporto compatto, R(x, ·) ≡ 0, cioè S = I.

V(f)(x) := ∫_{−x}^{x}K(x, s)f(s)ds è quasi-nilpotente su C(J): per induzione |V^n f(x)| ≤ ‖K‖^n(2|x|)^n‖f‖/n!. Quindi T è invertibile su C(J) (serie di Neumann). T′T = I vale sul sottoinsieme denso C²(J) e T′, T sono limitati su C(J), quindi T′T = I su C(J) e T′ = T^{−1}. Ne segue TT′ = I su C(J). Poiché T′ manda C² in C², T^{−1}(C²) ⊂ C²: T è biiettivo su C²(J).

**(4) Regolarità C^∞.** L'identità g″ = qg + T(f″) e l'induzione sull'ordine danno: f ∈ C^{2m} e q ∈ C^{2m−2} (con q ∈ C¹ per m = 1) implicano Tf ∈ C^{2m}. Per gli ordini dispari si usa g′ = f′ + K(x, x)f + ∫K_x f. Lo stesso vale per T′.

**(5) Stabilità.** La stima di ‖K‖ è in (1). La differenza δΦ := Φ_q − Φ_{q′} risolve δΦ = δΦ_0 + ¼∫∫[q δΦ + (q − q′)Φ_{q′}], con |δΦ_0| ≤ a‖q − q′‖/2. La stessa iterazione dà ‖δΦ‖ ≤ (a/2 + a²‖Φ_{q′}‖/4)e^{a√Q}‖q − q′‖. Su C(J): ‖T‖ ≤ 1 + 2a‖K‖. Su L²(J): il nucleo è limitato su Δ, di misura 2a², quindi la parte integrale è di Hilbert–Schmidt con norma ≤ √2·a‖K‖ ≤ 2a‖K‖ (fix ENC-8(d)).

**(6) Punto base.** Per q ≡ c, T^{(x_0)}e^{ik·} è l'autofunzione di L_c con autovalore k² e con i dati di Cauchy di e^{ikx} in x_0:

   T^{(x_0)}e^{ik·}(x) = e^{ikx_0}[cos μ(x − x_0) + ik sin μ(x − x_0)/μ], μ² = k² − c.

Valutata in x = x_1 vale e^{ikx_0}[cos μ(x_1 − x_0) + ik sin μ(x_1 − x_0)/μ], che in generale è diversa da e^{ikx_1} = T^{(x_1)}e^{ik·}(x_1) quando μ ≠ k. Per q = 2, k = 3/2, x_0 = 0, x_1 = 1/5 la differenza in x = 1/3 è ≈ 0.092 + 0.012i (`enc1_goursat`). ∎

**[ENC-U1] Classificazione e unicità (prova scritta; SymPy `enc1_goursat`).** Ipotesi di ENC-1. Sia 𝒯 la classe degli operatori T = I + ∫_{−x}^{x}K(x, s)·ds, con K ∈ C(Δ) ∩ C²(Δ_±), tali che L_q T = T L_0 su C²(J).
- (a) 𝒯 = {T_{k_0} : k_0 ∈ ℂ}, dove T_{k_0} ha il nucleo di Goursat con K(x, −x) ≡ k_0 e K(x, x) = k_0 + ½∫_0^x q.
- (b) (T_{k_0}f)′(0) = f′(0) + 2k_0 f(0). Quindi T_0 = T di ENC-1 è l'**unico** elemento di 𝒯 che conserva i dati di Cauchy in x_0.

*Prova.* Il calcolo di (2) vale per ogni K di questa regolarità e dà

   L_q Tf − T L_0 f = A(x)f(x) + B(x)f(−x) + ∫_{−x}^{x}C(x, s)f(s)ds,

con A = q − 2(d/dx)K(x, x), B = −2(d/dx)K(x, −x) e C = K_ss − K_xx + qK. Il fattore 2 di B corregge un refuso della prima versione (fix ENC-7): viene dal termine K(x, −x)f(−x) della regola di Leibniz in g′, che in ENC-1 è nullo perché K(x, −x) ≡ 0 (`enc_recep` 1/1). Se l'espressione si annulla per ogni f ∈ C²(J), allora:
- prendendo f con supporto in un piccolo intervallo interno a (−|x|, |x|) si ottiene C(x, ·) = 0 all'interno, e per continuità C ≡ 0;
- poi, con f(x) = 1 e f(−x) = 0, si ottiene A = 0, e analogamente B = 0.

Quindi K(x, −x) è costante su ciascun lato, con limite K(0, 0) in 0: vale K(0, 0) =: k_0 su entrambi i lati. Inoltre K(x, x) = k_0 + ½∫_0^x q. Il Goursat con questi dati ha soluzione unica, con la stessa iterazione di (1) e Φ_0 = k_0 + ½∫_0^{ξ/2} q. Viceversa ogni T_{k_0} sta in 𝒯 per il calcolo di (2). (b) è il calcolo di g′(0). ∎

*Lettura.* Senza normalizzazione l'encoder di Volterra è definito a meno di una retta affine di parametro k_0. Per q = 0 questa retta è {I + k_0∫_{−x}^{x}}: è un pezzo del commutante di L_0 (`enc1_goursat`). La normalizzazione "conserva i dati di Cauchy in x_0" lo rende unico, ma dipende dal punto base (6). ENC-U1 è dunque chiuso in questa classe. Resta aperto in classi più ampie, per esempio con nuclei solo L¹ o non triangolari (open_questions Q1).

**[ENC-C1] Corollario (prova scritta).** Ipotesi di ENC-1 con q ∈ C^∞(J°), Ω = I × J° (I intervallo aperto) e u ∈ C^∞(Ω). Per ogni P ∈ S:

   P(∂_t, L_q)u = 0 ⟺ P(∂_t, L_0)(Wu) = φ(P)(∂_t, ∂_x)(Wu) = 0.

Lo stesso W serve per Schrödinger, calore, onda, Klein–Gordon e ogni polinomio in (∂_t, L_q).

*Prova.* Si usa un'esaustione J° = ∪J_{a′}, a′ < a; i nuclei sono compatibili per l'unicità di (G). W agisce in x e commuta con ∂_t: il nucleo non dipende da t e si deriva sotto il segno d'integrale (u è C^∞ su compatti). Per induzione W L_q^j = L_0^j W su C^∞. W è biiettivo su C^∞(J°) per ENC-1(4). ∎

*Spazi per la regola R6 di S8-DICT* (risposta alla DOMANDA, §11): W e W^{−1} sono limitati su C(Ī × J) e su L²(I × J), con ‖W‖ ≤ 1 + 2a‖H‖_∞. Su questi spazi dist(u, ker P(∂_t, L_q)) e dist(Wu, ker φ(P)(∂)) si confrontano con ‖W‖ e ‖W^{−1}‖. Su H^{2k} la limitatezza segue dall'identità (Wf)″ = W(f″) − W(qf) per induzione, con q ∈ C^{max(1, 2k−2)}. Questo caso H^{2k} è una prova schizzata, non riportata per esteso: è in open_questions Q2.

---

## 3. ENC-T2: lemma di trasporto a q noto (fix F6)

**[ENC-T2] Lemma (prova scritta; SymPy `enc_algebra` (b) 6/6, `enc_s8b` (c) 2/2).** Ipotesi di ENC-C1. **q è noto**: il lemma non identifica q. Se q non è dato, l'uso del lemma per l'identificazione B1 è circolare (DEVIL-6 O6). Modello di dato: DM3 su Ω = I × J°, rettangolo simmetrico attorno a x_0.
- (a) Ann_q(u) = φ^{−1}(Ann(Wu)) = φ^{−1}(Ann(Wu) ∩ ℂ[τ, ξ²]).
- (b) Se Ann(Wu) = (Q) con Q ≠ 0, allora Ann_q(u) = (P_*) è principale, con φ(P_*) = lcm(Q, Q̃) se questo è pari in ξ, e φ(P_*) = ξ·lcm(Q, Q̃) se è dispari. Si ha sempre lcm(Q, Q̃)~ = ±lcm(Q, Q̃).
- (c) (*Getti.*) Per ogni N la mappa j^N_{(t_0, x_0)}u ↦ j^N_{(t_0, x_0)}(Wu) è ben definita, lineare e triangolare unipotente. Dipende solo dal getto di q in x_0 di ordine N − 2. In particolare (Wf)(x_0) = f(x_0), (Wf)′(x_0) = f′(x_0) e (Tf)″(x_0) = f″(x_0) + q(x_0)f(x_0). **W non conserva i getti, li trasforma in modo triangolare.** L'induzione vale per ogni ordine (risposta a D5 del revisore).
- (c′) (*Osservazione elementare, non usa W; fix ENC-6(a) ed ENC2-6; prova scritta, DA AUDITARE.*)
   - **Definizione.** Fissata una classe 𝒞 di dati, un getto j^N u in (t_1, x_1) *certifica* Ann_q(u) = (P_*) in 𝒞 se ogni u′ ∈ 𝒞 con lo stesso N-getto in (t_1, x_1) ha Ann_q(u′) = (P_*).
   - **Enunciato** (circoscritto a 𝒞 = C^∞(Ω) senza vincoli, post-Gate 8). Sia q ∈ C^∞ (basta q ∈ C^{2d−2}, con d come nella prova) e sia P_* ≠ 0. Per **ogni** punto (t_1, x_1) ∈ Ω e ogni N, nessun getto finito j^N u in (t_1, x_1) certifica Ann_q(u) = (P_*) in C^∞(Ω).
   - *Con un vincolo di grado* l'enunciato è **FALSO** (ENC2-6, KA P7): fra gli annullatori principali di grado totale ≤ 1, il 4-getto di e^{x²} certifica Ann = (τ).
   - *Nella classe degli annullatori principali* l'enunciato è **APERTO**: la perturbazione della prova fa uscire dalla classe (con u = e^{x²}, u + e^{αt}x^M ha annullatore non principale).
   - R6 di S8-DICT non usa (c′).

*Prova.*

(a) Segue da ENC-C1 e dall'iniettività di φ, la cui immagine è R^{pari} := ℂ[τ, ξ²].

(b) Primo passo: L := lcm(Q, Q̃) soddisfa L̃ = ±L. Infatti anche L̃ è un lcm di {Q̃, Q}, quindi L̃ = cL con c costante (le unità di R sono le costanti). Applicando di nuovo la tilde, L = c²L, quindi c = ±1.

Secondo passo: QB è pari ⟺ QB ∈ (L) ∩ R^{pari}. Se QB è pari, QB = (QB)~ = Q̃B̃, quindi Q̃ | QB e Q | QB, cioè L | QB. Viceversa, ogni multiplo di L è un multiplo di Q.
- Se L è pari: LB è pari ⟺ B è pari, quindi (Q) ∩ R^{pari} = L·R^{pari}.
- Se L è dispari: L = ξL_1 con L_1 pari (un polinomio dispari in ξ contiene solo potenze dispari). Allora LB è pari ⟺ B è dispari ⟺ B = ξB_1 con B_1 pari. Quindi (Q) ∩ R^{pari} = ξL·R^{pari}.

Si conclude con (a).

(c) Da W L_q = L_0 W segue (Wf)″ = W(f″) − W(qf). Per induzione (Wf)^{(n)}(x_0) = f^{(n)}(x_0) + Σ_{j ≤ n−2}c_{n,j}f^{(j)}(x_0), con c_{n,j} polinomi nel getto di q. Le derivate in t passano perché W commuta con ∂_t. Lo stesso vale per T = W^{−1} (`enc_s8b`: (Tf)‴(0) = f‴(0) + (3/2)f′(0) − f(0)/3 per q = 3/2 − x/3 + (5/7)x²).

(c′) Nella prima versione era provata solo in x_0, perché T non è locale fuori da x_0 (T2c2 dell'audit). Ecco una prova diretta in ogni punto.

Sia d := deg_σ P_*(τ, σ) e sia p_d(τ) il coefficiente di σ^d. Si sceglie α ∈ ℂ con p_d(α) ≠ 0. Si pone h := e^{αt}(x − x_1)^M con M > max(N, 2d). Allora L_q^j(x − x_1)^M = (−1)^jM!/(M − 2j)!·(x − x_1)^{M−2j} + (potenze più alte di x − x_1), perché q aumenta il grado. Quindi P_*(α, L_q)(x − x_1)^M = p_d(α)(−1)^dM!/(M − 2d)!·(x − x_1)^{M−2d} + (ordini superiori) ≢ 0 (`enc_recep` 1/1).

Dunque j^N h = 0 in (t_1, x_1) e P_*(∂_t, L_q)h = e^{αt}P_*(α, L_q)(x − x_1)^M ≠ 0. Ne segue che u′ := u + h ha lo stesso N-getto di u e P_* ∉ Ann_q(u′). Inoltre h ∈ C^∞(Ω), quindi u′ sta nella classe dei dati (DM3), e L_q^d h richiede solo q ∈ C^{2d−2}. La prova non controlla altre proprietà di Ann_q(u′): per questo l'enunciato vale in C^∞(Ω) senza vincoli e non in classi ristrette. ∎

*Lettura (fix F6).* ENC-T2 dice che, **dato q**, la teoria a coefficienti costanti (C3-T1, C12-T1′) si trasporta esattamente nel sottoanello ℂ[∂_t, L_q]. Gli operatori dispari in ∂_x si perdono. L'esempio è Wu = e^{ikx − ik²t}: Ann(Wu) = (τ + ik², ξ − ik) e Ann_q(u) = (τ + ik², σ − k²), e il "verso" ξ − ik si perde. L'esempio illustra (a), non (b): Ann(Wu) qui non è principale (fix ENC-6(b)). Gli elementi dispari di Ann(Wu) corrispondono a W^{−1}∂_xW, che in generale non è differenziale.

*Uso per B1 (fix ENC-6(b)).* Come lemma ENC-T2 non è circolare, perché dichiara q noto. Per B1 (identificare l'operatore) è inutilizzabile senza q: per calcolare W serve q, e per avere q da u serve conoscere la forma P. VAR-T1(b) vale per la forma di Schrödinger nota; calore e onda richiedono formule diverse. In G★″ ENC-T2 non va contato fra gli strumenti di B1. Se q non è dato, prima serve VAR-T1(b): q = (iu_t + u_xx)/u, che richiede la forma di Schrödinger nota.

**[ENC-S1] (non riscritto qui).** Il trasporto della scomposizione per fattori coprimi in S si appoggia a C12-T1′ per raggruppamenti coprimi. La sua verifica resta in carico come in F6-ENC NOTE §3 ed è in open_questions Q3. Non è proposto come claim di questa sessione.

---

## 4. ENC-P0: intertwiner non autonomi. Nessun encoder indipendente dal tempo; gli encoder che esistono dipendono dal tempo (rev. 2)

*Revisione 2 (fix ENC-2, ENC-3, ENC-4, ENC-14, ENC-15).* La sintesi della prima versione ("le eccezioni cambiano il tempo") è **FALSA come scritta**: Avron–Herbst e tutta la classe V = β(t)x + γ(t) hanno un rappresentante puntuale più gauge con θ = id. La sintesi corretta è:

> per V(t, ·) − c(t) davvero non autonomo non esiste un encoder strutturato indipendente dal tempo con nucleo finito sul suo dominio 𝒴 (P0(b) in L², P0(b)^cl classica, P0(b)^loc localizzata). Un encoder strutturato indipendente dal tempo vede solo la regione in cui V(t, ·) − c(t) è autonomo. Gli encoder che esistono dipendono dal tempo: sono quadri d'interazione W(t) = U_0(θ(t))W(0)U_V(t)^{−1}. I rappresentanti puntuali più gauge esistono esattamente nella classe V = α(t)x² + β(t)x + γ(t) (Bluman–Shtelen 1996). In questa classe **si può scegliere θ = id se e solo se α ≡ 0**; per α ≢ 0 ogni rappresentante puntuale ha θ non affine.

*Post-Gate 8 (ENC2-4).* La rev. 2 scriveva "con θ ≠ id ⟺ α ≢ 0", riferito a un rappresentante qualsiasi. Così è **FALSO**: per V = 0 il rappresentante pseudo-conforme ha θ ≠ id (ENC-P0′-DIC).

Il cambio del tempo è una proprietà del rappresentante locale, non dell'encoder (P0′ è la forma normale di P0(a)).

**Ipotesi (H-P0).**
- ℋ è uno spazio di Hilbert e H_0 è autoaggiunto con dominio D := D(H_0).
- V ∈ C(ℝ; B(ℋ)) è continuo in norma, con valori autoaggiunti, e H(t) := H_0 + V(t).
- Esiste un propagatore unitario U_V(t, s), fortemente continuo in **entrambi** gli argomenti, con U_V(t, s)D ⊂ D, continuo in t nella norma del grafo su D, e con i∂_tU_V(t, s)ψ = H(t)U_V(t, s)ψ e i∂_sU_V(t, s)ψ = −U_V(t, s)H(s)ψ per ψ ∈ D.
- Questo è CON-FONTE (Dyson–Phillips: Pazy cap. 5, senza numero di teorema; il rimando a Reed–Simon II §X.12 non è verificato (CIT-AUDIT-8 §5)). Per H_0 = −∂² e V(t) moltiplicazione limitata e continua in norma è VAR-P11 di S8-VAR: (a)–(d) auditati, (e) CON-FONTE. Il teorema di Kato per domini comuni chiede in genere t ↦ H(t) fortemente C¹: la regolarità con V solo continuo in norma va controllata sul testo (rilievo girato a S8-VAR e CIT-AUDIT-8, fix ENC-15(b)).
- U_V(t) := U_V(t, 0) e U_0(t) := e^{−itH_0}.
- (H-P0) richiede V limitato: lente (V = ½x²) e Avron–Herbst (V = Fx) ne sono **fuori**. Per questi casi c'è P0′ su nucleo denso, più sotto (fix ENC-3). Dentro (H-P0) su ℝ la classe di Bluman–Shtelen si riduce a V = γ(t).

*Classe 𝔈 degli encoder ammessi:* W: ℝ → B(ℋ) fortemente continua, con W(t)D ⊂ D, e t ↦ W(t)ψ di classe C¹ per ψ ∈ D.

*Intrecciamento:*

   (INT) iW′(t)ψ = (H_0 + c(t))W(t)ψ − W(t)H(t)ψ per ogni ψ ∈ D,

con c ≡ 0 per (E2) stretta e c costante per (E2′) (NOTAZIONE v5).

**[ENC-P0(a)] Classificazione a tempo fissato (prova scritta; condizionale a (H-P0)).** Per W ∈ 𝔈 e c ≡ 0:

   W soddisfa (INT) ⟺ W manda soluzioni forti in soluzioni forti libere ⟺ W(t) = U_0(t)W(0)U_V(t)^{−1} per ogni t.

*Prova.*

(⇒) Sia u_0 ∈ D, u(t) := U_V(t)u_0 e g(t) := W(t)u(t). Si scrive

   [W(t + h)u(t + h) − W(t)u(t)]/h = W(t + h)(u(t + h) − u(t))/h + (W(t + h) − W(t))u(t)/h.

Il primo termine tende a W(t)u′(t): W è localmente limitata per Banach–Steinhaus ed è fortemente continua. Il secondo tende a W′(t)u(t) perché u(t) ∈ D. Quindi ig′ = H_0g con g(t) ∈ D. Inoltre d/dt[U_0(−t)g(t)] = 0, quindi g(t) = U_0(t)g(0), cioè W(t)U_V(t)u_0 = U_0(t)W(0)u_0 su D denso, e per limitatezza su ℋ.

(⇐) Sia M := W(0). Dell'appartenenza a 𝔈 si usa solo MD ⊂ D (fix ENC-15(a)). M è chiuso come mappa (D, ‖·‖_grafo) → (D, ‖·‖_grafo): se ψ_n → ψ e Mψ_n → φ nel grafo, allora Mψ_n → Mψ in ℋ, quindi φ = Mψ. Per il teorema del grafo chiuso M è limitato nel grafo. Per ψ ∈ D, φ(t) := U_V(0, t)ψ è C¹ in ℋ e continua nel grafo (continuità di U_V nel secondo argomento). Quindi U_0(t)Mφ(t) è derivabile, e il calcolo con φ′ = iU_V(0, t)H(t)ψ dà (INT). ∎

**[ENC-P0(b)] Nessun encoder indipendente dal tempo in L² (prova scritta; non usa il propagatore).** Siano ℋ = L²(J), H_0 autoaggiunto, V(t) = moltiplicazione per V(t, ·) ∈ L^∞(J), e c(t) scalare ammessa in (INT). Sia W ∈ B(ℋ), con WD ⊂ D, indipendente da t, con **dim ker W < ∞ su ℋ** ((E1) sul dominio dell'encoder, fix ENC-14). Allora V(t, ·) − V(s, ·) = c(t) − c(s) q.o. per ogni t, s.

*Prova.* Con W′ = 0, (INT) dà (H_0 + c(t))Wψ = WH(t)ψ per ψ ∈ D. Sottraendo t e s: W m ψ = 0 per ψ ∈ D, con m := V(t) − V(s) − (c(t) − c(s)). Siccome m è limitato, D è denso e ker W è chiuso, si ottiene W m = 0 su ℋ, cioè Ran(m) ⊂ ker W.

Se |{m ≠ 0}| > 0, esistono ε > 0 e infiniti insiemi disgiunti E_k ⊂ {|m| > ε} di misura **finita** e positiva. Le funzioni m·1_{E_k} ∈ Ran(m) sono linearmente indipendenti, contro dim ker W < ∞. ∎

*Portata (fix ENC-4).* In L²(J) con J limitato, H_0 autoaggiunto impone condizioni al bordo che l'encoder di Volterra di ENC-1 non rispetta, per cui W ∉ 𝔈. Quindi P0(b), letto alla lettera, **non** esclude un encoder di tipo ENC-1 per V(t, x).

C'è anche un argomento spettrale (KA P0, P4). In L²(J) un W ∈ 𝔈 con nucleo finito forza σ(H_V) − c ⊂ σ(H_0), a meno di un numero finito di autovalori: la classe è quasi vuota già per V autonomo. Per questo l'enunciato di riferimento è la versione classica che segue.

**[ENC-P0(b)^cl] Versione classica (prova scritta; testo del revisore, fix ENC-4; DA AUDITARE come claim nuovo).** Siano J un intervallo aperto, V ∈ C(I × J) e c ∈ C(I). Valga una delle due ipotesi seguenti (post-Gate 8, ENC2-1: nella rev. 2 W era definito su C^∞(J) ma veniva applicato a V(t, ·)f, che non è C^∞):
- (i) V(t, ·) ∈ C^∞(J) per ogni t, e W: C^∞(J) → C^∞(J) è lineare con dim ker W < ∞;
- (ii) W: D_W → 𝒟′(J) è lineare, con C(J)·C^∞_c(J) ⊂ D_W (per esempio D_W = C(J)) e dim ker W < ∞ **su tutto D_W**; l'identità seguente è intesa nel senso delle distribuzioni.

Si suppone che

   W(−∂_x² + V(t, ·))f = (−∂_x² + c(t))Wf per ogni t ∈ I e ogni f ∈ C^∞_c(J).

In particolare, se W è sequenzialmente continuo su C^∞(J), W intreccia i∂_t − L_{V(t)} e i∂_t − L_0 − c(t) su C^∞(I × J). La rev. 2 diceva "equivalentemente", e l'equivalenza sulle sole soluzioni non è provata (ENC2-1).

Allora V(t, x) − V(s, x) = c(t) − c(s) per ogni t, s, x.

*Prova.* Sottraendo le identità in t e in s si ha W(mf) = 0 per ogni f ∈ C^∞_c(J), con m := V(t, ·) − V(s, ·) − (c(t) − c(s)) continua. Se m(x*) ≠ 0, allora m ≠ 0 su un intervallo U ∋ x*. Si scelgono φ_1, φ_2, … ∈ C^∞_c(U) non nulle a supporti disgiunti: le mφ_k sono linearmente indipendenti e stanno in ker W, contro dim ker W < ∞. Le mφ_k stanno nel dominio di W: in (i) perché m ∈ C^∞(J), in (ii) perché mφ_k ∈ C(J)·C^∞_c(J) ⊂ D_W. Che W mandi o no C^∞_c in C^∞_c non conta. ∎

Copre l'encoder di Volterra W_q di ENC-1, che agisce su C(J) ed è iniettivo su C⁰: con (ii) per q continuo, con (i) per q ∈ C^∞. Conclusione esplicita: se W_q, indipendente dal tempo, soddisfa l'ipotesi, allora V(t, x) = q(x) + c(t) + costante (KA P5 di AUDIT rev. 2).

**[ENC-P0(b)^loc] Versione localizzata (prova scritta; fix ENC-14 ed ENC2-1; DA AUDITARE).**

*La versione della rev. 2 è FALSA come scritta* (ENC2-1). Chiedeva il nucleo finito solo su C^∞_c(U). Controesempio: X := C^∞_c(U), w continua e liscia su nessun intervallo, W(g + w·f) := g su X ⊕ w·X, V = t·w, c = 0. L'identità vale, ker W|_X = {0}, e V non è autonomo.

*Versione corretta.* Sia U ⊂ J aperto e valga una delle ipotesi di P0(b)^cl con U al posto di J: (i) V(t, ·) ∈ C^∞(U); oppure (ii) W: D_W → 𝒟′(U) lineare, con D_W ⊃ C(U)·C^∞_c(U) e dim ker W < ∞ **su tutto D_W**. Se l'identità di P0(b)^cl vale per ogni f ∈ C^∞_c(U), allora V(t, ·) − c(t) è autonomo su U.

*Prova.* Quella di P0(b)^cl, con le funzioni φ_k supportate in U. ∎

*Perché serve (KA P0, P6).* Siano V = V_0(x) + χ(x)cos t, con χ ≡ 0 su ω ⊂ J, e W := W_{V_0, ω} ∘ (restrizione a ω). W è esplicito, indipendente da t, e intreccia; il suo nucleo su 𝒴 è infinito, quindi non contraddice P0(b) né P0(b)^cl. Se però (E1) si leggesse "iniettivo sulle soluzioni", W lo sarebbe non appena vale la continuazione unica laterale da I × ω a I × J. Domanda aperta a S8-VAR: VAR-L1 la fornisce? In quella lettura esisterebbe un encoder indipendente dal tempo per un V non autonomo.

Da qui la frase per G★″: **"un encoder strutturato indipendente dal tempo vede solo la regione in cui V(t, ·) − c(t) è autonomo"**.

*Sotto-caso aperto (fix ENC-15(d)).* "W commuta con ∂_t" è più largo di "W non dipende da t e agisce in x" (per esempio, le convoluzioni in t). Con c costante si chiude con l'invarianza per traslazioni temporali τ_h: Wτ_h = τ_hW dà W(V − V(· + h, ·))ψ = 0. Con c(t) non costante e W non locale in t resta **aperto** (open_questions Q11).

**[ENC-P0′] Forma normale, su nucleo denso (prova scritta; versione su nucleo denso DA AUDITARE, fix ENC-2, ENC-3).** Siano:
- ℋ uno spazio di Hilbert e H_0 autoaggiunto;
- U_V(t), t ∈ I, una famiglia di unitari con U_V(0) = I;
- W(t) ∈ B(ℋ);
- I un intervallo con 0 ∈ I (ENC2-2: serve per θ(0) = 0 e U_V(0) = I);
- θ ∈ C¹(I) con θ′ > 0 e θ(0) = 0;
- D_0 ⊂ ℋ un sottospazio denso.

Supponiamo che per ogni u_0 ∈ D_0 la funzione τ ↦ v(τ) := W(θ^{−1}(τ))U_V(θ^{−1}(τ))u_0 sia C¹ da θ(I) in ℋ, a valori in D(H_0), con iv′ = H_0v. Allora:

   W(t) = U_0(θ(t)) W(0) U_V(t)^{−1}, t ∈ I.

In particolare W_id(t) := U_0(t − θ(t))W(t) = U_0(t)W(0)U_V(t)^{−1}. Ogni encoder di P0′ è quindi equivalente a uno con θ = id, e θ **non** è un invariante dell'encoder.

*Prova.* d/dτ[U_0(−τ)v(τ)] = U_0(−τ)(v′ + iH_0v) = 0, per la regola del prodotto (v è C¹ in ℋ a valori in D(H_0) e U_0 è uniformemente limitato). Quindi v(τ) = U_0(τ)v(0) con v(0) = W(0)u_0. Si conclude per densità di D_0 e limitatezza di W(t) e U_V(t). ∎

La prova non usa (H-P0) né la classe 𝔈: è questo il senso della restrizione a 𝒮(ℝ) per le eccezioni.

*Esempi su D_0 = 𝒮(ℝ) (identità classiche, verificate direttamente).* Si usa la normalizzazione H = −½∂² + ½x².
- **Lente** (Niederer): H_0 = −½∂², θ = tan, W(0) = I, I = (−π/2, π/2). Per u_0 ∈ 𝒮, U_osc(t)u_0 ∈ 𝒮 (sviluppo di Hermite con coefficienti a decrescita rapida, C¹ in t a valori in 𝒮). La mappa puntuale u ↦ v(tan t, y) := (cos t)^{1/2}e^{iy² sin t cos t/2}u(t, y cos t) conserva 𝒮 e dà una soluzione libera C¹ in τ = tan t (calcolo: `enc_algebra` P0′, `enc_s8b` §6, NS3 dell'audit). Quindi P0′ si applica con D_0 = 𝒮, e dà W(t)^{−1} = U_osc(t)U_0(tan t)^{−1}.
- **Avron–Herbst** (V = Fx, normalizzazione del progetto H = −∂² + Fx): θ = id, u = e^{−iFtx − iF²t³/3}v(t, x + Ft²) (formula esplicita di Fourier, ENC-A9(b2)). È un'istanza di P0′ con θ = id e D_0 = 𝒮 (ENC2-3; non di P0(a), che chiede (H-P0) e V limitato), **senza** cambio del tempo. Normalizzazioni: la lente usa H = −½∂² + ½x²; Avron–Herbst e la classe seguente usano quella del progetto, H = −∂² + V.
- **Classe V = β(t)x + γ(t)** (KA P0, P1; `enc_recep` 1/1): u = e^{−iB(t)x − iΦ(t) − i∫γ}v(t, x − Ξ(t)), con B′ = β, Ξ′ = −2B, Φ′ = B². Anche qui θ = id.

Le identità valgono anche in L² (ENC2-3). Sia H essenzialmente autoaggiunto su 𝒮 e sia U(t) una famiglia di unitari con U(t)u_0 ∈ 𝒮, C¹ in t, e iU′(t)u_0 = HU(t)u_0 per u_0 ∈ 𝒮. Allora d/dt[e^{itH}U(t)u_0] = 0, quindi U(t) = e^{−itH} su 𝒮 e, per densità, su L². L'essenziale autoaggiuntezza su 𝒮 di oscillatore e campo costante è CON-FONTE: Reed–Simon II Thm X.38 (criterio di Faris–Lavine, Commun. Math. Phys. 35 (1974) 39–48, DOI 10.1007/BF01646453). Mehler serve per la convergenza al dato: CON-FONTE, DLMF 18.18.28 e Mehler 1866 (J. reine angew. Math. 66, 161–176), già in VAR-T10.

**[ENC-P0′-DIC] Dicotomia dei rappresentanti puntuali (post-Gate 8: forma esistenziale, fix ENC2-4; prova scritta, DA AUDITARE; fonte: KA P0 P1, sistema rifatto a mano dal revisore; classificazione di Bluman–Shtelen, J. Phys. A 29(15) (1996) 4473–4480, DOI 10.1088/0305-4470/29/15/018, §2, CON-FONTE verificata).** Sia V = α(t)x² + β(t)x + γ(t) reale. Nell'ansatz puntuale più gauge (chirp a(t), dilatazione ρ(t) > 0, traslazione, fase, tempo T(t) con T(0) = 0) le equazioni sono T′ = 1/ρ², ρ′ = 4aρ, a′ + 4a² = −α. Allora:
- **esiste un rappresentante puntuale più gauge con θ = T = id se e solo se α ≡ 0**; equivalentemente, ogni rappresentante puntuale più gauge ha θ ≠ id se e solo se α ≢ 0;
- se α ≢ 0, in nessun rappresentante θ è affine.

*Prova.* (⇐) Con α ≡ 0 si sceglie a ≡ 0, ρ ≡ 1, T = id. (⇒) Se T è affine, T′ = 1/ρ² è costante, quindi ρ è costante; da ρ′ = 4aρ segue a ≡ 0, e da a′ + 4a² = −α segue α ≡ 0 (`enc_g8` 1/1). ∎

*La forma della rev. 2 è FALSA come scritta.* Diceva "θ = T = id ⟺ ρ ≡ 1 ⟺ a ≡ 0 ⟺ α ≡ 0" per un rappresentante qualsiasi. Controesempio (DIC3): per V = 0 il rappresentante pseudo-conforme a = a_0/(1 + 4a_0t), ρ = 1 + 4a_0t, θ(t) = t/(1 + 4a_0t), con a_0 ≠ 0, risolve il sistema con α ≡ 0 e ha θ ≠ id. La mappa u = ρ^{−1/2}e^{iax²}v(θ(t), x/ρ) manda soluzioni libere in soluzioni libere (`enc_g8` 3/3). Inoltre a ≡ 0 implica solo ρ costante, non ρ ≡ 1. Il cambio del tempo serve per la parte quadratica nel senso esistenziale: si può evitare se e solo se α ≡ 0.

Con trasformazioni non locali ogni V ha il proprio quadro d'interazione (P0(a)). La restrizione a V quadratico riguarda **solo** i rappresentanti puntuali (fix ENC-15(c)).

**[POLE-N] Strada POLE: esito negativo per Schrödinger (rev.; prova scritta; versione classica DA AUDITARE, fix ENC-4).**

*Versione hilbertiana.* In (H-P0), sia W(t) ∈ 𝔈 con nucleo finito e W(t)L_{V(t)} = (L_0 + c)W(t) per ogni t (intertwiner **istantaneo**). Se W è un encoder per i u_t = L_{V(t)}u, allora (INT) dà iW′ = 0, quindi W è costante e P0(b) dà V autonomo modulo c(t). La classe non è vuota: per potenziali limitati senza riflessione gli operatori d'onda Ω_±^* sono limitati, hanno nucleo finito (gli stati legati) e intrecciano istantaneamente (KA P0, P7).

*Versione classica (POLE-N^cl).* Sia W(t) = Σ_j w_j(t, x)∂_x^j, con coefficienti C^∞ in (t, x) fuori dall'insieme dei poli e W(t)L_{V(t)} = (L_0 + c)W(t) per ogni t. Se W intreccia anche i∂_t − L_{V(t)} con i∂_t − L_0 − c, allora ∂_tW = 0 come operatore su C^∞, cioè i coefficienti non dipendono da t. Si fissa un rettangolo [s, t] × U contenuto nel complementare dei poli (ENC2-5). Un intervallo privo di poli "a entrambi i tempi" non basta: con un polo in x = z(t) = t, U = (½, 3/2) è libero ai tempi 0 e 2, ma il polo lo attraversa a t = 1 (POLE3; `enc_g8` 1/1). Su [s, t] × U si ha ∂_t w_j = 0, quindi w_j(t, ·) = w_j(s, ·) su U. Si applica P0(b)^cl con dim ker W = n: vale perché w_n è una costante non nulla (ENC-K1′(i)) e n ≥ 1. Inoltre V è C^∞ fuori dai poli, come si legge dai coefficienti dell'identità istantanea, quindi vale l'ipotesi (i) di ENC2-1. Ne segue che V è autonomo modulo c su U. In alternativa si enuncia la tesi in un intorno rettangolare di ogni punto regolare e si concatena. Questo copre i potenziali razionali di Adler–Moser con poli reali (non in L^∞) e gli intertwiner di Darboux differenziali (non limitati su L²), che la versione hilbertiana non copriva.

*Lettura.* Gli intertwiner istantanei di Darboux funzionano per il **flusso di Lax** (ψ_t = B_3ψ nella gerarchia KdV), non per Schrödinger nel suo tempo. Per B2 la strada POLE si richiude.

P0(b), P0(b)^cl, P0(b)^loc e POLE-N non usano il propagatore, quindi non ereditano la dipendenza CON-FONTE di (H-P0). P0(a) e la versione hilbertiana di POLE-N restano condizionali a (H-P0) (fix ENC-15(b)).

---

## 5. ENC-N1: encoder cieco e identificabilità (rev. 2, fix ENC-5, ENC-13)

**Quadro (rev.).** Tutti gli oggetti sono relativi a una **famiglia fissata** di encoder 𝒲 = {W_V} (fix ENC-5(c)). L'esistenza dell'encoder cieco è una proprietà della coppia (classe, famiglia), non della sola classe.

- 𝒟 è lo spazio lineare dei dati (funzioni su Ω), con l'equivalenza di gauge del modello di dato: DM3, u ~ u′ ⟺ u = u′; DM-φ, u ~ u′ ⟺ u′ = e^{iθ(t)}u con θ reale C¹.
- 𝒱 è una classe di potenziali, e per V ∈ 𝒱, 𝒮_V ⊂ 𝒟 è lo **spazio lineare** delle soluzioni. Non è saturato per ~: con DM-φ e^{iθ}u non è soluzione se θ non è costante.
- [𝒮_V] := {[u] : u ∈ 𝒮_V} ⊂ 𝒟/~.
- W_V agisce solo in x, è lineare, iniettivo su 𝒮_V e verifica W_V L_V = (L_0 + c_V)W_V. Quindi W_V(e^{iθ(t)}u) = e^{iθ(t)}W_V u. La normalizzazione N_V(v) := e^{ic_V t}v manda W_V(𝒮_V) in soluzioni libere.
- Uscite: 𝒪 := 𝒟_0/≈, dove 𝒟_0 sono le soluzioni libere; v ≈ v′ ⟺ v = v′ (DM3), v′ = e^{iθ(t)}v con θ arbitraria (DM-φ).
- *Encoder cieco per (𝒱, 𝒲):* una mappa E: ∪_V[𝒮_V] → 𝒪 con E([u]) = [N_V W_V u′] per ogni V e ogni u′ ∈ 𝒮_V con u′ ~ u.
- *Identificabilità modulo ~:* u ∈ 𝒮_V, u′ ∈ 𝒮_{V′}, u ~ u′, u ≠ 0 ⇒ V = V′.
- *(C) coerenza:* u ∈ 𝒮_V, u′ ∈ 𝒮_{V′}, u ~ u′ ⇒ [N_V W_V u] = [N_{V′}W_{V′}u′].
- *(S) separazione:* u ∈ 𝒮_V, u′ ∈ 𝒮_{V′}, u ~ u′ ≠ 0, V ≠ V′ ⇒ [N_V W_V u] ≠ [N_{V′}W_{V′}u′].

All'interno di un solo V la definizione è coerente. Se u, u′ ∈ 𝒮_V, u ~ u′ ≠ 0 con DM-φ, allora u′ = e^{iθ}u è soluzione solo se θ′u = 0, cioè θ è costante, e W_V commuta con la fase costante.

**[ENC-N1 (F6)] FALSO come scritto.** L'enunciato era: "esiste un encoder cieco ⟺ Φ(V, v) := W_V^{−1}v è iniettiva su 𝒱 × 𝒮". Il controesempio scritto nella prima versione (Φ(V, 0) = 0 per ogni V) è banale (fix ENC-5(b)). La versione caritatevole F6* — "Φ iniettiva su 𝒱 × (𝒮 ∖ {0}) modulo ~" — equivale all'identificabilità congiunta. Nell'istanza V(x) con DM3 F6* è **vera**. Come equivalenza è falsa **per il testimone (iv)** qui sotto, che è il controesempio di riferimento per il LEDGER.

Φ è definita su tutto 𝒱 × 𝒮_0 solo se W_V è suriettivo (vero per Volterra, non in generale), e il confronto va scritto Φ(V, v) ~ Φ(V′, v′) (fix ENC-13(d)).

**[ENC-N1′] Lemma di riduzione (prova scritta; non è un teorema, fix ENC-5(e)).** Per una famiglia fissata 𝒲:
- (i) Un encoder cieco esiste ⟺ vale (C).
- (ii) L'identificabilità modulo ~ implica (C), quindi l'encoder cieco esiste.
- (iii) (C) ∧ (S) ⟺ identificabilità. Vale **per definizione**: (S) è equivalente alla tesi data (C), e nessuna istanza nota ha (S) non vacua (open_questions Q4). La forma "encoder cieco ⟺ identificabilità congiunta" chiesta dal roster vale **solo in forma condizionale, con un'ipotesi equivalente alla tesi**.
- (iv) *Testimone: cieco senza identificabilità.* Si prendono DM-φ, 𝒱 = {q_0 + c : c ∈ ℝ} con q_0 ∈ C¹(J) reale, e 𝒲: W_{q_0 + c} := W_{q̂}, encoder di Volterra di q̂ := q_0 − q_0(x_0), con c_V = q_0(x_0) + c. Siano u ∈ 𝒮_{q_0} e u′ := e^{−ict}u ∈ 𝒮_{q_0 + c}, così u′ ~ u. Allora N_{V′}W_{q̂}u′ = e^{i(q_0(x_0)+c)t}e^{−ict}W_{q̂}u ≈ N_V W_{q̂}u. Dunque (C) vale e l'encoder cieco esiste, ma V è identificato solo modulo costanti.
- (v) *Dipendenza dalla famiglia.* Si prende la stessa classe con la **famiglia stretta** (W_{q_0 + c} = encoder di Volterra di q_0 + c normalizzato in x_0, c_V = 0). Per q_0 = 0, u = e^{−iλt}cos √λ(x − x_0) ∈ 𝒮_0 e u′ = e^{−ict}u ∈ 𝒮_c. Si ha W_0u = u e W_cu′ = e^{−i(λ+c)t}cos √(λ + c)(x − x_0), uscite non equivalenti modulo fasi. Quindi (C) fallisce e l'encoder cieco **non** esiste per questa famiglia (`enc_recep` 1/1; è coerente con ENC-1(6)).

*Prova.*
- (i) Se E esiste, (C) è la sua buona definizione. Viceversa, (C) dice che [N_V W_V u′] non dipende dalla scelta di (V, u′).
- (ii) Se u ~ u′ ≠ 0, allora V = V′, e per l'osservazione sul singolo V si ha u′ = e^{iθ_0}u con θ_0 costante, da cui [N_V W_V u′] = [N_V W_V u]. Se u ~ 0, allora u = u′ = 0.
- (iii) ⇐ è (ii). ⇒: se esistessero V ≠ V′ con u ~ u′ ≠ 0, (S) contraddirebbe (C).
- (iv) Si verifica W_{q̂}L_{q_0 + c} = (L_0 + q_0(x_0) + c)W_{q̂}, e W_{q̂} commuta con le fasi in t.
- (v) W_c manda l'autofunzione cos √λ(x − x_0) di L_c (autovalore λ + c) nell'autofunzione di L_0 con lo stesso autovalore e gli stessi dati di Cauchy in x_0. ∎

*Lettura di gauge (fix ENC-5(f), KA N1 P6).* Con DM-φ, per ogni dato regolare non nullo w = e^{iθ(t)}u, si ha (iw_t + w_xx)/w = q(x) − θ′(t): q è identificato modulo costanti. La formulazione corretta per G★″ e per il roster è:

> **encoder cieco ⟺ identificabilità modulo il gruppo di gauge del modello di dato**, per una famiglia fissata che rispetta il gauge.

In questa forma (iv) non è più un controesempio, e l'equivalenza resta tautologica salvo un'ipotesi di separazione modulo gauge. Questa formula sostituisce la citazione di VAR-P4(a), che riguarda gli stati stazionari.

*Istanze (rev., fix ENC-5(d), ENC-13).*
- **V(x) ∈ C¹, DM3, famiglia di Volterra stretta.** u ≢ 0 implica V = V′ q.o. per VAR-T1(b) nella forma auditata (soluzioni forti (SF), VAR-1, con la continuazione laterale VAR-L1). Quindi 𝒮_V ∩ 𝒮_{V′} = {0} e (S) vale a vuoto. L'encoder cieco esiste per (ii): q = (iu_t + u_xx)/u nei punti u ≠ 0, poi il Goursat (G). Non si afferma stabilità. Onda e calore sono fuori da questo quadro, che è (E2′) con i∂_t.
- **V(t, x).** Domanda **vuota** per encoder strutturati indipendenti dal tempo (P0(b), P0(b)^cl, P0(b)^loc, salvo la regione autonoma); **aperta** per W(t) strutturati.
- **Schrödinger magnetico in n ≥ 2.** **Aperto.** La non identificabilità di (A, V) (SYS-N3) è di gauge e non esclude un encoder cieco modulo gauge; inoltre n ≥ 2 è fuori dal quadro unidimensionale.

*Frase per G★″:* "encoder cieco ⟺ coerenza (C) per una famiglia fissata; ⟸ identificabilità; l'equivalenza piena vale solo sotto (S), ipotesi equivalente alla tesi; modulo il gauge del modello di dato, l'esempio DM-φ rientra". ENC-N2(a) di F6-ENC coincide con VAR-P4 ed è contata una volta sola (fix F9).

---

## 6. Tabella degli encoder (fix F7) ed ENC-K1

**[ENC-K1′] Proposizione: la direzione ⇒, locale (prova scritta; SymPy `enc_algebra` K1′ 5/5, `enc_s8b` passo generico 2/2).** Siano J un intervallo aperto, q ∈ C^∞(J; ℂ), c ∈ ℂ e W = Σ_{j=0}^{n}w_j∂^j (n ≥ 1, w_j ∈ C^∞(J), w_n ≢ 0) con W L_q = (L_0 + c)W. Allora:
- (i) w_n è costante;
- (ii) N := ker W ha dimensione n ed è invariante per L_q;
- (iii) esiste un insieme chiuso e numerabile Z ⊂ J (quindi a interno vuoto; non si afferma che sia discreto, fix ENC-9) tale che su ogni componente di J ∖ Z si ha W = w_n A_n ⋯ A_1, con A_k = ∂ − ψ_k′/ψ_k. Qui ψ_k è un'autofunzione (semi complessi ammessi) di L_{q_{k−1}} con autovalore λ_k, e q_0 := q, q_k := q_{k−1} − 2(ψ_k′/ψ_k)′, q_n ≡ c. Quindi L_q è ottenuto da L_0 + c con n trasformazioni di Darboux, lette all'indietro.

Viceversa, ogni catena di Darboux di questo tipo dà un intertwiner differenziale (Crum). Dunque, **localmente**: esiste un W differenziale con W L_q = (L_0 + c)W ⟺ q si ottiene da c con una catena finita di Darboux.

*Prova.*
- (i) Il coefficiente di ∂^{n+1} in W L_q − (L_0 + c)W è 2w_n′ (come in ENC-K0).
- (ii) W ha ordine n con coefficiente di testa costante non nullo, quindi dim ker W = n su J. Se Wf = 0, allora W L_q f = (L_0 + c)Wf = 0.
- (iii) Induzione su n. Si sceglie un autovettore ψ_1 di L_q|_N, che esiste perché ℂ è algebricamente chiuso, con autovalore λ_1. Su J_1 := J ∖ ψ_1^{−1}(0) (gli zeri di una soluzione non nulla di un'ODE lineare del secondo ordine sono isolati) si pone g := ψ_1′/ψ_1, A_1 := ∂ − g, A_1^♯ := −∂ − g. Si verificano tre identità (SymPy):
  - L_q − λ_1 = A_1^♯A_1, perché g′ + g² = ψ_1″/ψ_1 = q − λ_1;
  - A_1A_1^♯ = L_{q_1} − λ_1 con q_1 = q − 2g′;
  - quindi A_1L_q = L_{q_1}A_1.

  W(ψ_1) = 0, e la divisione euclidea a destra per l'operatore monico A_1 dà W = W_1A_1 + r, con r funzione e rψ_1 = 0, quindi r = 0. Da W_1A_1L_q = (L_0 + c)W_1A_1 e A_1L_q = L_{q_1}A_1 segue (W_1L_{q_1} − (L_0 + c)W_1)A_1 = 0. A_1 è suriettivo su C^∞ di ogni sottointervallo (ODE del primo ordine), quindi W_1L_{q_1} = (L_0 + c)W_1, con W_1 di ordine n − 1.

  Per n = 1 si arriva a W_0 = w_0 funzione con w_0L_{q_1} = (L_0 + c)w_0. Il coefficiente di ∂ dà w_0 costante, e quello di ∂^0 dà q_1 = c. Z := Z_1 ∪ … ∪ Z_n, dove Z_k sono gli zeri di ψ_k in J ∖ (Z_1 ∪ … ∪ Z_{k−1}). Ogni Z_k è discreto nel suo aperto, quindi Z è numerabile. Z è chiuso perché Z_1 ∪ … ∪ Z_k contiene la chiusura di Z_k. Il nucleo ker W_1 = A_1(N) è globale su J_1 (dimensione n − 1 su ogni componente), quindi ψ_2 si sceglie globalmente. Non è escluso che gli zeri di ψ_k si accumulino su Z_{k−1}, dove q_{k−1} ha poli doppi 2/(x − z)² + (liscio). Discretezza: vera se q è analitico reale, nel caso generale aperta (open_questions Q7). ∎

*Nota sulla priorità (post-Gate 8, CIT-AUDIT-8 §5).* La fattorizzazione di un intertwiner in passi di Darboux del primo ordine è il tema di Andrianov–Sokolov, Nucl. Phys. B 660(1–2) (2003) 25–50, DOI 10.1016/S0550-3213(03)00232-3 (hep-th/0301062), e di Sokolov, J. Math. Sci. 151(2) (2008) 2924–2936, DOI 10.1007/s10958-008-9009-3 (arXiv:0903.2835). Il verso inverso è Crum, Q. J. Math. 6(1) (1955) 121–127. **Rischio di novità alto, confermato: ENC-K1′ non è un risultato nuovo del progetto.** Si registra come prova autonoma di un fatto noto.

**[ENC-K1] Declassato a CON-FONTE (da verificare).** La caratterizzazione **globale ed esplicita** della classe è: "V razionale con V → 0 all'∞; esiste W differenziale con W L_V = L_0 W ⟺ V è una trasformata di Darboux iterata di 0 ⟺ V = −2(log τ)″ con τ polinomio di Adler–Moser". È **Duistermaat–Grünbaum 1986** (CMP 103, 177–240), con Wilson 1993 per la grassmanniana adelica bispettrale (*Bispectral commutative ordinary differential operators*, J. reine angew. Math. 442, 177–204, DOI 10.1515/crll.1993.442.177; CIT-AUDIT-8 §5). Wilson 1998 è un rimando facoltativo. D–G: DOI 10.1007/BF01206937. **Vale solo con V → 0 all'infinito.** Senza decadimento l'analogo "monodromia banale ⇒ Darboux di 0" è falso: Oblomkov (crescita quadratica, Darboux dell'oscillatore) e Gibbons–Veselov (sestica). I solitoni senza riflessione (−ℓ(ℓ + 1)sech², non razionali in x) stanno nella classe di ENC-K1′ (Crum, VAR-P8(c)), non in quella di D–G. Le due classi si coprono a vicenda solo attraverso ENC-K1′, che è locale e non parla di razionalità. **Niente "decidibile via Kovacic"**: Kovacic decide a λ fissato (DEVIL-6 O7.2).

**Tabella unica degli encoder (aggiorna SYNTHESIS-2 §3).**

| tipo di W | dove esiste | stato | dove |
|---|---|---|---|
| (E2′) gauge costante, W = I | q ≡ c | prova scritta (ENC-K0: con c = 0 non esiste W differenziale) | §1 |
| integrale di Volterra simmetrico (Povzner–Levitan–Marchenko) | ogni q ∈ C¹(J; ℂ), J = [x_0 − a, x_0 + a]; dipende da x_0; unico normalizzando i dati di Cauchy (ENC-U1) | **prova scritta** (ENC-1) + CON-FONTE Marchenko cap. 1 (senza numero di teorema); q ∈ L¹ solo CON-FONTE | §2 |
| differenziale (Darboux/Crum) **modulo costanti** | localmente ⟺ catena di Darboux da c (ENC-K1′); solitoni senza riflessione e Pöschl–Teller inclusi | ENC-K1′ prova scritta, nessuna novità (Andrianov–Sokolov 2003, Sokolov 2008); classe globale razionale: **CON-FONTE da verificare, solo V → 0** (Duistermaat–Grünbaum 1986) | §6 |
| puntuale + gauge, **dipendente dal tempo** (rev. 2) | V(t, x) = α(t)x² + β(t)x + γ(t) reale; si può scegliere θ = id se e solo se α ≡ 0 (Avron–Herbst, V = β(t)x + γ(t)); per α ≢ 0 ogni rappresentante ha θ non affine (lente, Niederer); forma normale ENC-P0′ su 𝒮(ℝ) | CON-FONTE verificata (Bluman–Shtelen 1996 §2); dicotomia esistenziale DA AUDITARE (post-Gate 8, ENC2-4, O2); su Ω limitato: NS-EQUIV-Ω (§8) | §4, §8 |
| non locale, a energia fissata (Born/Lippmann–Schwinger, Faddeev) | ogni q, ma a λ fissato; su intervallo limitato la serie converge sempre | prova scritta (FAD-1, §9) | §9 |
| omogeneizzazione / gamblets | V oscillante o ruvido (approssimato) | parcheggiato come approssimazione; gamblets = strumento (S) per scala (GAM-O1) | §9 |
| Foldy–Wouthuysen (Dirac) | Dirac libero esatto (moltiplicatore non locale); con V solo asintotico | FW-1 prova scritta (libero), con V CON-FONTE | §9 |
| operatori d'onda Ω_±^* | tutto lo spazio, t → ∞ | parcheggiato (fuori dal modello Ω limitato) | F6-ENC §7 |

---

## 7. E_int A9 per Schrödinger con potenziale (non E^conj)

**Definizione (NOTAZIONE v3, A9).** Termini: T_1 := −iH_0 (cinetico) e T_2 := −iV (potenziale), con flussi S_1(t) = U_0(t) e S_2(t) = e^{−itV}. Allora

   E^add(t) := U(t) − U_0(t) − e^{−itV} + I, E^mult(t) := U(t) − U_0(t)e^{−itV} (prima il flusso di V),

con U(t) = e^{−it(H_0 + V)}. Il difetto di coniugazione E^conj = W^{−1}S_0W − S_0S_V di F6-ENC è un altro oggetto e non entra qui (fix F6).

**[ENC-A9(a)] Stima, termine principale, annullamento (prova scritta; SymPy `enc_s8b` 2/2 sul toro, `eint_closed` sviluppo formale 2/2).** Sia V ∈ W^{2,∞}(ℝ) reale (risp. 2π-periodica su 𝕋). Allora, per f ∈ H¹ e t ≥ 0:

   ‖E^mult(t)f‖ ≤ (t²/2)(‖V″‖_∞‖f‖ + 2‖V′‖_∞‖f′‖) + (2t³/3)‖V′‖_∞²‖f‖;

per f ∈ H²:

   E^mult(t)f = (t²/2)[H_0, V]f + o(t²), [H_0, V] = −V″ − 2V′∂;

e infine E^mult ≡ 0 vicino a t = 0 ⟺ V è costante.

*Prova.* Per f ∈ H² si pone 𝒮(s) := U_0(s)e^{−isV}. Si ha e^{−isV}f ∈ H², continua in H² e C¹ in L² (V ∈ W^{2,∞}). Per il lemma del prodotto di §4, s ↦ U(t − s)𝒮(s)f è C¹ con derivata iU(t − s)[(H_0 + V)𝒮(s) − U_0(s)(H_0 + V)e^{−isV}]f = iU(t − s)[V, U_0(s)]e^{−isV}f: i due termini con H_0 si cancellano perché U_0 commuta con H_0. Integrando su [0, t]:

   E^mult(t)f = −i∫_0^t U(t − s)[V, U_0(s)]e^{−isV}f ds. (D1)

Allo stesso modo, derivando r ↦ U_0(r)VU_0(s − r)g per g ∈ H² (V manda H² in H²):

   [V, U_0(s)]g = i∫_0^s U_0(r)[H_0, V]U_0(s − r)g dr. (D2)

Siccome ‖[H_0, V]h‖ ≤ ‖V″‖‖h‖ + 2‖V′‖‖h′‖, U_0 è unitario e commuta con ∂, e ‖(e^{−isV}f)′‖ ≤ ‖f′‖ + s‖V′‖‖f‖, si ottiene

   ‖E^mult(t)f‖ ≤ ∫_0^t s[‖V″‖‖f‖ + 2‖V′‖(‖f′‖ + s‖V′‖‖f‖)]ds,

cioè la stima. Su H¹ si conclude per densità, perché entrambi i membri sono continui in H¹.

Termine principale: (D1)+(D2) danno E^mult(t)f = ∫_0^t∫_0^s U(t − s)U_0(r)[H_0, V]U_0(s − r)e^{−isV}f dr ds. L'integrando tende a [H_0, V]f in L² per t → 0: i gruppi sono fortemente continui e U_0(s − r)e^{−isV}f → f in H¹. Quindi E^mult(t)f/t² → ½[H_0, V]f.

Annullamento: se E^mult ≡ 0, allora [H_0, V]f = 0 per ogni f ∈ H². Con f ≡ 1 su un intervallo si ottiene V″ = 0 lì; poi, con f′ ≠ 0, V′ = 0. Quindi V è costante. Viceversa, per V costante e^{−itV} è uno scalare. ∎

*Commenti.*
- La stima richiede ‖f′‖: in norma operatoriale su L² l'errore non è piccolo. Per V = Fx, ‖E^mult(t)‖_{L²→L²} = 2 per ogni t ≠ 0 (b2).
- Rispetto al PLAN la costante del termine t³ scende da 1 a 2/3. **La costante 2/3 è ottimale** (rev. 2, revisore A9a). Per V = Fx la stima corretta di (b2) coincide con questa (V″ = 0, ‖V′‖ = |F|). Per f gaussiane di larghezza ~ 1/t² e t → 0 il rapporto fra i due membri tende a 1 (`enc_recep`: 0.9937, 0.9979, 0.9994).
- **E^add non si annulla per V costante**: per V ≡ c si ha E^add = (e^{−ict} − 1)(U_0(t) − I), con sviluppo E^add = −(t²/2){H_0, V} + O(t³) (`eint_closed`). Per questo il quadro che misura l'interazione vera fra cinetico e potenziale è E^mult, e il criterio "E^mult ≡ 0 ⟺ V costante" è quello giusto.

**[ENC-A9(b)] Forme chiuse.**
- (b1) **V ≡ c.** E^mult = 0 ed E^add = (e^{−ict} − 1)(U_0 − I). Prova: diretta.
- (b2) **V = Fx su L²(ℝ)** (prova scritta; SymPy `eint_closed` 6/6, `enc_s8b` 2/2). In questo caso

   U(t) = e^{−iF²t³/12} e^{−itV/2}U_0(t)e^{−itV/2} (Strang esatto a meno di una fase),
   E^mult(t) = e^{−itV/2}U_0(t)[e^{−iF²t³/12} − e^{iFt²p − iF²t³/4}]e^{−itV/2}, p = −i∂.

   Quindi ‖E^mult(t)f‖ = ‖(1 − e^{i(Ft²p − F²t³/6)})e^{−itV/2}f‖ = ‖(1 − e^{i(Ft²p − 2F²t³/3)})f‖ ≤ |F|t²‖f′‖ + (2/3)F²t³‖f‖, e ‖E^mult(t)‖_{L²→L²} = 2.

   *Correzione (fix ENC-1, CRITICAL locale).* La prima versione scriveva "≤ Ft²‖f′‖ + (F²t³/6)‖f‖", che è **falso**: dimenticava che e^{−itFx/2} trasla p di Ft/2, così che il moltiplicatore va valutato in p − Ft/2. Controesempio: F = t = 1, f gaussiana di larghezza 25, ‖E^mult f‖ = 0.6549 contro 0.1950 (`enc_recep` 3/3, A9b2 dell'audit). La forma corretta dà 0.6950.

   *Prova.* In trasformata di Fourier (f̂(p) = ∫f e^{−ipx}) x = i∂_p, quindi l'equazione diventa ∂_tû − F∂_pû = −ip²û. Il metodo delle caratteristiche (p(s) = p + F(t − s)) dà, per û_0 ∈ 𝒮, l'unica soluzione classica

   û(t, p) = û_0(p + Ft)exp(−i(p²t + pFt² + F²t³/3)).

   Il secondo membro: e^{−itFx/2} trasla p ↦ p + Ft/2 (perché (e^{iax}f)^ = f̂(p − a)), quindi e^{−itV/2}U_0e^{−itV/2} dà e^{−it(p + Ft/2)²}f̂(p + Ft) = e^{−i(p²t + pFt² + F²t³/4)}f̂(p + Ft). Il confronto fissa la fase F²t³/12. Il secondo addendo di E^mult è U_0e^{−itV} riscritto con e^{itV/2}U_0e^{−itV/2} = e^{−it(p − Ft/2)²}, controllo simbolico sul nucleo. La norma è il sup del moltiplicatore |1 − e^{iθ(p)}|, che vale 2 perché θ è affine non costante in p. Forma di Avron–Herbst equivalente: U(t)f(x) = e^{−itFx − iF²t³/3}(U_0(t)f)(x + Ft²). ∎
- (b3) **V = x² (H = −∂² + x²).** Per 0 < |t| < π/2:

   U(t) = e^{−i tan(t)x²/2}U_0(sin(2t)/2)e^{−i tan(t)x²/2}, quindi E^mult(t) = e^{−i tan t x²/2}U_0(sin 2t/2)e^{−i tan t x²/2} − U_0(t)e^{−itx²}.

   Prova: uguaglianza dei nuclei con quello di Mehler (`eint_closed` 4/4; il nucleo di Mehler risolve l'equazione, e la sua convergenza a δ è CON-FONTE). **Fuso in VAR-T10 di S8-VAR** (chirp·libero·chirp ⟺ sin 2t ≠ 0, nessuna rottura a cos t = 0): contato una volta. *Stato (post-Gate 8, O16):* CON-FONTE + V-ex, ereditato da VAR-T10(3)(iii). Il nucleo di Mehler è CON-FONTE: DLMF 18.18.28; Mehler 1866, J. reine angew. Math. 66, 161–176.
- (b4) **Pöschl–Teller modificato (iperbolico) q = −2sech²x** (Pöschl–Teller, Z. Phys. 83 (1933) 143–151; nome corretto da CIT-AUDIT-8 §5) (prova scritta; SymPy `eint_closed` 7/7, `enc_s8b` simbolico 2/2). Con A := ∂ − tanh x e P_b := ½⟨sech, ·⟩sech:

   U_q(t) = e^{it}P_b + A(L_0 + 1)^{−1}U_0(t)A†.

   La formula operatoriale è **VAR-P8(c) di S8-VAR**, contata una volta. ENC-L1 è fuso in VAR-P8(a) con R5-P7 (fix F5/F9). Contributo di questa sessione: il **nucleo esplicito** di U_0(t)(L_0 + 1)^{−1},

   G(t, z) = (e^{it}/4)[e^{−z}erfc(√(it) − z/(2√(it))) + e^{z}erfc(√(it) + z/(2√(it)))], √(it) := e^{iπ/4}√t,

   e quindi K_q(t, x, y) = (e^{it}/2)sech x sech y + (∂_x − tanh x)(∂_y − tanh y)G(t, x − y).

   *Prova del nucleo.* (1 − ∂_z²)G = K_0(t, z) e iG_t + G_zz = 0 sono verificati **simbolicamente** (`enc_s8b` §9). G è continua e limitata in z: per z → ±∞ gli argomenti di erfc hanno parte reale → ∓∞ e |e^{−w²}e^{∓z}| = O(1). Quindi G è temperata. L'unica soluzione temperata di (1 − ∂²)G = K_0 è Ĝ = e^{−itk²}/(1 + k²), perché 1 + k² ≠ 0 su ℝ, cioè G è il nucleo di U_0(t)(L_0 + 1)^{−1}. ∎ Da qui E^mult(t) = U_q(t) − U_0(t)e^{2it sech²} in forma chiusa nei soli ingredienti liberi.

*Domini limitati.* Su Ω limitato con condizioni al bordo, E_int A9 per V non è trattato qui: open_questions Q5. P3-T3 e CONV-Q6 riguardano il caso Dirichlet.

---

## 8. NS-EQUIV su Ω limitato (fix F7.4; HOR open_questions 4)

**[NS-EQUIV-Ω] Proposizione (prova scritta; SymPy `enc_s8b` 5/5, `enc_algebra` P0′).** Siano Ω = I × J un rettangolo limitato e Φ l'encoder puntuale più gauge.
- Avron–Herbst (i u_t = −u_xx + Fxu): v(t, y) = e^{iFt(y − Ft²) + iF²t³/3}u(t, y − Ft²).
- Lente (i u_t = −½u_xx + ½x²u, I ⊂ (−π/2, π/2)): v(tan t, x/cos t) = (cos t)^{1/2}e^{ix² tan t/2}u(t, x).

Allora:
- (a) *Dominio.* Φ è una biiezione Sol_V(Ω) → Sol_0(Ω′), senza condizioni al bordo (è un'operazione puntuale). Le immagini sono:
  - Avron–Herbst: Ω′ = {(t, y) : t ∈ I, y − Ft² ∈ J}, una striscia curva, rettangolo ⟺ F = 0;
  - lente: Ω′ = {(τ, y) : τ ∈ tan I, y/√(1 + τ²) ∈ J}, che per J = (−b, b) non è convessa ed è stellata rispetto all'origine se 0 ∈ I (fix ENC-10(a)).

  In entrambi i casi Ω′ è connesso e semplicemente connesso (immagine omeomorfa di un rettangolo).
- (b) *Bordo.*
  - Dirichlet su ∂_xΩ ⟷ Dirichlet sul bordo mobile di Ω′: il prefattore non si annulla.
  - Neumann ⟷ Robin dipendente dal tempo. Per Avron–Herbst: u_x = 0 ⟺ v_y = iFt v. Per la lente: u_x = 0 ⟺ v_y = i x sin t·v, cioè v_y = i y sin t cos t·v.
- (c) *I/S/E.*
  - (I) C3-T1 si applica a v su Ω′, perché richiede solo Ω connesso.
  - (S) C12-T1′ si applica su Ω′ semplicemente connesso.
  - Il trasporto all'indietro avviene però nell'anello coniugato Φ^{−1}ℂ[∂_τ, ∂_y]Φ, non in ℂ[∂_t, ∂_x]. Per Avron–Herbst ha coefficienti polinomiali in (t, x), non nel solo t: Φ^{−1}∂_yΦ = ∂_x + iFt e Φ^{−1}∂_tΦ = ∂_t − 2Ft∂_x + iFx − iF²t² (fix ENC-10(b); `enc_recep` 2/2). Per la lente i coefficienti sono trigonometrici in t e polinomiali in x.
  - (E): no. V è soppresso, non scomposto.
- (d) *Tempo di vita e incollamento della lente.* Per H = −½∂² + ½x² si ha U(π) = −iP (P parità), perché e^{−iπ(n+½)} = −i(−1)^n sulle funzioni di Hermite h_n. Sia W_k(t) := W_0(t − kπ) l'encoder sull'intervallo (kπ − π/2, kπ + π/2). Allora v_k(τ, y) = (−i)^k v_0(τ, (−1)^k y). L'incollamento attraverso le caustiche t = π/2 + kπ è esatto: la soluzione libera è la stessa a meno di parità e fase. Alle caustiche non c'è encoder di questa famiglia, perché θ = tan diverge.

*Prova.* (a) Calcolo diretto delle immagini. Non convessità della lente: (±T, b√(1 + T²) − ε) ∈ Ω′ ma (0, b√(1 + T²) − ε) ∉ Ω′. Stellatezza: s√(1 + τ²) ≤ √(1 + s²τ²) per s ∈ [0, 1]. Semplice connessione: Ω′ è l'immagine omeomorfa di un rettangolo. (b) Derivazione del prodotto (SymPy). (c) Rimandi a C3-T1 (Ω connesso) e C12-T1′ (H¹_dR = 0), più il calcolo del coniugato. (d) Si ha u(s + kπ) = (−iP)^k u(s) e W_0(s) commuta con P (chirp pari, x ↦ x/cos s pari). Quindi W_0(s)u(s + kπ) = (−i)^kP^kW_0(s)u(s). ∎

*Lettura.* "I/S/E sì/sì/sì" di F6-HOR va corretto in "I e S sì su Ω′ (dominio deformato, anello coniugato), E no". Il bordo resta Dirichlet ma diventa mobile, Neumann diventa Robin. L'incollamento della lente su tempi lunghi è esatto su ℝ. Su Ω limitato, ogni intervallo di lunghezza π ha la sua immagine Ω′_k, della stessa forma se I è simmetrico.

---

## 9. Strade riaperte assegnate a S8-ENC

**[FAD-1] Faddeev / Lippmann–Schwinger a energia fissata (prova scritta; SymPy `enc_s8b` 3/3).** Siano J = [x_0, x_0 + ℓ], λ = k² ∈ ℂ e V = Σ_{i=1}^{N}V_i con V_i ∈ C(J). Sia (G_0f)(x) := ∫_{x_0}^{x}sin(k(x − y))/k·f(y)dy (con sin(kz)/k := z per k = 0); G_0f risolve w″ + k²w = f con dati nulli in x_0. Sia u la soluzione di −u″ + Vu = λu con i dati di Cauchy di u^{(0)} (soluzione libera) in x_0. Allora:
- (i) u = u^{(0)} + G_0(Vu), e la serie di Neumann converge su J **senza ipotesi di piccolezza**: ‖(G_0V)^n‖ ≤ (C‖V‖_∞ℓ)^n/n!, con C := sup|sin(kz)/k|;
- (ii) le *componenti di Faddeev* u^{(i)} := G_0(V_iu) danno la scomposizione esatta u = u^{(0)} + Σ_iu^{(i)}, e il sistema N × N u^{(i)} = G_0V_i(u^{(0)} + Σ_ju^{(j)}) ha soluzione unica, per la stessa stima di Volterra su C(J)^N;
- (iii) (*E_int a energia fissata, quadro additivo di A9 nell'evoluzione in x.*) Sia u_i la soluzione con il solo V_i e sia 𝐕 := Σ_i‖V_i‖_∞. Allora E^add := u − Σ_iu_i + (N − 1)u^{(0)} = Σ_{i≠j}G_0V_iG_0V_ju^{(0)} + R, con ‖R‖_{C(J)} ≤ (Cℓ𝐕)³e^{Cℓ𝐕}‖u^{(0)}‖/3, uniformemente in N (fix ENC-11). Con ‖ΣV_i‖_∞ al posto di 𝐕 il resto non è controllato, perché i centri possono cancellarsi.

*Prova.*
- (i) (−∂² − λ)(u^{(0)} + G_0(Vu)) = −Vu, quindi u^{(0)} + G_0(Vu) risolve l'equazione e ha i dati di u^{(0)}: per unicità del problema di Cauchy coincide con u. G_0V è un operatore di Volterra con nucleo limitato da C‖V‖, da cui la stima fattoriale.
- (ii) Sommando su i si ritrova (i). L'unicità segue dalla stima di Volterra per il sistema.
- (iii) Sviluppando le serie di Neumann: u = Σ_n(G_0V)^nu^{(0)} e u_i = Σ_n(G_0V_i)^nu^{(0)}. I termini di ordine 0 e 1 si cancellano. All'ordine 2 resta (G_0V)² − Σ_i(G_0V_i)² = Σ_{i≠j}G_0V_iG_0V_j. Il resto è Σ_{n≥3}[(G_0V)^n − Σ_i(G_0V_i)^n]u^{(0)}. Siccome ‖V‖ ≤ 𝐕 e Σ_i‖V_i‖^n ≤ 𝐕^n, è ≤ 2Σ_{n≥3}(Cℓ𝐕)^n/n!·‖u^{(0)}‖ ≤ 2(Cℓ𝐕)³e^{Cℓ𝐕}‖u^{(0)}‖/6. ∎

*Lettura.* I: no. S: sì, esatta e lineare per centro. E: sì, fuori diagonale, con serie convergente. Ma tutto è **a λ fissato**: per dati non stazionari serve ENC-1, indipendente da λ (F6-ENC §6). La strada Faddeev entra in RT-ENC come strumento di scomposizione per centri a energia fissata.

**[POLE-N]** Vedi §4: negativa per Schrödinger, utile solo per il flusso di Lax.

**[GAM-O1] Gamblets (osservazione; CON-FONTE Owhadi 2017, SIAM Rev. 59, 99–149, numeri da verificare).** Per L_q coercivo su H¹_0(J) (per esempio q ≥ 0), la costruzione variazionale deterministica dei gamblets dà una decomposizione H¹_0 = ⊕_k𝔚^{(k)} ortogonale nel prodotto ⟨L_q·, ·⟩: la matrice di rigidezza è diagonale a blocchi per costruzione (proiezioni di Galerkin). Le basi dipendono da q, quindi non c'è un intertwiner W L_q = L_0 W: è una scomposizione (S) per scala, non un encoder. La localizzazione esponenziale delle basi è CON-FONTE (Owhadi 2017); l'interpretazione bayesiana non si usa (vincolo no-ML). Esito: **strumento, resta parcheggiato per B2**.

**[FW-1] MICRO / Foldy–Wouthuysen (prova scritta per il libero; SymPy `enc_s8b` 3/3).** Dirac 1+1 libero: H = αp + βm con α = σ_x, β = σ_z, m > 0. Sia U(p) := cos θ + βα sin θ con tan 2θ = p/m. Allora U è unitario e U H U^† = βE(p), E = √(p² + m²) (calcolo simbolico). U è un moltiplicatore di Fourier con entrate non razionali in p (sin²θ = (1 − m/E)/2), quindi **non locale**, coerente con II-T3 ("proiettori razionali ⟺ fattori"). Con potenziale V(x)·I la decomposizione esatta per fogli ±E esiste in forma astratta: Λ = sign(H), trasformazione di Eriksen, CON-FONTE, Thaller 1992 cap. 5, da verificare. La serie FW in 1/m è solo asintotica. Esito: FW è una **scomposizione (S) per fogli**, non un encoder (E2′) verso Dirac libero. Si passa a S8-SYS come strumento (S) per sistemi iperbolici; per B2 nessun encoder nuovo.

---

## 10. Kill-argument (passaggio avversariale interno; revisori esterni REVIEW_UNAVAILABLE)

*Rev. 2.* I kill-argument esterni sono stati eseguiti da S-CHECK-F8 (`work/CHECK-F8/KA_ENC_*`). Esiti:
- ENC-N1 (F6) è FALSO, con testimone (iv);
- ENC-N1′ SURVIVES come lemma di riduzione dopo ENC-5;
- ENC-P0(a), (b), P0′ e POLE-N SURVIVE con le riparazioni ENC-2, 3, 4, 14, 15;
- la tesi "le eccezioni cambiano il tempo" è KILLED.

Il passaggio interno che segue resta come documentazione della prima versione.

### 10.1 ENC-N1 / ENC-N1′

*Memo d'attacco (circa 200 parole).* "ENC-N1′ è una tautologia travestita da teorema. (i) è la definizione di funzione ben posta; (iii) aggiunge un'ipotesi (S) che è letteralmente la negazione del caso in cui la conclusione fallirebbe. Il risultato dipende interamente dalla scelta della famiglia di encoder {W_V}: cambiando la normalizzazione (stretta o modulo costanti, punto base x_0, parametro k_0 di ENC-U1) cambia la risposta, come mostra l'esempio (iv) costruito apposta. Il pacchetto non dimostra che esista una scelta canonica della famiglia, né che (S) valga in un caso non vuoto: nell'unico caso positivo (V(x), DM3) vale a vuoto, perché 𝒮_V ∩ 𝒮_{V′} = {0}. Dunque l'affermazione di G★″ 'encoder cieco ⟺ identificabilità congiunta' non aggiunge nulla a VAR-T1 e non andrebbe nel LEDGER come teorema."

*Difesa per punti.*
1. *"Tautologia."* **answered_by_current_text.** Il testo la dichiara come riduzione (prova di tre righe) e sposta il contenuto su VAR-T1(b), P0(b) e l'esempio (iv). Proposta di stato: PROVA SCRITTA con etichetta "lemma di riduzione", non teorema.
2. *"Dipende dalla famiglia."* **answered_by_current_text.** È il punto (iv), voluto: con DM-φ la risposta cambia con la normalizzazione. È un'informazione per l'algoritmo (fissare q(x_0) = 0, ENC-U1), non un difetto.
3. *"(S) vale solo a vuoto."* **partially_answered.** Vero per V(x) con DM3. Un caso con (S) non vuoto richiede soluzioni comuni non nulle, che VAR-T1 esclude nelle classi studiate. Resta aperto (open_questions Q4) se esiste una classe naturale con 𝒮_V ∩ 𝒮_{V′} ≠ {0} e (S) vera (candidato: classi V(t, x) con fasce di silenzio, dove però manca l'encoder).
4. *"Non andrebbe nel LEDGER."* **partially_answered.** Si propone di registrare ENC-N1 (F6) come FALSO come scritto e ENC-N1′ come lemma. Il contenuto "nuovo" è (iv) più (v).

*Esito.* PASS-WITH-FIXES: framing come lemma di riduzione (già nel testo), punto 3 in open_questions.

### 10.2 ENC-P0 / P0′ / P0(b)

*Memo d'attacco.* "ENC-P0(a) è il calcolo iM′ = 0, noto da sempre (quadro d'interazione); le ipotesi (H-P0) sono messe apposta per farlo funzionare, e la parte delicata, la regolarità del propagatore nella norma del grafo, è delegata a una fonte non verificata e a una prova di S8-VAR non auditata. P0′ è ancora più vuoto: ogni encoder 'soluzione → soluzione' è un quadro d'interazione riparametrizzato, quindi la 'classificazione' non distingue gli encoder utili (lente, locale) da quelli inutili (non locali). La sola affermazione con contenuto, 'solo V quadratico ha encoder puntuali', non è dimostrata qui ma citata (Bluman–Shtelen). P0(b) è una riga. Il claim di cammino critico 'ENC-P0 come teorema negativo in G★″ §6' è quindi sovradimensionato."

*Difesa per punti.*
1. *"Noto / calcolo banale."* **answered_by_current_text.** Il pacchetto non rivendica novità. Lo stato proposto è PROVA SCRITTA con nota "classico".
2. *"Regolarità delegata."* **partially_answered.** (H-P0) è un'ipotesi dichiarata. Per H_0 = −∂² e V(t) limitato continuo in norma la fonte è standard (Pazy cap. 5) e la prova è VAR-P11. S-CHECK deve controllare la continuità nella norma del grafo (CHECK_REQUEST D6).
3. *"P0′ non distingue i locali."* **answered_by_current_text.** È dichiarato: la località è la classificazione di Bluman–Shtelen (CON-FONTE verificata), citata e non dimostrata.
4. *"Il teorema negativo è una riga."* **answered_by_current_text.** P0(b) è rafforzato (nucleo finito, c(t) arbitraria, lemma sul rango delle moltiplicazioni). *Rev. 2:* il contenuto per G★″ è la sintesi in testa a §4. La frase della prima versione, "le eccezioni cambiano il tempo", è falsa (ENC-2). Post-Gate 8: anche la dicotomia "θ ≠ id ⟺ α ≢ 0" della rev. 2 vale solo in forma esistenziale (ENC2-4). POLE-N ne è un'applicazione nella versione classica.

*Esito.* PASS-WITH-FIXES. Da S-CHECK: verifica della continuità nella norma del grafo; in G★″ §6 citare P0(b), non P0(a), come teorema negativo.

### 10.3 Controllo rapido su ENC-1 (cammino critico della regola R6)
- *Attacco:* "rettangolo simmetrico e dipendenza da x_0 rendono l'encoder non canonico".
- *Risposta:* ENC-U1 classifica esattamente la non canonicità: retta {T_{k_0}} più il punto base. La simmetria del dominio è necessaria per la costruzione triangolare. *Domini non simmetrici (rev. 2, fix ENC-8(b)):* se il dominio dei dati J′ non è simmetrico attorno a x_0, si prende come punto base il centro di J′. In alternativa ci si restringe al più grande intervallo simmetrico attorno a x_0 contenuto in J′, perdendo dati. La frase della prima versione ("J ⊂ [x_0 − a, x_0 + a] basta, restringendo") andava nel verso sbagliato.
- *Unico punto non chiuso:* la limitatezza su H^{2k} (Q2).

---

## 11. Risposta alla DOMANDA di S8-DICT (R6)

Sì. ENC-C1 dà esattamente l'intrecciamento richiesto. Per ogni L = P(∂_t, L_q) del livello q-dizionario, L̂ = φ(P)(∂_t, ∂_x) = P(∂_t, L_0) soddisfa W(Lu) = L̂(Wu).
- Spazi: Y = C^∞(Ω) (biiezione), e con norme Y = C(Ω̄) o L²(Ω), Ω = I × (x_0 − a, x_0 + a). Lì W, W^{−1} sono limitati (ENC-1(5)), e dist(u, ker L) ≥ dist(Wu, ker L̂)/‖W‖, dist(Wu, ker L̂) ≥ dist(u, ker L)/‖W^{−1}‖.
- H^{2k}: non chiuso (Q2).
- Le disuguaglianze seguono da W(ker L) = ker L̂ (biiezione che intreccia). Sugli spazi completati ker L va inteso come chiusura in Y: da precisare in S8-DICT (nota del revisore, §2.1).
- Il livello libero corrispondente è solo il sottoanello pari ℂ[τ, ξ²]: gli elementi dispari del dizionario libero non hanno controparte (ENC-T2).
- W dipende da x_0 ed è unico solo con la normalizzazione dei dati di Cauchy (ENC-U1).
- q deve essere **dato**, oppure ottenuto da VAR-T1(b) a forma nota (circolarità F6).

## 12. Tabella riassuntiva (rev. 2, dopo S-CHECK-F8-ENC)

"Proposto dal revisore" indica lo stato che S-CHECK-F8-ENC propone. La registrazione spetta a central.

| ID | stato | SymPy |
|---|---|---|
| ENC-D (E2′) | definizione; (E1) = nucleo finito su 𝒴 | — |
| ENC-K0 | DIMOSTRATO (proposto dal revisore) | enc_algebra 6/6, enc_s8b 2/2 |
| ENC-1 (1)–(6) | DIMOSTRATO (proposto dal revisore); CON-FONTE Marchenko cap. 1, senza numero di teorema, solo come confronto | enc1_goursat 11/11; audit E1a–E1d, E6 |
| ENC-U1 | DIMOSTRATO dopo ENC-7 (proposto dal revisore) | enc1_goursat 3/3, enc_recep 1/1 |
| ENC-C1 | DIMOSTRATO (proposto dal revisore) | — |
| ENC-T2 (a)(b)(c) | DIMOSTRATO, lemma a q noto (proposto dal revisore); non è uno strumento di B1 | enc_algebra 6/6, enc_s8b 2/2 |
| ENC-T2(c′) | prova scritta, DA AUDITARE, solo in C^∞(Ω) senza vincoli e con la definizione di "certifica" (ENC2-6); con vincolo di grado **FALSO**; nella classe principale **APERTO**; R6 non lo usa | enc_recep 1/1 |
| ENC-P0(a) | DIMOSTRATO sotto (H-P0) (proposto dal revisore) | — |
| ENC-P0(b) | DIMOSTRATO, (E1) su ℋ, in L² (proposto dal revisore); non copre ENC-1 | — |
| ENC-P0(b)^cl | prova scritta con le ipotesi (i)/(ii) di ENC2-1, DA AUDITARE (il revisore propone DIMOSTRATO dopo ENC2-1) | — |
| ENC-P0(b)^loc | rev. 2 **FALSO come scritto** (ENC2-1); versione corretta prova scritta, DA AUDITARE | — |
| ENC-P0′ astratto | DIMOSTRATO (proposto dal revisore); versione su nucleo denso con 0 ∈ I ed esempi su 𝒮 DA AUDITARE (fix ENC2-2, ENC2-3 recepiti) | enc_algebra 3/3 |
| ENC-P0′-DIC, forma della rev. 2 | **FALSO come scritto** (controesempio pseudo-conforme, ENC2-4) | enc_g8 1/1 |
| ENC-P0′-DIC esistenziale (si può scegliere θ = id ⟺ α ≡ 0; α ≢ 0 ⇒ θ non affine) | prova scritta, DA AUDITARE + CON-FONTE Bluman–Shtelen | enc_recep 1/1, enc_g8 3/3 |
| "le eccezioni cambiano il tempo" | **FALSO come scritto** (KILLED) | enc_recep 1/1 |
| POLE-N | DIMOSTRATO dopo ENC-4 (proposto dal revisore); POLE-N^cl con il rettangolo di ENC2-5: prova scritta, DA AUDITARE | enc_g8 1/1 (POLE3) |
| ENC-N1 (F6) | **FALSO**, testimone ENC-N1′(iv) | enc_recep 1/1 per (v) |
| ENC-N1′ | DIMOSTRATO come lemma di riduzione dopo ENC-5 (proposto dal revisore) | — |
| ENC-K1′ | DIMOSTRATO dopo ENC-9 (proposto dal revisore); nessuna novità (Andrianov–Sokolov 2003, Sokolov 2008) | enc_algebra 5/5, enc_s8b 2/2 |
| ENC-K1 | **CON-FONTE da verificare** (D–G, solo V → 0) | — |
| ENC-A9(a) | DIMOSTRATO, costante 2/3 ottimale (proposto dal revisore) | enc_s8b 2/2, eint_closed 2/2, enc_recep 1/1 |
| ENC-A9(b1) | DIMOSTRATO (proposto dal revisore) | eint_closed |
| ENC-A9(b2) | forma chiusa DIMOSTRATO; stima della prima versione **FALSO**; stima corretta DIMOSTRATO (proposti dal revisore) | eint_closed 6/6, enc_recep 3/3 |
| ENC-A9(b3) | CON-FONTE + V-ex, ereditato da VAR-T10(3)(iii); fuso in VAR-T10 (O16) | eint_closed 4/4 |
| ENC-A9(b4) nucleo (Pöschl–Teller modificato) | DIMOSTRATO (proposto dal revisore) | eint_closed, enc_s8b |
| ENC-A9(b) per parti (O16) | (b1), (b2) corretta, (b4): DIMOSTRATO (proposto dal revisore); (b3): CON-FONTE + V-ex | — |
| NS-EQUIV-Ω | DIMOSTRATO dopo ENC-10 (proposto dal revisore) | enc_s8b 5/5, enc_recep 2/2 |
| FAD-1 | DIMOSTRATO dopo ENC-11 (proposto dal revisore) | enc_s8b 3/3 |
| FW-1 | DIMOSTRATO per il libero (proposto dal revisore); con V CON-FONTE | enc_s8b 3/3 |
| GAM-O1 | osservazione + CON-FONTE | — |
| ENC-L1 | fuso in VAR-P8(a) (R5-P7) | — |
