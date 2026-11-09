# GATE 4a — scelta delle strade non lineari (v2 del coordinatore, 26/10/2026, dopo DEVIL-4 e CIT-AUDIT-4)
Fonti: `research/F4-{ALG,LIN,INT,LIFT,HOR}/VERDETTO.md` (5/5), `research/DEVIL/ATTACK-4.md` (kill-argument **FAIL** sulla v1 di questa proposta), `research/CIT-AUDIT/AUDIT-4.md`, `FASE4_SCOUTING.md`, `GATE3.md`. Nessun enunciato di Fase 4 è DIMOSTRATO.

## 0. Perché questa è la v2
La v1 proponeva quattro sessioni (S4-IST, S4-CH, S4-MOD, S4-LIFT). L'avvocato del diavolo l'ha bocciata, e il coordinatore accoglie le due obiezioni critiche dopo averle verificate:
- **O1 (verificata a mano):** la colonna "E_int sì" della v1 metteva sotto lo stesso nome cinque oggetti diversi (E^trop, E^NL, u − Σ 1-solitoni, interazione fra modi di NF-1, E^mix). Nessuno è l'E_int della tua domanda (A9; NOTAZIONE v2: E_int^add = u − u₀ − Σ_n(S_n u₀ − u₀), con S_n il flusso del **solo** termine n). Su Burgers con u₀ = ε sin x: E_int^A9 = (3/2)νt²ε² sin 2x + …, che è l'anticommutatore dei due termini, mentre "E^NL" al primo ordine è solo t·B(u₀). **Nessuna sessione della v1 aveva come obiettivo la domanda per termine.**
- **O2:** "u identifica nell'anello intero" (ALG-T1) vale solo per u con grado di trascendenza infinito, quindi per nessun dato in forma chiusa (modello M1). Tutte le identificazioni utili sono relative a una classe o a un dizionario.
- Accolte anche: O3 (le prove chiave sono corollari brevi di fatti classici: vanno trattate come lemmi da auditare, non come obiettivi), O4 (risultati su ℝ, G★′ è su Ω limitato; doppio standard sulla continuazione analitica tra PAINLEVÉ e INT-T1), O5 (MON/splitting scartato per errore: è il solo quadro in cui il flusso del solo termine non lineare esiste dopo lo shock), O6 (criteri d'uscita non verificabili), O8 (manca un enunciato bersaglio non lineare).
**CIT-AUDIT-4** aggiunge: ALG-T1 è in parte anticipato da Scholl et al. (Mach. Learn. 115 (2026) 139, Prop. 1 / Thm 2); la costante 4ν ln 2 di F4LIN-T2 è un calcolo elementare (Wang 1998, SIAM J. Math. Anal. 30, 38–52); F4L-P3 **non** ha fonte classica trovata e corregge Kieffer et al. (arXiv:2512.12019, che sostiene raggio infinito ma ha un polo a δ = iπ/Re nella propria formula); Saut–Scheurer 1987 copre la continuazione unica solo al 3° ordine (KdV, M = 1).

## 1. Enunciato bersaglio non lineare (proposta, da approvare: G★′-NL)
Equazione scalare 1D u_t = Σ_{n=1}^N T_n(u), con T_n lineari a coefficienti costanti o non lineari polinomiali nel jet (banchi: Burgers, KdV–Burgers, Fisher–KPP; integrabili solo come controllo), su Ω limitato semplicemente connesso, dato una soluzione esatta u (modello M1/M2/M3 come in Fase 3).
1. **Termine d'interazione (la tua domanda):** con S_n(t) il flusso (non lineare) del solo termine T_n, dove esiste (per i termini iperbolici: soluzione entropica, Kružkov; Brezis–Pazy), studiare E_int^add = u − u₀ − Σ_n(S_n u₀ − u₀) e l'errore di splitting E^mult = S − S_1⋯S_N: forma chiusa, stima in (t, ε, ν), costo, oppure teorema negativo.
2. **Identificazione relativa a un dizionario 𝓓:** criterio esatto per I(u) ∩ span(𝓓) = ⟨F⟩ (generalizza Gram/C3-L1 e C3-T1); dicotomia "forma chiusa ⇒ non identifica" enunciata come teorema; classi speciali (𝓗_M per KdV/NLS, dizionari di Hammerstein) come casi.
3. **Trasporto dei risultati lineari** attraverso Cole–Hopf, IST, sollevamento, come lemmi con riduzione classica dichiarata.

## 2. Proposta del coordinatore (v2, recepisce la raccomandazione di DEVIL-4)
| sessione | contenuto | criterio d'uscita (datato, verificabile) |
|---|---|---|
| **S4-TERM** (prioritaria) | punto 1 di G★′-NL: E_int^add e E^mult nel senso A9 per Burgers (prima e oltre lo shock), poi KdV–Burgers e Fisher–KPP (non integrabili). Strumenti: MON/splitting (Kružkov, Brezis–Pazy, riammesso), forma normale NF-1, LIN-Q3, F4L-P2, i lemmi lineari di Fase 3 (P1-T2, P1-T4/T5, P3-T1) | entro una sessione: o una stima di ordine t² (o un ordine esplicito) valida oltre lo shock, o un **teorema negativo** registrato; predizione da scrivere nel PLAN prima di partire |
| **S4-ID** | punto 2: identificazione relativa a un dizionario; MODREL + linguaggio di F4-ALG (ALG-T1 con u analitica), INT-T1 come caso 𝓗_M, MON-1 (flusso f identificato senza dizionario); dicotomia come teorema; INT-Q1 con limite di tempo | criterio esatto per Burgers e KdV con dizionari polinomiali di grado ≤ d, oppure controesempio; delta di novità rispetto a Scholl et al. e He–Zhao–Zhong dichiarato |
| **S4-INTEG** (corta, solo audit) | punto 3: INT-T1/T2, F4LIN-T2, F4L-P3 (con il confronto con Kieffer et al.), Hirota, ALG-L1/T1/P3/P4/P6, MODREL-T1 portati a DIMOSTRATO come lemmi di trasporto, riduzione classica e modello di dato dichiarati; versione su Ω limitato o limite esplicito (O4) | fine quando ogni lemma è DIMOSTRATO, CON-FONTE o FALSO |
Più S-CHECK (revisore) e uno scout di orizzonte. **S4-LIFT autonoma scompare**: il sollevamento e la forma normale entrano in S4-TERM come strumenti; F4L-P3 entra in S4-INTEG.

## 3. Strade (proposta per ROUTES.md)
PROMUOVI: RT-TERM (nuova: E_int non lineare nel senso A9, splitting); RT-R7a ristretta a 𝓗 (come caso di S4-ID / lemma di S4-INTEG); MODREL. **Riammessa**: MON/splitting (dentro RT-TERM). Lemmi (non strade autonome): RT-R7b (Cole–Hopf tropicale), Carleman + NF, F4-ALG (linguaggio comune). PARCHEGGIA: Koopman (nota O9: le autofunzioni, non gli autovalori, portano il termine non lineare: riaprire con NF), PAINLEVÉ, NLSPEC, HAANTJES. ELIMINA: SPLIT-f come strada (SPLIT-L1 resta lemma: descrive lo schema di splitting a due cornici).

## 4. Decisioni che spettano a te
1. Approvi **G★′-NL** (§1) come enunciato bersaglio della Fase 4, in particolare la definizione A9 di E_int con i flussi dei singoli termini non lineari?
2. Approvi le tre sessioni della v2 (S4-TERM prioritaria, S4-ID, S4-INTEG) in parallelo?
3. Le decisioni sulle strade del §3 ti vanno bene?

---
## ESITO DEL GATE 4a (26/10/2026) — decisione dell'utente
Approvati: G★′-NL (§1, con la definizione A9 di E_int con i flussi dei singoli termini), le tre sessioni S4-TERM, S4-ID, S4-INTEG **in parallelo**, e le decisioni sulle strade del §3. Registrato in PROBLEM.md (G★′-NL), NOTAZIONE.md (v3), ROUTES.md, SESSIONS.md (roster Fase 4).
