# PLAN — R8 · Prior art e strumenti (Fase 1)

Agente: R8 · Data: 2026-10-22 · Cartella: `research/R8/` · Fonte del problema: `D:\piano di ricerca.md` (G★ §1.2, §1.6, Phase 1 tabella riga R8, Phase 5). Notazione: `NOTAZIONE.md` v1.

## 1. Domande

### Dal piano (riga R8 + §1.6 trigger "literature hit")
- **Q1 (posizionamento).** Quali lavori esistenti sono più vicini a G★ = "da UNA soluzione esatta u di una PDE lineare 1D ricostruire L (u ∈ ker L) e scomporre u in componenti per termine, con E_int caratterizzato"? Famiglie: SINDy, PDE-FIND (Rudy et al.), weak SINDy / WSINDy (Messenger–Bortz), operator inference (Peherstorfer–Willcox), symbolic regression (Schmidt–Lipson, AI Feynman, PySR), EPGP (Härkönen–Lange-Hegermann–Raiță), guessing D-finite (Kauers, ore_algebra, gfun, Guess), Prony / FRI (Vetterli–Marziliano–Blu).
- **Q2 (dichiarazione di novità).** Per ciascuna parte di G★ — (i) identificazione di L, (ii) scomposizione per termine u = Σu_n + E_int, (iii) identificabilità esatta, (iv) complessità < O(eⁿ) — cosa è già noto (con fonte), cosa è nuovo, rischio che sia già risolto ⇒ trigger di ri-pianificazione §1.6 (sì/no, con motivazione).
- **Q3 (Mathlib, Fase 5).** Copertura attuale di Mathlib per: spazi di Hilbert/prodotto interno, teorema spettrale (compatto autoaggiunto, matrici hermitiane, C*-calcolo funzionale continuo), ODE (Picard–Lindelöf, Grönwall, unicità), polinomi/ideali/Gröbner?, distribuzioni (stato), semigruppi (C₀/exp di operatori limitati), trasformata di Fourier, algebre di Clifford. Cosa manca per G★.
- **Q4 (CAS).** Capacità di SymPy (dsolve, pdsolve, ODE lineari, operatori differenziali `DifferentialOperator`, holonomic, Gröbner) e SageMath `ore_algebra` (guessing, lclm/gcrd, closure properties, desingolarizzazione) per il ruolo di "controllo simbolico" nelle fasi 3–5.
- **Q5 (ricerca sola, niente costruzione).** Letteratura per Problema 1 (V variabile: inverse Sturm–Liouville, Borg, Gel'fand–Levitan, Marchenko, inverse scattering), Problema 2 (coefficienti matriciali, Dirac 4×4, simboli Clifford-valued, sistemi D-module), Idea I (t-SNE/autoencoder/GMM per PDE discovery).
### Aggiunte motivate
- **Q6 (identificabilità da una traiettoria).** Esistono teoremi di identificabilità di PDE lineari da una sola soluzione (Scholl et al. "uniqueness of PDE discovery", Lu–Qin? "identifiability of linear PDE")? Motivo: tocca direttamente la parte (iii) di G★ e R4/G4 — rischio di sovrapposizione massima.
- **Q7 (sovrapposizioni interne).** Lettura di tutti i PLAN/REPORT di R1–R7, PR-C2a–e, SCOUT-1/2; segnalare duplicazioni (AVVISO).

## 2. Skill (Regola 2) — ordine e uso
1. `academic-research-skills\deep-research\SKILL.md` (Read integrale, workflow di sintesi; `anthropic-skills:deep-research` NON invocato perché orchestra subagenti e io sono già un subagente: equivalente seguito a mano). Uso: struttura domanda → fonti → sintesi → report.
2. `Auto-claude-code-research-in-sleep\skills\research-lit\SKILL.md` + `arxiv`, `semantic-scholar`, `openalex` (Read; le loro query vengono eseguite con WebSearch/WebFetch, NON con gli script vendor). Uso: raccolta e verifica bibliografica.
3. `Auto-claude-code-research-in-sleep\skills\novelty-check\SKILL.md` (Read). Uso: dichiarazione di novità per G★ (Q2).
4. `scientific-agent-skills\skills\citation-management\SKILL.md` (Read). Uso: `sources.bib`.
5. `scientific-agent-skills\skills\scientific-critical-thinking\SKILL.md` (Read). Uso: valutazione del rischio "già risolto" e delle affermazioni di novità (avvocato del diavolo).

## 3. Fonti / stringhe di ricerca previste
- "sparse identification of nonlinear dynamics" Brunton Proctor Kutz 2016; "data-driven discovery of partial differential equations" Rudy 2017; "weak SINDy PDE" Messenger Bortz 2021; "operator inference" Peherstorfer Willcox 2016; "AI Feynman"; "PySR"; "Ehrenpreis-Palamodov Gaussian processes" Härkönen 2023; "guessing holonomic" Kauers; "ore_algebra" Kauers Jaroschek Johansson; "finite rate of innovation" Vetterli 2002; "Prony method annihilating filter"; "identifiability of linear PDE from a single solution"; "uniqueness of PDE discovery" Scholl; "differential elimination Rosenfeld–Gröbner"; "linear differential equation from solution annihilator"; "kernel of linear PDE Gaussian process Lange-Hegermann"; "Mathlib spectral theorem", "Mathlib ODE Picard-Lindelöf", "Mathlib distributions", "Mathlib Fourier transform", "Mathlib Clifford algebra"; "inverse Sturm-Liouville Gel'fand-Levitan", "Borg uniqueness theorem", "Dirac operator inverse problem matrix potential"; "autoencoder PDE discovery latent coordinates Champion 2019".

## 4. Comunicazione
- Leggo TUTTI: `research/*/PLAN.md|REPORT.md` e `inbox/*.md` a metà lavoro; AVVISO agli interessati + `inbox/central.md` per sovrapposizioni.
- Contatti attesi: R4 (Prony/FRI, inverse Sturm–Liouville, guessing — sovrapposizione certa: io faccio POSIZIONAMENTO, R4 fa la teoria), R2 (EPGP, D-finite), R1 (sparsità/SINDy ↔ L¹), R6/R7 (Clifford, Dirac per Problema 2).
- NEW-ROUTE a `inbox/central.md` se emerge una strada nuova.

## 5. Criterio di "fatto"
- `REPORT.md` con: tabella prior art (metodo · dato richiesto · esatto/numerico · identifica L? · scompone u? · garanzie) + dichiarazione di novità per G★ con rischio e verdetto sul trigger §1.6 + sezione Mathlib/SymPy/ore_algebra + sezione Problema 1/2/Idea I; ogni affermazione con fonte (stato noto/aperto/probabilmente falso).
- `sources.bib` con tutte le fonti citate; `open_questions.md`; AVVISI inviati; `DONE R8` in `inbox/central.md`.
