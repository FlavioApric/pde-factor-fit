# PLAN — S8-SYS (Fase 8, L6: sistemi a coefficienti costanti, gauge, E per sistemi)
27/10/2026. Riprende `research/F6-SYS/` (NOTE.md, VERDETTO.md): si completa, non si ricomincia.

## Skill caricate
session-protocol, claim-lifecycle (letti per intero); proof-writer (struttura del pacchetto, triage onesto); math-skill modo proof/controesempio (letto); SymPy solo per verifiche (`.venv\Scripts\python.exe -I work/S8-SYS/sympy/*.py`). proof-checker e kill-argument: delegati a S-CHECK-F8 / DEVIL-8 via CHECK_REQUEST.md (non lancio subagenti). Nessuno script `_vendor`.

## Enunciati e predizione scritta
| ID | obiettivo | predizione |
|---|---|---|
| SYS-L1 | famiglia essenziale | prova standard, nessun problema |
| SYS-T1 | test di identificazione | **semplificabile**: il test si riduce a una indipendenza *per primo* (i primi immersi si eliminano moltiplicando per a ∈ ∏p ∖ q). Rischio novità: Oberst 1990 (cogeneratore grande, Matlis) → probabilmente CON-FONTE in sostanza per la parte "M ↪ 𝒜 ⟺ numeri di Bass", delta = test esplicito su una u data |
| SYS-E∃ (criterio d'esistenza) | ∃ u identificante ⟺ dim soc_m(M_P) ≤ 1 ∀ m massimale | **vero su ogni Ω aperto connesso** (non solo convesso): serve μ_p(C^∞) = ∞ per p non massimale (costruzione con integrali di esponenziali su una sezione locale di V(p) sopra iℝ^d, unicità di Fourier) + iniettività di C^∞(ℝ^N) + immagini analitiche sulla famiglia essenziale |
| SYS-N1, SYS-T0 | zoccolo; EDO | corollari di SYS-E∃ |
| SYS-C1 | P quadrata, det ≠ 0, N ≥ 2 ⇒ esiste u identificante | Koszul: Ext⁰(R/m,M) ↪ Ext¹(R/m,R^k) = 0 |
| SYS-S1 | somma di nuclei ⟺ lcm sinistro | (⇒) su ogni aperto (𝒜 cogeneratore su ogni Ω); (⇐) su Ω con H¹_dR = 0 se N ha lunghezza finita; per N di lunghezza infinita su Ω non convesso: ostruzione = mappa di connessione verso Ext¹(N,𝒜), controesempio non trovato (APERTO) |
| SYS-E | P1-T5 per Dirac 1+1 | (H) vale in Mat_2(ℂ[ξ]) su ℂ ⇒ P1-T5 si applica; Euler ZXZ con tempi g(t,ξ) non polinomiali = moltiplicatori non locali; algebra = twisted current algebra ⊂ sl_2⊗ℂ[ξ], dim ∞ su ℂ |
| G-T2, SYS-N3, G-T0 | gauge | G-T2 classico (prova di una pagina); SYS-N3 vero anche non stazionario; G-T0 osservazione |
| H-DIRAC | risposta "Mat 4×4" | forma hamiltoniana: α, βm identificati esattamente se ψ identifica; test = μ=2 su (ψ_3,ψ_4) in base chirale; 1+1 = C3-T1 per KG |
Criterio d'uscita: ogni claim con prova completa o FALSO/APERTO dichiarato; CHECK_REQUEST pronto; SymPy verde.

## Fonti
Oberst 1990 (Acta Appl. Math. 20, 1–175), Schindelar–Levandovskyy–Zerz 2011 (JSC 46), Matsumura (§18), Weibel (Koszul, Ext), Malgrange/Ehrenpreis (iniettività di C^∞(ℝ^N)), Booth–Legg–Jarvis 2001, Aharonov–Bohm 1959, Wu–Yang 1975, P1-T5 (work/P1/CHECK_REQUEST.md §C), C3-T1, C12-T1′/L2′.
## Contatti
S8-VAR (VMPUM, Schindelar et al.), S8-DICT (moltiplicatori U3 per SYS-E). Canale: inbox/central-F6.md.

## Aggiornamento 27/10/2026 (consuntivo rispetto alla predizione)
- SYS-T1: declassato come previsto, con delta dichiarato rispetto a SLZ 2011 (SYS-R1: dati EP ⇒ M_u di lunghezza finita); Oberst 1990 non leggibile, rischio di novità alto per SYS-EX su ℝ^n.
- SYS-E∃ (rinominato **SYS-EX** per non confonderlo con SYS-E): provato su ogni Ω connesso come previsto, senza bisogno della molteplicità di Bass di C^∞ come input; questa ne è un corollario (SYS-EX-C).
- SYS-S1: la predizione diceva "controesempio non trovato (APERTO)". Il controesempio esiste: dominio a U semplicemente connesso con U_1 = R(1,0), U_2 = R(1,∂_x). (⇐) vale solo se N ha lunghezza finita e H¹_dR = 0, oppure se Ext¹(N, 𝒜) = 0.
- SYS-E, gauge, H-DIRAC: come previsto. Lamé n = 3 svolto (μ = (1, 2)). II-T2(b′) derogatoria: non svolta (open_questions Q-S8SYS-4).
- Consegne: PROOF_PACKAGE.md, CHECK_REQUEST.md, LEDGER_ROWS.md, open_questions.md, sympy/ (32/32 OK).
