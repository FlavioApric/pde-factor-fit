# AUDIT S8-DICT, revisione 2 — S-CHECK-F8-DICT · 27/10/2026

Richiesta: mini-audit del coordinatore dopo il recepimento di S8-DICT (`work/S8-DICT/RECEPIMENTO.md`). Tre compiti: (1) auditare il claim nuovo DICT-MAG-NU (PROOF_PACKAGE §2.6, punto "Sistemi"); (2) verificare che il passaggio di DICT-R6 a DIMOSTRATO sia legittimo alla luce di `AUDIT_S8-ENC.md` e del recepimento di S8-ENC; (3) controllare a campione il recepimento dei fix DICT-1…DICT-18.

Letti: `work/S8-DICT/RECEPIMENTO.md`; PROOF_PACKAGE §1.4, §2.3, §2.6 (con "Sistemi"), §3.3 (nota), §3.6 completa, §5.2, §7; `work/S8-SYS/PROOF_PACKAGE.md` SYS-N3; `work/CHECK-F8/AUDIT_S8-ENC.md` §0, §1 (ENC-6, ENC-8), §2.1–§2.2; `work/S8-ENC/RECEPIMENTO.md`; coda di `inbox/S8-DICT.md` e `inbox/central-F6.md` (nessun avviso di S8-ENC che modifichi ENC-T2).

Script:
- `sympy/dict2_mag.py` → `.out`: **16/16 PASS** (indipendente; convenzione i u_t = −(∇ − iA)²u + Vu);
- rieseguito `work/S8-DICT/sympy/s8dict_checks3.py` (senza modificarlo): **9/9 OK**.

**Dichiarazione di non indipendenza.** La costruzione B = |u|^{−2}∇^⊥χ è stata proposta da questo revisore nell'aggiudicazione del KA (P4). L'audit di MAG-NU non è quindi del tutto indipendente. Il rischio è mitigato da due fatti: il caso u ≠ 0 ovunque è già SYS-N3(b)(c), auditato separatamente da S-CHECK-F8-SYS; e le verifiche di `dict2_mag.py` coprono casi (zeri di u, dipendenza dal tempo, n = 3) che non erano nell'aggiudicazione.

## 0. Verdetti

| ID | verdetto | fix | stato proposto |
|---|---|---|---|
| DICT-MAG-NU | **OK con fix MINOR** (ipotesi da completare) | MAG-1, MAG-2, MAG-3, MAG-4 | **DIMOSTRATO** dopo MAG-1 e MAG-2 |
| DICT-R6 (Lemma R6-T) | passaggio a DIMOSTRATO **legittimo** | MAG-5 (MINOR, citazione in (f)) | **DIMOSTRATO** |
| Recepimento DICT-1…DICT-18 | **completo** nel campione; tutte le 18 etichette presenti | — | stati della tabella di AUDIT_S8-DICT confermati |

Nessun punto dubbio sul cammino critico N1: kill-argument non necessario.

## 1. DICT-MAG-NU

**Enunciato nel pacchetto.** Per n = 2, con U aperto, u ≠ 0 su Ū, χ ∈ C_c^∞(U) non nulla, B := |u|^{−2}∇^⊥χ soddisfa div(|u|²B) = 0 ed è non nullo; quindi, se una legge reale (A, V) esiste, (A + B, V + δV) è una seconda legge reale, con δV = −2iB·∇u/u − i div B − 2A·B − |B|². Per n > 2 si usa lo stesso B nelle prime due coordinate.

