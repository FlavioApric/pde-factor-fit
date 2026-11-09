# REPORT — S5-FIX6 · 26/10/2026
(Salvato dal coordinatore: la scrittura del subagente era bloccata dall'ambiente; testo fedele alla sua risposta finale.)

Mandato: applicare in `work/OP-F5A/PROOF_PACKAGE.md` soltanto i fix decisi da `work/CHECK/AUDIT_OP-F5A.md` (S-CHECK-20, F5A-1..F5A-15), con marcatura inline `[fix <id>, S5-FIX6]` (37 occorrenze) e testo originale barrato o riportato come "testo originale". Nessuna matematica nuova oltre al testo dell'audit. Nessuno script `_vendor` eseguito; grep preliminare di "S5-FIX6": nessuna occorrenza.

## Fix applicati (id → dove)
- **Nota globale [F1]**: §0 e §6.3: "mod [F1] (= mod [K-U], fonte verificata)" (Kružkov 1970 Thm 1 §3, OPF5D-T7, S-CHECK-17).
- **F5A-1**: P = 1.188654, Γ(sin) = 2 log 2 + P = 2.57495 (T1(b), Numerica di T1, righe T1 di §1 e §5); valori Cole–Hopf indipendenti (2.5750 ± 1e-4).
- **F5A-2**: frase "Γ per E^add" barrata, ora **APERTO** (strada indicata dall'audit, non eseguita); nuovo punto aperto 5′ in §6.
- **F5A-3**: per T1 basta C⁴ (anzi C^{3,1}); C⁵ serve solo a T2/Lemma U.
- **F5A-4**: Lemma U: coefficiente −A²/(2tt*), resto O(√τ|A|⁵ + τA²); Ψ₀ invariato.
- **F5A-5**: inserito Lemma OPF5A-L3′ (enunciato e prova dall'audit); in Lemma U "L3" → "L3′".
- **F5A-6**: T2(b): code via margine (OP-ANA Lemma 1(iii)/Lemma 3) per t > t*; ψ ≥ (c₁/2)(z⁴+α²z²) per |z| ≤ z₀.
- **F5A-7**: c < 0: S₂ trasporto con inflow in L; segno nei riflessi j = 1 in L5(c) chiarito.
- **F5A-8**: portata di T5: C^{k+1} con k < ∞, oppure C^∞ piatti.
- **F5A-9**: conseguenza di L1: ψ″ = J(a+z)/t ≥ c > 0 per |z| ≤ δ.
- **F5A-10**: T4(i): Milnor 1965 → Sard 1942.
- **F5A-11**: Hirsch sostituito dalla prova della densità di Morse via Sard parametrico (m = n = 2, q = 1): DIMOSTRATA.
- **F5A-12**: densità di (SB) **CONDIZIONALE (schizzo)** (intestazione e (iv) di T4, §3, tabella §1); apertura di Morse+(SB) corretta.
- **F5A-13**: C1: portata dimostrata (0, t*+τ₀] più compatti disgiunti da T₁′, tutto (0,T] se T₁′ ∩ (0,T] = {t*} (es. sin x); resto **CONDIZIONALE** su L-loc (enunciato dall'audit). Esito OPA-Q1 e §6 aggiornati.
- **F5A-14**: T3: termine νκ nello strato e dominazione per n rami; artefatto 6.047 confermato (indice 799, rapporto ≈ 0.28).
- **F5A-15**: [TT97] CON-FONTE (Thm 3.1 del preprint 1996-025; su ℝ; numerazione pubblicata non verificata); su 𝕋 non si applica letteralmente; §6.1 "garantito da Tang–Teng" → CONDIZIONALE al trasferimento.
- **Tabelle stati** §1 e §5: nuova colonna "stato proposto dall'audit S-CHECK-20"; colonne originali etichettate "testo originale".
- **Bibliografia verificata**: nuova §7 ([TT97], [Sard42], [Milnor65], [Hirsch76], [F1] = [K-U]).

## Non applicato
- Nessuna dimostrazione nuova: L-loc e densità di (SB) restano CONDIZIONALI; "Γ per E^add" APERTO.
- LEDGER, BOARD e file del coordinatore non toccati.
