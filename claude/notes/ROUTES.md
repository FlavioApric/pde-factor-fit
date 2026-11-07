# ROUTES — registro delle strade (gestito dal coordinatore; proposte via inbox/central.md NEW-ROUTE)

| id | punto di decisione | origine | idea | stato | criterio promozione / eliminazione |
|---|---|---|---|---|---|
| RT-1 | A8 / C4 | seme (piano §1.2-2a) | split additivo per fattorizzazione P=P₁P₂ | seed | promuovi se teorema con intersezione di dim. finita; elimina se falso già per ODE |
| RT-2 | A8 / P1 | seme (§1.2-2b) | split moltiplicativo / log-simbolo per somme di termini commutanti | seed | promuovi se identificazione O(N) dimostrata |
| RT-3 | P1 / P3 | seme (§1.2-2c) | commutatori BCH/Zassenhaus/Dyson per termini non commutanti | seed | promuovi se serie convergente con ipotesi verificabili |
| RT-4 | C3 | seme | annullatore Ann(u), Gram del jet, Prony/Hankel | seed | elimina se l'identificabilità richiede ipotesi non verificabili |
| RT-5 | II | seme | via (a) tensore simbolo | seed | confronto invarianti (E4) |
| RT-6 | II | seme | via (b) compagna / matrice su anello di operatori | seed | confronto invarianti (E4) |
| RT-7 | C1 | seme (G6) | spazio di Ehrenpreis L²(V(P),μ) come encoder analitico | seed | promuovi se isometria/frame dimostrati |
| RT-ω | ogni decisione | slot aperto | strade non ancora note (scout) | open | — |
| RT-S1a | A8/C4/P1/C3 | SCOUT-1 | TROP: componenti = forme iniziali sulle facce del poligono di Newton del simbolo (dominant balance per scala) | proposed → scouting (verifica R4/R5) | promuovi: teorema dei limiti di scala + "vertice ⇔ classe propria"; elimina/fondi in RT-2 se solo i vertici estremi contano |
| RT-S1b | C4/P1/II | SCOUT-1 | NAT: ker è un anti-isomorfismo di reticoli (LCLM↔+, GCRD↔∩) ma non vede la somma di termini ⇒ E_int non è naturale | proposed → scouting (R2) | promuovi se non-naturalità dimostrata con precisione |
| RT-S1c | P1/P3 | SCOUT-1 | MOB: E_int = Σ_{|S|≥2} c_S, con c_S l'inversione di Möbius sul reticolo booleano dei termini; ordine d'interazione | proposed (candidata MERGE in RT-2/RT-3 come strato di definizione) | promuovi se dà un teorema sull'ordine (es. ≤ passo di nilpotenza) |
| RT-S1d | C2/C4/P1/P4 | SCOUT-1 | EXT: componenti = addendi indecomponibili di D/Ann(u) (Krull–Schmidt, eigenring), E_int ∈ Ext¹ | proposed → scouting (R2) | promuovi se a L1/L4 dà più della decomposizione primaria |
| RT-S1e | C3/P4/P1 | SCOUT-1 | RIGID: rigidità di Katz, Deligne–Simpson additivo; parametri accessori = moduli di E_int | parked fino a L1/L4 | promuovi se "rigido ⇒ identificabile da dati locali" enunciabile con fonte |
| RT-S1f | C2/C4/P1 | SCOUT-1 | STOKES: Levelt–Turrittin; E_int = fenomeno di Stokes (moltiplicatori) | proposed (L1) | promuovi con E_int in forma chiusa per confluenti ipergeometriche |
| RT-S1g | C4/P1 | SCOUT-1 | MICRO: disaccoppiamento microlocale nel caso strettamente iperbolico, E_int ∈ C^∞ | proposed (solo parte iperbolica) | promuovi con stima esplicita su telegrafo |
| RT-S1h | II/C3 | SCOUT-1 | APOL: apolarità/catalecticante ⇔ Hankel di Prony; Waring del simbolo principale | proposed → inviata a R6 | merge in RT-5/RT-4 se nessun invariante nuovo |
| RT-S1i | P1 | SCOUT-1 | WN: fattorizzazione Wei–Norman per algebre di Lie risolubili, complessità d anziché 2^N | merged-into: RT-3 (inviata a R5) | — |
| RT-S2a | C4/P1/P3 | SCOUT-2 | Faddeev / Lippmann–Schwinger: u = u⁽⁰⁾ + Σ_i u⁽ⁱ⁾, u⁽ⁱ⁾ = −G₀V_i u, sistema accoppiato N×N | proposed → scouting (R5) | promuovi: teorema L2 con pesi chiusi + legame con l'E_int di G3, e convergenza N×N in L4 |
| RT-S2b | C4/P1/P2/D1 | SCOUT-2 | separazione microlocale nello spazio delle fasi per regime di dominant balance; termini incrociati di Wigner = h(e₁,e₂) | merged-into: RT-S1a — enunciato unico [TROP-L2] in research/SCOUT-1/REPORT.md, Addendum | promuovi la strada fusa se ‖E_int‖/‖u‖ = O(ε^γ) con ε letto dal simbolo |
| RT-S2c | C3/P4/II | SCOUT-2 | behaviour di Willems / MPUM; realizzazione 2D di Rapisarda–Antoulas | proposed (inviata a R4, R6) | merge in RT-4 se si riduce ad Ann(u) + rango di Hankel |
| RT-S2d | P3 | SCOUT-2 | Mori–Zwanzig: proiezione su una classe ⇒ termine markoviano + memoria + "rumore" | parked / candidata merge in RT-3 | promuovi solo con E_int=0 ⇔ [𝒫,L]=0 o memoria = (K₁−δ)*(K₂−δ) |
| RT-R4a | C3/P4 (+A8) | R4 | restrizione al sottospazio ciclico Z(u) (sintesi spettrale, sempre univoca) + estensione alla classe 𝓛; identificabile ⟺ restrizione 𝓛→End(Z(u)) iniettiva. Verdetto C3.3: le componenti sono una carta di coordinate di Ann(u); scomposizione naturale indicizzata da V(P) (decomposizione primaria), termini = interpolazione lineare nel log-simbolo | proposed → scouting (candidata a ridefinire A8; **trigger di ri-pianificazione** §1.6 da portare al Gate 1/3 con l'utente) | promuovi con enunciato astratto per 𝓛 commutante (già in R4 §3); elimina se in L4 la restrizione non determina il simbolo anche con Z(u) denso |
| RT-R3a | C1/C1.4/A7/P3 | R3 | RW-DUAL: basi numerabili biortogonali di ker per equazioni di evoluzione (polinomi del calore v_n, funzioni associate w_n; Rosenbloom–Widder 1959, trasformata di Appell); risposta costruttiva ad A7 e duali per P3 | proposed → **R1 raccomanda PROMOZIONE** (base ortogonale di uno spazio di Fock pesato / RKHS di Mehler, R1-P11; non base in L²) | promuovi se si estende ad Airy/trasporto+diffusione (famiglie di Appell per ∂_t−a(∂_x)) con classe di crescita esplicita |
| RT-R2a | A8/A7/H0 | R2 | ostruzione periodica/risonanze: G2 vera su ℝ/convessi ma FALSA su 𝕋 (f=∂_t−∂_x², g=∂_t+∂_x, u=t; su ℝ t = x − (x−t)); criterio esatto: nessuna risonanza V(f)∩V(g)∩(ℂ×iℤ) | proposed — **decisione H0 (ℝ vs 𝕋) da portare all'utente al Gate 0/1** | promuovi se si sceglie 𝕋; elimina se H0 fissato su ℝ |
| RT-R2b | C4/P1 | R2 | quadro dei comportamenti di Oberst: componenti = moduli R/(P_i) (decomposizione primaria), A8 ⟺ esattezza di Hom(·,𝒜), E_int = ostruzione Ext¹ / quoziente ker L/(ker L∩Σker L_n) | proposed — contiene RT-1, gemella a coeff. costanti di RT-S1d; converge con il verdetto RT-R4a | promuovi se C4/P1 adottano "componente = fattore" |
| RT-R7a | Fase 4 / G3 / G7 / C3 | R7 | IST = log-simbolo non lineare: per equazioni integrabili (AKNS) i dati di scattering evolvono linearmente con la dispersione linearizzata ⇒ identificazione del termine dispersivo lineare e O(N) nel dominio spettrale | parked fino al Gate 4a (Fase 4) | promuovi se l'identificazione da una soluzione è dimostrata per KdV/NLS |
| RT-R7b | B3/D1/A6/P1 (Fase 4) | R7 | Cole–Hopf tropicale: per Burgers con φ=Σφ_i, u = Σ w_i u_i con pesi softmax w_i = φ_i/Σφ_j, E_int esplicito; per ν→0 (Maslov, Hopf–Lax) pesi → indicatori, E_int sugli shock | proposed — si salda con RT-S1a (TROP); versione non lineare di D1; **trovata indipendentemente da PR-C2c** (tropicalizzazione Cole–Hopf/Hirota, solitoni ultradiscreti box-ball: fusa qui) | promuovi in Fase 4 con stima di E_int in ν |
| RT-R7c | C3/G4/G7 | R7 | simmetria ⇒ non identificabilità: u invariante per una simmetria con caratteristica nel dizionario ⇒ dim ker 𝔾(u) ≥ 2 (1-solitone KdV: 3; 2-solitone: 1) | proposed → da raccordare con R4 (criterio G4) | promuovi se il criterio "u non invariante per sottoalgebre compatibili" si riconcilia con R4-T5 |
| RT-R1a | P2/C4/A8/D1 | R1 | MCA: separazione morfologica ℓ¹, min Σ_n ‖Φ_n*u_n‖₁ s.t. Σu_n = u, con cluster coherence (Donoho–Kutyniok 2013, errore ≤ 2δ/(1−2κ)); agisce solo su E_int^∥ | proposed — si coordina con RT-S1a/RT-S2b | promuovi se κ<1/2 calcolato per una coppia del ladder; elimina se κ≥1/2 per tutte le coppie L2/L3 |
| RT-R1b | P2.1/C2.3 | R1 | recupero per positività (T-sistemi) nella classe del calore: dato ≥0 ⇒ misura positiva di gaussiane, recupero esatto senza separazione (Schiebinger–Robeva–Recht 2018) | proposed / parked se il progetto non ammette ipotesi di segno | promuovi se si estende ad altre classi T-sistema |
| RT-D1 | C1/C1.0/C1.2/P2 | PR-C2d | C1 come somma di RKHS di Green: per ogni componente K_n = Green dell'operatore d'energia (= nucleo riproducente); dizionario K_𝒟=ΣK_n con norma inf-convoluzione (Aronszajn §I.6) = decomposizione L² regolarizzata | merged-into: RT-7 / C1.0 (coincide con R1-P4 e lo split ℓ² u_n = K_nK⁻¹u) | promuovi se H_{K1}∩H_{K2} caratterizzato per le coppie del catalogo |
| RT-D2 | C3.2/C2.70′ | PR-C2d | identificabilità = osservabilità: gramiano d'osservabilità ∫S(t)u0⊗S(t)u0 dt ↔ ker 𝔾(u) | proposed — candidata merge in RT-4/RT-R4a (sottospazio ciclico = spazio osservabile) | promuovi con teorema di equivalenza nel caso L2 |
| RT-R6a | II/E4 | R6 | via (a′): simbolo totale con ⋆-prodotto (Weyl / Kohn–Nirenberg) come versione tensoriale completa per coeff. variabili; raccordo BCH ↔ Moyal con R5 | proposed (atteso merge in RT-6) | promuovi se dà un invariante calcolabile non contenuto in D/DL |

## Triage del coordinatore per il Gate 1 (22/10/2026) — proposte all'utente, non ancora decise
Criteri (§1.6): serve G★/G★′? è analitica (k3)? è più economica o più forte della strada attiva? Kill criteria fissati sopra.
| id | proposta | motivazione |
|---|---|---|
| RT-1 / RT-R2b | **PROMUOVERE (attiva)** | G2 dimostrata su ℝ/convessi (R2-T2), coeff. variabili via LCLM (R2-T4); è la base di "componente = fattore" |
| RT-2 | **PROMUOVERE con restrizione** | log-simbolo additivo e O(N) dimostrati (R5-T2), ma solo per evoluzioni scalari del 1° ordine in t (PR-C2b P4/P5, R6-T8) |
| RT-3 (+S1i, S2d, S1c) | **PROMUOVERE** | criteri soddisfatti (R5: Wei–Norman globale per algebre risolubili, Dyson convergente per c∈L^∞+diffusione); S1c resta strato di definizione |
| RT-4 (+S1h, S2c, D2) | **PROMUOVERE** | ker 𝔾 = Ann(u)∩span (R4-T6), Prony ⟺ Waring (R6); S2c e D2 non hanno dato teoremi oltre RT-4 ⇒ fuse |
| RT-R4a | **PROMUOVERE** | enunciato astratto dimostrato nel caso commutativo (R4-T8); verdetto C3.3 confermato da R2, R6, PR-C2a; resta il kill criterion in L4 |
| RT-5 | **PARCHEGGIARE** | il tensore conserva solo il simbolo principale (R6-P1); utile come invariante geometrico |
| RT-6 (+R6a atteso) | **PROMUOVERE** | invarianti completi (R6-T1, T5) |
| RT-7 (+D1) | **PROMUOVERE come quoziente** | G6 vera come quoziente, isometria ⟺ sintesi iniettiva (R1) |
| RT-R3a | **PROMUOVERE** | base ortogonale di Fock pesato (R1-P11); estensione ad Airy aperta (PR-C2b Q2) |
| RT-S1a + S2b [TROP-L2] | **SCOUTING in Fase 3** | enunciato unico pronto (SCOUT-1 Addendum) ma non dimostrato; costo medio |
| RT-R7b (+PR-C2c) | **SCOUTING in Fase 4** | P6 di R7 dimostrata su Burgers; trovata indipendentemente da due agenti |
| RT-S2a | **SCOUTING in Fase 3** | identità esatta in N pezzi (SCOUT-2, R5) ma fuori dalle classi ker T_i; serve un principio di scelta di L₀ |
| RT-S1b | **SCOUTING breve** | la non-naturalità è coerente con R2-T3; da enunciare con precisione |
| RT-S1d | **FONDERE in RT-1/RT-6** a coeff. costanti; scouting a L1/L4 | coincide con la decomposizione primaria a coeff. costanti (R2, R6) |
| RT-S1e | **PARCHEGGIATA** fino a L1/L4 | nessun teorema a coeff. costanti |
| RT-S1f | **PARCHEGGIATA** fino a L1 | componenti solo settoriali |
| RT-S1g | **ELIMINARE per il core** (resta per la parte iperbolica) | non dà informazione per ellittiche/parabolic (kill criterion soddisfatto) |
| RT-R1a | **SCOUTING** | serve κ<1/2 su una coppia del ladder (R1-Q4) |
| RT-R1b | **PARCHEGGIATA** | richiede ipotesi di segno sul dato |
| RT-R2a | **DECISIONE UTENTE (H0)** | ℝ vs 𝕋 |
| RT-R7a | **PARCHEGGIATA** fino a Gate 4a | Fase 4 |
| RT-R7c | **FONDERE in RT-4** | ostruzione da simmetria = caso di R4-T5 con Z(u) finito su una componente |
Quota di esplorazione (§1.6): rotte non seme valutate in Fase 1 = 23; una eliminata con motivazione (RT-S1g per il core), 6 fuse, 5 parcheggiate.
| RT-S1a + RT-S2b [TROP-L2] — **esito scouting S-TROP (25/10)** | O1 | S-TROP | stima ‖E_int‖/‖u‖ = O(ε^γ) dal solo simbolo vale SOLO sulle facce dissipative (TROP-3, TROP-8); sulle conservative (KG, trasporto) nessuna stima uniforme (TROP-4) ed ε deve contenere T (TROP-5) | **merged-into: RT-2** come "corollario di regime" del log-simbolo (criterio di eliminazione fissato soddisfatto); versione per ramo di KG passata a S-II e S-P1 | work/SCOUT-TROP/VERDETTO.md, trop_checks 25/25 PASS; claim TROP-3…8 in attesa di S-CHECK |

## Decisione del coordinatore 25/10/2026 (sera)
- **RT-R1a (MCA / cluster coherence): MERGE-INTO C12-T5(c) / P2-T5, chiusa come strada autonoma.** Criterio formale soddisfatto (κ = 0 < 1/2 su τξ) ma il contenuto si riduce alla scelta di un rappresentante nell'ambiguità finita 𝓘 = 𝓗₁∩𝓗₂, già data dallo split di energia minima; a livello dei termini MCA non si applica (work/P2/PROOF_PACKAGE.md P2-T5, P2-P7).
- **RT-S2a (Faddeev–Lippmann–Schwinger): MERGE-INTO RT-2** (criterio scritto prima della valutazione, work/P3/PROOF_PACKAGE.md §7.0). (a) vale (E^add = Σ_i E^{(i)}); (b) fallisce in L² (risonanza secolare del trasporto); contributo netto P3-T6(i): decomposizione di bilancio u^{(i)} = ∫a_i(∂_x)u, esatta e continua in H^m(Ω) → aggiunta come quadro (f) di P1-D3. Riapertura solo se P3-Q4 (convergenza su scala di spazi) si risolve. In attesa dell'audit di S-CHECK-5 e di un kill-argument sul verdetto.
- **RT-R4a (restrizione 𝓛 → End Z(u) / sintesi spettrale): MERGE-INTO RT-4** (kill criterion scattato con P4-C1: in L4 l'algebra di Weyl è semplice, la restrizione è sempre iniettiva e non identifica — controesempio u = eˣ, 𝓛 = span{1,∂}; nel caso commutativo l'iniettività ⟺ Ann(u)∩𝓛 = 0 è una tautologia = Gram C3-L1). La lettura spettrale corretta (P4-T2 modulo ciclico, P4-T3 Padé 2D) va sotto RT-4. Audit S-CHECK-6: nessuna obiezione.
- **RT-S2a — REVISIONE della decisione precedente (25/10 sera, dopo S-CHECK-5):** il MERGE-INTO RT-2 NON è sostenuto (kill-argument FAIL: P3-T6(vi) "∂_t è l'unica scelta equivariante non degenere" è FALSO — famiglia L₀^θ = ∂_t − θΣa_i; criterio (b) non testato a coefficienti variabili). **Nuovo stato: PARCHEGGIATA.** P3-T6(i), (iv), (v) entrano in RT-2 come quadro (f) solo a coefficienti costanti, con il principio di bilancio termine per termine (∂_t u^{(i)} = a_i u, u^{(i)}(t₀) = 0) dichiarato come principio di selezione. Riapertura: criterio (b) a coefficienti variabili o P3-Q4.

## Gate 4a — decisioni dell'utente (26/10/2026) su proposta GATE4A.md v2 §3
| strada | stato |
|---|---|
| **RT-TERM** (nuova): E_int non lineare nel senso A9 + errore di splitting; include MON/splitting (Kružkov, Brezis–Pazy), forma normale NF-1, Carleman come strumento | **ATTIVA** (S4-TERM, prioritaria) |
| **MODREL** (Hammerstein, Syz_f(u)) + linguaggio F4-ALG + MON-1 | **ATTIVA** (S4-ID) |
| RT-R7a (IST) ristretta a 𝓗 (+ R7c, Hirota, Miura, Darboux) | **ATTIVA come caso di S4-ID e lemmi di S4-INTEG** |
| RT-R7b (Cole–Hopf tropicale, + WIENER), Carleman + NF, F4-ALG | **LEMMI** (S4-INTEG / strumenti di S4-TERM), non strade autonome |
| MON/splitting | **RIAMMESSA** (dentro RT-TERM; scarto precedente errato, DEVIL-4 O5) |
| Koopman | PARCHEGGIATA (riaprire con NF: le autofunzioni portano il termine non lineare) |
| PAINLEVÉ, NLSPEC, HAANTJES | PARCHEGGIATE (trigger nei verdetti F4-HOR) |
| SPLIT-f come strada | ELIMINATA (SPLIT-L1, SPLIT-L2 restano lemmi) |
| S4-LIFT autonoma | non avviata |

## Gate 6 — strade per le Fasi 8–11 (auto-approvato per delega dell'utente, 26/10/2026, revocabile; registrato il 27/10/2026)
Fonte: `research/SYNTHESIS-2.md` §4, `research/F6-HOR/VERDETTO.md` §2, `GATE6.md`.
| strada | contenuto | stato | sessione |
|---|---|---|---|
| **RT-SYS** | Morita + Malgrange–Oberst; SYS-T1/N1/T0/S1; gauge (G-T2, SYS-N3) | **ATTIVA** | S8-SYS |
| **RT-IDV** | identificazione strutturata VAR-T1 + confine VAR-N1 | **ATTIVA** | S8-VAR |
| **RT-ODE-GAL** | Weyl / Loewy / Galois per ODE (VAR-T2, VAR-T6) | **ATTIVA** | S8-VAR |
| **RT-NA** | propagatori non autonomi, VAR-P9/T10, CONV-T7 | **ATTIVA** | S8-VAR, S8-CONV |
| **RT-ENC** | trasformazione di Volterra + Darboux/Crum + puntuale/gauge | **ATTIVA** | S8-ENC |
| **RT-DICT** | U1–U4 + N1 + misfit MF1–MF3 + regole R1–R6, R-STOP + I-LIM | **ATTIVA** | S8-DICT |
| **RT-CONV** | CONV-T1…T6, CONV-P8, rumore, bordo e dimensione | **ATTIVA** | S8-CONV |
| NS-EQUIV, NS-GALDAR (non-seme) | equivalenze e Galois–Darboux | **FUSE in RT-ENC** | S8-ENC |
| NS-EXPALG (non-seme) | non linearità non polinomiali come variabili differenziali (sine-Gordon, e^u) | **FUSA in RT-DICT** | S8-DICT |
| RT-5 | via (a) tensore simbolo | **RIAPERTA → RT-SYS** | S8-SYS |
| RIGID + STOKES | — | **RIAPERTE → RT-IDV** | S8-VAR |
| Mori–Zwanzig; RT-R2a (bordo periodico, H0 intatto) | — | **RIAPERTE → RT-CONV** | S8-CONV |
| Faddeev; POLE; gamblets | strumenti | **RIAPERTE → RT-ENC** | S8-ENC |
| PAINLEVÉ; F4-ALG | strumenti (N1 non lineare) | **RIAPERTE → RT-DICT** | S8-DICT |
| MICRO (Foldy–Wouthuysen) | — | **RIAPERTA → RT-SYS / RT-ENC** | S8-SYS, S8-ENC |
| MPUM (Willems) | confronto con Schindelar–Levandovskyy–Zerz 2011 | **RIAPERTA → RT-SYS / RT-CONV** | S8-SYS, S8-CONV |
| Weyl per PDE; Sturm–Liouville inverso (dati spettrali); U3(a) nuclei; U5; omogeneizzazione; operatori d'onda; CONV-BORDO; Hartogs 1+d | — | PARCHEGGIATE | — |
| RT-R1b, Koopman (DMD = regressione, vincolo no-ML), NLSPEC, HAANTJES, MON, NAT, MOB | — | restano PARCHEGGIATE | — |
| consistenza statistica come metodo (no-ML); SPLIT-f, probabilità libera, ICA; quiver, microlocale oltre Char, Lie/Olver | — | ELIMINATE (o fuse) | — |

## Gate 8 — strade dopo le prove di Fase 8 (auto-approvato per delega dell'utente, 27/10/2026, revocabile; dettagli in GATE8.md §2)
| strada | stato | nota |
|---|---|---|
| RT-SYS | ATTIVA (ridotta) | Maxwell Q6, II-T2(b′), Q-S8SYS-1; CIT Oberst 1990/1993 prerequisito per ℝ^n |
| RT-IDV | ATTIVA | VAR-Q10, Q17, Q18 |
| RT-ODE-GAL | ATTIVA (solo C3-Q2 generale) | VAR-C3Q2-open |
| RT-NA | PARCHEGGIATA | trigger VAR-Q8, Q11, Q18 |
| RT-ENC | PARCHEGGIATA (strada); lemmi a RT-DICT e RT-IDV | trigger ENC-Q4, ENC-Q10 |
| RT-DICT | ATTIVA | Fase 9: R6, ILIM, RANGO; DICT-Q3, Q4, ILIM-Hs |
| RT-CONV | ATTIVA | contratto CONV-T7 (Magnus condizionato) |
| RT-5, RIGID, STOKES, CONV-BORDO | PARCHEGGIATE | non toccate in F8 |
| Mori–Zwanzig, RT-R2a, POLE, gamblets | ELIMINATE | criteri FALSI o solo CON-FONTE; i lemmi restano |
| Faddeev, MICRO/FW, MPUM, NS-EQUIV, NS-GALDAR, NS-EXPALG, F4-ALG | FUSE | vedi GATE8.md §2 |
| PAINLEVÉ | STRUMENTO | DICT-R4 |
