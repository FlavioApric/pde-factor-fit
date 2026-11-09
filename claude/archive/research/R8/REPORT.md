# REPORT — R8 · Prior art e strumenti (Fase 1)

Agente R8 · 2026-10-22 · PLAN: `research/R8/PLAN.md` · bib: `research/R8/sources.bib` · domande aperte: `research/R8/open_questions.md`

**Skill caricate (Regola 2), tutte per lettura del SKILL.md (nessuno script vendor eseguito):**
`academic-research-skills\deep-research\SKILL.md` (workflow domanda → fonti → verifica → sintesi; il pipeline a 13 agenti NON è stato lanciato perché R8 è già un subagente: fasi eseguite a mano; `anthropic-skills:deep-research` non invocato per lo stesso motivo) · `ARIS\skills\research-lit\SKILL.md` + `arxiv`/`semantic-scholar`/`openalex` (query via WebSearch/WebFetch e GitHub code search, non con i fetcher Python) · `ARIS\skills\novelty-check\SKILL.md` (fasi A–D; revisore Codex escluso per decisione utente: le "verdict limits" sono applicate da R8, §2.3–2.5) · `scientific-agent-skills\skills\citation-management\SKILL.md` (metadati verificati su arXiv/editori ove possibile; campi non verificati marcati `UNVERIFIED` in `sources.bib`) · `scientific-agent-skills\skills\scientific-critical-thinking\SKILL.md` (avvocato del diavolo §2.5).

Legenda stato: **NOTO** (con fonte) · **APERTO** · **PROB. FALSO**. Mappatura su item C/P/II e congetture G1–G7 di `NOTAZIONE.md`.

---

## 1. Mappa del prior art (Q1)

