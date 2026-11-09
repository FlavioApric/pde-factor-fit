# VERDETTO — F6-DICT (hub) · dizionario universale filtrato 𝓓_∞ · 26/10/2026
Criteri fissati in PLAN.md prima della ricerca. Prove: NOTE.md. SymPy: sympy/dict_checks.out **32/32 OK** (solo verifiche). Stati: prova scritta = prova completa NON auditata; nulla è DIMOSTRATO. Skill caricate: session-protocol, route-scout, claim-lifecycle, novelty-check (fasi A, B), math-skill (proof). Niente ML.

## Risposta alla domanda dell'utente, in una frase
**Sì, si può costruire un dizionario numerabile, esplicito e filtrato 𝓓_∞ = ∪𝓓_n che "tiene conto di tutto"**, ma solo nel senso di **approssimazione in una topologia dichiarata per ogni classe, più certificato di misfit livello per livello e identificazione nel limite**. È **falso** (teorema N1) che un dizionario qualsiasi dia rappresentazione esatta o identificazione esatta universale da una soluzione. Inoltre, nella classe "per tutto" ogni u ha banalmente una legge (N1(vi)): il contenuto sta nella **filtrazione**, non nella chiusura — conferma precisa dell'osservazione dell'utente sullo spazio di Hilbert.

## Enunciati candidati (forma più forte vera trovata)
| ID | enunciato | ipotesi | topologia / confine | stato |
|---|---|---|---|---|
| **U1** | 𝓓^{loc} = {χ_j y^β∂^α} denso fra i locali lineari; **N0**: i soli polinomi y^β∂^α bastano ⟺ ordine globale finito | T lineare, supp Tu ⊆ supp u, C^∞→C^∞ (Peetre: nessuna continuità richiesta) | τ₁ (coeff. in C^∞ sui compatti); velocità ρ^{−n} (analitici), n^{−s} (C^s); singolari: solo C^m→L^p + atomi |x−x₀|^{−j} | prova scritta; Peetre CON-FONTE verificata (Math. Scand. 7 (1959) 211–218; 8 (1960) 116–120; KMS §19.1) |
| **U2** | polinomi in (y, J^r u) densi vicino a ogni f, uniformemente su compatti di getti; sin u, e^u solo sui compatti, esatti con atomi e^{iku}, e^{λu} | D locale regolare (Slovák, Ann. Global Anal. Geom. 6 (1988) 273–283; KMS Thm 19.7 e §19.10, letti) | ordine localmente finito anche nel getto (controesempio Σψ_k(u)∂^ku) | prova scritta mod liscezza di F (KMS 18.16) |
| **U3** | (a) nuclei di Schwartz: denso in senso bilineare debole; (c) simboli: denso in **norma** H^s→H^{s−m′} per ogni m′ > m; **N2**: impossibile con m′ = m (S^m non separabile, blocchi diadici); (d) memoria completamente monotona = limite di **sistemi locali aumentati** (somme di esponenziali, velocità log); **N3**: ritardo NON nella chiusura in norma dei sistemi locali ⇒ atomo T_τ | p ∈ S^m; k c.m.; τ > 0 | vedi colonna | prova scritta (numeri Hörmander da verificare) |
| **U4** | componente per componente su Mat_k; razionali e memoria esponenziale ⊂ sistemi locali | — | gauge: F6-SYS | prova scritta (parte strutturale a F6-SYS) |
| **U5** | polinomi di funzionali lineari densi in TUTTI gli operatori continui, uniformemente sui compatti di dati | X, Y Fréchet separabili | nessuna velocità | prova scritta; **noto** (Prenter 1970, Chen–Chen 1995, Boyd–Chua 1985) |

## Teoremi negativi (il confine)
- **N1(i)** (Baire): per ogni dizionario numerabile, anche con finiti parametri continui per atomo, gli operatori rappresentabili esattamente sono **magri** in ogni classe che contiene un F-spazio infinito-dimensionale (coeff. C^∞, non linearità C^∞, S^m, nuclei L²).
- **N1(ii)**: nessun dato finito certifica l'identificazione (C3-P1, P4-T5); **Teorema A**: misfit al livello n è aperto e finitamente certificabile (Σ₁), fit è chiuso e raro (non certificabile da dati approssimati).
- **N1(iii)**: per dati in forma chiusa (EP) l'identificazione modulo conseguenze fallisce a tutti i livelli alti (non monotonia; esempio esatto e^{−t}sin x).
- **N1(iv)**: uscita finita ⇒ al più numerabili operatori ⇒ solo "nel limite"; e (CONV-T2, F6-CONV) Ann(u) = 0 vs ≠ 0 non è decidibile nel limite **da nessuna regola, nemmeno non continua**.
- **N1(v)**: la u generica non soddisfa alcuna equazione di 𝓓_∞ (Weyl intera, polinomi differenziali inclusi).
- **N1(vi)** (elementare, decisivo): L_{u,i} = u∂_i − ∂_iu annulla ogni u ⇒ con coefficienti C^∞(t,x) **ogni u ha una legge e nessun operatore è identificato**. **Tricotomia**: classe troppo grande (legge banale) / classe numerabile-dimensionale (u generica senza legge, identificazione esatta per livello) / classi compatte (identificazione nel limite, I-LIM).

