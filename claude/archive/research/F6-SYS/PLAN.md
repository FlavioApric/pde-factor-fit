# PLAN — F6-SYS (Fase 6, scouting) · P-A sistemi a coefficienti matriciali + gauge (R9, R16)
Data: 26/10/2026 · Cartella: `research/F6-SYS/` · Comunicazione: `inbox/F6-SYS.md` (lettura), `inbox/F6-VAR.md`, `inbox/F6-DICT.md`, `inbox/central-F6.md` (AVVISO del coordinatore: NON `inbox/central.md`).

## Skill caricate (in ordine d'uso)
1. `skills-local/session-protocol/SKILL.md` — letto per intero (orientamento, PLAN, inbox, consegna).
2. `skills-local/route-scout/SKILL.md` — letto: criteri fissati prima, verdetto di una pagina, proposta promote/park/merge/kill.
3. `skills-local/claim-lifecycle/SKILL.md` — letto: gli enunciati nuovi restano "candidato"/"prova scritta"; nessun DIMOSTRATO (manca S-CHECK).
4. `_vendor/.../novelty-check/SKILL.md` — letto (solo istruzioni; revisore esterno escluso per route-scout: i limiti del verdetto li valuto io; verifica citazioni senza script → voci non verificate marcate "da verificare").
5. `anthropic-skills:deep-research` — non invocata come subagente (vincolo: non delegare); uso WebSearch/WebFetch direttamente per i riferimenti.
6. `_vendor/math-skill/SKILL.md` (modo `proof`) — letto: esplorazione separata dalla prova, controesempi presto.
7. `_vendor/scientific-agent-skills/skills/scientific-critical-thinking/SKILL.md` — letto: verdetto finale.
Nessuno script `_vendor` eseguito. SymPy solo come verifica: `.venv\Scripts\python.exe -I research/F6-SYS/sympy/<script>.py`.

## Domande (piano esteso P-A, appunti H2: "fino ad ora coefficienti scalari J_λ·Φ; Dirac → λ sono Mat 4×4. Come risolvo?")
Q1 (oggetto). Per P ∈ Mat_{l×k}(R), R = ℂ[τ,ξ] (o ℂ[∂_0,…,∂_n]), e u ∈ 𝒜^k: Ann(u) := {r ∈ R^{1×k} : r(∂)u = 0} come sottomodulo di R^{1×k}; modulo M = R^{1×k}/Ann(u) ≅ R·u (non più ciclico come quoziente di R, ma ciclico come sottomodulo generato dalle k componenti? — chiarire). Coefficienti non commutativi (γ^μ): come si riducono a matrici su R commutativo.
Q2 (dualità). Malgrange–Oberst: 𝒜 cogeneratore iniettivo ⇒ Sol(P) ↔ M_P = R^{1×k}/R^{1×l}P antiequivalenza; Ann(Sol(P)) = R^{1×l}P (Nullstellensatz delle soluzioni).
Q3 (I) Analogo di C3-T1: quando una sola soluzione vettoriale u identifica il sistema (Ann(u) = R^{1×l}P)? Ostruzioni nuove (rango, torsione, modulo non ciclico).
Q4 (S) Analogo di C12-T1′: scomposizione per fattori matriciali; Dirac (γ·p−m)(γ·p+m) = (p²−m²)I; non unicità/non commutatività delle fattorizzazioni; riduzione scalare via determinante/aggiunta; forma di Smith dove esiste (anello a 1 variabile / PID) e Quillen–Suslin (moduli proiettivi liberi).
Q5 Compagna (II) per sistemi: sistema del 1° ordine in t ∂_tU = A(∂_x)U; II-T2/T3/T4 per A matrice qualsiasi (non compagna, possibilmente derogatoria).
Q6 (E) E_int con termini matriciali non commutanti a coeff. costanti: P1-T4/T5 (criterio per algebra di Lie) trasportato.
Q7 Compatibilità/sovradeterminati: Maxwell (div), elasticità, reazione–diffusione accoppiata.
Q8 (gauge) Teorema candidato: con potenziale EM l'identificazione è possibile solo modulo gauge; quoziente e dati identificabili (F = dA, olonomie se Ω non semplicemente connesso).
Q9 Novità rispetto a Oberst, Pommaret, Zerz, Shankar, Quadrat, Willems (identificabilità dei comportamenti).

## Criteri fissati PRIMA di cercare (route-scout)
**PROMUOVI (a Fase 8, sessione S8-SYS)** la strada "sistemi via modulo R^{1×k}/Ann(u) + Malgrange–Oberst" se valgono tutti:
 (P1) almeno due delle tre risposte I/S/E sono "sì" o "parziale con enunciato candidato preciso" (ipotesi esplicite);
 (P2) l'enunciato di identificazione (I) per sistemi si riduce a C3-T1 + algebra commutativa standard (prova scritta di ≤ 2 pagine, nessuna nuova macchina analitica), oppure c'è un controesempio verificato in SymPy che fissa il confine;
 (P3) il teorema di gauge (Q8) ha un enunciato preciso con quoziente esplicito, verificato su 1+1 Dirac/Schrödinger in SymPy;
 (P4) i casi minimi SymPy (2×2, Dirac 1+1, KG) passano.
**PARCHEGGIA** se (P1) vale ma (P2) o (P3) richiedono strumenti oltre il budget (es. teoria dei D-moduli a coeff. variabili per il gauge con A(x) generico → passa a F6-VAR).
**ELIMINA** (come strada autonoma, con MERGE nel pacchetto scalare) se il caso sistema si riduce interamente al caso scalare per determinante/eliminazione senza perdita (nulla di nuovo da dimostrare), oppure se la novità è nulla rispetto a un lavoro pubblicato nominato (Oberst/Zerz/Willems) che contiene già l'enunciato di identificazione.
**Teorema negativo atteso** (da dimostrare o confutare, non da assumere): la riduzione determinantale perde informazione (Ann(u) per u vettoriale non è determinato da det P); la fattorizzazione matriciale non è unica.

## Fonti / stringhe di ricerca
Oberst 1990 "Multidimensional constant linear systems" (Acta Appl. Math. 20); Malgrange 1963/64 (Sém. Bourbaki / ICASV Hörmander cap. 7); Palamodov 1970; Pommaret 1994/2001; Zerz 2000 (LNCIS 256) e "autonomy/controllability"; Shankar (controllability, Nullstellensatz for solutions); Quadrat & Pommaret (Serre's reduction, Quillen–Suslin effettivo: Fabiańska–Quadrat 2007); Willems 1991 (behaviors), Willems–Polderman 1998; Wood–Rogers–Owens; identifiability of behaviors (Willems "exact identification", Markovsky). Gauge: Eskin (inverse problems for magnetic Schrödinger, gauge equivalence), Nakamura–Sun–Uhlmann 1995, Aharonov–Bohm. Dirac: Dirac 1928, Clifford; inverse problems for Dirac (Isozaki, Salo–Tzou).

## Contatti
F6-VAR (moduli su Mat_k(R) ↔ D-moduli; gauge a coeff. variabili), F6-DICT (U4 = versione matriciale del dizionario). Inbox letta all'inizio (solo AVVIO), a metà, alla fine.

## Criterio di "fatto"
VERDETTO.md (1–2 pagine, I/S/E, enunciati candidati, ostruzioni, teoremi negativi, costo, novità, raccomandazione), NOTE.md (prove/argomenti), sources.bib, open_questions.md, sympy/ con output; messaggi a F6-VAR e F6-DICT; `DONE F6-SYS` in `inbox/central-F6.md`.
