# LEDGER_ROWS — S8-DICT (27/10/2026, aggiornato dopo l'audit)

Queste righe sono proposte nel formato LEDGER. Il LEDGER non è stato toccato: lo integra il coordinatore.

Gli stati sono quelli proposti da S-CHECK-F8-DICT (`work/CHECK-F8/AUDIT_S8-DICT.md` §0), dopo il recepimento dei fix DICT-1 … DICT-18 (elenco in `RECEPIMENTO.md`). "DA AUDITARE" marca il testo nuovo, nato dal recepimento, che l'audit non ha scritto.

**Post-Gate 8 (27/10/2026).** Recepiti `work/CHECK-F8/AUDIT_S8-DICT_rev2.md` (MAG-1…MAG-5), `research/DEVIL/ATTACK-8.md` (O5, O13, O15, O19) e `research/CIT-AUDIT/AUDIT-8.md` §5. Elenco in `RECEPIMENTO.md`, sezione "post-Gate 8". Gli stati in questa versione sono cambiati solo verso il basso: DICT-AX scende a "CON-FONTE da leggere"; DICT-RANGO e DICT-RANGO-cor valgono come ID-ker sotto (H-ex); DICT-MAG-NU non è più un claim autonomo, è un corollario di SYS-N3(c).

Abbreviazioni:
- PP = PROOF_PACKAGE.md.
- KA-ind = kill-argument indipendente `work/CHECK-F8/KA_DICT_N1_*`, esito SURVIVES-WITH-FIXES.
- dc = `work/CHECK-F8/sympy/dict_check.py` (18/18 PASS).
- c1, c2, c3 = `sympy/s8dict_checks{,2,3}.py` (27/27, 12/12, 9/9 OK).

