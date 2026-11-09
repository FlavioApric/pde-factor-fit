# Aggiudicazione kill-argument — OPF5B-T1 · S-CHECK-18 · 26/10/2026
Input: KA_OPF5B_T1_input.md (solo enunciato, ipotesi, prova §1). Attacco: KA_OPF5B_T1_attack.md (subagente indipendente, esito SURVIVES WITH MINOR FIXES).
## Punti dell'attacco e decisione
| punto | esito attacco | decisione del revisore |
|---|---|---|
| ricerca di controesempi (P in una variabile, m = 0, poligoni, fattori ripetuti) | sopravvive | confermato: la prova usa solo P ≠ 0 e la convessità |
| Passo 1 (partizione dell'unità indipendente da ε) | sopravvive | confermato |
| Passo 2 (geometria delle traslazioni locali) | sopravvive | confermato a mano: y₀+τ_i+q = (1−ε)y₀+ε(z+q/ε), z ∈ B̄(o,ρ/2); |y₀−p_i| < ρ/4+ερ/4 ≤ ρ/2 |
| Passo 5 (Leibniz, |P^{(α)}(iζ)| = |p^{(α)}| ≤ P̃, k_m/P̃ temperato) | sopravvive | confermato; Leibniz ricontrollato per P generico di grado 3 (s18, test 1) |
| Passo 6 (z = (φE)*g vicino a Ω̄, guadagno P̃) | sopravvive | confermato (è Hörmander 10.1.8 in forma elementare, L1(d)) |
| Passo 7 (P(∂)v = 0 su V_ε) | sopravvive | confermato: θ_iPũ_i = 0 su V_ε perché supp θ_i ∩ V_ε ⊂ O_i aperto; [P,Σθ_i]ũ = 0 su V |
| Passo 8 (intorno metrico convesso, mollificazione, C12-T1′) | sopravvive | confermato; ordine dei limiti corretto |
| F2 (Stein) | sopravvive | confermato: Ch. VI §3.1 Thm 5 (p. 181), convesso limitato ⇒ lipschitziano |
| F1 (Hörmander 10.2.1) | lacuna minore di forma | accolta → F5B-1: il teorema dà E/cosh(ε|x|) ∈ B_{∞,P̃}, da cui B^loc (moltiplicazione per C_c^∞) |
| P ≠ 0 implicito | minore | accolta → F5B-2 |
| conseguenze via C12-P7(a),(c) | non verificabili dall'input | verificate dal revisore sul LEDGER (C12-P7 DIMOSTRATO, ipotesi Ω lipschitziano connesso: soddisfatte) |
## Esito
**T1 SOPRAVVIVE** al kill-argument, con fix MINOR F5B-1, F5B-2. Nessun punto fatale.
