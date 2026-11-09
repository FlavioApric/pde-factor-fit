# PLAN — F4-LIN · Fase 4, sprint di scouting · strada (iv) linearizzazioni esatte
Agente F4-LIN · 26/10/2026 · regole: FASE4_SCOUTING.md (lette per intero), PROTOCOLLO.md, skills-local/session-protocol.
Stato: scouting preparatorio e reversibile. Nessun DIMOSTRATO, nessuna promozione: si propone, decide il Gate 4a.

## 0. Skill caricate (dichiarazione)
Lette per intero e seguite (nessuno script _vendor eseguito):
1. `skills-local/session-protocol` (per prima), `skills-local/route-scout` (nota → PLAN → ricerca/prova → verdetto di 1 pagina → riga ROUTES), `skills-local/claim-lifecycle` (stati; qui solo "candidato" / "prova scritta" / V-ex).
2. `_vendor/Auto-claude-code-research-in-sleep/skills/research-lit/SKILL.md`: solo fonte `web` (WebSearch/WebFetch); nessun Zotero/Obsidian/PDF locale (avviso D2: "local contributed nothing").
3. `_vendor/Auto-claude-code-research-in-sleep/skills/novelty-check/SKILL.md`: fasi A, B, D; fase C (revisore Codex) esclusa per decisione dell'utente → REVIEW_UNAVAILABLE, giudico io sotto i NOVELTY VERDICT LIMITS.
4. `_vendor/math-skill/SKILL.md`, modo `proof` (esplorazione separata dalla prova, controesempi presto).
5. `_vendor/Auto-claude-code-research-in-sleep/skills/formula-derivation/SKILL.md`: per ogni derivazione distinguo identità / proposizione / approssimazione / interpretazione (NOTE.md).
6. `_vendor/scientific-agent-skills/skills/sympy/SKILL.md`: script in `research/F4-LIN/sympy/`, `D:\ProblemaBase\.venv\Scripts\python.exe -I`, solo come verifica.

## 1. Domanda decisiva
Attraverso una mappa linearizzante esatta Λ (Cole–Hopf u = −2ν∂_x log φ; Cole–Hopf tropicale ν→0; Miura; Darboux/Bäcklund), quali dei tre risultati lineari di Fase 3 sopravvivono?
- (I) identificazione: C3-T1 (Ann(u) = (P) ⟺ test EP), C3-T3 (jet 2d−1), P4-T2;
- (S) scomposizione: C12-T1′ (fattori, Ω semplicemente connesso), P1-T2 (termini nella classe 𝔅);
- (E) E_int: P1-T3 (costo), P1-P1(e) (non continuità in H^m), stime TROP-3/4.
Banco di prova: Burgers u_t + uu_x = νu_xx; poi KdV/mKdV (Miura, Darboux).

## 2. Sotto-domande (con item / appunti)
- Q1 (I, Cole–Hopf): la mappa u ↦ φ è ben definita su Ω? (dove serve H¹_dR(Ω) = 0, legame con C12-T1′/C12-P10). Ann(φ) si traduce in relazioni differenziali su u? C3-T1 e C3-T3 si trasportano? [C3, G4, G7, A6]
- Q2 (S, Cole–Hopf): la scomposizione per fattori del calore (banale: τ−νξ² irriducibile, O1/G8) e la sovrapposizione φ = Σφ_j danno una scomposizione di u? è canonica (rappresentazione di Widder dei calori positivi su ℝ)? cosa succede su Ω limitato? i *termini* di Burgers (uu_x, νu_xx) corrispondono a termini del calore? [A8, A9, C2, P1, B3, D1]
- Q3 (E, Cole–Hopf / tropicale RT-R7b): forma chiusa di E_int (pesi softmax), stima esplicita in ν nel limite di Hopf–Lax, in quali norme, costo; confronto con P1-P1(e) e con la velocità classica di viscosità evanescente. [P1, B2, B3, D1, TROP-L2]
- Q4 (Miura): è una linearizzazione? cosa trasporta (I) tra mKdV e KdV? legame con fattorizzazione dell'operatore di Lax (Loewy/LCLM di Fase 3, II-T9). [G5, G7]
- Q5 (Darboux/Bäcklund/Crum): componente = autofunzione del seme; E_int a coppie dal Wronskiano; legame con "componente = fattore" e con la formula di Vandermonde C12-T2. [C2, P1, B2]

