# CHECK_REQUEST — S8-VAR → S-CHECK-F8
27/10/2026. Pacchetto: `work/S8-VAR/PROOF_PACKAGE.md` (§1–§8). Script: `work/S8-VAR/sympy/*.py` con uscite `*.out` (8 script, 50 controlli, tutti "TUTTO OK"). Comando: `D:\ProblemaBase\.venv\Scripts\python.exe -I work/S8-VAR/sympy/<script>.py`.

Nessun claim è marcato DIMOSTRATO. Chiedo a S-CHECK-F8 il giudizio (DIMOSTRATO / da correggere / FALSO) sui claim seguenti, in ordine di priorità.

## Priorità 1 — cammino critico (identificazione di V)
| ID | dove | cosa controllare |
|---|---|---|
| VAR-L0 | §1.3 | (i) il calcolo di P_λ = S + A e del commutatore [S,A], in particolare il termine 4λφ_xt Im(z_xz̄) e i termini di ordine zero (4λ³φ_x²φ_xx − λφ_xxxx + λφ_tt); (ii) l'assorbimento del termine incrociato con φ_xx = 2μ; (iii) l'estensione per mollificazione alla classe w ∈ C_c con w_t, w_xx continue |
| VAR-L1 | §1.3 | la lente Λ_{2ε} ⊂ int B (scelta di ε rispetto ad a, b); il supporto e la regolarità di w = χ(φ)u; l'assorbimento di V con (μλ³)^{1/2} ≥ 2‖V‖; la stima finale e^{−λε/2} |
| VAR-L2 | §1.3 | la definizione di s*, l'uguaglianza ∪_{s<s*}R_s = R_{s*}, la compattezza del grafico chiuso e l'η-intorno; gli estremi del grafico |
| VAR-T1(b) | §1.4 | il lemma di accumulazione: u_x = 0 e u_xx = 0 sulla retta x = x_0 con V solo L^∞; la regolarità C^{1,2} dell'estensione per zero |
| VAR-T1(c) | §1.5 + §7.1 att. 9 | la stima di Cauchy su g^{(k)} e la regolarità C^∞ della serie di Tychonoff in t = 0; la riduzione int Z(u) ≠ ∅ ⇒ fascia di silenzio |

**Domande mirate.**
Q1. L'identità ‖P_λz‖² = ‖Sz‖² + ‖Az‖² + q(z) con q come scritto è corretta? (La verifica in `s8_carleman` è numerica: chiedo un controllo simbolico o a mano.)
Q2. Il lemma VAR-L1 è noto in letteratura per V ∈ L^∞(t,x) in 1D? (Candidati: Saut–Scheurer 1987, Isakov 1993.) Se sì, lo stato giusto è "noto, prova autosufficiente".
Q3. VAR-T1(b) è stato provato nella classe V = V(x) ∈ L^∞_loc; vale l'identificazione per ogni u ≢ 0. È d'accordo che questo chiude la lacuna "V ∈ L^∞" del VERDETTO F6?

## Priorità 2 — struttura (ODE, Lie, Weyl)
| ID | dove | cosa controllare |
|---|---|---|
| VAR-T6 | §2.2 | (a) la corrispondenza sottospazi G-stabili ↔ fattori destri via Wronskiani (uso di E^G = K); (b) Sol(L_u) = span(Gu); (c) il criterio di ciclicità m_i ≤ dim S_i (densità di Jacobson); (d) socle/Loewy |
| VAR-E2 | §2.3 | la forma w = εx + Σ1/(x − a_j) delle soluzioni razionali della Riccati e la riduzione all'equazione di Hermite; l'unicità di ℂh_n |
| VAR-P8(a) | §3.1 | il lemma sul coefficiente di testa 2^jc^{(j)} e la crescita dei gradi per d ≥ 3 |
| VAR-P8(c) | §3.3 | la stima H_{j−1} + j² ≥ 2j − 1; il proiettore Q; l'intrecciamento e i domini |
| VAR-C3Q2 | §5 | l'unicità della divisione in A_2; (c) D-finita ⟺ esiste R ∈ B; (e) l'argomento di Fourier per l'esistenza; (f) ∂_t ∉ A_2x∂_t |

Q4. In VAR-T6(c) il passaggio "immagine di span(G) = ⊕End(S_i)" è corretto per G algebrico infinito (span(G) finito-dimensionale in End(V))?
Q5. In VAR-C3Q2(e) l'argomento "f̂ si annulla su intervalli e non è nulla su intervalli vicini ⇒ contraddizione con l'unicità di Cauchy su (0,δ)" è completo?

## Priorità 3 — non autonomo e varie
VAR-P3 (§1.6: le due interpolazioni e la nitidezza), VAR-P4 (§1.7), VAR-P5 (§1.8: esempio Dirac e caso hermitiano), VAR-P9 (§4.1: il maggiorante del resto), VAR-P11 (§4.2: unitarietà per approssimazione costante a tratti), VAR-T10 (§4.3: decomposizione LUL ⟺ M_12 ≠ 0; correzione "cos t = 0"), VAR-P12 (§4.4).
Q6. VAR-T10: è d'accordo che la frase F6 "si rompe a cos t = 0" va sostituita con "la parola chirp·libero·chirp esiste ⟺ M_12(t) ≠ 0; una parola fissa vale solo localmente"?

## Fonti da verificare (CIT-AUDIT)
Hörmander ALPDO I Thm 8.6.5 (Holmgren); van der Put–Singer Prop. 1.34/Thm 1.27 (E^G = K); Pazy cap. 5 (regolarità classica Dyson–Phillips); Folland, Harmonic Analysis in Phase Space, cap. 4 (metaplettica); Crum, Q. J. Math. Oxford 6 (1955) (catena di Darboux); Moan–Niesen 2008 Thm 3; Casas, J. Phys. A 40 (2007) 15001–15017 (letto solo l'abstract); Schindelar–Levandovskyy–Zerz, JSC 46 (2011) 1189–1204 (letto solo l'abstract); Wei–Norman 1964; Hochbruck–Lubich 2003; Saut–Scheurer 1987; Isakov 1993; Grigoriev–Schwarz (puntatore).
