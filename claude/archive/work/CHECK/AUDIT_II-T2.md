# AUDIT II-T2 — proiettori della compagna per fattore
Revisore: S-CHECK-2B · 25/10/2026 (2ª tornata, parte B; ripresa della tornata interrotta)
Fonte esaminata: SOLO `work/II/CHECK_REQUEST.md` (definizioni comuni F0, F1′, J; §II-T2). Nessun altro file di work/II letto.
Skill caricate: session-protocol, claim-lifecycle, proof-checker (io sono il reviewer), scientific-critical-thinking, sympy.
SymPy: `work/CHECK/sympy/audit_ii.py` → `audit_ii.out` sezione "II-T2" (**ESITO GLOBALE: OK**, 15 controlli + tabella dei poli) e `audit_round2.py/.out` sezione "II-T2" (OK).

**Verdetto: PASS-con-fix(II-T2-F1).** Un errore locale (CRITICAL) nella frase sul nucleo di Π_j in ξ₀ speciale, con correzione esatta; il resto della prova è corretto.

## 1. Enunciato canonico (Phase 0.5)
Dati: P ∈ ℂ[ξ][τ] monico di grado k; P = Q₁⋯Q_s, Q_j monici in τ, deg_τ Q_j ≥ 1, coprimi a coppie in K[τ] (K = ℂ(ξ)); B_j = P/Q_j; r_j = Res_τ(Q_j,B_j) ∈ ℂ[ξ]; C = C(ξ) compagna.
- (a) r_j ≢ 0; ∃ U_j, V_j ∈ ℂ[ξ][τ]: U_jQ_j + V_jB_j = r_j.
- (b) e_j := V_jB_j/r_j; Π_j := e_j(C) = N_j/r_j. Su K: idempotenti ortogonali, [Π_j,C] = 0, ΣΠ_j = I, Π_j = proiettore di Riesz su ker Q_j(C) lungo ⊕_{i≠j} ker Q_i(C). **"Lo stesso per ogni ξ₀ con r_j(ξ₀) ≠ 0".**
- (b′) Π_j olomorfo in ξ₀ ⟺ V(Q_j) ∩ V(B_j) non ha punti di ascissa ξ₀ (⟺ r_j(ξ₀) ≠ 0).
- (c) (τ₀,ξ₀) ∈ V(P), r_j(ξ₀) ≠ 0 ⇒ Π_j(ξ₀)v(τ₀) = v(τ₀) se Q_j(τ₀,ξ₀) = 0, = 0 altrimenti.
- (d) u = Σu_i, u_i ∈ ker_F Q_i ⇒ (V_jB_j)(∂)u = r_j(∂_x)u_j e N_j(∂_x)J(u) = r_j(∂_x)J(u_j).

## 2. Dipendenze
(a) ← proprietà del risultante (Sylvester/Cramer). (b) ← (a) + teorema cinese in K[τ] + Cayley–Hamilton (P(C) = 0, da F1′) + decomposizione primaria. (b′) ← (b) + F1′ in ogni ξ₀ + centralizzatore di una non derogatoria. (c) ← F0. (d) ← (a) + (J).

