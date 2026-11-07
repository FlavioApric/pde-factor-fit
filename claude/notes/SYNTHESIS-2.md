# SYNTHESIS-2 — Fase 6 (scouting): Problema 1, Problema 2, convergenza, dizionario universale
Coordinatore (sessione fork), 26/10/2026. Fonti: `research/F6-{SYS,VAR,ENC,DICT,CONV,HOR}/VERDETTO.md` e `NOTE.md`; `research/DEVIL/ATTACK-6.md` (kill-argument: **FAIL** sul pacchetto come proposto, **PASS-WITH-FIXES** con F1–F10: tutti i fix sono applicati qui sotto); `research/CIT-AUDIT/AUDIT-6.md` (vedi §7). Stati: **nessun enunciato di Fase 6 è DIMOSTRATO**; "prova scritta" = prova completa non auditata da S-CHECK; "candidato" = enunciato senza prova completa. Le obiezioni critiche O1 e O2 di DEVIL-6 sono state verificate a mano dal coordinatore (u = t − x²: una legge u_t + a u_x + b u = 0 in (0,0) dà 1 = 0; tempi dipendenti da ξ = moltiplicatori di Fourier, non flussi dei termini).
**Nota del Gate 8 (27/10/2026).** Corrette al Gate 8 le frasi FALSE indicate da DEVIL-8 (research/DEVIL/ATTACK-8.md, O1–O3): ENC-N1, "le eccezioni quadratiche cambiano il tempo", F5 su cos t = 0. Backup: SYNTHESIS-2_preGate8_backup.md. Decisioni in GATE8.md.


## 0. Risposte alle quattro domande dell'utente (forma corretta dopo DEVIL-6)
1. **Dirac, coefficienti matriciali.** A coefficienti costanti un operatore con λ_α ∈ Mat_k(ℂ) è una matrice di operatori commutativi: per Morita e Malgrange–Oberst l'oggetto canonico di Gate 3 diventa M_u = R^{1×k}/Ann(u) (non più ciclico). Nessuna algebra non commutativa nuova serve a coefficienti costanti. Da un dato ψ in una base fissata il sistema è identificato a meno di equivalenza **a sinistra** (D ~ VD, V ∈ GL(R)); **in forma hamiltoniana (iψ_t = (α·p + βm)ψ) α e β sono identificati esattamente** (fix F9). Criterio di identificazione SYS-T1 (candidato, verifica su Oberst 1990 obbligatoria, fix F8), ostruzioni di zoccolo SYS-N1 e di molteplicità; Dirac = radice di Klein–Gordon con proiettori polinomiali (SYS-S1). Gauge: con dati invarianti (|ψ|², correnti) solo l'orbita (F, più olonomie se Ω ha buchi); con il dato complesso completo il gauge non crea ambiguità: l'ostacolo vero è il conteggio equazioni/incognite (SYS-N3).
2. **Coefficienti variabili / non autonomi (Schrödinger).** Due facce (fix F1):
   - (a′) **identificazione intrinseca vuota**: in una classe di coefficienti ∂-chiusa grande, ogni u senza zeri ha un annullatore di rango 1 (VAR-N1): l'esistenza di una legge non spiega nulla;
   - (b′) **identificazione strutturata** (senso ID-res): a forma dell'equazione fissata (es. iψ_t = −ψ_xx + V(t,x)ψ), **fuori dalle fasce di silenzio, in (SF)** (classe delle soluzioni forti di S8-VAR; ATTACK-8 O17), V è identificato esattamente, anche se dipende dal tempo, ⟺ la mappa residuo ρ_u(Q) = Qu/u è iniettiva sulla classe (VAR-T1). Per V(t,x) il criterio è int Z(u) = ∅ (V continuo) oppure |Z(u)| = 0 (V ∈ L^∞) (VAR-T1(c)); con int Z(u) ≠ ∅ c'è una fascia di silenzio e la forma senza questa ipotesi è FALSO (VAR-T1(c)-F, serie di Tychonoff): V = (iu_t + u_xx)/u su {u ≠ 0}, con modulo di Lipschitz da C^{1,2} sui compatti dove |u| ≥ κ (VAR-P3: stima di modulo, **non** certificato di robustezza; ATTACK-8 O8, GATE9 O31). Stati stazionari: solo V − E se il dato è noto **a meno della fase temporale globale** (VAR-P4 = ENC-N2(a) con modello di dato dichiarato).
   - ODE a coefficienti razionali: analogo esatto di C3-T1 via ciclicità sotto il gruppo di Galois differenziale (VAR-T2). PDE nell'algebra di Weyl: C3-Q2, C12-Q5 aperti.
   - **Encoder analitico che rimuove V** (Problema 1 come "rumore"): per V(x) in 1D esiste sempre l'operatore di trasformazione di Volterra (Povzner–Levitan–Marchenko) che intreccia −∂²+V con −∂², valido per Schrödinger, calore, onda (ENC-1); encoder locali solo in classi ristrette (vedi tabella §3); per V(t,x) generico nessun encoder che commuti con ∂_t (ENC-P0(b), (b)^cl); le eccezioni quadratiche in x si trattano con trasformazioni metaplettiche e di gauge, e il tempo va riparametrizzato solo se α ≢ 0 (forma esistenziale; Avron–Herbst ha θ = id). L'encoder **cieco** (costruito dai dati) non dà guadagno identificativo: ENC-N1′ è un lemma di riduzione all'identificazione congiunta di (q, u); la forma "cieco ⟺ identificabilità congiunta" (ENC-N1) è FALSO. [Gate 8, O1–O2]