## D2–D4 e convergenza
- **Certificato di misfit** (prova scritta): formula della distanza di Hahn–Banach; Gram (r_n² = rapporto di determinanti, φ = residuo/‖residuo‖); **forma debole**: det(⟨u, D_i^tψ_j⟩) ≠ 0 con ψ da un insieme numerabile — solo integrali di u, robusto (σ_min(A(ũ)) > ‖δ‖_F), semi-decidibile; min–max (Sion) per coefficienti limitati, Farkas per coni.
- **Migliore approssimazione** (prova scritta): proiezione; stima a posteriori |c_n − c̃_n| ≤ 2η/√λ_min(G′_n); velocità per regolarità; n-larghezze ⇒ polinomi ottimali d'ordine per coeff. C^s (fonte da verificare).
- **Regole di arricchimento**: altezza; livello minimo + coerenza con le conseguenze (S4-ID P-a); **guadagno esatto di un atomo dal certificato** gain(D) = r_n²|φ_n(Du)|²/‖P^⊥Du‖² (criterio OLS, prior art); diagnostica di famiglia (potenza → |D|^s, esponenziale → memoria, fase → ritardo, picco → singolare); D4-ENC (quadro libero via operatore di trasformazione, da F6-ENC); **arresto: R-STOP = CONV-T5** (concordato con F6-CONV), Lepskii solo nel regime di approssimazione. Teorema G-R: si ferma esattamente al livello giusto sotto l'ipotesi ID, tempo non maggiorabile.
- **I-LIM** (concordato con F6-CONV): ramo esatto CONV-T1 + ramo approssimato (prova scritta): su 𝒦_R compatto con unicità (H1) e approssimazione limitata (H2), i minimizzatori convergono con modulo ω (lemma di Tikhonov) anche con rumore; Hölder con un coefficiente e |u_x| ≥ γ.

## Domanda guida (I/S/E)
- **(I) sì relativa al livello / parziale per la classe universale**: C3-L1/T1/T6 per livello, S4-ID P-a = regola di coerenza, P4-T2 spiega il fallimento, I-LIM il limite. Costo O(N_n³) per livello.
- **(S) parziale con ostruzione S-O1** (prova scritta): i polinomi riducibili sono rari ⇒ la struttura fattoriale non è stabile sotto approssimazione (τξ + ε irriducibile); C12-T1′ solo dopo identificazione esatta.
- **(E) parziale**: convergenza di E_int^add per L_n → L via Trotter–Kato (candidato); non continuità in u (P1-P1(e)) resta.

## Novità (novelty-check A+B; C omessa: Codex non disponibile)
3/10 per U1–U5 (ingredienti classici; nessuna fonte trovata che leghi Peetre/Slovák alla completezza dei dizionari di identificazione); 5/10 per il pacchetto di confine N0 + N1(v),(vi) + N2 + N3 + Teorema A (da confermare con ricerca estesa); 4/10 per I-LIM. **PROCEED WITH CAUTION.** Prior art chiave: Weak SINDy (forma debole come stima), OLS (R3), Chen–Chen/Boyd–Chua (U5), Gold 1967.

## Raccomandazioni (criteri del PLAN)
| sotto-strada | esito | motivo |
|---|---|---|
| U1 (+N0) | **PROMUOVI** | P1 (Peetre verificato), P2, P3 via lemma di confine N0 |
| U2 | **PROMUOVI (forma locale)** | Slovák verificato; serve S-CHECK sulla liscezza di F |
| U3-a nuclei | **PARCHEGGIA** | vero ma topologia debole senza stime (criterio b) |
| U3-c simboli + N2 | **PROMUOVI** | confine netto (perdita ε necessaria e sufficiente) |
| U3-d memoria / N3 ritardo | **PROMUOVI** | velocità e riduzione a sistemi locali; N3 come lemma negativo |
| U4 | **PROMUOVI subordinata — MERGE-INTO F6-SYS** | struttura algebrica e gauge lì |
| U5 | **PARCHEGGIA** | noto, senza velocità (criterio c) |
| N1(i)–(vi) | **PROMUOVI** (cammino critico, kill-argument richiesto) | è il confine richiesto dal piano |
| D2 misfit, D3 B2, D4 regole | **PROMUOVI** | certificati calcolabili, stime esplicite |
| I-LIM | **PROMUOVI — MERGE con CONV-T1** | teorema comune con F6-CONV |
Nessuna sotto-strada ELIMINATA (nessuna richiede ML; gli enunciati universali falsi sono sostituiti dalle versioni vere più deboli con i loro teoremi negativi).

## Costo
S per U1, N0, N2, N3, N1, M, B2 (prove di 1–2 pagine, audit S-CHECK); M per U2 (verifica di KMS 18.16 nel caso con intorno V) e I-LIM con (H2) via approssimazione simultanea; M per la verifica delle fonti di CIT-AUDIT (Hörmander I 4.2/5.2, III 18.1.13; Pinkus; Bagby–Bos–Levenberg; Engel–Nagel).
