# RECEPIMENTO — audit S-CHECK-F8-ENC → S8-ENC · 27/10/2026

Fonti: `work/CHECK-F8/AUDIT_S8-ENC.md` (fix ENC-1…ENC-15), `KA_ENC_N1_adjudication.md`, `KA_ENC_P0_adjudication.md`.

Le severità sono quelle dell'aggiudicazione del revisore:
- CRITICAL: ENC-1 (locale) ed ENC-2 (formale);
- MAJOR: ENC-3, ENC-4, ENC-5, ENC-14;
- MINOR: gli altri.

Abbreviazioni:
- PP = `work/S8-ENC/PROOF_PACKAGE.md` (rev. 2; la rev. 1 è in `PROOF_PACKAGE.v1.md`);
- LR = `LEDGER_ROWS.md`;
- CR = `CHECK_REQUEST.md`;
- OQ = `open_questions.md`.

Il cammino critico ENC-1 → ENC-C1 → ENC-T2 → R6 di S8-DICT **non è stato indebolito**: ENC-1, U1, C1, T2(a)(b)(c) restano come prima, con le sole correzioni MINOR richieste (refuso B, norma HS, notazione Δ, nota sui domini non simmetrici).

| fix | severità | modifica | file / sezione |
|---|---|---|---|
| ENC-1 | CRITICAL locale | La stima di A9(b2) diventa ‖E^mult f‖ = ‖(1 − e^{i(Ft²p − 2F²t³/3)})f‖ ≤ \|F\|t²‖f′‖ + (2/3)F²t³‖f‖, con nota di correzione e controesempio (0.6549 > 0.1950). Ottimalità della costante 2/3 aggiunta ai commenti di A9(a). Nuovo script. | PP §7 (b2) e commenti di (a); PP §0 riga E_int; LR ENC-A9(a)(b); `sympy/enc_recep.py` test 1–4 |
| ENC-2 | CRITICAL formale | La sintesi "le eccezioni cambiano il tempo" è dichiarata FALSA e sostituita dal testo proposto dal revisore. §4 è riscritta: nuovo titolo, sintesi in testa, P0′ come forma normale (W_id, θ non invariante), dicotomia θ ≠ id ⟺ α ≢ 0, classe V = β(t)x + γ(t) con θ = id (verificata). Riga della tabella encoder corretta; §10.2 punto 4 allineato. | PP §4 (intera), §0, §6 tabella, §10.2, §12; LR ENC-P0-sintesi (FALSO), ENC-P0′, ENC-P0′-DIC (DA AUDITARE); `enc_recep` test 5 |
| ENC-3 | MAJOR | Eccezioni ristrette a 𝒮(ℝ): P0′ riformulato su nucleo denso D_0, senza (H-P0) né 𝔈. Lente e Avron–Herbst presentati come identità su D_0 = 𝒮(ℝ), fuori da (H-P0) (V illimitato); essenziale autoaggiuntezza e Mehler CON-FONTE. Formula della lente riscritta nella variabile y. Nota: dentro (H-P0) su ℝ, Bluman–Shtelen si riduce a V = γ(t). | PP §4 (H-P0), ENC-P0′ ed esempi; LR ENC-P0′ (versione su nucleo denso DA AUDITARE); CR R3–R4 |
| ENC-4 | MAJOR | Dichiarato che P0(b) (L², bordo) non copre ENC-1. Aggiunti ENC-P0(b)^cl (testo del revisore) e POLE-N^cl, entrambi DA AUDITARE; argomento spettrale (KA P4); 𝔈 non vuota (operatori d'onda, KA P7); "Lettura" di POLE-N ristretta agli intertwiner istantanei. Il sotto-caso "commuta con ∂_t" con c costante è chiuso, con c(t) è aperto. | PP §4; LR ENC-P0(b), ENC-P0(b)^cl, POLE-N, POLE-N^cl; CR R1, R6; OQ Q11 |
| ENC-5 | MAJOR | §5 riscritta. Quadro ben posto con 𝒮_V lineare, classi [𝒮_V], N_V(v) = e^{ic_Vt}v, uscite 𝒪 = 𝒟_0/≈, quantificazione "per una famiglia fissata 𝒲". Etichetta "Lemma di riduzione"; (iii) dichiarato vero per definizione. Testimone di ENC-N1 (F6) = (iv) al posto di v = 0; F6* vera per V(x)/DM3. Nuovo punto (v): la famiglia stretta fa fallire (C) (verificato). Lettura di gauge "cieco ⟺ identificabilità modulo gauge" al posto della citazione di VAR-P4(a). VAR-T1(b) citato nella forma auditata (SF, VAR-1, VAR-L1). | PP §5; LR ENC-N1, ENC-N1′; CR R8; OQ Q14; `enc_recep` test 10 |
| ENC-6 | MINOR | (a) Conseguenza "nessun getto certifica" resa osservazione ENC-T2(c′), con prova diretta in ogni punto, senza W (DA AUDITARE); induzione dei getti confermata per ogni ordine. (b) Nota: l'esempio illustra (a), non (b); ENC-T2 non è uno strumento di B1. ENC-T2(a)(b)(c) **invariati**. | PP §3; LR ENC-T2, ENC-T2(c′); CR R7; `enc_recep` test 7 |
| ENC-7 | MINOR | B = −2(d/dx)K(x, −x) in ENC-U1, con spiegazione del termine di Leibniz. | PP §2 ENC-U1; `enc_recep` test 6 |
| ENC-8 | MINOR | (a) (H3) → notazione; (b) domini non simmetrici: punto base al centro di J′ (frase di §10.3 corretta); (c) nota del valor medio per D1; (d) misura di Δ = 2a², norma HS ≤ √2·a‖K‖. | PP §2 enunciato, prova (2) e (5); §10.3 |
| ENC-9 | MINOR | Z "chiuso e numerabile" (non "discreto"), con costruzione Z = ∪Z_k e scelta globale di ψ_2; discretezza in OQ Q7. | PP §6 ENC-K1′; LR ENC-K1′; OQ Q7; CR R9 |
| ENC-10 | MINOR | Stellatezza della lente solo se 0 ∈ I; anello coniugato con coefficienti polinomiali in (t, x), con Φ^{−1}∂_tΦ = ∂_t − 2Ft∂_x + iFx − iF²t² (verificato). | PP §8 (a), (c); LR NS-EQ-Ω; `enc_recep` test 8–9 |
| ENC-11 | MINOR | FAD-1(iii) con 𝐕 = Σ‖V_i‖ e resto ≤ (Cℓ𝐕)³e^{Cℓ𝐕}‖u^{(0)}‖/3, uniforme in N. | PP §9; LR FAD-1; CR R10 |
| ENC-12 | MINOR | Errata di Avron–Herbst estesa all'encoder inverso. | PP intestazione/§0; LR nota errata |
| ENC-13 | MINOR | Istanze di N1′: magnetico "aperto"; V(t, x) "vuota per encoder indipendenti dal tempo, aperta per W(t)"; V(x) senza "stabile", onda e calore fuori dal quadro; Φ(V, v) ~ Φ(V′, v′), suriettività di W_V. | PP §5 istanze |
| ENC-14 | MAJOR | (E1) = "dim ker W < ∞ su 𝒴" in ENC-D e in P0(b). Aggiunto ENC-P0(b)^loc (DA AUDITARE), con il controesempio per restrizione (KA P6) e la frase per G★″ "un encoder strutturato indipendente dal tempo vede solo la regione in cui V(t, ·) − c(t) è autonomo". Domanda a S8-VAR su VAR-L1. | PP §1 ENC-D, §4; LR ENC-D, ENC-P0(b)^loc; OQ Q12; `inbox/S8-VAR.md` |
| ENC-15 | MINOR | (a) In P0(a)(⇐) si usa solo MD ⊂ D; continuità di U_V nei due argomenti; Ran(m) ⊂ ker W per densità e chiusura; E_k di misura finita. (b) Dichiarato che P0(b), ^cl, ^loc e POLE-N non usano il propagatore; rilievo Kato C¹ a S8-VAR e CIT-AUDIT-8 (OQ Q13). (c) La frase "trasformazioni non locali" è riformulata (ogni V ha il quadro d'interazione; la restrizione a V quadratico vale solo per i rappresentanti puntuali). (d) Sotto-caso "commuta con ∂_t" con c(t): aperto (OQ Q11). | PP §4; OQ Q11, Q13; `inbox/S8-VAR.md` |

**Claim nuovi (DA AUDITARE):**
- ENC-P0(b)^cl, ENC-P0(b)^loc;
- ENC-P0′ su nucleo denso con gli esempi su 𝒮(ℝ);
- ENC-P0′-DIC;
- POLE-N^cl;
- ENC-T2(c′).

**Claim cambiati:**
- ENC-P0-sintesi → FALSO;
- ENC-N1 (F6): FALSO, con nuovo testimone;
- ENC-N1′ riformulato (lemma, famiglia fissata, gauge, punto (v));
- ENC-A9(b2): stima corretta, quella della rev. 1 è FALSO;
- ENC-A9(a) + ottimalità di 2/3;
- ENC-U1 (refuso B);
- ENC-K1′ (Z numerabile);
- NS-EQ-Ω (0 ∈ I, anello in (t, x));
- FAD-1(iii) (costante);
- ENC-D ((E1) su 𝒴);
- ENC-TAB (riga puntuale + gauge).

**Invariati:** ENC-K0, ENC-1, ENC-C1, ENC-T2(a)(b)(c), ENC-P0(a), ENC-K1, A9(b1), (b3), (b4), FW-1, GAM-O1, ENC-L1.

**Verifiche:** `sympy/enc_recep.py` → `enc_recep.out`, 10/10 OK. I quattro script della rev. 1 (80/80) non cambiano.

---

## Post-Gate 8 (27/10/2026)

Fonti:
- `GATE8.md`: la strada RT-ENC è **PARCHEGGIATA**; i lemmi di S8-ENC passano a RT-DICT (ENC-1, U1, C1, T2) e RT-IDV (P0, P0′, POLE-N, N1′, A9);
- `work/CHECK-F8/AUDIT_S8-ENC_rev2.md`: fix ENC2-1…ENC2-6;
- `research/DEVIL/ATTACK-8.md`: O2, O16;
- `research/CIT-AUDIT/AUDIT-8.md` §5: correzioni S8-ENC.

Abbreviazioni come sopra; la rev. 2 del pacchetto è in `PROOF_PACKAGE.rev2.md`, quella di LR in `LEDGER_ROWS.rev2.md`. Gli stati sono cambiati **solo verso il basso**. Dove il revisore propone DIMOSTRATO dopo un fix ENC2-k, LR lascia PROVA SCRITTA e la promozione spetta a central.

| fix | severità | modifica | file / sezione |
|---|---|---|---|
| ENC2-1 | MAJOR | P0(b)^cl con ipotesi coerenti: (i) V(t, ·) ∈ C^∞ e W: C^∞ → C^∞, oppure (ii) W: D_W → 𝒟′(J), D_W ⊃ C(J)·C^∞_c(J), nucleo finito su tutto D_W. "Equivalentemente" sostituito da "in particolare, se W è sequenzialmente continuo su C^∞(J), …". Nella prova: le mφ_k stanno in D_W. Conclusione esplicita per Volterra: V = q(x) + c(t) + costante; copertura con (ii) per q continuo, con (i) per q ∈ C^∞. P0(b)^loc della rev. 2 dichiarato **FALSO come scritto** con il controesempio W(g + w·f) := g, V = t·w; versione corretta con (i)/(ii) su U. | PP §4 P0(b)^cl, P0(b)^loc, §12; LR ENC-P0(b)^cl, ^loc |
| ENC2-2 | MINOR | Aggiunto "0 ∈ I" alle ipotesi di P0′. | PP §4 P0′; LR ENC-P0′ |
| ENC2-3 | MINOR | Avron–Herbst è un'istanza di P0′ con θ = id e D_0 = 𝒮, non di P0(a); normalizzazioni dichiarate (lente: −½∂² + ½x²; Avron–Herbst: progetto). Unicità in L² con d/dt[e^{itH}U(t)u_0] = 0; essenziale autoaggiuntezza CON-FONTE Reed–Simon II Thm X.38 (Faris–Lavine 1974). | PP §4 esempi; LR ENC-P0′ |
| ENC2-4 | MAJOR | P0′-DIC riscritto in forma esistenziale: esiste un rappresentante con θ = id ⟺ α ≡ 0; α ≢ 0 ⇒ θ non affine; prova in due righe. La forma della rev. 2 è **FALSO come scritto** (controesempio pseudo-conforme per V = 0); "a ≡ 0 ⇒ ρ ≡ 1" corretto in "ρ costante". Sintesi di §4, riga §0, §10.2 punto 4 e tabella ENC-TAB allineate. | PP §0, §4 sintesi e DIC, §6 tabella, §10.2, §12; LR ENC-P0′-DIC, ENC-TAB; `sympy/enc_g8.py` test 1–4 |
| ENC2-5 | MINOR | POLE-N^cl: rettangolo [s, t] × U privo di poli al posto dell'intervallo libero ai due tempi, con l'esempio POLE3; w_n costante non nulla (K1′(i)), n ≥ 1; V C^∞ fuori dai poli, quindi forma (i) di ENC2-1. | PP §4 POLE-N^cl, §12; LR POLE-N^cl; `enc_g8` test 5 |
| ENC2-6 | MAJOR | T2(c′): definizione di "certifica"; enunciato circoscritto a C^∞(Ω) senza vincoli; regolarità q ∈ C^{2d−2}; h nella classe dei dati (DM3). Con vincolo di grado **FALSO** (4-getto di e^{x²}); nella classe degli annullatori principali **APERTO** (OQ Q15). R6 non lo usa. | PP §3 (c′) e prova, §12; LR ENC-T2(c′); OQ Q15 |
| svista §10.2 | — | "CHECK_REQUEST D3" → "D6". | PP §10.2 punto 2 |
| ATTACK-8 O2 | — | La colonna delle eccezioni della riga "puntuale + gauge" di ENC-TAB non dice più "cambiano il tempo": "si può scegliere θ = id se e solo se α ≡ 0; per α ≢ 0 ogni rappresentante ha θ non affine". | PP §6 tabella; LR ENC-TAB |
| ATTACK-8 O16 | — | ENC-A9(b) con stato per parti: (b1), (b2) corretta, (b4) DIMOSTRATO (proposto da S-CHECK); (b3) **CON-FONTE + V-ex**, eredita VAR-T10(3)(iii). | PP §7 (b3), §12; LR ENC-A9(b) |
| CIT-AUDIT-8 §5.1 | — | Dicotomia riformulata (vedi ENC2-4) con "ρ costante"; Bluman–Shtelen con J. Phys. A 29(15) 4473–4480, DOI 10.1088/0305-4470/29/15/018. | PP §4 DIC; LR ENC-P0′-DIC |
| CIT-AUDIT-8 §5.2 | — | Reed–Simon II Thm X.38 (Faris–Lavine, CMP 35 (1974) 39–48, DOI 10.1007/BF01646453); §X.12 dichiarato non verificato; Pazy cap. 5 senza numero. | PP §4 (H-P0) ed esempi |
| CIT-AUDIT-8 §5.3 | — | Mehler → DLMF 18.18.28 e Mehler 1866 (J. reine angew. Math. 66, 161–176). | PP §4, §7 (b3) |
| CIT-AUDIT-8 §5.4 | — | ENC-K1: Wilson 1993 (J. reine angew. Math. 442, 177–204, DOI 10.1515/crll.1993.442.177) per la grassmanniana adelica; Wilson 1998 facoltativo; D–G con DOI. | PP §6 ENC-K1; LR ENC-K1 |
| CIT-AUDIT-8 §5.5 | — | ENC-K1′: Andrianov–Sokolov NPB 660(1–2) (2003) 25–50, DOI 10.1016/S0550-3213(03)00232-3; Sokolov J. Math. Sci. 151(2) (2008) 2924–2936, DOI 10.1007/s10958-008-9009-3; Crum Q. J. Math. 6 (1955) 121–127. Rischio di novità alto, **confermato**: nessuna novità. | PP §6 nota di priorità, tabella, §12; LR ENC-K1′ |
| CIT-AUDIT-8 §5.6 | — | (b4) "Pöschl–Teller modificato (iperbolico)", con Pöschl–Teller Z. Phys. 83 (1933) 143–151; Marchenko cap. 1 senza numero di teorema. | PP §2 ENC-1, §6 tabella, §7 (b4), §12; LR ENC-1, ENC-A9(b) |
| GATE8 | — | Nota RT-ENC PARCHEGGIATA in testa a PP e LR. | PP intestazione; LR intestazione |

**Claim declassati (verso il basso):**
- ENC-P0(b)^loc (rev. 2) → FALSO come scritto; versione corretta PROVA SCRITTA;
- ENC-P0′-DIC (rev. 2) → FALSO come scritto; forma esistenziale PROVA SCRITTA;
- ENC-T2(c′) → circoscritto a C^∞(Ω) senza vincoli; con vincolo di grado FALSO; classe principale APERTO;
- ENC-A9(b3) → CON-FONTE + V-ex (prima nascosto dentro "DIMOSTRATO" di ENC-A9(b));
- ENC-K1′ → nessuna novità (lo stato matematico non cambia).

**Claim riformulati senza cambio di stato:** ENC-P0(b)^cl (ipotesi (i)/(ii)), ENC-P0′ su nucleo denso (0 ∈ I, esempi), POLE-N^cl (rettangolo), ENC-TAB (O2), ENC-K1 (citazioni).

**Invariati:** cammino critico ENC-1 → ENC-C1 → ENC-T2(a)(b)(c) → R6; ENC-K0, ENC-U1, ENC-P0(a), ENC-P0(b), POLE-N hilbertiano, ENC-N1′, NS-EQ-Ω, FAD-1, FW-1, GAM-O1.

**Verifiche:** `sympy/enc_g8.py` → `enc_g8.out`, 5/5 OK (sistema DIC3, gaussiana libera, mappa pseudo-conforme, θ affine ⇒ α = 0, POLE3). Gli script precedenti non cambiano.
