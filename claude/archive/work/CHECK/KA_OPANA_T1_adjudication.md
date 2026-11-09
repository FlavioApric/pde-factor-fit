# KA OPA-T1 — Thread 2 (arbitrato), subagente Claude fresco afbeb747ddd38719e, 26/10/2026
Input: work/CHECK/KA_OPANA_T1_input.md (con appendice: formulazione verbatim di S4T-Q1) + memo d'attacco verbatim (KA_OPANA_T1_attack.md). Il revisore ha eseguito un controllo numerico proprio (scratchpad scheck15_adj_a.py: Λ_smooth(t) − 2log(1/(t−1)) → 0 per t↓1).

## Punti (sintesi fedele dell'arbitrato; il testo integrale è nella risposta del subagente, riportata qui nei contenuti essenziali)
| punto | attacco | verdetto | severità se aperto | fix raccomandato |
|---|---|---|---|---|
| P1 | la domanda S4T-Q1 sarebbe uniforme in t (Tang–Teng); un limite puntuale non risponde | partially_answered (la lettura a t fissato è difendibile: formulazione r. 88, quadro r. 89, "a ogni tempo fissato non degenere" r. 14; scelta intenzionale, sostenibile solo se dichiarata) | major | dopo r. 28 dire che il risultato è puntuale in t e che limsup_ν sup_{t∈(t*,T]} ‖·‖₁/ν = ∞ segue da OPA-T1 + OPA-C1 (coerente con Tang–Teng) |
| P2 | "senza fattore logaritmico" è una sovra-dichiarazione | **still_unresolved** (r. 2 e 28 dicono solo "(in (H_t))"; nessun "a t fissato", nessuna menzione della divergenza di Λ(t); OPA-R1 la registra ma come osservazione "non necessaria") | **major** | riscrivere r. 2 e 28: "per ogni t > t* fissato con (H_t): esattamente νΛ(t), senza log; Λ(t) ~ 2log(1/(t−t*)) diverge: non uniforme vicino a t*, dove il log ricompare" |
| P3 | costanti non quantitative (δ, j₀, η, r₀) e o(ν) non quantificato | answered_by_current_text (per l'enunciato a t fissato: lim ‖·‖/ν = Λ > 0 implica Θ(ν) con ν₀(t)) | minor | facoltativo: scrivere l'argomento C² per O(ν^{3/2}) nel profilo; dire che ν₀ dipende da t |
| P4 | (H_t) verificata solo per ε sin x; per dati generici fallisce a nascite/collisioni di shock | partially_answered (portata condizionale dichiarata; "(H_t) minima" non giustificata; Rischio (3) sui punti tripli non dimostrato) | major | dire che (H_t) è verificata solo per ε sin x (t ≠ t*); genericità di (H_t) (fallisce solo in un insieme discreto di tempi) APERTA; Rischio (3) → congettura |
| P5 | tasso ν|log ν| ai tempi degeneri (t* e successivi) | partially_answered (OPA-R1 non dimostrata; t* escluso da "oltre lo shock"; tempi degeneri successivi non discussi) | minor (lettura a t fissato) | estendere OPA-R1 a nascite/collisioni successive; elencare "tasso ai tempi degeneri" come APERTO separato |

Conteggi: answered 1 (P3), partially 3 (P1, P4, P5), still_unresolved 1 (P2, major).

## Net assessment (arbitro)
La matematica locale è corretta (ρ, costante di strato 4log(2cosh(ρ/2)), resti del Lemma 2, integrale di OPA-C1 = 1.2102 a t = 2). Il punto più forte dell'attacco è corretto nella sostanza: il tasso **uniforme** in t non è Θ(ν), e ciò segue rigorosamente (nel senso limsup_ν sup_t) da OPA-T1 + la forma chiusa di OPA-C1 (Λ(t) ~ 2log(1/(t−t*))). L'attacco eccede su: (a) cosa chiede S4T-Q1 (a t fissato, letteralmente); (b) le costanti non quantitative, che non toccano un Θ(ν) a t fissato. Quel che cade è la presentazione/portata: r. 28 omette "a t fissato" e "non uniformemente". Il claim va declassato nella formulazione, non respinto: "S4T-Q1 risolto a ogni t > t* fissato non degenere sotto (H_t): esattamente Θ(ν) con costante Λ(t); non uniforme in t; il log ricompare ai tempi degeneri". Fix testuale, non matematico.

## Top action items (arbitro)
1. Riscrivere r. 2 e 28: "a t fissato, non uniforme in t"; aggiungere limsup_{ν→0} sup_{t∈(t*,T]} ‖S(t)u₀−S_B(t)u₀‖₁/ν = ∞ (da OPA-T1 + OPA-C1) come riconciliazione con Tang–Teng.
2. (H_t) verificata solo per ε sin x; genericità APERTA o da dimostrare; Rischio (3) → congettura.
3. Spostare la divergenza Λ(t) ~ 2log(1/(t−t*)) da OPA-R1 (non dimostrata) a un enunciato dimostrato legato a OPA-C1.

## Verdetto (calcolato da S-CHECK-15 con la tabella della skill, non dall'arbitro)
≥ 1 still_unresolved a severità major, nessuno critical ⇒ **WARN** (reason_code: unresolved_major_or_minor). Fix obbligatorio: T1-1 (portata) nell'audit.
