# KA report: OPF5A-T1 (pre-shock L1 rate, constant Gamma at t*)
Adversarial reviewer, 26/10/2026. Source read: work/CHECK/KA_OPF5A_T1_input.md only.
Scripts (scratchpad, prefix s20ka_): s20ka_P.py, s20ka_P2.py (Pearcey constant), s20ka_CH.py (direct Cole-Hopf quadrature at t*=1, u0=sin).

## Attacks

1. **Setup / sign of u-v.** psi' = u0(a+z) - (x-a-z)/t, psi'' = J_t(a+z)/t, psi''' = u0''(a+z). u - v = -<z>/t. Checked. **SURVIVES**.

2. **Identities <psi'>=0, <z psi'>=2nu.** Integration by parts on R; psi grows quadratically (the (x-y)^2/2t term beats the linear growth of U0 when mean(u0) != 0), so boundary terms vanish. **SURVIVES**.

3. **Elimination: <z> = -nu q/p^2 + E1.** From 0 = p<z> + (q/2)<z^2> + <rho3> and 2nu = p<z^2> + (q/2)<z^3> + <z rho3>, I re-derived E1 = q^2/(4p^2)<z^3> + q/(2p^2)<z rho3> - <rho3>/p. Signs and factors are exact. Also nu q/(p^2 t) = nu t u0''/J^2 = nu kappa_t. **SURVIVES**.

4. **|E1| <= C nu^{3/2}/A^5 on O.** Uses p >= cA^2 (J >= eta + c alpha^2, t >= t*/2), |q| <= C|alpha| <= CA, and <|z|^k> <= C w^k with w = sqrt(nu)/A <= A. The three terms are w^3/A^2, w^4/A^3 (<= w^3/A^2 because w <= A) and w^3/A^2. The term <z rho3> needs moments up to k = 4, and L2(c) covers k <= 4. **SURVIVES**.

5. **L2(a),(b).** J_t = (t/t*)J_{t*} + eta holds identically. ∫_0^z (z-s)(alpha+s)^2 ds = z^4 f(alpha/z) holds. f - (1+beta^2)/50 has discriminant 1/9 - 4·0.48·(1/12 - 1/50) = -0.0105 < 0 (computed). The upper bound f z^4 <= alpha^2 z^2 + z^4/6 holds, since the quadratic alpha^2/2 - alpha z/3 + z^2/12 has negative discriminant. There is no wrap-around for |alpha| <= pi/2 and |s| <= pi/4. The tail beyond z0 follows from convexity and psi(0) = 0. **SURVIVES**.

6. **L2(c) moments.** The lower bound on the mass (psi <= 2C nu on |z| <= w) is fine. The upper bound is min(nu^{(k+1)/4}, (nu/A^2)^{(k+1)/2}). The exponential tail beyond z0 is fine. Small implicit point: the argument needs w <= z0, which holds for nu <= nu0. **SURVIVES**.

7. **∫_{A>=m} A^{-3} dalpha <= C/m^2.** If eta >= m^2, the integral is <= ∫_R (alpha^2+eta)^{-3/2} = 2/eta <= 2/m^2. Otherwise split at |alpha| = m: 2m·m^{-3} + 2∫_m^∞ alpha^{-3} = 3/m^2. Then ∫_O |E1| dx <= C nu^{3/2}·nu^{-1/2} = C nu, using J <= CA^2. **SURVIVES**.

8. **nu∫_O |kappa_t| dx = 2 nu log(1/max(sqrt nu, eta)) + O(nu), uniformly in t.** Near a*, t u0'' = ∂_a J_t, and its sign is fixed on each side for |alpha| < delta, with delta independent of t. Each side therefore contributes log J(delta) - log J(inner edge).
   - If eta >= sqrt(nu): the whole circle lies in O, J(a*) = eta, and the total is 2 log(1/eta) + O(1).
   - If eta < sqrt(nu): at the edge alpha^2 = sqrt(nu) - eta, J lies between c sqrt(nu) and C sqrt(nu).
   - Away from a*, J >= c and the integrand is bounded.
   All constants come from L2 and are uniform on [t*/2, t*]. **SURVIVES**.

9. **Inner region (Step 3).** The x-measure is <= ∫_{|alpha|<nu^{1/4}} C(eta+alpha^2) <= C nu^{3/4}, and |u-v| <= C nu^{1/4}. The product is O(nu). **SURVIVES**.

10. **Small times t <= t*/2.** J_t >= 1 - t/t* >= 1/2 globally, so psi >= z^2/(4t), and psi <= Cz^2/t gives the moments. nu q/(p^2 t) = O(nu t), E1/t = O(nu^{3/2}), and 2 nu log(1/eta) = O(nu). **SURVIVES**.

11. **Lower bound (Step 4).** |u-v| >= nu|kappa| - |E1|/t on O, combined with item 7. **SURVIVES**.

