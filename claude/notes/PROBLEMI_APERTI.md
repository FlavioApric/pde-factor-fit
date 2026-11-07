# PROBLEMI APERTI — registro dei residui alla chiusura della parte analitica (coordinatore, 28/10/2026)

Questo file raccoglie in un solo posto tutto ciò che resta APERTO o CONDIZIONALE quando si chiude la parte analitica del progetto. Gli stati **non** vengono alzati: nel LEDGER restano APERTO o CONDIZIONALE come prima. Cambia solo la decisione di gestione. Queste voci sono documentate come domande di prosecuzione, e la parte analitica si considera chiusa.

Fonti di questo registro:
- CHIUSURA_F10.md §3 e §5;
- REPORT_FINALE.md §6.3;
- il triage indipendente `work/CHECK-F10/TRIAGE_APERTI.md`, che contiene per ogni voce motivazione, tentativi e script;
- l'audit `work/CHECK-F10/AUDIT_TRIAGE.md`;
- le righe del LEDGER «F10-TRIAGE».

## 0. Perché si può chiudere: nessuna voce è fondamentale

I risultati centrali del progetto non dipendono da nessuna delle voci sotto. Sono i risultati sull'identificazione e sulla decomposizione di un operatore a partire da una soluzione esatta u, cioè le caratterizzazioni lineari, ALG-*, S4ID-T1, C12-T3/P2-T3, i teoremi negativi e i controesempi.

Il controllo è stato fatto cercando ogni ID in REPORT_FINALE.md, PROBLEM.md e PAPER/. Ogni voce di questo registro è di uno di tre tipi:
- (i) un'estensione a classi più generali di un risultato già DIMOSTRATO in un caso modello;
- (ii) una domanda nuova nata durante il lavoro;
- (iii) una dipendenza da una fonte pubblicata che non è disponibile offline.

Le uniche voci da cui dipendono enunciati del REPORT sono queste. Ogni dipendenza è già segnata nel REPORT con «mod …» o «CONDIZIONALE»:
- **[F1] Lax–Oleinik = Kružkov.** Il LEDGER la dà CON-FONTE, il REPORT la dà DIMOSTRATO mod Kružkov 1970, Thm 1 §3, verificato sul testo primario. Su [F1] poggiano i risultati di Burgers oltre lo shock: S4T-T3(iii), OPA-T1, OPF5A-T1/T2/C1. La fonte è classica ed è stata letta. Quello che manca è solo una prova autonoma, per cui il triage dà un piano. Questo **non** è un problema aperto.
- **[L-loc]**, da cui dipende OPA-Q1 nel caso di più nascite di shock. Il caso con una sola nascita di shock (per esempio sin x) è chiuso mod [F1].
- **[GT-u]**, cioè [GT-u₀] e [GT-u_m], da cui dipendono S4ID-P8 e OPR2-P7 (asintotica con derivate).
- **[F4⁻]**, da cui dipende INT-T1(B) (N-solitoni senza riflessione). È verificato per N = 2.
- **Malgrange 1966**, da cui dipende C3-P1 per dati generali su convessi. Il caso sul getto è DIMOSTRATO senza fonte, e il teorema citato è CON-FONTE verificato.

## 1. Problemi di ricerca: nessuna strada nota, classe B del triage

