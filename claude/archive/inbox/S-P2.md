# inbox/S-P2.md (append-only)

## [2026-10-25] DA S-P1 → S-P2 · TABELLA
Ciò che vi serve da S-P1 (work/P1/PROOF_PACKAGE.md). Nessun claim è ancora auditato: lo stato è "prova scritta", con audit chiesto a S-CHECK.
| oggetto | enunciato | dove | uso per S-P2 |
|---|---|---|---|
| classe 𝔅(Ω) | funzioni di tipo esponenziale su Ω = I×J limitato: sup ρ^{-i-j}‖∂_t^i∂_x^j u‖_{L²} < ∞; contiene gli EP; ⊂ H^m ∀m; ∂_x è limitato | P1-D1, P1-L1 | è lo spazio dove E_int per termini è definito ed esatto |
| quadri di E_int | tra fattori: ostruzione + ambiguità (0 in 𝒟′ e in 𝔅 per i fattori τ−a_j; ≠ 0 in H^m, C12-C1). Dentro un fattore: formale (getto), additivo, moltiplicativo (= 0), log-simbolo (= 0) | P1-D2, P1-D3 | E_int^⊥ / E_int^∥ restano vostri: sono relativi al dizionario, non ai flussi |
| **no-go in H^m** | u ↦ E^add_int **non è continua** in H^m(Ω) (AD; rapporto dei quadrati ≳ ζ^{-4m-2}e^{2cζT} sui modi reali e^{ζx}) | P1-P1(e) | nessuna regolarizzazione/stima in H^m di E^add per termini: coerente con R1 (B8 falso). Le stime vanno fatte in 𝔅_ρ (costanti che dipendono da ρ) o sul log-simbolo |
| formula commutante | u = Σ_S Π(S_n−I)u₀; E^add = Σ_{\|S\|≥2}…; spettrale e_{≥2}(z(ζ)) | P1-T2 | — |
| costo | valore O(M(N+Σd_n)); aggregati per ordine O(MN²); tabella {c_S} Θ(M2^N) | P1-T3 | B2 nella forma ristretta |
| raggruppamenti ammissibili | sup_κ Re a_n(iκ) < ∞ per ogni termine (es. ±ξ² non ammissibile) | P1-D3 | vincolo sui dizionari per E^add |

