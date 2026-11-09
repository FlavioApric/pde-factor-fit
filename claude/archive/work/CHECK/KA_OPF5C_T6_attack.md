# KA attack report: OPF5C-L9 and OPF5C-T6

Source read: `work/CHECK/KA_OPF5C_T6_input.md` only. Check script: `work/CHECK/sympy/s19ka_t6_checks.py`.

## Attacks on L9

### L9-A1. Regularity of g: C^1 vs C^{1,1}. Outcome: KILLED (as stated). Severity: MAJOR for L9, harmless for T6.
The proof uses |g(w)| <= C|w|^2 (the weight (1+sigma-x1)^{-2n}) and |g(w)-g(w')| <= C rho |w-w'|. Neither follows from g in C^1 with Dg(0)=0. That hypothesis gives only |g(w)-g(w')| <= omega(rho)|w-w'|, with omega(rho) -> 0 arbitrarily slowly. With only (1+sigma)^{-n} decay of the integrand, the centre-unstable integral int_x^inf (1+sigma-x)^m (1+sigma-x1)^{-n} dsigma is about (1+x-x1)^{m+1-n}, so m+1 powers are lost and T_xi does not map X_n into itself.

Explicit counterexample to (i). Take dimension 1, A = 0 (so s = 0), and g(z) = -z/(2 log(1/z)) for z > 0, extended oddly, with g(0) = 0.
- g is C^1 with g'(z) = (log z - 1)/(2 log^2 z), which tends to 0. So Dg(0) = 0. But g' is not Hoelder: g'/z^{0.1} tends to -infinity.
- z(x) = exp(-sqrt x) solves z' = g(z) exactly (sympy residual 0).
- z decays faster than every power of x, yet z is not identically 0. L9(i) predicts z = 0 eventually when s = 0.

Repair: assume g in C^{1,alpha} near 0 for some alpha > 0 (C^{1,1} or C^2 is simplest). Then |g(w)-g(w')| <= C(|w|+|w'|)^alpha |w-w'|, the weight becomes (1+sigma)^{-(1+alpha)n}, and the argument closes for n with alpha n > m+1. Sanity check in the scalar case: if |g| <= C|z|^{1+alpha} then (log|z|)' >= -C|z|^alpha, which is integrable, so super-polynomial decay is impossible unless z = 0.
In T6, g is real-analytic with g = O(|z|^2), so T6 is unaffected.

### L9-A2. Part (ii) under C^1. Outcome: SURVIVED.
The proof as written uses the quadratic bound. With only C^1, the bound |g(z)| <= omega(rho)|z| gives ||z||_beta <= C omega(rho)(beta-beta')^{-1} ||z||_beta. Here omega(rho) -> 0 as x1 -> infinity, so (ii) holds even for C^1. The written proof needs C^{1,1}. Severity MINOR. Repair: replace the quadratic estimate with the linear estimate that uses omega.

### L9-A3. Lyapunov–Perron setup, the representation of P_cu z, and uniqueness in the weighted ball. Outcome: SURVIVED (under C^{1,alpha}).
I checked the following:
- The boundary term e^{A(x-y)} P_cu z(y) tends to 0 because of super-polynomial decay. This covers centre directions, including purely imaginary roots, through the bound (1+|x|)^m.
- The kernel inequalities hold.
- ||z||_{n,x1} tends to 0 as x1 -> infinity.
- w*_xi lies in the same ball for the same operator T_xi, with the same xi = P_s z(x1).
- The constants do not depend on x1, because the system is autonomous.
The case s = 0 gives the fixed point 0. No gap.

### L9-A4. Exponential rate. Outcome: SURVIVED.
gamma' < gamma'' < gamma is used consistently. Resonant x^k e^{-gamma x} terms are compatible with the claim.

**Verdict L9: SURVIVES WITH FIXES.** The hypothesis must be strengthened to g in C^{1,alpha} (or C^{1,1}). As stated, with g only C^1, part (i) is false (explicit counterexample above). Part (ii) is true as stated but needs a modified proof.

## Attacks on T6

### T6-A1. Normal form, implicit function theorem, and the domain of the germ. Outcome: SURVIVED.
alpha != 0 makes the zero set a graph y_K = phi(y_0..y_{K-1}). The linear part of phi is -sum_{j<K} (p_j/alpha) y_j, so A is the companion matrix of l/alpha, with deg l = K. g is analytic and O(|z|^2). K = 0 is trivial (u = 0 near infinity).

### T6-A2. Complex-coefficient p. Outcome: GAP (statement precision). Severity: MINOR.
Because the jet is real, Re p and Im p both lie in J_u. Since alpha != 0, at least one of them has a nonzero top coefficient. The proof then works with that real part, so s, n_u and l in (a)–(c) are those of the chosen real relation, not of l_p = l_Re + i l_Im. The Corollary (ii), "every relation ... has >= 2 roots of l in each half-plane", is therefore ambiguous for complex p.

I found no counterexample for multi-solitons. Suppose two real relations of order k have nonsingular origin. Subtracting suitable multiples gives a nonsingular relation of lower order. So the linear parts of nonsingular relations are tied to the Novikov l_N. Complex combinations such as (a+bz) l_N keep l_N as a factor, so they still have N roots in each half-plane. But the general complex statement is not proved.

Repair: state T6 for real p. For complex p, define l as the l of Re p or Im p, whichever has nonzero alpha. Alternatively, restrict Corollary (ii) to real relations.

### T6-A3. (a) and the cases s = 0 or n_u = 0. Outcome: SURVIVED.
At -infinity, the change x -> -x gives the matrix -A, whose stable dimension is n_u. Vanishing on a half-line, combined with analyticity and conservation of the L^2 norm, gives u = 0. Purely imaginary roots are counted in neither s nor n_u, and L9 handles them through the polynomial weights.

### T6-A4. (b): the hypothesis covers u only, not the full jet z. Outcome: GAP. Severity: MINOR to MAJOR (missing step).
L9(ii) needs |z| = O(e^{-beta x}) for all components (u, ..., u^{(K-1)}). The hypothesis gives this for u alone. It is not automatic: interpolation loses rate.

Repair, by bootstrap. By (a), z = O(e^{-r x}) with r = gamma'. Write l(D)u = f, where f = O(e^{-(2r-eps)x}) together with its derivatives. Choose the particular solution u_p eigencomponent by eigencomponent: integrate from +infinity when Re lambda > -2r, and from x1 otherwise. Then u_p and its derivatives are O(e^{-(2r-eps)x}).
The difference u - u_p is an exponential polynomial that is O(e^{-min(beta, 2r-eps) x}). By asymptotic independence of x^k e^{lambda x}, including the oscillating ones, its derivatives satisfy the same bound up to polynomial factors.
Iterating r -> min(beta, 2r-eps) gives z = O(e^{-(beta-eps)x}). Choosing beta-eps > max|Re lambda| then lets L9(ii) apply. This works but must be written out.

### T6-A5. (c): the "two orbit arcs" step. Outcome: SURVIVED.
When s = 1, the stable root is real, because l is real and complex roots come in pairs. The flow reduced to W^ss_loc is a C^1 scalar field xi' = lambda xi + O(...) with lambda < 0. So an orbit with xi_0 > 0 decreases monotonically through all of (0, xi_0]. Hence W^ss_loc minus {0} is exactly two orbit arcs.

### T6-A6. (c): reaching q_+ from the tail (the choice of q_+). Outcome: GAP (missing argument, statement true). Severity: MINOR.
L9 places only z(x) for x >= x1(t) on W^ss_loc, and xi(x1(t)) may be smaller than xi(q_+). One must show that the jet follows B_+ backward up to q_+.
This needs the following argument. Because p is a germ, p(jet) is analytic on the connected component I(t) of {x : jet(x) in V} that contains +infinity, where V is the neighbourhood on which the zero set is a graph. Since p(jet) vanishes for x >= R(t), it vanishes on all of I(t), so the ODE holds on I(t). By ODE uniqueness, z equals the B_+ orbit as long as x stays in I(t). The left endpoint of I(t) cannot be reached while the orbit is still in W^ss_loc, which has closure inside V: by continuity the jet would lie in V there. So the jet does pass through q_+. The same argument gives the ODE on [x_2, infinity) for both u(t, . + x_2) and H_+.
Repair: insert this paragraph. For polynomial p it simplifies, since p(jet) is then entire in x.

### T6-A7. Closedness of T_± and continuity in t. Outcome: GAP (hidden assumption), repairable. Severity: MINOR.
The framework gives u in C^infinity and u(t) in S for each t. It does not give t -> u(t) continuous in L^2, and the proof uses u(t_n) -> u(t) in L^2.
Repair: use pointwise convergence, which follows from continuity of u. Suppose u(t_n, x) = H(x - c_n) -> u(t, x). If c_n is unbounded, the pointwise limit is 0, which contradicts u(t) != 0. If c_n is bounded, take a limit point c; then u(t) = H(. - c). The same argument gives continuity of c(t).
Also note that T_+ and T_- are disjoint: a translate never moves a tail from B_+ to B_-, and B_+ and B_- do not meet. So T_+ ∩ T_- ≠ ∅ cannot happen, and one of the two sets is empty. The conclusion is unchanged.

### T6-A8. Smoothness of c(t), constancy of c', and the profile ODE. Outcome: SURVIVED.
The local inverse is valid once c is continuous. From the profile equation, c'(t)H' = 6HH' + H''' with the right side independent of t, so c' is constant. Integrating twice gives H'^2 = cH^2 - 2H^3 (constants vanish by decay). OPR2-P6 then gives the 1-soliton.

### T6-A9. K <= 3 and purely imaginary roots. Outcome: SURVIVED.
s + n_u <= K <= 3, so min(s, n_u) <= 1. Imaginary roots reduce s + n_u, which only helps.

### T6-A10. Consistency with multi-solitons. Outcome: SURVIVED (numerically verified).
I took the 2-soliton tau = 1 + e^{eta1} + e^{eta2} + A12 e^{eta1+eta2} with k1 = 1, k2 = 3/2. Its KdV residual is about 1e-15. It satisfies G3 - (k1^2+k2^2) G2 + k1^2 k2^2 G1 = 0 with residual about 1e-13, where G1 = u, G2 = u'' + 3u^2, G3 = u'''' + 10uu'' + 5u'^2 + 10u^3.
So this is a nonsingular order-4 relation with l = (z^2-k1^2)(z^2-k2^2), giving s = n_u = 2. That is consistent with (c) and with Corollary (i)–(ii). (a) predicts decay rate up to k_min, which is correct. (b) predicts that decay faster than e^{-k_max x} forces u = 0, which is correct. The 1-soliton (N = 1) has min = 1, consistent with (c).
The order-3 first integrals of the Novikov system are quadratic at the origin, so they are singular. This is consistent with Corollary (i).

### T6-A11. L^2 conservation from the framework. Outcome: depends on the framework (not attacked).
Without locally uniform bounds in t, conservation is not automatic: characteristic non-uniqueness of Tychonoff type is conceivable. It is declared proved elsewhere (framework fact). Flag only.

**Verdict T6: SURVIVES WITH FIXES.** No counterexample was found, and multi-solitons are consistent. Fixes needed:
- (b) needs the bootstrap from u to the full jet (A4).
- The step that reaches q_+ needs the connected-component argument (A6).
- Closedness of T_± should use pointwise convergence instead of L^2 continuity (A7).
- l must be specified for complex p (A2).
- L9 must be cited with the C^{1,alpha} hypothesis. The analytic g satisfies it.