| ID | domanda | risultato già ottenuto | che cosa servirebbe |
|---|---|---|---|
| C12-Q2 = OPF-Q2 | chiusura della somma per N ≥ 3 nel caso di operatori differenziali | falso in Hilbert astratto (controesempio); caso N = 2 DIMOSTRATO | una famiglia differenziale con ≥ 2 interazioni non compatte |
| C12-Q1 | chiusura della somma per (τ−ξ²)(τ+cξ) | — | stime di strato di bordo (strada OPR2-L1, calore × trasporto) |
| OPF5C-Q1 | δ_N(K) per N generale | 9 valori esatti, computer-assisted; δ₆(12)=7 nuovo; congetture δ_N(2N−1)=N+2, δ_N(2N−2)=N+4, δ_N(2N)=N+1 | una struttura per N generale. Per N fissato è un calcolo finito; δ₆(11)=8 è PROVA SCRITTA, mentre Hirota N=5 non è concluso (run di circa 17 min interrotto) |
| OPR2-Q3 | zoccolo ripetuto, «nessun test finito» | DIMOSTRATO sotto (I) e (II) | teoria dei sollevamenti degli atomi |
| OPR2-Q2′ | cunei con direzioni degeneri | modello tangente chiuso e diretto (OPF5B-P8); controllo numerico 7/7 | la parte (L-int) è una stima HS esplicita scrivibile in poche ore; la parte (L-v) richiede l'analisi al vertice del cono |
| INT-Q1 | KdV, r ≢ 0, u analitica: esiste un'ODE autonoma in x? | OPF5C-T6: ordine ≤ 3 ⇒ 0 o 1-solitone | relazioni singolari nell'origine e termini sottodominanti dell'asintotica radiativa (a monte serve [GT-u_m]) |
| P1-Q7, caso generale | algebre con (H) senza (Dil) | il candidato (x³+x)∂, ∂ è DIMOSTRATO | nessuna strada senza dilatazione |
| P2-Q1-NL, caso generale | domini non lipschitziani | Δ, m ≥ 1, L^{1,2} ⊂ L² DIMOSTRATO | P generale e m = 0 |
| P2-Q1-COD | codimensione esatta per P generale | — | funzionali di periodo continui in H^m |
| VAR-Q18 | moltiplicazioni | — | un controesempio con W ruvido, v solo continuo e controllo dell'intera serie di Dyson |
| VAR-P12(d) | log non quadratici | osservazione parziale (parità, dilatazioni) | un'ostruzione per i log non quadratici |
| VAR-C3Q2-open / VAR-Q13 | caso non monico | caso monico (a′) DIMOSTRATO (VAR-C3Q2-R) | una decomposizione senza monicità |
| SYS-DIRAC-POL, tempi complessi | polinomialità per t, m complessi | caso con t, m reali DIMOSTRATO | il triage abbozza un Lemma E′ «per crescita»; manca l'audit |
| ENC-Q4 | lettura DM3 | — | prima va definita la classe W(t) |
| DICT-Q3(c) | divisione C^∞ a rango variabile | — | un criterio generale di divisione |
| AM-CL | chiusura AM | non più necessaria per altri risultati (LEDGER F10-TRIAGE) | — |
| OPA-Q2, densità | densità della classe Morse+(SB) | abbozzo (Sard a parametri finiti) | scrivere e auditare l'abbozzo |
| domini non convessi | densità di OPF5B-T1 fuori dai convessi | caso convesso DIMOSTRATO | — |
| [L-loc] | lemma di localizzazione per OPA-Q1 con più shock | enunciato scritto nell'audit S-CHECK-20 | una prova |

## 2. Voci bloccate su fonti non disponibili offline (classe C)

Il progetto vieta di scaricare file. Ognuna di queste voci si sblocca mettendo il testo indicato nella cartella del progetto (per esempio in VOLUMES/).

| voce | fonte necessaria | dopo la lettura |
|---|---|---|
| [GT-u₀] | Grunert–Teschl §5, Krüger–Teschl | riscrittura con costanti esplicite; lavoro di pochi giorni |
| [GT-u_m] | Deift–Zhou, CMP 165 (1994) 175–191; Buslaev–Sukhanov 1986 | derivazione termine a termine; non breve |
| VAR-Q17(b) | Baudouin–Puel; Lasiecka–Triggiani–Zhang; Mercado–Osses–Rosier (Carleman per Schrödinger con V(t,x)) | adattamento |
| ENC-Q10 | Matveev–Salle; Bagrov–Samsonov (Darboux a coppie) | adattamento, più una decisione su 𝔈 |
| DICT-U3d-v | Braess; Braess–Hackbusch | per t^{−β} probabilmente τ_k non serve; il limite uniforme sulla classe resta un problema di classe B |
| Malgrange 1966 | Malgrange, *Ideals of differentiable functions* | solo per avere una prova autonoma: il teorema è già CON-FONTE |
| (WP) | Bona–Smith; Kato 1983; Lax 1975 | in alternativa, una prova autonoma di più giorni |
| [F4⁻] | fonte primaria per gli N-solitoni senza riflessione | verificato per N = 2 |
| Oberst 1993 | MCSS 6 (letto solo l'abstract) | **solo priorità e novità**: SYS-EX è DIMOSTRATO su Ω arbitrario anche senza questa fonte |

## 3. Decisione

La parte analitica del progetto è **chiusa al 28/10/2026**. Le voci dei §1–§2 non bloccano nessun risultato centrale e sono il punto di partenza di un'eventuale fase successiva di ricerca. Il loro stato nel LEDGER resta invariato (APERTO o CONDIZIONALE): un'etichetta si alza solo dopo prova e audit, come prevede il protocollo.
