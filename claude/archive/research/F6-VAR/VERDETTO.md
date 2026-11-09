# VERDETTO — F6-VAR (R10 + R11: coefficienti variabili, identificare V, non autonomo, C3)
26/10/2026. Skill caricate (lettura integrale, nessuno script _vendor): session-protocol, route-scout, claim-lifecycle, novelty-check (fase A/B senza revisore esterno), math-skill (proof), scientific-critical-thinking. Dettagli e prove: `NOTE.md`. SymPy: `sympy/*.out`. Stati: nulla è DIMOSTRATO; "prova scritta" = elementare, non auditata.

## 1. Risposta in una frase
Identificare V da una soluzione è **facile quando la forma dell'equazione è fissata** (formula puntuale V = (iu_t + u_xx)/u, Lipschitz dalla norma C^{1,2}, mal posta di ordine 2) e **impossibile come identificazione intrinseca quando la classe dei coefficienti è grande** (ogni u senza zeri ha annullatore di rango 1); fra i due estremi, per le ODE a coefficienti razionali c'è un analogo esatto di C3-T1 (ciclicità sotto il gruppo di Galois), mentre per le PDE nell'algebra di Weyl C3-Q2 e C12-Q5 restano aperti con ostruzioni esplicite. Nel caso non autonomo E_int e splitting si estendono con commutatori **a due tempi**, e la convergenza delle parti iterative (C3) si classifica per struttura dell'algebra di Lie.

## 2. Enunciati candidati (ipotesi in NOTE)
| ID | enunciato | stato | SymPy |
|---|---|---|---|
| VAR-N1 | 𝒦 ∂-chiusa, u senza zeri con u_t/u, u_x/u ∈ 𝒦 ⇒ Ann_{𝒦[∂]}(u) = (∂_t − u_t/u, ∂_x − u_x/u), 𝒦[∂]/Ann ≅ 𝒦 (classi lisce/analitiche: nessuna identificazione intrinseca) | prova scritta | — |
| VAR-T1 | identificazione strutturata ⟺ iniettività della mappa residuo ρ_u(Q) = Qu/u sulla classe; Schrödinger V(x) ∈ C: V determinato su J ∖ int X_0 | prova scritta (Holmgren per gli zeri: candidato) | oscillatore, PT, Airy, Avron–Herbst OK |
| VAR-P3 | stabilità Lipschitz C^{1,2} → L^∞ su {|u| ≥ δ}; non continua da L^∞ | prova scritta | — |
| VAR-P4 | dato stazionario: solo V − E; (P, q) al più modulo q → q + c | prova scritta | OK |
| VAR-T2 | ODE in ℂ(x)[∂]: Ann(u) = (L) ⟺ u vettore ciclico di Gal(L) su Sol(L); L irriducibile ⇒ ogni u ≠ 0 identifica (Airy); u iperesponenziale non identifica (autostati di oscillatore, Pöschl–Teller) | prova scritta + fonte (van der Put–Singer, n. da verificare) | OK |
| VAR-P5 | Dirac: V scalare = ⟨ψ,r⟩/|ψ|²; V hermitiana 2×2 determinata ⟺ span_t ψ(t,x) = ℂ² | prova scritta | — |
| VAR-T6 | ODE: scomposizione per fattori = zoccolo (Loewy) del G-modulo; ambiguità Σ ord L_j − ord LCLM | prova scritta + fonte | — |
| VAR-C7 | PDE: Landau, QQP = SQ (3 contro 2 fattori irriducibili) ⇒ C12-T1′ per elementi falso | V-ex + fonte (irriducibilità di S verificata solo parzialmente) | OK |
| VAR-P8 | algebra di Lie ⟨∂², V⟩ finita ⟺ deg V ≤ 2 (V polinomiale); E_int in forma chiusa solo per potenziali al più quadratici | prova scritta (polinomiale), congettura (liscia) | x, x² finiti; x³ cresce; [V,[∂²,V]] = −2V′² |
| VAR-P9 | non autonomo: E^mult = ∬_{s1>s2}[A_2(s1),A_1(s2)] + O(t³); commutare a tempi uguali non basta | prova scritta | OK (2×2) |
| VAR-P11 | Dyson–Phillips non autonomo, B ∈ C_s([0,T],L(X)): converge per ogni t (estende P3-T1) | CON-FONTE (Phillips 1953, Pazy cap. 5; n. da verificare) | — |
| VAR-T10 | C3: nilpotente ⇒ Magnus termina (A); risolubile ⇒ Wei–Norman globale (A); sl_2 ⇒ locale, rottura a cos t = 0; limitato ⇒ Magnus se ∫‖A‖ < π (Moan–Niesen), Dyson sempre (B); illimitato generico ⇒ (C) | composizione di noti (candidato) | Stark nilpotente passo 3; LDU = cos t; Magnus Airy O(t^5) OK |
| VAR-P12 | Floquet unitario: K = (i/T)log U(T) esiste sempre, ma non è differenziale | prova scritta | — |

