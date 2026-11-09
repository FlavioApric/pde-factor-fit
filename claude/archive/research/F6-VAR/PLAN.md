# PLAN — scout F6-VAR (Fase 6, temi R10 + R11; problemi P-B1 e C3)
Data: 26/10/2026. Cartella: `research/F6-VAR/`. Stato: scouting preparatorio e reversibile (non promuove claim a DIMOSTRATO, non tocca PROBLEM/LEDGER/BOARD/ROUTES/NOTAZIONE/RIPRESA/PBLean/work).
Canale verso il coordinatore: `inbox/central-F6.md` (AVVISO del coordinatore: NON `inbox/central.md`).

## 0. Skill caricate (come)
- `skills-local/session-protocol/SKILL.md`, `skills-local/route-scout/SKILL.md`, `skills-local/claim-lifecycle/SKILL.md`: lette per intero, seguite (PLAN prima, criteri fissati prima, stati onesti, inbox append-only).
- `_vendor/Auto-claude-code-research-in-sleep/skills/novelty-check/SKILL.md`: letta; uso la fase A (estrarre 3–5 affermazioni portanti) e la fase B nella versione possibile qui (conoscenza della letteratura + controllo dei riferimenti noti); il revisore esterno (Codex) è escluso per decisione dell'utente: dichiaro i limiti del verdetto.
- `_vendor/math-skill/SKILL.md` (modo proof): letta; uso per le prove rapide dei casi minimi.
- `_vendor/scientific-agent-skills/skills/scientific-critical-thinking/SKILL.md`: letta; uso per il verdetto finale (separare evidenza da affermazione, stato onesto).
- Nessuno script `_vendor` eseguito. SymPy solo come verifica: `.venv\Scripts\python.exe -I research/F6-VAR/sympy/<script>.py`.
- deep-research (anthropic-skills) NON invocata: il lavoro è su teoria classica (Weyl, Loewy, Gel'fand–Levitan, Magnus) che conosco; i riferimenti vanno marcati "verificato (metadati noti)" o "da verificare" e passano a CIT-AUDIT.

## 1. Domande (dal roster, FASE6_SCOUTING.md riga F6-VAR; appunti H1, E1; item C3-Q2, C12-Q5, L4, P3-T1, P1-T4/T5)
**Q1 (V(x), autonomo, oggetto canonico).** Per coefficienti variabili l'oggetto canonico è la coppia (D·u, u) (Gate 3). In A_n (Weyl), ℂ(x)[∂], anelli di operatori a coefficienti analitici/lisci: cosa diventano (I) C3-T1 (Ann(u) = (P) ⟺ test), (S) C12-T1′ (LCLM / decomposizione di Loewy, non unicità), (E) E_int (A9)? Ostruzioni: niente base EP, niente gcd per ideali sinistri, fattorizzazione non unica (Landau), ideali sinistri non principali in A_n (n ≥ 1, ma generati da 2 elementi — Stafford).
**Q2 (classi di coefficienti).** Polinomiali (Weyl), razionali, analitici, lisci, singolari (Coulomb 1/r), illimitati (x²): dove cambia la risposta?
**Q3 (P-B1: identificare V da UNA soluzione).** iψ_t = −ψ_xx + V(x)ψ (e Dirac con potenziale). Formula puntuale V = (iu_t + u_xx)/u dove u ≠ 0: quando determina V, fallimenti (zeri, rumore, V fuori classe finita, regolarità). Confronto con la via dei dati spettrali (Sturm–Liouville inverso: Borg, Gel'fand–Levitan, Marchenko, Borg–Marchenko, funzione A di Simon): unicità e stabilità.
**Q4 (V(t,x) non autonomo).** Propagatori U(t,s), Dyson, Magnus (raggio ∫‖A‖ < π, Moan–Niesen), Floquet; destino di E_int (A9) e dello splitting (Fase 4) quando i termini dipendono da t; senso C3 (convergenza delle parti iterative) con teoremi candidati.
**Q5 (domanda guida I/S/E, regola 3)** + novelty-check.
**Q6 (SymPy)** sui casi minimi: oscillatore armonico, Pöschl–Teller, potenziale lineare/Airy.

## 2. Criteri fissati PRIMA di cercare (route-scout)
Per ogni strada (W = Weyl/D-moduli/Loewy; ID-PT = identificazione puntuale da una soluzione; ID-SP = via dei dati spettrali; NA = Dyson/Magnus/Floquet):
- **PROMUOVI** se: (a) dà almeno un enunciato candidato preciso (ipotesi esplicite) che trasporta I, S o E al caso variabile, (b) è analitica (niente ML, niente numerica come metodo), (c) il caso minimo SymPy lo conferma, (d) ha costo dichiarabile (algoritmico o di dato).
- **PARCHEGGIA** se: l'enunciato esiste solo per una sottoclasse stretta (es. solo ODE in x, solo potenziali in classe finita) o richiede dati che il modello M1–M3 non fornisce (es. dati spettrali completi da una soluzione sola), ma non c'è ostruzione.
- **ELIMINA** se: un controesempio o teorema noto mostra che il trasporto è falso nella forma richiesta, e non esiste una riformulazione più debole utile a G★′ / G★″.
- In più, per ogni risposta I/S/E: "sì" solo con enunciato candidato; "parziale" con classe precisa; "no" solo con ostruzione esplicita (controesempio o teorema).

## 3. Fonti / stringhe previste
Coutinho *A primer of algebraic D-modules* (1995); Björk *Rings of differential operators* (1979); Stafford 1978 (ideali sinistri di A_n generati da 2 elementi); Landau 1902 / Loewy 1903/1906; Grigoriev–Schwarz (Loewy per D-moduli, 2004–2008); Tsarev (fattorizzazione di LPDO, 2005); van der Put–Singer *Galois theory of linear differential equations* (2003); Ore 1933; Bronstein–Petkovšek 1996; Borg 1946; Gel'fand–Levitan 1951; Marchenko 1950/1986; Simon *A new approach to inverse spectral theory I* (Ann. Math. 150, 1999); Gesztesy–Simon 2000 (Borg–Marchenko locale); Freiling–Yurko 2001; Pöschel–Trubowitz 1987; Magnus 1954; Blanes–Casas–Oteo–Ros Phys. Rep. 470 (2009); Moan–Niesen Found. Comput. Math. 8 (2008); Casas 2007; Dyson 1949; Kato 1953/1970 (evoluzioni non autonome); Pazy cap. 5; Floquet 1883 / Eastham 1973; Lubich (splitting per Schrödinger); Jahnke–Lubich 2000; Hochbruck–Lubich 2003 (Magnus per Schrödinger). Problemi inversi di identificazione del potenziale da una soluzione: Baudouin–Puel 2002 (stabilità con stime di Carleman per Schrödinger), Bukhgeim–Klibanov 1981, Imanuvilov–Yamamoto.

## 4. Contatti (grafo, regola 5)
- F6-SYS ↔ F6-VAR: moduli su Mat_k(R) ↔ D-moduli (Dirac con potenziale = sistema a coefficienti variabili; Smith/Jacobson su ℂ(x)[∂]).
- F6-VAR ↔ F6-ENC: identificare V ↔ rimuovere V (operatori di trasformazione GLM: lo stesso nucleo K(x,y) che ricostruisce V rimuove V).
- F6-DICT (hub): classe di V = dizionario filtrato; N1 nel caso variabile.
- F6-CONV: stabilità condizionale dell'identificazione di V (C1), C3 lo tengo io.
Lettura della mia inbox: inizio (fatto), metà, fine.

## 5. Criterio di "fatto"
PLAN.md, NOTE.md (sviluppo), VERDETTO.md (1–2 pagine con PROMUOVI/PARCHEGGIA/ELIMINA per W, ID-PT, ID-SP, NA e tabella I/S/E), sources.bib, open_questions.md, sympy/ con almeno 3 script eseguiti (oscillatore, Pöschl–Teller, Airy; + Magnus/Floquet minimo), messaggi a F6-SYS, F6-ENC, F6-DICT; `DONE F6-VAR` in `inbox/central-F6.md`.
