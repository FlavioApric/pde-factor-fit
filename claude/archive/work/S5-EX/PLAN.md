# PLAN — S5-EX (Fase 5, requisito "Verification" del piano: esempi da manuale contro la teoria)
Data: 26/10/2026. Agente: S5-EX. Scrive solo in work/S5-EX/ e inbox/.

## Compito
Piano `D:\piano di ricerca.md`, sezione "Verification": *"Known textbook examples are checked against the theory: heat equation, Airy, Bessel, and transport + diffusion as a case with E_int."* Mai fatto come consegna dedicata. Per ogni esempio: soluzioni esatte esplicite (generiche e degeneri, es. EP), controllo SymPy delle predizioni dei teoremi principali; dove un teorema non si applica, dirlo con l'ipotesi che manca. Ogni discrepanza teoria/esempio = CONFLITTO in inbox/central.md con la prova.

## Skill caricate (lette come SKILL.md)
1. `skills-local/session-protocol` (passi 0–4: piano, inbox, consegna, DONE).
2. `skills-local/claim-lifecycle` — qui solo per lo **stato V-ex**: i controlli su esempi non alzano lo stato di nessun claim; le righe proposte sono "V-ex (esempi da manuale)" e non sostituiscono le prove. Nessun proof-checker/kill-argument (non ci sono enunciati nuovi; le osservazioni fuori dai teoremi sono marcate "osservazione, non claim").
3. `_vendor/scientific-agent-skills/skills/sympy` e `_vendor/math-skill` (modo verifica): solo come guida; nessuno script `_vendor` eseguito.

## Esempi × teoremi (matrice da verificare)
| # | esempio | operatore P (τ↔∂_t, ξ↔∂_x) | soluzioni esatte | teoremi |
|---|---|---|---|---|
| E1 | calore | τ − ξ² (e (τ−ξ²)²) | G = t^{-1/2}e^{-x²/4t}; tG; x²+2t; x³+6tx; e^{-k²t}sin kx; (x²+2t)+e^{t+x}; G+e^{t+x} | C3-T1(a,d), C3-T4, C3-T6 (G_u per P = (τ−ξ²)²), P4-T2 (σ_p, G_u, J_u, R·u∩EP), C3-T3 (jet 2d−1 per dati EP, ottimalità), C3-C2 |
| E2 | trasporto + diffusione (AD) | τ + cξ − Dξ² (termini a₁ = −cξ, a₂ = Dξ²) | nucleo AD G_AD; 1, x−ct, (x−ct)²+2Dt, (x−ct)³+6Dt(x−ct); e^{a(ζ)t+ζx}; e^{cx/D} (stazionario) | C3-T4, C3-T3, **P2-T2** (span{1,x−ct,(x−ct)²+2Dt}, g = −cDξ³, scomposizione nei D_n), **P1-T2** (i)–(iv) (E^add chiuso, getto formale, molteplicità), P1-E1, **P1-T3** (DP O(N²) vs tabella 2^N, conteggio operazioni), P1-P1(e) (non continuità, rapporto), **P3-T1** (criterio (Par)), **P3-P1/P3-T3** (elementi di matrice Dirichlet V_mn, φ, esponente 5/4 di E^{mult,(1)} dal bordo) |
| E3 | calore × trasporto (caso a due fattori) | (τ−ξ²)(τ+cξ); e (τ−ξ²)(τ−ξ²−1) | G + f(x−ct) (f gaussiana), G + e^{x−ct} | **C12-T1′** (δ(P) = 2, 𝒩 = span{1, e^{c²t−cx}}; δ = 0 e proiettori per varietà disgiunte), C3-T1(a,d) con testimone, C3-T6, P4-T2 |
| E4 | Airy (PDE) | τ + ξ³; e τ + cξ + ξ³ (KdV lineare) | soluzione fondamentale (3t)^{-1/3}Ai(x/(3t)^{1/3}); x³−6t; e^{ζx−ζ³t} | C3-T4/C3-T1(d) (libertà del t-getto), C3-T3, P2-T2 (K = 4), P1-T2 (getto), P3-T1 (Par **fallisce**: q dispari) |
| E5 | Airy (EDO) | ∂_x² − x ∈ A_1 | Ai, Bi, e^{μt}Ai(x+μ) per ∂_t − ∂_x² + x | P4-C1 (ρ_u iniettiva, non informativa), OP-ALG-T4 (m = 1: identifica ⟺ u ∉ 𝒯), OP-ALG-P5 (A_2), OPR2-T3 (P = ∂_t(∂_t − x), test D_i); quali **non** si applicano |
| E6 | Bessel | x∂_x² + ∂_x + x ∈ A_1; radiale x∂_t − ∂_x x ∂_x ∈ 𝒟 | J_0; e^{-k²t}J_0(kx); nucleo radiale t^{-1}e^{-x²/4t} | P4-C1; OP-ALG-T4/OPR2-T3: ipotesi "P monico in ∂_t" **non** soddisfatta (coefficiente x); cosa resta dopo la localizzazione su Ω ⊂ {x>0}; C3/C12/P1/P2/P3 non applicabili (coefficienti variabili) |

## Metodo SymPy
Script autonomi in `work/S5-EX/sympy/` (eseguiti con `.venv\Scripts\python.exe -I`, nessun import locale): `ex1_calore.py`, `ex2_AD.py`, `ex3_due_fattori.py`, `ex4_airy.py`, `ex5_bessel.py`; output `*.out` con righe `[OK]/[FAIL] <id>`.
- Ann(u) ∩ R_{≤n} per u EP: calcolo **diretto** (Q(∂)u raccolto per esponenziali, identità polinomiale), non tramite C3-T2(a), per non usare la teoria nel controllo.
- Jet: sistema lineare ∂^β(Q(∂)u)(p₀) = 0, |β| ≤ k; confronto di sottospazi.
- dim R/I con base di Gröbner (grevlex) e conteggio dei monomi standard.
- Non-EP: crescita del grado di ∂_x^k u/u (gaussiane) o sistemi lineari di relazioni con coefficienti polinomiali (Airy/Bessel) — dove la prova è solo fino a un ordine, lo dico (V-ex).

## Criterio di "fatto"
Tutti gli script girano; REPORT.md con tabella esempio × teorema → predetto / osservato / script / esito; elenco esplicito dei teoremi non applicabili e perché; righe LEDGER proposte (stato V-ex); CONFLITTO in inbox se un esempio contraddice un teorema; `DONE S5-EX` in inbox/central.md.
