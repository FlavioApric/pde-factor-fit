# PLAN — F4-HOR (scout di orizzonte, Fase 4, sprint di scouting) · 26/10/2026

Mandato (FASE4_SCOUTING.md, roster): strada (ii) del piano Fase 4, "f(S·x) con analisi per componenti come negli appunti", e slot aperto (v): Painlevé, forme normali, operatori monotoni / semigruppi non lineari (Crandall–Liggett), teoria spettrale non lineare, più strade nuove emerse dalla Fase 3. Vincolo piano v4: almeno una strada non-seme scoutata o eliminata con motivi.
Scrivo solo in `research/F4-HOR/` e `inbox/`. Stati onesti: niente DIMOSTRATO; enunciati nuovi = "candidato" o "prova scritta"; riferimenti verificati o "da verificare".

## 0. Letture fatte (Passo 0)
FASE4_SCOUTING.md, RIPRESA.md (agg. 26/10 Fase 4), PROTOCOLLO.md, NOTAZIONE.md v1+v2, PROBLEM.md (G★′), GATE3.md, claims/LEDGER.md (righe C3-T1, P1-T2, P1-P1(e), P1-T3, C12-T1′, P4-*), ROUTES.md (incl. parcheggiate RT-R7a, RT-S1e/f, RT-S2a, RT-R1b), research/SCOUT-1, SCOUT-2, R7 REPORT, piano (appunti 0B Pg.E–G, 0C, Fase 4). Inbox F4-HOR: vuota all'inizio.

