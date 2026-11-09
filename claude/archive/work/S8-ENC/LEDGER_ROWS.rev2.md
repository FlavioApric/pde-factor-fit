# LEDGER_ROWS — S8-ENC · rev. 2 dopo S-CHECK-F8-ENC · 27/10/2026

Righe proposte per `claims/LEDGER.md`, da applicare a cura di central.

**Come leggere gli stati.**
- "DIMOSTRATO (proposto da S-CHECK)": verdetto di `work/CHECK-F8/AUDIT_S8-ENC.md`; la registrazione spetta a central.
- "DA AUDITARE": claim nati nel recepimento, senza S-CHECK.

Abbreviazioni:
- PP = `work/S8-ENC/PROOF_PACKAGE.md` (rev. 2);
- AUD = `work/CHECK-F8/AUDIT_S8-ENC.md`;
- KA = `work/CHECK-F8/KA_ENC_{N1,P0}_adjudication.md`.

| ID | enunciato (1 riga) | ipotesi | stato | prova (file#sezione) | SymPy (script, esito) | proof-checker | kill-argument | dipende da |
|---|---|---|---|---|---|---|---|---|
| ENC-D | encoder strutturato: (E1) dim ker W < ∞ su 𝒴, (E2′) W L_q = (L_0 + c)W, (E3) esplicito | — | DEFINIZIONE | PP#1 | — | AUD OK (+ENC-14) | — | NOTAZIONE v5 |
| ENC-K0 | q ≡ c ≠ 0 non ha intertwiner differenziale stretto di nessun ordine; con (E2′) W = I | J intervallo, w_j ∈ C^∞ | DIMOSTRATO (proposto da S-CHECK) | PP#1 | enc_algebra 6/6, enc_s8b 2/2 | AUD OK | — | — |
| ENC-1 | Volterra simmetrico T = I + ∫_{−x}^{x}K: L_qT = TL_0 su C²(J), conserva i dati di Cauchy, biiettivo su C, C², C^∞; stima, stabilità Lipschitz; dipende da x_0 | J = [x_0 − a, x_0 + a], q ∈ C¹(J; ℂ) | DIMOSTRATO (proposto da S-CHECK); CON-FONTE Marchenko 1986 cap. 1 solo come confronto | PP#2 | enc1_goursat 11/11; AUD E1a–E1d, E6 | AUD OK (ENC-8 MINOR applicato) | AUD §3: non toccato | — |
| ENC-U1 | intertwiner nella classe Volterra simmetrica = retta {T_{k_0}}; unico che conserva Cauchy: k_0 = 0 | come ENC-1 | DIMOSTRATO (proposto da S-CHECK) | PP#2 | enc1_goursat 3/3, enc_recep 1/1 | AUD OK (ENC-7 applicato: B = −2 d/dx K(x, −x)) | — | ENC-1 |
| ENC-C1 | P(∂_t, L_q)u = 0 ⟺ P(∂_t, L_0)(Wu) = 0 per ogni P ∈ S | ENC-1, q ∈ C^∞, u ∈ C^∞(I × J°) | DIMOSTRATO (proposto da S-CHECK) | PP#2 | — | AUD OK | — | ENC-1 |
| ENC-T2 | a q noto: Ann_q(u) = φ^{−1}(Ann(Wu)); generatore lcm(Q, Q̃) o ξ·lcm; getti in x_0 triangolari unipotenti; solo sottoanello pari; non è uno strumento di B1 | DM3, Ω = I × J° simmetrico, q dato | DIMOSTRATO (lemma; proposto da S-CHECK) | PP#3 | enc_algebra 6/6, enc_s8b 2/2 | AUD OK (ENC-6 applicato) | non toccato | ENC-C1, C3-T1 |
| ENC-T2(c′) | in ogni punto (t_1, x_1), nessun getto finito certifica Ann_q(u) = (P_*) ≠ 0 | q ∈ C^∞, P_* ≠ 0 | PROVA SCRITTA — DA AUDITARE | PP#3 | enc_recep 1/1 | — | — | — |
| ENC-P0(a) | W ∈ 𝔈 soddisfa (INT) ⟺ W(t) = U_0(t)W(0)U_V(t)^{−1} | (H-P0) | DIMOSTRATO sotto (H-P0) (proposto da S-CHECK) | PP#4 | — | AUD OK (ENC-15 applicato) | KA P0: SURVIVES | VAR-P11(a)–(d); VAR-P11(e) CON-FONTE |
| ENC-P0(b) | W indipendente da t, dim ker W < ∞ su L²(J), intreccia ⇒ V(t) − V(s) = c(t) − c(s); non copre gli encoder di Volterra | H_0 autoaggiunto su L²(J), V(t) ∈ L^∞ | DIMOSTRATO (proposto da S-CHECK) | PP#4 | — | AUD OK, portata con ENC-4, ENC-14 | KA P0: SURVIVES | — |
| ENC-P0(b)^cl | versione classica: W su C^∞(J), nucleo finito, intreccia su C^∞_c ⇒ V(t, x) − V(s, x) = c(t) − c(s); copre ENC-1 | V ∈ C(I × J), c ∈ C(I) | PROVA SCRITTA (testo del revisore) — DA AUDITARE | PP#4 | — | — | — | — |
| ENC-P0(b)^loc | W con nucleo finito su C^∞_c(U) che intreccia lì ⇒ V(t, ·) − c(t) autonomo su U | U ⊂ J aperto | PROVA SCRITTA — DA AUDITARE | PP#4 | — | — | — | ENC-P0(b)^cl |
| ENC-P0′ | forma normale: soluzioni → soluzioni libere riparametrizzate su un nucleo denso D_0 ⇒ W(t) = U_0(θ(t))W(0)U_V(t)^{−1}; θ non è invariante (W_id) | H_0 autoaggiunto, D_0 denso (per lente e Avron–Herbst D_0 = 𝒮(ℝ)) | astratto: DIMOSTRATO (proposto da S-CHECK); versione su nucleo denso ed esempi su 𝒮 — DA AUDITARE | PP#4 | enc_algebra 3/3, enc_recep 1/1 | AUD OK astratto (ENC-3 applicato) | KA P0: SURVIVES | Reed–Simon II (ess. autoagg. su 𝒮), Mehler CON-FONTE |
| ENC-P0′-DIC | V = α(t)x² + β(t)x + γ(t): rappresentante puntuale + gauge con θ = id ⟺ α ≡ 0 | V reale, ansatz puntuale + gauge | DA AUDITARE (dal KA P0 P1; sistema rifatto dal revisore) + CON-FONTE Bluman–Shtelen 1996 §2 | PP#4 | enc_recep 1/1 (θ = id per β(t)x) | — | — | Bluman–Shtelen 1996 |
| ENC-P0-sintesi (rev. 1) | "le eccezioni cambiano il tempo" | — | **FALSO come scritto** (Avron–Herbst, V = β(t)x: θ = id) | PP#4 | enc_recep 1/1 | AUD ENC-2 | KA P0: KILLED | — |
| POLE-N | intertwiner istantanei con V(t) che evolve non sono encoder per Schrödinger; servono solo al flusso di Lax | hilbertiana: (H-P0), 𝔈, nucleo finito | DIMOSTRATO dopo ENC-4 (proposto da S-CHECK) | PP#4 | — | AUD OK | KA P0: SURVIVES | ENC-P0(b) |
| POLE-N^cl | versione classica: W(t) differenziale con poli, intrecciamento istantaneo e in i∂_t ⇒ V autonomo modulo c | coefficienti C^∞ fuori dai poli | PROVA SCRITTA (testo del revisore) — DA AUDITARE | PP#4 | — | — | — | ENC-P0(b)^cl |
| ENC-N1 (F6) | "encoder cieco ⟺ Φ(V, v) = W_V^{−1}v iniettiva" | come in F6-ENC | FALSO (testimone: ENC-N1′(iv)) | PP#5 | — | AUD OK | KA N1: FALSO confermato | — |
| ENC-N1′ | lemma di riduzione per una famiglia fissata: cieco ⟺ (C); identificabilità ⇒ (C); (C) ∧ (S) ⟺ identificabilità (per definizione); (iv) cieco senza identificabilità; (v) dipendenza dalla famiglia; lettura: cieco ⟺ identificabilità modulo gauge | quadro PP#5 rev. 2 (classi [𝒮_V], N_V, ≈) | DIMOSTRATO come lemma di riduzione (proposto da S-CHECK) | PP#5 | enc_recep 1/1 per (v) | AUD OK (ENC-5, ENC-13 applicati) | KA N1: SURVIVES come lemma | VAR-T1(b) (SF, VAR-1, VAR-L1), ENC-P0(b), ENC-1(6) |
| ENC-K1′ | W differenziale con W L_q = (L_0 + c)W ⇒ su ogni componente di J ∖ Z (Z chiuso numerabile) W = w_nA_n⋯A_1, catena di Darboux da c; viceversa (Crum) | q ∈ C^∞(J; ℂ) | DIMOSTRATO dopo ENC-9 (proposto da S-CHECK); probabilmente noto (Andrianov–Sokolov 2003) | PP#6 | enc_algebra 5/5, enc_s8b 2/2 | AUD OK | — | — |
| ENC-K1 | V razionale, V → 0: esiste W differenziale ⟺ V è un Darboux iterato di 0 (Adler–Moser) | V razionale, V → 0 all'∞ | CON-FONTE da verificare (Duistermaat–Grünbaum 1986) | PP#6 | — | AUD: declassamento confermato | — | — |
| ENC-TAB | tabella unica degli encoder (sostituisce SYNTHESIS-2 §3); riga "puntuale + gauge" corretta: dipendente dal tempo, θ ≠ id ⟺ α ≢ 0 | — | SINTESI | PP#6 | — | — | — | ENC-1, K0, K1′, P0′, FAD-1 |
| ENC-A9(a) | ‖E^mult f‖ ≤ (t²/2)(‖V″‖‖f‖ + 2‖V′‖‖f′‖) + (2t³/3)‖V′‖²‖f‖, costante 2/3 ottimale; E^mult/t² → ½[H_0, V]; E^mult ≡ 0 ⟺ V costante | V ∈ W^{2,∞}(ℝ) reale, f ∈ H¹ | DIMOSTRATO (proposto da S-CHECK) | PP#7 | enc_s8b 2/2, eint_closed 2/2, enc_recep 1/1 | AUD OK | — | — |
| ENC-A9(b) | forme chiuse: V = c; V = Fx (Strang esatto più fase, ‖E^mult f‖ ≤ \|F\|t²‖f′‖ + (2/3)F²t³‖f‖, norma 2); nucleo erfc per Pöschl–Teller | come in PP#7 | DIMOSTRATO (proposto da S-CHECK); la stima di (b2) della rev. 1 è FALSO; (b3) = VAR-T10; formula di (b4) = VAR-P8(c) | PP#7 | eint_closed 21/21, enc_s8b 4/4, enc_recep 3/3 | AUD ENC-1 applicato | — | VAR-T10, VAR-P8(c) |
| NS-EQ-Ω | Avron–Herbst e lente su Ω limitato: dominio deformato (semplicemente connesso; lente non convessa, stellata se 0 ∈ I), Neumann → Robin, I/S sì nell'anello coniugato (coefficienti in (t, x)), E no; incollamento esatto della lente | Ω = I × J rettangolo | DIMOSTRATO dopo ENC-10 (proposto da S-CHECK) | PP#8 | enc_s8b 5/5, enc_recep 2/2 | AUD OK | — | C3-T1, C12-T1′ |
| FAD-1 | Faddeev su intervallo a λ fissato: Neumann convergente senza piccolezza, componenti esatte, E^add = Σ_{i≠j}G_0V_iG_0V_ju^{(0)} + R, ‖R‖ ≤ (Cℓ𝐕)³e^{Cℓ𝐕}‖u^{(0)}‖/3 con 𝐕 = Σ‖V_i‖ | J limitato, V_i ∈ C(J) | DIMOSTRATO dopo ENC-11 (proposto da S-CHECK) | PP#9 | enc_s8b 3/3 | AUD OK | — | — |
| GAM-O1 | gamblets: scomposizione (S) per scala L_q-ortogonale, non encoder | L_q coercivo su H¹_0 | OSSERVAZIONE + CON-FONTE (Owhadi 2017) | PP#9 | — | — | — | — |
| FW-1 | Foldy–Wouthuysen esatto per Dirac 1+1 libero (moltiplicatore non razionale, non locale); con V solo asintotico: scomposizione (S) | m > 0 | DIMOSTRATO per il libero (proposto da S-CHECK); con V CON-FONTE (Thaller cap. 5) | PP#9 | enc_s8b 3/3 | AUD OK | — | II-T3 |
| ENC-L1 | — | — | FUSO in VAR-P8(a) (R5-P7) | — | — | — | — | VAR-P8 |

**Errata da registrare per F6.** F6-ENC NOTE §5 (riga 47), Avron–Herbst: la formula vale per H = −½∂² + Fx. Nella normalizzazione del progetto vale u = e^{−iFtx − iF²t³/3}v(t, x + Ft²), e lo stesso per l'encoder inverso (AUD ENC-12).
