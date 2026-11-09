# PLAN — S8-ENC (Fase 8, problema B2: rimuovere V come "rumore" con un encoder analitico) · 26/10/2026

Riga del roster (SESSIONS-F8.md): ENC-1 (Volterra, ipotesi nell'enunciato), ENC-T2 come lemma "a q noto" (F6), ENC-P0 (eccezioni che cambiano il tempo), ENC-N1 (cieco ⟺ identificabilità congiunta), tabella encoder (F7) con Duistermaat–Grünbaum (V → 0); E_int **A9** per Schrödinger con V (non E^conj); definizione (E2) "modulo costanti". Criterio d'uscita: ogni claim con prova completa o FALSO; CHECK_REQUEST pronto. Contatti: S8-VAR, S8-DICT.

Materiale di partenza (si completa, non si riparte): `research/F6-ENC/VERDETTO.md`, `NOTE.md` §§1–13, `sympy/`. Correzioni vincolanti: SYNTHESIS-2 §§1, 3, 7; DEVIL-6 O5, O6, O7 (fix F5, F6, F7, F10); CIT-AUDIT-6 voci 9, 10, 13, 15, 16 e §3.2–3.3.

## 1. Skill (in ordine d'uso)
1. `skills-local/session-protocol` (letto: Passi 0–4; canale `inbox/central-F6.md`, non central.md).
2. `skills-local/claim-lifecycle` → catena: `proof-writer` (SKILL.md letto: tre esiti ammessi — prova, enunciato corretto + prova, rapporto di blocco) → `math-skill` modo proof + SymPy (casi limite e controesempi presto) → proof-checker: **il revisore indipendente è S-CHECK-F8** (fase successiva del roster; qui nessun subagente) → `kill-argument` (SKILL.md letto; i revisori esterni non sono disponibili ⇒ passaggio avversariale interno documentato, REVIEW_UNAVAILABLE per i revisori esterni) → scientific-critical-thinking per lo stato finale.
3. Nessuno script `_vendor` eseguito; niente ML; SymPy/mpmath solo verifica: `.venv\Scripts\python.exe -I work/S8-ENC/sympy/<script>.py`.

## 2. Predizione scritta (prima delle prove)
| claim | predizione |
|---|---|
| ENC-1 | **Dimostrabile per intero** con ipotesi q ∈ C¹[x_0−a, x_0+a] (complesso ammesso), rettangolo simmetrico in x, punto base x_0: esistenza del nucleo (Goursat in coordinate caratteristiche + approssimazioni successive), intertwining senza condizioni al bordo, inverso di Volterra costruito con un secondo Goursat. Mi aspetto in più un risultato di **unicità** esatto: nella classe "Volterra simmetrica con nucleo C²" gli intertwiner formano una retta affine {T_{k_0}}, k_0 ∈ ℂ, e la conservazione dei dati di Cauchy in x_0 fissa k_0 = 0 (chiude ENC-U1 in questa classe). Dipendenza da x_0 vera già per q costante. |
| ENC-T2 | Corretto come lemma di trasporto **a q noto** (DEVIL-6 lo ha ricontrollato); lo riscrivo con la prova del caso dispari completa e con (c) riformulato: W induce una biiezione triangolare dei getti nel punto base (non li conserva). |
| ENC-P0 | Corretto a tempo fissato; prevedo una versione **P0′ con riparametrizzazione del tempo**: ogni encoder lineare soluzione→soluzione con τ = θ(t) è U_0(θ(t)) M U_V(t)^{-1}. La lente di Niederer è il caso θ = tan, M = I: l'eccezione quadratica rientra in P0′, non in P0. Il fatto "V dipendente da t ⇒ nessun W indipendente dal tempo" segue da W(V(t)−V(s)) = 0. |
| ENC-N1 | Il "⟺" nudo è **falso come scritto** (u ≡ 0 è dato di ogni V): prevedo la forma corretta "encoder cieco ⟺ la componente libera è identificabile; identificabilità congiunta ⇒ cieco; ⇐ sotto un'ipotesi di separazione (S)", e (S) vera per Volterra quando la proiezione su x di {u ≠ 0} è densa. |
| (E2) modulo costanti | q ≡ c ≠ 0 non ha intertwiner differenziale stretto a **ogni** ordine (prova per ricorsione sui coefficienti: diventano polinomi, contraddizione al grado n). Con (E2′) W L_q = (L_0 + c)W il caso entra. |
| ENC-K1 | Prevedo di dimostrare la direzione "⇒" **localmente** (ogni intertwiner differenziale è una catena di Darboux del primo ordine con semi complessi, su sottointervalli senza zeri dei semi: nucleo invariante + divisione a destra). La caratterizzazione globale delle classi (razionali che decadono: Duistermaat–Grünbaum; solitoni) resta CON-FONTE. |
| E_int A9 | Forma chiusa per V costante, **lineare** (prevedo: Strang esatto a meno della fase e^{−iF²t³/12}), **quadratico** (Mehler; chirp·libero·chirp esatto per \|t\| < π/2 nella normalizzazione H = −∂² + x²) e **Pöschl–Teller** (U_q = e^{it}P_b + A(L_0+1)^{-1}U_0(t)A†, nucleo con erfc). Per V ∈ W^{2,∞} reale: stima ‖E^mult(t)f‖ ≤ (t²/2)[(‖V″‖ + 2t‖V′‖²)‖f‖ + 2‖V′‖‖f′‖], ottimale nell'ordine t² (termine principale (t²/2)[L_0, V]); E^mult ≡ 0 ⟺ V costante. Tutto su ℝ; su Ω limitato resta aperto. |

## 3. Criterio di "fatto"
PROOF_PACKAGE.md con enunciati a ipotesi complete e prove per: ENC-1 (+U1, stabilità), ENC-C1, ENC-T2, ENC-P0/P0′, ENC-N1, ENC-K0 (q = c), ENC-K1′ (direzione ⇒), definizione (E2′), tabella encoder, E_int A9 (4 forme chiuse + stime). SymPy/mpmath per ogni forma chiusa e per ENC-T2/K0. CHECK_REQUEST.md, LEDGER_ROWS.md, open_questions.md; TABELLA a S8-VAR e S8-DICT; `DONE S8-ENC` in central-F6.
