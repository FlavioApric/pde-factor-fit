# PLAN — S8-DICT (Fase 8, prove) · L9–L10: dizionario universale filtrato 𝓓_∞ · 26/10/2026

Riga del roster (SESSIONS-F8.md): U1+N0, U2 (liscezza di F, KMS 18.16; Slovák 1987/1988), U3(c)+N2, U3(d), ritardo come sistema aumentato (F4), U4; N1(i)–(v) + (a′)/(b′) (F1); Teorema A, MF1–MF3, B2, regole R1–R6, R-STOP; I-LIM con (H-ID); NS-EXPALG (sine-Gordon, e^u via w = e^{iu}, Ax 1971); frazionari (S8-NLOC fuso qui). Criterio d'uscita: ogni claim con prova completa o FALSO; N1 con kill-argument; CHECK_REQUEST pronto.

Materiale di partenza (completare, non ricominciare): `research/F6-DICT/{VERDETTO,NOTE}.md`; correzioni di `research/SYNTHESIS-2.md` (F1, F3, F4, F10), `research/DEVIL/ATTACK-6.md` (O1, O3, O4, O10), `research/CIT-AUDIT/AUDIT-6.md`; NS-EXPALG da `research/F6-HOR/VERDETTO.md`; LEDGER C3-P1, P4-T5; S4-ID T1 (`work/S4-ID/PROOF_PACKAGE.md` §2).

## Skill caricate (lettura integrale del SKILL.md, nessuno script `_vendor` eseguito)
1. `skills-local/session-protocol` — piano, inbox, consegne, DONE (canale: `inbox/central-F6.md`).
2. `skills-local/claim-lifecycle` — catena per ogni claim.
3. `_vendor/.../proof-writer` — PROOF_PACKAGE.md: per ogni claim triage (PROVABLE AS STATED / AFTER WEAKENING / NOT JUSTIFIED), mappa delle dipendenze, prova.
4. `_vendor/math-skill` (modo `proof`) + SymPy — controesempi e casi limite presto; SymPy solo verifica (`.venv\Scripts\python.exe -I work/S8-DICT/sympy/<script>.py`).
5. `_vendor/.../kill-argument` — su N1 (enunciato del cammino critico). Codex non disponibile e nessun subagente lanciato da questa sessione: il thread d'attacco e quello di aggiudicazione sono eseguiti qui, separati, e marcati "revisore fresco non disponibile" (stessa prassi di DEVIL-6). Esito in `KILL_ARGUMENT_N1.md`.
6. proof-checker: NON eseguito qui (lo fa S-CHECK-F8, revisore indipendente) → CHECK_REQUEST.md.
Niente ML.

## Predizione scritta (prima delle prove)
- **Si dimostrerà completamente:** U1 (con N0); U2 con la liscezza di F ottenuta **senza** KMS 18.16, dalla regolarità di D applicata a una famiglia liscia esplicita di realizzazioni dei getti + teorema di Boman (1967); U3(c)+N2; U3(d) per t^{−β} (trapezi in striscia: errore relativo **uniforme in t**), con rappresentazione diffusiva **esatta** per ogni nucleo c.m. (sistema aumentato con variabile continua λ); ritardo = trasporto aumentato (equivalenza esatta per caratteristiche); N3 ristretto con **distanza esattamente 1**; frazionario = estensione di Caffarelli–Silvestre con costante esplicita (prova via Fourier e K_s); U4 per componenti.
- **N1:** (i), (iii), (iv) (con i due modelli di calcolo separati), (v) anche per dizionari polinomiali differenziali (lemma delle parti omogenee di grado massimo: fix F10); (vi) sostituito da (a′)/(b′) con un **unico teorema di rango**: per la mappa residuo puntuale ρ_u(y) = (T_1u(y),…,T_Ku(y)), *iniettiva su un denso ⟺ identificabile*, *suriettiva ovunque ⇒ non falsificabile*; (a′) = caso "tutti gli operatori" (K ≥ 2 ⇒ mai iniettiva). Mi aspetto che l'esempio V reale per Schrödinger sia **identificabile e falsificabile** (asse diverso dalla taglia).
- **Teorema A:** aperto/raro con dati approssimati; mi aspetto di poter aggiungere (iii): con **dati finiti esatti** (funzionali lineari continui qualsiasi) il fit non è certificabile per atomi differenziali (argomento di cono + supporti disgiunti).
- **I-LIM** sotto (H-ID): prova completa; esempio a(t,x) (correzione O1). Corollario hölderiano resta candidato (costante di interpolazione).
- **NS-EXPALG:** polinomializzazione esatta via w = e^{iu} (prova elementare), trasporto "trdeg = ∞" senza Ax; Ax serve solo per esponenziali di più variabili differenziali (osservazione CON-FONTE). Nucleo 3 del kink: prova esplicita.
- **Rischi di FALSO o declassamento previsti:** velocità per nuclei c.m. generali (resta candidato); B3 (n-larghezze multivariate, fonte non verificata); Hölder di I-LIM; R4 (diagnostica, euristica: non è un teorema).

## Ordine di lavoro
1. PROOF_PACKAGE §1 universalità (U1, U2, U3, ritardo, frazionari, U4) → SymPy A.
2. §2 N1 + (a′)/(b′) → SymPy B → kill-argument.
3. §3 Teorema A, MF1–MF3, B2, R1–R6, R-STOP, G-R → SymPy C.
4. §4 I-LIM; §5 NS-EXPALG → SymPy D.
5. §6 costruzione esplicita di 𝓓_∞ (tabella per livello, topologia e modello di dato per classe) — sezione per ALGORITMO_ESTESO.
6. CHECK_REQUEST, LEDGER_ROWS, open_questions; inbox (metà e fine); DONE.

## Contatti
S8-CONV (R-STOP = CONV-T5, I-LIM ramo esatto), S8-SYS (U4, conteggio di SYS-N3 nel teorema di rango), S8-ENC (R6 = D4-ENC "a q noto").

## Criterio di "fatto"
Ogni claim della riga con: enunciato con ipotesi complete, prova completa (o declassamento esplicito con motivo), SymPy dove sensato, riga LEDGER proposta, domanda mirata per S-CHECK-F8.
