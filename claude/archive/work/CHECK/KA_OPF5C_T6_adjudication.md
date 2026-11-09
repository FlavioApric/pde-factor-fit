# KA OPF5C-T6 + L9 — aggiudicazione (S-CHECK-19, 26/10/2026)

Input: `KA_OPF5C_T6_input.md`. Attacco: `KA_OPF5C_T6_attack.md` (subagente indipendente; script `sympy/s19ka_t6_checks.py`).

## L9
**Attacco L9-A1 — ACCOLTO: L9(i) è FALSO come enunciato (g solo C¹).** Controesempio dell'attaccante, verificato da me: dimensione 1, A = 0 (s = 0), g(z) = −z/(2 log(1/z)) (g(0) = 0, g ∈ C¹, g′(z) = −1/(2log(1/z)) − 1/(2log²(1/z)) → 0, quindi Dg(0) = 0; g′ non hölderiana). z(x) = e^{−√x}: z′ = −z/(2√x) = g(z) perché log(1/z) = √x; z decade più di ogni potenza ma non è definitivamente nulla, contro "z ≡ 0 definitivamente se s = 0".
La prova usa in effetti |g(w) − g(w′)| ≤ Cρ|w − w′| e |g(w)| ≤ C|w|², cioè g ∈ C^{1,1}.
**Riparazione (F5C-6, MAJOR sull'enunciato di L9, nessun effetto su T6):** ipotesi g ∈ C² (o C^{1,1}; in generale C^{1,α} con αn > m+1). In T6 g è analitica: T6 non è toccato. L9(ii) è vera anche per g ∈ C¹ ma la prova scritta usa la stima quadratica: con g ∈ C² la prova va bene così.

## T6
- **T6-A4 (b): l'ipotesi controlla solo u, L9(ii) richiede il getto z.** **ACCOLTO, MAJOR (lacuna di prova, enunciato plausibilmente vero)** (F5C-7). Riparazioni: (α) enunciare (b) e Cor.(iii) con ipotesi sul getto z = (u, …, u^{(K−1)}) = O(e^{−βx}) (vera per i dati esempio e^{−x²}·polinomio al tempo t₀, per i quali ogni derivata ha decadimento super-esponenziale); oppure (β) scrivere il bootstrap: su W^{ss}_loc, z = e^{A(x−x₁)}ζ + O(e^{−2rx}) se z = O(e^{−rx}); la prima componente della parte lineare è un polinomio-esponenziale con esponenti radici stabili di ℓ, che determina ζ (matrice compagna: osservabilità della prima componente); u = O(e^{−βx}) forza a zero i suoi modi con −Re > … e il tasso sale r → min(β, 2r − ε); dopo un numero finito di passi r > max|Re λ| e si applica L9(ii). Finché il bootstrap non è scritto, T6(b) e Cor.(iii) sono PROVA SCRITTA con lacuna.
- **Raggiungere q_± (passo "esiste x₂ con getto q_+ in x₂"):** ACCOLTO, MINOR (F5C-8). Fix: definire q_+ come getto di u(t_+,·) in un punto della sua coda dentro W^{ss}_loc; per ogni altro t con coda su B_+, le due code sono archi della stessa orbita del flusso 1-dimensionale monotono su W^{ss}_loc ∩ {ξ > 0}, quindi una è traslata dell'altra: esistono x, x′ nelle code con getti uguali, e l'unicità per l'ODE analitica più l'analiticità in x danno u(t,· + x) = u(t_+,· + x′).
- **Chiusura di T_±:** ACCOLTO, MINOR (F5C-8): la prova usa la continuità t ↦ u(t) in L², non dichiarata nel quadro (vera per soluzioni in C(ℝ, H^s)); basta la convergenza puntuale (u ∈ C^∞(ℝ×ℝ)): uno shift illimitato forza il limite puntuale 0, contro ‖u(t)‖ > 0. Inoltre T_+ ∩ T_− = ∅, quindi uno dei due è vuoto; conclusione invariata.
- **p a coefficienti complessi:** ACCOLTO, MINOR (F5C-9): ℓ, s, n_u vanno riferiti alla parte reale o immaginaria con α ≠ 0 (per p complesso, (c) con W^{ss} complessa non vale com'è scritto). Cor.(i) (ordine ≤ 3) invariato; Cor.(ii) va enunciato per relazioni reali.
- Sopravvissuti: "due archi d'orbita" (s = 1 ⇒ radice stabile reale, flusso scalare monotono); regolarità di c(t); costanza di c′; riduzione a H′² = cH² − 2H³; K ≤ 3 ⇒ min(s, n_u) ≤ 1; coerenza con i multi-solitoni (2-solitone k = (1, 3/2), relazione di Novikov d'ordine 4 con residuo ~1e−13, ℓ = (z²−k₁²)(z²−k₂²), s = n_u = 2).

## Verdetto
- **OPF5C-L9: SOPRAVVIVE CON FIX** (ipotesi g ∈ C², F5C-6). Come enunciato oggi: FALSO (i).
- **OPF5C-T6: SOPRAVVIVE.** (a), (c) e Cor.(i),(ii): PROVA SCRITTA dopo i fix MINOR F5C-8, F5C-9. (b) e Cor.(iii): lacuna MAJOR F5C-7 (riparabile, vedi sopra).
Stato proposto: T6(a),(c) **DIMOSTRATO** (dopo i fix MINOR; dipende da OPR2-P6 DIMOSTRATO e dal teorema della varietà stabile, standard, dimostrato nel testo via Lyapunov–Perron); T6(b)/Cor.(iii) **PROVA SCRITTA con lacuna** finché F5C-7 non è riparato.
