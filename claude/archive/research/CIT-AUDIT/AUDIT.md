# AUDIT — verifica delle citazioni di Fase 1 (CIT-AUDIT)

Data: 2026-10-22 · Agente: CIT-AUDIT · Ambito: i 15 `research/*/sources.bib` (625 voci, 445 opere distinte) e i riferimenti usati nei `REPORT.md`.

## 0. Metodo e skill
- **Skill caricate** (lette con Read; nessuno script `_vendor` eseguito):
  - `Auto-claude-code-research-in-sleep/skills/citation-audit/SKILL.md`: controllo su tre livelli (esistenza, metadati, contesto). I verdetti KEEP/FIX/REPLACE/REMOVE sono resi qui come VERIFICATO / METADATI ERRATI / NON TROVATO / CONTESTO NON SUPPORTATO.
  - `scientific-agent-skills/skills/citation-management/SKILL.md`: Crossref, arXiv e DOI come fonti canoniche; controllo dei duplicati.
  - `scientific-agent-skills/skills/paper-lookup/SKILL.md`: endpoint documentati; attenzione alle risposte "200 vuote".
  - Revisore Codex **escluso** per decisione dell'utente: tutte le verifiche le ha fatte CIT-AUDIT.
- **Livelli 1–2 (controllo automatico, con uno script scritto da CIT-AUDIT ed eseguito nel venv):**
  - DOI → `api.crossref.org/works/<doi>`.
  - eprint → `export.arxiv.org/api/query?id_list=`.
  - Voci senza DOI → `api.crossref.org/works?query.bibliographic=`. Una corrispondenza è accettata solo se la somiglianza del titolo è ≥ 0.85 e il primo autore compare.
  - Campi confrontati: titolo, anno, autori (numero e primo autore), volume, prima pagina.
  - Ogni discrepanza è stata rivista a mano. Quasi tutte erano falsi positivi: Crossref restituiva ristampe o recensioni dei libri.
- **Livello 3 (contesto) sui riferimenti prioritari.** Fonti lette:
  - Testo su arXiv: Scholl et al. v10, He–Zhao–Zhong v2, Donoho–Kutyniok, Casas–Murua–Nadinić v2, Robeva v3.
  - PDF dell'articolo o del libro: Jahnke–Lubich (BIT 2000), Engel–Nagel (testo completo), Tropp 2004.
  - Abstract Crossref: Pierce 1979, Stanhope–Rubin–Swigon, Rapisarda–Antoulas, Crawley-Boevey.
  - Fonti secondarie, quando il libro non era accessibile: Hörmander ICASV (Lomadze, LAA 438 (2013)); Higham (Higham–Al-Mohy 2010 e indice); Miller 1977 (indice Cambridge); Pazy (una citazione secondaria).
- **Categoria aggiuntiva VERIFICATO-K:** voce non indicizzata in Crossref (manuali classici, riviste sovietiche, serie storiche, pagine web). La riconosco come esistente e con metadati plausibili, ma **senza** riscontro via API. È una verifica a campione, non una conferma completa.
- **Limiti:** zbMATH e MathSciNet non usati; le pagine AMS (Zettl, Trans. AMS) sono bloccate da un controllo anti-bot; nessun libro cartaceo consultato.

## 1. Conteggi

| esito | voci (su 625) |
|---|---|
| VERIFICATO (riscontrato su Crossref, arXiv, DOI o sul testo) | 491 |
| VERIFICATO-K (riconosciuto, non indicizzato) | 123 |
| METADATI ERRATI (corretti in `sources_verified.bib`) | 8 |
| NON TROVATO (possibile allucinazione) | **0** |
| CONTESTO NON SUPPORTATO | 3 |

Nessuna voce risulta inventata. Gli errori di metadati sono titoli segnaposto, DOI o volumi scambiati e una voce che fonde due articoli. I problemi seri sono di **contesto**: in alcuni REPORT l'affermazione è più forte di quanto la fonte dimostri.

## 2. Errori che toccano risultati chiave (da sistemare prima del Gate 1)

1. **R8 → "G4 parte evolutiva NOTA" (RIPRESA §4H; R8 §(iii), raccomandazione 1): CONTESTO NON SUPPORTATO (parziale).**
   - He–Zhao–Zhong, FoCM 24 (2024), Thm 3.2 (letto su arXiv v2) dà solo una condizione **sufficiente**.
   - Ipotesi del teorema: dominio 𝕋^d; dati a due istanti t₁, t₂ vicini; |Q| = |supp û₀| oltre una soglia combinatoria; Q non contenuto in un'ipersuperficie algebrica di grado ≤ n (con soli termini pari o soli dispari).
   - G4, in NOTAZIONE, è invece un "se e solo se" (|supp û₀| ≥ deg a + 1). La fonte non dimostra né la necessità né la soglia esatta deg a + 1.
   - Riclassificare G4-evolutiva come **"⇐ con fonte (con ipotesi più forti); ⟺ da dimostrare (R4-T4)"**, non come "NOTO".
   - La valutazione di novità di R8 (6/10, PROCEED) non cambia. Va invece ridimensionata l'affermazione "(iii) già DIMOSTRATO-CON-FONTE".
2. **R4 → Pierce 1979: CONTESTO NON SUPPORTATO.**
   - R4 (righe 23 e 62) afferma che una soluzione parabolica "determina i coefficienti se tutti i coefficienti di Fourier iniziali sono ≠ 0".
   - L'abstract (SICON 17(4):494–499) dice altro. Osservando la soluzione in **un punto** nel corso del tempo si determinano gli **autovalori**, e "the coefficients are not uniquely determined". Solo in forma normale l'unico coefficiente è determinato, "in certain cases", tramite Gel'fand–Levitan o due spettri.
   - La frase va corretta. La fonte rafforza la tesi di R4 sulla non identificabilità dei coefficienti variabili, non la contraddice.
3. **Scholl et al., Prop. 10 sovra-generalizzata (R4 riga 21; RIPRESA §4H "coeff. variabili arbitrari mai identificabili"): contesto impreciso.**
   - La Prop. 10 riguarda le ODE di **ordine 2** lineari in (u, u_t) con coefficienti continui; l'osservazione che la segue la estende all'ordine 3.
   - Per l'**ordine 1** la Prop. 8 dà unicità ⟺ u ha solo zeri isolati.
   - Scrivere "ordine ≥ 2". La conclusione per il Gate 1 (restringere la classe dei coefficienti) resta valida.
4. **R2 → Oberst 1990: DOI errato.**
   - `10.1007/BF01235717` porta a un altro articolo: Oberst 1995, AAECC 6:211–243 ("Variations on the fundamental principle…").
   - Il DOI corretto è `10.1007/BF00046908`. Volume e pagine (Acta Appl. Math. 20:1–175) sono giusti.
   - Il riferimento sostiene il quadro modulo/comportamento di R2, SCOUT-1 e SCOUT-2.
5. **R8 → Rapisarda–Antoulas 2016: titolo errato** (fuso con un capitolo LNCIS del 2015).
   - Corretto: "State-Space Modeling of Two-Dimensional Vector-Exponential Trajectories", SICON 54(5):2734–2753, DOI 10.1137/15M1031837.
   - L'abstract tratta davvero l'MPUM per traiettorie esponenziali in due variabili, quindi l'uso in R8 e SCOUT-2 è corretto.
6. **R5 → He–Zhao–Zhong e Efendiev–Vabishchevich: titoli segnaposto.** Corretti in `sources_verified.bib`. Efendiev–Vabishchevich è stato pubblicato in Appl. Math. Comput. 397 (2021) 125785.

Riferimenti prioritari **verificati senza riserve** (esistenza, metadati e contesto):
- Scholl–Bacho–Boche–Kutyniok: Mach. Learn. 115(6), art. 139, 2026; Prop. 1, Cor. 1, Prop. 6, 7, 8, 10 riscontrate.
- He–Zhao–Zhong, Thm 3.4 e 3.5.
- Wei–Norman 1963 e 1964.
- Jahnke–Lubich, Thm 2.1–2.3.
- Casas–Murua–Nadinić: la regione di convergenza **contiene** ‖X‖+‖Y‖ < 1.054.
- Donoho–Kutyniok, Prop. 2.1 e Lemma 2.1.
- Schiebinger–Robeva–Recht.
- Stanhope–Rubin–Swigon (pagine confermate).
- Robeva 2016 (Thm 3.6, caso n = 2).
- Crawley-Boevey 2003.
- Malgrange 1956.
- Engel–Nagel II.2.7, III.1.3, III.1.10, III.2.10, III.3.14–16, III.5.8 (riscontrati sul testo completo).
- Miller 1977, cap. 2.
- Tropp 2004, Cor. 3.6.

## 3. Verifica di contesto dei riferimenti prioritari

| riferimento | uso nei REPORT | esito | evidenza |
|---|---|---|---|
| Scholl–Bacho–Boche–Kutyniok arXiv:2210.08342 | Cor. 1 (F lineare unica ⟺ feature linearmente indipendenti), cioè dim ker 𝔾(u) = 1 (R8, R1, R4); Prop. 6/7 per ODE di ordine 2/3; Prop. 10 | **VERIFICATO** per Cor. 1, Prop. 6 e Prop. 7. **Impreciso** l'uso della Prop. 10 come "mai identificabili" in generale (§2.3) | arXiv v10, §2.1 e §3.1.2–3.2.2. Rivista: Mach. Learn. 115(6), art. 139 (2026), DOI 10.1007/s10994-026-07068-0 (Crossref) |
| He–Zhao–Zhong FoCM 24(5):1595–1641 | Thm 3.2 (soglia sui modi); 3.4 (rango); 3.5 (dati casuali) | Thm 3.4 e 3.5 **VERIFICATI**. Thm 3.2: **CONTESTO NON SUPPORTATO** per "G4 ⟺ NOTO" (§2.1) | arXiv v2, pp. 17–21 |
| Rosenbloom–Widder, Trans. AMS 92 (1959) 220–266 | biortogonalità v_n/w_n; teorema di sviluppo nella striscia | Metadati **VERIFICATI**. Costante 2^n n! coerente in R1 e R3. PR-C2b usa w_m = (−∂_x)^m G con costante n!: normalizzazione propria, da dichiarare. Enunciato esatto del teorema di sviluppo **non riscontrato** (sito AMS bloccato) | calcolo diretto: w_n^{RW} = 2^n (−∂_x)^n G per D = 1 |
| Hörmander ICASV, 3a ed. 1990, Thm 7.6.13/7.6.14 | 7.6.13 = principio fondamentale (convessi); 7.6.14 = densità degli esponenziali-polinomi | **VERIFICATO (fonte secondaria)**: Lomadze, LAA 438 (2013) 2083–2089 cita 7.6.13 per il principio fondamentale e la dimostrazione di 7.6.14 per il lemma duale di densità | libro non consultato; la §7.6 esiste solo dalla 3a ed. |
| Oberst 1990, Acta Appl. Math. 20:1–175 | C^∞ e D' cogeneratori iniettivi; dualità modulo/comportamento | Contenuto **VERIFICATO**; **DOI errato in R2** | Crossref |
| Malgrange 1956, AIF 6:271–355 | esistenza e approssimazione su convessi | **VERIFICATO** | DOI 10.5802/aif.65 |
| Crawley-Boevey, Duke 118 (2003) 339–352 | problema additivo di Deligne–Simpson via radici di Kac–Moody | **VERIFICATO** (abstract). SCOUT-1 deve ancora trascrivere l'enunciato esatto, inclusa la condizione su p(α) | DOI 10.1215/S0012-7094-03-11825-6 |
| Rapisarda–Antoulas, SICON 54(5) 2016 | MPUM 2-D di traiettorie esponenziali | **VERIFICATO** in SCOUT-2; **titolo errato in R8** | Crossref + abstract |
| Pierce 1979, SICON 17(4):494–499 | identificazione dei coefficienti da una soluzione parabolica | **CONTESTO NON SUPPORTATO** (§2.2) | abstract Crossref |
| Wei–Norman, JMP 4 (1963) 575–581; PAMS 15 (1964) 327–334 | prodotto di esponenziali; globalità per algebre risolubili | **VERIFICATO** | Crossref |
| Jahnke–Lubich, BIT 40 (2000) 735–744 | R5-T6: Thm 2.1 (errore locale τ² e τ³); 2.2 (τ² log n, semigruppo analitico, α = β = 1); 2.3 (B(−A)^{−1/2} limitato) | **VERIFICATO**. Due precisazioni: in 2.1(b) la norma è ‖(−A)^β v‖; il Thm 2.3 dà ordine **3/2** | PDF dell'articolo |
| Casas–Murua–Nadinić, CPC 183 (2012) 2386–2391 | dominio di Zassenhaus ‖X‖+‖Y‖ < 1.054; Suzuki 0.193; Bayen 0.5967 | **VERIFICATO**. Il dominio contiene quella regione ma è più ampio | arXiv:1204.0389 v2 |
| Donoho–Kutyniok, CPAM 66(1) (2013) 1–47 | Prop. 2.1 + Lemma 2.1 | **VERIFICATO** | arXiv:1004.3006 |
| Schiebinger–Robeva–Recht, Inf. Inference 7(1) (2018) 1–30 | super-risoluzione senza separazione, 2M+1 misure | **VERIFICATO** | abstract arXiv:1506.03144 |
| Stanhope–Rubin–Swigon, SIADS 13(4) (2014) 1792–1815 | identificabile ⟺ traiettoria non confinata in un sottospazio proprio (x₀ ciclico) | **VERIFICATO** (pagine confermate) | Crossref + abstract |
| Efendiev–Vabishchevich, arXiv:2008.08111 | split additivo della soluzione; metodo numerico con L noto | **VERIFICATO**. Pubblicato in AMC 397 (2021) 125785; titolo segnaposto in R5 | arXiv + Crossref |
| Robeva, SIMAX 37(1) (2016) 86–102 | equazioni odeco; ideale per n = 2 | **VERIFICATO** (Thm 3.6) | arXiv:1409.6685 v3 |
| Engel–Nagel, GTM 194 (2000) | II.2.7, III.1.3, III.1.10, III.2.10, III.3.14–16, III.5.8 | **VERIFICATO** (tutte le numerazioni) | testo completo (PDF Tübingen) |
| Pazy 1983 | 1.3.1, 1.4.3, 3.1.1, 3.2.1, 3.4.2, 4.1.3, §3.5 | **Plausibile, non riscontrato sul libro**. Una fonte secondaria colloca Trotter–Kato nel Thm 3.4.5 (p. 88); il 3.4.2 sarebbe la versione di Trotter | citazione secondaria |
| Zettl 2005 (AMS Surv. 121) | cap. 4 (SL regolare); cap. 10 (BC autoaggiunte) | **Numeri di capitolo NON VERIFICATI** (sito AMS bloccato); voce bibliografica corretta | — |
| Higham 2008 | Def. 1.2/1.4, Thm 1.12 | **VERIFICATO (fonte secondaria + indice)** | Higham–Al-Mohy 2010 |
| Miller 1977 | cap. 2: calore e Schrödinger | **VERIFICATO** | indice Cambridge |
| Tropp 2004 (R1) | Cor. 3.6; Thm 3.1, 3.3, 3.5 | **VERIFICATO** | PDF |
| Paulsen–Raghupathi, "Thm 2.10" (R1) | teorema di Papadakis | **Numerazione NON VERIFICATA** (R1 lo segnala già) | — |

## 4. Altre correzioni e aggiornamenti (non bloccanti)
- **R8, Kunis et al. 2016:** il riferimento giusto è LAA **490**, 31–47 (non 499:191–212). R4 e SCOUT-2 hanno già i dati corretti.
- **R8, Willems 1986:** le Parti I–II sono in Automatica 22 (1986) 561–580 e 675–694; la Parte III è in Automatica **23** (1987) 87–115.
- **R5, González-López–Kamran–Olver:** la voce fonde due articoli. Per la classificazione 1D va citato CMP 153 (1993) 117–146 (DOI 10.1007/BF02099042).
- **R6, BasicModuleOre2013:** manca l'autore, che è J. Gómez-Torrecillas (LNCS 8372 (2014) 23–82).
- **R1/R4, Scholl 2026:** "pages={139}" è in realtà il numero di articolo; manca il DOI.
- **Preprint poi pubblicati** (la sede è aggiornata nelle note delle tabelle):
  - Hauger–Scholl–Kutyniok → ICASSP 2025.
  - Ait El Manssour–Härkönen–Sturmfels → Glasgow Math. J. 65 (2023) S2–S27.
  - Sattelberger–Sturmfels → EMS Ser. Congr. Rep. (2025) 251–293.
  - Vabishchevich, arXiv:1112.1294 → Math. Comp. 83 (2014) 2787–2797.
  - Giansiracusa–Mereta → manuscripta math. 173 (2024) 1273–1304.
  - Kutyniok, arXiv:1204.6120 → ACHA 36 (2014) 23–50.
  - Byrne et al. → Nonlinearity 38 (2025) 025022.
  - Stampfer–Plonka → Constr. Approx. 52 (2020) 247–282.
  - Casolo–Becker–Kilbertus → ICLR 2026.
  - Boalch 2008 → risultati principali in Publ. IHES 116 (2012).