| ID | enunciato | ipotesi | stato | prova | SymPy | proof-checker | kill-argument | dipende da |
|---|---|---|---|---|---|---|---|---|
| DICT-U1 | Ogni operatore lineare locale continuo è limite di elementi di 𝓓_∞ (LIN, LOC); vale N0 | Peetre; ordine localmente finito | DIMOSTRATO | PP §1.1 | c1 A* | S-CHECK-F8-DICT: OK | — | Peetre (KMS 19.1, verificata) |
| DICT-U1b | Classi di coefficienti: singolari e densità L^p; velocità 2–3 | — | singolari e L^p DIMOSTRATO; velocità CON-FONTE da verificare | PP §1.1 | — | S-CHECK-F8-DICT | — | Jackson, Bagby–Bos–Levenberg |
| DICT-U2 | Densità dei polinomi differenziali per operatori non lineari regolari; F liscia, dipendente da (f, K); U2-a = versione locale di KMS 18.16 sull'intorno di 19.10 | U2-a, 𝒲 aperto | DIMOSTRATO | PP §1.2 | — | S-CHECK-F8-DICT: OK con DICT-12; CIT-AUDIT-8 §5 (1, 5) | — | KMS 19.10 (verificata), Slovák, Boman, Math. Scand. 20 (1967) 249–268, DOI 10.7146/math.scand.a-10835 (enunciato CON-FONTE) |
| DICT-N2 | S^m non è separabile | — | DIMOSTRATO | PP §1.3 | — | S-CHECK-F8-DICT: OK | — | — |
| DICT-U3c | Densità dei simboli con perdita ε | moltiplicatori | DIMOSTRATO; caso dipendente da x CON-FONTE | PP §1.3 | — | S-CHECK-F8-DICT: OK | — | Hörmander 18.1.13 (da verificare) |
| DICT-U3d | Memoria c.m.: (i) rappresentazione diffusiva esatta, (ii) convergenza L¹ con nodo λ = 0 esatto, (iii) velocità uniforme in t per t^{−β} | Bernstein | DIMOSTRATO ((ii) dopo DICT-4) | PP §1.4 | c2 F5, F5b; c3 R1; dc B1, D1 | S-CHECK-F8-DICT: OK con DICT-4 | — | Trefethen–Weideman 2014, Thm 5.1 CON-FONTE non letta (CIT-AUDIT-8 §5 (4)); bordo verificato numericamente |
| DICT-U3d-v | Velocità per nuclei c.m. generali | — | CANDIDATO | — | — | — | — | — (Q1) |
| DICT-RIT1 | Il ritardo equivale al trasporto w_t + w_θ = 0 (sistema aumentato) | τ > 0 | DIMOSTRATO | PP §1.5 | — | S-CHECK-F8-DICT: OK | — | — |
| DICT-N3 | Distanza 1 su ℝ e ≥ 1 su (0,T) del ritardo dal dizionario locale | ristretto (fix F4) | DIMOSTRATO | PP §1.5 | c2 F4; dc I1 | S-CHECK-F8-DICT: OK | — | — |
| DICT-CS1 | Estensione CS con c_s = 2^{1−2s}Γ(1−s)/Γ(s) | s ∈ (0,1) | DIMOSTRATO | PP §1.6 | c2 F6, c1 A4; dc C1 | S-CHECK-F8-DICT: OK | — | — |
| DICT-U4 | Estensione ai sistemi per componenti | — | DIMOSTRATO | PP §1.7 | — | S-CHECK-F8-DICT: OK | — | S8-SYS |
| DICT-N1 | (i) Baire, (ii) nessun dato finito certifica il fit, (iv)(a) modello (T) | DM; (T)/(BSS) | DIMOSTRATO | PP §2.1, 2.2, 2.4 | — | S-CHECK-F8-DICT: OK con DICT-14 | KA-ind: SURVIVES-WITH-FIXES | C3-P1, P4-T5, C3-T4 |
| DICT-N1iii | Non monotonia: Ann(u) ∩ R_{≤n} ⊋ (L) ∩ R_{≤n} | N ≥ 2, **L ∈ Ann(u)** | DIMOSTRATO dopo DICT-6 | PP §2.3 | c1 B1, c2 F10; dc F1 | S-CHECK-F8-DICT: CRITICAL formale riparato | KA-ind P5 | C3-L3 |
| DICT-N1iv-bc | (b) BSS stabilizzazione esatta; (c) "Ann ≠ 0" verificabile ma non decidibile nel limite | DM2 | DIMOSTRATO (come in AUDIT_S8-CONV) | PP §2.4 | — | S-CHECK-F8-DICT: OK con DICT-15 | KA-ind P9 | CONV-T1, CONV-T2 |
| DICT-N1v | Le u con una legge nel dizionario formano un insieme magro e shy; (v)-ALG: le u differenzialmente algebriche formano un insieme magro e shy (denso, non raro) | Lemmi ND, ND-NL | DIMOSTRATO | PP §2.5 | c2 F1, F2, F10 | S-CHECK-F8-DICT: OK con DICT-16 | KA-ind P11 | MF3(a), Christensen, Israel J. Math. 13(3–4) (1972) 255–260 (CIT-AUDIT-8 §5 (3)); HSY (definizioni standard) |
| DICT-RANGO | (I)–(III) struttura, identificabilità nel significato **ID-ker** (ker Φ_u = 0), non falsificabilità | ID-ker dà l'unicità solo sotto **(H-ex)** (una legge esiste); controesempio u = t + sin x in u_t = a u_xx + b u (a, b costanti) | DIMOSTRATO come ID-ker | PP §2.6 | c2 F11 | S-CHECK-F8-DICT: OK; ATTACK-8 O5 | KA-ind | VAR-T1(a) |
| DICT-RANGO-cor | (IV) conteggio, (a′) con d ≥ 1 o m ≥ 2, (b′) V complesso e V reale ("⟺" solo per u senza zeri), trasporto a(t,x) | identificabile := ker Φ_u = 0 (ID-ker); unicità solo sotto (H-ex) | DIMOSTRATO dopo DICT-2, DICT-3, come ID-ker | PP §2.6 | c1 B3, B4; dc G1 | S-CHECK-F8-DICT: CRITICAL formali riparati; ATTACK-8 O5 | KA-ind P1, P2, P3, P10 | VAR-N1, VAR-T1(c) |
| DICT-MAG | Il caso magnetico esce da RANGO. Per B con supp B ⊂ {u ≠ 0}: le leggi reali (A, V) e (A + B, V + δV) coesistono ⟺ div_x(\|u\|²B) = 0; se supp B incontra Z(u) servono due condizioni in più (MAG-3), non trattate | n ≥ 2; A, V ∈ C^∞(J × Ω; ℝ) dipendenti da (t, x) (MAG-1) | rinviato a SYS-N3, riga canonica (O15) | PP §2.6 | c3 R3 | S-CHECK-F8-DICT: MAJOR riparato (DICT-5); rev2: MAG-1, MAG-3 | KA-ind P4 | SYS-N3 (S8-SYS) |
| DICT-MAG-NU | **Corollario di SYS-N3(c)**, non claim autonomo (O15): B = \|u\|^{−2}(∂_2χ, −∂_1χ, 0, …), χ ∈ C_c^∞(U) reale non nulla, U ⊂ {u ≠ 0} ⊂ J × Ω, dà una seconda legge reale con campo magnetico diverso (dB ≢ 0). Contenuto proprio rispetto a SYS-N3: u può avere zeri fuori da supp χ | n ≥ 2; A, V dipendenti da (t, x) (MAG-1); supp χ ⊂ {u ≠ 0}, u ≢ 0 (MAG-2); una legge reale esiste; caso statico solo per u stazionaria e χ = χ(x) | corollario di SYS-N3(c): nessuno stato autonomo. AUDIT_S8-DICT_rev2 propone DIMOSTRATO dopo MAG-1, MAG-2 (recepiti); qui lo stato non viene alzato, decide il coordinatore | PP §2.6 | c3 R3; CHECK-F8 dict2_mag.py 16/16 | AUDIT_S8-DICT_rev2: MAG-1…MAG-4 recepiti | — | SYS-N3(a)(b)(c) |
| DICT-N1vi | N1(vi) originale: "con coefficienti C^∞(t,x) nessun operatore è identificato; (H1) fallisce sempre" | — | **FALSO** | PP §2.6bis: controesempio u = t + x nella classe u_t = a(t,x)u_x (a ≡ 1 unica); u = t − x² falsifica la classe normalizzata | c3 R2; c1 B3d, B4 | S-CHECK-F8-DICT: "ritiro corretto, FALSO" | KA-ind | DEVIL-6 O1 |
| DICT-MF | MF1, MF2, MF3 (a)–(d), MF-C | — | DIMOSTRATO | PP §3.1–3.2 | c1 C3, A1, A2 | S-CHECK-F8-DICT: OK | — | Hahn–Banach, Weyl, Sion, Farkas |
| DICT-A | Teorema A (i)–(ii): misfit aperto con certificato finito (topologia D′ per atomi differenziali); fit chiuso con interno vuoto | — | DIMOSTRATO | PP §3.3 | — | S-CHECK-F8-DICT: OK con DICT-13 | KA-ind P7 | DICT-N1v |
| DICT-A-iii | Teorema A(iii): fit non certificabile con dati finiti esatti | atomi differenziali lineari a coefficienti lisci, indipendenti su Ω (**senza** ipotesi U_0) | DIMOSTRATO dopo DICT-1 | PP §3.3 | c2 F3; dc A1, A2 | S-CHECK-F8-DICT: MAJOR riparato | KA-ind P6 | Lemma ND, MF3(a) |
| DICT-B2 | Stima dei coefficienti con 2η/√λ_min | λ_min > 0 | DIMOSTRATO | PP §3.4 | c1 C1 | S-CHECK-F8-DICT: OK | — | — |
| DICT-B3 | Ottimalità d'ordine dei polinomi (n-larghezze) | — | CON-FONTE da verificare | — | — | — | — | Pinkus 1985 |
| DICT-R3 | Guadagno esatto di un atomo | — | DIMOSTRATO | PP §3.5 | c1 C2 | S-CHECK-F8-DICT: OK | — | prior art OLS |
| DICT-GR | Teorema G-R: R1 (test su r_n = dist(D_0u, W_n)) si ferma a n_0 sotto (H-ID); R2 segnala il fallimento | DM3 esatto, BSS; (H-ID): Ann(u) ∩ span 𝓓_n = ⟨L⟩_n per n ≥ n_0 | DIMOSTRATO | PP §3.5 | — | S-CHECK-F8-DICT: OK con DICT-7; ATTACK-8 O13 (etichetta) | — | P4-T5, CONV-T1 |
| DICT-R6 | Lemma R6-T: intrecciamento esatto W(Lu) = L̂(Wu); confronto di distanze e λ_min con ‖W‖, ‖W^{−1}‖ ≤ 1 + a²Q·e^{a√Q}; trasporto dei certificati ψ ↦ ψ∘W; (f) getti: triangolarità unipotente in (t, x_0), nessun dato finito certifica una legge (livello n e a nessun livello) | sottoanello pari ℂ[∂_t, L_q]; q dato; Ω rettangolo simmetrico attorno a x_0; Y = C(Ω̄) o L²(Ω); u ∈ C^∞ con D_iu ∈ Y; DM3 | (a)–(e) DIMOSTRATO (la condizione su ENC-1, ENC-C1 ed ENC-T2 è soddisfatta in AUDIT_S8-ENC). (f): DIMOSTRATO proposto dopo R6f-1, R6f-2 (AUDIT_S8-DICT_R6f, recepiti) | PP §3.6 | dc J1–J3; enc1_goursat, enc_algebra (S8-ENC) | S-CHECK-F8-DICT: OK con DICT-17, DICT-18; S-CHECK-F8-ENC: cammino ENC-1 → C1 → T2 → R6 regge; AUDIT_S8-DICT_R6f: PASS-con-fix, R6f-1 (triangolarità solo in (t, x_0)), R6f-2 (livello n e passo di Baire) | — | ENC-1, ENC-C1, ENC-T2(a)(b); (f) da DICT-N1(ii) e Teorema A (MAG-5, O19), non da ENC-T2(c)/(c′) |
| DICT-ILIM | I-LIM, ramo approssimato (a)–(d); ramo esatto = CONV-T1 (modello BSS) | (H0), (H-ID), (H2) | DIMOSTRATO | PP §4 | — | S-CHECK-F8-DICT: OK con DICT-8 | — | CONV-T1; Whitney–Stein (da verificare) per (H2) |
| DICT-ILIM-H0 | Modulo hölderiano per s = 0 | condizione del cono | DIMOSTRATO | PP §4 | c2 F8; dc H1 | S-CHECK-F8-DICT: OK | — | — |
| DICT-ILIM-Hs | Hölder per s ≥ 1 | — | CANDIDATO | — | c1 E1 | — | — | Gagliardo–Nirenberg |
| DICT-NS | NS-L1 (log globale: Ω semplicemente connesso o u modulo 2πi/λ), NS-T1 senza Ax; kink con nucleo 3; ALG-T1 solo per forme evolutive | esponenti commensurabili | DIMOSTRATO | PP §5.1–5.3 | c1 D1–D4, c2 F9; dc E1–E5 | S-CHECK-F8-DICT: OK con DICT-9, DICT-10 | — | ALG-T1 |
| DICT-2KINK | Il 2-kink ha nucleo 1 | — | V-ex | — | c2 F7 | — | — | — |
| DICT-AX | Ax–Schanuel differenziale | — | CON-FONTE **da leggere** (teorema differenziale non letto; prima "verificata") | PP §5.2 | — | S-CHECK-F8-DICT: DICT-11; CIT-AUDIT-8 §5 (2) | — | Ax, On Schanuel's conjectures, Ann. of Math. (2) 93(2) (1971) 252–268, DOI 10.2307/1970774 |
| DICT-R4, DICT-PAINLEVE | Strumenti euristici | — | STRUMENTO | PP §3.5, §5.4 | — | — | — | — |