3. **Convergenza a un'equazione differenziale** — sì **nel limite, mai certificata** (fix F9):
   - (C1) CONV-T1: con il jet che cresce la regola del grado minimo dà P esatto da un passo finito in poi, senza conoscere il grado; il tempo di convergenza non è limitato da nessuna funzione del grado e nessun dato finito dice che è stato raggiunto (C3-P1). Rumore: identificazione discontinua ovunque (CONV-T3); stabile solo a livello fissato con margine spettrale (CONV-T4), consistente con la regola di discrepanza sotto una soglia non calcolabile (CONV-T5).
   - (C2) Località: esiste una legge differenziale ⟺ il simbolo è algebrico sullo spettro di u (CONV-T6). Tricotomia: legge locale / legge locale solo con variabili aggiunte (Caffarelli–Silvestre, memoria, **ritardo** = trasporto ausiliario, fix F4) / nessuna legge. CONV-T2: nessuna regola, nemmeno non calcolabile, decide nel limite se esiste una legge (Ann(u) = 0 o no) — DEVIL-6 ha ricontrollato il passo cardine (ii).
   - (C3) Parti iterative: contratto CONV-T7 — ogni passo è (A) esatto, (B) convergente con maggiorante esplicito (Dyson–Phillips, Magnus con ∫‖A‖ < π, Trotter–Kato), o (C) senza garanzia; la catena garantita usa solo A e B.
4. **Operatori fuori catalogo / dizionario universale** (fix F3: niente "tiene conto di tutto" come teorema unico). Ciò che è vero:
   - per **ogni classe** (locali lineari U1, locali non lineari U2, non locali per simboli/memoria/ritardo U3, sistemi U4) esiste un dizionario numerabile esplicito che la **approssima** in una topologia dichiarata, con velocità dove la regolarità lo consente;
   - a ogni livello finito c'è un **certificato di misfit** calcolabile (Gram/Hahn–Banach; forma debole robusta al rumore) e una **migliore approssimazione con stima**; il misfit si certifica con dati finiti, il fit no (Teorema A);
   - l'identificazione è **relativa** al livello, e nel limite (I-LIM = CONV-T1 + ramo approssimato di Tikhonov) solo sotto l'ipotesi d'unicità (H1);
   - teorema negativo N1: nessun dizionario numerabile rappresenta esattamente più di un insieme magro di operatori (Baire), nessun dato finito certifica, e la u generica non soddisfa alcuna equazione del dizionario. La sola completezza tipo Hilbert (U5, già nota) non dà identificazione — conferma l'osservazione dell'utente: il contenuto sta nella **filtrazione** e nel certificato, non nella chiusura.

