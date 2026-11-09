# FASI_ALL — report (edizione completa, fasi 0–10)

## Deliverable
Quattro documenti in tutto. I primi due esistevano già e non sono stati toccati.

| # | file | pagine | contenuto |
|---|---|---|---|
| 1 | `../FASI05/paper_fasi05.pdf` | 72 | paper, fasi 0–5 |
| 2 | `../FASI05/dimostrazioni_fasi05.pdf` | 116 | catalogo delle dimostrazioni, fasi 0–5 |
| 3 | `paper_tutte_le_fasi.pdf` | 117 | paper, fasi 0–10 (Parte I: cap. 1–10; Parte II: cap. 11–18) |
| 4 | `dimostrazioni_tutte_le_fasi.pdf` | 261 | catalogo, fasi 0–10: Parte I A1–A31, Parte II A32–A53, Parte III B1–B72, Parte IV B73–B155 + 43 schede-elenco |

Build: `pdflatex dimostrazioni_tutte_le_fasi.tex` e `pdflatex paper_tutte_le_fasi.tex`, due volte ciascuno (riferimenti incrociati xr-hyper in entrambe le direzioni). Stile: `preamble_all.tex` (= preamble05, regole «oro» in memoria). Il grafo `graphify-out/` è stato usato per le dipendenze delle fasi 0–5 (tiers.md, già in FASI05) e per orientarsi; per le fasi 6–10 il grafo contiene pochi nodi di claim, quindi la scelta dei risultati portanti si è basata sul ledger (righe F8–F10, «Decisioni di stato del Gate 8») e sui passi di ALGORITMO_ESTESO che li citano.

## Cosa contiene di nuovo
- **Paper**, cap. 11–18: sistemi e gauge; coefficienti variabili; convergenza e rumore; encoder analitico; dizionario universale; cosa ha cambiato la Fase 10; algoritmo esteso (contratto per passo); limiti, falsi e aperti di tutto il progetto. Cap. 1–10 = FASI05, con: roadmap e abstract aggiornati, due riquadri di rimando alla Fase 10 nei cap. 7 e 8.
- **Catalogo**, Parte II (22 schede con prova): SYS-EX, SYS-C1, SYS-S1 (+controesempio), H-DIRAC; VAR-N1/T1(a), VAR-T1(b) con Carleman, VAR-T1(c) con Tychonoff, VAR-P3, VAR-P4; CONV-L1/T1, CONV-T2/T2′, CONV-T3/T4/T5; ENC-1/U1, ENC-C1, ENC-P0(b), ENC-N1′; DICT-U1, DICT-N1, DICT-A/MF, DICT-GR/I-LIM; S10A-T1 (P1-Q6) e S10A-P1 (buchi). Parte IV: 7 schede con prova (SYS-R1/T0, SYS-E1–3, LAME-3, G-T2, SYS-N3, VAR-P5, ENC-K0) e 108 schede-elenco.