- **Voci di R8 marcate "UNVERIFIED", ora verificate:**
  - Stanhope (pagine).
  - Messenger–Bortz (DOI 10.1137/20M1343166).
  - Kauers–Jaroschek–Johansson (DOI).
  - Mourrain, FoCM 18 (2018) 1435–1492.
  - Zhao–Zhong, PAFA 8(2) (2023) 751–773 (Duke Scholars).
  - Chelkak–Korotyaev, JFA 257 (2009).
- **Edizioni diverse, non errori.** Alcune opere compaiono con edizione o anno diversi a seconda dell'agente: Kato 1980/1995, Reed–Simon, Hörmander ALPDO I 1983/1990, Polyanin 2002/2016, Young 1980/2001, Marchenko 1977/1986. In Fase 3 conviene fissare un'edizione per ciascuna opera.
- **Normalizzazione da dichiarare (PR-C2b rispetto a R1/R3):** la costante di biortogonalità dei polinomi del calore è n! in PR-C2b e 2^n n! in R1/R3 (si veda la riga Rosenbloom–Widder in §3).

## 5. File consegnati
- `research/CIT-AUDIT/AUDIT.md`: questo file.
- `research/CIT-AUDIT/sources_verified.bib`: 445 opere uniche, con i campi `cit_status` e `cit_aliases` e le correzioni già applicate. I DOI sono stati aggiunti solo dove la corrispondenza Crossref era pulita.
- `research/CIT-AUDIT/PLAN.md`.
- AVVISI, come registro per la Fase 3, in `inbox/R2.md`, `inbox/R4.md`, `inbox/R5.md`, `inbox/R6.md`, `inbox/R8.md`; nota informativa in `inbox/PR-C2b.md` (normalizzazione).

## 6. Tabelle per agente
Colonne: chiave · voce · esito · fonte del controllo automatico · nota/correzione.

### PR-C2a

