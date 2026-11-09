# AUDIT II-T7 — fattorizzazione di Gauss / Wei–Norman di e^{tC}
Revisore: S-CHECK-2B · 25/10/2026
Fonte esaminata: SOLO `work/II/CHECK_REQUEST.md` §II-T7.
Skill: session-protocol, claim-lifecycle, proof-checker, scientific-critical-thinking, sympy.
SymPy: `work/CHECK/sympy/audit_ii.py` → `audit_ii.out` sezione "II-T7" (OK, 7 controlli); `audit_round2.out` sezione "II-T7" (OK, 3 controlli).

**Verdetto: PASS-con-fix(II-T7-F1).** (a)–(d) corretti; (e) è **falso per p a coefficienti complessi** (la prova assume radici non reali coniugate); vero per p ∈ ℝ[s].

## 1. Enunciato canonico
C compagna di p (coefficienti costanti, **in ℂ**: le ipotesi non dicono reali), Φ(t) = e^{tC}, φ_j sistema fondamentale canonico, Δ_r minori principali.
(a) Φ_ij = φ_j^{(i−1)}. (b) Δ_r = W(φ_1,…,φ_r), Δ_k = e^{−p_{k−1}t}. (c) LDU esiste ⟺ Δ_r(t) ≠ 0 per r < k; unica; D = diag(Δ_r/Δ_{r−1}). (d) Coordinate di seconda specie continue su [0,T], nulle in 0, nell'ordine L·D·U fissato ⟺ Δ_r ≠ 0 su [0,T] per ogni r < k. (e) k = 2: globale su [0,∞) ⟺ radici reali e non entrambe > 0.

## 2. Micro-claim
| MC | Passo | Esito |
|---|---|---|
| MC-1 | (a) colonne = jet di φ_j | OK |
| MC-2 | (b) Wronskiano; det e^{tC} = e^{t tr C}, tr C = −p_{k−1} | OK |
| MC-3 | (c) LDU ⟺ minori principali ≠ 0 | OK (fatto standard; ADD_REFERENCE: Horn–Johnson, *Matrix Analysis*, 2ª ed., §3.5, Cor. 3.5.6 — numerazione da verificare); Δ_k ≠ 0 sempre |
| MC-4 | (d) ⇐: L unipotente = prodotto ordinato di e^{gE_ij} con g polinomiali nelle entrate, **per qualsiasi ordine fissato** | OK ma è un teorema, non ovvio: per un gruppo unipotente il prodotto dei sottogruppi radice in un ordine arbitrario è un isomorfismo di varietà (Borel, *Linear Algebraic Groups*, Prop. 14.4; numerazione da verificare). Verificato per k = 3 in 4 ordini. MINOR ADD_REFERENCE |
| MC-5 | (d) h_i ramo continuo di log(Δ_i/Δ_{i−1}), nullo in 0 | OK: Δ_r(0) = 1 (Φ(0) = I), funzione continua mai nulla su un intervallo ⇒ logaritmo continuo; continuità di g_ij perché le entrate di L, U sono razionali nelle entrate di Φ con denominatori Δ_r |
| MC-6 | (d) ⇒ | OK (non serve neppure la continuità) |
| MC-7 | (e) radici reali distinte, doppie | OK (ricontrollati anche r_1 = 0 o r_2 = 0: φ_1 ≡ 1) |
| MC-8 | (e) "Non reali α ± iβ" | **LACUNA → ERRORE**: copre solo la coppia coniugata, cioè p ∈ ℝ[s] (F1) |

## 3. Problemi trovati
- **II-T7-F1 · HIDDEN_ASSUMPTION / CASE_INCOMPLETE · INVALID/LOCAL · CRITICAL.** Con p ∈ ℂ[s] le radici non reali non sono in generale coniugate e (e) è falso.
  *Controesempio verificato:* p = (s − (1+i))(s − (2+i)). φ_1 = (λ₂e^{λ₁t} − λ₁e^{λ₂t})/(λ₂ − λ₁) si annulla ⟺ e^{−t} = λ₁/λ₂ = (3+i)/5, impossibile (lato destro non reale); numericamente min_{[0,30]}|φ_1| ≈ 0.988. Quindi la fattorizzazione è globale su [0,∞) con radici non reali. Idem radice doppia non reale r: φ_1 = e^{rt}(1 − rt) si annulla solo in t = 1/r, mai reale positivo se r ∉ ℝ.
  Rilevanza per il progetto: le compagne C(ξ) valutate in frequenza (ξ = iκ) hanno coefficienti complessi appena P contiene derivate dispari in x con coefficienti reali (avvezione, telegrafo con deriva); l'esempio dell'onda (p = s² + κ², reale) non è rappresentativo.
  *Fix (STRENGTHEN_ASSUMPTION + criterio generale):* (e) per p ∈ ℝ[s] resta com'è (la prova è corretta in quel caso). Per p ∈ ℂ[s], k = 2: radici distinte λ₁ ≠ λ₂: globale su [0,∞) ⟺ λ₁/λ₂ ∉ {e^{(λ₁−λ₂)t} : t > 0} (con λ₂ = 0 o λ₁ = 0 sempre globale); radice doppia r: globale ⟺ r ∉ (0,∞). (Prova: la stessa equazione φ_1 = 0 ⟺ e^{(λ₁−λ₂)t} = λ₁/λ₂ già scritta da S-II, senza restringere a ℝ.)
- **II-T7-F2 · esposizione · MINOR.** "Wei–Norman" nel titolo: il claim dimostra l'esistenza globale di coordinate di seconda specie nell'ordine di Gauss; che esse coincidano con la soluzione delle equazioni di Wei–Norman finché esistono segue dall'unicità di LDU (c), ma non è scritto. *Fix:* una riga (ADD_DERIVATION).
- **II-T7-F3 · scope · MINOR.** "Globale ⟺" riguarda **un ordine fissato** (Gauss L·D·U). Un altro ordine (es. U·D·L, o una base diversa di gl_k) ha altri minori come ostruzione; il claim non afferma nulla su "nessun ordine funziona". Da dire esplicitamente quando lo si usa per correggere "Wei–Norman modo per modo" (PR-C2b P4).

## 4. Red team
| Tentativo | Esito |
|---|---|
| p complesso, radici non coniugate | **controesempio** a (e) (F1) |
| radice doppia non reale | (e) falso anche qui |
| radici reali con una nulla | (e) regge |
| onda κ = 1 | Δ₁ = cos t, globale solo su [0, π/2): coerente con il caso reale |
| ordini diversi dei sottogruppi radice (k = 3) | (d) ⇐ regge in tutti e 4 |

## 5. Stato proposto
**II-T7 (a)–(d): DIMOSTRATO** (con ADD_REFERENCE MC-3, MC-4). **II-T7(e): DIMOSTRATO per p ∈ ℝ[s]; FALSO per p ∈ ℂ[s] come scritto** (controesempio verificato); dopo il fix F1 (ipotesi p reale + criterio complesso) **DIMOSTRATO**.