## Correzioni che prevalgono sulle fasi 0–5 (Fase 10)
- P1-Q6 come scritto è FALSO (reazione–diffusione); forma corretta: ≥ 2 termini di grado ≥ 1.
- P2-Q1 falso come enunciato universale; densità falsa su domini con buchi (Laplaciano sull'anello); estensione di OPF5B-T1 ai non convessi FALSA.
- C12-P7 «chiusa ma non densa»: esempio differenziale sull'anello.
- Altri FALSI delle fasi 6–10 elencati nel cap. 19.

## Copertura onesta
- I pacchetti delle fasi 6–10 contano circa 160 000 parole (più ~110 000 di audit). Ho riscritto in forma di scheda **105 risultati** (22 in Parte II + 83 in Parte IV: B73–B155). Le **43** schede-elenco rimaste non hanno prova scritta perché non ce n'è una nei pacchetti: definizioni, risultati da fonte citata non letta (ALG-TK, ENC-K1, GAM-O1, DICT-AX), osservazioni (G-T0), aperti (GT-u, ENC-Q4/Q10 lettura DM3), falsi già smentiti in altre schede, controlli numerici (EX10, DICT-2KINK), formalizzazione Lean, e i casi che rimandano ad altre schede. Per i punti aperti le schede riportano la riduzione e ciò che manca. La Parte IV delle fasi 6–10 non è un'equivalenza con la parte 0–5 (103 prove complete).
- Le prove riscritte sono trascrizioni ristrutturate dei pacchetti; non sono state ri-auditate. Le etichette «proved» seguono il ledger (audit S-CHECK-F8/F10), non la riscrittura.
- Passaggi dichiarati *condensed* perché non li ho letti nel pacchetto per intero: A43 (soglia δ₀ non minorabile, costruzione di u′), A48 (N0, direzione ⇒), A50 (parte iii). Nelle schede dove un passaggio era più dettagliato del pacchetto ho tolto le parti ricostruite senza fonte.
- Ho letto per intero i pacchetti S10-OPEN-B, S10-OPEN-C, S10-COL e S10-OPEN-A §1–4 (con gli audit rev2), e le sezioni di S8-SYS (SYS-T1, G-T0), S8-VAR §2.2, S8-ENC §4 e S8-CONV §4.3/§5.3 che servivano alle nuove schede B124–B155. Non ho letto per intero S8-VAR §3–5, S8-ENC §6–9, S8-CONV (altre sezioni), S10-INT; i risultati corrispondenti restano nelle schede-elenco.
- Le nuove schede B124–B155 sono trascrizioni ristrutturate, non ri-auditate; gli stati sono quelli proposti dai pacchetti (prova scritta, non auditata) e dall'audit dove citato. Le pagine nuove sono state controllate a vista solo in parte (due pagine, B124 e B132–B133). Non incluse: le righe del ledger, le cronologie RIPRESA e BOARD, gli script SymPy, le domande aperte OP-* delle fasi 1–5.
- Fase 11 come fase di ricerca (audit proof-checker, audit citazioni, kill-argument sul testo finale) **non è stata eseguita** su questo testo.
- Non incluso: catalogo di ~60 equazioni, sorgenti Lean.
- Problemi aperti: nessuno chiuso da questo lavoro; sono elencati nel cap. 19 (voci di PROBLEMI_APERTI).

## Verifica
- Entrambi compilano senza errori e senza riferimenti non definiti. Overfull: paper 1, catalogo 3.
- Ogni «Dim.» del paper punta a una scheda esistente (nessun riferimento xr indefinito). Contatti visivi: ho guardato a occhio le pagine 1, 71, 90 del paper e 1, 65, 87, 116, 152, 160, 166, 174 del catalogo; le altre pagine nuove non sono state ispezionate.
- Errori trovati e corretti durante il lavoro: intestazioni correnti troppo lunghe (titoli brevi per i capitoli), intestazione di tabella dell'indice, riferimenti `ENC-N1'`, titolo del paper.

## File
`p_ch12…p_ch19.tex` (nuovi capitoli, cap. 11–18 nel PDF), `c_III1…6.tex` (Parte II), `c_IV1…4.tex` (Parte IV), `c_index_all.tex` (indice generato dalle schede; non rigenerare con `mkindex` senza correggere l'intestazione di tabella), `p_front_all.tex`, `c_front_all.tex`, `STATE.md`.

## Aggiornamento 2 (28/10/2026)
Aggiunte le prove di VAR (B80-B86), ENC (B88-B89) e CONV (B90-B97): catalogo 208 pp. Restano schede-elenco: DICT (24), Fase 10 (39), SYS/VAR/ENC residui (soprattutto S8-ENC par. 8-9, ENC-P0 e CONV-B3). Etichette allineate al ledger.

## Aggiornamento 3 (28/10/2026): aperti e spunti di miglioramento nei paper
- **Paper 0–10** (117 pp): nuovo cap. 19 «The complete list of open problems» (registro PROBLEMI_APERTI al completo: 18 problemi di ricerca, 9 voci bloccate su fonti, dipendenze [F1]/[L-loc]/[GT-u]/[F4⁻]/Malgrange; open questions di ogni pacchetto SYS, VAR, ENC, CONV, DICT; le 12 domande dell'algoritmo esteso; citazioni da chiudere; claim non pienamente dimostrati), cap. 20 «Directions for improvement and routes not taken» (miglioramenti concreti, strade parcheggiate/eliminate del registro ROUTES, pipeline statistica NOTE_ML proposta e rimandata, cosa non è stato fatto, limiti onesti) e appendice B «Bibliography of the project» (le 112 fonti di BIBLIOGRAFIA.bib, con le note di verifica nella lingua originale).
- **Paper 0–5** (`../FASI05/paper_fasi05.pdf`, 76 pp): nuovo cap. 12 con aperti, miglioramenti, strade e pipeline statistica delle sole fasi 0–5.
- Non è «tutto» alla lettera: non sono riportati le righe del ledger (560 righe), le cronologie di RIPRESA/BOARD, gli script SymPy, i singoli open_questions delle sessioni OP-* delle fasi 1–5 (coperti solo tramite REPORT_FINALE §6.3), e le prove dei risultati elencati solo come schede-elenco.