**Prova, ricontrollata.**
- *Identità delle differenze.* (∇ − i(A + B))²u − (∇ − iA)²u = δV·u, per A, B, u generici (`dict2_mag` M1, simbolico). Con la convenzione della legge, (A + B, V + δV) risolve la stessa equazione se e solo se δV è questo, dove u ≠ 0.
- *Realtà.* Im(δV)·|u|² = −div(|u|²B) (M2, simbolico, con u = a + ib generico). Quindi δV è reale ⟺ div(|u|²B) = 0 su {u ≠ 0}.
- *Costruzione.* div(|u|²B) = div ∇^⊥χ = 0. B è liscio perché |u|² > 0 sul supporto di χ, e ha supporto compatto in {u ≠ 0}; δV è liscio e a supporto nello stesso compatto (fuori, B = 0 e δV = 0), quindi la nuova coppia è liscia su tutto il dominio anche se u ha zeri altrove. B ≢ 0 perché χ, a supporto compatto e non nulla, non è costante nelle variabili spaziali.
- *n > 2.* B = |u|^{−2}(∂_2χ, −∂_1χ, 0, …): div(|u|²B) = 0 (M5, simbolico).
- *Esempi concreti.* M3: u = e^{−iEt} sin x sin y (zeri sulle rette x, y ∈ πℤ), A = 0, V = E − 2, χ bump nel disco di raggio 1 attorno a (π/2, π/2): la nuova legge risolve l'equazione (residuo ~10⁻¹⁷⁷) e δV è reale. M4: u = e^{i(x−t)} + e^{i(2y−4t)}, soluzione libera non stazionaria con zeri (t = 0, x = π, y = 0), χ bump nello spazio-tempo lontano dagli zeri: stesso esito.
- *Campi magnetici diversi.* rot B = −div(|u|^{−2}∇χ) ≢ 0 per il principio del massimo (come in SYS-N3(c)); in M3 |rot B| raggiunge 9,2 (M6). La seconda legge non è quindi un cambio di gauge.

**Fix.**

**MAG-1 (MINOR: ipotesi mancante).** La costruzione richiede che la classe ammetta A, V dipendenti da (t, x), come in SYS-N3: se |u| dipende da t, il B costruito dipende da t (M7: ∂_tB ≠ 0 in M4). Con coefficienti statici e u non stazionaria l'argomento non dà una legge della classe, e la non unicità non è dimostrata. Scrivere: "A, V ∈ C^∞(J × Ω; ℝ); U ⊂ J × Ω aperto; χ ∈ C_c^∞(U); ∇^⊥ agisce nelle variabili spaziali". Il caso statico è coperto solo per u stazionaria (|u| indipendente da t, χ = χ(x)).

**MAG-2 (MINOR: ipotesi da precisare).** Basta supp χ ⊂ {u ≠ 0}; "u ≠ 0 su Ū" è più forte del necessario. Serve {u ≠ 0} ≠ ∅; se u ≡ 0 ogni coppia (A, V) è una legge e la non unicità è banale. Va detto esplicitamente.

**MAG-3 (MINOR: "se e solo se" del punto "Sistemi").** La frase "(A + B, V + δV) è una legge reale se e solo se div(|u|²B) = 0 su {u ≠ 0}" è corretta per B a supporto in {u ≠ 0}. Se il supporto di B incontra Z(u), servono anche due cose: che δV si estenda in modo liscio attraverso Z(u), e che −2iB·∇u = 0 su Z(u). La seconda è l'equazione nei punti dove u = 0. È lo stesso schema di DICT-3. Ci sono due modi di sistemare: restringere il "se e solo se" ai B con supporto in {u ≠ 0}, oppure aggiungere le due condizioni. Per u reale la condizione B·∇u = 0 su Z(u) segue già da div(u²B) = 0 per continuità; nel caso complesso non è stata verificata.

**MAG-4 (MINOR: collocazione).** MAG-NU è la versione localizzata di SYS-N3(b)(c), con k = −|u|²B = −∇^⊥χ. Il contributo nuovo è che u può avere zeri fuori dal supporto di χ, mentre SYS-N3 chiede u ≠ 0 ovunque. Conviene citare SYS-N3(c) per rot B ≢ 0, e dire "una seconda legge con campo magnetico diverso" invece di "una seconda legge reale". Quest'ultima formulazione è vera ma più debole.

**Stato proposto:** DIMOSTRATO, dopo MAG-1 e MAG-2. MAG-3 e MAG-4 sono di redazione.

## 2. DICT-R6: legittimità del passaggio a DIMOSTRATO

