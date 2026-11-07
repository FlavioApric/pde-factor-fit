# BIBLIOGRAFIA — rapporto finale (CIT-BIBLIO, 26/10/2026)

Bibliografia completa delle fonti **effettivamente citate da claim** in `claims/LEDGER.md`, `REPORT_FINALE.md`, `work/*/PROOF_PACKAGE.md`, `work/KIEFFER/LETTURA.md` e `GATE3.md` §4, più R5-T1 (`research/R5/REPORT.md`, da cui dipende R5-T2). Le voci sono deduplicate; per ogni voce sono indicati la chiave BibTeX, il riferimento completo, il DOI/arXiv/URL, lo stato e i claim che la usano. Il file BibTeX corrispondente è `BIBLIOGRAFIA.bib`; contiene solo le voci VERIFICATA.

## Legenda degli stati

| sigla | stato | significato |
|---|---|---|
| **[VC]** | **VERIFICATA (numero controllato)** | Esistenza e metadati sono confermati. Il numero di teorema/sezione/pagina citato è stato confrontato con l'enunciato usato (prim. = testo della fonte letto; sec. = numero confermato da una fonte terza che cita esplicitamente quel numero). Per un articolo citato per intero, senza numero, vale [VC] se il contenuto usato è stato letto. |
| **[VN]** | **VERIFICATA (contenuto, numero non controllato)** | Esistenza e metadati sono confermati, e il contenuto usato è quello classico della fonte. Il numero citato (se c'è) non è stato confrontato col testo. "meta" = verificati solo i metadati (Crossref/arXiv/catalogo); il contenuto non è stato letto. |
| **[NT]** | **NON TROVATA** | Esistenza o metadati non confermati. |
| **[ER]** | **ERRATA** | La citazione **come compare oggi nei file del progetto** contiene un errore (numero, anno, attribuzione). Si indica la correzione. |

Metodo: (1) riuso degli esiti di CIT-AUDIT-2/3/4/5 e CIT-AUDIT-F5 (`research/CIT-AUDIT/`); (2) Crossref API (`works/<DOI>` e `query.bibliographic`) per tutte le voci con DOI, ri-eseguita in questa sessione; (3) arXiv API per gli identificativi arXiv; (4) ricerca web per i numeri portanti e per le voci senza DOI. Fonti terze lette in questa sessione: il PDF di Engel–Nagel GTM 194 ospitato dall'Università di Tubinga; C. O. Kiselman, *On fundamental solutions…* (2011, `www2.math.uu.se/~cki26691/fundamental2011.pdf`), che cita Hörmander ALPDO II Thm 10.2.1; le note di J. E. Fornæss (SMI Perugia 2021), che riportano la numerazione di Rudin RCA 3ª ed.; note di corso che seguono Humphreys §4.1 (Cor. A/B/C); fonti secondarie per Aronszajn §I.6 e per Kato 1983. I numeri confermati da fonte terza sono marcati "sec.".

---

## 1. Algebra, annullatori, operatori di Ore, D-moduli, algebra differenziale

- **Fulton2008** — W. Fulton, *Algebraic Curves. An Introduction to Algebraic Geometry*, ed. elettronica 2008 (orig. Benjamin 1969). URL: `dept.math.lsa.umich.edu/~wfulton/CurveBook.pdf`. **[VC]** prim.: §1.6 Prop. 2 p. 9; §5.3 p. 57 e Cor. 3 p. 58; §3.3 Proprietà (9) (CIT-AUDIT-2/3). Claim: C3-L2, C3-T2(c,d), R2-T3, II (intersezioni).
- **AtiyahMacdonald1969** — M. F. Atiyah, I. G. Macdonald, *Introduction to Commutative Algebra*, Addison-Wesley 1969. **[VC]** sec.: Prop. 2.4 (II-T1) e Prop. 7.14 (C3-L2; conferma debole) (CIT-AUDIT-3). Claim: II-T1, C3-L2.
- **Weibel1994** — C. A. Weibel, *An Introduction to Homological Algebra*, Cambridge Stud. Adv. Math. 38, CUP 1994. DOI 10.1017/CBO9781139644136. **[VC]** sec.: Thm 2.7.6 p. 63, §4.5. Claim: C12-L2.
- **CLO2015** — D. Cox, J. Little, D. O'Shea, *Ideals, Varieties, and Algorithms*, 4ª ed., UTM, Springer 2015. DOI 10.1007/978-3-319-16721-3. **[VN]** §3.5–3.6 (la numerazione dipende dall'edizione: nella 2ª ed. è §3.6 Prop. 1(ii); "Prop. 3 e 5" non confermate). Claim: C1C2 (risultanti), II. Non portante.
- **Humphreys1972** — J. E. Humphreys, *Introduction to Lie Algebras and Representation Theory*, GTM 9, Springer 1972. DOI 10.1007/978-1-4612-6398-2. **[ER]**. Il progetto usa la catena di ideali $\mathfrak i_k$ di codimensione 1 (algebra risolubile su ℂ), e cita "§4.1 Cor. A". In §4.1, Cor. A è la forma "a bandiera" (L ⊆ gl(V) risolubile stabilizza una bandiera), **Cor. B** è la catena di ideali con dim L_i = i, Cor. C è "[L,L] nilpotente" (sec.: note di corso strutturate su Humphreys §4.1). **Correzione: "Humphreys §4.1, Cor. B"** (oppure "Cor. A applicato ad ad L"). Il contenuto è corretto, l'ipotesi "campo algebricamente chiuso di caratteristica 0" è soddisfatta (ℂ). Claim: P1-T4.
- **Higham2008** — N. J. Higham, *Functions of Matrices: Theory and Computation*, SIAM 2008. DOI 10.1137/1.9780898717778. **[VC]** prim.: Def. 1.2, Thm 1.12. Claim: II-P5.
- **HornJohnsonMA2012** — R. A. Horn, C. R. Johnson, *Matrix Analysis*, 2ª ed., CUP 2012. DOI 10.1017/CBO9781139020411. **[VC]** sec.: Cor. 3.5.4 (2ª ed.). Il vecchio "Cor. 3.5.6" è già corretto nel package (CIT5-8). Claim: II-T7.
- **Borel1991** — A. Borel, *Linear Algebraic Groups*, 2ª ed., GTM 126, Springer 1991. DOI 10.1007/978-1-4612-0941-6. **[VN]**: "Prop. 14.4" (prodotto dei sottogruppi radice in ordine arbitrario = isomorfismo di varietà) non confrontata col testo; il fatto è stato verificato per k = 3 da S-CHECK. Claim: II (fattorizzazione unipotente). Non portante.
- **Ore1933** — O. Ore, "Theory of non-commutative polynomials", *Ann. of Math.* (2) 34(3) (1933) 480–508. DOI 10.2307/1968173. **[VN]** meta. Claim: II-T9, C12-P5, R4-T7, OP-ALG, OP-F5B, OP-R2.
- **BronsteinPetkovsek1996** — M. Bronstein, M. Petkovšek, "An introduction to pseudo-linear algebra", *Theoret. Comput. Sci.* 157(1) (1996) 3–33. DOI 10.1016/0304-3975(95)00173-5. **[VN]** meta. Claim: C1C2 (ord L₁L₂ = ord L₁ + ord L₂).
- **ChenKauersSinger2016** — S. Chen, M. Kauers, M. F. Singer, "Desingularization of Ore operators", *J. Symbolic Comput.* 74 (2016) 617–626. DOI 10.1016/j.jsc.2015.11.001. **[VN]** meta. Claim: R4-T7 (via C3).
- **vanderPutSinger2003** — M. van der Put, M. F. Singer, *Galois Theory of Linear Differential Equations*, Grundlehren 328, Springer 2003. DOI 10.1007/978-3-642-55750-7. **[VN]** (§2.1 non controllato). Claim: II-T9, C3.
- **Oberst1990** — U. Oberst, "Multidimensional constant linear systems", *Acta Appl. Math.* 20 (1990) 1–175. DOI 10.1007/BF00046908. **[VN]** meta. Claim: C3-T1(c) (dualità di Oberst, folklore), II.
- **Palamodov1970** — V. P. Palamodov, *Linear Differential Operators with Constant Coefficients*, Grundlehren 168, Springer 1970. DOI 10.1007/978-3-642-46219-1. **[VN]** meta. Claim: II (principio fondamentale), R2-T1.
- **Cohen1993** — H. Cohen, *A Course in Computational Algebraic Number Theory*, GTM 138, Springer 1993. DOI 10.1007/978-3-662-02945-9. **[VN]**: le sedi §4.2 p. 156, §3.3.2 p. 118, §3.5 p. 132, §3.6.2 p. 142, §3.6.3 p. 145 vengono dall'indice; gli enunciati non sono stati letti. Claim: P4-T6, OP-ALG-T1 (ipotesi (AC)), OP-F5C.
- **Loos1982** — R. Loos, "Computing in algebraic extensions", in *Computer Algebra* (Buchberger–Collins–Loos eds.), Computing Suppl. 4, Springer 1982, 173–187. DOI 10.1007/978-3-7091-3406-1_12. **[VN]** meta. Claim: P4 (AC).
- **Trager1976** — B. M. Trager, "Algebraic factoring and rational function integration", *Proc. SYMSAC '76*, ACM 1976, 219–226. DOI 10.1145/800205.806338. **[VN]** meta. Claim: P4 (AC).
- **Ritt1950** — J. F. Ritt, *Differential Algebra*, AMS Colloq. Publ. 33, 1950. DOI 10.1090/coll/033. **[VN]** (cap. II, numeri non controllati). Claim: OP-F5C (insieme caratteristico), S4-INTEG.
- **Kolchin1973** — E. R. Kolchin, *Differential Algebra and Algebraic Groups*, Pure Appl. Math. 54, Academic Press 1973. **[VN]**: esistenza confermata (capitoli della serie su ScienceDirect, Crossref); "cap. IV" e "p. 160 Prop. 4" (CIT-AUDIT-4) non riletti. Claim: OP-F5C, S4-INTEG (zero generico).
- **GoodearlWarfield2004** — K. R. Goodearl, R. B. Warfield Jr., *An Introduction to Noncommutative Noetherian Rings*, 2ª ed., LMS Student Texts 61, CUP 2004. DOI 10.1017/CBO9780511841699. **[VN]** (cap. 10, numeri non controllati). Claim: OP-ALG, OP-R2 (localizzazione di Ore).
- **McConnellRobson2001** — J. C. McConnell, J. C. Robson, *Noncommutative Noetherian Rings*, GSM 30, AMS 2001. DOI 10.1090/gsm/030. **[VN]** (§2.1). Claim: OP-F5B, OP-R2.
- **BrunsHerzog1998** — W. Bruns, J. Herzog, *Cohen–Macaulay Rings*, ed. riv., Cambridge Stud. Adv. Math. 39, CUP 1998 (1ª ed. 1993). DOI 10.1017/CBO9780511608681. **[VN]** (§1.5, §2.2). Claim: OP-F5C (L2, serie di Hilbert).
- **Zeilberger1990** — D. Zeilberger, "A holonomic systems approach to special functions identities", *J. Comput. Appl. Math.* 32(3) (1990) 321–368. DOI 10.1016/0377-0427(90)90042-X. **[VN]** meta. Claim: OP-ALG (letteratura).
- **Chyzak2000** — F. Chyzak, "An extension of Zeilberger's fast algorithm to general holonomic functions", *Discrete Math.* 217 (2000) 115–134. DOI 10.1016/S0012-365X(99)00259-9. **[VN]** meta. Claim: OP-ALG.
- **SST2000** — M. Saito, B. Sturmfels, N. Takayama, *Gröbner Deformations of Hypergeometric Differential Equations*, Algorithms Comput. Math. 6, Springer 2000. DOI 10.1007/978-3-662-04112-3. **[VN]** meta. Claim: OP-ALG.
- **OTT2001** — T. Oaku, N. Takayama, H. Tsai, "Polynomial and rational solutions of holonomic systems", *J. Pure Appl. Algebra* 164 (2001) 199–220. DOI 10.1016/S0022-4049(00)00153-5; arXiv:math/0001064. **[VC]** (abstract letto, CIT-AUDIT-F5). Claim: OP-ALG-L4.
- **Takayama1992** — N. Takayama, "An approach to the zero recognition problem by Buchberger algorithm", *J. Symbolic Comput.* 14(2–3) (1992) 265–282. DOI 10.1016/0747-7171(92)90039-7. **[VN]** meta. Autore e sede sono ora **confermati** (il package OP-ALG li dava come "non confermati"). Claim: OP-ALG-P1 (letteratura).
- **Shohat1936** — J. Shohat, "The relation of the classical orthogonal polynomials to the polynomials of Appell", *Amer. J. Math.* 58(3) (1936) 453–464. DOI 10.2307/2370962. **[VC]** (CIT-AUDIT-2). Claim: C12-P6.

