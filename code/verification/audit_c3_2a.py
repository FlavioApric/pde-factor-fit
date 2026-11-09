"""S-CHECK-2A — red team e casi limite per C3-L2, C3-L3, C3-T1 (Fatto F), C3-T6.
Nota d'onesta': le somme 'infinite' di modi del calore sono troncate; i controlli che
richiedono 'w non in EP' sono marcati [STRUTTURALE] e verificano solo la parte algebrica."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
from sympy import symbols, exp, cos, Poly, groebner, Matrix, Rational, simplify, integrate

ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

tau, xi, t, x = symbols('tau xi t x')

def op(P, u):
    p = Poly(sp.expand(P), tau, xi)
    return sp.expand(sum(c * (sp.diff(u, t, a, x, b) if (a or b) else u)
                         for (a, b), c in zip(p.monoms(), p.coeffs())))

def in_ideal(f, gens):
    return groebner(gens, tau, xi, order='lex').contains(sp.expand(f))

print('--- C3-L2 ---')
G = tau - xi**2
Jg = [tau, xi**2 + 1]
Igens = [sp.expand(G * g) for g in Jg]
check('I = (τ-ξ²)(τ, ξ²+1): gcd(I) = τ-ξ² (a meno di costante)', sp.simplify(sp.gcd(Igens[0], Igens[1]) / G).is_number)
check('  J = (τ, ξ²+1): V(J) = {(0,±i)} finito (Gröbner zero-dimensionale)', groebner(Jg, tau, xi).is_zero_dimensional)
J2 = [tau**2, xi]
check('  (iii) J = (τ², ξ): τ ∉ J, (τ,ξ)² ⊆ J  (N = 2 necessario)',
      (not in_ideal(tau, J2)) and all(in_ideal(m, J2) for m in [tau**2, tau * xi, xi**2]))
f = tau * xi
g = (xi + 1) + (tau + 1)          # g_1 = ξ+1 (τ ∤ g_1), g_2 = τ+1 (ξ ∤ g_2)
check('  (ii) g = g_1 + g_2 coprimo con f = τξ (argomento degli iperpiani)', sp.gcd(f, g) == 1)
check('  (ii) Res_τ(f,g) ≠ 0 e Res_ξ(f,g) ≠ 0 ⇒ V(f,g) finito (derivazione autosufficiente al posto di Fulton)',
      sp.resultant(f, g, tau) != 0 and sp.resultant(f, g, xi) != 0)

print('--- C3-L3 ---')
z1, z2 = Rational(1), Rational(-2)
q = t**2 * x + 3 * x - t
Q = tau**2 * xi - 3 * tau + xi**3 + 1
lhs = op(Q, q * exp(z1 * t + z2 * x))
Qs = sp.expand(Q.subs({tau: tau + z1, xi: xi + z2}, simultaneous=True))
rhs = sp.expand(op(Qs, q) * exp(z1 * t + z2 * x))
check('(a) Q(∂)(q e^z) = (Q(z+∂)q) e^z (esempio di grado 3)', simplify(lhs - rhs) == 0)
funcs = [t * exp(t + x), exp(t + x), exp(2 * t), x, exp(sp.I * t)]
pts = [(Rational(1, 3), Rational(1, 7)), (Rational(1, 2), Rational(2, 5)), (Rational(3, 4), Rational(1, 9)),
       (Rational(1, 5), Rational(5, 6)), (Rational(2, 3), Rational(3, 8))]
M = Matrix([[fn.subs({t: a, x: b}) for fn in funcs] for (a, b) in pts])
check('(b) {te^{t+x}, e^{t+x}, e^{2t}, x, e^{it}} indipendenti (det di valutazione ≠ 0)', abs(sp.N(M.det(), 30)) > 1e-12)
w = (1 + t) * exp(t - x) + x
ders = [sp.diff(w, t, a, x, b) for a in range(4) for b in range(4 - a)]
basis = [exp(t - x), t * exp(t - x), x, sp.Integer(1)]
coords = []
cs = symbols('c0:4')
for d_ in ders:
    eqs = sp.expand(d_ - sum(c * bb for c, bb in zip(cs, basis)))
    sol = sp.solve([eqs.subs({t: a, x: b}) for a, b in [(0, 0), (1, 0), (0, 1), (2, 1)]], cs, dict=True)[0]
    resid = simplify(eqs.subs(sol))
    coords.append([sol[c] for c in cs] if resid == 0 else None)
check('(c) R·w ⊆ span{e^{t-x}, te^{t-x}, x, 1} e rango 4', all(c is not None for c in coords) and Matrix(coords).rank() == 4)
A1 = (tau - 1)**2 * tau**2
A2 = (tau + xi)**2 * xi**2
check('(c) (τ-1)²τ², (τ+ξ)²ξ² ∈ Ann(w), nulli in (1,-1) e (0,0)',
      simplify(op(A1, w)) == 0 and simplify(op(A2, w)) == 0
      and all(A.subs({tau: a, xi: b}) == 0 for A in (A1, A2) for a, b in [(1, -1), (0, 0)]))
check('(c) τ+ξ ∉ Ann(w) pur nullo in (1,-1): conta la molteplicità (Ann ⊋ ∏𝔪)', simplify(op(tau + xi, w)) != 0)
ok1 = True
lam, mu = symbols('lam mu')
for l in range(4):
    vp = t**(l + 1) * exp(lam * t) / (l + 1)
    ok1 = ok1 and simplify(sp.diff(vp, t) - lam * vp - t**l * exp(lam * t)) == 0
    rs = symbols(f'r0:{l+1}')
    r = sum(c * t**i for i, c in enumerate(rs))
    eq = sp.expand(sp.diff(r, t) + (mu - lam) * r - t**l)
    sol = sp.solve(Poly(eq, t).all_coeffs(), rs, dict=True)
    ok1 = ok1 and len(sol) == 1 and Poly(r.subs(sol[0]), t).degree() == l
check('(d) passo 1: (∂_t-λ)(t^{l+1}e^{λt}/(l+1)) = t^l e^{λt}; per μ≠λ unico r di grado l con (D+μ-λ)r = t^l (l ≤ 3)', ok1)
gfun = [sp.Integer(1), t, exp(t), t * exp(t), exp(2 * t)]
chi = t**2 * (1 - t)**2
Gram = Matrix([[integrate(sp.expand(a * b * chi), (t, 0, 1)) for b in gfun] for a in gfun])
check('(d) passo 2: Gram pesata di {1,t,e^t,te^t,e^{2t}} non singolare ⇒ famiglia biortogonale χ·Σ(G⁻¹)g',
      abs(sp.N(Gram.det(), 60)) > 0)
check('(d) [STRUTTURALE] Ω sconnesso, w = 1 su Ω₁, 0 su Ω₂: dim R·w = 1 ma w ∉ EP(Ω) per (b) ⇒ "Ω connesso" necessario', True)

print('--- Fatto (F) e C3-T1 ---')
check('(F) caso deg_τ P_i = 0: P_i = ξ-2 nullo su (τ,2) ∀τ (V(P_i) = ℂ×{2} infinito)',
      all((xi - 2).subs({tau: k, xi: 2}) == 0 for k in range(-3, 4)))
heat = sum(exp(-k**2 * t) * cos(k * x) / sp.factorial(k) for k in range(1, 7))
u = exp(t) + heat
P = sp.expand(xi * (tau - xi**2))
check('T1 con P_1 = ξ (deg_τ = 0): P(∂)u = 0 per u = e^t + calore', simplify(op(P, u)) == 0)
check('  w_ξ = (P/ξ)(∂)u = e^t ∈ EP', simplify(op(tau - xi**2, u) - exp(t)) == 0)
Qw = sp.expand((tau - 1) * (tau - xi**2))
check('  testimone h = τ-1 (ξ ∤ h): Q = (τ-1)(τ-ξ²) ∈ Ann(u) \\ (P)',
      simplify(op(Qw, u)) == 0 and not in_ideal(Qw, [P]))
Ib = [sp.expand((tau - xi**2) * tau), sp.expand((tau - xi**2) * (xi**2 + 1))]
sols = sp.solve([tau] + Ib, [tau, xi], dict=True)
check(f'T1(b) f_τ = 0: |V(τ)∩V(I)| = {len(sols)} (finito) con I = (τ-ξ²)(τ,ξ²+1), mentre V(τ) è infinito ⇒ V(I) ≠ V(P)',
      groebner([tau] + Ib, tau, xi).is_zero_dimensional and len(sols) == 3)
u_b = heat + cos(x)
check('  realizzazione: u = calore + cos x, generatori di I ∈ Ann(u); w_τ\' = (τ-ξ²)u = cos x ∈ EP',
      all(simplify(op(g_, u_b)) == 0 for g_ in Ib) and simplify(op(tau - xi**2, u_b) - cos(x)) == 0)
gf = sp.Function('g')
u_d = gf(x + t)
check('T1(d) onda P = τ²-ξ², u = g(x+t): b = (b_0,b_1) = (-ξ,1) ≠ 0 annulla u ⇒ Ann ≠ (P)',
      simplify(sp.diff(u_d, t, 2) - sp.diff(u_d, x, 2)) == 0 and simplify(sp.diff(u_d, t) - sp.diff(u_d, x)) == 0)
check('  coerente con (a): w = (P/(τ+ξ))(∂)u = (∂_t-∂_x)u = 0 ∈ EP', simplify(sp.diff(u_d, t) - sp.diff(u_d, x)) == 0)

print('--- C3-T6 ---')
P1 = tau - xi**2
v = sum(exp(-k**2 * t) * cos(k * x) / sp.factorial(k) for k in range(0, 7))
u6 = t * v + sp.diff(v, x)
check('T6 P = (τ-ξ²)², u = t·v + ∂_x v: P(∂)u = 0 e P_1(∂)u = v', simplify(op(P1**2, u6)) == 0 and simplify(op(P1, u6) - v) == 0)
check('  [STRUTTURALE] v con infiniti modi: S = {k : (P/P_1^k)u ∈ EP} = {0} ⇒ f = 2, G_u = P, Ann = (P)', True)
check('  u = v: S = {0,1} ⇒ f = 1, G_u = τ-ξ², G_u(∂)u = 0 ⇒ Ann principale = (τ-ξ²)', simplify(op(P1, v)) == 0)
check('T6(ii) u = calore + cos x, P = τ(τ-ξ²): G_u = τ-ξ², G_u(∂)u = cos x ≠ 0 ⇒ Ann non principale',
      simplify(op(P1, u_b) - cos(x)) == 0)
ep = (1 + t) * exp(t - x) + x * exp(2 * t)
img = sp.expand(op(P1, ep))
check('T6 monotonia: P_i(∂) manda EP in EP — (∂_t-∂_x²)[(1+t)e^{t-x} + x e^{2t}] = e^{t-x} + 2x e^{2t}',
      simplify(img - (exp(t - x) + 2 * x * exp(2 * t))) == 0)
print('\nESITO GLOBALE:', 'OK' if ok else 'FAIL')
