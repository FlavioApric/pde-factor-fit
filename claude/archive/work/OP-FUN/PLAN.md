# PLAN — OP-FUN (chiusura Fasi 4–5: aperti su spazi funzionali, fattori, topologia) · 26/10/2026

## 0. Orientamento (fatto)
Letti: RIPRESA.md (fino all'ultimo aggiornamento), REPORT_FINALE.md §6, skills-local/session-protocol e claim-lifecycle, NOTAZIONE.md v4, PROBLEM.md, claims/LEDGER.md (righe C12-Q2, C12-Q6, P2-T4), work/C1C2/PROOF_PACKAGE.md (§§1–6, 5bis, 10) e gram.md, work/P2/PROOF_PACKAGE.md (P2-T3, P2-C2, P2-C1, §13), work/P1/PROOF_PACKAGE.md (§§2–6, 12), work/S5-INT/INTEGRAZIONE_LINEARE.md (§3.1 R-1…R-6, §3.4 S5-L1/S5-L2), research/CIT-AUDIT/AUDIT-5.md §2.3.

## 1. Skill (caricate leggendo i SKILL.md; nessuno script _vendor eseguito)
1. `skills-local/session-protocol`, `skills-local/claim-lifecycle` — protocollo e stati.
2. `_vendor/Auto-claude-code-research-in-sleep/skills/proof-writer` — una delle tre uscite per ogni claim (prova / enunciato corretto + prova / rapporto di blocco).
3. `_vendor/math-skill` modo `proof` — esplorazione separata dalla prova, controesempi presto.
4. `_vendor/scientific-agent-skills/skills/sympy` — controlli in work/OP-FUN/sympy/ (solo controllo, non metodo).
5. `_vendor/Auto-claude-code-research-in-sleep/skills/research-lit` — solo per collocare i fatti classici citati (Runge, de Rham, Malgrange–Ehrenpreis, coniugata logaritmica); nessuna ricerca web necessaria: le citazioni restano CON-FONTE con numero non verificato.
proof-checker/kill-argument: non eseguiti qui (revisore indipendente = S-CHECK); richiesta in CHECK_REQUEST.md.

## 2. Problemi, predizioni, criteri d'uscita
| # | problema | predizione | criterio d'uscita |
|---|---|---|---|
| 1 | **P1-Q2** (strato termini oltre τ − a_j distinti) | (a) l'esistenza della scomposizione per fattori in 𝔅 vale per **ogni** P (via r(∂_x) e s(∂_t) nell'ideale (Q_j, P/Q_j), primitive di Volterra in x e in t); (b) molteplicità (τ−a)^e: sistema di Jordan, termini {a_n I, N} commutanti ⇒ P1-T2 esatto; (c) grado ≥ 2 irriducibile monico: formula esatta di E^add via propagatore, ma E^mult ≢ 0 per ogni ordinamento (ostruzione); (d) non monico: il problema di Cauchy in t NON è unico in 𝔅 (controesempio di tipo Bessel per ξτ−1); teorema positivo nella classe spettrale con supporto K, ℂ∖K connesso, K ∩ Z(p_1) = ∅ (Runge) | prova completa di (a),(b),(d-positivo); controesempio verificato per (d); proposizione con prova per (c) |
| 2 | **P2-Q1** (densità di Σ ker_{H^m}Q_j in ker_{H^m}P) | densità VERA per ogni P che ammette contrazioni affini simmetriche del dominio (P quasi-omogeneo: onda su ogni convesso, trave su ogni rettangolo, τξ) e per i trasporti paralleli sul quadrato a ogni m (caso originale di P2-Q1 ⇒ ramo (ii) di P2-C1(b)); calore×trasporto: nessuna simmetria contraente ⇒ ostruzione del metodo, documentata | teorema con prova + corollari per le coppie ★; per calore×trasporto rapporto di blocco preciso |
| 3 | **C12-Q2** (P differenziale, N = 3, somme a coppie chiuse, tripla non chiusa) | nelle famiglie "parallele" (stessa parte principale di 1° ordine) e "separabili" (fattori in una sola variabile) il controesempio NON esiste: chiusura a coppie ⟺ chiusura totale | teorema negativo per le due famiglie + descrizione esatta di dove dovrebbe vivere un controesempio; il problema generale resta APERTO se non trovo un esempio |
| 4 | **C12-Q6** (condizione esatta su (P, A, Ω) non semplicemente connesso) | coker Σ_Ω ≅ ker[H¹(Ω;ℂ)⊗𝒩 → ⊕_j H¹(Ω;𝒦_{Q_j})] (coomologia di fasci); dim ≤ δ(P)·b₁(Ω); uguaglianza se ogni Q_j(∂) è suriettivo su A(Ω) (es. fattori ellittici ⇒ Laplaciano: scomposizione ⟺ Ω s.c.); formula esplicita della mappa con la primitiva polidroma | teorema con prova (fatti classici: de Rham, Malgrange–Ehrenpreis locale, come CON-FONTE dichiarati) + verifica sugli esempi di C12-P10 |
| 5 | **S5-L2** (prova completa) | vero; il criterio è solo sufficiente | prova completa + esempio di non necessità |

## 3. Output
work/OP-FUN/PROOF_PACKAGE.md (incrementale, una sezione per problema), work/OP-FUN/CHECK_REQUEST.md (autosufficiente), work/OP-FUN/sympy/*.py + .out; inbox/central.md: PLAN-READY, TABELLA LEDGER, DONE OP-FUN. Nessuna scrittura fuori da work/OP-FUN e inbox.

## 4. Contatti
central (coordinatore) per TABELLA/DONE; S-CHECK tramite CHECK_REQUEST.md. Inbox propria: nessuna (OP-FUN non ha scheda in SESSIONS.md); controllo di inbox/central.md a inizio e fine.