## 1. Tabella di raccordo (fix F9)
Modelli di dato: **DM1** formula/EP, **DM2** jet in un punto, **DM3** u noto esattamente in H^m(Ω) (= M1–M3 di Fase 3); **DM-φ** dato a meno della fase temporale globale; **DM-inv** dati invarianti di gauge. I teoremi di misfit di F6-DICT §3 sono rinominati **MF1–MF3** (non M1–M3). L'ipotesi d'unicità di I-LIM è **(H-ID)** (non (H1)). E_int è sempre quello di A9 (NOTAZIONE v3); il "difetto di coniugazione" di F6-ENC si chiama **E^conj** (fix F6).

| enunciato | scout | dominio | dato | stato | note |
|---|---|---|---|---|---|
| SYS-T1, SYS-N1, SYS-T0, SYS-S1 | SYS | Ω connesso (S1: convesso) | DM3 | prova scritta / candidato (T1) | F8: confronto con Oberst 1990 obbligatorio; obiettivo S8: criterio d'esistenza (zoccoli ≤ 1) |
| SYS-E (ex "P1-T5 no") | SYS | — | — | **"P1-T5 non si applica ai sistemi" = FALSO** (F2) | P1-T5 si applica a Dirac 1+1 (orbita aggiunta infinita su ℂ); Euler ZXZ = moltiplicatore non locale (U3) |
| G-T2, SYS-N3; G-T0 | SYS | H¹_dR(Ω) | DM-inv / DM3 | prova scritta; G-T0 = osservazione | |
| VAR-N1 (= N1(vi)(a′)) | VAR/DICT | — | DM3 | prova scritta | identificazione intrinseca vuota |
| VAR-T1 (= N1(vi)(b′)), VAR-P3, VAR-P5 | VAR | J ∖ int X_0 | DM3 | prova scritta | zeri di u: Holmgren (V analitico) candidato |
| VAR-P4 = ENC-N2(a) | VAR/ENC | — | DM-φ | prova scritta | con fase globale osservata il dato identifica q |
| VAR-T2, VAR-T6 | VAR | ODE in ℂ(x)[∂] | DM1/DM3 | prova scritta + fonte | van der Put–Singer, n. da verificare |
| VAR-C7 | VAR | LPDO | — | CON-FONTE (Landau 1902) | etichetta corretta: "unicità di Jordan–Hölder per elementi falsa per LPDO"; non falsifica C12-T1′ (F10) |
| VAR-P8 (+ ENC-L1, = R5-P7) | VAR/ENC | — | — | prova scritta (V polinomiale) | riscritto (F5): Wei–Norman finito ⟺ deg V ≤ 2; ma E_int esplicito esiste anche per Pöschl–Teller (Darboux) |
| VAR-P9, VAR-T10, VAR-P11, VAR-P12 | VAR | — | — | prova scritta / composizione di noti | in H = −∂² + x² la parola chirp·libero·chirp si rompe esattamente a cos t = 0 e si attraversa con la lente (VAR-T10; AUDIT_S8-VAR, VAR-6); F5 di DEVIL-6 è ritirata: \|t\| < π vale per H/2 [Gate 8, O3] |
| ENC-1 (trasformazione di Volterra) | ENC | rettangolo simmetrico, dipende da x_0 | — | prova scritta + fonte | ipotesi dentro l'enunciato (F10) |
| ENC-T2 | ENC | — | — | prova scritta, **lemma "a q noto"** (F6) | circolare per B1 se q non è noto |
| ENC-P0 | ENC | V(t,x) | — | DIMOSTRATO (P0(b)); sintesi rev. 1 FALSO | per V(t,x) generico nessun encoder indipendente da t; eccezioni quadratiche: metaplettiche + gauge, θ ≠ id solo se α ≢ 0 (forma esistenziale) [Gate 8, O2] |
| ENC-N1 | ENC | — | — | FALSO (ENC-N1); ENC-N1′ DIMOSTRATO come lemma di riduzione | nessun guadagno identificativo dalla costruzione cieca [Gate 8, O1] |
| U1+N0, U2, U3(c)+N2, U3(d), U4 | DICT | per classe | — | prova scritta | N3 ristretto ai sistemi ODE razionali a dim. finita su ℝ; il ritardo è un sistema locale aumentato (F4) |
| N1(i)–(v), Teorema A, MF1–MF3, B2, regole R1–R6, R-STOP | DICT | — | DM3 | prova scritta | N1(vi) sostituito da (a′)/(b′) (F1) |
| I-LIM = CONV-T1 + ramo Tikhonov | DICT/CONV | — | DM2/DM3 | prova scritta | sotto (H-ID) |
| CONV-T1…T6, CONV-P8 | CONV | 1+d | DM2/DM3 | prova scritta | T5: rumore in norma H^d; in L² serve il ramo hölderiano; soglia δ₀(u) non calcolabile |
| CONV-T7 | CONV | — | — | contratto (A/B/C) | entra nel passo 7 di ALGORITMO_ESTESO |
| NS-EQUIV, NS-GALDAR, NS-EXPALG, HOR-P1, HOR-O1, O-H1 | HOR | — | — | CON-FONTE da verificare / V-ex / candidato | HOR-P1: dichiarare la normalizzazione (atomo costante ⇒ nucleo affine ≥ 1) |

