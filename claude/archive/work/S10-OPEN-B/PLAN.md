# PLAN — S10-OPEN-B · residui della Fase 5 · 27/10/2026

Skill caricate: `skills-local/session-protocol`, `skills-local/claim-lifecycle` (lette per intero; nessuno script `_vendor` eseguito). SymPy solo come verifica (`.venv\Scripts\python.exe -I`), calcoli computer-assisted dichiarati come tali.

Letture fatte: REPORT_FINALE §6.2–6.3; work/OP-F5A (§3–4), OP-F5B (§1, §3, §4), OP-F5C (§1, §3, §4), OP-F5D (§3, §5, §8), OP-R2 (§2, §3), OP-NL (OP-L2, OP-P4), S4-ID (P8); audit relativi in work/CHECK.

## Problemi in ordine di trattabilità (predizione · limite di tempo)

| # | problema | predizione | via | limite |
|---|---|---|---|---|
| 1 | INT-T1(B) / [F4⁻] | (a) prova per N generale | Wronskiano dei semi φ_j = e^{−κ_jx} + ε_jc_je^{κ_jx}: sviluppo multilineare = f di Hirota (minori di Cauchy, regola dei segni); intreccio LA = A(−∂²) per divisione a destra (senza Crum citato); asintotica di Ae^{ikx} ai due estremi ⇒ b ≡ 0, a = Π(k − iκ_j)/(k + iκ_j), autovalori −κ_j² (OPF5D-L4) | 1 h |
| 2 | OPF5C-T5 (Ritt/Kolchin) | (a) prova autonoma | in una sola indeterminata il teorema "primo = [A] : H_A^∞" si dimostra con la pseudo-divisione differenziale e la minimalità del rango: il numero della fonte non serve | 30 min |
| 3 | OPA-Q2, densità di (SB) | (a) prova | perturbazioni C^∞ a supporto in corone attorno ai punti critici di u_0′: (1) valori critici distinti, (2) sollevamento di Φ fuori da un intorno di a_b; induzione finita sulle nascite con margini | 45 min |
| 4 | densità di OPF5B-T1 su non convessi | (b) controesempio | corona quadrata, P = ∂_x∂_y, u = φ(x)ψ(y) con φ′ψ′ supportato nel buco; funzionale "rettangolo attorno al buco" continuo su L², nullo sulla somma dei nuclei, = 1 su u | 30 min |
| 5 | [Hm] (parte di S4ID-P8 / OPR2-P7) | (a) prova per soluzioni nella classe (Cl) | leggi di conservazione di Gardner, parte quadratica (−1)^n∫(∂^{n−1}u)², Gagliardo–Nirenberg | 1 h |
| 6 | OPA-Q1, lemma L-loc | (a) prova per localizzazione | T1/T2/L2/Lemma U usano (G\*) solo per unicità, code e geometria locale: sostituzione con stime locali attorno ad a_b + margine (SB) + L3 localizzato in x | 1.5 h |
| 7 | OPF5C-Q1, δ_N(K) | (c) con valori nuovi | estensione di L8 a K = 2N (y_{2N} è un grafico); calcolo graduato k = 0 per K = 2N, N ≤ 4 (5, 6 se il tempo basta); δ_5(8) dal run concluso di OP-F5C; per N generale: riduzione al livello razionale graduato | 1 h (calcoli in background) |
| 8 | [GT-u] | (c) | lettura di GT §5/App. A se accessibile; altrimenti riduzione: dopo #5 P14/P15 dipendono solo da [GT-u] | 45 min |
| 9 | INT-Q1 (dati analitici) | (c) | combinazione T6 + S4ID-P8 (ora mod solo [GT-u]); residuo = relazioni con forma iniziale in I_PW e origine singolare | 30 min |
| 10 | OPR2-Q3, rimuovere (I) e (II) | (c) | caratterizzazione esatta dell'esistenza di un criterio a test finiti (insieme colpitore della famiglia {L_u}); (I) necessaria; (II) sostituita da una condizione più debole | 45 min |
| 11 | OPR2-Q2′ | (c) | nessuna prova della localizzazione prevista; registrazione precisa | 15 min |

Criterio di "fatto": per ogni problema un esito (a), (b) o (c) scritto in PROOF_PACKAGE.md, con stato proposto (mai DIMOSTRATO senza audit), riga in LEDGER_ROWS.md, richiesta in CHECK_REQUEST.md, residui in open_questions.md.
