# Contributo PR-C2a alla matrice delle componenti (PR-C2.5) — blocco T1 (ODE, C2.1–C2.5)
Agente: PR-C2a · 2026-10-22. Le righe usano gli ID di `research/PR-C2e/components_matrix.md` quando esistono; le righe **NUOVE** sono marcate ⊕.
Legenda colonne item: ✓ = il termine compare nella famiglia.

## 1. Termini × famiglie T1
| Termine | ID PR-C2e | C2.1 | C2.2 | C2.3 | C2.4 | C2.5 | Coefficiente tipico | Classe del termine isolato $\ker T$ | Classe tipica nella somma |
|---|---|---|---|---|---|---|---|---|---|
| $D$ | C-x | ✓ | ✓ | ✓ | ✓ | ✓ | costante / $a(x)$ | costanti | $e^{\lambda x}$ (con reazione) |
| $D^2$ | C-xx | ✓ | ✓ | | ✓ | ✓ | costante / $p(x)$ | $\{\alpha+\beta x\}$ | $e^{\pm\lambda x}$, trig.; Airy/Bessel con coeff. variabili |
| $D^3$, $D^4$, $D^n$ | C-xxx, C-xxxx, C-xn | ✓ | ✓ | | | | costante | polinomi di grado $<n$ | esponenziali-polinomi |
| $c\cdot$ (reazione / termine spettrale) | C-0 | ✓ | ✓ | ✓ | ✓ | ✓ (autovalore $n(n+1)$, $2n$, $\nu^2$) | costante | $\{0\}$ | fissa gli esponenti / l'autovalore |
| $x\cdot$ | V-x | | | ✓ ($a=2x$: gaussiana) | ✓ | ✓ (Airy $D^2-x$) | 1 | $\{0\}$ | Airy; $e^{-x^2}$ nel 1° ordine |
| $x^2\cdot$ | V-x2 | | | | ✓ | ✓ (Bessel, Hermite fn.) | 1 | $\{0\}$ | Bessel, oscillatore |
| $xD$ ($\theta$) | V-xdx | | | ✓ (Euler 1° ord.) | ✓ | ✓ (Hermite $-2xD$, Laguerre $-xD$) | costante | $\{1\}$ | potenze $x^r$ |
| $x^2D^2$ ⊕ | (in V-xdx come $\theta^2-\theta$) | | | | ✓ | ✓ (Bessel) | 1 | $\{1, x\}$ | $x^r$, $x^r\log x$ |
| $xD^2$ ⊕ | — | | | | ✓ | ✓ (Laguerre, Kummer) | 1 | $\{1,x\}$ | ${}_1F_1$ (singolare regolare in 0, irregolare in $\infty$) |
| $x(1-x)D^2$ ⊕ | (V-pol) | | | | ✓ | ✓ (${}_2F_1$) | 1 | $\{\alpha+\beta x\}$ (fuori da 0,1) | ${}_2F_1$, 3 punti regolari |
| $(1-x^2)D^2$ | V-pol | | | | ✓ | ✓ (Legendre/Jacobi/Geg./Cheb.) | 1 | $\{\alpha+\beta x\}$ | polinomi ortogonali classici |
| $1/x$, $1/x^2$ | V-rad | | | ✓ ($k/x$) | ✓ | ✓ (Bessel in forma $D^2+\frac1xD-\frac{\nu^2}{x^2}$) | $\nu$, $\nu^2$ | $\{0\}$ | Bessel, Euler |
| $\frac{m^2}{1-x^2}$ ⊕ | — | | | | | ✓ (Legendre ass., sferoidali) | $m^2$ | $\{0\}$ | gauge $(1-x^2)^{m/2}$ |
| $c^2x^2$ in $(1-x^2)D^2$ ⊕ | — | | | | | ✓ (sferoidali) | $c^2$ | $\{0\}$ | Heun confluente (non ipergeometrica) |
| $x^2D$ (singolarità irregolare) ⊕ | — | | | | ✓ | | 1 | $\{1\}$ | $e^{1/x}$, serie divergenti (Stokes) |
| $a(x)\cdot$ generico | V-f | | | ✓ | ✓ | | — | $\{0\}$ | $e^{-\int a}$ (1° ord.) |
| forzante $f(x)$ (inomogeneo) ⊕ | — | | ✓ | ✓ | | | — | — | $g*f$ (Green) |
| matrice $A$ (sistema $D-A$) ⊕ | (■) | | ✓ | | | | costante | — | $e^{xA}$, Jordan |
| $y^n$ (Bernoulli) ⊕ | NL (▲) | | | ✓ | | | $q$ | — | $v=y^{1-n}$ lineare |
| $y^2$ (Riccati) | (NL quadratico ▲) | | | ✓ | | | $q_2(x)$ | — | $y=-w'/(q_2w)$, lineare del 2° ordine (= Cole–Hopf ODE) |
| $f(y')$ (Clairaut / Lagrange) ⊕ | NL completamente nonlineare ▲ | | | ✓ | | | — | — | rette + inviluppo (trasformata di Legendre) |

## 2. Messaggi strutturali per la matrice
1. **Isolato vs bilanciamento** (concordo con l'osservazione 0.1 di PR-C2e).
   - Nel caso ODE ogni termine isolato ha nucleo banale (polinomi o $\{0\}$).
   - Le classi nascono dal **bilanciamento**: due termini fissano un esponente ($D-\lambda$), un punto singolare ($xD^2 + bD$) o un comportamento all'infinito ($D^2 - x$).
2. **Coefficienti costanti**: la componente naturale è il fattore primario $(D-\lambda)^m$, non il monomio $c_kD^k$. I termini si sommano nel simbolo; i nuclei si decompongono per radici (Bezout).
3. **Coefficienti polinomiali**: la componente naturale è il **dato locale nei punti singolari** (esponenti, rango), cioè il simbolo di Riemann (scheda C2.5, §0).
   - Termini con lo stesso dato locale producono la stessa classe a meno di gauge e cambio di variabile.
   - Quasi tutto C2.5 ⊂ $\{{}_2F_1, {}_1F_1, {}_0F_1\}$ ∘ (gauge, cambio di variabile). Unica eccezione nel blocco: le **sferoidali**.
4. **1° ordine con coefficiente variabile**: è sempre identificabile ($a=-(\log u)'$) e il nucleo è moltiplicativo nei termini (additivo nel log). È l'esempio più semplice di G3 che vale anche con coefficienti variabili.