## 2. PDE lineari: Malgrange, Ehrenpreis, Hörmander, principio fondamentale, analiticità

- **Malgrange1955** — B. Malgrange, "Existence et approximation des solutions des équations aux dérivées partielles et des équations de convolution", *Ann. Inst. Fourier* 6 (1955–56) 271–355. DOI 10.5802/aif.65. **[VC]** prim.: Chap. I §2 Thm 2 p. 292. Claim: C3-P1[gen], R2-T1, OPF-T4(iii), OP-F5B.
- **Ehrenpreis1970** — L. Ehrenpreis, *Fourier Analysis in Several Complex Variables*, Pure Appl. Math. 17, Wiley-Interscience 1970. **[VN]** (record di catalogo: ISBN 0471234001; non in Crossref). Claim: R2-T1 (principio fondamentale), P1 (P1-Q2, solo come via aperta).
- **HormanderICASV1990** — L. Hörmander, *An Introduction to Complex Analysis in Several Variables*, 3ª ed., North-Holland 1990. **[VC]** sec.: Thm 7.6.14 (C3-P1[gen], CIT-AUDIT-2). **[VN]** per "Thm 1.4.4" (soluzione C^∞ di ∂u/∂z̄ = f su aperti del piano; numero non trovato da CIT-AUDIT-F5 né in questa sessione). Claim: C3-P1[gen], OPF-T4(iv)(c).
- **HormanderALPDO1** — L. Hörmander, *The Analysis of Linear Partial Differential Operators I*, 2ª ed., Grundlehren 256, Springer 1990 (Classics 2003). DOI 10.1007/978-3-642-61497-2. **[VN]**. Thm 1.4.5, 2.2.1, 2.2.4 (incollamento di distribuzioni), 3.1.4′ (distribuzioni con derivata nulla in una variabile): numeri non controllati, non portanti (C3: 3.1.4′ sostituito dal Fatto (H); C1C2: 2.2.4 solo come richiamo). Claim: C3-T1 (non portante), C1C2.
- **HormanderALPDO2** — L. Hörmander, *The Analysis of Linear Partial Differential Operators II. Differential Operators with Constant Coefficients*, Grundlehren 257, Springer 1983 (Classics 2005). DOI 10.1007/b138375. **[VC]** sec. per **Thm 10.2.1**: "ogni P(D) ≠ 0 a coefficienti costanti ha una soluzione fondamentale in B^{loc}_{∞,P̃}". Confermato da Kiselman 2011, che cita "Hörmander 1983: Theorem 10.2.1" con questo enunciato. **[VC]** dall'indice (GBV) per §10.6–10.8 pp. 41–58, §11.1 p. 61, §11.4 pp. 85–91. Claim: OP-F5B-T1 [F1] (portante), OPF-T4(iii), OPR2-T1 (§11.1), C3-P5(b) (§11.4).
- **Petrowsky1939** — I. G. Petrowsky, "Sur l'analyticité des solutions des systèmes d'équations différentielles", *Mat. Sb.* 5(47)(1) (1939) 3–70. URL `mathnet.ru/eng/sm5769`. **[VN]** meta (Math-Net.ru, EuDML). Claim: C3-P5(b).
- **John1982** — F. John, *Partial Differential Equations*, 4ª ed., Appl. Math. Sci. 1, Springer 1982. DOI 10.1007/978-1-4684-0059-5. **[VC]** sec.: cap. 7 §1(a) pp. 211–213 (CIT-AUDIT-3). Claim: P1-P1(b).
- **Tychonoff1935** — A. Tychonoff, "Théorèmes d'unicité pour l'équation de la chaleur", *Mat. Sb.* 42(2) (1935) 199–216. **[VC]** (CIT-AUDIT-3; non in Crossref). Claim: P1-P1(b).
- **Folland1995** — G. B. Folland, *Introduction to Partial Differential Equations*, 2ª ed., Princeton Univ. Press 1995. DOI 10.2307/j.ctvzsmfgn. **[VN]** (cap. 1, pp. 30–65; numero di Cauchy–Kovalevskaya non controllato). Claim: P4-L7, P4-T5.
- **Evans2010** — L. C. Evans, *Partial Differential Equations*, 2ª ed., GSM 19, AMS 2010. DOI 10.1090/gsm/019. **[VC]** sec. (sezioni): §4.6.3 (Cauchy–Kovalevskaya), §3.4.2–3.4.3 (Lax–Oleinik), §11.4.3 (entropia/Kružkov) (CIT-AUDIT-5, F5). Claim: P4-L7, S4T-L2/T3 [F1], OPA-T1 [F1].
- **Driver2003** — B. K. Driver, *Math 231 Lecture Notes* (UCSD 2002–03), cap. 4 "Cauchy–Kovalevskaya Theorem", URL `mathweb.ucsd.edu/~bdriver/231-02-03/Lecture_Notes/pde4.pdf`. **[VC]** prim.: Thm 4.7 (CIT-AUDIT-5). Claim: P4-L7, OP-T1 (unicità analitica).
- **KrantzParks2002** — S. G. Krantz, H. R. Parks, *A Primer of Real Analytic Functions*, 2ª ed., Birkhäuser 2002. DOI 10.1007/978-0-8176-8134-0. **[VN]**: §2.3 è "The Implicit Function Theorem"; "Thm 2.3.5" (IFT reale-analitico) non confrontato col testo. Claim: OP-T1 (IFT-ω), portante; c'è un'alternativa con prova propria (maggioranti) nel package.
- **RosenbloomWidder1959** — P. C. Rosenbloom, D. V. Widder, "Expansions in terms of heat polynomials and associated functions", *Trans. Amer. Math. Soc.* 92 (1959) 220–266. DOI 10.1090/S0002-9947-1959-0107118-2. **[VN]** meta. Claim: C12-T6, P3-T5 (solo nome e definizione).
- **RudinRCA1987** — W. Rudin, *Real and Complex Analysis*, 3ª ed., McGraw-Hill 1987. **[VC]** sec.: **Thm 13.11, p. 274**, la lista di condizioni equivalenti per una regione piana semplicemente connessa (le note di Fornæss citano "Theorem 13.11 page 274, points (b) and (j)"). **[VN]** per il teorema di Runge (cap. 13, numero non controllato). Claim: C12-P10, OPF-P4 (Runge), OPF-T4(iv)(d).
- **Stein1970** — E. M. Stein, *Singular Integrals and Differentiability Properties of Functions*, Princeton Math. Ser. 30, PUP 1970. DOI 10.1515/9781400883882. **[VC]** sec.: cap. VI §3 pp. 180–192 (operatore di estensione; "Theorem 5" non controllato). Claim: OP-F5B [F2], OPR2-T1.
- **AdamsFournier2003** — R. A. Adams, J. J. F. Fournier, *Sobolev Spaces*, 2ª ed., Pure Appl. Math. 140, Academic Press/Elsevier 2003. **[VC]** sec.: Thm 3.22 (densità di C^∞(Ω̄), CIT-AUDIT-F5). Claim: OPF-T5, OPF-L3, C1C2.
- **MeyersSerrin1964** — N. G. Meyers, J. Serrin, "H = W", *Proc. Nat. Acad. Sci. USA* 51 (1964) 1055–1056. DOI 10.1073/pnas.51.6.1055. **[VN]** meta. Claim: OPF-L3.
- **deRham1955** — G. de Rham, *Variétés différentiables. Formes, courants, formes harmoniques*, Act. Sci. Ind. 1222, Hermann 1955. **[VN]** (catalogo/nLab). Claim: OPF-T4, C1C2.
- **Warner1983** — F. W. Warner, *Foundations of Differentiable Manifolds and Lie Groups*, GTM 94, Springer 1983. DOI 10.1007/978-1-4757-1799-0. **[VN]** (cap. 5). Claim: OPF-T4.
- **Bredon1997** — G. E. Bredon, *Sheaf Theory*, 2ª ed., GTM 170, Springer 1997. DOI 10.1007/978-1-4612-0647-7. **[VN]** meta. Claim: OPF-T4.
- **Lee2013** — J. M. Lee, *Introduction to Smooth Manifolds*, 2ª ed., GTM 218, Springer 2013. DOI 10.1007/978-1-4419-9982-5. **[VN]** (cap. 11 forme chiuse/esatte, cap. 17 de Rham; numeri non controllati). Claim: C1C2 (H¹_dR = 0 su semplicemente connessi). Non portante.