- **Condizione.** L'audit precedente (AUDIT_S8-DICT §2) proponeva "DIMOSTRATO condizionato a ENC-1, ENC-C1, ENC-T2". AUDIT_S8-ENC §0 dà ENC-1 (1)–(5) DIMOSTRATO, con il MINOR ENC-8. ENC-C1 è DIMOSTRATO. ENC-T2 (a)(b) è DIMOSTRATO come lemma a q noto, solo nel sottoanello pari; ENC-T2 (c) è DIMOSTRATO dopo ENC-6. Sul cammino critico l'audit ENC conclude, verbatim: «Il cammino critico ENC-1 → ENC-C1 → ENC-T2 → R6 di S8-DICT regge»; nessun kill-argument lo tocca. Le ipotesi di R6 corrispondono a queste letture: (H-q) q dato, che è ENC-6(b); il sottoanello pari, che è ENC-T2(b); (H-dom) il rettangolo simmetrico, coerente con ENC-8(b); la convenzione φ(P)(τ, ξ) = P(τ, −ξ²).
- **Recepimento di S8-ENC.** `work/S8-ENC/RECEPIMENTO.md` dichiara ENC-1, ENC-C1 ed ENC-T2(a)(b)(c) **invariati** («Il cammino critico ENC-1 → ENC-C1 → ENC-T2 → R6 di S8-DICT non è stato indebolito»). Le correzioni sono MINOR: il refuso B in ENC-U1, la norma HS, la notazione Δ e i domini non simmetrici. Nessuna tocca la costante C_W né l'intrecciamento. In inbox/S8-DICT.md non c'è alcun avviso di S8-ENC che modifichi ENC-T2.
- **Nota di AUDIT_S8-ENC §2.1** («sugli spazi completati serve che ker L sia inteso come chiusura, da precisare in S8-DICT»). R6-T(c) è scritto in termini di residui r_n = inf‖Lu‖_Y, non di dist(u, ker L). Così la questione della chiusura non si pone: soddisfatta.
- **MAG-5 (MINOR, citazione).** R6-T(f) attribuisce «nessun getto finito certifica Ann_q(u) ≠ 0» a ENC-T2(c). Dopo ENC-6(a) questa conseguenza vive in ENC-T2(c′), un'osservazione nuova di S8-ENC marcata DA AUDITARE. Il contenuto di (f) segue comunque da N1(ii) e dal Teorema A, già DIMOSTRATO. Citare quelli, oppure ENC-T2(c′) dopo il suo audit. (a)–(e) non dipendono da (f).
- **Esito:** il passaggio di DICT-R6 a DIMOSTRATO è **legittimo**. La riserva del pacchetto resta corretta: va riallineato se S8-ENC modificherà ENC-T2 in futuro.

## 3. Recepimento dei fix DICT-1…DICT-18 (campione)

Tutte le 18 etichette "[fix DICT-k]" sono presenti in PROOF_PACKAGE. Controllati nel merito:
- **DICT-1:** nota in §3.3, U_0 tolto, prova con gli O_m.
- **DICT-2:** definizione ker Φ_u = 0, (IV) riformulato, condizione d ≥ 1 o m ≥ 2 in (a′).
- **DICT-3:** "⟺" solo per u senza zeri, con i due controesempi.
- **DICT-4:** prova di §1.4(ii) riscritta con μ = μ({0})δ_0 + μ′. Ricontrollata: μ′ è finita vicino a 0 perché ∫min(T, 1/λ)dμ < ∞, la continuità dall'alto vale per μ′({0}) = 0, e la stima totale è 3η. Corretta.
- **DICT-5:** caso magnetico fuori da RANGO; vedi §1 sopra.
- **DICT-6:** "L ∈ Ann(u)" nell'enunciato. La nota N = 1 distingue deg L da deg L − D; ricontrollata: dim(P_min)_{≤n} − dim(L)_{≤n} = deg L − D.
- **DICT-7:** test di arresto r_n = dist(D_0u, W_n).
- **DICT-9:** conseguenza ristretta alle forme evolutive.
- **DICT-17:** dominio di (c).
- **DICT-18:** motivazione corretta.
- **Solo per presenza dell'etichetta:** DICT-8, 10–16.

Il check dell'autrice `s8dict_checks3.py`, rieseguito, dà 9/9.

Anche N1(vi) come FALSO (§2.6bis) è coerente con la tabella di AUDIT_S8-DICT. I controesempi sono u = t + x nella classe u_t = a u_x, dove a ≡ 1 è unica, e u = t − x² nella classe normalizzata.

## 4. Sintesi
- DICT-MAG-NU: DIMOSTRATO dopo i fix MINOR MAG-1 (A, V dipendenti da (t, x)) e MAG-2 (supp χ ⊂ {u ≠ 0}, u ≢ 0).
- DICT-R6: DIMOSTRATO legittimo; MAG-5 è solo una citazione.
- Recepimento dei fix DICT-1…18: completo nel campione.
