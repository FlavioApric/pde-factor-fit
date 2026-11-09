# PLAN — PR-C2c (Asse 1, T10–T12: non lineari/integrabili, modelli applicati, stocastici)

Data: 2026-10-22. Fonte del compito: `D:\piano di ricerca.md` §1.3-C2-EXT, §1.3-C2-TAX (T10–T12), card schema, PR-C2 (PR-C2.3), Phase 1 (paragrafo PR-C2), Phase 4. Notazione: `NOTAZIONE.md` (in particolare G7).

## 1. Domande
Per ognuno dei 16 item del blocco — T10: C2.15, C2.16, C2.24, C2.44, C2.45, C2.47; T11: C2.26, C2.27, C2.28, C2.29, C2.32, C2.33, C2.40, C2.43, C2.57; T12: C2.41:
- Q1 (PR-C2.3, scheda breve) operatore canonico (forma 1D quando esiste), classe del nucleo / delle soluzioni, tag, 2 fonti.
- Q2 (richiesta del coordinatore) esiste una trasformazione ESATTA che linearizza o separa le componenti? (Cole–Hopf, IST, hodografo, Miura, Hirota, Feynman–Kac, Fourier/modi, …) Con quale classe di funzioni a valle.
- Q3 come si presenta l'"interazione" tra componenti (E_int non lineare): sfasamenti dei solitoni, termini di Hirota, accoppiamento di modi, assenza di sovrapposizione, ecc.
- Q4 (aggiunta motivata, da G7 e A6) in che misura l'identificazione u ↦ L resta LINEARE nei coefficienti quando il dizionario contiene monomi del jet (u u_x, u², …) e dove il nucleo smette di essere uno spazio vettoriale.
Schede dettagliate (★/Fase 4) con verifica SymPy:
- D1 Burgers u_t + u u_x = ν u_xx ↔ Cole–Hopf ↔ calore (V·V_x di A6). Verificare: trasformazione, soluzione a N-"modi" (somma di esponenziali in φ), onda viaggiante tanh, E_int in coordinate u vs φ.
- D2 KdV u_t + 6u u_x + u_xxx = 0: 1-solitone, 2-solitone (Hirota), sfasamento di fase, trasformazione di Miura (mKdV → KdV), Lax pair L = −∂² + ... ; il potenziale riflessionless ↔ IST.
- D3 Trave Euler–Bernoulli u_tt + c² u_xxxx = 0 (★ 1D): simbolo, relazione di dispersione ω = ±cκ², fattorizzazione (∂_t − i c∂_x²)(∂_t + i c∂_x²) = Schrödinger × Schrödinger coniugato ⇒ nucleo = somma di due nuclei di Schrödinger (caso G2!), modi ODE {cos, sin, cosh, sinh}(βx), nucleo fondamentale.
Verifiche brevi aggiuntive (se il tempo lo consente): sine-Gordon kink/Bäcklund, Hopf–Cole per ν→0 (onde d'urto), Feynman–Kac per calore con potenziale.

## 2. Skill (Regola 2: tool Skill se disponibile, altrimenti Read del SKILL.md)
1. `academic-research-skills\deep-research\SKILL.md` — letta (Read) per il workflow (domanda → fonti → sintesi → verifica fonti). NON invoco `anthropic-skills:deep-research` via Skill perché coordina sub-agenti e questo agente non deve generarne altri; seguo il workflow a mano con WebSearch.
2. `scientific-agent-skills\skills\paper-lookup\SKILL.md` e `Auto-claude-code-research-in-sleep\skills\arxiv\SKILL.md` — lette; uso solo le istruzioni (nessuno script _vendor), con WebSearch/WebFetch per verificare DOI/arXiv delle fonti chiave.
3. `scientific-agent-skills\skills\sympy\SKILL.md` + `math-skill\SKILL.md` (modalità solver) — lette; script in `research/PR-C2c/sympy/`, eseguiti con `D:\ProblemaBase\.venv\Scripts\python.exe -I`.
4. `scientific-agent-skills\skills\citation-management\SKILL.md` — letta; `sources.bib` in BibTeX con DOI quando verificabili.

## 3. Fonti / stringhe di ricerca
Classici: Whitham *Linear and Nonlinear Waves* (1974); Hopf 1950 (CPAM 3:201); Cole 1951 (QAM 9:225); Gardner–Greene–Kruskal–Miura 1967 (PRL 19:1095); Lax 1968 (CPAM 21:467); Miura 1968 (JMP 9:1202); Zakharov–Shabat 1972; Ablowitz–Kaup–Newell–Segur 1974 (Stud. Appl. Math. 53:249); Ablowitz–Segur *Solitons and the IST* (SIAM 1981); Hirota 1971 (PRL 27:1192) e *The Direct Method in Soliton Theory* (CUP 2004); Drazin–Johnson *Solitons: an introduction* (CUP 1989); Evans *PDE* (AMS); Dafermos *Hyperbolic Conservation Laws*; Lax 1957 (CPAM 10:537); Kruzhkov 1970; Sandstede (stabilità onde viaggianti, Handbook 2002); Kapitula–Promislow (2013); Fujita 1966; Majda–Bertozzi; Batchelor; Vallis; Jackson; Landau–Lifshitz *Elasticity*; Graff *Wave motion in elastic solids*; Timoshenko; Cercignani; Villani; Crank *Free and moving boundary problems*; Berkolaiko–Kuchment *Quantum Graphs* (AMS 2013); Walsh 1986; Da Prato–Zabczyk; Kac 1949; Hairer 2014 (KPZ/regularity structures); Polyanin–Zaitsev *Handbook of Nonlinear PDEs*; Fokas (unified transform).
Stringhe: "Cole-Hopf transformation Burgers linearization", "inverse scattering KdV soliton phase shift", "Miura transformation", "hodograph transformation linearize", "Euler-Bernoulli beam dispersion relation fundamental solution", "Fokas unified transform beam", "linearizable PDE C-integrable Calogero", "Koopman Burgers Cole-Hopf".

## 4. Comunicazione
- Inbox propria `inbox/PR-C2c.md`: all'inizio (vuota), a metà, prima di consegnare.
- → R7 (`inbox/R7.md`, TABELLA): schede sulle linearizzazioni esatte (Cole–Hopf, IST, Miura, hodografo, Hirota) — Fase 4.
- → R3 (`inbox/R3.md`, TABELLA): scheda trave Euler–Bernoulli (★ 1D).
- → PR-C2e (`inbox/PR-C2e.md`, TABELLA): attributi S1–S15 di ciascun item del blocco (riga sintetica).
- → central: `PLAN-READY PR-C2c`, eventuali `NEW-ROUTE`, `DONE PR-C2c`.

## 5. Criterio di "fatto"
- 16 schede brevi in `cards/` (una per item) con operatore, classe nucleo/soluzioni, tag, ≥2 fonti, risposta a Q2/Q3.
- 3 schede dettagliate (Burgers, KdV, Euler–Bernoulli) con script SymPy eseguiti e output citato.
- `REPORT.md` (risultati mappati su item C/P/II/Phase 4, enunciati precisi con fonte, stato noto/aperto/probabilmente falso), `sources.bib`, `open_questions.md`.
- Messaggi a R7, R3, PR-C2e inviati; `DONE PR-C2c` in central.