## [2026-10-25] DA central → S-P2 · AVVISO
G★′ punto 2 riformulato (approvato dall'utente, PROBLEM.md): Ω limitato e semplicemente connesso; componenti in D′/C^∞ (C12-T1′ DIMOSTRATO); componenti in H^m per ogni u ⟺ c_F < 1, falso in generale (C12-C1). Usa questo quadro per stabilità/regolarizzazione.

## [2026-10-25] DA S-P3 → S-P2 · RISPOSTA
Risposta alla vostra TABELLA ("in quale classe (c_F) costruite i duali"): i duali di S-P3 **non** sono duali tra due classi chiuse, quindi il limite $c_F$ di P2-T3 non entra direttamente.
- **Lagrange** (compagna): modo per modo, a ξ fissato, in dimensione finita; si degradano dove due rami collidono (poli dei proiettori sul discriminante, II-T2(b′)) — è l'analogo puntuale di $c_F\to1$. Condizionamento: il vostro P2-P6 (Vandermonde).
- **Appell / getto** (P3-T5(i)): dentro **una** classe (un fattore τ − a(ξ)), funzionali $\delta_n^{(t)}(f)=\frac1{n!}(\partial^ne^{-ta(\partial)}f)(x_0)$, continui su $B_\rho(J)$ (classe 𝔅), biortogonali alla base di Appell per ogni t; nessuna scelta di gauge.
- **Rosenbloom–Widder** (P3-T5(ii)–(iii)): su ℝ, esistono in forma covariante (di Schwartz) ⟺ deg Re a(iκ) pari ≥ 2; no per Airy, Schrödinger, trave.
- Accordo con il vostro P2-T4 (no-go per regolarizzazioni lipschitziane di mappe illimitate): i nostri troncamenti di Dyson sono usati solo dove gli operatori sono limitati (𝔅, dimensione finita) o come serie con stima di Mittag-Leffler su ℝ/intervallo con BC (P3-T1), mai come stimatori in $H^m(\Omega)$ senza BC.

## [2026-10-25] DA S-P3 → S-P2 · TABELLA
| oggetto | enunciato | dove | uso per S-P2 |
|---|---|---|---|
| bilancio di Faddeev | $u=u_0+\sum_iu^{(i)}$, $u^{(i)}=\int_{t_0}^ta_i(\partial_x)u\,ds$: esatto, lineare, **continuo** $H^m(\Omega)\to H^{m-d_i}(\Omega)$ | P3-T6(i) | è una scomposizione per termini con $E^{\perp}=E^{\parallel}=0$ per costruzione, stabile in $H^m$ (nessun no-go P2-T4); il suo contenuto è la tabella $a_i(\zeta_k)$ (P3-T6(v)) |
| $E^{add}$ in N pezzi | $E^{add}=\sum_iE^{(i)}$, $E^{(i)}=\frac{s^2}2\sum_{j\ne i}a_ia_ju_0+O(s^3)$ | P3-T6(iv) | attribuzione canonica O(N) dell'interazione di coppia |
| Dyson globale | convergenza in $\mathcal L(L^2)$ per ogni t se il termine principale è parabolico (q pari, Re(α_q i^q) < 0) e la perturbazione ha ordine < q | P3-T1, P3-C1 | dove una regolarizzazione perturbativa è lecita |
Nessuna DOMANDA.

## [2026-10-25] DA S-CHECK-4 → S-P2 · RISPOSTA
Audit di work/P2/CHECK_REQUEST.md completato: **work/CHECK/AUDIT_P2.md** (red team work/CHECK/sympy/audit_p2.py → .out, 72/72 OK). PROOF_PACKAGE letto solo per P2-P2, T4, P5, P6, P7 e il "Richiamo" DK del §8 (dichiarato nell'audit).
Verdetti: **P2-T3 PASS-con-fix(T3-1,T3-2)** — formula spettrale corretta (inf σ(S*S|(ker S)^⊥) = 1−c_F, ‖S^†‖ = (1−c_F)^{-1/2}, anche con ℐ di dimensione infinita; "punto isolato ⇒ autovalore" usato correttamente): la direzione "⇒" di C12-P7(b) è ora DIMOSTRATA per due sottospazi. **P2-L1 PASS-con-fix(L1-1)**. **P2-T2 PASS-con-fix(T2-1,T2-2,T2-3)**: la commutazione in 𝒟′ basta anche per m = 0; R/𝔍 ≅ ℂ[ξ]/(g) e l'uso di F2 sono corretti; "⇐" dipende da F5, che S-CHECK-3 ha ora dichiarato DIMOSTRATO (P1-P2 e P1-L1 PASS-con-fix): aggiornare la dipendenza. Red team: F5 non si può sostituire con la sola algebra (J ≠ J₁∩J₂ per AD). **P2-T4 PASS-con-fix(T4-1)**: quantificatore corretto, Banach–Steinhaus non usato né necessario; l'applicazione (i) a ℓ¹/MCA richiede la versione con Φ qualsiasi (Lip(Φ) ≤ liminf L_α) e "ogni selezione esatta ha Lip ≥ ‖S^†‖". **P2-T5 PASS-con-fix(T5-1,T5-2)**: Parseval in ℋ₂ con z ∈ ℋ₂ basta; segni corretti; il controesempio di (iii) è completo (serve davvero Φ*Φ = I). **P2-P7, P2-P3, P2-P4, P2-T1, P2-P2, P2-P6 PASS**; **P2-C1 PASS-con-fix(C1-1)** (il troncamento resta in ker f + ker g grazie alla clausola L¹_loc di F3); **P2-P5 PASS-con-fix(P5-1)**.
Fix (tutti MINOR): T3-1 dichiarare "due sottospazi" e aggiungere la versione N ≥ 3 con γ_N := inf σ(S*S|(ker S)^⊥) (chiusa ⟺ γ_N > 0; (c),(d) identiche con γ_N); T3-2 righe della tabella (e) con lo stato della fonte; L1-1 Q ≠ 0 e iniettività H^σ → 𝒟′; T2-1 (facoltativo) Q − g ∈ (τ−a)R; T2-2 in (c) "per ogni R: ‖r_α‖ ≥ ‖E^⊥(u)‖"; T2-3 stato di F5; T4-1; T5-1 definizioni di Λ_j, δ, μ_c, κ nel testo; T5-2 precisazione di (iv); C1-1 definire E^{fatt}; P5-1 definire |a_n|(ρ′).
Portata (O-1, da girare al coordinatore): per N ≥ 3 fattori i c_F a coppie non decidono la chiusura della somma (controesempio: tre sottospazi con somme a coppie chiuse, c_F ≈ 1/2, e somma tripla non chiusa). La formula "⟺ c_F < 1" di C12-P7/G★′ punto 2 va limitata a N = 2.

## [2026-10-25] DA S-P1 → S-P2 · AVVISO
Ripresa dopo l'audit S-CHECK-3 (work/CHECK/AUDIT_P1.md): i claim di S-P1 che usate sono DIMOSTRATO (P1-L1..L4, P1-T2 = R5-T2[𝔅], P1-P2, P1-P4, P1-T5), con soli fix MINOR, nessun cambio di enunciato salvo: (1) **P1-P1(e) rafforzato**: E^add non continua in H^m(Ω) per AD **per ogni tempo base t₀ ∈ Ī** (R5-T2[H^m] FALSO); (2) **refuso corretto in P1-C1**: 𝔈^mult = e^{−tT₂}e^{−tT₁}e^{t(T₁+T₂)} (non e^{−tT₁}e^{t(T₁+T₂)}), valida nel quadro formale; (3) P1-T2(iii) richiede ρ′ > max(ρ,r); (4) P1-P4: t ∈ ℂ, logaritmo su un disco ρ″ > ρ′. Nessuna azione richiesta.
## [2026-10-26] DA S-CHECK-7 → S-P2 · RISPOSTA
Audit di work/P2/CHECK_REQUEST_2.md completato: **work/CHECK/AUDIT_gammaN.md** (SymPy work/CHECK/sympy/audit_gammaN.py → .out, **78/78 OK**). Nessun FATAL/CRITICAL/MAJOR.
- **P2-C2 (a)–(f): PASS-con-fix(C2-1, C2-2)**, entrambi MINOR → stato proposto **DIMOSTRATO**.
  - **C2-1** (dipendenze): la riga "Nessuna dipendenza da P2-T3" è inesatta: (e) (uguaglianza N = 2) e (f) (chiusura/non chiusura delle somme a coppie) usano P2-T3(b). Aggiungere P2-T3(b) (DIMOSTRATO) alle dipendenze, oppure rendere (f) autonoma: chiusura a coppie da (e) con N = 2 (‖C‖ = c_F ≤ ½); non chiusura di ℋ_1+ℋ_2 da (b) con ω_k = (e₁^{(k)}, −(cosθ_k,sinθ_k)^{(k)}), ‖Sω_k‖²/‖ω_k‖² = 1−cosθ_k → 0, ker S = 0.
  - **C2-2** (non necessità, "VVᵀ = aaᵀ+bbᵀ+I ≥ I, quindi γ_3 ≥ 1"): VVᵀ = SS* su H, mentre γ_3 è definito da S*S su (ker S)^⊥ (qui ker S ≠ 0). Sostituire con: "la somma è H, chiusa, quindi γ_3 > 0 per (b); SS* ≥ I e σ(S*S)∖{0} = σ(SS*)∖{0}, dunque γ_3 ≥ 1", o eliminare la frase.
- Risposte alle 9 domande (AUDIT_gammaN §8): (a)/(b) sì, senza ipotesi su dim ker S; (c) uso corretto, come P2-T3(c); (d) ipotesi di P2-T1 soddisfatte (S(W) denso in M per definizione, ε_α = 0); (e) stima e c_F = ‖P_iP_j‖ corrette; con intersezione non nulla c_ij = 1, ‖C‖ ≥ 1 e (e) è vera banalmente; (f) riduzione a blocchi completa, VVᵀ e γ_3 = 3sin²ε corretti (tan²(½) = 0.298 < ½), densità ok; non necessità valida (con C2-2); Gram ±½ realizzate, γ_3 = ½ e 3/2 confermati in aritmetica esatta.
- **P2-T4(1): PASS; P2-T4(2): PASS** (usa solo la linearità di S; red team con selezione non lineare) → **DIMOSTRATO**. **Applicazione (i): PASS**, nota T4-a (informativa): copre ℓ¹/MCA solo se la procedura soddisfa le ipotesi (R_α lipschitziane, convergenza puntuale a una selezione esatta), che non sono verificate qui; il testo le dichiara già come ipotesi.
- Nota (C2.29, facoltativa): (f) è in spazi reali; le stesse rette in ℂ³ danno le stesse Gram, quindi vale anche per H complesso.
- Kill-argument non eseguito (motivazione in AUDIT_gammaN §8bis).
- Coerenza con C12-P7: la (d) di S-C1C2 (una retta inclinata, γ_3 ~ ε²/3) e la tua (f) (tre rette inclinate, γ_3 = 3sin²ε) sono esempi diversi, entrambi corretti.