**Repliche non indipendenti** (fix F9): il fatto "potenziale dipendente da u" (VAR-N1, ENC-N2(b), HOR-O1/O-H1, ex-DICT N1(vi)) e la classificazione degli encoder (ENC-3/K1, NS-EQUIV, NS-GALDAR) sono **lo stesso fatto** ricomunicato via inbox: contano una volta.

## 2. Teoremi negativi (il confine, dopo i fix)
N1(i) Baire; N1(ii) nessun certificato finito / Teorema A; N1(iii) non monotonia per dati EP; N1(iv) solo nel limite + CONV-T2; N1(v) u generica senza legge; VAR-N1 (intrinseca vuota); N2 (simboli: perdita di ε necessaria); N3 (ristretto, F4); SYS-N1, SYS-N3; ENC-P0; CONV-T3 (discontinuità ovunque); VAR-P8 (nessuna algebra finita oltre il quadratico); S-O1 (la struttura fattoriale non regge l'approssimazione).

## 3. Tabella unica degli encoder (fix F7)
| tipo di encoder | dove esiste | stato |
|---|---|---|
| integrale di Volterra (GLM / Povzner–Levitan) | ogni V(x) in 1D, rettangolo simmetrico | prova scritta + fonte |
| differenziale (Darboux/Crum) **modulo costanti** | potenziali di catene di Darboux, **solitoni inclusi** (Pöschl–Teller senza riflessione); "solo se" = ENC-K1, valido solo per V razionale → 0 all'infinito (Duistermaat–Grünbaum 1986; falso senza, CIT-AUDIT-6), probabilmente già noto | CON-FONTE da verificare; **niente "decidibile via Kovacic"** (Kovacic decide a λ fissato) |
| puntuale + gauge (lens, Avron–Herbst, Niederer) | V(t,x) quadratico in x (θ ≠ id solo se α ≢ 0; Avron–Herbst ha θ = id) [Gate 8, O2] | CON-FONTE da verificare; su Ω limitato solo parziale |
| omogeneizzazione / media | V rapidamente oscillante (approssimato) | parcheggiato come approssimazione |
| operatori d'onda | tutto lo spazio, t → ∞ | parcheggiato (fuori dal modello Ω limitato) |
La definizione (E2) di encoder va allentata "modulo costanti" (q costante non ha intertwiner differenziale stretto).

## 4. Strade (proposta per ROUTES.md, da registrare dopo REPORT_FINALE di Fase 5)
PROMUOVI: RT-SYS (Morita + Malgrange–Oberst, SYS-T1/S1, gauge), RT-IDV (identificazione strutturata VAR-T1 + confine VAR-N1), RT-ODE-GAL (Weyl/Loewy/Galois per ODE), RT-NA (propagatori, VAR-P9/T10, CONV-T7), RT-ENC (trasformazione di Volterra + Darboux + puntuale), RT-DICT (U1–U4 + N1 + misfit + regole + I-LIM), RT-CONV (CONV-T1…T6). Non-seme promosse da F6-HOR: NS-EQUIV (→ RT-ENC), NS-GALDAR (→ RT-ENC), NS-EXPALG (→ RT-DICT). Riaperte da F6-HOR (12): RT-5 → RT-SYS; RIGID+STOKES → RT-IDV; Mori–Zwanzig → RT-CONV; Faddeev → RT-ENC; PAINLEVÉ, F4-ALG → RT-DICT; POLE, gamblets → RT-ENC; RT-R2a → RT-CONV; MICRO (Foldy–Wouthuysen) → RT-SYS/RT-ENC; MPUM Willems → RT-SYS/RT-CONV. PARCHEGGIA: Weyl per PDE, Sturm–Liouville inverso (dati spettrali fuori dal modello), U3(a) nuclei, U5, omogeneizzazione, operatori d'onda, CONV-BORDO, Hartogs 1+d; restano parcheggiate RT-R1b, Koopman (DMD = regressione, vincolo no-ML), NLSPEC, HAANTJES, MON, NAT, MOB. ELIMINA: consistenza statistica come metodo (vincolo no-ML); SPLIT-f, probabilità libera, ICA (confermate); quiver, microlocale oltre Char, Lie/Olver (fuse o eliminate).

## 5. Bersaglio proposto G★″ (per PROBLEM.md v3, dopo REPORT_FINALE)
Estendere G★′ e G★′-NL lungo la scala **L6** sistemi a coefficienti costanti (Dirac, Maxwell, Lamé) → **L7** coefficienti variabili V(x) (ODE prima, poi PDE) → **L8** non autonomi V(t,x) → **L9** non locali (simboli, memoria, ritardo, frazionari) → **L10** dizionario universale filtrato, con:
1. identificazione: SYS-T1 (+ criterio d'esistenza), VAR-T1/VAR-T2 con confine VAR-N1, versione a dizionario con MF e I-LIM;
2. scomposizione: SYS-S1, VAR-T6, ostruzione S-O1; C12-Q5 aperto;
3. termini ed E_int (A9): SYS-E (P1-T4 sì, P1-T5 sì per Dirac), VAR-P8 riscritto, VAR-P9, Pöschl–Teller esplicito;
4. encoder analitico (Problema 1, B2): tabella §3, ENC-T2 a q noto, ENC-P0(b), ENC-N1′ (lemma di riduzione; ENC-N1 FALSO) [Gate 8];
5. convergenza: CONV-T1…T7, nel limite e mai certificata;
6. complessità e impossibilità: N1, N2, N3 ristretto, CONV-T2/T3, SYS-N1/N3, ENC-P0.

## 6. Obiettivi per le sessioni di Fase 8 (dai fix e dalle domande aperte)
S8-SYS: verifica su Oberst 1990; criterio d'esistenza con zoccoli ≤ 1; SYS-S1 su Ω non convesso; II-T2(b′) derogatoria; Lamé n = 3. S8-VAR: zeri di u (Holmgren / unicità laterale per V ∈ L^∞); C3-Q2 in A_2. S8-ENC: ENC-K1; NS-EQUIV su Ω limitato; E_int A9 per V. S8-NA: VAR-T10 con oscillatore corretto; Magnus per illimitati. S8-DICT: liscezza di F in U2 (KMS 18.16); N1 non lineare (F4-ALG); kill-argument su N1. S8-CONV: CONV-T5 in L²; legame con P3-T3 (CONV-Q6). S8-NLOC: frazionari e ritardo come sistemi aumentati. S8-NOISE/DIM: CONV-P8 e l'ambiguità di scomposizione in 1+d.

## 7. CIT-AUDIT-6
Fonte: `research/CIT-AUDIT/AUDIT-6.md`. Nessuna fonte inesistente; cinque problemi di contenuto, ~20 correzioni bibliografiche, rischi di novità. Recepiti così:
- **Duistermaat–Grünbaum 1986** (CMP 103, 177–240): solo V razionale **che tende a 0 all'infinito**. NS-GALDAR ed ENC-K1 vanno ristretti a questa ipotesi; senza, falsi (Oblomkov: crescita quadratica; Gibbons–Veselov: sestica). ENC-K1 probabilmente già noto (Duistermaat–Grünbaum, Wilson, Andrianov–Sokolov 2003): declassato a CON-FONTE da verificare.
- **Moan–Niesen 2008**: il raggio π è per matrici **reali**; per operatori limitati su spazi di Hilbert (Schrödinger) citare **Casas 2007** (J. Phys. A 40, 15001–15017). Corretto in CONV-T7 e VAR-T10.
- **Prenter 1970**: solo spazi di Hilbert; U5 su Fréchet si appoggia a Chen–Chen/Boyd–Chua (U5 resta parcheggiato e noto).
- **Einkemmer–Ostermann 2015**: riduzione d'ordine per Dirichlet **non omogeneo** (CONV, legame con P3-T3 resta CONV-Q6).
- **Slovák**: primo Peetre non lineare = Slovák 1987 (atti di Brno); 1988 lo generalizza.
- **Bluman–Shtelen 1996** confermato: equivalenza puntuale alla libera ⟺ V = a(t)x² + b(t)x + c(t); esistono V non quadratici equivalenti con trasformazioni **non locali** ⇒ "solo quadratico" vale solo per gli encoder puntuali (tabella §3 già così).
- Peetre 1959/60 e KMS 19.1/19.3/19.7/19.10 confermati sul testo.
- Correzioni dei dati: Boyd–Chua pp. 1150–1161; Allaire–Vanninathan DCDS-B 6 (2006) 1–16 (DOI sbagliato nella voce); Bagrov–Samsonov titolo; Finkel et al. JMP 40 (1999) 3268–3274; Popovych et al. Acta Appl. Math. 109 (2010); Malgrange Sém. Bourbaki exp. 246; Povzner pp. 3–52; arXiv:2107.01588 = Fazzi–Markovsky; Kravchenko–Torba (tre autori); Willems Part II per MPUM; voce Holmgren mancante in F6-VAR. Da recepire nei sources.bib in Fase 8.
- Numeri di teorema **non verificati**: Hörmander I 2.3.4/4.2/5.2.1, III 18.1.13; Oberst "Thm 2.54"; Marchenko cap. 1; Engel–Nagel III.4.8–4.9; Pinkus; Adams–Fournier; Engl–Hanke–Neubauer; Kelly; Pazy; van der Put–Singer; Boyer 1974 (pagina in conflitto).
- **Rischi di novità**: Oberst 1990 non letto ⇒ SYS-N1/SYS-T0 rischio alto, SYS-T1 medio (fix F8 confermato: verifica obbligatoria); **prior art nuovo**: Schindelar–Levandovskyy–Zerz, J. Symbolic Comput. 46 (2011) 1189–1204 (MPUM e VMPUM a coefficienti variabili per dati polinomiali-esponenziali) — da confrontare con SYS-T1 e VAR-T2 in S8-SYS/S8-VAR.