## 3. Criteri fissati PRIMA di cercare (non si cambiano dopo)
### RT-R7b (Cole–Hopf tropicale) — criterio di ROUTES: "promuovi in Fase 4 con stima di E_int in ν"
- **PROMUOVI** se valgono entrambe: (P-a) una stima esplicita di E_int in ν (costante esplicita, norma dichiarata) su una classe non banale (miscele di N ≥ 2 componenti, N arbitrario), con prova scritta e controllo SymPy; (P-b) almeno uno fra I/S/E trasportato con un enunciato candidato collegato a un teorema di Fase 3 (non solo la velocità classica di viscosità evanescente).
- **PARCHEGGIA** se la stima esiste solo come risultato classico già pubblicato senza contenuto strutturale nuovo per G★′, oppure solo per N = 2, oppure se (P-b) fallisce.
- **ELIMINA** se E_int non ammette stima in ν in nessuna norma ragionevole (resta O(1) uniformemente), oppure se la scomposizione tropicale non è intrinseca nemmeno su ℝ (rappresentazione non unica senza principio di selezione).
- Novelty: un ABANDON della novelty-check (articolo pubblicato nominato che contiene il risultato) non elimina la strada ma ne declassa gli enunciati a CON-FONTE da verificare; la raccomandazione si basa sul contenuto per G★′.
### Le altre linearizzazioni (Cole–Hopf propria, Miura, Darboux/Bäcklund)
- **PROMUOVI** se trasportano almeno due fra I/S/E con enunciati candidati, e c'è un cammino senza ostruzioni note verso un teorema L5 per Burgers o KdV.
- **MERGE in RT-R7a (F4-INT)** se il contenuto utile è tutto nella coppia di Lax / IST (la mappa serve solo da strumento).
- **PARCHEGGIA** se trasporta un solo risultato.
- **ELIMINA** se non trasporta nulla oltre l'identità classica.

## 4. Caso di prova minimo
L5-Burgers: (a) 1 fronte φ = 1 + e^{kx+νk²t} (non identificante, simmetria); (b) N onde piane φ = Σ e^{−(c_i x − c_i² t/2 − β_i)/2ν}; (c) dato iniziale generale (Widder). KdV: 1- e 2-solitone via Crum (Wronskiano), Miura su v = tanh-tipo.

## 5. Script SymPy previsti (research/F4-LIN/sympy/)
- `ch_gauge.py`: potenziale ψ (forma chiusa ⟺ Burgers), φ calore, operatori coniugati D = ∂ + ∇g commutanti, B_Q[u] = φ^{-1}Q(∂)φ; 1-fronte: τ − νkξ ∈ Ann(φ) ⟺ u_t = νk u_x; jet di φ come polinomi nel x-jet di u; flussi dei termini di Burgers in φ (non lineari).
- `trop_burgers.py`: log-sum-exp −2ν log N ≤ ψ^ν − ψ^0 ≤ 0; L¹ dello shock = 4ν ln 2, L² = 4νΔ(ln 2 − 1/2); scaling Ḣ^s; controllo numerico N = 3.
- `miura_darboux.py`: Miura = fattorizzazione −∂² + u = (−∂ + v)(∂ + v) con u = v² − v_x; iniettività dell'omomorfismo sui jet; Crum N = 2 → Hirota A_12.

## 6. Fonti / stringhe di ricerca
Hopf 1950 (CPAM 3), Cole 1951 (Q. Appl. Math. 9), Widder 1944 (Trans. AMS 55), Kuznetsov 1976 (velocità √ν), Tang–Teng (velocità per soluzioni regolari a tratti), Maslov / Litvinov (dequantizzazione), Kolokoltsov–Maslov 1997, Dimakis–Müller-Hoissen (limite tropicale KP / Burgers), Miura 1968, Crum 1955, Matveev–Salle 1991, Freeman–Nimmo 1983, Drinfeld–Sokolov / Adler (Miura = fattorizzazione), Tokihiro et al. 1996 (box-ball), Holden–Lubich–Risebro (splitting per Burgers). Stringhe: "Cole-Hopf tropical limit Burgers shock", "Maslov dequantization Burgers", "vanishing viscosity rate L1 Burgers piecewise smooth", "Widder positive temperatures representation", "Miura transformation factorization Schrodinger operator", "Crum Wronskian Darboux soliton".

## 7. Contatti
- F4-ALG (hub): TABELLA "mappa Λ → ideale differenziale": cosa diventa Ann(φ) nell'ideale differenziale di u (sotto-ideale "linearizzabile" B_Q), iniettività dell'omomorfismo di Miura sui jet. Ricevo: la loro definizione di ideale e identificabilità.
- F4-INT: Miura = fattorizzazione dell'operatore di Lax; Darboux/Crum = scambio di fattori / Wronskiano; chiedo il loro stato su identificazione da una soluzione (RT-R7a/c).
- central: PLAN-READY, TABELLA righe ROUTES, DONE.
Lettura inbox/F4-LIN.md: all'inizio (vuota, 26/10), a metà, prima di consegnare.

## 8. Criterio di "fatto"
PLAN, NOTE (lavoro di dettaglio con enunciati candidati), VERDETTO di 1 pagina con risposte I/S/E per ciascuna mappa e raccomandazioni secondo §3, sources.bib (verificati / da verificare), open_questions.md, sympy/ con output; TABELLA in central; DONE F4-LIN.