## 3. Domanda guida (I/S/E)
- **(I) Parziale.** Strutturata: sì (VAR-T1, costo O(1) per punto). Intrinseca: sì per ODE (VAR-T2), no per classi grandi (VAR-N1, ostruzione), aperta per PDE in A_2 (C3-Q2; ostruzioni: niente gcd, Stafford, Landau, quozienti olonomi dei modi separati). Non autonomo: la formula vale, ma senza classe per V(t,x) è vuota.
- **(S) Parziale.** ODE: sì per gradi (VAR-T6 + C12-P5). PDE: no nella forma per elementi (VAR-C7); forma per moduli aperta (C12-Q5).
- **(E) Parziale.** Forma chiusa solo con algebra di Lie finita, cioè V al più quadratico (VAR-P8 + P1-T4/P5/T5); altrimenti Dyson (convergente per V limitato) e splitting con perdita di derivate. Non autonomo: VAR-P9 + VAR-T10.

## 4. Teoremi negativi / ostruzioni
VAR-N1 (classi grandi non identificano); VAR-P4 (spostamento q → q + c); VAR-C7 (Landau); VAR-P8 (niente forma chiusa di E_int oltre il quadratico); sl_2 locale (cos t = 0); VAR-P3 (mal posto di ordine 2, 1/|u| agli zeri).

## 5. Raccomandazioni (criteri fissati nel PLAN, §2)
- **W (Weyl / D-moduli / Loewy): PROMUOVI per le ODE** (enunciati VAR-T2 e VAR-T6, analitici, verificati sui casi minimi, costo: fattorizzazione / minimizzazione D-finita); **PARCHEGGIA per le PDE** (nessuna ostruzione definitiva ma nessun enunciato; C3-Q2 e C12-Q5 restano aperti; Landau elimina solo la forma per elementi).
- **ID-PT (identificazione puntuale/strutturata da una soluzione): PROMUOVI** come strada principale per P-B1 (VAR-T1, VAR-P3, VAR-P4, VAR-P5, VAR-N1 come confine). Avvertenza onesta: il contenuto matematico è elementare; il valore sta nel confine (VAR-N1) e nella stabilità.
- **ID-SP (Sturm–Liouville inverso: Borg, Gel'fand–Levitan, Borg–Marchenko, funzione A): PARCHEGGIA**: unicità e stabilità classiche, ma richiedono dati spettrali/al bordo che il modello M1–M3 non fornisce; resta utile come ponte con F6-ENC (stesso nucleo K) e per il dato in un punto (VAR-Q7).
- **NA (propagatori, Dyson, Magnus, Floquet; C3): PROMUOVI** la tassonomia VAR-T10 e VAR-P9 come input di S8-NA e del contratto di convergenza CONV-T7 di F6-CONV.
- Nessuna strada ELIMINATA.

## 6. Costo e novità
Costo: identificazione strutturata O(1) per punto (più derivazione dei dati); VAR-T2 richiede calcolo dell'operatore minimo (algoritmi di fattorizzazione/minimizzazione per funzioni D-finite, decidibile, costo non stimato qui). Novità (novelty-check senza ricerca web e senza revisore esterno — limite dichiarato): bassa per tutte le affermazioni prese singolarmente (risultati classici o corollari immediati); media come quadro unitario (dicotomia VAR-N1 ↔ G★′-NL punto 2; ciclicità di Galois come analogo di C3-T1; classificazione C3 per algebra di Lie). Nessuna affermazione da presentare come nuova senza CIT-AUDIT.

## 7. Comunicazioni
Inbox letta all'inizio, a metà e alla fine; risposte a F6-CONV (etichette C3, citazioni C1), F6-DICT (classe di V, (H1) = VAR-T1), F6-ENC (identificazione congiunta modulo spostamento, zeri); TABELLA e DOMANDA a F6-SYS (Dirac, gauge, Jacobson).
