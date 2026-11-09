# S10-OPEN-C — LEDGER_ROWS proposte (27/10/2026)

Gli stati sono **proposti**: li registra il coordinatore dopo l'audit. Il formato segue claims/LEDGER.md.

| ID | enunciato | ipotesi | stato | prova | SymPy | proof-checker | kill-argument | dipende da |
|---|---|---|---|---|---|---|---|---|
| VAR-P11 | (e) soluzioni classiche con B ∈ C¹ | A_0 genera C_0; B ∈ C¹([0,T]; 𝓛(X)); x ∈ D(A_0) | (e) da CON-FONTE a **prova scritta** → DIMOSTRATO dopo audit | S10-OPEN-C PP §1 | — | da fare | interno: nessun difetto | — |
| VAR-L2-cor | (invariato) | (invariato) | da CON-FONTE a **DIMOSTRATO** se l'audit conferma VAR-P11(e) | S8-VAR PP; S10-OPEN-C PP §1 | — | da fare | — | VAR-P11(e), VAR-L2 |
| VAR-Q18-CE | B continuo in norma, antiaggiunto, U(t,0) non conserva D(A_0) | X = ℋ ⊕ ℂ, B di rango 2 | **FALSO** l'enunciato P11(e) senza C¹ (controesempio, prova scritta) | PP §2 | T7 | da fare | interno | — |
| VAR-Q18-mult | P11(e) per moltiplicazioni V ∈ C([0,T]; L^∞) non C¹ | — | APERTO — ridotto a §2 Portata | PP §2 | — | — | — | — |
| VAR-Q10-EX | ∃ u, V = 0, \|Z(u)\| > 0, int Z = ∅ | I = (0,1) | **prova scritta** (esistenza) | PP §3 | T1, T2 | da fare | interno (I = (0,1)) | S8-VAR §7.1 |
| VAR-Q17(a) | osservabilità laterale per soluzioni miti, V = V_0(x) + v(t) | quadro di L2-cor | **prova scritta** | PP §4 | — | da fare | — | VAR-L2-cor |
| VAR-Q17(b) | caso V(t,x) | — | APERTO — ridotto a continuazione laterale con regolarità negativa in t | PP §4(c) | — | — | — | — |
| VAR-P12 | (d) nella classe quadratica: nessun log quadratico (tr M = −26/5) | ω costante a tratti o regolarizzata | (d) **FALSO nella classe quadratica** (controesempio); caso L^∞/differenziale generale APERTO — ridotto | PP §5 | T8 | da fare | interno (classe) | — |
| VAR-C3Q2-R | Ann(u) = A_2L ⟺ rank_B(A_2u) = m (L monico); f(x+t) non D-finita non identifica □; olonomo ⇒ mai | Lu = 0 | **prova scritta** (Wiman–Valiron e Bernstein CON-FONTE); caso non monico (VAR-Q13) APERTO | PP §6 | T10 | da fare | — | S8-VAR §5 |
| SYS-DIRAC-POL | (a) ZXZ in ℚ[ξ,m][[t]]; (b) a t ≠ 0 fisso nessuna parola finita a tempi polinomiali reali | m ≠ 0 | **prova scritta** | PP §7 | T3, T4 | da fare | interno | SYS-E3 |
| II-T2(b′) | derogatorio: polo ⟺ E_0 ∩ F_0 ≠ 0; la forma di Jordan non decide | Q, B coprimi | **prova scritta** (a); congettura Q-S8SYS-4 **FALSA** | PP §8 | T6 | da fare | — | — |
| SYS-MAXWELL | soc_𝔪(M_P) = 0 ⇒ campo identificante su Ω connesso | — | **prova scritta** | PP §9 | T5 | da fare | — | SYS-EX |
| ENC-T2(c′) | nella classe principale: nessun getto (né striscia) certifica | P_* ≠ 0 | da APERTO a **prova scritta** | PP §10 | — | da fare | — | — |
| ENC-Q4-S | (S) non vacua per {q_0 + c}, DM-φ, famiglia stretta | q_0 ∈ C¹ | **prova scritta**; lettura DM3 APERTO — ridotto a P0 con W(t) | PP §11 | — | da fare | interno | ENC-1, ENC-N1′ |
| ENC-Q10-D | encoder non locale esplicito di Darboux per V_1 = −2∂²log u | u libera senza zeri | **prova scritta** (formula di κ: verifica solo SymPy, da rifare a mano); V reale APERTO | PP §12 | T9 | da fare | — | — |
| DICT-ILIM-Hs | ‖f‖_{C^s} ≤ C‖f‖_2^θ‖f‖_{C^{s,1}}^{1−θ}, θ = 2/(2s+2+N) | Ω limitato lipschitziano | da CANDIDATO a **prova scritta** (cono: CON-FONTE Adams–Fournier) | PP §13 | — | da fare | — | — |
| DICT-U3d-v | velocità L¹ per ogni nucleo c.m.: 2e^{−J}max(1,4J/e²)C_k + τ_k(4J/(e²T)) | k c.m., k ∈ L¹(0,T) | da CANDIDATO a **prova scritta**; ottimalità APERTA | PP §14 | T13 | da fare | — | U3(d) |
| DICT-Q3-R | intermedio di RANGO = divisione C^∞; test puntuale e formale insufficiente in C^∞ | — | APERTO — ridotto (con controesempio prova scritta; caso analitico CON-FONTE Malgrange) | PP §15 | T11 | da fare | — | RANGO |
| DICT-Q4-C | A(iii) ⟺ (2); rango finito ⇒ falso; rango infinito ⇒ vero | atomi continui | (b) **prova scritta**; (a) CON-FONTE (Amitsur) | PP §16 | T12 | da fare | interno | Teorema A |
| DM-δ-MINIMAX | rischio minimax per V_u in DM-δ: Θ(ε^{1/3}) | classe 𝒰(M, δ_0, K) | **prova scritta** | PP §17 | T14 | da fare | — | VAR-P3(c) |
