# PLAN — F6-ENC (Fase 6, problema P-B2: rimuovere V come "rumore" con un encoder analitico)
Data: 26/10/2026. Scout: F6-ENC. Cartella: `research/F6-ENC/`. Canale verso il coordinatore: `inbox/central-F6.md` (AVVISO del coordinatore: NON scrivere in `inbox/central.md`).

## 0. Skill caricate (session-protocol Passo 2)
Lo strumento Skill non espone le skill di progetto: le ho caricate leggendo per intero i `SKILL.md` e seguendone il workflow.
1. `skills-local/session-protocol/SKILL.md` — orientamento, PLAN, inbox, consegna (letta per intera).
2. `skills-local/route-scout/SKILL.md` — struttura del verdetto (triage, evidenza pro/contro, caso di prova, proposta promote/park/merge/kill) (letta).
3. `skills-local/claim-lifecycle/SKILL.md` — stati onesti: gli enunciati di questo scouting sono "candidato" o "prova scritta", mai DIMOSTRATO (letta).
4. `_vendor/.../novelty-check/SKILL.md` — fasi A (claim), B (ricerca), D (rapporto) con il blocco NOVELTY VERDICT LIMITS; fase C (revisore esterno) esclusa per route-scout. Nessuno script eseguito.
5. `_vendor/math-skill/SKILL.md` modo `proof` (esplorazione separata dalla prova, controesempi presto) e `_vendor/scientific-agent-skills/skills/scientific-critical-thinking/SKILL.md` (verdetto tracciabile: osservazione → conseguenza → rimedio). Solo istruzioni Markdown.
6. Ricerca bibliografica: WebSearch per verificare metadati; ciò che non verifico è marcato "da verificare".