12. **Pearcey rescaling.** J(a*+alpha) = t*kappa3 alpha^2/2 (1 + O(alpha)), so psi = (kappa3/2) z^4 f(alpha/z)(1 + O(K nu^{1/4})) = (kappa3/2) nu Q, and psi/2nu -> (kappa3/4) Q. **SURVIVES**.
    - Q is 4-homogeneous, so with lambda^4 = 4/kappa3 the mean <zeta>_{kappa3 Q/4}(beta) equals lambda m(beta/lambda).
    - The inner integral (kappa3/2)∫ beta^2 |·| dbeta becomes (kappa3/2)·lambda^4 ∫_{|beta'|<K/lambda} beta'^2 |m| = F(K/lambda).
    - -4 log lambda = log(kappa3/4). The sign is correct; log(4/kappa3) would be wrong, and it is not what is used.

13. **Dominated convergence.** In zeta, domination comes from L2(b), with the tail outside |zeta| <= z0 nu^{-1/4} exponentially small. In beta over |beta| <= K, the integrand is bounded by C beta^2 via L2(c). Pointwise convergence in beta together with this bound gives the limit of the beta integral, so uniform convergence is not even needed. **SURVIVES** (exposition slightly terse).

14. **m(beta) = -beta^{-3} + O(beta^{-5}).** Step 1 with nu = 1/2, p = beta^2, q = 2beta, rho3 = zeta^3/3 exactly gives -beta^{-3}. Numerically, (m + beta^{-3})·beta^7 = -2.33427, -2.33339, -2.33334 at beta = 10, 20, 40. So in fact m = -beta^{-3} - (7/3) beta^{-7} + ..., with no beta^{-5} term. The claim holds with room to spare, and P is well defined. **SURVIVES**.

15. **K -> infinity argument.** Outer region: Gamma_out + |log nu| - 4 log K + o(1), with error <= C nu/K^2. Inner region: F(K/lambda). The sum regroups as Gamma_out - 4 log lambda + [F(K/lambda) - 4 log(K/lambda)] + O(K^{-2}) + o_nu(1), so limsup - liminf <= C K^{-2}. **SURVIVES**.

16. **Gamma_out = 4 log 2 for sin.** Here t* = 1, kappa3 = -cos(pi) = 1, and the integrand is |tan(a/2)|. ∫_0^{pi-eps} tan(a/2) da = -2 log sin(eps/2) = 2 log(2/eps) + O(eps^2), so the two sides give 4 log 2 + 4 log(1/eps). **SURVIVES**.

17. **Numerical value of P.** Independent quadrature (adaptive, symmetric, B up to 64, tail < 1e-7) gives P = 1.188654, against the claimed 1.18868, a difference of about 2.6e-5. The 5th decimal is off, but the claim "stable for B = 20, 40, 80" is close. The corrected value is Gamma = 4 log 2 - log 4 + P = 2.574948 (claimed 2.57497). **GAP (numerical), MINOR**: quote P ≈ 1.18865 or give error bars.

18. **Independent Cole–Hopf check at t* = 1, u0 = sin.** Direct quadrature of the Hopf average over a ∈ T, with dx = J da, gives (e - nu|log nu|)/nu = 2.58214 (nu = 1e-3) and 2.57727 (nu = 1e-4). This reproduces the claimed 2.5821 and 2.5773 and is consistent with the convergence to Gamma ≈ 2.5749. **SURVIVES**.

19. **E^add part.** It relies on the external OPA-T1 Step D (||h - u0|| <= 2 pi nu t ||u0''|| + O(nu^2)) and on the identification E^add = E_int^{A9}. I cannot verify these from the input. The "Gamma_out with |kappa(a(x)) - t* u0''(x)|" version for (b) is stated without proof; it is plausible, since h - u0 = nu t u0'' + O(nu^2) is smooth and the same K-argument applies. **GAP, MINOR** (dependency and short justification to be written).

20. **Hypotheses.** C^5 is more than needed (C^4 suffices for the O(eps) in log J and for rho3). Uniqueness and nondegeneracy of the minimum of u0' give J_{t*} >= c alpha^2 globally. Uniqueness of a(x) at t = t* follows from strict convexity (J vanishes only at isolated points). I found no missing hypothesis for (a)–(b). The note "(for large T, T4(iv))" is irrelevant here. **SURVIVES**.

## Overall verdict: **SURVIVES**
Every analytic step checks out: the identities, the elimination with its signs and factors, the E1 bound, the A^{-3} integral, the uniformity in t, the inner region, the Pearcey scaling with log(kappa3/4), the asymptotics of m, the K-limit, Gamma_out = 4 log 2, and the f-inequality. An independent Cole–Hopf computation matches the predicted constant. Only minor points remain:
- (i) P = 1.188654 rather than 1.18868, so Gamma(sin) = 2.574948.
- (ii) The E^add variant depends on the external OPA-T1 and needs a one-line justification for its Gamma_out.
- (iii) The DCT in beta could be stated explicitly. A side remark: m + beta^{-3} = O(beta^{-7}).