## 3. Micro-claim e verifica
| MC | Passo | Esito |
|---|---|---|
| MC-1 | r_j ≢ 0 per Q_j, B_j monici coprimi su K | OK |
| MC-2 | U_j, V_j a coefficienti in ℂ[ξ] (Cramer sulla Sylvester) | OK; riferimento: Cox–Little–O'Shea, *Ideals, Varieties, and Algorithms*, cap. 3 §6 (numero della Prop. da verificare con l'edizione) — controllo SymPy (a) |
| MC-3 | e_j ≡ 1 (Q_j), ≡ 0 (Q_i), relazioni idempotenti modulo P | OK (CRT in K[τ], PID) |
| MC-4 | f ↦ f(C) omomorfismo K[τ]/(P) → Mat_k(K) | OK (P(C) = 0 perché det(τI−C) = P) |
| MC-5 | Im Π_j = ker Q_j(C) su K | OK (Q_j(C)w = 0 ⇒ Π_jw = w; Q_j(C)Π_j = (V_jP)(C)/r_j = 0) |
| MC-6 | "questo caratterizza il proiettore spettrale" | OK con un passo implicito: un proiettore è determinato da immagine e nucleo; ker Q_j(C) = ⊕_{a: Q_j(τ_a)=0} ker(C−τ_a)^{μ_a} (decomposizione primaria; le molteplicità sono piene perché Q_j è coprimo col cofattore). → MINOR, ADD_DERIVATION (una riga) |
| MC-7 | specializzazione in ξ₀ con r_j(ξ₀) ≠ 0: Π_j(ξ₀) idempotente, commuta con C₀, Im = ker Q_j(ξ₀,C₀) | OK (e_j² − e_j ∈ P·ℂ[ξ][1/r_j][τ] perché P è monico: la divisione resta nell'anello) |
| MC-8 | "lungo ⊕_{i≠j} ker Q_i(C₀)" in ξ₀ con r_j(ξ₀) ≠ 0 | **ERRORE** (F1) |
| MC-9 | ortogonalità e ΣΠ_i = I in ξ₀ | ortogonalità OK dove Π_i, Π_j sono entrambi definiti (anzi N_iN_j ≡ 0, perché P | B_iB_j in ℂ[ξ][τ]); ΣΠ_i(ξ₀) = I solo se **tutti** gli r_i(ξ₀) ≠ 0 (F2) |
| MC-10 | (b′) ⇐ | OK: monici ⇒ Res commuta con la specializzazione; coprimi in ξ₀ ⇒ r_j(ξ₀) ≠ 0 |
| MC-11 | (b′) ⇒: identità per continuità | OK: le identità Π² = Π, [Π,C] = 0, Q_j(C)Π = 0, B_j(C)(I−Π) = 0 valgono come identità razionali, quindi sull'intorno bucato (zeri di r_j isolati); se le entrate sono olomorfe in ξ₀ passano al limite. Risposta alla domanda 3: corretto |
| MC-12 | "idempotente polinomio in C₀ ⇒ somma di proiettori spettrali" | OK, con la giustificazione da esplicitare: [Π₀,C₀] = 0 e C₀ non derogatoria (F1′ vale per ogni ξ₀) ⇒ Π₀ = g(C₀) (centralizzatore = ℂ[C₀]); g² ≡ g modulo il polinomio minimo m₀ = Π(τ−λ)^{ν_λ}; ℂ[τ]/(τ−λ)^{ν} è locale, i suoi unici idempotenti sono 0 e 1, quindi g ≡ 0 o 1 su ogni blocco. Risposta alla domanda 2: corretto; MINOR ADD_DERIVATION / ADD_REFERENCE (Horn–Johnson, *Topics in Matrix Analysis*, Thm. 4.4.17 sul centralizzatore; numerazione da verificare) |
| MC-13 | (b′) ⇒: blocco di Jordan unico di taglia μ_Q + μ_B, nucleo di Q_j(C₀) sul blocco di dimensione μ_Q | OK |
| MC-14 | (c) | OK, anche nei punti di collisione Q_i = Q_l (i,l ≠ j): verificato in ξ₀ = 0 |
| MC-15 | (d) e versione sul jet | OK (u ∈ ker P perché Q_i | P; (J) applicata a f = V_jB_j); verificato con u₁ = e^t sin x, u₂ = (t+x)³, u₃ = cos(x−t) |

## 4. Problemi trovati
- **II-T2-F1 · LOGICAL_GAP → affermazione falsa · INVALID/LOCAL · CRITICAL.** In ξ₀ con r_j(ξ₀) ≠ 0 il proiettore Π_j(ξ₀) ha nucleo **ker B_j(ξ₀,C₀)**, che in generale **non** è ⊕_{i≠j} ker Q_i(ξ₀,C₀): se due fattori Q_i, Q_l (i,l ≠ j) hanno una radice comune in ξ₀, la somma ker Q_i(C₀) + ker Q_l(C₀) non è diretta e ha dimensione minore (C₀ non derogatoria: un solo blocco di Jordan per autovalore). La prova lo nasconde perché l'identità Im(I−Π_j) = ⊕_{i≠j} ker Q_i(C) usa Π_i (i ≠ j), che non sono definiti dove r_i(ξ₀) = 0.
  *Controesempio verificato (audit_ii.py, audit_round2.py):* P = (τ−1)(τ−ξ)(τ+ξ), j = 1, ξ₀ = 0: r_1 = 1 − ξ², r_1(0) = 1 ≠ 0; Q_2(0,·) = Q_3(0,·) = τ; dim(ker Q_2(C₀) + ker Q_3(C₀)) = 1, mentre dim ker Π_1(0) = dim ker B_1(0,C₀) = 2 (e i due nuclei coincidono).
  *Fix (WEAKEN_CLAIM, correzione esatta):* "Per ogni ξ₀ con r_j(ξ₀) ≠ 0, Π_j(ξ₀) è il proiettore di Riesz di C₀ su ker Q_j(ξ₀,C₀) **lungo ker B_j(ξ₀,C₀)**, cioè sulla somma degli autospazi generalizzati delle radici di Q_j(ξ₀,·); il nucleo coincide con ⊕_{i≠j} ker Q_i(ξ₀,C₀) se e solo se anche i Q_i (i ≠ j) sono coprimi a coppie in ξ₀." Prova: Q_j(ξ₀,·) e B_j(ξ₀,·) sono coprimi (r_j(ξ₀) ≠ 0), quindi ℂ^k = ker Q_j(C₀) ⊕ ker B_j(C₀); Im Π_j(ξ₀) = ker Q_j(C₀) come in MC-5, e B_j(C₀)(I−Π_j(ξ₀)) = (U_jP)(C₀)/r_j(ξ₀) = 0 con I − Π_j(ξ₀) = (U_jQ_j)(C₀)/r_j(ξ₀) che si annulla su ker Q_j(C₀): quindi ker Π_j(ξ₀) = Im(I−Π_j(ξ₀)) = ker B_j(C₀).
- **II-T2-F2 · SCOPE (ambiguità di "lo stesso") · OVERSTATED/LOCAL · MINOR.** In ξ₀ con il solo r_j(ξ₀) ≠ 0, "somma I" non ha senso (alcuni Π_i hanno un polo). *Fix (WEAKEN_CLAIM testuale):* "Π_iΠ_l(ξ₀) = 0 se r_i(ξ₀)r_l(ξ₀) ≠ 0 (infatti N_iN_l ≡ 0); Σ_iΠ_i(ξ₀) = I se Π_i r_i(ξ₀) ≠ 0".
- **II-T2-F3 · HIDDEN_ASSUMPTION · UNCLEAR/COSMETIC · MINOR.** Le ipotesi dicono "Q_j monici in τ, coprimi in K[τ]" ma non "Q_j ∈ ℂ[ξ][τ]"; serve per (a) (risultante in ℂ[ξ]) e per (d) (Q_i(∂) operatore differenziale). Segue da Gauss (fattore monico in K[τ] di un monico in ℂ[ξ][τ]), come in II-T4. *Fix:* ADD_DERIVATION di una riga o STRENGTHEN_ASSUMPTION testuale.
- **II-T2-F4 · SCOPE (lettura di (d)) · MINOR, nessun errore.** (d) dà r_j(∂_x)u_j, non u_j: il recupero di u_j richiede di invertire r_j(∂_x), il cui nucleo contiene modi di ker Q_j ∩ ker B_j (es. e^{t+x} ∈ ker(τ−1) ∩ ker(τ−ξ), r_1(∂_x)e^{t+x} = 0). Coerente con II-T3 (unicità ⟺ V(Q_j) ∩ V(B_j) = ∅). Da ricordare a chi usa (d) come "formula di estrazione" (S-C1C2, S-P1).
- **Osservazione (non nel claim).** Nei 7 esempi testati l'ordine del polo di Π_j in ogni zero di r_j è ≤ (e in tutti i casi =) alla molteplicità dello zero: "denominatore = risultante" va letto come "insieme dei poli = zeri del risultante" (questo è dimostrato); l'uguaglianza degli ordini è solo V-ex.
Nessun FATAL. Un CRITICAL (F1) con correzione esatta.

## 5. Red team (Phase 1.5)
| Tentativo | Esito |
|---|---|
| collisione di due fattori diversi da Q_j con r_j(ξ₀) ≠ 0 | **controesempio** a "lungo ⊕ ker Q_i" (F1) |
| fattori con radici multiple ((τ−ξ)², τ), cuspide (τ² − ξ³, τ), cerchio–retta | (b′) regge: poli = zeri di r_j |
| (c) nel punto di collisione | regge |
| (d) con soluzioni non esponenziali (polinomio, seno) | regge |
| nucleo di r_j(∂_x) | non nullo: (d) non è una formula di recupero di u_j (F4) |

## 6. Acceptance gate e stato proposto
Gate dopo i fix: 0 FATAL; F1 corretto con WEAKEN_CLAIM esatto (prova data sopra); ipotesi esplicite dopo F3; controesempi tentati ✔.
**Stato proposto: DIMOSTRATO** per l'enunciato corretto (F1, F2, F3 applicati). Senza F1 l'enunciato (b) in ξ₀ è **FALSO**.
Kill-argument: già fatto da S-II inline (secondo il loro LEDGER provvisorio); non serve ripeterlo per F1 (correzione locale).
