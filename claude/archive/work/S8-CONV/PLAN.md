# PLAN — S8-CONV (Fase 8, prove) · P-C: convergenza, rumore, località, bordo, dimensione · 27/10/2026

Riga del roster (`SESSIONS-F8.md`): CONV-T1…T6, CONV-P8 (1+d), CONV-T7 come contratto per ALGORITMO_ESTESO; rumore (T3–T5, anche L² hölderiano); bordo e dimensione (S8-NOISE/DIM fuso qui); CONV-Q6 (P3-T3 contro Einkemmer–Ostermann, Dirichlet non omogeneo). In più, da ROUTES (tabella Gate 6): revisione di **RT-R2a** (bordo periodico, H0 intatto) e di **Mori–Zwanzig**, riaperte e assegnate a RT-CONV.
Criterio d'uscita: ogni claim ha una prova completa oppure è marcato FALSO; `CHECK_REQUEST.md` pronto per S-CHECK-F8.

Materiale di partenza (si completa, non si ricomincia): `research/F6-CONV/{NOTE,VERDETTO,open_questions}.md`; fix F4, F9, F10 di `research/DEVIL/ATTACK-6.md` (O4 ritardo, O9 modelli di dato e simboli, O10 su CONV-T1(5), CONV-T2 passo (ii), CONV-T5 in L²); correzioni di `research/CIT-AUDIT/AUDIT-6.md` (Peetre verificato; Moan–Niesen solo matrici reali → Casas 2007 per operatori limitati su Hilbert; Einkemmer–Ostermann solo Dirichlet **non omogeneo** e bordi non periodici; numeri di Adams–Fournier, Engl–Hanke–Neubauer, Kelly, Hörmander non verificati); LEDGER: C3-T1, C3-T3, C3-T6, C3-P1, P4-T5, C12-T1′, C12-P10, P2-T4, P3-T3; `work/P3/PROOF_PACKAGE.md` §P3-T3.

## Skill (lettura integrale dei SKILL.md; nessuno script `_vendor` eseguito)
1. `skills-local/session-protocol`: piano, inbox, consegne, DONE (canale `inbox/central-F6.md`).
2. `skills-local/claim-lifecycle`: per ogni claim bozza (proof-writer) → controesempi e casi limite (math-skill, modo proof) → SymPy → richiesta di audit (S-CHECK-F8) → kill-argument sui claim del cammino critico (**CONV-T1 e CONV-T2**, scritto in PROOF_PACKAGE §K) → stato.
3. `_vendor/.../proof-writer`: triage di ogni enunciato (PROVABLE AS STATED / AFTER WEAKENING / NOT JUSTIFIED).
4. `_vendor/math-skill` (modo proof) + SymPy: verifica, mai prova. Comando: `D:\ProblemaBase\.venv\Scripts\python.exe -I work/S8-CONV/sympy/<script>.py`.
5. `_vendor/.../kill-argument`: eseguito in forma "attacco più forte → difesa punto per punto" da questa sessione; il revisore indipendente è S-CHECK-F8 / DEVIL-8.
6. `_vendor/.../proof-checker`: il revisore è S-CHECK-F8 (niente DIMOSTRATO qui).

## Modelli di dato e di calcolo (fix F9, NOTAZIONE v5)
Ogni enunciato dichiara il modello: DM2 (jet esatto in un punto, aritmetica reale esatta, modello BSS) per T1/T2; DM3 (u in H^m(Ω) con rumore) per T3–T5; u intera in x con spettro compatto per T6; dati modali finiti su (0,L) Dirichlet per Q6; C^∞(I × 𝕋) per RT-R2a.