## 3. Analisi funzionale e somme di sottospazi

- **Aronszajn1950** — N. Aronszajn, "Theory of reproducing kernels", *Trans. Amer. Math. Soc.* 68(3) (1950) 337–404. DOI 10.1090/S0002-9947-1950-0051437-7. **[VC]** sec.: Part I §6 (somma di nuclei riproducenti: H(K₁+K₂) = H(K₁)+H(K₂) con norma minima sulle scomposizioni). La sede "§I.6" è confermata da una fonte terza (arXiv:1202.4443, "Aronszajn 1950, §I.6"). Claim: C12-T5, R1-T1, P2 (split di energia minima), C12-P7.
- **Deutsch2001** — F. Deutsch, *Best Approximation in Inner Product Spaces*, CMS Books, Springer 2001. DOI 10.1007/978-1-4684-9298-9. **[VN]** ("9.35" non controllato; non più portante). Claim: C12-P7, P2, OP-R2.
- **Kato1995** — T. Kato, *Perturbation Theory for Linear Operators*, ristampa Classics 1995 della 2ª ed. 1980, Springer. DOI 10.1007/978-3-642-66282-9. **[VN]** (I §5.3/§5.6, II §1.2: parziale). Claim: II, P3 (Kato modo per modo).
- **Nazarov1993** — F. L. Nazarov, "Local estimates for exponential polynomials and their applications to inequalities of the uncertainty principle type", *Algebra i Analiz* 5(4) (1993) 3–66; trad. *St. Petersburg Math. J.* 5(4) (1994) 663–717. **[VN]** (il primario non è stato letto; Crossref non restituisce la traduzione). Claim: OPA-T3(e).
- **FriedlandYomdin2011** — O. Friedland, Y. Yomdin, "An observation on the Turán–Nazarov inequality", arXiv:1107.0039. **[VC]** prim.: Thm 1.1 (CIT-AUDIT-F5; attribuzione riconfermata in questa sessione con l'arXiv API). Claim: OPA-T3(e).

## 4. Semigruppi e splitting (Trotter, Dyson–Phillips, Miyadera–Voigt, Wei–Norman)

- **EngelNagel2000** — K.-J. Engel, R. Nagel, *One-Parameter Semigroups for Linear Evolution Equations*, GTM 194, Springer 2000. DOI 10.1007/b97696. **[VC]** prim. (testo letto dal PDF dell'Università di Tubinga):
  - **II.2.7 "Product Semigroups"** (§II.2.a, pp. 59–65): per semigruppi C₀ commutanti, D(A)∩D(B) è un core per il generatore C del semigruppo prodotto e C = A+B su di esso. Coincide con R5-T1 (generatore = chiusura di A₁+A₂ su D(A₁)∩D(A₂)). La "numerazione da verificare" di R5 è confermata.
  - Thm III.3.14 p. 196, **Cor. III.3.16 p. 199** (Miyadera–Voigt: ∫₀^{t₀}‖BT(r)x‖dr ≤ q‖x‖, q < 1 ⇒ A+B genera), Cor. III.3.15.
  - Cor. III.5.8 (formula di Trotter con condizione di stabilità).
  - Claim: R5-T1 → R5-T2(i–iii); P3-L2(d); R5-T5.
- **Trotter1959** — H. F. Trotter, "On the product of semi-groups of operators", *Proc. Amer. Math. Soc.* 10(4) (1959) 545–551. DOI 10.1090/S0002-9939-1959-0108732-6. **[VN]** meta. Claim: R5-T1 (fonte alternativa), R5-T5.
- **Phillips1953** — R. S. Phillips, "Perturbation theory for semi-groups of linear operators", *Trans. Amer. Math. Soc.* 74(2) (1953) 199–221. DOI 10.1090/S0002-9947-1953-0054167-3. **[VN]** meta. Claim: P3-T1 (Dyson–Phillips), P1.
- **LumerPhillips1961** — G. Lumer, R. S. Phillips, "Dissipative operators in a Banach space", *Pacific J. Math.* 11(2) (1961) 679–698. DOI 10.2140/pjm.1961.11.679. **[VN]** meta. Claim: P1, P3 (contrazioni).
- **Dyson1949** — F. J. Dyson, "The radiation theories of Tomonaga, Schwinger, and Feynman", *Phys. Rev.* 75(3) (1949) 486–502. DOI 10.1103/PhysRev.75.486. **[VN]** meta. Claim: P3-L1/T1/T2, S4-TERM, OP-ANA, OP-F5A (serie di Dyson).
- **WeiNorman1963** — J. Wei, E. Norman, "Lie algebraic solution of linear differential equations", *J. Math. Phys.* 4(4) (1963) 575–581. DOI 10.1063/1.1703993. **[VN]** meta. Claim: P1-T4, II, OP-FUN.
- **WeiNorman1964** — J. Wei, E. Norman, "On global representations of the solutions of linear differential equations as a product of exponentials", *Proc. Amer. Math. Soc.* 15(2) (1964) 327–334. DOI 10.1090/S0002-9939-1964-0160009-0. **[VN]** (globalità per algebre risolubili: solo da fonti secondarie). Claim: P1-T4.
- **Pazy1983** — A. Pazy, *Semigroups of Linear Operators and Applications to Partial Differential Equations*, Appl. Math. Sci. 44, Springer 1983. DOI 10.1007/978-1-4612-5561-1. **[VC]** sec.: cap. 6 pp. 183–205 ("§6.3" non controllato). Claim: OPR2-T5 (LWP), R5-T5 (§3.5).
- **Henry1981** — D. Henry, *Geometric Theory of Semilinear Parabolic Equations*, LNM 840, Springer 1981. DOI 10.1007/BFb0089647. **[VC]** sec.: cap. 3 pp. 47–81. Claim: OPR2-T5.
- **HundsdorferVerwer2003** — W. Hundsdorfer, J. Verwer, *Numerical Solution of Time-Dependent Advection-Diffusion-Reaction Equations*, Springer Ser. Comput. Math. 33, 2003. DOI 10.1007/978-3-662-09017-6. **[VN]** (cap. IV). Claim: OP-ANA (splitting).
- **EinkemmerOstermann2015** — L. Einkemmer, A. Ostermann, "Overcoming order reduction in diffusion-reaction splitting. Part 1: Dirichlet boundary conditions", *SIAM J. Sci. Comput.* 37(3) (2015) A1577–A1592. DOI 10.1137/140994204. **[VN]** meta. Claim: OP-ANA.
- **Higham2008** (vedi §1) per BCH/funzioni di matrice.

## 5. Non lineare: Burgers, Cole–Hopf, Kružkov, Oleinik, KdV ben posta

- **Hopf1950** — E. Hopf, "The partial differential equation u_t + uu_x = μu_xx", *Comm. Pure Appl. Math.* 3(3) (1950) 201–230. DOI 10.1002/cpa.3160030302. **[VC]** (CIT-AUDIT-4). Claim: L-S, F4L-P3 [F-H], OPA-T1 [F2], S4-TERM, OP-F5A.
- **Cole1951** — J. D. Cole, "On a quasi-linear parabolic equation occurring in aerodynamics", *Quart. Appl. Math.* 9(3) (1951) 225–236. DOI 10.1090/qam/42889. **[VC]** (CIT-AUDIT-4). Claim: idem.
- **Kruzkov1970** — S. N. Kružkov, "First order quasilinear equations in several independent variables", *Math. USSR-Sb.* 10(2) (1970) 217–243. DOI 10.1070/SM1970v010n02ABEH002156. **[VC]** (CIT-AUDIT-F5; Lax–Oleinik = Kružkov via Evans §3.4/§11.4). Claim: S4T-L2, S4T-T3(i,ii,v–vii) [F1], OPA-T1 [F1], OPF5A-L3/T3.
- **Kuznetsov1976** — N. N. Kuznetsov, "Accuracy of some approximate methods for computing the weak solutions of a first-order quasi-linear equation", *USSR Comput. Math. Math. Phys.* 16(6) (1976) 105–119. DOI 10.1016/0041-5553(76)90046-X. **[VC]** (CIT-AUDIT-F5). Claim: S4T-T3(iv) [F3].
- **TangTeng1997** — T. Tang, Z.-H. Teng, "Viscosity methods for piecewise smooth solutions to scalar conservation laws", *Math. Comp.* 66(218) (1997) 495–526. DOI 10.1090/S0025-5718-97-00822-3. **[VC]** (CIT-AUDIT-4/F5). Claim: OPF5A-C1 (= OPA-Q1, ordine ν|log ν|), S4-TERM, OP-ANA.
- **GoodmanXin1992** — J. Goodman, Z. Xin, "Viscous limits for piecewise smooth solutions to systems of conservation laws", *Arch. Rational Mech. Anal.* 121(3) (1992) 235–265. DOI 10.1007/BF00410614. **[VN]** meta. Claim: S4-TERM (ordine O(ν) lontano dallo shock).
- **Wang1998** — W.-C. Wang, "On L¹ convergence rate of viscous and numerical approximate solutions of genuinely nonlinear scalar conservation laws", *SIAM J. Math. Anal.* 30(1) (1998) 38–52. DOI 10.1137/S0036141097316408. **[VN]** meta (testo non letto; il titolo è già corretto nei file). Claim: S4-INTEG (costante 4ν ln 2, solo "cfr.").
- **BenderBoettcherMilton1991** — C. M. Bender, S. Boettcher, K. A. Milton, "A new perturbative approach to nonlinear partial differential equations", *J. Math. Phys.* 32(11) (1991) 3031–3038. DOI 10.1063/1.529047. **[VN]** meta. Claim: S4-INTEG (letteratura δ-espansione).
- **BonaSmith1975** — J. L. Bona, R. Smith, "The initial-value problem for the Korteweg–de Vries equation", *Phil. Trans. R. Soc. Lond. A* 278(1287) (1975) 555–601. DOI 10.1098/rsta.1975.0035. **[VC]** (CIT-AUDIT-F5). Claim: S4ID-T4(iii), OP-C3′ (WP), OPR2.
- **Kato1983** — T. Kato, "On the Cauchy problem for the (generalized) Korteweg–de Vries equation", in *Studies in Applied Mathematics*, Adv. Math. Suppl. Stud. 8, Academic Press 1983, 93–128. **[VN]**: metadati confermati da tre bibliografie indipendenti (Ponce, RIMS Kôkyûroku; Kenig–Ponce–Vega, Duke 1993; Rev. Mat. Teor. Apl.); assente in Crossref. Claim: S4ID-T4(iii), OP-C3′ (WP).
- **Hoelder1887** — O. Hölder, "Ueber die Eigenschaft der Gammafunction keiner algebraischen Differentialgleichung zu genügen", *Math. Ann.* 28(1) (1887) 1–13. DOI 10.1007/BF02430507. **[VN]** meta. Crossref data il fascicolo al 1886, il volume 28 è del 1887: entrambe le date sono in uso, nessuna correzione necessaria. Claim: S4ID-T4(iii), OPR2.

## 6. Integrabile: IST, Lax, Hirota, Novikov, Riemann–Hilbert, Grunert–Teschl

- **GGKM1967** — C. S. Gardner, J. M. Greene, M. D. Kruskal, R. M. Miura, "Method for solving the Korteweg–deVries equation", *Phys. Rev. Lett.* 19(19) (1967) 1095–1097. DOI 10.1103/PhysRevLett.19.1095. **[VN]** meta. Claim: OP-C3′ (WP), OP-F5D.
- **Miura1968** — R. M. Miura, "Korteweg–de Vries equation and generalizations. I. A remarkable explicit nonlinear transformation", *J. Math. Phys.* 9(8) (1968) 1202–1204. DOI 10.1063/1.1664700. **[VN]** meta. Claim: OP-NL, S4-INTEG.
- **Lax1968** — P. D. Lax, "Integrals of nonlinear equations of evolution and solitary waves", *Comm. Pure Appl. Math.* 21(5) (1968) 467–490. DOI 10.1002/cpa.3160210503. **[VN]**. Claim: OP-P17 ((Lax) per n ≥ 4), INT-T1.
- **Lax1975** — P. D. Lax, "Periodic solutions of the KdV equation", *Comm. Pure Appl. Math.* 28(1) (1975) 141–188. DOI 10.1002/cpa.3160280105. **[VN]** meta. Claim: OP-NL, OPR2.
- **GelfandDickey1976** — I. M. Gel'fand, L. A. Dikii, "Fractional powers of operators and Hamiltonian systems", *Funct. Anal. Appl.* 10(4) (1976) 259–273. DOI 10.1007/BF01076025. **[ER]** nel package OP-NL (r. 183: "Gelfand–Dickey 1975: B_n = (L^{(2n+1)/2})_+"). **Correzione: Gel'fand–Dikii, Funct. Anal. Appl. 10 (1976) 259–273.** Il lavoro del 1975 (Russian Math. Surveys 30(5) 77–113) è un altro articolo, sulle espansioni asintotiche del risolvente. Il LEDGER r. 142 è già corretto. Claim: OP-P17.
- **AKNS1974** — M. J. Ablowitz, D. J. Kaup, A. C. Newell, H. Segur, "The inverse scattering transform – Fourier analysis for nonlinear problems", *Stud. Appl. Math.* 53(4) (1974) 249–315. DOI 10.1002/sapm1974534249. **[VN]**. Claim: OP-P18, INT-T2, OP-F5D.
- **ZakharovShabat1972** — V. E. Zakharov, A. B. Shabat, "Exact theory of two-dimensional self-focusing and one-dimensional self-modulation of waves in nonlinear media", *Sov. Phys. JETP* 34(1) (1972) 62–69 [orig. *Zh. Eksp. Teor. Fiz.* 61(1) (1971) 118–134]. **[VN]** meta (indice JETP; assente in Crossref). Claim: INT-T2 [ZS], OP-P18, OP-F5D.
- **KayMoses1956** — I. Kay, H. E. Moses, "Reflectionless transmission through dielectrics and scattering potentials", *J. Appl. Phys.* 27(12) (1956) 1503–1508. DOI 10.1063/1.1722296. **[VN]**. Claim: OP-NL, OP-F5C, OP-F5D, INT-T1(B).
- **DeiftTrubowitz1979** — P. Deift, E. Trubowitz, "Inverse scattering on the line", *Comm. Pure Appl. Math.* 32(2) (1979) 121–251. DOI 10.1002/cpa.3160320202. **[VN]** (enunciato da fonte secondaria). Claim: INT-T1 [F1–F4], OP-NL.
- **Hirota1971** — R. Hirota, "Exact solution of the Korteweg–de Vries equation for multiple collisions of solitons", *Phys. Rev. Lett.* 27(18) (1971) 1192–1194. DOI 10.1103/PhysRevLett.27.1192. **[VN]** meta. Claim: S4-INTEG, OP-F5D (non usato nelle prove (a)–(e)).
- **Novikov1974** — S. P. Novikov, "The periodic problem for the Korteweg–de Vries equation", *Funct. Anal. Appl.* 8(3) (1974) 236–246. DOI 10.1007/BF01075697. **[VN]**. Claim: OPR2-P4, OP-F5C, S4ID.
- **GesztesyHolden2003** — F. Gesztesy, H. Holden, *Soliton Equations and Their Algebro-Geometric Solutions. Vol. I*, Cambridge Stud. Adv. Math. 79, CUP 2003. DOI 10.1017/CBO9780511546723. **[VN]** meta. Claim: OP-F5C (Novikov).
- **Marchenko1986** — V. A. Marchenko, *Sturm–Liouville Operators and Applications*, Oper. Theory Adv. Appl. 22, Birkhäuser 1986. DOI 10.1007/978-3-0348-5485-6. **[VN]** meta (§4.2 non controllato). Claim: OP-C3′ (WP), S4-INTEG.
- **AblowitzSegur1981** — M. J. Ablowitz, H. Segur, *Solitons and the Inverse Scattering Transform*, SIAM Stud. Appl. Math. 4, SIAM 1981. DOI 10.1137/1.9781611970883. **[VN]** meta. Claim: S4-INTEG (tabella, "non letto").
- **EckhausVanHarten1981** — W. Eckhaus, A. van Harten, *The Inverse Scattering Transformation and the Theory of Solitons*, North-Holland Math. Stud. 50, 1981. **[VN]** meta (capitoli in Crossref, serie DOI 10.1016/S0304-0208(08)…). Claim: OP-C3′ (WP).
- **BealsCoifman1984** — R. Beals, R. R. Coifman, "Scattering and inverse scattering for first order systems", *Comm. Pure Appl. Math.* 37(1) (1984) 39–90. DOI 10.1002/cpa.3160370105. **[VN]**. Claim: INT-T2, OP-NL.
- **Zhou1989** — X. Zhou, "Direct and inverse scattering transforms with arbitrary spectral singularities", *Comm. Pure Appl. Math.* 42(7) (1989) 895–938. DOI 10.1002/cpa.3160420702. **[VC]** (Ex. 3.3.16, CIT-AUDIT-F5). Claim: INT-T2, OP-NL, OP-F5D.
- **GrunertTeschl2009** — K. Grunert, G. Teschl, "Long-time asymptotics for the Korteweg–de Vries equation via nonlinear steepest descent", *Math. Phys. Anal. Geom.* 12(3) (2009) 287–324. DOI 10.1007/s11040-009-9062-2. **[VC]** prim.: Lemma 2.2, Thm 4.4/Cor. 4.5, Thm 5.4. Claim: S4ID-P8, OPR2-P7, OP-F5D (L13, P14), OP-C3′.
- **DeiftZhou1993** — P. Deift, X. Zhou, "A steepest descent method for oscillatory Riemann–Hilbert problems. Asymptotics for the MKdV equation", *Ann. of Math.* (2) 137(2) (1993) 295–368. DOI 10.2307/2946540. **[VN]**. Claim: S4ID-P8.
- **DVZ1994** — P. Deift, S. Venakides, X. Zhou, "The collisionless shock region for the long-time behavior of solutions of the KdV equation", *Comm. Pure Appl. Math.* 47(2) (1994) 199–206. DOI 10.1002/cpa.3160470204. **[VN]** meta. Claim: S4-ID (letteratura asintotica).
- **KVZ2018** — R. Killip, M. Vişan, X. Zhang, "Low regularity conservation laws for integrable PDE", *Geom. Funct. Anal.* 28(4) (2018) 1062–1090. DOI 10.1007/s00039-018-0444-0; arXiv:1708.05362. **[VC]** sec.: §1 letto (CIT/OP-F5D). Nei file è citato come "KVZ 2017" (data arXiv): è corretto, ma per la versione a stampa usare 2018. Claim: OP-F5D [Hm].
- **DJKM1982** — E. Date, M. Jimbo, M. Kashiwara, T. Miwa, "Transformation groups for soliton equations — Euclidean Lie algebras and reduction of the KP hierarchy", *Publ. RIMS* 18 (1982) 1077–1110 / serie "Transformation groups for soliton equations" (Physica D 4 (1982) 343–365, DOI 10.1016/0167-2789(82)90041-0). **[VN]** meta. La sede esatta citata nel package S4-INTEG non è specificata. Claim: S4-INTEG (letteratura).
- **SandersWang1998** — J. A. Sanders, J. P. Wang, "On the integrability of homogeneous scalar evolution equations", *J. Differential Equations* 147(2) (1998) 410–434. DOI 10.1006/jdeq.1998.3452. **[VN]** meta. Claim: S4-INTEG (nota).
- **Olver1993** — P. J. Olver, *Applications of Lie Groups to Differential Equations*, 2ª ed., GTM 107, Springer 1993. DOI 10.1007/978-1-4612-4350-2. **[VN]** (cap. 5). Claim: S4-INTEG, S4-ID.
- **UmemuraWatanabe1997** — H. Umemura, H. Watanabe, "Solutions of the second and fourth Painlevé equations, I", *Nagoya Math. J.* 148 (1997) 151–198. DOI 10.1017/S0027763000006486. **[VN]** meta. Claim: S4ID-T4(iv) ("∉ 𝔉").
- **FokasLiu1994** — A. S. Fokas, Q. M. Liu, "Nonlinear interaction of traveling waves of nonintegrable equations", *Phys. Rev. Lett.* 72(21) (1994) 3293–3296. DOI 10.1103/PhysRevLett.72.3293. **[VN]** meta. Claim: S4-ID (simmetrie condizionali).
- **Zhdanov1995** — R. Z. Zhdanov, "Conditional Lie–Bäcklund symmetry and reduction of evolution equations", *J. Phys. A* 28(13) (1995) 3841–3850. DOI 10.1088/0305-4470/28/13/027. **[VN]** meta. Claim: S4-ID.
- **SautScheurer1987** — J.-C. Saut, B. Scheurer, "Unique continuation for some evolution equations", *J. Differential Equations* 66(1) (1987) 118–139. DOI 10.1016/0022-0396(87)90043-X. **[VC]** sec.: Thm 1.1. Claim: INT-T1 [F-SS] (UC-1).
- **DLMF** — *NIST Digital Library of Mathematical Functions*, Release 1.2.x, §9.7(ii), URL `dlmf.nist.gov/9.7`. **[ER]** nel package OP-NL (r. 92: "DLMF 9.7.9–9.7.11"). **Correzione: DLMF 9.7.9–9.7.10.** Le formule 9.7.9–9.7.10 sono gli sviluppi di Ai e Ai′ per x → −∞; 9.7.11 riguarda Bi. Il LEDGER r. 142 è già corretto. **[VC]** prim. per 9.7.9–9.7.10. Claim: OP-O5.

## 7. Letteratura recente su identificazione e PDE-discovery

- **Kieffer2025** — T. F. Kieffer, J. Cupp, J. S. Van Dyke, P. Titum, M. L. Wall, "Robust series linearization of nonlinear advection-diffusion equations", arXiv:2512.12019 (12/12/2025). **[VC]** prim. (letto in `work/KIEFFER/LETTURA.md`; autori e data riconfermati con l'arXiv API). Claim: KIEFFER-C, S4-INTEG (confronto).
- **Scholl2026** — P. Scholl, A. Bacho, H. Boche, G. Kutyniok, "Symbolic recovery of differential equations: the identifiability problem", *Machine Learning* 115(6) (2026), art. 139. DOI 10.1007/s10994-026-07068-0; arXiv:2210.08342. **[VC]** prim.: Prop. 1, Tab. 1. Claim: ALG-T1(b), ALG-L1/P3/P4/P6, S4ID-C1(i), S4ID-L2/L4/L5/C2/P5/P6, C3.
- **HeZhaoZhong2024** — Y. He, H. Zhao, Y. Zhong, "How much can one learn a partial differential equation from its solution?", *Found. Comput. Math.* 24(5) (2024) 1595–1641 (online 2023). DOI 10.1007/s10208-023-09620-z. **[VN]** meta. Claim: C3, S4-ID, S4-INTEG (posizionamento).
- **Byrne2025** — H. Byrne, H. A. Harrington, A. Ovchinnikov, G. Pogudin, H. Rahkooy, P. Soto, "Algebraic identifiability of partial differential equation models", *Nonlinearity* 38(2) (2025) 025022. DOI 10.1088/1361-6544/ada510. **[VN]** meta. Claim: S4-ID.
- **Rudy2017** — S. H. Rudy, S. L. Brunton, J. L. Proctor, J. N. Kutz, "Data-driven discovery of partial differential equations", *Sci. Adv.* 3(4) (2017) e1602614. DOI 10.1126/sciadv.1602614. **[VN]** meta. Claim: S4-ID.

## 8. Formalizzazione: Lean / Mathlib

- **Mathlib2020** — The mathlib Community, "The Lean mathematical library", *Proc. CPP 2020*, ACM 2020, 367–381. DOI 10.1145/3372885.3373824. **[VN]** meta. Claim: righe Lean (S5-LEAN), REPORT §Lean.
- **Lean4_2021** — L. de Moura, S. Ullrich, "The Lean 4 theorem prover and programming language", *CADE-28*, LNCS 12699, Springer 2021, 625–635. DOI 10.1007/978-3-030-79876-5_37. **[VN]** meta. Claim: S5-LEAN.

---

## 9. Tabella Claim → fonte (tutti i claim CON-FONTE / CONDIZIONALE)

| claim | stato nel LEDGER | fonte/i | stato della fonte |
|---|---|---|---|
| P1-P1(b) | CON-FONTE (verificata) | John1982 cap. 7 §1(a); Tychonoff1935 | VC |
| P1-T4 | DIMOSTRATO + CON-FONTE | Humphreys1972 §4.1 (**Cor. B**, non A); WeiNorman1964 | **ER** (numero) / VN |
| P1-P4(b) | DIMOSTRATO | argomento dei caratteri (Rudin FA 10.27 rimosso) | — |
| II-T1 | DIMOSTRATO (fonte d'appoggio) | AtiyahMacdonald1969 Prop. 2.4 | VC sec. |
| II-T7 | DIMOSTRATO (prova breve) | HornJohnsonMA2012 Cor. 3.5.4 | VC sec. |
| II-T9 | CON-FONTE | Ore1933; vanderPutSinger2003 §2.1 | VN |
| II-P5 | DIMOSTRATO (fonte d'appoggio) | Higham2008 Def. 1.2, Thm 1.12 | VC |
| II (fattorizzazione) | — | Borel1991 Prop. 14.4 | VN |
| C3-P1[gen] | CON-FONTE (verificata) | Malgrange1955 Chap. I §2 Thm 2 p. 292; HormanderICASV1990 Thm 7.6.14 | VC |
| C3-L2, C3-T2(c,d) | DIMOSTRATO (fonti d'appoggio) | Fulton2008; AtiyahMacdonald1969 Prop. 7.14 | VC |
| C3-T1 | DIMOSTRATO | HormanderALPDO1 3.1.4′, 2.2.1 (non portanti); Oberst1990 | VN |
| C3-P5(b) | CON-FONTE | Petrowsky1939; HormanderALPDO2 §11.4 | VN / VC (indice) |
| C12-P5, R4-T7 | CON-FONTE | Ore1933; BronsteinPetkovsek1996; ChenKauersSinger2016 | VN |
| C12-P6 | CON-FONTE (verificata) | Shohat1936 | VC |
| C12-P7(a–d) | CON-FONTE | Deutsch2001; Aronszajn1950 | VN / VC |
| C12-P10 | CON-FONTE | RudinRCA1987 Thm 13.11 p. 274 | **VC sec.** (numero ora controllato) |
| C12-L2 | DIMOSTRATO | Weibel1994 Thm 2.7.6 | VC |
| C12-T5, R1-T1 | CON-FONTE | Aronszajn1950 §I.6 | **VC sec.** |
| C12-T1′ | DIMOSTRATO (sostituisce Malgrange–Ehrenpreis) | — | — |
| R2-T1 → R2-T3 | CON-FONTE | Malgrange1955; Ehrenpreis1970; Palamodov1970; Fulton2008 | VC / VN |
| R5-T1 → R5-T2(i–iii) | CON-FONTE | EngelNagel2000 **II.2.7**; Trotter1959 | **VC prim.** (numero ora controllato) |
| P3-L2(d) | CON-FONTE (verificata) | EngelNagel2000 Thm III.3.14, Cor. III.3.15–3.16 | VC prim. |
| P3-T1, P3-L1 | DIMOSTRATO | Dyson1949; Phillips1953 (nomi) | VN |
| P4-L7, P4-T5 | CON-FONTE con sede | Folland1995 cap. 1; Evans2010 §4.6.3; Driver2003 Thm 4.7 | VN / VC |
| P4-T6, OP-ALG-T1 (AC) | CON-FONTE | Cohen1993; Loos1982; Trager1976 | VN |
| L-S, F4L-P3(i–iv) | CONDIZIONALE [F-H] | Hopf1950; Cole1951 | VC |
| INT-T1 (UC-1),(B),(C) | CONDIZIONALE [F-C, F-SS, F-MS, F1–F4] | SautScheurer1987 Thm 1.1; DeiftTrubowitz1979; KayMoses1956; Lax1968 | VC / VN |
| INT-T2 | CONDIZIONALE [ZS] | ZakharovShabat1972; AKNS1974; BealsCoifman1984; Zhou1989 | VN / VC |
| ALG-T1(b), ALG-L1/P3/P4/P6 | CON-FONTE | Scholl2026 Prop. 1, Tab. 1 | VC |
| S4ID-C1(i), L2, L4, L5, C2, P5, P6 | CON-FONTE | Scholl2026 | VC |
| S4ID-T4(iii) | CON-FONTE | Hoelder1887; BonaSmith1975; Kato1983 | VN / VC / VN |
| S4ID-T4(iv) | CON-FONTE | UmemuraWatanabe1997 | VN |
| S4ID-P8 | CONDIZIONALE | DeiftZhou1993; GrunertTeschl2009 | VN / VC |
| S4T-L2, S4T-T3(i,ii,v–vii) | DIMOSTRATO mod [F1] | Kruzkov1970; Evans2010 §3.4, §11.4 | VC |
| S4T-T3(iv) | CONDIZIONALE [F3] | Kuznetsov1976 | VC |
| S4T-T4(ii) | CONDIZIONALE [H-KB] | Hopf1950/Cole1951 (forma KdV–Burgers: ipotesi interna, nessuna fonte esterna) | — |
| OPA-T1 | mod [F1], [F2] | Kruzkov1970; Hopf1950/Cole1951 | VC |
| OPA-T3(e) | DIMOSTRATO (fonte letta) | FriedlandYomdin2011 Thm 1.1; Nazarov1993 | VC / VN |
| OPF5A-C1 (= OPA-Q1) | ordine CON-FONTE | TangTeng1997; GoodmanXin1992 | VC / VN |
| OP-T1 | CON-FONTE | KrantzParks2002 Thm 2.3.5; Driver2003 Thm 4.7 | VN / VC |
| OP-C3′ | CON-FONTE (WP) | BonaSmith1975; Kato1983; GGKM1967; Marchenko1986 §4.2; EckhausVanHarten1981; GrunertTeschl2009 §1 | VC / VN |
| OP-O5 | CON-FONTE → DIMOSTRATO | DLMF 9.7.9–9.7.10 | VC; **ER** nel package (9.7.11) |
| OP-P17 | CONDIZIONALE per n ≥ 4 | Lax1968; GelfandDickey1976 | VN; **ER** nel package (1975) |
| OP-P18 | CONDIZIONALE | AKNS1974; ZakharovShabat1972 | VN |
| OPF-P4 | DIMOSTRATO (Runge CON-FONTE) | RudinRCA1987 cap. 13 | VN |
| OPF-T4 (iii),(iv) | CON-FONTE | deRham1955; Warner1983; Bredon1997; HormanderALPDO2 §10.6–10.8; HormanderICASV1990 1.4.4; RudinRCA1987; Malgrange1955 | VN / VC |
| OPF-T5, OPF-L3 | CON-FONTE (densità) | AdamsFournier2003 Thm 3.22; MeyersSerrin1964 | VC / VN |
| OPR2-T1 | CON-FONTE | Stein1970 cap. VI §3; HormanderALPDO2 §11.1 | VC |
| OPR2-P4 | CON-FONTE | Novikov1974 | VN |
| OPR2-T5 | CON-FONTE (LWP) | Pazy1983 cap. 6; Henry1981 cap. 3 | VC |
| OPR2-P7 | CONDIZIONALE (SR) | GrunertTeschl2009; Novikov1974 | VC / VN |
| OP-F5B-T1 | mod F1, F2 | HormanderALPDO2 **Thm 10.2.1**; Stein1970 | **VC sec.** (numero ora controllato) |
| OP-F5C | CON-FONTE | Novikov1974; GesztesyHolden2003; BrunsHerzog1998; Ritt1950; Kolchin1973; Cohen1993 | VN |
| OP-F5D (L13, P14) | CONDIZIONALE ristretto | KayMoses1956; GrunertTeschl2009 Thm 5.4; KVZ2018 §1; Zhou1989 | VN / VC |
| OP-ALG-L4, P1 | letteratura | OTT2001; Takayama1992; SST2000; Zeilberger1990; Chyzak2000 | VC / VN |
| KIEFFER-C | CON-FONTE (lettura) | Kieffer2025 | VC |
| S5-LEAN | — | Mathlib2020; Lean4_2021 | VN |

## 10. Problemi

### 10.1 ERRATA ancora presenti nei file del progetto (da correggere a cura del coordinatore/package owner)

1. **Humphreys §4.1 "Cor. A"** (P1-T4; `work/P1/PROOF_PACKAGE.md` rr. 37, 234, 237, 324; LEDGER rr. 18, 62). L'enunciato usato, la catena di ideali di dimensione i, è **Cor. B**; Cor. A è la forma a bandiera in gl(V). Correzione: "Humphreys §4.1, Cor. B". Fonte secondaria: note di corso strutturate su Humphreys §4.1; una citazione isolata in arXiv:math/0308089 usa "Corollary 4.1 A" per un altro enunciato, quindi conviene ricontrollare sul libro. Il contenuto non cambia.
2. **Gelfand–Dickey "1975"** (OP-P17; `work/OP-NL/PROOF_PACKAGE.md` r. 183). Correzione: Gel'fand–Dikii, *Funct. Anal. Appl.* 10(4) (1976) 259–273, DOI 10.1007/BF01076025. Il LEDGER r. 142 è già corretto.
3. **DLMF "9.7.9–9.7.11"** (OP-O5; `work/OP-NL/PROOF_PACKAGE.md` r. 92). Correzione: 9.7.9–9.7.10 (9.7.11 riguarda Bi). Il LEDGER r. 142 è già corretto.

### 10.2 ERRATA già corretti in precedenza (solo traccia)

- Horn–Johnson MA "Cor. 3.5.6" → Cor. 3.5.4 (2ª ed.).
- Wang 1998: titolo corretto in "On L¹ convergence rate…".
- Weiss–Tabor–Carnevale: anno 1983 (J. Math. Phys. 24, 522–526, DOI 10.1063/1.525721). Non più citato da claim.
- arXiv:0704.3173 è Loutsenko–Spiridonov, non la fonte attribuita (bib di ricerca; non citato da claim).
- arXiv:1107.0039 è Friedland–Yomdin, non Nazarov. Nel package è ora attribuito correttamente.
- Gelfand–Dickey nel LEDGER (1976).
- DLMF nel LEDGER (9.7.9–9.7.10).

### 10.3 NON TROVATA

Nessuna voce citata da claim risulta inesistente o con metadati non confermabili. Due voci sono assenti da Crossref ma confermate per altra via: Kato 1983, con tre bibliografie indipendenti; Zakharov–Shabat 1972, con l'indice JETP. Per Zakharov–Shabat le pagine dell'originale russo variano tra le basi dati (118 secondo JETP, 12 secondo Math-Net.ru). Se si cita l'originale, conviene citare la traduzione inglese, JETP 34 (1972) 62–69.

### 10.4 Numeri non controllati (contenuto verificato) — da sanare o da dichiarare nel rapporto

- **Portanti:**
  - Krantz–Parks Thm 2.3.5 (OP-T1): §2.3 = IFT confermato, il numero no. Il package ha anche la prova per maggioranti, quindi si può citare "§2.3".
  - Cohen GTM 138 (AC): sedi solo dall'indice.
  - Hörmander SCV Thm 1.4.4 (OPF-T4(iv)(c)).
  - Rudin RCA, numero del teorema di Runge (OPF-P4).
- **Non portanti:**
  - Hörmander ALPDO I 1.4.5 / 2.2.1 / 2.2.4 / 3.1.4′
  - Lee ISM (cap. 11/17)
  - CLO "Prop. 3 e 5"
  - Borel LAG 14.4
  - Deutsch 9.35
  - van der Put–Singer §2.1
  - Kolchin cap. IV
  - Goodearl–Warfield cap. 10
  - McConnell–Robson §2.1
  - Marchenko §4.2
  - Pazy §6.3
  - Stein "Theorem 5"
  - Kato (Perturbation) IV §5.2

### 10.5 Numeri GATE3 §4 risolti in questa sessione

| citazione | esito |
|---|---|
| Rudin RCA 13.11 | **confermato** (p. 274; sec.) |
| Hörmander ALPDO 1.4.5 / 2.2.4 | non controllati; non portanti |
| Lee ISM | non controllato; non portante |
| CLO | non controllato; dipende dall'edizione |
| Humphreys "Cor. A" | **ERRATA → Cor. B** |
| Cohen GTM 138 | sedi da indice; enunciati non letti |

In più:
- **Hörmander ALPDO II Thm 10.2.1** (OP-F5B F1, portante): **confermato** (sec., Kiselman 2011).
- **Engel–Nagel II.2.7** (R5-T1): **confermato** (prim.).
- **Aronszajn §I.6** (C12-T5): **confermato** (sec.).
- **Takayama 1992**: autore e sede **confermati**.

## 11. Conteggi

Conteggi sulle 112 voci delle §§1–8. Higham, citato due volte, conta una volta. Ogni voce ha un solo stato, il primo indicato. HormanderICASV1990 e RudinRCA1987 contano come VC, DLMF come ER.

| stato | n. |
|---|---|
| VERIFICATA (numero controllato) [VC] | 34 |
| VERIFICATA (contenuto, numero non controllato) [VN] | 75 (di cui 45 solo metadati) |
| NON TROVATA [NT] | 0 |
| ERRATA [ER] | 3 (Humphreys Cor. A→B; Gelfand–Dickey 1975→1976; DLMF 9.7.11→9.7.10) |
