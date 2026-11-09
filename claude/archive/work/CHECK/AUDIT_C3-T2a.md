# AUDIT C3-T2(a) — annullatore di un esponenziale-polinomio (modello M1)
Revisore: S-CHECK-7 (7ª tornata) · 26/10/2026
**Fonte esaminata.** `work/C3/PROOF_PACKAGE.md` §5 [C3-T2]: ipotesi comuni, enunciato (a), prova di (a) (primo periodo della *Prova*); §1 (notazione: Ann, EP, 𝔪_z, R·w); §3 [C3-L3] (a),(b),(c) come lemmi richiamati. Stati e commenti non usati come evidenza. Per la verifica dell'uso a valle ho letto il solo passo di `work/P4/CHECK_REQUEST.md` §C P4-T2(v)(b) in cui C3-T2(a) è applicato (riga "Infine, con u = Σ_kq_ke^{⟨z_k,·⟩} …"); P4-T2 è nel perimetro di S-CHECK-6 e non è auditato qui.
**Fatti usati come dati.** C3-L3(a),(b),(c) (DIMOSTRATO, S-CHECK-2A, AUDIT_C3-T1.md).
**Skill caricate** (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol, skills-local/claim-lifecycle, proof-checker (enunciato canonico, micro-claim, checklist A–H, red team, severità a due assi), scientific-critical-thinking, sympy.
**SymPy:** `work/CHECK/sympy/audit_gammaN.py` §8 → `audit_gammaN.out` (4 controlli C3-T2(a), tutti OK; esito complessivo dello script 78/78 OK).

## 0. Verdetto
| claim | verdetto | stato proposto |
|---|---|---|
| **C3-T2(a)** | **PASS** (fix facoltativo T2a-1, INFO) | **DIMOSTRATO** |
| uso in P4-T2(v)(b) | le due proprietà usate (Ann(u) = ∩_kI_k; I_k ⊆ 𝔪_{z_k}, I_k = 𝔪_{z_k} per q_k costante) seguono da C3-T2(a) | — (il resto di P4-T2 è di S-CHECK-6) |

Nessun rilievo FATAL/CRITICAL/MAJOR/MINOR.

## 1. Enunciato canonico
∀Ω ⊂ ℝ² aperto (connesso) non vuoto, ∀M ≥ 0, ∀z_1,…,z_M ∈ ℂ² distinti, ∀q_1,…,q_M ∈ ℂ[t,x]∖{0}, con u := Σ_kq_ke^{⟨z_k,·⟩}:
Ann(u) := {Q ∈ R : Q(∂)u = 0 in 𝒟′(Ω)} = {Q : Q(z_k+∂)q_k = 0 ∀k} = ∩_kAnn(q_ke^{⟨z_k,·⟩}), e V(Ann u) = {z_1,…,z_M}.

## 2. Micro-claim ed esiti
| MC | passo | esito |
|---|---|---|
| T2a.1 | Q(∂)u = Σ_k(Q(z_k+∂)q_k)e^{⟨z_k,·⟩}, con Q(z_k+∂)q_k ∈ ℂ[t,x] | OK: C3-L3(a) termine per termine e linearità di Q(∂) |
| T2a.2 | u è liscia; Q(∂)u = 0 in 𝒟′(Ω) ⟺ la funzione continua Q(∂)u è nulla su Ω | OK (una funzione continua nulla come distribuzione è nulla) |
| T2a.3 | Σ_kp_ke^{⟨z_k,·⟩} = 0 su Ω (aperto non vuoto, z_k distinti) ⟺ tutti i p_k = 0 | OK: C3-L3(b) (ipotesi: aperto non vuoto, esponenti distinti — scaricate; i p_k possono essere nulli) |
| T2a.4 | quindi Ann(u) = {Q : Q(z_k+∂)q_k = 0 ∀k} | OK |
| T2a.5 | lo stesso argomento con un solo termine: Ann(q_ke^{⟨z_k,·⟩}) = {Q : Q(z_k+∂)q_k = 0}; quindi Ann(u) = ∩_kAnn(q_ke^{⟨z_k,·⟩}) | OK (la prova lo dice in una riga; il passaggio è lo stesso di T2a.1–T2a.3 con M = 1) |
| T2a.6 | V(Ann u) = {z_k} | OK: C3-L3(c) (ipotesi q_k ≠ 0 e z_k distinti, scaricate). Caso M = 0: u = 0, Ann = R, V = ∅ (ultima frase di L3(c)), coerente |
| T2a.7 | ipotesi minimali | la connessione di Ω non serve (L3(b) chiede solo un aperto non vuoto); q_k ≠ 0 serve solo per V(Ann u) → **T2a-1** (INFO) |

## 3. Uso a valle (P4-T2(v)(b)) — solo verifica di scarico
Lì si usa: (i) I = Ann(u) = ∩_kI_k, I_k := {Q : Q(z_k+∂)q_k = 0} — è T2a.4–T2a.5; (ii) I_k ⊆ 𝔪_{z_k} — segue da T2a.6 applicata al singolo termine (z_k ∈ V(I_k) ⇒ ogni Q ∈ I_k si annulla in z_k); (iii) per q_k = c costante, I_k = {Q : cQ(z_k) = 0} = 𝔪_{z_k} — da T2a.1 (Q(z_k+∂)c = cQ(z_k)). Le tre proprietà sono scaricate da C3-T2(a) + C3-L3. Suggerimento (non vincolante, per S-P4): citare (ii) come "C3-T2(a) applicato al singolo termine".

## 4. Red team (SymPy, audit_gammaN.py §8)
u = (1+t)e^{t−x} + 3e^{2t} + x·e^{x} (un modo con polinomio in t, uno semplice, uno con polinomio in x), grado n = 3 (10 monomi):
- nucleo del sistema diretto (Q(∂)u valutato in 40 punti casuali, SVD) = nucleo del sistema "Q(z_k+∂)q_k = 0": stessa dimensione 5, residuo 4·10⁻¹⁴ — OK;
- ogni Q della base si annulla in z_1 = (1,−1), z_2 = (2,0), z_3 = (0,1); in (0,0), (1,1), (2,1), (−1,3) qualche Q non si annulla — OK (coerente con V(Ann u) = {z_k});
- gli Ann(q_ke^{⟨z_k,·⟩}) ∩ R_{≤3} hanno dimensioni 8, 9, 8 (< 10) e la loro intersezione è Ann(u) ∩ R_{≤3} — OK;
- q_k costante: {Q : Q(z_k+∂)q_k = 0} ∩ R_{≤3} ha codimensione 1 (= 𝔪_{z_k} ∩ R_{≤3}) — OK.
Nessun controesempio (atteso: l'enunciato è una riscrittura diretta di L3(a),(b),(c)).

## 5. Fix
### T2a-1 (INFO, facoltativo; WEAKEN_ASSUMPTION non necessario)
"Ω connesso" può essere sostituito da "Ω aperto non vuoto" per (a); dichiarare che "q_k ≠ 0" serve solo per V(Ann u) = {z_k}. Nessun effetto sugli usi.

## 6. Giudizio
Prova completa e corta, che scarica le ipotesi di lemmi già DIMOSTRATI. Stato proposto: **DIMOSTRATO**. Il claim non è sul cammino critico come enunciato autonomo; serve P4-T2(v)(b) ("radicale ⟺ modi semplici").
