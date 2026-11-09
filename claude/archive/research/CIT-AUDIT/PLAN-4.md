# PLAN-4 — CIT-AUDIT-4 (Fase 4, fonti portanti dei verdetti di scouting, prima del Gate 4a)

Data: 2026-10-26 · Agente: CIT-AUDIT-4 · Input: GATE4A.md (bozza), research/F4-{ALG,LIN,INT,LIFT,HOR}/{sources.bib, VERDETTO.md, NOTE.md}, inbox/central.md (TABELLE degli scout), metodo di PLAN-3/AUDIT-3.

## 1. Domande (voce → enunciato candidato che la usa)
| # | voce | usata in | cosa verificare |
|---|---|---|---|
| A1 | Widder 1944 TAMS 55; Widder 1975 *The Heat Equation* | F4-LIN (S) canonicità su ℝ, Choquet/Widder ↔ Ehrenpreis positiva (RT-R7b) | metadati; enunciato: calore positivo su ℝ×(0,T) = Gauss–Weierstrass di un'unica misura positiva |
| A2 | Tang–Teng 1997 Math. Comp. 66; W.-C. Wang 1998 (SIAM J. Math. Anal.?) | F4LIN-T2 (novità della stima 4ν ln 2, confronto ν|log ν|) | metadati, enunciati O(ν), O(ν|log ν|), ottimalità |
| A3 | Miura 1968 J. Math. Phys. 9 | ALG-P6, F4LIN-L2 | metadati, trasformazione di Miura |
| A4 | Freeman–Nimmo 1983 Phys. Lett. A 95 | F4LIN-P7 (Wronskiano N-solitone) | metadati, enunciato |
| A5 | Kay–Moses 1956 J. Appl. Phys. 27 | INT-T1 (E) Hirota/det(I+C), O(N³) | metadati, potenziali senza riflessione via determinante |
| A6 | Deift–Trubowitz 1979 CPAM 32 | INT-T1 (F2: mappa di scattering) | metadati, enunciato |
| A7 | Saut–Scheurer 1987 JDE 66 | INT-T1 su Ω limitato (continuazione unica) | esistenza, metadati, copertura (ordine 3 in x?) |
| A8 | Novikov 1974 Funct. Anal. Appl. 8 (equazione stazionaria) | INT-T1 (N-solitone in 𝓗_N), ALG-P3 | metadati, enunciato |
| A9 | Kolchin 1964 Bull. AMS; Kolchin 1973; Ritt 1950 (Ritt–Raudenbush) | ALG-T1-gen, ALG-O1 | volume/pagine, Thm 4 (polinomio di dimensione), teorema della base |
| A10 | van der Put–Singer 2003 | ALG-P6 viceversa (Galois SL₂) | metadati; sezione |
| A11 | Kumei–Bluman 1982 SIAM J. Appl. Math. 42 | RT-H2 WIENER | metadati, criterio |
| A12 | Chudnovsky 1977 Nuovo Cimento B 40 | POLE-1 | metadati, contenuto |
| A13 | Weiss–Tabor–Carnevale J. Math. Phys. 24 (1983) | PAINLEVÉ | anno, DOI |
| A14 | Forets–Pouly 2017 arXiv:1711.02552 | F4L-P2 (noto in sostanza) | esistenza, contenuto |
| A15 | Page–Kerswell 2018 PRFluids 3 | Koopman (PARCHEGGIA), F4L-P5 | metadati, contenuto |
| A16 | Boreale–Collodi arXiv:2606.24473 | F4L-P2(b) | esistenza, contenuto; contiene F4L-P3? |
| A17 | Kieffer et al. arXiv:2512.12019 | F4L-P3 (distinzione) | esistenza; contiene il raggio in ampiezza? |
| A18 | Byrne et al. arXiv:2402.04241 | ALG-T1 (vicinanza) | esistenza, versione a stampa; tratta una soluzione singola? |
| A19 | Scholl et al. arXiv:2210.08342 | ALG-P3, INT-T1 (1-solitone) | esistenza, Example 1, Thm 2 |
| A20 | Rudy et al. 2017 Sci. Adv. 3 e1602614 | ALG (1-solitone) | metadati |
| A21 | Fujita 1966 J. Fac. Sci. Tokyo 13 | F4L-O1 | metadati, esponente critico |
| A22 | Burger–Gilboa et al. 2016 SIAM J. Imaging Sci. 9 | NLSPEC | metadati |
| A23 (extra) | Hopf 1950; Cole 1951; Lax 1968; AKNS 1974; Hirota 1971 | trasversali | metadati rapidi |
**Priorità di priorità (novità):** possibili anticipazioni di F4L-P3 (raggio 2πν/osc(U₀) in ampiezza per Burgers), INT-T1 (identificazione in 𝓗_M ⟺ |Λ| ≥ M+1), MODREL-T1 (rango del modulo delle sizigie), ALG-T1 (I(u) = [F] ⟺ trdeg = ∞ per una singola soluzione).

## 2. Skill (lette con Read; nessuno script `_vendor` eseguito)
1. `skills-local/session-protocol/SKILL.md` (per prima).
2. `_vendor/scientific-agent-skills/skills/citation-management/SKILL.md`: metadati da Crossref/OpenAlex/arXiv; mai inventare volume, pagine, DOI; log delle fonti.
3. `_vendor/scientific-agent-skills/skills/paper-lookup/SKILL.md`: provenienza ripetibile; una risposta 200 vuota o una pagina a pagamento non conferma; dichiarare i vuoti.

## 3. Fonti
Crossref API (`api.crossref.org/works?query.bibliographic=`), arXiv abs/API, OpenAlex, pagine editore; WebSearch per le anticipazioni (stringhe: "Burgers equation analytic in amplitude radius of convergence 2πν", "Carleman linearization Burgers convergence Reynolds number", "identifiability KdV hierarchy reflection coefficient", "differential ideal of a solution identifiability transcendence degree", "Hammerstein syzygy PDE identification"). Gradi come AUDIT-3: SÌ (primaria) / SÌ (secondaria) / PARZIALE / NO.

## 4. Comunicazione
PLAN-READY in inbox/central.md; alla fine TABELLA + DONE CIT-AUDIT-4. Scrivo solo in research/CIT-AUDIT/ e inbox/central.md.

## 5. Criterio di fatto
research/CIT-AUDIT/AUDIT-4.md con tabella (voce | usata in | esiste | metadati | enunciato verificato | fonte della verifica | azione) per A1–A22 (+A23), sezione "anticipazioni dei candidati nuovi", provenienza; TABELLA in central; DONE.
