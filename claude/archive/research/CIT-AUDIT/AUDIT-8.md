# AUDIT-8 — CIT-AUDIT-8 (Fase 8)

Data: 2026-10-27 · Agente: CIT-AUDIT-8 · Piano: `PLAN-8.md` · Modello: `AUDIT-6.md`.
Ambito: `work/S8-{SYS,VAR,CONV,ENC,DICT}/{PROOF_PACKAGE,LEDGER_ROWS,RECEPIMENTO}.md`, `work/CHECK-F8/AUDIT_*.md` e `KA_*`. Nessuna sessione S8 ha un `sources.bib`.

## 0. Metodo

- **Esiti.** VERIFICATO (metadati e contenuto coerenti con l'uso) / DATI CORRETTI (fonte giusta, dati o numerazione da correggere) / CONTENUTO DIVERSO (la fonte non dice ciò che le si attribuisce) / NON TROVATO / PARZIALE (metadati confermati, enunciato o numero non letto).
- **Gradi di lettura.** (primaria) testo della fonte; (abstract); (secondaria) fonte terza che riporta l'enunciato; (memoria) non conta come verifica.
- **Metadati.** Ottenuti con Crossref tramite `doi.org` in negoziazione CSL-JSON e con `api.crossref.org/works?query.bibliographic=`; con l'API arXiv; con PDF ad accesso aperto letti nello scratchpad della sessione. La prima tornata su Crossref è stata limitata (HTTP 429); i metadati sono stati riletti tutti il 2026-10-27 tramite `doi.org`.
- **Regole.** Nessuno script `_vendor` eseguito. Nessun PDF o script salvato nel progetto. Paywall, 403 e pagine di login non valgono come conferma.

## 1. Tabella, priorità A

| # | voce | usata in | esito | metadati verificati (fonte) | contenuto rispetto all'uso | correzione |
|---|---|---|---|---|---|---|
| A1 | Oberst, *On the minimal number of trajectories determining a multidimensional system* | S8-SYS §1 l.13–36; SYS-EX, SYS-N1, SYS-T0 (fix SYS-2) | **VERIFICATO** (abstract) | MCSS 6(3) (1993) 264–288, DOI 10.1007/BF01211623 (Crossref) | Abstract (scheda ACNP unibo; testo pieno dietro login). μ(S) è determinato costruttivamente per sistemi PDE e alle differenze a coefficienti costanti. Il risultato generalizza Heij (1D) e Zampieri (2D). μ(S) ≤ 1 identifica i sistemi principali di Macaulay. Per dimensione > 1 molti sistemi "grandi" sono principali. È esattamente il prior art di SYS-EX/N1 su ℝ^n. Secondaria: Pommaret, arXiv:0902.2314, Thm 5.2.5. Per M n-puro, il numero minimo di generatori del sistema duale è max_{m∈ass M} dim soc_m(M), come conseguenza di Kunz IV §2 e Macaulay §82. | SYS §1: completare i metadati (6(3), DOI). Dichiarare che il testo pieno non è stato letto. Aggiungere Pommaret 2010 Thm 5.2.5 e Macaulay come secondaria. Vedi §3 (rischio altissimo su ℝ^n). |
| A2 | Oberst, *Multidimensional constant linear systems* | SYS-EX Passo 3 (iniettività di C^∞(ℝ^n)), SYS-T1 | **PARZIALE** | Acta Appl. Math. 20(1–2) (1990) 1–175, DOI 10.1007/BF00046908 (Crossref; già in bib) | Le pp. 24–36 e i §2–4 chiesti dal mandato non sono stati letti (testo dietro login). Il cogeneratore iniettivo C^∞(ℝ^n) è risultato standard: Pommaret lo cita come [15]. | SYS: mantenere "CON-FONTE (non letto per numero di pagina)". Non citare pp. 24–36 come lette. |
| A3 | Oberst, *Variations on the fundamental principle for linear systems of partial differential and difference equations with constant coefficients* | SYS §1 (prior art possibile) | **VERIFICATO** (abstract) | AAECC 6(4–5) (1995) 211–243, DOI 10.1007/BF01235717 (Crossref) | Abstract: spazi di successioni e funzioni localmente finite e polinomiali-esponenziali che soddisfano il principio fondamentale. È pertinente come contesto del caso polinomiale-esponenziale, non come fonte di μ(S). | SYS §1: aggiungere i metadati completi. |
| A4 | Schindelar, Levandovskyy, Zerz, *Exact linear modeling using Ore algebras* | SYS-R1; VAR §2.4 (VMPUM), l.163 | **VERIFICATO** (abstract) | J. Symbolic Comput. 46(11) (2011) 1189–1204, DOI 10.1016/j.jsc.2011.08.001 (Crossref; arXiv:1004.2924) | L'abstract dice che il caso a coefficienti costanti è ben noto e che il caso a coefficienti variabili è trattato solo di recente. MPUM e VMPUM sono calcolati per segnali polinomiali e polinomiali-esponenziali. Il titolo corretto in VAR l.163 coincide. | Nessuna; aggiungere il DOI dove manca. |
| A5 | VMPUM (definizione) | VAR §2.4 | **VERIFICATO** (abstract) | come A4 | Il termine "VMPUM" compare nell'abstract di SLZ 2011. L'attribuzione è corretta. | Nessuna. |
| A6 | Kolář, Michor, Slovák 1993, 18.16 | S8-DICT l.51/65/400 ("senza KMS 18.16") | **VERIFICATO** (primaria) | già in bib (AUDIT-6); PDF dell'autore, pp. 173–174 | 18.16 riguarda gli operatori di morfismo. Per un operatore di ordine k la mappa associata D su J^k ×_Y Z → Z₂ è liscia se l'operatore è regolare, e viceversa. Richiede ordine finito globale. DICT U2-a è la versione locale, sull'intorno 𝒱 di 19.10. DICT fa bene a dare una prova propria. | Nessuna. Facoltativo: dire che U2-a è "versione locale di KMS 18.16". |
| A7 | Hörmander, ALPDO I, Thm 8.6.5 (Holmgren) | VAR l.75, VAR-L1, VAR-T1 | **VERIFICATO** (secondaria) | 2ª ed. (1990) | Huang, arXiv:1707.08548, rif. [5], cita Holmgren come Hörmander I Thm 8.6.5. | VAR l.75: togliere "numero da verificare" e precisare 2ª ed. |
| A8 | Saut, Scheurer, *Unique continuation for some evolution equations* | VAR l.75; LEDGER VAR-L2 ("probabilmente in Saut–Scheurer 1987") | **PARZIALE** (secondaria) | J. Differential Equations 66(1) (1987) 118–139, DOI 10.1016/0022-0396(87)90043-X (Crossref) | Secondo Huang, Saut–Scheurer (e Isakov) danno per operatori parabolici del 2° ordine la proprietà della componente orizzontale: soluzione nulla su un aperto ⇒ nulla sulla sua componente connessa orizzontale. Saut–Scheurer la affermano anche per ordine superiore. **Per Schrödinger non confermato.** | VAR-L2: sostituire "probabilmente in Saut–Scheurer 1987" con "Saut–Scheurer 1987 (caso parabolico); per tipo Schrödinger in n = 1 vedi Isakov 1993". Lo stato resta PROBABILMENTE NOTO. |
| A9 | Isakov, *Carleman type estimates in an anisotropic case and applications* | VAR l.75, VAR-L0–L2 | **VERIFICATO** (secondaria) | J. Differential Equations 105(2) (1993) 217–238, DOI 10.1006/jdeq.1993.1088 (Crossref) | Secondo Huang: in n = 1, continuazione unica locale attraverso un segmento parallelo all'asse dei tempi (x = cost) per soluzioni H^{2m}_loc con termini di ordine inferiore localmente limitati. Comprende equazioni di tipo Schrödinger. In n > 1 dà solo un risultato più debole. VAR-L1 tratta un grafico x = g(t) non caratteristico, più generale ma vicino. | VAR: citare Isakov 1993 come fonte più vicina a VAR-L1/L2. La dicitura "probabilmente noto" è coerente. |
| A10 | Casas, *Sufficient conditions for the convergence of the Magnus expansion* | VAR l.226 (VAR-T10(4)); CONV l.297 (contratto (B)) | **DATI CORRETTI** (primaria) | J. Phys. A 40(50) (2007) 15001–15017, DOI 10.1088/1751-8113/40/50/006 (Crossref; arXiv:0711.2381; già in bib) | Thm 3.4: la serie di Magnus converge se ∫_0^T‖A‖ < π, con A limitato su Hilbert. Vale anche in dimensione infinita se Y è normale (in particolare unitario). Esempio 2: π è ottimale per A limitato generico. VAR è corretto. CONV scrive "costante π non letta nel testo: da verificare", formula superata. | CONV l.297: sostituire con "Casas 2007, Thm 3.4: raggio π, ottimale (Es. 2); in dimensione infinita richiede Y normale". Completare AUDIT-6 riga 19 allo stesso modo. |
| A11 | Pöschl, Teller, *Bemerkungen zur Quantenmechanik des anharmonischen Oszillators* | VAR-P8(c)(d); ENC-A9(b4) | **DATI CORRETTI** | Z. Phys. 83 (1933) 143–151, DOI 10.1007/BF01331132 (Crossref) | Il potenziale del 1933 è trigonometrico (1/sin², 1/cos²). Il potenziale sech² usato in VAR ed ENC è il "Pöschl–Teller modificato (iperbolico)". L'uso è diffuso ma impreciso. | VAR, ENC: scrivere "Pöschl–Teller modificato (iperbolico)" e aggiungere i metadati. |
| A12 | Crum, *Associated Sturm–Liouville systems* | VAR l.184; ENC l.368; ENC-K1′ | **VERIFICATO** (metadati e titolo) | Q. J. Math. 6(1) (1955) 121–127, DOI 10.1093/qmath/6.1.121 (Crossref) | Catene di trasformazioni di Darboux: è l'oggetto del lavoro, e l'uso è standard. Il numero del teorema non è citato e non serve. | VAR, ENC: aggiungere i metadati. Togliere Crum dalla lista "numeri non verificati" di VAR l.323. |
| A13 | Duistermaat, Grünbaum, *Differential equations in the spectral parameter* | ENC-K1 l.384 | **VERIFICATO** (metadati; recepimento) | Commun. Math. Phys. 103(2) (1986) 177–240, DOI 10.1007/BF01206937 (Crossref) | ENC-K1 adotta correttamente la normalizzazione V → 0 all'infinito (correzione CONTENUTO DIVERSO di AUDIT-6 recepita). | Nessuna. |
| A14 | Wilson 1998 / Wilson 1993 | ENC-K1 l.384 (Grassmanniana adelica) | **DATI CORRETTI** | Wilson 1998: *Collisions of Calogero–Moser particles and an adelic Grassmannian*, Invent. Math. 133(1) 1–41, DOI 10.1007/s002220050237. Wilson 1993: *Bispectral commutative ordinary differential operators*, J. reine angew. Math. 442 177–204, DOI 10.1515/crll.1993.442.177 (Crossref) | La classificazione bispettrale tramite la Grassmanniana adelica è in Wilson 1993. Il 1998 riguarda Calogero–Moser. | ENC-K1: citare Wilson 1993 per la bispettralità. Wilson 1998 resta facoltativo. |
| A15 | Marchenko 1986 cap. 1; Povzner 1948; Levitan 1987 | ENC-1 (CON-FONTE) l.66 | **PARZIALE** (memoria) | Marchenko 1986 già in bib. Povzner: Mat. Sb. 23(65):1, 3–52 (AUDIT-6) | Il numero del teorema sul nucleo simmetrico in Marchenko cap. 1 non è stato letto. | ENC-1: citare "Marchenko 1986, cap. 1" senza numero di teorema finché non viene letto. |
| A16 | Bluman, Shtelen, *New classes of Schrödinger equations equivalent to the free particle equation through non-local transformations* | ENC-P0′-DIC l.208/296; tabella ENC | **VERIFICATO** (primaria) | J. Phys. A 29(15) (1996) 4473–4480, DOI 10.1088/0305-4470/29/15/018 (Crossref; PDF dell'autore) | Eq. (2.1)–(2.6), V reale. Trasformazione puntuale generale: y = σ(t)x + ρ(t), τ = ∫σ², u₂ = exp(i(σ̇x²/(4σ) + …))u₁. Equivalenza con la particella libera ⟺ V = α(t)x² + β(t)x + γ(t). Il §2 è citato correttamente. **Ma l'enunciato del progetto è troppo forte**: per α ≡ 0 esistono rappresentanti con θ ≠ id (σ costante ≠ 1 dà θ = σ²t; a = 1/(4(t − t₀)) risolve a′ + 4a² = 0). | ENC PROOF_PACKAGE l.296: sostituire "θ ≠ id ⟺ α ≢ 0" con "α ≢ 0 ⇒ θ non affine; α ≡ 0 ⟺ esiste un rappresentante con θ = id". Nella catena, "a ≡ 0 ⇒ ρ ≡ 1" diventa "ρ costante". La forma del LEDGER (esistenziale) va bene. Coerente con DEVIL-8 (ENC-P0′-DIC FALSO come scritto). MINOR per il checker. |
| A17 | Reed, Simon II | ENC l.294, LEDGER ENC-P0′ (essenziale autoaggiuntezza su 𝒮); ENC l.216 (§X.12) | **DATI CORRETTI** (secondaria) | già in bib. Faris, Lavine, *Commutators and self-adjointness of Hamiltonian operators*, Commun. Math. Phys. 35(1) (1974) 39–48, DOI 10.1007/BF01646453 (Crossref) | Thm X.38 (Faris–Lavine): V ∈ L²_loc e V ≥ −c|x|² − d ⇒ −Δ + V essenzialmente autoaggiunto su C_c^∞. Fonte secondaria: Simon, rassegna su Kato, arXiv:1711.00528. Copre −∂² + x² e −∂² + Fx su C_c^∞ ⊂ 𝒮. §X.12 (equazioni di evoluzione dipendenti dal tempo): non letto. | ENC l.294: citare "Reed–Simon II, Thm X.38 (Faris–Lavine 1974)". ENC l.216, §X.12: CON-FONTE non verificata. |
| A18 | Mehler (formula, nucleo) | ENC l.294/462, ENC-A9(b3); VAR-T10 | **DATI CORRETTI** | DLMF eq. (18.18.28), "is known as the Mehler formula". Mehler, *Ueber die Entwicklung einer Function von beliebig vielen Variablen nach Laplaceschen Functionen höherer Ordnung*, J. reine angew. Math. 66 (1866) 161–176, DOI 10.1515/crll.1866.66.161 (Crossref) | Il progetto cita "Mehler" senza riferimento. | ENC, VAR: citare DLMF 18.18.28 (e Mehler 1866 come fonte storica). |
| A19 | Avron, Herbst, *Spectral and scattering theory of Schrödinger operators related to the Stark effect* | ENC l.34/291/482; errata F6 | **VERIFICATO** (metadati) | Commun. Math. Phys. 52(3) (1977) 239–254, DOI 10.1007/BF01609485 (Crossref; già in bib) | La formula u = e^{−iFtx − iF²t³/3} v(t, x + Ft²) è dichiarata come normalizzazione del progetto, non come trascrizione della fonte. Va bene. | Nessuna. |
| A20 | Einkemmer, Ostermann 2015 | CONV l.258–261 (CONV-Q6) | **DATI CORRETTI** | *Overcoming order reduction in diffusion-reaction splitting. Part 1: Dirichlet boundary conditions*, SIAM J. Sci. Comput. 37(3) (2015) A1577–A1592, DOI 10.1137/140994204 (Crossref) | Analogia corretta. Il titolo citato è incompleto. | CONV: titolo completo con "Part 1: Dirichlet boundary conditions", più il DOI. |
| A21 | Dang, Einkemmer, Ostermann 2025 | CONV l.258–261 (CONV-Q6′) | **PARZIALE** (abstract) | arXiv:2504.10125v2, *An initial-boundary corrected splitting method for diffusion-reaction problems* (API arXiv) | L'abstract dà ordine 1 (Dirichlet) e 1.5 (Neumann/Robin). La norma non è dichiarata. | CONV-Q6′ resta aperto. Aggiungere il titolo. |
| A22 | Ax, *On Schanuel's conjectures* | DICT l.320 (DICT-AX, NS-EXPALG) | **PARZIALE** (metadati) | Ann. of Math. (2) 93(2) (1971) 252–268, DOI 10.2307/1970774 (Crossref) | Titolo confermato. L'enunciato in campi differenziali non è stato riletto (memoria). | DICT l.320: aggiungere titolo e DOI. Per il teorema serve lettura primaria (CON-FONTE). |
| A23 | Wei, Norman 1963 e 1964 | VAR (contesto Lie); AUDIT_S8-VAR | **VERIFICATO** (metadati) | 1963: *Lie algebraic solution of linear differential equations*, J. Math. Phys. 4(4) 575–581, DOI 10.1063/1.1703993. 1964: *On global representations of the solutions of linear differential equations as a product of exponentials*, Proc. AMS 15(2) 327–334, DOI 10.1090/S0002-9939-1964-0160009-0 (Crossref) | Uso di contesto. | Nessuna. |

## 2. Altre fonti, per sessione (priorità B)

| # | voce | usata in | esito | metadati / fonte | nota e correzione |
|---|---|---|---|---|---|
| B1 | Malgrange, Sém. Bourbaki exp. 246 (vol. 8, pp. 79–89), Thm 3.2(2) p. 83 | CONV l.34/215 (CONV-D2); SYS l.80 | **VERIFICATO** (primaria, da CHECK-F8) | Numdam SB_1962-1964__8__79_0 | Letto dall'auditor di CHECK-F8; non riletto qui. |
| B2 | Iniettività di 𝒟′(Ω) per Ω convesso (Palamodov 1970 cap. VII; Hörmander) | CONV l.217 (CONV-Q17) | **PARZIALE** | — | Nessuna fonte trovata. Confermato invece: principio fondamentale in 𝒟′(ℝ^n); iniettività di C^∞(Ω) per Ω convesso. Hörmander: P(D) suriettivo su 𝒟′(Ω) ⟺ Ω fortemente P-convesso, che non è l'iniettività. Lasciare il caso escluso, come fa CONV. |
| B3 | Stein 1970, *Singular integrals* | CONV l.142 (CONV-T4(b)) | **DATI CORRETTI** (secondaria) | — | Fonti secondarie (arXiv:2305.01441; note Rogers, UConn): operatore di estensione in cap. VI §3, Thm 5, p. 181 (domini lipschitziani limitati; Thm 5′ per i lipschitziani speciali). CONV: "cap. VI §3.1 Thm 5" → "cap. VI §3, Thm 5 (p. 181)". |
| B4 | Pazy, cap. 5 (Thm 5.2.?); Phillips 1953 | VAR l.214 (VAR-P11(e)); ENC l.216 | **PARZIALE** (memoria) | in bib | Numero non letto. Lasciare "cap. 5" senza numero di teorema. |
| B5 | Folland, *Harmonic Analysis in Phase Space*, cap. 4 (Stone–von Neumann) | VAR l.225 | **PARZIALE** (memoria) | in bib | Da memoria, Stone–von Neumann è al cap. 1 e il metaplettico al cap. 4. Verificare prima di citare "cap. 4". |
| B6 | van der Put, Singer, 1.27 / 1.34 | VAR-T6, VAR l.323 | **PARZIALE** (memoria) | — | Numeri non letti. |
| B7 | Matlis, *Injective modules over Noetherian rings* | SYS l.27 (SYS-T1) | **VERIFICATO** (metadati) | Pacific J. Math. 8(3) (1958) 511–528, DOI 10.2140/pjm.1958.8.511 (Crossref) | Aggiungere i metadati. |
| B8 | Matsumura §18 | SYS l.20 | **PARZIALE** (memoria) | — | Numero di paragrafo non controllato. |
| B9 | Eisenbud, Huneke, Vasconcelos, *Direct methods for primary decomposition* | SYS l.88 | **VERIFICATO** (metadati) | Invent. Math. 110(1) (1992) 207–235, DOI 10.1007/BF01231331 (Crossref) | Nessuna. |
| B10 | Andrianov, Sokolov, *Nonlinear supersymmetry in quantum mechanics: algebraic properties and differential representation* | ENC l.382 (ENC-K1′) | **VERIFICATO** (abstract) | Nucl. Phys. B 660(1–2) (2003) 25–50, DOI 10.1016/S0550-3213(03)00232-3 (Crossref; hep-th/0301062) | Rischio di novità ENC-K1′: vedi §3. |
| B11 | Sokolov, *Factorization of nonlinear supersymmetry in one-dimensional quantum mechanics. II: proofs of theorems on reducibility* | ENC l.382 | **DATI CORRETTI** (abstract) | J. Math. Sci. 151(2) (2008) 2924–2936, DOI 10.1007/s10958-008-9009-3 (Crossref; arXiv:0903.2835) | Abstract: fattorizzazione degli intertwiner SUSY in catene di trasformazioni di Darboux elementari con coefficienti non singolari. Citare la rivista oltre all'arXiv. |
| B12 | Niederer 1973 (lente) | ENC l.290 | **PARZIALE** | Helv. Phys. Acta 46, 191 (AUDIT-6); nessun DOI trovato | Non riletto. |
| B13 | Wu, Yang, *Concept of nonintegrable phase factors and global formulation of gauge fields* | SYS l.214; LEDGER G-T2 | **VERIFICATO** (metadati) | Phys. Rev. D 12(12) (1975) 3845–3857, DOI 10.1103/PhysRevD.12.3845 (Crossref) | SYS l.214: togliere "dati da verificare in CIT-AUDIT-8". |
| B14 | Aharonov, Bohm, *Significance of electromagnetic potentials in the quantum theory* | SYS l.214 | **VERIFICATO** (metadati) | Phys. Rev. 115(3) (1959) 485–491, DOI 10.1103/PhysRev.115.485 (Crossref) | Nessuna. |
| B15 | Boman, *Differentiability of a function and of its compositions with functions of one variable* | DICT l.54 (DICT-U2) | **DATI CORRETTI** (metadati) | Math. Scand. 20 (1967) p. 249–, DOI 10.7146/math.scand.a-10835 (Crossref dà solo la pagina iniziale) | DICT l.54: "Math. Scand.? 1967" → "Math. Scand. 20 (1967) 249–268". La pagina finale 268 è da memoria; con il DOI è sufficiente. |
| B16 | Slovák 1987 (Reidel, 283–294) e 1988 | DICT l.54 | **VERIFICATO** (audit precedenti) | in bib | Nessuna. |
| B17 | Trefethen, Weideman, *The exponentially convergent trapezoidal rule* | DICT l.98 | **PARZIALE** | SIAM Rev. 56(3) (2014) 385–458, DOI 10.1137/130932132 (Crossref) | Metadati corretti; il numero Thm 5.1 non è stato letto. |
| B18 | Christensen, *On sets of Haar measure zero in abelian Polish groups* | DICT l.180 | **VERIFICATO** (metadati) | Israel J. Math. 13(3–4) (1972) 255–260, DOI 10.1007/BF02762799 (Crossref) | Aggiungere i metadati. |
| B19 | Hunt, Sauer, Yorke, *Prevalence: a translation-invariant "almost every" on infinite-dimensional spaces* | DICT l.180 | **VERIFICATO** (metadati) | Bull. AMS 27(2) (1992) 217–238, DOI 10.1090/S0273-0979-1992-00328-2 (Crossref) | Dati di DICT corretti. |
| B20 | Caffarelli, Silvestre 2007 | DICT l.118 | **VERIFICATO** (in bib) | CPDE 32 (2007) 1245–1260 | Nessuna. |
| B21 | Weiss, Tabor, Carnevale, *The Painlevé property for partial differential equations* | DICT l.329 | **VERIFICATO** (metadati) | J. Math. Phys. 24(3) (1983) 522–526, DOI 10.1063/1.525721 (Crossref) | Dati corretti. |
| B22 | Weiss, *On classes of integrable systems and the Painlevé property* | DICT l.329 | **VERIFICATO** (metadati) | J. Math. Phys. 25(1) (1984) 13–24, DOI 10.1063/1.526009 (Crossref) | Dati corretti. |
| B23 | Owhadi, *Multigrid with rough coefficients and multiresolution operator decomposition from hierarchical information games* | ENC l.523 | **VERIFICATO** (metadati) | SIAM Rev. 59(1) (2017) 99–149, DOI 10.1137/15M1013894 (Crossref) | Dati corretti (in bib c'è solo Owhadi2019). |
| B24 | Thaller 1992, *The Dirac Equation*, cap. 5 | ENC l.525 | **PARZIALE** (memoria) | — | Capitolo non controllato. |
| B25 | Hochbruck, Lubich 2003 | VAR l.227; CONV l.297 | **VERIFICATO** (AUDIT-6) | in bib | Nessuna. |
| B26 | Moan, Niesen 2008, Thm 3 | VAR l.323; CONV l.297 | **PARZIALE** | in bib | Numero del teorema non riletto. |
| B27 | Faris, Lavine 1974 | sostegno di A17 | **VERIFICATO** (metadati; secondaria) | vedi A17 | Fonte nuova da aggiungere in ENC. |
| B28 | Pommaret, *Macaulay inverse systems revisited* | sostegno di A1 (nuova) | **VERIFICATO** (primaria) | arXiv:0902.2314v2 (2010) | Thm 5.2.5. Nella conclusione dice che l'approccio evita l'uso sistematico dell'inviluppo iniettivo di Oberst. |
| B29 | Engel, Nagel III.1 | CONV l.297 | **PARZIALE** (memoria) | — | Numero non letto. |
| B30 | Nečas 1967 / Grisvard 1985 | CONV l.227 | **PARZIALE** (memoria) | — | Nessun numero citato; uso generico. |
| B31 | Hörmander III, 18.1.13 | AUDIT_S8-DICT | **PARZIALE** (memoria) | — | Numero non letto. |
| B32 | Kato (domini comuni, condizione C¹) | ENC l.216 | **PARZIALE** (memoria) | — | Non verificato. |

**Priorità C (non riconteggiate).** Peetre 1959/60, Sun 1993, Nakamura–Sun–Uhlmann 1995, Radford 1996, Booth–Legg–Jarvis 2001, Morozov 1966, Engl–Hanke–Neubauer 1996, Mathé–Pereverzev 2003, Chen–Billings–Luo 1989, Bagby–Bos–Levenberg 2002, Pinkus 1985, Prenter 1970 e Macaulay (sistemi inversi) sono già trattati negli audit precedenti. I dati scritti in F8 non contraddicono quelli in bib; non li ho riletti uno per uno. Il rinvio a Kelly è stato tolto in CONV-7.

## 3. Rischio di novità

| claim | rischio | motivazione |
|---|---|---|
| SYS-EX / SYS-N1 / SYS-T0 su ℝ^n | **altissimo** | Oberst 1993 (abstract) determina μ(S) costruttivamente e caratterizza μ(S) ≤ 1 come principalità di Macaulay. Per lunghezza finita, "zoccoli ≤ 1" è il classico tipo 1 / Gorenstein (Macaulay §82). Pommaret 2010 Thm 5.2.5 dà la formula max dim soc_m. Il delta difendibile resta: (i) Ω arbitrario senza iniettività di C^∞(Ω); (ii) costruzione esplicita; (iii) lettura come criterio di identificazione. Riclassificare il caso ℝ^n come NOTO. |
| SYS-T1 | basso (standard) | Dualità di Matlis e cogeneratore iniettivo: già declassato in F8. |
| SYS-R1 / VAR-VMPUM | basso–medio | SLZ 2011 copre MPUM e VMPUM per segnali polinomiali e polinomiali-esponenziali con algebre di Ore. Il delta di VAR (1)–(4) va mantenuto esplicito. |
| VAR-L0–L2 | alto (noto) | Isakov 1993 (n = 1, tipo Schrödinger, attraverso x = cost) e Saut–Scheurer 1987 (parabolico). VAR-L1 su grafico non caratteristico x = g(t) è al massimo una variante. |
| ENC-K1′ | alto | Andrianov–Sokolov 2003 e Sokolov 2008 (abstract): fattorizzazione degli intertwiner in catene di Darboux elementari con coefficienti non singolari. ENC lo dice già "quasi certamente noto"; confermato a livello di abstract. |
| ENC-K1 | noto | Duistermaat–Grünbaum 1986 con V → 0, più Wilson 1993. |
| ENC-P0′-DIC | classico | Bluman–Shtelen 1996 §2. Con la precisazione su θ di A16. |
| DICT U2-a | basso come novità, corretto come uso | È la versione locale di KMS 18.16 sull'intorno di KMS 19.10. Dichiararlo. |

## 4. Esiti riassuntivi

Voci contate: 55 (A1–A23, B1–B32).

| esito | n. |
|---|---|
| VERIFICATO | 28 |
| DATI CORRETTI | 9 |
| CONTENUTO DIVERSO | 0 |
| NON TROVATO | 0 |
| PARZIALE | 18 |

- **DATI CORRETTI:** A10 Casas (CONV), A11 Pöschl–Teller, A14 Wilson, A17 Reed–Simon II, A18 Mehler, A20 Einkemmer–Ostermann, B3 Stein, B11 Sokolov, B15 Boman.
- **PARZIALE:** A2 Oberst 1990, A8 Saut–Scheurer, A15 Marchenko/Povzner/Levitan, A21 Dang–Einkemmer–Ostermann, A22 Ax, B2 𝒟′ convesso, B4 Pazy, B5 Folland, B6 vdPS, B8 Matsumura, B12 Niederer, B17 Trefethen–Weideman Thm 5.1, B24 Thaller, B26 Moan–Niesen Thm 3, B29 Engel–Nagel, B30 Nečas/Grisvard, B31 Hörmander III 18.1.13, B32 Kato.
- **Nessun CONTENUTO DIVERSO.** Il punto più vicino è A16: la fonte è citata correttamente, ma l'enunciato del progetto su θ è troppo forte.

## 5. Correzioni per sessione (da girare dopo il Gate 8)

**S8-SYS**
1. PROOF_PACKAGE §1 l.13–36 e LEDGER SYS-EX: Oberst 1993 → MCSS 6(3) 264–288, DOI 10.1007/BF01211623; letto solo l'abstract. Aggiungere Pommaret 2010 (arXiv:0902.2314) Thm 5.2.5 e Macaulay §82. Riclassificare SYS-EX/N1/T0 su ℝ^n come NOTO; il delta resta Ω arbitrario e la costruzione esplicita.
2. Oberst 1995 → AAECC 6(4–5) 211–243, DOI 10.1007/BF01235717.
3. Oberst 1990: le pp. 24–36 e i §2–4 non sono stati letti; non citarli come verificati.
4. l.214 e LEDGER G-T2: Wu–Yang → PRD 12(12) 3845–3857, DOI 10.1103/PhysRevD.12.3845; togliere "da verificare". Aharonov–Bohm → 115(3) 485–491.
5. l.27 Matlis → Pacific J. Math. 8(3) 511–528. l.88 EHV → Invent. Math. 110 207–235. l.20 Matsumura §18: numero da controllare.

**S8-VAR**
1. l.75: Hörmander I (2ª ed.) Thm 8.6.5 confermato; togliere "numero da verificare".
2. LEDGER VAR-L2: Saut–Scheurer 1987 (JDE 66, 118–139) è per il caso parabolico; per tipo Schrödinger citare Isakov 1993 (JDE 105, 217–238, n = 1, attraverso x = cost). Lo stato resta PROBABILMENTE NOTO.
3. VAR-P8(c)(d): "Pöschl–Teller" → "Pöschl–Teller modificato (iperbolico)", con Z. Phys. 83 (1933) 143–151.
4. l.184: Crum → Q. J. Math. 6(1) 121–127, DOI 10.1093/qmath/6.1.121. Togliere Crum, Casas e SLZ dalla lista l.323 dei numeri non verificati; Hörmander 8.6.5 esce anch'esso dalla lista.
5. l.225: Folland cap. 4 per Stone–von Neumann è dubbio (da memoria è il cap. 1); controllare. Pazy cap. 5 e vdPS 1.27/1.34 restano non verificati.
6. l.163: aggiungere il DOI di SLZ 10.1016/j.jsc.2011.08.001.
7. Mehler (VAR-T10): citare DLMF 18.18.28.

**S8-CONV**
1. l.297: Casas → "Thm 3.4: raggio π, ottimale (Es. 2); in dimensione infinita richiede Y normale". Togliere "costante π non letta".
2. l.142: Stein → "cap. VI §3, Thm 5 (p. 181)"; togliere "da verificare".
3. l.258–261: Einkemmer–Ostermann 2015 → titolo completo "… Part 1: Dirichlet boundary conditions", SIAM J. Sci. Comput. 37(3) A1577–A1592, DOI 10.1137/140994204. Dang–Einkemmer–Ostermann 2025 → titolo "An initial-boundary corrected splitting method for diffusion-reaction problems". CONV-Q6′ resta aperto: la norma non è nell'abstract.
4. l.217 (CONV-Q17): nessuna fonte per l'iniettività di 𝒟′(Ω), Ω convesso; mantenere l'esclusione.

**S8-ENC**
1. l.296 (ENC-P0′-DIC): "θ ≠ id ⟺ α ≢ 0" → "α ≢ 0 ⇒ θ non affine; α ≡ 0 ⟺ esiste un rappresentante con θ = id"; "a ≡ 0 ⇒ ρ ≡ 1" → "ρ costante". Fonte Bluman–Shtelen 1996 confermata (J. Phys. A 29(15) 4473–4480).
2. l.294 e LEDGER ENC-P0′: "Reed–Simon II (ess. autoagg. su 𝒮)" → "Reed–Simon II Thm X.38 (Faris–Lavine, CMP 35 (1974) 39–48)". l.216, §X.12: non verificato.
3. l.294/462: Mehler → DLMF 18.18.28; Mehler 1866, J. reine angew. Math. 66, 161–176.
4. l.384 (ENC-K1): aggiungere Wilson 1993 (J. reine angew. Math. 442, 177–204) per la Grassmanniana adelica bispettrale.
5. l.382 (ENC-K1′): Sokolov → J. Math. Sci. 151(2) (2008) 2924–2936; Andrianov–Sokolov → NPB 660 25–50. Rischio di novità alto, confermato.
6. ENC-A9(b4): "Pöschl–Teller modificato (iperbolico)". l.66 ENC-1: Marchenko cap. 1 senza numero di teorema.

**S8-DICT**
1. l.54: Boman → Math. Scand. 20 (1967) 249–268, DOI 10.7146/math.scand.a-10835.
2. l.320: Ax → "On Schanuel's conjectures", Ann. of Math. (2) 93(2) 252–268, DOI 10.2307/1970774. Il teorema differenziale resta CON-FONTE da leggere.
3. l.180: Christensen → Israel J. Math. 13(3–4) 255–260.
4. l.98: Trefethen–Weideman, Thm 5.1 non letto.
5. U2-a: facoltativo, dire "versione locale di KMS 18.16 sull'intorno di 19.10".

**CHECK-F8 / AUDIT-6**
- AUDIT-6 riga 19 (Casas): completare con Thm 3.4, ottimalità di π e ipotesi di normalità.

## 6. Provenienza (accesso 2026-10-27)

- Crossref tramite `doi.org` (CSL-JSON) e `api.crossref.org/works`: tutti i DOI in tabella.
- API arXiv: 1004.2924, hep-th/0301062, 0903.2835, 2504.10125.
- Testo pieno letto: Casas arXiv:0711.2381; Pommaret arXiv:0902.2314; Huang arXiv:1707.08548 (secondaria per Holmgren, Isakov, Saut–Scheurer); Simon arXiv:1711.00528 (secondaria per RS II Thm X.38); Bluman–Shtelen, PDF dell'autore (personal.math.ubc.ca/~bluman/jphysA96.pdf); KMS, PDF dell'autore (mat.univie.ac.at/~michor/kmsbookh.pdf), 18.16.
- Abstract: Oberst 1993, scheda ACNP unibo; Oberst 1995, pagina editoriale.
- Altre: DLMF §18.18 (eq. 18.18.28). Secondarie per Wilson 1993/1998 e Pöschl–Teller (rudn.ru, handwiki). Secondarie per Stein (arXiv:2305.01441; note Rogers, UConn).
- I PDF scaricati sono solo nello scratchpad della sessione.