| Famiglia | Lavoro chiave | Dato richiesto | Esatto / numerico | Identifica L? | Scompone u per termine? | Garanzie |
|---|---|---|---|---|---|---|
| SINDy | Brunton–Proctor–Kutz, PNAS 113 (2016) | traiettorie + derivate | numerico (STLSQ) | sì, in un dizionario | no | poche |
| PDE-FIND | Rudy–Brunton–Proctor–Kutz, Sci. Adv. 3 (2017); Schaeffer, Proc. R. Soc. A 473 (2017) | u(t,x) su griglia | numerico (ridge sparsa) | sì | no | nessuna identificabilità |
| Weak SINDy | Messenger–Bortz, JCP 443 (2021) 110525 | u + funzioni test | numerico, forma debole; precisione di macchina senza rumore | sì | no | robustezza al rumore |
| Operator inference | Peherstorfer–Willcox, CMAME 306 (2016) | snapshot | minimi quadrati su base POD | operatore ridotto | no | consistenza col ROM |
| Symbolic regression | Schmidt–Lipson, Science 324 (2009); AI Feynman (Udrescu–Tegmark, Sci. Adv. 6, 2020); PySR (Cranmer, arXiv:2305.01582); PDE-Net (Long et al., ICML 2018) | dati | ricerca / ML | sì (forma libera) | no | nessuna |
| Identificabilità simbolica | **Scholl–Bacho–Boche–Kutyniok** arXiv:2210.08342 (Machine Learning 115, 2026); Hauger–Scholl–Kutyniok arXiv:2410.09938 | una funzione u | teoria esatta + test numerici (FRanCo, JRC) | criterio | no | **CNS di unicità** (§2.1) |
| Identificabilità PDE, una traiettoria | **He–Zhao–Zhong**, FoCM 24 (2024) 1595–1641; Zhao–Zhong, PAFA 8 (2023) | u a 2 o m istanti, su 𝕋^d | teoria esatta + CaSLR | sì | no | **Thm 3.2, 3.4, 3.5** |
| ODE lineari (sistemi), una traiettoria | Stanhope–Rubin–Swigon SIADS 13 (2014); Qiu et al. (2022); Casolo–Becker–Kilbertus arXiv:2506.09816; Pan–Bölcskei arXiv:2606.27285 | una / molte traiettorie | teoria | x'=Ax | no | q.o. identificabile; sparsi falliscono |
| EPGP | Härkönen–Lange-Hegermann–Raiță ICML 2023 (arXiv:2212.14319); B-EPGP arXiv:2411.16663; Li–L-H–Raiță arXiv:2502.04276 | L noto / dati rumorosi | probabilistico (prior costruito esattamente in Macaulay2) | solo parametri (es. velocità d'onda) | no | posterior in ker L |
| Guessing D-finito | Kauers *Guessing handbook* (RISC 09-07, 2009); ore_algebra (Kauers–Jaroschek–Johansson, LNCS 8942, 2015); gfun (Salvy–Zimmermann, ACM TOMS 20, 1994); Hermite–Padé (Beckermann–Labahn SIMAX 15, 1994) | serie esatte | **esatto** | **sì: annullatore minimo** | no (solo chiusure) | certificabile |
| Prony / FRI | Prony 1795; Vetterli–Marziliano–Blu IEEE TSP 50 (2002); Peter–Plonka Inverse Problems 29 (2013) 025001; Kunis–Peter–Römer–von der Ohe LAA 499 (2016); Mourrain FoCM 18 (2018) | campioni di somme esponenziali / autofunzioni | **esatto** (Hankel) | sì (filtro annullante) | **sì ma per MODI, non per termini** | rango di Hankel |
| MPUM / behaviours (via SCOUT-2) | Willems 1986; Willems–Rapisarda–Markovsky–De Moor 2005; Rapisarda–Antoulas SICON 2016 | traiettorie esp.-polinomiali, anche 2-D | esatto | sì (ker dell'annullatore minimo) | no | persistenza di eccitazione |
| Split additivo della soluzione | Efendiev–Vabishchevich arXiv:2008.08111; Vabishchevich arXiv:1112.1294 | L noto | numerico | no | **sì, come schema numerico** | stabilità |
| Separazione di componenti | Starck–Elad–Donoho (MCA) IEEE TIP 14 (2005); Donoho–Kutyniok CPAM 66 (2013) (R1) | u, dizionari noti | ℓ¹ | no | sì, per dizionari | coerenza a cluster |

**Lettura.** La linea SINDy/PDE-FIND/WSINDy/OpInf/SR è numerica e statistica: identifica coefficienti, non scompone u, non dà identificabilità esatta. La teoria esatta di identificabilità esiste (Scholl; He–Zhao–Zhong; Stanhope; Willems) e l'identificazione esatta di annullatori esiste in computer algebra (guessing, Prony, MPUM). **Nessun lavoro trovato** formula la scomposizione u = Σ_n u_n + E_int **per termine dell'operatore**, con classi naturali per termine ed E_int caratterizzato.

## 2. Dichiarazione di novità per G★ (Q2, Q6)

### 2.1 Claim di G★ vs letteratura

**(i) λ ∈ ker 𝔾(u); unicità ⟺ dim ker 𝔾(u) = 1** (§1.2 fatto 1) — **NOTO.**
Scholl et al. arXiv:2210.08342, Prop. 1: in una classe V chiusa per somma/differenza, F con F(g)=∂_t^n u è unico ⟺ g=(u_{α_1},…,u_{α_k}) è annullata solo banalmente in V. **Cor. 1 (F lineare): unico ⟺ u_{α_1},…,u_{α_k} linearmente indipendenti** — con la normalizzazione "coeff. di ∂_t^n = 1" è esattamente dim ker 𝔾(u)=1. È anche la base implicita di SINDy/PDE-FIND (rango della libreria). (Unicità esatta, non "a meno di scala".)

**(iii) Identificabilità (G4).**
- *ODE coeff. costanti:* Scholl Prop. 6–7 (ordini 2, 3: unico ⟺ u non è costante, esponenziale, somma di ≤2 modi, blocco di Jordan, coppia e^{μt}cos/sin). Il caso generale "ordine dell'annullatore minimo = ordine di L" è teoria classica (ricorrenze lineari, Hankel/Prony, guessing). — **NOTO** (enunciato unico per ordine qualsiasi non trovato: da scrivere in Fase 3, rischio basso).
- *PDE evolutive u_t = −Σ p_α ∂^α u su 𝕋^d:* **He–Zhao–Zhong FoCM 2024, Thm 3.2**: con Q = supp û_0, se |Q| supera una soglia combinatoria e Q non giace su un'ipersuperficie algebrica di grado ≤ n (separatamente per termini pari/dispari), p è unico da u(·,t_1), u(·,t_2) con |t_2−t_1| piccolo. La prova usa proprio il log-simbolo: (2π)^{d/2} log|û(ξ,t_2)/û(ξ,t_1)|/(t_2−t_1) = −Σ_{|α| pari} c_α ξ^α, e l'argomento per i termini dispari. **G4 (parte evolutiva) è NOTO.** In 1D si riduce a "Q ha abbastanza punti" (Vandermonde pari/dispari), da riconciliare con la forma "|supp û_0| ≥ deg a + 1" di NOTAZIONE (attenzione alla fase: serve |t_2−t_1| piccolo o la conoscenza del ramo).
- *Coeff. variabili:* He–Zhao–Zhong Thm 3.4 (rango di (∂^α u(x,t_k))_{k,α}, m istanti), 3.5 (u_0 random ⇒ q.c. identificabile). **Scholl Prop. 10: ODE di ordine 2 con coeff. continui λ(t), μ(t): unicità MAI** (annullatore H = u_t y − u y'). ⇒ La versione E1 di G★ con f_k(x) arbitrarie è **PROB. FALSA** senza restringere la classe dei coefficienti (polinomi di grado ≤ d, olonomi, dimensione finita).
- *Caso generale coeff. costanti (non evolutivo): Ann(u) e chiusura di Zariski del supporto della misura di Ehrenpreis.* Non trovato in questa forma. Per u esponenziale-polinomiale coincide con Prony multivariato (Kunis et al. 2016; Mourrain 2018: ker della matrice dei momenti = ideale annullatore, inverse system per le molteplicità) e con l'MPUM 2-D (Rapisarda–Antoulas 2016). Per misure continue — **APERTO** come enunciato; rischio che sia corollario diretto di Ehrenpreis–Palamodov (Hörmander II; Björk) ⇒ novità bassa ma utile come teorema unificante.

**(ii) Scomposizione per termine u = Σ_n u_n + E_int, classi {e_{n,i}}, E_int caratterizzato, complessità < O(eⁿ)** — **nessun prior art diretto trovato** (ricerche: "decompose solution per operator term", "interaction term exact split", "solution splitting", "component separation PDE"). Vicini: splitting di operatore (Trotter 1959, Strang 1968, BCH/Zassenhaus — R5; Wei–Norman via SCOUT-1) e splitting additivo della SOLUZIONE di Efendiev–Vabishchevich (numerico, L noto); Prony generalizzato (Peter–Plonka 2013: autofunzioni di un operatore NOTO, cioè modi); MCA/separazione geometrica (dizionari, non termini); He–Zhao–Zhong usano l'additività del log-simbolo per identificare, non per scomporre.
⇒ **Il nucleo nuovo di G★ è (ii)** con la sua struttura algebrica: G1 (A8 additivo falso in generale), G2 (fattorizzazione ⇒ split esatto), G3 (split moltiplicativo/log-simbolo, E_int bilineare, 2^N termini), G5 (invarianti della "non-matrice"). Gli ingredienti sono classici (Bezout, Malgrange–Ehrenpreis, semigruppi, Jacobson); il delta è la **combinazione come teoria della scomposizione per termine**.

**Esattezza / "analitico, non ML":** l'identificazione esatta di annullatori è già tecnologia (guessing, Prony, MPUM): "esatto" da solo NON è un delta.

### 2.2 Lavori più vicini (formato novelty-check)
| Paper | Anno | Venue | Sovrapposizione | Differenza |
|---|---|---|---|---|
| Scholl, Bacho, Boche, Kutyniok | 2022/2026 | arXiv:2210.08342 / Machine Learning | (i); (iii) ODE ord. 2–3; coeff. variabili | nessuna scomposizione; non usa struttura di Ann(u) |
| He, Zhao, Zhong | 2024 | FoCM 24 | (iii) PDE evolutive; log-simbolo | nessuna scomposizione; solo 𝕋^d, solo evolutive |
| Mourrain; Kunis et al. | 2018; 2016 | FoCM; LAA | Ann(u) esp.-polinomiale multivariato | nessun legame con termini |
| Rapisarda–Antoulas (MPUM 2-D) | 2016 | SICON | identificazione esatta PDE coeff. cost. | non scompone; dim. finita |
| Peter–Plonka | 2013 | Inverse Problems | scomposizione esatta in autofunzioni | per modi, non per termini |
| Kauers et al. | 2009–2015 | RISC / LNCS | annullatore esatto | ODE/ricorrenze; nessuna scomposizione |
| Efendiev–Vabishchevich | 2020 | arXiv | split additivo di u | numerico, L noto |
| Härkönen–L-H–Raiță | 2023 | ICML | spazio di Ehrenpreis (G6) | direzione diretta, probabilistico |

### 2.3 Valutazione
- **Punteggio 6/10** (vicini chiari, delta difendibile su (ii)).
- **Raccomandazione: PROCEED con ri-scoping.** Nessun paper nominabile contiene la scomposizione per termine con E_int ⇒ nessun ABANDON.
- **Delta in una frase verificabile:** *data una soluzione esatta u di una PDE lineare 1D, si caratterizza quando e come u si scompone in componenti attribuite ai singoli termini dell'operatore, con E_int in forma chiusa (quadri additivo, moltiplicativo, log-simbolo), e i criteri di identificabilità noti (Scholl; He–Zhao–Zhong) diventano corollari della struttura dell'ideale annullatore.*
- **Rischio (cosa citerebbe un revisore):** Scholl e He–Zhao–Zhong per (i)/(iii); guessing/Prony/MPUM per l'esattezza; splitting/BCH per E_int evolutivo (come "errore di splitting").

### 2.4 Verdetto sul trigger §1.6 "literature hit" — **SCATTA (parzialmente)**
1. (i) e (iii)-evolutiva passano a **DIMOSTRATO-CON-FONTE** (Scholl Cor. 1; He–Zhao–Zhong Thm 3.2): in Fase 3 vanno solo riscritte in notazione comune (𝔾(u), Ann(u)) e citate.
2. G★ va **ri-centrato su (ii)** (scomposizione + E_int + complessità) e sul **teorema unificante di identificabilità** per coeff. costanti via Ann(u)/varietà (estensione di He–Zhao–Zhong a PDE non evolutive e a ℝ con misure continue — APERTO).
3. Coeff. variabili (L3/L4): fissare una classe di coefficienti a dimensione finita, altrimenti (iii) è falsa (Scholl Prop. 10).

### 2.5 Avvocato del diavolo
- *"(ii) è operator splitting rinominato."* In parte vero nel caso evolutivo commutante (G3). Contro: lo splitting tratta l'errore numerico di un L noto; qui L è incognito e la scomposizione è un oggetto dei dati. Il delta regge solo se la Fase 3 produce enunciati che lo splitting non dà (identificazione di u_n da u; caratterizzazione di quando A8 vale: G1/G2).
- *"G1 è banale."* L'osservazione algebrica è corta; da sola non basta, ma è il teorema negativo che giustifica il quadro moltiplicativo.
- *Bias di ricerca:* solo motori web + arXiv + GitHub; niente zbMATH/MathSciNet. Possibili lavori in teoria dei sistemi (Oberst/Willems/Pillai–Shankar) o D-moduli non intercettati ⇒ Q-R8-1.

## 3. Strumenti (Q3, Q4)

### 3.1 Mathlib (master di `leanprover-community/mathlib4`, ottobre 2026; verificato su elenco directory e code search GitHub)
| Area | Stato | Dettagli | Mancante per G★ |
|---|---|---|---|
| Spazi di Hilbert | presente | `Analysis/InnerProductSpace/*`: `Orthogonal`, `Projection/`, `l2Space`, `PiL2`, `Adjoint`, **`GramMatrix`**, **`Reproducing/` (RKHS)**, `JointEigenspace`, `Rayleigh`, `SingularValues`, `LaxMilgram` | frame continui, basi di Riesz (da verificare) |
| Teorema spettrale | parziale | `Spectrum.lean`: dim. finita (`LinearMap.IsSymmetric.eigenvectorBasis`, `diagonalization`, `charpoly_eq`); compatti autoaggiunti in spazio completo (`ContinuousLinearMap.orthogonalComplement_iSup_eigenspaces_eq_bot`, `finite_dimensional_eigenspace`); calcolo funzionale C* `Analysis/CStarAlgebra/ContinuousFunctionalCalculus/*` (`cfc`) | autoaggiunti NON limitati (operatori differenziali), misura spettrale |
| ODE | presente | `Analysis/ODE/{PicardLindelof, Gronwall, ExistUnique, Transform, DiscreteGronwall}`: `IsPicardLindelof.*`, `ODE_solution_unique` | teoria dedicata ODE lineari a coeff. costanti (base xᵏe^{λx}) non trovata; esiste `Algebra/LinearRecurrence.lean` (analogo discreto) |
| Polinomi/algebra | presente | `Polynomial`, `RingTheory/Polynomial/Wronskian.lean`, ideali/PID, `OreLocalization`, `LinearAlgebra/CliffordAlgebra/*` | **basi di Gröbner assenti**; **algebra di Weyl / polinomi di Ore assenti** (code search: 0 risultati); matrice compagna non trovata per nome |
| Distribuzioni | presente (recente) | `Analysis/Distribution/{Distribution, TemperedDistribution, SchwartzSpace/, TestFunction, Support, FourierMultiplier, Sobolev, DerivNotation}`: `Distribution Ω F n`, `delta`, `ofFun`, derivata direzionale `lineDerivCLM`; Doll arXiv:2510.24060 | convoluzione, soluzioni fondamentali, Malgrange–Ehrenpreis, Ehrenpreis–Palamodov: assenti |
| Semigruppi | assente | nessun "C₀-semigroup"/"strongly continuous semigroup"; c'è `NormedSpace.exp` (operatori limitati) | Hille–Yosida, Trotter ⇒ G3 formalizzabile solo per generatori limitati o modo per modo su 𝕋 |
| Clifford | solo algebra | `CliffordAlgebra/{Basic, Even, SpinGroup, Conjugation, Contraction, …}` | operatore di Dirac, analisi di Clifford |

**Raccomandazione Fase 5:** formalizzare per primo L0 in forma algebrica (ℂ[D] PID, Bezout, nucleo di prodotti coprimi) e il caso 𝕋 modo per modo (G3/G4 come identità su coefficienti di Fourier) — fattibile con la Mathlib attuale. Ehrenpreis–Palamodov, semigruppi C₀ e algebra di Weyl richiedono sviluppo di libreria pesante ⇒ riconsiderare ordine/strumento al Gate 5 (§1.6).

### 3.2 SymPy 1.14.0 (`.venv`; verifica con script nello scratchpad di sessione, non nel progetto)
- `sympy.holonomic`: `expr_to_holonomic`, `from_hyper`, somma/prodotto/composizione, `to_expr`/`to_hyper`/`to_meijerg` (annullatori a coeff. polinomiali, una variabile). **Verifica:** `expr_to_holonomic(exp(2x)+x·e^{−x})` → `(8/3−2x) + (−x−2/3)Dx + (x−1/3)Dx²`, **ordine 2** a coeff. polinomiali, mentre il minimo a coeff. costanti è (D−2)(D+1)², ordine 3. ⇒ **l'annullatore minimo, e quindi G4, dipende dall'anello dei coefficienti ammesso** (avvisati R2, R4). `J_0` → `x + Dx + x·Dx²` (corretto).
- `dsolve`: ODE lineari (coeff. costanti e varie classi variabili). `pdsolve`: solo primo ordine (`u_t+u_x=0` → `F(x−t)`); **calore → NotImplementedError** ⇒ le verifiche C2 vanno fatte per sostituzione (`T e = 0`).
- `groebner`: anelli commutativi (utile per Ann(u) a coeff. costanti); nessuna algebra di Weyl.

### 3.3 SageMath `ore_algebra` (repo `mkauers/ore_algebra`; LNCS 8942, 2015)
Guessing, `lclm`, `gcrd`, chiusure D-finite, desingolarizzazione, soluzioni in serie generalizzate, valutazione numerica rigorosa; Sage ≥ 9 o passagemath. Ruolo: oracolo esatto per C3-ODE e per G2 a coeff. variabili (ker lclm(L_1,L_2) = ker L_1 + ker L_2). **Non installato**; opzionale (piano Step 0). Multivariato: Mgfun (Maple), Macaulay2 `Dmodules`/`NoetherianOperators` (usato da EPGP), Singular `Plural`.

## 4. Problema 1, Problema 2, Idea I — solo bibliografia (Q5)
**Problema 1 (V variabile come "rumore").** Inverso spettrale: Borg (Acta Math 78, 1946), Gel'fand–Levitan (Izv. 1951), Marchenko, Hochstadt–Lieberman (SIAP 1978), Pöschel–Trubowitz (1987), Freiling–Yurko (2001); scattering inverso (GGKM, PRL 1967); Dirac: Gasymov–Levitan (1966). **Osservazione:** questi teoremi usano dati SPETTRALI. Con una soluzione esatta il recupero di V è puntuale: per −u''+Vu=Eu, V = E + u''/u dove u ≠ 0; per iψ_t = −ψ_xx + Vψ, V = (iψ_t+ψ_xx)/ψ (analogo di Scholl Prop. 8: unicità ⟺ zeri isolati). Quindi "V come rumore" non è un problema di identificazione ma di **scomposizione/separazione** (V fuori da ogni dizionario finito). Nulla costruito.
**Problema 2 (coefficienti matriciali, Dirac 4×4, Clifford).** Coefficienti matriciali costanti = sistemi ⇒ moduli R^k/M, Ehrenpreis–Palamodov per sistemi (Hörmander II; Björk 1979; Oberst 1990); EPGP gestisce già sistemi; MPUM multivariabile. Inverso vettoriale: Chelkak–Korotyaev (JFA 2009). Clifford: Brackx–Delanghe–Sommen (1982); Gilbert–Murray (CUP 1991). Mathlib: solo l'algebra. Nulla costruito.
**Idea I.** Champion–Lusch–Kutz–Brunton PNAS 116 (2019) (autoencoder + SINDy); Lusch–Kutz–Brunton Nat. Commun. 9 (2018) (Koopman); t-SNE (van der Maaten–Hinton JMLR 9, 2008); EM/GMM (Dempster–Laird–Rubin 1977). Controparte analitica senza pesi: MCA / separazione geometrica (R1). Nulla costruito.

## 5. Sovrapposizioni segnalate (AVVISI inviati)
| Sovrapposizione | Agenti | Azione |
|---|---|---|
| Prony/FRI, guessing, identificabilità, inverso SL | R4 ⇄ R8 | R8 solo posizionamento; hit passati a R4 |
| Identificabilità, Prony multidim., MPUM | SCOUT-2 ⇄ R4 (e SCOUT-1: Oberst/Willems) | SCOUT-2 propone già merge in RT-4: concordo |
| MCA / separazione geometrica | SCOUT-2 ⇄ R1 | segnalato |
| Koopman/DMD | R1 (R1-d) ⇄ R7 | segnalato |
| EPGP | R1 (R1-c) ⇄ R2 (Q7) | proposta: R2 algebra, R1 GP/RKHS |
| Log-simbolo / split additivo di u | R5 (G3) | segnalati He–Zhao–Zhong (3.5)–(3.6), Efendiev–Vabishchevich |
| Clifford / Dirac | R6 | ricordato fuori scopo |

## 6. Mappa su item del piano
- **C3:** (i), (iii) in gran parte NOTI; APERTO il teorema unificante Ann(u)/varietà per PDE non evolutive e misure continue.
- **C4 / A8 / P1 / P3:** (ii) APERTO e NUOVO.
- **C1 / G6:** EPGP come encoder (direzione diretta) NOTO; uso inverso APERTO.
- **II / G5:** nessun prior art specifico sulla "non-matrice" per l'identificazione.
- **Fase 5:** §3.1. **Problema 1/2, Idea I:** §4.