Conteggi: VERIFICATO 21, VERIFICATO-K 7

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `CoddingtonLevinson1955` | Coddington et al., *Theory of Ordinary Differential Equations*, McGraw-Hill  (1955) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |
| `Ince1926` | Ince, *Ordinary Differential Equations*, Longmans, Green  (1926) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: National Mathematics Magazine). |
| `Teschl2012` | Teschl, *Ordinary Differential Equations and Dynamical Systems*, American Mathematical Society 140 (2012) | **VERIFICATO** | Crossref-ricerca |  |
| `MIT1803S10` | Miller et al., *18.03 Differential Equations, Spring 2010 -- Lecture Notes*,   () | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `AnseloneKorevaar1964` | Anselone et al., *Translation invariant subspaces of finite dimension*, Proceedings of the American Mathematical 15 (1964) | **VERIFICATO** | Crossref-ricerca |  |
| `HirschSmaleDevaney2013` | Hirsch et al., *Differential Equations, Dynamical Systems, and an Introduction to Chao*, Academic Press  (2013) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Higham2008` | Higham, *Functions of Matrices: Theory and Computation*, SIAM  (2008) | **VERIFICATO** | Crossref-ricerca |  |
| `MolerVanLoan2003` | Moler et al., *Nineteen Dubious Ways to Compute the Exponential of a Matrix, Twenty-F*, SIAM Review 45 (2003) | **VERIFICATO** | Crossref-ricerca |  |
| `Wasow1965` | Wasow, *Asymptotic Expansions for Ordinary Differential Equations*, Interscience  (1965) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Ordinary Differential Equations). |
| `Olver1974` | Olver, *Asymptotics and Special Functions*, Academic Press  (1974) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `BenderOrszag1978` | Bender et al., *Advanced Mathematical Methods for Scientists and Engineers*, McGraw-Hill  (1978) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1999). |
| `vanderPutSinger2003` | van der Put et al., *Galois Theory of Linear Differential Equations*, Springer 328 (2003) | **VERIFICATO** | Crossref-ricerca |  |
| `Stanley1980` | Stanley, *Differentiably Finite Power Series*, European Journal of Combinatorics 1 (1980) | **VERIFICATO** | Crossref-ricerca |  |
| `Stafford1978` | Stafford, *Module structure of {W}eyl algebras*, Journal of the London Mathematical Socie 18 (1978) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref: Journal of the London Mathematical Society s2-18 429-442 1978 DOI 10.1112/jlms/s2-18.3.429. |
| `KauersPaule2011` | Kauers et al., *The Concrete Tetrahedron*, Springer  (2011) | **VERIFICATO** | Crossref-ricerca |  |
| `Katz1996` | Katz, *Rigid Local Systems*, Princeton University Press 139 (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `DLMF` | Olver et al., *{NIST} Digital Library of Mathematical Functions*,   () | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `NikiforovUvarov1988` | Nikiforov et al., *Special Functions of Mathematical Physics*, Birkh{\"a}user  (1988) | **VERIFICATO** | Crossref-ricerca |  |
| `Szego1939` | Szeg{\H o}, *Orthogonal Polynomials*, American Mathematical Society 23 (1939) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Watson1944` | Watson, *A Treatise on the Theory of Bessel Functions*, Cambridge University Press  (1944) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: National Mathematics Magazine). |
| `WhittakerWatson1927` | Whittaker et al., *A Course of Modern Analysis*, Cambridge University Press  (1927) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1996). |
| `ValleeSoares2004` | Vall{\'e}e et al., *Airy Functions and Applications to Physics*, Imperial College Press  (2004) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `MasonHandscomb2003` | Mason et al., *Chebyshev Polynomials*, Chapman \& Hall/CRC  (2003) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2002). |
| `Vilenkin1968` | Vilenkin, *Special Functions and the Theory of Group Representations*, American Mathematical Society 22 (1968) | **VERIFICATO** | Crossref-ricerca |  |
| `SlepianPollak1961` | Slepian et al., *Prolate spheroidal wave functions, {F}ourier analysis and uncertainty *, Bell System Technical Journal 40 (1961) | **VERIFICATO** | Crossref-ricerca |  |
| `Slater1960` | Slater, *Confluent Hypergeometric Functions*, Cambridge University Press  (1960) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Journal of the Royal Statistical Society. Series A (General)). |
| `Reid1972` | Reid, *Riccati Differential Equations*, Academic Press  (1972) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Strogatz2015` | Strogatz, *Nonlinear Dynamics and Chaos*, Westview Press  (2015) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2018). |

### PR-C2b

Conteggi: VERIFICATO 32, VERIFICATO-K 13

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Hancock2006MIT18303` | Hancock, *18.303 Linear Partial Differential Equations, Fall 2006 -- Lecture Not*,   (2006) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `GuentherLee1996` | Guenther et al., *Partial Differential Equations of Mathematical Physics and Integral Eq*, Dover  (1996) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `MyintUDebnath2007` | Myint-U et al., *Linear Partial Differential Equations for Scientists and Engineers*, Birkh{\"a}user  (2007) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Polyanin2002` | Polyanin, *Handbook of Linear Partial Differential Equations for Engineers and Sc*, Chapman \& Hall/CRC  (2002) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2001). |
| `Evans2010` | Evans, *Partial Differential Equations*, AMS 19 (2010) | **VERIFICATO** | Crossref-ricerca |  |
| `Hormander1983II` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators II*, Springer  (1983) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `Ehrenpreis1970` | Ehrenpreis, *Fourier Analysis in Several Complex Variables*, Wiley-Interscience  (1970) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Palamodov1970` | Palamodov, *Linear Differential Operators with Constant Coefficients*, Springer  (1970) | **VERIFICATO** | Crossref-ricerca |  |
| `AitElManssourHarkonenSturmfels2023` | Ait El Manssour et al., *Linear {PDE} with constant coefficients*, Glasgow Mathematical Journal 65 (2023) | **VERIFICATO** | DOI/Crossref+arXiv |  |
| `Widder1975` | Widder, *The Heat Equation*, Academic Press  (1975) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `RosenbloomWidder1959` | Rosenbloom et al., *Expansions in terms of heat polynomials and associated functions*, Transactions of the American Mathematica 92 (1959) | **VERIFICATO** | DOI/Crossref | Trans. AMS 92:220-266 ok. Nota: la costante n! di PR-C2b-P6 vale per w_m=(-d_x)^m G (normalizzazione propria); con le w_n di Rosenbloom-Widder la costante e' 2^n n! (come in R1/R3). Coerente, ma va dichiarata la diversa normalizzazione. Teorema di sviluppo (striscia /t/<sigma) non riscontrato sul testo. |
| `WeiNorman1963` | Wei et al., *Lie Algebraic Solution of Linear Differential Equations*, Journal of Mathematical Physics 4 (1963) | **VERIFICATO** | DOI/Crossref |  |
| `Casas1996` | Casas, *Solution of linear partial differential equations by {Lie} algebraic m*, Journal of Computational and Applied Mat 76 (1996) | **VERIFICATO** | DOI/Crossref |  |
| `Wilcox1967` | Wilcox, *Exponential Operators and Parameter Differentiation in Quantum Physics*, Journal of Mathematical Physics 8 (1967) | **VERIFICATO** | DOI/Crossref |  |
| `EngelNagel2000` | Engel et al., *One-Parameter Semigroups for Linear Evolution Equations*, Springer 194 (2000) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Friedman1964` | Friedman, *Partial Differential Equations of Parabolic Type*, Prentice-Hall  (1964) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Zettl2005` | Zettl, *Sturm--Liouville Theory*, AMS 121 (2005) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Mathematical Surveys and Monographs). |
| `Schwartz1947` | Schwartz, *Th{\'e}orie g{\'e}n{\'e}rale des fonctions moyenne-p{\'e}riodiques*, Annals of Mathematics 48 (1947) | **VERIFICATO** | Crossref-ricerca |  |
| `Gurevich1975` | Gurevich, *Counterexamples to a problem of {L}. {Schwartz}*, Functional Analysis and Its Applications 9 (1975) | **VERIFICATO** | DOI/Crossref |  |
| `MainardiLuchkoPagnini2001` | Mainardi et al., *The fundamental solution of the space-time fractional diffusion equati*, Fractional Calculus and Applied Analysis 4 (2001) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Kwasnicki2017` | Kwa{\'s}nicki, *Ten Equivalent Definitions of the Fractional {Laplace} Operator*, Fractional Calculus and Applied Analysis 20 (2017) | **VERIFICATO** | DOI/Crossref |  |
| `CaffarelliSilvestre2007` | Caffarelli et al., *An Extension Problem Related to the Fractional {Laplacian}*, Communications in Partial Differential E 32 (2007) | **VERIFICATO** | DOI/Crossref |  |
| `KilbasSrivastavaTrujillo2006` | Kilbas et al., *Theory and Applications of Fractional Differential Equations*, Elsevier  (2006) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Podlubny1999` | Podlubny, *Fractional Differential Equations*, Academic Press  (1999) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Mainardi2010` | Mainardi, *Fractional Calculus and Waves in Linear Viscoelasticity*, Imperial College Press  (2010) | **VERIFICATO** | Crossref-ricerca |  |
| `GorenfloKilbasMainardiRogosin2014` | Gorenflo et al., *Mittag-Leffler Functions, Related Topics and Applications*, Springer  (2014) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `JinRundell2015` | Jin et al., *A tutorial on inverse problems for anomalous diffusion processes*, Inverse Problems 31 (2015) | **VERIFICATO** | Crossref-ricerca |  |
| `ValleeSoares2004` | Vall{\'e}e et al., *Airy Functions and Applications to Physics*, Imperial College Press  (2004) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `DLMF` | , *{NIST} Digital Library of Mathematical Functions*,   () | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Whitham1974` | Whitham, *Linear and Nonlinear Waves*, Wiley  (1974) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1999). |
| `CourantHilbertII` | Courant et al., *Methods of Mathematical Physics, Vol. II*, Interscience  (1962) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |
| `MorseFeshbach1953` | Morse et al., *Methods of Theoretical Physics*, McGraw-Hill  (1953) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: American Journal of Physics). |
| `AxlerBourdonRamey2001` | Axler et al., *Harmonic Function Theory*, Springer 137 (2001) | **VERIFICATO** | Crossref-ricerca |  |
| `HedenmalmKorenblumZhu2000` | Hedenmalm et al., *Theory of Bergman Spaces*, Springer 199 (2000) | **VERIFICATO** | Crossref-ricerca |  |
| `GilbargTrudinger2001` | Gilbarg et al., *Elliptic Partial Differential Equations of Second Order*, Springer  (2001) | **VERIFICATO** | Crossref-ricerca |  |
| `ColtonKress` | Colton et al., *Inverse Acoustic and Electromagnetic Scattering Theory*, Springer  (2019) | **VERIFICATO** | Crossref-ricerca |  |
| `GazzolaGrunauSweers2010` | Gazzola et al., *Polyharmonic Boundary Value Problems*, Springer 1991 (2010) | **VERIFICATO** | Crossref-ricerca |  |
| `Bitsadze1964` | Bitsadze, *Equations of the Mixed Type*, Pergamon  (1964) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Otway2012` | Otway, *The Dirichlet Problem for Elliptic-Hyperbolic Equations of Keldysh Typ*, Springer 2043 (2012) | **VERIFICATO** | Crossref-ricerca |  |
| `Vazquez2007` | V{\'a}zquez, *The Porous Medium Equation: Mathematical Theory*, Oxford University Press  (2007) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2006). |
| `Murray2002` | Murray, *Mathematical Biology*, Springer  (2002) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1989). |
| `AblowitzZeppetella1979` | Ablowitz et al., *Explicit solutions of {Fisher}'s equation for a special wave speed*, Bulletin of Mathematical Biology 41 (1979) | **VERIFICATO** | Crossref-ricerca |  |
| `AblowitzClarkson1991` | Ablowitz et al., *Solitons, Nonlinear Evolution Equations and Inverse Scattering*, Cambridge University Press  (1991) | **VERIFICATO** | Crossref-ricerca |  |
| `Tao2006` | Tao, *Nonlinear Dispersive Equations: Local and Global Analysis*, AMS 106 (2006) | **VERIFICATO** | Crossref-ricerca |  |
| `AndreuMazonRossiToledo2010` | Andreu-Vaillo et al., *Nonlocal Diffusion Problems*, AMS 165 (2010) | **VERIFICATO** | Crossref-ricerca |  |

### PR-C2c

Conteggi: VERIFICATO 49, VERIFICATO-K 8

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Hopf1950` | Hopf, *The partial differential equation $u_t+uu_x=\mu u_{xx}$*, Comm. Pure Appl. Math. 3 (1950) | **VERIFICATO** | DOI/Crossref |  |
| `Cole1951` | Cole, *On a quasi-linear parabolic equation occurring in aerodynamics*, Quart. Appl. Math. 9 (1951) | **VERIFICATO** | DOI/Crossref |  |
| `GGKM1967` | Gardner et al., *Method for solving the {K}orteweg--de {V}ries equation*, Phys. Rev. Lett. 19 (1967) | **VERIFICATO** | DOI/Crossref |  |
| `Lax1968` | Lax, *Integrals of nonlinear equations of evolution and solitary waves*, Comm. Pure Appl. Math. 21 (1968) | **VERIFICATO** | DOI/Crossref |  |
| `Miura1968` | Miura, *{K}orteweg--de {V}ries equation and generalizations. {I}. {A} remarkab*, J. Math. Phys. 9 (1968) | **VERIFICATO** | DOI/Crossref |  |
| `Hirota1971` | Hirota, *Exact solution of the {K}orteweg--de {V}ries equation for multiple col*, Phys. Rev. Lett. 27 (1971) | **VERIFICATO** | DOI/Crossref |  |
| `ZabuskyKruskal1965` | Zabusky et al., *Interaction of ``solitons'' in a collisionless plasma and the recurren*, Phys. Rev. Lett. 15 (1965) | **VERIFICATO** | DOI/Crossref |  |
| `AKNS1974` | Ablowitz et al., *The inverse scattering transform---{F}ourier analysis for nonlinear pr*, Stud. Appl. Math. 53 (1974) | **VERIFICATO** | DOI/Crossref |  |
| `ZakharovShabat1972` | Zakharov et al., *Exact theory of two-dimensional self-focusing and one-dimensional self*, Sov. Phys. JETP 34 (1972) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `AblowitzSegur1981` | Ablowitz et al., *Solitons and the Inverse Scattering Transform*, SIAM  (1981) | **VERIFICATO** | DOI/Crossref |  |
| `DrazinJohnson1989` | Drazin et al., *Solitons: an Introduction*, Cambridge University Press  (1989) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |
| `Hirota2004` | Hirota, *The Direct Method in Soliton Theory*, Cambridge University Press  (2004) | **VERIFICATO** | Crossref-ricerca |  |
| `Whitham1974` | Whitham, *Linear and Nonlinear Waves*, Wiley  (1974) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1999). |
| `Evans2010` | Evans, *Partial Differential Equations*, AMS  (2010) | **VERIFICATO** | Crossref-ricerca |  |
| `Lax1957` | Lax, *Hyperbolic systems of conservation laws {II}*, Comm. Pure Appl. Math. 10 (1957) | **VERIFICATO** | DOI/Crossref |  |
| `Kruzhkov1970` | Kru{\v{z}}kov, *First order quasilinear equations in several independent variables*, Math. USSR Sb. 10 (1970) | **VERIFICATO** | - | DOI ok (differenza solo di traslitterazione Kruzkov/Kružkov). |
| `Glimm1965` | Glimm, *Solutions in the large for nonlinear hyperbolic systems of equations*, Comm. Pure Appl. Math. 18 (1965) | **VERIFICATO** | Crossref-ricerca |  |
| `Dafermos2016` | Dafermos, *Hyperbolic Conservation Laws in Continuum Physics*, Springer  (2016) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `ClarksonFokasAblowitz1989` | Clarkson et al., *Hodograph transformations of linearizable partial differential equatio*, SIAM J. Appl. Math. 49 (1989) | **VERIFICATO** | DOI/Crossref |  |
| `CourantFriedrichs1948` | Courant et al., *Supersonic Flow and Shock Waves*, Interscience  (1948) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `CarrierGreenspan1958` | Carrier et al., *Water waves of finite amplitude on a sloping beach*, J. Fluid Mech. 4 (1958) | **VERIFICATO** | DOI/Crossref |  |
| `Sandstede2002` | Sandstede, *Stability of travelling waves*, Handbook of Dynamical Systems, Vol. 2  (2002) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `KapitulaPromislow2013` | Kapitula et al., *Spectral and Dynamical Stability of Nonlinear Waves*, Springer  (2013) | **VERIFICATO** | Crossref-ricerca |  |
| `AblowitzZeppetella1979` | Ablowitz et al., *Explicit solutions of {F}isher's equation for a special wave speed*, Bull. Math. Biol. 41 (1979) | **VERIFICATO** | DOI/Crossref |  |
| `Fujita1966` | Fujita, *On the blowing up of solutions of the {C}auchy problem for $u_t=\Delta*, J. Fac. Sci. Univ. Tokyo Sect. I 13 (1966) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `GigaKohn1985` | Giga et al., *Asymptotically self-similar blow-up of semilinear heat equations*, Comm. Pure Appl. Math. 38 (1985) | **VERIFICATO** | DOI/Crossref |  |
| `BKM1984` | Beale et al., *Remarks on the breakdown of smooth solutions for the 3-{D} {E}uler equ*, Comm. Math. Phys. 94 (1984) | **VERIFICATO** | DOI/Crossref |  |
| `QuittnerSouplet2019` | Quittner et al., *Superlinear Parabolic Problems*, Birkh{\"a}user  (2019) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2007). |
| `MajdaBertozzi2002` | Majda et al., *Vorticity and Incompressible Flow*, Cambridge University Press  (2002) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2001). |
| `DrazinRiley2006` | Drazin et al., *The {N}avier--{S}tokes Equations: a Classification of Flows and Exact *, Cambridge University Press  (2006) | **VERIFICATO** | Crossref-ricerca |  |
| `Vallis2017` | Vallis, *Atmospheric and Oceanic Fluid Dynamics*, Cambridge University Press  (2017) | **VERIFICATO** | Crossref-ricerca |  |
| `Jackson1999` | Jackson, *Classical Electrodynamics*, Wiley  (1999) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: American Journal of Physics). |
| `Graff1975` | Graff, *Wave Motion in Elastic Solids*, Ohio State Univ. Press (Dover 1991)  (1975) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `HanBenaroyaWei1999` | Han et al., *Dynamics of transversely vibrating beams using four engineering theori*, J. Sound Vib. 225 (1999) | **VERIFICATO** | DOI/Crossref |  |
| `Timoshenko1921` | Timoshenko, *On the correction for shear of the differential equation for transvers*, Phil. Mag. 41 (1921) | **VERIFICATO** | DOI/Crossref |  |
| `LandauLifshitzElasticity` | Landau et al., *Theory of Elasticity*, Pergamon  (1986) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Achenbach1973` | Achenbach, *Wave Propagation in Elastic Solids*, North-Holland  (1973) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Risken1989` | Risken, *The {F}okker--{P}lanck Equation*, Springer  (1989) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Springer Series in Synergetics). |
| `Cercignani1988` | Cercignani, *The {B}oltzmann Equation and its Applications*, Springer  (1988) | **VERIFICATO** | Crossref-ricerca |  |
| `Villani2009` | Villani, *Hypocoercivity*, Mem. Amer. Math. Soc. 202 (2009) | **VERIFICATO** | Crossref-ricerca |  |
| `MouhotVillani2011` | Mouhot et al., *On {L}andau damping*, Acta Math. 207 (2011) | **VERIFICATO** | Crossref-ricerca |  |
| `Crank1984` | Crank, *Free and Moving Boundary Problems*, Oxford University Press  (1984) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Mathematics of Computation). |
| `Rubinstein1971` | Rubinstein, *The {S}tefan Problem*, AMS  (1971) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: IMA Journal of Applied Mathematics). |
| `Richardson1972` | Richardson, *Hele {S}haw flows with a free boundary produced by the injection of fl*, J. Fluid Mech. 56 (1972) | **VERIFICATO** | Crossref-ricerca |  |
| `BerkolaikoKuchment2013` | Berkolaiko et al., *Introduction to Quantum Graphs*, AMS  (2013) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Mathematical Surveys and Monographs). |
| `KostrykinSchrader1999` | Kostrykin et al., *{K}irchhoff's rule for quantum wires*, J. Phys. A 32 (1999) | **VERIFICATO** | DOI/Crossref |  |
| `Mugnolo2014` | Mugnolo, *Semigroup Methods for Evolution Equations on Networks*, Springer  (2014) | **VERIFICATO** | Crossref-ricerca |  |
| `Walsh1986` | Walsh, *An introduction to stochastic partial differential equations*, Springer  (1986) | **VERIFICATO** | DOI/Crossref |  |
| `DaPratoZabczyk2014` | Da Prato et al., *Stochastic Equations in Infinite Dimensions*, Cambridge University Press  (2014) | **VERIFICATO** | Crossref-ricerca |  |
| `Kac1949` | Kac, *On distributions of certain {W}iener functionals*, Trans. Amer. Math. Soc. 65 (1949) | **VERIFICATO** | Crossref-ricerca |  |
| `BertiniGiacomin1997` | Bertini et al., *Stochastic {B}urgers and {KPZ} equations from particle systems*, Comm. Math. Phys. 183 (1997) | **VERIFICATO** | DOI/Crossref |  |
| `Hairer2013` | Hairer, *Solving the {KPZ} equation*, Ann. of Math. 178 (2013) | **VERIFICATO** | DOI/Crossref |  |
| `BenderOrszag1978` | Bender et al., *Advanced Mathematical Methods for Scientists and Engineers*, McGraw-Hill  (1978) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1999). |
| `PageKerswell2018` | Page et al., *Koopman analysis of {B}urgers equation*, Phys. Rev. Fluids 3 (2018) | **VERIFICATO** | DOI/Crossref |  |
| `KutzProctorBrunton2018` | Kutz et al., *Applied {K}oopman theory for partial differential equations and data-d*, Complexity  (2018) | **VERIFICATO** | DOI/Crossref |  |
| `Calogero1991` | Calogero, *Why are certain nonlinear {PDE}s both widely applicable and integrable*, What is Integrability?  (1991) | **VERIFICATO** | Crossref-ricerca |  |
| `Fokas1997` | Fokas, *A unified transform method for solving linear and certain nonlinear {P*, Proc. R. Soc. Lond. A 453 (1997) | **VERIFICATO** | DOI/Crossref |  |

### PR-C2d

Conteggi: VERIFICATO 70, VERIFICATO-K 29

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Aronszajn1950` | Aronszajn, *Theory of reproducing kernels*, Trans. Amer. Math. Soc. 68 (1950) | **VERIFICATO** | DOI/Crossref |  |
| `Mercer1909` | Mercer, *Functions of positive and negative type, and their connection with the*, Phil. Trans. R. Soc. A 209 (1909) | **VERIFICATO** | DOI/Crossref |  |
| `Weyl1910` | Weyl, *{\"U}ber gew{\"o}hnliche Differentialgleichungen mit Singularit{\"a}te*, Math. Ann. 68 (1910) | **VERIFICATO** | DOI/Crossref |  |
| `Kodaira1949` | Kodaira, *The eigenvalue problem for ordinary differential equations of the seco*, Amer. J. Math. 71 (1949) | **VERIFICATO** | Crossref-ricerca |  |
| `Zettl2005` | Zettl, *Sturm--Liouville Theory*, AMS 121 (2005) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Mathematical Surveys and Monographs). |
| `CoddingtonLevinson1955` | Coddington et al., *Theory of Ordinary Differential Equations*, McGraw-Hill  (1955) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |
| `Titchmarsh1962` | Titchmarsh, *Eigenfunction Expansions Associated with Second-Order Differential Equ*, Oxford Univ. Press  (1962) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `Weidmann1987` | Weidmann, *Spectral Theory of Ordinary Differential Operators*, Springer 1258 (1987) | **VERIFICATO** | Crossref-ricerca |  |
| `Teschl2014` | Teschl, *Mathematical Methods in Quantum Mechanics*, AMS 157 (2014) | **VERIFICATO** | Crossref-ricerca |  |
| `Folland1999` | Folland, *Real Analysis*, Wiley  (1999) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `RudinRCA1987` | Rudin, *Real and Complex Analysis*, McGraw-Hill  (1987) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The Statistician). |
| `RudinFAG1962` | Rudin, *Fourier Analysis on Groups*, Interscience  (1962) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1990). |
| `PaleyWiener1934` | Paley et al., *Fourier Transforms in the Complex Domain*, AMS 19 (1934) | **VERIFICATO** | Crossref-ricerca |  |
| `HormanderI` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators I*, Springer  (1990) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `HormanderII` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators II*, Springer  (1983) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `HormanderSCV` | H{\"o}rmander, *An Introduction to Complex Analysis in Several Variables*, North-Holland  (1990) | **VERIFICATO-K** | - | 3a ed. 1990 corretta (sezione sul principio fondamentale aggiunta nella 3a ed.). Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Ehrenpreis1954` | Ehrenpreis, *Solution of some problems of division. Part I. Division by a polynomia*, Amer. J. Math. 76 (1954) | **VERIFICATO** | DOI/Crossref |  |
| `Malgrange1956` | Malgrange, *Existence et approximation des solutions des {\'e}quations aux d{\'e}r*, Ann. Inst. Fourier 6 (1956) | **VERIFICATO** | DOI/Crossref |  |
| `Ehrenpreis1970` | Ehrenpreis, *Fourier Analysis in Several Complex Variables*, Wiley-Interscience  (1970) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Palamodov1970` | Palamodov, *Linear Differential Operators with Constant Coefficients*, Springer  (1970) | **VERIFICATO** | Crossref-ricerca |  |
| `Bjork1979` | Bj{\"o}rk, *Rings of Differential Operators*, North-Holland  (1979) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Widder1941` | Widder, *The Laplace Transform*, Princeton Univ. Press  (1941) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Bargmann1961` | Bargmann, *On a Hilbert space of analytic functions and an associated integral tr*, Comm. Pure Appl. Math. 14 (1961) | **VERIFICATO** | DOI/Crossref |  |
| `StakgoldHolst2011` | Stakgold et al., *Green's Functions and Boundary Value Problems*, Wiley  (2011) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Kato1980` | Kato, *Perturbation Theory for Linear Operators*, Springer  (1980) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `ReedSimonI` | Reed et al., *Methods of Modern Mathematical Physics I: Functional Analysis*, Academic Press  (1980) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `ReedSimonIV` | Reed et al., *Methods of Modern Mathematical Physics IV: Analysis of Operators*, Academic Press  (1978) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `BerlinetThomasAgnan2004` | Berlinet et al., *Reproducing Kernel Hilbert Spaces in Probability and Statistics*, Kluwer  (2004) | **VERIFICATO** | Crossref-ricerca |  |
| `Saitoh1988` | Saitoh, *Theory of Reproducing Kernels and its Applications*, Longman  (1988) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Phillips1953` | Phillips, *Perturbation theory for semi-groups of linear operators*, Trans. Amer. Math. Soc. 74 (1953) | **VERIFICATO** | DOI/Crossref |  |
| `EngelNagel2000` | Engel et al., *One-Parameter Semigroups for Linear Evolution Equations*, Springer 194 (2000) | **VERIFICATO-K** | - | Numerazioni II.2.7 (Product Semigroups), III.1.3 (Bounded Perturbation Thm), III.1.10 (Dyson-Phillips), III.2.10, III.3.14-3.16 (Miyadera-Voigt), III.5.8 (Trotter product formula, Cor.) riscontrate sul testo. Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Pazy1983` | Pazy, *Semigroups of Linear Operators and Applications to Partial Differentia*, Springer  (1983) | **VERIFICATO** | Crossref-ricerca |  |
| `BenderOrszag1978` | Bender et al., *Advanced Mathematical Methods for Scientists and Engineers*, McGraw-Hill  (1978) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1999). |
| `KevorkianCole1996` | Kevorkian et al., *Multiple Scale and Singular Perturbation Methods*, Springer  (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `OlverFWJ1974` | Olver, *Asymptotics and Special Functions*, Academic Press  (1974) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `BLP1978` | Bensoussan et al., *Asymptotic Analysis for Periodic Structures*, North-Holland  (1978) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2011). |
| `Barenblatt1996` | Barenblatt, *Scaling, Self-Similarity, and Intermediate Asymptotics*, Cambridge Univ. Press  (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `Buckingham1914` | Buckingham, *On physically similar systems; illustrations of the use of dimensional*, Phys. Rev. 4 (1914) | **VERIFICATO** | Crossref-ricerca |  |
| `GMP1985` | Grossmann et al., *Transforms associated to square integrable group representations. I. G*, J. Math. Phys. 26 (1985) | **VERIFICATO** | DOI/Crossref |  |
| `AAG1993` | Ali et al., *Continuous frames in Hilbert space*, Ann. Physics 222 (1993) | **VERIFICATO** | DOI/Crossref |  |
| `Olver1993` | Olver, *Applications of Lie Groups to Differential Equations*, Springer 107 (1993) | **VERIFICATO** | Crossref-ricerca |  |
| `BlumanKumei1989` | Bluman et al., *Symmetries and Differential Equations*, Springer  (1989) | **VERIFICATO** | Crossref-ricerca |  |
| `Ovsiannikov1982` | Ovsiannikov, *Group Analysis of Differential Equations*, Academic Press  (1982) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Noether1918` | Noether, *Invariante Variationsprobleme*, Nachr. Ges. Wiss. G{\"o}ttingen, Math.-P  (1918) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref: Springer Collected Works in Mathematics None 231-239 1983 DOI 10.1007/978-3-642-39990-9_13. |
| `Miller1977` | Miller, *Symmetry and Separation of Variables*, Addison-Wesley  (1977) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1984). |
| `Vilenkin1968` | Vilenkin, *Special Functions and the Theory of Group Representations*, AMS 22 (1968) | **VERIFICATO** | Crossref-ricerca |  |
| `LaxMilgram1954` | Lax et al., *Parabolic equations*, Contributions to the Theory of Partial D 33 (1954) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref: Contributions to the Theory of Partial Differential Equations. (AM-33) None 167-190 1955 DOI 10.1515/9781400882182-010. |
| `Brezis2011` | Brezis, *Functional Analysis, Sobolev Spaces and Partial Differential Equations*, Springer  (2011) | **VERIFICATO** | Crossref-ricerca |  |
| `Evans2010` | Evans, *Partial Differential Equations*, AMS 19 (2010) | **VERIFICATO** | Crossref-ricerca |  |
| `CourantHilbert1953` | Courant et al., *Methods of Mathematical Physics, Vol. I*, Interscience  (1953) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |
| `Cea1964` | C{\'e}a, *Approximation variationnelle des probl{\`e}mes aux limites*, Ann. Inst. Fourier 14 (1964) | **VERIFICATO** | Crossref-ricerca |  |
| `KimeldorfWahba1971` | Kimeldorf et al., *Some results on Tchebycheffian spline functions*, J. Math. Anal. Appl. 33 (1971) | **VERIFICATO** | Crossref-ricerca |  |
| `EHN1996` | Engl et al., *Regularization of Inverse Problems*, Kluwer  (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `Borg1946` | Borg, *Eine Umkehrung der Sturm--Liouvilleschen Eigenwertaufgabe. Bestimmung *, Acta Math. 78 (1946) | **VERIFICATO** | DOI/Crossref |  |
| `Levinson1949` | Levinson, *The inverse Sturm--Liouville problem*, Mat. Tidsskr. B  (1949) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref: Selected Papers of Norman Levinson None 193-198 1998 DOI 10.1007/978-1-4612-5332-7_19. |
| `Ambarzumian1929` | Ambarzumian, *{\"U}ber eine Frage der Eigenwerttheorie*, Z. Phys. 53 (1929) | **VERIFICATO** | Crossref-ricerca |  |
| `GelfandLevitan1951` | Gel'fand et al., *On the determination of a differential equation from its spectral func*, Izv. Akad. Nauk SSSR Ser. Mat. 15 (1951) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Marchenko1986` | Marchenko, *Sturm--Liouville Operators and Applications*, Birkh{\"a}user  (1986) | **VERIFICATO** | Crossref-ricerca |  |
| `FreilingYurko2001` | Freiling et al., *Inverse Sturm--Liouville Problems and their Applications*, Nova Science  (2001) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `HochstadtLieberman1978` | Hochstadt et al., *An inverse Sturm--Liouville problem with mixed given data*, SIAM J. Appl. Math. 34 (1978) | **VERIFICATO** | DOI/Crossref |  |
| `Isakov2017` | Isakov, *Inverse Problems for Partial Differential Equations*, Springer  (2017) | **VERIFICATO** | Crossref-ricerca |  |
| `BukhgeimKlibanov1981` | Bukhgeim et al., *Global uniqueness of a class of multidimensional inverse problems*, Soviet Math. Dokl. 24 (1981) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `KauersPaule2011` | Kauers et al., *The Concrete Tetrahedron*, Springer  (2011) | **VERIFICATO** | Crossref-ricerca |  |
| `AdamsFournier2003` | Adams et al., *Sobolev Spaces*, Academic Press  (2003) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `LionsMagenes1972` | Lions et al., *Non-Homogeneous Boundary Value Problems and Applications I*, Springer  (1972) | **VERIFICATO** | Crossref-ricerca |  |
| `Gagliardo1957` | Gagliardo, *Caratterizzazioni delle tracce sulla frontiera relative ad alcune clas*, Rend. Sem. Mat. Univ. Padova 27 (1957) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Yosida1948` | Yosida, *On the differentiability and the representation of one-parameter semi-*, J. Math. Soc. Japan 1 (1948) | **VERIFICATO** | DOI/Crossref |  |
| `Hille1948` | Hille, *Functional Analysis and Semi-Groups*, AMS 31 (1948) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Colloquium Publications). |
| `LumerPhillips1961` | Lumer et al., *Dissipative operators in a Banach space*, Pacific J. Math. 11 (1961) | **VERIFICATO** | DOI/Crossref |  |
| `Stone1932` | Stone, *On one-parameter unitary groups in Hilbert space*, Ann. of Math. 33 (1932) | **VERIFICATO** | DOI/Crossref |  |
| `Trotter1958` | Trotter, *Approximation of semi-groups of operators*, Pacific J. Math. 8 (1958) | **VERIFICATO** | DOI/Crossref |  |
| `Trotter1959` | Trotter, *On the product of semi-groups of operators*, Proc. Amer. Math. Soc. 10 (1959) | **VERIFICATO** | DOI/Crossref |  |
| `Chernoff1968` | Chernoff, *Note on product formulas for operator semigroups*, J. Funct. Anal. 2 (1968) | **VERIFICATO** | DOI/Crossref |  |
| `Kato1978` | Kato, *Trotter's product formula for an arbitrary pair of self-adjoint contra*, Topics in Functional Analysis 3 (1978) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Petrowsky1938` | Petrowsky, *{\"U}ber das Cauchysche Problem f{\"u}r Systeme von partiellen Differe*, Bull. Univ. {\'E}tat Moscou S{\'e}r. Int 1 (1938) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Garding1951` | G{\aa}rding, *Linear hyperbolic partial differential equations with constant coeffic*, Acta Math. 85 (1951) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `KreissLorenz1989` | Kreiss et al., *Initial-Boundary Value Problems and the Navier--Stokes Equations*, Academic Press  (1989) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2004). |
| `Hadamard1923` | Hadamard, *Lectures on Cauchy's Problem in Linear Partial Differential Equations*, Yale Univ. Press  (1923) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |
| `BHdS2020` | Behrndt et al., *Boundary Value Problems, Weyl Functions, and Differential Operators*, Birkh{\"a}user  (2020) | **VERIFICATO** | Crossref-ricerca |  |
| `KostrykinSchrader1999` | Kostrykin et al., *Kirchhoff's rule for quantum wires*, J. Phys. A 32 (1999) | **VERIFICATO** | Crossref-ricerca |  |
| `Naimark1967` | Naimark, *Linear Differential Operators, Part I*, Ungar  (1967) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Mikhailov1962` | Mikhailov, *On Riesz bases in L2(0,1)*, Dokl. Akad. Nauk SSSR 144 (1962) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Keselman1964` | Kesel'man, *On the unconditional convergence of eigenfunction expansions of certai*, Izv. Vyssh. Uchebn. Zaved. Mat.  (1964) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Young1980` | Young, *An Introduction to Nonharmonic Fourier Series*, Academic Press  (1980) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Christensen2016` | Christensen, *An Introduction to Frames and Riesz Bases*, Birkh{\"a}user  (2016) | **VERIFICATO** | Crossref-ricerca |  |
| `DuffinSchaeffer1952` | Duffin et al., *A class of nonharmonic Fourier series*, Trans. Amer. Math. Soc. 72 (1952) | **VERIFICATO** | DOI/Crossref |  |
| `Kadec1964` | Kadec, *The exact value of the Paley--Wiener constant*, Dokl. Akad. Nauk SSSR 155 (1964) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Bari1951` | Bari, *Biorthogonal systems and bases in Hilbert space*, Uchen. Zap. Mosk. Gos. Univ. 148 (1951) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `GohbergKrein1969` | Gohberg et al., *Introduction to the Theory of Linear Nonselfadjoint Operators*, AMS  (1969) | **VERIFICATO** | Crossref-ricerca |  |
| `FeingoldVarga1962` | Feingold et al., *Block diagonally dominant matrices and generalizations of the Gerschgo*, Pacific J. Math. 12 (1962) | **VERIFICATO** | Crossref-ricerca |  |
| `Fokas2008` | Fokas, *A Unified Approach to Boundary Value Problems*, SIAM  (2008) | **VERIFICATO** | Crossref-ricerca |  |
| `BirkhoffRota1989` | Birkhoff et al., *Ordinary Differential Equations*, Wiley  (1989) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The Mathematical Gazette). |
| `Titchmarsh1937` | Titchmarsh, *Introduction to the Theory of Fourier Integrals*, Oxford Univ. Press  (1937) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Watson1944` | Watson, *A Treatise on the Theory of Bessel Functions*, Cambridge Univ. Press  (1944) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: National Mathematics Magazine). |
| `SteinWeiss1971` | Stein et al., *Introduction to Fourier Analysis on Euclidean Spaces*, Princeton Univ. Press  (1971) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1972). |
| `Weyl1912` | Weyl, *Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller*, Math. Ann. 71 (1912) | **VERIFICATO** | Crossref-ricerca |  |
| `Rosenberg1997` | Rosenberg, *The Laplacian on a Riemannian Manifold*, Cambridge Univ. Press  (1997) | **VERIFICATO** | Crossref-ricerca |  |
| `MIT18303` | Hancock, *18.303 Linear Partial Differential Equations, Fall 2006, lecture notes*,   () | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `MIT1803` | , *18.03 Differential Equations, Spring 2010, lecture notes*,   () | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |

### PR-C2e

Conteggi: VERIFICATO 17, VERIFICATO-K 8

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Evans2010` | Evans, *Partial Differential Equations*, American Mathematical Society 19 (2010) | **VERIFICATO** | Crossref-ricerca |  |
| `Hormander1983I` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators I: Distribution *, Springer  (1983) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Classics in Mathematics). |
| `Hormander1983II` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators II: Differential*, Springer  (1983) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `CourantHilbert1962` | Courant et al., *Methods of Mathematical Physics, Vol. II: Partial Differential Equatio*, Interscience  (1962) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Journal of Applied Mechanics). |
| `Polyanin2002` | Polyanin, *Handbook of Linear Partial Differential Equations for Engineers and Sc*, Chapman \& Hall/CRC  (2002) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2001). |
| `PolyaninZaitsev2004` | Polyanin et al., *Handbook of Nonlinear Partial Differential Equations*, Chapman \& Hall/CRC  (2004) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2016). |
| `DLMF` | Olver et al., *NIST Digital Library of Mathematical Functions*,   () | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Olver1993` | Olver, *Applications of Lie Groups to Differential Equations*, Springer  (1993) | **VERIFICATO** | Crossref-ricerca |  |
| `Pazy1983` | Pazy, *Semigroups of Linear Operators and Applications to Partial Differentia*, Springer  (1983) | **VERIFICATO** | Crossref-ricerca |  |
| `Kato1995` | Kato, *Perturbation Theory for Linear Operators*, Springer  (1995) | **VERIFICATO** | Crossref-ricerca |  |
| `Whitham1974` | Whitham, *Linear and Nonlinear Waves*, Wiley  (1974) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1999). |
| `Taylor2011` | Taylor, *Partial Differential Equations I--III*, Springer  (2011) | **VERIFICATO** | Crossref-ricerca |  |
| `SamkoKilbasMarichev1993` | Samko et al., *Fractional Integrals and Derivatives: Theory and Applications*, Gordon and Breach  (1993) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Podlubny1999` | Podlubny, *Fractional Differential Equations*, Academic Press  (1999) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `AblowitzClarkson1991` | Ablowitz et al., *Solitons, Nonlinear Evolution Equations and Inverse Scattering*, Cambridge University Press  (1991) | **VERIFICATO** | Crossref-ricerca |  |
| `GuentherLee1996` | Guenther et al., *Partial Differential Equations of Mathematical Physics and Integral Eq*, Dover  (1996) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `MyintUDebnath2007` | Myint-U et al., *Linear Partial Differential Equations for Scientists and Engineers*, Birkh{\"a}user  (2007) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Vilenkin1968` | Vilenkin, *Special Functions and the Theory of Group Representations*, American Mathematical Society  (1968) | **VERIFICATO** | Crossref-ricerca |  |
| `WeiNorman1963` | Wei et al., *Lie Algebraic Solution of Linear Differential Equations*, Journal of Mathematical Physics 4 (1963) | **VERIFICATO** | Crossref-ricerca |  |
| `AvronHerbst1977` | Avron et al., *Spectral and Scattering Theory of Schr{\"o}dinger Operators Related to*, Communications in Mathematical Physics 52 (1977) | **VERIFICATO** | Crossref-ricerca |  |
| `JKO1998` | Jordan et al., *The Variational Formulation of the Fokker--Planck Equation*, SIAM Journal on Mathematical Analysis 29 (1998) | **VERIFICATO** | Crossref-ricerca |  |
| `Hopf1950` | Hopf, *The Partial Differential Equation $u_t + uu_x = \mu u_{xx}$*, Communications on Pure and Applied Mathe 3 (1950) | **VERIFICATO** | Crossref-ricerca |  |
| `Cole1951` | Cole, *On a Quasi-Linear Parabolic Equation Occurring in Aerodynamics*, Quarterly of Applied Mathematics 9 (1951) | **VERIFICATO** | Crossref-ricerca |  |
| `MIT18303` | Hancock, *18.303 Linear Partial Differential Equations, Fall 2006*,   () | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `MIT1803` | Miller, *18.03 Differential Equations, Spring 2010, lecture notes*,   () | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |

### R1

Conteggi: VERIFICATO 60, VERIFICATO-K 7

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Aronszajn1950` | Aronszajn, *Theory of reproducing kernels*, Trans. Amer. Math. Soc. 68 (1950) | **VERIFICATO** | Crossref-ricerca |  |
| `SchoelkopfHerbrichSmola2001` | Sch{\"o}lkopf et al., *A generalized representer theorem*, COLT 2001, LNCS 2111  (2001) | **VERIFICATO** | Crossref-ricerca |  |
| `SchoelkopfSmola2002` | Sch{\"o}lkopf et al., *Learning with Kernels*, MIT Press  (2002) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `KimeldorfWahba1970` | Kimeldorf et al., *A correspondence between {B}ayesian estimation on stochastic processes*, Ann. Math. Statist. 41 (1970) | **VERIFICATO** | Crossref-ricerca |  |
| `KimeldorfWahba1971` | Kimeldorf et al., *Some results on {T}chebycheffian spline functions*, J. Math. Anal. Appl. 33 (1971) | **VERIFICATO** | Crossref-ricerca |  |
| `SteinwartChristmann2008` | Steinwart et al., *Support Vector Machines*, Springer  (2008) | **VERIFICATO** | Crossref-ricerca |  |
| `PaulsenRaghupathi2016` | Paulsen et al., *An Introduction to the Theory of Reproducing Kernel {H}ilbert Spaces*, Cambridge Univ. Press 152 (2016) | **VERIFICATO** | Crossref-ricerca |  |
| `EnglHankeNeubauer1996` | Engl et al., *Regularization of Inverse Problems*, Kluwer  (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `Scherzer2009` | Scherzer et al., *Variational Methods in Imaging*, Springer  (2009) | **VERIFICATO** | Crossref-ricerca |  |
| `GrasmairHaltmeierScherzer2011` | Grasmair et al., *Necessary and sufficient conditions for linear convergence of $\ell^1$*, Comm. Pure Appl. Math. 64 (2011) | **VERIFICATO** | Crossref-ricerca |  |
| `Hohage2000` | Hohage, *Regularization of exponentially ill-posed problems*, Numer. Funct. Anal. Optim. 21 (2000) | **VERIFICATO** | Crossref-ricerca |  |
| `Fuchs2004` | Fuchs, *On sparse representations in arbitrary redundant bases*, IEEE Trans. Inf. Theory 50 (2004) | **VERIFICATO** | Crossref-ricerca |  |
| `CandesRombergTao2006` | Cand{\`e}s et al., *Robust uncertainty principles: exact signal reconstruction from highly*, IEEE Trans. Inf. Theory 52 (2006) | **VERIFICATO** | Crossref-ricerca |  |
| `CandesTao2005` | Cand{\`e}s et al., *Decoding by linear programming*, IEEE Trans. Inf. Theory 51 (2005) | **VERIFICATO** | Crossref-ricerca |  |
| `Candes2008` | Cand{\`e}s, *The restricted isometry property and its implications for compressed s*, C. R. Acad. Sci. Paris, Ser. I 346 (2008) | **VERIFICATO** | Crossref-ricerca |  |
| `CaiZhang2014` | Cai et al., *Sparse representation of a polytope and recovery of sparse signals and*, IEEE Trans. Inf. Theory 60 (2014) | **VERIFICATO** | Crossref-ricerca |  |
| `Donoho2006` | Donoho, *Compressed sensing*, IEEE Trans. Inf. Theory 52 (2006) | **VERIFICATO** | Crossref-ricerca |  |
| `DonohoHuo2001` | Donoho et al., *Uncertainty principles and ideal atomic decomposition*, IEEE Trans. Inf. Theory 47 (2001) | **VERIFICATO** | Crossref-ricerca |  |
| `DonohoElad2003` | Donoho et al., *Optimally sparse representation in general (nonorthogonal) dictionarie*, Proc. Natl. Acad. Sci. USA 100 (2003) | **VERIFICATO** | Crossref-ricerca |  |
| `GribonvalNielsen2003` | Gribonval et al., *Sparse representations in unions of bases*, IEEE Trans. Inf. Theory 49 (2003) | **VERIFICATO** | Crossref-ricerca |  |
| `EladBruckstein2002` | Elad et al., *A generalized uncertainty principle and sparse representation in pairs*, IEEE Trans. Inf. Theory 48 (2002) | **VERIFICATO** | Crossref-ricerca |  |
| `Tropp2004` | Tropp, *Greed is good: algorithmic results for sparse approximation*, IEEE Trans. Inf. Theory 50 (2004) | **VERIFICATO** | Crossref-ricerca | Cor. 3.6 (condizione di coerenza m < (1/mu+1)/2 per OMP e BP) e Thm 3.1/3.3/3.5 riscontrati sul PDF. |
| `Tropp2006` | Tropp, *Just relax: convex programming methods for identifying sparse signals *, IEEE Trans. Inf. Theory 52 (2006) | **VERIFICATO** | Crossref-ricerca |  |
| `FoucartRauhut2013` | Foucart et al., *A Mathematical Introduction to Compressive Sensing*, Birkh{\"a}user  (2013) | **VERIFICATO** | Crossref-ricerca |  |
| `TillmannPfetsch2014` | Tillmann et al., *The computational complexity of the restricted isometry property, the *, IEEE Trans. Inf. Theory 60 (2014) | **VERIFICATO** | Crossref-ricerca |  |
| `DonohoKutyniok2013` | Donoho et al., *Microlocal analysis of the geometric separation problem*, Comm. Pure Appl. Math. 66 (2013) | **VERIFICATO** | Crossref-ricerca+arXiv | Prop. 2.1 e Lemma 2.1 (concentrazione congiunta <= max cluster coherence) riscontrati su arXiv:1004.3006. |
| `StarckEladDonoho2005` | Starck et al., *Image decomposition via the combination of sparse representations and *, IEEE Trans. Image Process. 14 (2005) | **VERIFICATO** | Crossref-ricerca |  |
| `CandesFernandezGranda2014` | Cand{\`e}s et al., *Towards a mathematical theory of super-resolution*, Comm. Pure Appl. Math. 67 (2014) | **VERIFICATO** | Crossref-ricerca |  |
| `SchiebingerRobevaRecht2018` | Schiebinger et al., *Superresolution without separation*, Information and Inference 7 (2018) | **VERIFICATO** | Crossref-ricerca+arXiv | Inf. Inference 7(1):1-30 ok; abstract: recupero esatto da 2M+1 osservazioni senza separazione (con positivita'/T-sistema): supportato. |
| `DuvalPeyre2015` | Duval et al., *Exact support recovery for sparse spikes deconvolution*, Found. Comput. Math. 15 (2015) | **VERIFICATO** | Crossref-ricerca |  |
| `ChandrasekaranRPW2012` | Chandrasekaran et al., *The convex geometry of linear inverse problems*, Found. Comput. Math. 12 (2012) | **VERIFICATO** | Crossref-ricerca |  |
| `EldarKuppingerBolcskei2010` | Eldar et al., *Block-sparse signals: uncertainty relations and efficient recovery*, IEEE Trans. Signal Process. 58 (2010) | **VERIFICATO** | Crossref-ricerca |  |
| `BachJMO2012` | Bach et al., *Optimization with sparsity-inducing penalties*, Found. Trends Mach. Learn. 4 (2012) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref:  None None 2011 DOI 10.1561/9781601985118. |
| `SimonFHT2013` | Simon et al., *A sparse-group lasso*, J. Comput. Graph. Statist. 22 (2013) | **VERIFICATO** | Crossref-ricerca |  |
| `RudinOsherFatemi1992` | Rudin et al., *Nonlinear total variation based noise removal algorithms*, Physica D 60 (1992) | **VERIFICATO** | Crossref-ricerca |  |
| `CandesWakinBoyd2008` | Cand{\`e}s et al., *Enhancing sparsity by reweighted $\ell_1$ minimization*, J. Fourier Anal. Appl. 14 (2008) | **VERIFICATO** | Crossref-ricerca |  |
| `Gribonval2011` | Gribonval, *Should penalized least squares regression be interpreted as maximum a *, IEEE Trans. Signal Process. 59 (2011) | **VERIFICATO** | Crossref-ricerca |  |
| `ColemanPothen1986` | Coleman et al., *The null space problem {I}. {C}omplexity*, SIAM J. Algebraic Discrete Methods 7 (1986) | **VERIFICATO** | Crossref-ricerca |  |
| `BenOrTiwari1988` | Ben-Or et al., *A deterministic algorithm for sparse multivariate polynomial interpola*, Proc. 20th ACM STOC  (1988) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref: Proceedings of the twentieth annual ACM symposium on Theory of computing  - STOC '88 None 301-309 1988 DOI 10.1145/62212.62241. |
| `Christensen2016` | Christensen, *An Introduction to Frames and {R}iesz Bases*, Birkh{\"a}user  (2016) | **VERIFICATO** | Crossref-ricerca |  |
| `Young2001` | Young, *An Introduction to Nonharmonic {F}ourier Series*, Academic Press  (2001) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `ShapiroShields1961` | Shapiro et al., *On some interpolation problems for analytic functions*, Amer. J. Math. 83 (1961) | **VERIFICATO** | Crossref-ricerca |  |
| `Nikolski1986` | Nikolski, *Treatise on the Shift Operator*, Springer  (1986) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `AvdoninIvanov1995` | Avdonin et al., *Families of Exponentials*, Cambridge Univ. Press  (1995) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `AliAntoineGazeau1993` | Ali et al., *Continuous frames in {H}ilbert space*, Ann. Physics 222 (1993) | **VERIFICATO** | Crossref-ricerca |  |
| `Bargmann1961` | Bargmann, *On a {H}ilbert space of analytic functions and an associated integral *, Comm. Pure Appl. Math. 14 (1961) | **VERIFICATO** | Crossref-ricerca |  |
| `Hall1994` | Hall, *The {S}egal--{B}argmann ``coherent state'' transform for compact {L}ie*, J. Funct. Anal. 122 (1994) | **VERIFICATO** | Crossref-ricerca |  |
| `RasmussenWilliams2006` | Rasmussen et al., *Gaussian Processes for Machine Learning*, MIT Press  (2006) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2005). |
| `Driscoll1973` | Driscoll, *The reproducing kernel {H}ilbert space structure of the sample paths o*, Z. Wahrsch. Verw. Gebiete 26 (1973) | **VERIFICATO** | Crossref-ricerca |  |
| `LukicBeder2001` | Luki{\'c} et al., *Stochastic processes with sample paths in reproducing kernel {H}ilbert*, Trans. Amer. Math. Soc. 353 (2001) | **VERIFICATO** | Crossref-ricerca |  |
| `HarkonenLHR2023` | H{\"a}rk{\"o}nen et al., *Gaussian process priors for systems of linear partial differential equ*, ICML 2023  (2023) | **VERIFICATO** | arXiv |  |
| `HuangEtAl2024BEPGP` | Huang et al., *Gaussian process priors for boundary value problems of linear partial *,   (2024) | **VERIFICATO** | arXiv |  |
| `LangeHegermann2018` | Lange-Hegermann, *Algorithmic linearly constrained {G}aussian processes*, NeurIPS 2018  (2018) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `DuvenaudNickischRasmussen2011` | Duvenaud et al., *Additive {G}aussian processes*, NeurIPS 2011  (2011) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Koopman1931` | Koopman, *Hamiltonian systems and transformation in {H}ilbert space*, Proc. Natl. Acad. Sci. USA 17 (1931) | **VERIFICATO** | Crossref-ricerca |  |
| `Mezic2005` | Mezi{\'c}, *Spectral properties of dynamical systems, model reduction and decompos*, Nonlinear Dyn. 41 (2005) | **VERIFICATO** | Crossref-ricerca |  |
| `Rowley2009` | Rowley et al., *Spectral analysis of nonlinear flows*, J. Fluid Mech. 641 (2009) | **VERIFICATO** | Crossref-ricerca |  |
| `Schmid2010` | Schmid, *Dynamic mode decomposition of numerical and experimental data*, J. Fluid Mech. 656 (2010) | **VERIFICATO** | Crossref-ricerca |  |
| `Tu2014` | Tu et al., *On dynamic mode decomposition: theory and applications*, J. Comput. Dyn. 1 (2014) | **VERIFICATO** | Crossref-ricerca |  |
| `KordaMezic2018` | Korda et al., *On convergence of extended dynamic mode decomposition to the {K}oopman*, J. Nonlinear Sci. 28 (2018) | **VERIFICATO** | Crossref-ricerca |  |
| `MauroyMezicSusuki2020` | Mauroy et al., *The {K}oopman Operator in Systems and Control*, Springer  (2020) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `vanderPutSinger2003` | van der Put et al., *Galois Theory of Linear Differential Equations*, Springer  (2003) | **VERIFICATO** | Crossref-ricerca |  |
| `RosenbloomWidder1959` | Rosenbloom et al., *Expansions in terms of heat polynomials and associated functions*, Trans. Amer. Math. Soc. 92 (1959) | **VERIFICATO** | Crossref-ricerca |  |
| `Owhadi2019` | Owhadi et al., *Operator-Adapted Wavelets, Fast Solvers, and Numerical Homogenization*, Cambridge Univ. Press  (2019) | **VERIFICATO** | Crossref-ricerca |  |
| `Ore1933` | Ore, *Theory of non-commutative polynomials*, Ann. of Math. 34 (1933) | **VERIFICATO** | Crossref-ricerca |  |
| `SchollBachoBocheKutyniok2026` | Scholl et al., *Symbolic recovery of differential equations: the identifiability probl*, Machine Learning 115 (2026) | **VERIFICATO** | Crossref-ricerca+arXiv | Completare: number=6, art. 139 (non 'pages'), doi 10.1007/s10994-026-07068-0. |
| `HeZhaoZhong2024` | He et al., *How much can one learn a partial differential equation from its soluti*, Found. Comput. Math. 24 (2024) | **VERIFICATO** | DOI/Crossref |  |

### R2

Conteggi: METADATI ERRATI 1, VERIFICATO 16, VERIFICATO-K 4

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Ehrenpreis1970` | Ehrenpreis, *Fourier Analysis in Several Complex Variables*, Wiley-Interscience  (1970) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Palamodov1970` | Palamodov, *Linear Differential Operators with Constant Coefficients*, Springer 168 (1970) | **VERIFICATO** | Crossref-ricerca |  |
| `Malgrange1956` | Malgrange, *Existence et approximation des solutions des {\'e}quations aux d{\'e}r*, Annales de l'Institut Fourier 6 (1956) | **VERIFICATO** | DOI/Crossref | AIF 6:271-355, DOI 10.5802/aif.65 ok. |
| `HormanderICASV` | H{\"o}rmander, *An Introduction to Complex Analysis in Several Variables*, North-Holland  (1990) | **VERIFICATO-K** | - | Numerazione 7.6.13 (principio fondamentale) / 7.6.14 (prova del lemma di densita' degli esponenziali-polinomi) attestata da Lomadze, LAA 438 (2013) 2083-2089; coerente con l'uso in R2. Il §7.6 esiste solo dalla 3a ed. (1990): citare la 3a ed. Non riscontrato sul libro. Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `HormanderALPDO2` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators II*, Springer  (1983) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `Oberst1990` | Oberst, *Multidimensional Constant Linear Systems*, Acta Applicandae Mathematicae 20 (1990) | **METADATI ERRATI** | - | DOI errato: 10.1007/BF01235717 e' Oberst 1995, AAECC 6:211-243 ('Variations on the fundamental principle...'). DOI corretto 10.1007/BF00046908 (Acta Appl. Math. 20(1-2):1-175, 1990). |
| `Bjork1979` | Bj{\"o}rk, *Rings of Differential Operators*, North-Holland  (1979) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `AitElManssourHarkonenSturmfels2023` | Ait El Manssour et al., *Linear {PDE} with Constant Coefficients*, Glasgow Mathematical Journal 65 (2023) | **VERIFICATO** | DOI/Crossref+arXiv |  |
| `CidRuizSturmfels` | Cid-Ruiz et al., *Primary Decomposition with Differential Operators*, International Mathematics Research Notic  () | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `HarkonenLHRaita2023` | H{\"a}rk{\"o}nen et al., *Gaussian Process Priors for Systems of Linear Partial Differential Equ*, Proceedings of the 40th ICML 202 (2023) | **VERIFICATO** | arXiv |  |
| `Sturmfels2002` | Sturmfels, *Solving Systems of Polynomial Equations*, AMS 97 (2002) | **VERIFICATO** | Crossref-ricerca |  |
| `Fulton1969` | Fulton, *Algebraic Curves*, Benjamin  (1969) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Ore1933` | Ore, *Theory of Non-Commutative Polynomials*, Annals of Mathematics 34 (1933) | **VERIFICATO** | Crossref-ricerca |  |
| `BronsteinPetkovsek1996` | Bronstein et al., *An Introduction to Pseudo-Linear Algebra*, Theoretical Computer Science 157 (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `vanderPutSinger2003` | van der Put et al., *Galois Theory of Linear Differential Equations*, Springer 328 (2003) | **VERIFICATO** | Crossref-ricerca |  |
| `Singer1996` | Singer, *Testing Reducibility of Linear Differential Operators: A Group Theoret*, Applicable Algebra in Engineering, Commu 7 (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `Stanley1980` | Stanley, *Differentiably Finite Power Series*, European Journal of Combinatorics 1 (1980) | **VERIFICATO** | Crossref-ricerca |  |
| `KauersPaule2011` | Kauers et al., *The Concrete Tetrahedron*, Springer  (2011) | **VERIFICATO** | Crossref-ricerca |  |
| `Lipshitz1989` | Lipshitz, *D-finite Power Series*, Journal of Algebra 122 (1989) | **VERIFICATO** | Crossref-ricerca |  |
| `Zeilberger1990` | Zeilberger, *A Holonomic Systems Approach to Special Functions Identities*, J. Comput. Appl. Math. 32 (1990) | **VERIFICATO** | Crossref-ricerca |  |
| `BostanChyzakLiSalvy2012` | Bostan et al., *Fast Computation of Common Left Multiples of Linear Ordinary Different*, ISSAC 2012  (2012) | **VERIFICATO** | Crossref-ricerca |  |

### R3

Conteggi: VERIFICATO 15, VERIFICATO-K 9

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Evans2010` | Evans, *Partial Differential Equations*, American Mathematical Society 19 (2010) | **VERIFICATO** | Crossref-ricerca |  |
| `CourantHilbert1953` | Courant et al., *Methods of Mathematical Physics, Vol. I*, Interscience  (1953) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |
| `CourantHilbert1962` | Courant et al., *Methods of Mathematical Physics, Vol. II: Partial Differential Equatio*, Interscience  (1962) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Journal of Applied Mechanics). |
| `Polyanin2002` | Polyanin, *Handbook of Linear Partial Differential Equations for Engineers and Sc*, Chapman \& Hall/CRC  (2002) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2001). |
| `PolyaninNazaikinskii2016` | Polyanin et al., *Handbook of Linear Partial Differential Equations for Engineers and Sc*, CRC Press  (2016) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2001). |
| `DLMF` | Olver et al., *NIST Handbook of Mathematical Functions*, Cambridge University Press  (2010) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Zettl2005` | Zettl, *Sturm--Liouville Theory*, American Mathematical Society 121 (2005) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Mathematical Surveys and Monographs). |
| `Titchmarsh1962` | Titchmarsh, *Eigenfunction Expansions Associated with Second-Order Differential Equ*, Oxford University Press  (1962) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `CoddingtonLevinson1955` | Coddington et al., *Theory of Ordinary Differential Equations*, McGraw-Hill  (1955) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |
| `GuentherLee1996` | Guenther et al., *Partial Differential Equations of Mathematical Physics and Integral Eq*, Dover  (1996) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `MyintUDebnath2007` | Myint-U et al., *Linear Partial Differential Equations for Scientists and Engineers*, Birkh{\"a}user  (2007) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Widder1975` | Widder, *The Heat Equation*, Academic Press  (1975) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `RosenbloomWidder1959` | Rosenbloom et al., *Expansions in terms of heat polynomials and associated functions*, Transactions of the American Mathematica 92 (1959) | **VERIFICATO** | Crossref-ricerca |  |
| `ValleeSoares2004` | Vall{\'e}e et al., *Airy Functions and Applications to Physics*, Imperial College Press  (2004) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Watson1944` | Watson, *A Treatise on the Theory of Bessel Functions*, Cambridge University Press  (1944) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: National Mathematics Magazine). |
| `Lebedev1965` | Lebedev, *Special Functions and Their Applications*, Prentice-Hall  (1965) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |
| `Graff1975` | Graff, *Wave Motion in Elastic Solids*, Ohio State University Press  (1975) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Hopf1950` | Hopf, *The partial differential equation u_t + u u_x = \mu u_{xx}*, Communications on Pure and Applied Mathe 3 (1950) | **VERIFICATO** | Crossref-ricerca |  |
| `Cole1951` | Cole, *On a quasi-linear parabolic equation occurring in aerodynamics*, Quarterly of Applied Mathematics 9 (1951) | **VERIFICATO** | Crossref-ricerca |  |
| `WeiNorman1963` | Wei et al., *Lie algebraic solution of linear differential equations*, Journal of Mathematical Physics 4 (1963) | **VERIFICATO** | Crossref-ricerca |  |
| `Vilenkin1968` | Vilenkin, *Special Functions and the Theory of Group Representations*, American Mathematical Society 22 (1968) | **VERIFICATO** | Crossref-ricerca |  |
| `Ehrenpreis1970` | Ehrenpreis, *Fourier Analysis in Several Complex Variables*, Wiley-Interscience  (1970) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `MIT1803` | {MIT OpenCourseWare}, *18.03 Differential Equations, Spring 2010, lecture notes*,   () | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `MIT18303` | Hancock, *18.303 Linear Partial Differential Equations, Fall 2006, lecture notes*,   () | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |

### R4

Conteggi: CONTESTO NON SUPPORTATO 2, VERIFICATO 28, VERIFICATO-K 6

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `VetterliMarzilianoBlu2002` | Vetterli et al., *Sampling signals with finite rate of innovation*, IEEE Trans. Signal Process. 50 (2002) | **VERIFICATO** | Crossref-ricerca |  |
| `DragottiVetterliBlu2007` | Dragotti et al., *Sampling moments and reconstructing signals of finite rate of innovati*, IEEE Trans. Signal Process. 55 (2007) | **VERIFICATO** | Crossref-ricerca |  |
| `HuaSarkar1990` | Hua et al., *Matrix pencil method for estimating parameters of exponentially damped*, IEEE Trans. Acoust. Speech Signal Proces 38 (1990) | **VERIFICATO** | Crossref-ricerca |  |
| `PeterPlonka2013` | Peter et al., *A generalized {Prony} method for reconstruction of sparse sums of eige*, Inverse Problems 29 (2013) | **VERIFICATO** | Crossref-ricerca |  |
| `StampferPlonka2019` | Stampfer et al., *The generalized operator based {Prony} method*,   (2019) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Mourrain2018` | Mourrain, *Polynomial-exponential decomposition from moments*, Found. Comput. Math. 18 (2018) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `KunisPeterRoemerOhe2016` | Kunis et al., *A multivariate generalization of {Prony}'s method*, Linear Algebra Appl. 490 (2016) | **VERIFICATO** | Crossref-ricerca |  |
| `Kauers2009Guessing` | Kauers, *Guessing Handbook*,   (2009) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `KauersJaroschekJohansson2015` | Kauers et al., *Ore polynomials in {Sage}*, Computer Algebra and Polynomials 8942 (2015) | **VERIFICATO** | Crossref-ricerca |  |
| `SalvyZimmermann1994` | Salvy et al., *{GFUN}: a {Maple} package for the manipulation of generating and holon*, ACM Trans. Math. Softw. 20 (1994) | **VERIFICATO** | Crossref-ricerca |  |
| `BeckermannLabahn1994` | Beckermann et al., *A uniform approach for the fast computation of matrix-type {Pad\'e} ap*, SIAM J. Matrix Anal. Appl. 15 (1994) | **VERIFICATO** | Crossref-ricerca |  |
| `ChenKauersSinger2016` | Chen et al., *Desingularization of {Ore} operators*, J. Symbolic Comput. 74 (2016) | **VERIFICATO** | Crossref-ricerca |  |
| `Ore1933` | Ore, *Theory of non-commutative polynomials*, Ann. of Math. 34 (1933) | **VERIFICATO** | Crossref-ricerca |  |
| `Ritt1950` | Ritt, *Differential Algebra*, AMS Colloquium Publ. 33  (1950) | **VERIFICATO** | Crossref-ricerca |  |
| `Kolchin1973` | Kolchin, *Differential Algebra and Algebraic Groups*, Academic Press  (1973) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `BoulierEtAl1995` | Boulier et al., *Representation for the radical of a finitely generated differential id*, Proc. ISSAC '95  (1995) | **VERIFICATO** | Crossref-ricerca |  |
| `BoulierEtAl2009` | Boulier et al., *Computing representations for radicals of finitely generated different*, Appl. Algebra Engrg. Comm. Comput. 20 (2009) | **VERIFICATO** | Crossref-ricerca |  |
| `LjungGlad1994` | Ljung et al., *On global identifiability for arbitrary model parametrizations*, Automatica 30 (1994) | **VERIFICATO** | Crossref-ricerca |  |
| `ByrneEtAl2024` | Byrne et al., *Algebraic identifiability of partial differential equation models*,   (2024) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `SchollBachoBocheKutyniok2026` | Scholl et al., *Symbolic recovery of differential equations: the identifiability probl*, Machine Learning 115 (2026) | **CONTESTO NON SUPPORTATO** | Crossref-ricerca+arXiv | Metadati OK (Mach. Learn. 115(6), art. 139, 2026, DOI 10.1007/s10994-026-07068-0; manca DOI/numero). Cor.1, Prop.6, Prop.7: supportati (letti su arXiv v10). Contesto impreciso: 'Prop. 10 coeff. variabili mai identificabili' (anche RIPRESA §4H) - Prop.10 riguarda ODE di ORDINE 2 lineari in (u,u_t) con coeff. continui; per l'ordine 1 la Prop.8 da' unicita' sse u ha solo zeri isolati. Scrivere 'ordine >= 2'. |
| `HeZhaoZhong2024` | He et al., *How much can one learn a partial differential equation from its soluti*, Found. Comput. Math. 24 (2024) | **VERIFICATO** | DOI/Crossref+arXiv | Thm 3.2/3.4/3.5 riscontrati (arXiv v2); in R4 usati correttamente come 'soglia sui modi' e 'coeff. variabili'. |
| `StanhopeRubinSwigon2014` | Stanhope et al., *Identifiability of linear and linear-in-parameters dynamical systems f*, SIAM J. Appl. Dyn. Syst. 13 (2014) | **VERIFICATO** | DOI/Crossref | Pagine 1792-1815 confermate (Crossref); 'identificabile sse traiettoria non confinata in sottospazio proprio (x0 ciclico)' coerente con l'abstract. |
| `QiuEtAl2022` | Qiu et al., *Identifiability analysis of linear ordinary differential equation syst*, Appl. Math. Comput. 430 (2022) | **VERIFICATO** | DOI/Crossref |  |
| `Ehrenpreis1970` | Ehrenpreis, *Fourier Analysis in Several Complex Variables*, Wiley-Interscience  (1970) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Palamodov1970` | Palamodov, *Linear Differential Operators with Constant Coefficients*, Springer  (1970) | **VERIFICATO** | Crossref-ricerca |  |
| `HormanderII` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators II*, Springer  (1983) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `Bjork1979` | Bj{\"o}rk, *Rings of Differential Operators*, North-Holland  (1979) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `CidRuizHomsSturmfels2021` | Cid-Ruiz et al., *Primary ideals and their differential equations*, Found. Comput. Math. 21 (2021) | **VERIFICATO** | Crossref-ricerca |  |
| `AitElManssourHarkonenSturmfels2021` | Ait El Manssour et al., *Linear {PDE} with constant coefficients*,   (2021) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Borg1946` | Borg, *Eine {Umkehrung} der {Sturm--Liouvilleschen} {Eigenwertaufgabe}*, Acta Math. 78 (1946) | **VERIFICATO** | Crossref-ricerca |  |
| `GelfandLevitan1951` | Gel'fand et al., *On the determination of a differential equation from its spectral func*, Izv. Akad. Nauk SSSR Ser. Mat. 15 (1951) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Marchenko1977` | Marchenko, *Sturm--Liouville Operators and Applications*, Naukova Dumka (trad. Birkh{\"a}user 1986  (1977) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2011). |
| `HochstadtLieberman1978` | Hochstadt et al., *An inverse {Sturm--Liouville} problem with mixed given data*, SIAM J. Appl. Math. 34 (1978) | **VERIFICATO** | Crossref-ricerca |  |
| `FreilingYurko2001` | Freiling et al., *Inverse {Sturm--Liouville} Problems and their Applications*, Nova Science  (2001) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Pierce1979` | Pierce, *Unique identification of eigenvalues and coefficients in a parabolic p*, SIAM J. Control Optim. 17 (1979) | **CONTESTO NON SUPPORTATO** | DOI/Crossref | Esiste (SICON 17(4):494-499, DOI ok), ma il REPORT (R4 riga 62) afferma che una soluzione parabolica 'determina i coefficienti' se i coefficienti di Fourier iniziali sono non nulli. L'abstract dice il contrario: dall'osservazione in UN PUNTO nel tempo si determinano gli AUTOVALORI; 'The coefficients are not uniquely determined'; solo in forma normale l'unico coefficiente e' determinato 'in certain cases' (via Gel'fand-Levitan / due spettri). Riformulare. |
| `IarrobinoKanev1999` | Iarrobino et al., *Power Sums, {Gorenstein} Algebras, and Determinantal Loci*, Springer 1721 (1999) | **VERIFICATO** | Crossref-ricerca |  |

### R5

Conteggi: METADATI ERRATI 3, VERIFICATO 19, VERIFICATO-K 5

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Kato1995` | Kato, *Perturbation Theory for Linear Operators*, Springer  (1995) | **VERIFICATO** | Crossref-ricerca |  |
| `ReedSimon1` | Reed et al., *Methods of Modern Mathematical Physics I: Functional Analysis*, Academic Press  (1980) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `ReedSimon2` | Reed et al., *Methods of Modern Mathematical Physics II: Fourier Analysis, Self-Adjo*, Academic Press  (1975) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `ReedSimon4` | Reed et al., *Methods of Modern Mathematical Physics IV: Analysis of Operators*, Academic Press  (1978) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Pazy1983` | Pazy, *Semigroups of Linear Operators and Applications to Partial Differentia*, Springer 44 (1983) | **VERIFICATO** | Crossref-ricerca |  |
| `EngelNagel2000` | Engel et al., *One-Parameter Semigroups for Linear Evolution Equations*, Springer 194 (2000) | **VERIFICATO-K** | - | Numerazioni usate in R5 (II.2.7, III.1.3, III.1.10, III.2.10, III.3.14-3.16, III.5.8) riscontrate sul testo: corrette. Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Sakurai` | Sakurai et al., *Modern Quantum Mechanics*, Addison-Wesley  (2011) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2017). |
| `Miller1977` | Miller, *Symmetry and Separation of Variables*, Addison-Wesley 4 (1977) | **VERIFICATO** | Crossref-ricerca | Cap. 2 = 'The Schroedinger and Heat Equations' (TOC Cambridge): coerente con R7/R5. Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1984). |
| `Schmudgen2012` | Schm{\"u}dgen, *Unbounded Self-adjoint Operators on Hilbert Space*, Springer 265 (2012) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `BlanesCasasOteoRos2009` | Blanes et al., *The {M}agnus expansion and some of its applications*, Physics Reports 470 (2009) | **VERIFICATO** | DOI/Crossref |  |
| `BlanesCasas2004` | Blanes et al., *On the convergence and optimization of the {B}aker--{C}ampbell--{H}aus*, Linear Algebra and its Applications 378 (2004) | **VERIFICATO** | Crossref-ricerca |  |
| `CasasMuruaNadinic2012` | Casas et al., *Efficient computation of the {Z}assenhaus formula*, Computer Physics Communications 183 (2012) | **VERIFICATO** | DOI/Crossref+arXiv | Dominio di convergenza: la regione trovata CONTIENE //X//+//Y// < 1.054 (non si riduce ad essa); Suzuki 0.1931, Bayen 0.5967 riscontrati su arXiv:1204.0389 v2. |
| `Suzuki1977` | Suzuki, *On the convergence of exponential operators -- the {Z}assenhaus formul*, Communications in Mathematical Physics 57 (1977) | **VERIFICATO** | Crossref-ricerca |  |
| `Bayen1979` | Bayen, *On the convergence of the {Z}assenhaus formula*, Letters in Mathematical Physics 3 (1979) | **VERIFICATO** | Crossref-ricerca |  |
| `MoanNiesen2008` | Moan et al., *Convergence of the {M}agnus series*, Foundations of Computational Mathematics 8 (2008) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Casas2007` | Casas, *Sufficient conditions for the convergence of the {M}agnus expansion*, Journal of Physics A 40 (2007) | **VERIFICATO** | Crossref-ricerca |  |
| `MoanOteo2001` | Moan et al., *Convergence of the exponential {L}ie series*, Journal of Mathematical Physics 42 (2001) | **VERIFICATO** | Crossref-ricerca |  |
| `Trotter1959` | Trotter, *On the product of semi-groups of operators*, Proceedings of the AMS 10 (1959) | **VERIFICATO** | Crossref-ricerca |  |
| `Chernoff1968` | Chernoff, *Note on product formulas for operator semigroups*, Journal of Functional Analysis 2 (1968) | **VERIFICATO** | Crossref-ricerca |  |
| `Kato1978` | Kato, *Trotter's product formula for an arbitrary pair of self-adjoint contra*, Topics in Functional Analysis 3 (1978) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `JahnkeLubich2000` | Jahnke et al., *Error bounds for exponential operator splittings*, BIT Numerical Mathematics 40 (2000) | **VERIFICATO** | Crossref-ricerca | Thm 2.1(a,b), 2.2, 2.3 riscontrati sul PDF: ipotesi e ordini come in R5-T6 (Thm 2.3: ordine 3/2 con B(-A)^{-1/2} limitato; in Thm 2.1(b) la norma e' //(-A)^beta v//). Aggiungere doi 10.1023/A:1022396519656. |
| `WeiNorman1963` | Wei et al., *Lie algebraic solution of linear differential equations*, Journal of Mathematical Physics 4 (1963) | **VERIFICATO** | Crossref-ricerca | JMP 4(4):575-581. Uso (algebra finita => prodotto di esponenziali locale) supportato; globalita' per risolubili in PAMS 1964. |
| `WeiNorman1964` | Wei et al., *On global representations of the solutions of linear differential equa*, Proceedings of the AMS 15 (1964) | **VERIFICATO** | Crossref-ricerca | PAMS 15(2):327-334 ok; risultato di globalita' per algebre risolubili supportato. |
| `GonzalezLopezKamranOlver1994` | Gonz{\'a}lez-L{\'o}pez et al., *Quasi-exactly solvable {L}ie algebras of differential operators in two*, Comm. Math. Phys. / J. Phys. A  (1993) | **METADATI ERRATI** | Crossref-ricerca | Voce che fonde due lavori diversi (titolo con '/', due riviste, anno 1993 vs chiave 1994). Per la classificazione 1D citata nel REPORT: 'Normalizability of one-dimensional quasi-exactly solvable Schroedinger operators', Comm. Math. Phys. 153 (1993) 117-146, DOI 10.1007/BF02099042. L'altro: 'Quasi-exactly solvable Lie algebras of differential operators in two complex variables', J. Phys. A 24 (1991) 3995-4008, DOI 10.1088/0305-4470/24/17/016. |
| `IserlesKropielnicka2024` | Iserles et al., *An elementary approach to splittings of unbounded operators*,   (2024) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `HeZhaoZhong2024` | He et al., *(identificazione PDE via log-simbolo, segnalato da R8)*, Foundations of Computational Mathematics 24 (2024) | **METADATI ERRATI** | - | Titolo segnaposto '(identificazione PDE via log-simbolo...)', mancano numero/pagine/DOI. Corretto: 'How Much Can One Learn a Partial Differential Equation from Its Solution?', Found. Comput. Math. 24(5):1595-1641 (2024), DOI 10.1007/s10208-023-09620-z, arXiv:2204.04602. |
| `EfendievVabishchevich2020` | Efendiev et al., *(split additivo della soluzione, segnalato da R8)*,   (2020) | **METADATI ERRATI** | - | Titolo segnaposto. Corretto: 'Splitting methods for solution decomposition in nonstationary problems', arXiv:2008.08111; pubblicato in Appl. Math. Comput. 397 (2021) 125785, DOI 10.1016/j.amc.2020.125785. |

### R6

Conteggi: METADATI ERRATI 1, VERIFICATO 25

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Higham2008` | Higham, *Functions of Matrices: Theory and Computation*, SIAM  (2008) | **VERIFICATO** | Crossref-ricerca | Thm 1.12 = equivalenza delle definizioni (Jordan/interpolazione/Cauchy) confermata da fonte secondaria (Higham-Al-Mohy 2010). Def. 1.2/1.4 coerenti con TOC §1.2.1-1.2.2. |
| `GLR2009` | Gohberg et al., *Matrix Polynomials*, SIAM (Classics in Applied Mathematics 58  (2009) | **VERIFICATO** | Crossref-ricerca |  |
| `Gantmacher1959` | Gantmacher, *The Theory of Matrices*, Chelsea 1 (1959) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Biometrika). |
| `Jacobson1943` | Jacobson, *The Theory of Rings*, AMS  (1943) | **VERIFICATO** | Crossref-ricerca |  |
| `Cohn1985` | Cohn, *Free Rings and Their Relations*, Academic Press  (1985) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `Ore1933` | Ore, *Theory of non-commutative polynomials*, Annals of Mathematics 34 (1933) | **VERIFICATO** | Crossref-ricerca |  |
| `Katz1987` | Katz, *A simple algorithm for cyclic vectors*, American Journal of Mathematics 109 (1987) | **VERIFICATO** | Crossref-ricerca |  |
| `Coutinho1995` | Coutinho, *A Primer of Algebraic D-modules*, Cambridge University Press  (1995) | **VERIFICATO** | Crossref-ricerca |  |
| `vdPutSinger2003` | van der Put et al., *Galois Theory of Linear Differential Equations*, Springer  (2003) | **VERIFICATO** | Crossref-ricerca |  |
| `Stafford1978` | Stafford, *Module structure of Weyl algebras*, J. London Math. Soc. (2) 18 (1978) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref: Journal of the London Mathematical Society s2-18 429-442 1978 DOI 10.1112/jlms/s2-18.3.429. |
| `Singer1996` | Singer, *Testing reducibility of linear differential operators: a group theoret*, AAECC 7 (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `BasicModuleOre2013` | , *Basic Module Theory over Non-Commutative Rings with Computational Aspe*,   (2013) | **METADATI ERRATI** | Crossref-ricerca+arXiv | Autore mancante. Corretto: Gomez-Torrecillas, J., in Algebraic and Algorithmic Aspects of Differential and Integral Operators, LNCS 8372, Springer 2014, pp. 23-82, DOI 10.1007/978-3-642-54479-8_2 (arXiv:1312.7096). |
| `Olver1993` | Olver, *Applications of Lie Groups to Differential Equations*, Springer  (1993) | **VERIFICATO** | Crossref-ricerca |  |
| `Lim2005` | Lim, *Singular values and eigenvalues of tensors: a variational approach*, Proc. IEEE CAMSAP 2005  (2005) | **VERIFICATO** | Crossref-ricerca |  |
| `Qi2005` | Qi, *Eigenvalues of a real supersymmetric tensor*, J. Symbolic Computation 40 (2005) | **VERIFICATO** | Crossref-ricerca |  |
| `QiLuo2017` | Qi et al., *Tensor Analysis: Spectral Theory and Special Tensors*, SIAM  (2017) | **VERIFICATO** | Crossref-ricerca |  |
| `CartwrightSturmfels2013` | Cartwright et al., *The number of eigenvalues of a tensor*, Linear Algebra Appl. 438 (2013) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Robeva2016` | Robeva, *Orthogonal decomposition of symmetric tensors*, SIAM J. Matrix Anal. Appl. 37 (2016) | **VERIFICATO** | Crossref-ricerca+arXiv | Equazioni odeco e Thm 3.6 (congettura dell'ideale primo provata per n=2) riscontrati su arXiv:1409.6685: l'uso in R6-T7(ii) e' supportato. |
| `BDHR2017` | Boralevi et al., *Orthogonal and unitary tensor decomposition from an algebraic perspect*, Israel J. Math. 222 (2017) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `DeLathauwer2000` | De Lathauwer et al., *A multilinear singular value decomposition*, SIAM J. Matrix Anal. Appl. 21 (2000) | **VERIFICATO** | Crossref-ricerca |  |
| `HillarLim2013` | Hillar et al., *Most tensor problems are NP-hard*, J. ACM 60 (2013) | **VERIFICATO** | Crossref-ricerca |  |
| `IarrobinoKanev1999` | Iarrobino et al., *Power Sums, Gorenstein Algebras, and Determinantal Loci*, Springer  (1999) | **VERIFICATO** | Crossref-ricerca |  |
| `MMMM2006` | Mackey et al., *Vector spaces of linearizations for matrix polynomials*, SIAM J. Matrix Anal. Appl. 28 (2006) | **VERIFICATO** | Crossref-ricerca |  |
| `Kato1995` | Kato, *Perturbation Theory for Linear Operators*, Springer (Classics)  (1995) | **VERIFICATO** | Crossref-ricerca |  |
| `HormanderIII` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators III*, Springer  (1985) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Classics in Mathematics). |
| `CourantHilbertII` | Courant et al., *Methods of Mathematical Physics, Vol. II*, Interscience  (1962) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |

### R7

Conteggi: VERIFICATO 39, VERIFICATO-K 9

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Olver1993` | Olver, *Applications of Lie Groups to Differential Equations*, Springer  (1993) | **VERIFICATO** | Crossref-ricerca |  |
| `Ovsiannikov1982` | Ovsiannikov, *Group Analysis of Differential Equations*, Academic Press  (1982) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Ibragimov1994` | Ibragimov, *CRC Handbook of Lie Group Analysis of Differential Equations, Vol. 1*, CRC Press  (1994) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2024). |
| `Vilenkin1968` | Vilenkin, *Special Functions and the Theory of Group Representations*, AMS  (1968) | **VERIFICATO** | Crossref-ricerca |  |
| `VilenkinKlimyk1991` | Vilenkin et al., *Representation of Lie Groups and Special Functions, Vol. 1*, Kluwer  (1991) | **VERIFICATO** | Crossref-ricerca |  |
| `Miller1968` | Miller, *Lie Theory and Special Functions*, Academic Press  (1968) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Miller1977` | Miller, *Symmetry and Separation of Variables*, Addison-Wesley  (1977) | **VERIFICATO** | Crossref-ricerca | Cap. 1 Helmholtz, Cap. 2 Schroedinger e calore (TOC verificata): uso supportato. Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1984). |
| `RosenbloomWidder1959` | Rosenbloom et al., *Expansions in terms of heat polynomials and associated functions*, Trans. AMS 92 (1959) | **VERIFICATO** | Crossref-ricerca |  |
| `Folland1989` | Folland, *Harmonic Analysis in Phase Space*, Princeton Univ. Press  (1989) | **VERIFICATO** | Crossref-ricerca |  |
| `ReedSimon1` | Reed et al., *Methods of Modern Mathematical Physics I: Functional Analysis*, Academic Press  (1980) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `Rudin1991` | Rudin, *Functional Analysis*, McGraw-Hill  (1991) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Schmudgen2012` | Schm{\"u}dgen, *Unbounded Self-adjoint Operators on Hilbert Space*, Springer  (2012) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `DunfordSchwartz1` | Dunford et al., *Linear Operators, Part I*, Interscience  (1958) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Gian-Carlo Rota on Analysis and Probability). |
| `Higham2008` | Higham, *Functions of Matrices: Theory and Computation*, SIAM  (2008) | **VERIFICATO** | Crossref-ricerca | Vedi R6. |
| `HornJohnson2013` | Horn et al., *Matrix Analysis*, Cambridge Univ. Press  (2013) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2012). |
| `GelfandVilenkin4` | Gel'fand et al., *Generalized Functions, Vol. 4*, Academic Press  (1964) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2016). |
| `Hormander2` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators II*, Springer  (1983) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `Bjork1979` | Bj{\"o}rk, *Rings of Differential Operators*, North-Holland  (1979) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `WeiNorman1963` | Wei et al., *Lie algebraic solution of linear differential equations*, J. Math. Phys. 4 (1963) | **VERIFICATO** | Crossref-ricerca |  |
| `WeiNorman1964` | Wei et al., *On global representations of the solutions of linear differential equa*, Proc. AMS 15 (1964) | **VERIFICATO** | Crossref-ricerca |  |
| `Hopf1950` | Hopf, *The partial differential equation u_t + u u_x = mu u_xx*, Comm. Pure Appl. Math. 3 (1950) | **VERIFICATO** | Crossref-ricerca |  |
| `Cole1951` | Cole, *On a quasi-linear parabolic equation occurring in aerodynamics*, Quart. Appl. Math. 9 (1951) | **VERIFICATO** | Crossref-ricerca |  |
| `Lax1968` | Lax, *Integrals of nonlinear equations of evolution and solitary waves*, Comm. Pure Appl. Math. 21 (1968) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref:  None None 1968 DOI 10.2172/4522657. |
| `GGKM1967` | Gardner et al., *Method for solving the Korteweg-de Vries equation*, Phys. Rev. Lett. 19 (1967) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `AKNS1974` | Ablowitz et al., *The inverse scattering transform -- Fourier analysis for nonlinear pro*, Stud. Appl. Math. 53 (1974) | **VERIFICATO** | Crossref-ricerca |  |
| `AblowitzSegur1981` | Ablowitz et al., *Solitons and the Inverse Scattering Transform*, SIAM  (1981) | **VERIFICATO** | Crossref-ricerca |  |
| `AblowitzClarkson1991` | Ablowitz et al., *Solitons, Nonlinear Evolution Equations and Inverse Scattering*, Cambridge Univ. Press  (1991) | **VERIFICATO** | Crossref-ricerca |  |
| `DrazinJohnson1989` | Drazin et al., *Solitons: An Introduction*, Cambridge Univ. Press  (1989) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Physics Today). |
| `Hirota1971` | Hirota, *Exact solution of the Korteweg-de Vries equation for multiple collisio*, Phys. Rev. Lett. 27 (1971) | **VERIFICATO** | Crossref-ricerca |  |
| `Hirota2004` | Hirota, *The Direct Method in Soliton Theory*, Cambridge Univ. Press  (2004) | **VERIFICATO** | Crossref-ricerca |  |
| `Miura1968` | Miura, *Korteweg-de Vries equation and generalizations. I. A remarkable explic*, J. Math. Phys. 9 (1968) | **VERIFICATO** | Crossref-ricerca |  |
| `WahlquistEstabrook1973` | Wahlquist et al., *Backlund transformation for solutions of the Korteweg-de Vries equatio*, Phys. Rev. Lett. 31 (1973) | **VERIFICATO** | Crossref-ricerca |  |
| `RogersSchief2002` | Rogers et al., *B{\"a}cklund and Darboux Transformations*, Cambridge Univ. Press  (2002) | **VERIFICATO** | Crossref-ricerca |  |
| `Koopman1931` | Koopman, *Hamiltonian systems and transformation in Hilbert space*, PNAS 17 (1931) | **VERIFICATO** | Crossref-ricerca |  |
| `Mezic2005` | Mezi{\'c}, *Spectral properties of dynamical systems, model reduction and decompos*, Nonlinear Dynamics 41 (2005) | **VERIFICATO** | Crossref-ricerca |  |
| `BudisicMohrMezic2012` | Budi{\v s}i{\'c} et al., *Applied Koopmanism*, Chaos 22 (2012) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `LanMezic2013` | Lan et al., *Linearization in the large of nonlinear systems and Koopman operator s*, Physica D 242 (2013) | **VERIFICATO** | Crossref-ricerca |  |
| `MauroyMezicSusuki2020` | Mauroy et al., *The Koopman Operator in Systems and Control*, Springer  (2020) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `PageKerswell2018` | Page et al., *Koopman analysis of Burgers equation*, Phys. Rev. Fluids 3 (2018) | **VERIFICATO** | Crossref-ricerca |  |
| `Carleman1932` | Carleman, *Application de la th{\'e}orie des {\'e}quations int{\'e}grales lin{\'e*, Acta Math. 59 (1932) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `KowalskiSteeb1991` | Kowalski et al., *Nonlinear Dynamical Systems and Carleman Linearization*, World Scientific  (1991) | **VERIFICATO** | Crossref-ricerca |  |
| `ForetsPouly2017` | Forets et al., *Explicit error bounds for Carleman linearization*,   (2017) | **VERIFICATO** | arXiv |  |
| `Liu2021` | Liu et al., *Efficient quantum algorithm for dissipative nonlinear differential equ*, PNAS 118 (2021) | **VERIFICATO** | Crossref-ricerca |  |
| `Rudy2017` | Rudy et al., *Data-driven discovery of partial differential equations*, Science Advances 3 (2017) | **VERIFICATO** | Crossref-ricerca |  |
| `Brunton2016` | Brunton et al., *Discovering governing equations from data by sparse identification of *, PNAS 113 (2016) | **VERIFICATO** | Crossref-ricerca |  |
| `KolokoltsovMaslov1997` | Kolokoltsov et al., *Idempotent Analysis and Its Applications*, Kluwer  (1997) | **VERIFICATO** | Crossref-ricerca |  |
| `Tokihiro1996` | Tokihiro et al., *From soliton equations to integrable cellular automata through a limit*, Phys. Rev. Lett. 76 (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `Robeva2016` | Robeva, *Orthogonal decomposition of symmetric tensors*, SIAM J. Matrix Anal. Appl. 37 (2016) | **VERIFICATO** | Crossref-ricerca | Vedi R6: supportato. |

### R8

Conteggi: CONTESTO NON SUPPORTATO 1, METADATI ERRATI 3, VERIFICATO 45, VERIFICATO-K 14

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Scholl2026Identifiability` | Scholl et al., *Symbolic Recovery of Differential Equations: The Identifiability Probl*, Machine Learning 115 (2026) | **VERIFICATO** | DOI/Crossref+arXiv | Metadati rivista confermati su Crossref (vol 115, n. 6, art. 139). Prop.1, Cor.1, Prop.6, 7, 8, 10 riscontrati su arXiv v10: supportano gli usi in R8 §(i)/(iii). |
| `Hauger2024Robust` | Hauger et al., *Robust identifiability for symbolic recovery of differential equations*,   (2024) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `HeZhaoZhong2024` | He et al., *How Much Can One Learn a Partial Differential Equation from Its Soluti*, Foundations of Computational Mathematics 24 (2024) | **CONTESTO NON SUPPORTATO** | DOI/Crossref+arXiv | Metadati OK. Contesto: R8 usa Thm 3.2 per dichiarare 'G4 (parte evolutiva) NOTO' dove G4 (NOTAZIONE) e' un 'sse' (/supp u0^/ >= deg a + 1). Thm 3.2 (letto su arXiv v2) e' solo SUFFICIENTE, su T^d, con dati a due istanti vicini, soglia combinatoria su /Q/ e condizione 'Q non su ipersuperficie algebrica di grado <= n (solo termini pari o solo dispari)'. Supporta la direzione <= sotto ipotesi piu' forti, non l'equivalenza. Thm 3.4/3.5: supportati. |
| `ZhaoZhong2023` | Zhao et al., *How much can one learn from a single solution of a {PDE}?*, Pure and Applied Functional Analysis 8 (2023) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Stanhope2014` | Stanhope et al., *Identifiability of Linear and Linear-in-Parameters Dynamical Systems f*, SIAM Journal on Applied Dynamical System 13 (2014) | **VERIFICATO** | Crossref-ricerca | Pagine 1792-1815 confermate (nota 'UNVERIFIED pages' risolta); aggiungere doi 10.1137/130937913. |
| `Qiu2022` | Qiu et al., *Identifiability analysis of linear ordinary differential equation syst*, Applied Mathematics and Computation  (2022) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Casolo2025Sparse` | Casolo et al., *Identifiability Challenges in Sparse Linear Ordinary Differential Equa*,   (2025) | **VERIFICATO** | arXiv |  |
| `PanBolcskei2026` | Pan et al., *Recovering Governing Equations from Solution Data: Identifiability Bou*,   (2026) | **VERIFICATO** | arXiv |  |
| `Brunton2016SINDy` | Brunton et al., *Discovering governing equations from data by sparse identification of *, Proceedings of the National Academy of S 113 (2016) | **VERIFICATO** | DOI/Crossref |  |
| `Rudy2017PDEFIND` | Rudy et al., *Data-driven discovery of partial differential equations*, Science Advances 3 (2017) | **VERIFICATO** | DOI/Crossref |  |
| `Schaeffer2017` | Schaeffer, *Learning partial differential equations via data discovery and sparse *, Proceedings of the Royal Society A 473 (2017) | **VERIFICATO** | DOI/Crossref |  |
| `MessengerBortz2021PDE` | Messenger et al., *Weak {SINDy} for partial differential equations*, Journal of Computational Physics 443 (2021) | **VERIFICATO** | DOI/Crossref+arXiv |  |
| `MessengerBortz2021ODE` | Messenger et al., *Weak {SINDy}: Galerkin-Based Data-Driven Model Selection*, Multiscale Modeling \& Simulation 19 (2021) | **VERIFICATO** | DOI/Crossref |  |
| `PeherstorferWillcox2016` | Peherstorfer et al., *Data-driven operator inference for nonintrusive projection-based model*, Computer Methods in Applied Mechanics an 306 (2016) | **VERIFICATO** | DOI/Crossref |  |
| `SchmidtLipson2009` | Schmidt et al., *Distilling Free-Form Natural Laws from Experimental Data*, Science 324 (2009) | **VERIFICATO** | DOI/Crossref |  |
| `UdrescuTegmark2020` | Udrescu et al., *{AI Feynman}: A physics-inspired method for symbolic regression*, Science Advances 6 (2020) | **VERIFICATO** | DOI/Crossref |  |
| `Cranmer2023PySR` | Cranmer, *Interpretable Machine Learning for Science with {PySR} and {SymbolicRe*,   (2023) | **VERIFICATO** | arXiv |  |
| `Long2018PDENet` | Long et al., *{PDE-Net}: Learning {PDE}s from Data*, Proceedings of the 35th International Co  (2018) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Harkonen2023EPGP` | H{\"a}rk{\"o}nen et al., *Gaussian Process Priors for Systems of Linear Partial Differential Equ*, Proceedings of the 40th International Co  (2023) | **VERIFICATO** | arXiv |  |
| `Huang2024BEPGP` | Huang et al., *Gaussian Process Priors for Boundary Value Problems of Linear Partial *,   (2024) | **VERIFICATO** | arXiv |  |
| `Li2025GPInverse` | Li et al., *Gaussian Process Regression for Inverse Problems in Linear {PDE}s*,   (2025) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `AitElManssour2021` | Ait El Manssour et al., *Linear {PDE} with Constant Coefficients*,   (2021) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `SattelbergerSturmfels2019` | Sattelberger et al., *D-Modules and Holonomic Functions*,   (2019) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Kauers2009Guessing` | Kauers, *Guessing Handbook*,   (2009) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `KauersJaroschekJohansson2015` | Kauers et al., *Ore Polynomials in Sage*, Computer Algebra and Polynomials 8942 (2015) | **VERIFICATO** | DOI/Crossref |  |
| `SalvyZimmermann1994` | Salvy et al., *{GFUN}: a {Maple} package for the manipulation of generating and holon*, ACM Transactions on Mathematical Softwar 20 (1994) | **VERIFICATO** | Crossref-ricerca |  |
| `BeckermannLabahn1994` | Beckermann et al., *A uniform approach for the fast computation of matrix-type {Pad\'e} ap*, SIAM Journal on Matrix Analysis and Appl 15 (1994) | **VERIFICATO** | Crossref-ricerca |  |
| `KauersPaule2011` | Kauers et al., *The Concrete Tetrahedron*, Springer  (2011) | **VERIFICATO** | Crossref-ricerca |  |
| `Prony1795` | de Prony, *Essai exp{\'e}rimental et analytique*, Journal de l'{\'E}cole Polytechnique 1 (1795) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Vetterli2002FRI` | Vetterli et al., *Sampling signals with finite rate of innovation*, IEEE Transactions on Signal Processing 50 (2002) | **VERIFICATO** | Crossref-ricerca |  |
| `PeterPlonka2013` | Peter et al., *A generalized {Prony} method for reconstruction of sparse sums of eige*, Inverse Problems 29 (2013) | **VERIFICATO** | Crossref-ricerca |  |
| `Kunis2016Prony` | Kunis et al., *A multivariate generalization of {Prony}'s method*, Linear Algebra and its Applications 499 (2016) | **METADATI ERRATI** | Crossref-ricerca | Volume/pagine errati (499:191-212). Corretto: Linear Algebra Appl. 490 (2016) 31-47, DOI 10.1016/j.laa.2015.10.023 (R4 e SCOUT-2 gia' corretti). |
| `Mourrain2018` | Mourrain, *Polynomial-exponential decomposition from moments*, Foundations of Computational Mathematics 18 (2018) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `RapisardaAntoulas2016` | Rapisarda et al., *Bilinear differential forms and the Loewner framework for rational int*, SIAM Journal on Control and Optimization  (2016) | **METADATI ERRATI** | Crossref-ricerca | Titolo errato (fusione con 'Bilinear differential forms and the Loewner framework...', LNCIS 2015). Corretto: 'State-Space Modeling of Two-Dimensional Vector-Exponential Trajectories', SIAM J. Control Optim. 54(5):2734-2753 (2016), DOI 10.1137/15M1031837 (SCOUT-2 gia' corretto). |
| `Willems1986` | Willems, *From time series to linear system, Part I--III*, Automatica 22 (1986) | **METADATI ERRATI** | Crossref-ricerca | Parti I-II: Automatica 22(5):561-580 e 22(6):675-694 (1986); Parte III: Automatica 23(1):87-115 (1987), DOI 10.1016/0005-1098(87)90120-8. La voce attribuisce I-III al vol. 22/1986. |
| `Willems2005Lemma` | Willems et al., *A note on persistency of excitation*, Systems \& Control Letters 54 (2005) | **VERIFICATO** | Crossref-ricerca |  |
| `Oberst1990` | Oberst, *Multidimensional constant linear systems*, Acta Applicandae Mathematicae 20 (1990) | **VERIFICATO** | Crossref-ricerca |  |
| `EfendievVabishchevich2020` | Efendiev et al., *Splitting methods for solution decomposition in nonstationary problems*,   (2020) | **VERIFICATO** | Crossref-ricerca+arXiv | Pubblicato: Appl. Math. Comput. 397 (2021) 125785, DOI 10.1016/j.amc.2020.125785 (aggiornare). |
| `Vabishchevich2011` | Vabishchevich, *Additive schemes (splitting schemes) for some systems of evolutionary *,   (2011) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `StarckEladDonoho2005` | Starck et al., *Image decomposition via the combination of sparse representations and *, IEEE Transactions on Image Processing 14 (2005) | **VERIFICATO** | Crossref-ricerca |  |
| `DonohoKutyniok2013` | Donoho et al., *Microlocal analysis of the geometric separation problem*, Communications on Pure and Applied Mathe 66 (2013) | **VERIFICATO** | Crossref-ricerca |  |
| `Doll2025Schwartz` | Doll, *Formalizing Schwartz functions and tempered distributions*,   (2025) | **VERIFICATO** | arXiv |  |
| `Mathlib2026` | {The mathlib Community}, *mathlib4 (master branch)*,   (2026) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `OreAlgebraRepo` | Kauers et al., *ore\_algebra (SageMath package)*,   (2026) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Hormander1983II` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators II*, Springer  (1983) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: The American Mathematical Monthly). |
| `Bjork1979` | Bj{\"o}rk, *Rings of Differential Operators*, North-Holland  (1979) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Borg1946` | Borg, *Eine Umkehrung der {Sturm--Liouvilleschen} Eigenwertaufgabe*, Acta Mathematica 78 (1946) | **VERIFICATO** | Crossref-ricerca |  |
| `GelfandLevitan1951` | Gel'fand et al., *On the determination of a differential equation from its spectral func*, Izvestiya Akad. Nauk SSSR Ser. Mat. 15 (1951) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Marchenko1977` | Marchenko, *Sturm--Liouville Operators and Their Applications*, Naukova Dumka (Engl. transl. Birkh{\"a}u  (1977) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 2011). |
| `HochstadtLieberman1978` | Hochstadt et al., *An inverse {Sturm--Liouville} problem with mixed given data*, SIAM Journal on Applied Mathematics 34 (1978) | **VERIFICATO** | Crossref-ricerca |  |
| `PoschelTrubowitz1987` | P{\"o}schel et al., *Inverse Spectral Theory*, Academic Press  (1987) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `FreilingYurko2001` | Freiling et al., *Inverse {Sturm--Liouville} Problems and Their Applications*, Nova Science  (2001) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `GGKM1967` | Gardner et al., *Method for solving the {Korteweg--de Vries} equation*, Physical Review Letters 19 (1967) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `GasymovLevitan1966` | Gasymov et al., *The inverse problem for the {Dirac} system*, Doklady Akademii Nauk SSSR 167 (1966) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `ChelkakKorotyaev2009` | Chelkak et al., *Weyl--{Titchmarsh} functions of vector-valued {Sturm--Liouville} opera*, Journal of Functional Analysis 257 (2009) | **VERIFICATO** | Crossref-ricerca |  |
| `BrackxDelangheSommen1982` | Brackx et al., *Clifford Analysis*, Pitman  (1982) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `GilbertMurray1991` | Gilbert et al., *Clifford Algebras and {Dirac} Operators in Harmonic Analysis*, Cambridge University Press  (1991) | **VERIFICATO** | Crossref-ricerca |  |
| `Champion2019` | Champion et al., *Data-driven discovery of coordinates and governing equations*, Proceedings of the National Academy of S 116 (2019) | **VERIFICATO** | Crossref-ricerca |  |
| `Lusch2018` | Lusch et al., *Deep learning for universal linear embeddings of nonlinear dynamics*, Nature Communications 9 (2018) | **VERIFICATO** | Crossref-ricerca |  |
| `vanderMaaten2008` | van der Maaten et al., *Visualizing Data using t-{SNE}*, Journal of Machine Learning Research 9 (2008) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Dempster1977` | Dempster et al., *Maximum likelihood from incomplete data via the {EM} algorithm*, Journal of the Royal Statistical Society 39 (1977) | **VERIFICATO** | Crossref-ricerca |  |
| `Trotter1959` | Trotter, *On the product of semi-groups of operators*, Proceedings of the AMS 10 (1959) | **VERIFICATO** | Crossref-ricerca |  |
| `Strang1968` | Strang, *On the construction and comparison of difference schemes*, SIAM Journal on Numerical Analysis 5 (1968) | **VERIFICATO** | Crossref-ricerca |  |

### SCOUT-1

Conteggi: VERIFICATO 27, VERIFICATO-K 3

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `ArocaGarayToghani2016` | Aroca et al., *The Fundamental Theorem of Tropical Differential Algebraic Geometry*, Pacific J. Math. 283 (2016) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Grigoriev2017` | Grigoriev, *Tropical differential equations*, Adv. Appl. Math.  (2017) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Falkensteiner2020` | Falkensteiner et al., *The Fundamental Theorem of Tropical Partial Differential Algebraic Geo*,   (2020) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `GiansiracusaMereta2021` | Giansiracusa et al., *A general framework for tropical differential equations*,   (2021) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `GKZ1994` | Gelfand et al., *Discriminants, Resultants, and Multidimensional Determinants*, Birkh{\"a}user  (1994) | **VERIFICATO** | Crossref-ricerca |  |
| `PassareRullgard2004` | Passare et al., *Amoebas, Monge--Amp{\`e}re measures, and triangulations of the Newton *, Duke Math. J. 121 (2004) | **VERIFICATO** | Crossref-ricerca |  |
| `Bruno2000` | Bruno, *Power Geometry in Algebraic and Differential Equations*, Elsevier  (2000) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Singer1996` | Singer, *Testing reducibility of linear differential operators: a group theoret*, Appl. Algebra Engrg. Comm. Comput. 7 (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `vanHoeij1996` | van Hoeij, *Rational solutions of the mixed differential equation and its applicat*, Proc. ISSAC 1996  (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `vanderPutSinger2003` | van der Put et al., *Galois Theory of Linear Differential Equations*, Springer 328 (2003) | **VERIFICATO** | Crossref-ricerca |  |
| `CassidySinger2007` | Cassidy et al., *Galois theory of parameterized differential equations and linear diffe*, IRMA Lect. Math. Theor. Phys. 9 (2007) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref: IRMA Lectures in Mathematics and Theoretical Physics None 113-155 2006 DOI 10.4171/020-1/7. |
| `Ore1933` | Ore, *Theory of non-commutative polynomials*, Ann. of Math. 34 (1933) | **VERIFICATO** | Crossref-ricerca |  |
| `Oberst1990` | Oberst, *Multidimensional constant linear systems*, Acta Appl. Math. 20 (1990) | **VERIFICATO** | Crossref-ricerca |  |
| `Katz1996` | Katz, *Rigid Local Systems*, Princeton Univ. Press 139 (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `CrawleyBoevey2003` | Crawley-Boevey, *On matrices in prescribed conjugacy classes with no common invariant s*, Duke Math. J. 118 (2003) | **VERIFICATO** | Crossref-ricerca | Duke 118(2):339-352, DOI 10.1215/S0012-7094-03-11825-6. Abstract: tuple di classi di coniugio con somma zero senza sottospazio invariante comune, risposta via sistema di radici di Kac-Moody: supportato. |
| `Oshima2012` | Oshima, *Fractional Calculus of Weyl Algebra and Fuchsian Differential Equation*, Math. Soc. Japan 28 (2012) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `Boalch2008` | Boalch, *Irregular connections and Kac--Moody root systems*,   (2008) | **VERIFICATO** | arXiv |  |
| `Turrittin1955` | Turrittin, *Convergent solutions of ordinary linear homogeneous differential equat*, Acta Math. 93 (1955) | **VERIFICATO** | Crossref-ricerca |  |
| `MalgrangeRamis1992` | Malgrange et al., *Fonctions multisommables*, Ann. Inst. Fourier 42 (1992) | **VERIFICATO** | Crossref-ricerca |  |
| `Balser2000` | Balser, *Formal Power Series and Linear Systems of Meromorphic Ordinary Differe*, Springer  (2000) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `KashiwaraSchapira1990` | Kashiwara et al., *Sheaves on Manifolds*, Springer 292 (1990) | **VERIFICATO** | Crossref-ricerca |  |
| `Taylor1981` | Taylor, *Pseudodifferential Operators*, Princeton Univ. Press  (1981) | **VERIFICATO** | Crossref-ricerca |  |
| `HormanderIII` | H{\"o}rmander, *The Analysis of Linear Partial Differential Operators III*, Springer  (1985) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: Classics in Mathematics). |
| `IarrobinoKanev1999` | Iarrobino et al., *Power Sums, Gorenstein Algebras, and Determinantal Loci*, Springer 1721 (1999) | **VERIFICATO** | Crossref-ricerca |  |
| `KungRota1984` | Kung et al., *The invariant theory of binary forms*, Bull. Amer. Math. Soc. 10 (1984) | **VERIFICATO** | Crossref-ricerca |  |
| `Rota1964` | Rota, *On the foundations of combinatorial theory I. Theory of M{\"o}bius fun*, Z. Wahrscheinlichkeitstheorie verw. Gebi 2 (1964) | **VERIFICATO** | Crossref-ricerca |  |
| `Speicher1994` | Speicher, *Multiplicative functions on the lattice of non-crossing partitions and*, Math. Ann. 298 (1994) | **VERIFICATO** | Crossref-ricerca |  |
| `Hoeffding1948` | Hoeffding, *A class of statistics with asymptotically normal distribution*, Ann. Math. Statist. 19 (1948) | **VERIFICATO** | Crossref-ricerca |  |
| `WeiNorman1963` | Wei et al., *Lie algebraic solution of linear differential equations*, J. Math. Phys. 4 (1963) | **VERIFICATO** | Crossref-ricerca |  |
| `WeiNorman1964` | Wei et al., *On global representations of the solutions of linear differential equa*, Proc. Amer. Math. Soc. 15 (1964) | **VERIFICATO** | Crossref-ricerca |  |

### SCOUT-2

Conteggi: VERIFICATO 28, VERIFICATO-K 1

| chiave | voce | esito | fonte controllo | nota / correzione |
|---|---|---|---|---|
| `Faddeev1961` | Faddeev, *Scattering theory for a three-particle system*, Soviet Physics JETP 12 (1961) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref: Fifty Years of Mathematical Physics None 37-42 2016 DOI 10.1142/9789814340960_0004. |
| `Watson1953` | Watson, *Multiple scattering and the many-body problem---applications to photom*, Physical Review 89 (1953) | **VERIFICATO** | Crossref-ricerca |  |
| `LippmannSchwinger1950` | Lippmann et al., *Variational principles for scattering processes. I*, Physical Review 79 (1950) | **VERIFICATO** | Crossref-ricerca |  |
| `GellMannGoldberger1953` | Gell-Mann et al., *The formal theory of scattering*, Physical Review 91 (1953) | **VERIFICATO** | Crossref-ricerca |  |
| `FaddeevYakubovsky2019` | , *The Faddeev-Yakubovsky symphony*,   (2019) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `DonohoKutyniok2013` | Donoho et al., *Microlocal analysis of the geometric separation problem*, Communications on Pure and Applied Mathe 66 (2013) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Kutyniok2012` | Kutyniok, *Geometric separation by single-pass alternating thresholding*,   (2012) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `Cohen1989` | Cohen, *Time-frequency distributions---a review*, Proceedings of the IEEE 77 (1989) | **VERIFICATO** | Crossref-ricerca |  |
| `HlawatschFlandrin1997` | Hlawatsch et al., *The interference structure of the Wigner distribution and related time*, The Wigner Distribution: Theory and Appl  (1997) | **VERIFICATO-K** | - | Non indicizzato su Crossref (manuale/serie storica/web): riconosciuto come esistente, metadati plausibili, non riscontrati via API. |
| `StarckEladDonoho2005` | Starck et al., *Image decomposition via the combination of sparse representations and *, IEEE Transactions on Image Processing 14 (2005) | **VERIFICATO** | Crossref-ricerca |  |
| `EladBruckstein2002` | Elad et al., *A generalized uncertainty principle and sparse representation in pairs*, IEEE Transactions on Information Theory 48 (2002) | **VERIFICATO** | Crossref-ricerca |  |
| `BenderOrszag1978` | Bender et al., *Advanced Mathematical Methods for Scientists and Engineers*, McGraw-Hill  (1978) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata (Crossref restituisce ristampa/recensione: ristampa 1999). |
| `ChenGoldenfeldOono1996` | Chen et al., *Renormalization group and singular perturbations: multiple scales, bou*, Physical Review E 54 (1996) | **VERIFICATO** | Crossref-ricerca |  |
| `Willems1986` | Willems, *From time series to linear system---Part I, II*, Automatica 22 (1986) | **VERIFICATO** | Crossref-ricerca | Esistenza confermata; Crossref: Automatica 23 87-115 1987 DOI 10.1016/0005-1098(87)90120-8. |
| `WillemsRapisardaMarkovskyDeMoor2005` | Willems et al., *A note on persistency of excitation*, Systems \& Control Letters 54 (2005) | **VERIFICATO** | Crossref-ricerca |  |
| `RapisardaAntoulas2016` | Rapisarda et al., *State-space modeling of two-dimensional vector-exponential trajectorie*, SIAM Journal on Control and Optimization  (2016) | **VERIFICATO** | DOI/Crossref | Titolo/rivista/DOI confermati: SICON 54(5):2734-2753. MPUM per traiettorie esponenziali in due variabili: supportato dall'abstract. |
| `Oberst1990` | Oberst, *Multidimensional constant linear systems*, Acta Applicandae Mathematicae 20 (1990) | **VERIFICATO** | Crossref-ricerca |  |
| `HoKalman1966` | Ho et al., *Effective construction of linear state-variable models from input/outp*, Regelungstechnik 14 (1966) | **VERIFICATO** | Crossref-ricerca |  |
| `Roesser1975` | Roesser, *A discrete state-space model for linear image processing*, IEEE Transactions on Automatic Control 20 (1975) | **VERIFICATO** | Crossref-ricerca |  |
| `Mori1965` | Mori, *Transport, collective motion, and Brownian motion*, Progress of Theoretical Physics 33 (1965) | **VERIFICATO** | Crossref-ricerca |  |
| `Zwanzig1961` | Zwanzig, *Memory effects in irreversible thermodynamics*, Physical Review 124 (1961) | **VERIFICATO** | Crossref-ricerca |  |
| `ChorinHaldKupferman2002` | Chorin et al., *Optimal prediction with memory*, Physica D 166 (2002) | **VERIFICATO** | Crossref-ricerca |  |
| `Mourrain2018` | Mourrain, *Polynomial-exponential decomposition from moments*, Foundations of Computational Mathematics 18 (2018) | **VERIFICATO** | Crossref-ricerca+arXiv |  |
| `KunisPeterRoemerVonDerOhe2016` | Kunis et al., *A multivariate generalization of Prony's method*, Linear Algebra and its Applications 490 (2016) | **VERIFICATO** | Crossref-ricerca |  |
| `OwhadiScovel2019` | Owhadi et al., *Operator-Adapted Wavelets, Fast Solvers, and Numerical Homogenization*, Cambridge University Press  (2019) | **VERIFICATO** | Crossref-ricerca |  |
| `XuLiuTongKailath1995` | Xu et al., *A least-squares approach to blind channel identification*, IEEE Transactions on Signal Processing 43 (1995) | **VERIFICATO** | Crossref-ricerca |  |
| `Hoeffding1948` | Hoeffding, *A class of statistics with asymptotically normal distribution*, Annals of Mathematical Statistics 19 (1948) | **VERIFICATO** | Crossref-ricerca |  |
| `Tu2014DMD` | Tu et al., *On dynamic mode decomposition: theory and applications*, Journal of Computational Dynamics 1 (2014) | **VERIFICATO** | Crossref-ricerca |  |
| `Kato1995` | Kato, *Perturbation Theory for Linear Operators*, Springer  (1995) | **VERIFICATO** | Crossref-ricerca |  |