# REPORT — SCOUT-1 (horizon scout: algebra / geometria / rappresentazioni / visioni categoriali)

Data: 2026-10-22 · Slot RT-ω · Notazione NOTAZIONE.md v1 · NEW-ROUTE in `inbox/central.md`, registrate in ROUTES.md come RT-S1a…RT-S1i.

## 0. Metodo e skill caricate (Regola 2)
- `academic-research-skills\deep-research\SKILL.md` (Read, struttura). Non ho usato `anthropic-skills:deep-research` perché orchestra sotto-agenti e non ero autorizzato a lanciarne. Ho seguito il flusso domanda → fonti → sintesi con WebSearch diretto.
- `scientific-brainstorming\SKILL.md` (Read integrale). Ho fatto prima un round di generazione indipendente, senza letteratura (14 idee grezze), poi il controllo bibliografico, poi ho riaperto la generazione. Etichette usate: idea / assunzione / evidenza localizzata / decisione.
- `idea-discovery\SKILL.md` (Read, struttura). Pipeline survey → idee → novelty → critica → ranking, senza pilot e senza revisore Codex (decisione dell'utente: solo Claude).
- `novelty-check\SKILL.md` (Read integrale). Ho applicato i "verdict limits": ABANDON solo se un articolo nominato contiene già il risultato. Il cross-check con un modello esterno non è stato eseguito (Codex escluso).
- `scientific-critical-thinking\SKILL.md` (Read integrale). Struttura di ogni verdetto: punti forti, criticità per gravità, rimedio.
- `research-lit`/`arxiv`: solo stringhe manuali via WebSearch. Nessuno script `_vendor` eseguito.
- Controllo SymPy (controllo, non metodo): `research/SCOUT-1/sympy/trop_check.py`, output riportato in coda allo script.

**Diagnosi comune (assunzione → decisione).** Per l'operatore, la **somma di termini** non è un'operazione che ker "vede"; la **composizione** lo è (LCLM ↔ +, GCRD ↔ ∩). Quindi ogni scomposizione per termine richiede una struttura aggiuntiva, e ciascuna strada ne sceglie una: scala/valutazione (TROP, STOKES), singolarità (MICRO), reticolo dei sottoinsiemi (MOB), modulo/Galois (EXT), dati locali (RIGID). RT-S1b (NAT) rende rigorosa questa diagnosi.

Ranking (giudizio di SCOUT-1; criteri fissati prima: valore per G★, analiticità k3, novità rispetto a RT-1…7, costo): **1 TROP · 2 NAT · 3 RIGID · 4 MOB · 5 STOKES · 6 EXT · 7 MICRO · 8 APOL · 9 WN (merge).**

---

## RT-S1a TROP — decomposizione tropicale / dominant balance
**Idea.** Prendo il poligono di Newton del simbolo, pesato con log|λ_k|. Le sue facce selezionano gruppi di termini, cioè le forme iniziali in_w P, che dominano in una regione di scala. La componente è il nucleo della forma iniziale: se questa è quasi-omogenea le soluzioni sono autosimili (Gauss, Airy). E_int è il contributo delle zone di crossover, vicino alla curva tropicale / all'ameba di V(P).
**Enunciati.**
- [S1-P1] (DIMOSTRATO, elementare) Per a(ξ)=Σa_kξ^k con |ξ|=e^s si ha log|a_kξ^k| = log|a_k|+ks. Quindi il termine k domina su una banda non vuota ⟺ (k, log|a_k|) è un vertice dell'inviluppo superiore. Con SymPy: per 1e-2ξ+ξ²+1e-3ξ³+ξ⁴ i vertici sono [1,2,4] e il termine 3 non domina mai. Per A6 ("∃ funzioni legate individualmente a ogni operatore?") la risposta è **sì solo per i termini-vertice**; i termini interni sono puro E_int.
- [S1-P2] (NOTO nella sostanza, da enunciare con tasso) Limiti di scala per u_t = D u_xx + b u_xxx: t·a(s/√t) → −Ds² per t→∞ (Gauss) e t·a(s t^{-1/3}) → −ibs³ per t→0⁺ (Airy), verificati con SymPy. Il nucleo riscalato converge al nucleo della forma iniziale estrema (convergenza dominata su Fourier).
- [S1-Q1] (APERTO) In 2 variabili (L3) le facce interne danno sotto-equazioni binomiali λ_iT_i+λ_jT_j: sono le "classi" di A6 nella lettura "sotto-equazione"?
**Evidenza localizzata.** La tropicalizzazione differenziale esiste (Grigoriev 2017; Aroca–Garay–Toghani, PJM 283 (2016); Falkensteiner et al. 2020 per PDE), ma riguarda il supporto di soluzioni in serie formali, non bande di frequenza di PDE a coefficienti costanti. Il dominant balance via poligono di Newton è classico (power geometry di Bruno). In questa ricerca limitata non ho trovato lavori che definiscano componenti per termine ed E_int con la geometria tropicale del simbolo. Novelty: PROCEED.
**Critica.** (Importante) La stima |e^{ta}−e^{ta_kξ^k}| ≤ t|a−a_kξ^k|·e^{t·max Re} cresce in modo secolare con t. La piccolezza di E_int vale solo in una finestra congiunta scala×tempo: è un teorema di regime, non "E_int=0". (Minore) L'identità u=Σu_k+E_int è esatta (B4); solo la stima è asintotica.
**Verdetto: PROMUOVERE a scouting** (1 sessione L2 + 1 sessione L3). Dà una risposta falsificabile ad A6/A8/B3.

## RT-S1b NAT — non-naturalità di E_int (somma vs prodotto)
**Fatti.** (DIMOSTRATO, banale) Se L=L1+L2 allora L ∈ D·L1+D·L2 = D·gcrd(L1,L2), quindi ker L1 ∩ ker L2 ⊆ ker L. (NOTO) Ore 1933: ker LCLM = ker L1 + ker L2 e ker GCRD = ∩. Oberst 1990: anti-isomorfismo sottomoduli ↔ comportamenti, con C^∞ cogeneratore iniettivo.
**Congettura [S1-Q2].** Non esiste una trasformazione naturale Sol(L) → Sol(L1)⊕Sol(L2), equivariante per le simmetrie del dato, che non passi per ker L1 ∩ ker L2. Dunque ogni E_int dipende da una struttura scelta, e l'elenco delle strutture classifica i "quadri" di WP2: additivo, moltiplicativo, log, scala, singolarità, sottoinsiemi.
**Critica.** (Critica) "Naturale" va formalizzato: con la categoria sbagliata l'enunciato è vuoto o falso. Rimedio: usare come equivarianza il gruppo delle simmetrie (traslazioni, scala, gauge).
**Verdetto: PROMUOVERE** (costo basso). Organizza WP2, rende rigorosa G1 e risponde a C3: "sì, ma relativamente a una struttura dichiarata".

## RT-S1c MOB — Möbius / cumulanti sul reticolo dei termini
**Fatti (DIMOSTRATI, algebra elementare).** Si pone c_S = Σ_{T⊆S}(−1)^{|S∖T|}u^{(T)}; allora u = Σ_S c_S (Rota 1964). Per coefficienti costanti c_S = Π_{k∈S}(S_k−1)u_0, cioè la (K_1−δ)*(K_2−δ)*u_0 di G3 e i 2^N termini di B2. Nel quadro log c_S=0 per |S|≥2. I quadri diventano "il gruppo in cui si fa la Möbius"; l'ordine d'interazione k dà costo O(N^k).
**Novità.** I mattoni sono noti (ANOVA/Hoeffding, cluster expansion, cumulanti liberi di Speicher). È nuovo l'uso come definizione unificata di E_int.
**Critica.** (Importante) u^{(T)} richiede i dati e L già identificato: serve alla scomposizione, non all'identificazione. (Importante) Con termini non commutanti l'ordine d'interazione è tipicamente N; la riduzione vale per algebre nilpotenti. (Minore) I cumulanti liberi qui sono solo un'analogia.
**Verdetto: strato di definizione per WP2/R5.** Va fuso in RT-2/RT-3 se entro la Gate 2 non produce un teorema sull'ordine d'interazione.

## RT-S1d EXT — addendi indecomponibili, Ext¹, K_0, Galois
**Idea.** Si prende M_u = D/Ann(u). Le componenti sono gli addendi di Krull–Schmidt, ottenuti con gli idempotenti dell'eigenring End_D(D/DL) (Singer, AAECC 7 (1996) 77–104; van Hoeij). Se la decomposizione non spezza, E_int ∈ Ext¹. In K_0 l'additività è esatta, quindi l'"encoder" di D1 è il passaggio a K_0, che perde esattamente Ext¹. Lato Galois: E_int ↔ radicale unipotente R_u(G), e G classifica la classe di funzioni (A5).
**Enunciati.** (NOTO, Singer 1996) L completamente riducibile ⟺ D/DL semisemplice; la decomposizione è calcolabile. (CONGETTURA) "A8 vale ⟺ M_u semisemplice, e la componente n è e_n(u)".
**Critica.** (Critica) A coefficienti costanti (L0–L3) coincide con RT-1 / decomposizione primaria: il valore aggiunto compare solo a L1/L4. (Importante) Le componenti sono fattori, non termini (cfr. NAT).
**Verdetto: scouting con merge condizionale** in RT-1/RT-6. La lettura E_int = Ext¹, D1 = K_0 va registrata subito nel glossario.

## RT-S1e RIGID — schema di Riemann, rigidità di Katz, Deligne–Simpson additivo
**Idea.** Un sistema fuchsiano è la somma di termini locali A_i/(x−a_i), ciascuno con la sua classe locale. Rigidità (Katz 1996): i dati locali determinano l'operatore. I parametri accessori sono ciò che le componenti non determinano, cioè i "moduli di E_int". Esistenza (Crawley-Boevey, Duke 2003): esistono A_i in classi di coniugio prescritte, con ΣA_i=0 e senza sottospazio invariante comune, ⟺ criterio sulle radici di Kac–Moody del quiver a stella. Costruzione: convoluzione media di Katz; Oshima, MSJ Memoirs 28 (2012).
**Perché conta.** È l'unico quadro trovato in cui "operatore = somma di termini, ognuno con la sua classe" è letteralmente la struttura, e in cui esistono teoremi di esistenza e unicità del tipo P4.
**Critica.** (Critica) Vale solo per coefficienti razionali con singolarità (L1/L4). (Importante) Estrarre i dati locali da una sola u è un problema di R4 (open_questions 6). (Minore) L'enunciato esatto di Crawley-Boevey va citato dal PDF arXiv math/0103101; io ho verificato solo l'abstract.
**Verdetto: PROMUOVERE condizionato al ladder.** Stato registrato dal coordinatore: parked fino a L1/L4, e lo condivido.

## RT-S1f STOKES — Levelt–Turrittin + Stokes come E_int
**Idea.** In un punto irregolare la decomposizione formale e^{q_j}x^{ρ_j}·(serie) esiste sempre (Turrittin 1955, Levelt, Malgrange). Le q_j vengono dal poligono di Newton dell'operatore, cioè da gruppi di termini. Le componenti sono multisommabili in settori (Ramis; Malgrange–Ramis 1992; Balser 2000), il che dà teoremi di convergenza. E_int è dato dai moltiplicatori di Stokes; esempio: Airy, con moltiplicatore noto.
**Critica.** (Importante) Le componenti sono settoriali, non globali. Se si vogliono componenti globali, la strada diventa un teorema d'impossibilità per C4. (Minore) È TROP applicato a coefficienti variabili.
**Verdetto: PROMUOVERE insieme a TROP** (una sessione "poligono di Newton" con due capitoli).

## RT-S1g MICRO — scomposizione microlocale
**Idea.** Nel caso strettamente iperbolico (trasporto, onde, telegrafo) u = Σu_j + E_int con WF(u_j) ⊂ Char_j e E_int ∈ C^∞ (Taylor 1981; Hörmander III; Kashiwara–Schapira 1990). È una lettura precisa di "E_int ≈ 0" (B1) e di "rumore = parte liscia" (A1).
**Critica.** (Critica) Nei casi parabolici, ellittici e dispersivi non dà informazione. (Importante) Vale solo modulo C^∞, quindi non è esatta nel senso di B4.
**Verdetto: PARCHEGGIARE** come attributo del catalogo ("iperbolico ⇒ split microlocale"). Va riattivata se PR-C2b mostra molte voci iperboliche.

## RT-S1h APOL — apolarità: catalecticante ⇔ Hankel
**Idea.** Per dualità di Sylvester/Macaulay, la Hankel di Prony (RT-4) e il catalecticante del simbolo come forma binaria (via a, RT-5) sono lo stesso oggetto (Iarrobino–Kanev 1999; Kung–Rota 1984). La decomposizione di Waring scrive P_m = Σc_iℓ_i^m, una somma di potenze di operatori di trasporto. Invarianti per E4: rango di Waring e rango del catalecticante.
**Critica.** (Importante) La novità sta nel lemma-ponte RT-4 ↔ RT-5; gli invarianti delle forme binarie sono probabilmente già noti a R6.
**Verdetto: MERGE in RT-5/RT-4** come lemma-ponte (inviata a R6).

## RT-S1i WN — Wei–Norman
**Idea.** Se i termini generano un'algebra di Lie risolubile di dimensione d, si ha e^{tΣA_k} = Π e^{g_i(t)B_i} esattamente, con g_i soluzioni di ODE (J. Math. Phys. 4 (1963) 575–581). E_int è codificato da d funzioni, quindi la complessità è d invece di 2^N.
**Verdetto: MERGE in RT-3** (già deciso dal coordinatore): è un'alternativa esatta e finita alla serie BCH.

---

## Idee scartate o fuse (round indipendente, per tracciabilità)
- **Jet / implicitizzazione dell'immagine di j^k u:** coincide con ker 𝔾(u) (RT-4); il caso non lineare è eliminazione differenziale (Fase 4). → merge.
- **Dualità di Oberst–Willems:** è il linguaggio di RT-1/RT-4 ed è assorbita in NAT. Non esistono rappresentazioni-immagine per P scalare non nullo in 2 variabili (modulo di torsione). → merge.
- **Hopf (Connes–Kreimer, Faà di Bruno, pre-Lie/Magnus):** già dentro RT-3 e MOB. → merge.
- **Probabilità libera:** solo un'analogia. → kill come strada autonoma.
- **Clifford / algebra geometrica:** serve solo per Dirac (Problema 2). → parked fino alla Fase 5.
- **Galois parametrizzato (Cassidy–Singer):** promettente ma costoso. → open_questions 8.
- **Riemann–Hilbert come encoder globale:** banale a L0–L3; il contenuto utile è già in RIGID/STOKES. → merge.

## Mappa sugli item
| strada | C1 | C2 | C3 | C4/A8 | P1 | P3 | P4 | II | D1 |
|---|---|---|---|---|---|---|---|---|---|
| TROP | | ✓ | ✓ | ✓ | ✓ | | | F6 | ✓ |
| NAT | ✓ | | ✓ | ✓ | ✓ | | | ✓ | ✓ |
| MOB | | | | ✓ | ✓ | ✓ | | | ✓ |
| EXT | | ✓ | | ✓ | ✓ | | ✓ | (b) | ✓ |
| RIGID | | C2.6 | ✓ | ✓ | | | ✓ | E1 | |
| STOKES | | ✓ | | ✓ | ✓ | | | | |
| MICRO | | ✓ | | ✓ | ✓ | | | | ✓ |
| APOL | | | ✓ | | | | | (a) E4,E5 | |
| WN | | | | | ✓ | ✓ | | G6 | |

Stato degli enunciati: S1-P1 DIMOSTRATO (elementare); S1-P2 noto nella sostanza, da scrivere con tasso; il fatto NAT ker L1∩ker L2 ⊆ ker L DIMOSTRATO; la congettura NAT APERTA; le identità MOB DIMOSTRATE; Singer 1996 DIMOSTRATO-CON-FONTE; Katz / Crawley-Boevey DIMOSTRATO-CON-FONTE (enunciato esatto da trascrivere).

---

## Addendum (dopo l'AVVISO del coordinatore): RT-S1a ∪ RT-S2b, enunciato unico da dimostrare
Ho letto `research/SCOUT-2/REPORT.md` §S2-B. Le due strade sono lo stesso oggetto visto da due lati. Il lato algebrico (SCOUT-1) dà il poligono di Newton pesato e la regola "vertice ⇔ classe propria". Il lato analitico (SCOUT-2) dà la localizzazione in fase e la separazione ℓ¹ di Donoho–Kutyniok. I termini incrociati di Wigner vanno usati **solo come diagnostica** (Wigner è quadratica in u), mentre la scomposizione resta lineare in u.

**[TROP-L2] Teorema da dimostrare (livello L2, poi L3).**
Ipotesi: u_t = a(∂_x)u con a(iκ) = Σ_{k∈K} a_k (iκ)^k, problema ben posto (sup_κ Re a(iκ) < ∞), u_0 ∈ L²(ℝ).
Siano k_1<…<k_r gli indici i cui punti (k, log|a_k|) sono vertici dell'inviluppo superiore; κ*_j = (|a_{k_j}|/|a_{k_{j+1}}|)^{1/(k_{j+1}−k_j)} i punti di rottura; B_j le bande |κ| ∈ [κ*_{j−1}, κ*_j). Si definiscono
u_j(t) := F^{-1}[ 1_{B_j}(κ) e^{t a_{k_j}(iκ)^{k_j}} û_0 ] (lineare in u_0; una classe per vertice) e E_int := u − Σ_j u_j.
Tesi:
(i) l'identità u = Σ_j u_j + E_int è esatta, e ogni u_j ∈ ker(∂_t − a_{k_j}∂_x^{k_j}) è localizzata in frequenza (classe C2 del termine k_j);
(ii) se k non è un vertice, il termine k non ha una banda dove domina (|a_kκ^k| ≤ max_j |a_{k_j}κ^{k_j}| per ogni κ), quindi non ha una componente propria;
(iii) vale la stima esplicita ‖E_int(t)‖ ≤ Σ_j sup_{κ∈B_j} |e^{t a(iκ)} − e^{t a_{k_j}(iκ)^{k_j}}| · ‖1_{B_j}û_0‖, con il fattore piccolo all'interno delle bande e O(1) vicino ai κ*_j;
(iv) limiti di scala: il nucleo riscalato tende al nucleo della forma iniziale estrema, Gauss per t→∞ se k_1=2, Airy/k_r-autosimile per t→0⁺ (verificato in SymPy per a = Dκ² + bκ³), con tasso da fissare;
(v) (lato SCOUT-2) se u_0 è sparso in due frame adattati a bande o regimi diversi, la separazione ℓ¹ ha errore relativo → 0 alle scale fini, perché la cluster coherence → 0 (Donoho–Kutyniok 2013).
Criterio d'eliminazione invariato: se a L3 gli unici vertici utili sono sempre i due estremi, la strada si fonde in RT-2.
Owner suggerito: una sessione congiunta "poligono di Newton" (TROP + STOKES + S2-B), con R5 per la stima (iii) e R1 per (v).
