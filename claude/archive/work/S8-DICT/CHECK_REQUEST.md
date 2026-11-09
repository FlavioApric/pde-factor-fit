# CHECK_REQUEST — S8-DICT (27/10/2026)

**Destinatario:** S-CHECK (proof-checker). **Testo da verificare:** `work/S8-DICT/PROOF_PACKAGE.md`, §1–§5.
**Check numerici:** sympy/s8dict_checks.py (27/27 OK) e sympy/s8dict_checks2.py (12/12 OK).
**Kill-argument:** KILL_ARGUMENT_N1.md, verdetto PASS-WITH-NOTES, senza revisore fresco.
**Stato richiesto:** per ogni claim marcato "prova scritta", passaggio da CANDIDATO a DIMOSTRATO solo dopo S-CHECK. Nessun claim è dichiarato DIMOSTRATO in questo pacchetto.

## Claim da verificare (in ordine di priorità)
1. **DICT-N1(v) con i Lemmi ND e ND-NL (§2.5).** La complementare di F_n è densa, magra e shy. Domande:
   - La sonda finito-dimensionale (base adattata al grado, F10) dà davvero un insieme di misura nulla per ogni traslato?
   - Serve la misurabilità universale di F_n, che è chiuso?
2. **Teorema RANGO (I)–(IV) (§2.6).**
   - Nel passo (II), il fibrato a rango costante su un denso aperto è giustificato? Il rango è semicontinuo inferiormente, quindi è localmente costante su un aperto denso.
   - Le conclusioni (a′) Schrödinger complesso/reale e (b′) a(t,x) seguono come scritto?
3. **Teorema A(iii) (§3.3).**
   - Il sistema M × (M+1) dà γ ≠ 0. La località dà l'indipendenza di D_iw su B_{k_0}.
   - Il polinomio in s ha coefficiente direttore non nullo: controllare la scelta dei funzionali ℓ′.
   - L'ipotesi dichiarata (aperto U_0 d'indipendenza) basta?
4. **Lemma U2-a (§1.2).** La realizzazione g_{y,j} e la levigatezza di F(y,j) via regolarità più Boman. Controllare in particolare la condizione 𝒲 (dominio aperto dei getti ammissibili) e che F non dipenda dalla scelta di f.
5. **CS-1 (§1.6).** Controllare:
   - la costante c_s = 2^{1−2s}Γ(1−s)/Γ(s);
   - la convergenza del limite y → 0 di y^{1−2s}∂_y;
   - la decrescenza di φ_s (F6).
6. **U3(d)(iii) (§1.4).** L'uniformità in t dell'errore relativo della regola dei trapezi in striscia per t^{−β}: controllare la stima della coda e la larghezza della striscia.
7. **N3(b) (§1.5).** Distanza ≥ 1 su (0, T) per il ritardo: l'argomento di estensione e il minimo del rapporto (F4, 1,0071).
8. **I-LIM (§4)** (a)–(d): la compattezza di 𝒦_R in C^s, la costante C_{R′} e il corollario hölderiano per s = 0.
9. **NS-L1, NS-T1 (§5.1–5.2).** L'argomento "aggiungere un elemento cambia trdeg di ≤ 1" e l'uguaglianza ℂ⟨w⟩ = F_1(w).
10. **MF3(a), (d) (§3.2).** La scelta delle ψ in un insieme numerabile Ψ denso e la terminazione della semi-decisione nel modello (T) con oracolo.
11. **R6-T (§3.6, aggiunto il 27/10).** Controllare (a) la biiezione φ fra livello q e livello libero pari con conservazione del peso j + 2k; (b) la stima ‖W‖, ‖W^{−1}‖ ≤ 1 + a²Q·e^{a√Q} su C(Ω̄) e L²(Ω) (Fubini in t); (c) il confronto delle distanze e dei λ_min; (d) il trasporto dei certificati ψ ↦ ψ∘W. Il lemma importa ENC-1, ENC-C1 ed ENC-T2 da S8-ENC.

## Punti delicati noti
- **N1(iii)** richiede N ≥ 2: per N = 1 l'enunciato originale è FALSO (§2.3).
- **N1(vi)** originale è ritirato.
- **R6** è recepita in §3.6: vale solo sul sottoanello pari ℂ[∂_t, L_q], con q dato, Y = C(Ω̄) o L²(Ω) su rettangolo simmetrico; H^{2k} e la forma debole MF3 non sono coperti.
- **Hölder per s ≥ 1**, la velocità per nuclei c.m. generali e B3 restano candidati o CON-FONTE.
- Le citazioni marcate "da verificare" sono elencate in open_questions Q7.

---

## Aggiornamento del 27/10/2026, dopo l'audit
L'audit è chiuso: `work/CHECK-F8/AUDIT_S8-DICT.md`, con il kill-argument indipendente `work/CHECK-F8/KA_DICT_N1_*` (SURVIVES-WITH-FIXES). Tutti i fix DICT-1 … DICT-18 sono recepiti: l'elenco "fix → modifica → file/sezione" è in `RECEPIMENTO.md`. Le domande 1–11 qui sopra hanno avuto risposta nell'audit.

La domanda 3 sull'ipotesi U_0 è superata: per DICT-1 l'ipotesi era vuota ed è stata tolta, e A(iii) vale senza ipotesi aggiuntive.

**Resta da auditare (claim nuovo, DA AUDITARE):**
12. **DICT-MAG-NU (PROOF_PACKAGE §2.6, punto "Sistemi: caso magnetico").**
   - Enunciato: per n ≥ 2, se (A, V) è una legge reale per u e χ ∈ C_c^∞ ha supporto dove u ≠ 0, allora B := |u|^{−2}∇^⊥χ (nelle prime due coordinate) dà una seconda legge reale (A + B, V + δV), con δV = −2iB·∇u/u − i div B − 2A·B − |B|².
   - Da controllare: la realtà di δV, che equivale a div(|u|²B) = 0, e l'identità delle differenze.
   - Verifica: `sympy/s8dict_checks3.py`, R3.
   - La condizione div(|u|²B) = 0 viene dall'aggiudicazione del KA (P4). La prova scritta della non unicità è di questo recepimento.

**Script nuovo:** `sympy/s8dict_checks3.py` → `.out`, **9/9 OK**:
- R1 per DICT-4: con il nodo λ = 0 trattato esattamente l'errore L¹ scende da 0,517 a 0,0151; senza nodo resta circa T;
- R2: il controesempio a N1(vi);
- R3: DICT-MAG-NU.

---

## Aggiornamento post-Gate 8 (27/10/2026)
- **Punto 12 (DICT-MAG-NU): chiuso** da `work/CHECK-F8/AUDIT_S8-DICT_rev2.md` §1, con i rilievi MAG-1…MAG-4 recepiti in PROOF_PACKAGE §2.6. Le ipotesi ora sono A, V dipendenti da (t, x), supp χ ⊂ {u ≠ 0} e u ≢ 0. Il "se e solo se" è ristretto a supp B ⊂ {u ≠ 0}.
- Per O15 di ATTACK-8, DICT-MAG-NU è registrato come corollario di SYS-N3(c) e non come claim autonomo.
- **Punto R6:** MAG-5 è recepito. (f) cita DICT-N1(ii) e il Teorema A.
- **Nessun claim nuovo da auditare** in questo recepimento. Le aggiunte sono riformulazioni richieste dagli audit:
  - il paragrafo "Significato e ipotesi" (O5) in §2.6;
  - la prova di (f) in §3.6, scritta con N1(ii) e il Teorema A(iii).
- Un controllo leggero della prova di (f) è comunque utile.