## 1. Skill caricate (lettura integrale/strutturale dei SKILL.md; nessuno script `_vendor` eseguito)
1. `skills-local/session-protocol` (per prima), `skills-local/route-scout` (workflow nota → PLAN → ricerca/prova → verdetto 1 pagina → riga ROUTES), `skills-local/claim-lifecycle` (stati).
2. `scientific-brainstorming` — generazione indipendente PRIMA della letteratura (fatta: §2 sotto, prima di qualunque WebSearch), etichette idea/assunzione/evidenza localizzata/decisione; riapertura dopo la ricerca.
3. `hypothesis-generation` — per ogni strada: enunciato candidato, rivale, predizione discriminante sul banco Burgers, esito incompatibile.
4. `idea-discovery` — solo la struttura survey → idee → novelty → critica → ranking (niente pilot GPU, niente revisore Codex: decisione dell'utente).
5. `research-lit` — eseguita come WebSearch/WebFetch manuali (sorgente `web`), stringhe in §4.
6. `novelty-check` — fasi A (claim) e B (ricerca); fase C cross-model sostituita da autovalutazione dei limiti; applico i "verdict limits" (ABANDON solo con articolo nominato).
SymPy (solo come CONTROLLO, k3): `.venv\Scripts\python.exe -I research/F4-HOR/sympy/<script>.py`.

## 2. Strade da scoutare (generazione indipendente, prima della letteratura) e criteri FISSATI ORA
Banco di prova comune: Burgers u_t + u u_x = ν u_xx (poi KdV u_t + 6uu_x + u_xxx = 0). Domanda guida: (I) identificazione / (S) scomposizione / (E) E_int.
Per ogni strada: **PROMUOVI** = merita una sessione di Fase 4 dopo il Gate 4a; **PARCHEGGIA** = idea valida ma non ora (motivo + trigger di riapertura); **ELIMINA** = criterio di eliminazione scattato; **MERGE-INTO** = contenuto già coperto da un altro scout/strada.

### H-ii-a MODREL — "f(S·x)" in forma di Hammerstein: modulo delle relazioni lineari tra feature non lineari
Idea: scrivere l'equazione come Σ_j Q_j(∂) f_j(u) = 0 (Burgers: (∂_t − ν∂_x²)u + ½∂_x(u²) = 0, f = (u, u²)). L'oggetto analogo di Ann(u) è il **modulo delle sizigie** Syz_f(u) = {(Q_j) ∈ R^d : Σ Q_j(∂) f_j(u) = 0} ⊂ R^d (R = ℂ[∂_t,∂_x]): resta un R-modulo **lineare**, quindi la macchina di Fase 3 (C3-T1, P4) può trasportarsi. Appunti: E2/E3 (â = f(J·Φ)), G3–G4, A6 (V·V_x), D2 (Φ = jet).
- PROMUOVI se: (a) enunciato candidato "Syz_f(u) è generato dalla relazione dell'equazione ⟺ test di tipo EP" scritto con prova schizzata per la classe di Hammerstein a coefficienti costanti, E (b) sul banco Burgers il controllo SymPy distingue 1-shock (non identificante) da 2-shock (identificante), E (c) non coincide con l'ideale differenziale di F4-ALG (dà qualcosa di lineare in più: struttura di modulo, rango, decidibilità).
- ELIMINA / MERGE-INTO F4-ALG se: Syz_f(u) è solo la parte "lineare nei Q" dell'ideale differenziale e nessun risultato di Fase 3 si trasporta oltre la tautologia "ker 𝔾(u) con dizionario di monomi" (G7/R7 già noto).

### H-ii-b WIENER — "f(S·x)" in forma di Wiener: u = g(φ), φ ∈ ker L lineare (C-integrabilità di Calogero)
Idea: lettura letterale di G4 "studio le f(S·x)": u = g(S·φ) con φ soluzione di un'equazione lineare. Burgers: u = −2ν∂_x log φ (Cole–Hopf) è esattamente di questo tipo. Componenti = fattori di L sul lato φ (C12-T1′ vale esattamente), E_int = g(Σφ_j) − Σ g(φ_j).
- PROMUOVI (come strada autonoma) se: la classe "u = g(φ), Lφ = 0" con g in una famiglia finita dà un teorema I/S/E che NON passa per una singola linearizzazione specifica (cioè un risultato uniforme sulla classe di Calogero), con fonte per la classificazione.
- MERGE-INTO F4-LIN (iv) se: ogni caso utile è una linearizzazione nota caso per caso (Cole–Hopf, Hopf–Cole generalizzate), senza enunciato uniforme.

### H-ii-c SPLIT-f — "rompo il sistema e lavoro per direzioni scalari" (F6) con f non lineare
Idea (ipotesi da verificare): la diagonalizzazione S = VΛV⁻¹ commuta con una non linearità componente per componente solo se V è monomiale; quindi F6 fallisce per f non lineare, e l'E_int statico f(Σu_j) − Σf(u_j) per f polinomiale di grado d ha ordine d'interazione ≤ d (Möbius, RT-S1c).
- PROMUOVI (come lemma di ostruzione da registrare, non come strada) se entrambi gli enunciati si dimostrano in poche righe e rispondono ad appunti F6/G4 in modo netto.
- ELIMINA come strada (resta il lemma) se — come previsto — l'ordine ≤ d vale solo per la mappa statica e l'evoluzione regenera tutti gli ordini (allora la parte dinamica è di F4-LIFT/Carleman).

### H-ii-d HAANTJES — versione vettoriale di f(S·x): invarianti di Riemann, torsione di Haantjes/Nijenhuis, sistemi semi-hamiltoniani (Tsarev) [non-seme]
Idea: per u_t + A(u)u_x = 0 la "diagonalizzazione per direzioni" (F6, II via b) esiste come cambio di coordinate non lineare ⟺ torsione di Haantjes nulla (autovalori distinti); poi hodograph generalizzato (Tsarev) linearizza.
- PROMUOVI se esiste un enunciato I/S/E utilizzabile già nel caso scalare (banco Burgers) o nel ladder L5 scalare.
- PARCHEGGIA (trigger: Problema 2 / sistemi, appunti H2) se serve n ≥ 2 componenti: fuori dal vincolo k5 "scalare prima".

### H-v1 PAINLEVÉ — analisi di singolarità (WTC, ARS) come strumento di identificazione e generatore di linearizzazioni
Idea: per soluzioni meromorfe, il bilancio dominante ai poli fissa i rapporti tra coefficienti (Burgers: poli semplici con residuo −2ν/a per u_t + a u u_x = ν u_xx); l'espansione WTC troncata produce Cole–Hopf/Bäcklund. Legame con TROP (poligono di Newton/power geometry).
- PROMUOVI se: (a) enunciato candidato "una singola soluzione meromorfa con almeno un polo identifica il rapporto ν/a (Burgers) / il rapporto dispersione/non linearità (KdV)" con controllo SymPy, E (b) il dato richiesto è compatibile con un modello di dato del progetto (M1 formula / M2 jet) e dà più di ker 𝔾(u).
- PARCHEGGIA / MERGE-INTO F4-LIN se: richiede continuazione analitica (incompatibile con M3 = u ∈ H^m(Ω), mal posta) e il contributo è solo "algoritmo per trovare la linearizzazione" (strumento per (iv)).

### H-v2 NF — forme normali (Poincaré–Dulac / Shatah): E_int = parte non risonante (rimovibile, in forma chiusa) + parte risonante (essenziale)
Idea: trasformazione quasi-identica u = v + B(v,v) + … con simbolo b(k₁,k₂) = N(k₁,k₂)/(ω(k₁)+ω(k₂)−ω(k₁+k₂)); per Burgers il divisore è 2νk₁k₂ ≠ 0 fuori da k = 0 (nessuna risonanza) — ipotesi: la forma normale di Burgers è il calore e la trasformazione è la serie di Cole–Hopf; per KdV la parte cubica risonante dà gli sfasamenti (Hirota a coppie). Appunti: B1–B2 (E_int ≈ h(e₁,e₂)), C2 (perturbazione), P1, P3.
- PROMUOVI se: (a) per Burgers la trasformazione al 2° ordine coincide con lo sviluppo di Cole–Hopf (SymPy), E (b) esiste un enunciato candidato per (E) "E_int al 2° ordine = B(u₁,u₂)+B(u₂,u₁) in forma chiusa dal simbolo" valido anche fuori dall'integrabilità (es. Burgers con dispersione, KdV–Burgers), E (c) la novità rispetto alla letteratura sulle forme normali è almeno l'uso per I/S/E.
- ELIMINA se la trasformazione non è definita (divisori nulli su un insieme di misura positiva) già su Burgers / KdV–Burgers, o se non dà nulla oltre F4-LIN.

### H-v3 MON — operatori monotoni / semigruppi non lineari (Crandall–Liggett, Brezis–Pazy, Kružkov): spazio L¹ e identificazione non parametrica di f
Idea: (I) un'orbita determina A solo sul grafo dell'orbita (nessuna "sottospazio ciclico" non lineare); in una classe strutturata (u_t = ∂_x² φ(u), u_t + ∂_x f(u) = ν u_xx) una soluzione identifica la FUNZIONE φ (o f) sul range di u (inversione "f(S·x)" non parametrica; Cannon–DuChateau). (S) somma di accretivi: formula prodotto di Lie–Trotter non lineare (Brezis–Pazy) = quadro moltiplicativo. (E) contrazione L¹ ⇒ E^mult di splitting continuo in L¹ (contrasto con P1-P1(e) in H^m).
- PROMUOVI se: (a) enunciato candidato di identificazione non parametrica di f (o φ) da una soluzione, con condizione esplicita (u_x ≠ 0 / range), controllato su Burgers, OPPURE (b) enunciato candidato "E^mult (splitting avvezione/diffusione di Burgers) è Lipschitz in L¹" che risponde alla domanda 3 del Gate 3 (uno spazio dei dati in cui la scomposizione per termine è continua).
- PARCHEGGIA se dà solo buona posizione (esistenza, contrazione) senza I/S/E nuovi.

### H-v4 NLSPEC — teoria spettrale non lineare (autoproblemi λu ∈ ∂J(u), p-Laplaciano, decomposizione spettrale TV di Gilboa–Burger)
Idea: F1 "â = Σ f(λ_a) v_a⊗v_a" ha un analogo non lineare: scomposizione del DATO in autofunzioni non lineari di un funzionale 1-omogeneo (trasformata spettrale TV).
- PROMUOVI se dà (I) o (S) per l'OPERATORE incognito (non solo per il dato) sul banco Burgers / p-Laplaciano.
- PARCHEGGIA (trigger: P2 / Idea I / Problema 1, regolarizzazione e "rumore") se agisce solo sul dato come regolarizzatore; ELIMINA per il core se le autofunzioni non lineari non hanno superposizione e la scomposizione non vede l'operatore.

### H-ω — strade nuove dalla Fase 3 (riapertura dopo la letteratura)
Domanda 3 del Gate 3 (spazio dei dati diverso da H^m in cui la scomposizione per termine sia continua) → candidato L¹ (H-v3). Altre emerse dopo la ricerca: da registrare qui con criterio prima di valutarle.

## 3. Ordine di lavoro
1. PLAN-READY + NEW-ROUTE (una nota per strada) in central; AVVISI a F4-ALG (MODREL), F4-LIN (WIENER, PAINLEVÉ, NF), F4-INT (NF/KdV, PAINLEVÉ), F4-LIFT (SPLIT-f, NF vs Carleman).
2. Prove rapide + SymPy: MODREL (Gram 1-shock vs 2-shock Burgers), NF (Burgers 2° ordine vs Cole–Hopf), PAINLEVÉ (residuo), MON (identificazione di f da una soluzione), SPLIT-f (lemma monomiale).
3. Ricerca bibliografica e novelty (WebSearch/WebFetch).
4. Inbox a metà. 5. NOTE.md (dettaglio), VERDETTO.md, sources.bib, open_questions.md. 6. Inbox prima di consegnare; TABELLA righe ROUTES in central; DONE F4-HOR.

## 4. Stringhe di ricerca previste
"Burgers equation normal form Cole-Hopf", "Kodama normal form asymptotic integrability", "Fokas Liu asymptotic integrability", "Shatah normal forms quadratic Klein-Gordon", "Weiss Tabor Carnevale Painleve property PDE", "Calogero C-integrable nonlinear PDE", "Cannon DuChateau inverse problem nonlinear diffusion coefficient", "Crandall Liggett generation semigroups nonlinear", "Brezis Pazy convergence nonlinear semigroups product formula", "Kruzkov L1 contraction", "Gilboa total variation spectral decomposition", "Burger Gilboa Moeller Eckardt spectral decompositions one-homogeneous", "Haantjes tensor diagonalization hydrodynamic type Tsarev", "Wiener Hammerstein block-oriented identification".

## 5. Contatti
central (PLAN-READY, NEW-ROUTE, TABELLA, DONE); F4-ALG (hub: MODREL ↔ ideale differenziale), F4-LIN (Cole–Hopf ↔ WIENER, NF, PAINLEVÉ), F4-INT (KdV: NF cubica ↔ Hirota; Painlevé ↔ Lax), F4-LIFT (SPLIT-f ↔ Carleman/Volterra).

## 6. Criterio di "fatto"
Ogni strada H-* ha: risposte I/S/E (sì/parziale/no + enunciato o ostruzione), costo, novità (con fonte verificata o "da verificare"), raccomandazione secondo i criteri del §2. Almeno una strada non-seme (H-ii-d, H-v2, H-v3 o H-v4) scoutata o eliminata con motivi. File consegnati; TABELLA e DONE in central.