## Predizione scritta (prima delle prove)
1. **CONV-L1, CONV-T1(1–7): si dimostrano come scritti**, con due correzioni: (a) T1(5) va riformulato in "numero di **uscite distinte** ≤ (d+1)(d+2)/2, quindi cambi ≤ (d+1)(d+2)/2 − 1" (O10); (b) il modello di calcolo è BSS (uscite reali esatte), va scritto nell'enunciato. Mi aspetto che il kill-argument non trovi falle; il punto più esposto è la definizione di O_K per K piccolo (m\*(K) = ∞ solo per K = 0).
2. **CONV-T2: si dimostra**; il passo (ii) va riscritto con la matrice esplicita e l'argomento "intersezione decrescente = 0 ⇒ rango pieno da un K₀ in poi". Predico che regga anche in 1+d.
3. **CONV-T3: si dimostra** per X ↪ D′(Ω) con immersione continua (ipotesi da aggiungere all'enunciato).
4. **CONV-T4: si dimostra**; il ramo hölderiano si scrive con l'estensione universale di Stein per esponenti interi (n, s ∈ ℕ), il caso s reale resta fuori dall'enunciato.
5. **CONV-T5: si dimostra** in entrambe le norme (H^d e L² + limite a priori in H^{d+s}); il punto 4 ("δ₀ non calcolabile") va trasformato in un enunciato preciso: per ogni u con legge e ogni η > 0 esiste u′ a distanza ≤ η (in ogni H^N) con legge e δ₀(u′) ≤ η. Predico che sia vero con u′ = u + ε·t^d x^d.
6. **CONV-T6: si dimostra** con l'insieme {f̂ ≠ 0} al posto del supporto; il ritardo va corretto (fix F4): Ann(u) = 0 nelle variabili date ma classe **L⁺** (trasporto ausiliario); la trascendenza del ramo di Lambert va dimostrata, non affermata; il frazionario irrazionale si dimostra con l'argomento di Puiseux.
7. **CONV-P8: si dimostra**; l'ambiguità in 1+d, d ≥ 2: "finita ⟺ nulla ⟺ fattori a due a due comassimali", con esponenziali sulle intersezioni (vale su ogni Ω aperto, senza convessità). L'esistenza della scomposizione su Ω convesso resta CON-FONTE (principio fondamentale), da verificare.
8. **CONV-T7: contratto A/B/C** come definizione + proposizione di composizione (telescopica) con prova; Moan–Niesen solo per matrici reali, Casas 2007 per operatori limitati su Hilbert.
9. **CONV-Q6:** predico un enunciato nuovo dimostrabile al primo ordine nell'accoppiamento ε nel quadro di P3-T3: **Lie conserva l'ordine globale 1 in L²** (il difetto locale Θ(h^{5/4}) non si accumula grazie al lisciamento parabolico), mentre **Strang scende dall'ordine 2 all'ordine 5/4 in L²**; in L^∞ l'ordine di Strang dovrebbe essere 1 (solo numerico, V-ex). Il meccanismo coincide con quello di Einkemmer–Ostermann (il passo non rigido esce dal dominio del passo rigido), ma il loro quadro è Dirichlet non omogeneo: confronto come analogia, non come equivalenza.
10. **Bordo:** (a) le condizioni al bordo sono invisibili ad Ann(u) (esempio esplicito Dirichlet/Neumann con lo stesso Ann); (b) CONV-T4/T5 si trasportano a un dizionario di tracce; (c) predico un teorema negativo: con derivate tangenziali nel dizionario di traccia il margine ρ è sempre 0 (il nucleo è chiuso per derivate tangenziali), quindi il dizionario di bordo va preso "normale" o modulo le conseguenze tangenziali.
11. **RT-R2a:** su I × 𝕋 vale il criterio esatto ker(fg) = ker f + ker g ⟺ nessuna risonanza "propria" V(f) ∩ V(g) ∩ (ℂ × iℤ) (fuori dalle rette contenute in V(f) o V(g)), con codimensione = Σ deg gcd; si dimostra con l'identità di Bézout A f + B g = r(ξ) (niente piccoli divisori perché r è un polinomio). H0 resta intatto: 𝕋 è un caso di bordo.
12. **Mori–Zwanzig:** a coefficienti costanti la componente osservata di un sistema quadrato con det D ≠ 0 ha sempre una legge locale (det D); la memoria di MZ è un caso L⁺ che diventa L dopo eliminazione. Predico che il criterio della strada "E_int = 0 ⟺ [𝒫, L] = 0" sia **FALSO** come scritto: la memoria si annulla ⟺ a₁₂a₂₁ ≡ 0, condizione strettamente più debole di [𝒫, A] = 0.

## Ordine di lavoro
1. T1, T2, T5 per primi (servono a S8-DICT per I-LIM): appena gli enunciati sono stabili, TABELLA in `inbox/central-F6.md` e in `inbox/S8-DICT.md`.
2. T3, T4, T6, P8, T7.
3. Q6, bordo, RT-R2a, Mori–Zwanzig.
4. SymPy per ogni blocco (script in `sympy/`, `.out` accanto).
5. PROOF_PACKAGE, kill-argument su T1/T2, CHECK_REQUEST, LEDGER_ROWS, open_questions; DONE.

## Contatti
S8-DICT (I-LIM usa CONV-T1; R-STOP = CONV-T5), S8-VAR (raggi Magnus/Dyson per V(t,x) in CONV-T7: CONV-Q9), coordinatore in `inbox/central-F6.md`. Lettura della mia inbox all'inizio, a metà e prima della consegna.