## 1. Domanda decisiva
Esiste un operatore W **analitico e costruttivo** (l'"encoder") tale che, se u risolve l'equazione con V, allora W u risolve l'equazione **libera** (V = 0)? Che cosa conserva W: Ann(u), la scomposizione per fattori (C12-T1′), E_int e la struttura per termini (P1-T2, P3-T1)? Quando esiste, è unico, è calcolabile dalla sola u (encoder **cieco**, l'interesse vero dell'utente), è stabile?

**Precisazione da fissare prima di cercare (evita una risposta vuota).** La sola richiesta "W u risolve l'equazione libera" è banale: W = 0 la soddisfa, e così W(t) = U_0(t)U_V(t)^{-1} (quadro d'interazione), che manda ogni soluzione nell'evoluzione libera del dato iniziale. Un encoder è **significativo** solo se: (E1) W è iniettivo, o ha nucleo di dimensione finita noto; (E2) W **interseca** gli operatori: W L_V = L_0 W (stazionario, W commuta con ∂_t), oppure W(t)(i∂_t − H(t)) = (i∂_t − H_0)W(t) nel caso non autonomo; (E3) W è esplicito: differenziale, puntuale più gauge, o integrale di Volterra con nucleo dato da un problema ben posto. La domanda viene studiata con (E1)–(E3).

Nota dal piano dell'utente (`D:\piano di ricerca.md`, incertezza u1): "rumore" lì significa *E_int / parti non spiegate*, non rumore stocastico. Tratto entrambe le letture: V deterministico da togliere esattamente, e V oscillante o casuale da togliere in media (omogeneizzazione).

## 2. Candidati (semi; la lista resta aperta)
| ID | Strada | Tipo di W | Ciò che verifico |
|---|---|---|---|
| ENC-1 | Operatori di trasformazione (Povzner–Levitan, Marchenko, Gel'fand–Levitan) | Volterra I + K, K da un problema di Goursat | esistenza per ogni q ∈ L¹, intertwining senza condizioni al bordo, unicità, dipendenza da q |
| ENC-2 | Darboux / Crum / SUSY (Pöschl–Teller senza riflessione) | differenziale di ordine n | quali q ammettono un W differenziale; nucleo (stati legati) |
| ENC-3 | Trasformazioni puntuali + gauge (Avron–Herbst, lens/Niederer, Liouville) | cambio di variabili × fase | classe dei V rimovibili (quadratici in x?) |
| ENC-4 | Serie di Born / Lippmann–Schwinger | I + G_0 V (dipende da λ) | convergenza (Volterra ⇒ quasi-nilpotente) |
| ENC-5 | Operatori d'onda di Møller Ω_± | globale, asintotico | encoder cieco asintotico; dimensione d ≥ 1 |
| ENC-6 | Omogeneizzazione / media (periodica, stocastica, Kapitza) | limite ε → 0 | operatore efficace e se è libero a meno di gauge |
| ENC-7 | Versioni Dirac | trasformazione per sistemi 2×2, gauge | cosa passa a F6-SYS |

## 3. Criteri fissati PRIMA di cercare
**PROMUOVI** (la strada entra nella Fase 8 come S8-ENC) se valgono tutti:
- (P1) esiste un W che soddisfa (E1)–(E3) su una classe di V esplicita e non banale (almeno V ∈ L¹ su un intervallo, o una classe a dimensione infinita);
- (P2) almeno una delle tre risposte I/S/E è "sì" con un enunciato candidato e una prova scritta di massimo una pagina;
- (P3) i tre controlli SymPy (Pöschl–Teller/Darboux, lens transform armonico, Avron–Herbst) passano;
- (P4) la versione cieca ha un enunciato preciso: positivo (con ipotesi) oppure un teorema negativo.

**PARCHEGGIA** se W esiste solo come teoria classica senza alcun trasporto di I/S/E, oppure se il trasporto richiede ipotesi che G★′ non ha (per esempio solo su ℝ intero con t → ∞).

**ELIMINA** se: W esiste solo nella forma vuota (W = 0, quadro d'interazione); oppure richiede metodi non analitici (ML, statistica come metodo); oppure le sole classi con W esplicito sono a dimensione finita e non coprono il caso fisico (Schrödinger/Dirac con V generico).

**Criterio per il teorema negativo (encoder cieco):** lo considero acquisito come "candidato" se esibisco una famiglia esplicita di coppie (V, v) ≠ (V′, v′) con lo stesso dato u, e se l'ostruzione resta sotto la normalizzazione più naturale.

## 4. Controlli SymPy (solo verifica; script in `research/F6-ENC/sympy/`)
1. `pt_darboux.py`: A = ∂ − tanh x, A†A = L_0 + 1, AA† = L_PT + 1 con q = −2 sech²x; W = A† soddisfa W L_PT = L_0 W; ker W = span{sech x}; Crum per n = 2 (q = −6 sech²x); operatore B_q = A∂A† che commuta con L_q.
2. `lens_harmonic.py`: trasformazione lens (Niederer) dalla Schrödinger libera all'oscillatore armonico, e il nucleo di Mehler come soluzione.
3. `avron_herbst.py`: potenziale lineare F·x ↔ libero (traslazione accelerata più fase).
4. `transmutation_const.py`: operatore di trasformazione simmetrico T f = f + ∫_{−x}^{x} K f per q costante (nucleo di Bessel): equazione di Goursat, K(x,x) = ½∫q, K(x,−x) = 0, intertwining controllato numericamente su funzioni test.
5. `homog_check.py`: spostamento efficace per −∂² + ε^{-1}V(x/ε) (diagonalizzazione nella base di Fourier, solo verifica numerica).

## 5. Fonti e stringhe di ricerca
Marchenko, *Sturm–Liouville Operators and Applications* (1977/1986; AMS Chelsea 2011); Levitan, *Inverse Sturm–Liouville Problems* (VNU 1987); Levitan–Sargsjan, *Sturm–Liouville and Dirac Operators* (Kluwer 1991); Povzner 1948; Gel'fand–Levitan 1951; Crum 1955; Matveev–Salle 1991; Cooper–Khare–Sukhatme 1995; Avron–Herbst 1977; Niederer 1972/1973; Bagrov–Samsonov (Darboux non autonomo); Wilson 1998 (Grassmanniana adelica); Reed–Simon III, Yajima (operatori d'onda); Bensoussan–Lions–Papanicolaou; Kapitza 1951; Kravchenko 2020 (calcolo degli operatori di trasformazione). Stringhe: "transmutation operator Sturm-Liouville Goursat", "differential intertwining operator free Schrödinger Darboux adelic Grassmannian", "point transformation Schrödinger equation free quadratic potential Niederer", "time-dependent Darboux transformation Bagrov Samsonov", "large highly oscillatory potential homogenization effective potential".

## 6. Contatti
- **F6-VAR** (identificare V ↔ rimuovere V): l'encoder cieco = identificazione di V + operatore di trasformazione. Mando TABELLA e DOMANDA sul loro risultato di identificabilità di q da una o più soluzioni.
- **F6-DICT** (hub): traduzione nel dizionario filtrato 𝓓_∞; W come cambio di coordinate del dizionario (Ann transportato).
- **F6-SYS**: AVVISO per Dirac (trasformazione per sistemi, gauge).
- Coordinatore: `inbox/central-F6.md` (PLAN-READY, NEW-ROUTE, TABELLA, DONE).

## 7. Criterio di "fatto"
PLAN, VERDETTO (1–2 pagine, risposte I/S/E, enunciati candidati con ipotesi, ostruzioni, teorema negativo cieco, costo, novità, raccomandazione secondo §3), NOTE (calcoli e prove scritte), sources.bib, open_questions.md, sympy/ con 5 script eseguiti; inbox letta tre volte; `DONE F6-ENC` in `inbox/central-F6.md`.
